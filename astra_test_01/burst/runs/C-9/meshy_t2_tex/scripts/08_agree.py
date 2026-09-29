# C-9 T5: do the 19.77 ring (sheet A) and the 52.95 views (sheet B) agree where
# they overlap? A seam or a double-marked feature there is the failure this
# whole two-sheet approach risks, and it is invisible in either sheet alone:
# each one looks fine, and only the texels BOTH painted can show the
# disagreement.
#
#   python3 scripts/08_agree.py <texA.png> <texB.png> <out_diff.png>
#
# Measured in linear light on the raw (pre-fill) bakes, restricted to texels
# both actually painted -- comparing filled texels would compare two guesses.
import json, os, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TA, TB, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
A = np.load(TA.replace(".png", "_raw.npy"))
B = np.load(TB.replace(".png", "_raw.npy"))
MA = np.array(Image.open(TA.replace(".png", "_mask.png")).transpose(
    Image.FLIP_TOP_BOTTOM)) > 127
MB = np.array(Image.open(TB.replace(".png", "_mask.png")).transpose(
    Image.FLIP_TOP_BOTTOM)) > 127
both = MA & MB
print("sheet A painted %d texels, sheet B %d, BOTH %d (%.1f%% of A, %.1f%% of B)"
      % (MA.sum(), MB.sum(), both.sum(), 100 * both.sum() / max(MA.sum(), 1),
         100 * both.sum() / max(MB.sum(), 1)))
if not both.any():
    print("no overlap"); sys.exit(0)


def l2s(x):
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


d = np.linalg.norm(l2s(A) - l2s(B), axis=2) / np.sqrt(3.0) * 255.0
v = d[both]
# WHAT THE BLEND ACTUALLY EXPOSES. Comparing the two sheets everywhere they
# both painted over-reports: most of that overlap is a texel one sheet saw
# square-on and the other saw at a grazing angle, where facing^4 has already
# reduced the second to nearly nothing and no viewer will ever see its opinion.
# A seam is only visible where the two contribute COMPARABLY, so the
# disagreement is weighted by how balanced they are: 2*min/(a+b), which is 1
# at a 50/50 blend and 0 where one sheet dominates.
WA = np.load(TA.replace(".png", "_wsum.npy"))
WB = np.load(TB.replace(".png", "_wsum.npy"))
bal = np.zeros_like(WA)
den = WA + WB
nz = den > 0
bal[nz] = 2.0 * np.minimum(WA, WB)[nz] / den[nz]
bw = bal[both]
exposed = float((v * bw).sum() / max(bw.sum(), 1e-9))
contested = both & (bal > 0.5)
print("  BLEND-EXPOSED delta (weighted by 2*min/(a+b)): %.2f" % exposed)
print("  contested texels (both sheets within 3x of each other): %d (%.1f%% of "
      "overlap); their mean delta %.2f, p90 %.2f"
      % (int(contested.sum()), 100 * contested.sum() / max(both.sum(), 1),
         float(d[contested].mean()) if contested.any() else 0.0,
         float(np.percentile(d[contested], 90)) if contested.any() else 0.0))
rep = dict(overlap_texels=int(both.sum()),
           blend_exposed_delta=round(exposed, 3),
           contested_texels=int(contested.sum()),
           contested_mean_delta=round(float(d[contested].mean()), 3) if contested.any() else None,
           mean_delta_sRGB=round(float(v.mean()), 3),
           median=round(float(np.median(v)), 3),
           p90=round(float(np.percentile(v, 90)), 3),
           p99=round(float(np.percentile(v, 99)), 3),
           pct_over_8=round(100 * float((v > 8).mean()), 3),
           pct_over_24=round(100 * float((v > 24).mean()), 3))
print("  delta on the overlap (sRGB 0-255): mean %.2f  median %.2f  p90 %.2f  "
      "p99 %.2f" % (rep["mean_delta_sRGB"], rep["median"], rep["p90"], rep["p99"]))
print("  %.2f%% of overlapping texels differ by more than 8/255, %.2f%% by more "
      "than 24/255" % (rep["pct_over_8"], rep["pct_over_24"]))
# a DOUBLE-MARKED feature is a disagreement that is structured, not uniform:
# a constant offset is a tone difference, a high local variance is ghosting
mean_off = (l2s(A) - l2s(B))[both].mean(0) * 255.0
rep["mean_channel_offset_sRGB"] = [round(float(x), 2) for x in mean_off]
resid = v - v.mean()
rep["structured_fraction"] = round(float((np.abs(resid) > v.mean()).mean()), 4)
print("  mean channel offset (A-B) %s  -- a uniform offset is a TONE shift, "
      "scattered high values are DOUBLE MARKING" % rep["mean_channel_offset_sRGB"])
hm = np.zeros(d.shape + (3,), np.uint8)
n = np.clip(d / 32.0, 0, 1)
hm[..., 0] = (n * 255).astype(np.uint8)
hm[..., 1] = ((1 - n) * 255 * both).astype(np.uint8)
hm[~both] = 30
Image.fromarray(hm).transpose(Image.FLIP_TOP_BOTTOM).save(OUT)
json.dump(rep, open(os.path.join(ROOT, "work", "agree_report.json"), "w"), indent=1)
print("wrote %s" % OUT)
