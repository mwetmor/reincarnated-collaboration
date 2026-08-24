# Metal VFX Smoke Probe — findings (charter P0-b)

**Author:** drax · **Date:** 2026-08-23 (session closed 2026-08-24) · **Status:** COMPLETE — full table, no partial rows
**Dispatch:** `agentic_orchestration/dispatches/2026-08-23-drax-metal-vfx-smoke-probe.md` (Gate-1 PASS-WITH-CHANGES)
**Brief (governs):** `agentic_orchestration/gandalf/notes/2026-08-23-metal-vfx-smoke-probe-brief.md`
**Charter:** `agentic_orchestration/gandalf/notes/2026-08-23-vfx-archetype-binding-charter.md` (§4 P0-b, §5, L-1..L-13)
**Governing ruling:** R-1(a) — Mac Metal is renderer of record for the prototype era.
**Consumer:** gandalf at **P4** (T-A emitter/constraint notes) + the R-1 empirical track.

`Round-trip: not applicable — no cross-seam contract change in this dispatch.`

---

## 0 · The two questions, answered directly

> **Q1 — Feature integrity: does the Metal renderer fail or visibly degrade any effect class we own?**
>
> **NO. Zero M-FEAT results across 13 probes covering 8 GPU feature classes.**
> Every effect rendered, every ffprobe gate passed, and on the four cross-checked
> suspects **Metal and MoltenVK produced output that is identical on all 90 frames
> at the house lit-pixel bar (LIT ≥ 12): worst-frame delta = 0 px, four for four** —
> including both compute-shader paths (GPUParticles collision, GPUParticles attractor),
> which are the two places a Metal backend was most plausibly going to diverge.
> There is no Metal feature failure to report and none was manufactured.

> **Q2 — Throughput: would a VFX bake-off cadence bottleneck on this machine?**
>
> **Measured, not adjectivised.** One 90-frame (3.0 s) 1920×1080 lossless capture,
> encode-ready, warm, including full process launch:
> **min 5.47 s · median 6.72 s · max 10.09 s** →
> **357 – 658 renders/hour, median 535 renders/hour.**
> **Cold-start (shader-cache wiped) costs Metal a median of 17 ms** — inside noise.
> (The same cold arm costs MoltenVK **+960 to +3,974 ms**. See § 6.)
> **Limb 2 of the revisit-trigger is NOT-ARMED-by-default** — I do not own the
> "bake-off-hostile" threshold and did not invent one. § 8 carries a labelled *proposal*.

**Revisit-trigger: NEITHER LIMB ARMED. The cross-host (PC/Vulkan) question does not reopen on this evidence.**
No HALT condition was hit.

---

## 1 · Selection rationale table (math-before-code, Discipline #1)

Deliberately worst-case, **not** a fair sample — the brief is explicit about this.
Chosen for GPU-feature diversity, then for weight within each class.

| id | asset | pack / vendor | GPU feature class under stress | why this one |
|---|---|---|---|---|
| `p_turb` | `NovaLightningWave.tscn` | PolygonArsenal / **Synty** | GPUParticles **turbulence** ×3 + trail ×3 + **RibbonTrailMesh** ×6 | heaviest single asset in the pack (155 particles / 6 emitters) |
| `p_trail` | `Stun.tscn` | PolygonArsenal / **Synty** | **RibbonTrailMesh** isolated (4 ribbons, 24 particles) | trail mesh with minimum confound |
| `p_slam` | `GroundSlamRed.tscn` | PolygonArsenal / **Synty** | turbulence ×2 + trail + **ground-plane decal quads** (depth interaction) | 128 particles landing on the floor plane |
| `p_spike` | `GroundSpikes.tscn` | PolygonArsenal / **Synty** | **mesh draw-pass** particles (non-billboard) + turbulence | 141 particles / 6 emitters, the non-billboard arm |
| `p_flame` | `FlamethrowerSprayBlue.tscn` | PolygonArsenal / **Synty** | **sustained** alpha overdraw (continuous, not a burst) | steady-state cost, not a one-shot spike |
| `b_beam` | `beam_vfx_01.tscn` | BinbunVFX assets-5 / **Binbun** | **beam / shader-driven**: 5 bespoke `.gdshader` + 2 emitters | the shader-COMPILE surface |
| `b_fire` | `fire_01.tscn` | BinbunVFX assets-19 / **Binbun** | **sub-emitter** + **TubeTrailMesh** + additive stacking | the only sub-emitter + tube-trail asset family we own |
| `b_smoke` | `smoke_big_vfx_01.tscn` | BinbunVFX assets-6 / **Binbun** | **alpha-blend stacking** + **proximity_fade** (soft-particle depth fade) | largest soft-alpha screen coverage |
| `b_expl` | `vfx_explosion_01.tscn` | BinbunVFX assets-21 / **Binbun** | 6 bespoke shaders — **proximity_fade + additive stacking in one asset** | peak overdraw: 46.4 % of screen |
| `b_poison` | `poison_cloud_vfx_01.tscn` | BinbunVFX assets-18 / **Binbun** | large soft alpha volume, depth fade at max coverage | second soft-volume sample, different pack |
| `s_fire` | `FX_Fire_Large_01.tscn` | Particle_FX / **Synty** | flipbook / particle-anim + additive | the **Synty-authored** particle sample (lineage arm) |
| `x_coll` | *constructed* | **none (no vendor pixels)** | **GPUParticles COLLISION** (`COLLISION_RIGID` + `GPUParticlesCollisionBox3D`) | **owned-pack coverage gap — see § 2** |
| `x_attr` | *constructed* | **none (no vendor pixels)** | **GPUParticles ATTRACTOR** (`GPUParticlesAttractorSphere3D`) | **owned-pack coverage gap — see § 2** |
| `x_none` | *constructed* | **none** | CONTROL — empty stage | the reference every coverage number is measured against |

### 2 · Coverage gaps — named, not silently dropped

Grep of every owned pack (`BinbunVFX/` all 12 categories, `PolygonArsenal/` 60 effects,
`Particle_FX/`, `brackeys_vfx_bundle/`, `Synty/particle-fx-shapes`, `ThirdParty/rpicster-vfx-textures`):

| feature class | assets in owned packs that use it | disposition |
|---|---|---|
| GPUParticles **collision** (`collision_mode`, `GPUParticlesCollision*`) | **0** | **COVERAGE GAP** — covered by constructed probe `x_coll` |
| GPUParticles **attractor** (`GPUParticlesAttractor*`) | **0** | **COVERAGE GAP** — covered by constructed probe `x_attr` |
| turbulence | 28 (all PolygonArsenal) | covered by `p_turb` / `p_slam` / `p_spike` |
| trail / RibbonTrailMesh | 26 / 12 (all PolygonArsenal) | covered by `p_turb` / `p_trail` |
| TubeTrailMesh | 6 (all Binbun fire) | covered by `b_fire` |
| sub-emitter | 15 (all Binbun fire) | covered by `b_fire` |
| `proximity_fade` (soft-particle depth fade) | 366 (Binbun-wide) | covered by `b_smoke` / `b_expl` / `b_poison` |
| blend mode / additive stacking | 271 Binbun + 31 Arsenal | covered by `b_fire` / `b_expl` / `s_fire` |

**The two gaps are a finding about our CONTENT, not about Metal.** Nothing we own exercises
particle collision or attractors. Both were constructed from scratch and both work on Metal
**and** are pixel-identical on MoltenVK. Carried to § 7 as a T-A constraint note.

---

## 3 · Method

- **Stage:** neutral dark floor (albedo 0.085), one directional key, filmic tonemap,
  glow at the standing `glow_hdr_threshold = 1.25` (Matt ruling 2026-06-22).
  **No king · no ambient dust · no HUD · zero contact with any SB-1 surface.**
- **One parameterised probe stage, one effect per RUN.** *Documented deviation:* the
  dispatch says "one probe scene per effect". A single code-built stage is a deliberate
  **strengthening** of that isolation — every effect is photographed against literally the
  same pixels (verified: the `x_none` control is byte-stable), so any difference between
  two rows is the effect and never the stage. Nothing about it is alignment-shaped.
- **Mounting style (load-bearing, § 5):** every emitter is instanced in `_ready()` —
  it **exists before frame 0 and nothing spawns mid-clip**. This is the opposite arm from
  BR-2 cell 5's runtime-spawned impact/cast VFX, which is what makes the two cases separable.
- **Clip:** 90 frames @ 30 fps = **3.00 s**, 1920×1080. Justified: covers windup/active/impact
  for every asset in the set (measured — see the coverage windows in § 4); the shortest length
  that still shows `p_flame` and `b_smoke` reach steady state.
- **Renders:** `--rendering-driver metal`, Movie Maker PNG sequence → ffmpeg h264.
  Headless never used (repo law). **Blind CLI used under the `CLAUDE.md:67-71` carve-out,
  pre-authorised by the dispatch** — no editor, no MCP, no halt; nothing here needed aligning.
- **Cold/warm:** run 1 wipes `.godot/shader_cache`, run 2 is hot. Exactly one cold and one
  warm, no third. The same pair doubles as the determinism ×2 pair.
- **On-frame evidence:** every effect is differenced per frame against the `x_none`
  empty-stage control at sa_gate.py's exact bar. "Rendered nothing", "rendered briefly"
  and "rendered throughout" are therefore distinguishable from numbers, not from vibes.

**Instrument (new, not a modification of any existing `run_*.sh` — U-7(b) upheld):**
- `~/Games/reincarnated-godot/scripts/run_vfx_metal_probe.sh`
- `~/Games/reincarnated-godot/scripts/vfx_metal_probe.gd`
- `~/Games/reincarnated-godot/scenes/vfx_metal_probe.tscn`
- `~/Games/reincarnated-godot/scripts/vfx_probe_delta.py`

`vfx_probe_delta.py` **reproduces** `scripts/sa_gate.py`'s bar (`LIT = 12`, `MIN_PX = 40`,
lines 51-52) so the numbers are commensurable, and **reports where sa_gate refuses** —
which is exactly the reclassification the dispatch ordered. `sa_gate.py` itself was
**not modified and not called**: its `SA_REPEAT` path is welded to the SLASH-ARC
trace/ghost/control arm structure this probe does not have, and it raises `SystemExit`
at the bar rather than reporting.

---

## 4 · The per-effect table

All rows: driver Metal 3.2, Apple M2 (Apple8), Godot 4.6.3, 1920×1080, 90 frames, free-seed arm.

| id | cold ms | warm ms | load ms | render span ms | render fps | on-frame | peak px (% screen) | peak frame | window | determinism (free seed) | anomaly class |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `p_turb` | 5588 | 5571 | 20 | 4970 | 18.11 | 16/90 | 91,420 (4.41 %) | 0 | 0..15 | differs; worst 3,270 px | **NONE** |
| `p_trail` | 5487 | 5471 | 8 | 4887 | 18.42 | 80/90 | 535 (0.03 %) | 34 | 10..89 | differs; worst 861 px | **NONE** (see § 4.1) |
| `p_slam` | 5649 | 5614 | 25 | 5002 | 17.99 | 36/90 | 82,341 (3.97 %) | 7 | 0..35 | differs; worst 30,695 px | **NONE** |
| `p_spike` | 6001 | 5898 | 17 | 5271 | 17.07 | 90/90 | 87,431 (4.22 %) | 9 | 0..89 | differs; worst 11,354 px | **NONE** |
| `p_flame` | 6775 | 6723 | 12 | 6106 | 14.74 | 90/90 | 70,067 (3.38 %) | 33 | 0..89 | differs; worst 26,948 px | **NONE** |
| `b_beam` | 8790 | 8792 | 20 | 8125 | 11.08 | 90/90 | 190,675 (9.20 %) | 66 | 0..89 | differs; worst 14,227 px | **SCENE** (fixed) + **ASSET** |
| `b_fire` | 6435 | 6203 | 22 | 5397 | 16.68 | 90/90 | 35,566 (1.72 %) | 86 | 0..89 | differs; worst 25,578 px | **NONE** |
| `b_smoke` | 8971 | 9240 | 15 | 8423 | 10.69 | 89/90 | 304,743 (14.70 %) | 69 | 1..89 | differs; worst 138,077 px | **ASSET** + **NONDET** (§ 5.3) |
| `b_expl` | 10022 | 10086 | 39 | 9086 | 9.91 | 77/90 | 961,343 (46.36 %) | 41 | 0..89 | differs; worst 476,176 px | **NONE** |
| `b_poison` | 9708 | 9247 | 17 | 8309 | 10.83 | 90/90 | 192,215 (9.27 %) | 54 | 0..89 | differs; worst 151,782 px | **NONE** |
| `s_fire` | 6521 | 6415 | 15 | 5806 | 15.50 | 90/90 | 69,971 (3.37 %) | 82 | 0..89 | differs; worst 23,515 px | **NONE** |
| `x_coll` | 7050 | 7096 | 4 | 6450 | 13.95 | 90/90 | 288,414 (13.91 %) | 86 | 0..89 | differs; worst 354,687 px | **NONE** |
| `x_attr` | 7188 | 7595 | 4 | 6959 | 12.93 | 90/90 | 1,389,597 (67.01 %) | 89 | 0..89 | differs; worst 796,145 px | **SCENE** (fixed) |

**ffprobe HARD gates: 13/13 PASS** — `h264 · 1920×1080 · nb_frames 90 · 30/1 · duration 3.000000`, every row.
(No gate failure anywhere in the run; these gates stayed hard as the dispatch required.)

### 4.1 · Eye-verification — the exact frames I looked at

Every anomaly row and every headline claim names the frame it rests on.
Stills retained in the capture set as `<id>_metal_free_still_<frame>.png`.

| what I read | frames eye-read | what I saw |
|---|---|---|
| `p_turb` "renders nothing?" | **0002**, 0020 | Frame 0002: full white nova flash + sparks. Frame 0020: empty. **Not a failure — a 16-frame one-shot burst that completes by frame 15.** The coverage window (0..15) confirms it numerically. |
| `p_trail` ribbon trail | **0020** | 4 tiny sparkle particles + a yellow ribbon fragment. Renders correctly but at 0.03 % of screen it is **too small to be strong evidence for the trail class** — the trail verdict rests on `p_turb` (6 ribbons) instead. Selection weakness, recorded. |
| `b_beam` beam shader | **0045** (before fix), **0045** (after fix) | Before: a blob at origin — I was photographing the beam **end-on** (it is authored along −Z and the fixed camera looks down that axis). After a 90° yaw: full beam with core, outer glow, travelling particles and both end flares, correct. **SCENE class — fixed, re-rendered, not reported as Metal.** |
| `b_smoke` soft particles | **0045**, **0088** | Smoke column renders with correct soft depth fade against the floor. **A hard black shadow blob sits on the floor beside it** (see § 7 ASSET note). |
| `x_coll` particle collision | **0045** | Particles visibly **bouncing off** the mid-air slab and pooling on it, and off the floor box. Collision demonstrably functioning on Metal. |
| `x_attr` attractor | **0045** (before), **0080** (after) | Before: blown to flat white at 0.85 alpha — could not read the shape. After alpha 0.55 / 900 particles: coherent clump gathered on the attractor. **SCENE class — fixed, re-rendered.** |
| Metal vs MoltenVK, `b_smoke` | **f88 pair + diff map** | `XCHECK_b_smoke_metal_f88.png` / `XCHECK_b_smoke_vulkan_f88.png` / `XCHECK_b_smoke_diffmap_f88.png`. Same shape, same brightness, same shadow, same silhouette — only a small phase offset in the turbulence noise. **No missing particles, no wrong blend, no broken shader, no colour shift.** |

---

## 5 · METHOD NOTE — determinism was MEASURED, not GATED

> **⚑ This section is the item the dispatch flagged for gandalf's ratification at P4.
> It is a method note, not a brief amendment. Ratify it as a decision, not an oversight.**

### 5.1 · What was changed and why

The brief (§ 3) asks for the house evidence chain including **SHA-256 determinism ×2** as a
hard gate. My own `AGENT_STATE.md` 2026-08-01 BR-2 cell-5 entry records that the renderer is
**not** byte-deterministic across processes once runtime-spawned VFX are in frame (2,305 lit px,
58× the 40 px bar, surviving `--nodust --noambient --nohud`).

**This probe's entire subject matter is VFX.** A hard SHA-256 gate would therefore have tripped
on all 13 rows for reasons having nothing to do with Metal, and would have injected a false
"Metal is broken" signal into the R-1(a) empirical track at its source.

**Per the dispatch:** the ×2 render and the SHA-256 comparison were kept; a **mismatch is
recorded as a MEASURED DATUM** (quantified in lit px at sa_gate.py's exact bar), **not** as a
failure and **not** as an anomaly. **ffprobe gates stayed hard** and all 13 passed.

### 5.2 · The side-benefit, harvested — and it is the biggest finding in this run

My probe scenes are the cleanest isolation of the free-running GPUParticles term the project
has ever had. So I ran a **second arm** on all 13 effects: identical in every respect except
that `use_fixed_seed = true` is set on every `GPUParticles3D` in the mounted tree.
(This **bounds** the term. It does **not** fix it, and no game surface was touched —
the dispatch's "measure it, bound it, do not chase it" is respected.)

**Result — free seed vs pinned seed, 13 effects, Metal:**

| arm | byte-identical ×2 | worst-frame lit-px |
|---|---|---|
| free seed (as the assets ship) | **0 / 13** | 861 – 796,145 px |
| **`use_fixed_seed` pinned** | **13 / 13** | **0 px, every row** |

**Every single effect went byte-identical across processes.** That is a reportable finding of
the kind the dispatch pre-registered, and it bounds BR-2 cell 5 hard:

1. **The Metal renderer is byte-deterministic across processes.** It is not the source of
   BR-2's drift. Nothing in the renderer needed to change to get 13/13 byte-identical output.
2. **The dominant BR-2 term is the `GPUParticles3D` per-launch RNG seed** — a single named,
   pinnable property (the term `AGENT_STATE.md:3547` already carries as "peelable with `--nofx`").
   BR-2's unproven hypothesis was *load-seeded vs runtime-instanced*; the mechanism is narrower
   and more actionable than that — it is the emitter seed itself.
3. **Mounting-style separability:** every probe scene used the **scene-preloaded** arm
   (instanced in `_ready()`, present before frame 0, nothing spawning mid-clip). This arm
   still produced 0/13 byte-identical on free seed — so **"runtime instancing" is NOT a
   necessary condition** for the drift. The seed is sufficient on its own to explain it.

### 5.3 · The honest residual — do not over-read § 5.2

I re-ran `b_smoke` under pinned seeds **four times** on Metal. **Three of four processes were
byte-identical to each other** (sha `0dd48601…`); **one diverged** from frame ~75 onward, up to
**165,841 lit px** at frame 88.

So the correct claim is: **seed-pinning collapses the dominant term and yields byte-identical
output in the large majority of runs, but a rare intermittent residual survives on at least one
effect.** It is *not* a complete determinism fix, and I am not claiming it is.

The residual is **not a Metal signal**, on two independent grounds:
- It is **visually equivalent** — eye-read at frame 88 (§ 4.1): same shape, brightness, shadow,
  silhouette; only turbulence phase differs.
- **MoltenVK shows it too** (`b_expl` vulkan pinned arm: 60 px cold-vs-warm), and MoltenVK's
  `b_smoke` output matches the **Metal majority cluster exactly** (0 px over all 90 frames).
  The dispatch's NONDET→M-FEAT promotion condition ("MoltenVK byte-stable where Metal is not,
  same scene") **does not fire**: Metal *is* byte-stable, and both drivers show the same residual class.

**Recommendation to P4 (not a decision I own):** any future pixel gate on a VFX-bearing clip
should pin `use_fixed_seed` rather than assume determinism or route around it. That converts
`sa_gate.py`'s standing refusal from a wall into a measurable arm. Chasing the last residual is
a separate, later question and I have not opened it.

---

## 6 · MoltenVK cross-check — the pre-flight, and the result

**Pre-flight (done FIRST, before any scene was authored, exactly as the dispatch ordered):**
`--rendering-driver vulkan` → **`Vulkan 1.2.283 - Forward+ - Using Device #0: Apple - Apple M2`**.
**MoltenVK is available on this machine.** The M-FEAT refuting test was proven live while it was
still cheap; no M-FEAT claim in this note is a rubber stamp. (Metal baseline for comparison:
`Metal 3.2 - Forward+ - Using Device #0: Apple - Apple M2 (Apple8)`.)

**Suspects cross-checked: 4 (at the cap, not over it).** Chosen as the two highest-risk feature
classes plus the two heaviest overdraw assets. Both drivers rendered under **pinned seeds**, so the
comparison is a genuine cross-driver pixel test rather than a comparison of two random draws.

| effect | why cross-checked | Metal vs MoltenVK, **all 90 frames** | verdict |
|---|---|---|---|
| `x_coll` | GPUParticles collision — **compute-shader path**, likeliest divergence | **0 px** | identical |
| `x_attr` | GPUParticles attractor — **compute-shader path** | **0 px** | identical |
| `b_expl` | peak overdraw (46.4 % screen), 6 bespoke shaders, additive + depth fade | **0 px** | identical |
| `b_smoke` | largest soft-alpha volume + proximity_fade; the one visible oddity | **0 px** (Metal majority cluster vs MoltenVK) | identical |

**No M-FEAT result exists in this run. Limb 1 of the revisit-trigger is NOT ARMED.**

**Bonus finding — Metal beats MoltenVK on cold start, and it is not close:**

| | cold-start penalty (shader-cache wiped) |
|---|---|
| **Metal** | **+17 ms median** (range −407 … +461 ms — i.e. inside run-to-run noise) |
| **MoltenVK** | **+960 … +3,974 ms** |

Warm steady-state render span is a wash (Metal 0.98× – 1.02× of MoltenVK). So on this machine
Metal is the equal of the reference driver in throughput and materially better on first-render
latency — which is the cost a bake-off cadence actually pays every time it opens a new session.
**This is affirmative empirical support for R-1(a), not merely an absence of counter-evidence.**

---

## 7 · Emitter / constraint notes for gandalf's T-A table

What a VFX author on this stack must respect. These are the deliverable P4 consumes.

1. **Both vendor packs ship shadow-casting geometry on VFX meshes.** On a stage with a single
   directional key and shadows on, `b_smoke` and `b_beam` both drop a **hard black blob on the
   floor** next to the effect (eye-read `b_smoke` frame 0045/0088, `b_beam` frame 0045). Binbun
   ships an explicit `shadow_caster.tres`. **Constraint: disable shadow casting on additive /
   emissive VFX meshes at mount time,** or the effect paints a black hole beside itself. Class
   **ASSET**, reproduces identically on MoltenVK, not a Metal signal.
2. **Beam-class assets are authored along −Z.** Mounted at identity in front of a camera that
   looks down that axis, a beam is photographed **end-on** and reads as a blob. **Constraint:
   beam archetypes need an explicit orientation contract in T-A** (aim vector → yaw), not a
   default transform.
3. **Additive stacking blows to white over a light floor.** Confirmed again here: the first
   calibration pass at floor albedo 0.20 washed the frame; 0.085 reads correctly. **Constraint:
   Tier-1 element parameterisation (charter § 3.3) must be judged against the actual stage
   albedo**, or "recolour survivability" will be assessed on a lie. Consistent with the
   2026-06-19 spell-VFX finding — this is now twice-attested.
4. **Effect lifetimes vary by more than 5×, and archetype binding must carry the number.**
   Measured on-frame windows: `p_turb` **16 frames** (0.53 s one-shot burst), `p_slam` 36 frames,
   `b_expl` 77 frames, and `p_flame`/`p_spike`/`b_poison`/`s_fire` **all 90** (continuous).
   **A telegraph that lasts 0.53 s and one that never stops are not interchangeable
   at the same archetype** — T-A should carry a lifecycle class (burst / decaying / sustained)
   alongside the VFX selection.
5. **Peak screen coverage spans 0.03 % → 67 %.** `p_trail` at 535 px is effectively invisible
   at our gameplay camera; `b_expl` covers 46 % and `x_attr` 67 %. **Readability (charter § 3.2)
   has to be scored against a coverage floor AND a ceiling** — one occludes the fight, the other
   cannot be seen.
6. **We own zero particle-collision and zero attractor content** (§ 2). Both work perfectly on
   this stack (and identically on MoltenVK). **If an archetype wants debris-that-lands or
   vortex-pull motion, it must be authored — it cannot be selected from the packs.**
7. **`beam_vfx` (Binbun assets-5) is the one pack whose internal resource paths point at the
   `.gdignore`d nested tree** (`res://Assets/Binbun_VFX/assets-5/…`) while all 9 other Binbun
   packs use the symlinked flat form (`res://assets/BinbunVFX/…`). It loads **only** because
   Godot resolves the `uid://` first. **Fragile — a UID-cache rebuild would break the beam pack.**
   Class **ASSET**; logged for a future lap, not fixed here (out of scope: `Assets/` is read-only).

---

## 8 · Revisit-trigger status — stated per limb, per the pre-registration

- **Limb 1 (feature failure) — MINE to arm. → NOT ARMED.**
  Zero M-FEAT results. Every cross-checked suspect is pixel-identical to MoltenVK over all 90
  frames. There is no concrete Metal feature failure in this evidence.
- **Limb 2 (throughput bottleneck) — NOT MINE to arm. → NOT-ARMED-BY-DEFAULT.**
  Raw number reported: **357 – 658 renders/hour, median 535** (one 90-frame 3.0 s 1080p
  capture, warm, including process launch). No "bake-off-hostile" threshold exists anywhere in
  the project and I did not invent one after seeing my own numbers.
  **gandalf rules limb 2 at P4 against the actual step-2 bake-off cadence.**

  **PROPOSAL (clearly labelled a proposal, not a gate):** a bake-off round of ~30 candidate
  effects × 2 renders = 60 renders lands in **~7 minutes** at the median. A cadence would only
  become hostile if a round needed several hundred renders *and* had to complete inside a single
  interactive session. On this machine I cannot construct a plausible step-2 round that does.

**Neither limb armed ⇒ per the dispatch, the cross-host (PC/SSH-tunnel/Vulkan) question does
not reopen, and I take no action toward it.** If gandalf's limb-2 ruling at P4 differs, that is
his call to make against the cadence number, not mine.

---

## 9 · Resource-bounds projection vs measured (Discipline #1.1)

**Occupancy measured at session start, not inherited** (the CP-B 6.69 G-of-10 G PL-5 figure is
stale): galadriel capture tree **7.2 G**, `reincarnated-godot/harness_logs/` **2.8 G**,
`reincarnated-godot/tmp/` 4.7 G. Real PL-5 headroom **≈ 2.8 G**. Disk-level free: 31 GiB.

**`frame-size` was calibrated, not assumed** — one real bloom-heavy effect (`b_expl`) rendered
first: **229 KB/frame** at 1920×1080 lossless PNG (the initial light-floor pass measured 360 KB/frame;
the tuned dark stage compresses better). Final measured spread across all 13: **min 20.7 KB,
median 81.3 KB, max 241.4 KB per frame** — a **11.7× spread**, which is exactly why a scalar
assumption would have mis-projected.

| | projected (from the calibration) | measured |
|---|---|---|
| PNG transient, peak (per effect, deleted after encode+hash+delta) | ~82 MB | ~66–82 MB |
| retained capture set incl. MoltenVK passes | ~100 MB | **44 MB** |
| repo work dir after cleanup | < 1 GB | **548 KB** |

**Measured footprint 44 MB against ~2.8 G real headroom — 1.6 % of it.** Well inside budget.
Achieved by the method the dispatch prescribed: short clips + **PNG cleanup after encode**
(the lossless intermediate is deleted per effect; only the mp4, 4 named eye-verification stills,
the JSON and the logs survive). No budget increase was needed or taken.

**Total renders this session: 79** (2 pre-flight + 1 load probe + 26 free pass ×2 laps + 26
fixed pass + 8 MoltenVK cross-check + 2 residual repeats + calibration).

---

## 10 · Anomaly register — every anomaly classified into exactly one bucket

| # | effect | class | finding | disposition |
|---|---|---|---|---|
| A-1 | `b_beam` | **SCENE** | beam authored along −Z, photographed end-on by the fixed camera | **FIXED** (90° yaw), re-rendered, not reported as Metal |
| A-2 | `x_attr` | **SCENE** | 2,000 additive quads at 0.85 alpha blew to flat white; attractor shape unreadable | **FIXED** (alpha 0.55, 900 particles), re-rendered |
| A-3 | *(all)* | **SCENE** | initial floor albedo 0.20 washed additive effects | **FIXED** (albedo 0.085) at calibration, before the measured pass |
| A-4 | `b_smoke`, `b_beam` | **ASSET** | vendor VFX meshes cast hard black shadow blobs on the floor | reported → T-A constraint § 7.1; reproduces on MoltenVK; not a renderer signal |
| A-5 | `b_beam` pack | **ASSET** | Binbun assets-5 internal paths point at the `.gdignore`d tree; loads only via `uid://` | reported § 7.7; `Assets/` read-only, not fixed |
| A-6 | *(all 13)* | **HARNESS** | 2 shutdown lines per run: `N shaders of type ParticlesShaderRD were never freed` / RID leak at exit | **exit-time RID accounting** when quitting with particles live. Present on **both** drivers, every effect, benign. **Never a renderer signal.** |
| A-7 | *(instrument)* | **HARNESS** | `--resolution 1280x720` sets the **window**; Movie Maker writes at the **project viewport** (1920×1080) | recorded, not "fixed" — 1080p is the house deliverable size. Related to but distinct from the `AGENT_STATE:3547` 1920×971 viewport trap. |
| A-8 | *(instrument)* | **HARNESS** | `/opt/homebrew/bin/python3` and `/usr/bin/python3` have no numpy; PATH order silently selected the wrong one | fixed — instrument resolves a numpy-capable interpreter explicitly |
| A-9 | all 13 free-seed rows | **NONDET** | cross-process variance 861 – 796,145 lit px | **datum, not a failure.** Dominant term identified as the emitter RNG seed (§ 5.2) |
| A-10 | `b_smoke` (1 run in 4), `b_expl` vulkan | **NONDET** | residual divergence survives seed-pinning, intermittently | § 5.3. Visually equivalent; present on both drivers; promotion condition does not fire |

**Zero M-FEAT. Zero SCENE defects left unfixed. Zero HARNESS defects misfiled as Metal.**
The `--quit-after`-is-FRAMES trap (`AGENT_STATE:2184`) was **inherited, not rediscovered** —
the probe carries an explicit `get_tree().quit()` on phase-complete from the first line of code.

---

## 11 · Capture set + license lineage

**Captures:** `agentic_orchestration/galadriel/captures/2026-08-23-metal-vfx-probe/`
**Class E — UNTRACKED, 340 files, 44 MB.** Per effect: `.mp4`, 4 named stills, `.delta.json`,
`.delta.txt`, `.metrics.json`, `.ffprobe.json`, cold+warm logs; plus the 4 MoltenVK cross-check
sets and the 3 `XCHECK_b_smoke_*` pair/diff-map files.

**Deliberate convention divergence, flagged so it does not read as drift:** the godot repo's
convention is `harness_logs/<task>_<date>/` (`CLAUDE.md:101`). These land in the galadriel
capture tree instead because **galadriel is the named downstream consumer** in the dispatch
deliverables. This is a dispatch-directed divergence, not repo drift.

### License lineage — in the TRACKED note, per the Stage-4 clearance gate

The same-date Synty EULA finding (gandalf+legolas, `158875bd` / `d27e2c75`) wrote a **license
lineage gate** into the ensemble spec Stage-4: a lane survives only if **no Synty-derived pixels
enter the 3D-generation input chain**. A `LINEAGE.md` inside an untracked Class-E dir would
itself be untracked, so the durable record is this table.

| id | vendor | pack | Synty-derived pixels? |
|---|---|---|---|
| `p_turb`, `p_trail`, `p_slam`, `p_spike`, `p_flame` | **Synty** | POLYGON Arsenal (`Assets/PolygonArsenal/`) | **YES** |
| `s_fire` | **Synty** | POLYGON Particle FX (`Assets/Particle_FX/`) | **YES** |
| `b_beam` | Binbun | BinbunVFX assets-5 | no |
| `b_fire` | Binbun | BinbunVFX assets-19 | no |
| `b_smoke` | Binbun | BinbunVFX assets-6 | no |
| `b_expl` | Binbun | BinbunVFX assets-21 | no |
| `b_poison` | Binbun | BinbunVFX assets-18 | no |
| `x_coll`, `x_attr`, `x_none` | **none** — constructed | — | **no vendor pixels at all** |

Stage: constructed in code (primitive meshes + `StandardMaterial3D`). **No Synty geometry,
textures or characters appear in the stage itself** — Synty pixels enter only via the six
Synty-vendor effect rows above.

> **⚑ EXCLUSION, flagged to charter § 4 P3 consumers so it travels with the data:
> these captures are DIAGNOSTIC EVIDENCE. They are excluded by construction from any
> reference corpus, any judge corpus, and any 3D-generation input chain.**
> Co-location in the galadriel capture tree is a real vector, but a directory-name convention
> is the wrong place to gate it — the durable gate is at the **consuming** end (charter § 4 P3
> selection, and Stage-4 clearance). P3 must not draw candidates from this directory.

**Repo law observed:** no Synty binaries committed (`/Assets/Synty/`, `/Assets/Particle_FX/`
remain git-ignored). Derivative render outputs stay untracked. `project.godot` restored after
every Godot launch that rewrote it.

---

## 12 · Scope discipline

**Untouched, as required:** any SB-1 surface · any existing `run_*.sh` (U-7(b)) · `sa_gate.py` ·
any write to `Assets/` · any engine-seam path · any PC / cross-host / SSH-tunnel work ·
any VFX authoring, minting, selection or archetype opinion (this is a **constraint envelope**,
not content) · the BR-2 nondeterminism *fix* (measured and bounded only).

**HALT conditions: none hit.** No crash, no non-terminating render, no suspect overflow
(4 suspects, at the cap), no resource-projection failure, no time-box overrun with unmeasured
effects. Every one of the 13 selected effects has a complete row. **No partial findings filed.**

**Blind CLI** used throughout under the dispatch's pre-authorisation of the `CLAUDE.md:67-71`
carve-out. Nothing mid-probe turned out to be genuinely alignment-shaped; the two
transform-adjacent moments (beam yaw, camera pull-back) were single stage constants, resolved by
simplifying rather than reaching for MCP — which is what the dispatch asked for.

---

*Filed by drax, 2026-08-23. Consumed by gandalf at charter P4 (T-A emitter/constraint notes,
§ 7) and by the R-1 empirical track (§ 0, § 6). **§ 5 awaits gandalf's formal ratification per
ledger L-13(a).***
