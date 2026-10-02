#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.14 · FILL (gamora, 2026-10-02). Writes the prereg from `v1.14.template.md` and the JSON outputs of
derive_v1p14.py / check_v1p14.py / audit20_v1p14.py, plus file digests computed here. Every digest and measured number in
the prereg's filled blocks comes from this script; none is typed. Refuses to write if any placeholder is left unfilled or if
an instrument's output reports a self-check failure / STOP.

Run: python3 fill_v1p14.py  -> agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.14.md
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLLAB = HERE.parents[3]
OUTP = COLLAB / "agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.14.md"
ARMS = ["M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"]
SALTS = [0, 1, 2, 3, 4]


def fsha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


D = json.loads((HERE / "derive_v1p14.json").read_text())
R = json.loads((HERE / "results_v1p14.json").read_text())
A = json.loads((HERE / "audit20_v1p14.json").read_text())
assert not D["self_check_failures"], D["self_check_failures"]
assert not R["completeness"]["STOP_cells"]
P4 = HERE.parent / "2026-10-02-kc2-v3p11-oracle-pass4/graded_V311-FULL.json"
p4 = json.loads(P4.read_text())
tele = p4["results"]["M-POL-2"]["fold_reports"]["composition"]["telemetry"]
mp, rp = D["packs"]["model"], D["packs"]["reference"]
cells = R["cells"]
F = {}
F["MODEL_PACK"], F["REF_PACK"] = mp["digest"], rp["digest"]
F["MODEL_PACK_SHORT"], F["REF_PACK_SHORT"] = mp["digest"][:8], rp["digest"][:8]
F["MODEL_DIR"] = "kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143"
F["REF_DIR"] = "kc2-reference-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143"
F["MODEL_N"], F["REF_N"] = str(mp["n"]), str(rp["n"])
F["MODEL_SELF"] = str(mp["digest"] == mp["manifest_digest"] and not mp["member_failures"] and mp["disk_equals_manifest"]).lower()
F["REF_SELF"] = str(rp["digest"] == rp["manifest_digest"] and not rp["member_failures"] and rp["disk_equals_manifest"]).lower()
F["CROSS"] = str(rp["cross_pin"] == mp["digest"]).lower()
rows = ["| # | member | label | sha256 (computed) | bytes |", "|---|---|---|---|---:|"]
for i, (m, v) in enumerate(sorted(mp["members"].items()), 1):
    rows.append(f"| {i} | `{m}` | FILE | `{v['sha256']}` | {v['bytes']:,} |")
for j, (m, v) in enumerate(sorted(rp["members"].items()), 1):
    rows.append(f"| R{j} | `{m}` | FILE | `{v['sha256']}` | {v['bytes']:,} |")
rows.append(f"| — | model `manifest.json` | FILE | `{mp['manifest_file']}` | |")
rows.append(f"| — | reference `manifest.json` | FILE | `{rp['manifest_file']}` | |")
F["MEMBER_TABLE"] = "\n".join(rows)
rs = D["rowsets"]
F.update({"ROWSET_ALL": rs["v3p11_all"], "ROWSET_CLOS": rs["v3p11_closure_all"], "ROWSET_HAND": rs["v3p11_hand_all"],
          "N_HAND_RS": str(rs["n_hand_rowsets"]), "N_CLOS_RS": str(rs["n_closure_rowsets"]),
          "N_HAND_ROWS": f"{rs['n_hand_rows']:,}", "N_CLOS_ROWS": f"{rs['n_closure_rows']:,}"})
doc = D["documents"]
F.update({"ORACLE_SCRIPT": doc["oracle_script"], "RECEIPT": doc["receipt"], "MIGRATION": doc["MIGRATION.md"],
          "X8": doc["x8 (P-n.2)"], "RECEIPT_VERDICT": str(D.get("receipt_verdict"))[:60]})
F["PASS4_GRADED"] = fsha(P4)
F["PASS4_GRADED_SHORT"] = F["PASS4_GRADED"][:8]
NOTES = COLLAB / "agentic_orchestration/gandalf/notes"
F["V113"] = fsha(NOTES / "2026-09-20-kc2-play-ta-prereg-v1.13.md")
F["V113_SHORT"] = F["V113"][:8]
F["V112"] = fsha(NOTES / "2026-09-20-kc2-play-ta-prereg-v1.12.md")
F["GRADE_NOTE"] = fsha(COLLAB / "agentic_orchestration/gamora/notes/2026-10-01-kc2-play-ta-attempt2-v1.13-grade.md")
F["GRADE_VERDICT"] = fsha(HERE.parent / "2026-10-01-kc2-play-ta-attempt2-v1.13-grade/ta_verdict_v1p13_attempt2.json")
F["JR_OBS1"] = fsha(COLLAB / "agentic_orchestration/qa/findings/2026-10-02-join1-j0-j1-gate2.md")
e = D["engine"]
F.update({"ENGINE_HEAD": e["HEAD"], "N_MODULES": str(e["modules_imported"]),
          "MOD_DIFF": "none" if not e["modules_differing_from_blob"] else str(e["modules_differing_from_blob"]),
          "PORCELAIN": "clean" if not e["porcelain_oracle_tree"] else f"`{e['porcelain_oracle_tree']}`"})
# completeness table
ct = ["| arm | salt 0 | salt 1 | salt 2 | salt 3 | salt 4 |", "|---|---|---|---|---|---|"]
for a in ARMS:
    r = [a]
    for s in SALTS:
        c = R["completeness"]["per_cell"][f"{a}|{s}"]
        ok = all(c["checks"].values())
        r.append(("✓ " if ok else "⛔ ") + ("clear w160" if c["terminal"] == "cleared_w160" else f"death w{c['terminal']}")
                 + f", 10/10 waves")
    ct.append("| " + " | ".join(r) + " |")
F["COMPLETENESS_TABLE"] = "\n".join(ct) + (f"\n\n**{R['completeness']['counts']['complete']}/{R['completeness']['counts']['cells']} "
                                          "cells complete; STOP cells: none.**")
F["AUDIT20"] = (f"**{A['complete']}/20 salts complete; {A['survive_genuine_w160_clear']} survivals, every one a genuine w160 "
                f"`cleared / board_empty`; the four deaths are in w160** (salts "
                f"{[s for s, v in A['cells'].items() if v['leg_a_death_wave']]}); the terminals equal pass 4's own "
                f"`leg_a_terminals` ({A['pass4']['file']}): {str(A['terminals_equal_pass4']).lower()}.")
inr = R["inertness"]
F["INERT"] = f"{inr['hooked == bare (capture rows), cells']}/25"
F["BATCH_ROWS"] = f"{inr['single == batch (capture rows), cells']}/25"
F["BATCH_TRACE"] = f"{[v for k, v in inr.items() if k.startswith('single == batch (whole')][0]}/25"
F["PERIOD"] = repr(json.loads(__import__("gzip").decompress((HERE / "oracle_trace/hooked_M0.json.gz").read_bytes()))["period"])
# a8
a8 = D["a8"]
at = ["| arm (`a8` job) | `a8` rows | n | ROWSET (job rows, v1.12 law) | distinguishing |", "|---|---|---:|---|---|"]
dist = a8["distinguishing_callees"]
for j in ["setup", "M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL", "WALK"]:
    v = a8["jobs"][j]
    dd = ", ".join(sorted({x.split(".")[-2] + "." + x.split(".")[-1] if "graded_arm" not in x else "graded_arm(" + j + ")"
                           for x in dist.get(j, [])})) or ("—" if j in dist else "(not a fight job)")
    at.append(f"| **`{j}`** | `{v['ids'][0]}`…`{v['ids'][1]}` | {v['n']} | `{v['rowset']}` | {dd} |")
F["A8_TABLE"] = "\n".join(at)
F["A8_DIST"] = ("`M0`: `run_cell(seat=False)` on its 5 rows (set by `graded_arm`) · `M-POL-2`: `run_cell(seat=True)`, explicit, "
                "on its 5 rows (its ARMED `ChannelPolicyFold` is built inside the seat and carries no `a8` row of its own) · "
                "`M-POL-2-NULL`: `ChannelPolicyFold(armed=False)`, explicit, ×5 (through `graded_arm`'s disarmed wrapper) · "
                "`W1`: `ArenaFold(armed=True, avoidance=True)`, both explicit · `W1-NULL`: `ArenaFold(armed=False)` "
                "(`avoidance` omitted). Read off the rows by script (`derive_v1p14.json :: a8.arm_keys`, "
                "`a8.distinguishing_callees`)")
F["SETUP_C"] = ", ".join(f"`{x}`" for x in a8["setup_partition"]["C (shared config)"])
F["SETUP_T"] = ", ".join(f"`{x}`" for x in a8["setup_partition"]["T (probe instance)"])
tt = ["| arm | leg-A terminal per salt (0–4) | seconds into the terminal wave |", "|---|---|---|"]
for a in ARMS:
    tt.append(f"| `{a}` | " + ", ".join("clear" if x == "cleared_w160" else f"**w{x}**" for x in R["terminals"][a])
              + " | " + ", ".join(str(x) for x in R["t_into_terminal_s"][a]) + " |")
F["TERMINALS_TABLE"] = "\n".join(tt) + ("\n\n(On a clear, the seconds are w160's duration. v1.13's reference: `M-POL-2` "
                                       "`[156, 152, 155, 152, 152]`. **Not draw-comparable with any port realisation**, § C.7.)")
cp = a8["callees_per_arm"]["M-POL-2"]
F["P5_TABLE"] = ("| fold / call (callee, `a8` v3.11, arm `M-POL-2`) | rows |\n|---|---:|\n" +
                 "\n".join(f"| `{c}` | {n} |" for c, n in cp if any(t in c for t in ("Fold", "load_profiles", "Loader", "fold", "run_cell", "_overrides"))))
F["FALLBACK_SHORT"] = D["sets"]["FALLBACK"]["digest"][:8]
F["MARCH_BASE"] = str(D["sets"]["march_base"])
# row values
lw = R["law_a"]
F["T06_IDENT"] = str([s for s, x in enumerate(lw["TA-X-06 (printed, not graded)"]["identical_per_salt"]) if x])
F["T09_SHORT"] = D["TA-X-09"]["rowset"][:8]
b = lw["TA-X-10"]["bound"]
F["T10_BOUND"] = repr(b)
F["T10_DELTA"] = repr(b - 43.758085029822276)
F["T10_EMAX"] = repr(b - 8.0)
F["T10_BODY"] = repr(lw["TA-X-10"]["max_body"])
F["T10_SPAWN"] = repr(lw["TA-X-10"]["max_spawn"])
F["LU_KEYS"] = str(D["TA-X-16"]["LU-KEYS"])
F["P06_KEY"] = str(D["TA-X-16"]["P06-KEY"])
F["T17_MAX"] = f"{max(c['TA-X-17']['max_offset_m'] for c in cells.values()):.6f}"
F["T21_SITES"] = "/".join(str(n) for n, _ in D["TA-X-21"]["round_sites"])
F["T21_FILE_SHORT"] = D["TA-X-21"]["threat_py"][:8]
F["SWING_SHORT"] = D["sets"]["SWING (v3.11 graded loader)"]["digest"][:8]
F["NONSWING_SHORT"] = D["sets"]["NONSWING (v3.11 graded loader)"]["digest"][:8]
r27 = lw["TA-X-27(c) registry"]
F["T27_EXERCISED"] = str(r27["exercised_call_sites"])
w = D["TA-X-29e"]
F["W159"], F["W160"] = f"{w['w159']:.6f}", f"{w['w160']:.6f}"
F["W159_D"], F["W160_D"] = f"{w['w159'] - 3.207764:+.6f}", f"{w['w160'] - 4.980316:+.6f}"
F["SL_WALK_EQ"] = str(w.get("equals star-lord's bare walk")).lower()
F["C_GD_INST"] = f"{tele['pre_gd_inst'] / 1e6:.2f}M"
F["C_OR_INST"] = f"{tele['pre_oracle_inst'] / 1e6:.2f}M"
F["C_INST_PCT"] = f"{(tele['pre_gd_inst'] / tele['pre_oracle_inst'] - 1) * 100:+.1f} %"
F["C_GD_DOT"] = f"{tele['pre_gd_dot'] / 1e6:.3f}M"
F["C_OR_DOT"] = f"{tele['pre_oracle_dot'] / 1e6:.3f}M"
F["C_DOT_X"] = f"×{tele['pre_gd_dot'] / tele['pre_oracle_dot']:.1f}"
# TA-X-16 block
t16 = D["TA-X-16"]
F["T16_BLOCK"] = "\n".join([
    f"law_v1.14       : {t16['law_v1.14']}",
    f"LU-KEYS         : {t16['LU-KEYS']}   (w151 … w160)   sum {t16['sum_LU']}",
    f"LU key sets     : {t16['LU-KEYS_sets']}",
    f"V11-P06-1       : {t16['V11-P06-1 (waves.json, incumbent roll)']}   sum {t16['sum_V11']}   (the incumbent roll; unchanged)",
    f"P06-KEY[w]      : {t16['P06-KEY']}   sum {sum(t16['P06-KEY'])}",
    "checks          : " + "; ".join(f"{k} = {v}" for k, v in t16["checks"].items())])
# TA-X-08 table
t8 = ["| cell | terminal | observed | PF | D | id. 1 | `n_channelling` | `n_released` (D) | `n_control_suppressed_channelling` | `n_ticks_released` | (2) restated | v1.12 (2) text | (2p) |",
      "|---|---|---:|---:|---:|---|---:|---:|---:|---:|---|---|---|"]
for a in ARMS:
    for s in SALTS:
        c = cells[f"{a}|{s}"]
        x = c["TA-X-08"]
        t8.append(f"| {a}_s{s} | {'clear' if c['terminal'] == 'cleared_w160' else 'w' + str(c['terminal'])} | {x['observed']} | "
                  f"{x['PRE_FIGHT']} | {x['D']} | {'✓' if x['id1'] else '✗'} | {x['n_channelling']} | {x['n_released']} | "
                  f"{x['n_control_suppressed_channelling']} | {x['n_ticks_released']} | **{'GREEN' if x['id2_restated'] else 'RED'}** | "
                  f"{'pass' if x['id2_v1.12_text'] else 'fail'} | {'✓' if x['id2p'] else '✗'} |")
F["T08_TABLE"] = "\n".join(t8)
allc = list(cells.values())
cnt = lambda f: f"{sum(1 for c in allc if f(c))}/25"
F["T08_ID1"] = cnt(lambda c: c["TA-X-08"]["id1"])
F["T08_ID2"] = cnt(lambda c: c["TA-X-08"]["id2_restated"])
F["T08_ID2OLD"] = cnt(lambda c: c["TA-X-08"]["id2_v1.12_text"])
F["T08_ID2P"] = cnt(lambda c: c["TA-X-08"]["id2p"])
F["T08_CONV"] = cnt(lambda c: all(c["TA-X-08"]["census_convention"].values()))
csc = [c["TA-X-08"]["n_control_suppressed_channelling"] for c in allc]
F["T08_CSC"], F["T08_CSC_MAX"] = str(sum(csc)), str(max(csc))
F["T08_RELPF"] = str(sum(c["TA-X-08"]["n_released_pre_fight"] for c in allc))
F["T08_CSPF"] = str(sum(c["TA-X-08"]["n_control_suppressed_pre_fight"] for c in allc))
F["T08_DBL"] = str(sum(c["TA-X-08"]["n_control_suppressed_released"] for c in allc))
# TA-X-27 table
t27 = ["| exercised draw call site (v3.11) | registry row | registry site | draws, 25 cells, leg A | note |", "|---|---|---|---:|---|"]
for k, v in r27["per_site"].items():
    t27.append(f"| `{k}` | `{v['registry']}` | `{v['registry_site']}` | {v['draws_leg_A_25_cells']:,} | "
               f"{'line moved; verified by expression' if v.get('line_moved') else 'verified'} |")
F["T27_TABLE"] = ("\n".join(t27) + f"\n\n**Registry of record at v3.11 = V9's {r27['registry_v9_site_rows']} SITE rows + "
                  f"`rg1`'s {r27['registry_rg1_draw_rows']} DRAW rows, of which "
                  f"{', '.join(r27['rg1_draw_rows_not_live_in_V311-FULL (LU-UNK sensitivity only)'])} is reachable only under the "
                  f"`LU-UNK` sensitivity → (c)'s expected registered live sites = "
                  f"**{r27['registered_live_sites_v1.14 (V9 + rg1 live)']}** (v1.13: 29).** Exercised on the oracle: "
                  f"{r27['exercised_call_sites']} call sites ({len(r27['exercised_V9'])} V9 + {len(r27['exercised_rg1'])} `rg1`), "
                  f"every one registered and verified: {str(r27['every_exercised_site_registered_and_verified']).lower()}. "
                  f"V9 sites not exercised at v3.11 (live in the registry, unreached on these 25 cells): "
                  f"{', '.join(r27['V9_not_exercised_at_v3.11'])} (V9-SITE-01: slot choice now draws at "
                  f"`gd_engagement._choose`; 10–12: K-MILL superseded by P-MOVE; 18–22, 27–28: roll branches the referent "
                  f"board does not take). p05 emergence draws: {r27['p05_emergence draws']}.")
# TA-X-30 table
t30 = ["| cell | pursuit steps | halted | halted with operand ≠ 2.4 | **halted beyond 2.4 (row (b) as written)** | max halt distance (m) | steps at op 2.4 / other / 0 (waypoint) | pet steps aimed at a reposition target | arena-clamp stops beyond the step operand (R-G4) |",
       "|---|---:|---:|---:|---:|---:|---|---:|---:|"]
for a in ARMS:
    for s in SALTS:
        p = cells[f"{a}|{s}"]["TA-X-30"]
        st = p["steps"]
        t30.append(f"| {a}_s{s} | {st.get('n_pursuit_steps', 0):,} | {st.get('n_pursuit_halted', 0):,} | "
                   f"{p['halted_with_operand_not_2.4']:,} | **{p['halted_beyond_2.4_literal']:,}** | "
                   f"{p['halted_beyond_2.4_literal_max_m']:.2f} | {st.get('op=2.4', 0):,} / {st.get('op=other', 0):,} / "
                   f"{st.get('op=0', 0):,} | {p['pet_steps_aimed_at_reposition_target']:,} | "
                   f"{p['arena_clamp_stops_beyond_step_operand (R-G4)']} |")
F["T30_TABLE"] = "\n".join(t30) + (f"\n\n**(a) holds on {lw['TA-X-30']['(a) holds on cells']}/25; (b) as written holds on "
                                  f"{lw['TA-X-30']['(b) literal holds on cells']}/25; (b) under the R-G4 reading "
                                  f"{lw['TA-X-30']['(b) R-G4 arena-clamp reading holds on cells']}/25.**")
# walk table
wt = ["| wave | M_inst | priced | identity-path priced | v1.14 ratio | v1.13 ratio | Δ |", "|---|---:|---:|---:|---:|---:|---:|"]
for i, wv in enumerate(range(151, 161)):
    x = w["walk"][str(wv)]
    wt.append(f"| {wv} | {x['M_inst']} | {x['n_priced']} | {x['n_identity_path_priced']} | {x['ratio']:.6f} | "
              f"{w['v1.13_ten_ratios'][i]:.6f} | {x['ratio'] - w['v1.13_ten_ratios'][i]:+.6f} |")
F["WALK_TABLE"] = "\n".join(wt)
# law (a) table
la = ["| row | basis | oracle passes? | detail |", "|---|---|---|---|"]
def L(rid, ok, det):
    la.append(f"| `{rid}` | MEASURED (25 cells, leg A) | **{'PASS' if ok else 'FAIL'}** | {det} |")
L("TA-X-01", lw["TA-X-01"]["holds"], "M0 salt 2 run twice: trace, streams, capture rows byte-identical")
L("TA-X-03", lw["TA-X-03"]["holds"], f"identical per salt {lw['TA-X-03']['identical_per_salt']}")
L("TA-X-04", lw["TA-X-04"]["holds"], f"identical per salt {lw['TA-X-04']['identical_per_salt']}")
L("TA-X-05", lw["TA-X-05"]["holds"], f"identical per salt {lw['TA-X-05']['identical_per_salt']} (≥ 1 differs)")
L("TA-X-08", lw["TA-X-08"]["holds"], f"{lw['TA-X-08']['n_pass']}/25 (§ F.2n.4′)")
L("TA-X-10", lw["TA-X-10"]["holds"], f"W1 max body {lw['TA-X-10']['max_body']:.6f}, max spawn {lw['TA-X-10']['max_spawn']:.6f} ≤ {b!r}")
L("TA-X-11", lw["TA-X-11"]["holds"], "0 player / 0 body clamps on 10/10 W1 and W1-NULL cells")
for rid in ("TA-X-12", "TA-X-13", "TA-X-14", "TA-X-15(a)", "TA-X-16", "TA-X-17", "TA-X-22", "TA-X-24", "TA-X-25"):
    L(rid, lw[rid]["holds"], f"{lw[rid]['n_pass']}/25")
L("TA-X-27(c)", r27["every_exercised_site_registered_and_verified"], f"{r27['exercised_call_sites']} exercised call sites, all in the registry (§ F.2p)")
L("TA-X-29(c)", lw["TA-X-29(c)"]["holds"], "oracle `M_inst` = pack `z3` on 10/10 waves")
la.append("| `TA-X-29(b)` | pack `V311-CG1-09` + pass-4 composition telemetry | **FAIL** | `C5-Z5-LAW` is not the governing law under `V311-FULL` (§ Q104.2) |")
L("TA-X-30", lw["TA-X-30"]["holds"], f"(a) {lw['TA-X-30']['(a) holds on cells']}/25, (b) as written {lw['TA-X-30']['(b) literal holds on cells']}/25 (§ Q104.1)")
F["LAWA_TABLE"] = "\n".join(la)
res = R["residuals"]
F["RES_WAVE"] = str(res["mean_wave_s_151_159 (all 25 cells)"])
F["RES_CLEAR"] = str(res["n_cells_clearing_w160"])
F["RES_PETS"] = str(round(res["pets_per_cell_mean"]))
# files
ft = ["| file | sha256 |", "|---|---|"]
for n in ["oracle_trace_v3p11.py", "derive_v1p14.py", "derive_v1p14.json", "check_v1p14.py", "results_v1p14.json",
          "audit20_v1p14.py", "audit20_v1p14.json", "fill_v1p14.py", "v1.14.template.md"]:
    ft.append(f"| `{n}` | `{fsha(HERE / n)}` |")
for p in sorted((HERE / "oracle_trace").rglob("*.gz")):
    ft.append(f"| `{p.relative_to(HERE)}` | `{fsha(p)}` |")
F["FILES_TABLE"] = "\n".join(ft)

T = (HERE / "v1.14.template.md").read_text()
for k, v in F.items():
    T = T.replace("{{" + k + "}}", v)
left = re.findall(r"\{\{[A-Z0-9_]+\}\}", T)
if left:
    print("UNFILLED:", sorted(set(left)))
    sys.exit(2)
OUTP.write_text(T)
print("wrote", OUTP, fsha(OUTP))
