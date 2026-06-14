# Dispatch — 2026-06-14 — gamora — BC-coordinate cutover, Stage 2 (simulation AI bin-keying)

**From:** knight-rider
**To:** gamora
**Approved by:** Matt 2026-06-14 (program authorized; gandalf §7 design call ratified; physical-pool DEFERRED post-Stage-3; ARCHETYPE_ROLE_PRIORITY **demoted-to-fallback** per Matt directive 2026-06-14)
**Estimated effort:** multi-unit / multi-session (this is the second instrument-side cut; math-note-first then implementation, each gated)
**Acceptance:** the simulator pilots every **coordinate-composed (bc_target-present)** kit by its BC bins, not its label; `ARCHETYPE_ROLE_PRIORITY` + `_PLAYER_CONTROLLER_ARCHETYPES` survive ONLY as the fallback for not-yet-migrated (physical-pool legacy) kits; behavior-preserving on the elemental set (one-variable: piloting equivalence, not diversification).

## Context

This is **Stage 2 of the three-stage BC-coordinate-identity cutover** (gandalf §7 ruling, Matt-authorized 2026-06-14). Stage 1 (rocket, generation) is LANDED as an elemental partial: `rocket/v1.0-bc-coordinate-cutover-stage-1-partial` @ `62a18bc` — 16/21 elemental archetypes now compose FROM `bc_target`, with `synthesize_archetype_label` emitting the legacy-format string as OUTPUT only (the §7.6 internal bridge). The 5/21 physical archetypes still route through the resident legacy b6 path (physical-pool expansion DEFERRED to a separate post-Stage-3 Matt-gated effort).

**The problem Stage 2 closes (§7.5 — the discrimination-law-at-the-instrument, third instance after M1.3.5 and the W-E search layer):** the simulator MEASURES a kit by PLAYING it. If it pilots by the label, even a perfectly axis-composed kit is measured through the label's ASSUMED behavior — the cut is incomplete until the instrument reads the coordinate. Stage 1 demoted the label to OUTPUT at the generation head; Stage 2 earns the true *"zero label-as-input in the live path"* by making the simulator read `bc_target` instead of the label.

**The Matt directive that shapes this dispatch — DEMOTE, do not retire.** Because physical kits ride the legacy path through Stage 3, `ARCHETYPE_ROLE_PRIORITY` and `_PLAYER_CONTROLLER_ARCHETYPES` are **demoted to a fallback for not-yet-migrated paths**, NOT deleted. Deletion is Stage 3, gated prove-then-delete. Stage 2's job: make BC-bin keying the PRIMARY mechanism for bc_target-present kits; keep the label-keyed tables as the fallback when `bc_target` is absent.

## Required reading before starting

- `agentic_orchestration/gandalf/notes/2026-06-14-class-generator-bc-target-cutover-ruling.md` — **§7.5 is your contract** (Component 5, the discrimination-law-at-the-instrument); §7.6 (staging — your stage frees the internal bridge); §7.8 (one-variable / behavior-preserving discipline); §7.9 (the two labels — you key off the coordinate, never the start-of-pipe `archetype_tag`)
- Stage 1 landing: `src/reincarnated/generation/MIGRATION.md` (rocket's `bc_target`-on-PlayerClass entry) + `src/reincarnated/generation/composed_kit_adapter.py` (where `bc_target` is stamped onto `PlayerClass`) — understand the 8-tuple shape you are consuming
- `src/reincarnated/generation/bc_target_source.py` — the bin definitions (control-density, engagement-profile, damage-tempo, etc.); your AI-keying map derives from THESE bins, so use the same bin vocabulary
- `src/reincarnated/simulation/ai_strategies.py` — `get_priority_roles` (`:160`, the lever), the `_PREFERRED_BEHAVIOR_ROLES` map (`:204`), `ARCHETYPE_ROLE_PRIORITY` (`:52`), `_PLAYER_CONTROLLER_ARCHETYPES` (`:45`), `_common`/`_scripted` paths
- `src/reincarnated/simulation/combatant.py` — `CombatantState.archetype` (`:109`), `preferred_behavior` (`:162`), `from_player_class` (`:730`, sets `archetype=player_class.archetype_tag` — your `bc_target` propagation site)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #1 (math-before-code), #12 (semantic-shift: bc_target-present vs absent is a tri-state, do NOT collapse to a silent default), #39 (no silent stub fallbacks — an unkeyable kit must log loud, not silently default)

## Math-before-code (Disc #1) — Unit 1 is the math note; math FIRST, gandalf §7.5-reviews, THEN implement

Author the **BC-bin → AI-keying map** math note against §7.5 BEFORE any implementation. The note must specify:

1. **The bin → role-priority derivation (§7.5).** A direct map from `bc_target` bins to role-priority ordering — NOT through the label:
   - **control-density bin → control-first ordering** — replaces the `_PLAYER_CONTROLLER_ARCHETYPES` membership test (`:45/:292`). A kit pilots control-first because it IS control-dense, not because it's labeled controller.
   - **engagement-profile bin → range/positioning** (kite vs face-tank) from the actual engagement axis.
   - **damage-tempo bin → rotation cadence** (burst-spike vs sustained) from the actual tempo axis.
   The existing `get_priority_roles(preferred_behavior=...)` lever (`:160`) and its `_PREFERRED_BEHAVIOR_ROLES` map (`:204`) are the non-label mechanism the monster path already uses — Stage 2 **promotes `preferred_behavior` from a monster-scripting override to the PRIMARY keying mechanism for players, derived from `bc_target` bins.**
2. **The smuggling-trap analog (gandalf owns catching this).** Derive AI keying from the `bc_target` BINS directly. Do NOT compute the legacy label from the coordinate and then look up `ARCHETYPE_ROLE_PRIORITY[label]` — that keeps the label as the structural hub at the instrument, exactly the disease Stage 1 cured at the head re-entering through the simulator. Go bins → role ordering.
3. **Behavior-preserving validation (one-variable, §7.8).** Stage 2 changes ONLY the keying mechanism (label-lookup → bin-derivation), behavior-preserving on the elemental set. The note must define the **piloting-equivalence criterion**: for the 16 elemental archetypes, the bin-derived role ordering must reproduce the current `ARCHETYPE_ROLE_PRIORITY[label]` ordering (or document + justify each intentional deviation). This is your gate evidence — a sim-run comparison (your seam) showing equivalent piloting label-keyed vs bin-keyed on the elemental set. Diversification (off-legacy coordinates) is explicitly OUT of scope.
4. **The demote-to-fallback contract (Matt directive).** Define the tri-state routing precisely (Disc #12 — do not collapse):
   - **`bc_target` present (coordinate-composed kit, elemental)** → bin-keying is PRIMARY.
   - **`bc_target` absent (legacy physical kit)** → fall back to `ARCHETYPE_ROLE_PRIORITY[archetype]` / `_PLAYER_CONTROLLER_ARCHETYPES` membership. These tables SURVIVE for this purpose.
   - **`bc_target` absent AND archetype unknown to the fallback tables** → loud WARN + registry default (Pattern P7 / Disc #39 — no silent convergence).
5. **`bc_target` as a field on `CombatantState` (§7.6).** Propagate `PlayerClass.bc_target` into `CombatantState` at `from_player_class` (`combatant.py:730`). This is the cross-seam consumption point.

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)

**YES.** This dispatch adds `bc_target` as a field on `CombatantState` (consumed from the Stage-1 `PlayerClass.bc_target` at the generation→simulation boundary). The rocket→gamora live boundary already carries the §7.6 internal legacy-format label bridge, so the boundary does NOT break — Stage 2 ADDS coordinate consumption alongside the still-present bridge label.

**Acceptance MUST include** (and does, below):
`Round-trip smoke: a Stage-1 coordinate-composed PlayerClass (bc_target present) flows through from_player_class into a CombatantState carrying bc_target, and choose_action / get_priority_roles pilots it via the bin-derived ordering (NOT ARCHETYPE_ROLE_PRIORITY[label]); a legacy physical PlayerClass (bc_target absent) falls back to ARCHETYPE_ROLE_PRIORITY and pilots unchanged.`

## Scope

- [ ] **Unit 1 — math note** (BC-bin → AI-keying map + behavior-preserving criterion + demote-to-fallback tri-state), authored, gandalf §7.5 review PASS before any code
- [ ] `bc_target` field on `CombatantState`; propagated at `from_player_class` (`combatant.py:730`)
- [ ] BC-bin → role-priority derivation (smuggling-trap-clean; bins → ordering, never label-lookup)
- [ ] `preferred_behavior` promoted to PRIMARY player keying mechanism, derived from `bc_target` bins
- [ ] `ARCHETYPE_ROLE_PRIORITY` + `_PLAYER_CONTROLLER_ARCHETYPES` **demoted to fallback** (bc_target-absent path) — NOT deleted
- [ ] Tri-state routing per Disc #12 (present → bins; absent-known → fallback table; absent-unknown → loud WARN + default)
- [ ] Behavior-preserving validation: sim-run comparison on the 16 elemental archetypes (label-keyed vs bin-keyed piloting equivalence), deviations documented + justified
- [ ] Smoke-test passes
- [ ] MIGRATION.md (cross-seam: `bc_target` on `CombatantState`; consumes Stage-1 `PlayerClass.bc_target`)
- [ ] Round-trip smoke (clause above) per Principle 6
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `gamora/v?.?-bc-coordinate-cutover-stage-2` (intermediate seam-prefixed tag)

## Acceptance criteria

- [ ] The simulator pilots every `bc_target`-present kit by its BC bins (control-density → control-first; engagement-profile → range; damage-tempo → cadence) — NOT by `ARCHETYPE_ROLE_PRIORITY[label]`
- [ ] `ARCHETYPE_ROLE_PRIORITY` + `_PLAYER_CONTROLLER_ARCHETYPES` retained ONLY as the bc_target-absent fallback; demoted, not deleted (Stage 3 deletes them, gated)
- [ ] Behavior-preserving on the 16 elemental archetypes: bin-keyed piloting reproduces label-keyed piloting (documented equivalence; justified deviations only)
- [ ] Tri-state routing is loud, not silent (Disc #39 / Pattern P7): an unkeyable kit WARNs, never silently defaults
- [ ] Round-trip smoke: coordinate-composed kit pilots via bins; legacy physical kit falls back to label table and pilots unchanged

## Out of scope (explicit non-goals)

- **Stage 3 deletion** — do NOT delete `ARCHETYPE_ROLE_PRIORITY`, `_PLAYER_CONTROLLER_ARCHETYPES`, `ARCHETYPE_TEMPLATES`, or the `legacy_archetype_shim`; they are demoted-but-load-bearing through Stage 3 (gated prove-then-delete after this stage proves the coordinate path)
- **Diversification** — Stage 2 is behavior-PRESERVING; do NOT tune the AI to exploit off-legacy coordinates; piloting equivalence on the elemental set is the bar
- **Physical-pool expansion** — DEFERRED to a separate post-Stage-3 Matt-gated effort; physical kits ride the legacy fallback through Stage 2 (this is precisely why the tables are demoted not deleted)
- **Generation seam** — do NOT touch `compose_kit`, `bc_target_source.py`, `composed_kit_adapter.py`, or `class_generator.py`; you CONSUME `PlayerClass.bc_target`, you do not produce it
- **The internal legacy-format bridge** — it stays load-bearing; Stage 2 frees it (the sim no longer NEEDS it for keying) but does not remove it (Stage 3 does)
- **Monster preferred_behavior R3 path** — the existing monster-scripting override stays as-is; you are EXTENDING the lever to players, not rewriting the monster path

## Open questions for the agent to resolve

- **Bin granularity vs the 6-value `_PREFERRED_BEHAVIOR_ROLES` enum:** the existing behavior enum has 6 values; the `bc_target` bins are finer. Resolve in the math note whether you (a) map bins → the existing 6-value enum then reuse `_PREFERRED_BEHAVIOR_ROLES`, or (b) author a direct bins → role-priority map. Document the choice and the equivalence rationale; gandalf reviews.
- **Behavior-preserving deviations:** if any of the 16 elemental archetypes' bin-derived ordering does NOT match its `ARCHETYPE_ROLE_PRIORITY[label]` ordering, document each case — is it a genuine label/coordinate mismatch (the label was lying about the kit, which is the point) or a bin-map miscalibration? gandalf adjudicates the former, jack-ryan Gate-2 the latter.
- **A3 calibration interaction:** the A3 shim ≤20%/1-bin gate (W0.2 §5, still OPEN, #39-tracked) is sim-dependent and may ride your Stage-2 sim run — coordinate whether the behavior-preserving validation run can also discharge A3, or note it as still-separate.

## References

- gandalf §7 ruling (§7.5 contract; §7.6 staging; §7.8 discipline; §7.9 two-labels)
- Stage 1 landing: `rocket/v1.0-bc-coordinate-cutover-stage-1-partial` @ `62a18bc`; rocket MIGRATION.md
- Matt directive 2026-06-14: demote-to-fallback (not retire); physical-pool deferred post-Stage-3
- Per-stage gate: jack-ryan Gate-2 + gandalf §7.5 review (on the math note FIRST, then on the implementation)
