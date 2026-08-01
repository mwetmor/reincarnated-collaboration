# LAP-2C RESTAGE — the final integration cell of run BR-1 (BATON-RENDER)

**drax · presentation seam · 2026-08-01 · conductor gandalf (RUN-CONDUCTOR)**
**Opened at godot `136ff81` (BODY-PROBE) — collision check CLEAN, no foreign commits on the head.**
**Charter target T-2. Substrate frozen: `tmp/wr3acc/traces/boss__FULL__seed74000909.jsonl`, opened READ-ONLY.**

---

## THE WATCH

> **`/Users/admin/Games/reincarnated-godot/tmp/restage/clips/LAP2C_WATCH.mp4`**

One integrated fight, start to the boss's death, in the crypt corner at the CAM-LOCK camera.
1600×900 · 1,264 frames · 42.13 s · **with audio**. Werewolf at parity ×1.29 on the authored
melee set, Arsenal CORE + Binbun SHELL + native charge glow and player aura, 50 cleared SFX on
the render's own beat ledger, hit-stop on three beat classes, HUD at grade C, end card.

Second camera arm, R-BR-20, identical in every other respect:
**`/Users/admin/Games/reincarnated-godot/tmp/restage/clips/LAP2C_WATCH_JUICE.mp4`**

⚑ **R-BR-21's named FAIL condition is Matt's to fire and this note does not pre-empt it.** If the
werewolf's strike still reads weaker than its own jump on that clip, the ruling pre-commits to the
Undead Knight. `--body knight` is one flag and both bodies bind the identical 16/18 clip set, so
it is a re-render, not a rebuild.

**No aesthetic self-verdict is taken anywhere in this note.** What binds, what fires, what
measures — measured. Whether it *looks* right is Matt's, in motion.

---

## §0 — The cell in nine sentences

1. **`land_hard` is gone from the tree, not out-ranked in it.** The werewolf's row was deleted
   from `STRIKE_CLIP_BY_BODY`, so the pounce is never loaded into its library and no branch of
   `strike()` can reach it. The three authored combo slices fired **16 / 16 / 16** — round-robin,
   deterministic, 112 of 126 tracks bound.
2. **G-7 answers 0.0000 m.** The boss's volume never touches room geometry anywhere along his
   trace path, so R-BR-22's disrepair edit is **not made**. ⚑ My first run of that gate said
   0.1849 m on 84 of 298 frames, and 81 of those 84 were **the floor slab** — see §5.
3. **R-BR-23 reconciles, and no `RIG_BOSS_H` edit is made.** 1.5278 is a ratio of two
   **constants**; 1.46 is a **rendered** ratio; this render measures the rendered mean at
   **1.4571**. GD-PARITY's own note already published both numbers in one row.
4. **`family` is a REAL rider on this trace — 9/9 — which refutes F-BR-2's standing claim** that
   the seam drops it and that no future trace could carry it. `icearmor` is real too (120/361
   boss ticks). `attack_id` is 4/57 on damage, and one of those four joins the nova. §4.
5. **The conductor's SFX table names a 2.32 s wind-up; this trace's is 0.8500 s.** A charge cut
   to 2.32 s would have outrun every tell in the watch by 1.47 s — the exact lie R-BR-16 forbade,
   arriving through a constant rather than through an asset. §6.
6. **Hit-stop drift is 1.11 %, not the 17.04 % my own first instrument printed.** The first
   version rolled the two deliberate cinematic holds into "drift". §7.
7. **The player aura was wrong twice and both are on the record** — first 17.5 m across, then a
   filled disc hiding the player's legs. Then I blamed it for a warm core it does not cause: the
   peel measures its whole contribution at **+0.3 % of the player box's luma**. §8.
8. **G-VFX PASSES** — 17 beats, 0 collapse — and a statistic the gate did not register says the
   shell works by **occlusion, not addition**, which is not the mechanism R-BR-17 described. §9.3a.
9. **G-6: 20 rows, 0 silently missing.** §12.

---

## §1 — BODY (R-BR-21): the werewolf ships, `land_hard` is unreachable

### 1.1 What was wired

`data/bp_melee_lib.res` — BODY-PROBE's seven sliced clips — is bound into the `loco` library as
`m_attack_1..3 / m_hit_react / m_guard / m_guard_hit / m_knockback`, on the two bodies BODY-PROBE
bind-tested (`MELEE_BODIES`). `--body werewolf|knight` is the single flag; both bodies bind the
identical set, so the swap is a re-render.

**Measured bind, this render, on the shipping werewolf:**

| | |
|---|---:|
| slices bound | **7 / 7** |
| tracks resolving to a real bone | **112 / 126 = 88.9 %** |
| `land_hard` in the library | **NOT PRESENT** |

112/126 is exactly BODY-PROBE's 16/18 per clip × 7 clips. The 14 misses are `Hat_jnt` /
`Hat_jnt1` × 7 — headgear attach points, correctly unmapped.

### 1.2 Which slices actually FIRED, which were only BOUND

Two different claims, and the render counts both:

| slice | bound | fired |
|---|---|---:|
| `attack_1` | ✓ | **16** |
| `attack_2` | ✓ | **16** |
| `attack_3` | ✓ | **16** |
| `hit_react` | ✓ | **4** |
| `guard` | ✓ | **0 — no block/parry beat in this trace to drive it from** |
| `guard_hit` | ✓ | **0 — same** |
| `knockback` | ✓ | **0 on the player; drives the death lead-in, and the player does not die** |

48 combo swings against 50 player-sourced damage events: two land while the body is charging or
dead and are correctly suppressed by the rig's own guards. `hit_react` fires 4 times against the
7 hits the player took — and only the player can flinch, because only the player's body binds
this library; the Fantasy Rivals cast is a different rig family and was never bind-tested against
it. **Binding it anyway would have been asserting an untested bind**, so the mobs keep their
measured incumbent clips and the log says which is which.

### 1.3 Why the deletion is stronger than a demotion

`land_hard` measured **+2.0230 m** forward on the werewolf against the authored strike's
**+1.3231 m**. It is a *landing* clip; its extra 0.70 m is a forward **lunge**, and that lunge is
what Matt read as *"mildly jumping forwards and attempting to scare the monsters but not striking
them"*. Reach and strike-reading are different quantities here and the larger number was the worse
clip. Out-ranking it would have left it one refactor away from returning. The row is deleted.

⚑ **R-BR-21's named FAIL condition is live and this cell does not pre-empt it.** If, on
`LAP2C_WATCH.mp4`, the werewolf's strike still reads weaker than its own jump, the ruling
pre-commits to the knight. That is Matt's read to make; `--body knight` costs a re-render.

---

## §2 — PARITY ×1.29 (R-BR-22), full cast

One multiplier on every body's target height **and on every body's stride ladder with it**,
because implied ground speed is linear in uniform scale. Scaling a body without scaling its ladder
re-introduces the moonwalk MOB-CAST spent a cell retiring.

| body | target before | **target at ×1.29** |
|---|---:|---:|
| player (werewolf) | 1.800 m | **2.322 m** |
| swarm | 1.650 m | 2.129 m |
| elite | 2.000 m | 2.580 m |
| troll | 2.150 m | 2.774 m |
| hero boar | 2.300 m | 2.967 m |
| **boss (golem)** | 2.750 m | **3.548 m** |

The carried lamp scales with the body (`CARRY_H` 1.42 m and `CARRY_OUT` 0.72 m are a *shoulder*
and an *arm's length*, not metres — SHADOW-UNIFY chose them as fractions of a 1.80 m body and
measured the silhouette lift they buy). `PLIGHT_RANGE` is **not** scaled: it is a WARMTH parameter
under R-BR-11 and this cell is forbidden to move one. Named, not smuggled.

### 2.1 G-7 — the pre-registered interpenetration gate

Measured **along the boss's trace path**, on his **alive** frames only, with the boss's body as a
cylinder at his trace radius × parity rather than as the AABB of a splayed golem.

| | |
|---|---:|
| alive frames sampled | 268 |
| floor meshes classified OUT of the obstacle set | 3,087 |
| max rendered top | 4.074 m |
| wall course | 3.006 m |
| **MAX INTERPENETRATION ALONG THE PATH** | **0.0000 m** |

**The disrepair edit is NOT MADE.** The boss stands 0.55 m over the wall course and his path never
brings his volume into it. A boss too large for the room is not a defect in a crypt; *visible
interpenetration* would have been, and there is none. Height against a datum was always a proxy;
this is the thing the proxy stood for.

⚑ **Consequence for Scope 39, stated rather than left implied:** R-BR-22 offered the broken beam
as a *cause* for the ceiling-crack slits. G-7 says there is no beam to break — `kit_replica_level`
states in its own header that **the room has no ceiling mesh**, and BEAM-PIN2 retired the "2.40 m
beam base" to −0.60 m under a Matt ruling, so the constant BODY-PROBE drew a datum stick against
is **stale by two cells**. The slits therefore still want a cause, and this cell did not invent
one. Routed.

---

## §3 — R-BR-23: reconciled, and the lever stays where it is

**HOLD SATISFIED. No `RIG_BOSS_H` edit made.**

Three statistics, measured in this render:

| # | statistic | value | what it is |
|---|---|---:|---|
| 1 | **TARGET-height ratio** | **1.5278** | `RIG_BOSS_H / RIG_PLAYER_H` = 2.75/1.80. A ratio of two **constants** — which is exactly why BODY-PROBE read it identically at ×1.00, ×1.15 and ×1.29 |
| 2 | **RENDERED MEAN-height ratio** | **1.4571** | the quantity GD-PARITY's **1.46** measures |
| 3 | RENDERED MAX-height ratio | 1.5594 | peak pose over the whole fight; comparable to neither |

Per body:

| body | target | rendered mean | rendered max |
|---|---:|---:|---:|
| player | 2.322 m | 2.330 m (+0.36 %) | 2.613 m (+12.51 %) |
| boss | 3.548 m | 3.395 m (−4.29 %) | 4.074 m (+14.85 %) |
| elite (medusa) | 2.580 m | 2.581 m (+0.02 %) | 2.699 m (+4.61 %) |

**There was never a disagreement.** GD-PARITY's own note publishes both numbers **in one row** —
*"boss height ÷ player height | GD 1.46 | ours (measured) 1.46 | ours (analytic ladder) 1.53"*.
The analytic ladder **is** the target-height ratio. BODY-PROBE re-derived the constant ratio and
compared it against the pixel ratio.

**The gap is attributable and small:** `target_height` scales a rig so its **rest-pose** AABB
equals the target; the eye reads an **animated** silhouette. GD-PARITY measured the werewolf
rendering +4 % of its target and the golem −0.4 %; 1.5278 × (0.99686 / 1.0405) = **1.4638**, the
published figure to three decimals. This render reproduces the same structure independently
(+0.36 % / −4.29 % → 1.4571).

⚑ **Pulling `RIG_BOSS_H` to "fix" (1) would push (2) — the ratio an eye actually sees, and the one
another instrument says is already GD-correct — AWAY from 1.46.** That is the wrong lever, and the
hold was right to stop it.

---

## §4 — RIDER CENSUS: honest, and one standing finding is refuted

Charter T-2 wants three riders visibly consumed. **Censused on this trace first, then consumed
where present, then declared where absent.**

| rider | present? | consumed how |
|---|---|---|
| **`icearmor`** | **YES — `wr3_icearmor` on the boss, 120 of 361 ticks (33.2 %)**, first at t=1.00 s, `element: cold`, carried in `ailments[]` | the ward ring (a breathing annulus at 2.05× the body radius, distinct from the rime lock's 1.45–1.63× and on a different period) — **inherited live from stage-2 close, verified firing on this seed** |
| **`family`** | **YES — 9 of 9 telegraphs**: blizzard ×3 · nova ×3 · wave ×3 | qualifies `is_nova` (so the blizzard cannot be scored as a nova), colours the tell, keys the charge-glow window, and selects the resolve SFX |
| **`attack_id`** | **PARTIAL — 9/9 on telegraph, 4/57 on damage** | identifies the **boss ultimate connect** hit-stop class (`…:nova:2`, t=19.70) and joins 4 telegraphs to their damage |

### 4.1 ⚑ F-BR-2 IS REFUTED ON THIS SUBSTRATE

The ledger's F-BR-2 (2026-07-31) states that `TelegraphSpec.family` *"is minted engine-side and
then DROPPED at `ReplicaFrameSink.telegraph()` — 0 occurrences in 13,573 records"*, and concludes:
**"NO future trace can carry `family` until the engine seam is fixed"**. G-5's 3-rider census was
amended to route around it.

**This trace carries `family`, populated 9 of 9.** Whatever fixed the seam, it is fixed on the
`wr3_acc` acceptance cohort. The G-5 amendment can be un-amended, and the substitute
(TELL-DRESS's substring sniff) is not needed here — the renderer reads the field.
→ **routed to knight-rider / the conductor: F-BR-2's forward-looking clause is stale.**

### 4.2 ⚑ HUD-BUILD's telegraph join is wrong on one row, and `attack_id` is what says so

HUD-BUILD §3.2 cross-checked telegraphs against damage **by amount + a ≤0.7 s window** and
reported nova #5 (fire 19.25 s) as having **no matching damage record**. There is one:
`attack_id = boss&…:nova:2`, t=**19.70**, delivered 68.11, element cold — 0.45 s after the fire,
inside the window. The amount criterion rejected it because the telegraph's `damage_amount` is
**pre-mitigation** and `delivered` is post.

So F-HB-4's "no attack→damage join key exists" is **too strong**: a join key exists on 4 of 57
records and joins 4 of 9 telegraphs exactly (`blizzard:1`, `blizzard:2`, `nova:2`, `wave:2`).
What is true is that it is **absent on 53 of 57**, so the join is available for a minority and
"did that nova hit" remains unanswerable *in general*. The corrected statement is the useful one.
→ **routed to knight-rider** as a correction to F-HB-4, not a reversal.

### 4.3 The third ask, answered honestly

Charter T-2's third rider is *"`attack_id`-keyed attack anims"*. `attack_id` is consumed for beat
classification and for the telegraph→family→glow/SFX chain. It is **NOT** consumed to select
between per-attack animations, **because there are none to select between**: BODY-PROBE swept
24,576 FBX and found attack-worded clip names **zero**, and one authored melee take yielding three
combo slices from one arc. Keying three round-robin slices off an `attack_id` that is null on 53
of 57 events would be a mapping wearing a rider's clothes. **An absent referent, named.**

### 4.4 The family → element step is OURS, and the frame says so

The trace publishes `family` on a telegraph and publishes **no element on it** (`element` is null
on every header skill row). So `blizzard/nova/wave → cold` is a **presentation mapping authored in
the renderer**, printed verbatim in the HUD footer via `restage_identity_line()` alongside the
charge-glow disclosure. A rider we have is named as had; a mapping we invented is named as ours.

---

## §5 — ⚑ MY G-7 GATE ANSWERED "YES" FOR A REASON THAT APPLIES TO EVERY BODY IN EVERY FRAME

Run 1 printed:

```
[restage/G-7] ⚑ INTERPENETRATION FOUND: max 0.1849 m against 'SM_Prop_Torch_08',
              on 84 of 298 sampled frames.
```

which is a clean, specific, actionable-looking result. The offender census says otherwise:

| offender | frames |
|---|---:|
| **`SM_Bld_Base_Floor_Quarter_01`** — **the floor slab** | **81** |
| `FaceEast` | 2 |
| `SM_Prop_Torch_08` (the one the headline named) | **1** |

A body's lowest vertices sitting 2–18 cm inside a floor **with thickness** is what standing on a
floor *is*. And the tail of the log is worse: the last rows are at t = 36.00 s, where the boss is
**dead** and the "0.1006 m overlap" is the **−0.28 m death sink this cell authored three hundred
lines up**, intersecting the floor **on purpose**, being reported back to me as a collision.

**Three fixes, all pre-verdict:** floors classified out by name **and** by geometry (flat in Y,
large in XZ — so the next kit's floor is caught too); dead frames skipped; the body modelled as a
cylinder at its trace radius rather than as the AABB of a splayed golem, whose box reaches a metre
past its own shoulders in a windup.

Run 2, on the same path: **0.0000 m, 3,087 floor meshes classified out, 268 alive frames.**

This is the same failure class BODY-PROBE caught three times and the run has now caught four: a
measurement that fails like a success. The number was real; the object it was measuring was not
the one the gate was written to ask about.

---

## §6 — SFX (R-BR-16): the cleared set, and two corrections to the conductor's table

### 6.1 Vendoring — 50 files, licence-tracked, gitignored

`bash scripts/rs_sfx/rebuild_sfx.sh` rebuilds `assets/sfx/` from Matt's library in one command.
`scripts/rs_sfx/sfx_manifest.tsv` is the **tracked authority**: dest name, licence tag and source
path per file. The audio is **not committed** — two of the four cleared licences forbid or
restrict redistribution — exactly the ARSENAL-HARVEST / Synty rule, and `/assets/sfx/` is now in
`.gitignore` with that reason written into it.

| licence | files | redistribution |
|---|---:|---|
| `leohpaz` (Minifantasy / RPG Essentials) | 35 | **NO** |
| `CC0-oga` (OpenGameArt RPG Sound Pack) | 11 | OK |
| `tommusic` (Free Fantasy SFX) | 4 | restricted |
| **total** | **50** (31 MB) | |

**The twelve unattributed dirs are not consumed** and cannot be: the rebuild script reads the
manifest and nothing else. `--check` verifies every source and destination without copying, and
the render harness runs it.

**Music is OFF** and is one flag away (`--music 1`); the file is vendored so the alternate arm
costs a re-render rather than a re-vendor.

### 6.2 ⚑ THE 2.32 s WIND-UP IS NOT THIS TRACE'S WIND-UP

The conductor's beat table and G-6 row 6 both name **"real nova … 2.32 s wind-up"**. Measured on
the acceptance trace, 9 of 9 telegraphs:

| family | `wind_up_s` | `fire_t_s − t_s` |
|---|---:|---:|
| blizzard ×3 | **0.8333** | 0.8333 |
| **nova ×3** | **0.8500** | 0.8500 |
| wave ×3 | **0.8519** | 0.8519 |

2.318840579710145 s is a **BATON-CENSUS reading of an earlier battery** (the Mechanism-D arm) and
it is **2.7× this trace's actual tell**. The renderer was never wrong — it reads the field — but
**a charge sample truncated to 2.32 s would have outrun every tell in this watch by ~1.47 s**,
which is precisely the lie R-BR-16 forbade, arriving through a constant rather than through an
asset. The mixer reads `wind_up_s` out of the render's own beat row.

### 6.3 ⚑ ONE ROW OF THE TABLE IS SUBSTITUTED, AND HERE IS THE MEASUREMENT

The table names `45_Charge_05` (5.33 s) as the wind-up bed, to be "truncated + faded". Measured
(50 ms RMS envelope, `tmp/restage/measure/`):

- the file's 5.333 s is **55 % trailing digital silence**; audible body ≈ 2.4 s
- its **peak is at t = 0.150 s** and it decays monotonically to nothing

So its energy is **front-loaded**. A tell must *build* toward its fire; a front-loaded decay
played across a wind-up announces the fire at the wrong end of the window. **Substituted:**
`45_Charge_05`'s first 0.30 s becomes the **announce transient** on the decal's own frame (which
is exactly what a 0.15 s onset is for), and the sustained bed is `19_orc_charging_loop` — a real
loop — truncated to the measured `wind_up_s` with a 0.45 → 1.0 rising gain ramp and a 0.10 s
fade-out. Both files are in the cleared set. **A replaced row is named, per the table's own rule.**

*A hazard the conductor predicted and refuted survives intact:* leohpaz's 0.667 s quantisation has
**no leading pad**, so no offset compensation is needed. Confirmed by use.

### 6.4 The variation hazard, sized and solved

57 damage events. The connect class has 7 real cleared variants and survives; **the claw class has
2**. Every instance gets **±2 semitone pitch** (resample — duration moves with it, as a real
pitched sample does), **±1.5 dB gain**, and **round-robin without immediate repeat**. All three are
driven by a PRNG seeded on the beat index, so two runs of the mixer over one ledger produce a
bit-identical WAV — the staticity bar this run has held since BEAM-FIX now covers the audio.

### 6.5 ⚑ THE AUDIO IS PLACED BY FRAME, NOT BY TIME

This is a captured-frame render; Godot's audio clock is the wall clock and a windowed Metal
capture does not run at 30 fps wall. So the render emits two ledgers and
`scripts/rs_sfx/mix_sfx.py` transcribes them:

- `beats_*.json` — one row per beat, stamped with the **captured frame index it was drawn on**
- `framemap_*.json` — one row per captured frame: the **trace time** it carries, and whether
  hit-stop was holding the cursor

Wall time is `frame / 30` **by construction**, so hit-stop, the establishing hold and the outro
hold are absorbed exactly and **a sound cannot land on a different frame from its own picture**.
Nothing here schedules against a clock; it transcribes one.

**Beat reconciliation against the trace — exact:**

| beat kind | rows | trace fact |
|---|---:|---|
| `connect` | **50** | player-sourced `damage` events: **50** |
| `hurt` | **7** | `damage` events targeting the player: **7** |
| `telegraph` | **9** | `telegraph` events: **9** |
| `resolve` | **9** | one per telegraph `fire_t_s` |
| `mob_death` | **3** | `death` events: **3** |
| `boss_ultimate` | **1** | `damage` carrying `:nova:`: **1** |
| **total damage covered** | **57** | `damage` events: **57** |

### 6.6 And the alignment is MEASURED on the shipped clip, not asserted

The claim "a sound cannot land on a different frame from its picture" is a property of the design,
so it deserves a check that could fail. The **shipped `LAP2C_WATCH.mp4`** was decoded, its audio
track reduced to a 25 ms RMS envelope, and every beat's own frame tested for a transient:

| | |
|---|---:|
| beats checked (`connect` / `hurt` / `resolve` / `mob_death` / `boss_ultimate`) | **70** |
| beats with a transient > 2.5× the ambience floor in [−150 ms, +250 ms] | **70 (100.0 %)** |
| peak offset from the beat's own frame — median | **+0.050 s** |
| … mean / p90 | +0.061 s / +0.150 s |
| ambience floor RMS / clip peak RMS | 0.00344 / 0.32402 |

The +50 ms median is the samples' own attack envelope (a sword-hit's RMS peak sits one to two
frames after its onset), not a scheduling error: the *onset* is on the frame, by construction.

---

## §7 — JUICE (R-BR-19 / R-BR-20)

### 7.1 ⚑ MY OWN DRIFT NUMBER WAS WRONG BY 15 POINTS, IN THE UNSAFE DIRECTION

Run 1 printed `DRIFT 6.133 s = 17.04 %`, which would have reported R-BR-19's ~3.7 % budget as
blown by 4.6×. It was measuring wall-minus-trace over the **whole clip**, which includes the two
**deliberate cinematic holds** — the establishing hold at tick 0 and the outro hold on the end
card. Those are not drift: they are frames in which the clock is held on purpose and nothing is
claimed about the fight's length.

**Decomposed, from the render's own frame map:**

```
captured 42.133 s wall  =  36.000 s trace
                        +   5.800 s deliberate holds (in 24 + out 150 frames)
                        +   0.400 s hit-stop
                            [residual −0.067 s]
```

| | |
|---|---:|
| hit-stop firings | **4** — mob_death ×3, boss_ultimate ×1 |
| held frames | **12** (3 per firing at 30 fps) |
| **hit-stop over the fight span** | **0.400 s / 36.000 s = 1.11 %** |
| R-BR-19's budget | ~3.7 % |

The frame map shows the three visible freezes cleanly at **f617 (t=19.700, the boss ultimate
connect)**, **f698 (t=22.300, the elite's death)** and **f1113 (t=36.000, the boss's death)**, each
holding trace time flat across exactly 3 frames. The fourth firing is the shaman's death at
**t = 0.00 s** — the werewolf opens with `rip_and_tear` on tick 0 — and it lands *inside* the
establishing hold, where the clock is already held.

**`player_death`: ZERO firings — ABSENT FROM THIS TRACE, named.** The footer records
`winner: player`, 0 player deaths. That is a PASS by G-6's own absence rule, not a dark path.

### 7.2 The no-displacement gate, checked rather than asserted

R-BR-19 forbids knockback and impact displacement outright. "We did not add any" is the kind of
claim that stays true until a later cell adds one, so every body's world position is **read back
after every write** and compared against `sim_to_world` of that tick's own interpolated `x_m/y_m`:

| | |
|---|---:|
| body writes checked | **3,441** |
| violations | **0** |

Every body sat exactly where the trace put it, on every frame.

### 7.3 The rest, with values

| element | shipped | why this number |
|---|---|---|
| victim flash | **additive emissive**, +1.35 energy, 0.08 s ease-out, **0-frame latency** | R-BR-19 forbids albedo replacement, and the reason is a property of *this* cast: SHADOW-UNIFY built the boss's identity out of a cold emissive, and MOB-CAST measured seven of eight mob bodies carrying the cold family in a uniform self-glow. Replacement would strip exactly that, on every hit, 57 times |
| numeral pop | **1.15× over 60 ms** (was 1.40× over 150 ms) | coupled to grade C on purpose: 0.70 × 1.40 = **0.98**, i.e. peak size essentially unchanged, which would have made grade C a lie. 0.70 × 1.15 = 0.805. The pop is a punch, not a size refund |
| death resolution | authored `knockback` lead-in → 1.2 s procedural collapse + **emissive fade to zero** + **0.28 m sink** | a body that keeps glowing after death reads as paused. The SFX bed gives death 2.0–2.67 s of tail for the fade to sit under. The clip is non-RM and moves nothing |
| camera, JUICE arm | rotational only, **≤0.4°, 120 ms decay**, same three beat classes | re-derived every frame from the locked basis, never accumulated onto the camera's own transform — a rounding residue would walk the framing over 1,264 frames |
| camera, CAM-LOCK arm | **untouched, 0 impulses applied** | the measurement surface every parity claim in this run stands on |

---

## §8 — ⚑ THE PLAYER AURA WAS WRONG TWICE, AND NEITHER WAS A TASTE CALL

R-BR-17 gap 2: stage `BinbunVFX/magic_areas/` — deliberately unstaged by VFX-BAKEOFF — and bind it
persistently to the player.

**What moved, said plainly:** nothing on disk. `Assets/BinbunVFX/magic_areas/` was already present;
`king_rig.gd::AURA_VFX` has been pointing at it by absolute path and no render had ever loaded it.
This is the first render that binds it. It loads, with the pack's own UID warnings (§10, F-RS-2).

**Attempt 1 — the catalogue correction, applied and wrong.** 1.7 × 1.29 = 2.19. Measured, the
scene's authored ground extent is **4.000 m radius**, so ×2.19 made an **8.76 m radius — 17.5 m
across, wider than the 12 m nova**. It swallowed the player, washed the frame warm, and read as a
*ground area marker* — a legibility collision with the one overlay in this render that has to be
unambiguous. The 1.7× is a correction for **impact bursts judged against a whole frame at a 34.8 m
stand-off**; this is a **persistent effect anchored on a body**, and the right size for it is set
by the body. **Refused, and replaced by a derived scale:** measure the scene's own extent, scale
so the rim sits at `entity_radius_m × parity × 1.35` = 0.871 m → **×0.218**.

**Attempt 2 — right size, wrong scene character.** At body scale the scene's *filled* core sat
directly under the werewolf and blew out his legs and feet. **No scale fixes it** — bigger swallows
the stage, smaller is a hot dot. `magic_areas/` ships exactly one scene, so there is no sibling to
switch to. **Fixed inside the scene, at instantiation, and named as ours:** `GroundGlow`,
`Flare_01` and `Flare_02` (the filled disc and the core flares) are suppressed; `Streaks` and
`UpwardGlow_01/02` (the rim and the updraft) ship. `--aurafull 1` restores the authored scene
exactly; nothing on disk was modified.

The scene's own `OmniLight3D` is capped to energy 0.55 / range 1.6 m. Uncapped it would have
warmed the whole floor and **quietly re-graded WARMTH's measured +9.110 / 71.4 % warm split** — a
parameter this cell is forbidden to move, moved sideways by a VFX scene.

### 8.1 ⚑ I SUSPECTED THE AURA FOR THE RESIDUAL WARM CORE. THE PEEL SAYS IT IS THE LAMP.

After both fixes a warm core remained at the player's feet, and my working hypothesis was the
aura's surviving updraft. **Two possible authors, and an eye cannot separate them — one flag can.**
`AURA_PEEL` is `--aura 0` against an otherwise byte-identical arm, so **the aura is the only
variable** and any pixel difference between them IS the aura.

Measured over 30 frames in a 260×260 px box around the CAM-LOCK player anchor
(`PL_ANCHOR_FX = 0.5010`, `PL_ANCHOR_FY = 0.5509` — the player is pinned there by construction):

| | |
|---|---:|
| mean \|diff\| inside the player box | **1.784** / 255 |
| mean \|diff\| over the whole frame | 0.1741 / 255 |
| max \|diff\| inside the box | 164.0 / 255 |
| pixels changed by > 8/255 | **1,133 of 67,600 = 1.68 %** |
| box mean luma, aura ON / OFF | 142.34 / 141.89 |
| **the aura's own contribution to the box** | **+0.45 / 255 = +0.3 %** |

**The aura is a thin rim, not a wash** — a 164/255 local delta on 1.68 % of the box, and +0.3 % of
its mean luma. **So the residual warm core is NOT the aura.** It is WARMTH's carried lamp (energy
5.20, colour 1.00/0.66/0.34, offset 0.72 m camera-side) falling on the wet-floor film — an
inherited R-BR-11 state this cell is forbidden to move, and which VERDICTED at Matt's eye
(*"the water sploches look AMAZING"*, Scope 32).

The hypothesis was mine, the instrument was built to test it, and it refuted it. **The attribution
is taken, not deferred.**

---

## §9 — VFX: the three-layer law, and G-VFX

### 9.1 What fired

| layer | owns | scale | count |
|---|---|---|---:|
| **CORE — Polygon Arsenal** | the silhouette of every strike beat | **1.0** (pack authored at ARPG combat scale) | **114** |
| **SHELL — Binbun** | wash / bloom / scorch / motes, stacked **UNDER** the core, never replacing | **1.7** catalogue correction | **114** |
| **NATIVE — Godot** | bone-attached charge glow (4 bodies), persistent player aura (1) | — | 5 |
| **R-BR-18 mob-skill pairs** | muzzle at caster + impact at target, **same frame** | — | **13** |

The discriminator is applied **by family and declared**: SHELL draws from `smoke_effects` /
`fire_effects` / `poison_cloud` / `ice_cloud` (no readable edge); the SHAPED families
(`muzzle_flash`, `impact_explosions`) are sent to the mob-skill pair, which is a beat Arsenal does
not cover. **A Binbun scene with a readable shape never goes under an Arsenal beat.**

13 mob-skill pairs = 9 telegraph resolves + 4 non-point mob-sourced damage events. **Zero travel**:
R-BR-3 forbids invented travel and the schema has none — one telegraph record, one damage record,
no spawn/flight/impact triple. It reads as a bolt and it lies about nothing.

### 9.2 Charge glows — the authorship split, held

| | keyed to |
|---|---|
| **boss / mob** | the **real** `wind_up_s` in the telegraph record — 0.8333 / 0.8500 / 0.8519 s, 9/9 populated. Sim truth |
| **player** | a **0.18 s presentation-layer pre-roll**, labelled as presentation timing **on the frame** |

`commit_skill_idx` is **−1 on 361 of 361 player ticks** (F-HB-3, re-verified this cell). There is
no player cast window in this trace and **none is invented**. What is invented is 0.18 s of lead
before a strike the trace *does* record, and the HUD footer says so in those words.

Bone attachment measured, not assumed: `RightHand` found on all four bodies (player idx 26, cast
idx 21). A body with no hand bone would have logged a warning and gone unglowed.

### 9.3 G-VFX — the soup gate

Pre-registered before any frame was read: at each beat's peak frame, count **connected components**
of the lit region in the F_law arm against an **Arsenal-alone control** rendered from the same
trace, same camera, same frames — arm the only variable. Peak |diff| may rise (that is drama);
**component count must not collapse** (that is the shell eating the core). Bar: F_law components
≥ **70 %** of the control's, threshold at the control's own 99th-percentile luma, components under
12 px discarded as noise.

⚑ **The arms differ in EXACTLY the shell and nothing else**, and the render's own layer report
proves it rather than the harness asserting it: control `{arm: D_arsenal, core: 44, shell: 0,
mobskill: 6}` vs law `{arm: F_law, core: 44, shell: 44, mobskill: 6}`. **Same core count, same
mob-skill count, 44 shell spawns is the whole variable.**

**RESULT — G-VFX PASSES: 17 beats measured, 0 FAIL.**

| | core (Arsenal alone) | law (CORE + SHELL) |
|---|---:|---:|
| components, median | **32** | **32** |
| components, mean | 33.5 | 33.4 |
| law ≥ core on | — | **12 of 17 beats** |
| law/core component ratio, median | — | **1.000** (worst beat 0.700, exactly on the bar) |
| mean \|diff\| | — | median **0.365**, range 0.073–1.306 |

**The shell did not eat the core.** Component counts hold at parity and rise above the control on
five beats (f131 43 vs 42, f218 46 vs 43, f324 49 vs 47, f342 58 vs 53, f274 39 vs 37) — the shell
is adding readable regions, not merging them.

### 9.3a ⚑ A SECOND STATISTIC THE GATE DID NOT REGISTER, AND IT POINTS THE OTHER WAY

Lit-pixel count, which the gate does **not** grade on:

| | |
|---|---:|
| law lit-px **LOWER** than the control on | **15 of 17 beats** |
| law/core lit-px ratio, median | **0.944** |

R-BR-17 describes the shell as *"bloom wash, ground scorch, motes"* — i.e. **additive**. Measured,
it is not: the Binbun smoke class is an alpha-blended grey puff, and stacked at the core's own
world point it **occludes** core light rather than adding to it, pushing ~6 % of the core's lit
pixels below threshold. The layer is doing its job — component count held, and |diff| confirms it
is visibly present — but it is contributing **weight by occlusion**, not **bloom by addition**, and
those are different things to hand Matt. The gate's registered criterion is met; the mechanism is
not the one the ruling described. **Stated, not smoothed over.**

The instrument is `scripts/rs_sfx/gvfx.py`; the ledger is `tmp/restage/measure/gvfx.json`; both
arms are in `tmp/restage/clips/`.

### 9.4 ⚑ F-AH-2 — the trail class is EXERCISED, and STILL NOT MEASURED

ARSENAL-HARVEST's debt: `SwordTrail` / `SwordTrailShadow` / `SwordChargeUp` passed the pixel gate
on 7–232 lit pixels because a static isolation stage gives a ribbon nothing to streak along.
`trail_attach` now parents `SwordTrail` to the striking rig on every connect, so this watch
**exercises** them on a swinging bone for the first time — 50 attachments.

**Exercising is not measuring, and this cell did not measure them.** A moving-host measurement
needs the trail isolated against its own null arm (attach vs no-attach, same frames, component or
lit-pixel delta in a box around the hand), and that is a fifth render this cell did not run.
**F-AH-2 stands, downgraded from "unproven and unexercised" to "unproven and exercised".** Named,
not paid.

---

## §10 — Findings routed

| id | finding | route |
|---|---|---|
| **F-RS-1** | **F-BR-2's forward clause is stale.** `family` is populated **9/9** on the `wr3_acc` acceptance trace; the seam that dropped it is fixed. G-5's rider-census amendment can be un-amended | conductor / knight-rider |
| **F-RS-2** | **The Binbun pack's `.tscn`/`.tres` reference `res://assets/BinbunVFX/…` (lowercase) while the tree is `Assets/BinbunVFX/…`.** Godot logs `Case mismatch … will not open when exported to other case-sensitive platforms` and falls back to text paths on every invalid UID. It works on macOS's case-insensitive filesystem and **would not survive an export to a case-sensitive target** | knight-rider → asset hygiene |
| **F-RS-3** | **F-HB-4 is too strong.** A telegraph→damage join key exists on **4 of 57** damage records and joins 4 of 9 telegraphs exactly. HUD-BUILD's amount+window heuristic mis-reported nova #5 as unmatched because `telegraph.damage_amount` is pre-mitigation and `delivered` is post | knight-rider → correction to F-HB-4 |
| **F-RS-4** | **The "2.40 m beam base" datum is stale by two cells.** BEAM-PIN2 retired the beam lift to −0.60 m under a Matt ruling; `kit_replica_level` states the room has **no ceiling mesh**. Any future collision argument that cites it is citing a constant that no longer describes the scene | conductor (BODY-PROBE §4 correction) |
| **F-RS-5** | **Scope 39's slits still want a cause.** R-BR-22 offered the broken beam; G-7 says there is nothing to break. The ceiling-crack slits currently have no visible cause in the frame | conductor |
| **F-RS-6** | `--slitgradfloor` is plumbed but **prints nothing**, so "grade A3 was applied" is verifiable for the energy (`shaft gain 0.0400` in the log) and only by code path for the floor. A flag that does not announce itself is one re-render away from being silently absent | mine, queue |
| **F-RS-7** | This machine has **four `python3` interpreters on PATH and only some carry numpy**; every harness in this repo prepends `/opt/homebrew/bin` for ffmpeg, which selects a numpy-less one. `mix_sfx.py` / `gvfx.py` re-exec into a capable interpreter and say which | standing guard row |
| **F-AH-2** | carried, downgraded: trail class **exercised** on a swinging bone, **still not measured** | mine, unpaid |

---

## §11 — Gates

| gate | result |
|---|---|
| **Single-writer** | opened `136ff81`, head unmoved through the cell, no foreign commits |
| **F-AH-3** (`--import` strips `[rendering]`) | **NOT FIRED — and that is a measured fact, not luck.** No asset was imported: `bp_apply_retarget.py` reported `ALREADY_RETARGETED` on all 5 targets and cleared no cache, so no reimport was triggered. `project.godot` sha256 `6bef17eb…ace8a` **identical before and after**; snapshot at `tmp/restage/guard/` |
| **F-AH-6** (ffmpeg exits 0 on corrupt H.264) | every clip encoded `-preset veryfast -crf 20 -r 30`, no `select`/`setpts`, and **full-decoded with `-xerror`** before being listed. Frame-count in = frame-count out on every one |
| **GDScript parse** | `--check-only` clean on all three edited files, run before every render |
| **Trace custody** | READ-ONLY. Nothing regenerated, no engine path touched |
| **Inherited stage state** | `kit_replica_level.gd`, `wr1_level.gd`, `sky_shaft.gdshader`, `sky_dust.gdshader`, `wet_floor.gdshader` are **byte-identical to `4f1a3ca`** (BEAM-SLITS head) — `git diff` returns empty. Beams A3, dust FULL, WARMTH, wet film, pools, CAM-LOCK all inherited untouched |
| **Files this cell changed** | exactly four: `scripts/wr2_playback.gd`, `scripts/wr2_actor_rig.gd`, `scripts/vfxbo_arms.gd`, `.gitignore` (+ new `scripts/rs_sfx/`) |
| **F-BR-4** (SIMPLE-asset gate) | RED at 900, **unchanged** — this cell added zero violations by the gate's own reckoning |
| **F-BR-5** | stands. This cell consumes `polygon-simple-fantasy` **animation only**, through a baked `.res` of rotation curves; no SIMPLE mesh, material, texture or rig is instantiated. Matt's ruling on the principle is still owed |
| **Frames pruned after encode** | yes, file-level `rm -f` between arms |

---

## §12 — GATE G-6, the 20 pre-registered rows

**Absence is a PASS if it is named. A row silently missing is a FAIL.**

| # | element | verdict | evidence |
|---|---|---|---|
| 1 | Cone-beam slits at **A3** + cold pools | **PASS** | `git diff 4f1a3ca -- kit_replica_level.gd …` **empty**; A3 passed as the R-BR-15 peel pair (`--shaftE 0.040 --slitgradfloor 0.28`); log: `shaft gain 0.0400 vs BEAM-PIN2's 0.1750 = 0.23x`; slit geometry 3.62–4.74 m, mean 4.03 m, n=5, aperture 8.950 m — BEAM-SLITS' numbers to two decimals. ⚑ The watch reads **warmer** than the BEAM-SLITS legacy stills, and that is the ruled consequence, not a drift: A3 halves the cold shaft against an unchanged warm torch bed, and BEAM-SLITS §5 measured exactly this at **76.7 % warm** against R-BR-12's ~80 % threshold — which did not trigger, so FULL dust stands |
| 2 | Unified shadow grammar at `UNIFIED_KEY_ENERGY` **3.50** | **PASS** | log: `⚑ --keyE 3.500: UNIFIED_KEY_ENERGY OVERRIDDEN (shipped default 1.00)`; `SHADOW-UNIFY: ONE shadow author … torches, sky lamps and the carried light NON-CASTING`; `0/12 sconces cast` |
| 3 | Wet floor film + sconce rake + graded lamp bump | **PASS** | log: `★ WARMTH ARM: dust_warm 1.00 · fog_warm 1.00 · wet 1.00 (rough 0.240, patch 3.40 m, thr 0.545, darken 0.16) · carried omni E=5.20 (shipped)` |
| 4 | Player body with warm carried light, at the verdicted parity grade | **PASS** | target 2.322 m = 1.80 × 1.29; rendered mean 2.330 m (**+0.36 %**), measured not eyeballed; `E1 ARM A: carried player light — energy 5.20 range 9.0 m colour (1.00,0.66,0.34)`, lamp offset scaled with the body |
| 5 | Boss with cold emissive + **icearmor rider readable** | **PASS** | `wr3_icearmor` present on the boss **120 of 361 ticks**; the ward annulus at 2.05× body radius renders (visible in `plates/a3_full.png`); Lap-2 diff vs Lap 1 = the rider is now *read from `ailments[]`* rather than absent |
| 6 | Telegraph decals rendering the **real** nova | **PASS, with a correction** | shape `circle` and radius **12.00 m** read from the record; wind-up read from the record at **0.8500 s** — ⚑ the row's own "2.32 s" is a stale figure from an earlier battery (§6.2). Log: `nova telegraph: … wind_up_s=0.850000000 fire_t_s=31.0500 radius_m=12.00 … [family=nova via family]` |
| 7 | Damage numerals at grade **C** with crit RED and the pop | **PASS** | `--numgrade C` (0.70×); pop re-cut to **1.15× / 60 ms** per R-BR-19 and coupled to the grade (§7.3); on-frame beats reconcile to the trace at **57/57** (§6.5); crit red untouched, 2 crits on this fight |
| 8 | Element-mapped VFX — 6/6 families exercised **or the absent named** | **PASS (absence named)** | this seed rolls `{chaos 50, cold 4, physical 3}` only. **fire / lightning / water / wind / earth: ABSENT — this seed never rolls them.** All three present elements resolve to a CORE and a SHELL scene by name |
| 9 | Arsenal CORE on every claw/strike beat | **PASS** | **114 core spawns**; 50 connect beats each firing a slash (alternating `SlashWide`/`SlashSpinThick` off the event key) plus impacts and the ultimate |
| 10 | Binbun SHELL under core beats — **component count did not collapse** | **PASS** | **17 beats, 0 FAIL.** Components median 32 vs 32; law ≥ control on 12 of 17; ratio median 1.000, worst 0.700 (exactly on the pre-registered bar). Arms differ in the shell ALONE — control `{core 44, shell 0}` vs law `{core 44, shell 44}`. ⚑ §9.3a: a statistic the gate did NOT register shows lit pixels *falling* 6 % — the shell works by occlusion, not addition |
| 11 | Player aura present and persistent | **PASS** | `magic_areas` bound, persistent on the player body, scale derived from the scene's own 4.000 m authored extent to a 0.871 m rim (§8) |
| 12 | Charge glows — boss/mob off real wind-up; player pre-roll **labelled as presentation** | **PASS** | 4 bodies bone-attached at `RightHand`; boss window = the record's `wind_up_s`; player = 0.18 s pre-roll, **labelled on the frame** in `restage_identity_line()` — a frame check, not a code claim |
| 13 | Mob skill VFX as instant-resolve pairs, **zero travel** | **PASS** | **13 pairs**, muzzle at caster + impact at target on the same frame, nothing between. ⚑ The one true *caster* mob (`slitha_shaman_c01`, range 18 m) **died at t = 0.00 s and cast nothing** — named absence |
| 14 | SFX from the cleared set only, with pitch/gain variation on repeats | **PASS** | 50 files, 3 cleared sources, manifest + licence column tracked, audio gitignored; ±2 st / ±1.5 dB / round-robin without immediate repeat, deterministic (§6.4) |
| 15 | Ambience bed under the whole watch | **PASS** | `tommusic/Cave.ogg` 60.0 s loop, tiled across the full clip duration at −22 dB |
| 16 | JUICE — hit-stop on exactly 3 beat classes, victim flash, **no knockback** | **PASS** | classes registered as constants and a fourth is a `push_error`; **4 firings across 2 classes**, third named absent; drift **1.11 %** decomposed (§7.1); **3,441 position writes, 0 displacement violations** |
| 17 | HUD on, four surfaces, non-fields labelled on frame | **PASS** | HUD-BUILD inheritance at grade C; footer carries the four DERIVED disclosures **plus** this cell's five presentation disclosures via `restage_identity_line()` |
| 18 | Death resolution on `alive→false` for every death | **PASS** | 3 deaths in the trace, 3 `mob_death` beats, 3 lead-in + collapse + emissive-fade + sink resolutions |
| 19 | End card | **PASS** | `--holdout 150` = 5.0 s on the card; 152 frames measured at `t_max` in the frame map |
| 20 | Both camera arms rendered | **PASS** | `LAP2C_WATCH.mp4` (CAM-LOCK, **0 impulses applied**) and `LAP2C_WATCH_JUICE.mp4` (≤0.4° rotational, 120 ms decay, position never written) |

**G-6: 20 rows. 0 silently missing.**

---

## §13 — Deliverables

All under `/Users/admin/Games/reincarnated-godot/tmp/restage/clips/`. **Every one decode-verified
with `-xerror`, frames-in = frames-out on all five.**

| clip | dims / frames / dur | audio | sha256 (16) | what it asks |
|---|---|---|---|---|
| **`LAP2C_WATCH.mp4`** ← **WATCH FIRST** | 1600×900 / **1264** / 42.13 s | **AAC 44.1 k st** | `e5f2c2eb4a92808a` | **charter T-2.** The whole fight in the crypt corner at CAM-LOCK: werewolf on the authored melee set at ×1.29, Arsenal core + Binbun shell + native glow and aura, 50 cleared SFX on the render's own beat ledger, hit-stop, HUD grade C, end card |
| `LAP2C_WATCH_JUICE.mp4` | 1600×900 / 1264 / 42.13 s | AAC | `fb08ef550e368ae4` | R-BR-20's second arm — **4 rotational impulses applied, position never written.** Matt judges the taste; the run keeps its instrument |
| `GVFX_CORE_ONLY.mp4` | 1600×900 / 360 / 12.00 s | — | `10adb4c43b1f7f44` | the G-VFX control: Arsenal alone, `shell 0`, NOHUD |
| `GVFX_LAW.mp4` | 1600×900 / 360 / 12.00 s | — | `c2fb27db0c12adb4` | the same trace, same camera, same frames, **shell the only variable** |
| `AURA_PEEL.mp4` | 1600×900 / 90 / 3.00 s | — | `e83140ee4fbc0ea1` | the aura attribution control (`--aura 0`) — §8.1's measurement runs on this pair |

**Plates** in `tmp/restage/plates/`: `R2_0060/0300/0600/0700/0900/1100.png` (the watch across the
fight) · `endcard.png` · `a3_full.png` (the ward annulus on the boss, G-6 row 5) ·
`crop_player.png` (attempt 2's filled-disc aura, kept as the evidence for §8) ·
`GL2_/GC2_0100/0230/0330.png` (the G-VFX pair) · `AP2_0060.png`.

**Instruments (committed):** `scripts/rs_sfx/sfx_manifest.tsv` · `rebuild_sfx.sh` · `mix_sfx.py` ·
`gvfx.py` · `tmp/restage/run_r.sh` · `run_all.sh` · `mkclip.sh`.
**Ledgers (committed):** `tmp/restage/measure/beats_*.json` · `framemap_*.json` · `g7_path.json` ·
`ratio.json` · `aura_attrib.json` · `gvfx.json` · `mix_*.json` · `tmp/restage/logs/` ·
`tmp/restage/guard/`.

⚑ **THE TWO WATCH CLIPS ARE NOT COMMITTED, AND THE REASON IS THE LICENCE.** A WAV mixed from
leohpaz + tommusic samples, and an MP4 with that WAV muxed into its AAC track, **are** the
restricted audio in another container — the same rule `assets/sfx/` lives under. So
`LAP2C_WATCH.mp4` and `LAP2C_WATCH_JUICE.mp4` stay LOCAL (path in §13, on this Mac) while the
**silent** evidence clips — the G-VFX pair and the aura peel — commit normally. The difference is
the audio track, not the pixels, and it is written into `.gitignore` in those words.
`bash tmp/restage/run_all.sh` rebuilds both from the committed instruments in one command.

---

## §14 — What this cell did NOT do

- **No `RIG_BOSS_H` edit** (R-BR-23 reconciled; the lever is the wrong one).
- **No disrepair edit** to the room (G-7 = 0.0000 m; there is nothing to fix, and no beam to break).
- **No beam, pool, dust, sheen or WARMTH parameter written.** Grade A3 arrives as a peel pair.
- **No aesthetic verdict** on the body, the VFX register, the numeral grade or the juice.
- **F-AH-2 not paid** — the trail class is exercised on a swinging bone, not measured there.
- **`guard` / `guard_hit` bound but never driven** — this trace emits no block/parry beat.
- **The five absent element families not exercised** — this seed rolls `{chaos, cold, physical}`.

---

## §15 — Debts, named

- **`reincarnated-godot/AGENT_STATE.md` is now eleven cells behind** (CAM-LOCK, MOB-CAST,
  BEAM-PIN2, VFX-BAKEOFF, BEAM-V3, ARSENAL-HARVEST, WARMTH, HUD-BUILD, BEAM-SLITS, BODY-PROBE,
  LAP-2C RESTAGE). Named at ARSENAL-HARVEST, named again here, still not paid.
- **`tmp/vfxbakeoff/` ~8 GB** still awaits Matt's hand — carried forward unchanged.
- **F-AH-2** — trail class exercised on a swinging bone, not measured there. Mine, unpaid.
- **F-RS-6** — `--slitgradfloor` prints nothing. Mine, queue.
- `tmp/restage/` is **567 MB** (5 clips + logs + ledgers + 13 plates), 0 PNG frames — pruned
  file-level between arms, per the prune policy.

## §16 — Commits

| repo | hash | what |
|---|---|---|
| godot | **`69264c5`** | opened at `136ff81`, no foreign commits on the head. Four source files (`wr2_playback.gd`, `wr2_actor_rig.gd`, `vfxbo_arms.gd`, `.gitignore`) + `scripts/rs_sfx/` + `tmp/restage/`. **Pushed** (standing Matt authorisation) |
| meta | this note | |

⚑ **The `tmp/l7race/` deletions sitting in the godot working tree at open were left exactly as
found.** They are Matt's PRUNE, pending from before this cell, and folding another party's
uncommitted work into this commit would misattribute it.

---

*LAP-2C RESTAGE · drax · presentation seam · 2026-08-01*
*Single-writer held throughout; opened and closed with no foreign commits on the godot head.*
*No aesthetic self-verdict taken anywhere. R-BR-21's FAIL condition is live and is Matt's to fire.*
