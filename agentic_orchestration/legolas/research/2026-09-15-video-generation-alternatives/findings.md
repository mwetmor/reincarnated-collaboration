# Legolas Mode A — video-generation alternatives to the Grok image_to_video route (filed by gandalf)

> **STATUS:** CURRENT — research findings, Legolas (UNKNOWN-RESEARCHER), commissioned by gandalf (RUN-CONDUCTOR, Run C-3) per Matt 2026-09-15 (video generation is the bottleneck). Commission: `agentic_orchestration/gandalf/requests/2026-09-15-legolas-video-generation-alternatives.md`. Filed verbatim from the sub-agent's text return; prices accessed 2026-09-14. Sub-agent ran serial/web-only under the 8 GB host guardrail.

---

# Research: video generation alternatives to Grok image_to_video (2026-09-14)

**Mode:** A (analytical) · **Commissioner:** gandalf (RUN-CONDUCTOR, C-3) · **Brief:** `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/requests/2026-09-15-legolas-video-generation-alternatives.md`
**Host discipline:** web only, one step at a time, no sub-agents, no downloads, no inference, no decoding. Nothing was written to the repo. Every price was accessed on **2026-09-14**.

**Evidence labels:**
- **V (VERIFIED):** I fetched the vendor page or docs myself.
- **V-snip:** vendor page text seen only in a search-index snippet, not fetched. Treat it as one step below V.
- **PR (PRACTITIONER-REPORT):** third-party blog or aggregator.
- **D (DERIVED):** my arithmetic, shown.
- **BLOCKED:** the page could not be read.

---

## 1. TL;DR

**Bake-off shortlist.** Three models, all with an end-frame input:
- **ByteDance Seedance 1.5 Pro** on fal. About **$0.16 per clip** with no audio (D). It has a real `camera_fixed` switch.
- **Kling v3 Standard** on fal. **$0.50 per clip** with no audio (D).
- **Google Veo 3.1 Lite** on the Gemini API. **$0.30 per clip** (V), native 24 fps, `lastFrame` supported.

**Probe cost.** 6 Keeper stills × 3 models × 2 arms (arm A asks for the first frame only, like Grok; arm B sets the last frame equal to the first for a loop) = 36 clips, **≈ $11.52**. With a 25% retry margin that is **≈ $14.40**. Adding an optional open-weights wildcard (Wan 2.2 A14B, 6 clips, arm A) brings it to **≈ $17.30**. Suggested approval cap: **$20**.

**Grok for comparison.** At the xAI API list price the same 6 s clip costs **$0.30–$0.84**. The range comes from two unknowns: which Grok video model the CLI used, and a price-page conflict (§5).

**First step-down route to try.** Pose-driven transfer:
- Render a walk cycle once from a plain 3D figure in Godot, per direction. This driving video costs $0.
- Apply it to each gear-tier still with **Wan 2.2 Animate Move** ($0.04–0.08 per output second) or **Kling 2.6 Motion Control** ($0.07/s).
- It does not remove the per-gear call. What it does is make timing and silhouette **identical across gear tiers**, so cycle-cutting becomes deterministic. That same determinism is what a later gear-layer compositing route would need.
- First experiment costs under $2.

---

## 2. Comparison table (T1 + T2)

**Our clip shape:** about 6 s, 720p, 24 fps, portrait. Our stills are 2:3 (768×1168). Most models only offer 9:16 or 3:4, so the still gets padded with plate colour.

| Model | Access | Price per clip at our shape | Free tier | First-frame fidelity | End / key frames | Camera lock | 2D/anime evidence | Licence / weights | Evidence + URL |
|---|---|---|---|---|---|---|---|---|---|
| **Grok Imagine Video** (`grok-imagine-video`) | xAI API `POST /v1/videos/generations`; 10 requests/s | Docs: $0.05/s flat → **$0.30** (D). Third-party reports: $0.05/s at 480p, $0.07/s at 720p, plus $0.002 per input image → $0.42 (D) | none found | "source image becomes the starting point" (V) | OpenRouter lists `frame_images`/first_frame; extension "from its last frame" (V) | prompt only | **works in our C-3 run (68/71)** | closed | V docs.x.ai/docs/models/grok-imagine-video · PR eesel.ai/blog/xai-pricing |
| **Grok Imagine Video 1.5** | xAI API; GA 2026-06-16 (PR) | Docs: $0.08/s → **$0.48** (D). Reports: $0.08 / $0.14 / $0.25 per s at 480p / 720p / 1080p → $0.84 (D) | none | x.ai: "continues the original image rather than reinterpreting it" (V, 2026-06-03) | 1–15 s; 480p/720p; 7 aspect ratios incl. 2:3 (V, OpenRouter) | prompt only | vendor claim only | closed | V docs.x.ai/docs/models/grok-imagine-video-1.5 · V x.ai/news/grok-imagine-1-5 · PR techjacksolutions.com |
| **Veo 3.1 Lite** (`veo-3.1-lite-generate-preview`) | Gemini API | $0.05/s at 720p → **$0.30** (V/D). Audio always on | "Not available" (V) | image used as initial frame (V) | **`lastFrame` supported** (with image); no reference images on Lite (V) | prompt only | none found | closed; SynthID watermark; videos deleted after 2 days (V) | V ai.google.dev/gemini-api/docs/pricing · ai.google.dev/gemini-api/docs/veo |
| Veo 3.1 Fast / Standard | Gemini API | $0.10/s → $0.60; $0.40/s → $2.40 (V/D) | no | yes | lastFrame + up to 3 reference images (V) | prompt | none found | closed | same URLs |
| **Sora 2** | OpenAI API | $0.10/s at 720p. Batch $0.05/s. **No 6 s option** (4/8/12/16/20 s); 8 s = $0.80, batch $0.40 (V/D) | no | "acts as the first frame"; must match output size (V) | none documented (V) | prompt | none found | closed; **"Input images with faces of humans are currently rejected"** (V), a risk for a painted humanoid; download URLs last 1 h | V developers.openai.com/api/docs/pricing · …/guides/video-generation |
| **Runway Gen-4 Turbo** (`gen4_turbo`) | Runway API; $0.01 per credit | 5 credits/s → 5 s = **$0.25** (V/D). Durations 5 or 10 s (PR) | no | first frame (PR) | reported: image-to-video accepts position "first" only (PR) | prompt | none found | closed | V docs.dev.runwayml.com/guides/pricing · PR docs.aimlapi.com (gen4_turbo), runware.ai |
| Runway Gen-4.5 | Runway API | 12 credits/s → 5 s $0.60 (V/D) | no | first | first only (PR) | prompt | — | closed | same |
| **Luma Ray 3.2** | Luma API | Image-to-video 5 s at 720p = **$0.30** (540p $0.15, 1080p $1.20); HDR 2× (V) | none stated | frame0 (V, Ray 2 docs) | **Multi-Keyframe "up to 16 keyframes inside a single clip"**, no extra charge listed (V); `loop: true` parameter (V, Ray 2 docs) | prompt | none found | closed | V lumalabs.ai/api/pricing · docs.lumalabs.ai/docs/video-generation (docs show ray-2 / ray-flash-2 only, so versions drift) |
| **Kling v3 Standard** | fal | $0.084/s audio off (V) → **$0.504** (D) | no | `start_image_url` (V) | **`end_image_url`** (V) | prompt | vendors advertise anime; no measurement | closed | V fal.ai/models/fal-ai/kling-video/v3/standard/image-to-video |
| Kling v3 Turbo Standard | fal | $0.112/s → $0.67 (V/D) | no | yes | not shown on page | prompt | — | closed | V fal.ai/…/v3/turbo/standard/image-to-video |
| Kling 2.5 Turbo Pro | fal | 5 s $0.35 + $0.07 per extra second → 6 s **$0.42** (V/D) | no | yes | **tail image (end frame)** (V) | prompt | — | closed | V fal.ai/models/fal-ai/kling-video/v2.5-turbo/pro/image-to-video |
| **MiniMax Hailuo 2.3 Fast** | fal | **$0.19** per 6 s at 768p (V) | no | yes | not stated | prompt | vendors advertise anime | closed | V fal.ai/models/fal-ai/minimax/hailuo-2.3-fast/standard/image-to-video |
| Hailuo 2.3 Standard | fal | $0.28 per 6 s at 768p (V) | no | yes | not stated | prompt | — | closed; MiniMax now labels 2.3 "Legacy", H3 current (PR) | V fal.ai/…/hailuo-2.3/standard/image-to-video |
| **Seedance 1.5 Pro** | fal | $1.2 per million tokens with no audio (V). Tokens ≈ h·w·24·s/1024; 720×1280·24·6/1024 = 129,600 → **$0.156**, with audio $0.311 (D). Cross-check: vendor says a 5 s 16:9 720p clip with audio is "roughly $0.26"; my formula gives $0.259 ✓ | no | yes | **`end_image_url`** ("lands precisely on this frame") (V) | **`camera_fixed: true` — "Lock the camera in place (tripod shot)"** (V) | none found | closed; 4–12 s; 9:16 and 3:4 available, no 2:3 (V) | V fal.ai/models/fal-ai/bytedance/seedance/v1.5/pro/image-to-video |
| Seedance 1.0 Lite | fal | 5 s 720p $0.18; $1.8/M → 6 s 9:16 ≈ $0.233 (V-snip/D) | no | yes | — | camera_fixed on v1 (PR) | — | closed | V-snip fal.ai/models/fal-ai/bytedance/seedance/v1/… |
| Seedance 2.0 / 2.0 Fast | fal | $0.3034/s → $1.82; $0.2419/s → $1.45 (V-snip/D) | no | reported best image-to-video fidelity (PR) | reference-to-video | — | — | closed | V-snip fal.ai/models/bytedance/seedance-2.0/image-to-video · PR opencreator.io |
| **Wan 2.2 A14B** | fal | $0.08 per "video second" at 720p, counting frames/16 (V). 96 frames ≈ **$0.48**, 81 frames $0.405; 480p $0.04 (D) | no | yes | **end image field** (V) | prompt | vendors advertise anime | **open weights, Apache 2.0.** Local run: no (14B, needs a 4090-class GPU per the HF Wan-Animate card) | V fal.ai/models/fal-ai/wan/v2.2-a14b/image-to-video |
| Wan 2.6 (and Flash) | Alibaba Model Studio (intl) | $0.10/s at 720p → $0.60; Flash reported from $0.025/s silent at 720p → $0.15 (PR, "as of 2026-08-28") | **50 free video seconds for 90 days** (PR) | yes | first/last-frame models exist (not verified) | prompt | — | closed (2.5+) | PR therundown.ai/tools/wan-2-6 · Alibaba pricing page had no Wan rows (BLOCKED-ish) |
| **Vidu Q3-turbo** | Vidu API; $0.005 per credit | 11 credits/s at 720p = $0.055/s → **$0.33**; off-peak 6 credits/s → **$0.18** (V/D) | none stated | yes | **start-end2video** (V) | prompt | vendor advertises anime | closed | V platform.vidu.com/docs/pricing |
| Vidu Q3-pro | Vidu API | $0.10/s → $0.60; off-peak $0.30 (V/D) | — | yes | start-end (V) | — | — | closed | same. Q2 credit table read inconsistently; do not use |
| Pika 2.2 | fal | 720p 5 s **$0.20** (V) | no | yes | Pikaframes not on page | prompt | — | closed | V fal.ai/models/fal-ai/pika/v2.2/image-to-video |
| **LTX-2.3 Fast** | fal (the LTX-2.0 endpoint was deprecated 2026-08-15) | $0.04/s but **minimum 1080p** and minimum 6 s → **$0.24** (V-snip/D) | no | yes | **`end_image_url`** (V); fps 24/25/48/50; 9:16 (V) | prompt | none found | **open weights**; fal says "Commercial use permitted" (V, LTX-2 page). Local run: no | V fal.ai/models/fal-ai/ltx-2.3/image-to-video/fast/api · V fal.ai/models/fal-ai/ltx-2/image-to-video/fast |
| HunyuanVideo 1.5 | fal | $0.075/s, 480p only reported → 5 s ≈ $0.375 (V-snip/D) | no | yes | — | — | — | open weights (Tencent licence, not checked). Local run: no | V-snip fal.ai/models/fal-ai/hunyuan-video-v1.5/image-to-video |
| CogVideoX-5B | fal | **$0.20 per video** (V); shape not stated | no | yes | — | — | — | open weights. Local run: no | V fal.ai/models/fal-ai/cogvideox-5b/image-to-video |

**T2 fit to our clip shape: what the evidence actually supports**
- **Camera lock as an API parameter:** verified only on **Seedance** (`camera_fixed`). Every other model controls camera through the prompt.
- **End-frame conditioning (last = first gives a one-stride loop):** verified on Veo 3.1 (all tiers), Kling v3 Standard, Kling 2.5 Turbo Pro, Seedance 1.5 Pro, Wan 2.2 A14B, Vidu Q2/Q3, LTX-2.3, and Luma (frame0/frame1 plus a `loop` flag, and 16 keyframes on Ray 3.2). Not supported on Sora 2 or Runway Gen-4.x image-to-video (PR).
- **Painted 2D staying painted, flat background kept, no camera drift:** I found **no public head-to-head** on sprite or cycle fitness. What exists is vendor marketing ("anime" for Kling, Hailuo, Vidu, Wan) and general quality rankings (e.g. "Seedance 2.0 wins on image-to-video fidelity" — PR, opencreator.io). One practitioner source lists Seedance 2.0, Wan 2.7, Kling 3.0 and Grok Imagine as "on-style across every frame" for sprite work, without measurements (PR, sorceress.games, verified 2026-05-10).
- **Our own 68/71 Grok run is the only real evidence for our register.** The bake-off exists to close this gap.

**Open weights vs this host.** Wan 2.1/2.2, LTX-2.x, HunyuanVideo 1.5, CogVideoX and ToonCrafter all have open weights. **None of them can run on the 8 GB Mac mini.** Wan-Animate 14B's card cites "consumer-grade graphics cards like 4090" (V). ToonCrafter needs "~24G", with the community reporting about 10 GB (V, GitHub). These models only become "free" with rented or owned CUDA GPUs.

**What the C-3 Grok clips would cost at API prices (D).** 71 calls × 6 s:
- grok-imagine-video at the docs rate: **$21.30**
- grok-imagine-video at the reported 720p tier: $29.82
- 1.5 at the docs rate: $34.08
- 1.5 at the reported 720p tier: $59.64

---

## 3. Bake-off design (T3)

**Inputs.** The same 6 Keeper stills from `runs/C-3/artifacts/K2c-gen-*/`, with the same prompt text used in C-3.
- Pad each 768×1168 still to 9:16 (720×1280 frame) with its flat plate colour; use 3:4 if a model prefers it.
- Record the pad box so frame 0 can be cropped back before scoring.
- Arm A is first frame only, the same ask as Grok. Arm B sets the end frame to the same still (loop request) and applies to walk/run/idle cells; for cast cells it runs as a control.

**Calls (parameters as documented; verify each schema just before firing):**
1. **Seedance 1.5 Pro**, fal `fal-ai/bytedance/seedance/v1.5/pro/image-to-video`: `{image_url, prompt, duration:6, resolution:"720p", aspect_ratio:"9:16", camera_fixed:true, generate_audio:false, [end_image_url]}`. ≈ $0.156 × 12 = **$1.87**.
2. **Kling v3 Standard**, fal `fal-ai/kling-video/v3/standard/image-to-video`: `{start_image_url, prompt, duration:6, generate_audio:false, [end_image_url]}`. $0.504 × 12 = **$6.05**.
3. **Veo 3.1 Lite**, Gemini API `veo-3.1-lite-generate-preview`: `{prompt, image, config:{aspectRatio:"9:16", durationSeconds:6, resolution:"720p", [lastFrame]}}`. $0.30 × 12 = **$3.60**.
4. *Optional wildcard:* **Wan 2.2 A14B**, fal `fal-ai/wan/v2.2-a14b/image-to-video`, 720p, 96 frames, arm A only. ≈ $0.48 × 6 = **$2.88**.

| Line | Cost (D) |
|---|---|
| Shortlist, 36 clips | $11.52 |
| + 25% retries | **$14.40** |
| + Wan wildcard | **$17.28** |
| Grok baseline | $0 (reuse the existing C-3 clips for the same 6 cells). An API re-run for like-for-like wall times would add 6 × $0.30–0.42 = $1.80–2.52 |
| **Suggested approval cap** | **$20** |

**Scoring.** Each score runs on every clip, Grok's 6 included, in one pass. Decoding must run one clip at a time under the memory watchdog.

| # | Measure | Instrument | Pass |
|---|---|---|---|
| S1 | Identity at frame 0 | SSIM of frame 0 vs still, cropped back from padding, on the character box | ≥ Grok's median on the same cells minus 0.02 |
| S2 | Cycle found | `oracle/steps_per_loop.py`: yes/no + period (frames) | yes |
| S3 | Loop seam (arm B) | SSIM of cut-cycle last frame → first frame | ≥ Grok arm-A seam SSIM |
| S4 | Camera / plate stability | plate-region mean absolute difference, or phase-correlation shift vs frame 0, max across clip | ≤ Grok median |
| S5 | Matte cleanliness | `gates/matte.py` pass + residual fringe px | pass |
| S6 | Drift | silhouette IoU across cycle frames (box-normalised) + ΔE of palette on character pixels vs frame 0 | ≥ / ≤ Grok median |
| S7 | Wall time per clip | client timer | recorded, not a gate |
| S8 | $ per accepted clip | spend ÷ clips passing S1–S6 | — |

**What "beats Grok" means in numbers:**
- The model's accepted count on the 6 cells is **≥ Grok's**, **and** its $/accepted clip is **≤ 50% of Grok's API-equivalent** ($0.30–0.42 per clip, so a target of ≤ $0.15–0.21). Seedance can clear this on price; Kling and Veo only win on quality.
- **Or** it has the same $/accepted clip and **+2 accepted cells**.
- **Arm-B bonus:** if end-frame loops make S2 pass on cells where Grok failed, count that as a pipeline simplification. A clip that already ends on its first frame needs less cycle hunting.

---

## 4. Step-down routes (T4)

| Route | Hosted / priced | What it removes | Quality risk for H1 painted register | Cheapest first experiment |
|---|---|---|---|---|
| **R1: Pose-driven transfer.** One still + a driving motion video. Options: Wan 2.2 Animate Move; Kling 2.6 Motion Control; Runway Act-Two; Wan-Animate-2 (research) | Wan Animate Move on fal: $0.08 / $0.06 / $0.04 per video-second at 720p / 580p / 480p (V). Kling 2.6 Motion Control: $0.07/s (V). Act-Two: 5 credits/s = $0.05/s (V). Wan-Animate weights Apache 2.0 (V). **Wan-Animate-2 (arXiv 2608.06009, 2026-08-06) adds "text driven viewpoint control that decouples the output camera perspective from the driving video"**, with Base weights promised; not seen hosted (V abstract) | Removes the **prompt lottery** and per-clip motion variance. A motion is authored once per direction, and the driving video can come free from a Godot mannequin render. Every gear tier gets **identical timing and silhouette path**, so cycle period is known in advance. It does **not** remove the per-gear paid call. Wan-Animate-2 viewpoint control could, in principle, collapse the direction axis too (untested) | Training and marketing are human-body based: Kling's page says "portraits and simple animations" (V); the Wan-Animate card never mentions stylised or anime characters (V). Risks are repainting of the tapered contour, staff/gear morphing, and background handling not documented (V). Act-Two is a face/upper-body performance tool, the weakest fit | 1 Keeper S-direction still + one Godot mannequin walk-cycle render (6 s) → Wan Animate Move at 480p (≈ $0.24) and Kling 2.6 Motion Control (≈ $0.42) → repeat with a second gear-tier still → score S1–S6 plus **cross-gear silhouette IoU per frame**. **< $2** (D) |
| **R2: 2D cut-out / part rig.** Spine, Godot Skeleton2D, Live2D-style | **GodMode AI Spine generator:** a single image becomes a split head/torso/limbs rig; exports Spine skeleton.json + atlas for Spine 3.5–4.2; REST API; **1 credit per character upload, "unlimited re-animations"**; $32 / 30 credits ($1.07) or $100 / 125 ($0.80) (V). **Currently: "New character uploads are disabled while we upgrade the service"** (V, 2026-09-14). anysplit and ImageToLayers do layer separation with occlusion fill for Live2D/Spine (PR, no pricing checked). **Meta Animated Drawings:** MIT licence, humanoid "two arms and two legs", BVH motion retargeted to any drawing, twisted-perspective retarget (V) | **Biggest collapse.** Motions become free keyframed or retargeted animation. Gear becomes a **texture/skin swap per part** (native Spine skins, Godot per-bone sprites). Directions still need a rig each: 8, or 5 with mirroring | Sweet spot is "Anime and Arknights-style sprites"; needs full body with "limbs readable" (V). For H1 specifically, the following is my inference, not sourced: the tapered dark contour breaks at every joint seam; hidden-area fill is hallucinated and may not match painted planes; limbs overlap badly in 3/4 views; flowing cloth and the staff do not rig as rigid parts. Reads as "puppet" rather than painted animation | Once uploads reopen: 1 Keeper S still → GodMode rig → walk/idle from templates → compare the silhouette silhouette-by-eye and via S6 against the Grok cycle. **≈ $1.07** (V/D). Zero-cost alternative: Animated Drawings on a front-view still (needs a local run, so blocked on this host; would run elsewhere) |
| **R3: Painted keyframes + interpolation.** Image model paints 4–8 keys per cycle; in-betweens are generated | **RIFE:** free, flow-based; rife-ncnn-vulkan on macOS; SVP reports "Apple M1 can only do 576p @48 fps", single GPU thread (PR svp-team.com). **ToonCrafter:** Replicate ≈ **$0.071/run**, A100, ~51 s (V); Apache-2.0 but "open-source research exploration" (V); **512×320, 16 frames** (V), so it mismatches portrait 768×1168. **Hosted key-pair video:** any end-frame model above chains key k → key k+1 (e.g. Seedance ≈ $0.10 per 4 s segment, D). **Luma Ray 3.2 Multi-Keyframe:** up to 16 keys in one clip, $0.30 per 5 s at 720p (V) | Makes the video model optional. Timing is authored by us, so cycles are exact by construction and no cycle-cut search is needed. With interpolation run locally, per-clip video cost drops to zero | Image-model **pose consistency across keys** is the new bottleneck: identity and gear drift between separately painted keys. RIFE ghosts on large limb displacement between walk contact and passing poses, so it needs 8+ keys per stride (inference from how flow interpolation works). ToonCrafter's resolution cap forces upscaling. Luma 16-keyframe fit for 2D is unmeasured | Take 4 walk keys the image model already produced (or paint 4), interpolate with **Luma Ray 3.2 multi-keyframe** (≈ $0.30) and **ToonCrafter** on Replicate (≈ $0.07 × 4 pairs = $0.28), then run steps_per_loop / S6. **< $1** (D). Local RIFE is a later step and needs a host that permits local inference |
| **R4 (added): 3D proxy.** Still → 3D mesh → auto-rig → render 8 directions | **Meshy API:** image-to-3D 30 credits (textured), **auto-rig 5 credits, animation 3 credits per action** (V). **USD per credit BLOCKED** (plan page JS-rendered). Free plan outputs are CC BY 4.0; premium "you own all assets" (V) | **Collapses the direction axis.** One rig renders all 8 directions × every motion in Godot. Renders can be the driving video for R1 or pose guides for R3 keys | Direct renders lose the painted register entirely; mesh fidelity from one painted still is unmeasured | Use it only as a **motion/pose source** for R1: one Meshy (or plain mannequin) rig → 8-direction walk render → R1. Cost: a few dozen credits, USD unknown |

**Recommendation (inference, grounded in the table above).** Run **R1 first**:
- It keeps the existing still → clip → cycle-cut → matte → SpriteFrames pipeline intact.
- Its driving source can be rendered in Godot for free at all 8 directions.
- It produces the invariant the gear-per-piece idea depends on: **the same motion timing across gear variants.** Without that invariant, per-piece gear layers can never be composited, and the multiplication stays multiplicative whatever the per-clip price.
- **R2** is the largest collapse but carries the highest register risk, and its best-fit API is currently not accepting uploads.
- **R3 via Luma multi-keyframe** is the cheapest parallel probe if Matt wants two lanes, as long as they run one after the other.

---

## 5. Gaps and blocked pages

1. **The Grok CLI's video model is not pinned.** The CLI does not print it, and no public page maps `grok-shell` 1.0.30's `image_to_video` to an API model. The API currently lists `grok-imagine-video` and `grok-imagine-video-1.5` (V). Our 768×1168 output matches the 2:3 aspect both advertise, which does not distinguish them. **Next step:** inspect the CLI's tool schema or response metadata, or email xAI.
2. **Grok price conflict (not averaged):**
   - docs.x.ai pricing and model pages list flat **$0.050/s** and **$0.080/s** (V).
   - The docs video guide itself says "both duration and resolution affect the total cost" (V).
   - Third parties report resolution tiers: $0.05 / $0.07 for the base model; $0.08 / $0.14 / $0.25 for 1.5 (PR).
   - **x.ai/api/imagine returned 403, BLOCKED.** vercel.com AI Gateway page was **BLOCKED** (fetch refused).
3. **BLOCKED or unreadable pages:**
   - ltx.io/model/api/pricing (header overflow) and help.ltx.io (403), so the LTX price comes from the fal snippet only.
   - MiniMax pay-as-you-go page (only package tables rendered).
   - Alibaba Model Studio pricing (no Wan rows rendered).
   - Meshy USD per credit.
   - Runway API reference for gen4_turbo duration and position values (not rendered; PR values used).
   - Vidu Q2 credit rows parsed inconsistently; excluded.
   - Kling's official klingai.com API price not fetched; fal resale prices only.
4. **Version drift:** Luma docs describe ray-2 / ray-flash-2 (including the `loop` flag), while the pricing page sells Ray 3.2. I have not confirmed that `loop` exists on Ray 3.2.
5. **No public evidence on painted-2D sprite-cycle fitness** for any candidate: first-frame identity, flat plate, no drift. This is the central T2 gap, and the bake-off is the only way to close it.
6. **Not checked per vendor:**
   - Rate limits (only xAI's 10 requests/s verified).
   - Output ownership and commercial terms on fal-resold closed models.
   - Data retention (only Veo's 2 days and Sora's 1-hour URLs verified).
   - Whether Veo's forced audio affects price (Gemini lists no audio-off rate).
7. **Unverified R1 capabilities:**
   - Wan-Animate background behaviour in animation mode.
   - Stylised-character support in Wan-Animate or Kling Motion Control.
   - Whether Wan-Animate-2's viewpoint control is hosted anywhere.
8. **Free tiers are thin:** none on Veo, fal, OpenAI or Runway. The only real free offer found is Alibaba's 50 video seconds for 90 days (PR), plus Vidu's half-price off-peak window (V).

---

## Sources (all accessed 2026-09-14)

**xAI / Grok**
- https://docs.x.ai/docs/models
- https://docs.x.ai/docs/models/grok-imagine-video
- https://docs.x.ai/docs/models/grok-imagine-video-1.5
- https://docs.x.ai/docs/guides/video-generations
- https://docs.x.ai/developers/pricing
- https://x.ai/news/grok-imagine-1-5
- https://openrouter.ai/x-ai/grok-imagine-video
- https://www.eesel.ai/blog/xai-pricing (PR)
- https://techjacksolutions.com/ai-brief/ai-video-news-grok-imagine-video-15-launches-25-second-gener/ (PR)
- BLOCKED: https://x.ai/api/imagine · https://vercel.com/ai-gateway/models/grok-imagine-video-1.5

**Google / OpenAI / Runway / Luma**
- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemini-api/docs/veo
- https://developers.openai.com/api/docs/pricing
- https://developers.openai.com/api/docs/guides/video-generation
- https://docs.dev.runwayml.com/guides/pricing/
- https://docs.aimlapi.com/api-references/video-models/runway/gen4_turbo (PR)
- https://runware.ai/docs/models/runway-gen-4-5/guides/directing-motion (PR)
- https://lumalabs.ai/api/pricing
- https://docs.lumalabs.ai/docs/video-generation

**fal model pages**
- https://fal.ai/pricing
- https://fal.ai/models/fal-ai/kling-video/v3/standard/image-to-video
- https://fal.ai/models/fal-ai/kling-video/v3/turbo/standard/image-to-video
- https://fal.ai/models/fal-ai/kling-video/v2.5-turbo/pro/image-to-video
- https://fal.ai/models/fal-ai/kling-video/v2.6/standard/motion-control
- https://fal.ai/models/fal-ai/minimax/hailuo-2.3/standard/image-to-video
- https://fal.ai/models/fal-ai/minimax/hailuo-2.3-fast/standard/image-to-video
- https://fal.ai/models/fal-ai/bytedance/seedance/v1.5/pro/image-to-video
- https://fal.ai/models/bytedance/seedance-2.0/image-to-video (V-snip)
- https://fal.ai/models/fal-ai/wan/v2.2-a14b/image-to-video
- https://fal.ai/models/fal-ai/wan/v2.2-14b/animate/move
- https://fal.ai/models/fal-ai/pika/v2.2/image-to-video
- https://fal.ai/models/fal-ai/ltx-2/image-to-video/fast
- https://fal.ai/models/fal-ai/ltx-2.3/image-to-video/fast/api
- https://fal.ai/models/fal-ai/hunyuan-video-v1.5/image-to-video (V-snip)
- https://fal.ai/models/fal-ai/cogvideox-5b/image-to-video

**MiniMax / Alibaba Wan / Vidu**
- https://platform.minimax.io/docs/guides/pricing-video
- https://www.therundown.ai/tools/wan-2-6 (PR)
- https://www.alibabacloud.com/help/en/model-studio/model-pricing
- https://platform.vidu.com/docs/pricing

**Step-down routes (R1–R4)**
- https://huggingface.co/Wan-AI/Wan2.2-Animate-14B
- https://arxiv.org/abs/2509.14055
- https://arxiv.org/abs/2608.06009
- https://replicate.com/fofr/tooncrafter
- https://github.com/Doubiiu/ToonCrafter
- https://www.svp-team.com/wiki/RIFE_AI_interpolation (PR)
- https://github.com/facebookresearch/AnimatedDrawings
- https://www.godmodeai.co/ai-spine-animation
- https://www.anysplit.net/ (PR)
- https://docs.meshy.ai/en/api/pricing
- https://www.meshy.ai/pricing

**Practitioner comparisons**
- https://sorceress.games/blog/ai-sprite-generator-pixel-walk-cycles-idles-and-vfx (PR)
- https://opencreator.io/blog/ai-video-models-comparison-2026 (PR)
