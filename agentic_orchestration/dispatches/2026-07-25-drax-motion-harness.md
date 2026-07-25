# DISPATCH — Motion harness (TCP-37 ③: commissioned by Matt, parallel to L5)

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Program:** `agentic_orchestration/gandalf/notes/2026-07-24-tool-capability-program-charter.md`
**Authorization:** Matt, verbatim: *"Motion harness commission to drax now, in parallel — go."*

## §0 — Why this exists

The program's L6 (animated monsters swinging weapons) and L7 (VFX) **cannot be judged from stills** —
a swing arc and a particle burst exist only in time — and law L-A (frames judgeable by Matt unaided)
is unsatisfiable for them without motion evidence. Per TCP-8 the evidence rig must be **OURS**: Pro
ships `capture_frames`/`record_frames`, Murzak ships nothing — borrow a wire's rig and the program
scores capture tooling instead of authoring capability.

## §1 — Home, and a hard concurrency rule

**Build in `~/Games/mcp-lab/harness/` — a NEW, self-contained minimal Godot project.**
**Do NOT touch `~/Games/mcp-lab/project/` at all** — the L5 lap owns that floor concurrently, and two
agents interleaving one Godot project dir (shared `.godot/`, `user://`) cross-contaminates both.
Read-only reference into other repos is fine and expected.

**Prior art, yours:** the MP4 walkthrough harness in `~/Games/reincarnated-godot/` (your own seam
work — camera-path-over-time is the closest ancestor); `~/Games/mcp-lab/project/l4_shoot.gd` for the
offscreen headless render idiom (read it; do not run in that dir). Note `reincarnated-godot` is under
concurrent authorized modification by the pillar-quilt dispatch — read-only for you, and declare
which state you saw if you read `scripts/kit_replica_level.gd`.

## §2 — Target state (decidable)

A reusable rig: **scene + camera + duration + fps + fixed timestep in → (a) numbered PNG frame
sequence, (b) assembled MP4 (and/or GIF), (c) a film-strip contact sheet** (N thumbnails at fixed
intervals, timestamped) **out**, fully headless.

- **Fixed-timestep stepping, not wall-clock** — frame k is at t = k/fps regardless of render cost,
  so re-renders are comparable. How you step time headlessly is your ruling to log (the L4 rigs'
  await pattern is known-good for stills; motion needs advancing `AnimationPlayer`/physics time).
- **Assembly tool:** ffmpeg if present (declare version); else a Python fallback (imageio/PIL GIF).
  Your ruling, declared.
- **Determinism measured, not assumed:** re-render one clip; report per-frame byte-identity. Stills
  were byte-stable (L4c); motion may not be. **Either answer is a finding, not a defect.**

## §3 — Demo proof (the exit's evidence)

One clip, **≥ 2 s at ≥ 24 fps**, of a Synty rigged character playing any animation from our packs,
at an ARPG-style camera — IF one is reachable without retargeting work. **Honorable fallback,
explicitly pre-authorized:** if no animated character is trivially loadable, demo with scripted
motion (rotating/translating object + a moving light). **The harness measures CAPTURE, not animation
authoring** — do not rabbit-hole on rigs/retargeting; that is L6's lap, not this commission.

## §4 — Exit predicate

1. `harness/` project + rig scripts + a README (inputs, invocation, stepping model).
2. Demo clip (mp4/gif) + its frame dir + film-strip sheet.
3. Determinism report (byte-identity per frame, or the measured divergence).
4. Rulings logged (stepping mechanism, assembly tool, demo target), read-list declared.
5. `user://` clean (TCP-34 ④ lineage); `mcp-lab/project/` untouched — state it.
6. The harness itself is **durable OURS tooling — it stays**; only scratch vacates.

**Report to:** `agentic_orchestration/drax/notes/2026-07-25-motion-harness-run-report.md`
**HALT to gandalf:** any need to write outside `mcp-lab/harness/`; any temptation to borrow Pro's
capture tools (that is a TCP-8 program question, not an implementation choice).

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`).

---

## Completion record

**drax, 2026-07-25 — COMPLETE. All six exit-predicate items met.**

Full report: `agentic_orchestration/drax/notes/2026-07-25-motion-harness-run-report.md`.

- **Built:** `~/Games/mcp-lab/harness/` — 12-file self-contained Godot 4.6.3 project. Rig +
  clip contract + 4 clips + `shoot_clip.sh` / `filmstrip.py` / `framediff.py` + README.
  Imports nothing (runtime `GLTFDocument` from absolute paths), so it has no `.godot/` cache
  at all. Nothing borrowed — TCP-8 holds.
- **Stepping ruling:** absolute seek (`t = k/fps`) primary; engine-fixed-delta `step` mode for
  integrators with no seek, which **refuses to start** without `--fixed-fps`. Godot Movie
  Maker rejected as primary (window-hostage resolution; accumulated time means no single-frame
  re-render). Proof: seek-mode engine delta wandered 6.5× and 5.4× across two runs that are
  byte-identical frames *and* MP4 sha256.
- **Assembly ruling:** ffmpeg 8.1.2 for MP4/GIF; **Pillow for the film-strip** — this ffmpeg
  has no `drawtext` (built without libfreetype) and an untimestamped strip answers nothing.
- **Demo ruling:** §3's pre-authorized fallback, taken on measurement — **all 2,178 `.glb` in
  `reincarnated-godot/Assets` scanned, zero carry animation channels**; the 25,992 animated
  assets are `.fbx` (no runtime import path) and the hero additionally needs a bone-map
  retarget config living in a read-only, concurrently-modified repo. Demo is a Binbun
  `Long_Sword_01.glb` cleaving (≈210° in 0.34 s) + a moving light, 3.000 s @ 30 fps, 1280×720,
  90 frames. L6 bridge is one line: `seek_all_players(node, t)`, already shipped.
- **Determinism — measured:** re-render **90/90 byte-identical**; 30 fps *k* vs 60 fps *2k*
  **90/90**; settle 30 vs 60 **90/90**; GPU particles in step mode **90/90**. Scale bar:
  adjacent frames of the motion differ by 150k–208k px (particles up to 824k).
  **Control experiment:** the same clip with glow/SSAO/SSIL/SDFGI ON is **0/90** byte-identical
  — max channel delta **1**, invisible, fatal to an equality differ. **The temporal-accumulator
  lockout is causal**, which reconciles this lap's clean result with L4c's measured drift.
  L7 must therefore declare a tolerance if its VFX needs glow.
- **Also found:** under `--headless` on this build, `frame_post_draw` never emits — the capture
  hangs and then **exits 0 with zero frames written**. Worse than the inherited "empty image"
  claim. The rig now refuses at startup. And the determinism instrument caught a defect in its
  own rig on first use: `manifest.json` carried wall-clock deltas against its own stated
  contract; moved to `timing.json`, manifests now byte-identical across runs.
- **Hygiene:** `mcp-lab/project/` **untouched — zero writes**; every invocation used
  `--path …/harness`, recorded in each `render.log`; the only access was the authorized read of
  `l4_shoot.gd`. `user://` clean (file logging needs **both** `enable_file_logging` and
  `.pc`; only Godot's regenerable `shader_cache/` remains). Scratch vacated; harness stays.
- **No HALT conditions hit.** `scripts/kit_replica_level.gd` was not read — no state to declare.
