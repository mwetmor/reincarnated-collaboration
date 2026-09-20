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
