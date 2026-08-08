#!/usr/bin/env python3
"""D2 — display-tag join: name -> tag -> record. READ-ONLY. Cites which tree each read used."""
import sys, pathlib
sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from gd_arc_reader_2026_07_26 import ArcArchive, parse_tag_file

ROOTS = {"II": pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-II-20260724"),
         "III": pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")}

def load_tags(tree):
    root = ROOTS[tree]; out = {}; arcs = sorted(root.rglob("Text_EN.arc"))
    for ap in arcs:
        try: a = ArcArchive(ap)
        except Exception as e:
            print(f"  !! open {ap}: {e}"); continue
        for name in a.names():
            if not name.lower().endswith(".txt"): continue
            try: payload = a.read_file(name)
            except Exception: continue
            for k, v in parse_tag_file(payload):
                out[k] = (v, str(ap.relative_to(root)), name)
    return out, len(arcs)

TARGETS = ["Ugdenbog Crabling", "Rotmouth", "Aregos", "Vanallius", "Chaosshell",
           "Mudflinger", "Chillslither", "Stonegaze Basilisk", "Crabling"]

TAGS = {}
for TREE in ("II", "III"):
    tags, n = load_tags(TREE)
    TAGS[TREE] = tags
    print(f"\n########## TREE {TREE}  ({n} Text_EN.arc)  tags={len(tags)} ##########")
    for t in TARGETS:
        hits = sorted((k, v) for k, v in tags.items() if t.lower() in v[0].lower())
        print(f"  --- '{t}' : {len(hits)} hit(s)")
        for k, (v, arc, txt) in hits:
            print(f"        {k} = {v!r}   [{arc} :: {txt}]")
import json
json.dump({t: {k: list(v) for k, v in TAGS[t].items()} for t in TAGS}, open("tags_all.json","w"))
print("\nwrote tags_all.json")
