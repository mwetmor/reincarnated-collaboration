#!/usr/bin/env python3
"""KC2-PLAY · T-A graded attempt 2 of 2 under prereg v1.13 (overall attempt 3; the last under the cap) -- THE GRADE OF
RECORD'S INSTRUMENT.

gamora, 2026-10-01. Grades drax's emission (godot 7a97716, evidence/kc2-play/2026-10-01-ta-attempt2-v1.13-cells/)
against prereg v1.13 (FILE c35cca9c...) and every row it carries from v1.12 (FILE a0454776...) and, by reference,
v1.8 ... v1.11. GRADING ONLY: every expected value and tolerance below is quoted from those texts; none is set here.

INDEPENDENCE: this grader is gamora's own. It shares no code with jack-ryan's H-7 grader (d02b5ac4 / r2 a75b39f5);
it was not read before this file was written beyond the two field-handling corrections his read discloses, which are
re-derived here from the pack and the source rather than copied. It re-uses gamora's attempt-1 instrument
(collab d2fe958ec) for the carried rows.

The SAME `grade()` is run on two emissions:
  * the ATTEMPT (graded; godot 7a97716) -- this is the grade of record;
  * the § G.1a PRE-READ (godot 4833bcf; NOT A GRADED RUN) -- read only to print § G.1a item 5's graded-vs-read face.

READ-ONLY everywhere: godot through `git show <rev>:<path>` (each worktree copy checked equal to its blob); the engine
oracle tree at 22cd2288 (clean under simulation/kc2, export) is imported read-only for the set digests; the pack is
hashed on disk; the sealed cells are not opened. Nothing graded is re-run.

Run:  python3 grade_attempt2_v1p13.py   -> prints the report; writes results.json + ta_verdict_v1p13_attempt2.json here.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
import struct
import subprocess
import sys
from collections import defaultdict
from fractions import Fraction as Fr
from pathlib import Path

HOME = Path.home() / "Games"
GODOT = str(HOME / "reincarnated-godot")
COLLAB = HOME / "reincarnated-collaboration"
ENGINE = HOME / "reincarnated-engine"
REV = "7a97716"                                   # drax's attempt evidence commit (KP-188)
REV_RT = "0f36826"                                # the candidate commit named at KP-186 (godot HEAD at the run)
EV = "evidence/kc2-play/2026-10-01-ta-attempt2-v1.13-cells"
REV_PR = "4833bcf"                                # the § G.1a pre-read emission (KP-186)
EV_PR = "evidence/kc2-play/2026-10-01-PRE-READ-NOT-A-GRADED-RUN-v1.13"
G3DIR = "evidence/kc2-play/2026-10-01-g3-25cell-kp184"
PREREG = COLLAB / "agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.13.md"
PREREG12 = COLLAB / "agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.12.md"
H7 = COLLAB / "agentic_orchestration/qa/findings/2026-10-01-kc2-play-v1.13-pre-attempt-read.md"
H7_COMMIT = "9e1b19872"
OUT = ENGINE / "src/reincarnated/output"
MODEL = OUT / "kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247"
REFP = OUT / "kc2-reference-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247"
HERE = Path(__file__).resolve().parent

ARMS = ["M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"]
SALTS = [0, 1, 2, 3, 4]
ALLC = [(a, s) for a in ARMS for s in SALTS]
EXACT = ["TA-X-%02d" % i for i in (1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24,
                                    25, 26, 27, 28, 29, 30)]
assert len(EXACT) == 28

PIN = {
    "prereg_v1.13": "c35cca9ceb189b5f78a09b402f9df81b3bb126db132643a57049eb1cc8a46d68",
    "prereg_v1.12": "a0454776ab91d85f37fadffcb8886a498e1f498f208e0eb33b9d5a9797fc7854",
    "emission_MANIFEST": "1e27c5fdd83e9927a570ae8bc81bf13babe3c726a7a7692abfd988a865027498",   # KP-188 (prefix 1e27c5fd)
    "ta_manifest": "9e35fb2e3286b0333b3b060056f7caff68d022e009d5efa62a2e219bc557bb82",         # KP-188 (prefix 9e35fb2e)
    "ta_verdict": "f7e19dc1a0ec0b1134bdf2841e005e10611edd6e130f66f2610842b61b80a090",          # KP-188 (prefix f7e19dc1)
    "preread_MANIFEST": "9ed1b999ff0186056beb4a1730629fa67131e5160519df235a776e572c78c43a",    # KP-186 / H-7
    "preread_ta_manifest": "347f8badb7dabebea22d5df8b25389abf87ddd4ea15f507e80db8a183623616f",
    "preread_ta_verdict": "8dc0a193b5e202295ae732eaa0d96560e372202d40f8aed5ad07e8921653a690",
    "runtime_tree": "d03ca8913901d61de73db40287e31e498e8b2714521f8221fde414682e328ccd",        # KP-186 candidate
    "H7_read": "69235e139a2e3bc4340fd2ace4762b023f8c7290cda7fe709f75bec0e486d742",             # KP-187 (FILE 69235e13)
    "g3_MANIFEST": "f861b7a16111531b1e0f7d8fc6358ffe78cc698202ec5f5645d295c6a903abbd",         # H-3 / H-7
    "l2_operands_jsonl": "b5bcdb7ba61b8ffd159108b44b53c6bc63927fb9821f6eda26bd9afd356c0e77",   # H-2 (KP-177/180/184)
    "model_pack": "48a4c94c165715d3f4f5db89c1278aa8439fbe1507c39dd555f7ce91d4636c96",
    "reference_pack": "1887257f5370443a1729fde2ff446579b1acc501dcd03679244297b541e3e5b1",
    "POOL-466": "33c886a11f91db1143c791ffcf9d95f7e7614e423373235231733c994c5c157b",
    "SWING-456": "706a61d55dc6621814fc923d7428c5b263a95ebb00e9786d12f35dd385a7a4c0",
    "NONSWING-10": "00b4cb0e24b43e591a2e30200979725801aad1e7c1f9b7764ebef67461816e10",
    "FALLBACK-158": "e8114efaa8fa678db6a26bb6e4ffb926fc2c1a15a978e3d589cf918ff17ae6cb",
    "P-i": "cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e",
    "booking_census": "73ebc5db15aa1df86ccacd802fc13ad5a034337bf4eede53591cbceae34ae794",      # PINS.2
    "math_rules": "3b1e2d014411cb314d5cbf42ea40773dbcfa3de242f13d3a1d31eb830643b62d",          # v1.12 § A.2
    "TA-X-09_rowset": "0e826ee093b98767901271c95e918a19e1c6d5b8a8663c99c87d8ced17086e78",      # v1.12 § A.2
    "H9_NOTE": "90717b83926f06b5939a48c01c0cc4973d5f20d7d7eb60007b976d01ebde53e5",
    "H9_W1": "c68fcd3c133c8b8a55d75e85425876fe73d6d1752dfdd1cd21fa9041e87a24ff",
    "H9_MPOL2": "2aedf43f2091d0c575af1d7d07deb0278be87f0b4c917efa5c33d01e77707f61",
    "H9_W1NULL": "90b9ea619e8adfd3f8532cc55e16990c15348dd537071c5758000c2edafdf801",
    "H9_SCRIPT": "eede32e85f362b5d57b136b81344cae1bfd4b804515db2d6f2d66279d1920f55",
    "H10_receipt": "a0ad8246ac49628f8bd729c8cc2fba564b6456c4c06df0ae300e0439bfc447c9",
}
A8_ROWSETS = {   # v1.12 § B.1a (carried)
    "M0": "68549af0608cb9979771fcc4955ae8010f4f3516ad55a97b83922c994f571d12",
    "M-POL-2": "e698d5f555a37fcc12e703343286d4e25c12662d8cd35c9571f9a0ac8ae45dbf",
    "M-POL-2-NULL": "4393a14b56a97960ef42e73909a1cdefc49f3dc1a4cc41e7f20267b661a1a7b6",
    "W1": "5188284d198c139422276e8ac92f9a0bee03cea7dbb1cea32c6c7bf1d19a55e8",
    "W1-NULL": "b2abff6978105bfc1566d678d5f1dea756ea9ef0eab02f8457821f81125a7fdd",
    "setup_C": "207ab21f853b18ca026327bf6c9ddc4afa705d29cd3ef0868c1e7818d1672b4c",
}
# v1.13 § F.2m.2, pinned. Typed here AND re-derived from waves.json by its law below; the two must agree.
V11_PIN = [5, 5, 5, 4, 4, 5, 5, 5, 5, 4]
P06KEY_PIN = [0, 1, 1, 0, 1, 1, 1, 1, 0, 1]
W1_BOUND = 43.758085029822276             # TA-X-10 (v1.12 § F.2)
EXTENTS = 8.0                             # TA-X-17 (v1.12 § F.2)
TA18_BITS = ["c00fffffffffffde", "be9777a5cf72cec6"]   # TA-X-18 (v1.12 § A.2 / § F.2l)
TA29_W159 = {"aetherial_fleshhulk_mine": 3.542988, "beetle_maggot01": 3.366517, "chthonianrylok_ekketzul": 3.59875,
             "chthonianservitor_lunalvalgoth": 2.546547, "humanwendigo_darkwood_01": 3.784114,
             "korvaakmessenger_02": 3.033476, "korvaakmessenger_02b": 3.034357, "manticore_jaggedwaste_01": 2.956584,
             "rokwind_01": 3.362895, "skeletalgolem_stepsoftorment_01": 3.120862, "statue_templeguardian_02": 1.960798,
             "statue_templeguardian_03": 1.960798, "stonegryphon_templeguardian_01": 2.762796,
             "wendigo_ancient_namadea": 4.077782, "witchgod_finalboss": 3.978465, "yeti_rimehorn_01": 3.080011}
TA29_W160 = {"aetherialcolossus_galakros": 3.80807, "statue_korvaaktombguardian": 4.102804,
             "wendigocannibal_h01": 5.951244, "wendigocannibal_h02": 5.946459, "wendigocannibal_h03": 5.476449,
             "wendigocannibal_h04": 5.429514, "wendigocannibal_h05": 5.429514, "nemesis_aetherial_01": 8.165613,
             "nemesis_aetherialvanguard_01": 6.466635, "nemesis_beast_01_p1": 3.829365, "nemesis_beast_02": 2.689026,
             "nemesis_chthonian_02": 5.55761, "nemesis_chthonianvoidborn_01": 4.653725, "nemesis_kymon_01": 3.474869,
             "nemesis_kymon_02": 1.075958, "nemesis_orderdeathsvigil_01": 6.944508,
             "nemesis_orderdeathsvigil_02": 3.658935, "nemesis_outlaw_01": 6.146017, "nemesis_outlaw_02": 5.388859,
             "nemesis_undead_01": 3.822594, "nemesis_undead_02b": 5.470426, "nemesis_wendigo_01": 6.06632,
             "nemesis_wendigo_02": 4.391011}
ORACLE_TERMINALS = {"M-POL-2": [156, 152, 155, 152, 152], "W1": [156, 152, 155, 152, 155]}   # v1.12 § B.1a
TALLY = ["CHANNELLING", "CHANNELLING_AND_MOVING", "MOVING", "IDLE"]                           # D (v1.1 § C.1)

# jack-ryan's H-7 read, Item 2 (collab 9e1b19872), transcribed row by row for the § G.1a item-5 reconciliation
JR_READ = {r: "GREEN" for r in EXACT}
JR_READ["TA-X-17"] = "GREEN-BY-CONSTRUCTION"
JR_READ.update({"P-1": "GREEN", "P-2": "GREEN", "P-3": "GREEN", "P-4": "GREEN", "P-5": "GREEN", "C1": "CONFORMING"})
JR_PINNED_GRADER = {"TA-X-29": "RED (clause b: a dict field tested as a bool)",
                    "TA-X-17": "UNGRADEABLE (a grep for a typed 8.0 where the port reads arena.json)"}


def git_bytes(path: str, rev: str = REV, repo: str = GODOT) -> bytes:
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True, capture_output=True).stdout


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fsha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def tree_law(lines) -> str:
    return sha("\n".join(sorted(lines)).encode("utf-8"))


def set_digest(s) -> str:
    return sha("\n".join(sorted(s)).encode("utf-8"))


def ls_tree(rev: str, prefix: str) -> list:
    out = subprocess.run(["git", "-C", GODOT, "ls-tree", "-r", "--name-only", rev, prefix + "/"],
                         check=True, capture_output=True, text=True).stdout.split()
    return sorted(t[len(prefix) + 1:] for t in out)


# ======================================================================================== 1 · EVIDENCE
def verify_folder(rev: str, ev: str, pins: dict) -> dict:
    man_b = git_bytes(f"{ev}/MANIFEST.json", rev)
    man = json.loads(man_b)
    bad, lines = [], []
    for m in man["members"]:
        b = git_bytes(f"{ev}/{m['path']}", rev)
        disk = (Path(GODOT) / ev / m["path"]).read_bytes()
        if sha(b) != m["sha256"] or len(b) != m["bytes"] or disk != b:
            bad.append(m["path"])
        lines.append(f"{m['path']}  {sha(b)}")
    tracked = ls_tree(rev, ev)
    members = sorted(m["path"] for m in man["members"])
    o = {"MANIFEST_sha256": sha(man_b), "members": len(members), "member_failures": bad,
         "tree_recomputed": tree_law(lines), "tree_manifest": man["tree_digest"],
         "tracked_minus_members": [t for t in tracked if t not in members],
         "members_minus_tracked": [t for t in members if t not in tracked],
         "ta_manifest_sha256": sha(git_bytes(f"{ev}/ta_manifest.json", rev)),
         "ta_verdict_sha256": sha(git_bytes(f"{ev}/ta_verdict.json", rev)),
         "pinned_harness_files": man.get("⚑ pinned_harness_files"),
         "filing_checks_all": (man.get("⚑ filing_checks") or {}).get("all"),
         "run_record": man.get("run_record")}
    o["ok"] = (not bad and o["tree_recomputed"] == man["tree_digest"] and o["tracked_minus_members"] == ["MANIFEST.json"]
               and not o["members_minus_tracked"] and o["MANIFEST_sha256"] == pins["MANIFEST"]
               and o["ta_manifest_sha256"] == pins["ta_manifest"] == o["pinned_harness_files"]["ta_manifest.json"]
               and o["ta_verdict_sha256"] == pins["ta_verdict"] == o["pinned_harness_files"]["ta_verdict.json"]
               and o["filing_checks_all"] is True)
    return o


def verify_evidence() -> dict:
    out = {"prereg_sha256": fsha(PREREG), "prereg12_sha256": fsha(PREREG12)}
    out["prereg_ok"] = out["prereg_sha256"] == PIN["prereg_v1.13"] and out["prereg12_sha256"] == PIN["prereg_v1.12"]
    out["attempt"] = verify_folder(REV, EV, {"MANIFEST": PIN["emission_MANIFEST"], "ta_manifest": PIN["ta_manifest"],
                                             "ta_verdict": PIN["ta_verdict"]})
    out["preread"] = verify_folder(REV_PR, EV_PR, {"MANIFEST": PIN["preread_MANIFEST"],
                                                   "ta_manifest": PIN["preread_ta_manifest"],
                                                   "ta_verdict": PIN["preread_ta_verdict"]})
    out["preread_unchanged_4833bcf_to_7a97716"] = subprocess.run(
        ["git", "-C", GODOT, "diff", "--quiet", REV_PR, REV, "--", EV_PR]).returncode == 0

    # runtime tree d03ca891: recomputed from kc2_runtime/MANIFEST.json over git blobs at REV, unchanged vs 0f36826
    rman = json.loads(git_bytes("kc2_runtime/MANIFEST.json"))
    rl, rbad = [], []
    for m in rman["members"]:
        g = sha(git_bytes("kc2_runtime/" + m["path"]))
        if g != m["sha256"]:
            rbad.append(m["path"])
        rl.append(f"{m['path']}  {g}")
    rtracked = ls_tree(REV, "kc2_runtime")
    rmembers = sorted(m["path"] for m in rman["members"])
    same = subprocess.run(["git", "-C", GODOT, "diff", "--quiet", REV_RT, REV, "--", "kc2_runtime/"]).returncode == 0
    same_pr = subprocess.run(["git", "-C", GODOT, "diff", "--quiet", REV_PR, REV, "--", "kc2_runtime/"]).returncode == 0
    rt = tree_law(rl)
    out["runtime_tree"] = {"recomputed": rt, "manifest_says": rman["tree_digest"], "n_members": len(rmembers),
                           "member_failures": rbad, "tracked_not_member": [t for t in rtracked if t not in rmembers],
                           "member_not_tracked": [m for m in rmembers if m not in rtracked],
                           "unchanged_0f36826_to_7a97716": same, "unchanged_4833bcf_to_7a97716": same_pr,
                           "booking_census_file": sha(git_bytes("kc2_runtime/tests/kc2rt_booking_census.gd"))}
    out["runtime_tree"]["ok"] = (rt == rman["tree_digest"] == PIN["runtime_tree"] and not rbad and same and same_pr
                                 and out["runtime_tree"]["booking_census_file"] == PIN["booking_census"]
                                 and not out["runtime_tree"]["member_not_tracked"])

    # the H-7 read: the worktree file, its committed blob at 9e1b19872, and the harness's finding_sha256
    h7_blob = subprocess.run(["git", "-C", str(COLLAB), "show",
                              f"{H7_COMMIT}:agentic_orchestration/qa/findings/{H7.name}"],
                             check=True, capture_output=True).stdout
    out["H7_read"] = {"file_sha256": fsha(H7), "blob_sha256_at_9e1b19872": sha(h7_blob)}
    out["H7_read"]["ok"] = out["H7_read"]["file_sha256"] == out["H7_read"]["blob_sha256_at_9e1b19872"] == PIN["H7_read"]

    # G3 input (KP-184) and the (L2) operand file
    out["g3_MANIFEST_sha256"] = sha(git_bytes(f"{G3DIR}/MANIFEST.json"))
    out["l2_operands_jsonl_sha256"] = sha(git_bytes(f"{G3DIR}/l2_operands_25cell.jsonl"))
    out["g3_ok"] = (out["g3_MANIFEST_sha256"] == PIN["g3_MANIFEST"]
                    and out["l2_operands_jsonl_sha256"] == PIN["l2_operands_jsonl"])

    def pack(d: Path, sub: str) -> dict:
        pm = json.loads((d / "manifest.json").read_text())
        pl, pbad = [], []
        for m in pm["members"]:
            p = d / m["path"]
            g = fsha(p)
            if g != m["sha256"] or p.stat().st_size != m["bytes"]:
                pbad.append(m["path"])
            pl.append(f"{m['path']}  {g}")
        disk = sorted(str(p.relative_to(d)) for p in (d / sub).rglob("*") if p.is_file())
        return {"digest": tree_law(pl), "manifest_digest": pm["pack_digest"], "n": len(pm["members"]),
                "failures": pbad, "disk_equals_manifest": disk == sorted(m["path"] for m in pm["members"]),
                "cross_pin": (pm.get("cross_pin") or {}).get("model_pack_digest")}
    mp, rp = pack(MODEL, "model"), pack(REFP, "reference")
    out["model_pack"], out["reference_pack"] = mp, rp
    out["math_rules_sha256"] = fsha(MODEL / "model/math_rules.json")
    out["packs_ok"] = (mp["digest"] == mp["manifest_digest"] == PIN["model_pack"] and not mp["failures"]
                       and mp["disk_equals_manifest"] and rp["digest"] == rp["manifest_digest"] == PIN["reference_pack"]
                       and not rp["failures"] and rp["disk_equals_manifest"] and rp["cross_pin"] == PIN["model_pack"]
                       and out["math_rules_sha256"] == PIN["math_rules"])

    h9 = COLLAB / "agentic_orchestration/gamora/analyses/2026-09-30-kc2-play-h9-w1-containment"
    docs = {}
    for k, p in {"H9_NOTE": h9 / "NOTE.md", "H9_W1": h9 / "h9_out_W1.json", "H9_MPOL2": h9 / "h9_out_M-POL-2.json",
                 "H9_W1NULL": h9 / "h9_out_W1-NULL.json", "H9_SCRIPT": h9 / "h9_w1_containment.py",
                 "H10_receipt": OUT / "kc2-baton-v3-cut-receipt-v3p7p1-20261001_021247.json"}.items():
        docs[k] = {"sha256": fsha(p) if p.exists() else None}
        docs[k]["ok"] = docs[k]["sha256"] == PIN[k]
    out["h9_h10_docs"] = docs
    out["engine"] = {"HEAD": subprocess.run(["git", "-C", str(ENGINE), "rev-parse", "HEAD"], capture_output=True,
                                            text=True).stdout.strip(),
                     "oracle_tree_porcelain": subprocess.run(
                         ["git", "-C", str(ENGINE), "status", "--porcelain", "--", "src/reincarnated/simulation/kc2",
                          "src/reincarnated/export", "src/reincarnated/simulation/scripts"],
                         capture_output=True, text=True).stdout.strip()}
    return out


# ======================================================================================== 2 · PACK-DERIVED EXPECTED VALUES
def pack_derivations() -> dict:
    model = MODEL / "model"
    waves = json.loads((model / "waves.json").read_text())
    keys_on = {w: {r["spawn_point"] for r in waves["pools"]["wave_spawn"] if r["global_wave"] == w}
               for w in range(151, 161)}
    v11 = [len(keys_on[w] - {6}) for w in range(151, 161)]
    p06 = [1 if 6 in keys_on[w] else 0 for w in range(151, 161)]
    # TA-X-27(d) / (b): the 139 (wave, point, pool) min/max pairs of wave_spawn_count, waves 151-160
    pairs = defaultdict(dict)
    for r in waves["pools"]["wave_spawn_count"]:
        if 151 <= r["global_wave"] <= 160:
            pairs[(r["global_wave"], r["spawn_point"], r["pool_record"], r.get("pool_kind"))][r["bound"]] = r["value"]
    plist = [(int(pairs[k]["min"]), int(pairs[k]["max"])) for k in sorted(pairs)]
    mr = json.loads((model / "math_rules.json").read_text())
    five = ["RULE-CHANNEL-MOVEMENT", "RULE-RELEASE-TYPE-A", "RULE-RELEASE-TYPE-B",
            "RULE-CAST-INTERRUPT-BINDING-EXCLUSIVITY", "RULE-DMG-APPLIED"]
    vecs, vec_meta = [], []
    for rule in mr["rules"]:
        if rule["rule_id"] in five:
            for i, v in enumerate(rule["test_vectors"]):
                vecs.append(v)
                vec_meta.append((rule["rule_id"], i, v))
    rowset = sha(json.dumps(vecs, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8"))
    z5 = mr["⚑ v3p4p2_rows"]["z5_global_magnitude_law"][0]
    c5 = mr["⚑ v3p6_rows"]["c5_global_fold_composition"][0]
    zv, cv = z5["value"], c5["value"]
    mo = json.loads((model / "monster_offense.json").read_text())
    z3 = {r["value"]["wave"]: r["value"]["M_inst"] for r in mo["⚑ v3p4p2_rows"]["z3_wave_damage_modifier_check"]}
    arena = json.loads((model / "arena.json").read_text())
    kit = json.loads((model / "player_kit.json").read_text())
    return {"V11-P06-1": v11, "P06-KEY": p06, "sum_v11": sum(v11), "sum_on": sum(len(keys_on[w]) for w in keys_on),
            "vector_equals_pin": v11 == V11_PIN and p06 == P06KEY_PIN,
            "pairs": plist, "n_pairs": len(plist), "n_degenerate": sum(1 for lo, hi in plist if lo == hi),
            "ta09_rowset": rowset, "ta09_n": len(vecs), "ta09_vectors": vec_meta,
            "z5_value_keys_missing_in_c5": [k for k in zv if k not in cv],
            "z5_value_keys_differing_in_c5": [k for k in zv if k in cv and zv[k] != cv[k]],
            "c5_value_keys_added": [k for k in cv if k not in zv],
            "c5_points_to": mr["⚑ v3p6_points_to"].get("Z5-LAW"),
            "z5_composition_order": zv.get("composition_order"),
            "z3_M_inst": z3, "arena_placement_extents_m": arena["placement_extents_m"]["value"],
            "kit_channel_radius_m": kit["channel"]["radius_m"]["value"]}


# ======================================================================================== 3 · SET DIGESTS (oracle)
def set_digests() -> dict:
    sys.path.insert(0, str(ENGINE / "src"))
    cwd = os.getcwd()
    os.chdir(ENGINE)
    try:
        from reincarnated.export.kc2_baton_v3p5p1_schema import pool466
        from reincarnated.simulation.kc2 import threat, pool_lift
        from reincarnated.simulation.kc2.winner_surface import WinnerSurfaceFold
        from reincarnated.simulation.kc2.c11a_corrections import C11aLoader, AuraScope
        tree = {"model/waves.json": json.loads((MODEL / "model/waves.json").read_text())}
        pool, routes_agree = pool466(tree)
        ws = WinnerSurfaceFold.from_x8("src/reincarnated/simulation/output/"
                                       "kc2-lifted-rows-KC2PLAY-SEALLAP-W1-c2-energy-fold-20260928_232836.json")
        roster, _pets, _rep = threat.load_profiles(dot_corrections=True, winner_surface=ws,
                                                   pool_lift=pool_lift.load(), c11a=C11aLoader(scope=AuraScope.CLASS))
        cs = {}
        for k, v in roster.items():
            s = v.can_swing
            cs[k.lower()] = bool(s() if callable(s) else s)
        swing = {r for r in pool if cs.get(r)}
        nonswing = pool - swing
    finally:
        os.chdir(cwd)
    return {"POOL-466": {"n": len(pool), "digest": set_digest(pool), "routes_agree": routes_agree},
            "SWING-456": {"n": len(swing), "digest": set_digest(swing)},
            "NONSWING-10": {"n": len(nonswing), "digest": set_digest(nonswing)},
            "FALLBACK-158": {"note": "not recomputed by this grade (no graded row reads it); v1.12 PINS value carried",
                             "pin": PIN["FALLBACK-158"]},
            "_sets": {"POOL": sorted(pool), "SWING": sorted(swing), "NONSWING": sorted(nonswing)}}


# ======================================================================================== 4 · (L2), exact rationals
U = Fr(1, 2 ** 53)
TOL = Fr(1, 10 ** 12)
K7 = ["offered", "applied", "dropped", "voided", "pool_truncated", "pcl_reclaim", "counterplay_absorbed"]


def gamma(k: int) -> Fr:
    k = max(k, 0)
    assert k * U < 1
    return k * U / (1 - k * U)


def g2(n: int) -> Fr:
    return gamma(n - 1) ** 2 if n >= 2 else Fr(0)


def l2_cell(lo: dict) -> dict:
    """v1.12 § F.2k (L2), from a cell's own emitted operands (gamora's attempt-1 law, unchanged)."""
    n, q, NI, tot = lo["n"], lo["q"], lo["N_inner"], lo["inner_totals"]
    lossless = all(repr(float(s)) == s for s in list(lo["A_hat"].values()) + list(lo["A_hat_inner"].values())
                   + [lo["offered"]])
    ah = {k: Fr(float(lo["A_hat"][k])) for k in K7}
    ahi = {I: Fr(float(lo["A_hat_inner"][I])) for I in ("stream", "pcl")}
    O = Fr(float(lo["offered"]))
    ap = {k: ah[k] / (1 - U - g2(n[k])) for k in K7}
    api = {I: ahi[I] / (1 - U - g2(tot[I + "_terms"])) for I in ("stream", "pcl")}
    cc = lo["census_counters"]
    fmax = max(cc["pkt_rows_max"] + 4, 2 * cc["dot_buckets_max"], 2 * cc["burn_n_due_max"] + 3)
    phi = gamma(2 * fmax)
    B = (sum((U + g2(n[k])) * ap[k] for k in K7)
         + (U + gamma(5) ** 2) * sum((1 + U + g2(n[j])) * ap[j] for j in K7[1:])
         + sum((U + g2(NI[I])) * api[I] for I in ("stream", "pcl"))
         + phi * sum(ap[k] for k in K7 if q[k] > 0))
    beta = (1 + U) ** 2 * B / max(Fr(1), abs(O))
    return {"beta": float(beta), "holds": beta <= TOL and lossless and lo["final_sum_n_terms"] == 6
            and lo["sink_terms_present"] == 6 and cc["n_unbound_pcl_rows"] == 0, "margin": float(TOL / beta)}


# ======================================================================================== 5 · SOURCE READS (TA-X-17/19/21/24)
def source_reads() -> dict:
    def src(p):
        return git_bytes("kc2_runtime/" + p).decode("utf-8")
    laws, board, rng, fight = src("sim/kc2rt_laws.gd"), src("sim/kc2rt_board.gd"), src("sim/kc2rt_rng.gd"), src("sim/kc2rt_fight.gd")
    lines = lambda s, pat: [(i + 1, l.strip()) for i, l in enumerate(s.splitlines()) if re.search(pat, l)]
    o = {}
    o["TA-X-17"] = {"law_line": lines(laws, r"var rho := extents_m \* u2"),
                    "f64_returns": lines(laws, r"return PackedFloat64Array\(\[rho \* cos\(theta\), rho \* sin\(theta\)\]\)"),
                    "placement_sites": lines(board, r"scatter_polar_uniform_rho_f64\(u1, u2, placement_extents_m"),
                    "extents_halt": lines(board, r"float\(pe\) != placement_extents_m"),
                    "randf_at": lines(rng, r"return _rng\.randf\(\)")}
    # TA-X-19: the deferred-arrival packet. ⚑ r1 of this read (pre-commit, printed in the grade): the first version
    # searched for the packet literal inside `_defer_arrivals` only; the packet is BUILT in `_land_attack_packet`
    # and CONSUMED in `_defer_arrivals`. The read below covers the build site, the arrival loop and the landing
    # functions it calls (`_cp_absorb`, `_land`), and looks for any position read in the arrival path.
    def fn_body(name):
        m = re.search(r"\nfunc " + re.escape(name) + r"\(.*?(?=\nfunc |\Z)", fight, re.S)
        return m.group(0) if m else ""
    pos_pat = r'(\bpx\b|\bpy\b|position|_dist_to_player|\.distance_to|"x"|"y")'
    build = [l.strip() for l in fight.splitlines() if re.search(r'_defer_queue\[at\] as Array\)\.append\(\{"seq"', l)]
    build_i = [i for i, l in enumerate(fight.splitlines()) if re.search(r'_defer_queue\[at\] as Array\)\.append\(\{"seq"', l)]
    packet = " ".join(fight.splitlines()[i].strip() + " " + fight.splitlines()[i + 1].strip() for i in build_i)
    keys = re.findall(r'"([A-Za-z_]+)"\s*:', packet)
    arrival = {n: [l.strip() for l in fn_body(n).splitlines() if re.search(pos_pat, l.split("#", 1)[0])]
               for n in ("_defer_arrivals", "_cp_absorb", "_land")}
    o["TA-X-19"] = {"_defer_arrivals_line": lines(fight, r"^func _defer_arrivals\("),
                    "packet_build_lines": build, "packet_keys": keys,
                    "position_keys_in_packet": [k for k in keys if re.fullmatch(r"px|py|pos|position|xy|x|y", k)],
                    "position_reads_in_arrival_path": arrival,
                    "cast_time_distance (latency only)": [l.strip() for l in fn_body("_land_attack_packet").splitlines()
                                                          if "_dist_to_player" in l]}
    # TA-X-21: no bare round( on the port (my own scan; comments stripped; the quantisation home exempt)
    files = [f for f in ls_tree(REV, "kc2_runtime") if f.endswith(".gd")]
    viol = []
    for f in files:
        if f == "sim/kc2rt_quant.gd":
            continue
        for i, l in enumerate(src(f).splitlines()):
            code = l.split("#", 1)[0]
            code = re.sub(r'"(?:[^"\\]|\\.)*"', '""', code)
            if re.search(r"(?<![A-Za-z0-9_])round\(", code):
                viol.append(f"{f}:{i + 1}: {l.strip()}")
    o["TA-X-21_port_scan"] = {"gd_files": len(files), "exempt": "sim/kc2rt_quant.gd", "bare_round_sites": viol}
    eng = ENGINE / "src/reincarnated/simulation/kc2/threat.py"
    tl = eng.read_text().splitlines()
    o["TA-X-21_oracle"] = {"threat_py_sha256": fsha(eng),
                           "round_lines": [(i + 1, l.strip()) for i, l in enumerate(tl) if "round(" in l]}
    # TA-X-24: every sha256 call site on the port's sim path
    sims = [f for f in files if f.startswith("sim/") or f.startswith("loader/")]
    o["TA-X-24_sha256_sites"] = [f"{f}:{i}: {t}" for f in sims for i, t in lines(src(f), r"sha256") if "#" not in t[:2]]
    return o


# ======================================================================================== 6 · ROWS
def load(rev: str, ev: str):
    cells = {(a, s): json.loads(git_bytes(f"{ev}/{a}/{s}/cell.json", rev)) for a in ARMS for s in SALTS}
    man = json.loads(git_bytes(f"{ev}/ta_manifest.json", rev))
    ver = json.loads(git_bytes(f"{ev}/ta_verdict.json", rev))
    return cells, man, ver


def short(rec: str) -> str:
    return rec.rsplit("/", 1)[-1].removesuffix(".dbr")


def K(k) -> str:
    return f"{k[0]}|{k[1]}"


def grade(cells: dict, man: dict, ver: dict, sets: dict, pk: dict, srcr: dict) -> dict:
    R = {}
    pre = man["preconditions"]

    # ---------------- preconditions
    p1 = pre["P1_coverage"]
    R["P-1"] = {"verdict": "GREEN" if (p1["mapped"] == p1["total"] == 89 and p1["unmapped"] == 0 and p1["closes"]
                                       and p1["counts"].get("UNMAPPED", 0) == 0) else "RED",
                "values": {"mapped": p1["mapped"], "total": p1["total"], "unmapped": p1["unmapped"], "counts": p1["counts"],
                           "refusals": p1["refusals"]}}
    p2 = pre["P2_stream_disjointness"]
    wf = p2["with_noop_fold"]
    ctr = p2["controls"]
    # § B.3a (1) a real inserted fold, invoked every tick, forked through fork_stream ahead of a live fold
    c1_ = (wf["fold"]["inserted"] and wf["fold"]["n_forks"] == 1 and wf["fold"]["n_invocations"] == p2["population"]["ticks_observed"][1]
           and "fork_stream" in wf["fold"]["stream"] and "forked FIRST" in wf["fold"]["stream"])
    # (2) a measured zero
    c2_ = wf["own_stream_draws_measured"] == 0 and wf["fold"]["own_stream_draws"] == 0 and wf["fold"]["n_shared_stream_draws"] == 0
    # (3) one digest function, zero-draw = absent; digests identical
    c3_ = ("cell_digest" in p2["digest_function"] and "zero-draw site = absent site" in p2["digest_function"]
           and p2["digest_plain"] == p2["digest_with_noop_fold"] == wf["digest"])
    # (4) controls (a), (a0), (b) from the emission: none GREEN, and each one's digest perturbed (the digest clause fires)
    ctl = {k: {"state": v["state"], "digest_identical": v["digest_identical"], "reasons": v["reasons"]} for k, v in ctr.items()}
    c4_emitted = (len(ctr) == 3 and all(v["state"] != "GREEN" and v["digest_identical"] is False for v in ctr.values()))
    # (c): not built by the T-A harness; the committed probe kc2rt_attempt2_probes.gd (a member of d03ca891) was run by
    # jack-ryan at this runtime FILE (H-3 INFO-C, collab ff6ea9fe6): RED as required. Carried as his evaluation of record.
    c4_c = "RED at d03ca891 (jack-ryan H-3 INFO-C, collab ff6ea9fe6; probe kc2rt_attempt2_probes.gd, a runtime member)"
    # (5) fresh pack per leg; the plain leg and every graded cell carry no fold key / probe site
    probe_sites = [K(k) for k in ALLC for s in cells[k]["draw_sites"]["per_site"]
                   if re.search(r"NOOP|p2_noop|P2", s["draw_site_id"])]
    c5_ = p2["fresh_pack_per_leg"] and p2["plain_leg_has_no_fold"] and not probe_sites
    R["P-2"] = {"verdict": "GREEN" if (c1_ and c2_ and c3_ and c4_emitted and c5_) else
                ("NOT RUN" if not (c1_ and c2_) else "RED"),
                "values": {"(1) real inserted fold": c1_, "(2) measured zero": c2_, "(3) one digest, identical": c3_,
                           "digest": p2["digest_plain"], "invocations": wf["fold"]["n_invocations"],
                           "ticks_observed": p2["population"]["ticks_observed"],
                           "(4) controls a/a0/b (emitted)": ctl, "(4) control (c)": c4_c,
                           "(5) fresh pack, no fold in plain leg or any graded cell": c5_, "probe sites in graded cells": probe_sites}}
    p3 = pre["P3_roll"]
    R["P-3"] = {"verdict": "GREEN" if (p3["population"] == "POOL-466" and p3["cardinality"] == 466
                                       and p3["law"] == {"alternative": "WEIGHTED:pool_weight", "name": "UNIFORM:randrange"})
                else "RED", "values": {k: p3[k] for k in ("population", "cardinality", "law")}}
    p4s = [cells[k]["⚑ P4_pack"] for k in ALLC] + [man["manifest_blocks_other"]["⚑ P4_pack"]]
    p4ok = all(p["verified"] and p["cross_pin"] and p["paired"] and p["mismatches"] == 0
               and p["model_pack"]["digest"] == PIN["model_pack"] and p["reference_pack"]["digest"] == PIN["reference_pack"]
               and p["cross_pin_model_pack_digest"] == PIN["model_pack"] for p in p4s)
    rh = ver["runtime_header"]
    rh_ok = (rh["read_by_running"] and rh["equals_P4"] and rh["model_pack_digest"] == PIN["model_pack"]
             and rh["reference_pack_digest"] == PIN["reference_pack"] and rh["p4_cross_pin"]
             and rh["runtime_tree_digest_vendored"]["tree_digest"] == PIN["runtime_tree"]
             and rh["vendored_runtime_equals_runtime_digest"])
    R["P-4"] = {"verdict": "GREEN" if p4ok and rh_ok and man["pack_digest"] == PIN["model_pack"] else "RED",
                "values": {"P4 blocks verified (25 cells + manifest)": p4ok, "n_blocks": len(p4s),
                           "runtime_header ok": rh_ok, "binary_sha256": rh["binary_sha256"],
                           "harness_measured_pack": man["pack_digest"]}}
    p5 = man["manifest_blocks_other"]["⚑ P5_folds"]
    p5_expect = {"winner_surface": "ARMED", "insufficient_energy_policy": "REFUSE", "regen_ungated": True,
                 "global_magnitude": "ARMED_UNCONDITIONAL", "measured_board_attached": True,
                 "per_cast_energy_column": "PARENT_PLUS_MODIFIER", "monster_march_base_m_per_s": 3.209466,
                 "pcl_limb": "MULTIPLICATIVE @ 26.0 %",
                 "monster_run_speed_population": "LAPR-MEASURED 128 · BANDA-DB-CITED 180 · FALLBACK 158"}
    p5_ok = (all(p5.get(k) == v for k, v in p5_expect.items())
             and all(t in p5["loader_call"] for t in ("dot_corrections=True", "winner_surface=ARMED", "pool_lift=ARMED",
                                                       "C11aLoader(CLASS)"))
             and all(t in p5["non_health_route"] for t in ("Disruption", "ManaBurnDrain", "PierceRatio"))
             and "POOL-466" in p5["pool_lift"] and "SWING-456" in p5["pool_lift"] and "NONSWING-10" in p5["pool_lift"]
             and "C3 NOT FOLDED" in p5["c11a"] and "CLASS" in p5["c11a"] and "C4" in p5["c11a"]
             and all(cells[k]["⚑ P5_folds"] == p5 for k in ALLC))
    R["P-5"] = {"verdict": "GREEN" if p5_ok else "RED", "values": p5}

    # ---------------- C1 conformance (§ B.1a, § G; § C.9.5a)
    ac = man["arm_config_a8"]
    g3c = ver["g3"]["per_cell"]
    c1 = {}
    for a in ARMS:
        c1[a] = {"rowset_eq_B1a": ac[a]["rowset"] == A8_ROWSETS[a],
                 "setup_C": ac[a]["setup_config_rowset"] == A8_ROWSETS["setup_C"],
                 "probe_rows_applied": ac[a]["setup_probe_rows_applied"], "configured_from_a8": ac[a]["configured_from_a8"],
                 "g3_5_salts": all(g3c[f"{a}|{s}"]["passes"] and g3c[f"{a}|{s}"]["injected"] == []
                                   and g3c[f"{a}|{s}"]["decision_divergences"] == 0 and g3c[f"{a}|{s}"]["draw_mismatches"] == 0
                                   and not g3c[f"{a}|{s}"]["port_only_streams"] and g3c[f"{a}|{s}"]["death"]["equal"]
                                   and g3c[f"{a}|{s}"]["census_equal"] is True
                                   and g3c[f"{a}|{s}"]["control_term"]["equal"] is True
                                   and g3c[f"{a}|{s}"]["control_term"]["port"] == g3c[f"{a}|{s}"]["control_term"]["oracle"]
                                   for s in SALTS)}
    du = ver["declared_ungradeable"]
    du_ok = [d.get("id") for d in du] == ["TA-X-06"]
    g3_sum = sum(g3c[K(k)]["control_term"]["port"] for k in ALLC)
    R["C1"] = {"verdict": "CONFORMING" if (all(v["rowset_eq_B1a"] and v["setup_C"] and v["probe_rows_applied"] == 0
                                               and v["configured_from_a8"] and v["g3_5_salts"] for v in c1.values())
                                           and ver["g3"]["all_25_pass"] and du_ok) else "NON-CONFORMING",
               "values": {"per_arm": c1, "declared_ungradeable": [d.get("id") for d in du],
                          "g3_control_term_sum_port": g3_sum,
                          "g3_control_term_sum_oracle": sum(g3c[K(k)]["control_term"]["oracle"] for k in ALLC)}}

    # ---------------- EXACT rows
    t1 = pre["⚑ TA-X-01_self_determinism"]
    m02 = [c["digest"] for c in man["cells"] if c["arm"] == "M0" and c["salt"] == 2]
    R["TA-X-01"] = {"verdict": "GREEN" if (t1["identical"] and t1["digest_run_1"] == t1["digest_run_2"] == m02[0]
                                         and t1["probe"].startswith("M0 salt 2")) else "RED",
                    "values": {"probe": t1["probe"], "run_1": t1["digest_run_1"], "run_2": t1["digest_run_2"],
                               "M0|2 cell digest": m02[0], "P-2 arm/salt": [p2["arm"], p2["salt"]]}}
    R["TA-X-02"] = {"verdict": R["P-1"]["verdict"], "values": f"{p1['mapped']}/{p1['total']}, unmapped {p1['unmapped']}"}

    # TA-X-03/04/05 on the per-cell cell_digest (§ B.3a digest law), from the manifest's 25 digests -- AND, independently,
    # on the digest's SUBJECT read off each cell (terminal, census state_counts, board counters, non-zero per-site draws)
    dig = {(c["arm"], c["salt"]): c["digest"] for c in man["cells"]}

    def subject(c):
        b = {k: v for k, v in c["board"].items() if not isinstance(v, (dict, list))}
        return json.dumps({"terminal": c["terminal"], "state_counts": c["census"]["state_counts"], "board": b,
                           "per_wave": c["board"]["per_wave"],
                           "draws": sorted((s["draw_site_id"], s["draws"]) for s in c["draw_sites"]["per_site"] if s["draws"])},
                          sort_keys=True)
    for rid, x, y, want_ident in [("TA-X-03", "M-POL-2-NULL", "M0", True), ("TA-X-04", "W1-NULL", "M-POL-2", True),
                                  ("TA-X-05", "M-POL-2", "M0", False)]:
        same_d = [dig[(x, s)] == dig[(y, s)] for s in SALTS]
        same_s = [subject(cells[(x, s)]) == subject(cells[(y, s)]) for s in SALTS]
        holds = all(same_d) if want_ident else (not all(same_d))
        R[rid] = {"verdict": "GREEN" if holds and same_d == same_s else ("RED" if not holds else "UNGRADEABLE"),
                  "values": {"compares": f"{x} vs {y}", "digest_identical_per_salt": same_d,
                             "subject_identical_per_salt (gamora)": same_s}}
    same6 = [dig[("W1", s)] == dig[("M-POL-2", s)] for s in SALTS]
    R["TA-X-06"] = {"verdict": "UNGRADEABLE-declared (Q83(b), KP-110)",
                    "values": f"W1 vs M-POL-2 identical on {sum(same6)}/5 salts {same6}"}

    # TA-X-07
    rho = {K(k): float(cells[k]["conservation"]["residual_relative"]) for k in ALLC}
    l2 = {K(k): l2_cell(cells[k]["conservation"]["l2_operands"]) for k in ALLC}
    jl = {}
    for line in git_bytes(f"{G3DIR}/l2_operands_25cell.jsonl").decode().splitlines():
        d = json.loads(line)
        jl[d.pop("cell")] = d
    ops_equal = sum(1 for k in ALLC if {kk: vv for kk, vv in cells[k]["conservation"]["l2_operands"].items()}
                    == {kk: vv for kk, vv in jl[K(k)].items() if kk in cells[k]["conservation"]["l2_operands"]}
                    and set(cells[k]["conservation"]["l2_operands"]) <= set(jl[K(k)]))
    rb = man["r11_bound"]
    a_ok = all(v <= 1e-12 for v in rho.values())
    c_ok = all(v["holds"] for v in l2.values()) and rb["all_25_hold"] and rb["probe_bitwise"]
    worst = max(l2.items(), key=lambda kv: kv[1]["beta"])
    R["TA-X-07"] = {"verdict": "GREEN" if a_ok and c_ok else ("RED" if not a_ok and c_ok else "UNGRADEABLE"),
                    "values": {"(a) max rho_hat": max(rho.values()), "(a) cells at 0.0": sum(v == 0.0 for v in rho.values()),
                               "(b) max |residual| (reported)": max(abs(float(cells[k]["conservation"]["residual"])) for k in ALLC),
                               "(c) gamora (L2), exact": {"all_25_hold": all(v["holds"] for v in l2.values()),
                                                          "worst": worst[0], "beta": worst[1]["beta"], "margin": worst[1]["margin"]},
                               "(c) operands == H-2's l2_operands_25cell.jsonl (b5bcdb7b)": f"{ops_equal}/25",
                               "(c) harness r11_bound": [rb["all_25_hold"], rb["probe_bitwise"]], "census": rb["census"]}}

    # TA-X-08 (v1.13 § F.2n.2 (1), (2) restated, (2p); § F.2o census convention)
    t8, fails8 = {}, []
    for k in ALLC:
        c = cells[k]
        tc = c["ta_x_08_counters"]
        sc = c["census"]["state_counts"]
        D = sum(sc.get(s, 0) for s in TALLY)
        PF = sc.get("PRE_FIGHT", 0)
        nch = sc.get("CHANNELLING", 0) + sc.get("CHANNELLING_AND_MOVING", 0)
        W = c["ta_x_16_counters"]["waves_played"]
        last = c["hp_trace"][-1]
        conv = {"one PRE_FIGHT per wave played": PF == len(W), "no DEAD": "DEAD" not in sc or sc["DEAD"] == 0,
                "lethal tick censused alive": (c["terminal"]["terminal_reason"] == "death" and last["hp"] <= 0.0
                                               and last["tick"] == c["terminal"]["run_tick"] == tc["n_player_ticks_observed"]),
                "no state outside the tally + PRE_FIGHT": set(sc) <= set(TALLY) | {"PRE_FIGHT"},
                "counters' D / PF = census": tc["D"] == D and tc["PRE_FIGHT"] == PF,
                "n_channelling = CHANNELLING + C&M": tc["n_channelling"] == nch}
        id1 = tc["n_player_ticks_observed"] == D + PF
        id2 = tc["n_channelling"] + tc["n_released"] + tc["n_control_suppressed_channelling"] == D
        id2p = tc["n_ticks_released"] == tc["n_released"] + tc["n_released_pre_fight"]
        m0 = (k[0] != "M0") or (tc["n_ticks_released"] == 0 and tc["n_released"] == 0 and tc["n_released_pre_fight"] == 0)
        ok = id1 and id2 and id2p and m0 and all(conv.values())
        if not ok:
            fails8.append(K(k))
        t8[K(k)] = {"observed": tc["n_player_ticks_observed"], "PRE_FIGHT": PF, "D": D, "waves_played": len(W),
                    "n_channelling": tc["n_channelling"], "n_released": tc["n_released"],
                    "n_control_suppressed_channelling": tc["n_control_suppressed_channelling"],
                    "n_ticks_released": tc["n_ticks_released"], "n_released_pre_fight": tc["n_released_pre_fight"],
                    "n_control_suppressed": tc["n_control_suppressed"],
                    "n_control_suppressed_released": tc["n_control_suppressed_released"],
                    "n_control_suppressed_pre_fight": tc["n_control_suppressed_pre_fight"],
                    "id1": id1, "id2": id2, "id2p": id2p, "M0_no_fold": m0, "census_convention": conv,
                    "harness_flags": [ver["ta_x_08"][K(k)]["id1_holds"], ver["ta_x_08"][K(k)]["id2_holds"],
                                      ver["ta_x_08"][K(k)]["id2p_holds"]]}
    R["TA-X-08"] = {"verdict": "RED" if fails8 else "GREEN", "values": {"fails": fails8, "per_cell": t8}}

    # TA-X-09
    t9 = man["ta_x_09"]
    want_pack = []
    for (rid, i, v) in pk["ta09_vectors"]:
        want_pack.append((rid, i, list(v["out"].values())[0] if isinstance(v["out"], dict) else v["out"]))
    em = [(v["rule_id"], v["vector_index"], v["want"], v["got"], v["verdict"], v["law_ok"], v["stored_ok"]) for v in t9["vectors"]]
    t9_ok = (pk["ta09_rowset"] == PIN["TA-X-09_rowset"] == t9["rowset"]["measured"] and t9["n"] == 9 == pk["ta09_n"]
             and len(em) == 9 and all(e[0] == w[0] and e[1] == w[1] and e[2] == w[2] and e[3] == e[2] and e[4] == "REPLAYED"
                                      and e[5] and e[6] for e, w in zip(em, want_pack))
             and t9["rowset"]["math_rules_file_sha256"] == PIN["math_rules"] and t9["all_replayed_to_the_law_and_the_stored_digits"])
    R["TA-X-09"] = {"verdict": "GREEN" if t9_ok else "RED",
                    "values": {"rowset (gamora, from the pack)": pk["ta09_rowset"], "rowset (emitted)": t9["rowset"]["measured"],
                               "per vector (rule, i, pack out, got)": [(w[0], w[1], w[2], e[3]) for e, w in zip(em, want_pack)]}}

    w1 = [cells[("W1", s)]["walls"]["max_body_radius_m"] for s in SALTS]
    R["TA-X-10"] = {"verdict": "GREEN" if all(v <= W1_BOUND for v in w1) and all(cells[("W1", s)]["walls"]["armed"] for s in SALTS)
                    else "RED", "values": {"W1 max_body_radius_m": w1, "bound": W1_BOUND}}
    cl = {K((a, s)): [cells[(a, s)]["walls"]["n_wall_clamps_player"], cells[(a, s)]["walls"]["n_wall_clamps_body"]]
          for a in ("W1", "W1-NULL") for s in SALTS}
    R["TA-X-11"] = {"verdict": "GREEN" if all(v == [0, 0] for v in cl.values()) else "RED", "values": cl}
    R["TA-X-12"] = {"verdict": "GREEN" if all(cells[k]["⚑ TA-X-12_pool_damage_total"] == 0.0 for k in ALLC) else "RED",
                    "values": [cells[k]["⚑ TA-X-12_pool_damage_total"] for k in ALLC]}
    R["TA-X-13"] = {"verdict": "GREEN" if all(cells[k]["⚑ TA-X-13_n_player_crits"] == 0 for k in ALLC) else "RED",
                    "values": [cells[k]["⚑ TA-X-13_n_player_crits"] for k in ALLC]}
    t14 = {K(k): [cells[k]["release"]["⚑ TA-X-14_do_not_1"]["cause_energy_count"], sorted(cells[k]["release"]["causes"]),
                  cells[k]["release"]["n_release_events"]] for k in ALLC}
    R["TA-X-14"] = {"verdict": "GREEN" if all(v[0] == 0 and set(v[1]) <= {"type_a", "type_b"} for v in t14.values()) else "RED",
                    "values": t14}
    ok15, n15 = True, 0
    for k in ALLC:
        t = cells[k]["⚑ TA-X-15_release_schedule"]
        for row in t["per_wave_per_point"]:
            n15 += 1
            want = [49] if row["point"] == 5 else [0]
            if row["release_ticks"] != want or row["point"] not in (1, 2, 3, 4, 5):
                ok15 = False
        if t["n_intra_point_staggers"] != 0 or t["staggers"] or t["p05_release_tick_expected"] != 49:
            ok15 = False
    R["TA-X-15"] = {"verdict": "GREEN" if ok15 else "RED",
                    "values": {"(wave, point) rows": n15, "(a) p01-p04 tick 0, p05 tick 49": ok15, "(b)": "GREEN-BY-CONSTRUCTION"}}

    # TA-X-16 (v1.13 § F.2m.3 (a)-(d), key grain, W = {151..T})
    v11, p06 = pk["V11-P06-1"], pk["P06-KEY"]
    t16, fails16 = {}, []
    for k in ALLC:
        c = cells[k]
        tc = c["ta_x_16_counters"]
        term = c["terminal"]
        T = 160 if term["terminal_reason"] == "cleared" else term["terminal_wave"]
        W = list(range(151, T + 1))
        idx = [w - 151 for w in W]
        pw = c["board"]["per_wave"]
        sched_pts = defaultdict(set)
        for row in c["⚑ TA-X-15_release_schedule"]["per_wave_per_point"]:
            sched_pts[row["wave"]].add(row["point"])
        a = (tc["waves_played"] == W and tc["terminal_wave"] == T
             and tc["pool_picks_per_wave"] == [v11[i] for i in idx]
             and [x["pool_picks"] for x in pw] == [v11[i] for i in idx] and [x["wave"] for x in pw] == W)
        b = tc["n_pool_picks"] == sum(v11[i] for i in idx) == c["board"]["n_pool_picks"]
        cc = (tc["n_spawn_point_6_keys_rolled"] == 0 and tc["n_spawn_point_6_keys_rolled_per_wave"] == [0] * len(W)
              and all(x["⚑ KP-180_p06_keys_rolled"] == 0 for x in pw) and all(6 not in sched_pts[w] for w in W))
        d = (tc["n_p06_keys_filtered_per_wave"] == [p06[i] for i in idx]
             and [x["⚑ KP-180_p06_keys_filtered"] for x in pw] == [p06[i] for i in idx]
             and tc["n_p06_keys_filtered"] == sum(p06[i] for i in idx))
        sched_cross = all(len(sched_pts[w]) <= v11[w - 151] for w in W)   # printed only: release rows are a subset of keys
        if not (a and b and cc and d):
            fails16.append(K(k))
        t16[K(k)] = {"T": T, "n_waves": len(W), "picks": tc["pool_picks_per_wave"], "n_pool_picks": tc["n_pool_picks"],
                     "expected_sum": sum(v11[i] for i in idx), "p06_rolled": tc["n_spawn_point_6_keys_rolled"],
                     "p06_filtered": tc["n_p06_keys_filtered_per_wave"], "a": a, "b": b, "c": cc, "d": d,
                     "schedule points <= keys (printed)": sched_cross, "harness_holds": ver["ta_x_16"][K(k)]["holds"]}
    R["TA-X-16"] = {"verdict": "RED" if fails16 else "GREEN",
                    "values": {"fails": fails16, "vector (gamora, from waves.json)": v11, "P06-KEY": p06,
                               "vector equals the § F.2m.2 pin": pk["vector_equals_pin"],
                               "harness vector": ver["ta_x_16"]["vector"]["V11-P06-1"], "per_cell": t16}}

    # TA-X-17: by source (no per-body statistic emitted), with the pack's extents
    s17 = srcr["TA-X-17"]
    ok17 = (len(s17["law_line"]) == 1 and len(s17["f64_returns"]) == 1 and len(s17["placement_sites"]) == 2
            and len(s17["extents_halt"]) == 1 and pk["arena_placement_extents_m"] == EXTENTS)
    R["TA-X-17"] = {"verdict": "GREEN-BY-CONSTRUCTION" if ok17 else "UNGRADEABLE",
                    "values": {"source": s17, "arena.json placement_extents_m": pk["arena_placement_extents_m"]}}

    x18 = man["ta_x_18"]
    parsed = [struct.pack(">d", float(s)).hex() for s in x18["emitted"]]
    lossless = (x18["emitter"] == "cpython-repr" and x18["roundtrip_probe"] and x18["lossless"]
                and all(repr(float(s)) == s for s in x18["emitted"]))
    R["TA-X-18"] = {"verdict": ("GREEN" if parsed == TA18_BITS else "RED") if lossless else "UNGRADEABLE",
                    "values": {"emitted": x18["emitted"], "gamora_parsed_bits": parsed, "emitter": x18["emitter"],
                               "repr(float(s)) == s": all(repr(float(s)) == s for s in x18["emitted"])}}
    s19 = srcr["TA-X-19"]
    ok19 = (bool(s19["_defer_arrivals_line"]) and len(s19["packet_build_lines"]) == 1
            and set(s19["packet_keys"]) == {"seq", "b", "rec", "direct", "pcl", "fams", "cast", "n_rows"}
            and not s19["position_keys_in_packet"] and not any(s19["position_reads_in_arrival_path"].values()))
    R["TA-X-19"] = {"verdict": "GREEN" if ok19 else "UNGRADEABLE", "values": s19}

    t20 = man["ta_x_20"]
    cases = {r["case"]: (r["expect"], r["got"], r["ok"]) for r in t20["rows"]}
    want20 = {"2.99": True, "3.01": False, "BEHIND": True, "12 bodies": 12}
    ok20 = (t20["radius_m"] == pk["kit_channel_radius_m"] == 3.0 and t20["failures"] == 0 and len(t20["rows"]) == 5
            and all(e == g and o for e, g, o in cases.values())
            and all(any(key in c and cases[c][0] == v for c in cases) for key, v in want20.items()))
    R["TA-X-20"] = {"verdict": "GREEN" if ok20 else "RED", "values": {"radius_m": t20["radius_m"], "cases": cases}}

    t21 = man["ta_x_21"]
    q = t21["quantisation"]
    # numeric rows: the port's value == the expected == CPython's round() (half-to-even); the two site-law rows
    # (CEIL / TRUNCATE) are asserted by the harness and carried as emitted
    q_ok = (q["failures"] == 0 and len(q["rows"]) == 12
            and all(r["ok"] and (("in" not in r) or r["got"] == r["expect"] == round(r["in"])) for r in q["rows"]))
    ol = t21["oracle_live_sites"]
    my_lines = [l for _, l in srcr["TA-X-21_oracle"]["round_lines"]]
    sites_ok = (ol["file_sha256"] == srcr["TA-X-21_oracle"]["threat_py_sha256"] and ol["re_verified"]
                and [c["site"] for c in ol["cited"]] == [f"threat.py:{n}" for n, _ in srcr["TA-X-21_oracle"]["round_lines"]]
                and [c["line_text"] for c in ol["cited"]] == my_lines and all("int(round(" in l for l in my_lines))
    scan_ok = (t21["no_bare_round_on_the_port"]["violations"] == 0 and t21["purity_scan"]["ok"]
               and not srcr["TA-X-21_port_scan"]["bare_round_sites"])
    R["TA-X-21"] = {"verdict": "GREEN" if q_ok and sites_ok and scan_ok else "RED",
                    "values": {"quantisation rows": len(q["rows"]), "rows ok (gamora: got == expect == python round)": q_ok,
                               "oracle round( sites (gamora, threat.py at engine HEAD)": srcr["TA-X-21_oracle"]["round_lines"],
                               "sites == emitted": sites_ok,
                               "port bare round( (harness / gamora)": [t21["no_bare_round_on_the_port"]["violations"],
                                                                       srcr["TA-X-21_port_scan"]["bare_round_sites"]],
                               "gd files scanned (gamora)": srcr["TA-X-21_port_scan"]["gd_files"]}}
    R["TA-X-22"] = {"verdict": "GREEN" if all(cells[k]["release"]["⚑ TA-X-22_flag_cause_count"] == 0 for k in ALLC) else "RED",
                    "values": [cells[k]["release"]["⚑ TA-X-22_flag_cause_count"] for k in ALLC]}
    R["TA-X-24"] = {"verdict": "GREEN" if man["v0_limb_set"]["phase_model"]["value"] == "PhaseModel.ENGAGE" else "RED",
                    "values": {"phase_model": man["v0_limb_set"]["phase_model"], "sha256 sites (read)": srcr["TA-X-24_sha256_sites"]}}

    pool, swing, nons = set(sets["_sets"]["POOL"]), set(sets["_sets"]["SWING"]), set(sets["_sets"]["NONSWING"])
    t25 = {}
    for k in ALLC:
        b = cells[k]["board"]["ta_x_25"]
        sbr = b["(c) spawn_by_record"]
        cnt = {"nodata_inert": 0, "measured_inert": 0, "measured_offense": 0}
        bad = [[], [], []]
        for rec, v in sbr.items():
            r = rec.lower()
            cnt[v["class"]] += v["n_bodies"]
            if r not in pool:
                bad[0].append(rec)
            if r in swing and v["class"] != "measured_offense":
                bad[1].append(rec)
            if r in nons and v["class"] not in ("nodata_inert", "measured_inert"):
                bad[2].append(rec)
        t25[K(k)] = {"a": b["(a) n_nodata_refused"] == 0,
                     "b": b["(b) n_nodata_spawn_inert"] + b["(b) n_measured_inert_spawn"] + b["(b) n_measured_offense_spawn"]
                     == b["(b) n_bodies_spawned"],
                     "c1": not bad[0], "c2": not bad[1], "c3": not bad[2],
                     "c4": (cnt["nodata_inert"] == b["(b) n_nodata_spawn_inert"] and cnt["measured_inert"] == b["(b) n_measured_inert_spawn"]
                            and cnt["measured_offense"] == b["(b) n_measured_offense_spawn"]),
                     "bodies": b["(b) n_bodies_spawned"]}
    R["TA-X-25"] = {"verdict": "GREEN" if all(all(v[x] for x in ("a", "b", "c1", "c2", "c3", "c4")) for v in t25.values()) else "RED",
                    "values": t25}

    t26 = man["manifest_blocks_other"]["ta_x_26"]
    t26b = man["ta_x_26_b"]
    e = t26["(e)"]
    ok26 = (t26["(a) join_consumption_audit"]["green"] and not t26["(a) join_consumption_audit"]["unaccounted"]
            and t26["(b) loaded"] and t26["(b) sha256_measured"] == PIN["P-i"] and t26b["sha256_of_loaded_bytes"] == PIN["P-i"]
            and t26b["agrees"]
            and t26["(c)"] == {"multipliers": 5, "records": 790, "rows": 7900, "tiers": 8, "wave_invariant": 790}
            and t26["(d)"]["formula_helper_call_sites"] == 1 and t26["(d)"]["formula_disagreements"] == 0
            and abs(e["mean"] - 0.2468965517) <= 5e-7 and abs(e["median"] - 0.25) <= 5e-7
            and abs(e["max"] - 0.35) <= 5e-7 and abs(e["min"] - 0.0) <= 5e-7 and e["n_zero"] == 17 and e["n"] == 464
            and all(sorted(cells[k]["⚑ V1-JOIN-1_leech_table"]["distinct_total_leech_resist_pct"])
                    == [65.0, 75.0, 83.0, 88.0, 105.0, 115.0, 565.0, 588.0] for k in ALLC))
    R["TA-X-26"] = {"verdict": "GREEN" if ok26 else "RED",
                    "values": {"(b) sha": t26b["sha256_of_loaded_bytes"], "(c)": t26["(c)"], "(d)": t26["(d)"], "(e)": e}}

    # TA-X-27: (a) emitted scan; (b) gamora's OWN CPython replay per seed against the port's emitted consumption;
    # (c) G3 draw rules at the graded digest + 29 live sites, p05 elided; (d) pack census, recomputed here
    t27, t27b = man["manifest_blocks_other"]["ta_x_27"], man["ta_x_27_b"]

    class _Cnt(random.Random):
        def __init__(self, seed):
            super().__init__(seed)
            self.n = 0

        def getrandbits(self, k):
            self.n += 1
            return super().getrandbits(k)
    per_seed = {}
    for ps in t27b["replay"]["per_seed"]:
        r = _Cnt(ps["seed"])
        cons, res = [], []
        for lo, hi in pk["pairs"]:
            b0 = r.n
            res.append(r.randint(lo, hi))
            cons.append(r.n - b0)
        per_seed[ps["seed"]] = {"gamora_cons == port_consumed": cons == ps["port_consumed"],
                                "gamora_results == port_results": res == ps["port_results"],
                                "gamora_words": sum(cons), "port_words": ps["port_words"]}
    b27 = (t27b["seeds"] == list(range(16)) and len(per_seed) == 16
           and all(v["gamora_cons == port_consumed"] and v["gamora_results == port_results"] and v["gamora_words"] == v["port_words"]
                   for v in per_seed.values()))
    g3ok = ver["g3"]["all_25_pass"] and all(v["draw_mismatches"] == 0 and not v["port_only_streams"]
                                            and {x.split("|")[0] for x in v["oracle_only_streams"]}
                                            <= {"spawn_structure.py:344", "player_kit_residual.py:286"}
                                            for v in ver["g3"]["per_cell"].values())
    a27 = t27["(a)"]["short_circuits_found"] == 0 and t27["(a)"]["unclassified"] == 0 and not t27["(a)"]["findings"]
    c27 = t27["(c)"]["registered_live_sites"] == 29 and "ELIDED" in t27["(c)"]["p05_draw"] and g3ok
    d27 = (t27["(d)"]["pairs"] == pk["n_pairs"] == 139 and t27["(d)"]["degenerate"] == pk["n_degenerate"] == 97)
    R["TA-X-27"] = {"verdict": "GREEN" if a27 and b27 and c27 and d27 else "RED",
                    "values": {"(a)": [t27["(a)"]["files_scanned"], t27["(a)"]["short_circuits_found"], t27["(a)"]["unclassified"]],
                               "(b) gamora replay (python %s)" % sys.version.split()[0]: per_seed,
                               "(b) harness python": t27b["python"], "(c)": [t27["(c)"], g3ok],
                               "(d) gamora from waves.json": [pk["n_pairs"], pk["n_degenerate"]]}}
    ok28 = all(cells[k]["leech_law"]["n_leech_target_caps_applied"] == 0 and cells[k]["leech_law"]["n_leech_tick_caps_applied"] == 0
               and cells[k]["leech_law"]["scope"] == "ALL_BODIES_IN_DISC" and cells[k]["leech_law"]["weapon_portion"] == 0.57
               for k in ALLC)
    R["TA-X-28"] = {"verdict": "GREEN" if ok28 else "RED", "values": "caps 0/0, ALL_BODIES_IN_DISC, 0.57 on 25/25" if ok28 else "fails"}

    # TA-X-29 (a)-(e), v1.8 § F.2h
    gm = man["gmag_conformance"]
    bcd = man["ta_x_29_b_c_d"]
    a29 = (gm["pred_gmag_whole"] is True and gm["attr_limb_records"] == 193 and gm["attr_lap_o"] == 154
           and gm["own_limb"] == 527 and gm["own_lap_o"] == 104 and gm["attr_limb_actors"] == 344)
    bb = bcd["(b)"]
    ce = bb["c5_equals_z5_in_content"]          # a DICT {unchanged, differ, added} -- read as emitted, not as a bool
    b_pack = (not pk["z5_value_keys_missing_in_c5"] and not pk["z5_value_keys_differing_in_c5"]
              and pk["c5_value_keys_added"] == ["⚑ C-11a_annotations"]
              and "RESTATEMENT" in pk["c5_points_to"]["⚑ nature"])
    b29 = (isinstance(ce, dict) and ce["unchanged"] is True and ce["differ"] == [] and ce["added"] == pk["c5_value_keys_added"]
           and b_pack and bb["exercised"]["all_equal_to_the_law"] and bb["exercised"]["dot_takes_nothing"]
           and bb["exercised"]["pcl_takes_nothing"] and bb["exercised"]["leech_dropped_from_health_path"]
           and bb["clamp_cross_check"]["green"] and bb["clamp_cross_check"]["rows"] == 527
           and not bb["clamp_cross_check"]["disagreements"]
           and bb["composition_order_read"] == pk["z5_composition_order"])
    cw = {w["wave"]: (w["port_M_inst"], w["z3_M_inst"]) for w in bcd["(c)"]["waves"]}
    c29 = (sorted(cw) == list(range(151, 161)) and bcd["(c)"]["green"] and not bcd["(c)"]["disagreements"]
           and all(abs(cw[w][0] - pk["z3_M_inst"][w]) <= 1e-9 and cw[w][1] == pk["z3_M_inst"][w] for w in cw))
    dd = bcd["(d)"]
    d29 = dd["n_inert"] == 29 and dd["identity_path_on_all"] and dd["printed"] == "unexercised: 0 of 29" and dd["in_POOL-466"] == 0

    def rec_ok(tab, w):
        got = {short(r): v["ratio"] for r, v in gm["per_record"][w].items()}
        miss = [n for n in tab if n not in got]
        extra = [n for n in got if n not in tab]
        dev = max(abs(got[n] - tab[n]) for n in tab if n in got)
        return {"n": len(got), "missing": miss, "extra": extra, "max_dev": dev, "ok": not miss and not extra and dev <= 5e-4}
    e159, e160 = rec_ok(TA29_W159, "w159"), rec_ok(TA29_W160, "w160")
    tm = gm["terminal_multiplier"]
    e29 = abs(tm["w159"] - 3.207764) <= 5e-4 and abs(tm["w160"] - 4.980316) <= 5e-4 and e159["ok"] and e160["ok"]
    R["TA-X-29"] = {"verdict": "GREEN" if a29 and b29 and c29 and d29 and e29 else "RED",
                    "values": {"(a)": a29, "(b)": b29, "(b) c5_equals_z5_in_content (emitted dict)": ce,
                               "(b) gamora from the pack": {"missing": pk["z5_value_keys_missing_in_c5"],
                                                            "differ": pk["z5_value_keys_differing_in_c5"],
                                                            "added": pk["c5_value_keys_added"]},
                               "(c)": c29, "(c) per wave (port, z3 emitted, z3 pack)": {w: (cw[w][0], cw[w][1], pk["z3_M_inst"][w]) for w in cw},
                               "(d)": d29, "(e)": {"w159": tm["w159"], "w160": tm["w160"], "rec159": e159, "rec160": e160}}}
    pur = man["manifest_blocks_other"]["pursuit"]
    ok30 = (pur["d_engage_m"] == 2.4 and pur["nan_test"]["nan"] is False and pur["nan_test"]["zero"] is False
            and pur["nan_test"]["d_engage"] is True and pur["source"] == "arena.json"
            and all(cells[k]["pursuit"]["n_bodies_halted_beyond_d_engage"] == 0 for k in ALLC))
    R["TA-X-30"] = {"verdict": "GREEN" if ok30 else "RED",
                    "values": {"d_engage_m": pur["d_engage_m"], "halted beyond": [cells[k]["pursuit"]["n_bodies_halted_beyond_d_engage"] for k in ALLC]}}
    return R


# ======================================================================================== 7 · DIAGNOSTICS / REPORT FACE
def diagnostics(cells: dict, man: dict, ver: dict, g3_summaries: dict) -> dict:
    D = {"TA-B-01 terminal waves (port, M-POL-2)": man["⚑ terminal_5_vectors_RAW"]["M-POL-2"],
         "oracle M-POL-2 (v1.12 § B.1a)": ORACLE_TERMINALS["M-POL-2"],
         "printed beside TA-X-06: port W1": man["⚑ terminal_5_vectors_RAW"]["W1"], "oracle W1": ORACLE_TERMINALS["W1"],
         "terminal vectors, all arms": man["⚑ terminal_5_vectors_RAW"]}
    keys = ["TA-B-02_uptime", "TA-B-03_frac_moving", "TA-B-04_P_chan_given_moving", "TA-B-05_P_chan_given_stationary",
            "TA-B-06_plant_ratio", "TA-B-07_release_duty", "TA-B-09_channel_split"]
    D["M-POL-2 per-tick (n = 5)"] = {kk: {"per_salt": [cells[("M-POL-2", s)]["census"][kk] for s in SALTS],
                                          "mean": sum(cells[("M-POL-2", s)]["census"][kk] for s in SALTS) / 5} for kk in keys}
    D["TA-B-08 ordering holds"] = [cells[("M-POL-2", s)]["census"]["TA-B-08_ordering_holds"] for s in SALTS]
    D["TA-B-14 W1 vetoes / occupancy"] = [(cells[("W1", s)]["walls"]["n_avoidance_vetoes"],
                                          cells[("W1", s)]["walls"]["n_pool_occupancy_ticks"]) for s in SALTS]
    D["TA-B-15 (nodata bodies, fraction)"] = {a: [(cells[(a, s)]["board"]["ta_b_15"]["n_nodata_spawn_inert"],
                                                  cells[(a, s)]["board"]["ta_b_15"]["fraction_of_bodies"]) for s in SALTS] for a in ARMS}
    inv1 = sum(1 for k in ALLC if cells[k]["terminal"]["killer_id"] and cells[k]["terminal"]["terminal_reason"] == "cleared")
    res = 0
    for k in ALLC:
        hit0 = False
        for row in cells[k]["hp_trace"]:
            if row["hp"] <= 0.0:
                hit0 = True
            elif hit0:
                res += 1
                break
    inv3 = sum(1 for k in ALLC if cells[k]["⚑ pcl"]["n_pcl_attacks_landed"] > 0
               and not cells[k]["intake_by_damage_family"].get("PercentCurrentLife", 0) > 0)
    D["R-6"] = {"(i)": inv1, "(ii)": res, "(iii)": inv3, "harness": ver["r6_invariants"]}
    D["sustain leech/intake (port, printed not asserted)"] = {a: [round(cells[(a, s)]["⚑ sustain"]["leech_over_intake"], 3)
                                                                  for s in SALTS] for a in ARMS}
    tc = {K(k): cells[k]["ta_x_08_counters"] for k in ALLC}
    csc = [v["n_control_suppressed_channelling"] for v in tc.values()]
    g3t = {k: v["ta_x_08_counters"] for k, v in g3_summaries.items()}
    D["rule 13"] = {"run_sum": sum(csc), "run_max": max(csc),
                    "run_n_control_suppressed_sum": sum(v["n_control_suppressed"] for v in tc.values()),
                    "run_doubly_suppressed_sum": sum(v["n_control_suppressed_released"] for v in tc.values()),
                    "run_pre_fight_suppressed_sum": sum(v["n_control_suppressed_pre_fight"] for v in tc.values()),
                    "run_released_pre_fight_sum": sum(v["n_released_pre_fight"] for v in tc.values()),
                    "g3_sum_port": sum(ver["g3"]["per_cell"][k]["control_term"]["port"] for k in ver["g3"]["per_cell"]),
                    "g3_sum_oracle": sum(ver["g3"]["per_cell"][k]["control_term"]["oracle"] for k in ver["g3"]["per_cell"]),
                    "g3_equal_cells": sum(1 for k in ver["g3"]["per_cell"] if ver["g3"]["per_cell"][k]["control_term"]["equal"]),
                    "g3_doubly_suppressed_sum (port/oracle)": [sum(v["port"]["n_control_suppressed_released"] for v in g3t.values()),
                                                               sum(v["oracle"]["n_control_suppressed_released"] for v in g3t.values())],
                    "g3_pre_fight_suppressed_sum (port/oracle)": [sum(v["port"]["n_control_suppressed_pre_fight"] for v in g3t.values()),
                                                                  sum(v["oracle"]["n_control_suppressed_pre_fight"] for v in g3t.values())],
                    "g3_summaries_ta_x_08_equal": sum(1 for v in g3t.values() if v["equal"])}
    # TA-B-19 / the dilution factor (v1.5 § dilution: per-salt D / n_waves, mean of salts, over the seal's 161.6)
    tpw = [cells[("M-POL-2", s)]["ta_x_08_counters"]["D"] / len(cells[("M-POL-2", s)]["ta_x_16_counters"]["waves_played"])
           for s in SALTS]
    D["TA-B-19 ticks/wave (M-POL-2, D / waves played)"] = {"per_salt": tpw, "mean": sum(tpw) / 5,
                                                           "seal_mean": 161.6, "dilution": (sum(tpw) / 5) / 161.6}
    D["terminals"] = {K(k): [cells[k]["terminal"]["terminal_wave"], cells[k]["terminal"]["terminal_reason"]] for k in ALLC}
    return D


def flat(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from flat(v, f"{p}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from flat(v, f"{p}[{i}]")
    else:
        yield p, o


def jdiff(a, b):
    fa, fb = dict(flat(a)), dict(flat(b))
    return sorted(set(k for k in fa.keys() | fb.keys() if fa.get(k, "<absent>") != fb.get(k, "<absent>")))


def main() -> int:
    ev = verify_evidence()
    pk = pack_derivations()
    sets = set_digests()
    srcr = source_reads()
    cells, man, ver = load(REV, EV)
    pcells, pman, pver = load(REV_PR, EV_PR)
    g3s = {}
    for k in ALLC:
        g3s[K(k)] = json.loads(git_bytes(f"{G3DIR}/summaries/{k[0]}_s{k[1]}.json"))
    R = grade(cells, man, ver, sets, pk, srcr)
    RP = grade(pcells, pman, pver, sets, pk, srcr)
    D = diagnostics(cells, man, ver, g3s)

    cls = {}
    for r in EXACT:
        v = R[r]["verdict"]
        cls.setdefault("GREEN" if v.startswith("GREEN") else v, []).append(r)
    pre_bad = [p for p in ("P-1", "P-2", "P-3", "P-4", "P-5") if R[p]["verdict"] != "GREEN"]
    c1_ok = R["C1"]["verdict"] == "CONFORMING"
    l2_ok = R["TA-X-07"]["verdict"] == "GREEN"
    if cls.get("RED"):
        verdict = "STRUCTURAL"
    elif cls.get("UNGRADEABLE") or pre_bad or not c1_ok:
        verdict = "INDETERMINATE"
    else:
        verdict = "PASS"

    # ---------------- § G.1a item 5: graded vs read
    cell_bytes = {K(k): (sha(git_bytes(f"{EV}/{k[0]}/{k[1]}/cell.json")), sha(git_bytes(f"{EV_PR}/{k[0]}/{k[1]}/cell.json", REV_PR)))
                  for k in ALLC}
    dig_a = {f"{c['arm']}|{c['salt']}": c["digest"] for c in man["cells"]}
    dig_p = {f"{c['arm']}|{c['salt']}": c["digest"] for c in pman["cells"]}
    rows_all = ["P-1", "P-2", "P-3", "P-4", "P-5", "C1"] + EXACT + ["TA-X-06"]
    row_diff = {r: {"attempt": R[r]["verdict"], "pre-read": RP[r]["verdict"],
                    "values_equal": json.dumps(R[r]["values"], sort_keys=True, default=str)
                    == json.dumps(RP[r]["values"], sort_keys=True, default=str)} for r in rows_all}
    item5 = {"cell.json bytes equal": sum(1 for a, b in cell_bytes.values() if a == b),
             "cell_digest equal": sum(1 for k in dig_a if dig_a[k] == dig_p.get(k)),
             "rows: verdict equal": sum(1 for v in row_diff.values() if v["attempt"] == v["pre-read"]),
             "rows: every value equal": sum(1 for v in row_diff.values() if v["values_equal"]),
             "rows compared": len(rows_all),
             "row differences": {r: v for r, v in row_diff.items() if not v["values_equal"] or v["attempt"] != v["pre-read"]},
             "ta_manifest.json differing leaf paths": jdiff(pman, man),
             "ta_verdict.json differing leaf paths": jdiff(pver, ver),
             "ta_x_08 / ta_x_16 / r11_bound / g3 blocks equal": [pver["ta_x_08"] == ver["ta_x_08"], pver["ta_x_16"] == ver["ta_x_16"],
                                                                  pver["r11_bound"] == ver["r11_bound"], pver["g3"] == ver["g3"]],
             "harness_stdout equal": sha(git_bytes(f"{EV}/harness_stdout.txt")) == sha(git_bytes(f"{EV_PR}/harness_stdout.txt", REV_PR))}
    recon = {r: {"gamora": R[r]["verdict"], "jack-ryan H-7": JR_READ[r],
                 "agree": (R[r]["verdict"] == JR_READ[r]) or (R[r]["verdict"].startswith("GREEN") and JR_READ[r].startswith("GREEN")
                                                             and R[r]["verdict"] == JR_READ[r])}
             for r in ["P-1", "P-2", "P-3", "P-4", "P-5", "C1"] + EXACT}
    sd_ok = all(sets[k]["digest"] == PIN[k] for k in ("POOL-466", "SWING-456", "NONSWING-10")) and sets["POOL-466"]["routes_agree"]
    ev_ok = (ev["prereg_ok"] and ev["attempt"]["ok"] and ev["preread"]["ok"] and ev["preread_unchanged_4833bcf_to_7a97716"]
             and ev["runtime_tree"]["ok"] and ev["H7_read"]["ok"] and ev["g3_ok"] and ev["packs_ok"] and sd_ok
             and all(d["ok"] for d in ev["h9_h10_docs"].values())
             and ev["engine"]["HEAD"].startswith("22cd2288") and ev["engine"]["oracle_tree_porcelain"] == "")
    id_ok = (ver["prereg_sha256"] == man["prereg_sha256"] == PIN["prereg_v1.13"] and ver["prereg_version"] == "v1.13"
             and ver["prereg_carried_from"]["sha256"] == PIN["prereg_v1.12"] and ver["run_kind"] == "attempt"
             and ver["attempt"] == "v1.13 attempt 2 of 2" and ver["attempt_overall"] == 3 and ver["verdict"] is None
             and ver["runtime_digest"]["value"] == ver["runtime_digest"]["at_boot"]["value"] == ver["runtime_digest"]["at_end"]["value"]
             == PIN["runtime_tree"] and ver["runtime_digest"]["unchanged_through_the_run"]
             and ver["pre_attempt_read"]["expected_runtime_digest"] == ver["pre_attempt_read"]["runtime_digest_at_boot"] == PIN["runtime_tree"]
             and ver["pre_attempt_read"]["equal_at_boot"] is True
             and ver["pre_attempt_read"]["finding_sha256"] == ev["H7_read"]["file_sha256"] == PIN["H7_read"]
             and ver["ta_manifest_sha256"] == PIN["ta_manifest"] and man["runtime_digest_boot"]["value"] == PIN["runtime_tree"]
             and pver["runtime_digest"]["value"] == PIN["runtime_tree"] and pver["run_kind"] == "pre_read")

    print("== EVIDENCE ==")
    print(f"  prereg v1.13 {ev['prereg_sha256']} ; v1.12 {ev['prereg12_sha256']} ok={ev['prereg_ok']}")
    for f in ("attempt", "preread"):
        x = ev[f]
        print(f"  {f}: MANIFEST {x['MANIFEST_sha256']} members={x['members']} fail={x['member_failures']} tree={x['tree_recomputed'][:16]}"
              f" ta_manifest={x['ta_manifest_sha256'][:16]} ta_verdict={x['ta_verdict_sha256'][:16]} filing_all={x['filing_checks_all']} ok={x['ok']}")
    print(f"  runtime {ev['runtime_tree']['recomputed']} ({ev['runtime_tree']['n_members']}) ok={ev['runtime_tree']['ok']}")
    print(f"  H-7 read {ev['H7_read']} ; G3 {ev['g3_MANIFEST_sha256'][:16]} l2 {ev['l2_operands_jsonl_sha256'][:16]} ok={ev['g3_ok']}")
    print(f"  packs ok={ev['packs_ok']} ; set digests ok={sd_ok} ; H9/H10 ok={all(d['ok'] for d in ev['h9_h10_docs'].values())} ;"
          f" engine {ev['engine']['HEAD'][:8]} oracle-clean={ev['engine']['oracle_tree_porcelain'] == ''}")
    print(f"  emission identity (prereg, run_kind, attempt, runtime digest x3, boot check, finding_sha256) ok={id_ok}")
    print(f"  vector from waves.json {pk['V11-P06-1']} sum {pk['sum_v11']}/{pk['sum_on']} P06 {pk['P06-KEY']} = pin {pk['vector_equals_pin']}")
    print("== PRECONDITIONS / C1 ==")
    for p in ("P-1", "P-2", "P-3", "P-4", "P-5", "C1"):
        print(f"  {p}: {R[p]['verdict']}")
    print("== EXACT ROWS ==")
    for r in EXACT + ["TA-X-06"]:
        print(f"  {r}: {R[r]['verdict']} :: {json.dumps(R[r]['values'], default=str, ensure_ascii=False)[:300]}")
    print("== COUNTS ==", {k: len(v) for k, v in cls.items()}, {k: v for k, v in cls.items() if k != "GREEN"})
    print("== § G.1a ITEM 5 ==", json.dumps({k: v for k, v in item5.items() if "leaf" not in k}, default=str))
    print("   ta_manifest diff paths:", item5["ta_manifest.json differing leaf paths"])
    print("   ta_verdict diff paths:", item5["ta_verdict.json differing leaf paths"])
    print("== RECONCILIATION ==", {r: v for r, v in recon.items() if not v["agree"]} or "all agree")
    print("== RULE 13 ==", D["rule 13"])
    print("== R-6 ==", D["R-6"])
    print("== TA-B-19 / dilution ==", D["TA-B-19 ticks/wave (M-POL-2, D / waves played)"])
    print("== VERDICT ==", verdict, "| evidence ok:", ev_ok, "| identity ok:", id_ok)

    res = {"evidence": ev, "pack_derivations": {k: v for k, v in pk.items() if k not in ("pairs", "ta09_vectors")},
           "set_digests": {k: v for k, v in sets.items() if k != "_sets"}, "source_reads": srcr, "rows": R,
           "rows_preread_same_grader": RP, "diagnostics": D, "counts": {k: len(v) for k, v in cls.items()}, "by_class": cls,
           "preconditions_not_green": pre_bad, "item5_graded_vs_read": item5, "reconciliation_jack_ryan": recon,
           "verdict": verdict, "evidence_ok": ev_ok, "identity_ok": id_ok}
    (HERE / "results.json").write_text(json.dumps(res, indent=1, default=str, ensure_ascii=False) + "\n")

    vf = {
        "schema": "kc2play.ta_verdict.v1",
        "written_by": "gamora (the grade of record), from grade_attempt2_v1p13.py; the harness's ta_verdict.json is pinned, not edited",
        "prereg_version": "v1.13", "prereg_sha256": ev["prereg_sha256"],
        "prereg_carried_from": {"version": "v1.12", "sha256": ev["prereg12_sha256"]},
        "substrate_epoch": "v3.7.1 / model 48a4c94c… / reference 1887257f…",
        "attempt": "v1.13 attempt 2 of 2", "attempt_overall": 3,
        "emission": {"godot_commit": REV, "dir": EV, "MANIFEST_sha256": ev["attempt"]["MANIFEST_sha256"],
                     "ta_manifest_sha256": ev["attempt"]["ta_manifest_sha256"], "ta_verdict_sha256": ev["attempt"]["ta_verdict_sha256"]},
        "runtime_digest": ev["runtime_tree"]["recomputed"],
        "verdict": verdict,
        "verdict_line": (f"{verdict} @ coverage 89/89, {len(cls.get('GREEN', []))}/28 EXACT rows green, TA-X-06 UNGRADEABLE-declared "
                         f"(Q83(b)), dilution {D['TA-B-19 ticks/wave (M-POL-2, D / waves played)']['dilution']:.3f}×, "
                         f"substrate_epoch v3.7.1/48a4c94c…, prereg v1.13"),
        "attempt_consumed": True,
        "cap_after_this_attempt": "0 of 2 remaining (the last attempt under the cap was spent)",
        "counts": res["counts"], "non_green_exact_rows": {k: v for k, v in cls.items() if k != "GREEN"},
        "preconditions": {p: R[p]["verdict"] for p in ("P-1", "P-2", "P-3", "P-4", "P-5")}, "C1": R["C1"]["verdict"],
        "exact_rows": {r: R[r]["verdict"] for r in EXACT},
        "declared_ungradeable": [{"id": "TA-X-06", "authority": "Q83(b) / KP-110", "printed": R["TA-X-06"]["values"]}],
        "ta_x_16": {K(k): R["TA-X-16"]["values"]["per_cell"][K(k)] for k in ALLC} | {"vector": {"V11-P06-1": pk["V11-P06-1"], "P06-KEY": pk["P06-KEY"]}},
        "ta_x_08": {K(k): {x: R["TA-X-08"]["values"]["per_cell"][K(k)][x] for x in
                           ("observed", "PRE_FIGHT", "D", "n_channelling", "n_released", "n_control_suppressed_channelling",
                            "n_ticks_released", "n_released_pre_fight", "id1", "id2", "id2p")} for k in ALLC},
        "g3": {k: {"census_equal": v["census_equal"], "control_term": v["control_term"]} for k, v in ver["g3"]["per_cell"].items()},
        "pre_attempt_read": {"finding": str(H7.relative_to(COLLAB)), "finding_sha256": ev["H7_read"]["file_sha256"],
                             "runtime_digest": ver["pre_attempt_read"]["expected_runtime_digest"], "rows_green": 28, "ungradeable": 0},
        "graded_vs_read": {k: v for k, v in item5.items()},
        "reconciliation_with_H7": recon,
        "rule_13": D["rule 13"],
        "r6_invariants": {k: D["R-6"][k] for k in ("(i)", "(ii)", "(iii)")},
        "set_digests": {k: sets[k] for k in ("POOL-466", "SWING-456", "NONSWING-10", "FALLBACK-158")},
        "hole_closure": "PENDING (H-5, jack-ryan) -- seal-blocking, not verdict-blocking",
        "seal_conditions_owed": ["H-5 (jack-ryan hole-closure finding at d03ca891)", "H-8 (Matt's T-C replay on the graded digest)"],
        "port_holes_printed": "the grade of record prints § F.5 cl. 11 with the v1.13 label",
    }
    (HERE / "ta_verdict_v1p13_attempt2.json").write_text(json.dumps(vf, indent=1, default=str, ensure_ascii=False) + "\n")
    print("evidence verified:", ev_ok and id_ok)
    return 0 if (ev_ok and id_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
