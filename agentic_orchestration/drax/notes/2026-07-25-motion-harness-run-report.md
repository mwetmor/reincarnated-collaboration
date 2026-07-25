# RUN REPORT — Motion harness (TCP-37 ③)

**Agent:** drax (presentation seam) · **Date:** 2026-07-25
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-drax-motion-harness.md`
**Authorization:** Matt, verbatim — *"Motion harness commission to drax now, in parallel — go."*
**Status:** **COMPLETE.** All six exit-predicate items met. Harness is durable and stays.

---

## 0 — One-line result

`~/Games/mcp-lab/harness/` now holds a self-contained Godot 4.6.3 project that turns
**scene + camera + duration + fps** into **numbered PNGs + MP4 + GIF + a timestamped
film-strip**, unattended, at a fixed timestep — and it re-renders **byte-identically**,
measured, 90/90 frames, on four independent tests.

---

## 1 — Read-list (declared, in order)

| # | Path | Note |
|---|---|---|
| 1 | `agentic_orchestration/dispatches/2026-07-25-drax-motion-harness.md` | the commission; governs |
| 2 | `~/Games/mcp-lab/project/l4_shoot.gd` | **read only, never executed, never written.** Dispatch-authorized. Source of the SubViewport + `frame_post_draw` + `save_png` idiom, of the `__box` camera derivation, and of the one-scene-per-process rule |
| 3 | `~/Games/mcp-lab/evidence/l4/CALIBRATION.md` | L4c's measured 2–7 px growing/spreading drift across repeat captures in one process. Set the determinism question this lap had to answer |
| 4 | `~/Games/reincarnated-godot/scripts/run_replica_mp4.sh` | my own prior art — Godot Movie Maker (`--write-movie` + `--fixed-fps`) → ffmpeg. Considered and **not** adopted as primary (§3 R1) |
| 5 | `~/Games/reincarnated-godot/scripts/hero_walker.gd` | how the animated hero is actually assembled: `SK_Chr_Male_Wizard.fbx` + `A_MOD_BL_Walk_F_Masc.fbx` through a Sidekick→GeneralSkeleton bone-map with `rest_fixer`/`fix_silhouette`. This is what made the rigged-character demo non-trivial (§3 R3) |
| 6 | `~/Games/reincarnated-godot/` asset tree (2,178 `.glb` scanned programmatically; `.fbx` counted) | the measurement behind the demo-target ruling |
| 7 | `~/Games/mcp-lab/env.sh`, `bin/`, `prep/`, `evidence/` listings | lab layout, to place the harness without colliding |

**`scripts/kit_replica_level.gd` was NOT read** — no state to declare. I had no need for the
replica level and the pillar-quilt dispatch owns it concurrently.

---

## 2 — What was built

`~/Games/mcp-lab/harness/` — new, self-contained, **12 files**, no dependency on
`mcp-lab/project/`:

```
project.godot          Godot 4.6, Forward+, 320x180 boot window, file-logging OFF
motion_rig.tscn        Node + rig script. That is the entire scene.
motion_rig.gd          THE RIG — args, SubViewport, camera, capture loop, manifest
motion_clip.gd         THE CLIP CONTRACT + helpers (runtime GLB load, locked-down env,
                       ground, seek_all_players)
clips/smoke_spin.gd            seek · zero external assets · the rig's own smoke test
clips/demo_sword_arc.gd        seek · THE DEMO OF RECORD
clips/demo_particles_step.gd   step · GPUParticles3D · L7's path
clips/probe_accum_on.gd        seek · control experiment (accumulators back ON)
bin/shoot_clip.sh      one command: render → mp4 → gif → film-strip → render.log
bin/filmstrip.py       Pillow contact sheet, N thumbs at fixed intervals, timestamped
bin/framediff.py       determinism instrument: per-frame sha256 + pixel forensics
README.md              inputs, invocation, stepping model, measured facts
```

The project **has no `.godot/` directory at all** — it imports nothing. Every asset a clip
uses is loaded from an absolute OS path at runtime via `GLTFDocument`. It therefore cannot
acquire a stale import cache, cannot collide with another project's, and cannot drag a
`res://` dependency on `reincarnated-godot` into the lab.

---

## 3 — Rulings, with reasoning (dispatch §4.4)

### R1 — Time-stepping mechanism: **absolute seek (`t = k/fps`) as primary, engine-fixed-delta step mode as the second gear**

Two modes, because not everything can be a function of `t`:

- **`--mode seek` (default).** The rig hands the clip the **absolute** time of every frame.
  No accumulation ⇒ no float drift; frame *k* is reproducible in isolation; the same clip
  at 30 and 60 fps yields the same world at the same wall-times.
- **`--mode step`.** For integrators with no seek (`GPUParticles3D`, physics). The rig
  advances by a fixed `dt = 1/fps` and **refuses to start** unless Godot's own frame delta
  already *is* that step (`--fixed-fps`), re-checking every frame plus asserting exactly one
  engine frame elapses per capture.

**Rejected: Godot Movie Maker (`--write-movie` + `--fixed-fps`) as primary**, despite it
being my own prior art in `run_replica_mp4.sh`. Three reasons. (a) It captures the *root
window* viewport, so output resolution is hostage to the OS window and HiDPI scaling; the
SubViewport path is resolution-exact and lets the boot window be 320×180. (b) Its time is
*accumulated*, so frame 137 can only be reached by simulating 0…136 — you cannot re-render
one frame, which is exactly the operation that makes a divergence diagnosable. (c) It forces
whole-engine behaviour that then has to be reasoned around. Movie Maker's genuinely useful
half — `--fixed-fps` — turns out to be a **standalone flag**, so step mode takes that and
leaves the rest. Documented in the README as the alternative if a future clip needs the
engine's own main loop to drive it.

**Measured, and this is the ruling's proof:** in seek mode the engine's frame delta wandered
**6.09 ms … 39.48 ms (6.5×)** in one run and **6.08 ms … 32.63 ms (5.4×)** in another, and the
two runs are byte-identical, frames and MP4 alike. Render cost provably does not reach the
clip. In step mode the same field reads **33.3333 ms … 33.3333 ms, spread 1.000**.

### R2 — Assembly tool: **ffmpeg for MP4/GIF; Pillow for the film-strip**

ffmpeg **8.1.2** (homebrew, `/opt/homebrew/bin/ffmpeg`) → h.264 CRF 17 yuv420p `+faststart`,
and a palettegen/paletteuse GIF. **But the contact sheet is Pillow 10.3.0, not ffmpeg**: this
ffmpeg is built *without libfreetype*, so the `drawtext` filter does not exist —
`ffmpeg -filters | grep drawtext` returns nothing. ffmpeg's `tile` alone would produce a
pretty grid with no timestamps, and an untimestamped strip cannot answer "is that thumbnail
at 0.20 s or 1.40 s", which is the only question a motion contact sheet is asked.

The MP4's frame rate is **read back from the manifest the rig wrote**, never from a shell
variable — if the two ever disagreed, the video would play at a rate the capture did not use
and every timing judgement made from it would be silently wrong.

### R3 — Demo target: **scripted motion (dispatch §3's pre-authorized fallback), taken on measurement, not on impression**

I scanned **all 2,178 `.glb` files** under `reincarnated-godot/Assets` for glTF animation
channels. **Zero have any.** Every animated Synty asset in the corpus is `.fbx` — **25,992**
of them — and `.fbx` has no runtime import path in Godot (it needs the editor's FBX2glTF
step). The hero specifically needs, per `hero_walker.gd`, the Sidekick → GeneralSkeleton
bone-map with `rest_fixer`/`fix_silhouette`, configuration that lives in
`reincarnated-godot`'s import cache — a repo that is read-only for me this lap *and* under
concurrent modification. There is no trivially-loadable rigged character. Fallback taken,
no rabbit-hole entered, per §3's explicit pre-authorization.

The fallback is still **our content**: `Binbun_VFX/Long_Sword_01.glb`, loaded at runtime from
an absolute path. And it is *chosen to stress the thing under test* — a cleave with a slow
windup and a ~210° strike in ~0.34 s, i.e. ~35° between adjacent frames at 30 fps. If the
clock were wall-clock, that strike would visibly stretch or compress between runs.

**The bridge to L6 is one line, not a rewrite.** When a rigged character arrives as a `.glb`
with an `AnimationPlayer`, it is a seek-mode clip whose `set_time` calls
`seek_all_players(node, t)` — already written and shipped on the base class. The rig does not
change.

### R4 — Not `--headless`, and the rig refuses rather than documents

**Measured on this build** (Godot 4.6.3, Metal, M2): under `--headless` the display server is
`headless`, the renderer is dummy, and `RenderingServer.frame_post_draw` **never emits**. The
first await blocks, `--quit-after` eventually kills the process, and it **exits 0 having
written zero frames**. A silent, successful-looking nothing — the worst failure shape there
is. Discovered by probing rather than by inheriting `l4_shoot.gd`'s claim, and the probe found
something worse than the claim (not "empty PNGs", but "no PNGs and success"). The rig now
**refuses at startup** if the display server is `headless`/`dummy`, before parsing a single
argument, with the reason and the fix in the message. Same principle as L3's `editor_up.sh`
and L4's one-scene-per-process refusal: structural, not documented.

"Fully headless" in the dispatch's sense is satisfied as **unattended** — no operator, no
editor, one CLI invocation. The OS window is 320×180 and is *not* what gets captured.

### R5 — Temporal-accumulator lockout as a rig-level precondition

`deterministic_env()` explicitly disables glow, SSAO, SSIL, SDFGI, volumetric fog and
auto-exposure, and the capture SubViewport disables TAA, screen-space AA and debanding. This
was a hypothesis when written (they are all cross-frame integrators, and a motion clip is
many captures in one process by definition) and is now **measured causal** — see §5.

---

## 4 — Demo proof (dispatch §4.2)

`out/demo_sword_arc/` — **3.000 s, 30 fps, 90 frames, 1280×720** (dispatch minimum: ≥2 s,
≥24 fps).

| artifact | path |
|---|---|
| MP4 | `~/Games/mcp-lab/harness/out/demo_sword_arc/demo_sword_arc.mp4` (h.264, 3.000 s, 90 frames) |
| GIF | `~/Games/mcp-lab/harness/out/demo_sword_arc/demo_sword_arc.gif` |
| frames | `~/Games/mcp-lab/harness/out/demo_sword_arc/frames/frame_00000…00089.png` + `manifest.json` + `timing.json` |
| film-strip | `~/Games/mcp-lab/harness/out/demo_sword_arc/demo_sword_arc_strip.png` (12 thumbs, each stamped `t=…s f=…`) |
| invocation + log | `~/Games/mcp-lab/harness/out/demo_sword_arc/render.log` |

Second demo, step mode: `out/demo_particles_step/` — same duration/rate, a `GPUParticles3D`
burst on an orbiting emitter. Not required by the dispatch; built because L7 needs to know
*before it starts judging bursts* whether particle evidence is bit-comparable. It is (§5).

Wall cost: **≈5 s per 90-frame 720p clip**, end to end including encode and strip.

---

## 5 — Determinism report (dispatch §4.3) — measured, not assumed

Godot 4.6.3.stable · Metal · Apple M2 · 1280×720 · MSAA 4× · 90-frame clips.
Instrument: `bin/framediff.py` (per-frame sha256; on mismatch, changed-pixel count, max
channel delta, mean abs delta, bbox). JSON artifacts in `~/Games/mcp-lab/harness/out/`.

**Scale bar first, because "3 px differ" means nothing without one.** Adjacent frames of the
demo motion differ by **150,602–208,321 px of 921,600** (max channel delta 180); for the
particle clip, up to **824,508 px**. That is the signal any run-to-run difference is read
against.

| test | artifact | result |
|---|---|---|
| Re-render same clip, separate process | `DETERMINISM_rerun.json` | **90/90 byte-identical.** MP4s share sha256 `3f64795a2aa1742d…` |
| Frame *k* @30 fps vs frame *2k* @60 fps | `DETERMINISM_samplerate.json` | **90/90 byte-identical** — sampling-rate independence |
| `--settle 30` vs `--settle 60` | `DETERMINISM_settle.json` | **90/90 byte-identical** — no index-dependent renderer drift |
| Step mode, GPU particles, re-render | `DETERMINISM_particles.json` | **90/90 byte-identical** |
| **Same clip, accumulators ON** | `DETERMINISM_accum_on.json` | **0/90 byte-identical** — 72–977 px/frame (max 0.106%), **max channel delta 1**, mean abs 0.00106, bbox spanning the whole frame |

### 5.1 — The finding: the lockout is causal, and it reconciles this lap with L4c

L4c measured, for **stills**, 2–7 px of *growing and spreading* drift across repeat captures
inside one process, and responded correctly by making `l4_shoot.gd` refuse more than one
scene per invocation. This harness renders **90 captures in one process** and reproduces all
90 byte-for-byte across processes. Both results are real; the variable is the lockout.

`probe_accum_on.gd` isolates it — identical to the demo clip in every respect except that
glow/SSAO/SSIL/SDFGI are switched back on. Byte-identity collapses on **every single frame**.
So:

- **A clip that keeps the lockout produces bit-comparable evidence.** Equality is a valid test.
- **A clip that needs glow — most VFX will — does not.** Its divergence is one LSB
  (max channel delta **1**, invisible), and *fatal to a differ that tests `==`*. Such evidence
  must be compared with a declared tolerance, and the clip must say so.

That is the actionable line for L6/L7, and it is the reason the probe ships: the next agent
re-runs it rather than re-deriving it.

Not claimed: that the lockout is the *only* contributor to L4c's drift. L4 also swapped
scenes between captures and this clip does not, and I cannot separate those two without
running inside `mcp-lab/project`, which is forbidden this lap. The probe isolates the
accumulator variable; scene-swapping remains untested. Also untested: **cold shader-cache
identity** — every run above had a warm `user://shader_cache`.

### 5.2 — The instrument caught its own rig, on the first run

The first determinism run returned 90/90 byte-identical frames **and two differing
manifests**. `manifest.json` carried `delta_min`/`delta_max` — the *observed engine deltas* —
while the file's own header comment claimed it contained no wall-clock. The doc was right and
the code was wrong. Those numbers are evidence and are kept, but they now live in
`timing.json`, which nothing compares. Manifests are now byte-identical across runs
(`42a6d79ef17df03b…`), so "the manifests differ" is once again a clean signal that **the
inputs differed** and any frame comparison downstream is meaningless.

---

## 6 — Hygiene (dispatch §4.5)

**`mcp-lab/project/` — untouched. Stated explicitly.** Zero writes. Every Godot invocation used
`--path /Users/admin/Games/mcp-lab/harness` and is recorded verbatim in the run's
`render.log`. The single access of any kind was the dispatch-authorized **read** of
`l4_shoot.gd`. `find mcp-lab/project -newermt '90 minutes ago' -type f` → **0 files**. (The
directory's own mtime did move at 16:25, which is the L5 lap's floor, not mine.)

**`user://` clean.** The rig writes nothing to `user://` — all output goes to absolute paths.
Godot's default file logging was dropping a timestamped `.log` per invocation; disabled in
`project.godot`, and note it takes **both** `debug/file_logging/enable_file_logging` **and**
`…enable_file_logging.pc`, because the desktop-specific override is the one that defaults to
true (measured: with the base key alone, `user://logs/godot.log` reappeared after every run).
Accumulated logs removed. What remains under
`~/Library/Application Support/Godot/app_userdata/tcp-motion-harness/` is Godot's own
regenerable `shader_cache/` and an empty `vulkan/`.

**Scratch vacated:** `out/_probe`, `out/_smoke`, `out/_headless_probe`, `out/_refusal`.
**Evidence kept:** the two demo runs, the four comparison runs, five determinism JSONs
(104 MB total).

**Nothing was borrowed.** No Pro `capture_frames`/`record_frames`, no Murzak, no addon. TCP-8
holds: what this scores is our authoring.

**Nothing was written outside `mcp-lab/harness/`** except this report and the dispatch
completion record in the meta-repo, both of which the dispatch directs.

---

## 7 — Exit predicate

| # | Item | Status |
|---|---|---|
| 1 | `harness/` project + rig scripts + README | **MET** — 12 files, README covers inputs/invocation/stepping model |
| 2 | Demo clip (mp4/gif) + frame dir + film-strip | **MET** — 3.000 s @ 30 fps, 1280×720, 90 frames; second step-mode demo as a bonus |
| 3 | Determinism report | **MET** — 4 tests byte-identical, 1 control experiment divergent by design; per-frame sha256 in JSON |
| 4 | Rulings logged, read-list declared | **MET** — §3, §1 |
| 5 | `user://` clean; `mcp-lab/project/` untouched | **MET** — §6, stated explicitly |
| 6 | Harness is durable and stays | **MET** — only scratch vacated |

**No HALT conditions hit.** Nothing needed writing outside `mcp-lab/harness/`; no temptation
to borrow a wire's capture tools arose, since building ours took one lap.

---

## 8 — What the next lap gets, in one paragraph

L6: a rigged `.glb` with an `AnimationPlayer` becomes a clip whose `set_time` is
`seek_all_players(node, t)`; the rig does not change, and the evidence is bit-comparable.
L7: use `--mode step`, lock `GPUParticles3D.fixed_fps` to the capture rate with
`interpolate = false` and a fixed seed, and the burst re-renders byte-identically — **unless**
the VFX needs glow, in which case declare a tolerance and stop testing equality. Both get a
timestamped film-strip for free, which is what makes L-A (judgeable by Matt unaided)
satisfiable for motion at all.

**Signed:** drax, 2026-07-25.
