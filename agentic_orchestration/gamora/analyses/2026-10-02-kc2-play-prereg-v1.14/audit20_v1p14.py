#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.14 · OBS-1 RETRO-AUDIT OF "16/20 SURVIVE" (gamora, 2026-10-02). Read-only.

The conductor's note on jack-ryan OBS-1 (collab 29124a46e): a stalled ladder reads as SURVIVED, so the KP-226 picture
(V311-FULL, seat M-POL-2, salts 0-19: 16 survive) is verified here cell by cell. Salts 0-4 come from the graded-arm
batch trace (oracle_trace/hooked_M-POL-2.json.gz); salts 5-19 from single-salt runs of the SAME instrument
(oracle_trace/audit20/), which check_v1p14.py shows equal to the batch run on every oracle field (25/25).
Each salt must bank w151..w160, every wave cleared/board_empty or player_death/player_died, no exception, raised None.
The terminals are compared with pass 4's own persisted `leg_a_terminals` for V311-FULL (summary only).

Run: python3 audit20_v1p14.py [--ingest <scratch audit20 dir>]  -> audit20_v1p14.json
"""
import gzip
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TD = HERE / "oracle_trace"
PASS4 = HERE.parent / "2026-10-02-kc2-v3p11-oracle-pass4"
if len(sys.argv) > 2 and sys.argv[1] == "--ingest":
    (TD / "audit20").mkdir(parents=True, exist_ok=True)
    for s in range(5, 20):
        n = f"single_M-POL-2_s{s}.json"
        (TD / "audit20" / (n + ".gz")).write_bytes(gzip.compress((Path(sys.argv[2]) / n).read_bytes(), mtime=0))
L = lambda p: json.loads(gzip.decompress(p.read_bytes()))
cells = {}
H = L(TD / "hooked_M-POL-2.json.gz")
for s in range(20):
    t = (H if s < 5 else L(TD / "audit20" / f"single_M-POL-2_s{s}.json.gz"))["trace"]["salts"][str(s)]
    oc = [(w["wave"], w["outcome"], w["termination_reason"]) for w in t["waves"]]
    death = next((w for w, o, _ in oc if o == "player_death"), None)
    ok = ([w for w, _, _ in oc] == list(range(151, 161))
          and all((o, r) in (("cleared", "board_empty"), ("player_death", "player_died")) for _, o, r in oc)
          and t["exceptions"] == [] and t["raised"] is None and t["capture_rows_n"] == 10
          and (death is not None or oc[-1] == (160, "cleared", "board_empty")))
    cells[s] = {"complete": ok, "leg_a_death_wave": death, "outcomes": oc}
p4 = None
for f in sorted(PASS4.glob("pw_*.json")):
    d = json.loads(f.read_text())
    if "V311-FULL" in d["results"]:
        p4 = {"file": f.name, "leg_a_terminals": d["results"]["V311-FULL"]["all"]["leg_a_terminals"]}
out = {"cells": cells, "complete": sum(v["complete"] for v in cells.values()),
       "survive_genuine_w160_clear": sum(1 for v in cells.values() if v["complete"] and v["leg_a_death_wave"] is None),
       "pass4": p4,
       "terminals_equal_pass4": p4 is not None and [v["leg_a_death_wave"] for v in cells.values()] == p4["leg_a_terminals"]}
(HERE / "audit20_v1p14.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
print({k: v for k, v in out.items() if k != "cells"})
