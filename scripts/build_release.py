#!/usr/bin/env python3
"""Build a deterministic, allowlisted Legends Firecrawl archive."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release"
ALLOW_FILES = {
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "CLAUDE.md",
    "GEMINI.md",
    "LEGENDS.md",
    "LICENSE",
    "NEXT.md",
    "README.md",
    "VERSION",
    "pyproject.toml",
}
ALLOW_DIRS = {"alexandria-src", "bin", "data", "docs", "evals", "python", "scripts", "skills", "tests", "vault"}


def included_files() -> list[Path]:
    files = [ROOT / name for name in sorted(ALLOW_FILES)]
    for directory in sorted(ALLOW_DIRS):
        files.extend(path for path in sorted((ROOT / directory).rglob("*")) if path.is_file() and "__pycache__" not in path.parts)
    return files


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    RELEASE.mkdir(parents=True, exist_ok=True)
    artifact = RELEASE / f"legends-firecrawl-{version}.zip"
    with zipfile.ZipFile(artifact, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in included_files():
            relative = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(f"legends-firecrawl/{relative}", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    receipt = {
        "schema": "legends-firecrawl-package/v1",
        "version": version,
        "artifact": str(artifact),
        "sha256": sha256(artifact),
        "file_count": len(included_files()),
        "allowlisted": True,
    }
    (RELEASE / "package-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

