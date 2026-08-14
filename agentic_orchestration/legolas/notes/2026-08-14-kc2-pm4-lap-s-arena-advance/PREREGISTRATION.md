# RUN KC2-PM4 — LAP S — PRE-REGISTRATION

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Fired under:** R-PM4-44 part 3 (ledger rows L-34, L-35) · **Written 2026-08-14T15:22Z**
**Discipline:** GL-12 DECODE-NEVER-ESTIMATE · outcome-firewalled · NOTE-9 basis on every number ·
FULL 64-hex sha256 on every input and output · read-only on every external source.

This file is written and hashed **BEFORE any instrument runs**. Every threshold, every verdict
rule, and every bound-direction claim used in `pm4s_findings.md` appears here first. Departures
will be declared in the findings under their own heading, as Lap R's `D-R-1`/`D-R-2` were.

---

## 0. Reconnaissance that PRECEDED this file — declared in full

Honesty requires naming what I already saw before hashing this document. Exactly three things:

1. **Directory listings** of `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` and
   `/Users/admin/Games/vendor/grim-dawn/` (file names and sizes only).
2. **ARC container listings** — `survivalmode{1,2,3}/resources/{Maps,Scripts}.arc` file-entry
   **names and decompressed sizes only**. No payload byte was decompressed or read.
   What this revealed: the Crucible ships `survivalworld_{a..j}.map` world assets and
   `game/survival/{eventcontrol,defenses,rewards,survival,tier15waves,tier16waves,tier17waves,
   tier18waves,tier19waves,tier20waves}.lua` scripts. **This is a feasibility fact — that a
   candidate source EXISTS — not an outcome.** It is the reason limbs (a) and (c) are written
   below as decode attempts rather than as UNREACHED-in-advance.
3. **Tool availability**: `objdump`, `nm`, `strings`, `ffprobe`, `python3` all present.

No sim output has been read at any point and none will be. The only sim-side quantities entering
this lap are the three comparators handed down in the commission itself:
**spawn radius 45.06 m**, **`D_ENGAGE_M` = 2.400 m**, **w154 sim span 46.12 s vs referent 14.20 s**.
They are targets to measure against, never inputs to a measurement.

---

## 1. Pinned inputs (each re-hashed at instrument start; mismatch ⇒ HALT)

| input | expected sha256 (from the emitting lap) |
|---|---|
| `…/lap-r-locomotion-contact/method/plates60_lapH2.npy` | `28e7d9dfcdff9316ccde86fd116d55655f8fa0436cd06b95b38d3cd1ff7cf7df` |
| `…/lap-h2-video-match/method/camera_translation_60fps_683-866.npy` | `029a8269af0f0cba39a9cb88bf15ed4478f66aa04068875bcdaa5655f971ea33` |
| `…/lap-h2-video-match/method/player_hp_frac_60fps.npy` | `692cd4115f93e7761e2ffe10089426ce096cc4abb263ce201b8ffec578c370aa` |
| `…/lap-n-crit-and-collision/pm4n_fct_events.csv` | `cf8ed21815339bd62813237c73363e06db86b1758a725ff32567212ed0424ce2` |
| `…/lap-r-locomotion-contact/pm4r_contact_occupancy.csv` | to be recorded at first read (Lap R emitted it; digest carried in `pm4r_digests.json`) |

Vendor corpus (read-only, never written): `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/`
Vendor binaries (read-only): `/Users/admin/Games/vendor/grim-dawn/`
Referent video (read-only): `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4`

**Carried constants, each with its emitting lap named (NOTE-9):**

- Ground-pixel convention `OBS-H2-8`: radial ground distance `r = hypot(dx, dy / K)`, **K = 0.537**.
- Player nameplate anchor: `(960, 429)` ±(50, 16) — Lap R's own gate, reused unchanged.
- **px→m bracket `U-R-1` / `R-PM4-43` part 2: [119.0, 125.0] gpx/m. BOTH EDGES REPORTED ALWAYS.**
  No point value will be used anywhere in this lap. (L-35 recorded the bracket is NOT MONOTONE on
  sim keys; that is a sim-side property and does not license collapsing it here.)
- Wave boundaries `OBS-H2-6`, ±0.25 s:
  151 ≤ 683.0 · 152 @ 698.6 · 153 @ 714.9 · 154 @ 729.8 · 155 @ 744.0 · 156 @ 760.2 ·
  157 @ 780.4 · 158 @ 799.7 · 159 @ 812.7 · 160 @ 839.0 · fight close 864.0.
- Fight window `FIGHT_T0 = 683.0`, `FIGHT_T1 = 864.0`.

---

## 2. LIMB (a) — Crucible spawn geometry from world assets

**Attempt order, declared in advance:**

- **a1** — decode the `survivalworld_*.map` container header from bytes. Report magic, version,
  section table. **No format is assumed from memory**; anything I cannot read from the bytes or
  from a public format description I will name UNREACHED.
- **a2** — if the container opens, seek: level bounds / terrain extent, and any entity/spawn-point
  table with world coordinates.
- **a3** — `.arz` arm: search `SurvivalMode{1,2,3}.arz` record names for spawn-point / arena /
  proxy records with coordinate or radius fields.

**Grading rule, fixed now:**

| finding | grade |
|---|---|
| a byte-level field I read directly out of the container | **MEASURED** |
| a container structure I match to a documented public format description (source cited) | **MEASURED-WITH-CITED-FORMAT** |
| any dimension I cannot read from bytes | **UNREACHED** — recorded, never estimated |

**No inference from arena screenshots, wiki text, or memory of the game will be graded above
INDICATIVE, and no INDICATIVE value will enter a headline number.**

---

## 3. LIMB (b) — THE VIDEO-GEOMETRY LIMB

### 3.0 The bound-direction claims, stated before measuring

- **A nameplate PROVES a living body; its absence proves nothing** (occlusion, VFX saturation,
  off-screen, plate suppression). Therefore **plate counts are LOWER bounds on bodies.**
  (Carried from Lap R, unchanged. Corpses are plate-free — `OBS-H2-1`.)
- **Nameplates only render inside the screen frustum.** Therefore the first-appearance radius
  distribution is **RIGHT-CENSORED at the frustum limit**: a measured first-appearance distance is
  a **LOWER bound on the true spawn distance** of that body. I pre-commit to publishing the
  frustum limit itself and the fraction of births at the boundary, and to never quoting a
  first-appearance percentile without the censoring attached.
- **The hull of observed positions is a strict LOWER bound on arena extent.** A place the player
  or a body demonstrably occupied is a place the arena contains. This limb is **one-directional
  and signed**, which is why it — not the censored first-appearance distribution — carries the
  arena headline.

### 3.1 The tracker (pre-registered parameters)

Plates are associated frame-to-frame by greedy nearest-neighbour in **ground-px** on the
player-relative offset `(x − x_p, (y − y_p)/K)`.

| parameter | PRIMARY | sensitivity sweep |
|---|---|---|
| `G_MAX` max per-frame association jump (gpx) | **60** | {40, 60, 90} |
| `N_MIN` frames a track must persist to be counted | **6** (0.100 s) | {3, 6, 12} |
| `H_GAP` frames a track may miss and still continue | **6** | {3, 6, 12} |

A track's **birth** is its first frame. **First-appearance radius** = the ground-px radius at that
frame, reported in gpx and in metres at **both** bracket edges. Frames lacking a detected player
plate are EXCLUDED, never imputed (Lap R's rule, reused).

**Every headline from this limb is reported at the PRIMARY setting with the full sweep published
beside it.** If the sweep changes a verdict, the verdict is reported as sweep-dependent and NOT
promoted to a headline.

### 3.2 Frustum limit (computed, not assumed)

The maximum measurable ground radius in each of the four screen directions from the player anchor
`(960, 429)` on a 1920×1080 frame, under `K = 0.537`. Published in gpx and in metres at both edges.

### 3.3 Arena bounds

World-frame player trajectory = cumulative sum of the Lap H-2 camera-translation trace (valid
because `OBS-H2-7` measured the camera rigidly player-locked, so camera translation IS player
world displacement in screen px). From it:

1. player axis-aligned bounding box, in gpx and m at both edges;
2. player convex-hull **diameter** (max pairwise distance);
3. the **entity hull** = player world position + each plate's ground offset, over all frames —
   axis-aligned box and diameter.

All three are **LOWER bounds on arena extent**.

### 3.4 Arrival curves

Per wave, living-plate count binned at **0.25 s** from the wave increment; time to first reach
50 % and 90 % of that wave's peak plate count; peak count and its time.

### 3.5 Pre-registered verdict rules for limb (b)

- **V-B1.** If the frustum radial limit is **< 45.06 m at BOTH** bracket edges, record as MEASURED:
  *the referent's camera cannot contain a body at the sim's spawn radius*, and mark the entire
  first-appearance distribution CENSORED. If it is ≥ 45.06 m at either edge, report the
  uncensored fraction instead.
- **V-B2.** If the **entity-hull diameter** (a LOWER bound on arena extent) is **< 90.12 m**
  ( = 2 × 45.06) at BOTH bracket edges, that is **not yet** a refutation — a lower bound below a
  claim refutes nothing. It becomes a refutation only in the form: *the sim's spawn radius alone
  (45.06 m) exceeds the referent's measured entity-hull DIAMETER*, i.e. `45.06 > D_entity_lb` at
  both edges. **Only that stronger statement may be quoted as a refutation**, and only with the
  word LOWER-BOUND attached. I pre-commit to this asymmetry now so I cannot choose the flattering
  framing later.
- **V-B3.** The headline spawn-distance comparator is the **95th percentile** of first-appearance
  radius in metres at the **LO edge (119.0 gpx/m)** — the edge that yields the LARGEST metre
  value, i.e. the reading most generous to the sim's 45.06 m. Median and full distribution also
  published, at both edges.

---

## 4. LIMB (c) — THE WAVE-ADVANCE RULE

### 4.1 The video arm — a signed falsification test

For each of the ten wave increments `t_inc` (`OBS-H2-6`, ±0.25 s), over the window
`W = [t_inc − Δ, t_inc]`, compute the **minimum living-monster-plate count** across all 60 fps
frames in `W` that carry a player plate.

- **Δ PRIMARY = 3.0 s**, sensitivity {1.0, 3.0, 5.0}.
- Additionally compute the **global minimum plate count over the whole fight** 683.0–864.0 s, and
  the total duration for which the plate count is exactly zero.

**Pre-registered verdict rule V-C1.** Because a plate PROVES a living body, `min count ≥ 1` over a
window proves the board was **never empty** in that window. Therefore:

> If `min plate count ≥ 1` over `W` for **all ten** increments, the hypothesis *"a Crucible wave
> advances only after every monster of the previous wave is dead"* is **FALSIFIED from the
> referent's own frames**, at the primary Δ, and the falsification is **one-directional** (it
> cannot be an artifact of missed detections, since missed detections only ever LOWER the count).

If falsified for some but not all ten, report the count and DO NOT generalise.
If not falsified, record NOT-FALSIFIED — this test can never *confirm* the rule, only fail to
falsify it, and I pre-commit to saying so in that case.

**Declared limitation, in advance (extends Lap R `UNREACHED-5`):** this test cannot attribute a
plate to a wave. It therefore decides *"was the board empty"*, which is exactly the quantity the
all-deaths gate requires — but it cannot by itself decode what the real rule IS. That is the
script arm's job.

### 4.2 The script/record arm — decode what the rule IS

- **c1** — decompress `survivalmode{1,3}/resources/Scripts.arc → game/survival/eventcontrol.lua`
  and the tier wave scripts; determine whether they are Lua **source text** or compiled bytecode.
  Source ⇒ read the advance condition verbatim. Bytecode ⇒ attempt `strings`-level constant
  recovery only, and grade anything recovered INDICATIVE unless the opcode stream is decoded.
- **c2** — identify which tier script covers waves **151–160** from the script's own contents
  (wave numbers written in the file), **never from an assumption about tier width**.
- **c3** — `SurvivalMode*.arz` record arm: search for wave/spawn/event records carrying advance
  conditions or timers.
- **c4** — `Game.dll` / `Engine.dll` symbol arm if the scripts do not carry the rule.

**Grading:** verbatim script text ⇒ **MEASURED**. Disassembled call site ⇒ **MEASURED**.
Anything else ⇒ **UNREACHED**. **The rule will not be inferred from gameplay memory.**

---

## 5. LIMB (d) — `characterRunSpeedJitter` (cliff `C-I18-1`)

Method is Lap J's, reused without modification: template decode from `templates.arc` bytes, then
PE export-table parse + `objdump -d --target=coff-i386` against the shipped modules with symbol
resolution.

**Questions, fixed now:**

| # | question |
|---|---|
| d1 | exact field name, declaring template(s), declaring group, type, default, description |
| d2 | per-record values across the 151–160 roster (population = Lap D's frozen baton, reused) |
| d3 | **roll timing** — per-spawn (once at creation) or per-tick (re-rolled during play)? |
| d4 | **application basis** — additive percent, multiplicative factor, or absolute units? |
| d5 | **sign/range semantics** — for a value `v`, is the realised speed drawn from `[base·(1−v/100), base·(1+v/100)]` (two-sided), `[base·(1−v/100), base]` (one-sided down), or something else? |
| d6 | is there a **consuming call site** in the shipped binaries at all? (Lap J's `pathMass` was authored-but-unconsumed; the same negative is a legitimate outcome here) |

**Grading, fixed now:** declaration facts and per-record values ⇒ **MEASURED**.
The runtime transform ⇒ **MEASURED** only if disassembled. Semantics argued from surrounding
evidence ⇒ **INFERRED-WITH-EVIDENCE**. No call site ⇒ **MEASURED-NEGATIVE**.
Anything I cannot reach ⇒ **UNREACHED**, and Gamora's `C-I18-1` refusal stands.

**I pre-commit: I will NOT hand gamora a jitter law that is graded below MEASURED on d3/d4/d5.
A partial law is worse than no law, because it folds silently.**

---

## 6. Outcome firewall

No simulation output, no engine telemetry, no I-18 emission set, and no gamora note beyond the
three comparator numbers in § 0 will be opened during this lap. The comparators are used only in
the direction *referent → compared against sim*, never *sim → tuned into referent*.

## 7. Deliverables

`PREREGISTRATION.md` (this file, hashed first) · `pm4s_first_appearance.csv` ·
`pm4s_arena_bounds.csv` · `pm4s_wave_advance.md` · `pm4s_jitter_law.md` · `pm4s_findings.md` ·
`pm4s_digests.json` · instruments at
`agentic_orchestration/research/scripts/pm4s_*_2026_08_14.py`.
