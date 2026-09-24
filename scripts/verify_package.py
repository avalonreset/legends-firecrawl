#!/usr/bin/env python3
"""Extract the built candidate and verify it without ambient repo state."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release"


def sha256(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def run(command: list[str], cwd: Path, env: dict[str, str]) -> dict[str, object]:
    completed = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False)
    return {
        "command": command,
        "exit_code": completed.returncode,
        "stdout": completed.stdout[-2000:],
        "stderr": completed.stderr[-2000:],
    }


def main() -> int:
    package = json.loads((RELEASE / "package-receipt.json").read_text(encoding="utf-8"))
    artifact = Path(package["artifact"])
    measured = sha256(artifact)
    temp_root = Path(tempfile.mkdtemp(prefix="legends-firecrawl-clean-room-"))
    try:
        with zipfile.ZipFile(artifact) as archive:
            archive.extractall(temp_root)
        candidate = temp_root / "legends-firecrawl"
        env = os.environ.copy()
        env["PYTHONPATH"] = str(candidate / "python")
        env.pop("FIRECRAWL_API_KEY", None)
        checks = [
            run([sys.executable, "-m", "legends_firecrawl.cli", "version"], candidate, env),
            run([sys.executable, "-m", "legends_firecrawl.cli", "routes"], candidate, env),
            run([sys.executable, "-m", "legends_firecrawl.cli", "crawl-preview", "https://example.com"], candidate, env),
            run(["node", str(candidate / "alexandria-src" / "cli.js"), "audit"], candidate, env),
            run([sys.executable, "-m", "pytest", "-q"], candidate, env),
        ]
        ok = measured == package["sha256"] and all(item["exit_code"] == 0 for item in checks)
        receipt = {
            "schema": "legends-firecrawl-clean-room/v1",
            "version": package["version"],
            "artifact": str(artifact),
            "expected_sha256": package["sha256"],
            "measured_sha256": measured,
            "checks": checks,
            "temporary_root_removed": True,
            "result": "pass" if ok else "fail",
        }
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)
    (RELEASE / "clean-room-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

