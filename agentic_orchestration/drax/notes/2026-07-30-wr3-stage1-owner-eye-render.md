# WR3-KITE-COMMIT — THE STAGE-1 OWNER-EYE RENDER (owner-eye #3)

> **Cell:** owner-eye #3 of run **WR3-KITE-COMMIT**. **Agent:** drax (presentation seam).
> **Conductor:** gandalf (RUN-CONDUCTOR). **Commission:** stage-1 owner-eye, geometry verbs first.
> **Consumed:** `agentic_orchestration/gamora/notes/2026-07-30-wr3-stage1-build-report.md`
> (engine `6de80aab`), and the WR2 AFTER-baton clause-by-clause where it still governs.
> **Repo:** `reincarnated-godot` — commit **`72723ca`**, **NOT PUSHED** (the conductor pushes).
> **Trace roots:** both opened **READ-ONLY**, nothing written, nothing copied out, nothing
> regenerated. `git status` in the engine tree shows **no modification** under
> `wr2_battery_after/` — the frozen WR3 BEFORE evidence — at cell end.

---

## §0 — THE ONE-PARAGRAPH ANSWER

**Seed 74000802, leg `pre` (R2_proxy, cold 0.14), tier `boss`, arm **B**, both arms of the WR3
battery pair.** In the BEFORE clip the player walks into the boss at t = 1.8 s and never leaves:
separation reads **2.000000 m** — the combined-radii floor, to six decimals — for **332 of 352**
post-contact ticks, the widest gap the whole 37-second fight ever produces is **2.022 m**, the boss's
`commit_state` reads `idle` on every tick of every entity, no `evade:` limb appears on any decision,
the player walks *into* the nova ring (10.21 m → **5.707 m**) and eats **414.80 HP = 2 × 207.40**,
and he dies. In the AFTER clip, same seed, same leg, same arm, the separation is **alive** — median
**2.471 m**, ranging **2.000 – 6.157 m**, pinned on only **146 of 915** ticks — the boss locks into
**55** commit windups of which **53 resolve against empty ground**, the player backs *out* of the
first nova ring (10.21 m → **12.221 m**, clear of the 12.00 m footprint by 0.221 m), and he wins at
**95.0 s**. **The contrast is not subtle and it does not need to be pointed at.** What does need
pointing at is what happens after **t ≈ 18.8 s**: the fight becomes a **metronome**. The separation
pair at (windup, strike) freezes at **(2.000, 2.7584) m** and repeats, bit-identical, roughly fifty
more times until the boss dies. That is build report **§F-4's "broken-easy" direction, visible** —
and it is the thing this watch exists to let Matt judge before anybody calibrates a number.

---

## §1 — THE DELIVERABLES

All under `/Users/admin/Games/reincarnated-godot/tmp/wr2/`. 1280×720 · 30 fps · **1× real time** ·
single fixed camera per clip · **no cut, no speed-up, no edit**.

| # | file | what it is |
|---|---|---|
| **1** | `/Users/admin/Games/reincarnated-godot/tmp/wr2/wr3_after_pre_boss_B_74000802.mp4` | **THE WATCH.** AFTER, 2,848 frames, **94.93 s**, 9.4 MB |
| **2** | `/Users/admin/Games/reincarnated-godot/tmp/wr2/wr3_before_pre_boss_B_74000802.mp4` | its **BEFORE twin**, same seed / leg / tier / arm, **same lens**, 1,109 frames, **36.97 s** |
| **3** | `/Users/admin/Games/reincarnated-godot/tmp/wr2/wr3_sidebyside_B_74000802.mp4` | (2) and (1) **hstacked**, 2560×720, BEFORE left / AFTER right, one timeline |
| **4** | `/Users/admin/Games/reincarnated-godot/tmp/wr2/wr3_stills/` | **the annotated frame sequence** — nine captioned stills, §3 |

**⚑ One disclosed edit, and it is only in (3).** The BEFORE fight is 37.0 s and the AFTER fight is
95.0 s. To hstack them on one timeline the BEFORE side **holds its final frame** (`tpad`
`stop_mode=clone`) for the remaining 58 s. Nothing is sped up, nothing is trimmed, and both halves
still carry their own full provenance banner. Clips (1) and (2) are untouched.

The nine stills (all under `/Users/admin/Games/reincarnated-godot/tmp/wr2/wr3_stills/`):

| file | tick / t | what it shows |
|---|---|---|
| `A1_ring_mint.png` | 7 / 0.70 s | the 12 m ring is minted; player **10.21 m** in, 2.32 s of tell to run, intent `evade:tg` |
| `A2_ring_fires.png` | 30 / 3.019 s | it fires; player **12.221 m** out — **OUTSIDE by 0.221 m** |
| `B1_kite_start.png` | 95 / 9.50 s | a kite bout opens at **2.025 m** — on the contact floor |
| `B2_kite_open.png` | 110 / 11.00 s | 1.5 s later, **6.157 m**. The bout gained **4.132 m** |
| `C1_commit_lands.png` | 72 / 7.20 s | a commit that **LANDS** — 2.259 m < C_reach 2.50 m |
| `C2_commit_windup.png` | 98 / 9.80 s | the lock opens; the 7-tick shape and the §1.2 disagreement |
| `C3_commit_whiffs.png` | 102 / 10.20 s | **WHIFF · 4.225 m > reach 2.50 m** |
| `D1_metronome.png` | 658 / 65.80 s | the same strike, 55 s later, at **2.7584 m** — bit-identical |
| `E1_before_pin.png` | 185 / 18.50 s | BEFORE: **2.000000 m**, welded |

**Machinery** (committed in `reincarnated-godot`, `72723ca`):
`/Users/admin/Games/reincarnated-godot/scripts/wr2_traceset.gd` ·
`/Users/admin/Games/reincarnated-godot/scripts/wr2_playback.gd` ·
`/Users/admin/Games/reincarnated-godot/scripts/wr3_pick_scan.py` ·
`/Users/admin/Games/reincarnated-godot/scripts/wr3_stills.py` ·
`/Users/admin/Games/reincarnated-godot/scripts/run_wr2_playback.sh`

---

## §2 — WHY THIS FIGHT, AND WHY THE COMMISSION'S DEFAULT PICK WOULD NOT HAVE WORKED

**Selection was measured, not eyeballed.** `wr3_pick_scan.py` scores every one of the **66** AFTER
boss fights (3 legs × 2 arms × 11 seeds) on the three verbs the commission names, and it requires
all three: a kite bout that **opens** separation, at least one **whiffed** strike, and a **ring
escape**. **60 of 66 carry all three** — which independently reproduces G2's 60/66 from the other
side of the seam.

**⚑ THE COMMISSION'S FALLBACK PICK CANNOT CARRY VERB (c).** The brief says *"if selection is hard,
default to seed 74000800."* **Seed 74000800 fires no nova at all** — zero `circle` telegraphs, in
both arms, in all three legs. It is the same seed that was nova-free at WR1 and it is still nova-free
here. A render on it would have shown the kite and the whiffs and then silently omitted the ring.
Absence is data; it is not a demonstration.

**Why 74000802 / pre / B.** Every other qualifying fight was scored against it and none of them buys
what this one buys:

> **The WR3 BEFORE root IS the WR2 AFTER battery.** Those are the same 450 files under two roles,
> not a copy. So the BEFORE clip Matt watches at owner-eye #3 is **byte-identically the fight he
> watched as the AFTER clip at owner-eye #2**. One seed, three geometries — WR1's corner-pinned
> drift, WR2's east-wall orbit, WR3's kite — and one continuous lineage.

The cost is honestly stated: at **95.0 s** it is the longest of the qualifying candidates (the
shortest, `post`/74000810, runs 64.6 s). The lineage was judged worth 20 seconds. The measured
contrast:

| | BEFORE (frozen) | AFTER (11-seed diagnostic) |
|---|---|---|
| winner / duration | `monster` / **37.0 s** | **`player`** / **95.0 s** |
| post-contact separation | med **2.000000** · max **2.022** m | med **2.471** · max **6.157** m |
| ticks at the 2.0 m floor | **332 / 352** | **146 / 915** |
| `evade:` limbs on `decision` | **none** | `evade:commit` **315** · `evade:pressure` **46** · `evade:tg` **18** |
| boss commit episodes | **0** | **55** |
| strikes landed / whiffed | — | **2 / 53** |
| nova ring #1, player radius at firing | **5.707 m** — INSIDE, delivers 414.80 | **12.221 m** — **OUTSIDE** |

Every figure above is measured by this seam off the traces. None is transcribed.

---

## §3 — THE THREE VERBS, AS RENDERED

Each is a **field read** or **a distance between two trace-authored positions**. Nothing else.

### (a) THE KITE — `decision.intent`, `evade:`-prefixed

`evade:commit` (K-T2a) is **315** of this fight's ticks. The widest bout runs ticks **95 → 110** and
takes separation **2.025 → 6.157 m**. It is drawn as an aim-line colour and named on the clock line
with its limb gloss (`evade:commit [K-T2a COMMIT evade — the kite]`), because the limb is a string
the engine emits and not a label this seam invented.

### (b) THE COMMIT LOCK AND THE WHIFF — `tick.entities[].commit_state`

The boss's block cycles `idle → windup → strike → recovery → idle`. The scene draws a **ground disc
under the boss at C_reach**, amber through the windup, white on the strike tick, slate through
recovery; on the strike tick it freezes a **reach ring at the strike origin** — frozen, not chasing,
because **C2-L2 freezes position AND heading for the whole lock and a ring that followed would draw a
re-aim the mechanism does not have** — and floats the verdict:

```
WHIFF · 4.225 m  >  reach 2.50 m
```

**The whiff is the ABSENCE of a boss-sourced damage event on the strike tick.** This renderer runs no
hit-test of its own; that absence *is* C2-L1's live-geometry semantics, and using anything else would
have been a second implementation of the mechanism.

### (c) THE RING ESCAPE — `telegraph` (shape `circle`) + the player's position at `fire_tick`

The 12.00 m footprint is drawn unclipped from `radius_m` at the record's own `origin_x_m/y_m`, for
`fire_t_s − t_s` = **2.318840580 s**, and the clock line carries the live radius:

```
ring live  r 10.21 m / 12.00 m  (2.3 s to fire)      ...      ⚑ RING FIRES  r 12.22 m / 12.00 m  →  OUTSIDE
```

**⚑ ESCAPED IS NOT DELIVERED, and this seam does not conflate them.** Build report §F-2 measures
**0 of 114** rings delivering on this arm and **54 of 114** firings that neither escaped nor
delivered. "Outside the footprint" is what the frame claims and all it claims. This fight's **second**
ring fires with the player at **11.011 m — inside the footprint — and still delivers nothing**; it is
rendered exactly that way, and it is one of the 54.

### WHAT IS DELIBERATELY NOT DRAWN

**There is no per-frame `ai_state` in this schema.** That is W-1, post-stage-1, and the commission
says so. No label on any frame names a policy state the trace does not name. `commit_state` and
`intent` are quoted verbatim; everything else on screen is a distance.

---

## §4 — ⚑ FINDINGS. Three of these disagree with something on record.

### FINDING 1 — ⚑ **THE COMMIT LOCK IS 7 EMITTED TICKS, NOT THE 6 THE BUILD REPORT DECLARES.**

Build report §1.2: *"T_lock realizes as exactly 6 locked ticks with the strike inside: windup 3
(0.30 s) → strike 1 (0.10 s) → recovery 2 (0.20 s)."*

**Measured on `commit_state`, all 66 AFTER boss fights, 3,096 of 3,098 episodes, zero variance:**

```
windup 4  →  strike 1  →  recovery 2      = 7 LOCKED TICKS
```

The other two are windups truncated by the end of a fight. **And the boss's own melee telegraph sides
with the field, not the prose:** mint tick **68**, `fire_tick` **72** — a **four-tick lead** against
`wind_up_s: 0.30`. The engine's own `c2_telegraph_lead_mismatch` reads **0**, so the emitter is
self-consistent; the disagreement is **prose vs emission**, not field vs field. Most likely an
inclusive/exclusive sampling convention at the windup boundary — but that is a guess and this seam
does not ship guesses. **The render draws the field (4/1/2) and puts the disagreement on the banner.
Not split, not reconciled, routed.**

### FINDING 2 — ⚑ **THE FIGHT BECOMES A METRONOME AT t ≈ 18.8 s, AND MATT SHOULD SEE THAT.**

From roughly the fifth commit episode onward, the separation pair at (windup tick, strike tick)
freezes:

```
sep@windup 2.0000 m   →   sep@strike 2.7584 m       repeated, bit-identical, ~50 times
```

Across all 66 AFTER boss fights the **median fight spends 69 % of its commit episodes inside one
frozen pair**, and the frozen value is `(2.000, 2.7584)` on 46 of 66. Onset ranges 12.9 – 56.6 s,
median **18.8 s**.

This is not a render artifact and it is not a defect — it is the legible surface of §F-4. The boss
lands **4.45 %** of its melee (136 / 3,098) and **0 %** of its novas, the player wins **66 of 66**,
and the reason is visible on the frame: **the swing is a clockwork and the player has solved it.**
`bout_max` / `release_m` / `pressure_threshold` are stage-2 [CAL] rows and the build report already
routes them; this note only adds that **the failure §8.6 called "the one that does not announce
itself" announces itself very clearly at 1× real time**, and by 20 seconds in.

### FINDING 3 — ⚑ **C_reach LIVES OUTSIDE THE TRACE. Same custody shape the nova unit payload had.**

The whiff verdict needs the boss's reach, and **the trace does not carry it**. The boss's skill row
says `range_m: 2.0` and the combined body radii are **2.0 m**; **neither is C_reach** — a renderer
drawing 2.0 m would put **100 % of the whiffs AND 100 % of the lands** on the same side of its own
ring. The number is **2.5 m** and it lives in `AFTER.G2.definition.c_reach_m` inside
`output/kitcal_g5/wr3_cell_kc_statistics.json`.

Rather than hold it, this seam **reads it**, exactly as R-WR2-15(2) made it read the nova unit
payload — and **verifies it against the traces before drawing anything**:

| | n | min | max |
|---|---|---|---|
| separation at strike, **LANDED** | 136 | 2.0055 | **2.4837** |
| separation at strike, **WHIFFED** | 2,960 | **2.5750** | 4.2251 |

**2.5 m separates them cleanly, with 0.091 m of air between the two sets**, and 136 / 2,960
reproduces the build report's counters exactly. So the ring is a **measured boundary**. An
unresolvable C_reach draws **no ring at all** and the frame says why — it never falls back to 2.0.

**The ask, routed not ruled:** the cell-statistics JSON is a *grading artifact*, not an emission
contract. If C_reach were emitted into the leg report (or the `g5_header`) beside
`presentation_units`, the render would stop depending on a cell's output file. **Same argument that
closed the unit-payload custody question, one layer out.**

### FINDING 4 — ⚑ THE `evade` VALUE GREW A SUFFIX, AND THE WR2 CONSUMER WOULD HAVE DROPPED IT SILENTLY

SS-K-1's consumer obligation is real and this seam was on the wrong side of it. The WR2 aim-line
matched `"evade"` by **exact equality** — correct then, because that was the whole value set. Under
`kite_policy_v1` the intent reads `evade:tg` / `evade:commit` / `evade:pressure`, and on this fight
that is **379 of ~950 ticks** falling through to the unknown-value arm and being painted in the
default colour. **It would have warned, not errored, and the clip would have looked fine.**

Now `TS.is_evade()` tests the **prefix** first and the three limbs get three colours; the bare value
keeps its own arm; a fourth limb hits a default that warns by name. **This is the third value-set
growth in three runs** (`reposition` at WR2, `evade:*` here, `commit_state` going non-`idle`). The
pattern is stable enough to state as a rule: *on this schema, an exhaustive match without a default
arm is a latent silent-wrong-render.*

### FINDING 5 — INFO — the telegraph channel is **one event per attacker per skill**, not per swing

This fight has **55** boss melee commits and **one** boss melee `telegraph` event. Across 22 AFTER
boss traces: 22 boss point telegraphs (exactly 1 each), 44 escort point telegraphs (2 each), 38
circle telegraphs. **The per-swing wind-up is therefore NOT recoverable from the telegraph channel** —
`commit_state` is the only per-swing source, and it is the one the render uses. Recorded because a
consumer that reached for `telegraph` to draw the tell would have drawn **one** tell in a
95-second fight and nothing would have errored.

### FINDING 6 — INFO — the presentation-units block reports **0 crossings**, and the reader handles it correctly

`presentation_units.nova_unit_payload_hp` on the WR3 legs reads `values_observed: []`,
`n_nova_crossings: 0`. The reader resolves the unit to **UNRESOLVED** with the reason
*"absence is data"*, prints it on the banner, and never guesses a divisor. That is F-2 arriving at
the presentation seam intact. **The BEFORE twin still decomposes 414.80 → 2 × 207.40 exactly**, so
the reader is not merely failing quietly in both directions.

### FINDING 7 — INFO — arms A and B are **not** identical, but they are geometrically indistinguishable here

The A and B traces differ (different SHA-256). Every geometric statistic in the scan — median
separation, max separation, bout count, best-bout gain, strike count, whiff count, both nova radii —
is **identical to four decimals** between the arms on all 11 seeds. Only fight length and HP differ.
Recorded, not investigated: the arms exist for `battle_surge`'s absence, which is a healing question,
and this render is a geometry render.

---

## §5 — ⚑ PIPELINE GAPS AND ONE CAUGHT LIE

### GAP 1 — the lens the fight needs and the lens the comparison needs are not the same lens

`arena_full` (yaw 47° / pitch −41° / FOV 40° / 58 m) is the pose owner-eye #2 shipped on, so the
BEFORE/AFTER pair is apples-to-apples with the clip Matt has already seen. The framing audit confirms
it holds this fight: worst normalised player margin **+0.152**, all four arena corners on frame.

But it stands 58 m off a 36 m arena because it has to — **the AFTER player crosses from x = 31.01 m
to x = 0.50 m**, nearly the full arena width, and no closer fixed camera holds that. The consequence
is arithmetic: **≈ 17 screen-px per sim-metre** at 1280×720. **The entire geometric finding of stage 1
is a 0.758 m step, which is 13 px.** Legible if you know to look; not legible if you do not.

**Disposition:** the clip ships on that lens, and the **annotated still set is the magnifier**. The
stills are cut from **the delivered clip's own frames** — no second render, no second camera pose to
reconcile, no way for the still and the clip to disagree about what happened. Crop windows are placed
by a ground-plane homography fitted to the scene's own printed corner audit, not by eye.

**Not fixed, and named as owed:** a tracking or auto-framing camera would answer this properly. A
moving camera is a change to the "single fixed camera per clip" rule this seam has held since WR1,
and that rule change is not mine to make unilaterally.

### GAP 2 — ⚑ A PROJECTION LIE, CAUGHT BY DRAWING TWO SHAPES THAT HAD TO COINCIDE

`_audit_framing()` reports normalised coordinates from `Camera3D.unproject_position()`, which returns
**screen** coordinates — origin top-left, **y DOWN**. The still-maker's first homography flipped y,
on the assumption of a bottom-up convention.

**It still looked right.** The arena is a near-symmetric diamond under this bearing, so mirroring
about the frame's centre-line produced a 12 m ring that sat plausibly over the scene's own nova disc
on a downsampled view. It was caught **only** by drawing a **2.5 m ring next to the scene's own 2.5 m
commit disc** and finding them **114 px apart**. Two shapes that must coincide are the only honest
test of a projection; a shape that merely *looks* about right is not a test at all.

Same family as WR2 §5.2 (two floaters collapsing to one on screen) and WR2 §4(3) (tangent capsules
reading as interpenetrating): **the data was right and the frame said otherwise.**

### GAP 3 — INFO — the harness had a hidden interpreter dependency

`wr3_stills.py` originally used `numpy` for one 8×8 solve. This machine has **four** `python3` on
PATH and only two carry numpy — the tool worked from one shell and died from another. The dependency
was replaced with plain Gaussian elimination. **Pillow is still required** and the script now names
the exact interpreter that has it rather than failing with a bare `ModuleNotFoundError`.

### NO HALT WAS NEEDED

The replica traces consumed cleanly: `parse_errors = 0` on both roots, all five record types and all
five event kinds present and dispatched, both schema strings quoted on the frame. **The WR3 schema is
unchanged** — the build report's §2 statement that no `MIGRATION.md` entry is owed for stage 1 is
confirmed from the consumer side. **Both WR2 batteries were re-probed after the registry change and
reproduce their banked numbers unchanged** (`414.80 → 2 × 207.40` at t = 3.3536 on `after`, at
t = 1.9512 on `before`, 0 quantum violations).

---

## §6 — SMOKE GATE

Headless `--probe` on **all four** batteries. The WR3 probe re-proves the three verbs off the trace
with no renderer running, and its numbers are re-derived independently in GDScript from the ones
`wr3_pick_scan.py` computes in Python:

```
[wr3probe] battery=wr3_after  armed=true  boss=boss&quest_slith_wightmirecave01_0
[wr3probe] (a) KITE  — {"evade:commit":315,"evade:pressure":46,"evade:tg":18}
[wr3probe] (b) COMMIT/WHIFF — lock shapes {"w4/s1/r2":55} ; strikes 55, whiffed 53, landed 2
[wr3probe]     C_reach 2.50 m separates them: max LAND sep 2.2591, min WHIFF sep 2.6813 -> true
[wr3probe] (c) RING — mint t=0.70 fire t=3.0188  player r=12.221 m / footprint 12.00 m -> OUTSIDE
[wr3probe]            mint t=11.30 fire t=13.6188 player r=11.011 m / footprint 12.00 m -> INSIDE
[wr3probe] ⚑ NO `ai_state` field exists in this schema (W-1, post-stage-1). None is drawn.

[wr3probe] battery=wr3_before armed=false
[wr3probe] (a) KITE  — NONE — the arm is dark on this battery
[wr3probe] (b) COMMIT/WHIFF — lock shapes {} ; strikes 0, whiffed 0, landed 0
[wr3probe] (c) RING — mint t=0.70 fire t=3.0188  player r=5.707 m / footprint 12.00 m -> INSIDE
```

**Regression, WR2 `after` / `before`:** `parse_errors = 0`, crossings decompose exactly, **0 quantum
violations**, engine pins `f1ab3b09` on both, `armed=false` on both — the WR3 layer is inert on the
WR2 batteries, as it must be.

---

## §7 — WHAT MATT SHOULD BE ABLE TO TELL ME AFTER WATCHING

Not pre-answered. Four things to disbelieve if they look wrong:

1. **The AFTER fight is a WIN, at 95 seconds.** The BEFORE fight, same seed, is a **loss at 37**.
   Build report §F-4 records that stage 1's own prediction said the boss win rate would *fall or
   hold at 0.00* and it went to **1.00 for the player, 66 of 66**. **The prediction is refuted, and
   the refutation is what the clip shows.** If that reads as the render doing something rather than
   the sim doing something, say so.
2. **`sep 2.000 m / floor 2.00 m` sits on the BEFORE clock line for essentially the whole fight**,
   and the AFTER line moves between 2.000 and 6.157. That is the degenerate pin dying. It is the one
   thing G1(b) went 66/66 → 0/66 on.
3. **`WHIFF · x.xxx m > reach 2.50 m` fires 53 times in the AFTER clip and 0 times in the BEFORE.**
   The reach is the engine's own C_reach, verified against 3,096 strikes before it was drawn.
4. **From about 20 seconds in, the AFTER fight repeats.** Same windup separation, same strike
   separation, same whiff, every 1.5 s, for a minute. **That is the finding, not a stuck render.**

And one question that is his and not mine: **whether "the player has solved the boss's swing" is the
stage-1 result he wants to calibrate away from, or the geometry he wanted to see exist before anybody
touches a number.** The gates say the geometry exists. The clip says what it feels like.

---

*WR3-KITE-COMMIT stage-1 owner-eye render — drax, presentation seam, 2026-07-30.
`reincarnated-godot` committed at `72723ca`; NOT pushed. No engine path touched.*
