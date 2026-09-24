"""Legends Packet compatibility surface.

Packet can import this module and use the same credential, safety, and usage
ledger contract as every other house consumer.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .client import FirecrawlClient


def scrape_page(
    url: str,
    *,
    client: FirecrawlClient | None = None,
    max_age_ms: int = 86_400_000,
) -> dict[str, Any]:
    runtime = client or FirecrawlClient(consumer="legends-packet")
    return runtime.scrape(url, formats=["markdown", "links"], max_age_ms=max_age_ms)


def discover_site_pages(
    url: str,
    *,
    client: FirecrawlClient | None = None,
    limit: int = 100,
    search: str | None = None,
) -> dict[str, Any]:
    runtime = client or FirecrawlClient(consumer="legends-packet")
    return runtime.map_site(url, limit=limit, search=search)


def write_text_evidence(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
