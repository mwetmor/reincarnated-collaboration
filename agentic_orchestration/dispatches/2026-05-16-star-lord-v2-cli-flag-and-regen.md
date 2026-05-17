# Dispatch — 2026-05-16 — star-lord — V2 CLI flag + V2-mode live regen (closes V1-vs-V2 mode gap)

**From:** knight-rider (authored per star-lord regen-001009 finding 2026-05-16: standard CLI uses V1 mode; V2 mode requires explicit invocation; Matt 2026-05-16 directive "fire tier 1 #2")
**To:** star-lord
**Approved by:** Matt at 2026-05-16 Day 4 (Tier 1 #2 confirmation)
**Status:** PENDING — HOLD-on-prior. Do NOT execute until: (1) your in-flight Stage 2 cosmological-vocabulary dispatch completes; (2) V2.4 telemetry migration dispatch completes. Star-lord can only run one dispatch per session. Sequence: Stage 2 → V2.4 telemetry → THIS → Stage 3 cipher migration.
**Estimated effort:** 1 session (~2-4h); CLI flag addition + V2-mode regen + smoke verification.
**Acceptance:** `--use-room-evaluation` CLI flag added to `python -m reincarnated.cli generate-season`; V2-mode regen completes for a fresh season; V2.1 per-fight fields (`encounter_index_within_room`, `room_won`, `hp_fraction_at_encounter_start`) populate non-null; smoke verifies V2 mode mechanics worked end-to-end; intermediate tag.

---

## Why this dispatch exists

Per star-lord regen-001009 completion finding (2026-05-16):

> Standard CLI (`python -m reincarnated.cli generate-season`) does not expose `--use-room-evaluation`. Season_001009 ran in V1 mode (`use_room_evaluation=False` for all 10 classes). V2.1 fields are NULL because the V2 code path was never invoked — this is correct V1 behavior, NOT a recorder bug. The V2.1 emission gap fix at `df717a8` is confirmed correct by 27/27 unit tests in `test_telemetry_v21.py`. But live V2 regen verification requires `use_room_evaluation=True` which needs either a CLI flag addition or a direct orchestrator invocation.

Star-lord recommended: knight-rider routes a small CLI-flag addition dispatch + V2 regen for live V2.1 emission fix verification.

**Closes the V1-vs-V2 mode gap** + establishes V2-mode calibration baseline (which is the actual VS2a-relevant mode per B10 V2 sequential rooms).

## What this dispatch produces

### Step 1 — CLI flag addition

In `python -m reincarnated.cli generate-season` (or equivalent CLI module):

1. Add `--use-room-evaluation` flag (boolean; default False for backward compat)
2. Flag passed through to balance_loop / class generation orchestration
3. Test: verify flag works via `python -m reincarnated.cli generate-season --seed=1010 --use-room-evaluation`

### Step 2 — V2-mode regen (next sequential season)

1. Run V2-mode regen with fresh seed (likely season_001010)
2. Use Matt-approved standard balance+regen workflow + `--use-room-evaluation` flag
3. Generate 10 classes (per standard regen pattern)
4. Verify regen completes without errors

### Step 3 — V2.1 emission-gap-fix live verification

Per gamora V2.1 emission-gap-fix completion (`gamora/v1.3-b10-v2-emission-gap-fix @ df717a8`):

1. Query `class_fight_loadouts` rows from the new V2-mode regen
2. Verify V2.1 per-fight fields populate NON-NULL:
   - `encounter_index_within_room` — cycles [0, 1, 2] per V2 sequential-room semantics
   - `room_won` — consistent within room groups (0 violations)
   - `hp_fraction_at_encounter_start` — encounter_0 always 1.0; always in [0,1]
3. Cross-verify against gamora V2.1 fix's 27 unit tests (same behavior expected live)
4. If V2 mode fails to populate non-null fields → flag as REGRESSION; do NOT assume tests cover live behavior

### Step 4 — Calibration baseline check

Per Discipline #1 (math-before-code) + star-lord's regen-001009 finding (mean |mod-1.0| = 0.876 — worse than V1 baseline 0.799):

1. Compute mean |mod-1.0| for V2-mode regen
2. Compare to V1 baseline (0.799) AND V1-post-Day4-changes (0.876)
3. **V2-mode baseline establishment**: this is the actual VS2a-relevant calibration anchor; document it explicitly in MIGRATION.md
4. Surface to knight-rider: is V2-mode calibration better, similar, or worse than V1-post-Day4? Informs whether jack-ryan calibration analysis (Tier 1 #3) is needed

### Step 5 — Intermediate tag + AGENT_STATE + completion record

- Tag: `star-lord/v1.3-v2-cli-flag-and-regen-season_001010` (or per actual season_id)
- AGENT_STATE.md updated
- Completion record at bottom filled
- Cross-seam notification to knight-rider — V2-mode baseline established; jack-ryan calibration analysis routing decision unblocked

## Cross-seam considerations

- **Gamora**: READ-ONLY upstream (V2.1 emission-gap-fix is your verification target); MIGRATION.md cross-reference
- **Rocket**: READ-ONLY (generation seam unaffected by CLI flag)
- **Knight-rider**: notify at completion; Tier 1 #3 (jack-ryan calibration analysis) routing decision unblocked + Stage 3 cipher migration can fire after this (sequencing)

## Out of scope (explicit)

- **NO Stage 3 cipher migration work** (separate dispatch queued after this)
- **NO new regen beyond the single V2-mode verification regen**
- **NO V1-mode regen** (V1 mode is the standard CLI default; no test regen needed)
- **NO calibration epoch decisions-log entry** (jack-ryan-led; separate)
- **NO recorder code changes** (V2.1 emission fix already landed)
- **NO V2.x schema changes** (V2.3 schema in place)

## Required reading

- Star-lord regen-001009 completion record (your own report; the V1-vs-V2 gap finding)
- Gamora V2.1 emission-gap-fix dispatch + completion (`gamora/v1.3-b10-v2-emission-gap-fix @ df717a8`)
- `reincarnated-engine/src/reincarnated/cli/` or equivalent (target for CLI flag addition)
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` — V2 invocation site (use_room_evaluation parameter)
- `reincarnated-engine/tests/test_telemetry_v21.py` — 27/27 unit tests; live regen should match
- Engineering disciplines #1 (math-before-code: calibration baseline check); #2 (smoke); #11 (attribution)

## Acceptance criteria

- [ ] `--use-room-evaluation` CLI flag added
- [ ] V2-mode regen completes for fresh season (likely season_001010)
- [ ] V2.1 per-fight fields populate non-null (live V2.1 emission-gap-fix verification)
- [ ] V2-mode calibration baseline computed + documented in MIGRATION.md
- [ ] No regressions in V1-mode (standard CLI behavior preserved per backward compat)
- [ ] Intermediate tag `star-lord/v1.3-v2-cli-flag-and-regen-<season_id>` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion (Tier 1 #3 routing + Stage 3 sequencing unblocked)

## Tag policy

- **Intermediate tag:** `star-lord/v1.3-v2-cli-flag-and-regen-<season_id>` at the commit closing CLI flag + regen + verification.
- **Milestone tag:** none from this dispatch.

---

## Completion record

**Completed:** 2026-05-16/17 (regen completed 02:38 UTC, verification + tag + completion record 03:xx UTC)
**Intermediate tag:** `star-lord/v1.3-v2-cli-flag-and-regen-season_001010` at commit `faea479`
**CLI flag commit:** `505f7fe` (feat(cli): add --use-room-evaluation flag to generate-season)
**Season ID:** season_001010 (seed 1010, 10 classes, 2284.3s, exit 0, validation PASSED)

**V2.1 emission fields verification (non-null %):**
- `encounter_index_within_room`: 92,488/92,488 = **100%** — cycles [0, 1, 2]
- `room_won`: 92,488/92,488 = **100%** — 0 consistency violations within room groups
- `hp_fraction_at_encounter_start`: 92,488/92,488 = **100%** — enc_0=1.0 for all; range [0.002, 1.000]
- Note: 6,751 rooms have < 3 encounter rows — all room_won=0 (correct V2 early-termination behavior)
- **Gamora V2.1 emission-gap-fix (`df717a8`) CONFIRMED LIVE. No regression.**

**V2-mode calibration baseline (mean |mod-1.0|):**
- All 10 classes: **0.5994**
- Excl. wind_controller (flagged tier="review"): **0.3743** (9 classes)
- Room winrate: mean=0.494, mean |wr-0.50|=0.032 (well-centered)
- LLM cost: 368 calls, ~$0.99 (within normal band)

**Comparison to V1 baselines:**
| Cohort | Mean |mod-1.0| | Notes |
|---|---|---|
| V1 baseline (season_001005) | 0.7990 | Pre-B6, pre-V2 |
| V1 post-Day4 (season_001009) | 0.8760 | 2 FAILED classes |
| V2 season_001006 (all) | 0.4570 | wind_ctrl 3.51 |
| V2 season_001010 (all) | **0.5994** | **This regen** |
| V2 season_001010 (excl. wind_ctrl) | **0.3743** | **9 classes** |
V2-mode baseline is **better** than both V1 baselines (0.5994 vs 0.876/0.799). Even with wind_controller included, V2 is significantly better than V1.

**V2.4 migration:** Applied automatically at 2026-05-17 02:00:42 UTC. Live DB now at schema 2.4.
**V1 backward compat:** Confirmed — season_001009 rows unchanged; standard CLI behavior preserved.

**Notes for knight-rider (jack-ryan calibration analysis routing recommendation):**

1. **V2.1 emission-gap-fix is confirmed live.** Gamora's fix (`df717a8`) works end-to-end in live regen. Item 7 in star-lord's open list is now CLOSED.

2. **wind_controller structural anomaly — second occurrence.** season_001006: modifier=3.51, season_001010: modifier=3.6250. Same archetype, same V2 mode, both times. This is a confirmed structural issue (not seed-specific): wind_controller under V2 sequential HP-carryover mechanics consistently requires extreme modifier inflation. Route a gamora dispatch to investigate the wind_controller V2 room dynamics. Until this is classified, the V2 calibration epoch cannot be declared.

3. **jack-ryan calibration analysis (Tier 1 #3) routing recommendation:** HOLD until gamora classifies the wind_controller structural anomaly. Two options after gamora investigation: (a) if the anomaly is accepted as inherent (INTENTIONAL_OUTLIER V2 behavior) → route jack-ryan calibration analysis anchored on the 9 non-flagged V2 season_001010 classes (mean |mod-1.0|=0.3743); (b) if gamora's investigation yields a structural fix → re-regen V2 mode with fix applied, then route jack-ryan. Either way, the V2-mode calibration baseline is NOW established and documented in MIGRATION.md.

4. **Stage 3 cipher migration sequencing:** Unblocked per dispatch intent. This dispatch is COMPLETE. Stage 3 can proceed as next dispatch.

5. **season_001010 is the new canonical V2-mode season.** 10/10 converged, 0 FAILED, validation PASSED. Drax can use this as the reference V2 season for encounter analytics once knight-rider decides on routing.
