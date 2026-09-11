"""Bounded publisher-still acquisition. Never modifies downloaded image bytes."""
import concurrent.futures, hashlib, json, subprocess
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent
if (ROOT/'sources.json').exists() and any(x.get('inspection','').startswith('VISUALLY_') for x in json.loads((ROOT/'sources.json').read_text())):
    raise SystemExit('Reviewed manifest exists. Run validate_packet.py; do not restart completed intake.')
jobs=[]
def add(id,game,url,page,publisher,edition):jobs.append(dict(id=id,game=game,url=url,page=page,publisher=publisher,edition=edition))
d2='https://classic.battle.net'
for id,url,page in [('D2-01','/images/battle/diablo2exp/images/skills/frozenorb01.jpg','/diablo2exp/skills/sorceress-cold.shtml'),('D2-02','/diablo2exp/basics/images/ss01.jpg','/diablo2exp/basics/'),('D2-03','/images/battle/diablo2exp/images/npcs/hire01.jpg','/diablo2exp/npcs/act1.shtml')]:add(id,'Diablo II',d2+url,d2+page,'Blizzard Entertainment','Original Diablo II / LoD-era official guide; exact patch unknown; NOT D2R')
for i,file in enumerate(['2015-12_alpinevalley01.jpg','2017-10-06_GDX1-4.jpg','2019-03-GDX2_08.png'],1):add(f'GD-0{i}','Grim Dawn','https://www.grimdawn.com/wp-content/uploads/sites/3/2019/06/'+file,'https://www.grimdawn.com/media/','Crate Entertainment', ['Base-game promotional screenshot, Dec 2015','Ashes of Malmouth promotional screenshot, Oct 2017','Forgotten Gods promotional screenshot, Feb 2019'][i-1]+'; exact patch unknown')
for name,app,pub,ids in [('le',899770,'Eleventh Hour Games',[1,3,5]),('poe',238960,'Grinding Gear Games',[12,13,14,16])]:
 d=json.loads((ROOT/'raw'/f'{name}-api.txt').read_text())[str(app)]['data']
 for i,idx in enumerate(ids,1):
  row=next(x for x in d['screenshots'] if x['id']==idx)
  add(f'{name.upper()}-0{i}',d['name'],row['path_full'],f'https://store.steampowered.com/app/{app}/',pub,('PoE1; NOT PoE2' if name=='poe' else 'Last Epoch')+'; exact screenshot patch unknown')
def fetch(j):
 path=ROOT/'media'/(j['id']+Path(j['url'].split('?')[0]).suffix)
 if not path.exists():subprocess.run(['curl','-fLsS','--max-time','30',j['url'],'-o',str(path)],check=True)
 with Image.open(path) as im: dims=im.size
 return dict(j,path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size,dimensions=list(dims),fps=None,timestamp=None,native_content_rect=[0,0,*dims],capture_settings='Unknown; publisher-distributed full file, not guaranteed lossless game framebuffer',acquired_utc='2026-09-11',inspection='PENDING',role='Still only; motion and dynamic-state claims excluded',rights_context='Publisher media, internal genre comparison; not project artwork or redistribution asset')
results=[]
with concurrent.futures.ThreadPoolExecutor(6) as pool:
 for j,res in zip(jobs,pool.map(fetch,jobs)):
  results.append(res); print(res['id'],res['dimensions'],res['sha256'][:12])
(ROOT/'sources.json').write_text(json.dumps(results,indent=2)+'\n')
