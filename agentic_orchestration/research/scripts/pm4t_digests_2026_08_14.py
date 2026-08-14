#!/usr/bin/env python3
"""pm4t_digests_2026_08_14.py — RUN KC2-PM4 LAP T. FULL 64-hex sha256 on every input and output (GL-6)."""
import hashlib
import json
import pathlib

OUT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                   "legolas/notes/2026-08-14-kc2-pm4-lap-t-arrival-decode")
SCRIPTS = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
LAPS = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes")
VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
GD = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    d = {"inputs": {}, "instruments": {}, "outputs": {}}
    for rel in ["database/database.arz", "gdx1/database/GDX1.arz", "gdx2/database/GDX2.arz",
                "gdx3/database/GDX3.arz", "mods/survivalmode/database/SurvivalMode.arz",
                "survivalmode1/database/SurvivalMode1.arz",
                "survivalmode2/database/SurvivalMode2.arz",
                "survivalmode3/database/SurvivalMode3.arz",
                "database/templates.arc",
                "mods/survivalmode/resources/Scripts.arc",
                "survivalmode1/resources/Scripts.arc",
                "survivalmode3/resources/Scripts.arc",
                "survivalmode1/resources/Maps.arc", "survivalmode2/resources/Maps.arc",
                "survivalmode3/resources/Maps.arc"]:
        p = VENDOR / rel
        if p.exists():
            d["inputs"][f"corpus:{rel}"] = sha256(p)
    for n in ["Game.dll", "Engine.dll", "Grim Dawn.exe"]:
        if (GD / n).exists():
            d["inputs"][f"binary:{n}"] = sha256(GD / n)
    for rel in ["2026-08-14-kc2-pm4-lap-s-arena-advance/pm4s_arena_placements.csv",
                "2026-08-14-kc2-pm4-lap-s-arena-advance/pm4s_findings.md",
                "2026-08-14-kc2-pm4-lap-r-locomotion-contact/pm4r_speed_terms.csv",
                "2026-08-14-kc2-pm4-lap-p-sustain-engine/pm4p_leech_resistance.csv"]:
        p = LAPS / rel
        if p.exists():
            d["inputs"][f"lap:{rel}"] = sha256(p)
    for n in sorted(SCRIPTS.glob("pm4t_*.py")):
        d["instruments"][n.name] = sha256(n)
    for n in sorted(OUT.rglob("*")):
        if n.is_file():
            d["outputs"][str(n.relative_to(OUT))] = sha256(n)
    with open(OUT / "pm4t_digests.json", "w") as fh:
        json.dump(d, fh, indent=2, sort_keys=True)
    for k in ("inputs", "instruments", "outputs"):
        print(f"--- {k} ({len(d[k])})")
        for a, b in sorted(d[k].items()):
            print(f"  {b}  {a}")


if __name__ == "__main__":
    main()
