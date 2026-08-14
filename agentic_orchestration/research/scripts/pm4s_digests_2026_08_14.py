#!/usr/bin/env python3
"""KC2-PM4 Lap S — FULL 64-hex sha256 over every input and every emitted artifact (GL-6).

Digests are recomputed here from the files on disk at landing time, never copied from a run log.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-14.  Run KC2-PM4, Lap S.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

META = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
NOTES = META / "agentic_orchestration" / "legolas" / "notes"
OUT = NOTES / "2026-08-14-kc2-pm4-lap-s-arena-advance"
SCRIPTS = META / "agentic_orchestration" / "research" / "scripts"
VENDOR = pathlib.Path("/Users/admin/Games/vendor/grim-dawn-edition-III-20260808")
GD = pathlib.Path("/Users/admin/Games/vendor/grim-dawn")


def sha256(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    inputs = {
        "lapR/method/plates60_lapH2.npy":
            NOTES / "2026-08-14-kc2-pm4-lap-r-locomotion-contact/method/plates60_lapH2.npy",
        "lapH2/method/camera_translation_60fps_683-866.npy":
            NOTES / "2026-08-13-kc2-pm4-lap-h2-video-match/method/camera_translation_60fps_683-866.npy",
        "vendor/grim-dawn/Game.dll": GD / "Game.dll",
        "vendor/grim-dawn/Engine.dll": GD / "Engine.dll",
        "vendor/grim-dawn/Grim Dawn.exe": GD / "Grim Dawn.exe",
        "vendor/database/templates.arc": VENDOR / "database/templates.arc",
        "vendor/survivalmode1/resources/Maps.arc": VENDOR / "survivalmode1/resources/Maps.arc",
        "vendor/survivalmode2/resources/Maps.arc": VENDOR / "survivalmode2/resources/Maps.arc",
        "vendor/survivalmode3/resources/Maps.arc": VENDOR / "survivalmode3/resources/Maps.arc",
        "vendor/survivalmode1/resources/Scripts.arc": VENDOR / "survivalmode1/resources/Scripts.arc",
        "vendor/mods/survivalmode/resources/Scripts.arc":
            VENDOR / "mods/survivalmode/resources/Scripts.arc",
        "vendor/survivalmode1/database/SurvivalMode1.arz":
            VENDOR / "survivalmode1/database/SurvivalMode1.arz",
    }
    instruments = {p.name: p for p in sorted(SCRIPTS.glob("pm4s_*_2026_08_14.py"))}
    outputs = {p.name: p for p in sorted(OUT.rglob("*")) if p.is_file()}

    doc = {
        "lap": "KC2-PM4 Lap S — the arena-and-advance decode",
        "agent": "legolas (UNKNOWN-RESEARCHER)",
        "date": "2026-08-14",
        "preregistration_sha256":
            "68f4e3a35ca7fdf4a2808f2bf3af16b3f1a2c13c6fbd7b6be65cf2115522af59",
        "preregistration_hashed_utc": "2026-08-14T15:23:39Z",
        "inputs": {k: sha256(v) for k, v in inputs.items()},
        "instruments": {k: sha256(v) for k, v in instruments.items()},
        "outputs": {k: sha256(v) for k, v in outputs.items()
                    if k != "pm4s_digests.json"},
    }
    tgt = OUT / "pm4s_digests.json"
    tgt.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")

    print("=" * 96)
    print("KC2-PM4 LAP S — DIGESTS")
    print("=" * 96)
    for sect in ("inputs", "instruments", "outputs"):
        print(f"\n  {sect.upper()}")
        for k, v in sorted(doc[sect].items()):
            print(f"    {v}  {k}")
    print(f"\n  PREREGISTRATION {doc['preregistration_sha256']}")
    print(f"  wrote {tgt}")


if __name__ == "__main__":
    main()
