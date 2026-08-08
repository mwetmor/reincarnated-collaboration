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

### 2.2 Truth boundary (R-KC2-7) — and the locomotion model of record

The player path and the circle sweep are **sim-owned causal truth** and are baton payload
(§ 11.4). ~~Presentation owns locomotion *aesthetics* — how a monster's approach between spawn and
engagement is choreographed — within the constraints the baton fixes.~~ **AMENDED at the L-46 fold
(F-12 / L-46(a)): under a static board a monster's approach was aesthetic; under motion it is
CAUSAL, because this kit's damage predicate is an AREA that sweeps (§ 2.1). A monster that crosses
the disc while travelling takes ticks it would not take standing still, and a monster that arrives
late is alive for ticks it would otherwise have missed.** The boundary therefore moves one notch:
the sim owns **where every actor is, over time, to hit-test resolution**; presentation owns gait,
footfall, turn-in-place, crowd micro-spacing, camera and VFX **within** the emitted motion. The sim
emits the player's position at a stated sample rate, and the disc centre is that position:
presentation must never re-derive the sweep, because re-deriving it would let the picture disagree
with the damage. **The same non-re-derivation rule now binds monster motion** — with a baton
consequence the schema does not yet carry (**R-LOCO-1**, § 10.9a G).

**Locomotion model of record — `path-to-zone` THEN `pursuit-gate`** *(conductor ruling L-46(a),
reasoning-boundary, **veto-open**; supersedes L-43 C-3's "monsters path to the player")*. The
mechanism is SOURCE-CITED, in Crate's own comments:

- **Non-ambush spawns are told to follow a set path to a named group.**
  `sm_mod/game/events/survivalevent.lua:552` links each spawned proxy to a patrol-point group —
  *"patrol point group the spawns should head to upon spawning"* / *"Execute the proxy to dispense
  monsters and follow the set path"* — and **17/17 Crucible tier modules set
  `patrolPoint = "PatrolPoint_Attack"`, all 200 waves.** The destination is arena-resident: a group
  of **173 decoded patrol nodes**, median **18.85 m** from their own centroid (§ 10.6 layer 1).
- **Pursuit of the player is a SEPARATE, gated controller behaviour** — not the spawn instruction.
  Every band-A record points at a `ControllerMonster` DBR (**126 distinct, 0 missing**) declaring
  `ViewDistance` **80.0 m** (868/895), `MaxPursuitDistance` **125.0 m** (868/895) and `PursuitTime`
  **10 000 ms**.
- **Ambush spawns are excluded from the patrol link by construction** — `IsAmbush() == false` gates
  it. p05 is the ambush point (§ 10.6), and its measured radius (median **10.17 m** vs the ring's
  **37.53 m**) agrees with that exclusion from a second, independent direction.

**This shape is the HYPOTHESIS the lap TESTS, never an assumption it inherits.** The fixture's
fingerprint is a clear time that barely tracks body count (**r = +0.154**) against a static-board
sim that tracks it strongly (**r = +0.737**). A model in which the *monsters* travel is the less
body-count-coupled family, which is why it is adopted — but adoption is a starting hypothesis with a
pre-registered test (§ 10.9a F), and **T-1 is UNCHANGED** (standing safety #1). If the amended model
also fails T-1, that is a finding, not a licence to widen the goalpost or to fit `v_ref`.

**One discriminability caveat, stated here so nobody reads more into the ruling than the citations
carry.** `ViewDistance = 80 m` **exceeds every measured emitter radius** (max 47.89 m) and
`MaxPursuitDistance = 125 m` exceeds every arena's full diagonal — so for a player anywhere inside
the arena the pursuit gate is **open from t = 0**, and the priority between "follow the set path"
and "pursue the acquired target" lives in the executable, which no pin contains
(**NAMED-ABSENT**). The two limbs are therefore near-indistinguishable for a centrally-camped
player and diverge only for an off-centre one. § 10.9a A carries both limbs with the ruled default
and the divergence condition; the lap reports which limb it ran.

### 2.3 Composition + telegraph law

- Composes with the arena shell in § 10.6 (6 emitters, `placementExtents = 8.0` scatter, single
  player spawn) — *amended L-46: the emitters now carry **cited per-arena radii** (ring median
  37.53 m, p05 ambush 10.17 m), and the actors on them **move**; the movement rules are § 10.9a.*
- **G-1h under motion [consequence, not a restatement].** The reconstruction bar below was
  satisfiable from `{centre, radius, tick}` alone only because the board was static and each
  actor's position was its emitted `spawn_x/spawn_y` forever. Once actors move, hit/no-hit is a
  function of **two** trajectories, and the emitted set must permit reconstruction of the monster
  one as well. This is a baton-schema consequence and is registered as **R-LOCO-1** (§ 10.9a G),
  routed — not landed here, because § 11 is a signed cross-seam contract.
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
- ~~**Soulfire carries a SEPARATE, DECLARED cost term NOT inside 176.4**~~ — **STRUCK L-35:
  Soulfire declares NO cost.** The "3–20 rank-scaled `skillManaCost`" this bullet carried was a
  **spec-authoring fusion** (SPEC-AUTHOR error, owned at L-35): the array belongs to
  **Disintegration** (`aetherray2.dbr` — P-E1 § 5 cited it as a *control*, not as Soulfire);
  `eyeofreckoning2.dbr` omits the field entirely, as do 474/476 `SkillSecondary_*` records. The
  0.2 s-plain-seconds interval basis (HALT-8) remains true of the record it belongs to. Nothing
  folds into `drain_rate_per_s`; the magnitude tension, its admissibility bound, and **F-8 are
  RETIRED premise-withdrawn** — gamora's `effective_per_s = 0.0` graduates to **DB-CITED** (the
  record's silence is the citation). Full retirement: F-8 (§ 14). Bonus coherence:
  `eyeofreckoning1` carries `skillManaCost` [4..16], rank 26 = 16.0 — the drain constant's own
  home (16.0 × 12.25 × 0.90 = 176.4/s).

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

**Leech stacking RULED — NON-STACKING, refresh-on-reproc [L-32/E-1].** The 2.0 s duration on a
1.0 s cooldown arithmetically admits two concurrent instances; the ruling is non-stacking on three
independent legs: (i) GD same-source buff behaviour is refresh-not-stack; (ii) this section's own
"100/s **while up**" is a state predicate, not an instance count — and § 3.1's sustain arithmetic
(nets ≈ −1/s) was authored on that reading; (iii) the BINDING instruments are unproducible under
stacking — net would be **+98.97/s**, the pool pins at the usable ceiling, and neither the s2
in-combat **1477** nor the 86–117 draw-down band (§ 3.3) can occur. The stacking reading's side
effect of nearly admitting the naive Soulfire 100/s is NAMED AND REFUSED as a reason — adopting a
mechanism to rescue an inadmissible constant is the fitting charter § 4.2 forbids.

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
| per-wave composition (pools, rosters, weights, record paths) | **P-E6 emissions** — `pe6_crucible_wave_pools.csv` (1,998 rows), `pe6_crucible_waves.csv` (200 rows), `s4_waves_full.json`. **L-35 exemption-aware supersession:** consumers needing `ignoreGameBalance` read `legolas/scratch/2026-08-08-kc2-e2-exemption/pe6_crucible_wave_pools_v2.csv` (1,998 rows + per-pool flag; SHA `bbdc18f1…`) + `pe6_pool_ignoregamebalance.csv` (635 pools, **74 exempt**; SHA `40182de2…`, conductor-verified). Exemption is a **per-pool CITED fact, never a class heuristic** — exactly one non-boss exempt pool exists (`celestialmonstrosity_t3`, trash) |
| per-wave counts | **U-9 count model** (§ 10.5) — *"count from U-9, composition from P-E6"* is declared in both notes |
| per-wave monster scaling | **U-8 emission** `u8_survival_wave_scaling.csv` — joined via the **§ 10.7 array-lookup law (CORRECTED L-33): fighting wave *w* reads 0-based index *w*−1 = the cell LABELED *w*** |
| monster level | **SINGLE-STAGE + DECLARED OFFSET (L-33; supersedes the HALT-10 two-stage):** the proxy `levelVarianceEquation` sets the level — nemeses `lv8_boss+` = POINT `(apl+4)+(apl/50)` = **106** at L100; p04 `lv7_uber` min `(apl+3)` = 103; p06 `lv6_hero` 104–105 — **plus a MEASURED +3 offset** (nameplates: nemeses **109**, Galakros **106** = uber-min+3, Bileeater summon 112; measured on two independent proxies/bodies; **DB source NAMED-ABSENT** after an enumerated search — carried as a **DECLARED sim input**, § 6.2b). The old stage-2 per-record `charLevel` re-evaluation is **STRUCK** (`character.tpl` scopes that equation to MANUAL placement; `Proxy.Create` passes no level; the 118.6 was a degeneracy artifact — probe § 3.2). Trash `lv2_normal`/`lv3_strong`. **No player-level gate on tier access**; at L100 every `minPlayerLevel{j}` roster gate is open (P-E6 § 2.7). **No Epic/Legendary variance branch exists** — re-swept 0 of 32 corpus-wide |
| boss concurrency | **engine cap explicitly defeated.** `survivalevent.lua` L548 verbatim: `Proxy.Create(…, …, true) -- true for 'ignore boss spawn limit'`, on **every** wave spawn. Campaign boss-concurrency intuitions do not transfer (U-9 § 5.5) |

### 6.2b Opposition eHP — the four-link composition chain (L-33; supersedes the HALT-10 five-link)

**CLOSED EXACT — 8/8 camera-named bodies (7 distinct values), residual 0, zero free parameters.**
Probe: `legolas/notes/2026-08-08-kc2-groupassign-microprobe.md` (falsification: per-body level
unique over L∈[80,160] = the camera nameplates 8/8; joint (G, L) unique over a 16,200-pair scan).
**Source-of-record: `legolas/scratch/2026-08-08-kc2-ehp-composition/t21_wave160_board_ehp_r2.csv`**
(39 rows × 33 cols; per-row provenance incl. `charLevel_grade`). The HALT-10 `t20` CSV and its
`glad_cell = 322` consumption rule are **SUPERSEDED** (the 322 cell scores 0/8, all −0.177 %).

> **⚠ BINDING consumption rule (conductor-measured hazard, L-33(i)):** the 3 Kubacabra P2/P3 rows
> (`nemesis_beast_01_p2a/p2b/p3a`) carry `verdict = PREDICTION-uncorroborated` — class-identical to
> the 28 rollable pool alternatives; the must-not-sum distinction lives only in the note column.
> **Exclude `nemesis_beast_01_p{2,3}*` rows from any Crucible board enumeration.** legolas emits r3
> with a distinct `phase-UNWIRED-in-crucible` verdict class on his next touch.

```
L          = levelVarianceEquation(apl) + 3           proxy lv*.dbr band + MEASURED offset (DECLARED input)
base_life  = characterLife(L)                          bio curve (characterAttributeEquations), winner-only
M          = 1 + 5.80 + G/100 + armorbaseNN[L−1]/100   ADDITIVE — see below
eHP        = floor(base_life × M)                      floor, not round (round misses 5 of 8 bodies)
```

- **Level is SINGLE-STAGE + declared +3.** The nameplate level IS the HP-equation level (probe
  § 8.1 — substituting the camera numerals closes 8/8 exact with unique solutions). The +3 above
  the proxy band is MEASURED on two independent proxies (`lv8_boss+` 106→109 · `lv7_uber` min
  103→106) and its **DB source is NAMED-ABSENT** (enumerated search: 32 variance records, 627
  adjustment fields, `gameengine.dbr`, the survival Lua — no level term anywhere). ~~Two
  observationally-equivalent readings — (a) +3 offset · (b) `averagePlayerLevel` evaluating to 103 —
  are non-discriminable from a single wave; a nameplate read at any other wave separates them
  (galadriel follow-up in flight, L-33).~~ **DISCRIMINATED — L-37(a), the follow-up fired (third
  extraction): reading (a) +3-offset WINS; the apl-evaluation reading is STRUCK.** Camera: level
  does NOT track wave (w20 common 102/103 vs w158 common 104 — 2 levels across 138 waves); nemesis
  **109 INVARIANT at w90 AND w160** (4/4, two arenas); within-wave same-TYPE spread up to 5 (w151
  Carnivorous Plants 103 AND 107, ×4 consecutive-frame audit). Kill shot for (b): **champions read
  103–104 at s1 (w40–80) but 109–112 at w160 under the SAME character** — a pool-blind
  `f(apl, rank)` cannot produce the divergence, and any per-pool patch of (b) IS (a). Standing law:
  nameplate/HP-equation level = the per-body `levelVarianceEquation` band draw over the **proxy's
  own wave-invariant level fields** + the MEASURED +3. The sim carries +3 as a **stated input, not
  a derived one** (DB source still NAMED-ABSENT — now multi-wave-measured).
  Summon levels: MEASURED per body (summoner's 109; Galakros's bloater 112 = +6); general rule
  NAMED-ABSENT.
- **STRUCK from the old chain (L-33, DB-cited):** the per-record `charLevel` re-evaluation
  (`character.tpl` scopes it to MANUAL placement; Crucible bodies are `Proxy.Create` spawns — three
  arguments, no level; the 118.6 was a degeneracy artifact, probe § 3.2) · the per-record own
  `characterLifeModifier` (falsified on camera: Bileeater's +50 breaks its own exact closure by
  +4.41 %; **Raddoth's +100 does NOT apply — "Raddoth = 4,102,036" is struck; he is 3,722,896 like
  every `bio_boss_nemesis_01` nemesis**; single-witness-graded).
- **REVERSED into the chain (L-33): `armorbaseNN.characterLifeModifier[L−1]` is REQUIRED.** Every
  wave-160 monster runs an armorbase passive at `skillLevel = charLevel`; array index = skill
  level − 1. Values on the board: `armorbase05[108] = 125` (nemeses, Death Revenant) ·
  `armorbase05[105] = 103` (Galakros) · `armorbase01[108] = 110` (Skeletal Archer) ·
  `armorbase04[111] = 129` (Bileeater) · `armorbase04[108] = 125` (Shard). HALT-10's exclusion
  test ran at the wrong level (118.6); at the true L this term closes the deviating bodies to the
  cent (−22/100 · −15/100 · +4/100).
- **M is ADDITIVE:** `1` + **5.80** (ordinary Ultimate/solo —
  `balancingadjustment_mp+difficulty_enemies01.characterLifeModifier[8] = +580` `[base]`, wired by
  `gameengine.monsterAttributePak`) + **G/100** (Gladiator wave cell per the CORRECTED § 10.7 law:
  **324** while fighting 160 = `characterLifeModifier[159]`, the cell labeled 160) +
  **armorbase/100** (above). Multiplicative composition still overshoots — **×5.746 all-three-term,
  ×2.664 two-term, every multiplicative reading scoring 0/8** per AC-6.5 *(~~×2.9~~ — the figure
  formerly here was the C-1 mixed-chain artifact: multiplicative WITHOUT armorbase against additive
  at the superseded G = 322; L-40 value-set sweep)* (structural guard retained);
  `characterLifeMultModifier` — the only multiplicative life term in the layer — is 0 at
  solo on every difficulty.
- **The wave-160 board, closed (8/8 EXACT):** 3,722,896 ×2 (Zantarin · Archmage Aleksander —
  **every `bio_boss_nemesis_01` nemesis is eHP-identical**; the "nemesis band" is a POINT; dedupe
  collision between any two non-Kubacabra draws is CERTAIN, L-33/C-11) · 2,955,796 (Kubacabra P1 —
  **single-phase in the Crucible, DB-CITED**: the phase chain is a death-spawn and [sm1] deletes
  its wiring, 994 vs gdx1's 995 fields; **the Crucible strips campaign-only mechanics** — loot
  chests, map nuggets, phase chains) · 2,295,755 (Galakros, L=106 — **EXACT**; the HALT-10 −4.3 %
  "named gap" was the missing armorbase term; § 12 T-8 RETIRED) · 484,095 (Aetherial Bileeater —
  **Galakros's summon**, skill12, 1/3) · 468,504 (Death Revenant — **Zantarin's summon**, skill6,
  1/3) · 103,912 ×2 (Aleksander's Shard — skill9, burst 2/6) · 41,237 ×3 (Skeletal Archer —
  Zantarin's skill13, burst 2/12). **DB-derived window total 13,981,477 = the camera-measured total
  EXACT** — two independent instruments, one integer.
- **⚠ Summons are a FLOW, not a stock (gamora TTK surface, G-D):** summons respawn (`petLimit`
  3/6/12; `spawnObjectsTimeToLive` 30–75 s) — total eHP destroyed over a wave is strictly greater
  than the instantaneous board. The r2 CSV gives per-body eHP + per-skill limits; the flow model is
  the sim's to build, not the probe's claim.
- **⚠ Overlay law (CORRECTED L-33/C-9): `.arz` overlay is WHOLE-RECORD REPLACEMENT, never
  field-merge** — every archive ships a complete record; the winner is the last archive's record
  ENTIRE (`base→gdx1→gdx2→gdx3→sm_mod→sm1→sm2→sm3`). A field-merge resurrects deliberately-deleted
  fields (exactly how Kubacabra's phase chain would have haunted the model). The two live wave-160
  traps stand: `colossusgalakros` (gdx1 curve vs governing sm1) and `tombguardian` (gdx2 vs sm2).
- **Exclusions, re-confirmed (L-33(j)):** monster rank carries NO direct HP term (H2 NAMED-ABSENT;
  rank differentiates indirectly via which `armorbaseNN` a record runs) · mutators neither wired
  nor needed · no Epic/Legendary variance branch (0 of 32 corpus-wide).
- **Scale:** the engaged wave-160 window totals **13,981,477** eHP (≈ 3.4× the superseded flat
  model's ≈ 4.1 M; supersedes the interim ≈ 9.4 M floor, which missed the summon layer and the
  armorbase term).

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
5. **AC-6.5** *(rewritten L-33 — supersedes the ±0.05 % two-fingerprint form)* The § 6.2b four-link
   chain reproduces **all eight camera-named wave-160 bodies (seven distinct values) at ±0 — exact
   integer equality** — against the r2 CSV of record (`t21_wave160_board_ehp_r2.csv`, § 6.2b
   consumption rule applied: `nemesis_beast_01_p{2,3}*` rows excluded). Three structural guards, each
   of which must FAIL if violated:
   - **Additive-M guard** — every multiplicative composition scores **0/8**; on the nemesis row
     the all-three-term multiplicative reading overshoots **×5.746 (M 64.87 vs 11.29)**, the
     two-term variant (armorbase added, G multiplied) ×2.664 (M 30.08). *(C-1 restatement, G-D
     fold: the earlier "×2.9 (28.83 vs 10.02)" mixed chains — multiplicative WITHOUT armorbase
     against additive at the superseded G = 322 — and survives only as a pinned superseded literal
     inside the guard test, so neither reading of the old prose can be silently picked.
     **Predicate-form lineage (D-W2 → L-40(d)):** this restatement also changed the guard's
     predicate FORM, ratio-threshold → **0/8 score** — substance verified 0/8 under both forms,
     but L-38(e)'s "binding predicate untouched" was false of the TEXT; the score-form is the
     binding predicate of record and this clause is its lineage.)*;
   - **Floor guard** — `floor`, not `round`: rounding misses 5 of the 8 bodies by ±1;
   - **G-index guard** — G must read the cell **LABELED 160** (0-based `[159] = 324`); the
     index-inverted read (`[158] = 322`) scores **0/8**, all bodies −0.177 %.

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
`spawnMin +1` on a hero pool is modelled as spawning **zero regulars**. ~~≤1 monster per hero
placement~~ **[CORRIGENDUM L-32/E-4: the struck phrase overstated the edge — read as a TOTAL cap it
contradicts § 10.5 fact 5 (hero placements spawn THREE champions each over 151–170). The edge
governs the REGULAR limb only: `roster_n = 0` ⇒ zero regulars from the `spawnMin` term. The
champion limb rolls per fact 5 — purely additive, no rounding, no clamp — and that branch
reproduces the pinned **63.0 expected champions EXACTLY** (AC-10.4). Fact 5 governs; the sim
implements it.]** The zero-regulars limb remains the plausible engine behaviour, not a measurement.

### 10.5 Count model — U-9, verbatim in structure

```
per spawn point, per wave, Gladiator, solo:

if pool.ignoreGameBalance:                      # 74/632 pools (POP-A axis; Gladiator-slot 74/635, L-40(d));
                                                #   73 boss + 1 trash -- was "ALL boss" (fact 3 strike)
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
3. **`ignoreGameBalance` exempts 74/632 pools** *(census-axis note, L-40(d): 632 = POP-A
   all-difficulty rows; the Gladiator difficulty-slot axis this solo model walks = **635** (POP-B),
   full = 637 (POP-C); numerator **74 invariant** across all three — the adopted E-2 probe § 2.1
   had already published the axis before the L-38 flag)*, and ~~every exempt pool is a boss pool~~. ~~No trash or
   hero pool is ever exempt.~~ *(FALSE BY ONE — L-35 sidecar, DB-CITED: `celestialmonstrosity_t3.dbr`
   is `trash` with `ignoreGameBalance=True`, the sole non-boss exempt pool of the 74. The universal
   was a heuristic that survived until per-pool citation; "boss-pool" is a description of 73/74,
   never a derivation rule — consume the sidecar flags, never the class.)* (All 36 FoA boss pools
   are exempt; only 18 of 96 base-game ones are.)
4. **Champions ADD, they never convert** (Crate, modding guide, verbatim). Census: 515 pools have
   `championChance = 0` and no champion roster; 117 have both; **zero** have a roster with chance 0 —
   so the champion gate is safe to model as a hard gate.
5. **Waves 151–170 hero placements spawn THREE heroes each**, exactly: `championMin' = 1 + 1 + 1 = 3`,
   `championMax'` likewise. `championMinModifier`/`MaxModifier` are unset, so this term is purely
   additive — no rounding, no clamp. Over waves 151–170 that is an expected **63.0 champions against
   292 regulars ≈ 18 %** of the wave population *(292 = pin-era denominator — basis note below)*.
   *(G-I1/L-34: this pairing is the p06-OFF limb — with p06 ON the ~~measured~~ **informative**
   expectation is 81.0 champions / ~~306.83~~ **290.17** regulars (count model of record, T-3/F-10;
   306.83 was the L-34-era branch, superseded with its pin — D2-1 sweep); see AC-10.4 scoping.)*

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

*(Denominator basis — D2-1 sweep annotation: the **292** in fact 5 and the residual above is the
PIN-ERA regulars total, retained by the § 12 T-2 tolerance-on-target ruling — percentages take the
PINNED target as denominator, goalpost fixed at pin time. F-10 superseded that pin; the count model
of record runs **271.50** regulars p06-OFF operative / 290.17 informative-ON (T-3). The 1.9 % spread
and the ≈ 18 % champion share are pin-era arithmetic kept with their pin's lineage, not live model
output; any future re-pin restates both at its own pre-registration point.)*

**U9-6 — ~~RESOLVED: p06 is ON (L-21)~~ → DEMOTED-OPEN (L-33(g)) → RULED OFF for the specified run
(L-37(b), MEASURED-NULL, positive-controlled, veto-open).** p06 is **player-opt-in**
(`survivalevent.lua`: *"final spawn point is for bonus spawns, player chooses to enable this"*;
achievement + `SURVIVALMODE_GLADIATORBONUSSPAWNS` token corroborate), declared on 13 of the 20 waves
151–170 — worth +8.4 % on the pin-era totals (292.0 → 316.5). ~~galadriel's wave-160 body census
measured the state: max-simultaneous **5** distinct hostiles (4 skull-tier + 1 star-tier) at
t = 850.87/852.87 — the 5th body **is** the p06 hero slot~~ *(IDENTIFICATION SUPERSEDED — the third
extraction read the 5th body's nameplate: **"Aleksander's Shard," CHAMPION-tier level-109 Aetherial
SUMMON** (first non-boss icon +5.00 s ± 0.13; first `103,912` readout +4.93 s; icon→body binding
STRONG not MEASURED, her stated honest limit), not a p06 hero. The p06 hero band 450,012–460,431 is
**ZERO across all 5,146 wave-160 readouts** — and the band is not dead instrument: w158's 458,794
one-star hero sits INSIDE it. Residual honestly carried: the census closes engaged on-screen bodies
only.)* The sim runs **p06 = OFF** as the fixture parameter for the specified run, the ON limb
carried informative — both recorded in baton provenance. The rung-2 one-liner to Matt remains
**MOOT** (the ruling is measured, veto-open).

**Design finding, transferable, parked for RDR difficulty design:** `spawnMinModifier` is
**variance suppression, not volume**. Deterministic (width-0) pools go **68 % → 93 %** from Aspirant
to Gladiator. Gladiator escalates by *removing the downside roll*, not by raising the cap — the
player experiences "always the bad case" instead of "sometimes a worse case."

### 10.6 Arena shell — 6 parameterised emitters — provenance TWO-LAYER (L-46(b)): emitter geometry CITED-per-arena, arena selection DECLARED

~~**Arena geometry is mostly NOT DB-resident, and the sim must not go looking for it.** The database
gives structure; it does not give coordinates. `Levels.arc` holds the geometry and **zero**
`.wrl`/`.map`/`.lvl` files exist in the fetch.~~ **SUPERSEDED at the L-46 fold — the geometry WAS
resident; one archive sat outside the read set.** legolas's citation probe decoded Edition-I
`Maps.arc`: **10 Crucible arenas** (`tagSurvivalArena_01..10`, 7,473 placements), per-arena emitter
rings with **ring median 37.53 m** vs **p05 ambush median 10.17 m** (3.7× separation); the build's
uncited 30.0 m sits at the ring distribution's **9.3rd percentile** → **F-12a re-graded
STRUCTURAL**. The database gives structure AND coordinates; what it does not give is **which arena
a sitting ran** (s2 favours `survivalworld_a` — lean, not citation; selection stays DECLARED). The
pre-L-46 field-name sweep (`position|worldpos|coord|spawnloc|location|levelname|mapname` →
UI-bitmap offsets only) was faithful over the four survival archives; the claim died when the read
set widened — the F-10 lesson wearing geometry clothes.

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

**Traversal bounds (L-44(d), measured) — the readout is ENGAGEMENT, not emitter departure.** The
fourth extraction's first-arrival timestamps measure spawn-to-engagement lags of **3.5–6.1 s**
~~across the censused waves — the empirical band that bounds the arena's one free timescale until an
engine m/s citation lands (HALT-2; no such citation exists — see the L-46 closure there)~~ *—
CONDUCTOR STRIKE 2026-08-08 (R-L48-1; JC-1/R-LOCO-7 GRANTED): that band is an **AMBUSH-CLASS**
measurement (p05 plant chain, 10.17 m traversal) and binds ONLY its own emitter class — it is not
a global arena timescale. The ring-class analogue in the same L-44(d) row is the w152/w157 boss
glyph→readout window: **3.0–4.3 s over p04 38.45 m**. Binding the ambush band over the 37.53 m
ring median is a 3.7× radius error. Per-emitter-class binding + the K-1..K-3 `v_ref` bracket live
at § 10.9a D; HALT-2 status unchanged (engine m/s citation NAMED-ABSENT, L-46 closure).* Evidence
anchors ride L-44(d) by reference.

**Emitter positions: provenance TWO-LAYER (L-46(b) — supersedes L-10d's "never DB-hunted").**
Layer 1, **emitter geometry: CITED-per-arena** — the Maps.arc decode makes per-arena ring + ambush
radii database facts, not free parameters. Layer 2, **arena selection: DECLARED** — which of the
10 arenas a sitting ran is not DB-decidable (s2 favours `survivalworld_a`; lean). The sim carries
the selected arena's cited geometry plus one player-spawn parameter; **`v_ref` is the sole free
scalar** (L-46), ~~traversal-bounded 3.5–6.1 s (above)~~ *— R-L48-1: `v_ref` is bracketed per
emitter class at § 10.9a D (K-1..K-3; the 3.5–6.1 s band is ambush-class only)*. This intersects R-KC2-7 cleanly: the sim
owns causal spatial truth on a **cited-geometry, declared-selection** arena, and the baton records
`arena_id` + the geometry provenance it ran with so the Godot session builds the same arena.

**Footage-estimated bearings (L-21, grade ESTIMATED-FOOTAGE ± 15°) — TWO ARENAS, NEVER POOLED.**
galadriel's spawn-direction extraction shows the two sittings ran **different arenas**: s1 arrivals
bear ≈ 3.0 / 5.2 / 6.9 / 9.6 o'clock; s2 wave-151 bears ≈ 9.9 + 2.2, and wave-160's four arrival
bearings read 1.8 / 10.5 / 4.5 / 7.5. **Position parameters are per-sitting sets; calibration bands
load their own sitting's set; the baton pins the arena it ran** (`arena_id` + the six bearings +
player spawn). Pooling bearings across sittings is a spec violation, not a modelling choice.

**Motion hook — how the movement model consumes this geometry (§ 10.9a).** The two-layer ruling
changes what the sim *reads*, so state the read precisely:

- **Per selected `arena_id`, the sim loads SIX radii, not one.** Five ring radii (p01–p04, p06) and
  one ambush radius (p05), from the decoded per-arena placement table
  (`legolas/notes/2026-08-08-kc2-citation-microprobe/kc2_crucible_emitter_geometry.csv`,
  sha256 `ece0c345…`, 332 rows × 15). The build's `Arena.emitter_radius_m = 30.0` is **retired** —
  not re-valued. *One radius cannot describe six emitters whose ring : ambush ratio is 3.7×* is the
  F-12a defect in one line.
- **p01 is keyed PER TIER.** Spawn point 1 is placed per tier, spread up to **17.36 m** within a
  single arena across its 15–17 tier placements; band-A (tiers 1–10) spread runs 0.31–16.39 m by
  arena. The sim reads `p01_tier<NN>` for the tier it is instantiating, never a per-arena p01 mean.
- **The reference frame is the `PatrolPoint_Attack` centroid, not `playerspawnpoint`.** The player
  spawn is the level ENTRY and sits tens of metres outside the arena (arena b: player-spawn Z 26.2
  vs patrol centroid Z 64.7). A sim that anchors on the player spawn imports a level-entry offset
  into every traversal.
- **The convergence destination is a NODE SET, not a point** — 173 `PatrolPoint_Attack` nodes,
  median **18.85 m** from their own centroid (max 30.07). Node assignment per spawn is
  **NAMED-ABSENT**; § 10.9a A declares the assignment rule and the baton records which one ran.
- **Geometry provenance travels with the numbers.** Whatever `arena_id` the sim declares, it
  records the arena's cited radii and their source alongside it, so a later reader can tell a
  *cited* radius from a *declared* selection. The lineage note: `Maps.arc` is **Edition-I**
  (Edition-II ships no `.arc` at all — § 13 hygiene row, widened at L-46(e)); the decode is
  first-of-kind and was **solved, not assumed** (string-table indices valid 16/16 files,
  independent patrol-group cross-check 16/16 counts, 155/173 positions to 3 dp).
- **Reconciliation with the per-sitting rule above.** "Position parameters are per-sitting sets" now
  reads: **the ARENA SELECTION is per-sitting; the positions inside a selected arena are cited.**
  Pooling remains a spec violation — but the thing that must not be pooled is now a choice among
  ten cited geometries rather than a free bearing set.

**MO-5 re-check rides this hook (F-12/C-4).** The § 12 MO-5 sim-side PASS was re-graded
*provisional-on-geometry* at L-43 because it was earned on the uncited 30.0 m radius. The flag
clears only when the floor is re-demonstrated **under the selected arena's cited radii**, and the
direction is not neutral: the cited ring is **~25 % larger** than the retired float, so the
traversal leg lengthens and the floor is pushed **up**, while removing the player-tours-the-board
term pushes total cycle time **down**. The two moves are independent and must be reported
separately — a floor that passes because traversal grew is not the same result as a floor that
passes because the model is right. **If the re-check UNDERSHOOTS the pinned ~7.0 s, that is a
finding against `v_ref` (too fast) or against the arena selection — never a licence to re-pin
MO-5**, whose measured value stands (7.03 / 7.05 / 7.07 s observed).

### 10.7 Wave scaling — the U-8 emission is the HP/damage basis

`legolas/scratch/2026-08-07-u8-tierwave/u8_survival_wave_scaling.csv` — **600 rows
(200 waves × 3 difficulties) × 9 scaling columns**, version-stable pre/post-FoA. The sim joins on 0-based index
`(wave_fought − 1, difficulty)` = the row **LABELED `wave_fought`** (U-8's `wave = index + 1`) — see
the **array-lookup law** below.

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

**⚠ ARRAY-LOOKUP LAW (CORRECTED L-33; supersedes L-29's fought-reads-label-*w−1* ruling): fighting
wave *w* reads 0-based index *w−1* = the cell LABELED *w*** (U-8's `wave = index + 1`; the natural
0-based read — no completed-waves offset exists). Evidence: the § 6.2b four-link chain closes **8/8
wave-160 bodies at ±0 (exact integers, zero free parameters)** with G = `characterLifeModifier[159]
= 324` — the cell **LABELED 160** — while the index-inverted read (`[158] = 322`) scores **0/8,
every body −0.177 %** (microprobe § 3.6). L-29's opposite ruling rested on back-solved M under
HALT-10's five-link chain — **two ~12 % errors cancelling** (base −11.25 % × M +12.67 %; microprobe
§ 9.1): its "noise-shaped ±0.004 %" match was cancellation residue, not closure. Ledger rules
adopted (L-33(c)): **exact-closure evidence (residual-0 × uniqueness-in-scan) OUTRANKS
statistical-shape evidence**; and **verification against a ruled-but-wrong convention propagates the
convention's error** — L-29's "conductor-verified consequences" were derived *through* the false
law. Corrected consequence map, conductor-verified against the full-grain CSV: (a) life while
fighting 160 = **324**; (b) `offensiveTotalDamageModifier` **+43 UNCHANGED** (labels 159 and 160
both carry 43.0 — L-29's strike of the probe's "+43 → +41" claim **STANDS on arithmetic**: no cell
in the family carries 41); (c) fighting 200 reads the labeled-200 cell — life **990**, total-damage
**+130** (L-29's "965 / +125" consequences REVERSE; every label row is read by exactly one fought
wave); (d) **decade walls bind AT their labels** — the 420 cell binds while fighting **171**; (e)
the label-0 boundary **DISSOLVES** — the law is total on fought waves [1, 200] (fighting 1 reads
index 0 = label 1); the L-29 clamp is retired. The true law has no edge case. **One rule for EVERY
array in the `enemies0{1,2,3}` family.** Pre-registered G-D diagnostic unchanged: a damage-side
misfit at exactly-one-cell granularity re-opens this rule. Distinct fact from L-7's
`first_wave_fought = label + 1` start invariant (tier-start labeling — a different table, a
different semantic); both measured, no contradiction.

**Full grain for the remaining wave-varying fields (HALT-9 CLOSED, L-26):**
`legolas/scratch/2026-08-08-kc2-halt-bundle/halt9_survival_wave_scaling_full.csv` (600 × 28 — all
**25** array fields × 3 difficulties; scalars in `halt9_survival_scalars.csv`, 8 × 3; **33** non-zero
fields total, not ~35; all 9 U-8 columns byte-identical). Headline ramps the wave-100 slice hid:
**`offensiveTotalDamageModifier` = +43 % while fighting wave 160** (not +20; robust to the L-33 law
flip — the 43 plateaus across labels 158–160; **+130 while fighting wave 200** per the corrected
law); **`offensivePhysicalModifier` = −21 %** at wave-160 Gladiator (not −15; labels 159/160 agree,
so also flip-robust). The sim joins this CSV on 0-based `(wave_fought − 1, difficulty)` = the row
labeled `wave_fought`, per the corrected array-lookup law, exactly as it does the U-8 nine.

**Wave 171 is a step discontinuity, not a continuation** — Gladiator jumps **+76 pp in one label**
(344 → 420) where labels 161–170 stepped ~+4 pp each. The FoA band is a deliberate wall. Under the
corrected array-lookup law (L-33) the wall **binds while fighting 171** — the fought wave reads its
own label. Relevant to full-ladder runs beyond the fixture bands, which are reported UNBOUND per
charter Phase D.

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
| **p06** | `poolsherogdx1/wendigocannibal_hero`, `championChance 100 %` | 1 of 5, uniform — **fixture state DEMOTED-OPEN (L-33(g)): the L-21 census leg is STRUCK** — the 5th initial-window body is a SUMMON, and the corrected hero band 450,012–460,431 has zero census hits; `u9_bonus_spawn_state` rides the galadriel star-tier follow-up **(→ since RULED OFF — L-37(b) MEASURED-NULL, positive-controlled; F-10 names OFF the operative limb)** | **False (explicit)** → **takes the additives** |

**There is no p05 — no ambush drip in the POOL structure. All pool spawns arrive together.**
*(The camera's t ≈ 862 late cohort (L-30) is NOT a p05 refutation — the DB fact stands; mechanism
**RESOLVED (L-33(f)): summon respawn** — the cohort is Zantarin's summon layer re-casting (Skeletal
Archer ×3, skill13 · Death Revenant, skill6) plus a returning Shard. Summons are a FLOW with
30–75 s TTLs, not pool spawns.)*

**Measured wave-160 census (L-21/L-23/L-29/L-30 — the fixture's own kill wave, instrumented, and
now NAMED on camera):**

- **Seven distinct max-HP fingerprints — census-CLOSED for engaged on-screen bodies** (30 Hz
  full-window pass + parse-failure audit + OCR-noise disproof; NOT closed for the arena —
  unengaged/off-viewport bodies leave no readout). **≥ 11 engaged bodies** across the 25.88 s
  window. The initial-spawn window's max-simultaneous 5 (t = 850.87/852.87) reads as the **4 pool
  spawns + an early summon** (L-33(g) — the p06-ON reading is STRUCK: no corrected-band hero value
  appears anywhere in the census; whether p06 rolled at all is DEMOTED-OPEN *(→ subsequently RULED OFF — L-37(b), L-40 sweep)*,
  since engaged-census closure cannot see an unengaged hero); the death window carries **≥ 6 simultaneous** (twins +
  cohort).
- **The board, named (L-30):**

  | max HP | bodies | identity (nameplate) | rank | displayed lv |
  |---:|--:|---|---|---:|
  | 3,722,896 | **2** | **Archmage Aleksander · Zantarin, the Immortal** — the dedupe twins (73 dual-readout frames, never three) | nemesis | 109 |
  | 2,955,796 | 1 | **Kubacabra, the Endless Menace** (P1 denominator; phases unmanifested) | nemesis | 109 |
  | 2,295,755 | 1 | **Galakros, the Mountain** — p04 MEASURED (violet boss plate; near-empty-bar binding t = 854.30 → death 854.50; the Steward never appears) | boss | 106 |
  | 484,095 | 1 | **Aetherial Bileeater — SUMMON** (L-33(f): ← Galakros skill12, 1 per cast, cap 3) | summon | 112 |
  | 468,504 | 1 | **Death Revenant — SUMMON** (L-33(f): ← Zantarin skill6, 1 per cast, cap 3) | summon | 109 |
  | 103,912 | 2 | **Aleksander's Shard — SUMMON** (← Aleksander skill9, 2 per cast, cap 6) | summon | 109 |
  | 41,237 | 3 | **Skeletal Archer — SUMMON** (L-33(f): ← Zantarin skill13, 2 per cast, cap 12) | summon | 109 |

  *All four small fingerprints are summons (L-33(f)) — every "probable" tag from L-30 resolved by
  DB summon-skill match, eHP EXACT under the § 6.2b chain at each summon's own level.*

- **The L-29 prediction menu RESOLVED (L-30) → F-7 RESOLVED (L-33):** both value-branches
  FALSIFIED — zero hits across 4,401 raw OCR strings (nulls on a dense instrument). The dedupe
  MECHANISM is confirmed-MEASURED, and the F-7 micro-probe LANDED: the twins' 3,722,896 is the
  **nemesis point-value, EXACT under the § 6.2b four-link chain** — no ×1.1-group approximation
  survives (that framing was HALT-10-chain residue). The "hero band 398,747–404,406 vs measured
  484,095/468,504" mismatch **DISSOLVES**: those bodies are SUMMONS (Bileeater ← Galakros skill12 ·
  Death Revenant ← Zantarin skill6), not p06 heroes, and the corrected hero band 450,012–460,431
  has zero census hits (→ the p06 demotion, L-33(g)).
- **Kill ledger CLOSED — three distinct corpses:** +12 (853.2) = **Kubacabra** · +7 (854.5) =
  **Galakros** · +11 (864.5) = **Archmage Aleksander**. The L-29 phase-credit caveat is RESOLVED —
  the counter counted bodies, and the phases could not have manifested: **Kubacabra is single-phase
  DB-CITED** (L-33(h): the `[sm1]` overlay REPLACES the record wholesale — C-9 — and deletes the
  campaign death-spawn phase chain; camera agrees: denominator never moves, bar 9.1 % → vanish, no
  refill anywhere). The fixture died fighting the survivors at 25.88 s in.
- **Fresh cohort t ≈ 862.0** (3× Skeletal Archer + Death Revenant + a returning 103,912) into an
  arena down to ONE monster at 861; the player is dead 2.7 s later. **Mechanism RESOLVED (L-33(f)):
  summon respawn** — Zantarin, the standing survivor, re-casts his summon layer. The DB-side p05
  absence stands; the cohort is HIS, not the wave's.
- **The killing blow is a one-frame burst:** 20,005 → 0 in ≤ 0.100 s (~17,900 in one 1/60 s frame) —
  exceeding every quoted single-hit raw. On a ≥ 6-body death board this reads as
  **multi-hit-same-frame**; the G-5 identification's quantitative face, carried in baton
  provenance. *(Grava'Thul's 6,729-chaos quote stays MOOT — p02 went to Kubacabra.)*
- **Board eHP (L-30/L-33): fight-window engaged total = 13,981,477 — MEASURED and DB-DERIVED
  EXACT** (the § 6.2b chain over the 11 engaged bodies reproduces the camera total to the integer;
  supersedes L-29's ≈ 9.4 M interim). A window total over a **FLOW** — summons carry 30–75 s TTLs
  and respawn by cast, so board eHP is not a stock and never a simultaneity claim. Every TTK /
  narrative-shape judgment about the death wave calibrates against this.

```
bodies:  5 raw   |   8 under full modifier application   (E-3 CLOSED-AGAINST-BOUND, L-35)
         three nemesis slots are EXACTLY ONE EACH regardless (explicit exemption)
```

*[E-3 CLOSED-AGAINST-BOUND (L-35): the E-2 citation probe extracted p04's flag — **both p04 pools
omit `ignoreGameBalance` → template-default False → NOT exempt → takes the additives**. gamora's
honest roll of **8 modified** (3 exempt nemeses + 2 at p04-additive + 3 at p06) was RIGHT; the
spec's ≤ 7 bound was the spec's error and is RETIRED. The probe decided the bound — no
reconciliation was fitted (§ 4.2). Sidecar of record:
`legolas/scratch/2026-08-08-kc2-e2-exemption/pe6_pool_ignoregamebalance.csv` (635 pools, 74
exempt). Caution carried from the probe: "all exempt pools are boss pools" is FALSE by exactly one
(`celestialmonstrosity_t3` — trash, True) — exemption is a per-pool CITED fact, never a class
heuristic.]*

*Census-vs-roll reconciliation (L-30/L-33): the camera's ≥ 11 engaged bodies do NOT contradict the
roll — the roll governs POOL SPAWNS only. The measured board decomposes as **4 pool spawns** (the
nemesis trio + Galakros) **+ 7 summon-layer bodies** (Bileeater ← Galakros · Death Revenant +
3× Skeletal Archer ← Zantarin · 2× Shard ← Aleksander — including the entire t ≈ 862 cohort,
RESOLVED as Zantarin's respawn). The sim's opposition board takes its pool-spawn identities from
the r2 CSV of record under the § 6.2b consumption rule; summons are kit products of the monsters
that cast them, never slot occupants.*

**RULING IN FORCE (L-11): the sim models wave 160 as an all-champion, no-trash burst wave ROLLED
HONESTLY FROM THE POOLS — never a scripted Zantarin reenactment.**

The reasons are worth carrying, because the temptation to script it is real:

- The save banks `greatest-monster-killed[2].last-monster-hitBy = tagNemesis_OrderDeathsVigil01` =
  **Zantarin, the Immortal**, who is in the wave-160 p01 pool at **exactly p = 0.100**. Zantarin's
  kit *is* a precise counter to a channelled melee spin: Curse of Frailty (−30 vitality resist,
  −75 % run speed, 10 m, 6 s), a 12 m death aura, a 2 s-cooldown vitality nova ≤ 2,888, and a
  **passive that retaliates against every incoming hit with a global attack-speed and run-speed
  slow** — the exact anti-pattern for a build whose damage is hits-per-second in contact range.
  **And (L-30) Zantarin is on camera as the standing survivor** — body B of the dedupe twins,
  ≈ 2.1 M HP at the death frame, still on camera at 866.3.
- **The G-5 field contradiction DISSOLVES fully (L-30 camera + L-33(f) mechanism).** The sibling
  save field `last-monster-hit = "Death Revenant"` names a monster in no wave-160 POOL (nearest:
  153, 155) — but the camera shows one at t = 863.2/867.1, and the mechanism is now named: **it is
  Zantarin's summon** (skill6, 1 per cast). Not a pool body at all — the compositional puzzle is
  CLOSED, both save fields are camera- AND DB-consistent, and the attribution tightens: the
  fixture's last recorded hit came from Zantarin's own summon layer. Write-cadence stays
  unverified, and Zantarin's own wave-150 presence is p = 0.311.
- **The co-credible killer set, camera-adjudicated (L-30; summon layer named L-33).**
  **Kubacabra EXITS** — dead at 852.5, 12.3 s before the death; his 3-phase pressure never existed
  (single-phase DB-CITED, § 6.2b). **Archmage Aleksander WAS present** — dedupe twin A at the
  nemesis point-value 3,722,896, which the § 6.2b chain closes EXACT (F-7 RESOLVED; the ×1.1-group
  framing and the t20-assigned 3,389,926 are both HALT-10-chain residue) — **but he predeceases
  the player by ≈ 0.15 s** (+11 at 864.5; death 864.75): meteors-in-flight can contribute, his
  corpse cannot swing. Grava'Thul stays **ELIMINATED** — the p02 slot-argument stands *(and rests
  on the slot alone: the nemesis class is a POINT (C-11/C-12) — his eHP is the same 3,722,896, so
  eHP could never have distinguished him)*.
  **Standing at the death frame: Zantarin (≈ 2.1 M, twin B) + his own summon layer — Death
  Revenant (skill6) · 3× Skeletal Archer (skill13) — plus an orphaned Aleksander's Shard
  (103,912)** — and the one-frame ~17,900 burst reads **multi-hit-same-frame** across that set, so
  the killing blow is plural. The save's `hitBy = Zantarin` is the strongest single attribution,
  is camera-compatible — and the swarm that delivered the plural blow was largely his.

**Both declarations ride in the baton provenance: the G-5 killer-attribution record (both save
fields camera-consistent per L-30; killing blow = multi-hit-same-frame on a ≥ 6-body board), and
the G-2 boss-skill rank ceilings (all monster damage figures are UPPER BOUNDS).**

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

~~The four terms sum.~~ **AMENDED (L-45(e) / L-46(a)): the `+` above is the STATIC-BOARD reading and
does not survive the locomotion amendment.** When monsters travel, later arrivals traverse *while*
earlier arrivals are being killed, so the traversal and kill terms **overlap in time** and the
composition law is closer to `max(last_arrival, cumulative_kill) + tail` than to a sum. **The
composition law is not assumed here — the lap establishes it empirically and reports it** (§ 10.9a
E). Every bound argument built on the additive form — including F-12's own 89/92 lower-bound
argument, which was correct under the static board — must be **re-derived** under the amended
model, never inherited.

A sim that reproduces kill time but not the floor will beat the fixture on every early wave by
construction. **Structural companion:** the clear-time distribution is **bimodal** — waves at
multiples of 10 cost ~2× (**mean 28.57 s, n = 9** vs **14.29 s, n = 83**). Any model fitted against
a pooled mean is fitting a bimodal quantity (§ 12 pins the comparison classes accordingly).

### 10.9a Locomotion — the movement rules — **NEW (F-12 amendment; consumes L-43 C-2/C-3, L-44(d), L-45(d)/(e), L-46(a)–(d))**

> **Why this subsection exists.** F-12 measured the defect precisely: `simulate_wave` hands the disc
> each actor's SPAWN coordinate forever, so the board is static and the player tours it
> (2.5×–5.1× traversal inflation, T-1 FAIL 92/92). §§ 2.2 / 10.6 / 10.9 *described* motion; **no
> section stated the RULES**, which is why the build could omit them and still read as
> spec-conformant. This subsection is the rules. Everything in it is DB-, TPL-, SOURCE- or
> LEVEL-CITED with its record named, or DECLARED with its empirical bound stated. **Zero fitted
> parameters** (charter § 4.2).

#### A — The model

```
per actor a, spawned at wave-clock t_spawn(a) from emitter p(a) in arena A:

  x_a(t_spawn)  := emitter_pos(A, p(a), tier) + scatter_roll        # LEVEL-CITED + SIM-ROLLED
  v(a)          := characterRunSpeed(a) x v_ref                     # DB-CITED x ONE free scalar
  target_a(t)   := player_pos(t)        if pursuit_gate(a, t)
                   patrol_target(a)     otherwise                   # LEVEL-CITED node set
  x_a(t+dt)     := x_a(t) + v(a) * dt * unit( target_a(t) - x_a(t) )   # planar, open-plane
  engaged(a)    := first t with | x_a(t) - player_pos(t) | <= d_engage

  pursuit_gate(a, t) := | x_a(t) - player_pos(t) |  <= ViewDistance(a)          # 80.0 m, 868/895
                    AND | x_a(t) - x_a(t_spawn)  |  <= MaxPursuitDistance(a)    # 125.0 m, 868/895
                    AND   time_in_pursuit(a)        <= PursuitTime(a)           # 10 000 ms

  p05 (ambush) spawns DO NOT patrol-link — `IsAmbush() == false` gates the link
  (survivalevent.lua:552). They enter the gate directly from the ambush radius.
```

**Two limbs, one ruled default, one divergence condition.** The priority between *follow the set
path* and *pursue the acquired target* is **NAMED-ABSENT** — it lives in the executable, and no pin
contains it (the Lua movement surface is exactly `LinkPatrolPointGroup` · `Run()` · `MoveAction` ·
`SetCoords` · `Teleport*`; none takes or returns a rate or a priority). Therefore:

| limb | rule | status |
|---|---|---|
| **L-A — zone-first** *(the ruled default, L-46(a))* | patrol target holds until the actor reaches its assigned node, then the gate governs | **RUN THIS** |
| **L-B — gate-first** | the gate governs from t = 0 whenever it is open (which, in-arena, is always) | run as the declared sensitivity limb |

**They are near-indistinguishable for a centrally-camped player** — `ViewDistance` 80 m exceeds
every measured emitter radius (max 47.89 m) and `MaxPursuitDistance` 125 m exceeds every arena
diagonal, so the gate is open at t = 0 for any in-arena player, and a player standing in the patrol
node cloud *is* the zone. **They diverge when the player is off-centre**, because L-A routes via a
node at median 18.85 m from the centroid before turning. The lap runs L-A, runs L-B as a
sensitivity check, and **reports the delta rather than choosing on taste**. Node assignment
(nearest node vs group centroid vs per-emitter assignment) is **DECLARED** — the baton records
which rule ran.

#### B — Every term, with its citation — **the free-parameter surface is ONE scalar**

| term | value | grade | source of record |
|---|---|---|---|
| ring emitter radius (p01–p04, p06) | per-arena, per-emitter; **median 37.53 m** (n = 322, 15.52–47.89) | **LEVEL-CITED** | `Maps.arc` decode → `kc2_crucible_emitter_geometry.csv` (sha `ece0c345…`) |
| **p01 radius** | keyed **per tier** (`p01_tier<NN>`); band-A tiers 1–10 median 38.51 m; within-arena spread up to 17.36 m | **LEVEL-CITED** | same |
| p05 ambush radius | **median 10.17 m** (n = 10, 1.70–17.15) | **LEVEL-CITED** | same |
| patrol node set | 173 nodes, median **18.85 m** from their own centroid (max 30.07) | **LEVEL-CITED** | `kc2_crucible_patrolpoints.csv` (sha `106facba…`) |
| reference frame | the `PatrolPoint_Attack` centroid — **not** `playerspawnpoint` | **LEVEL-CITED** | probe § 4.3 |
| arena enumeration | 10 arenas `survivalworld_a…j` / `tagSurvivalArena_01…10` | **LEVEL-CITED** | probe § 4.2 |
| **arena selection** | which arena a sitting ran | **DECLARED** over the cited enumeration (s2 leans `survivalworld_a`; a lean, not a citation) | § 10.6 layer 2 |
| scatter | `placementExtents = 8.0` m, all 925 proxies; **SIM-ROLLED** | **DB-CITED** | P-E6 § 2.3 / M-7 |
| **length unit** | the **METRE** | **DB-CITED (Crate annotation)** | `travelSpeed` / `tailTravelSpeed` / `particleSpeed` / `textureSpeed` all declare *meters per second* |
| `characterRunSpeed(a)` | per-record multiplier; band-A **n = 895, median 1.000**, mean 1.0358, range 0.60–2.00 (191 exactly 1.0; 311 below; 393 above) | **DB-CITED** | `kc2_s1_banda_record_inputs.csv` (sha `ac50ef77…`) |
| player run speed | **135 %** — AT `playerRunSpeedCapMax = 135`; monsters carry 3.7× the headroom (`monsterRunSpeedCapMax = 500`) | **DB-CITED** + ceremony § D | `gameengine.dbr` |
| `ViewDistance(a)` | **80.0 m** on 868/895 (min 15.0) | **DB-CITED** | `ControllerMonster` DBR, 126 distinct, 0 missing |
| `MaxPursuitDistance(a)` | **125.0 m** on 868/895 (min 75.0) | **DB-CITED** | same |
| `PursuitTime(a)` | **10 000 ms** (max 12 000) | **DB-CITED** | same |
| `d_engage` | **2.4 m** `meleeTargetDistance` … **4.0 m** `meleeAutoTargetDistance` — the sim declares which, in range | **DB-CITED** | `gameengine.dbr` |
| `disableMovement` | **ABSENT on 895/895** — nothing in band A is exempt from the movement manager | **DB-CITED** | probe § 2.5 |
| collision / occlusion | `OPEN-PLANE — no blocking geometry modelled` | **DECLARED** (unchanged, M-10) | § 11.4 |
| **`v_ref`** | **the SOLE free scalar of the whole locomotion surface** | **DECLARED**, bracketed in D | HALT-2 **CLOSED-BY-TYPE**; L-46 |

**`v_mob` enters DB-CITED ONLY.** There is no global monster speed. Each actor's speed is its own
record's `characterRunSpeed` multiplier times **the same `v_ref`** the player's 135 % resolves
against — one engine reference, two consumers. A sim that carries a single `v_mob` constant has
re-introduced exactly the class of uncited bare float that F-12a caught in `Arena.emitter_radius_m`.
**The radius has EXITED the free-parameter list** (§ 10.6 layer 1); `v_ref` is what remains.

#### C — Declared unmodelled inputs — **NAMED as lap inputs, never silently absorbed**

| input | measured extent | disposition this lap |
|---|---|---|
| **`characterRunSpeedJitter`** | n = 810, **median 15.0**, mean 12.21, max 50.0 (85 band-A records carry none) | **OUT-OF-MODEL, DECLARED.** If it disperses run speed, arrival is a **distribution**, not a time, and a single `v(a)` under-describes it. The lap runs point-speed and **reports the omission by name**; it does not fold a dispersion into `v_ref`. |
| **the `controller` surface** | 126 `ControllerMonster` records × **27 emitted fields**: `RoamBehavior` / `RoamDistance`, patrol-idle timings (1–5 s), `EmoteBeforePursuingChance`, swing pauses | **OUT-OF-MODEL except the three gate fields in B.** Every unmodelled field here adds *latency*, i.e. pushes arrival **later** — a known, signed bias, stated in D. |
| **`walkDistance`** | *"Distance below which to walk when pursuing"*, n = 677, median **4.5 m**; `walkSpeed` median 1.000 | **OUT-OF-MODEL.** Inside 4.5 m the actor walks, not runs; the effect is a sub-second terminal correction against a 33–36 m approach. Named, bounded, not modelled. |
| **`distressCall` / range / time** | emitted per record | **OUT-OF-MODEL** — a pull mechanic that could couple arrivals across actors. |
| patrol-node assignment | 173 nodes; assignment rule not in any pin | **DECLARED** (A above). |
| **F-13 residual on N** | the count model's trash limb is INCOMPLETE (§ 14 F-13) | **DECLARED** — see F below. |

#### D — `v_ref`: the sole free scalar, and the three measurements that box it in

**Nothing here calibrates `v_ref`.** These are consistency bounds computed from cited geometry and
independently measured timings; the lap reports the feasible region, and **an empty region is a
FINDING** (a named model error) — never a licence to widen a bound or solve for a term.

**⚠ First, a provenance correction the lap MUST NOT get wrong.** The **3.5–6.1 s** traversal band
(§ 10.6, L-44(d)) was measured at the **AMBUSH** emitter — it is the per-body residual of the p05
plant chain against its DB cadence (spawns 4.0 / 7.0 / 10.0 s; engagements +10.1 / +12.7 / +13.5 s
⇒ lags **6.1 / 5.7 / 3.5 s**), and p05's median radius is **10.17 m**. **Binding `v_ref` to that
band over the 37.53 m RING is a 3.7× radius mismatch.** The ring-class analogue lives in the same
L-44(d) row and is a different number: the w152 / w157 **boss skull-glyph on the minimap 3.0–4.3 s
before first readout** — a spawn→engagement lag for a body travelling from the boss point
(p04, median 38.45 m).

| # | constraint | arithmetic (traversed = radius − `d_engage`; `t_path ≤ t_lag` because latency ≥ 0) | what it bounds |
|---|---|---|---|
| **K-1** *(ring class)* | boss glyph→readout **3.0–4.3 s** over p04 median **38.45 m** | traversed 34.45–36.05 m ⇒ **closing ≥ 8.01 m/s** (most conservative: 34.45 / 4.3) | **LOWER** bound on closing speed |
| **K-2** *(ambush class)* | p05 chain **3.5–6.1 s** over median **10.17 m** | traversed 6.17–7.77 m ⇒ **closing ≥ 1.01 m/s** | **LOWER**, and weak — likely player-dominated if the plant stream is low-mobility |
| **K-3** *(the floor)* | MO-5 `~7.0 s` one-sided PIN; ring median 37.53 m; `kill ≈ 0` for a trivially-dying wave; AC-10.6 puts p01–p04 at t = 0 so `spawn_resolution = 0` | closing ≤ 33.53 / (7.0 − `advance_tick_latency`) | **UPPER** bound on closing speed |

**The joint consequence, pre-registered.** K-1 ∧ K-3 are simultaneously satisfiable **only if the
declared non-traversal latency budget is ≳ 2.8 s** (33.53 / (7.0 − A) ≥ 8.01 ⇒ A ≥ 2.81 s).
So the amended model makes a falsifiable prediction the lap must check: **either the wave cycle
carries ≈ 3 s of non-traversal latency, or one of the two readings is misattributed** (candidates,
named not chosen: the minimap glyph is not spawn; the readout is not first-contact; the boss uses a
sub-1.0 `characterRunSpeed`; the player was closing and the attribution differs). **Solving the
inequality for `A` and adopting the result is FITTING and is forbidden** (charter § 4.2) — `A` is
declared from evidence or declared as unknown, and the check is then run.

**Closure attribution.** K-1…K-3 all bound *closing* speed, which is `v_ref × (player multiplier +
mob multiplier)` when both parties close and `v_ref × mob multiplier` when the player is stationary.
The lap **declares its player-movement policy** (camp / kite / tour) and converts once, in one
place. For scale: under mutual closure at `characterRunSpeed = 1.0` and player 135 %, K-1's
≥ 8.01 m/s closing reads **`v_ref` ≥ 3.41 m/s**; under a stationary player it reads **≥ 8.01 m/s**.
**That is the whole of F-12's negative control, explained without fitting anything:** the
~ 10 m/s the static-board fit demanded *(digit per D2-2 discipline — cite the finding, not the
numeral, until gamora's 32-seed re-run restates it)* is what you get when a **single** party is
credited with all the closing. The amended model does not need the absurd number — and
demonstrating that it does not is a *result of the lap*, not an input to it.

#### E — Composition law and separability — **RE-ESTABLISHED, never inherited (L-45(e))**

Gate-2 Phase-D2 verified the lower-bound separability that F-12's 89/92 argument rests on **holds
under the static model and INVERTS under this one.** The reason is structural: with a static board,
traversal and kill are sequential per actor and additive over the wave, so locomotion alone is a
lower bound on completion. With actors in motion, **later arrivals traverse while earlier arrivals
are being killed** — the terms overlap, and

```
static  :  clear_time  =  SUM over actors ( traversal_i + kill_i )        -> locomotion is a LOWER bound
amended :  clear_time ~=  MAX( last_arrival , cumulative_kill ) + tail    -> neither term bounds alone
```

**Binding rules for the lap:**

1. The composition law is **measured, then stated** — the lap instruments arrival times and kill
   times separately and reports which term is binding, per wave and per class.
2. **No bound argument is inherited.** Any claim of the form *"term X alone already exceeds
   measured"* must be re-derived under the amended model with its own arithmetic shown.
3. **F-12's 89/92 lower-bound argument is RETIRED as a live argument** and retained as a record of
   the static-board diagnosis. It is not evidence about the amended model.
4. Separability is a **finding to report**, not an assumption to consume: if the lap finds the
   terms are in fact near-additive (e.g. because bodies arrive faster than they can be killed), it
   says so with the measurement that shows it.

**Three channels the amended model predicts will flatten the body-count coupling** — the lap
measures each, and **does not credit the model for a channel it did not demonstrate**:

- **(i) Traversal transfer.** The player stops touring; the 2.5×–5.1× inflation term disappears.
- **(ii) Convergence bunching.** Actors converging on a common destination (zone or player) arrive
  spatially clustered, and a 3.0 m self-centred disc engages a cluster at once — so throughput
  tracks *cluster occupancy*, not N. Note the honest ordering: **pure pursuit (L-B) bunches on a
  point and should bunch MORE than zone-first (L-A), which bunches on an 18.85 m node cloud.** Any
  claim that L-A is "the less body-count-coupled limb" must be measured, not asserted.
- **(iii) Arrival schedule.** p01–p04 fire at t = 0 and p05 staggers from t + 4 s (AC-10.6), so wave
  duration has a geometric floor that is nearly independent of how many bodies ride each emitter.

The fixture's r = +0.154 is the target *shape*; **r is a DIAGNOSTIC, reported, and is not a
goalpost.** T-1 is the only binding clear-time gate and it is UNCHANGED.

#### F — Calibration procedure for the amendment lap

1. **Order.** Build the movement rules (A–C) → re-run the **micro-oracles** (unchanged, direct-binding)
   → re-run the **s1 ramp 1→93** against **UNCHANGED T-1** → run the **s2 second-geometry
   diagnostic** (below) → report. Full-ladder stays out of scope (beat 5 remains paused).
2. **`v_ref` calibration re-enters** — C-2's SUSPENDED-PENDING-LOCOMOTION condition is met by this
   subsection's existence, not by its results. `v_ref` is set **within the K-1…K-3 feasible region**
   and the region is reported; it is **never solved against T-1 residuals.** A `v_ref` that must
   leave the region to pass T-1 is a FINDING and the lap says so with the number.
3. **Calibrate on UNFALSIFIED waves only.** Any wave whose modelled body count is empirically
   falsified is **excluded from the calibration surface and reported as a finding**. Today that set
   is exactly **{w152, w153, w157}** (F-13: the model of record's regular component falsified at its
   own support — 17 > 7 deterministic on w152, 23 > 18 on w153, 15 > 14 on w157). Calibrating a
   body-count-coupled timing model on a falsified N bakes the count error into the timing terms.
   **The three excluded waves are still SIMULATED and still REPORTED** — they are excluded from
   parameter selection, not from the record. *(L-50, fifth extraction: the exclusion set is
   UNCHANGED — 16,368 struck from w153's census as NOT-HOSTILE leaves 22-or-23 > 18, both
   accountings falsify; w152 stands (margin 10); w157's 15 > 14 is margin-1 with bar_hue UNRUN —
   it stays excluded on suspicion. If the commissioned bar_hue cohort pass de-falsifies w157, it
   re-enters calibration only at a future pre-registration point, never mid-lap — standing
   safety #1.)*
4. **The band-A N residual is DECLARED, not assumed away.** Band A (waves 1–93) contains **no
   censused wave**, so no band-A count is *falsified* — and none is *corroborated* either. Band A
   draws from the same count model whose trash limb F-13 graded **INCOMPLETE**, so band-A N may be
   systematically low by the same unresolved mechanism. The lap therefore reports **how sensitive
   its result is to N** (a per-wave N perturbation at the F-13 measured-floor scale is sufficient);
   a result that is insensitive to N is robust to the residual, and one that is sensitive inherits
   it. Do not re-pin counts in-run.
5. **Beat-4 rides INSIDE this lap (L-45(d) / D2-5).** The **s2 one-sided inequality** —
   sim-kit-alone at waves 151–160 must clear **≤** fixture-with-defenses; faster ⇒ anomaly tripwire
   ⇒ finding — runs as a **second-geometry diagnostic**, not as a separate beat. Its value here is
   that s2 ran a **different arena** from s1 (§ 10.6 bearings; s2 leans `survivalworld_a`, s1's best
   fit is `survivalworld_f`), so it exercises the movement rules against a **second cited
   geometry** — a generalisation test the s1 band cannot provide. It stays **INFORMATIVE**
   (R-KC2-2: s2 field outcomes inform, they do not bind) and it **cannot false-trip under a slow
   bias**, which is why it is safe to bundle. **N-exclusions apply here too** — w152 / w153 / w157
   are inside this band; run them, report them, keep them out of parameter selection.
6. **MO-5 re-check** per the § 10.6 motion hook: re-demonstrate the floor under the selected arena's
   **cited** radii, reporting the traversal-lengthening and player-touring-removal effects
   separately. The *provisional-on-geometry* flag clears only on that demonstration.
7. **Zero fitted parameters, restated at the point of temptation.** Every constant is either cited
   in B with its record, or declared in C/D with its bound. The one free scalar is bracketed by
   measurements that are **not** the T-1 target. If the lap ends wanting an eighth term, the term is
   a **HALT row or a finding**, not a slider.

#### G — What the lap must report — and one residual it must not swallow

**Report (per wave, and per two-class summary):** arrival times by emitter · first-engagement times
· the composition law measured (E.1) · clear time vs T-1 (UNCHANGED) · **r(clear time, N)** as a
diagnostic against the fixture's +0.154 · the K-1…K-3 feasible region and where the declared `v_ref`
sits in it · the L-A vs L-B sensitivity delta · the N-sensitivity result (F.4) · MO-5 under cited
radii · the three excluded waves, by name, with their simulated results · every C-row omission
restated as an omission.

**R-LOCO-1 — the baton cannot express a moving board, and this spec will not pretend otherwise.**
§ 2.3's **BR-2 G-1h law** requires that an independent function reconstruct hit/no-hit from the
emitted telegraph alone. Under a static board that was satisfiable from `circle_sweep`
`{centre, radius, tick}` plus each actor's `spawn_x / spawn_y` — because the actor's position was
its spawn position, forever. **Under motion it is not:** hit/no-hit is now a function of two
trajectories and the baton emits only one. **This is a schema gap, named at the moment the
amendment creates it.** It is **NOT resolved in this subsection** — § 11 is a signed cross-seam
contract (star-lord R-1…R-39, drax SIGNED-as-amended), and a spec author does not unilaterally
amend a signed contract. **Routed to the conductor** for star-lord + drax re-sign, with the shape
question stated rather than decided:

- **Option 1 — per-actor path waypoints.** `actors[].path[] { t_s, x, y }` plus
  `config.arena.path_model: "PIECEWISE-LINEAR"` and the interpolation rule. Exact reconstruction if
  motion is piecewise-linear; a handful of nodes per actor (spawn → node → engage), so the cost is
  ~tens of bytes per actor against a measured 17.4 MB artifact.
- **Option 2 — per-tick actor position tracks.** Exact under any motion law, but it multiplies the
  columnar track surface by the live actor count and lands squarely against § 11.6.1's size work.
- **Lean:** Option 1, on cost and on the fact that A's motion law *is* piecewise-linear by
  construction. **The conductor rules; star-lord and drax sign.**

Two smaller schema consequences ride the same routing, both currently **operative-false in a signed
artifact**: `config.arena.arena_id: "s1" | "s2"` names a *sitting*, not an arena, and can no longer
express *which* of the ten cited arenas ran (a sibling `arena_ref` over the cited enumeration plus
the six radii would); and `positions_provenance: "DECLARED"` is now wrong at layer 1 — emitter
positions are **CITED**, selection is **DECLARED** (§ 10.6). The `D-ARENA-DECLARED` declaration
string is corrected below at § 11.4 with strike-lineage, because a **false provenance claim inside a
provenance block** is the one defect this artifact exists to prevent.

### 10.10 Acceptance criteria

1. **AC-10.1** `first_wave_fought == start_wave_label + 1` for every label in `{0, 50, 100, 150, 180}`.
2. **AC-10.2** Instantiating wave *w* selects the `tier<NN>` content band with
   `NN = ceil(w/10)` and a `rewardTier` of `floor(w/10)` — and the two are allowed to differ.
3. **AC-10.3** Wave 160 puts exactly one nemesis on each of p01/p02/p03 across 1,000 rolls, with
   marginal frequencies matching the emitted pool weights within sampling error, and **zero trash**.
4. **AC-10.4** Expected wave totals over waves 151–170 reproduce **292.0 ± 5.5** regulars with p06
   off and **316.5** with p06 on, and **63.0** expected champions **on the p06-OFF limb** *(G-I1
   scoping, L-34: the champion expectation is limb-dependent — measured p06 OFF → 63.00, p06 ON →
   **81.00**; § 10.5 fact 5 always paired 63.0 with the 292-regular OFF limb, so the build's reading
   was defensible; the ON-limb 81.0 is a measured-consistency figure with NO camera pin — the
   fixture's own p06 state is DEMOTED-OPEN per L-33(g), which is why both limbs are carried —
   *tense frozen at L-34 writing; the state has since been RULED OFF (L-37(b), G-D annotation
   below) — D2-1 sweep-extension catch, L-47*)*. *(L-35 annotation: numbers stand
   as written pending a pre-registered G-D re-evaluation under the citation-complete exemption
   sidecar — the probe measures the exemption set at ≈ 20.7 bodies over the band vs the 4.0 these
   totals accounted; both p06 limbs are CARRIED because the fixture's p06 state is DEMOTED-OPEN
   (L-33(g)) *(tense frozen at L-35 — since RULED OFF, L-37(b) below; L-47 sweep-extension
   catch)*; F-9's empty-roster `+1` question may perturb further. Re-evaluation is by citation,
   never by fitting — § 4.2.)* *(G-D RE-EVALUATION EXECUTED + **F-10**, fold 2026-08-08: p06 is now
   **OFF-MEASURED** for the specified run (L-37(b) — hero band 450,012–460,431 ZERO across all
   5,146 wave-160 readouts, positive-controlled by w158's in-band 458,794; **the OFF limb is the
   operative limb**, the ON limb rides informative). Under the citation-complete sidecar + the
   ~~on-camera-confirmed~~ **pre-registered** no-op *(re-graded L-40(b): camera NON-DISCRIMINATING
   at w160 — CORROBORATION NOT AVAILABLE; the no-op stands on the L-35(e) pre-registration)* (F-9
   status / L-37(c)) the model of record returns **271.50** regulars
   p06-OFF (pin 292.0 → **MISS**, Δ −20.50 / 7.02 %) and **290.17** p06-ON (pin 316.5 → **MISS**,
   Δ −26.33 / 8.32 %); champions **63.00 EXACT** (structural: all 28 citation-flipped band pools
   carry `championChance = 0`, so the champion expectation is provably invariant under the
   exemption correction). **Both regular-limb pins are re-graded SUPERSEDED-PROVENANCE per finding
   F-10** — they are faithful evaluations of the roster-blind pin-era model, not measurements of
   the game. The misses stay pinned as named findings in the tests; the **CITED + no-op model is
   the count model of record for the baton**; re-derivation of pins happens only via F-10's
   corroboration path, never by fitting.)* *(F-13 fold, L-47 — second annotation, first
   EMPIRICAL contact: the model of record's per-wave regular components are falsified at support
   on w152 (17 > 7 deterministic) / w153 (23 > 18) / w157 (15 > 14); the band re-grades to a
   RANGE — 248.83 … 271.50 (record, unchanged) … 289.62 (measured floor) … 632–772 (not
   endorsed); the excess is a second low-HP population — the trash limb is INCOMPLETE, not
   WRONG — mechanism UNDECIDABLE among four named-never-fitted candidates. The champion pin's
   "63.0 EXACT" claim is now **empirically corroborated for the first time** (w157 6/6;
   star-furniture ≠ champion count, F-13 § 1.4). No re-pin in-run; the w153 sub-50k decider is
   commissioned; baton `count_model` carries F-13 by name.)* *(F-13 fold, L-50 — third
   annotation, decider (1) EXECUTED: the fifth extraction binds one 37,840 = `Skeletal Archer`
   L105 Undead common (FRACTION-UNIQUE 5/5 frames, Δ = 1.1 px, runner-up 17× out) and strikes
   16,368 as NOT A HOSTILE BODY (green bar 92/93 frames, zero nameplates, fraction-excluded on
   all 22 plate-valid frames). `Skeletal Archer` is ABSENT from every rostered pool on waves
   151–158 (pools CSV, checked at this fold) → the decider's un-rostered branch FIRES:
   summon-or-conjure, with ×4 bodies > CONJURE's +2 — pointing SUMMON; w153's own p03 rosters
   `skeletonrevenant_t3` (Revenant-class undead), the named summoner-candidate — citation probe
   queued. w153's falsification STANDS (22-or-23 > 18 — count-pass and census accountings both
   exceed support); w157's 15 > 14 is SUSPENDED at margin-1 (bar_hue unrun there); w152 STANDS
   (margin 10; the second green entity 20,005 was never in its 17). The 289.62 floor re-grades
   CONTINGENT pending bar_hue-corrected excesses — endpoints 248.83/271.50 untouched. The
   champion w157 6/6 corroboration gains a rank-audit caveat (fifth § 9.2/9.3: `~ Affix` ≠ rank
   signal; stars bind HERO only; glyph-colour re-verification commissioned).)*
5. **AC-10.5** Monster life scaling while fighting wave *w* on Gladiator equals the CSV's 0-based
   `(w−1, gladiator)` row = the row **LABELED *w*** per the § 10.7 corrected array-lookup law — in
   particular **324 while fighting wave 160**: not 322 (index-inversion guard — the L-29 error;
   scores 0/8 on the measured board) and not 168 (F-2 regression guard).
6. **AC-10.6** p05 arrivals are staggered 3 s from t + 4 s; p01–p04 arrive at t = 0; p06 arrives
   only when the bonus toggle is on.
7. **AC-10.7** The minimum achievable cycle time for a trivially-dying wave in the modelled arena is
   ≥ the pinned floor (§ 12), i.e. the floor emerges from spawn + traversal geometry rather than
   being asserted as a constant — **re-demonstrated under the selected arena's CITED radii**
   (§ 10.6 motion hook; the pre-L-46 pass consumed the retired 30.0 m float).
8. **AC-10.8 — the board moves, and the motion is causal.** For any actor whose spawn radius exceeds
   `d_engage`, its position at engagement differs from its spawn position; and a wave exists in which
   an actor takes disc ticks **before** its engage time (motion intersecting the sweep). A build in
   which `position(t) == spawn_position` for all `t` fails this criterion by construction — it is the
   F-12 regression guard.
9. **AC-10.9 — speed is per-record, never global.** Two actors spawned from the same emitter under
   the same target policy with `characterRunSpeed` 2.00 and 1.00 arrive with arrival-time ratio
   1 : 2 within tick quantisation. **No global monster-speed constant exists in the build**: the only
   free locomotion scalar is `v_ref`, and every actor speed is `characterRunSpeed(a) × v_ref`
   (§ 10.9a B).
10. **AC-10.10 — six radii, cited, p01 per tier.** The six emitter radii equal the selected
    `arena_id`'s cited values; p01 resolves per content tier (`p01_tier<NN>`); **the literal 30.0
    appears nowhere in the arena surface** (F-12a regression guard). p05's radius is the arena's
    ambush value, not a ring value.
11. **AC-10.11 — the ambush point is excluded from the patrol link.** p05 actors take no patrol leg
    (`IsAmbush()` gate, `survivalevent.lua:552`) and enter the pursuit gate directly from the ambush
    radius, on the arrival choreography AC-10.6 already pins.
12. **AC-10.12 — the lap's reporting obligations are artifacts, not prose.** The run emits: the
    K-1…K-3 feasible region with the declared `v_ref`'s position in it; `r(clear_time, N)` as a
    **diagnostic** (never a gate); the measured composition law (§ 10.9a E.1); the L-A vs L-B
    sensitivity delta; the N-sensitivity result; and **w152 / w153 / w157 simulated, reported, and
    absent from parameter selection** (F-13).

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
| **deterministic serialization** | `json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n"` (`arena_scenario_emitter`) | **adopted-AS-AMENDED [S7 corrigendum — L-31/CD-1]:** `sort_keys` + `ensure_ascii` + trailing newline stand; **`indent=2` REPLACED by `json_style="rows-compact"` default** (one event-row per line). The literal was inherited from a dict-serialising emitter; on a row-array payload it measures **1.95×** (MID 33.2 MB vs drax's signed ≈ 22 MB budget). `"indent"` stays reachable for human diffing; all styles `json.loads` to the identical object. Two batons from one seed must still diff to nothing — determinism is style-independent |
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
| who hit whom, for how much, at what time | ~~monster approach choreography between spawn and engagement~~ **→ gait, footfall, turn-in-place and micro-spacing WITHIN the sim-emitted approach** *(amended L-46: the approach PATH is causal under a sweeping-area damage predicate — § 2.2. Schema consequence routed, not landed: **R-LOCO-1**, § 10.9a G)* |
| **per-actor HP, carried event-locally on `hp_after`** (§ 11.3.1) | idle/walk/run animation blending, footfall, turn-in-place |
| player HP + energy, as continuous columnar tracks | camera framing, lighting, VFX selection |
| deaths (actor, time, killer — non-null on `player_death`) | crowd micro-spacing inside the declared scatter |
| wave clocks (start, end, outcome, termination reason) | body radius / proxy sizing (the hit test is centre-to-centre — § 11.4 `hit_test_model`) |
| **spawn positions** (the scatter roll is sim-rolled), **engage times**, and — *added L-46* — **every actor's position over time, to hit-test resolution** (§ 10.9a A) | anything not fixed by an emitted field |
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
│                  sim_module_version, seed, rng_algorithm,
│                  tree_state_policy, tree_state_untracked_entries_outside_src }  [R-8, R-9, CD-2]
│                # engine_tree_state ∈ {clean, dirty}; "unknown" sha is a HARD STOP
│                # CD-2 fields (L-42): tree_state_policy — string enum, NULLABLE default null
│                #   (pre-ruling batons load honestly as "policy not recorded"); five values,
│                #   exhaustive by construction: "code-surface-v1" (ruled default: dirty ⟺ any
│                #   tracked modification OR any untracked path under src/) | "any-change-v1" |
│                #   "tracked-only-v1" | "declared-override" (fixture hook, log.warning, never
│                #   selectable) | "unavailable" (git unreachable → forced dirty, never selectable).
│                # tree_state_untracked_entries_outside_src — int ≥ 0, NULLABLE; set only under
│                #   code-surface-v1. ENTRIES not files (porcelain -unormal collapses untracked
│                #   dirs). See F-11 (§ 14): code-surface-v1 grades THIS repo dirty by construction.
├── config
│   ├── fixture   { name: "EoRWarlGuts", build_of_record: "b28gD0KN",
│   │               eor_rank_total: 26, identity_grade: "MEASURED",
│   │               identity_envelope: "+3.9%/-0.5%" }
│   ├── encounter { difficulty: "gladiator", start_wave_label, first_wave_fought,
│   │               lives: 1,
│   │               fixture_p06_state: false,    # RULED-OFF (L-37(b) MEASURED-NULL; F-10)  [M-1]
│   │               #   -- was `true # MEASURED ON (L-21)`: pin-era claim; the L-40(e) value-set
│   │               #      sweep missed this SPELLING (owned L-43 — sweep sets must enumerate all
│   │               #      historical spellings). TYPE GAP (gamora beat-3 flag → star-lord rider):
│   │               #      bool + `_ac_11_4g`'s RESOLVED/UNKNOWN mapping cannot express RULED-OFF;
│   │               #      schema extension queued, not landed here.
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
│                   positions_provenance: "DECLARED",   # ⚠ OPERATIVE-FALSE post-L-46 — layer-1
│                                       #   positions are CITED-per-arena, selection is DECLARED.
│                                       #   Value + the arena_id/radii/path shape route via
│                                       #   R-LOCO-1 (§ 10.9a G) for star-lord + drax re-sign;
│                                       #   NOT changed here — § 11 is a signed contract.
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
│                   t_start_s, t_end_s, tick_start, tick_end,   # tick span INCLUSIVE (L-31/CD-6) [R-19]
│                   outcome, outcome_enum_version: 1,                                    [M-15]
│                   termination_reason, termination_enum_version: 1,                     [R-20]
│                   life_modifier_pct,        # 324 while FIGHTING 160 (§ 10.7 corrected law: reads the cell LABELED 160) — F-2 + L-33 index guards
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
    onto the frame so nobody reads a declared bearing as a measured one. *(L-46 annotation: the
    non-pooling rule is unchanged, but what is per-sitting is now the **arena SELECTION** over a
    cited 10-member enumeration — the positions inside a selected arena are **CITED**, and the
    radial coordinate the parameter list never had is now a level fact. The field that expresses
    which arena ran, and the six radii that come with it, are **R-LOCO-1** — routed for re-sign,
    not landed here.)*
12. **`config.encounter.bonus_spawn_p06` splits [M-1], and the fixture side is ~~MEASURED~~
    RULED-OFF.** `fixture_p06_state: false` records the L-37(b) ruling — MEASURED-NULL (hero band
    zero across 5,146 readouts, positive-controlled; F-10 OFF-operative). ~~`fixture_p06_state:
    true` records the L-21 census result (max-simultaneous **5** hostiles at t = 850.87 — the 5th
    body *is* the p06 hero slot; the 4-body branch excluded on two independent instruments)~~
    *— struck at the D2-1 sweep: the 5th-body leg was itself STRUCK at L-33(g), and L-37(b)
    superseded the ON reading; this item was asserting the struck state as live.* `run_p06_enabled`
    is mandatory and non-null — the run is not unknown to itself — and at the § 10.8 showcase the
    OFF ruling is operative: **4 raw start bodies, not 5**; a run electing p06 ON departs from the
    fixture state and this field pair says so.

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
  u9_bonus_spawn_state:        RULED-OFF     # L-37(b): MEASURED-NULL — hero band 450,012-460,431 ZERO
                                             #   across all 5,146 wave-160 readouts, positive-controlled
                                             #   (w158 in-band 458,794); F-10 names OFF operative, ON
                                             #   informative -- was DEMOTED-OPEN (L-33(g)) -- was RESOLVED (L-21)
  u9_bonus_spawn_branch_pct:   RETIRED   # the +-8.4% branch is DEAD, not carried as a tolerance
  drain_unit:                  PER_TICK  # PINNED L-22; enum frozen, hook retained -- was drain_fork
  drain_rate_per_s:            176.4     # @ 196% AS, client-verbatim = 16.0 x 12.25 x 0.90
  soulfire_cost_term:          DECLARED-SEPARATE   # never folded into drain_rate_per_s (§ 3.1)
  halt_register:                         # L-26 bundle outcome, carried so the artifact is auditable
    closed:          [HALT-1, HALT-3, HALT-5, HALT-6, HALT-8, HALT-9, HALT-10]
                                         # HALT-10 closed EXACT (L-33, § 6.2b four-link chain):
                                         #   8/8 wave-160 bodies at +-0 integer, zero free params;
                                         #   p04 gap DISSOLVED (T-8 RETIRED); F-7 RESOLVED;
                                         #   eHP source-of-record = r2 CSV (§ 6.2b consumption rule)
    partial:         [HALT-4]            # HALT-4: ORDER-1 FAVOURED, not proven
    closed_by_type:  [HALT-2]            # v_ref is a DECLARED free parameter (bundle § 6.1);
                                         #   post-L-46 it is the SOLE free scalar of the locomotion
                                         #   surface -- radius is CITED, v_mob is DB-CITED per
                                         #   record. Bracketed two-sided at § 10.9a D.
    unfired:         [HALT-7]            # pre-registered G-D contingency
    open:            []
  open_halt_effect:  []                  # was HALT-10 -- closed EXACT L-33; residue rides declarations
  arena_pin:
    arena_id:        <s1 | s2>           # names the SITTING, not the arena -- post-L-46 this can no
                                         #   longer express WHICH of the 10 cited arenas ran.
                                         #   Sibling arena_ref (survivalworld_a..j) + the six cited
                                         #   radii route via R-LOCO-1 (§ 10.9a G). Not added here.
    geometry_layer:  CITED-PER-ARENA (emitter radii) / DECLARED (arena selection)   # L-46 two-layer
    bearings_grade:  ESTIMATED-FOOTAGE +-15 deg (L-21)
    pooling_rule:    per-sitting sets, NEVER pooled -- pooling is a spec violation (§ 10.6)
                     # post-L-46 reading: the SELECTION is per-sitting; positions inside a selected
                     # arena are cited. The non-pooling rule is unchanged.
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
    - { id: G-5,  text: "wave-160 save fields RECONCILED (L-30/L-33): 'Death Revenant' = Zantarin's
                         summon (skill6), camera- AND DB-consistent; hitBy 'Zantarin' is the
                         strongest single attribution on a plural killing blow. Wave 160 is rolled
                         honestly from the pools, NOT a scripted Zantarin reenactment." }
    - { id: G-2,  text: "ALL monster damage figures are UPPER BOUNDS. Boss-skill rank binding unread." }
    - { id: LV-OFFSET-3, text: "monster level L = levelVarianceEquation(apl) + 3 -- the +3 is
                         MEASURED (8/8 closure + nameplates) but its DB residence is NAMED-ABSENT:
                         a DECLARED input, riding the galadriel multi-wave nameplate follow-up." }
    - { id: SUMMON-FLOW, text: "board eHP is a FLOW, not a stock: 7 of 11 engaged wave-160 bodies
                         are summons (TTL 30-75 s, respawn by cast). The sim's opposition board =
                         pool spawns + summon layer as kit products; window totals are not
                         simultaneity claims. eHP chain CLOSED EXACT 8/8 (L-33, § 6.2b)." }
    - { id: G-4,  text: "p05 concurrency model is the safe reading (pool count staggered 3 s from
                         t+4 s); the t+4.0 s start anchor is MEASURED x3 (L-21)." }
    - { id: G-7,  text: "4 dangling roster refs of ~7,000 dropped, weights renormalised." }
    # ~~{ id: D-ARENA-DECLARED, text: "arena emitter positions are DECLARED free parameters,
    #                                  footage-estimable, never DB-hunted (L-10d)." }~~
    #   STRUCK at the L-46 fold: OPERATIVE-FALSE. The positions WERE DB-hunted, in Edition-I
    #   `Maps.arc`, and they are cited. A false claim inside a provenance block is the one defect
    #   this artifact exists to prevent, so the text is corrected here rather than left standing.
    #   AC-11.4b set-compares against this register => star-lord re-sync required (R-LOCO-1).
    - { id: D-ARENA-CITED,       text: "arena emitter geometry is CITED per arena (Maps.arc decode,
                                        10-member enumeration, ring median 37.53 m / p05 ambush
                                        10.17 m); ARENA SELECTION is DECLARED (L-46 two-layer)." }
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

> **MEASURED AT PHASE C — SUPERSEDES THE 9–12 MB RECOMPOSITION (S-I2, Gate-2 INFO; L-34).** The
> built emitter's `rows-compact` MID emission measures **17.4 MB**. The DERIVED 9–12 MB figure
> under-called by ~1.6× and is retired for planning purposes — **plan against 17.4 MB.** Still
> inside drax's declared ≈ 22 MB budget and far inside his ~100 MB split threshold, so the
> signature holds unchanged; Discipline #10 honoured twice over (the estimate was labeled DERIVED,
> the measurement now governs).

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
| **O-1** | **gzip [S4]** — measured **~10×** (7.84 → 1.67 MB). Godot reads standard gzip via `PackedByteArray.decompress_dynamic(…, FileAccess.COMPRESSION_GZIP)`, but that is a change **inside drax's loader**, and there is no gzip / NDJSON / streaming-write machinery anywhere in `export/` or `telemetry/` at HEAD — adopting it is a **new capability**. | **drax** | **OPEN-ROUTED — deliberately NOT resolved here.** drax's sign budgets ≈ 22 MB uncompressed and asks for no split, which is adjacent evidence but is **not** an answer to the yes/no. If the answer is no, § 11.6.1's measured **17.4 MB** stands (S-I2 — the derived ~9–12 MB is superseded), inside the signed ≈ 22 MB budget. |
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
| **AC-11.4c** | Every `out_of_model[]` entry is `{id, text}`; the ID set equals the register; no entry duplicates a `config.encounter` field. *(Reading ratified L-31/CD-4: "duplicates" = value-carriage — where an OOM id names something `config.encounter` also types, the typed field MUST carry the value and the OOM row carries only the reason; both present is the required state, and the check fails if the typed field is missing.)* |
| **AC-11.4d** | A baton with a **truthful `PARTIAL`** grade passes; a baton with a missing declaration does **not**. |
| **AC-11.4e** | `engine_tree_state == "dirty"` ⇒ `calibration_grade != FULL`, enforced at the write boundary [R-8]. |
| **AC-11.4f** | `engine_version_sha == "unknown"` ⇒ **hard stop**; no baton is written. |
| **AC-11.4g** | `provenance.u9_bonus_spawn_state` agrees with `config.encounter.fixture_p06_state` — asserted at the write boundary [R-38]. |
| **AC-11.4h** | `devotion_envelope_disclosure` is the § 9.5 block **verbatim and complete** (AC-9.2), un-restructured. *(L-31/CD-5: the block's leading register-key line IS the wire key, not part of the value; every content line byte-identical, indentation preserved.)* |
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
| M-1 | split `bonus_spawn_p06` | `config.encounter.fixture_p06_state` **+** `run_p06_enabled` | **ADOPTED** — fixture side ~~`true`, MEASURED (L-21)~~ **`false`, RULED-OFF (L-37(b) MEASURED-NULL; F-10)** *(D2-1 sweep)* |
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
| **T-2** | count model — intra-order + rounding + clamp | **1.9 %** (5.5 monsters on 292, waves 151–170) *(C-2 ruling, G-D fold: the percentage takes the **PINNED TARGET** as denominator — tolerance-on-target, goalpost fixed at pin time; re-deriving the band from the model's own output each lap would let the goalpost track the model, the drift this table exists to prevent. Margins of record at the G-D re-evaluation: ±5.55 on 292.0 / ±6.01 on 316.5 — both regular limbs MISS under either denominator reading, so the ruling moves margins, never verdicts. With F-10 the 292-anchored band is superseded together with its pin; any future re-pin restates T-2 against the newly pinned value at its own pre-registration point.)* | wave-total counts | declared residual |
| **T-3** | count model — **U9-6 bonus spawn** | ~~RESOLVED: p06 = ON, measured (L-21 census)~~ **RULED OFF — L-37(b) MEASURED-NULL** (hero band zero across 5,146 readouts, positive-controlled; F-10 OFF-operative) | ~~counts run the p06-on table~~ counts run the **p06-OFF model of record 271.50 / 63.00** (ON informative 290.17 / 81.00) | **closed** — closure cites **L-37(b)**, never L-21 *(row re-annotated at the L-40 sweep — this was the D-W3 stale sibling)* *(F-13, L-47: the OFF-limb REGULAR figure 271.50 is CONTESTED-with-band — falsified below at ≥ 289.62 (measured floor); carried as a **floor with a named finding** per the F-10 pattern, NOT re-pinned in-run. Champion **63.00 untouched** — unfalsified on all five discriminating waves, EXACT at w157 (6/6); star-furniture ≠ champion count. The p06-state closure THIS row records is unaffected.)* *(L-50: decider (1) executed — 16,368 NOT-HOSTILE struck from w153's census; w153 falsification STANDS (22-or-23 > 18), w152 STANDS, w157 SUSPENDED margin-1 (bar_hue unrun); floor 289.62 → CONTINGENT pending corrected excesses, endpoints 248.83/271.50 untouched; champion 63.00 unmoved — its w157 6/6 corroboration carries a glyph rank-audit caveat (fifth § 9.2).)* |
| **T-4** | energy drain rate | **PINNED: PER_TICK, 176.4 / s @ 196 % AS** (client-verbatim, L-22) | drain rate now BINDS alongside ceiling/reserve; Soulfire term declared-separate (§ 3.1) | **closed** — fork collapsed |
| **T-5** | devotion envelope | error-bar **classes**, not a scalar: defensive-trigger (opposition-dependent) · dual-bound (Shifting Sands ~200×) · piloting-parameter | envelope disclosure | structural (L-3) |
| **T-6** | monster damage | **upper bounds only** (G-2 rank binding unread) | INFORMATIVE rows only | declared ceiling |
| **T-7** | fixture identity | **+3.9 % / −0.5 %** | every derived player stat | declared envelope |
| **T-8** | opposition eHP chain (§ 6.2b) | **RETIRED — L-33 ledgered ruling** (the pin note permits change only as a ledgered ruling; this is one). The corrected **four-link** chain closes **8/8 wave-160 bodies at ± 0 — exact integers, zero free parameters** — a tolerance band on exact closure is meaningless, so the row retires in favour of **AC-6.5's exact-equality + three structural guards**. ~~± 0.05 % nemesis / p04 ± 5 % band~~ — the p04 "named gap" was the missing armorbase term (**Galakros EXACT**), and the ± 0.05 % re-confirmation was two ~12 % errors cancelling (§ 10.7 / microprobe § 9.1) | every opposition-eHP consumer (AC-6.5); source-of-record = **r2 CSV** under the § 6.2b consumption rule | **RETIRED (L-33)** |

**Micro-oracle rows (BINDING per R-KC2-2 — direct-binding, calibrate FIRST):**

| Oracle | Target | Tolerance |
|---|---|---|
| **MO-1** energy usable ceiling | **1594 / 2576** | `PIN` — exact-integer expected |
| **MO-2** energy reservation | **982 — exact-integer** (BINDING-and-derived; bundle § 3.3 ledger, L-26) | `PIN` — derived from DB, not hard-coded |
| **MO-3** s2 in-combat energy | **1477 / 2576** | `PIN` |
| **MO-4** HP orb / max health | **20,005** | `PIN` — two independent instruments agree (sheet + in-combat orb) |
| **MO-5** cycle floor | **~7.0 s** (7.03 / 7.05 / 7.07 observed) | `PIN` as a **floor**, one-sided — *beat-3 sim-side PASS re-graded **provisional-on-geometry** (L-43, F-12/C-4): the PASS consumed the uncited 30.0 m radius (F-12a); the measured pin itself stands* *(L-46 annotation, ledgered-ruling consequence: the re-check is now **specifiable** — re-demonstrate under the selected arena's **CITED** radii per the § 10.6 motion hook; the flag clears on that demonstration and on nothing else. Second role acquired: this floor is the **UPPER** bound on closing speed in the § 10.9a D bracket (K-3), so it now constrains `v_ref` from the opposite side to the measured traversal lags — an undershoot is a finding against `v_ref` or the arena selection, **never a re-pin**.)* |

**Ordering for G-D (charter Phase D):** micro-oracles (direct-binding) → s1 ramp 1→93 through the
envelope (BINDING) → s2 one-sided inequality (INFORMATIVE tripwire: sim kit-alone at 151–160 must
clear **≤** fixture-with-defenses; **faster ⇒ anomaly tripwire → finding**) → full-ladder runs beyond
the fixture bands (reported, unbound).

*(Ordering annotation — ledgered ruling **L-45(d) / D2-5**, not an edit to a pinned row. At the
locomotion amendment lap the **s2 one-sided inequality runs INSIDE the lap**, not as a separate
beat: it is the model's **second-geometry diagnostic** (s2 ran a different arena from s1 — § 10.6
bearings), it stays **INFORMATIVE**, and it **cannot false-trip under a slow bias**, which is what
makes the bundling safe. Procedure: § 10.9a F.5, including the F-13 N-exclusions that fall inside
this band. **Full-ladder runs stay PAUSED** (beat 5) until the lap lands against **UNCHANGED T-1**.)*

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
| **HALT-2** | Player base movement rate (m/s); `delayMovement` magnitude | **CLOSED-BY-TYPE** — `characterRunSpeed = 0.92` is a *dimensionless multiplier* (1,467-record census: median/mode 1.0); engine m/s reference **NAMED-ABSENT**; `delayMovement` is `bool`, no magnitude exists. **Adopted disposition: declared free parameter `v_ref`** (bundle § 6.1 recommendation), ~~calibrated at D against traversal times~~ *— C-2 annotation (L-43): calibration **SUSPENDED-PENDING-LOCOMOTION**; beat-3 broke its precondition (static board ⇒ kill term ≈ 0 ⇒ calibrating v_ref = fitting the wrong mechanism; F-12 negative control: fitted v_ref ≈ 10.5 m/s = 2.63× the declared class buys only the mean, 75/92 still fail). `v_ref` stays DECLARED; calibration re-enters after the locomotion lap. Degeneracy: time ∝ radius/v_ref — (radius, v_ref) is ONE free timescale; an engine m/s citation (Lua lane, L-9) collapses it*; fixture is AT the run-speed cap (135 = `playerRunSpeedCapMax`) *(L-46 closure: the m/s hunt is CLOSED NAMED-ABSENT-CONFIRMED, census-complete — 260 Lua files / 97,907 lines with zero speed call; 18,999 template Variables, no base run speed; `gameengine.dbr` caps are percentages. The METRE is engine-declared — four template fields say meters/second — and the degeneracy half-collapses the measured way round: RADIUS becomes CITED-per-arena (`Maps.arc` decode, § 10.6 two-layer ruling), leaving **v_ref the sole free scalar**, ~~traversal-bounded 3.5–6.1 s (L-44(d))~~ *— R-L48-1 strike: that band is AMBUSH-CLASS (p05, 10.17 m); ring-class analogue 3.0–4.3 s @ p04 38.45 m (same L-44(d) row); per-emitter-class binding + the K-1..K-3 bracket at § 10.9a D*. Unmodelled surfaces registered as lap inputs: `characterRunSpeedJitter` (median 15.0, n = 810) · per-record `controller` surface (126 × 27).)* |
| **HALT-3** | P(crit) from OA vs DA | **CLOSED** — `records/game/combatformulas.dbr` **was in the base archive**: `probabilityToHitEquation` verbatim; crit = **PTH-band** mechanic (6 thresholds → ×1.0…×1.5, `pthMinimum = 55`). Band *semantics* INFERRED → gamora proves by test (§ 4.2) |
| **HALT-4** | Damage application order | **PARTIAL — ORDER-1 (convert-then-modify) FAVOURED** (1.26× vs 1.84× residual), not proven: 3.2 % signal under ~20 % un-enumerated devotion/component remainder. Weapon term **CONFIRMED** (solved w = 0.671 vs DB 0.64, +4.8 %); **crit proven EXCLUDED** from the sheet window; missing `× (1 + cunning/245)` = ×5.98 supplied by `physicalDamageEquation`. Spec declares ORDER-1; **residual enumeration = G-D contingency alongside HALT-7** |
| **HALT-5** | ≈ 358 unattributed reservation | **CLOSED-EXACT — 982 = 982** (§ 3.2 ledger; Presence of Might 300; Divine Mandate reserves 0; `characterManaLimitReserveModifier` dead corpus-wide) |
| **HALT-6** | Monster→player mitigation model | **CLOSED** — two-branch armour equation, `armorDefensiveAbsorption = 70.0`, per-hit **body-region sampling** (7 regions, weights Σ100), `playerDefenseCap = [80,80,80]`. Monster damage rows stay INFORMATIVE per R-KC2-2 |
| **HALT-7** | Boss-skill rank binding per wave | **UNFIRED — pre-registered G-D contingency, unchanged** |
| **HALT-8** | Soulfire `projectilePeriod` unit | **CLOSED** — Crate's own annotation *"Delay between projectile launches (seconds)."* **0.2 = plain seconds, no ×0.8.** Now also the **Soulfire cost-interval basis** (§ 3.1, L-22) |
| **HALT-9** | Wave-dependence of non-emitted fields | **CLOSED** — full 600 × 28 grain emitted (§ 10.7); 33 non-zero fields (25 arrays / 8 scalars); 9 U-8 columns byte-identical; `offensiveTotalDamageModifier` +43 @160 / +130 @200; `offensivePhysicalModifier` −21 @160 Glad. **F-4 adjudicated as a side effect** (§ 14) |
| **HALT-10** | **Opposition eHP composition beyond the wave-scaling array** | **CLOSED (nemesis class) / PARTIAL (p04) — L-29.** Five-link chain extracted DB-cited (§ 6.2b): apl → `levelVarianceEquation` spawn level → **per-record `charLevel` re-evaluation** (four forms; `lv8_boss+` is a POINT = 106) → five bio `characterLife` curves → **ADDITIVE M = 1 + 5.80 (Ultimate `characterLifeModifier[8]`) + G/100 (§ 10.7 array, lookup law) + own/100**. Lands F1 = 3,722,896 (−0.004 %) and F2 = Kubacabra P1 2,955,749 (+0.002 %); the L-17 interim ≈1,308,800 and P-E6's 827 k are **SUPERSEDED**. **Residue: p04 −4.3 % named gap** (Galakros favoured; nine explanations ruled out by reading) → declared **± 5 % band, INFORMATIVE-side** (T-8). Probe note `legolas/notes/2026-08-08-kc2-ehp-composition-probe.md`; sim consumes `t20_wave160_board_ehp.csv` (glad_cell = 322 rows). See **F-6 (RESOLVED)** · **L-30 postscript:** board NAMED on camera (§ 10.8) — dedupe twins = **Zantarin + Archmage Aleksander**, both at the `×1.1` figure (−0.004 %); **p04 bearer NAMED = Galakros, MEASURED**; Kubacabra phase chain **FALSIFIED on camera** (sim models P1 only); **F-7 FIRED** — the t20 record→form assignments are falsified while the chain stands; t20 consumed **mechanism-correct / values-pending** until the **F-7 revision lands for calibration** (pre-G-D) · **L-33 POSTSCRIPT — CLOSED EXACT; everything before this postscript is RECORD, not law:** the five-link chain was wrong in two links (**per-record `charLevel` re-evaluation STRUCK** — manual-placement scope only; 118.6 was a degeneracy artifact, the bio-curve ratio spans 0.018 % over L ∈ [106, 150] · **own-`characterLifeModifier` STRUCK** — breaks closure +4.41 % on Bileeater) and missing one (**armorbase — REVERSED IN**); the corrected **four-link** chain (§ 6.2b) closes **8/8 at ± 0** under the corrected lookup law (G = the cell LABELED 160 = **324**, not 322); p04 gap DISSOLVED (Galakros EXACT) · T-8 RETIRED · F-7 RESOLVED · source-of-record = **r2 CSV**. The ± 0.004 % this row records was **two ~12 % errors cancelling** (base −11.25 % × M +12.67 % — § 9.1 diagnostic: *a residual that survives on one body but not on others is a term, not a mystery*) |

**Declared-not-HALT** (unknown but carrying a *declared* disposition rather than a hole):
~~emitter world positions (DECLARED free parameters, per-sitting sets, § 10.6)~~ **STRUCK at the
L-46 fold — emitter geometry is CITED-per-arena (`Maps.arc` decode, § 10.6 layer 1); what remains
declared is the ARENA SELECTION over a cited 10-member enumeration, and the single player-spawn
parameter** · mutator identities
(OUT-OF-MODEL, **six** glyphs confirmed, 25-pool prior, § 10.3) · `maxGroupSize` concurrency
semantics (safe model, start anchor measured, § 10.6) · Shifting Sands host delegation (DUAL-BOUND,
§ 9.4) · `v_ref` movement reference (free parameter by bundle § 6.1 disposition — *L-46: now the
**SOLE** free scalar of the locomotion surface, bracketed two-sided by measurement at § 10.9a D;
`v_mob` is DB-CITED per record and is **not** a member of this list*) · `characterRunSpeedJitter`
and the 126 × 27 `controller` surface (**OUT-OF-MODEL, DECLARED as lap inputs**, § 10.9a C) ·
Soulfire
cost-term effective magnitude (declared-separate, fixture-sustain-bounded, § 3.1). *(Former members
CLOSED and struck: energy-drain unit → PINNED L-22; U9-6 → ~~measured ON L-21~~ **RULED OFF
L-37(b)** — closure cites L-37(b), never L-21 (T-3's own rule; D2-1 sweep).)*

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

> **FOLDED — L-30 (board closure):** the question returned and the board is NAMED (§ 10.8): seven
> fingerprints, ≥ 11 engaged bodies, fight-window eHP **13,981,477 MEASURED**; p04 = **Galakros,
> MEASURED**; the L-29 prediction menu resolved **against both value-branches** ⇒ the residue
> graduated into **F-7 (GROUP-ASSIGNMENT)** below. F-6 itself stays RESOLVED — the chain the probe
> extracted survived the camera at −0.004 % on two named bodies.

> **L-33 POSTSCRIPT (final):** the composition term is now closed EXACT, and the L-29 chain above
> is RECORD, not law — two of its five links were wrong (per-record `charLevel` re-evaluation: the
> ×1.62 spread it "explained" is really the **summon layer** + per-class armorbase variation ·
> own-modifier term) and one was missing (**armorbase**). The corrected four-link chain closes
> **8/8 bodies at ± 0** (§ 6.2b). The *"fighting 160 reads label-159's 322"* join quoted above is
> the L-29 lookup-law error — corrected at L-33 to the cell LABELED 160 (**324**), § 10.7. Its
> −0.004 % was two ~12 % errors cancelling (microprobe § 9.1). *(L-40 sweep extension: the quote's
> "overshoots ×2.9 and fails AC-6.5" is the same-era **mixed-chain artifact** — multiplicative
> WITHOUT armorbase against additive at the superseded G = 322 (C-1 restatement, § 6.2b guard
> lineage); the guard of record is AC-6.5's **0/8 score**, ×5.746 all-three-term. The quote stays
> as RECORD.)*

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

### F-7 — The eHP chain is camera-exact but the record→form map is falsified (group assignment)

> **RULED — L-30 (board closure; targeted legolas micro-probe FIRED, Phase-C-concurrent, lands
> before G-D binds):** the five-link chain (§ 6.2b) is **camera-exact** — the `×1.1`-group figure
> 3,723,043 landed at measured 3,722,896 = **−0.004 %** on TWO named bodies (Zantarin + Archmage
> Aleksander, the dedupe twins) — but the t20 CSV's **record→form assignments are FALSIFIED** for
> at least those two (t20-assigned ×1 → 3,176,863 and ×1+5 → 3,389,926 respectively; zero hits
> across 4,401 OCR strings) and the p06 hero band (398,747–404,406) is falsified vs measured
> **484,095 / 468,504**. Mechanism right; map wrong. gamora's build consumes t20
> **mechanism-correct / values-pending**; **calibration (G-D) consumes the revised CSV** — emission
> pins it as the eHP source-of-record.

> **RESOLVED — L-33 (micro-probe return:
> `legolas/notes/2026-08-08-kc2-groupassign-microprobe.md`):** the map is corrected by CITATION,
> not fitting — and most of its falsified degrees of freedom **dissolve** rather than re-assign.
> The nemesis class is a **POINT** (every rollable nemesis reads **3,722,896** — C-11/C-12), so
> "which ×-group form" was never a real degree of freedom; the "hero band" bodies are **SUMMONS**
> (Bileeater ← Galakros skill12 · Death Revenant ← Zantarin skill6), so the hero-record audit
> target dissolves — and the corrected hero band **450,012–460,431 has zero census hits** → p06
> **DEMOTED-OPEN** (L-33(g)) *(→ since RULED OFF — L-37(b)/L-40 sweep)*; Kubacabra's phase wiring is answered — **single-phase DB-CITED**
> (`[sm1]` whole-record overlay deletes the death-spawn chain, C-9); the nameplate displayed level
> **is the real spawn level** (`L = levelVarianceEquation(apl) + 3`; modelled 118.6 was a
> degeneracy artifact). Source-of-record: **r2 CSV** (`t21_wave160_board_ehp_r2.csv`, § 6.2b
> consumption rule — exclude `nemesis_beast_01_p{2,3}*`, whose verdict column is class-mislabeled).
> Every consumer below now reads r2; the pre-registered fallback never fired.

The L-29(g) prediction menu resolved against BOTH pre-registered value-branches (zero hits across
4,401 raw OCR strings — nulls on a dense instrument) while confirming the dedupe MECHANISM (73
dual-readout frames, never three). The camera then named the twins as the two monsters the menu had
predicted absent — both measuring the `×1.1`-group value. One finding, two faces: the CHAIN is now
the strongest-verified object in the opposition model, and the per-record FORM assignments feeding
it are wrong for at least two of sixteen nemeses plus the hero class. *(Naming caution: fingerprint
indices F1–F7 in galadriel's tables are unhyphenated; run findings F-1..F-7 are hyphenated.)*

- **Micro-probe scope (citation, never fitting — charter § 4.2):** pool-slot DBR enumeration for
  the wave-160 slots · exact-carrier search — which records' `charLevel` forms evaluate to the
  measured values · hero-record audit vs 484,095 / 468,504 · Kubacabra phase wiring (why P2/P3
  never manifested) · the nameplate displayed-level field (106/109/112 vs modelled 118.6) ·
  **revised `t20_wave160_board_ehp.csv`** into the same scratch dir.
- **Consumers:** § 6.2b (assignment column) · § 10.8 board table · gamora opposition stack (values
  bind at G-D) · baton provenance (assignment grade).
- **Also carried (L-30):** Kubacabra models single-body P1 = 2,955,796 MEASURED, phases
  declared-unmanifested · kill ledger CLOSED (+12/+7/+11 = three distinct corpses) · fresh-cohort
  t ≈ 862 mechanism OPEN · displayed level ≠ modelled `charLevel`, both recorded, neither forced.
- **Fallback (§ 4.2-compliant, pre-registered):** if the micro-probe cannot close the map by
  citation before G-D, the affected rows carry **named residuals with bands** (the chain's
  −0.004 % accuracy is unaffected; only identity labels degrade) and the baton's assignment grade
  says so.

### F-8 — ~~Soulfire's separate cost is OVER-CONSTRAINED~~ → RETIRED: the premise was a spec-authoring fusion; Soulfire declares NO cost

> **REGISTERED — L-32 (gamora fold, E-5):** the § 3.1 magnitude tension is now a NUMBER. The
> admissibility bound `S ≤ 100·u − 176.4 + 75.37·(1−d)/d` (u = leech uptime ≤ 1, d = channel duty
> cycle) is **negative at every d ≥ 0.5**: −1.03/s at d = 0.5 · −57.56/s at d = 0.8 · −76.40/s at
> d = 1.0. Against the naive max-rank read (20 per 0.2 s interval = 100/s) there is NO positive
> Soulfire cost the fixture's own sustain can admit — the naive read is INADMISSIBLE, not merely
> unmeasured.

> **RETIRED — L-35 (E-2 rider return): PREMISE WITHDRAWN.** `eyeofreckoning2.dbr` (Soulfire)
> declares **no `skillManaCost` field at all** — the 3–20 cost array belongs to **Disintegration**
> (`aetherray2.dbr`), and the fusion of the two happened at spec authoring (§ 3.1 — a SPEC-AUTHOR
> error, owned at L-35; P-E1 itself was clean and cited Disintegration as a *control*). There is no
> Soulfire cost to adjudicate: gamora's `effective_per_s = 0.0` graduates **UNADJUDICATED →
> DB-CITED** — the record's silence IS the citation (474/476 `SkillSecondary_*` records omit the
> field). The admissibility bound above survives as a derived consistency check — a zero cost
> trivially satisfies it; the "over-constrained" tension dissolves with the premise. The **×0.90
> cost-reduction hunt stays open on the DRAIN side only.** Bonus coherence: `eyeofreckoning1` (the
> channel itself) carries `skillManaCost` len = 26, range [4..16] — rank 26 = **16.0**, the drain
> constant's home: 16.0 × 12.25 × 0.90 = **176.4/s**, closing the loop with L-22's client-verbatim
> tooltip.

- **Sim disposition (ratified):** `effective_per_s = 0.0`, grade **UNADJUDICATED**, the bound
  exposed as a function; never folded into `drain_rate_per_s`. AC-3.2's FINDING clause is the
  destination, exactly as § 3.1 pre-registered.
- **Resolution path (citation, never calibration):** DB re-read of `eyeofreckoning2.dbr`'s cost
  line + its template fine-print — is the 3–20 a per-interval INCREMENT or a total? does the cost
  gate on projectile launches or damage intervals? The same unit-decomposition discipline that
  closed the 176.4 drain (P-E1 → L-22). **Rider on the E-2 exemption probe.**
- **What this is NOT:** a licence to tune. A fitted Soulfire cost that makes sustain work is the
  free-parameter pattern charter § 4.2 forbids; the term stays 0.0-UNADJUDICATED until a record
  citation moves it. *(L-35: the citation arrived — the record declares no cost; 0.0 is now
  DB-CITED, and the resolution path above is CLOSED as written: the DB re-read happened and
  answered "neither — the field does not exist on this record.")*

### F-9 — 117 of 635 wave pools carry EMPTY regular rosters while the non-exempt `+1` additive expects a regular draw — engine behavior NAMED-ABSENT

> **REGISTERED — L-35 (E-2 unasked rider):** the exemption sidecar shows **117/635 pools have zero
> regular-roster entries** (champion/boss-only structures), while the non-exempt additive path
> grants `spawnMax +1` / `spawnMin +1` to the REGULAR draw. A `+1` against an empty roster either
> conjures a body from nothing, silently no-ops, or promotes into the champion draw — **the
> engine's resolution is NAMED-ABSENT** (no field or template fine-print in the read set
> adjudicates it). Band effect if the `+1` lands: **≈ 27.0 expected bodies over waves 151–170** —
> the dominant structural unknown in the AC-10.4 G-D count re-evaluation (larger than the ≈ 20.7
> exemption-set correction and far larger than the 4.0 originally accounted).

- **Sim disposition (pre-registered, § 4.2):** the sim implements **no-op on empty roster** — a
  draw from an empty set yields nothing — and DECLARES it in the baton count-model provenance.
  The alternative branches (conjure-from-template · promote-to-champion-draw) are NAMED, never
  fitted.
- **Resolution path (citation or footage, never calibration):** template fine-print for the
  `proxypool` spawner family; and/or a galadriel count-instrument pass on a boss-only s2 wave —
  the fixture's own 151–160 band contains empty-regular-roster waves, so existing footage may
  already decide whether any un-rostered trash body appears.
- **Consumers:** § 10.5 count model · AC-10.4 (annotated) · gamora wave instantiation (G-D wiring
  re-lap) · baton `count_model` provenance.
- **Status at the G-D fold (2026-08-08):** the footage limb of the resolution path **FIRED** —
  galadriel's third extraction (L-37(c)): the wave-160 start cohort is **4 skulls, ZERO stars
  through +4.75 s**, and no un-rostered trash body appears (the r2 census closes 8/8 camera-named
  bodies with multiplicities); w151–159 ALL show stars at matched offsets (w159 control: 4 skulls
  + 2 stars), so the property is w160's, not the detector's. ~~**No-op-on-empty
  CONFIRMED-ON-CAMERA** for the engaged window.~~ **RE-GRADED at Gate-2 Phase-D (adopted L-40(b)):
  NOT DISCRIMINATED ON CAMERA.** w160's only non-exempt empty-regular-roster alternative sits at
  spawn point 6, so under the operative p06-OFF limb all three branch hypotheses (NO_OP / CONJURE /
  PROMOTE) predict the SAME w160 cohort — likelihood ratio zero; under p06-ON the check is
  circular. The discriminating waves are **151 / 152 / 153 / 157 / 158** — inside the extracted s2
  footage and UNREAD at re-grade time; deterministic separation (weight-1 picks, integer): CONJURE
  predicts **+2 / +3 / +2 / +2 / +2** extra un-rostered bodies vs NO_OP **+0**, with **w152 (+3)
  decisive** — galadriel fourth extraction commissioned (L-40(c)). The no-op disposition stands on
  the **L-35(e) pre-registration** (declared before any camera claim was available). The
  `proxypool` template fine-print limb stays open as citation-grade corroboration (legolas r3
  rider). The un-adopted `+1` branch is measured as a parameter in the build: band effect
  **+21.00 / +27.00** over 151–170 — the registered ≈ 27.0 reproduced exactly. See **F-10** for
  what that reproduction turned out to mean.
- **Status at the F-13 fold (2026-08-08, L-47): CONTESTED — disposition UNCHANGED, un-adopted.**
  The discriminating waves are now READ (fourth extraction, L-44) and ADJUDICATED (F-13, L-47):
  **the count leg REJECTS the CONJURE magnitude and shape** (predicted +2/+3/+2/+2/+2 vs measured
  overshoot +0/+10/+5/+1/+0; adding the `+1` still leaves w152 at 17 > 10 and w153 at 23 > 20);
  **the identity leg produces exactly ONE un-rostered body consistent with CONJURE at a predicted
  point** (`Ugdenbog Crabling`, w152 +3.40 s — common rank, swampcrab family, bracketed inside
  0.8 s by the `swampcrab_hero` pool's own champions; that pool is non-exempt with
  `roster_n = 0`). The two legs disagree, and the un-rostered class is **known non-unique in
  mechanism** — `Aleksander's Shard` (w160) is equally un-rostered and graded SUMMON. The no-op
  stands on the L-35(e) pre-registration, **now with a named contradiction on the record**;
  adopting the `+1` because a crabling appeared would fit one free parameter to a residual that
  is demonstrably not that parameter's shape (charter § 4.2 — the exact move F-10 caught the
  pin-era model making). The count excess is a LARGER finding than F-9 (+18-to-+45 bodies over
  three waves vs F-9's ±21 over the band) and is owned by **F-13**, not resolved into this one;
  the `proxypool` fine-print limb (legolas r3 rider) remains the citation path, joined by the
  **w153 sub-50k identity decider** (commissioned at L-47) and the **Crabling fingerprint
  binding** (F-13 § 5). *(L-50: both deciders resolved — w153: one 37,840 = `Skeletal Archer`
  L105, UN-ROSTERED across 151–158 → summon-or-conjure branch, ×4 > CONJURE's +2 points SUMMON
  (Revenant summoner-candidates rostered at w153 p03; citation probe queued); 16,368
  NOT-HOSTILE, struck. Crabling: CLOSED-UNBINDABLE — plate saturated FULL on all 4 hover
  frames, ≥ 5 parsed bodies ≥ 0.988; the low band neither confirmed nor excluded. F-9's no-op
  disposition UNCHANGED.)*

### F-10 — AC-10.4's regular-count pins were computed by the roster-blind pin-era model — pins re-graded SUPERSEDED-PROVENANCE; the CITED + no-op model is the count model of record

> **REGISTERED — G-D fold 2026-08-08 (conductor adjudication of gamora CONFLICT C-3, ledger L-38;
> veto-open).** The G-D re-evaluation made both regular limbs of AC-10.4 MISS (271.50 vs 292.0;
> 290.17 vs 316.5) while F-9's un-adopted `+1`-on-empty branch lands Δ +0.50 / +0.67 **INSIDE T-2
> on both limbs**. Two readings existed (gamora § 12.1, correctly not discriminated in-seam):
> **(i)** the pins were computed with the `+1` landing on empty rosters, or **(ii)** two ≈ 20-body
> corrections coincidentally cancelling. **RULED (i) — by construction — on ~~three~~ two independent
> legs** *(leg count as MODIFIED at Gate-2 Phase-D, adopted L-40(b): the empirical leg is REJECTED
> AS GRADED → CORROBORATION NOT AVAILABLE; the disposition additionally rests on the L-35(e)
> pre-registration)*:
>
> - **Documentary** *(as MODIFIED at Gate-2 Phase-D, adopted L-40(b))*. § 10.5's published model
>   draws `regulars = randint(n_min, n_max)` with **no roster term** — primary evidence is
>   **U-9 § 4.3: "Applying A/floor with clamp across all 558 non-exempt pools"** (558 = 632 − 74:
>   the pin-era evaluator walked EVERY non-exempt pool, roster-blind, empty included). ~~the only
>   roster-awareness at pin time was the U9-8 hero-pool edge~~ *(STRUCK — arithmetically false:
>   edge-APPLIED evaluation gives 280.50 / 301.17, not the pins; the edge covers only 95/117 empty
>   pools, leaving DEVOTION 15 + BOUNTY 7 uncovered, 47 in-band: HERO 26 / DEV 15 / BOUNTY 6)*. A
>   **§ 10.4 ↔ § 10.5 pin-time inconsistency is REGISTERED on the re-pin clause** — the two
>   sections' models differ at pin time; any future re-pin must resolve which walked. The
>   empty-roster class (117 pools) was discovered at L-35 (E-2 sidecar), AFTER the pins were
>   published; F-9's registration framing (the ≈ 27.0 as a correction the G-D re-evaluation *would
>   confront*) is downgraded **CORROBORATIVE** — language-reading, never load-bearing. A
>   roster-blind evaluator grants the `+1` to empty-roster pools because it cannot see that they
>   are empty: for the non-exempt empty class, **the pin-era model IS the `+1` branch.**
> - **Arithmetic — unique fit on the config lattice** *(as MODIFIED at Gate-2 Phase-D, adopted
>   L-40(b): unique on the 6-cell lattice AS DRAWN; the 12-cell edge-extension lands TWO cells —
>   the rival "6-override + hero-only edge" cell (+3.83 / +1.33 residual) also lands sub-residual
>   but is NOT live: it fails per-limb miss-tracking (+9.00 / +11.00 vs misses 5.17 / 9.67). The
>   load-bearing sub-criterion is **per-limb tracking + historical availability**, not bare
>   landing)*. Of the exemption × empty-disposition configurations {none, 6-override, cited} ×
>   {no-op, +1}, **only cited/+1 lands at the pins** (292.50 / 317.17 vs 292.0 / 316.5), jointly,
>   on both limbs — residual **+0.50 / +0.67, STRUCTURED not noise** (mixture quanta ½ and ½+⅙;
>   POP-A/POP-B axis ruled out — 0/7 differing pools in band; `legendary_override` False on all
>   265 band rows; carried OPEN, never absorbed into a "sub-0.25 %" gloss) — and the correction
>   tracks the miss **per limb** (OFF: band +21.00 vs miss 20.50; ON: +27.00 vs 26.33).
>   Independent corrections would have to cancel twice at different magnitudes; the ON-limb band
>   effect reproduces F-9's registered ≈ 27.0 **exactly**. Shared computational origin is the only
>   parsimonious reading: the pin-era evaluator carried § 10.5's exemption branch (fact 3's
>   74-pool set) but no roster join.
> - ~~**Empirical.** The game itself no-ops — CONFIRMED-ON-CAMERA (L-37(c), F-9 status above).~~
>   **REJECTED AS GRADED at Gate-2 Phase-D (adopted L-40(b)) → CORROBORATION NOT AVAILABLE.**
>   w160 carries no non-exempt empty-regular-roster alternative off spawn point 6, so under the
>   operative p06-OFF limb every branch hypothesis predicts the same w160 cohort (likelihood ratio
>   zero); under p06-ON the check is circular. The camera is SILENT here, not confirming — the
>   discriminating waves (151/152/153/157/158, w152 decisive at +3) ride the galadriel fourth
>   extraction (L-40(c)). The no-op stands on the **L-35(e) pre-registration**, declared before
>   any camera claim; a model "corrected" toward the pins by adopting the `+1` would still be the
>   free-parameter fit charter § 4.2 forbids.

- **Disposition.** AC-10.4's 292.0 / 316.5 are **SUPERSEDED-PROVENANCE** — faithful evaluations of
  the pin-era roster-blind model, not measurements of the game. The **CITED + no-op** model is the
  count model of record: p06-OFF (operative, L-37(b)) **271.50 regulars / 63.00 champions**
  expected over 151–170; p06-ON informative 290.17 / 81.00. The champion pin **63.0 survives
  EXACT** (structurally invariant — all 28 citation-flipped pools carry `championChance = 0`). The
  misses stay pinned AS misses in named tests; the `+1` branch stays an un-adopted parameter
  (`empty_roster_plus_one`), never a fit. This is the Run-A Gate-B event class: a pre-registered
  criterion FAILED, was diagnosed to its provenance, and is reclassified as a published finding
  under independent Gate-2 review — the run continues.
- **What would re-open this** *(WIDENED at Gate-2 Phase-D, adopted L-40(b))*: **either** the
  `proxypool` template fine-print (legolas r3 rider) reading that an empty-roster `+1` conjures or
  promotes, **or** the galadriel fourth-extraction count pass on the discriminating waves
  (w151/152/153/157/158) finding un-rostered extra bodies — the camera is currently SILENT on the
  no-op (empirical leg above), so footage evidence would be **first contact, not contradiction**.
  Either goes to the conductor loudly (the branch is a parameter; the tests name both worlds).
  Absent that, re-derived pins may be registered at a future pre-registration point from the model
  of record — never retro-fitted inside this run.
- **Count-pass leg — FIRED and adjudicated (F-13 fold, L-47).** The fourth-extraction count pass
  (first contact, L-44) + the F-13 identity-join: **the model of record stands UNCHANGED and is
  now CONTESTED-with-band** — its regular limb is falsified at its own support on w152 (17 > 7,
  deterministic zero-width) / w153 (23 > 18) / w157 (15 > 14), while the HP decomposition lands
  the above-gap plains EXACTLY on the model's support on both hard-falsifying waves (7 and 18):
  the trash limb is **INCOMPLETE, not WRONG** — a second low-HP population the model does not
  represent. Band 151–170 becomes a **RANGE**: 248.83 (`boss_add=OFF`) … **271.50 (record)** …
  **289.62 (measured floor, assumption-free — carried as a FLOOR; the point estimate is
  refused)** … 632–772 (lattice survivors, NOT endorsed). Champions **63.00 unmoved and now
  empirically corroborated** (w157 6/6 EXACT; star-furniture ≠ champion count per F-13 § 1.4).
  No re-pin fires in-run (standing safety #1); the un-adopted parameter list extends to **four
  named-never-fitted mechanisms** (`trash_pool_multiplicity` · `p05_replenishment` ·
  `boss_spawn_additive` · `summoned_bodies`) alongside `empty_roster_plus_one`; baton
  `count_model` provenance carries F-13 + the falsification table + the floor by name. Full
  adjudication: **F-13**. *(L-50 — decider (1) executed, fifth extraction: 16,368 struck
  NOT-HOSTILE. A second green entity, 20,005, matches MO-4's pinned player max health EXACTLY —
  the green class contains the player's own readout; 16,368's profile (pixel-static box, never
  damaged, persists across badge flips) plus the save regime's +4 purchased defenses name
  Crucible defense structures as the candidate class — adjudication queued, not ruled. The
  falsification triple survives as w152 STANDS · w153 STANDS (22-or-23 > 18) · w157 SUSPENDED
  margin-1 pending the commissioned bar_hue cohort pass (w151/157/158 + w152 re-pass; eye-read
  mandatory on green-lit scenes); M1's PLAIN falsification survives on w152+w153 alone. Floor
  289.62 CONTINGENT. New instruments registered: plate-bar fraction binding (± 2.5 px on a
  199.8 px track; ceiling f ≈ 0.985) + bar-hue classifier. Identity outcome: `Skeletal Archer`
  L105 UN-ROSTERED corpus-wide → summon-or-conjure fires, SUMMON indicated (×4 > +2);
  summoner-candidate `skeletonrevenant_t3` rostered at w153 p03; the mechanism-adjudication
  piece is QUEUED at the bar_hue fold.)*
- **One census-count note for Gate-2:** § 10.5 fact 3 says 74/**632** pools; the sidecar registry
  counts 74/**635** (F-9's own text uses 635). The 632-vs-635 denominator delta is unresolved in
  this spec — a one-line verification item, not material to any count above.
- **Consumers:** AC-10.4 (annotated) · § 12 T-2 (annotated) · baton `count_model` provenance
  (carries F-10 + the superseded pins by name) · jack-ryan Gate-2 (reclassification review per
  desirable-pattern standing safety #2).

### F-11 — `code-surface-v1` grades this repo dirty by construction (tree-state policy; star-lord Phase-D, folded L-42)

- **Status:** OPEN — policy fork to Matt at the Phase-E touch (R-KC2-5 agenda); `code-surface-v1`
  STANDS until ruled.
- **Finding.** The ruled policy (dirty ⟺ any tracked modification OR any untracked path under
  `src/`) implemented literally grades THIS repo dirty in perpetuity: the engine's runtime artifact
  directory IS `src/reincarnated/output/`. Star-lord measured 2,403 untracked entries with 2,393
  (99.6 %) under output/; the conductor's independent reproduction minutes later read **2,414 /
  2,404 / 10** — the +11 delta was gamora's beat-3 writing new run artifacts into
  `src/reincarnated/output/` BETWEEN the two measurements: **the mechanism confirmed itself live.**
  ENTRIES not files (porcelain `-unormal` collapses wholly-untracked dirs).
- **Phase-E consequence.** Baton emits `engine_tree_state: dirty` → AC-11.4e forbids `FULL`. Under
  the current policy an honest emitter cannot grade this repo's baton FULL even with every tracked
  file committed.
- **The 10 non-output entries** (conductor enumeration, evidence-by-reference to L-42): 1 export
  delta note, 2 generation notes, 2 simulation math notes, 2 simulation scripts, 1 telemetry
  backup, 2 telemetry-seed WAL/shm files. All notes/artifacts, zero code.
- **Options (fork):** **(a)** `code-surface-v2` = `src/` minus `src/**/output/` — conductor lean:
  the artifact dir is the sim's own exhaust; excluding it makes the policy measure the code surface
  its name claims. **(b)** keep v1, emit non-FULL honestly. **(c)** demand a clean tree at emit —
  fragile: the sim dirties its own tree by running.
- **Consumers:** CD-2 fields (§ 11.4, landed) · AC-11.4e · Phase-E emit gate · Matt touch.

### F-12 — Locomotion: the sim's board is static; the fixture's is not (T-1 BINDING FAIL 92/92; gamora beat-3, folded L-43 — Run-A Gate-B event class)

- **Status:** OPEN — citation probe RETURNED + FOLDED (L-46: lap precondition MET); the locomotion
  model amendment lands via the named-gandalf spec-amendment piece (commissioned at the L-47
  fold), then the gamora lap; **beats 4–5 PAUSED** (beat-4 re-scoped at L-45(d)/D2-5 — bundled
  into the lap as a second-geometry diagnostic); **T-1 UNCHANGED** (standing safety #1 — the run
  cannot move its own goalposts). **Lap N-inputs EXCLUDE w152/153/157** (F-13: falsified-count
  waves — calibrating a body-count-coupled timing model on a falsified N would bake the count
  error into `v_mob`/radius); the lap calibrates on unfalsified waves and reports the excluded
  three as findings.
- **Headline.** First full s1 calibration (ramp 1→93): **T-1 (± 1.0 s, two-class, tick-quantised)
  FAILS 92/92.** ×10 class mean 28.57 s measured vs 34.04 s sim; non-×10 **14.29 vs 39.37**; class
  ratio **INVERTED** (measured ×10/non-×10 = 2.00×, sim 0.86×); 0 waves in band; mean abs error
  +23.16 s.
- **Correlation fingerprint.** Sim clear time is a function of body count (r = +0.737 vs N); the
  fixture's is NOT (r = +0.154). That is not a constant missing — it is a **mechanism** missing.
- **Mechanism.** `simulate_wave` hands the disc each actor's SPAWN coordinate forever: static
  board, player tours it, 2.5×–5.1× traversal inflation. Spec §§ 2.2 / 10.6 / 10.9 describe
  monsters APPROACHING the player. **Spec-described, build-omitted.**
- **Lower-bound argument (why no eHP fix rescues this).** `engagement_kill_time ≥ 0` ⇒ the current
  locomotion cycle is a lower bound on any completion time. On **89/92 waves the lower bound ALONE
  already exceeds measured + 1.0 s.** Survivors: waves 80/90/92 ~~(few-bodies/high-HP,
  kill-term-dominated)~~ *(gloss RESTATED per D2-3, adopted L-47: "few-bodies" is false of two of
  the three — w80 carries E[bodies] 25.00 = 1.75× its own class mean 14.28, w92 carries 27.33 =
  1.35× of 20.23; only w90 (2.00) is few-bodies. "High-HP" is unmeasurable for band A — eHP absent
  for 889/896 band-A records by § C.1's own census. What the evidence DOES support, and it is
  enough: the three survivors are the fixture's 1st, 2nd and 4th SLOWEST measured waves, and the
  absent kill term is the only modelled term whose sign could lengthen the sim on them. Set
  membership, the 89/3 split, and the arithmetic are EXACT — only the causal gloss was
  unsupported.)*.
- **Negative control (refusal-to-fit as measurement).** Fitting `v_ref` to the residual demands
  ≈ 10.5 m/s — 2.63× the declared reference class, with the fixture already AT the run-speed cap
  (135 = `playerRunSpeedCapMax`) — and buys only the mean: **75/92 still fail**, correlation stays
  +0.757, inversion stays 0.84×. The residual is not a speed. Charter § 4.2 forbids the fit and
  the fit would not even work. *(D2-2 annotation, adopted L-47: this bullet's digit-set does NOT
  co-reproduce at any single `n_seeds` — 75/92 occurs only at n = 1, +0.757 sits at n ≈ 8–16,
  0.84× occurs nowhere in the grid; the parameterisation was undeclared. The CONCLUSION is
  grid-robust — corr stays ≥ 0.70 against measured +0.154, ratio stays < 1.0 against measured
  2.00×, 74–81/92 fail everywhere: "a scale parameter cannot repair a structure error" stands.
  Digits restate from gamora's 32-seed re-run at the locomotion lap; until then cite D2-2, not
  these numerals.)*
- **Dispositions (conductor, L-43; Gate-2 Phase-D2 review commissioned per standing safety #2):**
  - **T-1 UNCHANGED** — preregistration holds; a gate FAIL is a processable finding, not a
    goalpost-move license.
  - **C-1 ADOPT** — legolas band-A per-record eHP emission (896 records; 7 exist; ehp-composition
    t0–t21 precedent) so the kill term composes per-record INPUTS, not summaries.
  - **C-2 ADOPT** — `v_ref` calibration SUSPENDED-PENDING-LOCOMOTION (§ 13 HALT-2 annotated): at
    kill term ≈ 0, calibration is fitting the wrong mechanism.
  - **C-3 ADOPT (core)** — locomotion amendment: ~~monsters path to the player~~ **AMENDED L-46(a)
    — `path-to-zone` THEN `pursuit-gate`** (`PatrolPoint_Attack`, `survivalevent.lua:552`, 17/17
    tier modules; pursuit is a separate gated controller behaviour). Model of record + movement
    rules now live at **§ 10.9a**; `v_mob` enters ONLY
    DB-CITED (per-record `characterRunSpeed` multipliers × the SAME engine reference as `v_ref`,
    per HALT-2's census). **Degeneracy:** time ∝ radius / v_ref ⇒ (radius, v_ref) collapse to ONE
    free timescale; ~~an engine m/s citation from the Lua lane (legolas, L-9/U-8) collapses the
    whole free-parameter surface by citation~~ — *RESOLVED the OTHER way (L-46): the m/s hunt
    returned **NAMED-ABSENT-CONFIRMED** (census-complete) while the **RADIUS** became
    LEVEL-CITED, so the degeneracy half-collapsed on the geometry side and **`v_ref` is the sole
    survivor**, bracketed two-sided by measurement at § 10.9a D.*
  - **C-4 ADOPT, two limbs** — build: ARENA_S1 completes to 6 emitters per § 10.6 (measured
    bearings where measured — ≈ 3.0/5.2/6.9/9.6 o'clock — declared where not; p05 ambush + p06
    bonus points join per their measured/ruled states). Spec-side: **F-12a** below. MO-5 sim-side
    PASS re-graded provisional-on-geometry (§ 12 annotated); the measured ~7.0 s pin stands.
  - **C-5 PARKED-REGISTERED** — ± 1.0 s vs single-draw process sd ≈ 3.21 s is a legitimate
    tolerance-FORM question that may NOT move this run's goalposts; re-enters only at a future
    pre-registration point (F-10 re-pin pattern). Matt surface.
- **F-12a (spec-side OWN, conductor).** § 10.6's parameter list (:1089) enumerates arena_id + six
  bearings + player spawn — **NO radial coordinate**; `Arena.emitter_radius_m = 30.0` entered the
  build as an uncited bare float. The radius joins the declared-parameter list with a provenance
  ladder (footage-estimable; DB/template hunt riding the legolas geometry probe). A spec that
  omits a load-bearing free parameter from its own declared list has under-declared its freedom —
  same class as the § 10.4 ↔ § 10.5 inconsistency registered at F-10. *(Hunt LANDED — L-46: it
  returned CITATION, not absence. Per-arena ring + ambush radii are `Maps.arc` facts (ring median
  37.53 m / ambush 10.17 m); the uncited 30.0 sits at the ring distribution's 9.3rd percentile →
  re-graded **STRUCTURAL** — the bare float was not merely undeclared, it was ~20 % low against
  the plausible arena set. The radius EXITS the free-parameter list: CITED-per-arena under the
  § 10.6 two-layer ruling; arena selection remains the declared freedom.)*
- **Beats 4–5 PAUSED.** s2 + full-ladder against a known 2.5×–5.1× traversal inflation produce
  structurally-known-wrong numbers. Un-pause condition: locomotion lap lands AND s1 re-runs
  against UNCHANGED T-1.
- **Consumers:** § 12 T-1 · § 13 HALT-2 (annotated) · § 10.6 (F-12a) · gamora locomotion lap
  (N-exclusions per F-13) · legolas citation probe (C-1 / C-3 / F-12a — RETURNED, L-46) ·
  jack-ryan Gate-2 Phase-D2 · Matt surfaces (T-1 outcome · C-5 · amendment path).

### F-13 — The count model's trash limb is INCOMPLETE: falsified at its own support on 3/5 discriminating waves while the above-gap population lands EXACTLY on that support (fourth extraction + identity-join)

> **REGISTERED — L-44 (fourth-extraction fold, first contact); ADJUDICATED — L-47 (identity-join
> piece, `gandalf/notes/2026-08-08-kc2-f13-count-model-discrimination.md`; conductor adoptions
> veto-open).** Instrument calibrated before any claim: all four F-10 published cells (271.50 /
> 63.00 · 292.50 · 290.17 / 81.00 · 317.17) and the CONJURE lattice (2/3/2/2/2, band 21.00)
> reproduced exactly. Methodological pin governing every verdict: one censored realization per
> wave ⇒ falsification is **support-based only** (observed lower bound > support maximum);
> undershoots are UNINFORMATIVE without exception.

- **Identity (Q1):** 31/33 plates ROSTERED (30 exact, 1 one-char fuzzy: Culldar → *Tulldar*);
  zero roster-other-point. Exactly **ONE un-rostered body corpus-wide**: `Ugdenbog Crabling`
  (w152 +3.40 s — absent from 1,492 names + 1,617 record paths; robust to the obvious eye-read
  failure, since `Ugdenbog Crab` is also absent from w151/152/153). `Carnivorous Plant` w152
  +0.40 s: UNDECIDABLE, lean carryover. **91 of ~113 bodies are UNIDENTIFIED, not un-rostered** —
  the join has no power over unplated fingerprints; that asymmetry is load-bearing.
  **Un-rostered ≠ conjured:** `Aleksander's Shard` (w160) is equally un-rostered and graded
  SUMMON — the class has ≥ 2 mechanisms, and the level-inheritance summon discriminator has NO
  power on 151–158 (every plausible summoner sits inside the 102–108 regular band). *(L-50: the
  un-rostered class gains a THIRD member — `Skeletal Archer` L105, w153 ×4 (fifth-extraction
  fraction binding; absent from every 151–158 roster across all pool kinds) — and the summon
  discriminator regains power through IDENTITY: the citation question is now concrete — do the
  Revenant records rostered at w153 p03 `skeletonrevenant_t3` carry a summon skill referencing
  `skeleton_a02_archer.dbr`? Corpus-wide un-rostered: Crabling (w152) · Aleksander's Shard
  (w160, SUMMON) · Skeletal Archer (w153, ×4).)*
- **Star-furniture ≠ champion count (§ 1.4 category-error correction):** regular rosters carry
  champion- and hero-ranked RECORDS on 4/5 waves — rank is a property of the monster record, not
  of the proxypool limb that drew it. AC-10.4's 63.00 counts `nameChampion{j}` DRAWS; star-pairs
  count RANK FURNITURE — a superset. The commissioning brief's "star-pairs exceed selection
  champs" premise is RETIRED; reproduced, the champion limb never overshoots. *(L-50 refinement, fifth
  § 7.1/§ 9.3: seven bound star cases are ORANGE/HERO names ONLY — champions carry bare bars,
  so the fourth extraction's "88 plain" bucket mixes commons AND champions; star-pairs are a
  HERO instrument. And § 9.2: `~ Affix` name-shape is NOT a rank signal — glyph colour is
  (champion band G/R 0.91–0.95 vs hero 0.71–0.79). Consistent, not contradictory: the w153
  champion-glyph reads (Revenants, Ugdenbog Golems) are record-rank champions drawn through
  TRASH pools — this § 1.4 correction working in the other direction.)*
- **Discrimination (Q2):** M1 (model of record) **FALSIFIED at its own support on the PLAIN
  limb** — w152 **17 > 7 DETERMINISTIC** (zero-width support: both trash alternatives are
  (5,6) → 7; the hero pools are empty → no-op 0), w153 **23 > 18**, w157 **15 > 14**. STAR limb
  unfalsified everywhere, **w157 6/6 EXACT** (positive control: the instrument CAN reach the
  champion expectation — undershoots elsewhere are engagement censoring, not model error). *(L-50: w157's PLAIN 15 > 14
  SUSPENDED at margin-1 — bar_hue unrun there, one green-bar contaminant collapses it;
  w152/w153 STAND post-strike. The 6/6 gains a glyph rank-audit caveat, fifth § 9.2.)* SKULL
  unfalsified. Lattice: 12/64 cells survive, ALL requiring `trash=ALL` ∧ `CONJURE` — **NOT
  endorsed**: a 2.33–2.84× band correction implying w158 ≈ 81 regulars against a ≈ 14-icon
  minimap, while the **HP decomposition** (unsupervised max-ratio split) lands the above-gap
  plains **EXACTLY on M1's support on both hard-falsifying waves** (w152: gap 2.53×, above-gap
  7 = the deterministic 7; w153: gap 5.37×, above-gap 18 = the support top). **The trash limb is
  INCOMPLETE, not WRONG** — it reproduces the rostered population and is silent about a second,
  low-HP population. Four candidate mechanisms NAMED, none fitted: **(i)** summoned minions
  (w160 precedent MEASURED — same 40k–104k HP band), **(ii)** p05 replenishment (w153
  sensitivity: n = 2 emissions → 23 EXACT; § 10.6's own declared-undetermined `maxGroupSize`
  flag, now load-bearing; does NOT explain w152), **(iii)** CONJURE-on-empty (≤ +3 at w152 —
  insufficient alone; supported by the identity leg only), **(iv)** trash-point multiplicity.
- **Quiet opposite-direction finding (§ 2.5):** `boss_add=OFF` matches the camera 3/3 (w152 1 ·
  w157 1 · w160 4, vs record-model 1.75 / 2.00 / 5.00); band effect 271.50 → **248.83** (−22.67,
  −8.35 %). STRONG CIRCUMSTANTIAL, NOT DECIDED (three undershoots cannot falsify). Rides the
  legolas r3 `proxypool`/`adj03` fine-print rider.
- **F-9 (Q3):** status → **CONTESTED**, disposition UNCHANGED (see F-9's own status bullet). The
  count-pass found something LARGER than F-9: a +18-to-+45-body question over three waves vs
  F-9's ±21 over the band. F-13 is a NEW finding, not a resolution of F-9.
- **Blast radius (Q4):** band = **RANGE — the point estimate is refused**: 248.83 … **271.50
  (record, UNCHANGED)** … **289.62 (measured floor = 271.50 + 18.12 E-form; assumption-free
  arithmetic on measured lower bounds — carried as a FLOOR)** … 632–772 (not endorsed) *(L-50:
  floor CONTINGENT — the 18.12 E-form consumed w153/w157 excesses now under census correction
  (16,368 struck; w157 margin-1 suspended); re-derives at the bar_hue fold from HOSTILE-ONLY
  cohorts. Endpoints 248.83/271.50 untouched.)*. MOVES:
  § 12 T-3 (regular limb → floor-with-named-finding, the F-10 pattern; champion untouched) ·
  AC-10.4 (second annotation; 63.0 empirically corroborated for the first time) · **F-12
  locomotion N-inputs (the painful one: w152's N = 7 vs measured ≥ 17 is a 2.4× error on a
  body-count-coupled timing model — w152/153/157 EXCLUDED from calibration, reported as
  findings)** · baton `count_model` provenance (additive: F-13 + the falsification table + the
  floor + the four named-never-fitted parameters). DOES NOT MOVE: MO-5 (one-sided floor,
  N-independent) · T-2 (annotated: 1.9 % bounds intra-order/rounding/clamp, NOT total count
  error — w152's miss is +10 on a deterministic 7). NEEDS-DATA: AC-10.3 "zero trash" scoping
  (the w160 seven plains are graded SUMMON, which the AC does not model — scope it "about
  spawns") · § 10.6 p05 replenishment fork.
- **Deciders (§ 5, priority order):** **(1) w153 per-body identity pass on the five sub-50k
  bodies** (16,368 ×1, 37,840 ×4) — the only falsifying wave with no boss/skull confound:
  `livingplant_t3` plates (Carnivorous Plant / Ugdenbog Golem) → p05 replenishment; `giant_t3`
  plates (Asterkarn / Groble) → trash multiplicity; un-rostered → summon-or-conjure.
  Deterministic three-way separation on five bodies; **commissioned to galadriel at L-47**.
  *(EXECUTED — L-50: B1 16,368 NOT-A-HOSTILE-BODY, struck; B2 = `Skeletal Archer` L105 Undead
  common — un-rostered across 151–158, the separation lands in its THIRD branch:
  summon-or-conjure, ×4 > CONJURE's +2 → SUMMON indicated. Note: this bullet's plate-class map
  under-enumerated w153's trash pools — four, not two (+ `wendigo_t3` p01,
  `skeletonrevenant_t3` p03) — neither silent case occurred, and the Revenant pool is now the
  summoner-candidate. B3–B5 UNIDENTIFIED (degenerate / no-plate; the ×4 independently
  reproduced by damage-state banding).)*
  (2) `Ugdenbog Crabling` fingerprint binding (a low-cluster binding makes w152's un-rostered
  population seven-bodies-from-one-point, killing CONJURE's 1-body prediction). *(L-50:
  CLOSED-UNBINDABLE — plate saturated FULL on all 4 hover frames, ≥ 5 parsed bodies ≥ 0.988;
  the low band neither confirmed nor excluded.)* (3) w152
  +0.40 s carryover — badge-advance semantics, one `survivalevent.lua` citation (worth 1 of
  w152's 17 and the above-gap count's exact landing). (4) `boss_add` template fine-print
  (legolas r3 rider).
- **Consumers:** § 12 T-3 (annotated) · AC-10.4 (annotated) · AC-10.3 (scoping) · § 10.6 (p05
  fork now load-bearing) · F-9 / F-10 (status bullets) · F-12 + gamora locomotion lap
  (N-exclusions) · baton `count_model` provenance · galadriel w153 decider · legolas r3 rider.

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
