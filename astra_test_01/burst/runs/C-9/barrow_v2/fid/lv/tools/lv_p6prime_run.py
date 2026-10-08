#!/usr/bin/env python3
"""BV2F LV (R-C9-234): run PH's OWN P6' harness (fid/ph/harness/p6prime_art.py, unchanged, frozen bars) on the current
art blockout WITHOUT writing into PH's lane: every file the harness would dump under fid/ph/ is redirected to
fid/lv/art/p6prime_lv/<same relative path>. PH's record (results/p6prime_art.json) is untouched; PH's formal run stands.

    python3 fid/lv/tools/lv_p6prime_run.py   -> fid/lv/art/p6prime_lv/results/p6prime_art.json (+ summary on stdout)
"""
import json
import os
import sys
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
LV = Path(HERE).parent
FID = LV.parent
OUT = LV / "art" / "p6prime_lv"
sys.path.insert(0, str(FID / "ph" / "harness"))

import common  # noqa: E402

_dump = common.dump
PHs = str(FID / "ph")


def dump_redirect(obj, p):
    p = str(p)
    if p.startswith(PHs):
        p = str(OUT / os.path.relpath(p, PHs))
        os.makedirs(os.path.dirname(p), exist_ok=True)
    return _dump(obj, p)


common.dump = dump_redirect
import p6_phase1  # noqa: E402
import p6prime  # noqa: E402
import p6prime_art as A  # noqa: E402

for m in (p6_phase1, p6prime, A):
    m.dump = dump_redirect
_pv = A.point_variant


def point_variant_redirect():
    lvl, syn = _pv()
    p6_phase1.LAYOUT = OUT / "results" / "art" / "layout_art_slots.json"     # read back the slot file it just wrote (redirected)
    assert p6_phase1.LAYOUT.exists()
    return lvl, syn


A.point_variant = point_variant_redirect

if __name__ == "__main__":
    r = A.run()
    print(json.dumps({k: r[k] for k in ("slot_crosscheck_vs_layout", "I4_red_shift_1p5m", "presence", "placement", "scale", "P6prime_pass")},
                     indent=1, default=str)[:5000])
