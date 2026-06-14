# Finding — 2026-06-14 — gamora-bc-coordinate-cutover-stage-2 (DEV-MODE Gate-2, MATH-NOTE gate, pre-implementation)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-AMENDMENTS — WARN-1 (outcome-equivalence criterion needs two tightenings before it is sufficient gate evidence), plus INFO amendments. No BLOCK.
**Target:** math note `simulation/math/bc-coordinate-cutover-stage-2-ai-bin-keying-2026-06-14.md` @ commit `c29599b` (NOT pushed)
**Developer:** gamora
**Principles applied:** 1 (math-before-code), 3 (cross-seam MIGRATION), 4 (decisions-log/contract truth), 6 (cross-seam round-trip)
**Disciplines cited:** #1, #7.8 (one-variable / behavior-preserving), #12 (semantic-shift), #39 (no silent stub fallback / Pattern P7)
**Design contract:** gandalf §7.5/§7.6/§7.8/§7.9 (gandalf reviews the design half in parallel; this finding is process/discipline only)

## Verdict (one line)

The math note is implementable, smuggling-trap-clean, tri-state-clean, and demote-not-delete-clean. I independently verified at source every load-bearing empirical claim it makes about the Stage-1 bin emissions and the keying sites — all hold. The one substantive process gap is in the gate-EVIDENCE rigor: the outcome-equivalence criterion (§3.1) is the right idea but, as written, has two holes through which a real regression could hide. Both are fixable in the criterion text before implementation; neither blocks authoring Unit 2.

---

## What I found

I verified the note's mechanism at source rather than trusting its self-report. The smuggling trap is genuinely avoided: §2.1/§2.3 derive role ordering as a pure function of `ctrl_bin`/`eng_bin`/`tempo_bin` (+ `geo_bin`/`var_bin`/`def_bin` proxies), never computing the legacy label from the coordinate and never reading `archetype` or element/substrate — and §2.5 explicitly forbids the element re-coupling that would re-introduce the Phase-5-deferred disease at the instrument. The keying sites the note names (`_PLAYER_CONTROLLER_ARCHETYPES` membership at `_common:292`; `ARCHETYPE_ROLE_PRIORITY[archetype]` via `get_priority_roles`) match source exactly, as does the `from_player_class:730` propagation point and the `preferred_behavior` non-label lever it promotes. Every empirical bin-emission claim the note rests its equivalence argument on is confirmed against `bc_target_source.py`: damage→`damage-pure` / control→`control-pure` (`_ROLE_CTRL`), all-mana→`tempo=medium` (`_ENERGY_TEMPO`, so tempo is honestly flagged as non-discriminating within the 16), and the bc-collapse of water/earth/holy at long range (element nudges only `var_bin`/`geo_bin`/`def_bin`, never a rotation-identity axis — so the three DO collapse to one coordinate, exactly as §2.6 claims). The tri-state (§4) is a genuine three-state with a loud-WARN unkeyable path, not a collapsed binary. The note correctly scopes Stage 3 deletion out and rules A3 separate. The single weakness is the equivalence CRITERION's coverage, addressed below.

## SMUGGLING-TRAP — independently CLEAN (the structural check)

This was the primary thing to catch and the note catches it itself, correctly:
- §2.1 names the forbidden pattern verbatim (`bins → label → ARCHETYPE_ROLE_PRIORITY[label]`) and §2.3 specifies a direct `bc_target_role_priority(bc_target) -> list[str]` keyed on bins only.
- §2.2 resolves the dispatch's open question to option (b) — direct bins→role-priority — with a sound rationale: routing through the 6-value `_PREFERRED_BEHAVIOR_ROLES` monster enum would re-quantize the player space through a monster vocabulary and LOSE per-axis discrimination. I concur. I confirmed `_PREFERRED_BEHAVIOR_ROLES` is a 6-value monster-scripting map (`ai_strategies.py:204`); forcing players through it is genuinely lossy.
- §2.5 forbids reading `CombatantState.substrate` (which IS available at the site — `substrate=getattr(player_class,"dominant_element","physical")` at `from_player_class`). This is the one place the disease could quietly re-enter; the note pre-empts it. Good.

**One implementation-phase watch-item (INFO-1, not a math-note gap):** the note says the map "plays the role `preferred_behavior` plays for monsters (a non-label override)" but must NOT route through the literal `preferred_behavior` field/`_PREFERRED_BEHAVIOR_ROLES` path. At `choose_action` the monster `preferred_behavior` branch is gated `combatant.ai_strategy=="scripted" and not combatant.is_player` — players are `is_player=True, ai_strategy="common"`, so they never hit that branch today. The new player bin-keying must enter at `_common` (the control gate at `:292`) and at `get_priority_roles`, NOT by setting `combatant.preferred_behavior` on a player. Gate-2 of the IMPLEMENTATION will verify the player path does not borrow the monster `is_player==False` branch. Flagging now so the wiring is right the first time.

## TRI-STATE (Disc #12) — CLEAN, not buried

§4 frames the routing as a strict three-state table: PRIMARY (`bc_target` present → bins) / FALLBACK (`bc_target` absent AND `archetype ∈ ARCHETYPE_ROLE_PRIORITY` → legacy table unchanged) / LOUD-DEFAULT (`bc_target` absent AND archetype unknown → `log.warning` + `_REGISTRY_DEFAULT_PRIORITY`). The present-vs-absent distinction is NOT collapsed to a silent default, and the semantic-shift is called out per Disc #12 with the commit-message + decisions-log obligation named explicitly. This is exactly the framing the dispatch demanded. The LOUD-DEFAULT path matches the existing Pattern-P7 precedent already live in `get_priority_roles` (the unknown-archetype WARN + `_REGISTRY_DEFAULT_PRIORITY` fall-through at source), so Disc #39 is satisfied by reusing an established loud-fail, not inventing a silent one.

## DEMOTE-NOT-DELETE (Matt directive) — CLEAN

§4 + §7 hold the line precisely: `ARCHETYPE_ROLE_PRIORITY` / `_PLAYER_CONTROLLER_ARCHETYPES` / `ARCHETYPE_TEMPLATES` / `legacy_archetype_shim` / the internal legacy-format bridge are demoted-but-resident; the monster `_PREFERRED_BEHAVIOR_ROLES` path is untouched. Deletion is correctly deferred to Stage 3. No scope creep into retirement.

## THE OUTCOME-EQUIVALENCE CRITERION — IS IT RIGOROUS ENOUGH? (the call Matt routed to me)

**Short answer: the IDEA is sound and correct; the CRITERION AS WRITTEN is not yet sufficient gate evidence. It needs two tightenings (WARN-1). With them, it is rigorous enough. Without them, it leaves a hole a real regression can hide in.**

Why the idea is right: the role-priority list is an INPUT to `choose_action`; "behavior" is the EMITTED fight. Two different priority lists that produce statistically indistinguishable fights ARE piloting-equivalent, and the literal-list-match criterion provably FAILS by construction on the bc-collapsed groups (§2.6) — I verified the collapse is real (water/earth/holy → identical 8-tuple at long range; element never touches a rotation axis in `bc_target_source.py`). So outcome-equivalence is the only criterion that can even be evaluated for those groups. gamora is correct to reject list-equality. That part is a genuine analytical advance, not a dodge.

Why it is not YET sufficient — two holes:

**WARN-1a — the group-envelope test (§3.1 / §3.2 Type-D) can launder a regression as "within the envelope."** The criterion says the bc-collapsed group is evaluated as a GROUP: the single bin ordering must land "within the envelope spanned by the group's three label orderings, not match one specific member." The hole: the envelope is defined by the three LEGACY orderings' outcomes, but those three were never required to be close to each other. If `water_mage` (DoT-first), `earth_caster` (control/area-first), and `holy_caster` (area-first) already produce a WIDE outcome spread (e.g., win-rates spanning 20pp), then "within the envelope" is a band so wide that a genuinely mis-piloted bin ordering trivially passes — the criterion would certify a regression because the legacy baseline was itself dispersed. The envelope must be characterized BEFORE it is used as a gate, and a max-width guard applied.
- **Required tightening:** the criterion must (i) FIRST report the legacy intra-group outcome spread (the width of the envelope per metric), and (ii) state a maximum-acceptable envelope width beyond which "within the envelope" is NOT a valid PASS — instead the collapse must be escalated to gandalf as a design question ("the coordinate genuinely cannot reproduce a behavior the label was carrying, and the gap is large enough to matter"). An envelope wider than, say, the §3.1 per-archetype tolerance band (±3pp win-rate) means the single canonical ordering is NOT behavior-equivalent to all members — it is equivalent to at most one. Whether that is acceptable is gandalf's design call, but the CRITERION must surface it rather than silently pass it. As written, a wide envelope is an automatic pass, and that is the hole.

**WARN-1b — the opponent set and fixed-seed are under-specified, which is where outcome-equivalence runs usually leak.** §3.1 says "a fixed opponent set + fixed seed." For an outcome-equivalence claim to be CAUSALLY attributable to the one variable (keying mechanism), the run must be one-variable-clean at the harness level (Disc #7.8): identical opponents, identical seed, identical kit, ONLY the keying swapped between arm A and arm B. The note asserts this but does not specify (i) WHAT the opponent set is (a fixed gauntlet? the trial bosses? a peer-archetype round-robin?), nor (ii) that N=30 smoke is powered to resolve a ±3pp win-rate delta. ±3pp at N=30 is inside the binomial noise floor (a 3pp shift on 30 fights is ~1 fight) — the smoke run as specified CANNOT distinguish a 3pp regression from sampling noise. The smoke N is fine as a SMOKE (sanity that nothing exploded), but the note currently presents the smoke band as if it were the gate; it must distinguish smoke-sanity from the milestone gate's statistical power.
- **Required tightening:** the criterion must (i) name the fixed opponent set explicitly (so the run is reproducible and the envelope is meaningful), and (ii) state that the ±3pp/±5%/L1≤0.10 PASS band is the MILESTONE gate at full-N, with N chosen to resolve those deltas above noise; the N=30 smoke arm is a did-not-explode sanity check, NOT the equivalence gate. Otherwise the gate evidence is a band the smoke run cannot actually measure.

**Net:** with WARN-1a (characterize + width-cap the envelope, escalate over-wide collapses to gandalf) and WARN-1b (name the opponent set; separate smoke-sanity from milestone-gate statistical power), the outcome-equivalence criterion becomes rigorous enough to be the gate evidence. Both are amendments to the CRITERION TEXT in §3, addable before Unit-2 implementation — they do not require re-deriving the map. The Type-M path (§3.2 — discriminating-axis miss) is already correctly specified as a hard hold; my concern is exclusively the Type-D envelope, which is the path a real regression would travel disguised as expected collapse.

## CROSS-SEAM ROUND-TRIP (Principle 6) — adequately PLANNED

The note declares the cross-seam consumption (`PlayerClass.bc_target` → `CombatantState.bc_target` at `from_player_class:730`, additive-nullable, defensive `getattr`), names MIGRATION.md as a deliverable (§2.4/§6), and §3/§6 plan a round-trip smoke matching the dispatch's Principle-6 clause (coordinate-composed kit pilots via bins; legacy physical kit falls back and pilots unchanged). The field is additive-nullable on the CONSUMER side, so the boundary does not break — consistent with rocket's Stage-1 MIGRATION which I verified at the Stage-1 gate. Principle 6 is satisfied AT THE PLAN level; Gate-2 of the implementation will confirm the round-trip smoke output is actually present (Principle 6 Gate-2 check).

**INFO-2 — name the round-trip fixture as PRODUCTION-PATH.** Principle 6 requires the round-trip use a production-path fixture, not a test-isolated one. The note says "a Stage-1 coordinate-composed PlayerClass" — at implementation, that fixture must come through the live `compose_kit` + adapter path (the same path rocket's Stage-1 round-trip exercised), not a hand-built `CombatantState` with `bc_target` stuffed in. Flagging so the implementation round-trip is production-path; non-blocking for the math note.

## A3 SEPARATION — CONCUR

§5 rules A3 (the ≤20%/1-bin composition-fidelity gate, still OPEN from my Stage-1 finding) SEPARATE from the Stage-2 piloting run, on the correct one-variable grounds: A3's variable is kit COMPOSITION (generation/shim seam); Stage-2's variable is AI KEYING (sim seam). Bundling them would conflate the two and break attribution if either fails. This is the right call and matches my Stage-1 finding's A-4 amendment (A3 closes on the generation side via the KR-routed sim on the 24-default-coordinate fixture). The note's "shared tooling, separate experiments" framing is exactly right. No change needed.

## INFO amendments (non-blocking; address at implementation)

- **INFO-1** — player bin-keying must NOT route through the monster `preferred_behavior` `is_player==False` branch at `choose_action`; enter at `_common`/`get_priority_roles` instead (mechanism detail above).
- **INFO-2** — round-trip fixture must be production-path (`compose_kit`+adapter), not a hand-built CombatantState.
- **INFO-3** — the `mixed` ctrl_bin row (§2.3.1) is specified as "in-rotation, not forced-first" but the note also says `mixed` does not occur in the 16 elemental set (it is support/hybrid). At implementation, confirm the `mixed` branch is exercised by at least one test fixture even though it is out-of-the-16, OR document it as forward-compat-only/untested — an unexercised branch in the keying function is a latent gap when physical/support paths arrive post-Stage-3. Non-blocking now; track it.
- **INFO-4** — the note should, at implementation, emit the §3.3 per-archetype gate table as a committed artifact (not just inline), so Gate-2 of the implementation has the evidence on disk. The note already commits to producing it; just ensure it lands as a file.

## Action

- [ ] Developer (gamora): amend §3.1/§3.2 of the math note per WARN-1a — characterize the legacy intra-group outcome envelope width FIRST, set a max-acceptable-width cap, and escalate over-wide bc-collapses to gandalf rather than auto-passing them as "within envelope."
- [ ] Developer (gamora): amend §3.1 per WARN-1b — name the fixed opponent set explicitly; state that ±3pp/±5%/L1≤0.10 is the MILESTONE gate at full-N (N powered to resolve the band above noise), and that N=30 smoke is sanity-only, not the equivalence gate.
- [ ] Developer (gamora) at implementation: route player bin-keying via `_common`/`get_priority_roles`, not the monster `preferred_behavior` branch (INFO-1); production-path round-trip fixture (INFO-2); cover or document the `mixed` ctrl_bin branch (INFO-3); commit the §3.3 gate table as a file (INFO-4).
- [ ] gandalf (parallel design review): the bc-collapse design-acceptability (is a single canonical damage-core ordering OK for water/earth/holy?) is YOUR call, not mine; WARN-1a routes the OVER-WIDE collapse case to you as a gate, but the in-band collapse acceptability is design taste in your lane.
- [ ] Matt: no decision needed at this gate (no BLOCK; amendments are within gamora's seam + my ADR-002 process-amendment authority). Milestone tagging (dropping the seam prefix) remains yours per ADR-002 when the implementation lands.

## May Unit-2 implementation proceed?

**YES — conditional on:** (a) the WARN-1a + WARN-1b criterion amendments landing in §3 of the math note (they sharpen the gate EVIDENCE; they do not change the map derivation, so they do not block starting implementation in parallel — but the equivalence run MUST be measured against the amended criterion, not the as-written one), and (b) gandalf's §7.5 design half clearing. The map (§2) is implementable as-is, the tri-state and demote-not-delete contracts are clean, the smuggling trap is avoided, and the cross-seam round-trip is planned. The amendments are to the proof's rigor, not the plan's structure. Criterion-text amendments are within gamora's seam and my ADR-002 process authority; no Matt escalation required at this gate.

## References

- Math note: `src/reincarnated/simulation/math/bc-coordinate-cutover-stage-2-ai-bin-keying-2026-06-14.md` @ `c29599b`
- Dispatch: `agentic_orchestration/dispatches/2026-06-14-gamora-bc-coordinate-cutover-stage-2.md`
- Source verified: `src/reincarnated/simulation/ai_strategies.py` (`:45` `_PLAYER_CONTROLLER_ARCHETYPES`, `:52` `ARCHETYPE_ROLE_PRIORITY`, `:160` `get_priority_roles` + P7 WARN fall-throughs, `:204` `_PREFERRED_BEHAVIOR_ROLES`, `:237` `choose_action` is_player gate, `:292` `_common` control gate)
- Source verified: `src/reincarnated/simulation/combatant.py` (`:109` archetype, `:224` substrate, `:730` `from_player_class` propagation site)
- Source verified: `src/reincarnated/generation/bc_target_source.py` (`:25-76` `_ROLE_CTRL`/`_ENERGY_TEMPO` bin maps confirming the note's empirical claims; `:158-197` element-nudge confirming the §2.6 bc-collapse mechanism)
- Continuity: `agentic_orchestration/qa/findings/2026-06-14-rocket-bc-coordinate-cutover-stage-1-gate-2.md` (Stage-1 gate; A3-OPEN; one-variable precedent)
- Companion design ruling: `agentic_orchestration/gandalf/notes/2026-06-14-class-generator-bc-target-cutover-ruling.md` (§7.5 contract — gandalf's parallel review)
