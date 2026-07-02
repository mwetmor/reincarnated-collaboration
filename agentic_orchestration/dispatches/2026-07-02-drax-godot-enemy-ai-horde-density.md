# Dispatch — 2026-07-02 — drax — enemy AI baseline + horde-density rendering (D7)

**From:** knight-rider
**To:** drax
**Approved by:** Matt 2026-07-02 (one-realm §6.4)
**Estimated effort:** 4–6 days
**Acceptance:** enemy AI baseline + horde-density RENDERING — 50+ enemies on screen at min-spec for the escape; balance hand-tuned. Certification-at-density stays launch (III.3).
**Status:** GATED on D5 (verbs) + D6 (floors). Gate-1 required before execution. **Matt directive 2026-07-02: a density-per-area spec + a min-spec perf spike are slotted AHEAD of / WITH this dispatch** — de-risk 50+ at min-spec BEFORE committing the full AI+horde build (see the Density de-risk section below + D10).

## Context

§6.4: "Enemy AI baseline + horde-density *rendering* for the escape (50+ on screen at min-spec; balance hand-tuned)." The escape (§23.3, §1 step 5) is THE trailer: reap the champion = become it, combine the conduits, erupt the realm, flee as the stolen god-body "plowing through the soldier-mass." That soldier-mass is the horde — a **rendering** problem at min-spec, NOT a sim certification problem. The tracker is explicit (III.3): the demo's density need is Godot RENDERING at min-spec; certification-at-density lags to launch. Balance is **hand-tuned** by playtest (§5.3), not sim-certified.

## Required reading before starting

- `canonical/reap-die-rise-game/one-realm-mvp-scope.md` §6.4, §1 step 5 (the escape), §2 (min-spec floor non-negotiable), §5.3 ("escape fodder density = hand-tuned; Godot renders the mass; certification-at-density lags")
- `canonical/reap-die-rise-story/gameplay-loop-design.md` §23.3 (the escape crescendo — generous-but-urgent clock; "winning must feel won")
- `current-to-end-state-engine.md` III.3 (LAUNCH-SCOPE for sim certification — the demo's density is a render need)
- D5 verbs + D6 floors + D10 min-spec cadence (50+ at min-spec is THE perf hotspot)

## Cross-seam contract change? (Principle 6 gate)

Presentation-side AI + rendering; no engine schema change. Density is hand-tuned, not sim-certified — do NOT reach for the engine's density certification (III.3, launch).
- `Round-trip: not applicable — presentation AI + render; balance hand-tuned; no cross-seam contract or sim certification invoked.`

## Density de-risk — PRECEDES the full build (Matt directive 2026-07-02)

Before committing the full AI+horde build, land two de-risk artifacts (ahead of / with this dispatch):
- **Density-per-area spec** — define the target on-screen entity density *per playable area* (enemies + player summon-proxies combined; the escape scene is the max-density case). This spec is what D10's min-spec gate measures against and what D5's summon-cap coordinates with. It converts "50+ on screen" into a per-area budget the loader/floors can honor.
- **Min-spec perf spike** — a throwaway GTX-1650-class perf spike proving the density-per-area target renders at the min-spec framerate floor (D10). This is D10's first real application. If the spike fails the floor, the density spec re-budgets (or the render technique changes) BEFORE the full build — not after.

**Rationale:** the escape is the trailer (§23.3); discovering a min-spec density wall after building the full AI is the expensive path. Spike first.

## Scope

- [ ] **Density-per-area spec** (per-area entity budget; enemies + summon-proxies; escape = max case) — precedes the build
- [ ] **Min-spec perf spike** (throwaway; proves the density target holds at the GTX-1650-class floor — D10's first application) — precedes the build
- [ ] Enemy AI baseline (pursue / attack / the escape's soldier-mass behavior)
- [ ] Horde-density rendering: 50+ enemies on screen **at min-spec** (GTX-1650-class — D10 gate is load-bearing here)
- [ ] The escape "plow through the soldier-mass" feel (§1 step 5, §23.3 crescendo)
- [ ] Escape clock: generous-but-urgent (§23.3 — winning must feel won)
- [ ] Balance hand-tuned by playtest (NOT sim-certified)
- [ ] Min-spec verification per D10 — this is the make-or-break perf dispatch
- [ ] AGENT_STATE updated
- [ ] Tag: `drax/v-godot-enemy-ai-horde-1`

## Acceptance criteria

- [ ] 50+ enemies render on screen at min-spec (GTX-1650-class) during the escape — D10 gate PASS at density
- [ ] Enemy AI baseline drives the descent encounters + the escape soldier-mass
- [ ] The escape reads as the crescendo (§23.3 — generous-but-urgent, winning feels won)
- [ ] Balance hand-tuned (documented as playtest-tuned, not sim-certified)

## Out of scope (explicit non-goals)

- Sim certification-at-density (III.3, launch — the demo renders the mass, doesn't certify it)
- Enemy AI depth beyond baseline (launch)
- `SCENARIO_OVERRUN` certification (§4 OUT, launch)
- The becoming/conduit-combination logic itself (that's the run-stitch/escape-trigger work; this dispatch is the enemy-mass + AI it plows through)
- Nemesis / enemies-that-remember-you (patent hygiene, §2)

## Quality criterion

**Game-quality goal:** the escape crescendo — the trailer moment — lands: the stolen god-body plows through a rendered soldier-mass at min-spec, winning feels won. This is the autoplay clip that drives wishlists (§7 streamability).

**Refutation conditions (surface if any apply):**
- 50+ at min-spec tanks framerate (the escape is the trailer — a stuttering trailer is a net negative; §2 min-spec floor)
- The escape feels un-won (clock too tight or too loose — §23.3 generous-but-urgent band)
- The team reaches for sim density certification (III.3 is launch — the demo hand-tunes)
- AI drifts toward remembering the player (patent hygiene)

## Open questions for the agent to resolve (document)

- Render technique for 50+ at min-spec (MultiMesh / GPU instancing / LOD) — your call, min-spec governs
- On-screen proxy (summon) count + enemy count combined budget (coordinate with D5's summon cap)

## References

- one-realm-mvp-scope.md §6.4/§1/§2/§5.3 · gameplay-loop-design §23.3 · current-to-end-state-engine.md III.3
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md`
