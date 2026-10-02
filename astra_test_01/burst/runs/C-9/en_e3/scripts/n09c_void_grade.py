# EN-E3 VOID GRADE (the conductor's note on the void drone: the chitin read dusty mauve; push it toward black-violet so it reads as void
# against the arena floor, keep the crimson seams and the pale bone scythes/spikes bright).
#   python3 scripts/n09c_void_grade.py <in.png> <out.png> [strength 0..1] [--boss]
# A texel is CHITIN if it is mid-dark and not strongly red (crimson seams/eyes) and not pale (bone). Chitin is pulled toward a deep
# black-violet target, keeping its own luminance detail (hatching) at a reduced amplitude. --boss: the boss record's variant grade --
# the same mesh, the chitin pushed to a darker, more violet-chaos tone and the seams warmed toward gold.
import sys, numpy as np
from PIL import Image
from scipy import ndimage
IN, OUT = sys.argv[1:3]; K = float(sys.argv[3]) if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else 0.75; BOSS = '--boss' in sys.argv
A = np.asarray(Image.open(IN).convert('RGB')).astype(np.float32); R, G, B = A[..., 0], A[..., 1], A[..., 2]; L = A.mean(2)
red = (R - np.maximum(G, B)) > 28; pale = L > 165
chit = ~red & ~pale
w = ndimage.gaussian_filter(chit.astype(np.float32), 1.2)[..., None] * K
target = np.array([46, 30, 58] if not BOSS else [40, 22, 66], np.float32)
detail = (L - ndimage.gaussian_filter(L, 3))[..., None]
graded = np.clip(target + 0.45 * detail + 0.25 * (A - L[..., None]), 0, 255)
out = A * (1 - w) + graded * w
if BOSS:
    sm = ndimage.gaussian_filter(red.astype(np.float32), 1.0)[..., None]
    out = out * (1 - 0.5 * sm) + np.clip(A * np.array([1.05, 0.85, 0.45]) + np.array([30, 20, 0]), 0, 255) * 0.5 * sm
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(OUT)
print('void grade%s: chitin %.1f%% of texels, mean lum %.1f -> %.1f' % (' (boss)' if BOSS else '', 100 * chit.mean(), L.mean(), out.mean()))
