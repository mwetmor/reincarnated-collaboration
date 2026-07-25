# Research — GD Playtest Capture Instrument Scoping — 2026-07-25

**Mode:** A (analytical)
**Commissioner:** gandalf (`RUN-CONDUCTOR` / `ELICITOR`)
**Authorized by:** Matt, 2026-07-24
**Date established from primary source:** datetoday.net confirmed **Saturday, July 25, 2026** at research time. The commission is dated July 24; research was executed the following day. All "current" model and pricing figures below are as of July 25, 2026.
**Sources consulted:** Crate Entertainment forums, Steam community discussions, PCGamingWiki, Nexus Mods, GitHub (WanezGD_Tools, GrimDawnLuaUnlocker, heinermann), FearLess Cheat Engine forums, OpenAI API pricing page, Anthropic API pricing, Google Gemini API pricing, Roboflow blog, Ultralytics docs, Mixpeek/DataCamp/Labellerr VLM roundups, CloudZero/FinOut pricing summaries, digitalapplied.com computer-use comparison, localaimaster.com, insiderllm.com, Game Rant, VidaBytes, mejoress.com, en.paperblog.com.

---

## 1. Headline

**There is a partial non-vision channel in Grim Dawn, but it does not solve the measurement problem.** Two console debug commands — `character.ShowAngerLevels` and `character.LogData` — exist and expose AI anger state and entity data in-game. However, both output to on-screen overlay or console, not to a file. GD has no native combat log, no telemetry export, and no published memory-offset map for AI state. The DLL-injection community tool ecosystem (DPYes, Grim Internals) targets v1.2/v1.3 but has broken compatibility with v1.3.0.0 (Fangs of Asterkarn, released July 23, 2026). **The honest answer is: a useful but narrow non-vision channel exists — enough to validate KPI 2 (anger accumulation) at coarse temporal resolution via screen-reading the in-game overlay — but it does not replace a vision or memory-reading instrument for the other four BLOCKED KPIs.** The hybrid architecture hypothesis (CV tracking + VLM labeling + telemetry where it exists) is the right framing, though the telemetry leg is weaker than hoped.

---

## 2. Q1 — Non-vision channels: findings

### 2.1 Grim Internals — STATUS: BROKEN FOR v1.3.0.0

Grim Internals was the primary community overlay tool: it exposed combat text, monster HP bars, DPS readout, buff/debuff icons, and a "realtime combat log" (display only, not file output). Last official update: v1.107 x64, August 21, 2022, targeting GD v1.1.9.7. The Crate forum thread title explicitly says "v1.1.9.8 only" and even that version required a binary-swap workaround.

Fangs of Asterkarn shipped July 23, 2026 as v1.3.0.0 — a major patch that added a tenth mastery class, new territories, 60+ bosses, and accompanying engine changes. **Grim Internals has not been updated for v1.3.0.0 and is not expected to be** (author has been inactive since 2022). Community posts confirm it does not load under v1.3.

What Grim Internals *would have* exposed (prior versions): HP bars on monsters, floating combat numbers, a DPS meter. **Notably absent even in working versions:** world-space monster coordinates, AI state flags (aggro/idle/pursuing), anger accumulation values, spawn positions, or distress-call propagation.

### 2.2 DPYes — STATUS: REPORTEDLY COMPATIBLE WITH v1.3, LIMITED SCOPE

DPYes (Crate forum thread, v1.3 support noted) is a DLL-injection tool (deploys `DPYes.dll` + `DPYes.exe` into GD root folder; loads via `winmm.dll` proxy DLL). It exposes:
- DPS meter for player damage dealt/received and pet damage
- Game speed adjustment, teleportation, auto-loot, zoom extension

**Does not expose:** monster positions, AI state, anger levels, aggro radius, HP of individual mobs in a queryable form, or any data export to file. Generates debug output via Windows Sysinternals DebugView (not a structured log). Compatibility with v1.3.0.0 (FoA) is stated by the author but unverified post-July-23-2026.

### 2.3 GD Stash / GD Item Assistant — NOT RELEVANT

GD Stash (Java, reads `database.arz`) and GD Item Assistant (process injection for stash management) operate on item data and stash contents, not on live gameplay state. They have no mechanism to expose monster entity positions, AI state, or combat events. Not relevant to the KPI measurement task.

### 2.4 Console debug commands — PARTIAL CHANNEL, SCREEN-ONLY

GD ships a developer debug console accessible **only in Custom Game mode** (tilde or apostrophe key). The commands relevant to the KPI task:

| Command | Documented behavior | Output surface | KPI relevance |
|---|---|---|---|
| `character.ShowAngerLevels` | "Debug information for AI" | On-screen overlay | **KPI 2 (anger accumulation)** — if it shows per-mob anger bars, OCR or visual read of this overlay gives coarse anger state. Exact output format unconfirmed. |
| `character.LogData` | "Displays a variety of data above player, NPCs, and monsters" | On-screen overlay above entities | **KPI 1, 4 partial** — may show HP, name, possibly position values over mobs. Exact fields unconfirmed. |
| `debug.physics` | "Physics engine data on occurrences" | On-screen | No KPI relevance |
| `graphics.Stats` | "Frame rate and a variety of stats" | On-screen | Useful for recording setup validation only |

**Critical limitation:** console commands require Custom Game mode. This disables achievements and may alter zone behavior. More important: **Custom Game mode may alter the very AI behavior being measured** — if zone seeding, spawning, or aggro parameters differ between Custom and normal mode, the measurement instrument changes the measured system. This is the trap the commission flagged (§ 1). **This must be confirmed before any measurement protocol relies on console commands.**

**Output is to screen only.** No command writes to a file. Capturing console output requires either (a) OCR of the in-game overlay, or (b) a memory-reading tool that intercepts the same values the console commands display.

### 2.5 Memory reading — FEASIBLE IN PRINCIPLE, NO CURRENT MAINTAINED TABLE FOR v1.3.0.0

The FearLess Revolution Cheat Engine community has documented GD memory tables, including "Enemy Anger" modifiers and "Enemy Pursuit Distance Multiplier." These are tables originally built for v1.1.x–v1.2.x. Cheat Engine tables for games like GD break on major patches because pointer offsets change. **No confirmed published Cheat Engine table targeting v1.3.0.0 was found in this search.** The FearLess forum was 403-blocked; the existence of updated tables cannot be confirmed or denied from available results.

What a working CE table *could* expose (based on historical tables): enemy anger values (matching `SightAngerRate`/`InnerSightAngerRate` mechanics), pursuit distance multipliers, possibly entity position pointers. **This is the highest-value non-vision channel if a working table can be obtained or constructed.** It would deliver exact numeric ground truth for KPIs 1, 2, 3, and 4 — not estimates.

**Crate Entertainment's stance on memory reading:** No explicit ToS prohibition found. GD is a single-player-first game with an active official modding culture. Crate has never banned Grim Internals or DPYes despite their being DLL injectors. The practical stance is permissive for single-player use. No online competitive component exists that would motivate enforcement.

### 2.6 The Lua modding path — SANDBOXED, NOT A TELEMETRY CHANNEL

GD ships a full modding toolset (ArchiveTool.exe, DBREditor.exe, AssetManager). Lua scripting is supported for quest/event scripting within mods. The Lua API exposed to modders includes `Game` (time, player, difficulty), `Character` (give items, experience, set coords), UI notifications, and quest management.

**What the Lua API does not include:** file I/O (no `io.write` or equivalent), network calls, access to individual monster AI state or positions, anger values, or any mechanism to emit structured data to an external process. The API is sandbox-constrained. A community project (GrimDawnLuaUnlocker) attempts to unwrap the Lua library to restore standard Lua functions including file I/O, but it has 4 commits, no documented maintenance for v1.3, and no evidence of a working telemetry pipeline built on top of it.

**The behavioral contamination risk is real:** a mod that emits telemetry would run inside a Custom Game mode session and would be authored against DBR parameters — the same parameters whose in-game expression we are trying to measure. If the mod alters zone layout, spawner behavior, or AI parameter loading, the measurement changes the system. Until this is ruled out by a narrow passthrough-only mod design, the Lua path carries a contamination flag.

### 2.7 GD's own file output — MINIMAL

GD writes to `Documents/MyGames/GrimDawn/Settings/Options.txt` (user settings). No combat log, no debug output file, no crash dump with entity state, no launch parameter documented to enable file-based logging. Community consensus (multiple Steam threads) is that GD does not produce a text-format combat log and this has been the case for the game's full lifespan.

### 2.8 Q1 Summary

| Channel | Available? | Data it provides | KPI coverage | File output? | Status |
|---|---|---|---|---|---|
| Grim Internals | No (broken v1.3.0.0) | HP bars, DPS display | Tangential | No | Dead |
| DPYes | Possibly (v1.3 claim unverified post-FoA) | DPS meter only | None (KPIs 1-5) | No | Unverified |
| Console: ShowAngerLevels | Yes (Custom Game only) | Anger state, format unknown | KPI 2 (partial) | No | Usable with caveats |
| Console: LogData | Yes (Custom Game only) | Entity data overlay, fields unknown | KPI 1, 4 (partial) | No | Usable with caveats |
| Cheat Engine memory table | Unknown for v1.3.0.0 | Anger values, pursuit distances, possibly positions | KPIs 1–4 if working | Via CE output | Not confirmed |
| Lua mod telemetry | Possible but fragile | Whatever the Lua API exposes | Unknown | With LuaUnlocker | Contamination risk |
| GD native file output | No | Nothing relevant | None | — | Does not exist |

---

## 3. Q2 — Instrument landscape as of 2026-07-25

### Pricing arithmetic method used throughout

- **Sampling rate assumed for game analysis:** 1 frame per second (1 fps) — rationale below in § 4.
- **Hourly frame count:** 3,600 frames/hour.
- **Image token assumption:** per Roboflow (May 2026 analysis) at 1920×1080 or comparable game-output resolution:
  - GPT-5.5: ~1,700 tokens/image (patch-based 32×32 tiling, high-detail)
  - Claude Sonnet (current pricing): ~2,765 tokens/image (width × height ÷ 750 = 1920×1080÷750)
  - Gemini 2.5 Flash: ~258–516 tokens/image (tile-based, 258 per 768×768 tile; 1080p = roughly 2 tiles = ~516 tokens)
- **Output tokens:** assumed 100 tokens/frame for structured numeric output (bounding boxes + event label).
- **Cost = (input_tokens × input_price + output_tokens × output_price) × frames_per_hour ÷ 1,000,000**

Note: the pricing for frontier models has shifted substantially since GPT-4o was the reference. The current generation is GPT-5.x and Gemini 3.x. Prices below are cited from sources dated May–July 2026; treat as spot estimates requiring re-check against live pricing pages.

---

### Candidate A: Frontier VLMs (cloud API)

#### A1: OpenAI GPT-5.4 (current mid-tier vision flagship)

| Field | Value |
|---|---|
| **Instrument** | GPT-5.4 via OpenAI API (vision input) |
| **Class** | Frontier VLM |
| **KPI coverage** | KPIs 1, 3, 4 plausible at low precision; KPI 2 (sub-second anger timing) requires <100ms latency per frame — not achievable via API; KPI 5 (multi-mob identity tracking) plausible but expensive at high frame rates |
| **Modality** | Post-hoc video analysis (frame extraction + batch) or periodic screenshot (real-time feasible at ≤1 fps) |
| **Windows deployment** | Python + `openai` SDK; trivial to install. No special hardware. |
| **Hardware requirement** | None on Matt's PC beyond internet connection. All compute is cloud-side. |
| **Cost per hour of gameplay** | Input: $2.50/M tokens. Output: $15.00/M tokens. At 1 fps: 3,600 frames × (1,700 input + 100 output) / 1,000,000 = 3,600 × 1,800 / 1M = **6.48M tokens → $16.20 input + $0.54 output = ~$16.74/hour** at 1 fps. At 0.25 fps (1 frame per 4 seconds): **~$4.19/hour**. |
| **Maturity** | Shipping; GPT-5.4 is current stable tier (July 2026) |
| **Licensing/ToS** | OpenAI API ToS does not restrict analysis of game footage. Screen capture for data extraction is a documented use case. |

**Precision per KPI class:**
- KPI 1 (aggro onset distance): ±2–4 m estimated — VLM must estimate pixel distance from game frame; calibration required; single-digit meter precision achievable with good prompting.
- KPI 2 (anger latency sub-second): Not feasible at API rates. API round-trip latency is typically 1–3 seconds minimum; sub-second timing requires a different instrument.
- KPI 3 (pursuit/leash timing): ±0.5–1 s feasible at 1 fps. Tolerable for KPI 3's ±0.5s requirement only if frame is timestamped.
- KPI 4 (idle wander): Position tracking over minutes is feasible if frames are sampled at 0.1–0.5 fps; excursion radius estimation requires calibrated pixel-to-distance conversion.
- KPI 5 (distress-call propagation): Identity tracking across frames is weak — VLMs do not maintain persistent object IDs across calls; requires external tracking layer.

#### A2: Gemini 2.5 Flash (Google)

Note: Gemini 2.5 Flash is scheduled for deprecation October 16, 2026. Successor is Gemini 3 Flash Preview.

| Field | Value |
|---|---|
| **Instrument** | Gemini 2.5 Flash via Google Gemini API |
| **Class** | Frontier VLM |
| **KPI coverage** | Same structure as GPT-5.4; Flash is faster with lower accuracy |
| **Modality** | Post-hoc or periodic screenshot; video understanding supported natively (frames extracted at $0.00079/frame per Gemini pricing) |
| **Windows deployment** | Python + `google-generativeai` SDK |
| **Hardware requirement** | None on PC |
| **Cost per hour of gameplay** | Input: $0.30/M tokens. Output: $2.50/M tokens. At 1 fps: 3,600 × (516 input + 100 output) / 1M = **2.22M tokens → $0.67 input + $0.25 output = ~$0.92/hour**. Gemini video pricing: 3,600 frames × $0.00079 = **$2.84/hour** via video-frame path (higher because the $0.00079/frame rate is for the video embedding model, not the generative model — do not conflate these). At 0.25 fps: **~$0.23/hour** via screenshot path. |
| **Maturity** | Shipping but pending deprecation Oct 2026; migrate to Gemini 3.x for longevity |
| **Licensing/ToS** | Google API ToS permits commercial analysis of user-provided content including game captures |

**Precision per KPI class:** Same structural limits as GPT-5.4. Flash offers faster throughput but lower spatial reasoning accuracy — possibly worse on pixel-to-distance estimation.

#### A3: Claude Sonnet 5 (Anthropic, via API)

| Field | Value |
|---|---|
| **Instrument** | Claude Sonnet 5 via Anthropic API (vision input) |
| **Class** | Frontier VLM |
| **KPI coverage** | Same structure; Claude strong on structured output + OCR, competitive for event labeling |
| **Modality** | Post-hoc or periodic screenshot |
| **Windows deployment** | Python + `anthropic` SDK |
| **Hardware requirement** | None on PC |
| **Cost per hour of gameplay** | Input: $3.00/M tokens (standard; introductory $2.00 through Aug 31 2026). At 1 fps: 3,600 × (2,765 input + 100 output) / 1M = **10.32M tokens → $30.96 input + $0.36 output = ~$31.32/hour** at standard rate. At 0.25 fps: **~$7.83/hour**. Claude's area-formula tokenization makes it the most expensive per-image at 1080p resolution. |
| **Maturity** | Shipping |
| **Licensing/ToS** | Anthropic usage policy: analysis of game footage for research purposes is not restricted |

#### A4: OpenAI GPT-5.4-mini (budget frontier)

| Field | Value |
|---|---|
| **Instrument** | GPT-5.4-mini |
| **Class** | Frontier VLM (budget tier) |
| **KPI coverage** | Weaker spatial reasoning than GPT-5.4; suitable for event labeling (onset yes/no) but less reliable for precise distance estimation |
| **Cost per hour of gameplay** | Input: $0.75/M tokens. At 1 fps: 3,600 × 1,800 / 1M = 6.48M × $0.75 = **$4.86/hour input + $0.36/hour output = ~$5.22/hour** |
| **Maturity** | Shipping |

---

### Candidate B: Computer-use / screen-agent harnesses

#### B1: Claude computer use (Windows-native via Desktop app)

| Field | Value |
|---|---|
| **Instrument** | Claude computer use (Anthropic API computer-use tool) |
| **Class** | Screen agent / computer-use harness |
| **KPI coverage** | Can observe screen, interpret state, issue actions ("approach that mob"). Useful for **controlled-trial execution** (KPIs 1, 2, 5 require controlled approach/retreat runs); can direct Matt's play. Not suited for high-frequency measurement. |
| **Modality** | Real-time screenshot-roundtrip; typically 1–4 second cycle |
| **Windows deployment** | Claude Desktop app for Windows (launched Feb 10, 2026). API-based orchestration also available. |
| **Hardware requirement** | None (cloud-side compute); Windows PC + Claude Desktop app |
| **Cost per hour of gameplay** | Same as Claude Sonnet 5 API rate per screenshot, but typically invoked at lower frequency (human-in-the-loop pacing). At 1 screenshot per 5 seconds: 720 frames/hour × 2,865 tokens = 2.06M tokens → **~$6.19/hour** |
| **Maturity** | Shipping; Windows feature parity confirmed Feb 2026 |
| **Licensing/ToS** | Same Anthropic policy; computer-use for research data collection is not restricted |

**Note on utility:** Claude computer use is the only agent class that can **direct** Matt's gameplay (send text instructions, observe the result, confirm event onset). This is load-bearing for KPIs 1, 2, and 5, which require controlled approach trials rather than opportunistic observation.

**Note on OpenAI Codex computer use:** macOS-first as of July 2026; Windows not yet shipping. Not a viable candidate for Matt's PC.

**Note on Gemini computer use:** browser-anchored only; cannot control native Windows desktop apps. Not viable.

---

### Candidate C: Open / local VLMs

#### C1: Qwen2.5-VL 7B via Ollama (Windows)

| Field | Value |
|---|---|
| **Instrument** | Qwen2.5-VL 7B, Q4_K_M quantization, via Ollama on Windows |
| **Class** | Local/open VLM |
| **KPI coverage** | Event labeling, basic spatial reasoning. Benchmark quality competitive with GPT-4o-class on standard VQA. Spatial distance estimation: untested for this task. |
| **Modality** | Post-hoc or periodic screenshot; local inference removes API latency floor |
| **Windows deployment** | Install Ollama for Windows → `ollama pull qwen2.5vl:7b`. Python client. No special coding. |
| **Hardware requirement** | **Minimum 8 GB VRAM** (Q4_K_M). RTX 3060/3070/4060 class. **Matt's PC spec is unknown.** An RTX 3050 with 4 GB VRAM cannot run this model. A 12 GB VRAM card runs it comfortably with headroom. |
| **Cost per hour of gameplay** | $0 API cost. Electricity + hardware amortization only. Inference speed on RTX 3060: roughly 10–20 tokens/second for text; vision inference including image encoding is slower, approximately 2–5 seconds per frame for a 7B model — meaning sustained 1 fps analysis is borderline feasible; 0.25 fps is safe. |
| **Maturity** | Shipping; Ollama stable on Windows; Qwen2.5-VL 7B is available as Ollama model |
| **Licensing/ToS** | Apache 2.0 (Qwen2.5-VL); Ollama MIT. No restrictions on game footage analysis. |

#### C2: Qwen3-VL (successor, as available)

The search results reference Qwen3-VL as a 2026 improvement over Qwen2.5-VL on spatial and multi-object tasks. Hardware requirements are similar (7B variant, 8 GB VRAM). Availability via Ollama as of July 2026 is confirmed by community sources but the exact model card was not directly inspected.

#### C3: MiniCPM-V 4.5

Noted in local-VLM sources as supporting up to ~10 fps via temporal frame compression (6 frames → 64 tokens). Relevant for high-frame-rate video analysis. VRAM requirement: lower than Qwen2.5-VL (reportedly ~4–6 GB). This is the most viable candidate if Matt's VRAM is limited. Temporal compression means sequential frames are analyzed as a batch — useful for KPI 3 (leash timing) and KPI 4 (wander tracking).

---

### Candidate D: Classical CV and object-tracking stacks

#### D1: OpenCV + YOLO + ByteTrack (deterministic tracking pipeline)

| Field | Value |
|---|---|
| **Instrument** | YOLO detection (YOLOv8/v11 or YOLO-World) + ByteTrack multi-object tracker + OpenCV for pixel measurement |
| **Class** | Classical CV + modern tracker |
| **KPI coverage** | **Highest precision for spatial KPIs** (1, 3, 4) if monsters are detectable. Distance is pixel → world-unit via calibration. Sub-50ms timing precision is achievable. KPI 5 (multi-mob tracking) is exactly what ByteTrack was built for. KPI 2 (anger accumulation) requires reading the anger-state change in the overlay, which is OCR territory not detection territory. |
| **Modality** | Real-time at 30+ fps (ByteTrack operates at 171 fps on GPU); post-hoc on captured video |
| **Windows deployment** | Python + `ultralytics` + `opencv-python`. Requires a custom YOLO model trained to detect Grim Dawn monster sprites. Training requires labeled screenshots (~200–500 labeled examples per monster class for detection). |
| **Hardware requirement** | CPU: feasible at reduced fps. GPU: RTX 3060 or better for real-time 30 fps analysis. YOLO inference is much lighter than a VLM — 4 GB VRAM is sufficient. |
| **Cost per hour of gameplay** | $0 API cost post-setup. Setup cost: ~4–8 hours engineering to train a detector on labeled GD screenshots + calibrate pixel-to-distance constant. |
| **Maturity** | YOLOv11/YOLO-World: shipping. ByteTrack: production-grade. OpenCV: mature. |
| **Licensing/ToS** | All open source (AGPL-3.0 / MIT). No footage restrictions. |

**Precision per KPI class:**
- KPI 1 (onset distance): ±0.3–0.8 m if calibration constant is known (see § 2 note below on camera)
- KPI 2 (anger latency): YOLO cannot read anger state; would need OCR of `ShowAngerLevels` overlay alongside tracking
- KPI 3 (leash timing): ±0.1–0.5 s depending on frame rate
- KPI 4 (wander): ±0.5 m over long window; most tractable of all KPIs with tracking
- KPI 5 (distress propagation): ByteTrack maintains persistent IDs across frames — multi-mob alerting is directly measurable; 75% rate estimation requires ~40+ events

**Camera calibration note (from research):** GD uses a variable-pitch non-rotating (base game) or slowly-rotating camera at a three-quarter isometric angle. The camera **can rotate** (left/right via hotkeys) and **zoom** is adjustable by player. This means pixel-per-world-unit is **not a fixed constant** — it varies with zoom level and camera rotation. Establishing a stable calibration requires either (a) locking zoom and disabling rotation during test sessions, or (b) dynamically re-calibrating per frame using known geometry (e.g., tile grid or character height as reference). This is a significant constraint. The brief's hypothesis that calibration might be "a stable constant" is **not confirmed — it is variable.** Players can and do adjust zoom mid-session.

#### D2: OCR pipeline (Tesseract / EasyOCR / WindowsOCR) — for overlay reading

| Field | Value |
|---|---|
| **Instrument** | OCR (Tesseract, EasyOCR, or Windows built-in OCR API) targeting `character.ShowAngerLevels` overlay and `character.LogData` entity overlay |
| **Class** | Classical CV (OCR) |
| **KPI coverage** | KPI 2 (anger accumulation): if `ShowAngerLevels` shows a numeric bar or value, OCR at 5–10 fps captures anger evolution. KPI 1 and 4: if `LogData` prints position values above entities. |
| **Modality** | Real-time (sub-100ms per OCR pass at low complexity) |
| **Windows deployment** | `pytesseract` or `easyocr` Python; trivial |
| **Hardware requirement** | CPU-only; minimal |
| **Cost per hour of gameplay** | $0 |
| **Maturity** | Mature |
| **Precision concern:** The exact format of `ShowAngerLevels` output is not confirmed from available sources (only "debug info for AI" documented). If it outputs a floating-point anger value per mob, OCR can extract it. If it outputs a visual bar only, OCR accuracy degrades. **This must be tested before relying on it.** |

#### D3: Video capture pipeline (OBS + ffmpeg + millisecond timestamps)

This is infrastructure, not an instrument — but it is the highest-leverage enabler in the stack.

- OBS `gdigrab`/game-capture records GD at 60 fps with hardware-encoded H.264/AV1
- ffmpeg with `-accurate_seek` and `-ss` in milliseconds extracts frames at any sample rate post-hoc
- Frame timestamp precision: sub-millisecond from video PTS (presentation timestamp)
- **Key advantage:** records once; any number of instruments can be run against identical footage in post-hoc mode — this is what makes a fair bake-off possible
- Windows deployment: OBS and ffmpeg are both trivial to install on Windows; no special hardware beyond a GPU encoder (NVENC) which any gaming PC has
- Cost: $0
- This should be **assumed as baseline infrastructure** for the bake-off regardless of which VLM/CV instrument is selected

---

## 4. Q3 — Real-time vs post-hoc; protocol question

### 4.1 The experimental protocol question precedes the instrument question

This is the finding the commission anticipated. For KPIs 1, 2, and 5, opportunistic footage of normal play is almost certainly insufficient:

- **KPI 1 (aggro onset radius):** Requires a clean approach run — hero walking toward a stationary, un-aggroed mob from a known distance. Normal play has the hero running through packs constantly. Finding a clean approach in opportunistic footage requires hours of footage and careful labeling.
- **KPI 2 (anger accumulation):** Requires standing at a known distance from a mob's outer/inner zone boundary for a measured time, then observing the onset. A 4× rate ratio between inner and outer zones (12.0 vs 3.0 anger/s) needs ±50ms precision. Normal play provides no controlled trial.
- **KPI 5 (distress-call propagation rate):** A 75% response rate needs approximately 40 aggro events to estimate at ±10% confidence (binomial: n=40 → ±7.5%). Normal play would need to be mined for events where exactly one mob aggros and neighbors are in the 16-wu range. This is possible from post-hoc video but requires many labeled events.
- **KPIs 3 and 4** (pursuit/leash, idle wander) are more tractable from opportunistic footage — wander happens constantly to un-aggroed mobs, and leash events happen frequently in normal play.

**Conclusion:** The bake-off design requires two session types:
1. **Controlled-trial sessions** (scripted): Matt approaches a lone mob at measured pace, stops, waits, retreats. Repeated 40+ times per zone for KPI 5. These sessions exist primarily to yield clean measurement events, not gameplay value.
2. **Opportunistic sessions** (free play): For KPIs 3 and 4, normal play footage suffices.

**A VLM or CV agent that can direct Matt in real-time is load-bearing for the controlled-trial sessions.** Claude computer use is the candidate for this role — it can observe the screen and prompt Matt ("walk toward the pack slowly, stop when I say"). Post-hoc analysis cannot substitute for real-time direction in these sessions.

### 4.2 Real-time vs post-hoc recommendation per KPI

| KPI | Session type needed | Instrument modality needed | Minimum sample size |
|---|---|---|---|
| 1 — Aggro onset radius | Controlled approach runs | Real-time direction + post-hoc measurement | ~20 runs (2 zones: outer + inner) |
| 2 — Anger accumulation latency | Controlled dwell runs | ShowAngerLevels OCR (real-time) + timestamp log | ~10 runs per zone (inner + outer) |
| 3 — Pursuit / leash | Opportunistic | Post-hoc video measurement | ~20 events |
| 4 — Idle wander | Opportunistic | Post-hoc video measurement | 1–2 un-aggroed mob observations over 5 min each |
| 5 — Distress-call propagation rate | Controlled aggro triggers | Post-hoc labeling of many events | 40+ events for ±10% rate precision |

### 4.3 On sampling rate and the 1 fps assumption

The 1 fps figure used in pricing arithmetic deserves defense:
- KPI 2 requires sub-second precision → 10 fps minimum for the anger-accumulation measurement leg, but only during the onset window (seconds around the event, not the whole session)
- KPIs 3 and 4 are multi-second events; 1 fps is sufficient
- KPI 1 onset is a single frame event; 1 fps is sufficient if onset is confirmed on the anger/AI-state overlay simultaneously
- KPI 5 requires fast multi-mob state reads; 2–5 fps during aggro events

**Practical architecture:** capture at 60 fps via OBS; analyze only key windows (approach runs, onset moments) at high frame rate; analyze idle wander at 0.1 fps. This collapses the effective cost by 10–100× vs continuous 1 fps analysis.

---

## 5. Proposed bake-off design

### Premise

Matt hands one agent at a time the spec and plays while it captures. The bake-off needs:
1. Identical footage as input (achievable via OBS recording)
2. A task all candidates are given exactly the same way
3. Pass criteria that map to KPI measurement quality, not general VLM benchmarks
4. A cost estimate for running the bake-off itself

### Finalists (3–5)

| Finalist | Class | Rationale for inclusion |
|---|---|---|
| **F1: Classical CV pipeline (YOLO + ByteTrack + OCR)** | Deterministic | Ground-truth candidate for spatial KPIs; highest precision; cost-free at run time; requires upfront training effort |
| **F2: Gemini 2.5 Flash (or 3.x Flash successor)** | Frontier VLM (cheap) | Lowest API cost per hour (~$0.92/hr at 1 fps); native video understanding; benchmarks well on spatial/OCR |
| **F3: GPT-5.4-mini** | Frontier VLM (budget) | Intermediate cost (~$5.22/hr); strong structured-output reliability |
| **F4: Qwen2.5-VL 7B (local)** | Local VLM | $0 API cost; privacy; benchmarks competitive with GPT-4o-class; contingent on Matt's VRAM being 8 GB+ |
| **F5: Claude computer use (for trial direction only)** | Screen agent | Not competing on measurement precision; included specifically to evaluate whether real-time trial direction enables better controlled experiments for KPIs 1, 2, 5 |

### Bake-off task specification

**Session recording:** Matt plays a 30-minute controlled-trial session using a blank character in an early-game area with sparse mob density (so mobs are individually identifiable). OBS records at 60 fps with system clock timestamps synced. Session includes:
- 10 approach-until-onset runs (hero walks slowly toward one un-aggroed mob)
- 5 dwell-at-distance runs (hero stands inside apparent outer zone, waits 10s, retreats)
- 10 minutes of free play for leash / wander observation

**Task given to each finalist:** "Given this video (or screenshot stream), for each approach run: (1) at what elapsed time does the mob begin moving toward the player; (2) estimate the screen-pixel distance between hero and mob at that instant; (3) classify the mob's behavior as idle / pursuing / returning."

**Pass criteria:**
- Onset detection: sensitivity ≥80% (detects ≥8/10 runs as an onset event)
- Onset frame precision: within ±0.5 s of human-labeled ground truth
- Distance estimate: within ±15% of the calibration-corrected ground truth (established by human pixel-measurement of the same frame)

**Calibration step (pre-bake-off, not per-finalist):** Measure pixel distance between two known GD landmarks (e.g., tiled floor squares whose in-game dimension is known from DBR data) at Matt's default zoom setting. Lock zoom for all bake-off sessions. This is a 30-minute one-time task, not per-finalist.

**Estimated cost of running the bake-off:**
- Recording session: 30 min of Matt's time (one session, reused by all finalists)
- F1 (classical CV): ~4–8 hours engineering to train YOLO detector; inference is free
- F2 (Gemini Flash): 30 min × 60 fps → 1,800 frames → at analysis rate 1 fps from post-hoc → 450 frames analyzed (0.25 fps effective) → ~$0.10–$0.20 total cost
- F3 (GPT-5.4-mini): ~$0.50–$1.00 per 30-min run
- F4 (local): $0 if VRAM adequate; requires Ollama setup time (~1 hour)
- F5 (Claude computer use): real-time session, billed per screenshot → ~$3–5 for a 30-min trial session at 1 screenshot/5s

**Total bake-off budget estimate:** $5–$15 API cost + ~10 hours engineering for the CV pipeline. The CV pipeline setup cost is front-loaded but the production instrument costs nothing per hour thereafter.

---

## 6. Coverage-boundary declaration (D-a — MANDATORY)

**What this research could NOT check and why:**

1. **FearLess Revolution Cheat Engine forum (fearlessrevolution.com):** Returned 403 Forbidden during fetch. I confirmed from search result summaries that GD CE tables exist and have historically documented "Enemy Anger" modifiers, but I could not verify whether any table targets v1.3.0.0 (FoA). The current state of the CE table ecosystem for FoA is unconfirmed. This is the single most consequential gap in Q1 — a working CE table for v1.3.0.0 would materially change the architecture.

2. **Crate Entertainment forums — thread pages 2+ of Console Commands Reference and Grim Internals thread:** The main thread pages beyond page 1 were not accessible (Discourse forum pagination + 403). I retrieved the OP for Grim Internals compatibility info and console command descriptions from third-party aggregators. The exact output format of `character.ShowAngerLevels` (whether it shows a numeric value vs a visual bar, whether it labels per-mob or globally) was not confirmed from a primary source. This affects the OCR-of-overlay approach directly.

3. **PCGamingWiki Grim Dawn page:** Returned 403. Config file locations, launch parameters, and any version-specific notes were taken from secondary sources (Steam discussions, community blogs) rather than PCGamingWiki's structured table.

4. **OpenAI current pricing page (developers.openai.com):** The direct fetch returned data inconsistent with other sources (showed `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna` variants not found in other 2026 pricing summaries). These model IDs may be real or may be hallucinations by the WebFetch model summarizing the page. I used the crosschecked figures from multiple third-party pricing aggregators (finout.io, metacto.com, pecollective.com) instead. OpenAI pricing page itself was not cleanly verified; treat all OpenAI pricing figures as approximate ±20%.

5. **Matt's PC hardware spec:** Explicitly unknown. The local VLM section (C1-C2) gives VRAM floors; whether Matt's PC meets them cannot be stated. The `matt_to_do` T2 item (cited in commission brief) confirms we do not have a certified GPU spec on file.

6. **GrimDawnLuaUnlocker functionality:** The GitHub repo was visible but the README was not informative about which Lua functions are unlocked. I could not determine whether `io.write` or equivalent file output is enabled. This was not pursued further because the Lua path carries an independent contamination risk (Custom Game mode + mod potentially altering measured behavior).

7. **DPYes post-FoA compatibility:** The forum thread stated "v1.3 support" but this predates the July 23, 2026 FoA release. No post-July-23 confirmation of DPYes working with v1.3.0.0 was found.

8. **The `character.ShowAngerLevels` precision question:** No screenshot, video, or firsthand account of what this overlay looks like was found. "Debug information for AI" is the only documentation. Whether it shows a per-mob anger scalar (useful for KPI 2 extraction) or a simple is-aggroed indicator is unknown.

9. **Gemini 3.x Flash pricing:** Gemini 3 Flash Preview ($0.50/$3.00/M tokens) was mentioned in deprecation context but not directly priced for vision/image input. The image token formula for Gemini 3.x was not separately confirmed.

10. **Local VLM inference speed benchmarks on consumer gaming GPUs for vision:** Found text-token throughput benchmarks (57 tokens/sec on RTX 3060) but not vision-specific (screenshot encode + inference) throughput. The 2–5 second estimate per frame for Qwen2.5-VL 7B at 1080p is an inference from general model behavior, not a cited benchmark.

---

## 7. Open questions for Matt

These require Matt's input and cannot be resolved from external research:

1. **PC hardware spec (GPU model and VRAM).** The local VLM path (Candidate C) is viable if VRAM ≥ 8 GB. If VRAM is 4 GB or less, local VLMs are not viable and the choice is between cloud API instruments and the classical CV pipeline. This is a binary branch point in the bake-off design.

2. **Willingness to install a DLL injector (DPYes) on the GD installation.** DPYes requires dropping a DLL into the game root folder. It is community-maintained and uses `winmm.dll` proxy injection — not a signed driver, not a rootkit, but it does modify the process. Matt's comfort level with this determines whether the DPS meter / debug data access from DPYes is in scope.

3. **Willingness to seek / compile / use a Cheat Engine table for v1.3.0.0.** This is the highest-value Q1 channel if a working table can be found. It requires: installing Cheat Engine, obtaining or building a pointer map for FoA-era GD, and running CE alongside GD during sessions. Matt's comfort level with CE tooling is unknown.

4. **Custom Game mode for controlled-trial sessions.** The debug console commands (`ShowAngerLevels`, `LogData`) only work in Custom Game mode. Does enabling Custom Game mode alter mob AI parameters or zone seeding in a way that would make the measurements unrepresentative of normal play? Matt may have direct knowledge from his GD experience, or this may require a targeted test (compare mob behavior in Custom vs normal mode).

5. **Zoom level discipline during bake-off sessions.** The camera calibration is only stable if zoom level is locked. Is Matt willing to lock zoom for the 30-minute controlled-trial sessions? (Normal-play sessions for KPIs 3 and 4 do not require this.)

6. **Tolerance for scripted play sessions.** The controlled-trial protocol for KPIs 1, 2, and 5 requires Matt to walk a hero slowly toward a mob and stop repeatedly — not normal gameplay. How many such sessions is he willing to do, and in what area of the game (early-game access to a diverse mob set is helpful)?

7. **Cost tolerance per bake-off run.** At $0.92/hour (Gemini Flash) to $31.32/hour (Claude Sonnet) for continuous 1-fps cloud analysis, and $0 for local or classical CV, the cost question is not about the bake-off (small) but about the production measurement run. How many hours of play is Matt planning for the GD measurement program? That determines whether the cloud API instruments are feasible at all.

8. **Any existing GD modding infrastructure.** Matt is the player; does he already use any custom mods, GrimCam, or other overlays that would interact with the bake-off instruments? A GrimCam mod that extends zoom would break pixel-calibration unless accounted for.

---

## Source list

- datetoday.net — today's date confirmation (accessed 2026-07-25): https://www.datetoday.net/
- Crate Entertainment forum — Grim Internals thread: https://forums.crateentertainment.com/t/tool-grim-internals-v1-1-9-8-only/38773
- Crate Entertainment forum — DPYes thread: https://forums.crateentertainment.com/t/tool-dpyes-player-pet-dps-meter-misc-util/133378
- Crate Entertainment forum — Lua API thread: https://forums.crateentertainment.com/t/script-lua-api-sort-of/106349
- Crate Entertainment forum — Lua Resources: https://forums.crateentertainment.com/t/lua-resources/35166
- ResetEra — Fangs of Asterkarn release: https://www.resetera.com/threads/grim-dawn-fangs-of-asterkarn-releases-july-23-2026.1533202/
- Game Rant — GD console commands: https://gamerant.com/grim-dawn-console-command-list-help/
- Steam community — GD combat log discussion: https://steamcommunity.com/app/219990/discussions/0/3454730619133205198/
- Steam community — GD camera angle discussion: https://steamcommunity.com/app/219990/discussions/0/1738882453509730412/
- GitHub — WanezGD_Tools: https://github.com/WareBare/WanezGD_Tools
- GitHub — GrimDawnLuaUnlocker: https://github.com/heinermann/GrimDawnLuaUnlocker
- Google Gemini API pricing: https://ai.google.dev/gemini-api/docs/pricing
- Roboflow — image token costs VLMs: https://blog.roboflow.com/image-token-cost-vlm/
- CloudZero — Gemini pricing 2026: https://www.cloudzero.com/blog/gemini-pricing/
- finout.io — OpenAI pricing 2026: https://www.finout.io/blog/openai-pricing-in-2026
- finout.io — Anthropic pricing 2026: https://www.finout.io/blog/anthropic-api-pricing
- Digital Applied — computer use agents 2026: https://www.digitalapplied.com/blog/computer-use-agents-2026-claude-openai-gemini-matrix
- localaimaster.com — local AI video analysis: https://localaimaster.com/blog/local-ai-video-analysis
- insiderllm.com — vision models locally: https://insiderllm.com/guides/vision-models-locally/
- Ultralytics — ByteTrack docs: https://academy.ultralytics.com/courses/yolo-in-production/tracking-with-bytetrack-and-botsort
- FoA release — Fangs of Asterkarn Crate forum: https://forums.crateentertainment.com/t/grim-dawn-fangs-of-asterkarn-releases-july-23rd-2026/154855
- Mixpeek — best VLMs 2026: https://mixpeek.com/curated-lists/best-vision-language-models
