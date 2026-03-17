"""
benchmark_models.py
Run reproducible PPO vs PPO+LSTM benchmark campaigns and write a report.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
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
                    cwd: str,
                    seed: int,
                    extra_args: list[str] | None = None) -> dict[str, float | int | str]:
    if extra_args is None:
        extra_args = []

    started = time.time()
    return_code, output = run_command(
        [python_bin, script, "--target", target, "--steps", str(steps), "--random-seed", str(seed), *extra_args],
        cwd,
    )
    elapsed_wall = time.time() - started
    metrics = parse_metrics(output)
    metrics.update(
        {
            "script": script,
            "target": target,
            "seed": seed,
            "return_code": return_code,
            "wall_time": round(elapsed_wall, 3),
        }
    )
    if return_code != 0:
        metrics["error"] = output[-1200:]
    metrics["raw_output"] = output
    return metrics


def summarize_runs(results: list[dict]) -> dict[str, float | int | str | list[int]]:
    numeric_fields = ["total_steps", "total_time", "exec_speed", "total_edges", "total_crashes", "ppo_updates", "wall_time"]
    summary: dict[str, float | int | str | list[int]] = {
        "target": results[0]["target"],
        "script": results[0]["script"],
        "seeds": [int(result["seed"]) for result in results],
        "runs": len(results),
    }

    for field in numeric_fields:
        values = [float(result[field]) for result in results if field in result]
        if not values:
            continue
        summary[f"{field}_avg"] = round(statistics.mean(values), 3)
        summary[f"{field}_min"] = round(min(values), 3)
        summary[f"{field}_max"] = round(max(values), 3)

    failures = [result for result in results if result.get("return_code", 1) != 0]
    summary["failures"] = len(failures)
    return summary


def write_report(report_path: Path,
                 baseline_runs: list[list[dict]],
                 lstm_runs: list[list[dict]],
                 baseline_summary: list[dict],
                 lstm_summary: list[dict],
                 steps: int):
    lines = [
        "# PPO vs PPO+LSTM Benchmark Report",
        "",
        f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Steps per target: {steps}",
        f"Seeds per target: {baseline_summary[0]['seeds'] if baseline_summary else []}",
        "",
        "## Baseline PPO",
        "",
        "| Target | Runs | Avg Time (s) | Avg Exec/s | Avg Edges | Avg Crashes | Avg Updates |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for result in baseline_summary:
        lines.append(
            f"| `{result['target']}` | {result.get('runs', 'n/a')} | "
            f"{result.get('total_time_avg', 'n/a')} | {result.get('exec_speed_avg', 'n/a')} | "
            f"{result.get('total_edges_avg', 'n/a')} | {result.get('total_crashes_avg', 'n/a')} | "
            f"{result.get('ppo_updates_avg', 'n/a')} |"
        )

    lines.extend([
        "",
        "## PPO+LSTM",
        "",
        "| Target | Runs | Avg Time (s) | Avg Exec/s | Avg Edges | Avg Crashes | Avg Updates |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])

    for result in lstm_summary:
        lines.append(
            f"| `{result['target']}` | {result.get('runs', 'n/a')} | "
            f"{result.get('total_time_avg', 'n/a')} | {result.get('exec_speed_avg', 'n/a')} | "
            f"{result.get('total_edges_avg', 'n/a')} | {result.get('total_crashes_avg', 'n/a')} | "
            f"{result.get('ppo_updates_avg', 'n/a')} |"
        )

    lines.extend([
        "",
        "## Comparison Summary",
        "",
    ])

    for baseline_result, lstm_result in zip(baseline_summary, lstm_summary):
        edge_delta = float(lstm_result.get("total_edges_avg", 0)) - float(baseline_result.get("total_edges_avg", 0))
        crash_delta = float(lstm_result.get("total_crashes_avg", 0)) - float(baseline_result.get("total_crashes_avg", 0))
        speed_delta = round(
            float(lstm_result.get("exec_speed_avg", 0)) - float(baseline_result.get("exec_speed_avg", 0)),
            1,
        )
        lines.append(
            f"- `{baseline_result['target']}`: "
            f"edge delta {edge_delta:+}, crash delta {crash_delta:+}, exec/s delta {speed_delta:+}."
        )

    lines.extend([
        "",
        "## Per-Seed Results",
        "",
    ])

    for baseline_target_runs, lstm_target_runs in zip(baseline_runs, lstm_runs):
        target = baseline_target_runs[0]["target"]
        lines.append(f"### `{target}`")
        lines.append("")
        lines.append("| Model | Seed | Time (s) | Exec/s | Edges | Crashes |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
        for result in baseline_target_runs:
            lines.append(
                f"| PPO | {result['seed']} | {result.get('total_time', 'n/a')} | {result.get('exec_speed', 'n/a')} | "
                f"{result.get('total_edges', 'n/a')} | {result.get('total_crashes', 'n/a')} |"
            )
        for result in lstm_target_runs:
            lines.append(
                f"| PPO+LSTM | {result['seed']} | {result.get('total_time', 'n/a')} | {result.get('exec_speed', 'n/a')} | "
                f"{result.get('total_edges', 'n/a')} | {result.get('total_crashes', 'n/a')} |"
            )
        lines.append("")

    lines.extend([
        "",
        "## Notes",
        "",
        "- These benchmarks now aggregate multiple seeds for each target.",
        "- Baseline PPO uses `agent/train.py`.",
        "- PPO+LSTM uses `agent/train_lstm.py`.",
        "- For stronger statistical confidence, rerun with longer campaigns and more seeds.",
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
    parser.add_argument("--seeds", nargs="+", type=int, default=[1337, 2027, 4242])
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--lstm-hidden", type=int, default=None)
    parser.add_argument("--lstm-layers", type=int, default=None)
    parser.add_argument("--lstm-device", type=str, default=None)
    args = parser.parse_args()

    cwd = os.getcwd()
    baseline_results: list[list[dict]] = []
    lstm_results: list[list[dict]] = []
    baseline_summary = []
    lstm_summary = []

    baseline_extra_args: list[str] = []
    if args.device is not None:
        baseline_extra_args.extend(["--device", args.device])

    lstm_extra_args: list[str] = []
    if args.lstm_device is not None:
        lstm_extra_args.extend(["--device", args.lstm_device])
    elif args.device is not None:
        lstm_extra_args.extend(["--device", args.device])
    if args.lstm_hidden is not None:
        lstm_extra_args.extend(["--lstm-hidden", str(args.lstm_hidden)])
    if args.lstm_layers is not None:
        lstm_extra_args.extend(["--lstm-layers", str(args.lstm_layers)])

    for target in args.targets:
        target_baseline_runs = []
        target_lstm_runs = []

        for seed in args.seeds:
            target_baseline_runs.append(
                benchmark_model(args.python_bin, "agent/train.py", target, args.steps, cwd, seed, baseline_extra_args)
            )
            target_lstm_runs.append(
                benchmark_model(args.python_bin, "agent/train_lstm.py", target, args.steps, cwd, seed, lstm_extra_args)
            )

        baseline_results.append(target_baseline_runs)
        lstm_results.append(target_lstm_runs)
        baseline_summary.append(summarize_runs(target_baseline_runs))
        lstm_summary.append(summarize_runs(target_lstm_runs))

    write_report(Path(args.report), baseline_results, lstm_results, baseline_summary, lstm_summary, args.steps)

    payload = {
        "baseline": baseline_results,
        "lstm": lstm_results,
        "baseline_summary": baseline_summary,
        "lstm_summary": lstm_summary,
        "report": args.report,
        "steps": args.steps,
        "seeds": args.seeds,
        "lstm_overrides": {
            "lstm_hidden": args.lstm_hidden,
            "lstm_layers": args.lstm_layers,
            "device": args.lstm_device or args.device,
        },
    }
    Path(args.json_out).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    concise_payload = {
        "baseline_summary": baseline_summary,
        "lstm_summary": lstm_summary,
        "report": args.report,
        "json_out": args.json_out,
        "steps": args.steps,
        "seeds": args.seeds,
        "lstm_overrides": payload["lstm_overrides"],
    }
    print(json.dumps(concise_payload, indent=2))


if __name__ == "__main__":
    sys.exit(main())
