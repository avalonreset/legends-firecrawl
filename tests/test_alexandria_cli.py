"""Offline regressions for released Alexandria operator workflows."""
from __future__ import annotations
import json
import os
from pathlib import Path
import shutil
import subprocess
import pytest
ROOT = Path(__file__).resolve().parents[1]

def invoke(*args: str, root: Path = ROOT):
    env = os.environ.copy()
    env.pop('FIRECRAWL_API_KEY', None)
    env['FIRECRAWL_DISABLE_USER_ENV'] = '1'
    return subprocess.run(['node', str(root/'alexandria-src'/'cli.js'), *args], cwd=root, env=env, capture_output=True, text=True, timeout=15)

@pytest.mark.skipif(os.name != 'nt', reason='Windows PowerShell wrapper regression')
@pytest.mark.parametrize('command', ['audit','captures','help'])
def test_single_word_alexandria_command_through_powershell(command):
    shell = shutil.which('pwsh') or shutil.which('powershell')
    if not shell: pytest.skip('PowerShell unavailable')
    env = os.environ.copy()
    env['FIRECRAWL_DISABLE_USER_ENV'] = '1'
    env.pop('FIRECRAWL_API_KEY',None)
    r = subprocess.run([shell,'-NoProfile','-File',str(ROOT/'bin'/'lfc.ps1'),'alexandria',command],cwd=ROOT,env=env,capture_output=True,text=True,timeout=20)
    assert r.returncode == 0, r.stderr
    assert 'Unknown command' not in r.stderr
    if command == 'audit': assert json.loads(r.stdout)['catalogCapabilities'] == 797

def test_search_is_compact_and_keeps_usable_capability():
    r=invoke('search','treasury')
    assert r.returncode == 0, r.stderr
    assert len(r.stdout.encode()) < 15000
    providers=json.loads(r.stdout)
    treasury=next(p for p in providers if p['id']=='treasury-fiscal-data')
    tools={t['capability']:t for t in treasury['tools']}
    assert 'debt/to-the-penny' in tools
    assert tools['debt/to-the-penny']['listedCredits'] == 1
    assert tools['debt/to-the-penny']['route'] == 'paid_preview'

def test_full_inspect_explicitly_restores_input_contracts():
    brief=invoke('inspect','treasury-fiscal-data')
    full=invoke('inspect','treasury-fiscal-data','--full')
    assert brief.returncode == full.returncode == 0
    short=json.loads(brief.stdout)[0]
    detail=json.loads(full.stdout)[0]
    assert all('options' not in t for t in short['tools'])
    assert any(t.get('options') for t in detail['tools'])
    assert len(brief.stdout) < len(full.stdout)

def test_capture_inventory_returns_readable_paths_and_unknown_cost(tmp_path):
    # Minimal isolated tree prevents fixture captures from polluting user data.
    for rel in ['alexandria-src/cli.js','alexandria-src/router.js','data/alexandria_catalog.json']:
        destination=tmp_path/rel
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/rel,destination)
    directory=tmp_path/'var'/'captures'/'treasury-fiscal-data'
    directory.mkdir(parents=True)
    raw=directory/'sample.raw.json'
    raw.write_text(json.dumps({'metadata':{'provider':'treasury-fiscal-data','capability':'debt/to-the-penny','source':'firecrawl-alexandria-gateway','creditsBurned':None},'response':{'status':'ok','creditsUsed':None},'data':{'data':[{'amount':'12'}]}}))
    r=invoke('captures',root=tmp_path)
    assert r.returncode == 0, r.stderr
    result=json.loads(r.stdout)
    assert result['errors'] == []
    item=result['captures'][0]
    assert item['capability'] == 'debt/to-the-penny'
    assert item['creditsUsed'] is None
    assert Path(item['rawFilePath']).resolve() == raw.resolve()
    assert json.loads(Path(item['rawFilePath']).read_text())['data']['data'][0]['amount']=='12'
