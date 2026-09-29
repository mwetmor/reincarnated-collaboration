# Character pipeline for 100+ characters: the recommendation (Run C-9 Phase 2, deliverable D5)

> **STATUS:** DRAFT. It is finalised after Matt's looks at G2 (the barbarian walking in the 3D cliffside) and G3 (his gear). Author gandalf (ARCHITECT), 2026-09-29.
> **Question (Matt, R-C9-60):** *"an animated character pipeline which could potentially produce up to 100+ characters which are unique and which don't have any AI tells"*, and (R-C9-69) *"a character we can make with less clothes/gear on and then test the modular armor/gear additions."*
> **Evidence:** C-9 ledger milestones M-C9-T4 … M-C9-D2 (every number below is from a measured run, not an estimate, unless marked *est.*).

## 1 · The route

**Painted texture on a real 3D body, seen at the real 53° camera, in a scene painted over its own 3D blockout.** Nothing is redrawn per frame, so nothing drifts.

| Step | Tool | Barbarian actuals |
|---|---|---|
| 1. **Model sheet made for 3D** (R-C9-67): four views, A-pose, weapon-free, one scale; an asymmetry marker (e.g. a one-arm tattoo) | Astra, GENERATE | 4 image calls, ~12 min |
| 2. Cut-out of the four views | fal BiRefNet | ~$0.003 |
| 3. **3D build** | **Tripo H3.1 multiview** (T6 winner: IoU 0.88 knight, 0.84 barbarian vs Meshy 0.75 / 0.71; one watertight island; read the back view correctly) | $0.40, ~3 min |
| 4. **Rig and clips** (walk, run, idle, one attack) | Meshy rigging via `model_url` (any GLB) + library clips | 21 credits, ~5 min |
| 5. **Painted texture**: sheet A = coverage ring at 19.77° plus face close-ups; sheet B = **repaint over A's projection** at 52.95° | Astra EDIT ×2, projection bake with density weighting | 4 image calls, ~25 min; unseen 0.44% after fill |
| 6. **Into the scene**: one line of `character.json`, speeds taken from the clip's own stride | Godot | zero code |

**Modular gear (D2):** one Astra EDIT of the base sheet per layer (the pose and scale match by construction), a Tripo build of the dressed body, the piece isolated and skinned to the SAME rig. Rigid pieces go on bones; weapons go on sockets with a strike-frame assert. A `helmet_on` morph compresses the hair.
- **The swap test passes:** five stacks on one painted body, zero repaint.
- **Measured:** garment poke-through ~1%; D2 cost $2.00 Tripo for five builds plus four Astra sheets.

## 2 · Cost and time per character

| | Base body | Per gear piece | 100 characters with ~6 pieces each |
|---|---|---|---|
| Astra images | ~8–10 | ~3 | *est.* ~2,800: the ChatGPT weekly allowance is the binding limit (≈ 2–3 weeks) |
| Tripo | $0.40 | $0.40 | *est.* ~$280 (gear shared across bodies cuts this sharply) |
| Meshy | ~21 credits | 0 | *est.* ~2,100 credits |
| Agent time | ~4 h (first time; tooling written and five defects found) | ~45 min | *est.* ~45–60 min per base once hardened: **the number to drive down next** |

## 3 · What was rejected, and why (measured)

- **Per-frame painted sprites.** They look beautiful where the subject is hair or fur: the manticore's head drift is 4.56 against 6.2–6.7 for the propagation methods. But they drift on hard surfaces (the knight's helm morph, 1.49× its own floor). Each character costs 24–32 Astra sheets, and there's **no modular gear**. *Keep for hero creatures and bosses.*
- **Video models.** Kling keeps the gait and loses the character (identity drift 21.6). Ludo keeps the character and loses the gait (cadence −17% to −35%, no clean loop). Neither is a backbone. *Keep Ludo for look-dev.*
- **AI 3D worlds for levels (World Labs).** The palette is right (ΔE 10), but it builds a pano bubble 33–132× too coarse at our camera. *Keep its 360° panoramas as backdrop material.*
- **The 2D masters as 3D sources.** They're illustrations with readability cheats, not views of one object (R-C9-67).

## 4 · Known limits and next steps

1. **The "reads as 3D" risk is Matt's G2 call.** The levers, if needed:
   - an ink outline pass at render time (the dark line of R-C9-9);
   - a stylised light ramp;
   - painted hero frames for key actions only.
2. **Double-marking is halved, not gone.** Repainting B over A's projection cut the overlap disagreement 55–67%. The residual comes from placement, not wording.
3. **Custom actions** (casts, polearms): the Meshy library is thin. Use text-to-motion, or keyed clips on the shared rig.
4. **Prove repeatability:** a second, different character run end to end on the hardened tooling, timed. That's the number the 100-character plan rests on.
5. **Scenes:** camera-projected paint over a blockout is exact (median |Δ| 1–2 against the 2D). It needs the painting made over the blockout's own guides and locked camera, which is the discipline for the cathedral and every future scene.

*— gandalf (ARCHITECT), 2026-09-29. DRAFT; final after G2 and G3.*
