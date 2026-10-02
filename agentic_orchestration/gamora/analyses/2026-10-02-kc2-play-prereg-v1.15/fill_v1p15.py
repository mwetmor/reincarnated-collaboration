#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.15 · FILL (gamora, 2026-10-02). Writes the prereg from v1.15.template.md + results_v1p15.json +
v1.14's committed derive_v1p14.json; every digest and number computed here. Refuses on a STOP, a failing restated row
(that would be a HALT, not a fill), or an unfilled placeholder.

Run: python3 fill_v1p15.py -> agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.15.md
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLLAB = HERE.parents[3]
NOTES = COLLAB / "agentic_orchestration/gandalf/notes"
OUTP = NOTES / "2026-09-20-kc2-play-ta-prereg-v1.15.md"
fsha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
R = json.loads((HERE / "results_v1p15.json").read_text())
D14 = json.loads((HERE.parent / "2026-10-02-kc2-play-prereg-v1.14/derive_v1p14.json").read_text())
if R["STOP"] or not (R["TA-X-30(a')"]["holds"] and R["TA-X-30(b)"]["holds"] and R["TA-X-29(b')"]["holds"]):
    print("HALT: a restated row fails on the oracle, or a STOP; not filling")
    sys.exit(2)
F = {"V114": fsha(NOTES / "2026-09-20-kc2-play-ta-prereg-v1.14.md")}
assert F["V114"] == "5bbe7ae5f0c3f73c77ee7cc3e21870ed8523b6d19fa1eae977dff451ef6b2d92"
F["F_LO"] = repr(R["constants"]["F_LO (min measured)"])
F["MOTION_LINE"] = str(R["constants"]["pet_motion_write_line(run.py)"])
w = D14["TA-X-29e"]
assert (round(w["w159"], 6), round(w["w160"], 6)) == (3.197066, 4.935649)
et = []
for wv in ("159", "160"):
    x = w["walk"][wv]
    et.append(f"| w{wv} (`M_inst` {x['M_inst']}) | ratio | on | off |\n|---|---:|---:|---:|")
    for rec, v in sorted(x["records"].items(), key=lambda kv: kv[0].rsplit('/', 1)[-1]):
        et.append(f"| `{rec.rsplit('/', 1)[-1].replace('.dbr', '')}` | {v['ratio']} | {v['sum_fold_on']} | {v['sum_fold_off']} |")
    et.append(f"| *unpriced (no profile): {len(x['unpriced_no_profile'])}* | | | |")
    et.append(f"| **w{wv} supply-weighted** | **{x['ratio']:.6f}** | | |\n")
F["E_TABLES"] = "\n".join(et)
kt = ["| cell | complete | terminal | (a′) roster steps / law-exact unclipped / held | (a′) pet steps / moved exact / no travel | (a′) fails | (b′) beyond | armed wall | (b′) vacuous | (b′) | (b′) composed rows / fails | TA-X-29 (b′) |",
      "|---|---|---|---|---|---|---:|---|---|---|---|---|"]
for k, c in R["cells"].items():
    a, b, z = c["TA-X-30(a')"], c["TA-X-30(b) R-G4-V311"], c["TA-X-29(b')"]
    nrows = sum(v for kk, v in z["families"].items())
    kt.append(f"| {k.replace('|', '_s')} | {'✓' if c['complete'] else '⛔'} | {'clear' if c['terminal'] == 'cleared_w160' else 'w' + str(c['terminal'])} | "
              f"{a['steps_checked']:,} / {a['unclipped']:,} / {a['held']:,} | {a['pet_steps']:,} / {a['pet_moved_exact']:,} / "
              f"{a['pet_no_travel_by_law']:,} | {sum(a['fails'].values())} | {b['n_bodies_halted_beyond_d_engage']} | "
              f"{'yes' if b['arena_armed_waves'] else 'no'} | {'**vacuous**' if b['vacuous'] else 'tested'} | "
              f"**{'PASS' if (a['holds'] and b['holds']) else 'FAIL'}** | {nrows:,} / {sum(z['fails'].values())} | "
              f"**{'PASS' if z['holds'] else 'FAIL'}** |")
F["K_TABLE"] = "\n".join(kt)
A, B, Z = R["TA-X-30(a')"], R["TA-X-30(b)"], R["TA-X-29(b')"]
F["T30A"] = f"PASS {A['n_pass']}/25"
F["T30B"] = f"PASS {B['n_pass']}/25"
F["T29B"] = f"PASS {Z['n_pass']}/25"
F.update({"R_STEPS": f"{A['steps_checked']:,}", "R_UNCLIP": f"{A['unclipped']:,}", "R_CLIP": f"{A['clipped']:,}",
          "R_HELD": f"{A['held']:,}", "R_WP": f"{A['waypoint']:,}", "P_STEPS": f"{A['pet_steps']:,}",
          "P_EXACT": f"{A['pet_moved_exact']:,}", "P_CLIP": f"{A['pet_moved_clipped_shorter']:,}",
          "P_NONE": f"{A['pet_no_travel_by_law']:,}", "P_UNOBS": f"{A['pet_moved_unobserved']:,}",
          "N_VAC": str(len(B["vacuous_cells"])),
          "W1_CLAMPS": f"{sum(R['cells'][f'W1|{s}']['TA-X-30(b) R-G4-V311']['arena_clamp_calls'] for s in range(5)):,}",
          "OPCLASSES": "; ".join(f"`{k}` {v:,}" for k, v in sorted(A["op_classes"].items())),
          "FAMILIES": "; ".join(f"`{k}` {v:,}" for k, v in sorted(Z["families"].items())),
          "INSTANCES": "; ".join(f"`{k}` {v:,}" for k, v in sorted(Z["instances"].items())),
          "Z5DIFF": f"{Z['rows_where_the_Z5_form_differs']:,}"})
ft = ["| file | sha256 |", "|---|---|"]
for n in ["audit_v1p15.py", "check_v1p15.py", "results_v1p15.json", "fill_v1p15.py", "v1.15.template.md"]:
    ft.append(f"| `{n}` | `{fsha(HERE / n)}` |")
for p in sorted((HERE / "audit_out").glob("*.gz")):
    ft.append(f"| `{p.relative_to(HERE)}` | `{fsha(p)}` |")
ft.append(f"| v1.14 `derive_v1p14.json` (read for (e)) | `{fsha(HERE.parent / '2026-10-02-kc2-play-prereg-v1.14/derive_v1p14.json')}` |")
F["FILES_TABLE"] = "\n".join(ft)
T = (HERE / "v1.15.template.md").read_text()
for k, v in F.items():
    T = T.replace("{{" + k + "}}", v)
left = re.findall(r"\{\{[A-Z0-9_]+\}\}", T)
if left:
    print("UNFILLED", sorted(set(left)))
    sys.exit(2)
OUTP.write_text(T)
print("wrote", OUTP, fsha(OUTP))
