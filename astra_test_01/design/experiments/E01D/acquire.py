from pathlib import Path
import json,subprocess,sys,urllib.parse,datetime
b=Path(__file__).resolve().parent;game=sys.argv[1];start=float(sys.argv[2]);meta=json.loads((b/'evidence'/'metadata.json').read_text());file=next(f for f in meta['files']if f['name'].endswith('.mp4'));id=meta['metadata']['identifier'];url='https://archive.org/download/'+id+'/'+urllib.parse.quote(file['name']);out=b/'evidence'/f'{game}-{start:g}.mp4';assert not out.exists()
cmd=['/opt/homebrew/bin/ffmpeg','-hide_banner','-loglevel','warning','-rw_timeout','20000000','-ss',str(start),'-i',url,'-t','10','-an','-c:v','libx264','-preset','fast','-crf','20','-fs','15000000','-movflags','+faststart',str(out)]
r={'game':game,'source_page':'https://archive.org/details/'+id,'source_url':url,'start_s':start,'duration_requested_s':10,'command':cmd,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=90);r.update({'returncode':p.returncode,'stderr':p.stderr[-12000:]})
except subprocess.TimeoutExpired:r.update({'returncode':None,'error':'90s acquisition timeout'})
r['output_bytes']=out.stat().st_size if out.exists()else 0
(b/'evidence'/f'{game}-{start:g}-acquisition.json').write_text(json.dumps(r,indent=2)+'\n');print(game,r['returncode'],r['output_bytes'])
