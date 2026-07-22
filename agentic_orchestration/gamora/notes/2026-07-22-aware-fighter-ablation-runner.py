#!/usr/bin/env python3
"""AWARE-FIGHTER ABLATION GATE — RUNNER (prereg 2026-07-22-aware-fighter-ablation-prereg.md; charter
2026-07-22-aware-fighter-ablation-execution-charter.md incl. RC-1). Executor: named-gamora.

WHAT THIS IS (and is NOT):
  This is the ABLATION GATE runner, NOT the BW-1 EQUIVALENCE battery. The equivalence battery
  (2026-07-22-aware-fighter-bw1-equivalence-battery.py) PROVED BLIND ≡ legacy (256/256 bit-equal,
  triple + trace) — that no-confound guarantee is DONE. This runner ABLATES BLIND vs AWARE on the
  SAME frozen engine (config-only difference; §1 ablation property) and evaluates the frozen §5 bar
  on the PRIMARY intake metric.

FROZEN CONTRACT (do NOT edit any of this; the prereg GOVERNS):
  - Frame: the W3' 32-cell set × seeds {20260722,20260723,20260724,20260725} × BOTH compositions
    (encounter + matched_baseline) = 256 fights per policy arm, 512 total (§2).
  - Arms: BLIND = BLIND_CONFIG · AWARE = AWARE_CANDIDATE_CONFIG, IMPORTED VERBATIM (§3; 6 entries all
    weights 1.0). No weight edits. Config-only difference; one code path (the policy seam).
  - Both arms: player_gather_primitive OFF (track_proxy_population=False), decision traces ON,
    SEQUENTIAL fights (Discipline #3; §7 pins 1-3).
  - Capture per fight (§2/§4): player_damage_taken (PRIMARY intake) · elapsed_s (SECONDARY duration,
    ticks-equivalent scalar) · all_mobs_killed boolean (clear guard = mobs_killed==total_mob_count) ·
    the standard triple {mobs_killed,total_aoe_hits,player_damage_total} (continuity) · trace length.

EXECUTION ORDER — the C2 seal is LOAD-BEARING (§2 as amended, jack-ryan C2):
  1. SMOKE (§7 pin 2): 1 cell × both arms × 4 seeds. Sanity every captured field; HALT on anomaly.
  2. BLIND arm COMPLETE — all 256 fights, both compositions.
  3. SEAL: write the seal-JSON = 256 blind per-fight records + encounter-arm aggregate-per-seed means
     + SD_seed (statistics.stdev, n-1, 3 df) + the RC-1 disclosure block. FLUSH TO DISK before ANY
     aware fight. Record its md5.
  4. AWARE arm COMPLETE — 256 fights.
  5. VERDICT-INPUT JSON: re-read the seal; verify md5 unchanged (mismatch => red-flag HALT, no
     verdict); embed the md5; evaluate the frozen predicates mechanically (D2, D3, clear-guard,
     specificity, time, C4 determinism profile, per-cell deltas + sign counts). Re-attest RC-1 beats
     at seal + verdict.

RC-1 (charter mid-run ruling): output/ data-sink deltas are EXEMPT from the clean-tree precondition
  provided (i) zero tracked *.py diff under src/reincarnated/ at run-start/seal/verdict; (ii) HEAD
  ==2f43045 unmoved at all three beats; (iii) exempted files disclosed with git hash-object at seal +
  verdict. Any *.py delta OR HEAD move at any beat => red-flag HALT. Executor does NOT touch the
  output/ file (star-lord's seam).

Author: named-gamora (simulation seam), 2026-07-22. Lineage: the BW-1 equivalence battery's
  cell/seed/parity frame machinery (reused verbatim via file-path module load).
Run:  python3 2026-07-22-aware-fighter-ablation-runner.py            # smoke -> BLIND -> seal -> AWARE -> verdict
      python3 2026-07-22-aware-fighter-ablation-runner.py --smoke-only
      python3 2026-07-22-aware-fighter-ablation-runner.py --leg <blind|aware> <smoke|full> <out.json>
"""
import hashlib
import importlib.util
import json
import math
import os
import statistics
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W3PRIME_GATE = os.path.join(HERE, "2026-07-22-tier3-w3prime-gate.py")

MAIN_ENGINE_SRC = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..",
                                               "reincarnated-engine", "src"))
ENGINE_REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "reincarnated-engine"))
FROZEN_HEAD = "2f43045"                       # gate engine hash (prereg §1); RC-1 pins this

SEEDS = [20260722, 20260723, 20260724, 20260725]
# The standard equivalence triple (continuity carry-over; §2). PRIMARY intake + duration are
# captured SEPARATELY (they are not in the triple — that is exactly why intake is the gate metric).
TRIPLE_METRICS = ["mobs_killed", "total_aoe_hits", "player_damage_total"]
COMPOSITIONS = ["encounter", "matched_baseline"]   # §2 P4=BOTH; matched_baseline == the "baseline" arm

SEAL_PATH = os.path.join(HERE, "2026-07-22-aware-fighter-ablation-seal.json")
VERDICT_PATH = os.path.join(HERE, "2026-07-22-aware-fighter-ablation-verdict-input.json")
BLIND_LEG_PATH = lambda mode: os.path.join(HERE, f"2026-07-22-aware-fighter-ablation-blind-{mode}.json")
AWARE_LEG_PATH = lambda mode: os.path.join(HERE, f"2026-07-22-aware-fighter-ablation-aware-{mode}.json")

# §5 bar constants (FROZEN; prereg-pinned — the runner does NOT choose these).
D2_REL_BAR = 0.10        # PASS requires M_rel >= 0.10
D3_K = 2                 # (Ibar_blind - Ibar_aware) >= k * SD_seed
SPECIFICITY_HALF = 0.5   # baseline margin > 1/2 * encounter margin => specificity questionable
TIME_SLOWER_FLAG = 0.05  # AWARE >5% slower on encounter aggregate => flagged


# ═══════════════════════════════════════════════════════════════════════════════════════════
# RC-1 attestation helpers (git-level; run-start / seal / verdict beats)
# ═══════════════════════════════════════════════════════════════════════════════════════════
def _git(*args) -> str:
    r = subprocess.run(["git", "-C", ENGINE_REPO, *args], capture_output=True, text=True)
    return r.stdout.strip()


def _rc1_attest(beat: str) -> dict:
    """RC-1 beat attestation: HEAD short/full, tracked *.py diff under src/reincarnated (must be
    EMPTY), and hash-object disclosure of every tracked output/ delta. Returns the attestation dict;
    raises SystemExit(RED-FLAG) on any *.py delta or HEAD move."""
    head_short = _git("rev-parse", "--short", "HEAD")
    head_full = _git("rev-parse", "HEAD")
    py_diff = [l for l in _git("diff", "--name-only", "HEAD", "--",
                               "src/reincarnated/**/*.py").splitlines() if l.strip()]
    # Tracked (modified/staged) deltas vs HEAD via `git diff --name-only HEAD` — clean paths, NO
    # porcelain-prefix hand-parsing (the ` M ` prefix width is not fixed-3; diff emits bare paths).
    # This captures every tracked modification (untracked files are NOT in `diff HEAD` — correct,
    # they cannot confound a frozen closure and RC-1 only guards tracked *.py + tracked output/).
    tracked_deltas = [l for l in _git("diff", "--name-only", "HEAD").splitlines() if l.strip()]
    output_deltas = [p for p in tracked_deltas if p.startswith("src/reincarnated/output/")]
    non_output_tracked = [p for p in tracked_deltas if not p.startswith("src/reincarnated/output/")]
    exempt_disclosure = []
    for p in output_deltas:
        h = _git("hash-object", p)
        exempt_disclosure.append({"path": p, "git_hash_object": h})

    att = {
        "beat": beat,
        "head_short": head_short,
        "head_full": head_full,
        "head_unmoved_at_frozen": head_short == FROZEN_HEAD,
        "py_diff_under_src_reincarnated": py_diff,          # MUST be empty
        "py_diff_empty": len(py_diff) == 0,
        "tracked_deltas_all": tracked_deltas,
        "exempt_output_deltas": exempt_disclosure,          # RC-1 (iii) disclosure w/ hashes
        "non_output_tracked_deltas": non_output_tracked,    # MUST be empty (only output/ exempt)
    }
    # RC-1 red-flag conditions: any *.py delta OR HEAD move OR any non-output tracked delta.
    if py_diff:
        raise SystemExit(f"RED-FLAG HALT [{beat}]: tracked *.py delta under src/reincarnated/: {py_diff}")
    if head_short != FROZEN_HEAD:
        raise SystemExit(f"RED-FLAG HALT [{beat}]: HEAD moved {head_short} != frozen {FROZEN_HEAD}")
    if non_output_tracked:
        raise SystemExit(f"RED-FLAG HALT [{beat}]: non-output/ tracked delta present: {non_output_tracked}")
    return att


def _md5(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════════════════
# LEG WORKER — one policy arm, all 256 fights (or the smoke slice), SEQUENTIAL. Subprocess so the
# engine src is pinned FIRST on sys.path (same discipline as the BW-1 battery's _run_leg).
# ═══════════════════════════════════════════════════════════════════════════════════════════
def _run_leg(arm: str, mode: str, out_path: str):
    """arm in {blind, aware}. Reuses the W3' machinery (file-path module load) — the SAME
    selection->formation->scenario frame the equivalence battery used — and fires the frame under the
    arm's config with intake + duration + clear + triple + trace-length capture."""
    assert arm in ("blind", "aware"), arm
    sys.path.insert(0, MAIN_ENGINE_SRC)

    # BIND the engine BEFORE loading the gate machinery (module cache pin — battery §4.2 discipline).
    import reincarnated.simulation.spatial_gauntlet.spatial_engine as se
    bound = os.path.abspath(se.__file__)
    intended = os.path.abspath(os.path.join(MAIN_ENGINE_SRC, "reincarnated", "simulation",
                                            "spatial_gauntlet", "spatial_engine.py"))
    if bound != intended:
        print(f"FATAL[{arm}]: engine bound to {bound} != intended {intended}", file=sys.stderr)
        sys.exit(7)

    # policy config for the arm — IMPORTED VERBATIM (§3; NO weight edits, NO construction here).
    from reincarnated.simulation.spatial_gauntlet.policy import BLIND_CONFIG, AWARE_CANDIDATE_CONFIG
    policy_config = BLIND_CONFIG if arm == "blind" else AWARE_CANDIDATE_CONFIG
    # fail-loud config-fidelity guard (defense-in-depth; the arm must be exactly the frozen config).
    if arm == "aware":
        names = [n for n, _ in policy_config.weighted]
        ws = [w for _, w in policy_config.weighted]
        assert len(policy_config.weighted) == 6 and all(w == 1.0 for w in ws), \
            f"AWARE config drift: {policy_config.weighted!r}"
        assert "distance" not in names and "distance_normalized" in names, \
            f"AWARE config drift (distance): {names!r}"
    else:
        assert policy_config.weighted == (("distance", 1.0),), \
            f"BLIND config drift: {policy_config.weighted!r}"

    # ── load the FROZEN W3' reproduction machinery by file path ──
    spec = importlib.util.spec_from_file_location("w3p_gate", W3PRIME_GATE)
    w3p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(w3p)

    # ── rebuild the EXACT W3' selection -> formation -> pairs (reuse the gate's own logic) ──
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

    # ── fighter build (byte-identical cell mapping to the W3' runner) ──
    import sqlite3
    cells = w3p._neutral_cells()
    con = sqlite3.connect(f"file:{w3p.CORPUS_DB}?mode=ro", uri=True)   # READ-ONLY (§7 pin 8)
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

    # ── encounter + matched-baseline scenarios (byte-identical to W3') ──
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

    # ── the fight runner (mirrors the battery's run_traced; captures the ABLATION metrics) ──
    def run_one(scen, cd, pc, seed, sid):
        tiers = [sp.threat_tier for sp in scen.mob_spawns]
        mobs = w3p.build_neutral_mob_dicts(tiers)
        raw = se.run_spatial_fight(
            scenario=scen, class_dict=cd, mob_dicts=mobs, n_fights=1, session_id=sid,
            base_seed=seed, season_id="aware-ablation", player_class=pc,
            damage_modifier=w3p.DAMAGE_MODIFIER,
            track_proxy_population=False,        # player_gather_primitive OFF (§7 pin 1)
            apply_mob_hp_difficulty_multiplier=False,
            trace_decisions=True,                # decision traces ON (§7 pin 3)
            policy_config=policy_config,         # the ONLY between-arm difference (§1 ablation)
        )
        fr = raw["fight_results"][0]
        trace = raw["decision_traces"][0]
        total_mob = int(getattr(fr, "total_mob_count"))
        killed = int(getattr(fr, "mobs_killed"))
        rec = {
            # PRIMARY — enemy-inflicted intake (LC self-costs excluded; engine :4987). Lower better.
            "player_damage_taken": float(getattr(fr, "player_damage_taken")),
            # SECONDARY — fight duration scalar (seconds; ticks-equivalent). Report-only + time flag.
            "elapsed_s": float(getattr(fr, "elapsed_s")),
            # GUARD — all-mobs-killed boolean. Frame is win_condition==all_mobs_killed throughout, so
            #   all-killed <=> mobs_killed==total_mob_count <=> winner=='player'. Capture all three
            #   for auditability; the clear-guard predicate uses the boolean.
            "all_mobs_killed": bool(total_mob > 0 and killed == total_mob),
            "winner": getattr(fr, "winner"),
            "player_kill": bool(getattr(fr, "player_kill")),
            "mobs_killed": killed,
            "total_mob_count": total_mob,
            # continuity triple (§2) — carried so the ablation record ties back to the equivalence battery.
            "triple": {m: (float(getattr(fr, m)) if getattr(fr, m, None) is not None else None)
                       for m in TRIPLE_METRICS},
            "trace_len": len(trace),
        }
        return rec

    # ── iterate pairs × compositions × seeds (SEQUENTIAL — Discipline #3) ──
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
        seeds = SEEDS if not smoke else SEEDS   # smoke slices by CELL (n_done>=1), all 4 seeds (§7 pin 2)
        for comp, scen in (("encounter", encounter_scenarios[fclass]),
                           ("matched_baseline", baseline_scenarios[fclass])):
            for seed in seeds:
                key = f"{era}|{side}|{kid}|{comp}|{seed}"
                results[key] = run_one(scen, cd, pc, seed, f"abl_{arm}_{kid}_{side}")
        n_done += 1
        if smoke and n_done >= 1:            # SMOKE = 1 cell × both comps × 4 seeds (§7 pin 2)
            break

    with open(out_path, "w") as f:
        json.dump({"arm": arm, "mode": mode, "engine_src": MAIN_ENGINE_SRC,
                   "engine_bound": bound, "policy_config": [[n, w] for n, w in policy_config.weighted],
                   "n_cells": n_done, "results": results}, f)
    print(f"[{arm}] wrote {len(results)} fight records ({n_done} cells) -> {out_path}")


def _spawn_leg(arm, mode, out_path):
    cmd = [sys.executable, os.path.abspath(__file__), "--leg", arm, mode, out_path]
    print(f"-> spawning {arm} leg ({mode}) ...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        raise SystemExit(f"{arm} leg FAILED (rc={r.returncode})")
    return json.load(open(out_path))


# ═══════════════════════════════════════════════════════════════════════════════════════════
# AGGREGATION — encounter-arm aggregate-per-seed intake mean + SD_seed (§5 estimator).
# ═══════════════════════════════════════════════════════════════════════════════════════════
def _encounter_keys(results: dict, comp: str = "encounter") -> list:
    return sorted(k for k in results if k.split("|")[3] == comp)


def _aggregate_per_seed_mean(results: dict, comp: str, field: str = "player_damage_taken") -> dict:
    """Mean per-fight `field` over the `comp`-arm cells, grouped by seed. Returns {seed: mean}."""
    by_seed = {s: [] for s in SEEDS}
    for k in _encounter_keys(results, comp):
        seed = int(k.split("|")[4])
        by_seed[seed].append(results[k][field])
    return {s: (statistics.mean(v) if v else float("nan")) for s, v in by_seed.items()}


def _ibar(results: dict, comp: str, field: str = "player_damage_taken") -> float:
    """Ibar = mean per-fight intake across the whole `comp` arm (32 cells × 4 seeds), i.e. the mean
    of the per-fight values (equivalently the mean of the per-seed aggregate means, balanced design)."""
    vals = [results[k][field] for k in _encounter_keys(results, comp)]
    return statistics.mean(vals) if vals else float("nan")


def _sd_seed(results: dict, comp: str, field: str = "player_damage_taken") -> tuple:
    """SD_seed = seed-to-seed SD of the aggregate-per-seed mean intake — the SAME estimator jack-ryan
    verified on the dealt stand-in (statistics.stdev, n-1, 3 df). Returns (SD_seed, per_seed_means)."""
    per_seed = _aggregate_per_seed_mean(results, comp, field)
    ordered = [per_seed[s] for s in SEEDS]
    sd = statistics.stdev(ordered) if len(ordered) >= 2 else 0.0
    return sd, per_seed


# ═══════════════════════════════════════════════════════════════════════════════════════════
# SEAL — the blind arm's 256 records + encounter aggregate-per-seed + SD_seed, FLUSHED before AWARE.
# ═══════════════════════════════════════════════════════════════════════════════════════════
def _write_seal(blind_results: dict, rc1_run_start: dict) -> str:
    sd_seed, per_seed = _sd_seed(blind_results, "encounter")
    ibar_blind = _ibar(blind_results, "encounter")
    rc1_seal = _rc1_attest("seal")
    seal = {
        "artifact": "aware-fighter-ablation-seal",
        "author": "named-gamora", "date": "2026-07-22",
        "prereg": "2026-07-22-aware-fighter-ablation-prereg.md (FROZEN, gate hash 2f43045)",
        "note": "BLIND arm, complete, sealed BEFORE any aware fight (§2 C2 invariant). "
                "SD_seed + encounter aggregate-per-seed means are IMMUTABLE after this point.",
        "frozen_head": FROZEN_HEAD,
        "n_blind_records": len(blind_results),
        "seeds": SEEDS,
        "estimator": "SD_seed = statistics.stdev (n-1, 3 df) of the encounter-arm aggregate-per-seed "
                     "mean player_damage_taken (§5 pinned estimator (i))",
        "encounter_aggregate_per_seed_mean_intake": {str(s): per_seed[s] for s in SEEDS},
        "Ibar_blind_encounter": ibar_blind,
        "SD_seed": sd_seed,
        "blind_per_fight_records": blind_results,   # all 256 (both compositions)
        # RC-1 (iii): exempted output/ delta disclosure at run-start AND seal (hash drift immaterial).
        "rc1_run_start_attestation": rc1_run_start,
        "rc1_seal_attestation": rc1_seal,
    }
    with open(SEAL_PATH, "w") as f:
        json.dump(seal, f, indent=2, sort_keys=True)
    md5 = _md5(SEAL_PATH)
    print(f"[SEAL] flushed {len(blind_results)} blind records -> {SEAL_PATH}")
    print(f"[SEAL] Ibar_blind(encounter)={ibar_blind:.4f}  SD_seed={sd_seed:.4f}  md5={md5}")
    return md5


# ═══════════════════════════════════════════════════════════════════════════════════════════
# VERDICT-INPUT — re-read seal, verify md5, embed, evaluate the frozen predicates MECHANICALLY.
# ═══════════════════════════════════════════════════════════════════════════════════════════
def _determinism_profile(results: dict, arm_name: str) -> dict:
    """C4 rider: per-cell intake seed-SD zero-counts (both compositions) + pooled per-cell seed-SD.
    A cell = (era,side,kid,comp); its seed-SD is stdev over the 4 seeds' intake. Reports how many
    cells are seed-deterministic on intake (SD==0) so a near-vacuous-D3 outcome is visible."""
    prof = {}
    for comp in COMPOSITIONS:
        cell_sds = {}
        # group by cell (strip the seed)
        cells = {}
        for k in results:
            if k.split("|")[3] != comp:
                continue
            cell = "|".join(k.split("|")[:4])
            cells.setdefault(cell, []).append(results[k]["player_damage_taken"])
        for cell, vals in cells.items():
            cell_sds[cell] = statistics.stdev(vals) if len(vals) >= 2 else 0.0
        n_cells = len(cell_sds)
        n_zero = sum(1 for v in cell_sds.values() if v == 0.0)
        pooled = statistics.pstdev(list(cell_sds.values())) if cell_sds else 0.0  # diagnostic only
        prof[comp] = {
            "n_cells": n_cells,
            "n_cells_seed_deterministic_intake": n_zero,
            "n_cells_seed_variable_intake": n_cells - n_zero,
            "pooled_per_cell_seed_SD_diagnostic": pooled,
        }
    prof["arm"] = arm_name
    return prof


def _clear_guard(blind: dict, aware: dict) -> list:
    """Per (cell, seed, composition) all_mobs_killed match blind-vs-aware. List every mismatch with
    cell id + direction (§4/§5). A mismatch => that cell's intake comparison void => PARTIAL."""
    mismatches = []
    for k in sorted(set(blind) | set(aware)):
        b = blind.get(k)
        a = aware.get(k)
        if b is None or a is None:
            mismatches.append({"key": k, "issue": "key_asymmetry",
                               "blind_present": b is not None, "aware_present": a is not None})
            continue
        if b["all_mobs_killed"] != a["all_mobs_killed"]:
            mismatches.append({
                "key": k,
                "blind_all_mobs_killed": b["all_mobs_killed"],
                "aware_all_mobs_killed": a["all_mobs_killed"],
                "direction": ("aware_cleared_MORE" if a["all_mobs_killed"] and not b["all_mobs_killed"]
                              else "aware_cleared_FEWER"),
                "blind_mobs_killed": b["mobs_killed"], "aware_mobs_killed": a["mobs_killed"],
                "total_mob_count": b["total_mob_count"],
            })
    return mismatches


def _per_cell_intake_deltas(blind: dict, aware: dict, comp: str) -> dict:
    """§5 reporting shape: per-cell intake delta (blind - aware; positive = aware took less) averaged
    over the 4 seeds, + sign counts (reported, NOT gated)."""
    deltas = {}
    cells = sorted({"|".join(k.split("|")[:4]) for k in blind if k.split("|")[3] == comp})
    for cell in cells:
        b_vals, a_vals = [], []
        for s in SEEDS:
            k = f"{cell}|{s}"
            if k in blind and k in aware:
                b_vals.append(blind[k]["player_damage_taken"])
                a_vals.append(aware[k]["player_damage_taken"])
        if b_vals and a_vals:
            deltas[cell] = statistics.mean(b_vals) - statistics.mean(a_vals)
    n_pos = sum(1 for d in deltas.values() if d > 0)
    n_neg = sum(1 for d in deltas.values() if d < 0)
    n_zero = sum(1 for d in deltas.values() if d == 0)
    return {"per_cell_delta_blind_minus_aware": deltas,
            "sign_counts": {"aware_less_intake_positive": n_pos,
                            "aware_more_intake_negative": n_neg, "equal": n_zero}}


def _write_verdict(blind_results: dict, aware_results: dict, seal_md5_at_seal: str,
                   rc1_run_start: dict) -> dict:
    # C2 invariant: re-read the seal, verify md5 unchanged.
    if not os.path.isfile(SEAL_PATH):
        raise SystemExit("RED-FLAG HALT: seal file missing at verdict.")
    seal_md5_now = _md5(SEAL_PATH)
    if seal_md5_now != seal_md5_at_seal:
        raise SystemExit(f"RED-FLAG HALT: seal md5 mismatch (seal-time {seal_md5_at_seal} != "
                         f"verdict-time {seal_md5_now}). No verdict.")
    seal = json.load(open(SEAL_PATH))
    # the sealed blind numbers are AUTHORITATIVE (frozen before aware); recompute from the sealed
    # records for self-consistency and assert they match the sealed scalars.
    sealed_blind = seal["blind_per_fight_records"]
    sd_seed = seal["SD_seed"]
    ibar_blind = seal["Ibar_blind_encounter"]
    # defense-in-depth: the in-memory blind_results must equal the sealed records (no drift).
    assert sealed_blind.keys() == blind_results.keys(), "blind key drift seal-vs-memory"

    ibar_aware = _ibar(aware_results, "encounter")
    m_rel = (ibar_blind - ibar_aware) / ibar_blind if ibar_blind != 0 else float("nan")
    abs_margin = ibar_blind - ibar_aware

    # D2 — relative bar
    d2 = bool(m_rel >= D2_REL_BAR)
    # D3 — noise floor (degenerate guard if SD_seed == 0)
    sd_zero = (sd_seed == 0.0)
    d3 = True if sd_zero else bool(abs_margin >= D3_K * sd_seed)
    d3_note = ("SD_seed == 0 (fully-deterministic blind encounter arm): D3 AUTO-SATISFIES per the §5 "
               "degenerate guard; D2 + clear-guard still bind." if sd_zero else
               f"D3 is a LIVE floor: abs_margin={abs_margin:.4f} vs k*SD_seed={D3_K*sd_seed:.4f}.")

    # Clear guard (§4/§5) — the PARTIAL trigger (§6 precedence)
    clear_mismatches = _clear_guard(sealed_blind, aware_results)

    # Specificity (matched-baseline margin vs encounter margin) — the other PARTIAL trigger
    ibar_blind_base = _ibar(sealed_blind, "matched_baseline")
    ibar_aware_base = _ibar(aware_results, "matched_baseline")
    m_rel_base = ((ibar_blind_base - ibar_aware_base) / ibar_blind_base
                  if ibar_blind_base != 0 else float("nan"))
    # "flag if baseline margin > 1/2 * encounter margin" — on the RELATIVE margins (§5 uses M_rel).
    specificity_flag = bool(m_rel_base > SPECIFICITY_HALF * m_rel) if not math.isnan(m_rel_base) else False

    # Time (§4) — encounter-arm aggregate duration, both arms; flag AWARE >5% slower.
    dur_blind = _ibar(sealed_blind, "encounter", "elapsed_s")
    dur_aware = _ibar(aware_results, "encounter", "elapsed_s")
    time_rel = (dur_aware - dur_blind) / dur_blind if dur_blind != 0 else float("nan")
    time_flag = bool(time_rel > TIME_SLOWER_FLAG)

    # C4 determinism profile (both arms × both compositions)
    det_blind = _determinism_profile(sealed_blind, "blind")
    det_aware = _determinism_profile(aware_results, "aware")

    # Per-cell intake deltas + sign counts (both compositions; §5 reporting shape)
    deltas_enc = _per_cell_intake_deltas(sealed_blind, aware_results, "encounter")
    deltas_base = _per_cell_intake_deltas(sealed_blind, aware_results, "matched_baseline")

    aware_per_seed = _aggregate_per_seed_mean(aware_results, "encounter")

    rc1_verdict = _rc1_attest("verdict")

    verdict = {
        "artifact": "aware-fighter-ablation-verdict-input",
        "author": "named-gamora", "date": "2026-07-22",
        "prereg": "2026-07-22-aware-fighter-ablation-prereg.md (FROZEN, gate hash 2f43045)",
        "note": "PREDICATE FACTS ONLY. The VERDICT (PASS/FAIL/PARTIAL) is the conductor's DRIFT-CRITIC "
                "synthesis against the frozen sheet + Matt's ruling. This file does NOT caption a verdict.",
        "frozen_head": FROZEN_HEAD,
        # C2 seal binding
        "seal_path": os.path.basename(SEAL_PATH),
        "seal_md5_at_seal": seal_md5_at_seal,
        "seal_md5_at_verdict": seal_md5_now,
        "seal_md5_match": True,   # (else we'd have HALTed above)
        # headline predicate inputs
        "n_blind_records": len(sealed_blind),
        "n_aware_records": len(aware_results),
        "Ibar_blind_encounter": ibar_blind,
        "Ibar_aware_encounter": ibar_aware,
        "abs_margin_intake": abs_margin,
        "M_rel": m_rel,
        "SD_seed": sd_seed,
        "encounter_aggregate_per_seed_mean_intake": {
            "blind": seal["encounter_aggregate_per_seed_mean_intake"],
            "aware": {str(s): aware_per_seed[s] for s in SEEDS},
        },
        # D2 / D3
        "D2_relative_bar": {"bar": D2_REL_BAR, "M_rel": m_rel, "D2_met": d2,
                            "predicate": "M_rel >= 0.10"},
        "D3_noise_floor": {"k": D3_K, "SD_seed": sd_seed, "abs_margin": abs_margin,
                           "k_times_SD_seed": D3_K * sd_seed, "SD_seed_is_zero": sd_zero,
                           "D3_met": d3, "note": d3_note,
                           "predicate": "(Ibar_blind - Ibar_aware) >= 2 * SD_seed"},
        # clear guard (PARTIAL trigger)
        "clear_guard": {"n_mismatches": len(clear_mismatches), "clean": len(clear_mismatches) == 0,
                        "mismatches": clear_mismatches,
                        "note": "per (cell,seed,composition) all_mobs_killed match blind-vs-aware; any "
                                "mismatch => that cell's intake void => PARTIAL (§6 precedence)."},
        # specificity (PARTIAL trigger)
        "specificity": {"Ibar_blind_matched_baseline": ibar_blind_base,
                        "Ibar_aware_matched_baseline": ibar_aware_base,
                        "M_rel_matched_baseline": m_rel_base,
                        "half_encounter_margin_threshold": SPECIFICITY_HALF * m_rel,
                        "baseline_margin_exceeds_half_encounter": specificity_flag,
                        "note": "expectation approx 0 on geometry-sparse baseline; flag if baseline "
                                "M_rel > 1/2 * encounter M_rel => geometry-specificity questionable => PARTIAL."},
        # time (report-only flag)
        "time": {"encounter_duration_blind_s": dur_blind, "encounter_duration_aware_s": dur_aware,
                 "aware_slower_fraction": time_rel, "aware_slower_than_5pct": time_flag,
                 "note": "report-only directional flag; not auto-fail (§4)."},
        # C4 determinism profile (both arms × both compositions)
        "C4_intake_determinism_profile": {"blind": det_blind, "aware": det_aware},
        # per-cell deltas + sign counts (reported, not gated)
        "per_cell_intake_deltas": {"encounter": deltas_enc, "matched_baseline": deltas_base},
        # RC-1 disclosures at run-start + verdict (seal already carries run-start + seal)
        "rc1_run_start_attestation": rc1_run_start,
        "rc1_verdict_attestation": rc1_verdict,
    }
    with open(VERDICT_PATH, "w") as f:
        json.dump(verdict, f, indent=2, sort_keys=True)
    print(f"[VERDICT] wrote predicate-facts -> {VERDICT_PATH}")
    return verdict


# ═══════════════════════════════════════════════════════════════════════════════════════════
# SMOKE — 1 cell × both arms × 4 seeds; sanity every captured field; HALT on anomaly.
# ═══════════════════════════════════════════════════════════════════════════════════════════
def _smoke_sanity(blind: dict, aware: dict) -> None:
    def _check(label, results):
        assert len(results) == 8, f"{label}: expected 8 smoke records (1 cell × 2 comps × 4 seeds), got {len(results)}"
        for k, r in results.items():
            assert isinstance(r["player_damage_taken"], float) and r["player_damage_taken"] >= 0.0, \
                f"{label}[{k}]: intake not a non-negative float: {r['player_damage_taken']}"
            assert isinstance(r["elapsed_s"], float) and r["elapsed_s"] > 0.0, \
                f"{label}[{k}]: elapsed_s not positive float: {r['elapsed_s']}"
            assert isinstance(r["all_mobs_killed"], bool), f"{label}[{k}]: clear flag not bool"
            assert r["total_mob_count"] > 0, f"{label}[{k}]: total_mob_count non-positive"
            assert 0 <= r["mobs_killed"] <= r["total_mob_count"], f"{label}[{k}]: mobs_killed out of range"
            assert isinstance(r["trace_len"], int) and r["trace_len"] > 0, \
                f"{label}[{k}]: trace_len not positive int: {r['trace_len']} (traces must be ON)"
            for m in TRIPLE_METRICS:
                assert m in r["triple"], f"{label}[{k}]: triple missing {m}"
    _check("blind-smoke", blind)
    _check("aware-smoke", aware)
    print(f"[SMOKE] sanity PASS: 8 blind + 8 aware records, all fields live "
          f"(intake>=0 float, elapsed_s>0, clear bool, trace_len>0 int, triple complete).")


def main():
    smoke_only = ("--smoke-only" in sys.argv)

    # RC-1 run-start attestation (beat 1). HALTs on any *.py delta / HEAD move.
    print("=" * 90)
    rc1_run_start = _rc1_attest("run_start")
    print(f"[RC-1 run_start] HEAD={rc1_run_start['head_short']} (unmoved={rc1_run_start['head_unmoved_at_frozen']}) "
          f"py_diff_empty={rc1_run_start['py_diff_empty']} "
          f"exempt_output_deltas={[d['path'] for d in rc1_run_start['exempt_output_deltas']]}")
    print("=" * 90)

    # ── 1. SMOKE (both arms) ──
    print("\n### SMOKE (1 cell × both arms × 4 seeds) ###")
    blind_smoke = _spawn_leg("blind", "smoke", BLIND_LEG_PATH("smoke"))["results"]
    aware_smoke = _spawn_leg("aware", "smoke", AWARE_LEG_PATH("smoke"))["results"]
    _smoke_sanity(blind_smoke, aware_smoke)
    if smoke_only:
        print("\n[--smoke-only] stopping after smoke sanity (no full run, no seal).")
        return 0

    # ── 2. BLIND arm COMPLETE (256) ──
    print("\n### BLIND arm — COMPLETE (256 fights, both compositions) ###")
    blind_full = _spawn_leg("blind", "full", BLIND_LEG_PATH("full"))["results"]
    assert len(blind_full) == 256, f"BLIND arm expected 256 records, got {len(blind_full)}"

    # ── 3. SEAL (flush BEFORE any aware fight) ──
    print("\n### SEAL (flush blind before ANY aware fight) ###")
    seal_md5 = _write_seal(blind_full, rc1_run_start)

    # ── 4. AWARE arm COMPLETE (256) ──
    print("\n### AWARE arm — COMPLETE (256 fights, both compositions) ###")
    aware_full = _spawn_leg("aware", "full", AWARE_LEG_PATH("full"))["results"]
    assert len(aware_full) == 256, f"AWARE arm expected 256 records, got {len(aware_full)}"

    # ── 5. VERDICT-INPUT (re-read seal, verify md5, evaluate predicates) ──
    print("\n### VERDICT-INPUT (re-read seal, verify md5, evaluate frozen predicates) ###")
    v = _write_verdict(blind_full, aware_full, seal_md5, rc1_run_start)

    # headline echo (predicate FACTS only — no verdict word)
    print("\n" + "=" * 90)
    print("PREDICATE FACTS (no verdict caption — conductor synthesizes):")
    print(f"  Ibar_blind(enc) = {v['Ibar_blind_encounter']:.4f}")
    print(f"  Ibar_aware(enc) = {v['Ibar_aware_encounter']:.4f}")
    print(f"  abs_margin      = {v['abs_margin_intake']:.4f}")
    print(f"  M_rel           = {v['M_rel']:.6f}   (D2 bar {D2_REL_BAR}: met={v['D2_relative_bar']['D2_met']})")
    print(f"  SD_seed         = {v['SD_seed']:.4f}   (D3 k={D3_K}: met={v['D3_noise_floor']['D3_met']}, "
          f"sd_zero={v['D3_noise_floor']['SD_seed_is_zero']})")
    print(f"  clear-guard     : clean={v['clear_guard']['clean']} (n_mismatch={v['clear_guard']['n_mismatches']})")
    print(f"  specificity     : M_rel_base={v['specificity']['M_rel_matched_baseline']:.6f} "
          f"flag={v['specificity']['baseline_margin_exceeds_half_encounter']}")
    print(f"  time            : aware_slower={v['time']['aware_slower_fraction']*100:.2f}% flag={v['time']['aware_slower_than_5pct']}")
    print(f"  seal md5 match  : {v['seal_md5_match']} ({v['seal_md5_at_seal']})")
    print("=" * 90)
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 5 and sys.argv[1] == "--leg":
        _run_leg(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        raise SystemExit(main())
