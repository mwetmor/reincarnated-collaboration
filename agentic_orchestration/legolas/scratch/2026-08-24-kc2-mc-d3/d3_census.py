#!/usr/bin/env python3
"""D-3 STEP 1 — the RECORD census.  READ-ONLY."""
from __future__ import annotations
import collections, csv, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import d3_lib as L

OUT = pathlib.Path(__file__).resolve().parent


def main():
    ts = L.template_surface()
    fields = [r["name"] for r in ts]
    C = L.ARZ.Corpus()
    print(f"corpus: {len(C.paths())} winning records", file=sys.stderr)

    rolled = L.roster("in_rolled_20w")
    pool = L.roster("in_pool")
    print(f"roster in_rolled_20w={len(rolled)}  in_pool={len(pool)}", file=sys.stderr)

    mp_r, bad_r = L.controller_join(C, rolled)
    mp_p, bad_p = L.controller_join(C, pool)
    ctrl_r = sorted(set(mp_r.values()))
    ctrl_p = sorted(set(mp_p.values()))
    print(f"distinct controllers: rolled={len(ctrl_r)} pool={len(ctrl_p)}", file=sys.stderr)
    print(f"unresolved: rolled={len(bad_r)} pool={len(bad_p)}", file=sys.stderr)

    allcm = L.all_controllermonster_records(C)
    print(f"corpus ControllerMonster records: {len(allcm)}", file=sys.stderr)

    pops = {
        "rolled_20w_controllers": ctrl_r,
        "pool_controllers": ctrl_p,
        "corpus_all_ControllerMonster": allcm,
    }
    res = {}
    for tag, recs in pops.items():
        cen, cls = L.census(C, recs, fields)
        res[tag] = dict(n=len(recs), classes=dict(cls.most_common()),
                        fields={f: dict(sorted(c.items(), key=lambda x: -x[1]))
                                for f, c in cen.items()})

    # which archive layer OWNS each rolled controller (Crucible override evidence)
    owners = collections.Counter()
    per_owner_fields = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for c in ctrl_r:
        o = C.owner(c)
        owners[o] += 1
        r = C.read(c)
        for f in fields:
            v = r.get(f, "__ABSENT__")
            if isinstance(v, list):
                v = ";".join(str(x) for x in v) if v else "__EMPTY__"
            per_owner_fields[o][f][str(v)] += 1

    res["rolled_controller_owner_archives"] = dict(owners.most_common())
    res["rolled_controller_records"] = ctrl_r
    res["unresolved_rolled"] = bad_r
    res["template"] = ts

    with open(OUT / "d3_census.json", "w") as fh:
        json.dump(res, fh, indent=2)

    # human-readable dump
    with open(OUT / "d3_census.txt", "w") as fh:
        for r in ts:
            f = r["name"]
            fh.write(f"\n=== [{r['group']}] {f}  ({r['vtype']}, {r['vclass']}) "
                     f"default={r['default']!r}  desc={r['description']!r}\n")
            for tag in pops:
                c = res[tag]["fields"][f]
                top = list(c.items())[:6]
                fh.write(f"    {tag:32s} n={res[tag]['n']:5d}  {top}\n")
    print("wrote d3_census.json / d3_census.txt", file=sys.stderr)


if __name__ == "__main__":
    main()
