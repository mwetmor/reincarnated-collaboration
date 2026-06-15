# Battle-room replication — design read + routing note (gamora · drax · galadriel · KR)

**Type:** routing + framing note (gandalf → gamora / drax / galadriel / KR). Render the engine's *actual* spatial battle rooms in Godot with Dark Fantasy assets, at register-2 parity.
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-authorized 2026-06-15 (Pattern-B) — *"yes please"* (to the offer to author this routing note).
**Parents:**
- `agentic_orchestration/gandalf/notes/2026-06-15-a-holds-extension-real-curated-content-ruling.md` (A-holds extension — this increment is the named **"second real biome" hardening gate**, repurposed as something stronger: a *spec-faithful battle room* that also demonstrates the sim→visual bridge).
- `agentic_orchestration/gandalf/notes/2026-06-15-dark-fantasy-pack-routing-note.md` (the asset drop + the marketing-render caveat discipline this note inherits 1:1).
**Spec source (load-bearing — what drax replicates):**
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` — the 6 `ArenaScenario` definitions (meter-precise dimensions + spawn positions).
- Math note: `reincarnated-engine/design/working-agreement/R2-spatial-combat-math-2026-05-19.md`; scenario design: `…/R2-scenario-design-2026-05-19.md`.
**Asset + recipe source:**
- Dark Fantasy pack: `~/Games/reincarnated-godot/Assets/Synty/polygon-dark-fantasy-01/`; reference frames `…/modular_asset_idea_pictures/{maps,theme}/`.
- Validated lift recipe: `reincarnated-godot/scenes/lift_render.tscn` (A-holds baseline) + `scenes/dark_fantasy_cathedral.tscn` (the curated 5.00/5 build).
- galadriel rubric harness: `register-metrics.mjs` / `lifecycle-score.mjs`; scorecard precedent `agentic_orchestration/galadriel/reports/2026-06-15-cathedral-register2-scorecard.md`.

---

## 0. One line

The engine's "battle simulation rooms" already EXIST as concrete, meter-precise specs — gamora's `spatial_gauntlet` defines **6 `ArenaScenario`s** with real geometry (dimensions + spawn positions + mob formations). This increment renders those *exact* footprints in Godot with Dark Fantasy assets at register-2 parity. drax **replicates** a spec he doesn't invent; galadriel scores parity; the new thing we learn is whether **register-2 premium and fight-readability coexist** in a spec-faithful fight room. It is the first sim→visual bridge AND a stronger form of the A-holds second-biome gate.

## 1. The source that exists (what drax replicates — NOT invents)

The 1D `fight_engine` is abstract (scalar distance). But the R2 **`spatial_gauntlet`** is a 2D spatial combat substrate with real arena geometry — origin at `(0,0)`, positions in meters, choke zones, spawn specs. The 6 scenarios (`ALL_SCENARIOS` in `arena.py`):

| Scenario constant | Footprint | Reads as | Mob composition (from spawn specs) |
|---|---|---|---|
| `SCENARIO_OPEN_ARENA` | **50 × 50 m** | open fight field | 8 swarmers (y≈8–18) vs player at y=40 |
| `SCENARIO_CHOKEPOINT` | **10 × 50 m** | dungeon corridor (narrow) | 8 swarmers funneled down a 10m-wide strand |
| `SCENARIO_ELITE_PACK` | **28 × 28 m** | elite pack room | elite pack |
| `SCENARIO_MAGIC_PACK` | **32.7 × 14 m** | wide caster room (shallow) | ranged caster pack |
| `SCENARIO_MINI_BOSS` | **30 × 30 m** | mini-boss chamber | mini-boss + escort |
| `SCENARIO_BOSS_WITH_ADDS` | **30 × 30 m** | boss arena | boss + adds |

These are renderable specs, not mood notes. "Exact fight specs" has a literal home: drax reads the dimensions + spawn positions and builds **that** footprint. **gamora confirms which scenario specs are frozen-for-replication** (the module is scaffolding-status — § 4).

## 2. The design read

**Two structural alignments make this a clean fit:**

1. **Dimensionality matches perfectly.** The arena is 2D — a ground-plane `(x,y)` layout. Our locked camera is the fixed elevated **2.5D**. The 2D arena footprint IS the floor plan the camera looks down on; Godot adds the vertical + the lift on top. No translation — the sim's flat arena is literally the room's floor.
2. **The 6 scenarios ARE the genre's dungeon-room grammar.** Open arena / chokepoint corridor / elite pack / caster pack / mini-boss / boss-with-adds is, near-verbatim, the **Diablo dungeon-encounter taxonomy** and PoE's map-arena vocabulary. Replicating them hands us the encounter grammar for free.

**Player consequence:** the player reads each room *type* instantly from the fixed camera — a 10×50 corridor feels like a chokepoint, a 30×30 boss square reads as an arena — because the spatial spec already encodes the encounter shape. We don't invent readability; the spec carries it.

## 3. What "EXACT" must mean — the discipline that keeps the proof honest

**The combat geometry is sacrosanct.** drax preserves arena dimensions + spawn positions faithfully and **dresses that exact footprint** with Dark Fantasy art. He does NOT resize the arena or move spawn points to compose a prettier shot — that breaks "exact replication" and reverts the work to a mood piece. **Art serves the spec.** This is precisely how Diablo's procedural dungeons work: the combat-functional layout graph is fixed; the tileset dresses it. Same contract here.

**The spike's real question (the load-bearing thing we learn):** the cathedral was a mood piece with NO fight-readability constraint — it could be as dark and cluttered as the lift wanted. A *battle room* must satisfy three things at once: (a) render the **exact** spawn geometry, (b) stay **readable** from the fixed 2.5D camera (every combatant visible + parseable), and (c) still hold **register-2**. These can fight each other — a near-black premium room may be too dark to read a 12-mob pack in. **Do register-2 premium and fight-readability coexist in a spec-faithful fight room?** That is the new axis, and it is load-bearing for the whole game (every fight happens in one of these rooms).

**A design finding the corridor may force:** a `10×50` corridor under a *fixed* elevated camera is a hard composition — long and thin; the camera either sees a slice (loses the length) or pulls back (mobs go tiny). The spike may reveal that the "fixed" camera needs a **follow-mode for long footprints** while staying fixed for square arenas. That is a real camera-design finding the corridor would surface — flag it as an expected, valuable output, not a failure.

## 4. The caveats (load-bearing — protect the build/score)

1. **The marketing-render caveat carries 1:1 from the Dark Fantasy routing note.** The `modular_asset_idea_pictures` frames are Synty's own marketing renders — calibration/mood anchor, **NOT the pass bar.** galadriel scores our built scene against the **register-2 rubric** (composite ≥3.6; **lighting ≥4 AND VFX ≥4 mandatory**), **lifecycle-sampled** (stills under-represent VFX per F1). **Parity = rubric pass, not pixel-match.** drax builds to the rubric + the proven lift recipe, not to matching a marketing post.
2. **`spatial_gauntlet` is SCAFFOLDING status** — jack-ryan Gate-1 not yet passed (per the module docstring). The `ArenaScenario` *geometry* is stable enough to render; treat current dimensions as the **v1 spec** and expect possible refinement. **gamora confirms the frozen-for-replication specs at handoff.** Not a blocker — the 6 archetypes won't change fundamentally; only dimensions might drift.
3. **Placeholder combatants are fine — and this is WHY the sequencing is right.** drax stands composed Synty Dark Fantasy characters (skeletons; the composed knight) in the spawn positions, exactly as the A-holds graybox used the composed knight. This needs **none** of the Blender character-creation modularity — which is why running this *before* the character work is sound. The battle room proves the **arena**; the character creator (next) proves the **combatant**. Clean decouple.

## 5. Routing

- **gamora (spec handoff):** confirm which `ArenaScenario` specs are frozen-for-replication (dimensions + spawn positions + mob composition per scenario). Hand drax the v1 spec set. Owns the spatial model; the only seam that can certify the specs are stable to render.
- **drax (build):** for each nominated scenario, build a Godot scene that replicates the **exact** footprint + spawn geometry (§ 3), dressed with Dark Fantasy assets via the validated lift recipe, composed fight-readable for the fixed 2.5D camera. Reference frames for mood/asset-selection only (§ 4.1).
- **galadriel (score):** lifecycle-score each built room against the register-2 rubric (parity = rubric, not pixel-match). Add a fight-readability read alongside the register axes — can every combatant be located + parsed from the fixed camera. Produce a scorecard as for the cathedral.
- **jack-ryan:** the spatial-gauntlet Gate-1 he already owes **intersects** here — a visual replication of the arenas is incidental pressure to firm the spec. Coordinate, don't gate the visual increment on it.
- **gandalf:** design-coherence read; author the canonical update if the score fires (§ 7).
- **KR (sequence):** gamora spec-handoff → drax build → galadriel score, as the **"render the battle rooms at register-2 parity"** increment. Not blocking WS1 (balance) — orthogonal. Fires on Matt greenlight.

## 6. Build sequence (gandalf nomination — footprint-diversity, NOT three similar rooms)

Spike **3 scenarios chosen for maximal geometric coverage**, so a pass proves the lift generalizes across arena *shapes*, not just one shape thrice:

- **Build #1 — `BOSS_WITH_ADDS` (30×30).** Lowest-risk, highest-value first proof: a 30×30 enclosed square is closest to the **already-validated cathedral** (the proven dark-interior recipe transfers most directly), and it is the marquee room type (the trial-boss arena — load-bearing structural surface). Establishes the spec-faithful baseline.
- **Build #2 — `CHOKEPOINT` (10×50).** The high-information stress case: the **most distinct footprint** (long narrow corridor) — proves the lift holds on geometry radically unlike the cathedral square — AND it is a 8-swarmer scenario, so it tests fight-readability at its sharpest (many small mobs, tight space) and is the room most likely to surface the fixed-vs-follow camera finding (§ 3). Only attempt after #1 lands.
- **Build #3 — `MAGIC_PACK` (32.7×14).** The wide-shallow footprint — rounds out the coverage (square / corridor / wide-shallow = three genuinely different camera problems) and tests a ranged-caster spread across the back of a shallow room.

*(Skip `MINI_BOSS` 30×30 for the spike — geometrically identical to `BOSS_WITH_ADDS`; redundant on the shape axis. `OPEN_ARENA` 50×50 and `ELITE_PACK` 28×28 round out the full set once the spike's 3 prove the pipeline.)*

## 7. Canonical trigger (what makes this a canon update vs. just an increment)

This note is a routing/framing artifact, **not** a canonical doc. The canonical moment is downstream: **if galadriel scores drax's spec-faithful battle rooms at register-2 parity**, that is a *second, stronger* A-holds extension — from "one curated mood environment" to **"N spec-faithful battle rooms, across diverse footprints, sim-driven, fight-readable."** That establishes three things the cathedral did not:

1. the lift holds on **constraint-bound** geometry (footprints chosen for combat-math, not visual drama);
2. **register-2 premium + fight-readability coexist** (the new axis);
3. the **sim→visual bridge is demonstrated** — the abstract spatial sim renders as a register-2 world.

It also satisfies the A-holds **"second real biome"** hardening gate (content-agnostic: inference → demonstration) and does so across *multiple* footprints — stronger than one arbitrary second biome. THAT is the canonical update (an A-holds second-extension + a style-register note). **Recognition discipline: the canon fires on the score, not on the build.**

---

**Signed:** gandalf, 2026-06-15
**For:** routing the battle-room replication increment — the engine's `spatial_gauntlet` already defines 6 meter-precise `ArenaScenario` battle rooms (open arena / chokepoint corridor / elite + caster packs / mini-boss / boss-with-adds = the Diablo dungeon-encounter grammar); the 2D arena footprint maps 1:1 to the fixed 2.5D camera's floor plan; drax replicates the *exact* footprint + spawn geometry (combat geometry sacrosanct, Dark Fantasy art dresses it — Diablo procedural-dungeon contract), galadriel lifecycle-scores register-2 **parity** (rubric not pixel-match, marketing-render caveat carried 1:1) plus a fight-readability read, gamora confirms the frozen-for-replication specs (module is scaffolding-status), placeholder Synty combatants defer the Blender character work cleanly; spike 3 footprint-diverse scenarios first (boss-square / corridor / wide-shallow); the canonical moment is downstream and fires on the score — a stronger second A-holds extension proving the lift on constraint-bound geometry, register-2 + readability coexistence, and the first sim→visual bridge.
