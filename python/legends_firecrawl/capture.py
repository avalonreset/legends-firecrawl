"""Preserve complete provider JSON before agent interpretation."""
from __future__ import annotations
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

def archive_response(operation: str, response: dict, *, root: Path | None = None, request: dict | None = None, workspace: str | None = None) -> dict:
    base = Path(root or os.environ.get('LEGENDS_FIRECRAWL_CAPTURE_ROOT') or Path.home() / '.legends-firecrawl' / 'research').expanduser().resolve()
    stamp = datetime.now(timezone.utc).isoformat()
    slug = ''.join(c if c.isalnum() or c == '-' else '-' for c in operation)
    name = stamp.replace(':', '-').replace('.', '-') + '_' + str(uuid4()) + '_' + slug
    raw_dir = base / 'var/captures/firecrawl'
    card_dir = base / 'vault/captures/firecrawl'
    raw_dir.mkdir(parents=True, exist_ok=True)
    card_dir.mkdir(parents=True, exist_ok=True)
    raw = raw_dir / (name + '.raw.json')
    card = card_dir / (name + '.md')
    payload = {'metadata': {'timestamp': stamp, 'provider': 'firecrawl', 'capability': operation, 'source': 'official-firecrawl-api', 'request': request or {}, 'workspace': workspace or os.environ.get('LEGENDS_WORKSPACE_ID')}, 'response': response}
    data = json.dumps(payload, ensure_ascii=False, indent=2).encode('utf-8')
    with raw.open('xb') as stream:
        stream.write(data)
    digest = hashlib.sha256(data).hexdigest()
    with card.open('x', encoding='utf-8') as stream:
        stream.write(f'# Firecrawl capture: {operation}\n\nObserved: {stamp}\n\nSource: official Firecrawl API. This is a captured response, not an analysis.\n\n[Complete JSON]({Path(os.path.relpath(raw, card.parent)).as_posix()})\n\nSHA-256: `{digest}`\n\nAll returned fields are preserved. Pagination may require additional requests; this file is one response.\n')
    sidecar = raw.with_suffix('.manifest.json')
    sidecar.write_text(json.dumps({'timestamp': stamp, 'provider':'firecrawl', 'capability':operation, 'workspace':workspace or os.environ.get('LEGENDS_WORKSPACE_ID'), 'rawFileName':raw.name, 'sha256':digest, 'bytes':len(data)}, indent=2), encoding='utf-8')
    return {'rawFilePath': str(raw), 'cardFilePath': str(card), 'sha256': digest, 'bytes': len(data)}
