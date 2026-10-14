#!/usr/bin/env python3
"""C-13 enemy anchor, PART 3: GD wave 151-160 enemy quantities (read-only extractor).

Run:
    PYTHONPATH=/Users/admin/Games/reincarnated-engine/src \
    python3 gd_enemy_quantities.py ../gd_enemy_quantities.json

READ-ONLY. It imports the frozen KC2 oracle (`reincarnated.simulation.kc2`) and calls only its
loaders and pure functions. It reads the digest-pinned CSVs under reincarnated-engine/data/kc2.
It writes exactly one file, the JSON path given on the command line. Nothing under
reincarnated-engine is written.

Two populations, two weightings each (see gd_notes.md):
  REF   the referent line-up's PINNED bodies (referent_lineup.REFERENT_LINEUP). Body weight = pin
        count, split uniformly over a class-only pin's candidates.
  BOARD the measured board (data/kc2/pm4o_oa_da.csv, row_kind == monster: 95 (record, wave) rows,
        91 distinct records). Body weight = n_actors_this_wave.
Each population is summarised twice: equal weight per (record, wave) cell, and body-weighted.
"""
from __future__ import annotations

import csv
import hashlib
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

from reincarnated.simulation.kc2 import (global_magnitude as gm, measured_board as mb,
                                         monster_stats as ms, offense as off, pool_lift as PL,
                                         referent_lineup as rl, threat as th)

ENGINE = Path("/Users/admin/Games/reincarnated-engine")
DATA = ENGINE / "data" / "kc2"
WAVES = range(151, 161)

INPUTS = {
    "pm4o_oa_da.csv": DATA / "pm4o_oa_da.csv",
    "pm4l_mitigation_by_body.csv": DATA / "pm4l_mitigation_by_body.csv",
    "pm4_band_b_ehp_by_wave.csv": DATA / "pm4_band_b_ehp_by_wave.csv",
    "pm4_band_b_wave_life_modifier.csv": DATA / "pm4_band_b_wave_life_modifier.csv",
    "pm4i_wave_damage_modifier.csv": DATA / "pm4i_wave_damage_modifier.csv",
    "pm2_tg2_attack_damage.csv": DATA / "pm2_tg2_attack_damage.csv",
    "pm2_tg2_monster_timing.csv": DATA / "pm2_tg2_monster_timing.csv",
    "pm4i_band_c_roster.csv": DATA / "pm4i_band_c_roster.csv",
    "pm4o_trash_terms.csv": DATA / "pm4o_trash_terms.csv",
    "kc2_referent_lineup_v3p11.csv": DATA / "kc2_referent_lineup_v3p11.csv",
}
RESISTS = ["res_physical", "res_pierce", "res_fire", "res_cold", "res_lightning", "res_poison",
           "res_life", "res_aether", "res_chaos", "res_bleeding"]
# Families the oracle routes OFF the health path, or that are not flat per-hit magnitudes.
NON_FLAT_TYPES = set(th.NON_HEALTH_DAMAGE_TYPES) | set(th.DECODED_NON_HEALTH_TYPES)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def base(rec: str) -> str:
    return rec.rsplit("/", 1)[-1].replace(".dbr", "")


def q(vals, weights=None):
    """median / p25 / p75 / min / max / n; weighted quantiles if weights are given."""
    pairs = [(float(v), float(w if weights else 1.0))
             for v, w in zip(vals, weights or [1.0] * len(vals)) if v is not None]
    if not pairs:
        return {"n": 0}
    pairs.sort()
    tot = sum(w for _, w in pairs)

    def wq(p):
        acc = 0.0
        for v, w in pairs:
            acc += w
            if acc >= p * tot - 1e-12:
                return v
        return pairs[-1][0]

    out = {"n_cells": len(pairs), "weight_total": round(tot, 4), "median": wq(0.5),
           "p25": wq(0.25), "p75": wq(0.75), "min": pairs[0][0], "max": pairs[-1][0]}
    if weights is None:  # unweighted: use the statistics module's median, as a cross-check
        out["median_statistics"] = statistics.median([v for v, _ in pairs])
    return out


def role_of(rec: str, tier: str | None, mclass: str | None) -> tuple[str, str]:
    if tier:
        return {"hero": "champion-hero"}.get(tier, tier), "pm4o_oa_da.csv:threat_tier (DATAMINED)"
    r = rec.lower()
    if "/nemesis/" in r:
        return "nemesis", "INFERRED from record path /nemesis/"
    if "boss&quest" in r or (mclass or "") in ("Boss", "Quest"):
        return "boss", f"INFERRED from path/monsterClassification={mclass}"
    if "/hero/" in r or (mclass or "") in ("Hero", "Champion") or "bounty" in r:
        return "champion-hero", f"INFERRED from path/monsterClassification={mclass}"
    return "trash", f"INFERRED from path/monsterClassification={mclass}"


def main(out_path: str) -> None:
    # ── loaders (the oracle's own) ──────────────────────────────────────────────────────────
    ro, _pets, rep = th.load_profiles(dot_corrections=True, pool_lift=PL.load())
    by_base = {base(k): k for k in ro}
    mit = {(r["record"], int(r["wave"])): r for r in csv.DictReader(open(INPUTS["pm4l_mitigation_by_body.csv"]))}
    board_rows = [r for r in csv.DictReader(open(INPUTS["pm4o_oa_da.csv"])) if r["row_kind"] == "monster"]
    board_idx = {(r["record_path"], int(r["wave"])): r for r in board_rows}
    mclass = {r["record"]: r["monster_class"] for r in csv.DictReader(open(INPUTS["pm4i_band_c_roster.csv"]))}
    lineup_csv = list(csv.DictReader(open(INPUTS["kc2_referent_lineup_v3p11.csv"])))
    board_by_rec = defaultdict(list)
    for r in csv.DictReader(open(INPUTS["pm4o_oa_da.csv"])):
        if r["row_kind"] == "monster":
            board_by_rec[r["record_path"]].append(r)
    tt = {r["record_path"]: r for r in csv.DictReader(open(INPUTS["pm4o_trash_terms.csv"]))}
    # Ultimate-pak DA terms: constant on all 95 board rows (pm4o da_flat_ultimate_pak / da_mod_pct_ultimate_pak).
    ULT_DA_FLAT, ULT_DA_PCT = 75.0, -8.0

    # ── populations ─────────────────────────────────────────────────────────────────────────
    ref_w: dict = defaultdict(float)       # (record, wave) -> bodies
    for w, pts in rl.REFERENT_LINEUP.items():
        for _p, alts in pts.items():
            share = 1.0 / len(alts)        # several alternatives at a point: equal split (DECLARED)
            for a in alts:
                for pin in a.pins:
                    for c in pin.candidates:
                        ref_w[(by_base[c], w)] += pin.count * share / len(pin.candidates)
    board_w = {(r["record_path"], int(r["wave"])): float(r["n_actors_this_wave"] or 0) for r in board_rows}

    cells = sorted(set(ref_w) | set(board_w))
    rows = {}
    folds = {w: off.fold_at(w, to_hit=True, attack_speed=True) for w in WAVES}
    gmags = {w: gm.GlobalMagnitudeFold(wave=w, board=mb.MeasuredBoardFold(wave=w),
                                       c11b=gm.C11bAttributeFold()) for w in WAVES}
    hp_lo = {w: ms.ehp_lookup_band_b(w, ms.LevelLimb.LO) for w in WAVES}
    hp_hi = {w: ms.ehp_lookup_band_b(w, ms.LevelLimb.HI) for w in WAVES}
    lv_lo = ms.level_lookup_band_b(ms.LevelLimb.LO)

    for rec, w in cells:
        p = ro[rec]
        fo, g = folds[w], gmags[w]
        gt = g.terms_for(rec)

        def row_hit(r, folded: bool):
            if r.kind not in ("direct",) or r.damage_type in NON_FLAT_TYPES:
                return None
            mag = r.magnitude()
            if not folded:
                return mag
            a, t, own = g.multipliers(gt, kind=r.kind, damage_type=r.damage_type)
            return mag * a * t * (fo.mult_for(r.kind, r.damage_type) + own)

        def slot_entry(name, rws, cd, chance, weapon):
            fam_raw, fam_fold = defaultdict(float), defaultdict(float)
            lohi = defaultdict(lambda: [0.0, 0.0])
            excluded = defaultdict(int)
            for r in rws:
                v = row_hit(r, False)
                if v is None:
                    excluded[f"{r.kind}:{r.damage_type}"] += 1
                    continue
                fam_raw[r.damage_type] += v
                fam_fold[r.damage_type] += row_hit(r, True)
                lohi[r.damage_type][0] += r.lo
                lohi[r.damage_type][1] += (r.hi if r.hi > 0 else r.lo)
            return {"slot": name, "weapon_swing": weapon, "cooldown_or_delay_s": cd, "chance_pct": chance,
                    "raw_min_max_by_type": {k: v for k, v in sorted(lohi.items())},
                    "raw_mean_by_type": dict(sorted(fam_raw.items())),
                    "folded_mean_by_type": {k: round(v, 3) for k, v in sorted(fam_fold.items())},
                    "raw_total_per_hit": round(sum(fam_raw.values()), 3),
                    "folded_total_per_hit": round(sum(fam_fold.values()), 3),
                    "rows_not_flat_per_hit": dict(excluded)}

        slots = []
        if p.weapon_rows:
            slots.append(slot_entry("weapon_swing(basic)", p.weapon_rows, None, None, True))
        for s in p.slots:
            rws = list(s.rows) + (list(p.weapon_rows) if s.is_weapon_swing else [])
            slots.append(slot_entry(s.slot, rws, s.effective_cooldown_s, s.chance_pct, s.is_weapon_swing))
        hit_slots = [x for x in slots if x["folded_total_per_hit"] > 0]
        m = mit.get((rec, w))
        b = board_idx.get((rec, w))
        tier = b["threat_tier"] if b else None
        role, role_src = role_of(rec, tier, mclass.get(rec))
        oa_fold = p.oa_for(fo)
        # ── OA / DA, best available, with the source named (gd_notes.md § OA/DA) ──
        anyw = sorted(board_by_rec.get(rec, []), key=lambda r: abs(int(r["wave"]) - w))
        strn = (float(b["da_attr_characterStrength"]) if b else
                float(anyw[0]["da_attr_characterStrength"]) if anyw else
                float(tt[rec]["str_total"]) if rec in tt else None)
        lvl = lv_lo.get(rec)
        da_recon = None
        if m and lvl is not None:
            da_recon = ((float(m["DA_bio"]) + float(m["DA_wave_flat"]) + ULT_DA_FLAT + 12 * lvl
                         + 0.5 * (strn or 0.0)) * (1 + (float(m["DA_wave_pct"]) + ULT_DA_PCT) / 100) + 53)
        if b:
            oa_best, da_best, oada_src = float(b["OA"]), float(b["DA"]), "BOARD-EXACT (pm4o_oa_da.csv OA/DA at this wave)"
        elif anyw:
            oa_best, da_best = float(anyw[0]["OA"]), float(anyw[0]["DA"])
            oada_src = f"BOARD-SAME-RECORD-OTHER-WAVE (pm4o row at w{anyw[0]['wave']})"
        else:
            oa_best, da_best = oa_fold, da_recon
            oada_src = ("RECON: OA = oracle profile oa_for(fold_at(w,to_hit=True)) [dex term ABSENT, lower bound]; "
                        "DA = stored DA equation over pm4l DA_bio + wave + ultimate pak + 12*level_lo"
                        + (" + 0.5*str (pm4o_trash_terms)" if strn is not None else " [str ABSENT, lower bound]"))
        rows[f"{rec}@w{w}"] = {
            "record": rec, "wave": w, "role": role, "role_source": role_src,
            "monster_classification": mclass.get(rec),
            "weight_ref_bodies": round(ref_w.get((rec, w), 0.0), 4),
            "weight_board_actors": board_w.get((rec, w), 0.0),
            "level_band_b_lo": lv_lo.get(rec), "level_profile": p.level,
            "hp_lo": hp_lo[w].get(rec), "hp_hi": hp_hi[w].get(rec),
            "OA_board": float(b["OA"]) if b else None,
            "OA_profile_folded_to_hit": round(oa_fold, 3),
            "OA_profile_unfolded": p.oa_eff,
            "OA_best": oa_best, "DA_best": da_best, "OA_DA_source": oada_src,
            "DA_reconstructed": round(da_recon, 3) if da_recon is not None else None,
            "DA_pm4l_partial_NOT_EQUATION_DA": float(m["DA"]) if m else None,
            "armor": float(m["armor"]) if m else None,
            "absorption_pct": float(m["absorption_pct"]) if m else None,
            "resists": {k: float(m[k]) for k in RESISTS} if m else None,
            "swing_period_s": p.swing_period_s,
            "swing_period_s_with_wave_attack_speed": (p.swing_period_s / fo.attack_speed_mult
                                                      if p.swing_period_s else None),
            "slots": slots,
            "dmg_raw_basic_hit": slots[0]["raw_total_per_hit"] if p.weapon_rows else None,
            "dmg_folded_basic_hit": slots[0]["folded_total_per_hit"] if p.weapon_rows else None,
            "dmg_folded_max_slot": max((x["folded_total_per_hit"] for x in hit_slots), default=None),
            "dmg_folded_mean_slot": (statistics.mean(x["folded_total_per_hit"] for x in hit_slots)
                                     if hit_slots else None),
            "dmg_raw_max_slot": max((x["raw_total_per_hit"] for x in hit_slots), default=None),
            "special_reuse_s_min": min((x["cooldown_or_delay_s"] for x in slots
                                        if x["cooldown_or_delay_s"]), default=None),
            "global_terms": {"dex": gt.dexterity, "int": gt.intelligence,
                             "own_tdm_pct": gt.own_total_damage_modifier_pct,
                             "physical_clamped": gt.physical_clamped,
                             "attr_basis": gt.attr_basis, "own_basis": gt.own_basis},
        }

    # ── footage HP cross-check (lineup CSV max_hp_fingerprints vs band-B lo..hi) ─────────────
    xcheck = []
    for r in lineup_csv:
        nm = r["record"].strip()
        if nm in by_base and r["max_hp_fingerprints"].strip():
            fp = [float(x.replace(",", "")) for x in r["max_hp_fingerprints"].split()]
            key = f"{by_base[nm]}@w{int(r['wave'])}"
            w = int(r["wave"])
            lo, hi = hp_lo[w].get(by_base[nm]), hp_hi[w].get(by_base[nm])
            xcheck.append({"csv_line_wave": w, "record": nm, "footage_max_hp": fp, "levels_read": r["levels"],
                           "band_b_hp_lo": lo, "band_b_hp_hi": hi,
                           "all_footage_within_lo_hi": (all(lo - 1 <= x <= hi + 1 for x in fp)
                                                        if lo and hi else None),
                           "in_population": key in rows})

    # ── summaries ───────────────────────────────────────────────────────────────────────────
    fields = {
        "hp_lo": lambda x: x["hp_lo"], "hp_hi": lambda x: x["hp_hi"],
        "dmg_folded_basic_hit": lambda x: x["dmg_folded_basic_hit"],
        "dmg_folded_max_slot": lambda x: x["dmg_folded_max_slot"],
        "dmg_folded_mean_slot": lambda x: x["dmg_folded_mean_slot"],
        "dmg_raw_basic_hit": lambda x: x["dmg_raw_basic_hit"],
        "dmg_raw_max_slot": lambda x: x["dmg_raw_max_slot"],
        "OA_profile_folded_to_hit": lambda x: x["OA_profile_folded_to_hit"],
        "OA_board": lambda x: x["OA_board"],
        "OA_best": lambda x: x["OA_best"], "DA_best": lambda x: x["DA_best"],
        "DA_reconstructed": lambda x: x["DA_reconstructed"],
        "DA_pm4l_partial_NOT_EQUATION_DA": lambda x: x["DA_pm4l_partial_NOT_EQUATION_DA"],
        "armor": lambda x: x["armor"],
        "absorption_pct": lambda x: x["absorption_pct"],
        "swing_period_s": lambda x: x["swing_period_s"],
        "swing_period_s_with_wave_attack_speed": lambda x: x["swing_period_s_with_wave_attack_speed"],
        "special_reuse_s_min": lambda x: x["special_reuse_s_min"],
        **{k: (lambda kk: (lambda x: x["resists"][kk] if x["resists"] else None))(k) for k in RESISTS},
    }
    summaries = {}
    for pop, wkey in (("REF", "weight_ref_bodies"), ("BOARD", "weight_board_actors")):
        sel = [x for x in rows.values() if x[wkey] > 0]
        summaries[pop] = {"n_cells": len(sel), "n_records": len({x["record"] for x in sel}),
                          "bodies": round(sum(x[wkey] for x in sel), 3),
                          "roles_by_bodies": {}, "equal_per_cell": {}, "body_weighted": {}}
        for x in sel:
            summaries[pop]["roles_by_bodies"][x["role"]] = round(
                summaries[pop]["roles_by_bodies"].get(x["role"], 0) + x[wkey], 3)
        for f, fn in fields.items():
            vals = [fn(x) for x in sel]
            ws = [x[wkey] for x in sel]
            summaries[pop]["equal_per_cell"][f] = q(vals)
            summaries[pop]["body_weighted"][f] = q(vals, ws)
        summaries[pop]["OA_DA_source_counts"] = {}
        for x in sel:
            k = x["OA_DA_source"].split(" ")[0]
            summaries[pop]["OA_DA_source_counts"][k] = summaries[pop]["OA_DA_source_counts"].get(k, 0) + 1
        rc = [(x["DA_reconstructed"], x["DA_best"]) for x in sel if x["OA_DA_source"].startswith("BOARD-EXACT")
              and x["DA_reconstructed"]]
        summaries[pop]["DA_reconstruction_check_vs_board"] = {
            "n": len(rc), "min_rel_err": min((a / b - 1 for a, b in rc), default=None),
            "max_rel_err": max((a / b - 1 for a, b in rc), default=None)}
        fire = [x["resists"]["res_fire"] for x in sel if x["resists"]]
        summaries[pop]["fire_resist_census"] = {
            "n": len(fire), "ge_100_immune_cells": sum(1 for v in fire if v >= 100),
            "distinct_values": sorted(set(fire))}

    out = {
        "what": "C-13 PART 3: GD wave 151-160 enemy quantities, read through the frozen KC2 oracle's own loaders",
        "generator": "scripts/gd_enemy_quantities.py",
        "inputs_sha256": {k: sha(v) for k, v in INPUTS.items()},
        "oracle_digests_verified": {"threat.verify_substrate": True, "load_report": rep.__dict__},
        "lineup_csv_sha256_pinned_in_oracle": rl.LINEUP_CSV_SHA256,
        "wave_folds": {w: {"instant_mult": folds[w].instant_mult, "attack_speed_mult": folds[w].attack_speed_mult,
                           "oa_flat_add": folds[w].oa_flat_add, "oa_modifier_add": folds[w].oa_modifier_add,
                           "G_life_pct": ms.load_band_b_G()[w]} for w in WAVES},
        "summaries": summaries,
        "footage_hp_crosscheck": xcheck,
        "per_cell": rows,
    }
    Path(out_path).write_text(json.dumps(out, indent=1, sort_keys=False, default=str))
    print(json.dumps({k: {kk: summaries[k][kk] for kk in ("n_cells", "n_records", "bodies", "roles_by_bodies")}
                      for k in summaries}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gd_enemy_quantities.json")
