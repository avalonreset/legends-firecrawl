"""Verify an installed wheel in isolation, offline and without user credentials."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile
import venv

SMOKE = r'''
import json,tempfile
from pathlib import Path
from legends_firecrawl import cli,client,evidence
assert 'site-packages' in str(Path(cli.__file__))
layout=cli._runtime_layout_check()
assert layout['status']=='pass' and layout['detail']['layout']=='installed_python'
assert layout['detail']['recipes']=='not_bundled_in_wheel'
assert client._kit_root() is None
assert client.ledger_path().is_relative_to(Path.home()) or 'LEGENDS_SMOKE' in str(client.ledger_path())
cli._vendor_cli_version=lambda: ('firecrawl',cli.EXPECTED_VENDOR_CLI)
cli.credential_status=lambda: {'present':True}
assert cli.doctor(offline=True)[1]==0
cli.credential_status=lambda: {'present':False}
assert cli.doctor(offline=True)[1]==1
with tempfile.TemporaryDirectory() as directory:
    root=Path(directory).resolve()
    package=evidence.export_bytes(json.dumps({'success':True,'data':[1]}).encode(),root,workspace='wheel',endpoint='scrape',request={'url':'https://example.com'},observed_at='2026-10-01T12:00:00Z')
    assert evidence.verify(package)['response_integrity']=='verified'
    assert evidence.inventory(root)['total']==1
print(json.dumps({'status':'pass','layout':layout,'provider_calls':0}))
'''
def main():
    parser=argparse.ArgumentParser();parser.add_argument('wheel_directory');args=parser.parse_args()
    wheels=list(Path(args.wheel_directory).glob('legends_firecrawl-*.whl'))
    if len(wheels)!=1:raise SystemExit('Expected exactly one wheel')
    with tempfile.TemporaryDirectory(prefix='legends-wheel-') as directory:
        root=Path(directory).resolve();environment=root/'venv';venv.EnvBuilder(with_pip=True).create(environment)
        executable=environment/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
        env=os.environ.copy()
        for key in ('PYTHONPATH','FIRECRAWL_API_KEY','LEGENDS_FIRECRAWL_HOME','LEGENDS_FIRECRAWL_LEDGER'):env.pop(key,None)
        env['FIRECRAWL_DISABLE_USER_ENV']='1';env['LOCALAPPDATA']=str(root/'LEGENDS_SMOKE')
        subprocess.run([str(executable),'-m','pip','install','--no-index','--no-deps',str(wheels[0].resolve())],check=True,env=env)
        subprocess.run([str(executable),'-I','-c',SMOKE],check=True,env=env,cwd=root)
if __name__=='__main__':main()
