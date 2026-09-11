from pathlib import Path
from PIL import Image
import json,hashlib,io
p=Path(__file__).resolve().parent
if (p/'evidence/lossless-packaging.json').exists():raise SystemExit('Refusing to overwrite encoding lineage')
peak=sum(f.stat().st_size for f in p.rglob('*')if f.is_file());records=[]
for f in sorted((p/'evidence').rglob('*.png')):
 raw=f.read_bytes();im=Image.open(io.BytesIO(raw));im.load();pixels=im.tobytes();pixel_hash=hashlib.sha256(pixels).hexdigest();buf=io.BytesIO();im.save(buf,format='PNG',optimize=True,compress_level=9);out=buf.getvalue();check=Image.open(io.BytesIO(out));assert check.mode==im.mode and check.size==im.size and check.tobytes()==pixels
 if len(out)<len(raw):f.write_bytes(out)
 records.append({'path':str(f.relative_to(p)),'dimensions':im.size,'mode':im.mode,'decoded_pixels_sha256':pixel_hash,'original_png_sha256':hashlib.sha256(raw).hexdigest(),'packaged_png_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'before_bytes':len(raw),'after_bytes':f.stat().st_size,'exact_pixels_preserved':True})
result={'peak_observed_before_packaging_bytes':peak,'registered_limit_bytes':100000000,'historical_limit_exceeded':True,'codec_only':True,'files':records,'current_bytes_before_receipt':sum(f.stat().st_size for f in p.rglob('*')if f.is_file())};(p/'evidence/lossless-packaging.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='files'}))
