# WR3-KITE-COMMIT — THE STAGE-2-CLOSE OWNER-EYE RENDER (owner-eye #4)

> **Cell:** owner-eye #4 of run **WR3-KITE-COMMIT** — the last gate before stage 2 closes.
> **Agent:** drax (presentation seam). **Conductor:** gandalf (`RUN-CONDUCTOR`).
> **Consumed:** `agentic_orchestration/gamora/notes/2026-07-30-wr3-anchor-refit-report.md` (engine
> `9c978b1e`) · `2026-07-30-wr3-w1-schema-amendment.md` · `reincarnated-engine/src/reincarnated/
> simulation/MIGRATION.md` head entry (ANCHOR-REFIT) · my own owner-eye #3 note.
> **Repo:** `reincarnated-godot`, **NOT PUSHED** (the conductor pushes). No engine path written.
> **Gate-2 (jack-ryan) passed 2026-07-31 with 0 BLOCK.** This render is the remaining gate.

---

## ⚑ THE FRAMING SENTENCE — read this before the link

> **This is a PARITY watch, not a band watch: per Matt's R-WR3-36 ruling (c), this cell is the
> verification anchor — acceptance is that the engine reproduces the referent's own arithmetic
> (H1 1.000, residual −0.9%), and NO band verdict exists on this cell by design. The [0.40, 0.60]
> design band detached to a future RDR design lap. Watch for: the melee's physical+cold composition
> landing, the blizzard and nova as distinct verbs, and the overall fight reading as the referent
> fight.**

**That sentence is also on every frame of the clip**, in the banner, because a watch that does not
say what it is a watch OF gets read against whatever criterion the viewer last heard, and the
picture is what travels.

---

## §1 — THE LINK

**THE WATCH:**
`/Users/admin/Games/reincarnated-godot/tmp/wr3anchor/clips/WR3ANCHOR_sidebyside_74000802.mp4`

2560×720 · 30 fps · **1× real time** · single fixed camera (`arena_full`, the pose owner-eye #2 and
#3 shipped on) · **BEFORE left / ANCHOR right** · 83.2 s · 16 MB.

| # | file | what it is |
|---|---|---|
| **1** | `/Users/admin/Games/reincarnated-godot/tmp/wr3anchor/clips/WR3ANCHOR_sidebyside_74000802.mp4` | **THE WATCH.** hstack, one timeline |
| 2 | `/Users/admin/Games/reincarnated-godot/tmp/wr3anchor/clips/WR3ANCHOR_split_74000802.mp4` | the **ANCHOR** alone — 2,473 frames, **82.43 s**, 12 MB |
| 3 | `/Users/admin/Games/reincarnated-godot/tmp/wr3anchor/clips/WR3ANCHOR_dark_74000802.mp4` | its **seed-matched DARK twin** — 1,535 frames, **51.17 s**, 7 MB |
| 4 | `/Users/admin/Games/reincarnated-godot/tmp/wr3anchor/stills/` | seven stills cut from the delivered clips' own frames |

**⚑ One disclosed edit, and it is only in (1).** The DARK fight ends at 51.2 s and the ANCHOR fight
at 82.5 s. To hstack them on one timeline the DARK side **holds its final frame** (`tpad`
`stop_mode=clone`) for the remaining 32 s. Nothing is sped up, nothing is trimmed, both halves carry
their own full provenance banner. Clips (2) and (3) are untouched.

**The still that is the whole cell** — `stills/C_melee_pair_t5.80.png`, both halves at **the same
tick, t = 5.80 s, the first boss melee landing of each fight**:

```
ANCHOR   MELEE LANDED t=5.80 s  element `physical`  delivered 18.62
         DECLARED (roster `_kc1_meta.melee_channel_split`): physical 38.699 + cold 11.301
                                                          = 50.0 pre-mit   share 0.7740
         ⚑ 45.6 % of that 18.62 is the COLD RIDER — DERIVED from 0.30·phys + 0.86·cold,
           because NO FIELD IN THE TRACE CARRIES IT

DARK     MELEE LANDED t=5.80 s  element `cold`      delivered 39.15
         roster declares NO `melee_channel_split` — this is the 100 % COLD melee,
         one channel, whole magnitude
```

Stills: `A_split_melee_t5.80` · `B_dark_melee_t5.80` · `C_melee_pair_t5.80` ·
`D_nova_ring_t4.20` (the 12 m star, named NOVA on the clock line) ·
`E_blizzard_storm_t14.10` (the 8 m storm, named BLIZZARD) · `F_ward_up_t0.20` ·
`G_anchor_win_t82.3` · `H_dark_death_t51.2`.

**Machinery** (`reincarnated-godot`): `scripts/wr3_anchor_trace.py` (new) ·
`scripts/wr3_anchor_pick.py` (new) · `scripts/wr2_traceset.gd` · `scripts/wr2_playback.gd` ·
`scripts/run_wr2_playback.sh`.

---

## §2 — ⚑ THERE WAS NO TRACE OF THE ANCHOR, ANYWHERE, AND I DID NOT EDIT THE ENGINE TO GET ONE

The commission says "run the anchor-refit cell / replica frame emitter READ-ONLY to produce a fresh
trace if needed." It is stronger than "if needed": **the anchor has no trace and cannot have one
through any existing path.**

1. `wr3_cell_refit_2026_07_30.py` attaches `_ReceivedSink`, whose `tick()` is `pass`. It writes no
   frames. Its output root holds one JSON artifact and no `traces/` directory.
2. `kitcal_g5_harness.drive()` — the only thing in the tree that writes replica traces — **has no
   `wr3_melee_split_v1` parameter at all**. There is no argv that makes it emit a split-armed fight.

So `scripts/wr3_anchor_trace.py` reproduces the cell's own `_run(split=True)` **character for
character** out of its source and swaps the sink for a `G5TraceSink`. Everything lands in this
repo's `tmp/`. The engine tree was never opened for write (`git status` under
`reincarnated-engine/src/` shows no modification at cell end).

**The reproduction is PROVEN on three axes, not asserted:**

| claim | measured |
|---|---|
| the anchor's own figures | H1 **1.0000** · intake **384.0105** · duration **36.1067 s** · **30/30** wins |
| the FROZEN artifact of record | H1 1.000 · intake 384.011 · 36.107 s |
| the DARK twin (`split=False`) | H1 **0.9667** · intake **426.6461** · **34.7500 s** — the refit report §3.1 before-column, **digit for digit** |
| sink byte-neutrality | seed-matched no-sink leg: H1 / intake / duration / per-seed vector **identical** |
| `trace_decisions` non-perturbation | both sets written, `decision` records stripped, **13,573 / 13,573 records byte-identical**, outcome identical on 30/30 |

**⚑ `trace_decisions` had to be armed and it is NOT part of the anchor arm.** The cell does not
pass it, so the anchor's own traces carry **zero** `decision` records — measured, 0 evade ticks on
30/30 — and the kite has no aim-line data at all. It is a pure emission gate (`if
self._trace_decisions:` guards two appends), but "it's emission-only" is exactly the claim this run
has been burned by three times, so it is proven record-for-record above rather than inspected.

**Three fixture facts I measured rather than assumed, because they are NOT the melee split and a
viewer could mistake them for it:** the cell does not pass
`apply_mob_hp_difficulty_multiplier` (so the anchor runs the engine default `True`, while
`run_one_fight` passes `False`); it does not wrap in `effect_name_policy_scope("strict")` (the
harness does); and its `session_id` / `season_id` differ from the harness's. The driver reproduces
**the anchor**, so it matches the cell on all three. Boss `max_hp` reads **14812.0**, the same as
the stage-1 s11 header.

---

## §3 — THE FIGHT, AND WHY IT IS THIS ONE (MEASURED, NOT EYEBALLED)

`wr3_anchor_pick.py` scores all 30 anchor fights on the four things this close is watched for
(melee composition · both circle families firing · the ward visible · `attack_id` on damage) plus
the three stage-1 verbs. **14 of 30 carry both circle families AND ≥ 2 melee landings AND the ward.**

**SELECTED: seed 74000802.** And the reason is not that it scores well — seed 74000817 scores
higher on the composite. It is this:

> **⚑ 74000802 IS THE ONE SEED IN THIRTY WHOSE OUTCOME THE MELEE RE-SPLIT MOVES.** The refit report
> §3.1 records the per-seed win vector going **29/30 → 30/30, "loss on seed +2"**. Seed +2 is
> **74000802**. And 74000802 is the seed Matt has already watched **twice** — as the WR2 AFTER clip
> at owner-eye #2, and as *both* the BEFORE and the AFTER at owner-eye #3.

So the fourth cell on the same seed is the one where the change **decides the fight**:

| | DARK (100 % cold) | ANCHOR (referent split) |
|---|---|---|
| winner / duration | **`monster`** / **51.17 s** | **`player`** / **82.43 s** |
| boss melee landings | 20 | **37** |
| melee element | `cold` | **`physical`** |
| melee delivered, mean | **40.833** (11.667 … 50.995) | **21.650** (18.621 … 24.761) |
| commit episodes / strikes | 24 / 24 | 42 / 41 |
| landed / whiffed | 20 / 4 | 37 / 4 |
| telegraph families | nova 2 · blizzard 1 · wave 1 | nova 2 · blizzard 1 · wave 1 |
| `wr3_icearmor` entity-ticks | 120 | 120 |
| separation median / max | 2.249 / 17.061 m | 2.279 / 17.061 m |

**The verbs were verified to fire before rendering**, headlessly, off the file, by the scene's own
`--probe` — the discipline that caught the nova-free fallback at owner-eye #3:

```
[wr3probe] (b) COMMIT/WHIFF — lock shapes {"w2":1,"w5/s1/r9":41} ; strikes 41, whiffed 4, landed 37
[wr3probe]     C_reach 2.50 m separates them: max LAND sep 2.4097, min WHIFF sep 2.5714 -> true
[wr3probe] (c) CIRCLE TELEGRAPHS — firings and the footprint verdict, BY FAMILY:
[wr3probe]     NOVA      mint t=3.60  fire t=4.4500   player r=5.478 m / footprint 12.00 m -> INSIDE
[wr3probe]     BLIZZARD  mint t=13.50 fire t=14.3333  player r=2.520 m / footprint  8.00 m -> INSIDE
[wr3probe]     NOVA      mint t=17.20 fire t=18.0500  player r=5.162 m / footprint 12.00 m -> INSIDE
[wr3probe/s2] (2) MELEE — 37 landings, elements {"physical":37}, delivered 18.6205..24.7610 mean 21.6501
[wr3probe/s2] (3) records carrying a `family` KEY: 0 / 4  ⚑ DROPPED AT THE EMISSION BOUNDARY
[wr3probe/s2] (4) ICEARMOR WARD — `wr3_icearmor` on 120 entity-ticks
```

**The melee mean cross-validates the cell.** My consumer-side 30-fight measurement is **21.344**
(91 landings, 18.067 … 24.761). The cell's own §1.3 probe predicts **21.3285** and measures
**21.1317**. And my measured range sits **inside** the referent band `[17.13, 27.90]`. The dark
twin's **42.247** reproduces the report's 42.4205. Two independent instruments, one number.

**And the telegraph counts reproduce gamora's counters exactly.** Over 30 anchor fights I count
**wave 77 · blizzard 60 · nova 67** telegraphs; the refit report §3.1 records `wave_casts 77`,
`blizzard_casts 60`. Not transcribed — measured from the other side of the seam.

---

## §4 — ⚑ FINDINGS. Four of these disagree with something on record.

### FINDING 1 — ⚑⚑ **`TelegraphSpec.family` IS MINTED AND THEN DROPPED AT THE EMISSION BOUNDARY.** BLOCK-class for any consumer told to key on it.

The commission says: *"`TelegraphSpec.family` ∈ {nova, blizzard, wave, melee} now rides telegraph
events … your playback consumer should key on `family`."*

**It does not ride telegraph events.** `spatial_telemetry.py:223` declares the field;
`spatial_engine.py` sets it at three mint sites (`:5431` nova, `:6439` wave, `:6578` blizzard);
`replica_frame_emitter.py:497-544` then builds the telegraph record **key by key** and never copies
`family` across.

**MEASURED: the string `family` occurs in 0 of 13,573 records across the 30 anchor traces, and in 0
records of the 30 dark traces.**

This is the **same defect shape the field was added to close, one layer out** — and it is the shape
the emitter's own `attack_id` comment names in bold: *"the discriminator existed and was **LOST AT
THE SEAM**."* That comment counts three instances and calls them a pattern. **This is the fourth,
and it is inside the repair.**

**What this seam did instead, and why it is not a workaround.** My TELL-DRESS cell (2026-07-31) had
already built the ladder for exactly this: `(a)` the `family` rider → `(b)` the `attack_id`
`:mechanic:` substring sniff → `(c)` shape, which **refuses** to promote a bare circle → `(d)` a
loud UNKNOWN fallback decal. Rung (a) is dead; rung **(b)** — which that cell said out loud was *a
SUBSTRING SNIFF, not a field* — is carrying the whole discriminator, and it is the same substring
the engine's own analyser sniffs (`wr3_cell_kc_2026_07_30.py:551`). **The render is correct. The
contract is not.** The frame says so, by name, on every frame.

**THE SIZE OF WHAT RUNG (b) IS HOLDING UP, measured on the anchor:**

```
circle-shaped telegraphs .................. 127
  of which family `nova`   (the 12 m star)   67
  of which family `blizzard` (the 8 m storm) 60      = 47.2 %
```

**And one precision that is owed in the other direction.** The stage-2c report §7 audit says *"the
drax-seam playback consumer had that defect."* True as a **latent** statement; **false about the
stage-1 owner-eye numbers.** Measured on the frozen s11 battery: **114 nova circles, 0 blizzard
circles**, across all 66 boss traces. `circle` had exactly one producer at stage 1, so my
shape-test was correct on the data it ran against. It became a defect at stage 2b, and it was
closed at TELL-DRESS before this cell opened. Also worth stating: on **this** battery the escape
statistic it would corrupt is **0 under both tests** (0 of 67 rings escaped), so the defect does not
*bite* here — it is live, and it bites on any battery where a ring is cleared.

**The ask, routed not ruled:** one line in `ReplicaFrameSink.telegraph()`. Until it lands, every
consumer of this schema is discriminating mechanisms by substring.

---

### FINDING 2 — ⚑ **MIGRATION §2(1) IS FALSE AT THE EMISSION BOUNDARY, AND ACTING ON IT WOULD HALVE THE BOSS'S MELEE ON SCREEN.**

The ANCHOR-REFIT MIGRATION entry §2 states two consumer consequences that read as contradictory:

> **§2(1)** *"Per-swing damage-event **COUNT DOUBLES** on the boss melee. Any consumer counting boss
> melee events as swings will double-count."*
> **§2(2)** *"The engine still emits **ONE** `on_hit` per swing, carrying the SUMMED post-mitigation
> `delivered`."*

**MEASURED, 30 anchor fights vs 30 seed-matched dark fights, boss `skill_idx == 0`:**

| leg | events | elements | delivered |
|---|---|---|---|
| split **ARMED** | **91** | `physical` × 91 | 18.067 … 24.761, **mean 21.344** |
| split **DARK** | **77** | `cold` × 77 | 11.667 … 50.995, **mean 42.247** |

**ONE event per landing in BOTH legs.** §2(1) describes the damage-**effect list inside the mob
packet**, which `replica-frame/v1` does not carry; §2(2) is the one that is true of the trace. A
consumer that acted on §2(1) would have gone hunting for a second event that does not exist — and
one that "corrected" for the double-count would have **halved the boss's melee on screen** and made
the anchor look twice as forgiving as it is.

**⚑ AND SO THE COMPOSITION IS IN THE NUMBER AND NOT IN THE STREAM.** 21.344 is
`0.30 × 38.699 + 0.86 × 11.301 = 21.329`. **45.57 % of what the player takes from that swing is
COLD, and there is no field anywhere in the trace that says so.** The only visible tells are
`element` flipping `cold → physical` and the magnitude collapsing **1.98×**.

That is why the composition ships as a **declared** caption reading the roster's own
`_kc1_meta.melee_channel_split`, beside the **read** `delivered`, with the cold share labelled
**DERIVED** — never as a field, and never by multiplying `delivered` by `physical_share` (the shares
are pre-mitigation and the two operators differ, so `0.774 × delivered` would be a number this seam
invented).

---

### FINDING 3 — ⚑ **THE ROSTER ROW THAT CARRIES THE SPLIT HAS NO ENTITY ID. The join is a string transform.**

An `opposition_roster` row carries exactly:

```
{cell_of_record, char_level, char_level_owner, dmg_grade, hp_grade, hp_provenance,
 label, max_hp, record, tier}          (+ melee_channel_split on the boss row)
```

**Not one of those is the entity id.** The per-frame block is keyed on `entity_id` =
`boss&quest_slith_wightmirecave01_0`; the roster's nearest thing is `record` =
`boss&quest/slith_wightmirecave01`. Bridging them needs a `/`→`_` substitution **and** a spawn-index
suffix — the consumer has to reconstruct the producer's id-minting rule.

**This is the third instance of the same custody shape in three cells**: C_reach before D-F3, the
nova unit payload before R-WR2-15(2), and now this. The information exists; the **join** does not.

My first cut read `row["mob_id"]`, got `{}` on every row, and cheerfully rendered the ANCHOR fight
labelled *"roster declares NO split — 100 % cold."* **It was wrong on the picture and silent in the
log**, and it was caught only because I knew from a Python measurement what the answer had to be.
The shipped reader selects the unique split-declaring row **and** cross-checks the `record`
transform against the attacker id, and returns `{}` with a warning if they disagree — it never picks
one and carries on.

---

### FINDING 4 — ⚑ **THE COMMIT LOCK IS NOW 15 EMITTED TICKS (`w5/s1/r9`), NOT THE 7 (`w4/s1/r2`) I MEASURED AT STAGE 1.**

Measured on the anchor, seed 74000802: `{"w5/s1/r9": 41, "w2": 1}` — and cross-checked against the
W-1 census on the same fight, which is exact by construction: `windup 206 = 41 × 5 + 1`,
`recover 369 = 41 × 9`, `strike 41`.

The W-1 amendment §2 states the tick-edge convention is **parametric in `W` and `R`** and that a
referent-driven change to `W` would fail `TestDF1Fencepost` *"loudly and by name"* rather than
silently re-opening the D-F1 disagreement. **`W` moved 3 → 4 and `R` moved 2 → 9 between stage 1 and
the anchor.** Reported from the consumer side; whether the test fired is gamora's to say. The render
draws the field, as it always has.

**The consequence a viewer sees:** at stage 1 the boss landed **4.45 %** of its melee (136 / 3,098)
and the fight became a metronome the player had solved. **On the anchor the boss lands 28.2 %**
(91 / 323 strikes over 30 fights) and **90.2 %** on the rendered seed (37 / 41). The stage-1
"broken-easy" reading — *the swing is a clockwork and the player has solved it* — **is gone.**

---

### FINDING 5 — ⚑ **THE "CYCLING" ICEARMOR CASTS ONCE, AT t = 0, AND NEVER RETURNS — AND G-I1's 0.336 IS A FUNCTION OF FIGHT LENGTH.**

`wr3_icearmor` reads TRUE on **ticks 0–119, one contiguous run, on 30 of 30 anchor fights, σ = 0.**
120 ticks = 12.0 s = exactly one buff duration. `icearmor_casts` = 30 over 30 fights = **one cast
per fight.** The arm of record calls this *"icearmor cycling"*; it does not cycle.

G-I1 measures uptime **3630 / 10802 = 0.3360** against `[0.30, 0.42]` and PASSES. But 120 ticks over
a 361-tick mean fight **is** 33.2 % — so **the gate is reading fight length, not buff behaviour.**
On the rendered seed (824 ticks) the true uptime is **14.6 %**; on seed 74000817 (480 ticks) it is
**25.0 %**. Both sit outside the band, and the pooled number sits inside it. **A ratio whose
denominator is the fight duration is not a duty cycle**, and this one can be walked across its own
band by the fight getting longer.

Routed, not ruled. The ward is drawn — a slow cold shell at 2.05× the body radius, breathing on a
3.1 s period, deliberately **not** the rime lock ring (1.45–1.63×, 6–7.5 s) — because a boss that is
absorbing and a boss that is frozen must not look the same.

---

### FINDING 6 — INFO — **THE PLAYER NEVER CLEARS A RING IN THE ANCHOR WORLD. 0 escapes of 67 firings, 30 of 30 fights.**

At owner-eye #3 the headline geometric beat was the player backing *out* of the first nova ring
(10.21 m → **12.221 m**, clear by 0.221 m). On the anchor: **zero** ring escapes across 67 nova
firings. On the rendered seed the player is at **5.478 m** and **5.162 m** when the two rings fire,
both deep inside the 12 m footprint. `evade:tg` — the K-T1 telegraph limb that produced the stage-1
escape — fires **95 ticks over 30 fights** against `evade:commit`'s **3,212**. The kite is alive and
it is doing something else.

**Escaped is still not delivered, and this seam still does not conflate them.** The frame claims
"inside the footprint" and nothing more.

---

### FINDING 7 — INFO — **A FOURTH `evade:` LIMB EXISTS AND IS DARK: `evade:dash`.**

`spatial_engine.py:5671-5676` emits `evade:dash` under MECHANISM EV when `_ev_arm_dash` succeeds.
It is now **registered in `EVADE_LIMBS` before being observed** — measured **0** occurrences on the
anchor, and `evade:pressure` is also **0** (it was 46 ticks at stage 1). This is the **fourth
value-set growth in four runs** on the intent channel and the rule stated at owner-eye #3 holds
verbatim: *on this schema, an exhaustive match without a default arm is a latent silent-wrong-render.*

---

## §5 — TWO OVERRIDES OF MINE, RETIRED CLEANLY, BECAUSE THE ENGINE CAUGHT UP

### RETIRED 1 — **C_reach no longer comes out of a grading artifact.**

Owner-eye #3 FINDING 3 routed it: the whiff verdict needed the boss's reach, the trace did not carry
it, and this seam was reading `AFTER.G2.definition.c_reach_m` out of `wr3_cell_kc_statistics.json` —
*a grading artifact, not an emission contract*. **D-F3 granted it.** The engine now measures the
reach through the same `wr3_effective_reach` that `_wr3_reach_to` resolves through and emits it at
`g5_header.g5.commit_reach`. The override is out, and **the two sources are cross-checked on the way
out** rather than one silently replacing the other:

```
[wr3] C_reach 2.5000 m  <- EMITTED — g5_header.g5.commit_reach
      [min(range_m over damaging skills) + target.entity_radius]
      ·  cross-checks the retired artifact read to 1e-9
```

The artifact read survives **only** as a fallback for the older batteries whose headers predate
D-F3, and it says so on the banner when it fires. It still never falls back to 2.0.

### RETIRED 2 — **"there is no per-frame `ai_state` in this schema" is no longer true, and no longer printed.**

Owner-eye #3's probe printed, on every run: *"⚑ NO `ai_state` field exists in this schema (W-1,
post-stage-1). None is drawn."* **R-WR3-14 (W-1) landed it.** Measured on the anchor:

```
boss    {approach 2, engage 206, windup 206, strike 41, recover 369, null 1}
escort  {approach 91, engage 23, null 1}
player  key ABSENT on 825 / 825 ticks
```

The AI tag now draws the **witness label**, with **three arms for three-valued presence** exactly as
AI-D3 requires: key **absent** → the player, out of scope, fall through to `commit_state`; key
present + **`null`** → *no state to be in* (a corpse); key present + **string** → a vocabulary
member, carried verbatim, warning by name if it is outside `AI_STATES`. `null` and "unknown label"
**do not share a branch** — that was gamora naming my own D-F4 rule back at me, and it is honoured.

---

## §6 — ⚑ FOUR OF MY OWN FAILURES, ON RECORD

1. **The melee caption was invisible three times, and world-space could never have fixed it.**
   Anchored on the target at +3.5 m, then +5.6 m, then on the **attacker** at +7.2 m — and the
   Bangers damage numeral went straight through the text every time. The reason is arithmetic, not
   luck: `arena_full` stands 58 m off a 36 m arena and resolves **~17 screen-px per sim-metre**, and
   the boss and player are welded at the 2.0 m contact floor for most of this fight. **Two metres is
   34 pixels.** No world-space offset separates a caption from a floater rising out of a body 34 px
   away; raising it only moves the collision. The composition moved to a **fixed screen slot**. One
   fact per channel, and the channels cannot overlap because one of them is not in the world.
   *Caught on a rendered frame at 3× zoom — invisible in the source, every time.*

2. **The banner ran off the bottom of the frame and straight through the roster.** Its Y was a
   literal (522) and the stage-2 additions took it to 21 lines. Then two hand-picked Y literals for
   the melee slot (118, then 140) **both** landed inside the camera-identity block, which is three
   long lines that *wrap* at 1280 px and therefore has no constant height. Both blocks are now
   placed by `_banner_reflow()` from their own measured line counts, bottom-anchored.

3. **My `trace_decisions` non-perturbation proof reported PERTURBS on its first run — and it was the
   proof that was broken, not the engine.** The filter was written `'"event": "decision"'`; the sink
   writes **compact** JSON (`separators=(",", ":")`), so it matched nothing and every decision record
   was counted as a difference. Caught because the difference count landed on **exactly** the record
   surplus (14,580 = 28,153 − 13,573), which is the shape of a filter that matched zero, not of a
   perturbation. A verdict of "PERTURBS" that I had believed would have HALTed this cell on a
   punctuation bug.

4. **`wr3_pick_scan.py` scored 66 stage-1 fights with an unqualified circle-test** and I shipped it
   at owner-eye #3. It was correct then — 114 nova circles, 0 blizzard circles in that battery — but
   I did not know that when I wrote it; I knew it after I measured it for this note. The new scan
   carries a `--shape-test` mode that **reproduces the defect on purpose** so its size is a
   measurement in the file rather than a claim in a note.

*(And GAP 3 from owner-eye #3 bit again: four `python3` on PATH, two carry Pillow. Prefixing
`/opt/homebrew/bin` for `ffmpeg` shadowed the interpreter that had it. The still-makers now name
their interpreter.)*

---

## §7 — SMOKE GATE

Headless `--probe` on **both** anchor batteries: `parse_errors = 0`, all five record types and all
six event kinds present and dispatched, both schema strings quoted on the frame, engine pin read off
the trace (`9c978b1e`) and cross-checked against the registry. The stage-1 probe's three verbs still
run; `_wr3_probe_stage2()` adds the four this close is watched for. Both legs' full output is in §3
and §4 above.

**Regression, the older batteries:** the WR2 `after` / `before` and WR3 `wr3_after` / `wr3_before`
paths are untouched by the registry addition — the anchor entries are new keys, `fight_path` gains a
`flat` arm that only fires for them, and the C_reach reader falls back to the artifact for any
header that predates D-F3 and says so.

---

## §8 — WHAT MATT SHOULD BE ABLE TO TELL ME AFTER WATCHING

Not pre-answered. Five things to disbelieve if they look wrong.

1. **At t = 5.80 s, the same swing lands for 18.62 on the right and 39.15 on the left.** Same seed,
   same tick, one flag. That is the re-split, and it is the only difference between the two clips.
2. **The left-hand fight ENDS at 51.2 s with the player dead. The right-hand fight runs to 82.5 s
   and the player wins.** This is the one seed of thirty whose outcome the change moves, and it is
   the seed you have watched twice before.
3. **The 12 m star and the 8 m storm are on the frame within 10 seconds of each other**, at
   different radii, from different origins, each named on the clock line — `tell: NOVA … r 12.00 m`
   and `tell: BLIZZARD … r 8.00 m`. They are told apart by a **substring**, not by the field that
   exists for it, and the banner says so.
4. **The ward is up for the first 12 seconds and then never again**, in a fight that runs 82. If
   "icearmor cycling" was meant to describe a duty cycle, this is not one.
5. **The boss lands 37 of 41 swings.** At stage 1 it landed 4.45 % and you were shown a metronome
   the player had solved. That reading is gone. Whether *this* is the referent fight is the
   question the parity criterion actually asks.

And one question that is yours and not mine: **the anchor reproduces the referent's arithmetic to
−0.9 % and wins 30 of 30. H1 has stopped discriminating** (the refit report says so itself, §7.5).
The clip is the only instrument left that can tell you whether a fight the engine reproduces
*correctly* is a fight that reads *right*.

---

*WR3-KITE-COMMIT stage-2-close owner-eye render — drax, presentation seam, 2026-07-31.
`reincarnated-godot` committed LOCAL, **NOT pushed**. No engine path touched.*
