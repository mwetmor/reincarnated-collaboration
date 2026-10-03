#!/usr/bin/env python3
"""KC2-PLAY · T-A graded attempt "1 of 2, overall 4" -- gamora's INDEPENDENT SECOND READ (v1.13-era practice).

gamora, 2026-10-03. Reads drax's emission (godot 9756c31,
evidence/kc2-play/2026-10-03-ta-attempt1of2-overall4-v1.15-cells/) against the prereg set of record:
  v1.14  FILE 5bbe7ae5...  (every row except TA-X-29(b) and TA-X-30; carries v1.13 -> v1.12 -> v1.8 by reference)
  v1.15  FILE d1c4a75a...  (TA-X-29(b'), TA-X-30(a')(b'))
  notes  FILE 7797ff17...  (TA-X-13 scope, TA-X-21 site list, face rules)
GRADING ONLY: every expected value and tolerance is quoted from those texts (or recomputed from the pack by the
law they state); none is set here.

INDEPENDENCE: gamora's own code. It reuses gamora's attempt-2 grader (grade_attempt2_v1p13.py, collab, 2026-10-01)
for the carried rows and shares nothing with jack-ryan's grader, which was not read. jack-ryan's finding is read
only AFTER this file printed its row table (the reconciliation is written separately, by hand, in README.md).

READ-ONLY everywhere: godot through `git show <rev>:<path>` (each worktree copy checked equal to its blob); the
oracle source through `git show 969fbd8d:<path>` (engine HEAD has moved; nothing is imported from the oracle tree
except the pure pool466 law, whose file is checked unchanged since 969fbd8d); the packs hashed on disk. Nothing graded
is re-run.

Run:  python3 read_attempt4_v1p15.py   -> prints the report; writes results.json here.
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
ORACLE_REV = "969fbd8d"
REV = "9756c31"                                    # drax KP-278 evidence commit
REV_RUN = "c64c192"                                # godot HEAD at the run (run_record.godot_head)
REV_G3 = "66605a1"                                 # G3 runtime commit
EV = "evidence/kc2-play/2026-10-03-ta-attempt1of2-overall4-v1.15-cells"
G3DIR = "evidence/kc2-play/2026-10-03-g3-25cell-kp274-V311FULL-66605a1"
NOTES = COLLAB / "agentic_orchestration/gandalf/notes"
PREREG14 = NOTES / "2026-09-20-kc2-play-ta-prereg-v1.14.md"
PREREG15 = NOTES / "2026-09-20-kc2-play-ta-prereg-v1.15.md"
PREREGN = NOTES / "2026-09-20-kc2-play-ta-prereg-v1.15-notes.md"
PREREAD = COLLAB / "agentic_orchestration/qa/findings/2026-10-03-kc2-attempt4-candidate-h2-h7-reread-3e2359a6.md"
DERIVE14 = COLLAB / "agentic_orchestration/gamora/analyses/2026-10-02-kc2-play-prereg-v1.14/derive_v1p14.json"
OUT = ENGINE / "src/reincarnated/output"
MODEL = OUT / "kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143"
REFP = OUT / "kc2-reference-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143"
HERE = Path(__file__).resolve().parent

ARMS = ["M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"]
SALTS = [0, 1, 2, 3, 4]
ALLC = [(a, s) for a in ARMS for s in SALTS]
EXACT = ["TA-X-%02d" % i for i in (1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24,
                                    25, 26, 27, 28, 29, 30)]
assert len(EXACT) == 28

PIN = {   # the task brief (conductor) + v1.14 § A + v1.15 header + notes header
    "prereg_v1.14": "5bbe7ae5f0c3f73c77ee7cc3e21870ed8523b6d19fa1eae977dff451ef6b2d92",
    "prereg_v1.15": "d1c4a75ae2d35b2c27ddd127b18ef0066664eb54926e8466f2fe522a1ca34593",
    "prereg_notes": "7797ff17e5096b893aed3d041d8244165aebf34421a4252d1bfd9f91ab7ec752",
    "ta_verdict": "03f20be4694e01218141086f6e0c94046d3ccfb05fd65be941e39208f5dc3e16",       # brief: FILE 03f20be4…
    "ta_manifest_prefix": "4ec6fdc3",                                                         # brief: 4ec6fdc3…
    "tree_prefix": "51dc9d68",                                                                # brief: tree 51dc9d68…
    "runtime_tree": "3e2359a6d46c78029f7994a0f600434894dc8916d580b81732c20278257d3057",      # brief
    "model_pack": "997117278c1e28dac0da9a6cf64ddaf72111347094a7ac5e3b4c03590507d788",        # v1.14 § A.1
    "reference_pack": "af58ef4009029c99a618586f1bfccbd05a91fb381d49bd5483b7dce6eefeac1c",    # v1.14 § A.1
    "math_rules": "af2b0c52f9c7472febfea4f86413a8d088a6cb6efee8b099c4e56973fdf721de",        # v1.14 § A.1 #8
    "arena_json": "f06f3a64ae9d5a88b3b163433c494dc6881c9f1f0f8195c211867b708aac4c3b",        # v1.14 § A.1 #2
    "player_kit": "2b68af939b6c795c1b4c9f0411aa037fb4d0332f983fa942aa307c85329eeac6",        # v1.14 § A.1 #15
    "POOL-466": "33c886a11f91db1143c791ffcf9d95f7e7614e423373235231733c994c5c157b",
    "NONSWING-0": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",        # v1.14 TA-X-25 (∅)
    "FALLBACK-158": "e8114efaa8fa678db6a26bb6e4ffb926fc2c1a15a978e3d589cf918ff17ae6cb",
    "P-i": "cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e",
    "TA-X-09_rowset": "0e826ee093b98767901271c95e918a19e1c6d5b8a8663c99c87d8ced17086e78",
    "threat_py": "18b2500e7c429f67e82e489637212b3f1148762ac7f865d340b2a64f51a2d8a3",         # Q104.4 item 8
    "derive_v1p14_json": "7e9c28bd25b1406b7dd5f879f3ae9f5ed7cfc24c3b4cb7a670d1dd58ba2f7a1b",  # v1.14 § Z
    "preread_finding": "76667f56d037d97c4326bedc96d65d26a94259e1013c932415fe9f4ed060e492",   # the harness's pre_read_finding (verified here against git)
}
A8_ROWSETS = {   # v1.14 § B.1a
    "M0": "7c20aad10038076dccacc7e2c820d4fa32ff41466351fb7e9e8c8b18d03ec76c",
    "M-POL-2": "cf1c96e40535037d2c8dc42aa84615a9c0feca608d6a9d436fbb9e3c775e7ca7",
    "M-POL-2-NULL": "629b9271cc254833a45b2a0ff83d872712a0d99e273660221595dd71cda3505f",
    "W1": "5102fd732dde3f1c7a1bda7ea522be9ff15bc26acc86c3b640d6414d8ff8361e",
    "W1-NULL": "54934746784371a15caf6053e4379e4fb04d680202714cae68992af33bb1ca8f",
}
A8_RANGE = {"M0": ("IC7-A-V311-0322", "IC7-A-V311-0477", 156), "M-POL-2": ("IC7-A-V311-0168", "IC7-A-V311-0321", 154),
            "M-POL-2-NULL": ("IC7-A-V311-0001", "IC7-A-V311-0167", 167), "W1": ("IC7-A-V311-0635", "IC7-A-V311-0791", 157),
            "W1-NULL": ("IC7-A-V311-0478", "IC7-A-V311-0634", 157)}
SETUP_C, SETUP_T = ["IC7-A-V311-0832"], ["IC7-A-V311-0831", "IC7-A-V311-0833", "IC7-A-V311-0834", "IC7-A-V311-0835"]
# notes § 4 Note 1: the explicit chaos_aether_dot_divisor=True row per job (the one "configured from a8" takes)
DIVISOR_TRUE_ROW = {"M-POL-2-NULL": "IC7-A-V311-0017", "M-POL-2": "IC7-A-V311-0179", "M0": "IC7-A-V311-0334",
                    "W1-NULL": "IC7-A-V311-0490", "W1": "IC7-A-V311-0647", "WALK": "IC7-A-V311-0792"}
LU_KEYS = [5, 5, 5, 4, 4, 5, 5, 5, 5, 4]                       # v1.14 § F.2m′
LU_SETS = {151: [1, 2, 3, 4, 5], 152: [1, 2, 3, 4, 5], 153: [1, 2, 3, 4, 5], 154: [1, 2, 3, 4], 155: [1, 2, 3, 4],
           156: [1, 2, 3, 4, 5], 157: [1, 2, 3, 4, 5], 158: [1, 2, 3, 4, 5], 159: [1, 2, 3, 4, 5], 160: [1, 2, 3, 4]}
P06KEY = [0, 1, 1, 0, 1, 1, 1, 1, 0, 1]
W1_BOUND = 43.71638147965161                                   # v1.14 TA-X-10
EXTENTS = 8.0                                                  # TA-X-17 (carried value)
TA18_BITS = ["c00fffffffffffde", "be9777a5cf72cec6"]
RG1_LIVE = ["V311-RG-003", "V311-RG-005", "V311-RG-007", "V311-RG-008", "V311-RG-009", "V311-RG-010", "V311-RG-012",
            "V311-RG-014", "V311-RG-015", "V311-RG-016", "V311-RG-017", "V311-RG-018"]       # v1.14 § F.2p
# TA-X-21: notes § 2, the in-scope modules, live and dead sites, and FILE digests at 969fbd8d
T21_MOD = {"threat.py": "18b2500e7c429f67e82e489637212b3f1148762ac7f865d340b2a64f51a2d8a3",
           "deferred_arrival.py": "0a6b579b78aaf748732afadce50558c6f00eb2eb916ea7d9b5def7a69243557a",
           "dot_timeline.py": "b4a3bb8268c71005b4d2f317cbd9a7b20e505193f09e78924712258ed92cbe37",
           "control_application.py": "c0b0cc73bea6fb860cf49b2602a507a2a57b6242728cf520bc6a4960b3405643",
           "gd_engagement.py": "776e7048427bbd47bbf9ffb36f9a3d162a990b182fd71e3f207a41c0cafee920",
           "gd_reposition.py": "28c2031ddbdd8f30eeaefd10467a81353dfe9004163fd1f18f82f8164fab3c1c"}
T21_LIVE = ["control_application.py:591", "dot_timeline.py:380", "gd_engagement.py:121", "gd_engagement.py:187",
            "gd_reposition.py:364", "gd_reposition.py:365", "gd_reposition.py:519", "gd_reposition.py:530",
            "gd_reposition.py:554", "gd_reposition.py:726", "gd_reposition.py:731", "gd_reposition.py:739",
            "threat.py:1613", "threat.py:1774"]
T21_DEAD = ["deferred_arrival.py:329", "threat.py:1813", "threat.py:2182"]
# TA-X-29(e): v1.15 § F.2h′ per-record tables (= v1.14 § Q104.2 re-derivation)
TA29_W159 = {"aetherial_fleshhulk_mine": 3.514042, "beetle_maggot01": 3.301094, "chthonianrylok_ekketzul": 3.59875,
             "chthonianservitor_lunalvalgoth": 2.546547, "humanwendigo_darkwood_01": 3.75048,
             "korvaakmessenger_02": 3.033476, "korvaakmessenger_02b": 3.034357, "manticore_jaggedwaste_01": 2.956584,
             "rokwind_01": 3.362895, "skeletalgolem_stepsoftorment_01": 3.120862, "statue_templeguardian_02": 1.960798,
             "statue_templeguardian_03": 1.960798, "stonegryphon_templeguardian_01": 2.762796,
             "wendigo_ancient_namadea": 4.077782, "witchgod_finalboss": 3.978465, "yeti_rimehorn_01": 3.080011}
TA29_W160 = {"aetherialcolossus_galakros": 3.80807, "nemesis_aetherial_01": 8.165613,
             "nemesis_aetherialvanguard_01": 6.466635, "nemesis_beast_01_p1": 3.829365, "nemesis_beast_02": 2.689026,
             "nemesis_chthonian_02": 5.55761, "nemesis_chthonianvoidborn_01": 4.517305, "nemesis_kymon_01": 3.474869,
             "nemesis_kymon_02": 1.075958, "nemesis_orderdeathsvigil_01": 6.921402,
             "nemesis_orderdeathsvigil_02": 3.658935, "nemesis_outlaw_01": 5.837726, "nemesis_outlaw_02": 5.07033,
             "nemesis_undead_01": 3.822594, "nemesis_undead_02b": 5.470426, "nemesis_wendigo_01": 6.06632,
             "nemesis_wendigo_02": 4.391011, "statue_korvaaktombguardian": 4.102804, "wendigocannibal_h01": 5.916297,
             "wendigocannibal_h02": 5.946459, "wendigocannibal_h03": 5.476449, "wendigocannibal_h04": 5.429514,
             "wendigocannibal_h05": 5.429514}
TA29_E = {"w159": 3.197066, "w160": 4.935649}
TALLY = ["CHANNELLING", "CHANNELLING_AND_MOVING", "MOVING", "IDLE"]
F14_SENTENCE = ("The oracle of record is v3.11 (`V311-FULL`), sealed with five residuals carried to REFERENT-v2: (1) waves "
                "last ≈ 2.3× the referent's (oracle mean w151–159 ≈ 39.4 s vs the referent's 17.3 s, KP-226; on the 25 graded "
                "cells 37.812 s); (2) the oracle survives w160 more often than the referent did (graded cells: 20/25 clear w160; "
                "seat M-POL-2 over 20 salts: 16/20; the referent died in w160 at 25 s); (3) summons are over-produced (≈ 492 "
                "monster summons per graded cell) and 3 of the referent's 13 summon identities are absent (Haraxis's "
                "Aberrations, Skeletal Archers, Margul's Maggots); (4) the referent's max-HP dip (16,368 = ⌊20,005 × 9/11⌋, "
                "w153) is unidentified and not modelled; (5) the six mutators' flat-array level-index law is INFERRED, not "
                "decoded. A T-A PASS says port ≡ oracle; it says nothing about these.")


def git(repo, *a, text=False):
    return subprocess.run(["git", "-C", str(repo), *a], check=True, capture_output=True, text=text).stdout


def git_bytes(path: str, rev: str = REV, repo: str = GODOT) -> bytes:
    return git(repo, "show", f"{rev}:{path}")


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
    out = git(GODOT, "ls-tree", "-r", "--name-only", rev, prefix + "/", text=True).split("\n")
    return sorted(t[len(prefix) + 1:] for t in out if t)


def K(k) -> str:
    return f"{k[0]}|{k[1]}"


def short(rec: str) -> str:
    return rec.rsplit("/", 1)[-1].removesuffix(".dbr")


# ======================================================================================== 1 · IDENTITY / EVIDENCE
def verify_folder(rev: str, ev: str) -> dict:
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
    return {"MANIFEST_sha256": sha(man_b), "members": len(members), "member_failures": bad,
            "tree_recomputed": tree_law(lines), "tree_manifest": man["tree_digest"],
            "tracked_minus_members": [t for t in tracked if t not in members],
            "members_minus_tracked": [t for t in members if t not in tracked],
            "pinned_harness_files": man.get("⚑ pinned_harness_files"),
            "filing_checks": man.get("⚑ filing_checks"), "identity": man.get("⚑ identity"),
            "run_record": man.get("run_record")}


def verify_identity() -> dict:
    o = {"preregs": {"v1.14": fsha(PREREG14), "v1.15": fsha(PREREG15), "notes": fsha(PREREGN)}}
    o["preregs_ok"] = (o["preregs"]["v1.14"] == PIN["prereg_v1.14"] and o["preregs"]["v1.15"] == PIN["prereg_v1.15"]
                       and o["preregs"]["notes"] == PIN["prereg_notes"])
    # the preregs as committed (worktree == HEAD blob)
    o["preregs_committed_clean"] = git(COLLAB, "status", "--porcelain", "--", str(PREREG14), str(PREREG15), str(PREREGN),
                                       text=True).strip() == ""
    f = verify_folder(REV, EV)
    o["emission"] = f
    o["emission"]["ta_verdict_sha256"] = sha(git_bytes(f"{EV}/ta_verdict.json"))
    o["emission"]["ta_manifest_sha256"] = sha(git_bytes(f"{EV}/ta_manifest.json"))
    o["emission_ok"] = (not f["member_failures"] and f["members"] == 28 and f["tree_recomputed"] == f["tree_manifest"]
                        and f["tree_recomputed"].startswith(PIN["tree_prefix"])
                        and f["tracked_minus_members"] == ["MANIFEST.json"] and not f["members_minus_tracked"]
                        and o["emission"]["ta_verdict_sha256"] == PIN["ta_verdict"] == f["pinned_harness_files"]["ta_verdict.json"]
                        and o["emission"]["ta_manifest_sha256"].startswith(PIN["ta_manifest_prefix"])
                        and o["emission"]["ta_manifest_sha256"] == f["pinned_harness_files"]["ta_manifest.json"]
                        and f["filing_checks"]["all"] is True)
    o["emission_commit_subject"] = git(GODOT, "log", "-1", "--format=%H %s", REV, text=True).strip()[:200]
    # runtime tree: recomputed from kc2_runtime/MANIFEST.json over the blobs at REV; unchanged since the run and G3
    rman = json.loads(git_bytes("kc2_runtime/MANIFEST.json"))
    rl, rbad = [], []
    for m in rman["members"]:
        g = sha(git_bytes("kc2_runtime/" + m["path"]))
        if g != m["sha256"]:
            rbad.append(m["path"])
        rl.append(f"{m['path']}  {g}")
    rtracked = ls_tree(REV, "kc2_runtime")
    rmembers = sorted(m["path"] for m in rman["members"])
    same_run = subprocess.run(["git", "-C", GODOT, "diff", "--quiet", REV_RUN, REV, "--", "kc2_runtime/"]).returncode == 0
    same_g3 = subprocess.run(["git", "-C", GODOT, "diff", "--quiet", REV_G3, REV, "--", "kc2_runtime/"]).returncode == 0
    lib = "native/bin/libkc2rt_contact.macos.arm64.dylib"
    o["runtime_tree"] = {"recomputed": tree_law(rl), "manifest_says": rman["tree_digest"], "n_members": len(rmembers),
                         "member_failures": rbad, "member_not_tracked": [m for m in rmembers if m not in rtracked],
                         "unchanged_run_head_c64c192_to_9756c31": same_run, "unchanged_g3_66605a1_to_9756c31": same_g3,
                         "native_lib_is_member": lib in rmembers,
                         "native_lib_sha256": sha(git_bytes("kc2_runtime/" + lib))}
    o["runtime_ok"] = (o["runtime_tree"]["recomputed"] == rman["tree_digest"] == PIN["runtime_tree"] and not rbad
                       and not o["runtime_tree"]["member_not_tracked"] and same_run and same_g3
                       and o["runtime_tree"]["native_lib_is_member"])
    # G3 evidence folder: integrity of its own manifest
    gman = json.loads(git_bytes(f"{G3DIR}/MANIFEST.json"))
    gl, gbad = [], []
    for p, m in gman["members"].items():
        b = git_bytes(f"{G3DIR}/{p}")
        s = m["sha256"] if isinstance(m, dict) else m
        if sha(b) != s:
            gbad.append(p)
        gl.append(f"{p}  {sha(b)}")
    o["g3_folder"] = {"MANIFEST_sha256": sha(git_bytes(f"{G3DIR}/MANIFEST.json")), "tree_recomputed": tree_law(gl),
                      "tree_manifest": gman["tree_digest"], "member_failures": gbad, "n": len(gl),
                      "oracle_level": gman.get("oracle_level"), "runtime_commit": gman.get("runtime_commit"),
                      "all_25_zero_divergence": gman.get("all_25_zero_divergence")}
    o["g3_folder_ok"] = (not gbad and o["g3_folder"]["tree_recomputed"] == gman["tree_digest"]
                         and gman.get("oracle_level") == "V311-FULL")
    # the pre-attempt read finding the harness pinned
    rel = str(PREREAD.relative_to(COLLAB))
    c = git(COLLAB, "log", "-1", "--format=%h", "--", rel, text=True).strip()
    o["preread_finding"] = {"file_sha256": fsha(PREREAD), "commit": c,
                            "blob_sha256": sha(git(COLLAB, "show", f"{c}:{rel}"))}
    o["preread_ok"] = o["preread_finding"]["file_sha256"] == o["preread_finding"]["blob_sha256"] == PIN["preread_finding"]

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
    o["model_pack"], o["reference_pack"] = mp, rp
    o["files"] = {"math_rules": fsha(MODEL / "model/math_rules.json"), "arena_json": fsha(MODEL / "model/arena.json"),
                  "player_kit": fsha(MODEL / "model/player_kit.json"), "derive_v1p14_json": fsha(DERIVE14)}
    o["packs_ok"] = (mp["digest"] == mp["manifest_digest"] == PIN["model_pack"] and mp["n"] == 21 and not mp["failures"]
                     and mp["disk_equals_manifest"] and rp["digest"] == rp["manifest_digest"] == PIN["reference_pack"]
                     and rp["n"] == 7 and not rp["failures"] and rp["disk_equals_manifest"]
                     and rp["cross_pin"] == PIN["model_pack"] and all(o["files"][k] == PIN[k] for k in o["files"]))
    o["engine"] = {"HEAD": git(ENGINE, "rev-parse", "HEAD", text=True).strip(),
                   "oracle_rev_reachable": subprocess.run(["git", "-C", str(ENGINE), "cat-file", "-e", ORACLE_REV + "^{commit}"]).returncode == 0}
    return o


# ======================================================================================== 2 · PACK / ORACLE-SOURCE DERIVATIONS
def pack_derivations() -> dict:
    model = MODEL / "model"
    waves = json.loads((model / "waves.json").read_text())
    keys_on = {w: {r["spawn_point"] for r in waves["pools"]["wave_spawn"] if r["global_wave"] == w} for w in range(151, 161)}
    off_sets = {w: sorted(keys_on[w] - {6}) for w in keys_on}
    p06 = [1 if 6 in keys_on[w] else 0 for w in range(151, 161)]
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
    mo = json.loads((model / "monster_offense.json").read_text())
    z3 = {r["value"]["wave"]: r["value"]["M_inst"] for r in mo["⚑ v3p4p2_rows"]["z3_wave_damage_modifier_check"]}
    arena = json.loads((model / "arena.json").read_text())
    kit = json.loads((model / "player_kit.json").read_text())
    d14 = json.loads(DERIVE14.read_text())
    return {"off_sets": off_sets, "LU_equals_pools_for_off": all(off_sets[w] == LU_SETS[w] for w in LU_SETS),
            "LU_vector_from_sets": [len(LU_SETS[w]) for w in range(151, 161)], "P06-KEY": p06,
            "P06_equals_pin": p06 == P06KEY, "LU_equals_derive14": d14["TA-X-16"]["LU-KEYS"] == LU_KEYS
            and {int(k): v for k, v in d14["TA-X-16"]["LU-KEYS_sets"].items()} == LU_SETS,
            "pairs": plist, "n_pairs": len(plist), "n_degenerate": sum(1 for lo, hi in plist if lo == hi),
            "ta09_rowset": rowset, "ta09_n": len(vecs), "ta09_vectors": vec_meta,
            "z3_M_inst": z3, "arena_placement_extents_m": arena["placement_extents_m"]["value"],
            "arena_d_engage_m": arena["d_engage_m"]["value"] if isinstance(arena.get("d_engage_m"), dict) else arena.get("d_engage_m"),
            "kit_channel_radius_m": kit["channel"]["radius_m"]["value"],
            "sets_v311 (derive_v1p14.json)": d14["sets"]}


def pool466_now() -> dict:
    """POOL-466 by the export law (pure; the module is checked byte-identical to its 969fbd8d blob first)."""
    rel = "src/reincarnated/export/kc2_baton_v3p5p1_schema.py"
    same = subprocess.run(["git", "-C", str(ENGINE), "diff", "--quiet", ORACLE_REV, "--", rel]).returncode == 0
    sys.path.insert(0, str(ENGINE / "src"))
    from reincarnated.export.kc2_baton_v3p5p1_schema import pool466
    pool, agree = pool466({"model/waves.json": json.loads((MODEL / "model/waves.json").read_text())})
    return {"module_equals_969fbd8d": same, "n": len(pool), "digest": set_digest(pool), "routes_agree": agree,
            "_set": sorted(pool)}


def oracle_reads() -> dict:
    o = {"TA-X-21": {}}
    for mod, want in T21_MOD.items():
        b = git(ENGINE, "show", f"{ORACLE_REV}:src/reincarnated/simulation/kc2/{mod}")
        lines = b.decode().splitlines()
        o["TA-X-21"][mod] = {"sha256": sha(b), "equals_notes": sha(b) == want,
                             "round_lines": [(i + 1, l.strip()) for i, l in enumerate(lines) if "round(" in l]}
    return o


# ======================================================================================== 3 · (L2), exact rationals (v1.12 § F.2k; gamora's attempt-1 law, unchanged)
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
    n, q, NI, tot = lo["n"], lo["q"], lo["N_inner"], lo["inner_totals"]
    lossless = all(repr(float(s)) == s for s in list(lo["A_hat"].values()) + list(lo["A_hat_inner"].values()) + [lo["offered"]])
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
            and lo["sink_terms_present"] == 6 and cc["n_unbound_pcl_rows"] == 0, "margin": float(TOL / beta),
            "lossless": lossless}


# ======================================================================================== 4 · PORT SOURCE READS (TA-X-17/19/21/24)
def source_reads() -> dict:
    def src(p):
        return git_bytes("kc2_runtime/" + p).decode("utf-8")
    laws, board, fight = src("sim/kc2rt_laws.gd"), src("sim/kc2rt_board.gd"), src("sim/kc2rt_fight.gd")
    lines = lambda s, pat: [(i + 1, l.strip()) for i, l in enumerate(s.splitlines()) if re.search(pat, l)]
    o = {"TA-X-17": {"law_line": lines(laws, r"var rho := extents_m \* u2"),
                     "f64_returns": lines(laws, r"return PackedFloat64Array\(\[rho \* cos\(theta\), rho \* sin\(theta\)\]\)"),
                     "placement_sites": lines(board, r"scatter_polar_uniform_rho_f64\(u1, u2, placement_extents_m"),
                     "extents_halt": lines(board, r"float\(pe\) != placement_extents_m")}}

    def fn_body(name):
        m = re.search(r"\nfunc " + re.escape(name) + r"\(.*?(?=\nfunc |\Z)", fight, re.S)
        return m.group(0) if m else ""
    pos_pat = r'(\bpx\b|\bpy\b|position|_dist_to_player|\.distance_to|"x"|"y")'
    fl = fight.splitlines()
    build_i = [i for i, l in enumerate(fl) if re.search(r'_defer_queue\[at\] as Array\)\.append\(\{"seq"', l)]
    packet = " ".join(fl[i].strip() + " " + fl[i + 1].strip() for i in build_i)
    keys = re.findall(r'"([A-Za-z_]+)"\s*:', packet)
    o["TA-X-19"] = {"_defer_arrivals_line": lines(fight, r"^func _defer_arrivals\("),
                    "packet_build_lines": [fl[i].strip() for i in build_i], "packet_keys": keys,
                    "position_keys_in_packet": [k for k in keys if re.fullmatch(r"px|py|pos|position|xy|x|y", k)],
                    "position_reads_in_arrival_path": {n: [l.strip() for l in fn_body(n).splitlines()
                                                           if re.search(pos_pat, l.split("#", 1)[0])]
                                                       for n in ("_defer_arrivals", "_cp_absorb", "_land")}}
    files = [f for f in ls_tree(REV, "kc2_runtime") if f.endswith(".gd")]
    viol = []
    for f in files:
        if f == "sim/kc2rt_quant.gd":
            continue
        for i, l in enumerate(src(f).splitlines()):
            code = re.sub(r'"(?:[^"\\]|\\.)*"', '""', l.split("#", 1)[0])
            if re.search(r"(?<![A-Za-z0-9_.])round\(", code):
                viol.append(f"{f}:{i + 1}: {l.strip()}")
    o["TA-X-21_port_scan"] = {"gd_files": len(files), "exempt": "sim/kc2rt_quant.gd", "bare_round_sites": viol}
    sims = [f for f in files if f.startswith("sim/") or f.startswith("loader/")]
    o["TA-X-24_sha256_mod_sites"] = [f"{f}:{i}: {t}" for f in sims for i, t in lines(src(f), r"sha256\(.*actor|actor_id.*sha256")
                                     if not t.startswith("#")]
    return o


# ======================================================================================== 5 · ROWS
def load():
    cells = {(a, s): json.loads(git_bytes(f"{EV}/{a}/{s}/cell.json")) for a in ARMS for s in SALTS}
    man = json.loads(git_bytes(f"{EV}/ta_manifest.json"))
    ver = json.loads(git_bytes(f"{EV}/ta_verdict.json"))
    g3s = {K(k): json.loads(git_bytes(f"{G3DIR}/summaries/{k[0]}_s{k[1]}.json")) for k in ALLC}
    return cells, man, ver, g3s


def grade(cells, man, ver, g3s, pk, pool, orr, srcr) -> dict:
    R = {}
    pre = man["preconditions"]
    # ---------------- preconditions (v1.14 § B; carried laws)
    p1 = pre["P1_coverage"]
    R["P-1"] = {"verdict": "GREEN" if (p1["mapped"] == p1["total"] == 89 and p1["unmapped"] == 0 and p1["closes"]
                                       and p1["counts"].get("UNMAPPED", 0) == 0) else "RED",
                "values": {k: p1[k] for k in ("mapped", "total", "unmapped", "counts", "refusals")}}
    p2 = pre["P2_stream_disjointness"]
    wf, ctr = p2["with_noop_fold"], p2["controls"]
    c1_ = (wf["fold"]["inserted"] and wf["fold"]["n_forks"] == 1 and wf["fold"]["n_invocations"] == p2["population"]["ticks_observed"][1]
           and "fork_stream" in wf["fold"]["stream"] and "forked FIRST" in wf["fold"]["stream"])
    c2_ = wf["own_stream_draws_measured"] == 0 and wf["fold"]["own_stream_draws"] == 0 and wf["fold"]["n_shared_stream_draws"] == 0
    c3_ = ("cell_digest" in p2["digest_function"] and "zero-draw site = absent site" in p2["digest_function"]
           and p2["digest_plain"] == p2["digest_with_noop_fold"] == wf["digest"])
    c4_ = len(ctr) == 3 and all(v["state"] != "GREEN" and v["digest_identical"] is False for v in ctr.values())
    probe_sites = [K(k) for k in ALLC for s in cells[k]["draw_sites"]["per_site"] if re.search(r"NOOP|p2_noop|P2", s["draw_site_id"])]
    c5_ = p2["fresh_pack_per_leg"] and p2["plain_leg_has_no_fold"] and not probe_sites
    R["P-2"] = {"verdict": "GREEN" if (c1_ and c2_ and c3_ and c4_ and c5_ and p2["arm"] == "M-POL-2" and p2["salt"] == 0) else "RED",
                "values": {"(1)": c1_, "(2)": c2_, "(3)": c3_, "(4) controls a/a0/b": {k: v["state"] for k, v in ctr.items()},
                           "(5)": c5_, "digest": p2["digest_plain"], "arm/salt": [p2["arm"], p2["salt"]],
                           "control (c)": "not built by the T-A harness; carried as H-3/H-7's (as at attempt 3)"}}
    p3 = pre["P3_roll"]
    R["P-3"] = {"verdict": "GREEN" if (p3["population"] == "POOL-466" and p3["cardinality"] == 466
                                       and p3["law"] == {"alternative": "WEIGHTED:pool_weight", "name": "UNIFORM:randrange"})
                else "RED", "values": {k: p3[k] for k in ("population", "cardinality", "law")},
                "note": "v1.14 § L.2: P-3 is the INCUMBENT roll's law; the FOUGHT roll is the line-up fold's (covered by G3/TA-X-16/25/27)"}
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
                "values": {"P4 blocks (25 cells + manifest)": p4ok, "runtime_header": rh_ok, "binary_sha256": rh["binary_sha256"]}}
    p5 = man["manifest_blocks_other"]["⚑ P5_folds"]
    p5_expect = {"winner_surface": "ARMED", "insufficient_energy_policy": "REFUSE", "regen_ungated": True,
                 "global_magnitude": "ARMED_UNCONDITIONAL", "per_cast_energy_column": "PARENT_PLUS_MODIFIER",
                 "monster_march_base_m_per_s": 3.209466, "pcl_limb": "MULTIPLICATIVE @ 26.0 %",
                 "monster_run_speed_population": "LAPR-MEASURED 128 · BANDA-DB-CITED 180 · FALLBACK 158"}
    ac = man["arm_config_a8"]
    a8 = {a: ac[a]["rowset"] == A8_ROWSETS[a] and ac[a]["configured_from_a8"] and ac[a]["setup_rows_applied"] == 0
          and ac[a]["pilot"] == "P-MOVE" and ac[a]["a8_rows"] == f"{A8_RANGE[a][0]}…{A8_RANGE[a][1]}" for a in ARMS}
    h4 = man["⚑ H4"]
    setup_ok = (h4["setup_partition"]["C"] == SETUP_C and h4["setup_partition"]["T"] == SETUP_T
                and h4["setup_partition"]["setup_rows_applied_to_any_arm"] == 0
                and all(h4["a8_rowsets"][a]["port"]["n"] == A8_RANGE[a][2] for a in ARMS))
    p5_ok = (all(p5.get(k) == v for k, v in p5_expect.items())
             and all(t in p5["non_health_route"] for t in ("Disruption", "ManaBurnDrain", "PierceRatio"))
             and "C3 NOT FOLDED" in p5["c11a"] and "CLASS" in p5["c11a"] and all(cells[k]["⚑ P5_folds"] == p5 for k in ALLC)
             and all(a8.values()) and setup_ok)
    R["P-5"] = {"verdict": "GREEN" if p5_ok else "RED",
                "values": {"carried settings": {k: p5.get(k) for k in p5_expect}, "a8 rowsets = § B.1a, configured from a8, P-MOVE": a8,
                           "setup partition C/T, 0 applied": setup_ok},
                "face": "the P5 block's pool_lift label still reads 'SWING-456 · NONSWING-10' (v1.13 sets); v1.14 TA-X-25 re-derived "
                        "SWING = POOL-466 / NONSWING = ∅. The per-arm fold list § B.6 says the harness prints is not printed; the "
                        "folds are carried by the a8 ROWSET equality (graded) -- face note, not a P-5 criterion I can fail"}

    # ---------------- C1: G3 conformance (§ C.9 incl. C.9.1′, C.9.8, C.9.9)
    g3c = ver["g3"]["per_cell"]
    ORACLE_ONLY = {"spawn_structure.py:344", "player_kit_residual.py:286"}   # stream-open lines of the two declared streams (§ C.9.1′)
    c1 = {}
    for k in ALLC:
        v, s = g3c[K(k)], g3s[K(k)]
        c1[K(k)] = (v["passes"] and v["injected"] == [] and v["decision_divergences"] == 0 and v["draw_mismatches"] == 0
                    and all(x == 0 for x in v["decision_by_class"].values()) and len(v["decision_by_class"]) == 8
                    and not v["port_only_streams"] and {x.split("|")[0] for x in v["oracle_only_streams"]} <= ORACLE_ONLY
                    and v["death"]["equal"] and v["census_equal"] is True and v["control_term"]["equal"] is True
                    and v["oracle_complete"] is True and s["oracle_complete"]["complete"] is True
                    and s["oracle_complete"]["waves"] == list(range(151, 161)) and v["native_shadow_ok"] is True
                    and v["shadow_mismatch_ticks"] == 0 and v["petpath_shadow_mismatch_calls"] == 0
                    and v["place_shadow_mismatch_calls"] == 0
                    and s["contact_solver"]["native_lib_sha256"] == PIN_NATIVE[0]
                    and s["decision_divergences"] == v["decision_divergences"] and s["draw_mismatches"] == v["draw_mismatches"]
                    and s["trace_sha256"] == v["trace_sha256"])
    ns = ver["g3"]["native_shadow"]
    cs_cells = all(cells[k]["contact_solver"]["contact_solver"] == "shadow" and cells[k]["contact_solver"]["native_lib_sha256"] == PIN_NATIVE[0]
                   and cells[k]["contact_solver"]["shadow_mismatch_ticks"] == 0 and cells[k]["contact_solver"]["place_shadow_mismatch_calls"] == 0
                   and cells[k]["contact_solver"]["petpath_shadow_mismatch_calls"] == 0 for k in ALLC)
    du_ok = [d.get("id") for d in ver["declared_ungradeable"]] == ["TA-X-06"]
    R["C1"] = {"verdict": "CONFORMING" if (all(c1.values()) and ver["g3"]["all_25_pass"] and ns["mismatches_all_zero"]
                                           and ns["library_sha256"] == PIN_NATIVE and cs_cells and du_ok) else "NON-CONFORMING",
               "values": {"G3 cells conforming": sum(c1.values()), "native lib (runtime member) sha": PIN_NATIVE[0],
                          "T-A run contact=shadow on 25/25 with 0 mismatches (C.9.8 fresh run per arm)": cs_cells,
                          "declared_ungradeable": [d.get("id") for d in ver["declared_ungradeable"]],
                          "G3 control term port/oracle": [sum(g3c[K(k)]["control_term"]["port"] for k in ALLC),
                                                          sum(g3c[K(k)]["control_term"]["oracle"] for k in ALLC)],
                          "oracle_only stream labels": sorted({x.split("|")[0] for k in ALLC for x in g3c[K(k)]["oracle_only_streams"]})}}

    # ---------------- EXACT rows
    t1 = pre["⚑ TA-X-01_self_determinism"]
    dig = {(c["arm"], c["salt"]): c["digest"] for c in man["cells"]}
    R["TA-X-01"] = {"verdict": "GREEN" if (t1["identical"] and t1["digest_run_1"] == t1["digest_run_2"] == dig[("M0", 2)]
                                         and t1["probe"].startswith("M0 salt 2") and (p2["arm"], p2["salt"]) != ("M0", 2)) else "RED",
                    "values": {"run_1": t1["digest_run_1"], "run_2": t1["digest_run_2"], "M0|2 cell digest": dig[("M0", 2)]}}
    R["TA-X-02"] = {"verdict": R["P-1"]["verdict"], "values": f"{p1['mapped']}/{p1['total']}, unmapped {p1['unmapped']}"}

    def subject(c):
        b = {k: v for k, v in c["board"].items() if not isinstance(v, (dict, list))}
        return json.dumps({"terminal": c["terminal"], "state_counts": c["census"]["state_counts"], "board": b,
                           "per_wave": c["board"]["per_wave"], "hp": c["hp_trace"],
                           "draws": sorted((s["draw_site_id"], s["draws"]) for s in c["draw_sites"]["per_site"] if s["draws"])},
                          sort_keys=True)
    for rid, x, y, ident in [("TA-X-03", "M-POL-2-NULL", "M0", True), ("TA-X-04", "W1-NULL", "M-POL-2", True),
                             ("TA-X-05", "M-POL-2", "M0", False)]:
        sd = [dig[(x, s)] == dig[(y, s)] for s in SALTS]
        ss = [subject(cells[(x, s)]) == subject(cells[(y, s)]) for s in SALTS]
        holds = all(sd) if ident else not all(sd)
        R[rid] = {"verdict": "GREEN" if holds and sd == ss else ("RED" if not holds else "UNGRADEABLE"),
                  "values": {"compares": f"{x} vs {y}", "digest_identical_per_salt": sd, "subject_identical_per_salt (gamora)": ss}}
    s6 = [dig[("W1", s)] == dig[("M-POL-2", s)] for s in SALTS]
    R["TA-X-06"] = {"verdict": "UNGRADEABLE-declared (Q83(b), KP-110)",
                    "values": f"port W1 vs M-POL-2 identical on salts {[s for s in SALTS if s6[s]]}; oracle (v1.14): salts [0, 1, 4]"}

    # TA-X-07 (a) relative ≤ 1e-12; (b) reported; (c) (L2) per cell from its own operands (v1.12 § F.2k; v1.14 § L.4 / H-2)
    rho = {K(k): float(cells[k]["conservation"]["residual_relative"]) for k in ALLC}
    l2 = {K(k): l2_cell(cells[k]["conservation"]["l2_operands"]) for k in ALLC}
    rb = man["r11_bound"]
    a_ok = all(v <= 1e-12 for v in rho.values())
    c_ok = all(v["holds"] for v in l2.values())
    worst = max(l2.items(), key=lambda kv: kv[1]["beta"])
    R["TA-X-07"] = {"verdict": "GREEN" if a_ok and c_ok else ("RED" if not a_ok else "UNGRADEABLE"),
                    "values": {"(a) max rho_hat": max(rho.values()), "(a) cells at 0.0": sum(v == 0.0 for v in rho.values()),
                               "(b) max |residual|": max(abs(float(cells[k]["conservation"]["residual"])) for k in ALLC),
                               "(c) gamora (L2) exact": {"all_25": c_ok, "worst": worst[0], "beta": worst[1]["beta"], "margin": worst[1]["margin"]},
                               "(c) harness r11_bound.all_25_hold (printed)": rb["all_25_hold"],
                               "max n_terms_accumulated (stale 4,500 label; budget retired v1.12)": max(cells[k]["conservation"]["n_terms_accumulated"] for k in ALLC)}}

    # TA-X-08 (v1.13 § F.2n.2 (1), (2) restated, (2p); § F.2o; v1.14 Q104.4 item 4 / § F.5 cl. 15)
    t8, f8 = {}, []
    for k in ALLC:
        c = cells[k]
        tc, sc = c["ta_x_08_counters"], c["census"]["state_counts"]
        D = sum(sc.get(s, 0) for s in TALLY)
        PF = sc.get("PRE_FIGHT", 0)
        nch = sc.get("CHANNELLING", 0) + sc.get("CHANNELLING_AND_MOVING", 0)
        W = c["ta_x_16_counters"]["waves_played"]
        term = c["terminal"]
        death = term["terminal_reason"] == "death"
        last = c["hp_trace"][-1]
        conv = {"one PRE_FIGHT per wave played": PF == len(W),
                "cleared => 10 PRE_FIGHT, 10 waves": death or (PF == 10 and len(W) == 10),
                "no DEAD": sc.get("DEAD", 0) == 0,
                "lethal tick censused alive (death only)": (not death) or (last["hp"] <= 0.0 and last["tick"] == term["run_tick"]
                                                                           == tc["n_player_ticks_observed"]),
                "cleared: no lethal tick": death or (last["hp"] > 0.0 and term["⚑ n_lethal_floor_ticks"] == 0
                                                     and term["run_tick"] == tc["n_player_ticks_observed"]),
                "states ⊆ tally + PRE_FIGHT": set(sc) <= set(TALLY) | {"PRE_FIGHT"},
                "counters = census": tc["D"] == D and tc["PRE_FIGHT"] == PF and tc["n_channelling"] == nch}
        id1 = tc["n_player_ticks_observed"] == D + PF
        id2 = tc["n_channelling"] + tc["n_released"] + tc["n_control_suppressed_channelling"] == D
        id2p = tc["n_ticks_released"] == tc["n_released"] + tc["n_released_pre_fight"]
        m0 = (k[0] not in ("M0", "M-POL-2-NULL")) or (tc["n_ticks_released"] == tc["n_released"] == tc["n_released_pre_fight"] == 0)
        ok = id1 and id2 and id2p and m0 and all(conv.values())
        if not ok:
            f8.append(K(k))
        t8[K(k)] = {"terminal": term["terminal_reason"], "observed": tc["n_player_ticks_observed"], "PF": PF, "D": D,
                    "n_channelling": tc["n_channelling"], "n_released": tc["n_released"],
                    "n_control_suppressed_channelling": tc["n_control_suppressed_channelling"], "id1": id1, "id2": id2,
                    "id2p": id2p, "no-fold arms release nothing": m0, "conv": conv}
    R["TA-X-08"] = {"verdict": "RED" if f8 else "GREEN", "values": {"fails": f8, "per_cell": t8,
                    "control term Σ (port realisation)": sum(cells[k]["ta_x_08_counters"]["n_control_suppressed_channelling"] for k in ALLC)}}

    t9 = man["ta_x_09"]
    em = [(v["rule_id"], v["vector_index"], v["want"], v["got"], v["verdict"], v["law_ok"], v["stored_ok"]) for v in t9["vectors"]]
    want = [(rid, i, list(v["out"].values())[0] if isinstance(v["out"], dict) else v["out"]) for rid, i, v in pk["ta09_vectors"]]
    em9 = [e for e in em if any(e[0] == w[0] and e[1] == w[1] for w in want)]
    t9_ok = (pk["ta09_rowset"] == PIN["TA-X-09_rowset"] == t9["rowset"]["measured"] and t9["n"] == 9 == pk["ta09_n"]
             and len(em9) == 9 and all(e[0] == w[0] and e[1] == w[1] and e[2] == w[2] and e[3] == e[2] and e[4] == "REPLAYED"
                                       and e[5] and e[6] for e, w in zip(em9, want))
             and t9["rowset"]["math_rules_file_sha256"] == PIN["math_rules"])
    R["TA-X-09"] = {"verdict": "GREEN" if t9_ok else "RED", "values": {"rowset (gamora)": pk["ta09_rowset"], "n": pk["ta09_n"]}}

    w1 = {s: cells[("W1", s)]["walls"]["max_body_radius_m"] for s in SALTS}
    w1s = {s: cells[("W1", s)]["ta_x_10"]["max_spawn_radius_m"] for s in SALTS}
    R["TA-X-10"] = {"verdict": "GREEN" if all(v <= W1_BOUND for v in w1.values()) and all(cells[("W1", s)]["walls"]["armed"] for s in SALTS)
                    and all(cells[("W1", s)]["ta_x_10"]["max_body_radius_m"] == w1[s] for s in SALTS) else "RED",
                    "values": {"W1 max_body_radius_m": w1, "W1 max_spawn_radius_m (printed)": w1s, "bound": W1_BOUND,
                               "emitted bound": cells[("W1", 0)]["ta_x_10"]["bound"],
                               "emitted bound == prereg bound (bit)": cells[("W1", 0)]["ta_x_10"]["bound"] == W1_BOUND}}
    cl = {K((a, s)): [cells[(a, s)]["walls"]["n_wall_clamps_player"], cells[(a, s)]["walls"]["n_wall_clamps_body"]]
          for a in ("W1", "W1-NULL") for s in SALTS}
    R["TA-X-11"] = {"verdict": "GREEN" if all(v == [0, 0] for v in cl.values()) else "RED", "values": cl}
    R["TA-X-12"] = {"verdict": "GREEN" if all(cells[k]["⚑ TA-X-12_pool_damage_total"] == 0.0 for k in ALLC) else "RED",
                    "values": sorted({cells[k]["⚑ TA-X-12_pool_damage_total"] for k in ALLC})}
    t13 = {K(k): (cells[k]["⚑ TA-X-13_n_player_crits"], cells[k]["⚑ TA-X-13"]["n_player_crit_rows"],
                  cells[k]["⚑ TA-X-13"]["n_player_rows"], cells[k]["⚑ TA-X-13"]["vacuous"]) for k in ALLC}
    R["TA-X-13"] = {"verdict": "GREEN" if all(v[0] == 0 and v[1] == 0 and v[2] > 0 and v[3] is False for v in t13.values()) else "RED",
                    "values": {"(crits, crit rows, player rows, vacuous)": t13, "scope": "source == player (KP-248)"}}
    t14 = {K(k): [cells[k]["release"]["⚑ TA-X-14_do_not_1"]["cause_energy_count"], sorted(cells[k]["release"]["causes"])] for k in ALLC}
    R["TA-X-14"] = {"verdict": "GREEN" if all(v[0] == 0 and set(v[1]) <= {"type_a", "type_b"} for v in t14.values()) else "RED",
                    "values": t14}
    ok15, n15, p05w = True, 0, defaultdict(set)
    for k in ALLC:
        t = cells[k]["⚑ TA-X-15_release_schedule"]
        for row in t["per_wave_per_point"]:
            n15 += 1
            if row["point"] == 5:
                p05w[K(k)].add(row["wave"])
            if row["release_ticks"] != ([49] if row["point"] == 5 else [0]) or row["point"] not in (1, 2, 3, 4, 5):
                ok15 = False
        if t["n_intra_point_staggers"] != 0 or t["staggers"] or t["p05_release_tick_expected"] != 49 or t["p05_release_s"] != 4.0:
            ok15 = False
    R["TA-X-15"] = {"verdict": "GREEN" if ok15 else "RED",
                    "values": {"(wave, point) rows": n15, "(a)": ok15, "(b)": "GREEN-BY-CONSTRUCTION",
                               "p05 waves (M0|0, printed)": sorted(p05w["M0|0"])}}

    # TA-X-16 (v1.14 § F.2m′ (a)-(d), key grain, W = {151..T})
    t16, f16 = {}, []
    for k in ALLC:
        c = cells[k]
        tc, tk, term = c["ta_x_16_counters"], c["ta_x_16_keys"], c["terminal"]
        T = 160 if term["terminal_reason"] == "cleared" else term["terminal_wave"]
        W = list(range(151, T + 1))
        idx = [w - 151 for w in W]
        pw = c["board"]["per_wave"]
        fk = {int(w): sorted(v) for w, v in tk["fought_keys_per_wave"].items()}
        ik = {int(w): sorted(v) for w, v in tk["incumbent_keys_rolled_per_wave"].items()}
        sched = defaultdict(set)
        for row in c["⚑ TA-X-15_release_schedule"]["per_wave_per_point"]:
            sched[row["wave"]].add(row["point"])
        a = (tc["waves_played"] == W and tc["terminal_wave"] == T and sorted(fk) == W and sorted(ik) == W
             and all(fk[w] == LU_SETS[w] and ik[w] == LU_SETS[w] for w in W)
             and tc["pool_picks_per_wave"] == [LU_KEYS[i] for i in idx] and [x["pool_picks"] for x in pw] == [LU_KEYS[i] for i in idx]
             and [x["wave"] for x in pw] == W and tk["grain"] == "key")
        b = tc["n_pool_picks"] == sum(LU_KEYS[i] for i in idx) == c["board"]["n_pool_picks"]
        cc = (tc["n_spawn_point_6_keys_rolled"] == 0 and tc["n_spawn_point_6_keys_rolled_per_wave"] == [0] * len(W)
              and all(x["⚑ KP-180_p06_keys_rolled"] == 0 for x in pw) and all(6 not in fk[w] and 6 not in ik[w] for w in W)
              and all(6 not in sched[w] for w in W))
        d = (tc["n_p06_keys_filtered_per_wave"] == [P06KEY[i] for i in idx]
             and [x["⚑ KP-180_p06_keys_filtered"] for x in pw] == [P06KEY[i] for i in idx]
             and tc["n_p06_keys_filtered"] == sum(P06KEY[i] for i in idx))
        if not (a and b and cc and d):
            f16.append(K(k))
        t16[K(k)] = {"T": T, "n_waves": len(W), "n_pool_picks": tc["n_pool_picks"], "expected": sum(LU_KEYS[i] for i in idx),
                     "a": a, "b": b, "c": cc, "d": d, "harness holds": ver["ta_x_16"][K(k)]["holds"],
                     "every fought key carried a body (printed)": all(sched[w] == set(fk[w]) for w in W)}
    R["TA-X-16"] = {"verdict": "RED" if f16 else "GREEN",
                    "values": {"fails": f16, "LU-KEYS": LU_KEYS, "LU sets == pools_for(w, False) from waves.json": pk["LU_equals_pools_for_off"],
                               "P06-KEY (waves.json) == pin": pk["P06_equals_pin"], "LU == derive_v1p14.json": pk["LU_equals_derive14"],
                               "per_cell": t16}}

    # TA-X-17: ‖spawn − anchor‖ ≤ 8.0, anchor = v3.8 GD emitter (v1.14); now a per-cell statistic is emitted; source read too
    s17 = srcr["TA-X-17"]
    m17 = {K(k): cells[k]["ta_x_17"]["max_offset_m"] for k in ALLC}
    src17 = (len(s17["law_line"]) == 1 and len(s17["f64_returns"]) == 1 and len(s17["placement_sites"]) == 2
             and len(s17["extents_halt"]) == 1 and pk["arena_placement_extents_m"] == EXTENTS)
    anc = all("v3p8 GD geometry" in cells[k]["ta_x_17"]["anchor_source"] and cells[k]["ta_x_17"]["bound_m"] == EXTENTS for k in ALLC)
    R["TA-X-17"] = {"verdict": "GREEN" if all(v <= EXTENTS for v in m17.values()) and anc and src17 else "RED",
                    "values": {"max offset per cell (max over 25)": max(m17.values()), "anchor = v3.8 GD emitter": anc,
                               "source law + pack extents 8.0": src17}}
    x18 = man["ta_x_18"]
    parsed = [struct.pack(">d", float(s)).hex() for s in x18["emitted"]]
    lossless = x18["emitter"] == "cpython-repr" and all(repr(float(s)) == s for s in x18["emitted"])
    R["TA-X-18"] = {"verdict": ("GREEN" if parsed == TA18_BITS else "RED") if lossless else "UNGRADEABLE",
                    "values": {"emitted": x18["emitted"], "gamora parsed bits": parsed}}
    s19 = srcr["TA-X-19"]
    ok19 = (bool(s19["_defer_arrivals_line"]) and len(s19["packet_build_lines"]) == 1
            and set(s19["packet_keys"]) == {"seq", "b", "rec", "direct", "pcl", "fams", "cast", "n_rows"}
            and not s19["position_keys_in_packet"] and not any(s19["position_reads_in_arrival_path"].values()))
    R["TA-X-19"] = {"verdict": "GREEN" if ok19 else "UNGRADEABLE", "values": {"packet keys": s19["packet_keys"],
                    "position reads in arrival path": s19["position_reads_in_arrival_path"]}}
    t20 = man["ta_x_20"]
    cases = {r["case"]: (r["expect"], r["got"], r["ok"]) for r in t20["rows"]}
    want20 = {"2.99": True, "3.01": False, "BEHIND": True, "12 bodies": 12}
    ok20 = (t20["radius_m"] == pk["kit_channel_radius_m"] == 3.0 and t20["failures"] == 0 and len(t20["rows"]) == 5
            and all(e == g and o for e, g, o in cases.values())
            and all(any(key in c and cases[c][0] == v for c in cases) for key, v in want20.items()))
    R["TA-X-20"] = {"verdict": "GREEN" if ok20 else "RED", "values": {"radius_m": t20["radius_m"], "cases": cases}}

    # TA-X-21: quantisation rows (Python 3 round, half-to-even) + the notes § 2 site list re-verified + no bare round( on the port
    t21 = man["ta_x_21"]
    q = t21["quantisation"]
    q_ok = q["failures"] == 0 and all(r["ok"] and (("in" not in r) or r["got"] == r["expect"] == round(r["in"])) for r in q["rows"])
    ol = t21["oracle_live_sites"]
    mine = {}
    for mod, v in orr["TA-X-21"].items():
        for n, l in v["round_lines"]:
            mine[f"{mod}:{n}"] = l
    expect_sites = set(T21_LIVE) | set(T21_DEAD)
    cited = {c["site"]: c for c in ol["cited"]}
    sites_ok = (all(v["equals_notes"] for v in orr["TA-X-21"].values()) and set(mine) == expect_sites
                and all("int(round(" in mine[s] for s in T21_LIVE) and set(cited) == expect_sites
                and all(cited[s]["line_text"] == mine[s] for s in cited)
                and {s for s, c in cited.items() if c["live_under_V311_FULL"]} == set(T21_LIVE)
                and ol["n_live"] == 14 and ol["n_dead"] == 3 and ol["re_verified"]
                and all(v["equal"] and v["sha256_at_969fbd8d"] == T21_MOD[m] for m, v in ol["module_digests"].items())
                and set(ol["module_digests"]) == set(T21_MOD))
    scan_ok = (t21["no_bare_round_on_the_port"]["violations"] == 0 and t21["purity_scan"]["ok"]
               and not srcr["TA-X-21_port_scan"]["bare_round_sites"])
    R["TA-X-21"] = {"verdict": "GREEN" if q_ok and sites_ok and scan_ok else "RED",
                    "values": {"quantisation rows": len(q["rows"]), "rows ok (got == expect == python round)": q_ok,
                               "every round( line in the 6 modules @969fbd8d (gamora)": len(mine),
                               "= notes' 17 (14 live int(round( + 3 dead), emitted list equal": sites_ok,
                               "port bare round( (harness / gamora)": [t21["no_bare_round_on_the_port"]["violations"],
                                                                       srcr["TA-X-21_port_scan"]["bare_round_sites"]],
                               "gd files scanned (gamora)": srcr["TA-X-21_port_scan"]["gd_files"]},
                    "face": "quantisation.live_sites still labels the 12 test rows with the v1.13 threat.py list (incl. the two dead sites "
                            "1813 / 2182); the graded site list (oracle_live_sites) is the notes' -- label only"}
    R["TA-X-22"] = {"verdict": "GREEN" if all(cells[k]["release"]["⚑ TA-X-22_flag_cause_count"] == 0 for k in ALLC) else "RED",
                    "values": sorted({cells[k]["release"]["⚑ TA-X-22_flag_cause_count"] for k in ALLC})}
    R["TA-X-24"] = {"verdict": "GREEN" if man["v0_limb_set"]["phase_model"]["value"] == "PhaseModel.ENGAGE"
                    and not srcr["TA-X-24_sha256_mod_sites"] else "RED",
                    "values": {"phase_model": man["v0_limb_set"]["phase_model"], "sha256(actor_id) sites (gamora scan)": srcr["TA-X-24_sha256_mod_sites"]}}

    # TA-X-25 (v1.14: SWING = POOL-466, NONSWING = ∅)
    P = set(pool["_set"])
    swing, nons = P, set()
    t25 = {}
    for k in ALLC:
        b = cells[k]["board"]["ta_x_25"]
        sbr = b["(c) spawn_by_record"]
        cnt = {"nodata_inert": 0, "measured_inert": 0, "measured_offense": 0}
        bad = [[], [], []]
        for rec, v in sbr.items():
            r = rec.lower()
            cnt[v["class"]] += v["n_bodies"]
            if r not in P:
                bad[0].append(rec)
            if r in swing and v["class"] != "measured_offense":
                bad[1].append(rec)
            if r in nons:
                bad[2].append(rec)
        t25[K(k)] = {"a": b["(a) n_nodata_refused"] == 0,
                     "b": b["(b) n_nodata_spawn_inert"] + b["(b) n_measured_inert_spawn"] + b["(b) n_measured_offense_spawn"] == b["(b) n_bodies_spawned"],
                     "c1": not bad[0], "c2": not bad[1], "c3 (over ∅)": not bad[2],
                     "c4": cnt["nodata_inert"] == b["(b) n_nodata_spawn_inert"] and cnt["measured_inert"] == b["(b) n_measured_inert_spawn"]
                     and cnt["measured_offense"] == b["(b) n_measured_offense_spawn"], "bodies": b["(b) n_bodies_spawned"],
                     "c2 failures": bad[1][:5]}
    x25 = ver["ta_x_25"]
    face25 = x25["SWING"] == "POOL-466 (466)" and x25["NONSWING"] == "∅" and x25["c3_face"] == "satisfied over an empty set" \
        and x25["nonswing_digest"] == PIN["NONSWING-0"] and x25["swing_digest"] == PIN["POOL-466"]
    R["TA-X-25"] = {"verdict": "GREEN" if all(all(v[x] for x in ("a", "b", "c1", "c2", "c3 (over ∅)", "c4")) for v in t25.values())
                    and pool["digest"] == PIN["POOL-466"] and face25 else "RED",
                    "values": {"POOL-466 (gamora, export law)": [pool["n"], pool["digest"]], "face": face25,
                               "bodies per cell": {k: v["bodies"] for k, v in t25.items()},
                               "failing clauses": {k: [x for x in ("a", "b", "c1", "c2", "c3 (over ∅)", "c4") if not v[x]] for k, v in t25.items()
                                                   if not all(v[x] for x in ("a", "b", "c1", "c2", "c3 (over ∅)", "c4"))}}}

    t26, t26b = man["manifest_blocks_other"]["ta_x_26"], man["ta_x_26_b"]
    e = t26["(e)"]
    ok26 = (t26["(a) join_consumption_audit"]["green"] and not t26["(a) join_consumption_audit"]["unaccounted"]
            and t26["(b) loaded"] and t26["(b) sha256_measured"] == PIN["P-i"] and t26b["sha256_of_loaded_bytes"] == PIN["P-i"] and t26b["agrees"]
            and t26["(c)"] == {"multipliers": 5, "records": 790, "rows": 7900, "tiers": 8, "wave_invariant": 790}
            and t26["(d)"]["formula_helper_call_sites"] == 1 and t26["(d)"]["formula_disagreements"] == 0
            and abs(e["mean"] - 0.2468965517) <= 5e-7 and abs(e["median"] - 0.25) <= 5e-7 and abs(e["max"] - 0.35) <= 5e-7
            and abs(e["min"]) <= 5e-7 and e["n_zero"] == 17 and e["n"] == 464
            and all(sorted(cells[k]["⚑ V1-JOIN-1_leech_table"]["distinct_total_leech_resist_pct"]) == [65.0, 75.0, 83.0, 88.0, 105.0, 115.0, 565.0, 588.0]
                    for k in ALLC))
    R["TA-X-26"] = {"verdict": "GREEN" if ok26 else "RED", "values": {"(b)": t26b["sha256_of_loaded_bytes"], "(c)": t26["(c)"], "(e)": e}}

    # TA-X-27 (a) scan; (b) gamora's own CPython replay; (c) 41 registered live (V9 29 + rg1 12), p05 elided, G3 draw rules; (d) 139/97
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
        per_seed[ps["seed"]] = cons == ps["port_consumed"] and res == ps["port_results"] and sum(cons) == ps["port_words"]
    b27 = t27b["seeds"] == list(range(16)) and len(per_seed) == 16 and all(per_seed.values())
    a27 = t27["(a)"]["short_circuits_found"] == 0 and t27["(a)"]["unclassified"] == 0 and not t27["(a)"]["findings"]
    c = t27["(c)"]
    c27 = (c["registered_live_sites"] == 41 and c["V9"] == 29 and c["rg1_live"] == 12 and sorted(c["rg1_live_ids"]) == RG1_LIVE
           and c["rg1_registered_not_live"] == ["V311-RG-019"] and "ELIDED" in c["p05_draw"] and ver["ta_x_27_c"] == c
           and R["C1"]["verdict"] == "CONFORMING")
    d27 = t27["(d)"]["pairs"] == pk["n_pairs"] == 139 and t27["(d)"]["degenerate"] == pk["n_degenerate"] == 97
    R["TA-X-27"] = {"verdict": "GREEN" if a27 and b27 and c27 and d27 else "RED",
                    "values": {"(a)": a27, "(b) gamora replay, 16 seeds (python %s)" % sys.version.split()[0]: b27,
                               "(c)": c27, "(d) gamora from waves.json": [pk["n_pairs"], pk["n_degenerate"]]},
                    "face": "cell.draw_sites still prints sites_live 29 (the V9 count); the row's registry count (41) is in ta_x_27_c"}
    ok28 = all(cells[k]["leech_law"]["n_leech_target_caps_applied"] == 0 and cells[k]["leech_law"]["n_leech_tick_caps_applied"] == 0
               and cells[k]["leech_law"]["scope"] == "ALL_BODIES_IN_DISC" and cells[k]["leech_law"]["weapon_portion"] == 0.57 for k in ALLC)
    R["TA-X-28"] = {"verdict": "GREEN" if ok28 else "RED", "values": "caps 0/0, ALL_BODIES_IN_DISC, 0.57 on 25/25" if ok28 else "fails"}

    # TA-X-29: (a) carried; (b′) v1.15 § F.2h′.1; (c), (d) carried; (e) v1.15 values, |Δ| ≤ 5e-4
    gm, bcd = man["gmag_conformance"], man["ta_x_29_b_c_d"]
    a29 = (gm["pred_gmag_whole"] is True and gm["attr_limb_records"] == 193 and gm["attr_lap_o"] == 154
           and gm["own_limb"] == 527 and gm["own_lap_o"] == 104 and gm["attr_limb_actors"] == 344)
    FAM = ["instant_nonphys", "phys_clamped", "phys_clamped_unmapped", "phys_unclamped", "dot", "dot_leech_type", "dot_chaos_aether"]

    def b_block_ok(bb):
        return (bb["law"] == "CompositionFold" and bb["phys_limb"] == "LO" and bb["f_unmapped"] == -0.44
                and bb["chaos_aether_dot_divisor"] is True and bb["lapm_wave"] == 160
                and all(bb["exercised"][f]["n_equal_to_law"] == bb["exercised"][f]["n"] for f in FAM)
                and bb["exercised"]["pcl_rows_untouched"] is True)
    per = {K(k): cells[k]["ta_x_29_b"] for k in ALLC}
    per_ok = {kk: b_block_ok(v) and v == ver["ta_x_29_b_per_cell"][kk] and v["a8_row"] == DIVISOR_TRUE_ROW[kk.split("|")[0]]
              for kk, v in per.items()}
    tot = {f: sum(v["exercised"][f]["n"] for v in per.values()) for f in FAM}
    toteq = {f: sum(v["exercised"][f]["n_equal_to_law"] for v in per.values()) for f in FAM}
    bb = bcd["(b)"]
    b29 = (all(per_ok.values()) and b_block_ok(bb) and all(bb["exercised"][f]["n"] == tot[f] == toteq[f] for f in FAM)
           and sum(tot.values()) > 0 and tot["dot_chaos_aether"] == 0)
    cw = {w["wave"]: (w["port_M_inst"], w["z3_M_inst"]) for w in bcd["(c)"]["waves"]}
    c29 = (sorted(cw) == list(range(151, 161)) and bcd["(c)"]["green"] and not bcd["(c)"]["disagreements"]
           and all(abs(cw[w][0] - pk["z3_M_inst"][w]) <= 1e-9 and cw[w][1] == pk["z3_M_inst"][w] for w in cw))
    dd = bcd["(d)"]
    d29 = dd["n_inert"] == 29 and dd["identity_path_on_all"] and dd["printed"] == "unexercised: 0 of 29" and dd["in_POOL-466"] == 0

    def rec_ok(tab, w):
        got = {short(r): v["ratio"] for r, v in gm["per_record"][w].items()}
        miss, extra = [n for n in tab if n not in got], [n for n in got if n not in tab]
        dev = max(abs(got[n] - tab[n]) for n in tab if n in got)
        return {"n": len(got), "missing": miss, "extra": extra, "max_dev": dev, "ok": not miss and not extra and dev <= 5e-4}
    e159, e160 = rec_ok(TA29_W159, "w159"), rec_ok(TA29_W160, "w160")
    tm = gm["terminal_multiplier"]
    e29 = abs(tm["w159"] - TA29_E["w159"]) <= 5e-4 and abs(tm["w160"] - TA29_E["w160"]) <= 5e-4 and e159["ok"] and e160["ok"]
    R["TA-X-29"] = {"verdict": "GREEN" if a29 and b29 and c29 and d29 and e29 else "RED",
                    "values": {"(a)": a29, "(b′)": b29, "(b′) families Σ25 (n, n_equal)": {f: (tot[f], toteq[f]) for f in FAM},
                               "(b′) per-cell blocks ok": sum(per_ok.values()), "(c)": c29, "(d)": d29,
                               "(e)": {"w159": tm["w159"], "w160": tm["w160"], "rec159": e159, "rec160": e160}},
                    "face": "the divisor clause is UNREACHABLE-IN-PACK (notes § 4); port composed 0 such rows, so no RED-on-presence. "
                            "(e)'s emitted provenance still cites the v3.7.1 WALK rows (IC7-A-0379…0432) and 'carried to v1.12'; the "
                            "values are the v3.11 walk's (they equal v1.15 to 6 dp) -- provenance label stale"}

    # TA-X-30 (a′), (b′): v1.15 § F.2i′.2 GREEN-iff, per cell
    t30, f30 = {}, []
    mp = man["manifest_blocks_other"]["pursuit"]
    man_ok = mp["ring_halt_m"] == 2.4 == pk["arena_d_engage_m"] and mp["source"] == "arena.json" and mp["nan_test"]["nan"] is False
    for k in ALLC:
        p = cells[k]["pursuit"]
        tl, op, pe = p["travel_law"], p["operand"], p["pets"]
        need = [tl.get(x) for x in ("n_player_arg_steps", "n_unclipped", "n_unclipped_law_exact", "n_clipped", "n_clipped_shorter",
                                    "n_held", "n_held_zero", "n_halt_flag_mismatch", "n_position_mismatch", "n_nan")] + \
               [op.get(x) for x in ("n_attack_stand", "n_pursue_reach", "n_default_ring_halt", "n_waypoint_op0", "n_waypoint_reach_gr2",
                                    "n_waypoint_reach_default", "n_waypoint_reach_packed", "n_reach_ne_pack", "n_op_ne_rule")] + \
               [pe.get(x) for x in ("n_steps", "n_no_travel_by_law", "n_moved_law_exact", "n_moved_clipped_shorter", "n_moved_against_law",
                                    "n_op_incumbent_2.4", "n_op_pet_target_0", "n_reach_ne_pack")] + \
               [p.get(x) for x in ("n_bodies_halted_beyond_d_engage", "arena_armed", "r_g4_vacuous")]
        present = all(v is not None for v in need)
        a = present and (tl["n_unclipped_law_exact"] == tl["n_unclipped"] and tl["n_clipped_shorter"] == tl["n_clipped"]
                         and tl["n_held_zero"] == tl["n_held"] and tl["n_halt_flag_mismatch"] == 0 and tl["n_position_mismatch"] == 0
                         and tl["n_nan"] == 0 and op["n_reach_ne_pack"] == 0 and op["n_op_ne_rule"] == 0
                         and pe["n_moved_against_law"] == 0 and pe["n_reach_ne_pack"] == 0
                         and pe["n_moved_law_exact"] + pe["n_moved_clipped_shorter"] + pe["n_no_travel_by_law"] == pe["n_steps"]
                         and tl["n_player_arg_steps"] > 0 and tl["n_unclipped"] + tl["n_clipped"] + tl["n_held"] == tl["n_player_arg_steps"])
        b = present and p["n_bodies_halted_beyond_d_engage"] == 0
        armed_ok = p["arena_armed"] == (k[0] == "W1") and p["r_g4_vacuous"] == (not p["arena_armed"])
        vac = p["n_clamp_stops"] == 0
        face_ok = (ver["face"]["ta_x_30_b_prime"][K(k)]["face"] == "(b′) vacuous: no clamp stopped a body") == vac
        if not (a and b and armed_ok):
            f30.append(K(k))
        t30[K(k)] = {"a′": a, "b′": b, "armed": p["arena_armed"], "clamp calls/stops": [p["n_clamp_calls"], p["n_clamp_stops"]],
                     "(b′) vacuous (notes § 3.1)": vac, "face prints it": face_ok,
                     "steps / law-exact / held": [tl["n_player_arg_steps"], tl["n_unclipped_law_exact"], tl["n_held"]],
                     "pets steps / exact / no-travel": [pe["n_steps"], pe["n_moved_law_exact"], pe["n_no_travel_by_law"]],
                     "clipped (roster, pets)": [tl["n_clipped"], pe["n_moved_clipped_shorter"]],
                     "non-waypoint pursue steps": op["n_pursue_reach"]}
    R["TA-X-30"] = {"verdict": "RED" if (f30 or not man_ok) else "GREEN",
                    "values": {"fails": f30, "manifest ring_halt_m from arena.json, nan test": man_ok,
                               "(b′) vacuous cells": sum(v["(b′) vacuous (notes § 3.1)"] for v in t30.values()),
                               "per_cell": t30}}
    return R


PIN_NATIVE = ["74360ffae1a434ba0de85708009c8129c6b39c4ca03898a3e4be01641e27467f"]   # set from the runtime member in main()


# ======================================================================================== 6 · REPORT-FACE CHECKS (v1.14 § F.5 cl. 14/15; notes § 3/4)
def face_checks(cells, man, ver) -> dict:
    f = ver["face"]
    o = {}
    o["cl14 declared_residuals verbatim"] = ver["declared_residuals"] == F14_SENTENCE
    o["cl15 per-cell terminal_reason + lethal-tick reason"] = all(
        ver["terminal"][K(k)]["terminal_reason"] in ("death", "cleared")
        and ver["obs1_port"][K(k)]["lethal_tick_clause"] == ("applicable (a death)" if cells[k]["terminal"]["terminal_reason"] == "death"
                                                             else "inapplicable: no lethal tick (terminal_reason cleared)")
        for k in ALLC)
    o["port OBS-1 completeness 25/25, no STALL"] = all(ver["obs1_port"][K(k)]["complete"] and not ver["obs1_port"][K(k)]["stall"] for k in ALLC)
    o["notes 3.1 (b′) vacuity printed where n_clamp_stops == 0"] = all(
        (f["ta_x_30_b_prime"][K(k)]["face"] == "(b′) vacuous: no clamp stopped a body") == (cells[k]["pursuit"]["n_clamp_stops"] == 0) for k in ALLC)
    o["notes 3.2 reference collapse printed"] = f["trajectories"]["reference"] == "25 cells / 12 distinct trajectories (9 clear, 3 die)"
    # gamora's own count of the port's distinct trajectories (hp_trace + terminal)
    tr = {}
    for k in ALLC:
        h = sha(json.dumps([cells[k]["hp_trace"], cells[k]["terminal"]], sort_keys=True).encode())
        tr.setdefault(h, []).append(k)
    o["port distinct trajectories (gamora)"] = {"n": len(tr), "clear": sum(1 for v in tr.values() if cells[v[0]]["terminal"]["terminal_reason"] == "cleared"),
                                                "die": sum(1 for v in tr.values() if cells[v[0]]["terminal"]["terminal_reason"] == "death"),
                                                "emitted": f["trajectories"]["port"]}
    o["notes 3.3 unexercised printed"] = (f["unexercised_on_referent"]["non_waypoint_pursue_operand"]["reference_steps"] == 0
                                          and f["unexercised_on_referent"]["non_penetration_clip"]["reference_clipped_steps"] == 0)
    o["notes 3.4 clip flags (port clipped steps)"] = {"emitted": f["clip_flags"], "gamora": [K(k) for k in ALLC
                                                    if cells[k]["pursuit"]["travel_law"]["n_clipped"] > 0 or cells[k]["pursuit"]["pets"]["n_moved_clipped_shorter"] > 0]}
    o["notes 3.5 lethal tick face"] = f["ta_x_08_lethal_tick"]
    o["notes 4 divisor UNREACHABLE-IN-PACK printed"] = "UNREACHABLE-IN-PACK" in f["ta_x_29_b_divisor"]["clause"] and f["ta_x_29_b_divisor"]["port_composed_rows"] == 0
    o["KP-248 TA-X-13 scope printed"] = f["ta_x_13_scope"]
    o["§ G.3 prereg_carried_from (v1.15 says {v1.14, 5bbe7ae5})"] = {"emitted": {"version": ver["prereg_carried_from"]["version"],
                                                                             "sha256": ver["prereg_carried_from"]["sha256"][:8]},
                                                                 "conforms": ver["prereg_carried_from"]["version"] == "v1.14"
                                                                 and ver["prereg_carried_from"]["sha256"] == PIN["prereg_v1.14"]}
    o["§ G.3 prereg_set_of_record"] = ver["prereg_set_of_record"] == {"v1.14": PIN["prereg_v1.14"], "v1.15": PIN["prereg_v1.15"],
                                                                     "v1.15_notes": PIN["prereg_notes"]}
    o["§ F.5 cl. 11 holes sentence label"] = re.findall(r"A (v1\.\d+) PASS", ver["port_holes_sentence"])
    o["hole_closure"] = ver["hole_closure"]
    o["§ C.9.8 native shadow cited (lib sha, evidence)"] = {"lib": ver["g3"]["native_shadow"]["library_sha256"],
                                                           "evidence_dir": ver["g3"]["source_dir"].split("/evidence/")[-1]}
    o["r6_invariants"] = ver["r6_invariants"]
    return o


def main() -> int:
    ident = verify_identity()
    PIN_NATIVE[0] = ident["runtime_tree"]["native_lib_sha256"]
    pk = pack_derivations()
    pool = pool466_now()
    orr = oracle_reads()
    srcr = source_reads()
    cells, man, ver, g3s = load()
    R = grade(cells, man, ver, g3s, pk, pool, orr, srcr)
    F = face_checks(cells, man, ver)

    cls = {}
    for r in EXACT:
        v = R[r]["verdict"]
        cls.setdefault("GREEN" if v.startswith("GREEN") else v, []).append(r)
    pre_bad = [p for p in ("P-1", "P-2", "P-3", "P-4", "P-5") if R[p]["verdict"] != "GREEN"]
    c1_ok = R["C1"]["verdict"] == "CONFORMING"
    if cls.get("RED"):
        verdict = "STRUCTURAL"
    elif cls.get("UNGRADEABLE") or pre_bad or not c1_ok:
        verdict = "INDETERMINATE"
    else:
        verdict = "PASS"
    id_ok = (ident["preregs_ok"] and ident["emission_ok"] and ident["runtime_ok"] and ident["g3_folder_ok"] and ident["preread_ok"]
             and ident["packs_ok"] and pool["module_equals_969fbd8d"]
             and ver["prereg_version"] == man["prereg_version"] == "v1.15" and ver["prereg_sha256"] == man["prereg_sha256"] == PIN["prereg_v1.15"]
             and ver["run_kind"] == "attempt" and ver["attempt"] == "attempt 1 of 2, overall 4" and ver["attempt_overall"] == 4
             and ver["verdict"] is None and ver["substrate_epoch"] == "v3.11 / model 99711727… / reference af58ef40…"
             and ver["oracle_of_record"] == "engine 969fbd8d scripts/gamora_kc2_play_v3p11_oracle_2026_10_02.py run_one('V311-FULL') + v3p8.graded_arm"
             and ver["runtime_digest"]["value"] == ver["runtime_digest"]["at_boot"]["value"] == ver["runtime_digest"]["at_end"]["value"] == PIN["runtime_tree"]
             and ver["runtime_digest"]["unchanged_through_the_run"]
             and ver["pre_attempt_read"]["expected_runtime_digest"] == ver["pre_attempt_read"]["runtime_digest_at_boot"] == PIN["runtime_tree"]
             and ver["pre_attempt_read"]["equal_at_boot"] is True and ver["pre_attempt_read"]["finding_sha256"] == PIN["preread_finding"]
             and ver["ta_manifest_sha256"] == ident["emission"]["ta_manifest_sha256"]
             and man["runtime_digest_boot"]["value"] == PIN["runtime_tree"]
             and ver["godot_head_graded"]["head"].startswith(REV_RUN) and not ver["godot_head_graded"]["kc2_runtime_dirty"]
             and ver["model_pack"]["digest"] == PIN["model_pack"] and ver["reference_pack"]["digest"] == PIN["reference_pack"]
             and ver["cross_pin_verified"] is True and man["failures"] == [] and man["⚑ conditions_raised_to_the_grader"] == [])

    print("== IDENTITY / PINS ==")
    print(f"  preregs {ident['preregs']} ok={ident['preregs_ok']} committed-clean={ident['preregs_committed_clean']}")
    e = ident["emission"]
    print(f"  emission {REV}: MANIFEST {e['MANIFEST_sha256'][:16]} members={e['members']} fail={e['member_failures']} tree={e['tree_recomputed']}"
          f" ta_verdict={e['ta_verdict_sha256']} ta_manifest={e['ta_manifest_sha256']} filing.all={e['filing_checks']['all']} ok={ident['emission_ok']}")
    print(f"  runtime {ident['runtime_tree']['recomputed']} ({ident['runtime_tree']['n_members']}) native {ident['runtime_tree']['native_lib_sha256'][:16]} ok={ident['runtime_ok']}")
    print(f"  G3 folder {ident['g3_folder']['tree_recomputed'][:16]} n={ident['g3_folder']['n']} fail={ident['g3_folder']['member_failures']} ok={ident['g3_folder_ok']}")
    print(f"  pre-read finding {ident['preread_finding']} ok={ident['preread_ok']} ; packs ok={ident['packs_ok']} ; engine HEAD {ident['engine']['HEAD'][:8]}")
    print(f"  POOL-466 {pool['n']} {pool['digest'][:16]} module==969fbd8d {pool['module_equals_969fbd8d']}")
    print(f"  emission identity ok={id_ok}")
    print("== PRECONDITIONS / C1 ==")
    for p in ("P-1", "P-2", "P-3", "P-4", "P-5", "C1"):
        print(f"  {p}: {R[p]['verdict']} :: {json.dumps(R[p]['values'], default=str, ensure_ascii=False)[:260]}")
    print("== EXACT ROWS ==")
    for r in EXACT + ["TA-X-06"]:
        v = R[r]["values"]
        if isinstance(v, dict):
            v = {kk: vv for kk, vv in v.items() if kk != "per_cell"}
        print(f"  {r}: {R[r]['verdict']} :: {json.dumps(v, default=str, ensure_ascii=False)[:420]}")
    print("== COUNTS ==", {k: len(v) for k, v in cls.items()}, {k: v for k, v in cls.items() if k != "GREEN"})
    print("== FACE ==")
    for k, v in F.items():
        print(f"  {k}: {json.dumps(v, default=str, ensure_ascii=False)[:300]}")
    print("== VERDICT ==", verdict, "| identity ok:", id_ok)
    res = {"identity": ident, "pack_derivations": {k: v for k, v in pk.items() if k not in ("pairs", "ta09_vectors")},
           "pool466": {k: v for k, v in pool.items() if k != "_set"}, "oracle_reads": orr, "source_reads": srcr, "rows": R,
           "face": F, "counts": {k: len(v) for k, v in cls.items()}, "by_class": cls, "preconditions_not_green": pre_bad,
           "verdict": verdict, "identity_ok": id_ok}
    (HERE / "results.json").write_text(json.dumps(res, indent=1, default=str, ensure_ascii=False) + "\n")
    return 0 if id_ok else 1


if __name__ == "__main__":
    sys.exit(main())
