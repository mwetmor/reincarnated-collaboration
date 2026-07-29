# M-3 — Dodge-on-tell / evasion policy · design-spec-as-math

**Agent:** gandalf (`SPEC-AUTHOR`) · **Date:** 2026-07-29 · **Run:** WR1-2026-07-28 · **Cell:** WR1-SPEC-M123
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Charter:** §3 M-3 — *"gamora (spec: gandalf — **design
surface**)"* · **Rulings inherited:** R-WR1-9 (windup measured-input; M-3's dodge window derives from
the same measurement) · R-KC1-19a (**sim thinks, Godot renders — no live AI**) · R-KC1-22
**Class:** design-spec (design layer of the math note; gamora authors her own per Discipline #1)
**Builds against:** KC1 **§14.24** (Matt's Primordian WIN — the acceptance fixture, banked from his
hands) · **§14.26** (the symmetry finding) · extraction **E-1.2** range bands · efficacy verdict
§A-8.1 row 2 (N-7 / N-8 / N-9)
**Serves gate:** **G-B winnable half**
**Companion specs:** M-1 (`…-wr1-m1-mitigation-spec.md`) · M-2 (`…-wr1-m2-frigidring-nova-spec.md`)

---

## §0 — FRAMING AUDIT

**Q1 — the question.** Give the sim player a behaviour that converts the death-2 trajectory into
Matt's winning trajectory, using only information a player could actually have.

**Q2 — pre-imposed assumptions.** The brief is sound. Two amendments:

> ### ⚠ FLAG F-1 — M-3 depends on M-2's U-M2-1, and inherits its reversal risk.
> This spec's entire tactical structure — *close, don't back off* — rests on the **single-hit**
> reading of the ring (M-2 §0 F-2 / U-M2-1). If multiple projectiles can strike one target, melee
> is **2.9× worse** than the outer edge and the correct policy inverts to *flee*. The policy is
> written so the inversion is a **config change, not a rewrite** (§3.2's band table is data), but
> the risk must travel with the spec and not be discovered at grading time.

> ### ⚠ FLAG F-2 — M-3 cannot move N-7, and grading it against N-7 would be an instrument error.
> §A-8.1 row 2 lists M-3's evidence as **N-7** (zero-intake encounter fraction: fixture 0.378, sim
> 0.000; target 0.228–0.528), N-8 and N-9. But **N-7 is dominated by trash encounters**, and trash
> mobs have **no telegraphed attacks** — `controller_zombiea01`-class mobs swing on a
> `minSwingPause/maxSwingPause` cadence with no special-attack slot (E-3.4). A human taking **zero**
> damage in 38 % of encounters did it by **killing things before they closed** and by **approach
> control** — mechanisms M-4 (attack speed) and positioning own, not dodge-on-tell.
> **M-3 as scoped moves the BOSS-tier and champion-tier telegraph statistics. It will barely touch
> N-7.** Recorded now so a small N-7 movement is read as *correct scoping*, not as a failed
> mechanism. §6.3 states the disposition.

> ### ⚠ FLAG F-3 — R-KC1-19a is preserved, but a prior design intent is SUPERSEDED.
> `TelegraphSpec`'s own docstring says *"Godot renders + resolves **the dodge** (dispatch 5)."*
> **That intent is superseded here.** M-3 resolves the dodge **in the sim**; the trace records what
> happened; Godot renders it. This is R-KC1-19a honoured (sim thinks, Godot renders) and it is the
> only arrangement compatible with a deterministic replayable baton. The docstring must be amended
> alongside M-2 §4.4(ii)'s HG-2 amendment — **one MIGRATION, both edits.**

**Q3 — what would change the answer.** galadriel's windup measurement. §3.5 shows the measured value
**decides whether the attack has an undodgeable zone at all** — the mechanic's tactical character is
a function of one unmeasured number.

---

## §1 — WHAT THIS MECHANISM IS, AND WHY IT IS A DESIGN SURFACE

§14.26 named the fight's whole drama:

> *"Matt's WIN required evasion — inexpressible. Matt's DEATH required the frigidring nova — also
> inexpressible. Both outcomes of the real boss fight lived in mechanics the sim cannot yet
> express."*

M-2 builds the death. M-3 builds the win. But M-3 is not a transcription of a GD record — **GD has
no "dodge policy" record; the dodge lived in Matt's hands.** So M-3 is authored design constrained
by measured geometry, and the constraint that keeps it honest is stated once, plainly:

> **THE ORACLE PROHIBITION.** The policy may read anything that describes the **DANGER ZONE**. It
> may read nothing that describes the **OUTCOME.** Geometry, timing and band structure are what a
> tell *shows*; resolved damage is what a tell *conceals*. A policy that reads `damage_amount` is
> not evading — it is consulting the answer key, and every win it produces is counterfeit.

---

## §2 — THE POLICY'S INFORMATION SET (BINDING)

### 2.1 KNOWS — read at the telegraph announce instant

| Source | Fields |
|---|---|
| the `telegraph` event (M-2 §4.2, emitted at `t_announce`) | `attack_id`, `attacker_id`, `skill_idx`, `fire_t_s`, `wind_up_s`, `shape`, `origin_x_m`/`origin_y_m`, `radius_m`, and M-2 §4.4(iii)'s additive ring fields — `ring_thickness_m`, `ring_gapless_radius_m`, **`ring_band_scales`** |
| self | own position, own `movement_speed`, own move-lock / slow state |
| declared config | `threat_profile` — a **static, pre-registered** per-attack-class band table (§3.2). "This player has fought this boss before." Auditable; cannot see a roll |

### 2.2 DOES NOT KNOW — enumerated, and each must be unreachable by construction

- **`damage_amount`.** No magnitude-gated "is this one worth dodging."
- **Any attack not yet announced.** No lookahead past the current telegraph window.
- **The attacker's intent, target selection, next skill, cooldowns, or `nova_chance` roll.**
- **Any HP** other than its own; no fight-outcome, no seed, no future tick.
- **Its own post-mitigation intake.** The policy never learns what a hit *would have* cost.

**Assertion `A-M3-BLIND`:** the policy function's signature admits only the §2.1 set. Enforce it by
**passing a projection**, not the `TelegraphSpec` object — a policy handed the full spec can read
`damage_amount` by accident, and "we agreed not to" is not an assertion. This is the one place in
M-3 where the type system does real governance work.

---

## §3 — THE POLICY

### 3.1 The tactical structure it exploits (measured, E-1.2 — not invented)

| band | primordian | scale | note |
|---|---|---|---|
| inner | 0 – 2.5 m | **50 %** | the melee hug — **safest place that is still in the fight** |
| mid | 2.5 – 9.0 m | 100 % | |
| outer | 9.0 – 12.0 m | **140 %** | hardest, and the **only** band with angular gaps (gapless ≤ 7.64 m) |
| beyond | > 12.0 m | **0 %** | the bolt expires — total safety, total disengagement |

> **The reflex is inverted.** Backing away from a frigidring makes it **2.8× worse** (50 % → 140 %).
> The counterplay is to **stand in its face** — or to leave the fight entirely. E-1.2 calls this
> *"the single most fidelity-relevant geometric fact for M-2/M-3,"* and it is the reason M-3 is a
> design surface rather than a reflex: a naive "run from the red circle" policy would kill the
> player faster than no policy at all.

### 3.2 Algorithm

```
on telegraph_announce(tg) at t_a:                    # tg = the §2.1 projection
    schedule evaluate(tg) at t_a + reaction_latency_s

evaluate(tg) at t_e:
    if move_locked(self):            return HOLD("cc_locked")      # §3.4 — not a choice
    window = tg.fire_t_s - t_e
    if window <= 0:                  return HOLD("too_late")
    d      = dist(self, tg.origin)
    band   = band_of(d, tg.ring_band_scales)
    if band.scale == min_scale_of(tg):  return HOLD("already_safest_reachable")   # the inverted reflex
    v      = effective_move_speed(self)                            # slow-aware; NOT a teleport
    reach  = v * window
    cands  = []
    if (d - inner_max)   <= reach:   cands += [(scale_inner, d - inner_max, "close")]
    if (extent   - d)    <= reach:   cands += [(0.0,        extent - d,     "exit" )]
    if not cands:                    return HOLD("no_boundary_reachable")   # partial moves are NOT taken
    return DODGE(argmin(cands, key=(scale, displacement)))          # damage first, distance breaks ties
```

Four rulings embedded, each stated so it can be argued with:

- **M3-R1 — no partial dodges.** A move that does not cross a band boundary buys nothing and can
  buy harm (mid → outer is a 40 % *increase*). The policy commits to a boundary or holds.
- **M3-R2 — real movement, not teleport.** The dodge consumes the movement budget tick by tick
  through the existing navigation path, subject to `_f8_slow_factor` and arena clamps. **Its DPS
  cost is therefore emergent** — a melee player who backs to 12 m stops attacking. This is what
  stops the policy from being strictly dominant, and it is why no explicit "dodge cost" term is
  needed.
- **M3-R3 — deterministic resolution.** Success is a geometric fact at `fire_t_s`, not a roll.
  `dodge_failure_rate` exists (§4) and defaults to **0.0 — inert**, so **M-3 adds no RNG stream**
  and the door-closed digest is unmoved. Human fallibility is a later dial with a seam already cut.
- **M3-R4 — the band table is CONFIG, read from the tell.** Reading `ring_band_scales` off the
  telegraph is legitimate: a readable tell *shows where it hurts* (R-KC1-22's design-DNA note —
  *"dangerous = visible = dodgeable"*). Reading `damage_amount` is not (§1).

### 3.3 The emergent geometry — a derived structure, no tuning

At the harness's `movement_speed = 5.75 m/s` (`spatial_engine.py:6006` default; tick 0.1 s):

| d (m) | close to 2.5 | t_close | exit past 12 | t_exit | **t_min** |
|---|---|---|---|---|---|
| 3.0 | 0.50 | 0.087 s | 9.00 | 1.565 s | **0.087** |
| 5.0 | 2.50 | 0.435 s | 7.00 | 1.217 s | **0.435** |
| **7.25** | 4.75 | **0.826 s** | 4.75 | **0.826 s** | **0.826 — the worst point** |
| 7.64 | 5.14 | 0.894 s | 4.36 | 0.758 s | 0.758 |
| 9.0 | 6.50 | 1.130 s | 3.00 | 0.522 s | **0.522** |
| 10.0 | 7.50 | 1.304 s | 2.00 | 0.348 s | **0.348** |

**The close/exit crossover is at `(2.5 + 12)/2 = 7.25 m`** — within 0.4 m of the **gapless radius,
7.64 m**. The hardest place to escape a frigidring is, to within a step, the exact radius at which
the ring stops having gaps. Nobody designed that into this spec; it falls out of two measured
numbers and one speed. It is worth naming because it is the kind of coherence that tells you the
model is reading the real object.

### 3.4 Freeze, and the death spiral (the mechanism that makes M-2 and M-3 one system)

`move_locked(self)` is the **first** branch, and it is not a decision. GD freeze is full movement
**and** action immobilisation for 1.3–1.8 s (M-2 §3.4), landing **ungated on every hit that lands**.

```
nova 1 lands  →  freeze 1.3–1.8 s  →  policy returns HOLD("cc_locked") for the whole lock
              →  (+ push, if U-M2-5 lands non-zero: displaced OUT of the inner band)
              →  nova 2 arrives with the player mispositioned and only just unfrozen
```

**One dodge missed costs the next dodge too.** That is the death-2 trajectory expressed as a
mechanism rather than as a number, and it is the honest reason a no-evasion player dies where an
evading player does not. The policy must **not** be given a "break out of CC" affordance — the lock
is the stake.

### 3.5 ⚠ The windup measurement decides the mechanic's character

With `reaction_latency_s = 0.35`, the reachable displacement is `(w − 0.35) × 5.75`. Everything
between `2.5 + reach` and `12 − reach` is **undodgeable**:

| measured `w` | window | reach | **undodgeable annulus** |
|---|---|---|---|
| 0.6 s | 0.25 s | 1.44 m | **3.94 – 10.56 m** (a wide no-out zone) |
| 0.8 s | 0.45 s | 2.59 m | 5.09 – 9.41 m |
| 1.0 s | 0.65 s | 3.74 m | 6.24 – 8.26 m |
| **≥ 1.176 s** | — | — | **EMPTY — every position is escapable** |
| 3.0 s (the `specialAttackTimeout` upper bracket) | 2.65 s | 15.2 m | empty by a wide margin |

> **This is a single measured number that determines whether the frigidring is a positioning
> puzzle with a trap ring, or a skill check every competent player passes.** No value is authored
> here (R-WR1-9). The table exists so that when galadriel's number lands, its design consequence is
> already legible and nobody has to re-derive it under time pressure.
>
> **Design lean, offered not imposed:** a *small* undodgeable annulus (w ≈ 1.0 s) is the better
> game — it makes the 140 % band genuinely punishing to loiter in and rewards the player who
> commits to melee *early* rather than reacting late. But **the fixture decides, not the lean.**
> If the measurement says 2.0 s, the mechanic is fully dodgeable and that is the truth of it.

### 3.6 Multi-telegraph rule (spec'd; INERT at M-2 scope)

With one telegraphed attack modelled, this cannot fire. Stated so it does not get invented later:
evaluate candidate destinations against the **union** of live danger zones and minimise the **sum**
of band scales, ties broken by displacement. Still no `damage_amount` read.

---

## §4 — PARAMETERS (all tunable; every default justified or labelled)

| parameter | default | grade / justification |
|---|---|---|
| `reaction_latency_s` | **0.35** | **CALIBRATION CONSTANT, NOT A GD VALUE.** Mid-range human visual choice-reaction. Swept **{0.20, 0.35, 0.50}**. **Falsifiable against the fixture:** Matt dodged and won (§14.24), so `latency + traversal ≤ w` held for him on the casts he beat — once `w` is measured, §3.3's `t_min` column brackets his effective latency from above |
| `inner_band_max_m` | **2.5** | **M** — `projectileDamageRange1` upper bound |
| `extent_m` | **12.0** | **M** — `projectileDistance` |
| `threat_profile` band scales | 0.5 / 1.0 / 1.4 | **M** — E-1.2. Igrixx set: 0.5 / 1.0 / 1.5 at 2.0 / 10.0 breakpoints |
| `dodge_failure_rate` | **0.0 (INERT)** | M3-R3 — no RNG added; seam cut for later human fallibility |
| `evasion_enabled` | **False** | The A/B lever. **Default OFF ⇒ every pre-M-3 result is byte-reproducible** |
| `allow_disengage` | **True** | Whether "exit past extent" is a legal candidate. Setting False models a player who refuses to break melee — a **behavioural** arm worth one sweep, since §3.3 says exit dominates beyond 7.25 m and disallowing it creates a much larger trap zone |
| `min_dodge_gain` | **0.0** | Reserved: minimum band-scale improvement required to move. At 0.0 any strict improvement is taken |

---

## §5 — EMISSION (the baton, G-C / G-D)

- **`decision` event, `intent = "evade"`** — the schema already streams `decision` events carrying
  `(tick, chosen_target_id, intent)` (§14.25 conductor verification). A dodge rides that channel
  with the triggering `attack_id`, the chosen `action` (`close` | `exit`), and the destination.
  **Godot draws the evade vector the same way it draws aim-lines.** No new event type.
- **`telegraph.resolution`** — M-2 §4.4(ii)'s additive field is what makes a dodge *visible* in the
  baton. A telegraph with `resolution: "avoided"` and no paired `damage` event is the render-side
  proof that the sim dodged. **Without it, a successful dodge and a dropped event are
  indistinguishable in the trace, and G-D's evidence is ambiguous.**
- **HOLD reasons are diagnostics, not renders.** Emit `hold_reason` on the decision event
  (`cc_locked` / `already_safest_reachable` / `no_boundary_reachable` / `too_late`). §6.2 makes
  this distribution the primary instrument, so it must be in the artifact — not reconstructed after.

---

## §6 — ACCEPTANCE (G-B, winnable half)

### 6.1 ⚠ G-B is a PAIRED gate, and grading M-3 alone would be VACUOUS

The sim wins **30/30 at the boss tier today** (§14.26). *"The win becomes reachable"* is therefore
satisfied **before M-3 exists** — the exact vacuity §A-4.2 caught in S-3 (*"a predicate asking the
step to drive a count to zero cannot be evidenced by a count that starts at zero"*). Pre-registering
the fix rather than discovering it at grading:

**FOUR ARMS, same seeds (74000800 × 30), same battery:**

| arm | M-2 nova | M-3 evasion | expected | what it proves |
|---|---|---|---|---|
| **A0** baseline | off | off | 30/30 win | reproduces §14.26 — the before-baseline holds |
| **A1 — G-B killable half** | **on** | off | **deaths appear** | the nova kills a no-evasion player (M-2 §7) |
| **A2 — G-B winnable half** | **on** | **on** | **win rate recovers materially above A1** | **evasion converts the loss** |
| **A3 — NEGATIVE CONTROL** | off | **on** | **≈ A0, and `hold_reason` ≈ 100 % no-telegraph** | the policy is **not a generic damage reducer** |

> **A3 is not optional.** Without it, "evasion improved survival" is unfalsifiable — a policy that
> merely keeps the player moving would also improve survival, for reasons that have nothing to do
> with tells. A3 is the S-1-control lesson (§A-2.2: *"a control that reads exactly 1.0000 is what
> tells you the instrument works"*) applied before the fact instead of after.

**PRIMARY PREDICATE:** `WR(A2) − WR(A1)` is materially positive **and** attributable — the boss-tier
death count falls, and the `hold_reason` / dodge-outcome ledger shows the falls coincide with
successful evades. **A win-rate lift without a matching dodge ledger is not a pass.**

### 6.2 The instrument that actually carries the verdict

Per nova cast, per arm: `d`-at-announce · `d`-at-fire · policy verdict · `hold_reason` · realised
band · resulting damage. **This table is M-3's real deliverable.** §A-4 exists because a run
produced a band letter with no signature behind it; the dodge ledger is the signature.

### 6.3 The N-7 / N-8 / N-9 disposition (F-2)
- **N-7** (zero-intake fraction, 0.378 target ±0.15): **report, do not grade M-3 against it.** It is
  trash-dominated and telegraph-free (F-2). It belongs to M-4 + positioning. Carrying it as an M-3
  band would manufacture a MISS from correct scoping.
- **N-8 / N-9** (median encounter intake and median worst-drop, both 1.79 %): **legitimate M-3
  surfaces at the tiers that carry telegraphs.** Report per tier so the boss/champion contribution
  is separable from trash.

### 6.4 Honorable fallback
If A2 does not lift over A1, the honest readings — to be distinguished, not blended — are:
(i) the window is too short (§3.5 — a *measurement* result, and a real one);
(ii) freeze chains lock the player out (§3.4 — the mechanism working as designed, and arguably
the correct model of death-2);
(iii) the DPS cost of disengaging (M3-R2) exceeds the survival gain — **sweep `allow_disengage`**;
(iv) the policy is built wrong. **The `hold_reason` distribution discriminates (i)–(iii) from (iv)
directly.** Report which, and grade the miss as a miss.

---

## §7 — SIMPLIFICATION LEDGER

| # | Reality | Sim abstraction | Risk |
|---|---|---|---|
| SL-1 | Human dodging is continuous, anticipatory, and pattern-learned across a fight | **Reactive, per-telegraph, memoryless** | Under-states a skilled player; **conservative against G-B**. A player who pre-positions before the tell is not modelled |
| SL-2 | Reaction latency is a distribution, and degrades with fatigue and stimulus density | **Single deterministic scalar** | `dodge_failure_rate` is the reserved seam. Named |
| SL-3 | Movement has acceleration, turn cost, and animation commitment | Instant-heading constant-speed step (existing engine model) | **Over-states** dodge feasibility by roughly one acceleration ramp. The only simplification in this document that flatters the gate — **named for exactly that reason** |
| SL-4 | GD dodge is positional in 3D with terrain, LOS and collision | Flat arena, no collision volumes (baton §9 HG-6), soft-push only | Inherited from the engine. Named |
| SL-5 | Matt's death-2 sample is contaminated — he stood still ~2 s taking a screenshot (§14.24) | Not modelled | **The contamination runs in the anchor's favour** (§14.24: standing still is the sim's native behaviour, so the human sample is pulled *toward* the sim's space). Carried, not smoothed |
| SL-6 | A real player weighs dodging against DPS uptime, resource timing and kill windows | Damage-minimising within reach, ties on displacement | The DPS cost is **emergent** (M3-R2), not optimised against. A future policy could trade them; this one does not pretend to |

---

## §8 — NAMED UNKNOWNS

| # | Unknown | Disposition |
|---|---|---|
| **U-M3-1** | Telegraph windup `w` | **Inherited, R-WR1-9.** §3.5 shows it decides the mechanic's character. Bracket (0, 3.0] s |
| **U-M3-2** | Human reaction latency at this fixture | `0.35 s` **calibration constant**; swept; bracketable from the fixture once `w` lands (§4) |
| **U-M3-3** | Multi-hit ring (M-2 U-M2-1) | **Inherited. Reverses §3.1 if true** (F-1). Config-level flip by design |
| **U-M3-4** | Whether a real player disengages past 12 m or holds melee | `allow_disengage` swept both ways (§4) |
| **U-M3-5** | Whether Matt's win used close-in or exit evasion | **Not decidable from the banked fixture.** Closable from the capture in the same galadriel pass (M-2 §8.3) — his distance-from-caster track across the winning attempt |

---

## §9 — BUILD NOTE FOR GAMORA

**You own:** the implementation math note **before code** (Discipline #1); the tests; **jack-ryan
Gate-2, MANDATORY** — M-3 touches the fight loop's decision path, which is as kernel-adjacent as
this run gets.

**Sequencing:** M-3 **cannot start before M-2's two-phase commit (§4.2) lands.** There is no dodge
window until the announce phase exists. If M-2 slips, M-3 slips — say so early rather than building
against a mock telegraph.

**Landing shape (recommendation; the seam is yours):**
1. **`evasion_enabled` default False**, door-scoped. Digest byte-unmoved with it off — **every
   pre-M-3 battery stays reproducible.** This is what makes the §6.1 four-arm design cheap.
2. **No new RNG stream** (M3-R3). If you find yourself wanting one, that is a signal the policy has
   grown a stochastic component the spec did not authorise — raise it, do not add it.
3. **Assertions:** `A-M3-BLIND` (§2.2 — the projection type, not the `TelegraphSpec`) ·
   `A-M3-DET` (arm A2 bit-reproducible across two runs at fixed seed) · `A-M3-NOTP` (**arm A3
   produces zero dodge decisions** — no telegraph, no policy activity; the negative control's own
   control) · `A-M3-LOCK` (a move-locked entity never returns `DODGE`).
4. **Emit the §6.2 dodge ledger from the first run.** Not a follow-up. The ledger *is* the verdict;
   a battery that produces a win-rate without it has produced a number nobody can grade.
5. **Ship the §6.1 four arms in one battery**, same seeds. A0 doubles as the regression check on
   §14.26.

**You do not own:** the windup value (galadriel, R-WR1-9) · the U-M2-1 multi-hit ruling (conductor,
after measurement) · the schema/MIGRATION amendment for `telegraph.resolution` + HG-2 + the
`TelegraphSpec` docstring — **that is one MIGRATION covering M-2 §4.4(ii) and M-3 F-3 together, and
drax must receive it before he builds the Godot leg against v1 semantics.**

---

## §10 — CLOSING NOTE (`STORYWRIGHT`, one paragraph, and it is load-bearing)

R-KC1-22 banked the design-DNA line: *"slow, readable tells — dangerous = visible = dodgeable; the
Primordian fight was winnable through skill, not stat-checking."* M-3 is the first mechanism in this
project that makes that sentence **testable**. And the substrate handed us something better than a
generic dodge: an attack whose safest position is *in the monster's face*, whose most dangerous
position is the one every instinct sends you to, and whose punishment for a missed read is that you
cannot read the next one either. That is not a stat check wearing a telegraph. It is a genuine
question the fight asks the player, and the player's answer is the fight. **Build it so the sim can
be asked the same question** — and if the sim answers it badly, that is a finding about the sim's
positional model, which is exactly what this run exists to surface.

**Signed:** gandalf (`SPEC-AUTHOR`), 2026-07-29. Veto-open per the WR1 ruling ledger.
