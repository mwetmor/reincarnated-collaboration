#!/usr/bin/env python3
"""KC2-PM4 Lap O emission -- Part A (trash-board terms) + Part B (OA/DA both sides).

Writes into `agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-o-trash-board/`:
  pm4o_trash_terms.csv   one row per ROSTER ACTOR (344) -- attribute terms + own TDM passives
  pm4o_oa_da.csv         one row per (body, wave) on waves 151-160 + one PLAYER row
  pm4o_digests.json      FULL 64-hex sha256 + row counts (GL-6: never truncated)
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from pm4o_lib_2026_08_14 import (
    META, I14, PLAYER_SHEET, ULT_SOLO, halt_list, roster_actors,
    attr_terms, own_tdm_terms, ability, pth_prediction, thresholds,
    combatformulas, pth, dump_csv, sha256,
)
from pm4i_lib_2026_08_13 import (E3, survival_arrays, difficulty_pak, surv_at, BATON_20W,
                                 pool_population, level_sets)

OUT = (META / "agentic_orchestration" / "legolas" / "notes"
       / "2026-08-14-kc2-pm4-lap-o-trash-board")
OUT.mkdir(parents=True, exist_ok=True)

BAND_FIRST, BAND_LAST = 151, 160
NAMED_B = (
    "records/creatures/enemies/nemesis/nemesis_kymon_01.dbr",
    "records/creatures/enemies/nemesis/nemesis_wendigo_01.dbr",
    "records/creatures/enemies/nemesis/nemesis_aetherialvanguard_01.dbr",
    "records/creatures/enemies/boss&quest/statue_korvaaktombguardian.dbr",
)

surv = survival_arrays()
pak, pak_scalars, pak_arc = difficulty_pak()
H = halt_list()
actors = roster_actors()

own_halted = set(H["own_halted"])
attr_measured = H["attr_measured"]
all_records = sorted({a["record_path"].lower() for a in actors})
attr_halted = set(all_records) - attr_measured

print(f"roster: {len(actors)} actors / {len(all_records)} records")
print(f"halt list: attr-halted {len(attr_halted)} records ({H['⚑ n_attr_halted_actors'] if '⚑ n_attr_halted_actors' in H else H['n_attr_halted_actors']} actors) · "
      f"own-halted {len(own_halted)} records ({H['n_own_halted_actors']} actors)")

# ⚑ THE LEVEL BASIS, AND ITS ONE DIVERGENCE.  Primary basis = the frozen roster's own per-actor
#   `level` (a spawn property of the roll, the same class of field as `record_path`/`wave`; Lap M
#   confirmed 109 for the wave-160 nemesis against the referent's own on-screen monster banner).
#   Lap D's INDEX-PAIRED pool-proxy law is carried BESIDE it as a sensitivity band, because the
#   two disagree for 175 of 344 actors -- every disagreement being a roster level of exactly 109
#   where the proxy law would place the body lower.  Neither is discarded; both are emitted.
_rp, _rw, _rs, _rk, _pools = pool_population(151, 170)
PROXY_LV, _prox, _lvt = level_sets(_pools, _rp)

# ══════════════════════════════════════════════════════════════════════════════════════════════
# PART A
# ══════════════════════════════════════════════════════════════════════════════════════════════
cache_attr, cache_own, cache_rec = {}, {}, {}


def _terms(rec, L):
    key = (rec, float(L))
    if key not in cache_attr:
        cache_attr[key] = attr_terms(rec, float(L))
        cache_own[key] = own_tdm_terms(rec, float(L))
    return cache_attr[key], cache_own[key]


rowsA = []
for a in actors:
    rec = a["record_path"].lower()
    L = float(a["level"])
    if rec not in cache_rec:
        r, arc = E3.winner(rec)
        cache_rec[rec] = (r or {}, arc)
    cr, arc = cache_rec[rec]
    at, ot = _terms(rec, L)
    halt = ("both" if rec in attr_halted and rec in own_halted else
            "attr_only" if rec in attr_halted else
            "own_only" if rec in own_halted else "none")

    proxy = PROXY_LV.get(rec, [])
    sens = {}
    if proxy:
        lo, hi = float(min(proxy)), float(max(proxy))
        at_lo, ot_lo = _terms(rec, lo)
        at_hi, ot_hi = _terms(rec, hi)
        sens = dict(
            pool_proxy_levels="|".join(str(x) for x in proxy),
            level_basis=("AGREE" if int(L) in proxy else "DIVERGENT"),
            dex_total_at_proxy_lo=at_lo["dex_total"], dex_total_at_proxy_hi=at_hi["dex_total"],
            int_total_at_proxy_lo=at_lo["int_total"], int_total_at_proxy_hi=at_hi["int_total"],
            own_tdm_at_proxy_lo=ot_lo["own_total_damage_modifier_pct"],
            own_tdm_at_proxy_hi=ot_hi["own_total_damage_modifier_pct"],
        )
    else:
        sens = dict(pool_proxy_levels="", level_basis="NO-PROXY",
                    dex_total_at_proxy_lo="", dex_total_at_proxy_hi="",
                    int_total_at_proxy_lo="", int_total_at_proxy_hi="",
                    own_tdm_at_proxy_lo="", own_tdm_at_proxy_hi="")

    rowsA.append(dict(
        actor_id=a["actor_id"], record_path=rec, record_archive=arc,
        display_name=a.get("display_name", ""), wave=a["wave"], spawn_level=a["level"],
        threat_tier=a.get("threat_tier", ""), is_champion=a.get("is_champion", ""),
        monster_classification=str(cr.get("monsterClassification") or "ABSENT"),
        charlevel_equation=str(cr.get("charLevel") or "ABSENT"),
        halt_class=halt,
        halt_attr=(rec in attr_halted), halt_own=(rec in own_halted),
        # the two numbers a damage consumer actually multiplies by (combatformulas.dbr):
        #   physical / pierce   x (1 + dexterity/245)
        #   every magical family x (1 + intelligence/215)
        attr_mult_physical_pierce=round(1 + at["dex_total"] / 245.0, 6),
        attr_mult_magical=round(1 + at["int_total"] / 215.0, 6),
        **at, **ot, **sens,
    ))

COLS_A = [
    "actor_id", "record_path", "record_archive", "display_name", "wave", "spawn_level",
    "threat_tier", "is_champion", "monster_classification", "charlevel_equation",
    "halt_class", "halt_attr", "halt_own",
    "attr_mult_physical_pierce", "attr_mult_magical",
    "bio_record", "bio_archive",
    "dex_equation", "dex_bio_value", "dex_skill_add", "dex_total", "dex_source",
    "dex_skill_sources",
    "int_equation", "int_bio_value", "int_skill_add", "int_total", "int_source",
    "int_skill_sources",
    "str_equation", "str_bio_value", "str_skill_add", "str_total", "str_source",
    "oa_equation", "oa_bio_value", "oa_skill_add", "oa_total", "oa_source",
    "da_equation", "da_bio_value", "da_skill_add", "da_total", "da_source",
    "own_total_damage_modifier_pct", "own_tdm_state", "own_tdm_lapI_crosscheck",
    "own_tdm_n_sources", "own_tdm_sources", "own_tdm_slots_checked",
    "pool_proxy_levels", "level_basis",
    "dex_total_at_proxy_lo", "dex_total_at_proxy_hi",
    "int_total_at_proxy_lo", "int_total_at_proxy_hi",
    "own_tdm_at_proxy_lo", "own_tdm_at_proxy_hi",
]
pA = OUT / "pm4o_trash_terms.csv"
shaA = dump_csv(pA, rowsA, COLS_A)
print(f"PART A -> {pA.name}  rows={len(rowsA)}  sha256={shaA}")

# ══════════════════════════════════════════════════════════════════════════════════════════════
# PART B
# ══════════════════════════════════════════════════════════════════════════════════════════════
band = collections.defaultdict(list)
for a in actors:
    if BAND_FIRST <= int(a["wave"]) <= BAND_LAST:
        band[(a["record_path"].lower(), int(a["wave"]), float(a["level"]))].append(a)

# every named Part-B body is present at its own wave; assert it rather than assume it
present = {k[0] for k in band}
for n in NAMED_B:
    if n not in present:
        print(f"  ⚑ NAMED BODY NOT ON THE 151-160 FROZEN ROSTER: {n}")

PLAYER_OA, PLAYER_DA = PLAYER_SHEET["OA"], PLAYER_SHEET["DA"]

rowsB = []
for (rec, wave, L), group in sorted(band.items()):
    cr, arc = cache_rec.get(rec, (None, ""))
    if cr is None:
        r, arc = E3.winner(rec)
        cr = r or {}
    oa = ability(rec, L, wave, surv, pak, "oa")
    da = ability(rec, L, wave, surv, pak, "da")
    m2p = pth_prediction(oa["OA"], PLAYER_DA)          # monster attacks player
    p2m = pth_prediction(PLAYER_OA, da["DA"])          # player attacks monster

    proxy = PROXY_LV.get(rec, [])
    if proxy:
        lo, hi = float(min(proxy)), float(max(proxy))
        oa_lo = ability(rec, lo, wave, surv, pak, "oa")["OA"]
        oa_hi = ability(rec, hi, wave, surv, pak, "oa")["OA"]
        da_lo = ability(rec, lo, wave, surv, pak, "da")["DA"]
        da_hi = ability(rec, hi, wave, surv, pak, "da")["DA"]
        sensB = dict(
            pool_proxy_levels="|".join(str(x) for x in proxy),
            level_basis=("AGREE" if int(L) in proxy else "DIVERGENT"),
            OA_at_proxy_lo=oa_lo, OA_at_proxy_hi=oa_hi,
            DA_at_proxy_lo=da_lo, DA_at_proxy_hi=da_hi,
            m2p_pth_at_proxy_lo=pth_prediction(oa_lo, PLAYER_DA)["pth_effective"],
            m2p_pth_at_proxy_hi=pth_prediction(oa_hi, PLAYER_DA)["pth_effective"],
            p2m_pth_at_proxy_lo=pth_prediction(PLAYER_OA, da_lo)["pth_effective"],
            p2m_pth_at_proxy_hi=pth_prediction(PLAYER_OA, da_hi)["pth_effective"],
        )
    else:
        sensB = dict(pool_proxy_levels="", level_basis="NO-PROXY",
                     OA_at_proxy_lo="", OA_at_proxy_hi="",
                     DA_at_proxy_lo="", DA_at_proxy_hi="",
                     m2p_pth_at_proxy_lo="", m2p_pth_at_proxy_hi="",
                     p2m_pth_at_proxy_lo="", p2m_pth_at_proxy_hi="")

    row = dict(
        row_kind="monster", record_path=rec, record_archive=arc,
        display_name=group[0].get("display_name", ""), wave=wave, spawn_level=L,
        n_actors_this_wave=len(group),
        threat_tier=group[0].get("threat_tier", ""),
        monster_classification=str(cr.get("monsterClassification") or "ABSENT"),
        halt_attr=(rec in attr_halted), halt_own=(rec in own_halted),
        named_in_commission=(rec in NAMED_B),
        bio_record=cache_attr.get((rec, L), attr_terms(rec, L))["bio_record"],
        wave_crit_damage_modifier_pct=surv_at(surv["offensiveCritDamageModifier"], wave)
        if "offensiveCritDamageModifier" in surv else "ABSENT",
        **oa, **da, **sensB,
    )
    for k, v in m2p.items():
        row["m2p_" + k] = v
    for k, v in p2m.items():
        row["p2m_" + k] = v
    row["m2p_defender_DA"] = PLAYER_DA
    row["p2m_attacker_OA"] = PLAYER_OA
    rowsB.append(row)

# the PLAYER row -- sheet totals, and the equation decomposed as a residual check
cf = combatformulas()
lvl = float(PLAYER_SHEET["level"])
oa_struct = lvl * 12 + PLAYER_SHEET["cunning"] * 0.5 + 53
da_struct = lvl * 12 + PLAYER_SHEET["physique"] * 0.5 + 53
prow = dict(
    row_kind="player", record_path="gdc/_EoRWarlGuts/player.gdc",
    record_archive="save", display_name="EoRWarlGuts", wave="", spawn_level=lvl,
    n_actors_this_wave=1, threat_tier="player", monster_classification="Player",
    halt_attr=False, halt_own=False, named_in_commission=True,
    bio_record="Lap A measured-player-sheet.csv (screenshots 495/508) + Lap G gdc parse",
    oa_attr_characterDexterity=PLAYER_SHEET["cunning"],
    oa_level_term=lvl * 12, oa_attr_term=PLAYER_SHEET["cunning"] * 0.5,
    OA=PLAYER_OA,
    da_attr_characterStrength=PLAYER_SHEET["physique"],
    da_level_term=lvl * 12, da_attr_term=PLAYER_SHEET["physique"] * 0.5,
    DA=PLAYER_DA,
    oa_flat_bio=round(PLAYER_OA - oa_struct, 4),        # gear+skill flat/% residual
    da_flat_bio=round(PLAYER_DA - da_struct, 4),
    oa_mod_pct_total="UNDECOMPOSED (flat vs %% not separable from the sheet total)",
    da_mod_pct_total="UNDECOMPOSED (flat vs %% not separable from the sheet total)",
    wave_crit_damage_modifier_pct=PLAYER_SHEET["crit_damage_pct"],
    pool_proxy_levels="", level_basis="MEASURED-FROM-SHEET",
)
rowsB.append(prow)

COLS_B = ["row_kind", "record_path", "record_archive", "display_name", "wave", "spawn_level",
          "n_actors_this_wave", "threat_tier", "monster_classification",
          "halt_attr", "halt_own", "named_in_commission", "bio_record",
          "wave_crit_damage_modifier_pct"]
for k in rowsB[0]:
    if k not in COLS_B:
        COLS_B.append(k)
for r in rowsB:
    for k in r:
        if k not in COLS_B:
            COLS_B.append(k)

pB = OUT / "pm4o_oa_da.csv"
shaB = dump_csv(pB, rowsB, COLS_B)
print(f"PART B -> {pB.name}  rows={len(rowsB)}  sha256={shaB}")

# ══════════════════════════════════════════════════════════════════════════════════════════════
# Coverage + headline
# ══════════════════════════════════════════════════════════════════════════════════════════════
attr_closed = sum(1 for r in rowsA
                  if r["halt_attr"] and r["dex_equation"] != "ABSENT"
                  and r["int_equation"] != "ABSENT")
attr_absent = sorted({r["record_path"] for r in rowsA
                      if r["halt_attr"] and (r["dex_equation"] == "ABSENT"
                                             or r["int_equation"] == "ABSENT")})
own_measured = sorted({r["record_path"] for r in rowsA
                       if r["halt_own"] and r["own_tdm_state"] == "MEASURED"})
own_absent = sorted({r["record_path"] for r in rowsA
                     if r["halt_own"] and r["own_tdm_state"] != "MEASURED"})
own_absent_actors = sum(1 for r in rowsA
                        if r["halt_own"] and r["own_tdm_state"] != "MEASURED")

mrows = [r for r in rowsB if r["row_kind"] == "monster"]
named_rows = [r for r in mrows if r["named_in_commission"]]

summary = dict(
    lap="KC2-PM4 Lap O -- trash-board decode + OA/DA both sides",
    firewall="ONLY ⚑ data_gate keys read from the i14 findings JSON",
    halt_list_source=str(I14),
    halt_list_i14=dict(
        n_actors=H["n_actors"], n_records=H["n_records"],
        n_attr_halted_records=H["n_attr_halted_records"],
        n_attr_halted_actors=H["n_attr_halted_actors"],
        n_own_halted_records=H["n_own_halted_records"],
        n_own_halted_actors=H["n_own_halted_actors"],
    ),
    partA=dict(
        rows=len(rowsA),
        attr_halted_records=len(attr_halted),
        attr_halted_actors_closed=attr_closed,
        attr_records_ABSENT=attr_absent,
        own_halted_records=len(own_halted),
        own_halted_records_MEASURED_nonzero=len(own_measured),
        own_halted_records_ABSENT_measured_zero=len(own_absent),
        own_halted_actors_ABSENT=own_absent_actors,
        own_tdm_pct_on_halted_actors=dict(
            n=len([r for r in rowsA if r["halt_own"]]),
            min=min(r["own_total_damage_modifier_pct"] for r in rowsA if r["halt_own"]),
            median=__import__("statistics").median(
                [r["own_total_damage_modifier_pct"] for r in rowsA if r["halt_own"]]),
            mean=round(__import__("statistics").mean(
                [r["own_total_damage_modifier_pct"] for r in rowsA if r["halt_own"]]), 4),
            max=max(r["own_total_damage_modifier_pct"] for r in rowsA if r["halt_own"]),
        ),
        attr_mult_on_halted_actors=dict(
            physical_pierce_median=__import__("statistics").median(
                [r["attr_mult_physical_pierce"] for r in rowsA if r["halt_attr"]]),
            physical_pierce_min=min(r["attr_mult_physical_pierce"] for r in rowsA if r["halt_attr"]),
            physical_pierce_max=max(r["attr_mult_physical_pierce"] for r in rowsA if r["halt_attr"]),
            magical_median=__import__("statistics").median(
                [r["attr_mult_magical"] for r in rowsA if r["halt_attr"]]),
            magical_min=min(r["attr_mult_magical"] for r in rowsA if r["halt_attr"]),
            magical_max=max(r["attr_mult_magical"] for r in rowsA if r["halt_attr"]),
        ),
        level_basis=dict(
            AGREE=sum(1 for r in rowsA if r["level_basis"] == "AGREE"),
            DIVERGENT=sum(1 for r in rowsA if r["level_basis"] == "DIVERGENT"),
            NO_PROXY=sum(1 for r in rowsA if r["level_basis"] == "NO-PROXY"),
        ),
    ),
    partB=dict(
        rows=len(rowsB), monster_rows=len(mrows),
        band=f"{BAND_FIRST}-{BAND_LAST}",
        player_OA=PLAYER_OA, player_DA=PLAYER_DA,
        named=[dict(record=r["record_path"], wave=r["wave"], level=r["spawn_level"],
                    OA=r["OA"], DA=r["DA"],
                    m2p_pth=r["m2p_pth_effective"], m2p_hit_pct=r["m2p_p_hit_pct"],
                    m2p_crit_pct=r["m2p_p_crit_any_pct"],
                    m2p_E_mult=r["m2p_expected_mult_per_swing"],
                    p2m_pth=r["p2m_pth_effective"], p2m_hit_pct=r["p2m_p_hit_pct"],
                    p2m_crit_pct=r["p2m_p_crit_any_pct"],
                    p2m_E_mult=r["p2m_expected_mult_per_swing"])
               for r in named_rows],
        m2p_pth_min=min(r["m2p_pth_effective"] for r in mrows),
        m2p_pth_max=max(r["m2p_pth_effective"] for r in mrows),
        p2m_pth_min=min(r["p2m_pth_effective"] for r in mrows),
        p2m_pth_max=max(r["p2m_pth_effective"] for r in mrows),
        n_m2p_floored_at_55=sum(1 for r in mrows if r["m2p_pth_floored_at_55"]),
        n_p2m_floored_at_55=sum(1 for r in mrows if r["p2m_pth_floored_at_55"]),
        n_p2m_cannot_miss=sum(1 for r in mrows if r["p2m_p_hit_pct"] >= 100.0),
        n_m2p_cannot_miss=sum(1 for r in mrows if r["m2p_p_hit_pct"] >= 100.0),
    ),
    combatformulas=dict(
        archive=E3.winner("records/game/combatformulas.dbr")[1],
        probabilityToHitEquation=cf["probabilityToHitEquation"],
        offensiveAbilityEquation=cf["offensiveAbilityEquation"],
        defensiveAbilityEquation=cf["defensiveAbilityEquation"],
        normalPTHEquation=cf["normalPTHEquation"],
        pthMinimum=cf["pthMinimum"],
        thresholds={f"pthThreshold{i}": t for i, t, _m in thresholds()},
        multipliers={f"pthDamageModifier{i}": m for i, _t, m in thresholds()},
    ),
)

digests = dict(
    lap="KC2-PM4 Lap O",
    generated_utc=__import__("datetime").datetime.utcnow().isoformat() + "Z",
    artifacts={
        "pm4o_trash_terms.csv": dict(sha256=shaA, rows=len(rowsA), cols=len(COLS_A)),
        "pm4o_oa_da.csv": dict(sha256=shaB, rows=len(rowsB), cols=len(COLS_B)),
    },
    instruments={
        str(p): sha256(p) for p in sorted(
            pathlib.Path(__file__).resolve().parent.glob("pm4o_*_2026_08_14.py"))
    },
    inputs={
        str(I14): dict(sha256=sha256(I14), keys_read=["⚑ data_gate"]),
        str(BATON_20W): dict(sha256=sha256(BATON_20W),
                             keys_read=["actors[].record_path", "actors[].wave",
                                        "actors[].level", "actors[].actor_id",
                                        "actors[].display_name", "actors[].threat_tier",
                                        "actors[].is_champion"]),
    },
    summary=summary,
)
pD = OUT / "pm4o_digests.json"
pD.write_text(json.dumps(digests, indent=2, ensure_ascii=False))
digests_sha = sha256(pD)
print(json.dumps(summary, indent=2, ensure_ascii=False))
print(f"\npm4o_digests.json sha256={digests_sha}")
