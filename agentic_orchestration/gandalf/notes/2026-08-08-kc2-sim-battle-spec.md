# KC2-SIM — battle-sim spec (Phase B draft) — 2026-08-08

**Run:** KC2-SIM (autonomous, desirable-run pattern). **Charter:** `gandalf/notes/2026-08-07-kc2-sim-run-charter.md`. **Ledger:** `gandalf/notes/2026-08-07-kc2-sim-run-ledger.md`.
**Author:** named-gandalf sub-agent, `SPEC-AUTHOR`. **Commissioned:** Phase B open (post-G-A PASS, post-B.1 micro-probe fold).
**Status:** DRAFT — conductor folds at G-B. Tolerances in § 12 are PREFILLED placeholders **pinned at G-B by the conductor**, not by this document. § 11 is **MERGED** — star-lord's redlines R-1…R-39 and drax's SIGNED-as-amended coverage list (23 MUST + 5 SHOULD) folded under rulings **L-25 / L-26 / L-27**; four items remain routed or conductor-flagged (§ 11.6.4).
**Commit state:** UNCOMMITTED by instruction (charter § 4.7 — conductor commits at gate close).

**Consumers:** gamora (`simulation/`, § 1–10) · star-lord (`export/`, § 11) · jack-ryan (Gate-2) · conductor (G-B fold, § 12 pinning).

---

## § 0 — Load-bearing assumptions (framing audit, before any number)

This spec is only as good as five assumptions. Each is named with where its evidence lives, so a
later reader can attack the assumption rather than the arithmetic.

| # | Assumption | Evidence lives at | If false |
|---|---|---|---|
| **A1** | **The fixture is the build-of-record.** Gear, devotions, skills and EoR rank on Matt's `EoRWarlGuts` character are the `b28gD0KN` spec, within a stated envelope. | `gandalf/notes/2026-08-05-eor-ceremony-cross-verification.md` — 13/13 gear slots name-identical; EoR rank 26 both sides; devotion 55/55; Divine Mandate exclusive confirmed. Envelope **+3.9% / −0.5%** (fixture reads *above* spec on every axis but Defensive Ability). | Every calibration row is un-attributable. Claim vocabulary in force: *name-identical; derived within +3.9%/−0.5%*. **"matches 100%" is retired.** |
| **A2** | **Channel constants are build-invariant.** Cadence, radius, channel duration and drain are fixed for every EoR build in the game; gear moves damage, conversion and attack speed only. | P-E1 § 6.3 — corpus-wide negative scan of all **26** EoR-family records; zero occurrences of `timeBetweenAttacks`, `skillTargetRadius`, `duration`, `expansionTime`, `skillManaCost` outside the base record. | § 1's constants become per-fixture and the spec must carry a modifier-resolution layer it currently does not. |
| **A3** | **The corpus and the client join.** Corpus pinned Edition-II 2026-07-24 (patch 1.3.0.0); the sitting ran client v1.3.0.5. | Patch-delta probe 2026-08-04 (zero touches to this build's skills/devotions across 1.3.0.1–1.3.0.5; one Crucible line, at wave 200, outside both fixture bands). L-2 corpus check PASS on all six probes. | Any number here can be one patch stale. Bounded LOW; declared. |
| **A4** | **The Crucible is decidable from Lua + `.arz` + `.arc`.** Wave sequencing, checkpoint semantics, mutator ladder and bonus timer come from Crate's own source comments; composition from the `.arz`; field semantics from `templates.arc`. | L-9 citation-hygiene ladder: `Scripts.arc`/`Conversations.arc` Lua > `.arz` > patch notes > dev guide (stale-checked) > **community wiki BANNED for Crucible wave facts on this client**. | The encounter spec (§ 10) drops to folklore grade. |
| **A5** | **The fixture's two sittings are two different regimes, not two samples of one.** s1 = zero defenses (tribute pinned at 150 across prep + the entire 1→93 ramp, camera-verified). s2 = four positional defenses (Deathchill · Stormcaller · Inferno · Vanguard, one each). | galadriel § 1 + § 1a; L-12(a). | R-KC2-2's binding split collapses. It does not: s1 ramp BINDS (regime-clean), s2 **field outcomes** INFORM only, s2 **kit-internal micro-oracles** (energy, HP-orb) BIND. |

**Two disciplines this spec inherits and never relaxes:**

- **No free parameters** (charter § 4.2). Where a value the sim needs is absent from the probe corpus, this document writes a **named-HALT row** (§ 13) rather than an estimate. A fit failure beyond DB-cited correction is a FINDING, not a tuning target.
- **M1 ≠ M2.** *M1* = Lokarr's fixed checkpoint offers `{50, 100, 150, 180}`. *M2* = the post-death rewind (`wave − 20`, round down to the nearest 10, cost ladder 5/15/30, cap 3). These are different mechanisms and are never blurred.

### § 0.1 — Glossary (terminology pin — GD conflates three things under "tier")

| Term | Meaning here | Range |
|---|---|---|
| **wave** | the global wave counter; what the HUD badge shows | 1 … 200 |
| **content tier** | the 10-wave authoring band; selects the `tier<NN>waves` proxy directory | 1 … 20; tier *n* = waves 10(*n*−1)+1 … 10*n* |
| **rewardTier** | `floor(wave / 10)`; selects loot table, mutator count, bonus-timer bonus | 0 … 20 |
| **tick** | one EoR damage application, `timeBetweenAttacks` apart | — |
| **cycle time** | badge-to-badge interval = spawn + approach + kill for one wave | — |
| **clear time** | cycle time for a wave that ended in a clear (not a death) | — |

At wave 151: content tier **16**, rewardTier **15**. They differ. The sim must not inherit GD's
conflation (U-8 § 5).

---

## § 1 — Channel state machine (gap-table row 1 — BUILD)

### 1.1 Mechanism model

Eye of Reckoning is a **self-refreshing channelled effect** that applies damage in a
player-centred disc on a fixed period, with no cooldown and no channel-duration cap.

```
state ∈ {IDLE, CHANNELLING, TAIL}

on press:            state := CHANNELLING;  effect_expiry := t + 0.25
while held:          effect_expiry := t + 0.25            # useResetsDuration
                     every tick_period seconds: emit DamageTick
on release:          state := TAIL                        # effect persists to effect_expiry
at effect_expiry:    state := IDLE

tick_period(s) = 0.16 × (100 / attack_speed_percent)
```

`skillCooldownTime` is **absent** from the record → 0. `expansionTime` absent → the disc does not
grow over the channel. The 0.25 s `duration` is **not** the tick period; `timeBetweenAttacks` is.

### 1.2 Constants of record

| Symbol | Value | Source |
|---|---|---|
| `timeBetweenAttacks` | **200** (int) | P-E1 § 1.1 → `records/skills/playerclass09/eyeofreckoning1.dbr` [GDX2.arz] |
| DB→engine conversion | **× 0.8 ms / unit** (`period_s = value × 0.0008`) | P-E1 § 1.3 — **two distinct DB values, nine channelled skills, zero exceptions**; corroborated by the sibling field `projectilePeriod` being typed `real`/seconds while `timeBetweenAttacks` is `int` |
| base tick period @ 100% AS | **0.16 s** (6.25 Hz) | P-E1 § 1.2 — the skill's own display tag, verbatim: *"At 100% Attack Speed, Eye of Reckoning deals damage and drains Energy every 0.16s."* `tagGDX2Class09SkillDescription07A` |
| attack-speed law | `tick_period = 0.16 × (100 / AS%)` | P-E1 § 1.4 — **INFERRED (strong)**: DB-CITED that the coupling exists; simple inverse proportionality is the only form under which "at 100% Attack Speed" is a meaningful qualifier. Closes P-E5's OS-2. |
| **fixture attack speed** | **196 %** (Attacks per Second 2.66) | Ceremony cross-verification § D, character-sheet tab II `#511` |
| **fixture effective tick period** | **0.0816 s → 12.25 ticks/s** | DERIVED from the two rows above. *(See FINDING F-3 — this closes P-E1's own open item P3.)* |
| `skillTargetRadius` | **3.0 m**, scalar, no per-rank array | P-E1 § 2. Unit MEASURED-pinned twice against screenshot text in KIT-CAL-1 (`skillTargetRadius = 2.5` → *"2.5 Meter Target Area"*; `= 12.0` → *"12 Meter Radius"*) |
| `duration` / `useResetsDuration` | **0.25 s** / **True** | P-E1 § 1.5 → `SkillChanneled.tpl` include |
| `rotationSpeedMultiplier` | **0.35** — player turns at 35% of normal rate while channelling | P-E1 § 1.5 |
| `canUseWhileMoving` / `delayMovement` | True / True | P-E1 § 1.5 |
| weapon gate | `Mace2h = True`; all ranged/caster types False | P-E1 § 1.5 |
| `skillMaxLevel` / `skillUltimateLevel` | 16 / **26** | P-E1 § 5.2 |

**EoR is cited at TOTAL rank 26 everywhere in this spec, never 15.** Rank 26 closes exactly:
allocated **15** (`player.gdc`) + Gutsmasher +4 + Warborn Visor +2 + Warborn Chestguard +2 +
Sandreaver Bracers +2 + Kaisan's `augmentAllLevel` +1 = **26** = `skillUltimateLevel`
(P-E1 § 5.1; save-parse corrigendum **C-2** — the +11 attribution is Gutsmasher/Visor/Chestguard/
Sandreaver/Kaisan's, **not** an Oathkeeper mastery grant; **no equipped item grants any Oathkeeper
mastery rank**, so the mastery route contributes zero to EoR. The TOTAL-26 conclusion stands on the
corrected arithmetic).

### 1.3 Per-tick damage basis @ rank 26

| Component | Value | Source |
|---|---|---|
| base `weaponDamagePct[26]` | 50 % | P-E1 § 3.1 |
| + Gutsmasher EoR modifier | **+14 %** | `itemskillsgdx2/skillmodifiers/upgradedgdx2/mace2h_d107_eyeofreckoning.dbr` |
| + Warborn set modifier | **+0** — gated OFF | `itemSkillModifierControl = [0,0,0,1]` → **0 at 3 pieces worn**; do not credit the +5 % (P-E1 § 5.3) |
| **weapon damage per tick** | **64 %** | |
| flat physical | 162 – 182 | base `offensivePhysicalMin/Max[26]` |
| + Sandreaver | +24 | `hands_d206_eyeofreckoning.offensivePhysicalMin` |
| flat fire | **138, a point value** | base `offensiveFireMin[26]`. **`offensiveFireMax` is genuinely absent from the record** — model flat, not 138–138 by parser default (P-E1 § 3.1) |
| **Fire → Physical** | **100 % conversion** | Gutsmasher `conversionInType Fire → conversionOutType Physical`, `conversionPercentage 100`. **This is the record field that makes this a physical build.** Any sim modelling EoR as mixed physical/fire is modelling a different build (P-E1 § 6.2) |
| **composed flat, all physical** | **≈ 324 – 344** | components DB-CITED; **composition INFERRED** (application order unresolved — HALT-6) |
| crit damage | +12 % | Warborn Visor `head_d028_eyeofreckoning.offensiveCritDamageModifier` |
| bleed | Gutsmasher 330/3 s (+50 % dmg mod, +100 % duration mod) + Sandreaver 210/3 s | **540 / 3 s pre-modifier** |
| CC resist while channelling | `defensiveCrowdControl` 25 %, `…MaxResist` 25 % | 1.3.0.0 addition, present in the extracted record |

**Sanity anchor (independent lane):** the fixture's own character sheet reads
**Eye of Reckoning `43,691 – 59,761` Damage Per Hit** (ceremony § D, `#511`). That is the composed
in-client number; a sim reproducing the component arithmetic above should land inside it, and any
gap is the § HALT-6 application-order question made visible.

### 1.4 Soulfire — a second cadence, do not fold into the disc

`records/skills/playerclass09/eyeofreckoning2.dbr`, `Class = SkillSecondary_AttackProjectileOrbiting`,
**total rank 15** (allocated 12 + Warborn Pauldrons +2 + Kaisan's +1):

| Field | Value |
|---|---|
| `projectilePeriod` | **0.2** (typed `real`, plain seconds) |
| `projectileExplosionRadius` | 0.2 |
| `skillProjectileNumber` / `projectilePiercingChance` | 1 / 100 % |
| `projectileDirection` / `projectileStart` | Counterclockwise / Front |
| `skillProjectileTargetGroundOnly` | True |
| `offensiveLightningMin[15]` | **246** |
| `offensiveTotalDamageReductionPercentMin[15]` / Duration | **23 %** / 2.0 s (scalar) |

**Gutsmasher converts Fire→Physical only.** Soulfire's damage is **Lightning** despite the name, and
is therefore **un-converted** — this otherwise all-physical build emits a genuine Lightning component
(P-E1 § 6.4). Model it on its own 0.2 s cadence, independent of the 3 m disc. This is the **OS-3**
treatment adopted per L-3.

### 1.5 Acceptance criteria (gamora's tests must demonstrate)

1. **AC-1.1** With `attack_speed_percent = 100`, ticks are emitted at 0.16 s ± one sim-tick over a
   60 s hold; count = 375 ± 1.
2. **AC-1.2** With `attack_speed_percent = 196`, tick period = 0.0816 s; a 60 s hold emits 735 ± 1
   ticks. *(The 196 value is a fixture parameter, not a constant — the law is what is under test.)*
3. **AC-1.3** Release leaves a tail: the last tick may land up to 0.25 s after button-release, and
   never later.
4. **AC-1.4** `tick_period` is invariant under every gear configuration the sim can express
   (A2 regression test — the negative result is testable).
5. **AC-1.5** A target at 3.01 m from the player centre at tick time takes zero damage; at 2.99 m it
   takes one tick. Radius does not change with rank, channel elapsed time, or number of targets.
6. **AC-1.6** With the fixture loadout, per-tick physical flat lands in [324, 344] and weapon-damage
   contribution is 64 % — and **no fire damage is emitted at all**.
7. **AC-1.7** Soulfire emits on 0.2 s, not on the disc's period, and its damage is typed Lightning.

---

## § 2 — Moving circle (gap-table row 2 — BUILD)

### 2.1 Mechanism model

The 3.0 m disc is **self-centred and re-evaluated at every tick against the player's current
position**, while the player is free to move (`canUseWhileMoving = True`). This is the first
player-side skill in the engine whose resolver predicate is *self-centred-while-moving*; boss-side
circles resolve, but they resolve about a stationary or independently-driven origin.

```
at each tick t_k:
    c_k := player_position(t_k)                  # NOT the position at channel start
    hit_set := { e ∈ actors : |e.position(t_k) − c_k| ≤ 3.0 }
    for e in hit_set: apply DamageTick(e)
```

Two handling constraints ride with it, both DB-CITED and both real inputs to how the disc sweeps:

- `delayMovement = True` — movement is impeded while the skill is active (magnitude not stated in
  the record → **HALT-2**).
- `rotationSpeedMultiplier = 0.35` — the player turns at **35 %** of normal turn rate while
  channelling. This caps how fast the disc can be *re-aimed* and is a genuine constraint on the
  sweep path, not flavour.

**Run speed:** the fixture reads **135 %** (ceremony § D). That is a modifier; the base rate in
m/s is not in the read set → **HALT-2**.

### 2.2 Truth boundary (R-KC2-7)

The player path and the circle sweep are **sim-owned causal truth** and are baton payload
(§ 11.4). Presentation owns locomotion *aesthetics* — how a monster's approach between spawn and
engagement is choreographed — within the constraints the baton fixes. The sim therefore emits the
player's position at a stated sample rate, and the disc centre is that position: presentation must
never re-derive the sweep, because re-deriving it would let the picture disagree with the damage.

### 2.3 Composition + telegraph law

- Composes with the arena shell in § 10.6 (6 emitters, `placementExtents = 8.0` scatter, single
  player spawn).
- **BR-2 G-1h law applies to the player's kit for the first time:** the telegraph fields the sim
  emits must be sufficient for an independent function to reconstruct hit/no-hit from the telegraph
  alone. For a self-centred moving disc that means `{centre_position, radius, tick_time}` per tick —
  not a single "channel active" flag with a duration.
- **RECON RESOLVED (conductor fold, ledger § B.2/L-16):** row 2 re-verified at launch HEAD
  `ebf13240` — verb stays **BUILD** (BR-2 *exposed nova resolver semantics*; it did not build a
  player-centred moving disc). **Geometry-family law (L-16 — Phase-C BINDING):** the spin is a
  TRUE uniform disc (`skillTargetRadius = 3.0`, per-tick 360°) and must **NOT reuse the engine's
  nova family** — the nova resolver is ground-truth **SIXTEEN CORRIDORS**
  (`spatial_engine.py:6569–6576`); disc↔corridor conflation = **3.076× lethal-area error**
  (147.06 vs 452.39 m² measured). The spin mechanism declares its OWN geometry family + `shape`
  value; telegraph consumers adopt the dual-family + shape-boundary match pattern (`shape`
  semantics shifted at `16fa7e8d`: nova→"star", wave→"trapezoid"; selector-repair precedent
  `wr2_cell_bat_2026_07_29.py:262` — matching on `shape` alone silently blinds).

### 2.4 Acceptance criteria

1. **AC-2.1** A target stationary at 4 m, with the player walking past it, takes damage on exactly
   the ticks during which the separation was ≤ 3.0 m — verified against a recomputation from the
   emitted telegraph alone (the G-1h bar).
2. **AC-2.2** The disc centre in the emitted trace equals the player position at the same tick
   timestamp, for every tick, to sim-position precision.
3. **AC-2.3** Turn rate while `CHANNELLING` is 0.35 × the idle turn rate.

---

## § 3 — Energy drain (gap-table row 3 — EXTEND)

### 3.1 The drain — CLOSED ON CAMERA (L-22): per-tick, attack-speed-scaled, **176.4 / s** at the fixture

The fork is closed. galadriel's follow-up sweep found the EoR skill tooltip **inside the s2 video**
(t ≈ 193–240, skill-window open), verbatim:

> *"At 100% Attack Speed, Eye of Reckoning deals damage and drains Energy every **0.16s**"* ·
> **Energy Cost: 176.4 per Second** · Current Level **15 + 11 = 26**.

**The number decomposes EXACTLY** — one line validates per-tick, AS-scaling, and the rank read at once:

```
drain_unit = PER_TICK                          # PINNED (L-22) — hook retained, enum frozen
drain_rate_per_s = skillManaCost[26] × ticks_per_s(AS) × cost_factor
                 = 16.0 × 12.25 × 0.90 = 176.4   @ the fixture's 196 % AS   (client-verbatim)
per_tick_effective = 16.0 × 0.90 = 14.4
```

- **PER-TICK confirmed (M2):** the tooltip computes its cost line at *current* stats — 176.4 / 12.25
  ticks/s = 14.4 per tick. M1 (16/s flat) is refuted **twice over**: by the tooltip figure and by
  F-3's income arithmetic (16/s gross against 75.37/s regen pins the bar at the ceiling; the observed
  86–117 draw-down at wave 158 is unproducible). Two independent instruments agree.
- **The ×0.90 cost factor is measured-exact, source UNLOCATED** — no "−% Energy Cost" line surfaced
  in the ceremony sheet or build notes; candidates are gear/component/augment cost reduction
  (grimtools `b28gD0KN` could locate it). Non-blocking: the client-computed 176.4 governs; the sim
  carries `cost_factor = 0.90` as a fixture constant with this provenance note.
- **Sustain arithmetic (now decidable):** gross −176.4/s + regen 75.37/s = **net −101.0/s before
  leech** ⇒ **Tip the Scales (100/s while up, 2.0 s duration, 1.0 s cooldown) is LOAD-BEARING for
  sustain** — near-continuous uptime nets ≈ −1/s, reproducing the draw-down-then-recovery band.
  AC-3.2 tests exactly this.
- **Soulfire carries a SEPARATE, DECLARED cost term NOT inside 176.4** (the decomposition's exactness
  is the evidence). Its own `skillManaCost` is 3–20 rank-scaled (P-E1 § 5, build MAXES the node);
  fine print: *"Energy Cost increase is per damage interval"*; interval basis **CLOSED at 0.2 s plain
  seconds** (HALT-8, L-26). **Magnitude tension, declared:** a naive max-rank read (20 / 0.2 s =
  100/s) would break the fixture's own observed sustain — so the term's *effective* magnitude is
  bounded above by the fixture's sustain band, and Phase D adjudicates via AC-3.2's FINDING clause.
  The sim carries the term declared-and-separate; it is never folded into `drain_rate_per_s`.

**Resolution ladder (L-6) — final disposition:** (a) galadriel sweep **CLOSED IT** (in-video tooltip
beats any still) · (a′) energy-direction read **MOOT** · (b) matt_to_do T14 screenshot
**SHORT-CIRCUITED**, row annotated · (c) DUAL-BOUND fallback **retired unused**.

### 3.2 Reservation — the part that binds regardless of the fork

The fixture's energy globe reads **1594 / 2576** at four timestamps spanning 830 s of footage
(`s2-full-200`, `-500`, `-1000`, `-1030`), and **1508 / 2576** at wave 158 in active combat
(P-E1 § 4.4). A value that recurs identically across 830 s is a **ceiling**, not a coincidence:

```
reserved ≈ 2576 − 1594 = 982        # exclusive-aura reservation
usable_ceiling ≈ 1594
observed sustained-combat draw-down: 86 – 117 below the ceiling, then recovery
```

**The reservation is now ATTRIBUTED EXACTLY — 982 = 982 (HALT-5 CLOSED, bundle § 3.3, L-26).**
P-E1's 624 was a *rank understatement*, not a missing skill; the genuinely missing source was
**Presence of Might (component skill), 300 flat**; and **Divine Mandate reserves ZERO**
(`characterManaLimitReserve = 0.0` — exclusivity and reservation are independent mechanics). The
unique solve (mastery-wide offsets O = +1, S = +4, one cell of 81; cross-validated by EoR total = 26
on an unrelated instrument):

| Source | total rank | reserve |
|---|---:|---:|
| Presence of Virtue 1 / 2 / 3 | 18 / 10 / 11 | 220 / 100 / 107 |
| Field Command 1 / 2 | 14 / 12 | 205 / 50 |
| Presence of Might (component) | 1 | **300** |
| Divine Mandate (exclusive, non-reserving) | 13 | **0** |
| | **TOTAL** | **982** vs observed 2576 − 1594 = **982** |

`reserved = 982` thereby graduates **BINDING-as-observed → BINDING-and-derived**: the sim reproduces
it from the DB rather than hard-coding the globe reading, making AC-5.2 (deactivating an aura returns
exactly its reserve) *testable*. **`characterManaLimitReserveModifier` is non-zero on ZERO records
corpus-wide — that term is dead in § 5.2's formula.** The reserve mechanic itself stays
MEASURED-pinned in prior art (`characterManaLimitReserve = 50.0` → *"50 Energy Reserved"*).

**Income terms the sim must carry** (otherwise the fork looks decidable when it is not):

| Term | Value | Source |
|---|---|---|
| Energy Regeneration | **75.37 / s** | Ceremony § D `#511` — *(closes P-E1's open item P4; see FINDING F-3)* |
| Energy Absorption | 20 % | Ceremony § D `#511` |
| Tip the Scales leech | **200 energy over 2.0 s = 100 / s while up**, `skillCooldownTime = 1.0 s` | P-E5 § 2.3 |

### 3.3 Micro-oracles (BINDING per R-KC2-2)

| Oracle | Value | Grade |
|---|---|---|
| energy ceiling / max | **1594 / 2576** | BINDING (attribution-clean, kit-internal) |
| s2 in-combat energy | **1477 / 2576** | BINDING (R-KC2-2 names it explicitly) |
| sustained-combat draw-down below ceiling | 86 – 117 | BINDING as a band |
| reservation | **≈ 982** | BINDING |

### 3.4 Acceptance criteria

1. **AC-3.1** With auras active, `energy_max_usable = energy_max − reserved`, and the sim's usable
   ceiling reproduces **1594** given `energy_max = 2576` and the modelled reservation.
2. **AC-3.2** Under a continuous channel with the pinned drain (**PER_TICK, 176.4/s at 196 % AS,
   L-22**) and the fixture's regen + leech terms, energy settles into a band **86–117 below** the
   usable ceiling and does not floor out. The **Soulfire cost term rides declared-and-separate**
   (§ 3.1): if no declared-term combination reproduces the band, **that is a FINDING for the
   conductor, not a licence for the sim to retune** (charter § 4.2).
3. **AC-3.3** Flipping `drain_unit` changes exactly one derived quantity (`drain_rate_per_s`) and no
   structural behaviour — the resolution hook is proven by test, not asserted.
4. **AC-3.4** A dry-out event (energy insufficient at a tick boundary) emits a distinct reason code
   and terminates the channel; the fixture is expected to produce **zero** of these
   (Matt's silence on "out of energy" across both sittings is itself the finding).

---

## § 4 — Righteous Fervor charge-stacks (gap-table row 5 — EXTEND) → **DISSOLVES**

**Disposition: this row dissolves against the endgame fixture, exactly as the block row does
(§ 7). The sim models nothing here.** This is a FINDING for the conductor (F-1), because the
charter § 3 Phase-B row list carries it as a live EXTEND row.

**Evidence, two independent lanes:**

1. **Save-parse § 2.2 — measured absence.** The fixture holds ranks on **28 player-class skills**;
   the enumerated list is Soldier `_classtraining_class01`, `warcry1/2`, `fieldcommand1/2`,
   `passive1–4`, `blitz1/2`, `fightingspirit1`, `willtolive1` and Oathkeeper
   `_classtraining_class09`, `eyeofreckoning1/2`, `presenceofvirtue1/2/3`, `divinemandate1`,
   `summon_celestialguardian1`, `summon_celestialguardian2_petmodifier`, `ascension1/2`,
   `viremight1/2/3`, `passive02`. **`righteousfervor1` is not among them.** The same note records
   **0 of 318** common skill entries changed across the save migration (2,226 field comparisons,
   2,226 identical) — so this is a measured zero, not a parse gap.
2. **Build-of-record § 1.6 — never prescribed.** The V1 ordered acquisition list names every skill
   the build touches. Righteous Fervor is absent from it.

**Why the row existed.** Gap-table row 5 reads *"Window 1 is fought with THIS, not EoR"* — that is
**v2-spine inheritance**, written when the fixture was a level-13→20 leveling character for whom EoR
had not yet arrived. The v3 ENDGAME-FIRST ruling (Matt: *"we need to play test end game"*) replaced
that character with an L100 build-of-record that never allocates the skill. The row is a survivor of
a superseded premise.

**Standing residue, declared:** Righteous Fervor remains a *genre-legitimate* mechanic and P-E2 (its
template probe) was never fired. Nothing in this run needs it. If a future lap wants
default-attack-replacer charge stacks in RDR, it starts from a fresh probe, not from this spec.

**Acceptance non-requirement:** gamora writes **no** RF tests. A test asserting RF absence in the
fixture loadout is acceptable as an A1-regression guard and nothing more.

---

## § 5 — Auras and permanent buffs (gap-table row 6 — EXTEND)

### 5.1 The fixture's buff surface, measured

From the grimtools `Buffs (4/13)` modal on camera (ceremony § E, `#387`) cross-read against the
save's allocated ranks (save-parse § 2.2):

| Class | Skills | Note |
|---|---|---|
| **Permanent** | **Divine Mandate** · Field Command · Presence of Virtue · Presence of Might (item — Seal of Might) | **Divine Mandate is the V1 discriminator** — it is the check that would most cleanly have caught a wrong-variant build (V4 runs Oleron's Rage instead) |
| **Activated** | Ascension (10 s) | allocated `ascension1/2` = 1/1 |
| **Triggered** | Menhir's Will (100 % at 33 % health) · Fighting Spirit (30 % when hit) · Resilience (5 s) | Menhir's Will appears at `Current Level : 1 + 4` (`#525`) — **granted, not allocated**; the § 1.6 "don't allocate Menhir's Will" trap is respected and the save confirms `menhirswill` absent from the allocated set |

### 5.2 The mechanism the sim must model: **reservation**

Divine Mandate is an **exclusive** aura. The load-bearing behaviour is not its damage bonus — it is
that it **removes energy from the usable pool permanently while active**:

```
energy_max_usable = energy_max − Σ characterManaLimitReserve(active auras)
                                − energy_max × Σ characterManaLimitReserveModifier(active auras)
```

Fixture instance: `2576 − ≈982 = 1594` (§ 3.2). **A sim that models auras as pure stat grants and
not as pool reservations will fail the v1 energy micro-oracle regardless of how the § 3 drain fork
resolves** — which is exactly why R-KC2-2 named the ceiling/reserve read as attribution-clean and
binding.

Reserve constants (P-E1 § 4.4), at **total** ranks:

| Skill | field | value |
|---|---|---:|
| `presenceofvirtue1_buff` | `characterManaLimitReserve` @16 | 200 |
| `presenceofvirtue2` | `characterManaLimitReserve` @10 | 100 |
| `presenceofvirtue3` | `characterManaLimitReserve` @11 | 107 |
| `fieldcommand1buff` | `characterManaLimitReserve` @11 | 175 |
| `fieldcommand2` | `characterManaLimitReserve` @9 | 42 |
| | **enumerated total** | **624** |
| | **observed reservation** | **≈ 982** |
| | **unattributed residual** | **≈ 358 → HALT-5** |

*(Note the two rank scales in play: the save stores **allocated** ranks — `presenceofvirtue1` = 12,
`fieldcommand1` = 10 — while these reserve values are quoted at **total** rank after gear. This is
the same allocated-vs-total discipline that forces EoR to be cited at 26. Never compare a `.gdc`
rank to a grimtools rank.)*

### 5.3 What the sim models this lap

- **Reservation** — modelled, binding (above).
- **Permanent auras as always-on stat sources** — modelled at their composed character-sheet values
  rather than reconstructed per-skill, because the composed values are MEASURED (ceremony § D) and
  the per-skill composition order is HALT-6. Declared simplification.
- **Ascension (activated, 10 s)** — **DECLARED OUT-OF-MODEL this lap.** It is a piloting decision
  with no recorded activation ledger in the read set; folding it in would put an undeclared piloting
  parameter inside a calibration band. If G-D diagnosis implicates burst windows, this is the first
  pre-registered place to look.
- **Triggered buffs (Menhir's Will / Fighting Spirit / Resilience)** — **OUT-OF-MODEL**, declared,
  same reasoning as the defensive-trigger devotion procs (§ 9): their rate is a function of the
  opposition model, and this lap does not model procs.

### 5.4 Acceptance criteria

1. **AC-5.1** With the fixture aura set active, usable energy ceiling = 1594 given max 2576.
2. **AC-5.2** Deactivating a reserving aura returns exactly its reserve to the usable pool
   (reservation is reversible and not double-counted).
3. **AC-5.3** The out-of-model set (Ascension, triggered buffs) appears by name in the baton
   provenance block, so a consumer can see what the number does *not* contain.

---

## § 6 — Pack opposition (gap-table row 7 — COMPOSE) · **RECON RESOLVED (§ B.2/L-16)**

### 6.1 Disposition

This row **composes on existing engine machinery** — it is the one row in the table whose verb is
COMPOSE, and charter § 9 is explicit: pack opposition composes on Lane-2 arena/horde machinery at
HEAD, **no double-build**. What this spec supplies is the *content* (roster, counts, scalars,
arrival choreography); what the engine supplies is the multi-actor substrate.

**RECON RESOLVED (conductor fold, ledger § B.2/L-16):** row 7 re-verified **CONFIRMED** at launch
HEAD `ebf13240` — 8/8 gap-table rows verb-intact at HEAD, zero GONE. The COMPOSE verb stands on
live machinery; no double-build.

| Gap-table claim (v2 § II.2 row 7) | Status |
|---|---|
| boss / champion / trash tiers exist | **CONFIRMED at HEAD** — tier structure live in the encounter-AI surface (§ B.2 row-7 grade) |
| full-mix battery exists | **CONFIRMED at HEAD** (within § B.2's row-7 CONFIRMED grade) |
| `wr3_encounter_ai_v1` (M1/M2/M3) exists | **CONFIRMED at HEAD** — `wr3_encounter_ai.py:175+`, m1/m2/m3 sub-flags |
| roster comes from the dense room's measured pools | **superseded here** — roster comes from P-E6's Crucible emissions (§ 10.4), not from the SoT dense room; the window moved to the Crucible per R-V3-3 |

### 6.2 Content the sim binds against

| Input | Source of record |
|---|---|
| per-wave composition (pools, rosters, weights, record paths) | **P-E6 emissions** — `pe6_crucible_wave_pools.csv` (1,998 rows), `pe6_crucible_waves.csv` (200 rows), `s4_waves_full.json` |
| per-wave counts | **U-9 count model** (§ 10.5) — *"count from U-9, composition from P-E6"* is declared in both notes |
| per-wave monster scaling | **U-8 emission** `u8_survival_wave_scaling.csv` — joined via the **§ 10.7 array-lookup law: fighting wave *w* reads the row labeled *w−1*** |
| monster level | **TWO-STAGE (HALT-10, § 6.2b):** the proxy `levelVarianceEquation` sets spawn level — nemesis/boss `lv8_boss+` is a **POINT**, `(apl+4)+(apl/50)` = **106** at L100 (P-E6's band read + its 104 corrected: min = max; the `apl/50` term was dropped) — then the **monster record's own `charLevel` equation re-evaluates it** (four forms on the wave-160 board; the `(charLevel*1.1)+2` form → **118.6**). Hero `lv6_hero`, trash `lv2_normal`/`lv3_strong`. **No player-level gate on tier access**; at L100 every `minPlayerLevel{j}` roster gate is open (P-E6 § 2.7). **No Epic/Legendary variance branch exists** — 0 of 16 proxy records populate them |
| boss concurrency | **engine cap explicitly defeated.** `survivalevent.lua` L548 verbatim: `Proxy.Create(…, …, true) -- true for 'ignore boss spawn limit'`, on **every** wave spawn. Campaign boss-concurrency intuitions do not transfer (U-9 § 5.5) |

### 6.2b Opposition eHP — the five-link composition chain (HALT-10; L-29)

**CLOSED for the nemesis class (±0.005 %); PARTIAL for the p04 superboss (named gap).** Probe:
`legolas/notes/2026-08-08-kc2-ehp-composition-probe.md`. Sim-ready numbers:
`legolas/scratch/2026-08-08-kc2-ehp-composition/t20_wave160_board_ehp.csv` — **the sim consumes the
`glad_cell = 322` rows** (per the § 10.7 array-lookup law; the 324 rows are the labeled-cell
alternative, retained for provenance).

```
apl        = averagePlayerLevel = 100                  (fixture is L100)
spawn_lv   = levelVarianceEquation(apl)                records/proxies/lv*.dbr        [base]
charLevel  = <per-record equation>(spawn_lv)           monster record field           [overlay winner]
base_life  = characterLife(charLevel)                  bio curve (characterAttributeEquations)
M          = 1 + 5.80 + G/100 + own/100                ADDITIVE — see below
eHP        = base_life × M
```

- **Two-stage level.** Stage 1 sets spawn 106 (nemeses; point, not band). Stage 2 — the record's own
  `charLevel` equation — splits the board four ways: `*1` (106) · `*1+2` (108) · `*1+5` (111) ·
  **`*1.1+2` (118.6** — 10 of 16 nemeses; ×1.172 on base HP through the ^1.5 curve). This is the term
  a shared-base model could not produce: 15/16 nemeses share `bio_boss_nemesis_01` but NOT the
  `charLevel` equation.
- **Five bio curves on the wave-160 board:** `bio_boss_nemesis_01` `((cl*42)^1.5)+20000` (16 records) ·
  `nemesis3phase_01/02/03` `((cl*36)^1.5)+16000` / `((cl*19)^1.5)+9000` / `((cl*13)^1.5)+3000`
  (**Kubacabra is 3-phase — P1→P2→P3 eHP 2,955,749 → 1,162,010 → 636,671 at the 322 cell; the sim
  needs all three**) · `colossusgalakros` + `tombguardian` `((cl*33)^1.5)+500` · `hero_standard_01`
  `((cl*11)^1.5)−20` (≈ 398,747–404,406).
- **M is ADDITIVE:** `1` + **5.80** (ordinary Ultimate/solo —
  `balancingadjustment_mp+difficulty_enemies01.characterLifeModifier[8] = +580` `[base]`, wired by
  `gameengine.monsterAttributePak`; the P-E6 line-377 phrase *"before ordinary Ultimate difficulty
  scaling"*, now a number) + **G/100** (Gladiator wave cell per § 10.7 lookup: **322** while fighting
  160) + **own/100** (per-record `characterLifeModifier`: **+100 on Raddoth only**, 0 on the other 22).
  Multiplicative composition gives 28.83 — **−61 % wrong**. The DB's own additive statement:
  `characterLifeMultModifier` — the only multiplicative life term in the adjustment layer — is **0 at
  solo** on every difficulty.
- **Verification (conductor re-run independently):** back-solved M = **10.019603 (F1) / 10.020158
  (F2)** — two fingerprints through two different power-law curves (42 vs 36 coefficient, 20000 vs
  16000 constant) agree to **0.006 %**; residuals at the 322 cell **+0.004 % / −0.002 %**
  (noise-shaped, opposite-signed) vs **+0.204 % / +0.198 %** (systematic, same-signed) at 324.
- **Exclusions, measured:** monster rank (Hero/Boss/SuperBoss) carries **NO HP term anywhere in the
  corpus** (H2 NAMED-ABSENT — all 366 `gameengine.dbr` fields read; rank differentiation is bio choice
  + `charLevel` equation, nothing else); the `armorbaseNN` passive's 200-cell `characterLifeModifier`
  is **empirically EXCLUDED** from the life composition (including it breaks the exact closure by
  +13.9 %/−9.6 % and demands a level no record can produce); **mutators are neither wired into the
  Crucible nor needed** (H4 — zero proxy/pool/wave references to `records/game/mutators/` corpus-wide).
- **⚠ Overlay law:** bios resolve through the eight-archive survival stack **last-wins**
  (`base→gdx1→gdx2→gdx3→sm_mod→sm1→sm2→sm3`). **Two live wave-160 traps:** `colossusgalakros` (gdx1
  `((cl*55)^1.53)+6000` vs the governing sm1 curve) and `tombguardian` (gdx2 vs sm2) — a
  campaign-stack join returns a wildly different curve. Same class as P-E6 § 5.2's werewolf trap, but
  these two are ON the board.
- **p04 NAMED GAP:** Galakros @110 predicts 2,196,440 (322 cell) vs measured 2,295,755 = **−4.3 %**
  (−4.1 % at the 324 cell; the Steward −10.6 %); closing it needs charLevel ≈ 113.3 and the DB permits
  ≤ 110; nine candidate explanations ruled out by reading, none by fitting. **Declared ±5 % band on
  the p04 slot** (§ 12 T-8) — INFORMATIVE-side only (no p04 slot exists in the BINDING s1 band);
  galadriel board-closure question in flight (§ 10.8).
- **Scale of the correction:** measured wave-160 board floor ≈ **9.4 M** eHP (three fingerprints +
  hero) vs ≈ 4.1 M under the superseded flat model — opposition health was understated **~2.3×**.
  *(Supersedes L-17's interim per-nemesis 1,308,800 figure and P-E6 § 4.1's ≈ 827 k; the corrected
  nemesis band is 3.18 M – 3.73 M, 4.10 M for Raddoth.)*

### 6.3 Monster-side damage — the declared ceiling

**All monster damage figures reachable from this corpus are UPPER BOUNDS.** P-E6's § 4 statlines
quote array-max across 60-rank damage arrays; **the rank binding at any given wave is unread**
(P-E6 gap G-2). Per L-11 this is:

- **second-order for BINDING rows** — s1 clear-times and the micro-oracles bind on *player-side*
  truth;
- **first-order only for INFORMATIVE s2 intake** — which R-KC2-2 already downgraded and L-12(a)
  already flagged as confounded by two defense-side intake debuffs.

A targeted rank-binding probe is the **pre-registered contingency** if G-D diagnosis implicates
monster damage. It does not fire pre-emptively.

**Also HALT-7:** converting a monster skill payload into player HP loss needs GD's mitigation model
(armour absorption curve, resistance application order, flat-vs-percent ordering). That model is not
in the read set.

### 6.4 Acceptance criteria

1. **AC-6.1** For any (wave, difficulty) the sim can instantiate, the set of monster records it
   spawns is a subset of the P-E6 roster for that wave and spawn point, with pool selection weighted
   as emitted.
2. **AC-6.2** Expected body count per wave reproduces § 10.5's model to the integer, for all 20
   waves of the 151–170 calibration window.
3. **AC-6.3** Concurrent bosses are not capped.
4. **AC-6.4** Every emitted monster carries its source record path — so any statline dispute is
   resolvable without re-running (R-BR-34 census rule).
5. **AC-6.5** The § 6.2b chain reproduces the two measured nemesis-class fingerprints — **3,722,896**
   (F1) and **2,955,796** (F2, Kubacabra P1) — within **±0.05 %** under the § 10.7 lookup law, and
   places the p04 slot inside its declared ±5 % band. Structural guard: the composition is ADDITIVE —
   a multiplicative build overshoots ×2.9 (M 28.83 vs 10.02) and must fail this test.

---

## § 7 — Block (gap-table row 4 — PARAMETERIZE) → **DISSOLVES**

**Disposition: dissolved. The fixture cannot block. The sim models no block for this fixture, and
the WR3 mitigation door stays where it is.**

The fixture wields **Gutsmasher**, an Augmented Legendary **Two-Handed** Mace (144–740 damage,
1.46 APS) — confirmed name-identical to `b28gD0KN` on camera (ceremony § A, slot 1). A two-hander
occupies the off-hand slot; there is no shield.

**Measured, not inferred** — ceremony § D, character-sheet Defense tab (`#519`):

```
Chance to Block   0%
Damage Blocked    0
Block Recovery    0%
```

The ceremony note calls this out in its own words: *"`Chance to Block 0%` is an independent
structural confirmation of the two-hander: no shield slot in play."* Three zeroes on the instrument
that would show a non-zero if one existed.

**Consequence for the gap row.** Row 4's prescription was *"un-force `block_chance` behind a door;
block recovery cadence needs a probe"* — and P-E3 (the Soldier-block probe) was never fired. Neither
action is needed for this fixture: the door forcing `block_chance = 0.0` produces **exactly the
correct behaviour** here. The row is deferred, not solved, and it is deferred honestly: a
shield-bearing fixture would reopen it and would need P-E3 first.

**Acceptance non-requirement:** gamora writes no block tests beyond a guard asserting the fixture's
`block_chance == 0.0`.

---

## § 8 — Retaliation — **EXCLUDED**

**Disposition: EXCLUDED by the gap table (row 8) and re-affirmed here. Declared, not silently
dropped.**

Three reasons, in descending weight:

1. **Build-rule exclusion.** Gap-table row 8 records retaliation as *"explicitly unwired"* and
   excluded by build rule § 2.3. v3's PART II table restates it: *"Row 8 Retaliation — still
   EXCLUDED (V1 is the physical-hit spin; V5's bleed-conversion variant was explicitly rejected as a
   different BC-axis signature)."*
2. **The fixture's retaliation is incidental, and small relative to its output.** Ceremony § D
   Retaliation tab reads **Physical 1008**. Compare the same sheet's **Damage Per Second 20,233** and
   **Eye of Reckoning 43,691–59,761 per hit**. Retaliation is not a damage lane of this build; it is
   a residue of Ulzaad's Decree (`retaliationPhysicalMin/Max = 205 / 450` while the 10 s buff is up)
   and passive sources.
3. **Modelling it would import an unmodelled dependency.** Retaliation output is a function of
   incoming-hit rate — the same opposition-model dependency that widens the defensive-trigger
   devotion error bars (§ 9.3). Excluding it keeps that dependency in exactly one place.

**Not excluded, and not confused with it: monster-side retaliation.** The Crucible balancing records
carry a `retaliationTotalDamageModifier` on the *enemy* side. That is an opposition property the
Crucible room needs and the SoT room does not — and its value is contested across two sources
(**FINDING F-4**). It is carried in § 10.7 as opposition data, not here.

**Acceptance non-requirement:** no retaliation tests. The baton provenance names retaliation in its
out-of-model list so a consumer cannot mistake its absence for a zero measurement.

---

## § 9 — Devotion contribution envelope (R-KC2-1 ruling (d))

### 9.1 Scope, ruled

**No proc mechanism is built this lap.** Per R-KC2-1 (Matt: *"I agree with (d)"*), this section is
**descriptive** plus a **contribution envelope** — uptime × magnitude per power, with error bars
stated. Baton damage is **kit-native**, and the envelope is declared in the baton provenance so a
consumer knows what the damage number does and does not contain.

The RDR receiving-surface re-grill is **GATED+TRACKED** on an empirical criterion: *measured
proc-share in hand.* This run produces it.

### 9.2 Envelope discipline (L-3) — three rules, binding

- **(a) NO invented ICDs.** Where `skillCooldownTime` is **absent** from a record, it is modelled
  **absent**, not zero-and-then-quietly-capped. P-E5 § 3.1 is flat about this: **there is no
  internal-cooldown field on any of the 176 autocast controllers in the corpus** — a plausible-
  looking "global proc ICD" is exactly what an envelope model invents when it needs one, and the
  corpus does not contain one.
- **(b) Defensive triggers carry wider, opposition-model-dependent error bars, declared.** Two of
  seven powers fire on `HitByEnemy` — when the **player** is hit. Their uptime is a function of
  incoming hit rate, i.e. of the opposition model. *(The controller basenames read `onanyhit`,
  which is easy to misread as "any hit you land." The `triggerType` field is the authority.)*
- **(c) Shifting Sands is carried DUAL-BOUND** — two orders of magnitude apart — until a probe closes
  P-E5's gap G-6. Both bounds go in the disclosure.

### 9.3 The seven powers — trigger, rate ceiling, payload, envelope

All seven bindings cross-verified **DB ⟷ save 7/7** (P-E5 § 3.2). Ranks are **save-measured at DB
max, 7/7, XP byte-exact** — and **no allocated-vs-total ambiguity exists for devotions**: 0 of 93,190
records grant +skill to a devotion power (P-E5 § 1.2–1.3).

| # | Power → host | Trigger (`triggerType`, chance) | Rate ceiling | Duration | Payload @ fixture rank |
|---|---|---|---|---|---|
| 1 | **Assassin's Mark** → Eye of Reckoning | `AttackEnemyCrit`, **100 %** | **no cooldown — field ABSENT from both records** | 18.0 s | `defensivePhysical −32` · `defensivePierce −36` (target resistance reduction). No damage component. Single-target by structural discriminator (`Skill_AttackBuff`, one-field wrapper; the AoE variant is `Skill_AttackBuffRadius` + `pointBlank`) |
| 2 | **Turtle Shell** → Field Command | `LowHealth`, `triggerParam 50.0`, 100 % | 1 per **8.0 s** | **NOT IN THE CORPUS → HALT-1** | `damageAbsorption 6100`, **unfiltered** (all six damage-type qualifiers False → absorbs everything) |
| 3 | **Tip the Scales** → Presence of Virtue | **`HitByEnemy`**, 33 % — **DEFENSIVE** | 1 per **1.0 s** | instant (+ riders) | 310 vitality · **132 % ADCtH** · 33 % weapon damage · **−20 all resist / 3.0 s** · **200 energy leech / 2.0 s** |
| 4 | **Maul** → Vire's Might | `AttackEnemy`, 20 % | **no cooldown — ABSENT**; **host-limited**: Vire's Might `skillCooldownTime = 3.5999999 s` | 5.0 s | 305 physical · 45 % ADCtH · **`defensiveProtectionModifier −35 %`** (target armour) · radius **4.5**, `pointBlank`, unlimited targets in radius |
| 5 | **Arcane Barrier** → Divine Mandate | **`HitByEnemy`**, 30 % — **DEFENSIVE** | 1 per **3.0 s** | **no duration exists — absorb-POOL** (HALT-1 CLOSED, L-26: the `.tpl` declares none) | `damageAbsorption 2900`, **FILTERED**: aether · chaos · elemental · life · poison qualifiers True. **Physical, Pierce and Bleed are NOT in the qualifier set** |
| 6 | **Ulzaad's Decree** → War Cry | `AttackEnemy`, 20 % | 1 per **22.0 s**; host War Cry `skillCooldownTime = 7.5 s` | **10.0 s** | **+200 % Physical · +200 % Pierce · +200 % Internal Trauma** · +42–45 flat physical · +190 armour · +205–450 physical retaliation |
| 7 | **Shifting Sands** → Summon Celestial Guardian | `AttackEnemy`, 20 % — **host is `Skill_TargetedSpawnPet`** | 1 per **0.5 s** *(if player-side)* | 1.0 s projectile life | 205 physical · 335 pierce · 30 % weapon · +40 % crit damage *(caveat: on an attack record, parsimonious reading is the projectile's own — a player-wide grant is a materially different contribution, not DB-decidable)* · **−140 OA / 3 s** · **25 % impaired aim / 3 s**. Geometry: 1 projectile, max 5 concurrent, 100 % pierce, 2.0 explosion radius |

### 9.4 Envelope arithmetic, per power

**1 — Assassin's Mark: saturates. Uptime ≈ 100 % on any engaged target.**
Chance 100 %, no cooldown, 18 s duration. Saturation on a single engaged target requires only
`P(crit) ≥ 1 / (18 s × tick_rate)`. At the fixture's **12.25 ticks/s** that threshold is
**0.45 %** — a floor so low that any plausible crit rate clears it, and the fixture's Offensive
Ability is **3,259** against nemesis base DA **715** (P-E6 § 4.1). *(An exact P(crit) is not
derivable from the read set — HALT-3 — but the envelope does not need one, because the bound is
one-sided and the margin is three orders.)*
**The interesting quantity is therefore not uptime but *breadth*: how many distinct targets carry
the mark.** That turns on **OS-1** (per-tick vs per-target-struck trigger generation) and is
**OPEN-SEMANTIC**. DB evidence bearing on it, offered without a ruling: the controller carries
`targetType = Enemy` **and** `autoTargetRadius = 22.0` — it performs its own target selection
within 22 m, 7.3× EoR's own 3.0 m damage radius. A trigger that selects its own target argues
against per-target-struck; the controller schema carries no "targets per fire" field, so this is a
lean, not a proof.
→ **Envelope: −32 physical / −36 pierce resistance on the primary engaged target, ≈100 % of engaged
time. Breadth: 1 target (OS-1a/c) to N-in-radius (OS-1b). Declared.**

**2 — Turtle Shell: rate-ceilinged and state-triggered.**
Ceiling 1 per 8 s, but the trigger is a **state predicate** (health ≤ 50 %) rather than an event, so
realized rate is a function of incoming-damage volatility, not attack cadence. The fixture's health
is 20,005 and s1 ran the entire 1→93 ramp with one death.
→ **Envelope: ≤ 6100 unfiltered absorption per 8 s, realized rate ≈ 0 outside near-death windows.
Shield lifetime unknown (HALT-1) — the envelope is stated as a per-proc pool, not a per-second rate.**

**3 — Tip the Scales: DEFENSIVE, wide bars, and load-bearing for § 3.**
Ceiling 1 per 1.0 s × 33 % chance per incoming hit. In a Crucible pack with continuous incoming
hits the ceiling is the binding constraint, not the chance.
→ **Envelope: up to 100 energy/s leech and −20 all-resist with 3 s duration on a 1 s cooldown ⇒
near-continuous resistance shred and a large energy income term. Error bar: opposition-model
dependent — declared per L-3(b).** This is the term that makes the § 3 drain fork empirically hard;
it is also the term fordprefect's own build rationale points at (*"You need Scales for energy
regen"*).

**4 — Maul: the lowest-frequency offensive proc in the kit.**
Host-limited, not chance-limited: Vire's Might can offer at most 1 trigger per 3.6 s, and 20 % of
those fire.
→ **Envelope: ≤ 0.056 procs/s ceiling (1 / 3.6 × 0.20), and lower still if Vire's Might is not used
on cooldown — a piloting parameter, declared. Contribution: −35 % target armour for 5 s in a 4.5 m
disc, plus 305 physical.** The armour debuff is worth more to a physical-hit spin than the damage is.

**5 — Arcane Barrier: DEFENSIVE, and the 2900 is TYPE-GATED AWAY from this fixture's threat profile.**
Ceiling 1 per 3.0 s (`skillCooldownTime = 3.0`, scalar). **Envelope re-run with the gate applied**,
per the HALT bundle's record read (`legolas/notes/2026-08-08-kc2-halt-bundle-microprobe.md` § 7.3 →
`records/skills/devotion/tier2_17c_skill.dbr`): the record carries five `*DamageQualifier` flags —
**aether · chaos · elemental · life · poison** — and **Physical, Pierce and Bleed are not among
them.** The Crucible opposition this fixture dies to is predominantly physical, so the *realized*
contribution against the damage that actually kills it is **≈ 0, not 2900**. Sibling contrast from
the same read: Turtle Shell carries **no qualifiers at all** and absorbs everything — which is why
the two must never be summed.
→ **Envelope: ≤ 2900 per 3 s against aether/chaos/elemental/life/poison ONLY; ≈ 0 against the
physical/pierce/bleed intake that dominates this fixture's threat profile. Do not pool it with
Turtle Shell's unfiltered 6100 — the two are materially different defensive contributions and the
qualifier gate is the reason. Error bar: opposition-model dependent — declared per L-3(b).**
*Class note (same bundle, § 7.2, HALT-1 CLOSED): `Skill_BuffSelfShield` declares no duration field
anywhere in its template chain — these are absorb-**POOLS**, spent by damage rather than expiring on
a timer. "Per 3 s" is therefore a **proc-rate ceiling on a pool**, never a duty cycle.*

**6 — Ulzaad's Decree: the cleanest analytic bound in the kit, and it is a duty cycle.**
Hard ceiling = duration / cooldown = **10.0 / 22.0 = 45.45 %**, reached only if the 20 % trigger
fires in the first instant of every cooldown expiry. War Cry offers a trigger at most every 7.5 s, so
if the pilot uses War Cry on cooldown the expected inter-proc interval is 7.5 / 0.20 = 37.5 s, giving
a practical duty cycle of **10 / 37.5 ≈ 26.7 %** (DERIVED; the War-Cry-on-cooldown premise is a
**declared piloting parameter**, not a measurement).
→ **Envelope: +200 % physical / pierce / internal-trauma damage for 26.7 %–45.45 % of combat time.
This is the largest single damage-side devotion term in the kit and the one whose envelope is
genuinely uptime-shaped rather than rate-shaped.**

**7 — Shifting Sands: DUAL-BOUND, two orders apart (L-3(c)).**
The host is `Skill_TargetedSpawnPet` (Summon Celestial Guardian, `skillCooldownTime = 20 s`). An
`AttackEnemy` trigger on a summon either **delegates to the 2 Guardians** — in which case the 0.5 s
cooldown is the binding constraint and the proc is high-rate — or it fires **~once per 100 s** on the
host's own attack events. The corpus carries a devotion-pets record lane, which is *consistent with*
delegation but not probative (P-E5 gap G-6).
→ **Envelope, both bounds carried:**
  - **upper (delegated):** ≤ 2 procs/s ceiling (1 / 0.5 s), i.e. a continuous secondary damage +
    −140 OA + 25 % impaired-aim debuff stream;
  - **lower (host-only):** ≈ 0.01 procs/s — negligible.
  **The spread is ~200×. Nothing in this run resolves it, and the envelope disclosure carries both.**

### 9.5 Envelope disclosure block (reusable verbatim in the baton provenance)

```
devotion_envelope_disclosure:
  ruling: R-KC2-1(d) — no proc mechanism modelled this lap; baton damage is kit-native
  powers: 7, all at DB-max rank, save-measured, XP byte-exact, bindings DB<->save 7/7
  icd_policy: NO invented internal cooldowns. skillCooldownTime absent on
              Assassin's Mark and Maul => modelled absent (L-3a).
              The corpus contains no internal-cooldown field on any of its
              176 autocast controllers.
  saturating:
    - assassins_mark: uptime ~100% on engaged target (threshold P(crit) >= 0.45%
                      at 12.25 ticks/s); BREADTH open on OS-1
  duty_cycle_bounded:
    - ulzaads_decree: 26.7% (War-Cry-on-cooldown premise) .. 45.45% (hard ceiling)
  rate_ceilinged:
    - tip_the_scales:   <= 1 / 1.0 s   [DEFENSIVE trigger - wide bar]
    - arcane_barrier:   <= 1 / 3.0 s   [DEFENSIVE trigger - wide bar; FILTERED,
                                        absorbs nothing vs physical/pierce/bleed]
    - turtle_shell:     <= 1 / 8.0 s   [state-predicate trigger; shield lifetime HALT-1]
    - maul:             <= 1 / 3.6 s x 0.20 = 0.056/s  [host-limited]
  dual_bound:
    - shifting_sands:   delegated <= 2/s   vs   host-only ~0.01/s   (~200x, P-E5 G-6)
  open_semantics:
    - OS-1: per-tick vs per-target-struck trigger generation  [affects mark breadth]
    - OS-3: does the Soulfire orbital count as an attack event [affects trigger rate]
  error_bar_classes:
    - defensive_triggers: opposition-model dependent (Tip the Scales, Arcane Barrier)
    - piloting_parameters: War Cry cadence, Vire's Might cadence, Ascension usage
```

### 9.6 Acceptance criteria

1. **AC-9.1** The sim emits **no** proc damage events. A non-zero proc-damage total is a spec
   violation, not a bonus.
2. **AC-9.2** The envelope disclosure block above is present, verbatim and complete, in every
   emitted baton's provenance.
3. **AC-9.3** No modelled quantity anywhere in the sim carries an internal cooldown for Assassin's
   Mark or Maul (L-3a, testable as an absence).

---

## § 10 — Crucible encounter spec (the wave engine)

### 10.1 The ladder — 200 waves, twenty tiers

**The Crucible runs to wave 200. This is R-KC2-4's measured answer** (L-7; U-8 CLOSED).

Tier *n* covers waves 10(*n*−1)+1 … 10*n*. Tiers 1–15 ship in the base Crucible, 16–17 in AoM
(`SurvivalMode1`), **18–20 in FoA (`SurvivalMode3`)**. Proven by a three-cut corpus differential
(two independent pre-FoA cuts carry tiers 1–17 *only*; the FoA cut carries 1–20; 90 of tier-18's
monsters absent from tier 17), plus `eventFinished()` terminal-callback placement, plus four
external developer/publisher corroborations.

**"Cash out at 170" is RETIRED as framing.** Cash-out is offered at **every** 10-wave boundary
(`npc_event_02.cnv` → `eventFinishedCashOut()`, and Crate's own guide says so verbatim). 170 was
merely the *pre-FoA terminal wave*. On the fixture's 1.3.x client nothing ends at 170.

**Honesty flag, carried into any re-derivation:** the reward tables and the per-wave scaling record
have **always** been 200 rows, byte-identical pre/post-FoA. **Length proves the design ceiling, not
playability.** Do not stack these as independent ceiling evidence — the ceiling stands on the tier
differential + `eventFinished()` + patch notes.

### 10.2 Start-wave invariant — **`first_wave_fought = label + 1`**

```
start_wave_label ∈ {0 (Standard), 50, 100, 150, 180}     # the PARAMETER takes the LABEL
first_wave_fought = start_wave_label + 1                 # the ENGINE applies the +1
```

"Start on Wave 150" sets the counter to **151** and suppresses exactly one increment — Crate's own
comment reads `-- Start the Event at Wave 151`. **A sim starting AT 150 would run one extra wave and
mis-tier the entire run.**

Two-lane confirmation, Lua and camera:
- **M1 side:** galadriel measured the s2 badge reading `0` through the 11-minute prep, flipping to
  **151** at t = 682.10 — 0.05 s after Lokarr's dialogue closed, with "Start on Wave 150" highlighted
  under the cursor. **This was the run's first pre-registered falsifiable prediction, and it PASSED.**
- **M2 side:** the s1 wave-93 death → checkpoint restart returned the badge **pre-set to 70**
  (93 − 20 = 73 ↓ 10 → 70), which is the same invariant implemented the other way (pre-set the label,
  let the increment fire).

**Downstream relabel (L-7):** the s2 calibration band is **"waves 151–160 fought"** in every
artefact — galadriel timelines, spec bands, baton provenance. *(Matt-ruling verbatims are untouched;
the substance is the band he played.)*

### 10.3 Run control — simplified, DECLARED

| Surface | Sim behaviour | Grade |
|---|---|---|
| start wave | parameter, takes the **label**; engine applies +1 | modelled |
| offer set | **FIXED static list `{50, 100, 150, 180}`**, ungated since v1.2.1.3 (checkpoint tokens RETIRED for offers; the *difficulty* gate is separate and still live, amended v1.3.0.0 to wave-110/160 triggers) | modelled as a constant |
| lives | **single life.** No M1/M2 fidelity | **DECLARED SIMPLIFICATION** |
| M2 rewind | not modelled (formula recorded: `wave − 20`, round down to nearest 10; cost ladder 5/15/30, cap 3) | **DECLARED OUT-OF-MODEL** |
| defense structures | **not modelled** | **excluded by charter** (§ 10 ARCHITECT gate: RESOLVED, excluded) |
| blessings | not modelled — **fixture bought zero, both sittings** | measured zero, not an omission |
| tributes / score / rewards | not modelled | **DECLARED OUT-OF-MODEL** |

**Defense permanence — recorded so nobody re-derives an expiry model (L-15b).** All 15 defense DBRs
carry `lifeTime = 0` (a field that is live elsewhere in the corpus), there are zero `spawnObjects*`
references corpus-wide, and Crate's own comment reads *"permanently saved into the world once
spawned."* **The four s2 defenses were ACTIVE at the wave-160 death.** galadriel's flagged
first-order confound on that death is dead. This does not change the exclusion — it changes what the
exclusion *means*: s2's field outcomes are confounded for the whole run, not for part of it.

**Mutators — OUT-OF-MODEL, declared (L-15c, L-12e).** The ladder is confirmed at full grain:
`SurvivalEvent_SelectMutators` by `rewardTier` — `≥17 → 7 · ≥15 → 6 · ≥13 → 5 · ≥11 → 4 · ≥9 → 3 ·
≥6 → 2 · ≥3 → 1 · else 0`. The fixture ran **SIX** (2 player + 4 monster) at rewardTier 15; the
five-icon camera read is display-side (icon pane authored 300 px = five 48 px icons; galadriel's
140 px crop covered 47 % of it). **Identities were never extracted** — prior is a 25-pool (an
off-by-one bug makes Voidmarked and Vengeful unselectable). Mutators reroll every 10 waves.
**This is a live, unquantified per-decade confound in BOTH sittings, and models must not fold it into
noise.**

**One-wave tier-override quirk, declared-ignore.** After an M1 start, mutators / bonus-timer /
trap-rate use the *checkpoint's* tier for exactly one wave. At a 151 start both sides yield 6
mutators, so the declared-ignore is clean **for this fixture's start config** and only for it.

**Bonus timer — recorded, not modelled.** Formula DB-CITED (`SurvivalEvent_StartBonusTimer`):
`T = (1 / (multiplier + 1)^0.49) × (defaultTimer + rewardTier × tierBonus)`, Gladiator
`defaultTimer = 80000 ms`, `tierBonus = 12000 ms`; **SET per wave, not accumulated**. Upward vectors
between waves: hero kill **+4000 ms**, boss **+8000**, nemesis **+12000**. Closed by pre-registered
prediction: 185.13 s at a wave-151 Gladiator start → **03:02 predicted at t = 685, 03:02 read on
camera**. The **kill-class fingerprint (+3 / +7 / +11 net of countdown) decodes kill classes while
the timer runs** — noted as a census aid for the wave-160 window (838.87 → ~919), not as a sim
mechanism.

### 10.4 Composition — source of record

**Composition = P-E6. Count = U-9.** The division of authority is declared explicitly in both notes
(P-E6 § 4.6; U-9 § 6) and adopted at L-10(a).

| Emission | Rows | Content |
|---|---:|---|
| `legolas/scratch/2026-08-07-pe6-crucible/pe6_crucible_waves.csv` | 200 | per-wave: `tier`, `tier_wave`, `spawn_points`, `ambush_points`, `raw_min/max/E`, `glad_adj_min/max/E`, `n_trash/boss/hero/devotion/bounty`, `nemesis_wave`, per-difficulty E |
| `…/pe6_crucible_wave_pools.csv` | 1,998 | per-wave-per-spawn-point: proxy class + record, `legendary_override`, pool record, weight, kind, `spawn_min/max`, `champion_chance/min/max`, full roster names **and record paths** |
| `…/s4_waves_full.json` | — | full nested (12.7 MB) |

**925 spawn proxies → 632 pools → 1,617 monster records, ZERO unresolved references, all 200 waves,
all three difficulty views, both priority bands at per-pool grain with record paths.**

Resolution is three-hop and the engine picks **exactly one** weighted alternative per spawn point:

```
proxy_wWW_pPPa.dbr   [Class: Proxy (818) | ProxyAmbush (107)]
   └─ pool{i} / poolEpic{i} / poolLegendary{i}      weighted ALTERNATIVES — pick ONE
        └─ proxypool record
             spawnMin, spawnMax, championChance, championMin, championMax
             name{j} / weight{j} / limit{j} / minPlayerLevel{j} / levelVarianceEquation{j}
             nameChampion{j} / weightChampion{j} / limitChampion{j}
             └─ records/creatures/enemies/**.dbr   [Class: Monster]
```

**TWO difficulty views only.** 29 of 925 proxies carry `poolEpic{i}`/`poolLegendary{i}` overrides;
of the 28 sites carrying both, **28/28 are identical** — Challenger ≡ Gladiator. Only Aspirant
differs, on **24 of 200 waves** (22 of them at wave ≤ 65; only wave 150 falls inside the priority
bands, and the fixture never fought it). Binding: base pools = Aspirant · `poolEpic` = Challenger ·
`poolLegendary` = **Gladiator**.

**Dangling roster references (G-7): dropped and weights renormalised** — 4 slots of ~7,000, one
alternative at wave 93. Cited here so the renormalisation is not silent.

**Hero-pool edge (U9-8), declared:** hero pools carry no `name1..N` regular roster, so a Gladiator
`spawnMin +1` on a hero pool is modelled as spawning **zero** regulars. ≤1 monster per hero
placement; the plausible engine behaviour, not a measurement.

### 10.5 Count model — U-9, verbatim in structure

```
per spawn point, per wave, Gladiator, solo:

if pool.ignoreGameBalance:                      # 74/632 pools — ALL of them boss pools
    n_min, n_max = pool.spawnMin, pool.spawnMax
    c_min, c_max = pool.championMin, pool.championMax
else:
    n_min = floor( (pool.spawnMin + 1 + adj03.spawnMinAdj[w]) * 120/100 )   # adj == 0 for all w
    n_max =        pool.spawnMax + 1 + adj03.spawnMaxAdj[w]                 # adj == 0 for all w
    if n_min > n_max: n_min = n_max                                         # clamp-min-down
    c_min = pool.championMin + 1 + adj03.spawnChampionMinAdj[w]             # = +2 for w >~ 68
    c_max = pool.championMax + 1 + adj03.spawnChampionMaxAdj[w]             # = +2 for w >~ 52

regulars  = randint(n_min, n_max)
champions = randint(c_min, c_max) if rand() < pool.championChance/100 else 0

wave_total = Σ over ACTIVE spawn points     # 1–5 always; 6 only if bonus spawns enabled
```

Five load-bearing facts inside that model:

1. **`spawnMinModifier` is a MULTIPLIER where 0 AND 100 both mean "no change."** Gladiator's `120` =
   **× 1.20**, not `+120` and not `× 2.20`. Decisive source is **not** the `.arz` — it is
   `database/templates.arc` field annotations in Crate's own English: *"Percent (0 or 100) no
   change."* This kills the ×2.20 reading that would have roughly **doubled** the densest calibration
   wave.
2. **`spawnMaxModifier` is declared-but-unset** — the ceiling moves by the **+1 additive only**.
3. **`ignoreGameBalance` exempts 74/632 pools, and every exempt pool is a boss pool.** No trash or
   hero pool is ever exempt. (All 36 FoA boss pools are exempt; only 18 of 96 base-game ones are.)
4. **Champions ADD, they never convert** (Crate, modding guide, verbatim). Census: 515 pools have
   `championChance = 0` and no champion roster; 117 have both; **zero** have a roster with chance 0 —
   so the champion gate is safe to model as a hard gate.
5. **Waves 151–170 hero placements spawn THREE heroes each**, exactly: `championMin' = 1 + 1 + 1 = 3`,
   `championMax'` likewise. `championMinModifier`/`MaxModifier` are unset, so this term is purely
   additive — no rounding, no clamp. Over waves 151–170 that is an expected **63.0 champions against
   292 regulars ≈ 18 %** of the wave population.

**No player-count scaling exists anywhere in the chain.** All 632 Crucible pools reference the
identity `proxypoolequation_01.dbr` (`poolValue * 1` on all four outputs), and the multiplayer
attribute paks carry no `spawn*Adj` fields at all. GD's MP scaling is a *stat* scalar, not a *count*
scalar. The sim carries no such term.

**Declared residual — 1.9 %.** Intra-order (add-then-multiply vs multiply-then-add), rounding mode
and clamp direction are each genuinely undecidable from the shipped data. All four surviving
branches over waves 151–170 spread **5.5 monsters on 292 = 1.9 %**; 12 of the 20 calibration waves
are identical under all four; the largest single-wave divergence is 2 monsters. **A/floor with
clamp-min-down is adopted.** *(The cheapest full-green option — one screenshot-countable Gladiator
wave with a pool of `base_min ≡ 4 (mod 5)` — was ASSESSED NOT-WORTH-A-LAP at L-14.7: 1.9 % ≈ 0.3 s on
a median wave, dominated ×3 by the ±1.0 s timing floor.)*

**U9-6 RESOLVED — p06 is ON; the ±8.4 % branch is RETIRED (L-21).** p06 is **player-opt-in**
(`survivalevent.lua`: *"final spawn point is for bonus spawns, player chooses to enable this"*;
achievement + `SURVIVALMODE_GLADIATORBONUSSPAWNS` token corroborate), declared on 13 of the 20 waves
151–170 worth +8.4 % (292.0 → 316.5). **galadriel's wave-160 body census measured the state:**
max-simultaneous **5** distinct hostiles (4 skull-tier + 1 star-tier) at t = 850.87/852.87 — the
5th body **is** the p06 hero slot (4-body branch excluded on two independent instruments; 6 distinct
HP fingerprints across the wave, two pairs simultaneous). The rung-2 one-liner to Matt is **MOOT**;
the sim runs **p06 = ON** as the fixture parameter, recorded in baton provenance.

**Design finding, transferable, parked for RDR difficulty design:** `spawnMinModifier` is
**variance suppression, not volume**. Deterministic (width-0) pools go **68 % → 93 %** from Aspirant
to Gladiator. Gladiator escalates by *removing the downside roll*, not by raising the cap — the
player experiences "always the bad case" instead of "sometimes a worse case."

### 10.6 Arena shell — 6 parameterised emitters, positions DECLARED

**Arena geometry is mostly NOT DB-resident, and the sim must not go looking for it.** The database
gives structure; it does not give coordinates. `Levels.arc` holds the geometry and **zero**
`.wrl`/`.map`/`.lvl` files exist in the fetch. A field-name sweep across all four survival archives
for `position|worldpos|coord|spawnloc|location|levelname|mapname` returns only UI-bitmap offsets.

| Element | Value | Source |
|---|---|---|
| emitters | **6 named spawn points**, `tier<NN>spawnpoint01..06.dbr` (`Class: ScriptEntity`, script hooks only) | P-E6 § 6.3 |
| scatter | **`placementExtents = 8.0`** on all 925 proxies | P-E6 § 2.3 |
| proxy render | `scale = 2.0`, `mesh = proxybounty01.msh` on all 925 | P-E6 § 2.3 |
| **p05 = the ambush point** | **107/107 both directions**, byte-identical params at every site: `minGroupSize = maxGroupSize = 30`, `spawnThreshold = 15`, `minSpawnTime = maxSpawnTime = 3.0 s`, `minDelayTime = maxDelayTime = 4.0 s`, `alertArea = 100.0` | P-E6 § 2.5 |
| **p06 = the bonus point** | player-elected toggle; hangs off the *rewards* script namespace, not the wave namespace | P-E6 § 2.6 / U-9 § 5.4 |
| player entry | **one** `playerspawnpoint` | P-E6 § 6.3 |
| other fixtures (not modelled) | 5 spawn beacons · 7 defense points + 7 NPCs · 8 trap points · 5 reward chests · 2 bonus chests · 1 event NPC · 1 merchant NPC | P-E6 § 6.3 |

**p05 arrival model (adopted, G-4 declared):** p05 emits **its pool count, staggered on a 3 s cadence
beginning at t + 4 s** — not instantaneously with the other points. The `maxGroupSize = 30`
concurrency cap never binds in the Crucible because p05 pool budgets run 3–11. *(Whether
`maxGroupSize` caps concurrency independently of the pool budget is not determinable from the
database — flagged, safe model adopted.)* **Check RETURNED (L-21): galadriel confirmed the
t + 4.0 s p05 start ×3 (s1 waves 4/6/13, wave 13 clean); the 3 s intra-drip cadence sits below the
minimap instrument's resolution — the adopted model stands unfalsified with its start anchor
MEASURED.**

**Emitter positions: provenance DECLARED, footage-estimable, never DB-hunted (L-10d).** The sim
carries six position parameters and one player-spawn parameter as **free, declared** inputs. They
intersect R-KC2-7 cleanly: the sim owns causal spatial truth **on a declared-parameter arena**, and
the baton records the parameter values it ran with so the Godot session builds the same arena.

**Footage-estimated bearings (L-21, grade ESTIMATED-FOOTAGE ± 15°) — TWO ARENAS, NEVER POOLED.**
galadriel's spawn-direction extraction shows the two sittings ran **different arenas**: s1 arrivals
bear ≈ 3.0 / 5.2 / 6.9 / 9.6 o'clock; s2 wave-151 bears ≈ 9.9 + 2.2, and wave-160's four arrival
bearings read 1.8 / 10.5 / 4.5 / 7.5. **Position parameters are per-sitting sets; calibration bands
load their own sitting's set; the baton pins the arena it ran** (`arena_id` + the six bearings +
player spawn). Pooling bearings across sittings is a spec violation, not a modelling choice.

### 10.7 Wave scaling — the U-8 emission is the HP/damage basis

`legolas/scratch/2026-08-07-u8-tierwave/u8_survival_wave_scaling.csv` — **600 rows
(200 waves × 3 difficulties) × 9 scaling columns**, version-stable pre/post-FoA. The sim joins on
`(wave_fought − 1, difficulty)` — see the **array-lookup law** below.

Columns: `characterLifeModifier` · `characterOffensiveAbility` · `characterOffensiveAbilityModifier` ·
`characterDefensiveAbility` · `characterDefensiveAbilityModifier` · `characterAttackSpeedModifier` ·
`characterSpellCastSpeedModifier` · `characterLifeRegenModifier` · `characterPercentHealIncreaseModifier`.

**`characterLifeModifier` is WAVE-INDEXED, not a difficulty constant.** Gladiator values at the
waves this run cares about:

| wave | 1 | 50 | 93 | 100 | 150 | 151 | 155 | 160 | 161 | 170 | **171** | 180 | 200 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Gladiator `characterLifeModifier` | 95 | 110 | 156 | 168 | 304 | 306 | 314 | **324** | 326 | 344 | **420** | 510 | 990 |

**⚠ This table supersedes the "Gladiator scalar block" as folded at ledger § A.6. See FINDING F-2 —
the folded block is the wave-100 slice of a 200-row array, and applying it at wave 160 understates
monster HP by 1.58×.**

**⚠ ARRAY-LOOKUP LAW (L-29; INFERRED-TESTED, single-point): fighting wave *w* reads the row LABELED
*w−1*** (0-based array index *w−2* — the engine indexes the survival adjustment by **completed**
waves). Measured: the wave-160 big-three HP fingerprints back-solve M = 10.0196/10.0202 across two
different power-law bios (0.006 % agreement) — matching the label-159 cell (`characterLifeModifier`
**322**) at **+0.004 %/−0.002 % (noise-shaped, opposite-signed)** vs the label-160 cell (324) at
**+0.204 %/+0.198 % (systematic, same-signed)**. "Footage was wave 159" is excluded on bio census —
neither measured bio exists anywhere on the 159 board. Consequences, **conductor-verified against the
full-grain CSV**: (a) life while fighting 160 = **322**; (b) `offensiveTotalDamageModifier`
**plateaus at 43 across labels 158–160** — the +43 figure is UNCHANGED (the probe note's "+43 → +41"
consequence claim is **STRUCK**: no cell in the family carries 41); (c) at the ladder end, fighting
200 reads label-199 — life **965** (not 990), total-damage **+125** (not +130; the label-200 row is
read by no fought wave); (d) **decade walls land one fought-wave later than their labels** — fighting
171 reads label-170 (**344**); the 420 cell binds while fighting **172**. Boundary: fighting wave 1
has no label-0 row — engine behavior UNKNOWN, declared (sim clamps to label-1; negligible at that
band). **One rule for EVERY array in the `enemies0{1,2,3}` family.** Pre-registered G-D diagnostic:
a damage-side misfit at exactly-one-cell granularity re-opens this rule. Distinct fact from L-7's
`first_wave_fought = label + 1` start invariant — two different off-by-one semantics, both measured,
no contradiction.

**Full grain for the remaining wave-varying fields (HALT-9 CLOSED, L-26):**
`legolas/scratch/2026-08-08-kc2-halt-bundle/halt9_survival_wave_scaling_full.csv` (600 × 28 — all
**25** array fields × 3 difficulties; scalars in `halt9_survival_scalars.csv`, 8 × 3; **33** non-zero
fields total, not ~35; all 9 U-8 columns byte-identical). Headline ramps the wave-100 slice hid:
**`offensiveTotalDamageModifier` = +43 % while fighting wave 160** (not +20; unchanged under the
lookup law — the 43 plateaus across labels 158–160; **+125 while fighting wave 200**);
**`offensivePhysicalModifier` = −21 %** at wave-160 Gladiator (not −15; also unchanged — labels
159/160 agree). The sim joins this CSV on `(wave_fought − 1, difficulty)` per the array-lookup law,
exactly as it does the U-8 nine.

**Wave 171 is a step discontinuity, not a continuation** — Gladiator jumps **+76 pp in one label**
(344 → 420) where labels 161–170 stepped ~+4 pp each. The FoA band is a deliberate wall. Under the
array-lookup law the wall **binds while fighting 172** (fighting 171 still reads label-170's 344).
Relevant to full-ladder runs beyond the fixture bands, which are reported UNBOUND per charter Phase D.

**Fixture calibration bands:**

| band | waves | grade | source |
|---|---|---|---|
| **A** — s1 attempt 1 | **1 → 93 fought**, death at 93 | **BINDING** (regime-clean: zero defenses, camera-verified) | galadriel § 2.3 |
| **B** — s2 | **151 → 160 fought**, death in wave 160 | field outcomes **INFORMATIVE**; kit-internal micro-oracles **BINDING** | galadriel § 2.2; R-KC2-2; L-7 relabel |

*(s1 attempt 2 — the checkpoint-70 restart — contributes **zero** timed waves. All s1 aggregates are
A1-only.)*

**Band landmarks for the calibration table (P-E6):** band A Σ raw E = **1,600.4 over 93 waves**;
wave **87** = density peak (E 33.8); **51 / 65 / 89 / 90** = collapse waves (0–4 bodies, pure
champion/boss); **89** = the only pure-boss wave; **90** = the Crucible's first nemesis wave
(Benn'Jahr, solo); **91** up to 39 bodies; **92** up to 32 + four bosses; **93** = a
hero-saturation wave (nine of ≤10 bodies champion-tier) fought immediately after the band's two
densest waves. Band B Σ raw E = **137.6 over 10 waves**, nemesis at {154, 160}. **Wave 150 is
retained in the sim's table but excluded from sitting-2 reconstruction** — and it is the heaviest
nemesis wave below 170 (three independent nemesis rolls). *The fixture started FROM the band's
heaviest wave without fighting it.*

**Curve shape, for Phase-E narrative-shape selection:** the Crucible **does not get denser; it gets
harder per body.** Trash ΣE peaks at decade 121–130 (217.7) then halves by 191–200, while nemesis
waves go 0 → 8-of-10. **Inflection ≈ wave 150: a volume test before, a boss gauntlet after.**

### 10.8 Wave 160 — the showcase, and how it is rolled

**Wave 160 is the first wave in the Crucible to put three independent nemesis rolls + a superboss +
a hero on the board simultaneously with zero trash.** It is also the wave that killed the fixture —
**death at t = 864.75, 25.88 s into the wave** (L-23; the earlier 943.60 / "104.73 s" read was the
post-death menu view, corrected on the hourglass + UI-clear evidence).

| point | pool | picks | `ignoreGameBalance` |
|---|---|---|---|
| **p01** | `poolsboss/nemesis_all` (`spawn 1-1`) | **1 of 10, uniform** — Valdaran · Benn'Jahr · **Zantarin** · Fabius · Moosilauke · Iron Maiden · Raddoth · Curate Ignus · Shriek · Vinn | **True — exempt** |
| **p02** | `poolsbossgdx1/nemesis_all_noaetherialvanguard` (`1-1`) | **1 of 5** — **Kubacabra (the fixture's MEASURED draw — F2 unique-bio fingerprint, L-29)** · Grava'Thul · Reaper of the Lost · The Underking · Reaper of Rot | **True — exempt** |
| **p03** | `poolsbossgdx1/nemesis_wendigooraetherialvanguard` (`1-1`) | **1 of 2, 50/50** — **Archmage Aleksander** · Reaper of the Lost | **True — exempt** |
| **p04** | `aetherialcolossus_galakros` (w 100) **/** `korvaaktombguardian` (w 100) | 1 of 2 pools, 50/50 — Galakros · The Steward | field absent → **takes the additives** |
| **p06** | `poolsherogdx1/wendigocannibal_hero`, `championChance 100 %` | 1 of 5, uniform — **measured ON in the fixture (L-21 census)** | **False (explicit)** → **takes the additives** |

**There is no p05 — no ambush drip. All arrive together.**

**Measured wave-160 census (L-21/L-23/L-29 — the fixture's own kill wave, instrumented and now
IDENTIFIED under the § 6.2b chain):**

- **Max-simultaneous 5 hostiles** (4 skull-tier + 1 star-tier) at t = 850.87/852.87 — matches the
  5-raw roll with p06 ON. **Six distinct HP fingerprints** across the wave (two pairs simultaneous).
- **The big three, identified (L-29):**
  **F1 = 3,722,896 ≈ the `×1.1`-group nemesis prediction 3,723,043 (−0.004 %)** — candidates:
  Benn'Jahr · Curate Ignus · Shriek · Vinn Ozmald (p01) · Reaper of the Lost (p03). **NOT Zantarin**
  (his `×1` group predicts 3,176,863) and **NOT Raddoth** (own +100 → 4,094,605).
  **F2 = 2,955,796 ≈ Kubacabra P1, predicted 2,955,749 (+0.002 %)** — `bio_boss_nemesis3phase_01`
  is **unique on this board**, so **the p02 draw is SETTLED: Kubacabra**, 3-phase eHP chain
  2,955,749 → 1,162,010 → 636,671 at the 322 cell.
  **F3 = 2,295,755 = the p04 slot** — Galakros favoured (−4.3 %; Steward ≈ −10.6 %) — the § 6.2b
  **named gap**, declared ± 5 % band.
- **Third-nemesis accounting (OPEN — galadriel board-closure question, Phase-C-concurrent):** three
  nemesis slots spawned three nemeses; only two appear in the big three. Either the fingerprint
  list is top-N and the third nemesis hides in the remaining three values, or **both non-Kubacabra
  nemeses drew `×1.1`-group and deduped** (one fingerprint, two bodies, both at 3,722,896 — prior
  P ≈ 0.20). **Prediction menu:** dedupe ⇒ remaining three = {1,162,010 (Kuba P2) · 636,671
  (Kuba P3) · ~398,747–404,406 (hero)} and Zantarin + Aleksander + Grava'Thul were ALL absent;
  else one remaining value ∈ {3,176,863 (`×1` group, incl. Zantarin) · 3,261,498 (Valdaran) ·
  3,389,926 (Aleksander) · 4,094,605 (Raddoth)} **identifies the third nemesis directly**.
- **Kill ledger before the death:** counter steps +12 (t 853.2) / +7 (854.5) / +11 (864.5) decode as
  **2 nemesis-class + 1 boss-class killed pre-death** (± 1 display quantization). **Phase-credit
  caveat (L-29):** Kubacabra is 3-phase and the timer-credit semantics of a phase transition are
  UNKNOWN — the ledger may be counting phase deaths, not distinct bodies. Declared, not modelled.
  The fixture died fighting the survivors at 25.88 s in.
- **The killing blow is a one-frame burst:** 20,005 → 0 in ≤ 0.100 s (~17,900 in one 1/60 s frame) —
  exceeding every quoted single-hit raw ⇒ multi-hit-same-frame or an unquoted skill; this is the
  G-5 identification's quantitative face, carried in baton provenance alongside the Death-Revenant
  contradiction. *(Grava'Thul's 6,729-chaos quote is MOOT for this board — p02 went to Kubacabra.)*
- **Board eHP floor (L-29): ≈ 9.4 M measured** (F1 + F2-P1 + F3 + hero ≈ 404 k) — **≥ 2.3× the
  superseded 4.1 M-class model**; **≈ 13.1 M if the dedupe-twin holds.** Every TTK / narrative-shape
  judgment about the death wave was understated by at least that factor before HALT-10 closed.

```
bodies:  5 raw   |   <= 7 under full modifier application
         three nemesis slots are EXACTLY ONE EACH regardless (explicit exemption)
```

**RULING IN FORCE (L-11): the sim models wave 160 as an all-champion, no-trash burst wave ROLLED
HONESTLY FROM THE POOLS — never a scripted Zantarin reenactment.**

The reasons are worth carrying, because the temptation to script it is real:

- The save banks `greatest-monster-killed[2].last-monster-hitBy = tagNemesis_OrderDeathsVigil01` =
  **Zantarin, the Immortal**, who is in the wave-160 p01 pool at **exactly p = 0.100**. Zantarin's
  kit *is* a precise counter to a channelled melee spin: Curse of Frailty (−30 vitality resist,
  −75 % run speed, 10 m, 6 s), a 12 m death aura, a 2 s-cooldown vitality nova ≤ 2,888, and a
  **passive that retaliates against every incoming hit with a global attack-speed and run-speed
  slow** — the exact anti-pattern for a build whose damage is hits-per-second in contact range.
- **But the identification does not close (G-5).** The sibling save field
  `last-monster-hit = "Death Revenant"` names a monster **not spawnable at wave 160** (nearest: 153,
  155). The two fields cannot both date from 160. Write-cadence is unverified, and Zantarin's own
  wave-150 presence is p = 0.311.
- **The co-credible killer set is RESTRUCTURED by L-29.** Grava'Thul is **ELIMINATED** — the p02
  slot measurably went to Kubacabra (F2 unique-bio fingerprint), so his Nullification kit was never
  on this board. *(Note the elimination rests on the p02-slot argument alone — Grava'Thul is
  himself `×1.1`-group at 3,723,043, so eHP could not have distinguished him.)* Archmage Aleksander
  (p = 0.50 on p03) remains co-credible — 4,893-aether meteors into the classic Warlord hole — but
  his candidacy now **rides the remaining-fingerprints check**: his predicted 3,389,926 ≠ F1's
  3,722,896, so he was present only if a remaining fingerprint carries his value. **Kubacabra
  himself joins the killer-candidate list** — measured on the board, 3-phase pressure through the
  death window. Zantarin's save-field identification survives only through the same door: a
  remaining fingerprint at 3,176,863. The galadriel board-closure read adjudicates all three at
  once.

**Both declarations ride in the baton provenance: the G-5 Death Revenant contradiction, and the G-2
boss-skill rank ceilings (all monster damage figures are UPPER BOUNDS).**

Zantarin appears in **15 of 200 waves** (coin-flip at 130) — a Phase-E narrative-shape input, not a
script.

### 10.9 Cycle floor — a spec parameter, not overhead

**The fixture's fastest observed wave intervals are 7.03 s (wave 47), 7.05 s (wave 8) and 7.07 s
(wave 81).** That ~7.0 s is **spawn + approach + kill for a wave that dies instantly at L100** — a
property of the fixture and of the arena's geometry, and therefore **a wave-engine spec parameter,
NOT measurement overhead to subtract** (L-13; galadriel § 4.3).

The sim's wave cycle must therefore decompose into at least:

```
cycle_time(wave) = spawn_resolution + approach_traversal + engagement_kill_time + advance_tick_latency
                   \_______________ >= ~7.0 s floor for a trivially-dying wave _____/
```

A sim that reproduces kill time but not the floor will beat the fixture on every early wave by
construction. **Structural companion:** the clear-time distribution is **bimodal** — waves at
multiples of 10 cost ~2× (**mean 28.57 s, n = 9** vs **14.29 s, n = 83**). Any model fitted against
a pooled mean is fitting a bimodal quantity (§ 12 pins the comparison classes accordingly).

### 10.10 Acceptance criteria

1. **AC-10.1** `first_wave_fought == start_wave_label + 1` for every label in `{0, 50, 100, 150, 180}`.
2. **AC-10.2** Instantiating wave *w* selects the `tier<NN>` content band with
   `NN = ceil(w/10)` and a `rewardTier` of `floor(w/10)` — and the two are allowed to differ.
3. **AC-10.3** Wave 160 puts exactly one nemesis on each of p01/p02/p03 across 1,000 rolls, with
   marginal frequencies matching the emitted pool weights within sampling error, and **zero trash**.
4. **AC-10.4** Expected wave totals over waves 151–170 reproduce **292.0 ± 5.5** regulars with p06
   off and **316.5** with p06 on, and **63.0** expected champions.
5. **AC-10.5** Monster life scaling while fighting wave *w* on Gladiator equals the CSV's
   `(w−1, gladiator)` row per the § 10.7 array-lookup law — in particular **322 while fighting wave
   160**: not 324 (lookup-law guard) and not 168 (F-2 regression guard).
6. **AC-10.6** p05 arrivals are staggered 3 s from t + 4 s; p01–p04 arrive at t = 0; p06 arrives
   only when the bonus toggle is on.
7. **AC-10.7** The minimum achievable cycle time for a trivially-dying wave in the modelled arena is
   ≥ the pinned floor (§ 12), i.e. the floor emerges from spawn + traversal geometry rather than
   being asserted as a constant.

---

## § 11 — Baton schema v1 — **MERGED (both consults folded)**

> **This section is MERGED, not DRAFT.** Both consults returned and are folded here:
> **star-lord** `star-lord/notes/2026-08-08-kc2-baton-schema-consult.md` (redlines **R-1…R-39**,
> every line-cite verified at engine HEAD `ebf13240`) and **drax**
> `drax/notes/2026-08-08-kc2-baton-coverage-sign.md` (**SIGNED — coverage sufficient as amended**,
> 23 MUST + 5 SHOULD). Conductor rulings **L-25 / L-26 / L-27** govern where the two met.
>
> Division of authority is unchanged: **star-lord owns the emitter and the JSON assembly**;
> **drax's signed list — not this section — is what AC-11.3 runs against**, and § 11.9 is the
> row-by-row reconciliation of that list against the schema below. Four items remain open or routed;
> they are named with their owners in **§ 11.6.4** and nowhere else.

### 11.1 What the baton is, and what it is not

**The baton is a SIBLING run-trace artifact.** It is versioned `baton/v1` and it **never occupies
the `encounters` bundle key** (L-1). That key is measured-reserved and grammar-frozen:
`one_realm_bundle_assembler.py:1531–1544` holds
`{"_reserved": True, "_grammar_frozen_by": "Tier-3-W1", "_acceptance_fixture": "RD-1-run-object"}`
with a must-be-dict validation guard at `:1270–1276`. Whether a future RD-1 run-object *references*
batons is **Tier-3's call, not this run's**.

**The baton is the engine's first JSON event-trace surface.** P-X1 established that event-level data
is telemetry-DB-resident (schema v2.17, `fight_events` via `record_fight_events()`), but batch JSON
outputs are **aggregates-only**. This is an extension, not a duplication. star-lord's Q5 duplication
sweep confirms it: nothing duplicates the baton whole.

**It is the SECOND engine→Godot JSON contract, not the first.** `export/arena_scenario_emitter.py`
(MIGRATION § v1.77, 2026-06-15) already emits `reincarnated-godot/data/arena_scenarios.json` to the
same consumer. The baton therefore **adopts that emitter's conventions rather than inventing parallel
ones** (§ 11.2) and states the kinship *inside the artifact* — `config.arena.arena_schema_kinship` —
so the relationship survives past this note (star-lord D1, resolution **(b)**, ruled).

**It closes a three-month-old standing flag.** MIGRATION § v1.15 (2026-05-18, *"OBSERVATION —
positional telemetry gap"*) recorded that `fights.jsonl` carries no spawn positions, no cast
positions and no player trajectories, and flagged it *"to knight-rider for future dispatch."* That
dispatch never came; `aoe_cast_events` still carries `true_radius`/`apparent_radius` and **no
position at all**. The baton is the first artifact that closes it, and § 11.8's MIGRATION entry says
so — a standing open observation becomes a closed one, and that lineage belongs in the log.

### 11.2 Conventions it extends (`export/` machinery, not a parallel format)

| Convention | Precedent (verified at HEAD `ebf13240`) | Baton form |
|---|---|---|
| format-version constant | `EXPORT_FORMAT_VERSION` (`schemas.py:149`, string `"1.0"`) + `ExportMetadata.format_version` (`:373`) | `baton_trace_format: "v1"` as the **human label** |
| **loader-comparable version int** | `arena_scenarios.json` `_schema_version` = int `1` — the idiom the Godot loader already reads | **`_schema_version: 1` (int), carried alongside** [R-1]. `"v1" >= "v1.10"` is a lexicographic trap; an int is not |
| **root provenance keys** | `arena_scenario_emitter`: `_generated_from`, `_schema_version`, `_emitted_at` (`%Y-%m-%dT%H:%M:%SZ`), `_do_not_hand_edit` (the regen command) | **all four, verbatim in form** [R-2] |
| **deterministic serialization** | `json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n"` (`arena_scenario_emitter`) | **adopted** [S7]. Two batons from one seed must diff to nothing |
| **atomic write** | `.json.tmp` → `os.replace`, reason stated in source: *"prevents partial reads by Godot/drax"* | **adopted** [S7] |
| Pydantic validation at the export boundary | Discipline #8; `season_exporter.py:972–974` | **adopted — and this is a stated DIVERGENCE**, see below |
| **run identity** | `run_registry.make_run_id()` (`:135`, UUID4); `emission_runs.run_id TEXT PRIMARY KEY` (`:70`) | **`baton_run_id`** — a *named distinct namespace*, plus optional `emission_run_id` cross-reference [R-5 / M2] |
| **config hash** | `run_registry.compute_config_hash()` (`:140`) and `one_realm_bundle_assembler._compute_config_hash()` — sha256 truncated to 16 hex | **`config_hash`, same idiom** [R-6 / M3] — lets a consumer tell two batons apart without diffing 10 MB |
| **embedded self-describing provenance** | `_build_stage2_run_record()` (`one_realm_bundle_assembler.py:794–834`) — pins + counts + status + **declared-null-with-a-reason** | the § 11.5 provenance block, including the declared-null pattern [M4] |
| **engine-version sourcing** | `telemetry/db.py:52 get_engine_version()` (7-char, `"unknown"` on any failure); `kit_space_emitter.py:104–135` adds `_full` 40-char | **extended** — `engine_version_sha` + `engine_version_full` + **`engine_tree_state`**, because neither existing helper reports a dirty tree [R-8] |
| event-record shape | `record_fight_events()` dict spine (`recorder.py:952–1025`): REQUIRED `event_type` + `fight_tick`; 11 optional columns, Pattern-P7 defensive-get → NULL | the baton's column set is the `fight_events` set **plus** baton-only additions; **every dropped column is dropped BY NAME** in the MIGRATION entry, never by silent omission [D2] |
| MIGRATION chain | `export/MIGRATION.md`, reverse-chronological, **current style** `## [YYYY-MM-DD] <title>` (HEAD's two newest entries at `:8` and `:56`) | one entry in the **current** style at the top of the file — § 11.8 |

**Three divergences, stated so the next reader does not find two Godot-facing emitters behaving two
ways with no note saying which is intentional:**

1. **Validation style.** `arena_scenario_emitter` validates with assert-based `_validate_payload()`
   over `frozenset` required-field sets — **not** Pydantic. The baton uses **Pydantic anyway**
   (stronger discipline, and it makes the `Provenance` sub-model independently testable against
   AC-11.4). The MIGRATION entry states the divergence and the reason.
2. **Write helper.** The two helpers in `export/` already disagree —
   `season_exporter._write_json` (`:1092–1093`) has no `sort_keys` and no atomic replace. The baton
   picks the **`arena_scenario_emitter` form explicitly**, because the baton is a *reproducibility*
   artifact.
3. **Validated model ≠ wire form.** The emitter validates a **rich nested family** — `BatonV1` →
   `SpecPin` / `SimPin` / `Config{Fixture, Encounter, Kit, Model, Arena}` / `Actor` / `Wave` /
   `Event` / `Tracks` / `RunSummary` / `Provenance` — then **flattens at the write boundary** into
   the columnar/row-array wire form of § 11.6.2. The round-trip test inflates rows back into objects
   and asserts model equality. Per-event Pydantic is affordable and the objection was **measured
   away, not assumed** (star-lord Q2(d), Discipline #10): pydantic 2.13.3, 10-field event model with
   nested position, `model_validate` **3.1 µs each** — the 198 k high case is ~0.6 s.

**Sim-side sourcing note for Phase C:** gamora's wave-engine work emits per-event records compatible
with the `record_fight_events()` dict shape; star-lord's emitter owns JSON assembly, precision
truncation, columnarisation and schema validation. **Nothing in § 11.6.2's wire form is gamora's
concern** — she emits objects.

### 11.3 Truth boundary (R-KC2-7 — hybrid)

| Owned by the SIM (causal combat truth — baton payload) | Owned by PRESENTATION (aesthetics within baton constraints) |
|---|---|
| who hit whom, for how much, at what time | monster approach choreography between spawn and engagement |
| **per-actor HP, carried event-locally on `hp_after`** (§ 11.3.1) | idle/walk/run animation blending, footfall, turn-in-place |
| player HP + energy, as continuous columnar tracks | camera framing, lighting, VFX selection |
| deaths (actor, time, killer — non-null on `player_death`) | crowd micro-spacing inside the declared scatter |
| wave clocks (start, end, outcome, termination reason) | body radius / proxy sizing (the hit test is centre-to-centre — § 11.4 `hit_test_model`) |
| **spawn positions** (the scatter roll is sim-rolled) and **engage times** | anything not fixed by an emitted field |
| **player path + circle sweep** | |

**The rule that makes the split safe:** presentation must never *re-derive* a sim-owned quantity. The
disc centre is the emitted player position; if presentation recomputed it, the picture could disagree
with the damage.

**Two things that are NOT re-derivation, stated so the rule stays usable:** (a) computing `t_s` from
`run_tick × tick_period_s` is *arithmetic on an emitted constant*, which is why the tracks carry no
per-sample time [R-31]; (b) **reading** `hp_after` off an emitted event row is reading a sim-owned
number, not recomputing one. **Integrating a damage-event sum to obtain HP is re-derivation and is
forbidden** — § 11.3.1.

#### 11.3.1 The per-actor-HP ruling — **RULED L-27** (closes drax M-23 × star-lord R-37)

The consults collided here, and the collision was real: **§ 11.3 as drafted promised the sim owned
"HP tracks (player + every actor)"; § 11.4 as drafted emitted one track, the player's.** drax named
it *"the single most load-bearing absence"* (his § B.10) and star-lord independently raised it as a
conductor question with a sizing note — a dense per-tick per-actor track is the largest single item
in the artifact (≈ 17.7 k ticks × ~18 concurrent bodies ≈ 318 k samples, roughly doubling the file).

**RULING (L-27): per-actor HP truth is `hp_after`, carried on EVERY damage, DoT and heal event.
There are NO dense per-actor HP tracks. Player-only continuous series remain columnar tracks.**

The three consequences, stated as obligations rather than as prose:

1. **Emitter obligation.** `hp_after` is a **mandatory, non-null** column on every row whose
   `event_type ∈ {damage_dealt, dot_tick, heal_tick}`, for the row's `target_id` — player or actor,
   no exceptions. It is the target's HP *after* the event resolved, in the same units as
   `actors[].hp_max` / `tracks.player_hp.hp`.
2. **Consumer obligation.** The Godot consumer **reads `hp_after` and never integrates event sums.**
   This is the ruling's whole point: drax's own WR3-ACC measurement is the proof that event sums are
   a **lower bound, one-signed** — summing `delivered` under-read `player_damage_taken` by up to
   **47.5 %** (max residual 288.96 HP) on 200 seeds, exact on only 17. A sanctioned re-derivation
   would have re-imported that failure mode into a schema built to prevent it.
3. **What it buys, in one field.** Monster HP bars with no re-derivation · exact bar motion at any
   track sample rate · the kill-blow frame for free (the row whose `hp_after` is 0) · and a
   **load-time reconciliation**: `Σ damage_applied` against successive `hp_after` values must close
   exactly, per actor, which converts drax's standing obligation #6 from a measurement into an
   assertion (AC-11.7e). It also retires drax's fallback ask M-23b (a separate kill-blow flag) —
   with `hp_after` present, the kill blow is a join between two emitted facts.

**Why this is the correct side of the truth boundary and not a dodge.** Actor HP *is* sim-owned
causal truth — the ruling does not demote it. What the ruling rejects is the claim that sim-owned
truth must be *densely sampled* to be owned. Actor HP is naturally **sparse**: it changes only when
an event changes it, and every such event is already in the stream. Event-locking the value is
therefore **exact where a sampled track would be interpolated**, and it costs one column instead of
doubling the artifact. § 11.3's row is amended accordingly — the promise is kept, the shape changed.

### 11.4 Field inventory — **FINAL (merged)**

Bracketed tags are provenance for each amendment: **R-n** = star-lord redline, **M-n** = drax
coverage-sign amendment, **L-n** = conductor ruling. The tree below is the **logical** inventory; the
**wire** form applies § 11.6.2's columnar/row-array/precision transforms to `events` and `tracks`
and to nothing else.

```
baton/v1
├── baton_trace_format: "v1"                 # human label
├── _schema_version: 1                       # int — the arena_scenarios.json loader idiom   [R-1]
├── _generated_from, _emitted_at, _do_not_hand_edit                                          [R-2]
├── _precision   { position_dp: 3, time_dp: 4, damage_dp: 2 }                                [R-3]
├── _integrity   { event_row_count, actor_count, wave_count,
│                  events_columns_len, track_sample_counts{} }                               [R-4]
├── baton_run_id, emission_run_id | null, config_hash                                   [R-5, R-6]
├── spec_pin     { spec_note, spec_sha256, charter_commit, ledger_commit, pin_state }        [R-7]
│                # pin_state ∈ {COMMITTED, UNCOMMITTED-WORKING-COPY}
├── sim_pin      { engine_version_sha, engine_version_full, engine_tree_state,
│                  sim_module_version, seed, rng_algorithm }                            [R-8, R-9]
│                # engine_tree_state ∈ {clean, dirty}; "unknown" sha is a HARD STOP
├── config
│   ├── fixture   { name: "EoRWarlGuts", build_of_record: "b28gD0KN",
│   │               eor_rank_total: 26, identity_grade: "MEASURED",
│   │               identity_envelope: "+3.9%/-0.5%" }
│   ├── encounter { difficulty: "gladiator", start_wave_label, first_wave_fought,
│   │               lives: 1,
│   │               fixture_p06_state: true,     # MEASURED ON (L-21) — provenance side  [M-1]
│   │               run_p06_enabled: <bool>,     # MANDATORY, NON-NULL — what the run did [M-1]
│   │               defenses: [], blessings: [], mutators: "OUT-OF-MODEL" }
│   ├── kit       { drain_unit: "PER_TICK", drain_rate_per_s: 176.4,            # PINNED  [L-22]
│   │               tick_period_s: 0.0816, attack_speed_pct: 196,
│   │               radius_m: 3.0, weapon_damage_pct: 64,
│   │               rotation_speed_multiplier: 0.35,                                     [M-2]
│   │               channel_tail_s: 0.25,                                                [M-4]
│   │               soulfire { period_s: 0.2, direction: "CCW",
│   │                          start: "front", explosion_radius_m: 0.2 },                [M-4]
│   │               hit_test_model: "point",                                             [M-5]
│   │               body_radius_role: "NON-CAUSAL" }                                     [M-5]
│   ├── model     { monster_attack_model: <see § 11.6.4 O-2>,                            [M-18]
│   │               mitigation_model, damage_semantic,                                   [M-20]
│   │               crit_model: "PTH-BAND" | "NOT_MODELLED",                             [M-24]
│   │               player_hp_increase_sources: [ … ] | [] }                             [M-17]
│   └── arena     { arena_id: "s1" | "s2",         # per-sitting set — NEVER pooled  [§ 10.6, L-21]
│                   arena_schema_kinship: "arena_scenarios.json v1",                     [R-13]
│                   width_m, height_m,                                                   [R-11]
│                   arena_bounds { shape: "rect" | "disc" | "UNBOUNDED", … },            [M-9]
│                   axis_convention { up_axis, handedness, units: "m", ground_elevation,
│                                     facing_units: "rad", facing_zero, facing_sign,
│                                     facing_range },        # MANDATORY, NON-NULL  [M-8 BLOCKING]
│                   collision_model: "OPEN-PLANE — no blocking geometry modelled",       [M-10]
│                   spawn_points[6] { point_id: "p01".."p06",                       [R-10, M-6]
│                                     x, y, heading_rad,
│                                     bearing_clock, bearing_grade },              [§ 10.6, L-21]
│                   player_spawn { x, y, heading_rad },
│                   placement_extents_m: 8.0,                                            [R-12]
│                   scatter_model: "SIM-ROLLED",                                         [M-7]
│                   positions_provenance: "DECLARED",
│                   bearings_provenance: "ESTIMATED-FOOTAGE ±15°" }                      [L-21]
├── actors[]      { actor_id,                       # unique RUN-WIDE, not per-wave      [M-13]
│                   record_path,                    # AC-6.4 — every statline resolvable
│                   display_name,
│                   threat_tier: trash|hero|boss|nemesis,                                [R-14]
│                   archetype_tag,                                                  [R-15, M-11]
│                   is_champion,                                                         [M-12]
│                   spawn_point_id, spawn_x, spawn_y, spawn_heading_rad,            [R-16, M-7]
│                   entity_radius_m | null,                                         [R-17, M-5]
│                   spawn_t_s, spawn_tick,                                               [R-18]
│                   engage_t_s | null, engage_tick | null, engage_null_reason | null,    [M-14]
│                   level, hp_max, hp_max_basis: "POST-SCALING",                         [M-13]
│                   life_modifier_pct, wave }
├── waves[]       { wave, content_tier, reward_tier,             # AC-10.2 allows these to differ
│                   t_start_s, t_end_s, tick_start, tick_end,                            [R-19]
│                   outcome, outcome_enum_version: 1,                                    [M-15]
│                   termination_reason, termination_enum_version: 1,                     [R-20]
│                   life_modifier_pct,                           # 324 at wave 160 — F-2 guard
│                   nemesis_wave,                                                        [M-16]
│                   spawn_points_active[],           # by point_id, never by array slot  [M-6]
│                   actor_ids[],
│                   event_row_range: [lo, hi), track_sample_range: [lo, hi) }            [R-21]
├── events                                                                          [R-22, S3]
│   ├── columns[]      # DECLARED HEADER — the rows are unreadable by inspection without it
│   └── rows[][]       # row-array; column order ≡ columns[]
├── tracks                                                                          [R-29, S2]
│   ├── _sample_stride { player_path: 1, circle_sweep: 1, player_hp: 1, player_energy: 1 }[R-30]
│   ├── _tick_base     { first_tick: 0, tick_period_s: 0.0816 }                          [R-31]
│   ├── player_path    { tick[], x[], y[], heading_rad[] }                          [R-32, M-27]
│   ├── circle_sweep   { tick[], centre_x[], centre_y[], radius_m[], channel_active[] }
│   │                                                                    [R-33, R-34 (L-25)]
│   ├── player_hp      { tick[], hp[], hp_max[] }                                        [R-35]
│   └── player_energy  { tick[], energy[], energy_max[], energy_reserved[] }        [R-36, M-13]
├── run_summary   { waves_cleared, actors_killed, run_duration_s,
│                   final_wave, end_reason }         # emitted so joins can be ASSERTED  [M-28]
└── provenance    (§ 11.5)
```

**`events.columns` — the declared header, in order:**

```
[ event_type, run_tick, fight_tick, t_s, wave,
  source_id, target_id, source_skill_id,
  damage_raw, damage_applied, damage_source_tag,
  hp_after,
  geometry_type, geometry_family,
  source_x, source_y, target_x, target_y,
  is_crit, dot_expires_tick,
  mitigation_source, resource_cost, resource_gained, mobs_in_range ]

event_type ∈ { spawn, engage, damage_dealt, dot_tick, heal_tick, death,
               channel_start, channel_release, channel_expiry,
               energy_dryout, wave_start, wave_end, player_death }
```

**Twelve pins that make the inventory decidable. Each is a merge decision, not a restatement.**

1. **`damage_dealt`, never `tick_damage` [R-25, ruled].** `record_fight_events()` branches on
   `event_type == "damage_dealt"` for its Pattern-P7 geometry guard (`recorder.py:986–991`). A stream
   labelled `tick_damage` ingests with that guard **silently inert** — the exact silent-field-drop
   failure this seam exists to catch. drax's B.8 listed `tick_damage` as SUFFICIENT under M-26; the
   member is **renamed**, the M-26 obligation is unchanged and is pinned at (2).
2. **`damage_dealt` rows are per-(tick, target), NEVER aggregated [M-26].** One row per
   `(run_tick, target_id, source_skill_id)`. This is a **schema obligation with an acceptance test**
   (AC-11.7b), not a convention: drax's entire crowd choreography rests on the per-tick in/out-of-disc
   membership predicate, and aggregation destroys it.
3. **`run_tick` is the identity key; `fight_tick` is retained, nullable, for join compatibility
   [M-13, amending R-23].** star-lord's R-23 made `fight_tick` the identity because it joins to
   `fight_events`. drax's M-13 found the hazard: **that spine is per-FIGHT and this artifact is one
   continuous 93-wave run** — a per-wave reset would let the `events ↔ circle_sweep` join silently
   cross waves. Resolution: **`run_tick` (int, monotonic run-wide from 0, never reset) is the
   identity**, carried by every event row and every track; `fight_tick` rides alongside, nullable,
   carrying whatever the recorder's per-fight counter says, so the `fight_events` join survives.
   AC-11.7a tests the monotonicity as an absence-of-reset.
4. **`t_s` is derived and is NEVER a key.** `t_s = run_tick × tick_period_s`, rounded per
   `_precision`, origin **t = 0 at the first tick of `first_wave_fought`**, monotonic run-wide
   [M-13]. Float equality across a JSON round-trip is how a trace begins disagreeing with itself; all
   cross-block references use `run_tick`.
5. **Positions are flat scalars, and every damage row says WHOSE [R-27, M-21].** There is no `{x, y}`
   object anywhere in this project's serialized surface — engine entities carry flat `.x`/`.y`
   (`spatial_engine.py:1855`), and `arena_scenarios.json` serializes every spawn flat. `position`
   splits into **`source_x/source_y` (nullable) + `target_x/target_y`**; for a damage row
   `target_x/target_y` is the target's position at that tick — **the number the sim already computed
   for the § 2.1 hit test**, so it is emitted rather than re-solved. drax called this
   *"the highest-value line in this document."*
6. **`geometry_family` rides alongside `geometry_type` [R-26].** L-16 is Phase-C BINDING: the spin
   declares its OWN family and must not reuse the nova's (disc↔corridor conflation = **3.076×**
   lethal-area error, 147.06 vs 452.39 m²). `TelegraphSpec.family` + `VALID_FAMILIES` already exist
   (`spatial_telemetry.py:505–511`), and matching on `shape` alone is the documented silent-blinding
   failure (`wr2_cell_bat_2026_07_29.py:262`). Both columns, or the consumer inherits the bug.
7. **The channel machine gets its third state [M-3].** `channel_end` cannot express
   `{IDLE, CHANNELLING, TAIL}`, and **AC-1.3 puts ticks up to 0.25 s after release** — a spin that
   stops on `channel_end` is a picture disagreeing with the damage. The member splits into
   **`channel_release`** (button up → TAIL) and **`channel_expiry`** (TAIL → IDLE), with
   `config.kit.channel_tail_s = 0.25` carried so the consumer reads the constant instead of holding
   it as a literal.
8. **`damage_raw` AND `damage_applied`, always — not "if they differ" [M-20].** HALT-6 is CLOSED
   (two-branch armour equation, `armorDefensiveAbsorption = 70.0`, 7-region per-hit sampling,
   `playerDefenseCap = [80,80,80]`) and HALT-4 is PARTIAL with ORDER-1 declared, so the sim has a
   mitigation model to apply and the two numbers can genuinely differ. Emitting both unconditionally
   removes the "which one is this?" ambiguity that WR3-ACC's **47.5 % under-read** looks like from the
   outside. `config.model.damage_semantic` states the pair's meaning in the artifact;
   `hp_after` is authoritative over both (§ 11.3.1).
9. **`hit_test_model: "point"` — a spec fact, not a new decision [M-5].** § 2.1's predicate is
   `|e.position − c| ≤ 3.0`, centre-to-centre, and AC-1.5 tests it at 3.01 / 2.99 m. Body radius is
   therefore **NON-CAUSAL**: `actors[].entity_radius_m` is emitted when the sim's spatial substrate
   holds one (so both sides use one number rather than two) and is `null` otherwise, with
   `config.kit.body_radius_role: "NON-CAUSAL"` licensing presentation to size proxies and say so.
10. **The scatter roll is SIM-ROLLED [M-7].** AC-10.7 requires the ~7.0 s cycle floor to *emerge* from
    spawn-and-traversal geometry rather than be asserted — which is only possible if the sim holds an
    actual spawn position inside `placement_extents_m = 8.0`. That position is causal, so it is
    emitted per actor (`spawn_x/spawn_y`) rather than invented downstream. Crowd micro-spacing
    *inside* the declared scatter remains presentation's.
11. **`arena_id` is mandatory and the sets are never pooled [§ 10.6, L-21].** galadriel's
    spawn-direction extraction shows the two sittings ran **different arenas** (s1 arrivals bear
    ≈ 3.0 / 5.2 / 6.9 / 9.6 o'clock; s2 wave-160 reads 1.8 / 10.5 / 4.5 / 7.5). Position parameters
    are **per-sitting sets**; a calibration band loads its own sitting's set; the baton pins the
    arena it ran (`arena_id` + six bearings + player spawn). **Pooling bearings across sittings is a
    spec violation, not a modelling choice** — and `bearing_grade` carries ESTIMATED-FOOTAGE ± 15°
    onto the frame so nobody reads a declared bearing as a measured one.
12. **`config.encounter.bonus_spawn_p06` splits [M-1], and the fixture side is now MEASURED.**
    `fixture_p06_state: true` records the L-21 census result (max-simultaneous **5** hostiles at
    t = 850.87 — the 5th body *is* the p06 hero slot; the 4-body branch excluded on two independent
    instruments). `run_p06_enabled` is mandatory and non-null — the run is not unknown to itself, and
    at the § 10.8 showcase p06 is the difference between 5 raw bodies and 4.

**Sample rate — ANSWERED by drax, no longer a consult question [M-27].** `player_path` and
`circle_sweep` both run the **12.25 Hz tick grid, stride 1, across the whole run including IDLE
stretches.** The reasoning is not smoothness — drax's sagitta arithmetic (`e ≈ v·ω·h²/8`) shows 10 Hz
costs only 1.57 cm — it is **grid commensurability**: § 2.2 rules the disc centre *is* the emitted
player position, so if the path runs a wall clock and the sweep runs the tick grid, **AC-2.2 becomes
unverifiable inside the baton** because there is no pair of records to compare. On one grid it is a
load-time check (AC-11.7c). Cost of the simple form is ≈ 2.0 MB over a 40-minute run against a ~10 MB
document. `tracks._sample_stride` [R-30] is the hook that lets a later rate decision land **with no
schema entry and no MIGRATION break**; v1 ships stride 1 throughout.

**Bit-identity survives truncation — the one interaction between two adopted redlines.** M-27 requires
`player_path[i].(x, y)` be **bit-identical** to `circle_sweep[i].(centre_x, centre_y)` at every tick;
S1 truncates positions to 3 dp at the write boundary. These compose **only if the truncation is
applied identically to both channels from the same source value**, which is therefore an emitter
obligation, tested at AC-11.7c. Truncate once, write twice.

### 11.5 Provenance block (mandatory, complete, per charter § 3 Phase E)

Every prose string that carried a machine-relevant value has been **typed** [R-38], and every free-form
declaration has been given a **stable ID** [R-39], because AC-11.4b is a set comparison against an ID
register and an eyeball check against prose is not a test.

```
provenance:
  calibration_grade: FULL | PARTIAL      # per G-D outcome; PARTIAL is the honorable fallback
                                         # GUARD [R-8]: engine_tree_state == "dirty" => MAY NOT be
                                         # FULL. A clean SHA stamped on an edited tree is a false
                                         # provenance claim, and provenance is this artifact's job.
  binding_rows:      [...]               # which measurements bound, with deltas
  informative_rows:  [...]               # s2 field outcomes; one-sided inequality direction
  devotion_envelope_disclosure:  <the § 9.5 block, VERBATIM — AC-9.2 requires it verbatim and
                                  complete; do NOT restructure it. The Shifting Sands DUAL-BOUND
                                  (~200x, P-E5 G-6) lives inside it and remains OPEN.>
  u8_closure_state:            CLOSED    # ladder = 200 waves; first_wave_fought = label + 1
  u9_closure_state:            CLOSED
  u9_intra_order_residual_pct: 1.9       # intra-order + rounding + clamp, waves 151-170
  u9_bonus_spawn_state:        RESOLVED  # p06 measured ON (L-21 census)  -- was <resolved|UNKNOWN>
  u9_bonus_spawn_branch_pct:   RETIRED   # the +-8.4% branch is DEAD, not carried as a tolerance
  drain_unit:                  PER_TICK  # PINNED L-22; enum frozen, hook retained -- was drain_fork
  drain_rate_per_s:            176.4     # @ 196% AS, client-verbatim = 16.0 x 12.25 x 0.90
  soulfire_cost_term:          DECLARED-SEPARATE   # never folded into drain_rate_per_s (§ 3.1)
  halt_register:                         # L-26 bundle outcome, carried so the artifact is auditable
    closed:          [HALT-1, HALT-3, HALT-5, HALT-6, HALT-8, HALT-9]
    partial:         [HALT-4, HALT-10]   # HALT-4: ORDER-1 FAVOURED, not proven · HALT-10: nemesis
                                         #   class CLOSED +-0.05% (L-29, § 6.2b); p04 = named gap
    closed_by_type:  [HALT-2]            # v_ref is a DECLARED free parameter (bundle § 6.1)
    unfired:         [HALT-7]            # pre-registered G-D contingency
    open:            []
  open_halt_effect:  []                  # was HALT-10 -- closed L-29; residue rides declarations/T8-P04
  arena_pin:
    arena_id:        <s1 | s2>
    bearings_grade:  ESTIMATED-FOOTAGE +-15 deg (L-21)
    pooling_rule:    per-sitting sets, NEVER pooled -- pooling is a spec violation (§ 10.6)
  out_of_model:                          # {id, text} -- set-comparable, no free-form phrases [R-39]
    - { id: OOM-DEVOTION-PROCS,  text: "no proc mechanism modelled this lap (R-KC2-1(d))" }
    - { id: OOM-MUTATORS,        text: "6 active (2 player + 4 monster), identities unextracted,
                                        25-pool prior, reroll every 10 waves" }
    - { id: OOM-DEFENSES,        text: "defense structures excluded by charter (§ 10 ARCHITECT gate)" }
    - { id: OOM-BLESSINGS,       text: "fixture bought ZERO, both sittings -- measured, not omitted" }
    - { id: OOM-RETALIATION,     text: "player retaliation excluded (§ 8)" }
    - { id: OOM-ASCENSION,       text: "activated 10 s, no activation ledger in the read set (§ 5.3)" }
    - { id: OOM-TRIGGERED-BUFFS, text: "Menhir's Will / Fighting Spirit / Resilience (§ 5.3)" }
    - { id: OOM-M2-REWIND,       text: "wave-20, round down to 10; cost 5/15/30, cap 3 (§ 10.3)" }
    - { id: OOM-REWARDS,         text: "tributes / score / rewards / bonus timer (§ 10.3)" }
  declarations:                          # {id, text} -- AC-11.4b set-compares against this register
    - { id: G-5,  text: "wave-160 save fields (last-monster-hit 'Death Revenant' vs
                         last-monster-hitBy 'Zantarin') cannot both date from wave 160. Wave 160 is
                         rolled honestly from the pools, NOT a scripted Zantarin reenactment." }
    - { id: G-2,  text: "ALL monster damage figures are UPPER BOUNDS. Boss-skill rank binding unread." }
    - { id: T8-P04, text: "p04 superboss eHP carries a -4.3% named gap (Galakros favoured; charLevel
                         ceiling 110 vs required ~113.3): declared +-5% band, INFORMATIVE-side only.
                         Nemesis-class eHP chain is CLOSED +-0.05% (L-29, § 6.2b, § 10.7 lookup law)." }
    - { id: G-4,  text: "p05 concurrency model is the safe reading (pool count staggered 3 s from
                         t+4 s); the t+4.0 s start anchor is MEASURED x3 (L-21)." }
    - { id: G-7,  text: "4 dangling roster refs of ~7,000 dropped, weights renormalised." }
    - { id: D-ARENA-DECLARED,    text: "arena emitter positions are DECLARED free parameters,
                                        footage-estimable, never DB-hunted (L-10d)." }
    - { id: D-ARENA-PER-SITTING, text: "the two sittings ran DIFFERENT arenas; parameter sets are
                                        per-sitting and are never pooled (L-21)." }
    - { id: D-IDENTITY-ENVELOPE, text: "fixture identity is name-identical, derived within
                                        +3.9%/-0.5%. 'matches 100%' is RETIRED." }
    - { id: D-MUTATORS-LIVE,     text: "mutators were live in BOTH sittings and are NOT folded
                                        into noise -- a live, unquantified per-decade confound." }
    - { id: D-S2-INTAKE,         text: "s2 intake side is confounded (Deathchill -OA,
                                        Inferno -damage-dealt); defenses positional => per-wave." }
    - { id: D-S2-OUTPUT,         text: "s2 output side is confounded (Stormcaller -resist,
                                        Vanguard +offense); defenses were ACTIVE at the wave-160
                                        death, so the confound runs the whole run (L-15b)." }
    - { id: D-HP-AFTER,          text: "per-actor HP is carried event-locally on hp_after (L-27).
                                        Consumers READ it; integrating a damage-event sum to obtain
                                        HP is re-derivation and is forbidden (§ 11.3.1)." }
  seed_pins: { batch_seed, run_seed, selection_criteria_version, rng_algorithm }   # [R-9]
```

**Write-boundary assert [R-38]:** `u9_bonus_spawn_state` must agree with
`config.encounter.fixture_p06_state`. One fact in two encodings is how the two drift apart; the
emitter checks it rather than trusting it (AC-11.4g).

### 11.6 Size, write discipline, and the open items

#### 11.6.1 Size — measured, then recomposed against the merged column set

star-lord measured rather than estimated (Discipline #10), taking run geometry from this spec's own
§ 10.9 clear-time distribution: 9 waves at 28.57 s + 83 at 14.29 s = **1,443.2 s ≈ 24.1 min**, which
at `tick_period_s = 0.0816` is **17,686 ticks**.

| scenario | events | § 11.4 as originally drafted | compact + 3 dp | **columnar + row-array + 3 dp** |
|---|---:|---:|---:|---:|
| LOW — 50 % uptime, 4 in disc | 35 k | 17.4 MB | 11.2 MB | **~4.0 MB** |
| **MID — 65 %, 7 in disc** | **80 k** | **31.6 MB** | 21.3 MB | **~8.4 MB** |
| HIGH — 80 %, 14 in disc | 198 k | 68.8 MB | 47.6 MB | **~20 MB** |

**Why 31.6 MB was a problem when a 45 MB artifact elsewhere in `output/` is not.** The largest thing
in `src/reincarnated/output/` is `w3_batch1_bundle.json` at 45.3 MB, but nothing consumes it in a game
loop. The largest artifact **Godot** parses is `one_realm_demo_bundle.json` at **3.29 MB**, and
`reincarnated-godot/scripts/bundle_loader.gd:98` does `JSON.parse_string(txt)` — whole file into a
String, then the whole tree into Variants. The hazard was never the disk figure; it was 80 k
ten-key Dictionaries materialised at once.

**Recomposed for the merged schema (DERIVED, not measured):** the merged `events.columns` carries
**24 columns** against the 17 star-lord measured. The additions are null on most rows (≈ 2 B each
under a row-array), so MID lands at roughly **9–12 MB**, plus ~0.6 MB of columnar tracks and ~0.4 MB
of actors. That is **inside drax's declared ≈ 22 MB budget** and far inside his stated
ask-for-a-split threshold of ~100 MB — he signed *"no sidecar or NDJSON split is needed at v1,"* and
this merge does not move him past it. **Three transforms do all the work and none of them sets a
sample rate:** precision truncation [S1, 1.4×], columnar tracks [S2, measured 1.89 → 0.51 MB, 3.7×],
row-array events [S3, measured 18.06 → 7.84 MB, 2.3×].

#### 11.6.2 Wire form + write discipline

- **Precision truncation, declared in the artifact [S1].** Positions and radii → **3 dp** (mm —
  500× finer than the 0.5 m entity radius); `t_s` → **4 dp** (0.1 ms against an 81.6 ms tick);
  damage → **2 dp**. `_precision` is emitted at root so a consumer never has to guess whether a
  difference is signal or rounding. *This is a new convention, not an inherited one* —
  `arena_scenarios.json` emits full float repr today (`1443.2160000000001` is 18 characters).
- **Columnar tracks [S2].** Struct-of-arrays. **Boundary invariant: every channel array within one
  track has equal length** (AC-11.7d).
- **Row-array events [S3].** `{columns[], rows[][]}`. The `columns` header is load-bearing — without
  it the artifact is unreadable by inspection, and star-lord would not have proposed the shape.
- **Sharding HOOK, not sharding [S5].** v1 is **not** sharded. `waves[].event_row_range` and
  `track_sample_range` make a per-wave split a v1.1 **additive** change that breaks nothing, and let
  a consumer slice wave 160 (the § 10.8 showcase) without loading the whole document. Cost: two
  fields × 93 waves.
- **Down-sample HOOK, not a rate [S6].** `tracks._sample_stride` ships `1` throughout. A later rate
  decision then needs no schema entry and no MIGRATION break.
- **Write discipline [S7]:** `.json.tmp` → `os.replace`; `sort_keys=True`. Sorting costs nothing
  under a columnar layout (arrays keep their order; only key order sorts) and makes two batons from
  one seed diff to nothing.
- **Hard stop:** `engine_version_sha == "unknown"` — the existing helper's swallow-everything
  tolerance is right for telemetry rows and wrong here — **no baton is written** (AC-11.4f).

#### 11.6.3 What is already testable with machinery that exists today

- **AC-11.5** is testable as an **absence**: `validate_bundle()`
  (`one_realm_bundle_assembler.py:1270–1276`) already requires `encounters` be a dict, and the
  reserved marker at `:1531–1544` is what belongs there. A test asserting the marker is byte-unchanged
  after a baton emit is a two-line pin. The L-1 namespace guard is **live in code**.
- **AC-11.1** follows the existing `save_sim_cycling_quality_report` / `load_…` round-trip pattern
  (`season_exporter.py:970–994`): write via `model_dump()`, reload via `model_validate()`, assert
  model equality.

#### 11.6.4 Open + routed items — **four, and only four**

| # | Item | Owner | State |
|---|---|---|---|
| **O-1** | **gzip [S4]** — measured **~10×** (7.84 → 1.67 MB). Godot reads standard gzip via `PackedByteArray.decompress_dynamic(…, FileAccess.COMPRESSION_GZIP)`, but that is a change **inside drax's loader**, and there is no gzip / NDJSON / streaming-write machinery anywhere in `export/` or `telemetry/` at HEAD — adopting it is a **new capability**. | **drax** | **OPEN-ROUTED — deliberately NOT resolved here.** drax's sign budgets ≈ 22 MB uncompressed and asks for no split, which is adjacent evidence but is **not** an answer to the yes/no. If the answer is no, § 11.6.1's ~9–12 MB stands, which is a step and not a leap. |
| **O-2** | **`config.model.monster_attack_model` VALUE** — `"abstract-schedule"` (presentation owns monster wind-ups, origins and shapes, labelled presentation-owned on frame) vs `"geometric"` (sim emits `{origin, shape, radius, wind_up_s}` per attack and drax draws the real thing). | **conductor** | **RULED — L-28: `"abstract-schedule"` for baton v1.** Not a preference — forced by the spec's own substrate posture: §§ 1–10 specify NO monster telegraph model (§ 6 COMPOSEs monster damage as declared ceilings on an abstract schedule; HALT-7 unfired; G-2 figures are upper bounds), so `"geometric"` would require the sim to **invent** per-attack `{origin, shape, radius, wind_up_s}` — § 4.2 free-parameter territory. The sim still owns WHEN monster damage lands and HOW MUCH (the `hp_after` stream); presentation choreographs the visible attack within those facts, **labelled presentation-owned on frame** — drax's meteor hazard is answered by the label discipline, not by silence. Evolution path: if G-D implicates monster damage and HALT-7 fires, a v2 schema may add `"geometric"` — version note, not v1. |
| **O-3** | **ADR-006 / `emission_registry.db`** — does the emitter register the baton run? | conductor, **veto-open** | **ANSWERED BY DEFAULT: NO external DB write this lap.** `baton_run_id` is a **named distinct namespace** with an optional `emission_run_id` cross-reference, so `run_registry`'s `run_id` primary key is never shadowed [M2]. This is the non-escalating default; **reversing it makes the emitter an external-DB writer and requires Matt authorization per statement (ADR-006).** § 11.8's MIGRATION entry states the answer explicitly rather than omitting it. |
| **O-4** | **`config.arena.axis_convention` VALUES** — the eight keys are pinned mandatory-non-null [M-8, drax's blocking item]; the values are a **read of the sim's own coordinate frame**, not a schema choice. `units: "m"` and `facing_units: "rad"` are pinned by the established `_m` / `heading_rad` conventions. | star-lord + gamora, **at build** | **BUILD-TIME OBLIGATION, not an open design question.** Recorded here because the failure mode is silent: wrong handedness **mirrors the arena**, so the body taking damage stands opposite a disc drawn perfectly — the same family as the WR2 projection lie, where a correct 2.000000 m separation *looked* like interpenetration at 41°. A frame will not tell anyone which side is wrong. |

### 11.7 Acceptance criteria — individually addressable

| ID | Criterion |
|---|---|
| **AC-11.1** | Every emitted baton validates against the Pydantic model at the export boundary; an invalid baton is **never written**. |
| **AC-11.2** | **Consumer-stub round-trip green** — a stub reconstructs, from the baton alone: every actor's spawn time **and position**, every wave's start/end, the player's path, the disc sweep, and every damage event's (source, target, amount, time). *This is the G-E bar; emission is not the bar.* |
| **AC-11.3** | Coverage 100 % against **the drax-SIGNED list** (`drax/notes/2026-08-08-kc2-baton-coverage-sign.md`), not against this document. § 11.9 is the reconciliation and is itself auditable row by row. |
| **AC-11.4a** | Provenance is complete — **no field elided**. |
| **AC-11.4b** | Every `declarations[]` entry is `{id, text}`; the ID set **equals** § 11.5's register (a set comparison, not an eyeball check). |
| **AC-11.4c** | Every `out_of_model[]` entry is `{id, text}`; the ID set equals the register; no entry duplicates a `config.encounter` field. |
| **AC-11.4d** | A baton with a **truthful `PARTIAL`** grade passes; a baton with a missing declaration does **not**. |
| **AC-11.4e** | `engine_tree_state == "dirty"` ⇒ `calibration_grade != FULL`, enforced at the write boundary [R-8]. |
| **AC-11.4f** | `engine_version_sha == "unknown"` ⇒ **hard stop**; no baton is written. |
| **AC-11.4g** | `provenance.u9_bonus_spawn_state` agrees with `config.encounter.fixture_p06_state` — asserted at the write boundary [R-38]. |
| **AC-11.4h** | `devotion_envelope_disclosure` is the § 9.5 block **verbatim and complete** (AC-9.2), un-restructured. |
| **AC-11.5** | The baton **never** appears under the `encounters` bundle key (L-1, testable as an absence; the reserved marker is byte-unchanged after emit). |
| **AC-11.6** | `_integrity` counts equal the emitted structures, and the stub consumer **asserts every one of them** — so AC-11.2 is a reconstruction exercise *with a checksum*. |
| **AC-11.7a** | `run_tick` is strictly monotonic run-wide and **never resets** at a wave boundary [M-13]. |
| **AC-11.7b** | Every `damage_dealt` row is unique on `(run_tick, target_id, source_skill_id)` — **no aggregation**, per tick or per wave [M-26]. |
| **AC-11.7c** | `tracks.player_path` carries a sample at **every** tick from `tick_start` of the first wave to `tick_end` of the last; and for every tick, `(x, y)` is **bit-identical** to `(centre_x, centre_y)` after truncation [M-27]. *This is AC-2.2 made checkable at load.* |
| **AC-11.7d** | Every channel array within one track has **equal length** [S2 invariant]. |
| **AC-11.7e** | `hp_after` is present and **non-null** on every `damage_dealt` / `dot_tick` / `heal_tick` row; and per actor, `Σ damage_applied` reconciles **exactly** against successive `hp_after` values [L-27]. |
| **AC-11.7f** | Every `player_death` row carries a **non-null `source_id`** [M-19] — the death card names the killer, and G-5 rides with it. |
| **AC-11.7g** | `len(events.columns)` equals the length of **every** row in `events.rows` [S3 invariant]. |
| **AC-11.8** | The MIGRATION entry exists, in the **current** `## [YYYY-MM-DD]` style, at the **top** of `export/MIGRATION.md`, carrying the explicit ADR-006 answer and the by-name list of dropped `fight_events` columns. |

### 11.8 MIGRATION entry — shape, and the two things it must state

`export/MIGRATION.md` is 8,733 lines and **reverse-chronological, newest at the top.** § 11.2's
original citation (v1.6 / v1.7 / v1.10 / v1.12) is correct **as entries** but is the **2026-05-27
generation** of entry *shape*; HEAD's two newest entries (`## [2026-07-29] HQ-2 …` at `:8`,
`## [2026-07-22] W3 …` at `:56`) use the current form. **Write the baton entry in the current shape,
at the top** [Q4]:

```
## [2026-08-XX] baton/v1 — first JSON event-trace emitter (KC2-SIM Phase C)

**Author:** star-lord
**Run:** KC2-SIM 2026-08-08 (conductor: gandalf), Phase C
**Source:** spec `gandalf/notes/2026-08-08-kc2-sim-battle-spec.md` § 11 (MERGED — star-lord
  consult R-1..R-39 + drax coverage sign, folded under L-25/L-26/L-27)
  · charter R-KC2-7 (truth boundary) · ledger § A.1 (P-X1 recon; L-1 namespace guard) · G-B fold <sha>
**Consumer impact:** NEW artifact for drax (`reincarnated-godot/`). No change to
  `one_realm_demo_bundle.json`, `arena_scenarios.json`, or any existing key.
  `encounters` UNTOUCHED and still reserved (L-1 / AC-11.5).
**Discipline compliance:** #1 (companion math note) · #2 (smoke test) · #8 (Pydantic + `_integrity`
  at the write boundary) · #10 (size figures MEASURED, not assumed)
**ADR compliance:** ADR-004 (cross-seam schema change => MIGRATION.md).
  **ADR-006 — ANSWERED, not omitted: the emitter writes NO row to `emission_registry.db`.**
  `baton_run_id` is a distinct namespace; `emission_run_id` is an optional cross-reference.
  Registering the run would be an external-DB write requiring Matt authorization per statement.
**Composes with:** § v1.77 (`arena_scenario_emitter`, the sibling Godot-facing emitter) ·
  § v1.86 (run registry) · `[2026-07-22]` (the `encounters` reservation this must not occupy)
**Closes:** § v1.15 (2026-05-18) "OBSERVATION — positional telemetry gap", open since 2026-05-18.
```

Three lines the newer style dropped are **restored**, because this change earns all three where the
last two did not: `Discipline compliance`, `ADR compliance`, `Composes with`.

**Two things this entry must state that no prior entry had to:**

1. **The drax-SIGNED coverage list, by path** — AC-11.3 makes drax's signature, not the spec, the
   acceptance bar. Precedent exists: the `[2026-07-22]` entry cites
   `export/drax-SIGNED-encounters-delta-2026-07-22.md` the same way.
2. **The by-name drop list**, per D2 — never silent omission. The baton **keeps** `geometry_type`,
   `damage_source_tag`, `damage_dealt` (as `damage_raw` + `damage_applied`), `mobs_in_range`,
   `mitigation_source`, `resource_cost`, `resource_gained`. It **drops, by name:** `damage_taken`
   (superseded — direction is carried by `source_id`/`target_id`, magnitude by `damage_applied`,
   effect by `hp_after`), `skill_type` (superseded by `source_skill_id` + `geometry_family`),
   `recovery_source` (superseded by the `heal_tick` member + `source_skill_id`), and
   `schema_version` (promoted to root `_schema_version`).

**Companion math note** per Discipline #1 and the `[2026-07-22]` precedent:
`export/math/2026-08-XX-baton-v1-schema.md`, carrying the § 11.6.1 size measurements so the MIGRATION
entry **cites** rather than restates them.

### 11.9 Coverage reconciliation — drax's 28 items against the merged schema

Per AC-11.3 the signed list is the bar. **Every item resolves to a named schema element. There are
zero gap rows, and all five SHOULDs are adopted** — each is a constant the spec already holds, a
declaration of a choice already made, or one nullable column under a row-array layout.

| ID | Ask | Merged schema element | Disposition |
|---|---|---|---|
| M-1 | split `bonus_spawn_p06` | `config.encounter.fixture_p06_state` **+** `run_p06_enabled` | **ADOPTED** — fixture side now `true`, MEASURED (L-21) |
| M-2 | rotation-speed constant | `config.kit.rotation_speed_multiplier: 0.35` | ADOPTED |
| M-3 | release ≠ tail expiry | `event_type` members `channel_release` / `channel_expiry` | ADOPTED — `channel_end` retired |
| M-4 | tail + Soulfire constants | `config.kit.channel_tail_s` · `config.kit.soulfire{}` | ADOPTED |
| M-5 | hit-test model + radii | `config.kit.hit_test_model: "point"` · `body_radius_role: "NON-CAUSAL"` · `actors[].entity_radius_m \| null` | ADOPTED — the answer is a § 2.1 spec fact |
| M-6 | emitter label space | `config.arena.spawn_points[].point_id: "p01".."p06"` | ADOPTED — `spawn_points_active[]` uses labels, never slots |
| M-7 | scatter-roll owner | `config.arena.scatter_model: "SIM-ROLLED"` + `actors[].spawn_x/spawn_y` | ADOPTED — AC-10.7 requires the sim to hold it |
| M-8 | axis convention **(blocking)** | `config.arena.axis_convention{8 keys}`, mandatory non-null | ADOPTED — values are a build-time read (§ 11.6.4 O-4) |
| M-9 | arena bounds | `config.arena.arena_bounds{}` incl. `UNBOUNDED` | ADOPTED |
| M-10 | collision model | `config.arena.collision_model` | ADOPTED — § 10.6's not-modelled list is the evidence |
| **M-11** *(SHOULD)* | family / archetype | `actors[].archetype_tag` | **ADOPTED** — converges with R-15; retires the substring-sniff fallback |
| **M-12** *(SHOULD)* | champion flag | `actors[].is_champion` | **ADOPTED** — § 10.5(4): champions ADD, never convert |
| M-13 | clock + identity pins | `run_tick` · `t_s` origin · `actor_id` run-wide · `hp_max_basis: "POST-SCALING"` · `energy_reserved` **absolute** (982 of 2576, MO-2) | ADOPTED — see § 11.4 pin 3 |
| M-14 | engage timestamp | `actors[].engage_t_s` / `engage_tick` / `engage_null_reason` | ADOPTED — causal under AC-10.7 |
| M-15 | outcome enum | `waves[].outcome` + `outcome_enum_version: 1`; death wave's `t_end_s` = death time | ADOPTED — merged with R-20's `termination_reason` |
| **M-16** *(SHOULD)* | nemesis wave | `waves[].nemesis_wave` | **ADOPTED** — P-E6 already emits the column |
| M-17 | heal author | `event_type: heal_tick` **+** `config.model.player_hp_increase_sources[]` | ADOPTED — an empty list is the declaration, and drax asserts against it |
| M-18 | monster attack model | `config.model.monster_attack_model` | **FIELD ADOPTED · ⚠ VALUE = CONDUCTOR-DECISION (§ 11.6.4 O-2)** |
| M-19 | killer named | `player_death.source_id` non-null (AC-11.7f) | ADOPTED |
| M-20 | damage semantic | `damage_raw` + `damage_applied` columns + `config.model.damage_semantic` | ADOPTED — **both, always** |
| M-21 | whose position | `source_x/source_y` + `target_x/target_y` columns | ADOPTED |
| M-22 | skill discriminator | `source_skill_id` column | ADOPTED — retires the `damage_type` accident |
| **M-23** | per-actor HP | **`hp_after` column** on damage/DoT/heal | **ADOPTED AS RULED (L-27) — § 11.3.1** |
| M-24 | crit | `is_crit` column + `config.model.crit_model` | ADOPTED — HALT-3 closed; band semantics proven by gamora's test |
| **M-25** *(SHOULD)* | DoT window | `dot_expires_tick` column | **ADOPTED** — bleed is 540/3 s at **+100 % duration** |
| M-26 | per-(tick, target) | schema obligation + **AC-11.7b** | ADOPTED — tested, not conventional |
| M-27 | path rate + coincidence | `tracks.player_path` on the tick grid, stride 1, bit-identical to `circle_sweep` centre | ADOPTED — **AC-11.7c** |
| **M-28** *(SHOULD)* | run summary | `run_summary{}` | **ADOPTED** — emitted so drax's joins can be *asserted*, not just computed |

**What drax explicitly did NOT ask for, recorded so the coverage check never reads absence as
oversight:** monster position tracks (M-21 + M-26 + M-14 constrain him tightly enough, and full paths
would invert R-KC2-7 and cost the most bytes) · camera / lighting / VFX selection / animation / audio
/ crowd micro-spacing / disc rotation phase · bonus timer, tributes, score, rewards, mutator
identities, defense structures, M2 rewind, devotion procs, Ascension, retaliation — all of which
appear as a **NOT-MODELLED strip on frame and nowhere else** · a scripted wave 160 (L-11) · any
sidecar or NDJSON split at v1.

---

## § 12 — Tolerance table — **PINNED (G-B close, conductor, 2026-08-08)**

> Charter § 4.1: tolerances are pinned at **G-B close**, from **Phase-A instrument data**, **before
> any build begins.** Goalposts precede results; they do not precede knowledge of instrument noise.
> **PINNED as the conductor's act at G-B close: T-1..T-8 + MO-1..MO-5, exactly as tabled below.
> The G-D gate binds against these rows as written; any later change is a ledgered ruling, not an
> edit** (ledger G-B verdict block).

| # | Quantity | Instrument value | Comparison class | Grade |
|---|---|---|---|---|
| **T-1** | **per-wave clear-time interval** | **± 1.0 s semantic floor** | **per-wave**, or two-class (**×10 vs non-×10**) — **NEVER a pooled mean over the bimodal mix (28.57 s vs 14.29 s)**. Comparisons model **tick-quantised** intervals | **the anchor (L-13)** |
| T-1a | *instrument precision* | ± 0.05 s / transition (± 0.07 s / interval) | **NOT the pinnable number** — *"the instrument is far finer than the thing it is pointed at"* | do not pin |
| T-1b | badge-vs-last-kill lag | ≤ 1 game tick, same-signed | **contained inside T-1 — never added to it** | contained |
| T-1c | s2 band | ± 1.0 s, by deliberate under-claim | n = 9 has no power to claim finer | under-claimed |
| **T-2** | count model — intra-order + rounding + clamp | **1.9 %** (5.5 monsters on 292, waves 151–170) | wave-total counts | declared residual |
| **T-3** | count model — **U9-6 bonus spawn** | **RESOLVED: p06 = ON, measured** (L-21 census) | branch RETIRED — counts run the p06-on table | **closed**, no tolerance carried |
| **T-4** | energy drain rate | **PINNED: PER_TICK, 176.4 / s @ 196 % AS** (client-verbatim, L-22) | drain rate now BINDS alongside ceiling/reserve; Soulfire term declared-separate (§ 3.1) | **closed** — fork collapsed |
| **T-5** | devotion envelope | error-bar **classes**, not a scalar: defensive-trigger (opposition-dependent) · dual-bound (Shifting Sands ~200×) · piloting-parameter | envelope disclosure | structural (L-3) |
| **T-6** | monster damage | **upper bounds only** (G-2 rank binding unread) | INFORMATIVE rows only | declared ceiling |
| **T-7** | fixture identity | **+3.9 % / −0.5 %** | every derived player stat | declared envelope |
| **T-8** | opposition eHP chain (§ 6.2b) | nemesis class **± 0.05 %** (measured −0.004 % / +0.002 % under the § 10.7 lookup law, two independent curves) | every opposition-eHP consumer (AC-6.5); **p04 = declared ± 5 % band, INFORMATIVE-side only** (−4.3 % named gap; no p04 spawns inside the BINDING s1 band; galadriel board-closure question in flight) | **pinned (L-29)** |

**Micro-oracle rows (BINDING per R-KC2-2 — direct-binding, calibrate FIRST):**

| Oracle | Target | Tolerance |
|---|---|---|
| **MO-1** energy usable ceiling | **1594 / 2576** | `PIN` — exact-integer expected |
| **MO-2** energy reservation | **982 — exact-integer** (BINDING-and-derived; bundle § 3.3 ledger, L-26) | `PIN` — derived from DB, not hard-coded |
| **MO-3** s2 in-combat energy | **1477 / 2576** | `PIN` |
| **MO-4** HP orb / max health | **20,005** | `PIN` — two independent instruments agree (sheet + in-combat orb) |
| **MO-5** cycle floor | **~7.0 s** (7.03 / 7.05 / 7.07 observed) | `PIN` as a **floor**, one-sided |

**Ordering for G-D (charter Phase D):** micro-oracles (direct-binding) → s1 ramp 1→93 through the
envelope (BINDING) → s2 one-sided inequality (INFORMATIVE tripwire: sim kit-alone at 151–160 must
clear **≤** fixture-with-defenses; **faster ⇒ anomaly tripwire → finding**) → full-ladder runs beyond
the fixture bands (reported, unbound).

**Note on the s2 inequality's expected margin (L-12a):** the fixture had **+offense AND
−enemy-threat** (Vanguard + Stormcaller on the output side; Deathchill + Inferno on the intake side).
The inequality's *direction* is unchanged, but the expected margin is **wider** than a naive reading
suggests. Declare this in the G-D interpretation.

---

## § 13 — Named-HALT register

Per charter § 4.2, each row is a value the spec needs that is **absent from the probe corpus**. None
is improvised, estimated, or fetched externally.

> **BUNDLE RETURNED (L-26; note `legolas/notes/2026-08-08-kc2-halt-bundle-microprobe.md`): 6 CLOSED,
> 1 PARTIAL, 1 CLOSED-BY-TYPE; HALT-7 unfired by design; HALT-10 OPENED at fold (F-6), returned +
> ruled at L-29.** Register restated with outcomes:

| # | Value | Outcome (L-26) |
|---|---|---|
| **HALT-1** | Shield lifetime for `Skill_BuffSelfShield` | **CLOSED** — the `.tpl` declares **no duration field at all** (nor its four includes); clone of `Skill_BuffSelfToggled.tpl`. **Absorb-POOLS, not timed buffs.** Bonus: Arcane Barrier's 2900 is **type-gated away from Physical** → § 9.4 envelope re-runs its row (merge-pass touch) |
| **HALT-2** | Player base movement rate (m/s); `delayMovement` magnitude | **CLOSED-BY-TYPE** — `characterRunSpeed = 0.92` is a *dimensionless multiplier* (1,467-record census: median/mode 1.0); engine m/s reference **NAMED-ABSENT**; `delayMovement` is `bool`, no magnitude exists. **Adopted disposition: declared free parameter `v_ref`** (bundle § 6.1 recommendation), calibrated at D against traversal times; fixture is AT the run-speed cap (135 = `playerRunSpeedCapMax`) |
| **HALT-3** | P(crit) from OA vs DA | **CLOSED** — `records/game/combatformulas.dbr` **was in the base archive**: `probabilityToHitEquation` verbatim; crit = **PTH-band** mechanic (6 thresholds → ×1.0…×1.5, `pthMinimum = 55`). Band *semantics* INFERRED → gamora proves by test (§ 4.2) |
| **HALT-4** | Damage application order | **PARTIAL — ORDER-1 (convert-then-modify) FAVOURED** (1.26× vs 1.84× residual), not proven: 3.2 % signal under ~20 % un-enumerated devotion/component remainder. Weapon term **CONFIRMED** (solved w = 0.671 vs DB 0.64, +4.8 %); **crit proven EXCLUDED** from the sheet window; missing `× (1 + cunning/245)` = ×5.98 supplied by `physicalDamageEquation`. Spec declares ORDER-1; **residual enumeration = G-D contingency alongside HALT-7** |
| **HALT-5** | ≈ 358 unattributed reservation | **CLOSED-EXACT — 982 = 982** (§ 3.2 ledger; Presence of Might 300; Divine Mandate reserves 0; `characterManaLimitReserveModifier` dead corpus-wide) |
| **HALT-6** | Monster→player mitigation model | **CLOSED** — two-branch armour equation, `armorDefensiveAbsorption = 70.0`, per-hit **body-region sampling** (7 regions, weights Σ100), `playerDefenseCap = [80,80,80]`. Monster damage rows stay INFORMATIVE per R-KC2-2 |
| **HALT-7** | Boss-skill rank binding per wave | **UNFIRED — pre-registered G-D contingency, unchanged** |
| **HALT-8** | Soulfire `projectilePeriod` unit | **CLOSED** — Crate's own annotation *"Delay between projectile launches (seconds)."* **0.2 = plain seconds, no ×0.8.** Now also the **Soulfire cost-interval basis** (§ 3.1, L-22) |
| **HALT-9** | Wave-dependence of non-emitted fields | **CLOSED** — full 600 × 28 grain emitted (§ 10.7); 33 non-zero fields (25 arrays / 8 scalars); 9 U-8 columns byte-identical; `offensiveTotalDamageModifier` +43 @160 / +130 @200; `offensivePhysicalModifier` −21 @160 Glad. **F-4 adjudicated as a side effect** (§ 14) |
| **HALT-10** | **Opposition eHP composition beyond the wave-scaling array** | **CLOSED (nemesis class) / PARTIAL (p04) — L-29.** Five-link chain extracted DB-cited (§ 6.2b): apl → `levelVarianceEquation` spawn level → **per-record `charLevel` re-evaluation** (four forms; `lv8_boss+` is a POINT = 106) → five bio `characterLife` curves → **ADDITIVE M = 1 + 5.80 (Ultimate `characterLifeModifier[8]`) + G/100 (§ 10.7 array, lookup law) + own/100**. Lands F1 = 3,722,896 (−0.004 %) and F2 = Kubacabra P1 2,955,749 (+0.002 %); the L-17 interim ≈1,308,800 and P-E6's 827 k are **SUPERSEDED**. **Residue: p04 −4.3 % named gap** (Galakros favoured; nine explanations ruled out by reading) → declared **± 5 % band, INFORMATIVE-side** (T-8). Probe note `legolas/notes/2026-08-08-kc2-ehp-composition-probe.md`; sim consumes `t20_wave160_board_ehp.csv` (glad_cell = 322 rows). See **F-6 (RESOLVED)** |

**Declared-not-HALT** (unknown but carrying a *declared* disposition rather than a hole): emitter
world positions (DECLARED free parameters, per-sitting sets, § 10.6) · mutator identities
(OUT-OF-MODEL, **six** glyphs confirmed, 25-pool prior, § 10.3) · `maxGroupSize` concurrency
semantics (safe model, start anchor measured, § 10.6) · Shifting Sands host delegation (DUAL-BOUND,
§ 9.4) · `v_ref` movement reference (free parameter by bundle § 6.1 disposition) · Soulfire
cost-term effective magnitude (declared-separate, fixture-sustain-bounded, § 3.1). *(Former members
CLOSED and struck: energy-drain unit → PINNED L-22; U9-6 → measured ON L-21.)*

**Corpus hygiene (L-26):** the Edition-II pin ships **no `templates.arc`** — bundle `.tpl` citations
are graded `TPL-CITED (Edition-I, freshness-probed)` (all 19 field names probed present; numeric
values kept on Edition-II `.arz`). **The pin should acquire `templates.arc`** — run-end hygiene row.

---

## § 14 — FINDINGS for the conductor (contradictions surfaced while drafting; NOT resolved here)

> Per commission: contradictions between sources are **findings for the conductor**, reported, not
> adjudicated by the spec author.

### F-1 — The RF gap-table row dissolves; the charter still carries it as live

> **RULED — L-20:** dissolution ADOPTED; charter § 3 row annotated in-run (veto-open, § A.2b
> precedent). The gap-table-vintage observation is logged as its own finding.

Charter § 3's Phase-B row list names *"RF charge-stacks EXTEND"* as a spec section. **The fixture has
no Righteous Fervor** (save-parse § 2.2: 28 ranked skills, `righteousfervor1` not among them, on a
migration with 0 of 318 entries changed; build-of-record § 1.6 never prescribes it). The row is
v2-leveling-spine inheritance that the v3 ENDGAME-FIRST ruling superseded. **§ 4 states the
dissolution; the conductor may want to amend the row list at fold** so the gate does not look for a
section that correctly contains nothing. *(This makes **two** of eight gap rows dissolve against the
endgame fixture — block and RF — which is itself a finding about the gap table's vintage.)*

### F-2 — ⚠ The "Gladiator scalar block" folded at ledger § A.6 is a **wave-100 slice**, and the wave-160 nemesis HP figure is understated **1.58×**

> **RULED — L-17:** ADOPTED (conductor grep-verified against the CSV); ledger § A.6 annotated as
> the wave-100 slice, twice; the U-8 CSV governs; HALT-9 graduated to the L-19 bundle, priority-1.

This is the highest-consequence contradiction found while drafting.

- **P-E6 § 2.8** presents `balancingadjustment_survivalmode_enemies03.dbr` as *"Gladiator monster
  scalars"*, stating in its own preamble: *"values at array index 99 (level 100)"*. Ledger § A.6
  folded these as a **"sim-consumable scalar block"** — reading as difficulty constants.
- **U-8 emitted the same record family at full 200-row grain.** Cross-check at wave 100, Gladiator:
  life **168**, OA **26**, OAmod **2.1**, DA **33**, DAmod **3.0**, AS **8**, cast **8**, life-regen
  **20**, heal **−43** — **all nine columns match P-E6 § 2.8's Gladiator column exactly.** § 2.8 *is*
  the wave-100 row.
- **These fields are wave-indexed.** Gladiator `characterLifeModifier`: wave 100 = **168**, wave 150 =
  **304**, wave 160 = **324**, wave 170 = **344**, wave 171 = **420**, wave 200 = **990**.
- **Consequence.** P-E6 § 4.1 / § 6.5 compute wave-160 nemesis effective HP as
  `308,685 × (1 + 1.68) ≈ 827,000`. Under the wave-160 row the same base gives
  `308,685 × (1 + 3.24) ≈ **1,308,800**`. **The showcase wave's HP is understated by a factor of
  1.58.** Any TTK estimate, kill-rate expectation or Phase-E narrative-shape judgement built on the
  827k figure is wrong in the direction of "the sim will look too slow."
- **Second-order:** U-8 § 2.5's own prose table has two transcription errors against its own CSV —
  it prints wave 160 Gladiator **328** (CSV: **324**) and wave 160 Challenger **240** (CSV: **229**).
  **The CSV governs**; the prose table should not be cited.
- **Third-order → HALT-9, now CLOSED (L-26):** U-8 emitted 9 of the record's non-zero fields; the
  remainder were known only at index 99 (the +20 % / −15 % / −40 % figures in earlier drafts are
  that wave-100 slice). The bundle's full-grain emission settles it: **33** non-zero fields
  (25 arrays / 8 scalars), and the arrays **ramp hard** — `offensiveTotalDamageModifier` **+43 % at
  wave 160, +130 % at wave 200**; `offensivePhysicalModifier` **−21 %** at wave-160 Gladiator.
  § 10.7 carries the CSV pointers; the § A.6 flat-block reading is dead twice over.

**This spec uses the U-8 CSV throughout (§ 10.7) and marks the ledger § A.6 block superseded. The
conductor rules whether to amend § A.6, re-lap the emission (HALT-9), or both.**

### F-3 — Two of P-E1's open items are already closed by a charter-§2 substrate document

> **RULED — L-18:** sheet constants ADOPTED as spec constants (0.0816 s → 12.25 ticks/s; regen
> 75.37/s); P3/P4 closed against substrate; the L-6 ladder gains rung (a′) — channel-without-contact
> energy-direction read (+59.4/s vs −120.6/s), assessed against galadriel's return at fold. The
> fork itself stays unruled per charter § 4.2.
>
> **POSTSCRIPT — L-22:** the fork closed at rung (a) — in-video tooltip, § 3.1. F-3's two
> quantitative predictions both resolved for **M2**: the tooltip's 176.4/s is the per-tick reading,
> and the leech-load-bearing sustain arithmetic is exactly what item 2 below predicted. Rung (a′)
> was never needed — MOOT.

P-E1 § 8 lists **P3** (*"the build's total attack speed %"*) and **P4** (*"the build's energy regen
/ s"*) as open, each closable by *"one character-sheet frame."* **That frame was already read.** The
ceremony cross-verification note (`gandalf/notes/2026-08-05-eor-ceremony-cross-verification.md`
§ D, character-sheet tab II `#511`) records: **Attacks per Second 2.66 · Attack Speed 196 % ·
Critical Damage +57 % · Run Speed 135 % · Health Regeneration 129.38 · Energy Regeneration 75.37 ·
Energy Absorption 20 %.**

That note is in the charter § 2 substrate manifest but **not** in this commission's enumerated read
list; I reached into the manifest to source A1 and found it there. **Two consequences the conductor
should weigh:**

1. **The channel machine's effective cadence is now a measured quantity**, not a placeholder:
   0.16 / 1.96 = **0.0816 s → 12.25 ticks/s**. Every proc-rate and saturation argument in § 9 is
   computed on it.
2. **It bears on the L-6 drain fork, and I have deliberately not ruled on it.** With regen at
   **75.37/s**: M1 implies a gross drain of 16/s against 75.37/s regen — the bar would sit pinned at
   the ceiling and the observed **86–117 draw-down at wave 158** would be hard to produce. M2 at the
   fixture's AS implies **196.1/s** gross, which needs Tip the Scales' ≤100/s leech to be up most of
   the time to explain a merely-86–117 dip. **Both readings now make quantitative predictions that
   the existing footage can test.** That is a conductor's call on the L-6 ladder — possibly a cheaper
   closure than the tooltip screenshot — and it is emphatically not mine to make (charter § 4.2).

### F-4 — Monster retaliation figure disagrees across two sources

> **RE-RULED — L-26, F-4 DISSOLVED (supersedes L-20's low-stakes clause):** the bundle's full-grain
> read adjudicates it — **both sources are right at their own wave.** The 08-01 note's "74 Glad /
> 53–54 lower" is the **wave-150–170 plateau**; P-E6's "+22/+24/+16" is **wave 100**; the ordering
> genuinely **flips at wave 112**. No mismeasure needed — **L-10(b) is not required to explain F-4**
> (it remains true of the 08-01 note's provenance, just not load-bearing here). Figure in force at
> the showcase band: **Gladiator 74**, from the full CSV.

The v3 directions' closing opposition note (from the 2026-08-01 density probe § 3.2) states the
Crucible balancing records carry **`retaliationTotalDamageModifier` of 74 at Gladiator versus 53–54
at the lower difficulties.** P-E6 § 2.8 measures the same field at **+22 % Gladiator / +24 % Aspirant
/ +16 % Challenger** — a different magnitude *and a different ordering* (the 08-01 reading has
Gladiator highest; P-E6 has Aspirant highest).

L-10(b) already established that the 08-01 note **measured Aspirant** where it believed it was
measuring Gladiator, which explains part of it; HALT-9's wave-indexing question may explain the rest.
**Not resolved here.** It matters because § 8 excludes *player* retaliation while § 6 carries
*monster* retaliation as a live opposition property — the one place in this spec where a retaliation
number is load-bearing.

### F-5 — The v3 directions carry a superseded Crucible-density claim

> **RULED — L-20:** parked to run-end hygiene; v3 § 5.4 corrigendum rides legolas's next v3 touch;
> the play-test directions are not re-cited as a count authority meanwhile.

v3 § 5.4 tells Matt, as a "second measured fact worth knowing while you play," that
*"`spawnMinAdj` and `spawnMaxAdj` are **zero on all three difficulties**"* and that Crucible
difficulty is *"not a density dial."* **U-9 supersedes this.** The `*Adj` arrays are indeed zero, but
that is not the operative term: `spawnMinModifier` (**×1.20** on Gladiator) and the additive
`spawnMin +1` **are**, and they move 68 % → 93 % of pools to deterministic counts plus a real count
increase. The claim was directionally right about *why* Gladiator is harder (HP does most of the
work) and wrong about the mechanism. Low consequence for the sim, which uses U-9's model — flagged
so the play-test directions are not re-cited as a count authority.

### F-6 — The measured wave-160 HP fingerprints exceed the corrected model ×1.75–×2.84 — an unextracted composition term

> **RULED — L-24:** FINDING ACCEPTED; **HALT-10 OPENED and FIRED** (targeted legolas micro-probe);
> § 6's opposition-eHP formula must carry the composition term **EXPLICIT and DB-cited before gamora
> builds the opposition stack** — a ~2× eHP error at the BINDING s1 band swamps the ±1.0 s floor,
> and charter § 4.2 forbids fitting it away. The rest of Phase C is unblocked.

> **RESOLVED — L-29 (HALT-10 return; probe note
> `legolas/notes/2026-08-08-kc2-ehp-composition-probe.md`):** the two missing terms were
> **Ultimate's additive +580 %** (`balancingadjustment_mp+difficulty_enemies01.characterLifeModifier[8]`)
> and **two-stage level re-evaluation** (spawn level = 106 via `levelVarianceEquation`, then the
> monster record's own `charLevel` equation re-evaluates it — the `×1.1`-group form `*1.1+2` → 118.6
> produces exactly the ×1.62 spread the shared-base model could not). All modifiers compose
> **ADDITIVELY** (`characterLifeMultModifier` = 0 solo is the DB's own statement; a multiplicative
> build overshoots ×2.9 and fails AC-6.5). Joined under the § 10.7 **array-lookup law** (fighting
> 160 reads label-159's 322), the chain lands **F1 = 3,722,896 vs predicted 3,723,043 (−0.004 %)**
> — a `×1.1`-group nemesis — and **F2 = 2,955,796 vs Kubacabra P1's 2,955,749 (+0.002 %)** — unique
> bio on the board ⇒ **the p02 draw MEASURED; Grava'Thul eliminated** (slot argument, not eHP —
> he is `×1.1`-group himself). **F3 = p04 stays a −4.3 % named gap** (Galakros favoured; nine
> explanations ruled out by reading) → declared **± 5 % band, INFORMATIVE-side** (T-8). Board floor
> **≈ 9.4 M measured** (~2.3× the superseded model; ≈ 13.1 M if the dedupe-twin holds). The probe's
> one consequence error — "HALT-9's +43 becomes +41" — is **conductor-STRUCK** (43 plateaus across
> labels 158–160 in the full-grain CSV; no cell carries 41). Chain + law: § 6.2b / § 10.7. Tolerance:
> T-8. Board identification + prediction menu: § 10.8. The galadriel board-closure question
> (remaining three fingerprints · census methodology top-N-vs-all · p04 visual ID) fires
> Phase-C-concurrent and folds at its return.

galadriel's census read three boss-class HP fingerprints on wave 160: **3,722,896 · 2,955,796 ·
2,295,755.** The L-17-corrected model gives `308,685 × (1 + 3.24) ≈ 1,308,800` — residuals
**×1.75–×2.84**, and the **×1.62 spread** between fingerprints is the sharper fact: 15 of 16 nemeses
share the same base record, so a shared-base model cannot produce it. *(galadriel's own "2.8–4.5×"
side-note was computed against the stale 827 k denominator — her brief predates L-17; restated here,
not edited in her seam.)*

- **Prime suspect is named by P-E6 itself:** the 308,685 base is quoted *"before ordinary Ultimate
  difficulty scaling"* — and that composition chain (proto HP → spawn level via the level-indexed
  `characterLife` curves → hero/boss rank multipliers → difficulty term) **was never extracted**.
  The L-19 bundle's HALT-3/6 scope was hit/crit/armour equations, not HP composition — **the bundle
  did not close this** (its § 9 not-resolved list confirms).
- **Candidate mechanisms for the probe:** H1 spawn-level re-evaluation (the gdx3 curve
  `((charLevel×44)^1.53)+6000` moves the residual band substantially if nemeses spawn above the
  proto's quoted level); H2 hero/boss rank multipliers (G-2 territory); H3 per-nemesis proto
  variation (the 16th record); H4 mutator HP terms (out-of-model — if implicated, it becomes a
  declared confound on the census, not a sim term).
- **What closes it:** DB-cited composition chain reproducing all three fingerprints within a stated
  envelope, or an explicit NAMED-ABSENT verdict that demotes s2-side eHP realism to
  INFORMATIVE-with-declared-gap (R-KC2-2 already shields the BINDING split — but s1-band trash eHP
  uses the same chain, so the term must land either way).

---

## Closing note

The spec's load is carried by three things and it is worth naming them plainly. **The channel is
build-invariant**, which is a bounding negative result and lets § 1 be short. **The Crucible is
deterministic to 93 %** on Gladiator, which means the wave engine needs the right constants far more
than it needs a rich sampler. And **the fixture's own instruments — a red numeral, an energy globe,
a tribute counter — turned out to be finer than the datamine on exactly the questions the datamine
could not answer.** Where those three agree, this spec is confident. Where they do not, § 13 and
§ 14 say so out loud rather than splitting the difference.

The one place I would point the conductor first: **F-2**. A 1.58× understatement on the showcase
wave's monster HP is the kind of error that survives every gate downstream of it, because everything
downstream is *consistent* with it.

---

**Filed:** named-gandalf `SPEC-AUTHOR`, 2026-08-08, KC2-SIM Phase B. Uncommitted per charter § 4.7.
Every row DB-cited or named-HALT. Tolerances prefilled for the conductor's pin. Schema DRAFT pending
star-lord + drax consult.
