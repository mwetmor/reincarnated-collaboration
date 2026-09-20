# KC2-PLAY · THE 2D RE-TARGET DELTA SPEC — projection law, view contract, and what replaces the SKIRT

> ▶ **ROLE: SPEC-AUTHOR** — P0-b of the KC2-PLAY ARCHITECT pass. **Spec, not code.** No production code in this seat; no dispatch fired; nothing pushed.
>
> **STATUS:** SPEC — **DELTA. This file governs over SKIRT and F-5 wherever those two are 3D-shaped, and over nothing else.** Every clause of `2026-08-25-kc2-mc-w4-godot-runtime-spec.md` (SKIRT) and `2026-08-25-kc2-mc-w4-twin-test-spec.md` (F-5) that is not named superseded here **stands unamended by reference**. **Neither August file is edited** — forward supersession, superseded clauses named in place *here*, nothing deleted there.
> **Date:** 2026-09-20 · **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`) · **Conductor:** gandalf `RUN-CONDUCTOR` (run KC2-PLAY, pre-charter)
> **Why a delta exists at all:** **3D scenes were retired 2026-09-15** (engine decisions-log `20e778a8`; scene-builder ruling R-C3-102). SKIRT was written for a 3D drax build that never fired. SKIRT §§ 1–6 and 8–9 are **render-agnostic and carry verbatim**; **§ 7's dress-plane / fog / `camera_ground_gate`** and **F-5 § 6.1's camera ratification** are the 3D-shaped surfaces, and they are what this file re-targets.
> **Authority:** ARCHITECT pass `2026-09-20-kc2-play-architect-pass.md` § 2 (the design) + § 4 (Matt's ruling of record, **Q81 F1–F7**, verbatim *"Agreed - accept all"*, 2026-09-20 — F1 closes SKIRT **OQ-3** / `matt_decision_needed` **Q66**).
> **Companion docs:** SKIRT (what the runtime implements) · F-5 (how it is proven) · `2026-08-25-kc2-lift-run-charter.md` (LIFT ledger; **L-3** carries R-L3-2) · `canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md` + `…/scene-builder-workflow.md` (the painted-2D register and its ruled projection constants) · `astra_test_01/burst/runs/C-7/cliffside_v45/README.md` (what the 2D lane actually renders).
> **Standing law, unchanged and binding on every line:** **Law 3** (no fitted constants, no invented rules — **an absence is DECLARED**) · **GL-6** digest before load · **GL-7** linear interpolation between knots IS the position function · **GL-10** use the wire's constant, never re-derive one it carries · **GL-12** absence is declared, not filled · **GL-13** the pinned rectangle is a fact about the recording, not an extent claim · **D4** prereg before results · **K-7** the sealed referent is never regraded · **obs-1** coverage gates before accuracy gates · **obs-3** rubric before instrument.
>
> ⚑ **THREE PREDICATES RUN AGAINST DOCUMENTS THIS SESSION CHANGED WHAT THIS SPEC SAYS.** They are in § 9, not buried: **(1)** a footage **HP trace exists** and is stronger than the ARCHITECT pass assumed — and it **tempers the pass's own headline metaphor**; **(2)** `hp_frac` is the **wrong snapshot field** — the referent's `health_max` is **not constant** (`D-Q1`); **(3)** the arena geometry file's own scale chain **already assumes a character height**, which decides the projection's free constant rather than leaving it to taste.

---

## 0 · Headline — the one sentence, and the one line of arithmetic under it

**The model lives in metres on a plane; the screen is an affine shadow of it; and no pixel ever resolves a hit.**

That is the same constitutional split SKIRT already carries (§ 0: *v1 was a recording, v2 is a model-pack*) and the same one v1's `apply_tick(tick_f)` held — a pure function of the tick. **In 3D the split was easy to keep by accident, because Godot's 3D physics was never wired.** In 2D it is easy to lose by accident, because the lane it is being built beside *already resolves movement with Godot 2D physics*: `keeper.gd` uses floor collision, the VFX kits use `StaticBody2D` on their bolts, and both of those are correct for a cell-review stub and **fatal for a comparison instrument.**

> ⚠ **The single highest-value failure to refuse in this whole re-target:** a build where a pixel capsule decides whether EoR's **3.0 m** radius touched a body. That build has replaced the model with the art, and every T-A and T-B number it emits is grading the art. SKIRT asserted the 3D analogue by *walking 1,430 nodes for `CollisionObject3D`* rather than by care (§ 7.2); **R2D-3 below is that same assertion in 2D, and it is not optional.**

---

## 1 · PROJECTION LAW

### 1.1 The law

**Sim-space** is **model metres on the arena plane**, in the frame the arena geometry file declares: `frame.axes = "+x = EAST, +y = SOUTH (minimap is north-up; the frame is the minimap's own frame, not screen)"`. Height above the plane (`z`) exists only for presentation — **nothing in combat reads it.**

**Screen-space** is an affine projection at the ratified camera elevation **α**:

```
screen_x =  ppm · x
screen_y =  ppm · sin(α) · y   −   ppm · cos(α) · z
draw order = ascending screen_y of the actor's GROUND point (y-sort)
```

with **α = 52.9535411256029°** — *not* 53°. **GL-10 binds here** (use the wire's constant): the value is the ratified GD `player_lock` pitch carried in F-5 § 6.1 and re-quoted by the scene-builder workflow as the painted-canvas angle. Constants of record:

| | value | basis |
|---|---:|---|
| `sin α` | **0.798148** | derived from α |
| `cos α` | **0.602463** | derived from α |
| `tan α` | **1.324808** | derived from α |

⚑ **The lane's own ruled numbers corroborate α to five figures, and this is a free cross-check worth stating once.** The scene-builder workflow's size rule (**R-C3-68(5)**, corrected **R-C3-73**) publishes **60.62 px/m vertical** and **80.31 px/m ground depth** for the painted canvas. Their ratio is **80.31 / 60.62 = 1.32480**, against **tan(52.9535411256029°) = 1.324808**. The lane's two independently-ruled px/m figures *are* `S·cos α` and `S·sin α` for a single uniform ground scale **S = 60.62 / cos α = 100.62 px/m**. The projection law above is therefore not a new invention imposed on the lane — **it is the law the lane is already drawing under**, written down.

**Y-sort is correct by construction, and say why:** because `screen_y` is a positive multiple of ground `y`, sorting by screen-y is sorting by world depth. No depth buffer, no manual z-index table, no per-frame sort key of the view's own devising.

### 1.2 `ppm` — the one free constant, and what fixes it

**`ppm` (pixels per model metre along screen-x) is the entire presentation degree of freedom.** Everything else in § 1.1 is derived. Fixing `ppm` is fixing the F4 zoom.

**F4 ruled:** GD-matched **~8 % figure** as default (the measured register, **D3: 8.02 %**), **house 17 %** on a toggle. A figure fraction is a statement about *screen height occupied by a body of a given height in metres*, so the conversion needs exactly one more number: **`h_fig`, the reference figure height in metres.**

⚑ **`h_fig := 1.9 m` — and this is a substrate-decided value, not a taste call.** The arena geometry file's own scale chain (`scale.chain`) derives `u` from `character_pixel_height = 70.0` and **`character_height_m_ASSUMED = 1.9`**. **If the figure's height constant and the arena's scale chain disagree, the figure is drawn the wrong size relative to the arena for free** — a 5.3 % error against the 2.0 m nav-agent height, permanently baked into every T-C "does it read at the right scale" judgment, and invisible. **One character height governs both halves of the projection or neither is trustworthy.** (The decoded `NavManager::SetDefaultConfig` **agent height 2.0 m** is *not* imported here for the same reason the geometry file declines to import it: its own note says *"Corroborating (not importing)"*. It stays the nav-bake value, which is what it is.)

**Derived, and they are the numbers a builder types:**

| preset | figure px @ 1080p | `ppm` (px/m) | Camera2D `zoom` |
|---|---:|---:|---|
| **`ZOOM-GD`** (F4 default) | 8.02 % → **86.616** | **71.885** | `ppm / ppm_plate` |
| **`ZOOM-HOUSE`** (F4 toggle) | 17 % → **183.600** | **152.374** | `ppm / ppm_plate` |

`ppm = (fraction · 1080) / (h_fig · cos α)`. Worked once, so nobody re-derives it wrong: `86.616 / (1.9 × 0.602463) = 86.616 / 1.144680 = 71.885`.

**Zoom is expressed as a RATIO to the plate's authored scale, never as an absolute.** The plate is painted at some `ppm_plate` (the cliffside canvas is at **100.62 px/m**); the camera's job is `zoom = ppm / ppm_plate`. Against a cliffside-scale plate that is **0.714** (GD) and **1.514** (house) — both comfortable, which is the practical finding: **the F4 toggle is a camera change, not two sets of art.**

### 1.3 What this buys, stated as three sanity checks a builder can eyeball

- **EoR's 3.0 m ring at `ZOOM-GD`** draws as an ellipse **215.7 px** wide by **172.1 px** deep — against an **86.6 px** figure. The signature skill is **2.5× the character's height across.** It reads. (At `ZOOM-HOUSE`: 457 × 365 px against a 184 px figure — same ratio, as it must be.)
- **Monster `ViewDistance` = 80.0 m** (the Crucible override, Lap U, 169/169 rolled tier-16 monsters) is **5,751 px at `ZOOM-GD`** — **3× the viewport width**. ⚑ **Design consequence, and it is robust across the entire scale uncertainty in § 1.4: there is no approach phase and no stealth. Aggro is arena-wide.** A player who expects to pull a corner of the board will not get one; what he gets is the referent's experience — *everything already knows*. That is a T-C axis ("threat pressure") whose expected answer is known before a frame is rendered.
- **The arena does not fit on the screen, and should not.** At `ZOOM-GD` and the geometry file's own extent, the ring is **~1.7× the viewport wide and ~3.2× tall** (§ 1.4 numbers). The referent could not see the whole arena either. A build that zooms out to fit it has re-litigated F4 by accident.

### 1.4 ⚑ THE SCALE CAVEAT — carried, and it is larger than the ARCHITECT pass states

**Every metre figure drawn from the arena ring is PROVISIONAL until `R-L68-2` lands.** The geometry file publishes `value_m_per_minimap_px = 0.1981`, `provenance: "DERIVED-WEAK"`, band `[0.094, 0.3663]`, and its own `consequence` row: *"Every metre figure in this file inherits a ~1.7× uncertainty factor. The NATIVE minimap-px geometry does not."*

⚑ **SUPERSEDED IN THE ARCHITECT PASS, named here (§ 2.7 (iv), *"Metre scale 1.7× band until R-L68-2 is confirmed"*).** Two things have moved and the pass carries neither:

1. **The point estimate `u = 0.1981` is EXCLUDED by the game's own placement data.** `R-L3-2` (LIFT ledger **L-3**, finding `D-W1-1`, **routed not adjudicated**): containment of the tier-16 spawn emitters requires **`u ≥ 0.22277`** under all sixteen cited geometries. **Window of record: `[0.22277, 0.3663]` — 1.64×, not 1.7×, and 0.1981 is outside it.** Quoting 0.1981 forward is the § 8.2 figure-hygiene failure (*a corrected figure must move with its derivations, never be re-quoted*).
2. **The scale chain rests on two assumptions the consuming build must not mistake for measurements:** `character_height_m_ASSUMED = 1.9` and `cos_camera_pitch = 0.5` with the note *"theta ~60 deg assumed; bracketed 50-70 deg by two weak independent reads"*. ⚠ **That 60° is GRIM DAWN's camera. Our α is 52.95°. They are different cameras doing different jobs** — GD's converts screen px → ground metres *inside the u chain*; ours converts ground metres → screen px *in § 1.1*. **A builder who "notices the inconsistency" and unifies them has corrupted `u`.** Named here so the collapse cannot happen quietly.

**What is NOT provisional:** **EoR's `radius_m = 3.0`** is a pack value (SKIRT § 4 row 8, L-22 pins), as are every other model metre — `ViewDistance`, body radii, move speeds, projectile ranges. **The uncertainty is confined to the ARENA'S SIZE IN METRES and to nothing else.** That containment is why the build is safe to start.

**Build consequence, and it is the whole reason this subsection is normative:** **author the plate in NATIVE MINIMAP PIXELS**, with `u` as a **single named constant read from one place**. A pin that moves `u` by 1.64× is then a one-line change and a camera re-gate — not a re-authoring. A plate baked in metres is a plate that must be repainted.

### 1.5 The claim-class table — what is a model value and what is a presentation choice

**Every row in the right-hand column must appear in the runtime-choice ledger (GL-12, SKIRT § 1.6). A presentation choice that is not in the ledger has been laundered.**

| MODEL VALUE (from the pack / decoded / Matt-ruled — never a consumer choice) | PRESENTATION CHOICE (no wire basis — LEDGER ROW REQUIRED) |
|---|---|
| EoR `radius_m` 3.0 · `drain_rate_per_s` 176.4 · `channel_tail_s` 0.25 · `rotation_speed_multiplier` 0.35 | **`ppm`** (both presets) — and therefore the whole screen scale |
| `tick_period_s` = 1/12.25, `MODEL-BINDING` (**F1**, closing OQ-3 / Q66) | **`h_fig` = 1.9 m** — *substrate-corroborated, still a choice* |
| `ViewDistance` 80.0 m (Crucible scope, Lap U) | **α as the render camera** (ratified for a *3D* subject; see § 3.4) |
| All `math_rules` test vectors; DoT stacking law; eHP `G_BAND_A` verbatim | Every VFX texture, palette, particle count, easing curve |
| `interrupts_channel` flags: Blitz `true` · Vire's Might `true` · War Cry `false` · Rune of Rush **`UNDETERMINED`** (L-90) | Monster token colour, silhouette, nameplate typography |
| Type-A lag 1.60 s / dur 1.03 s; Type-B dur 0.60 s; uptime 0.838; cast rate 0.290/s | Damage-number formatting; floating proc labels; HUD layout |
| Pool DoT **⅙ max pool / tick, defences ignored** (**D-LIFT-1**) at **~1 s** cadence (**D-LIFT-2**) | Pool **radius** (upper bounds only), pool **outline shape** (`polygons: null`) |
| Authored walls, claim-class `AUTHORED-RULING-NOT-DECODED-SUBSTRATE` (**D-CP2-1**) | The plate's **dressed margin** beyond the wall (the SKIRT's successor, § 3.1) |
| Arena ring **native-px** vertices (177 outer + 4 obstructions) | **`u`** (metres per native px) — **provisional**, § 1.4 |

---

## 2 · THE VIEW CONTRACT — the normative interface, and what unblocks parallelism

**F2 ruled the seats: drax builds the runtime; the Astra lane builds the scene and PACKs it, vendoring the runtime by sha.** Two seats cannot proceed in parallel against a handshake that does not exist. **This section is that handshake, and it is the deliverable that gates P1/P2 concurrency** — the scene seat drives against a canned event stream conforming to § 2.2 until the runtime lands.

### 2.1 Per-tick world snapshot (runtime → view, once per sim tick)

```jsonc
{ "tick": 1834, "t_s": 149.71, "wave": 156, "wave_elapsed_s": 11.34,
  "actors": [
    { "id": 4102, "kind": "monster", "record_path": "…", "faction": "hostile",
      "x_m": 12.418, "y_m": -3.902, "facing_rad": 2.114,
      "hp": 84220, "hp_max": 96000,          // ⚑ NOT hp_frac — see below
      "body_radius_m": 0.62, "size_class": "M",
      "state": "ENGAGE", "controls": ["SLOW"], "is_hero": false, "name": null },
    …],
  "player": { "x_m": …, "y_m": …, "facing_rad": …,
              "hp": 17400, "hp_max": 20005, "energy": 2388, "energy_max": 2576,
              "channel": "ACTIVE", "cooldowns": {"blitz_s": 1.20, …}, "buffs": [...] } }
```

⚑ **`hp` + `hp_max`, NEVER `hp_frac` — and this corrects the ARCHITECT pass § 2.2, which specifies `hp frac`.** Lap Q finding **7** (`D-Q1`): for a contiguous **8.283 s** episode (`t = 713.383–721.650`, straddling w152→w153) the referent's player `health_max` read **16,368, not 20,005** — a **−18.18 %** max-health reduction — and **the sim models `health_max` as a constant.** A fraction-only wire **silently hides exactly that event**: the globe would show the same fill for a wholly different situation, and a T-B HP comparison against footage that contains the episode would compare two different quantities without saying so. **Ship both numbers; let the view compute the fraction; let the recorder see the denominator move.** *(This is not an instruction to model the mechanism — the mechanism is `D-Q1`, unmodelled and declared. It is an instruction not to build a wire that cannot express it.)*

**Field-class rule:** every field above is a **model quantity**. `size_class` is the one derived field and it is **derived from `body_radius_m` by a declared banding**, never art-assigned (§ 4).

### 2.2 The event stream (runtime → view AND → recorder, same emitter)

**One emitter, two consumers.** The recorder is not a second instrument sampling the view; it is a tee off the same stream. **This is what makes it structurally impossible for the comparison instrument to drift from what was on screen** — the KIT-FIDELITY failure family in its presentation-layer form.

| event | payload | notes |
|---|---|---|
| `spawn` | `actor_id, record_path, kind, faction, x_m, y_m, spawn_point_id, wave` | |
| `cast_start` | `skill_id, actor_id, aim_x_m, aim_y_m, tick` | |
| `channel_on` | `actor_id, tick` | |
| `channel_off` | `actor_id, tick, cause` ∈ **{`input`, `type_A_wave_transition`, `type_B_flagged_cast`, `energy`, `death`}** | **`cause` is normative.** `type_B_flagged_cast` additionally carries `by_skill_id` — this is the field the per-skill attribution statistic (§ 6) is computed from, and 8/8 attributed / zero orphans is the footage standard it mirrors (L-89). **`energy` must be emitted `0` times** — it is the `energy_gated_release` DO-NOT, present as an enum member *so its zero-count is assertable* rather than merely believed (SKIRT § 4.1). |
| `hit` | `src_id, dst_id, amount, damage_type, crit: bool, mitigated: float, tick` | |
| `dot_tick` | `dst_id, source_key {type, attacker_id}, amount, ordinal, tick` | `source_key` carries the per-(type,attacker) timeline identity; **same-source MAX, distinct-source ADD** is resolved in the runtime, and the event reports the *applied* value with its ordinal so stacking is auditable |
| `control_applied` / `control_expired` | `dst_id, control_type, duration_s, tick` | ⚑ **overlapping controls burn each other's wall-clock** (SKIRT P1) — the events make that visible; a queue/refresh reading would show up as expiries that outlive their grants |
| `proc` | `proc_id, actor_id, tick` | seven devotion procs; `proc_id` drives the floating label (§ 4) |
| `summon` | `owner_id, actor_id, record_path, x_m, y_m` | same actor template as monsters (R-6) |
| `death` | `actor_id, killer_id, tick` | |
| `wave_flip` | `from_wave, to_wave, tick` | the T-B per-wave duration instrument reads *these*, not a timer |
| `pool_tick` | `dst_id, pool_id, amount, tick` | **D-LIFT-1/2** (§ 3.2) |
| `player_death` | `tick, wave, killer_id` | F6: one life → restart |
| `runtime_choice` | `absent_ref, choice, chooser, rationale` | ⚑ **emitted into the STREAM, once, at load.** GL-12's ledger is a required output of a green G-0 (F-5 § 2.4); putting it in the same stream means **a recording of a session carries its own provenance** and a T-B number can never be quoted without the ledger that qualifies it |

### 2.3 View → runtime (per render frame)

```jsonc
{ "move_target_m": [x, y] | null,     // move-to-cursor, F3
  "channel_held": true|false,          // RMB state, sampled — NOT an edge
  "skill_pressed": [{"skill_id": "blitz", "aim_m": [x, y]}],  // edges, queued
  "toggle_zoom": false, "restart": false }
```

**The view may post intents and nothing else.** No writes to actor state, no position corrections, no "the view noticed a wall". If the view can change the world other than through this struct, the twin-test is grading the view.

### 2.4 Ordering + determinism

1. **The runtime is a pure function of `(tick_index, intents sampled at that tick, its own RNG state)`.** No wall-clock, no `randf()` outside a declared draw site, no frame-rate-dependent accumulation, no iteration over an unordered container.
2. **RNG:** the runtime's own RNG, at the **declared `draw_site_id`s** in the **declared consumption order** (`model/rng_contract.json`). **BANDS-NOT-TAPE** stands (**R-L91-4**, **R-L92-2**): there is no tape, it was ruled unwanted, and the draw-site registry + band grading is the drive substrate. Unchanged by 2D.
3. **Phase order within a tick is DECLARED and fixed**, so the event stream is byte-stable for a given seed and intent log: `intent sample → channel state → player ability resolution → monster AI → monster ability resolution → DoT + pool ticks → deaths → wave logic → snapshot emit`. A build that emits a different order has a different recorder, and two recorders cannot be compared.
4. **Replay is an acceptance test, not a feature:** re-feeding a recorded intent log at the same seed reproduces the event stream **exactly** (R2D-9). This is the cheapest possible proof that no pixel entered the loop.

### 2.5 Render interpolation — and the F1 rider's two-authority problem

- **Monsters and summons: GL-7.** Linear interpolation between tick knots **is** the position function. Do not fit one speed per body; do not ease; do not add a velocity integrator. *(SKIRT § 2 verbatim; unchanged by 2D.)*
- **The player: the F1 rider.** *"The player's own kinematics integrate at render rate and are sampled by the sim each tick."* The 82 ms quantisation lands on ability resolution, never on the feel of your own feet.

⚑ **The rider creates a two-authority position for exactly one actor, and the spec must resolve it rather than let a builder discover it.** The view integrates the player; the sim also owns him. **Rule:**

> **The view's render-rate integration is AUTHORITATIVE for the player's position between ticks, and the sim SAMPLES it at the tick boundary. The sim writes the player's position back ONLY on a CORRECTION — wall clamp, control/root application, knockback, or death — and every correction is emitted as an explicit `position_correction` event so the view SNAPS rather than smooths.**

A silent write-back is the worst of both: it looks like input lag, it is untraceable, and it makes the movement ratios of § 6 meaningless. **Corrections are countable; a green run with a high correction count is a finding, not a pass.**

---

## 3 · § 7 RE-TARGET — what replaces the dress plane, the fog, and `camera_ground_gate`

> **Superseded by this section, named in place:** SKIRT **§ 7.2's SKIRT paragraph** in its entirety — *"an 800 × 800 m dress plane, 1 cm under the measured floor"*, the `clip_rect()` identity/difference assertions, the 1,430-node `CollisionObject3D` walk, `camera_ground_gate(eye, look, fov, aspect, far)` with its nine frustum rays, and the whole fog discipline (`fog_density` in DEPTH mode, fog colour ≡ background, skirt albedo 0.038). **These describe a 3D scene that will not be built.** ⚑ **What is NOT superseded is every DISCIPLINE those mechanisms carried** — the skirt was never the containment; it was the presentation floor beyond the wall, and the camera gate existed so the player never saw the world end. Both obligations survive; only their instruments change. SKIRT **§ 7 (1), (2), (3)**, **§ 7.1**, **§ 7.2's ruling + claim-class paragraphs**, and **§ 7.3** stand unamended.

### 3.1 The arena plate (the SKIRT's successor)

**Object:** one authored level object — the **video-measured ring** (SKIRT § 7 (3), geometry of record `agentic_orchestration/galadriel/notes/crucible-arena-geometry-v1.json`, sha256 `68d895d75702996473cfd654a9a834816d4be0421c4b5ad7a3d2a0cc5d40481f`) drawn in native minimap px and scaled by the single `u` constant.

- **177 outer-ring vertices** + **4 interior obstruction rings** (`OB-1…OB-4`). `interpolated_segments` is `[]` **in the file and must be `[]` in the build.**
- **Claim class UNCHANGED: `AUTHORED-RULING-NOT-DECODED-SUBSTRATE`** (D-CP2-1). ⚠ **Never written back into `arena_bounds`.** Substrate still says `UNBOUNDED` / `OPEN-PLANE`; the closing mechanism behind `NavManager::CreateNavigationData` is undecoded; **reimplementing it is still inventing a rule.**
- **The dressed margin** — painted ground extending beyond the wall so the camera never shows the world's edge — **is the SKIRT's direct successor and inherits its honesty clause verbatim: it is a presentation choice with NO WIRE BASIS and it says so in its own report row.** Its extent is a ledger entry (§ 1.5).
- **The wall is not scenery and not physics.** Containment is resolved in the runtime, in metres, against the ring polygon. The plate's wall art is a *depiction* of a rule that lives elsewhere.

**Axis-convention assertion (new, and it is a real trap).** The file states `+y = SOUTH` and warns: *"Godot import must flip or rotate to its own convention; no flip is applied in the file."* Godot 2D screen-y points down. **Assert the convention with a named landmark, not by eye:** `frame.origin` is *"shot 612 player position (the north gate, in front of the Master of the Crucible's red door)"*. **The north gate must render at the TOP of the plate.** One assertion, mechanically checkable, catches a whole-arena mirror that would otherwise survive to T-C and read as "the arena feels wrong somehow".

### 3.2 Pools — ⚑ THE MAGNITUDE IS NO LONGER A RUNTIME CHOICE

> **Superseded in SKIRT § 7.3 / OQ-2, named in place.** SKIRT specifies: *"A number is required to make ticks fire, so the build supplies one as a registered runtime choice against the `absent_ref` — never as a model value"* (R-L91-7 ruled (a)). **That disposition is overtaken.** **D-LIFT-1** (**⅙ of max pool per tick, defences ignored**) and **D-LIFT-2** (**~1 s ticks; death ≈ 6 s; crossable-not-campable**) are **MATT-RULED model-design values.** At the runtime layer the pool DoT is **SPECIFIED. It is not a free choice and a build that registers one has ignored a ruling.** The `absent_ref` row stays as record of what the *footage* did not measure (`dot_mechanic.provenance: "ATTESTED-UNMEASURED"`, `magnitude: null`, `element: "suspected-poison"`); the ruling is a design decision *about the game*, not a claim about the referent, and **the two must not be collapsed** — that is the § 7.3 split, honoured in the direction it now points.

**Unchanged and still binding:** count ships **`≥ 6`** (a zone entered between exposures leaves no evidence) · radii are **UPPER BOUNDS** (`Z-614` 41.2 px, `Z-618` 44.0, `Z-620` 47.8, … — per-zone in `green_zones.zones`) · **`polygons: null`** with the reason in-file · the unexplained station-622 anomaly is **reported, not explained**.

⚑ **The geometry file carries a build instruction in its own data and it is load-bearing:** `green_zones.class_note` — ***"ENTERABLE DAMAGE FIELDS, NOT WALLS. The Godot arena must NOT collide-block these."*** A pool implemented as an obstacle is the opposite of *crossable-not-campable*, and it would change the fight's whole movement grammar: the referent **walked through** hazards when the board demanded it. **`R2D-6` asserts non-blocking.**

### 3.3 The § 7.1 traps, re-expressed as 2D assertions

| trap (SKIRT § 7.1) | 3D form | **2D assertion — mechanical, not care** |
|---|---|---|
| **Phantom pillars** — 3 of 7 candidate obstructions were teal pedestal HUD icons | read an earlier draft, grow 3 pillars | **Assert `len(interior_obstructions) == 4`** against the geometry JSON at load, by script. The plate's obstruction node count must equal it. A build with 5 or 7 **fails load**, it does not warn. |
| **Two north arcs MAPPED-BUT-NEVER-WALKED** | smoothed closed | The file names them: `unwalked_arcs` = vertex spans **[0→8]** (9 vertices) and **[174→176]** (3 vertices). **Assert the built polygon's vertex set is IDENTICAL to the file's** — no resampling, no spline, no decimation, no convex hull. Those 12 vertices carry a `flagged` attribute the debug overlay draws distinctly, so a viewer can *see* which boundary was never walked. |
| **Metre scale `DERIVED-WEAK`** | a camera ratified before a scale move | **Assert the HUD contains no metre-denominated readout**, and that `u` is read from exactly **one** symbol. Until `R-L68-2` lands, **no metre figure reaches the screen or a report.** |
| ⚑ **NEW — 2D-only, and the most dangerous of the four** | *(SKIRT's 1,430-node `CollisionObject3D` walk)* | **Walk the scene tree; assert ZERO `CollisionObject2D` / `CollisionShape2D` / `CollisionPolygon2D` / `Area2D` on the arena plate, on any actor token, and on any VFX node.** The lane this is built beside ships floor collision (`keeper.gd`) and `StaticBody2D` bolts — **both are correct there and fatal here.** See § 0. |

### 3.4 The camera gate — `camera_ground_gate` → `camera2d_plate_gate`

**What the 3D gate did:** nine frustum rays intersected with the ground plane, each landing inside the skirt **or** beyond fog saturation, per frame, HALT on red. **What it was FOR:** the player never sees the world end.

**2D equivalent, and it is simpler because Camera2D's visible region is an exact rectangle:**

```
visible_rect = Rect2( camera.global_position - viewport_size/(2·zoom),  viewport_size/zoom )
ASSERT visible_rect ⊆ plate.dressed_extent      // per frame, HALT on red
```

- **Camera2D `limits` are set from the PLATE'S DRESSED EXTENT, never from the playable ring** — otherwise the wall sits at the screen edge with void beyond, which is the exact failure the skirt existed to prevent.
- **`zoom` is bounded to the two F4 presets.** A free zoom control is not in scope (F6) and would silently re-scale every T-C judgment.
- ⚑ **Camera2D applies `offset` AFTER `limits`** — the lane learned this the expensive way (**R-C3-53**, parallax positions had to be shifted by the anchor offset). The gate must be evaluated on the **post-offset** rect or it validates a rectangle the player never saw. *(Same shape as the `git diff HEAD~1` family: an instrument answering a neighbouring question and returning cleanly.)*
- **Fog discipline does not port and is not replaced.** Its 2D analogue is the dressed margin's own painted falloff — an art decision inside the H1 register, with no gate.

**F-5 § 6.1 in 2D** is § 7 of this document.

---

## 4 · GEOMETRY-TRUE PLACEHOLDER CLAUSE

**The discipline in one line: art may be fake; space and time may not.** Matt licensed placeholder monster animation and placeholder VFX. **Every dimension below marked MODEL-BOUND is asserted against a pack value by a HEADLESS probe (no rendering, no eye) — `R2D-5`.** Everything else is free art and no one may spend a burst improving it on the critical path.

| class | **MODEL-BOUND — probe-asserted against the pack** | **FREE ART** |
|---|---|---|
| **EoR channel ring** | radius **3.0 m** (projected ellipse per § 1.1); active for exactly the channel's ACTIVE ticks; rotation multiplier 0.35 | ring texture, colour, trail, particle density |
| **Projectiles** | **travel speed**, **flight time**, **range** from the pack; spawn tick; arrival tick. ⚑ The referent's **1.6166 s dwell WAS projectile flight** — a projectile that arrives on a different tick has changed the fight | sprite, trail, muzzle flash |
| **Ground effects / telegraphs** | **true radius**, **true duration**, **onset tick** | fill, edge treatment, pulse |
| **Pools** | radius (**UPPER BOUND, labelled**); **tick cadence ~1 s**, **⅙ max pool per tick** (D-LIFT-1/2) | plume art, colour (`suspected-poison`) |
| **Monster tokens** | **`body_radius_m` drawn at true size** — the token's drawn footprint **IS** its model radius; `size_class` **derived from `body_radius_m` by a declared banding**, never art-chosen | silhouette shape, tint, outline weight |
| **Monster animation** | the **attack flash lands on the volley tick**, not near it; the **death fade starts on the `death` event tick** | move bob, lunge curve, fade duration — **tweens, zero image generation** |
| **Hero / nemesis** | identity comes from the **nameplate**, not from inflated size — an inflated token is a *lie about reach* | nameplate style, body larger *only if* the model says so |
| **Player body (F5 — the Keeper)** | position, facing, move speed = **`ppm` × the model's m/s**. ⚑ **The lane's `walk/run 247/494 px/s` are PRESENTATION CONSTANTS WITH NO MODEL BASIS and must be REPLACED, not tuned** | which cell set; the camera flaw (Q80) is cosmetic here |
| **Player channel presentation** | the channel **survives movement** (`channel_breaks_on_movement: False`, MD-B4app-2; Lap R: *movement-while-channeling CONTINUES*, ratio 0.971, CIs overlap) | **walk/run cells play under the EoR ring while held** — model-true, no new cells |
| **Casts** | cast tick, cooldown sweep from **base** cooldowns + **declared CDR absence** (R-L91-7(a)) | one-shot cast cells for Blitz / Vire's Might / War Cry |
| **Devotion procs** | the **`proc` event tick** | seven distinct coloured bursts, **each with a floating label** — ⚑ in a comparison build, seeing *which* proc fired is worth more than beauty |
| **Hit-react / death (player)** | the tick | a flash; a fade |

**Reuse the four existing VFX grammars (G1 projectile · G2 field/flipbook · G3 · G4) with stub art. No new kit minting is on the critical path.** The 19 kits already in `cliffside_v45` are more than a placeholder set needs.

---

## 5 · INPUT SPEC (F3)

**Ruled: GD-faithful mouse, desktop native build only.** WASD makes Matt a different pilot, and T-B would then be measuring the control scheme.

| binding | skill | `interrupts_channel` | basis |
|---|---|:---:|---|
| **RMB held** | **Eye of Reckoning** | *n/a — is the channel* | L-90 slot R; the only bar skill with **no `skillCooldownTime` field at all** — the format's own signature of a channel |
| **LMB** | Blitz | **true** | 0.385 over 13 casts; 5/8 releases attributed |
| **key 2** | Vire's Might | **true** | 0.136 over 22 casts; 3/8 attributed — **the datum that killed the pure-binding rule** |
| **key 3** | War Cry | **false** | 0.000 over 19 casts; the channel *tightens* around its casts (p = 4.9 × 10⁻⁷) |
| **key 7** | Rune of Rush | **`UNDETERMINED`** | **footage-blind.** A registered default, **never a measured `false`** |
| **movement** | move-toward-cursor | — | D-CP2-2's referent explanation |

**Mechanism (SKIRT § 3, D-CP2-2), unchanged:** *casting a flagged skill while the channel is ACTIVE releases it.* A per-skill property — **not** a rule over mouse buttons, **not** a per-cast die roll. ⚠ **A builder who inserts a per-cast probability to close the § 3 rate residual (Blitz 0.385 vs fight-wide uptime 0.838) has re-created the 0.15 cancellation this whole run took apart.** That is the specific failure to refuse.

**`channel_held` is sampled as a LEVEL, never as an edge** (§ 2.3) — which is what makes the next question answerable at all, and it is not answered anywhere.

### 5.1 ⚑ OPEN — held-RMB across a Type-B release (registered, not invented)

**The question:** a flagged cast fires while the channel is ACTIVE; the channel releases for the Type-B duration (**median 0.60 s**). **If RMB is still held when that elapses, does the channel auto-resume, or does it require a re-press?**

**Predicate run against the documents: SKIRT § 3, § 4, § 4.1, § 9, OQ-1…OQ-5; F-5 § 5; the LIFT ledger; the ARCHITECT pass § 4. NONE of them answer it.** It is not a superseded clause and it is not a registered absence — **it is a hole**, and it is decided the moment a builder writes the state machine. Registered here rather than filled (§ 8, **OQ-1**).

**Lean (ONE): AUTO-RESUME for Type-B while the intent is held; NO auto-resume for Type-A.** And the reason is evidential rather than aesthetic — **the two release types have opposite duration signatures, which is what a mechanical lockout versus a human hand looks like:**

| | median | spread | reading |
|---|---:|---|---|
| **Type-B** (flagged cast) | **0.60 s** | IQR **0.55–0.63**, range **0.53–0.67**, n = 8 — **the tightest distribution in the entire measurement** | a **fixed mechanical duration**. A human re-pressing eight times does not produce a 0.14 s total range. |
| **Type-A** (wave transition) | **1.03 s** | IQR **0.62–1.56**, **max 3.50**, n = 11 | **a hand that let go** — and L-85's finding under the finding says so: *"he was not counting his energy; he was counting the fight."* |

**So the lean is not a preference; it is the shape of the two distributions.** Type-B is a lockout the game imposed and the channel resumed under a still-held button; Type-A is the player releasing at the flip and pressing again when he chose to. If Matt rules otherwise, the runtime registers the choice against an `absent_ref` and the § 6 uptime row names it as its first suspect.

---

## 6 · TELEMETRY + COMPARISON SPEC

### 6.1 The recorder

**The recorder IS the § 2.2 event stream, tee'd to JSONL, plus the § 2.1 snapshot at a declared decimation.** Header: pack digest (two-level, GL-6), runtime build sha, seed, zoom preset, `u`, `h_fig`, `ppm`, the full runtime-choice ledger, and `spec_version` of this document. **A run without a header is not comparable and the harness rejects it.** Recording is **always on** — a session that was not recorded cannot be compared, and the cost is a JSONL.

### 6.2 T-A · PORT FIDELITY (machine) — unchanged

**T-A is F-5 as specified and this document does not touch it.** G-0 coverage census over all five facets closes **before** any accuracy tier is scored (**obs-1**; a tier scored on an unclosed census is **VOID, not preliminary**); T-0 vectors normative; T-1/T-2 banded; T-3 **report-only**; the **§ 5 cast-interrupt divergence prereg stands exactly as written** (D4 forbids editing a prereg toward an anticipated result) and may be **DISCHARGED BY SUPERSESSION** naming the reference side actually graded — silence is not a disposition. **Scripted pilot, not a human.** `R-1…R-9` stand.

**What F-5 § 6.1 (camera ratification) BECOMES in 2D:** see § 7 below — it survives, and it changes what it is *for*.

### 6.3 T-B · REFERENT FIDELITY (instrumented) — Matt plays; the recorder computes the footage statistics

**Every row names the footage instrument it mirrors and that instrument's published value AND its published uncertainty. A row with a reference value but no uncertainty is not ready and does not ship.**

| # | statistic | computed from | **footage reference** | **uncertainty / hygiene, carried** |
|---|---|---|---:|---|
| B-1 | **channel uptime** | `channel_on/off` | **0.838** | **6.2 % blind residual CARRIED, not closed** |
| B-2 | **release duty** | `channel_off` spans | **≈ 10.5 %** | → **16.7 %** if the blind gaps are releases |
| B-3 | **cast rate** | `cast_start` | **0.290 /s** (one per 3.45 s) | n = 53 casts |
| B-4 | **Type-A onset lag** | `wave_flip` → `channel_off(type_A…)` | median **1.60 s**; 8/11 within 2.0 s | Fisher p = 0.00336 |
| B-5 | **Type-A duration** | `channel_off/on` | median **1.03 s**, IQR 0.62–1.56, max 3.50 | n = 11; **A-1**: 1 release/flip modelled vs **1.1** measured — **PARKED, explicitly not fired** (R-L88-3) |
| B-6 | **Type-B duration** | `channel_off/on` | median **0.60 s**, IQR 0.55–0.63 | n = 8; range 0.53–0.67 |
| B-7 | **per-skill interrupt attribution** | `channel_off.by_skill_id` | Blitz **0.385** (13) · Vire's **0.136** (22) · War Cry **0.000** (19) · Rune of Rush **BLIND** | **8/8 attributed, ZERO orphans** (L-89). ⚠ Rune of Rush is graded **UNDETERMINED**, never against `0` |
| B-8 | **movement** | `player` snapshot | ⚑ **RATIOS ONLY** | `frac_moving` reads **0.883 / 0.705 / 0.6265** across three instruments — **1.41×**. On this evidence "movement excess" is an **instrument disagreement about the referent**, routed not adjudicated (**D-MPOL2-2**). **An absolute movement figure in a green report is a defect in the report.** |
| B-9 | **per-wave durations** | `wave_flip` | Lap R: **w154 = 14.20 s** (the referent's second-most-contacted wave) | wave boundaries **± 0.25 s** (Lap H-2 `OBS-H2-6`) |
| B-10 | **terminal wave** | `player_death` | **160** | ⚑ **REPORT-ONLY BY CONSTRUCTION, never a gate** (Matt-ruled). The sealed sim ends at **153.2, σ 2.32** |
| B-11 | **time at full health** | HP trace | **42.84 %** (4,653 of 10,861 frames) | Lap Q, 60 fps OCR, **100.00 % accepted** against the decoded denominator; resolves to **1 HP / 1 frame** |
| B-12 | **time below 50 % / 33 %** | HP trace | **3.46 %** / **1.00 %** | *ibid.* |
| B-13 | **frames showing HP decrease** | HP trace | **13.73 %** | *ibid.* |
| B-14 | **HP min** | HP trace | **5,360** (of 20,005) | *ibid.* |
| B-15 | **leech tick cadence** | `hit` + HP trace | **11.408 ticks/s** (mean inter-tick gap 5.259 frames) | **INSIDE** Lap L's decoded bracket [11.387, 12.250], at its LO edge |
| B-16 | **leech tick magnitude** | HP deltas | clean median **820.8 HP** (n = 67); all-129 median **782.8** | `U-P-N-1` = **COUPLED** |
| B-17 | **health regeneration** | HP trace, clean subset | **124.67 HP/s** measured | vs Lap P's decoded **129.38**, residual **−3.64 %**. ⚠ The naive whole-trace drip reads **178.40 HP/s** and is **CONTAMINATED** by sub-50 HP leech ticks — reported so nobody mistakes it for regeneration |
| B-18 | **`health_max` constancy** | `hp_max` | **{20,005 · 16,368}** — one **8.283 s** episode | **`D-Q1`. UNMODELLED in the sim.** Expect the twin to hold 20,005 throughout; **that difference is a KNOWN model gap, pre-registered here, and is not a build defect** |
| B-19 | **HP saw-tooth period + depth** | HP trace | ⚑ **NOT PUBLISHED — DECLARED ABSENT** | see § 6.4 |

**Reporting rule:** every T-B row is reported **with the footage instrument's uncertainty beside it**, and where instruments disagree the row is a **ratio** (B-8 is the founding case). **A published aggregate can be arithmetically true and mechanically false** (R-L89-4) — every aggregate says whether it is a *rate* or a *cancellation*. **G5's uptime is 0.0960, not 1.9 %** (R-L88-5, a 5.2× correction) and any derived figure **moves with it and is RE-DERIVED, never re-quoted.**

### 6.4 ⚑ B-19 — the HP-trace question the ARCHITECT pass asked, ANSWERED

**The pass asks: *"does a footage HP trace exist in galadriel's KC2 notes? cite it or register its absence."*** Predicate run. **The answer is better than the question assumed, and it is not in galadriel's notes — it is legolas's.**

**The trace EXISTS, is committed, and is per-frame:**
`agentic_orchestration/legolas/notes/2026-08-14-kc2-pm4-lap-q-heal-discriminator/pm4q_hp_trace.csv` — **10,861 rows**, 60 fps, `t ∈ [683.0, 864.0]`, columns `frame, t_sec, wave, hp, health_max, deficit, delta_hp`. Committed at `57f191f3`. Findings: `pm4q_findings.md` (**RUN KC2-PM4 · LAP Q**, prereg sha `da62709f…` **UNCHANGED between pre-registration and banking**). **PC-3: 100.00 % accepted reads.** The trace even carries a `wave` column — **per-wave HP statistics are available without a join.**

**So the disposition splits cleanly:**
- **B-11…B-18 have PUBLISHED reference values** (above). **The pass's `time-below-50 %` is already measured: 3.46 %.**
- **B-19 (saw-tooth PERIOD and DEPTH) is NOT published** — Lap Q measured tick magnitude, cadence, regen and the occupancy fractions, not the waveform's period/depth. ⚑ **It is derivable from the committed CSV by re-query of already-measured data** — the *cheapest-refuting-test* shape, no video required (which matters: the referent MP4 left this machine, `matt_to_do` **T30**). **Registered as § 8 OQ-4**, not invented.

### 6.5 ⚑ AND THE METAPHOR THE TRACE CORRECTS — this is the one that would have mis-tuned the build

The ARCHITECT pass § 2.6 puts this first, journey-shaper voice: *"the EoR warlord's feel is… living on leech inside the pack: the HP globe saw-toothing at a characteristic rate while you hold RMB and wade… D2's Whirlwind barb had the same signature."*

**The instinct is right and the shape is wrong, and Lap Q says so with numbers.** He is at **FULL health 42.84 %** of the fight and **below half only 3.46 %** — 376 frames out of 10,861. **He is not living on leech; he is TOPPED UP by it.** The saw-tooth is **high-frequency and shallow**: 13.73 % of frames show a decrease, and the leech ticks at **11.408 /s** at **~820 HP** a tick refill faster than the board drains him. **Menhir's Will — the `+120 hp/s` below-33 % circuit-breaker — is MEASURED-ABSENT**, which is the tell: *the safety net never had to catch him.*

**Why this matters to the build rather than to the prose:** a builder who takes "living on leech" literally tunes toward a knife-edge and will read the twin as *too easy* when it sits at full health — and will "fix" it. **The correct T-B expectation is a globe that is mostly full, dipping constantly and shallowly, with rare deep excursions.** D2's Whirlwind barb is still the right comparison; the referent is simply the **geared** version of it, where the leech has already won. **The D2 feel-note that actually transfers is the INVERSION moment** — you feel the instant leech stops out-racing intake — and on this footage that moment is **rare (3.46 %) and is exactly what a terminal wave at 160 is made of.** B-12 and B-19 are the rows that would catch a twin that gets it wrong in either direction.

### 6.6 T-C · FELT FIDELITY (Matt's eye) — rubric declared BEFORE the instrument (obs-3)

**GATED on the referent video's return (`matt_to_do` T30).** Side-by-side, synced **at wave flips** (B-9 gives the sync points). Verdict per named axis, each with its pre-declared expected direction so a verdict is informative rather than a shrug:

| axis | what Matt is ruling | pre-declared expectation |
|---|---|---|
| **density on screen** | bodies in view at a mid wave | GD-matched at `ZOOM-GD`; **house zoom shows ~½ the ground** (confound (ii)) |
| **threat pressure** | does the board feel like it is closing | arena-wide aggro (§ 1.3) → **no approach phase** |
| **time-to-kill** | per-body, by eye | base cooldowns → **systematically slow pilot** (CDR NOT RECOVERED) |
| **move speed** | traversal against arena size | **gated on `u`** — this axis is not rulable before `R-L68-2` |
| **EoR reach** | does 3.0 m read as it did | model-bound; a miss here is a **projection** bug, not a feel one |
| **sustain** | the globe's behaviour | **§ 6.5** — mostly full, shallow saw-tooth |

**T-C is not run before T-A is green** (F7: pre-T-A play is for **feel only**; no fidelity figure is quoted from those sessions).

---

## 7 · WHAT F-5 § 6.1 BECOMES IN 2D

**OE-1 SURVIVES, and it changes what it is FOR.**

- **It is no longer a CANON-CAMERA ratification.** The 3D object it ratified — `player_lock` yaw 47.0 / pitch 52.9535 / fov_v 31.786 / **k = 0.665**, ruling image `arena-pl-k0665-n160-1920x1080.png` — **has no Camera2D analogue**: there is no boom, no fov, no k. **And F4 already ruled this scene's zoom.** The project ARPG camera (game tracker **A′1/B1**) remains **BANKED, not ratified**, and ratifies at the demo's first authored floor — **not here.** ⚠ **Nothing this scene shows Matt is a canon-camera candidate**, and a session that banks one from it has ratified a comparison instrument as a product register.
- **It IS still a READABILITY gate, and that half of F-5 is the half that was always load-bearing:** *"a camera that cannot resolve the behaviour being ratified turns an owner-eye gate into sliver-certification"* (obs-1 at the presentation layer). **WW-8 measured exactly that failure at k = 0.665.** The behaviours Matt rules on are **channel-through-movement · release-at-wave-flip · the spawn drip · monster state changes**. If `ZOOM-GD` cannot show them, **the gate is re-run at `ZOOM-HOUSE` and that second frame is a DIAGNOSTIC, not a canon candidate** (the A2g demotion precedent, R-CPB-17(c)).
- **The `R-L68-2` ordering gate STILL BINDS, and the reason is narrower than in 3D.** `u` does not touch the figure or `ppm` — it scales **the plate relative to the figure**, which *is* "how much ground you are looking at," which *is* what OE-1 rules. **R-L91-5 stands: a camera ratified before a 1.64× scale move ratifies a different scene. Ordering is conduction.**
- **Matt's own gate discipline governs (R-CPB-17b, verbatim):** *"I have never eyeballed this fixed boom… so we won't want to check it off as canon until I can eyeball…"* — **he ratifies a LOOK, not a number.** F-5 closes when his word is recorded against a frame **of this build**, identified by **path + sha** (NOTE-96: never assume the artifact). Until then the build's camera row reads **PROVISIONAL** and the report card says so on its face.
- **OE-2 (the fight moves) and OE-3 (the report card) carry UNCHANGED.**

---

## 8 · ACCEPTANCE CRITERIA — `R2D-1 … R2D-10`

**`R-1 … R-9` (SKIRT § 10) and `A-1 … A-7` (F-5 § 8) STAND. These extend them; none replaces one.** Each is mechanically checkable — a comment is not enforcement.

- [ ] **R2D-1 · Projection law implemented as § 1.1**, with **α = 52.9535411256029°** (not 53°), `ppm` a single named constant, and the **§ 1.1 cross-check reproduced**: `tan α` against the lane's ruled `80.31 / 60.62`, agreeing to 5 significant figures.
- [ ] **R2D-2 · `ppm` derived, not typed.** `ppm = (fraction · 1080)/(h_fig · cos α)` with `h_fig = 1.9 m`; both F4 presets reproduce **71.885** and **152.374** px/m; **`ppm`, `h_fig`, `u` and the dressed-margin extent each carry a runtime-choice ledger row** declaring them presentation choices with no wire basis (§ 1.5).
- [ ] **R2D-3 · ⚑ NO PHYSICS IN COMBAT.** Scene-tree walk asserts **ZERO** `CollisionObject2D` / `CollisionShape2D` / `CollisionPolygon2D` / `Area2D` on the plate, on any actor token, and on any VFX node. **Every hit-test, radius test and containment test resolves in metres in the runtime.** *(The direct successor to SKIRT's 1,430-node walk.)*
- [ ] **R2D-4 · View contract honoured.** The view's only write path is the § 2.3 intent struct; the § 2.4 phase order is declared and fixed; **`channel_off.cause` is emitted for every release and `cause == "energy"` occurs ZERO times** (the DO-NOT, made assertable); `runtime_choice` events are present at load for every touched `absent_ref`.
- [ ] **R2D-5 · Geometry-true probe green.** A **headless** probe asserts every § 4 MODEL-BOUND dimension against its pack value — EoR radius, projectile speed/flight/range, ground-effect radius/duration/onset, pool cadence + magnitude, token radius, player move speed. **No rendering, no eye.** A free-art change can never red this probe; a geometry change always does.
- [ ] **R2D-6 · Arena plate.** 177 outer vertices + **exactly 4** obstructions asserted against the geometry JSON (sha `68d895d7…`); vertex set **identical**, `interpolated_segments == []`; the two `unwalked_arcs` spans `[0→8]` and `[174→176]` carried **flagged, not smoothed**; **pools are NON-BLOCKING** (`class_note`); the north-gate landmark renders at the **TOP** of the plate; **the plate is never written back into `arena_bounds`.**
- [ ] **R2D-7 · Camera gate.** `visible_rect ⊆ dressed_extent` asserted **per frame on the POST-OFFSET rect**, HALT on red; Camera2D limits derived from the dressed extent, **not** the ring; zoom bounded to the two F4 presets; **no metre-denominated readout anywhere on screen** until `R-L68-2` lands.
- [ ] **R2D-8 · Recorder.** The § 6.1 header is complete (pack digest, build sha, seed, zoom, `u`, `h_fig`, `ppm`, full ledger, `spec_version`); **the recorder is the § 2.2 stream, not a second observer**; every § 6.3 row computes from it; **B-8 emits ratios only**; **B-10 and B-18 are structurally report-only** (no code path turns them into a FAIL).
- [ ] **R2D-9 · Determinism.** Re-feeding a recorded intent log at the same seed reproduces the event stream **exactly**. **`position_correction` events are COUNTED and reported** — a high count is a finding, not a pass.
- [ ] **R2D-10 · Pre-T-A hygiene (F7).** Any session played before T-A is green is labelled **FEEL-ONLY** in the recorder header, **and the harness refuses to emit a T-B table from a feel-only recording.** *(F7 as a structural guarantee rather than a procedural promise — the § 4 report-only pattern, applied to the thing most likely to be quoted early.)*

---

## 9 · OPEN QUESTIONS BACK TO THE CONDUCTOR

*Decision-shaped. **ONE recommendation each, stated first.** Not resolved here.*

**OQ-1 · Held-RMB across a Type-B release — auto-resume, or re-press?** (§ 5.1)
**Recommendation: AUTO-RESUME for Type-B while `channel_held` is true; NO auto-resume for Type-A.** Basis: Type-B's duration distribution is the tightest in the entire measurement (median 0.60 s, range 0.53–0.67, n = 8) — a fixed mechanical lockout; Type-A's is broad (median 1.03, IQR 0.62–1.56, **max 3.50**) — a hand that let go. **No document answers this**; if not ruled, the runtime registers the choice against an `absent_ref` and **B-1 (uptime) names it as its own first suspect.**

**OQ-2 · `h_fig` = 1.9 m (the arena scale chain's own character height) or 2.0 m (the decoded nav agent)?** (§ 1.2)
**Recommendation: 1.9 m.** One character height must govern both halves of the projection; the geometry file's `u` chain is *built from* 1.9 m and its own note says the NavManager decode is *"Corroborating (not importing)."* Choosing 2.0 buys a permanent, invisible 5.3 % figure-to-arena error. *(2.0 m remains the nav-bake value — different job, § 1.4.)*

**OQ-3 · ⚑ A containment arithmetic that appears to push `u` ABOVE the published window — route or ignore?** (§ 1.4)
**Recommendation: ROUTE to galadriel as a rider on `R-L68-2`. Do NOT adjudicate, and do NOT let it block the build.**
The observation, stated with its assumptions because it is a re-derivation from published figures, **not a new measurement**: SKIRT § 7 (2) pins the recorded occupancy hull at **86.915 × 85.303 m**; the ring's native extent is **201 × 269 px**. The recorded path must lie inside the arena — the same containment direction `D-W1-1` used. Unrotated, that needs **`u ≥ 86.915/201 = 0.4324`**, which is **above the window's top (0.3663)**. Under the most favourable rotation (ring diagonal **335.80 px**), the floor is **`u ≥ 0.2588`** — inside the window, and it would **raise its floor from 0.22277**. Netting out the hull's 3.0 m sweep radius on all sides softens both figures (**0.4026** / **0.2410**) without changing the direction. **Reading:** either the ring is substantially rotated relative to the path frame (*ring rotation is UNDERIVABLE* — the W1 prereg refused the ring's shape for exactly this reason), or the window's top is low. **This is the third independent instrument to push `u` upward** — after the published 0.1981 point estimate and `D-W1-1`'s 0.22277 floor — and three instruments agreeing on a *direction* is worth a measurement seat's attention even though none of them is mine to adjudicate. **Build impact: none, if § 1.4's native-px rule is honoured.**

**OQ-4 · Fire the HP saw-tooth re-query (B-19)?** (§ 6.4)
**Recommendation: YES — fire it, and fire it before T-B sessions begin.** It is a **re-query of already-committed measured data** (`pm4q_hp_trace.csv`, 10,861 rows, per-frame, with a `wave` column) — **no video needed**, which matters because the referent MP4 has left the machine (T30). It is the only T-B family with **no published reference value**, and without it B-19 is a row with a twin figure and no referent. Seat: legolas or galadriel; deliverable is **period + depth + per-wave excursion depth**, banded, against the already-published occupancy fractions as controls (B-11…B-14 must reproduce, which makes the re-query self-checking).

**OQ-5 · Runtime↔view packaging: in-process module, or separate process?** (§ 2, F2)
**Recommendation: IN-PROCESS — one Godot project; the runtime is plain GDScript with ZERO scene-tree dependencies (no autoloads, no `Node` base class, no `get_tree()`), vendored by sha per F2.** It then runs headless under `godot --headless` for T-A and the R2D-5 probe **with no scene at all**, which is the property that makes the headless suite honest; and the view calls it directly, which removes an IPC layer that could reorder events and quietly break R2D-9. **The seam that matters is the § 2 contract, not a process boundary** — a separate process would give the *appearance* of separation while the real guarantee (the view can only post intents) is a code-review fact either way.

**OQ-6 · Monster token drawn size — model radius exactly, or art-inflated for readability?** (§ 4)
**Recommendation: MODEL RADIUS EXACTLY, with identity carried by the nameplate.** An inflated token is **a lie about reach** — the player learns a spacing that the model does not honour, and every T-C "threat pressure" and "time-to-kill" verdict is then rendered against a board he is misreading. Hero/nemesis distinction goes to the **nameplate and outline weight**, which cost nothing and mislead nobody. If a small body is genuinely unreadable at `ZOOM-GD`, the fix is a **minimum-visibility outline drawn OUTSIDE the true radius** and reported as a presentation choice — never a grown body.

---

## 10 · ⚑ WHAT I BELIEVE IS WRONG IN THE ARCHITECT PASS

*Four items. Three are corrections; one is a metaphor that would have mis-tuned the build. The pass's structure, its seat map, and all seven F-rulings stand — I dissent from none of them.*

1. **§ 2.2 specifies `hp frac` in the world snapshot. It should be `hp` + `hp_max`.** `D-Q1` (Lap Q finding 7): the referent's `health_max` dropped **18.18 %** for **8.283 s** and the sim models it as constant. A fraction-only wire cannot express that, and a T-B HP comparison would silently compare two different quantities. **§ 2.1 + B-18.**
2. **§ 2.7 (iv) quotes the metre scale as *"1.7× band until R-L68-2"*. Both halves have moved.** `R-L3-2` (LIFT **L-3**) **excludes** the published `u = 0.1981` outright and narrows the window to **[0.22277, 0.3663] — 1.64×**. Quoting the superseded point estimate forward is the § 8.2 figure-hygiene failure the spec itself legislates against. **§ 1.4.**
3. **§ 2.1 writes the projection as `sin 53°`.** The camera of record is **52.9535411256029°**, and the 2D lane's own ruled px/m pair (**60.62 / 80.31**, R-C3-68(5)/R-C3-73) reproduces **tan(52.9535°)** to five significant figures. **GL-10 binds: use the wire's constant.** The error is negligible in pixels and the *habit* is not — and there is a free prize in the correction: **the projection law is not being imposed on the lane, it is the law the lane already draws under**, which is a much stronger position from which to hand a scene seat a spec. **§ 1.1.**
4. **§ 2.6's headline metaphor — *"living on leech inside the pack… the HP globe saw-toothing"* — is the right instinct with the wrong shape, and the footage says so.** The referent is at **full health 42.84 %** of the fight and **below half 3.46 %**; **Menhir's Will is MEASURED-ABSENT** — the safety net never had to catch him. He is **topped up** by leech, not living on it. **A builder who takes the metaphor literally tunes toward a knife-edge and will "fix" a correct twin for sitting at full health.** The metric survives — HP-trace shape *is* first-class, the pass is right about that — but its **expected value is a mostly-full globe with a shallow, fast saw-tooth and rare deep excursions**, and the D2 Whirlwind-barb comparison transfers at the **inversion moment**, not at the steady state. **§ 6.5.**

*(Two things I checked expecting to dissent and did not: **F2's seat split** — drax builds the runtime, the Astra lane builds the scene — is right, and the C-7 LSP-gate spike shows drax already operating in the lane, so the P0-c assignment is not a seam violation; and **F4's GD-default zoom**, which I expected to fight on readability grounds, produces an EoR ring **2.5× the figure's height across** (§ 1.3) and needs no defending.)*

---

*Filed 2026-09-20 by gandalf (named sub-agent, `SPEC-AUTHOR`), **P0-b of run KC2-PLAY** (pre-charter). Delta spec: **governs over SKIRT § 7 and F-5 § 6.1 where they are 3D-shaped; everything else in both stands unamended by reference.** Forward supersession — superseded clauses named in place here; **neither August file edited.** **K-7 held:** no sentence describing the sealed referent is altered. **Law 3 held:** every constant in this document is either derived in the open from a cited value, or DECLARED as a presentation choice requiring a ledger row, or registered as an OPEN QUESTION. **No fitted constants.** No production code, no dispatch, no push.*


---

## ⚑ CORRIGENDUM-FORWARD 1 (2026-09-20, conductor; jack-ryan Gate-1 BLOCK-A + WARN-9/12 on the KC2-PLAY charter) — governs over the body; nothing above is rewritten

1. **§ 1.2 / R2D-2 — the two `ppm` presets were computed at `h_fig = 2.0` while the text fixes `h_fig = 1.9`.** The worked line `86.616 / (1.9 × 0.602463) = 86.616 / 1.144680 = 71.885` is arithmetically false: `1.9 × 0.602462 = 1.144679` and `86.616 / 1.144679 = 75.668`; the printed 71.885 back-solves to `h_fig = 2.00000` exactly. **`h_fig = 1.9 m` STANDS** (OQ-2, conductor ruling KP-0e — the arena scale chain's own character height; the 5.3 % argument in § 1.2 is the reason). **Values of record: `ZOOM-GD` = 75.668 px/m · `ZOOM-HOUSE` = 160.394 px/m.** Zoom ratios against a 100.62 px/m plate: **0.752 / 1.594** (were 0.714 / 1.514). R2D-2 asserts the corrected pair. The lane-corroboration finding (the lane's px/m pair reproduces tan α) does not depend on `h_fig` and stands. Re-derived independently by the conductor before landing (`cos α = 0.6024624070853052`).
   **Hit table (OP § 4.11 value-set sweep — `71.885` · `152.37x` · `0.714` · `1.514`, all KC2-PLAY surfaces):** this file L64, L65, L67, L69, L386 → **superseded by this block** (body left as lineage) · `2026-09-20-kc2-play-architect-pass.md` § 6.4 → **annotated forward in that file** · charter → no hit. Any § 1.3 figure derived from 71.885 is re-derived at build from the formula, never copied.
2. **R2D-7's metre-readout gate** hung on `R-L68-2` landing; charter ruling R-KP-0c retired the hull as a pin target. **Re-based:** any metre readout drawn from the ring displays the registered `u` and its window `[0.22277, 0.3663]` beside it, until galadriel's rider returns.
3. **Acceptance criteria are `R2D-1 … R2D-10`, closed at ten, in § 8** (the brief's "§ 7 / 1…n" was the brief's error; the charter cites § 8 / ten).

## ⚑ CORRIGENDUM-FORWARD 2 (2026-09-20; Gate-1 re-check WARN-15 + INFO-6) — the sweep took the changed literals, not the figures DERIVED from them

§ 1.3 (body L73–77) still prints figures on the dead 71.885 basis. **Superseded, values of record at `ppm = 75.668` (conductor-re-derived where marked ✓, else jack-ryan's re-check figure):** EoR ring semi-axes **227.0 × 181.2 px** ✓ (was 215.7 × 172.1) — ⚑ **these are RADII; the ring is 454.0 px across** (INFO-6: the body's "2.5×" compared a radius to a figure height) · ring radius = **2.62 × figure height** ✓, i.e. **≈ 5.2 figure-heights across** · 80 m ViewDistance = **6,053.5 px** ✓ (was 5,751) · **481.2 × 384.1** (was 457 × 365) · house-zoom multiples **1.79× / 3.37×** (were 1.7× / 3.2×). **Build rule:** every one of these is computed from the formula at build and asserted by R2D-2's probe; none is copied from prose.
