# Character pipeline for 100+ characters: the recommendation (Run C-9 Phase 2, deliverable D5)

> **STATUS:** DRAFT. Matt's G2 and G3 looks are in (R-C9-71, R-C9-72): *"The barbarian is the best artwork that we've ever produced"*, then *"The barbarian is very coherent now."* This is finalised after his looks at the armed motion (`d3_armed_v2`) and the Barrow (T10). Author gandalf (ARCHITECT), 2026-09-29.
> **Question (Matt, R-C9-60):** *"an animated character pipeline which could potentially produce up to 100+ characters which are unique and which don't have any AI tells"*, and (R-C9-69) *"a character we can make with less clothes/gear on and then test the modular armor/gear additions."*
> **Evidence:** C-9 ledger milestones M-C9-T4 … M-C9-ARMED-SCENE and notes through N-C9-MANIFEST-LINT (every number below is from a measured run, not an estimate, unless marked *est.*).

## 1 · The route

**Painted texture on a real 3D body, seen at the real 53° camera, in a world built the way he was: 3D first, then painted (T10).** Nothing is redrawn per frame, so nothing drifts.

| Step | Tool | Barbarian actuals |
|---|---|---|
| 1. **Model sheet made for 3D** (R-C9-67): four views, A-pose, weapon-free, one scale; an asymmetry marker (e.g. a one-arm tattoo) | Astra, GENERATE | 4 image calls, ~12 min |
| 2. Cut-out of the four views | fal BiRefNet | ~$0.003 |
| 3. **3D build** | **Tripo H3.1 multiview** (T6 winner: IoU 0.88 knight, 0.84 barbarian vs Meshy 0.75 / 0.71; one watertight island; read the back view correctly) | $0.40, ~3 min |
| 4. **Rig and clips** | Meshy rigging via `model_url` (any GLB) + library clips; **text-to-motion, retargeted to his rig, for anything the library lacks**; every clip through the export lint | Rig 21 credits, ~5 min. Armed set (11 library clips, 3 generated): 63 credits |
| 5. **Painted texture**: sheet A = coverage ring at 19.77° plus face close-ups; sheet B = **repaint over A's projection** at 52.95° | Astra EDIT ×2, projection bake with density weighting | 4 image calls, ~25 min; unseen 0.44% after fill |
| 6. **Into the scene**: one line of `character.json`; speeds read from the model's own manifest at load; one blend on ground speed, so nothing snaps | Godot | zero code |

**Modular gear (D2):** one Astra EDIT of the base sheet per layer (the pose and scale match by construction), a Tripo build of the dressed body, the piece isolated and skinned to the SAME rig. Rigid pieces go on bones; weapons go on sockets with a strike-frame assert. A `helmet_on` morph compresses the hair. Weapons are held by closed-hand morphs (the rig has no finger bones); the shield by a centre grip, raised by a guard layer.
- **The swap test passes:** five stacks on one painted body, zero repaint.
- **Measured:** garment poke-through ~1%; D2 cost $2.00 Tripo for five builds plus four Astra sheets.

## 2 · Cost and time per character

| | Base body | Per gear piece | 100 characters with ~6 pieces each |
|---|---|---|---|
| Astra images | ~8–10 | ~3 | *est.* ~2,800: the ChatGPT weekly allowance is the binding limit (≈ 2–3 weeks) |
| Tripo | $0.40 | $0.40 | *est.* ~$280 (gear shared across bodies cuts this sharply) |
| Meshy | 21 credits (rig) + 63 (armed motion set) | 0 | *est.* ~2,100 credits for rigs. Motion is ~6,300 more if bought per character, or close to zero if one set carries to the next body by the retargeter (**untested: the next measurement**) |
| Agent time | ~4 h (first time; tooling written and five defects found) | ~45 min | **Measured on the second character (the sorceress, D7): 71 min end to end, including a base body, texture, 7 clips and 6 gear pieces; 20 min of that was vendor waiting.** At that rate, 100 characters are ~120 h of wall-clock, and it parallelises |

**Measured, second character (D7, the fire sorceress, 2026-09-29):** fal **$2.41** (Tripo base plus gear, and cut-outs), Meshy **38 credits**, Astra **18 images**, **71 min**. That's for one character with a base body, a painted texture, 7 clips (locomotion, hit, death and two casts) and 6 gear pieces. At 100 characters: about $241 fal, 3,800 Meshy credits and 1,800 images. The images are the binding limit: they come from the ChatGPT plan's weekly allowance.

**Her pass 2 (finish, 2026-09-30):** Meshy **9 credits**, fal **$0**, **0 images**, **~1.7 h** wall-clock. Most of that time was one-time work: fixing the measuring rig and the shared tooling (§ 5). The part that recurs per character is fitting the held prop (her staff). Its cost is not yet measured separately; the sword build (task 1 of the next dispatch) is timed to measure it.

**Measured, one weapon (the barbarian's JOIN sword, 2026-09-30):** **27 min** wall-clock (4.5 min of it vendor waiting), **1 image** (an edit to fix the blade-to-grip ratio before 3D), **$0.40** fal for one Tripo build. That's under the per-piece estimate of ~45 min and ~3 images. It covers the image fix, the build, cleanup, skinning, the mount on the weapon bone with its guard check, and a film. **A lesson:** check a weapon's proportions on the design sheet, not in 3D. At any single scale, a blade-to-grip ratio of 2.6 to 1 gives either a dagger or a two-handed grip.

## 3 · What was rejected, and why (measured)

- **Per-frame painted sprites.** They look beautiful where the subject is hair or fur: the manticore's head drift is 4.56 against 6.2–6.7 for the propagation methods. But they drift on hard surfaces (the knight's helm morph, 1.49× its own floor). Each character costs 24–32 Astra sheets, and there's **no modular gear**. *Keep for hero creatures and bosses.*
- **Video models.** Kling keeps the gait and loses the character (identity drift 21.6). Ludo keeps the character and loses the gait (cadence −17% to −35%, no clean loop). Neither is a backbone. *Keep Ludo for look-dev.*
- **AI 3D worlds for levels (World Labs).** The palette is right (ΔE 10), but it builds a pano bubble 33–132× too coarse at our camera. *Keep its 360° panoramas as backdrop material.*
- **The 2D masters as 3D sources.** They're illustrations with readability cheats, not views of one object (R-C9-67).
- **A painted world around a 3D character.** Unlit, he doesn't belong in it (R-C9-71). Lit, it *"mostly looks worse"* (R-C9-72): its light is painted in, and the geometry under it can't carry the form once that light comes out. *The painted world stays right for painted characters (Matt: "The manticore fits the painted world perfectly"). A 3D character gets a world built 3D-first: the Barrow, T10.*

## 4 · Known limits and next steps

1. **Resolved (G2): the 3D look.** Matt: *"he does have lighting and seems much more real."* The watercolour light ramp and the ink line now sit in one render stack shared by the world and the character (T10).
2. **Double-marking is halved, not gone.** Repainting B over A's projection cut the overlap disagreement 55–67%. The residual comes from placement, not wording.
3. **Resolved: custom motion.** Text-to-motion plus the retargeter (`41_retarget_smplh.py`) generated his straight armed run and both strafes, 10 credits a clip. Polearms and casts go the same way.
4. **Prove repeatability:** a second, different character run end to end on the hardened tooling, timed. That's the number the 100-character plan rests on. It also answers whether one motion set carries to a second body (§ 2).
5. **Worlds:** a 3D character needs a world built 3D-first (§ 3). The Barrow (T10) is the test of a fully generated one. If it passes Matt's look, any approved concept painting becomes a playable level by the same steps.
6. **Open, Matt's look:** weapon handling (`d3_armed_v2`): a centre grip, a raised guard, a held block, a locked wrist.

## 5 · What the first character taught the pipeline

Each defect below was found on the barbarian and is now caught or fixed automatically, so the second character shouldn't meet it.

| Found on the barbarian | Cause | Now caught or fixed by |
|---|---|---|
| **The idle was about 18% larger** than the walk and run (Matt spotted it) | Meshy's Idle action ships a Hips scale of 1.176 (20/17) | The export lint: FAIL on any joint scale ≠ 1 |
| **Nothing looked held** | The 24-bone rig has no finger bones; the hands ship open and flat | `grip_R` / `grip_L` morphs close the hands, driven by what he carries |
| **The shield was never in his hand** | The fist was 0.46 m from the boss; a 0.0013 m "gap" had been measured to the rim | A centre grip; measure to a named feature, never to the nearest surface |
| **The axe waffled** (Matt) | Unarmed walk and run clips: a free wrist swings a rigid axe (5–7 reversals a cycle) | Armed library clips, plus a per-clip wrist lock tuned to the idle Matt liked |
| **No straight armed run or strafe in the library** | The left/right diagonal blend leans (mean yaw −32°) | Text-to-motion, retargeted to his rig |
| **The armed idle drifted 0.90 m; feet ended up below the ground** | Root motion in the source; grounding lost in export | De-root at source, keeping the hip sway; re-ground after every retarget; a lint warning on root travel |
| **The run was 19% off; hand-copied speeds went stale twice** | fps hard-coded to 30 in a 24 fps scene; duration counted over keys, not intervals | Every number re-read from the shipped GLB; speeds read from the manifest at load; a manifest-vs-GLB check on every write |
| **The idle snapped in with no transition** (Matt) | Separate states with nothing between them | One blend on ground speed; stops take 0.29 s from a walk and 0.42 s from a run |
| *Found on the sorceress (D7)* | | |
| **Every "clean" speckle count had been measured at the wrong scale** | A 1080-line display clamps a 1080-row window to 971 rows, so every still ran at 90.5 px/m, not 100.6 | Stills render into an offscreen viewport at the exact size, and the output's scale is checked |
| **Her robe's seams showed pale dots** | The decimator split the UV seams | Seams welded before decimation (robe boundary loops 215 → 83) |
| **The staff went through her body in the Meteor** (638 verts) | A one-hand cast clip with a two-hand prop | The barbarian's mount method plus a carry layer, and baked staff tracks for the Meteor (grazing only, ≤ 1.1 cm). The two-handed Meteor needs a source clip where the hands meet |
| **Shared tooling double-applied gamma; two scripts spent outside the fal ledger** | `07_isolate2`; `03_slice_views` and `04_tripo` | Fixed. The barbarian's four gear pieces were re-derived byte-identical, and paid calls now refuse to run without a ledger |
| **Her run popped once per loop, and her walk hitched** (about 5 cm of foot slide per cycle) | Clips were cut on a 24 fps grid, but Meshy keys at 30 fps, so each cut began on a held frame and ended short of the source's own closing frame | Loops are re-cut on the source's own keys, with no resampling (joint closure 4.95 cm → 0). A per-clip window check is written into the manifest. Foot-lock speeds are measured on the clip's own key times |
| **The barbarian's Blender-merged armed clips were off their sources by 0.2–0.9 of his hips-to-head length** | The merge carried each bone's motion in the wrong rest frame; the two skeletons' rest orientations differ by up to ~110° | A world-space graft (`55_clip_graft.py`). A source-fidelity lint on every shipped clip is part of the T12_8 dispatch; *not yet confirmed*, pending its report |
| **A hit reaction read as an attack** (the staff swung out to arm's length) | No prop layer on reactions | A staff layer on hit that keeps the prop inside its carry range while the body flinches |

*— gandalf (ARCHITECT), 2026-09-29. DRAFT; final after Matt's looks at the armed motion and the Barrow.*
