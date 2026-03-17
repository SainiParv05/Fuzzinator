"""
run_report.py
Helpers for writing detailed per-run training reports.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path


def _slugify(value: str) -> str:
    slug = []
    for char in value.lower():
        if char.isalnum():
            slug.append(char)
        elif char in {"-", "_"}:
            slug.append(char)
        else:
            slug.append("_")
    return "".join(slug).strip("_") or "run"


def write_run_report(report_dir: str, report: dict) -> tuple[str, str]:
    """
    Write markdown and JSON reports for a completed training run.

    Returns:
        Tuple of (markdown_path, json_path)
    """
    os.makedirs(report_dir, exist_ok=True)

    timestamp = report["started_at"].replace(":", "-")
    target_slug = _slugify(report["target_name"])
    model_slug = _slugify(report["model"])
    base_name = f"{timestamp}_{model_slug}_{target_slug}"

    markdown_path = str(Path(report_dir) / f"{base_name}.md")
    json_path = str(Path(report_dir) / f"{base_name}.json")

    Path(json_path).write_text(json.dumps(report, indent=2), encoding="utf-8")
    Path(markdown_path).write_text(_render_markdown(report), encoding="utf-8")

    return markdown_path, json_path


def _render_markdown(report: dict) -> str:
    lines = [
        f"# Run Report: {report['model']}",
        "",
        f"Started: {report['started_at']}",
        f"Finished: {report['finished_at']}",
        f"Status: `{report['status']}`",
        "",
        "## Completion",
        "",
        f"- Requested steps: `{report['requested_steps']}`",
        f"- Completed steps: `{report['completed_steps']}`",
        f"- Completion rule: `{report['completion_rule']}`",
        "",
        "## Target",
        "",
        f"- Target binary: `{report['target_path']}`",
        f"- Seed file: `{report['seed_path']}`",
        f"- Target name: `{report['target_name']}`",
        "",
        "## Configuration",
        "",
    ]

    for key, value in report["config"].items():
        lines.append(f"- {key}: `{value}`")

    lines.extend([
        "",
        "## Final Metrics",
        "",
    ])

    for key, value in report["metrics"].items():
        lines.append(f"- {key}: `{value}`")

    lines.extend([
        "",
        "## Crashes Created In This Run",
        "",
    ])

    if report["new_crash_files"]:
        for crash_file in report["new_crash_files"]:
            lines.append(f"- `{crash_file}`")
    else:
        lines.append("- None")

    lines.extend([
        "",
        "## Notable Events",
        "",
    ])

    if report["events"]:
        for event in report["events"]:
            summary = ", ".join(f"{key}={value}" for key, value in event.items())
            lines.append(f"- {summary}")
    else:
        lines.append("- No notable events captured")

    lines.extend([
        "",
        "## Artifacts",
        "",
        f"- Final checkpoint: `{report['final_checkpoint']}`",
        f"- Crash dir: `{report['crash_dir']}`",
        f"- Markdown report: `{report.get('markdown_report_path', '')}`",
        f"- JSON report: `{report.get('json_report_path', '')}`",
    ])

    return "\n".join(lines) + "\n"
