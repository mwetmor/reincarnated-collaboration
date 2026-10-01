#!/usr/bin/env python3
"""KC2-PLAY · T-A graded attempt 1 of 2 under prereg v1.12 -- THE GRADE OF RECORD'S INSTRUMENT.

gamora, 2026-10-01. Grades drax's emission (godot 9b0ad0c, evidence/kc2-play/2026-10-01-ta-attempt1-v1.12-cells/)
against prereg v1.12 (FILE a0454776...). GRADING ONLY: no expected value or tolerance is set here that the prereg
does not carry; every expected value below is quoted from v1.12 (or the version it carries the row from by reference).

READ-ONLY everywhere:
  * godot: every emission byte is read through `git show 9b0ad0c:<path>` (and the worktree copy is checked equal);
  * engine: the pack members are hashed on disk; POOL-466 / SWING-456 / NONSWING-10 are recomputed by calling the
    oracle's own `pool466` and `threat.load_profiles(...)` under P-5's loader call (a8 IC7-A-0453), nothing written;
  * the sealed cells are not opened.

Run:  python3 grade_attempt1_v1p12.py      (prints the report; writes results.json + the verdict file beside this file)
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import struct
import subprocess
import sys
from fractions import Fraction as Fr
from pathlib import Path

HOME = Path.home() / "Games"
GODOT = str(HOME / "reincarnated-godot")
COLLAB = HOME / "reincarnated-collaboration"
ENGINE = HOME / "reincarnated-engine"
REV = "9b0ad0c"                       # drax's evidence commit (KP-176)
REV_RT_STATE = "0802ab1"              # godot HEAD at the run (MANIFEST.godot_head_at_run)
EV = "evidence/kc2-play/2026-10-01-ta-attempt1-v1.12-cells"
G3DIR = "evidence/kc2-play/2026-10-01-g3-25cell-kp173"
PREREG = COLLAB / "agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.12.md"
OUT = ENGINE / "src/reincarnated/output"
MODEL = OUT / "kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247"
REFP = OUT / "kc2-reference-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247"
HERE = Path(__file__).resolve().parent

ARMS = ["M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"]
SALTS = [0, 1, 2, 3, 4]

# ---- pins quoted from v1.12 (PINS, § B.5, § A.2, § B.1a); the script asserts each against its recomputation
PIN = {
    "prereg_v1.12": "a0454776ab91d85f37fadffcb8886a498e1f498f208e0eb33b9d5a9797fc7854",
    "emission_MANIFEST": "25e4e5bd20dbd07e39a265d82b907a61cdd106b15713ed3b329d38dcf59f04ae",   # charter KP-176
    "ta_manifest": "d352293d90da0f73fecd41767a8def0cb31055aff2ecd00a4bbd8ef47bfbb4f9",         # charter KP-176
    "runtime_tree": "a9b756cddc4a046ca7a755e51d798158bb4cf84928ec1c12bfdb82c5e12165bb",        # KP-175 / jack-ryan
    "g3_MANIFEST": "90195c7ca96e04263cfb289e667a1437fa6e16ad97be392c5fdb085b26f2c8a7",         # KP-175
    "model_pack": "48a4c94c165715d3f4f5db89c1278aa8439fbe1507c39dd555f7ce91d4636c96",
    "reference_pack": "1887257f5370443a1729fde2ff446579b1acc501dcd03679244297b541e3e5b1",
    "POOL-466": "33c886a11f91db1143c791ffcf9d95f7e7614e423373235231733c994c5c157b",
    "SWING-456": "706a61d55dc6621814fc923d7428c5b263a95ebb00e9786d12f35dd385a7a4c0",
    "NONSWING-10": "00b4cb0e24b43e591a2e30200979725801aad1e7c1f9b7764ebef67461816e10",
    "FALLBACK-158": "e8114efaa8fa678db6a26bb6e4ffb926fc2c1a15a978e3d589cf918ff17ae6cb",
    "P-i": "cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e",
    "booking_census": "cf49eefec225b3d306d3773fe0e264b1c96739b1a2f1185a7706f71b527c2c24",
    # documents of record carried by v1.12 for H-9 / H-10 (filled into the verdict file, not emitted by the harness)
    "H9_NOTE": "90717b83926f06b5939a48c01c0cc4973d5f20d7d7eb60007b976d01ebde53e5",
    "H9_W1": "c68fcd3c133c8b8a55d75e85425876fe73d6d1752dfdd1cd21fa9041e87a24ff",
    "H9_MPOL2": "2aedf43f2091d0c575af1d7d07deb0278be87f0b4c917efa5c33d01e77707f61",
    "H9_W1NULL": "90b9ea619e8adfd3f8532cc55e16990c15348dd537071c5758000c2edafdf801",
    "H9_SCRIPT": "eede32e85f362b5d57b136b81344cae1bfd4b804515db2d6f2d66279d1920f55",
    "H10_receipt": "a0ad8246ac49628f8bd729c8cc2fba564b6456c4c06df0ae300e0439bfc447c9",
}
A8_ROWSETS = {   # § B.1a
    "setup": "c01d1ddaa4a5b7074203662522276a24a150312d9faeceb6634dc5438e0f71f1",
    "M0": "68549af0608cb9979771fcc4955ae8010f4f3516ad55a97b83922c994f571d12",
    "M-POL-2": "e698d5f555a37fcc12e703343286d4e25c12662d8cd35c9571f9a0ac8ae45dbf",
    "M-POL-2-NULL": "4393a14b56a97960ef42e73909a1cdefc49f3dc1a4cc41e7f20267b661a1a7b6",
    "W1": "5188284d198c139422276e8ac92f9a0bee03cea7dbb1cea32c6c7bf1d19a55e8",
    "W1-NULL": "b2abff6978105bfc1566d678d5f1dea756ea9ef0eab02f8457821f81125a7fdd",
    "WALK": "63c530edd2e825c05f0f95ce2f629d56dbff98da206ddb45690fc129d7bba0f2",
    "setup_C": "207ab21f853b18ca026327bf6c9ddc4afa705d29cd3ef0868c1e7818d1672b4c",
    "setup_T": "ab3197727b59cc355f479862a297b33bef89e74e6d40dbff14762c701f2c7be0",
}
# TA-X-29(e)'s per-record table, v1.8 § F.2h (carried unchanged to v1.12): short name -> ratio
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
ORACLE_TERMINALS = {"M-POL-2": [156, 152, 155, 152, 152], "W1": [156, 152, 155, 152, 155]}   # § B.1a oracle table


def git_bytes(path: str, rev: str = REV) -> bytes:
    return subprocess.run(["git", "-C", GODOT, "show", f"{rev}:{path}"], check=True, capture_output=True).stdout


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fsha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def set_digest(s) -> str:
    return sha("\n".join(sorted(s)).encode("utf-8"))


# ======================================================================================== 1 · EVIDENCE
def verify_evidence() -> dict:
    out = {}
    out["prereg_sha256"] = fsha(PREREG)
    out["prereg_ok"] = out["prereg_sha256"] == PIN["prereg_v1.12"]

    man_b = git_bytes(f"{EV}/MANIFEST.json")
    man = json.loads(man_b)
    out["emission_MANIFEST_sha256"] = sha(man_b)
    bad, lines = [], []
    for m in man["members"]:
        b = git_bytes(f"{EV}/{m['path']}")
        disk = (Path(GODOT) / EV / m["path"]).read_bytes()
        if sha(b) != m["sha256"] or len(b) != m["bytes"] or disk != b:
            bad.append(m["path"])
        lines.append(f"{m['path']}  {sha(b)}")
    tracked = subprocess.run(["git", "-C", GODOT, "ls-tree", "-r", "--name-only", REV, EV + "/"],
                             check=True, capture_output=True, text=True).stdout.split()
    tracked = sorted(t[len(EV) + 1:] for t in tracked)
    members = sorted(m["path"] for m in man["members"])
    out["emission"] = {"members": len(members), "member_failures": bad,
                       "tree_digest_recomputed": sha("\n".join(sorted(lines)).encode()),
                       "tree_digest_manifest": man["tree_digest"],
                       "tracked_minus_members": [t for t in tracked if t not in members],
                       "ta_manifest_sha256": sha(git_bytes(f"{EV}/ta_manifest.json"))}
    out["emission"]["ok"] = (not bad and out["emission"]["tree_digest_recomputed"] == man["tree_digest"]
                             and out["emission"]["tracked_minus_members"] == ["MANIFEST.json", "README.md"]
                             and out["emission_MANIFEST_sha256"] == PIN["emission_MANIFEST"]
                             and out["emission"]["ta_manifest_sha256"] == PIN["ta_manifest"])
    out["emission_manifest_claims"] = {k: man[k] for k in ("runtime_tree_digest", "godot_head_at_run",
                                                           "harness_exit_and_why", "verdict_file_note")}

    # runtime tree a9b756cd: recomputed from kc2_runtime/MANIFEST.json over git blobs at REV, and unchanged vs 0802ab1
    rman = json.loads(git_bytes("kc2_runtime/MANIFEST.json"))
    rl, rbad = [], []
    for m in rman["members"]:
        g = sha(git_bytes("kc2_runtime/" + m["path"]))
        if g != m["sha256"]:
            rbad.append(m["path"])
        rl.append(f"{m['path']}  {g}")
    rt = sha("\n".join(sorted(rl)).encode())
    rtracked = subprocess.run(["git", "-C", GODOT, "ls-tree", "-r", "--name-only", REV, "kc2_runtime/"],
                              check=True, capture_output=True, text=True).stdout.split()
    rtracked = sorted(t[len("kc2_runtime/"):] for t in rtracked)
    rmembers = sorted(m["path"] for m in rman["members"])
    same = subprocess.run(["git", "-C", GODOT, "diff", "--quiet", REV_RT_STATE, REV, "--", "kc2_runtime/"]).returncode == 0
    out["runtime_tree"] = {"recomputed": rt, "manifest_says": rman["tree_digest"], "n_members": len(rmembers),
                           "member_failures": rbad, "tracked_not_member": [t for t in rtracked if t not in rmembers],
                           "member_not_tracked": [m for m in rmembers if m not in rtracked],
                           "unchanged_0802ab1_to_9b0ad0c": same,
                           "booking_census_file": sha(git_bytes("kc2_runtime/tests/kc2rt_booking_census.gd"))}
    out["runtime_tree"]["ok"] = (rt == rman["tree_digest"] == PIN["runtime_tree"] and not rbad and same
                                 and out["runtime_tree"]["booking_census_file"] == PIN["booking_census"])

    # G3 input MANIFEST
    out["g3_MANIFEST_sha256"] = sha(git_bytes(f"{G3DIR}/MANIFEST.json"))
    out["g3_MANIFEST_ok"] = out["g3_MANIFEST_sha256"] == PIN["g3_MANIFEST"]

    # the packs, recomputed by the manifests' own law; the on-disk member set equals each manifest's
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
        return {"digest": sha("\n".join(sorted(pl)).encode("utf-8")), "manifest_digest": pm["pack_digest"],
                "n": len(pm["members"]), "failures": pbad,
                "disk_equals_manifest": disk == sorted(m["path"] for m in pm["members"]),
                "cross_pin": (pm.get("cross_pin") or {}).get("model_pack_digest")}
    mp, rp = pack(MODEL, "model"), pack(REFP, "reference")
    out["model_pack"], out["reference_pack"] = mp, rp
    out["packs_ok"] = (mp["digest"] == mp["manifest_digest"] == PIN["model_pack"] and not mp["failures"]
                       and mp["disk_equals_manifest"] and rp["digest"] == rp["manifest_digest"] == PIN["reference_pack"]
                       and not rp["failures"] and rp["disk_equals_manifest"] and rp["cross_pin"] == PIN["model_pack"])

    # H-9 / H-10 documents of record (filled into the verdict file; not emitted by the harness)
    h9 = COLLAB / "agentic_orchestration/gamora/analyses/2026-09-30-kc2-play-h9-w1-containment"
    docs = {}
    for k, p in {"H9_NOTE": h9 / "NOTE.md", "H9_W1": h9 / "h9_out_W1.json", "H9_MPOL2": h9 / "h9_out_M-POL-2.json",
                 "H9_W1NULL": h9 / "h9_out_W1-NULL.json", "H9_SCRIPT": h9 / "h9_w1_containment.py",
                 "H10_receipt": OUT / "kc2-baton-v3-cut-receipt-v3p7p1-20261001_021247.json"}.items():
        docs[k] = {"path": str(p), "sha256": fsha(p) if p.exists() else None}
        docs[k]["ok"] = docs[k]["sha256"] == PIN[k]
    out["h9_h10_docs"] = docs
    return out


# ======================================================================================== 2 · SET DIGESTS
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
        # FALLBACK-158 is not recomputed here: no row this grade evaluates reads it (it pins P-5 setting 9's
        # population, which the harness declares as 128 / 180 / 158). Reported as not recomputed, not as reproduced.
        fb = {"note": "not recomputed by this grade (no graded row reads it); v1.12 PINS value carried, not re-derived",
              "v1.12_pin": PIN["FALLBACK-158"]}
    finally:
        os.chdir(cwd)
    return {"POOL-466": {"n": len(pool), "digest": set_digest(pool), "routes_agree": routes_agree},
            "SWING-456": {"n": len(swing), "digest": set_digest(swing)},
            "NONSWING-10": {"n": len(nonswing), "digest": set_digest(nonswing)},
            "FALLBACK-158": fb,
            "_sets": {"POOL": sorted(pool), "SWING": sorted(swing), "NONSWING": sorted(nonswing)}}


# ======================================================================================== 3 · (L2) cross-check
U = Fr(1, 2 ** 53)
TOL = Fr(1, 10 ** 12)
K7 = ["offered", "applied", "dropped", "voided", "pool_truncated", "pcl_reclaim", "counterplay_absorbed"]


def gamma(k: int) -> Fr:
    k = max(k, 0)
    assert k * U < 1
    return k * U / (1 - k * U)


def g2(n: int) -> Fr:
    return gamma(n - 1) ** 2 if n >= 2 else Fr(0)


def l2_cell(c: dict) -> dict:
    """§ F.2k (L2), exact rationals, from the cell's own emitted operands (same law as h6_l2_exact.py)."""
    lo = c["conservation"]["l2_operands"]
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
            and lo["sink_terms_present"] == 6 and cc["n_unbound_pcl_rows"] == 0,
            "margin": float(TOL / beta), "f_max": fmax, "lossless": lossless}


# ======================================================================================== 4 · ROWS
def load_cells() -> dict:
    return {(a, s): json.loads(git_bytes(f"{EV}/{a}/{s}/cell.json")) for a in ARMS for s in SALTS}


def short(rec: str) -> str:
    return rec.rsplit("/", 1)[-1].removesuffix(".dbr")


def grade(cells: dict, man: dict, sets: dict) -> dict:
    R = {}
    allc = [(a, s) for a in ARMS for s in SALTS]
    pre = man["preconditions"]

    # ---------------- preconditions
    p1 = pre["P1_coverage"]
    p2 = pre["P2_stream_disjointness"]
    p3 = pre["P3_roll"]
    p4s = [cells[k]["⚑ P4_pack"] for k in allc] + [man["manifest_blocks_other"]["⚑ P4_pack"]]
    p5 = man["manifest_blocks_other"]["⚑ P5_folds"]
    R["P-1"] = {"verdict": "GREEN" if (p1["mapped"] == p1["total"] == 89 and p1["unmapped"] == 0 and p1["closes"])
                else "RED", "observed": p1}
    R["P-2"] = {"verdict": "GREEN" if p2["identical"] else "RED",
                "observed": {"digest_plain": p2["digest_plain"], "digest_with_noop_fold": p2["digest_with_noop_fold"],
                             "identical": p2["identical"], "noop_fold_draws (a literal, drax b215b11)": p2["noop_fold_draws"]}}
    R["P-3"] = {"verdict": "GREEN" if (p3["population"] == "POOL-466" and p3["cardinality"] == 466
                                       and p3["law"] == {"alternative": "WEIGHTED:pool_weight", "name": "UNIFORM:randrange"})
                else "RED", "observed": {k: p3[k] for k in ("population", "cardinality", "law")}}
    p4ok = all(p["verified"] and p["cross_pin"] and p["paired"] and p["mismatches"] == 0
               and p["model_pack"]["digest"] == PIN["model_pack"] and p["reference_pack"]["digest"] == PIN["reference_pack"]
               and p["cross_pin_model_pack_digest"] == PIN["model_pack"] for p in p4s)
    R["P-4"] = {"verdict": "GREEN" if p4ok and man["pack_digest"] == PIN["model_pack"] else "RED",
                "observed": {"cells_and_manifest_P4_verified": p4ok, "harness_measured_pack_digest": man["pack_digest"]}}
    p5_expect = {"winner_surface": "ARMED", "insufficient_energy_policy": "REFUSE", "regen_ungated": True,
                 "global_magnitude": "ARMED_UNCONDITIONAL", "measured_board_attached": True,
                 "per_cast_energy_column": "PARENT_PLUS_MODIFIER", "monster_march_base_m_per_s": 3.209466}
    p5_ok = (all(p5.get(k) == v for k, v in p5_expect.items())
             and "dot_corrections=True" in p5["loader_call"] and "pool_lift=ARMED" in p5["loader_call"]
             and "C11aLoader(CLASS)" in p5["loader_call"] and "winner_surface=ARMED" in p5["loader_call"]
             and p5["pcl_limb"] == "MULTIPLICATIVE @ 26.0 %" and "Disruption" in p5["non_health_route"]
             and "ManaBurnDrain" in p5["non_health_route"] and "PierceRatio" in p5["non_health_route"]
             and p5["monster_run_speed_population"] == "LAPR-MEASURED 128 · BANDA-DB-CITED 180 · FALLBACK 158"
             and "C3 NOT FOLDED" in p5["c11a"] and "CLASS" in p5["c11a"] and "C4" in p5["c11a"])
    R["P-5"] = {"verdict": "GREEN" if p5_ok else "RED", "observed": p5}

    # ---------------- C1 conformance (§ B.1a / § G): arms from their a8 rows, evidenced by G3 at the graded digest
    ac = man["arm_config_a8"]
    h4r = man["⚑ H4"]["a8_rowsets"]
    g3c = man["g3"]["per_cell"]
    c1 = {a: {"rowset_eq_B1a": ac[a]["rowset"] == A8_ROWSETS[a], "setup_C": ac[a]["setup_config_rowset"] == A8_ROWSETS["setup_C"],
              "probe_rows_applied": ac[a]["setup_probe_rows_applied"], "configured_from_a8": ac[a]["configured_from_a8"],
              "g3_pass_5_salts": all(g3c[f"{a}|{s}"]["passes"] and g3c[f"{a}|{s}"]["injected"] == []
                                     and g3c[f"{a}|{s}"]["decision_divergences"] == 0 and g3c[f"{a}|{s}"]["death"]["equal"]
                                     for s in SALTS)} for a in ARMS}
    R["C1"] = {"verdict": "CONFORMING" if all(v["rowset_eq_B1a"] and v["setup_C"] and v["probe_rows_applied"] == 0
                                              and v["g3_pass_5_salts"] for v in c1.values()) else "NON-CONFORMING",
               "observed": c1, "h4_rowsets": h4r}

    # ---------------- EXACT rows
    t1 = pre["⚑ TA-X-01_self_determinism"]
    R["TA-X-01"] = {"verdict": "GREEN" if (t1["identical"] and t1["digest_run_1"] == t1["digest_run_2"]
                                         and "M0 salt 2" in t1["probe"]) else "RED",
                    "observed": f"{t1['probe']}: {t1['digest_run_1'][:16]} == {t1['digest_run_2'][:16]}; "
                                f"arm+salt (M0, 2) != P-2's (M-POL-2, 0); equals the M0/2 cell digest "
                                f"{[c['digest'][:16] for c in man['cells'] if c['arm'] == 'M0' and c['salt'] == 2]}"}
    R["TA-X-02"] = {"verdict": R["P-1"]["verdict"], "observed": f"{p1['mapped']}/{p1['total']}, unmapped {p1['unmapped']}"}

    rel = man["⚑ relation_rows_RAW_not_graded"]
    p2_red = not p2["identical"]
    for rid, want_ident, rule in [("TA-X-03", True, "all"), ("TA-X-04", True, "all"), ("TA-X-05", False, "any")]:
        r = rel[rid]
        raw = (r["n_identical"] == 5) if want_ident else (r["n_identical"] <= 4)
        R[rid] = {"verdict": "UNGRADEABLE" if p2_red else ("GREEN" if raw else "RED"),
                  "observed": f"{r['compares']}: identical {r['n_identical']}/5 (raw relation "
                              f"{'holds' if raw else 'fails'}); P-2 RED -> UNGRADEABLE (v1.8 § B.3, carried)"}
    r6 = rel["TA-X-06"]
    R["TA-X-06"] = {"verdict": "UNGRADEABLE-declared (Q83(b), KP-110)",
                    "observed": f"W1 vs M-POL-2 identical on {r6['n_identical']}/5 salts "
                                f"({[p['salt'] for p in r6['per_salt'] if p['identical']]} identical)"}

    # TA-X-07
    rho = {k: float(cells[k]["conservation"]["residual_relative"]) for k in allc}
    l2 = {k: l2_cell(cells[k]) for k in allc}
    rb = man["r11_bound"]
    a_ok = all(v <= 1e-12 for v in rho.values())
    c_ok = all(v["holds"] for v in l2.values()) and rb["all_25_hold"] and rb["probe_bitwise"]
    worst = max(l2.items(), key=lambda kv: kv[1]["beta"])
    R["TA-X-07"] = {"verdict": ("GREEN" if a_ok and c_ok else ("RED" if not a_ok and c_ok else "UNGRADEABLE")),
                    "observed": {"(a) max rho_hat": max(rho.values()), "(a) cells at 0.0": sum(v == 0.0 for v in rho.values()),
                                 "(b) max |residual| (reported)": max(abs(float(cells[k]["conservation"]["residual"])) for k in allc),
                                 "(c) (L2) of record": "jack-ryan addendum c210b1979: 25/25 hold, worst beta 3.590829330577844e-14 (x27.85)",
                                 "(c) gamora cross-check from the graded cells' own operands": {
                                     "all_25_hold": c_ok, "worst_cell": "|".join(map(str, worst[0])),
                                     "worst_beta": worst[1]["beta"], "worst_margin": worst[1]["margin"]},
                                 "census": rb["census"]}}

    # TA-X-08
    t8 = {}
    for k in allc:
        ce = cells[k]["census"]
        i1, i2 = ce["⚑ TA-X-08_identity_1"], ce["⚑ TA-X-08_identity_2"]
        sc = ce["state_counts"]
        D = sum(sc.get(s, 0) for s in ("CHANNELLING", "CHANNELLING_AND_MOVING", "MOVING", "IDLE"))
        pre_f = sc.get("PRE_FIGHT", 0)
        id1 = i1["n_player_ticks_observed"] == D + pre_f
        id2 = i2["n_channelling"] + i2["n_released"] == D
        t8["|".join(map(str, k))] = {"observed": i1["n_player_ticks_observed"], "D": D, "PRE_FIGHT": pre_f,
                                     "DEAD": sc.get("DEAD", 0), "chan+rel": i2["n_channelling"] + i2["n_released"],
                                     "id1": id1, "id2": id2, "emitted_holds": [i1["holds"], i2["holds"]]}
    n_fail = sum(1 for v in t8.values() if not (v["id1"] and v["id2"]))
    R["TA-X-08"] = {"verdict": "RED" if n_fail else "GREEN",
                    "observed": f"identity 1 (n_player_ticks_observed == D + PRE_FIGHT) and identity 2 "
                                f"(n_channelling + n_released == D) FAIL on {n_fail}/25 cells, each by exactly 1 "
                                f"(the DEAD tick: DEAD = 1 on every cell)", "per_cell": t8}

    R["TA-X-09"] = {"verdict": "UNGRADEABLE", "observed": "no TA-X-09 value in the emission (the nine vectors' replay "
                    "is not in ta_manifest.json or any cell); supplementary tmp/kc2/t0/t0_report.json (05:32:11) reads "
                    "9/9 but is outside the MANIFEST and predates the graded tree's last runtime-content commit"}
    w1 = {s: cells[("W1", s)]["walls"]["max_body_radius_m"] for s in SALTS}
    R["TA-X-10"] = {"verdict": "GREEN" if all(v <= 43.758085029822276 for v in w1.values()) and
                    all(cells[("W1", s)]["walls"]["armed"] for s in SALTS) else "RED",
                    "observed": f"W1 max_body_radius_m {list(w1.values())}; max {max(w1.values())} <= 43.758085029822276"}
    cl = {(a, s): (cells[(a, s)]["walls"]["n_wall_clamps_player"], cells[(a, s)]["walls"]["n_wall_clamps_body"])
          for a in ("W1", "W1-NULL") for s in SALTS}
    R["TA-X-11"] = {"verdict": "GREEN" if all(v == (0, 0) for v in cl.values()) else "RED",
                    "observed": f"clamps (player, body) = (0, 0) on 10/10 (W1 wall armed r=43.7580850298223; vacuous "
                                f"on W1-NULL, § 0.2 NOTE). A port with no wall also scores zero (§ F.5 cl. 6)"}
    R["TA-X-12"] = {"verdict": "GREEN" if all(cells[k]["⚑ TA-X-12_pool_damage_total"] == 0.0 for k in allc) else "RED",
                    "observed": "pool damage 0.0 on 25/25; aprons ABSENT under ORACLE (armed false)"}
    R["TA-X-13"] = {"verdict": "GREEN" if all(cells[k]["⚑ TA-X-13_n_player_crits"] == 0 for k in allc) else "RED",
                    "observed": "n_player_crits 0 on 25/25; CritLimb.LO (x1.0) DRIVER-OF-RECORD"}
    t14 = all(cells[k]["release"]["⚑ TA-X-14_do_not_1"]["cause_energy_count"] == 0
              and set(cells[k]["release"]["causes"]) <= {"type_a", "type_b"} for k in allc)
    R["TA-X-14"] = {"verdict": "GREEN" if t14 else "RED",
                    "observed": f"cause==energy 0 on 25/25; release causes only type_a/type_b; n_release_events "
                                f"{min(cells[k]['release']['n_release_events'] for k in allc)}-"
                                f"{max(cells[k]['release']['n_release_events'] for k in allc)} per cell (event-scheduled)"}
    ok15 = True
    for k in allc:
        t = cells[k]["⚑ TA-X-15_release_schedule"]
        for row in t["per_wave_per_point"]:
            want = [49] if row["point"] == 5 else [0]
            if row["release_ticks"] != want or row["point"] not in (1, 2, 3, 4, 5):
                ok15 = False
        if t["n_intra_point_staggers"] != 0 or t["staggers"] or t["p05_release_tick_expected"] != 49:
            ok15 = False
    R["TA-X-15"] = {"verdict": "GREEN" if ok15 else "RED",
                    "observed": "(a) every (wave, point) row: p01-p04 release tick 0, p05 release tick 49 (4.000 s), "
                                "25/25; (b) 0 intra-point staggers, GREEN-BY-CONSTRUCTION (one release tick per point)"}
    # TA-X-16
    v11 = man["roster"]["⚑ TA-X-16_p06"]["V11-P06-1_expects"]
    picks = {k: cells[k]["board"]["n_pool_picks"] for k in allc}
    prefix_ok = all([w["pool_picks"] for w in cells[k]["board"]["per_wave"]] == v11[:len(cells[k]["board"]["per_wave"])]
                    for k in allc)
    p6 = sum(1 for k in allc for row in cells[k]["⚑ TA-X-15_release_schedule"]["per_wave_per_point"] if row["point"] == 6)
    n47 = sum(1 for v in picks.values() if v == 47)
    R["TA-X-16"] = {"verdict": "GREEN" if n47 == 25 and p6 == 0 else "RED",
                    "observed": {"n_pool_picks per cell": {"|".join(map(str, k)): v for k, v in picks.items()},
                                 "cells == 47": n47, "per-wave picks equal V11-P06-1 on every wave played": prefix_ok,
                                 "point-6 rows in any cell": p6,
                                 "manifest active_points_per_wave": man["roster"]["⚑ TA-X-16_p06"]["active_points_per_wave"],
                                 "filtered-key counter (manifest grain) picks_suppressed": man["roster"]["⚑ TA-X-16_p06"]["picks_suppressed"]}}
    R["TA-X-17"] = {"verdict": "GREEN-BY-CONSTRUCTION",
                    "observed": "ScatterLaw.POLAR_UNIFORM_RHO (DRIVER-OF-RECORD): rho = PLACEMENT_EXTENTS_M (8.0) * u2, "
                                "u2 in [0,1) (kc2rt_board.gd:600/784, scatter_polar_uniform_rho_f64) -> > 8.0 m impossible; "
                                "no per-body statistic emitted"}
    x18 = man["ta_x_18"]
    exp_bits = ["c00fffffffffffde", "be9777a5cf72cec6"]
    parsed = [struct.pack(">d", float(s)).hex() for s in x18["emitted"]]
    string_ok = all(len(s.replace("-", "").replace(".", "").split("e")[0].lstrip("0")) >= 17 or repr(float(s)) == s
                    for s in x18["emitted"])
    lossless = x18["emitter"] == "cpython-repr" and x18["roundtrip_probe"] and x18["lossless"] and string_ok
    R["TA-X-18"] = {"verdict": ("GREEN" if parsed == exp_bits else "RED") if lossless else "UNGRADEABLE",
                    "observed": {"emitted": x18["emitted"], "grader_parsed_bits": parsed, "expected_bits": exp_bits,
                                 "emitter": x18["emitter"], "roundtrip_probe": x18["roundtrip_probe"],
                                 "repr(float(s)) == s": string_ok}}
    R["TA-X-19"] = {"verdict": "GREEN",
                    "observed": "read at the graded tree (kc2rt_fight.gd): the deferred-arrival limb IS NOW PORTED for "
                                "projectiles (_defer_arrivals :4125); a packet carries {seq,b,rec,direct,pcl,fams,cast,n_rows} "
                                "(:4105) -- no arrival position -- and landing (_land :5577, _cp_absorb :3964) reads no "
                                "position. GREEN-VACUOUSLY has EXPIRED; graded by source at the pinned digest, no emitted counter"}
    R["TA-X-20"] = {"verdict": "UNGRADEABLE", "observed": "no TA-X-20 value in the emission; supplementary t0_report "
                    "(05:32:11, outside the MANIFEST, pre-final-tree) reads 2.99 hit / 3.01 miss / no angular gate / 12->12"}
    R["TA-X-21"] = {"verdict": "UNGRADEABLE", "observed": "no TA-X-21 value in the emission; supplementary t0_report + "
                    "kc2rt_purity_scan.json (05:28:37) read 12 rows / 0 violations, but predate 2ce053d (05:32:37), the "
                    "commit that removed a py_round from the walk because of THIS row's purity assertion"}
    R["TA-X-22"] = {"verdict": "GREEN" if all(cells[k]["release"]["⚑ TA-X-22_flag_cause_count"] == 0 for k in allc)
                    else "RED", "observed": "interrupts_channel_flag cause 0 on 25/25"}
    R["TA-X-24"] = {"verdict": "GREEN" if man["v0_limb_set"]["phase_model"]["value"] == "PhaseModel.ENGAGE" else "RED",
                    "observed": "PhaseModel.ENGAGE DRIVER-OF-RECORD (emitted); negative by source search at the graded "
                                "tree: no sha256 of any actor id (the sha256 sites are pack/register/leech-table digests, "
                                "the V9-STREAM-07 seed and kc2rt_kmill.seed_for's wave material)"}
    # TA-X-25
    pool, swing, nons = set(sets["_sets"]["POOL"]), set(sets["_sets"]["SWING"]), set(sets["_sets"]["NONSWING"])
    t25 = {}
    for k in allc:
        b = cells[k]["board"]["ta_x_25"]
        sbr = b["(c) spawn_by_record"]
        cnt = {"nodata_inert": 0, "measured_inert": 0, "measured_offense": 0}
        bad1, bad2, bad3 = [], [], []
        for rec, v in sbr.items():
            r = rec.lower()
            cnt[v["class"]] += v["n_bodies"]
            if r not in pool:
                bad1.append(rec)
            if r in swing and v["class"] != "measured_offense":
                bad2.append(rec)
            if r in nons and v["class"] not in ("nodata_inert", "measured_inert"):
                bad3.append(rec)
        a_ok = b["(a) n_nodata_refused"] == 0
        b_ok = (b["(b) n_nodata_spawn_inert"] + b["(b) n_measured_inert_spawn"] + b["(b) n_measured_offense_spawn"]
                == b["(b) n_bodies_spawned"])
        c4 = (cnt["nodata_inert"] == b["(b) n_nodata_spawn_inert"] and cnt["measured_inert"] == b["(b) n_measured_inert_spawn"]
              and cnt["measured_offense"] == b["(b) n_measured_offense_spawn"])
        nons_bodies = sum(v["n_bodies"] for rec, v in sbr.items() if rec.lower() in nons)
        t25["|".join(map(str, k))] = {"a": a_ok, "b": b_ok, "c1": not bad1, "c2": not bad2, "c3": not bad3, "c4": c4,
                                      "bodies": b["(b) n_bodies_spawned"], "nonswing_bodies (d, not graded)": nons_bodies}
    ok25 = all(all(v[x] for x in ("a", "b", "c1", "c2", "c3", "c4")) for v in t25.values())
    R["TA-X-25"] = {"verdict": "GREEN" if ok25 else "RED",
                    "observed": "(a) refused 0, 25/25 (satisfied over an empty refusal set); (b) the three counters present "
                                "and summing to n_bodies_spawned, 25/25; (c) against POOL-466 / SWING-456 / NONSWING-10 "
                                "recomputed here from the oracle (digests reproduce): (1)-(4) hold 25/25; (d) printed",
                    "per_cell": t25}
    t26 = man["manifest_blocks_other"]["ta_x_26"]
    e = t26["(e)"]
    ok26 = (t26["(a) join_consumption_audit"]["green"] and not t26["(a) join_consumption_audit"]["unaccounted"]
            and t26["(b) loaded"] and t26["(b) sha256_measured"] == PIN["P-i"] and t26["call_sites"]
            and t26["(c)"] == {"multipliers": 5, "records": 790, "rows": 7900, "tiers": 8, "wave_invariant": 790}
            and t26["(d)"]["formula_helper_call_sites"] == 1 and t26["(d)"]["formula_disagreements"] == 0
            and abs(e["mean"] - 0.2468965517) <= 5e-7 and abs(e["median"] - 0.25) <= 5e-7
            and abs(e["max"] - 0.35) <= 5e-7 and abs(e["min"] - 0.0) <= 5e-7 and e["n_zero"] == 17 and e["n"] == 464
            and sorted(cells[("M-POL-2", 0)]["⚑ V1-JOIN-1_leech_table"]["distinct_total_leech_resist_pct"])
            == [65.0, 75.0, 83.0, 88.0, 105.0, 115.0, 565.0, 588.0])
    R["TA-X-26"] = {"verdict": "GREEN" if ok26 else "RED",
                    "observed": f"(a) audit green, 0 unaccounted; (b) loaded, sha {t26['(b) sha256_measured'][:16]} = P-i, "
                                f"call site {t26['call_sites']}; (c) {t26['(c)']}; (d) helper call sites 1, disagreements 0; "
                                f"(e) ARMED-464 mean {e['mean']} median {e['median']} max {e['max']} min {e['min']} immune "
                                f"{e['n_zero']} (grain-labelled; the port's fight-armed 456 printed beside, not instead)"}
    t27 = man["manifest_blocks_other"]["ta_x_27"]
    g3 = man["g3"]
    g3ok = g3["all_25_pass"] and all(v["draw_mismatches"] == 0 and not v["port_only_streams"]
                                     and set(x.split("|")[0] for x in v["oracle_only_streams"])
                                     <= {"spawn_structure.py:344", "player_kit_residual.py:286"}
                                     for v in g3["per_cell"].values())
    R["TA-X-27"] = {"verdict": "UNGRADEABLE",
                    "observed": f"(a) scan {t27['(a)']['files_scanned']} files, short-circuits {t27['(a)']['short_circuits_found']}, "
                                f"unclassified {t27['(a)']['unclassified']} -> holds; (b) NOT EMITTED: the harness emits only a "
                                f"pointer to tmp/kc2/kc2rt_rules_smoke.json (outside the MANIFEST; 05:28:45; 58 checks / 0 failures) "
                                f"-> UNGRADEABLE; (c) {t27['(c)']}; G3 draw rules at the graded digest: {g3ok} -> holds; "
                                f"(d) {t27['(d)']['degenerate']}/{t27['(d)']['pairs']} -> holds"}
    ok28 = all(cells[k]["leech_law"]["n_leech_target_caps_applied"] == 0 and cells[k]["leech_law"]["n_leech_tick_caps_applied"] == 0
               and cells[k]["leech_law"]["scope"] == "ALL_BODIES_IN_DISC" and cells[k]["leech_law"]["weapon_portion"] == 0.57
               for k in allc)
    R["TA-X-28"] = {"verdict": "GREEN" if ok28 else "RED",
                    "observed": "(a) port target/tick caps 0/0 on 25/25 (no cap site exists: structural zero, § F.5 cl. 6); "
                                "oracle side derived from oracle code: player_sustain.py:19 'NO CAP IS INVENTED', run.py:805 "
                                "'per-body leech with no target cap and no per-tick cap'; (b) ALL_BODIES_IN_DISC, 0.57; "
                                "(c) same shape. A green says one leech law, not that it reproduces Matt's fight (cl. 10)"}
    gm = man["gmag_conformance"]
    def rec_ok(tab, w):
        got = {short(r): v["ratio"] for r, v in gm["per_record"][w].items()}
        miss = [n for n in tab if n not in got]
        extra = [n for n in got if n not in tab]
        dev = max(abs(got[n] - tab[n]) for n in tab if n in got)
        return {"n_expected": len(tab), "n_emitted": len(got), "missing": miss, "extra": extra, "max_dev": dev,
                "ok": not miss and not extra and dev <= 5e-4}
    e159, e160 = rec_ok(TA29_W159, "w159"), rec_ok(TA29_W160, "w160")
    tm = gm["terminal_multiplier"]
    e_ok = abs(tm["w159"] - 3.207764) <= 5e-4 and abs(tm["w160"] - 4.980316) <= 5e-4 and e159["ok"] and e160["ok"]
    a_ok29 = (gm["pred_gmag_whole"] and gm["attr_limb_records"] == 193 and gm["attr_lap_o"] == 154
              and gm["own_limb"] == 527 and gm["own_lap_o"] == 104 and gm["attr_limb_actors"] == 344)
    R["TA-X-29"] = {"verdict": "UNGRADEABLE",
                    "observed": {"(a)": f"PRED-GMAG-WHOLE {gm['pred_gmag_whole']}: attr 193/154 (actors 344), own 527/104 -> "
                                        f"{'holds' if a_ok29 else 'FAILS'}",
                                 "(b)": "NOT EMITTED at this digest (the v1.7 emission carried the Z5-LAW composition "
                                        "declaration and the 527-row clamp cross-check; this one does not)",
                                 "(c)": "NOT EMITTED as a check: M_inst per wave is printed (1.82 x5, 1.83 x5) but no "
                                        "z3_wave_damage_modifier_check comparison is asserted",
                                 "(d)": f"inert_records {gm['inert_records']}; 'unexercised: 0 of 29' not printed",
                                 "(e)": {"w159": tm["w159"], "w160": tm["w160"], "per_record_w159": e159,
                                         "per_record_w160": e160, "holds": e_ok}}}
    pur = man["manifest_blocks_other"]["pursuit"]
    ok30 = (pur["d_engage_m"] == 2.4 and pur["nan_test"] == {"d_engage": True, "nan": False, "predicate":
            pur["nan_test"]["predicate"], "zero": False}
            and all(cells[k]["pursuit"]["n_bodies_halted_beyond_d_engage"] == 0 for k in allc))
    R["TA-X-30"] = {"verdict": "GREEN" if ok30 else "RED",
                    "observed": "(a) halt at arena.json d_engage_m 2.4, NaN tested explicitly (nan rejected, zero rejected); "
                                "(b) n_bodies_halted_beyond_d_engage 0 on 25/25"}
    return R


# ======================================================================================== 5 · DIAGNOSTICS / REPORT FACE
def diagnostics(cells: dict, man: dict) -> dict:
    allc = [(a, s) for a in ARMS for s in SALTS]
    D = {"TA-B-01 terminal waves (port, M-POL-2)": man["⚑ terminal_5_vectors_RAW"]["M-POL-2"],
         "oracle M-POL-2 (v1.12 § B.1a)": ORACLE_TERMINALS["M-POL-2"],
         "printed beside TA-X-06: port W1": man["⚑ terminal_5_vectors_RAW"]["W1"], "oracle W1": ORACLE_TERMINALS["W1"],
         "terminal vectors, all arms": man["⚑ terminal_5_vectors_RAW"]}
    keys = ["TA-B-02_uptime", "TA-B-03_frac_moving", "TA-B-04_P_chan_given_moving", "TA-B-05_P_chan_given_stationary",
            "TA-B-06_plant_ratio", "TA-B-07_release_duty", "TA-B-09_channel_split"]
    per = {}
    for kk in keys:
        vals = [cells[("M-POL-2", s)]["census"][kk] for s in SALTS]
        per[kk] = {"per_salt": vals, "mean_of_salts": sum(vals) / 5}
    D["M-POL-2 per-tick (n = 5, mean of salts)"] = per
    D["TA-B-08 ordering holds"] = [cells[("M-POL-2", s)]["census"]["TA-B-08_ordering_holds"] for s in SALTS]
    D["TA-B-14 W1 vetoes / occupancy"] = [(cells[("W1", s)]["walls"]["n_avoidance_vetoes"],
                                          cells[("W1", s)]["walls"]["n_pool_occupancy_ticks"]) for s in SALTS]
    D["TA-B-15 (nodata bodies, fraction) per arm"] = {a: [(cells[(a, s)]["board"]["ta_b_15"]["n_nodata_spawn_inert"],
                                                         cells[(a, s)]["board"]["ta_b_15"]["fraction_of_bodies"])
                                                        for s in SALTS] for a in ARMS}
    # R-6 invariants (report face)
    inv1 = sum(1 for k in allc if cells[k]["terminal"]["killer_id"] and cells[k]["terminal"]["terminal_reason"] == "cleared")
    res = 0
    for k in allc:
        tr = cells[k]["hp_trace"]
        hit0 = False
        for row in tr:
            if row["hp"] <= 0.0:
                hit0 = True
            elif hit0:
                res += 1
                break
    inv3 = sum(1 for k in allc if cells[k]["⚑ pcl"]["n_pcl_attacks_landed"] > 0
               and not cells[k]["intake_by_damage_family"].get("PercentCurrentLife", 0) > 0)
    D["R-6"] = {"(i) killer_id set and cleared": inv1, "(ii) in-tick resurrections": res,
                "(iii) cells where a PCL row landed and PCL intake is not > 0": inv3}
    D["sustain (port, printed not asserted)"] = {a: [round(cells[(a, s)]["⚑ sustain"]["leech_over_intake"], 3) for s in SALTS]
                                                 for a in ARMS}
    return D


def main() -> int:
    ev = verify_evidence()
    sets = set_digests()
    man = json.loads(git_bytes(f"{EV}/ta_manifest.json"))
    cells = load_cells()
    R = grade(cells, man, sets)
    D = diagnostics(cells, man)
    exact = ["TA-X-%02d" % i for i in (1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24,
                                        25, 26, 27, 28, 29, 30)]
    assert len(exact) == 28
    cls = {}
    for r in exact:
        v = R[r]["verdict"]
        c = "GREEN" if v.startswith("GREEN") else v
        cls.setdefault(c, []).append(r)
    pre_red = [p for p in ("P-1", "P-2", "P-3", "P-4", "P-5") if R[p]["verdict"] != "GREEN"]
    if cls.get("RED"):
        verdict = "STRUCTURAL"
    elif cls.get("UNGRADEABLE") or pre_red:
        verdict = "INDETERMINATE"
    else:
        verdict = "PASS"
    sd_ok = all(sets[k]["digest"] == PIN[k] for k in ("POOL-466", "SWING-456", "NONSWING-10"))
    assert sets["POOL-466"]["routes_agree"]
    print("== EVIDENCE ==")
    print(f"  prereg {ev['prereg_sha256']} ok={ev['prereg_ok']}")
    print(f"  emission MANIFEST {ev['emission_MANIFEST_sha256']} members={ev['emission']['members']} "
          f"tree={ev['emission']['tree_digest_recomputed']} ok={ev['emission']['ok']}")
    print(f"  ta_manifest {ev['emission']['ta_manifest_sha256']}")
    print(f"  runtime tree {ev['runtime_tree']['recomputed']} ({ev['runtime_tree']['n_members']} members) "
          f"unchanged 0802ab1..9b0ad0c={ev['runtime_tree']['unchanged_0802ab1_to_9b0ad0c']} ok={ev['runtime_tree']['ok']}")
    print(f"  model pack {ev['model_pack']['digest']} ({ev['model_pack']['n']}); reference {ev['reference_pack']['digest']} "
          f"({ev['reference_pack']['n']}); cross-pin {ev['reference_pack']['cross_pin'][:16]} ok={ev['packs_ok']}")
    print(f"  G3 MANIFEST {ev['g3_MANIFEST_sha256']} ok={ev['g3_MANIFEST_ok']}")
    print(f"  H-9/H-10 docs ok={all(d['ok'] for d in ev['h9_h10_docs'].values())}")
    print(f"  set digests: { {k: (sets[k]['n'], sets[k]['digest'][:16]) for k in ('POOL-466','SWING-456','NONSWING-10')} } "
          f"reproduce={sd_ok}; FALLBACK-158: {sets['FALLBACK-158']}")
    print("== PRECONDITIONS ==")
    for p in ("P-1", "P-2", "P-3", "P-4", "P-5"):
        print(f"  {p}: {R[p]['verdict']}")
    print("== EXACT ROWS ==")
    for r in exact + ["TA-X-06"]:
        o = R[r]["observed"]
        print(f"  {r}: {R[r]['verdict']} :: {o if isinstance(o, str) else json.dumps(o, default=str)[:400]}")
    print("== COUNTS ==", {k: len(v) for k, v in cls.items()}, {k: v for k, v in cls.items() if k != "GREEN"})
    print("== R-6 ==", D["R-6"])
    print("== VERDICT ==", verdict)
    res = {"evidence": ev, "set_digests": {k: v for k, v in sets.items() if k != "_sets"}, "rows": R,
           "diagnostics": D, "counts": {k: len(v) for k, v in cls.items()}, "by_class": cls,
           "preconditions_not_green": pre_red, "verdict": verdict}
    (HERE / "results.json").write_text(json.dumps(res, indent=1, default=str) + "\n")

    # ------------------------------------------------------------------ the verdict file (§ G.3), assembled by the grader
    vf = {
        "schema": "kc2play.ta_verdict.v1",
        "prereg_version": "v1.12", "prereg_sha256": ev["prereg_sha256"],
        "substrate_epoch": "v3.7.1 / model 48a4c94c… / reference 1887257f…",
        "graded_attempt": "v1.12 attempt 1 (overall attempt 2 under the v1.8+ naming, § G.1)",
        "grader": "gamora", "emission": {"godot_commit": REV, "dir": EV, "MANIFEST_sha256": ev["emission_MANIFEST_sha256"],
                                         "ta_manifest_sha256": ev["emission"]["ta_manifest_sha256"]},
        "verdict": verdict,
        "attempt_consumed": verdict == "STRUCTURAL",
        "counts": res["counts"], "non_green_exact_rows": {k: v for k, v in cls.items() if k != "GREEN"},
        "preconditions": {p: R[p]["verdict"] for p in ("P-1", "P-2", "P-3", "P-4", "P-5")},
        "exact_rows": {r: R[r]["verdict"] for r in exact},
        "declared_ungradeable": [{"id": "TA-X-06", "authority": "Q83(b) / KP-110",
                                  "printed": R["TA-X-06"]["observed"]}],
        # ---- fields the harness EMITTED (carried from ta_manifest.json)
        "emitted_by_harness": {k: man[k] for k in ("arm_config_a8", "arm_of_record", "ta_x_18")} | {
            "g3_all_25_pass": man["g3"]["all_25_pass"], "r11_bound_all_25_hold": man["r11_bound"]["all_25_hold"],
            "model_pack": man["pack_digest"], "P5_folds": man["manifest_blocks_other"]["⚑ P5_folds"]},
        # ---- fields the harness did NOT emit, FILLED BY THE GRADER from pinned evidence (labelled; not 'emitted')
        "filled_by_grader_not_emitted": {
            "runtime_digest": {"value": ev["runtime_tree"]["recomputed"], "source": "recomputed from kc2_runtime/MANIFEST.json "
                               "over git blobs at 9b0ad0c (= drax's MANIFEST.runtime_tree_digest)"},
            "runtime_header": {"value": None, "note": "no header field emitted; the running harness measured pack "
                               f"{man['pack_digest']} and verified both packs + cross-pin (P4_pack)"},
            "cross_pin_verified": {"value": ev["reference_pack"]["cross_pin"] == ev["model_pack"]["digest"],
                                   "source": "grader recomputation; the harness emits it as P4_pack.cross_pin"},
            "oracle_containment_H9": {"value": "PASS (KP-146)", "docs": {k: ev["h9_h10_docs"][k]["sha256"] for k in
                                      ("H9_NOTE", "H9_W1", "H9_MPOL2", "H9_W1NULL", "H9_SCRIPT")}},
            "closure_H10": {"value": "DISCHARGED (KP-153)", "receipt": ev["h9_h10_docs"]["H10_receipt"]["sha256"]},
            "set_digests": {k: sets[k] for k in ("POOL-466", "SWING-456", "NONSWING-10", "FALLBACK-158")},
            "hole_closure": {"value": "PENDING (H-5, jack-ryan)", "note": "seal-blocking, not verdict-blocking (§ G.2)"},
            "port_holes_printed": {"value": True, "where": "the grade of record, § 8 (the harness printed none)"}},
        "r6_invariants": D["R-6"],
    }
    (HERE / "ta_verdict_v1p12_attempt1.json").write_text(json.dumps(vf, indent=1, default=str) + "\n")
    ok = ev["prereg_ok"] and ev["emission"]["ok"] and ev["runtime_tree"]["ok"] and ev["packs_ok"] and sd_ok
    print("evidence verified:", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
