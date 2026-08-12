# SB-1 · Cell 0 — the drax COUNTERSIGN of the consumer contract

**Cell ID:** `SB1-CELL-0` (charter § 7 lane table, § 11 launch condition (3))
**Date:** 2026-08-12
**Author:** drax (presentation seam — demo / loadout / **godot**)
**Charter:** `agentic_orchestration/gandalf/notes/2026-08-10-sb1-kc2-scene-run-charter.md` @ **`9b3e7e2b`**
(+ retention rider `7e503a8b`) · conductor gandalf (`RUN-CONDUCTOR`)
**Handoff under countersign:** `agentic_orchestration/gandalf/notes/2026-08-09-kc2-godot-handoff.md`
(Rider-1 verbatim § 2 · the ten consumer semantics § 3 · the countersign ask § 4)
**Producer contract:** `reincarnated-engine/src/reincarnated/export/MIGRATION.md` **`[2026-08-09b]`**
(board boundary R-L82-4 · BOX shape R-L82-2) and **`[2026-08-09]`** (the OBJ-1 seam-side re-law, F5-E := SIM-KNOTS)
**Godot repo HEAD at this cell:** `978a423b206c3b0881dd3d788a2523b64b51f5d5` (ledger L-0 pin — matches)

---

## 0 · What this cell is, and what it is not

This is a **countersign cell**. Split-cell law (CL-1): countersign and build never share a cell.
Nothing was built. **No Godot project mutation, no scene, no script, no import, no `.godot/` touch,
no engine write.** The engine tree was opened **read-only** (FG-17), the baton was read by `python3`
in a throwaway process, and the only artifact of this cell is this note plus its commit.

Everything below labelled *measured* was measured **from my own seat, off the bytes on disk**, not
taken from the handoff's or the producer's word. That is the whole point of a countersign: a
signature that only repeats the claim is worth nothing.

---

## 1 · Baton verification

**BATON VERIFICATION — digest MATCH: YES (`d7ecd866ac45`) · actors 344/344 · waves 20/20 ·
`provenance.out_of_model` = 9 entries · R-L53-2 ACKNOWLEDGED (cited on the wire at
`provenance.informative_rows[OBJ-1-UNION-RELAW]`, not in `out_of_model` — see NOTE-3).**

| check | expected | measured | |
|---|---|---|---|
| path | `…/output/kc2-baton-v1-E-s09-cp150-20260809_052836.json` | same | ✓ |
| SHA-256 | `d7ecd866ac45ec9647ca3d4f7850c41f6a7654e718451d9e5c38ccdb59b8d5aa` | **identical, full 64 hex** | ✓ |
| first 12 hex | `d7ecd866ac45` | `d7ecd866ac45` | ✓ |
| size | 1,065,632 B (1.066 MB) | 1,065,632 B | ✓ |
| actors | 344 | **344** | ✓ |
| waves | 20 | **20** | ✓ |
| event rows | 1,900 | **1,900** (`wave_start` 20 · `channel_start` 20 · `spawn` 344 · `damage_dealt` 1,132 · `death` 344 · `channel_release` 20 · `wave_end` 20 — sums to 1,900 exactly) | ✓ |
| track samples | 3,732 | **3,732 per track**, 4 tracks (`player_path` · `player_hp` · `player_energy` · `circle_sweep`), stride 1 on all four | ✓ |
| path knots | 1,003 | **1,003** (61×2 + 271×3 + 4×5 + 8×6) | ✓ |
| `out_of_model` | 9 | **9** — `OOM-DEVOTION-PROCS · OOM-MUTATORS · OOM-DEFENSES · OOM-BLESSINGS · OOM-RETALIATION · OOM-ASCENSION · OOM-TRIGGERED-BUFFS · OOM-M2-REWIND · OOM-REWARDS` | ✓ |
| R-L53-2 (summons out-of-model) | present | **present, one level over** — text on `informative_rows[OBJ-1-UNION-RELAW]`: *"Summoned bodies carry no path: OUT-OF-MODEL per R-L53-2, an absence rather than a gap."* Zero of the 9 `OOM-*` rows is the summons row. | ✓ w/ NOTE-3 |
| `informative_rows` | 19 (6 DIVERGENCE + 13 DECLARATION) | **19 — `{DECLARATION: 13, DIVERGENCE: 6}`** | ✓ |
| `tick_period_s` | `0.0816326530612245` | **`0.0816326530612245`** at `tracks._tick_base.tick_period_s` | ✓ |

The digest matched on the **first** read. I did not load this file a second time to build anything.

---

## 2 · Disposition table

Disposition ∈ **ACCEPT** / **ACCEPT-WITH-NOTE** / **OBJECT**.

| # | Item | Disposition | Basis — measured from my seat, on this baton |
|---|---|---|---|
| **a** | **Board boundary** (MIGRATION `[2026-08-09b]` § 1, R-L82-4): `spawn_tick` is LAST-STILL-TICK; the body is **not on the board until `path[0].run_tick + 1`**; the consumer **MUST NOT hit-test at `path[0]`** | **ACCEPT** | Non-vacuous, and I reproduced the exact consequence: **exactly 6 of 344** bodies have `path[0]` lying inside the `circle_sweep` disc (r = 3.0 m, `channel_active` true throughout) **at that same tick**. A loader that hit-tests at `path[0]` draws those 6 inside the telegraph one tick early and then finds no damage row for them — star-lord's "6 of the 61 drip bodies" reproduces exactly. The rule buys 6 real false positives and costs me nothing. **Signed.** |
| **b** | **BOX shape declaration** (MIGRATION `[2026-08-09b]` § 2, R-L82-2): read the SHAPE word from `scatter_model`, the half-extent from the typed `placement_extents_m`; magnitude is never in the prose | **ACCEPT** | Re-measured against `spawn_points[].point_id` at h = **8.0 m**: **342/344 inside the box · 272/344 inside the disc**. A disc loader misplaces **72 of 344**. The two outside-box bodies are **`w162_a001`** and **`w163_a004`**, **both p01** — precisely `DIV-P01-TIER`, declared, measured, not a scatter defect. Every producer number reproduces to the body. **Signed.** Two-token grammar (`"<OWNER> <SHAPE> -- <prose>"`) is machine-readable and I read the token, never the prose. |
| **c** | **OBJ-1** — `config.arena.path_coverage`, my 2026-08-08 named objection (`drax/notes/2026-08-08-kc2-baton-countersign.md` § OBJ-1) | **ACCEPT — OBJECTION WITHDRAWN, satisfied by measurement, without residue** | OBJ-1 was: two shipped rules gave two answers, **73.2 % of the render window had no position rule at all**, and `path[-1].run_tick == engage_tick` on **13 of 13** fixture actors. On the baton of record: **`path[-1].run_tick == death_tick` on 344/344**; `== engage_tick` on only **6** (bodies that died *at* engage — a tick coincidence, not the failure signature); **0** actors whose path ends before their terminal tick; lifetime-tick coverage **32,031 / 32,031 = 100.00 %, residual gap 0 ticks**. The contradiction is gone too — the "post-engage rides the event rows" clause no longer appears in `path_coverage`, and `path_interpolation`'s UNDEFINED now means pre-spawn and post-terminal only, which is what I asked for. I asked for an event-row **union**; the seam delivered **SIM-KNOTS**, which is strictly better — sim-recorded vertices instead of a reconstruction, and it declines to assert a straight line through the 283 bodies that measurably bend. **The banked `rows-compact` mitigation was never spent; it stays banked.** |
| **1** | `actors[].path[]` is VERTEX-COMPLETE in **VELOCITY** vertices; linear interpolation between knots **IS** the position function; **never assume uniform speed across a leg boundary** | **ACCEPT** | 1,003 knots over 344 actors, exact. The cross-leg warning is **non-vacuous**: **23 of the 283** multi-leg bodies carry measurably different per-leg speeds (e.g. `w154_a004` = 0.3265 / 0.3265 / 0.3265 / **0.1392** / **0.0** m per tick — the clipped arrival step and then the dwell). A renderer that fits one speed per body puts that body in the wrong place for its whole final leg. Within a leg the speed **is** uniform; that is what makes the interpolation exact, and I interpolate rather than resample. |
| **2** | A 2-knot path is a **measured straight walk** (61 of them — the p05 ambush bodies), **not a subsample** | **ACCEPT** | Knot-length histogram is exactly **{2: 61, 3: 271, 5: 4, 6: 8}**, and the p05 spawn-point population is **exactly 61**. The identity is 1:1. I draw a straight line between two knots and I do not "densify" it. |
| **3** | A dwell is **two knots at one place, two times**; 12 bodies wait 44–70 ticks at the engage ring before dying; **draw the wait**; never collapse on position | **ACCEPT-WITH-NOTE** | The named 12 reproduce exactly: zero-displacement knot pairs with Δtick **44, 44, 55, 69, 69, 69, 69, 69, 70, 70, 70, 70**. **But the dwell predicate as written catches 17 pairs, not 12** — five more are Δtick = 1. See **NOTE-1**. The rule itself is unimpaired and I follow it literally. |
| **4** | `spawn_tick` is LAST-STILL-TICK; not on the board until `path[0].run_tick + 1`; do not hit-test at `path[0]`; **the spawn knot's `tick`/`t_s` disagreement IS the measured drip — do not snap it to the grid** | **ACCEPT-WITH-NOTE** | Board-boundary half: **ACCEPT** (see row **a**). Drip half: accepted, with the magnitude corrected. Measured `actor.spawn_tick − spawn-event.run_tick`: **0 on 283 bodies, and +48 … +306 ticks on exactly 61** — the p05 set, one-signed positive. The handoff's "(≤ 1 tick, one-signed)" is the **bound tightness** from `DECLARED-BOUND-ON-DRIP`, **not the drip's magnitude**. Also measured: `spawn_t_s == path[0].t_s` on **344/344** — the sub-tick remainder does not ride `t_s`, exactly as the wire declares. See **NOTE-2**. |
| **5** | Spawn scatter is a **BOX, not a disc** — half-width `placement_extents_m` per axis; an 8 m circle places 72 of 344 wrong; the 2 tier-17 crossers are `DIV-P01-TIER` | **ACCEPT** | Same measurement as row **b**: 342 box / 272 disc / 72 misplaced by a disc / 2 crossers named to the body. Nothing further to add. |
| **6** | `tick` is **wave-local**; `run_tick` is the **global** clock; the tick period is the sim's exact float `0.0816326530612245` — **use the wire's value, never a re-derivation** | **ACCEPT-WITH-NOTE** | **Second half accepted flat and it is the load-bearing half:** the exact float is present at `tracks._tick_base.tick_period_s`, I read it from there verbatim, and I re-derive nothing (`1/12.25` written by hand moves 20 of 344 spawn ticks). **The naming half does not describe this wire** — on this artifact the only field literally named `tick` is global, and the wave-local column is null on every row. See **NOTE-4**. This is a prose hazard, not a wire defect: applied literally it would mis-join the entire player track in Act 2. |
| **7** | **Summons carry NO path** — out-of-model per R-L53-2, an **absence, not a gap**; do not fabricate motion for them | **ACCEPT-WITH-NOTE** | **0 pathless actors of 344** — PL-4's empty domain reproduced independently from my seat, before reading PL-4's number. Every one of the 344 carries a full measured path, so K-4's render-half has no domain on this baton and its prohibition-half is trivially satisfiable: **I fabricate no body and no motion.** The citation lives one level over from where the field name suggests — see **NOTE-3**. |
| **8** | Player heading is `0` and **DECLARED-NON-SEMANTIC** (EoR is a spin channel; heading is mine to drive from channel state); monster spawn heading is the **FACE-PLAYER-CAMP** convention, declared as such | **ACCEPT** | `player_path.heading_rad` distinct value set across all **3,732** samples = **{0.0}**. It carries no information and I will not read information out of it. `spawn_heading_rad` carries **344 distinct** values — a derived convention, and I treat it as a spawn-facing seed only, never as a motion authority. Channel→heading mapping is K-3, the conductor's ruling at the cell; I will not pre-empt it here. |
| **9** | `crit` columns are **NULL under `crit_model: NOT_MODELLED`** — null means not-modelled, never "measured zero crits"; defenses ship **DECLARED-COUNT-ONLY** (+4, names NAMED-ABSENT) | **ACCEPT** | `is_crit` is `None` on **1,900 / 1,900** rows, including all **1,132** `damage_dealt`. There is therefore **no crit channel in this scene**: no crit numbers, no crit colour ramp, no crit sound, and no "0 crits" readout — a rendered zero would be a fabricated measurement. Defenses render as a **count of +4 with NAMED-ABSENT labels**; I will not invent four defense names to fill four icon slots. |
| **10** | The **divergence ledger rides `provenance.informative_rows`** (19 rows: 6 `DIVERGENCE` + 13 `DECLARATION`, families overlap by design) — read it before judging any feel mismatch, including `DIV-F7-WALL` | **ACCEPT** | Exactly **19** rows, `{DECLARATION: 13, DIVERGENCE: 6}`; filtering `class == "DIVERGENCE"` yields **6**, precisely as the `[2026-08-09b]` corrigendum promises. `DIV-F7-WALL` is present. Per charter § 6 the ledger **ships beside the CP-C watch**, not after it — Matt reads the declared departures with the clip in front of him, not as an excuse afterwards. |

**OBJECT count: 0.** No item breaks Act 1 (statics), Act 2 (motion) or Act 3 (watch).

---

## 3 · Notes in full

The four NOTES are consumer hazards in **prose**, not defects in the **wire**. In every case the
typed fields are correct and self-consistent; what would break is a loader written from the
sentence instead of from the field. I record them so the next reader of this contract — including
me in six months — is not the one who finds them.

### NOTE-1 (semantic 3) — the dwell predicate catches 17, the named wait class is 12

Zero-displacement consecutive-knot pairs: **17**, not 12. Twelve sit in the named 44–70 tick band
(the engage-ring waits). Five more are **Δtick = 1** — the clipped arrival step landing a body on
its node for one tick before the next leg. Both satisfy the stated predicate ("two knots at one
position with different ticks"). **I draw all 17 as measured and filter none of them**; the five
one-tick pairs are invisible at watch scale, and dropping them would be me deciding which measured
knots count. Recorded so a future coverage gate that asserts "12 dwells" knows to assert
"12 dwells **≥ 44 ticks**" instead.

### NOTE-2 (semantic 4) — the drip is up to 306 ticks, not up to 1 tick

`DECLARED-BOUND-ON-DRIP` is accurate and I am not disputing it. The handoff's compression of it is
the hazard. The sim carries two disagreeing spawn facts and the gap between them is **large**:

| population | `actor.spawn_tick − spawn-event.run_tick` | count |
|---|---|---|
| non-p05 | 0 | 283 |
| **p05 (the drip)** | **+48, +85, +122, +159, +195, +232, +269, +306** | **61** (14 · 13 · 12 · 8 · 6 · 4 · 3 · 1) |

At the wire's own tick period, +306 ticks is **≈ 25.0 seconds**. A loader that puts bodies on the
board at their wave's `spawn` **event** row places 61 of 344 up to twenty-five seconds early —
the ambush stops being an ambush. **The ≤ 1 tick figure is the residual the `t_s` field cannot
carry, not the drip.** My mechanism closes this by construction: entry time comes from the
**actor row's `path[0].run_tick + 1`**, never from the spawn event row, which is the same rule as
the board boundary. The two semantics compose; following (a) literally makes NOTE-2 unreachable.

### NOTE-3 (semantic 7) — R-L53-2 is cited, but not in `out_of_model`

`provenance.out_of_model` holds **9** rows and every one is an `OOM-*` id (procs, mutators,
defenses, blessings, retaliation, ascension, triggered buffs, M2 rewind, rewards). **None of them
is the summons row.** R-L53-2 rides the free text of `provenance.informative_rows[OBJ-1-UNION-RELAW]`.
It is on the wire, it is unambiguous, and I accept it — but a consumer that programmatically
enumerates `out_of_model` to build its "declared absences" panel will not find summons there.
Zero impact on SB-1 (empty domain, PL-4). Recorded for the lap where a summon body actually lands.

### NOTE-4 (semantic 6) — on this wire, the field named `tick` is GLOBAL

Measured:

- `tracks.player_path.tick` (and `player_hp` / `player_energy` / `circle_sweep`) is **contiguous
  1 … 3,732**, monotonic, and joins 1:1 with the knots' `run_tick` domain (0 … 3,732; only knot
  tick `0` sits outside the track domain, which is the spawn of the wave-151 bodies).
- `waves[].tick_start` / `tick_end` are **also global and non-restarting**: w151 = 1…226,
  w152 = 227…370, w153 = 371…566.
- **`events[].fight_tick` — the wave-local column — is NULL on 1,900 / 1,900 rows.**
- **0 of 1,003** knots fall outside their own wave's global `[tick_start − 1, tick_end]` span.

So the wave-local clock is *absent by measurement* on this artifact, and the one field literally
spelled `tick` is the global one. A loader that reads semantic 6 at face value and offsets track
ticks by `waves[].tick_start` mis-joins the **entire** player track — 3,732 samples, every wave.
**Not an OBJECT:** nothing on the wire is wrong or ambiguous once you look at the domain, and my
loader keys on one integer clock in `[0, 3732]` and applies no wave offset anywhere. It would bite
in **Act 2**. The smallest change that would remove the hazard for the next consumer is one
sentence in the handoff — *"on baton/v1 the `tracks.*.tick` column is the global clock;
`events[].fight_tick` is the wave-local one and is null under this emit"* — and that sentence is
gandalf's to write, not mine to take.

### NOTE-5 (raised, not mine to fix) — the `OBJ-1-UNION-RELAW` row cites the superseded knot supply

The provenance row ends: *"Supply: `kc2-phase-e-actor-paths-E-s09-cp150-R-L80-2-20260809_025245.json`"*.
Measured on disk:

| artifact | sha256 | knots |
|---|---|---|
| `…-R-L80-2-20260809_025245.json` (**named on the wire**) | `303978a01337…` | **995** |
| `…-R-L82-1-20260809_041421.json` (**pinned by MIGRATION `[2026-08-09b]`**) | `2ba67fc152c3…` | **1,003** |

The baton carries **1,003** knots, so it was built from the **R-L82-1** supply while its own
provenance sentence names the **R-L80-2** one. The numbers on the wire are right; the citation is
one lap stale — the exact class of thing the L-79(e) stale-field rule exists to catch, sitting in
free text rather than in a typed field. **Nothing breaks in any SB-1 act** (I load the baton, never
the supply, and the knot count verifies), so this is **non-blocking and not a HALT**. Per my seam
rule I do not patch the engine: **routed to knight-rider for star-lord.** No `// TODO(drax)`
override is needed anywhere on my side, because nothing of mine reads that string.

---

## 4 · Consumer-readiness statement

Per item: the Godot-side mechanism I will **actually** use. Existing harness pieces are named by
path at `reincarnated-godot` HEAD `978a423b`. Where a piece does not exist yet, I say so — those
are **NOTES, not blockers**, and none of them blocks **Act 1 (statics / CP-A)**.

**Baseline that already exists and transfers:** the WR2 trace-playback stack is a working
implementation of exactly this shape of contract — a frozen upstream measurement, rendered with
zero derivation.

| piece | path | what it gives SB-1 |
|---|---|---|
| playback root | `scripts/wr2_playback.gd` (14,559 lines) | the **ZERO-DERIVATION law in code**: entity transforms are authored by the trace; it computes no damage, resolves no hit, decides no death, moves nothing the trace did not move. That law is the SB-1 law verbatim. |
| trace loader | `scripts/replica_trace.gd` (302 lines) | the int-cast JSON boundary discipline (`int(o.get("tick", …))` at `:228`, `:240`, `:252`, `:255`, `:279`) — my **O-1** obligation, already implemented once and proven. |
| registry | `scripts/wr2_traceset.gd` (838 lines) | the pattern for **units-and-constants-come-from-the-emission, never from a presentation-seam literal** (R-WR2-15(2)). |
| actor rig | `scripts/wr2_actor_rig.gd` (925 lines), extending `scripts/rival_boss_rig.gd` | `drive(speed_ms, dt, …)` at `:539` — locomotion blended from **measured** speed; `strike()` at `:624` — damage-emission driver; `set_frozen()` at `:678`; `set_death_phase(k)` at `:694` (procedural, declared procedural — there is no death clip in the Synty tree). |
| room grammar | `scripts/kit_replica_level.gd` (5,064) via `scripts/wr1_level.gd` (643) | K-2 arena dressing under GL-17 (reference governs frame/layout/ornament/palette, never copied). |
| capture | `scripts/capture_rig.gd` + `scenes/CaptureRig.tscn` + `scripts/render_capture.gd` | CP-A still-sets. |
| watch | `scripts/run_wr2_playback.sh`, `scripts/run_replica_mp4.sh` | headless render → ffmpeg → MP4 for CP-B / CP-C and the G-WATCH promotion path (temp-name → ffprobe-verify → promote). |

| item | Godot-side mechanism |
|---|---|
| **a · board boundary** | The loader computes an **entry tick** per actor as `int(path[0].run_tick) + 1` and the actor node's `visible` / hit-test participation both key off it. `path[0]` is used **for placement only**. Concretely: two separate fields on the actor record — `draw_from_tick = path[0].run_tick`, `test_from_tick = path[0].run_tick + 1` — so the distinction cannot be lost to a later edit. Any sweep-membership query below `test_from_tick` returns UNDEFINED, and UNDEFINED is a state I render as *absent from the test*, never as *false*. |
| **b / 5 · BOX** | Spawn markers are drawn as an **axis-aligned square of side 2 × `placement_extents_m`** (16.0 m) centred on the body's own emitter anchor, read from `config.arena.spawn_points[]` joined on `actor.spawn_point_id`. The shape token is parsed from `scatter_model` by splitting on whitespace and taking token 2 against the closed set `{BOX, DISC}`; the magnitude comes only from the typed field. **No circle is drawn anywhere for scatter.** The two `DIV-P01-TIER` crossers (`w162_a001`, `w163_a004`) are rendered in place with a declared-divergence marker, not clamped into the box. |
| **c · OBJ-1** | Position comes from `path[]` alone, over the closed span `[path[0].run_tick, path[-1].run_tick]`, which I have measured to be the body's **whole life**. `Scene.actor_position(run_tick)` in GDScript is a bracketing-knot lookup + `lerpf` on the two bracketing knots, differentially checked against `export/baton_v1_stub_consumer.py` per G-SEM. **No event-row union is implemented** — it is not needed and building it would reintroduce a second position authority. |
| **1 · velocity-vertex-complete** | Bracketing-knot interpolation **parameterised on `run_tick`**, per leg, with the leg re-selected every frame. ⚑ **Gap, named:** the existing dense-frame lerp in `wr2_playback.gd` (`:4147–4149`, `_lerp_angle` at `:4530`) assumes consecutive **frames**, because WR2 replica traces are per-tick dense. The KC2 baton is **knot-sparse with non-uniform per-leg speed**, so the KC2 loader gets a **new** bracketing function rather than a reuse of that one; the WR2 lerp stays untouched and un-forked. Locomotion cadence feeds `drive(speed_ms)` from the **leg's own measured speed** (`Δdistance / Δtick × 1/tick_period_s`), so a body that clips its arrival step visibly slows — which is what the wire says happened. |
| **2 · 2-knot straight walk** | Falls out of the same bracketing function with no special case: one leg, one uniform speed. **No densification pass exists in the loader**, so there is nothing that could turn a measured straight walk into a fitted curve. |
| **3 · dwell** | Handled by the same function without a branch — a zero-displacement leg holds position for its Δtick, and `drive(0.0)` selects the idle clip on the rig. The rig's `set_frozen()` (`:678`) is **not** used for dwells: a dwell is a body standing still, not a paused animation. **Never keyed on position** — the knot list is walked by index, so two knots at one place cannot collapse. |
| **4 · spawn drip** | Entry time is the actor row's `path[0].run_tick + 1`, so the 61 p05 bodies arrive at their measured +48…+306 tick offsets **as data**. No snap, no quantise, no per-wave batch spawn. Per **K-5** the drip is rendered as measured. The `spawn` event row is used **only** for its roster/binning duty, never for timing (NOTE-2). |
| **6 · tick domain** | **One integer clock.** Every join — actor knots, `circle_sweep`, `player_path`, `player_hp`, `player_energy`, event rows — is keyed on `int(run_tick)` in `[0, 3732]`, with `int()` applied at the JSON boundary per **O-1** (the pattern already in `replica_trace.gd:228`). `t_s` is never a key. `waves[].tick_start/tick_end` are used for wave banners and binning only, and **no wave offset is applied to any track index**. |
| **7 · summons** | Nothing to build: 344/344 pathed. The loader's actor-instantiation path **has no fabricate branch at all** — a pathless actor raises rather than being placed, so K-4's prohibition half is enforced structurally rather than by discipline. If a future baton lands a pathless body, the loader stops and says so instead of guessing. |
| **8 · heading** | Player heading is driven **entirely** from channel state (`tracks.circle_sweep.channel_active` + K-3's conductor-ruled channel→heading mapping), and the loader **does not read `player_path.heading_rad` at all** — reading a declared-non-semantic field is how a zero becomes a fact. Monster bodies are seeded to `spawn_heading_rad` at spawn, then yawed from **trace kinematics** (leg bearing), one writer, per the `wr2_actor_rig` rule that heading is the playback's job and not the rig's. |
| **9 · crit / defenses** | No crit channel is instantiated. HUD damage readout renders `damage_applied` with `hp_after` authoritative (`config.model.damage_semantic`), and the crit slot is **absent from the layout**, not present-and-empty. Defenses render as a count of 4 with `NAMED-ABSENT` labels, using the existing declared-absence dress from `scripts/hud_minimap.gd`'s vocabulary. |
| **10 · divergence ledger** | Parsed from `provenance.informative_rows` and rendered as a companion panel/card beside the CP-C watch, filtered on `class` (6 DIVERGENCE, 13 DECLARATION, both shown, families labelled as overlapping). ⚑ **Gap, named:** no such panel exists yet; it is Act-3 work and blocks nothing before then. |
| **K-1 · melee under Rider-1** | ⚑ **The sharpest thing in this note.** `scripts/wr2_actor_rig.gd` documents a two-driver attack split: `charge(k)` = telegraph **wind-up**, `strike()` = damage **emission**. Measured at HEAD: **`strike()` exists at `:624`; `func charge` does not exist anywhere in `scripts/`.** I will use **`strike()`, keyed to the `damage_dealt` row's `run_tick`**, and I will implement **no** wind-up driver. Likewise `wr2_playback.gd:_spawn_telegraph()` (`:5958`) stays dark: this baton's event vocabulary is `wave_start / channel_start / spawn / damage_dealt / death / channel_release / wave_end` — **there is no telegraph row to drive it from**, measured across all 1,900 rows. Back-timing a wind-up from an impact is fabricating timing grammar (GL-12), and I am refusing it here in writing before anyone asks. The abruptness is the honest declared state until Rider-2. |
| **G-COV event binning** | All 7 event types have a named consumer: `wave_start`/`wave_end` → wave banner + phase boundary; `spawn` → roster binning only (**not** timing, NOTE-2); `damage_dealt` (1,132) → `strike()` + arriving-damage dress + HUD numbers; `death` (344) → `set_death_phase(k)` at the row's `run_tick`; `channel_start`/`channel_release` → the EoR spin channel drive (K-3). **0 rows unbinned.** |

**Not-blockers, restated plainly:** the two gaps above (KC2 bracketing interpolator; divergence-ledger
panel) are **new work in my own lane**, not missing inputs. Nothing in the baton is absent that Act 1
needs. **Act 1 can start on this contract as it stands.**

---

## 5 · Already-ruled context, acknowledged (not re-litigated)

- **PL-4 — zero summon bodies in this baton.** Acknowledged and independently reproduced (0 pathless
  actors of 344). **K-4 reduces to its prohibition half**: fabricate no bodies, no motion. The
  render-half is **DORMANT — empty domain this run**. I do not re-open which rostered kits *could*
  summon in the source game; the sim simulated none, the wire carries none, the scene renders none.
- **K-1 as leaned — impact-anchored melee.** Acknowledged and adopted as written; my mechanism above
  implements the prohibition structurally (no wind-up driver exists to accidentally call).
- **Retention law PL-5 (Matt: "LAW").** Acknowledged as **binding on capture work**. It is
  galadriel's lane this cell and I ran no render and wrote no frame; my Act-2/Act-3 render cells will
  open with the floor check.
- **Rider-1.** Acknowledged verbatim. This baton underwrites geometry, composition, roster, path,
  sweep and timing; it does **not** underwrite attack-timing grammar, and that absence is
  **declared, not missing**. Playtest-readiness is a downstream milestone at Matt's eye, not a
  predicate of this run.

## 6 · Standing consumer obligations, carried forward unchanged

From `drax/notes/2026-08-08-kc2-baton-countersign.md` § Obligations and the coverage sign § F.1–F.7:
**O-1** int-cast `run_tick` at the GDScript JSON boundary, never key on `t_s` · **O-2**
`positions_provenance` read as an object, no prose sniff · **O-3** scene identity keyed on
(`arena_archive`, `arena_key`) = (`sm1`, `survivalworld_a`), with `emitter_radii.grade` =
`CITED-PER-ARENA` permitting the emitter rings to be drawn · **O-4** replay only — no position
derived from `d_engage_m` + `player_path`, none from `v_ref` (which remains a DECLARED FREE
PARAMETER at 4.0 and which my loader does not read), none from re-simulation · **O-5** default-arm +
`push_warning` on unrecognised declaration ids and policy strings · **O-6** re-measure real artifact
size against ~100 MB, not against a remembered 22 MB — **measured this cell: 1,065,632 B. Not close.
Nothing to escalate.**

One frame fact I add here because Act 1 depends on it: `config.arena.axis_convention` declares
**right-handed, `up_axis: +z`, `facing_zero: +x`, CCW-positive, metres, `ground_elevation: 0.0`**,
with `collision_model: OPEN-PLANE` and `arena_bounds.shape: UNBOUNDED`. Godot is right-handed with
**+Y** up, so the loader maps sim `(x, y)` → Godot `(X, Z) = (x, −y)` at ground `Y = 0`, under which
a sim heading θ becomes a Godot yaw of **+θ about +Y** with no sign flip. That is a **presentation-seam
frame transform, mine to own** — not a gap in the wire, and stated here so the sign convention is on
the record before any body is placed.

---

## 7 · Sign-off

I read the handoff, the charter at `9b3e7e2b`, and the producer contract at MIGRATION
`[2026-08-09b]`. I verified the baton's digest, counts and declarations against the bytes on disk
rather than against anyone's summary, and every producer claim I could test reproduced **exactly**
— 342/344 in the box, 272 in the disc, 72 misplaced by a circle, 2 crossers named to the actor id,
6 bodies caught by the board boundary, 61 p05 straight walks, 12 waits in the 44–70 band, 1,003
knots, 19 provenance rows, 6 divergences.

**My one standing objection, OBJ-1, is withdrawn.** It asked for a position rule over the whole
render window; the wire now measures **100.00 % coverage with a residual gap of zero ticks**, by a
better mechanism than the one I proposed. That is what a satisfied objection looks like, and I will
not carry it forward as a grudge.

Four notes ride out of this cell. **None of them is a defect in the artifact** — each is a place
where the prose would mislead a loader that trusted the sentence over the field, and each is closed
on my side by a mechanism named above. One finding (NOTE-5, the stale supply citation) is routed to
knight-rider for star-lord and is **not mine to patch**.

**The consumer contract is countersigned. Act 1 is unblocked from my seat.**

**VERDICT: NOTES**

— drax, presentation seam, 2026-08-12
