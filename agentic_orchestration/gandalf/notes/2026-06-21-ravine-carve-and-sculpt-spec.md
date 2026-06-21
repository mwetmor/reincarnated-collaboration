# Ravine Carve + Post-Carve Sculpt/Dress Spec — enchanted-forest

**Status:** BUILD CONTRACT (the Drax carve input). GATED — does not fire until (1) the at-grade polish Pass 1 lands + I eye-verify, and (2) the baked at-grade scene is saved. Authored ahead so it's ready at the gate.
**Author:** gandalf (design steward), 2026-06-21.
**Parents:** `2026-06-20-ravine-cutout-pattern-spec.md` (the at-grade build contract — the carve is a transform on THAT approved surface); `2026-06-20-ravine-atgrade-matt-gate-package.md` (the gate package); `2026-06-20-enchanted-forest-target-aesthetic-rubric.md` (the GPT-5.4 scoring target). Matt's 2026-06-21 carve+dressing directive.

---

## 0. Where this sits in the sequence

```
[DONE]      at-grade patterned scene, real POLYGON assets, tripod-passed
[DONE]      hero native-walk fix (Base Locomotion Sidekick clip, no hack)
[IN FLIGHT] Pass 1 polish: giant-card fix (camera blockage) + spore squares + enemy idle + water slab
[GATE]      gandalf eye-verify Pass 1  →  SAVE baked at-grade scene
[THIS SPEC] CARVE the ravine (new scene, transform of the approved surface)
[THIS SPEC] post-carve wall sculpt + dressing
[GATE]      tripod (galadriel CV + drax self-score + gandalf §1/§4)  →  Matt Gate
```

**Discipline preserved:** the carve is a NEW scene (`scenes/ravine_carved.tscn`), built by transforming the approved at-grade surface. Do NOT destroy or overwrite the approved `ravine_atgrade.tscn` — it is the gate artifact and the illusion's "real rim forest" source. The footprint mechanism is unchanged by the carve.

## 1. The carve itself (the core transform)

- **Drop the channel.** Lower the walkable footprint interior 7-10 `Dirt_Cliff` modules below grade. The at-grade rim forest (dense trunks + overgrowth built outside the footprint) stays at grade and becomes the genuine massive-zone illusion ABOVE the player — real geometry continuing past the frustum, restricted only by wall height (per the no-black / massive-zone ruleset already validated).
- **Footprint boundary = the cliff line.** The overgrowth/rock transition that marked the footprint edge at grade becomes the `Dirt_Cliff_01..12` wall line, alternating variants down its length for non-repeating rock.
- **Raise the cross-log.** The pre-placed `SM_Env_Log_01` spanning the connector-pinch (quasi-snake) rises to span the gorge OVERHEAD as the cross-log bridge — non-walkable, no false affordance. "A cross log or two" (Matt): connector-pinch is the primary; a second may span the entry- or exit-pinch if it reads naturally.

## 2. Wall sculpt — tapered overhangs (Matt's directive, verbatim intent)

The defining move: the ravine should feel like a sculpted natural gorge, not a flat-walled trench.

- **Overhang taper.** Most rock faces are **wider at the BOTTOM than at the TOP** → the walls lean IN over the play space, producing overhangs. This is the opposite of a box trench; it makes the slot feel enclosed and ancient, and it tightens the "restricted only by wall height" illusion (the player can't see straight up out — the overhang caps the sightline).
- **Smooth rock, not flat wall.** Sculpt the faces to read as **smooth rounded rock masses**, not flat planes. Break the wall plane with bulges, recesses, and rounded outcrops. Low-poly faceting is fine (Synty register) — "smooth" = the silhouette curves, not that it's high-poly.
- **Some down-angled edges.** Not every face overhangs uniformly — **some rock edges taper DOWN at an angle** (sloping outcrops, leaning shelves) for variety. Mix overhang + down-angle so the wall line is irregular.
- **Variant alternation** down the gorge length so no two adjacent wall sections read identical.

## 3. On the overhangs / upper rim (atop the carved walls)

- **Ferns atop overhangs/outcrops** — fern clusters perched on the outcrop tops + rim, some spilling over the edge toward the gorge (vegetation-spilling-over-edges is a rubric §3 [CRITICAL] signature).
- **Vines wrap the log bridge** — hanging vines/roots around and dangling from the cross-log (rubric §3 supporting: hanging vines/roots bridging the ravine).
- **Leaf piles on the upper level** — small leaves strewn across the rim's top-most surfaces, **accumulating in wide piles** (drifts in low spots / against trunk bases). Naturalistic ground litter; adds the "visually packed / heavily overgrown" density the rubric scores (Vegetation density 10%).

## 4. Within the ravine (the play space dressing)

- **Magical flowing VFX current — intermittent visibility.** A flowing emissive current along the gorge floor (in the undulation troughs, where water already pools) that is **sometimes visible, other times transparent** — opacity pulses/fades in and out so the magic reads as alive and uncanny, not a static ribbon. This IS the rubric §3 [CRITICAL] "glowing green ravine/stream/chasm" + a chunk of the Emissive-magic 12% weight. Cyan/green emissive; flow direction down-gorge (+Z). Keep it walkable/cosmetic (no movement barrier — same rule as the trough water).
- **Leaves + moss on the top-most rock surfaces** — moss caps + scattered leaves on the upper faces of the in-gorge rocks and islands (top surfaces catch the litter; undersides stay bare rock). Naturalism + density.
- **A few ferns** tucked in corners next to the walls, or perched atop a rock here and there — sparse, accenting, NOT on the combat islands themselves (keep AoE telegraphs readable per the R-dressing-gradient rule).
- **Downward roots in a few places** — smooth small patches of tree roots growing DOWN from the rim trees, descending the overhang faces (the at-grade rim trees' roots breaking through the carved wall). A few placements only; reads as the forest above intruding into the gorge.
- **Small mushrooms (distinct from the large hero mushrooms).** Small mushroom assets that fit at the **bottom and along the sides** of the ravine — **mostly BLUE/cyan, some green and yellow**. These are the rubric §3 [CRITICAL] "bioluminescent blue/cyan mushrooms near ground and cliff edges" — a signature the at-grade scene under-served. They carry the cool bioluminescent accent; cluster them at wall bases, in rock crevices, and along the trough edges. Source the small `SM_Env_Mushroom_*` variants (NOT the large `Mushroom_Giant` hero forms); skin/emissive-tint blue/cyan primary, sprinkle green + yellow.

## 5. Register + combat constraints carried forward (do not regress)

- **Emissive-led** over dark teal base (5-20% value) — the carve must stay nocturnal/enchanted, not open up to daylight. Deeper walls = darker base = MORE emissive contrast (good).
- **Combat unbroken.** Floor stays navmesh-walkable; undulation amplitude < character height (no LoS breaks / unintended cover); spawns on dry matte islands; water + current cosmetic + walkable. The carve drops the whole footprint as a unit — it does not add in-play verticality the combat sim doesn't model.
- **No SIMPLE assets, ever** (mechanical guard must stay green). POLYGON line only.
- **Pool 2 keeps the brightest emissive hero element** (the climax focal) — the carve + current must not steal its primacy.

## 6. Scoring + gate (unchanged tripod)

- Drax self-scores the carved+dressed scene against the rubric (§2 palette/lighting, §3 signatures incl. the now-added blue mushrooms + flowing current + overhang vines/roots, §5 weighted table, §6 anti-patterns = ZERO).
- galadriel CV-scores against the rubric.
- gandalf judges §1/§4 (does it READ as the target — mood, enclosure, depth hierarchy; does the overhang make the slot feel enclosed and vast-above).
- Threshold: composite ≥ 0.75 AND zero §6 auto-fails. **Matt adjudicates the actual gate.**

## Revision 1 — post-first-carve correction (Matt, 2026-06-21, viewing the carved run)

The first carve (CARVE_D = 8.0 m uniform; env ambient lowered + key light → 0.38) over-rotated into dark enclosure. Frame `ravine_carved_10_carve_floor_downgorge` reads murky-dark on the floor; frame `ravine_carved_06_carve_up_pool1` (looking up the wall) is a near-pure-black void with no sky. Matt's two corrections — both targeting "more light reaches the bottom":

**R1-A — Sky sliver + sun (fill light, depth-hierarchy framing).**
- Add a faint **slightly-blue sky** visible as a SLIVER at the very TOP of the rim trees — the narrow band of sky above the gorge when the eye travels up. This is the depth-hierarchy framing the carve lost: a bright far-above sliver over the dark enclosed gorge (the shaft-of-sky-into-the-deep read), replacing frame-06's pure black.
- Add a **sun** (DirectionalLight3D) as **FILL, not KEY** — low energy, soft/low-shadow, tuned so the gorge FLOOR lifts from murky-black to dark-teal-LEGIBLE. Its job is floor readability + a touch of warmth down the walls, NOT to daylight the scene.
- **Register guard (CRITICAL — do not regress the locked emissive-led register):** keep it SLIGHT. Sky stays a thin sliver (small % of frame); sun fill must keep the base value in the 5–20% band and must NOT wash the emissive contrast (mushrooms / current / hero focal still POP as the primary light). "Slightly-blue sky reaching down into an enchanted gorge" ≠ "daylit forest." galadriel CV re-scores to confirm dark-first/lit-from-within still holds (neutral-gray near zero, emissive hotspots 5–15%).

**R1-B — Shallower, VARIABLE depth (mushroom-height referenced).** Replace the uniform 8 m drop:
- **Shallow point ≈ 1 × large-mushroom height. Deep point ≈ 1.5 × large-mushroom height.** Anchor "large-mushroom height" to the **measured rendered world-height of the largest hero mushrooms actually placed** (`SM_Env_Mushroom_01/02` at the scale-~1.6–2.0 Pool-2 placements) — drax MEASURES the exact AABB.y × placement-scale and reports the number; depth follows from it. (Estimate for sanity-check only: large mushroom renders ~4–6 m → walls ~4–6 m shallow to ~6–9 m deep; net meaningfully BELOW the current uniform 8 m, and varying.)
- **Depth varies ALONG the gorge** (not one flat trench): shallowest at the **entry-pinch** (you step gently down into it), deepening toward the **connector-reveal / Pool-2 climax** (a descent-into-depth as you near the boss — a mythic descent beat), easing back at the exit. 
- **Combat constraint preserved:** the play FLOOR within any pool stays locally flat + navmesh-walkable; any grade change along the through-axis stays gentle (<~25–30°, same rule as the undulation) so it adds no LoS-breaking verticality the combat sim doesn't model. Implementation (vary floor-drop vs vary rim-height) is drax's call under that constraint; the VISUAL outcome is the gorge reading ~1 mushroom deep in shallow stretches and ~1.5 deep at the climax.
- **Reinforces R1-A:** shallower walls + less aggressive overhang capping = more sky reaches the floor naturally; the two corrections compound.

R1 re-runs the full tripod (drax self-score + galadriel CV + gandalf §1/§4) before the Matt Gate — specifically confirming the register survived the sky/sun addition.

## Revision 2 — post-R1 correction (Matt, 2026-06-21, viewing the carved R1 run)

R1 fixed the floor darkness but the carve still reads as a dark capping SLOT CANYON, not an enchanted forest. Frame `04_downgorge`: the left ~half is a massive dark overhang leaning hard in over the play space; the walkable space is a thin cyan sliver. Frame `00_committed`: water visibly BLOCKY (rectangular cyan tiles), dark overhang eats the corner. Matt's directive (a coherent vision, not piecemeal):

**R2-A — Wall height + overhang (Matt: "MORE importantly… WAY too tall… overhang WAY too much").** THE key fix.
- **Cut overhang lean-in to ~10% of current.** KEEP the "great rocky overhang feel" — subtle rocky bulges + a slight top lip — but the lean is ~1/10th. The walls go near-vertical with rocky character, NOT a capping cantilever.
- **Wall top sits JUST ABOVE the in-gorge giant-mushroom tops** (a modest +1–2 m margin), no towering. drax MEASURES the in-gorge hero-mushroom world-top-Y and sets the rim there. This is much shorter than R1's towering cliff stacks. **The height tension from R1 is resolved by Matt here:** walls rise just past the mushroom tops (enclosure) but the reduced overhang + pulled-back camera (R2-D) let the eye see OVER the rim into the forest above.

**R2-B — Lighting / sky (Matt: "the entire scene needs to be a lot brighter… hazy green-blue sky… deep forest zelda feel… right now it feels like a dark cave").** REGISTER EVOLUTION — flagged, supported, guarded:
- **Brighten substantially.** Lift ambient + key off the cave-dark floor. The scene reads as a luminous deep forest, not a cave.
- **Hazy green-blue sky at the top** — BotW Korok-Forest / Lost-Woods register: green-blue volumetric haze, god-ray softness, brighter sky band. Not the thin near-black sliver of R1 — a genuine hazy forest sky.
- **DESIGN-STEWARD FLAG (gandalf):** this intentionally evolves the locked register from *dark-first emissive-led nocturnal* → *brighter hazy green-blue forest with emissive ACCENTS*. It is Matt-directed and sound (an enchanted FOREST, not a cave — the carve drifted cave-ward; this corrects back). **Craft-guard:** the glowing signatures (mushroom caps, trough current, Pool-2 hero focal) shift from PRIMARY light to ACCENTS — they must be tuned to still POP against the brighter hazy base, or they lose meaning. **Rubric consequence:** the GPT-5.4 dark-first rubric (`2026-06-20-enchanted-forest-target-aesthetic-rubric.md`) no longer matches this target; galadriel's CV dark-first/value-band checks become ADVISORY, and the rubric needs a hazy-bright companion re-baseline. Matt's eye is the gate for R2.

**R2-C — Above-ground dense forest (Matt: "details at the top… seem to be lacking… add tons of ferns, leaves, mushrooms, palm trees and other plant life… we really do not want to see much of the forest floor… deep dense forest").**
- The at-grade version's rich rim detail was lost in the carve. RESTORE + AMPLIFY: pack the above-ground rim with ferns, leaf litter, mushrooms, **palm trees**, and varied plant life.
- **Hide the forest floor above** — dense overgrowth so the eye reads lush canopy + undergrowth, not bare ground. This dense forest is the PAYOFF the shorter walls + pulled-back camera reveal over the rim.

**R2-D — Camera (Matt: "moved out a bit further… maybe half way between the cathedral camera and the ravine camera").**
- Pull the ARPG/walkthrough camera out to a MID distance between the current ravine cam and the cathedral cam (drax has both). Not full cathedral zoom. The pull-back affords the over-the-rim view of the dense forest above — the whole point of R2.

**R2-E — Detail / quality fixes (Matt: "needs a lot more detail… no leaves on the tops of the rocks… water is still blocky… still a lot of cards, especially on roots below the trees and the trees themselves").**
- **Rock-top leaves** in the gorge — the spec called for moss+leaf caps on rock tops; they're not landing. Make them actually appear.
- **Water blockiness — fix definitively (3rd time raised).** The per-trough tile approach is producing rectangular cyan tiles. Replace with coherent calm water sheets (one still level per pool, organic edge), not tiled quads.
- **Foliage cards on trees + roots** — the transparency/billboard cards persist on tree foliage and the root meshes below trees. Do the foliage-alpha fix that was deferred as "risky" at the at-grade gate (Matt is now explicitly calling it out): ALPHA_SCISSOR (alpha cutout, writes depth) or proper-mesh replacement so they stop reading as hard rectangles.

**R2 supersedes R1's depth call and the held frame-01 occlusion** (subsumed by the overhang reduction). Re-render, then back to Matt (his eye is the R2 gate; galadriel CV advisory pending rubric re-baseline).

## Sign-off
gandalf, 2026-06-21. Carve = transform on the approved at-grade surface into a NEW scene. Tapered smooth overhangs (wider at bottom), fern-topped outcrops, vine-wrapped log bridge, leaf-pile rim. Within: intermittent magical current, moss+leaf rock caps, corner ferns, downward roots, and small blue/cyan bioluminescent mushrooms at the base and sides. Gated behind Pass 1 + baked-scene save; then back through the tripod to the Matt Gate. **Revision 1 (Matt, same date):** shallower variable depth + slight blue-sky sliver and sun-FILL so more light reaches the floor. **Revision 2 (Matt, same date):** overhang cut to ~10% + walls just above the mushroom tops (not towering); much brighter hazy green-blue Zelda-forest sky (register evolution from dark-cave → luminous forest, emissive→accents, rubric re-baseline flagged); dense above-ground forest (ferns/palms/mushrooms/leaves, floor hidden) revealed by a pulled-back mid-camera; + rock-top leaves, definitive water-coherence fix, and tree/root foliage-card fix.
