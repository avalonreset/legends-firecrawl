"""House command-line surface for Legends Firecrawl."""

from __future__ import annotations

import argparse
import json
import os
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
    credential_status,
    estimate,
    load_routes,
    usage_summary,
)


KIT_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_VENDOR_CLI = "1.23.3"


def emit(payload: Any) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def _vendor_cli_version() -> tuple[str | None, str | None]:
    executable = shutil.which("firecrawl")
    if not executable:
        return None, None
    completed = subprocess.run(
        [executable, "--version"],
        text=True,
        capture_output=True,
        check=False,
        timeout=20,
    )
    version = completed.stdout.strip() if completed.returncode == 0 else None
    return executable, version


def doctor(*, offline: bool = False) -> tuple[dict[str, Any], int]:
    executable, vendor_version = _vendor_cli_version()
    auth = credential_status()
    checks = [
        {"name": "kit-root", "status": "pass" if (KIT_ROOT / "LEGENDS.md").is_file() else "fail", "detail": str(KIT_ROOT)},
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
                "Set FIRECRAWL_API_KEY with bin/setup-auth.ps1 if auth failed.",
                "Re-run doctor. Do not install or fall back to Firecrawl MCP.",
            ]
        ),
    }
    return result, 0 if result["ready"] else 1


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lfc", description="Legends Firecrawl house spine")
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

    scrape = sub.add_parser("scrape")
    scrape.add_argument("url")
    scrape.add_argument("--formats", default="markdown")
    scrape.add_argument("--max-age-ms", type=int, default=86_400_000)
    scrape.add_argument("--country", default="US")
    scrape.add_argument("--full-page", action="store_true", help="include navigation and footer content")

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

    vendor = sub.add_parser("vendor")
    vendor.add_argument("args", nargs=argparse.REMAINDER)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
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
            executable, _ = _vendor_cli_version()
            if not executable:
                raise SafetyError("official firecrawl CLI is missing; install firecrawl-cli@1.23.3 via npm")
            if any(value in {"init", "setup", "launch", "launcher"} for value in args.args):
                raise SafetyError("vendor integration installers are blocked; use the house setup scripts")
            return subprocess.call([executable, *args.args])

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

        client = FirecrawlClient(consumer="lfc")
        if args.command == "credits":
            emit(client.credit_usage())
        elif args.command == "scrape":
            emit(
                client.scrape(
                    args.url,
                    formats=split_csv(args.formats),
                    only_main_content=not args.full_page,
                    max_age_ms=args.max_age_ms,
                    country=args.country,
                )
            )
        elif args.command == "map":
            emit(
                client.map_site(
                    args.url,
                    limit=args.limit,
                    search=args.search,
                    sitemap=args.sitemap,
                    include_subdomains=args.include_subdomains,
                )
            )
        elif args.command == "search":
            emit(
                client.search(
                    args.query,
                    limit=args.limit,
                    country=args.country,
                    location=args.location,
                    scrape_results=args.scrape_results,
                )
            )
        elif args.command == "crawl":
            kwargs = {
                "limit": args.limit,
                "max_depth": args.max_depth,
                "include_paths": split_csv(args.include_paths),
                "exclude_paths": split_csv(args.exclude_paths),
            }
            emit(client.crawl(args.url, confirm=args.confirm, **kwargs))
        elif args.command == "crawl-status":
            emit(client.crawl_status(args.job_id))
        else:
            raise SafetyError(f"unknown command {args.command}")
        return 0
    except (CredentialError, ApiError, SafetyError) as exc:
        emit({"success": False, "error": str(exc), "command": args.command})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

