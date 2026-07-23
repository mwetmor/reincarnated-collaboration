# KT-4 Twin Verification Captures — galadriel

**Run:** KING-TWIN (conductor: gandalf `RUN-CONDUCTOR`). **Gate:** KT-4 verification-capture lane (fired KTL-6).
**Author:** galadriel (visual-perception + verification-capture seam). **Date:** 2026-07-23.
**Consumes into:** KT-5 (Matt's twin verdict). This is an **EVIDENCE package for Matt's eye**, not a
rubric-grade similarity benchmark (per invocation — rubric scoring NOT required at this gate).
**Godot repo state:** `1a25caa` (drax KT-4), READ-ONLY — I ran scenes, wrote/committed nothing there.
**Godot binary:** `/Applications/Godot.app/Contents/MacOS/Godot` (Metal, off-screen).

---

## 1. What this lane proves that headless smoke cannot

drax's KT-4 headless smoke is GREEN (0 errors / 0 leaks) but **proves structure, not pixels**. Two
things are verified ONLY here, under Metal:

- **The element aura (criterion 3) exists under Metal.** It is *suppressed* in the headless `--smoke`
  path (drax's `enable_aura` opt-out — the third-party Binbun `.gdshader` throws a harmless
  RendererDummy shutdown-accounting artifact there). Every visible render keeps it. My captures are the
  aura's only existence proof under Metal. **CONFIRMED — numerically (see §3, criterion 3).**
- **The near-black king void (criterion 4) applies in playback, NOT pale.** A prior KT-3 frame showed a
  pale off-arena void (KTL-5 SCENEWRIGHT eye-note); drax asserted the runtime WorldEnvironment fixes it.
  **CONFIRMED — numerically: off-arena void samples (26.0, 28.0, 33.0) vs king-register spec
  (25.5, 28.0, 33.2). Essentially exact.** (see §3, criterion 4.)

---

## 2. Per-criterion verdict table (playback TWIN vs king EXEMPLAR)

| # | Criterion | Verdict | What the pixels show |
|---|-----------|---------|----------------------|
| 1 | **Synty mesh, no capsules** | **PRESENT** | Every entity is an articulated Synty humanoid rig — upright in formation (bowazon t6 arc; frost-blades t68 flanks), toppling as corpses (t51 crops). Zero capsule/cylinder proxies in any frame. drax's `SWAP_SUMMARY` (41 rig / 0 proxy / 17 distinct mob meshes) confirmed by eye. |
| 2 | **Weapon prop in hand socket** | **PRESENT** | Best-resolved in `crop_frostblades_tick68_mob_props.png`: a bone rig holds a distinct staff/spear shaft; a second rig holds a teal-bladed weapon. `crop_bowazon_tick51_player_prop.png` shows a toppled rig with an elongated polearm prop. Props are parented and posing in the hand-local frame. NOTE: at orbit zoom the slender bowazon bows read thinner than the frost-blades staffs/blades — props are visibly present on rigs; the *exemplar* (king's held greatsword) is the fidelity anchor. |
| 3 | **Element aura (tinted, under Metal)** | **PRESENT** | Player rig stands in a dense volumetric tinted aura column. Bowazon reads **GREEN** (peak pixel (51,229,64), footprint 20,663 strong-green px) — the REPLICA-1 bridge default (element-derived tint), **expected, not a defect** per KTL-6. The five ruled pilot tints activate when compiled-kit frames land (later gate). Exemplar aura is GOLDEN (`basic_area_vfx_01` + `aura_clip` interior-scissor) — same grammar, different tint. |
| 4 | **King lighting + camera register** | **PRESENT** | Off-arena void **numerically near-black** (26.0,28.0,33.0 ≈ spec 25.5,28.0,33.2 = bg 0.10,0.11,0.13). Long directional **rake shadows** from Key −22°/28° E2.4 clearly cast across the lit floor (sharp in the t51 player crop). Glow ON (aura haloes bloom). Arena floor bright (151,138,125) against dark void = register working. **The prior pale-void concern is RESOLVED in my captures.** |
| 5 | **Synty floors + walls** | **PRESENT** | Dressed dungeon arena: tiled stone floor, arched-arcade walls, pillars, arch, sparse bone/ribcage deco at edges. No procedural flat placeholder inside the 30×30. drax's `ARENA_SUMMARY (crit4=true crit5=true)` confirmed by eye. |

**Aura + void — the two headless-blind criteria — are the strongest confirmations, both numeric.**

---

## 3. Numeric verification (defensible, reproducible)

Sampled with PIL on `playback_bowazon_tick51_dense.png` (1920×972):

- **Criterion 4 (void):** four off-arena-void boxes → `(26.0,28.0,33.0)` ×3 corners; bottom-left slightly
  lighter `(35,37,41)` = the sunk backstop grid-plane catching a sliver of key light near frame edge
  (minor KT-5 taste item, NOT a pale void). King-register spec bg `Color(0.10,0.11,0.13)*255 =
  (25.5,28.0,33.2)`. **Match.** Arena floor for contrast: `(151.2,138.4,125.1)`.
- **Criterion 3 (aura):** peak-green pixel `(51,229,64)` at (x=699,y=463); aura-core 30×30 avg
  `(105,134,106)`; **20,663 px** with greenness (G−max(R,B)) > 40 = a real volumetric column, not stray
  pixels. Rendered under Metal — the criterion headless suppresses.

---

## 4. Capture inventory + exact reproduce commands

All under `agentic_orchestration/galadriel/captures/2026-07-23-kt4-twin/`. Frames dir (REPLICA-1,
default): `agentic_orchestration/gamora/notes/replica1-frames/`. PNGs land at
`~/Library/Application Support/Godot/app_userdata/reincarnated-godot-spike/<prefix>_tick<N>.png`, then
copied in with tick-meaningful names.

### Playback (the TWIN) — `replica_playback.tscn`, Metal, off-screen

| File | Fight | Tick | State | Reproduce |
|------|-------|------|-------|-----------|
| `playback_bowazon_tick06_forming.png` | d2-bowazon blind seed22 | 6 | fight forming (arc) | `Godot --path ~/Games/reincarnated-godot scenes/replica_playback.tscn --quit-after 240 -- --capture --capture-tick 6 --capture-prefix kt4_playback_bowazon --fight replica-d2-bowazon__blind__encounter__seed20260722.ndjson` |
| `playback_bowazon_tick25_mid.png` | d2-bowazon blind seed22 | 25 | mid-fight | …`--capture-tick 25 --capture-prefix kt4_playback_bowazon --fight replica-d2-bowazon__blind__encounter__seed20260722.ndjson` |
| `playback_bowazon_tick51_dense.png` | d2-bowazon blind seed22 | 51 | late/dense (primary) | …`--capture-tick 51 --capture-prefix kt4_playback_bowazon --fight replica-d2-bowazon__blind__encounter__seed20260722.ndjson` |
| `playback_frostblades_tick37_mid.png` | poe1-frost-blades blind seed22 | 37 | mid (2nd roster) | …`--capture-tick 37 --capture-prefix kt4_playback_frostblades --fight replica-poe1-frost-blades__blind__encounter__seed20260722.ndjson` |
| `playback_frostblades_tick68_dense.png` | poe1-frost-blades blind seed22 | 68 | late/dense (2nd roster) | …`--capture-tick 68 --capture-prefix kt4_playback_frostblades --fight replica-poe1-frost-blades__blind__encounter__seed20260722.ndjson` |

- Bowazon runs ticks 0–55 (56 tick-records, 40 mobs +1 player); frost-blades ticks 0–74 (75, diff roster).
- **Crops** (sharp, `extract` + `resize nearest`, from `playback_bowazon_tick51_dense.png` /
  `..._tick06_forming.png` / `playback_frostblades_tick68_dense.png`):
  `crop_bowazon_tick51_player_prop.png` (left560 top330 340×340 →1020) ·
  `crop_bowazon_tick51_mob_props.png` (left1250 top230 420×360 — landed on void, non-load-bearing) ·
  `crop_frostblades_tick68_mob_props.png` (left1150 top140 460×360 →1380 — **best hand-prop read**) ·
  `crop_bowazon_tick06_arc_rigs.png` (left430 top250 560×280 →1400).

### Movie (the auto-battle Matt presses play on)

| File | Reproduce |
|------|-----------|
| `playback_bowazon_autobattle.mp4` (1920×1080, H.264, 7.0s @60fps, 1.2MB) | `Godot --rendering-driver metal --path ~/Games/reincarnated-godot scenes/replica_playback.tscn --write-movie /tmp/kt4_movie/kt4_bowazon.avi -- --movie --fight replica-d2-bowazon__blind__encounter__seed20260722.ndjson` → then `ffmpeg -y -i /tmp/kt4_movie/kt4_bowazon.avi -c:v libx264 -crf 26 -preset medium -pix_fmt yuv420p -movflags +faststart <out>.mp4`. (Movie mode auto-plays @1x from tick 0, holds tail, quits: `420 frames at 60 FPS`, `Done recording`.) |

### King EXEMPLAR — `exemplar/`, Metal, off-screen

| File | Source | Reproduce |
|------|--------|-----------|
| `king_exemplar_idle_fullbody.png` | `shoot_king_closeup.tscn` (full-body, golden aura column, HELD greatsword, crown/cape) | `Godot --rendering-driver metal --path ~/Games/reincarnated-godot scenes/shoot_king_closeup.tscn --quit-after 240 -- --outdir=harness_logs/king_exemplar_kt4_2026-07-23` → copied from `harness_logs/.../king_idle.png` |
| `king_exemplar_closeup_front.png` | same harness | `.../king_closeup_front.png` |
| `king_exemplar_walk.png` | same harness | `.../king_walk_frame.png` |
| `king_exemplar_walk_side.png` | same harness | `.../king_walk_frame_side.png` |

**Side-by-side pointer for Matt (KT-5):** open `exemplar/king_exemplar_idle_fullbody.png` (the golden-
aura King twin-target) beside `playback_bowazon_tick51_dense.png` (the green-aura dressed playback). Same
visual grammar: a Synty rig, holding a prop, standing in a tinted interior-clip aura column, under a
near-black king-register void with long rake shadows, in/against Synty dungeon dressing.

---

## 5. KT-5 taste items — NOTED, not judged (for Matt's brief to point at)

Per invocation §5, surfaced for Matt's eye (these are taste calls at KT-5, not defects):

1. **Rig brightness under king ambient.** Under the ambient-E0.8 / single-Key register, mob rigs read
   somewhat dark/silhouetted from the orbit distance (visible in all wide frames). The exemplar King is
   bright because he is bathed in his own golden aura light; the un-aura'd starter mobs (aura reserved as
   elite marking per KTL-3 Fork 2) get only the register lighting. Whether the mobs want a fill/brighten
   is Matt's call.
2. **Large ribcage deco piece.** The cream bone/ribcage element at the arena edge (left of
   `crop_frostblades_tick68_mob_props.png`; top-left of most wides) is count-sparse (Fork 3) but large in
   scale. Scale is Matt's taste call.
3. **Sim-grid / backstop beneath the dressed 30×30.** The sunk flat-plane backstop's grid lines show in
   the near-black void beyond the dungeon floor (the faint lattice in `crop_bowazon_tick51_mob_props.png`
   and frost-blades t68 crop). Off-arena, behind the register void — noted for Matt.

---

## 6. Deviations LOGGED (per invocation: never silently skipped)

- **DEV-1 — king-EXACT-register exemplar frame not captured; substituted + evidenced otherwise.**
  `probe_king_mcp.tscn` (the exemplar at the *identical* register the playback applies) is a persistent
  never-quit scene with no capture affordance. Attempts to capture it without writing into the READ-ONLY
  godot repo failed: `--write-movie` on that scene wrote 0 frames / early-exited (its script fights the
  movie flags); a self-quitting register-shot harness authored in **my own** pipeline tree
  (`kt4_king_register_shot.gd`) could not be loaded as a main scene from outside the godot project root
  (Godot `res://`-root strictness; `--script` on a `Node`/`_process` harness does not drive the tree).
  Pushing further would have required writing a script INTO the godot repo — which I will not do
  (READ-ONLY). **Resolution (defensible):** criterion 4 is a property of the TWIN, and I evidence it
  *directly in the twin's own pixels* — numerically matched to the register spec (§3) + eye-confirmed
  rake shadows/glow. The king EXEMPLAR is supplied via `shoot_king_closeup` frames (canonical King
  deliverable: mesh + crown + cape + HELD sword + golden aura column), which anchor criteria 1–3 at max
  fidelity. The non-working harness files were removed to keep the tree clean.
- **DEV-2 — texture import-mode warnings (non-fatal, cosmetic).** Every capture run prints
  `WARNING: Loaded resource as image file, this will not work on export` for a handful of Synty textures
  (`PolygonZombieBoss_Texture_04_A.png`, `PolygonDarkFantasy_Texture_01_A.png`,
  `Dungeons_Texture_01_A.png`) sourced from `mob_rig.gd:226` / `king_rig.gd:870`. These are import-mode
  warnings (textures loaded as raw image resources rather than imported), NOT errors — every fight LOADS
  with `parse_errors=0`, all rigs render, and captures succeed. Surfaced for drax's awareness as an
  export-time (not runtime) discipline item; does not affect KT-4/KT-5 visual verification.
- **Expected artifact (NOT a deviation):** capture runs carry the Binbun `ParticlesShaderRD`/shader
  shutdown line at exit under Metal (KTL-6 diagnosis: RendererDummy shutdown-accounting on the aura
  `.gdshader`). Ignored per invocation — the evidence is the PNGs, all `err=0`.

---

## 7. Verdict summary

**All five twin criteria PRESENT in the KT-4 playback** — mesh (1), hand prop (2), tinted aura (3),
king register (4), Synty floors+walls (5) — with criteria 3 and 4 (the two headless-blind ones)
confirmed **numerically** under Metal. Second roster (frost-blades) corroborates mesh-variety + props.
The dressed auto-battle is the twin of the king exemplar's visual grammar. **Present-and-assembled is
confirmed; whether it reads as *belonging in the king's world* is Matt's KT-5 verdict.**

The Mirror was set on the fight and on the King both. They stand in the same near-black; the same light
rakes across them; each holds its arm and each is wrapped in its own coloured fire. The playback wears a
green flame where the King wears gold — a younger light, but the same kind of light. What remains is not
whether they are kin, but whether Matt names them twins.

**— galadriel, 2026-07-23**
