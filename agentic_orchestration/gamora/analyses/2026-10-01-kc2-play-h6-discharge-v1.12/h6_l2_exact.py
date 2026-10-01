#!/usr/bin/env python3
"""KC2-PLAY · H-6 discharge for T-A prereg v1.12 (FILE a0454776...) -- gamora, 2026-10-01.

Independent evaluation of § F.2k (L2) on all 25 cells, in EXACT RATIONALS (fractions.Fraction over
the emitted binary64 values; jack-ryan v1.12 pre-read INFO-2), plus the antecedents, the census
check and the re-pins. READ-ONLY on godot: every byte is read through `git show <rev>:<path>`;
nothing is checked out, run or written there.

Run:  python3 h6_l2_exact.py            (prints the report; writes results.json beside this file)
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import struct
import subprocess
import sys
from fractions import Fraction as Fr
from pathlib import Path

GODOT = str(Path.home() / "Games" / "reincarnated-godot")
REV_RT = "ada8048"        # drax: runtime tree fda00e28... (graded-digest candidate)
REV_ST = "e40a4fc"        # drax: AGENT_STATE with the 25 lossless operand lines
HERE = Path(__file__).resolve().parent

U = Fr(1, 2 ** 53)
TOL = Fr(1, 10 ** 12)     # clause (a)/(L2) tolerance 1e-12, read as the decimal 10^-12 exactly
K7 = ["offered", "applied", "dropped", "voided", "pool_truncated", "pcl_reclaim", "counterplay_absorbed"]
SINKS = K7[1:]

# Expected digests, as REPORTED by drax / the brief. Each is recomputed below; a mismatch fails the run.
EXPECT = {
    "kc2_runtime/sim/kc2rt_fight.gd": "5dfb865cf4d4bb0431db17e2ebd00f47bf0eb8455a6aecefd34be391ebbabbcb",
    "kc2_runtime/sim/kc2rt_laws.gd": "c234376e9cbadc2d6f69549966112ec4fc1da7df46069831c7f1b80e3f581a9c",
    "kc2_runtime/tools/kc2rt_g3_loop_trace.gd": "50908a225430b3e9ed67dff098d8a730f50c40f25cc91f436ff88ec353e40443",
    "kc2_runtime/tools/kc2rt_g3_oracle_trace.py": "90a036201acab154eed70c43bacbd83f729c6435568d20757fee3016564e5179",
    "kc2_runtime/tests/kc2rt_booking_census.gd": "ecdea42edc35b1e04ac725907ba6fc6a877cada3bfe129a1aff3d81bacde7a54",
}
EXPECT_TREE = "fda00e2876405cec4ff73d8ab836679539ca96b1e77b22a47750cbd598c09a86"


def git_bytes(rev: str, path: str) -> bytes:
    return subprocess.run(["git", "-C", GODOT, "show", f"{rev}:{path}"], check=True,
                          capture_output=True).stdout


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def gamma(k: int) -> Fr:
    k = max(k, 0)
    assert k * U < 1, "n*u >= 1: gamma undefined"
    return k * U / (1 - k * U)


def g2(n: int) -> Fr:
    """gamma^2_{n-1}; an accumulator with <= 1 term has no addition, so 0."""
    return gamma(n - 1) ** 2 if n >= 2 else Fr(0)


def exact(s: str) -> Fr:
    return Fr(float(s))   # exact value of the binary64 the string denotes


# ---------------------------------------------------------------------------------------------- pins
def pins() -> dict:
    out = {"files": {}, "ok": True}
    for p, want in EXPECT.items():
        a, b = sha(git_bytes(REV_RT, p)), sha(git_bytes(REV_ST, p))
        ok = a == want == b
        out["files"][p] = {"sha256_at_" + REV_RT: a, "sha256_at_" + REV_ST: b, "reported": want, "match": ok}
        out["ok"] &= ok
    man = json.loads(git_bytes(REV_RT, "kc2_runtime/MANIFEST.json"))
    lines, bad = [], []
    for m in man["members"]:
        got = sha(git_bytes(REV_RT, "kc2_runtime/" + m["path"]))
        if got != m["sha256"]:
            bad.append(m["path"])
        lines.append(f"{m['path']}  {got}")
    tree = sha("\n".join(sorted(lines)).encode())
    tracked = subprocess.run(["git", "-C", GODOT, "ls-tree", "-r", "--name-only", REV_RT, "kc2_runtime/"],
                             check=True, capture_output=True, text=True).stdout.split()
    tracked = sorted(t[len("kc2_runtime/"):] for t in tracked)
    members = sorted(m["path"] for m in man["members"])
    out["tree"] = {"law": man["tree_digest_law"], "n_members": len(members), "recomputed": tree,
                   "manifest_says": man["tree_digest"], "reported": EXPECT_TREE,
                   "member_digest_failures": bad,
                   "tracked_not_member": [t for t in tracked if t not in members],
                   "member_not_tracked": [m for m in members if m not in tracked]}
    out["tree"]["match"] = (tree == man["tree_digest"] == EXPECT_TREE) and not bad
    out["ok"] &= out["tree"]["match"]
    for p in ["sim/kc2rt_fight.gd", "sim/kc2rt_laws.gd", "tools/kc2rt_g3_loop_trace.gd",
              "tools/kc2rt_g3_oracle_trace.py", "tests/kc2rt_booking_census.gd"]:
        assert p in members, p
    # the tree is unchanged by the AGENT_STATE commit
    out["tree_unchanged_" + REV_ST] = (
        git_bytes(REV_RT, "kc2_runtime/MANIFEST.json") == git_bytes(REV_ST, "kc2_runtime/MANIFEST.json"))
    return out


# ---------------------------------------------------------------------------------------------- census
def census() -> dict:
    src = git_bytes(REV_RT, "kc2_runtime/sim/kc2rt_fight.gd").decode()
    cen = git_bytes(REV_RT, "kc2_runtime/tests/kc2rt_booking_census.gd").decode()
    body = cen[cen.index("const SITES := ["):cen.index("## The chains")]
    rows = []
    for m in re.finditer(r'^\t\[(\d+), "((?:[^"\\]|\\.)*)", "(\w+)", "((?:[^"\\]|\\.)*)", "([TSF])", "([^"]*)"',
                         body, re.M):
        code = m.group(4).encode().decode("unicode_escape")
        rows.append({"line": int(m.group(1)), "caller": m.group(2), "acc": m.group(3), "code": code,
                     "cls": m.group(5), "f": m.group(6)})
    lines = src.split("\n")
    grep = [i + 1 for i, l in enumerate(lines) if re.match(r'^\s*(_cons_add\("|_offer\()', l)]
    # the literal git grep the census names, run against the git object (read-only)
    gg = subprocess.run(["git", "-C", GODOT, "grep", "-n", "-E", r'^[[:space:]]*(_cons_add\("|_offer\()',
                         REV_RT, "--", "kc2_runtime/sim/kc2rt_fight.gd"],
                        check=True, capture_output=True, text=True).stdout.split("\n")
    gg = sorted(int(l.split(":")[2]) for l in gg if l)
    problems = []
    for r in rows:
        code = lines[r["line"] - 1].strip()
        if code != r["code"]:
            problems.append(f"line {r['line']}: source `{code}` != census `{r['code']}`")
        flagged = code.endswith(", true)") or " > 0, " in code
        if r["cls"] == "S" and not code.endswith(", true)"):
            problems.append(f"line {r['line']}: S without split flag")
        if r["cls"] == "F" and not flagged:
            problems.append(f"line {r['line']}: F without flag")
        # T with an UNCONDITIONAL flag is a contradiction; a CONDITIONAL flag (`carried > 0, carried`) on a
        # caller whose carried count is 0 (the PLAY-path `_land` rows) books unflagged, so T is consistent.
        if r["cls"] == "T" and code.endswith(", true)"):
            problems.append(f"line {r['line']}: T but unconditionally flagged")
    sites = sorted({r["line"] for r in rows})
    if sites != grep:
        problems.append(f"site set != grep: missing {sorted(set(grep) - set(sites))}, extra {sorted(set(sites) - set(grep))}")
    if gg != grep:
        problems.append("python grep != git grep")
    cls = {c: sum(1 for r in rows if r["cls"] == c) for c in "TSF"}
    # which accumulators receive an S/F row (jack-ryan's Path-B indicator check, read off the census)
    nonT = sorted({r["acc"] for r in rows if r["cls"] != "T"})
    return {"rows": len(rows), "sites": len(sites), "git_grep_sites": len(gg), "classes": cls,
            "F_rows": [(r["line"], r["caller"], r["acc"], r["f"]) for r in rows if r["cls"] == "F"],
            "accumulators_with_S_or_F_rows": nonT, "problems": problems, "green": not problems,
            "f_max_rule": "f_max = max(R + 4, 2N, 2K + 3); phi = gamma_{2 f_max}"}


# ---------------------------------------------------------------------------------------------- (L2)
def operands() -> list[dict]:
    st = git_bytes(REV_ST, "AGENT_STATE.md").decode()
    sec = st[st.index("### The emitted (L2) operands"):]
    sec = sec[:sec.index("\n---")]
    return [json.loads(l) for l in sec.split("\n") if l.startswith('{"cell"')]


def lossless(s: str) -> bool:
    return isinstance(s, str) and repr(float(s)) == s and math.isfinite(float(s))


def evaluate(c: dict) -> dict:
    n, q = c["n"], c["q"]
    ah = {k: exact(c["A_hat"][k]) for k in K7}
    ahi = {I: exact(c["A_hat_inner"][I]) for I in ("stream", "pcl")}
    NI = c["N_inner"]
    tot = c["inner_totals"]
    O = exact(c["offered"])
    # antecedent 1: every operand present and lossless
    strs = [c["A_hat"][k] for k in K7] + [c["A_hat_inner"][I] for I in ("stream", "pcl")] + [c["offered"]]
    ints = [n[k] for k in K7] + [q[k] for k in K7] + [NI["stream"], NI["pcl"], c["final_sum_n_terms"],
                                                       c["sink_terms_present"]]
    a1 = (all(lossless(s) for s in strs) and all(isinstance(i, int) and not isinstance(i, bool) for i in ints)
          and set(c["A_hat"]) == set(K7) == set(n) == set(q)
          and c["final_sum_n_terms"] == 6 and c["sink_terms_present"] == 6)
    # antecedent 3: n*u < 1 for every count (incl. the abs-sums' own counts)
    counts = [n[k] for k in K7] + [NI["stream"], NI["pcl"], tot["stream_terms"], tot["pcl_terms"], 6]
    a3 = all(x * U < 1 for x in counts)
    # A+ = A_hat / (1 - u - gamma^2_{n-1}); for the inner abs-sums n = total inner terms (run-level sum)
    ap = {k: ah[k] / (1 - U - g2(n[k])) for k in K7}
    api = {I: ahi[I] / (1 - U - g2(tot[I + "_terms"])) for I in ("stream", "pcl")}
    cc = c["census_counters"]
    R, N, K = cc["pkt_rows_max"], cc["dot_buckets_max"], cc["burn_n_due_max"]
    fmax = max(R + 4, 2 * N, 2 * K + 3)
    phi = gamma(2 * fmax)
    t_acc = sum((U + g2(n[k])) * ap[k] for k in K7)
    t_fin = (U + gamma(5) ** 2) * sum((1 + U + g2(n[j])) * ap[j] for j in SINKS)
    t_inn = sum((U + g2(NI[I])) * api[I] for I in ("stream", "pcl"))
    t_phi = phi * sum(ap[k] for k in K7 if q[k] > 0)
    B = t_acc + t_fin + t_inn + t_phi
    den = max(Fr(1), abs(O))
    beta = (1 + U) ** 2 * B / den
    # first-order Lambda and margin (printed, never graded; § F.2k.5), on A_hat
    pt = phi / U
    lam = (ah["offered"] + sum((2 + (pt if q[j] > 0 else 0)) * ah[j] for j in SINKS) + ahi["stream"] + ahi["pcl"]) / den
    M_first = (TOL / U) / lam
    # SENSITIVITY (not the law; printed only): phi charged at 2*phi on ALL seven accumulators.
    # Covers (i) packet-chain roundings carried into `counterplay_absorbed` (q = 0) when a packet is
    # absorbed in whole or in part; (ii) the DOT_INC row's error scaling with mit_total rather than |x|.
    B_s = t_acc + t_fin + t_inn + 2 * phi * sum(ap[k] for k in K7)
    beta_s = (1 + U) ** 2 * B_s / den
    return {"cell": c["cell"], "a1_lossless": a1, "a3_nu_lt_1": a3, "R": R, "N": N, "K": K, "f_max": fmax,
            "phi": phi, "B": B, "beta": beta, "holds_beta": beta <= TOL, "margin_exact": TOL / beta,
            "Lambda": lam, "M_first_order": M_first, "beta_stress": beta_s, "holds_stress": beta_s <= TOL,
            "n": n, "q": q, "N_inner": NI, "O": c["offered"], "rho_hat": c["residual_relative"],
            "unbound_pcl": cc["n_unbound_pcl_rows"],
            "share": {"acc": float(t_acc / B), "final6": float(t_fin / B), "inner": float(t_inn / B),
                      "phi": float(t_phi / B)}}


# drax's AGENT_STATE table, for the comparison (beta to 5 s.f., Lambda, M as printed)
DRAX = {
    "M0|0": (3.5825e-14, 322.69, 27.91), "M0|1": (2.2425e-14, 201.98, 44.59), "M0|2": (2.2507e-14, 202.72, 44.43),
    "M0|3": (2.2443e-14, 202.15, 44.56), "M0|4": (2.2444e-14, 202.15, 44.56),
    "M-POL-2|0": (2.2405e-14, 201.81, 44.63), "M-POL-2|1": (2.2488e-14, 202.55, 44.47),
    "M-POL-2|2": (2.2504e-14, 202.70, 44.44), "M-POL-2|3": (2.2443e-14, 202.15, 44.56),
    "M-POL-2|4": (2.6853e-14, 241.87, 37.24),
    "M-POL-2-NULL|0": (3.5825e-14, 322.69, 27.91), "M-POL-2-NULL|1": (2.2425e-14, 201.98, 44.59),
    "M-POL-2-NULL|2": (2.2507e-14, 202.72, 44.43), "M-POL-2-NULL|3": (2.2443e-14, 202.15, 44.56),
    "M-POL-2-NULL|4": (2.2444e-14, 202.15, 44.56),
    "W1|0": (2.2405e-14, 201.81, 44.63), "W1|1": (3.5780e-14, 322.27, 27.95), "W1|2": (2.2504e-14, 202.70, 44.44),
    "W1|3": (2.2444e-14, 202.16, 44.55), "W1|4": (2.2438e-14, 202.11, 44.57),
    "W1-NULL|0": (2.2405e-14, 201.81, 44.63), "W1-NULL|1": (2.2488e-14, 202.55, 44.47),
    "W1-NULL|2": (2.2504e-14, 202.70, 44.44), "W1-NULL|3": (2.2443e-14, 202.15, 44.56),
    "W1-NULL|4": (2.6853e-14, 241.87, 37.24),
}


def neumaier_probe() -> dict:
    """The Python half of H-6 (d): rebuild the probe vector (kc2rt_v3p7p1_probes.gd:585-640) and
    check the reference bits the port is asserted against."""
    s, out = 20261001, []
    for i in range(1000):
        s = (s * 1103515245 + 12345) & 0x7fffffff
        k = (s % 2001) - 1000
        e = ((s >> 11) % 141) - 70
        x = float(k) * (2.0 ** e)
        if i % 97 == 0:
            x = 2.0 ** 60 if ((s >> 5) & 1) == 1 else -(2.0 ** 60)
        out.append(x)
    out += [-out[i] for i in range(0, 1000, 97)]

    def neu(xs):
        sm = c = 0.0
        for x in xs:
            t = sm + x
            c += ((sm - t) + x) if abs(sm) >= abs(x) else ((x - t) + sm)
            sm = t
        return sm + c

    def bits(x):
        return struct.pack(">d", x).hex()
    naive = 0.0
    for x in out:
        naive += x
    r = {"n": len(out), "neumaier": bits(neu(out)), "fsum": bits(math.fsum(out)), "naive": bits(naive),
         "neumaier_abs": bits(neu([abs(x) for x in out]))}
    r["match_refs"] = (r["n"] == 1011 and r["neumaier"] == "c4e02c678b219c80" == r["fsum"]
                       and r["naive"] == "c4e02c678b219c7e" and r["neumaier_abs"] == "4517dfbddad11c7f")
    return r


def main() -> int:
    P = pins()
    C = census()
    probe = neumaier_probe()
    cells = [evaluate(c) for c in operands()]
    assert len(cells) == 25 and len({c["cell"] for c in cells}) == 25
    print("== PINS ==")
    for p, v in P["files"].items():
        print(f"  {p}: {v['sha256_at_' + REV_RT]}  match={v['match']}")
    print(f"  tree: {P['tree']['recomputed']}  members={P['tree']['n_members']}  match={P['tree']['match']}"
          f"  member failures={P['tree']['member_digest_failures']}  tracked-not-member={P['tree']['tracked_not_member']}"
          f"  member-not-tracked={P['tree']['member_not_tracked']}  unchanged@{REV_ST}={P['tree_unchanged_' + REV_ST]}")
    print("== CENSUS ==")
    print(f"  rows={C['rows']} sites={C['sites']} git-grep sites={C['git_grep_sites']} classes={C['classes']}"
          f" green={C['green']} problems={C['problems']}")
    print(f"  accumulators with S/F rows: {C['accumulators_with_S_or_F_rows']}")
    print(f"== NEUMAIER PROBE (python half) == {probe}")
    print("== (L2) ==")
    hdr = "cell | f_max | beta (exact, 6 s.f.) | margin 1e-12/beta | Lambda | M | drax beta/Lambda/M | agree | beta_stress | rho_hat"
    print(hdr)
    rows_out, allhold, agree_all = [], True, True
    for c in cells:
        d = DRAX[c["cell"]]
        agree = (f"{float(c['beta']):.4e}" == f"{d[0]:.4e}" and f"{float(c['Lambda']):.2f}" == f"{d[1]:.2f}"
                 and f"{float(c['M_first_order']):.2f}" == f"{d[2]:.2f}")
        agree_all &= agree
        ok = c["a1_lossless"] and c["a3_nu_lt_1"] and C["green"] and c["holds_beta"] and c["unbound_pcl"] == 0
        allhold &= ok
        print(f"{c['cell']} | {c['f_max']} | {float(c['beta']):.6e} | x{float(c['margin_exact']):.2f} | "
              f"{float(c['Lambda']):.2f} | {float(c['M_first_order']):.2f} | {d} | {agree} | "
              f"{float(c['beta_stress']):.4e} | {c['rho_hat']}")
        rows_out.append({k: (str(v) if isinstance(v, Fr) else v) for k, v in c.items()} |
                        {"beta_float": float(c["beta"]), "margin_float": float(c["margin_exact"]),
                         "Lambda_float": float(c["Lambda"]), "M_float": float(c["M_first_order"]),
                         "beta_stress_float": float(c["beta_stress"]), "holds": ok, "agrees_with_drax": agree})
    worst = max(cells, key=lambda c: c["beta"])
    worst_s = max(cells, key=lambda c: c["beta_stress"])
    print(f"worst beta: {worst['cell']} = {float(worst['beta']):.6e} (exact {worst['beta'].numerator.bit_length()}-bit "
          f"numerator), margin x{float(worst['margin_exact']):.3f}; M(first order) = {float(worst['M_first_order']):.3f}")
    print(f"worst beta_stress: {worst_s['cell']} = {float(worst_s['beta_stress']):.6e}; all stress hold = "
          f"{all(c['holds_stress'] for c in cells)}")
    print(f"ALL 25 (L2) HOLD: {allhold}; all agree with drax's printed figures: {agree_all}; pins ok: {P['ok']};"
          f" probe ok: {probe['match_refs']}")
    res = {"pins": P, "census": C, "probe": probe, "cells": rows_out, "all_hold": allhold,
           "agree_with_drax": agree_all,
           "worst": {"cell": worst["cell"], "beta": str(worst["beta"]), "beta_float": float(worst["beta"]),
                     "margin": float(worst["margin_exact"]), "M_first_order": float(worst["M_first_order"])}}
    (HERE / "results.json").write_text(json.dumps(res, indent=1, default=str) + "\n")
    return 0 if (allhold and P["ok"] and C["green"] and probe["match_refs"]) else 1


if __name__ == "__main__":
    sys.exit(main())
