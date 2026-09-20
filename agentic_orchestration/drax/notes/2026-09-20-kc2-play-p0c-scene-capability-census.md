# KC2-PLAY · P0-c — Astra scene capability census (presentation seam)

> **STATUS:** CURRENT — audit return, read-only. **Author:** drax (presentation seam), 2026-09-20.
> **Dispatch:** gandalf `RUN-CONDUCTOR` prep, run **KC2-PLAY**, P0-c; Matt-authorized 2026-09-20 (Q81 *"Agreed - accept all"*).
> **Authority:** census + recommendation only. **No code written, no Godot launched** (gandalf's C-6/C-7 hold `~/astra-burst/.heavy.lock`, stamped 2026-09-19T11:21 — not contended), **nothing pushed**, nothing in the frozen lane touched.
> **Governing texts:** `2026-09-20-kc2-play-architect-pass.md` (§ 4 table = Matt's ruling of record) · runtime spec `2026-08-25-kc2-mc-w4-godot-runtime-spec.md` (R-1…R-9) · `astra_test_01/burst/HOWTO.md` · `SPEC.md § 7`.
> **Surveyed on disk this session:** `astra_test_01/burst/runs/C-7/cliffside_v45/` (scripts, scenes, sprites, props, vfx, `sockets.json`, README) · `astra_test_01/burst/export/` (`godot_import.py` 6,533 ln, `effect_kit.py` 1,995 ln, `props_layer.py`, `parallax_scene.py`) · `runs/C-5/vfx_kits/kits_v9.json` (19 kits) · `runs/C-7/conductor_scripts/` · `~/Games/reincarnated-godot/` (`scripts/kc2_*.gd` 16,147 ln, `web/build_playtest.sh`, `web/cliffside/export_presets.cfg`) · `agentic_orchestration/galadriel/notes/crucible-arena-geometry-v1.json`.

---

## 0 · The one structural fact that shapes every answer below

**`cliffside_v45/` is a BUILD ARTIFACT, not a source tree.** Every `.gd` in it is emitted from a Python string constant in the exporter:

- `export/godot_import.py:457` — `(out/'scripts/keeper.gd').write_text(KEEPER_SCRIPT)`
- `:1066` — `keeper + _authored_flare_script(...)`, and `:1479` — `keeper + directional + '\nconst VFX_KITS = ' + …`
- the emitted `keeper.gd:378` is a **63,415-character single line**: the generated `VFX_KITS` table.

**Consequence, and it is the whole answer to "exporter work or hand-authored":** a GDScript file hand-edited inside a generated project is destroyed by the next PACK. There is no merge. So the question is never *"which is easier to write"* — it is **"which side of the PACK boundary does this live on."** Anything that must survive a re-PACK is either (a) Python in `export/`, or (b) a **vendored file the exporter copies verbatim and never authors**. Route (b) does not exist today; § 3 recommends minting it, and it is the single cheapest enabling change in this census.

---

## 1 · REUSE — what carries over as-is

### 1.1 The 8-direction cell / SpriteFrames system — **carries whole, unchanged**

`keeper.gd:3` `DIRECTIONS = ["S","SW","W","NW","N","NE","E","SE"]`; facing chosen from the input angle at `:46` (`posmod(roundi(angle/(PI/4))+6, 8)`). The resolution ladder at `:66–105` (`_nearest_animation` → nearest circular direction within state → idle → any state, warn-once, deterministic tie order) is the piece that makes a *placeholder* body safe: a missing cell degrades visibly and loudly rather than blanking. Action states self-return via `animation_finished` with a frame-count fallback timer (`:103–110`) so a mis-authored loop flag cannot wedge the body.

**Keeper is 40/40 cells.** This is the only complete set, which is why F5 is right on the facts. Adopt as-is; the only edit needed is the facing *source* (see § 2, mouse-to-move).

### 1.2 The socket table — **carries whole**

`sockets.json`: `version` / `canvas` / `cells` / `notes`; 8 cells (`cast_E`, `cast_N`, … — cast states only), each `{sockets: [8 per-frame [x,y] or null], measurements: [8 {tip, reason, line_inliers, slope}], release_index: 3, release_socket_rule: "far end along facing (FL-1a)"}`. Read at `keeper.gd:146` and resolved through the **displayed** sprite transform at `:151–160` (`sprite.to_global(point + sprite.offset − texture_size/2)`), never through an E-row rotation. Firing gates on `sprite.frame == cell.release_index` at `:162–168`, and a missing socket **suppresses the cast with a warning** (`:176–178`) rather than firing from a guessed origin.

That last behaviour is exactly the honesty posture R-8 wants, already built. Keep it.

### 1.3 The four VFX grammars — **carry as VIEW; per-instance parameterisation is real**

All four take the kit dictionary **as a call argument**, and each instance deep-copies it (`vfx_g1.gd:80` `config = kit.duplicate(true)`). Every radius/duration/speed is read out of `config` at the use site. **So a caller can compose a kit dict from model values at cast time without touching the exporter.** Signatures:

| | entry point | model-drivable per instance | cited at |
|---|---|---|---|
| **G1** projectile | `vfx_g1.gd:42` `acquire(parent, kit, origin, destination, owner, art_scale)` | `speed_px_s` (`:151` step = `speed_px_s·spell_scale·delta`), `range_px` (`:150`), `pierce` (`:88`), `collision_radius_bh` (`:133`), `head_length_px` (`:134`), `contact_only` (`:146`) | ✅ radius, speed, travel all drivable |
| **G2** field + flipbook | `vfx_g2.gd:89` `acquire(parent, kit, origin, destination, owner, art_scale)` | `radius_px` (`:167` field art scaled to `2·radius_px / used_rect.x`; `:341` in-field membership = `distance_to(ground_point) > radius_px`), `duration_s` / `residue_s` (`:222–223`), `flight_s` **recomputed per instance from actual distance** at `:144` so travel *speed* is preserved, `schedule` (tick list) | ✅ radius, duration, tick cadence all drivable |
| **G3** chain/bolt | `vfx_g3.gd:39` `acquire(...)` | `hop_range_px`, `link_length_px`, `prong_length_px`, `width_px`, `life_s`, `afterimage_s`, `max_links`/`min_links`, `max_branches`, `schedule`, `seed` | ✅ |
| **G4** aura loop | `vfx_g4.gd:17` `acquire(owner_root, kit)`, `:69` `start(kit, owner, refresh)`, `:211` `cancel()` | `radius_px`, `duration_s`, `pulses`/`schedule`, `orbit_period_s`, `petal_life_s`, `release_s` | ✅ **and it has explicit `start` + `cancel`** |

**G4 is the EoR ring, essentially pre-built.** It attaches to the owner, re-acquires without restarting (`vfx_g4.gd:18–22` matches an existing child by `config.name` and calls `start(..., refresh=true)`), and exposes `cancel()`. That is a **held-channel-shaped API already.** Drive the ring's life by `start`/`cancel` from the sim, **not** by handing it a `duration_s` — see the 60-Hz caveat in § 5 R-4.

Authoring-side provenance, for the record: these values come from `kit['effect']['skill_spec']['mechanics']` — `_g4_config` at `godot_import.py:4506–4516` (`radius_px`, `duration_s`, `pulse_schedule_s` → `tick_schedule_report`), `_g2_config` at `:3631–3661`, `_g1_config` at `:1855–1875`.

**One exception, and it is a real one:** G1's `range_px` is **hard-coded `650.0`** at `godot_import.py:1869` — it is not read from the kit. Per-instance override at the call site still works (the value is read from `config`, `vfx_g1.gd:150`), so this is a *default* gap, not a wall. Named so nobody reports it as drivable-from-the-kit without checking.

### 1.4 The model-unit bridge that already exists — **body heights, not metres**

`collision_radius_bh` is in **body heights** and is converted in the generated script by a **hard-coded `130.0`**: `vfx_g1.gd:133` `shape.radius = config.get("collision_radius_bh", 0.25) * 130.0`. G2 instead carries `px_per_bh` in its config (`godot_import.py:3657`, default `130`). So a dimensionless→pixel seam is built and used; it is just **inconsistently plumbed** (one grammar hard-codes the constant, one carries it) and its unit is **BH, not metres**. § 2's projection layer is where metres enter, and § 5 R-2 is where the two scale chains collide.

### 1.5 Capture / probe harness — **carries whole, and it is better than it needs to be**

`cliffside_v45/probe_events.gd` is `extends SceneTree`, loads the real scene headless, synthesises `Input.action_press/release` for kit-cycle + facing + cast, waits a fixed frame budget, then walks the tree collecting **every node exposing an `events` Array** and dumps one JSON line (`PROBE_EVENTS=…`) with targets, wall layers, keeper colliders and per-effect event logs. `probe_cast_ab.gd` (N casts at `CAST_GAP_FRAMES`, `CAPTURE_FRAMES`), `probe_cast_dir.gd` (8-direction sheets) and `conductor_scripts/ab_chain_v45.sh` (import → traces → captures → sheets → realtime + third-speed MP4 → purge frames) complete the chain. Every grammar already carries `static var events: Array` + `_record(event, …)` with an **effect-age frame clock independent of `time_scale`** (`vfx_g1.gd:68–77`).

**This is 80 % of the telemetry recorder already written, in the right shape** — a static event array per emitter, drained by a headless harness. § 2's recorder is mostly a *second consumer* on that pattern, not a new mechanism.

### 1.6 The v1 baton's gate/loader code — **carries as the pattern and partly as code**

`reincarnated-godot/scripts/kc2_baton.gd` (1,111 ln). Directly reusable:

- **`load_file(path, expected_sha256)` `:183–205`** — GL-6 digest-before-load, and the clause that matters: an **empty expected digest is `DIGEST-NOT-DECLARED` → NOT-RUNNABLE, never green** (`:189–191`). Generalising this to the v2 pack's two levels (pack digest, then member digests) is an extension of this function, not a rewrite.
- schema-version fail-closed `:223–226`; `_read_wire_constants()` `:269` (GL-10, absent constant ⇒ named load error, never a default); `census_report()` `:902`; `_declare_absences()` `:946`; `_verify_integrity()` `:1073`; `gate_line()` `:1107`.
- **`actor_position_t(actor_id, tick_f)` `:520`** — GL-7 knot interpolation as a **pure function of a fractional tick**, no accumulator, no velocity integrator. This is precisely the shape F1's render-interpolation rider needs for monsters.

Not reusable: `sim_to_godot()` `:769` and `actor_position_v3()` `:595` are Vector3 (3D seam, retired 2026-09-15) — they become the 2D projection of § 2. And the file's own constitutional law (line 22: *"computes no damage, resolves no hit"*) is exactly what R-1…R-9 invert; the **gates** carry forward, the **posture** does not.

`kc2_player_channel.gd` (4,217 ln) and `kc2_motion.gd` (329 ln) are v1 measurement/animation-binding harnesses against the *recording*; they are lineage, not runtime parts. I would not lift code from them.

---

## 2 · GAPS — what the scene needs that does not exist

Side = **which side of the PACK boundary** it must live on (§ 0). "Exporter" = Python in `export/`, Astra burst lane. "Hand" = GDScript authored outside the generated project (and therefore requiring the vendoring seam of § 3.3). "Data" = a JSON the exporter consumes.

| # | Gap | What exists today | Side | Size |
|---|---|---|---|---|
| **G-a** | **Enemy actor tokens** — tinted silhouette sized by size-class, procedural move-bob / attack-lunge + volley-tick flash / death fade, nameplate for hero/nemesis | **Nothing movable.** The only "enemies" are `props_layer.py:693–699` `VfxTarget_N` — a static `Area2D` in group `vfx_targets` with a `CollisionPolygon2D` footprint, parented under the y-sorted `Actors` node (`:589`). No HP, no state, no motion, no death. | Exporter (token scene + tween library) + Hand (the per-tick driver) | **M** |
| **G-b** | **Projection + y-sort layer** — metres on the arena plane → `(x·ppm, y·ppm·sin53°)`, y-sorted, one place | `y_sort_enabled` exists on the Actors node (`props_layer.py:589`, `godot_import.py:578`) so the *sort* is free. The **projection does not exist at all**; the cliffside is pixels end to end. | Hand (it is runtime law, must not be re-authored by a PACK) | **S** |
| **G-c** | **Arena plate** from the video-measured ring | Nothing. Geometry JSON confirmed present (§ 2.1 below). Cliffside's `parallax/walkable.json` + `blocked` polygons are the *consumption* pattern G2 already reads (`vfx_g2.gd:37–42` `is_walkable`), so the shape of the target object is known. | Data (ring JSON → polygons) + Exporter (plate + wall bodies) | **M** |
| **G-d** | **HUD** — HP globe, energy, wave badge, skill bar with cooldown sweep, buff row, damage numbers | One `Label` (`keeper.gd:383–402`, the VFX kit name + "(Tab)"). That is the entire HUD. Damage-number precedent exists as `vfx_contact_label.gd` (pooled `Label`, `vfx_g1.gd:257–272`) — reusable for floating numbers and for § 2.3's proc labels. | Hand (it reads runtime state every frame; a generated HUD would freeze the contract) | **L** |
| **G-e** | **Held-channel state on the player view** — walk/run cells under a held EoR ring, cast one-shots for Blitz / Vire's / War Cry, flash hit-react, fade death | `keeper.gd:37–43` **zeroes velocity and blocks all input during `cast`/`jump`** — the opposite of MD-B4app-2's walk-while-channelling. G4 supplies `start`/`cancel` (§ 1.3) so the *ring* half is free; the *body* half is a rewrite of the state machine. | Hand | **M** |
| **G-f** | **Mouse-to-move + GD-faithful binds** (RMB-hold EoR, LMB Blitz, keys 2/3/7) | `project.godot` binds WASD/arrows, Space, `cast` on **E or LMB**, Shift run, G gear, Tab kit-cycle. `Input.get_vector` movement (`keeper.gd:44`). No RMB action, no hold semantics, no move-to-cursor, no 2/3/7. Cursor *reading* exists (`get_global_mouse_position`, `keeper.gd:295/305`) with a `vfx_cursor_override` test hook — reusable for a scripted pilot. | Exporter (`project.godot` input map) + Hand (the controller) | **S–M** |
| **G-g** | **Camera2D zoom gate** — GD-matched ≈8 % figure default, house 17 % on a toggle (F4) | Camera2D exists and follows without smoothing (`godot_import.py:480`, `:621–623`), **zoom is a fixed emit-time constant** (`:541` `zoom = max(1536/w, 1024/h)`, reported at `:652–653`). No runtime toggle, no figure-height register, no gate. | Exporter (expose) + Hand (toggle + assertion) | **S** |
| **G-h** | **Telemetry recorder** on the view-contract stream | The emitter pattern is built (§ 1.5) but it is **per-VFX-effect**, not per-run, and there is no single stream, no wall-clock/tick stamping, no session file, no T-B statistics. | Hand | **M** |
| **G-i** | **Restart** (F6: waves 150–160, one life, restart key) | Nothing — the cliffside has no run, so nothing to restart. Trivial once the runtime is a re-instantiable object. | Hand | **S** |

**Top five by size: G-d (HUD, L) · G-a (enemy tokens, M) · G-c (arena plate, M) · G-e (held-channel body, M) · G-h (telemetry recorder, M).**

### 2.1 Arena geometry — **CONFIRMED PRESENT**

```
path    agentic_orchestration/galadriel/notes/crucible-arena-geometry-v1.json
sha256  68d895d75702996473cfd654a9a834816d4be0421c4b5ad7a3d2a0cc5d40481f
bytes   28,899        author galadriel, 2026-08-24, version 1
```

Contents verified: outer ring **177 vertices, closed**, both `vertices_native` and `vertices_m` present; **4** interior obstructions `OB-1…OB-4` (309 / 284 / 67 / 62 native px², 13 / 10 / 6 / 6 vertices) — **not seven; the three phantom pillars are already absent from the file** (§ 7.1 trap 1 is satisfied by the data, not by care); `interpolated_segments: []` with an explicit NONE note; **2 `unwalked_arcs`** (vertices 0→8 and 174→176) carrying `provenance` + `caveat` — flagged, not smoothed (trap 2 satisfied); extent `201 × 269` native px = `39.8 × 53.3 m`; scale `0.1981 m/px`, `DERIVED-WEAK`, band `[0.094, 0.3663]`; frame `+x EAST, +y SOUTH` with an explicit `handedness_note` that **Godot import must flip or rotate and no flip is applied in-file**; 6 green zones (interior point + `radius_upper_bound_px` 23.3–52.0), `polygons: null`, `dot_mechanic.magnitude: null` / `ATTESTED-UNMEASURED`, and `class_note` — *"the Godot arena must NOT collide-block these."*

⚑ **Two figures in the file do not match the runtime spec's § 7 (3) quotation, and the file is the instrument.** Spec says floor **27,875 px²**; file says **29,455** (+5.7 %). Spec says scale **0.198**; file says **0.1981**. Spec describes the four obstructions as *"2 symmetric inner-wall arcs, 2 south-lobe blocks"*; the file describes all four identically as *"unmapped island inside the arena floor."* Not a blocker — I will build from the file and quote the file — but the spec's figure should not be re-quoted forward, and the discrepancy is routed, not absorbed. → conductor / P0-d.

---

## 3 · RUNTIME HOME — recommendation

### 3.1 Where it lives

**`~/Games/reincarnated-godot/kc2_runtime/`** — a new top-level directory, deliberately **not** `scripts/`.

Reasons, in order of weight:

1. `reincarnated-godot/scripts/` holds **638 entries / 16,147 lines of `kc2_*` alone**, almost all one-shot probes, stills harnesses and bake scripts from the retired 3D seam. A combat runtime with normative test vectors dropped into that directory becomes indistinguishable from `kc2_a2d_probe.gd` within one session. A flat namespace is where R-2's census obligation goes to die.
2. The repo is already the right *repo* — it is mine, it is in git, it has the baton lineage (§ 1.6) physically present for lift, and F2 names me.
3. A single directory is what § 3.3's vendoring can address by path and hash.

Proposed shape (names are a recommendation, not a claim about what exists):

```
reincarnated-godot/kc2_runtime/
  loader/      pack_load.gd  digest_gate.gd  precedence.gd  census.gd  absence_ledger.gd   ← R-1, R-2, R-8
  model/       math_rules.gd  channel.gd  skills.gd  dots.gd  controls.gd  crit.gd  leech.gd
  actors/      actor_template.gd  monsters.gd  summons.gd  waves.gd                        ← R-6
  arena/       walls.gd  hazards.gd                                                        ← R-7
  sim/         clock.gd  rng.gd  world.gd  view_contract.gd
  pilot/       scripted_pilot.gd                                                           ← T-A
  tests/       *_smoke.gd  vectors/                                                        ← R-5
  MANIFEST.json   (member list + per-file sha256 + runtime version)
```

**Hard constraint on the whole tree: it must not `preload` a scene, reference a `res://` art path, or touch `Input`.** It is a GDScript library that runs under `--headless` with no `scenes/`. The view contract (world snapshot + event stream out; input intents in) is the only surface. If that constraint holds, the Astra lane can vendor it blind; if it breaks once, the vendoring seam becomes a merge problem.

### 3.2 How it is unit-tested headless — **the convention already exists; use it, don't invent GUT**

There is **no GUT in `addons/`** (24 addons, all 3D/import/VFX tooling). What exists and works is better suited anyway:

```
extends SceneTree                                        # kc2_loader_smoke.gd:1
/Applications/Godot.app/Contents/MacOS/Godot --headless --path . \
    --script scripts/kc2_loader_smoke.gd
```

with three properties worth preserving verbatim:

- **Pinned expectation constants re-measured independently and asserted**, not recited — `kc2_loader_smoke.gd:36–40` (`EXPECT_ACTORS 344`, `EXPECT_WAVES 20`, `EXPECT_KNOTS 1003`, `EXPECT_EVENT_ROWS 1900`), with the file's own comment: *"a silent regression in the loader cannot pass as a green."*
- **Machine-readable artifacts** written to `tmp/kc2/*.json`, small + load-bearing ones committed, regenerable intermediates receipted not committed.
- **A committed, byte-reproducible transcript** with the exact regeneration command and the exact `grep` that drops the two vendor-addon GDExtension errors that are repo baseline.

Also present and worth adopting: `--check-only --script` as a **compile gate with no window** (`scripts/run_boss_v1summon.sh:40`) — a cheap first leg on every runtime commit.

So: `kc2_runtime/tests/*_smoke.gd` as `SceneTree` scripts, one per rule family, `math_rules` vectors driven from the pack's own `test_vectors` (R-5 says they are normative — the suite reads them, it does not transcribe them), plus one `run_kc2_runtime_suite.sh` that fires `--check-only` then every smoke and greps a single `[kc2rt]` prefix. **Smoke definition for this seam, stated so Gate-2 can hold me to it: `--check-only` clean + every smoke green + every `math_rules` test vector reproduced to declared precision + the R-2 census and absence ledger emitted non-empty.**

### 3.3 How the Astra PACK vendors it by sha without a copy drifting — **this is the piece that does not exist yet**

Today the exporter *authors* every script it emits (§ 0). It needs one new capability, and only one:

**`godot_import.py --vendor <dir> --vendor-manifest <MANIFEST.json>`** — copies the tree **byte-for-byte** into `out/kc2_runtime/`, verifies each file's sha256 against the manifest **before** copying, writes the manifest's `runtime_version` + per-file digests into the generated project (a `kc2_runtime_vendored.json` beside it), and **refuses to emit the project at all on any mismatch**. It authors nothing under `kc2_runtime/`; it never opens those files for anything but hashing and copying.

Drift then cannot be silent in either direction:

- **runtime edited, PACK not re-fired** → the shipped project's `kc2_runtime_vendored.json` digests ≠ the source tree's. One `shasum -c` in `verify.sh suite` catches it.
- **vendored copy edited inside the generated project** → digest ≠ manifest, and it is overwritten on the next PACK anyway.
- **PACK fired against a stale runtime** → the manifest's `runtime_version` is stamped in the project and ledgered with the PACK; `HOWTO.md § 4`'s existing "bump N and the kit count" ritual gains one more field.

This mirrors exactly what `kc2_baton.gd:183–205` already does for the baton file, one level up. **It is small (S) and it is the enabling dependency for F2** — without it, "drax builds the runtime, the lane vendors it" has no mechanism and degrades into hand-patching a generated project, which is the failure mode § 0 describes.

### 3.4 Desktop native build (F3)

**There is no macOS export preset anywhere in `reincarnated-godot/`.** The only presets on disk are Web:

- `web/cliffside/export_presets.cfg` — `name="Web"`, `platform="Web"`, `export_path="build/web/index.html"`
- `web/_overlay/export_presets.template.cfg` — `name="Web"`, `platform="Web"`

`web/build_playtest.sh` (6,294 B) is a **Web** pipeline: overlay → `export_presets` from template → headless export → `index.pck` → stage → verified live by independent `curl + shasum` (`HOWTO.md § 7`). Its *structure* — template preset, overlay directory, headless export, post-export digest verification, license fence — ports cleanly to macOS; its *target* does not.

So F3's "desktop native build only" needs a **new `macOS` preset + a `build_desktop.sh` sibling, size S**, plus one decision I do not own: whether the macOS build is **signed/notarised** (Matt's machine, Matt's Gatekeeper) or run from a local unsigned `.app` with the quarantine bit cleared by hand. I recommend the latter for a comparison build — it is the referent's own audience of one — but it is a Matt call and I am flagging it rather than assuming it. Also note `reincarnated-godot/project.godot` currently declares `config/features=PackedStringArray("4.6", "Forward Plus")` and `run/main_scene=res://scenes/sidekick_test.tscn` — a 3D spike's settings. The KC2-PLAY scene must **not** inherit that project file; see § 4.

---

## 4 · PERFORMANCE — tens to low hundreds of tokens + VFX, 2D

**Not a concern at the stated scale, with three specifics.**

**(a) Renderer.** `cliffside_v45/project.godot` runs `renderer/rendering_method="gl_compatibility"` — chosen for the Web deploy, and it is the *wrong* default for a desktop-only comparison build. At a few hundred 2D sprites GL Compatibility is fine on batching grounds, but the four grammars lean on per-instance `ShaderMaterial`s (`vfx_g1.gd:106` `$Head.material = load(config.material)`, plus `_material.gd` binding scripts per kit), and **a distinct material per instance breaks the batch in GL Compatibility specifically.** Forward+ on Metal absorbs this without thought. **Recommendation: Forward+ for the desktop build**, which also lines up with `reincarnated-godot`'s existing `Forward Plus` feature string. No measurement taken — the lock is held; this is a stated expectation, not a result, and the cheapest refuting test is a 200-token spawn scene under both renderers, which I will run when the lock frees.

**(b) The 12.25 Hz tick is a performance *gift*, not a cost.** Sim work runs 12.25×/s instead of 60×/s — a 4.9× reduction in the only O(n²)-shaped work in the build (target selection, AoE membership, DoT timelines). Render interpolation between knots is `lerp` on a `Vector2` per body per frame and is free. **The real cost centre is node count, not tick rate**: a few hundred `AnimatedSprite2D` + tween + `Label` nodes with a y-sorted parent. Mitigations already present in the lane: the G1 pool (`vfx_g1.gd:53–56`, reuse by `scene_file_path` + `active == false`) and the pooled contact labels (`:258–264`). **Extend pooling to enemy tokens and damage numbers from day one** — retro-fitting a pool after the HUD exists is how this gets expensive.

**(c) The quantisation arithmetic, stated because it bites the view and not the sim.** `tick_period_s = 1/12.25 = 81.63 ms` = **4.898 frames at 60 Hz** — deliberately non-integer. Every VFX timeline in the lane is on a **60-Hz frame clock** (`age_frames()` normalises physics frames to 60, `vfx_g1.gd:68–70`, `godot_import.py:1586/2439/3860`; every schedule converts seconds → 60-Hz frames, `vfx_g2.gd:220–223`). So a VFX duration handed in as `duration_s` will **never** land on an exact tick boundary. This does not corrupt the sim — the sim is authoritative and the VFX is decoration — but it directly violates § 2.3's geometry-true clause if we try to express "the ring is up for exactly the channel's active ticks" as a duration. **Drive the ring by `G4.start()` / `G4.cancel()` from the sim** (§ 1.3) and the problem disappears. This is the single most likely place for a builder to ship a subtly-wrong comparison, so it is named here rather than discovered at T-B.

---

## 5 · RISKS, and where I think the ruled design is wrong for my seam

### R-1 · The VFX grammars contain a SECOND hit resolver, and § 2.1 forbids it

G1 resolves contact with **Godot physics**: `PhysicsShapeQueryParameters2D` + `intersect_shape` + `cast_motion` sweeps (`vfx_g1.gd:159–198`), a capsule built from `collision_radius_bh × 130.0` (`:133`), pierce decrement (`:251–255`), a contact ledger, FULL/PARTIAL labels (`:257–272`), and a static cone/range target search over group `vfx_targets` (`:26–40`). G2 tests field membership by `distance_to(ground_point) > radius_px` (`vfx_g2.gd:341`).

**Every one of those is a pixel capsule deciding whether a thing was hit — exactly what the architect pass says must not happen.** Reused naively, the build gets two hit resolvers that disagree, and the disagreement will be *small*, *intermittent* and *invisible in a screenshot* — the worst possible defect in an instrument whose purpose is fidelity comparison.

**Mitigation, and it must be a build rule rather than a habit:** enemy tokens carry **no `CollisionObject2D` and are not in group `vfx_targets`**; every kit dict composed by the runtime sets `contact_only`/`pierce` such that the sweep finds nothing; and the census gate **asserts** it — one headless check walking the token subtree for `CollisionObject2D`/`CollisionShape2D`/`CollisionPolygon2D` and failing red on any hit. That assertion pattern is already built and proven in this project (SKIRT's *"1,430 nodes walked, zero `CollisionObject3D`"*, runtime spec § 7.2). Port it. **Assert it, don't be careful about it.**

### R-2 · Two scale chains disagree, and mine is the one on screen

The lane's unit is **body heights at 130 px/BH** (§ 1.4). The arena JSON's metre scale is derived through a *different* chain: `character_pixel_height 70.0`, `character_height_m_ASSUMED 1.9`, `s_screen_px_per_minimap_px 14.6`, `cos_camera_pitch 0.5` (θ≈60°, bracketed 50–70° by two weak reads) → `0.1981 m/px`, `DERIVED-WEAK`, band `[0.094, 0.3663]` — **a 1.7× spread, explicitly inherited by every metre figure in the file.**

Three things follow, and the third is the one I want the conductor to read twice:

1. **The camera gate is correctly ordered.** R-L91-5 already rules that OE-1 gates on the pin, and F4 sets the zoom by *figure height* (8 % / 17 %) — a figure-relative register that is immune to the metre scale. Good. Keep the figure-relative form; do not restate F4 in metres.
2. **`ppm` (pixels per metre) must be ONE constant in ONE file**, read by the projection and by nothing else, and stamped into every telemetry session and every capture. A 1.7× band means a frame captured before the pin and one after are *different scenes*, and a session file that does not carry its own `ppm` cannot be re-read later.
3. ⚑ **R-L68-2's stated pin METHOD looks unsound, and it lands on my plate as an arena that cannot hold its own bodies.** The method of record is *"register the Class-1 footprint against the final pursuit model's occupancy hull."* The ring is `201 × 269` px. The occupancy hull is `86.915 × 85.303 m`. Matching x requires `86.915 / 201 = 0.4324 m/px` — **above the band's own upper bound of 0.3663.** So the pin as described cannot be satisfied inside the scale's declared uncertainty. The resolution is almost certainly benign and is stated in the spec itself — **the sealed sim was generated wall-less** (§ 7.2, K-7 note), so bodies spread where walls would have stopped them, and the hull is an AABB of that spread plus a 3.0 m sweep radius. But then **the hull is not a valid pin target**, because it measures a world with no walls against a ring that *is* the wall. Pinning to it would inflate `ppm` to fit an artifact of the sealed run's own unboundedness.

   The consequence for my seam either way: at the file's own `0.1981`, the walled arena is **39.8 × 53.3 m**, while the sealed sim's bodies occupied **86.9 × 85.3 m** — roughly **2.2× narrower and 1.6× shorter**. Wave 150–160 densities that were comfortable in the sealed run will be **markedly tighter** on my plate. That is not necessarily wrong (D-CP2-1 ruled walls in on both sides, and *"a sim that never meets a wall cannot tell you what walls do to a fight"* is the point), but it is a **large, predictable, first-order difference between the sealed sim and the runtime, and T-A must expect it rather than discover it as a port bug.** → routed to conductor / gamora (P0-a), not adjudicated here.

### R-3 · § 0 again, as a risk rather than a fact

F2 says "the Astra lane builds the scene and vendors the runtime by sha." The vendoring mechanism does not exist (§ 3.3). Until it does, the only way to get GDScript into the scene is to author it into `godot_import.py` as a Python string — which puts the combat runtime **inside** the codex-burst lane that F2 explicitly (and rightly) says is the wrong grain for it. **`--vendor` is therefore not a nice-to-have; it is the seam that makes F2 executable.** It should be an early, small, own-item TOOLING burst, before any P2 scene work is sized.

### R-4 · The 60-Hz VFX clock vs the 12.25 Hz sim tick

Covered in § 4(c). Stated here as a standing risk because it fails *quietly* and only shows up as a small timing error in exactly the statistics T-B measures (channel uptime 0.838, release duty ≈10.5 %, Type-A onset 1.60 s / duration 1.03 s, Type-B 0.60 s). Build rule: **no combat-relevant duration is ever expressed to a VFX grammar as `duration_s`; the sim starts it and the sim cancels it.**

### R-5 · The frozen lane, and where KC2-PLAY's scene work should actually live

C-7 is frozen (last notice `2026-09-19T03:45:05Z`, MANIFEST `059379a19782`) and holds the heavy lock. The architect pass already names the option — *"takes its own project directory outside the cliffside freeze."* **I recommend that unambiguously.** The Crucible scene shares the *cell system*, the *socket table* and the *four grammars* with the cliffside, and shares nothing else: no parallax cliff, no props layer, no walkable/blocked polygons, no 8-px ambient lattice, no G-switch, no Tab kit-cycle. Growing it inside `cliffside_v*` would couple a fidelity instrument to a taste-round scene that is still moving under `C-7`, and would put KC2-PLAY behind the freeze ritual (`HOWTO.md § 3`) for every runtime iteration. A sibling `runs/<run>/crucible_v<N>/` with its own PACK brief costs one brief and buys full independence.

### R-6 · Pushback on the ruled design — one item, and it is small

**F3 "desktop native build only" is right, and I am not contesting it.** But it silently retires the *only* delivery pipeline this seam actually has (`web/build_playtest.sh` → `index.pck` → staged → sha-verified live, `HOWTO.md § 7`) and replaces it with a macOS preset that **does not exist on disk** (§ 3.4) and a signing question that is Matt's, not mine. That is a small cost paid at exactly the wrong moment — F7 authorises pre-T-A play "as soon as P1 + P2 meet," and on the current asset base the fastest path to Matt's hands is the Web pipeline that is already built, ledgered and proven.

**What I am NOT proposing:** shipping the comparison on Web. F3's reasoning is sound — a browser changes input latency and RMB semantics (the context menu alone), and **a pilot on a different input path is a different pilot**, which is the whole argument F3 makes against WASD.

**What I am proposing** is one sentence of sequencing, not a fork: **build the macOS preset as its own small item early in P2, and do not let the first `feel` session (F7) be the thing that discovers there is no desktop build.** If that item slips, the honest fallback for a *feel-only* session is running from the Godot editor on Matt's Mac — not a Web build, because a Web build would quietly become the thing someone measures. Flagging it now so it is sequenced rather than discovered.

---

## 6 · What this census did not do

- **No Godot launched**, headless or windowed — the heavy lock is held by C-6/C-7 and this audit was scoped read-only. Every performance statement in § 4 is a **stated expectation with its refuting test named**, not a measurement.
- **No code written, nothing committed but this note, nothing pushed.**
- **No size estimate validated against an implementation.** S/M/L in § 2 are my seam's judgement from the surveyed surface area; they are not derived from a spike.
- **R-L68-2 landing status not determined** — that is P0-d (conductor recon). § 5 R-2 (3) raises a question about the pin's *method* that P0-d should carry to whoever owns it; I did not adjudicate it.
- **`kc2_player_channel.gd` (4,217 ln) read only at the function-index level** — it is v1 measurement harness against the recording, judged lineage not runtime parts. If the conductor believes something in it is liftable, name it and I will read it properly.

---

*Filed 2026-09-20 by drax (presentation seam), P0-c of run KC2-PLAY. Read-only census; recommendation and risk only; no production code, no dispatch, no deploy. Tracker-delta: none proposed — this note is an audit return, not a canon write. Routed to conductor: the § 2.1 arena-JSON figure discrepancy (floor px², obstruction descriptions), and the § 5 R-2 (3) question about R-L68-2's pin method and the walled-vs-wall-less extent gap.*
