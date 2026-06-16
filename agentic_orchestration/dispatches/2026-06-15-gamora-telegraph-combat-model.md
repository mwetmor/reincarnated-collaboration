# Dispatch — 2026-06-15 — gamora — telegraph combat-model (wind-up time + danger-zone shape)

**Status:** ✅ FIRE-READY — jack-ryan Gate-1 (DESIGN-MODE) CLEAR-WITH-AMENDMENTS 2026-06-15 (A3-1, CL-3 folded); fire-able after dispatch 1 lands (CL-3). Critical-path heart.
**From:** knight-rider
**To:** gamora
**Pre-fire gate:** jack-ryan Gate-1 (DESIGN-MODE) on this dispatch BEFORE it fires.
**Estimated effort:** Pattern B (multi-session — this is the LOAD-BEARING CONTENT of the whole bridge).
**Parent ruling (STEP 0):** `canonical/story/telegraph-dodge-temporal-decoupling-2026-06-15.md` § 2 (the temporal decoupling), § 6 (Move 3 step 1), § 7.1 (the no-drift invariant — gamora is the SOURCE), § 7.2 (inert-in-sim).

## What this is — Move 3, step 1: the load-bearing content (NOT plumbing)

This is the critical-path heart. Each boss attack gets a defined **wind-up TIME** (how long the pre-move telegraphs before it lands) and **danger-zone SHAPE** (the space the attack covers), wired into the sim's **action resolution**. The ruling is explicit (§ 6): *if the sim currently resolves a hit as "deal X at action tick T," this telegraph model does NOT yet exist — it is a combat-model extension, the load-bearing content (it IS the dodge game), not JSON plumbing. Scope it as such.*

gamora is the **single source of truth** for the telegraph (§ 7.1). The TelegraphSpec defined here is the one object that star-lord serializes (dispatch 4) and Godot renders (dispatch 5). No drift starts with a clean, complete source definition here.

## THE INVARIANT + THE DISCIPLINE (name from line one)

- **§ 7.1 — one telegraph source, two consumers, no drift.** The telegraph the sim COSTS must EQUAL the telegraph Godot renders. A single TelegraphSpec definition; the sim consumes it to cost/flag, star-lord serializes it, Godot renders it. Design the TelegraphSpec as the canonical contract object from the first line — not as a field bolted on later. This mirrors the battle-room wall-ring invariant (spatial twin).
- **§ 7.2 — the dodge is INERT in the sim.** Compute the telegraph and, in the sim, resolve the boss attack as it resolves today: **the attack LANDS (full damage); there is NO dodge in the autobattle.** The telegraph is COMPUTED + COSTED + EXPORTED, but its avoidance is a Godot-only layer. **Do NOT add a probabilistic dodge/avoidance term to the sim** — that re-imports the exact faking dispatch 1 deletes. After this dispatch, the sim must STILL wall glass-close-ST and STILL flag it dodge-gated.
- **(CL-3, jack-ryan Gate-1 — sequencing) This dispatch ASSUMES dispatch 1 (flag-and-defer) has already landed in the gamora queue.** The § 7.2 regression-guard asserts against the *already-honest* baseline (post-flag-and-defer): telegraphs must change no balance result AND the `dodge-gated` flag from dispatch 1 must be PRESERVED. KR sequences dispatch 1 before dispatch 3 within gamora's queue so the guard asserts against a fixed baseline, not a moving one.

## ⚠ CHECK FIRST: is there reusable telegraph machinery? (KR coordination)
`src/reincarnated/simulation/spatial_gauntlet/arena.py` already references telegraph/wind-up/danger-zone concepts. **First task: audit whether the spatial-gauntlet arena already models any of this** — wind-up timing, danger-zone shapes, spatial hit resolution. If reusable, extend it (do not re-invent); if it is a different abstraction (e.g., a positional gauntlet unrelated to per-attack telegraphs), say so and design the TelegraphSpec fresh. Report the audit result in the math-note before designing.

## What the TelegraphSpec must capture (design it complete — Godot depends on it)
The downstream render + dodge-resolution (dispatch 5) can only be faithful if the SOURCE is complete. At minimum, per boss attack:
- **wind-up time** — duration of the telegraph before the hit lands (sim time units; define the unit explicitly so star-lord/Godot share it).
- **danger-zone shape** — the geometry the attack covers (define the shape primitives: e.g., circle/cone/line/AABB + origin + extent + orientation, in the sim's coordinate frame — the SAME frame the battle-room spatial decoupling fixes for spawn/damage geometry, so telegraphs land where the sim says damage lands).
- **(A3-1, jack-ryan Gate-1 — pins the one unit-drift vector at the source) spatial UNIT of the danger-zone geometry** — declare it explicitly (tiles vs sim-world-units) and IDENTICAL to the battle-room spawn/damage-geometry unit, so star-lord and drax inherit ONE unambiguous spatial unit. A telegraph defined in tiles but rendered as meters is exactly the silent drift § 7.1 exists to prevent — and it enters at the SOURCE if the unit is not pinned here. (Wind-up time gets the same explicit-unit treatment per above.)
- **attack identity** — a stable id linking the telegraph to its boss attack (so the round-trip can assert sim-telegraph == rendered-telegraph per attack).
- **timing anchor** — WHEN in the fight timeline the telegraph fires (the action tick), so Godot can place it on its rendered timeline.
- **damage payload linkage** — the hit the telegraph precedes (so a dodge in Godot negates the right damage; in the sim the damage always applies).

**Coordinate-frame consistency (load-bearing):** the danger-zone shape MUST be expressed in the same spatial frame as the battle-room sim-invariant (spawn positions / where damage lands — see the spatial-twin doc). A telegraph that disagrees with the damage geometry is drift by construction.

## Cross-seam contract change? (Principle 6 gate — KR assessment; gamora resolves)
**Assessment: YES — this is a cross-seam contract change (ADR-004).** The TelegraphSpec is a NEW data structure produced at the gamora→star-lord boundary; star-lord (dispatch 4) serializes it. **MIGRATION.md REQUIRED** at the simulation seam documenting the TelegraphSpec shape + the timing/coordinate-frame units, addressed to star-lord. The round-trip smoke is OWNED by star-lord (dispatch 4) but gamora must provide a **production-path fixture**: a real fight on one boss + the glass-close-ST exemplar that emits TelegraphSpecs, so star-lord exercises the boundary against real data, not a hand-built stub.
- `Round-trip: gamora provides the production fixture (one-boss + glass-close-ST exemplar fight emitting TelegraphSpecs); star-lord's dispatch-4 export round-trip consumes it.`

## Required reading before starting
- STEP-0 ruling § 2, § 6, § 7.1, § 7.2, § 8.1 (the round-trip gate).
- The spatial twin `canonical/story/battle-room-presentation-decoupling-2026-06-15.md` — the coordinate frame + the invariant-discipline you are mirroring on the time axis.
- `src/reincarnated/simulation/spatial_gauntlet/arena.py` — the existing telegraph-adjacent machinery to audit/reuse.
- The action-resolution path (where "deal X at tick T" lives) — `damage_resolver.py`, `gauntlet_sim.py` (cite the resolution site you extend).
- Disciplines #1 (math-first — telegraph geometry is math), #1.1 (resource-bounds if the telegraph model adds per-attack compute over batch runs), #2/#2.1 (smoke + resource-scaling), #11, #12.

## Math-before-code (Discipline #1) — MANDATORY math-note; produce FIRST, HALT for Gate-1
1. **The spatial-gauntlet reuse audit** (above) — reuse vs fresh.
2. **The TelegraphSpec geometry** — the shape primitives + their math (a cone is origin+angle+radius; a line is origin+direction+length+width; etc.), the timing model (wind-up duration + fire tick), the coordinate frame (= the sim-invariant frame), and the units (so star-lord/Godot inherit them unambiguously).
3. **The resolution wiring** — how the telegraph attaches to action resolution WITHOUT changing sim outcomes: the attack still lands full damage; assert (smoke) that introducing telegraphs does NOT change any existing balance result (the telegraph is additive metadata + an inert avoidance layer, not a damage change). **This is the § 7.2 proof: the sim still walls glass-close-ST identically.**
4. **The cross-seam contract** (MIGRATION.md content) — the TelegraphSpec the star-lord export must match.
5. **Resource-bounds (#1.1)** — peak memory/compute of emitting TelegraphSpecs across a batch run; verify against host RAM (the season runs are large).

**HALT for MANDATORY jack-ryan Gate-1 on the telegraph math-note before any code.**

## Scope
- [ ] Math-note FIRST (incl. spatial-gauntlet audit + § 7.2 no-change proof + resource-bounds); **HALT, MANDATORY Gate-1.**
- [ ] Define the canonical TelegraphSpec (complete per the "must capture" list, in the sim-invariant coordinate frame).
- [ ] Wire telegraph computation into action resolution — additive; the boss attack still lands full damage; NO sim dodge term.
- [ ] Emit TelegraphSpecs on a real fight (one boss + glass-close-ST exemplar) as the production fixture for dispatch 4.
- [ ] Prove the sim STILL walls glass-close-ST identically (§ 7.2 regression guard).
- [ ] MIGRATION.md (gamora→star-lord) — TelegraphSpec shape + units + coordinate frame.
- [ ] Smoke + resource-scaling rehearsal (#2.1); AGENT_STATE.md; tag `gamora/v1.x-telegraph-combat-model`.

## Acceptance criteria
- [ ] A defined wind-up time + danger-zone shape exists per boss attack, in the sim-invariant coordinate frame, with a stable attack id + fire-tick.
- [ ] Introducing telegraphs changes NO existing balance result (telegraphs are additive; the sim still walls glass-close-ST identically) — smoke-proven.
- [ ] NO probabilistic dodge/avoidance term in the sim (§ 7.2) — code-cited absence.
- [ ] MIGRATION.md authored for star-lord with the complete TelegraphSpec contract + units.
- [ ] Round-trip: gamora provides the one-boss + glass-close-ST production fixture emitting TelegraphSpecs (star-lord's dispatch-4 round-trip consumes it).
- [ ] Resource-bounds projected + verified against host RAM (#1.1).

## Out of scope (explicit non-goals)
- **NO export/JSON serialization** — that is star-lord (dispatch 4). gamora defines + emits the in-sim TelegraphSpec; star-lord serializes it.
- **NO Godot/render/input work** — dispatch 5.
- **NO dodge modeling in the sim** (§ 7.2).
- **NO balance re-tuning** off the telegraphs (the telegraph does not change sim damage; if it appears to, that is a bug → HALT).
- **NO coverage beyond the one-boss + glass-close-ST exemplar first** (§ 8.1 — first increment of the real pipeline; coverage extension is a follow-on).
- **NO push** (Matt-gated).

## Open questions for the agent to resolve (document in the math-note)
- Reuse spatial_gauntlet/arena.py vs fresh TelegraphSpec.
- The shape-primitive vocabulary (which shapes the bosses actually need for increment-1; keep minimal, extend later).
- The timing-unit + coordinate-frame definitions star-lord/Godot will inherit (get these RIGHT — they are the no-drift anchor).

## Sequence
jack-ryan Gate-1 on this dispatch → gamora telegraph math-note → **HALT, MANDATORY Gate-1** → gamora implement + emit fixture → jack-ryan Gate-2 → **star-lord dispatch 4 (export) fires off the MIGRATION.md contract** → **drax dispatch 5 (Godot) fires off the export schema** → ROUND-TRIP GATE. Critical path; this dispatch gates 4 and 5.

## References
- STEP-0 ruling § 2/§ 6/§ 7.1/§ 7.2/§ 8.1; spatial twin battle-room doc; reframe b23dce3.
