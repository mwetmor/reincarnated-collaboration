# WR3-KITE-COMMIT — STAGE-1 MECHANISM SPEC (K + C2)

> **STATUS:** CURRENT · **Date:** 2026-07-30 · **Author:** gandalf (`SPEC-AUTHOR`)
> **Status:** SPEC FROZEN for stage 1, pending the two §8 items the conductor must rule and the one
> §8.6 pre-build measurement.
> **Authority:** charter `agentic_orchestration/gandalf/notes/2026-07-30-wr3-kite-commit-run-charter.md`
> §2 (R-WR3-7 · R-WR3-9 · R-WR3-10 · R-WR3-11) + §4 (stage-1 shape + gates). Commissioned by
> gandalf `RUN-CONDUCTOR`. The grill is CLOSED — this document turns ratified decision rules into a
> buildable engine spec and rules nothing the charter left open.
> **Builder:** gamora (simulation seam). **Gate-2:** jack-ryan, untouched.
> **Companion docs:** `gamora/notes/2026-07-30-wr3-formswap-feasibility.md` (engine facts of record) ·
> `gamora/notes/2026-07-30-wr2-f5-pursuit-diagnostic.md` (the measured BEFORE state) ·
> `canonical/reap-die-rise-engine/telegraph-dodge-temporal-decoupling-2026-06-15.md` §7.2 (the canon
> constraint §8.1 flags) · `operating-procedures/desirable-run-pattern.md` (honorable fallback).

---

## §0 — What this document is, and the two disciplines that bound it

**IS:** the engine spec a specialist builds against. Mechanism K (player kite/evade) and Mechanism C2
(boss attack-commit), the env-interface contract they land behind, and the pre-registered gate table
with every column's computing cell named.

**IS NOT:** production code, an engine edit, a calibration pass, or a reopening of the grill. No
number in this document tunes the fixture. Every value stage 2 owns is marked **[CAL]** and
registered in §6.

**Two disciplines govern every clause below.**

1. **One implementation (R-M3-1).** Where a function already computes the thing, the spec calls it
   and does not re-derive it. K's telegraph limb calls `nova_expected_delivered`; C2 parses its
   packet through the existing `read_commitment`; the gate cell imports the WR2 instruments by
   module rather than by copy. A second copy of a payload law is the defect R-M3-1 exists to prevent,
   and it is invisible until the day the two disagree.
2. **Named semantic shift (Discipline #12).** Every invariant this build makes false is named here,
   at the clause that breaks it, not discovered at Gate 2.

### 0.1 Provenance of the engine facts cited

Facts marked **[gamora]** come from `gamora/notes/2026-07-30-wr3-formswap-feasibility.md` or
`…-wr2-f5-pursuit-diagnostic.md`; cite the note, not its line numbers, which drift. Facts marked
**[SA-read]** are this author's own read at engine HEAD `54536c30` (the same commit as gamora's read)
and carry the same drift caveat. Facts marked **[banked]** come from
`simulation/output/kitcal_g5/wr2_battery_after/wr2_bat_statistics.json`, frozen.

---

## §1 — The substrate this builds on (the BEFORE state, restated as build inputs)

| fact | value | source |
|---|---|---|
| boss / player speed ratio | 4.025 / 5.75 = **0.70** (boss slower) | [gamora] |
| player speed provenance | **ungraded engine default** 5.75 (`movement_speed_provenance = "engine-default-ungraded"`) | [gamora] |
| boss commit state | `idle` on **76,714 / 76,714** boss-alive ticks | [gamora] |
| boss movement | displaces on **100 %** of ticks, mean `u` 0.9577, incl. 100 % of its own nova wind-up | [gamora] |
| median separation | **exactly 2.000 m in 180 / 180 boss fights** (= body floor `C_body`) | [gamora] |
| melee gate | `C_reach` = `range_m` 2.0 + target radius 0.5 = **2.5 m** under `body_separation_v2` | [gamora] |
| player intents | `{reposition 22,758 · advance 960 · hold 572}`, **evade 0** | [gamora] |
| nova firings eaten | **132 / 132**; player never left the 12 m footprint in any window | [gamora] |
| nova fuse | derived at cast from the **target's kit speed**, per-fight-constant: 12.0 / (0.90 × 5.75) = 2.3188 s | [gamora] + [SA-read] |
| boss-fight win rate | **0.00** (30/30 losses, `boss/A`, BEFORE arm) | [banked] `s3` |
| paired M-3 arms | armed positional evade moved nova crossings **66 → 0** (rate 1.00 → 0.00) | [banked] `s7_clause2` |
| boss inter-swing pause | `BOSS_SWING_PAUSE_S = (0.30, 0.40)` — **"M — Primordian, measured"**, drawn per swing on a dedicated seeded RNG sub-stream | [SA-read] |
| boss swing **animation** | **graded CANNOT-ANSWER (EXT-A)** — no M-grade operand exists for the swing's own duration | [SA-read] |
| nova telegraph wind-up | **0.750 s** (45 frames @ 60.000 fps CFR, two independent reads) | [SA-read] |
| actionable window | **0.70 s** (charter §8.6, M) · reaction latency default **0.30 s** | [SA-read] |

**Three structural facts that shape the whole build.**

- **`commit_state` is a `SpatialEntity` field with default `"idle"`, and it is only ever *written* for
  the player** [SA-read]. The mob navigation phase consults no attack or cast state [gamora]. So the
  boss's 76,714/76,714 idle is not a missing field — it is a machine that was never given a mob-side
  consumer, on a fixture kit that carries no commitment packet. **C2 is a second consumer of an
  existing pattern, not a new architecture.**
- **`commit_state` is already emitted on the per-frame entity block, for every entity** [SA-read].
  Therefore **stage 1 requires NO replica-frame schema change**: gate G2's commit-attribution join
  is computable from frames the emitter already writes. (The schema amendment R-WR3-10(b) names is
  K2-prep and stays out of scope — §7.)
- **The E4 pattern changes no stat.** It produces a per-tick scalar applied at the read site, leaving
  `entity.movement_speed` untouched [gamora §1.5]. C2 **must** inherit this, and §3.5 states why it
  is mandatory rather than merely tidy.

---

## §2 — MECHANISM K — player kite / evade

**Ratified rule (R-WR3-7 / K-1):** *the kite intent fires on (i) telegraph events **and** (ii) a
sustained-pressure rhythm heuristic.* K is therefore **two limbs**, and they are deliberately
asymmetric in cost: one already exists.

### 2.1 K-T1 — the telegraph limb is an ARMING change, not new policy

The M-3 `piloted_competence` telegraph-response policy already implements limb (i) completely: it
reads the earliest pending ring, applies `t_eff = min(t_remaining, 0.70) − reaction_latency`, budgets
`movement_speed × t_eff`, generates candidates over four headings plus the payload-band shelf points,
scores each by the resolver's own `nova_expected_delivered`, and returns the argmin or a HOLD
[SA-read]. It is pure, RNG-free, unit-tested, and it holds R-M3-1 by construction.

> **K-T1 = arm the existing limb on the battery-of-record path. Write no new evade math.**

Rewriting it would be a second implementation of a payload law — the exact defect R-M3-1 forbids.
This is a large scope reduction and it is the honest reading of the ratified rule.

**Preserved verbatim from M-3, because each is load-bearing and none is incidental:**

- **The limb OWNS the tick whenever a telegraph is live** — on EVADE *and* on HOLD. A HOLD must not
  fall through to the advance branch. M-3's SS-M12b-5 records the observed artifact when it did: the
  pilot evaded to its optimum and then sprinted back during the final reaction window, arriving at a
  worse radius than it started. *A pilot that undoes its own read is not a competent pilot.*
- **It scores payload, never distance.** The nova's exposure profile is a step function with cliffs
  at 2.5 m and 9.0 m; distance-greedy is not merely suboptimal, across a cliff it is actively
  harmful (+40 % / +32 % delivered in M-3's own worked cases).
- **A locked player cannot evade.** `_f8_move_locked` or `move_scale ≤ 0` returns HOLD-LOCKED. The
  nova's own `action_lock` is the mechanic's structural counter — the CC answers the read. Keep it.
- **No teleport.** The policy names a target *point*; the engine walks toward it at the same
  `movement_speed · dt · move_scale` chain every other player motion uses.
- **Evade costs the action slot** (`_m3_evaded_this_tick`). See §2.5.

**Predicted behaviour, stated so it is not mistaken for a surprise.** At nova onset the player sits
10.209 m from the ring origin [gamora] with a 12.0 m footprint. Budget = 5.75 × (0.70 − 0.30) =
**2.30 m**; the shelf candidate `projectile_distance_m + ε` = 12.01 m sits **1.80 m** away, inside
budget on the first decision. The limb clears the footprint in roughly four ticks — which is exactly
what the banked paired arms measured (`evade_ticks` 264 over 66 firings = 4.0/firing, crossings
66 → 0) [banked]. **G3 will pass, and §8.2 flags what that means for G3 as a gate.**

### 2.2 K-T2 — the rhythm limb (new)

Limb (ii) is what unpins the 2.000 m median in the long stretches where no ring is in the air — which
is most of the fight, and *all* of the 48 boss fights that fire no nova at all [gamora §6.1].

K-T2 has **two sub-triggers**, and they answer different failure modes.

#### K-T2a — commit-reactive (the primary; the direct instantiation of R-WR3-5)

R-WR3-5's sharpest fact: the referent boss was **faster** than the player and Matt still kited it —
the windows came entirely from attack-commit, never from outrunning. K-T2a is that sentence made
mechanical.

> **Trigger:** the focused target's `commit_state`, **as seen through the delayed-observation buffer
> (§2.3)**, is `windup` or `recovery`.
> **Effect:** the player enters a kite bout for as long as that state holds (plus the release
> conditions of §2.4).

This is the K↔C2 coupling, and it is the reason the two mechanisms must ship in the same stage:
C2 manufactures the windows, K spends them. Neither alone moves the geometry.

#### K-T2b — pressure-reactive (the safety valve; what "rhythmically, not only on telegraphs" buys)

If the boss's commit duty cycle is tight, K-T2a alone leaves the player pinned. K-T2b fires on
accumulated contact regardless of commit state.

**State (per player, per fight; no RNG, no allocation on the non-contact path):**

```
contact_timer_s  += dt                       while  separation <= C_reach
contact_timer_s  -= dt * CONTACT_DECAY_MULT  while  separation >  C_reach     (floored at 0.0)
```

> **Trigger:** `contact_timer_s >= PRESSURE_THRESHOLD_S` **[CAL-K2]**.
> **On bout entry:** `contact_timer_s := 0.0` — **not** `:= threshold`. This is the anti-chatter
> rule: the next bout requires a fresh accrual, so a yield cannot immediately re-trigger. It is
> SS-M12b-5's "does not undo its own read" law, transposed from the telegraph limb.

#### Precedence inside K

`K-T1 > K-T2a > K-T2b`. A live telegraph preempts a commit bout preempts a pressure bout. The
enum-level precedence `EVADE > REPOSITION > ADVANCE > HOLD` is **FROZEN and unchanged** — K adds a
third claimant on the EVADE branch, and that is:

> **⚠ SEMANTIC SHIFT SS-K-1 (NAMED).** `MovementIntent.EVADE` acquires a second producer. Until now
> `evade` in a decision trace meant "the M-3 limb fired" — the WR2 clause-2 instrument relies on
> exactly that, verbatim: *"`evade` is UNIQUE to the M-3 limb"* [SA-read]. After K it is not.
> **Obligation on the build:** the decision record must carry a limb discriminator (`evade:tg` /
> `evade:commit` / `evade:pressure`) or every downstream instrument that read `evade` as an M-3
> witness silently changes meaning. This is the third extension of this enum's consumers; the seam's
> own comments already warn that the prior two made external exhaustive matches non-exhaustive.

### 2.3 The human constraint — ONE mechanism, applied ONCE

R-WR3-11(c) fixes the 0.30 s reaction delay as fast-competent-human by validated precedent (DeepMind
FTW: agents 258 ms vs humans 559 ms; injected-delay handicapping is the established human-likeness
lever). The spec implements it as a **delayed-observation buffer**, not as scattered timer checks:

> The env maintains a ring buffer of per-tick observation vectors. A policy reading the buffer
> receives the observation as of `elapsed − REACTION_LATENCY_S` **[CAL-K1 = 0.30]**, or the earliest
> available entry before the buffer fills. `REACTION_LATENCY_S = 0.0` reproduces the clairvoyant
> ceiling arm, exactly as M-3's `latency_floor_ok` already contemplates (floor: one tick; `0.0`
> legal and explicitly reported).

Why a buffer rather than per-trigger latency arithmetic: it applies the handicap **once, for every
observable, for every present and future policy** — including any learned policy landed later behind
the §4 adapter, which then inherits the handicap for free rather than needing it re-imposed.

> **⚠ LATENCY IS APPLIED EXACTLY ONCE. NAMED, because double-application is the obvious defect.**
> K-T1's latency is applied *inside* `evade_decision` as the `− reaction_latency_s` term of `t_eff`.
> **K-T1 therefore reads the LIVE ring state, not the delayed buffer** — its existing behaviour is
> preserved byte-for-byte. K-T2 and the §4 observation contract apply latency via the buffer and
> perform no further subtraction. Unifying the two is a stage-2+ item, explicitly not this build.

**The actionable window** (0.70 s, M-graded) stays a **budget horizon** on K-T1 only — it is
`min(t_remaining, 0.70)`, a ceiling on how far ahead the pilot plans, and it is not a re-plan rate.
K-T2 gets its own optional re-plan floor `DECISION_HOLD_S` **[CAL-K6]**, whose stage-1 value is one
tick (0.1 s), i.e. **inert**: the parameter exists so stage 2 can raise it without a code change, and
it changes nothing at its stage-1 value. Stated rather than smuggled.

### 2.4 The evade vector, and when K yields back

**K-T1's target selection is unchanged** (payload argmin over the M-3 candidate set).

**K-T2's target selection** cannot reuse it: there is no payload function for a melee swing, and
inventing one would be a second implementation of damage. But the contact threat *is* a step function
— zero outside `C_reach`, full inside it — so the honest score is the same *shape* as M-3's, keyed on
the one boundary that exists. The two limbs are one method with different bands:

```
budget      = movement_speed * dt * move_scale            (ONE TICK — K-T2 walks, it does not waypoint)
headings    = [ away-from-focus (the ray focus->player), the two lateral tangents ]
candidates  = { here } U { here + h * budget*k/N : h in headings, k = 1..N }         N = 8, deterministic
            U { the shelf point at radius C_reach + eps from the focus, if within budget }
filter      : reject any candidate that ENDS inside another alive hostile's C_reach
              when the current position is OUTSIDE it   (do not kite into the pack)
clamp       : arena_clamp applied, then reachability RE-VERIFIED   (a clamped candidate is a
              different point; this is also what stops the arena wall becoming a teleport)
score       : projected separation from the focused target at tick end
select      : argmax, STRICTLY better only — ties keep the incumbent (never move for free)
```

The shelf point is included for the same reason M-3 includes its band shelves: **a uniform sampler
straddles the boundary where the threat function jumps and misses the optimum.** It is a *sampling*
rule and receives no scoring privilege.

**Yield conditions — K-T2 returns the tick to the frozen precedence when ANY fires:**

1. `bout_duration >= KITE_BOUT_MAX_S` **[CAL-K3]** — uptime cannot be surrendered indefinitely.
2. `separation >= KITE_RELEASE_M` **[CAL-K5]** — daylight achieved; re-engage.
3. (K-T2a only) the focused target's delayed `commit_state` leaves `windup`/`recovery` **AND**
   `bout_duration >= KITE_BOUT_MIN_S` **[CAL-K7]** — the minimum prevents a one-tick flicker at a
   state edge.
4. The player is locked (`move_scale <= 0` or F8 hard-CC) — **the lock answers the kite exactly as it
   answers the M-3 dodge.** Preserved verbatim; it is the mechanic's structural counter.
5. A telegraph goes live → K-T1 preempts.

On yield, `contact_timer_s := 0.0` (§2.2). The classifier then falls through unchanged to
REPOSITION / ADVANCE / HOLD.

### 2.5 K costs uptime — the single most load-bearing balance property of this mechanism

**K-T2 evade ticks CLAIM THE ACTION SLOT, exactly as M-3's do.** Kiting costs damage.

Without this clause K is a pure win — free distance at no cost — and stage 2 would then calibrate
player DPS against a fight in which the player never pays for its positioning. That is the shape of
a fixture that balances a lie.

> **Consequence, stated now so it is not misread as a gate failure later: stage-1 boss win rate is
> predicted to FALL or hold at 0.00.** The player already sits at ~250 HP/s against a 310–620 band
> [charter §3] and loses 30/30 [banked]; K removes uptime on top of that. **Stage 1's gates are
> geometry gates, correctly so** (charter §4). The R-WR3-2 majority-win-rate acceptance belongs to
> stage 2, after the DPS row is calibrated toward band. A stage-1 win-rate drop is the mechanism
> working, not the mechanism failing. §8.3 asks the conductor to confirm this reading.

### 2.6 The classifier's new inputs — stated explicitly, because it is a pure function

gamora's warning is correct and this spec honours it. `movement_intent(...)` is today a pure function
of `(distance_to_target, min_attack_range, move_scale, band_outer)` and returns nothing else. K adds
**one** parameter carrying a frozen, engine-handle-free value object:

```python
movement_intent(
    distance_to_target: float,
    min_attack_range: float,
    move_scale: float,
    *,
    band_outer: float | None = None,
    kite: KiteInput | None = None,      # WR3 Mechanism K. None => byte-identical legacy classifier.
) -> MovementIntent


@dataclass(frozen=True)
class KiteInput:
    """Everything the kite predicate needs. Pure values only: no entity, no engine, no callable
    that closes over engine state. The classifier must remain unit-testable on a grid."""
    telegraph_live:        bool     # a ring is pending (K-T1 owns the tick; the classifier defers)
    focus_commit_state:    str      # DELAYED view: "idle" | "windup" | "strike" | "recovery"
    contact_pressure_s:    float    # the K-T2b accumulator
    pressure_threshold_s:  float    # [CAL-K2]
    in_bout:               bool     # hysteresis latch, engine-held
    bout_elapsed_s:        float
    bout_min_s:            float    # [CAL-K7]
    bout_max_s:            float    # [CAL-K3]
    separation_m:          float
    release_m:             float    # [CAL-K5]
```

`kite is None` is the legacy classifier, byte-identical — the same default-inert shape
`band_outer=None` already uses.

**Unit-test obligation (the Cell-C precedent, and it is not optional):** the engine INLINES this
predicate at its player-movement phase rather than calling it [SA-read]. Cell B's HALT was a
transcription defect of exactly that shape. Pin the declared law and its transcription against each
other with a **grid-equivalence test** over the full cross product of
`{telegraph_live} × {commit_state} × {pressure above/below} × {in_bout} × {separation bands} ×
{move_scale 0, >0}`. Do not trust them to agree.

### 2.7 Arming

K lands behind a new engine flag `kite_policy_v1: bool = False`, **default OFF**, armed by the WR3
battery-of-record only — the same default-off shape `movement_policy_v2` and `piloted_competence`
already use. It is **not** armed by production content paths, generation, or the balance loop.
**§8.1 flags the canon question this raises and asks the conductor to rule it.**

---

## §3 — MECHANISM C2 — boss attack-commit

**Ratified rule (R-WR3-7 / C2-1):** *wind-up + short recovery — GD-style animation lock on both sides
of the swing. The recovery is where the referent's kite windows lived.*

### 3.1 Where it lives

The E4 commitment state machine is the natural home and the correct precedent: it produces a per-tick
scalar applied at the read site and writes no stat [gamora §1.5]. C2 extends the same pattern to the
mob side. Two pieces are missing today and both are small:

- **the consumer** — the mob navigation phase consults no attack state [gamora];
- **the packet** — the fixture boss's melee skill carries no commitment fields, so `read_commitment`
  parses it to EXEMPT (`bin=None`) and the machine could never leave idle even if called [SA-read].

### 3.2 The states

| state | enter on | duration | exit to | mob `_c2_move_scale` | may the swing land? |
|---|---|---|---|---|---|
| `idle` | fight start; `recovery` expiry | — | `windup`, on attack initiation | **1.0** (full pursuit, unchanged) | — |
| `windup` | target within `range_m + target.entity_radius` **AND** skill off cooldown | `WINDUP_S` **[CAL-C1]** | `strike` | `WINDUP_MOVE_SCALE` **[CAL-C3]** | no |
| `strike` | `windup` expiry | exactly **one tick** (the resolution tick; fixed, not [CAL]) | `recovery` | **0.0** | **YES — damage resolves here** |
| `recovery` | `strike` completion | `RECOVERY_S` **[CAL-C2]** | `idle` | `RECOVERY_MOVE_SCALE` **[CAL-C4]** | no |

**Two laws, and the first is the mechanism.**

> **C2-L1 — THE STRIKE RESOLVES AGAINST LIVE GEOMETRY AND MISSES.** At the strike tick the swing
> tests separation against `range_m + target.entity_radius` **as it is at that moment**, and delivers
> nothing if the target has left. This is inherited directly from E4's player-side wind-up semantic
> ("resolve-at-completion, motion-whiff") [SA-read].
>
> **If the swing auto-hits at strike regardless of separation, kiting is cosmetic and this entire run
> measures nothing.** C2-L1 is what converts a wind-up into a kite window. It is the single clause
> whose omission would silently void gates G1 and G2.

> **C2-L2 — THE BOSS COMMITS AT WINDUP ENTRY AND DOES NOT RE-AIM.** No re-target, no re-solve of the
> strike geometry during `windup`. A boss that re-aims mid-commit has not committed, and the player's
> read cannot be rewarded. (GD's own behaviour; the Souls-family convention; and the necessary
> counterpart to C2-L1 — without it the whiff is unreachable.)

### 3.3 The packet, and the one additive field

C2 reads its durations through the **existing** `read_commitment(skill)` — honouring the E4 contract's
own rule that emitted constants are consumed AS-EMITTED and never re-derived. The fixture authors a
commitment packet onto the boss melee skill (`commitment_bin: "wind-up"`, `cast_time: WINDUP_S`).

E4 has **no recovery concept** (its machine is `idle → committing → resolve`). C2 needs one:

> **⚠ SEMANTIC SHIFT SS-C2-1 (NAMED).** `Commitment` gains `recovery_s: float`, parsed with the same
> `.get`-based read every other field uses. **A packet without the field parses to `0.0`, which is
> byte-identical for every existing player-side consumer** — the shift is additive and default-inert.
> §8.5 flags the cross-seam routing question: the E4 packet's emitter half is rocket's, and whether a
> new field on the shared dataclass needs an emitter-side MIGRATION is knight-rider's call, not this
> spec's.

### 3.4 Initial values, and the reasoning that produces them

The GD envelope's commit/telegraph-rhythm row is the operand set, and its honest grading matters:

- **The swing *animation* is graded CANNOT-ANSWER (EXT-A)** [SA-read]. There is no M-grade operand
  for the basic swing's own duration. Any `WINDUP_S` is therefore **[CAL] by necessity**, not by
  laziness — and it must be anchored to something measured rather than invented.
- **The measured anchors that DO exist:** the Primordian's inter-swing pause **0.30–0.40 s**
  ("M — Primordian, measured", EXT-B) [SA-read], and the signature-heavy nova wind-up **0.750 s**
  (45 frames @ 60 fps, two reads) [SA-read].

**Derivation.**

1. **`WINDUP_S = 0.35` [CAL-C1].** The mean of the referent boss's own measured dead-time quantum
   (0.30–0.40). It is 2.14× shorter than the measured signature heavy (0.750 s), which preserves the
   heavy-vs-basic distinction — if the basic swing's wind-up approached the nova's, the telegraphed
   heavy would stop reading as heavy and the fight would lose its rhythm hierarchy.
2. **`RECOVERY_S = 0.25` [CAL-C2],** from the kite-window arithmetic, which is the thing the value
   has to buy. With the boss fully locked and the player retreating from the body floor:

   ```
   T_lock   = WINDUP_S + RECOVERY_S                       = 0.60 s
   usable   = T_lock - REACTION_LATENCY_S (0.30)          = 0.30 s
   daylight = player_speed 5.75 * usable                  = 1.725 m
   ```

   Separation goes 2.000 → 3.725 m, clearing `C_reach` 2.5 m after only 0.087 s of retreat. Post-lock
   the boss re-closes 1.225 m at 4.025 m/s = 0.304 s, plus the player's own release lag — giving a
   window on the order of **0.9 s**, comfortably above G2's `W_MIN_TICKS` floor.

   The binding constraint, stated as the floor these values clear: a window can only exist at all if
   `5.75 × (T_lock − 0.30) ≥ 0.5 m`, i.e. **`T_lock ≥ 0.387 s`**. Below that the mechanism is
   built and inert, and G1/G2 fail for a reason that is arithmetic rather than behavioural. `0.60`
   sits 1.55× above the floor deliberately — stage 1 is proving the geometry exists, not tuning it.
3. **`WINDUP_MOVE_SCALE = 0.0` and `RECOVERY_MOVE_SCALE = 0.0` [CAL-C3 / C4].** Full lock on both
   sides. R-WR3-5's fact is that the referent boss was *faster* than the player and the fight still
   worked — which is only possible if the lock, not the speed, made the windows. A partial scale
   would be tuning at a stage that has not yet established the effect exists.

**The duty cycle is NOT specified here, and §8.6 says why that is a pre-build gate rather than an
omission.** C2 changes no attack cadence: the free time between swings remains governed by the
existing `cooldown_seconds` + the seeded `gd_swing_pause` draw. If `T_lock` turns out to be a large
fraction of the realized swing cycle, the boss is locked for most of the fight and the encounter
inverts from unwinnable to trivial — which would corrupt stage 2 in the opposite direction.

### 3.5 The scalar pattern is MANDATORY, not stylistic — three invariants depend on it

C2 multiplies the mob's per-tick displacement by `_c2_move_scale(mob)` at its single step site and
**never writes `entity.movement_speed`.** A C2 that wrote the field instead would break, silently:

1. **The M-3 pilot floor's forward-integration**, which reads `target.movement_speed` to project the
   target's position over a cast window [SA-read] — it would project a frozen boss and mis-place
   every wind-up decision.
2. **The mob motion model** shared between the projection and the world (a projection/resolution
   split biases the estimate — the reason the pilot floor re-uses the same function).
3. **The `u` utilization instrument** the F-WR2-5 diagnostic is built on, whose denominator is
   `v_boss · dt`.

**And the fuse law is untouched either way, by construction.** The nova fuse is derived at cast from
the *target's* kit speed [gamora §2.2(1)] — the player's, not the boss's. Neither K (which moves the
player to a target point at the existing speed) nor C2 (which scales the boss's realized step) writes
any entity's `movement_speed`. **Therefore S-7's `movement_speed_ms` join key is invariant across
this build.** That is not a hope; it is the structural argument G4 tests, and §5's G4 row states the
consequence: if S-7 moves, the mechanism was built wrong.

### 3.6 Scope: boss tier only

The charter names the mechanism *"boss attack-commit"* (§4). C2 applies to entities carrying
`is_boss` in stage 1. This follows the charter's own naming, minimizes the diff against the frozen
BEFORE arm, and keeps trash/champion/mixed-pack legs comparable — which G4's S-1/S-2 rows require.
Generalizing to all mob tiers is a later question and is fenced in §7.

---

## §4 — THE ENV-INTERFACE CONTRACT (R-WR3-9 + R-WR3-11(a))

**Ruling restated:** duck-typed Gymnasium compatibility, **zero new dependency**. The sim core exposes
`reset` / `step` with exact signatures in plain Python values. A thin `GymEnvAdapter` and `gymnasium`
itself land later behind an optional `[rl]` extra. **The 450-trace battery hot path imports no RL
package, ever** — the gate chain stays pure-Python and diffable, and no non-diffable weights artifact
can enter a gate.

### 4.1 Signatures (exact)

```python
def reset(self, *, seed: int | None = None, options: dict | None = None) -> tuple[Obs, dict]: ...
def step(self, action: int) -> tuple[Obs, float, bool, bool, dict]: ...
```

- `seed` sets the fight seed. `options` carries `{leg, arm, scenario, mitigation_regime, flags}`.
- Returns `(obs, info)` from `reset`; `(obs, reward, terminated, truncated, info)` from `step`.
- `terminated` — the fight resolved (a winner exists). `truncated` — tick cap / timeout.
- **`reward` is a STUB returning `0.0` in stage 1. Stated explicitly.** There is no reward function
  to write yet: R-WR3-11(b) banks preference-comparison learning as the named stage-3 candidate, and
  inventing a hand-authored reward now would prejudge it. The channel exists so the shape is right.
- `step` consumes **no RNG beyond the engine's existing seeded streams**. The adapter introduces no
  sampling. G5 depends on this.

### 4.2 `Obs` — a frozen-order tuple of plain floats

`Obs` is a `tuple[float, ...]` of fixed length with a frozen index order (below). A `to_numpy()`
helper ships **in the `[rl]` extra only**, importing numpy lazily — so the contract itself carries
zero dependency, not merely no *new* one.

**Every observation is read through the delayed buffer (§2.3), except K-T1's live-ring read.**

| idx | name | units / range | note |
|---|---|---|---|
| 0 | `self_hp_frac` | [0,1] | `hp / max_hp` against the **CURRENT** pool, per R-WR3-8(a) |
| 1 | `self_energy_frac` | [0,1] | |
| 2 | `self_move_scale` | [0,1] | the E4/F8 product; `0.0` = locked |
| 3 | `focus_dist_m` | m | separation to the focused target |
| 4 | `focus_dist_norm` | [0,1] | `dist / C_reach`, clipped — scale-free |
| 5 | `focus_hp_frac` | [0,1] | CURRENT pool |
| 6 | `focus_in_reach` | {0,1} | `dist <= C_reach` |
| 7–10 | `focus_commit_onehot` | {0,1}⁴ | `idle` / `windup` / `strike` / `recovery` — **C2's output; the observable that makes kiting possible** |
| 11 | `focus_commit_t_remaining_s` | s | time left in the current commit state — **§8.4 flags the clairvoyance fork** |
| 12 | `telegraph_live` | {0,1} | an unlaunched ring exists |
| 13 | `telegraph_t_remaining_s` | s | `t_launch − elapsed` |
| 14 | `telegraph_r_norm` | — | `r_player / projectile_distance_m` |
| 15 | `telegraph_payload_now_norm` | [0,1] | `nova_expected_delivered(r) / max_hp` — **calls the resolver's own function**, R-M3-1 |
| 16 | `contact_pressure_norm` | [0,1] | `contact_timer_s / PRESSURE_THRESHOLD_S`, clipped — K-T2b's state, exposed |
| 17..20 | `skill_ready[i]` | {0,1} | `skill_cooldowns[i] <= 0`, **fixed width 4**; absent slots emit `0.0` |
| 21 | `n_hostiles_in_reach_norm` | [0,1] | count in `C_reach` / a declared cap |
| 22 | `arena_edge_dist_norm` | [0,1] | so the policy can know it is being cornered |

**Fixed width is part of the contract.** A variable-length observation is not a Gymnasium observation
space, and a policy trained on one width cannot read another. Widening appends; it never inserts.

### 4.3 Action space

`Discrete(4)` over `MovementIntent`, in **declaration order**, frozen:

```
0 = ADVANCE   1 = HOLD   2 = EVADE   3 = REPOSITION
```

> **⚠ TRAP, NAMED.** The index IS the enum's declaration order. Adding a member must **APPEND**.
> An inserted member silently re-maps every previously-recorded action index — a defect that produces
> no error and no diff, only wrong behaviour. Declare the mapping as a frozen table in the adapter
> and unit-test it against the enum, so the enum cannot drift out from under it.

### 4.4 What stage 1 ships

**The contract, not the adapter.** Stage 1 delivers the `reset`/`step` surface, the frozen `Obs`
order, the frozen action mapping, and the delayed-observation buffer. `GymEnvAdapter`, the `[rl]`
extra, and any training stack are **out of scope (§7)**.

---

## §5 — PRE-REGISTERED GATES

Charter §4's stage-1 gates, reproduced and extended with exact computable definitions.
**§8.38 is law here: every pre-registered column NAMES its computing cell.**

**Computing cell of record:** `simulation/wr3_cell_kc_2026_07_30.py`, following the
`wr2_cell_bat_2026_07_29.py` precedent. It **imports** the WR2 instruments by module — `CB.s1_scan_dir`,
`CC.s2_scan_battery`, `CC.s3_outcomes`, `wr2_cell_bat.s7_clause1` — and the two F-WR2-5 diagnostic
instruments (`wr2_f5_pursuit.py`, `wr2_f5_kite_onsets.py`), **verbatim, never by copy**, so BEFORE and
AFTER are the same measurement rather than two similar ones.

**BEFORE arm:** the frozen `output/kitcal_g5/wr2_battery_after/`. **No regeneration.** Any comparison
that regenerates the BEFORE arm is void, and the cell must assert the root's identity before reading.

**AFTER arm:** a full battery at the same seeds/legs/argv plus `--kite-policy-v1 --boss-commit-v1`.

| gate | predicate | statistic + threshold | BEFORE value | computing cell |
|---|---|---|---|---|
| **G1** | separation UNPINS from the 2.000 m floor | **(a)** `median_of(per-fight median separation) >= 2.000 + Δ`, `Δ` = **[CAL-G1, 0.25 m]`**; **AND (b)** `count(fights with per-fight median == 2.000 ± 1e-6) <= ` **[CAL-G2, 90 of 180]**. Reported beside, not graded: per-fight `P25`, `frac_ticks_within_C_body+1cm`, `frac_ticks_inside_melee_gate` | median-of-medians **2.000**; degenerate count **180/180**; 0.921; 0.953 | `wr3_cell_kc.g1_separation()` — `wr2_f5_pursuit.py` separation instrument, verbatim, over all boss traces |
| **G2** | ≥1 **conceded** kite window per boss fight beyond the opening charge | **window** := a maximal run of `>= W_MIN_TICKS` **[CAL-G3, 3 ticks = 0.3 s]** contiguous ticks with `separation > C_reach (2.5 m)`, onset `> 1.5 s` (excludes the measured mutual charge, which closes at t = 1.4–1.5 s in all 180). **conceded** := the focused boss is in `windup` or `recovery` for `>= 50 %` of the window's ticks. **PASS:** `windows_conceded >= 1` in `>=` **[CAL-G4, 90 %]** of boss fights. Both `windows_post_charge` (any) and `windows_conceded` reported | **0/180 conceded** — by construction: `commit_state` idle 76,714/76,714, so no window can be commit-attributed. (Any-windows BEFORE: 1.267/fight, all opening-charge or player-initiated) | `wr3_cell_kc.g2_kite_windows()` — `wr2_f5_kite_onsets.py` run-detector, extended with the **per-frame `commit_state` join, which needs no schema change** |
| **G3** | production telegraph-escape rate > 0 | **G3a (GRADED, positional, conflation-free):** per firing, `player_max_r_from_origin_m` over `[onset, realized delivery]`; **ESCAPED iff `> projectile_distance_m` (12.0)**. PASS: `escaped >= 1`. **G3b (REPORTED, not graded):** `crossings / firings`, the S-7 clause-2 GRADED denominator, carrying its banked caveat **verbatim** — `non_delivering` conflates "the player escaped the footprint" with "the ring's spokes missed" | **0 of 132** escaped (G3a); crossings/firings **1.00** (G3b) | `wr3_cell_kc.g3_escape()` — positional rows recomputed from frames; `s7_clause1` imported verbatim. **§8.2 flags that this gate cannot fail informatively** |
| **G4** | no S-1 / S-2 / S-7 regression vs the FROZEN WR2 battery | **S-1:** `violations == 0` **AND** `worst_slack_m >= −0.01` (declared tol). **S-2:** weapon-DoT lift direction preserved; anchor grain `207.40` / `worst_drop_abs 414.80` unchanged. **S-7 cl.1:** `assessable == firings` (completeness) **AND** `worst_ratio_to_bound <= 1.0` **AND** the frozen margin identity `ratio_to_bound == 1 − d_onset/radius_m` holds | S-1: 450 traces / 292,305 pair samples / **0** violations / worst slack **−0.000989 m**. S-7 cl.1 worst ratio **0.149** | `wr3_cell_kc.g4_regression()` — `CB.s1_scan_dir`, `CC.s2_scan_battery`, `wr2_cell_bat.s7_clause1`, all imported. **Structural expectation (§3.5): S-7 is invariant by construction, because no entity's `movement_speed` is written. If S-7 moves, the mechanism was built wrong — this row is a tripwire on the implementation, not a test of the design** |
| **G5** | determinism — same seed, byte-identical | Two full battery runs, identical seeds + argv, different out-dirs; byte-compare every trace. PASS: `differed == 0` over all legs (BEFORE instrument: 150 traces/leg, `S4_PASS`). **Plus:** K's classifier and C2's transition function are **pure and RNG-free**, unit-tested on the §2.6 grid. C2 adds **no** RNG draw — the existing seeded `gd_swing_pause` sub-stream is unchanged | 150 matched / **0** differed / `S4_PASS: true` | `wr3_cell_kc.g5_determinism()` — the banked `determinism` instrument shape, reused |

### 5.1 Honorable fallback (desirable-run pattern) — a FAIL is processable, with one asymmetry

> **G1 / G2 / G3 FAIL → a processable FINDING, not a terminal event.**
>
> - **G1 or G2 fail:** the mechanism is built but the parameters are wrong. Routes to **one** bounded
>   [CAL] sweep whose bracket is **pre-registered here, now**, so firing it is not goalpost motion:
>   `WINDUP_S ∈ {0.25, 0.35, 0.50}` × `RECOVERY_S ∈ {0.15, 0.25, 0.40}`, nine cells, one lap.
>   **The sweep does not fire without a conductor ruling.** If the whole bracket fails, that is a
>   finding about the fixture's duty cycle (§8.6), not about K or C2, and it escalates.
> - **G3 fails:** F-WR2-4's regime is genuinely unreachable in production. That is a finding about
>   the fixture and it escalates to the conductor — it does not get tuned around.
>
> **G4 / G5 FAIL → BLOCK. HALT and report.** A regression or a determinism break is not a finding;
> it is a build defect. The asymmetry is deliberate: G1–G3 measure whether the design is *right*,
> G4–G5 measure whether the build is *correct*, and only the first question is allowed to have a
> surprising answer.

---

## §6 — [CAL] PARAMETER REGISTER — 15 parameters, all stage-2-owned

Every value below is a stage-1 **initial** value chosen to be defensible, not correct. Stage 2 owns
them all. No value here is a fixture measurement, and none may be cited as one.

| # | parameter | stage-1 value | reasoning | owner |
|---|---|---|---|---|
| **CAL-K1** | `REACTION_LATENCY_S` | 0.30 s | R-WR3-11(c): fast-competent-human **by validated precedent** (DeepMind FTW 258 ms agent / 559 ms human; injected-delay handicapping). No ARPG-telegraph measurement exists in the literature. **If stage 2 wants it numerically, it gets measured from Matt** (ledgered R-WR3-11(c)) | stage 2 |
| **CAL-K2** | `PRESSURE_THRESHOLD_S` | 2.00 s | ≈3.3× the C2 lock cycle: K-T2b is the safety valve, so it must not fire before K-T2a has had ~3 chances to work | stage 2 |
| **CAL-K3** | `KITE_BOUT_MAX_S` | 1.50 s | the measured BEFORE any-window duration ceiling (1.5 s, n=228) — the fight's own demonstrated daylight quantum | stage 2 |
| **CAL-K4** | `CONTACT_DECAY_MULT` | 1.0 | symmetric decay; the neutral prior. Asymmetry is a stage-2 lever | stage 2 |
| **CAL-K5** | `KITE_RELEASE_M` | 4.00 m | 1.6× `C_reach`; past it, further retreat buys no safety and only costs uptime | stage 2 |
| **CAL-K6** | `DECISION_HOLD_S` | 0.10 s (one tick) | **INERT at this value** — exists so stage 2 can raise the re-plan floor without a code change | stage 2 |
| **CAL-K7** | `KITE_BOUT_MIN_S` | 0.20 s (2 ticks) | prevents a one-tick flicker at a commit-state edge | stage 2 |
| **CAL-C1** | `WINDUP_S` | 0.35 s | mean of the **measured** Primordian inter-swing pause (0.30–0.40, EXT-B); 2.14× shorter than the measured signature-heavy 0.750 s, preserving the heavy/basic hierarchy. **[CAL] by necessity — the swing animation is graded CANNOT-ANSWER (EXT-A)** | stage 2 |
| **CAL-C2** | `RECOVERY_S` | 0.25 s | §3.4 kite arithmetic: `T_lock` 0.60 s → 1.725 m daylight → ~0.9 s window; sits 1.55× above the `T_lock >= 0.387 s` existence floor | stage 2 |
| **CAL-C3** | `WINDUP_MOVE_SCALE` | 0.0 | full lock — R-WR3-5: the referent boss was faster and the fight still worked, so the lock is the mechanism | stage 2 |
| **CAL-C4** | `RECOVERY_MOVE_SCALE` | 0.0 | as C3; R-WR3-7 names recovery as where the referent's windows lived | stage 2 |
| **CAL-G1** | G1 separation `Δ` | 0.25 m | half the `C_body`→`C_reach` gap (0.5 m): a shift smaller than this cannot open a window | conductor |
| **CAL-G2** | G1 degenerate-median cap | 90 of 180 | half the fights must stop landing on exactly 2.000 m. **The sharper clause of G1** — the degenerate signature's disappearance is the finding, not its magnitude | conductor |
| **CAL-G3** | G2 `W_MIN_TICKS` | 3 ticks (0.3 s) | one reaction latency — a window shorter than a human's reaction is not a window | conductor |
| **CAL-G4** | G2 fight fraction | 90 % | 132 of 180 fights fire a nova; the gate must be satisfiable by commit alone in the 48 that do not | conductor |

**Not [CAL] and not to be treated as such:** `ACTIONABLE_WINDOW_S` 0.70 (M-graded, charter §8.6),
`TELEGRAPH_WIND_UP_S` 0.750 (M, 45 frames), `NOVA_ESCAPE_FRAC` 0.90 (frozen law), `C_body` 2.0 /
`C_reach` 2.5 (fixture geometry), `strike` duration (one tick, structural).

---

## §7 — OUT-OF-SCOPE FENCE

| fenced | ruling |
|---|---|
| **In-fight form-swap (Mechanism K2)** — the swap verb, the two-body atomic rebind, its four pre-code decisions | **R-WR3-10**: own lane, does not fold into K. Scoped CONSTANT-POOL per R-WR3-10(a); HP-carry semantics stay unruled and moot |
| **The replica-frame schema amendment** (pool from header → per-frame block) | **R-WR3-10(b)** — K2-prep, sequenced first **in the K2 lane**. Stage 1 needs no schema change: `commit_state` is already per-frame |
| **The compiled human-form kit** (legolas kit-spec extraction) | **R-WR3-10(c)** — K2's owed input; math-before-code cannot start without it |
| **Envelope calibration: player DPS ↑ toward the 310–620 band** | charter §4 **stage 2** |
| **Nova pool-fraction ↓ toward the ≤34.3 % measured worst** | **R-WR3-7 / CAL-1**, stage 2. **DO NOT TOUCH ANY NOVA NUMBER IN STAGE 1** — the fixture's nova is the BEFORE arm's own constant |
| **R-WR3-2 majority-win-rate acceptance** | charter §4 stage 2, measured separately on boss and full-mix. Stage 1's gates are geometry gates (§2.5) |
| **Learned policies · `GymEnvAdapter` · the `[rl]` extra · SB3 or any training stack** | **R-WR3-9 + R-WR3-11(a)** — stage 1 ships the **contract**, never the adapter. Battery hot path imports no RL package |
| **Preference-comparison reward learning** | **R-WR3-11(b)** — the named **stage-3** candidate; presupposes stage-1 geometry + the adapter |
| **Playstyle-similarity metric** (Lin, arXiv 2508.19152) | **R-WR3-11(d)** — probe ledgered, not fired |
| **C2 generalization to trash / champion tiers** | charter §4 names *"boss attack-commit"*; §3.6 |
| **G-5a HP errata banners · the U-5 `lastHitBy` anomaly** | **R-WR3-3 / R-WR3-6** — legolas follow-on; no decision here leans on 273.704 |
| **The 3-ticks-late ring delivery** (declared `fire_tick` 30, realized 33, 132/132) | charter §8.41 / diagnostic §7.1 — INFO, unruled. Note for the builder: **G3a's window must extend to REALIZED delivery, not declared fire**, or it measures 0.3 s short |

---

## §8 — UNDERDETERMINED BY THE CHARTER — flagged, not ruled

Six items. Each states the fork, a lean where one is defensible, and who must rule.

### 8.1 — The §7.2 canon collision. **The conductor must rule this before the build starts.**

`canonical/reap-die-rise-engine/telegraph-dodge-temporal-decoupling-2026-06-15.md` §7.2 is
Matt-ratified canon, verbatim: *"the dodge is inert in the sim, active in Godot… **Do not let anyone
try to make the sim 'model' the dodge**."* R-M3-2 operationalized it: *"IF THIS ARM EVER DEFAULTS ON,
OR EVER REACHES THE BALANCE LOOP, §7.2 IS VIOLATED"* — which is precisely why M-3 shipped dark.

The charter directs that *"the production policy must start emitting the EVADE intent."* Neither the
charter nor gamora's read raises §7.2, so it arrives here unreconciled.

**The distinction that may resolve it, and it is real rather than convenient.** §7.2's subject is the
**dodge skill** — a kit ability whose value is timing-based and which the autobattle cannot time, so
crediting it would stop the balance loop from walling glass-close-ST. K is **positional movement**:
no skill, no i-frames, no roll, no avoidance stat, no chance term. M-3's own header already draws
this line ("*It is POSITIONAL, not statistical*") — and then kept the arm dark anyway.

**Proposed resolution (lean):** K arms under `kite_policy_v1`, **default OFF**, set by the WR3
battery-of-record only and by nothing in the balance loop, generation, or production content. Under
that fence §7.2's actual protection — the balance loop keeps walling dodge-gated coordinates — is
untouched, and "production" is read in the WR2/WR3 sense the charter uses it (the battery's
flags-on arm, as against the M-3 calibration arm).

**But this is a canon question, not a spec question, and I decline to rule it.** Note also that this
would be the **third** default-off flag on the same movement code path (`piloted_competence`,
`movement_policy_v2`, `kite_policy_v1`), and the arm-combinatorics are themselves becoming a finding.

### 8.2 — G3 as written cannot fail informatively

The banked paired arms already measured an armed positional evade against this exact fixture:
crossings **66 → 0**, rate **1.00 → 0.00** [banked]. §2.1's shelf arithmetic explains it — the escape
point is 1.80 m away against a 2.30 m first-decision budget. G3's `> 0` predicate is therefore
near-certain to pass and carries almost no information.

The informative question is the **two-sided** one: does the escape rate go **total**? A player who
escapes 132/132 has made the nova inert, which collides directly with stage 2's CAL-1 nova
calibration — you cannot calibrate a heavy the player never eats.

**Handled as follows:** G3 is reproduced **as the charter wrote it** (charter is law here), and the
cell computes `escape_rate = escaped / firings` as a **reported diagnostic column beside it**, not as
a gate. **Recommendation, for the conductor to rule:** consider a two-sided band on that column at
the stage boundary. I have not imposed one.

### 8.3 — Stage-1 win rate is predicted to fall; confirm the reading

Per §2.5, K costs uptime and the player already loses 30/30 at ~250 HP/s against a 310–620 band. A
stage-1 win-rate drop is the mechanism working. **Confirm that the conductor and the owner-eye
checkpoint both read it that way** before the render is watched, because "the change made it worse"
is the most natural and most wrong reading of that number.

### 8.4 — Should the policy see `focus_commit_t_remaining_s`? (Obs idx 11)

Exposing exact remaining commit time models a player who **knows the animation** — which Matt, at
L13, having fought the thing repeatedly, did. Withholding it models a first encounter.

**Lean: expose it, through the delayed buffer** (so it is known-as-of-0.30 s-ago, not clairvoyant).
This matches the referent experience R-WR3-2 names. **Ruling is the conductor's** — it is a fidelity
question about *which* player is being replicated, not an engineering one.

### 8.5 — Cross-seam routing for `Commitment.recovery_s` (SS-C2-1)

The E4 packet's **emitter** half is rocket's; the sim consumer honours emitted constants AS-EMITTED
and does not re-derive them. Adding `recovery_s` to the shared dataclass is additive and default-inert
for every existing consumer (§3.3) — but whether it needs an emitter-side counterpart and a MIGRATION
is a **cross-seam routing call for knight-rider**, not a spec decision. Flagged so it is not
discovered at Gate 2.

### 8.6 — The duty-cycle measurement is OWED BEFORE THE BUILD. This is the one I would gate on.

C2's `T_lock` (0.60 s initial) is specified without knowing the boss's **realized inter-swing
interval**. The fixture's cadence is `gd_attack_interval(attack_speed, …)` plus a seeded per-swing
pause draw from `BOSS_SWING_PAUSE_S (0.30, 0.40)` [SA-read] — and the realized value over the 180
frozen boss fights is not in any note I hold.

**Why it matters in both directions.** If `T_lock` is a small fraction of the realized cycle, C2
concedes too little and G2 fails on arithmetic rather than on behaviour. If it is a large fraction,
the boss is locked for most of the fight, the encounter inverts from unwinnable to trivial, and
**stage 2 would then calibrate against a broken-easy fixture** — the more expensive failure, because
it is the one that does not announce itself.

**Recommendation:** commission a read-only measurement from gamora over the frozen `wr2_battery_after/`
traces — realized boss attack events per fight, inter-swing interval distribution, and the implied
duty cycle at `T_lock ∈ {0.40, 0.60, 0.90}`. It is cheap (the instrument shape already exists in the
F-WR2-5 support scripts), it consumes no new runs, and it converts CAL-C1/CAL-C2 from defensible to
grounded before a line of code is written. **Math-before-code (Discipline #1) points at exactly this
number.**

---

*Stage-1 mechanism spec v1 — SPEC-AUTHOR (gandalf), commissioned by gandalf RUN-CONDUCTOR.
No production code written. No engine edits. Spec only.*
