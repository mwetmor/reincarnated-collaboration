# Dispatch — 2026-06-15 — rocket — weapon-envelope coordinate-derived role-floor fix

**Status:** 🔥 FIRED — Matt-GREENLIT 2026-06-15 ("greenlight the rogue fix — recognition + validate are done; the fix is real, isolated, code-cited"); jack-ryan Gate-1 CLEAR-WITH-AMENDMENTS (finding `2026-06-15-gate1-rocket-envelope-role-floor-fix.md`, commit `b376ae0`; amendments A1/A2/A3 folded below — documentation-only, ADR-002 tiered authority, re-verified at the MANDATORY math-note Gate-1).
**From:** knight-rider
**To:** rocket
**Pre-fire gate:** jack-ryan Gate-1 (DESIGN-MODE) on this dispatch BEFORE it fires.
**Estimated effort:** multi-day (Pattern B)
**Parent:** `agentic_orchestration/gandalf/notes/2026-06-15-rogue-degeneracy-role-floor-diagnosis-for-kr.md` §5 (the fix direction) + §6 (the b6-deletion coupling) + §7.3 (routing); `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 6-septies (CONFIRMED status).

## What this is

The remediation for the CONFIRMED rogue degeneracy. rocket's role-count audit (commits `56f5179`/`c0fce09`, script `scripts/rocket_rogue_role_floor_audit_2026_06_15.py`) empirically confirmed the diagnosis: the weapon-as-ENVELOPE composer dropped the role-composition floor the b6 template guaranteed. The envelope rogue kit emits **0 defensive, 0 burst** across all 6 DEX geometries; the b6 rogue kit carries **defensive=5, burst=1, mobility=3**. The entire arm-to-arm delta IS the role floor. A glass single-target cell composed with zero survival + zero spike over-shreds swarm and craters boss → unshapeable for one global balance modifier; b6 converges only because its template forces the floor.

This dispatch ADDS a **coordinate-derived role-composition floor** to `compose_physical_kit_envelope`, derived from the bc-cell's own 8-tuple — so the envelope produces shapeable kits without the legacy label machinery.

## THE NON-NEGOTIABLE SPINE (Matt anti-creep mandate)

The floor is derived from the **bc-cell's own 8-tuple coordinates** (`def_bin`, `eng_bin`, `geo_bin`, `tempo_bin`, …), NEVER from a re-introduced archetype label. **No "rogue" (or any archetype) label returns — not as a template, not as a classify step, not as a string lookup.** If the implementation finds itself reaching for an archetype label to drive the floor, that is a design failure — halt and surface it. The genre truth (every viable ARPG glass striker carries a survival tech) is re-encoded at the coordinate layer. This is the whole point of the weapon-as-envelope architecture; the fix must honor it.

**⚠ Gate-1 amendment A1 (BLOCKING for the math-note — the NEVER-cross collision):** the obvious defensive-emission path collides head-on with the envelope's load-bearing physical/caster invariant. The grammar's `defensive` role maps ONLY to `self_buff`/`teleport` (`ability_grammar.py:138`), and BOTH of those are in `CASTER_ENVELOPE_GEOMETRIES` (`weapon_envelope_composer.py:74-77`) — the NEVER-cross set the physical envelope must never draw from. So a naive "emit a defensive skill" reaches straight for a caster geometry. **rocket MUST meet this deliberately in the math-note** — design a coordinate-derived defensive-role emission that lands on a PHYSICAL-eligible geometry (or otherwise satisfies the survival-minimum intent) WITHOUT (a) drawing a caster geometry (regresses NEVER-cross) and WITHOUT (b) reaching for a label (regresses the spine). Name this collision as an explicit open question; the math-note Gate-1 WILL verify no floor skill lands on a caster geometry.

**⚠ Gate-1 amendment A2 (smuggle-test — a Gate-1 PASS criterion):** each floor rule must key on the SINGLE genre-justifying coordinate and demonstrably fire on a NON-rogue cell that shares that coordinate. A rule that needs a ≥3-coordinate conjunction to fire IS the label-in-coordinate-clothing tell (it's a 1:1 proxy for the old rogue label). The math-note must show each rule's single load-bearing coordinate + a non-rogue cell it also fires on. This is how "coordinate-derived, not label" is VERIFIED, not just asserted.

## Acceptance — the fix composes shapeable kits AND re-passes G7

- **The fixed envelope rogue kit carries the role floor** the audit showed it was missing: ≥1 defensive (the highest-leverage line — `def_bin=glass` → survival minimum), burst-role presence reconciled for sub-60 cells, mobility floor for mobile cells, AoE-share floor for pure-single-target cells (so it stops trivially over-shredding swarm). All COORDINATE-derived.
- **No regression of the kit_size dissolution** (Phase-2 §4.1): the envelope must still compose the **10–13 distinct-skill** band with the role-floor slots reserved — the cross-product cardinality must still clear the floor with reserved roles. Report geometry-only-distinct, as Phase-2 did.
- **No regression of L1 identity proxy or the §1.2 ratio guardrail** (Phase-1).
- **HONEST clause:** if a coordinate-derived floor CANNOT be built without either (a) re-introducing a label, or (b) breaking the kit_size band, that is a valid, valuable finding — report it; do NOT force it or smuggle a label. Route to gandalf.
- **The fixed envelope rogue must re-pass Prereq B / G7 HOLD-SIM** (gamora seam, downstream — see Sequence): the envelope arm now CLEARS the upper tiers (elite/mini_boss/boss) b6 was carrying. That G7 re-pass — NOT this dispatch — is what closes the b6-deletion both-pass tally. This dispatch produces the fixed composer + its own Gate-2; the G7 re-pass is the coupled follow-on KR orchestrates.

## Math-before-code (Discipline #1) — produce FIRST; HALT for the MANDATORY Gate-1

This is a composer **semantic addition** (Discipline #12) — the math-note Gate-1 is MANDATORY, not conditional. Produce, code-cited, BEFORE any code:

1. **The coordinate→floor mapping**, derived purely from the 8-tuple: which coordinate drives which role-floor, and the floor magnitude. At minimum (gandalf §5):
   - `def_bin=glass` → **defensive-role minimum** ≥1. The composer has NO defensive-emission path today (`_role_for_geometry` `:243-252` emits only {mobility, burst_damage, area_damage, primary_attack}; `mobility` only on `geometry=="defensive_dash"` `:245-246`). Design the coordinate-derived defensive emission. THE highest-leverage line.
   - `eng_bin=*-fast` → **mobility minimum** ≥1–2.
   - `geo_bin=single-target` → **AoE-share floor** (mirror the b6 25–35% intent `b6_archetype_templates.py:242`, coordinate-derived) so a pure-ST cell doesn't over-shred swarm.
   - **burst:** reconcile the `power_tier >= 60` burst gate (`weapon_envelope_composer.py:248`) with sub-60 single-target cells — floor burst-role presence by COORDINATE, not by a power threshold, OR justify the power gate's retention.
2. **The cross-product cardinality re-proof (⚠ A3):** show the 10–13 distinct-skill band still holds WITH the reserved role-floor slots — the floor must not starve the kit_size dissolution Phase-2 proved. Report the **distinct-GEOMETRY count WITH the floor slots reserved** (not just total kit_size) — the floor slots consume geometry draws, so the distinctness proof must account for them explicitly.
3. **How distinctness + role are stamped** without a label: confirm roles emerge from the coordinate-derived rules, not a classify→template path.

**HALT for MANDATORY jack-ryan Gate-1 on the floor math-note before any code.**

## Cross-seam contract change? (Principle 6 gate — knight-rider completed at authoring time)

**Assessment: CONDITIONAL — rocket resolves at math-note.** The fix changes skill CONTENT (adds defensive-role + burst-role emission). **Lean: NO contract change** — `role` is already a field on the shared `Skill` dict (the b6 kits carry `role="defensive"`; the envelope composer already stamps `role`, per the audit's role-counts), so emitting `role="defensive"` skills reuses the EXISTING field and the EXISTING shared Skill dict shape. **But rocket MUST decide + state explicitly** (Principle-6 silence = Gate-1 BLOCK): if the fix adds/renames/removes ANY field on the Skill dict / loadout packet consumed by gamora sim or star-lord export, that IS a cross-seam contract change (ADR-004) → write MIGRATION.md + round-trip smoke. If NO → state `Round-trip: not applicable because the role-floor reuses the existing shared Skill dict role field; no field added/renamed/removed` (and the gamora G7 re-pass exercises the sim boundary regardless).

## Required reading before starting
- gandalf diagnosis note `agentic_orchestration/gandalf/notes/2026-06-15-rogue-degeneracy-role-floor-diagnosis-for-kr.md` (§1 mechanism, §2 why rogue, §5 fix direction, §6 b6 coupling) — the spec.
- YOUR role-count audit: `scripts/rocket_rogue_role_floor_audit_2026_06_15.py` + its result (the confirmed numbers).
- `weapon_envelope_composer.py` — `_role_for_geometry` (`:243-252`), burst gate (`:248`), `compose_physical_kit_envelope` (`:277-372`), `PHYSICAL_GEOMETRY_PALETTE` (`:49-61`).
- The b6 rogue template floor (the genre-truth being re-encoded, coordinate-side): `b6_archetype_templates.py` rogue entry (`:247-250` mobility/defensive/burst, `:242` AoE-share). **You re-encode its INTENT at the coordinate layer; you do NOT call it.**
- `bc_target_source.py` — the rogue cell coordinates (`def_bin=glass` `:36`, `geo_bin=single-target` `:54`, `eng_bin=close-fast` `:147-149`).
- Your Phase-2 build + math-note (the kit_size dissolution not to regress): `weapon_envelope_composer.py`; `src/reincarnated/generation/notes/2026-06-15-weapon-as-identity-phase-2-math-note.md`; gate artifact `output/weapon-as-identity-phase2-gate-20260615.json`.
- Genre anchors for the floor's SHAPE (gandalf §5): D3 Demon Hunter (Smoke Screen/Vault mandatory), D2 Assassin (Shadow Discipline), PoE glass-cannon defensive-layers doctrine.
- Disciplines #1 (math-first), #1.2 (code-cite), #2/#2.1 (smoke + resource-scaling), #11 (empirical), #12 (semantic-shifting — this fix IS one; document it).

## Scope
- [ ] **Math-note FIRST (Discipline #1)** — the coordinate→floor mapping + cross-product cardinality re-proof + Principle-6 resolution. **HALT, MANDATORY jack-ryan Gate-1.**
- [ ] Add the coordinate-derived defensive-role emission path to `compose_physical_kit_envelope` (the composer has none today).
- [ ] Add the coordinate-derived role-floor (defensive/mobility/AoE-share/burst) keyed on the 8-tuple — NO archetype label.
- [ ] Preserve the kit_size 10–13 band + geometry-only-distinct floor + L1 proxy + §1.2 ratio guardrail (no regression).
- [ ] Smoke-test passes (Discipline #2; #2.1 resource-scaling if compute-heavy).
- [ ] MIGRATION.md IF the Principle-6 assessment resolves YES (else the not-applicable justification).
- [ ] AGENT_STATE.md updated; tag `rocket/v1.x-rogue-role-floor` (seam-prefixed).

## Out of scope (explicit non-goals)
- **NO b6 deletion.** That is the downstream destructive move, fired only AFTER the gamora G7 re-pass closes the both-pass tally AND gandalf+Matt give the fire-confirmation. This dispatch does not touch b6 or `balance_loop.py`'s ARCHETYPE_TEMPLATES imports.
- **NO live-wiring of the envelope path into `class_generator.py`.** The audit found `compose_physical_kit_envelope` is not yet referenced there (physical coords still route to legacy b6). Live-wiring is a SEPARATE downstream routing step; this dispatch fixes the composer + re-validates via the G7 harness, it does not re-route the live path.
- **NO architecture-generalization / caster work.** The architectural question is HELD (resisted two levers, needs an unbuilt spatial/coverage lever). Do NOT touch the caster path.
- **NO caster mini_boss/boss kills-deficit work** (orthogonal; its own future rocket dispatch if/when Matt commissions it).
- **NO re-introduction of any archetype label** (the spine — see above).
- **NO push** (Matt-gated).

## Open questions for the agent to resolve (document in the math-note)
- The coordinate-derived defensive-emission design: how a glass cell's `def_bin` forces ≥1 defensive skill from the weapon-gated geometry vocabulary without a label, and which geometry/role rule carries it. **(A1) Resolve the NEVER-cross collision explicitly:** the grammar's `defensive` role currently maps only to `self_buff`/`teleport`, both in `CASTER_ENVELOPE_GEOMETRIES` — so name how a physical-eligible defensive emission is achieved without drawing a caster geometry and without a label.
- **(A2) The single load-bearing coordinate per floor rule** + a non-rogue cell each rule also fires on (the smuggle-test).
- The burst reconciliation: floor burst-role by coordinate vs retain/justify the `power_tier>=60` gate.
- The AoE-share floor magnitude for single-target cells (mirror b6 25–35% intent, coordinate-derived).
- The Principle-6 resolution (reuses role field vs new field) — decide + surface.
- Whether the reserved role-floor slots leave the cross-product enough headroom for 10–13 distinct (the cardinality re-proof).

## Sequence
jack-ryan Gate-1 on this dispatch → rocket floor math-note → **HALT, MANDATORY jack-ryan Gate-1 on the math-note** → rocket implement → **jack-ryan Gate-2 on the fix** → KR orchestrates the coupled **gamora G7 HOLD-SIM re-pass on the rogue cell** (the envelope arm now clears the upper tiers b6 was carrying; jack-ryan Gate-2 on that result) → on G7 re-pass, KR carries it toward closing the b6-deletion both-pass tally → Decision 2 (b6 deletion) becomes fire-able with gandalf+Matt confirmation (a SEPARATE move, not this dispatch). The architectural question stays HELD throughout; it does NOT gate this fix.
