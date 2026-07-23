#!/usr/bin/env python3
"""KF-7 RE-EMISSION DRIVER — COMPILED pilot-5 reference set with LIVE fidelity gauge.

Run: KIT-FIDELITY · Gate KF-7 · ledger KFL-19b · conductor gandalf · 2026-07-23. Executor: named-gamora.

WHAT THIS IS + WHY IT EXISTS (read the report §"Load-bearing pre-flight finding" first):
  The on-disk `replica1-frames/` set was emitted at engine hash 2f43045 — which PREDATES the KF-5 gauge
  fields — and its fighters are procedurally-generated W3'-gate MARTIAL classes (d2-bowazon, …) that carry
  NO `_composition` block and therefore CANNOT light the KF-5 gauge. The KF-7 exit predicate (player-DEALT
  hits with median pct ≈ 100), the charter payload ("compositions attached via attach_composition_blocks,
  gauge fields live"), and drax's KF-6 scene (binds by kit_ref to the COMPILED pilot-5) are all coherent
  ONLY when the re-emitted fighters are the KF-4 COMPILED KITS. So "same fights/arms/seeds as on-disk" =
  the same GRID SHAPE (blind/aware × encounter × 4 seeds); the PAYLOAD is the compiled pilot-5, replacing
  the stale pre-gauge martial-pilot frames in place. (drax scene comment replica_playback.gd:43-52
  documents this exact hand-off: "the COMPILED-kit frames arrive with the parent run's KF-5/KF-6 … the
  by-kit path lights up and the bridge default falls away with no scene change.")

MACHINERY (all PROVEN, reused verbatim):
  * fighter  = compile_kit(pilot) → attach_composition_blocks(class_dict, ck)   [the KF-5 smoke pattern
    that lights the DEALT-side gauge; math note §4 + §10]. PROJECTION path (player_class=None), the KF-4
    compiler target.
  * encounter = the SAME W3' make_encounter_scenario(fclass) + build_neutral_mob_dicts(tiers) the on-disk
    frames used (40-parity neutral arena). Mobs carry skills (mob→player hits land) but NO _composition →
    pct_received stays honestly NULL (charter Task 6; KF-3 mob-harvest is next-lap, do NOT fake it).
  * arm     = policy_config BLIND_CONFIG / AWARE_CANDIDATE_CONFIG (imported verbatim), exactly as the
    on-disk driver mapped blind/aware.
  * sink    = ReplicaFrameSink(kit_id=<compiled pilot id>) → header kit_ref = the compiled pilot id →
    drax PILOT_RIGS binds. Observability-only, default-off elsewhere.

DISCIPLINE:
  * Engine src pinned FIRST on sys.path. corpus.db READ-ONLY. NO telemetry write. NO seed additions
    (seeds are the on-disk 20260722..25 verbatim). SEQUENTIAL (Discipline #3 — no parallel same-seed).
  * Determinism (spec §6): the sink is a pure-read observability hook — a re-run reproduces exact fight +
    exact frame bytes. --dup-check emits one cell twice + diffs.
  * Frames dir replica1-frames/ is UNTRACKED-by-default in the engine repo but LIVES IN COLLAB and IS the
    dir drax's scene reads (FRAMES_DIR_DEFAULT absolute path). We REPLACE the martial-pilot files with the
    compiled-pilot files (data swap in place); the manifest records the roster switch + engine hash.

Author: named-gamora (simulation seam), 2026-07-23. Lineage: 2026-07-22-replica1-emit-refset.py (grid +
  arms + manifest + dup-check structure) × smoke_kf5_expected_pct._emit_frames (compiled-kit gauge path).
Run:  python3 2026-07-23-kf7-emit-compiled-refset.py            # emit all 40 (5 compiled kits × 2 arms × 4 seeds) + manifest
      python3 2026-07-23-kf7-emit-compiled-refset.py --smoke    # 1 kit (poe2-bonestorm) × both arms × 1 seed
      python3 2026-07-23-kf7-emit-compiled-refset.py --dup-check # emit bonestorm/blind/seed0 twice → byte-diff
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

# on-disk seeds (verbatim; NO seed additions). COMPOSITION label preserved for filename/scene parity.
SEEDS = [20260722, 20260723, 20260724, 20260725]
COMPOSITION = "encounter"

# The 5 COMPILED pilot kits (KF-1 roster after the LE→d2-fire-sorc swap, KFL-4). gd-flames is HELD
# (GAP base) → its DEALT gauge is honestly null (charter accepts the 1 GAP). The other 4 light the gauge.
REFSET_KITS = [
    "d2-firewall-sorc",
    "d2-fire-sorc",
    "gd-flames-of-ignaffar-purifier",
    "poe2-bonestorm",
    "poe1-cyclone",
]

# Deterministic formation per pilot (each kit always dresses the SAME encounter → stable visuals +
# reproducible dynamics). The 4 W3' formation classes cycled by roster order; a fixed map, not a hash.
_FORMATION_OF = {
    "d2-firewall-sorc": "swarm",
    "d2-fire-sorc": "volley-fan",
    "gd-flames-of-ignaffar-purifier": "lane",
    "poe2-bonestorm": "emplacement",
    "poe1-cyclone": "swarm",
}


def _git(*args) -> str:
    r = subprocess.run(["git", "-C", ENGINE_REPO, *args], capture_output=True, text=True)
    return r.stdout.strip()


def _build_ctx():
    """Load the engine + W3' encounter machinery + policy configs; compile the pilot-5 kits and attach
    their _composition blocks (the DEALT-gauge bridge). Returns everything _emit_one_fight needs."""
    sys.path.insert(0, MAIN_ENGINE_SRC)

    import reincarnated.simulation.spatial_gauntlet.spatial_engine as se
    bound = os.path.abspath(se.__file__)
    intended = os.path.abspath(os.path.join(MAIN_ENGINE_SRC, "reincarnated", "simulation",
                                            "spatial_gauntlet", "spatial_engine.py"))
    assert bound == intended, f"engine bound {bound} != intended {intended}"

    from reincarnated.simulation.spatial_gauntlet.replica_frame_emitter import ReplicaFrameSink
    from reincarnated.simulation.spatial_gauntlet.policy import BLIND_CONFIG, AWARE_CANDIDATE_CONFIG
    from reincarnated.simulation.spatial_gauntlet.kf5_expected import attach_composition_blocks
    from reincarnated.simulation.kit_compiler.kit_compiler import compile_kit
    from reincarnated.simulation.kit_compiler.kit_reader import CorpusKitReader

    # W3' encounter machinery (verbatim file-path load; SAME as the on-disk driver)
    spec = importlib.util.spec_from_file_location("w3p_gate", W3PRIME_GATE)
    w3p = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(w3p)

    # pre-build the encounter scenarios (one per formation class we use), fail-loud on any red flag
    encounter_scenarios = {}
    for fclass in sorted(set(_FORMATION_OF.values())):
        scen, rf = w3p.make_encounter_scenario(fclass)
        if rf:
            raise SystemExit(f"FATAL: encounter builder {fclass} red-flagged: {rf}")
        encounter_scenarios[fclass] = scen

    # compile + gauge-bridge each pilot ONCE (reused across arms/seeds — the compile is seed-independent)
    reader = CorpusKitReader()
    compiled = {}
    for kid in REFSET_KITS:
        ck = compile_kit(kid, reader=reader)
        attach_composition_blocks(ck.class_dict, ck)
        # sanity: which skills carry a live base (dealt gauge will be non-null there)
        anchored = [cs.skill_dict.get("name") for cs in ck.skills if (cs.composition or {}).get("base_max") is not None]
        compiled[kid] = {"ck": ck, "anchored_skills": anchored}

    return {
        "se": se, "w3p": w3p, "ReplicaFrameSink": ReplicaFrameSink,
        "BLIND_CONFIG": BLIND_CONFIG, "AWARE_CANDIDATE_CONFIG": AWARE_CANDIDATE_CONFIG,
        "encounter_scenarios": encounter_scenarios, "compiled": compiled, "engine_bound": bound,
    }


def _emit_one_fight(ctx, kit_id, arm, seed, out_path, engine_hash):
    """Run ONE compiled-kit encounter fight (n_fights=1) with a ReplicaFrameSink writing out_path.
    PROJECTION path (player_class=None). SEQUENTIAL. Returns (fight_result, file_stats)."""
    se = ctx["se"]
    w3p = ctx["w3p"]
    fclass = _FORMATION_OF[kit_id]
    scen = ctx["encounter_scenarios"][fclass]
    ck = ctx["compiled"][kit_id]["ck"]
    arm_config = ctx["BLIND_CONFIG"] if arm == "blind" else ctx["AWARE_CANDIDATE_CONFIG"]

    tiers = [sp.threat_tier for sp in scen.mob_spawns]
    mobs = w3p.build_neutral_mob_dicts(tiers)
    cell_slot = f"kf7|{fclass}|{kit_id}"
    fight_key = f"{kit_id}__{arm}__{COMPOSITION}__seed{seed}"

    with open(out_path, "w") as fh:
        sink = ctx["ReplicaFrameSink"](
            fh, fight_key=fight_key, kit_id=kit_id, cell=cell_slot, composition=COMPOSITION,
            policy_arm=arm, seed=seed, engine_git_hash=engine_hash, formation_class=fclass)
        raw = se.run_spatial_fight(
            scenario=scen, class_dict=ck.class_dict, mob_dicts=mobs, n_fights=1,
            session_id=f"kf7_{arm}_{kit_id}",
            base_seed=seed, season_id="kf7-reemission", player_class=None,   # PROJECTION (compiler target)
            damage_modifier=w3p.DAMAGE_MODIFIER,
            track_proxy_population=False,        # player_gather_primitive OFF (parity with on-disk)
            apply_mob_hp_difficulty_multiplier=False,
            trace_decisions=True,                # decision traces ON (aim-line overlay)
            policy_config=arm_config,
            frame_sink=sink,
        )
    fr = raw["fight_results"][0]
    st = os.stat(out_path)
    # tally record types + gauge stats for the report (python-side validation, Task 6)
    n_tick = n_dmg = n_death = n_tg = n_decision = 0
    dealt_pcts = []
    dealt_amounts = []
    recv_nonnull = 0
    recv_total = 0
    tick_hp_ok = True
    with open(out_path) as fh:
        for line in fh:
            rec = json.loads(line)
            rt = rec.get("record_type")
            if rt == "tick":
                n_tick += 1
                for e in rec.get("entities", []):
                    if "hp" not in e:
                        tick_hp_ok = False
            elif rt == "event":
                ev = rec.get("event")
                if ev == "damage":
                    n_dmg += 1
                    is_player_src = (rec.get("source_id") == kit_id)
                    if is_player_src and rec.get("geometry") != "dot":
                        dealt_amounts.append(rec.get("amount"))
                        if rec.get("pct") is not None:
                            dealt_pcts.append(rec.get("pct"))
                    elif not is_player_src and rec.get("geometry") != "dot":
                        recv_total += 1
                        if rec.get("pct_received") is not None:
                            recv_nonnull += 1
                elif ev == "death":
                    n_death += 1
                elif ev == "telegraph":
                    n_tg += 1
                elif ev == "decision":
                    n_decision += 1
    pct_med = statistics.median(dealt_pcts) if dealt_pcts else None
    return fr, {
        "file": os.path.basename(out_path), "bytes": st.st_size,
        "ticks": n_tick, "damage_events": n_dmg, "death_events": n_death,
        "telegraph_events": n_tg, "decision_events": n_decision,
        "winner": fr.winner, "mobs_killed": int(fr.mobs_killed),
        "total_mob_count": int(fr.total_mob_count),
        "player_damage_taken": float(fr.player_damage_taken), "elapsed_s": float(fr.elapsed_s),
        "dealt_hits": len(dealt_amounts), "dealt_pct_n": len(dealt_pcts),
        "dealt_pct_median": pct_med,
        "dealt_pct_min": (min(dealt_pcts) if dealt_pcts else None),
        "dealt_pct_max": (max(dealt_pcts) if dealt_pcts else None),
        "dealt_amount_min": (min(dealt_amounts) if dealt_amounts else None),
        "dealt_amount_max": (max(dealt_amounts) if dealt_amounts else None),
        "dealt_amount_all_pos": (all(a is not None and a > 0 for a in dealt_amounts) if dealt_amounts else None),
        "recv_hits": recv_total, "recv_pct_nonnull": recv_nonnull,
        "tick_hp_present": tick_hp_ok,
    }


def main():
    smoke = ("--smoke" in sys.argv)
    dup_check = ("--dup-check" in sys.argv)

    head_short = _git("rev-parse", "--short", "HEAD")
    head_full = _git("rev-parse", "HEAD")
    print("=" * 96)
    print(f"[KF-7 RE-EMIT compiled] engine HEAD={head_short} ({head_full})")
    print("=" * 96)

    ctx = _build_ctx()
    for k in REFSET_KITS:
        info = ctx["compiled"][k]
        print(f"  compiled {k:34s} formation={_FORMATION_OF[k]:12s} anchored_skills={info['anchored_skills']}")

    os.makedirs(OUT_DIR, exist_ok=True)

    if dup_check:
        a = os.path.join(OUT_DIR, "replica-poe2-bonestorm__blind__encounter__seed20260722.ndjson")
        b = os.path.join(OUT_DIR, "_dupcheck__poe2-bonestorm__blind__seed20260722.ndjson")
        _emit_one_fight(ctx, "poe2-bonestorm", "blind", 20260722, a, head_full)
        _emit_one_fight(ctx, "poe2-bonestorm", "blind", 20260722, b, head_full)
        identical = filecmp.cmp(a, b, shallow=False)
        print(f"\n[DETERMINISM] byte-identical(re-emit poe2-bonestorm/blind/seed20260722): {identical}")
        if identical:
            os.remove(b)
        return 0 if identical else 1

    kits = ["poe2-bonestorm"] if smoke else REFSET_KITS
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
                             "file": fname, "formation_class": _FORMATION_OF[kit_id]})
                medstr = f"{st['dealt_pct_median']:.2f}" if st['dealt_pct_median'] is not None else "null"
                print(f"[emit] {fname:64s} {st['bytes']:>9d}B ticks={st['ticks']:>4d} "
                      f"dmg={st['damage_events']:>5d} dealt={st['dealt_hits']:>4d} "
                      f"pct_med={medstr:>7s} killed={st['mobs_killed']}/{st['total_mob_count']}")

    if not smoke:
        manifest = {
            "artifact": "replica1-frames-manifest",
            "schema_version": "replica-frame/v1",
            "engine_git_hash": head_full,
            "engine_git_hash_short": head_short,
            "author": "named-gamora", "date": "2026-07-23",
            "charter": "2026-07-23-kit-fidelity-run-charter.md (KF-7 re-emission, KFL-19b)",
            "spec": "2026-07-22-replica1-frame-schema-spec.md",
            "roster_note": ("KF-7 COMPILED pilot-5 (replaces the pre-KF-5 martial-pilot ref roster). "
                            "kit_ref = compiled pilot id → drax PILOT_RIGS by-kit bind. DEALT gauge live "
                            "(base_mean shape, Matt-ratified KFL-19); gd-flames GAP base → dealt gauge "
                            "null (HELD, T4); pct_received null (mob _composition next-lap, KF-3)."),
            "composition": COMPOSITION, "seeds": SEEDS, "kits": REFSET_KITS, "arms": arms,
            "formation_of": _FORMATION_OF,
            "n_fights": len(grid),
            "grid": grid,
            "note": "REGENERABLE from the frozen engine + seed (Discipline #3). Directory UNTRACKED.",
        }
        with open(os.path.join(OUT_DIR, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)

    total_bytes = sum(s["bytes"] for s in all_stats)
    print("\n" + "=" * 96)
    print(f"[EMIT COMPLETE] {len(all_stats)} fights → {OUT_DIR}")
    print(f"  total {total_bytes/1e6:.2f} MB")
    # per-fight gauge validation summary (Task 6)
    print("  --- gauge validation (Task 6) ---")
    for s in all_stats:
        medstr = f"{s['dealt_pct_median']:.2f}" if s['dealt_pct_median'] is not None else "null(GAP)"
        print(f"    {s['file']:64s} dealt={s['dealt_hits']:>4d} pct[med={medstr:>9s} "
              f"min={('%.2f'%s['dealt_pct_min']) if s['dealt_pct_min'] is not None else '--':>7s} "
              f"max={('%.2f'%s['dealt_pct_max']) if s['dealt_pct_max'] is not None else '--':>7s}] "
              f"amt>0={s['dealt_amount_all_pos']} recv={s['recv_hits']}(nonnull={s['recv_pct_nonnull']}) "
              f"hp={s['tick_hp_present']}")
    print("=" * 96)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
