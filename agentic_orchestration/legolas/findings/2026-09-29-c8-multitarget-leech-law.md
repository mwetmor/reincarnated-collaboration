# Research — C-8: Grim Dawn's multi-target leech / ADCtH law — 2026-09-29

**Mode:** A (analytical / primary-source probe)
**Commission:** **C-8**, issued under *The Commission Rule* (`gandalf/notes/2026-09-21-the-commission-rule.md` § 4), Run KC2-PLAY; charter ledger **KP-86 F-5/F-6 → KP-93 → KP-95**
**Commissioner / conductor:** gandalf (RUN-CONDUCTOR)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Boundary of record:** KP-95 — *"the oracle accumulates leech per body inside the loop over hits, with no target cap and no per-tick cap: structurally identical to the port"*; port `kc2rt_fight.gd:1320`, oracle `player_sustain.py` + the `leech_pool += applied` loop.
**Access:** read-only throughout. No save, archive, template, footage, pack, oracle or port modified. Footage never opened this lap — the committed 60 Hz traces were re-queried in place. **Disk HALT honoured: this lap wrote ~40 KB and copied nothing.**
**Precedence:** every DBR value re-checked under **KP-79 CRUCIBLE order**.

---

## HEADLINE

> ⚑ **THE COMMISSION ASKED WHICH LEECH LAW. THE EVIDENCE SAYS THE LAW IS PROBABLY RIGHT AND THE *OCCUPANCY* IS WRONG.**
>
> Full per-target credit with **no cap of any kind** is what Grim Dawn's data layer expresses, exhaustively; and the referent's own frames are **consistent** with it. What the referent's frames **exclude** is the oracle's **5.62 mean bodies in the disc at wave 160**. Two independent instruments — the 60 Hz HP-tick inversion and the nameplate ring census — both put the referent at **≈ 1–1.7 bodies**. That is a **2.2×–5.7× occupancy error**, and because leech is linear in bodies it multiplies straight into the surplus.
>
> **I did not find the cap the commission hoped for, and I am not going to supply one.** No cap exists to find. Crate's own answer to over-performing life steal, shipped in v1.2.0.0, was **more monster Life Leech Resistance** — not a cap and not a multi-target rule (§ 6.3).
>
> ⚑ **Two open brackets close as a side effect, both on OFFICIAL sources I re-verified myself:** the ADCtH **basis** (`U-P-N-4` — Crate ratifies the oracle's incumbent, § 6.1) and **`U-P-N-1`** (Crate's patch note says Life Leech Resistance reduces ADCtH; Lap Q measured the same thing off the frames six weeks ago, § 6.3).

| # | question | verdict | grade |
|---|---|---|---|
| **(1)** | GD's law when one activation/tick hits N targets | ⚑ **FULL PER-TARGET CREDIT, NO CAP — no target cap, no per-activation cap, no per-second cap, no diminishing term, no primary-target rule.** Established as an **exhaustive absence over the complete field-name inventory of all 8 archives**, not as a failure to find. | **`DB-EXHAUSTIVE-ABSENCE`** + **`TEMPLATE-CITED`** |
| **(2)** | is there an *engine* cap outside the data layer? | ❌ **SEARCHED `SOURCE-UNLOCATED`.** The binary is not on disk (re-verified, § 0). The data layer cannot see an engine-level clamp. **Footage bounds it: no clamp binds below 8,542 HP per tick** (§ 4.3). | `SOURCE-UNLOCATED` (fact) / `MEASURED-BOUND` (the bound) |
| **(3)** | are EoR's channel ticks "attacks" for ADCtH? | ⚑ **YES.** `Skill_AttackRadiusSpin` → `SkillChanneled.tpl` → includes **`Skill_Attack.tpl`** and `Skill_Activated.tpl`; the record carries `weaponDamagePct = 43` (57 with gear). A skill with a weapon-damage percentage in the attack chain **is** a weapon attack. | **`TEMPLATE-CITED`** (extends C-7 § 2.2) |
| **(4)** | does ADCtH ride the Soulfire/fire limb or only weapon damage? | ⚑ **ANSWERED BY CRATE, AND IT RATIFIES THE ORACLE'S INCUMBENT.** The official guide splits the rule by *source*: **equipment-sourced** ADCtH (all five of this build's summed sources) *"applies as if you attacked with your weapon, scaling with the % Weapon damage"*; **skill-sourced** ADCtH *"applies to all of that skill's direct damage."* **DoT never triggers it.** Zantai adds that flat damage from basic modifiers rides the base skill's %WD — a **bounded upward correction** to the basis, not a change of reading. | **`OFFICIAL-GUIDE-VERBATIM`** + **`OFFICIAL-DEV-POST`** |
| **(7)** | ⚑ does Life Leech Resistance gate ADCtH? (`U-P-N-1`) | ⚑ **YES — CRATE SAYS SO IN ITS OWN PATCH NOTES, and this independently CONFIRMS Lap Q's measured `COUPLED` verdict.** *"Increased Monster % Life Leech Resist. This makes % Attack damage Converted to Health less effective."* — Zantai, v1.2.0.0. **`U-P-N-1` is closeable.** | **`OFFICIAL-PATCH-NOTE`** + **`MEASURED-EXACT`** |
| **(5)** | what does the footage EXCLUDE? | ⚑ **It excludes a primary-target-only rule (§ 5.2), a hard per-tick cap below 8,542 HP (§ 4.3), and — decisively — the ORACLE'S BODY COUNT (§ 5.1).** It does **not** exclude full per-target credit; it is the *only* shape it positively supports. | **`MEASURED-EXACT`** |
| **(6)** | the deciding number KP-86 F-6 called `SOURCE-UNLOCATED` | ⚑ **NO LONGER UNLOCATED ON THE REFERENT SIDE.** Referent mean bodies-in-disc at wave 160: **1.66** (ring census, declared lower bound) and **0.98–2.52** (independent HP-tick inversion). Oracle: **5.62**. | **`MEASURED-EXACT`** ×2, agreeing |

---

## 0 · Surfaces — what was searched, and what is not there

| Surface | Status |
|---|---|
| **Crate authoring templates (808 `.tpl`)** | ✅ **LIVE**, and load-bearing for (1), (3) and the target-cap absence. § 1.2, § 2 |
| **DBRs / ARZ, 8 archives** | ✅ **LIVE.** The **complete string tables** of all 8 were swept for the field-name inventory — this is the instrument that makes the absence exhaustive rather than unfound. § 1.1 |
| **Client strings (`Text_EN.arc` ×7, 20,394 tags)** | ✅ swept. The game's own ADCtH definition recovered; **no multi-target qualifier exists anywhere.** § 1.3 |
| **Client binary (`Game.dll` / `Engine.dll`)** | ❌ **STILL NOT ON DISK** (`find` over `~/depots` and `~/Games`, re-run this lap: zero hits). Unchanged from C-7 § 0. **This is the only surface that could carry an engine-level clamp, and it is absent.** |
| **Footage — committed traces** | ✅ **THE SURFACE THAT DECIDED IT.** Lap Q `pm4q_hp_trace.csv` (10,861 rows, 60 Hz, 100.00 % accepted) + `pm4q_heal_events.csv` (129 ticks) + Lap H-2 `pm4h2_ring_density.csv`. **Read in place; the MP4 was never opened.** § 3–§ 5 |
| **Save (`player.gdc`)** | ⚪ **NOT PROBED, deliberately.** A save records allocation, not engine arithmetic. Its contribution is already folded into `pm4p_adcth_sources.csv`. |
| **Official Crate guide (grimdawn.com)** | ✅ **LIVE and load-bearing.** `/guide/gameplay/combat/` § "Life Steal" carries the ADCtH rule verbatim — **and C-7 § 0 recorded this same page as "silent," which was true of *energy* and not of this.** § 6.1 |
| **Crate dev posts / patch notes** | ✅ **LIVE.** Staff identity verified by API, not reputation; every OFFICIAL quote re-fetched and re-read by me. § 6.1–6.3 |
| **Community (forums / wiki / Steam)** | ⚪ surveyed exhaustively and **cited for nothing**. Fandom returns 402/403 — the same block C-7 hit. § 6.4 |

---

## 1 · (1) — the law, from the data layer

### 1.1 ⚑ The exhaustive field-name inventory — the instrument, stated before the result

Every field name Grim Dawn's data layer uses appears in an archive **string table**, which can be read without decompressing a single record. Sweeping all 8 archives' string tables is therefore a **complete census of the game's vocabulary**, and an absence found this way is exhaustive by construction.

**Every leech-named string in the entire game** (131 hits; the field-shaped ones):

```
offensiveLifeLeech{Min,Max,Chance,XOR,Global}          <- ADCtH, instant
offensiveSlowLifeLeach{Min,Max,Chance,XOR,Global,
                       DurationMin,DurationMax,
                       Modifier,ModifierChance,
                       DurationModifier}                <- "Life Leech", the DoT
defensiveSlowLifeLeach{…,Duration,…,MaxResist}          <- "Life Leech Resistance"
retaliationSlowLifeLeach{…}                             <- retaliation twin
lifeLeachDamageFxPak                                    <- FX
(+ the Mana/Energy twins of each)
```

> ⚑ **NOT ONE of them names a target count, a per-activation cap, a per-second cap, a diminishing term, a primary-target flag, or an AoE scalar.** The vocabulary does not contain the concept.

**And the cross-check that makes the absence meaningful: Crate names its caps.** Sweeping the same string tables for cap/limit-shaped names returns **47**, among them `playerReflectCap`, `playerDefenseCap`, `monsterDefenseCap`, `petLimit`, `miniPetLimit`, `contagionLimit`, `tetherLimit`, `linkLimit`, `potionStackLimit`, `physicsTimeLimit`, `manaOverStorageLimit`, `healthOverStorageLimit`, and the full player/monster/boss attack-, cast- and run-speed cap ladder.

> ⚑ **Crate capped RETALIATION at 30 % (`playerReflectCap = 30.0` in `records/game/gameengine.dbr`) and did not cap leech.** The engine's global tuning record holds the exact class of constant a leech cap would be, by name, and leech is not among them. **That is a deliberate design position, legible in the authoring surface.**

`records/game/combatformulas.dbr` — the global equation record — carries the PTH, damage, block and ability equations and **no leech or heal equation of any kind.**

### 1.2 The target-count field exists, and EoR does not have it

Exactly **one** target-count field exists in the whole game: **`skillTargetNumber`**. It appears in `skill_wpattack_radius.tpl`, `skill_wpattack_radialcrit.tpl`, `skill_wpattack_basicattack.tpl`, `skill_weaponpool_charged*.tpl`, `skill_modifier.tpl`, `skill_kick.tpl`, `skill_spawnpettransmuter.tpl`, `skillsecondary_buffattackradiusdrop.tpl`, `skill_refreshcooldownmodifier.tpl`.

**Eye of Reckoning's include chain does not reach it.** `records/skills/playerclass09/eyeofreckoning1.dbr` (CRUCIBLE winner **`GDX2.arz`**) → `skill_attackradiusspin.tpl`, whose five includes are `SkillChanneled.tpl`, **`Skill_Radius.tpl`**, `Skill_Cast.tpl`, `Parameters_Character.tpl`, `parameters_defensive.tpl`. `Skill_Radius.tpl`'s entire "Skill Config" group is **two fields: `expansionTime` and `skillTargetRadius`.** No count, no angle, no arc.

EoR's own record, rank 20: `skillTargetRadius = 3.0` · `duration = 0.25` · `useResetsDuration = 1` · `timeBetweenAttacks = 200` · `weaponDamagePct = 43`.

> ⚑ **So the authoring surface cannot express a target cap on EoR** — the same strong form C-7 § 4.1 used for regen. This independently confirms my own Lap P column `pm4p_attack_kit.csv :: target_cap_field = ABSENT`, which was derived by a different route.

**A candidate shape the commission did not list, and I checked it because "Spin" invites it:** does the spin hit only a swept *arc* per tick rather than the full disc? **No arc field exists** in `skill_attackradiusspin.tpl` (`timeBetweenAttacks`, `startSound`, `loopSound`, `rotationSpeedMultiplier`, `delayMovement`) or in `Skill_Radius.tpl`. `rotationSpeedMultiplier` is animation. **Full disc, TEMPLATE-CITED.**

### 1.3 The client's own definition — and what it is silent about

`Text_EN.arc`, `tags_ui.txt`, verbatim:

| tag | value |
|---|---|
| `tagCharStatsDamageToHealth` | `Life Steal` |
| **`tagCharStatsDamageToHealthInfo`** | ⚑ **`The percent of the weapon attack damage you deal which also replenishes your health.`** |
| `DamageLifeLeech` | `{%t0}% {^E}of Attack Damage converted to Health` |
| `tagCharStatsHealIncreaseInfo` | `The percent bonus to all healing effects, including Potions and Attack Damage Converted to Health. Does not increase Health Regeneration.` |
| `DefenseLifeLeach` | `{%.0f0}% {^E}Life Leech Resistance` |
| `tagCharStatsLifeLeechResistInfo` | `Resistance to life-draining attacks.` |

**Two things fall out and a third does not.**

1. **The basis is a *proportion of damage dealt*, with no per-event language.** "The percent of the damage you deal" is structurally per-damage, hence per-hit, hence per-body. A capped or primary-only rule would be a *lie* in this string, and Crate writes precise stat glosses (compare the `HealIncrease` gloss, which carves out regeneration explicitly).
2. **No multi-target qualifier exists anywhere in 20,394 tags.** Searched `each enemy` / `per enemy` / `multiple target` / `additional target` / `per target` / `enemies hit` / `targets hit` on **values as well as keys**: **one** hit, and it is Phantasmal Blades' flavour text. **Recorded so the negative is on the record.**
3. ⚑ **What it does NOT settle: "weapon attack damage" is ambiguous** between *the damage dealt by a weapon attack* (total, including EoR's flat adders) and *the weapon-damage portion*. Both readings are grammatical. **`SOURCE-UNLOCATED`** — and § 5.3 shows it does not rescue the oracle either way.

### 1.4 `Global` and `XOR` are affix-roll flags, not leech scoping

`offensiveLifeLeechGlobal` / `offensiveLifeLeechXOR` look like they might scope the stat. They do not: **the identical `{Chance, XOR, Global}` triple appears on every one of the ~30 offensive stat groups** (`offensiveBaseColdGlobal`, `offensivePhysicalXOR`, …) alongside one record-level `offensiveGlobalChance`. A flag present on every group cannot encode a leech-specific rule. Crate's descriptions for the whole group are **empty strings**, so the exact roll semantics are `SOURCE-UNLOCATED`; what is established is only the negative — **they are not a multi-target scope.**

---

## 2 · (3) — EoR's ticks are attacks, and (4) — what the leech rides

**(3)** C-7 § 2.2 established `SkillChanneled.tpl` → `Skill_Activated.tpl`. The same include list carries **`Skill_Attack.tpl`** and `Skill_Spell.tpl`. EoR holds `weaponDamagePct` — the field that *makes* a skill a weapon attack — at 43 (skill) + 14 (Gutsmasher `mace2h_d107_eyeofreckoning.dbr`) = **57 %**, clamp not reached (`adcth_clamped_at_100 = no`). **Each of the ~11.4 ticks/s is a discrete weapon attack.** No other reading is available in the schema.

**(4)** EoR rank 20 carries `offensivePhysicalMin/Max = 109/122` and `offensiveFireMin = 90` (the Soulfire limb) as **flat skill adders**, and **carries no `offensiveLifeLeech*` of its own** — the player's 21 % is a global character stat reached through `parameters_character.tpl`, not a skill property. Under the char-sheet gloss the ADCtH basis is the **weapon** line. Lap Q's inversion (§ 5.3) recovered exactly that line, which is an empirical vote for the portion reading — **reported as corroboration, not as a decode.**

---

## 3 · The referent, re-measured — the equilibrium the oracle does not reproduce

Recomputed **fresh this lap** from Lap Q's committed 60 Hz HP trace (10,861 rows; `health_max` 20,005, with the `D-Q1` 16,368 episode carried as-is), by summing signed frame-to-frame deltas:

| wave | dur (s) | Σ heal (HP) | Σ intake (HP) | **heal : intake** | heal/s | intake/s |
|---|---:|---:|---:|---:|---:|---:|
| 151 | 15.58 | 19,032 | 19,032 | 1.00 | 1,221 | 1,221 |
| 152 | 16.30 | 12,480 | 16,117 | **0.77** | 766 | 989 |
| 153 | 14.90 | 24,403 | 20,766 | 1.18 | 1,638 | 1,394 |
| 154 | 14.20 | 36,484 | 38,230 | 0.95 | 2,569 | 2,692 |
| 155 | 16.20 | 18,045 | 16,512 | 1.09 | 1,114 | 1,019 |
| 156 | 20.20 | 33,503 | 33,290 | 1.01 | 1,659 | 1,648 |
| 157 | 19.30 | 41,214 | 41,832 | 0.99 | 2,135 | 2,167 |
| 158 | 13.00 | 4,366 | 3,748 | 1.16 | 336 | 288 |
| 159 | 26.30 | 60,106 | 60,963 | 0.99 | 2,285 | 2,318 |
| **160** | **25.00** | **102,604** | **101,747** | ⚑ **1.01** | **4,104** | **4,070** |
| **all** | **181.02** | **352,237** | **352,237** | ⚑ **1.000** | 1,946 | 1,946 |

> ⚑ **The referent is a system in EXACT equilibrium.** Ten consecutive waves, every ratio in **[0.77, 1.18]**, the whole fight at **1.000**.
>
> **Against: port 24.1 (KP-93) · oracle median 132.69, ~72.5 after the missing ×1.830 (KP-86 F-1).**

**The caveat that must travel with this table, stated first and not buried: an HP trace CANNOT see heal at the cap.** 42.84 % of frames sit at full health, so **every figure in the heal column is a LOWER BOUND** and the ratio is not a measurement of gross leech. It *is* a measurement of **net survival pressure**, and § 5.1 supplies the unclipped instrument.

---

## 4 · The tick census — the unclipped instrument

Lap Q's 129 leech ticks (step ≥ 50 HP, deficit ≥ 3,000 so the cap cannot bind, step not landing on the cap), re-queried here.

### 4.1 Distribution

| | min | p25 | median | p75 | max |
|---|---:|---:|---:|---:|---:|
| all 129 | 54.8 | 310.8 | **782.8** | 1,303.8 | **8,541.8** |
| clean 67 | 60.8 | 370.8 | **820.8** | 1,330.8 | 5,468.8 |
| wave 160 (56) | 289.8 | — | **910.3** | — | 8,541.8 |

### 4.2 Histogram (500-HP bins, all 129) — smooth, monotone, long-tailed

```
    0- 499 | 49  #################################################
  500- 999 | 34  ##################################
 1000-1499 | 20  ####################
 1500-1999 |  9  #########
 2000-2499 |  8  ########
 2500-2999 |  3  ###
 3000-3499 |  2  ##
 3500-3999 |  1  #
 4500-4999 |  1  #
 5000-5499 |  1  #
 8500-8999 |  1  #
```

### 4.3 ⚑ What the shape excludes

> **A hard per-activation or per-tick heal cap would produce a PILE-UP at the cap value.** There is none. The distribution decays monotonically over a **156× range** (54.8 → 8,541.8 HP) with a single unbounded tail observation.
>
> **VERDICT: no per-tick heal cap binds anywhere below 8,542 HP in the referent.** Graded `MEASURED-BOUND`, not `MEASURED-ABSENT` — a cap above 8,542 is untested and unlikely to matter, since 8,542 is 42.7 % of the player's max health **in one tick**.

---

## 5 · ⚑ THE DISCRIMINATION — and it lands on the occupancy, not the law

### 5.1 Two independent instruments, one answer

**Instrument A — inverting the tick magnitude.** Lap Q's identity, unchanged:

```
step = ADCTH 0.21 × WD-fraction 0.57 × heal-increase 1.22 × leech_mult × D_weapon × N_bodies
```

Per-body heal at wave 160 under the **COUPLED** arm (Lap Q § 5.5 verdict; `pm4p_leech_resistance.csv`, 790 bodies): non-zero **median 561.0** at the sheet's LO weapon line and **1,435.6** at HI; board max 2,092.0; **6.2 % of bodies return zero.** Dividing each observed tick by those:

| implied `N` per tick, all 129 | min | p25 | median | p75 | p95 | max | **mean** |
|---|---:|---:|---:|---:|---:|---:|---:|
| at **LO** weapon line | 0.10 | 0.59 | **1.40** | 2.30 | 5.13 | 15.23 | **1.84** |
| at **HI** weapon line | 0.04 | 0.23 | **0.55** | 0.90 | 2.01 | 5.95 | **0.72** |

Wave 160 alone: mean implied `N` = **0.98 (HI) – 2.52 (LO)**.

**Instrument B — the nameplate ring census** (Lap H-2 `pm4h2_ring_density.csv`, contact = plate anchor within 150 ground px, **declared LOWER BOUND**):

| wave | mean contact | median | p90 | max |
|---|---:|---:|---:|---:|
| 159 | 1.78 | 1 | 4 | 9 |
| **160** | **1.66** | **1** | **4** | **8** |
| whole fight | 1.31 | 1 | 3 | 10 |

> ⚑ **THE ORACLE SAYS 5.62 MEAN, MODE 5 (75.5 % of ticks), MAX 8. THE REFERENT SAYS MEAN 1.66, MODE 1, MAX 8.** Two instruments built on different physics — OCR'd HP arithmetic and nameplate geometry — **independently return ≈ 1–2 where the oracle returns 5.62.** The maxima agree exactly (8); the *distribution* does not.
>
> **And the bias runs the right way.** Ticks are only *observable* when the player has a deficit, i.e. at the moments of heaviest contact, so instrument A is biased **high**. Instrument B is a declared lower bound, biased **low**. **They converge from opposite directions on the same answer.**

**Grade-honest limit:** `OBS-H2-9` declares the **ground-px → metre conversion UNRULED**, so R150 cannot be pinned against EoR's 3.0 m disc. I decline the conversion, as Lap H-2 did. The ring census is therefore corroboration of instrument A, **not** a metric measurement of the 3.0 m disc.

### 5.2 Which candidate shapes the footage EXCLUDES

Predicted gross leech = `11.408 ticks/s × N × per-body`, against the referent's **unclipped** peak recovery from Lap Q's five pre-registered maximum-healing windows (damage-corrected, deficit ≥ 3,000 so no clipping): **4,289 – 10,690 HP/s**.

| N | predicted heal (HP/s) | vs observed peak 4,289–10,690 |
|---|---:|---|
| **1.00** | 6,400 – 16,377 | ✅ **brackets it** |
| 1.66 (referent census) | 10,624 – 27,186 | ✅ upper edge |
| **5.62 (ORACLE)** | **35,967 – 92,041** | ❌ **3.4× – 21× ABOVE the referent's best window in the whole fight** |

| candidate shape | verdict from the footage |
|---|---|
| **full per-target credit, no cap** | ⚑ **NOT EXCLUDED — and it is the only shape positively supported.** The tail requires it: the largest tick, 8,541.8 HP, is **4.08×** the best single body's HI ceiling (2,092). Multi-body credit demonstrably happens. |
| **per-activation / per-tick cap** | ⚑ **EXCLUDED below 8,542 HP** (§ 4.3, no pile-up) **and has no field to live in** (§ 1.1). |
| **per-second heal cap** | ⚑ **EXCLUDED below ~10,690 HP/s**; no field exists (§ 1.1). |
| **primary-target-only (N ≡ 1)** | ⚑ **EXCLUDED at 2.6×–4.1×.** Largest clean tick 5,468.8 = **2.61×** the best wave-160 body's HI ceiling; largest tick 8,541.8 = **4.08×**. **Caveat named, not smoothed:** the sheet carries `critical_damage = +57 %` and `combatformulas.dbr` a PTH ladder topping at `pthDamageModifier6 = 1.5`; whether the camera-measured weapon bracket [16,972, 40,930] already spans those is **not established**, so this exclusion is **strong, not absolute.** |
| **per-target diminishing** | ⚠ **NOT EXCLUDED.** No field expresses it (§ 1.1) and the footage cannot separate "8 bodies diminished" from "2.6 bodies at full credit." **A *severe* diminishing rule (primary + a token remainder) is excluded by the same 2.6–4.1× tail.** Mild-to-moderate diminishing survives. **Declared open; do not close it by plausibility.** |
| **engine-level heal cap per unit time** | ❌ `SOURCE-UNLOCATED` in principle (no binary), **bounded** at ≥ 10,690 HP/s in practice. |
| ⚑ **the ORACLE's 5.62 bodies-in-disc** | ⚑ **EXCLUDED, 3.4×–21×, by the one window in the entire fight where the referent healed hardest.** |

### 5.3 Could each shape produce a player who DIES at wave 160?

Measured intake at wave 160: **4,070 HP/s** (also a lower bound — heal masks decrements). Max health 20,005.

- **Full per-target @ N = 5.62:** heal 35,967 – 92,041 HP/s. To die, a burst must beat that for long enough to cross 20,005 HP — an intake spike of **9×–23× the wave's measured mean**. ⚑ **CANNOT PRODUCE THE OBSERVED DEATH.**
- **Full per-target @ N ≈ 1–1.7 (the referent's own occupancy):** heal 6,400 – 27,186 HP/s against 4,070 HP/s mean intake — a surplus in the single digits, **and the measured net ratio is 1.01.** Deep excursions are observed (HP min 5,360 = 26.8 % of max; 13.73 % of frames are decreasing; 1.00 % below 33 %). ⚑ **CONSISTENT WITH DEATH AT 29.0 s.**
- **Primary-only / capped / severely-diminished:** would fall *below* the referent's measured recovery and are excluded from the other side (§ 5.2).

> ⚑ **The law survives the footage. The occupancy does not.** Because `heal ∝ N` exactly, **the oracle's 3.4× occupancy error is a 3.4× heal error on its own**, and it composes multiplicatively with KP-86's missing ×1.830 on the intake side. Together those two are ~6.2× of a surplus KP-95 sizes at ~72.5×. **They are not the whole gap — but they are the two that are now MEASURED, and neither requires inventing a rule.**

### 5.4 ⚑ Where the occupancy error most likely comes from — named as a HYPOTHESIS, folded by nobody

`kc2/locomotion.py` records that the oracle's record limb drives the player at the densest live cluster, with the objective **derived from the leech identity itself** (`sustain = ADCtH% × Σ_{j∈disc} min(D, hp_j)`) — a policy that *maximises the very quantity in dispute*. `CLUSTER_SEEK` even "arrives and dwells."

Against that, Lap H-2 measured the referent: **0.883 of fight time in significant motion**, 107 movement bouts, 34 dash-class events, median bout 1.03 s.

⚑ **And the counter-evidence, reported because omitting it would be dishonest:** Matt's own account, quoted in that same file — *"I kited multiple packs into a single area to max leech/tick."* **He was deliberately stacking bodies, and he still died.** The reconciliation the data offers is that stacking produced the **tail** (implied N up to 6–15, max clean tick 5,469) and not the **mean** (0.72–1.84). **A policy that dwells at the centroid converts an occasional tail into a sustained mean, and that is a 3.4× on the heal.** ⚑ **Stated as the leading unexcluded hypothesis for the occupancy gap. It is NOT measured and must not be folded as though it were.**

### 5.5 A field-identity thread found in passing, handed over rather than acted on

`pm4p_leech_resistance.csv` — my own Lap P table, consumed by the oracle — keys "Life Leech Resistance" to **`defensiveSlowLifeLeach`**. This lap confirms **that is the only candidate: no `defensiveLifeLeech` field exists in the game.** `parameters_defensive.tpl`'s "Defensive Special" group holds exactly one life-leech resistance family (`defensiveSlowLifeLeach` + `Duration` + `MaxResist` + the chance/modifier twins), and the client's `DefenseLifeLeach*` tag family maps onto it 1:1. **So the `U-P-N-1` COUPLED verdict is not resting on a mis-identified field** — the "Slow" in the name is legacy TQ vocabulary, not a scope. **Recorded to close a doubt, not to reopen one.**

---

## 6 · The external surfaces

> **Verification discipline:** the sweep was run as a delegated pass; **every quote graded OFFICIAL below was then re-fetched and re-read by me at its own URL before being granted that grade.** Staff identity was established programmatically, not by reputation: `forums.crateentertainment.com/u/Zantai.json` returns `title: "Crate Employee - Designer"`, `groups: ["Crate_Employee"]` (same for `medierra`). `medea_fleecestealer` is a Super Moderator and **not** in `Crate_Employee` — community tier.

### 6.1 ⚑ The official guide states the ADCtH rule — and it splits it by SOURCE

`https://www.grimdawn.com/guide/gameplay/combat/`, Crate's own domain, **§ "Life Steal", accessed and re-verified by me 2026-09-29, verbatim**:

> "Percent of Attack Damage Converted to Health is a form of life steal available in Grim Dawn."
> **"When on equipment, life steal applies only to your weapon attacks."**
> **"If you use a skill with % Weapon Damage, the life steal applies as if you attacked with your weapon, scaling with the % Weapon damage."**
> **"In either case, only the direct damage is considered for life steal."**
> "Damage over Time, such as Bleed or Poison, does not trigger it."
> **"When found on a skill, Percent of Attack Damage Converted to Health applies to all of that skill's direct damage."**
> **"Note that % Weapon damage beyond 100% on skills will not scale life steal any further."**

and § "% Weapon Damage":

> "What this means is that the skill takes the damage and effects you would deal on a regular attack and multiplies it by the displayed %."
> "This includes things such as life steal, bonus magical damage and chance on attack item skills."

> ⚑ **THE EQUIPMENT / SKILL SPLIT MAPS 1:1 ONTO MY OWN LAP P `scope` COLUMN, AND CRATE RATIFIES THE SPLIT LAP P MADE.** `pm4p_adcth_sources.csv` classifies every source as `GLOBAL-WEAPON-ATTACKS` or `SKILL-SCOPED` and sums **only** the former into the 21 %. The five summed sources — Solael-Sect Legguards, Restless Remains, Scales of Ulcama, Dire Bear, Toad — are **all gear or devotion passives**, i.e. Crate's "on equipment" case, which *"applies as if you attacked with your weapon, scaling with the % Weapon damage."* **That is `weapon_portion_raw = 0.57 × D_weapon` — the oracle's incumbent basis, now `OFFICIAL-GUIDE-VERBATIM` instead of inferred.** Tip the Scales (132 % at rank 20) and Maul (45 %) are the `SKILL-SCOPED` case and correctly excluded from the EoR channel's sum.
>
> ⚑ **And the 100 %-WD clamp is Crate's ONLY published cap in the entire leech system — a cap on the RATE, not on healing per activation.** Lap P implemented it over the whole attack table and declared it **inert on the record channel** (EoR is 57 %). Confirmed correct.

### 6.2 The one refinement Crate adds to the basis — and its direction

Zantai (Crate Employee - Designer), `https://forums.crateentertainment.com/t/suggestion-chaos-sabo-could-definitely-use-some-love/105007/33`, **re-verified by me**, verbatim:

> "Flat damage would scale with any leech applied from your weapon damage."
> "As it does have % Weapon damage, any damage it deals will leech proportionally to the % Weapon damage it has."
> "As it has no % Weapon damage, it does not leech."

and at `/37`: *"Flat damage from basic modifiers is added to the base skill, so it does apply leech from the base skill's % Weapon damage."*

> ⚑ **Consequence for (4), stated as a bracket and not as a fold:** EoR's own `offensivePhysicalMin/Max = 109/122` and `offensiveFireMin = 90` (the Soulfire limb) **do join the leech basis**, at the base skill's 57 % — they are not excluded as "not weapon damage." **Direction: UP.** The oracle's basis is therefore a **lower** bound, which pushes every implied-`N` figure in § 5.1 **DOWN** and strengthens § 5.2 rather than weakening it. **Sizing it is gamora's, not mine — I decline to compute a factor from a sheet line I did not measure.**

### 6.3 ⚑ Crate confirms Life Leech Resistance reduces ADCtH — `U-P-N-1` is closeable

Zantai (Crate Employee - Designer), official patch notes, **both re-verified by me**:

> `https://forums.crateentertainment.com/t/grim-dawn-version-v1-2-0-0-v1-2-0-1-v1-2-0-2-v1-2-0-3-hotfixes/132117/1`
> **"Increased Monster % Life Leech Resist. This makes % Attack damage Converted to Health less effective. On Ultimate difficulty, this is roughly a 30% reduction against an average boss."**

> `https://forums.crateentertainment.com/t/grim-dawn-version-v1-3-0-0-hotfixes/155979/1`
> "Reduced Monster % Life Leech Resist on Ultimate difficulty. This makes % Attack damage Converted to Health roughly 16% more effective against an average boss."

and, separating the two stats while keeping the shared resistance (v1.0.2.0):
> "Replaced all sources of flat and % Life Leech damage and retaliation on equipment and skill procs. Note: this does not affect sources of Attack Damage Converted to Health, which remain unchanged."

> ⚑ **Lap Q measured `U-P-N-1 = COUPLED` off the referent's own frames on 2026-08-14 under a pre-registered rule. Crate had said the same thing in a patch note.** The bracket that has been open since Lap P is now carried by **two independent surfaces of different kinds** — a measurement and the developer's own words. **Recommend `U-P-N-1` be CLOSED as COUPLED.** § 5.5 disposes of the last doubt (the field identity).
>
> ⚑ **Note the direction of the 1.2.0.0 change:** Crate's answer to over-performing life steal was **monster Life Leech Resist**, *not* a cap and *not* a multi-target rule. That is the design position § 1.1 reads off `gameengine.dbr`, stated in Crate's own voice.

### 6.4 ❌ THE NEGATIVE — and it is the commission's central answer from this surface

> ⚑ **CRATE HAS PUBLISHED NOTHING, ANYWHERE, ABOUT WHAT HAPPENS WHEN ONE ACTIVATION HITS N TARGETS.** Not per-target crediting, not a per-activation cap, not diminishing returns on secondary targets, not a primary-target rule.

**Searched, so the negative is a result:**

| surface | what was done | outcome |
|---|---|---|
| **grimdawn.com official guide** | `/guide/gameplay/combat/`, `/guide/items/`, `/guide/character/character-basics/`, `/guide/game-difficulties/`, `/guide/gameplay/monsters/` — raw HTML grepped for `leech\|life steal\|converted to health` | only `/combat/` carries the rule (§ 6.1). **No mention of multiple targets, target count, or per-attack caps anywhere.** |
| **forums.crateentertainment.com** | ~30 Discourse `/search.json` queries, exact-phrase + `@author` filtered, incl. `"attack damage converted to health" "per target"`, `"lifesteal is capped"`, `"life steal is capped"`, `"life steal" "diminishing" @Zantai`, `"life steal" "primary target"`, `lifesteal "number of enemies"`, `"Eye of Reckoning" lifesteal @Zantai`, `"Blade Arc" lifesteal @Zantai`; plus Zantai's post history date-sliced | **zero dev hits.** `"attack damage converted to health" "per target"` and both `"…is capped"` forms return **0 results from anyone**. |
| **the eight threads that ask this exact question** | read post-by-post via Discourse JSON — incl. `eye-of-reckoning-not-affected-by-lifesteal/91720`, `eye-of-reckoning-and-life-steal/49241` (24 posts), `mechanics-question-flames-of-ignaffar-and-lifesteal/102179`, `life-steal-and-total-damage/29830` | ⚑ **NOT ONE contains a Crate-staff post.** The community argues it out unresolved; Crate has never entered. |
| **`defensiveSlowLifeLeach`** (the internal stat name) | forum search | 8 results, **all community/modders**; no Crate post ever uses the internal name. |
| **Official Grim Dawn Wiki (Fandom)** | `grimdawn.fandom.com/wiki/Game_Mechanics` | ❌ **HTTP 402 via fetch, HTTP 403 via curl.** Not retrievable — **the same block C-7 § 0 recorded.** `grimdawn-archive.fandom.com` also 403; `grimdawn.wiki.fextralife.com/Life+Steal` connection failed. |

**Community material, labelled and cited for nothing.** The only multi-target claim anywhere is a non-staff post on the EoR thread (`…/91720/2`, user `rmsinj`, trust level 2): *"this is AOE skill, so you should notice it when get into pack of mobs (each one counts, multiplying your lifesteal value)."* ⚑ **It agrees with my § 1.1 / § 5.2 conclusion and it is NOT evidence for it.** Law 3 governs inside a commission: *"the community says roughly"* is not a value, and it is not a law either. **Recorded so that a later reader can see it was found, weighed, and declined.**

**Suggestive-only, flagged rather than used.** Zantai, `https://forums.crateentertainment.com/t/some-feedback-after-750h/85411/16`, refusing to extend ADCtH devotions to spells: *"It would fundamentally affect game balance and require major changes, especially for AoE skills."* **Crate regards AoE life steal as the pressure point — which tells us they know the interaction is strong, and tells us nothing about its arithmetic.** Not a source for any row.

⚑ **One instrument caution, recorded because it is the C-7 § 7 lesson in a new place:** the general web-search tool's prose summaries asserted a multi-target rule outright (*"AoE skills generate more lifesteal heals per cast"*). **That is model synthesis of snippets, not a quotable source**, and it was correctly refused. A search tool that returns a confident sentence is not a source that said it.

---

## 7 · Rows a consumer can take

| row | value | grade | cite |
|---|---|---|---|
| multi-target ADCtH law — target cap | ⚑ **none exists** | `DB-EXHAUSTIVE-ABSENCE` (all 8 archive string tables) | § 1.1 |
| — per-activation / per-tick heal cap | ⚑ **none exists in data**; **no cap binds below 8,542 HP** in the referent | `DB-EXHAUSTIVE-ABSENCE` + `MEASURED-BOUND` | § 1.1, § 4.3 |
| — per-second heal cap | **none exists in data**; none binds below ~10,690 HP/s | `DB-EXHAUSTIVE-ABSENCE` + `MEASURED-BOUND` | § 1.1, § 5.2 |
| — per-target diminishing | **no field**; **severe forms excluded**, mild forms **OPEN** | `DB-EXHAUSTIVE-ABSENCE` / `UNDECIDED` | § 5.2 |
| — primary-target-only | ⚑ **EXCLUDED at 2.6×–4.1×** (crit caveat named) | `MEASURED-EXACT` | § 5.2 |
| — engine-level clamp outside the data layer | ❌ **not recoverable** (no binary on disk) | **searched `SOURCE-UNLOCATED`** | § 0 |
| ⚑ **Crate's published position on multi-target ADCtH** | ⚑ **NOTHING EXISTS.** Guide grepped, ~30 forum queries, 8 on-topic threads read post-by-post — **no Crate-staff post has ever entered the question** | ⚑ **searched `SOURCE-UNLOCATED`** (was *unsearched*) | § 6.4 |
| ADCtH rate — the only cap Crate publishes | **%WD clamped at 100 %** — a cap on the RATE, **not** on healing per activation; **INERT here** (EoR = 57 %) | `OFFICIAL-GUIDE-VERBATIM` | § 6.1 |
| ADCtH basis, **equipment-sourced** (all 5 summed sources) | *"applies as if you attacked with your weapon, scaling with the % Weapon damage"* → **the oracle's incumbent `0.57 × D_weapon` is RATIFIED** | **`OFFICIAL-GUIDE-VERBATIM`** | § 6.1 |
| ADCtH basis, **skill-sourced** (Tip the Scales, Maul) | *"applies to all of that skill's direct damage"* — a **different rule**, correctly excluded from the EoR sum by Lap P's `scope` column | `OFFICIAL-GUIDE-VERBATIM` | § 6.1 |
| ADCtH and damage-over-time | ⚑ **DoT never triggers it** — *"only the direct damage is considered"* | `OFFICIAL-GUIDE-VERBATIM` | § 6.1 |
| EoR's flat adders (`offensiveFireMin 90`, `offensivePhysicalMin 109`) | **DO join the basis** at the base skill's %WD (Zantai). **Direction UP → implied `N` moves DOWN.** Magnitude is gamora's to size | `OFFICIAL-DEV-POST` / magnitude `UNSIZED` | § 6.2 |
| ⚑ **`U-P-N-1` — Life Leech Resistance gates ADCtH** | ⚑ **COUPLED, now on TWO independent surfaces:** Crate's v1.2.0.0 patch note **and** Lap Q's pre-registered measurement. **RECOMMEND CLOSED.** | **`OFFICIAL-PATCH-NOTE` + `MEASURED-EXACT`** | § 6.3, § 5.5 |
| EoR target-cap field | **ABSENT** from the include chain | `TEMPLATE-CITED` | § 1.2 |
| EoR hits the full disc, not a swept arc | **no arc field is expressible** | `TEMPLATE-CITED` | § 1.2 |
| EoR channel tick is a weapon attack for ADCtH | **YES** (`Skill_Attack.tpl` in chain; `weaponDamagePct` 57 %) | `TEMPLATE-CITED` | § 2 |
| ADCtH basis | **weapon attack damage**, per the game's own stat gloss | `UI-STRING-CITED` | § 1.3 |
| — "total of a weapon attack" vs "weapon-damage portion" | ❌ **not stated by any source**; the portion reading is corroborated by Lap Q's inversion | `SOURCE-UNLOCATED` / `MEASURED-CORROBORATED` | § 1.3, § 5.3 |
| ⚑ **referent mean bodies-in-disc, wave 160** | ⚑ **1.66** (ring census, lower bound) · **0.98–2.52** (HP-tick inversion) | **`MEASURED-EXACT`** ×2 | § 5.1 |
| ⚑ **oracle mean bodies-in-disc, wave 160** | **5.62** — **EXCLUDED by the footage, 3.4×–21×** | `MEASURED-EXACT` (KP-95) vs `MEASURED-EXACT` | § 5.1–5.2 |
| ⚑ **referent heal : intake, wave 160** | ⚑ **1.01** (102,604 : 101,747 HP over 25.00 s) | `MEASURED-EXACT` (clipped lower bound on heal) | § 3 |
| ⚑ **referent heal : intake, waves 151–160** | ⚑ **1.000** (352,237 : 352,237 HP over 181.02 s) | `MEASURED-EXACT` (same caveat) | § 3 |
| referent **unclipped** peak gross recovery | **4,289 – 10,690 HP/s** | `MEASURED-EXACT` (Lap Q, 5 pre-registered windows) | § 5.2 |
| `playerReflectCap` | **30.0** — Crate caps retaliation and **not** leech | `DB-CITED` | § 1.1 |
| `meleeTargetDistance` | **2.4** m — independently corroborates KP-93's `d_engage_m` | `DB-CITED` | § 1.1 |

---

## 8 · What the seams would fold — **proposed, not ordered; the conductor issues**

**gamora (oracle) — three folds and one refusal:**

1. ⚑ **DO NOT ADD A CAP.** Keep `n_caps_applied == 0` on the assert wall. § 1.1 upgrades Lap P's *"MEASURED-ABSENT from `parameters_offensive.tpl` and `gameengine.dbr`"* to an **exhaustive absence over the complete field vocabulary of all 8 archives**, and § 4.3 shows none binds in the referent below 8,542 HP. **The `no-cap` posture is now the best-sourced thing in the sustain fold.**
2. ⚑ **The defect is the OCCUPANCY, and it is now a measured target, not a bracket.** `5.62` at wave 160 is excluded by the referent at **3.4×–21×**; the referent's own figure is **1.66** (ring census, lower bound) / **0.98–2.52** (HP-tick inversion). The **leading unexcluded cause** is the cluster-seeking drive limb whose objective is derived from the leech identity itself (§ 5.4) — **a hypothesis, not a finding.** The honest next instrument is a `DRIVE_TO_PACK` / hold comparison on bodies-in-disc against **1.66**, not a tuning constant.
3. **Close `U-P-N-1` as COUPLED** on Crate's v1.2.0.0 patch note plus Lap Q (§ 6.3). The field-identity doubt is disposed of in § 5.5.
4. **Size, do not assume, the § 6.2 basis rider** — EoR's flat 109/122 physical + 90 fire join the leech basis at 57 %. It moves the basis **UP** and implied `N` **DOWN**; it does not rescue the surplus.

**drax (port) — one fold and one warning:**

1. `kc2rt_fight.gd:1320`'s per-body, uncapped accumulation is **faithful to the referent's law** and should not be changed. The port's own post-repair occupancy of **0.803** (KP-93, one seed, one scripted hand) is *below* the referent's 1.66 — ⚑ **the port and the oracle disagree about occupancy by ~7×, and the referent sits between them.** That is the number to converge, not the leech loop.
2. ⚑ **Warning against the obvious cheap fix:** capping targets or heal in the port to make it survivable would encode a rule Grim Dawn does not have, and would be **unfaithful in a way the footage can detect** — the tail (a single 8,542 HP tick, 42.7 % of max health) requires multi-body credit to exist.

**star-lord (pack):** nothing this lap. No new constant is minted; every number here is either already in the pack or a re-query of committed evidence.

---

## 9 · Operational notes

- **Free disk 43 GiB at open.** This lap wrote ~40 KB (this file + a scratch dir of symlinks). **The MP4 was never opened and nothing was copied.** ⛔ The HALT is respected; the disk is unchanged by this commission.
- **Tooling:** `legolas/scratch/2026-09-29-c8-multitarget-leech/` — four **symlinks** to the C-7 readers (`arz.py`, `arcread.py`, `tags.py`, `scan_fields.py`), **unmodified**. No new code was banked; every computation in § 3–§ 5 is a one-shot re-query over committed CSVs and is reproducible from the commands in this file's own text.
- ⚑ **Method note worth keeping — the ARCHIVE STRING TABLE is the cheap exhaustive-absence instrument.** C-7 recommended reaching for the templates on any *"what does this field MEAN"* question. This lap adds the complement: on any *"does a field for X exist AT ALL"* question, sweep the 8 string tables. It costs one pass with **no record decompression**, it is complete by construction, and it converts "we looked and didn't find it" into "the vocabulary does not contain the concept." **That is the difference between an unfound cap and an absent one, and it is the whole evidentiary weight of § 1.1.**
- ⚑ **A commission that could only succeed would have manufactured a cap.** C-8 named six candidate shapes and asked me to discriminate. Five are excluded or absent; the sixth — the incumbent — survives. **The answer to "which law reduces the heal" turned out to be "none of them; the body count does."** Recorded plainly because the conductor's brief, correctly, made a negative a result.

---

**Filed by:** legolas (UNKNOWN-RESEARCHER), 2026-09-29, Run KC2-PLAY. Read-only throughout. Committed with an explicit file list; **did not push — the conductor releases.**
