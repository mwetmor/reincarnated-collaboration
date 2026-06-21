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

## Sign-off
gandalf, 2026-06-21. Carve = transform on the approved at-grade surface into a NEW scene. Tapered smooth overhangs (wider at bottom), fern-topped outcrops, vine-wrapped log bridge, leaf-pile rim. Within: intermittent magical current, moss+leaf rock caps, corner ferns, downward roots, and small blue/cyan bioluminescent mushrooms at the base and sides. Gated behind Pass 1 + baked-scene save; then back through the tripod to the Matt Gate.
