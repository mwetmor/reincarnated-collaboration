# M-2 — Frigidring / telegraph-burst nova · design-spec-as-math

**Agent:** gandalf (`SPEC-AUTHOR`) · **Date:** 2026-07-29 · **Run:** WR1-2026-07-28 · **Cell:** WR1-SPEC-M123
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Charter:** §3 M-2 · **Rulings:** **R-WR1-8** (mechanism
class, primary calibration) · **R-WR1-9** (windup is a measured input) — both BINDING here
**Class:** design-spec (design layer of the math note; gamora authors her own per Discipline #1)
**Builds against:** legolas `2026-07-28-wr1-mechanism-extraction.md` **E-1** · KC1 §14.23 **H-1**
(fidelity law, BINDING) · §14.24 **R-KC1-22** · §14.26 (the symmetry finding) · efficacy verdict
§A-8.1 row 1 · baton schema `2026-07-22-replica1-frame-schema-spec.md` §3.3 / §9 HG-2
**Serves gate:** **G-B killable half** (charter §2) — and supplies M-3's entire input surface
**Companion specs:** M-1 (`…-wr1-m1-mitigation-spec.md`) · M-3 (`…-wr1-m3-evasion-policy-spec.md`)

---

## §0 — FRAMING AUDIT, and what it caught

**Q1 — the question.** Make the sim capable of the death-2 trajectory: a burst that can kill a
no-evasion player at the fixture's band, modelled as the GD mechanism rather than an RDR analogue.

**Q2 — pre-imposed assumptions.** The brief is accurate to the extraction on every parameter. Two
items it does **not** carry, both load-bearing, both sourced:

> ### ⚠ FLAG F-1 — the nova carries a KNOCKBACK, and without it the nova probably does not kill.
> E-1.2 measures `ragDollDirection = Push` / `ragDollElevation = Downward` / `ragDollEffect =
> TakeHit` on `primordian_frigidring`. The brief does not mention it. It matters more than any
> damage number in this document, because of §4.3: **the sim player is a melee kit that hugs the
> target, and melee is the nova's 50 % band.** A nova that cannot displace its victim out of the
> weakest band will be evaluated, every single cast, at 15.9 % of pool — and G-B's killable half
> will fail for a reason that looks like a magnitude problem and is actually a positional one.
> The push (plus the freeze, §3.4) is the mechanism that walks the player *out* of safety.

> ### ⚠ FLAG F-2 — whether multiple ring projectiles can hit ONE target is UNKNOWN, and it
> ### **reverses the tactical structure** on which R-WR1-8, this spec, and all of M-3 depend.
> Ring geometry (§2.3) puts **6.1 projectile-explosion widths** over a point at 1.25 m and **0.76**
> at 12 m. Under a *single-hit* reading the range bands read literally and the nova hits hardest at
> the outer edge — *"this inverts the usual back-off-to-survive reflex,"* E-1.2's own words, and the
> premise of M-3. Under a *multi-hit* reading, effective melee damage is `6.11 × 0.50 = 3.06×` base
> against the outer edge's `0.76 × 1.40 = 1.06×` — **melee becomes 2.9× WORSE than range and the
> inversion vanishes.** The 50 % melee band may well *be* GD's own normalisation for overlap
> density, which is the reading that makes the multi-hit hypothesis uncomfortable to dismiss.
> The corpus states no aggregation rule (`skill_attackprojectilering.tpl` declares 13 variables,
> none of them about target-hit arbitration).
> **Disposition:** §5 U-M2-1 — single-hit default, named, with a routed cheap close (§8.3).

**Q3 — what would change the answer.** galadriel's frame measurement (R-WR1-9) — **if its scope is
extended to count damage floaters per nova cast, it closes F-2 in the same pass that closes the
windup.** Routed as a recommendation in §8.3.

---

## §1 — MECHANISM CLASS AND CALIBRATION (R-WR1-8, binding)

M-2 models the **`Skill_AttackProjectileRing` mechanism class** — a radial burst of `N` projectiles
launched simultaneously on a `360°/N` spacing, each carrying the full damage row, each detonating in
a small explosion radius, all expiring at a fixed travel distance, with damage scaled by a
range-band table read at the **victim's distance from the caster.**

| | **PRIMARY calibration** | **SECONDARY parameterisation** |
|---|---|---|
| record | `records/skills/nonplayerskills/bossskills/primordian_frigidring.dbr` | `records/skills/nonplayerskills/heroskills/igrixx_frigidring.dbr` |
| carrier | `boss&quest/slith_wightmirecave01` — *Primordian, the Forgotten One* | `hero/slith_h01` — **"Igrixx, the Rimeheart"** |
| the fixture's boss encounter | **yes** | champion-slot, 15–40 % chance, same Act-1 Wightmire pools |

**The attribution caveat travels with the mechanism, not resolved by it** (R-WR1-8, extraction G-7):
two lineages fire the same `icebolt_nova_fxprojectile` in the same content and the corpus cannot
decide which killed Matt. **G-B grades against the death-2 BAND, not the attacker's identity,** so
the gate is unaffected. Igrixx is spec'd as a real second parameterisation, not a footnote, because
he is *reachable in the champion tier* — which is a battery tier G-C must emit.

---

## §2 — MEASURED PARAMETER SET

### 2.1 Damage row — `primordian_frigidring` @ **rank 5** (all M, E-1.2)

Rank resolution: carrier `skillLevel7 = 'charLevel/4+1'`; at the fixture band Primordian
`charLevel = 17–18` → **rank 5**. Rank 4 is carried as the sensitivity arm because the KC1 charLevel
question is **U**.

| field | **r4** | **r5** | note |
|---|---|---|---|
| `offensiveColdMin` | 200 | **247** | |
| `offensiveColdMax` | 0.0 | **0.0** | **Min-only** |
| `offensivePhysicalMin` | 118 | **148** | |
| `offensivePhysicalMax` | 0.0 | **0.0** | **Min-only** |
| `offensiveFreezeMin / Max` (s) | 1.3 / 1.8 | **1.3 / 1.8** | CC duration, §3.4 |
| `offensiveSlowColdMin` | 60 | **77** | cold **DoT** — §2.2 |
| `offensiveSlowColdDurationMin` (s) | — | **2.0** | |
| `skillManaCost` | 34 | **38** | |

> **The nova is a FLAT hit, not a range roll.** Both damage rows are Min-only — the **C-flag**
> (max clamped to min) from the G-5a ledger applies. There is **no per-hit damage variance on this
> attack.** The sim must not apply its ±15 % resolver variance to the nova's magnitude, or it will
> manufacture spread the source does not have. Assert it.
>
> **~85 % of the flat payload is cold** (247 of 395 at r5). Against M-1 §2.4: armor is
> **structurally inert** against 247 of the 395. This is the single sentence that ties M-1 and M-2
> into one law, and it is why the mitigation that tames the trash tier does nothing to this attack.

### 2.2 The `offensiveSlowCold` reading — a named fork, 2× on the DoT

GD's `offensiveSlow*` family is **damage-over-time**, not movement-slow. Two confirmations:
E-1.2 annotates `offensiveSlowColdDurationMin = 2.0` as *"the cold DoT window"*; and kit spec v2
§1.6 channel 5 reads the sibling field `offensiveSlowBleedingMin @16` as **"270/s × 3.0 s = 810"** —
i.e. the `Min` field is a **per-second rate.**

Carrying that precedent: cold DoT = **77/s × 2.0 s = 154 total** at r5. The alternative reading
(77 *total* over 2.0 s) halves it. **U-M2-2**, §5. Default = the rate reading, by kit-spec-v2
precedent, graded **[I]**.

> **Note the phrasing drift to guard against:** charter §8.4 and the cell brief both render this as
> *"cold-slow 77/2.0 s"*, which reads naturally as a movement slow. The extraction body says DoT.
> **The extraction wins** (cell brief's own instruction). Recording the drift so it is not
> re-introduced downstream: **there is no movement-slow rider on this nova.** The only movement
> effect is the freeze (§3.4) and the push (§3.5).

### 2.3 Ring geometry and kinematics

| field | primordian | igrixx | grade |
|---|---|---|---|
| `projectileLaunchNumber` | **16** | 16 | M |
| `projectileLaunchRotation` | **360.0°** → 22.5° spacing | 360.0° | M |
| `projectileExplosionRadius` | **1.5 m** | **2.0 m** | M |
| `projectileUsesAllDamage` | **True** — every bolt carries the full row | True | M |
| damage range bands | **0–2.5 → 50 % · 2.5–9.0 → 100 % · 9.0–20.0 → 140 %** | 0–2.0 → 50 % · 2.0–10.0 → 100 % · 10.0–20.0 → **150 %** | M |
| `projectileVelocity` | **14.0 m/s** | 14.0 | M |
| `projectileDistance` | **12.0 m** | 12.0 | M |
| `skillSpecialAnimationName` | **`Roar`** | — | M |
| `cameraShakeAmplitude` | 0.12 | — | M |

**Derived (D — geometry only):**

| d (m) | arc spacing `2πd/16` | overlap `2R_exp / spacing` | flight time `d/14` | band scale |
|---|---|---|---|---|
| 1.25 (`meleeRange`) | 0.49 | **6.11** | 0.089 s | 50 % |
| 2.50 | 0.98 | 3.06 | 0.179 s | 50 % / 100 % edge |
| 5.00 | 1.96 | 1.53 | 0.357 s | 100 % |
| **7.64** | 3.00 | **1.00 — the gapless boundary** | 0.546 s | 100 % |
| 9.00 | 3.53 | 0.85 | 0.643 s | 140 % |
| 12.00 | 4.71 | 0.64 | 0.857 s | **140 %, and the bolt expires** |

Two structural facts the build must carry:

1. **Inside 7.64 m the ring is GAPLESS.** There is no "step between the bolts" evasion. Outside it,
   angular gaps open — but the 140 % band starts at 9.0 m, so the only place a gap exists is also
   the only place the damage is maximal. GD gave the player a genuine dilemma; do not flatten it.
2. **The 140 % band is 9–12 m, not 9–20 m.** The record declares the band to 20 m but the projectile
   only lives to 12 m (`projectileDistance`). Past 12 m the attack simply does not exist. **The two
   safe places are ≤ 2.5 m and > 12 m, and everything between is worse than both.**

### 2.4 Wiring / cadence (M, E-1.4) — and the G-2 ruling this spec must make

`slith_wightmirecave01`: `specialAttack2SkillName = primordian_frigidring`,
`specialAttack2Chance = **80.0**`, `specialAttack2Delay = **6.0** s`,
`specialAttack2Timeout = **3.0** s`, `specialAttack2Range = **MediumRange** (≤ 10.0 m)`.
Creature bands: `shortRangeMax 4.0` / `mediumRangeMax 10.0` / `longRangeMax 12.0`.

Extraction **G-2** is explicit that `specialAttackTimeout`'s global-vs-per-slot semantics are
genuinely ambiguous in source and that *"the M-2 spec must name which reading it adopts"*, with a
**~2× swing in nova cadence.**

> **RULING M2-R1 (this spec, veto-open): adopt READING A — per-slot.** Nova available every **6.0 s**
> at an **80 %** roll. Rationale: (i) slots 2–7 declare `Delay`/`Timeout` as their own fields, and
> the only authored description belongs to slot 1 — reading slot-1's wording onto slots that
> redeclare the field is the weaker inference; (ii) Reading B additionally requires modelling
> `primordian_wave`'s lockout to be coherent, which widens M-2 into a second skill this cell has not
> spec'd; (iii) Reading A is the *more dangerous* reading, so adopting it and still missing G-B
> would be informative, whereas adopting the safer reading and passing would be uninformative.
> **`nova_delay_s` is exposed and swept at {6.0, 11.0}** so the 2× sensitivity is measured, not
> assumed. Named as **[I]** in the artifact.

**Range gate:** the nova fires only when the target is within `MediumRange = 10.0 m` of the caster.
Note the interaction: the caster will not *initiate* beyond 10 m, but the projectile reaches 12 m —
so the 140 % band (9–12 m) is only partly inside the initiation window (9–10 m). Model both:
`nova_initiation_range_m = 10.0`, `projectile_extent_m = 12.0`. They are different numbers and
collapsing them removes a real 2 m of GD texture.

### 2.5 Igrixx — the secondary set (M, E-1.3)

`skillLevel5 = 'charLevel/4+1'`, `charLevel = 'charLevel*1+5'`, spawn `lv6_hero` → at player 12,
**rank 5–6**. At r5: `offensiveColdMin = 171`; `offensiveFreezeMin = 0.9` with `offensiveFreezeMax`
**absent from the record entirely** (→ fixed duration, not a range); **no `offensivePhysical*`,
no `offensiveSlowCold*`.** Pure cold, fixed freeze, no DoT rider, no physical component —
**mechanically cleaner and weaker than Primordian's, and completely armor-proof.**
Gapless radius `2×2.0/(2π/16) = 10.19 m`. Wiring on `hero/slith_h01`: chance **100 %**,
delay **10.0 s**, timeout 3.0, **ShortRange**.

---

## §3 — THE SIM MODEL

### 3.1 Resolution model (the honest abstraction)

The sim has **no projectile flight** (baton schema §9 HG-1: AOE resolves instantaneously at cast).
M-2 does **not** add flight ticks — that is a much larger change and it is not what G-B needs.

**Abstraction:** the nova resolves as an **instantaneous distance-banded hit at
`t_fire + d/14.0`**, where the flight term is carried as `resolve_delay_s` per target and is
**≤ 0.857 s** at maximum extent. Two sub-options, and the spec picks:

> **RULING M2-R2: resolve ALL targets at `t_fire`, and carry `d/14.0` as REPORTED metadata on the
> telegraph event (`ring_speed_mps`), not as engine timing.** Rationale: staggering resolution
> introduces a per-target scheduling queue the engine does not have, for a ≤0.86 s effect on a
> 6.0 s cadence; and the *rendering* of ring expansion (which is what G-D needs) is fully
> reconstructible in Godot from `origin`, `ring_speed_mps` and `fire_t_s`. **Named divergence:**
> a target at 12 m is damaged 0.86 s "early" relative to GD. **Consequence to watch:** it slightly
> *reduces* the dodge window at range for M-3, i.e. it is conservative against the gate rather than
> flattering to it.

### 3.2 Per-target damage

```
d      = distance(caster, target) at fire instant
scale  = band_scale(d)            # 0.50 / 1.00 / 1.40  (step function, §2.3)
if d > projectile_extent_m (12.0): NO HIT                       # the bolt expired
cold_instant = 247 * scale
phys_instant = 148 * scale
cold_dot     = 77  * scale        # per second, 2.0 s   (§2.2, U-M2-2)

applied_cold = cold_instant * (1 - min(res_cold, cap))          # M-1 §2.4 — armor NEVER consulted
applied_phys = gd_armor_through(phys_instant, armor)            # M-1 §2.3
per_hit      = applied_cold + applied_phys                       # the worst_drop_abs candidate
```

**No damage variance** (§2.1 C-flag). **One hit per target per cast** (U-M2-1 default, §5).

At the harness's pinned player (pool 759, armor 125, `res_cold = 0.20` default):

| band | instant (the `worst_drop` candidate) | % of 759 | cold DoT (2 s) | window total | % of 759 |
|---|---|---|---|---|---|
| **melee ≤ 2.5 m (50 %)** | **121.0** | **15.9 %** | 61.6 | 182.6 | 24.1 % |
| **mid 2.5–9 m (100 %)** | **258.1** | **34.0 %** | 123.2 | 381.3 | 50.2 % |
| **outer 9–12 m (140 %)** | **396.3** | **52.2 %** | 172.5 | 568.8 | **74.9 %** |

Sensitivity at `res_cold ∈ {0.00, 0.40}`: outer-band instant reads **61.3 %** / **43.1 %** of pool.

> **G-B's magnitude half is comfortably reachable, and §A-8.1 row 1's target is met at the outer
> band:** *"single hit ≥ 40 % of pool becomes possible"* — **52.2 %**, and ≥ 40 % across the whole
> `res_cold` sweep. Against the sim's current boss worst drop of **7.80 %** (§14.26) that is a
> **6.7× jump in the worst-hit statistic.**
>
> **And it is unreachable at melee (15.9 %) — which is exactly the design point, and exactly the
> risk.** See §4.3.

Igrixx at `res_cold = 0.20`: melee **9.0 %** · mid **18.0 %** · outer (10–12 m, 150 %) **27.0 %**.
Below the 40 % existence target on every band — **correct and expected**: Igrixx is a champion, not
a boss, and G-B is a boss-tier gate.

### 3.3 Cadence

```
first available at t = nova_delay_s (6.0)
thereafter every nova_delay_s, each attempt gated on nova_chance (0.80)
and on distance(caster, target) <= nova_initiation_range_m (10.0)
```
Expected casts in the sim's measured 27.3–30.3 s boss fight: `⌊29/6⌋ = 4` windows × 0.80 ≈ **3.2**.

### 3.4 Freeze — CC ONLY. **FIDELITY LAW, BINDING (Gate-2 H-1).**

`offensiveFreezeMin/Max = 1.3 / 1.8 s`; `offensiveFreezeChance` **absent** and every `*Chance` in
the record is 0 → **no chance gate. The CC lands on every hit that lands** (E-1.2, graded I but
uniform across the record).

> **The nova must NOT carry an effect named `freeze`.** RDR's `freeze` triggers **shatter-on-expiry**
> — `effect_resolver.py:244-258` keys the shatter branch on `effect.name == "freeze"` exactly, and
> at the fixture's own numbers one expiry below 25 % HP costs `0.20 × max_hp`. **GD freeze has no
> shatter. RDR's shatter is an RDR mechanic and importing it here would fabricate damage the source
> does not have** — and it would do so *in the exact statistic G-B grades.* This is KC1 §14.23 H-1
> and the §14.25 `A-FRZ-1` assertion, carried forward into a build that finally has a nova to
> assert about.

**Semantics to reproduce:** full movement **and** action immobilisation for `U(1.3, 1.8)` s.

**Landing options, with the spec's lean:**

- **(a) LEAN — reuse the engine's `stun` with `immunity_after_seconds = 0.0`.** `stun` already
  appears in **both** hard-CC predicates (`_f8_action_locked` :560 and `_f8_move_locked` :578), which
  is precisely GD freeze's "full movement + action immobilization"; shatter cannot fire because the
  branch is name-keyed to `freeze`; and the one un-sourced rider `stun` carries —
  immunity-after-expiry, default 2.0 s (`effect_resolver.py:266`) — is a **per-effect param** that
  zeroes cleanly. **No kernel predicate is touched.** Cost: the trace labels a freeze as a stun.
  Mitigate by stamping `source_element = "cold"` on the effect so the baton and Godot can render
  the right visual (M-3 §3 also reads it). Name the cosmetic divergence in the artifact.
- **(b) a new effect name (`gd_freeze`)** added to both predicates, shatter-free and immunity-free
  by construction. Cleaner semantics, but it edits kernel CC predicates for a naming benefit.

**Assertion (extend `A-FRZ-1`): `A-M2-FRZ` — no effect named `freeze` on any Primordian, Igrixx or
kit dict, and any `stun` sourced from the nova carries `immunity_after_seconds == 0.0`.** Both
halves, so neither the shatter hazard nor an un-sourced DR can reach the boss fight.

**The compounding property is the whole point** (§4.3): a frozen player cannot dodge the next nova.
At `nova_delay_s = 6.0` and freeze 1.3–1.8 s the lock does not span two casts by itself — but it
spans the melee cadence (`controller_boss_viloth` `minSwingPause/maxSwingPause = **0.30/0.40 s** —
the tightest bounded pause in the entire roster, E-3.4) and it spans the push-recovery.

### 3.5 Knockback — `ragDollDirection = Push` (FLAG F-1)

**Measured:** `Push` / `Downward` / `TakeHit` (E-1.2). **Magnitude: NOT DERIVABLE.**
`physicsStrengthEquation = (2·(damage/(maxLife·0.3))) + 4`, clamped [7, 15] (E-2.1) — at 258 damage
on a 759 pool this evaluates to 6.27 → clamps to the **floor, 7**. The *units* of that impulse are
**U** and no displacement in metres is obtainable from the corpus.

> **Disposition: `nova_push_m` is a named parameter with default `0.0` (INERT).** The spec
> **refuses to author a displacement**, exactly as R-WR1-9 refuses to author a windup. If G-B's
> killable half fails **and** the measured cause is melee-band residency (§4.3's pre-registered
> diagnostic), the push is the **first named candidate** — and the correct response is to
> **measure it** (galadriel, §8.3), not to tune it until the player dies. Pre-registering this
> distinction is the point: a push value discovered by fitting to a gate is not a fidelity model.

### 3.6 Out of scope, named so their absence is not mistaken for a claim

`primordian_wave` (`Skill_AttackWave`, 16 m cone, delay 5.0 s) · `chillbane_blizzard`
(`Skill_BuffAttackRadiusDrop`, 8 s ground hazard, delay 10.0 s) · `primordian_icearmor`
(25 % absorb / **+35 % attack speed**, 12-on/32-off — touches M-4) · `primordian_passive` (cold
rider on the base attack). **`primordian_arcticblast` is referenced by no creature — orphaned in the
corpus. DO NOT MODEL IT** (E-1.4, verbatim instruction).

---

## §4 — TELEGRAPH EMISSION, AND THE CONTRACT IT BREAKS

### 4.1 The windup slot (R-WR1-9, binding — no value is authored here)

`wind_up_s` is **already a supported per-skill key**: `_mint_telegraph_spec`
(`spatial_engine.py:1638`) reads `skill_dict.get("wind_up_s")` before falling back to the
per-geometry default table. **No new plumbing is needed for the measured input to land.**

| | |
|---|---|
| **status** | **MEASURED-INPUT SLOT — UNRESOLVED.** Not in the corpus: `skill_attackprojectilering.tpl` declares **zero** timing fields; the `Roar` animation resolves to `slith01_cast_buff_01.anm` at speed 1.0 (asset **named**, M) but the pin ships no `.anm` (E-1.5, extraction G-1) |
| **source of truth** | galadriel's frame measurement of Matt's 2026-07-26 capture, tell-onset → damage-application (cell WR1-WINDUP-GAL) |
| **upper bracket** | **3.0 s** = `specialAttack2Timeout` (R-WR1-9) |
| **build disposition** | `wind_up_s` REQUIRED on the nova skill dict; **raise on absent** — do not silently fall back to `TELEGRAPH_WIND_UP_DEFAULTS_S`, which is an RDR-authored constant and would launder an unmeasured value into a fidelity claim |
| **fallback if the capture cannot resolve it** | ship the measured range + the 3.0 s bracket, flagged, per R-WR1-9 |

### 4.2 The telegraph must become a TWO-PHASE COMMIT — and this is the largest build implication

Today `_mint_telegraph_spec` is called **at the fire site** (`spatial_engine.py:4968-4981`), *after*
resolution: `wind_up_s` is retro-annotation on an already-resolved hit. That is coherent for
rendering an inert tell. **It cannot support M-3**, because there is no interval during which the
player is inside a danger zone that has not yet resolved.

**M-2 must schedule the cast:**

```
t_announce = t_fire - wind_up_s
  · attacker COMMITS to the nova; geometry (origin, bands) FROZEN at announce
  · TelegraphSpec emitted at t_announce            [the tell]
  · attacker is ANIMATION-LOCKED for the windup    [GD-faithful: `Roar` is a cast animation]
t_fire
  · resolve §3.2 against each target's CURRENT position
  · the announced origin and the resolve origin are IDENTICAL (the lock guarantees it)
```

**The animation lock is not decoration — it is what preserves §7.1 no-drift** (the TelegraphSpec
invariant that the danger-zone shape is minted from the same footprint the resolver uses). A caster
free to move during windup would make the announced footprint a lie. Locking it makes the invariant
*stronger* than it is today, and it is independently GD-faithful.

**Corollary the build must not miss:** the player's distance is read at `t_fire`, not at
`t_announce`. That is what makes the tell *actionable* — and it is exactly the seam M-3 plugs into.

### 4.3 ⚠ The pre-registered diagnostic: the sim player may be standing in the safe band already

The G-5 kit is **melee** (`range_profile: "melee"`, claws/charge at ~2 m). The sim player closes and
stays closed. **Melee is the nova's 50 % band.** So the sim's naive behaviour is, by accident,
close to GD's correct counterplay — and a nova bolted onto an unchanged positional model may
resolve at 15.9 % of pool on nearly every cast and **fail G-B's killable half while being perfectly
correctly built.**

> **PRE-REGISTERED (before the build, so it cannot be a post-hoc rescue):** the M-2 battery must
> report **the distribution of `d` at nova fire-instant** — per cast, per tier — alongside the
> damage numbers. If G-B's killable half fails, the FIRST reading is that distribution.
> - If `d ≤ 2.5 m` on most casts → the cause is **positional**, and the named candidates in
>   priority order are (1) `nova_push_m` (§3.5, F-1), (2) freeze-during-approach, (3) spawn
>   distance / the boss's own kiting. **Each is a measurement, not a knob.**
> - If `d` is spread and the nova still fails to kill → the cause is **magnitude**, and §3.2's
>   table says that should not happen at `res_cold ≤ 0.40`.
>
> **Reporting `d` is not optional.** Without it, a G-B miss is uninterpretable, and an
> uninterpretable miss is the failure mode that produced the S-3 lap.

### 4.4 Baton schema consequences (G-C / G-D — reaches drax)

Three, and the second is a **contract change requiring MIGRATION**.

- **(i) `emit_telegraphs=True` for the baton emission.** Constructor default is `False`
  (`spatial_engine.py:2732`). G-D requires *"telegraph tells rendered from `telegraph` events"* —
  the baton run must set it.

- **(ii) ⚠ MIGRATION — the INERT invariant DIES.** `TelegraphSpec`'s docstring §7.2 states
  *"the sim damage ALWAYS applies at fire_time_s, full magnitude, with NO dodge/avoidance branch,"*
  and baton-schema §9 **HG-2** instructs drax *"the renderer must not let a player 'dodge' a
  telegraph — there is no such mechanic in the sim."* **M-3 makes that false.** The docstring, HG-2,
  and §3.3's `damage_amount` gloss (*"metadata; sim always applies it"*) must all be amended
  together to: *"`damage_amount` is what the hit WOULD deal; whether it landed is the sim's own
  resolution, and the trace states it."* **Recommended additive field on the telegraph event:**
  `resolution: "hit" | "avoided" | "expired"` plus `resolved_target_ids: [str]`. Without it a
  renderer cannot distinguish "the sim dodged" from "the emitter dropped an event," and G-D's
  evidence becomes ambiguous. **Owner: gamora writes it; drax must be told before he builds against
  v1 semantics.** Note the schema's own §7.1-adjacent principle survives intact — the *geometry* is
  still minted from the resolver's footprint; only the *outcome* claim changes.

- **(iii) ring geometry does not fit the shape enum.** The enum is `circle|cone|line|point`; a nova
  is an expanding **annulus**. Options: extend the enum (breaks unknown-value consumers), or —
  **the lean** — keep `shape = "circle"` with `radius_m = 12.0` (the danger extent, so an
  un-updated Godot still draws a correct-extent circle) and ride the ring detail as **optional
  additive fields**: `ring_speed_mps` (14.0), `ring_thickness_m` (3.0 = `2 × projectileExplosionRadius`),
  `ring_projectile_count` (16), `ring_gapless_radius_m` (7.64), `ring_band_scales`
  ([[0,2.5,0.5],[2.5,9,1.0],[9,12,1.4]]). Additive-only ⇒ old readers degrade gracefully, and drax
  gets everything he needs to render the expansion **and** the band shading. The band table is
  worth shipping to the renderer: a tell that shows *where it hurts most* is the readable-telegraph
  contract R-KC1-22 named (*"dangerous = visible = dodgeable"*).

---

## §5 — NAMED UNKNOWNS

| # | Unknown | Source | Default / disposition |
|---|---|---|---|
| **U-M2-1** | **Can multiple ring projectiles hit one target?** | corpus states no aggregation rule; FLAG F-2 | **Single hit per target per cast.** Exposed as `nova_max_hits_per_target = 1`. **REVERSES M-3's tactical structure if false** — highest-value close in this spec (§8.3) |
| **U-M2-2** | `offensiveSlowColdMin = 77` — per-second rate or total? | §2.2 | **Rate** (kit-spec-v2 §1.6 bleed precedent) [I]; 2× sensitivity swept |
| **U-M2-3** | Telegraph windup duration | extraction G-1; **R-WR1-9** | **MEASURED-INPUT slot; raise-on-absent.** Bracket (0, 3.0] s |
| **U-M2-4** | `specialAttackTimeout` global vs per-slot | extraction G-2 | **Reading A adopted (M2-R1)** [I]; `nova_delay_s` swept {6.0, 11.0} |
| **U-M2-5** | Knockback displacement in metres | E-2.1 impulse clamps to 7; units U | `nova_push_m = 0.0` (**inert**); measurement-routed, not fitted |
| **U-M2-6** | Which nova killed Matt | extraction G-7; **R-WR1-8** | **Not adjudicated.** Mechanism class modelled; caveat travels with G-B, which grades on the band |
| **U-M2-7** | Primordian `charLevel` (17–18?) → rank 4 vs 5 | KC1, still U | **r5** primary; r4 swept |
| **U-M2-8** | Player cold resistance | shared with M-1 U-2 | 0.20 **calibration constant**; swept {0.00, 0.20, 0.40} |
| **U-M2-9** | Freeze CC chance-gate reading (`Chance = 0` ⇒ ungated) | E-1.2, graded I | **Ungated** — uniform across the record |

---

## §6 — SIMPLIFICATION LEDGER

| # | GD truth | Sim abstraction | Risk |
|---|---|---|---|
| SL-1 | 16 discrete projectiles with 0.089–0.857 s flight | Instantaneous banded hit at `t_fire`; flight carried as render metadata (M2-R2) | Damage arrives ≤0.86 s early at range. **Conservative against G-B, not flattering.** Named |
| SL-2 | Continuous angular geometry; the ring can miss through a gap beyond 7.64 m | Distance-only band function; **no angular miss** | Over-states hits at 9–12 m — the band where damage is maximal. **The single most consequential simplification in this document.** Named. Cheap refinement if it bites: multiply by the coverage fraction `min(1, 2R_exp/(2πd/16))` |
| SL-3 | Per-region hit location | Single armor scalar | Inherited from M-1 SL-1 |
| SL-4 | Ragdoll push with engine-physics displacement | `nova_push_m` **inert by default** | §3.5; the pre-registered first suspect for a §4.3 positional failure |
| SL-5 | GD freeze | `stun` with `immunity_after_seconds = 0.0` + `source_element = "cold"` | Cosmetic label divergence in the trace. **Named. The alternative (b) is available** |
| SL-6 | Boss AI kites/repositions between specials | Existing sim boss movement, unchanged | Feeds §4.3's `d` distribution — **measure it, do not assume it** |
| SL-7 | `chillbane_blizzard` ground hazard + `primordian_wave` cone are live in the same fight | **Not modelled** | Under-states the real boss. Consistent with §14.25's named-absent discipline: bias named, not smoothed. **Biases G-B toward a MISS**, which is the safe direction |
| SL-8 | `primordian_icearmor` grants **+35 % attack speed** for 12 s in 44 | Not modelled here (M-4 territory) | Under-states boss DPS in the same direction as SL-7 |

---

## §7 — ACCEPTANCE (G-B, killable half)

**PRIMARY:** with M-2 landed and **evasion OFF**, the sim player **dies** at the boss tier in a
non-trivial fraction of the 30 seeds. Today: **0/30 deaths, 30/30 wins** (§14.26).

**SUPPORTING (from §A-8.1 row 1, the wave charter's own targets):**
- `worst_drop_pct_maxhp` **≥ 40 %** of pool becomes **possible** (N-11's one-sided existence test).
  §3.2 predicts **52.2 %** at the outer band across the whole `res_cold` sweep.
- share of total intake carried by drops ≥ 10 % EHP reaches **30–65 %** (N-12, carried at
  R2-whole grain with its NOT-RECUT caveat, §A-9.4).

**MANDATORY REPORT REGARDLESS OF OUTCOME:** the §4.3 `d`-at-fire distribution; the nova cast count;
the per-band hit counts; the branch counts for M-1's armor operator on the physical component.

**FALSIFICATION / honorable-miss:** if the player survives 30/30 with the nova landing at ≥ 40 % of
pool on measured casts, the mechanism is built and the **survival** is the finding (sustain economy,
leech, cadence) — report it as such. If the player survives because every cast resolved at melee,
that is §4.3 and it is a **positional** result, not a magnitude one. **The two must not be
conflated in the verdict.**

---

## §8 — BUILD NOTE FOR GAMORA

### 8.1 You own
Implementation math note **before code** (Discipline #1); the tests; **jack-ryan Gate-2, MANDATORY**
(charter §3 — kernel-touching, and this landing touches the CC layer, the telegraph emission path
and the cast-scheduling loop; the KC1 precedent of five operand-class fixes across two Gate-2 cycles
is the calibration for how much this bites).

### 8.2 Landing shape (recommendation; the seam is yours)
1. **Door-scoped**, like M-1 — production-inert, door-closed digest byte-unmoved.
2. **Determinism:** exactly **one** new RNG draw is justified — the `U(1.3, 1.8)` freeze duration.
   The 80 % cast roll consumes an existing decision stream if one exists; if not, name the new
   stream in the math note. **The nova's damage takes NO variance draw** (§2.1 C-flag) — assert it.
3. **Two-phase commit** (§4.2) is the structural piece; build it before the damage numbers, because
   M-3 cannot start until the announce phase exists.
4. **Assertions:** `A-M2-FRZ` (§3.4, both halves) · `A-M2-BAND` (band function is a step function
   over the measured breakpoints; `d > 12.0` ⇒ no hit) · `A-M2-FLAT` (no variance on nova damage) ·
   `A-M2-WIND` (`wind_up_s` present on the nova dict or raise) · `A-M2-LOCK` (caster position at
   `t_announce == t_fire`).
5. **Report** the §7 mandatory set. Report `d`-at-fire even on a pass.

### 8.3 ⚠ ROUTED TO THE CONDUCTOR — extend WR1-WINDUP-GAL's measurement scope
galadriel is already frame-measuring the death-2 nova for windup (R-WR1-9). **Three more quantities
are visible in the same frames at near-zero marginal cost, and each closes a named unknown that
otherwise ships open:**
- **U-M2-1 (multi-hit)** — count damage floaters / HP-bar steps per nova cast. *Reverses M-3's
  entire tactical premise if multi-hit is true.* **Highest value in this list.**
- **U-M2-5 (push)** — measure player displacement across the nova impact.
- **§4.3 cross-check** — Matt's own distance from the caster at each nova, which is the human
  baseline for the `d` distribution the sim will be graded on.

**Signed:** gandalf (`SPEC-AUTHOR`), 2026-07-29. Veto-open per the WR1 ruling ledger.
