#!/usr/bin/env python3
"""KC2-PLAY · v1.15 NOTES companion · FILL (gamora). Writes the companion from notes.template.md + results_v1p15n.json and
digests computed here. Refuses on a STOP, a non-zero in-scope TA-X-13 count, a non-int(round( live in-scope site, or an
unfilled placeholder (each would be a HALT, not a note).

Run: python3 fill_v1p15n.py <instrument commit> -> agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.15-notes.md
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLLAB = HERE.parents[3]
NOTES = COLLAB / "agentic_orchestration/gandalf/notes"
OUTP = NOTES / "2026-09-20-kc2-play-ta-prereg-v1.15-notes.md"
ENGINE = Path("/Users/admin/Games/reincarnated-engine")
fsha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
R = json.loads((HERE / "results_v1p15n.json").read_text())
if R["STOP"] or R["TA-X-13"]["player_rows_crit (in scope)"] != 0 or not R["TA-X-21"]["every_live_in_scope_is_int_round"]:
    print("HALT: not filing")
    sys.exit(2)
F = {"V114": fsha(NOTES / "2026-09-20-kc2-play-ta-prereg-v1.14.md"), "V115": fsha(NOTES / "2026-09-20-kc2-play-ta-prereg-v1.15.md"),
     "H6": fsha(COLLAB / "agentic_orchestration/qa/findings/2026-10-02-kc2-ta-prereg-v1.15-h6-preread.md"),
     "INSTR_COMMIT": sys.argv[1]}
assert F["V114"].startswith("5bbe7ae5") and F["V115"].startswith("d1c4a75a")
chk = (HERE.parent / "2026-10-02-kc2-play-prereg-v1.14/check_v1p14.py").read_text().splitlines()
F["CHK_LINE"] = str(next(i + 1 for i, l in enumerate(chk) if '"out_of_scope_player_summon_printed"' in l) - 1)
t = R["TA-X-13"]
F.update({"C_PLAYER": str(t["player_rows_crit (in scope)"]), "C_PS": f"{t['player_summon_ps_ (out of scope)']:,}",
          "C_PS_RANGE": "{}–{}".format(*t["ps_ per cell range"]), "C_MON": f"{t['monster (roster + pet)']:,}",
          "C_OTHER": str(t["other"])})
F["C_AGREE"] = (f"jack-ryan's independent probe (H-6 § 7 WARN-2) read 0 player · 4,281 `ps_` · 132 monster; this census "
                f"reads {t['player_rows_crit (in scope)']} · {t['player_summon_ps_ (out of scope)']:,} · "
                f"{t['monster (roster + pet)']:,}: **{'equal' if (t['player_rows_crit (in scope)'], t['player_summon_ps_ (out of scope)'], t['monster (roster + pet)']) == (0, 4281, 132) else 'DIFFERENT (printed, see results_v1p15n.json)'}**.")
F["INERT"] = R["inert_vs_v1.14_bare (capture rows)"]
s21 = R["TA-X-21"]
rows = ["| site | scope | live hits (25 cells) | `int(round(` | cited in v1.14 | line |", "|---|---|---:|---|---|---|"]
for x in s21["sites"]:
    rows.append(f"| `{x['site']}` | {x['scope']} | {x['hits_25_cells']:,} | {'yes' if x['int_round'] else '**no**'} | "
                f"{'yes' if x['cited_in_v1.14'] else ''} | `{x['text'][:90].replace('|', '¦')}` |")
F["SITE_TABLE"] = "\n".join(rows)
fmt = lambda L: ", ".join(f"`{s}`" for s in L) or "none"
F.update({"N_LIVE": str(len(s21["live_in_scope"])), "LIVE_LIST": fmt(s21["live_in_scope"]),
          "ALL_INT": str(s21["every_live_in_scope_is_int_round"]).lower(), "DEAD_LIST": fmt(s21["dead_in_scope"]),
          "DEAD_CITED": fmt(s21["dead_v1.14_cited"]), "GD_LIST": fmt(s21["live_gd"]) + f" ({len(s21['live_gd'])})",
          "OUT_LIST": fmt(s21["live_outside_scope"]), "FILES_EQ": str(s21["files_equal_across_arms"]).lower()})
F["FILES_TABLE_SITES"] = "| module | FILE sha256 |\n|---|---|\n" + "\n".join(f"| `{k}` | `{v}` |" for k, v in sorted(s21["files_sha256"].items()))
tr = R["trajectories"]
F.update({"N_TRAJ": str(tr["distinct"]), "N_CLEAR": str(tr["clearing"]), "N_DIE": str(tr["dying"]),
          "W1_CALLS": f"{R['TA-X-30_face']['clamp_calls_W1']:,}",
          "PURSUE_STEPS": str(R["TA-X-30_face"]["non_waypoint_pursue_steps"]),
          "CLIP_STEPS": str(R["TA-X-30_face"]["clipped_steps"])})
d = R["divisor"]
F.update({"N_ROSTER": str(d["n_roster_profiles"]), "N_PET": str(d["n_pet_profiles"]),
          "DIV_PER_ARM": ", ".join(f"{a} {n}" for a, n in d["SlowChaos_SlowAether_rows_per_arm"].items()),
          "DIV_PACK": ", ".join(f"`{k}` {v}" for k, v in d["pack_offense_text_hits"].items()),
          "DOT_TYPES": ", ".join(f"`{x}`" for x in d["dot_types_present"])})
a8 = json.loads((ENGINE / "src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143/model/"
                 "input_closure_v3p11.json").read_text())["⚑ v3p11_rows"]["a8_composition_calls_v3p11"]
tru, fal = [], []
for r in a8:
    if r["value"]["callee"].endswith("gd_composition.CompositionFold.__init__"):
        v = r["value"]["args"]["chaos_aether_dot_divisor"]
        (tru if (v["value"] is True and v["explicit"]) else fal).append(f"`{r['id']}` ({r['value']['job']})")
F["A8_TRUE"], F["A8_FALSE"] = ", ".join(tru), ", ".join(fal)
gcl = (ENGINE / "src/reincarnated/simulation/kc2/gd_composition.py").read_text().splitlines()
F["FALLBACK_LINE"] = str(next(i + 1 for i, l in enumerate(gcl) if "d = 1.0 if v_int is None else float(v_int) / 200.0 + 1.0" in l))
F["GUARD"] = R["guard_module_sha256"][0]
assert len(R["guard_module_sha256"]) == 1 and F["GUARD"].startswith("5f3f4f1e")
g0 = R["guard"]["M0"]
F.update({"CAP_T": str(g0["max_ticks (G2 cap)"]), "CAP_S": str(g0["tick_cap_s"]),
          "GUARD_N": str(sum(1 for v in R["guard"].values() if v["complete"])),
          "LONGEST": str(R["longest_wave_ticks_25_cells (v1.14 traces)"])})
ft = ["| file | sha256 |", "|---|---|"]
for n in ["census_v1p15n.py", "check_v1p15n.py", "results_v1p15n.json", "fill_v1p15n.py", "notes.template.md"]:
    ft.append(f"| `{n}` | `{fsha(HERE / n)}` |")
for p in sorted((HERE / "census").glob("*.gz")):
    ft.append(f"| `{p.relative_to(HERE)}` | `{fsha(p)}` |")
for n in ("check_v1p14.py", "oracle_trace_v3p11.py"):
    ft.append(f"| v1.14 folder `{n}` (fixed, KP-248) | `{fsha(HERE.parent / '2026-10-02-kc2-play-prereg-v1.14' / n)}` |")
F["FILES_TABLE"] = "\n".join(ft)
T = (HERE / "notes.template.md").read_text()
for k, v in F.items():
    T = T.replace("{{" + k + "}}", v)
left = re.findall(r"\{\{[A-Z0-9_]+\}\}", T)
if left:
    print("UNFILLED", sorted(set(left)))
    sys.exit(2)
OUTP.write_text(T)
print("wrote", OUTP, fsha(OUTP))
