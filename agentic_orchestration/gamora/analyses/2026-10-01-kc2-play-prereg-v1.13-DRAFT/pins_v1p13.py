#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.13 DRAFT · EVERY PIN v1.12 CARRIES, RECOMPUTED; plus the new documents of record.

gamora, 2026-10-01. DRAFT INSTRUMENT, NOT A PREREG.

Rule (KP-20, KP-43): a new version recomputes every pin it carries, including the ones it believes unchanged.
This script never types a carried digest: each v1.12 value is EXTRACTED from the v1.12 file (FILE a0454776...) by the
unique row text it sits on, and the recomputation is asserted equal to it. New pins (documents that did not exist
at v1.12) are computed and reported, with no expected value.

READ-ONLY everywhere. godot is read through `git show <rev>:<path>` only. The sealed cells are HASHED ONLY (K-7).
The oracle is called only through `pool466`, `load_profiles`, `derive_oracle_speeds`, `SpawnStructureFold.offset`
(the same entry points v1.12 used) and `wave_engine.pools_for`.

Run: python3 pins_v1p13.py   -> prints a report; writes pins_v1p13.json beside itself.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import struct
import subprocess
import sys
from pathlib import Path

HOME = Path.home() / "Games"
COLLAB = HOME / "reincarnated-collaboration"
ENGINE = HOME / "reincarnated-engine"
GODOT = HOME / "reincarnated-godot"
AO = COLLAB / "agentic_orchestration"
SIM = ENGINE / "src/reincarnated/simulation"
OUT = ENGINE / "src/reincarnated/output"
MODEL = OUT / "kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247"
REFP = OUT / "kc2-reference-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247"
V112 = AO / "gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.12.md"
HERE = Path(__file__).resolve().parent
TEXT = V112.read_text(encoding="utf-8")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fsha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def gshow(rev: str, path: str) -> bytes:
    return subprocess.run(["git", "-C", str(GODOT), "show", f"{rev}:{path}"], check=True, capture_output=True).stdout


def v112(anchor: str, nth: int = 0) -> str:
    """The nth 64-hex on the ONE line of v1.12 containing `anchor` (asserted unique)."""
    lines = [ln for ln in TEXT.split("\n") if anchor in ln]
    assert len(lines) == 1, (anchor, len(lines))
    hx = re.findall(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", lines[0])
    return hx[nth]


R: dict = {"carried": {}, "new": {}, "failures": []}


def carried(key: str, got: str, want: str, label: str, path: str) -> None:
    ok = got == want
    R["carried"][key] = {"label": label, "path": path, "sha256": got, "v1.12": want, "reproduces": ok}
    if not ok:
        R["failures"].append(key)


# ---------------------------------------------------------------------------------------------- PINS table (FILE)
FILEPINS = {
    "P-a": ("| P-a |", AO / "gamora/notes/2026-09-20-kc2-play-ta-band-widths.md"),
    "P-b": ("| P-b |", AO / "galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values-and-u-rider.md"),
    "P-c": ("| P-c |", AO / "galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values.json"),
    "P-d": ("| P-d |", AO / "galadriel/notes/2026-09-20-kc2-play-w1-tb-release-labels.json"),
    "P-e": ("| P-e |", SIM / "math/kc2-play-v3p4-roster-basis-rebase-2026-09-21.md"),
    "P-e'": ("| P-e′ |", SIM / "math/kc2-play-v3p3-monster-offense-prereg-2026-09-20.md"),
    "P-i": ("| P-i |", ENGINE / "data/kc2/pm4p_leech_resistance.csv"),
    "P-j": ("| P-j |", ENGINE / "data/kc2/pm4l_mitigation_by_body.csv"),
    "P-k": ("| P-k |", ENGINE / "data/kc2/pm2_tg2_monster_timing.csv"),
    "P-l.c2": ("| P-l.c2 |", SIM / "math/kc2-c2-per-cast-energy-cost-fold-2026-09-28.md"),
    "P-l.c7": ("| P-l.c7 |", SIM / "math/kc2-c7-insufficient-energy-refuse-fold-2026-09-29.md"),
    "P-l.nine": ("| P-l.nine |", SIM / "math/kc2-play-nine-winner-surface-reconstruction-2026-09-29.md"),
    "P-l.upn4": ("| P-l.upn4 |", SIM / "math/kc2-play-upn4-occupancy-by-pilot-2026-09-29.md"),
    "P-l.upn5": ("| P-l.upn5 |", SIM / "math/kc2-play-upn5-global-magnitude-fold-lift-2026-09-29.md"),
    "P-l.upn5A": ("| P-l.upn5A |", SIM / "math/kc2-play-upn5-global-magnitude-fold-lift-ADDENDUM-2026-09-29.md"),
    "P-l.q91": ("| P-l.q91 |", SIM / "math/kc2-play-q91-338-pool-damage-lift-2026-09-29.md"),
    "P-l.q91a": ("| P-l.q91a |", SIM / "math/kc2-play-q91-338-pool-damage-lift-ADDENDUM-2026-09-29.md"),
    "P-l.c11a": ("| P-l.c11a |", SIM / "math/kc2-play-c11a-oracle-corrections-fold-2026-09-30.md"),
    "P-l.c11aA": ("| P-l.c11aA |", SIM / "math/kc2-play-c11a-oracle-corrections-fold-ADDENDUM-2026-09-30.md"),
    "P-n.1": ("| P-n.1 |", SIM / "output/kc2-play-q91-pool-lift-pricing-20260930_023137.json"),
    "P-n.2": ("| P-n.2 |", SIM / "output/kc2-lifted-rows-KC2PLAY-SEALLAP-W1-c2-energy-fold-20260928_232836.json"),
    "P-n.3": ("| P-n.3 |", SIM / "output/kc2-play-c11a-fold-pricing-NOT-A-GRADED-RUN-20260930_043045-SUMMARY.json"),
    "P-n.4": ("| P-n.4 |", SIM / "output/kc2-play-c11a-landed-by-source-NOT-A-GRADED-RUN-20260930_033242.json"),
    "P-o": ("| P-o |", ENGINE / "data/kc2/c11a_aura_buff_grants.csv"),
}
for k, (anc, p) in FILEPINS.items():
    carried(k, fsha(p), v112(anc), "FILE", str(p))


# ---------------------------------------------------------------------------------------------- the two PACKs
def pack(d: Path, sub: str) -> dict:
    pm = json.loads((d / "manifest.json").read_text())
    pl, bad = [], []
    for m in pm["members"]:
        p = d / m["path"]
        g = fsha(p)
        if g != m["sha256"] or p.stat().st_size != m["bytes"]:
            bad.append(m["path"])
        pl.append(f"{m['path']}  {g}")
    disk = sorted(str(p.relative_to(d)) for p in (d / sub).rglob("*") if p.is_file())
    return {"digest": sha("\n".join(sorted(pl)).encode("utf-8")), "manifest_digest": pm["pack_digest"],
            "n": len(pm["members"]), "member_failures": bad,
            "disk_equals_manifest": disk == sorted(m["path"] for m in pm["members"]),
            "cross_pin": (pm.get("cross_pin") or {}).get("model_pack_digest"),
            "manifest_file": fsha(d / "manifest.json"),
            "members": {m["path"]: fsha(d / m["path"]) for m in pm["members"]}}


mp, rp = pack(MODEL, "model"), pack(REFP, "reference")
carried("P-h model PACK", mp["digest"], v112("| P-h |"), "PACK", str(MODEL))
carried("P-h2 reference PACK", rp["digest"], v112("| P-h2 |"), "PACK", str(REFP))
R["pack_checks"] = {"model": {k: mp[k] for k in ("n", "member_failures", "disk_equals_manifest", "manifest_digest")},
                    "reference": {k: rp[k] for k in ("n", "member_failures", "disk_equals_manifest", "manifest_digest",
                                                     "cross_pin")}}
for nm, pk in (("model", mp), ("reference", rp)):
    if pk["member_failures"] or not pk["disk_equals_manifest"] or pk["digest"] != pk["manifest_digest"]:
        R["failures"].append(f"{nm} pack self-check")
if rp["cross_pin"] != mp["digest"]:
    R["failures"].append("cross_pin")
carried("model manifest.json", mp["manifest_file"], v112("· reference `manifest.json`", 0), "FILE",
        str(MODEL / "manifest.json"))
carried("reference manifest.json", rp["manifest_file"], v112("· reference `manifest.json`", 1), "FILE",
        str(REFP / "manifest.json"))
for mem in sorted(mp["members"]):
    name = mem.split("/", 1)[1]
    carried(f"model/{name}", mp["members"][mem], v112(f" | `{name}` | FILE |"), "FILE", mem)
refline = [ln for ln in TEXT.split("\n") if ln.startswith("**Reference pack (7), FILE each:**")][0]
for mem, g in rp["members"].items():
    name = mem.split("/", 1)[1]
    m = re.search(re.escape(f"`{name}` ") + r"`([0-9a-f]{64})`", refline)
    carried(f"reference/{name}", g, m.group(1), "FILE", mem)

# ---------------------------------------------------------------------------------------------- set digests (oracle)
sys.path.insert(0, str(ENGINE / "src"))
cwd = os.getcwd()
os.chdir(ENGINE)
try:
    from reincarnated.export.kc2_baton_v3p5p1_schema import pool466, derive_oracle_speeds, partition
    from reincarnated.simulation.kc2 import threat, pool_lift
    from reincarnated.simulation.kc2.winner_surface import WinnerSurfaceFold
    from reincarnated.simulation.kc2.c11a_corrections import C11aLoader, AuraScope
    from reincarnated.simulation.kc2.spawn_structure import SpawnStructureFold, ScatterLaw, RngRepr
    tree = {"model/waves.json": json.loads((MODEL / "model/waves.json").read_text())}
    pool, routes_agree = pool466(tree)
    ws = WinnerSurfaceFold.from_x8("src/reincarnated/simulation/output/"
                                   "kc2-lifted-rows-KC2PLAY-SEALLAP-W1-c2-energy-fold-20260928_232836.json")
    roster, _p, _r = threat.load_profiles(dot_corrections=True, winner_surface=ws, pool_lift=pool_lift.load(),
                                          c11a=C11aLoader(scope=AuraScope.CLASS))
    cs = {}
    for k, v in roster.items():
        s = v.can_swing
        cs[k.lower()] = bool(s() if callable(s) else s)
    swing = {r for r in pool if cs.get(r)}
    nonswing = pool - swing
    mtree = {f"model/{p.name}": json.loads(p.read_text()) for p in (MODEL / "model").glob("*.json")}
    spd = derive_oracle_speeds(mtree)
    part = partition(spd)
    # TA-X-18 on the oracle's own fold, a stream returning 0.5 twice
    class _Half:
        def random(self):
            return 0.5
    off = SpawnStructureFold(scatter=ScatterLaw.POLAR_UNIFORM_RHO, rng_repr=RngRepr.CONTINUOUS).offset(_Half())
finally:
    os.chdir(cwd)


def setd(s) -> str:
    return sha("\n".join(sorted(s)).encode("utf-8"))


fb_key = [k for k in part if len(part[k]) == 158]
carried("POOL-466", setd(pool), v112("| **POOL-466** |"), "ROWSET", "pool466(waves.json)")
carried("SWING-456", setd(swing), v112("| **SWING-456** |"), "ROWSET", "load_profiles can_swing over POOL-466")
carried("NONSWING-10", setd(nonswing), v112("| **NONSWING-10** |"), "ROWSET", "POOL-466 minus SWING-456")
carried("FALLBACK-158", setd(part[fb_key[0]]) if len(fb_key) == 1 else "n/a", v112("| **FALLBACK-158** |"), "ROWSET",
        "derive_oracle_speeds partition, FALLBACK class")
R["set_cardinalities"] = {"POOL": len(pool), "routes_agree": routes_agree, "SWING": len(swing),
                          "NONSWING": len(nonswing), "partition": {k: len(v) for k, v in part.items()},
                          "march_base": spd["march_base"]}
bits = [struct.pack(">d", x).hex() for x in off]
R["TA-X-18"] = {"value": [repr(x) for x in off], "bits": bits,
                "equals_v1.12": bits == ["c00fffffffffffde", "be9777a5cf72cec6"]}
if not R["TA-X-18"]["equals_v1.12"]:
    R["failures"].append("TA-X-18")

# ---------------------------------------------------------------------------------------------- TA-X-09 and a8 ROWSETs
mr = json.loads((MODEL / "model/math_rules.json").read_text())
FIVE = ["RULE-CHANNEL-MOVEMENT", "RULE-RELEASE-TYPE-A", "RULE-RELEASE-TYPE-B",
        "RULE-CAST-INTERRUPT-BINDING-EXCLUSIVITY", "RULE-DMG-APPLIED"]
vecs = [tv for r in mr["rules"] if r.get("rule_id") in FIVE for tv in r.get("test_vectors", [])]
carried("TA-X-09 nine vectors", sha(json.dumps(vecs, sort_keys=True, separators=(",", ":"), default=str).encode()),
        v112("* **ROWSET `0e826ee0"), "ROWSET", f"math_rules five rules, {len(vecs)} vectors")
R["TA-X-09_n"] = len(vecs)

ic = json.loads((MODEL / "model/input_closure_v3p7p1.json").read_text())
a8 = ic["⚑ v3p7p1_rows"]["a8_composition_calls"]
jobs: dict = {}
for row in a8:
    jobs.setdefault(row["value"]["job"], []).append(row)


def rowset(rows) -> str:
    return sha(json.dumps(sorted(rows, key=lambda r: r["id"]), sort_keys=True, separators=(",", ":"),
                          default=str).encode())


A8_ANCHOR = {"setup": "| **`setup`** (shared", "M0": "| **`M0`** |", "M-POL-2": "| **`M-POL-2`** |",
             "M-POL-2-NULL": "| **`M-POL-2-NULL`** |", "W1": "| **`W1`** |", "W1-NULL": "| **`W1-NULL`** |",
             "WALK": "| **`WALK`** ("}
for job, anc in A8_ANCHOR.items():
    carried(f"a8 {job}", rowset(jobs[job]), v112(anc), "ROWSET", f"a8 job {job} ({len(jobs[job])} rows)")
C_IDS = {"IC7-A-0435", "IC7-A-0439", "IC7-A-0446", "IC7-A-0452", "IC7-A-0453", "IC7-A-0454", "IC7-A-0455", "IC7-A-0459"}
fight_callees = [{r["value"]["callee"] for r in jobs[j]} for j in ("M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL")]
C_rule = {r["id"] for r in jobs["setup"] if not any(r["value"]["callee"] in fc for fc in fight_callees)}
T_rule = {r["id"] for r in jobs["setup"] if all(r["value"]["callee"] in fc for fc in fight_callees)}
R["setup_partition"] = {"C_by_rule_equals_v1.12_list": C_rule == C_IDS, "n_C": len(C_rule), "n_T": len(T_rule),
                        "covers_27": len(C_rule | T_rule) == 27 and not (C_rule & T_rule)}
carried("setup C", rowset([r for r in jobs["setup"] if r["id"] in C_rule]), v112("| **C · shared configuration**"),
        "ROWSET", "setup part C")
carried("setup T", rowset([r for r in jobs["setup"] if r["id"] in T_rule]), v112("| **T · the tick-period probe**"),
        "ROWSET", "setup part T")

# ---------------------------------------------------------------------------------------------- documents of record
DOCS = {
    "prereg v1.11": ("⚑ prereg **v1.11** (superseded", AO / "gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.11.md"),
    "v1.11 pre-read": ("⚑ jack-ryan's **v1.11 pre-read**", AO / "qa/findings/2026-10-01-kc2-play-prereg-v1.11-pre-read.md"),
    "prereg v1.10": ("| prereg v1.10 (not edited", AO / "gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.10.md"),
    "prereg v1.9": ("| prereg v1.9 (not edited", AO / "gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.9.md"),
    "prereg v1.8": ("| prereg v1.8 (not edited", AO / "gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.8.md"),
    "prereg v1.7": ("| prereg v1.7 (not edited)", AO / "gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.7.md"),
    "prereg v1.6": ("| prereg v1.6 (not edited)", AO / "gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.6.md"),
    "prereg v1.5": ("| ⚑ prereg **v1.5**", AO / "gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.5.md"),
    "v1.8 pre-read": ("| jack-ryan's v1.8 pre-read", AO / "qa/findings/2026-09-30-run-KC2-PLAY-prereg-v1.8-preread.md"),
    "v1.7 pre-read": ("| jack-ryan's v1.7 pre-read", AO / "qa/findings/2026-09-29-run-KC2-PLAY-prereg-v1.7-preread.md"),
    "v1.7 att1 Gate-2": ("| jack-ryan's Gate-2 on attempt 1", AO / "qa/findings/2026-09-29-run-KC2-PLAY-ta-grade-v1p7-attempt1-gate2.md"),
    "v1.7 att1 grade": ("| attempt-1 grade note |", AO / "gamora/notes/2026-09-29-kc2-play-ta-grade-v1p7-attempt1.md"),
    "v1.7 att1 verdict": ("| attempt-1 verdict file |", AO / "gamora/notes/2026-09-29-kc2-play-ta-verdict-v1p7-attempt1.json"),
    "v1.6 pre-read": ("| jack-ryan's v1.6 pre-read", AO / "qa/findings/2026-09-29-run-KC2-PLAY-w2-prereg-v1.6-preread.md"),
    "grade of record": ("| the grade of record (", AO / "gamora/notes/2026-09-21-kc2-play-ta-grade.md"),
    "discrimination audit": ("| the discrimination audit", AO / "gamora/notes/2026-09-21-kc2-play-discrimination-audit.md"),
    "divergence register v0.3": ("| divergence register v0.3", AO / "gandalf/notes/2026-09-20-kc2-play-divergence-register-v0.3.md"),
    "H-9 NOTE": ("`H-9` evidence: `NOTE.md`", AO / "gamora/analyses/2026-09-30-kc2-play-h9-w1-containment/NOTE.md"),
    "H-9 W1": ("`H-9` evidence: `h9_out_W1.json`", AO / "gamora/analyses/2026-09-30-kc2-play-h9-w1-containment/h9_out_W1.json"),
    "H-9 M-POL-2": ("`H-9` evidence: `h9_out_M-POL-2.json`", AO / "gamora/analyses/2026-09-30-kc2-play-h9-w1-containment/h9_out_M-POL-2.json"),
    "H-9 W1-NULL": ("`H-9` evidence: `h9_out_W1-NULL.json`", AO / "gamora/analyses/2026-09-30-kc2-play-h9-w1-containment/h9_out_W1-NULL.json"),
    "H-9 script": ("`H-9` evidence: `h9_w1_containment.py`", AO / "gamora/analyses/2026-09-30-kc2-play-h9-w1-containment/h9_w1_containment.py"),
    "v3.7 cut prereg": ("| star-lord's v3.7 cut prereg", ENGINE / "src/reincarnated/export/math/2026-09-30-kc2-pack-v3-7-input-closure-prereg.md"),
    "v3.7 cut receipt": ("| the v3.7 cut receipt", OUT / "kc2-baton-v3-cut-receipt-v3p7-20260930_231652.json"),
    "v3.7 closure BEFORE": ("| v3.7 closure table BEFORE", OUT / "kc2-v3p7-closure-table-BEFORE-20260930_231652.json"),
    "v3.7 closure AFTER": ("| v3.7 closure table AFTER", OUT / "kc2-v3p7-closure-table-AFTER-20260930_231652.json"),
    "H-10 run v3.7": ("the H-10 run on v3.7", OUT / "kc2-v3p7-h10-summary-20261001_001232.json"),
    "v3.7.1 PRE gate": ("the v3.7.1 PRE gate and dry run", OUT / "kc2-v3p7p1-PRE-gate-and-dry-run-20261001_PRE2.json"),
    "v3.7.1 cut prereg": ("star-lord's **v3.7.1 cut prereg**", ENGINE / "src/reincarnated/export/math/2026-10-01-kc2-pack-v3-7-1-closure-law-prereg.md"),
    "v3.7.1 cut receipt": ("the **v3.7.1 cut receipt**", OUT / "kc2-baton-v3-cut-receipt-v3p7p1-20261001_021247.json"),
    "closure instrument": ("the closure instrument `export/kc2_v3p7_closure.py`", ENGINE / "src/reincarnated/export/kc2_v3p7_closure.py"),
    "v3.7.1 law": ("the v3.7.1 law `export/kc2_v3p7p1_law.py`", ENGINE / "src/reincarnated/export/kc2_v3p7p1_law.py"),
    "POST M0": ("oracle terminals, instrument-free, `M0`", OUT / "kc2-v3p7p1-POST-bare-M0-20261001_021247.json"),
    "POST M-POL-2": ("| ⚑ … `M-POL-2` |", OUT / "kc2-v3p7p1-POST-bare-M-POL-2-20261001_021247.json"),
    "POST M-POL-2-NULL": ("| ⚑ … `M-POL-2-NULL` |", OUT / "kc2-v3p7p1-POST-bare-M-POL-2-NULL-20261001_021247.json"),
    "POST W1": ("| ⚑ … `W1` |", OUT / "kc2-v3p7p1-POST-bare-W1-20261001_021247.json"),
    "POST W1-NULL": ("| ⚑ … `W1-NULL` |", OUT / "kc2-v3p7p1-POST-bare-W1-NULL-20261001_021247.json"),
}
for k, (anc, p) in DOCS.items():
    carried(k, fsha(p), v112(anc), "FILE", str(p))
GDOCS = {
    "933b438 kc2rt_fight.gd (READ, lineage)": ("the port's conservation code, READ for § F.2k", "933b438", "kc2_runtime/sim/kc2rt_fight.gd", 0),
    "933b438 kc2rt_laws.gd (READ, lineage)": ("`kc2_runtime/sim/kc2rt_laws.gd` (same status)", "933b438", "kc2_runtime/sim/kc2rt_laws.gd", 0),
    "933b438 G3 oracle tool (READ, lineage)": ("the G3 instrument, READ for § C.9", "933b438", "kc2_runtime/tools/kc2rt_g3_oracle_trace.py", 0),
    "933b438 G3 port tool (READ, lineage)": ("`kc2_runtime/tools/kc2rt_g3_loop_trace.gd` (the port side)", "933b438", "kc2_runtime/tools/kc2rt_g3_loop_trace.gd", 0),
    "ffb454e kc2rt_fight.gd (lineage)": ("lineage only, superseded: `kc2rt_fight.gd`", "ffb454e", "kc2_runtime/sim/kc2rt_fight.gd", 0),
    "fae29ec kc2rt_fight.gd (lineage)": ("lineage only, superseded: `kc2rt_fight.gd`", "fae29ec", "kc2_runtime/sim/kc2rt_fight.gd", 1),
    "ffb454e kc2rt_laws.gd (lineage)": ("lineage only: `kc2rt_laws.gd` at `ffb454e`", "ffb454e", "kc2_runtime/sim/kc2rt_laws.gd", 0),
}
for k, (anc, rev, path, nth) in GDOCS.items():
    carried(k, sha(gshow(rev, path)), v112(anc, nth), "FILE", f"godot {rev}:{path}")
SEALED = {
    "[M-POL2]": "kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json",
    "[MECH]": "kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json",
    "[W1W]": "kc2-checkpoint-E-s09-cp150-w1walls-20260825_220058.json",
}
for k, name in SEALED.items():
    p = SIM / "output" / name
    carried(f"sealed {k}", fsha(p), v112(f"| `{k}` | `{name}`"), "FILE (hashed only, K-7)", str(p))

# ---------------------------------------------------------------------------------------------- NEW documents of record
NEW = {
    "prereg v1.12 (v1.13's only predecessor)": V112,
    "attempt-1 (v1.12) grade note": AO / "gamora/notes/2026-10-01-kc2-play-ta-attempt1-v1.12-grade.md",
    "attempt-1 (v1.12) verdict file": AO / "gamora/analyses/2026-10-01-kc2-play-ta-attempt1-v1.12-grade/ta_verdict_v1p12_attempt1.json",
    "attempt-1 (v1.12) grade script": AO / "gamora/analyses/2026-10-01-kc2-play-ta-attempt1-v1.12-grade/grade_attempt1_v1p12.py",
    "jack-ryan grade Gate-2 (347ce2e1e)": AO / "qa/findings/2026-10-01-kc2-play-attempt1-v1.12-grade-gate2.md",
    "jack-ryan repairs Gate-2 (ea0317306)": AO / "qa/findings/2026-10-01-kc2-play-attempt1-repairs-gate2.md",
    "this draft's oracle hook": HERE / "oracle_channel_hook.py",
}
for k, p in NEW.items():
    R["new"][k] = {"label": "FILE", "path": str(p), "sha256": fsha(p)}
G3REV = "b4c1ff3"
G3M = "evidence/kc2-play/2026-10-01-g3-25cell-kp177/MANIFEST.json"
R["new"]["G3 KP-177 MANIFEST (godot b4c1ff3)"] = {"label": "FILE", "path": f"godot {G3REV}:{G3M}",
                                                   "sha256": sha(gshow(G3REV, G3M))}
R["new"]["G3 oracle tool (godot b4c1ff3)"] = {"label": "FILE", "path": f"godot {G3REV}:kc2_runtime/tools/kc2rt_g3_oracle_trace.py",
                                              "sha256": sha(gshow(G3REV, "kc2_runtime/tools/kc2rt_g3_oracle_trace.py"))}
rman = json.loads(gshow(G3REV, "kc2_runtime/MANIFEST.json"))
rl, rbad = [], []
for m in rman["members"]:
    g = sha(gshow(G3REV, "kc2_runtime/" + m["path"]))
    if g != m["sha256"]:
        rbad.append(m["path"])
    rl.append(f"{m['path']}  {g}")
R["new"]["runtime tree at b4c1ff3 (KP-179 repairs; NOT the attempt-2 runtime)"] = {
    "label": "FILE-SET (make_manifest law, recomputed from git blobs)", "path": f"godot {G3REV}:kc2_runtime/",
    "sha256": sha("\n".join(sorted(rl)).encode()), "manifest_says": rman["tree_digest"], "n_members": len(rman["members"]),
    "member_failures": rbad}
R["engine_head"] = subprocess.run(["git", "-C", str(ENGINE), "rev-parse", "--short=8", "HEAD"], check=True,
                                  capture_output=True, text=True).stdout.strip()
R["engine_kc2_tracked_mods"] = subprocess.run(
    ["git", "-C", str(ENGINE), "status", "--porcelain", "--", "src/reincarnated/simulation/kc2",
     "src/reincarnated/export", "src/reincarnated/simulation/scripts"], check=True, capture_output=True,
    text=True).stdout.split("\n")
R["engine_kc2_tracked_mods"] = [x for x in R["engine_kc2_tracked_mods"] if x and not x.startswith("??")]

R["summary"] = {"n_carried": len(R["carried"]), "n_reproduce": sum(v["reproduces"] for v in R["carried"].values()),
                "failures": R["failures"], "n_new": len(R["new"])}
(HERE / "pins_v1p13.json").write_text(json.dumps(R, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
print(json.dumps(R["summary"], indent=1))
print("engine HEAD", R["engine_head"], "tracked mods under kc2/export/scripts:", R["engine_kc2_tracked_mods"])
print("setup partition", R["setup_partition"], "TA-X-18", R["TA-X-18"]["equals_v1.12"], "sets", R["set_cardinalities"])
for k, v in R["new"].items():
    print("NEW", k, v["sha256"])
sys.exit(1 if R["failures"] else 0)
