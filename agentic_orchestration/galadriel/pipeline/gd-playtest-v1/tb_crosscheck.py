#!/usr/bin/env python3
"""T-B step 4 -- independent cross-check of the globe delta machinery.

The globe reader and the panel `life_healed` counter are two instruments with
no shared failure mode: one is a 15 fps template match on the health-globe
numerals, the other a 2 fps OCR of a different UI region on a different
monotonic series. Positive globe deltas (healing received) must therefore
track `life_healed` increments over the same windows.

They cannot be EQUAL, and the inequality has a known direction:
  globe_heal <= life_healed_delta
because the globe clips at max HP -- overheal is counted by the panel and
invisible to the globe -- and because refused frames drop real heals.
A violation in the other direction would mean the globe is inventing healing.
"""
import csv
import json
import sys


def main():
    W = json.load(open(sys.argv[1]))["windows"]
    rows = list(csv.DictReader(open(sys.argv[2])))
    S = [(float(r["pts_s"]),
          float(r["life_healed"]) if r["life_healed"] not in ("", "None")
          else None) for r in rows]
    out, viol = [], 0
    for w in W:
        seg = [(t, v) for t, v in S
               if w["pts_start"] - 0.5 <= t <= w["pts_end"] + 0.5]
        have = [v for _, v in seg if v is not None]
        if len(have) < 2 or not seg:
            continue
        cov = len(have) / len(seg)
        panel = have[-1] - have[0]
        globe = w["healed_hp"]
        rec = dict(eng=w["eng_id"], regime=w["regime"],
                   globe_cov=w["coverage"], panel_cov=round(cov, 3),
                   globe_heal=globe, panel_heal=round(panel, 2),
                   ratio=round(globe / panel, 3) if panel > 0 else None)
        if panel > 0 and globe > panel * 1.05:
            rec["VIOLATION"] = "globe heal exceeds panel life_healed"
            viol += 1
        out.append(rec)
    usable = [r for r in out if r["ratio"] is not None
              and r["globe_cov"] >= 0.9 and r["panel_cov"] >= 0.9]
    print("windows compared      : %d" % len(out))
    print("usable (both cov>=0.9): %d" % len(usable))
    print("direction violations  : %d  (globe > panel by >5%%)" % viol)
    for R in ("R1", "R2", "R3"):
        u = [r for r in usable if r["regime"] == R]
        if not u:
            print("  %s: none usable" % R)
            continue
        g = sum(r["globe_heal"] for r in u)
        p = sum(r["panel_heal"] for r in u)
        print("  %s: n=%2d  globe=%8.0f  panel=%8.0f  globe/panel=%.3f"
              % (R, len(u), g, p, g / p if p else float("nan")))
    json.dump(out, open(sys.argv[3], "w"), indent=1)


if __name__ == "__main__":
    main()
