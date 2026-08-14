#!/usr/bin/env python3
"""pm4u_digests_2026_08_14.py — RUN KC2-PM4 LAP U.  GL-6: full 64-hex on everything.

Every INPUT consumed, every INSTRUMENT run, every ARTIFACT emitted.  The PREREGISTRATION digest is
RECOMPUTED here, not quoted, so the conductor's CL-10 check is a re-run rather than a reading.
READ-ONLY.  Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
NOTES = META / "agentic_orchestration" / "legolas" / "notes"
OUT = NOTES / "2026-08-14-kc2-pm4-lap-u-ramp-decode"
SCRIPTS = META / "agentic_orchestration" / "research" / "scripts"
VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
GD = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")

PREREG_EXPECTED = "7a250772bad3bf8cbce2e43455bc3e4dae2fee677aeedc1ffad978f3dda6b144"
PREREG_HASHED_UTC = "2026-08-14T18:03:05Z"


def sha256(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


INPUTS = {
    # carried lap artifacts
    "lap:lapH2/method/camera_translation_60fps_683-866.npy":
        NOTES / "2026-08-13-kc2-pm4-lap-h2-video-match/method/camera_translation_60fps_683-866.npy",
    "lap:lapR/method/plates60_lapH2.npy":
        NOTES / "2026-08-14-kc2-pm4-lap-r-locomotion-contact/method/plates60_lapH2.npy",
    "lap:lapS/pm4s_video.json": NOTES / "2026-08-14-kc2-pm4-lap-s-arena-advance/pm4s_video.json",
    "lap:lapS/pm4s_findings.md": NOTES / "2026-08-14-kc2-pm4-lap-s-arena-advance/pm4s_findings.md",
    "lap:lapT/pm4t_map_placements_v2.csv":
        NOTES / "2026-08-14-kc2-pm4-lap-t-arrival-decode/pm4t_map_placements_v2.csv",
    "lap:lapT/pm4t_geometry_corrected.csv":
        NOTES / "2026-08-14-kc2-pm4-lap-t-arrival-decode/pm4t_geometry_corrected.csv",
    "lap:lapT/pm4t_findings.md":
        NOTES / "2026-08-14-kc2-pm4-lap-t-arrival-decode/pm4t_findings.md",
    "lap:lapT/pm4t_digests.json":
        NOTES / "2026-08-14-kc2-pm4-lap-t-arrival-decode/pm4t_digests.json",
    "lap:lapD/pm4d_band_b_monster_life.csv":
        NOTES / "2026-08-13-kc2-pm4-lap-d-roster-ehp/pm4d_band_b_monster_life.csv",
    # shipped binaries
    "binary:Game.dll": GD / "Game.dll",
    "binary:Engine.dll": GD / "Engine.dll",
    "binary:Grim Dawn.exe": GD / "Grim Dawn.exe",
    # corpus containers
    "corpus:database/database.arz": VENDOR / "database/database.arz",
    "corpus:database/templates.arc": VENDOR / "database/templates.arc",
    "corpus:gdx1/database/GDX1.arz": VENDOR / "gdx1/database/GDX1.arz",
    "corpus:gdx2/database/GDX2.arz": VENDOR / "gdx2/database/GDX2.arz",
    "corpus:gdx3/database/GDX3.arz": VENDOR / "gdx3/database/GDX3.arz",
    "corpus:mods/survivalmode/database/SurvivalMode.arz":
        VENDOR / "mods/survivalmode/database/SurvivalMode.arz",
    "corpus:survivalmode1/database/SurvivalMode1.arz":
        VENDOR / "survivalmode1/database/SurvivalMode1.arz",
    "corpus:survivalmode2/database/SurvivalMode2.arz":
        VENDOR / "survivalmode2/database/SurvivalMode2.arz",
    "corpus:survivalmode3/database/SurvivalMode3.arz":
        VENDOR / "survivalmode3/database/SurvivalMode3.arz",
    "corpus:survivalmode1/resources/Maps.arc": VENDOR / "survivalmode1/resources/Maps.arc",
    "corpus:survivalmode2/resources/Maps.arc": VENDOR / "survivalmode2/resources/Maps.arc",
    "corpus:survivalmode3/resources/Maps.arc": VENDOR / "survivalmode3/resources/Maps.arc",
}

INSTRUMENTS = [
    # this lap's
    "pm4u_video_2026_08_14.py", "pm4u_ramp_2026_08_14.py", "pm4u_mapv3_2026_08_14.py",
    "pm4u_pursue_2026_08_14.py", "pm4u_lvl_2026_08_14.py", "pm4u_digests_2026_08_14.py",
    # reused, unmodified, from earlier laps (NOTE-9: imported, never copied)
    "pm4s_pe_2026_08_14.py", "pm4t_map_v2_2026_08_14.py", "pm4t_arz_2026_08_14.py",
    "gd_arc_reader_2026_07_26.py",
]

OUTPUTS = [
    "PREREGISTRATION.md", "pm4u_findings.md",
    "pm4u_map_placements_v3.csv", "pm4u_map_v3_summary.json",
    "pm4u_geometry_v3.csv",
    "pm4u_arrivals.csv", "pm4u_arrival_stats.json", "pm4u_ramp_analysis.json",
    "pm4u_pursue_decode.json", "pm4u_lvl_regions.json",
]


def main():
    print("=" * 92)
    print("KC2-PM4 LAP U — GL-6 DIGESTS")
    print("=" * 92)
    res = {
        "lap": "KC2-PM4 Lap U — the ramp decode",
        "agent": "legolas (UNKNOWN-RESEARCHER)",
        "date": "2026-08-14",
        "commission": "R-PM4-52 part 5 (ledger L-43)",
        "preregistration_hashed_utc": PREREG_HASHED_UTC,
        "inputs": {}, "instruments": {}, "outputs": {},
    }
    for k, p in sorted(INPUTS.items()):
        if not p.exists():
            res["inputs"][k] = "ABSENT"
            print(f"  ABSENT  {k}")
            continue
        res["inputs"][k] = sha256(p)
        print(f"  {res['inputs'][k]}  IN   {k}")
    print()
    for n in sorted(INSTRUMENTS):
        p = SCRIPTS / n
        res["instruments"][n] = sha256(p) if p.exists() else "ABSENT"
        print(f"  {res['instruments'][n]}  INS  {n}")
    print()
    for n in sorted(OUTPUTS):
        p = OUT / n
        res["outputs"][n] = sha256(p) if p.exists() else "ABSENT"
        print(f"  {res['outputs'][n]}  OUT  {n}")

    got = res["outputs"]["PREREGISTRATION.md"]
    res["preregistration_sha256"] = got
    res["preregistration_recomputed_EXACT"] = (got == PREREG_EXPECTED)
    print(f"\n  ⚑ PREREGISTRATION recomputed: {got}")
    print(f"    expected                    : {PREREG_EXPECTED}")
    print(f"    EXACT: {res['preregistration_recomputed_EXACT']}   (hashed {PREREG_HASHED_UTC}, "
          f"before any instrument of this lap ran)")
    assert res["preregistration_recomputed_EXACT"], "HALT: PREREGISTRATION digest moved"

    with open(OUT / "pm4u_digests.json", "w") as fh:
        json.dump(res, fh, indent=2, sort_keys=True)
    print(f"\n  wrote {OUT/'pm4u_digests.json'}")
    print(f"  {len(res['inputs'])} inputs · {len(res['instruments'])} instruments · "
          f"{len(res['outputs'])} outputs")


if __name__ == "__main__":
    main()
