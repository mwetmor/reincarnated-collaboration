#!/usr/bin/env python3
"""dbr_probe.py — READ-ONLY cooldown / nature cross-check for the decoded hot bar.

Reads the banked Grim Dawn depot .arz corpus via the established adapter
(research/scripts/gd_arz_adapter_2026_07_24.py). Nothing is written.
"""
import functools
import pathlib
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/"
                   "agentic_orchestration/research/scripts")
from gd_arz_adapter_2026_07_24 import ArzArchive  # noqa: E402

EDITIONS = {
    "II-20260724": pathlib.Path(
        "/Users/admin/Games/vendor/grim-dawn-edition-II-20260724"),
    "III-20260808": pathlib.Path(
        "/Users/admin/Games/vendor/grim-dawn-edition-III-20260808"),
}
SUB = ["database/database.arz", "gdx1/database/GDX1.arz",
       "gdx2/database/GDX2.arz", "gdx3/database/GDX3.arz",
       "mods/survivalmode/database/SurvivalMode.arz",
       "survivalmode1/database/SurvivalMode1.arz",
       "survivalmode2/database/SurvivalMode2.arz",
       "survivalmode3/database/SurvivalMode3.arz"]


@functools.lru_cache(maxsize=4)
def stack(edition):
    root = EDITIONS[edition]
    out = []
    for s in SUB:
        p = root / s
        if p.exists():
            out.append((s, ArzArchive(p)))
    return out


def merged(path, edition="II-20260724"):
    """Overlay-merge a record across the archive stack (later wins)."""
    key = path.lower().replace("\\", "/")
    fields, srcs = {}, []
    for name, a in stack(edition):
        recs = {r.lower(): r for r in a.records}
        if key in recs:
            srcs.append(name)
            fields.update(a.read_record(recs[key]))
    return fields, srcs


def find(edition, *needles):
    hits = []
    for name, a in stack(edition):
        for r in a.records:
            rl = r.lower()
            if all(n.lower() in rl for n in needles):
                hits.append((name, r))
    return hits
