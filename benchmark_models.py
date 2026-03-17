"""
benchmark_models.py
Run reproducible PPO vs PPO+LSTM benchmark campaigns and write a report.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path


METRIC_PATTERNS = {
    "total_steps": re.compile(r"Total steps:\s+(\d+)"),
    "total_time": re.compile(r"Total time:\s+([0-9.]+)s"),
    "exec_speed": re.compile(r"Exec speed:\s+([0-9.]+) exec/sec"),
    "total_edges": re.compile(r"Total edges:\s+(\d+)"),
    "total_crashes": re.compile(r"Total crashes:\s+(\d+)"),
    "ppo_updates": re.compile(r"PPO updates:\s+(\d+)"),
}


def parse_metrics(output: str) -> dict[str, float | int]:
    metrics: dict[str, float | int] = {}
    for key, pattern in METRIC_PATTERNS.items():
        match = pattern.search(output)
        if not match:
            continue
        value = match.group(1)
        metrics[key] = float(value) if "." in value else int(value)
    return metrics


def run_command(cmd: list[str], cwd: str) -> tuple[int, str]:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    combined_output = result.stdout + ("\n" + result.stderr if result.stderr else "")
    return result.returncode, combined_output


def benchmark_model(python_bin: str,
                    script: str,
                    target: str,
                    steps: int,
                    cwd: str) -> dict[str, float | int | str]:
    started = time.time()
    return_code, output = run_command(
        [python_bin, script, "--target", target, "--steps", str(steps)],
        cwd,
    )
    elapsed_wall = time.time() - started
    metrics = parse_metrics(output)
    metrics.update(
        {
            "script": script,
            "target": target,
            "return_code": return_code,
            "wall_time": round(elapsed_wall, 3),
        }
    )
    if return_code != 0:
        metrics["error"] = output[-1200:]
    metrics["raw_output"] = output
    return metrics


def write_report(report_path: Path, baseline: list[dict], lstm: list[dict], steps: int):
    lines = [
        "# PPO vs PPO+LSTM Benchmark Report",
        "",
        f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Steps per target: {steps}",
        "",
        "## Baseline PPO",
        "",
        "| Target | Steps | Time (s) | Exec/s | Edges | Crashes | Updates |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for result in baseline:
        lines.append(
            f"| `{result['target']}` | {result.get('total_steps', 'n/a')} | "
            f"{result.get('total_time', 'n/a')} | {result.get('exec_speed', 'n/a')} | "
            f"{result.get('total_edges', 'n/a')} | {result.get('total_crashes', 'n/a')} | "
            f"{result.get('ppo_updates', 'n/a')} |"
        )

    lines.extend([
        "",
        "## PPO+LSTM",
        "",
        "| Target | Steps | Time (s) | Exec/s | Edges | Crashes | Updates |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])

    for result in lstm:
        lines.append(
            f"| `{result['target']}` | {result.get('total_steps', 'n/a')} | "
            f"{result.get('total_time', 'n/a')} | {result.get('exec_speed', 'n/a')} | "
            f"{result.get('total_edges', 'n/a')} | {result.get('total_crashes', 'n/a')} | "
            f"{result.get('ppo_updates', 'n/a')} |"
        )

    lines.extend([
        "",
        "## Comparison Summary",
        "",
    ])

    for baseline_result, lstm_result in zip(baseline, lstm):
        edge_delta = lstm_result.get("total_edges", 0) - baseline_result.get("total_edges", 0)
        crash_delta = lstm_result.get("total_crashes", 0) - baseline_result.get("total_crashes", 0)
        speed_delta = round(
            float(lstm_result.get("exec_speed", 0)) - float(baseline_result.get("exec_speed", 0)),
            1,
        )
        lines.append(
            f"- `{baseline_result['target']}`: "
            f"edge delta {edge_delta:+}, crash delta {crash_delta:+}, exec/s delta {speed_delta:+}."
        )

    lines.extend([
        "",
        "## Notes",
        "",
        "- These are short smoke benchmarks intended for apples-to-apples comparison on the same targets.",
        "- Baseline PPO uses `agent/train.py`.",
        "- PPO+LSTM uses `agent/train_lstm.py`.",
        "- For stronger statistical confidence, rerun with multiple seeds and longer campaigns.",
        "",
    ])

    report_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Benchmark PPO and PPO+LSTM.")
    parser.add_argument("--python-bin", default="./.venv/bin/python")
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument(
        "--targets",
        nargs="+",
        default=[
            "targets/target_buffer_overflow",
            "targets/target_format_string",
            "targets/target_maze",
        ],
    )
    parser.add_argument("--report", default="BENCHMARK_REPORT.md")
    parser.add_argument("--json-out", default="benchmark_results.json")
    args = parser.parse_args()

    cwd = os.getcwd()
    baseline_results = []
    lstm_results = []

    for target in args.targets:
        baseline_results.append(
            benchmark_model(args.python_bin, "agent/train.py", target, args.steps, cwd)
        )
        lstm_results.append(
            benchmark_model(args.python_bin, "agent/train_lstm.py", target, args.steps, cwd)
        )

    write_report(Path(args.report), baseline_results, lstm_results, args.steps)

    payload = {
        "baseline": baseline_results,
        "lstm": lstm_results,
        "report": args.report,
    }
    Path(args.json_out).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    concise_payload = {
        "baseline": [
            {key: value for key, value in result.items() if key != "raw_output"}
            for result in baseline_results
        ],
        "lstm": [
            {key: value for key, value in result.items() if key != "raw_output"}
            for result in lstm_results
        ],
        "report": args.report,
        "json_out": args.json_out,
    }
    print(json.dumps(concise_payload, indent=2))


if __name__ == "__main__":
    sys.exit(main())
