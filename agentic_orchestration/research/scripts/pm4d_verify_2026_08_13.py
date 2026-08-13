#!/usr/bin/env python3
"""KC2-PM4 Lap D VERIFIER -- the conductor's three hooks, plus the board magnitude.

    V-a  COVERAGE   -- n/188 rolled actors, n/91 rolled records, n/663 pool, n/748 closed
    V-b  AGREEMENT  -- the 6 already-covered actors must reproduce their existing eHP.
                       Disagreement is a FINDING, never a silent overwrite.
    V-c  WAVE-160   -- SIGMA eHP consistency with the existing 15,967,220-across-5-bodies figure
    V-d  MAGNITUDE  -- per-wave SIGMA eHP the sim gains, waves 151-170 (what I-1 actually buys)
    V-e  PETS       -- cross-reference against Lap B's 149/149 pet chain (no duplication)
    V-f  STRUCTURE  -- monotone in wave, convex in L, floor-not-round, no negative eHP

READ-ONLY.  Author: legolas, 2026-08-13.
"""
from __future__ import annotations

import collections
import csv
import json
import math
import pathlib
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/scripts")
import pm4d_lib_2026_08_13 as L  # noqa: E402

NOTES = pathlib.Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/"
                     "legolas/notes/2026-08-13-kc2-pm4-lap-d-roster-ehp")
SEP = "=" * 98
OUT: dict = {}

#: PM-3 S 5's published figures. Targets to CHECK AGAINST, never inputs to anything.
PM3_BODIES_ROLLED = 188
PM3_RECORDS_COVERED_ACTORS = 6
PM3_W160_SUM_EHP = 15_967_220
PM3_W160_BODIES = 5


def load_long():
    idx: dict = {}
    with (NOTES / "pm4d_band_b_ehp_by_wave.csv").open() as fh:
        for r in csv.DictReader(fh):
            if not r["wave"]:
                continue
            idx[(r["record"], int(r["wave"]))] = (float(r["ehp_lo"]), float(r["ehp_hi"]))
    return idx


def load_wide():
    with (NOTES / "pm4d_band_b_monster_life.csv").open() as fh:
        return {r["record"]: r for r in csv.DictReader(fh)}


def main() -> None:
    surv = L.survival_life_modifier_array()
    ult = L.ultimate_life_modifier_pct()
    long = load_long()
    wide = load_wide()
    acts20 = L.rolled_actors(first=151, last=170)
    acts10 = L.rolled_actors(first=151, last=160)
    rolled20 = L.rolled_records(first=151, last=170)
    rolled10 = L.rolled_records(first=151, last=160)
    rec_pools, _rw, _rs, _rk, _pools = L.pool_population()

    # ═════════════════════════════════════════════════════════════════════════════════ V-a
    print(SEP)
    print("V-a  COVERAGE -- every ratio names its population (NOTE-9)")
    print(SEP)
    meas = {rec for rec, r in wide.items() if r["life_grade"] == "MEASURED"}

    def cov(name, pop_recs, pop_actors=None):
        n_rec = sum(1 for r in pop_recs if r in meas)
        line = f"    {name:34s} records {n_rec:4d}/{len(pop_recs):4d} = {100*n_rec/len(pop_recs):6.2f} %"
        n_act = None
        if pop_actors is not None:
            n_act = sum(1 for a in pop_actors if a["record_path"].lower() in meas)
            line += f"   actors {n_act:4d}/{len(pop_actors):4d} = {100*n_act/len(pop_actors):6.2f} %"
        print(line)
        return {"records_measured": n_rec, "records_total": len(pop_recs),
                "actors_measured": n_act,
                "actors_total": len(pop_actors) if pop_actors is not None else None}

    OUT["coverage"] = {
        "P-ROLLED-10 (PM-3 S 5)": cov("P-ROLLED-10  waves 151-160", set(rolled10), acts10),
        "P-ROLLED-20": cov("P-ROLLED-20  waves 151-170", set(rolled20), acts20),
        "P-POOL": cov("P-POOL       pool records", set(rec_pools)),
        "P-CLOSED": cov("P-CLOSED     + summon fixpoint", set(wide)),
    }
    before = sum(1 for a in acts10 if (a.get("hp_max") or 0) > 0)
    after = OUT["coverage"]["P-ROLLED-10 (PM-3 S 5)"]["actors_measured"]
    print(f"\n    ⚑ PM-3 S 5's population, before -> after : "
          f"{before}/{len(acts10)} ({100*before/len(acts10):.1f} %) -> "
          f"{after}/{len(acts10)} ({100*after/len(acts10):.1f} %) actors with a body")
    print(f"       bodies that entered with hp_max = 0 and now do not : {after - before}")
    OUT["coverage"]["pm3_before_after"] = {"population": "P-ROLLED-10 actors",
                                           "n": len(acts10), "before": before, "after": after,
                                           "pm3_published_covered": PM3_RECORDS_COVERED_ACTORS,
                                           "pm3_published_rolled": PM3_BODIES_ROLLED,
                                           "rolled_agrees": len(acts10) == PM3_BODIES_ROLLED,
                                           "covered_agrees": before == PM3_RECORDS_COVERED_ACTORS}

    # ═════════════════════════════════════════════════════════════════════════════════ V-b
    print("\n" + SEP)
    print("V-b  AGREEMENT on the already-covered bodies -- disagreement is a FINDING")
    print(SEP)
    covered = [a for a in acts10 if (a.get("hp_max") or 0) > 0]
    agree = disagree = 0
    detail = []
    for a in covered:
        rec = a["record_path"].lower()
        w = int(a["wave"])
        lo, hi = long.get((rec, w), (None, None))
        sim = float(a["hp_max"])
        lo_ok = lo is not None and abs(lo - sim) < 0.5
        hi_ok = hi is not None and abs(hi - sim) < 0.5
        # ALSO check against wave 160, because the sim applied the WAVE-160 board at EVERY wave.
        lo160, hi160 = long.get((rec, 160), (None, None))
        m = ("EXACT@lo" if lo_ok else "EXACT@hi" if hi_ok else
             "EXACT@w160-lo" if lo160 is not None and abs(lo160 - sim) < 0.5 else
             "EXACT@w160-hi" if hi160 is not None and abs(hi160 - sim) < 0.5 else "DISAGREE")
        (agree, disagree) = (agree + 1, disagree) if m != "DISAGREE" else (agree, disagree + 1)
        detail.append({"record": rec, "wave": w, "sim_hp_max": sim,
                       "lap_d_ehp_lo_at_wave": lo, "lap_d_ehp_hi_at_wave": hi,
                       "lap_d_ehp_lo_w160": lo160, "lap_d_ehp_hi_w160": hi160, "match": m})
        print(f"    w{w}  {rec.split('/')[-1]:36s} sim {sim:12,.0f}   "
              f"lap-D@w{w} lo {lo:12,.0f} hi {hi:12,.0f}   [{m}]")
    print(f"\n    reproduced {agree}/{len(covered)} · disagreements {disagree}")
    OUT["agreement"] = {"population": "the 6 covered actors of P-ROLLED-10",
                        "n": len(covered), "reproduced": agree, "disagree": disagree,
                        "detail": detail}

    # ⚑ THE FINDING THIS HOOK SURFACES.
    off_wave = [d for d in detail if d["match"].startswith("EXACT@w160") and d["wave"] != 160]
    if off_wave:
        print(f"\n    ⚑ FINDING -- {len(off_wave)} covered actor(s) reproduce ONLY at wave 160's G, "
              f"not at their own wave's:")
        for d in off_wave:
            corr = d["lap_d_ehp_lo_at_wave"]
            print(f"        {d['record'].split('/')[-1]} rolled on wave {d['wave']} "
                  f"(G={L.G_at(surv, d['wave']):.0f}) but entered at {d['sim_hp_max']:,.0f} "
                  f"= the wave-160 value (G=324).")
            print(f"        Its wave-{d['wave']} eHP is {corr:,.0f} -- the sim OVERSTATED this body "
                  f"by {100*(d['sim_hp_max']/corr - 1):+.2f} %.")
            print(f"        Mechanism: the driver builds ONE `board160` dict and hands it to every "
                  f"wave in 151-160 (gamora_kc2_pm3_fight_v2 :: line ~169/184). The wave-160 board "
                  f"is a wave-160 object.")
        OUT["agreement"]["off_wave_finding"] = off_wave

    dupes = [d for d in detail if d["match"] == "EXACT@hi"]
    if dupes:
        print(f"\n    ⚑ FINDING -- {len(dupes)} covered actor(s) reproduce on the HI limb:")
        for d in dupes:
            print(f"        {d['record'].split('/')[-1]} entered at {d['sim_hp_max']:,.0f} = "
                  f"lap-D HI ({d['lap_d_ehp_hi_at_wave']:,.0f}); LO is "
                  f"{d['lap_d_ehp_lo_at_wave']:,.0f} ({100*(d['sim_hp_max']/d['lap_d_ehp_lo_at_wave']-1):+.2f} %).")
        print(f"        Mechanism: `{{e.record: e.ehp for e in load_wave160_board()}}` is a dict "
              f"over a CSV that carries duplicate records; last row wins.")
        # count the collisions on the r2 board
        c = collections.Counter()
        with (L.BOARD160_CSV).open() as fh:
            for r in csv.DictReader(fh):
                c[r["record"].lower()] += 1
        col = {k: v for k, v in c.items() if v > 1}
        print(f"        The r2 board carries {len(col)} record(s) on more than one row "
              f"({sum(col.values())} rows collapse to {len(col)}); the surviving limb is "
              f"CSV-ORDER-DETERMINED, not ruled.")
        OUT["agreement"]["limb_collision_finding"] = {
            "records_with_duplicate_rows_on_r2_board": col,
            "note": "baton declares DECLARED-LEVEL-LO-LIMB (F5-A -> LO) for band-A-sourced bodies; "
                    "band-B board bodies get whichever CSV row is last."}

    # ═════════════════════════════════════════════════════════════════════════════════ V-c
    print("\n" + SEP)
    print("V-c  WAVE-160 SIGMA eHP -- against PM-3 S 5's 15,967,220 across 5 bodies")
    print(SEP)
    w160 = [a for a in acts10 if int(a["wave"]) == 160]
    old_sum = sum(float(a["hp_max"]) for a in w160)
    old_n = sum(1 for a in w160 if float(a["hp_max"]) > 0)
    new_lo = sum(long[(a["record_path"].lower(), 160)][0] for a in w160
                 if (a["record_path"].lower(), 160) in long)
    new_hi = sum(long[(a["record_path"].lower(), 160)][1] for a in w160
                 if (a["record_path"].lower(), 160) in long)
    n_new = sum(1 for a in w160 if (a["record_path"].lower(), 160) in long)
    print(f"    wave-160 actors rolled                     : {len(w160)}")
    print(f"    bodies the sim had                         : {old_n}   SIGMA {old_sum:14,.0f}")
    print(f"    PM-3 S 5 published                         : {PM3_W160_BODIES}   SIGMA {PM3_W160_SUM_EHP:14,.0f}"
          f"   {'AGREES' if abs(old_sum - PM3_W160_SUM_EHP) < 1 else 'DISAGREES'}")
    print(f"    bodies Lap D supplies                      : {n_new}   "
          f"SIGMA lo {new_lo:14,.0f}   SIGMA hi {new_hi:14,.0f}")
    # subset agreement: the overlap must reproduce
    ov_old = sum(float(a["hp_max"]) for a in w160 if float(a["hp_max"]) > 0)
    ov_lo = sum(long[(a["record_path"].lower(), 160)][0] for a in w160 if float(a["hp_max"]) > 0)
    ov_hi = sum(long[(a["record_path"].lower(), 160)][1] for a in w160 if float(a["hp_max"]) > 0)
    print(f"    ⚑ ON THE OVERLAP ({old_n} bodies)            : sim {ov_old:14,.0f}   "
          f"lap-D lo {ov_lo:14,.0f}   lap-D hi {ov_hi:14,.0f}")
    print(f"       overlap reproduces on the HI limb: {abs(ov_hi - ov_old) < 1}   "
          f"on the LO limb: {abs(ov_lo - ov_old) < 1}")
    print(f"    board growth (hi limb)                     : x{new_hi/old_sum:.2f}")
    OUT["wave160"] = {"population": "P-ROLLED-10 actors on wave 160", "actors": len(w160),
                      "sim_bodies": old_n, "sim_sum": old_sum,
                      "pm3_published_sum": PM3_W160_SUM_EHP,
                      "pm3_published_bodies": PM3_W160_BODIES,
                      "agrees_with_pm3": abs(old_sum - PM3_W160_SUM_EHP) < 1,
                      "lapd_bodies": n_new, "lapd_sum_lo": new_lo, "lapd_sum_hi": new_hi,
                      "overlap_sim": ov_old, "overlap_lapd_lo": ov_lo, "overlap_lapd_hi": ov_hi,
                      "overlap_reproduces_hi": abs(ov_hi - ov_old) < 1,
                      "overlap_reproduces_lo": abs(ov_lo - ov_old) < 1}

    # ═════════════════════════════════════════════════════════════════════════════════ V-d
    print("\n" + SEP)
    print("V-d  MAGNITUDE -- per-wave SIGMA eHP the board gains (P-ROLLED-20 actors)")
    print(SEP)
    print(f"    {'wave':>5} {'G':>5} {'actors':>7} {'sim bodies':>11} {'SIGMA sim':>15} "
          f"{'SIGMA lap-D lo':>16} {'SIGMA lap-D hi':>16} {'x lo':>7}")
    per_wave = []
    for w in range(151, 171):
        aw = [a for a in acts20 if int(a["wave"]) == w]
        so = sum(float(a["hp_max"]) for a in aw)
        sn = sum(1 for a in aw if float(a["hp_max"]) > 0)
        lo = sum(long[(a["record_path"].lower(), w)][0] for a in aw
                 if (a["record_path"].lower(), w) in long)
        hi = sum(long[(a["record_path"].lower(), w)][1] for a in aw
                 if (a["record_path"].lower(), w) in long)
        ratio = (lo / so) if so else float("inf")
        print(f"    {w:>5} {L.G_at(surv,w):>5.0f} {len(aw):>7} {sn:>11} {so:>15,.0f} "
              f"{lo:>16,.0f} {hi:>16,.0f} " + (f"{ratio:>7.1f}" if so else "     inf"))
        per_wave.append({"wave": w, "G": L.G_at(surv, w), "actors": len(aw),
                         "sim_bodies": sn, "sim_sum": so, "lapd_sum_lo": lo, "lapd_sum_hi": hi})
    tot_old = sum(x["sim_sum"] for x in per_wave)
    tot_lo = sum(x["lapd_sum_lo"] for x in per_wave)
    tot_hi = sum(x["lapd_sum_hi"] for x in per_wave)
    print(f"    {'TOTAL':>5} {'':>5} {len(acts20):>7} "
          f"{sum(x['sim_bodies'] for x in per_wave):>11} {tot_old:>15,.0f} "
          f"{tot_lo:>16,.0f} {tot_hi:>16,.0f} {tot_lo/tot_old:>7.1f}")
    OUT["magnitude"] = {"population": "P-ROLLED-20 actors", "per_wave": per_wave,
                        "total_sim": tot_old, "total_lapd_lo": tot_lo, "total_lapd_hi": tot_hi}
    # the 151-160 band, which is what PM-3 measured
    t10_old = sum(x["sim_sum"] for x in per_wave if x["wave"] <= 160)
    t10_lo = sum(x["lapd_sum_lo"] for x in per_wave if x["wave"] <= 160)
    print(f"\n    ⚑ waves 151-160 (PM-3's band): SIGMA sim {t10_old:,.0f} -> lap-D lo "
          f"{t10_lo:,.0f}  = x{t10_lo/t10_old:.1f}")
    OUT["magnitude"]["band_151_160"] = {"sim": t10_old, "lapd_lo": t10_lo,
                                        "ratio": t10_lo / t10_old}

    # ═════════════════════════════════════════════════════════════════════════════════ V-e
    print("\n" + SEP)
    print("V-e  PET CROSS-REFERENCE -- Lap B measured pet life 149/149; NOT duplicated here")
    print(SEP)
    pc = L.DATA / "pm2_tg2_pet_chain.csv"
    pet_rows = [r for r in csv.DictReader(pc.open()) if r.get("pet_record")]
    pet_recs = {r["pet_record"].lower() for r in pet_rows}
    print(f"    Lap B pet chain rows with a pet_record : {len(pet_rows)}  "
          f"(life_grade MEASURED on {sum(1 for r in pet_rows if r['life_grade']=='MEASURED')})")
    print(f"    distinct pet bodies                    : {len(pet_recs)}")
    ov = pet_recs & set(wide)
    print(f"    reached by this lap's P-CLOSED         : {len(ov)} / {len(pet_recs)}   "
          f"[IS-B2 + IS-B3; band A's own closure reached 43]")
    print(f"    NOT reached                            : {sorted(pet_recs - set(wide))}")

    # ⚑ THE CLIFF. The two folds are compared, not merged; the ruling is the conductor's.
    ratios, ex = [], []
    for r in pet_rows:
        p = r["pet_record"].lower()
        if (p, 160) not in long or not r.get("pet_life_at_owner_level"):
            continue
        lapb = float(r["pet_life_at_owner_level"])
        lo, hi = long[(p, 160)]
        if lapb <= 0:
            continue
        ratios.append(lo / lapb)
        if len(ex) < 4:
            ex.append((p.split("/")[-1], lapb, lo, lo / lapb))
    ratios.sort()
    if ratios:
        med = ratios[len(ratios) // 2]
        print(f"\n    ⚑ CLIFF C-D1 -- THE TWO FOLDS ON ONE BOARD DO NOT AGREE, AND I DO NOT RULE IT.")
        print(f"       Lap B's `pet_life_at_owner_level` = floor(base x (1 + tree_pct/100)).")
        print(f"       It folds the granted-passive term ONLY. It does NOT fold the Ultimate cell")
        print(f"       (+580 %) nor the Crucible wave term G. The roster chain folds both.")
        print(f"       Over the {len(ratios)} pet rows this lap also covers, at wave 160:")
        print(f"           lap-D eHP / Lap-B pet life :  min {ratios[0]:.2f}   med {med:.2f}   "
              f"max {ratios[-1]:.2f}")
        for n, a, b, rr in ex:
            print(f"           {n:44s} Lap-B {a:10,.0f}   lap-D {b:12,.0f}   x{rr:.2f}")
        print(f"       CONSEQUENCE IF UNRESOLVED: once I-1 lands, pet bodies become the SOFTEST")
        print(f"       targets on the board by a factor of ~{med:.0f}, and PM-3 S 10's note that")
        print(f"       'CLUSTER's live set includes pets (they are the only bodies carrying real")
        print(f"       HP)' inverts into its opposite -- the sim would prefer pets for the wrong")
        print(f"       reason. FILED, not improvised past. This lap emits a same-chain value for")
        print(f"       all {len(ov)} pet bodies so the conductor can rule either way from measured")
        print(f"       numbers. I have NO evidence on which fold the game applies to a summon.")
    OUT["pets"] = {"lapb_pet_rows": len(pet_rows), "lapb_pet_bodies": len(pet_recs),
                   "reached_by_P_CLOSED": len(ov),
                   "not_reached": sorted(pet_recs - set(wide)),
                   "policy": "CROSS-REFERENCED, NOT DUPLICATED (charter instruction)",
                   "CLIFF_C_D1": {
                       "what": "Lap-B pet life folds granted passives ONLY; the roster chain folds "
                               "Ultimate (+580) + Crucible G + passives. Same board, two folds.",
                       "n_compared": len(ratios),
                       "ratio_lapd_over_lapb_at_w160": {
                           "min": ratios[0] if ratios else None,
                           "median": med if ratios else None,
                           "max": ratios[-1] if ratios else None},
                       "disposition": "FILED for the conductor. legolas does NOT rule it: no "
                                      "measured evidence was found either way on whether the "
                                      "Crucible applies its wave scaling to summoned bodies."}}

    # ═════════════════════════════════════════════════════════════════════════════════ V-f
    print("\n" + SEP)
    print("V-f  STRUCTURAL CHECKS on the emitted table")
    print(SEP)
    bad_mono = bad_sign = bad_limb = 0
    for rec, r in wide.items():
        if r["life_grade"] != "MEASURED":
            continue
        seq = [long[(rec, w)][0] for w in range(151, 171)]
        if any(b < a for a, b in zip(seq, seq[1:])):
            bad_mono += 1
        if any(x < 0 for x in seq):
            bad_sign += 1
        if long[(rec, 160)][1] < long[(rec, 160)][0]:
            bad_limb += 1
    print(f"    population: {len(meas)} MEASURED records x 20 waves")
    print(f"    eHP non-decreasing in wave (G is non-decreasing on 151-170) : "
          f"violations {bad_mono}")
    print(f"    eHP >= 0                                                    : violations {bad_sign}")
    print(f"    eHP(hi limb) >= eHP(lo limb)                                : violations {bad_limb}")
    # floor-not-round, re-derived independently of the emitter
    spot = 0
    for rec in sorted(meas)[:200]:
        r = wide[rec]
        lo = int(r["level_lo"])
        base = float(r["base_life_lo"]); pas = float(r["life_passive_pct_lo"])
        e = math.floor(base * (1.0 + (ult + L.G_at(surv, 160) + pas) / 100.0))
        if abs(e - long[(rec, 160)][0]) < 0.5:
            spot += 1
    print(f"    floor-not-round re-derivation spot-check (200 records)      : {spot}/200 EXACT")
    OUT["structure"] = {"population": f"{len(meas)} MEASURED records x 20 waves",
                        "monotone_violations": bad_mono, "negative_violations": bad_sign,
                        "limb_order_violations": bad_limb, "floor_spotcheck": f"{spot}/200"}

    # ═════════════════════════════════════════════════════════════════════════════════ V-g
    print("\n" + SEP)
    print("V-g  ARITHMETIC CONSEQUENCE -- what the covered board costs at the sim's OWN kill term")
    print(SEP)
    print("    ⚑ THIS IS DIVISION, NOT A PREDICTION.  It ignores travel, arrival, overkill, pets,")
    print("       leech, deaths and every other term.  gamora's fold is what decides anything.")
    try:
        sys.path.insert(0, str(L.ENGINE / "src"))
        from reincarnated.simulation.kc2 import monster_stats as ms  # noqa: E402
        from reincarnated.simulation.kc2.channel import ticks_per_s  # noqa: E402
        from reincarnated.simulation.kc2.fixture import FIXTURE_ATTACK_SPEED_PCT, v  # noqa: E402
        tps = ticks_per_s(float(v(FIXTURE_ATTACK_SPEED_PCT)))
        band = OUT["magnitude"]["band_151_160"]
        #: The limb the RUN OF RECORD uses -- `gamora_kc2_phase_e_seeded_batch` line 77 sets
        #: `PLAYER_DAMAGE_LIMB = SHEET_MEASURED`, and the PM-3 driver imports it from there.
        #: Reading the default (`DB_COMPONENT`) instead would report a limb nothing ran on.
        rows = {}
        for limb in (ms.PlayerDamageLimb.SHEET_MEASURED, ms.PlayerDamageLimb.DB_COMPONENT):
            pt = ms.player_damage_per_tick(limb)
            dps = pt * tps
            rows[limb.name] = {"per_tick": pt, "dps": dps,
                               "contact_s_sim": band["sim"] / dps,
                               "contact_s_lapd": band["lapd_lo"] / dps}
        print(f"    ticks/s = {tps:.4f}   waves 151-160 SIGMA eHP  sim {band['sim']:,.0f} -> "
              f"lap-D {band['lapd_lo']:,.0f}")
        print(f"    {'limb':>16} {'dmg/tick':>12} {'dps':>13} {'contact s (sim)':>17} "
              f"{'contact s (lap-D)':>19}")
        for n, d in rows.items():
            mark = "  <- the run of record" if n == "SHEET_MEASURED" else ""
            print(f"    {n:>16} {d['per_tick']:>12,.0f} {d['dps']:>13,.0f} "
                  f"{d['contact_s_sim']:>17.1f} {d['contact_s_lapd']:>19.1f}{mark}")
        t_new = rows["SHEET_MEASURED"]["contact_s_lapd"]
        print(f"\n    reference MEASURED (Lap C): ten waves 151-160 in 186 s")
        print(f"    ⚑ lap-D pure-contact on the run-of-record limb : {t_new:.1f} s  "
              f"(ratio {t_new/186.0:.2f})")
        print(f"       PM-3 S 3 measured CLUSTER at 102.4 s for SIX waves on a board 96.8 % empty,")
        print(f"       and read the agreement as 'throughput matched'. On a FULL board the same")
        print(f"       kill term needs {t_new:.0f} s of contact for TEN. That is arithmetic, and it")
        print(f"       is the number I-2 has to argue with -- it is NOT a claim about the fold.")
        OUT["arithmetic"] = {"ticks_per_s": tps, "limbs": rows,
                             "run_of_record_limb": "SHEET_MEASURED",
                             "reference_measured_s": 186.0,
                             "ratio_run_of_record": t_new / 186.0,
                             "caveat": "DIVISION ONLY -- no travel, arrival, overkill, pets, "
                                       "leech or death term. Not a prediction."}
    except Exception as exc:
        print(f"    kill-term import unavailable ({type(exc).__name__}: {exc}) -- section skipped, "
              f"not estimated.")
        OUT["arithmetic"] = {"status": f"SKIPPED: {type(exc).__name__}: {exc}"}

    (NOTES / "pm4d_verify_summary.json").write_text(json.dumps(OUT, indent=2, default=str))
    print(f"\n    wrote {NOTES / 'pm4d_verify_summary.json'}")


if __name__ == "__main__":
    main()
