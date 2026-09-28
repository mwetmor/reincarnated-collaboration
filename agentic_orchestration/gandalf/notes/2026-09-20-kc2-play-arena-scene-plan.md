# The Cathedral Arena — scene plan (SCENEWRIGHT), Run KC2-PLAY

> **STATUS:** PROPOSED — for Matt's rulings (§ 6 forks, one recommendation each). Author gandalf (`SCENEWRIGHT`, ELICITOR at § 6), 2026-09-20. **Trigger (Matt, verbatim):** *"the style is good, but it is not the frame that we need … run the entire plan by me. I want to understand the style/register across the planned arena. Also … different levels beyond the playable surface, just like in the cliffside scene … other parts of the cathedral, the outside hillside, maybe a far off view of the cliff itself, maybe a bit of open valley before the cliff. Should we have it be more sunlit from the direction of the sunset? … what else would fit this scene and really make it POP with beautiful 2D art (and also what would give it an obscenely grotesque Diablo 2/4 feel at the same time. Obscenely beautiful. A scene that you can't take your eyes away from, but at the same time, a place that you would NEVER want to be in real life."*
> **Standing constraints that do not move:** the projection law (52.95° down, north up; 100.6 px/m east, 80.3 px/m south at plate scale); `u = 0.285`; the H1 register (hand-drawn contour, clean planes, restrained texture — the cliffside's hand); Keeper 1.9 m = 115 px on the plate; every range/radius true metres; the boundary follows the art (KP-19) and is read from the passed painting by sha (KP-20). Painted geometry never resolves combat. No source-game names in any prompt.

---

## 1 · Yes — B1a was the style pass, not the frame

B1a answered one question: *can Astra paint this room in the cliffside's hand?* It can. It was one 15 × 13 m chunk of a plate that is **63 × 84 m (6359 × 7066 px)** — the frame you need is the **whole arena with its world around it**, and that is built the way the cliffside was: an **establishing image** you rule on → a **guide** re-authored to what you chose → the plate **chunk-painted at plate scale with outpainted seams** → **parallax layers** beyond the walls → an **overhead/near layer** → a **dressing pass** whose objects become reusable props → mask-from-paint → assembly → PACK → the Godot scene. § 4 is that sequence with counts.

## 2 · The place, and why it is this place

The cliffside is a walk *toward* a burning cathedral on a crag at sunset. The arena is **inside it** — the reveal the cliffside promised. It should feel like arriving: you have seen this building from a mile away for the whole approach, and now you are standing on its floor. The world outside the walls must therefore be **the world you walked through**, seen from the other side: the valley, the mist, and — through the collapsed apse — **the cliff itself, with the bridge you crossed**, small and far. That callback is the single strongest thing the scene can do and it costs one parallax panel.

**Whose cathedral.** The bible's faction is the *Keepers of Hours* — ceremonial, arcane instruments, blue / ivory / brass, monumental stonework, fractured observatories. So this is **their** cathedral: the rose window is an astrolabe, the floor inlay is an hour-ring with the *Needle through Strata* mark at its centre (the provenance glyph from the advanced set), the piers carry brass gnomons, the banners are the Keeper blue. **And it has been desecrated.** That is the whole grotesque: not a ruin, a *violation*. Everything beautiful in it was made by careful people for a purpose, and everything that has been done to it was done by something that hates purpose. The beauty is the Keepers'; the horror is what was done to it; the fire is the argument between them.

**The one line that governs every prompt:** *a place made for keeping time, where time has been butchered.*

## 3 · The layers (what you see beyond the playable surface)

Same stack as the cliffside (z-order and scroll rates are the cliffside's, T3l), read from far to near:

| Layer | Scroll | What it is | Where you see it |
|---|---|---|---|
| **Sky** | 0.12 | The cliffside's own sunset sky — the same sky, later; the sun sitting on the western ridge, violet above | through every breach in the north and west walls; above the broken vault |
| **Far — the valley and the cliff** | 0.25 | Open valley floor in violet mist, the river, and **the cliff with the bridge** — the cliffside scene's silhouette, tiny, lit gold on its west faces | through the collapsed **apse** (north) and the fallen **west** wall |
| **Mid — the hillside** | 0.45 | The crag's own slopes falling away: the road up, terraces, the cloister garden dead in the fire's light, outbuildings burning | south (the forecourt beyond the shattered façade) and east (the transept) |
| **Mist** | 0.70 | The cliffside's mist, drifting through the breaches into the nave at floor level | breaches and floor edges |
| **THE PLATE** | 1.0 | the nave floor, the walls and their faces, the dais, the piers, everything that gates movement | the playable surface |
| **Below** *(in the plate)* | — | **the crypt**, seen through floor breaches: cold blue-white light from beneath, ossuary walls, stairs the monsters come up | 3–4 breaches; two of them are spawn points — *the thing under the floor is where they come from* |
| **Overhead / near** | > 1 | broken vault ribs crossing the frame, a great fallen chandelier-wheel hanging by one chain, chains with what hangs from them, smoke, the shadow of the roof's edge | edge-anchored, y-sorted over the player (T3p rule: the cut end never on screen) |
| **Air** | — | embers rising from the pools, ash drifting from upper-left, god-ray shafts (additive), candle flicker, banner sway | glows/particles (T3q/T3r), never baked into the plate |

**Light — the sunset question, answered YES.** The sun sets in the **west = screen left**, and the cathedral's west wall is the one that has fallen. So **the sunset floods the nave from the upper-left** — which is exactly where the register card's key already lives. Long gold shafts rake **east** across the floor between the piers; the piers throw blue shadows a body-length long; dust and smoke make the shafts visible. Three temperatures carry the whole scene: **gold** (sunset, dignity, the world outside going on), **red-orange** (fire, the violation, close and hot), **violet-blue** (the shadow everything else lives in). Fire stays the *only saturated* warm; sunset is gold-amber and diffuse. That keeps the card's clause honest and makes the scene sing: the most beautiful light in the world falling on the worst thing in it.

## 4 · The build sequence (what each burst makes; counts)

| # | Step | Labour | Images | Output |
|---|---|---|---|---|
| **B1a ✓** | style pass (the chancel chunk) | Astra GENERATE | 1 | passed on register |
| **B1c** | **THE ESTABLISHING IMAGE** — the whole arena and its world in one 1536×1024, plate + layers composed as the camera would see it from above the nave; **this is the frame you rule structure on** | Astra GENERATE | 2 (+2 retry) | your R3 ruling happens HERE: which structures make the boundary |
| **G2** | guide v2 — boundary, islands, breaches, spawn stairs, pools re-authored to your picks from B1c; chunk grid over the plate | drax script | 0 | grey room, id mask, per-chunk guides |
| **B2** | **plate chunk paint** — 1536×1024 chunks, 256-px overlaps, painted in dependency waves by outpaint (the cliffside's `autopaint_v4` method; DP seam cut; mask IoU gate ≥ 0.98 vs guide for the *frozen* classes only — floor plane + pool discs) | Astra GENERATE, 4–5 bursts | **~35 chunks + ~10 retries** | the plate |
| **B3** | crypt breaches (EDIT over the painted plate: cut the floor, paint the below) | Astra EDIT | 4 | below-level |
| **B4** | parallax panels: sky · far (valley + cliff + bridge, gold-lit) · mid (hillside north/south/east) · mist | Astra GENERATE | 6–8 | 4 layers |
| **B5** | overhead/near: vault ribs, chandelier-wheel, chains + what hangs, smoke | Astra GENERATE on green | 4–6 | near layer, edge-anchored |
| **B6** | **dressing pass** (dress-then-isolate, R-C3-62): statues, pews, banners, candelabra, bodies, bone piles, the altar, the standard | Astra EDIT + isolation CHECKs | 8–12 | reusable props with footprints + sort lines |
| **M** | mask-from-paint (walkable / blocked / pools) from the sha of the plate you passed | drax script | 0 | `walkable.json` for the runtime |
| **A/P** | assembly (`props.json`, `parallax.json`, glows, particles) → PACK → headless proof → Desktop + phone | conductor glue + Astra PACK + drax | 0 | the scene |

**Total ≈ 70–85 images**, in ~8 GENERATE bursts of ≤ 12; every burst halts on a named-reason basis; **you see B1c before anything is chunked, and the assembled plate before it is dressed.** The runtime and the scene meet at A/P; the runtime's monster tokens, HUD and VFX ride on top (geometry-true, never painted).

## 5 · What makes it POP — and what makes it grotesque (one list, on purpose)

The instinct to keep: **every horror is placed where something beautiful was.** That is the D2 Act-I cathedral/D4 register at its best — not gore for volume, but *sacrilege with craftsmanship*, painted so cleanly you keep looking.

1. **The apse — the eye of the scene.** Where the great window was, a colossal figure hangs in the arch, backlit by the fire behind — a Keeper hierarch, flayed and displayed as a clock-hand, arms fixed at an hour. Below it the altar, brass, running. The player faces north for most of the fight; this is what they face. *(Fork F-S3.)*
2. **The astrolabe rose window, shattered on the floor** — B1a already found this; keep it, and let its stained glass throw **coloured light onto the blood** around it in the sunset shafts. The most beautiful square metre in the scene is the worst one.
3. **The hour-ring inlay** across the nave floor, brass in blue stone, *walked through by something huge* — a drag-mark of tar and bone across the ring, the Needle mark at the centre cracked.
4. **The congregation.** Pews rearranged into pens. In the north-east chapel, the congregation still seated, facing the altar, long dead, candles still burning between them. Readable at 8 % figure as a *field of seated silhouettes* — no close gore needed; the arrangement is the horror.
5. **Chains from the vault** with the Keepers' brass instruments hung as trophies among the bodies — the overhead layer sways.
6. **The crypt breaches**, cold blue from below against the warm nave — the only cold light source, and it is where they come from. Bone stairs. The wave-spawn "points" become *places*.
7. **The burning pitch pools with bodies in them** — the Crucible's hazard, reinterpreted: the pitch was poured *over* something.
8. **Saints with smashed faces weeping tar**, brass gnomons bent, banners flayed and re-hung inside-out (blue lining out — the Keeper blue defiled, not removed).
9. **Through the apse: the valley in gold, the cliff, the bridge, the world going on.** Beauty as indifference. Hope you can't reach.
10. **Sound of the eye:** ash falling *through* sunset shafts; embers rising; the one intact candle-tree still lit on the dais.

What to refuse: gore as texture (it reads as noise at this figure size and breaks the clean-plane register); anything that makes the floor unreadable (walkable vs not must stay unmistakable — the fight depends on it); saturated warm anywhere but fire; source-game names in prompts.

## 6 · Forks (one recommendation each — rule with a word)

| # | Fork | Recommendation |
|---|---|---|
| **F-S1** | Sunset light | **Yes** — sun in the west (screen left), the fallen west wall lets it in, gold shafts rake east; fire stays the only saturated warm |
| **F-S2** | Grotesque register | **"Sacrilege with craftsmanship"** — desecration placed where beauty was (§ 5), readable at 8 % figure; no gore-as-texture |
| **F-S3** | The landmark you can't look away from | **The hanging hierarch in the apse arch**, fire behind, altar running below — the north end the player faces |
| **F-S4** | Below level | **Yes** — crypt breaches with cold blue light; two of them are spawn points |
| **F-S5** | Beyond the walls | **North: valley + the cliff with the bridge (the cliffside's own silhouette). South: hillside + road. East: transept and burning outbuildings.** |
| **F-S6** | Next burst | **B1c, the establishing image, before any chunking** — the frame you rule structure on |
| **F-S7** | Identity | **A Keepers-of-Hours cathedral, desecrated** — astrolabe window, hour-ring floor, Needle mark, brass instruments hung as trophies |
| **F-S8** | The Banner object (×1.03 aura, 8 m) | **The Keeper's own standard planted on the dais steps** — the one banner still hanging right-side-out; its aura is a runtime light overlay, never painted |

*Tracker-delta: game tracker SESSION-DELTA on Matt's rulings. — gandalf, 2026-09-20.*

---

## ⚑ CORRIGENDUM-FORWARD 2 (2026-09-20, Matt's B1d notes — ledger R-KP-B4) — governs over § 4 and § 5

1. **BARE FIRST (process, the cliffside's own):** the plate is painted **open** — floor, walls and their faces, dais, piers, breaches, crypt openings, collapsed vault, the world beyond — with **no dressing** (no pews, statues, candles, bodies, bone piles, banners, gates, rubble props). Floor damage per the crack law is plate paint; everything else is a **later object** (§ 4 B6, dress-then-isolate) so the space is planned first. B1c (the establishing image) is painted bare; B2's chunks are painted bare.
2. **THE FALLEN WINDOW IS A HERO OBJECT** (Matt: *"the best part"*): the great sun-window torn from the apse, lying flat, ~8 m across, **vibrant real-church stained glass** (ruby, cobalt, emerald, amber, violet, gold; a saint-knight, a sun, chains in the lead), tracery as an **ornate cross — in a circle (rosette) or free-standing** (B1e: two variants, Matt picks) — with the **sunset gleaming across it and flames reflected in the panes**: the most beautiful and most violated thing in the room. Isolated on green as a prop (its shadow is the scene's); its gleam and flame-reflection become a **glow layer** over the prop (T3q additive flicker) so the reflections *dance*. It sits on the nave axis south of the dais.
3. **No exterior-courtyard iron gates or fences inside the nave** (B1d's were wrong); iron only where structural — vault chains, bound doors, portcullis on the crypt stairs.
4. B1d's "pile under the right column" is struck; nothing like it is authored — every object in the dressing pass is named, sized and placed on purpose.

---

## ⚑ CORRIGENDUM-FORWARD 3 (2026-09-27, Matt, Run C-9 ledger R-C9-43) — the arena is INDOORS; governs over § 3 and F-S1/F-S5 where they conflict

**Matt, verbatim:** *"I want the cathedral arena scenes to feel like they're indoors by having two sides of the cathedral extend above the camera. Just like the original grey box idea from Claude on mobile."* and, answering the near-side fork, *"A for the arena's near side. Agreed. Also, [from the arena] we should see more cathedral rooms beyond the arena. The high windows (some second, all 3rd floor) should see the outside world (trees/horizon/sky)."*

Source convention: `matt_notes_handoff_docs/rdr-art-illuminated-archive-brief.md` § 4 (full-bleed crop · back walls exit the frame, tops never painted · near side cut low or dissolved).

1. **The two FAR walls rise out of the top of the frame.** They are the two walls whose inner faces point at the camera. At our scale (130 px person, about 72 px/m), any wall over about 18 m exceeds a 1080 frame, and a true-scale nave (30 to 37 m) never fits. So the walls are painted to the plate's top edge, and the camera clamp keeps their crowns off-screen at every position.
2. **The NEAR side is (a) CUT LOW: broken off at knee height, Diablo 2-style** (Matt: "A"). Nothing full-height stands between the camera and the floor. The option (b) full-height wall that dissolves around the player is reserved for set pieces only.
3. **The ceiling closes the space.** § 3's overhead/near layer (vault ribs, the hanging wheel, chains) runs over the player. Rising walls plus that ceiling layer are what make it read as a room, not a courtyard.
4. **The rooms beyond the arena are seen through ground-level arches.** The arcades open onto the side aisles, the chapels and the transept. These are more cathedral rooms, painted in the plate as UNWALKABLE dead space (the walkable mask decides; seams hide there). They are sized as real rooms so a later map can open them. The east transept (F-S5 "East") becomes one of these interior rooms, seen through the arches.
5. **Windows on the upper floors show the outside world** (trees, horizon, sky):
   - **3rd floor (clerestory): ALL of them.** Their glass is blown out by the fire and the tracery stands open.
   - **2nd floor (triforium gallery): SOME bays** open through a broken outer wall to the outside. The others stay as dark gallery passages. **Those dark galleries are where the "descend from above" spawns come from** (the walled descent areas of the spawn design).
   - **Mechanism:** each see-through opening is a HOLE in the plate's alpha. The existing Parallax2D stack (sky, far, forest, mist) shows through it, so the view beyond moves with correct depth as the camera scrolls, for free.
   - The stack is offset per scene (the per-style offset mechanism built in C-9) so the HORIZON crosses the window band: the 3rd floor sees horizon and sky, and the open 2nd-floor bays see treetops and the horizon.
   - The view is the same burning world as the cliffside (sunset, the burning forest band, the Keepers' tower). Nothing repeats.
6. **Consequence for F-S1 (sunset). ⚑ RATIFIED by Matt 2026-09-27 (R-C9-44): *"Agreed on your recommendation with the top of the west wall being breached for sunlight"*. The breach is in the UPPER west wall (the clerestory and gallery levels); the lower wall stands. Original recommendation:** with the far walls standing, the WEST wall is a far wall. It is **BREACHED, not fallen**. The sunset enters through its open clerestory, its broken gallery bays and the breaches, as gold shafts raking across the nave floor toward the lower right. It keeps the register card's upper-left key, and shafts from high windows read as MORE indoor than an open side would.
7. **Build (the cliffside's own method, unchanged):**
   - a 3D grey box of the nave (the rising far walls with three floors of openings, the cut-low near side, the arcades to the rooms beyond), rendered from the game camera into guide, depth and walkable-mask images;
   - Astra paints the chunks over it, bare first (Corrigendum 2 § 1);
   - window holes are keyed #00ff00 in the guide, so they come out as alpha.
   - The layout itself (room size, spawn pools, which bays open) still waits for Matt's arena sitting (S1/S4/S5).

*— gandalf, RUN-CONDUCTOR, 2026-09-27.*

---

## ⚑ CORRIGENDUM-FORWARD 4 (2026-09-27, Matt's arena sitting — C-9 ledger R-C9-45) — closes S1 / S4 / S5; governs over the establishing images CA-est-A/B

**The establishing images keep LAYOUT authority only.** Their roofless open crown on the crag is superseded by the indoor ruling (Corrigendum 3). Matt took all four recommendations.

1. **CAMERA: diagonal, from the SOUTH-EAST looking NORTH-WEST.** Only walls that face the camera can rise out of frame, and a north-up camera gives just one. With the diagonal camera:
   - **Rising walls:** NORTH (the apse, the hanging knight-saint, the empty cross mount) and WEST (the top breached for the sunset, R-C9-44), which keeps the card's upper-left key.
   - **Cut low at knee height:** SOUTH (the façade, the road entry) and EAST (the blue-fire crypt, which stays a hole in the floor).
   - ⚑ **Consequence:** the east "gallery stair above the crypt" cannot stand on a cut-low wall. The **descend-from-above spawns move to the dark triforium galleries of the NORTH and WEST walls** (Corrigendum 3 § 5). The divergence row for the gallery-stair entrance is re-keyed accordingly (arrival timing unchanged).
2. **S1 LAYOUT: CRUCIFORM, crater at the CROSSING.** Ratifies the parked veto-open ruling (Crack-law doc, Corrigendum 2 § 1). The sequence: road in through the south façade → north up the nave → the demon-gate crater at the crossing → dais and apse. The transept arms are among the "rooms beyond" seen through the arcades. Room size is still solved from encounter math (brief § 3), not from pictures.
3. **S4 POOLS: the APRONS plus a FEW pools.** Every entrance keeps its hazard apron. Of the six measured pools, only those that do NOT coincide with an entrance survive, painted as spilled burning pitch on the nave floor; the floor stays mostly calm and readable. Registering the measured pools against the entrances is the UNTESTED item (Crack-law doc, Corrigendum 4 § 6); that registration now decides the count. Anything dropped is a divergence row, never silent.
4. **S5 THE VIEW OUT (through the windows of Corrigendum 3 § 5):**
   - **WEST windows:** the low sun over the burning forest band, with the Keepers' tower on the horizon.
   - **NORTH windows:** the valley, the river and the cliff with its bridge (where the player came from).
   - It is the same world as the cliffside, and nothing repeats.
   - **Rooms beyond (ground arches):** the west aisle and chapels, the transept arms, and the ambulatory behind the apse.

**Next in the build:** a 3D grey box of the nave from this camera (the cliffside method) → guide, depth and walkable-mask images → an Astra establishing pass over the grey box (bare first) → Matt gate → chunks.

*— gandalf, RUN-CONDUCTOR, 2026-09-27.*

---

## ⚑ CORRIGENDUM-FORWARD 5 (2026-09-28, Matt, C-9 ledger R-C9-53): the indoor feel is carried OVER and AROUND the player; no zoom-out

**Why:** the grey box CA-guides-v1 (drax, `286112bc6`) measured that at the plate scale (a 130 px knight, ppm 100.6) the camera sees about 19 × 13 m of floor and about 10 m of wall above the player. In the 57 × 77 m room most frames are floor only, and the upper storeys never enter the frame. **Matt, verbatim:** *"let's go with ceiling layer + side piers at the current knight size.. don't zoom out."*

1. **No zoom-out.** The arena keeps the cliffside's plate scale; character size is constant across scenes.
2. **The CEILING layer is the primary indoor carrier, everywhere.** The § 3 overhead/near layer (vault ribs, chains, the hanging wheel, drifting smoke) crosses the frame at every position. The floor carries the VAULT's shadow pattern and the sunset SHAFTS falling from the (off-screen) west clerestory, so the unseen upper storeys are present by their light.
3. **SIDE PIERS:** a pier arcade runs down both sides of the nave (and the transept arms where the plan allows), with aisles beyond.
   - The piers rise out of the frame from almost any position.
   - The aisle floor is walkable and counts toward the encounter area.
   - The piers are props with footprints and sort lines (Crack-law doc, Corrigendum 2 § 2) that FADE around the player (the T3m fade, applied to piers). This is the set-piece dissolve of Corrigendum 3 § 2, used for piers only; the near WALLS stay cut low.
   - Divergence row owed: `DIV-nave-piers`, obstacles at the vessel edges that the measured open plane did not have.
4. **Conductor settlements of the grey-box conflicts (veto-open; recorded so they travel):**
   - pools: keep Z-618, Z-622 and Z-623; drop Z-614 and Z-626 (off the floor) and Z-620 (on the chancel apron);
   - the vessel width becomes 21.768 m (derived from the measured area);
   - the four crossing piers and the east arm's north wall (R4) are cut low, so the chancel and the empty cross mount stay visible;
   - the north breach stair moves to the playable side;
   - the tall WEST-wall segment that hides the west transept arm FADES when the player is behind it;
   - the 57 m wall height is a framing device (cropped at 28 m), not a true-scale claim.
5. **Next:** grey box v2 (piers, aisles, vault geometry for the ceiling guide and floor light pattern) → the establishing pass, which is also **bake-off round 3** (Astra vs Sol, R-C9-49) → Matt gate → chunks.

*— gandalf, 2026-09-28.*
