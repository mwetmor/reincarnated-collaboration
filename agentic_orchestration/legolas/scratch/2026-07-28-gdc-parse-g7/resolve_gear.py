#!/usr/bin/env python3
"""SCRATCH — resolve .gdc gear record paths against the Edition-II .arz corpus.

Record paths are the run's identity join key (R-KC1-7). This walks every .arz in
the vendor corpus, resolves each equipped item's base/prefix/suffix record, and
pulls the name tags so the measured gear can be checked against Matt's attested
item names.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")))
from gd_arz_adapter_2026_07_24 import ArzArchive  # noqa: E402

VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724")
ARZS = ["database/database.arz", "gdx1/database/GDX1.arz",
        "gdx2/database/GDX2.arz", "gdx3/database/GDX3.arz"]

NAME_FIELDS = ("itemNameTag", "lootRandomizerName", "description",
               "itemQualityTag", "itemStyleTag", "itemClassification",
               "itemLevel", "levelRequirement", "itemSkillName")


def load():
    arcs = []
    for rel in ARZS:
        p = VENDOR / rel
        if p.exists():
            try:
                arcs.append((rel, ArzArchive(p)))
            except Exception as exc:
                print(f"  !! {rel}: {exc}", file=sys.stderr)
    return arcs


def lookup(arcs, path):
    if not path:
        return None
    for rel, a in arcs:
        try:
            rec = a.read_record(path)
        except Exception:
            continue
        if rec:
            out = {"_source": rel}
            for f in NAME_FIELDS:
                if f in rec:
                    out[f] = rec[f]
            return out
    return None


if __name__ == "__main__":
    parsed = json.load(open(sys.argv[1]))
    arcs = load()
    print(f"loaded {len(arcs)} archives: {[r for r, _ in arcs]}\n")
    inv = parsed["blocks"]["inventory"]
    groups = [("equipment", inv["equipment"]),
              ("weapon1", inv["weapon1"]), ("weapon2", inv["weapon2"])]
    result = []
    for gname, items in groups:
        for it in items:
            if not it["baseName"] or not it.get("attached"):
                continue
            row = {"group": gname, "slot": it["_slot"], "offset": it["_offset"],
                   "seed": it["seed"]}
            for role in ("baseName", "prefixName", "suffixName",
                         "componentName", "augmentName"):
                row[role] = {"record": it[role], "resolved": lookup(arcs, it[role])}
            result.append(row)
    json.dump(result, open(sys.argv[2], "w"), indent=1)
    for row in result:
        print(f"--- {row['group']}[{row['slot']}] @ {row['offset']} seed={row['seed']}")
        for role in ("prefixName", "baseName", "suffixName",
                     "componentName", "augmentName"):
            r = row[role]
            if not r["record"]:
                continue
            res = r["resolved"] or {}
            tag = res.get("itemNameTag") or res.get("lootRandomizerName") or "??"
            print(f"    {role:<13} {r['record']}")
            print(f"    {'':13} tag={tag}  src={res.get('_source', 'NOT FOUND')}  "
                  f"lvl={res.get('itemLevel')} req={res.get('levelRequirement')} "
                  f"class={res.get('itemClassification')}")
