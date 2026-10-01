#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.13 § G.1a · THE 28-ROW PRE-ATTEMPT READ — jack-ryan's grader (H-7).

PINNED BEFORE THE EMISSION IS READ. This file is committed ALONE, and its FILE sha256 is cited by the read, before any
byte of `evidence/kc2-play/2026-10-01-PRE-READ-NOT-A-GRADED-RUN-v1.13/` is opened. Every expected value, tolerance,
population, grain and antecedent applied here is quoted from prereg v1.13 (FILE c35cca9c…) or from the rows it carries
from v1.12 (FILE a0454776…) and, by reference, v1.8 / v1.10. The emission's FORMAT (field names) was learned from the
harness SOURCE at the candidate tree (godot 0f36826, tree d03ca891), never from the emission.

Not a verdict of record (§ G.1a item 3). Prints the § G verdict the emission WOULD take, and § F.5 rule 13's sentence.

Pre-pinned decision rules (stated here so they cannot be chosen after the read):
  R1  a field the row needs and the emission does not carry -> the row is UNGRADEABLE (never GREEN), EXCEPT where the
      prereg makes presence part of the row (TA-X-25(b)): there absence is RED.
  R2  P-2 is GREEN only if § B.3a (1)-(5) all hold. Controls (a)/(a0)/(b) are read off the emission; control (c)
      (the attempt-1 digest law reproducing its false RED) is not built by the T-A harness: it is accepted ONLY from
      (i) the emission folder, or (ii) the committed probe `kc2rt_attempt2_probes.gd` run by jack-ryan at the SAME
      runtime tree FILE (d03ca891), recorded in the read with its output. `--p2c <json>` passes (ii)'s result.
  R3  TA-X-08 is graded on v1.13 § F.2n.2 (1), (2) restated, (2p), with D / PRE_FIGHT per § F.2o: PRE_FIGHT == waves
      played, no DEAD, D == the census's live states; and M0 emits n_ticks_released == 0 (§ F.2n.4).
  R4  TA-X-16 is graded on v1.13 § F.2m.3 (a)-(d) at key grain with W = {151..T}, T the leg-A terminal wave (160 if
      cleared), against the vector pinned in § F.2m.2 (typed below AND re-derived from the pack and asserted equal).
  R5  TA-X-17 / TA-X-19: graded on an emitted per-body statistic if one exists; otherwise by source at the candidate
      tree, as the attempt-1 grade of record did (GREEN-BY-CONSTRUCTION / by source), with the source lines printed.
  R6  The read is GREEN overall only on 28/28 GREEN (BY-CONSTRUCTION counts as GREEN), P-1…P-5 GREEN, C1 conforming.

Run:  python3 <this file> [--p2c <json from the probe run>]   -> prints the read; writes <this>.results.json beside it
      (into the scratch dir given by --out, never the repo).
"""
from __future__ import annotations

import gzip
import hashlib
import json
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
REV = "0f36826"
EV = "evidence/kc2-play/2026-10-01-PRE-READ-NOT-A-GRADED-RUN-v1.13"
G3DIR = "evidence/kc2-play/2026-10-01-g3-25cell-kp184"
OUT = ENGINE / "src/reincarnated/output"
MODEL = OUT / "kc2-model-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247"
REFP = OUT / "kc2-reference-pack-v3-E-s09-cp150-mech-v3p7p1-20261001_021247"
ARMS = ["M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"]
SALTS = [0, 1, 2, 3, 4]
WAVES = list(range(151, 161))

PIN = {
    "prereg_v1.13": "c35cca9ceb189b5f78a09b402f9df81b3bb126db132643a57049eb1cc8a46d68",
    "prereg_v1.12": "a0454776ab91d85f37fadffcb8886a498e1f498f208e0eb33b9d5a9797fc7854",
    "runtime_tree": "d03ca8913901d61de73db40287e31e498e8b2714521f8221fde414682e328ccd",   # the candidate (KP-186)
    "g3_MANIFEST": "f861b7a16111531b1e0f7d8fc6358ffe78cc698202ec5f5645d295c6a903abbd",    # recomputed at H-3
    "model_pack": "48a4c94c165715d3f4f5db89c1278aa8439fbe1507c39dd555f7ce91d4636c96",
    "reference_pack": "1887257f5370443a1729fde2ff446579b1acc501dcd03679244297b541e3e5b1",
    "POOL-466": "33c886a11f91db1143c791ffcf9d95f7e7614e423373235231733c994c5c157b",
    "SWING-456": "706a61d55dc6621814fc923d7428c5b263a95ebb00e9786d12f35dd385a7a4c0",
    "NONSWING-10": "00b4cb0e24b43e591a2e30200979725801aad1e7c1f9b7764ebef67461816e10",
    "P-i": "cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e",
    "math_rules": "3b1e2d014411cb314d5cbf42ea40773dbcfa3de242f13d3a1d31eb830643b62d",
    "TA-X-09_rowset": "0e826ee093b98767901271c95e918a19e1c6d5b8a8663c99c87d8ced17086e78",
}
# the conductor's relay (KP-186), prefixes only: asserted, then the full values are printed
RELAYED = {"MANIFEST": "9ed1b999", "ta_manifest.json": "347f8bad", "ta_verdict.json": "8dc0a193"}
A8 = {"M0": "68549af0608cb9979771fcc4955ae8010f4f3516ad55a97b83922c994f571d12",
      "M-POL-2": "e698d5f555a37fcc12e703343286d4e25c12662d8cd35c9571f9a0ac8ae45dbf",
      "M-POL-2-NULL": "4393a14b56a97960ef42e73909a1cdefc49f3dc1a4cc41e7f20267b661a1a7b6",
      "W1": "5188284d198c139422276e8ac92f9a0bee03cea7dbb1cea32c6c7bf1d19a55e8",
      "W1-NULL": "b2abff6978105bfc1566d678d5f1dea756ea9ef0eab02f8457821f81125a7fdd",
      "setup_C": "207ab21f853b18ca026327bf6c9ddc4afa705d29cd3ef0868c1e7818d1672b4c"}
# v1.13 § F.2m.2 (pinned) — typed, then re-derived from the pack below and asserted equal
V11 = [5, 5, 5, 4, 4, 5, 5, 5, 5, 4]
P06KEY = [0, 1, 1, 0, 1, 1, 1, 1, 0, 1]
W1_BOUND = 43.758085029822276            # TA-X-10
EXTENTS = 8.0                            # TA-X-17
TA18_BITS = ["c00fffffffffffde", "be9777a5cf72cec6"]   # v1.12 § F.2l
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
EXACT = ["TA-X-%02d" % i for i in (1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24,
                                    25, 26, 27, 28, 29, 30)]
assert len(EXACT) == 28


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fsha(p: Path) -> str:
    return sha(p.read_bytes())


def gshow(path: str, rev: str = REV) -> bytes:
    return subprocess.run(["git", "-C", GODOT, "show", f"{rev}:{path}"], check=True, capture_output=True).stdout


def set_digest(s) -> str:
    return sha("\n".join(sorted(s)).encode("utf-8"))


class Missing(Exception):
    pass


def need(d, *keys):
    cur = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            raise Missing("/".join(str(x) for x in keys))
        cur = cur[k]
    return cur


def row(verdict: str, observed, **kw) -> dict:
    out = {"verdict": verdict, "observed": observed}
    out.update(kw)
    return out


def guarded(fn):
    """R1: a missing field makes the row UNGRADEABLE, never GREEN."""
    def w(*a, **k):
        try:
            return fn(*a, **k)
        except Missing as e:
            return row("UNGRADEABLE", f"field absent from the emission: {e}")
    return w


# ============================================================================ evidence
def verify_evidence() -> dict:
    out = {}
    pr = COLLAB / "agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.13.md"
    pr12 = COLLAB / "agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.12.md"
    out["prereg_v1.13"] = fsha(pr) == PIN["prereg_v1.13"]
    out["prereg_v1.12"] = fsha(pr12) == PIN["prereg_v1.12"]
    man_b = gshow(f"{EV}/MANIFEST.json")
    man = json.loads(man_b)
    out["MANIFEST_sha256"] = sha(man_b)
    bad, lines = [], []
    for m in man["members"]:
        b = gshow(f"{EV}/{m['path']}")
        if sha(b) != m["sha256"] or len(b) != m["bytes"]:
            bad.append(m["path"])
        lines.append(f"{m['path']}  {sha(b)}")
    members = sorted(m["path"] for m in man["members"])
    tracked = subprocess.run(["git", "-C", GODOT, "ls-tree", "-r", "--name-only", REV, EV + "/"],
                             check=True, capture_output=True, text=True).stdout.split()
    tracked = sorted(t[len(EV) + 1:] for t in tracked)
    out["members"] = len(members)
    out["member_failures"] = bad
    out["tracked_not_member"] = [t for t in tracked if t not in members]
    out["tree_digest_recomputed"] = sha("\n".join(sorted(lines)).encode())
    out["tree_digest_manifest"] = man.get("tree_digest")
    ph = man.get("⚑ pinned_harness_files", {})
    out["pinned_harness_files"] = ph
    tm, tv = sha(gshow(f"{EV}/ta_manifest.json")), sha(gshow(f"{EV}/ta_verdict.json"))
    out["ta_manifest_sha256"], out["ta_verdict_sha256"] = tm, tv
    out["both_pinned"] = all(f in members and h in json.dumps(ph.get(f), ensure_ascii=False)
                             for f, h in (("ta_manifest.json", tm), ("ta_verdict.json", tv)))
    out["relayed_prefixes_match"] = (out["MANIFEST_sha256"].startswith(RELAYED["MANIFEST"])
                                     and tm.startswith(RELAYED["ta_manifest.json"]) and tv.startswith(RELAYED["ta_verdict.json"]))
    out["filing_checks"] = man.get("⚑ filing_checks")
    out["identity"] = man.get("⚑ identity")
    # the runtime tree at REV, recomputed from git blobs (make_manifest law)
    rman = json.loads(gshow("kc2_runtime/MANIFEST.json"))
    rl, rbad = [], []
    for m in rman["members"]:
        g = sha(gshow("kc2_runtime/" + m["path"]))
        if g != m["sha256"]:
            rbad.append(m["path"])
        rl.append(f"{m['path']}  {g}")
    out["runtime_tree_recomputed"] = sha("\n".join(sorted(rl)).encode())
    out["runtime_tree_ok"] = out["runtime_tree_recomputed"] == rman["tree_digest"] == PIN["runtime_tree"] and not rbad
    out["g3_MANIFEST_ok"] = sha(gshow(f"{G3DIR}/MANIFEST.json")) == PIN["g3_MANIFEST"]

    def pack(d: Path, sub: str) -> dict:
        pm = json.loads((d / "manifest.json").read_text())
        pl, pbad = [], []
        for m in pm["members"]:
            g = fsha(d / m["path"])
            if g != m["sha256"]:
                pbad.append(m["path"])
            pl.append(f"{m['path']}  {g}")
        disk = sorted(str(p.relative_to(d)) for p in (d / sub).rglob("*") if p.is_file())
        return {"digest": sha("\n".join(sorted(pl)).encode()), "manifest_digest": pm["pack_digest"], "failures": pbad,
                "disk_equals_manifest": disk == sorted(m["path"] for m in pm["members"]),
                "cross_pin": (pm.get("cross_pin") or {}).get("model_pack_digest")}
    mp, rp = pack(MODEL, "model"), pack(REFP, "reference")
    out["packs_ok"] = (mp["digest"] == mp["manifest_digest"] == PIN["model_pack"] and not mp["failures"]
                       and mp["disk_equals_manifest"] and rp["digest"] == rp["manifest_digest"] == PIN["reference_pack"]
                       and not rp["failures"] and rp["disk_equals_manifest"] and rp["cross_pin"] == PIN["model_pack"])
    # the § F.2m.2 vector re-derived from the pack (R4)
    ws = json.loads((MODEL / "model/waves.json").read_text())["pools"]["wave_spawn"]
    pts = {w: {r["spawn_point"] for r in ws if r["global_wave"] == w} for w in WAVES}
    out["vector_rederived"] = ([len(pts[w] - {6}) for w in WAVES] == V11 and [int(6 in pts[w]) for w in WAVES] == P06KEY)
    return out


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
        wsf = WinnerSurfaceFold.from_x8("src/reincarnated/simulation/output/"
                                        "kc2-lifted-rows-KC2PLAY-SEALLAP-W1-c2-energy-fold-20260928_232836.json")
        roster, _p, _r = threat.load_profiles(dot_corrections=True, winner_surface=wsf, pool_lift=pool_lift.load(),
                                              c11a=C11aLoader(scope=AuraScope.CLASS))
        cs = {}
        for k, v in roster.items():
            s = v.can_swing
            cs[k.lower()] = bool(s() if callable(s) else s)
        swing = {r for r in pool if cs.get(r)}
        nons = pool - swing
    finally:
        os.chdir(cwd)
    return {"POOL": pool, "SWING": swing, "NONSWING": nons, "routes_agree": routes_agree,
            "ok": (set_digest(pool) == PIN["POOL-466"] and set_digest(swing) == PIN["SWING-456"]
                   and set_digest(nons) == PIN["NONSWING-10"] and routes_agree)}


# ============================================================================ (L2), § F.2k, exact
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
    lo = need(c, "conservation", "l2_operands")
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
    return {"beta": float(beta), "margin": float(TOL / beta) if beta else None, "lossless": lossless,
            "holds": beta <= TOL and lossless and lo["final_sum_n_terms"] == 6 and lo["sink_terms_present"] == 6
            and cc["n_unbound_pcl_rows"] == 0}


# ============================================================================ the rows
def grade(cells: dict, man: dict, ver: dict, sets: dict, p2c: dict | None) -> dict:
    R = {}
    allc = [(a, s) for a in ARMS for s in SALTS]
    pre = man.get("preconditions", {})

    # ---------------------------------------------------------------- P-1 … P-5
    @guarded
    def p1():
        p = need(pre, "P1_coverage")
        ok = p["mapped"] == p["total"] == 89 and p["unmapped"] == 0 and p.get("closes", True)
        return row("GREEN" if ok else "RED", {k: p.get(k) for k in ("mapped", "total", "unmapped", "closes", "counts")})
    R["P-1"] = p1()

    @guarded
    def p2():
        p = need(pre, "P2_stream_disjointness")
        f = need(p, "with_noop_fold", "fold")
        inv, forks, own = f.get("n_invocations"), f.get("n_forks"), p.get("noop_fold_draws")
        ticks_obs = need(p, "population", "ticks_observed")[1]
        c = {
            "(1) a real inserted fold, forked once, invoked every tick": bool(f.get("inserted")) and forks == 1
            and isinstance(inv, int) and inv > 0 and inv in (ticks_obs, f.get("n_ticks", ticks_obs)),
            "(2) a measured zero on its own stream": own == 0 and need(p, "with_noop_fold", "own_stream_draws_measured") == 0,
            "(3) one digest function, zero-draw = absent": "zero-draw site = absent site" in str(p.get("digest_function")),
            "digests identical": bool(p.get("identical")) and p.get("digest_plain") == p.get("digest_with_noop_fold"),
            "(4) controls (a), (a0), (b) not GREEN": bool(p.get("controls_all_not_green"))
            and all(v.get("state") != "GREEN" for v in need(p, "controls").values()) and len(p["controls"]) >= 3,
            "(4) control (c) RED (R2)": bool(p2c and p2c.get("control_c_red") is True
                                             and p2c.get("runtime_tree") == PIN["runtime_tree"]),
            "(5) fresh pack per leg": p.get("fresh_pack_per_leg") is True,
            "(5) plain leg carries no fold": p.get("plain_leg_has_no_fold") is True,
            "(5) no graded cell carries the fold": all("⚑ p2_noop_fold" not in cells[k] for k in allc),
            "harness says GREEN": p.get("green") is True and p.get("result") == "GREEN"}
        ok = all(c.values())
        st = "GREEN" if ok else ("NOT RUN" if not (c["(1) a real inserted fold, forked once, invoked every tick"]
                                                  and c["(2) a measured zero on its own stream"]) else "RED")
        return row(st, {"clauses": c, "n_invocations": inv, "ticks_observed_with_fold": ticks_obs,
                        "control_c_evidence": p2c})
    R["P-2"] = p2()

    @guarded
    def p3():
        p = need(pre, "P3_roll")
        ok = (p["population"] == "POOL-466" and p["cardinality"] == 466
              and p["law"] == {"alternative": "WEIGHTED:pool_weight", "name": "UNIFORM:randrange"})
        return row("GREEN" if ok else "RED", {k: p.get(k) for k in ("population", "cardinality", "law")})
    R["P-3"] = p3()

    @guarded
    def p4():
        ps = [need(cells[k], "⚑ P4_pack") for k in allc] + [need(man, "manifest_blocks_other", "⚑ P4_pack")]
        ok = all(p["verified"] and p["cross_pin"] and p["paired"] and p["mismatches"] == 0
                 and p["model_pack"]["digest"] == PIN["model_pack"] and p["reference_pack"]["digest"] == PIN["reference_pack"]
                 and p["cross_pin_model_pack_digest"] == PIN["model_pack"] for p in ps)
        ok = ok and man.get("pack_digest") == PIN["model_pack"]
        hdr = need(ver, "runtime_header")
        hdr_ok = hdr.get("equals_P4") is True and hdr.get("vendored_runtime_equals_runtime_digest") is True
        return row("GREEN" if ok and hdr_ok else "RED", {"26 P4 blocks verified": ok, "runtime_header ok": hdr_ok})
    R["P-4"] = p4()

    @guarded
    def p5():
        p = need(man, "manifest_blocks_other", "⚑ P5_folds")
        exp = {"winner_surface": "ARMED", "insufficient_energy_policy": "REFUSE", "regen_ungated": True,
               "global_magnitude": "ARMED_UNCONDITIONAL", "measured_board_attached": True,
               "per_cast_energy_column": "PARENT_PLUS_MODIFIER", "monster_march_base_m_per_s": 3.209466}
        ok = (all(p.get(k) == v for k, v in exp.items())
              and all(s in p["loader_call"] for s in ("dot_corrections=True", "pool_lift=ARMED", "C11aLoader(CLASS)",
                                                      "winner_surface=ARMED"))
              and p["pcl_limb"] == "MULTIPLICATIVE @ 26.0 %"
              and all(s in p["non_health_route"] for s in ("Disruption", "ManaBurnDrain", "PierceRatio"))
              and p["monster_run_speed_population"] == "LAPR-MEASURED 128 · BANDA-DB-CITED 180 · FALLBACK 158"
              and "C3 NOT FOLDED" in p["c11a"] and "CLASS" in p["c11a"] and "C4" in p["c11a"])
        return row("GREEN" if ok else "RED", p)
    R["P-5"] = p5()

    # ---------------------------------------------------------------- C1 (§ B.1a / § G; v1.13 § C.9.5a in G3)
    @guarded
    def c1():
        ac = need(man, "arm_config_a8")
        g3c = need(man, "g3", "per_cell")
        per = {}
        for a in ARMS:
            per[a] = {"rowset": ac[a]["rowset"] == A8[a], "setup_C": ac[a]["setup_config_rowset"] == A8["setup_C"],
                      "probe_rows_applied": ac[a]["setup_probe_rows_applied"] == 0,
                      "g3_5_salts": all(g3c[f"{a}|{s}"]["passes"] and g3c[f"{a}|{s}"]["injected"] == []
                                        and g3c[f"{a}|{s}"]["decision_divergences"] == 0
                                        and g3c[f"{a}|{s}"]["death"]["equal"]
                                        and g3c[f"{a}|{s}"].get("census_equal") is True
                                        and (g3c[f"{a}|{s}"].get("control_term") or {}).get("equal") is True
                                        for s in SALTS)}
        du = ver.get("declared_ungradeable")
        du_ok = isinstance(du, list) and [d.get("id") for d in du] == ["TA-X-06"]
        ok = all(all(v.values()) for v in per.values()) and need(man, "g3", "all_25_pass") is True and du_ok
        return row("CONFORMING" if ok else "NON-CONFORMING", {"per_arm": per, "declared_ungradeable": du})
    R["C1"] = c1()

    # ---------------------------------------------------------------- EXACT rows
    @guarded
    def t01():
        t = need(pre, "⚑ TA-X-01_self_determinism")
        named_diff = "M-POL-2 salt 0" not in t["probe"]
        ok = t["identical"] and t["digest_run_1"] == t["digest_run_2"] and named_diff
        return row("GREEN" if ok else "RED", {"probe": t["probe"], "identical": t["identical"]})
    R["TA-X-01"] = t01()
    R["TA-X-02"] = row(R["P-1"]["verdict"], R["P-1"]["observed"])

    p2_green = R["P-2"]["verdict"] == "GREEN"
    rel = man.get("⚑ relation_rows_RAW_not_graded", {})
    for rid, ident in (("TA-X-03", True), ("TA-X-04", True), ("TA-X-05", False)):
        r = rel.get(rid)
        if r is None:
            R[rid] = row("UNGRADEABLE", "relation row absent")
            continue
        raw = (r["n_identical"] == 5) if ident else (r["n_identical"] <= 4)
        R[rid] = row("UNGRADEABLE" if not p2_green else ("GREEN" if raw else "RED"),
                     f"{r.get('compares')}: identical {r['n_identical']}/5; raw relation {'holds' if raw else 'fails'}"
                     + ("" if p2_green else "; P-2 not GREEN -> UNGRADEABLE (v1.8 § B.3)"))
    r6 = rel.get("TA-X-06", {})
    R["TA-X-06"] = row("UNGRADEABLE-declared (Q83(b), KP-110)", f"W1 vs M-POL-2 identical {r6.get('n_identical')}/5")

    @guarded
    def t07():
        rho = {k: float(need(cells[k], "conservation", "residual_relative")) for k in allc}
        l2 = {k: l2_cell(cells[k]) for k in allc}
        rb = need(man, "r11_bound")
        cen = need(rb, "census")
        cen_ok = cen.get("sites") == 35 and cen.get("classes") == {"T": 22, "S": 11, "F": 14} and bool(cen.get("file"))
        a_ok = all(v <= 1e-12 for v in rho.values())
        c_ok = all(v["holds"] for v in l2.values()) and rb.get("all_25_hold") is True and rb.get("probe_bitwise") is True and cen_ok
        worst = max(l2.items(), key=lambda kv: kv[1]["beta"])
        v = "UNGRADEABLE" if not c_ok else ("GREEN" if a_ok else "RED")
        return row(v, {"(a) max rho": max(rho.values()), "(c) L2 25/25": sum(x["holds"] for x in l2.values()),
                       "worst": "|".join(map(str, worst[0])), "worst beta": worst[1]["beta"],
                       "worst margin": worst[1]["margin"], "census": cen},
                   l2_all_hold=c_ok)
    R["TA-X-07"] = t07()

    @guarded
    def t08():
        per, fails = {}, []
        for k in allc:
            c = cells[k]
            sc = need(c, "census", "state_counts")
            ctr = need(c, "ta_x_08_counters")
            t16 = need(c, "ta_x_16_counters")
            D = sum(sc.get(s, 0) for s in ("CHANNELLING", "CHANNELLING_AND_MOVING", "MOVING", "IDLE"))
            PF = sc.get("PRE_FIGHT", 0)
            obs = ctr["n_player_ticks_observed"]
            nch = sc.get("CHANNELLING", 0) + sc.get("CHANNELLING_AND_MOVING", 0)
            waves_played = len(t16["waves_played"])
            conv = (PF == waves_played and sc.get("DEAD", 0) == 0 and ctr["D"] == D and ctr["PRE_FIGHT"] == PF
                    and ctr["n_channelling"] == nch)
            id1 = obs == D + PF
            id2 = ctr["n_channelling"] + ctr["n_released"] + ctr["n_control_suppressed_channelling"] == D
            id2p = ctr["n_ticks_released"] == ctr["n_released"] + ctr["n_released_pre_fight"]
            m0 = (k[0] != "M0") or (ctr["n_ticks_released"] == 0 and ctr["n_released"] == 0)
            ok = conv and id1 and id2 and id2p and m0
            per["|".join(map(str, k))] = {"obs": obs, "D": D, "PF": PF, "waves": waves_played, "chan": ctr["n_channelling"],
                                          "rel": ctr["n_released"], "csc": ctr["n_control_suppressed_channelling"],
                                          "ntr": ctr["n_ticks_released"], "rel_pf": ctr["n_released_pre_fight"],
                                          "conv": conv, "id1": id1, "id2": id2, "id2p": id2p, "M0_ntr0": m0}
            if not ok:
                fails.append("|".join(map(str, k)))
        return row("RED" if fails else "GREEN", f"fails on {len(fails)}/25 {fails}", per_cell=per)
    R["TA-X-08"] = t08()

    @guarded
    def t09():
        t = need(man, "ta_x_09")
        rs = need(t, "rowset")
        ok = (t["n"] == 9 and t["all_replayed_to_the_law_and_the_stored_digits"] is True
              and rs["measured"] == PIN["TA-X-09_rowset"] and rs["equal"] is True
              and rs["math_rules_file_sha256"] == PIN["math_rules"])
        return row("GREEN" if ok else "RED", {"n": t["n"], "replayed": t["all_replayed_to_the_law_and_the_stored_digits"],
                                              "rowset": rs["measured"]})
    R["TA-X-09"] = t09()

    @guarded
    def t10():
        w = {s: need(cells[("W1", s)], "walls", "max_body_radius_m") for s in SALTS}
        armed = all(need(cells[("W1", s)], "walls", "armed") for s in SALTS)
        ok = armed and all(v <= W1_BOUND for v in w.values())
        return row("GREEN" if ok else "RED", {"max_body_radius_m": w, "armed": armed})
    R["TA-X-10"] = t10()

    @guarded
    def t11():
        cl = {f"{a}|{s}": (need(cells[(a, s)], "walls", "n_wall_clamps_player"), need(cells[(a, s)], "walls", "n_wall_clamps_body"))
              for a in ("W1", "W1-NULL") for s in SALTS}
        return row("GREEN" if all(v == (0, 0) for v in cl.values()) else "RED", cl)
    R["TA-X-11"] = t11()

    @guarded
    def t12():
        v = {k: need(cells[k], "⚑ TA-X-12_pool_damage_total") for k in allc}
        return row("GREEN" if all(x == 0.0 for x in v.values()) else "RED", f"max {max(v.values())}")
    R["TA-X-12"] = t12()

    @guarded
    def t13():
        v = {k: need(cells[k], "⚑ TA-X-13_n_player_crits") for k in allc}
        return row("GREEN" if all(x == 0 for x in v.values()) else "RED", f"max {max(v.values())}")
    R["TA-X-13"] = t13()

    @guarded
    def t14():
        ok = all(need(cells[k], "release", "⚑ TA-X-14_do_not_1", "cause_energy_count") == 0
                 and set(need(cells[k], "release", "causes")) <= {"type_a", "type_b"} for k in allc)
        extra = {kk: cells[("M-POL-2", 0)]["release"][kk] for kk in cells[("M-POL-2", 0)]["release"] if "TA-X-14" in kk}
        return row("GREEN" if ok else "RED", {"do_not_1 + causes": ok, "printed (M-POL-2|0)": extra})
    R["TA-X-14"] = t14()

    @guarded
    def t15():
        ok = True
        for k in allc:
            t = need(cells[k], "⚑ TA-X-15_release_schedule")
            for r in t["per_wave_per_point"]:
                if r["point"] not in (1, 2, 3, 4, 5) or r["release_ticks"] != ([49] if r["point"] == 5 else [0]):
                    ok = False
            if t["n_intra_point_staggers"] != 0 or t["staggers"] or t["p05_release_tick_expected"] != 49:
                ok = False
        return row("GREEN" if ok else "RED", "(a) p01-p04 tick 0, p05 tick 49 on every (wave, point); (b) by construction")
    R["TA-X-15"] = t15()

    @guarded
    def t16():
        per, fails = {}, []
        for k in allc:
            c = need(cells[k], "ta_x_16_counters")
            term = need(cells[k], "terminal")
            T = int(c.get("terminal_wave", term["terminal_wave"]))
            if term.get("terminal_reason") == "cleared":
                T = 160 if T in (160, 161) else T
            W = list(range(151, min(T, 160) + 1))
            wp = [int(x) for x in c["waves_played"]]
            picks = [int(x) for x in c["pool_picks_per_wave"]]
            r6 = [int(x) for x in c["n_spawn_point_6_keys_rolled_per_wave"]]
            filt = [int(x) for x in c["n_p06_keys_filtered_per_wave"]]
            exp = [V11[w - 151] for w in W]
            expk = [P06KEY[w - 151] for w in W]
            a = wp == W and picks == exp
            b = c["n_pool_picks"] == sum(exp)
            cc = c["n_spawn_point_6_keys_rolled"] == 0 and r6 == [0] * len(W)
            d = filt == expk
            per["|".join(map(str, k))] = {"T": T, "W": f"{W[0]}..{W[-1]}" if W else "[]", "waves_played": wp,
                                          "picks": picks, "(a)": a, "(b)": b, "(c)": cc, "(d)": d}
            if not (a and b and cc and d):
                fails.append("|".join(map(str, k)))
        return row("RED" if fails else "GREEN", f"fails on {len(fails)}/25 {fails}", per_cell=per)
    R["TA-X-16"] = t16()

    def t17():
        found = {}
        for k in allc:
            for kk, vv in cells[k].items():
                if "TA-X-17" in kk:
                    found["|".join(map(str, k))] = vv
        if found:
            mx = []
            for v in found.values():
                if isinstance(v, dict):
                    for kk, x in v.items():
                        if "max" in kk and isinstance(x, (int, float)):
                            mx.append(x)
            if mx:
                return row("GREEN" if max(mx) <= EXTENTS else "RED", f"emitted max offset {max(mx)} <= 8.0")
        # r2: the extents are read from the pack (arena.json placement_extents_m = 8.0), not typed in the source
        laws = gshow("kc2_runtime/sim/kc2rt_laws.gd").decode()
        board = gshow("kc2_runtime/sim/kc2rt_board.gd").decode()
        emit = gshow("kc2_runtime/tests/kc2rt_ta_emit.gd").decode()
        arena = json.loads((MODEL / "model/arena.json").read_text())["placement_extents_m"]["value"]
        hits = ([ln.strip() for ln in laws.splitlines() if "var rho := extents_m * u2" in ln]
                + [ln.strip() for ln in board.splitlines() if "scatter_polar_uniform_rho_f64(u1, u2, placement_extents_m" in ln]
                + [ln.strip() for ln in emit.splitlines() if 'get("placement_extents_m"' in ln])
        ok = arena == 8.0 and len(hits) == 4
        return row("GREEN-BY-CONSTRUCTION" if ok else "UNGRADEABLE",
                   {"no per-body statistic emitted; source at candidate (R5)": hits})
    R["TA-X-17"] = t17()

    @guarded
    def t18():
        x = need(man, "ta_x_18")
        parsed = [struct.pack(">d", float(s)).hex() for s in x["emitted"]]
        lossless = x["emitter"] == "cpython-repr" and x["roundtrip_probe"] and x["lossless"] and all(repr(float(s)) == s for s in x["emitted"])
        return row(("GREEN" if parsed == TA18_BITS else "RED") if lossless else "UNGRADEABLE",
                   {"emitted": x["emitted"], "bits": parsed}, lossless=lossless)
    R["TA-X-18"] = t18()

    def t19():
        src = gshow("kc2_runtime/sim/kc2rt_fight.gd").decode().splitlines()
        defer = [i + 1 for i, ln in enumerate(src) if "func _defer_arrivals" in ln]
        pkt = [ln.strip() for ln in src if '"seq"' in ln and '"rec"' in ln][:3]
        pos_in_pkt = any(('"px"' in p or '"py"' in p or '"x"' in p) for p in pkt)
        ok = bool(defer) and bool(pkt) and not pos_in_pkt
        return row("GREEN" if ok else "UNGRADEABLE", {"by source at candidate (R5)": {"_defer_arrivals": defer, "packet": pkt}})
    R["TA-X-19"] = t19()

    @guarded
    def t20():
        t = need(man, "ta_x_20")
        rows = t["rows"]
        want = {"2.99 m ahead — HIT": True, "3.01 m ahead — MISS": False, "3.0 m BEHIND — HIT (no angular gate)": True,
                "3.0 m to the side — HIT (no corridor)": True}
        got = {r["case"]: r for r in rows}
        ok = (t["green"] is True and t["radius_m"] == 3.0 and all(c in got and got[c]["got"] == v and got[c]["ok"] for c, v in want.items())
              and any("12 bodies" in r["case"] and r["got"] == 12 and r["ok"] for r in rows))
        return row("GREEN" if ok else "RED", [(r["case"], r["got"]) for r in rows])
    R["TA-X-20"] = t20()

    @guarded
    def t21():
        t = need(man, "ta_x_21")
        q = need(t, "quantisation")
        qrows = q.get("rows", [])
        ls = need(t, "oracle_live_sites")
        nb = need(t, "no_bare_round_on_the_port")
        eng = fsha(ENGINE / "src/reincarnated/simulation/kc2/threat.py")
        ok = (bool(qrows) and all(r.get("ok") is True for r in qrows) and ls["re_verified"] is True
              and ls["file_sha256"] == eng and nb["violations"] == 0 and (nb.get("files_scanned") or 0) > 0)
        return row("GREEN" if ok else "RED", {"quant rows ok": sum(r.get("ok") is True for r in qrows), "of": len(qrows),
                                              "live sites": [c.get("site") for c in ls["cited"]],
                                              "bare round violations": nb["violations"], "files scanned": nb.get("files_scanned")})
    R["TA-X-21"] = t21()

    @guarded
    def t22():
        ok = all(need(cells[k], "release", "⚑ TA-X-22_flag_cause_count") == 0 for k in allc)
        return row("GREEN" if ok else "RED", "interrupts_channel_flag cause count 0 on 25/25" if ok else "non-zero")
    R["TA-X-22"] = t22()

    @guarded
    def t24():
        v = need(man, "v0_limb_set", "phase_model", "value")
        return row("GREEN" if v == "PhaseModel.ENGAGE" else "RED", v)
    R["TA-X-24"] = t24()

    @guarded
    def t25():
        pool, swing, nons = sets["POOL"], sets["SWING"], sets["NONSWING"]
        per = {}
        for k in allc:
            b = need(cells[k], "board", "ta_x_25")
            names = ["(b) n_nodata_spawn_inert", "(b) n_measured_inert_spawn", "(b) n_measured_offense_spawn"]
            present = all(n in b for n in names)
            if not present:
                per["|".join(map(str, k))] = {"(b) presence": False}
                continue
            sbr = need(b, "(c) spawn_by_record")
            cnt = {"nodata_inert": 0, "measured_inert": 0, "measured_offense": 0}
            c1_, c2_, c3_ = True, True, True
            for rec, v in sbr.items():
                r = rec.lower()
                cnt[v["class"]] += v["n_bodies"]
                c1_ &= r in pool
                c2_ &= not (r in swing and v["class"] != "measured_offense")
                c3_ &= not (r in nons and v["class"] not in ("nodata_inert", "measured_inert"))
            per["|".join(map(str, k))] = {
                "(a)": b["(a) n_nodata_refused"] == 0,
                "(b)": b[names[0]] + b[names[1]] + b[names[2]] == b["(b) n_bodies_spawned"], "(b) presence": True,
                "(c1)": c1_, "(c2)": c2_, "(c3)": c3_,
                "(c4)": (cnt["nodata_inert"], cnt["measured_inert"], cnt["measured_offense"]) == (b[names[0]], b[names[1]], b[names[2]])}
        ok = sets["ok"] and all(all(v.values()) for v in per.values())
        return row("GREEN" if ok else "RED", f"set digests reproduce {sets['ok']}; cells all clauses {sum(all(v.values()) for v in per.values())}/25",
                   per_cell=per)
    R["TA-X-25"] = t25()

    @guarded
    def t26():
        t = need(man, "manifest_blocks_other", "ta_x_26")
        e = t["(e)"]
        ok = (t["(a) join_consumption_audit"]["green"] and not t["(a) join_consumption_audit"]["unaccounted"]
              and t["(b) loaded"] and t["(b) sha256_measured"] == PIN["P-i"] and t["call_sites"]
              and t["(c)"] == {"multipliers": 5, "records": 790, "rows": 7900, "tiers": 8, "wave_invariant": 790}
              and t["(d)"]["formula_helper_call_sites"] == 1 and t["(d)"]["formula_disagreements"] == 0
              and abs(e["mean"] - 0.2468965517) <= 5e-7 and abs(e["median"] - 0.25) <= 5e-7
              and abs(e["max"] - 0.35) <= 5e-7 and abs(e["min"] - 0.0) <= 5e-7 and e["n_zero"] == 17 and e["n"] == 464
              and sorted(need(cells[("M-POL-2", 0)], "⚑ V1-JOIN-1_leech_table", "distinct_total_leech_resist_pct"))
              == [65.0, 75.0, 83.0, 88.0, 105.0, 115.0, 565.0, 588.0])
        return row("GREEN" if ok else "RED", {"(c)": t["(c)"], "(e)": {k: e[k] for k in ("mean", "median", "max", "min", "n_zero", "n")}})
    R["TA-X-26"] = t26()

    @guarded
    def t27():
        t = need(man, "manifest_blocks_other", "ta_x_27")
        b = need(man, "ta_x_27_b")
        g3 = need(man, "g3")
        a_ok = t["(a)"]["short_circuits_found"] == 0 and t["(a)"]["unclassified"] == 0 and t["(a)"]["files_scanned"] > 0
        b_ok = (b["all_seeds_equal"] is True and b["python_exit_code"] == 0 and len(b["replay"]["per_seed"]) >= 1
                and all(p["results_equal"] and p["consumption_equal"] for p in b["replay"]["per_seed"]))
        c_ok = g3["all_25_pass"] is True and all(
            v["draw_mismatches"] == 0 and not v["port_only_streams"]
            and {x.split("|")[0] for x in v["oracle_only_streams"]} <= {"spawn_structure.py:344", "player_kit_residual.py:286"}
            for v in g3["per_cell"].values())
        d_ok = (b["pairs"]["n"] == 139 and b["pairs"]["degenerate"] == 97)
        ok = a_ok and b_ok and c_ok and d_ok
        return row("GREEN" if ok else "RED", {"(a)": a_ok, "(b) seeds": len(b["replay"]["per_seed"]), "(b)": b_ok,
                                              "(c)": c_ok, "(c) port note": t.get("(c)"), "(d)": (b["pairs"]["degenerate"], b["pairs"]["n"])})
    R["TA-X-27"] = t27()

    @guarded
    def t28():
        ok = all(need(cells[k], "leech_law", "n_leech_target_caps_applied") == 0
                 and cells[k]["leech_law"]["n_leech_tick_caps_applied"] == 0
                 and cells[k]["leech_law"]["scope"] == "ALL_BODIES_IN_DISC" and cells[k]["leech_law"]["weapon_portion"] == 0.57
                 for k in allc)
        return row("GREEN" if ok else "RED", "caps 0/0, ALL_BODIES_IN_DISC, 0.57 on 25/25" if ok else "fails")
    R["TA-X-28"] = t28()

    @guarded
    def t29():
        gm = need(man, "gmag_conformance")
        bcd = need(man, "ta_x_29_b_c_d")

        def short(rec):
            return rec.rsplit("/", 1)[-1].removesuffix(".dbr")

        def rec_ok(tab, w):
            got = {short(r): v["ratio"] for r, v in gm["per_record"][w].items()}
            miss = [n for n in tab if n not in got]
            extra = [n for n in got if n not in tab]
            dev = max(abs(got[n] - tab[n]) for n in tab if n in got)
            return not miss and not extra and dev <= 5e-4, dev
        a_ok = (gm["pred_gmag_whole"] and gm["attr_limb_records"] == 193 and gm["attr_lap_o"] == 154
                and gm["own_limb"] == 527 and gm["own_lap_o"] == 104 and gm["attr_limb_actors"] == 344)
        bb, cc, dd = bcd["(b)"], bcd["(c)"], bcd["(d)"]
        c5 = bb["c5_equals_z5_in_content"]   # r2: the emission carries a dict {unchanged, differ, added}, not a bool
        c5_ok = c5 is True or (isinstance(c5, dict) and c5.get("unchanged") is True and c5.get("differ") == [])
        b_ok = (c5_ok and bb["exercised"]["all_equal_to_the_law"] is True
                and bb["exercised"]["n_compositions"] > 0 and bb["exercised"]["dot_takes_nothing"]
                and bb["exercised"]["pcl_takes_nothing"] and bb["exercised"]["leech_dropped_from_health_path"] is True)
        c_ok = cc.get("green") is True and len(cc.get("waves", [])) == 10
        d_ok = dd["n_inert"] == 29 and dd["identity_path_on_all"] is True and dd["printed"] == "unexercised: 0 of 29"
        tm = gm["terminal_multiplier"]
        e159, dev159 = rec_ok(TA29_W159, "w159")
        e160, dev160 = rec_ok(TA29_W160, "w160")
        e_ok = abs(tm["w159"] - 3.207764) <= 5e-4 and abs(tm["w160"] - 4.980316) <= 5e-4 and e159 and e160
        ok = a_ok and b_ok and c_ok and d_ok and e_ok
        return row("GREEN" if ok else "RED", {"(a)": a_ok, "(b)": b_ok, "(c)": c_ok, "(d)": d_ok, "(e)": e_ok,
                                              "w159": tm["w159"], "w160": tm["w160"], "max dev": max(dev159, dev160)})
    R["TA-X-29"] = t29()

    @guarded
    def t30():
        pur = need(man, "manifest_blocks_other", "pursuit")
        ok = (pur["d_engage_m"] == 2.4 and pur["nan_test"].get("d_engage") is True and pur["nan_test"].get("nan") is False
              and pur["nan_test"].get("zero") is False
              and all(need(cells[k], "pursuit", "n_bodies_halted_beyond_d_engage") == 0 for k in allc))
        return row("GREEN" if ok else "RED", {"d_engage_m": pur["d_engage_m"], "nan_test": pur["nan_test"]})
    R["TA-X-30"] = t30()
    return R


def main() -> int:
    outdir = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else Path.cwd()
    p2c = json.loads(Path(sys.argv[sys.argv.index("--p2c") + 1]).read_text()) if "--p2c" in sys.argv else None
    ev = verify_evidence()
    sets = set_digests()
    man = json.loads(gshow(f"{EV}/ta_manifest.json"))
    ver = json.loads(gshow(f"{EV}/ta_verdict.json"))
    cells = {(a, s): json.loads(gshow(f"{EV}/{a}/{s}/cell.json")) for a in ARMS for s in SALTS}
    R = grade(cells, man, ver, sets, p2c)

    # identity of the run (v1.13 § G.1a items 1-2)
    rd = ver.get("runtime_digest", {})
    ident = {"prereg_version": ver.get("prereg_version"), "prereg_sha256 == v1.13": ver.get("prereg_sha256") == PIN["prereg_v1.13"],
             "carried_from v1.12": (ver.get("prereg_carried_from") or {}).get("sha256") == PIN["prereg_v1.12"],
             "run_kind": ver.get("run_kind"), "runtime_digest == candidate": rd.get("value") == PIN["runtime_tree"],
             "unchanged_through_the_run": rd.get("unchanged_through_the_run"),
             "boot-checked expected == candidate": (ver.get("pre_attempt_read") or {}).get("expected_runtime_digest") == PIN["runtime_tree"],
             "verdict null": ver.get("verdict") is None,
             "ta_manifest_sha256 in verdict file == filed": ver.get("ta_manifest_sha256") == ev["ta_manifest_sha256"]}

    cls = {}
    for r in EXACT:
        v = R[r]["verdict"]
        cls.setdefault("GREEN" if v.startswith("GREEN") else v, []).append(r)
    pre_not = [p for p in ("P-1", "P-2", "P-3", "P-4", "P-5") if R[p]["verdict"] != "GREEN"]
    if R["C1"]["verdict"] != "CONFORMING":
        would = "C1 (non-conforming)"
    elif cls.get("RED"):
        would = "STRUCTURAL"
    elif cls.get("UNGRADEABLE") or pre_not:
        would = "INDETERMINATE"
    else:
        would = "PASS"
    fire = would == "PASS" and len(cls.get("GREEN", [])) == 28 and all(ident.values()) and ev["runtime_tree_ok"]

    csc = {f"{a}|{s}": cells[(a, s)].get("ta_x_08_counters", {}).get("n_control_suppressed_channelling") for a in ARMS for s in SALTS}
    g3ct = [v.get("control_term", {}).get("port") for v in man.get("g3", {}).get("per_cell", {}).values()]
    g3_sum = sum(x for x in g3ct if isinstance(x, int))
    g3_eq = all(v.get("control_term", {}).get("equal") is True for v in man.get("g3", {}).get("per_cell", {}).values())
    vals = [x for x in csc.values() if isinstance(x, int)]
    rule13 = (f"`TA-X-08` identity 2 carries `n_control_suppressed_channelling`. On this run it was {sum(vals)} "
              f"(max {max(vals) if vals else 'n/a'} on one cell); in G3 it was {g3_sum} and equal to the oracle's on every "
              f"cell{'' if g3_eq else ' [NOT EQUAL ON EVERY CELL]'}. A GREEN `TA-X-08` on a run where the term is 0 everywhere "
              f"has not tested the control path; G3 has.")

    print("== EVIDENCE ==")
    for k in ("prereg_v1.13", "prereg_v1.12", "MANIFEST_sha256", "members", "member_failures", "tracked_not_member",
              "tree_digest_recomputed", "tree_digest_manifest", "ta_manifest_sha256", "ta_verdict_sha256", "both_pinned",
              "relayed_prefixes_match", "runtime_tree_recomputed", "runtime_tree_ok", "g3_MANIFEST_ok", "packs_ok",
              "vector_rederived"):
        print(f"  {k}: {ev[k]}")
    print("  filing_checks:", json.dumps(ev["filing_checks"], ensure_ascii=False)[:600])
    print("  set digests reproduce:", sets["ok"])
    print("== IDENTITY ==")
    for k, v in ident.items():
        print(f"  {k}: {v}")
    print("== PRECONDITIONS / C1 ==")
    for p in ("P-1", "P-2", "P-3", "P-4", "P-5", "C1"):
        print(f"  {p}: {R[p]['verdict']} :: {json.dumps(R[p]['observed'], default=str, ensure_ascii=False)[:700]}")
    print("== 28 EXACT ROWS ==")
    for r in EXACT + ["TA-X-06"]:
        print(f"  {r}: {R[r]['verdict']} :: {json.dumps(R[r]['observed'], default=str, ensure_ascii=False)[:500]}")
    print("== COUNTS ==", {k: len(v) for k, v in cls.items()}, {k: v for k, v in cls.items() if k != "GREEN"})
    print("== § G VERDICT THE EMISSION WOULD TAKE ==", would)
    print("== § F.5 RULE 13 ==", rule13)
    print("== FIRE (28/28 GREEN, identity, antecedents) ==", fire)
    res = {"evidence": ev, "identity": ident, "rows": R, "counts": {k: len(v) for k, v in cls.items()},
           "by_class": cls, "preconditions_not_green": pre_not, "would_take": would, "fire": fire, "rule13": rule13,
           "csc_per_cell": csc, "grader_sha256": fsha(Path(__file__))}
    (outdir / "pre_attempt_read.results.json").write_text(json.dumps(res, indent=1, default=str, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
