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
    for path in [ROOT / "README.md", ROOT / "skills" / "cto-legends" / "SKILL.md"]:
        text = path.read_text(encoding="utf-8").lower()
        assert "install firecrawl mcp" not in text
        assert "mcp install" not in text


def test_router_native_contract_shape():
    skills = ROOT / "skills"
    assert sorted(p.name for p in skills.iterdir()) == ["cto-legends"]
    assert (skills / "cto-legends" / "SKILL.md").is_file()
    for forbidden in ("CLAUDE.md", "GEMINI.md", "LEGENDS.md", "NEXT.md",
                      "bin/setup-multi-agent.ps1", "bin/setup-multi-agent.sh",
                      "bin/install-spine.ps1"):
        assert not (ROOT / forbidden).exists(), forbidden
    assert (ROOT / ".legends-module").read_text(encoding="utf-8").strip() == "legends-firecrawl"
    assert "Agent setup (via `cto-legends`)" in (ROOT / "README.md").read_text(encoding="utf-8")


def test_doctor_accepts_router_native_checkout(monkeypatch):
    from legends_firecrawl import cli
    monkeypatch.setattr(cli, "_vendor_cli_version", lambda: ("firecrawl", cli.EXPECTED_VENDOR_CLI))
    monkeypatch.setattr(cli, "credential_status", lambda: {"present": True})
    report, code = cli.doctor(offline=True)
    assert code == 0
    assert next(x for x in report["checks"] if x["name"] == "kit-root")["status"] == "pass"


def test_doctor_rejects_wrong_module_marker(monkeypatch, tmp_path):
    from legends_firecrawl import cli
    (tmp_path / ".legends-module").write_text("unrelated-module", encoding="utf-8")
    monkeypatch.setattr(cli, "KIT_ROOT", tmp_path)
    monkeypatch.setattr(cli, "_vendor_cli_version", lambda: ("firecrawl", cli.EXPECTED_VENDOR_CLI))
    monkeypatch.setattr(cli, "credential_status", lambda: {"present": True})
    report, code = cli.doctor(offline=True)
    assert code == 1
    assert next(x for x in report["checks"] if x["name"] == "kit-root")["status"] == "fail"

def test_doctor_accepts_installed_package_without_source_recipes(monkeypatch,tmp_path):
    from legends_firecrawl import cli
    monkeypatch.setattr(cli,'KIT_ROOT',tmp_path)
    monkeypatch.setattr(cli,'_vendor_cli_version',lambda:('firecrawl',cli.EXPECTED_VENDOR_CLI))
    monkeypatch.setattr(cli,'credential_status',lambda:{'present':True})
    report,code=cli.doctor(offline=True)
    assert code==0
    layout=next(x for x in report['checks'] if x['name']=='kit-root')
    assert layout['detail']['layout']=='installed_python'
    assert layout['detail']['recipes']=='not_bundled_in_wheel'

def test_installed_package_missing_runtime_data_rejected(monkeypatch,tmp_path):
    from legends_firecrawl import cli
    monkeypatch.setattr(cli,'KIT_ROOT',tmp_path)
    monkeypatch.setattr(cli,'load_routes',lambda:{'version':'wrong'})
    assert cli._runtime_layout_check()['status']=='fail'

def test_installed_layout_does_not_hide_vendor_or_auth_failure(monkeypatch,tmp_path):
    from legends_firecrawl import cli
    monkeypatch.setattr(cli,'KIT_ROOT',tmp_path)
    monkeypatch.setattr(cli,'_vendor_cli_version',lambda:(None,None))
    monkeypatch.setattr(cli,'credential_status',lambda:{'present':False})
    report,code=cli.doctor(offline=True)
    assert code==1 and not report['ready']
    assert next(x for x in report['checks'] if x['name']=='kit-root')['status']=='pass'
