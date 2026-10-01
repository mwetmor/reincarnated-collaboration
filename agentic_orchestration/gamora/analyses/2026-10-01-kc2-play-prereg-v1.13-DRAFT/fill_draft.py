#!/usr/bin/env python3
"""Fills the machine-made blocks of v1.13-DRAFT.md from pins_v1p13.json and results.json (gamora, 2026-10-01).

No digest or measured number in the draft is typed: every block between `<!-- FILL:<name> -->` and
`<!-- /FILL:<name> -->` is regenerated from the two JSON files that the two instruments wrote. Re-run after either
instrument re-runs. Idempotent.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRAFT = HERE / "v1.13-DRAFT.md"
P = json.loads((HERE / "pins_v1p13.json").read_text())
R = json.loads((HERE / "results.json").read_text())
CELLS = R["cells"]
ORDER = [f"{a}_s{s}" for a in ["M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"] for s in range(5)]


def fsha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def b_pins() -> str:
    out = ["| pin | label | **sha256 (recomputed by `pins_v1p13.py`)** | v1.12 → v1.13 |", "|---|---|---|---|"]
    for k, v in P["carried"].items():
        out.append(f"| {k} | {v['label']} | `{v['sha256']}` | {'reproduces v1.12' if v['reproduces'] else '⛔ DOES NOT REPRODUCE'} |")
    s = P["summary"]
    out += ["", f"**{s['n_reproduce']} of {s['n_carried']} carried pins reproduce v1.12. Failures: "
                f"{s['failures'] or 'none'}.** Engine HEAD `{P['engine_head']}`; tracked modifications under "
                f"`simulation/kc2`, `export`, `simulation/scripts`: {P['engine_kc2_tracked_mods'] or 'none'}. "
                f"`setup` partition re-derived by rule: C = {P['setup_partition']['n_C']}, T = {P['setup_partition']['n_T']}, "
                f"C equals v1.12's list: {P['setup_partition']['C_by_rule_equals_v1.12_list']}. Set cardinalities "
                f"{P['set_cardinalities']['POOL']} / {P['set_cardinalities']['SWING']} / {P['set_cardinalities']['NONSWING']}, "
                f"partition {P['set_cardinalities']['partition']}, `march_base` {P['set_cardinalities']['march_base']}. "
                f"`TA-X-18` bits {P['TA-X-18']['bits']} (equal to v1.12: {P['TA-X-18']['equals_v1.12']}). "
                f"`TA-X-09`: {P['TA-X-09_n']} vectors.",
            "", "**New documents of record (no v1.12 value exists; computed, not compared):**", "",
            "| document | label | sha256 |", "|---|---|---|"]
    for k, v in P["new"].items():
        out.append(f"| {k} | {v['label']} | `{v['sha256']}` |")
    rt = [v for k, v in P["new"].items() if k.startswith("runtime tree")][0]
    out.append("")
    out.append(f"The runtime-tree row is recomputed from `kc2_runtime/MANIFEST.json` at godot `b4c1ff3` over git blobs "
               f"({rt['n_members']} members, member failures: {rt['member_failures'] or 'none'}; the MANIFEST's own "
               f"`tree_digest` reads `{rt['manifest_says']}`). **It is NOT the attempt-2 runtime**: drax's counters "
               f"(§ H) move the tree, so the graded runtime digest is ⚑ **PENDING**.")
    return "\n".join(out)


def b_vector() -> str:
    v = R["vector"]
    return "\n".join([
        "```",
        f"law            : {v['law']}",
        f"V11-P06-1      : {v['vector_p06_off']}   (w151 … w160)   sum {v['sum_off']}",
        f"p06 ON (info)  : {v['vector_p06_on']}   sum {v['sum_on']}",
        f"P06-KEY[w]     : {v['p06_key_per_wave']}   sum {sum(v['p06_key_per_wave'])}   (key grain: one (w, 6) key, or none)",
        f"P06-ROWS[w]    : {v['p06_rows_per_wave']}   sum {sum(v['p06_rows_per_wave'])}   (row grain: NOT graded; printed so the two grains are never confused)",
        "checks         : " + "; ".join(f"{k} = {ok}" for k, ok in v["checks"].items()),
        "```"])


def b_t16() -> str:
    out = ["| cell | terminal | waves played | picks per wave (= V11-P06-1 prefix?) | `n_pool_picks` / Σ expected | p06 keys rolled | filtered keys per wave (= P06-KEY prefix?) | restated | v1.12 text (`== 47`) |",
           "|---|---|---:|---|---|---:|---|---|---|"]
    for k in ORDER:
        t = CELLS[k]["TA-X-16_restated"]
        pw = t["per_wave"]
        out.append(f"| {k} | w{CELLS[k]['terminal_wave']} | {len(pw)} | {[x['picks'] for x in pw]} "
                   f"({all(x['picks'] == x['expected'] for x in pw)}) | {t['n_pool_picks']} / {t['expected_sum']} | "
                   f"{t['n_spawn_point_6_keys_rolled']} | {[x['filtered_keys'] for x in pw]} "
                   f"({all(x['filtered_keys'] == x['filtered_expected'] for x in pw)}) | "
                   f"**{'GREEN' if t['holds'] else 'RED'}** | {'GREEN' if CELLS[k]['TA-X-16_v1.12_text']['holds'] else 'RED'} |")
    s = R["summary"]
    out += ["", f"**Restated row on the oracle: {s['TA-X-16 restated (oracle passes)']}. v1.12's text on the oracle: "
                f"{s['TA-X-16 v1.12 text (oracle passes)']}.** Every roll passed `bonus_spawns_enabled=False`: "
                f"{all(x['bonus_spawns_enabled_passed'] == [False] for k in ORDER for x in CELLS[k]['TA-X-16_restated']['per_wave'])}. On every "
                f"wave played the actor grain (distinct `spawn_point_id` among spawned roster actors) equals the key "
                f"grain and carries no `p06`: "
                f"{all(x['actor_grain_equals_picks'] for k in ORDER for x in CELLS[k]['TA-X-16_restated']['per_wave'])}."]
    return "\n".join(out)


def b_t08() -> str:
    out = ["| cell | observed | PF | D | id. 1 | `n_channelling` | `n_released` (D) | released PF ticks | `n_control_suppressed_channelling` | trace control `channel` entries | as written: lhs − D (jack-ryan KP-180) | **restated** |",
           "|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---|"]
    for k in ORDER:
        c = CELLS[k]
        i1, i2, r2, f = c["identity_1"], c["identity_2_v1.12"], c["identity_2_restated"], c["fold"]
        out.append(f"| {k} | {i1['observed']} | {i1['PRE_FIGHT']} | {i1['D']} | {'✓' if i1['holds'] else '✗'} | "
                   f"{r2['n_channelling']} | {r2['n_released (D population)']} | {f['n_released_on_PRE_FIGHT']} | "
                   f"{r2['n_control_suppressed_channelling (D population)']} | {f['trace_control_channel_entries_leg_A']} | "
                   f"{i2['lhs_minus_D']:+d} ({i2['jack_ryan_KP180_cross_reference']:+d}) | "
                   f"**{'GREEN' if r2['holds'] else 'RED'}** |")
    s = R["summary"]
    out += ["", "**Summary, measured on the oracle:**", ""]
    for k in ["TA-X-08 identity 1 (oracle passes)", "TA-X-08 identity 2 AS WRITTEN (oracle passes)",
              "TA-X-08 identity 2 RESTATED (oracle passes)", "identity 2 restated, rival population (all observed ticks)",
              "shortfall == jack-ryan KP-180 table", "shortfall == -(control-suppressed channelling)",
              "independent: trace control `channel` entries (leg A) == n_control_suppressed_channelling",
              "fold counter n_ticks_released == released on observed ticks (fold arms)",
              "fold aligned + consistent + no desync", "census chan == trace chan on D",
              "released PRE_FIGHT ticks (all cells)", "control-suppressed PRE_FIGHT ticks (all cells)",
              "control-suppressed RELEASED ticks on D (all cells)"]:
        out.append(f"* {k}: **{s[k]}**")
    return "\n".join(out)


def b_census() -> str:
    out = ["| cell | one PRE_FIGHT per wave played | no DEAD | lethal tick censused alive | D = G3 `D_oracle` | PF = G3 `PRE_FIGHT_oracle` |",
           "|---|---|---|---|---|---|"]
    for k in ORDER:
        cc = CELLS[k]["census_convention"]
        out.append("| " + k + " | " + " | ".join("✓" if v else "✗" for v in cc.values()) + " |")
    out += ["", f"**Census convention on the oracle: {R['summary']['census convention holds']}.**"]
    return "\n".join(out)


def b_lawa() -> str:
    out = ["| row | basis | oracle passes? | detail |", "|---|---|---|---|"]
    for k, v in R["law_a_measured"].items():
        out.append(f"| `{k}` | {v['basis']} (this draft, 25 reference traces) | **{'PASS' if v['passes'] else 'FAIL'}** | {v['detail']} |")
    return "\n".join(out)


def b_files() -> str:
    out = ["| file | sha256 |", "|---|---|"]
    for name in ["pins_v1p13.py", "pins_v1p13.json", "pins_stdout.txt", "oracle_channel_hook.py", "check_v1p13_draft.py",
                 "results.json", "run_stdout.txt", "fill_draft.py", "oracle_hook/rerun_trace_sha256.json"]:
        out.append(f"| `{name}` | `{fsha(HERE / name)}` |")
    n = len(list((HERE / "oracle_hook").glob("*.hook.json.gz")))
    out.append(f"| `oracle_hook/*.hook.json.gz` | {n} files (one per cell; gzip mtime 0) |")
    return "\n".join(out)


BLOCKS = {"pins": b_pins, "vector": b_vector, "t16": b_t16, "t08": b_t08, "census": b_census, "lawa": b_lawa,
          "files": b_files}


def main() -> None:
    text = DRAFT.read_text(encoding="utf-8")
    for name, fn in BLOCKS.items():
        pat = re.compile(rf"(<!-- FILL:{name} -->\n).*?(<!-- /FILL:{name} -->)", re.S)
        assert pat.search(text), name
        text = pat.sub(lambda m: m.group(1) + fn() + "\n" + m.group(2), text)
    DRAFT.write_text(text, encoding="utf-8")
    print("filled", list(BLOCKS))


if __name__ == "__main__":
    main()
