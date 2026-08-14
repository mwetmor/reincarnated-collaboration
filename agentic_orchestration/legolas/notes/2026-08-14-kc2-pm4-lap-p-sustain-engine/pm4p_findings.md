# KC2-PM4 · Lap P · FINDINGS — THE SUSTAIN ENGINE

> **Run:** KC2-PM4 · **Seat:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-14
> **Laws:** READ-ONLY on every source · **GL-12 decode-never-estimate** · **GL-6 full 64-hex digests**
> **NOTE-9** every quantity asserts its own basis · **R-PM4-25** LO/HI for monotone scalars only;
> structural unknowns take pre-registered mechanism candidates (**U-P-N**) published as BOTH limbs,
> never averaged · **OUTCOME-FIREWALLED**.
> **Instrument:** `agentic_orchestration/research/scripts/pm4p_emit_2026_08_14.py`

---

## 0 — The firewall, stated precisely

This lap read **no** sim output, **no** gamora landing note, **no** baton, **no** wave-duration / ToD /
player-HP track, and **no** part of the gandalf run charter's scorecard. Its substrate is exhaustively:

| source | used for |
|---|---|
| `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` (8 `.arz`, `Text_EN.arc`, `templates.arc`) | every field identity and magnitude |
| `/Volumes/reincarnated/matt-notes-from-pc/gd-save/_EoRWarlGuts/player.gdc` — sha256 `b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5`, 98,101 B | allocations, devotion levels, equipment |
| Lap A `measured-player-sheet.csv` | the camera-measured character sheet (corroboration **and** three run-of-record scalars) |
| Lap G `pm4g_defensive_actives.csv` | the ratified devotion-rank law and the proc bindings (referenced, **not** re-decoded) |
| Lap L `pm4l_eor_per_hit.csv`, `pm4l_mitigation_by_body.csv` | EoR rank/`%WD` chain; per-body armour / absorption / physical resist |
| Lap D `pm4d_band_b_ehp_by_wave.csv` | the 151–170 body board |
| **external, cited inline** | Crate's own combat guide + community mechanics threads, for the composition law the corpus does not declare |

Nothing here is fitted to any observed clear time.

---

## 1 — The one-paragraph answer

**The reference player's continuous sustain is one mechanism carrying essentially all of the load, and
it is not health regeneration.** Permanent global **Attack Damage Converted to Health is 20 % by the
table walk / 21 % by the game's own sheet**, assembled from **exactly five sources** (two gear, three
devotion stars) — and **44 further points of ADCTH exist in his own records and are INACTIVE**, a trap
a "sum everything" pass walks straight into. That ADCTH reaches the board through the
**weapon-damage fraction of Eye of Reckoning, decoded at 57 %** (43 % skill at rank 20 + 14 % from the
Gutsmasher's EoR modifier), at a hit cadence of **11.387–12.250 hits per second**, against an
**uncapped, purely geometric** target set (`Skill_AttackRadiusSpin` declares **no** target-count field,
`skillTargetRadius = 3.0 m`). It is scaled by **+22 % Healing Increase**, which the game's own stat
tooltip says applies to ADCTH by name. Against that stands the finding this lap exists to produce:
**every enemy in the game carries a flat +65 % Life Leech Resistance on Ultimate difficulty, from
`balancingadjustment_mp+difficulty_enemies01.dbr[8]`** — and the wave-151–160 board layers per-record
resistance on top of it in a clean five-tier ladder topping out at **565–588 %**, at which the leech
returns **nothing at all**. Health regeneration, the only other continuous source, is **129.38 hp/s** —
between **55× and 141× smaller** than the leech at a single body.

---

## 2 — P1 · EVERY ADCTH SOURCE ON THE PLAYED CHARACTER

**Deliverable: `pm4p_adcth_sources.csv`** (32 rows; every record in the played configuration that
declares *any* sustain field, with its rank, array index, condition, uptime basis and active flag).

### 2.1 ⚑ The field identity, decoded — not spelled from memory

Four different fields in this corpus contain the substring `LifeLeech`/`LifeLeach`. Conflating any two
of them produces a wrong sustain model, so each was resolved to its printed tooltip through
`templates.arc` → `Text_EN.arc`:

| DBR field | tag | printed text | what it is |
|---|---|---|---|
| **`offensiveLifeLeechMin/Max/Chance`** | `DamageLifeLeech` | **“{%t0}% of Attack Damage converted to Health”** | **ADCTH — this lap's subject** |
| `offensiveSlowLifeLeachMin/Max` + `…DurationMin` | `DamageDurationLifeLeach` | “Life Leech” | a **damage-over-time damage type**, not lifesteal |
| **`defensiveSlowLifeLeach`** | `DefenseLifeLeach` | **“{%.0f0}% Life Leech Resistance”** | the resistance (§ 4) |
| `offensiveLifeMin/Max` | — | Vitality damage | unrelated |

Declared in `templatebase/parameters_offensive.tpl` / `…_defensive.tpl`. **There is no
`defensiveLifeLeech` field anywhere in the corpus** — `defensiveSlowLifeLeach` is the *only* candidate
resistance, which is what makes § 4's coupling question a real one.

### 2.2 The five permanent, global sources — and the total

| % | source | record | archive | index |
|---:|---|---|---|---|
| 5.0 | **legs** — Solael (base item) | `records/items/gearlegs/b002e_legs.dbr` | base | scalar |
| 3.0 | **hands: component** — Restless Remains | `records/items/materia/compa_restlessremains.dbr` | base | scalar |
| 5.0 | **devotion** — Scales of Ulcama | `records/skills/devotion/tier2_02d.dbr` | base | scalar |
| 4.0 | **devotion** — Dire Bear | `records/skills/devotion/tier2_05e.dbr` | base | scalar |
| 3.0 | **devotion** — Toad | `records/skills/devotion/tier1_42c.dbr` | gdx1 | scalar |
| **20.0** | **TABLE SUM** | — | — | additive within field |

* **Check `P1-adcth-table-vs-sheet` — RESIDUAL-DECLARED.** The game's own sheet (Lap A, frame 513)
  prints **`Life Steal 21 %`**. The equipped-record walk reaches **20**. **1-point residual, declared,
  not smoothed** — see gap **D-P1**.
* **Additivity is the game's own statement**, not an assumption: *“If you have multiple sources of
  'attack damage converted to health', they will add together.”*
  (<https://www.grimdawn.com/guide/gameplay/combat/>)
* The whole-corpus census settles two things by absence: `offensiveLifeLeechMax` occurs in **exactly one
  record in 84,829** (a sandbox test sword), and `offensiveLifeLeechChance` in four (none equipped).
  **This character's ADCTH is unconditional and single-valued — no roll, no proc chance.**

### 2.3 ⚑ 44 points of ADCTH that are IN HIS RECORDS AND DO NOT EXIST

Emitted `MEASURED-INACTIVE` rather than dropped, because this is the exact class of error a naive walk
makes — and it is worth more than double the real total:

| % | record | why it is dead |
|---:|---|---|
| 4.0 | `devotion/tier1_42c_petbonus.dbr` | Toad's **pet** bonus, reached via `petBonusName`. Heals pets, never the player. |
| 15.0 | `playerclass08/weaponpool01.dbr` (Reaping Strike) | reached via **waist base** `augmentSkillName1` — a **rank grant**, not a skill grant. **Necromancer is not allocated** (block 8: only `playerclass01` and `playerclass09` `_classtraining_*` carry rank). |
| 15.0 | `playerclass08/weaponpool01.dbr` | the same skill again via **chest base** `augmentSkillName3`. |
| 10.0 | `playerclass06/weaponpool01.dbr` (Feral Hunger) | via **waist base** `augmentSkillName3`; **Shaman not allocated**. |

`augmentSkillName*` is a *skill-specific rank grant*; `itemSkillName` is a *skill grant*. Reading the
first as the second is precisely how 44 phantom points get banked.

### 2.4 The two SKILL-SCOPED sources (they do **not** join the global total)

Crate's law has two cases; these are the second one — *“When found on a skill, Percent of Attack Damage
Converted to Health applies to all of that skill's direct damage.”*

| % | skill | record | rank | its own damage |
|---:|---|---|---:|---|
| **132.0** | **Tip the Scales** (Scales of Ulcama celestial power) | `devotion/tier2_02f_skill.dbr` | 20 | 310 vitality + **33 %WD**; cd 1.0 s; trigger `HitByEnemy` 33 % |
| **45.0** | **Maul** (Dire Bear celestial power payload) | `devotion/tier2_05f_skill_buff.dbr` | 20 | **305 physical flat**, 4.5 m radius, 5 s; trigger `AttackEnemy` 20 % via Vire's Might |

Both ranks are **Lap G's ratified devotion law**: a bound Celestial Power is read at its block-8
`devotion_level` (15 / 20 / 25 — and each such record's arrays are exactly that long), **not at rank 1**.
Reading them at rank 1 would have returned 85 % and 15 %. *Tip the scales in your favour, **sapping your
attackers of vitality and transferring it to you*** (`tagDevotionEffectB02Desc`) — the game says plainly
that this is a heal-to-player mechanism.

### 2.5 Healing-received modifiers — EXACT

| field | value | source | condition |
|---|---:|---|---|
| `characterHealIncreasePercent` | **22 %** | **Haven** `playerclass09/presenceofvirtue2.dbr` @ rank 10 | **PERMANENT** — modifier on the always-on Presence of Virtue aura |
| `characterHealIncreasePercent` | +24 % | **Resilience** `playerclass09/passive02.dbr` @ rank 3 | **CONDITIONAL** — `lifeMonitorPercent = 66`, i.e. below 66 % health |
| `characterPercentHealIncreaseModifier` | — | **MEASURED-ABSENT** on this character | — |

**Check `P1-healing-increase-table-vs-sheet` — EXACT.** Table 22 vs sheet `healing_increase = 22`.
Haven alone accounts for the entire printed stat; Resilience's +24 is a conditional add on top.

**That this scales ADCTH is the game's own text, not community lore:**
`tagCharStatsHealIncreaseInfo` = *“The percent bonus to all healing effects, **including Potions and
Attack Damage Converted to Health**. Does not increase Health Regeneration.”* Corroborated externally
(*“Healing increase increases ADCtH… however, it does not work on health regen.”*).

---

## 3 — P2 · THE COMPOSITION LAW AND THE ATTACK KIT

**Deliverable: `pm4p_attack_kit.csv`** (10 rows).

### 3.1 ⚑ The law, cited verbatim — the corpus does **not** declare it

`records/game/combatformulas.dbr` was dumped in full (44 fields). It carries the armour, PTH, crit and
attribute equations — and **no leech equation of any kind**. The composition rule is therefore
**MEASURED-ABSENT from the records** and is taken from Crate's own published guide,
<https://www.grimdawn.com/guide/gameplay/combat/>, quoted rather than paraphrased:

> “Percent of Attack Damage Converted to Health is a form of life steal available in Grim Dawn.”
> “**When on equipment, life steal applies only to your weapon attacks.**”
> “**If you use a skill with % Weapon Damage, the life steal applies as if you attacked with your weapon,
> scaling with the % Weapon damage.**”
> “**Note that % Weapon damage beyond 100 % on skills will not scale life steal any further.**”
> “When found on a skill, Percent of Attack Damage Converted to Health applies to all of that skill's
> direct damage.”
> “**Damage over Time, such as Bleed or Poison, does not trigger it.**”
> — and on `% Weapon Damage` generally: “the skill takes the damage and effects you would deal on a
> regular attack and multiplies it by the displayed %. **This includes things such as life steal.**”

Corroborated independently on the community side: *“if you have 10 % life steal, and a skill uses 50 %
weapon damage, then you will steal 5 % weapon damage”*
(<https://forums.crateentertainment.com/t/further-clarification-on-attack-damage-converted-to-health/39080>);
*“only the weapon damage part is used to calculate the amount of heal you receive… the ADCTH is also
modified by the percentage of weapon damage % if it is less than 100 %”*
(<https://forums.crateentertainment.com/t/attack-damage-converted-to-health-on-items-and-components/42048>).

**Therefore, emitted as the `adcth_leech_fraction` column:**

```
leech_fraction(skill) = min( total %WeaponDamage , 100 ) / 100
heal_per_hit          = ADCTH_total% × leech_fraction × (weapon-attack damage DEALT to that body)
                        × (1 + HealingIncrease/100) × f(target Life-Leech-Resistance)      [§ 4]
```

**Which damage types it applies to:** the guide says the leech rides *the weapon-damage portion*,
whatever its types — it is **not** physical-only. The one exclusion the guide states is by damage
*delivery*, not damage *type*: **damage-over-time does not trigger it.** That is load-bearing here: the
Gutsmasher EoR modifier's **+330 bleed / 3 s** and the Sandreaver's **+210 bleed** (Lap L) are
**MEASURED-EXCLUDED from the leech basis**, as is Soulfire's orbiting lightning stream if it is modelled
as its own skill (`eyeofreckoning2.dbr` declares **no** `weaponDamagePct`).

### 3.2 The attack kit, decoded

| skill | record | rank | %WD skill | %WD gear | **%WD total** | leech frac | clamped? | own skill-scoped ADCTH |
|---|---|---:|---:|---:|---:|---:|---|---:|
| **Eye of Reckoning** | `playerclass09/eyeofreckoning1` | **20** | 43 | **+14** | **57** | **0.57** | no | — |
| Blitz | `playerclass01/blitz1` | 5 | 195 | 0 | 195 | 1.00 | **YES** | — |
| Vire's Might | `playerclass09/viremight1` | 2 | 125 | 0 | 125 | 1.00 | **YES** | — |
| Violent Delights (rune, medal) | `itemskillsgdx2/runes/rush_d203` | 1 | 240 | 0 | 240 | 1.00 | **YES** | — |
| default weapon attack | `default/defaultweaponattack` | 1 | 100 | 0 | 100 | 1.00 | no | — |
| default WP basic attack | `default/defaultwpbasicattack` | 1 | 100 | 0 | 100 | 1.00 | no | — |
| default kick | `default/defaultkickattack` | 1 | 150 | 0 | 150 | 1.00 | **YES** | — |
| Tip the Scales | `devotion/tier2_02f_skill` | 20 | 33 | 0 | 33 | 0.33 | no | **132 %** |
| Shifting Sands | `devotion/tier3_20e_skill` | 15 | 30 | 0 | 30 | 0.30 | no | — |
| **Maul** | `devotion/tier2_05f_skill_buff` | 20 | **none** | 0 | 0 | 0.00 | no | **45 %** on 305 flat physical |

* **EoR's 57 %** reproduces Lap L's IS-L1 chain **EXACTLY** (check `P2-eor-wd-total`): rank
  `15 (block 8) + 1 (all-skills) + 0 (Oathkeeper) + 4 (Gutsmasher `augmentSkillLevel2`) = 20`,
  `weaponDamagePct[19] = 43`, plus the Gutsmasher EoR modifier's `+14`. **The Warborn set's further
  `+5 %WD` is 4-piece-gated and he wears three — emitted `[INACTIVE]` in the `gear_wd_sources` column.**
* **The clamp bites on four skills and not on the channel.** Blitz, Vire's Might, Violent Delights and
  the kick all exceed 100 %WD and therefore leech at **exactly 100 %**, not at 195/125/240/150. Any model
  that scales leech linearly past 100 % over-heals those four by up to 2.4×.
* **Maul is the case that forces the schema.** It carries **no `weaponDamagePct` at all** — its 45 %
  ADCTH rides its own flat 305 physical. A weapon-damage-only census silently drops it.

### 3.3 Cadence — decoded, with the sheet's own self-disagreement carried as LO/HI

```
records/skills/playerclass09/eyeofreckoning1.dbr        [gdx2]
  Class              = Skill_AttackRadiusSpin
  timeBetweenAttacks = 200        "Time between hits to enemies along the path"
  skillTargetRadius  = 3.0 m      targetingMode = Point
  skillTargetNumber / skillMaxTargets / numTargets / maxTargets  =  ALL MEASURED-ABSENT
```

`timeBetweenAttacks` is denominated in **0.8 ms quanta** (PE-1's whole-family establishment, cited not
re-derived): `200 × 0.0008 = 0.160 s` at 100 % attack speed. **Independently corroborated by Crate's own
skill text** — *“at 100 % Attack Speed, Eye of Reckoning deals damage and drains Energy every 0.16 s.”*

The sheet does not agree with itself on attack speed, so both limbs are carried and **neither averaged**
(attack speed is a monotone scalar — the one class R-PM4-25 ratifies for LO/HI):

| limb | AS multiplier | hit period | **hit rate** |
|---|---:|---:|---:|
| **LO** | 1.8219 (sheet APS 2.66 ÷ item APS 1.46) | 0.087820 s | **11.387 /s** |
| **HI** | 1.9600 (sheet attack-speed stat line 196 %) | **0.081633 s** | **12.250 /s** |

Check `P2-eor-hit-period-HI-vs-sim-tick`: the HI limb's period is **0.081633 s** — the sim's own
`TICK_S = 0.08163` to five decimals. Stated as an arithmetic identity between two independently derived
constants, and re-confirmed from this seat.

**Multiplicity is geometric and uncapped** (Lap L's L3, reproduced here as a positive control — the
`target_cap_field` column reads `ABSENT` for EoR and `PRESENT` for Blitz, so the instrument can tell the
difference). Every body inside the 3.0 m disc takes every tick, so **every body inside the disc is an
independent leech event** — the reason clear rate and survivability are both density-dependent.

**⚑ There is no revolution-rate field.** `Skill_AttackRadiusSpin` declares no rotation period;
`rotationSpeedMultiplier = 0.35` is by its own template description a *player-turning* multiplier.
"Revolutions per second" remains **not decodable** (Lap L's D-L4, unchanged). *Damage ticks* per second
is the quantity the leech rides, and it is decoded.

---

## 4 — P3 · THE CAP / CLAMP QUESTIONS, AND THE MONSTER LEECH-RESISTANCE TABLE

**Deliverable: `pm4p_leech_resistance.csv`** (7,900 rows = 790 bodies × waves 151–160, **zero named
gaps**; every body resolved). Wave 150 is **DECLARED-ABSENT**: the Crucible run of record starts at
checkpoint 150, so 151 is the first fought wave and Lap D's board begins there.

### 4.1 ⚑ The finding: a flat +65 % leech resistance on every enemy in the game, from the difficulty record

```
records/game/balancingadjustment_mp+difficulty_enemies01.dbr                    [base]
  characterLifeModifier   = [50,50,50,50, 320,320,320,320, 580,580,580,580]
  defensiveSlowLifeLeach  = [35,35,35,35,  45, 45, 45, 45,  65, 65, 65, 65]
                                                            ^^ index 8 = Ultimate
  offensiveSlowLifeLeachModifier = [-25,-25,-25,-25, 0,0,0,0, 0,0,0,0]
```

Index 8 is the Ultimate cell — the *same* index Lap D ratified on `characterLifeModifier[8] = 580`.

**And it has an independent positive control that closes the identification completely:**

```
records/game/balancingadjustment_mp+difficulty_players01.dbr                    [base]
  defensiveSlowLifeLeach  = [0,0,0,0, 0,0,0,0, -25,-25,-25,-25]
```

`players01[8] = −25.0` reproduces the sheet's camera-read **`life_leech_resist = −25`** EXACTLY
(check `P3-player-leech-resist-positive-control` — **EXACT**). Two independent surfaces — a `.arz` array
cell and a screenshot of the game's own defence panel — land on the same number. **That simultaneously
confirms (a) index 8 = Ultimate, and (b) that `defensiveSlowLifeLeach` IS the stat the game prints as
"Life Leech Resist".**

**MEASURED-ABSENT, and it matters:** the Crucible's own balancing record
`balancingadjustment_survivalmode_enemies03.dbr` carries `defensiveSlowLifeLeach = 0.0` (scalar, no wave
array), and **there is no `balancingadjustment_survivalmode_players*` record at all** in the whole
corpus. **The Crucible adds no wave-scaled leech resistance and applies no player-side healing or leech
penalty.** (It *does* carry `characterPercentHealIncreaseModifier = −25 → −60` across its 200-cell wave
array — but that record is the **enemies** adjustment, so it is a nerf to *monster* healing, not the
player's. Recorded here so nobody later mis-homes it.)

### 4.2 The board, decoded — a clean five-tier ladder plus two immunity classes

Per-record resistance is composed by **exactly the chain Lap D used for life and Lap L for armour**:
`record.defensiveSlowLifeLeach + Σ_i skill_i.defensiveSlowLifeLeach[ rank_i(L) ]`, then + the difficulty
term, then + the survival wave term (0).

| **total leech resist** | own | bodies | dominant classes | ADCTH multiplier (COUPLED) | median mitigated heal/hit LO–HI |
|---:|---:|---:|---|---:|---:|
| **65 %** | 0 | **255** | Common 82, **Champion 172** | 0.350 | **789 – 2,014** |
| **75 %** | +10 | **367** | **Hero 360**, Champion 7 | 0.250 | **561 – 1,436** |
| **83 %** | +18 | 77 | Quest 59, Hero 15 | 0.170 | 313 – 818 |
| **88 %** | +23 | 43 | Quest 25, **Boss 18** | 0.120 | 195 – 510 |
| **105 %** | +40 | 5 | Hero 2, Champion 3 | **0.000** | **0** |
| **115 %** | +50 | 11 | Hero 11 | **0.000** | **0** |
| **565 %** | **+500** | 31 | traps / anomalies / tentacles | **0.000** | **0** |
| **588 %** | +523 | 1 | **Boss — Nemesis, Zantarin** | **0.000** | **0** |

The per-record term is almost entirely one shared record, `resists_heroboss.dbr`, read at the body's own
`skillLevel{i}` index — `[1] = 10` (hero), `[3] = 18`, `[4] = 23` (boss/quest). The 500-point class is
`passiveproperties_trap.dbr` and its siblings: **traps, anomalies (Whirlwind, Entropic Void, Sandstorm,
Ice Spike, Storm Conduit) and Writhing Tentacles are un-leechable objects.** 230 of the 7,900 rows are
additionally **physical-immune**, so they return zero life under *either* reading.

**Bottom line for the board: 490 of 7,900 body-waves (6.2 %) return ZERO life to the channel, and the
median body returns a quarter of face value.**

### 4.3 ⚑ **U-P-N-1 — does Life Leech Resistance gate ADCTH?** Both limbs, quantified, not averaged

The corpus declares **no equation** joining `defensiveSlowLifeLeach` to `offensiveLifeLeech`.

* **U-P-N-1a · COUPLED** — the resistance gates ADCTH multiplicatively, `mult = max(0, 1 − res/100)`.
  Evidence: (i) it is the **only** leech-resistance field in the corpus — there is no
  `defensiveLifeLeech`; (ii) it *is* the field the character sheet prints as "Life Leech Resist"
  (§ 4.1's exact positive control), and the community answer to "what does Life Leech Resist resist?" is
  verbatim *“resistance to Attack Damage Converted to Health”*
  (<https://steamcommunity.com/app/219990/discussions/0/1675812484339676047/>); (iii) the same threads
  document the standard counter-play — *“you can reduce life leech resistance by using either global
  'x reduced target resistances' debuffs… or specific '-% life leech' debuffs (i.e. Will of Ratosh)”* —
  which only makes sense if it gates ADCTH.
* **U-P-N-1b · DECOUPLED** — it gates only the `offensiveSlowLifeLeach` **DoT damage type** and leaves
  ADCTH untouched. Evidence: the field names pair `defensiveSlowLifeLeach` ↔ `offensiveSlowLifeLeach`
  *by construction*, and ADCTH's field carries no `Slow`.

**Both are emitted per row** (`adcth_mult_COUPLED` / `adcth_mult_DECOUPLED`) and both are carried
through the arithmetic in § 5. **The gap between them is a factor of 4 at the median body and infinite
at 48 of 790 bodies** — this is the single largest undecided term in the sustain model, and it is named
rather than resolved.

**Discriminator, pre-registered for whoever can run it:** put the reference character in front of a
**105 %+** body (any of the 16) and a **65 %** body and read the floating combat text heal. COUPLED
predicts zero on the first; DECOUPLED predicts the same heal on both.

### 4.4 The cap/clamp inventory

| candidate cap | verdict | basis |
|---|---|---|
| per-hit ADCTH cap | **MEASURED-ABSENT** — no such field in `parameters_offensive.tpl` or `gameengine.dbr` | corpus |
| per-second ADCTH cap | **MEASURED-ABSENT** | corpus |
| **%WD > 100 does not scale leech further** | **CONFIRMED — a real clamp**, and it bites on 4 of this character's 10 attack rows | Crate guide, quoted § 3.1 |
| target-count cap on the channel | **MEASURED-ABSENT** on `eyeofreckoning1.dbr` (four field names checked) | corpus |
| enemy leech-resistance cap | **MEASURED-ABSENT** — `gameengine.dbr` declares no monster resistance ceiling; the board's own values run to 523 | corpus |
| `defensiveSlowLifeLeachMaxResist` | present as a field; **0.0 on every body on this board** | emitted column |
| DoT excluded from leech | **CONFIRMED** | Crate guide |
| super-boss CC/leech asymmetry | *“most super bosses… are immune to life reduction effects… they do **not** have 500 % resistance to life leech”* — but this board contains bodies that **do**, at 500 | community + this board |

---

## 5 — P4 · THE WORKED ARITHMETIC

### 5.1 The formula, with every term's provenance

```
heal_per_hit_per_body =  ADCTH_frac                 20 % (table) | 21 % (sheet)     § 2.2
                       × leech_fraction             0.57  = min(57,100)/100         § 3.2
                       × D_weapon                   weapon-attack damage per hit    § 5.2
                       × (1 + HealingIncrease/100)  1.22                            § 2.5
                       × leech_resist_multiplier    COUPLED | DECOUPLED             § 4.3

HPS = heal_per_hit_per_body × hit_rate (11.387 | 12.250 /s) × N_bodies_in_the_3.0 m_disc
```

### 5.2 The weapon-damage term, and its declared limits

`D_weapon` is the sheet's own **`Weapon — damage per hit = 16,972 – 40,930`** (Lap A, frame 511) — the
100 %-WD reference the guide's law is written against, camera-measured, carried as a monotone LO/HI pair.

Two honest limits ride it:
* Lap L's **D-L1 stands**: the closed-form composition of the sheet's per-hit numbers is not reproducible
  from the corpus, so the *measurement* is used rather than a reconstruction.
* **U-P-N-4:** that the sheet's "Weapon" damage-per-hit line **is** the 100 %-WD reference is a reading,
  not a decoded identity. It is the only line on the sheet that can be — the default weapon attack carries
  100 %WD and no skill flat — but the game does not label it as such.

### 5.3 Full-uptime (raw, pre-mitigation) — the upper envelope

| ADCTH | leech-resist limb | heal/hit/body | HPS @ 1 body | HPS @ 5 | HPS @ 10 |
|---|---|---:|---:|---:|---:|
| 21 % (sheet) | **DECOUPLED** (0 %) | 2,478 – 5,977 | 28,223 – 73,220 | 141,113 – 366,102 | 282,226 – 732,204 |
| 21 % | **COUPLED @ 65 %** (trash floor) | 867 – 2,092 | 9,878 – 25,627 | 49,390 – 128,136 | 98,779 – 256,271 |
| 21 % | **COUPLED @ 75 %** (board median) | 620 – 1,494 | 7,056 – 18,305 | 35,278 – 91,525 | 70,556 – 183,051 |
| 20 % (table) | DECOUPLED | 2,360 – 5,693 | 26,879 – 69,734 | 134,393 – 348,668 | 268,786 – 697,337 |
| 20 % | COUPLED @ 65 % | 826 – 1,992 | 9,408 – 24,407 | 47,038 – 122,034 | 94,075 – 244,068 |
| 20 % | COUPLED @ 75 % | 590 – 1,423 | 6,720 – 17,433 | 33,598 – 87,167 | 67,197 – 174,334 |

### 5.4 Measured-uptime (mitigated, damage-**dealt**) — the defensible basis

The game's own stat text is *“the percent of the weapon attack damage **you deal**”*, so the weapon
portion is mitigated **per body** before ADCTH applies, using Lap L's imported chain (armour, absorption,
physical resist) under `combatformulas.dbr`'s verbatim armour law. Emitted per row as
`weapon_portion_applied_LO/HI` and `heal_per_hit_COUPLED_LO/HI`.

| basis | heal/hit/body (board median) | HPS @ 1 | HPS @ 5 | HPS @ 10 |
|---|---:|---:|---:|---:|
| **MITIGATED, ADCTH 21 %, COUPLED** | **561 – 1,436** | **6,388 – 17,587** | 31,939 – 87,934 | **63,879 – 175,867** |
| rows returning **zero** life | **490 / 7,900 (6.2 %)** | | | |

The weapon portion raw is `0.57 × 16,972–40,930 = 9,674 – 23,330`; the board's median mitigated value is
`8,758 – 22,415` — i.e. **the wave-151–160 board removes ~9 % of the weapon portion to armour and
physical resist, and the leech resistance removes 65–100 %.** *Mitigation is the small term; leech
resistance is the large one.*

**Sense of scale, stated without reference to any sim outcome:** against the sheet's own
`health_max = 20,005`, the mitigated COUPLED median at a single body is **0.32 – 0.88 max-health per
second**; at ten bodies it is **3.2 – 8.8 max-health per second**.

### 5.5 Non-ADCTH continuous sustain

| source | value | condition |
|---|---:|---|
| **Health regeneration (sheet, camera)** | **129.38 hp/s** | permanent |
| ↳ `bio_pc.characterLifeRegen` | 1.0 | engine base |
| ↳ gear/skill flat: Veterancy 30 + Scales of Ulcama 30 | 60.0 | permanent |
| ↳ `characterLifeRegenModifier`: Veterancy 25 % + Scales of Ulcama 33 % | +58 % | permanent |
| ↳ **table total** `1 + 60 × 1.58` | **95.80 hp/s** | **residual vs sheet = 33.58 → gap D-P2** |
| Menhir's Will `characterLifeRegen` | +120 hp/s | **only** below 33 % health (Lap G's circuit breaker) |
| `characterPercentHealIncreaseModifier` | — | **MEASURED-ABSENT** on this character |
| % max-health-per-second effects | — | **MEASURED-ABSENT** (`skillLifePercentBuffDuration` absent; `skillLifePercentSlow = 25` belongs to the **potion** modifier, Lap G) |
| Overguard | — | **MEASURED-ABSENT from block 8** — not allocated. Its `characterLifeRegenModifier` array exists but this character does not have the skill. |

**The composition law for regen is the game's own**, from `tagCharStatsLifeRegenInfo`: *“Percent bonuses
only affect regeneration from gear and skills; not base regeneration, which is based on physique.”* The
physique→base-regen formula is **MEASURED-ABSENT from the corpus** (`bio_pc.characterLifeRegen = 1` is the
only declared base) — hence gap **D-P2**; the sheet governs.

**The headline comparison: at one body, mitigated and COUPLED, ADCTH is 55× – 141× health regeneration.
Health regeneration is not a sustain layer on this character; it is a rounding term.**

Potions, Turtle Shell, Arcane Barrier, Menhir's Will and Ascension are **Lap G's** and are referenced,
not re-decoded. Their records are nonetheless re-emitted in `pm4p_adcth_sources.csv` (`damageAbsorption`
6,100 / 2,900 / 130, `skillLifePercent` 35, `skillLifeBonus` 800 + 25 %, `lifeMonitorPercent` 50/33/66) so
that a consumer sees the whole sustain surface in one table with one basis convention.

---

## 6 — DECLARED GAPS AND UNDECIDED ITEMS

| id | statement |
|---|---|
| **D-P1** | **ADCTH table 20 % vs sheet 21 % — 1-point residual.** The exhaustive walk (13 equipped items × base/affix/component/augment, the Warborn set at 3 pieces, all 55 allocated devotion nodes at their `devotion_level`, all 28 allocated class skills at effective rank, every one-hop `buffSkillName`/`petBonusName`/`itemSkillName` payload, and a 219-record broad closure) finds **exactly five** permanent global sources. Named candidates for the missing point, none decidable from the corpus: an **affix value carried in the item seed** rather than the base record (Lap L's D-L2b class, unchanged), or a sheet rounding of a fractional term. **Consequence ruled, not hidden: where the sheet prints a composed stat, the SHEET governs** (Lap L's standing ruling); the table walk is published beside it so every term is visible. Both are carried through § 5. |
| **D-P2** | **Health-regen residual 33.58 hp/s.** The physique→base-regeneration formula is MEASURED-ABSENT. Sheet governs. |
| **U-P-N-1** | **Does Life Leech Resistance gate ADCTH?** COUPLED vs DECOUPLED, § 4.3. Both limbs emitted per row. Factor of 4 at the median body, infinite at 48 of 790. Discriminator pre-registered. |
| **U-P-N-2** | **Is the leech basis pre- or post-mitigation?** The game's own stat text says *“damage you deal”* (post-mitigation) and § 5.4 takes that reading; § 5.3 publishes the pre-mitigation envelope. On this board the two differ by only ~9 %, so **this one is not load-bearing** — recorded so it is not later mistaken for a hidden assumption. |
| **U-P-N-3** | **Does each body struck leech independently?** No target cap and no per-hit/per-second leech cap exist in the corpus (§ 4.4), and each body is an independent damage application — so the arithmetic multiplies by `N_bodies`. The corpus **declares nothing either way**; no source found states it in terms. If a future probe finds a per-swing aggregation, every `HPS @ N` figure divides by N. |
| **U-P-N-4** | **Is the sheet's `Weapon — damage per hit` the 100 %-WD reference?** § 5.2. |
| **U-P-N-5** | **Crit interaction.** ADCTH is a fraction of damage dealt, so it inherits the crit multiplier — but the sheet's `weapon_damage_per_hit` is a **pre-crit** line, so § 5's numbers carry **no** crit uplift. Lap N's crit multipliers (`pthDamageModifier1..6 = 1.0 … 1.5`) are the multiplier to apply; the join is deliberately **not** performed here because whether the sheet line is pre- or post-crit is not decodable. |
| **ABSENT-1** | No leech equation of any kind in `combatformulas.dbr` (44 fields dumped). The composition law is external and cited. |
| **ABSENT-2** | No `balancingadjustment_survivalmode_players*` record exists — the Crucible applies no player-side healing or leech adjustment. |
| **ABSENT-3** | No monster-resistance ceiling in `gameengine.dbr`; no `maxPlayerResistance`-class field bounds `defensiveSlowLifeLeach` on enemies. |
| **ABSENT-4** | `offensiveLifeLeechMax` occurs once in 84,829 records (a sandbox test sword); `offensiveLifeLeechChance` four times, none equipped. This character's ADCTH is unconditional. |
| **ABSENT-5** | Wave 150 is not on the board — the run of record starts at checkpoint 150, so 151 is the first fought wave. The table is 151–160. |
| **D-L4 (inherited, unchanged)** | EoR revolution rate is not a decodable quantity. Damage ticks per second is, and is decoded. |

---

## 7 — CHECKS

| check | verdict |
|---|---|
| `P1-adcth-table-vs-sheet` | **RESIDUAL-DECLARED** — table 20.0, sheet 21.0, residual 1.0 (D-P1) |
| `P1-healing-increase-table-vs-sheet` | **EXACT** — table 22.0 = sheet 22.0 |
| `P2-eor-wd-total` | **EXACT** — 57.0 %, reproduces Lap L's IS-L1 chain from an independent walk |
| `P2-eor-hit-period-HI-vs-sim-tick` | **AGREES-TO-5DP** — 0.081633 s vs `TICK_S` 0.08163 |
| `P3-player-leech-resist-positive-control` | **EXACT** — `players01[8] = −25.0` = sheet `life_leech_resist = −25` |
| `P4-health-regen-table-vs-sheet` | **RESIDUAL-DECLARED** — 95.80 vs 129.38 (D-P2) |
| board coverage | 790 bodies × 10 waves = **7,900 rows, ZERO named gaps** |
| mitigation join | **7,900 / 7,900** Lap-L mitigation rows matched |

---

## 8 — SOURCE LIST

**Primary — records (read-only, Edition III):** `.arz` set at
`/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` (base, gdx1, gdx2, gdx3, sm_mod, sm1, sm2,
sm3; 84,829 record paths), `resources/Text_EN.arc`, `templates.arc`.
Named records: `combatformulas.dbr`, `gameengine.dbr`, `bio_pc.dbr`,
`balancingadjustment_mp+difficulty_enemies01.dbr`, `balancingadjustment_mp+difficulty_players01.dbr`,
`balancingadjustment_survivalmode_enemies03.dbr`, `eyeofreckoning1.dbr`, `eyeofreckoning2.dbr`,
`d107_blunt2h.dbr`, `mace2h_d107_eyeofreckoning.dbr`, `itemset_d025b.dbr`, `tier1_42c.dbr`,
`tier2_02d.dbr`, `tier2_02f_skill.dbr`, `tier2_05e.dbr`, `tier2_05f_skill{,_buff}.dbr`,
`presenceofvirtue2.dbr`, `passive02.dbr`, `passive2.dbr`, `willtolive1.dbr`, `b002e_legs.dbr`,
`compa_restlessremains.dbr`, `resists_heroboss.dbr`, `passiveproperties_trap.dbr`.

**Primary — save:** `player.gdc` sha256 `b8e6f510650dad0b12d60115d119b266283eda674c9c1a7186220ec93454bfa5`.

**Primary — official developer documentation:**
Crate Entertainment, *Guide → Gameplay → Combat*, <https://www.grimdawn.com/guide/gameplay/combat/>
(accessed 2026-08-14) — the ADCTH composition law, the >100 %WD clamp, the DoT exclusion, additivity.

**Secondary — community mechanics (used only where the corpus and the official guide are silent; each
quoted, none averaged):**
- <https://forums.crateentertainment.com/t/further-clarification-on-attack-damage-converted-to-health/39080>
- <https://forums.crateentertainment.com/t/attack-damage-converted-to-health-on-items-and-components/42048>
- <https://forums.crateentertainment.com/t/still-dont-understand-attack-damage-converted-to-health/86358> (global vs skill-specific ADCTH)
- <https://steamcommunity.com/app/219990/discussions/0/1675812484339676047/> (Life Leech Resist = resistance to ADCTH; −25 % player base on Ultimate)
- <https://steamcommunity.com/app/219990/discussions/0/1488861734120280082/> (leech-resistance reduction; super-boss asymmetry)
- <https://grimdawn.fandom.com/wiki/Game_Mechanics> — **NOT FETCHABLE** (HTTP 402 from this seat, twice). Recorded as an unreached source rather than cited from memory.

**In-corpus tag strings used as the game's own documentation:** `DamageLifeLeech`, `DefenseLifeLeach`,
`tagCharStatsDamageToHealthInfo`, `tagCharStatsHealIncreaseInfo`, `tagCharStatsLifeRegenInfo`,
`tagCharStatsLifeLeechResistInfo`, `tagDevotionEffectB02Desc`.

**Prior laps referenced, not re-decoded:** Lap A (sheet), Lap D (roster/life chain), Lap G (played kit,
devotion-rank law, circuit breakers, potions), Lap I (band C), Lap L (equipment array, IS-L1 EoR rank 20,
mitigation chain, target multiplicity), Lap N (crit multipliers), Lap O (OA/DA).
