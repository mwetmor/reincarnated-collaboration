#!/usr/bin/env python3
"""L8 HOLY glyph — collision / coherence scoring.

Two measures, both reported so the read is falsifiable:

  dHash-32 Hamming distance  — low-frequency structural similarity of the DARK-COMPOSITED
      32px render (i.e. what the eye gets at HUD size). Lower = more confusable.
  bbox-normalised mask IoU   — each glyph's alpha mask is cropped to its bbox and rescaled
      to 64x64, then intersection-over-union. Measures silhouette overlap independent of
      scale/placement. Higher = more confusable.

Also emits per-candidate layer cards (Clean / Stroke / Underlay composited on RGB 35,35,45)
and a size-ladder strip at 24/32/48/64 px.

Run:  python3 agentic_orchestration/galadriel/pipeline/l8-holy-glyph-score.py
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = "/Users/admin/Games/reincarnated-collaboration"
PACK = os.path.join(
    ROOT,
    "matt_notes_handoff_docs/recent-synty-packs/INTERFACE_Fantasy_Warrior_HUD/Source_Sprites/Sprites",
)
OUT = os.path.join(ROOT, "agentic_orchestration/galadriel/captures/2026-07-28-l8-holy-glyph")
CAND = os.path.join(OUT, "candidates")
DARK = (35, 35, 45)

RULED = [
    ("freeze", "Icons_Status/ICON_FantasyWarrior_Status_Cold01_Clean.png"),
    ("physical", "Icons_Status/ICON_FantasyWarrior_Status_Attack01_Clean.png"),
    ("consecrate", "FX/SPR_FX_FantasyWarrior_RitualCircle01.png"),
    ("knockback", "Icons_Status/ICON_FantasyWarrior_Status_Down01_Clean.png"),
    ("shadow", "Icons_Status/ICON_FantasyWarrior_Status_Cursed02_Clean.png"),
    ("air", "Icons_Elements/ICON_FantasyWarrior_Element_Air02_Clean.png"),
]
CANDS = ["H-A_radiant-disc", "H-B_ascendant-halo", "H-C_dawn-rise"]


def font(sz, bold=False):
    p = "/System/Library/Fonts/Supplemental/Arial%s.ttf" % (" Bold" if bold else "")
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.load_default()


def on_dark(rgba, size=None):
    if size:
        rgba = rgba.resize((size, size), Image.LANCZOS)
    bg = Image.new("RGB", rgba.size, DARK)
    bg.paste(rgba, (0, 0), rgba)
    return bg


def dhash(rgba, n=32):
    g = np.asarray(on_dark(rgba, n).convert("L"), dtype=np.int16)
    return (g[:, 1:] > g[:, :-1]).flatten()


def norm_mask(rgba, n=64):
    a = np.array(rgba.getchannel("A"))
    m = a > 96
    ys, xs = np.nonzero(m)
    crop = Image.fromarray((m * 255).astype(np.uint8)).crop(
        (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    )
    return np.array(crop.resize((n, n), Image.LANCZOS)) > 128


def iou(a, b):
    return float((a & b).sum()) / float((a | b).sum())


def main():
    ruled = {k: Image.open(os.path.join(PACK, v)).convert("RGBA") for k, v in RULED}
    cands = {
        c: Image.open(os.path.join(CAND, f"ICON_Holy_{c}_Clean.png")).convert("RGBA")
        for c in CANDS
    }

    print("dHash-32 Hamming distance (of 992 bits; LOWER = more confusable at 32px)")
    hdr = "%-20s" % "" + "".join("%12s" % k for k, _ in RULED)
    print(hdr)
    ham = {}
    for c, im in cands.items():
        hc = dhash(im)
        row = []
        for k, _ in RULED:
            dist = int((hc != dhash(ruled[k])).sum())
            ham[(c, k)] = dist
            row.append(dist)
        print("%-20s" % c + "".join("%12d" % v for v in row))

    print("\nbbox-normalised mask IoU @64 (HIGHER = more confusable silhouette)")
    print(hdr)
    ious = {}
    for c, im in cands.items():
        mc = norm_mask(im)
        row = []
        for k, _ in RULED:
            v = iou(mc, norm_mask(ruled[k]))
            ious[(c, k)] = v
            row.append(v)
        print("%-20s" % c + "".join("%12.3f" % v for v in row))

    print("\nbaseline: pairwise among the ruled five+consecrate (the family's own spread)")
    keys = [k for k, _ in RULED]
    dv, iv = [], []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            dv.append(int((dhash(ruled[keys[i]]) != dhash(ruled[keys[j]])).sum()))
            iv.append(iou(norm_mask(ruled[keys[i]]), norm_mask(ruled[keys[j]])))
    print("  dHash  min %d  median %.0f  max %d" % (min(dv), np.median(dv), max(dv)))
    print("  IoU    min %.3f  median %.3f  max %.3f" % (min(iv), np.median(iv), max(iv)))

    # ---- layer cards + size ladder
    for c in CANDS:
        cell, pad = 220, 14
        card = Image.new("RGB", (3 * cell + 4 * pad, cell + 152), DARK)
        d = ImageDraw.Draw(card)
        d.text((pad, 8), f"ICON_Holy_{c}  —  pack three-layer set", fill=(230, 200, 130),
               font=font(15, True))
        for i, lay in enumerate(["Clean", "Stroke", "Underlay"]):
            im = Image.open(os.path.join(CAND, f"ICON_Holy_{c}_{lay}.png")).convert("RGBA")
            im = im.resize((cell, cell), Image.LANCZOS)
            card.paste(im, (pad + i * (cell + pad), 32), im)
            d.text((pad + i * (cell + pad), 32 + cell + 4), lay, fill=(190, 190, 200),
                   font=font(13))
        x = pad
        # ladder sits on its own row so it cannot overlap the layer labels
        d.text((pad, cell + 58), "size ladder", fill=(120, 150, 185), font=font(12, True))
        for n in (24, 32, 48, 64):
            im = Image.open(os.path.join(CAND, f"ICON_Holy_{c}_Clean.png")).convert("RGBA")
            im = im.resize((n, n), Image.LANCZOS)
            card.paste(im, (x, cell + 120 - n), im)
            d.text((x, cell + 124), f"{n}px", fill=(150, 190, 230), font=font(11))
            x += n + 22
        card.save(os.path.join(OUT, f"layers_{c}.png"))
        print("wrote", os.path.join(OUT, f"layers_{c}.png"))


if __name__ == "__main__":
    main()
