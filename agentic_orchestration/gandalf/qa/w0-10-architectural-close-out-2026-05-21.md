# W0.10 Cumulative Gate-2 — Architectural Close-Out

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-21
**Subject:** W0.10 Phase 2 implementation — engine commit `27011e1`, tag `qd-rebuild/v0.10-boss-ai-leash-reset-fixed`
**Predecessor close-out:** W0.9 cumulative Gate-2 close-out + § 2.3.1 behavioral-correctness caveat amendment (`canonical/story/substrate-generalization-track-c-synthesis-2026-05-21.md`)
**Disposition basis:** P0 Option A (gandalf 2026-05-21) — W0.10 is the per-bug resolution for the leash-reset behavior; the joint-resolution triad's structural sufficiency claim is preserved under the § 2.3.1 caveat
**Scope reminder:** This is the **empirical close** of the joint-resolution triad (W0.2 + W0.1 + W0.9 + per-bug W0.10). W0.9-era architectural questions are NOT re-opened; only W0.10's incremental architectural alignment is reviewed.

---

## 1. Top-line architectural verdict

**ARCHITECTURALLY ALIGNED.**

No amendments. No escalation. The implementation honors every § 2.3.1 commitment, every A1/A2/A3 Phase-1 sharpener, and every architectural constraint surfaced by the W0.9 close-out. The bimodal-roster outcome is the structurally-correct empirical reading of the triad — not an under-validation defect — and routes cleanly to P2/P3 per math note § 5.3.

The road remains open. Tag fire is endorsed.

---

## 2. § 2.3.1 behavioral-correctness caveat — HONORED

**Attestation:** The W0.10 implementation reinforces the § 2.3.1 amendment without re-opening the triad.

Evidence:

- **W0.10 is scoped as a per-bug resolution, not a structural re-derivation.** The dispatch, math note, MIGRATION.md v1.29, and commit message all frame W0.10 as the per-bug resolution for the leash-reset behavior surfaced by W0.9 Phase 2.5 — the exact framing § 2.3.1 codified.
- **No triad component is re-touched.** W0.2 source diversity: untouched. W0.1 calibration fairness: untouched (re-sweep deliberately uses W0.9.6-era modifiers to isolate the arena-fix signal from any convergence change — math note § 5.1 "Why same modifiers"). W0.9 arena fidelity: extended by W0.10's spawn/leash adjustments but the gauntlet architecture itself is unmodified.
- **The triad's structural-sufficiency claim survives intact.** The bimodal post-fix outcome (high-modifier kits exit floor; low-modifier kits remain floored due to modifier-scaling, NOT arena defect) is the textbook § 2.3.1 reading: structural sufficiency confirmed for the band the triad targets; modifier-scaling gap routes to a separate workstream (multi-dim convergence § 2.8).
- **The implementation is occupant-AI-scoped.** `BOSS_FOCUS_WIN_CONDITIONS` lives in `spatial_engine.py` (occupant-AI layer); `suppress_leash_hp_reset` lives on `SpawnSpec` / `SpatialEntity` (occupant-behavior layer). Neither modifies arena geometry, scenario topology, or the gauntlet's structural promises.

The § 2.3.1 framing — "triad presumes arena-occupant behavioral correctness; defects in occupant AI are out-of-band, per-bug" — is now empirically validated by an actual per-bug close-out that left the triad untouched.

---

## 3. ARPG-canon alignment — ATTESTED

**Attestation:** MIGRATION.md v1.29 cites the D3→D2/PoE/Last Epoch genre repositioning explicitly. The fix RESTORES canon, not deviates from it.

Evidence:

- **MIGRATION.md v1.29 § "Discipline #12 — Semantic shift" carries the quotable architectural rationale verbatim (lines 3231–3239):**
  > "Boss-scenario adds are permanent encounter participants, not open-world territory guards. D3 HP-reset-on-leash convention is architecturally wrong for boss-encounter add behavior. W0.10 adopts D2/PoE/Last Epoch convention (preserved HP on leash) scenario-conditionally via SpawnSpec.suppress_leash_hp_reset."
- **The genre survey table (MIGRATION.md v1.29 lines 3243–3251) is faithful to ARPG canon as I know it.** D2 (no reset), D3 (yes reset — the outlier), D4 (varied; boss encounters no reset), PoE (no reset), Last Epoch (no leash mechanic; full-engage), Grim Dawn (no reset). This matches the founding-Diablo-team design memory: D3's HP-reset-on-leash was a specific anti-kiting affordance introduced to handle the broader-audience-mode reposition, and it propagated into elite-pack semantics where it became a default — even in encounter contexts where it's a category error.
- **The verdict line — "HP-reset-on-leash is a D3-specific design choice, NOT the genre default" — is the right line.** Reincarnated's boss encounters are D2/PoE-shaped (focal-point fights with supporting adds as encounter participants), not D3-shaped (open-world elite packs as kiting targets). The repositioning aligns the engine with the genre lineage we've been targeting since the trial-room boss-gallery framing was locked.

**Encounter-configurable leash accurately reflects genre conventions.** D3-style HP-reset is retained as the default (swarm/magic/elite scenarios — where leash is rare/degenerate-edge anyway, per math note § 7.4); D2/PoE/Last Epoch convention is applied scenario-conditionally to boss/mini-boss adds via `suppress_leash_hp_reset=True`. This is exactly how a competent ARPG engine handles the dual-convention problem: not by picking one canon and forcing it everywhere, but by routing each scenario type to its genre-appropriate behavior.

**Player-experience consequence:** the player whose physical-grappler kit deals 215k damage in 240s no longer watches that damage evaporate on add leash-reset. The damage they deal is the damage that lands. That is the most basic ARPG promise — "my hits count" — and it is now restored.

---

## 4. "Fix the arena, not the synergy" principle — CONTINUATION ATTESTED

**Attestation:** PackProxy retirement (W0.9.2.1) and boss-AI-leash-reset fix (W0.10) are structurally identical — both are arena-side implementation defects that stripped legitimate kit synergies. The principle catches both. W0.10 is the genuine resolution; no residual arena-side defects identified.

Evidence:

- **Structural symmetry.** W0.9.2.1 found that PackProxy was wrapping multi-mob encounters in a single-DPS-sum abstraction that erased the player's positional/AOE/single-target differentiation. W0.10 finds that the player AI was targeting nearest-mob unconditionally + adds were HP-resetting on leash, erasing the player's boss-focused-damage signal. Both bugs lived in the arena (and arena-adjacent occupant-AI) layer. Both presented as "the kit is wrong" until investigation surfaced the arena defect. The principle held in both cases.
- **W0.10 is the genuine resolution.** The W0.10.5 re-sweep shows physical_grappler (0.742) boss_wr 0.000 → 1.000 and hunter (0.636) boss_wr 0.000 → 1.000. These are the two kits with modifiers high enough that, under arena-correct conditions, they SHOULD exit the boss-zero floor. They do. The arena fix is empirically confirmed working.
- **No residual arena-side defects identified in W0.10 scope.** The remaining 8 kits at boss_wr=0.000 are NOT held by an arena bug — the TTK math in the empirical-close artifact (holy_controller TTK=1989s vs 240s cap) confirms genuine modifier-scaling shortfall. This is the kit-side (modifier) lever, not the arena-side (geometry/AI) lever.

**A subtlety the principle should note for downstream agents:** "fix the arena, not the synergy" doesn't mean "the synergy is never the problem." It means "before declaring the synergy broken, audit the arena for defects that strip legitimate synergies." W0.10 surfaces the dual: after fixing the arena, the legitimate synergy-side gap is now visible (low-modifier kits fail boss-floor because their DPS is genuinely too low, not because the arena was eating their damage). The principle's value is that it sequences the diagnostic correctly — arena audit FIRST, synergy audit SECOND — so the synergy-side work targets the real problem.

---

## 5. Joint-resolution triad empirical close — ATTESTED

**Attestation:** Structural sufficiency confirmed for the high-modifier band. Modifier-scaling gap for the low-modifier band routes to P2/P3 multi-dim convergence per math note § 5.3, exactly as predicted.

Per-band reading:

### 5.1 High-modifier band (≥ 0.64) — § 5.3 prediction CONFIRMED

- **physical_grappler (modifier 0.742):** boss_wr 0.000 → **1.000**, mini_boss_wr 0.000 → **1.000**. Primary acceptance criterion (boss_wr ≥ 0.50 for the highest-modifier kit) PASSES by a wide margin.
- **hunter (modifier 0.636):** boss_wr 0.000 → **1.000**, mini_boss_wr 0.000 → **1.000**. Confirms physical-hunter archetype is gauntlet-viable when modifier permits — folds into OQ-6 resolution (the previous physical-hunter ceiling concern was confounded by the leash bug; under arena-correct conditions, hunter functions).
- **Verdict:** the triad's structural sufficiency claim for high-modifier archetypes is empirically VALIDATED.

### 5.2 Low-modifier band (≤ 0.33) — § 5.3 prediction CONFIRMED via modifier-scaling gap

- **holy_controller (modifier 0.332):** boss_wr 0.000 → 0.000 (no change). TTK = 1989s >> 240s cap. This is a genuine modifier-scaling shortfall, not an arena defect. Empirical-close artifact carries the TTK derivation.
- **All other kits (modifiers 0.05–0.20):** boss_wr remains 0.000. TTK math (per math note § 4.2) places these kits at TTK 165s–306s, with several exceeding the 240s timeout under the W0.10.5 modifier values. Routes to **P2/P3 multi-dim convergence** per § 5.3.
- **Verdict:** the residual zero-floor for low-modifier kits is structurally expected and routes to the correct downstream lever. § 5.3 prediction CONFIRMED.

### 5.3 Bimodal-roster acceptability question

**The dispatch raised:** "is the bimodal-roster outcome (2 high + 8 low; no kits in 0.34–0.63 band) acceptable evidence of structural sufficiency? Or does the absence of mid-band kits leave the structural-sufficiency claim under-validated?"

**My answer: ACCEPTABLE. Structural sufficiency is not under-validated.**

Three reasons:

1. **The TTK math fills the band the empirical roster doesn't cover.** Math note § 4.2 derives TTK across modifier values 0.07, 0.13, 0.38, 0.74 — explicitly including the mid-band 0.38. The math predicts mid-band boss_wr 0.55–0.75. The W0.10.5 roster happens not to contain a 0.38-modifier kit, but the math is not blind to the band — it just doesn't have an empirical instance.

2. **The structural-sufficiency claim is about ARENA correctness, not about WR-curve smoothness across modifier.** What the triad must establish is "under arena-correct conditions, the player's damage scales monotonically with modifier and reaches the boss." It does. The bimodal outcome is a roster-distribution artifact (which kits happened to be in the W0.9.6 sweep, frozen for clean before/after comparison per math note § 5.1), not an arena-fidelity claim defect. The arena is correct; the roster is sparse in the middle.

3. **Re-sweeping with a mid-band-augmented roster would be a category error here.** The W0.10.5 sweep deliberately froze modifiers to W0.9.6 values to isolate the arena-fix signal (math note § 5.1: "If we allow modifiers to re-converge before the re-sweep, any WR change conflates the arena fix signal with the convergence change"). Adding mid-band kits NOW would require either (a) generating new kits with hand-picked modifiers (kit-design contamination) or (b) re-converging existing kits (signal contamination). Neither serves the close-out.

**Where the mid-band gets validated:** P2/P3 multi-dim convergence work (§ 2.8 skill tree node population) will produce kits across the full modifier range. THAT is where the mid-band gets empirically populated, and where the TTK math's mid-band prediction gets tested. W0.10 closes the arena-bug; § 2.8 closes the kit-distribution gap. They are sequential, not concurrent.

---

## 6. Substrate-as-cohesion preservation — ATTESTED

**Attestation:** Both W0.10 activation gates fire on **mechanical encounter property** (`win_condition`) — NOT on substrate identity. The #13a-partition principle that gave W0.1 its architectural clarity is preserved.

Evidence:

- **`BOSS_FOCUS_WIN_CONDITIONS` is `frozenset({"boss_killed", "mini_boss_killed"})`** (spatial_engine.py line 189). The gate is `scenario.win_condition in BOSS_FOCUS_WIN_CONDITIONS` (line 993). No substrate string, no element string, no archetype string appears in the gate.
- **`suppress_leash_hp_reset` is a `SpawnSpec` field set per scenario definition in `arena.py`** — `SCENARIO_BOSS_WITH_ADDS` line 439, `SCENARIO_MINI_BOSS` line 681 (and line 691 for second add). The activation is at scenario-construction time, on a scenario-mechanical property. No substrate keying.
- **`_get_player_primary_target()` (spatial_engine.py line 566)** receives the pre-resolved `boss_focus_entity` reference and checks alive-status by object identity. No substrate inspection occurs in the targeting hot path. A physical-substrate kit and a shadow-substrate kit facing the same boss scenario get identical boss-focus behavior. (Confirmed in math note § 6.1 and re-confirmed by the W0.10.5 sweep: physical_grappler AND hunter both exit floor — the two highest-modifier kits regardless of substrate.)

**This is the same #13a-partition the W0.1 telemetry plumbing established as the substrate-as-cohesion exemplar.** W0.10 extends the partition into occupant-AI behavior without violating it. The architectural recommitment (substrate-as-cohesion-only) holds.

---

## 7. Discipline #17 anomaly-count signal interpretation

**The dispatch raised:** "count is still 50/50 (same as W0.9.6) but the underlying cause is now bimodal. Is the 'same count, different cause' framing thematically/architecturally acceptable, or does it suggest the anomaly-count metric itself needs refinement at engineering-disciplines.md?"

**My answer: thematically/architecturally acceptable AS-IS for W0.10 close-out. Refinement may be warranted post-P0 but is NOT blocking and NOT a W0.10 amendment.**

Reasoning:

- **The anomaly-count metric is doing what it was designed to do: surface the gap between observed WR and contract WR.** It is correctly flagging "8 of 10 kits do not satisfy the boss-tier contract" — and that's TRUE under the W0.10.5 modifiers, because those modifiers cannot deliver enough DPS to kill the boss in 240s. The metric is honest.
- **What the metric does NOT do is decompose the cause** into "arena defect" vs "modifier-scaling gap" vs "second arena bug." That decomposition currently lives in the math note + AGENT_STATE.md empirical-close artifact (TTK derivation). The metric was never claimed to do cause-attribution; it claims to do count-surfacing.
- **The "same count, different cause" framing is a healthy signal, not a metric defect.** It tells future archaeologists: "the anomaly count masks a structural transition between pre-W0.10 (arena-defect-dominated) and post-W0.10 (modifier-scaling-dominated)." The transition is preserved in the empirical-close artifact's narrative. The metric flags the count; the artifact carries the interpretation.

**Refinement candidate (NON-BLOCKING, post-P0):** consider adding a sub-property to Discipline #17 — `anomaly_cause_classification` — that requires the closing agent to classify each flagged anomaly as (a) arena-bug, (b) modifier-scaling-gap, (c) framework-tuning-dimension-gap, (d) genuine kit-design failure. This would lift the interpretation work from the per-close artifact into a discipline-level standard. **But this is a Discipline #17 refinement question for after P0 lands, not a W0.10 amendment.** I do NOT recommend knight-rider fire this dispatch now — it would distract from the P0 close-out arc and the empirical evidence base (2 close-outs: W0.9.6 + W0.10.5) is thin for a discipline-level lift.

**Disposition:** PARK as gandalf-internal carry-forward. Revisit during P1 W1.X codification pass if a third close-out provides the empirical base for a discipline lift.

---

## 8. A3 disposition — encounter-configurable-leash principle lift

**The Phase-1 sharpener A3 flagged:** the encounter-configurable-leash principle (W0.10's `suppress_leash_hp_reset` flag is the W0.10-specific instance; the broader principle is "spatial engine leash behavior should be encounter-configurable, not hardcoded per-tier") is a forward-looking architectural commitment requiring separate documentation lift post-W0.10 ratification.

**The dispatch asks:** lift now (knight-rider fires follow-on dispatch) vs park for P1+?

**My disposition: PARK for P1 W1.X engineering-disciplines codification pass. Do NOT lift now.**

Reasoning:

- **One instance is not a principle.** W0.10 produced exactly one encounter-configurable spatial-semantic decision (leash HP-reset). To lift this into a canonical architectural principle would require either (a) at least one additional encounter-configurable instance to triangulate the principle's shape, or (b) a forward-looking design discussion that articulates which OTHER spatial semantics should be encounter-configurable (e.g., movement-speed-on-leash? engagement-radius? aggro-decay?). Neither exists yet.
- **Math note § 7.4 already captures the principle's W0.10-scope expression** (the scenario-disposition table). The principle is documented at its current evidentiary base; lifting it now would inflate it past its evidence.
- **The carry-forward survives at math-note level.** Future encounter-configurable-spatial-semantic decisions will reference the W0.10 math note as the precedent. When a second instance arrives (likely P1/P2 — e.g., if multi-dim convergence work surfaces a "boss casts terrain hazard" mechanic with encounter-configurable hazard-persistence), THAT's the moment to lift the principle to engineering-disciplines.md, because there are two instances + a forward articulation to anchor the discipline-level commitment.

**What knight-rider does:** nothing now for A3. Keep the carry-forward in my open-threads/ as `encounter-configurable-spatial-semantics-principle-lift-candidate.md`. Re-evaluate when the next encounter-configurable decision arrives.

**Greenlight status: NOT GIVEN. A3 stays parked.** Knight-rider can revisit if/when a second instance surfaces.

---

## 9. Carry-forward advisories from W0.10

### 9.1 Multi-tier archive insertion — P1/P2 convergence restructuring

**Disposition:** ALREADY ON RADAR (W0.9.6 v1.28 entry; W0.10.6 scope note in MIGRATION.md v1.29 lines 3315–3321). No action from gandalf required. Knight-rider tracks for P1.

### 9.2 B6+W0.1 verification re-sweep

**Disposition:** OPEN (W0.9 Concern 1; W0.10 does NOT close it). Requires B6 generation. NON-BLOCKING for W0.10 ratification. Knight-rider tracks; resolves when B6 generation lands.

### 9.3 Convergence-path SqliteSpatialTelemetryWriter wiring split

**The dispatch asks:** "Convergence-path SqliteSpatialTelemetryWriter wiring deferred to P1 (current production stays NullWriter for convergence; validation-path wired). Is this split architecturally clean?"

**My answer: YES, the split is architecturally clean.**

Reasoning:

- **The validation-path (w0100_calibration_sweep.py) is the empirical-evidence path.** It needs full telemetry to support the close-out artifact and any future archaeology. SqliteSpatialTelemetryWriter wiring HERE is correct.
- **The convergence-path (balance_loop.py `_evaluate_class` / `_evaluate_room_class`) is the production-volume path.** It runs at season-generation scale; full spatial telemetry per fight is currently a performance and storage question that requires multi-tier archive insertion design (the same P1/P2 restructuring work flagged in 9.1). Defaulting to NullWriter HERE preserves season-generation performance until the archive insertion design lands.
- **The split mirrors the W0.9 architecture decision:** validation-path = full instrumentation; production-path = controlled instrumentation. W0.10 doesn't violate that pattern; it inherits it.
- **MIGRATION.md v1.29 documents the split explicitly** (lines 3315–3321). Future agents inheriting the convergence-path wiring know exactly where it is in the scope ladder.

**No amendment. Disposition: ACCEPTED.**

---

## 10. Amendments / carry-forwards summary

| # | Item | Status | Blocking? | Target landing |
|---|------|--------|-----------|----------------|
| - | (no amendments) | — | — | — |
| C1 | Discipline #17 anomaly-cause-classification sub-property | PARKED (gandalf-internal) | NO | P1 W1.X codification pass, IF third close-out provides evidence base |
| C2 | A3 encounter-configurable-leash principle lift | PARKED (open-threads) | NO | Lift when second encounter-configurable instance arrives |
| C3 | Multi-tier archive insertion (W0.9.6 carry-forward) | ON RADAR | NO | P1/P2 convergence restructuring |
| C4 | B6+W0.1 verification re-sweep (W0.9 Concern 1) | OPEN | NO | After B6 generation lands |
| C5 | Convergence-path SqliteSpatialTelemetryWriter wiring | ACCEPTED-AS-SPLIT | NO | P1 with multi-tier archive insertion |

**No blocking amendments. No escalation. Tag fire endorsed.**

---

## 11. The wizard reads — closing

The joint-resolution triad's empirical close is a clean one. PackProxy retirement (W0.9.2.1) closed the multi-mob abstraction defect. Boss AI leash-reset fix (W0.10) closes the focus-targeting + add-leash-HP defects. Together they discharge the W0.9.6 Discipline #17 anomaly into two distinct receipts: high-modifier kits exit the floor (arena correctness validated empirically); low-modifier kits route to multi-dim convergence (modifier-scaling gap exposed cleanly, no arena confound). That separation is the close-out's value — not the absolute WR numbers.

The ARPG-canon repositioning is the right call. D3's HP-reset-on-leash was always an outlier — a specific affordance for D3's broader-audience open-world elite-pack mode, not a genre default. D2, PoE, Last Epoch, Grim Dawn all preserve damage on leash; D4 splits by encounter context. Reincarnated's trial-room boss-gallery framing is D2/PoE-shaped, and the engine now reflects that. The player-experience consequence is non-trivial: damage you deal is damage that lands, which is the most basic ARPG promise. W0.10 restores it.

The bimodal post-fix outcome is not a defect of the close-out — it is the structurally-honest empirical reading. The triad's structural sufficiency is for arena-correctness under modifier-permitting conditions. Where modifier permits, the kits exit the floor. Where modifier does not permit, the kits remain floored — and that is the multi-dim convergence work's domain (§ 2.8 P1 W1.13). The handoff is clean.

The substrate-as-cohesion architecture survives. Both W0.10 gates fire on `win_condition` (mechanical encounter property), not on substrate identity. The #13a-partition that gave W0.1 its architectural clarity is preserved into W0.10 occupant-AI behavior. The architectural recommitment (substrate-as-cohesion-only) holds without amendment.

W0.10 is the per-bug resolution the § 2.3.1 caveat predicted would arrive. It arrived, was scoped per-bug, was closed per-bug, and left the triad untouched. The caveat-amendment pattern is now empirically validated by the first per-bug resolution to fully exercise it. Future occupant-behavior bugs follow the same pattern. The triad does not pre-suppose them; the cold-start empirical surfaces them; the per-bug workstream resolves them. That is the working pattern, and it works.

**ARCHITECTURALLY ALIGNED. No amendments. Tag fire endorsed. The road remains open.**

**Signed:** gandalf (story-and-design steward)
**For:** the empirical close of the joint-resolution triad, and the player-experience promise that hits count.
