#!/usr/bin/env python3
"""[r2: ONE change vs the pinned grader (FILE 8efa88e3, collab 15cad337): the census-row regex took the f column as
\\d+; F-class rows carry f as an expression ("R+4", "2K+3"), so 14 F rows were not parsed. Field READ fixed; no expected
value, tolerance or rule touched.]
KC2-PLAY · H-2 + H-7 at the attempt-4 candidate — jack-ryan's grader (prereg v1.14 + v1.15 + v1.15 notes).

PINNED BEFORE THE EMISSION IS READ. Committed ALONE (collab) before any cell.json / ta_manifest.json / ta_verdict.json
of the pre-read emission is opened. Field names were learned from the harness SOURCE at godot ef5c04a (runtime tree
fd799b63), never from the emission. Every expected value / tolerance below is quoted from:
  v1.14 FILE 5bbe7ae5…  (§ 0.2, § B.1a, § B.6, § F.2m′, § F.2p, § F.5, § G.1a, § K, § L)
  v1.15 FILE d1c4a75a…  (§ F.2i′ TA-X-30 restated, § F.2h′ TA-X-29(b′) restated, (e) tables)
  notes FILE 7797ff17…  (§ 1 TA-X-13 scope, § 2 TA-X-21 live list, § 3 face rules, § 4 divisor unreachable)
and, for rows those files CARRY, from v1.13 / v1.12 / v1.8 as my v1.13 pre-attempt read applied them (grader-r2,
FILE a75b39f5…). (L2) is v1.12 § F.2k.3, evaluated in exact rationals.

NOT A VERDICT OF RECORD. NOT THE ATTEMPT. Consumes nothing (§ G.1a).

Pre-pinned decision rules:
  R1  a field a row needs and the emission lacks -> UNGRADEABLE (never GREEN); EXCEPT where the prereg makes presence part
      of the row (TA-X-25(b); TA-X-30 per v1.15 § F.2i′.2 "a missing field is a RED on presence") -> RED.
  R2  P-2 GREEN only if v1.8 § B.3a (1)-(5) hold; control (c) accepted only from the committed probe
      kc2rt_attempt2_probes.gd run by jack-ryan at the SAME tree FILE (passed as --p2c <json>).
  R3  TA-X-08 on v1.13 § F.2n.2 (1), (2) restated, (2p) + § F.2o (PRE_FIGHT == waves played, no DEAD, D == live states);
      M0 n_ticks_released == 0.
  R4  TA-X-16 on v1.14 § F.2m′ (a)-(d), W = {151..T}, T = first-death wave or 160 on a clear, LU-KEYS / P06-KEY typed
      here AND re-derived from the pack (waves.json; referent_lineup via the oracle module) and asserted equal.
  R5  a row graded by source (TA-X-19) prints the source lines at the candidate tree.
  R6  TA-X-07 is GREEN iff (a) rho_hat <= 1e-12 on 25/25 AND (L2) holds on 25/25 by MY exact evaluation (operands lossless,
      census verified by MY independent re-implementation against the candidate fight.gd, phi from each cell's counters,
      beta <= 1e-12 exactly). (L2) failing on a cell -> UNGRADEABLE (never RED).
  R7  The face items of the notes companion § 3 are PRINTED, never graded.
  R8  The read would FIRE only on 28/28 GREEN (GREEN-BY-CONSTRUCTION counts), P-1…P-5 GREEN, C1 CONFORMING, identity true.
      runtime_header (the .app) is printed separately: in scratch it is environment-absent; it is NOT one of the 28 rows.

Run: python3 grader_h7.py --ev <emission dir> --src <scratch godot root> --out <scratch out dir> [--p2c <json>]
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
from fractions import Fraction as Fr
from pathlib import Path

HOME = Path.home() / "Games"
COLLAB = HOME / "reincarnated-collaboration"
ENGINE = HOME / "reincarnated-engine"
NOTES = COLLAB / "agentic_orchestration/gandalf/notes"
OUT = ENGINE / "src/reincarnated/output"
MODEL = OUT / "kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143"
REFP = OUT / "kc2-reference-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143"
ARMS = ["M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"]
SALTS = [0, 1, 2, 3, 4]
WAVES = list(range(151, 161))

PIN = {
    "v1.14": "5bbe7ae5f0c3f73c77ee7cc3e21870ed8523b6d19fa1eae977dff451ef6b2d92",
    "v1.15": "d1c4a75ae2d35b2c27ddd127b18ef0066664eb54926e8466f2fe522a1ca34593",
    "notes": "7797ff17e5096b893aed3d041d8244165aebf34421a4252d1bfd9f91ab7ec752",
    "runtime_tree": "fd799b635734904a2f477795526a20c1bbce93b683cc9b8063e865e413804813",
    "native_lib": "74360ffae1a434ba0de85708009c8129c6b39c4ca03898a3e4be01641e27467f",
    "model_pack": "997117278c1e28dac0da9a6cf64ddaf72111347094a7ac5e3b4c03590507d788",
    "reference_pack": "af58ef4009029c99a618586f1bfccbd05a91fb381d49bd5483b7dce6eefeac1c",
    "POOL-466": "33c886a11f91db1143c791ffcf9d95f7e7614e423373235231733c994c5c157b",
    "EMPTY": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "P-i": "cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e",
    "TA-X-09_rowset": "0e826ee093b98767901271c95e918a19e1c6d5b8a8663c99c87d8ced17086e78",
}
# v1.14 § B.1a (the v3.11 a8 jobs)
A8 = {"setup": "7750a88f0c03c181ad0487e2d27567063910ebabb11b4fcb346c2e0c5f5532e8",
      "M0": "7c20aad10038076dccacc7e2c820d4fa32ff41466351fb7e9e8c8b18d03ec76c",
      "M-POL-2": "cf1c96e40535037d2c8dc42aa84615a9c0feca608d6a9d436fbb9e3c775e7ca7",
      "M-POL-2-NULL": "629b9271cc254833a45b2a0ff83d872712a0d99e273660221595dd71cda3505f",
      "W1": "5102fd732dde3f1c7a1bda7ea522be9ff15bc26acc86c3b640d6414d8ff8361e",
      "W1-NULL": "54934746784371a15caf6053e4379e4fb04d680202714cae68992af33bb1ca8f"}
# v1.14 § F.2m′ (typed; re-derived below and asserted equal)
LU = [5, 5, 5, 4, 4, 5, 5, 5, 5, 4]
LU_SETS = {w: ([1, 2, 3, 4] if w in (154, 155, 160) else [1, 2, 3, 4, 5]) for w in WAVES}
P06KEY = [0, 1, 1, 0, 1, 1, 1, 1, 0, 1]
W1_BOUND = 43.71638147965161          # TA-X-10, v1.14 RE-DERIVED
EXTENTS = 8.0                         # TA-X-17
TA18_BITS = ["c00fffffffffffde", "be9777a5cf72cec6"]
TA21_LIVE14 = ["control_application.py:591", "dot_timeline.py:380", "gd_engagement.py:121", "gd_engagement.py:187",
               "gd_reposition.py:364", "gd_reposition.py:365", "gd_reposition.py:519", "gd_reposition.py:530",
               "gd_reposition.py:554", "gd_reposition.py:726", "gd_reposition.py:731", "gd_reposition.py:739",
               "threat.py:1613", "threat.py:1774"]
TA21_DEAD3 = ["deferred_arrival.py:329", "threat.py:1813", "threat.py:2182"]
TA27C = {"registered_live_sites": 41, "V9": 29, "rg1_live": 12, "not_live": ["V311-RG-019"]}
DECLARED_ORACLE_ONLY = {"spawn_structure.py:344", "player_kit_residual.py:286"}   # stream keys (construction lines);
#   v1.14 § C.9.1′: identity carried, draw lines re-cited to :345 / :353 (checked against the engine source below)
# v1.15 § F.2h′ (e)
TA29_E = {"w159": 3.197066, "w160": 4.935649}
TA29_W159 = {"aetherial_fleshhulk_mine": 3.514042, "beetle_maggot01": 3.301094, "chthonianrylok_ekketzul": 3.59875,
             "chthonianservitor_lunalvalgoth": 2.546547, "humanwendigo_darkwood_01": 3.75048, "korvaakmessenger_02": 3.033476,
             "korvaakmessenger_02b": 3.034357, "manticore_jaggedwaste_01": 2.956584, "rokwind_01": 3.362895,
             "skeletalgolem_stepsoftorment_01": 3.120862, "statue_templeguardian_02": 1.960798,
             "statue_templeguardian_03": 1.960798, "stonegryphon_templeguardian_01": 2.762796,
             "wendigo_ancient_namadea": 4.077782, "witchgod_finalboss": 3.978465, "yeti_rimehorn_01": 3.080011}
TA29_W160 = {"aetherialcolossus_galakros": 3.80807, "nemesis_aetherial_01": 8.165613, "nemesis_aetherialvanguard_01": 6.466635,
             "nemesis_beast_01_p1": 3.829365, "nemesis_beast_02": 2.689026, "nemesis_chthonian_02": 5.55761,
             "nemesis_chthonianvoidborn_01": 4.517305, "nemesis_kymon_01": 3.474869, "nemesis_kymon_02": 1.075958,
             "nemesis_orderdeathsvigil_01": 6.921402, "nemesis_orderdeathsvigil_02": 3.658935, "nemesis_outlaw_01": 5.837726,
             "nemesis_outlaw_02": 5.07033, "nemesis_undead_01": 3.822594, "nemesis_undead_02b": 5.470426,
             "nemesis_wendigo_01": 6.06632, "nemesis_wendigo_02": 4.391011, "statue_korvaaktombguardian": 4.102804,
             "wendigocannibal_h01": 5.916297, "wendigocannibal_h02": 5.946459, "wendigocannibal_h03": 5.476449,
             "wendigocannibal_h04": 5.429514, "wendigocannibal_h05": 5.429514}
EXACT = ["TA-X-%02d" % i for i in (1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24,
                                    25, 26, 27, 28, 29, 30)]
assert len(EXACT) == 28


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fsha(p: Path) -> str:
    return sha(Path(p).read_bytes())


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


def guarded(fn, presence_red=False):
    def w(*a, **k):
        try:
            return fn(*a, **k)
        except Missing as e:
            return row("RED" if presence_red else "UNGRADEABLE", f"field absent from the emission: {e}")
    return w


# ============================================================================ (L2), v1.12 § F.2k, exact
U = Fr(1, 2 ** 53)
TOL = Fr(1, 10 ** 12)
K7 = ["offered", "applied", "dropped", "voided", "pool_truncated", "pcl_reclaim", "counterplay_absorbed"]


def gamma(k: int) -> Fr:
    k = max(k, 0)
    assert k * U < 1
    return k * U / (1 - k * U)


def g2(n: int) -> Fr:
    return gamma(n - 1) ** 2 if n >= 2 else Fr(0)


def l2_cell(c: dict, census_ok: bool) -> dict:
    lo = need(c, "conservation", "l2_operands")
    n, q, NI, tot = lo["n"], lo["q"], lo["N_inner"], lo["inner_totals"]
    strs = list(lo["A_hat"].values()) + list(lo["A_hat_inner"].values()) + [lo["offered"]]
    lossless = all(isinstance(s, str) and repr(float(s)) == s for s in strs)
    ah = {k: Fr(float(lo["A_hat"][k])) for k in K7}
    ahi = {I: Fr(float(lo["A_hat_inner"][I])) for I in ("stream", "pcl")}
    O = Fr(float(lo["offered"]))
    counts_ok = all(int(n[k]) * U < 1 for k in K7) and all(int(NI[I]) * U < 1 for I in ("stream", "pcl"))
    ap = {k: ah[k] / (1 - U - g2(n[k])) for k in K7}
    api = {I: ahi[I] / (1 - U - g2(tot[I + "_terms"])) for I in ("stream", "pcl")}
    cc = lo["census_counters"]
    fmax = max(cc["pkt_rows_max"] + 4, 2 * cc["dot_buckets_max"], 2 * cc["burn_n_due_max"] + 3)
    phi = gamma(2 * fmax)
    B = (sum((U + g2(n[k])) * ap[k] for k in K7)
         + (U + gamma(5) ** 2) * sum((1 + U + g2(n[j])) * ap[j] for j in K7[1:])
         + sum((U + g2(NI[I])) * api[I] for I in ("stream", "pcl"))
         + phi * sum(ap[k] for k in K7 if q[k] > 0))
    den = max(Fr(1), abs(O))
    beta = (1 + U) ** 2 * B / den
    lam = (ap["offered"] + api["stream"] + api["pcl"]
           + sum((2 + (phi / U if q[j] > 0 else 0)) * ap[j] for j in K7[1:])) / den
    holds = (beta <= TOL and lossless and counts_ok and census_ok and lo["final_sum_n_terms"] == 6
             and lo["sink_terms_present"] == 6 and cc["n_unbound_pcl_rows"] == 0)
    return {"beta": float(beta), "margin_exact": float(TOL / beta) if beta else None, "Lambda": float(lam),
            "M": float((1 / (U * 10 ** 12)) / lam) if lam else None, "f_max": fmax, "phi": float(phi),
            "lossless": lossless, "counts_ok": counts_ok, "n": {k: int(n[k]) for k in K7}, "q": {k: int(q[k]) for k in K7},
            "N_inner": dict(NI), "inner_totals": dict(tot), "census_counters": dict(cc), "holds": holds,
            "rho_hat": lo.get("residual_relative")}


def census_verify(fight_src: str, census_src: str) -> dict:
    """An INDEPENDENT re-implementation of the booking-census check (v1.12 § F.2k.4) in Python: parse SITES out of
    kc2rt_booking_census.gd, compare every row's code to the candidate fight.gd line, check flags per class, and grep
    the call sites with the census's own GIT_GREP pattern. Not the harness's verify()."""
    lines = fight_src.split("\n")
    rows = re.findall(r'^\s*\[(\d+),\s*"((?:[^"\\]|\\.)*)",\s*"(\w+)",\s*"((?:[^"\\]|\\.)*)",\s*"([TSF])",\s*"([^"]*)"',
                      census_src, flags=re.M)
    bad, listed = [], set()
    classes = {"T": 0, "S": 0, "F": 0}
    for ln, caller, acc, code, cls, f in rows:
        ln = int(ln)
        listed.add(ln)
        code = code.encode().decode("unicode_escape")
        got = lines[ln - 1].strip() if ln - 1 < len(lines) else ""
        if got != code:
            bad.append(f"line {ln}: `{got}` != census `{code}`")
        flagged = got.endswith(", true)") or " > 0, " in got or ", true, " in got
        if cls == "S" and not got.endswith(", true)"):
            bad.append(f"line {ln} S unflagged")
        if cls == "F" and not flagged:
            bad.append(f"line {ln} F unflagged")
        if cls == "T" and (got.endswith(", true)") or ", true, " in got):
            bad.append(f"line {ln} T flagged")
        classes[cls] += 1
    found = [i + 1 for i, s in enumerate(lines) if re.match(r'^\s*(_cons_add\("|_offer\()', s)]
    uncensused = [x for x in found if x not in listed]
    stale = [x for x in listed if x not in found]
    return {"rows": len(rows), "sites": len(listed), "call_sites_found": len(found), "classes": classes,
            "problems": bad, "uncensused": uncensused, "stale": stale,
            "green": not bad and not uncensused and not stale and len(rows) > 0}


# ============================================================================ pack-side re-derivations
def pack_digest(d: Path, sub: str) -> dict:
    pm = json.loads((d / "manifest.json").read_text())
    pl, pbad = [], []
    for m in pm["members"]:
        g = fsha(d / m["path"])
        if g != m["sha256"]:
            pbad.append(m["path"])
        pl.append(f"{m['path']}  {g}")
    return {"digest": sha("\n".join(sorted(pl)).encode()), "manifest_digest": pm["pack_digest"], "failures": pbad,
            "cross_pin": (pm.get("cross_pin") or {}).get("model_pack_digest")}


def rederive() -> dict:
    out = {}
    mp, rp = pack_digest(MODEL, "model"), pack_digest(REFP, "reference")
    out["packs"] = {"model": mp["digest"], "reference": rp["digest"], "cross_pin": rp["cross_pin"],
                    "ok": (mp["digest"] == mp["manifest_digest"] == PIN["model_pack"] and not mp["failures"]
                           and rp["digest"] == rp["manifest_digest"] == PIN["reference_pack"] and not rp["failures"]
                           and rp["cross_pin"] == PIN["model_pack"])}
    ws = json.loads((MODEL / "model/waves.json").read_text())["pools"]["wave_spawn"]
    pts = {w: {r["spawn_point"] for r in ws if r["global_wave"] == w} for w in WAVES}
    out["V11-P06-1"] = [len(pts[w] - {6}) for w in WAVES]
    out["P06-KEY"] = [int(6 in pts[w]) for w in WAVES]
    try:
        sys.path.insert(0, str(ENGINE / "src"))
        from reincarnated.simulation.kc2 import referent_lineup as rl
        lu = {w: sorted(int(k) for k in rl.REFERENT_LINEUP[w].keys()) for w in WAVES}
        out["LU_sets"] = {str(w): lu[w] for w in WAVES}
        out["LU"] = [len(lu[w]) for w in WAVES]
    except Exception as e:     # recorded, not swallowed: the typed vector then stands alone and the read says so
        out["LU_error"] = repr(e)
    out["vector_ok"] = (out["V11-P06-1"] == LU and out["P06-KEY"] == P06KEY
                        and out.get("LU") == LU and all(out.get("LU_sets", {}).get(str(w)) == LU_SETS[w] for w in WAVES))
    out["math_rules_sha256"] = fsha(MODEL / "model/math_rules.json")
    eng_head = subprocess.run(["git", "-C", str(ENGINE), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    out["engine_head"] = eng_head
    kc2 = ENGINE / "src/reincarnated/simulation/kc2"
    out["oracle_streams"] = {
        "spawn_structure.py:344": (kc2 / "spawn_structure.py").read_text().split("\n")[343].strip(),
        "spawn_structure.py:345": (kc2 / "spawn_structure.py").read_text().split("\n")[344].strip(),
        "player_kit_residual.py:286": (kc2 / "player_kit_residual.py").read_text().split("\n")[285].strip(),
        "player_kit_residual.py:353": (kc2 / "player_kit_residual.py").read_text().split("\n")[352].strip()}
    out["threat_py_sha256"] = fsha(kc2 / "threat.py")
    return out


# ============================================================================ the rows
def grade(cells: dict, man: dict, ver: dict, rd: dict, src: Path, p2c: dict | None) -> dict:
    R = {}
    allc = [(a, s) for a in ARMS for s in SALTS]
    K = lambda k: f"{k[0]}|{k[1]}"
    pre = man.get("preconditions", {})

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
            "(4) control (c) RED (R2)": bool(p2c and p2c.get("control_c_red") is True and p2c.get("runtime_tree") == PIN["runtime_tree"]),
            "(5) fresh pack per leg": p.get("fresh_pack_per_leg") is True,
            "(5) plain leg carries no fold": p.get("plain_leg_has_no_fold") is True,
            "(5) no graded cell carries the fold": all("⚑ p2_noop_fold" not in cells[k] for k in allc),
            "harness says GREEN": p.get("green") is True and p.get("result") == "GREEN"}
        ok = all(c.values())
        return row("GREEN" if ok else "RED", {"clauses": c, "n_invocations": inv, "ticks_observed": ticks_obs,
                                              "control_c_evidence": p2c})
    R["P-2"] = p2()

    @guarded
    def p3():
        p = need(pre, "P3_roll")
        ok = (p["population"] == "POOL-466" and p["cardinality"] == 466
              and p["law"] == {"alternative": "WEIGHTED:pool_weight", "name": "UNIFORM:randrange"})
        return row("GREEN" if ok else "RED", {k: p.get(k) for k in ("population", "cardinality", "law")},
                   note="v1.14 § L.2: P-3 is the INCUMBENT roll's law; the fought roll is graded by G3 / TA-X-16 / 25 / 27(c)")
    R["P-3"] = p3()

    @guarded
    def p4():
        ps = [need(cells[k], "⚑ P4_pack") for k in allc] + [need(man, "manifest_blocks_other", "⚑ P4_pack")]
        ok = all(p["verified"] and p["cross_pin"] and p["paired"] and p["mismatches"] == 0
                 and p["model_pack"]["digest"] == PIN["model_pack"] and p["reference_pack"]["digest"] == PIN["reference_pack"]
                 and p["cross_pin_model_pack_digest"] == PIN["model_pack"] for p in ps)
        ok = ok and man.get("pack_digest") == PIN["model_pack"] and rd["packs"]["ok"]
        hdr = ver.get("runtime_header") or {}
        return row("GREEN" if ok else "RED", {"26 P4 blocks verified + packs re-derived from disk": ok,
                                              "runtime_header (printed, R8)": {k: hdr.get(k) for k in
                                              ("read_by_running", "equals_P4", "vendored_runtime_equals_runtime_digest", "error")}})
    R["P-4"] = p4()

    @guarded
    def p5():
        p = need(man, "manifest_blocks_other", "⚑ P5_folds")
        exp = {"winner_surface": "ARMED", "insufficient_energy_policy": "REFUSE", "regen_ungated": True,
               "global_magnitude": "ARMED_UNCONDITIONAL", "measured_board_attached": True,
               "per_cast_energy_column": "PARENT_PLUS_MODIFIER", "monster_march_base_m_per_s": 3.209466}
        c = {k: p.get(k) == v for k, v in exp.items()}
        c["loader_call"] = all(s in str(p.get("loader_call")) for s in ("dot_corrections=True", "pool_lift=ARMED",
                                                                       "C11aLoader(CLASS)", "winner_surface=ARMED"))
        c["pcl_limb"] = str(p.get("pcl_limb")).startswith("MULTIPLICATIVE @ 26.0")
        c["non_health_route"] = all(s in str(p.get("non_health_route")) for s in ("Disruption", "ManaBurnDrain", "PierceRatio"))
        c["run_speed"] = p.get("monster_run_speed_population") == "LAPR-MEASURED 128 · BANDA-DB-CITED 180 · FALLBACK 158"
        c["c11a CLASS"] = "CLASS" in str(p.get("c11a"))
        h4p = (man.get("⚑ H4") or {}).get("problems")
        c["v3.8-v3.11 folds read off a8 (H-4 green, no problems)"] = (man.get("⚑ H4") or {}).get("green") is True and not h4p
        return row("GREEN" if all(c.values()) else "RED", {"clauses": c, "declared": p})
    R["P-5"] = p5()

    @guarded
    def c1():
        ac = need(man, "arm_config_a8")
        g3 = need(man, "g3")
        g3c = need(g3, "per_cell")
        per = {}
        for a in ARMS:
            cfg = ac[a]
            per[a] = {"rowset": cfg.get("rowset") == A8[a],
                      "configured_from_a8": cfg.get("configured_from_a8", True) is True,
                      "setup_probe_rows_applied 0": cfg.get("setup_probe_rows_applied", 0) == 0,
                      "g3_5_salts": all(g3c[f"{a}|{s}"].get("passes") is True and g3c[f"{a}|{s}"].get("injected") == []
                                        and g3c[f"{a}|{s}"].get("decision_divergences") == 0
                                        and g3c[f"{a}|{s}"].get("draw_mismatches") == 0
                                        and (g3c[f"{a}|{s}"].get("death") or {}).get("equal") is True
                                        and g3c[f"{a}|{s}"].get("census_equal") is True
                                        and (g3c[f"{a}|{s}"].get("control_term") or {}).get("equal") is True
                                        for s in SALTS)}
        du = ver.get("declared_ungradeable")
        du_ok = isinstance(du, list) and [d.get("id") for d in du] == ["TA-X-06"]
        ok = all(all(v.values()) for v in per.values()) and g3.get("all_25_pass") is True and du_ok
        return row("CONFORMING" if ok else "NON-CONFORMING", {"per_arm": per, "declared_ungradeable": du,
                                                              "g3_all_25_pass": g3.get("all_25_pass")})
    R["C1"] = c1()

    # ---------------------------------------------------------------- EXACT rows
    @guarded
    def t01():
        t = need(pre, "⚑ TA-X-01_self_determinism")
        named = "M0 salt 2" in t["probe"]
        ok = t["identical"] and t["digest_run_1"] == t["digest_run_2"] and named
        same_as_graded = t["digest_run_1"] == next((c["digest"] for c in man.get("cells", [])
                                                    if c["arm"] == "M0" and c["salt"] == 2), None)
        return row("GREEN" if ok else "RED", {"probe": t["probe"], "identical": t["identical"],
                                              "equals graded M0|2 digest": same_as_graded})
    R["TA-X-01"] = t01()
    R["TA-X-02"] = row(R["P-1"]["verdict"], R["P-1"]["observed"], note="v1.14 § L.1: 89/89 says the census is mapped, "
                       "not that the v3.11 oracle is covered (G3 is that evidence)")

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

    # TA-X-07 (and H-2)
    census = census_verify((src / "kc2_runtime/sim/kc2rt_fight.gd").read_text(),
                           (src / "kc2_runtime/tests/kc2rt_booking_census.gd").read_text())

    @guarded
    def t07():
        rho = {K(k): float(need(cells[k], "conservation", "residual_relative")) for k in allc}
        l2 = {K(k): l2_cell(cells[k], census["green"]) for k in allc}
        rb = need(man, "r11_bound")
        a_ok = all(v <= 1e-12 for v in rho.values())
        c_ok = all(v["holds"] for v in l2.values())
        harness_agrees = all((rb["per_cell"].get(k) or {}).get("L2_holds") == l2[k]["holds"] for k in l2)
        probe = rb.get("probe_bitwise") is True
        c_ok = c_ok and probe
        worst = max(l2.items(), key=lambda kv: kv[1]["beta"])
        v = "UNGRADEABLE" if not c_ok else ("GREEN" if a_ok else "RED")
        return row(v, {"(a) max rho_hat": max(rho.values()), "(c) L2 holds": f"{sum(x['holds'] for x in l2.values())}/25",
                       "worst cell": worst[0], "worst beta": worst[1]["beta"], "worst margin (1e-12/beta)": worst[1]["margin_exact"],
                       "census (independent)": {k: census[k] for k in ("rows", "sites", "call_sites_found", "classes", "green")},
                       "harness r11_bound agrees per cell": harness_agrees, "neumaier probe bitwise": probe,
                       "harness census": rb.get("census")},
                   per_cell_l2=l2, per_cell_rho=rho, census_full=census)
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
            per[K(k)] = {"obs": obs, "D": D, "PF": PF, "waves": waves_played, "chan": ctr["n_channelling"],
                         "rel": ctr["n_released"], "csc": ctr["n_control_suppressed_channelling"],
                         "ntr": ctr["n_ticks_released"], "rel_pf": ctr["n_released_pre_fight"],
                         "terminal": need(c, "terminal", "terminal_reason"),
                         "conv": conv, "id1": id1, "id2": id2, "id2p": id2p, "M0_ntr0": m0}
            if not ok:
                fails.append(K(k))
        return row("RED" if fails else "GREEN", f"fails on {len(fails)}/25 {fails}", per_cell=per)
    R["TA-X-08"] = t08()

    @guarded
    def t09():
        t = need(man, "ta_x_09")
        rs = need(t, "rowset")
        ok = (t["n"] == 9 and t["all_replayed_to_the_law_and_the_stored_digits"] is True
              and rs["measured"] == PIN["TA-X-09_rowset"] and rs["equal"] is True
              and rs["math_rules_file_sha256"] == rd["math_rules_sha256"])
        return row("GREEN" if ok else "RED", {"n": t["n"], "replayed": t["all_replayed_to_the_law_and_the_stored_digits"],
                                              "rowset": rs["measured"], "math_rules (pack file)": rd["math_rules_sha256"]})
    R["TA-X-09"] = t09()

    @guarded
    def t10():
        w = {s: need(cells[("W1", s)], "ta_x_10", "max_body_radius_m") for s in SALTS}
        sp = {s: cells[("W1", s)]["ta_x_10"].get("max_spawn_radius_m") for s in SALTS}
        pb = {s: cells[("W1", s)]["ta_x_10"].get("bound") for s in SALTS}
        armed = all(need(cells[("W1", s)], "walls", "armed") for s in SALTS)
        ok = armed and all(v <= W1_BOUND for v in w.values())
        return row("GREEN" if ok else "RED", {"bound (v1.14)": W1_BOUND, "max_body_radius_m": w, "max_spawn_radius_m": sp,
                                              "port-computed bound == v1.14": all(b == W1_BOUND for b in pb.values()),
                                              "armed": armed})
    R["TA-X-10"] = t10()

    @guarded
    def t11():
        cl = {f"{a}|{s}": (need(cells[(a, s)], "walls", "n_wall_clamps_player"), need(cells[(a, s)], "walls", "n_wall_clamps_body"))
              for a in ("W1", "W1-NULL") for s in SALTS}
        return row("GREEN" if all(v == (0, 0) for v in cl.values()) else "RED", cl,
                   note="§ F.5 cl. 6 / v1.14 § L.6: 'the port never needed to clamp', not 'the wall works'")
    R["TA-X-11"] = t11()

    @guarded
    def t12():
        v = {K(k): need(cells[k], "⚑ TA-X-12_pool_damage_total") for k in allc}
        return row("GREEN" if all(x == 0.0 for x in v.values()) else "RED", f"max {max(v.values())}")
    R["TA-X-12"] = t12()

    @guarded
    def t13():
        per = {K(k): need(cells[k], "⚑ TA-X-13") for k in allc}
        crit = {k: v["n_player_crit_rows"] for k, v in per.items()}
        nrows = {k: v["n_player_rows"] for k, v in per.items()}
        vac = [k for k, v in per.items() if v.get("vacuous")]
        ok = all(x == 0 for x in crit.values()) and not vac and all(x > 0 for x in nrows.values())
        legacy = {K(k): cells[k].get("⚑ TA-X-13_n_player_crits") for k in allc}
        return row("GREEN" if ok else ("UNGRADEABLE" if vac and all(x == 0 for x in crit.values()) else "RED"),
                   {"player crit rows (max)": max(crit.values()), "player rows (min / max)": (min(nrows.values()), max(nrows.values())),
                    "vacuous cells": vac, "legacy field max": max(x for x in legacy.values() if x is not None)},
                   note="notes § 1 (KP-248): source == player rows only; ps_ rows out of scope")
    R["TA-X-13"] = t13()

    @guarded
    def t14():
        ok = all(need(cells[k], "release", "⚑ TA-X-14_do_not_1", "cause_energy_count") == 0
                 and set(need(cells[k], "release", "causes")) <= {"type_a", "type_b"} for k in allc)
        return row("GREEN" if ok else "RED", {"do_not_1 + causes ⊆ {type_a, type_b}": ok})
    R["TA-X-14"] = t14()

    @guarded
    def t15():
        ok, n_p05 = True, 0
        for k in allc:
            t = need(cells[k], "⚑ TA-X-15_release_schedule")
            for r in t["per_wave_per_point"]:
                if r["point"] not in (1, 2, 3, 4, 5) or r["release_ticks"] != ([49] if r["point"] == 5 else [0]):
                    ok = False
                n_p05 += r["point"] == 5
            if t["n_intra_point_staggers"] != 0 or t["staggers"] or t["p05_release_tick_expected"] != 49:
                ok = False
        return row("GREEN" if ok else "RED", f"(a) p01-p04 tick 0, p05 tick 49 on every (wave, point); p05 rows {n_p05}; (b) by construction")
    R["TA-X-15"] = t15()

    @guarded
    def t16():
        per, fails = {}, []
        for k in allc:
            c = need(cells[k], "ta_x_16_counters")
            keys = need(cells[k], "ta_x_16_keys")
            term = need(cells[k], "terminal")
            T = int(term["terminal_wave"])
            T = 160 if term.get("terminal_reason") == "cleared" else T
            W = list(range(151, min(T, 160) + 1))
            wp = [int(x) for x in c["waves_played"]]
            fk = {int(w): sorted(int(x) for x in v) for w, v in keys["fought_keys_per_wave"].items()}
            ik = {int(w): sorted(int(x) for x in v) for w, v in keys["incumbent_keys_rolled_per_wave"].items()}
            r6 = [int(x) for x in c["n_spawn_point_6_keys_rolled_per_wave"]]
            filt = [int(x) for x in c["n_p06_keys_filtered_per_wave"]]
            a = (wp == W and all(fk.get(w) == LU_SETS[w] and len(fk.get(w, [])) == LU[w - 151] for w in W)
                 and all(ik.get(w) == LU_SETS[w] for w in W))
            b = c["n_pool_picks"] == sum(LU[w - 151] for w in W)
            cc = (c["n_spawn_point_6_keys_rolled"] == 0 and r6 == [0] * len(W)
                  and all(6 not in fk.get(w, []) and 6 not in ik.get(w, []) for w in W))
            d = filt == [P06KEY[w - 151] for w in W]
            per[K(k)] = {"T": T, "W": f"{W[0]}..{W[-1]}", "(a)": a, "(b)": b, "(c)": cc, "(d)": d,
                         "n_pool_picks": c["n_pool_picks"]}
            if not (a and b and cc and d):
                fails.append(K(k))
        ok = not fails and rd["vector_ok"]
        return row("GREEN" if ok else "RED", f"fails on {len(fails)}/25 {fails}; vector re-derived from pack + line-up = {rd['vector_ok']}",
                   per_cell=per)
    R["TA-X-16"] = t16()

    @guarded
    def t17():
        per = {K(k): need(cells[k], "ta_x_17") for k in allc}
        mx = max(float(v["max_offset_m"]) for v in per.values())
        src_ok = all("v3p8" in str(v.get("anchor_source")) and float(v.get("bound_m")) == EXTENTS for v in per.values())
        return row("GREEN" if mx <= EXTENTS and src_ok else "RED", {"max ‖spawn − anchor‖ (25 cells)": mx, "bound": EXTENTS,
                   "anchor source v3.8 GD emitter, extents 8.0 on 25/25": src_ok,
                   "anchor_source (M0|0)": per["M0|0"].get("anchor_source")})
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
        s = (src / "kc2_runtime/sim/kc2rt_fight.gd").read_text().splitlines()
        defer = [i + 1 for i, ln in enumerate(s) if "func _defer_arrivals" in ln]
        pkt = [ln.strip() for ln in s if '"seq"' in ln and '"rec"' in ln][:3]
        pos = any(('"px"' in p or '"py"' in p or '"x"' in p) for p in pkt)
        ok = bool(defer) and bool(pkt) and not pos
        return row("GREEN-BY-CONSTRUCTION" if ok else "UNGRADEABLE", {"by source at candidate (R5)": {"_defer_arrivals": defer, "packet": pkt}})
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
        blob = json.dumps(ls, ensure_ascii=False)
        live_cited = [s for s in TA21_LIVE14 if s in blob]
        ok = (bool(qrows) and all(r.get("ok") is True for r in qrows) and len(live_cited) == 14
              and nb["violations"] == 0 and (nb.get("files_scanned") or 0) > 0
              and str(ls.get("re_verified", ls.get("all_re_verified"))) in ("True", "true"))
        return row("GREEN" if ok else "RED", {"quant rows ok": f"{sum(r.get('ok') is True for r in qrows)}/{len(qrows)}",
                                              "notes § 2 live sites cited": f"{len(live_cited)}/14",
                                              "dead cited": [s for s in TA21_DEAD3 if s in blob],
                                              "bare round violations": nb["violations"], "files scanned": nb.get("files_scanned"),
                                              "live-site block keys": sorted(ls.keys()) if isinstance(ls, dict) else type(ls).__name__})
    R["TA-X-21"] = t21()

    @guarded
    def t22():
        ok = all(need(cells[k], "release", "⚑ TA-X-22_flag_cause_count") == 0 for k in allc)
        return row("GREEN" if ok else "RED", "interrupts_channel_flag cause 0 on 25/25" if ok else "non-zero")
    R["TA-X-22"] = t22()

    @guarded
    def t24():
        v = need(man, "v0_limb_set", "phase_model", "value")
        return row("GREEN" if v == "PhaseModel.ENGAGE" else "RED", v)
    R["TA-X-24"] = t24()

    def t25():
        try:
            v = need(ver, "ta_x_25")
        except Missing as e:
            return row("UNGRADEABLE", str(e))
        sets_ok = v.get("n_nonswing") == 0 and v.get("nonswing_digest") == PIN["EMPTY"] and v.get("swing_digest") == PIN["POOL-466"] \
            and v.get("n_swing") == 466
        per = {}
        for k in allc:
            nd = cells[k].get("nodata")
            if not isinstance(nd, dict) or not all(x in nd for x in ("refused", "nodata_spawn_inert", "measured_inert_spawn",
                                                                       "measured_offense_spawn", "bodies_spawned", "spawn_by_record")):
                per[K(k)] = {"(b) presence": False}
                continue
            cnt = {"nodata_inert": 0, "measured_inert": 0, "measured_offense": 0}
            c1_ = c2_ = True
            pool_ok = True
            for rec, x in nd["spawn_by_record"].items():
                cnt[x["class"]] = cnt.get(x["class"], 0) + x["n_bodies"]
                c2_ &= x["class"] == "measured_offense"   # SWING = POOL-466: every body measured_offense
            per[K(k)] = {"(a)": nd["refused"] == 0,
                         "(b)": nd["nodata_spawn_inert"] + nd["measured_inert_spawn"] + nd["measured_offense_spawn"] == nd["bodies_spawned"],
                         "(b) presence": True, "(c2) SWING -> measured_offense": c2_,
                         "(c4)": (cnt["nodata_inert"], cnt["measured_inert"], cnt["measured_offense"])
                         == (nd["nodata_spawn_inert"], nd["measured_inert_spawn"], nd["measured_offense_spawn"])}
        ok = sets_ok and all(all(x.values()) for x in per.values())
        return row("GREEN" if ok else "RED", {"SWING = POOL-466 / NONSWING = ∅ (digests)": sets_ok,
                                              "cells all clauses": f"{sum(all(x.values()) for x in per.values())}/25",
                                              "(c3)": "satisfied over an empty set (§ F.5 cl. 6)",
                                              "(c1) membership": "see per_cell; graded by G3 alive_set on the oracle's draws"},
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
              and abs(e["max"] - 0.35) <= 5e-7 and abs(e["min"] - 0.0) <= 5e-7 and e["n_zero"] == 17 and e["n"] == 464)
        return row("GREEN" if ok else "RED", {"(c)": t["(c)"], "(e)": {k: e[k] for k in ("mean", "median", "max", "min", "n_zero", "n")}})
    R["TA-X-26"] = t26()

    @guarded
    def t27():
        t = need(man, "manifest_blocks_other", "ta_x_27")
        b = need(man, "ta_x_27_b")
        cc = need(ver, "ta_x_27_c")
        g3 = need(man, "g3")
        a_ok = t["(a)"]["short_circuits_found"] == 0 and t["(a)"]["unclassified"] == 0 and t["(a)"]["files_scanned"] > 0
        b_ok = (b["all_seeds_equal"] is True and b["python_exit_code"] == 0 and len(b["replay"]["per_seed"]) >= 1
                and all(p["results_equal"] and p["consumption_equal"] for p in b["replay"]["per_seed"]))
        reg_ok = (cc["registered_live_sites"] == 41 and cc["V9"] == 29 and cc["rg1_live"] == 12
                  and cc["rg1_registered_not_live"] == ["V311-RG-019"])
        g3_ok = g3["all_25_pass"] is True and all(
            v["draw_mismatches"] == 0 and not v["port_only_streams"]
            and {x.split("|")[0] for x in v["oracle_only_streams"]} <= DECLARED_ORACLE_ONLY
            for v in g3["per_cell"].values())
        d_ok = (b["pairs"]["n"] == 139 and b["pairs"]["degenerate"] == 97)
        ok = a_ok and b_ok and reg_ok and g3_ok and d_ok
        return row("GREEN" if ok else "RED", {"(a)": a_ok, "(b) seeds": len(b["replay"]["per_seed"]), "(b)": b_ok,
                                              "(c) registry 41 = 29 V9 + 12 rg1": reg_ok, "(c) G3 draw rules": g3_ok,
                                              "(d)": (b["pairs"]["degenerate"], b["pairs"]["n"])})
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
            return not miss and not extra and dev <= 5e-4, dev, miss, extra
        a_ok = (gm["pred_gmag_whole"] and gm["attr_limb_records"] == 193 and gm["attr_lap_o"] == 154
                and gm["own_limb"] == 527 and gm["own_lap_o"] == 104 and gm["attr_limb_actors"] == 344)
        # (b′) — summed by ME over the per-cell blocks (v1.15 § F.2h′.1), constants exact
        fam, consts_ok, pcl_ok = {}, True, True
        for k in allc:
            b = need(cells[k], "ta_x_29_b")
            consts_ok &= (b.get("law") == "CompositionFold" and b.get("phys_limb") == "LO" and b.get("f_unmapped") == -0.44
                          and b.get("chaos_aether_dot_divisor") is True and b.get("lapm_wave") == 160)
            for f_, v in b["exercised"].items():
                if isinstance(v, dict):
                    fam.setdefault(f_, [0, 0])
                    fam[f_][0] += v["n"]
                    fam[f_][1] += v["n_equal_to_law"]
                elif f_ == "pcl_rows_untouched":
                    pcl_ok &= v is True
        tot = sum(v[0] for v in fam.values())
        ca = fam.get("dot_chaos_aether", [0, 0])[0]
        b_ok = consts_ok and pcl_ok and tot > 0 and all(v[0] == v[1] for v in fam.values()) and ca == 0
        cc, dd = bcd["(c)"], bcd["(d)"]
        c_ok = cc.get("green") is True and len(cc.get("waves", [])) == 10
        d_ok = dd["n_inert"] == 29 and dd["identity_path_on_all"] is True and dd["printed"] == "unexercised: 0 of 29"
        tm = gm["terminal_multiplier"]
        e159, dev159, m159, x159 = rec_ok(TA29_W159, "w159")
        e160, dev160, m160, x160 = rec_ok(TA29_W160, "w160")
        e_ok = abs(tm["w159"] - TA29_E["w159"]) <= 5e-4 and abs(tm["w160"] - TA29_E["w160"]) <= 5e-4 and e159 and e160
        ok = a_ok and b_ok and c_ok and d_ok and e_ok
        return row("GREEN" if ok else "RED", {"(a)": a_ok, "(b′)": b_ok, "(b′) families": fam, "(b′) constants": consts_ok,
                                              "(b′) chaos/aether rows (UNREACHABLE-IN-PACK; presence = RED)": ca,
                                              "(c)": c_ok, "(d)": d_ok, "(e)": e_ok, "w159": tm["w159"], "w160": tm["w160"],
                                              "max per-record dev": max(dev159, dev160), "missing/extra": [m159, x159, m160, x160],
                                              "manifest (b) block law": (bcd.get("(b)") or {}).get("law")})
    R["TA-X-29"] = t29()

    def t30():
        try:
            pm = need(man, "manifest_blocks_other", "pursuit")
        except Missing as e:
            return row("RED", f"presence: {e}")
        per, fails = {}, []
        req_tl = ["n_player_arg_steps", "n_unclipped", "n_unclipped_law_exact", "n_clipped", "n_clipped_shorter", "n_held",
                  "n_held_zero", "n_halt_flag_mismatch", "n_position_mismatch", "n_nan"]
        req_op = ["n_attack_stand", "n_pursue_reach", "n_default_ring_halt", "n_waypoint_op0", "n_reach_ne_pack", "n_op_ne_rule"]
        req_pe = ["n_steps", "n_no_travel_by_law", "n_moved_law_exact", "n_moved_clipped_shorter", "n_moved_against_law", "n_reach_ne_pack"]
        for k in allc:
            p = cells[k].get("pursuit")
            if not isinstance(p, dict):
                per[K(k)] = {"presence": False}
                fails.append(K(k))
                continue
            tl, op, pe = p.get("travel_law", {}), p.get("operand", {}), p.get("pets", {})
            missing = ([f"travel_law.{x}" for x in req_tl if x not in tl] + [f"operand.{x}" for x in req_op if x not in op]
                       + [f"pets.{x}" for x in req_pe if x not in pe]
                       + [x for x in ("n_bodies_halted_beyond_d_engage", "arena_armed", "n_clamp_calls", "n_clamp_stops") if x not in p])
            if missing:
                per[K(k)] = {"presence": False, "missing": missing}
                fails.append(K(k))
                continue
            g = (tl["n_unclipped_law_exact"] == tl["n_unclipped"] and tl["n_clipped_shorter"] == tl["n_clipped"]
                 and tl["n_held_zero"] == tl["n_held"] and tl["n_halt_flag_mismatch"] == 0 and tl["n_position_mismatch"] == 0
                 and tl["n_nan"] == 0 and op["n_reach_ne_pack"] == 0 and op["n_op_ne_rule"] == 0
                 and pe["n_moved_against_law"] == 0 and pe["n_reach_ne_pack"] == 0
                 and pe["n_moved_law_exact"] + pe["n_moved_clipped_shorter"] + pe["n_no_travel_by_law"] == pe["n_steps"]
                 and tl["n_player_arg_steps"] > 0 and p["n_bodies_halted_beyond_d_engage"] == 0)
            per[K(k)] = {"(a′)+(b′)": g, "roster steps": tl["n_player_arg_steps"], "unclipped": tl["n_unclipped"],
                         "held": tl["n_held"], "clipped": tl["n_clipped"], "pet steps": pe["n_steps"],
                         "pets exact/no-travel": (pe["n_moved_law_exact"], pe["n_no_travel_by_law"]),
                         "(b′) beyond": p["n_bodies_halted_beyond_d_engage"], "arena_armed": p["arena_armed"],
                         "clamp calls/stops": (p["n_clamp_calls"], p["n_clamp_stops"]),
                         "pursue_reach (non-waypoint)": op["n_pursue_reach"], "waypoint_op0": op["n_waypoint_op0"]}
            if not g:
                fails.append(K(k))
        m_ok = pm.get("ring_halt_m") == 2.4 and pm.get("nan_test", {}).get("nan") is False and pm.get("nan_test", {}).get("d_engage") is True
        presence_fail = any(v.get("presence") is False for v in per.values())
        v = "RED" if (fails or not m_ok) else "GREEN"
        return row(v, {"fails": fails, "manifest ring_halt_m 2.4 + NaN test": m_ok, "presence failures": presence_fail},
                   per_cell=per)
    R["TA-X-30"] = t30()
    return R


def face(cells: dict, man: dict, ver: dict, R: dict) -> dict:
    allc = [(a, s) for a in ARMS for s in SALTS]
    dig = {(c["arm"], c["salt"]): c["digest"] for c in man.get("cells", [])}
    term = {k: cells[k]["terminal"]["terminal_reason"] for k in allc}
    classes = {}
    for k in allc:
        classes.setdefault(dig.get(k), []).append(f"{k[0]}|{k[1]}")
    dying = {d: v for d, v in classes.items() if term[tuple([v[0].split("|")[0], int(v[0].split("|")[1])])] == "death"}
    out = {}
    out["trajectories"] = {"distinct (cell digest)": len(classes), "clear": len(classes) - len(dying), "die": len(dying),
                           "classes": sorted(classes.values(), key=lambda x: x[0]),
                           "reference": "25 cells / 12 distinct trajectories (9 clear, 3 die)"}
    out["ta_x_30_b_prime_vacuity"] = {}
    n_nonwp = n_clip = 0
    clip_flags = []
    for k in allc:
        p = cells[k].get("pursuit", {})
        stops = p.get("n_clamp_stops")
        out["ta_x_30_b_prime_vacuity"][f"{k[0]}|{k[1]}"] = {
            "arena_armed": p.get("arena_armed"), "n_clamp_calls": p.get("n_clamp_calls"), "n_clamp_stops": stops,
            "face": "(b′) vacuous: no clamp stopped a body" if stops == 0 else f"(b′) tested: {stops} clamp stops"}
        n_nonwp += (p.get("operand") or {}).get("n_pursue_reach", 0)
        nc = (p.get("travel_law") or {}).get("n_clipped", 0) + (p.get("pets") or {}).get("n_moved_clipped_shorter", 0)
        n_clip += nc
        if nc:
            clip_flags.append(f"{k[0]}|{k[1]}: {nc}")
    out["unexercised_on_referent"] = {"non-waypoint Pursue operand (port steps)": n_nonwp, "non-penetration clip (port steps)": n_clip}
    out["clip_flag"] = clip_flags or "none (0 clipped steps on 25/25)"
    out["ta_x_08_lethal_tick"] = f"exercised on {len(dying)} distinct dying trajectories ({[v for v in dying.values()]}); inapplicable on the clearing cells (§ F.5 cl. 15)"
    out["harness_face_block"] = ver.get("face")
    return out


def main() -> int:
    a = sys.argv
    ev = Path(a[a.index("--ev") + 1])
    src = Path(a[a.index("--src") + 1])
    outdir = Path(a[a.index("--out") + 1])
    p2c = json.loads(Path(a[a.index("--p2c") + 1]).read_text()) if "--p2c" in a else None
    ident = {}
    ident["v1.14"] = fsha(NOTES / "2026-09-20-kc2-play-ta-prereg-v1.14.md") == PIN["v1.14"]
    ident["v1.15"] = fsha(NOTES / "2026-09-20-kc2-play-ta-prereg-v1.15.md") == PIN["v1.15"]
    ident["notes"] = fsha(NOTES / "2026-09-20-kc2-play-ta-prereg-v1.15-notes.md") == PIN["notes"]
    rman = json.loads((src / "kc2_runtime/MANIFEST.json").read_text())
    rl, rbad = [], []
    for m in rman["members"]:
        g = fsha(src / "kc2_runtime" / m["path"])
        rbad += [m["path"]] if g != m["sha256"] else []
        rl.append(f"{m['path']}  {g}")
    ident["runtime_tree_recomputed"] = sha("\n".join(sorted(rl)).encode())
    ident["runtime_tree_ok"] = ident["runtime_tree_recomputed"] == PIN["runtime_tree"] and not rbad
    ident["native_lib"] = fsha(src / "kc2_runtime/native/bin/libkc2rt_contact.macos.arm64.dylib") == PIN["native_lib"]
    rd = rederive()
    man = json.loads((ev / "ta_manifest.json").read_text())
    ver = json.loads((ev / "ta_verdict.json").read_text())
    cells = {(x, s): json.loads((ev / x / str(s) / "cell.json").read_text()) for x in ARMS for s in SALTS}
    rdg = ver.get("runtime_digest", {})
    ident.update({"prereg_version": ver.get("prereg_version"), "prereg_sha256 == v1.15": ver.get("prereg_sha256") == PIN["v1.15"],
                  "set of record": ver.get("prereg_set_of_record") == {"v1.14": PIN["v1.14"], "v1.15": PIN["v1.15"], "v1.15_notes": PIN["notes"]},
                  "run_kind": ver.get("run_kind"), "verdict null": ver.get("verdict") is None,
                  "runtime_digest == candidate": rdg.get("value") == PIN["runtime_tree"],
                  "unchanged_through_the_run": rdg.get("unchanged_through_the_run"),
                  "ta_manifest_sha256 in verdict == file": ver.get("ta_manifest_sha256") == fsha(ev / "ta_manifest.json")})
    R = grade(cells, man, ver, rd, src, p2c)
    F = face(cells, man, ver, R)
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
    idok = all(ident[k] is True for k in ("v1.14", "v1.15", "notes", "runtime_tree_ok", "native_lib", "prereg_sha256 == v1.15",
                                         "set of record", "verdict null", "runtime_digest == candidate", "unchanged_through_the_run",
                                         "ta_manifest_sha256 in verdict == file")) and ident["run_kind"] == "pre_read"
    fire = would == "PASS" and len(cls.get("GREEN", [])) == 28 and idok
    print("== IDENTITY ==")
    for k, v in ident.items():
        print(f"  {k}: {v}")
    print("== RE-DERIVED ==", json.dumps({k: rd[k] for k in rd if k != "LU_sets"}, ensure_ascii=False)[:1500])
    print("== PRECONDITIONS / C1 ==")
    for p in ("P-1", "P-2", "P-3", "P-4", "P-5", "C1"):
        print(f"  {p}: {R[p]['verdict']} :: {json.dumps(R[p]['observed'], default=str, ensure_ascii=False)[:900]}")
    print("== 28 EXACT ROWS ==")
    for r in EXACT + ["TA-X-06"]:
        print(f"  {r}: {R[r]['verdict']} :: {json.dumps(R[r]['observed'], default=str, ensure_ascii=False)[:900]}")
    print("== COUNTS ==", {k: len(v) for k, v in cls.items()}, {k: v for k, v in cls.items() if k != "GREEN"})
    print("== § G VERDICT THE EMISSION WOULD TAKE ==", would)
    print("== FACE ==", json.dumps({k: v for k, v in F.items() if k != "harness_face_block"}, ensure_ascii=False, default=str)[:4000])
    print("== FIRE (R8) ==", fire)
    res = {"identity": ident, "rederived": rd, "rows": R, "counts": {k: len(v) for k, v in cls.items()}, "by_class": cls,
           "preconditions_not_green": pre_not, "would_take": would, "fire": fire, "face": F,
           "grader_sha256": fsha(Path(__file__))}
    (outdir / "h7_results.json").write_text(json.dumps(res, indent=1, default=str, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
