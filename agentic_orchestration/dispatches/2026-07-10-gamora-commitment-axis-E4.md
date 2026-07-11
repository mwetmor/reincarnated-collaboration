# Dispatch — gamora: Commitment-axis (E4) — sim consumer (cast-state machine + pricing measurement + regime-mix cert)

**From:** knight-rider → **To:** gamora (simulation seam)
**Date:** 2026-07-10
**Pattern:** B (multi-hour cross-seam build; math-before-code) — **Gate-1 (critique pair: jack-ryan + gandalf) REQUIRED before fire**
**Authority (ONE build authority — note + addendum together):**
1. `agentic_orchestration/gandalf/notes/2026-07-10-e4-commitment-axis-design-note.md` — all six 2026-07-09 forks RULED.
2. `agentic_orchestration/gandalf/notes/2026-07-10-e4-runtime-interaction-and-pressure-addendum.md` — F-0/F-1(b)/F-2(b)/F-4/F-5(a) RATIFIED; F-3 ADOPT+DEFER. Where the addendum extends the note, **the addendum governs**.

Surface-ledger **E4**; roster row **H6**. Fourth axis of the full-spec main line (E1→E2→**E4**→E3).

**Status:** FIRE-READY (PHASE 1) — Gate-1 critique pair PASS. gandalf **CONCUR-WITH-AMENDMENTS** (all folded: §6 flatten/none non-flip + fight-completion floor, §2.3 drain honor-as-emitted); jack-ryan **PASS-WITH-AMENDMENTS** (all folded: §0 fight-completion co-sign, §7 round-trip FAIL condition, §10 §E.14, §12 shared-MIGRATION ownership). PHASE 1 (math-note co-sign) cleared to execute NOW; **PHASE 2 (sim BUILD) fires on the open pilot completion-build landing** (§0 serialization law).

**This is the SIM-CONSUMER half of a rocket + gamora PAIR.** Companion dispatch: `2026-07-10-rocket-commitment-axis-E4.md` (emitter + math-note lead). The two build against ONE shared math note and ONE versioned packet contract (ADR-004 MIGRATION.md at the seam).

---

## 0. ⛔ SEQUENCING LAW — read this FIRST (KR-orchestrated, non-negotiable)

**The gamora seam is the serialization point — not the sessions.** Two phases with different timing:

- **PHASE 1 — math-note CO-SIGN (overlaps the open pilot session SAFELY, fire NOW-eligible on Gate-1 PASS):** rocket LEADS the shared math note `generation/math/commitment-axis-e4-2026-07.md`; **you co-sign the consumer half** — whiff-resolution semantics, channel-lock, the cast-state-machine params you will consume, the forced-break threshold form, the telemetry field list, and **the fight-completion-ceiling check (≥2 completed casts of the slowest modulated skill in a representative gauntlet fight)** — a **sim-measured** constraint (rocket's note asserts it; only your instrument produces it) that the pricing loop consumes (Disc #1). This is derivation, not sim code; it does not touch the pilot's in-flight files.
- **PHASE 2 — the E4 sim BUILD (QUEUES BEHIND the pilot completion-build landing):** your cast-state-machine + tick + forced-break + pilot-floor + regime-matrix + telemetry code queues **behind** the open pilot session's in-flight work landing: **arm plumbing w4g1/w4g2/w5g1 + the Leg-i two-arm driver**. **Do NOT interrupt, re-task, or close the open pilot KR session** — it finishes its completion-build, feed-2 hook, and jack-ryan §2 ratification independently. When the pilot build lands, PHASE 2 unblocks.

**No pair code (yours OR rocket's) fires before the shared math note closes (Disc #1).** The pricing loop is the coupling point: **you measure completion/whiff rates → rocket prices the premium from them.** ONE math-note conversation.

## 1. Why this axis exists (design note §0, §5)

`cast_time_seconds` is emitted today but **never read** — cadence derives from `cooldown_seconds` alone (`spatial_engine.py` readiness gate); damage applies instantly at cast. E4's build is a PAIR precisely because the coordinate is inert without a NEW sim consumer. Your half makes the commitment REAL: a wind-up genuinely whiffs against a target that moved; a channel is genuinely position-committed and genuinely breakable under pressure; the premium rocket prices is priced against **risks your instrument actually expresses**. If your instrument's risks are fake, the premium is fiction (addendum §C.1 — both failure signs).

## 2. Target seam + the changes (addendum §B, §C)

**File:** `simulation/spatial_engine.py` (yours) + telemetry emission at the sim→star-lord boundary.

### 2.1 Cast-state machine — the new sim primitive (addendum §B.1)
One actor-level state machine, two live configurations + one degenerate:
- **wind-up:** `idle → committing(cast_time) → resolve-at-completion` — damage resolves against world positions **AT completion** (motion-whiff law).
- **channel:** `idle → channeling(tick loop) → released | broken | exhausted` — per-tick resolution.
- **snap:** degenerate (no state; current behavior).
Integration points: the **readiness gate** (`action_available_at`, `spatial_engine.py:1281`) gains a **busy-state**; the **behavior branch** (kite/reposition logic `:1052-1173`) **SUSPENDS while committed under `rooted` policy** — this is what makes lock-opportunity-cost mechanically real: a rooted channeler stops kiting, and the sim's kiting is real, so the exposure is real.

### 2.2 Tick system — channel (addendum §B.2)
Damage applies per tick; **each tick resolves against positions at tick time** (extends motion-honesty from completion-instant to the tick train — a beam tracks, a ground-tether doesn't; the packet declares which). `tick_interval_seconds` per the math-note-derived value in band **[0.25, 0.5] s**. Per-tick damage share from the k-aware period model.

### 2.3 Drain + pay-on-commit economics (addendum §B.3)
Channel pays per tick (`drain_rate`/s); wind-up + snap pay on commit; a whiffed wind-up **forfeits the resource** (no refund). Sustain window = pool ÷ net drain (a NATURAL duration bound — no artificial max). `drain_rate` **arrives parameterized per (economy bin, `k`)** from the math note — **honor it as-emitted; do NOT re-derive sim-side** (re-derivation is a seam drift). **Honor the economy-coupling guard:** overflow×channel drain must BIND; starved×channel = double-starve (low sustain uptime is the identity, flagged).

### 2.4 Move-while-channeling policy (addendum §B.4)
Consume `move_policy ∈ { rooted | walk(pct) | full_move }`: **rooted** suspends the behavior branch; **walk** scales `movement_speed`; **full_move** leaves it untouched (spin class — the B12 re-cert target + the dodger×channel resolution).

### 2.5 Break rules (addendum §B.5)
Voluntary release (free, any tick boundary); wind-up move-cancel (legal, forfeits cast + committed cost, no refund); **forced-break (§2.6)**.

### 2.6 Forced-break RULE v1 (F-1(b) RATIFIED — addendum §C.2)
Cumulative incoming damage **≥ Y% max-HP within window W** forces a channel break → ramp/stage reset (F-2b) + short recovery lockout (0.3–0.5 s) + no refund of the broken tick. **Y and W come from the shared math note (Disc #17 calibrated).** ONE rule — **NOT a poise/stagger system.** **Stagger UX is v1.1 presentation, NOT this pair.** Wind-up stays **un-interruptible at v1** (its priced risks — whiff + truncation + move-cancel forfeit — are already real once regimes are honest; adding interrupt without the full stagger design double-charges the bin).

### 2.7 Whiff resolution at cast-completion
Wind-up damage resolves against world positions **at completion time** — wind-ups genuinely whiff against targets that moved. Fight-truncation kills in-flight casts (already real). Channel-lock exposure is real via §2.1 branch suspension.

## 3. Pilot-competence floor v1 (F-competence — addendum §C.4; criterion 18) — the counter-direction threat

The action policy today optimizes fastest-cycling under kills-only timeout semantics (`spatial_engine.py:1265-1337`) — it is **commitment-blind**. This is the **mis-pricing threat**: a dumb pilot initiates wind-ups against departing targets → pessimistic completion rates → inflated premium → over-banded the moment a competent player pilots the kit. v1 floor:
- **initiate wind-up ONLY when the target's projected position at completion is inside the template** (the sim has positions AND velocities — one extrapolation);
- **hold channel until drain exhaustion, threat threshold, or target death** — no frivolous release.
Cert measures the kit at a **COMPETENT baseline, not an idiot one.** **Deliverable (criterion 18): report the delta in measured completion rates vs the blind pilot** — the calibration-honesty receipt.

## 4. Three-honesty-axes regime matrix (guard-2 extended — addendum §C.3; criterion 17)

The pricing loop calibrates premiums against MEASURED risk; the cert regime matrix MUST contain **≥1 regime per honesty axis**, or the corresponding premium is uncalibrated. The substrate ALREADY EXISTS in the sim — this is a **regime-matrix composition requirement**, not new machinery:

| Honesty axis | Regime property (already in sim) | Prices |
|---|---|---|
| **Mobility** | targets that reposition (kite/hit-and-run, `spatial_engine.py:1134-1173`) | wind-up whiff rate |
| **Lethality** | incoming damage that genuinely threatens (deaths + HP<50%-timeout losses, fitness-visible) | channel lock exposure + forced-break rate |
| **Attrition** | fights long enough that sustain windows bind (60–240 s scenarios) | drain economics |

The pricing loop consumes rates measured **across all three**. (Guard 2 as LAW: pricing measured only against stationary targets is dishonest and reopens Matt's spiky-caster over-reward concern.)

## 5. Telemetry (addendum §C.5; criterion 16) — the pricing loop's inputs

Per **(kit, commitment_bin, regime)**: `completion_rate`, `whiff_rate`, `damage_taken_while_committed`, `forced_break_count`, `move_cancel_count`, `drain_exhaustion_events`, `sustain_uptime`. **These ARE the pricing loop's inputs — guard 1 (risk-priced premium) is unimplementable without them.** star-lord is the downstream consumer of the telemetry-schema addition (note in MIGRATION.md; do not draft star-lord's work).

## 6. Regime composition — three-honesty-axes cert matrix (criterion 17)

The cert gauntlet must demonstrably carry **≥1 mobility + ≥1 lethality + ≥1 attrition** regime AND the cert record's regime composition must carry **≥1 mobility + ≥1 lethality + ≥1 attrition** for every certified kit (the honesty-axes law applies to the cert matrix itself). Capstone `invert` kits certify at the **EXPRESSED coordinate** (declaration-vs-measured mismatch = cert FAIL — substrate votes; the cert record carries native + post-T4 expressed, design note §1.5). **The three amplitude_delta declarations differ at cert:** `invert` FLIPS the expressed coordinate (spiky→flat); **`flatten`/`none` do NOT flip it** — cert confirms the *declared* delta whichever of the three it is, never assumes `invert`.

**Fight-completion floor (a sim-only guard — G-A4):** cert asserts the **slowest modulated skill completes ≥2 casts in a representative gauntlet fight**, else the kit is flagged **dead-slot**. This is the guard against a wind-up that prices fine but never fires — only your instrument can see it (rocket's math note asserts the ceiling; your cert measures it).

## 7. Cross-seam contract (ADR-004) — MIGRATION.md (shared with rocket)

You CONSUME the versioned packet contract fields rocket emits (cast-state-machine params, tick_interval, drain/pay-on-commit, move_policy, break rules) and you ADD a telemetry-schema addition (§5) at the sim→star-lord boundary. **The pair's MIGRATION.md** (rocket-authored at the emitter seam; you co-author the sim-consumer + telemetry sections) documents both. **Round-trip clause MANDATORY** (Principle 6): a production-path fixture exercising the emitter→sim boundary with field-presence checks (rocket's round-trip §10 emits K1/K7/K19 + an invert kit; your side consumes them without a contract mismatch and produces the telemetry fields — **FAIL if any mechanical field rocket emits is absent, mistyped, or unconsumed at the sim boundary, or if a consumed value round-trips to a different number than emitted**).

## 8. Perf bound (criterion 19) — HARD gate

Instrument throughput **≥30 fights/s** with the cast-state machine + ticks live. **Baseline 36; regression >17% BLOCKS.** The tick_interval floor [0.25 s] exists to protect this instrument — do not let per-tick resolution collapse throughput. Report measured fights/s before/after.

## 9. #2-FF fields (MANDATORY)

- **Verdict-rendering instrument named:** the completion/whiff telemetry over the three-honesty-axes matrix + the blind-vs-competent pilot delta report + the perf-regression measurement.
- **One-command pre-fire verification exercising the PATH:** e.g. a single command confirming `cast_time_seconds` is emitted-but-unread pre-change (the inert state you are activating — cadence derives from `cooldown_seconds` at `spatial_engine.py` readiness gate). State the expected post-change first-log line (e.g. "K1 wind-up: completion_rate=X in mobility regime; whiff_rate=Y; forced_break_count=Z; fights/s=W ≥30").
- **Precondition state cited:** design note + addendum; surface-ledger E4; the open pilot completion-build landing (PHASE-2 unblock signal); E2 landed (`d99635a`); E1 landed (`bfc94eb`).

## 10. Acceptance criteria (design note §3 (3,5,7,8,12) + addendum §E (13–19) — sim-side share)

- **§3.3** cast_time READ; three v1 risk components mechanically present; completion/whiff telemetry per (bin, regime).
- **§3.5** regime-mix cert; pricing derives ONLY from the certified mix.
- **§3.7** capstone transform: expressed-coordinate cert path (declaration-vs-measured mismatch = FAIL); cert record native + expressed.
- **§3.8** channel consistency (one channel mechanic; divergence cert-blocking).
- **§3.12** report measured KPM deltas; do NOT re-anchor bands (the ONE post-E3/E4 Matt-gated re-anchor absorbs them).
- **§E.13** cast-state machine + per-tick position resolution; readiness gate + behavior-branch suspension integrated.
- **§E.14** drain consumed k-aware AND economy-aware; overflow-binding honored in the tick loop (drain_rate honored as-emitted per §2.3, not re-derived).
- **§E.15** move-policy enum honored; spin class certifies under `full_move`.
- **§E.16** v1 forced-break rule implemented + calibrated (Disc #17); telemetry fields land with it.
- **§E.17** three-honesty-axes regime matrix; pricing consumes rates across all three.
- **§E.18** pilot-competence floor; blind-vs-competent completion-rate delta report.
- **§E.19** perf ≥30 fights/s; regression >17% blocks.

**Tag (yours, sim consumer):** `gamora/v<X.Y>-commitment-axis-4` (seam prefix — intermediate; Matt approves any prefix drop).

## 11. Explicitly OUT OF SCOPE (prevents scope creep)

- **The emitter half** — coordinate, packet-contract emission, premium pricing, coupling enforcement at the sampler, capstone declaration: **rocket's half.** You consume the fields + measure the rates rocket prices against.
- **Interrupting the open pilot session** — see §0. PHASE 2 queues behind its landing; do not touch its files.
- **stagger / poise / player-facing interrupt UX** — v1.1 named re-entry; v1 is the forced-break RULE only.
- **wind-up damage-interrupt** — wind-up stays un-interruptible at v1.
- **band re-fit / re-anchor** — the ONE post-E3/E4 Matt-gated re-anchor; report deltas, do NOT re-anchor.
- **E3 (hybrid dual-scaling)** — own design pass, queued.
- **B12 spin-channel re-cert** — downstream (fires at pair-landing → G3 zero-diff audit); note in MIGRATION.md, do not draft.
- **QD ninth-axis (F-3)** — deferred; build against the 324→972 catalog space.

## 12. FLAGGED — pending KR+Matt decision (do NOT resolve)

**Batch-2 sample-vs-pin `bc_commitment` fork** (design note §4) — named KR+Matt sequencing decision; flag in the **shared MIGRATION.md (rocket-authored)** as pending, do NOT resolve (single flag, single author — no double-flag). Composes with the standing K9 coordinate-drift reconcile.

---

**Required reading (gamora, at session start):**
1. This dispatch — ESPECIALLY §0 sequencing law.
2. `agentic_orchestration/gandalf/notes/2026-07-10-e4-commitment-axis-design-note.md`.
3. `agentic_orchestration/gandalf/notes/2026-07-10-e4-runtime-interaction-and-pressure-addendum.md` (§B, §C, §E).
4. `2026-07-10-rocket-commitment-axis-E4.md` — the companion emitter dispatch (co-sign the shared math note against it).
5. The open pilot session's in-flight dispatch(es) — to know the PHASE-2 unblock signal (arm plumbing w4g1/w4g2/w5g1 + Leg-i two-arm driver landing), NOT to touch them.
6. `canonical/current-to-end-state/surface-ledger.md` — E4 row.

**Sign-off:** knight-rider, 2026-07-10 (FIRE-READY — Gate-1 critique pair PASS, all 10 amendments folded). PHASE 1 cleared NOW; PHASE 2 fires on the pilot completion-build landing. The player only ever feels what the sim already paid for.

---

## KR PHASE-2 GO RECORD — 2026-07-11 (knight-rider, fresh session)

**PHASE 2 (the E4 sim BUILD) is FIRED.** §0 serialization law RESOLVED and slot call made. Gate verification this session:

1. **Pilot completion-build landed** — `a63aae2` + Gate-2 PASS (released via Q13), 2026-07-08 (confirmed in the pilot close record).
2. **§0 unblock signal present (verbatim)** — `canonical/current-to-end-state/current-to-end-state-engine.md` 2026-07-11 delta: *"pilot session CLOSED → E4 PHASE-2 unblocked"*. The pilot session stewardship ended; the two-arm driver + per-axis model + `pilot_policy` rider persist as the standing instrument.
3. **PHASE-1 co-sign landed** — `56e1eb4` (E4 commitment-axis math note, consumer half) in engine `main`.
4. **Gamora slot FREE (KR slot call)** — no gamora unit in flight: pilot session closed; the F5 cost-TYPE math-note unit (relay Prompt 3) is NOT fired. Per the fire-order rule (Prompt 2 vs Prompt 3 both gamora-seam, one unit at a time), **E4 PHASE-2 goes first.** F5 math-note serializes behind PHASE-2's landing.

**On return:** jack-ryan **Gate-2** on the build (BLOCK authority). Shared MIGRATION.md (rocket-authored emitter half; gamora co-authors sim-consumer + telemetry sections) required before tag per ADR-004. Tag: `gamora/v<X.Y>-commitment-axis-4`.

**Downstream note (dispatch record):** the **ninth-axis (QD/F-3) measurement half (ii) unblocks when PHASE-2 lands.** Deferred until then; build against the 324→972 catalog space (§11 out-of-scope holds until the unblock).

**Fired by:** knight-rider, 2026-07-11.

---

## Completion record
**Completed:** 2026-07-11
**Phase:** PHASE-2 (the E4 sim BUILD) — math-before-code satisfied (shared math note CLOSED + §13 co-sign; consumer note `simulation/math/commitment-axis-e4-sim-consumer-2026-07-11.md`).
**Tag shipped:** `gamora/v1.5-commitment-axis-4` (seam prefix; NOT pushed — KR owns push per ADR-006).

**What landed (sim consumer half):**
- NEW module `simulation/spatial_gauntlet/commitment_state_machine.py` — [M] packet parse + ramp + pilot-floor projection (motion-model forward-integration, NO velocity field) + forced-break ring. Unit-testable.
- Engine integration in `spatial_engine.py`: `_e4_service_commitment` / `_e4_initiate_commitment` / `_e4_pay_and_cooldown`; action-phase interception; `_PosProbe`/`_point_in_template`/`_channel_fixed_hits`; `damage_scalar` on `_apply_skill_damage` (channel ramp, identity at 1.0); move-policy at nav branch (rooted/walk/full_move); ring-push + `damage_taken_while_committed` at the player-hp site; seven telemetry producer fields on `SpatialFightResult`. `WIRE_COMMITMENT_AXIS` kill-switch + `e4_blind_pilot` A/B toggle.
- Consumed AS-EMITTED (NO re-derivation): `commitment_premium`, `drain_rate`, `tick_interval`, forced-break Y/W/lockout, ramp, `move_policy`, `tick_tracking`.

**Smoke results:** `simulation/notes/e4_commitment_sim_consumer_smoke_2026_07_11.py` — RT + BI + PF + WU + CH-lethality + CH-drain ALL PASS (round-trip [M] consumption/identity; snap degenerate; projection tracks motion model; motion-whiff real c_wind=0.875; 16 forced-breaks + 56K lock exposure; 78 drain-exhaustion + sustain_uptime→0). C18 + PERF reported.

**Byte-identity guard (dispatch load-bearing) — PROVEN:** A/B harness `simulation/notes/e4_byte_identity_ab_2026_07_11.py` — golden captured on PRE-E4 tree (git-stash), **12/12 (kit,scenario) cells byte-identical** on the E4 tree (production path, real seed-57000000 kits). Snap-grade population unchanged by construction. ONE-COMMAND A/B in the harness docstring.

**Perf gate (criterion 19) — PASS:** 41.0 fights/s (E4) vs 40.0 (pre-E4 baseline) = −2.5% (≥30 floor; ≤17% gate).

**Criterion 16 (telemetry):** LANDED — seven producer fields (`completion_rate`, `whiff_rate`, `damage_taken_while_committed`, `forced_break_count`, `move_cancel_count`, `drain_exhaustion_events`, `sustain_uptime`) on `SpatialFightResult`, additive-defaulted, brownfield-safe.
**Criterion 17 (regime matrix):** demonstrated in the smoke — mobility (kiting mobs → whiffs), lethality (boss_with_adds → forced-breaks + exposure), attrition/drain (bound pool → exhaustion). The cert-matrix composition requirement is documented in the consumer math note §6.
**Criterion 18 (pilot floor / blind-vs-competent):** A/B mechanism wired + runs; competent arm cancels doomed casts (active floor), blind arm rides everything out (distinct behaviors — a `_e4_blind` clobber-bug was found + fixed during the simplify review). Δc_wind signal lands in the production RANGED-mobility cert; the melee-close smoke shows Δ≈0 by regime with the projection logic proven via the PF unit check.

**MIGRATION.md written:** YES — shared doc `generation/MIGRATION.md` (CONSUMER IMPACT — gamora section marked LANDED) + sim producer-contract entry `simulation/MIGRATION.md` [2026-07-11] E4. **star-lord follow-on noted** (DB columns + `_INSERT_SQL` widen + schema bump + pricing-loop join — NOT drafted). **B12 spin re-cert noted** (full_move consumed; substrate ready). **Batch-2 sample-vs-pin `bc_commitment` fork FLAGGED PENDING** (KR+Matt; primary flag in generation MIGRATION, sim cross-ref) — NOT resolved.

**Notes for jack-ryan Gate-2 review:**
- Byte-identity is the load-bearing claim: A/B harness proves it 12/12 on the production path (real resolver-mitigated damage, not projection). The snap path adds one no-op method call + one `read_commitment` parse per tick; perf −2.5% confirms negligible.
- Semantic shift (Disc #12) DECLARED in code + math note §2.1: `action_available_at` gains a BUSY-state meaning during commitment (readiness = cooldown-elapsed AND not-committed AND not-locked-out). Framed, not buried.
- `damage_scalar` on `_apply_skill_damage` is multiply-by-1.0 on every pre-E4 call (exact IEEE-754 no-op → byte-identity holds); the channel ramp is the only caller that passes ≠1.0.
- Two PRE-EXISTING regression sets are OUT of the sim seam (confirmed by stashing E4): 4 llm/naming vocab-path collection errors (missing collab doc) + 6 generation-seam `test_cycle13_wave5` cell-grain contract errors (rocket's pipeline). Routed to KR.
- NO push (KR owns). NO band re-fit/re-anchor (deltas reported; the ONE post-E3/E4 Matt-gated re-anchor absorbs them).

**Completed by:** gamora, 2026-07-11.
