from pathlib import Path
from PIL import Image
import sys,hashlib,json
f=Path(sys.argv[1]);im=Image.open(f);out=f.with_suffix('.webp');im.save(out,lossless=True,method=4,exact=True);assert im.convert('RGBA').tobytes()==Image.open(out).convert('RGBA').tobytes();r={'original_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'packed_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'original_bytes':f.stat().st_size,'packed_bytes':out.stat().st_size,'rgba_exact':True};f.unlink();print(json.dumps(r))
