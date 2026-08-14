#!/usr/bin/env python3
"""
pm4t_beacon_2026_08_14.py — RUN KC2-PM4 LAP T, INSTRUMENT I-T1  (v2, after defect D-T-1).

LIMB (a): UNREACHED-S2 — THE BEACON MAGNITUDE.

DEFECT D-T-1 (self-caught, v1 -> v2)
    v1 walked EVERY `.dbr`-valued field breadth-first. `records/controllers/factions/
    faction_aetherial.dbr` is a PEER-LISTING (it names other faction members), not a mechanical
    chain, and expanding it reached 6,044 records -- the whole aetherial creature graph and its
    gear. The movement-term search then "found" `characterRunSpeed` on nemesis monsters that have
    nothing to do with the beacon's buff, which would have made the load-bearing NEGATIVE
    meaningless. v2 expands only through an EXPLICIT ALLOW-LIST of fields that mean
    "this record's own behaviour includes that record", records the faction/anim references as
    LEAVES (content captured, not expanded), and resolves `.tpl` templates from `templates.arc`.

GATE G2: the walk must reach a fixed point over the allow-list, or list what it did not reach.

Emits:
    pm4t_beacon_chain.csv     one row per (record, field) over the mechanical chain
    pm4t_beacon_summary.json  the modifier surface + the movement-term search result

READ-ONLY on the vendor tree.
"""
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pm4t_arz_2026_08_14 as M
import gd_arc_reader_2026_07_26 as ARC

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-14-kc2-pm4-lap-t-arrival-decode")
TEMPLATES_ARC = pathlib.Path(
    "/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/database/templates.arc")

ROOT = "records/creatures/traps/spawnbeacon.dbr"

# Fields whose value is a record this record's OWN BEHAVIOUR runs through.
# Everything else is captured as a leaf. This list is the instrument's decode claim and is
# reported with the finding so it can be argued with.
EXPAND_FIELDS = {
    "initialskillname", "buffskillname", "controller", "petskillname",
    "skillname1", "skillname2", "skillname3", "skillname4", "skillname5",
    "skillname6", "skillname7", "skillname8", "skillname9", "skillname10",
    "skillname11", "skillname12", "skillname13", "skillname14", "skillname15",
    "skillname16", "skillname17",
    "spawnobjects", "petbonusname", "modifierskillname", "skillsecondaryname",
    "attackskillname", "auraskillname", "passiveskillname",
}
# Explicitly NOT expanded, and why. Captured as leaves.
LEAF_FIELDS_DECLARED = {
    "factions": "peer-listing of faction members; not a mechanic this record runs",
    "charanimationtablename": "animation table; art asset, not a mechanic",
}

# Movement-term patterns. Deliberately over-broad: a negative is only worth stating if the
# search that produced it could not plausibly have missed the term.
MOVEMENT_PATTERNS = [
    "runspeed", "movespeed", "movementspeed", "walkspeed", "speedmodifier",
    "pathmass", "pathingsize", "rotationspeed", "avoidforce", "charge",
    "leap", "teleport", "blink", "sprint", "haste", "slow", "velocity",
    "accel", "locomot", "stride", "gait",
]


def is_neutral(v):
    vals = v if isinstance(v, list) else [v]
    return all((isinstance(x, (int, float)) and x in (0, 0.0)) or x in ("", None, False)
               for x in vals)


def walk_mechanical(corpus, root, max_depth=10):
    seen = {}
    leaves = {}
    frontier = [(root.lower(), 0, None, None)]
    while frontier:
        path, depth, parent, via = frontier.pop(0)
        path = path.replace("\\", "/")
        if path in seen:
            seen[path]["parents"].append((parent, via))
            continue
        if not corpus.has(path):
            seen[path] = {"depth": depth, "owner": None, "type": None, "fields": None,
                          "parents": [(parent, via)], "missing": True}
            continue
        fields = corpus.read(path)
        seen[path] = {"depth": depth, "owner": corpus.owner(path),
                      "type": corpus.record_type(path), "fields": fields,
                      "parents": [(parent, via)], "missing": False}
        if depth >= max_depth:
            continue
        for k, v in fields.items():
            vals = v if isinstance(v, list) else [v]
            for x in vals:
                if not (isinstance(x, str) and x.lower().endswith(".dbr")):
                    continue
                if k.lower() in EXPAND_FIELDS:
                    frontier.append((x.lower(), depth + 1, path, k))
                else:
                    leaves.setdefault(x.lower(), []).append((path, k))
    return seen, leaves


def main():
    corpus = M.Corpus()
    chain, leaves = walk_mechanical(corpus, ROOT)
    reached = {k: v for k, v in chain.items() if not v.get("missing")}
    missing = {k: v for k, v in chain.items() if v.get("missing")}

    # ---- templates for every reached record, from templates.arc
    tpl_arc = ARC.ArcArchive(TEMPLATES_ARC)
    tpl_names = {n.lower(): n for n in tpl_arc.names()}
    templates = {}
    for path, info in reached.items():
        tn = (info["fields"] or {}).get("templateName")
        if not tn:
            continue
        base = tn.split("/")[-1].lower()
        if base in tpl_names and base not in templates:
            body = tpl_arc.read_file(tpl_names[base]).decode("latin-1", "replace")
            templates[base] = body

    # ---- G2 fixed point over the allow-list
    unexplored = []
    for path, info in reached.items():
        if info["depth"] >= 10:
            for k, v in (info["fields"] or {}).items():
                if k.lower() in EXPAND_FIELDS:
                    unexplored.append((path, k, v))

    # ---- rows
    rows = []
    for path in sorted(reached):
        info = reached[path]
        for k in sorted(info["fields"]):
            v = info["fields"][k]
            rows.append({
                "record": path, "archive": info["owner"],
                "override_layers": ";".join(corpus.layers(path)),
                "class": info["type"], "depth": info["depth"],
                "reached_via": ";".join(f"{p}::{f}" for p, f in info["parents"] if p),
                "field": k,
                "value": json.dumps(v) if isinstance(v, list) else v,
            })
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "pm4t_beacon_chain.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # ---- MOVEMENT-TERM SEARCH over the mechanical chain
    movement_hits = []
    for path in sorted(reached):
        info = reached[path]
        for k, v in (info["fields"] or {}).items():
            if any(p in k.lower() for p in MOVEMENT_PATTERNS):
                movement_hits.append({"record": path, "class": info["type"], "field": k,
                                      "value": v, "neutral": is_neutral(v),
                                      "depth": info["depth"]})
    # ---- and over the TEMPLATE variable declarations (a term could be template-defaulted)
    tpl_movement = {}
    for base, body in templates.items():
        hits = [ln.strip() for ln in body.splitlines()
                if any(p in ln.lower() for p in MOVEMENT_PATTERNS)]
        if hits:
            tpl_movement[base] = hits

    modifiers = []
    for path in sorted(reached):
        info = reached[path]
        for k, v in (info["fields"] or {}).items():
            if k.endswith("Modifier") and not is_neutral(v):
                modifiers.append({"record": path, "class": info["type"], "field": k, "value": v})

    gate_pats = ["cooldown", "duration", "energycost", "activeduration",
                 "lifecost", "maxpettime", "lifetime", "expiretime", "chargelevel"]
    gates = []
    for path in sorted(reached):
        info = reached[path]
        for k, v in (info["fields"] or {}).items():
            if any(p in k.lower() for p in gate_pats) and not is_neutral(v):
                gates.append({"record": path, "class": info["type"], "field": k, "value": v})

    radius = []
    for path in sorted(reached):
        info = reached[path]
        for k, v in (info["fields"] or {}).items():
            if "radius" in k.lower() and not is_neutral(v):
                radius.append({"record": path, "class": info["type"], "field": k, "value": v})

    summary = {
        "instrument": "I-T1 v2 (after D-T-1)",
        "root": ROOT,
        "expand_fields": sorted(EXPAND_FIELDS),
        "declared_leaf_fields": LEAF_FIELDS_DECLARED,
        "records_reached": len(reached),
        "records_missing": sorted(missing),
        "leaf_references_not_expanded": {k: v for k, v in sorted(leaves.items())},
        "fixed_point": len(unexplored) == 0,
        "unexplored_refs": unexplored,
        "chain": [{"record": p, "class": reached[p]["type"], "archive": reached[p]["owner"],
                   "depth": reached[p]["depth"], "layers": corpus.layers(p),
                   "n_fields": len(reached[p]["fields"]),
                   "via": [f"{a}::{b}" for a, b in reached[p]["parents"] if a]}
                  for p in sorted(reached, key=lambda x: (reached[x]["depth"], x))],
        "templates_resolved": sorted(templates),
        "MOVEMENT_TERM_SEARCH": {
            "patterns": MOVEMENT_PATTERNS,
            "scope_records": len(reached),
            "hits": movement_hits,
            "non_neutral_hits": [h for h in movement_hits if not h["neutral"]],
            "template_hits": tpl_movement,
        },
        "active_modifiers": modifiers,
        "uptime_gates": gates,
        "radius_fields": radius,
        "archive_digests": corpus.digests,
    }
    with open(OUT / "pm4t_beacon_summary.json", "w") as fh:
        json.dump(summary, fh, indent=2, default=str)

    print(f"MECHANICAL CHAIN: {len(reached)} records reached, {len(missing)} missing, "
          f"fixed_point={len(unexplored) == 0}")
    print("\n--- CHAIN")
    for s in summary["chain"]:
        print(f"  d{s['depth']}  {s['record']}")
        print(f"        class={s['class']}  archive={s['archive']}  layers={s['layers']}  "
              f"fields={s['n_fields']}")
        for v in s["via"]:
            print(f"        via {v}")
    print("\n--- LEAF REFERENCES (captured, deliberately NOT expanded)")
    for k, v in summary["leaf_references_not_expanded"].items():
        print(f"    {k}   <- {v}")
    print("\n--- MOVEMENT-TERM SEARCH  (scope = the mechanical chain only)")
    print(f"    patterns {len(MOVEMENT_PATTERNS)} | records {len(reached)} | "
          f"hits {len(movement_hits)} | NON-NEUTRAL {len(summary['MOVEMENT_TERM_SEARCH']['non_neutral_hits'])}")
    for h in movement_hits:
        print(f"      {'NON-NEUTRAL' if not h['neutral'] else 'neutral    '} d{h['depth']}  "
              f"{h['record']} :: {h['field']} = {h['value']!r}")
    print("\n    template-side movement declarations:")
    for base, hits in tpl_movement.items():
        print(f"      {base}: {hits}")
    if not tpl_movement:
        print("      (none)")
    print("\n--- ACTIVE MODIFIERS (what the beacon actually does)")
    for m in modifiers:
        print(f"      {m['record']} [{m['class']}] :: {m['field']} = {m['value']!r}")
    print("\n--- UPTIME GATES")
    for g in gates:
        print(f"      {g['record']} :: {g['field']} = {g['value']!r}")
    if not gates:
        print("      (none)")
    print("\n--- RADIUS FIELDS")
    for r in radius:
        print(f"      {r['record']} :: {r['field']} = {r['value']!r}")


if __name__ == "__main__":
    main()
