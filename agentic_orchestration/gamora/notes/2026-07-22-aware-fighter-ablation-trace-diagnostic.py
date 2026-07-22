#!/usr/bin/env python3
"""AWARE-FIGHTER ABLATION — TRACE DIAGNOSTIC (mechanism diagnosis, NOT re-scoring).

Under gandalf RUN-CONDUCTOR authority. The sealed ablation gate (commit 116aa896, engine FROZEN at
2f43045) tripped its clear-guard (14 mismatches) → verdict state is the conductor's. This script
does NOT touch the verdict. It DIAGNOSTICALLY RE-OBSERVES the deterministic engine to explain the
MECHANISM behind the guard trip, per the trace-investigation work order.

WHY A RE-RUN: the on-disk full-run JSONs (…-blind-full.json / …-aware-full.json) are SUMMARY-ONLY —
they carry `trace_len` (a COUNT) but NOT the decision-trace BODIES, and no per-tick HP. The engine's
run_spatial_fight() PRODUCES the (tick, chosen_target_id, intent) trace when trace_decisions=True; it
just isn't dumped. To answer 2a–2d we need the bodies + richer per-decision reads (chosen-target
DISTANCE, chosen-target HP, alive-mob-HP snapshot). We obtain them by RE-RUNNING the specific
diagnostic cells with a READ-ONLY instrument.

INSTRUMENT DISCIPLINE (zero engine edits — Discipline #11, RC-1 spirit):
  - The engine `src/reincarnated/**/*.py` tree is UNTOUCHED (HEAD stays 2f43045; zero *.py diff).
  - Instrumentation is a MONKEYPATCH applied from THIS collab-notes file at runtime: it wraps the
    engine's `_get_player_primary_target` with a PURE-READ recorder (no RNG, no HP/pos mutation — it
    calls the real selector, then records position/HP READS of the returned target + the alive set).
    The wrapped function returns EXACTLY what the real one returns, so fight trajectories are
    byte-identical to the gate (the recorder is side-effect-free w.r.t. engine state).
  - Frame logic (selection → formation → scenario → cell build) is REUSED VERBATIM from the gate
    runner via file-path module load — same W3' machinery, same seeds, same configs.
  - SEQUENTIAL fights only (Discipline #3). corpus.db READ-ONLY.

Run:  python3 2026-07-22-aware-fighter-ablation-trace-diagnostic.py
Out:  2026-07-22-aware-fighter-ablation-trace-dump.json  (untracked; regenerable)
Author: named-gamora (simulation seam), 2026-07-22.
"""
import contextlib
import importlib.util
import io
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN_ENGINE_SRC = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..",
                                               "reincarnated-engine", "src"))
ENGINE_REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "reincarnated-engine"))
FROZEN_HEAD = "2f43045"
W3PRIME_GATE = os.path.join(HERE, "2026-07-22-tier3-w3prime-gate.py")
RUNNER = os.path.join(HERE, "2026-07-22-aware-fighter-ablation-runner.py")
OUT = os.path.join(HERE, "2026-07-22-aware-fighter-ablation-trace-dump.json")

SEEDS = [20260722, 20260723, 20260724, 20260725]

# Diagnostic cell set (cell-slot without seed). Chosen per the work order:
#   ranged-direct FAIL-all-4 · ranged-DoT aware-cleared-MORE · melee-volley big-delta-no-trip ·
#   clean controls (0 or near-0 delta, both arms cleared).
DIAG_CELLS = [
    # (era, side, kit_id) — resolved to formation by the frame logic below.
    ("IV", "high", "poe1-kinetic-fusillade"),   # ranged-direct volley, FAIL all 4 (repr of its class)
    ("I", "high", "d2-bowazon"),                # ranged-direct volley, FAIL all 4 (bit-twin of above)
    ("II", "high", "poe1-caustic-arrow"),       # ranged DoT-ailment, aware-cleared-MORE (seed 23)
    ("I", "high", "d2-poison-javazon"),         # ranged DoT-ailment, aware-cleared-MORE (bit-twin)
    ("I", "low", "poe1-frost-blades"),          # melee volley, big -2677 delta, NO guard trip
    ("III", "high", "gd-primal-strike-vindicator"),  # clean control, delta 0.00 (melee emplacement)
    ("I", "high", "d2-frenzy-barb"),            # clean control, delta 0.00 (melee emplacement)
    ("II", "high", "poe1-armageddon-brand"),    # clean control, small +34 (ranged emplacement)
    ("II", "high", "poe1-spark"),               # ranged volley, -1210 delta, NO guard trip (contrast)
]
COMPOSITIONS = ["encounter", "matched_baseline"]


def _git(*args):
    import subprocess
    r = subprocess.run(["git", "-C", ENGINE_REPO, *args], capture_output=True, text=True)
    return r.stdout.strip()


def _attest(beat):
    head = _git("rev-parse", "--short", "HEAD")
    py_diff = [l for l in _git("diff", "--name-only", "HEAD", "--",
                               "src/reincarnated/**/*.py").splitlines() if l.strip()]
    if head != FROZEN_HEAD:
        raise SystemExit(f"HALT[{beat}]: HEAD {head} != frozen {FROZEN_HEAD}")
    if py_diff:
        raise SystemExit(f"HALT[{beat}]: tracked *.py delta under src/reincarnated/: {py_diff}")
    print(f"[attest {beat}] HEAD={head} (frozen OK)  py_diff_empty={len(py_diff)==0}")
    return {"beat": beat, "head_short": head, "py_diff": py_diff, "py_diff_empty": len(py_diff) == 0}


def main():
    att_start = _attest("run_start")
    sys.path.insert(0, MAIN_ENGINE_SRC)

    import reincarnated.simulation.spatial_gauntlet.spatial_engine as se
    bound = os.path.abspath(se.__file__)
    intended = os.path.abspath(os.path.join(MAIN_ENGINE_SRC, "reincarnated", "simulation",
                                            "spatial_gauntlet", "spatial_engine.py"))
    assert bound == intended, f"engine bound {bound} != intended {intended}"

    from reincarnated.simulation.spatial_gauntlet.policy import (
        BLIND_CONFIG, AWARE_CANDIDATE_CONFIG)

    # ── load the W3' frame machinery (verbatim, file-path load — same as the runner) ──
    spec = importlib.util.spec_from_file_location("w3p_gate", W3PRIME_GATE)
    w3p = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(w3p)
        full_rows = w3p.load_full_fit_rows()

    selection = {}
    for era in w3p.ERAS:
        cands = [r for r in full_rows if r["era"] == era]
        deck_median = statistics.median([c["fit_score"] for c in cands])
        high = w3p.round_robin_draft(cands, "high")
        low = w3p.round_robin_draft(cands, "low")
        high, low, _ = w3p.courts_swap(high, low, cands, cands, deck_median)
        selection[era] = {"high": high, "low": low}
    pairs = []
    for era in w3p.ERAS:
        for side in ("high", "low"):
            for kit_row in selection[era][side]:
                chosen, subs, rf = w3p.assign_formation(kit_row, side)
                pairs.append({"era": era, "side": side, "kit_row": kit_row,
                              "formation": chosen, "red_flag": rf})

    import sqlite3
    cells = w3p._neutral_cells()
    con = sqlite3.connect(f"file:{w3p.CORPUS_DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    sc = json.load(open(w3p.SIDECAR))
    active_ids = {r["kit_id"] for r in sc["memberships"]
                  if not r.get("shadowed_by") and r.get("on_spine")}
    all_kits = []
    for row in con.execute("SELECT kit_id, attr_val, range_val, tempo_val, amp_val "
                           "FROM canon_corpus WHERE corpus_class='record' ORDER BY kit_id"):
        if row["kit_id"] in active_ids:
            all_kits.append(dict(row))
    con.close()
    cell_of = {k["kit_id"]: w3p.nearest_cell(k, cells)[0] for k in all_kits}
    all_used_cells = sorted(set(cell_of.values()))
    from reincarnated.generation.resource_economy import DEFAULT_RESOURCE_ECONOMY
    pc_cache = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for idx, cid in enumerate(all_used_cells):
            pc, _ = w3p._build_martial_player_class(cid, idx, "balanced")
            cd = pc.model_dump()
            cd["resource_economy"] = dict(DEFAULT_RESOURCE_ECONOMY)
            pc_cache[cid] = (pc, cd)

    encounter_scenarios, encounter_tiers, encounter_red_flags = {}, {}, {}
    for fclass in ("swarm", "volley-fan", "lane", "emplacement"):
        scen, erf = w3p.make_encounter_scenario(fclass)
        encounter_scenarios[fclass] = scen
        if erf:
            encounter_red_flags[fclass] = erf
        else:
            encounter_tiers[fclass] = [sp.threat_tier for sp in scen.mob_spawns]
    baseline_scenarios, baseline_red_flags = {}, {}
    for fclass in ("swarm", "volley-fan", "lane", "emplacement"):
        if fclass in encounter_red_flags:
            continue
        bscen, brf = w3p.make_matched_baseline_scenario(fclass, encounter_tiers[fclass])
        baseline_scenarios[fclass] = bscen
        if brf:
            baseline_red_flags[fclass] = brf

    # index the pairs by (era, side, kit_id) so we can pull the exact diagnostic cells
    pair_index = {}
    for p in pairs:
        if p["red_flag"] is not None or p["formation"] is None:
            continue
        fclass = p["formation"]["common4_class"]
        if fclass in encounter_red_flags or fclass in baseline_red_flags:
            continue
        pair_index[(p["era"], p["side"], p["kit_row"]["kit_id"])] = (p, fclass)

    # ── READ-ONLY instrument: capture per-DECISION rich reads without perturbing the fight ──
    # The engine calls se._get_player_primary_target(player, alive_mobs, boss_focus, policy_config=…)
    # once per player decision tick. We wrap it: call the REAL selector, then RECORD read-only state
    # (chosen entity_id + distance + hp; alive-set size + HP list; per-mob HP snapshot). The return
    # value is IDENTICAL to the real selector → fight trajectory byte-identical to the gate.
    _real_select = se._get_player_primary_target
    _cap = {"decisions": []}  # filled per fight; reset by run_one

    def _instrumented_select(player, alive_mobs, boss_focus_entity, policy_config=None):
        chosen = _real_select(player, alive_mobs, boss_focus_entity, policy_config=policy_config)
        # pure reads only
        try:
            chosen_d = player.distance_to(chosen) if chosen is not None else None
            chosen_hp = float(getattr(chosen, "hp")) if chosen is not None else None
            chosen_maxhp = float(getattr(chosen, "max_hp")) if chosen is not None else None
            chosen_id = getattr(chosen, "entity_id", None)
            alive_hps = [float(getattr(m, "hp")) for m in alive_mobs]
            alive_maxhps = [float(getattr(m, "max_hp")) for m in alive_mobs]
            alive_ids = [getattr(m, "entity_id", None) for m in alive_mobs]
            alive_dists = [player.distance_to(m) for m in alive_mobs]
        except Exception as e:  # never let the recorder perturb the run
            _cap["decisions"].append({"record_error": repr(e)})
            return chosen
        _cap["decisions"].append({
            "chosen_id": chosen_id,
            "chosen_distance": chosen_d,
            "chosen_hp": chosen_hp,
            "chosen_maxhp": chosen_maxhp,
            "n_alive": len(alive_mobs),
            # nearest-alive distance (what BLIND would pick) for switch/commit contrast
            "nearest_alive_distance": min(alive_dists) if alive_dists else None,
            "alive_hp_snapshot": alive_hps,          # HP of each alive mob at this decision
            "alive_maxhp_snapshot": alive_maxhps,
            "alive_id_snapshot": alive_ids,
        })
        return chosen

    def run_one(scen, cd, pc, seed, sid, arm_config):
        _cap["decisions"] = []
        tiers = [sp.threat_tier for sp in scen.mob_spawns]
        mobs = w3p.build_neutral_mob_dicts(tiers)
        se._get_player_primary_target = _instrumented_select
        try:
            raw = se.run_spatial_fight(
                scenario=scen, class_dict=cd, mob_dicts=mobs, n_fights=1, session_id=sid,
                base_seed=seed, season_id="aware-ablation-diag", player_class=pc,
                damage_modifier=w3p.DAMAGE_MODIFIER,
                track_proxy_population=False,
                apply_mob_hp_difficulty_multiplier=False,
                trace_decisions=True,
                policy_config=arm_config,
            )
        finally:
            se._get_player_primary_target = _real_select
        fr = raw["fight_results"][0]
        engine_trace = raw["decision_traces"][0]  # (tick, chosen_id, intent) from the engine itself
        total_mob = int(getattr(fr, "total_mob_count"))
        killed = int(getattr(fr, "mobs_killed"))
        decisions = list(_cap["decisions"])
        return {
            "player_damage_taken": float(getattr(fr, "player_damage_taken")),
            "elapsed_s": float(getattr(fr, "elapsed_s")),
            "all_mobs_killed": bool(total_mob > 0 and killed == total_mob),
            "winner": getattr(fr, "winner"),
            "mobs_killed": killed,
            "total_mob_count": total_mob,
            "trace_len_engine": len(engine_trace),
            "engine_trace": engine_trace,           # [(tick, chosen_id, intent), ...]
            "n_decisions_recorded": len(decisions),
            "decisions": decisions,                 # rich per-decision reads (chosen dist/hp, alive HP)
        }

    # ── run the diagnostic cells (SEQUENTIAL) ──
    dump = {"engine_src": MAIN_ENGINE_SRC, "engine_bound": bound, "frozen_head": FROZEN_HEAD,
            "attest_run_start": att_start, "seeds": SEEDS, "cells": {}}
    for (era, side, kid) in DIAG_CELLS:
        key = (era, side, kid)
        if key not in pair_index:
            print(f"[WARN] cell {era}|{side}|{kid} not in frame index — SKIP")
            continue
        p, fclass = pair_index[key]
        cid = cell_of.get(kid)
        pc, cd = pc_cache[cid]
        cell_range = cid.split("_")[2] if "_bc_" in cid else "?"
        kr = p["kit_row"]
        cellslot = f"{era}|{side}|{kid}"
        dump["cells"][cellslot] = {
            "formation_class": fclass, "cell_id": cid, "cell_range": cell_range,
            "kit_range_val": kr.get("range_val"), "element": kr.get("element"),
            "draft_family": kr.get("draft_family"), "arms": {}}
        for arm, cfg in (("blind", BLIND_CONFIG), ("aware", AWARE_CANDIDATE_CONFIG)):
            dump["cells"][cellslot]["arms"][arm] = {}
            for comp, scen in (("encounter", encounter_scenarios[fclass]),
                               ("matched_baseline", baseline_scenarios[fclass])):
                for seed in SEEDS:
                    rec = run_one(scen, cd, pc, seed, f"diag_{arm}_{kid}_{side}", cfg)
                    dump["cells"][cellslot]["arms"][arm][f"{comp}|{seed}"] = rec
        print(f"[done] {cellslot}  fclass={fclass} range={cell_range} family={kr.get('draft_family')}")

    att_end = _attest("run_end")
    dump["attest_run_end"] = att_end
    with open(OUT, "w") as f:
        json.dump(dump, f)
    print(f"\n[trace-dump] wrote {len(dump['cells'])} diagnostic cells -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
