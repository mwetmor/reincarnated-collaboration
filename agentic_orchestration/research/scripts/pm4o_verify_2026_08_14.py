#!/usr/bin/env python3
"""KC2-PM4 Lap O verification -- independent re-derivation of the emitted artifacts.

Six checks, each on a path that does NOT reuse the emitting code path:
  V1  every halt-list record (attr-halted 154, own-halted 104) has >= 1 emitted row
  V2  actor counts per own-halted record reproduce the i14 gate's own counts exactly
  V3  attribute terms re-derived by reading the bio record STRAIGHT out of the archive and
      evaluating its equation string -- compared against the CSV
  V4  PTH re-derived by textually substituting OA/DA into `combatformulas.probabilityToHitEquation`
      and `eval`-ing the RECORD'S OWN STRING -- compared against the CSV
  V5  every tier distribution conserves mass to 1e-6
  V6  OA/DA re-derived by textually substituting into the record's own ability equation strings
"""
from __future__ import annotations

import collections
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from pm4o_lib_2026_08_14 import META, I14, halt_list, roster_actors, combatformulas
from pm4i_lib_2026_08_13 import E3, ev

OUT = (META / "agentic_orchestration" / "legolas" / "notes"
       / "2026-08-14-kc2-pm4-lap-o-trash-board")
A = list(csv.DictReader((OUT / "pm4o_trash_terms.csv").open()))
B = list(csv.DictReader((OUT / "pm4o_oa_da.csv").open()))
H = halt_list()
actors = roster_actors()
all_records = {a["record_path"].lower() for a in actors}
attr_halted = all_records - H["attr_measured"]
own_halted = set(H["own_halted"])

fails = []


def chk(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}  {detail}")
    if not ok:
        fails.append(f"{name}: {detail}")


# ── V1 ────────────────────────────────────────────────────────────────────────────────────────
seen = collections.Counter(r["record_path"] for r in A)
chk("V1a attr-halted records covered",
    all(seen[r] > 0 for r in attr_halted), f"{len(attr_halted)} records")
chk("V1b own-halted records covered",
    all(seen[r] > 0 for r in own_halted), f"{len(own_halted)} records")
chk("V1c row count == roster actor count", len(A) == H["n_actors"],
    f"{len(A)} vs {H['n_actors']}")

# ── V2 ────────────────────────────────────────────────────────────────────────────────────────
bad = [(r, n, seen[r]) for r, n in H["own_halted"].items() if seen[r] != n]
chk("V2 per-record actor counts reproduce the i14 gate", not bad, f"{len(bad)} mismatches")

n_attr_halt_rows = sum(1 for r in A if r["halt_attr"] == "True")
n_own_halt_rows = sum(1 for r in A if r["halt_own"] == "True")
chk("V2b attr-halted actor count", n_attr_halt_rows == H["n_attr_halted_actors"],
    f"{n_attr_halt_rows} vs {H['n_attr_halted_actors']}")
chk("V2c own-halted actor count", n_own_halt_rows == H["n_own_halted_actors"],
    f"{n_own_halt_rows} vs {H['n_own_halted_actors']}")

# ── V3 ────────────────────────────────────────────────────────────────────────────────────────
worst, n3 = 0.0, 0
for r in A:
    bio, _ = E3.winner(r["bio_record"])
    if not bio:
        chk("V3 bio present", False, r["bio_record"])
        break
    L = float(r["spawn_level"])
    for field, col, addcol in (("characterDexterity", "dex_bio_value", "dex_skill_add"),
                               ("characterIntelligence", "int_bio_value", "int_skill_add"),
                               ("characterStrength", "str_bio_value", "str_skill_add")):
        eq = bio.get(field)
        if eq is None:
            continue
        got = float(ev(eq, L))
        worst = max(worst, abs(got - float(r[col])))
        n3 += 1
chk("V3 attribute equations re-evaluated from the archive", worst < 1e-6,
    f"{n3} comparisons, max |delta| = {worst:.3e}")

# ── V4 ────────────────────────────────────────────────────────────────────────────────────────
cf = combatformulas()
EQ = cf["probabilityToHitEquation"]


def pth_from_record_string(oa: float, da: float) -> float:
    expr = (EQ.replace("offensiveAbilityDV", f"({oa!r})")
              .replace("defensiveAbilityDV", f"({da!r})"))
    return float(eval(expr, {"__builtins__": {}}, {}))


worst4, n4 = 0.0, 0
PLAYER_OA, PLAYER_DA = 3259.0, 2591.0
for r in B:
    if r["row_kind"] != "monster":
        continue
    got_m = pth_from_record_string(float(r["OA"]), PLAYER_DA)
    got_p = pth_from_record_string(PLAYER_OA, float(r["DA"]))
    worst4 = max(worst4, abs(got_m - float(r["m2p_pth_raw"])),
                 abs(got_p - float(r["p2m_pth_raw"])))
    n4 += 2
# tolerance = 5.1e-5 = one half-ULP of the CSV's own 4-decimal rounding.  The residual is the
# artifact's storage precision, not a formula disagreement.
chk("V4 PTH re-derived by eval-ing the record's OWN equation string", worst4 < 5.1e-5,
    f"{n4} comparisons, max |delta| = {worst4:.3e} (CSV 4-dp half-ULP = 5.0e-5)")

# ── V5 ────────────────────────────────────────────────────────────────────────────────────────
worst5 = 0.0
for r in B:
    if r["row_kind"] != "monster":
        continue
    for pre in ("m2p_", "p2m_"):
        worst5 = max(worst5, abs(float(r[pre + "tier_mass_sum_check_pct"]) - 100.0))
        parts = (float(r[pre + "p_miss_pct"]) + float(r[pre + "p_normal_x1_0_pct"])
                 + sum(float(r[k]) for k in r if k.startswith(pre + "p_tier")))
        worst5 = max(worst5, abs(parts - 100.0))
chk("V5 tier distributions conserve probability mass", worst5 < 1e-5,
    f"max |delta| = {worst5:.3e} pct-points")

# ── V6 ────────────────────────────────────────────────────────────────────────────────────────
OAE, DAE = cf["offensiveAbilityEquation"], cf["defensiveAbilityEquation"]


def ability_from_record_string(eq, flat, lvl, attr, mod):
    expr = (eq.replace("offensiveAbilityDV", f"({flat!r})")
              .replace("defensiveAbilityDV", f"({flat!r})")
              .replace("characterLevelDV", f"({lvl!r})")
              .replace("dexterityDV", f"({attr!r})")
              .replace("strengthDV", f"({attr!r})")
              .replace("offensiveAbilityModifierDV", f"({mod!r})")
              .replace("defensiveAbilityModifierDV", f"({mod!r})")
              .replace("bonusDV", "(0.0)"))
    return float(eval(expr, {"__builtins__": {}}, {}))


worst6, n6 = 0.0, 0
for r in B:
    if r["row_kind"] != "monster":
        continue
    L = float(r["spawn_level"])
    oflat = sum(float(r[k]) for k in ("oa_flat_bio", "oa_flat_own_skills",
                                      "oa_flat_wave_surv", "oa_flat_ultimate_pak"))
    dflat = sum(float(r[k]) for k in ("da_flat_bio", "da_flat_own_skills",
                                      "da_flat_wave_surv", "da_flat_ultimate_pak"))
    got_oa = ability_from_record_string(OAE, oflat, L,
                                        float(r["oa_attr_characterDexterity"]),
                                        float(r["oa_mod_pct_total"]))
    got_da = ability_from_record_string(DAE, dflat, L,
                                        float(r["da_attr_characterStrength"]),
                                        float(r["da_mod_pct_total"]))
    worst6 = max(worst6, abs(got_oa - float(r["OA"])), abs(got_da - float(r["DA"])))
    n6 += 2
chk("V6 OA/DA re-derived by eval-ing the record's OWN equation strings", worst6 < 5.1e-5,
    f"{n6} comparisons, max |delta| = {worst6:.3e} (CSV 4-dp half-ULP = 5.0e-5)")

print()
print("VERIFY:", "ALL PASS" if not fails else f"{len(fails)} FAILURES")
for f in fails:
    print("  ", f)
sys.exit(1 if fails else 0)
