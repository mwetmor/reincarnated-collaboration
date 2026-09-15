# Painted-2D Scene Builder — THE SCENE WORKFLOW

> **STATUS:** CURRENT (load-bearing as of 2026-09-15) — see `canonical/00-ground-state.md`. The official scene-builder workflow for *Reap. Die. Rise.* (Matt R-C3-102). Workflow canon: it says **how a scene is built, by whom, with what gate**; the lane's machinery (bursts, audit, oracles, freeze, SYNC) is described in `00-system.md` and is not repeated here.

**Date:** 2026-09-15
**Author:** gandalf (CANON-STEWARD / SPEC-AUTHOR; RUN-CONDUCTOR of Run C-3)
**Status:** v1.0 — canonized from Run C-3 lap 2 (the cliffside scene, v3 → v15 + web2). Ground shadows OPEN (§ 4).
**Authority:** Matt 2026-09-15 — R-C3-102 (ledger text): *"once the shadows are finalized, CANONIZE this pipeline as the official scene-builder workflow; Synty left behind; 3D scenes crossed off the plan"*. **Precondition state:** the shadow layer was REMOVED entirely for the mobile playtest (R-C3-109 + amendment) and ground shadows remain OPEN (§ 4.1); **Matt confirmed 2026-09-15 (R-C3-119): "the Godot scene with shadow layer removed meets expectations and is now canon"** — the precondition is satisfied by that ruling; ground shadows stay an open research item (§ 4.1). (jack-ryan Gate-1 BLOCK of the same date closed by this confirmation.) · R-C3-103 (roles and models, mandatory) · R-C3-109/110 (shadows open; ship the playtest first) · R-C3-113/114/115 (scene references). Rulings live in `astra_test_01/burst/runs/C-3/ledger.json`.
**Companion docs:**
- `canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md` — the lane system description (bursts, wrapper audit, oracles, freeze manifest, SYNC table)
- `canonical/reap-die-rise-game/painted-2d-pipeline/mechanical-process.md` — agent-facing burst recipe + invariants
- `agentic_orchestration/gandalf/notes/2026-09-13-cliffside-scene-hitl-plan.md` — the scene's HITL plan, § OPEN ground shadows, scene-style reference table
- `agentic_orchestration/gandalf/notes/2026-09-13-astra-burst-lane-run-C-3-charter.md` — Run C-3 charter
- `astra_test_01/burst/SPEC.md` § 7 lap 2 (T3g…T3u) — the exporter / tooling contract
- `agentic_orchestration/gandalf/notes/2026-09-14-vfx-style-card-v0.md` — VFX hypothesis (separate lane, § 4.3)
- `reincarnated-godot/web/README.md` — web playtest build + deploy (drax)

---

## 0. TL;DR

- **Painted-2D scene building is THE scene workflow.** A scene is a flat, screen-space painting at a fixed ARPG camera, assembled in Godot 2D as layers (parallax background → painted foreground → y-sorted actors → near-camera occluders → air). Nothing is projected onto 3D. **Synty and 3D scenes are retired from the project plan** (§ 1).
- **Labour split:** ChatGPT (`gpt-6-astra`, HIGH) paints, isolates, checks, packs and builds the tooling; Grok (`image_to_video`) turns character stills into motion clips; gandalf conducts; drax builds the grey room and the Godot/web presentation; Legolas researches; **Matt rules at every checkpoint** (§ 2).
- **The loop:** grey room → walkable → chunk paint → cloud band → parallax → dressing → layered world → JSON manifests → PACK → headless proof → Desktop review → Matt notes → next version (§ 3). The cliffside went v3 → v15 on this loop.
- **Not yet solved:** ground shadows (three methods rejected), Astra-placed reusable assets (deferred to procedural maps), VFX (own lane) (§ 4).
- **Live on the web:** the cliffside is deployed for phones at `https://reincarnated-loadout.vercel.app/playtest` — deploy verified headless (boot, checksum, 200s) and **played on an iPhone by Matt: "exceptionally well" (R-C3-119)** (§ 6).

---

## 1. Scope and ruling

**Ruled (R-C3-102, Matt 2026-09-15):** the painted-2D pipeline that built the cliffside is the official scene-builder workflow (precondition "once the shadows are finalized" satisfied by R-C3-119: shadow layer removed = the canon state). **Crossed off the project plan:** 3D scenes, and Synty as the scene asset source.

**What that retires, and where it is recorded:**

| Retired | Recorded at |
|---|---|
| 3D scene authoring (Synty POLYGON kits assembled in Godot 3D) as the scene path | ledger R-C3-102 · this doc · game tracker SESSION-DELTA 2026-09-15 · decisions-log entry ratified by jack-ryan (engine `20e778a8`, 2026-09-15) |
| The `00-system.md § 1` clause *"the 3D Synty/Godot register (`style-register.md`) still the locked register until X2–X6 evidence"* — for scenes | superseded by R-C3-102; `00-index.md` pointer line |

**Reconciliation owed (partial supersession — reconcile in place, never amputate, `canonical-doc-format § 6.4`):** Synty/3D-register text is still load-bearing-looking in `canonical/reap-die-rise-story/style-register.md` (register lock, sub-fork A), the game tracker (PART A4 king-rig on the Synty map pack; PART B4 Godot/Synty asset binding; PART B1/B2 3D descent floors; PART C ravine carry-forward), `reap-die-rise-game/ensemble-asset-pipeline-spec.md`, `current-to-end-state/pipeline-game.md`, and several engine-spec docs (e.g. `gear-spec-generation-deferred-architecture-2026-06-16.md`, `godot-agent-contract.md`, `performance-target-specs.md`), plus `matt_decision_needed/2026-08-24-vfx-frame-retention-vs-synty-licence.md`. **OPEN — scope:** the ruling names *scenes* and *Synty*; whether it also retires the 3D character/gear mannequin route in the ensemble spec is not stated in the sources and is not assumed here.

**What this doc does not change:** the character matrix method (Run C-3 P1–P6: Astra stills → Grok clips → cycle cut → matte → register), the lane's invariants (`mechanical-process.md § 1`), or the camera grammar below.

---

## 2. Roles and models (Matt R-C3-103 — mandatory)

| Role | Tool + model, exactly | Does |
|---|---|---|
| **ChatGPT — "Astra"** | OpenAI Codex CLI `codex exec`, profile **`astra-burst`** (`~/.codex/astra-burst.config.toml`), model **`gpt-6-astra`**, `model_reasoning_effort = "high"` (always HIGH, Matt 2026-09-11); built-in `image_gen` | **Every GENERATE / CHECK / PACK / TOOLING burst:** grey-room paint-over, chunk outpaint (EDIT mode), cloud texture and cloud-edge repaints, parallax panels, dressing edits, object isolation on flat `#00ff00`, repaints (corners, cathedral swap, burning branch), near-camera assets and props (spire, raven, cow), assembly/seam/matting CHECKs, PACK export runs, and all lane tooling (T3g…T3u). Fresh ephemeral process per burst, workdir outside the repo, wrapper-audited (`00-system.md § S3/§ 5`). |
| **Grok** | **Grok Build CLI 1.0.30** (`~/.grok/bin/grok -p … --always-approve`), tool **`image_to_video`** (xAI Grok Imagine backend). **Exact video model id is not printed by the CLI — pinning it is OPEN** (Legolas findings § 1/§ 5 flag the model as unknown; § 2 prices both candidates, `grok-imagine-video` and `grok-imagine-video-1.5`). | The still → clip step for character motion: one judged rest-frame still → **6 s / 720p / 24 fps clip, 768×1168** (ffprobe `768,1168,24/1,6.04 s,145 frames`), one clip per cell. Consumed by the cycle cutter `oracle/video_cut.py` (T3a/T3g/T3n). Conductor-driven via `runs/C-3/conductor_scripts/grok_clip.sh`; each call ledgered in `grok_calls[]` (C-3: 71 calls, 68 ok). Budget risk on record: **H-C3-1** (402 balance exhausted). Grok is not used by the scene steps in § 3. |
| **Conductor** | gandalf (Claude, RUN-CONDUCTOR) | Charter, briefs (`astra_test_01/burst/briefs/C-3/`), rulings + ledger, conductor glue scripts (`runs/C-3/conductor_scripts/` — assembly, walkable clip, builds, probes; not lane code, not frozen), headless Godot proofs outside the Codex sandbox, Desktop packets, DRIFT-CRITIC eyeball. Writes no production code. |
| **drax** | Godot 4.6.3 + web (owner `reincarnated-godot/`, `reincarnated-loadout/`) | Grey room / blockout guides (orthographic canvas, depth map, ID mask, walkable + parallax extents — v3, v4, v4.1, v4.2), the HTML5 export + touch overlay + Vercel deploy, deploy-truth verification; the VFX atlas viewer. |
| **Legolas** | research (Mode A) | ARPG movement-speed comparison (R-C3-72), VFX oracles + style atlas, video-generation alternatives. |
| **Matt** | ruler | Rules at every checkpoint in § 3; playtests each version and returns notes; rules medium, bar and scope changes. |

**Future step-down goals — recorded as GOALS, not done (R-C3-103):**
- **(a) ChatGPT model: Astra → "Sol"** (Matt's term). **OPEN:** the model id is not pinned; test on one bounded burst (same brief, same gate) before any profile change; the profile row in `00-system.md § 7 SYNC` changes in the same commit.
- **(b) Step down from Grok video generation.** Video generation is the bottleneck (one clip per character × gear tier × direction × motion × ability). Evidence: `agentic_orchestration/legolas/research/2026-09-15-video-generation-alternatives/findings.md` — bake-off shortlist (Seedance 1.5 Pro · Kling v3 Standard · Veo 3.1 Lite; probe ≈ $14.40, cap $20) and **route R1 pose-driven transfer first** (Godot mannequin driving walk → Wan 2.2 Animate Move / Kling 2.6 Motion Control; identical timing and silhouette across gear tiers; first experiment < $2). Not commissioned as a run; Matt gate — and R1's mannequin is exactly what the open decision `canonical/matt_decision_needed/2026-09-15-does-the-3d-retirement-cover-the-character-mannequin-route.md` rules on.

---

## 3. The workflow (one scene, one loop)

**Fixed grammar for every step:** camera = the ratified GD `player_lock` angles (yaw 47°, pitch 52.95°), Keeper at **12.5 %** of 1080p screen height = **130 px** (R-C3-42/44); all art is painted on an **orthographic canvas** at that yaw/pitch (the cliffside canvas is 5376×4096) — a perspective camera cannot align with flat paintings (R-C3-43). Style anchor = the approved chunk (`runs/C-3/artifacts/CS-chunk-A/chunk_A.png`) passed as IMAGE 2 in every paint brief. Every image burst: one call, one diagnosed retry, re-drive as `-r1` (R-C3-55). **No conductor writes under `burst/` while a TOOLING burst runs; TOOLING is serial** (R-C3-65).

| # | Step | Who / burst type | Brief pattern (example) | Accepting gate | Human checkpoint |
|---|---|---|---|---|---|
| 1 | **Grey room (v4.1 organic)** | drax | flat-shaded guide: olive = grass/rock top, tan = dirt path, light grey = rim verge, dark grey = faces, brown = bridge, magenta = loose plank, `#00ff00` = void; depth map uint16 mm; ID mask | organic rules (R-C3-54/55): one continuous landmass, no area ending in high cliff beside ground below, no straight run > ~2 m, no right angles; faces to 20 m (R-C3-48); **no props in the ground** — boulders are sprites (R-C3-56) | **Matt sees the grey room before any painting** (R-C3-55a) |
| 2 | **Walkable / collision** | conductor glue (`conv_walkable_v4.py`, `clip_walkable.py`) | — | walkable = all flat tops with a 0.5 m rim margin + bridge deck (R-C3-57); clipped 24 px inside the canvas so Godot keeps the wall polygons (R-C3-58); headless edge-escape probes (`probe_move.gd`) | — |
| 3 | **Chunk paint** | Astra GENERATE, EDIT mode | `CS-v4-<row>_<col>`: canvas = painted neighbour strips (256 px) + guide elsewhere; *"painted strips stay; every guide area replaced by painting that continues them seamlessly"* | 1536×1024 chunks, 256-px overlaps, painted in dependency waves (`autopaint_v4.py` / `grid_paint_v4.py`); minimum-error seam cut (DP ±1 px, feather ±3) — **outpaint, never prompt-only strips** (R-C3-45/46/47: 31.3 → 1.8–3.0 /255); mask IoU vs guide (v4 ≥ 0.982); **plus conductor eyeball of every join band** — the DP metric is blind to a join at a strip's inner edge (R-C3-54) | Matt on the painted assembly (R-C3-54 notes → v4) |
| 4 | **Cloud band** (transparent undersides) | Astra GENERATE (`CS-cloudtex-a/b`, `CS-edge-*`) + CHECK (`CS-asm-fg-v4-band3`, `…-band5`) | band3: Astra paints a tileable sunset cumulus texture; assembly fills a depth-map band (cloud top ≈ 11 m below rim ± noise, 100–260 px into the void), opaque inside. band5: Astra repaints canyon-facing edges over pure black; wisps recovered by known-background matting | 0 see-through deep face, 0 exposed underside, rock/top untouched (M-C3-CLOUD-BAND, M-C3-CLOUD-EDGES). **Rejected on record:** linear depth fade, baked fog, per-chunk mist, procedural puffs (band4), tile haze fix (band6) — R-C3-59/60/63/66/69/76/82 | Matt: "clouds perfect" (R-C3-80) |
| 5 | **Parallax layers** | Astra GENERATE (`L-sky-*`, `L-far_ruins-*`, `L-forest_valley-*`, `L-mist-*`) + TOOLING **T3k** | native-scale panels per layer (R-C3-46(3)); horizon-silhouette bands (green only above the silhouette) + mist on black (R-C3-49) | scroll 0.12 / 0.25 / 0.45 / 0.70, positions tuned by simulated follow views for a **reveal-by-walking** story beat (R-C3-51, `sim_view.py`); camera limits shifted by the anchor offset because Camera2D applies offset after limits (R-C3-53); in-engine render matches the simulation; AI-tell check on repeated landmarks (duplicate temple → cathedral, R-C3-70/72/82) | Matt on story + style (plan checkpoint 2) |
| 6 | **Dressing pass** | Astra GENERATE EDIT (`CS-dress-<zone>`) → isolation (`CS-objsheets-*`, `CS-objiso-*`) → CHECK catalogue (`CS-assets-<zone>`) | **dress-then-isolate:** Astra dresses the bare crop with IMAGE 2 = Keeper scale figures at true size and IMAGE 3 = **camera-projected size chart**; then the AFTER object crops go 2× onto green sheets and an EDIT replaces all ground/grass/shadow with flat `#00ff00`, objects unchanged; cut back, downscale, key; placement = the diff bbox (registration by construction) | diff-only extraction failed its gate 7/7 (R-C3-64) → isolation is the method; every object catalogued as a **reusable asset** (kind, px size, footprint, sort line, light upper-left, register, states, provenance — R-C3-62); **size rule:** ±25 % against the *projected* bbox of the object's nominal metric size, never against Keeper height (60.62 px/m vertical, 80.31 px/m ground depth — R-C3-68(5), corrected R-C3-73) | Matt playtest of the dressed version (R-C3-75/79) |
| 7 | **Layered world** | TOOLING T3l, T3m, T3o, T3p, T3q, T3r (frozen) | — | **z-order** foreground tiles < `Shadows` z1 < `Actors` z2 (y-sort: Keeper + props) < `Overhead` z3 < near `Parallax2D` z4 (scroll > 1) < `Air` z5 (T3l, R-C3-71). **T3m** pixel-accurate fade (Keeper frame alpha vs prop alpha) + mask-derived rect footprints (R-C3-75/78). **T3p** near `fade:false`; near objects are **edge-anchored** so their cut end is never on screen (R-C3-87/89). **T3q** glows/particles `z_parent: 'near:<i>'` (R-C3-95/96). **T3r** fly swarms (R-C3-97/100). **T3o** additive flicker glows on ember cracks + extended particle keys + Tab VFX picker (R-C3-81/83/86) | — |
| 8 | **Props / near / glows / particles JSON** | conductor glue (`build_v11.py`, `build_v14.py`) | `props.json` (assets, instances, shadows, overhead, near, particles, glows, swarms) + `parallax.json` (layers, camera, `movement`) | exporter validation rejects unknown keys, missing files, NaN, near scroll ≤ 1 before writing anything (T3l); orphan glows/emitters dropped by sprite ownership (R-C3-105) | — |
| 9 | **PACK export** | Astra PACK (`CS-pack-v<N>`, `CS-pack-web2`) | runs once: `python3 -B -m export.godot_import --cells <cells> --out OUT/godot --parallax <dir> --props <dir> --vfx-kits <kits.json> --sockets <sockets.json>`; no `--scene/--vfx/--gear-variant`; **do not run Godot** | exporter JSON stdout pasted verbatim to `out/exporter.json`; frozen exporter (MANIFEST) | — |
| 10 | **Headless proof** | conductor, outside the sandbox | Godot 4.6.3 `--import`, `probe_cliff.gd` (teleport to sample positions, capture), `probe_move.gd` (walk / edge / collision); the touched test modules run outside the sandbox | clean import; zero ERROR/SCRIPT lines; probes land; measured speeds / fade / coverage match the manifest (e.g. M-C3-V6-PLAYABLE: fade 1.0 → 0.35 at contact, walk 247.0 / run 494.0 px/s) | — |
| 11 | **Desktop review** | conductor | `~/Desktop/Astra Burst Review - <date>/<NN> <TITLE> (open godot - project.godot)` | folder opens and runs | **Matt plays it** |
| 12 | **Matt notes → next version** | Matt → conductor | notes ledgered verbatim as a `matt` ruling; dispositions `veto_open` | the next version fixes exactly the named notes; rejected attempts stay as lineage, never assembled | loop to step 1, 3, 6 or 7 as the note requires |

**Movement (by reference):** run = Grim Dawn base run **3.8 body-heights/s → 494 px/s**; walk = **50 % → 247 px/s**; anim fps run 14.5 / walk 20.7 against foot slide (R-C3-77); applied through the T3l `movement` block. **One-stride re-cut rule:** walk/run cells must measure 2 steps per loop; double-stride cuts are re-cut with the forced period (T3n `--period-frames`, `oracle/steps_per_loop.py`) — R-C3-80/86.

---

## 4. What the workflow does NOT yet solve

### 4.1 Ground shadows — OPEN (R-C3-109)
Three attempts rejected by Matt: v9 extracted painted shadow sprites (edit-drift blotches read as ash, R-C3-97); v10 synthetic per-prop contact ellipses (R-C3-101: "no good"); v11/v13 extracted shadows boosted ×1.6 and masked to prop vicinity (R-C3-109: "no good"). **v14 ships with no shadow layer at all** (the cow's contact shadow removed too — ledger note 2026-09-15). The `Shadows` z1 node remains in the exporter, empty.
Candidate methods, none tried: **(a)** Astra paints shadows into the picture (dressed chunks and isolated objects carry their cast shadow as paint, or a final shadow-only repaint over the assembled scene); **(b)** a grey-room shadow layer authored before painting so the paint carries it natively, then runtime light augmentation (particles / 2D lighting). Others noted in the plan § OPEN (2D light occluders, normal maps from paint, per-object shadow sprites in register).
**Gate to re-open:** a method note + one A/B chunk.

### 4.2 Reusable-asset placement by Astra — DEFERRED (R-C3-62)
The catalogue exists (`runs/C-3/artifacts/CS-assets-*`, merged in `CS-props-v*`). Not tested: give Astra the asset base and ask it to place props on a new bare painted map, compared with Astra-composed clutter. **Gate:** procedural maps begin.

### 4.3 VFX — separate lane
The scene workflow ships a **placeholder** cast only. The Gigapack / CreativeKind library look is rejected (R-C3-88). The VFX lane: style card `agentic_orchestration/gandalf/notes/2026-09-14-vfx-style-card-v0.md` (v0 + v0.1), tooling T3s oracle measurer / T3t effect-kit builder / T3u tint ramp (R-C3-104/111), Frozen Orb kit v2 (R-C3-112), the **six-kit breadth test** (R-C3-98/99). **Gate:** the breadth test corrects the style card; the web build then re-exports with the bake-off kits (R-C3-110). **Result (R-C3-123, Matt):** the six-kit breadth test is closed as a *tooling + register* proof (sheet → kit → picker → web, six times; style card v0.2 corrections landed), **not** as a skill-fidelity result — all six are one projectile grammar, there are no targets/targeting, and the effects are too small; the VFX session (hand-off `agentic_orchestration/skill_handoff_2026-09-15.md` § 4) starts with placeholder monster dummies + targeting, then size/timing estimation by video, then per-skill grammars, then sheets. The hybrid-oracle ruling is deferred to that session.

### 4.4 Also open from the sources
Breakables/interactives (boxes, vines, the falling bridge plank) — plan checkpoint 5, not built. Mobile memory and texture limits (§ 6). Scene-register fold into `style-register.md` (§ 5).

---

## 5. Scene-style references (R-C3-113 / 114 / 115)

| Reference | Use | Never |
|---|---|---|
| **Diablo 2** | scene weight and darkness; density of things; pre-rendered-isometric lineage | — |
| **Bastion** (Supergiant, 2011) | the **painted-scene pole**: hand-painted 2D isometric world, storybook clarity, warm saturated palette, bold chunky silhouettes, detail legible on a simple value structure; may be used as a scene style anchor phrase in briefs (style, never assets). Devices noted for later: the world assembling underfoot (procedural maps), the narrator across time | as an asset source |
| **Secret of Evermore** | the *feel*: displaced-kid wonder and unease, journey through eras, magic as gathered craft | a visual register |
| **Earthbound** | **THEME ONLY** — the teenager-into-the-future story comparison | **any** visual, palette, UI or VFX reference in any brief, register card or style anchor (Matt, explicit) |
| Chronicon · Children of Morta · The Slormancer · CrossCode | **VFX** references under measurement (Legolas) — not scene references | scene briefs |

Scene register in force for the cliffside: H1 line register with Hades-flavoured environment (saturated jewel tones, bold graphic shadows, exaggerated shapes), Keeper sprite unchanged (R-C3-42). **Owed:** fold this table into `canonical/reap-die-rise-story/style-register.md` (story-side; not written by this doc).

---

## 6. Delivery surfaces

**Desktop review folder (every version):** `~/Desktop/Astra Burst Review - <date>/<NN> <TITLE> (open <entry>)` — numbered in sequence across the run (cliffside: 70 blockout … 82 v15), the title names what changed, the parenthesis names the file to open. Checkpoint packets (renders, proofs) use the same convention.

**Vercel mobile playtest — LIVE (M-C3-web-playtest):** `https://reincarnated-loadout.vercel.app/playtest` (landing) → `/playtest/cliffside/`. Build: shadow-free `CS-pack-web2`, Frozen Orb only, GL Compatibility, threads off, touch overlay (left joystick, run past 60 %; CAST / JUMP / VFX), large textures as lossy WebP (.pck 34.8 MB, ~45 MB download); deploy-truth verified by drax (200s, wasm mime, pck checksum, headless boot 5.9 s, joystick + CAST).
- **Build script:** `reincarnated-godot/web/build_playtest.sh <SOURCE>/out/godot <route>`; deploy = commit `public/playtest` in `reincarnated-loadout` and push `main` (push needs Matt authorization) — `reincarnated-godot/web/README.md`.
- **License rule:** only self-authored VFX kits ship publicly. The overlay's license fence fails the build if library packs (`vfx_frost/fire/lightning/arcane/holy/poison`, CreativeKind, Gigapack) are present and greps the exported `.pck`; public builds use `kits_web.json`.
- **Known caveats (drax):** iOS decoded-texture memory ~700 MB (416 Keeper frames at 512²); `mist.png` 4340 px exceeds some older Android GPUs' 4096 limit; fixed 16:9. Real-phone test DONE: Matt, iPhone, "played exceptionally well" (R-C3-119; to-do closed). Older-device memory and the Android 4096-px caveat remain untested.

---

## 7. Provenance and evidence

- **Rulings:** `astra_test_01/burst/runs/C-3/ledger.json` R-C3-42 … R-C3-115 — scene build 42–101 (with 105, 109); exporter tooling acceptances 49, 71, 78, 86, 89, 96, 100, 104, 111; movement 72, 77, 80, 86; VFX 81, 88, 90–92, 98, 99, 106–108, 112; delivery 102, 103, 110; references 113–115. Halts H-C3-1 (Grok 402 balance exhausted), H-C3-2 (jack-ryan Gate-2 BLOCK on the R-C3-9 halt re-scope).
- **Milestones:** M-C3-CLIFF-PLAYABLE (first playable, `runs/C-3/cliffside_final/`) · M-C3-CLOUD-BAND · M-C3-CLOUD-EDGES · M-C3-LAYERED-PLAYABLE · M-C3-V6…V10-PLAYABLE · M-C3-T3st · **M-C3-web-playtest**.
- **Artifacts:** briefs `astra_test_01/burst/briefs/C-3/CS-*` (dress / objsheets / objiso / assets / near / near2 / corner / prop / v4 chunks / cloudtex / edge / asm / pack) and `T3g…T3u`; guides `runs/C-3/artifacts/CS-guides-v4/`; glue `runs/C-3/conductor_scripts/` (see its `README.txt`); exports `runs/C-3/cliffside_*`.
- **Freeze:** `astra_test_01/burst/MANIFEST.sha256` sha256[:12] **`9543d3842e2b`** (== `00-system.md § 7` SYNC row). Tooling freezes along the way are ledgered per burst (e.g. T3r `df80ca44c500`).
- **Commit range (collaboration repo):** `e4cb6e37` (R-C3-42, cliffside opened) … `eae5790f` (playtest LIVE). Loadout `ef5e544` / `c84352e` (pushed); godot `60c1063` / `8b260b1` (local only, per the milestone).

## 8. Cross-references

Router `canonical/00-ground-state.md` · game index `canonical/reap-die-rise-game/00-index.md` · lane `painted-2d-pipeline/00-system.md` + `mechanical-process.md` · game tracker `canonical/current-to-end-state/current-to-end-state-game.md` (SESSION-DELTA 2026-09-15) · register `canonical/reap-die-rise-story/style-register.md` (fold owed) · Matt to-do `canonical/matt_to_do/2026-09-15-phone-playtest-cliffside.md` · research `agentic_orchestration/legolas/research/2026-09-15-video-generation-alternatives/findings.md`.

Tracker-delta: game tracker SESSION-DELTA 2026-09-15 — closed: painted-2D scene workflow canonized, 3D scenes / Synty crossed off the plan, web playtest live; new gaps: ground shadows (§ 4.1), Synty/3D-register reconciliation across PART A4/B1/B2/B4/C + style-register + ensemble spec (§ 1), Sol model pin + Grok video model pin + video step-down (§ 2).

---

**Signed:** gandalf (CANON-STEWARD / SPEC-AUTHOR)
**For:** the canonical scene-builder workflow — who does what with which model, each step's gate and checkpoint, and what is still open — so the next scene is built the way the cliffside was, not reinvented.
