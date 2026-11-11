"""Static public-release and EDR gate for legends-firecrawl."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\ufffd]")
FORBIDDEN_EXTENSIONS = {".pem", ".key", ".p12", ".pfx", ".ps1", ".bat", ".cmd", ".vbs", ".ahk", ".exe", ".dll", ".pyc"}

REQUIRED_FILES = [
    ".legends-module",
    ".legends-router-pin",
    "AGENTS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "MANIFEST.in",
    "README.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    "VERSION",
    "assets/banner.png",
    "assets/banner.webp",
    "assets/manifest.json",
    "assets/preview.png",
    "assets/social-preview.png",
    "docs/AGENT-RECIPE.md",
    "pyproject.toml",
    "python/legends_firecrawl/__init__.py",
    "python/legends_firecrawl/__main__.py",
    "python/legends_firecrawl/cli.py",
    "skills/cto-legends/SKILL.md",
]

FORBIDDEN_PATHS = [
    "CLAUDE.md",
    "GEMINI.md",
    "CODEX.md",
    "GROK.md",
    "SKILL.md",
    "github/SKILL.md",
    "gemini-extension.json",
    "skill-package.json",
    ".claude-plugin",
    "install.ps1",
    "install.sh",
    "install-codex.ps1",
    "install-codex.sh",
    "bin/setup-multi-agent.ps1",
    "bin/setup-multi-agent.sh",
    "bin/setup-multi-agent",
    "bin/install-spine.ps1",
    "bin/install-spine.sh",
    "bin/lfc.ps1",
    "bin/lfc.cmd",
    "bin/lax.ps1",
    "bin/lax.cmd",
    "bin/doctor.ps1",
    "bin/canary.ps1",
    "bin/setup-auth.ps1",
]

FORBIDDEN_CODE_PATTERNS = [
    r"CREATE_NO_WINDOW",
    r"0x08000000",
    r"-WindowStyle\s+Hidden",
    r"-ExecutionPolicy\s+Bypass",
    r"ctypes\.windll",
    r"CryptUnprotectData",
    r"GetAsyncKeyState",
    r"SetWindowsHookEx",
    r"IndexedDB",
    r"LevelDB",
    r"Login Data",
    r"(?i)\.tail[a-z0-9]+\.ts\.net",
    r"(?i)nsec1[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{30,}",
    r"(?i)sk_live_[a-z0-9]{12,}",
    r"(?i)rk_live_[a-z0-9]{12,}",
    r"(?i)whsec_[a-z0-9]{12,}",
    r"gh[pousr]_[A-Za-z0-9]{20,}",
    r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
]

HOUSE_PATH_PATTERNS = [
    r"C:\\" + r"Users\\",
    r"(?<![:\w])/home/[a-z0-9_-]+/",
    r"E:\\" + r"empire",
    r"E:\\" + r"legends-firecrawl",
    r"E:\\" + r"ai-marketing-hub",
    r"rc" + r"col",
    r"glit" + r"chyglitch",
    r"omni" + r"gent",
]


def tracked_files() -> list[Path]:
    out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    return [ROOT / line.strip() for line in out.splitlines() if line.strip()]


def check_release() -> list[str]:
    issues: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            issues.append(f"Missing required file: {rel}")

    for rel in FORBIDDEN_PATHS:
        if (ROOT / rel).exists():
            issues.append(f"Forbidden path exists: {rel}")

    mod_file = ROOT / ".legends-module"
    if mod_file.is_file() and mod_file.read_text(encoding="utf-8").strip() != "legends-firecrawl":
        issues.append(".legends-module must equal 'legends-firecrawl'")

    pin_file = ROOT / ".legends-router-pin"
    if pin_file.is_file():
        pin = pin_file.read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"[0-9a-f]{40}", pin):
            issues.append(".legends-router-pin must be a 40-char lowercase hex SHA")

    ver_file = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    init_text = (ROOT / "python" / "legends_firecrawl" / "__init__.py").read_text(encoding="utf-8")
    m_init = re.search(r'^__version__\s*=\s*"([^"]+)"', init_text, re.M)
    init_ver = m_init.group(1) if m_init else None
    routes = json.loads((ROOT / "python" / "legends_firecrawl" / "routes.json").read_text(encoding="utf-8"))
    routes_ver = routes.get("version")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    m_chg = re.search(r"^#{1,3}\s+\[?v?(\d+\.\d+\.\d+)\]?", changelog, re.M)
    chg_ver = m_chg.group(1) if m_chg else None
    if not ver_file or len({ver_file, init_ver, routes_ver, chg_ver}) != 1:
        issues.append(f"Version mismatch: VERSION={ver_file}, __init__={init_ver}, routes={routes_ver}, CHANGELOG={chg_ver}")

    skill_files = [p.relative_to(ROOT).as_posix() for p in tracked_files() if p.name == "SKILL.md"]
    if skill_files != ["skills/cto-legends/SKILL.md"]:
        issues.append(f"Expected only skills/cto-legends/SKILL.md, found: {skill_files}")

    manifest_path = ROOT / "assets" / "manifest.json"
    if manifest_path.is_file():
        try:
            manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
            entries = (
                manifest_data["files"]
                if isinstance(manifest_data.get("files"), list)
                else [
                    {"name": k, **v}
                    for k, v in manifest_data.items()
                    if isinstance(v, dict) and "sha256" in v
                ]
            )
            for entry in entries:
                asset_path = ROOT / "assets" / entry["name"]
                if not asset_path.is_file():
                    issues.append(f"Manifest asset missing: {entry['name']}")
                    continue
                raw_asset = asset_path.read_bytes()
                if len(raw_asset) != entry.get("bytes"):
                    issues.append(f"Manifest byte mismatch for {entry['name']}")
                if hashlib.sha256(raw_asset).hexdigest() != entry.get("sha256"):
                    issues.append(f"Manifest sha256 mismatch for {entry['name']}")
        except Exception as exc:
            issues.append(f"Invalid assets/manifest.json: {exc}")

    for js_name in ("cli.js", "router.js", "encapsulation.js"):
        src_js = ROOT / "alexandria-src" / js_name
        pkg_js = ROOT / "python" / "legends_firecrawl" / "alexandria-src" / js_name
        if not pkg_js.is_file() or src_js.read_bytes() != pkg_js.read_bytes():
            issues.append(f"Package data drift: python/legends_firecrawl/alexandria-src/{js_name}")
    src_cat = ROOT / "data" / "alexandria_catalog.json"
    pkg_cat = ROOT / "python" / "legends_firecrawl" / "data" / "alexandria_catalog.json"
    if not pkg_cat.is_file() or src_cat.read_bytes() != pkg_cat.read_bytes():
        issues.append("Package data drift: python/legends_firecrawl/data/alexandria_catalog.json")

    for p in tracked_files():
        rel = p.relative_to(ROOT).as_posix()
        if rel == "scripts/check_release.py":
            continue
        suffix = p.suffix.lower()
        if suffix in FORBIDDEN_EXTENSIONS:
            issues.append(f"Forbidden file extension tracked: {rel}")
            continue
        if suffix in (".png", ".webp"):
            raw = p.read_bytes()
            for chunk in (b"tEXt", b"iTXt", b"zTXt", b"eXIf", b"EXIF", b"XMP "):
                if chunk in raw:
                    issues.append(f"Image metadata chunk {chunk!r} found in {rel}")
        if suffix in (".py", ".md", ".toml", ".yml", ".yaml", ".json", ".ps1", ".sh", ".cmd", ".bat", ".js", ".mjs", ".cff", ".in", ".txt"):
            text = p.read_text(encoding="utf-8", errors="replace")
            if CONTROL_CHAR_RE.search(text):
                issues.append(f"Control character or U+FFFD replacement character in {rel}")
            for pat in FORBIDDEN_CODE_PATTERNS:
                if re.search(pat, text, re.IGNORECASE):
                    issues.append(f"Forbidden pattern '{pat}' in {rel}")
            for pat in HOUSE_PATH_PATTERNS:
                if re.search(pat, text, re.IGNORECASE):
                    issues.append(f"House/private pattern '{pat}' in {rel}")
            if suffix == ".md" and rel != "skills/cto-legends/SKILL.md":
                if "\u2014" in text or "\u2013" in text:
                    issues.append(f"Typography dash (em/en dash) found in {rel}")
                for target_link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                    if target_link.startswith(("https://", "http://", "mailto:", "#")):
                        continue
                    cleaned = unquote(target_link.split("#", 1)[0].split("?", 1)[0]).strip()
                    if not cleaned:
                        continue
                    resolved = (p.parent / cleaned).resolve()
                    if not resolved.is_relative_to(ROOT.resolve()) or not resolved.exists():
                        issues.append(f"Broken or external local link in {rel}: {target_link}")

    return issues


def main() -> int:
    issues = check_release()
    if issues:
        for issue in issues:
            print(f"FAIL: {issue}")
        return 1
    print("Release checks: PASS (0 issues)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
