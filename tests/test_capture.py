"""Offline independent checks of full response archival and billing-safe failures."""
from __future__ import annotations
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import pytest
from legends_firecrawl.capture import archive_response
from legends_firecrawl import cli

@pytest.fixture
def full_response():
    return {'success':True,'data':{'markdown':'α'*120000,'metadata':{'title':'Complete','nested':[{'unknown':None,'values':[0,False,'x']}]},'links':['https://example.com/x']},'unknown_provider_field':{'keep':'verbatim'}}

def test_complete_nested_payload_archived_without_mutation(tmp_path,full_response):
    original=deepcopy(full_response)
    receipt=archive_response('scrape',full_response,root=tmp_path,request={'url':'https://example.com'})
    raw=Path(receipt['rawFilePath'])
    saved=json.loads(raw.read_text(encoding='utf-8'))
    assert saved['response']==original==full_response
    assert len(saved['response']['data']['markdown'])==120000
    assert receipt['sha256']==hashlib.sha256(raw.read_bytes()).hexdigest()
    assert receipt['bytes']==raw.stat().st_size
    card=Path(receipt['cardFilePath']).read_text(encoding='utf-8')
    assert receipt['sha256'] in card and '../../../var/captures/firecrawl/' in card

def test_archive_uses_shared_env_and_distinct_filenames(tmp_path,monkeypatch,full_response):
    monkeypatch.setenv('LEGENDS_FIRECRAWL_CAPTURE_ROOT',str(tmp_path))
    first=archive_response('scrape',full_response)
    second=archive_response('scrape',full_response)
    assert first['rawFilePath']!=second['rawFilePath']
    assert Path(first['rawFilePath']).is_relative_to(tmp_path)
    assert Path(first['rawFilePath']).exists()

def test_relative_capture_root_is_resolved(tmp_path,monkeypatch,full_response):
    monkeypatch.chdir(tmp_path)
    receipt=archive_response('scrape',full_response,root=Path('relative-archive'))
    assert Path(receipt['rawFilePath']).is_absolute()
    assert Path(receipt['cardFilePath']).exists()

def install_client(monkeypatch,payload):
    calls=[]
    class Client:
        def __init__(self,**kwargs): pass
        def scrape(self,*args,**kwargs):calls.append((args,kwargs));return payload
    monkeypatch.setattr(cli,'FirecrawlClient',Client)
    return calls

def test_cli_stdout_preserves_all_fields_and_saved_original(tmp_path,monkeypatch,capsys,full_response):
    monkeypatch.setenv('LEGENDS_FIRECRAWL_CAPTURE_ROOT',str(tmp_path))
    calls=install_client(monkeypatch,full_response)
    assert cli.main(['scrape','https://example.com'])==0
    stdout=json.loads(capsys.readouterr().out)
    receipt=stdout.pop('_capture')
    assert stdout==full_response
    assert json.loads(Path(receipt['rawFilePath']).read_text(encoding='utf-8'))['response']==full_response
    assert len(calls)==1

def test_no_save_retains_full_stdout_without_file_writes(tmp_path,monkeypatch,capsys,full_response):
    monkeypatch.setenv('LEGENDS_FIRECRAWL_CAPTURE_ROOT',str(tmp_path))
    calls=install_client(monkeypatch,full_response)
    assert cli.main(['scrape','https://example.com','--no-save'])==0
    assert json.loads(capsys.readouterr().out)==full_response
    assert list(tmp_path.iterdir())==[]
    assert len(calls)==1

def test_capture_failure_retains_paid_response_without_retry(tmp_path,monkeypatch,capsys,full_response):
    blocked=tmp_path/'not-a-directory'
    blocked.write_text('keep')
    monkeypatch.setenv('LEGENDS_FIRECRAWL_CAPTURE_ROOT',str(blocked))
    calls=install_client(monkeypatch,full_response)
    assert cli.main(['scrape','https://example.com'])==2
    result=json.loads(capsys.readouterr().out)
    assert result['requestCompleted'] is True
    assert result['response']==full_response
    assert len(calls)==1
    assert blocked.read_text()=='keep'

def test_cli_receipt_preserves_file(tmp_path,monkeypatch,capsys,full_response):
    monkeypatch.setenv('LEGENDS_FIRECRAWL_CAPTURE_ROOT',str(tmp_path))
    calls=install_client(monkeypatch,full_response)
    assert cli.main(['scrape','https://example.com','--receipt','--workspace','client-a'])==0
    result=json.loads(capsys.readouterr().out)
    assert result['response_omitted'] and len(calls)==1
    saved=json.loads(Path(result['_capture']['rawFilePath']).read_text(encoding='utf8'))
    assert saved['response']==full_response and saved['metadata']['workspace']=='client-a'

def test_provider_failure_archived_once(tmp_path,monkeypatch,capsys):
    monkeypatch.setenv('LEGENDS_FIRECRAWL_CAPTURE_ROOT',str(tmp_path))
    calls=[]
    class Client:
        def __init__(self,**kwargs):pass
        def scrape(self,*args,**kwargs):
            calls.append(1)
            raise cli.ApiError('rejected',response={'success':False,'unexpected':{'keep':1}})
    monkeypatch.setattr(cli,'FirecrawlClient',Client)
    assert cli.main(['scrape','https://example.com'])==2
    result=json.loads(capsys.readouterr().out)
    assert len(calls)==1
    saved=json.loads(Path(result['_capture']['rawFilePath']).read_text(encoding='utf8'))
    assert saved['response']['response']=={'success':False,'unexpected':{'keep':1}}
