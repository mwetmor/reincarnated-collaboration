# Dispatch — 2026-06-15 — star-lord — telegraph export to JSON + the no-drift schema contract

**Status:** ✅ FIRE-READY — jack-ryan Gate-1 (DESIGN-MODE) CLEAR 2026-06-15 (best-hardened dispatch in the chain; no folds). Fires after dispatch 3 lands. Gate-2 watch-item below.
**From:** knight-rider
**To:** star-lord
**Pre-fire gate:** jack-ryan Gate-1 (DESIGN-MODE) on this dispatch BEFORE it fires.
**Estimated effort:** Pattern B (multi-session — owns THE load-bearing invariant of the whole bridge).
**Depends on:** `2026-06-15-gamora-telegraph-combat-model.md` (dispatch 3) — the TelegraphSpec + its MIGRATION.md must exist first.
**Parent ruling (STEP 0):** `canonical/story/telegraph-dodge-temporal-decoupling-2026-06-15.md` § 6 (Move 3 step 2), § 7.1 (the no-drift invariant — **star-lord OWNS this**).

## What this is — Move 3, step 2: serialize the telegraph, own the no-drift contract

gamora's TelegraphSpec (dispatch 3) is the single source. This dispatch serializes it to JSON **alongside the existing fight export**, and — critically — **owns the no-drift schema contract** (§ 7.1): the telegraph the sim costs MUST equal the telegraph the JSON carries, which Godot then renders. star-lord is the enforcement point. If the export drops, reshapes, rounds, or re-frames any part of the TelegraphSpec, the balance answer and the playtest answer diverge silently. **No drift is star-lord's deliverable, not a nicety.**

## THE INVARIANT (name from line one — star-lord is its owner)
**§ 7.1 — one telegraph source, two consumers, no drift.** The export is a **faithful serialization**, not a re-derivation. Specifically:
- The JSON telegraph MUST reconstruct to the EXACT TelegraphSpec gamora costed — same wind-up time, same danger-zone shape (same primitives, same origin/extent/orientation), same coordinate frame, same units, same attack id, same fire-tick.
- **No lossy transforms.** If serialization must change representation (e.g., float precision, unit conversion, coordinate-frame transform for Godot's axis convention), each transform must be **explicit, documented, and round-trip-exact** (or its tolerance bounded + justified). A silent unit/axis mismatch IS the drift this dispatch exists to prevent.
- The schema is the **contract** drax (dispatch 5) consumes. Author it as a contract: versioned, with the units + coordinate frame + shape vocabulary stated IN the schema, so the consumer cannot misread it.

## Cross-seam contract change? (Principle 6 gate — KR assessment; MANDATORY round-trip)
**Assessment: YES — this IS the cross-seam contract (ADR-004), and the round-trip is MANDATORY, not optional.** This dispatch adds a new section to the season/fight export packet (the telegraph JSON). Two boundaries:
- **gamora→star-lord (inbound):** consume the TelegraphSpec per gamora's MIGRATION.md.
- **star-lord→drax/Godot (outbound):** the telegraph JSON schema drax consumes.

**MANDATORY round-trip smoke (the pipeline-completion gate's technical core, § 8.1):**
`Round-trip smoke: load gamora's production fixture (one-boss + glass-close-ST exemplar fight emitting TelegraphSpecs) → export to JSON → re-parse the JSON → assert the re-parsed telegraph EQUALS the source TelegraphSpec field-for-field (wind-up time, shape primitives + geometry, coordinate frame, units, attack id, fire-tick), within explicitly-bounded tolerance for any documented transform.`
This round-trip is the deliverable's spine. A PASS here is half of the § 8.1 pipeline-completion gate (the other half is drax's render==JSON in dispatch 5).

**MIGRATION.md REQUIRED** (export seam → drax) documenting the telegraph JSON schema.

## ⚠ ALSO CONFIRM: the dodge skill survives export (feeds dispatch 5)
Dispatch 2 (rocket) flagged that Godot must SEE the dodge skill in the kit to wire its input. Confirm the existing **skill-list export carries the inert dodge skill through** — that no export-side "sim-usable only" filter strips a movement skill the autobattle cannot use. If such a filter exists and drops the dodge, that is a contract gap to FIX here (the dodge must reach Godot). State the finding explicitly.

## Required reading before starting
- STEP-0 ruling § 6, § 7.1, § 8.1.
- gamora's `2026-06-15-gamora-telegraph-combat-model.md` + its MIGRATION.md (the TelegraphSpec contract) — REQUIRED; do not start before it lands.
- The existing fight/season export path: `src/reincarnated/export/season_exporter.py`, `src/reincarnated/export/MIGRATION.md`, `src/reincarnated/telemetry/recorder.py` — where the telegraph JSON attaches alongside the fight export.
- The spatial twin `canonical/story/battle-room-presentation-decoupling-2026-06-15.md` — the coordinate-frame the danger-zone geometry lives in (so the export does not silently re-frame it).
- ADR-004 (MIGRATION.md cross-seam handoff); REVIEW_PROCESS.md Principle 6 (round-trip).
- Disciplines #1, #2, #8 (schema validation at boundaries — directly load-bearing here), #11.

## Math-before-code (Discipline #1) — produce FIRST, HALT for Gate-1
1. **The JSON schema** — the telegraph section's structure, field-by-field, with units + coordinate frame + shape vocabulary stated in-schema; versioned.
2. **The transform ledger** — every representation change between TelegraphSpec and JSON (precision, units, axis/coordinate-frame for Godot), each marked round-trip-exact or tolerance-bounded+justified. A telegraph with NO transforms is ideal; document whichever path is taken.
3. **The round-trip assertion design** — exactly which fields are compared and how equality/tolerance is defined.
4. **The dodge-skill export-survival finding** (above).

**HALT for MANDATORY jack-ryan Gate-1 on the schema + transform ledger before any code.**

## Scope
- [ ] Schema + transform-ledger math-note FIRST; **HALT, MANDATORY Gate-1.**
- [ ] Serialize the TelegraphSpec to JSON alongside the existing fight export, faithfully (no silent drift).
- [ ] Implement the round-trip assertion (export → re-parse → field-for-field equality vs the source TelegraphSpec).
- [ ] Confirm/fix the dodge-skill export survival.
- [ ] MIGRATION.md (export → drax) — the telegraph JSON schema contract.
- [ ] Smoke + the MANDATORY round-trip on gamora's one-boss + glass-close-ST fixture.
- [ ] AGENT_STATE.md updated; tag `star-lord/v1.x-telegraph-export`.

## Acceptance criteria
- [ ] Telegraph JSON exports alongside the fight export for the one-boss + glass-close-ST exemplar.
- [ ] **Round-trip smoke PASSES:** re-parsed telegraph == source TelegraphSpec field-for-field (within documented, bounded tolerance for any explicit transform).
- [ ] The schema states its units + coordinate frame + shape vocabulary in-band (drax cannot misread it); versioned.
- [ ] The dodge skill survives export to Godot (no filter strips it) — confirmed or fixed.
- [ ] MIGRATION.md authored for drax with the complete JSON schema contract.

## Out of scope (explicit non-goals)
- **NO telegraph combat-model changes** — gamora owns the source (dispatch 3); star-lord serializes, never re-derives.
- **NO Godot/render work** — dispatch 5 (drax consumes this schema).
- **NO new telegraph semantics** — if the JSON needs a field the TelegraphSpec lacks, that is a gamora source gap → route back to dispatch 3, do NOT invent it in the export (inventing it IS drift).
- **NO coverage beyond the one-boss + glass-close-ST exemplar first** (§ 8.1).
- **NO push** (Matt-gated).

## Open questions for the agent to resolve (document in the math-note)
- Coordinate-frame/axis transform for Godot's convention: handle in the export (documented transform) or pass through raw and let Godot transform? Whichever — the round-trip must stay exact and the choice stated in-schema.
- Float precision policy for wind-up time + geometry (exact vs bounded tolerance).
- Whether the telegraph JSON rides the existing season packet or a sidecar file alongside it (state + justify; the consumer must know where to read).

## Sequence
gamora dispatch 3 lands (TelegraphSpec + MIGRATION.md) → jack-ryan Gate-1 on THIS dispatch → star-lord schema math-note → **HALT, MANDATORY Gate-1** → star-lord implement + round-trip → jack-ryan Gate-2 (the round-trip PASS is the gate) → **drax dispatch 5 fires off this schema.** Critical path; gates dispatch 5.

## Gate-2 watch-items (jack-ryan Gate-1 INFO — carry to Gate-2)
- **Transform-choice inheritance:** whichever coordinate-frame/axis transform choice star-lord makes (transform-in-export vs pass-through-raw), the transform-ledger must show it AND drax's dispatch-5 schema-read must inherit the SAME choice. The schema-states-its-own-frame requirement closes this — verify at Gate-2 that the in-schema frame declaration matches what drax consumes.
- **Composed tolerance:** drax asserts render==JSON and this dispatch asserts JSON==sim, so render==sim holds transitively. If THIS dispatch's round-trip uses bounded tolerance on any transform (allowed), that tolerance COMPOSES with any drax-side tolerance across the two hops. If both hops carry tolerance, document the composed bound at Gate-2.

## References
- STEP-0 ruling § 6/§ 7.1/§ 8.1; gamora dispatch 3 + its MIGRATION.md; spatial twin battle-room doc; ADR-004; REVIEW_PROCESS Principle 6.
