#!/usr/bin/env python3
"""Turn a player-HP frame trace into a damage-event timeline.

THE FAILURE MODE THIS GUARDS. The per-frame OCR fails in exactly one direction:
adjacent glyph strokes touch at the mask threshold and two glyphs segment as one,
so the read LOSES a digit (`11418/15939` -> `1140/15939`). It never gains one --
single-column specular runs are filtered upstream. Both guards below are therefore
one-sided, and neither can invent a damage event out of a clean frame.

  G1  `max` must equal the modal max of its own +/-150-frame window. In this
      substrate max is piecewise constant (health-reduction debuffs step it), so a
      one-frame disagreement is an OCR fault, not a game event. Genuine steps are
      recovered because they are sustained and become the window mode themselves.
  G2  the digit-count of `cur` must not be a strict minority (<25%) of its own
      +/-15-frame window. A merge shortens `cur`; a real 10000->9999 crossing is
      sustained and so is never a minority.

Event definition (falsifiable, stated):
  DAMAGE  cur[k] < cur[k-1] on consecutive SURVIVING frames with equal max.
          Magnitude = cur[k-1]-cur[k]. Simultaneous hits inside one frame are
          indistinguishable and count as ONE event: a FLOOR on hit count, never
          a ceiling.
  HEAL    cur[k] > cur[k-1]. Warlord regen + ADCtH leech + potions are not
          separated here; they are reported, not interpreted.
  MAXSHIFT max[k] != max[k-1]. A drop is a health-reduction debuff landing; a
          rise is it expiring or being cleansed.

  events <trace.json> <out.json> [t_offset]
"""
import sys, json
from collections import Counter
import numpy as np

MAXWIN = 150      # frames each side for the max-mode guard
DIGWIN = 15       # frames each side for the digit-count guard
DIGMIN = 0.25     # minority threshold


def clean(rows):
    idx = [i for i, r in enumerate(rows) if r["cur"] is not None and r["max"] is not None
           and r["cur"] <= r["max"]]
    if not idx:
        return []
    mx = np.array([rows[i]["max"] for i in idx])
    nd = np.array([len(str(rows[i]["cur"])) for i in idx])
    keep = []
    n = len(idx)
    for k in range(n):
        lo, hi = max(0, k - MAXWIN), min(n, k + MAXWIN + 1)
        if mx[k] != Counter(mx[lo:hi].tolist()).most_common(1)[0][0]:
            continue
        lo, hi = max(0, k - DIGWIN), min(n, k + DIGWIN + 1)
        w = nd[lo:hi]
        if (w == nd[k]).sum() / len(w) < DIGMIN:
            continue
        keep.append(idx[k])
    return keep


def events(path, out, off=0.0):
    d = json.load(open(path))
    rows = d["rows"]
    keep = clean(rows)
    kept = [(rows[i]["t"] + off, rows[i]["cur"], rows[i]["max"]) for i in keep]
    dmg, heal, mxs = [], [], []
    for i in range(1, len(kept)):
        t0, c0, m0 = kept[i - 1]
        t1, c1, m1 = kept[i]
        gap = round((t1 - t0) * 60)
        if m1 != m0:
            mxs.append({"t": round(t1, 5), "from": m0, "to": m1})
            continue
        if gap > 6:                       # a hole: do not attribute a step across it
            continue
        if c1 < c0:
            dmg.append({"t": round(t1, 5), "amount": c0 - c1, "hp_after": c1,
                        "frac": round((c0 - c1) / m1, 5), "gap_f": gap})
        elif c1 > c0:
            heal.append({"t": round(t1, 5), "amount": c1 - c0, "gap_f": gap})
    json.dump({"source": path, "offset": off, "n_frames": len(rows),
               "n_kept": len(kept), "damage": dmg, "heal": heal, "maxshift": mxs},
              open(out, "w"))
    print(f"{path}: kept {len(kept)}/{len(rows)}; "
          f"{len(dmg)} damage, {len(heal)} heal, {len(mxs)} max-shift")
    if dmg:
        a = np.array([e["amount"] for e in dmg])
        print(f"  damage: n={len(a)} total={a.sum()} median={np.median(a):.0f} "
              f"p90={np.percentile(a,90):.0f} max={a.max()}")
    for m in mxs:
        print(f"  MAXSHIFT t={m['t']:.3f}  {m['from']} -> {m['to']}")


if __name__ == "__main__":
    events(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.0)
