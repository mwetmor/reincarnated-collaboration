# A world that fits the barbarian: options and recommendation (T10)

> **STATUS:** CURRENT recommendation for Matt's choice. Author gandalf (ARCHITECT + SCENEWRIGHT), 2026-09-29, Run C-9 Phase 2.
> **Matt, verbatim:** *"Per your question on the lit painted world, it mostly looks worse being lit. Please ultra think through our options of making a new world/scene that would fit our barbarian. It does not need to look at all like the prior painted scene or have anything to do with it. Be creative and find the best world to fit him via any of our available potential paths (or recommend a new path/API if needed)."*

## 1 · Why he looks right: the six rules a world must share with him

He reads as *"the best artwork we've ever produced"* because every part of him obeys one set of rules. A world fits him if it obeys the same six:

1. **3D-first form:** real sculpted geometry (Tripo), not a picture of one.
2. **Albedo-only paint in one hand:** the watercolour-and-ink surface carries colour, material and pen hatching, never light direction or cast shadow (T5/T8 method).
3. **One real light:** the renderer lights him. Painted light would be lit twice.
4. **One ink line:** the dark contour is drawn by the renderer, around his current silhouette.
5. **One scale:** true metres. No 2D sprite cheats (the painted props were 1.51× their geometry).
6. **One camera:** the fixed 52.95° orthographic tactical view (R-C9-68).

**Why the lit painted cliffside failed:** it breaks rules 1, 2 and 5 by construction.
- It was **2D-first**: a painting with its light baked in, projected onto a greybox.
- Taking the light out (T9-1b) also took out the painter's form cues, because the geometry underneath could not carry them.

A world that fits him must be built **3D-first and then painted**, exactly as he was.

## 2 · The paths, assessed

| Path | What it is | Fit to the six rules | Speed | Verdict |
|---|---|---|---|---|
| **A. Our asset pipeline** | Astra four-view sheet → Tripo → painted albedo texture (T8/T9 tooling, proven on five props) | Perfect: the same hand and process as him | ~$0.40 + ~3 Astra images + ~30 min per unique asset | **For hero pieces** |
| **B. Synty POLYGON Viking Realm** (licensed; 1,025 meshes on disk in `reincarnated-godot/Assets/Synty/polygon-viking-realm`) | A modular Norse kit: halls, docks, boats, props, rocks, nature | Rules 1, 3–6 yes. Rule 2 needs a **repaint in our hand** (same projection method), because its flat gradient atlas is another style | Layout in hours | **For layout and bulk, repainted** |
| **C. Hybrid (A + B)** | Synty modular bulk and layout, plus Tripo hero pieces, plus Astra-painted tiling terrain textures, all under ONE render stack | All six | ~1–2 days for a slice | **RECOMMENDED** |
| D. AI world generators (World Labs Marble, HY-World) | Pano-bubble splat worlds | Fails rules 1, 3 and 5 at our camera (T7-B: 33–132× too coarse; light baked in) | Minutes | Skies and far backdrops only |
| E. Procedural terrain (Blender geometry nodes / Godot Terrain3D) | Heightfield ground, cliffs and erosion | Rules 1, 3–6. Rule 2 via painted tiling materials | Hours | **Inside C, for the ground** |

**The one thing all paths need: a unified render stack.** Everything in the scene gets:
- painted albedo;
- a soft light ramp (watercolour falloff, not photographic);
- screen-space ink edges on depth and normals (the hull outline stays on characters);
- a light paper grain and colour grade.

That stack is what turns kit pieces, AI pieces and terrain into one picture, and it's the part to prove first.

**New tools and APIs worth adding:**
- **Blockade Labs Skybox AI** (API): painted 360° skies in our register, for any outdoor level.
- **Mixamo** (free): a sword-and-shield animation set, if the Synty packs lack shield-specific motion.
- **Cascadeur** (desktop, AI-assisted keying): custom attacks and blocks.

## 3 · Three worlds (concept paintings T10C-*, attached to the report)

| World | Why it fits him | Build risk |
|---|---|---|
| **The Frost King's Barrow**: a snowbound hill, standing-stone ring, barrow with a carved lintel, frozen tarn, dead birches, low winter sun | His warm palette (red-gold, woad, fur) is at its strongest on snow. Snow is the most forgiving albedo, so the ink line and cast shadows read at their crispest. Maximum combat readability at 53° | **Lowest:** stones, rock, snow, bare trees. Little foliage, no water |
| **The Fjord Landing at Dusk**: shingle shore, jetty, beached longship, rune stones, signal fire, pines, sea stacks, mist | His home. Richest mood: long dusk shadows, water motion | Medium: a water shader, the shoreline, pines (foliage is Tripo's weak spot) |
| **The Burning Mead-Hall**: a courtyard at night, the hall ablaze, braziers, a shield wall | Maximum showcase of real-time light on him ("he has lighting and seems much more real") | Medium-high: fire VFX, many light sources, sparks |

*Recommendation, subject to Matt's eye on the concept paintings:* **the Frost King's Barrow** as the first world. It flatters him most, is the most readable for play, and is the cheapest to make well. The fjord is the natural second realm.

## 4 · The plan (each step ends in a Matt look)

1. **T10-0, now:** Matt picks the world from the concept paintings.
2. **T10-1, the look test (~½ day), one screen:**
   - the render stack first;
   - one terrain material set (Astra seamless tiles);
   - 4–6 kit pieces repainted, plus 1–2 Tripo hero pieces;
   - the barbarian walking in it.
   Judged at the play camera.
3. **T10-2, the slice (~1–2 days):** a playable area of 3–4 screens with a clear combat space, a sky, and fog and particles (snow, embers).
4. **Budget:** Tripo under $10; Astra under 80 images (tiles, sheets, repaints); no new subscriptions needed. Blockade Labs is optional.

## 5 · Motion (W1, in progress in parallel)

Matt: *"there is no shield grip… the shield is not moving as a shield would need to as a defensive item… the axe… waffles back and forth awkwardly."* The walk and run clips are **unarmed** mocap: a free wrist swings a rigid axe. The fix uses licensed motion on disk (Synty Sword Combat: idles, combos, blocks and parries, dodges, hit reacts, deaths), retargeted to his rig:
- a Viking **centre grip** (fist behind the boss);
- a **guard** layer and a **block**;
- an **armed carry** layer that holds the axe's orientation while the arm still swings.

*— gandalf, 2026-09-29. Anchors: R-C9-67/68/69/70/71; M-C9-T7A-2, M-C9-T7B, M-C9-T9-0, M-C9-T9-SLICE.*
