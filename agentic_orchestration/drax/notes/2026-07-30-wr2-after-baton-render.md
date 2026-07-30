# WR2-ENCGEO — THE AFTER-BATON RENDER (owner-eye #2)

> **Cell:** G-D2 of run **WR2-ENCGEO-2026-07-29**. **Agent:** drax. **Conductor:** gandalf.
> **Contract:** `agentic_orchestration/gandalf/notes/2026-07-30-wr2-grading-synthesis-after-baton.md`
> **PART 3 (§3.1–§3.8)**. Supersedes the WR1 baton clause-by-clause where geometry changed it;
> the WR1 baton stays CURRENT as the BEFORE-evidence contract. Nothing here edits a WR1 artifact.
> **Repo:** `reincarnated-godot` — **NOT PUSHED** (the conductor pushes).
> **Trace sets:** opened **READ-ONLY**, never written, nothing copied out, nothing regenerated.
> `git status` on the engine tree is clean on `wr2_battery_after/` at cell end; `wr2_battery_before/`
> shows its three `traces/` dirs as untracked exactly as **Gate-2 INFO-4** declares it should.

---

## §0 — ADR-004 ACKNOWLEDGEMENT (§3.8 / INFO-5 — the thing that was OWED AT THIS DELIVERY)

**drax acknowledges both MIGRATION entries against
`~/Games/reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`. Acknowledgement only;
nothing is owed to ship, and nothing was owed to ship.**

**1. `[2026-07-30] WR2-ENCGEO Cell D`** — read in full, including §5 and §6.
Acknowledged as consumed:
* `replica-frame/v1` gains **`header.entities[].movement_speed_ms`**, **CONDITIONAL** — present only
  when `nova_telegraph_v2` is armed. Consumed with `has()`, never positionally. **Verified on both
  batteries of the watch pick:** present on all four roster rows on the AFTER trace, **absent on all
  four** on the BEFORE trace. The roster panel prints `absent (nova_telegraph_v2 dark)` rather than a
  zero, because a missing conditional key and a zero speed are different statements.
* The nova telegraph's **duration changes 3.09×** (0.750 → 2.318840579710145 s), with the explicit
  warning that **a tell hard-coded to 0.750 s is wrong by 1.57 s**. See §3 — honored, and honored by
  *reading*, not by substituting one literal for another.
* The schema does **not** bump, correctly: the field is additive and conditional.
* §5's **name collision** is acknowledged and acted on: the trace field (per-entity, conditional) and
  the report field (player-only, unconditional) are **never joined** in this seam. The report field
  feeds the banner's player audit line; the trace field feeds the per-entity roster line. Two
  readers, two sites, no cross-join.

**2. `[2026-07-30] WR2-ENCGEO Cell BAT`** — read in full, including its own late-entry disclosure.
Acknowledged as consumed:
* **`report["presentation_units"]`** (unconditional block) — now the system of record for the nova
  unit payload. **This is the emission whose stated purpose is that my decomposer stops hard-coding
  207.40 / 235.40, and as of this cell it does.** See §2.
* **`fights[].movement_speed_ms`** + **`movement_speed_provenance`** — read as a pair. The magnitude
  never appears on the frame without its grade beside it, because the grade is
  `engine-default-ungraded` and that is the whole finding.
* **`fights[].a_dmg1.nova_per_projectile_hp`** — consumed as the **preferred** source (per-fight
  beats per-leg for a renderer drawing one fight), with the per-leg block as fallback.
* §3's two named traps are both honored: the unit is **not** `telegraph.damage_amount` (§4), and
  `n_nova_crossings: 0` with an empty list is read as **no crossing happened**, never as a skipped
  emission.

---

## §1 — THE DELIVERABLES

All under `/Users/admin/Games/reincarnated-godot/tmp/wr2/`. 1280×720 · 30 fps · 1× real time ·
single fixed camera per clip · no cut, no speed-up, no edit.

| # | file | what it is |
|---|---|---|
| **1** | `wr2_after_pre_boss_B_74000802.mp4` | **THE WATCH.** AFTER, `pre` leg, boss, arm **B**, seed **74000802** — the §3.7 pick |
| **2** | `wr2_before_pre_boss_B_74000802.mp4` | its **BEFORE twin**, same seed / leg / tier / arm, **same camera** |
| **3** | `wr2_sidebyside_B_74000802.mp4` | (1) and (2) **hstacked**, BEFORE left / AFTER right, one timeline |
| **4** | `wr2_after_ownereye1cam_B_74000802.mp4` | AFTER under the **literal owner-eye #1 camera pose**, byte-identical — see §5, it does not hold the fight |
| **5** | `wr2_after_pre_boss_B_74000803.mp4` | the optional §3.7-caution-3 pick: the **1× → 2× catastrophic flip** |

**The fight, and why this one** (§3.7, and the reason is measured):
`pre` (`R2_proxy`, cold 0.14) · `boss` · arm **B** · seed **74000802** ·
`fight_key KC1-2026-07-27/boss/B/74000802`.

| property | BEFORE | AFTER | why it earns the pick |
|---|---|---|---|
| duration | **37.1 s** | **37.0 s** | ⚑ **duration-INVARIANT** — the geometry finding is isolated from the pacing finding |
| winner | `monster` | `monster` | **it is a loss, and it was a loss before too. That is not a bug** |
| nova crossing | 414.80 @ t = 1.9512 | 414.80 @ t = **3.3536** | later, from a moved origin |
| player path length | **36.14 m** | **185.13 m** | **5.1×** |
| cumulative heading change | **4.97 rad** | **64.98 rad** | drift becomes orbit |
| player x range | [0.500, 22.793] | [17.618, **35.500**] | SW quadrant becomes east-wall orbit |
| min player↔boss centre sep | **1.554864 m** | **2.000000 m** | the repair, exactly at the floor |

Every figure in that table is measured by this seam off the traces, not transcribed.

---

## §2 — THE HARD-CODES ARE RETIRED. This was the point of the swap-in.

**Retired, at `scripts/wr2_traceset.gd`:** the `LEGS` table's `unit_payload_hp: 207.40 / 235.40`
literals are **gone**. There is no `unit_payload_for()` any more. In their place,
`resolve_units(leg_key, tier, arm, seed)` **reads the leg report**:

```
1. fights[row].a_dmg1.nova_per_projectile_hp     (PER-FIGHT — preferred)
2. presentation_units.nova_unit_payload_hp.values_observed   (PER-LEG — fallback)
```

**Proved on the watch pick, both batteries** (headless `--probe`):

```
[wr2] unit payload: 207.4000 HP  <- fights[].a_dmg1.nova_per_projectile_hp (PER-FIGHT, emitted)
[wr2probe] crossing t=3.3536 delivered=414.80 -> 2 x 207.40 exact=true in{1,2}=true
[wr2probe] quantum violations: 0
```

**The provenance string is printed ON THE FRAME**, not just in a log. A frame that cannot say where
its divisor came from cannot be audited, and until today the answer would have been "a GDScript
file in the presentation repo".

**Design choices worth recording, because each one could have been made lazily:**
* A **non-constant** set at either level leaves the unit `NAN` and the renderer draws **one
  undecomposed floater and says so**. It does **not** average the set and does **not** take `modal`
  to obtain a number. An averaged unit draws a projectile count the sim never realized — which is
  precisely the render lie this emission exists to stop. `constant: false` is a finding, not an
  inconvenience.
* A missing `presentation_units` block is reported **by name** as a possible pre-`21abff12` baseline,
  not as a missing crossing. Different causes must not produce the same message.
* The engine pin is read off **`header.engine_git_hash`** and cross-checked against the registry
  literal (`f1ab3b09`), so a mismatch is visible on the frame. Both traces and both reports read
  `f1ab3b09`. The registry literal is a **cross-check**, never the displayed value.
* The leg's `mitigation_regime_m1` is cross-checked against the registry's own label, so a
  mis-registered leg dir cannot ship a correct number under a wrong name.
* **Longest-key-first leg resolution.** The BEFORE dir names are strict *prefixes* of the AFTER ones
  (`..._tg_dec` vs `..._tg_dec_bsep_mv2_ntv2`). A shortest-first scan resolves **every** AFTER path
  to the BEFORE leg — right numbers under the wrong battery's label, silently. Caught before it shipped.

**Also retired — five nova depiction constants**, all of which had moved:
`NOVA_ORIGIN_X/Y` (25.917083, 15.094333 → the origin **moved 0.402 m NE** to 26.158596, 15.416323),
`NOVA_WINDUP_S` 0.75, `NOVA_FIRE_T_S` 1.55, `NOVA_TELEGRAPH_T_S` 0.80, `NOVA_CROSS_T_S` 1.9512.
`NOVA_RADIUS_M` 12.0 is **unchanged** and was retired anyway — a value that happens to agree is not
a licence to hold it. `_last_nova_origin` initialises to **NAN**, not to the old literal: a crossing
that arrives with no telegraph origin now degrades to a vertical-only floater stack and warns,
instead of drawing the ring's radial off a point the sim retired.

`MODAL_SEPARATION_M` 1.600 is retired as an AFTER descriptor per §3.4(3) and replaced by the
combined-radii floor. The 5.617 m native standoff remains retired and unused.

---

## §3 — THE TELL: 2.32 s, HONORED, AND HONORED BY READING

`_spawn_telegraph()` computes the tell's life as `fire_t_s - t_s` off the record, so this scene was
duration-correct **by construction** and never held 0.750 s. What this cell added is that the number
is now **surfaced and cross-checked** rather than merely consumed — because a value that happens to
be right is not the same as one that is read on purpose.

Read off the AFTER watch pick, printed on stdout and on the frame:

```
[wr2] nova telegraph: tick 7 t=0.7000 wind_up_s=2.318840580 fire_t_s=3.0188
      radius_m=12.00 origin=(26.158596, 15.416323) announced=218.0759
```

and off the BEFORE twin: `tick 8 t=0.8000 wind_up_s=0.750 fire_t_s=1.5500 origin=(25.917083,
15.094333) announced=241.3655`. **3.09×, exactly as the entry states.**

The banner carries the tell **with the grade of its input**, because §3.3's caveat is the point:

```
nova tell 2.3188 s (read off telegraph.wind_up_s) · v=5.750 m/s [engine-default-ungraded] · frac 0.9
```

**Nothing in this seam holds 2.3188 s.** It is default-specific: the escape law's one free input is
`v = 5.75 m/s`, an engine literal filling an absent kit field, provenance `engine-default-ungraded`
on 900/900 fights, neither M nor D graded. A kit that declares `movement_speed` moves it, and the
frame will say so without a code change.

`telegraph.damage_amount` is now labelled **`announced`** on the frame (§3.6 A3), and excluded from
the decomposition. On the pick the nova **announces 218.076** and the crossing **delivers 414.80**.

---

## §4 — THE CONSUMER NOTES THAT CHANGED, AS BUILT

**(3) Separation — the repair is the most visible geometric change, and it nearly did not survive
the projection.** Measured independently by this seam on the watch pick, from the traces:

| | AFTER | BEFORE |
|---|---|---|
| floor (r_player 0.5 + r_boss 1.5) | 2.0 m | 2.0 m |
| min centre separation | **2.000000 m** | **1.554864 m** |
| ticks below floor | **0 of 369** | **350 of 370** |
| worst overlap | **0.0000 mm** | **445.1357 mm** |

That reproduces §3.4(3) exactly — bodies no longer overlap, anywhere, at any tick — and the BEFORE
figure lands on the WR1 baton's retired "0.40 m interpenetration" note.

**⚑ And a rendered frame caught that the depiction argued the opposite.** At a 41° depression the
boss's r = 1.5 m capsule **mesh** occludes a player standing *exactly tangent* to it, so the AFTER
frame *looked* like the interpenetration this run repaired. The footprint rings carry the truth
(tangent, not crossing) but a ring pair is a judgement call at this stand-off, and a judgement call
is not evidence. **So the number went on the frame:**
`sep 2.000 m / floor 2.00 m (no overlap)`, live, per tick, with a `⚑ OVERLAP nnn mm` arm that the
BEFORE clip exercises for 350 of its 370 ticks. It is a distance between two trace-authored
positions minus two header radii — read and subtracted, nothing simulated.
Same correction family as §5.2/§5.3 at owner-eye #1: the data was right and the frame did not say so.

**Playback collision stays OFF**, ruling unchanged, and for the reason it was always right rather
than the reason WR1 gave: transforms are **authored by the trace** and never solved.

**(4) Arena 1:1 stands; the corner-pin note is gone.** The player never reaches (0.5, 0.5) on these
traces. The wall faces are still dressed — a boundary touched 2.722 % of the time is still a
boundary, and the player does reach **x = 35.5 m**, i.e. the east wall, on this pick. The `ROOM_EDGE`
37.5 m vs 36.0 m item from WR1 is **unchanged and still open**: it is dressing trim outside the clear
interior, and it is hereby *declared* as such rather than left implied. Ambient coverage at 37.5 m
still owed.

**(5) The nova — later, bigger, moved.** Origin re-read from the record every firing. The 12.0 m disc
is drawn **unclipped**, so the now-**2.16 m** east overrun reproduces by construction and the wall
face visibly crosses it. Trimming it would draw a footprint the sim never had.

**(8) `intent` grew a fourth value and the aim-line is LIVE.** The WR1 `decision` channel was
schema-ready and dark; it now carries one event per tick. **It lit up with no code change, exactly as
WR1 §6.3 predicted — but only because the match carried a default arm.** Measured:

| | AFTER | BEFORE |
|---|---|---|
| tick records / `decision` events | 370 / **370** | 371 / **371** |
| intents | `{reposition: 341, advance: 16, hold: 13}` | `{hold: 355, advance: 16}` |

`reposition` is **92 %** of AFTER ticks. **Without the default arm, an exhaustive three-value match
would have painted 92 % of the fight in the wrong colour and never errored.** It now has its own
colour, and **the default arm stays for the fifth value**. `evade` is still zero (M-3 dark by charter
design) and its arm stays: absence is data. `decision` moved from the coverage ledger's *stub*
column to its *drawn* column.

**The unchanged notes were re-read, not re-derived** (§3.5): per-crossing bucketing, `element` as a
skill label only, the structural received-side crit zero, four-valued `hp_provenance` with `D-HELD`
never folding into `D`, spawn-from-header. `leech` remains a counted, undrawn stub per §3.6 A1.
Corpses remain carried at last-known position per A4.

---

## §5 — ⚑ FLAGS. Read these; two of them contradict something on record.

### FLAG 1 — §3.7 caution 3 is WRONG about the watch pick, and it contradicts §3.6 A3 of the same document.

> §3.7 caution 3: *"Its nova quantum stayed 1× — a single 207.40 floater."*

**Measured on `pre/boss__B__seed74000802`: the crossing delivers `414.80 = 2 × 207.40`. It is a 2×
crossing — on BOTH arms, and in BOTH batteries.** §3.6 A3 of the same baton states this outright
(*"the nova telegraph announces 218.076 while the crossing delivers 414.80 = 2 × 207.40"*), so the
document disagrees with itself and the traces side with §3.6. **Not reconciled silently** per the
dispatch's standing instruction.

**Consequence is favourable and worth stating plainly:** the deliverable pick **already exercises the
now-majority 2× decomposition**, so the render Matt watches does the job caution 3 said it would not,
and no substitution was needed.

Where caution 3 **is** right, verified: `pre/boss__B__seed74000803` genuinely flips
**1× (BEFORE: 207.40, `player` win at 65.3 s) → 2× (AFTER: 414.80, `monster` win at 34.3 s)**. It is
rendered as deliverable #5.

### FLAG 2 — the "same camera" instruction and a watchable render are not simultaneously satisfiable, and the baton predicted it.

§3.4(4) warns that *"a camera tuned to a static corner stand-off will lose the fight."* **Measured,
not accepted on assurance:** `_audit_framing()` projects every player tick through the actual
`Camera3D`. Under **owner-eye #1's exact pose** the player reaches **normalised screen y = 1.300** —
**30 % of a frame-height below the bottom edge** — and the arena's NE corner projects to **1.807**.
`Camera3D.fov` is *vertical* under `keep_height`, so this is **resolution-independent**: not a
headless artefact, and it does not go away at 1280×720. Cause is exactly as predicted — owner-eye
#1's aim is biased 3 m toward the SW corner because 179/180 WR1 fights resolved there, and the AFTER
player orbits out to the **east** wall, the near side under this bearing, i.e. the bottom of frame.

**Disposition — both, rather than a choice made quietly:**
* **`--cam arena_full`** carries the watch and the BEFORE/AFTER pair. **Same bearing (yaw 47°), same
  pitch (−41°), same FOV (40°)** — the lens is unchanged, which is what keeps the pair
  apples-to-apples. Only the aim (arena centre, +7 m along the NE diagonal) and the stand-off
  (43 → 58 m) move. Both values were **swept against the audit**, not chosen by eye: at 58/7 the
  worst normalised player margin is **+0.256** and all four arena corners clear the frame by
  **+0.139**.
* **Deliverable #4** is the AFTER fight under the **byte-identical owner-eye #1 pose**, so continuity
  with the first watch is not lost — it is simply not asked to do a job it measurably cannot do.

**Matt's call to make, not mine:** whether the apples-to-apples pair (#3) or the literal same-lens
clip (#4) is the one that answers his question.

### FLAG 3 — the point-shape telegraphs disagree with themselves, and the baton's §3.3 note reads past it.

§3.3 says *"Non-non nova telegraphs (the point-shape mob melees) still carry `wind_up_s: 0.5`"* —
true as a field read. But on those events **`fire_tick == tick` and `fire_t_s == t_s`**, i.e. the
attack resolves on the tick it is announced. So `wind_up_s: 0.5` and `fire_t_s − t_s = 0.0` are two
fields stating different things about the same melee. **A renderer that draws the tell from
`wind_up_s` draws half a second of wind-up the fight did not have.** `fire_t_s` / `fire_tick`
governs here, because that is the field the sim's own resolution used; the disagreement is reported
once per run and **not split**. Same discipline as the still-open `range_m: 10.0` vs
`radius_m: 12.0` mismatch. **Nothing is owed on this for the watch** — it does not touch the nova,
which is internally consistent to nine decimal places (2.318840579710145 = 3.0188405797101447 − 0.7).

### FLAG 4 — INFO — `delivered_unclamped` is `null` on crossing events, so the unit's definition is not recoverable from a trace.

`presentation_units.nova_unit_payload_hp.definition` reads
`delivered_unclamped / realized_count`, and **neither operand exists on the trace**:
`realized_count` appears in 0 of 450 files (known) and `delivered_unclamped` is `null` on the
crossing event (measured here). **That is not a defect — it is what makes the emission load-bearing
rather than convenient**, and it removes any path by which a stale reader could "recompute" the unit
and drift. Recorded so nobody later reads the definition as a trace-side recipe.

### FLAG 5 — INFO — two of §3.4(4)'s quoted figures are seed-74000800 figures, and one uses a different accumulator than mine.

§3.4(4) quotes *"path length 34.70 → 340.96 m"* and *"cumulative heading change 150.80 rad"* on
`pre/boss__B__seed74000800`. **Path reproduces exactly** here: 34.70 → 340.96 m on that seed.
**Heading does not:** my wrap-normalised (shortest-arc) accumulator reads **4.63 → 125.44 rad** on
that seed against the baton's 3.84 → 150.80, which is the signature of a raw-`|Δ|` accumulator.
Not a substantive disagreement and not a defect in either — **but I quote my own number for my own
pick (4.97 → 64.98 rad) and have not adopted 150.80**, because two accumulators over one field are
exactly how a figure nobody re-measures becomes a premise.

### FLAG 6 — INFO — the BEFORE battery is untracked and I did not bank it.

Per §3.1 / Gate-2 INFO-4 the 450 BEFORE traces are **untracked**; a `git clean` in the engine tree
would take them, and deliverable #2 depends on them. **I did not copy them out and did not
regenerate them** — copying engine evidence into the presentation repo makes a second system of
record, and regeneration is not this seam's to do. They were opened read-only in place. **The
banking call is the conductor's**, per §3.1's own offer. The BEFORE clip's banner declares its
battery untracked on every frame.

---

## §6 — WHAT MATT SHOULD BE ABLE TO TELL ME AFTER WATCHING

The §3.7 question, re-pointed and not pre-answered: whether **the orbit, the non-overlapping bodies,
the 2.32 s telegraph and the later, bigger nova** read as **the fight he played** or as **a renderer
doing something else**. Three specific things to disbelieve if they look wrong:

1. **The fight is a loss at ~37 s.** It was a loss before too, at 37.1 s. Duration-invariance is why
   this seed was picked — same length, unrecognisable geometry.
2. **`sep 2.000 m / floor 2.00 m (no overlap)`** sits on the clock line for the whole AFTER clip.
   If the capsules still *look* interlocked, that is the 41° projection, and the number is the
   authority. The BEFORE clip shows `⚑ OVERLAP` up to 445 mm for 350 of its 370 ticks — that is the
   contrast.
3. **The two `207` floaters** on one crossing are one ring delivering **two** projectiles, not one
   hit of 414.80 and not a duplicated label.

And one question that is his and not mine: **which camera** (§5 FLAG 2).

---

## §7 — FILES TOUCHED (all in `reincarnated-godot`, none in the engine)

| file | state | what changed |
|---|---|---|
| `scripts/wr2_traceset.gd` | **rewritten** | two batteries, six legs; **the hard-coded unit payload replaced by `resolve_units()` reading the leg report**; five nova depiction constants retired; longest-key-first leg resolution |
| `scripts/wr2_playback.gd` | **modified** | `--battery` / `--cam arena_full` / `--camdist` / `--camaim`; unit provenance on the frame; tell + `v` + grade on the frame; `announced` label; `reposition` intent arm; `decision` ledgered as drawn; NAN nova origin; **`_audit_framing()`**; **the separation readout**; paired-floater lift |
| `scripts/run_wr2_playback.sh` | **modified** | battery arg, the §3.7 watch pick as the default, frame budget for a 37 s fight |

Smoke gate: headless `--probe` clean on **both** batteries — `parse_errors = 0`, all five record
types and all five event kinds consumed, decomposition exact, **0 quantum violations**.
