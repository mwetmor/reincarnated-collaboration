#!/usr/bin/env python3
"""s59 / s63 P6a on a delta build (D-5, jack-ryan r339 delta Gate-2): the code that wrote the r339 P6a record.
  (1) KELP MODE (s59): every PAINTING candidate whose centre lies in the delta mask dilated 32 px is a 'kelp-mode candidate'
      -> p6a.json kelp_mode_candidates_in_delta_dil32 (r339: []).
  (2) ROW CARRY-FORWARD: each new row is matched to the previous build's row (same source, candidate px within 2 px). The
      final verdict, ruling and conductor read are carried; a row whose crop sha changed is flagged for re-confirm
      (conductor_read = PENDING re-confirm) instead of carried. Declared rows carry their declared verdict.
  (3) Conductor re-confirms are applied by candidate name from a {candidate: (read, ruling)} map (r339: c015, R-C9-346).
  site_p6a_carry.py check  -> recompute (1)-(3) from results/site_r332 + the committed r339 rows' raw fields; assert equal
  site_p6a_carry.py write <new_dir> <old_dir> <delta_mask.png> -> rewrite <new_dir>/p6a_triage.jsonl + p6a.json"""
import json
import sys
import os

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, os.path.dirname(__file__))
from common import *  # noqa

RECONFIRM = {"painting_2_4_c015": ("MATERIAL: open water (re-confirmed on the r339 crop; the kelp ice at the crop's top edge is the "
                                   "declared R-C9-339 change) -- R-C9-346", "R-C9-333 + R-C9-338 + R-C9-346")}


def kelp(rows, delta_png):
    D = ndimage.binary_dilation(np.asarray(Image.open(delta_png)) > 0, iterations=32)
    return [r["candidate"] for r in rows if r["source"] == "painting" and D[r["candidate_px"][1], r["candidate_px"][0]]]


def carry(rows, old, reconfirm=RECONFIRM):
    out = []
    for r in rows:
        r = dict(r)
        raw = r.get("verdict_pending_before", r["verdict"])
        o = [x for x in old if x["source"] == r["source"] and abs(x["candidate_px"][0] - r["candidate_px"][0]) <= 2
             and abs(x["candidate_px"][1] - r["candidate_px"][1]) <= 2]
        assert o, "no previous row for %s" % r["candidate"]
        o = o[0]
        r["verdict_pending_before"] = raw
        r["final_verdict"] = r["verdict"] = o["final_verdict"]
        if raw == "declared":
            r["conductor_read"] = "n/a"
            out.append(r)
            continue
        r["verdict_ruling"], r["conductor_reader"] = o.get("verdict_ruling"), o.get("conductor_reader")
        same = o.get("crop_sha") == r.get("crop_sha")
        r["carried_from"] = "r332 row %s (candidate px within 2 px; crop sha %s)" % (o["candidate"], "equal" if same else "CHANGED")
        r["kelp_mode"] = False
        if same:
            r["conductor_read"] = o["conductor_read"] + " (carried to r339; crop sha equal)"
        else:
            r["conductor_read"] = "PENDING re-confirm (crop changed by layer 25)"
        if r["candidate"] in reconfirm:
            r["conductor_read"], r["verdict_ruling"] = reconfirm[r["candidate"]]
            r["conductor_reader"] = "gandalf (conductor, by eye)"
        out.append(r)
    return out


KEYS = ("candidate", "verdict", "final_verdict", "conductor_read", "verdict_ruling", "carried_from", "kelp_mode")


def main():
    if sys.argv[1] == "check":
        old = [json.loads(l) for l in open(PH / "results/site_r332/p6a_triage.jsonl")]
        cur = [json.loads(l) for l in open(PH / "results/site_r339/p6a_triage.jsonl")]
        re_ = carry(cur, old)
        diff = [(a["candidate"], k) for a, b in zip(re_, cur) for k in KEYS if a.get(k) != b.get(k)]
        k = kelp(cur, PH / "results/site_r339/delta_mask.png")
        j = jload(PH / "results/site_r339/p6a.json")
        print({"rows": len(cur), "field_diffs": diff, "kelp_recomputed": k, "kelp_committed": j["kelp_mode_candidates_in_delta_dil32"],
               "pending": [r["candidate"] for r in re_ if "PENDING" in str(r.get("conductor_read"))]})
        assert not diff and k == j["kelp_mode_candidates_in_delta_dil32"]
        print("REPRODUCED")
    elif sys.argv[1] == "write":
        nd, od, dm = pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]), sys.argv[4]
        old = [json.loads(l) for l in open(od / "p6a_triage.jsonl")]
        cur = carry([json.loads(l) for l in open(nd / "p6a_triage.jsonl")], old)
        open(nd / "p6a_triage.jsonl", "w").write("".join(json.dumps(r) + "\n" for r in cur))
        j = jload(nd / "p6a.json")
        j.update(rows=cur, kelp_mode_candidates_in_delta_dil32=kelp(cur, dm),
                 pending_conductor_triage=[r["candidate"] for r in cur if "PENDING" in str(r.get("conductor_read"))])
        dump(j, str(nd / "p6a.json"))


if __name__ == "__main__":
    main()
