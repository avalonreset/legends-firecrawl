"""Offline synthetic evidence-bank benchmark. No credentials or provider requests."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import platform
import sys
import time
import tracemalloc
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'python'))
from legends_firecrawl import evidence

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--destination',required=True);parser.add_argument('--records',type=int,default=1000)
    args=parser.parse_args();root=Path(args.destination)
    if root.exists():raise SystemExit('Use a new destination to avoid contaminating measurements')
    root.mkdir(parents=True)
    stamp=datetime.now(timezone.utc).isoformat();bank=root/'bank';measurements={}
    start=time.perf_counter()
    for i in range(args.records):
        evidence.export_bytes(json.dumps({'success':True,'data':{'markdown':'x'*1024,'record':i}}).encode(),bank,workspace='synthetic-client',endpoint='scrape',request={'url':f'https://example.com/{i}'},observed_at=stamp)
    measurements['export_records_seconds']=round(time.perf_counter()-start,3)
    start=time.perf_counter();listing=evidence.inventory(bank,limit=10);measurements['inventory_seconds']=round(time.perf_counter()-start,3)
    start=time.perf_counter();evidence.inventory(bank,query='example.com/999',limit=10);measurements['find_seconds']=round(time.perf_counter()-start,3)
    large=json.dumps({'success':True,'data':{'markdown':'x'*10_000_000}}).encode()
    start=time.perf_counter();package=evidence.export_bytes(large,root/'large',workspace='synthetic-client',endpoint='scrape',request={'url':'https://example.com/large'},observed_at=stamp);measurements['large_export_seconds']=round(time.perf_counter()-start,3)
    tracemalloc.start();start=time.perf_counter();receipt=evidence.view(package,select='data.markdown');measurements['large_view_seconds']=round(time.perf_counter()-start,3);measurements['large_view_peak_traced_bytes']=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
    measurements['large_response_bytes']=len(large);measurements['large_view_output_bytes']=len(json.dumps(receipt).encode())
    result={'scope':'offline synthetic local filesystem only','provider_calls':0,'records':args.records,'inventory_count':listing['total'],'python':sys.version.split()[0],'os':platform.system(),'measurements':measurements,'limits':'Not API scalability, source coverage, throughput SLA, or credit-savings proof. Whole-response parsing uses proportional memory.'}
    (root/'receipt.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
