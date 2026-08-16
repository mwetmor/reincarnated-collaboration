#!/usr/bin/env python3
"""
KC2-PM4 · MICRO-LAP AD — digest manifest.

D-AA-5: digests are computed AFTER the final write of every artifact.
R-PM4-75 part 2 / I-28 DO-NOT 8: a truncated pin is a LOCATOR, not a digest.  Every full-64
value here is re-hashed FROM BYTES at the moment of writing.  Nothing is expanded from memory.
"""
import hashlib
import json
import pathlib

ROOT = pathlib.Path("/Users/admin/Games/reincarnated-collaboration")
LAP = ROOT / "agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-microlap-ad-t-leg"
SCRIPTS = ROOT / "agentic_orchestration/research/scripts"

EMITTED = ["prereg.md", "pm4ad_t_ref.csv", "pm4ad_t_ref.json", "pm4ad_findings.md"]
INSTRUMENTS = ["pm4ad_t_leg_2026_08_16.py", "pm4ad_digests_2026_08_16.py"]
INPUTS = [
    "agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-ac-referent-residence/pm4ac_residence.json",
    "agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-ac-referent-residence/pm4ac_digests.json",
    "agentic_orchestration/legolas/notes/2026-08-16-kc2-pm4-lap-ac-referent-residence/pm4ac_findings.md",
    "agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-r-locomotion-contact/pm4r_contact_occupancy.csv",
    "agentic_orchestration/research/scripts/pm4ac_residence_2026_08_16.py",
    "agentic_orchestration/research/scripts/pm4ac_lib_2026_08_16.py",
    "agentic_orchestration/research/scripts/pm4r_contact_2026_08_14.py",
    "agentic_orchestration/research/scripts/pm4r_lib_2026_08_14.py",
]


def h(p):
    p = pathlib.Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else "ABSENT-AT-HASH-TIME"


def main():
    out = {
        "lap": "AD",
        "law": ("digests computed AFTER the final write (D-AA-5); every full-64 re-hashed from "
                "bytes at the moment of writing (R-PM4-75 part 2 / I-28 DO-NOT 8); a truncated "
                "pin is a LOCATOR and is never expanded from memory"),
        "emitted": {f: h(LAP / f) for f in EMITTED},
        "instruments": {f: ("SELF — not self-referential; hashed by the conductor"
                            if f == "pm4ad_digests_2026_08_16.py" else h(SCRIPTS / f))
                        for f in INSTRUMENTS},
        "inputs": {f: h(ROOT / f) for f in INPUTS},
        "determinism": "x2 into separate directories; every emitted artifact byte-identical",
    }
    (LAP / "pm4ad_digests.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    for k, v in out["emitted"].items():
        print(f"  {v}  {k}")


if __name__ == "__main__":
    main()
