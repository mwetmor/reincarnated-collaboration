# Hidden known-bad JUDGE control for K1p-jdg-01: a horizontally mirrored copy of candidate C (key light lands upper-RIGHT → axis 3 must score ≤ 2). Conductor-side control preparation, as at K1-jdg-04 (K1-control/k1_control_mirror_4.png).
import hashlib, pathlib, sys
from PIL import Image, ImageOps
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-1/artifacts')
src = B/'K1p-gen-01'/(sys.argv[1] if len(sys.argv)>1 else 'k1p_master_C.png'); dst = B/'K1p-control'/'k1p_control_mirror.png'
dst.parent.mkdir(exist_ok=True)
im = Image.open(src); ImageOps.mirror(im).save(dst, 'PNG')
print('control:', dst, 'from', src.name, 'size', im.size, 'sha256', hashlib.sha256(dst.read_bytes()).hexdigest()[:12])
