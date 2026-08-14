# KC2-PM4 · Lap M · METHOD — the DEATH-MECHANISM decode

> **Run:** KC2-PM4 · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Ruling:** R-PM4-32 (charter L-23)
> **Author:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-14
> **Charter:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md`
> **Laws:** READ-ONLY on every source · **GL-12 decode-never-estimate** · **NOTE-9** every quantity
> asserts its basis · **OUTCOME-FIREWALLED** (§ 0.2) · GL-6 FULL digests (§ 9)

---

## HEADLINE — three findings, in the order they bind

**1. NO SINGLE HIT ON THE WAVE-159/160 BOARD CAN DELIVER 20,005 POST-MITIGATION. NOT ONE.**
196 damage-bearing (body × skill) rows were composed end-to-end against the camera-measured player
defence sheet. The largest **single application of any skill** — melee, weapon, ground-burst,
spell, one projectile — is **16,813.58** (`Reaper of the Lost` / `wendigo_necroticnovainverse`,
one of its twelve projectiles). The largest **melee/weapon** hit anywhere is 16,031.87. The
largest **ground-burst** is 13,785.42. **The referent's 20,005 one-shot cannot be a single hit,
and the tables say so with no bracket wide enough to change it.**

**2. THE ONLY MECHANISM CLASS THAT REACHES IT IS A MULTI-PROJECTILE NOVA WHOSE PROJECTILES
CO-LAND — AND IT REACHES IT EASILY.** 21 of 196 rows exceed 20,005 at their full decoded
projectile count. Six of them need only **two or three** of their projectiles to arrive in the same
sim tick. `Reaper of the Lost`'s inverse nova needs **2 of 12** at the mid range-band and **1 of 12**
at the far band. The conclusion survives the entire declared sensitivity space (attribute-scaling
composition ON/OFF × range band 1/2/3): at the most conservative corner it still needs only 3–6 of
12, against a skill that launches twelve.

**3. THE MEASURED VIDEO AGREES ON MECHANISM CLASS AND CANNOT RESOLVE IDENTITY.** At the kill frame
the referent's screen carries its wave-160 maximum nameplate census (13, a lower bound) with only
**2** bodies inside the melee contact ring — a ranged-arrival board, not a melee board. The
vitality-coloured ink class spikes to **0.02582**, 2.4–2.5× the three next-deepest wave-160 bursts,
while red and magenta fall to their lowest of the four; the green ink centroid moves **monotonically
inward from 550 → 422 ground-px across the 1.1 s ending at the death**. But the screen is 30–47 %
saturated ink in every annulus, and the discrete-blob instrument returns a **measured negative**:
no discrete cyan or green blob comes within 220 ground-px of the player anchor in the 0.9 s before
death. **The optical channel is saturated. It corroborates "ranged, vitality-coloured, converging."
It does not name the killer, and this lap does not name it either.**

---

## 0 — Preliminaries

### 0.1 What this lap is

Ruling R-PM4-32: *T1 is the run's title and the reference cell has never died.* Lap K measured the
death to the frame; Lap L measured the player's offence; I-12 got the sim to floor 0.131 without
dying. **The missing object is the KILLER.** This lap asks the tables, by pure arithmetic, which
bodies and which skills on the wave-159/160 board can price 20,005 post-mitigation inside one sim
tick (≤ ~0.09 s), cross-checks the referent footage at the death frame, and reads the measured
timing structure against the candidates' own cadence.

### 0.2 The firewall, stated precisely

This lap read **no** sim output, **no** findings JSON, **no** gamora landing note, **no** baton
produced after the frozen roster roll. Sources, exhaustively:

| source | what for |
|---|---|
| `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` (8 `.arz` archives + `database/templates.arc` + 7 `Text_EN.arc`) | every magnitude, every field description, every display name |
| `…/output/kc2-baton-v1-E-s09-cp150-20260809_052836.json` (`actors[].record_path/wave` only) | the frozen ROSTER basis — flagged per row, never used as a filter |
| `reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv` | pool/roster basis (my own pe6 emission, re-verified at Lap I § 4.2) |
| `/Volumes/reincarnated/…/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` | Q2/Q3 video, digest re-verified IN FULL this session (§ 4.1) |
| legolas Lap A `measured-player-sheet.csv` · Lap L § 6.2 armour law · Lap K `pm4k_deep_bursts.csv` | the player defence sheet and the death anchor |

**Not read:** any I-9…I-12 baton, any sim CSV, any T-scorecard. I do not know what result would help
the sim converge, and § 5's null results are reported at the same weight as § 2's positives.

### 0.3 Instruments

`agentic_orchestration/research/scripts/`:
`pm4m_lib_2026_08_14.py` (chain + mitigation) · `pm4m_emit_2026_08_14.py` (Q1) ·
`pm4m_cycle_2026_08_14.py` (Q3) · `pm4m_video_2026_08_14.py` (Q2 colour/annulus) ·
`pm4m_blobs_2026_08_14.py` (Q2 discrete-blob discriminator).
The `.arz` reader, the summon closure, the skill closure, the level sets and the wave-array law are
**imported from Lap D / Lap I, never re-implemented** (`E3.winner` whole-record replacement, the
L-33 / C-9 overlay law).

---

## 1 — THE POPULATION (NOTE-9 — five populations, each named)

| id | basis | n |
|---|---|---:|
| **P-POOL-159/160** | every record the Crucible's own spawn pools can place on waves 159 or 160 (`pe6_crucible_wave_pools_v2.csv`, roster + champ columns) | **39 records / 19 pools** |
| **+ summon closure** | `summon_closure_extended` to fixpoint, layers `[39, 3]` | **81 bodies** |
| **damage-bearing (body × skill) rows** | any body × any skill in its closure carrying ≥ 1 instant damage family or weapon damage | **196** |
| **P-ROLLED (flag only)** | frozen baton `actors[].record_path`, waves 159–160 | 14 actors / 9 records |
| bodies with no level source | | **0** |

**⚑ Why the POOL and not the ROLL is the population.** The frozen baton is *the sim's* roll from the
pools. The referent (Matt's actual fight) rolled its own, and this lap must not assume the two
agree. Every row therefore carries `in_frozen_baton_roll` as a **flag, never a filter**. Four of the
top six candidates are bodies the baton did *not* roll — a consumer that had filtered to the baton
would have discarded `Valdaran` and `Zantarin` before looking at them.

Levels are MEASURED from the pool proxies (Lap D's index-paired slot law, `APL_B_PRIME = 103.4`):
`lv7_uber hero` → {106, 107, 108}; `lv6_hero` → {107, 108}; **`lv8_boss+` → {109}** — every wave-160
nemesis at charLevel **109**. The referent's own screen prints **109** under the wave-160 monster
banner (§ 4.3): *the level chain is confirmed by the game's own HUD.*

---

## 2 — Q1 · THE ARITHMETIC CHAIN, TERM BY TERM

`pm4m_candidate_table.csv` (196 rows × 47 cols) · `pm4m_body_chain.csv` (81 rows × 24 cols).
Every row carries `arithmetic_chain` as a human-readable string of exactly the numbers below.

### 2.1 The player's defence sheet — MEASURED, and where each number comes from

| quantity | value | basis |
|---|---:|---|
| HP the killing blow had to overcome | **20,005** | Lap K (post-death max 18,065 ⇒ 1,940 was buff) |
| Armour | **3,557** | Lap A, screenshots 495/508 |
| Armour absorption | **70.0 %** | `records/game/gameengine.dbr :: armorDefensiveAbsorption` (Lap L closed Lap A's GAP) |
| Defensive Ability | **2,591** | Lap A |
| resists — physical / bleed / **all eight others** | 16 / 85 / **80** | Lap A resistance grid |
| Block · Dodge · Deflect | **0 · 0 · 0** | Lap A frame 519 — **no avoidance layer exists on this build** |

Armour law, verbatim from `records/game/combatformulas.dbr`:

```
dmg <= armour :  physcialDamageDefenseEquationDLEP = dmg * (1 - absorption)
dmg >  armour :  physicalDamageDefenseEquationDGP  = armour*(1-absorption) + (dmg - armour)
```

**⚑ What the sheet implies before any monster is read.** To land 20,005 post-mitigation the attack
must carry, at the *raw* end: **26,305 physical** (armour + 16 %), or **100,025** of any of the eight
80 %-resisted types, or **133,367 bleed**. And **there is no resistance-reduction magnitude anywhere
on this board** — see § 5.1. The player's 80 % wall holds for the whole fight.

### 2.2 The attacker chain — five terms, each with record + field + index

```
flat(type, rank)   skill.offensive<TYPE>Min|Max  at rank = int(ev(skillLevel_i, charLevel))
                   [+ the body's own PASSIVE weapon damage x weaponDamagePct, for weapon classes]

attribute          combatformulas.physicalDamageEquation = dmg*((dexterityDV/245)+1)     [phys, pierce]
                   combatformulas.magicalDamageEquation  = dmg*((intelligenceDV/215)+1)  [the rest]
                   dex/int from the body's characterAttributeEquations bio at charLevel

total-damage mod   mp+difficulty_enemies01.offensiveTotalDamageModifier[8] = +40.0   (Ultimate/solo)
                 + survivalmode_enemies03.offensiveTotalDamageModifier[159] = +43.0  (wave 160)
                 + the body's OWN offensiveTotalDamageModifier passives

per-type mod       survivalmode_enemies03.offensive<T>Modifier[159]  (physical = -21.0; all others 0)
                 + mp+difficulty_enemies01.offensive<T>Modifier[8]   (all instant types 0 on Ultimate)
                 + the body's OWN offensive<T>Modifier passives

crit               combatformulas.probabilityToHitEquation(body OA, player DA 2591)
                   OA per combatformulas.offensiveAbilityEquation, floored at pthMinimum = 55
                   -> pthThreshold1..6 = 70/90/105/120/130/135 -> pthDamageModifier = 1.0..1.5
```

Composition of the three total-damage terms is **ADDITIVE-BY-PARALLEL** with the life chain — Lap I's
named soft joint (`DERIVED-SUM-ADDITIVE-BY-PARALLEL`), carried unchanged, components on the row.

### 2.3 ⚑ MEASURED: no monster on this board can crit the player above tier 2

Every wave-160 nemesis resolves OA **2,725 – 3,118** against the player's DA 2,591 → PTH **93.0 –
104.7**. Every one of them clears threshold 2 (90) and **none reaches threshold 3 (105)** — the
closest is `The Iron Maiden` at 104.72, short by 0.28. So:

- **hit chance = 1.0 for every body** (`PTH/70 > 1`) — combined with Block/Dodge/Deflect = 0,
  **every monster attack on this board connects, always.** There is no miss limb to hide behind.
- **crit multiplier = ×1.1, universally.** The kill is not a crit-tail event.

`offensiveCritDamageModifier = +27.0` (wave) is decoded and **carried, not applied** — how a
crit-damage percentage composes with `pthDamageModifier` is engine-internal (§ 5.4). Applying it
would move the top candidate by at most a further ×1.25.

### 2.4 The candidate table — what reaches 20,005, and how

`reaches_20005_single` is **NO on all 196 rows.** `reaches_20005_volley` is YES on 21.

| Σ volley | N | need @r1 / r2 / r3 | body (game's own name) | skill |
|---:|---:|---|---|---|
| 266,680 | 21 | 3 / **2** / 2 | **Valdaran, the Storm Scourge** | `valdaran_lightningorbnova` |
| 201,763 | 12 | 2 / **2** / **1** | **Reaper of the Lost** | `wendigo_necroticnovainverse` |
| 185,207 | 16 | 3 / **2** / 2 | Reaper of the Lost | `wendigo_necroticnovaboomerang` |
| 144,697 | 16 | 5 / **3** / 2 | **Archmage Aleksander** | `aetherialvanguard_aethermissileinversenova` |
| 125,869 | 18 | 6 / **3** / 3 | Archmage Aleksander | `aetherialvanguard_arcanemissilenova` |
| 125,349 | 18 | 8 / **3** / 2 | **Zantarin, the Immortal** | `zantarin_vitalitynovabarrage` |
| 57,274 | 5 | 4 / **2** / 2 | Valdaran, the Storm Scourge | `valdaran_lightningorb` |
| … 14 more rows in the CSV | | | | |

Display names are **decoded from the game's own `Text_EN.arc` tag files**, never spelled from memory
(`nemesis_wendigo_01.description = tagGDX1Nemesis_Wendigo01` → `gdx1/…/tagsgdx1_creatures.txt` →
"Reaper of the Lost").

**The headline chain, in full** — `Reaper of the Lost` (`nemesis_wendigo_01`, charLevel 109, OA
2,945.19, PTH 99.98, crit ×1.1, own total-damage modifier +109.0 from
`damage_totaladjuster[10]=44 · armorbase05[108]=25 · wendigo_enrage=40`, total modifier **+192.0 %**)
casting `wendigo_necroticnovainverse` at rank 28 (`skillLevel13 = charLevel/4+1`):

```
Life (vitality) : flat 1,986 × attr 6.4419 × total 2.9200 × type 1.0000 = raw 37,357 → applied  7,471
Pierce          : flat 1,249 × attr 5.7755 × total 2.9200 × type 1.0000 = raw 21,064 → applied  4,213
%CurrentLife    : 18 % × 20,005 (at FULL health)                                     → applied  3,601
                                                                            per projectile 15,285
                                                            × crit 1.1              →         16,814
                                             × 12 projectiles (projectileLaunchNumber) =    201,763
```

**Two of the twelve projectiles = 33,627 post-mitigation. The referent needed 20,005.**

### 2.5 The three mechanism classes, and why only one qualifies

| class | rows | max post-mitigation, one application | reaches 20,005? |
|---|---:|---:|---|
| **single-hit** (melee / weapon / spell / one projectile) | 124 | **16,031.87** (`Grava'Thul, the Voiddrinker` / `chthonian02_homingchaos`) | **NO** |
| **ground-burst** (radius / wave / drop) | 41 | **13,785.42** (`The Sentinel` / `witchgodguardian_sentinel_eldritchblast`) | **NO** |
| **volley-overlap** (`projectileLaunchNumber` > 1) | 31 | 266,680 at full N; 20,005 crossed at N = 2 | **YES, 21 rows** |

This is the lap's load-bearing structural claim, and it is a claim about **arrival structure, not
magnitude**: the wave-160 board's per-application damage is bounded well below the player's pool,
and the *only* way it exceeds that pool is by several arrivals sharing one tick. That is precisely
the property I-10 was folding when it replaced the `sha256(actor_id)` swing phase — this lap says the
same thing from the other side of the wire, from tables the sim has never read.

### 2.6 ⚑ The geometry that makes co-landing physical — INVERSE novas

Three of the top six are **inverse** novas (`…novainverse`, `…missileinversenova`) plus one
**boomerang** nova. `Skill_AttackProjectileRing` with `projectileLaunchRotation = 360.0` and
`projectilePiercingChance = 100.0`: the projectiles are placed on a full circle and converge on the
caster rather than flying outward. **A melee player — and an Eye-of-Reckoning player is by
construction standing inside the caster's disc — sits at the convergence point.** The 16-projectile
boomerang carries `projectileTravelDistance = 16.0`, so it returns to the same point.

This is a **decoded geometric affordance, not an observation.** The table does not assert that N
projectiles co-landed in the referent's fight; it asserts that the skill launches N on a 360° ring
with 100 % pierce and that N ≥ 2 suffices. `n_coincident_max` on every row is the *ceiling*, and the
condition is spelled on the row.

---

## 3 — THE DECLARED SENSITIVITY SPACE (the verdict at every corner)

Two composition questions are genuinely undecidable from the corpus (§ 5.3, § 5.5). Rather than pick
one, the table is emitted at every corner. For the top candidate,
`Reaper of the Lost / wendigo_necroticnovainverse`, **projectiles needed to reach 20,005**:

| | range band 1 (≤2 m, ×0.70) | band 2 (2–9 m, ×1.00) | band 3 (9–20 m, ×1.30) |
|---|---:|---:|---:|
| **attribute scaling ON** (combatformulas as written) | 2 of 12 | **2 of 12** | **1 of 12** |
| **attribute scaling OFF** (conservative limb) | 5 of 12 | 4 of 12 | 3 of 12 |

**The verdict is corner-invariant.** At the single most conservative corner the skill still needs
only 5 of the 12 projectiles it launches. There is no reading of the tables in which this board
cannot produce the referent's death by projectile coincidence, and no reading in which it can
produce it any other way.

Note the direction of the range term for an *inverse* nova: a projectile that has converged on the
caster has travelled its **full** distance, i.e. band 3 (×1.30), not band 1. Both are carried
because whether `projectileDamageRange*` measures travel or caster-to-target separation is
undecided (§ 5.5) — but under the reading that matches the geometry, **one projectile alone
delivers 21,857.66 ≥ 20,005.**

---

## 4 — Q2 · THE VIDEO AT THE DEATH FRAME

### 4.1 Substrate + instrument budget

`/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4`
sha256 **`4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8`** — re-verified in full
this session. 1920×1080, 60 fps.

**⚑ Image budget honoured: 3 images read, all downscaled ≤1440 px on the long edge** (the Lap K
crash constraint, banked as a lane rule). Everything else in this section is arrays.

### 4.2 What the already-measured burst composition says (no image cost)

Lap K's `pm4k_deep_bursts.csv`, the death row against the three next-deepest wave-160 bursts:

| burst | t | `vit_green` | `chaos_magenta` | `fire_red` | `plates_at_t0` | `ring_at_t0` | `boss_banner` |
|---|---:|---:|---:|---:|---:|---:|---:|
| **1 = the death** | 864.775 | **0.02582** | **0.00062** | **0.03129** | **13** | **2** | 0 |
| 2 | 850.542 | 0.01022 | 0.00514 | 0.04949 | 6 | 2 | 0 |
| 3 | 847.608 | 0.01064 | 0.00511 | 0.05475 | 10 | 4 | 0 |
| 4 | 845.725 | 0.01546 | 0.00498 | 0.06446 | 7 | 2 | 0 |

At the kill the vitality-coloured class is **2.4–2.5× its value at the three next-deepest bursts and
the highest of the four**, while magenta collapses **8×** and red is the lowest of the four. Nameplates
(a LOWER BOUND) are at their wave-160 maximum of 13 with only **2** inside the melee contact ring.

**Read exactly:** this is a *colour* class, not a damage type (Lap K's I-4 caveat, carried). It is
consistent with a vitality-coloured nova and it does not prove one.

### 4.3 The three images, and what they measured

**Image 1 + 2 (banner crops, `x 560–1360 / 760–1160`, `y 0–96 / 0–40`, ×3.5 upscale).** The
top-centre monster banner at `t = 862.067` and `863.600` reads **"Skeletal Archer"**, with the red
numeral **109** beneath it at `t = 864.723`. The banner names the body under the cursor, **not the
killer** — but the level numeral is a hard cross-check: **the referent's wave-160 board is at
charLevel 109, exactly what the pool-proxy level chain decodes (§ 1).** A Skeletal Archer at wave
160 is a summon: `skeleton_b01_archer_summon` is in the wave-159/160 summon closure, and the same
closure contains `nemesis_orderdeathsvigil_01_revenantsummon` → three skeleton bodies, i.e.
**`Zantarin, the Immortal` was plausibly on the referent's board.** Stated as plausible, not proven:
several bodies summon skeletons.

**Image 3 (full frame at `t = 864.7233`, the last full-health frame, downscaled 1920→1400).** The
board at the kill: the player at screen centre inside a white/red core; a large green energy mass
off-screen-left; scattered cyan/blue point-sources distributed around the lower field; multiple
nameplate HP readouts in the 40k–2M range. **The frame corroborates "ranged, crowded, heavily
VFX-saturated." It does not disambiguate a killer, and I do not name one from it.**

### 4.4 The numeric instruments — one positive trend, one clean negative

`pm4m_death_window_862.0_865.4_60fps.csv` (204 frames) · `pm4m_blobs_864.0_864.9.csv` (3,485 blobs).

**Positive (trend).** The green-ink **radial centroid**, computed over annuli de-projected to the
ground plane (K = 0.537, Lap H-2 D2), falls **monotonically 550.0 → 463.7 ground-px across
`863.72 → 864.7333`** — the full-health dwell — and continues to 422.4 at the death frame and 405 by
864.90. Inward motion of the vitality-coloured ink through the dwell and into the kill is MEASURED.

**Clean negative (discriminator).** The discrete-blob instrument — connected components, area-gated
40–4,000 px, ground-plane radius, **no tracker and no association model, so nothing can be smuggled
in by the linker** — finds **no cyan or green blob within 220 ground-px of the player anchor at any
frame in `864.0 → 864.9`**. The single blob that *is* at the anchor is present, constant, and
**extinguishes exactly at `864.75`** — it is player-attached (it dies when the player does), not
incoming.

**Why the negative does not falsify § 2.** Saturated-ink fraction in the inner annuli runs
**0.107 – 0.528** through this window; the player sits inside a near-white core that the
saturation-gated colour masks exclude by construction. **The optical channel at Crucible 160 is
saturated past the point of resolving individual arrivals, and that is itself the measurement.**
Q2 corroborates Q1's mechanism class and is *unable* to confirm or deny the arrival count.

---

## 5 — Q3 · THE TIMING STRUCTURE

### 5.1 What the referent measured (Lap K, carried unchanged)

```
wave-160 counter first readable   838.8667
excursion start (hp_frac < 0.95)  855.7000          death - 9.1167
excursion floor 0.291877          859.9500
full recovery to 1.0000           863.1167
DEATH                             864.8167          wave-160 arrival + 25.9500
full-health dwell before the kill   1.6166 s
```

### 5.2 The candidates' own cadence — MEASURED (`pm4m_attack_cycle.csv`, 162 rows)

`Reaper of the Lost` (`nemesis_wendigo_01`), verbatim from the record:

| slot | skill | Chance | **Delay** | **Timeout** | Range |
|---|---|---:|---:|---:|---|
| basic | `wendigo_frenzyswipes` | — | — | — | — |
| special1 | `wendigo_tearflesh` | 100 | 11.0 | 5.0 | ShortRange |
| special2 | `wendigo_summonwraiths` | 100 | 18.0 | 7.0 | AnyRange |
| **special3** | **`wendigo_necroticnovainverse`** | **100** | **16.0** | **10.0** | **ShortRange** |
| special4 | `wendigo_bloodheal` | 100 | 22.0 | 8.0 | ShortRange |
| special5 | `wendigo_necroticnovaboomerang` | 100 | 10.0 | 3.0 | AnyRange |

Field semantics, read from the game's own template (`database/templates.arc ::
templatebase/copy of monsterskillmanager.tpl`):

```
specialAttackDelay    description = "Seconds - delay for special skill use"
specialAttackTimeout  description = "Seconds - time out for all skill use"
specialAttackChance   description = "[0..100]"    defaultValue = 100
```

Across the 146 special-attack slots on this board, `Delay > Timeout` on **139**.

### 5.3 The timing verdict — CONSISTENT, NOT FITTED

The commission asks whether the Q1/Q2 mechanism explains the timing. Three statements, graded:

1. **A wave-160 spawn event is RULED OUT as the trigger.** The wave counter reads 160 continuously
   from 838.8667 to 868.3167 (Lap K, I-2 at 60 fps): no new wave arrives at the death. The kill lands
   **25.95 s into a wave the player had been fighting**, not at an arrival.
2. **A ~1.6 s charge-up telegraph is NOT SUPPORTED by the records.** None of the top candidates
   carries a windup, charge or cooldown field: `skillCooldownTime`, `skillChargeDuration` and
   `skillWindUpTime` are all absent on `wendigo_necroticnovainverse`,
   `valdaran_lightningorbnova` and `aetherialvanguard_aethermissileinversenova`. The FX records carry
   `projectileFlightAnimationSpeed = 1.0` and (boomerang only) `projectileTravelDistance = 16.0`;
   **no projectile speed exists anywhere in the corpus**, so flight time is
   UNDECODABLE-FROM-SUBSTRATE. The 1.6166 s dwell is fully explained without a telegraph: the
   player's decoded sustain (leech 21 % + regen 129.38 /s) refilled the bar, and the next nova came
   when its own gate opened.
3. **The interval structure is CONSISTENT with the nova cadence, and I decline to call it a fit.**
   Excursion-start → death is **9.1167 s**; `necroticnovainverse`'s `Timeout` is **10.0** and its
   `Delay` **16.0**; wave-arrival → death is **25.9500 s** and `Delay + Timeout = 26.0`. These are
   suggestive and they are **two data points against a five-slot table with delays 10–22 s** — the
   space is dense enough that a near-hit is cheap. **The AI's actual selection rule is engine-internal
   (§ 5.6) and the referent's monster aggro clock is not the wave counter.** GL-12: decoded numbers
   reported, coincidence flagged, no mechanism asserted from arithmetic that convenient.

**Independent video cadence (MEASURED, descriptive).** Green-ink episodes across wave 160 peak at
`844.667 · 849.767 · 858.967 · 863.267` — intervals **5.1 / 9.2 / 4.3 s**, and the terminal episode
(`863.167 → 864.667`, peak 0.02944) is the longest and brightest of the wave. **It begins 0.05 s
after the player reaches full health and is still up at the kill.** No single period fits the four
peaks, so no cadence is asserted.

---

## 6 — DECLARED GAPS AND CLAMPS (GL-12: a measured negative is a finding; an estimate is not)

### 6.1 ⚑ MEASURED-ABSENT — the board carries NO resistance reduction

Across all 449 skills in the wave-159/160 closure, **no `offensive*ResistanceReduction*` magnitude
field is non-zero anywhere.** One record carries
`offensiveTotalResistanceReductionAbsoluteDurationMin` with **no magnitude beside it**. The player's
80 % wall therefore stands unreduced for the entire terminal band, and every "raw needed" figure in
§ 2.1 is the true bar. This is a *measured* negative and it is load-bearing: it is why the
100,025-raw threshold cannot be dodged by a debuff limb.

### 6.2 ⚑ DEFECT D-M-1, CAUGHT AND BANKED — `offensiveLifeLeech` is not damage

The first emission of this lap treated `offensiveLifeLeechMin` as a damage family. It sits in the
same field namespace as the others, the player sheet carries **Life Leech Resist −25 %** (amplified),
and `Curate Ignus` carries **3,000** of it on a *basic weapon attack*. Composed, it produced a
**60,876 post-mitigation white hit** — an instant kill every 1.4 s, from a nemesis, on every player
in the game. The game's own text settles it:

```
Text_EN.arc :: tags_ui.txt
  DamageLifeLeech          = "{%t0}% of Attack Damage converted to Health"   <- ATTACKER's leech
  DamageDurationLifeLeach  = " Life Leech"                                   <- the actual DoT
```

The instant family is the attacker's **leech percentage**, not damage dealt. Excluded, named in the
library (`EXCLUDED_NOT_DAMAGE`), and the player's −25 % Life Leech Resist correctly belongs to the
`offensiveSlowLifeLeach*` DoT limb (Lap I's, not this one). **Banked because the failure mode —
a plausible field name in the right namespace producing a 4× headline — is exactly the class of
error that would have handed the conductor a confident wrong killer.**

### 6.3 ⚑ DEFECT D-M-2, CAUGHT AND CLAMPED — the Crucible zeroes boss PHYSICAL damage at level 101+

`records/skills/nonplayerskills/passive/armorbase05.dbr` (`FileDescription = "For Bosses - Damage
Reduced Levels 1-20"`) carries `offensivePhysicalModifier = −135.0` at every index ≥ 100. Summed with
the wave term (−21) and the body's `damage_totaladjuster` (+33), the physical multiplier at wave 160
is **−1.23**, i.e. negative. Un-clamped, the first emission produced **negative applied damage** and
inflated three candidates by cancelling their real families. The clamp is applied at 0, graded
`DERIVED-CLAMPED`, and flagged per row (`type_modifier_clamped_to_zero`, non-empty on 9 of 196).

**The finding behind the defect is real and matters to the sim:** at charLevel ≥ 101 the Crucible's
own tables **suppress boss physical damage to zero**, which is why every candidate that reaches
20,005 does so with vitality, pierce, lightning, aether or acid — never physical. **The player's
16 % physical resistance, the weakest number on her sheet, is never the hole she dies through.**

### 6.4 UNDECODABLE-FROM-SUBSTRATE — crit-damage composition

`offensiveCritDamageModifier = +27.0` (wave 160) is decoded. How a crit-damage percentage composes
with `pthDamageModifier` (additive on the multiplier → ×1.37, or multiplicative on the excess →
×1.127) is an engine rule with no corpus field. **Not applied.** Every row's crit term is the bare
`pthDamageModifier` (×1.1). Applying either reading would only strengthen § 2.

### 6.5 UNDECODABLE-FROM-SUBSTRATE — attribute-scaling composition

`physicalDamageEquation` / `magicalDamageEquation` are read verbatim, but whether the attribute
multiplier composes *multiplicatively* with the `%`-modifier pool or is folded *into* it is not in
any record — for the player, GD's character sheet displays the combined figure, which is exactly the
ambiguity. **Both limbs are emitted** (`applied_*` and `applied_*_ATTROFF`) and § 3 gives the verdict
at both. It is corner-invariant.

### 6.6 UNDECODABLE-FROM-SUBSTRATE — projectile range-band reference, and flight time

`projectileDamageRange1..3Min/Max/Scale` exist on 39 skills; whether the band is selected by
**distance travelled** or **caster-to-target separation** is not stated. Both are carried
(`applied_single_hi_crit_r1` / `_r3`). **No projectile speed field exists in the corpus**, so
projectile flight time — the quantity that would decide whether N projectiles of a 360° ring can
share one 0.0834 s window — is not decodable here. **This is the single gap that stands between
"can reach 20,005" (proven) and "did" (not).**

### 6.7 UNDECODABLE-FROM-SUBSTRATE — the AI's special-attack selection rule

`Delay` / `Timeout` / `Chance` / `Range` are decoded per slot with the template's own descriptions
(§ 5.2). Which slot fires on a given opportunity, and how the two clocks interact, live in the
engine. Not asserted (§ 5.3.3).

### 6.8 SCOPE STATEMENTS, not gaps

- **DoT is out of scope here.** This lap prices *instant* arrival only, because the question is a
  0.0834 s window. Lap I owns the DoT limb, and its § 3.4 finding stands: at wave 160 the board's
  DoT is suppressed **−91 points** while instant damage is boosted **+83**.
- **`offensivePercentCurrentLife` is carried at full health** (`18 % × 20,005 = 3,601` for the top
  candidate) with the resistance question declared: the game's text reads
  `DamagePercentCurrentLife = "{%t0}% Reduction to Enemy's Health"` and no resistance field pairs
  with it. It can never be lethal alone — it is a fraction of a survivor's bar.
- **Retaliation is not modelled.** The player carries 1,008 flat physical retaliation at +371 %; a
  reflect limb is a different lap.

---

## 7 — WHAT THIS LAP ESTABLISHES, AND WHAT IT DOES NOT

**Establishes (MEASURED):**
- No single application of any skill on the wave-159/160 board reaches 20,005 post-mitigation. Max
  16,813.58; max melee 16,031.87; max ground-burst 13,785.42.
- Twenty-one (body × skill) rows reach it as a co-landing volley; six need ≤ 3 of their projectiles.
- The verdict is invariant across the whole declared sensitivity space.
- Every monster on this board hits the player with certainty (PTH ≥ 93 ⇒ hit 1.0; Block/Dodge/
  Deflect all 0) and none can crit above ×1.1.
- The board carries no resistance reduction; boss physical damage is table-suppressed to zero at
  charLevel ≥ 101.
- The referent's wave-160 board is at charLevel 109 — confirmed by the game's own HUD numeral.
- At the kill: 13 nameplates (lower bound, the wave-160 maximum), 2 in the contact ring, vitality-
  colour ink at 2.4× the neighbouring deep bursts, green centroid converging 550 → 422 ground-px.
- No wave-160 spawn event and no decodable charge-up telegraph explain the 1.6166 s dwell.

**Does NOT establish:**
- **Which body killed the referent.** The optical channel is saturated; the banner names the cursor
  target, not the killer; and the pool is a superset of what actually spawned in Matt's run.
- **How many projectiles actually co-landed.** No projectile speed exists in the corpus (§ 6.6).
- **That the sim's board would produce the same coincidence.** That is a sim question and this lap
  is firewalled from it.

---

## 8 — CLIFFS FILED (disposition: conductor)

- **C-M1 — projectile speed / flight time.** Not in the corpus. Closable by one controlled in-game
  observation (cast an inverse nova, count frames from cast to impact) or by an engine-binary probe.
  **This is the gap between "can" and "did", and it is the highest-value single measurement left.**
- **C-M2 — the range-band reference (§ 6.6).** Same closure route. Worth a factor **1.857** on every
  projectile candidate — and on the top candidate it is the difference between "1 projectile
  suffices" and "2 do".
- **C-M3 — the referent's actual wave-160 spawn set.** The pool offers 16 nemeses; the referent got
  some subset. Closable only from the footage (silhouette/FX identification at native resolution
  across wave 160) — a **bounded, mapped, crawler-shaped** job now that the candidate list is 21 rows
  long, not a researcher-shaped one.
- **C-M4 — crit-damage composition (§ 6.4)** and **C-M5 — attribute-scaling composition (§ 6.5).**
  Both engine rules; both currently immaterial to this lap's verdict (corner-invariant), both
  material to any future absolute-magnitude claim.

---

## 9 — OUTPUTS AND FULL DIGESTS (GL-6 — never truncated)

| file | rows (excl. header) | sha256 |
|---|---:|---|
| `pm4m_candidate_table.csv` | 196 | `5af996789064870486c44d49e9686a8f5245e37b54f11d294456568f3254e0d3` |
| `pm4m_body_chain.csv` | 81 | `fb8624cb0ef4b6c292ad5f1d6b89bdb55ac0ba01eded25e52434c9f4e00a4797` |
| `pm4m_attack_cycle.csv` | 162 | `1afa81a0efe2916cccc9a8b9b416aef2ae88472e80db9964e913b2fe7803c4b4` |
| `pm4m_death_window_862.0_865.4_60fps.csv` | 204 | `bd6dc4e77513f47164576404cd93deab50266037538a3c7c119023aaa12c3d48` |
| `pm4m_wave160_838.87_865.87_10fps.csv` | 270 | `e3d94c807610356abe308d6314c41363db12b17e65837bd07869ea15aa8bb352` |
| `pm4m_blobs_864.0_864.9.csv` | 3,485 | `8e5191a2c809ecb75b84d1bf2797dac4a9523ba0f1f3d0dd3ed50a315ad4a6a7` |
| `pm4m_emit_summary.json` | — | `66e97449cea91c4b9111cdb4accbcbdc0e43b9035da84ef9853a28259fb3d805` |

Referent video sha256 (verified in full this session):
`4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8`

---

## 10 — LAWS OBSERVED

- **READ-ONLY** on the vendor corpus, the engine tree, the capture store and every baton. Writes are
  confined to this notes directory and `research/scripts/`.
- **OUTCOME-FIREWALLED** — sources enumerated exhaustively in § 0.2. No sim output was opened. The
  null result in § 2.4 (`reaches_20005_single = NO` on all 196 rows) is reported at the same weight
  as the positives, with the maximum any candidate CAN deliver stated three ways (§ 2.5).
- **GL-12 decode-never-estimate** — every magnitude traces to record + field + index. Two defects
  self-caught and banked (§ 6.2, § 6.3), one clamp declared and flagged per row, five gaps declared
  (§ 6.1, § 6.4–6.7), three scope statements named (§ 6.8). Nothing interpolated, nothing
  sibling-filled, nothing modal-filled.
- **NOTE-9** — five populations declared by name (§ 1); the frozen baton is a **flag, never a
  filter**; nameplate counts are stated as LOWER BOUNDS every time they appear.
- **Image-instrument constraint honoured** — 3 images, all ≤1440 px long edge, all downscaled before
  reading. Everything else is arrays.
- **GL-6** — seven FULL sha256 digests in § 9, none truncated.
- **Cliffs filed** (§ 8) rather than resolved by preference.
