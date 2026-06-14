# Dispatch — 2026-06-14 — rocket — BC-coordinate cutover, Stage 1 (generation)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-06-14 (program authorized; gandalf §7 design call ratified)
**Estimated effort:** multi-unit / multi-session (Act 2 is a workstream, not a re-point — per your own NO-GO probe)
**Acceptance:** generation composes every class FROM `bc_target`; the `KitConstraintError → pre-B6 5-skill fallback` path is structurally gone; water_mage 1/29 dissolved; zero archetype-label-as-INPUT in generation (label is OUTPUT only).

## Context

The lock-compliant substrate-agnostic composer (`bc_target_composer.compose_kit` + `synthesize_archetype_label`) was built and ratified under W0.2 (2026-05-21) and then shelved — every season since has shipped through the legacy label-locked path the qd-engine-bc-axes-lock forbids. gandalf's design call (§7 of the cutover ruling) makes the BC-coordinate 8-tuple the shared currency across generation↔simulation and demotes the archetype label to derived, display-only output. This is the form-bias root retired at the generation head.

Your Act-1 cutover-readiness probe (`agentic_orchestration/rocket/notes/2026-06-14-compose-kit-cutover-readiness-probe.md`, committed `bd36d2d`) is ENDORSED: the "cutover, not rebuild" framing understated the integration surface. The three blockers you found (no `PoolMechanic→Skill` converter; orchestrator can't emit a free BC-target; substrate hole) are now resolved by gandalf's design call. This dispatch answers your "start unit 1 now vs route deps first" question: **unit 1 now has its design contract — author it.** A4 (the cross-seam schema dependency) is being routed by KR to star-lord + gamora IN PARALLEL with your math note; it may gate Stage-1 persistence but does NOT gate the note.

This is **Stage 1 of a three-stage program**. Stage 2 (gamora, simulation AI bin-keying) is sequenced AFTER your stage. Stage 3 (irreversibility deletion — the GOAL) is sequenced after Stage 2, gated prove-then-delete. You own Stage 1 only.

## Required reading before starting

- `agentic_orchestration/gandalf/notes/2026-06-14-class-generator-bc-target-cutover-ruling.md` — **§7.0–7.4, §7.6, §7.8–7.9** are your contract (read §5–§6 for the program shape)
- Your own probe note (above) — your blockers are what §7 discharges
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/w0-2-archetype-removal-bc-target-composition.md` — the W0.2 migration that built `compose_kit`; note the substrate section `:405-409/:485` (#13a-partition: composer stays substrate-blind) and the shim removal trigger `:639`
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — the lock this completes
- `agentic_orchestration/legolas/research/2026-06-14-archetype-label-as-input-vestigial-sweep.md` — §5.1 gives your exhaustive re-point list (V-1..V-9), incl. the two beyond your original 7: `season_orchestrator.py:145` (`_pick_range_profile` pre-derives the label) and `mechanic_alteration.py:932-1001` (`_bc_view_from_generation_params` reconstructs a synthetic BC-target FROM the label — the lock inverted)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #1 (math-before-code), #13a (substrate partition)

## Math-before-code (Disc #1) — Unit 1 is the math note; math FIRST, gandalf reviews, THEN implement

Author the adapter + source + substrate-binding math note against §7.2/§7.3/§7.4 BEFORE any implementation. The note must specify:

1. **Zero-label source (§7.2).** A direct `(role, range, energy, element) → bc_target` map — NOT through a label. **The smuggling trap (gandalf owns catching this):** do NOT compute the label then look up its coordinate; that keeps the label as the structural hub and re-quantizes to the ~29 legacy points. Go inputs → BINS directly (role → control-density + defensive-profile; range → engagement-profile + damage-geometry; energy → resource-economy + damage-tempo). **Behavior-preserving, NOT diversifying** (one-variable discipline): reproduce current kits through the coordinate-shaped pipe; do NOT sample off-legacy coordinates (diversification is a separate later gated effort). **Element subtlety:** element transitionally nudges the bins (fire→burst-tempo/no-sustain, water→sustain) so behavior holds — mark it TRANSITIONAL, removal trigger = Phase-5 cohesion-judge operational (same trigger as the shim).
2. **Provisional substrate (§7.3).** Binds in the `ComposedKit→PlayerClass` ADAPTER, NOT in `compose_kit` (composer stays substrate-blind per #13a). `canonical_element ← season dominant_element`, marked PROVISIONAL (Phase-5 re-coheres, may re-skin to a different element). Feeds `damage_resolver.py:328/842` + `Skill.canonical_element` (required, `skill_schema.py:40`). Do NOT block the cut on the unbuilt Phase-5.
3. **`PoolMechanic → Skill` adapter contract (§7.4) — a RESOLUTION layer, not glue.** One `PoolMechanic` → exactly one `Skill`; no label consulted ever. Mechanical shape preserved 1:1 (`geometry`, `range_m`, `energy_cost`, `cooldown_seconds`, `cc_effect`/`cc_duration_s`/`cc_slow_magnitude` straight from `PoolMechanic` — these ARE the coordinate, do not re-derive). Substrate stamped here. Gap-fields (`abilities`, `effects`, `timing`, `triggers`, `effect_category`, `power_tier`, `color_value`, `scaling_attribute`, `role`) enriched off the mechanic + coordinate + substrate, **NEVER the label.** If you reuse b6 ability-construction machinery, re-key it off the mechanic, not the archetype — or the disease re-enters through the back door.
4. **`bc_target` as a first-class field on `PlayerClass` (§7.1).**
5. **INTERNAL legacy-format label bridge (§7.6).** The label becomes OUTPUT (computed from `bc_target`) but keeps its legacy string format so the still-label-keyed simulator runs UNCHANGED through Stage 1. This bridge is INTERNAL-ONLY — never player-facing (the player already sees `PlayerClass.name`, the LLM end-of-pipe label). It dies in Stage 3.

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)

**YES.** This dispatch adds `bc_target` as a first-class field on `PlayerClass` (generation output → consumed at the simulator + export boundaries) and introduces the internal legacy-format label bridge.

- The **internal legacy-format label bridge (§7.6) is the decoupling buffer**: in Stage 1 the simulator continues to receive a label of unchanged string format, so the rocket→gamora live boundary does NOT break in this stage.
- `archetype_label` persistence to telemetry is the **A4 v2.15 `ALTER TABLE`** (`archetype_label` + `recompose_energy_calibration_applied` on `class_fight_loadouts`) — routed cross-seam by KR to star-lord (schema owner) + gamora in parallel with this note. A4 may gate Stage-1 persistence; coordinate with star-lord before emitting `archetype_label` to telemetry.

**Acceptance MUST include** (and does, below):
`Round-trip smoke: production-path fixture (a generated season's PlayerClass) flows through the ComposedKit→PlayerClass adapter and is consumed at the simulator boundary (bc_target present + legacy-format label present + skills are full Skill objects) AND, if A4 has landed, at the telemetry boundary (archetype_label column populated).`

## Scope

- [ ] **Unit 1 — math note** (adapter + zero-label source + provisional substrate-binding), authored, gandalf §7 review PASS before any code
- [ ] Direct `(role, range, energy, element) → bc_target` source map (smuggling-trap-clean; element nudge marked transitional)
- [ ] `ComposedKit → PlayerClass` adapter (field-by-field per §7.4 contract)
- [ ] `PoolMechanic → Skill` resolution layer
- [ ] Provisional substrate binding in the adapter
- [ ] `bc_target` first-class field on `PlayerClass`
- [ ] Internal legacy-format label bridge (`synthesize_archetype_label` → legacy string format; OUTPUT only)
- [ ] Re-point all V-1..V-9 generation label-consumption sites (legolas §5.1 exhaustive list)
- [ ] Route infeasibility through `compose_kit`'s `None`/`DeferredEvaluation` — the `KitConstraintError → 5-skill fallback` is structurally removed
- [ ] A3 calibration folded into the Stage-1 gate (shim ≤20%/1-bin — see Open questions)
- [ ] Smoke-test passes
- [ ] MIGRATION.md (cross-seam: `bc_target` on `PlayerClass`; coordinate with A4)
- [ ] Round-trip smoke (clause above) per Principle 6
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `rocket/v?.?-bc-coordinate-cutover-stage-1` (intermediate seam-prefixed tag)

## Acceptance criteria

- [ ] Generation composes every class FROM `bc_target` via `compose_kit` — `class_generator` no longer calls `b6_builder.build(label)`
- [ ] The `KitConstraintError → pre-B6 5-skill fallback` path is **structurally removed** (it cannot fire)
- [ ] The water_mage coordinate composes a full kit (1/29 dissolved — absorbed, not patched)
- [ ] Zero archetype-label-as-INPUT in generation — the legacy label appears only as `synthesize_archetype_label` OUTPUT / the internal bridge
- [ ] Round-trip smoke: production-path fixture (a generated season's PlayerClass) flows through the ComposedKit→PlayerClass adapter and is consumed at the simulator boundary (bc_target present + legacy-format label present + skills are full Skill objects) AND, if A4 has landed, at the telemetry boundary (archetype_label column populated)

## Out of scope (explicit non-goals)

- **Stage 2 (gamora's simulation AI bin-keying)** — you emit the internal legacy-format bridge so the sim keeps running; you do NOT touch `ai_strategies.py` / `ARCHETYPE_ROLE_PRIORITY` / `_PLAYER_CONTROLLER_ARCHETYPES` / `CombatantState`
- **Stage 3 deletion** — do NOT delete `ARCHETYPE_TEMPLATES`, the shim, or any V-D1..V-D6 deprecated-resident machinery; the bridge and shim stay load-bearing through Stages 1–2
- **Diversification** — Stage 1 is behavior-PRESERVING; do NOT sample off-legacy coordinates
- **Element-agnosticism** — element stays a transitional bin-nudge + provisional skin; removing element-from-mechanics is a separate Phase-5-gated change
- **A4 schema authoring** — star-lord owns the `ALTER TABLE`; you provide the `archetype_label` spec only
- **The end-of-pipe LLM label** (`PlayerClass.name`, `llm/naming.py:276`) — untouched; that is the player-facing nameplate and is the goal-state display

## Open questions for the agent to resolve

- **A3 calibration:** run the shim ≤20%/1-bin calibration gate (W0.2 math note §5 / `:590`: if >20% of shim-path kits land >1 bin from BC-target default on any axis, recalibrate). This needs Phase-3/4 simulation — coordinate with gamora for a sim run, or document the gate as deferred-with-criterion if the sim dependency blocks. Document the result in the math note.
- **Zero-label BC-target source option (§7.2):** confirm the direct-map approach (your probe §2 option b) over orchestrator-direct BC-target emission (option a) — gandalf §7.2 rules the direct map; document the binning rationale.
- **MIGRATION.md timing relative to A4:** sequence the `bc_target`-on-PlayerClass MIGRATION with star-lord's A4 `ALTER TABLE`.

## References

- gandalf §7 ruling (above); legolas vestigial sweep §5.1
- W0.2 math note `w0-2-archetype-removal-bc-target-composition.md`
- qd-engine-bc-axes-lock-2026-05-20.md
- Per-stage gate: jack-ryan Gate-2 + gandalf §7 review (on the math note FIRST, then on the implementation)
