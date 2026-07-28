# G-4 — KIT SPEC — `gd-werewolf-kitcal-1` + mechanism-requirements manifest

**▶ ROLE: SPEC-AUTHOR — G-4, phase P-2 of run `KC1-2026-07-27` (KIT-CAL-1).**
**Author:** named `gandalf` sub-agent · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Authority:** charter `gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §2 T-4, §3 P-2, §8–§12.
Rulings binding this phase: **R-KC1-1, 6, 7, 9, 10, 11, 12** (§12.1); testimony amendments §8.
**Fixture:** `GD-R2-werewolf` (session `GP-gd-2026-07-26-s1`, regime R2) · **Kit id:** `gd-werewolf-kitcal-1`
**Source:** S-3 Edition-II `.arz`, `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`, read-only.
**Consumers:** G-5 (gamora — coverage gate, density sweep, band comparison); star-lord/gamora (adapter);
Matt (owner-eye checkpoint, §7).

**Status:** DRAFT for the §5 owner-eye checkpoint. **§6 bands are DRAFT and do not bind until HALT H-2.**

---

## §0 — What this document is, and the one sentence that governs reading it

Per **R-KC1-9**, the primary claim this run pursues is **structural**, not numeric. The kit spec below
exists so that G-5 can ask *"does the sim express the mechanism classes that produce the fixture's
structural signatures, at `.arz`-plausible parameters?"* — **not** *"does the sim hit 8.4
kills/engagement?"*

Per **R-KC1-12**, when a signature does not reproduce and instrument error is excluded, **the default
attribution is that the sim is wrong**, and the deliverable is a **genre-gap map first, tuning target
second**. §4 is therefore the centerpiece of this document; §1–§3 are its evidence, and §6 is
corroboration that must never be read as the verdict.

**Method note on grades (R-KC1-1, T-4).** Every numeric below is one of:

| Grade | Meaning |
|---|---|
| **MEASURED** | read byte-exact from a named `.arz` record path in S-3 by this pass |
| **DERIVED** | arithmetic over MEASURED or banked values; the derivation is shown |
| **ATTESTED** | Matt's testimony, no instrument; the upgrade criterion is named |
| **UNKNOWN** | named gap; nothing is inferred into it |

**Tooling provenance.** All `.arz` reads reuse legolas's proven TQIT parser
(`research/scripts/gd_arz_adapter_2026_07_24.py`, class `ArzArchive`) — imported, **not**
reimplemented. The probe wrapper is non-production scratch at
`agentic_orchestration/gandalf/scratch/2026-07-28-kitcal1-g4-arz/g4_arz_probe.py`.
**No `.arz` read failed.** Every record named below decoded cleanly.

---

## §1 — The sim-abstract kit spec

### 1.1 Identity and join keys (R-KC1-7)

`.dbr` record paths are the **identity** join key. They are cited exactly, and they are the strings a
`.gdc` `character_skills.skills[].name` will match verbatim when T11 lands — **the save-file join
drops in with no rework**, because every row below is already keyed on the path rather than on a
display name.

| Element | Record path (identity key) | Archive | Template `Class` | Ranks (base/ult) |
|---|---|---|---|---|
| Transform | `records/skills/playerclass10/werewolf1.dbr` | GDX3 | `Skill_Shapeshift` | 16 / 26 |
| Claws | `records/skills/playerclass10/werewolf1_skill01_claws.dbr` | GDX3 | `Skill_AttackWeapon` | 16 / 26 |
| Charge | `records/skills/playerclass10/werewolf1_skill02_charge.dbr` | GDX3 | `Skill_AttackPathCharge` | 16 / 26 |
| Onslaught | `records/skills/playerclass10/onslaught1.dbr` | GDX3 | `Skill_WeaponPool_BasicAttack` | 16 / 26 |
| Default attack | `records/skills/default/defaultweaponattack.dbr` | database | `Skill_WeaponPool_Default` | 1 |
| *(transmuter, likely untaken)* | `records/skills/playerclass10/werewolf1b.dbr` | GDX3 | `Skill_Transmuter` | 1 / 1 |
| *(claws modifier, likely untaken)* | `records/skills/playerclass10/werewolf2.dbr` | GDX3 | `Skill_Modifier` | 12 / 22 |
| *(charge modifier, likely untaken)* | `records/skills/playerclass10/werewolf3.dbr` | GDX3 | `Skill_Modifier` | 12 / 22 |

All eight are **MEASURED**. Mastery is `playerclass10` (Berserker, the Fangs-of-Asterkarn mastery);
`onslaught1` and `werewolf1` are both `skillTier=1`, `skillMasteryLevelRequired=0`, which is
consistent with the fixture's werewolf being available at level ~3 (G-2b §10.1: R2 spans levels 3→11).

**Rank state is UNKNOWN and is the single largest identity gap.** Nothing in T-A/T-B reads a skill
rank. The `.gdc` `skills[].level` closes it exactly (T11 / R-KC1-4). §6's bands are widened for this.

### 1.2 The transform — `werewolf1.dbr` (MEASURED)

| Field | Value | Sim-abstract meaning |
|---|---|---|
| `activeSkillSet` | **1** | **selects skill set 1** — see §2, this is the whole augment/replacement answer |
| `grantedSkills` | `[…claws.dbr, …charge.dbr]` | the form's entire active kit |
| `skillManaCost` | `[50 … 250]` per rank | one-off activation cost, not sustained |
| `notDispelable` | `True` | form cannot be stripped by enemies |
| `exclusiveSkill` | `False` | not an exclusive-slot buff |
| `distanceProfile` | `Short` | — |
| `replacementMeshMale/Female`, `replacementAnims`, `replacementSounds`, `replacementFootsteps` | set | **presentation only** |
| every `characterXxx` stat modifier | **0.0** | **the form grants NO stat bonus** |
| every weapon-type flag (`Axe`/`Mace`/`Sword`/`Shield`/`Staff`/`Ranged1h`/`Ranged2h`/`Magical`/`Spear`) | `False`; `unarmedOnly` `False` | **no weapon requirement** |

**Two consequences that matter to the sim spec, both load-bearing:**

1. **The transform is not a power buff.** It confers zero attributes, zero HP, zero resistances. Its
   entire mechanical content is *skill-set replacement plus a mesh swap*. Whatever the fixture's A-step
   is, **it is not a stat step** — it is a change of what the attack *is*.
2. **The equipped weapon still governs damage.** Claws and charge are both `weaponDamagePct` skills
   (§1.3) and the form imposes no weapon restriction, so the level-12 weapon at the R2/R3 boundary
   **feeds offense as well as the defensive step** (F-KC1-1, §9). The gear event is compound on three
   axes, not two.

### 1.3 Claws — the fixture's primary attack (MEASURED)

`records/skills/playerclass10/werewolf1_skill01_claws.dbr` · `Skill_AttackWeapon` · `skillSet=1` ·
`distanceProfile=Melee` · `skillSpecialAnimationName=DoubleClaw` · `ignoreDisruption=True`

Rank arrays are length 26 (ranks 1–16 base, 17–26 ultimate). **The three that carry the A-step:**

| Rank | 1 | 2 | 3 | 8 | 13 | 16 | 26 |
|---|---|---|---|---|---|---|---|
| `skillTargetNumber` | **2** | **2** | **3** | 4 | 5 | 5 | 7 |
| `skillTargetAngle` (deg) | **90** | **90** | **110** | 130 | 150 | 150 | 190 |
| `weaponDamagePct` | 70 | 77 | 84 | 110 | 135 | 150 | 192 |
| `offensivePierceMin` (flat) | 12 | 27 | 42 | 117 | 192 | 237 | 444 |
| `skillManaCost` | 2 | 2 | 2 | 3 | 5 | 5 | 8 |

Full arrays: `skillTargetNumber` `[2,2,3,3,3,3,3,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,6,7,7]`;
`skillTargetAngle` `[90,90,110,110,110,110,110,130,130,130,130,130,150,150,150,150,150,150,170,170,170,170,170,170,190,190]`;
`weaponDamagePct` `[70,77,84,90,95,100,105,110,115,120,125,130,135,140,145,150,154,158,162,166,170,174,178,182,186,192]`.

**The template documents its own geometry.** `records/skills/base_template skills/skill_attackweapon.dbr`
carries `FileDescription`:

> *"Modifies a basic attack. Can affect multiple targets within a set angle. Angle should not be 180.
> 360 is a full circle while angles less than 180 make cone attacks."*

So `Skill_AttackWeapon` is **a basic-attack modifier**, and the geometry is a **swept arc with a hard
target-count cap** — not a radius disc. See §3.

### 1.4 Charge — `werewolf1_skill02_charge.dbr` (MEASURED)

`Skill_AttackPathCharge` · `skillSet=1` · `distanceProfile=Long` · `targetingMode=Point`

| Field | Value | Sim-abstract meaning |
|---|---|---|
| `waveDistance` | **14.0** | charge travel distance (world units) |
| `skillTargetRadius` | **2.5** | impact radius along the path |
| `endRadiusMultiplier` | **1.5** | terminal radius = 3.75 |
| `maxMoveRatio` | 2.0 | overshoot allowance |
| `characterRunSpeedModifier` | **+200%** | the traversal term |
| `skillCooldownTime` | **4.0 s** | the gating term |
| `timeBetweenAttacks` | 100 ms | — |
| `weaponDamagePct` | `[100 … 385]` | rank 1 = 100% |
| `offensivePierceMin` | `[15 … 718]` | flat pierce |
| `offensiveSlowBleedingMin` / `…DurationMin` | `[15 … 484]` / **3.0 s** | **a bleed DoT, present in R2** |
| `offensiveKnockdownMin` | 0.5 s | control |
| `skillManaCost` | `[12 … 62]` | — |

**Finding, and it changes §4's B-factor reading.** Charge carries a **3-second bleed DoT at every
rank**. R3's poison is therefore **not the fixture's first DoT** — R2 already has a damage-over-time
channel riding on 175 charge presses. This is a *strengthening* of the B-signature's testability: the
sim must express a DoT tail in R2 as well as R3, and the R2→R3 B lift (2.27 → 2.94) is a *second* DoT
stacking onto a regime that already had one, not a DoT appearing from nothing.

**Charge is also the C-factor's mechanism, measured.** `waveDistance=14.0` + `+200%` run speed on a
4.0 s cooldown is exactly the dash-chaining G-2b measured at ρ=0.665 (R2) / 0.772 (R3). Per R-KC1-9,
**C is a declared non-target** — but the sim should carry the mechanism so C is *expressible*, because
a sim that cannot chain will mis-shape engagement duration even while A and B match.

### 1.5 Onslaught — `onslaught1.dbr` (MEASURED)

`Skill_WeaponPool_BasicAttack` · **no `skillSet` field → set 0 (base)** · `distanceProfile=Melee` ·
`skillTier=1`

| Field | Value |
|---|---|
| `weaponDamagePct` | `[100 … 210]` |
| `offensiveColdMin` | `[7 … 188]` — **cold**, the kit's only non-physical/pierce channel |
| `skillComboChargeDuration` | 5.0 s |
| `skillComboChargeLevel` | `[3,3,3,3,4,4,4,4,5,5,5,…,5]` — a charge-up basic attack |
| `skillManaCost` | `[1 … 10]` |

Onslaught is a **default-attack replacer** (the weapon-pool basic-attack family; siblings are Cadence
`Skill_WeaponPool_ChargedFinale` and Savagery `Skill_WeaponPool_ChargedScaling`). It is
**single-target** — it carries no `skillTargetNumber` and no `skillTargetAngle`. That is the second
half of the A-step explanation in §3.

### 1.6 Untaken-but-adjacent nodes (MEASURED records, ATTESTED-absent state)

Three nodes would materially change the kit if allocated. **All three are graded ATTESTED-absent** on
the combination of level (~5–11, so ~10–12 skill points total) and skill-tier gating; **T11 upgrades
each to MEASURED** via `skills[].level`.

| Record | Effect if taken | Why the spec assumes absent |
|---|---|---|
| `werewolf2.dbr` | `subSkillName` = **claws**; adds bleed `[12…338]` @ **2.0 s**, life-leech `[10…38]`, crit-damage `[6…65]` | `skillTier=3`; a second DoT + sustain on claws would materially move both B and the intake tail |
| `werewolf3.dbr` | `refreshCooldownSkill` = **charge**, chance `[8…30]%` on `AttackEnemyCrit`, amount 0.8 | `skillTier=6` — deep; would inflate C (dash-chaining) |
| `werewolf1b.dbr` | transmuter: `conversionInType=Pierce → conversionOutType=Chaos`, **100%** | `skillTier=2`, 1 point; would re-route the kit's entire pierce damage to chaos |

**⚠ This is the spec's largest sensitivity.** If `werewolf2` is allocated, claws carries a bleed and a
life-leech that the sim spec below does not model, and the R2 intake tail is partly self-healed.
Named here rather than discovered at G-5.

### 1.7 Controls and state (charter §1, §8, §9)

| Property | Value | Grade |
|---|---|---|
| Potions used | 0 / 0 | MEASURED (T-A endpoints) |
| Devotion assigned | **zero** | **ATTESTED** (Matt 2026-07-28) → MEASURED on T11 conjunctive test |
| Devotion proc fired | none in 313 stills | MEASURED |
| Level span (R2) | 3 → 11 | MEASURED |
| Max HP (R2) | 366 → 759 (2.07× within regime) | MEASURED |
| Max HP (R3) | 1600, **flat** | MEASURED |
| `shield_block_chance` | 15.0 → 18.0 at `play_time` 3256 (**mid-R2**) | MEASURED (§11.2) |
| Difficulty | Normal (assumed; `notes.md` absent) | **UNKNOWN** |
| Skill ranks, all skills | — | **UNKNOWN** → T11 |
| Attribute allocation | — | **UNKNOWN** → T11 |

### 1.8 The level-12 gear event (ATTESTED-identity; structured for the T11 join)

Matt: *"the weapon, shield and amulet I equipped at level 12 added HUGE health boosts."* Confirmed
larger than the testimony implies (§9): **max HP 759 → 1600, 2.11×, then flat for all of R3**;
largest single-frame raw drop 541 → 136; median drop 5.0 → 1.0 raw HP.

**The spec models this as a single parameterised regime transition, not as three items**, because item
identity is UNKNOWN until T11:

```
GEAR-STEP (R2 → R3), sim-abstract:
  ehp_multiplier         = 2.11        [MEASURED from the max-HP series]
  mitigation_delta       = UNKNOWN     [see below]
  offense_delta          = UNKNOWN     [weaponDamagePct scales off the new weapon]
  added_dot              = poison, ~1.000 s tick period   [MEASURED, T-B]
  boundary               = DERIVED-NONIDENTIFYING, play_time 6052-6282  [§11.3]
```

Two corrections carried forward so they are not re-made downstream:

- **Block is NOT the mitigation mechanism** (§11.2). `shield_block_chance` moves once, at `play_time`
  3256 — mid-R2, nowhere near the boundary. Matt wore a shield long before level 12. **Armour remains
  an uninstrumented candidate** for the residual magnitude collapse; the sim spec must therefore treat
  `mitigation_delta` as a **free parameter fitted to the intake tail**, not as a known input.
- **The boundary is DERIVED-NONIDENTIFYING**, not merely uncertain: there is no combat between
  `play_time` 5808 and 6475, so every candidate boundary in the 230 s bracket partitions the
  engagement data **identically**. G-5 must not spend error budget on boundary placement.

**T11 join, pre-wired.** When the save lands, each of `equipment[12]` / `weapon1[2]` / `weapon2[2]`
yields `baseName` / `prefixName` / `suffixName` / `componentName` / `augmentName` — all `.dbr` record
paths — which resolve against this same Edition-II corpus by the §1.1 identity key. **No row above
needs rewriting**: `ehp_multiplier` / `mitigation_delta` / `offense_delta` simply move from
fitted-parameter to MEASURED, and `added_dot` gains its source record. Legolas's hypothesis that a
low-level poison DoT most plausibly lives on `componentName` rather than an affix is **recorded as a
hypothesis, not adopted** (`legolas/notes/2026-07-28-gd-gdc-save-probe.md` §2.2).

---

## §2 — Augment vs replacement: **REPLACEMENT**, settled from source (R-KC1-6)

The last open sub-question of T-2. Matt's testimony established that UI-masking is CERTAIN and asked
the question the telemetry cannot answer: *did Onslaught function as a claws-damage augment while
transformed, or was the press replaced?* R-KC1-6 routed it wholly to this `.arz` read. **It resolves
outright.**

### 2.1 The mechanism: GD partitions skills into numbered skill sets

| Record | Field | Value |
|---|---|---|
| `.../playerclass10/werewolf1.dbr` (transform) | `activeSkillSet` | **1** |
| `.../playerclass10/werewolf1_skill01_claws.dbr` | `skillSet` | **1** |
| `.../playerclass10/werewolf1_skill02_charge.dbr` | `skillSet` | **1** |
| `.../playerclass10/onslaught1.dbr` | `skillSet` | **field absent → 0 (base set)** |

`activeSkillSet` is proven to be a **set selector**, not a boolean, by exhaustive enumeration of every
`Skill_Shapeshift` record in the corpus:

| Shapeshift record | `activeSkillSet` | Granted skills carry `skillSet` |
|---|---|---|
| `records/skills/base_template skills/skill_shapeshift.dbr` (template) | **0** | — |
| `records/skills/playerclass10/werewolf1.dbr` | **1** | claws=1, charge=1 |
| `records/skills/playerclass10/wereraven1.dbr` | **2** | icicles=2, icering=2 |
| `records/skills/itemskillsgdx3/relics/fangs.dbr` | **3** | triplejab=3, screech=3 |
| `.../bossskills/yurra_werewolfform.dbr` | 1 | claws/leap/howl = 1 |
| `.../bossskills/nemesis/mogdrogen2_werewolfform.dbr` | 1 | 5 granted, all = 1 |
| `.../bossskills/scorv_wendigoform.dbr` | 1 | 3 granted, all = 1 |

A corpus-wide scan finds `skillSet` non-zero on exactly **18 records across all four archives**:
14 at set 1 (werewolf/wendigo forms, player + NPC), 2 at set 2 (wereraven), 2 at set 3 (the Fangs
relic). **Every one of them is a transform-granted skill.** The field exists for no other purpose.

### 2.2 The ruling

> **Onslaught is REPLACED, not augmented.** While `werewolf1` is active it sets `activeSkillSet = 1`;
> only skills carrying `skillSet == 1` are in the active set; Onslaught carries no `skillSet` and is
> therefore in set 0. It is **excluded from the active skill set for the duration of the form** —
> exclusion by set partition, which is GD's shapeshift machinery in place of a per-skill exclusion list.
> **Grade: MEASURED.**

### 2.3 Four independent lines now agree

This is the strongest closure available on the question, and it is worth naming that the agreement is
non-trivial — these are four different instruments:

1. **Source (this pass):** set-partition exclusion, MEASURED.
2. **Matt's testimony:** *"the skill that impacted the enemies was the werewolf claw."* ATTESTED.
3. **`onslaught` counter:** frozen at 54 across 10,065 consecutive samples, series terminating on its
   own human-read endpoint (G-2b §10.2). MEASURED.
4. **`defaultweaponattack` counter:** frozen at **74** across 11,486 consecutive samples (verdict C-2).
   **This is the corroboration that was available all along and went unremarked** — the base-set
   *default attack* froze at exactly the same moment as Onslaught. Set-partition exclusion predicts
   precisely that: both are set-0 skills, and both stop. An augment reading predicts neither freeze.

**No disagreement between testimony and series. §8's "testimony and series must agree or the
disagreement is a finding" is discharged — they agree.**

### 2.4 Consequence for the kit spec

`gd-werewolf-kitcal-1` is a **two-active kit for the whole of R2 and R3**: claws (basic attack) +
charge (cooldown gap-close). Onslaught is specified as **present-but-inert** — allocated skill points
that contribute nothing while transformed. The third active graded ATTESTED under R-KC1-6 branch (b)
is therefore **correctly graded, and now known to be inert rather than hidden**: it is not that
Onslaught fired invisibly; it is that it could not fire.

**This retires the "model Onslaught presses as claws-attributed events" clause of branch (b).** There
were no Onslaught presses to re-attribute. The sim must model two actives, not three, and must NOT
carry an Onslaught damage term.

---

## §3 — Claws AoE geometry + spawn/proxy density priors (R-KC1-10)

### 3.1 The claws footprint is an ARC WITH A CAP — not a radius

| Parameter | Source | Value |
|---|---|---|
| Arc (full angle) | `skillTargetAngle`, rank array | **90° at ranks 1–2**, 110° at 3–7, 130°, 150°, 170°, **190° at 25–26** |
| Target cap | `skillTargetNumber`, rank array | **2 at ranks 1–2**, 3 at 3–7, 4, 5, 6, **7 at 25–26** |
| Radius | — | **NOT IN THE SKILL RECORD** — see below |
| Damage per target | `weaponDamagePct` | 70% → 192% of weapon damage |

**The radius is a named gap, and the gap is informative rather than a failure.** `Skill_AttackWeapon`
is a *basic-attack modifier* (§1.3, template `FileDescription`): the reach is the character's weapon
melee reach, a character/weapon property, not a skill property. There is no `skillTargetRadius`,
`maxRange`, or `minRange` on the claws record — I checked, and the absence is structural, not a parse
miss (charge, by contrast, carries `skillTargetRadius=2.5` and `waveDistance=14.0` explicitly).

> **Design finding for the sim:** GD's melee AoE is a **swept arc at weapon reach with a hard
> target-count cap**. It is *not* the "circle of radius R" primitive. This is a genre-obligatory shape
> — Diablo II's Whirlwind/Frenzy sweep, D3's cleave arcs, PoE's melee splash all carry an arc, and
> D2/PoE both carry target caps on splash. §4 grades RDR against it.

**Grade: MEASURED** for arc + cap; **UNKNOWN** for radius, with the reason named.

### 3.2 Why this is the A-step, and why R1 had none

Set the two attacks side by side at the ranks that were live:

| | R1 build (pre-swap) | R2/R3 build (werewolf) |
|---|---|---|
| Basic attack | `defaultweaponattack` / `onslaught1` | `werewolf1_skill01_claws` |
| Targets per swing | **1** (no `skillTargetNumber` on either record) | **2–3** at plausible ranks |
| Arc | none | **90°–110°** |

The fixture's most extreme measured fact — *R1: 43 kills in 43 separate half-seconds, zero multi-kills,
P(0 of 43 | R2's rate) = 7.0e-11* — is **exactly what a single-target basic attack produces**, and
R2's immediate multi-kill (first four engagements 1.33 / 1.80 / 1.00 / 1.40) is **exactly what
`skillTargetNumber ≥ 2` produces.** The A-step is not a proficiency ramp, not a zone ramp, and not a
pack-size ramp — G-2b ruled out all three empirically. **It is one integer field in one `.dbr`
record.**

That is the cleanest calibration target this run has, and it is why §4 grades the A-step's mechanism
classes hardest.

### 3.3 Density priors — `.arz`-plausible pack sizes for the G-5 sweep

**Source: `records/proxies/pools/` in `database.arz` — 326 pool records, 326 of which carry
`spawnMin`/`spawnMax`. MEASURED.**

| Statistic | `spawnMin` | `spawnMax` |
|---|---|---|
| Mode | **3** (118 pools) | **5** (72 pools) |
| Median | **3** | **6** |
| Mean | 6.48 | 9.40 |
| Distribution (head) | 1:48 · 2:42 · **3:118** · 4:51 · 5:29 · 6:19 | 1:21 · 4:33 · **5:72** · 6:49 · 7:51 · 8:30 |

Restricted to **low-tier pools** (those whose `levelVarianceEquation1` is `lv1_*` or `lv2_*` — the
level band the fixture actually played), **227 pools**: `spawnMin` mode **3** (86 pools),
`spawnMax` mode **5** (50 pools). Champion overlay across all pools: `championChance` median
**30.0%**, `championMin` 1, `championMax` 2.

> **The G-5 density sweep band, recommended: pack size 3–6, centred on 4, with a ~30% chance of 1–2
> champions.** Mean is reported but should **not** be used for centring — it is inflated by a handful
> of large-swarm and sentinel pools (including one `999` unlimited-pool record), and the mode/median
> agree tightly at 3–5 where the mean does not.

**Why this is strictly stronger than the cancelled T-C pixel census.** The sweep asks: *does the sim
reproduce the A-step at these densities?* A pack of 3–6 with a 2–3-target arc yields multi-kill
routinely; a single-target attack against the same pack yields none. Both regimes are reproducible
from the same density prior — which means **the A-step is testable without measuring GD's actual
on-screen pack sizes at all.** If the sim needs pack sizes outside 3–6 to produce the A-step, that is
a miscalibration finding with a pre-registered threshold, exactly as R-KC1-10 intends.

**One honest limit, stated rather than smoothed.** Which specific pool a world spawn instantiates
lives in `Levels.arc` spawn tables, which are **not parsed** (the same limit M4 recorded for monster
identity). These are therefore **corpus-wide priors over Act-1-tier pools**, not the fixture's actual
zone tables. That is adequate for a sweep band and inadequate for a point estimate — and the sweep is
what R-KC1-10 asked for.

---

## §4 — MECHANISM-REQUIREMENTS MANIFEST (R-KC1-12) — the centerpiece

**⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC.** §1–§3 authored a spec. This section judges the sim against
it, read-only, with file/line evidence. The conflict seam is live and declared: I am about to grade an
engine against requirements I derived one section earlier.

**Grading vocabulary (R-KC1-12):** **PRESENT-CALIBRATABLE** (the mechanism exists; only numbers are
wrong) · **PRESENT-MISCALIBRATED** (exists but its *shape* diverges structurally) · **ABSENT** (no
mechanism; routes to the build queue as a design finding, **not** a failure).

**Obligation vocabulary:** **genre-obligatory** (absence is a gap RDR should close) vs **GD-specific**
(absence is fine — RDR identity governs; spirit-swap, form-library and elements are design divergence,
not error).

**Two priors were carried in and both were re-verified rather than assumed, per commission.**

> **PRIOR 1 — "`retaliation` appears nowhere in simulation code." CONFIRMED, current.** Exhaustive
> grep across `simulation/*.py` and `simulation/spatial_gauntlet/*.py`: **0 hits.** Unchanged.
>
> **PRIOR 2 — "a 2026-05-08 finding recorded no melee geometry exists." SUPERSEDED. The prior is
> stale and the current state is materially better.** The 1D `fight_engine.py` kernel was **deleted**
> (`gamora/v1.1-1d-sim-b6-deletion`, commit `a8b28a1`, 2026-06-16) and the **2D
> `spatial_gauntlet/spatial_engine.py` is now the sole battle sim** for every tier
> (`spatial_engine.py:1-10`). It carries 2D positions, headings, per-entity HP and `is_alive`, cone /
> circle / line geometry kernels, and clustered pack spawning. **Had I graded on the prior, every A-step
> row below would have been wrongly marked ABSENT.** This is the value of the re-verify instruction and
> I am recording it as such.

### 4.1 Signature (i) — the A-STEP: multi-kill emergence

*Required: spatial AoE geometry · pack spatial distribution · melee arc · per-entity kill resolution.*

| # | Mechanism class | Obligation | Grade | Evidence |
|---|---|---|---|---|
| A1 | **Multi-target resolution with per-entity death in one tick** | genre-obligatory | **PRESENT-CALIBRATABLE** | `spatial_engine.py:2449` `_apply_skill_damage(targets_hit: list[SpatialEntity], …)`; per-target loop `:2518-2549` and `:2562-2578`, each with `if target.hp <= 0: target.is_alive = False`. Several targets can die in one call. **Multi-kill is expressible.** |
| A2 | **Cone / arc melee geometry** | genre-obligatory | **PRESENT-MISCALIBRATED** | `_compute_cone_hits` `:1434-1454` is a genuine angular test (`delta <= CONE_HALF_ANGLE_RAD` within `CONE_RANGE_M`). But `CONE_HALF_ANGLE_RAD = math.pi/4` (**90° full**) and `CONE_RANGE_M = 5.0` are **module-level global constants** (`:186`, `:185`) — **not per-skill and not per-rank.** See 4.1a. |
| A3 | **Target-count cap (`skillTargetNumber`)** | genre-obligatory | **ABSENT** | `_compute_cone_hits` returns **every** target inside the wedge; `_compute_circle_hits` / `_compute_line_hits` likewise. Corpus-wide grep for `max_target` / `target_cap` / `max_hits` / `targets[:` in `spatial_engine.py`: **0 hits.** |
| A4 | **Pack spatial distribution (clustered spawns)** | genre-obligatory | **PRESENT-CALIBRATABLE** | `arena.py:1228-1257` `build_swarm_pack_formation(n_packs, pack_size=4, pack_spread_m=12.0, intra_pack_offset_m=2.5, …)` — packs ringed tightly about a pack centre, centres dispersed on a ring. Hand-authored scenarios corroborate (`:491` "leader + 3 minions, tight cluster ≤4m"; `:1158` "≤3m"). |
| A5 | **Parametrised density knob for the G-5 sweep** | genre-obligatory | **PRESENT-CALIBRATABLE** | Same signature: `pack_size` and `n_packs` are free parameters. **The sweep needs no new code.** |
| A6 | **Aggregate-pack damage multiplier** *(the anti-pattern)* | GD-specific / **actively undesirable** | **PRESENT-DEPRECATED — do not use** | `damage_resolver.py:1084-1085`: `if defender.pack_proxy_size > 0 and skill.geometry in AOE_GEOMETRIES: dmg *= defender.pack_proxy_size`. `PackProxy` is **DEPRECATED** and retired from the convergence path (`combatant.py:1148-1170`, W0.9.1 2026-05-21). See 4.1b. |

**4.1a — A2 is the sharpest calibration finding in this manifest.** GD's claws arc **scales with rank**
(90° → 190°) and the sim's cone is a **fixed 90°**. Three consequences, in ascending severity:

- At claws ranks 1–2 the sim's 90° cone is an **exact match**. The fixture's own R2 is therefore
  reproducible *today* if the rank was low — which T11 will tell us.
- At ranks 3+ the sim under-covers, monotonically.
- At ranks 25–26 GD's 190° arc is **not expressible as a cone at all** — past 180° it is nearer a
  circle, which is exactly the distinction the template's `FileDescription` draws
  (*"360 is a full circle while angles less than 180 make cone attacks"*). A rank-scaling arc that
  crosses 180° would need to migrate geometry kernel mid-rank. **Naming this now**, because it will
  bite any future high-rank GD kit long before it bites this one.

Note also the **latent flattening** at `spatial_engine.py:137`: the proxy geometry map sends
`"melee_arc" → "point"`, while the main map at `:903` sends `"melee_arc" → "cone"`. Player-allied
proxies therefore lose the arc entirely. Out of scope for this fixture (zero proxies), flagged so it
is not discovered later as a mystery.

**4.1b — A6 is a live trap and I want it named loudly.** The deprecated path models an enemy pack as
**one aggregate defender whose HP is `pack_size × base` and against whom AoE damage is *multiplied* by
`pack_size`.** Under that model **the A-step is structurally inexpressible** — there is one defender,
so "two things died in the same half-second" is not a representable event, and the fixture's single
most decisive fact (43 kills in 43 separate half-seconds vs routine multi-kill) has no image in the
sim. The guards are described in-tree as safety-only and no convergence-path code constructs
`PackProxy`, so this is a warning rather than a defect — **but G-5 must assert `pack_proxy_size == 0`
on every combatant and fail loud if not.** Adding that assertion is my recommendation to gamora.

**Verdict on (i):** the A-step is **reproducible today**, with one ABSENT class (A3) and one
structurally-diverging class (A2) that together bound how faithfully. **A3 is the design finding to
route to the build queue.**

### 4.2 Signature (ii) — the B DoT-TAIL: kill-events-per-burst lift

*Required: DoTs that persist past the killing blow and can themselves be lethal · per-application
stacking.*

| # | Mechanism class | Obligation | Grade | Evidence |
|---|---|---|---|---|
| B1 | **DoT ticks on mobs during a spatial fight** | genre-obligatory | **PRESENT-CALIBRATABLE** | `spatial_engine.py:5134-5142` imports and calls `effect_resolver.tick_effects(e.combatant_state, self._tick_size, self._resolver_rng)` per entity per tick; realized float subtracted from authoritative `e.hp` at `:5176`. |
| B2 | **A DoT tick can be the KILLING BLOW** | genre-obligatory — **the whole B-signature** | **PRESENT-CALIBRATABLE** | `spatial_engine.py:5176-5179`: `e.hp -= _dot; if e.hp <= 0: e.hp = 0.0; e.is_alive = False`, and the frame event carries `lethal=(not e.is_alive)` `:5183`. **Kills arrive after the player stops attacking — exactly the B mechanism.** |
| B3 | **DoT tick period** | genre-obligatory | **PRESENT-CALIBRATABLE, already correct** | `effect_resolver.py:26` `DOT_TICK_INTERVAL = 1.0`. GD's measured DoT tick period on this fixture is **1.000 s** (verdict §6). **Coincident, not calibrated to — worth noting as a free agreement.** |
| B4 | **Per-application independent stacking** | genre-obligatory | **PRESENT-CALIBRATABLE** | `damage_resolver.py:1760-1777` `_add_poison_stack` — *"PoE1-style independent-stack poison model. Each application appends a fresh ActiveEffect with its own duration + tick_damage. Multiple stacks coexist and tick independently."* FIFO eviction at a cap. |
| B5 | **Non-stacking DoT refresh preserving max magnitude** | genre-obligatory | **PRESENT-CALIBRATABLE** | `damage_resolver.py:1780+` `_add_or_refresh` — refresh duration always, keep the **stronger** `tick_damage` (the F3-DEFECT fix). This is the correct ARPG rule and it is already in. |
| B6 | **Bleed as a distinct DoT channel** (charge, §1.4) | genre-obligatory | **PRESENT-CALIBRATABLE** | `effect_resolver.py:52-56` `_DOT_AILMENT_NAMES` is registry-derived from `config/ailments.yaml`, category `dot` → **burn, bleed, drain**. Bleed is first-class. |
| B7 | **Poison as a distinct DoT channel** (R3's gear DoT) | **GD-specific naming** | **PRESENT via the stacking path** | `_add_poison_stack` exists and is poison-named; the ailment registry's DoT set is burn/bleed/drain. Whether `poison` is a registry ailment or only a stacking special case is a **naming reconciliation for gamora**, not a mechanism gap. |
| B8 | **DoT survives the target's death to keep ticking** | **GD-specific — deliberately NOT required** | **ABSENT, and correctly so** | Effects live on the defender; the defender dies, the effect goes. GD is the same. Listed only to close the class. |

**Verdict on (ii):** **fully present.** Every mechanism the B DoT-tail needs exists, including the one
that actually carries the signature (B2: lethal DoT ticks). This is the strongest section of the
manifest and it is worth saying plainly — **the sim can express a DoT tail, so if B misses at G-5, the
locus is numeric, not structural.** Note that §1.4's finding raises the bar usefully: the sim must
show a DoT tail in **R2** (charge's bleed) as well as R3.

### 4.3 Signature (iii) — the GEAR-STEP regime change

*Required: gear→EHP pipeline capable of ~2× discontinuities · a hazard model making intake events
meaningful.*

| # | Mechanism class | Obligation | Grade | Evidence |
|---|---|---|---|---|
| C1 | **Gear→EHP pipeline reaching `max_hp`** | genre-obligatory | **PRESENT-CALIBRATABLE** | `combatant.py:758-759`: `max_hp = (compute_max_hp(vitality, strength) + g_bonus_hp + t_flt["bonus_hp"]) * (1.0 + t_pct["bonus_hp"])` — **both a flat and a percent gear term reach max HP.** A 2.11× step is trivially expressible. |
| C2 | **Gear stats as an injectable measured state** | genre-obligatory | **PRESENT-CALIBRATABLE** | `combatant.py:517` `keystone_measured_gear_stats(...)`, `:560` `certification_gear(...)` returning `bonus_hp` / `bonus_armor` / `bonus_crit_chance` / `bonus_damage_flat` / `bonus_damage_percent` / `resistances`; consumed via `run_spatial_fight(measured_gear_stats=…)`. **The R2→R3 step is two dicts, not a code change.** |
| C3 | **Armour mitigation** (the §11.2 residual candidate) | genre-obligatory | **PRESENT-CALIBRATABLE** | `bonus_armor` on the gear dict; armour mitigation constants at `spatial_engine.py:~210` ("production calibration, jack-ryan Condition 2"); `_armor_symmetric_resistances` in `combatant.py`. |
| C4 | **Block as a discrete avoidance event** | genre-obligatory | **PRESENT-CALIBRATABLE** | `combatant.py:234-235` `block_chance` / `block_value`. Correctly **not** the mechanism here (§11.2 falsified it), but present if the fit needs it. |
| C5 | **Per-hit intake as an EVENT SERIES (not a rate)** | genre-obligatory — **required for tail-fitting** | **PRESENT-CALIBRATABLE** | Per-hit application with `hp_after` and `lethal` at `replica_frame_emitter.py:250` `on_hit(...)` and `:293` `dot(...)`; `BCSignals.premitigation_damage` / `shield_absorbed` / `evasion_misses` / `incoming_attempts` on every combatant (`combatant.py:134-144`). **A zero-inflated intake distribution is measurable, not just a mean.** |
| C6 | **Damage taken by the player from multiple simultaneous attackers** | genre-obligatory | **PRESENT-CALIBRATABLE** | Mobs are independent positioned entities with their own attack loops; intake accumulates per-source. |
| C7 | **Retaliation / reflect as a player-side damage source** | **GD-specific for THIS kit — not required** | **ABSENT (confirmed current)** | 0 hits for `retaliation` in `simulation/`. Nearest analogue is defender-side `_apply_wavec_th_reflect` (`damage_resolver.py:1092`), a monster/TH mechanic. **Not on the werewolf kit's critical path** — no record in §1 carries a `retaliation*` non-zero value. Correctly out of scope; the shortlist already excludes retaliation builds on these grounds. |

**Verdict on (iii):** **fully present and calibratable.** The gear step is the *easiest* of the three
signatures for the sim to express — it is a parameter change. The difficulty is not mechanism, it is
that `mitigation_delta` is a **free parameter** (§1.8) until T11, so C is the signature most improved
by the save-file join.

### 4.4 Manifest summary — the genre-gap map (R-KC1-12's primary deliverable)

| Signature | Classes | PRESENT-CALIBRATABLE | PRESENT-MISCALIBRATED | ABSENT |
|---|---|---|---|---|
| **(i) A-step** | 6 | 3 (A1, A4, A5) | 1 (**A2** arc: fixed 90°, no rank scaling) | 1 (**A3** target-count cap) · 1 deprecated-trap (A6) |
| **(ii) B DoT-tail** | 8 | 6 (B1–B6) | 0 | 1 correctly-absent (B8) · 1 naming item (B7) |
| **(iii) Gear-step** | 7 | 6 (C1–C6) | 0 | 1 correctly-absent-for-this-kit (C7) |

> **Headline: exactly ONE genre-obligatory mechanism class is ABSENT — A3, the AoE target-count cap —
> and exactly ONE is structurally miscalibrated — A2, the fixed-90°/non-rank-scaling melee arc. Both
> sit on the A-step, and both are geometry.** Everything the B and C signatures require is present.

**Two build-queue findings (design findings, not failures, per R-KC1-12):**

- **BQ-1 — AoE target-count cap.** Add a per-skill max-targets parameter to
  `_compute_cone_hits` / `_compute_circle_hits` / `_compute_line_hits`, applied nearest-first after the
  geometry test. Genre-obligatory: D2 splash caps, D3 cleave caps, PoE melee-splash caps, and GD's
  `skillTargetNumber` are the same design device — **it is the primary knob by which an ARPG tunes AoE
  breadth against pack density**, and RDR currently has no such knob at all. Its absence means RDR AoE
  breadth is governed solely by geometry size, which couples breadth to *reach* — a coupling every
  named comparator deliberately breaks.
- **BQ-2 — per-skill (and rank-scaling) cone angle + range.** Promote `CONE_HALF_ANGLE_RAD` /
  `CONE_RANGE_M` from module constants to per-skill fields with a global default. Genre-obligatory:
  a sim in which every cone is the same 90° cannot differentiate a narrow jab from a wide sweep, which
  is a *class-fantasy* distinction, not just a numeric one.

**One G-5 pre-flight assertion, recommended to gamora:** assert `pack_proxy_size == 0` on every
combatant and fail loud otherwise (§4.1b). The deprecated aggregate-pack path would silently make the
A-step inexpressible while producing plausible-looking totals — the most dangerous failure shape there
is, and precisely the D-1 pattern (a legible, wrong answer).

**What this manifest does NOT claim.** It does not claim the sim will hit the bands. It claims that
for two of three signatures the mechanism classes are all present, so a miss there is numeric; and
that for the A-step, two named geometry gaps bound achievable fidelity in advance. Per §7 of the
charter, a miss decomposed is a run succeeded — and this manifest is what makes the decomposition
possible **before** the comparison runs rather than after.

---

## §5 — ADAPTER-SPEC ADDENDUM (R-KC1-11) — requirements only

**For star-lord / gamora to implement later. This is a specification, not an implementation.**
Authority: R-KC1-11 — *findings flow into sim mechanics; parameters (grain, sampling, gating) flow into
harness + adapter, **never** into sim mechanics* (the D3 Greater-Rift-timer Goodhart guard).

### 5.1 The architectural law, restated so it cannot be eroded

> **The sim never sees pixels. The adapter never touches mechanics.**
> The comparison is made fair by **degrading the sim's native telemetry to OCR-like conditions**, not
> by enriching the fixture. The exact native ledger is **retained in parallel** for diagnosis.

Concretely: no degradation parameter (`fps`, coverage-hole geometry, counter lag) may be read by any
module under `simulation/` that participates in damage, HP, RNG or control flow. The adapter is a
**sink**, downstream of everything.

### 5.2 Substrate — the emitter already exists, and it is the right one

`spatial_gauntlet/replica_frame_emitter.py` (`replica-frame/v1`, NDJSON) is the correct foundation and
should be **extended, not duplicated**:

- It is **observability-only and default-off**: *"READS engine state and mutates NOTHING — no RNG
  draw, no HP/position/is_alive/energy write, no accumulator touch. `frame_sink=None` ⇒ byte-identical
  existing behavior."* That is the Goodhart guard already enforced in code.
- It emits exactly the event vocabulary the ledger needs: `header` · `tick(tick, t_s)` ·
  `on_hit(source, target, amount, delivered, hp_after, lethal, …)` · `dot(…, lethal, …)` ·
  `deaths_from_diff` / `_emit_death(entity_id, killer_id, death_element, tick, t_s)` · `footer(winner,
  elapsed_s, mobs_killed, …)`.
- It is determinism-safe: full-precision floats, **no wall-clock and no UUID fields**, fail-loud on
  non-finite.

### 5.3 Adapter requirements

| # | Requirement | Rationale |
|---|---|---|
| **AD-1** | Emit a **common ledger schema matching the ta-full column shape** — one row per sample per field, carrying `play_time`-analogue, `kills`, `deaths`, per-skill `skill_use_count` keyed by **sim kit-element id** (the R-KC1-7 identity analogue of a `.dbr` path), `hp_current`, `hp_max`, `life_healed`-analogue. | Comparison joins on the **measurement** key (R-KC1-7): common schema + `harness_version`. |
| **AD-2** | **Down-sample to 2 fps** (0.5 s), matching T-A. Down-sampling is **decimation of a monotone counter series, never interpolation** — emit the counter value as of the sample instant. | The fixture's 0.5 s grain aliases multi-kills into single samples (verdict §5: 201 of 514 kill-samples are multi-kill). The sim must inherit that aliasing or A is measured on a finer instrument than the fixture and the comparison is invalid. |
| **AD-3** | **Coverage-hole injection** per the fixture's coverage model: R2 90.11%, R3 75.89% frame coverage; **4 of 16 R3 engagements at zero coverage**. Holes are applied as *contiguous blackouts*, not as i.i.d. dropout — the real hole is a gold XP-bar bloom occluding screen rows for a sustained span. | An i.i.d. dropout model would be *easier* than reality and would flatter the sim. Contiguity is the property that makes a hole cost whole engagements. |
| **AD-4** | **Deaths-counter lag.** The fixture's death events are known to sit outside instrument windows (R-KC1-8: the `play_time` 2837 death is invisible to every instrument on the table). The adapter must reproduce the **attribution lag**, not just the count. | Otherwise the sim appears to have perfect death attribution the fixture never had. |
| **AD-5** | **Emit both a degraded ledger and the exact native ledger**, tagged, from the same run. Diagnosis reads the exact one; comparison reads the degraded one. | The exact ledger is how an honorable-fail decomposition separates *instrument* error from *sim* error (§7 loci i/ii/iii). |
| **AD-6** | Stamp **`harness_version`** on every emitted row (`harness-v1` = R-KC1-8: encounter gap > 5 s for reporting/TTK/intake; burst ≤ 1.5 s as pack-proxy carrying A and B). | R-KC1-8: the grain is **instrument-canonical**. Comparisons join on `harness_version` for structural like-for-like. |
| **AD-7** | The adapter applies **harness-v1 segmentation via the same code galadriel's `tb_rollup.py` refactor will host** — not a reimplementation. | §11.4's admission: adjacency/bridging/spike rules live in Python, and two copies will drift. One versioned source-agnostic harness, two sources. |
| **AD-8** | **Refusals are emitted as refusals, never as values.** A blacked-out sample carries an explicit refusal marker, matching the fixture's 2,165 kept refusals. | The fixture banked refusals rather than interpolating; the sim's degraded ledger must be readable by the same consumer. |
| **AD-9** | **No adapter parameter may be readable from `simulation/`.** Recommend a CI-grade guard: grep-assert that no module under `simulation/` imports the adapter's config. | The Goodhart guard, made structural rather than documentary — the same move elrond made with the pooled-regime FK. |

### 5.4 Degradation model — the one thing to get right

The degradation model is itself a **hypothesis about the instrument**, and it should be labelled as
one. **R-KC1-11 already names the calibration rig that will settle it:** the Godot OCR leg, where
OCR runs against known truth and yields the pipeline's real error model, applied backward to tighten
this fixture's error bars. Until that lands, AD-2/3/4 are **declared approximations**, and any G-5
result sensitive to their exact form must say so.

---

## §6 — SECONDARY NUMERIC BANDS — **DRAFT for HALT H-2**

### 6.0 Preamble — read this before reading a single number

> **These bands are SECONDARY CORROBORATION, not the verdict.** Per **R-KC1-9** the primary claim is
> **structural fidelity**: (i) the A-step, (ii) the B DoT-tail, (iii) the gear-step regime change.
> §4's manifest grades are what this run is actually about. **A band miss with all three structural
> signatures reproduced is a PASS with a tuning note. A band hit with a signature absent is a FAIL.**
>
> The bands are deliberately **wide and honest**. They are set so that a miss is *informative* —
> narrow bands on a fixture with 106 engagements, ~11% TTK quantization, an unknown skill-rank state
> and a free `mitigation_delta` parameter would be false precision, and false precision is how a
> calibration run learns nothing.
>
> **G-5 runs the coverage gate FIRST** (charter T-5): which fixture series the sim reproduces *at all*.
> Bands are only read after the gate.

### 6.1 Structural targets (PRIMARY — restated so nothing below outranks them)

| # | Target | Fixture value | Pass condition |
|---|---|---|---|
| **S-1** | **A-step exists** | R1 A = **1.000** (43 kills / 43 kill-events, zero multi-kills); R2/R3 A > 1 | Single-target kit yields A ≈ 1.0; arc kit yields A > 1.0, **at `.arz`-plausible density (3–6)** |
| **S-2** | **B lift is confined to B** | R2 B = 2.27 → R3 B = 2.94, with A and C unchanged | Adding a DoT lifts kill-events-per-burst and **not** A, **not** C |
| **S-3** | **Gear-step inverts hazard shape** | max HP 759→1600 (2.11×); largest raw drop 541→136; median raw drop 5.0→1.0 | A 2.11× EHP step + fitted mitigation reproduces a **fall in absolute worst-hit**, not merely in %EHP |

### 6.2 TTK-shape bands (R2 primary)

Unit: **encounter**, harness-v1, gap > 5 s (R-KC1-8).

| Quantity | Fixture (R2) | Proposed band | Basis / why this width |
|---|---|---|---|
| Median encounter duration | ~4.5 s *(all-106 median; per-regime figure to be read from `fixtures.db`, **not** taken from here)* | **3.0 – 7.0 s** | 4.5 s at 0.5 s sampling is 9 samples → ~11% quantization (verdict §4). Band ≈ ±50%. |
| Mean / median ratio | 6.1 / 4.5 = **1.36** (all-106) | **1.15 – 1.75** | Right-skew is the shape claim; the ratio tests skew without pinning either moment. |
| Max encounter duration | 37.5 s (all-106) | **≥ 20 s present** | A one-sided *existence* test for a long tail. Maxima are not bandable at n=77. |
| **A** (kills per kill-event), R2 | **≈1.74** *(DERIVED: 647 kills / ~371 kill-events, from 880 total kills / 514 kill-event samples less R1's 43/43 and R3's 190/100)* | **1.35 – 2.20** | Wide because the R2 kill-event count is derived, not read. **G-5 must read the exact value from `fixtures.db`** and re-centre. |
| **B** (kill-events per burst), R2 | **2.27** | **1.80 – 2.90** | Burst grain ≤ 1.5 s is instrument-canonical; B is the most robust of the three. |
| **C** (bursts per encounter), R2 | **≈2.20** | **DECLARED NON-TARGET** | R-KC1-9: player + level routing. Reported, never scored. |

### 6.3 Intake-tail bands (R2 primary) — **fit the tail, not the mean**

The R2 intake distribution is **zero-inflated with a heavy tail**: 27 hits ≥10% EHP carry **46.8%** of
all R2 intake; the largest single-frame drop is **72.4% of EHP** (at EHP 747, late-regime). A mean is
close to meaningless here and must not be the scored quantity.

| Quantity | Fixture (R2) | Proposed band | Why |
|---|---|---|---|
| Fraction of encounters with **zero** recorded intake | *(read from `fixtures.db`)* | **within ±15 percentage points** | The zero-inflation is the shape; it is also the most instrument-sensitive quantity (coverage). |
| Share of total intake carried by hits ≥10% EHP | **46.8%** | **30% – 65%** | This is the tail-dominance statistic and the single best one-number summary of hazard shape. |
| Count of ≥10%-EHP events per 100 kills | 27 per 647 = **4.2** | **2.0 – 8.0** | Rate form, so it survives sample-size differences. |
| Largest single intake event, as %EHP | **72.4%** | **≥ 40% present** | One-sided existence test: the sim must be *capable* of near-lethal single hits. |
| Median intake event, raw HP | **5.0** | **ratio to max-event within 3× of fixture's** | Scored as a **ratio** (median/max), because raw HP units differ between GD and RDR and an absolute band would be meaningless. |

### 6.4 R3 — travels with TWO conditions, always (report-only)

Per R-KC1-9, R1/R3 are **report-only** — no band binds them. Every R3 figure must carry **both**
conditions or it must not be quoted:

> **R3 figures are (a) POST-GEAR-STEP and (b) COVERAGE-HOLED** — 4 of 16 engagements (33 kills) at
> zero coverage; `life_healed` rejection **15.15%** in R3 against 1.26% in R2 (a 12× skew);
> **R3 mean intake is 163.3 (delta-gated) or 188.4 (frame-gated)** and **must never travel as a bare
> number** (§11.4). Both quantities are real; the store holds both.

R3's role in this run is **structural only**: it is the evidence for S-2 (the B lift) and S-3 (the
gear step). It is not a numeric target and its 16 engagements could not support one.

### 6.5 What would make me want to re-draft these bands

Stated so the preregistration discipline is honest about its own inputs (§5 owner-eye, and the H-2
gate): **T11 landing.** Exact skill ranks change §6.2's A band materially (claws at rank 2 vs rank 5 is
2 targets vs 3, i.e. a different A entirely), and exact gear identity converts `mitigation_delta` from
a fitted parameter to a MEASURED input, which tightens §6.3 substantially. If T11 lands **before** G-5
runs, these bands should be re-drafted rather than used. If it lands after, the run proceeds on these
and T11 becomes the next lap's tightening.

---

## §7 — FOR MATT'S EYE (charter §5, owner-eye checkpoint)

You played this build; your testimony has already twice caught what the instruments graded wrong. Two
short lists.

### 7.1 Every ATTESTED grade in this spec

| # | Claim | Basis | What upgrades it |
|---|---|---|---|
| 1 | **Devotion assigned = zero** | your testimony 2026-07-28 | T11 `.gdc`: the conjunctive test (`devotionPointsUnspent == totalDevotionUnlocked` **AND** `devotionReclamationPointsUsed == 0` **AND** ∀ `skill.devotionLevel == 0`) — closes the refund loophole neither the proc-absence observation nor the attestation can close |
| 2 | **Onslaught was pressed but had no effect** (third active present, inert) | your testimony + the frozen counter | Nothing further needed — **§2 upgraded the *mechanism* to MEASURED.** Your intent to press it remains attested; that a press could not fire is now source-proven |
| 3 | **The three level-12 items' identity** (weapon + shield + amulet) | your testimony | T11 `.gdc`: `equipment[12]` / `weapon1[2]` / `weapon2[2]` → `baseName` / `componentName` / `augmentName` |
| 4 | **`werewolf2`, `werewolf3`, `werewolf1b` NOT allocated** (§1.6) | inference from level ~5–11 and skill tiers 3 / 6 / 2 — **this one is mine, not yours** | T11 `skills[].level`. **If any of the three IS allocated, §1.6 says what changes** — `werewolf2` in particular adds a bleed + life-leech to claws that this spec does not model |
| 5 | **Potions 0/0** | 313 stills + your ruling | T11 `play_stats.healthPotionsUsed` / `.manaPotionsUsed` |

### 7.2 Every judgment call I made (each is yours to overturn)

1. **§2 — I graded augment-vs-replacement MEASURED, not merely strongly-inferred.** The basis is the
   `skillSet` / `activeSkillSet` partition plus an exhaustive corpus scan showing the field exists for
   no purpose other than transform gating. I consider this decisive. **If you read it as inference
   rather than measurement, say so** — the downstream effect is whether the sim spec carries an
   Onslaught damage term (it currently does not).
2. **§2.4 — I retired branch (b)'s "model Onslaught presses as claws-attributed events" clause.**
   There were no presses to re-attribute. This is a small unilateral narrowing of a ruling you
   ratified, and I am flagging it rather than absorbing it silently.
3. **§3.3 — I recommend centring the density sweep on mode/median (3–6), not mean (6.5–9.4).** The
   mean is inflated by large-swarm and sentinel pools. Defensible, but it is a choice, and it moves
   what "`.arz`-plausible" means for the whole sweep.
4. **§3.3 — the density priors are corpus-wide over low-tier pools, not the fixture's actual zone
   tables.** `Levels.arc` is unparsed. I judged this adequate for a *sweep band* and inadequate for a
   point estimate. If you want the real zone tables, that is a new legolas lane.
5. **§4 — I graded A2 (fixed 90° cone) PRESENT-MISCALIBRATED rather than ABSENT.** A real angular
   test exists and at claws ranks 1–2 it is an *exact* 90° match. A harsher reading is available.
6. **§4 — I raised two build-queue items (BQ-1 target-count cap, BQ-2 per-skill cone angle) as
   genre-obligatory.** That is a design claim about what ARPGs owe players, not a measurement. It is
   the most opinionated thing in this document.
7. **§4 — I overturned the 2026-05-08 "no melee geometry" prior as superseded.** The 2D spatial engine
   is now the sole sim. Had I not re-verified, the A-step would have been graded ABSENT across the
   board and this run would have reached a badly wrong conclusion.
8. **§6.2 — the R2 A value ≈1.74 is DERIVED by arithmetic**, not read. I have said so at the point of
   use and instructed G-5 to re-centre from `fixtures.db`. The band is widened to absorb the
   derivation.
9. **§6.3 — I scored the median intake as a RATIO to the max event, not in absolute HP.** GD HP and
   RDR HP are different units; an absolute band would be meaningless. This is the right call but it
   does weaken the test.
10. **§6.5 — I recommend re-drafting these bands if T11 lands before G-5 runs.** That is me proposing
    to move a goalpost, which preregistration discipline exists to prevent. I am therefore asking
    **now**, before the comparison, rather than after — the decision is yours at H-2.

### 7.3 The one thing I would most like you to check

**§1.6 / item 4 above — whether you put any points into the werewolf line beyond the transform itself.**
Everything else in this spec is either source-measured or closes on T11. That one is my inference from
your level, and it is the assumption with the largest blast radius: `werewolf2` would put a **second
DoT and a life-leech on your primary attack**, which changes both the B-signature and the intake tail
that §6.3's bands are drawn around.

---

## §8 — Provenance

**`.arz` reads performed (all successful, all read-only):** `werewolf1` · `werewolf1_skill01_claws` ·
`werewolf1_skill02_charge` · `onslaught1` · `werewolf1b` · `werewolf2` · `werewolf3` (GDX3);
`defaultweaponattack` · `base_template skills/skill_attackweapon` · `base_template
skills/skill_shapeshift` (database); exhaustive `skillSet` scan across `database` / `GDX1` / `GDX2` /
`GDX3`; exhaustive `Skill_Shapeshift` enumeration (GDX3); 326 `records/proxies/pools/` records
(database). **Zero parse failures. Zero records not found.**

**Sim files audited (read-only, no modification):** `simulation/damage_resolver.py` ·
`simulation/combatant.py` · `simulation/effect_resolver.py` ·
`simulation/spatial_gauntlet/spatial_engine.py` · `simulation/spatial_gauntlet/arena.py` ·
`simulation/spatial_gauntlet/proxy_population.py` ·
`simulation/spatial_gauntlet/replica_frame_emitter.py` · `foundation/math_model.py`.

**Scratch tooling (non-production, marked as such in its own docstring):**
`agentic_orchestration/gandalf/scratch/2026-07-28-kitcal1-g4-arz/g4_arz_probe.py` — a thin wrapper
importing legolas's `ArzArchive`. No new parser was written.

**Signed:** gandalf (`SPEC-AUTHOR` / `DRIFT-CRITIC`), 2026-07-28.
*T-4 satisfied pending the §5 owner-eye checkpoint. G-5 remains held on HALT H-2.*
