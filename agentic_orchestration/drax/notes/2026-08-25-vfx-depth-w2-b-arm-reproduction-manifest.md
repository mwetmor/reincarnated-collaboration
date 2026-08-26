# VFX-DEPTH W2 — B-ARM REPRODUCTION MANIFEST (twin + 4a, Cathedral)

**Date:** 2026-08-25 · **Agent:** drax · **Authority:** charter R-15 (Matt: *"we should have the logs so that we can reproduce it exactly"*)
**Class:** evidentiary note · **Status:** CURRENT
**Arm:** B — the clean-room twin whirlwind WITH the W1 `4a` spin-following-scuff treatment, in the Cathedral, at the ratified judging camera.

> **The standard this file is written to.** Matt's requirement is *reproduce it exactly*, so
> everything below is either a **hash**, a **verbatim log line**, or a **literal invocation**.
> Where a value is derived, the derivation is shown. Nothing here is "approximately".

---

## 1. THE ONE-LINE REPRODUCTION

```bash
cd ~/Games/reincarnated-godot
git checkout 27baafc
SNAP=/tmp/frozen_run_wwcr_w2_b.sh
cp scripts/run_wwcr_stage.sh "$SNAP"          # sha256 must be 4c06c106…745978
env REPO="$PWD" ARMS=gate CAPTURE=seq CAM=player_lock PLK=0.665 STAGE=cathedral \
    bash "$SNAP" 2026-08-25-w2-bcath
```

**Launch from a frozen copy, not from the in-tree script.** `bash` reads a running script lazily by
byte offset; editing it mid-run shifts every offset after the edit and the interpreter resumes at a
position that no longer means what it meant. It does not necessarily error — it can mis-parse into
something that RUNS.

---

## 1a. THE ARTIFACT THIS MANIFEST REPRODUCES

| # | file | bytes | sha256 |
|---|---|---|---|
| **fx ON** | `/Users/admin/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25-w2-bcath/plk06650_cathedral_fxon.mp4` | 2,250,003 | `19d5e9c29dbc67cbdaf8100d6362b210568f77487529153e4d49219327bf117b` |
| **control** | `/Users/admin/Games/reincarnated-godot/harness_logs/wwcr_2026-08-25-w2-bcath/plk06650_cathedral_fxctl.mp4` | 2,179,910 | `f8434eb643c3e24b5e810e1fdb9a66ebfdc97675977d4e145f5ae6d558c7f44c` |

Both `ffprobe`-verified: **h264 · yuv420p · 1920 × 1080 · 60/1 fps · 210 frames · 3.500 s**.
`FRAME_CENSUS rendered=420 delivered=420` — no shortfall, no stale frame.

**The control is rendered WITH the arm, not borrowed.** Same pose, same rotation, same venue, VFX
layers hidden. It is the only valid occlusion baseline: diffing against "no whirlwind at all" would
measure the caster's pose rather than the effect.

**Filename note:** the venue is in the name (`…_cathedral_…`) by construction. A Cathedral frame and a
bare-plane frame are not comparable — every band statistic, occlusion count and luma threshold moves
with the background — so the harness makes them unable to collide on a filename.

---

## 2. BINARY + HOST

| item | value |
|---|---|
| Godot | **4.6.3.stable.official.7d41c59c4** |
| renderer | `--rendering-driver metal` (Forward+, Apple Metal) |
| host | macOS 24.6.0, Apple silicon Mac Mini |
| resolution | **1920 × 1080** — the stage's `RES`; Godot's Movie Maker locks to `project.godot`'s viewport and ignores per-run overrides (measured at WW-4a v2) |

---

## 3. SOURCE PIN — sha256 of every file that authored a pixel

| file | sha256 | role |
|---|---|---|
| `scripts/wwcr_whirlwind.gd` | `ce2204524a09bc5ac747b0db3050cdf0bc8e55b832b04c55249f0767d15de8b4` | **the twin effect — the certified artifact** |
| `scripts/wwcr_stage.gd` | `970658bdd49bb1f8ad8c464a3ca9af7d9adf77c198044fb4809d27cae7f35ec9` | stage, camera, capture |
| `scenes/wwcr_stage.tscn` | `ddcdddeb96f5c0299732090d49d6e645708b68b122cb18023502404605968c36` | scene |
| `scripts/s2_stage_env.gd` | `65354ef1c82b25e466fde916c289103407be35f247ba0cd54af47b6ea00d913c` | **the Cathedral venue + the W2 fight-surface extension** |
| `scripts/run_wwcr_stage.sh` | `4c06c1067267c29bd844701e7a92e6a99495beddc2c24bf525bb29e2be745978` | harness (= the frozen copy, verified equal) |

**Repo state:** `reincarnated-godot` @ **`27baafc`**, pushed to `origin/main`.

⚑ **The effect is BYTE-UNCHANGED from the W1 `4a` landing.** Verified, not asserted:

```
$ git diff --stat fde563c..HEAD -- scripts/wwcr_whirlwind.gd scenes/wwcr_stage.tscn scripts/wwcr_stage.gd
    -> EMPTY
```

So the B-arm is **W1's clip-3 article in a new room, and nothing else moved.** Every difference
between W1 clip 3 and this file's output is attributable to the venue alone.

---

## 4. CAMERA RECEIPT — verbatim from `render.txt`, rendered IN THE CATHEDRAL

```
[wwcr] PL-PIN unscaled offset (14.7262048721313, 28.3970108032227, 13.7826108932495) m
       vs pl_audit.json (14.7262048721313, 28.3970108032227, 13.7826108932495) m
       — |delta| 0.000000000000 m, z_player delta 0.000000000000 m, tol 0.000010000000 m — MATCH
[wwcr] PL-CAM k=0.665000 — DOLLY only. pitch 52.9535411256029 deg  yaw 47.0 deg
       fov_v 31.7861018306101 deg VERTICAL/KEEP_HEIGHT  z_player 34.8165340347471 m
[wwcr] PL-CAM offset k=1 (the PORT, pinned above) = (14.7262048721313, 28.3970108032227, 13.7826108932495) m
       stand-off 34.8311882019043 m  height 28.3970108032227 m
[wwcr] PL-CAM offset k=0.665000 (THIS RUN) = (9.7929267883301, 18.8840122222900, 9.1654367446899) m
       stand-off 23.1627407073975 m  height 18.8840122222900 m
[wwcr] PL-AUDIT anchor: subject ground projects to frac (0.501041571299, 0.550925191243);
       expected (0.501041450500, 0.550925123427);
       delta (0.000000120799, 0.000000067817) frac = (0.0002, 0.0001) px at 1920 x 1080
```

**`|delta| 0.000000000000 m` — W1's bar, met in the new venue.** Every dispatched parameter is
present verbatim: stand-off **23.1627407073975 m** · pitch **52.9535411256029°** · yaw **47.0°** ·
fov_v **31.7861018306101° VERTICAL / KEEP_HEIGHT** · anchor frac
**(0.501041450500488, 0.550925123426649)** · **k = 0.665**.

⚑ **The anchor audit is a real test in the Cathedral and not a formality.** The offset solves the
subject's ground point onto the measured anchor ray at depth `zp`; the venue change moves the entire
world around the subject. Had the fight-surface extension shifted the derived floor plane, the anchor
would have moved. It moved **two ten-thousandths of a pixel** — single-precision residue, the same
figure W1 recorded on the bare stage.

---

## 5. STAGE CONFIG — the Cathedral, as built

Read from `STAGE_META` in `render.txt` (the builder measures the live scene tree; none of this is
asserted).

| key | value |
|---|---|
| `recipe` | `cathedral` |
| `geometry_source` | `…/PolygonDarkFantasy/Scenes/Demo_Cathedral_01.tscn :: Cathedral section` |
| `arena_center_source` | DERIVED — AABB centre of the largest `Ritual_Circle` mesh (`SM_Prop_Ritual_Circle_01 (2)`), footprint 73.60 m² |
| `arena_center_derived` | `[0.06, 1.593, -32.15]` |
| `floor_y_derived_m` | `1.593` |
| `stage_radius_m` | `26.0` |
| `offstage_meshes_culled` / `onstage_meshes_kept` | `6561` / `834` |
| `ceiling_meshes_culled` / `ceiling_cut_m` | `283` / `7.5` |
| `inherited_lights_total` / `kept` | `29` / `1` |
| `pack_particle_emitters_disabled` | `0` |

### 5a. The fight-surface extension (W2 Task 1 — Matt's scene order)

| key | value |
|---|---|
| `fight_surface_r_m` | **`16.0`** |
| `fight_tile_donor` | `SM_Bld_Base_Floor_Combined_01 (260)` — the NEAREST matching instance |
| `fight_tile_pitch_m` | `[2.5, 2.5]` (measured off the donor's mesh AABB × its world scale) |
| `fight_tile_top_offset_m` | `0.0081` |
| `fight_tiles_laid` | **`126`** |
| `fight_tiles_skipped_existing_floor` | `3` |
| `fight_rock_donor` | `SM_Env_Rock_01 (255)` |
| `fight_skirt_rocks_placed` | **`148`** |
| `fight_skirt_seed` | **`20260825`** |
| `fight_skirt_flanks` | `[{r:14.8, y:+0.35, s:0.55, n:56}, {r:16.8, y:−1.4, s:1.05, n:40}, {r:18.6, y:−5.0, s:1.60, n:30}, {r:19.4, y:−10.5, s:2.10, n:22}]` |
| `fight_surface_nodes_added` | `274` |

**Radius derivation** (both demands stated, the binding one named): the judging camera frames ground
between depression 68.847° and 37.061°, i.e. `18.8840 / tan(68.847°) = 7.31 m` to
`18.8840 / tan(37.061°) = 24.98 m` from nadir = **17.68 m of depth**; and the cast translates at
3.5 m/s across the 0.20–3.70 s window = **12.25 m of travel** while the lock dollies with it. **The
travel binds.** 16.0 m clears it with margin and fits inside `STAGE_RADIUS_M` = 26 m by construction.

**Determinism of the skirt:** one `RandomNumberGenerator`, `seed = 20260825`, no other consumer. Two
builds place identical rock.

---

## 6. EFFECT CONFIG — `4a`, from the runtime `selfcheck()`, not from the source

| key | value |
|---|---|
| `scuff_entrain_frac` | `0.1` |
| `scuff_drag_tau_s` | `0.09` |
| `scuff_v0_at_full_w_ms` | `5.52134908868406` |
| `scuff_travel_predicted_m` | `0.453801395134981` |
| `scuff_arc_predicted_deg` | `7.39712793126117` |
| `scuff_color_rgb` | `[0.620000004768372, 0.600000023841858, 0.560000002384186]` |
| `scuff_is_tinted` | `false` |
| `tinted_surfaces` | `["TrailRibbon", "ContactSpark"]` |
| `tinted_count_is_2` | `true` — **R-9's assert PASSED on this render** |

**Element:** `wind`. **Capture window:** `--seq-from=0.20 --seq-to=3.70 --seq-every=1`, `SEQ_FPS=60`.

---

## 7. WHAT IS *NOT* PINNED, STATED RATHER THAN IMPLIED

- **GPU determinism across hosts is not claimed.** The clock pin, the seeded RNG and the frozen
  harness make this reproducible **on this host with this binary**. A different GPU may differ at the
  sub-LSB level; CLK-1 measured a one-time renderer transient over frames 16–25 on a related scene.
- **The Synty pack version is pinned only by repo state.** `Assets/` is not hashed here; the pack is
  vendored and unmodified, and `git checkout 27baafc` restores the tree that produced these frames.
- **The `harness_logs/` PNGs are gitignored.** `render.txt` (8.5 MB, 424 lines of `[wwcr]` output plus
  the full per-frame census) is the durable artifact and lives beside the capture.
