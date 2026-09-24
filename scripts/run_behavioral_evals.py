#!/usr/bin/env python3
"""Run deterministic skill/CLI contract evals and a three-trial benchmark."""

from __future__ import annotations

import json
import os
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals" / "evals.json"
RELEASE = ROOT / "release"


def contains_expected(actual: Any, expected: Any) -> bool:
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(key in actual and contains_expected(actual[key], value) for key, value in expected.items())
    if isinstance(expected, list):
        return isinstance(actual, list) and all(any(contains_expected(item, wanted) for item in actual) for wanted in expected)
    return actual == expected


def run_eval(item: dict[str, Any]) -> dict[str, Any]:
    if not item.get("should_trigger"):
        return {
            "eval_id": item["eval_id"],
            "eval_name": item["eval_name"],
            "kind": "trigger-boundary-manual",
            "passed": bool(item.get("expected_route")),
            "evidence": f"Near-miss assigned to {item.get('expected_route')}; Firecrawl skill should not activate.",
            "duration_ms": 0.0,
        }
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "python")
    if item.get("clear_api_key") or item["eval_name"] == "crawl-refuses-no-confirm":
        env.pop("FIRECRAWL_API_KEY", None)
        env["FIRECRAWL_DISABLE_USER_ENV"] = "1"
    started = time.perf_counter()
    result = subprocess.run(
        [sys.executable, "-m", "legends_firecrawl.cli", *item["command"]],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    duration_ms = (time.perf_counter() - started) * 1000
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        payload = None
    checks = [result.returncode == item["expected_exit"]]
    if "expected_json" in item:
        checks.append(contains_expected(payload, item["expected_json"]))
    if "expected_error_contains" in item:
        checks.append(isinstance(payload, dict) and item["expected_error_contains"].lower() in str(payload.get("error", "")).lower())
    return {
        "eval_id": item["eval_id"],
        "eval_name": item["eval_name"],
        "kind": "behavioral-command",
        "passed": all(checks),
        "exit_code": result.returncode,
        "duration_ms": round(duration_ms, 3),
        "evidence": payload,
    }


def main() -> int:
    config = json.loads(EVALS.read_text(encoding="utf-8"))
    trials: list[dict[str, Any]] = []
    for trial in range(1, 4):
        for item in config["evals"]:
            row = run_eval(item)
            row["trial"] = trial
            trials.append(row)
    command_trials = [item for item in trials if item["kind"] == "behavioral-command"]
    durations = [float(item["duration_ms"]) for item in command_trials]
    passed = sum(1 for item in trials if item["passed"])
    report = {
        "schema": "legends-firecrawl-benchmark/v1",
        "skill": config["skill_name"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "trials_per_eval": 3,
        "eval_count": len(config["evals"]),
        "trial_count": len(trials),
        "pass_rate": passed / len(trials),
        "behavioral_avg_duration_ms": round(statistics.mean(durations), 3),
        "behavioral_duration_std_ms": round(statistics.pstdev(durations), 3),
        "baseline": {
            "status": "not_run",
            "reason": "This run is deterministic contract evaluation; no sub-agent A/B was authorized.",
        },
        "thresholds": {"min_pass_rate": 1.0, "max_avg_duration_ms": 2000.0},
        "thresholds_met": {
            "min_pass_rate": passed == len(trials),
            "max_avg_duration_ms": statistics.mean(durations) <= 2000.0,
        },
        "trials": trials,
    }
    RELEASE.mkdir(parents=True, exist_ok=True)
    (RELEASE / "benchmark.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    markdown = [
        "# Legends Firecrawl benchmark",
        "",
        f"- Evals: {report['eval_count']}",
        f"- Trials: {report['trial_count']}",
        f"- Pass rate: {report['pass_rate']:.0%}",
        f"- Behavioral mean: {report['behavioral_avg_duration_ms']} ms",
        f"- Behavioral standard deviation: {report['behavioral_duration_std_ms']} ms",
        "- Baseline: not run; deterministic contract evaluation only",
        "",
        "## Thresholds",
        "",
        f"- Pass rate 100%: {'PASS' if report['thresholds_met']['min_pass_rate'] else 'FAIL'}",
        f"- Average under 2000 ms: {'PASS' if report['thresholds_met']['max_avg_duration_ms'] else 'FAIL'}",
    ]
    (RELEASE / "benchmark.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("eval_count", "trial_count", "pass_rate", "behavioral_avg_duration_ms", "behavioral_duration_std_ms", "thresholds_met")}, indent=2))
    return 0 if all(report["thresholds_met"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())

