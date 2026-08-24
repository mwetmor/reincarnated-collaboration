#!/usr/bin/env python3
"""D-3 STEP 2 — THE CRUCIBLE-OVERRIDE DIFF.

For each of the 77 rolled controllers: read the BASE-GAME winner (database/GDX1-3 layers only)
and the FULL-STACK winner (base + the four SurvivalMode layers), and diff every field.
This generalises the ViewDistance 15.0 -> 80.0 precedent to the whole ControllerMonster surface.
READ-ONLY.
"""
from __future__ import annotations
import collections, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import d3_lib as L
ARZ = L.ARZ
OUT = pathlib.Path(__file__).resolve().parent

BASE_ORDER = [a for a in ARZ.ARCHIVE_ORDER if "urvival" not in a[0]]


def norm(v):
    if isinstance(v, list):
        return ";".join(str(x) for x in v) if v else "__EMPTY__"
    return "__ABSENT__" if v is None else str(v)


def main():
    full = ARZ.Corpus()
    base = ARZ.Corpus(order=BASE_ORDER)
    cen = json.load(open(OUT / "d3_census.json"))
    ctrls = cen["rolled_controller_records"]
    fields = [r["name"] for r in cen["template"]]

    rows = []
    diffs = collections.defaultdict(collections.Counter)
    present_in_base = 0
    for c in ctrls:
        fr = full.read(c)
        br = base.read(c) if base.has(c) else None
        if br is not None:
            present_in_base += 1
        for f in fields:
            fv = norm(fr.get(f))
            bv = norm(br.get(f)) if br is not None else "__NO-BASE-RECORD__"
            if fv != bv:
                diffs[f][f"{bv} -> {fv}"] += 1
            rows.append(dict(controller=c, field=f, base=bv, crucible=fv,
                             changed=int(fv != bv)))

    summary = {}
    for f in fields:
        n_changed = sum(diffs[f].values())
        summary[f] = dict(n_changed=n_changed, n_total=len(ctrls),
                          transitions=dict(diffs[f].most_common(8)))

    json.dump(dict(base_archives=[a[0] for a in BASE_ORDER],
                   n_controllers=len(ctrls),
                   n_present_in_base=present_in_base,
                   per_field=summary), open(OUT / "d3_override.json", "w"), indent=2)

    import csv as _csv
    with open(OUT / "d3_override_rows.csv", "w", newline="") as fh:
        w = _csv.DictWriter(fh, fieldnames=["controller", "field", "base", "crucible", "changed"])
        w.writeheader()
        w.writerows(rows)

    print(f"base archives: {[a[0] for a in BASE_ORDER]}")
    print(f"77 rolled controllers; present in base-game layers: {present_in_base}")
    print("\nFIELD                             changed/77   transitions")
    for f in fields:
        s = summary[f]
        if s["n_changed"]:
            print(f"  {f:34s} {s['n_changed']:3d}/{len(ctrls)}   {list(s['transitions'].items())[:4]}")
    print("\nUNCHANGED BY THE CRUCIBLE LAYER:")
    for f in fields:
        if not summary[f]["n_changed"]:
            print(f"  {f}")


if __name__ == "__main__":
    main()
