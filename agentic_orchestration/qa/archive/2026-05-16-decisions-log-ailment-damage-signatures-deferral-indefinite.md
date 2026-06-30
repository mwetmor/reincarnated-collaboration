# Decisions-log entry draft — Ailment-damage-signatures deferral made indefinite (post-B14.5 V1 doppelganger gate re-run HIGH signal)

**Author:** knight-rider
**Date drafted:** 2026-05-16 (Day 4)
**Source:** Gamora's doppelganger gate re-run findings at `agentic_orchestration/qa/findings/2026-05-16-gamora-doppelganger-gate-rerun.md` — HIGH SIGNAL confirmed. Routing per the open-thread `agentic_orchestration/gandalf/open-threads/2026-05-16-ailment-damage-signatures-timing-and-arpg-canon.md` Option B path.
**Process:** Knight-rider drafts → jack-ryan Gate 1 → Matt approval → commit to `reincarnated-engine/design/decisions/decisions-log.md`. Same pattern as the form-bias 5-entry batch (committed `5d51b5a`).

**Target location:** before the "Recently considered, not yet decided" section, after the 5-entry form-bias batch's cadence-option entry (last entry in `5d51b5a`).

**Companion-to:** the 2026-05-16 form-bias 5-entry batch (specifically Entry 2's "Future" framing of the ailment-damage-signatures bullet). This entry resolves the "Future" status definitively in the deferral-indefinite direction.

---

## Entry — Ailment-damage-signatures deferral made indefinite

### 2026-05-16: Ailment-damage-signatures deferral made indefinite (post-B14.5 V1 doppelganger gate re-run HIGH signal); demoted from engineering queue to design-polish queue

**Decision:** The ailment-damage-signatures design proposal (per memory note `project_ailment_damage_thematic.md`) is **deferred indefinitely**. The proposal is demoted from the engineering critical-path queue to the design-polish queue. No rocket implementation dispatch is authored; no future re-trigger gates are set unless new evidence surfaces a regression.

This resolves the "Future" status carried in the 2026-05-16 form-bias-cadence-strategy decisions-log batch's Entry 2 (three-layer model + cipher-width framework — § "cipher architecture stays operative" subsection). The "Future" framing in Entry 2 stands unchanged from `5d51b5a`; this entry adds the empirical resolution that the future revisit-trigger has now been satisfied + classified.

**Empirical basis:**

Per the memory note's § "Trigger conditions to revisit", the deferral was set with an explicit revisit trigger: "After `v1.3-b14-5-recompose-validated` tag lands, run doppelganger gate one more time with the goal of either retiring this design idea or scheduling its implementation." Signal-strength thresholds (memory note table) define the three possible outcomes:

| Signal | Pure-control archetype WR | Implication |
|---|---|---|
| **High** | 30-50% | Defer indefinitely; thematic damage solved at a different layer |
| **Medium** | 20-25% (in-band borderline) | Lift; implement |
| **Urgent** | Out of band (<20% or >60%) | Lift; immediate implementation |

**Per gamora's 2026-05-16 doppelganger gate re-run** (findings file `agentic_orchestration/qa/findings/2026-05-16-gamora-doppelganger-gate-rerun.md`), all four pure-control archetypes land squarely in the HIGH band:

| Archetype | Avg mirror-match WR | Signal class |
|---|---|---|
| wind_controller/wind | 0.487 | HIGH |
| earth_controller/earth | 0.473 | HIGH |
| fire_controller/fire | 0.393 | HIGH |
| water_controller/water | 0.393 | HIGH |

All 11 classes in the current `season_001005` roster pass the doppelganger gate (`DOPPELGANGER_BALANCED_RANGE [0.20, 0.80]`). **Pure-control fight termination rate: 0.0% across 21,600 fights** — complete reversal from the KI-B6-1 crisis state (wind_controller was 100% timeout at N=60 that triggered the deferred ailment-damage-signatures design in the first place).

**Attribution honesty (Discipline #13b):** the substrate (season_001005 classes) was generated at commit `b15ecb2`, which **predates** both rocket's B6 pre-work (`639ac3d`) and gamora's B10 V2 (`9db2f5a`). The doppelganger gate code is byte-identical between `b15ecb2` and current HEAD. The HIGH signal therefore isolates **B14.5 V1's effect alone** (the recompose-first balance loop), NOT the compound B14.5 V1 + B6 + V2 stack. **B14.5 V1's recompose-first loop is the primary driver of the resolution.**

**V2-semantic alignment (load-bearing clarification):** the doppelganger gate is inherently encounter-level — it calls `simulate_fight()` directly, not `simulate_room()`. The memory note's signal thresholds were defined against encounter-level WR, so there is **no semantic mismatch** to address. A future V2-aware room-level doppelganger gate extension is a separate small dispatch flagged but NOT triggered by this entry's resolution.

**Operational implications:**

- **Design-polish queue placement:** the proposal is preserved as a design-polish item should a player-facing build (e.g., Unity client work) surface UX concerns ("why did my knockback do nothing visually?") that aren't visible in the headless sim. Memory note's § "Other situations that could surface the need" remains operative as the secondary re-trigger condition.
- **No rocket dispatch authored.** Per memory note's HIGH-signal text: "downgrade to pure design polish." Implementation cost (~1-2 days per memory note timing) is preserved as a known quantity if the design-polish queue activates.
- **Form-bias-cadence-strategy doc § 9.1 rocket cascade item 4** ("ailment-damage-signatures (future)") and § 6.3 (cipher architecture "stays operative" bullet, amended 2026-05-16 by gandalf to "Future" framing) both **stand unchanged**. This entry resolves their "Future" status to "indefinite" without re-amending the strategy doc.
- **Discipline #12 (semantic-shifting) note:** the design proposal was originally framed as load-bearing for the doppelganger gate (per memory note + strategy doc § 6.3). Post-B14.5 V1, the doppelganger gate passes without the proposal. The load-bearing claim is therefore retired; the proposal's status moves from "deferred load-bearing dependency" to "deferred design-polish candidate."

**Reasoning:** Per gamora's empirical findings (HIGH signal across all four pure-control archetypes; 0% timeout rate; 21,600-fight sample size). The memory note's revisit-trigger framework defined the decision space at trigger-setting time (2026-05-12); the trigger has fired; the signal classifies definitively. The Matt-gandalf 2026-05-16 convergence on Option B ("re-run gate first; then decide") routed the decision to this empirical evidence; the evidence has now landed.

The cleaner-than-expected attribution (B14.5 V1 isolated as primary driver, NOT compound stack) further strengthens the resolution: the recompose-first loop architecturally dissolved the wind_controller mirror-match weakness via kit-shape adjustments rather than ailment mechanics — exactly the "different layer" the HIGH-signal memory note text anticipated.

**Alternatives considered:**

- **(a) Lift the deferral and implement** despite HIGH signal. Rejected. The HIGH-signal threshold was set in the memory note explicitly as "thematic damage is solved at a different layer; defer indefinitely or downgrade to pure design polish." Implementing against an explicitly-defined no-implementation signal would be process-incoherent.
- **(b) Keep the deferral as "Future" without resolving** (status quo from `5d51b5a`). Rejected. Leaves the form-bias batch's Entry 2 ambiguity unresolved; invites future re-litigation. Resolving definitively closes the question.
- **(c) Set a new re-trigger gate** (e.g., "revisit after B14.5 V2 lands"). Rejected. B14.5 V1's recompose-first loop dissolved the original signal; B14.5 V2 (energy-type lever) addresses a different concern (modifier compression toward calibration epoch target, per the 2026-05-16 calibration-epoch entry committed `c000d7d`). The two are architecturally distinct; coupling them would invite confusion.
- **(d) Defer indefinitely but author the rocket implementation dispatch anyway** for opportunistic execution. Rejected. The bandwidth-binding constraint on the team (per roadmap Risk 1: drax saturation across VS2a + VS2b) means commissioned-but-not-prioritized work invites scope creep. Design-polish queue placement preserves the option without committing engineering bandwidth.

**Cross-seam cascades:**

- **Rocket:** NO ailment-damage-signatures implementation dispatch. The memory note's § "Implementation cost at revisit time" (~1-2 days work) preserves the cost estimate for design-polish queue activation if needed later.
- **Gamora:** the doppelganger gate re-run (this dispatch's evidence) is COMPLETE. No follow-on from this entry. Future V2-aware room-level gate extension is a separately-flagged small dispatch (gamora's findings file flag), NOT triggered by this entry.
- **Star-lord + drax + elrond + legolas:** no cross-seam ask from this entry.
- **Jack-ryan:** the form-bias 5-entry batch's Entry 2 "Future" framing for ailment-damage-signatures is now empirically-resolved-to-indefinite per this entry; downstream dispatches treat ailment-damage-signatures as design-polish-deferred, not engineering-queue-active.
- **Gandalf:** strategy doc § 6.3 + § 9.1 framings stand unchanged. No strategy-doc amendment triggered by this entry. The ARPG-genre-implications discussion Matt-gandalf had during the open-thread Option B convergence (per `agentic_orchestration/gandalf/open-threads/2026-05-16-ailment-damage-signatures-timing-and-arpg-canon.md`) is preserved in the open-thread's CLOSED resolution section.

**Status:** Active. Resolves the form-bias batch Entry 2 "Future" status to "indefinite" definitively.

**Implementation cascade:**

- **Memory note status update** (Matt-owned per Anthropic Claude memory model): annotation suggestion at `agentic_orchestration/memory-annotations/2026-05-16-suggestion-project-ailment-damage-thematic.md` (revised 2026-05-16 post-HIGH-signal to capture the resolution).
- **Open-thread closure** (already done): `agentic_orchestration/gandalf/open-threads/2026-05-16-ailment-damage-signatures-timing-and-arpg-canon.md` Status was set to CLOSED with the Option B routing path; this entry completes that routing's final action.

**Related:**

- `agentic_orchestration/qa/findings/2026-05-16-gamora-doppelganger-gate-rerun.md` (the empirical basis — HIGH signal confirmed)
- `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_ailment_damage_thematic.md` (the deferred design proposal; § "Trigger conditions to revisit" defines the threshold framework this entry classifies against)
- `agentic_orchestration/dispatches/2026-05-16-gamora-doppelganger-gate-rerun.md` (the dispatch that produced the empirical evidence)
- `agentic_orchestration/gandalf/open-threads/2026-05-16-ailment-damage-signatures-timing-and-arpg-canon.md` (Matt-gandalf 2026-05-16 Option B convergence; CLOSED with this entry completing the routing)
- 2026-05-16 form-bias-cadence-strategy 5-entry batch (committed `5d51b5a`) — Entry 2 "Future" framing this entry resolves; § 6.3 strategy-doc amendment context
- 2026-05-16 calibration-epoch entry (committed `c000d7d`) — B14.5 V1 calibration-baseline context
- `canonical/story/form-bias-cadence-strategy.md` § 6.3 + § 9.1 (rocket cascade item 4; "Future" framings stand unchanged)
- `agentic_orchestration/memory-annotations/2026-05-16-suggestion-project-ailment-damage-thematic.md` (memory note annotation suggestion for Matt's approval)

---

## Knight-rider note (NOT for decisions-log; for jack-ryan Gate 1)

Cross-cutting questions for jack-ryan to test:

1. **Discipline #13b attribution claim — is the "B14.5 V1 isolated as primary driver" claim defensible?** Substrate provenance (b15ecb2 predating B6+V2) + gate-code-byte-identity supports the claim, but it relies on inference from "what HASN'T changed" rather than direct ablation. My read: defensible per Discipline #13b's narrow legitimate use — the inference IS the empirical isolation (no ablation needed because the substrate naturally pre-dates the candidate confounders). Confirm or push back.
2. **Discipline #12 (semantic-shifting) — is the "load-bearing retired" framing precise?** The original framing (memory note + strategy doc § 6.3) listed ailment-damage-signatures as "load-bearing for the doppelganger gate under Position (ii)." This entry says that load-bearing claim is retired given the empirical evidence. Verify the semantic shift is clean and doesn't accidentally retire load-bearing claims that should persist (e.g., if Position (ii) cipher architecture has OTHER doppelganger-gate dependencies that aren't ailment-damage-signature-specific).
3. **Alternatives section completeness** — four alternatives. Any missing?
4. **"Design-polish queue" terminology** — is this a recognized project category, or am I introducing new vocabulary? My read: gandalf's strategy doc § 9.1 used "Future" framing; "design-polish queue" is the memory note's own language ("downgrade to pure design polish"). Both vocabularies are operative; not introducing new project category. Confirm.

If all four pass with no BLOCK, this entry is ready for Matt approval and commit.
