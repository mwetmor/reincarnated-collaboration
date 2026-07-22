# Aware-Fighter BW-1.1 — Slice Report (as-built)

**Author:** gamora (simulation seam). **Conductor:** gandalf RUN-CONDUCTOR (ledger L-25).
**Scope:** two Gate-2 INFO dispositions — F2 ALIGN (E4 commitment-site coherence) + F9 NORMALIZE
(distance dominance in mixed configs). Full build discipline (production engine code).
**Math addendum (Discipline #1, landed BEFORE code):**
`2026-07-22-aware-fighter-bw11-math-addendum.md` (§A0 recon, §A1 F2, §A2 F9, §A3 gate, §A4 Disc-#12).

## Battery verdict (the hard gate) — PASS
`--baseline-file` FULL 256: **PASS, 256/256 bit-equal** vs the recorded frozen BW-1 BEFORE leg.
triple_mismatch=0, trace_mismatch=0, key_asymmetry=0, rng_divergence_class=0. BEFORE cross-check vs
recorded W3′ clean 256/256. No tolerance bands, no red flags. Smoke (4/4) PASS first (Discipline #2).
Verdict JSON: `…-battery-verdict-bw11-baseline-full.json` (engine_after = main tree; engine_before =
the frozen a3671d4 record). AFTER leg record: `…-bw11-battery-after-full.json`.

## Test counts — 72 passed (was 59 in BW-1; +13)
`test_aware_fighter_policy_seam.py`: 45 (32 BW-1 + 13 new BW-1.1) + `test_spatial_gauntlet_scenarios.py`: 27.
New: `TestF9DistanceNormalization` (7) — both distance variants share one scorer; BLIND unchanged raw
fast path; AWARE re-points to distance_normalized; neither variant needs the map; normalized scores in
[0,1]; normalization removes distance-dominance in a mixed config (measured weight, not knife-edge).
`TestF2E4CommitmentTargetReuse` (6) — BLIND E4-projection target ≡ legacy nearest; AWARE can differ;
both sites call the seam not raw-min; no boss_focus (attack-target semantics); `_e4_blind` gate
predicate preserved; sites are player-only (`p = self.player`). All existing tests green.

## Files touched
**Engine** (confined to `simulation/spatial_gauntlet/` + `tests/`; NO telemetry, NO corpus.db, NO schema):
- `policy/considerations.py` (+27/−8): F9 — added `distance_normalized` (same `_score_distance`
  scorer, normalize=True); `_MAP_CONSUMERS` excludes both distance variants; `AWARE_CANDIDATE_CONFIG`
  re-points `("distance",1.0)`→`("distance_normalized",1.0)`. BLIND_CONFIG + `distance` entry UNCHANGED.
- `spatial_engine.py` (+17/−?): F2 — at both E4 sites (service move-cancel `:3137`, initiate `:3239`)
  `nearest = min(alive_mobs, key=…)` → `_policy_choose_target(p, alive_mobs, config=self._policy_config)`.
  No signature change (`self._policy_config` already in scope). `_e4_blind` gate untouched.
- `tests/test_aware_fighter_policy_seam.py` (+178): the two new classes + `_ctx`/`_normalize_scores` imports.

**Collab notes:** math addendum (new); battery runner (+`--baseline-file` mode via extracted
`_compare_and_verdict`, no gate-logic drift); verdict + after JSONs (new).

## Deviations / as-found corrections (Discipline #11)
1. **Line numbers as-found:** E4 sites gated at `:3129`/`:3225` (brief cited ~:3130/~:3226); the
   `min(...)` was at `:3130`/`:3226` pre-edit, now `_policy_choose_target` at `:3137`/`:3239` post-edit
   (comment blocks shifted them). `self._policy_config` set at `:2407` (brief ~:2407 — exact).
2. **No mob path exists at the E4 sites** — both `_e4_service_commitment`/`_e4_initiate_commitment`
   bind `p = self.player` and are called only from the player action phase. "Mob paths unchanged"
   holds trivially (there are none to change); reported as-found, not as-briefed.
3. **F2 uses attack-target semantics (no boss_focus)** — the E4 whiff-projection is for a CAST/ATTACK,
   so it matches `_select_skill_for_entity`'s no-boss_focus seam call (`:1957`), NOT the movement
   boss-focus limb. Neutral in-frame regardless (W3′ 32 cells are all `all_mobs_killed` → boss_focus
   is None throughout). Rationale in addendum §A1.2.
4. **Test fixture correction (honest):** my first F9-dominance fixture used cluster weight 8.0, which
   let cluster dominate even the RAW config (raw picked `c3`, not `near`) — the test failed. I probed
   the scores empirically and set weight 2.0 (measured to straddle the crossover: raw→`near`,
   normalized→`c3`). Engine unchanged; only the test's demonstration weight corrected.
5. **Worktree removal:** ran the full gate FIRST (worktree present as insurance), then removed. Plain
   remove refused (worktree held the BW-1 byte-neutral trace hook — 1 modified file); force-removed
   after confirming detached-at-`a3671d4` (stamp lives in main history) and untracked-diff = the
   trace hook only. **`/tmp/aware-before-worktree` ABSENT (confirmed).**

## Semantic-shift declarations (Discipline #12) — full text in addendum §A4
- F2: E4 whiff-projection target RE-SOURCED raw-nearest → seam attack-target. BLIND no-op (proven);
  AWARE re-targets. `_e4_blind` axis predicate untouched.
- F9: `distance_normalized` ADDED; AWARE re-points to it. BLIND keeps raw {distance} (IEEE-exact).
  Changes AWARE argmax (scale-commensurate), not BLIND. Machinery, not tuning — weights pin at prereg.

## Guardrails honored
`_e4_blind` gating semantics UNCHANGED; BLIND_CONFIG + `distance` registry entry + fast-path predicate
UNCHANGED; skill selection / movement execution / escape-gather overrides UNTOUCHED; no telemetry
schema change; corpus.db READ-ONLY. Commit-never-push (both repos) — conductor pushes after delta check.
