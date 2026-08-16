#!/usr/bin/env python3
"""KC2-PM4 Lap AC — the digest artifact.  Run AFTER the final write of every other file
(the `D-AA-5` law: digests are computed post-final-write, and the committed blob must equal
the working tree).

READ-ONLY.  OUTCOME-FIREWALLED.
Author: legolas (UNKNOWN-RESEARCHER), 2026-08-16.
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
from pm4ac_lib_2026_08_16 import OUT, SCRIPTS, PINNED, PREREG_SHA, sha256   # noqa: E402

EMITTED = [
    "prereg.md",
    "pm4ac_findings.md",
    "pm4ac_ring_intervals.csv",
    "pm4ac_ring_exits.csv",
    "pm4ac_tracks.csv",
    "pm4ac_residence.json",
    "pm4ac_green_census.csv",
    "pm4ac_green_detections.csv",
    "pm4ac_green_census.json",
    "pm4ac_green_persistence.csv",
    "pm4ac_green_persistence.json",
    "pm4ac_green_adjudication.csv",
    "evidence/crop-700-cluster.png",
    "evidence/crop-702-cluster.png",
    "evidence/contact-offcentre-green.png",
    "evidence/strip-green-0.png",
    "evidence/strip-green-1.png",
    "evidence/strip-green-2.png",
    "evidence/strip-green-3.png",
]
INSTRUMENTS = [
    "pm4ac_lib_2026_08_16.py",
    "pm4ac_residence_2026_08_16.py",
    "pm4ac_green_census_2026_08_16.py",
    "pm4ac_green_persist_2026_08_16.py",
    "pm4ac_digests_2026_08_16.py",
]


def main():
    out = {"lap": "AC", "prereg_sha256": PREREG_SHA,
           "law": "digests computed AFTER the final write (D-AA-5); the committed blob must "
                  "equal the working tree",
           "emitted": {}, "instruments": {}, "inputs": {}}
    for rel in EMITTED:
        p = OUT / rel
        if p.exists():
            out["emitted"][rel] = sha256(p)
    for rel in INSTRUMENTS:
        p = SCRIPTS / rel
        if rel == "pm4ac_digests_2026_08_16.py":
            out["instruments"][rel] = "SELF — not self-referential; hashed by the conductor"
            continue
        out["instruments"][rel] = sha256(p)
    for path, want in sorted(PINNED.items()):
        got = sha256(path)
        assert got == want, f"HALT: pinned input drifted: {path}"
        out["inputs"][path] = got

    q = OUT / "pm4ac_digests.json"
    q.write_text(json.dumps(out, indent=2, sort_keys=True))
    print(json.dumps(out["emitted"], indent=2, sort_keys=True))
    print(f"\npm4ac_digests.json  sha256={sha256(q)}")


if __name__ == "__main__":
    main()
