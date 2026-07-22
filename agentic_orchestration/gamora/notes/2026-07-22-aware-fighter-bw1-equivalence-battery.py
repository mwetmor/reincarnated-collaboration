#!/usr/bin/env python3
"""AWARE-FIGHTER BW-1 — EQUIVALENCE BATTERY (charter §2.3, THE WAVE'S HARD GATE).

Proves BLIND (the policy seam with consideration set = {distance}) is BEHAVIORALLY IDENTICAL to
the legacy hardcoded nearest-first fighter, so the future ablation gate's margin is purely the value
of the AWARE reads (the no-confound guarantee).

STANDARD (charter §2.3, no tolerance bands):
  - bit-equal metric triples per fight (mobs_killed / total_aoe_hits / player_damage_total), AND
  - decision-trace equality per fight ((tick, chosen_target_id, movement_intent) sequence).
  ANY mismatch ⇒ RED-FLAG STOP + report (incl. RNG-stream divergence with provably identical
  decisions — reported as its OWN class; the conductor rules on the substitute standard).

SEQUENCING (charter §2.3):
  (a) BEFORE any refactor: legacy path at the W3' engine stamp a3671d4 (a detached git worktree),
      with a byte-neutral decision-trace instrument. Record per-fight triple + trace. CROSS-CHECK
      the triples against the recorded W3' gate-output.json — mismatch ⇒ STOP (HEAD drift).
  (b) AFTER the refactor: same 256 fights via the policy seam in BLIND config (main engine tree).
  (c) Compare (a) vs (b): triple bit-equality + trace equality.

The 256 = 32 cells × {matched-baseline, encounter} × 4 seeds {20260722..25}. The exact fights are
reproduced by IMPORTING the W3' runner's selection→formation→scenario→fight machinery (same
cell/seed/composition/parity logic). player_gather_primitive OFF in both configs (charter §3).

ARCHITECTURE: each leg runs in a SUBPROCESS with its own sys.path (main engine src vs worktree src)
so the SAME reproduction code binds to the correct engine. Each leg emits a JSON of per-fight
{triple, trace} keyed by (arm, era, side, kit_id, seed). The parent compares + cross-checks +
writes the verdict. Discipline #2: --smoke runs a 2-pair × 1-seed slice first. Discipline #3:
fights run SEQUENTIALLY within each leg (the W3' runner is sequential; no parallel same-seed regen).

Author: gamora, 2026-07-22. Math note: 2026-07-22-aware-fighter-bw1-math.md §4.
Run:  python3 2026-07-22-aware-fighter-bw1-equivalence-battery.py            # full 256×2
      python3 2026-07-22-aware-fighter-bw1-equivalence-battery.py --smoke    # 2 pairs × 1 seed ×2
      python3 2026-07-22-aware-fighter-bw1-equivalence-battery.py --leg <before|after> <smoke|full> <out.json>
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W3PRIME_GATE = os.path.join(HERE, "2026-07-22-tier3-w3prime-gate.py")
W3PRIME_OUTPUT = os.path.join(HERE, "2026-07-22-tier3-w3prime-gate-output.json")

MAIN_ENGINE_SRC = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..",
                                               "reincarnated-engine", "src"))
BEFORE_ENGINE_SRC = "/tmp/aware-before-worktree/src"   # detached worktree @ stamp a3671d4 + trace

PRIMARY_METRICS = ["mobs_killed", "total_aoe_hits", "player_damage_total"]
SEEDS = [20260722, 20260723, 20260724, 20260725]


# ═══════════════════════════════════════════════════════════════════════════════════════════
# LEG WORKER — runs in a subprocess with the leg's engine src FIRST on sys.path.
# ═══════════════════════════════════════════════════════════════════════════════════════════
def _run_leg(arm: str, mode: str, out_path: str):
    """arm ∈ {before, after}. Imports the W3' machinery (which imports run_spatial_fight from the
    engine src at sys.path[0]) + runs the 256 (or smoke slice) fights with trace_decisions=True and
    the arm's config. Writes {key: {triple, trace}} JSON."""
    engine_src = BEFORE_ENGINE_SRC if arm == "before" else MAIN_ENGINE_SRC
    sys.path.insert(0, engine_src)

    # BIND the engine to the intended src BEFORE importing the gate (Python module cache): once
    # `reincarnated...` is imported from `engine_src`, the gate's later `import reincarnated...`
    # REUSES the cached module — the gate's own sys.path.insert(main_src) cannot rebind an
    # already-loaded module. This is the robust way to pin the BEFORE leg to the worktree engine
    # even though the gate hard-inserts the main src at its import (math note §4.2, Discipline #11).
    import reincarnated.simulation.spatial_gauntlet.spatial_engine as se
    bound = os.path.abspath(se.__file__)

    # import the FROZEN W3' reproduction machinery by file path (module load) ------------------
    import importlib.util
    spec = importlib.util.spec_from_file_location("w3p_gate", W3PRIME_GATE)
    w3p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(w3p)
    intended = os.path.abspath(os.path.join(engine_src, "reincarnated", "simulation",
                                            "spatial_gauntlet", "spatial_engine.py"))
    if bound != intended:
        print(f"FATAL[{arm}]: engine bound to {bound} != intended {intended}", file=sys.stderr)
        sys.exit(7)

    # policy config for the arm ---------------------------------------------------------------
    policy_config = None
    if arm == "after":
        from reincarnated.simulation.spatial_gauntlet.policy import BLIND_CONFIG
        policy_config = BLIND_CONFIG   # explicit BLIND (None also → BLIND; explicit is clearer)

    # ---- rebuild the EXACT W3' selection → formation → pairs (reuse the gate's own logic) ----
    full_rows = w3p.load_full_fit_rows()
    import statistics
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

    # ---- fighter build (byte-identical cell mapping to the W3' runner) ----
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
    for idx, cid in enumerate(all_used_cells):
        pc, _ = w3p._build_martial_player_class(cid, idx, "balanced")
        cd = pc.model_dump()
        cd["resource_economy"] = dict(DEFAULT_RESOURCE_ECONOMY)
        pc_cache[cid] = (pc, cd)

    # ---- encounter + matched-baseline scenarios (byte-identical to W3') ----
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

    # ---- the fight runner (mirrors w3p.run_one_fight, PLUS trace_decisions + policy_config) ----
    def run_traced(scen, cd, pc, seed, sid):
        tiers = [sp.threat_tier for sp in scen.mob_spawns]
        mobs = w3p.build_neutral_mob_dicts(tiers)
        raw = se.run_spatial_fight(
            scenario=scen, class_dict=cd, mob_dicts=mobs, n_fights=1, session_id=sid,
            base_seed=seed, season_id="bw1-battery", player_class=pc,
            damage_modifier=w3p.DAMAGE_MODIFIER, track_proxy_population=False,
            apply_mob_hp_difficulty_multiplier=False, trace_decisions=True,
            **({"policy_config": policy_config} if arm == "after" else {}),
        )
        fr = raw["fight_results"][0]
        triple = {m: (float(getattr(fr, m)) if getattr(fr, m, None) is not None else None)
                  for m in PRIMARY_METRICS}
        trace = raw["decision_traces"][0]
        # normalize trace tuples → lists (JSON round-trip) for stable comparison
        trace = [[int(t[0]), t[1], t[2]] for t in trace]
        return triple, trace

    # ---- iterate pairs × arms × seeds (SEQUENTIAL — Discipline #3) ----
    smoke = (mode == "smoke")
    results = {}
    n_done = 0
    for p in pairs:
        if p["red_flag"] is not None or p["formation"] is None:
            continue
        fclass = p["formation"]["common4_class"]
        if fclass in encounter_red_flags or fclass in baseline_red_flags:
            continue
        era, side, kid = p["era"], p["side"], p["kit_row"]["kit_id"]
        cid = cell_of.get(kid)
        pc, cd = pc_cache[cid]
        seeds = SEEDS[:1] if smoke else SEEDS
        for scen_arm, scen in (("baseline", baseline_scenarios[fclass]),
                               ("encounter", encounter_scenarios[fclass])):
            for seed in seeds:
                key = f"{era}|{side}|{kid}|{scen_arm}|{seed}"
                triple, trace = run_traced(scen, cd, pc, seed, f"bw1_{arm}_{kid}_{side}")
                results[key] = {"triple": triple, "trace": trace}
        n_done += 1
        if smoke and n_done >= 2:
            break

    with open(out_path, "w") as f:
        json.dump({"arm": arm, "mode": mode, "engine_src": engine_src,
                   "engine_bound": bound, "n_pairs": n_done, "results": results}, f)
    print(f"[{arm}] wrote {len(results)} fight records ({n_done} pairs) → {out_path}")


# ═══════════════════════════════════════════════════════════════════════════════════════════
# PARENT — spawn both legs, compare, cross-check vs recorded W3' output, write verdict.
# ═══════════════════════════════════════════════════════════════════════════════════════════
def _load_recorded_w3prime_triples():
    """Recorded W3' gate-output → {era|side|kid|arm|seed: triple}. This IS the legacy metric-triple
    record at the stamp; the BEFORE leg's triples must match it (charter §2.3 cross-check)."""
    d = json.load(open(W3PRIME_OUTPUT))
    out = {}
    for arm, listkey in (("baseline", "baseline_fight_records"),
                         ("encounter", "encounter_fight_records")):
        for rec in d.get(listkey, []):
            if rec.get("skipped"):
                continue
            era, side, kid = rec["era"], rec["side"], rec["kit_id"]
            for f in rec.get("fights", []):
                if "error" in f:
                    continue
                seed = f["seed"]
                out[f"{era}|{side}|{kid}|{arm}|{seed}"] = {
                    m: (float(f[m]) if f.get(m) is not None else None) for m in PRIMARY_METRICS}
    return out


def _spawn_leg(arm, mode, out_path):
    cmd = [sys.executable, os.path.abspath(__file__), "--leg", arm, mode, out_path]
    print(f"→ spawning {arm} leg ({mode}) …")
    r = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        raise SystemExit(f"{arm} leg FAILED (rc={r.returncode})")
    return json.load(open(out_path))


def main():
    mode = "smoke" if ("--smoke" in sys.argv) else "full"
    before_out = os.path.join(HERE, f"2026-07-22-aware-fighter-bw1-battery-before-{mode}.json")
    after_out = os.path.join(HERE, f"2026-07-22-aware-fighter-bw1-battery-after-{mode}.json")

    if not os.path.isdir(BEFORE_ENGINE_SRC):
        raise SystemExit(f"FATAL: BEFORE worktree engine src not found at {BEFORE_ENGINE_SRC} "
                         f"(create: git worktree add --detach /tmp/aware-before-worktree a3671d4 "
                         f"+ install the byte-neutral trace hook).")

    before = _spawn_leg("before", mode, before_out)
    after = _spawn_leg("after", mode, after_out)
    recorded = _load_recorded_w3prime_triples()

    b, a = before["results"], after["results"]
    keys = sorted(set(b) | set(a))

    red_flags = []
    # ---- (a) cross-check BEFORE triples vs recorded W3' gate-output (HEAD-drift guard) ----
    xcheck_missing, xcheck_mismatch = [], []
    for k in sorted(b):
        if k not in recorded:
            xcheck_missing.append(k)
            continue
        for m in PRIMARY_METRICS:
            if b[k]["triple"][m] != recorded[k][m]:
                xcheck_mismatch.append({"key": k, "metric": m,
                                        "before": b[k]["triple"][m], "recorded": recorded[k][m]})
    if xcheck_mismatch:
        red_flags.append({"class": "HEAD_DRIFT_before_vs_recorded_w3prime",
                          "detail": "BEFORE-leg legacy triples diverge from recorded W3' output — "
                                    "HEAD drift on the fight path. STOP.",
                          "n": len(xcheck_mismatch), "examples": xcheck_mismatch[:8]})

    # ---- (c) BEFORE vs AFTER: bit-equal triples + trace equality ----
    triple_mismatch, trace_mismatch, key_asym, rng_divergence_class = [], [], [], []
    for k in keys:
        if k not in b or k not in a:
            key_asym.append(k)
            continue
        # triple bit-equality
        t_eq = all(b[k]["triple"][m] == a[k]["triple"][m] for m in PRIMARY_METRICS)
        if not t_eq:
            triple_mismatch.append({"key": k, "before": b[k]["triple"], "after": a[k]["triple"]})
        # trace equality
        tr_eq = (b[k]["trace"] == a[k]["trace"])
        if not tr_eq:
            trace_mismatch.append({
                "key": k,
                "before_len": len(b[k]["trace"]), "after_len": len(a[k]["trace"]),
                "first_diff": _first_trace_diff(b[k]["trace"], a[k]["trace"]),
            })
        # RNG-stream divergence class (charter §2.3): identical triples AND traces, but the seam is
        # deterministic & consumes no RNG — so an identical-decision-different-draw case can only
        # surface as a triple/trace mismatch here. We record the CLASS explicitly if a mismatch has
        # provably-identical decisions (trace equal) yet triple differs (the only way draws could
        # differ with identical decisions is a non-decision RNG reordering).
        if (not t_eq) and tr_eq:
            rng_divergence_class.append({"key": k, "note": "triple differs but decision trace EQUAL "
                                         "— provably-identical decisions, divergent outcome "
                                         "(RNG-stream divergence class; conductor rules)."})

    if key_asym:
        red_flags.append({"class": "KEY_ASYMMETRY", "detail": "fight keys present in one leg only",
                          "n": len(key_asym), "examples": key_asym[:8]})
    if triple_mismatch:
        red_flags.append({"class": "METRIC_TRIPLE_MISMATCH_before_vs_after",
                          "detail": "BLIND ≠ legacy on the metric triple. STOP.",
                          "n": len(triple_mismatch), "examples": triple_mismatch[:8]})
    if trace_mismatch:
        red_flags.append({"class": "DECISION_TRACE_MISMATCH_before_vs_after",
                          "detail": "BLIND ≠ legacy on the decision trace. STOP.",
                          "n": len(trace_mismatch), "examples": trace_mismatch[:8]})
    if rng_divergence_class:
        red_flags.append({"class": "RNG_STREAM_DIVERGENCE_identical_decisions",
                          "detail": "Reported as its own class (charter §2.3). Conductor rules on "
                                    "the substitute standard.",
                          "n": len(rng_divergence_class), "examples": rng_divergence_class[:8]})

    bit_equal = (not triple_mismatch and not trace_mismatch and not key_asym)
    verdict = "PASS" if (bit_equal and not xcheck_mismatch and not rng_divergence_class) else "RED-FLAG-STOP"

    out = {
        "artifact": "aware-fighter-bw1-equivalence-battery",
        "author": "gamora", "date": "2026-07-22", "mode": mode,
        "standard": "bit-equal metric triples per fight AND decision-trace equality; no tolerance bands",
        "verdict": verdict,
        "bit_equal": bit_equal,
        "n_fights_before": len(b), "n_fights_after": len(a),
        "n_fights_compared": len([k for k in keys if k in b and k in a]),
        "before_cross_check_vs_recorded_w3prime": {
            "n_before_keys": len(b), "n_recorded_matched": len(b) - len(xcheck_missing),
            "n_missing_in_recorded": len(xcheck_missing),
            "n_triple_mismatch": len(xcheck_mismatch),
            "clean": (not xcheck_mismatch),
            "missing_examples": xcheck_missing[:8],
        },
        "before_vs_after": {
            "n_triple_mismatch": len(triple_mismatch),
            "n_trace_mismatch": len(trace_mismatch),
            "n_key_asymmetry": len(key_asym),
            "n_rng_divergence_class": len(rng_divergence_class),
        },
        "red_flags": red_flags,
        "engine_before": before.get("engine_bound"),
        "engine_after": after.get("engine_bound"),
    }
    out_path = os.path.join(HERE, f"2026-07-22-aware-fighter-bw1-battery-verdict-{mode}.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print("\n" + "=" * 78)
    print(f"BATTERY VERDICT [{mode}]: {verdict}")
    print(f"  bit_equal(before≡after): {bit_equal}  |  fights compared: {out['n_fights_compared']}")
    print(f"  BEFORE cross-check vs recorded W3': clean={not xcheck_mismatch} "
          f"(matched {len(b) - len(xcheck_missing)}/{len(b)}, mismatch {len(xcheck_mismatch)})")
    print(f"  before-vs-after: triple_mismatch={len(triple_mismatch)} "
          f"trace_mismatch={len(trace_mismatch)} key_asym={len(key_asym)} "
          f"rng_class={len(rng_divergence_class)}")
    if red_flags:
        print("  RED-FLAGS:")
        for rf in red_flags:
            print(f"    - {rf['class']}: n={rf['n']} — {rf['detail']}")
    print(f"  verdict JSON → {out_path}")
    print("=" * 78)
    return 0 if verdict == "PASS" else 1


def _first_trace_diff(t1, t2):
    n = min(len(t1), len(t2))
    for i in range(n):
        if t1[i] != t2[i]:
            return {"index": i, "before": t1[i], "after": t2[i]}
    if len(t1) != len(t2):
        return {"index": n, "before": (t1[n] if n < len(t1) else None),
                "after": (t2[n] if n < len(t2) else None), "note": "length differs"}
    return None


if __name__ == "__main__":
    if len(sys.argv) >= 5 and sys.argv[1] == "--leg":
        _run_leg(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        raise SystemExit(main())
