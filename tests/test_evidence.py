import json
import shutil
from datetime import datetime,timezone,timedelta
from pathlib import Path
import pytest
from legends_firecrawl import evidence as e
STAMP='2026-10-01T12:00:00+00:00'
NOW=datetime.fromisoformat(STAMP)
def bank(tmp_path,payload=None,endpoint='scrape'):
    raw=tmp_path/'input.json';raw.write_text(json.dumps(payload if payload is not None else {'success':True,'data':{'markdown':'hello'}}),encoding='utf8')
    return e.export(raw,tmp_path/'bank',workspace='client-a',endpoint=endpoint,request={'url':'https://example.com'},observed_at=STAMP)
def reuse(package,**kwargs):
    return e.assess_reuse(package,workspace='client-a',endpoint='scrape',request={'url':'https://example.com'},max_age_hours=24,now=NOW,**kwargs)
def test_export_original_bytes_duplicate_move(tmp_path):
    p=bank(tmp_path);assert (p/'response.json').read_bytes()==(tmp_path/'input.json').read_bytes()
    assert bank(tmp_path)==p
    q=tmp_path/'moved';shutil.move(str(p),q)
    assert e.verify(q)['note_integrity']=='verified'
    assert '(response.json)' in (q/'README.md').read_text()
    assert reuse(q)['eligible']
@pytest.mark.parametrize('name',['response.json','README.md','manifest.json'])
def test_tamper(tmp_path,name):
    p=bank(tmp_path);(p/name).write_text('{}')
    with pytest.raises(ValueError):e.verify(p)
def test_incomplete_not_repaired(tmp_path):
    p=bank(tmp_path);(p/'README.md').unlink()
    with pytest.raises(ValueError):bank(tmp_path)
    assert not (p/'README.md').exists()
@pytest.mark.parametrize('payload',[{'success':False},{'status':'queued','data':[1]},{'success':True,'status':'paused','data':[1]},{'success':True,'status':None,'data':[1]},{'status':'empty'},{'success':True,'data':[]},{'success':True,'next':'url','data':[1]},{'status':'ok','data':[1],'response':{'success':False}}])
def test_noncompleted_not_reusable(tmp_path,payload):
    assert not reuse(bank(tmp_path,payload))['eligible']
def test_reuse_exact_scope_staleness(tmp_path):
    p=bank(tmp_path)
    for changes in [{'workspace':'other'},{'endpoint':'map'},{'request':{'url':'x'}},{'now':NOW+timedelta(days=2)},{'now':NOW-timedelta(seconds=1)}]:
        kwargs=dict(workspace='client-a',endpoint='scrape',request={'url':'https://example.com'},max_age_hours=24,now=NOW);kwargs.update(changes)
        assert not e.assess_reuse(p,**kwargs)['eligible']
def test_inventory_never_reads_raw(tmp_path,monkeypatch):
    p=bank(tmp_path);original=Path.read_bytes
    def guarded(path):
        if path.name=='response.json':raise AssertionError('read raw')
        return original(path)
    monkeypatch.setattr(Path,'read_bytes',guarded)
    (p/'response.json').write_text('corrupt')
    result=e.inventory(p.parent)
    assert result['total']==1 and result['items'][0]['response_integrity']=='not_checked'
def test_large_view_explicit_full(tmp_path):
    data={'success':True,'data':{'markdown':'α'*120000,'rows':list(range(100))}}
    p=bank(tmp_path,data)
    assert len(json.dumps(e.view(p,select='data.markdown')))<14000
    assert e.view(p,full=True)['value']==data
    assert e.view(p,select='data.rows',limit=3)['value']['omitted']==97
def test_capture_bridge(tmp_path):
    from legends_firecrawl.capture import archive_response
    receipt=archive_response('scrape',{'success':True,'data':[1]},root=tmp_path,request={'url':'example'})
    p=e.export_capture(receipt['rawFilePath'],tmp_path/'bank',workspace='a')
    assert e.verify(p)['request']=={'url':'example'}
def test_legacy_capture_missing_request_refuses(tmp_path):
    p=tmp_path/'legacy.json';p.write_text(json.dumps({'metadata':{'timestamp':STAMP,'capability':'scrape'},'response':{'success':True}}))
    with pytest.raises(ValueError,match='request'):e.export_capture(p,tmp_path/'bank',workspace='a')
def test_cli_offline(tmp_path,capsys):
    from legends_firecrawl.cli import main
    p=bank(tmp_path)
    assert main(['evidence','verify',str(p)])==0
    assert json.loads(capsys.readouterr().out)['response_integrity']=='verified'

@pytest.mark.parametrize('raw',[b'{"success":true,"data":[1],"data":[2]}',b'{"success":true,"data":{"nested":NaN}}',b'{"success":true,"data":{"nested":1e999}}'])
def test_ambiguous_json_rejected_without_touching_source(tmp_path,raw):
    source=tmp_path/'raw.json';source.write_bytes(raw)
    with pytest.raises(ValueError):e.export(source,tmp_path/'bank',workspace='a',endpoint='scrape',request={'url':'x'},observed_at=STAMP)
    assert source.read_bytes()==raw and not (tmp_path/'bank').exists()

def test_cli_reuse_ineligible_exit_two(tmp_path,capsys):
    p=bank(tmp_path);request=tmp_path/'request.json';request.write_text('{"url":"https://example.com"}')
    assert e.main(['reuse',str(p),'--workspace','wrong','--endpoint','scrape','--request-file',str(request),'--max-age-hours','24'])==2
    assert not json.loads(capsys.readouterr().out)['eligible']
