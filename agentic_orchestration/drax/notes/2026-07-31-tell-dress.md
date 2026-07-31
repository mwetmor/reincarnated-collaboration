# TELL-DRESS — the ring measures 12 m, and the substrate the charter pinned has no telegraphs in it

> **Cell:** TELL-DRESS (BR-1 BATON-RENDER §3 cell #5) — the telegraph decal renderer in the trace
> playback path: ground decals at TRUE radius, clock-driven wind-up and burst, element-tinted rim with
> a warm danger lip, `family`-qualified shape switch pre-built for Lap 2, `action_lock` body language,
> boss wind-up body language.
> **Agent:** drax (presentation seam). **Conductor:** gandalf (`RUN-CONDUCTOR`). **Gates:** T-1 … T-5.
> **Date:** 2026-07-31.
> **Contract of record:** `gandalf/notes/2026-07-30-ambient-refit-fold-in.md` (Scopes 1–23) ·
> `gandalf/notes/2026-07-31-baton-render-run-charter.md` (BR-1 §1 S-1, §3 cell 5, R-BR-3) ·
> `legolas/notes/2026-07-30-baton-census.md` (**§2 geometry, §3 flavour, §4 status states, §7 the
> blizzard mis-registration, §9 the three riders**).
> **Inherited:** godot `97cac6d` LOCAL (ahead 13). **Shipped:** godot LOCAL ahead 14, **NOT pushed**.
> **Files touched:** `scripts/wr2_playback.gd` — **ONE file.** Nothing else in the tracked tree moved.

---

## §0 — The cell in six sentences

**The 12.0 m nova now measures 12.0 m on Matt's screen and the number came off the pixels, not off the
mesh:** 33 azimuths walked outward from the telegraph's own projected origin against a decal-peeled
control frame give a mean radius of **11.939 m against a declared 12.000 m — 0.104 m mean error,
0.157 m at p95**, with the five azimuths the 36 m arena wall genuinely eats excluded **by geometry
rather than as outliers**. **The corruption hazard BATON-CENSUS §7 flagged is closed by splitting one
predicate into two**: `shape` decides what is DRAWN, `family` decides what it IS, and only a family
that resolves to `nova` may touch `_nova_verdicts` / `_tell_radius_m` / `_tell_wind_up_s` — so the
Stage-2b blizzard, when it arrives, renders correctly as a circle and enters the escape-rate statistic
NOWHERE. **The decal is driven by the playback clock rather than by `create_tween`**, which is why
"bursts at `fire_tick`" is a measured property (**−1 frame on the real nova, +1 / 0 on the synthetics,
all inside the ±1 tolerance**) instead of a coincidence that held at 30 fps. **⚑ THE CHARTER'S
LAP-1 SUBSTRATE PIN IS WRONG AND THE CELL COULD NOT HAVE RUN ON IT**: `kitcal_g5/g5/traces/` —
the 30 `boss__A__seed74000800-829.jsonl` files BR-1 §1 S-1 names — contain **ZERO telegraph events**
(that battery is BATON-CENSUS's *G-5 BASELINE*, which predates the telegraph channel); the corpus that
carries telegraphs AND the only `action_lock` frames in the tree is **`wr2_battery_after/`**, which the
census itself says in §0 and §4. **Three of my own things went wrong and are written down**: the first
decal build painted a 12 m disc with `no_depth_test` and erased both bodies under it; my glow
attribution for the interior lift was made with a screen-space mask that is not a constant ground
radius at a 53° pitch and is REFUTED by the arm that followed it; and the fallback decal — the arm this
cell exists to build — threw **59 SCRIPT ERRORs** on its first synthetic render, caught by scanning the
log rather than by the frames, which looked right.

---

## §1 — THE SUBSTRATE FINDING (read this before the gates)

BR-1 §1 S-1 pins Lap 1 to
`reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/g5/traces/boss__A__seed74000800-829.jsonl`
and describes them as carrying 19-field telegraphs. Parsed, all 30:

| battery | circle telegraphs | point telegraphs | `action_lock` frames | circle damage |
|---|---:|---:|---:|---:|
| **`kitcal_g5/g5/traces/` (the charter's pin)** | **0** | **0** | **0** | **0** |
| `kitcal_g5/wr2_battery_after/**/traces/` | 1 per fight × 132 | many | **13 per fight** | 1 per fight |

`grep -c telegraph g5/traces/boss__A__seed74000801.jsonl` → **0**. This is not a surprise once you
re-read the census: its §0 table calls `g5/traces/` the **"G-5 BASELINE for the before/after diff"**,
its §8 lists `telegraph` as a **new event type that landed in `after_s11`**, and its §4 says in bold
that the `action_lock` exemplar **"lives in `wr2_battery_after/` (08:25) and nowhere newer."** The
charter transcribed the wrong row.

**Substituted, and declared:** this cell runs on the **`after` battery / `pre` leg / boss / arm A**,
which is the playback harness's own battery of record (`wr2_traceset.gd::BATTERIES["after"]`, engine
pin `f1ab3b09`, git-tracked, Gate-2 CLEAR). **Nothing was regenerated and the engine tree was never
opened for write.**

**Seed selection — `74000806`, and the census that picked it.** All 132 nova firings in that battery
are the SAME event (mint `t_s` 0.700, `fire_tick` 30, `fire_t_s` 3.0188405797101447, `wind_up_s`
2.318840579710145, `shape` circle, `radius_m` 12.0, origin (26.158596, 15.416323), `damage_amount`
218.076) — so the choice is about what happens AROUND it:

| seed (arm A) | nova crossing | `action_lock` | crits | player death |
|---|---|---|---|---|
| 74000802 | **414.80** (2 × 207.40) | 13 frames, t 3.3→4.5 | **0** | 21.8 s |
| 74000804 | 207.40 (1 ×) | 13 frames | 2 | 33.9 s |
| **74000806 (SHIPPED)** | **414.80 = 2 × 207.40** | **13 frames, t 3.3→4.5** | **2** (t 7.4, 11.9) | **23.8 s** |
| 74000815 | 207.40 (1 ×) | 13 frames | 3 | 35.4 s |

74000806 is the only candidate that is simultaneously the **double-spoke crossing** (the worst case the
decomposition exists for), **carries the CC channel**, **carries crits** (so CRIT-RED is not dark) and
is **short**. **The `action_lock` seed the contract asked me to name is `boss__A__seed74000806`, leg
`g5_m4cadence_nova_mitR2proxy_tg_dec_bsep_mv2_ntv2`, ticks 33–45, `remaining_s` 1.2 → 0.**

**⚑ AND THE LOCK DOES NOT STOP HIM MOVING.** Measured on that seed: t=3.5 (28.98, 12.27) → t=4.0
(29.94, 13.80) → t=4.5 (30.90, 15.34), ~2.15 m/s, for the whole 1.3 s. `action_lock` locks ACTIONS
(`gd_nova.py:21-26` applies it in place of an RDR `freeze` because GD's freeze has no shatter
operator); it is not a root. That one measurement is why §4's body language does what it does.

---

## §2 — GATES, tolerances named, then the numbers

**Tolerances (named before the shipped render; the instrument-development passes that exposed the
bloom skirt, the arena clip and the HUD glyphs are §6 and are disclosed there, not hidden in a
tolerance):**

| gate | tolerance |
|---|---|
| **T-1** radius truth | mean \|err\| **≤ 0.15 m** AND p95 **≤ 0.25 m** on a 12.0 m radius (1.25 % / 2.1 %). Justified by the instrument's own floor: the rim band is 0.55 m and one pixel on the far arc is 0.046 m. |
| **T-2** timing truth | decal appears on the frame its event tick is fired; burst frame within **±1 frame** of `(fire_t_s − t_s) × 30 fps`. |
| **T-3** legibility | rim/local-floor luma, same pixel, ship vs decal-peeled control: **median ≥ 2.5** AND **p05 ≥ 2.0**. |
| **T-4** no regression | on a segment the trace carries NO telegraph and NO `action_lock`: ship vs `--tgoff` **≤ the NULL floor + 0.01 % of frame** (≤ 92 px/frame), zero spatial structure; LSTAT-2 sha unchanged. |
| **T-5** qualified switch | synthetic rect renders at its declared extents; synthetic unknown draws a visible fallback AND logs a warning; neither enters `_nova_verdicts`. |

### T-1 — RADIUS TRUTH · **PASS**

Instrument: `tmp/telldress/measure/rim.py` + the in-engine dump `_tg_dump_rim()`. At the last wind-up
frame the renderer writes, for 64 azimuths, the screen projections of the ground points at
**r−0.5 m, r, r+0.5 m** using the live CAM-LOCK camera. Python then walks each radial in the shipped
frame, differences it against the **`--tgoff` control frame** (identical render, decal layer peeled),
and takes the rim's outer edge at the **half-maximum** of that difference. The pixel offset is
converted to metres by **that azimuth's own 1.00 m baseline** — no global px/m constant appears
anywhere, because at a 53° pitch the near arc and the far arc are at wildly different scales and one
number for both IS the error.

| | |
|---|---:|
| declared `radius_m` | **12.000 m** |
| **measured mean radius** | **11.939 m  (−0.51 %)** |
| mean \|err\| | **0.104 m** |
| p95 \|err\| | **0.157 m** |
| max \|err\| | 0.495 m (one azimuth) |
| median \|err\| | 0.074 m |
| azimuths: sampled / in frame / eaten by the arena wall / **measured** | 64 / 38 / 5 / **33 (51.6 %)** |
| bloom skirt beyond the half-max edge (reported, NOT scored) | 0.299 m mean |

**Two exclusions, both by construction and both counted:**
1. **26 of 64 azimuths are off-frame** — the 12 m ring DOES NOT FIT at CAM-LOCK and that is the camera's
   whole point (GAL-CAM §5: the near arc runs 191 rows off a 1080p bottom edge; the referent player
   answered novas partially blind on the near side). Widening to fit would destroy the thing the camera
   reproduces. Coverage is stated, never a silently-shrunk sample.
2. **5 azimuths are eaten by the 36 m arena wall.** Origin (26.159, 15.416) + 12 m runs to x = 38.16, so
   the east arc has no floor to lie on. The renderer draws the disc whole and the wall face crosses it —
   the honest picture, and the banked nova was clipped in all 132 firings. Computed from the geometry
   (`0 ≤ x,y ≤ 36`), not discovered as outliers.

**Plate:** `plates/PLATE_T1_radius_truth.png` — every sampled azimuth ringed green/amber/red by its
error, the arena-eaten ones crossed magenta, all the numbers on the frame.

### T-2 — TIMING TRUTH · **PASS**

Every decal's ledger row is printed by the render itself (`_tg_print_census`). Frames at 30 fps:

| decal | family (source) | shape → kind | tick → `fire_tick` | frames | expected | **err** |
|---|---|---|---|---|---:|---:|
| real nova | `nova` (attack_id) | circle → circle | 7 → 30 | 51 → 120 (69) | 70 | **−1** |
| mob melee ×3 | `melee` (shape) | point → circle | n → n | d = 0 or 1 | 0 | **0 / +1** |
| synthetic wave | `wave` (attack_id) | rect → rect | 60 → 80 | 209 → 270 (61) | 60 | **+1** |
| synthetic bloom | `eldritch_bloom` (**family rider**) | hexagram → unknown | 100 → 120 | 330 → 390 (60) | 60 | **0** |

The decal also SPAWNS on the frame its tick is fired (`spawn_play_t` 0.7333 against an event `t_s` of
0.700 — the next rendered frame after the tick crosses, which is the earliest a frame can show it).
The point telegraphs' d = 1 is the `fire_tick == tick` convention: they resolve on the tick they are
announced, so the decal is a one-frame flash and the ±1 is quantisation, not drift.

### T-3 — LEGIBILITY · **PASS**

Same instrument, same frame, same pixels: **luma(ship) / luma(control) at the rim's peak pixel**. The
denominator is the actual local floor at that spot — cold pool, torch throw or shadow, whatever is
genuinely there — not an annulus chosen to flatter the ratio.

| | |
|---|---:|
| **median rim / floor** | **× 3.355** |
| p05 | × 2.546 |
| min | × 2.228 |
| rim luma (mean) | 198.4 |
| floor luma (mean) | 58.1 |

Scored on median and p05 rather than mean, **and that choice is stated because the mean is garbage
here**: the crypt floor legitimately goes near-black between torches, a handful of samples therefore
return ratios in the hundreds, and the arithmetic mean is a number about those samples only.

### T-4 — NO REGRESSION · **PASS**, and the zero had to be EARNED

Window: trace **t 8.0 → 11.3 s** of the shipped seed — censused as carrying **no telegraph** (they are
at ticks 0, 7, 53, 68 only) and **no `action_lock`** (ticks 33–45 only). Arms: ship · `--tgoff` (decal
AND body language peeled) · NULL (ship inputs, second process launch).

**⚑ THE FIRST PASS FAILED, AND THE FAILURE WAS THE INSTRUMENT.** Raw ship-vs-`--tgoff` returned
**393,347 differing pixels over 10 frames — and the NULL returned 379,074.** The diff image named the
culprits in one look: the damage numerals (whose pop/rise is `create_tween` on the WALL clock, so two
launches catch them mid-flight at different phases) and the sky dust (unseeded `GPUParticles3D` — the
same landmine SHADOW-UNIFY's ρ census hit at 20,757 px). A single NULL cannot MASK those, because a
moving mote occupies different pixels in different pairs. So they were peeled **at the author**, and a
third author showed up when the first two left: the room ambient particle dressing.

| arm | ship vs `--tgoff` | NULL |
|---|---:|---:|
| raw | 393,347 px | 379,074 px |
| + `--nodust --nonum` | 227,604 px | 217,908 px |
| **+ `--noambient` (SHIPPED MEASUREMENT)** | **29 px** | **1 px** |

**29 px across 12 frames of 921,600 = 0.00026 %, worst channel 17, and no spatial structure** —
isolated single pixels in the upper frame, values almost all 1 (`(975,29)=1 · (971,65)=1 · (751,151)=12
· (784,74)=1 · (782,85)=17`). Below the tolerance and, honestly, **not chased to zero**: the layer
writes identical values to identical materials on those frames and the residual is renderer noise on
the beam's screen-space fade. Three new one-word peels are the by-product and they belong to every
future cell: `--nodust`, `--nonum`, `--noambient`. **Measurement arms turn them on; deliverable clips
never do.**

**LSTAT-2 — NO DELTA.** L7 stage sha256 **`5d4fa240cb0ead2c…` → `5d4fa240cb0ead2c…`**, the same value
BEAM-CONE and SHADOW-UNIFY banked; pixel diff **0 of 921,600, max channel 0**. It is zero for a
structural reason worth saying rather than letting the zero look bigger than it is: **this cell touched
exactly one file and it is not on the L7 path.**

### T-5 — THE QUALIFIED SWITCH · **PASS**

Two records the schema says are possible and no trace on disk contains, built from
`spatial_engine.py` and fed through the SAME `_fire_events` path a real record takes:

| synthetic | fields | family resolved | rendered | in `_nova_verdicts`? |
|---|---|---|---|---|
| **rect** (`primordian_wave` shape) | `shape:"rect"`, `orientation_rad` = caster heading, `range_m` 14.0, `width_m` 5.0, `radius_m: null` | **`wave` via `attack_id` `:wave:`** | box on the floor at the declared extents, sweep growing along its length, four-bar rim | **no** |
| **unknown** | `shape:"hexagram"` (no producer writes it) + `family:"eldritch_bloom"` (no Lap-1 trace carries it) | **`eldritch_bloom` via the `family` RIDER — the Lap-2 path, exercised** | magenta disc + magenta cross + floor caption naming shape and family verbatim | **no** |

Warning emitted verbatim, once:
`[wr2/tell] ⚑ UNKNOWN TELEGRAPH shape='hexagram' family='eldritch_bloom' — FALLBACK DECAL DRAWN (never dropped). keys=[…]`
Census line: `family 'eldritch_bloom' x1 [unqualified (rendered, counted in NOTHING)]`.

**The rect is a CORRECTION, not just an implementation.** The inherited `else` branch built a
`BoxMesh(width, 0.04, range)` **centred on the origin** — which for a wave that runs FROM the caster
TO `range_m` draws half the wave behind the boss. It is offset forward by `range/2` now. Flagged as a
**source read**: no rect trace exists, so re-verify §7 against data before trusting it.

---

## §3 — WHAT I SHIPPED FOR COLOUR AND ANIMATION, and why

### 3.1 The ring style: **explicit static rim + a moving front band**

The contract left ring-expansion vs fill-sweep open. Shipped **both, because they answer different
questions**, and the split is the design:

- **A STATIC OUTER RIM at the true radius, from the first frame** — the WHERE. A ring that only grows
  into its final size tells you where the edge is at the moment it is too late to leave. D3 and Lost Ark
  both draw the full footprint immediately; that IS the affordance.
- **A FRONT BAND travelling 0 → `radius_m` over `wind_up_s`, arriving at the rim exactly at
  `fire_tick`** — the WHEN, readable peripherally, coinciding with the WHERE at the instant that matters.
- **A shock at the burst**: the band overshoots to 1.16 × radius and fades over 0.32 s of TRACE time,
  the rim flashes white-hot, then everything is freed. It is the only moment anything crosses
  `radius_m`, and it is gone in ten frames.

**⚑ THE FRONT IS A BAND BECAUSE TWO EARLIER BUILDS WERE WRONG IN THE SAME DIRECTION.** Build 1 ran the
sweep as a filled disc at α 0.30 → 0.48: a 12 m disc at CAM-LOCK covers most of the visible floor, and
the frames read as a pale wash that erased the room, the pools and the cone beams — a decal that
destroys the scene it is a decal ON. Build 2 halved it and still read as a grey circle laid over the
room. The band also happens to be the truer picture: the sim's nova IS a ring front travelling at
14.0 m/s (`spatial_engine.py:6028-6033`), not a disc that fills. **The band's RATE is still not read
from the trace** — census §5 is explicit that there is no spawn/travel/impact event and `v` is not a
field — so it spans `wind_up_s` and is declared as a **presentation clock, not the sim's 14.0 m/s
front.**

### 3.2 The colour: cold from `SKY_COLOR`, with a warm danger lip — the escalation, fired

`TG_COLD = KRLS.SKY_COLOR (0.620, 0.740, 1.000)` — **read from the level's own constant**, the same one
the floor pools, the cone beams and (RIVAL-CAST) the boss's cold emissive are authored on. One
temperature by construction, not by eye.

**And cold-on-cold DID fail, exactly as the contract anticipated.** The escalation shipped is a
**two-band rim, both bands INSIDE the true radius so the lit rim's outer edge IS `radius_m`**:

| band | extent | colour |
|---|---|---|
| core | `[r − 0.55, r − 0.14]` (0.41 m) | `SKY_COLOR` lightened 0.50 — the element identity |
| **warm danger lip** | `[r − 0.14, r]` (0.14 m) | **`(1.00, 0.46, 0.14)` — NOT an element colour** |

The lip is what survives a cold floor pool; the core keeps the ring element-true. Result: **× 3.355
median rim contrast** against a floor that is itself cold.

**⚑ THE PRICE, MEASURED, AT MATT'S EYE.** The decal lifts the floor INSIDE the ring to **× 2.02** of
its unlit value at the worst-case frame (median over 37 azimuths sampled 5.0 m inside the rim; ship
107.97 vs control 53.42). Attributed by an arm that draws nothing inside: with the fill and sweep
alphas set to **0.000** the same measurement still reads **× 1.410**, so **roughly half the interior
lift is bloom spreading inward from a 198-luma rim, and half is the fill geometry.** That is the price
of T-3, it is legible and intentional, and it is a one-constant retreat in either direction
(`TG_FILL_A` / `TG_SWEEP_A`) if his eye says the room matters more than the ring for 2.3 seconds.

### 3.3 `action_lock` body language — and the one thing it refuses to do

**It never moves a body.** `x_m`, `y_m` and `heading_rad` are trace facts assigned four lines above the
call; everything the layer writes goes to the body's CHILD mesh as scale / lean / colour — channels the
schema does not carry, so nothing here can contradict a field. **That is why the lock does NOT nail him
to the floor**, which was the obvious "legible" choice and would have been a lie (§1: he moves 2.15 m/s
for the whole lock).

Shipped, in order of legibility: **(1)** an **anim hold** — `AnimationPlayer.speed_scale = 0` if the
body owns one; **(2)** a **flinch** — a damped lean-back impulse, `0.16 rad · e^(−τ/0.21) · sin(22τ)`,
one impulse per lock onset; **(3)** **rime** — a ground ring at the body's own `entity_radius_m` in the
DECAL's family colour, pulsing, with the proxy's emissive and 35 % of its albedo pulled toward that same
colour. The rime reads the colour **off the telegraph that caused it**, not off a second literal.

**⚑ ARM (1) IS DARK IN THIS PATH AND THAT IS A DECLARED LIMIT, NOT A PROMISE.** The playback bodies are
**capsule proxies** — rig integration is BR-1 cell #7 / R-BR-2 — so there is no `AnimationPlayer` to
pause. The branch is written, guarded, and reached by node lookup rather than a stored handle, so the
rig swap does not have to remember to wire it. On a capsule, the flinch and the rime are the half a
capsule CAN act, and they are what makes the lock read at CAM-LOCK today.

**And this is the first time anything in this seam has READ the CC channel at all.** Census §8 measured
the consumer's coverage of `ailments` as **0** — carried by the producer since the G-5 baseline, read
by nobody. It is read now.

### 3.4 Boss wind-up body language

During `[t_s, fire_t_s]` the attacker reads as **gathering**: a crouch (−17 % height, +6 % width), a
0.17 rad backward lean, and a rising cold charge on the emissive, all keyed to
`k = (t − t₀)/(t_fire − t₀)`; then a **snap forward** on release decaying over 0.25 s. Only a telegraph
with a REAL window arms it (`fire_t_s − t_s > 0.05`) — the point tells resolve on the tick they are
announced, and drawing a charge for them would be inventing half a second the fight never had. **So the
2.3188 s is attributable to the boss's body and not only to the floor**, which was the ask.

Emissive energies were pulled down twice: the first build ran the charge to ×4.2 and the boss blew out
to white against the burst.

### 3.5 What the decal does NOT draw

`telegraph.damage_amount` is present on 100 % of telegraph events and the WR2 pip that printed it
(**"announced 218.076 · r=12.0 m · tell 2.32 s"**) is **RETIRED FROM THE DEFAULT** per the contract —
numerals belong to `damage` events and the Bangers stack, and a second numeral font on the floor
competes with the one telling the truth about a hit that actually happened. It peels back on with
`--tgpip 1`; the code and its provenance comment are kept, not deleted.

---

## §4 — THE QUALIFIED SWITCH, as code

The census caught this seam's own D-F4 shape at what was then `wr2_playback.gd:2435`:

```gdscript
var is_ring := (shape == "circle") and rad_v != null      # ONE test, TWO questions
```

Shipped:

```gdscript
var is_ring: bool = (shape == "circle") and rad_v != null   # GEOMETRY only
var fq := _tg_family(ev)
var is_nova: bool = (String(fq["family"]) == "nova") and is_ring   # the ONLY gate on the statistic
```

**Precedence ladder (`_tg_family`)** — (a) the `family` rider [Lap 2; absent from 100 % of the 785
traces on disk] → (b) the `attack_id` `:mechanic:` segment [Lap 1's only discriminator, reported as
`source=attack_id` on every decal so nobody later reads it as a field] → (c) `shape` + context, which
**refuses to promote a bare circle** and returns `circle?` → (d) `unknown` → the loud fallback. When (a)
and (b) are both present and disagree, the rider wins **and the disagreement is warned**, never
swallowed.

A circle that is not a qualified nova prints, verbatim:
`[wr2/tell] circle telegraph with family '…' (source …) — RENDERED at r=… m, EXCLUDED from _nova_verdicts / _tell_* (BATON-CENSUS §7)`

**That is the blizzard's branch, and the sentence it will print.**

---

## §5 — CONSTANTS AND PEELS

| constant | value | why |
|---|---|---|
| `TG_COLD` | `KRLS.SKY_COLOR` | read, not typed — one temperature family |
| `TG_RIM_W` / `TG_RIM_LIP` | 0.55 m / 0.14 m | rim INSIDE r, so the lit outer edge IS `radius_m` (T-1) |
| `TG_DANGER` | (1.00, 0.46, 0.14) | the warm lip; the declared contrast escalation |
| `TG_FILL_A` / `TG_SWEEP_A` | 0.050 / 0.050, **non-emissive** | interior is huge area → low alpha (§3.2) |
| `TG_BAND_A` / `TG_BAND_F` | 0.34 / 0.78 | the moving front; 2.64 m wide at r = 12 m |
| `TG_BURST_S` / `TG_BURST_GROW` | 0.32 s (TRACE) / 1.16 × | the shock, then clean removal |
| `TG_FAMILY_ELEMENT` | nova/blizzard/wave → cold, melee → physical | **TODO(drax): delete and read `ev.element` when the engine ships element on the telegraph** (census §9) |
| depth test on the decal | **ON** | opposite of the marker-layer rule, deliberately — §6.1 |

**New peels (one word each, same law):** `--tgoff` (the whole tell) · `--tgpip 1` (the WR2 announced
pip) · `--tgmeasure 1` (the per-decal ledger) · `--tgsynth rect|unknown|both` (T-5 injection, **declared
in capitals on the frame banner**) · `--tgdump <path>` (the T-1 rim samples) · `--nohud 1` ·
`--nodust 1` · `--nonum 1` · `--noambient 1`. **All earlier peels survive unchanged.**

---

## §6 — MY OWN FAILURES, in the order they happened

1. **The decal painted over the bodies.** The first build gave every decal surface
   `no_depth_test = true`, copying the footprint-ring / HP-bar marker-layer rule. Those markers are ~1 m
   wide and an occluded 1 m ring says nothing; a **12 m disc drawn that way erased both capsules and the
   walls**, destroying the one thing it exists to answer ("where is the boss relative to the danger?").
   A telegraph is a mark ON THE FLOOR and must be occluded by anything standing on it — **that occlusion
   IS the spatial information**. Caught in the first frame I looked at.
2. **Two wash builds** (§3.1) — recorded as constants with the rejected values in the comment.
3. **A refuted attribution.** I explained the interior lift as bloom from the rim, ran `--noglow`, got
   "3.9 %", and wrote it down. It was measured with a screen-space polygon scaled toward the projected
   origin — **which is not a constant ground radius at a 53° pitch**. The arm that replaced it (fill and
   sweep alpha → 0.000, sampled per-azimuth with each azimuth's own local scale) says **half the lift
   is bloom**. The first reading is superseded and is recorded as superseded in
   `measure/T3b_interior_lift.json`.
4. **I broke the fallback arm the cell exists to build.** The unknown decal has `"sweep": null`, and the
   wind-up path assigned `.scale` to it unguarded: **59 SCRIPT ERRORs on the first synthetic render.**
   The frames looked correct throughout — it was caught by `grep -c "SCRIPT ERROR"` on the deliverable
   log, which is now the reason that grep is in the guard list rather than a habit. Fixed, re-rendered,
   0 errors; the nova clips were re-rendered at the fixed revision too so every shipped clip comes from
   the shipped code.
5. **A wrong emission theory, cheaply disproved.** I believed Godot's `EMISSION` was doubling the fill's
   source brightness under `SHADING_MODE_UNSHADED` and made the interior surfaces non-emissive on that
   basis. The measurement after the change was **unmoved**. The change is kept (a non-emissive fill is
   the right thing regardless) but the reasoning that motivated it is not supported by the numbers, and
   the comment in the code says so.

---

## §7 — DELIVERABLES — `~/Games/reincarnated-godot/tmp/telldress/` (86 MB after prune)

**M-EYE, MOTION FIRST. CAM-LOCK on every clip, camera identity AND the TELL-DRESS grammar line printed
on every frame. The HUD is ON in every deliverable and OFF in every measurement arm — never both.**

1. **`clips/TELLDRESS_before_after_watch_CAMLOCK.mp4`** — **WATCH THIS FIRST.** The decal-peeled
   depiction beside the shipped one, same trace, same frames, same camera, one variable.
2. **`clips/TELLDRESS_nova_cycle_CAMLOCK.mp4`** — 190 frames, trace t 0.00 → 6.33 s: mint at 0.700 →
   front growth → **BURST at `fire_tick` 30 (t 3.0188)** → aftermath → `action_lock` 3.3 → 4.5 → the
   2 × 207.40 numerals → release. **Both bodies in frame throughout** (boss 1.5–3 m from the player).
3. **`clips/TELLDRESS_action_lock_x3slow_CAMLOCK.mp4`** — the lock moment at ⅓ rate so the flinch
   impulse and the rime ring separate by eye. A **video** slow-down (`setpts`), not a sim one: the same
   frames clip 2 contains. **Seed `boss__A__seed74000806`.**
4. **`clips/TELLDRESS_synthetic_shapes_CAMLOCK.mp4`** — 380 frames: the real nova, then the **synthetic
   rect** (t 6→8) and the **synthetic unknown** (t 10→12). Banner declares the injection in capitals.
5. **`plates/PLATE_T1_radius_truth.png`** — the fastest read: every azimuth ringed by its error, the
   arena-eaten arcs crossed magenta, all the gate numbers on the frame.

**Keyframes:** `keyframes/TD_nova_{windup,prefire,burst,lock}.png` · `TD_synth_{rect,unknown}.png`.
**Instruments:** `measure/rim.py` · `measure/rim_M.json` · `measure/T1_T3_ship.json` ·
`measure/T3b_interior_lift.json` · `measure/T4_noregress.json` · `l7/l7_telldress.png` ·
`render_deliverables.sh` · `logs/`.

---

## §8 — GUARDS

| guard | result |
|---|---|
| collision check at cell start | clean, HEAD `97cac6d` as expected |
| declared authorised surface | **`scripts/wr2_playback.gd` ONLY** — 1 file, `M`, no `.uid`, no stray probes |
| `project.godot` sha256 | `6bef17eb…` — **NO DELTA** (SHADOW-UNIFY's banked value) |
| `walltop_void_radial` / `walltop_occlude` shaders | `2710fc11…` / `d29a01be…` — unchanged |
| `sky_shaft` / `sky_dust` shaders | untouched — this cell draws decals, not beams |
| all `vfx/ambient/**` rollup | **`e049676b…`** — byte-identical to BEAM-CONE and SHADOW-UNIFY |
| prior cells' clips | beamcone ×4, beamfix ×5, rivalcast ×1, shadowunify ×6 — **intact** |
| engine tree | **never opened for write**; traces read-only |
| `SCRIPT ERROR` / `Parse Error` scan on every shipped deliverable log | **0** |
| LSTAT-2 | sha unchanged, 0 px |
| disk | `tmp/telldress` **86 MB** after prune; peak intermediates ~900 MB, well under the 2 GB ceiling; every PNG sequence encoded then deleted |
| godot commit | **LOCAL, ahead 14, NOT pushed** |

---

## §9 — AT MATT'S EYE / ROUTED

1. **⚑ CHARTER AMENDMENT (conductor's, not mine): BR-1 §1 S-1 names a battery with zero telegraphs.**
   The Lap-1 substrate for anything telegraph- or CC-shaped is `kitcal_g5/wr2_battery_after/`, not
   `kitcal_g5/g5/traces/`. Worth fixing in the charter before cell #7 selects the watch fight on the
   wrong pin (R-BR-4 requires a nova AND a crit AND a death — the G-5 baseline can supply none of them).
2. **Interior floor lift × 2.02 inside the ring for 2.3 s**, half of it bloom off the rim. Legibility
   trumping ambience, as ruled — but it is the biggest thing the cell does to the beautiful corner, and
   it retreats on one constant.
3. **The warm danger lip is a NON-ELEMENT colour on an element-tinted decal.** Deliberate and measured
   (it is what beats cold-on-cold), but it is a taste call and taste calls in this run are veto-open.
4. **`--tgsynth` writes events into the depiction.** Guarded by a capitalised banner line, but it exists,
   and the run should know it exists.
5. **Lap 2 is still shut** (G-5): `wr3_stage2c/` is on disk and contains **zero `.jsonl`**. The
   `family` path is built and PROVEN (the synthetic bloom resolves through the rider), so when
   rider-bearing traces land the switch changes behaviour with no code change.
