# EN-E3: a PAINTED mouth interior for the maw (conductor's readability pass: "replace the dark box with a painted mouth interior --
# gums, the throat glow of the bile spit"). Same wash + ink hand as the VFX (n20_vfx.wash): madder gums pooling at the rim, ivory
# tooth roots along both edges, a deep throat, and a pale bile-ochre pool at its centre (paint, not light: no emission).
#   python3 scripts/n21_mouth_tex.py <out.png>
import sys, numpy as np
from PIL import Image
sys.path.insert(0, __file__.rsplit('/', 1)[0]); V = __import__('n20_vfx')
S = 512; yy, xx = np.mgrid[0:S, 0:S] / (S - 1.0)
base = np.zeros((S, S, 3)) + np.array([128, 44, 40], float)                     # gums: madder
d = np.hypot((xx - 0.5) / 0.42, (yy - 0.5) / 0.36)
throat = np.clip(1.2 - d, 0, 1)
rgb, al = V.wash(np.clip(1.3 - d, 0, 1), (92, 26, 30), (54, 14, 18), S, S, pool=0.7)   # the throat's darker wash
out = base * (1 - al[..., None]) + rgb * al[..., None]
bile = np.clip(1 - np.hypot((xx - 0.5) / 0.16, (yy - 0.55) / 0.12), 0, 1) ** 0.8
rb, ab = V.wash(bile, (196, 186, 104), (150, 140, 60), S, S, pool=0.5)
out = out * (1 - ab[..., None] * 0.85) + rb * ab[..., None] * 0.85
for edge in (0.06, 0.94):                                                        # tooth roots along the two long edges
    for i in range(14):
        cx = (i + 0.5) / 14 * S; cy = edge * S
        m = V.disc(S, S, cx, cy, S * 0.03, 1.6)
        rt, at = V.wash(m, (226, 214, 176), (170, 150, 110), S, S)
        out = out * (1 - at[..., None]) + rt * at[..., None]
g = V.paper(S, S) * 6
Image.fromarray(np.clip(out + g[..., None], 0, 255).astype(np.uint8)).save(sys.argv[1]); print('wrote', sys.argv[1])
