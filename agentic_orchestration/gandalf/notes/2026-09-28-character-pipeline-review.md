# Animated-character pipeline review: 100+ unique characters with no AI tells (R-C9-60)

> **STATUS:** CURRENT review for Matt's decision. Author gandalf (ARCHITECT), 2026-09-28.
>
> **Matt, verbatim:** *"take a step back … it doesnt seem like a sensible solution if it needs this much work just for one direction … exhaustively review all 2D and 3D options by searching the web and socials for how people have been having success with the new Opus 5.5 generating animated characters for video games … lift any constraints such as working with Astra or Grok and 2D vs 3D … understand and test all of the viable options for an animated character pipeline which could potentially produce up to 100+ characters which are unique and which don't have any AI tells."*
>
> Follow-ups, verbatim: *"I think it may not make sense to use weapons in the image for meshy.. please verify. Also T and A poses may be needed."* · *"did you look up socials and web details on people having Opus 5.5 (you) build the animations directly? I really wonder what their processes are."*

## 1 · How people are getting Opus 5.5 to make animation (their processes)

Four distinct processes show up in the web and social record. Only the fourth scales to a game roster.

| Process | What the model does | Evidence | Fit for us |
|---|---|---|---|
| **1. Code-drawn animation** | Writes a program that draws every frame (Canvas/SVG/p5.brush/Remotion); characters are jointed SVG rigs with procedural walks; renders a contact sheet, looks at it, fixes, repeats | A 2-minute Steve Jobs film from one prompt: Remotion+React+SVG, ~8.7k lines, *"jointed character rig with a procedural walk cycle"* ([oozn](https://x.com/oozn/status/2103482545111232946)). Anthropic's own kit animates a hand-painted-look cartoon with p5.brush and a contact-sheet review loop ([ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase)); seeded randomness for a hand-made wobble ([iArt](https://www.iart.ai/blog/ai-javascript-animation)) | **No.** A vector/cartoon ceiling; cannot reach the manuscript-watercolor register. Fine for UI/FX. |
| **2. Code pixel sprites** | Writes the sprite as an SVG or pixel array, renders, looks, revises (4 rounds for one rabbit sprite) | [Ciyo test](https://ciyo.ai/blog/can-claude-opus-5-5-generate-images): *"for texture, lighting … image-generation models remain superior"* | **No.** Pixel art only. |
| **3. Rig and key in Blender (MCP)** | Given a mesh, places bones, weights, keys an action in `bpy`, renders, looks, iterates. There is now an **official Anthropic Blender connector** (Apr 2026) | Monster rig plus jump and bite in 40 min ([Stefan 3D AI](https://x.com/Stefan_3D_AI/status/2102641562824135022)); octopus via the Higgsfield plugin ([Higgsfield](https://x.com/higgsfield_ai/status/2102526940859232433)); an honest humanoid test: *"the first iteration was rough … the second … not bad"*, not production-level ([YouTube](https://www.youtube.com/watch?v=qhi9A_j-1Gc)); [connector](https://www.anthropic.com/news/claude-for-creative-work) | **This is what our drax spike was**, and our result matches theirs: it works, but hours to days per character. It does not scale to 100 on its own. |
| **4. The model as ORCHESTRATOR of generators** | Writes the spec and gates; drives image, 3D, rig and motion services; retargets motion; bakes sprites; checks everything | A **36-hour autonomous MMO**: spec plus skills, Unity, Blender and generator APIs; $230 of 2D/3D/music generation ([Stefan 3D AI](https://x.com/Stefan_3D_AI/status/2103778468660162615)). An **open-source concept-to-sprite pipeline built with Claude**: spec → concept art → **Meshy** multi-view 3D → **Meshy** rig → **Mixamo** motion retargeted by bone *role* → Blender bake to **16 directions** → Godot, gated by **67 measured rules** ([marrowfall PR #20](https://github.com/ozturkberkay/marrowfall/pull/20)) | **Yes. This is the scalable pattern.** Marrowfall's recorded pain is instructive: rest-pose and twist errors in retargeting, *"the neck juts forward … baked into the bought clip"*, *"no walk clip"*. Motion-library quality and retarget correctness are where the work goes. |

## 2 · Weapons and T/A-pose: verified, Matt is right

- Meshy's own rigging guide: *"Props belong in separate generations, then get attached to a bone after rigging … a sword generated in-hand deforms with the arm."* *"A T-pose works best for rigging; an A-pose gives more natural shoulder skinning."* ([Meshy tutorial](https://www.meshy.ai/tutorials/character-auto-rigging-workflow))
- Also: *"there is no cloth physics … a long flowing skirt will stretch"*, which applies to our tabard. And inputs work best *"photorealistic or semi-realistic"* ([Meshy help](https://help.meshy.ai/en/articles/16102152-fix-character-pose-face-and-hand-issues-in-meshy)).
- **Our own test confirms it:** from four painted views WITH the pollaxe, `pose_mode: a-pose` produced an A-pose knight, split the pollaxe off as a floating object, and **lost the axe head** (reduced to a knob). Meshy also **invented the tabard's back as red** (misreading the lining).
- **Rule for production:**
  - Astra paints a **weapon-free A-pose character sheet** (front / side / back, arms clear of the torso).
  - Weapons and shields get **their own sheets and meshes**, attached to a hand socket.

## 3 · What was tested (one direction: the E walk; every route on the same benchmark)

Comparison video: `agentic_orchestration/gandalf/captures/2026-09-28-pipeline-review/routes_walk_E_comparison.mp4`

| Route | Result | Time/cost for this one cycle | Scales to 100+? |
|---|---|---|---|
| **A · Video (Grok i2v)** | Looks painted; slides; stride and speed drift; each direction × action a separate generation; no gear | ~$/clip, minutes | Poorly: consistency across 100 characters × 8 directions × N actions is the known failure of video models |
| **B · Cut-out puppet from one still** | Joint gaps, flat feet, no hip/torso turn (Matt's five defects); the method's ceiling | Days per direction | No |
| **C · Hand-built 3D body** (drax) | Motion right after two rounds (pinned feet, Grok-fitted); raw paint failed; **Astra paint-over held the poses at 0.89–0.92 IoU**; **EbSynth pos-guided propagation works** (error 36.5 vs raw 56.8, 7.5 s/frame, no drift) | ~2 days of agent work for one direction | Only if the body-building step is automated → route D |
| **D · AI 3D (Meshy) + auto-rig + library motion** | **4 min / 30 credits** for the model from 4 painted views; **1 min / 5 credits** to rig, **with free walk and run**; a natural upright mocap walk, no gaps (one continuous skinned mesh); raw render reads flat and plastic | ≈ $0.50 of Meshy credit + ~15 min | **Yes**, mechanically |
| **D+ · Meshy + Astra one-sheet paint-over** | Reads as the painted knight; **poses held at 0.93–0.94 IoU**; the red invented tabard back and one stray fragment are input/cleanup defects, not method defects | + 1 Astra run (~7 min) | Yes, with a paint budget (§ 5) |

## 4 · The options, with constraints lifted

1. **Video models** (Grok, Kling 3.0 Motion Control, Seedance; wrappers such as Ludo.ai and AutoSprite): the fastest first result. They cannot guarantee identity, stride or foot contact across a roster, and every direction × action is a fresh roll. **AI-tell risk: highest** (morphing, sliding, detail drift). Keep as reference and concept motion, not the backbone. *Not tested: Kling motion control and Ludo (need accounts).*
2. **Cut-out 2D rigs** (ours; also Spine-style): the method's ceiling is out-of-plane motion; every direction needs its own full part set. **No.**
3. **Hand-built 3D (Opus in Blender)**: proven workable, too slow per character. **No, as the backbone.**
4. **AI 3D + auto-rig + motion library → render → paint pass (D+)**:
   - One body gives **all 8 (or 16) directions, every action and modular gear** by construction.
   - Motion comes from **real mocap**, which removes motion AI tells.
   - The painted look is re-applied by Astra.
   - **Recommended backbone.**
5. **Real-time 3D in Godot with painted textures and a painterly/ink shader** (the Darkest Dungeon 2 and Hades II route; [PC Gamer](https://www.pcgamer.com/interview-darkest-dungeon-2s-new-3d-look-monsters-the-narrator-and-its-surprising-aspirational-spirit/), [Game Developer](https://www.gamedeveloper.com/art/learn-how-supergiant-brought-i-hades-i-hand-painted-characters-to-life)): no per-frame work at all, runtime gear swaps, the cheapest at scale. **Risk: reads as 3D** unless textures and ink are hand-quality. Worth one test on the same Meshy knight.
6. **Code-drawn characters (Opus)**: **no** for this register.

## 5 · The paint budget, the scale question

Per character, 8 actions × 8 directions:
- **D+1, Astra paints every cycle on one sheet:** 64 sheet runs ≈ 7–8 h of Astra per character. Too heavy for 100 unless reserved for hero actions.
- **D+2, Astra paints KEYS only and EbSynth (pos-guided) propagates the rest:** 2 keys × 64 clips = 128 keys ≈ 11 sheet runs (~1.3 h) plus ~1.6 h local CPU. **About 100 characters ≈ 130 h Astra + 160 h CPU**, parallelisable. Mirroring (W from E, where heraldry allows) cuts about ⅜.
- **E, runtime 3D:** 1–3 Astra runs per character (sheet plus texture pass); zero per frame.

## 6 · Recommended next tests (each ends in a Matt look)

- **T1: redo the knight the right way.**
  1. Astra paints a weapon-free A-pose sheet and a separate pollaxe sheet.
  2. Meshy builds the model and the rig; walk, run, idle and one attack come from the library; the pollaxe is attached on a hand socket.
  3. Render all 8 directions.
  4. Paint E and SE with D+1, and the rest with D+2.
  5. Walk it in the A/B scene next to Grok.
- **T2: generality.** The demon or a four-legged monster, through the same route, since the roster is not all humanoid (Meshy's quadruped/"smart" rig, or Tripo).
- **T3: the runtime-3D look test in Godot**, on the same knight: painted texture plus ink shader, vs D+.
- **T4 (needs Matt's accounts): close the video branch fairly.** One Kling 3.0 motion-control clip and one Ludo.ai sheet on the same knight.
- **Custom actions** (polearm attacks are not in Meshy's library: sword, spear walk, parry, casts, hits and blocks only). Text-to-motion (Meshy / Uthana / Hunyuan Motion), or Opus keying in Blender on the auto-rig, the process-3 strength on a body it did not have to build.

*Sources: the links in-line above. Also Meshy API docs ([rigging/animation](https://docs.meshy.ai/en/api/rigging-and-animation), [pricing](https://docs.meshy.ai/en/api/pricing)), the [auto-rigging showdown](https://www.strayspark.studio/blog/ai-auto-rigging-showdown-2026-tripo-meshy-cascadeur-mixamo), [Ludo](https://ludo.ai/features/sprite-generator), [Kling motion control](https://kling.ai/feature/ai-motion-control), [Sprite Sheet Diffusion](https://arxiv.org/html/2412.03685v2), [EbSynth](https://github.com/jamriska/ebsynth), [Steam's 2026 AI disclosure rules](https://www.strayspark.studio/blog/steam-ai-disclosure-rules-2026-indie-developer-guide). — gandalf, 2026-09-28.*
