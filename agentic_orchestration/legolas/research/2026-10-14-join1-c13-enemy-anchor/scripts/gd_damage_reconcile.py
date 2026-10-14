#!/usr/bin/env python3
"""C-13 / KP-428 (2) — reconcile GD per-hit monster damage with the oracle's configuration of record.

READ-ONLY. Imports the sealed KC2 oracle and its v3.11 driver chain; edits NOTHING under reincarnated-engine.
Monkeypatches are in-process only (wrappers around `threat.mitigate` and `ThreatEngine.resolve_attack`
that record arguments and return the real result unchanged), restored in `finally`.

Two instruments, one question ("what per-hit damage does the referent apply before player mitigation?"):

  STATIC  — per (record, wave) cell, every slot's instant `direct` rows composed EXACTLY as the oracle of record
            composes them (threat.py resolve_attack L2023-2246 under V311-FULL's folds):
              om   = offense.fold_at(w, to_hit=True, attack_speed=True).mult_for(kind, type)      (threat.py:2039)
                     + gmag own_add                                                                (threat.py:2083)
                     + mutators.pct_add(r)  [Brutal/Corrupted +50 % on instant Pierce/Chaos]       (threat.py:2100)
              a,t  = GlobalMagnitudeFold(wave=w, board=MeasuredBoardFold(w), c11b=C11b(a_mean 1.010)).multipliers
                                                                                                   (threat.py:2079-2080)
              a   <- C11aFold(retaliation_gate, duration_divisors).attr_mult                       (threat.py:2081-2082)
              row  = CompositionFold.instant(...) = m * max(0, a + (om-1)) [+ physical term]       (gd_composition.py:130-153)
            weapon swings add the body's weapon rows + mutators.flat_rows(prof)                    (threat.py:1940-1953)
            crit: x1.0 base, and E[mult | hit] under the sealed d100 resolve_hit at the board PTH  (threat.py:390-405,1870)
            NOT static (positional): C-11a aura GRANTS (flat rows + om_add on covered bodies) -> lower bound.
  DYNAMIC — one salt of the V311-FULL oracle, arm M0 (config_of_record V0-ARM-M0 "the model of record"), with
            every landed monster hit's pre-mitigation INSTANT direct damage captured at the `mitigate` call
            (threat.py:2242: mitigate(_im * mult, type)), x volley_n x band_scale (threat.py:2245). DoT
            ('Slow*' families), leech ('Life') and %current-life rows are excluded and counted.
            This weights slots by the oracle's OWN slot-choice law (choose_slot / gd_engagement), i.e. by use.

Run (engine src on PYTHONPATH):  python3 scripts/gd_damage_reconcile.py <out.json> [salt]
"""
from __future__ import annotations

import csv
import hashlib
import json
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path

ENG = Path("/Users/admin/Games/reincarnated-engine")
PKT = Path(__file__).resolve().parents[1]
DATA = ENG / "data" / "kc2"

from reincarnated.simulation.kc2 import threat as th                       # noqa: E402
from reincarnated.simulation.kc2 import offense as off                     # noqa: E402
from reincarnated.simulation.kc2 import global_magnitude as gm             # noqa: E402
from reincarnated.simulation.kc2 import measured_board as mb               # noqa: E402
from reincarnated.simulation.kc2 import gd_composition as gc               # noqa: E402
from reincarnated.simulation.kc2 import c11a_corrections as C              # noqa: E402
from reincarnated.simulation.kc2 import mutators as mu                     # noqa: E402
from reincarnated.simulation.kc2 import pool_lift as PL                    # noqa: E402
from reincarnated.simulation.kc2 import referent_lineup as rl              # noqa: E402

WAVES = tuple(range(151, 161))
EXCL_TYPES = set(getattr(th, "NON_HEALTH_DAMAGE_TYPES", ())) | set(getattr(th, "DECODED_NON_HEALTH_TYPES", ()))


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def wq(pairs):
    pairs = sorted((v, w) for v, w in pairs if v is not None and w > 0)
    if not pairs:
        return None
    tot = sum(w for _, w in pairs)
    out = []
    for q in (0.25, 0.5, 0.75):
        acc = 0.0
        for v, w in pairs:
            acc += w
            if acc >= q * tot - 1e-9:
                out.append(v)
                break
    return {"p25": out[0], "median": out[1], "p75": out[2], "min": pairs[0][0], "max": pairs[-1][0],
            "weight_total": round(tot, 3), "n": len(pairs)}


def expected_crit_mult(p: float) -> float:
    """E[mult | hit] under the sealed `threat.resolve_hit` (d100 integer roll) at PTH p."""
    hits = [th.resolve_hit(p, roll) for roll in range(1, 101)]
    landed = [m for h, m, _ in hits if h]
    return sum(landed) / len(landed) if landed else 0.0


class _Eng:
    """The minimal attribute surface `CompositionFold.instant` reads (gmag, wave). Nothing else."""
    def __init__(self, gmag, wave):
        self.gmag, self.wave = gmag, wave
        self.offense = None


def static_part(muts=True, composition=True, c11b=True, c11a=True):
    loader = C.C11aLoader(scope=C.AuraScope.CLASS)
    roster, _pets, _rep = th.load_profiles(dot_corrections=True, pool_lift=PL.load(), c11a=loader)
    comp = gc.CompositionFold(chaos_aether_dot_divisor=True)          # V39 dec "dot" (instant path identical)
    mut = mu.MutatorFold(brutal=muts, corrupted=muts, leeching=True, cruel=True, resilient=True, ascended=True)
    with open(DATA / "pm4o_oa_da.csv", newline="") as fh:
        board = [r for r in csv.DictReader(fh) if r["row_kind"] == "monster"]
    by_base = {Path(k).stem: k for k in roster}
    ref_w = defaultdict(float)
    for w, pts in rl.REFERENT_LINEUP.items():
        for _p, alts in pts.items():
            share = 1.0 / len(alts)
            for a in alts:
                for pin in a.pins:
                    for c in pin.candidates:
                        if c in by_base:
                            ref_w[(by_base[c], w)] += pin.count * share / len(pin.candidates)
    board_w = {(r["record_path"], int(r["wave"])): float(r["n_actors_this_wave"] or 0) for r in board}
    board_role = {(r["record_path"], int(r["wave"])): r["threat_tier"] for r in board}
    board_pth = {(r["record_path"], int(r["wave"])): float(r["m2p_pth_effective"]) for r in board}
    prior = json.loads((PKT / "gd_enemy_quantities.json").read_text())["per_cell"]

    cells = {}
    for w in WAVES:
        fo = off.fold_at(w, to_hit=True, attack_speed=True)
        board_fold = mb.MeasuredBoardFold(wave=w)
        g = gm.GlobalMagnitudeFold(wave=w, board=board_fold, c11b=gm.C11bAttributeFold(a_mean=1.010) if c11b else None)
        c11 = C.C11aFold(wave=w, retaliation_gate=True, duration_divisors=True, aura=loader)
        eng = _Eng(g, w)
        for (rec, ww) in sorted(set(k for k in list(ref_w) + list(board_w) if k[1] == w)):
            p = roster.get(rec)
            if p is None:
                continue
            gt = g.terms_for(rec)
            excluded = defaultdict(int)

            def row_dmg(r):
                if r.kind != "direct" or r.damage_type in EXCL_TYPES:
                    excluded[f"{r.kind}:{r.damage_type}"] += 1
                    return None
                a, t, own = g.multipliers(gt, kind=r.kind, damage_type=r.damage_type)
                if c11a:
                    a = c11.attr_mult(gt, r, a, attr_on=g.attr_on)
                om = fo.mult_for(r.kind, r.damage_type) + own + mut.pct_add(r)
                return comp.instant(eng, p, r, a, om, t) if composition else r.magnitude() * a * om * t

            slots = []
            for s in p.slots:
                rws = list(s.rows)
                if s.is_weapon_swing:
                    rws += list(p.weapon_rows) + list(mut.flat_rows(p))
                vals = [row_dmg(r) for r in rws]
                tot = sum(v for v in vals if v is not None)
                slots.append({"slot": s.slot, "skill": s.skill, "weapon_swing": s.is_weapon_swing,
                              "per_hit_record": round(tot, 3), "chance_pct": s.chance_pct,
                              "cooldown_s": s.effective_cooldown_s})
            basic = next((x["per_hit_record"] for x in slots if x["slot"] == "basic"), None)
            hit_slots = [x["per_hit_record"] for x in slots if x["per_hit_record"] > 0]
            pth = board_pth.get((rec, w))
            ecm = expected_crit_mult(pth) if pth is not None else None
            pc = prior.get(f"{rec}@w{w}", {})
            cells[f"{rec}@w{w}"] = {
                "record": rec, "wave": w,
                "role": board_role.get((rec, w)) or pc.get("role"),
                "weight_board_actors": board_w.get((rec, w), 0.0), "weight_ref_bodies": ref_w.get((rec, w), 0.0),
                "record_basic_hit": basic, "record_max_slot": max(hit_slots, default=None),
                "pth_board": pth, "expected_crit_mult_given_hit": ecm,
                "record_basic_hit_x_crit": None if (basic is None or ecm is None) else basic * ecm,
                "prior_folded_basic_hit": pc.get("dmg_folded_basic_hit"),
                "prior_folded_max_slot": pc.get("dmg_folded_max_slot"),
                "prior_raw_basic_hit": pc.get("dmg_raw_basic_hit"),
                "n_oracle_slots": len(slots), "slots": slots, "rows_excluded_from_per_hit": dict(excluded),
                "gmag_terms": {"folds_attr": getattr(gt, "folds_attr", None), "physical_clamped": getattr(gt, "physical_clamped", None),
                               "own_add": getattr(gt, "own_add", None)},
                "offense_instant_mult": fo.instant_mult,
            }
    return cells, comp.report(), mut.report()


def engine_slot_values(eng, prof, *, composition=True, mut_flat=True, mut_pct=True, c11a=True, c11b=True):
    """Per-slot pre-mitigation INSTANT direct damage per landed hit, computed with the run's OWN ThreatEngine folds,
    line for line after threat.py resolve_attack L1932-2246 with granted=None, crit mult 1.0, n_volley 1.
    DoT / leech / %current-life / non-health rows are counted, not summed (the per-hit flat quantity)."""
    off, g = eng.offense, eng.gmag
    saved_c11b = g.c11b if g is not None else None
    if g is not None and not c11b:
        g.c11b = None
    try:
        gt = g.terms_for(prof.record) if g is not None else None
        out = []
        for slot in prof.slots:
            rows = list(slot.rows)
            if slot.is_weapon_swing:                                     # threat.py:1932-1953
                rows += list(prof.weapon_rows)
                if eng.mutators is not None and mut_flat:
                    rows += list(eng.mutators.flat_rows(prof))
            tot, excl = 0.0, defaultdict(int)
            for r in rows:
                if r.damage_type in EXCL_TYPES:                          # threat.py:2026-2037
                    excl[f"non_health:{r.damage_type}"] += 1
                    continue
                om = off.mult_for(r.kind, r.damage_type) if off is not None else 1.0   # threat.py:2039
                a = t = 1.0
                if g is not None:                                        # threat.py:2077-2090
                    a, t, own = g.multipliers(gt, kind=r.kind, damage_type=r.damage_type)
                    if eng.c11a is not None and c11a:
                        a = eng.c11a.attr_mult(gt, r, a, attr_on=g.attr_on)
                    om = om + own
                    if g.drops_leech(r.kind):
                        excl["leech_dropped"] += 1
                        continue
                if eng.mutators is not None and mut_pct:                 # threat.py:2100-2101
                    om = om + eng.mutators.pct_add(r)
                if r.kind != "direct":                                   # pcl / leech / dot: not a flat per-hit term
                    excl[f"{r.kind}:{r.damage_type}"] += 1
                    continue
                tot += (eng.composition.instant(eng, prof, r, a, om, t)  # threat.py:2230-2231
                        if (eng.composition is not None and composition) else r.magnitude() * a * om * t)
            out.append({"slot": s_name(slot), "skill": slot.skill, "weapon_swing": slot.is_weapon_swing,
                        "per_hit": tot, "chance_pct": slot.chance_pct, "cooldown_s": slot.effective_cooldown_s,
                        "reach_m": slot.reach_m, "excluded_rows": dict(excl)})
        return out
    finally:
        if g is not None:
            g.c11b = saved_c11b


def s_name(slot):
    return slot.slot


def dynamic_part(salt: int, arm: str = "M0"):
    from reincarnated.simulation.scripts import gamora_kc2_play_v3p11_oracle_2026_10_02 as V11
    from reincarnated.simulation.scripts import gamora_kc2_play_c11a_fold_pricing_2026_09_30 as FP
    real_mit, real_ra = th.mitigate, th.ThreatEngine.resolve_attack
    frame = {"on": False, "direct": 0.0, "n_dot": 0, "n_leech": 0}
    hits = []
    engines = {}

    # ⚑ `mitigate(x, "Life")` is called by BOTH the leech branch (threat.py:2160) and every Vitality ("Life")
    #   direct row (threat.py:2242), so the damage KIND is read at the composition site instead, where the row
    #   object is in hand: CompositionFold.instant is the `_im` of every instant row (threat.py:2160/2230).
    real_inst, real_dot = gc.CompositionFold.instant, gc.CompositionFold.dot

    def inst(self, eng, prof, r, a_mult, om, t_mult):
        v = real_inst(self, eng, prof, r, a_mult, om, t_mult)
        if frame["on"]:
            if r.kind == "direct":
                frame["direct"] += v
            else:
                frame["n_leech"] += 1
        return v

    def dot(self, eng, prof, r, om):
        if frame["on"]:
            frame["n_dot"] += 1
        return real_dot(self, eng, prof, r, om)

    def mit(damage, damage_type, *a, **kw):
        return real_mit(damage, damage_type, *a, **kw)

    def ra(self, *a, **kw):
        engines.setdefault(id(self), self)
        frame.update(on=True, direct=0.0, n_dot=0, n_leech=0)
        try:
            total, detail = real_ra(self, *a, **kw)
        finally:
            frame["on"] = False
        if detail.get("hit"):
            prof = kw.get("prof") if "prof" in kw else next((x for x in a if hasattr(x, "record")), None)
            slot = kw.get("slot") if "slot" in kw else next((x for x in a if hasattr(x, "slot") and hasattr(x, "rows")), None)
            n = float(detail.get("volley_n", 1)) * float(detail.get("volley_band_scale", 1.0))
            n = n * float(detail.get("multiplier", 1.0))          # raw = _im * mult * n_volley * band_scale (threat.py:2245)
            hits.append({"record": getattr(prof, "record", None), "slot": getattr(slot, "slot", None),
                         "wave": getattr(self, "wave", None), "engine_id": id(self), "raw_direct": frame["direct"] * n,
                         "multiplier": detail.get("multiplier"), "pcl": detail.get("percent_current_life", 0.0),
                         "n_dot_rows": frame["n_dot"], "n_leech_rows": frame["n_leech"],
                         "aura_granted": kw.get("granted") is not None, "volley": n,
                         "volley_n": detail.get("volley_n", 1)})
        return total, detail

    period = FP._period()            # the probe run happens BEFORE the instruments are installed
    th.mitigate = mit
    th.ThreatEngine.resolve_attack = ra
    gc.CompositionFold.instant, gc.CompositionFold.dot = inst, dot
    t0 = time.time()
    try:
        V11.run_one("V311-FULL", (salt,), period, arm=arm)
    finally:
        th.mitigate, th.ThreatEngine.resolve_attack = real_mit, real_ra
        gc.CompositionFold.instant, gc.CompositionFold.dot = real_inst, real_dot
    return hits, round(time.time() - t0, 1), period, engines


def main(out: Path, salt: int):
    cells, comp_rep, mut_rep = static_part()
    ABL = {"A0_prior_form (no composition, no c11a, no c11b, no mutator flats/pct)": dict(muts=False, composition=False, c11b=False, c11a=False),
           "A1 +c11b (a_mean 1.010)": dict(muts=False, composition=False, c11b=True, c11a=False),
           "A2 +c11a (retaliation gate, duration divisors)": dict(muts=False, composition=False, c11b=True, c11a=True),
           "A3 +composition (GD Game.dll form)": dict(muts=False, composition=True, c11b=True, c11a=True),
           "A4 +Brutal/Corrupted (= V311-FULL record)": dict(muts=True, composition=True, c11b=True, c11a=True)}
    abl = {}
    for name, kw in ABL.items():
        cc = cells if kw == dict(muts=True, composition=True, c11b=True, c11a=True) else static_part(**kw)[0]
        sel = [(c["record_basic_hit"], c["weight_board_actors"]) for c in cc.values()
               if (c.get("role") or "") == "trash"]
        mx = [(c["record_max_slot"], c["weight_board_actors"]) for c in cc.values() if (c.get("role") or "") == "trash"]
        abl[name] = {"trash_basic_board_weighted": wq(sel), "trash_max_slot_board_weighted": wq(mx)}
    t_static = time.time()
    hits, wall, period, engines_by_id = dynamic_part(salt)
    engines = {}
    for e in engines_by_id.values():
        engines.setdefault(int(e.wave), e)
    n_eng_per_wave = defaultdict(int)
    for e in engines_by_id.values():
        n_eng_per_wave[int(e.wave)] += 1
    # ── ENGINE-NATIVE STATIC: every (record, wave) cell from the run's own engine objects ─────────────
    ENG_ABL = {"E0 oracle-multiplicative, no c11a, no c11b, no mutator terms": dict(composition=False, mut_flat=False, mut_pct=False, c11a=False, c11b=False),
               "E1 +c11b": dict(composition=False, mut_flat=False, mut_pct=False, c11a=False, c11b=True),
               "E2 +c11a": dict(composition=False, mut_flat=False, mut_pct=False, c11a=True, c11b=True),
               "E3 +GD composition": dict(composition=True, mut_flat=False, mut_pct=False, c11a=True, c11b=True),
               "E4 +Brutal/Corrupted flats": dict(composition=True, mut_flat=True, mut_pct=False, c11a=True, c11b=True),
               "E5 +Brutal/Corrupted +50% pool (= RECORD)": dict(composition=True, mut_flat=True, mut_pct=True, c11a=True, c11b=True)}
    eng_cells = {}
    for key, c in cells.items():
        e = engines.get(c["wave"])
        prof = e.roster.get(c["record"]) if e is not None else None
        if prof is None:
            continue
        ent = {"role": c["role"], "weight_board_actors": c["weight_board_actors"], "weight_ref_bodies": c["weight_ref_bodies"],
               "prior_folded_basic_hit": c["prior_folded_basic_hit"], "prior_folded_max_slot": c["prior_folded_max_slot"],
               "prior_raw_basic_hit": c["prior_raw_basic_hit"]}
        for an, kw in ENG_ABL.items():
            sv = engine_slot_values(e, prof, **kw)
            dmg = [x["per_hit"] for x in sv if x["per_hit"] > 0]
            ent[an] = {"basic": next((x["per_hit"] for x in sv if x["slot"] == "basic"), None),
                       "max_slot": max(dmg, default=None), "mean_damaging_slot": statistics.mean(dmg) if dmg else None}
            if an.startswith("E5"):
                ent["slots_record"] = sv
        ent["n_oracle_slots"] = len(prof.slots)
        eng_cells[key] = ent
    # summaries
    roles = {"trash": {"trash"}, "champion-hero": {"champion-hero", "Hero", "hero"}, "boss+nemesis": {"boss", "nemesis", "Boss", "Nemesis"}}

    def role_of(c):
        r = (c.get("role") or "").lower()
        if r in ("trash",):
            return "trash"
        if "hero" in r or "champion" in r:
            return "champion-hero"
        if r in ("boss", "nemesis"):
            return "boss+nemesis"
        return r or "unknown"
    summ = {}
    for wkey in ("weight_board_actors", "weight_ref_bodies"):
        summ[wkey] = {}
        for rk in ("trash", "champion-hero", "boss+nemesis", "all"):
            sel = [c for c in cells.values() if rk == "all" or role_of(c) == rk]
            summ[wkey][rk] = {f: wq([(c[f], c[wkey]) for c in sel]) for f in (
                "record_basic_hit", "record_max_slot", "record_basic_hit_x_crit",
                "prior_folded_basic_hit", "prior_folded_max_slot", "prior_raw_basic_hit")}
    # dynamic: per landed hit (each hit weight 1 = use-weighted by the oracle's own slot choice)
    role_by_rec = {}
    for c in cells.values():
        role_by_rec.setdefault(c["record"], role_of(c))
    dyn = {}
    for rk in ("trash", "champion-hero", "boss+nemesis", "all"):
        sel = [h for h in hits if h["raw_direct"] > 0 and (rk == "all" or role_by_rec.get(h["record"]) == rk)]
        dyn[rk] = {"per_landed_hit_raw_direct": wq([(h["raw_direct"], 1.0) for h in sel]),
                   "n_hits": len(sel),
                   "slot_mix": dict(sorted(((s, sum(1 for h in sel if h["slot"] == s)) for s in {h["slot"] for h in sel}),
                                           key=lambda kv: -kv[1]))}
    zero = sum(1 for h in hits if h["raw_direct"] == 0)
    # ratio record / prior folded per cell
    ratios = [(c["record_basic_hit"] / c["prior_folded_basic_hit"], c["weight_board_actors"]) for c in cells.values()
              if c["record_basic_hit"] and c["prior_folded_basic_hit"]]
    def _role(c):
        r = (c.get("role") or "").lower()
        return "trash" if r == "trash" else "champion-hero" if ("hero" in r or "champion" in r) else "boss+nemesis" if r in ("boss", "nemesis") else r
    eng_summ = {}
    for wkey in ("weight_board_actors", "weight_ref_bodies"):
        eng_summ[wkey] = {}
        for rk in ("trash", "champion-hero", "boss+nemesis", "all"):
            sel = [c for c in eng_cells.values() if rk == "all" or _role(c) == rk]
            eng_summ[wkey][rk] = {
                **{f"{an.split()[0]}_{f}": wq([(c[an][f], c[wkey]) for c in sel]) for an in ENG_ABL for f in ("basic", "max_slot", "mean_damaging_slot")},
                "prior_folded_basic_hit": wq([(c["prior_folded_basic_hit"], c[wkey]) for c in sel]),
                "prior_folded_max_slot": wq([(c["prior_folded_max_slot"], c[wkey]) for c in sel]),
                "prior_raw_basic_hit": wq([(c["prior_raw_basic_hit"], c[wkey]) for c in sel]),
                "bodies_with_no_oracle_slot": sum(c[wkey] for c in sel if c["n_oracle_slots"] == 0),
                "bodies_total": sum(c[wkey] for c in sel)}
    # dynamic vs engine-native static, per hit (raw_direct / (crit mult * volley)) — the reproduction check
    chk = {"n": 0, "exact": 0, "aura_granted": 0, "aura_granted_exact": 0, "no_cell": 0}
    for h in hits:
        e = engines_by_id.get(h["engine_id"])
        prof = (e.roster.get(h["record"]) or e.pets.get(h["record"])) if e is not None else None
        if prof is None or not h["multiplier"]:
            chk["no_cell"] += 1
            continue
        sv = {x["slot"]: x["per_hit"] for x in engine_slot_values(e, prof)}
        if h["slot"] not in sv:
            chk["no_cell"] += 1
            continue
        chk["n"] += 1
        ok = abs(h["raw_direct"] / h.get("volley", 1.0) - sv[h["slot"]]) <= 1e-6 * max(1.0, sv[h["slot"]])
        if h.get("aura_granted"):
            chk["aura_granted"] += 1
            chk["aura_granted_exact"] += int(ok)
        else:
            chk["exact"] += int(ok)
        h["engine_static_per_hit"] = sv[h["slot"]]
    doc = {
        "what": "C-13 KP-428 (2): GD per-hit monster damage under the oracle's configuration of record (V311-FULL)",
        "engine_head": None,
        "inputs_sha256": {"pm4o_oa_da.csv": sha(DATA / "pm4o_oa_da.csv"),
                          "kc2_referent_lineup_v3p11.csv": sha(DATA / "kc2_referent_lineup_v3p11.csv"),
                          "gd_enemy_quantities.json (prior)": sha(PKT / "gd_enemy_quantities.json")},
        "composition_report": comp_rep, "mutator_report": mut_rep,
        "static_summaries": summ,
        "static_record_over_prior_folded_basic": wq(ratios),
        "dynamic": {"salt": salt, "arm": "M0", "config": "V311-FULL", "tick_period_s": period, "wall_s": wall,
                    "n_landed_hits": len(hits), "n_landed_hits_zero_direct": zero,
                    "n_hits_with_pcl": sum(1 for h in hits if h["pcl"]),
                    "n_hits_with_dot_rows": sum(1 for h in hits if h["n_dot_rows"]),
                    "n_hits_with_leech_rows": sum(1 for h in hits if h["n_leech_rows"]),
                    "n_hits_aura_granted": sum(1 for h in hits if h.get("aura_granted")),
                    "summaries": dyn,
                    "hits_by_wave": dict(sorted(defaultdict(int, {w: sum(1 for h in hits if h["wave"] == w) for w in {h["wave"] for h in hits}}).items())),
                    "trash_basic_slot_only": wq([(h["raw_direct"], 1.0) for h in hits if h["raw_direct"] > 0 and h["slot"] == "basic"
                                                 and role_by_rec.get(h["record"]) == "trash"]),
                    "trash_crit_mult_mean": (statistics.mean(h["multiplier"] for h in hits if role_by_rec.get(h["record"]) == "trash")
                                             if any(role_by_rec.get(h["record"]) == "trash" for h in hits) else None)},
        "static_ablation_ladder_trash": abl,
        "engine_native_static_summaries": eng_summ,
        "dynamic_vs_engine_static_check": chk,
        "engines_per_wave": dict(sorted(n_eng_per_wave.items())),
        "engine_native_cells": eng_cells,
        "per_cell": cells,
        "dynamic_hits": hits,
    }
    out.write_text(json.dumps(doc, indent=1, default=str))
    st = summ["weight_board_actors"]["trash"]
    es = eng_summ["weight_board_actors"]["trash"]
    print("ENGINE E5 trash", {k: es[k] and es[k]["median"] for k in es if k.startswith("E")})
    print("CHECK", chk)
    print("STATIC trash basic", st["record_basic_hit"], "\n max", st["record_max_slot"], "\n prior folded", st["prior_folded_basic_hit"])
    print("record/prior folded ratio", doc["static_record_over_prior_folded_basic"])
    print("DYNAMIC", json.dumps(dyn["trash"]["per_landed_hit_raw_direct"]), dyn["trash"]["n_hits"], "wall", wall)


if __name__ == "__main__":
    main(Path(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 0)
