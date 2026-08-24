#!/usr/bin/env python3
"""D-3 STEP 8 — EMIT.  Per-controller parameter table for the rolled tier-16 roster, plus the
group-level roll-ups the findings note quotes.  READ-ONLY on substrate; writes only to the lap dir."""
from __future__ import annotations
import collections, csv, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import d3_lib as L
from d3_consumers import SLOTS
OUT = pathlib.Path(__file__).resolve().parent
NOTES = L.OUT

GROUPS = {r["name"]: r["group"] for r in L.template_surface()}
D3 = ["SkillUsage", "Attacking", "Dodging", "Fleeing", "PetBehaviour", "Roaming",
      "Patrolling", "Emote", "Sleep", "Loot", "Dying", "RandomAnger"]
HIDDEN = {"LeaderBehavior": "Leader (HIDDEN — not in .tpl)",
          "LeaderDistance": "Leader (HIDDEN — not in .tpl)",
          "MaxFollowers": "Leader (HIDDEN — not in .tpl)"}


def norm(v):
    if isinstance(v, list):
        return ";".join(str(x) for x in v) if v else "__EMPTY__"
    return "__ABSENT__" if v is None else str(v)


def main():
    C = L.ARZ.Corpus()
    BASE = [a for a in L.ARZ.ARCHIVE_ORDER if "urvival" not in a[0]]
    Cb = L.ARZ.Corpus(order=BASE)

    rolled = L.roster("in_rolled_20w")
    mp, _ = L.controller_join(C, rolled)
    per_ctrl_monsters = collections.Counter(mp.values())

    ts = L.template_surface()
    fields = [r["name"] for r in ts] + list(HIDDEN)

    rows = []
    for ctrl in sorted(per_ctrl_monsters):
        r = C.read(ctrl)
        rb = Cb.read(ctrl) if Cb.has(ctrl) else {}
        for f in fields:
            g = GROUPS.get(f) or HIDDEN.get(f)
            if g not in D3 and f not in HIDDEN:
                continue
            rows.append(dict(controller=ctrl, n_monsters=per_ctrl_monsters[ctrl],
                             group=g, field=f,
                             crucible_value=norm(r.get(f)),
                             base_game_value=norm(rb.get(f)) if rb else "__NO-BASE-RECORD__",
                             owner_archive=C.owner(ctrl),
                             slot=hex(SLOTS[f]) if f in SLOTS else ""))
    with open(NOTES / "d3_roster_controller_params.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # monster-weighted value histogram per field
    agg = collections.defaultdict(collections.Counter)
    for ctrl, n in per_ctrl_monsters.items():
        r = C.read(ctrl)
        for f in fields:
            g = GROUPS.get(f) or HIDDEN.get(f)
            if g not in D3 and f not in HIDDEN:
                continue
            agg[f][norm(r.get(f))] += n
    out = {f: dict(group=GROUPS.get(f) or HIDDEN.get(f),
                   slot=hex(SLOTS[f]) if f in SLOTS else None,
                   monster_weighted=dict(c.most_common()))
           for f, c in agg.items()}
    json.dump(dict(n_monster_records=len(rolled), n_controllers=len(per_ctrl_monsters),
                   fields=out), open(NOTES / "d3_group_rollup.json", "w"), indent=2)

    print(f"{len(rolled)} monster records -> {len(per_ctrl_monsters)} controllers")
    for f, c in sorted(agg.items(), key=lambda x: (GROUPS.get(x[0]) or HIDDEN.get(x[0]), x[0])):
        print(f"  [{GROUPS.get(f) or HIDDEN.get(f):12s}] {f:30s} {list(c.most_common(5))}")


if __name__ == "__main__":
    main()
