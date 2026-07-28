#!/usr/bin/env python3
"""
KIT-CAL-1 G-8, task 6: find every frame in the corpus that renders a MONSTER's
numeric health as "(cur/max)" over the monster's head.

Method, and why it is a detector-then-eye pass rather than an OCR pass.

The in-world monster-health numerals use the same near-white, dark-outlined,
low-saturation face as the player globes -- so the FCT/globe brightness rule
(`min channel > 150 AND chroma < 50`) isolates them from the world with no
tuning. What the glyph model does NOT have is a template for the THOUSANDS
COMMA, which this string uses ("13,571"). Running the greedy matcher over a
string containing an unmodelled glyph is exactly panel_ocr's G-3 failure:
the matcher does not abstain at the comma, it substitutes the nearest digit
and returns a confidently wrong number.

So: the machine finds the candidates (cheap, exhaustive, no false negatives at
this threshold), and galadriel reads them at 6x (accurate, and only over the
handful of bands the detector returns). The detector's job is recall; the eye's
job is precision. Banking a wrong monster max-HP here would corrupt the HP
composition rule the run is trying to pin, which is the thing the Slith
cross-check already falsified once.

Candidate rule: a horizontally-contiguous bright-achromatic band, 8-16 px tall,
45-260 px wide, lying inside the play area (HUD regions masked out), whose
column profile contains at least 6 ink groups -- a damage number like "515" has
3, a "(13,571/14,812)" has 14.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
           "galadriel/captures/2026-07-28-kitcal1-g8")

BRIGHT_MIN, CHROMA_MAX = 150, 50
# play area: drop the PlayStats panel / quest tracker (right), the globes +
# skill bar (bottom), and the boss nameplate strip (top, handled separately).
Y0, Y1 = 100, 960
X0, X1 = 40, 1330


def bands(m):
    """Row-runs of ink, returned as (y0, y1)."""
    rows = m.sum(axis=1) > 0
    out, run = [], None
    for i, v in enumerate(rows):
        if v:
            run = [i, i] if run is None else [run[0], i]
        elif run is not None:
            out.append(tuple(run))
            run = None
    if run:
        out.append(tuple(run))
    return out


def groups(col):
    out, run = [], False
    n = 0
    for v in col:
        if v > 0 and not run:
            n += 1
            run = True
        elif v == 0:
            run = False
    return n


def main():
    ids = sorted(int(f.name[12:-5]) for f in SRC.iterdir()
                 if f.name.startswith("Screenshot (") and f.name.endswith(").png"))
    hits = {}
    (OUT / "monhp-candidates").mkdir(parents=True, exist_ok=True)
    for i in ids:
        with Image.open(SRC / f"Screenshot ({i}).png") as im:
            im = im.convert("RGB")
            a = np.asarray(im).astype(np.int16)
        sub = a[Y0:Y1, X0:X1]
        mx, mn = sub.max(axis=2), sub.min(axis=2)
        m = (mn > BRIGHT_MIN) & ((mx - mn) < CHROMA_MAX)
        found = []
        for by0, by1 in bands(m):
            h = by1 - by0 + 1
            if not (8 <= h <= 16):
                continue
            colprof = m[by0:by1 + 1].sum(axis=0)
            nz = np.nonzero(colprof)[0]
            if not len(nz):
                continue
            # split the band into horizontally separated TEXT RUNS (>=12 blank
            # columns apart) -- two unrelated numbers can share a row.
            runs, s, prev = [], nz[0], nz[0]
            for x in nz[1:]:
                if x - prev > 12:
                    runs.append((s, prev))
                    s = x
                prev = x
            runs.append((s, prev))
            for rx0, rx1 in runs:
                w = rx1 - rx0 + 1
                if not (45 <= w <= 260):
                    continue
                ng = groups(colprof[rx0:rx1 + 1])
                if ng < 6:
                    continue
                # paren shape test, inline (see g8_monhp_filter.py for the
                # rationale): a health readout opens on '(' and closes on ')',
                # both <=5 px wide and spanning the full cap height. Tooltip
                # lines ("18-24 Physical Damage") fail both ends.
                band = m[by0:by1 + 1, rx0:rx1 + 1]
                gs, run = [], None
                for gi, gv in enumerate(band.sum(axis=0)):
                    if gv > 0:
                        run = [gi, gi] if run is None else [run[0], gi]
                    elif run is not None:
                        gs.append(tuple(run))
                        run = None
                if run:
                    gs.append(tuple(run))
                paren = False
                if len(gs) >= 6:
                    (l0, l1), (r0, r1) = gs[0], gs[-1]
                    lh = np.nonzero(band[:, l0:l1 + 1].sum(axis=1))[0]
                    rh = np.nonzero(band[:, r0:r1 + 1].sum(axis=1))[0]
                    if len(lh) and len(rh):
                        paren = ((l1 - l0 + 1) <= 5 and (r1 - r0 + 1) <= 5
                                 and (lh.max() - lh.min() + 1) >= h - 2
                                 and (rh.max() - rh.min() + 1) >= h - 2)
                found.append({"y0": int(Y0 + by0), "y1": int(Y0 + by1),
                              "x0": int(X0 + rx0), "x1": int(X0 + rx1),
                              "h": int(h), "w": int(w), "n_groups": int(ng),
                              "paren": bool(paren)})
        if found:
            hits[i] = found
            for k, b in enumerate(found):
                if not b["paren"]:
                    continue
                c = im.crop((b["x0"] - 8, b["y0"] - 5, b["x1"] + 8, b["y1"] + 5))
                c.resize((c.width * 6, c.height * 6), Image.LANCZOS).save(
                    OUT / "monhp-candidates" / f"f{i:04d}-{k}.png")
            np_ = sum(1 for b in found if b["paren"])
            if np_:
                print(f"f{i:4d}  {np_} PAREN band(s): "
                      + "; ".join(f"({b['x0']},{b['y0']}) {b['w']}x{b['h']} g{b['n_groups']}"
                                  for b in found if b["paren"]), flush=True)
    with open(OUT / "g8-monhp-candidates.json", "w") as f:
        json.dump(hits, f, indent=1)
    print(f"\n{len(hits)} frames with candidates, "
          f"{sum(len(v) for v in hits.values())} bands total")


if __name__ == "__main__":
    main()
