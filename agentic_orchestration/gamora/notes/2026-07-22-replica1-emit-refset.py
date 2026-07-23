#!/usr/bin/env python3
"""REPLICA-1 G2 — REFERENCE-SET EMISSION DRIVER (charter 2026-07-22-replica-1-godot-sim-window-run.md;
schema spec 2026-07-22-replica1-frame-schema-spec.md, `replica-frame/v1`). Executor: named-gamora.

WHAT THIS IS: the emission driver that produces the 40-fight `replica-frame/v1` reference set drax
(G3) renders in Godot. It REUSES the aware-fighter ablation runner's frame machinery VERBATIM (the
SAME W3' selection -> formation -> scenario -> cell-build the gate cells were configured with — so
each replica fight is configured IDENTICALLY to its ablation-gate cell), FILTERS to the 5 ref-set
kits, runs BOTH arms (BLIND_CONFIG / AWARE_CANDIDATE_CONFIG, imported verbatim) x ENCOUNTER
composition x seeds {20260722..25} = 40 fights, and attaches a ReplicaFrameSink (engine seam,
observability-only, default-off) to each single-fight run so it writes one NDJSON per fight.

REF SET (RL-1 correction (i) + RL-2):
  5 kits {d2-bowazon, poe1-kinetic-fusillade, poe1-caustic-arrow, d2-poison-javazon, poe1-frost-blades}
  x {blind, aware} x encounter x {20260722,20260723,20260724,20260725} = 40 fights.
  player_gather_primitive OFF, decision traces ON, SEQUENTIAL (Discipline #3).

DISCIPLINE:
  - Engine src pinned FIRST on sys.path (subprocess-free here; single process, sequential).
  - corpus.db READ-ONLY. No telemetry write. No seed additions.
  - Frames dir agentic_orchestration/gamora/notes/replica1-frames/ is UNTRACKED (regenerable).
  - Determinism (spec §6): the ReplicaFrameSink is a pure-read observability hook — a re-run of a
    seed reproduces the exact fight AND exact frame bytes. --dup-check emits one cell twice + diffs.

Author: named-gamora (simulation seam), 2026-07-22. Lineage: 2026-07-22-aware-fighter-ablation-runner.py
  frame machinery (reused via file-path module load — same selection/formation/scenario/cell frame).
Run:  python3 2026-07-22-replica1-emit-refset.py                 # emit all 40 + manifest
      python3 2026-07-22-replica1-emit-refset.py --smoke         # 1 kit (bowazon) x both arms x 1 seed
      python3 2026-07-22-replica1-emit-refset.py --dup-check      # emit bowazon/blind/seed0 twice -> diff
"""
import contextlib
import filecmp
import importlib.util
import io
import json
import os
import statistics
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN_ENGINE_SRC = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..",
                                               "reincarnated-engine", "src"))
ENGINE_REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "reincarnated-engine"))
W3PRIME_GATE = os.path.join(HERE, "2026-07-22-tier3-w3prime-gate.py")
OUT_DIR = os.path.join(HERE, "replica1-frames")

# RL-1 (i): gate seeds x4. RL-2 + RL-1 (i): ENCOUNTER composition only for the first emit.
SEEDS = [20260722, 20260723, 20260724, 20260725]
COMPOSITION = "encounter"

# The 5 ref-set kits (charter §2 / RL-1 (i)). Resolved to (era, side, formation) by the frame
# machinery below — NOT hardcoded; we filter the full pair set to these kit_ids.
REFSET_KITS = [
    "d2-bowazon",
    "poe1-kinetic-fusillade",
    "poe1-caustic-arrow",
    "d2-poison-javazon",
    "poe1-frost-blades",
]


def _git(*args) -> str:
    r = subprocess.run(["git", "-C", ENGINE_REPO, *args], capture_output=True, text=True)
    return r.stdout.strip()


def _build_frame_context():
    """Reconstruct the EXACT ablation-gate frame (selection -> formation -> pairs -> cell build ->
    scenarios) via the runner's own W3' machinery, then index the pairs by kit_id. Returns
    everything run_one needs. This is the ablation runner's _run_leg body, verbatim in structure."""
    sys.path.insert(0, MAIN_ENGINE_SRC)

    import reincarnated.simulation.spatial_gauntlet.spatial_engine as se
    bound = os.path.abspath(se.__file__)
    intended = os.path.abspath(os.path.join(MAIN_ENGINE_SRC, "reincarnated", "simulation",
                                            "spatial_gauntlet", "spatial_engine.py"))
    assert bound == intended, f"engine bound {bound} != intended {intended}"
    from reincarnated.simulation.spatial_gauntlet.replica_frame_emitter import ReplicaFrameSink
    from reincarnated.simulation.spatial_gauntlet.policy import (
        BLIND_CONFIG, AWARE_CANDIDATE_CONFIG)

    # ── W3' frame machinery (verbatim file-path load; same as runner) ──
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
    con = sqlite3.connect(f"file:{w3p.CORPUS_DB}?mode=ro", uri=True)   # READ-ONLY
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

    # index the pairs by kit_id (era/side/formation resolved by the frame logic)
    pair_index = {}
    for p in pairs:
        if p["red_flag"] is not None or p["formation"] is None:
            continue
        fclass = p["formation"]["common4_class"]
        if fclass in encounter_red_flags:
            continue
        pair_index[p["kit_row"]["kit_id"]] = (p, fclass)

    return {
        "se": se, "ReplicaFrameSink": ReplicaFrameSink,
        "BLIND_CONFIG": BLIND_CONFIG, "AWARE_CANDIDATE_CONFIG": AWARE_CANDIDATE_CONFIG,
        "w3p": w3p, "pair_index": pair_index, "cell_of": cell_of, "pc_cache": pc_cache,
        "encounter_scenarios": encounter_scenarios, "engine_bound": bound,
    }


def _emit_one_fight(ctx, kit_id, arm, seed, out_path, engine_hash):
    """Run ONE fight (n_fights=1) with a ReplicaFrameSink writing to out_path. SEQUENTIAL, single
    process. Returns (fight_result, file_stats)."""
    se = ctx["se"]
    w3p = ctx["w3p"]
    p, fclass = ctx["pair_index"][kit_id]
    cid = ctx["cell_of"][kit_id]
    pc, cd = ctx["pc_cache"][cid]
    scen = ctx["encounter_scenarios"][fclass]
    arm_config = ctx["BLIND_CONFIG"] if arm == "blind" else ctx["AWARE_CANDIDATE_CONFIG"]

    tiers = [sp.threat_tier for sp in scen.mob_spawns]
    mobs = w3p.build_neutral_mob_dicts(tiers)
    era, side = p["era"], p["side"]
    cell_slot = f"{era}|{side}|{kit_id}"
    fight_key = f"{kit_id}__{arm}__{COMPOSITION}__seed{seed}"

    with open(out_path, "w") as fh:
        sink = ctx["ReplicaFrameSink"](
            fh, fight_key=fight_key, kit_id=kit_id, cell=cell_slot, composition=COMPOSITION,
            policy_arm=arm, seed=seed, engine_git_hash=engine_hash, formation_class=fclass)
        raw = se.run_spatial_fight(
            scenario=scen, class_dict=cd, mob_dicts=mobs, n_fights=1,
            session_id=f"replica1_{arm}_{kit_id}_{side}",
            base_seed=seed, season_id="replica1", player_class=pc,
            damage_modifier=w3p.DAMAGE_MODIFIER,
            track_proxy_population=False,        # player_gather_primitive OFF
            apply_mob_hp_difficulty_multiplier=False,
            trace_decisions=True,                # decision traces ON (aim-line overlay)
            policy_config=arm_config,
            frame_sink=sink,                     # REPLICA-1 G2: the per-fight observability sink
        )
    fr = raw["fight_results"][0]
    st = os.stat(out_path)
    # tally record types for the report
    n_tick = n_dmg = n_death = n_tg = n_decision = 0
    with open(out_path) as fh:
        for line in fh:
            rec = json.loads(line)
            rt = rec.get("record_type")
            if rt == "tick":
                n_tick += 1
            elif rt == "event":
                ev = rec.get("event")
                if ev == "damage":
                    n_dmg += 1
                elif ev == "death":
                    n_death += 1
                elif ev == "telegraph":
                    n_tg += 1
                elif ev == "decision":
                    n_decision += 1
    return fr, {
        "file": os.path.basename(out_path), "bytes": st.st_size,
        "ticks": n_tick, "damage_events": n_dmg, "death_events": n_death,
        "telegraph_events": n_tg, "decision_events": n_decision,
        "winner": fr.winner, "mobs_killed": int(fr.mobs_killed),
        "total_mob_count": int(fr.total_mob_count),
        "player_damage_taken": float(fr.player_damage_taken), "elapsed_s": float(fr.elapsed_s),
    }


def main():
    smoke = ("--smoke" in sys.argv)
    dup_check = ("--dup-check" in sys.argv)

    head_short = _git("rev-parse", "--short", "HEAD")
    head_full = _git("rev-parse", "HEAD")
    print("=" * 90)
    print(f"[REPLICA-1 G2 emit] engine HEAD={head_short} ({head_full})")
    print("=" * 90)

    ctx = _build_frame_context()
    # verify all 5 ref-set kits resolved in the frame
    missing = [k for k in REFSET_KITS if k not in ctx["pair_index"]]
    if missing:
        raise SystemExit(f"FATAL: ref-set kits not in frame index: {missing}")
    for k in REFSET_KITS:
        p, fclass = ctx["pair_index"][k]
        print(f"  ref-set kit {k:28s} -> {p['era']}|{p['side']} formation={fclass} "
              f"cell={ctx['cell_of'][k]}")

    os.makedirs(OUT_DIR, exist_ok=True)

    if dup_check:
        # Determinism gate (spec §6): emit bowazon/blind/seed0 TWICE -> byte-identical diff.
        a = os.path.join(OUT_DIR, "replica-d2-bowazon__blind__encounter__seed20260722.ndjson")
        b = os.path.join(OUT_DIR, "_dupcheck__d2-bowazon__blind__seed20260722.ndjson")
        _emit_one_fight(ctx, "d2-bowazon", "blind", 20260722, a, head_full)
        _emit_one_fight(ctx, "d2-bowazon", "blind", 20260722, b, head_full)
        identical = filecmp.cmp(a, b, shallow=False)
        print(f"\n[DETERMINISM] byte-identical(re-emit d2-bowazon/blind/seed20260722): {identical}")
        print(f"  A={os.path.basename(a)}  B={os.path.basename(b)}")
        if identical:
            os.remove(b)   # keep the canonical A; drop the scratch B
        return 0 if identical else 1

    kits = ["d2-bowazon"] if smoke else REFSET_KITS
    arms = ["blind", "aware"]
    seeds = [SEEDS[0]] if smoke else SEEDS

    all_stats = []
    grid = []
    for kit_id in kits:                       # SEQUENTIAL (Discipline #3)
        for arm in arms:
            for seed in seeds:
                fname = f"replica-{kit_id}__{arm}__{COMPOSITION}__seed{seed}.ndjson"
                out_path = os.path.join(OUT_DIR, fname)
                fr, st = _emit_one_fight(ctx, kit_id, arm, seed, out_path, head_full)
                all_stats.append(st)
                grid.append({"kit_id": kit_id, "arm": arm, "composition": COMPOSITION, "seed": seed,
                             "file": fname})
                print(f"[emit] {fname:62s} {st['bytes']:>9d}B  ticks={st['ticks']:>4d} "
                      f"dmg={st['damage_events']:>5d} death={st['death_events']:>3d} "
                      f"tg={st['telegraph_events']:>3d} dec={st['decision_events']:>4d} "
                      f"winner={st['winner']} killed={st['mobs_killed']}/{st['total_mob_count']}")

    manifest = {
        "artifact": "replica1-frames-manifest",
        "schema_version": "replica-frame/v1",
        "engine_git_hash": head_full,
        "engine_git_hash_short": head_short,
        "author": "named-gamora", "date": "2026-07-22",
        "charter": "2026-07-22-replica-1-godot-sim-window-run.md",
        "spec": "2026-07-22-replica1-frame-schema-spec.md",
        "composition": COMPOSITION, "seeds": SEEDS, "kits": REFSET_KITS, "arms": arms,
        "n_fights": len(grid),
        "grid": grid,
        "note": "REGENERABLE from the frozen engine + seed (Discipline #3). Directory UNTRACKED.",
    }
    if not smoke:
        with open(os.path.join(OUT_DIR, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)

    total_bytes = sum(s["bytes"] for s in all_stats)
    print("\n" + "=" * 90)
    print(f"[EMIT COMPLETE] {len(all_stats)} fights -> {OUT_DIR}")
    print(f"  total {total_bytes/1e6:.2f} MB  (mean {total_bytes/len(all_stats)/1024:.1f} KB/fight)")
    print(f"  ticks: min={min(s['ticks'] for s in all_stats)} "
          f"max={max(s['ticks'] for s in all_stats)}")
    print(f"  damage events: min={min(s['damage_events'] for s in all_stats)} "
          f"max={max(s['damage_events'] for s in all_stats)} "
          f"total={sum(s['damage_events'] for s in all_stats)}")
    print(f"  death events: total={sum(s['death_events'] for s in all_stats)}")
    print("=" * 90)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
