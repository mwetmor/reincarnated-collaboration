# PLATE VALUE, measured: CIE L* of the figure's pixels in classes -- GOLD (hue 35-75 deg in LCh(ab), C* > 22), CAPE/CLOTH
# (hue 250-340, C* > 7), PLATE (everything else on the figure: the near-black steel, C* <= 22, not cloth).
# Report the median L* of PLATE, the gold share of the figure, and the same on the SHEET (DK-A1_r1, chroma-key mask).
#   python3 e22_plate_lstar.py <godot stills dir> <stack> [--json f]
import sys, json, glob, numpy as np
from PIL import Image
def lab(rgb):
    c = rgb / 255.0; c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]); X = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(X > 0.008856, np.cbrt(X), 7.787 * X + 16 / 116)
    return np.stack([116 * f[:, 1] - 16, 500 * (f[:, 0] - f[:, 1]), 200 * (f[:, 1] - f[:, 2])], 1)
def classes(px):
    Lb = lab(px.astype(float)); C = np.hypot(Lb[:, 1], Lb[:, 2]); h = np.degrees(np.arctan2(Lb[:, 2], Lb[:, 1])) % 360
    gold = (h > 35) & (h < 95) & (C > 22); cloth = (h > 250) & (h < 340) & (C > 7) & ~gold
    plate = ~gold & ~cloth
    return dict(n=len(px), plate_L_median=round(float(np.median(Lb[plate, 0])), 2), plate_L_p25=round(float(np.percentile(Lb[plate, 0], 25)), 2),
                plate_L_p75=round(float(np.percentile(Lb[plate, 0], 75)), 2), gold_share=round(float(gold.mean()), 4), cloth_share=round(float(cloth.mean()), 4),
                plate_share=round(float(plate.mean()), 4), gold_L_median=round(float(np.median(Lb[gold, 0])), 2) if gold.any() else None)
d, st = sys.argv[1], sys.argv[2]; px = []
for f in sorted(glob.glob('%s/stack%s_idle_h*_s2_beauty.png' % (d, st))):
    b = np.asarray(Image.open(f).convert('RGB')); idm = np.asarray(Image.open(f.replace('beauty', 'id')).convert('RGB')).astype(int)
    m = (idm[..., 0] > 128) | (idm[..., 2] > 128)          # body red + garments blue; the mace (green) excluded
    px.append(b[m])
R = classes(np.vstack(px))
s = np.asarray(Image.open('../artifacts/DK-A1/DK-A1_r1.png').convert('RGB')).astype(int)
sm = ~((s[..., 1] > 150) & (s[..., 0] < 120) & (s[..., 2] < 120))
S = classes(s[sm].astype(np.uint8))
out = dict(render=R, sheet=S, delta_plate_L=round(R['plate_L_median'] - S['plate_L_median'], 2), delta_gold_share=round(R['gold_share'] - S['gold_share'], 4))
print(json.dumps(out, indent=1))
if '--json' in sys.argv: json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)
