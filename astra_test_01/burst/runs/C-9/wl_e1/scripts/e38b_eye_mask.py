# E1 stage J 3b, part 2 (outside Blender): rasterise the slit's UV triangles into the emission image -- glow colour on the mask
# dilated by --dil px, a hot near-white CORE where the mask survives a 1-px erosion.  python3 e38b_eye_mask.py <uv.json> <out.png> --glow r,g,b --core r,g,b [--dil 3]
import sys, json, numpy as np
from PIL import Image, ImageDraw, ImageFilter
a = sys.argv[1:]; UVJ, OUT = a[0], a[1]; opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
GLOW = np.array([float(x) for x in opt('--glow', '0.62,0.30,1.0').split(',')]); CORE = np.array([float(x) for x in opt('--core', '0.96,0.92,1.0').split(',')]); DIL = int(opt('--dil', '3'))
J = json.load(open(UVJ)); W_, H_ = J['size']; mask = Image.new('L', (W_, H_), 0); d = ImageDraw.Draw(mask)
for tri in J['tris']: d.polygon([(u * W_, (1 - v) * H_) for u, v in tri], fill=255)
m1 = mask.filter(ImageFilter.MaxFilter(2 * DIL + 1)).filter(ImageFilter.GaussianBlur(1.2)); core = mask.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
A = np.asarray(m1, np.float32)[..., None] / 255.0; Cc = np.asarray(core, np.float32)[..., None] / 255.0
em = A * GLOW * (1 - Cc) + Cc * CORE
Image.fromarray((np.clip(em, 0, 1) * 255).astype(np.uint8)).save(OUT)
print('mask texels', int((np.asarray(mask) > 0).sum()), 'dilated', int((np.asarray(m1) > 10).sum()), 'core', int((np.asarray(core) > 128).sum()))
