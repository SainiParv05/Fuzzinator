"""
dashboard_server.py
Local dashboard server for file upload, target build, PPO+LSTM runs, and report access.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from datetime import datetime
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
TARGETS_DIR = PROJECT_ROOT / "targets"
INSTRUMENTATION_DIR = PROJECT_ROOT / "instrumentation"
REPORT_DIR = PROJECT_ROOT / "data" / "reports"
CHECKPOINT_DIR = PROJECT_ROOT / "data" / "checkpoints"
PYTHON_BIN = str(PROJECT_ROOT / ".venv" / "bin" / "python")


def sanitize_stem(filename: str) -> str:
    stem = Path(filename).stem
    safe = "".join(char if char.isalnum() or char == "_" else "_" for char in stem)
    safe = safe.strip("_")
    return safe or "uploaded_target"


class DashboardState:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.current_run: dict[str, Any] = {
            "status": "idle",
            "target": "",
            "started_at": None,
            "completed_at": None,
            "steps": None,
            "mode": "PPO+LSTM",
            "stdout_tail": [],
            "return_code": None,
            "report_markdown": None,
            "report_json": None,
            "error": None,
        }
        self.last_build: dict[str, Any] = {
            "status": "idle",
            "source_path": None,
            "binary_path": None,
            "stdout": "",
            "stderr": "",
            "built_at": None,
            "return_code": None,
        }
        self.process: subprocess.Popen[str] | None = None
        self.reader_thread: threading.Thread | None = None

    def snapshot(self) -> dict[str, Any]:
        with self.lock:
            return {
                "current_run": dict(self.current_run),
                "last_build": dict(self.last_build),
                "latest_report": load_latest_report_summary(),
                "available_reports": list_recent_reports(),
            }


STATE = DashboardState()


def list_recent_reports(limit: int = 10) -> list[dict[str, Any]]:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    reports = sorted(REPORT_DIR.glob("*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    items: list[dict[str, Any]] = []
    for path in reports[:limit]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        items.append({
            "name": path.name,
            "path": str(path),
            "model": payload.get("model"),
            "status": payload.get("status"),
            "target_name": payload.get("target_name"),
            "finished_at": payload.get("finished_at"),
            "metrics": payload.get("metrics", {}),
            "markdown_report_path": payload.get("markdown_report_path"),
        })
    return items


def load_latest_report_summary() -> dict[str, Any] | None:
    recent = list_recent_reports(limit=1)
    if not recent:
        return None
    return recent[0]


def compile_target(source_filename: str) -> dict[str, Any]:
    source_path = TARGETS_DIR / source_filename
    binary_path = TARGETS_DIR / sanitize_stem(source_filename)
    cmd = [
        "bash",
        str(INSTRUMENTATION_DIR / "build_target.sh"),
        sanitize_stem(source_filename),
    ]

    result = subprocess.run(
        cmd,
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )

    with STATE.lock:
        STATE.last_build = {
            "status": "completed" if result.returncode == 0 else "failed",
            "source_path": str(source_path),
            "binary_path": str(binary_path) if result.returncode == 0 else None,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "built_at": datetime.now().isoformat(timespec="seconds"),
            "return_code": result.returncode,
        }

    return dict(STATE.last_build)


def _read_process_output(process: subprocess.Popen[str]) -> None:
    assert process.stdout is not None
    for line in process.stdout:
        with STATE.lock:
            STATE.current_run["stdout_tail"].append(line.rstrip())
            STATE.current_run["stdout_tail"] = STATE.current_run["stdout_tail"][-200:]

    return_code = process.wait()
    latest = load_latest_report_summary()

    with STATE.lock:
        STATE.current_run["status"] = "completed" if return_code == 0 else "failed"
        STATE.current_run["completed_at"] = datetime.now().isoformat(timespec="seconds")
        STATE.current_run["return_code"] = return_code
        if latest and latest.get("target_name") == Path(STATE.current_run["target"]).name:
            STATE.current_run["report_json"] = latest["path"]
            STATE.current_run["report_markdown"] = latest.get("markdown_report_path")
        if return_code != 0:
            STATE.current_run["error"] = "Run process exited with a non-zero status."
        STATE.process = None


def start_lstm_run(target_binary: str, steps: int = 200) -> dict[str, Any]:
    binary_path = TARGETS_DIR / target_binary
    if not binary_path.exists():
        raise FileNotFoundError(f"Compiled target not found: {binary_path}")

    with STATE.lock:
        if STATE.process and STATE.process.poll() is None:
            raise RuntimeError("A run is already in progress")

        cmd = [
            PYTHON_BIN,
            "agent/train_lstm.py",
            "--target",
            str(binary_path),
            "--steps",
            str(steps),
            "--device",
            "cpu",
            "--lstm-hidden",
            "128",
            "--lstm-layers",
            "1",
        ]

        process = subprocess.Popen(
            cmd,
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        STATE.process = process
        STATE.current_run = {
            "status": "running",
            "target": str(binary_path),
            "started_at": datetime.now().isoformat(timespec="seconds"),
            "completed_at": None,
            "steps": steps,
            "mode": "PPO+LSTM",
            "stdout_tail": [],
            "return_code": None,
            "report_markdown": None,
            "report_json": None,
            "error": None,
        }

        reader = threading.Thread(target=_read_process_output, args=(process,), daemon=True)
        STATE.reader_thread = reader
        reader.start()
        return dict(STATE.current_run)


class DashboardRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/status":
            self.respond_json(STATE.snapshot())
            return

        if parsed.path == "/api/report/latest":
            latest = load_latest_report_summary()
            self.respond_json({"report": latest})
            return

        if parsed.path == "/api/report":
            query = parse_qs(parsed.query)
            path = query.get("path", [None])[0]
            if not path:
                self.respond_json({"error": "Missing report path"}, status=HTTPStatus.BAD_REQUEST)
                return
            report_path = Path(path).resolve()
            try:
                report_path.relative_to(REPORT_DIR.resolve())
            except ValueError:
                self.respond_json({"error": "Report path is outside the report directory"}, status=HTTPStatus.BAD_REQUEST)
                return
            if not report_path.exists():
                self.respond_json({"error": "Report not found"}, status=HTTPStatus.NOT_FOUND)
                return
            self.respond_json(json.loads(report_path.read_text(encoding="utf-8")))
            return

        if parsed.path == "/":
            self.path = "/Dashboard.html"
        return super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        body = self.read_json_body()

        if parsed.path == "/api/upload_and_build":
            filename = body.get("filename", "")
            content = body.get("content", "")
            if not filename.endswith(".c"):
                self.respond_json({"error": "Only .c source files are supported"}, status=HTTPStatus.BAD_REQUEST)
                return

            source_stem = sanitize_stem(filename)
            source_filename = f"{source_stem}.c"
            source_path = TARGETS_DIR / source_filename
            source_path.write_text(content, encoding="utf-8")

            build_result = compile_target(source_filename)
            self.respond_json({
                "uploaded": str(source_path),
                "build": build_result,
            }, status=HTTPStatus.CREATED if build_result["status"] == "completed" else HTTPStatus.OK)
            return

        if parsed.path == "/api/run_lstm":
            target_binary = body.get("target_binary")
            try:
                if not isinstance(target_binary, str):
                    raise TypeError("target_binary must be a string")
                steps = int(body.get("steps", 200))
                run_state = start_lstm_run(target_binary, steps=steps)
            except (RuntimeError, FileNotFoundError, ValueError, TypeError) as exc:
                self.respond_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)
                return

            self.respond_json({"run": run_state}, status=HTTPStatus.ACCEPTED)
            return

        self.respond_json({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args) -> None:
        return

    def read_json_body(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length)
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def respond_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


def main() -> int:
    port = int(os.environ.get("FUZZINATOR_DASHBOARD_PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), DashboardRequestHandler)
    print(f"Dashboard server running at http://127.0.0.1:{port}")
    print("Open /Dashboard.html in the browser to use the GUI.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
