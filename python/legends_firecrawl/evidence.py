"""Portable offline Firecrawl evidence. Never calls a provider or mutates a vault."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

SCHEMA = 'legends-firecrawl-evidence/v1'
def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
def _decode(raw):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result: raise ValueError('duplicate JSON key: '+key)
            result[key]=value
        return result
    def constant(value): raise ValueError('nonfinite JSON number: '+value)
    def finite(value):
        result=float(value)
        if not math.isfinite(result): raise ValueError('nonfinite JSON number: '+value)
        return result
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=constant,parse_float=finite)
def _hash(value):
    return hashlib.sha256(value).hexdigest()
def _date(value):
    if not isinstance(value,str): raise ValueError('actual observation timestamp required')
    date = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if date.tzinfo is None: raise ValueError('timestamp requires timezone')
    return date
def _safe(path):
    path = Path(path)
    for item in (path, *path.parents):
        if item.is_symlink() or getattr(item, 'is_junction', lambda: False)():
            raise ValueError('linked evidence path refused')
    return path
def _state(data, endpoint):
    if not isinstance(data, dict): return 'unknown'
    status = data.get('status')
    if data.get('success') is False or status in ('error','failed','cancelled'): return 'error'
    if status in ('scraping','pending','queued','processing','in_progress') or endpoint == 'crawl': return 'pending'
    if 'status' in data and status not in ('empty','completed','ok'): return 'unknown'
    if isinstance(data.get('response'),dict) and data['response'].get('success') is False: return 'error'
    if status == 'empty': return 'empty'
    if data.get('next'): return 'partial'
    if status in ('completed','ok') or data.get('success') is True:
        payload = data.get('data', data.get('links'))
        if payload in (None, [], {}): return 'empty'
        return 'completed'
    return 'unknown'
def _note(observed_at):
    return ('# Firecrawl research evidence\n\nUnreviewed source material, not an accepted finding.\n\n'
            f'Observed: {observed_at}\n\n[Complete response](response.json) | [Request and scope](manifest.json)\n\n'
            'One returned response only. Pagination, accuracy and semantic relevance require review.\n'
            'Reported costs are snapshots, not incremental charges. Do not sum repeated task receipts.\n'
            'Keep private client evidence outside module installations and public repositories.\n')
def export(response, destination, *, workspace, endpoint, request, observed_at, producer='legends-firecrawl'):
    """Preserve original file bytes; supplied collection time must be actual, not export time."""
    return export_bytes(Path(response).read_bytes(), destination, workspace=workspace, endpoint=endpoint,
                        request=request, observed_at=observed_at, producer=producer)
def export_bytes(raw, destination, *, workspace, endpoint, request, observed_at, producer='legends-firecrawl'):
    if not isinstance(workspace,str) or not workspace.strip(): raise ValueError('explicit workspace required')
    if not isinstance(endpoint,str) or not endpoint.strip(): raise ValueError('endpoint required')
    if not isinstance(request,dict) or not request: raise ValueError('complete request object required')
    _date(observed_at)
    data = _decode(raw)
    if not isinstance(data,dict): raise ValueError('full response object required')
    note = _note(observed_at).encode('utf-8')
    manifest = dict(schema=SCHEMA, workspace=workspace, endpoint=endpoint, request=request,
                    observed_at=observed_at, producer=producer, provider='firecrawl',
                    response_sha256=_hash(raw), note_sha256=_hash(note), status=_state(data,endpoint),
                    coverage={'scope':'single_response','completeness':'not_asserted'})
    identity = _hash(_json(manifest).encode('utf-8'))
    manifest['evidence_id'] = identity
    if len(_json(manifest).encode('utf-8'))>2_000_000: raise ValueError('manifest exceeds 2 MB inspection limit')
    target = _safe(Path(destination) / identity)
    if target.exists():
        verify(target)
        return target
    target.parent.mkdir(parents=True,exist_ok=True)
    try: target.mkdir()
    except FileExistsError:
        verify(target)
        return target
    # Deliberately exclusive. Interrupted packages stay visible and fail verification.
    for name,content in [('response.json',raw),('README.md',note),('manifest.json',_json(manifest).encode('utf-8'))]:
        with (target/name).open('xb') as stream: stream.write(content)
    return target

def _manifest(package):
    root = _safe(package)
    path = _safe(root/'manifest.json')
    if path.stat().st_size > 2_000_000: raise ValueError('manifest exceeds 2 MB inspection limit')
    manifest = _decode(path.read_text(encoding='utf-8'))
    identity = manifest.get('evidence_id')
    if manifest.get('schema') != SCHEMA or _hash(_json({k:v for k,v in manifest.items() if k!='evidence_id'}).encode('utf-8')) != identity:
        raise ValueError('manifest integrity mismatch')
    for name in ('workspace','endpoint','request','observed_at','response_sha256','note_sha256','status'):
        if name not in manifest: raise ValueError('incomplete manifest')
    _date(manifest['observed_at'])
    return manifest

def verify(package):
    root = _safe(package)
    manifest = _manifest(root)
    for name,key in [('response.json','response_sha256'),('README.md','note_sha256')]:
        file = _safe(root/name)
        if not file.is_file(): raise ValueError('incomplete evidence package')
        digest = hashlib.sha256()
        with file.open('rb') as stream:
            for chunk in iter(lambda:stream.read(1024*1024),b''): digest.update(chunk)
        if digest.hexdigest()!=manifest[key]: raise ValueError(name+' integrity mismatch')
    data = _decode((root/'response.json').read_bytes())
    if _state(data,manifest['endpoint'])!=manifest['status']: raise ValueError('response state mismatch')
    return dict(manifest, response_integrity='verified', note_integrity='verified')

def inventory(bank, *, workspace=None, endpoint=None, query=None, limit=50, offset=0):
    """Read manifests only. Does not certify response or note integrity."""
    if not isinstance(limit,int) or not 1<=limit<=1000 or not isinstance(offset,int) or offset<0: raise ValueError('limit 1..1000 and nonnegative offset required')
    root = _safe(bank)
    entries,errors=[],[]
    if root.exists():
        for child in root.iterdir():
            if not child.is_dir(): continue
            try:
                m=_manifest(child)
                if workspace is not None and workspace!=m['workspace']: continue
                if endpoint is not None and endpoint!=m['endpoint']: continue
                if query and query.casefold() not in _json(m).casefold(): continue
                entries.append({k:m[k] for k in ('evidence_id','workspace','endpoint','observed_at','status') } | {'package':str(child),'response_integrity':'not_checked','note_integrity':'not_checked'})
            except (OSError,ValueError,KeyError,TypeError) as exc: errors.append({'package':str(child),'error':str(exc)})
    entries.sort(key=lambda x:(x['observed_at'],x['evidence_id']),reverse=True)
    return dict(items=entries[offset:offset+limit],total=len(entries),offset=offset,limit=limit,errors=errors[:limit],error_count=len(errors),provider_calls=0)

def assess_reuse(package, *, workspace, endpoint, request, max_age_hours, now=None):
    if not math.isfinite(max_age_hours) or max_age_hours<0: raise ValueError('finite nonnegative freshness limit required')
    m=verify(package)
    current=now or datetime.now(timezone.utc)
    if current.tzinfo is None: raise ValueError('now requires timezone')
    reasons=[key+' differs' for key,value in [('workspace',workspace),('endpoint',endpoint),('request',request)] if m[key]!=value]
    age=(current-_date(m['observed_at'])).total_seconds()/3600
    if age<0 or age>max_age_hours: reasons.append('future or stale observation')
    if m['status']!='completed': reasons.append('response not completed; inspect state separately')
    return dict(eligible=not reasons,reasons=reasons,evidence_id=m['evidence_id'],requires_semantic_review=True,provider_calls=0)

def view(package, *, select=None, limit=20, full=False, max_chars=16000):
    if not isinstance(limit,int) or limit<1 or limit>1000: raise ValueError('limit must be 1..1000')
    if not isinstance(max_chars,int) or max_chars<100 or max_chars>1000000: raise ValueError('max_chars must be 100..1000000')
    m=verify(package)
    value=_decode((Path(package)/'response.json').read_bytes())
    if select:
        for key in select.split('.'):
            try: value=value[int(key)] if isinstance(value,list) else value[key]
            except (KeyError,IndexError,TypeError,ValueError): raise ValueError('selection not found: '+select) from None
    def bounded(obj):
        if isinstance(obj,str): return obj if len(obj)<=2000 else {'preview':obj[:2000],'characters':len(obj),'omitted_characters':len(obj)-2000}
        if isinstance(obj,list): return {'items':[bounded(x) for x in obj[:limit]],'total':len(obj),'omitted':max(0,len(obj)-limit)}
        if isinstance(obj,dict):
            pairs=list(obj.items())
            return {'fields':{k:bounded(v) for k,v in pairs[:limit]},'total_fields':len(pairs),'omitted_fields':max(0,len(pairs)-limit)}
        return obj
    projected=value if full else bounded(value)
    encoded=_json(projected) if not full else ''
    if not full and len(encoded)>max_chars:
        projected={'preview_json_text':encoded[:max_chars],'projected_characters':len(encoded),'omitted_characters':len(encoded)-max_chars,'complete_response':'response.json'}
    return dict(evidence_id=m['evidence_id'],selection=select,full=full,value=projected,provider_calls=0)

def export_capture(capture,destination,*,workspace,request=None,endpoint=None,observed_at=None):
    saved=_decode(Path(capture).read_bytes())
    m=saved.get('metadata',{})
    raw=saved.get('response')
    if not isinstance(raw,dict): raise ValueError('capture has no full response')
    selected_request=request or m.get('request') or raw.get('request')
    if not selected_request: raise ValueError('legacy capture lacks request; supply original request file')
    return export_bytes(_json(raw).encode('utf-8'),destination,workspace=workspace,
        endpoint=endpoint or m.get('capability') or raw.get('capability'), request=selected_request,
        observed_at=observed_at or m.get('timestamp'))

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    for name in ('export','export-capture'):
        p=sub.add_parser(name);p.add_argument('response');p.add_argument('destination');p.add_argument('--workspace',required=True)
        for flag in ('endpoint','request-file','observed-at'): p.add_argument('--'+flag,required=name=='export')
    p=sub.add_parser('verify');p.add_argument('package')
    for name in ('inventory','find'):
        p=sub.add_parser(name);p.add_argument('bank');p.add_argument('--workspace');p.add_argument('--endpoint');p.add_argument('--query');p.add_argument('--limit',type=int,default=50);p.add_argument('--offset',type=int,default=0)
    p=sub.add_parser('view');p.add_argument('package');p.add_argument('--select');p.add_argument('--limit',type=int,default=20);p.add_argument('--full',action='store_true');p.add_argument('--max-chars',type=int,default=16000)
    p=sub.add_parser('reuse');p.add_argument('package');p.add_argument('--workspace',required=True);p.add_argument('--endpoint',required=True);p.add_argument('--request-file',required=True);p.add_argument('--max-age-hours',required=True,type=float)
    args=vars(parser.parse_args(argv));command=args.pop('command')
    try:
        if 'request_file' in args:
            file=args.pop('request_file');args['request']=_decode(Path(file).read_text(encoding='utf-8-sig')) if file else None
        if command.startswith('export'):
            function=export if command=='export' else export_capture
            response=args.pop('response');destination=args.pop('destination')
            result={'package':str(function(response,destination,**args)),'provider_calls':0}
        else:
            function={'verify':verify,'inventory':inventory,'find':inventory,'view':view,'reuse':assess_reuse}[command]
            target=args.pop('bank',None) or args.pop('package',None);result=function(target,**args)
        print(_json(result));return 2 if command=='reuse' and not result['eligible'] else 0
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(_json({'error':str(exc),'provider_calls':0}));return 2
if __name__=='__main__': raise SystemExit(main())
