"""House command-line surface for Legends Firecrawl."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .client import (
    ApiError,
    CredentialError,
    FirecrawlClient,
    SafetyError,
    _windows_user_environment,
    credential_status,
    estimate,
    load_routes,
    read_api_key_file,
    usage_summary,
)


KIT_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_VENDOR_CLI = "1.23.3"
BLOCKED_VENDOR_COMMANDS = frozenset({
    "init", "setup", "launch", "launcher", "login", "logout", "auth", "config", "mcp",
})
_CMD_META_RE = re.compile(r'[&|<>^()%!"\r\n\x00]')


def _resolve_vendor_argv(executable: str, vendor_args: list[str]) -> list[str]:
    """Resolve vendor CLI execution safely without Windows cmd.exe batch injection."""
    for arg in vendor_args:
        if any(ch in arg for ch in ("\r", "\n", "\x00")):
            raise SafetyError("Control characters are forbidden in vendor arguments.")
    exe_path = Path(executable)
    if os.name == "nt" and not exe_path.suffix:
        cmd_sibling = exe_path.with_suffix(".cmd")
        if cmd_sibling.is_file() and not cmd_sibling.is_symlink():
            exe_path = cmd_sibling
            executable = str(cmd_sibling)
    if os.name == "nt" and exe_path.suffix.lower() in {".cmd", ".bat"}:
        node_exe = shutil.which("node")
        if node_exe and exe_path.is_file() and not exe_path.is_symlink():
            try:
                shim_text = exe_path.read_text(encoding="utf-8", errors="ignore")
                m = re.search(r'"%~dp0\\([^"]*node_modules[\\/][^"]+\.c?m?js)"', shim_text, re.I)
                if m:
                    candidate = (exe_path.parent / m.group(1).replace("\\", "/")).resolve()
                    if candidate.is_file() and not candidate.is_symlink():
                        return [node_exe, str(candidate), *vendor_args]
            except OSError:
                pass
        if any(_CMD_META_RE.search(arg) for arg in vendor_args):
            raise SafetyError(
                "Refusing to pass shell metacharacters to a Windows .cmd/.bat shim."
            )
    return [executable, *vendor_args]


def _ensure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        encoding = getattr(stream, "encoding", None)
        if isinstance(encoding, str) and encoding.lower().replace("-", "") != "utf8":
            reconfigure = getattr(stream, "reconfigure", None)
            if callable(reconfigure):
                try:
                    reconfigure(encoding="utf-8", errors="replace")
                except (OSError, ValueError, AttributeError):
                    pass


def emit(payload: Any) -> None:
    _ensure_utf8_stdio()
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def _vendor_cli_version() -> tuple[str | None, str | None]:
    executable = shutil.which("firecrawl")
    if not executable:
        return None, None
    completed = subprocess.run(
        _resolve_vendor_argv(executable, ["--version"]),
        text=True,
        capture_output=True,
        check=False,
        timeout=20,
    )
    version = completed.stdout.strip() if completed.returncode == 0 else None
    return executable, version


def _runtime_layout_check() -> dict[str, Any]:
    """Wheel runtime and source recipe layouts are distinct valid installations."""
    marker = KIT_ROOT / ".legends-module"
    source_layout = marker.exists() or (KIT_ROOT / "python" / "legends_firecrawl").is_dir()
    if source_layout:
        valid = marker.is_file() and marker.read_text(encoding="utf-8").strip() == "legends-firecrawl" and (KIT_ROOT / "skills" / "cto-legends" / "SKILL.md").is_file()
        return {"name":"kit-root", "status":"pass" if valid else "fail", "detail":{"layout":"source", "path":str(KIT_ROOT), "recipes":"verified" if valid else "missing_or_invalid"}}
    try:
        routes = load_routes()
        valid = routes.get("schema") == "legends-firecrawl-routes/v1" and routes.get("version") == __version__ and isinstance(routes.get("routes"), list) and bool(routes["routes"])
    except (OSError, ValueError, AttributeError):
        valid = False
    return {"name":"kit-root", "status":"pass" if valid else "fail", "detail":{"layout":"installed_python", "path":str(Path(__file__).parent), "recipes":"not_bundled_in_wheel", "runtime_data":"verified" if valid else "missing_or_invalid"}}


def doctor(*, offline: bool = False) -> tuple[dict[str, Any], int]:
    executable, vendor_version = _vendor_cli_version()
    auth = credential_status()
    checks = [
        _runtime_layout_check(),
        {"name": "python", "status": "pass", "detail": sys.version.split()[0]},
        {
            "name": "official-firecrawl-cli",
            "status": "pass" if executable and vendor_version == EXPECTED_VENDOR_CLI else "fail",
            "detail": {"path": executable, "expected": EXPECTED_VENDOR_CLI, "observed": vendor_version},
        },
        {"name": "api-key", "status": "pass" if auth["present"] else "fail", "detail": auth},
        {"name": "mcp-runtime", "status": "pass", "detail": "not installed, not required, not checked"},
    ]
    live: dict[str, Any] = {"status": "skipped", "reason": "offline requested" if offline else "auth unavailable"}
    if not offline and auth["present"]:
        try:
            usage = FirecrawlClient(consumer="doctor").credit_usage()
            live = {"status": "pass", "credit_usage": usage}
        except (CredentialError, ApiError, SafetyError) as exc:
            live = {"status": "fail", "error": str(exc)}
        checks.append({"name": "live-credit-usage", "status": live["status"], "detail": live})
    failed = [item for item in checks if item["status"] == "fail"]
    result = {
        "schema": "legends-firecrawl-doctor/v1",
        "kit": "Legends Firecrawl",
        "version": __version__,
        "ready": not failed,
        "mode": "offline" if offline else "live",
        "checks": checks,
        "live": live,
        "remediation": (
            []
            if not failed
            else [
                "Install the pinned official spine (firecrawl-cli@1.23.3) via npm if its check failed.",
                "Set FIRECRAWL_API_KEY in your environment if auth failed.",
                "Re-run doctor. Do not install or fall back to Firecrawl MCP.",
            ]
        ),
    }
    return result, 0 if result["ready"] else 1


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _parse_valuable_sources(raw: str | None) -> list[dict[str, str]] | None:
    if not raw or not raw.strip():
        return None
    text = raw.strip()
    if text.startswith(("[", "{")):
        try:
            loaded = json.loads(text)
        except json.JSONDecodeError:
            raise SafetyError("--valuable-sources must be valid JSON or a comma-separated list of URLs") from None
        entries = loaded if isinstance(loaded, list) else [loaded]
        out: list[dict[str, str]] = []
        for entry in entries:
            if isinstance(entry, str) and entry.strip():
                out.append({"url": entry.strip()})
            elif isinstance(entry, dict) and isinstance(entry.get("url"), str) and entry["url"].strip():
                row: dict[str, str] = {"url": entry["url"].strip()}
                if isinstance(entry.get("reason"), str) and entry["reason"].strip():
                    row["reason"] = entry["reason"].strip()
                out.append(row)
        return out or None
    return [{"url": item} for item in split_csv(text)] or None


def _parse_missing_content(values: list[str] | None) -> list[dict[str, str]] | None:
    if not values:
        return None
    out: list[dict[str, str]] = []
    for raw in values:
        text = (raw or "").strip()
        if not text:
            continue
        if text.startswith(("[", "{")):
            try:
                loaded = json.loads(text)
            except json.JSONDecodeError:
                raise SafetyError("--missing-content must be valid JSON, 'topic: description', or comma-separated topics") from None
            entries = loaded if isinstance(loaded, list) else [loaded]
            for entry in entries:
                if isinstance(entry, str) and entry.strip():
                    out.append({"topic": entry.strip()})
                elif isinstance(entry, dict) and isinstance(entry.get("topic"), str) and entry["topic"].strip():
                    row: dict[str, str] = {"topic": entry["topic"].strip()}
                    if isinstance(entry.get("description"), str) and entry["description"].strip():
                        row["description"] = entry["description"].strip()
                    out.append(row)
            continue
        for part in split_csv(text):
            if ":" in part:
                topic, desc = part.split(":", 1)
                if topic.strip():
                    row = {"topic": topic.strip()}
                    if desc.strip():
                        row["description"] = desc.strip()
                    out.append(row)
            else:
                out.append({"topic": part})
    return out[:20] or None


def _parse_inline_schema(raw: str | None) -> dict[str, Any] | None:
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        raise SafetyError("Invalid JSON in --schema option") from None
    if not isinstance(parsed, dict):
        raise SafetyError("--schema must be a JSON object")
    return parsed


def _monitor_kwargs(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "monitor_id": getattr(args, "monitor_id", None),
        "check_id": getattr(args, "check_id", None),
        "name": getattr(args, "name", None),
        "cron": getattr(args, "cron", None),
        "schedule_text": getattr(args, "schedule_text", None),
        "timezone_name": getattr(args, "timezone_name", None),
        "page": getattr(args, "page", None),
        "scrape_urls": split_csv(getattr(args, "scrape_urls", None)) or None,
        "crawl_url": getattr(args, "crawl_url", None),
        "queries": split_csv(getattr(args, "queries", None)) or None,
        "search_window": getattr(args, "search_window", None),
        "max_results": getattr(args, "max_results", None),
        "include_domains": split_csv(getattr(args, "include_domains", None)) or None,
        "exclude_domains": split_csv(getattr(args, "exclude_domains", None)) or None,
        "webhook_url": getattr(args, "webhook_url", None),
        "webhook_events": split_csv(getattr(args, "webhook_events", None)) or None,
        "email_recipients": split_csv(getattr(args, "email", None)) or None,
        "retention_days": getattr(args, "retention_days", None),
        "goal": getattr(args, "goal", None),
        "state": getattr(args, "state", None),
        "limit": getattr(args, "limit", None),
        "offset": getattr(args, "offset", None),
        "skip": getattr(args, "skip", None),
        "page_status": getattr(args, "page_status", None),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lfc", description="Legends Firecrawl house spine")
    parser.add_argument(
        "--allow-custom-api-url",
        action="store_true",
        help="Allow a custom HTTPS FIRECRAWL_API_URL outside api.firecrawl.dev",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("version")
    doctor_parser = sub.add_parser("doctor")
    doctor_parser.add_argument("--offline", action="store_true")
    sub.add_parser("routes")
    route = sub.add_parser("route")
    route.add_argument("operation")
    estimate_parser = sub.add_parser("estimate")
    estimate_parser.add_argument("operation")
    estimate_parser.add_argument("--limit", type=int)
    estimate_parser.add_argument("--formats")
    sub.add_parser("cost")
    sub.add_parser("credits")
    evidence_parser = sub.add_parser("evidence", add_help=False, help="Portable offline evidence bank operations")
    evidence_parser.add_argument("args", nargs=argparse.REMAINDER)
    alexandria_parser = sub.add_parser("alexandria", add_help=False, help="Offline Alexandria catalog and bounded query routing")
    alexandria_parser.add_argument("args", nargs=argparse.REMAINDER)

    scrape = sub.add_parser("scrape")
    scrape.add_argument("url")
    scrape.add_argument("--formats", default="markdown")
    scrape.add_argument("--max-age-ms", type=int, default=86_400_000)
    scrape.add_argument("--country", default="US")
    scrape.add_argument("--full-page", action="store_true", help="include navigation and footer content")

    scrape_serp = sub.add_parser("scrape-serp", help="Scrape organic URLs from a saved legends-dataforseo SERP envelope")
    scrape_serp.add_argument("envelope", help="Saved legends-dataforseo SERP JSON (serp --output file)")
    scrape_serp.add_argument("--limit", type=int, default=10)
    scrape_serp.add_argument("--formats", default="markdown")
    scrape_serp.add_argument("--max-age-ms", type=int, default=86_400_000)
    scrape_serp.add_argument("--country", default="US")
    scrape_serp.add_argument("--full-page", action="store_true", help="include navigation and footer content")
    scrape_serp.add_argument("--confirm", action="store_true", help="required: scrapes one page per URL")
    scrape_serp.add_argument("--resolve-goto", action="store_true",
                             help="resolve google.com/goto-wrapped results via map/search before scraping (extra credits)")

    mapping = sub.add_parser("map")
    mapping.add_argument("url")
    mapping.add_argument("--limit", type=int, default=100)
    mapping.add_argument("--search")
    mapping.add_argument("--sitemap", choices=["only", "include", "skip"], default="include")
    mapping.add_argument("--include-subdomains", action="store_true")

    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=5)
    search.add_argument("--country", default="US")
    search.add_argument("--location")
    search.add_argument("--scrape-results", action="store_true")

    resolve = sub.add_parser("resolve")
    resolve.add_argument("target", help="Target domain, URL, or SERP breadcrumb string")
    resolve.add_argument("--path-hint", help="Breadcrumb slug or URL path hint to match")
    resolve.add_argument("--title", help="Page title to match on the domain")
    resolve.add_argument("--keyword", help="Search keyword context")
    resolve.add_argument("--limit", type=int, default=25)
    resolve.add_argument("--scrape", action="store_true", help="Also scrape the resolved inner URL")
    resolve.add_argument("--formats", default="markdown")
    resolve.add_argument("--country", default="US")

    for name in ("crawl-preview", "crawl"):
        crawl = sub.add_parser(name)
        crawl.add_argument("url")
        crawl.add_argument("--limit", type=int, default=25)
        crawl.add_argument("--max-depth", type=int, default=2)
        crawl.add_argument("--include-paths")
        crawl.add_argument("--exclude-paths")
        if name == "crawl":
            crawl.add_argument("--confirm", action="store_true")

    status = sub.add_parser("crawl-status")
    status.add_argument("job_id")

    developer = sub.add_parser(
        "developer",
        help="Search Firecrawl coding-agent index (GitHub issues, PRs, READMEs, curated docs)",
    )
    developer.add_argument("query")
    developer.add_argument("--limit", type=int, default=10)
    developer.add_argument("--scrape", action="store_true", help="Also scrape returned public URLs")
    developer.add_argument("--formats", default="markdown")
    developer.add_argument("--country", default="US")
    developer.add_argument("--confirm", action="store_true")
    developer.add_argument("--dry-run", action="store_true")

    research = sub.add_parser(
        "research",
        help="Search Firecrawl scientific paper abstract index (arXiv, PubMed, bioRxiv, medRxiv)",
    )
    research.add_argument("query", nargs="?", default="")
    research.add_argument("--limit", type=int, default=10)
    research.add_argument("--scrape", action="store_true", help="Also scrape returned public URLs")
    research.add_argument("--formats", default="markdown")
    research.add_argument("--country", default="US")
    research.add_argument("--mode", choices=["papers", "inspect", "related", "read", "github"], default="papers")
    research.add_argument("--authors", help="Comma-separated author substring filters")
    research.add_argument("--categories", help="Comma-separated arXiv taxonomy category filters")
    research.add_argument("--from", dest="date_from", help="Lower bound date (YYYY-MM-DD)")
    research.add_argument("--to", dest="date_to", help="Upper bound date (YYYY-MM-DD)")
    research.add_argument("--paper-id", help="Paper ID for inspect/read modes")
    research.add_argument("--seed-ids", help="Comma-separated seed paper IDs for related mode")
    research.add_argument("--intent", help="Ranking intent for related mode")
    research.add_argument("--relation-mode", choices=["similar", "citers", "references"])
    research.add_argument("--rerank", action="store_true")
    research.add_argument("--question", help="Question for read mode")
    research.add_argument("--confirm", action="store_true")
    research.add_argument("--dry-run", action="store_true")

    parse_cmd = sub.add_parser(
        "parse",
        help="Parse a local file (HTML, PDF, DOCX, DOC, ODT, RTF, XLSX, XLS) via /v2/parse",
    )
    parse_cmd.add_argument("file", help="Path to local file to parse")
    parse_cmd.add_argument("--formats", default="markdown")
    parse_cmd.add_argument("--full-page", action="store_true", help="Disable onlyMainContent")
    parse_cmd.add_argument("--query", help="Ask a question about the parsed document")
    parse_cmd.add_argument("--include-tags")
    parse_cmd.add_argument("--exclude-tags")
    parse_cmd.add_argument("--timeout-ms", type=int)
    parse_cmd.add_argument("--confirm", action="store_true")
    parse_cmd.add_argument("--dry-run", action="store_true")

    agent_cmd = sub.add_parser("agent", help="Start an AI web extraction agent via POST /v2/agent")
    agent_cmd.add_argument("prompt")
    agent_cmd.add_argument("--urls", help="Comma-separated URLs to focus extraction on")
    agent_cmd.add_argument("--model", choices=["spark-1-mini", "spark-1-pro"], default="spark-1-mini")
    agent_cmd.add_argument("--max-credits", type=int, default=25, help="Hard credit cap (1-500, default 25)")
    agent_cmd.add_argument("--schema", help="Inline JSON schema object")
    agent_cmd.add_argument("--schema-file", help="Path to JSON schema file")
    agent_cmd.add_argument("--strict-urls", action="store_true")
    agent_cmd.add_argument("--confirm", action="store_true")
    agent_cmd.add_argument("--dry-run", action="store_true")

    agent_status = sub.add_parser("agent-status", help="Check or cancel an agent job via /v2/agent/{id}")
    agent_status.add_argument("job_id")
    agent_status.add_argument("--cancel", action="store_true", help="Cancel the running agent job")
    agent_status.add_argument("--confirm", action="store_true")
    agent_status.add_argument("--dry-run", action="store_true")

    interact_cmd = sub.add_parser("interact", help="Run prompt/code or stop an interactive scrape browser session")
    interact_cmd.add_argument("scrape_id")
    interact_cmd.add_argument("--prompt")
    interact_cmd.add_argument("--code")
    interact_cmd.add_argument("--language", choices=["node", "python", "bash"], default="node")
    interact_cmd.add_argument("--timeout", type=int)
    interact_cmd.add_argument("--stop", action="store_true")
    interact_cmd.add_argument("--confirm", action="store_true")
    interact_cmd.add_argument("--dry-run", action="store_true")

    monitor_cmd = sub.add_parser("monitor", help="Manage recurring content change monitors via /v2/monitor")
    monitor_sub = monitor_cmd.add_subparsers(dest="monitor_action", required=True)
    mon_create = monitor_sub.add_parser("create")
    mon_create.add_argument("--name", required=True)
    mon_create.add_argument("--cron")
    mon_create.add_argument("--schedule", dest="schedule_text")
    mon_create.add_argument("--timezone", dest="timezone_name", default="UTC")
    mon_create.add_argument("--page")
    mon_create.add_argument("--scrape-urls")
    mon_create.add_argument("--crawl-url")
    mon_create.add_argument("--queries")
    mon_create.add_argument("--search-window")
    mon_create.add_argument("--max-results", type=int)
    mon_create.add_argument("--include-domains")
    mon_create.add_argument("--exclude-domains")
    mon_create.add_argument("--webhook-url")
    mon_create.add_argument("--webhook-events")
    mon_create.add_argument("--email")
    mon_create.add_argument("--retention-days", type=int)
    mon_create.add_argument("--goal")

    mon_list = monitor_sub.add_parser("list")
    mon_list.add_argument("--limit", type=int)
    mon_list.add_argument("--offset", type=int)

    mon_get = monitor_sub.add_parser("get")
    mon_get.add_argument("monitor_id")

    mon_update = monitor_sub.add_parser("update")
    mon_update.add_argument("monitor_id")
    mon_update.add_argument("--name")
    mon_update.add_argument("--goal")
    mon_update.add_argument("--cron")
    mon_update.add_argument("--schedule", dest="schedule_text")
    mon_update.add_argument("--timezone", dest="timezone_name")
    mon_update.add_argument("--state", choices=["active", "paused"])
    mon_update.add_argument("--retention-days", type=int)

    mon_delete = monitor_sub.add_parser("delete")
    mon_delete.add_argument("monitor_id")

    mon_run = monitor_sub.add_parser("run")
    mon_run.add_argument("monitor_id")

    mon_checks = monitor_sub.add_parser("checks")
    mon_checks.add_argument("monitor_id")
    mon_checks.add_argument("--limit", type=int)
    mon_checks.add_argument("--offset", type=int)

    mon_check = monitor_sub.add_parser("check")
    mon_check.add_argument("monitor_id")
    mon_check.add_argument("check_id")
    mon_check.add_argument("--limit", type=int)
    mon_check.add_argument("--skip", type=int)
    mon_check.add_argument("--page-status", choices=["same", "new", "changed", "removed", "error"])

    for mon_p in (mon_create, mon_list, mon_get, mon_update, mon_delete, mon_run, mon_checks, mon_check):
        mon_p.add_argument("--confirm", action="store_true")
        mon_p.add_argument("--dry-run", action="store_true")
        mon_p.add_argument("--receipt", action="store_true", help="Print archive receipt only; full response remains saved")
        mon_p.add_argument("--workspace", help="Client/project identity recorded with capture")
        mon_p.add_argument("--no-save", action="store_true", help="Skip automatic full response archive")

    sf_cmd = sub.add_parser("search-feedback", help="Submit search feedback for a searchId (free; 1-credit refund on first submit)")
    sf_cmd.add_argument("search_id")
    sf_cmd.add_argument("--rating", required=True, choices=["good", "bad", "partial"])
    sf_cmd.add_argument("--valuable-sources", help="Comma-separated URLs or JSON array of {url, reason}")
    sf_cmd.add_argument("--missing-content", action="append", help="Missing topic(s) or JSON array of {topic, description}")
    sf_cmd.add_argument("--query-suggestions")
    sf_cmd.add_argument("--confirm", action="store_true")
    sf_cmd.add_argument("--dry-run", action="store_true")

    for guarded in (scrape, resolve, scrape_serp):
        if guarded is not scrape_serp:
            guarded.add_argument("--serp-envelope", help="SERP envelope the target came from; refused unless verified")
        guarded.add_argument("--allow-unverified-serp", "--allow-suspect-serp", dest="allow_suspect_serp",
                             action="store_true",
                             help="Override the fail-closed refusal of a SERP whose serp_integrity.verified is not true "
                                  "(unverified, unprotected, suspect or unverified_decoy; loud warning)")

    for capture_parser in (
        scrape,
        scrape_serp,
        mapping,
        search,
        resolve,
        crawl,
        status,
        developer,
        research,
        parse_cmd,
        agent_cmd,
        agent_status,
        interact_cmd,
        sf_cmd,
    ):
        capture_parser.add_argument("--receipt", action="store_true", help="Print archive receipt only; full response remains saved")
        capture_parser.add_argument("--workspace", help="Client/project identity recorded with capture")
        capture_parser.add_argument("--no-save", action="store_true", help="Skip automatic full response archive")

    vendor = sub.add_parser("vendor")
    vendor.add_argument("args", nargs=argparse.REMAINDER)
    return parser


def lax_main(argv: list[str] | None = None) -> int:
    command_line = list(argv) if argv is not None else sys.argv[1:]
    pkg_dir = Path(__file__).resolve().parent
    if os.environ.get("LEGENDS_FIRECRAWL_HOME"):
        root = Path(os.environ["LEGENDS_FIRECRAWL_HOME"]).expanduser()
        script_path = root / "alexandria-src" / "cli.js"
    elif (KIT_ROOT / "alexandria-src" / "cli.js").is_file():
        script_path = KIT_ROOT / "alexandria-src" / "cli.js"
    else:
        script_path = pkg_dir / "alexandria-src" / "cli.js"
    if not script_path.is_file():
        emit({"status": "error", "message": f"Alexandria CLI not found at {script_path}. Run from a legends-firecrawl checkout or installed package."})
        return 2
    node_exe = shutil.which("node")
    if not node_exe:
        emit({"status": "error", "message": "Node.js executable ('node') not found on PATH."})
        return 2
    env = os.environ.copy()
    if not env.get("FIRECRAWL_API_KEY") and env.get("FIRECRAWL_API_KEY_FILE"):
        try:
            env["FIRECRAWL_API_KEY"] = read_api_key_file(env["FIRECRAWL_API_KEY_FILE"])
        except (CredentialError, SafetyError) as exc:
            emit({"status": "error", "message": str(exc)})
            return 2
    if not env.get("FIRECRAWL_API_KEY") and env.get("FIRECRAWL_DISABLE_USER_ENV") != "1":
        user_key = _windows_user_environment("FIRECRAWL_API_KEY")
        if user_key:
            env["FIRECRAWL_API_KEY"] = user_key
    completed = subprocess.run([node_exe, str(script_path), *command_line], env=env, check=False)
    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    command_line = argv if argv is not None else sys.argv[1:]
    if command_line and command_line[0] == 'evidence':
        from .evidence import main as evidence_main
        return evidence_main(command_line[1:])
    if command_line and command_line[0] == 'alexandria':
        return lax_main(command_line[1:])
    args = build_parser().parse_args(argv)
    if getattr(args, "allow_custom_api_url", False):
        os.environ["FIRECRAWL_ALLOW_CUSTOM_API_URL"] = "1"
    try:
        if args.command == "evidence":
            from .evidence import main as evidence_main
            return evidence_main(args.args)
        if args.command == "alexandria":
            return lax_main(args.args)
        if args.command == "version":
            emit({"kit_version": __version__, "vendor_cli_expected": EXPECTED_VENDOR_CLI})
            return 0
        if args.command == "doctor":
            result, code = doctor(offline=args.offline)
            emit(result)
            return code
        if args.command == "routes":
            emit(load_routes())
            return 0
        if args.command == "route":
            from .client import route_for

            emit(route_for(args.operation))
            return 0
        if args.command == "estimate":
            emit(estimate(args.operation, limit=args.limit, formats=split_csv(args.formats)))
            return 0
        if args.command == "cost":
            emit(usage_summary())
            return 0
        if args.command == "vendor":
            lowered = {
                str(value).strip().lower().lstrip("-")
                for value in args.args
                if str(value).strip()
            }
            if lowered & BLOCKED_VENDOR_COMMANDS:
                raise SafetyError("vendor integration installers and credential/config mutators are blocked; use the house setup scripts")
            for raw_arg in args.args:
                if any(ch in str(raw_arg) for ch in ("\r", "\n", "\x00")):
                    raise SafetyError("Control characters are forbidden in vendor arguments.")
            executable, _ = _vendor_cli_version()
            if not executable:
                raise SafetyError("official firecrawl CLI is missing; install firecrawl-cli@1.23.3 via npm")
            return subprocess.call(_resolve_vendor_argv(executable, list(args.args)))

        if args.command == "crawl-preview":
            emit(
                FirecrawlClient.crawl_preview(
                    args.url,
                    limit=args.limit,
                    max_depth=args.max_depth,
                    include_paths=split_csv(args.include_paths),
                    exclude_paths=split_csv(args.exclude_paths),
                )
            )
            return 0

        if args.command == "crawl" and not args.confirm:
            raise SafetyError("crawl is multi-page and requires --confirm after reviewing crawl-preview")

        if args.command == "developer":
            dev_plan = FirecrawlClient.developer_preview(
                args.query,
                limit=args.limit,
                scrape=args.scrape,
                formats=split_csv(args.formats),
            )
            if args.dry_run:
                emit(dev_plan)
                return 0
            if not args.confirm:
                raise SafetyError("developer search requires --confirm (or pass --dry-run to preview)")
        elif args.command == "research":
            res_plan = FirecrawlClient.research_preview(
                args.query,
                limit=args.limit,
                scrape=args.scrape,
                formats=split_csv(args.formats),
                mode=args.mode,
                authors=split_csv(args.authors),
                categories=split_csv(args.categories),
                date_from=args.date_from,
                date_to=args.date_to,
                paper_id=args.paper_id,
                seed_ids=split_csv(args.seed_ids),
                intent=args.intent,
                relation_mode=args.relation_mode,
                question=args.question,
                rerank=args.rerank,
            )
            if args.dry_run:
                emit(res_plan)
                return 0
            if not args.confirm:
                raise SafetyError("research search requires --confirm (or pass --dry-run to preview)")
        elif args.command == "parse":
            parse_plan = FirecrawlClient.parse_preview(
                args.file,
                formats=split_csv(args.formats),
                only_main_content=not args.full_page,
                query=args.query,
                include_tags=split_csv(args.include_tags),
                exclude_tags=split_csv(args.exclude_tags),
                timeout_ms=args.timeout_ms,
            )
            if args.dry_run:
                emit(parse_plan)
                return 0
            if not args.confirm:
                raise SafetyError("parse uploads a local file and requires --confirm (or pass --dry-run to preview)")
        elif args.command == "agent":
            agent_schema = _parse_inline_schema(args.schema)
            agent_plan = FirecrawlClient.agent_preview(
                args.prompt,
                urls=split_csv(args.urls),
                model=args.model,
                max_credits=args.max_credits,
                schema=agent_schema,
                schema_file=args.schema_file,
                strict_constrain_to_urls=args.strict_urls,
            )
            if args.dry_run:
                emit(agent_plan)
                return 0
            if not args.confirm:
                raise SafetyError("agent runs autonomous multi-page extraction and requires --confirm (or --dry-run)")
        elif args.command == "agent-status":
            if args.cancel:
                if args.dry_run:
                    from .client import JOB_ID_PATTERN
                    jid = args.job_id.strip()
                    if not JOB_ID_PATTERN.fullmatch(jid):
                        raise SafetyError("agent job id format is invalid")
                    emit({
                        "operation": "agent-cancel",
                        "dry_run": True,
                        "requires_confirm": True,
                        "method": "DELETE",
                        "path": f"/v2/agent/{jid}",
                        "job_id": jid,
                        "estimated_credits": 0,
                    })
                    return 0
                if not args.confirm:
                    raise SafetyError("cancelling an agent job requires --confirm (or pass --dry-run to preview)")
            elif args.dry_run:
                from .client import JOB_ID_PATTERN
                jid = args.job_id.strip()
                if not JOB_ID_PATTERN.fullmatch(jid):
                    raise SafetyError("agent job id format is invalid")
                emit({
                    "operation": "agent-status",
                    "dry_run": True,
                    "requires_confirm": False,
                    "method": "GET",
                    "path": f"/v2/agent/{jid}",
                    "job_id": jid,
                    "estimated_credits": 0,
                })
                return 0
        elif args.command == "interact":
            interact_plan = FirecrawlClient.interact_preview(
                args.scrape_id,
                prompt=args.prompt,
                code=args.code,
                language=args.language,
                timeout=args.timeout,
                stop=args.stop,
            )
            if args.dry_run:
                emit(interact_plan)
                return 0
            if not args.confirm:
                raise SafetyError("interact operates a live cloud browser session and requires --confirm (or --dry-run)")
        elif args.command == "monitor":
            mon_kwargs = _monitor_kwargs(args)
            mon_plan = FirecrawlClient.monitor_preview(args.monitor_action, **mon_kwargs)
            if args.dry_run:
                emit(mon_plan)
                return 0
            if mon_plan["requires_confirm"] and not args.confirm:
                raise SafetyError(
                    f"monitor {mon_plan['action']} is mutating/recurring and requires --confirm (or --dry-run)"
                )
        elif args.command == "search-feedback":
            sf_plan = FirecrawlClient.search_feedback_preview(
                args.search_id,
                rating=args.rating,
                valuable_sources=_parse_valuable_sources(args.valuable_sources),
                missing_content=_parse_missing_content(args.missing_content),
                query_suggestions=args.query_suggestions,
            )
            if args.dry_run:
                emit(sf_plan)
                return 0

        serp_provenance = None
        serp_envelope = None
        if args.command == "scrape-serp" or getattr(args, "serp_envelope", None):
            from .serp_guard import guard_serp, load_serp_envelope, serp_targets

            serp_envelope = load_serp_envelope(args.envelope if args.command == "scrape-serp" else args.serp_envelope)
            serp_provenance = guard_serp(serp_envelope, allow_suspect=getattr(args, "allow_suspect_serp", False))
            for warning in serp_provenance["warnings"]:
                print("lfc WARNING: " + warning, file=sys.stderr)
        if args.command == "scrape-serp":
            split = serp_targets(serp_envelope, limit=args.limit)
            serp_direct, serp_wrapped = split["urls"], split["needs_resolve"]
            if not serp_direct and not serp_wrapped:
                raise SafetyError("SERP envelope contains no organic URLs to scrape")
            if serp_wrapped and not args.resolve_goto:
                print(f"lfc WARNING: {len(serp_wrapped)} of {len(serp_direct) + len(serp_wrapped)} organic results are "
                      "google.com/goto-wrapped and will NOT be scraped; rerun with --resolve-goto or use "
                      "'lfc resolve <target> --path-hint ... --scrape' (listed under needs_resolve).", file=sys.stderr)
                if not serp_direct:
                    raise SafetyError("All organic results are google.com/goto-wrapped; rerun scrape-serp with "
                                      "--resolve-goto (map/search credits per result) or use lfc resolve per item")
            planned = len(serp_direct) + (len(serp_wrapped) if args.resolve_goto else 0)
            if not args.confirm:
                raise SafetyError(f"scrape-serp scrapes {planned} pages and requires --confirm")

        if getattr(args, "receipt", False) and getattr(args, "no_save", False):
            raise SafetyError("--receipt requires saving; cannot combine --no-save")
        capture_failed = False
        def emit_result(payload):
            nonlocal capture_failed
            if serp_provenance is not None and isinstance(payload, dict):
                payload = {**payload, "serp_provenance": serp_provenance}
            if getattr(args, "no_save", False):
                emit(payload)
                return
            from .capture import archive_response
            request = {k: v for k, v in vars(args).items() if k not in {"command", "no_save", "confirm", "receipt", "workspace", "allow_suspect_serp"}}
            try:
                capture = archive_response(args.command, payload, request=request, workspace=getattr(args,"workspace",None))
                emit({"_capture":capture,"response_omitted":True} if getattr(args,"receipt",False) else {**payload, "_capture": capture})
            except OSError as exc:
                capture_failed = True
                emit({"success": False, "error": "Response received but local capture failed", "capture_error": str(exc), "requestCompleted": True, "response": payload})

        client = FirecrawlClient(consumer="lfc")
        if args.command == "credits":
            emit(client.credit_usage())
        elif args.command == "scrape":
            emit_result(
                client.scrape(
                    args.url,
                    formats=split_csv(args.formats),
                    only_main_content=not args.full_page,
                    max_age_ms=args.max_age_ms,
                    country=args.country,
                )
            )
        elif args.command == "scrape-serp":
            pages = []
            unresolved_goto = []
            if args.resolve_goto:
                for wrapped in serp_wrapped:
                    if not wrapped.get("target"):
                        unresolved_goto.append({**wrapped, "error": "no breadcrumb host, domain, or "
                                                "allowlisted website_name to resolve"})
                        continue
                    try:
                        resolved = client.resolve_url(
                            wrapped["target"], path_hint=wrapped.get("path_hint"), title=wrapped.get("title"),
                            scrape=True, formats=split_csv(args.formats), country=args.country,
                            require_candidate=True,
                        )
                        pages.append({"rank": wrapped.get("rank"), "url": resolved.get("resolved_url"),
                                      "goto_resolved": True, "resolution": {k: resolved.get(k) for k in
                                      ("resolution_method", "base_url", "path_hint")},
                                      "resolution_basis": wrapped.get("resolution_basis"),
                                      "response": resolved.get("scraped") or resolved})
                    except (ApiError, SafetyError) as exc:
                        unresolved_goto.append({**wrapped, "error": str(exc)})
            else:
                unresolved_goto = list(serp_wrapped)
            for target in serp_direct:
                try:
                    pages.append({"url": target, "response": client.scrape(
                        target,
                        formats=split_csv(args.formats),
                        only_main_content=not args.full_page,
                        max_age_ms=args.max_age_ms,
                        country=args.country,
                    )})
                except (ApiError, SafetyError) as exc:
                    pages.append({"url": target, "error": str(exc)})
            emit_result({"success": any("response" in page for page in pages), "pages": pages,
                         "needs_resolve": unresolved_goto})
        elif args.command == "map":
            emit_result(
                client.map_site(
                    args.url,
                    limit=args.limit,
                    search=args.search,
                    sitemap=args.sitemap,
                    include_subdomains=args.include_subdomains,
                )
            )
        elif args.command == "search":
            emit_result(
                client.search(
                    args.query,
                    limit=args.limit,
                    country=args.country,
                    location=args.location,
                    scrape_results=args.scrape_results,
                )
            )
        elif args.command == "resolve":
            emit_result(
                client.resolve_url(
                    args.target,
                    path_hint=args.path_hint,
                    title=args.title,
                    keyword=args.keyword,
                    limit=args.limit,
                    scrape=args.scrape,
                    formats=split_csv(args.formats),
                    country=args.country,
                )
            )
        elif args.command == "crawl":
            kwargs = {
                "limit": args.limit,
                "max_depth": args.max_depth,
                "include_paths": split_csv(args.include_paths),
                "exclude_paths": split_csv(args.exclude_paths),
            }
            emit_result(client.crawl(args.url, confirm=args.confirm, **kwargs))
        elif args.command == "crawl-status":
            emit_result(client.crawl_status(args.job_id))
        elif args.command == "developer":
            emit_result(
                client.developer_search(
                    args.query,
                    limit=args.limit,
                    scrape=args.scrape,
                    formats=split_csv(args.formats),
                    country=args.country,
                    confirm=args.confirm,
                    dry_run=args.dry_run,
                )
            )
        elif args.command == "research":
            emit_result(
                client.research_search(
                    args.query,
                    limit=args.limit,
                    scrape=args.scrape,
                    formats=split_csv(args.formats),
                    country=args.country,
                    mode=args.mode,
                    authors=split_csv(args.authors),
                    categories=split_csv(args.categories),
                    date_from=args.date_from,
                    date_to=args.date_to,
                    paper_id=args.paper_id,
                    seed_ids=split_csv(args.seed_ids),
                    intent=args.intent,
                    relation_mode=args.relation_mode,
                    question=args.question,
                    rerank=args.rerank,
                    confirm=args.confirm,
                    dry_run=args.dry_run,
                )
            )
        elif args.command == "parse":
            emit_result(
                client.parse_file(
                    args.file,
                    formats=split_csv(args.formats),
                    only_main_content=not args.full_page,
                    query=args.query,
                    include_tags=split_csv(args.include_tags),
                    exclude_tags=split_csv(args.exclude_tags),
                    timeout_ms=args.timeout_ms,
                    confirm=args.confirm,
                    dry_run=args.dry_run,
                )
            )
        elif args.command == "agent":
            emit_result(
                client.agent_start(
                    args.prompt,
                    urls=split_csv(args.urls),
                    model=args.model,
                    max_credits=args.max_credits,
                    schema=_parse_inline_schema(args.schema),
                    schema_file=args.schema_file,
                    strict_constrain_to_urls=args.strict_urls,
                    confirm=args.confirm,
                    dry_run=args.dry_run,
                )
            )
        elif args.command == "agent-status":
            if args.cancel:
                emit_result(client.agent_cancel(args.job_id, confirm=args.confirm, dry_run=args.dry_run))
            else:
                emit_result(client.agent_status(args.job_id))
        elif args.command == "interact":
            emit_result(
                client.interact(
                    args.scrape_id,
                    prompt=args.prompt,
                    code=args.code,
                    language=args.language,
                    timeout=args.timeout,
                    stop=args.stop,
                    confirm=args.confirm,
                    dry_run=args.dry_run,
                )
            )
        elif args.command == "monitor":
            emit_result(
                client.monitor(
                    args.monitor_action,
                    confirm=args.confirm,
                    dry_run=args.dry_run,
                    **_monitor_kwargs(args),
                )
            )
        elif args.command == "search-feedback":
            emit_result(
                client.search_feedback(
                    args.search_id,
                    rating=args.rating,
                    valuable_sources=_parse_valuable_sources(args.valuable_sources),
                    missing_content=_parse_missing_content(args.missing_content),
                    query_suggestions=args.query_suggestions,
                    dry_run=args.dry_run,
                )
            )
        else:
            raise SafetyError(f"unknown command {args.command}")
        return 2 if capture_failed else 0
    except ApiError as exc:
        failure = {"success":False,"error":str(exc),"requestMayHaveCompleted":exc.request_may_have_completed,"response":exc.response}
        if exc.response is not None and args.command in {
            "scrape", "scrape-serp", "map", "search", "resolve", "crawl", "crawl-status",
            "developer", "research", "parse", "agent", "agent-status", "interact", "monitor", "search-feedback",
        }:
            emit_result(failure)
        else: emit(failure)
        return 2
    except (CredentialError, SafetyError) as exc:
        failure = {"success": False, "error": str(exc), "command": args.command}
        verdict = getattr(exc, "verdict", None)
        if isinstance(verdict, dict):
            failure["serp_provenance"] = verdict
        emit(failure)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
