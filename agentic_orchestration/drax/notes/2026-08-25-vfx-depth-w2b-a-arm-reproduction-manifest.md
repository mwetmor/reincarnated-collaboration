# VFX-DEPTH W2b — A-ARM REPRODUCTION MANIFEST (HITL whirlwind, Cathedral)

**Date:** 2026-08-25 · **Agent:** drax · **Authority:** charter **R-15** (Matt: *"we should have the logs so that we can reproduce it exactly"*) + **R-18(f)** (A-arm PARKED-NAMED, W2b fires to discharge it)
**Class:** evidentiary note · **Status:** CURRENT
**Arm:** **A** — Matt's own HITL whirlwind treatment (Undead Knight rig + tick-indexed trace), re-hosted in the Cathedral, at the ratified judging camera.
**Companion:** `2026-08-25-vfx-depth-w2-b-arm-reproduction-manifest.md` (the B-arm, same venue, same camera).

> **The standard this file is written to.** Matt's requirement is *reproduce it exactly*, so
> everything below is either a **hash**, a **verbatim log line**, or a **literal invocation**.
> Where a value is derived, the derivation is shown. Nothing here is "approximately".

---

## 1. THE ONE-LINE REPRODUCTION

```bash
cd ~/Games/reincarnated-godot
git checkout c029c03
bash scripts/run_kc2_cathedral_arm.sh
```

Every parameter below is that script's default. The explicit form, for a checkout at a different
commit or with the defaults changed:

```bash
env FPS=60 DELIVER=210 PREROLL=60 PLK=0.665 SHOT=canon STAGE=cathedral \
    UNDULATE=on CRF=18 STAMP=2026-08-25-w2b-acath \
    bash scripts/run_kc2_cathedral_arm.sh
```

⚑ **`FRAMES=209`, not 210, and the difference is a MEASURED HARNESS FACT rather than a fudge.**
Godot's Movie Maker writes a PNG for the frame in which the scene quits, so `--frames N --preroll P`
leaves **N + P + 1** files on disk. Measured on the invocation smoke: N=6, P=4 → **raw 11**, delivered
7 where 6 were asked for. Uncorrected, the A-arm would be **211** frames against the B-arm's **210**
and the two arms would not be frame-for-frame comparable — the one property that makes the
side-by-side clamp arithmetically inert instead of a crop. The runner takes `DELIVER`, passes
`DELIVER - 1`, and **ASSERTS the post-prune count**, so if Movie Maker ever stops writing that
terminal frame the run FAILS rather than silently shipping 209.

---

## 1a. THE ARTIFACT THIS MANIFEST REPRODUCES

| # | file | bytes | sha256 |
|---|---|---|---|
| **A-arm** | `/Users/admin/Games/reincarnated-godot/harness_logs/kc2_2026-08-25-w2b-acath/acath-hitl-ww-plk0665-60fps-1920x1080.mp4` | 2,023,251 | `5a5e1514e02750e31ffd376aad6ffa6bedc465c026644777df60564c1883263f` |

`ffprobe`-verified, **read off the stream and not from the invocation**:
**h264 · yuv420p · 1920 × 1080 · 60/1 fps · 210 frames · 3.500000 s**.
Decoded frame count **counted, not read from the header**: `210`.

**Frame-for-frame equal to the B-arm** (`plk06650_cathedral_fxon.mp4`, 210 frames, 60/1 fps,
1920 × 1080). That equality is what `CLAMP = min(210, 210) = 210` in the AB cut rests on.

| companion artifact | path |
|---|---|
| render log | `…/kc2_2026-08-25-w2b-acath/render.txt` |
| **sidecar** (baton sha, camera derivation, anchor audit, epoch schedule, venue meta) | `…/kc2_2026-08-25-w2b-acath/shot-B-undulating-canon.json` · sha256 `bab6404ed4ccde39017dcb7152b8eb07fb130b8bb59ead0cea2b56a54f038b93` |
| prune receipt | `…/kc2_2026-08-25-w2b-acath/prune_receipts.txt` |

⚑ **The sidecar was written to `$TMP` and is RESCUED into the capture dir — and that was a real
defect, not tidiness.** It carries the baton sha, the camera derivation, the anchor audit, the epoch
schedule, the venue meta and the tick period: most of what *"reproduce it exactly"* actually means.
In `$TMP` it is one reboot from gone while the mp4 it describes lives forever. **Caught by writing
this manifest and having to read the file out of `/tmp` to do it.** Fixed at the runner
(`cp -p "$SIDECARS"/shot-*.json "$OUT"/`), not just here.

---

## 2. BINARY + HOST

| item | value |
|---|---|
| Godot | **4.6.3.stable.official.7d41c59c4** (sidecar records `4.6.3-stable (official)`) |
| renderer | `--rendering-driver metal` (Forward+, Apple Metal) |
| host | macOS 24.6.0, Apple silicon Mac Mini |
| resolution | **1920 × 1080** — the scene's `SHOT_W`/`SHOT_H`; Godot's Movie Maker locks to `project.godot`'s viewport and ignores per-run overrides (measured at WW-4a v2) |
| render wall time | **156 s** for 270 raw frames |

---

## 3. SOURCE PIN — sha256 of every file that authored a pixel

| file | sha256 | role |
|---|---|---|
| `scripts/kc2_player_channel.gd` | `e8c0c4ac3cdd14f49ec46b654c9560f1aaf9e623ac1d24da8729d0a8f5f2dda3` | **THE HITL EFFECT — Matt's own hand. 4,217 lines. Byte-untouched by this wave.** |
| `scripts/kc2_cpb_clip.gd` | `393cf760a736177d16fc85fb92892a8cdb0a555c927ed56ab70f86d3ea91bb48` | the clip driver — **the only file this wave amended for the port** |
| `scripts/kc2_arena.gd` | `c629ae7d68fbb49cc71f775783acf67b4d7c9d00665416b7143ed466d95965f5` | arena, actors, player station, ground gate. **Byte-untouched.** |
| `scripts/kc2_motion.gd` | `4cf6d0d4d990f3fd0a081fa4a3497c67711fe13618abeb4d0e93ffe29d959bd5` | trace driver. **Byte-untouched.** |
| `scripts/s2_stage_env.gd` | `65354ef1c82b25e466fde916c289103407be35f247ba0cd54af47b6ea00d913c` | **THE VENUE — and this is the SAME HASH the B-arm manifest pins.** |
| `scenes/kc2_cpb_clip.tscn` | `4dc947312b9180369b218443b3cc309a3d205868c77a883f60670e58ca192ec3` | scene |
| `scripts/run_kc2_cathedral_arm.sh` | `f057522c62f5b8206adf05ea97225eb748e1825ff2f514a10d36c421a832c54a` | harness (post sidecar-rescue amendment; the render ran at `897cde41f7356f337c8c6969a5051c3b3c00b4855d3dde83dc11d0553aa78b1f`, which differs ONLY by that `cp`) |

**Repo state:** `reincarnated-godot` @ **`c029c03`**, pushed to `origin/main`.

**The trace:**

| item | value |
|---|---|
| baton | `/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-baton-v1-E-s09-cp150-20260809_052836.json` |
| baton sha256 | `d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa` — **GL-6: digest verified BEFORE load; a refusal is a refusal, nothing is built from an unverified artifact** |
| tick period | `0.0816326530612245` s |

⚑ **`s2_stage_env.gd` HASHES IDENTICALLY IN BOTH MANIFESTS.** That is the mechanical form of R-15's
requirement. The two arms do not render *similar* rooms; they call the same function in the same
build of the same file.

---

## 4. CAMERA RECEIPT — verbatim from `render.txt`, rendered IN THE CATHEDRAL

```
[cpb] player_lock ported offset (k=1, THE PORT, pinned below) = (14.7262, 28.3970, 13.7826) m
      |offset| 34.8312 m  height 28.3970 m
[cpb] player_lock: offset (camera - player ground) = k * ported = (9.7929, 18.8840, 9.1654) m
      |offset| 23.1627 m  height 18.8840 m
      (full precision: 9.7929267883301, 18.8840122222900, 9.1654367446899 · stand-off 23.1627407073975 m)
[cpb] player_lock PIN vs tmp/br2watch/m6/pl_audit.json: offset delta 0.000000000000 m,
      z_player delta 0.000000000000 m, tol 0.000010000000 m — MATCH
[cpb] player_lock: pitch 52.9535 deg  fov_v 31.7861 deg  z_player 34.8165 m
      anchor (0.50104, 0.55093) frac  yaw 47.0 deg
[cpb] PL-AUDIT anchor: subject ground projects to frac (0.501042, 0.550925);
      expected (0.501041, 0.550925);
      delta (0.000000, 0.000000) frac = (0.0002, 0.0001) px at 1920 x 1080
```

### ⚑ PIN RE-VERIFICATION AFTER THE PORT — the dispatch's explicit ask

**`|delta| 0.000000000000 m`. Twelve decimals of zero, in the Cathedral, after the venue swap.**
Identical to W1's bar and to the B-arm's W2 receipt.

Every dispatched parameter present verbatim: stand-off **23.1627407073975 m** · pitch
**52.9535411256029°** · yaw **47.0°** · fov_v **31.7861018306101° VERTICAL / KEEP_HEIGHT** · anchor
frac **(0.501041450500488, 0.550925123426649)** · **k = 0.665**.

⚑ **The anchor audit is a REAL test here, not a formality, and it is a HARDER test than the B-arm's.**
The venue swap moves the entire world around the subject *and* re-homes it against a station read out
of the trace. Had the port shifted the plane the anchor is solved against, the anchor would have moved
and convicted the build. **It moved two ten-thousandths of a pixel** — single-precision residue, the
same figure W1 recorded on the bare stage and the B-arm recorded in this same room.

---

## 5. THE VENUE — the port, and the receipt that it is the SAME room

```
[cpb] ⚑ VENUE SWAP -> 'cathedral'. root at (0.000000, 0.000000, -0.000000) = the player station;
      hidden ["ArenaFloor", "ArenaSkirtDress", "Key", "Fill"];
      Env (WorldEnvironment) — removed from tree, referenced, not freed
[cpb] VENUE floor reconciliation: baton ground_elevation 0.000000 m vs arena Y_FLOOR 0.000000 m
      — delta 0.000000 m
[cpb] VENUE meta: arena_center_derived [0.06, 1.593, -32.15] · floor_y_derived 1.593 ·
      stage_radius 26.0 · fight_surface_r 16.0 · tiles 126 · skirt rocks 148 · seed 20260825
```

### 5a. The room, side by side with the B-arm's own manifest

| `STAGE_META` key | **A-arm (this render)** | **B-arm (W2 manifest § 5)** |
|---|---|---|
| `recipe` | `cathedral` | `cathedral` |
| `arena_center_derived` | `[0.06, 1.593, -32.15]` | `[0.06, 1.593, -32.15]` |
| `floor_y_derived_m` | `1.593` | `1.593` |
| `stage_radius_m` | `26.0` | `26.0` |
| `fight_surface_r_m` | `16.0` | `16.0` |
| `fight_tiles_laid` | `126` | `126` |
| `fight_skirt_rocks_placed` | `148` | `148` |
| `fight_skirt_seed` | `20260825` | `20260825` |

**Character for character.** The skirt's jitter is one `RandomNumberGenerator` with **no other
consumer**, so two builds place identical rock — which is why this table is an equality and not a
resemblance.

### 5b. How the room was re-homed, and the choice I did NOT take

The venue is built under **one `Node3D` named `CathedralVenue`, translated to the kc2 player
station**, and `S2StageEnv.build()` is handed *that* root. The offset therefore reaches geometry,
lights and environment **uniformly, by construction**.

⚑ **The W2 seam map called for building into `self` and RE-PARENTING `PackCathedral` + `FightSurface`
afterwards. I did not do that.** Two node moves that must each preserve a global transform, and which
silently leave the directional lights and the `WorldEnvironment` behind at the origin — invisible
today (the environment is position-free and the lights are directional), and a trap the moment a
point light enters the recipe. Handing the builder an already-offset root **cannot desynchronise,
because there is nothing to keep in sync.**

⚑ **Why the station and not the world origin. Measured, not assumed:** `player_station` reports
`player_moves = false` with x = y = 0 across all **3,732** samples, so on THIS trace the station IS
the origin and the two choices coincide. **They coincide by accident of this baton.** Homing to the
station is what makes both arms see the venue from the same *relative* pose under a subject-locked
camera — the whole of R-15 — and it survives a trace where the caster stands elsewhere.

### 5c. The arena's own venue is HIDDEN, not freed

| node | disposition |
|---|---|
| `ArenaFloor` (the GL-13 `PlaneMesh`) | `visible = false` |
| `ArenaSkirtDress` (400 m dress plane) | `visible = false` |
| `Key`, `Fill` (DirectionalLight3D) | `visible = false` |
| `Env` (WorldEnvironment) | **removed from the tree, referenced in `_venue_parked`, never freed** |

`visible = false` takes a mesh out of rendering **and out of shadow casting**, while leaving
`kc2_arena.floor_mesh` / `.skirt_mesh` valid — `kc2_arena_smoke.gd` asserts both non-null and
`kc2_cpa_stills.gd` toggles the floor's visibility. **Freeing them would have made this change reach
two files it has no business reaching.** A `WorldEnvironment` is not a `VisualInstance3D` and cannot
be hidden, so it is removed and parked: **removed, referenced, never freed and never dangling.**

---

## 6. EFFECT CONFIG — the HITL treatment, read from the sidecar, not from the source

| key | value |
|---|---|
| `cut_per_rev` | **17** |
| `density_target_cuts_per_rev` | `11.0` |
| `weapon_scale` | `1.95` |
| `grip_frac` / `grip_seat_m` | `0.2` / `0.1` |
| `undulate` | `true` — **segment B, the shipped default cadence (R-CPB-14)** |
| `epoch_count_in_window` | `36` |
| `palette` | ONE RAMP, FOUR CONSUMERS (R-CPB-13): white-hot (1.00, 0.97, 0.90) → orange (1.00, 0.42, 0.06) → red (0.98, …) |
| `clk1_diagnostics` | `anim: true · fx: true · phaselog: false · shipped_configuration: true` |

**Rig:** Undead Knight FBX + warhammer, head/helmet attachments, `WEAPON_SCALE 1.95`.
**Not one parameter of the effect was touched by this wave.** `kc2_player_channel.gd` is byte-identical
to its state before the port (hash in § 3).

---

## 7. CAPTURE WINDOW — the arithmetic, not the claim

| item | value |
|---|---|
| shot | `canon` |
| tick window (full) | `1570.0 → 1700.0` = 130 ticks = **10.6122448979592 s** of trace |
| `tick0_is_shot_default` | `true` — no `--tick0` override; the window starts at the shot's own first tick |
| tick period | `0.0816326530612245` s |
| fps | **60** (`fps_default_const` 30.0 — the record's rate, unmoved as the default) |
| delivered frames | **210** |
| captured trace | 210 / 60 = **3.500000 s**, i.e. ticks `1570.000 → 1612.875` |
| preroll | **60** CLK-1 tick-frozen warm-up frames, rendered then pruned before the encode |
| encode | `libx264 · yuv420p · crf 18` — **the B-arm's crf, so neither arm is favoured** |

⚑ **Why 3.5 s and not the whole window.** The B-arm captures `0.20 s → 3.70 s` at 60 fps = 3.500 s =
210 frames. Matching it frame-for-frame is what lets the side-by-side clamp be **arithmetically
inert** rather than a crop.
**DECLARED, NOT BURIED:** the canon shot's full window at 60 fps is **~640 frames**. This is its first
210. `DELIVER=0` renders the whole window and costs ~1.2 GB more of intermediates.

---

## 8. THE GROUND GATE — what was consumed, and what was NOT

```
[cpb] camera gate: PASS (9 rays)
[cpb] ⚑ VENUE SWAP — arena gate's SKIRT leg NOT consumed (it tests a hidden 400 m skirt
      + a fog mode this env does not have). DESCEND leg consumed: 0/9 rays fail to descend.
[cpb] VENUE COVERAGE: max ground radius 19.1788 m · fight disc r 16.00 m · pack stage r 26.00 m ·
      rays outside pack stage 0/9 · descend failures 0/9
```

⚑ **`Kc2Arena.camera_ground_gate` IS ANALYTIC AGAINST THE ARENA SKIRT AND NEVER TOUCHES A MESH.** It
solves nine frustum rays onto y = 0 and asks whether each hit lands inside `SKIRT_HALF_M` (400 m) or
past `FOG_DEPTH_END_M` (260 m). **After the swap it would return `PASS` on the strength of a 400 m
skirt that is not being drawn and a depth-fog saturation the lift environment does not have.** A check
that runs, returns cleanly, and has stopped answering the question. See **F-1** in the completion
record.

**So the legs are separated, in the code, in the open:**

| leg | standing under a venue swap |
|---|---|
| **DESCEND** — "the ray never reaches the ground plane" | **CONSUMED.** Venue-independent geometry. Still a HALT. `0/9` failures this run. |
| **SKIRT** — "the hit lands inside 400 m or past 260 m of fog" | ⛔ **NOT CONSUMED.** Vacuous once the skirt is hidden. |

Replaced by `_venue_coverage`: the same nine rays, measured against the radii **this** venue has.
It **REPORTS rather than refuses** — the composition call at this camera is Matt's (W2 F-4, ruled at
R-18d), and the B-arm has already rendered 210 frames of this venue at this exact camera without void
in frame. **A measurement, not a verdict.**

---

## 9. THE AB CUT (TASK 3) — derived from this arm and the B-arm

| cut | path | stream (read off the bytes) | sha256 |
|---|---|---|---|
| **sequential** | `/Users/admin/Games/reincarnated-godot/harness_logs/w2b_ab_cut/w2b-ab-sequential-A-then-B-plk0665-cathedral-1920x1080.mp4` | 1920×1080 · 60/1 · **456 frames** (210 + 36 seam + 210) · 3,933,946 B | `f82607763cc6b8f11b738a6290f35878b266809aed32ed6c433763275b4331ec` |
| **side-by-side** | `/Users/admin/Games/reincarnated-godot/harness_logs/w2b_ab_cut/w2b-ab-sidebyside-AB-plk0665-cathedral-3840x1080.mp4` | **3840×1080** · 60/1 · **210 frames** · 3,817,955 B | `74a523ea2c7de3db3b2d67322272419f49bc34c447b8d31abb6ac1d1f1104ce8` |

Receipt: `…/harness_logs/w2b_ab_cut/ab_cut_receipt.txt`. Reproduce with
`bash scripts/run_w2b_ab_cut.sh`.

- **`CLAMP = min(210, 210) = 210`, counted off both streams**, never assumed from the invocations.
  The W1 lesson: `hstack` runs until its LONGEST input ends and holds the exhausted one on its final
  frame, so an unclamped stack shows a frozen arm beside a running one and reads as a rendering fault.
- **Native resolution, no scale.** Downscaling a side-by-side is how a depth judgement gets made on a
  texture that is no longer there — and depth/texture/juice is the entire rubric.
- **Labels are PIL-rasterised PNGs composited with `overlay`.** Measured: this host's ffmpeg is built
  **without libfreetype**, so every `drawtext` filter fails at graph-build time. One labelled clip
  beside one unlabelled fallback is exactly the silent divergence a viewing artifact must not have.
- ⚑ **Both cuts are a SECOND ENCODE GENERATION of both arms**, with identical settings so neither is
  favoured by the compositor. **The artifacts of record are the two arm mp4s and their sha256s.
  Nothing is measured on the cut.**

---

## 10. WHAT IS *NOT* PINNED, STATED RATHER THAN IMPLIED

- **GPU determinism across hosts is not claimed.** The trace clock (GL-18), the digest-verified baton,
  the seeded skirt and the frozen parameters make this reproducible **on this host with this binary**.
  CLK-1 measured a one-time renderer transient over frames 16–25 on a related scene; the 60-frame
  tick-frozen preroll is the measured bound that covers it, and it is pruned before the encode.
- **The Synty pack version is pinned only by repo state.** `Assets/` is not hashed here; the pack is
  vendored and unmodified, and `git checkout c029c03` restores the tree that produced these frames.
- **x2 determinism was NOT run on this arm.** The B-arm was not x2'd either; the AB cut is a first
  look for Matt's eye, not a certified deliverable. Stated so that its absence is a declared deferral
  rather than a waiver by omission.
- **The `harness_logs/` capture dir is untracked**, following the B-arm's precedent. `render.txt`,
  the sidecar and `prune_receipts.txt` live beside the mp4; the hashes above are what travels.
