#!/usr/bin/env python3
"""LAP N PART A — build the raw FCT event table + measured crit-multiplier distribution.

Sampling method (recorded so the table is reproducible):
  source : /Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/
           eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4   (1920x1080, 60 fps, 1034.10 s)
  span   : t = 680.0 .. 870.0 s  (combat span located by a 1-frame/10 s pre-scan: FCT present
           690..800 and 830..860; span padded to 680..870)
  cadence: fps=1/2  -> 95 sample frames, F0000..F0094, t = 680 + 2*index seconds
  why 2 s: FCT on-screen lifetime measured at ~1.2-1.5 s by tracking single strings across a
           10 fps burst at t=749..753 (see notes). 2.0 s > lifetime => each FCT event is
           sampled AT MOST ONCE. Verified: 1 adjacent-frame repeat of a (dmg,mult) pair in 90.
  OCR    : Apple Vision VNRecognizeTextRequest, .accurate, languageCorrection OFF (ocr.swift).
  colour : mean RGB of the brightest 12% of pixels in each OCR bounding box (glyph strokes).
"""
import re, csv, json, hashlib, collections, statistics
import numpy as np
from PIL import Image

OCR = "/tmp/pm4n/fct_ocr.tsv"
OUT = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
       "notes/2026-08-14-kc2-pm4-lap-n-crit-and-collision")
T0, DT = 680.0, 2.0

CRIT = re.compile(r'^(\d[\d,]{0,9})\s*\(x(\d\.\d{2})\)$')     # clean "12345 (x1.67)"
BARE = re.compile(r'^(\d[\d,]{0,9})$')                          # clean "12345"
MULT_ANY = re.compile(r'\(?x(\d)[.,](\d{2})\)?')                # multiplier salvaged from garbled read
HEALTH = re.compile(r'^\(?[\d,]+\s*/\s*[\d,]+\)?$')             # "(324,077/429,073)" health readout

_cache = {}
def swatch(path, bx, by, bw, bh):
    if path not in _cache:
        _cache[path] = np.asarray(Image.open(path).convert("RGB"))
    im = _cache[path]; H, W, _ = im.shape
    x0, x1 = int(bx*W), int((bx+bw)*W)
    y1, y0 = int((1-by)*H), int((1-by-bh)*H)
    x0, x1 = max(0, x0), min(W, x1); y0, y1 = max(0, y0), min(H, y1)
    if x1 <= x0 or y1 <= y0: return None
    p = im[y0:y1, x0:x1].reshape(-1, 3).astype(float)
    sel = p[p.sum(1) >= np.percentile(p.sum(1), 88)]
    return sel.mean(0)

# HUD text that sits at a fixed screen position in nearly every frame -> not combat text.
HUD_BOXES = [(0.715, 0.885, 0.025, 0.02), (0.822, 0.846, 0.030, 0.022),
             (0.486, 0.053, 0.028, 0.021), (0.297, 0.050, 0.062, 0.020),
             (0.645, 0.046, 0.055, 0.027), (0.700, 0.960, 0.120, 0.030)]
def is_hud(bx, by, bw, bh):
    return any(abs(bx-hx) < 0.02 and abs(by-hy) < 0.02 for hx, hy, _, _ in HUD_BOXES)

rows = []
for ln in open(OCR):
    f = ln.rstrip("\n").split("\t")
    if len(f) >= 7: rows.append(f)

events = []
for path, text, conf, bx, by, bw, bh in rows:
    bx, by, bw, bh = map(float, (bx, by, bw, bh))
    fi = int(re.search(r"F(\d+)\.png", path).group(1))
    t = T0 + DT*fi
    c = swatch(path, bx, by, bw, bh)
    if c is None: continue
    r, g, b = c
    rg = r/max(g, 1.0)
    # class of text
    if HEALTH.match(text):            cls = "health_readout"
    elif is_hud(bx, by, bw, bh):      cls = "hud"
    elif CRIT.match(text):            cls = "crit"
    elif BARE.match(text):            cls = "bare"
    elif MULT_ANY.search(text):       cls = "crit_garbled"
    else:                             cls = "other"
    m = CRIT.match(text)
    dmg = int(m.group(1).replace(",", "")) if m else (
          int(BARE.match(text).group(1).replace(",", "")) if BARE.match(text) else "")
    toks = [float(f"{a}.{b}") for a, b in MULT_ANY.findall(text)]
    mult = float(m.group(2)) if m else (toks[0] if toks else "")
    events.append(dict(
        frame=fi, t_sec=round(t, 1), text=text, ocr_conf=float(conf), cls=cls,
        damage=dmg, mult=mult,
        bbox_x=round(bx, 5), bbox_y=round(by, 5), bbox_w=round(bw, 5), bbox_h=round(bh, 5),
        mult_tokens=";".join(f"{v:.2f}" for v in toks),
        rgb_r=round(r, 1), rgb_g=round(g, 1), rgb_b=round(b, 1), r_over_g=round(rg, 3),
        colour_class=("red_taken" if rg >= 1.6 else "cream_dealt" if 1.02 <= rg < 1.6 else "neutral"),
    ))

events.sort(key=lambda e: (e["frame"], -e["ocr_conf"]))
FIELDS = list(events[0].keys())
with open(f"{OUT}/pm4n_fct_events.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=FIELDS); w.writeheader(); w.writerows(events)

# ---------- measured distribution ----------
def rung(v):  # cent value
    return round(v*100)

clean = [e for e in events if e["cls"] == "crit" and e["ocr_conf"] == 1.0]
# analysis unit = ONE crit multiplier token (a garbled OCR line can carry two merged events)
allc = []
for e in events:
    if e["cls"] in ("crit", "crit_garbled"):
        for v in [float(x) for x in e["mult_tokens"].split(";") if x]:
            allc.append(dict(e, mult=v))
lattice = collections.Counter(rung(e["mult"]) for e in allc)
with open(f"{OUT}/pm4n_crit_multipliers.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["frame","t_sec","ocr_conf","clean_read","damage","multiplier",
                "residue_cents","offset_family","implied_tier","source_text"])
    for e in sorted(allc, key=lambda z: (z["frame"], z["mult"])):
        k = rung(e["mult"]); r = k % 10
        fam = "A(+0.57)" if r == 7 else "B(+0.69)" if r == 9 else "unresolved"
        tier = f"{(k-57)/100:.2f}" if r == 7 else f"{(k-69)/100:.2f}" if r == 9 else ""
        if tier and not (1.00 <= float(tier) <= 1.55): tier = ""
        w.writerow([e["frame"], e["t_sec"], e["ocr_conf"], int(e["cls"] == "crit"),
                    e["damage"], f"{e['mult']:.2f}", r, fam, tier, e["text"]])

print("=== PART A — measured effective crit multiplier ===")
print(f"sample frames                 : 95   (t=680..868 s, 2.0 s cadence)")
print(f"OCR text observations         : {len(events)}")
print(f"clean crit events (conf 1.0)  : {len(clean)}")
print(f"all crit events w/ multiplier : {len(allc)}")
print("\nmultiplier lattice (all crit events):")
for k in sorted(lattice): print(f"   x{k/100:.2f}   {lattice[k]:4d}   residue mod 0.10 = .{k%10:02d}")

res = collections.Counter(rung(e["mult"]) % 10 for e in allc)
print("\nresidue mod 0.10 :", dict(res))

# tier decomposition: offset A = 0.57, offset B = 0.69 (differ by exactly 0.12)
OFFA, OFFB = 57, 69
tiers = collections.Counter()
for e in allc:
    k = rung(e["mult"])
    if k % 10 == 7 and 100 <= k-OFFA <= 150: tiers[k-OFFA] += 1
    elif k % 10 == 9 and 100 <= k-OFFB <= 150: tiers[k-OFFB] += 1
print("\ntier decomposition (offsetA=+0.57, offsetB=+0.69):")
tot = sum(tiers.values())
for k in sorted(tiers): print(f"   tier x{k/100:.2f}   {tiers[k]:4d}   {100*tiers[k]/tot:5.1f}%")

# PTH survival readout: under R~U(1,PTH) the density of R over a band is proportional to S(r)
BANDS = {110: (90, 105), 120: (105, 120), 130: (120, 130), 140: (130, 135), 150: (135, 182)}
print("\nband density -> PTH survival S(r)=P(PTH>=r)   [conditional on these being direct attacks]")
d0 = None
for k in sorted(BANDS):
    lo, hi = BANDS[k]; n = tiers.get(k, 0); dens = n/(hi-lo)
    if d0 is None: d0 = dens
    print(f"   roll band [{lo:3d},{hi:3d})  n={n:4d}  density={dens:6.2f}  S~{dens/d0:5.3f}")

mults = [e["mult"] for e in allc]
print(f"\nmean effective multiplier on crit events   = {statistics.mean(mults):.4f}")
print(f"median                                     = {statistics.median(mults):.4f}")
print(f"min / max                                  = {min(mults):.2f} / {max(mults):.2f}")

# crit rate (graded): cream player-dealt bare vs crit, conf 1.0, excluding hud/health
dealt_bare = [e for e in events if e["cls"] == "bare" and e["ocr_conf"] == 1.0
              and e["colour_class"] == "cream_dealt"]
dealt_crit = [e for e in clean if e["colour_class"] == "cream_dealt"]
n_b, n_c = len(dealt_bare), len(dealt_crit)
print(f"\ncream player-dealt: non-crit {n_b} | crit {n_c} | apparent crit share "
      f"{100*n_c/(n_b+n_c):.1f}%  [LOWER BOUND - see caveat]")

digests = {}
for name in ["pm4n_fct_events.csv", "pm4n_crit_multipliers.csv"]:
    p = f"{OUT}/{name}"
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    n = sum(1 for _ in open(p)) - 1
    digests[name] = {"sha256": h, "rows": n}
    print(f"\n{name}: rows={n} sha256={h}")
json.dump(digests, open("/tmp/pm4n/digests_partial.json", "w"), indent=2)
