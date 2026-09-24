from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "python")
    env.pop("FIRECRAWL_API_KEY", None)
    env["FIRECRAWL_DISABLE_USER_ENV"] = "1"
    return subprocess.run(
        [sys.executable, "-m", "legends_firecrawl.cli", *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_version_and_routes_work_without_auth():
    version = run_cli("version")
    assert version.returncode == 0
    assert json.loads(version.stdout)["kit_version"] == (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    routes = run_cli("routes")
    assert routes.returncode == 0
    assert json.loads(routes.stdout)["vendor_cli"] == "firecrawl-cli@1.23.3"


def test_crawl_preview_works_without_auth():
    result = run_cli("crawl-preview", "https://example.com", "--limit", "12", "--max-depth", "1")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["dry_run"] is True
    assert payload["limit"] == 12


def test_live_command_fails_closed_without_key():
    result = run_cli("scrape", "https://example.com")
    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert "FIRECRAWL_API_KEY" in payload["error"]
    assert "MCP" not in payload["error"]


def test_vendor_integration_installers_are_blocked():
    result = run_cli("vendor", "setup", "mcp")
    assert result.returncode == 2
    assert "blocked" in json.loads(result.stdout)["error"]


def test_product_docs_never_instruct_mcp_install():
    for path in [ROOT / "README.md", ROOT / "LEGENDS.md", ROOT / "skills" / "legends-firecrawl" / "SKILL.md"]:
        text = path.read_text(encoding="utf-8").lower()
        assert "install firecrawl mcp" not in text
        assert "mcp install" not in text


def test_spine_installer_is_pinned_and_does_not_run_vendor_init():
    text = (ROOT / "bin" / "install-spine.ps1").read_text(encoding="utf-8")
    assert "firecrawl-cli@1.23.3" not in text  # composed from pinned parameter, not hidden literal command
    assert "Version = '1.23.3'" in text
    assert "firecrawl init" not in text


def test_multi_agent_installer_names_grok_and_codex():
    text = (ROOT / "bin" / "setup-multi-agent.ps1").read_text(encoding="utf-8")
    assert "Name='Grok'" in text
    assert "Name='Codex'" in text
    assert "vendor integration" in text


def test_skill_is_compact_and_has_valid_identity():
    path = ROOT / "skills" / "legends-firecrawl" / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    assert text.count("\n") < 500
    assert "name: legends-firecrawl" in text
    assert "Doctor" in text or "doctor" in text

