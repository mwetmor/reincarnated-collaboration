"""Supplement the same E01 publisher-source pass; append sources, no overwritten art."""
from pathlib import Path
import concurrent.futures,hashlib,json,subprocess
from PIL import Image
p=Path(__file__).resolve().parent
if (p/'sources.json').exists() and any(x.get('inspection','').startswith('VISUALLY_') for x in json.loads((p/'sources.json').read_text())):
    raise SystemExit('Reviewed manifest exists. Run validate_packet.py; do not restart completed intake.')
rows=json.loads((p/'sources.json').read_text());jobs=[]
for i,n in enumerate(['shiverarmor01','frozenarmor02'],5):jobs.append((f'D2-0{i}','Diablo II','https://classic.battle.net/images/battle/diablo2exp/images/skills/'+n+'.jpg','https://classic.battle.net/diablo2exp/skills/sorceress-cold.shtml','Blizzard Entertainment','Original D2 / LoD-era guide; exact patch unknown; NOT D2R'))
for i,n in enumerate(['game_bridgeBroken01','game_bridgeFixed01','game_1shotChest01'],4):jobs.append((f'GD-0{i}','Grim Dawn','https://www.grimdawn.com/wp-content/uploads/sites/3/2019/09/'+n+'.jpg','https://www.grimdawn.com/guide/gameplay/exploration/','Crate Entertainment','Grim Dawn official guide; exact patch unknown'))
d=json.loads((p/'raw'/'le-api.txt').read_text())['899770']['data']
for i,idx in enumerate([0,2,4,6],8):jobs.append((f'LE-{i:02}','Last Epoch',next(x for x in d['screenshots'] if x['id']==idx)['path_full'],'https://store.steampowered.com/app/899770/','Eleventh Hour Games','Last Epoch; patch unknown'))
def get(j):
 id,g,u,page,pub,ed=j;f=p/'media'/(id+'.jpg')
 if not f.exists():subprocess.run(['curl','-fLsS','--max-time','25',u,'-o',str(f)],check=True)
 with Image.open(f) as im:w,h=im.size
 return dict(id=id,game=g,url=u,page=page,publisher=pub,edition=ed,path='media/'+f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size,dimensions=[w,h],fps=None,timestamp=None,native_content_rect=[0,0,w,h],capture_settings='Unknown; full publisher file',acquired_utc='2026-09-11',inspection='PENDING',role='Still only',rights_context='Publisher media; internal genre comparison')
with concurrent.futures.ThreadPoolExecutor(6) as ex:
 for r in ex.map(get,jobs):
  if not any(x['id']==r['id'] for x in rows):rows.append(r)
  print(r['id'],r['dimensions'])
(p/'sources.json').write_text(json.dumps(rows,indent=2)+'\n')
