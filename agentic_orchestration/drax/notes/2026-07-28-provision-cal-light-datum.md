# PROVISION-CAL · cell PC-LIGHT — the crypt-lighting fix, measured

**Agent:** drax (presentation seam) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Date:** 2026-07-28
**Ruling:** R-PC-3 (Matt) — G-L1 = **FIX**, executed in-run as **the program's first measured
lighting-authoring datum.**
**Defect under repair:** CEILING-1 (L7-V, `2026-07-25-tcp-l7v-vfx-arrival-report.md` §0) — *"the
substrate is lit as a daylit exterior court, not a crypt: a 2.0-energy directional key through a
roof it does not have, giving a median lit pixel of 88/255 and only 4.66× contrast."*

> **The deliverable is the CURVE, not the endpoint.** Per the cell brief, the measurement of the
> authoring process ranks equal to the fix. §2 below is written step-by-step as the work happened,
> including the steps that measured badly.
>
> **No aesthetic self-judgement is offered anywhere in this note.** The after-render is a Matt-eye
> checkpoint (charter §7). What is claimed here is measured; what is looked at is Matt's.

---

## §0 — What was touched (PC-T3 repo discipline)

`reincarnated-godot` is **not committed by this cell.** Full changed-file list in §6.

**The authoring surface, located by evidence rather than by assumption.** The L7-V substrate is
`mcp-lab/project/scene_before.tscn`, a *bake*. Its builder is
`mcp-lab/prep/FORBIDDEN_do_not_place_in_project/l4prep_build_scene_before.gd`, whose own header
states it was *"ported from `reincarnated-godot/scripts/kit_replica_level.gd` (the `dark-fortress`
kit entry, ~line 199)"* with the environment and lighting **"PORTED VERBATIM."** Diffing the two
lighting blocks confirms it: every value matches (`Key` 2.0 warm + shadows, `Fill` 0.45 cool,
`InteriorPool` 3.4 warm at y=2.0, ambient 0.35, glow 0.6/0.12/1.25, black fog 0.015).

So **the crypt's lighting is authored in exactly one place in the repo that matters here:**
`scripts/kit_replica_level.gd` → `_build_environment()` + `_build_lighting()`. That is the whole
diff surface. Nothing else is edited.

**Finding L-1 (logged, NOT acted on — minimal-diff scope).** `scripts/walltop_level.gd`
(lines 214–277) carries a **byte-identical duplicate** of both blocks — it is the parent lineage
`kit_replica_level.gd` was forked from. The crypt lighting therefore exists twice in the repo and
this fix moves one copy. Propagating it is a separate decision (the two files serve different
consumers) and is left to the conductor, named here so it cannot be discovered later as a surprise.

---

## §1 — BEFORE

### 1.1 Method — LSTAT-1 (frozen) and LSTAT-2 (added by this cell)

**LSTAT-1** is the CEILING-1 measurement, reproduced exactly: Rec.709 luma on 8-bit sRGB, stride-3
sample from (0,0), lit filter `luma > 12.0` (excludes the black surround outside the walled box),
contrast = p95/p05 of the lit sample, percentile index `int(q·n)` on the ascending sort — the
non-interpolated convention `mcp-lab/l7vfx/scripts/ab_stats.py` used, kept so the successor value
cannot be moved by an estimator change. Tool: `tmp/pclight/light_stats.py`.

**LSTAT-2 was added BEFORE any authoring, because LSTAT-1 has a hazard the L7-V cell never had to
face.** LSTAT-1 re-derives its lit pixel set from *each* frame. That is sound when exposure is held
constant (L7-V was measuring an additive VFX pass on a fixed room). It is **not** sound across a
lighting re-author: darkening the room pushes real room pixels under the 12.0 threshold, they leave
the sample, and the ratio then moves for a reason that is an artefact of the filter rather than a
fact about the picture — *and it moves in the flattering direction.* LSTAT-2 freezes the pixel set
once from the BEFORE frame's lit mask (72,175 sampled px) and evaluates every later frame over that
identical set. Same pixels, changing values.

**Both are reported at every step.** LSTAT-1 keeps the lineage to 4.66× unbroken; **LSTAT-2 is the
number the trajectory is steered by**, and it is the number the defect's measured successor should
be read from.

Instrument control (L-N — clear the instrument before recording anything): LSTAT-2 evaluated on the
mask frame itself returns **4.81× = LSTAT-1 exactly**, 0.0 % of masked px under threshold. The two
metrics are identical at the origin by construction, so any later divergence between them is the
filter drift LSTAT-2 exists to expose, not noise.

### 1.2 Camera — R-6, unmoved

dist 34 · fov 24 · yaw 47 · pitch −50 · aim_h 1.0 · 1280×720 · target origin. The L7-V play camera,
per R-6 (*"the camera is the judge; you do not move the judge"*). The rig's pose math is
algebraically byte-equivalent to `mcp-lab/harness/motion_rig.gd::_pose_camera` — `Basis.from_euler`
in Godot's default YXZ order gives −Z = `(−sin y·cos p, sin p, −cos y·cos p)`, hence
`eye = aim + (sin y·cos p, −sin p, cos y·cos p)·dist`, which is the form
`tmp/pct12/probe_rig.gd` already used for the same camera. Rig echoes its pose every run:
`eye = (15.983573, 27.045511, 14.904923)`, fov 24.

**One camera, one exposure, one resolution — no multi-exposure bracket.** The L7-V record used a
second framing (the `__box` still at fov 20 / dist 50 / 1920×1080), but that framing exists to judge
*composition*, not light, and the brief pins the canonical camera. Reproducing a second camera would
add a second set of numbers with no second question attached.

### 1.3 The BEFORE numbers

Capture: `tmp/pclight/frames/before00.png` · stats: `tmp/pclight/stats_before00.json`

| | value |
|---|---|
| frame mean luma | **55.27** |
| lit fraction (of stride-3 sample) | 70.4 % (72,175 / 102,480) |
| p05 / p50 / p95 | 23.4 / **89.1** / 112.6 |
| min / max | 12.0 / 150.0 |
| lit mean | 78.17 |
| **LSTAT-1 contrast p95/p05** | **4.81×** |
| **LSTAT-2 contrast (mask = self)** | **4.81×** |

**Reconciliation with the 4.66× of record — reported, not smoothed.** L7-V measured **4.66×** and a
median lit pixel of **88**; this cell measures **4.81×** and a median of **89.1** on an independently
rebuilt path (live builder rather than the bake, this repo's `project.godot` rather than the lab
harness's, a still rather than frame 75 of a 120-frame step-mode clip). Median agrees to **1.2 %**,
contrast to **3.2 %**. That is a *reproduction* of CEILING-1, not a re-derivation of it — and the
residual is a real difference between two render paths, so it is **not** absorbed by declaring one
of them correct. **Every delta claimed below is measured within this cell's own path**, before
against after, so the 3.2 % path offset cancels out of the trajectory entirely and appears only in
this paragraph.

### 1.4 What the numbers say, before any picture is looked at

The 16×9 lit-luma map (`stats_before00.json → cell_mean_luma`) is a **plateau**: the entire floor
field sits between **86 and 105**, edge to edge, with the highest cell (105.0) only 1.2× the typical
cell (~89). A 3.4-energy warm omni sits at the room's centre and moves the cells beneath it from ~92
to ~105 — **a 14 % lift, at the point of maximum effect.** The defect is not "too bright"; it is
**too even.** The p05 of 23.4 is contributed almost entirely by the *outside* faces of the far
walls, not by anything inside the room. Firelight has nothing to own.

---

## §2 — The authoring trajectory

*(written incrementally, in execution order)*

### 2.0 — How the trajectory was run, and what "effort" means here

One rig, one camera, one settle count, one stat tool, held fixed for every step. Each step is
**one coherent authoring intent**, applied to `scripts/kit_replica_level.gd`, then rendered and
measured before the next intent is formed. No step is retro-fitted and **no step is deleted**:
S8 and S12 measured badly and are reported as run, because a trajectory with the failures removed
is not a trajectory, it is a result with a story attached.

**Effort is reported as wall-clock between step captures.** That number is honest but it is not
the interesting one, and the cell's headline effort finding is that **the authoring was cheap and
the instrument was expensive** — see §4.

### 2.1 The steps

Each row: what changed (node/property/value), why, and the measured response. **L1c** = LSTAT-1
contrast (the frozen metric). **L2c** = LSTAT-2 contrast (mask-locked; the steering metric).
**u12** = % of the BEFORE room mask now under luma 12 — the legibility counter-gate defined in 2.2.

| # | change (node · property · value) | why | L1c | **L2c** | p50 | mean | u12 | Δt |
|---|---|---|---|---|---|---|---|---|
| **S0** | — (as authored) | the defect | 4.81× | **4.81×** | 89.1 | 78.2 | 0.0 % | — |
| **S1** | `Key.light_energy` 2.0 → **0.0** | *diagnostic, not a fix.* Measure what the false sun is actually contributing before replacing it | 4.09× | **28.52×** | 19.2 | 22.7 | 16.7 % | 2m14s |
| **S2** | `Key.light_energy` 0.0 → **0.22**, `light_color` warm → **cold (0.55,0.66,0.95)** | the room has no ceiling, so a faint *cold* sky-leak is diegetically honest and gives the walls a top edge | 3.87× | **4.19×** | 26.2 | 28.3 | 4.6 % | 32s |
| **S3** | `Key.light_energy` 0.22 → **0.10** | S2 came out **worse than the original defect**. Third point on the axis, to see whether that is a threshold or a trend | 3.93× | **6.56×** | 22.9 | 25.4 | 12.3 % | 18s |
| **S4** | `Key` → **0.0**, `Fill.light_energy` 0.45 → **0.0** | the dose-response is settled (see 2.3). Both directionals go; isolate `Fill`'s own contribution | 4.81× | **661.58×** | 3.4 | 11.1 | 70.9 % | 22s |
| **S5** | `InteriorPool`: y 2.0→**1.35**, energy 3.4→**7.0**, colour→**(1.0,0.58,0.25)**, range 9→**13**, atten 1.3→**1.7** | give the room's one omni the **fire** register, on the ground plane per R-10 | 5.01× | **38.45×** | 5.7 | 11.3 | 72.9 % | 32s |
| **S6** | **+4 `CornerSconce_*` OmniLight3D** at the existing corner pillars (±7.9, 2.3, ±7.9), energy 2.6, range 8, atten 1.5 | the perimeter needs a source that is *not* a global. The only nodes this fix adds | 5.29× | **21.76×** | 11.5 | 17.4 | 52.2 % | 47s |
| **S7** | `ambient_light_energy` 0.35 → **1.00** | test the legibility dial: ambient is the *honest* flattener (it stands for stone bounce) | 5.21× | **14.79×** | 12.5 | 18.2 | 48.1 % | 24s |
| **S8** | ambient → **0.55**; pool atten 1.7→**0.85**; sconce range 8→**11**, atten 1.5→**0.90** | S7 bought +5 % mean for 3× energy — a weak lever. The real lever is **falloff shape**: slow the falloff so the pools spread | 3.81× | **4.45×** ✗ | 30.8 | 35.4 | 3.8 % | 19s |
| **S9** | pool energy 7→**9.0**, atten 0.85→**1.25**; sconce energy 2.6→**3.4**, atten 0.90→**1.20** | **S8 REJECTED** — perfectly readable and re-flattened to *below* the original 4.81×. Re-steepen, raising energy to hold the level | 4.52× | **6.22×** | 25.2 | 30.0 | 7.6 % | 18s |
| **S10** | sconce energy 3.4→**4.6**, range 11→**8.5**, atten 1.20→**1.55** | tighten the sconces from a wash into **discrete pools** — light *and darkness between it* is the register | 5.03× | **9.18×** | 22.5 | 28.2 | 16.3 % | 22s |
| **S11** | pool energy 9.0→**10.5**, range 13→**15.0** | S10 is the best contrast but fails **both** gates marginally. Reach the pool into the dark mid-field bands, which is exactly where the deficit is | 5.16× | **7.63×** | 24.8 | 31.2 | 11.1 % | 27s |
| **S12** | `fog_density` 0.015 → **0.030** | does deeper recession buy contrast? | 4.54× | **9.23×** ✗ | 16.8 | 21.8 | 31.5 % | 25s |
| **S13** | `fog_density` → **0.015** | **S12 REJECTED** — it buys contrast the same way S4 did, by deleting the picture (31.5 % of the room under threshold). Reverting also doubles as a **reversion check** | 5.16× | **7.63×** | 24.8 | 31.2 | 11.1 % | 23s |
| **S14** | `Key.light_energy` 0.0 → **0.06** (cold) | one last register question the numbers cannot answer alone — see 2.4 | 4.86× | **6.83×** | 26.9 | 32.7 | 7.1 % | 10s |
| **FINAL** | `Key` → **0.0** (S13 config) | ships the stronger measured result; S14 goes to Matt as a named variant | 5.16× | **7.63×** | 24.8 | 31.2 | 11.1 % | — |

**S13 reproduced S11 PIXEL-IDENTICALLY** (`ImageChops` bbox `None`, max delta 0) across two separate
Godot processes — the trajectory is reversible and the config, not the session, determines the frame.

### 2.2 The counter-gate, declared at S4 and not moved afterwards

S4 measured **661.58×** — and 70.9 % of the room was under luma 12. That is the moment the cell
learned that **contrast alone optimises toward a black frame**, so a counter-gate was written down
*before* any further tuning, and never adjusted to fit a result:

- **legibility:** `u12 < 15 %` — the player must be able to read the floor plane they walk on.
- **key:** `p50` in **25–45** — roughly one-third to one-half of the daylit 89.1. Low-key interior,
  not unreadable.
- **contrast:** maximise, *subject to* the two above.

Under that gate the eligible steps are **S9 (6.22×), S11/S13 (7.63×), S14 (6.83×)**. S10's 9.18× and
S12's 9.23× are **both disqualified**, and this is stated plainly because 9.2× is the better-looking
number and it is not the one that ships.

### 2.3 ★ The finding the trajectory exists to have produced

**CEILING-1 was never a brightness defect. A directional light is the wrong instrument for an
interior, at any energy.** The dose-response, all four points at the same camera:

| `Key.light_energy` | LSTAT-2 p05 | p95 | **contrast** |
|---|---|---|---|
| 2.00 (as authored) | 23.4 | 112.6 | 4.81× |
| 0.22 | 12.7 | 53.3 | **4.19×** ← *worse than the defect* |
| 0.10 | 7.9 | 52.1 | 6.56× |
| 0.00 | 1.8 | 51.0 | 28.52× |

The mechanism is visible in the p05 column: a directional light **puts a floor under every surface
in frame**, and `p95/p05` is governed by the darkest surface, not the brightest. Between 0.22 and
0.00 the p95 barely moves (53.3 → 51.0 — that is the torch pool, which the sun was never lighting)
while p05 collapses 12.7 → 1.8. **Dimming the sun 9× made the picture worse.** Only deleting it
worked.

This generalises past this room and is the datum worth carrying: *at the fixed ARPG camera,
whether a light flattens is a property of its FALLOFF, not of its energy.* A directional has no
falloff, so it can only ever flatten. An omni falls off, so it can only ever shape. Every
lighting-authoring decision in the trajectory above is a corollary of that one sentence — including
S8, which is the same error committed in the other direction (falloff slowed to 0.85/0.90 until the
omnis *behaved* like globals, and the contrast promptly fell to 4.45×, below the original defect).

### 2.4 The one thing handed up rather than decided

**S14 — the cold sky-leak.** `Key.light_energy = 0.06`, cold. Measured: contrast **6.83× vs 7.63×**
(−10 %), legibility **7.1 % vs 11.1 %** under-threshold (better), p50 **26.9 vs 24.8** (better). It
also introduces a **cold rim against warm torchlight**, a colour-contrast the luma metric cannot
see at all.

The numbers split, so the numbers do not decide it. **Shipped: `Key = 0.0`** (the stronger measured
contrast, both gates cleared). **S14 is parked as a one-property flip** — `key.light_energy` 0.0 →
0.06, nothing else moves — with its render at `REVIEW/04_VARIANT_cold_skyleak.png`. This is a
register call and it belongs to Matt's eye, not to mine.

---

## §3 — AFTER

Capture: `tmp/pclight/frames/afterA.png` · stats: `tmp/pclight/stats_afterA.json`

| | BEFORE | **AFTER** | Δ |
|---|---|---|---|
| **LSTAT-2 contrast p95/p05** *(the defect's successor)* | **4.81×** | **7.63×** | **+59 %** |
| LSTAT-1 contrast *(frozen metric, see caveat)* | 4.81× | 5.16× | +7 % |
| frame mean luma | 55.27 | 22.17 | −60 % |
| p50 (median room pixel) | 89.1 | 24.8 | −72 % |
| p95 | 112.6 | 68.5 | −39 % |
| p05 | 23.4 | 9.0 | −62 % |
| max | 150.0 | 197.3 | +32 % |
| room under luma 12 | 0.0 % | 11.1 % | +11.1 pt |

**Against the number of record: the 4.66× of CEILING-1 has a measured successor of 7.63×** on this
cell's path, whose own reproduction of the defect reads 4.81×. Stated both ways so neither can be
cherry-picked: **+59 % against this cell's own before, +64 % against the 4.66× of record.**

### 3.1 ★ The measurement that says it best, and it is not p95/p05

The original complaint was that the room is **too even**, and evenness is spatial — so the honest
test is spatial. Take the **82 cells of the 16×9 map that BEFORE rendered as the daylit floor
plateau** (cell mean > 60), freeze that cell set, and read the same cells after:

| | spread across the 82 fixed cells |
|---|---|
| BEFORE | min 60.3 · max 105.0 · **max/min 1.74×** · p90/p10 **1.22×** |
| **AFTER** | min 14.8 · max 106.7 · **max/min 7.21×** · p90/p10 **2.62×** |

**The floor the player walks went from a 1.22× plateau to a 2.62× modulation over an identical,
BEFORE-defined set of cells** — 4.1× more spatial range by max/min. The room's brightest cell is
essentially unchanged (105.0 → 106.7); everything that moved, moved *downward and unevenly*. That
is the shape of "lit by sources in the room" rather than "lit by a sun above it."

### 3.2 Instrument caveat, stated because it cuts against a headline number

**LSTAT-1 cannot tell these pictures apart, and this cell can prove it.** At **S4** — a room 86 %
darker than the original, 70.9 % of it below threshold — LSTAT-1 returned **4.81×**, which is the
BEFORE value to three significant figures. LSTAT-1 also read the fix as *worse than the defect* at
S1, S2, S3, S8 and S12. That is not noise; it is the per-frame threshold re-deriving its own sample
until the ratio is nearly scene-independent. **The +7 % LSTAT-1 figure in the table above should be
given no weight.** It is reported only because it is the metric that produced 4.66×, and deleting
it after the fact would be moving the goalposts. This is exactly the failure LSTAT-2 was written in
§1.1 to pre-empt, *before* any of these numbers existed.

---

## §4 — Determinism (charter §6 check 9, the accumulator lockout)

### 4.1 Result: CLEAN, and stronger than byte-identity

| test | result |
|---|---|
| `afterA` vs `afterB` — two separate Godot processes, identical args | **byte-identical** (`sha256 992a1ccf…`), 0 differing px, max delta 0 |
| `s11` vs `s13` — same config reached by two different edit paths | **byte-identical**, same sha256 |
| `afterC` — re-render after the comment-only edits to the builder | **byte-identical**, same sha256 |
| **settle-invariance**, shipped stage: settle 90 vs settle 40 | **0 differing px** |

Five independent processes, one sha256. **Verdict: LOADS-CLEAN / no accumulator.**

### 4.2 ★ The instrument was blind first, and the fix to it is a standing method note

An instrument that only ever says "identical" has not been shown to be capable of saying anything
else (L-N). So SDFGI was forced ON as a positive control — L7-V established SDFGI *is* the
accumulator — and **the control initially FAILED to fire:**

```
ctrlSDFGI_A vs ctrlSDFGI_B   ->  byte-identical, same sha256
```

Two SDFGI runs, byte-identical. Under a naive reading that would have said "SDFGI is deterministic",
contradicting L7-V. The naive reading is wrong, and finding out why is the useful part:

1. **SDFGI was genuinely active** — `ctrlSDFGI_A` vs `afterA` differs across the **whole frame**
   (bbox `(0,0,1280,720)`, max delta 7). The control was not a no-op.
2. **The divergence axis is the settle count, not the process.** Re-run with settle 40 against
   settle 90:

```
SDFGI ON  : settle 90 vs 40  ->  500 px differ, max channel delta 1, bbox (32,1,1251,707)
SDFGI OFF : settle 90 vs 40  ->    0 px differ
```

That SDFGI-ON signature — **max channel delta 1, spread over essentially the whole frame** — is an
exact fingerprint match for L7-V's SDFGI result (*129 px, max channel delta 1, bbox
[16, 0, 1275, 716]*). **The instrument is now validated in both directions**: it reads > 0 on a
known accumulator and 0 on the shipped stage. L-N discharged.

> **METHOD NOTE (standing, for every later cell running check 9).** **Run-to-run byte identity at a
> FIXED settle count does not clear the accumulator lockout. SDFGI passes that test.** A progressive
> cascade converges along a deterministic path, so two processes asked for frame 90 both arrive at
> the same partially-converged frame 90 and agree perfectly. The discriminating test is **varying
> the settle count**, which is the axis the accumulator actually lives on. Cells that captured a
> still at a fixed settle and reported "byte-identical" have measured process determinism, not
> accumulator absence — those are different claims and only the second one is check 9.

### 4.3 A correction owed to the brief, in the brief's favour

This cell's brief says *"SDFGI is the determinism-safe GI (the accumulator lockout findings)."*
**The banked finding is the opposite:** L7-V's headline (§0 ★★) is *"GLOW IS INNOCENT. SDFGI is the
accumulator"* — glow is the safe one; SDFGI is what breaks byte-equality. The measurements in 4.2
reproduce L7-V, not the brief. **No SDFGI was enabled on the shipped stage**, which is what the
banked fact actually requires, and glow was left ON and untouched throughout. Flagging it because
a lighting cell acting on the inverted reading would have enabled SDFGI *for the crypt bounce* and
handed the L7 race a nondeterministic stage.

### 4.4 One property deliberately NOT touched, for a cross-consumer reason

`glow_hdr_threshold` stays at **1.25**. Lowering it would let the new torch cores halo, which is a
real register move and was considered. It is declined because that exact constant carries a **Matt
ruling of 2026-06-22** (raised 1.0 → 1.25 so the king's lit white gauntlet stopped blooming like an
emissive), the king rig is not in this scene, and **this cell therefore cannot verify the regression
it would risk.** Logged as considered-and-declined rather than silently skipped.

---

## §5 — Captures, for the Matt-eye checkpoint

All under **`/Users/admin/Games/reincarnated-godot/tmp/pclight/REVIEW/`** — same camera, same render
settings, same resolution for every frame. Kept local, untracked: they show Synty textures and the
`/Assets/Synty/` licence rule forbids a shared remote.

| file | what |
|---|---|
| `01_BEFORE_daylit_court.png` | the defect, as-is |
| `02_AFTER_crypt.png` | **the shipped fix** |
| `03_AB_before_left_after_right.png` | **the pair, side by side, stats burned in** — the one plate to look at |
| `04_VARIANT_cold_skyleak.png` | the S14 variant Matt is asked to rule on (§2.4) |
| `05_TRAJECTORY_contact_sheet.png` | all 14 measured steps in order, each labelled with its numbers — **the curve, as pictures** |

Raw frames: `tmp/pclight/frames/*.png` · per-step stats: `tmp/pclight/stats_*.json` · render logs:
`tmp/pclight/*.log`.

**No aesthetic verdict is offered.** Per charter §7 the after-render is a looked-at-by-Matt gate;
this note's claims stop at the measurements.

---

## §6 — Changed files (PC-T3 discipline — nothing committed in `reincarnated-godot`)

**TRACKED, modified — one file:**

| file | change |
|---|---|
| `scripts/kit_replica_level.gd` | **+56 / −9**, entirely inside `_build_environment()` and `_build_lighting()`. 9 property values + 4 added `OmniLight3D` nodes; the rest is comment. |

The complete value-level diff: `ambient_light_energy` 0.35→0.55 · `Key.light_energy` 2.0→0.0 ·
`Key.light_color` warm→cold *(inert; staged for the S14 variant)* · `Fill.light_energy` 0.45→0.0 ·
`InteriorPool` position.y 2.0→1.35, energy 3.4→10.5, colour (1.0,0.85,0.62)→(1.0,0.58,0.25),
range 9.0→15.0, attenuation 1.3→1.25 · **+4 `CornerSconce_*`** OmniLight3D.

**Scope held:** no geometry, no material, no shader, no prop, no texture, no camera, no kit-table
entry, no invariant (I1–I9 untouched). Lighting only. `fog_density` and `glow_*` end the cell at
their authored values.

**UNTRACKED, new — the cell's instrument (`tmp/` is scratch, none of it is repo product):**
`tmp/pclight/light_rig.gd` · `light_rig.tscn` · `shoot.sh` · `light_stats.py` · `make_plates.py` ·
`frames/` (19 PNG) · `REVIEW/` (5 PNG) · `stats_*.json` · `*.log`

**Repo left clean otherwise.** `git status --untracked-files=no` at cell exit returns **exactly one
line**: `M scripts/kit_replica_level.gd`. The pre-existing untracked state (13 addon trees from
PC-T12/PC-T3, the `.uid` sidecars) is **not touched and not tidied** — it is not this cell's to
resolve. **`project.godot` is unmodified and was never written**; F8 (headless `--import` pruning
default-equal settings) could not fire because no import pass was run. *(Correction to my own
PC-T12 state note, which recorded an uncommitted `[rendering] mesh_lod` deletion as outstanding —
it is not present in the working tree now; verified, not assumed.)*

**`AGENT_STATE.md` in `reincarnated-godot` is deliberately NOT updated.** Writing it would add a
second tracked modification to a repo this cell is instructed not to commit, leaving the next agent
a dirty file with no commit explaining it. **This note is the cell's record.**

### Findings logged, not acted on

- **L-1 — the fix has a twin.** `scripts/walltop_level.gd` (its `_build_environment` +
  `_build_lighting`, ~lines 214–277) carries a **byte-identical copy** of the old lighting block; it
  is the parent `kit_replica_level.gd` was forked from. **The crypt lighting exists twice in the
  repo and this cell moved one copy.** Not propagated: the two files serve different consumers (the
  play-shell and the PNG harness vs the kit-replica ladder), the brief scopes this cell to the L7-V
  stage, and silently re-lighting a second consumer is exactly the blast-radius widening minimal-diff
  exists to prevent. **Conductor's call.**
- **L-2 — the sconces have no fixture.** Four lights nothing in the room makes. That is CEILING-1's
  own pathology in miniature (R-4: *"the pass is the missing SOURCE of a light the room already
  has"*), at roughly 1/20th the energy and mounted at the four existing corner pillars so a brazier
  mesh has somewhere to land. A prop pass is **owed**; it is out of a lighting-only scope. Named in
  the source comment as well as here so it cannot be rediscovered as a surprise.
- **L-3 — the room is still empty.** L7-V's other finding (288 of 296 nodes are floor/wall/post)
  is untouched by this cell and no lighting change can address it.

---

## §7 — Cell summary

| | |
|---|---|
| **Defect** | CEILING-1 — crypt lit as a daylit court, **4.66×** contrast (4.81× on this cell's path) |
| **Measured successor** | **7.63×** — +59 % on this path, +64 % on the number of record |
| **The spatial number** | walked-floor plateau **1.22× → 2.62×** p90/p10 over an identical 82-cell set |
| **Steps** | **14 measured** (S1–S14) + BEFORE + final; **2 rejected on their own numbers** (S8, S12), both retained in the record |
| **Authoring effort** | **5 min 49 s** wall-clock across the 14 steps (~25 s/step, render-bound). Whole cell ≈ 70 min, of which **~80 % was instrument**: locating the authoring surface by evidence, writing the rig, writing LSTAT-1/2, and the determinism controls |
| **Determinism** | **CLEAN** — 5 processes, 1 sha256; settle-invariant; instrument validated in both directions |
| **Diff** | 1 tracked file, +56/−9, lighting only. **Not committed** in `reincarnated-godot` |
| **Owed to Matt** | (a) eye-check the after-render; (b) rule the S14 cold-sky-leak variant; (c) L-1 twin-file propagation |

### The effort finding, which is the part that generalises

**The lighting authoring cost 6 minutes. Everything else cost an hour.** The room was re-lit in 9
property values and 4 nodes, and each iteration was ~25 seconds of render. What was expensive was
(a) establishing *which file* authors the crypt's light — answered by following L7-V's port header
back to `kit_replica_level.gd`, not by assuming — and (b) discovering that the metric of record
**cannot measure the thing being fixed**, and building one that can before touching anything.

Lighting has been every lap's obstacle and never a lap's subject. On this first outing as a subject,
the obstacle was never the lighting. **It was not having an instrument that could tell a dark room
from a bright one** — LSTAT-1 returns 4.81× for both. If lighting becomes a recurring surface
(the handoff's *"cross-cut → own surface"* row), the reusable asset from this cell is not the
crypt's nine values; it is **LSTAT-2, the counter-gate in §2.2, and the check-9 settle-variance
correction in §4.2.**

---

**Signed:** drax (presentation seam), 2026-07-28. Evidence: `/Users/admin/Games/reincarnated-godot/tmp/pclight/`.
