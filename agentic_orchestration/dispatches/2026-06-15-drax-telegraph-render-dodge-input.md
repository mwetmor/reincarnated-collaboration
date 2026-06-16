# Dispatch — 2026-06-15 — drax — Godot: render telegraphs + wire dodge input (close the round-trip)

**Status:** ✅ FIRE-READY — jack-ryan Gate-1 (DESIGN-MODE) CLEAR 2026-06-15 (cleanest deferred-playtest boundary in the chain; no folds). Fires after dispatch 4 round-trip-PASSES. Gate-2 watch-item below.
**From:** knight-rider
**To:** drax (Godot battle-room seam — `reincarnated-godot/`, per WS2 precedent)
**Pre-fire gate:** jack-ryan Gate-1 (DESIGN-MODE) on this dispatch BEFORE it fires.
**Estimated effort:** Pattern B (multi-session — the render + input layer that closes the pipeline).
**Depends on:** `2026-06-15-star-lord-telegraph-export-schema.md` (dispatch 4) — the telegraph JSON schema + its MIGRATION.md must exist + round-trip-PASS first.
**Parent ruling (STEP 0):** `canonical/story/telegraph-dodge-temporal-decoupling-2026-06-15.md` § 6 (Move 3 step 3), § 7.1 (no-drift — drax is the SECOND consumer), § 8.1 (the round-trip gate closes HERE).

## What this is — Move 3, step 3: Godot proves the skill check

The sim computed the telegraph (dispatch 3); star-lord serialized it faithfully (dispatch 4). This dispatch makes the player experience it: **consume the telegraph JSON, render the danger zones + wind-up timers, and wire the dodge input** so the player times the dodge against the rendered telegraph. This is where the dodge — INERT in the sim — becomes ACTIVE. The piloted layer, not the sim, proves whether glass-close-ST passes its boss skill check.

This dispatch **closes the pipeline-completion round-trip gate** (§ 8.1): the telegraph drax renders must EQUAL the telegraph the sim costed (via star-lord's JSON), AND the dodge input must resolve against it.

## THE INVARIANT (drax is the second consumer — render what the sim costed, nothing else)
**§ 7.1 — one telegraph source, two consumers, no drift.** drax renders the telegraph FROM THE JSON — it does NOT re-derive, re-shape, or "improve" the geometry. The rendered danger-zone shape, wind-up time, position, and orientation must match the JSON (which matches the sim). This is the **temporal twin** of the battle-room **spatial** decoupling drax already built (iter1→4): there, the sim-invariant footprint is rendered faithfully under free presentation; here, the sim-invariant telegraph (when + what-shape) is rendered faithfully. Presentation polish (VFX styling of the danger zone, timer art) is free; the GEOMETRY + TIMING are invariant.

**Coordinate-frame discipline:** the danger-zone shape lives in the sim-invariant frame (the same frame the battle-room parity contract fixes for spawn/damage geometry). Render it in that frame. If Godot's axis convention differs, apply ONLY the transform star-lord documented in the schema — no ad-hoc re-framing (that is drift).

## The round-trip gate this dispatch closes (§ 8.1 — the deliverable)
**Faithful round-trip, proven on ONE boss + the glass-close-ST exemplar first** (first increment of the real pipeline, not a throwaway):
1. **Render == JSON == sim:** the telegraph drax renders (danger-zone shape + wind-up time + position) equals the JSON star-lord exported, which equals the TelegraphSpec the sim costed. Prove it (a parity check in the spirit of `check_descent_parity.py` — assert rendered geometry/timing against the JSON source).
2. **Dodge resolves against it:** the wired dodge input, timed within the wind-up window and moving the player out of the danger-zone shape, negates the hit; mistimed/in-zone, it does not. The dodge RESOLVES against the rendered telegraph (this is the mechanic that was inert in the sim).

PASS on both = the pipeline is complete. star-lord's export round-trip (dispatch 4) is the other half; together they are the § 8.1 gate.

## ⚠ DEFERRED — do NOT slot the viability playtest into this build (§ 8.2, Matt directive)
**No playtest until the pipeline is complete.** "Can a skilled player dodge-clear glass-close-ST" fires on a **separate Matt go**, AFTER the round-trip is proven. This dispatch BUILDS the instrument (render + input + round-trip proof); it does NOT run the viability test. Do not add a playtest step, a difficulty-tuning pass, or a "does it feel clearable" judgment to scope — those are the deferred separate move.

## The dodge skill must be present (depends on dispatch 2 + 4)
Godot wires the dodge input for kits that CARRY the dodge. The dodge is baked into glass-close-ST composition (dispatch 2, rocket) and must survive export (confirmed in dispatch 4, star-lord). Read the dodge skill from the kit's exported skill list; wire input only for kits that carry it. If the dodge is absent from the export for a glass-close-ST kit, HALT and surface (dispatch 2/4 contract gap) — do not hardcode a dodge Godot-side (that would un-source it and re-create drift).

## Cross-seam contract change? (Principle 6 gate — KR assessment)
**Assessment: CONSUMER of star-lord's schema (dispatch 4).** drax does not define the contract; it consumes it. The Principle-6 obligation here is the **render==JSON round-trip** (the consumer side of the no-drift invariant):
`Round-trip: consume star-lord's telegraph JSON for the one-boss + glass-close-ST exemplar → render → assert rendered danger-zone geometry + wind-up timing == the JSON source (parity check) → assert dodge input resolves against the rendered telegraph.`
No new outbound contract; the parity check IS the acceptance.

## Required reading before starting
- STEP-0 ruling § 6, § 7.1, § 8.1, § 8.2 (the playtest is deferred — do not build it).
- star-lord's `2026-06-15-star-lord-telegraph-export-schema.md` + its MIGRATION.md (the JSON schema, units, coordinate frame, shape vocabulary) — REQUIRED; do not start before it round-trip-PASSES.
- The spatial twin you already built: `canonical/story/battle-room-presentation-decoupling-2026-06-15.md` — the sim-invariant-vs-presentation discipline + the coordinate frame; this is its time-axis twin.
- Your battle-room scene + parity tooling: `reincarnated-godot/scripts/check_descent_parity.py`, `scenes/arena_descent.tscn`, `scripts/bake_descent_scene.sh` — the parity-check pattern to mirror for telegraph render==JSON.
- Genre render references: Diablo III/IV ground telegraphs, Hades red danger-zones, Souls wind-up reads — the render vocabulary.
- Disciplines #1, #2, #8 (schema validation at the consume boundary), #11.

## Math-before-code (Discipline #1) — produce FIRST, HALT for Gate-1
1. **The render mapping** — JSON danger-zone primitives → Godot rendered geometry (faithful; same frame; only star-lord's documented transform applied). Wind-up time → rendered timer.
2. **The dodge-resolution model (Godot-side)** — i-frame window vs danger-zone-exit: how the dodge input negates the hit (timing within the wind-up window AND/OR exiting the danger-zone shape — pick the model that matches the i-frame-roll design intent from dispatch 2's ruling §5).
3. **The round-trip parity assertion** — render geometry/timing vs JSON, in the spirit of `check_descent_parity.py`.

**HALT for jack-ryan Gate-1 on the render mapping + round-trip design before any code.**

## Scope
- [ ] Render-mapping + round-trip math-note FIRST; **HALT, Gate-1.**
- [ ] Consume the telegraph JSON (one-boss + glass-close-ST exemplar) per star-lord's schema.
- [ ] Render danger-zone shapes + wind-up timers, faithful to the JSON (same frame; only documented transform).
- [ ] Wire the dodge input; resolve it against the rendered telegraph (i-frame/zone-exit per the §5 design).
- [ ] Round-trip parity check: rendered geometry + timing == JSON source.
- [ ] AGENT_STATE.md updated; tag `drax/v1.x-telegraph-render-dodge-input`.

## Acceptance criteria
- [ ] Telegraphs render for the one-boss + glass-close-ST exemplar with danger-zone shape + wind-up timer.
- [ ] **Round-trip PASSES:** rendered danger-zone geometry + wind-up timing == the JSON star-lord exported (== the sim TelegraphSpec). Parity check proves it.
- [ ] The dodge input resolves against the rendered telegraph: timed-in-window/out-of-zone negates the hit; mistimed/in-zone does not.
- [ ] The dodge is read from the kit's exported skill list (not hardcoded Godot-side).
- [ ] NO viability playtest performed (deferred — § 8.2).

## Out of scope (explicit non-goals)
- **NO viability playtest / difficulty tuning / "is it clearable" judgment** — DEFERRED to a separate Matt go (§ 8.2). Build the instrument only.
- **NO re-deriving or "improving" the telegraph geometry Godot-side** — render the JSON faithfully (§ 7.1). Geometry/timing are invariant; only VFX styling is free.
- **NO hardcoded dodge** — read it from the exported kit (else it un-sources and drifts).
- **NO coverage beyond the one-boss + glass-close-ST exemplar first** (§ 8.1); extension is a follow-on.
- **NO regression of the battle-room parity contract** (spawn/footprint 35/35) — telegraphs render INTO the existing faithful scene, they do not perturb it.
- **NO push** (Matt-gated).

## Open questions for the agent to resolve (document in the math-note)
- The i-frame-window vs danger-zone-exit dodge model (match the §5 i-frame-roll intent; if ambiguous on feel, that's a design question — but per § 8.2 do NOT tune for clearability, just implement a faithful resolution).
- The render vocabulary for each danger-zone primitive (circle/cone/line/AABB) — keep to what increment-1's one boss needs.
- Whether the parity check runs as a Godot-side script or a cross-repo harness comparing JSON↔rendered (mirror `check_descent_parity.py`).

## Sequence
star-lord dispatch 4 round-trip-PASSES → jack-ryan Gate-1 on THIS dispatch → drax render-mapping math-note → **HALT, Gate-1** → drax implement + round-trip parity → jack-ryan Gate-2 (round-trip PASS = the gate) → **PIPELINE-COMPLETION GATE MET** (render==JSON==sim + dodge resolves). KR reports completion to Matt. The viability playtest fires on a SEPARATE Matt go thereafter (§ 8.2).

## Gate-2 watch-items (jack-ryan Gate-1 INFO — carry to Gate-2)
- **Composed tolerance across hops:** this dispatch asserts render==JSON; dispatch 4 asserts JSON==sim; render==sim holds transitively. If BOTH hops carry bounded tolerance on any transform, document the COMPOSED bound (render-vs-sim) at Gate-2 — confirm it stays within the faithfulness intent of § 7.1.
- **Transform-choice inheritance:** apply ONLY the coordinate-frame/axis transform star-lord documented in the dispatch-4 schema; confirm at Gate-2 that the frame drax reads matches the in-schema frame declaration (no ad-hoc re-framing).

## References
- STEP-0 ruling § 6/§ 7.1/§ 8.1/§ 8.2; star-lord dispatch 4 + its MIGRATION.md; spatial twin battle-room doc + `check_descent_parity.py`; dispatch 2 (the dodge source).
