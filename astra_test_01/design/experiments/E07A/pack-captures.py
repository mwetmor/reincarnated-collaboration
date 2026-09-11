from pathlib import Path
from PIL import Image
import json,hashlib,time
p=Path(__file__).resolve().parent;records=[];start=time.monotonic()
for i,f in enumerate(sorted((p/'evidence/batch-01').glob('*.png'))):
 im=Image.open(f);out=f.with_suffix('.webp');im.save(out,lossless=True,method=4,exact=True);assert im.convert('RGBA').tobytes()==Image.open(out).convert('RGBA').tobytes();records.append({'original_path':str(f.relative_to(p)),'packed_path':str(out.relative_to(p)),'original_bytes':f.stat().st_size,'packed_bytes':out.stat().st_size,'original_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'packed_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'rgba_exact':True});f.unlink()
 if i%200==0:print(i,'packed',flush=True)
(p/'evidence/lossless-pack.json').write_text(json.dumps({'records':records,'elapsed_s':time.monotonic()-start},indent=2)+'\n');print('owned bytes',sum(f.stat().st_size for f in p.rglob('*')if f.is_file()))
