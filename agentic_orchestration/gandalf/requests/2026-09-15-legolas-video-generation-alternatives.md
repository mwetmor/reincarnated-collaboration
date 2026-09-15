# Legolas Mode A — free / cheap video-generation models callable via API, compared against the Grok image_to_video route used in Run C-3

> **STATUS:** CURRENT — research commission, gandalf (RUN-CONDUCTOR, Run C-3). Matt 2026-09-15: *"look up free or cheap video generation apps/models that we can use in a similar process, called via API, with the goal of comparing them to the specific Grok model that we used. … the video generation is a HUGE bottleneck for us. We will likely need one video for each character's gear tier × each direction, motion, ability … possibly one video per each character's individual piece of gear × all of the above."* Higher priority than stepping the ChatGPT model down.

## 0. The baseline to beat — exactly what Grok did in C-3 (from the run ledger, 71 calls)

| Fact | Value |
|---|---|
| Tool | **Grok Build CLI** (`grok-shell` 1.0.30, origin `cli-chat-proxy.grok.com`), chat model `grok-4.6`, its **`image_to_video`** tool (xAI Grok Imagine video backend; the CLI does not print the video model id — **pin it, with the public API model name and list price, as task 1**) |
| Call shape | `image_to_video(image = STILL as the FIRST frame, prompt, duration = 6, resolution = 720p)` — one call per clip, `--always-approve`, stop-on-first-failure |
| Output | MP4 **768 × 1168**, **24 fps**, 6.04 s, 145 frames; median wall **55 s** per clip |
| Input | one painted 2D character still per cell (Keeper, H1 painted register — tapered dark contour, painted planes — on a flat plate), 8 directions × motions {idle, idle_alert, walk, run, jump, cast …} |
| Billing | SuperGrok subscription "Grok Build usage balance"; cost NOT printed per call; **balance exhausted (HTTP 402) after 53 clips** → HALT H-C3-1, topped up by Matt |
| Success | 68 / 71 ok; 3 failures were the 402s |
| Downstream | `oracle/video_cut.py` + `oracle/steps_per_loop.py` cut a **loopable cycle** out of each clip (walk/run one stride; cast key frames), then the frames are matted (`gates/matte.py`) and packed to Godot SpriteFrames. So what matters is not "nice video" but: first frame == our still (identity, palette, contour), **no camera motion**, **flat background preserved**, one clean cycle inside the clip, silhouette stable across frames, no morphing of gear / hands / staff. |

The combinatorics Matt named: characters × gear tiers (× possibly per gear piece) × 8 directions × motions × abilities. At Grok's ~55 s and an unknown per-clip price, that is the bottleneck. **Two axes therefore:** (A) cheaper / faster / freer i2v with equal-or-better cycle-cut quality; (B) routes that reduce the NUMBER of videos needed at all (see T4) — Matt also said "step down from video generation".

## 1. Threads

**T1 — Hosted i2v APIs, priced.** For each: model + version · API access (direct vendor / fal.ai / Replicate / Vercel AI Gateway / Together …) · **price per clip at our shape** (≈5–6 s, ~720p, 24 fps, portrait) and per second · free tier or credits · rate limits · max/min duration, fps, resolutions, aspect ratios · **first-frame fidelity** (does the input still become frame 1 unchanged?) · last-frame / keyframe conditioning · camera-lock control (negative prompts, "static camera") · loop options · licence / commercial use · data-retention. Candidates to check at minimum: **xAI Grok Imagine API** (the API-side twin of what we used), **Runway Gen-4 / Gen-4 Turbo**, **Luma Ray 2 / Ray 3**, **Kling 2.x** (official + fal/Replicate), **MiniMax Hailuo 02**, **Google Veo 3 / 3.1** (Gemini API / Vertex), **OpenAI Sora 2 API**, **ByteDance Seedance 1.x**, **Vidu Q1/Q2**, **Pika 2.x**, **Wan 2.1 / 2.2 / 2.5** (hosted), **LTX-Video / LTX-2** (hosted), **HunyuanVideo** (hosted), **CogVideoX** (hosted). Mark the ones that are open-weights (they are the "free" tier if we ever get GPU access; **our host is a Mac mini with 8 GB RAM — local inference is NOT an option**, say so per model rather than assuming).

**T2 — Fit to OUR clip shape.** Which of the above accept a painted 2D character on a flat plate without (a) re-rendering it as 3D/photoreal, (b) adding camera drift, (c) inventing background? Look for published examples of 2D / anime / illustration i2v (Kling, Hailuo, Vidu and Wan advertise anime; Grok Imagine is what we know works). Any evidence on **loopable** or "sprite sheet" / "walk cycle" generation. Any model that takes **first + last frame** (Kling, Luma, Runway, LTX) — that is directly useful for a one-stride loop (last = first).

**T3 — A cheap first bake-off, designed.** Propose a 3-model shortlist and a **6-clip probe** (same 6 Keeper stills we already have in `runs/C-3/artifacts/K2c-gen-*/`, same prompt text, same 6 s / 720p ask) with the exact API calls, expected cost, and how we would score them against Grok: first-frame SSIM to the still, cycle found by `steps_per_loop.py` (yes/no + period), matte cleanliness, silhouette/palette drift across frames, wall time, $ per accepted clip. Return the cost estimate for the probe before anything is spent — Matt approves spend.

**T4 — Stepping DOWN from video generation (the bigger lever).** Survey the routes that make the per-gear / per-direction multiplication collapse instead of paying it per clip:
- **pose- / skeleton-driven character animation** from ONE still + a motion source (Wan-Animate / Wan 2.2 Animate, Kling Motion Control, Runway Act-Two, Animate Anyone / MagicAnimate / MusePose class, ToonCrafter keyframe interpolation, AnimateDiff): a motion recorded once, re-applied to every gear tier and every direction still — which of these are hosted, priced, and work on painted 2D?
- **2D cut-out / part rig** (Spine / Godot Skeleton2D / Live2D-style): animate once per motion, gear = texture swap on the part. Does anyone auto-rig a painted still via API (Meta Animated Drawings / Sketch RNN-class, Cascadeur 2D, Adobe Character Animator, Rive)? Where does it break for our contour-heavy H1 register?
- **frame-interpolation on our own keyframes** (RIFE / FILM / ToonCrafter): we paint 4–8 keys with the image model, interpolate the in-betweens for free locally (CPU feasible?) — that turns the video model into an optional step.
For each: cost, what it removes from the multiplication, quality risk, and the cheapest first experiment.

**T5 — Evidence discipline.** VERIFIED (vendor page / docs, with URL + date) · PRACTITIONER-REPORT (forum / blog, named) · DERIVED (your arithmetic, shown). Prices change monthly — timestamp every number. Never substitute recalled prices for un-fetched pages; if a page is blocked, say BLOCKED.

## 2. Deliverable (return as TEXT; gandalf files it at `agentic_orchestration/legolas/research/2026-09-15-video-generation-alternatives/findings.md`)
1. **TL;DR** — the 3-model shortlist for the T3 probe with its cost, and the single T4 route you would try first, in one paragraph.
2. **Comparison table** — model · access · price/clip (our shape) · free tier · first-frame fidelity · keyframe conditioning · camera lock · 2D/anime evidence · licence · evidence class + URL + date.
3. **Probe design** (T3) — calls, cost, scoring, what "beats Grok" means numerically.
4. **Step-down routes** (T4) — table + recommendation.
5. **Gaps / BLOCKED** stated plainly.

## 3. Host guardrails (hard — the 2026-09-14 kernel panic)
Web research only; **no downloads of model weights, no local inference, no video decoding**; run **serially** (no parallel sub-forks); stay under 1.5 GB RSS; the memory watchdog `~/Games/vendor/vfx-atlas/_memwatch.sh` kills any python/ffmpeg over 2 GB. Return text; do not write into the repo (the harness blocks it — gandalf files the findings).

— gandalf, 2026-09-15
