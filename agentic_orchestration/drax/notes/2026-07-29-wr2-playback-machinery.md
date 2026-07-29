# WR2-PLAYBACK-MACHINERY — the Godot consumer for the WR1 banked baton

> **Cell:** parallel Godot cell of run **WR2-ENCGEO-2026-07-29** (charter §4, *"Parallel,
> non-blocking (Godot seam, drax)"*). **Agent:** drax. **Conductor:** gandalf.
> **Repo:** `reincarnated-godot` — commit **`4f69e93`**, **NOT PUSHED** (conductor coordinates).
> **Contract:** `agentic_orchestration/gandalf/notes/2026-07-29-wr1-baton.md` (BEFORE-evidence +
> machinery substrate per R-WR1-23).
> **Trace set:** `~/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr1_battery_2/`
> — **opened READ-ONLY, never written, nothing copied out.** `git status` on that path is clean
> at cell end (SS-1 held).

---

## §1 — THE DELIVERABLE

**MP4 (Matt's scheduled mid-run owner-eye):**

```
/Users/admin/Games/reincarnated-godot/tmp/wr2/wr2_smoke_pre_boss_A_74000802.mp4
```

1280×720 · 30 fps · **658 frames = 21.93 s**, against the trace footer's own
`elapsed_s: 22.0`. One banked boss fight, played at **1× real time**, start to finish, single
fixed camera. No cut, no speed-up, no edit.

**The fight, and why this one.** `pre` leg (`R2_proxy`, cold 0.14) · `boss` · arm **A** ·
seed **74000802** · `fight_key KC1-2026-07-27/boss/A/74000802`.

| property | value | why it earns the pick |
|---|---|---|
| nova crossings | **1** | 48/180 boss fights have **zero** — the brief said avoid those, and seed 74000800 (the obvious demo pick) is one of them |
| crossing payload | **414.80 = 2 × 207.40** | the **2× case**. 30 of 44 crossings per leg are 1×; picking a 1× would have exercised the decomposer without ever showing it decompose |
| duration | 22.0 s | short enough to watch whole; long enough to contain the drift |
| wall-share | **61.4 %** of ticks | first wall touch t = 8.5 s, then pinned |
| resolution | player dies at **exactly (0.5, 0.5)** | the SW corner, 179/180 fights' resolution point |
| separation at mid-fight | **1.706 m**, settling to **1.600 m** | the modal engagement separation, against 2.0 m of combined body |

So one 22-second clip carries the nova, the 2× decomposition, the straight-line drift, the corner
pin, the interpenetration, and a death. **Nothing in it was arranged. It is what seed 74000802 did.**

**Evidence stills** (all under `/Users/admin/Games/reincarnated-godot/tmp/wr2/frames/`):
`F0000.png` (spawn frame) · `z_tg.png` (the 12.0 m telegraph, east overrun visible) ·
`chk65z.png` (**both 207.40 floaters**) · `F0657.png` (the corner, at death) ·
`z_sw4.png` (SW-corner witness: the two footprint rings **crossing**).

---

## §2 — WHAT WAS BUILT

| file | state | what it is |
|---|---|---|
| `scripts/replica_trace.gd` | **modified** (additive) | the loader gains the **g5 battery layer** |
| `scripts/wr2_traceset.gd` | **new** | leg registry + **the nova decomposer** |
| `scripts/wr2_playback.gd` | **new** | the stage: datum seat, playback, FX, wall faces |
| `scenes/wr2_playback.tscn` | **new** | 4-line scene; the script builds everything |
| `scripts/run_wr2_playback.sh` | **new** | capture harness → PNG sequence → MP4 |

**Nothing was forked.** The two things that carry HISTORY are reused: the NDJSON parse
(`replica_trace.gd`, extended not copied) and the room placement maths
(`kit_replica_level.gd` via `wr1_level.gd`, including the wall origin-recentre fix). The new
code is new because its **contract** is new — ArenaDatum seat, per-leg decomposer,
`delivered`-not-`amount`, wall-face dressing, a roster with no rig bindings.
`replica_playback.gd` (the REPLICA-1/KT-4 stage) was **not touched**: its KT-3 arena and its
pct-gauge floater grammar do not apply to these traces.

### 2.1 The g5 layer was a silent parse error

The baton's §4.0 is not a footnote. `g5_header` had **no arm** in the loader's `match`, so every
one of the 450 files would have charged **one `parse_errors`** on an otherwise clean parse — a
counter nobody reads, hiding the fact that the battery contract was never being read at all.
Fixed; `parse_errors = 0` on the demo fight, verified in the load banner. **Both schema strings
are now quoted on the frame itself**, because quoting only one is how a consumer validates
against the wrong document.

### 2.2 The decomposer is the one number living outside the trace

`realized_count` appears in **0 of 450 traces**, confirmed at source by the baton. So the count is
a division, and the divisor is a **per-leg constant the trace does not carry**:

| leg | dir | regime | unit payload |
|---|---|---|---|
| `pre` | `g5_m4cadence_nova_mitR2proxy_tg` | R2_proxy (cold 0.14) | **207.40** |
| `pre_endpoint` | `g5_m4cadence_nova_mitR2proxyresistslow_tg` | R2_proxy_resists_low (cold 0.00) | **235.40** |
| `post` | `g5_r3arm_m4cadence_nova_mitR3_tg` | R3 | **207.40** |

`wr2_traceset.gd` is that dependency **made visible** rather than buried in a renderer.
An **unregistered leg returns NAN**, and the renderer then draws one floater of `delivered` and
**says it did not decompose** — it never guesses a constant. A future battery at a different
mitigation regime will carry a different one.

**Re-proved, not trusted.** Independently over all 450 files, using the baton's exact predicate
(`geometry == "circle"` ∧ `skill_idx == -1` ∧ `element == "cold"` ∧ target is player):

```
g5_m4cadence_nova_mitR2proxy_tg              {1.0: 30, 2.0: 14}
g5_m4cadence_nova_mitR2proxyresistslow_tg    {1.0: 30, 2.0: 14}
g5_r3arm_m4cadence_nova_mitR3_tg             {1.0: 30, 2.0: 14}
ALL LEGS                                     {1.0: 90, 2.0: 42}   = 132 crossings
```

Exactly the banked histogram, on all three legs. And the machinery's own headless probe
(`-- --probe`) reproduces it per fight:

| leg | seed | crossing | decomposed | violations |
|---|---|---|---|---|
| pre | 74000802 | 414.80 | **2 × 207.40** exact | 0 |
| pre_endpoint | 74000802 | 470.80 | **2 × 235.40** exact | 0 |
| post | 74000802 | 414.80 | **2 × 207.40** exact | 0 |
| pre | **74000800** | — | **0 crossings** | 0 |

The last row is the point: **absence is data.** The machinery reports zero and renders nothing,
which is correct — and it is the row that would have made a nova test pin to 74000800 pass
vacuously forever.

**`pre` and `pre_endpoint` are never pooled**, and there is deliberately **no selector that
offers both** — the omission is the enforcement.

### 2.3 R-WR1-21 — the wall-face dressing

The kit wall stands at ±18.75 m; the sim clamp line at ±18.00 m. The band is **filled, not
marked**: four slabs 0.750 m deep × one wall-course high, **outer face flush to the kit wall,
inner face exactly on the arena line**, plus four corner pilasters and a low emissive kerb along
each base. A player clamped to x = 0.5 m is then standing half a metre from a solid face.

Three alternatives rejected, each for a reason: a **painted floor line** still reads as floor you
may cross; **shrinking the room to 36.0 m** is illegal in this grammar (not a multiple of the
2.5 m bay) and would move every torch, tile and pillar the WR1-ROOMS cell verified pixel-identical;
**collision** is forbidden by R-WR1-20 — the face is an obstruction *to the eye*, and the trace
already contains the clamped positions.

**What I SAW** (`z_sw4.png`, the purpose-built SW-corner witness): two dark wall faces meeting at
a corner, the gold kerb running along the base of each, the boss standing in the corner — and
**the cyan player footprint ring crossing INSIDE the boss's red ring.** The 0.40 m
interpenetration, visible, from the frame. The corner reads as a corner.

---

## §3 — SCHEMA-COVERAGE CHECKLIST

Machine-generated by the build itself (`_print_coverage()`), not asserted by hand.

**Record types — 5 of 5 present, 5 of 5 consumed**

| record type | count across 450 | consumed |
|---|---|---|
| `header` | 450 | ✅ frame contract: arena, entities, spawns, radii, max_hp, hp_provenance, skills |
| `g5_header` | 450 | ✅ battery contract: run/tier/arm/window, door_values, opposition_roster, named_absent |
| `tick` | 117,907 | ✅ every per-entity key: `alive` `x_m` `y_m` `heading_rad` `hp` (+ `commit_state`) |
| `event` | 54,394 | ✅ dispatched (below) |
| `footer` | 450 | ✅ winner / elapsed_s / mobs_killed / player_alive |

**Event kinds**

| kind | count across 450 | state | note |
|---|---|---|---|
| `damage` | 41,289 | **RENDERED** | floater from **`delivered`**, per-crossing decomposition on nova hits, `element` colours ONLY |
| `death` | 2,160 | **RENDERED** | flash + corpse; never decided from hp |
| `telegraph` | 1,752 | **RENDERED** | footprint at the **resolved** `radius_m`; `damage_amount` shown as the announced figure |
| `leech` | 9,193 | **STUB (drawn: no)** | resource accounting, not spatial; fires with `healed = 0.0` for most of the fight — drawing a heal tick for a 0.0 heal is a render lie. Counted, undrawn, awaiting a HUD resource surface. |
| `decision` | **0** | **SCHEMA-READY, DARK** | absent from all 450 (baton §4.2). Path built, wired, inert; lights up with no code change when `trace_decisions` is armed. |

**Field-level disciplines honoured** (each is a named trap in the baton):

- `delivered` not `amount` — measured on this fight: `amount 1354.54` vs `delivered 846.00` on the
  shaman's death. `amount` overshoots on a lethal hit; the decomposition histogram was proved
  against `delivered`.
- `element` colours a hit and **nothing else** — no mitigation, no resist join, no type split.
- **No received-side crit affordance.** Structural zero with a named mechanism.
  `crit_multiplier = null` is read as *did not crit*, never as zero, never back-computed.
- `hp_provenance` rendered **four-valued**: `M (measured)` / `D (derived, adopted)` /
  `D-HELD (derived, WITHHELD)` / `— (none declared)`. **D-HELD has no code path that reaches D.**
  Unknown values hit a default arm that warns and renders verbatim.
- `MovementIntent` match carries a **default arm**; so does the event-kind match one level up.
- `range_m: 10.0` vs `radius_m: 12.0` — **the telegraph value governs**, and the mismatch is left
  standing as the routed discrepancy it is, not split.
- The 12.0 m disc is drawn **unclipped**, so the 1.92 m east overrun is visible running into the
  wall face. Trimming it would draw a footprint the sim never had.

---

## §4 — BATON-CONTRACT AMBIGUITIES (reported, not improvised)

**A1 — `leech` is a fifth event kind and the baton gives it no consumer note.**
§2 lists it among "event kinds present" (9,193 occurrences, 17 % of all events) but none of the
eight consumer notes says what a depiction owes it. `healed` reads 0.0 on the opening events while
`capacity` reads 42.30, and there is no note on whether the 0.0 is a floor, a cap-not-yet-consumed,
or an accounting artefact. **Stubbed and counted rather than guessed.** Ask: is `leech` a
presentation surface for G-D, and if so is the number to show `healed`, `cum_healed`, or the
capacity headroom?

**A2 — the per-leg unit payload has no home in the artifact set.**
The baton flags this itself (§4.1, "the one place where G-D depends on a number living outside the
trace set") and the flag is correct, but it leaves the number's *custody* unassigned. It currently
lives in `wr2_traceset.gd::LEGS` in the Godot repo — i.e. a **presentation-seam file is the
system of record for a simulation constant.** That is the wrong owner and it will drift the first
time a battery ships at a new regime. Ask: emit `unit_payload_hp` into the `g5_header` (additive,
no event-grain change, so §8.17's rejection does not apply), or publish it in the leg's
`kitcal_g5_*_report.json`. Either kills the external dependency; I should not be the one holding it.

**A3 — `damage_amount` on a telegraph is not the realized payload, and nothing says so.**
§2 certifies "telegraph events: 100 % carry `damage_amount`" as a completeness win, which reads
like it is the number to show. Measured on this fight: the nova telegraph announces **241.37**
while the crossing delivers **2 × 207.40 = 414.80**. Neither the announced figure nor its ratio to
the payload is documented. Rendered as an **announced** figure and explicitly excluded from the
decomposition. Ask: confirm `damage_amount` is nominal-pre-mitigation, so the depiction can label
it honestly instead of just placing it.

**A4 — a dead entity is DROPPED from the tick frame, not carried at `alive: false`.**
The baton's §2 per-frame key list includes `alive`, which implies a persistent row. Measured: the
shaman is `alive: false` at tick 0, and the melee escort simply **stops appearing in the entity
list** after it dies. A consumer that only reads rows present in the frame leaves the escort
standing at full health for the rest of the fight — and it looks fine, because nothing errors.
Handled (absence is read as the death it is), but the frame contract should say which of the two
it is, because they are different contracts and the traces use both.

**A5 — tick 0 is a POST-resolution frame, not an initial state.**
Player `hp` reads 728.24 against `max_hp` 759.0 at `t_s = 0.0`, and one mob is already dead. The
tick-0 damage events explain it exactly (30.757 to the player, 846.0 lethal to the shaman), so it
reconciles — but "tick 0 = state after tick 0 resolved" is not stated anywhere, and a consumer
that spawns from tick 0 rather than from the header's `spawn_x_m`/`spawn_y_m` will silently start
the fight a tick late. Spawning is done from the **header**, per the baton's §3(4) instruction.

*None of these is baton-blocking, none moves a banked number, and none touched a trace.*

---

## §5 — WHAT THE RENDER TAUGHT ME (three things the frame corrected)

Each was invisible in code and only a rendered frame caught it.

**5.1 — A settle window silently eats the nova.** The capture harness warms the renderer for 45
frames before the first PNG. The clock was running through it, so the first 1.5 s of the fight went
unrecorded — and the telegraph (t = 0.80 s) and its crossing (t = 1.9512 s) live entirely inside
that window. It would have failed **identically on every seed**, so nothing would have looked
wrong; the render would just never have had a nova in it. The clock is now **held through the
settle**: playback starts when capture does.

**5.2 — Two floaters on the ring's radial can be one floater on screen.** The decomposition fired
correctly and rendered as a single number. The radial from the nova origin through the target on
this fight runs (−0.60, −0.80) in sim coords — **within 10° of the play camera's view axis** — so
1.7 m of radial lead projected to ~0.3 m of screen separation and the two 207.40s landed on top of
each other. The count now rides the **screen-vertical** axis, which no camera bearing can collapse;
a small radial lead is kept so the pair still reads as coming off the ring. *The most faithful
decomposition in the world is worth nothing if the frame shows one number.*

**5.3 — A fade-in and a fade-out in parallel on one property is two writers per frame.** The
floater tween ran both on `modulate:a` under `Tween.parallel()`. Which one wins is a scheduling
detail. Symptom: **N−1 of N floaters render**, and it looks exactly like "the decomposer didn't
fire" — a rendering bug wearing a data bug's clothes. Split into two tweens, one property each.

*A fourth, smaller one:* the four-line provenance banner was laid across the **top** of the frame,
which is precisely where the SW corner sits under this camera bearing. The banner was covering the
finding. Only the clock stays up top now.

---

## §6 — SWAP-IN READINESS FOR THE AFTER TRACES

The AFTER traces are schema-identical, so the swap is a **path and a constant**, not a code change:

1. **Path** — `wr2_traceset.gd::BATTERY_ROOT` + a `LEGS` entry per AFTER leg (dir name → leg id,
   regime, unit payload). `--path <abs>` already bypasses the registry entirely for a one-off.
2. **Constant** — if the AFTER battery runs at a different mitigation regime its unit payload
   differs. **Unregistered legs render one undecomposed floater and say so**, so a forgotten
   constant fails loudly instead of silently rendering a 2× crossing as a single slab. See §4-A2.
3. **Aim-line** — if Cell A's supplementary emission arms `decision`, the overlay lights up with
   **no code change**; the `intent` match already carries its default arm for `EVADE`.
4. **Collision / movement v2 (Cells B and C)** — these change the *trace content*, not the schema.
   Playback stays trace-authored: **combatant collision is OFF here regardless**, because the
   traces already contain the positions and playback never re-simulates. If the AFTER traces stop
   showing interpenetration, the depiction stops showing it — because the numbers changed, not
   because the renderer did.

**What Matt should be able to tell me after watching:** whether the corner pin, the interpenetration
and the once-early clipped nova read as *findings* or as *bugs in my render*. That distinction is
the whole reason this eye is scheduled before the AFTER traces exist.
