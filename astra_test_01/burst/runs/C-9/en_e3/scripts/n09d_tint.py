# EN-E3 provisional summon grades from ONE Tripo texture (no paint pass: the Astra limit): a luminance-preserving tint toward a target
# palette, keeping the ink/hatching detail. larva = a pale bloated grub (ivory-grey, faint violet); worm = sickly aether-poison
# (bruise-violet back, bile-green belly glints).
#   python3 scripts/n09d_tint.py <in.png> <out.png> <larva|worm>
import sys, numpy as np
from PIL import Image
from scipy import ndimage
IN, OUT, WHO = sys.argv[1:4]
A = np.asarray(Image.open(IN).convert('RGB')).astype(np.float32); L = A.mean(2, keepdims=True)
dark, light = {'larva': ([92, 82, 88], [228, 220, 200]), 'worm': ([58, 36, 72], [176, 186, 104])}[WHO]
t = np.clip((L - 40) / 160.0, 0, 1)
base = np.array(dark, np.float32) * (1 - t) + np.array(light, np.float32) * t
detail = L - ndimage.gaussian_filter(L[..., 0], 3)[..., None]
out = np.clip(base + 0.6 * detail + 0.15 * (A - L), 0, 255) * 0.8 + A * 0.2
Image.fromarray(out.astype(np.uint8)).save(OUT); print('tint', WHO, 'mean lum %.1f -> %.1f' % (A.mean(), out.mean()))
