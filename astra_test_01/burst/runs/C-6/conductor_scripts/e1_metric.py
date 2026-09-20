# E1 probe metric (R-C6-39, pinned before results): figure HEIGHT ÷ SHOULDER WIDTH on the green-keyed matte, frame 0 vs frame 72 (and the median of f60–f84).
# A figure that is "stood up" by the video model gets taller relative to its shoulders; HOLDS = |Δratio| < 10 % and crown/shoulder tops still visible by eye.
# The weapon is excluded by measuring width only inside the BODY column band found from the sole row. usage: e1_metric.py <mp4 relpath> <label>
import sys, subprocess, glob, pathlib, json, tempfile
from PIL import Image
import numpy as np
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); mp4 = B/sys.argv[1]; label = sys.argv[2]
wd = pathlib.Path(tempfile.mkdtemp(prefix='e1_', dir='/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/c798c4cb-f5ae-4f80-8419-ca68760f2e6f/scratchpad'))
subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-y','-i',str(mp4),'-vf','select=not(mod(n\\,6))','-vsync','vfr',str(wd/'f_%03d.png')],check=True)
def ratio(p):
    a = np.asarray(Image.open(p).convert('RGB')).astype(int); fg = ~((a[...,1] > 150) & (a[...,0] < 120) & (a[...,2] < 120)); ys, xs = np.nonzero(fg)
    if not len(ys): return None
    sole = ys.max(); cx = int(np.median(xs[ys > sole - 30])); H0 = sole - ys.min()
    band = fg[:, max(0, cx - int(0.45 * H0)):cx + int(0.45 * H0)]          # body column ±0.45 H (drops a far-flung weapon)
    rows = np.nonzero(band.any(1))[0]; crown = rows.min(); H = sole - crown
    sh = band[crown + int(0.18 * H):crown + int(0.34 * H)]                   # shoulder band 18–34 % below the crown
    widths = [np.nonzero(r)[0].max() - np.nonzero(r)[0].min() for r in sh if r.any()]
    return (H / float(np.median(widths))) if widths else None, int(H)
fs = sorted(glob.glob(str(wd/'f_*.png'))); R = [ratio(f) for f in fs]
r0 = R[0][0]; mid = [r[0] for r in R[10:15] if r and r[0]]; r72 = float(np.median(mid)) if mid else None
out = dict(label=label, clip=str(mp4.name), sampled=len(fs), ratio_f0=round(r0, 3), ratio_f60_84_median=round(r72, 3) if r72 else None, delta_pct=round(100 * (r72 - r0) / r0, 1) if r72 else None, height_f0=R[0][1], heights=[r[1] if r else None for r in R], verdict_rule='HOLDS if |delta| < 10 % (and crown/shoulder tops visible by eye)')
print(json.dumps(out))
