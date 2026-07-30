# WR3 — K2-PREP / W-1 SCHEMA AMENDMENT (the D-F1 verdict, the witness label, C_reach's custody, the per-frame pool)

**Date:** 2026-07-30 · **Author:** gamora (simulation seam) · **Class:** verdict note
**Cell:** K2-PREP/W-1 schema amendment of run **WR3-KITE-COMMIT**. **Conductor:** gandalf (`RUN-CONDUCTOR`).
**Authority:** charter §2 **R-WR3-16** (D-F1 routed-and-blocking, D-F3 ADOPTED, and the "NOW FIRING"
bundle) · **R-WR3-14 (W-1)**, MATT-SIGNED · **R-WR3-10(b)** (K2-prep sequenced first in the K2 lane).
**Consumed:** drax `2026-07-30-wr3-stage1-owner-eye-render.md` §4 Findings 1 / 3 / 5; my own
`2026-07-30-wr3-stage1-build-report.md` §1.2; the frozen `wr3_battery_after_s11/` traces (READ-ONLY).
**Math note (written BEFORE the code, Discipline #1):**
`reincarnated-engine/src/reincarnated/simulation/math/wr3-w1-schema-amendment-2026-07-30.md`
**MIGRATION (ADR-004):** `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`, entry
**"[2026-07-30] WR3 K2-PREP / W-1"** (top of file). Consumers named: **drax**, **galadriel**, **star-lord**.
**Schema doc:** `agentic_orchestration/gandalf/notes/2026-07-22-replica1-frame-schema-spec.md`,
new **§2-AMENDMENT** (the convention is declared there as well as here, per the commission).

---

## §0 — THE D-F1 VERDICT, IN ONE SENTENCE

**NO HALT. The movement lock is SIX ticks (`T_lock = 0.60 s`, R-WR3-13 F1 STANDS); drax's SEVEN is
the EMISSION count, and the two differ by exactly one tick because the frame is written at the end
of the tick — after the action phase that enters `windup` — while the movement lock is read at the
navigation phase, before it.**

`N_emit = N_lock + 1`, always, by phase order. The fencepost is **inclusive-on-emit,
exclusive-on-lock**, exactly the shape R-WR3-16 predicted. It is now a **declared contract** in the
math note, in `MIGRATION.md` §2, in the schema doc's new §2-AMENDMENT, and in the producer's own
docstring — and it is **pinned in both directions** by tests that fail if the lock ever becomes 7.

---

## §1 — D-F1 RESOLVED FROM SOURCE (line numbers, both readers, the tick edge)

### 1.1 Which variable does each reader read?

| reader | reads | site |
|---|---|---|
| **the committed-tick-share counter** | the **EMITTED** `commit_state` — `sum(1 for s in cs if s != "idle") / len(cs)` | `simulation/wr3_cell_kc_2026_07_30.py:424` (populated from `eb.get("commit_state")` at **:397**) |
| **the emitter** | `getattr(ent, "commit_state", "idle")` | `spatial_gauntlet/replica_frame_emitter.py:256` |
| **the movement lock** | `_c2_move_scale(mob)` → `getattr(mob, "commit_state", "idle")`, at the `_navigate_entity` **read site** | `spatial_engine.py:5025-5037`, called at **`:6002`** |

**⚑ THE FIRST CORRECTION: the share counter and the emitter read THE SAME VARIABLE.** The counter is
a census of the emitted field and is **structurally incapable** of measuring the movement lock. It
does not "side with 6" — it cannot side with anything but the emission.

### 1.2 At which tick edge does the initiation tick get its state?

Execution order inside one loop iteration (`spatial_engine.py`):

| # | phase | line |
|---|---|---|
| 1 | `_c2_service(alive_mobs)` — advance the state machine one tick | **5976** |
| 2 | `_k_obs_snapshot(...)` — world-at-tick-start observation | 5985 |
| 3 | **mob navigation** — `_navigate_entity(..., move_scale=self._c2_move_scale(mob))` | **6002** |
| 4 | **mob action phase** — `_c2_initiate(...)` sets `commit_state = "windup"` | **6668** |
| 5 | **`_frame_sink.tick(...)`** — the frame is written | **7390** |

Initiation happens at **phase 4**; the frame is written at **phase 5**; navigation already ran at
**phase 3**. So on the initiation tick **T** the boss **emits `windup` and moves at full speed**.
The transition rule (`:5061-5083`) then locks **T+1 … T+6** — windup 3, strike 1 (`:5114` puts the
strike at `T + windup_ticks + 1 = T+4`), recovery 2 — and `_c2_clear` releases at T+7.

| | ticks | value |
|---|---|---|
| **N_emit** (`commit_state` non-idle) | T … T+6 | **7** — `w4 / s1 / r2` |
| **N_lock** (`move_scale < 1.0` at navigation) | T+1 … T+6 | **6** — **`T_lock = 0.60 s`** |

The telegraph is minted at phase 4 of tick T (`:5144`) with `fire_tick = T+4` — the **4-tick lead**
drax measured (mint 68 → fire 72). The telegraph channel was **siding with `N_emit`, correctly.**

### 1.3 ⚑ THE SECOND CORRECTION: 0.3992 does NOT side with 6

R-WR3-16 read `0.3992 ≈ 6/15 = 0.400`. That assumed a 15-tick period with no dead time. **Measured
directly off the 66 frozen AFTER boss traces (read-only, nothing regenerated):**

| quantity | measured |
|---|---|
| emitted episode shape | **`w4/s1/r2` on 3,096 / 3,098** (the 2 exceptions are `w3/s0/r0` — windups truncated by fight end) |
| mean per-fight share (the reported statistic) | **0.399167** |
| pooled share | 0.399816 |
| boss-alive ticks | 54,220 (mean **821.5** / fight) |
| commit episodes | 3,098 (mean **46.94** / fight) |
| initiation→initiation gap | mean **16.18** ticks; `{15: 2664, 16: 314, 75: 42, 77: 12}` |
| first initiation tick | **68 on 66/66 fights**, σ = 0 |

`46.94 × 7 / 821.5 = 0.400`. **The 6-tick counterfactual reads 0.3427, not 0.400.** The four-figure
agreement with the duty-cycle prediction is real, but it is agreement about **7 emitted ticks over a
16.18-tick realized period diluted by a 68-tick commit-free opening** — not about `6/15`. The
arithmetic that appeared to corroborate 6 was a coincidence of two wrong inputs.

### 1.4 The empirical falsifier (the thing that would have forced the HALT)

`C2_WINDUP/STRIKE/RECOVERY_MOVE_SCALE` are all **0.0** (`spatial_engine.py:123-125`), so a locked
tick has **exactly zero navigation displacement**. Boss per-tick displacement keyed by index within
the emitted episode, all 3,098 episodes:

| idx | emitted state | n | max disp (m) | mean disp (m) | n > 1e-9 |
|---|---|---|---|---|---|
| −1 | idle (pre) | 3098 | 0.402500 | 0.392271 | 3098 |
| **0** | **windup** | **3098** | **0.402500** | **0.389992** | **3098** |
| 1 | windup | 3098 | 0.054211 | 0.001929 | 244 |
| 2 | windup | 3098 | 0.038765 | 0.001750 | 246 |
| 3 | windup | 3096 | 0.037682 | 0.001289 | 214 |
| 4 | strike | 3096 | 0.035770 | 0.000783 | 132 |
| 5 | recovery | 3096 | 0.033074 | 0.000649 | 132 |
| 6 | recovery | 3096 | 0.029336 | 0.000588 | 72 |
| 7 | idle | 3096 | 0.407537 | 0.400432 | 3096 |

**Index 0 moves a full step — `0.4025 m = 4.025 m/s × 0.10 s` — on 3,098 of 3,098.** Indices 1–6 do
not navigate. **`N_lock = 6`, measured, not reasoned.** Had index 0 read zero, this note would have
been a HALT report.

### 1.5 INFO — the lock is a NAVIGATION lock, not a position freeze

Indices 1–6 are not bit-zero on ~8 % of episodes: the boid soft push-apart / boss hard-collision body
(`spatial_engine.py:2331-2409`) is a **separate position writer** and still runs. Measured mint-tick →
strike-tick origin drift over 3,096 strikes: **median 0.000000 m, mean 0.005624, p99 0.108, max
0.148**, non-zero on **248 / 3,096**. **Heading drift is exactly 0.0 rad on 3,096 / 3,096** —
C2-L2's no-re-aim clause is bit-exact. So `_c2_initiate`'s claim that the mint origin equals the
strike origin "BY CONSTRUCTION" is **exact for heading** and **true to within 0.148 m for origin**.
Moves no gate (C_reach's land/whiff bracket carries 0.091 m of clean air, and this is a *pre*-strike
origin question, not a strike-separation one). **Reported, not ruled.**

---

## §2 — THE DECLARED CONVENTIONS

> **TICK-EDGE CONVENTION (`replica-frame/v1`).** Every per-frame entity field is sampled at the
> **END of the tick, after the action phase**. `commit_state` — and therefore `ai_state`'s commit
> limb — is **INCLUSIVE of the initiation tick**: an episode emits `windup × (W+1)`, `strike × 1`,
> `recovery × R`. The **movement lock** is read at the **navigation** phase, before the action
> phase, and **EXCLUDES** it: `N_lock = W + 1 + R`. **`N_emit = N_lock + 1`, always, by phase
> order.** A consumer measuring `T_lock` from a trace **drops the first tick of the run**; a
> consumer drawing the **animation** uses all of it.

> **W-1 SAMPLING-EDGE CONTRACT.** `ai_state`'s commit limb is a **pure rename of `commit_state`**
> (`recovery` → `recover`, and nothing else). Label and lock therefore agree **by construction —
> the label reads the locked variable** — rather than by coincidence, which is what R-WR3-16 asked
> for. Verified per entity per tick: **0 violations**.

Both are written into: the math note §1.6/§2.7 · `MIGRATION.md` §2 · the schema doc's §2-AMENDMENT ·
`ReplicaFrameSink.tick`'s docstring · `ai_state_label`'s docstring.

---

## §3 — WHAT WAS ADDED

### 3.1 W-1 — per-frame `ai_state` (R-WR3-14)

Three additive keys on the per-tick entity block, plus one engine classifier:

| key | scope | meaning |
|---|---|---|
| `ai_state` | **ENEMY (mob-side) blocks ONLY** | the witness label |
| `max_hp` | every block | the pool **NOW** (§3.3) |
| `movement_speed_ms` | every block | the live speed stat (§3.3) |

**Vocabulary FIXED** — `approach, engage, windup, strike, recover, leash-return` — as
`spatial_engine.AI_STATES`, pinned by test.

**Derivation law — ONE IMPLEMENTATION (R-M3-1 family), no parallel state machine:**

| label | READS |
|---|---|
| `windup` / `strike` / `recover` | `entity.commit_state` — **the field C2 itself writes** |
| `leash-return` | `entity.is_leashing` — the R2 territory-guard latch (**dormant**: 0 occurrences in these batteries, which is correct) |
| `engage` | `_select_skill_for_entity`'s **own** range predicate, ∃ over damaging skills |
| `approach` | otherwise |

**Measured on the re-emitted smoke fight** (`pre`/boss/B/74000802, 950 ticks): boss
`engage 554 / windup 220 / strike 55 / recover 110 / approach 10 / null 1`; escort `slitha_melee`
`approach 80 / engage 31 / null 1`; escort `slitha_shaman` `null 1`; player **absent on 950/950**.
`windup 220 = 55 × 4`, `recover 110 = 55 × 2` — the emitted 4/1/2 shape, by construction. The one
`null` per mob is its death-transition frame (AI-D3: a corpse has no AI state).

### 3.2 C_reach custody (D-F3)

Emitted **MEASURED** from `spatial_engine.wr3_effective_reach` — the same function `_wr3_reach_to`
resolves through, so a whiff and a drawn ring cannot disagree — at **two sites**:

- **`g5_header.g5.commit_reach`** (per trace; the renderer's join): `{law, against_entity_id,
  body_separation_v2, by_attacker_m}`.
- **leg report top level, `commit_reach`, immediately beside `presentation_units`** (D-F3's literal
  wording): `{ruling, definition, source, n_fights_recorded, values_observed_m, constant, per_tier}`.

Smoke output on the boss leg: `{boss: 2.5, slitha_melee_b01: 2.5, slitha_shaman_c01: 18.5}` —
**boss C_reach 2.5 m, reproducing drax's independently-verified value exactly**, and `constant:
false` because the shaman's 18 m cast reach is a different number. **A leg-wide scalar would have
been wrong** and the block says so.

### 3.3 K2-prep — the pool onto the per-frame block (R-WR3-10(b))

`max_hp` and `movement_speed_ms` now ride every per-frame entity block. `hp / max_hp` is computable
from **one tick record**, which is the pool-fraction grader's actual join, and a K2 form swap will
move the per-frame value while the header stays truthful about the form the fight opened in.

---

## §4 — DECISIONS I HAD TO NAME (conductor ratifies; none is silent)

| id | decision | why it needed naming |
|---|---|---|
| **AI-D1** | **The approach/engage discriminator is CONTACT-BASED on the SELECTOR'S OWN range predicate, with cooldown / energy / silence readiness EXCLUDED.** The range test was **extracted verbatim** out of `skill_ready` into `spatial_engine._skill_range_covers`, so the label and a range-legal swing are **one expression**. Three sub-decisions: **(1)** the target is the mob action phase's `min(_enemies_of(…), key=distance_to)`, **not** the taunt-weighted *navigation* target — `engage` is an action predicate and must name the body a swing would test against; **(2)** cooldown excluded, because a mob standing in reach between swings is engaged and gating on it would make the label flicker at the 1.5 s metronome, which `windup/strike/recover` already witnesses; **(3)** reach is the **∃ over damaging skills (MAX)**, deliberately **not** `_wr3_reach_to`'s **MIN** — the MIN is C_reach, the kite shelf, a different question, and on the fixture boss they differ by **8 m** (2.5 vs 10.5). | the commission asked for it explicitly ("state it as a named decision, not silently"). The expected shape — contact-based — is what landed. |
| **AI-D2** | **Commit OUTRANKS `leash-return`.** `_navigate_entity` returns at `move_scale <= 0.0` (`:1996`) **before** its `is_leashing` branch (`:2036`) — a committed mob is frozen, it does not walk home. **⚑ The ACTION path orders them the OTHER WAY** (`if mob.is_leashing: continue` at `:6588` precedes the C2 block at `:6606`), so the two mechanical paths disagree; the label follows the **movement** path, because five of six vocabulary members are locomotion/animation states. | there is **no single mechanical precedence to inherit** — this had to be chosen. The corner is **dormant** in every current battery (boss leash 18 m in a 36 m arena, `is_leashing` False on 100 % of ticks); a dormant disagreement that later fires silently is the WARN-N1 shape. |
| **AI-D3** | **`null` is a member of the EMISSION, not of the vocabulary.** Key **absent** = player/ally block, out of scope; key present + **`null`** = **no state to be in** (no live foe, **or the body is a corpse** — the frame keeps emitting a just-dead entity for the renderer's death transition, and `alive: false` beside `ai_state: "engage"` would be a small lie on that frame); key present + **string** = a vocabulary member. | three-valued presence. Drax's own D-F4 rule applies at its fourth occurrence: an exhaustive match without a default arm is a latent silent-wrong-render — and **`null` and "unknown label" must not share a branch**. |
| **K2P-D1** | **The pool move is an ADDITIVE MIRROR, not the literal "move" R-WR3-10(b) words.** The header **keeps** `max_hp` (now explicitly *the pool at SPAWN*); the per-frame block **gains** it (*the pool NOW*). | a true move deletes the field every existing HP-bar reader binds to, and the cell's own rules are *additive, default-absent, old traces still parse*. Deviation from the ruling's literal wording — flagged, not smuggled. |
| **K2P-D2** | **`movement_speed_ms` rides the same move, UNCONDITIONALLY on the per-frame block**, while the **header's** key keeps its existing **conditional** emission and meaning (WR2 Cell D: *absent = the escape law did not govern*). | R-WR3-10(b) names S-7's join key; a form swap moves pool **and** speed in one event, and a key that is form-aware only when an unrelated nova arm is set is not form-aware. **⚠ Two fields, same name, different meanings** — called out in MIGRATION §4 so no consumer conflates them. |

### Declared vocabulary debts (routed to W-2, NOT patched)

The vocabulary is FIXED, so two mechanically-real states take the geometric fallback: an
**un-activated serial mob** (proximity-aggro pre-pull, `spatial_engine.py:6595-6599`) reads
`approach`, and a **hard-CC'd** mob reads `engage`/`approach` by distance. **Both are ABSENT from
the WR3 batteries by construction.** W-2's encounter-AI lap owns proximity aggro and therefore owns
the dormant/aggro labels; adding them here would have been me widening a Matt-signed vocabulary.

### Two things left alone on purpose

- **The cell's `C_REACH_M = 2.5` literal stays.** Moving a grading artifact's constant to read the
  emitted value would change a graded column and break comparability with the frozen cell
  statistics. Routed as a follow-on.
- **`_skill_range_covers` preserves an UNREACHABLE branch.** `float(skill.get("range_m") or 2.0)`
  maps a declared `0.0` to `2.0` (0.0 is falsy), so the `range_m == 0.0` self-cast/leap carve-out
  below it **can never fire**. The extraction is faithful **including the dead branch** — "fixing"
  it would be a silent behaviour change smuggled inside an emission amendment. Pinned by a test
  that asserts the branch is dead. **Reported; routed, not patched.**

---

## §5 — SMOKE EVIDENCE

**Cheap suite first, then the battery-shaped smoke — the two never ran concurrently.**

### 5.1 One re-emitted smoke fight (the cell's proof obligation)

Argv is the WR3 battery's argv character-for-character with `--seeds 1 --seed-base 74000802` and a
scratch `--out-dir`. Root: `simulation/output/kitcal_g5/wr3_w1_smoke/`. The boss/B fight runs
**95.0 s, player wins** — the same fight drax rendered.

```
g5_header.g5.commit_reach = {
  "law": "min(range_m over damaging skills) + target.entity_radius",
  "against_entity_id": "gd-werewolf-kitcal-1", "body_separation_v2": true,
  "by_attacker_m": { "boss&quest_slith_wightmirecave01_0": 2.5,
                     "slitha_melee_b01_1": 2.5, "slitha_shaman_c01_2": 18.5 } }

tick[0].entities[]:
  gd-werewolf-kitcal-1   ai_state=<ABSENT>   max_hp=759.0     movement_speed_ms=5.75
  boss&quest_slith_…_0   ai_state=approach   max_hp=14812.0   movement_speed_ms=4.025
  slitha_melee_b01_1     ai_state=approach   max_hp=577.0     movement_speed_ms=4.0825
  slitha_shaman_c01_2    ai_state=engage     max_hp=846.0     movement_speed_ms=4.0825

ai_state census, 950 ticks:  boss {engage 554, windup 220, strike 55, recover 110,
                                   approach 10, null 1}
                             slitha_melee {approach 80, engage 31, null 1} · slitha_shaman {null 1}
                             player <ABSENT> ×950      (the one null per mob = its death frame)
commit_state <-> ai_state contract violations: 0
ai_state episode shapes: {'w4/s1/r2': 55}
displacement on the INITIATION tick  (idx 0):    n=55  max 0.402500  mean 0.392505
displacement on the LOCKED ticks (idx 1..6):  n=330  max 0.037867  mean 0.000877
```

### 5.2 ⚑ NON-PERTURBATION, MEASURED

The re-emitted trace was compared **record-for-record** against its frozen twin in
`output/kitcal_g5/wr3_battery_after_s11/`. With the four new keys stripped and the engine hash
normalised:

```
records new/old: 2445 2445
differing records after stripping the amendment keys: 0
```

**2,445 / 2,445 byte-identical.** The amendment is emission-only; the fight did not move.

### 5.3 Frozen roots untouched

`wr2_battery_after/` and `wr3_battery_after_s11*` were opened **READ-ONLY**, never regenerated,
never written. `git status` reports **no modification** under either root at cell end. No battery
re-run was performed and none was required.

### 5.4 Unit tests + regression

| item | value |
|---|---|
| New unit tests | **30** in `tests/test_wr3_w1_schema_amendment.py`, all passing |
| WR3 stage-1 suite (re-run) | **3,523** passing, unchanged |
| Combined WR3 files | **3,553 passed in 1.52 s** |
| Full regression vs the 81-name baseline | **PENDING-LINE — see §5.5** |

The new file pins: the D-F1 fencepost **in both directions** (including the falsifier that fires if
the lock ever becomes 7 ticks); the sampling-edge contract per entity per tick; AI-D1/D2/D3; W-1
scope (present on boss **and** escorts, absent on the player); the per-frame pool/speed keys and
K2P-D2's conditional-vs-unconditional split; D-F3's `2.5 ≠ 2.0`; and additivity — an engine with no
`ai_state_map` still emits a frame, and a pre-amendment record still parses.

---

## §6 — FILES TOUCHED

**`reincarnated-engine`:**

| file | change |
|---|---|
| `simulation/math/wr3-w1-schema-amendment-2026-07-30.md` | **NEW** — math note, written before the code |
| `simulation/spatial_gauntlet/spatial_engine.py` | `wr3_effective_reach` + `_skill_range_covers` extracted (behaviour-preserving); `AI_STATES` + `ai_state_label`; `ai_state_map` / `commit_reach_map`; `_wr3_reach_to` delegates |
| `simulation/spatial_gauntlet/replica_frame_emitter.py` | the tick-edge convention docstring; three additive per-frame keys |
| `simulation/spatial_gauntlet/kitcal_g5_trace.py` | `g5_header.g5.commit_reach` |
| `simulation/spatial_gauntlet/kitcal_g5_harness.py` | `G5MetricsSink.commit_reach_m`; `FightRecord.commit_reach_m`; `_commit_reach_block`; the leg-report key beside `presentation_units` |
| `simulation/MIGRATION.md` | the ADR-004 entry (top of file) |
| `tests/test_wr3_w1_schema_amendment.py` | **NEW** — 30 tests |

**`reincarnated-collaboration`:** this note · the schema doc's new **§2-AMENDMENT**.

Neither repo pushed — **the conductor pushes.**

---

*WR3 K2-prep / W-1 schema amendment — gamora, simulation seam, 2026-07-30.*
