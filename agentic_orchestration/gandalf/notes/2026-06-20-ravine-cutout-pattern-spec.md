# Ravine Cut-Out Pattern Spec — enchanted-forest, one level (at-grade-first)

**Status:** FIRING-READY pattern spec (the Drax build input). Pattern B disposition (Matt + gandalf, 2026-06-20). Two design choices locked by Matt: **2 pools**, **mostly-gentle meander with one quasi-snake**.
**Author:** gandalf (design steward).
**Parents:** `2026-06-20-enchanted-forest-target-aesthetic-rubric.md` (the scoring reference); the burn-down + carve-down-vs-build-up + trough-water dialogue this session; the floor-sizing research (`2026-06-20-arpg-room-sizing-monster-density-ravine-wfc.md`).
**Build order (Matt-locked):** find pattern → embed in ONE level AT GRADE (fully walkable, undulation, 50% shiny water, combatants) → **Matt Gate** → only then carve down 7-10 cliff-modules + add cross-log(s).

---

## 1. The footprint (plan view) — a meandering, alternating-width channel

One level = one ravine stretch along a primary down-gorge axis (+Z, into the committed ARPG camera). The footprint is the WALKABLE combat region; everything outside it is forest at grade.

**Beat sequence (down-axis):**
`entry-pinch → POOL 1 → connector-pinch(QUASI-SNAKE) → POOL 2 → exit-pinch`

| Beat | Width | Length | Role |
|---|---|---|---|
| entry-pinch | ~7 m | ~12 m | arrival corridor; first sightline into the gorge |
| **POOL 1** | ~18-20 m | ~20 m | TRASH arena — goblin pack (6-10 trash) |
| connector-pinch | ~6-7 m | ~14 m | **the quasi-snake** — tight S-bend; HIDES Pool 2 from Pool 1 (the reveal beat) |
| **POOL 2** | ~20-22 m | ~22 m | ELITE arena — elite goblin + shaman (SM_Bld_Shaman_01); brightest emissive hero element (climax) |
| exit-pinch | ~7 m | ~12 m | departure corridor |

Approx level extent: ~80-90 m long × ~36-40 m wide envelope (footprint max ~22 m + forest margin both sides).

**Meander (centerline):**
- **Mostly gentle:** entry, Pool 1, exit wander softly off-axis — long wavelength, low amplitude (~±4-6 m). Reads as a broad natural gorge; clean combat sightlines.
- **One quasi-snake:** the connector-pinch is a tighter S (amplitude ~±8-10 m, short wavelength) so POOL 2 IS NOT VISIBLE FROM POOL 1 — round the corner, the elite arena reveals. This is the single pronounced corner; everything else stays gentle.
- **Linear-now / turns-later:** the meander gives visual turns with NO topological branching — single enter→exit through-path. Harder snaking + U-shapes come free later by letting the centerline wander more; the footprint mechanism is unchanged.

## 2. Combat-surface rules (INSIDE the footprint) — validated non-interrupting

- **R-floor.** Combat plane is the footprint interior. Gentle undulation: every slope **navmesh-walkable (<~25-30°)**; amplitude **< character height (~<1 m)** so it NEVER breaks line-of-sight or creates cover. Verified earlier: gentle undulation does not interrupt ARPG combat.
- **R-water.** **Water pools in the undulation TROUGHS** (it flows downhill — physically correct). That trough coverage = the ~50%. The water is **fully walkable** (ankle-shin shallow, cosmetic, no movement debuff — never a barrier; a 50% barrier would funnel the fight and IS an interruption). The water is **emissive cyan/green** — per the rubric it is a PRIMARY light source, not just reflective. Shine lives in the troughs (between fighting); the raised dry islands stay **matte** for telegraph clarity.
- **R-islands.** Raised dry matte islands carry the combat + ALL spawns. Spawns never land mid-stream-deep.
- **R-dressing-gradient.** Combat islands = SPARSE dressing (keep AoE telegraphs readable). Footprint EDGES = densely overgrown (ferns spilling in, mushroom clusters, rock pebbles, roots) — meets the rubric "visually packed" density score without fouling combat.

## 3. Outside-the-footprint rules (the future rim, at grade)

- Dense forest at grade: framing trunks (Tree_Giant, Tree_Large), Background_Trees, heavy fern + mushroom overgrowth. REAL geometry continuing toward the skybox.
- This is what makes the eventual carve's massive-zone illusion GENUINE (not a faked false-front): when the footprint drops 7-10 modules, this at-grade forest becomes the rim above, and the player in the slot sees real forest continuing past the frustum.
- **Footprint boundary = the future cliff line.** At grade, mark it as an overgrowth/rock transition. On carve, it becomes the Dirt_Cliff_01..12 wall line (alternating variants down its length).

## 4. Emissive-led register (per rubric — the big correction)

The "enchanted" read is lit FROM WITHIN over a dark teal base (5-20% value shadows), NOT by broad daylight on surfaces.
- Primary light = emissive: glowing mushrooms (warm-amber caps + cyan/blue bioluminescent clusters), emissive trough-water (green/cyan), spore-mote particles (blue/violet).
- Cool green-cyan fog, medium density, depth-fading the background 30-50%.
- Concentrated bright hotspots (5-15% of frame), dark vignette edges.
- **Pool 2 gets the brightest emissive hero element** (a glowing pool / glowing great-tree / crystal cluster) — the climax focal.
- Goblin packs: Pool 1 trash goblins; Pool 2 elite goblin + SM_Bld_Shaman_01. Hero from Fantasy Characters pack. (Animations: Goblin Locomotion.)

## 5. Cross-log (Matt: "add a cross log or two")

Activates on CARVE (step 4): SM_Env_Log_01..04 spans a pinch (most legibly the connector-pinch / quasi-snake), becoming the literal cross-gorge bridge OVER the play space (overhead, not walkable — no false-affordance). At grade, pre-place one log focal spanning the connector-pinch so it's present in the gate scene (rubric §3 "natural bridge/overhang") and rises to span the gorge on carve.

## 6. Scoring + gate

- Drax self-scores the built scene against the rubric (§2 palette/lighting, §3 signatures, §5 weighted table, §6 anti-patterns — reproduce ZERO of the prior-run anti-patterns).
- **galadriel CV-scores** against the rubric before the Matt Gate.
- gandalf judges §1/§4 (does it READ as the target — mood, enclosure, depth hierarchy).
- Hand-off threshold (gandalf-proposed): composite ≥ 0.75 AND zero §6 auto-fails. Matt adjudicates the actual gate.
- **No carve until Matt passes the flat patterned scene.**

## Sign-off
gandalf, 2026-06-20. Pattern locked: 2 pools, gentle meander + one quasi-snake on the inter-pool connector (the reveal beat). At-grade-first; carve is a post-gate transform on an approved surface.
