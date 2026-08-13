# KC2-PM2 · LAP B — THREAT DECODE EXTENSION (legolas)

**Charter:** `gandalf/notes/2026-08-12-kc2-pm2-run-charter.md` — forks **F-2(a)** (monster damage
magnitudes) and **F-6 conditional-(a)** (summon threat, gated on this lap).
**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Date:** 2026-08-12 · **Author:** legolas (UNKNOWN-RESEARCHER)
**Lineage:** extends `legolas/notes/2026-08-12-kc2-roster-decode-completion/` (same seat, same
roster basis, same eight-archive overlay stack). That directory is **unmodified**; `s2_lib.py` is
imported from it, not copied.
**Mode:** read-only. Vendor corpus, engine tree and godot tree untouched. Python run from `/tmp`
under `PYTHONDONTWRITEBYTECODE=1`. The only writes are the files in this directory and four new
scripts in `research/scripts/`.
**GL-17:** Grim Dawn data is reference-study substrate for the private verification instrument.
Nothing here ships.

---

## 0 · HEADLINE

**The F-6 gate is CLEAN.** See § 5 — it has its own section because the charter's pre-registered
fallback fires on this word, and it does not fire.

The baton this run is measured against declares, in its own provenance block:

> **G-2 — "ALL monster damage figures are UPPER BOUNDS. Boss-skill rank binding unread."**

That declaration is now retired. Rank binding is read (§ 3, IS-2), and every damage magnitude in
this lap is the value at the rank the Crucible actually assigns — not a ceiling.

Three headline numbers:

| | |
|---|---|
| damage rows emitted | **4,724** (4,722 OK, 2 named unresolvable) across **169/169** identities **and 70 pet bodies** |
| hit-math constants | **55 of 55** present in the corpus, **zero ABSENT**; the load-bearing seven confirmed a second time against Crate's own guide |
| pet chain | **47 summoners → 70 distinct pet bodies → 149 spawn-contract rows, life + OA/DA MEASURED on 149/149** |

And the lap found what the prior lap found: **the cliff was in the instrument, not in the source.**
Five separate instrument-schema misses are named in § 3. Four of them were hiding damage.

---

## 1 · FILES

| file | rows × cols | what it is |
|---|---|---|
| `tg2_attack_damage.csv` | **4,724 × 84** | one row per (identity/pet, surface, slot-or-tree-index, skill record, offensive family). Value at the assigned rank + full rank table + delivery geometry + a grade on every quantity |
| `tg2_pet_chain.csv` | **232 × 57** | one row per (owner, spawning skill, spawn target). 149 are `Class=Monster` threat actors; 83 are loot/destructible spawns, labelled and excluded from the threat count |
| `hit-math.md` | — | the OA-vs-DA / PTH / crit-tier / armour formula set, with a provenance grade per constant and one named UNRESOLVED (SEM-1) |
| `hit_math_constants.json` | 55 keys | machine-readable raw dump of `combatformulas.dbr` + `gameengine.dbr` |
| `tg2_monster_oa_da.csv` | 169 × 17 | per-identity OA/DA at roster level, **169/169 MEASURED**, plus the tree passives that move them (listed, not folded) |

**Scripts** (in `agentic_orchestration/research/scripts/`, extending the s2/tg2 harness):
`pm2b_lib_2026_08_12.py` · `pm2b_damage_2026_08_12.py` · `pm2b_hitmath_2026_08_12.py` ·
`pm2b_petchain_2026_08_12.py` · `pm2b_verify_2026_08_12.py`

**Join keys.** `record` + `slot` → `tg2_attack_slots.csv`. `record` + `tree_index` →
`tg2_skill_tree.csv`. `record` → `tg2_monster_timing.csv` / `tg2_monster_stats.csv` /
`tg2_monster_oa_da.csv`. Pet rows carry `actor_kind=pet` + `owner_record`, so the fight cell reads
**one** damage table for every body that can hit the player. Join integrity is asserted, not
assumed (§ 6, A5).

---

## 2 · INSTRUMENT-SCHEMA DECLARATION (charter Law 7 / NOTE-9 basis discipline)

The charter names two prior misses — the two-surface cliff and the magnitude gap — and requires
this lap to declare its own schema's bounds. It does, and it found three more misses while doing
so. **All five are stated as bounds on the PRIOR instrument that this lap removed; each is a
place where a future re-run of the old harness on any other roster inherits the same hole.**

### IS-1 · the damage vocabulary was hand-written, and short

The 08-08 and 08-12 harnesses tested a hand-listed 10-name direct set and 8-name DoT set. A census
of every `offensive*` field carrying a nonzero value across the 711 distinct skill records this
roster touches returns **113 populated field names**. Families the hand list never had, with their
populations: `offensivePercentCurrentLifeMin` (**73 skills** — %-of-current-life damage, which no
flat-mitigation model handles), `offensiveLifeLeechMin` (**42** — monster ADCtH), `offensiveFumbleMin`
and `offensiveProjectileFumbleMin` (attacker-miss debuffs), `offensiveDisruptionMin`,
`offensiveTotalDamageModifier` (**20**), `offensiveCritDamageModifier` (**26**),
`offensiveTotalResistanceReductionAbsolute`, `offensiveSlowOffensiveReduction`,
`offensiveSlowDamageMult` (sunder).

**This lap's bound:** the taxonomy is not written by me either. It is read out of Grim Dawn's own
template — `templatebase/parameters_offensive.tpl` inside `database/templates.arc` — which supplies
a first-party group name for every field (`"Offensive Slow Fire"`, `"Offensive Percent Current
Life"`, `"Total Damage Modifier"`, …, 64 groups). The one reasoning step left is the map from
group name to the seven `kind` buckets (`direct` / `dot` / `leech` / `percent_current_life` /
`control` / `debuff` / `modifier` / `armor_pierce_ratio`), and that map is written out in full in
`pm2b_lib_2026_08_12.py` § IS-1 so any single row of it can be overruled without re-running.

### IS-2 · `skillLevel<i>` is a string equation on 1,733 of 1,733 rows

The 08-12 harness read it through a numeric guard: `num(rec.get("skillLevel%d" % i))`. Every value
in the corpus is a string (`'charLevel/4+1'` ×949, `'charLevel*1'` ×335, `'(charLevel/30)+1'` ×83,
`'0'` ×64, …). The guard therefore returned `None` **100 % of the time, silently**, and
`tg2_skill_tree.csv` ships with an empty `skill_level` column. Rank assignment was structurally
invisible to that schema — which is exactly why the baton could only declare upper bounds.

**This lap's bound:** the equations are evaluated with `charLevel` bound and nothing else; an
equation referencing any other variable returns `LEVEL-EQ-UNEVALUABLE` rather than a value
(0 occurrences on this roster). Rank is `floor(eq)`, GD skill level 1 → array index 0, clamped to
the table length with the clamp named on the row (`RANK-CLAMPED-TO-TABLE`, 20 rows). Rank 0 is
emitted as `RANK-0-NOT-GRANTED` with **no value**, never as rank 1.

**The rank carrier is the tree, and only the tree.** 663 of 667 attack slots also appear in their
creature's granted tree; a slot's rank comes from its tree twin. The remaining **5 slot rows carry
`SLOT-RANK-UNASSIGNED` and no magnitude** — a documented gap, not an estimate.

### IS-3 · spawn targets must be classified by `Class`, not by path

The prior lap's *"92 of 169 identities summon"* is a path-blind count of `spawnObjects` references.
Resolved by target `Class`, the 92 splits **exactly**:

- **47 identities** spawn a `Class = Monster` actor — real threat
- **45 identities** spawn only `Class = Destructible` (77 refs) or `FixedItemContainer` (6 refs) —
  **loot chests on death, not threat**
- 47 + 45 = 92. The prior number is reproduced and then correctly partitioned.

The error runs both ways: **15 of the pet bodies live under `records/skills/.../pets/`** while
carrying `Class = Monster` (e.g. `bossskills/pets/firedevil_01.dbr` is a 935-field creature record
filed in the skills tree). A path-prefix classifier drops those *and* counts the chests.

### IS-4 · the nested skill surface — a THIRD surface neither prior lap followed

A `Skill_Buff*` or auto-cast skill frequently carries **no damage of its own**; it points at a
second record that does, via `buffSkillName` (84 refs, 51 damage-bearing) or `autoCastSkill`
(62 refs, 36 damage-bearing). Neither the 08-08 nor the 08-12 harness followed either pointer.

Consequence measured: **584 damage rows across 95 skill records** live at nest depth ≥ 1. The chain
runs to **depth 6** and contains **no cycles** (cycle guard installed anyway; 0 fired). This is what
made nine pet bodies — blood pools, voids, molten pools, rifts, traps — read as harmless: *all* of
their damage is one pointer down.

**This lap's bound:** a nested skill carries no level equation of its own anywhere in this corpus,
so it is resolved at its invoking surface skill's rank, marked
`rank_source = INHERITED-FROM-PARENT-RANK`. That is a declared rule, not a measurement.

### IS-5 · `chainInitialSkill` / `chainNextSkill` are a ninth and tenth attack slot

The 08-08 schema models 8 slots (`attackSkillName` + `specialAttack1..5` + `initial` + `dying`).
Creature records also carry a **chained** attack pair. On this roster that is **36 (record, slot)
pairs across 19 identities and 31 distinct skills**, including *Dermapteran Mad Queen* and the
Malmouth Enclave council bosses. Those rows are emitted here with `slot = chain_initial` /
`chain_next` and **have no twin row in `tg2_attack_slots.csv` to join against** — the assert wall
reports them separately as `A5-slot-IS5-chain` rather than pretending the join is clean (§ 6).

### IS-6 · what THIS schema still does not model — stated up front

- **Telegraph wind-up is not one field.** `skillChargeDuration` is populated on only **17 of 506**
  damage-bearing skill records. The AOE/wind-up signal is spread across
  `projectileExplosionRadius` (**149 skills** — the largest AOE carrier, and *not* decoded by any
  prior lap), `skillTargetRadius` (122), the expanding-wave block
  `waveStartWidth`/`waveEndWidth`/`waveDepth`/`waveDistance`/`waveTime`/`expansionTime` (51–53),
  `skillAllowsWarmUp` (28) and `skillChargeLevel` (14). All of these are now emitted as columns.
  **A telegraph rule keyed on `skill_target_radius` alone would see under a third of the AOE
  surface** — flagged directly at F-4, which the charter says is geometry-decided from
  "decoded `skill_radius` + warmup/charge durations."
- **Distance-banded projectile damage is emitted but not applied.** `projectileDamageRange1..3
  Min/Max/Scale` is populated on 69–78 skills — damage that scales with travel distance. Columns
  ride the CSV; the fold is gamora's.
- **Resistances are not in this lap.** Monster resistance passives are named in
  `tg2_monster_stats.csv` (`resist_passives`) but their magnitudes are not extracted here — the
  player's *outgoing* damage is not this lap's scope. Incoming-damage mitigation is (§ hit-math § 4).
- **`tagDurationDamageOverTime` / DoT storage semantics: UNRESOLVED** (hit-math SEM-1). Both
  readings are emitted; neither is chosen.

---

## 3 · WHAT THE MAGNITUDE EXTRACTION COVERS

### 3.1 Coverage against the prior CSVs

| surface | rows in prior CSV | prior schema called damage-bearing | **rows with ≥1 damage row now** | delta |
|---|---|---|---|---|
| attack slots (`tg2_attack_slots.csv`) | 667 | 496 | **561** | **+65** |
| tree skills (`tg2_skill_tree.csv`) | 1,733 | 903 | **989** | **+86** |
| nested (IS-4, no prior row exists) | — | — | **584 rows / 95 skills** | new surface |
| identities with ≥1 damage row | 169 | — | **169 / 169** | 100 % |

"Rows with ≥1 damage row now" counts a prior-CSV row as covered if damage is attributable to it
**including via the nested chain**. Restricted to damage found on the surface skill itself
(nest depth 0), the figures are 532 slots and 906 tree rows; the difference is IS-4's contribution
attributed back to its invoking surface.

**Zero unresolvable damage rows beyond the one already known.** The only `SKILL-UNRESOLVED-IN-ARZ`
rows are 2, both `records/skills/nonplayerskillsgdx3/attackmelee/dranghoul_butcher.dbr` granted by
*Fariim ~ Bramble* — the single dangling reference the prior lap documented at 1/1,733 (0.06 %),
now surfacing once per surface (slot + tree). No new dangling references were found.

**The 106 slot rows with no damage row are genuinely damage-free, and that was checked, not
assumed:** each was walked to the bottom of its nested chain and returns zero offensive families.
They are `Skill_BuffRadiusToggled` (16), `Skill_SpawnPet`/`TargetedSpawnPet`/`SpawnPetMonster` (37),
`Skill_WeaponPool_ChargedLinear` (12), `Skill_AttackWeaponCharge` (12), buffs, teleports.

**No roster identity's damage depends on an equipped-weapon record.** This was the one plausible
hole and it is closed by measurement: 45 identities carry no `damagebase_*` base-damage passive,
and **zero of those 45 declare a hand-item record** — their damage is skill-sourced. The other 124
carry `damagebase_*` natural-weapon passives, which this lap extracts. `weaponDamagePct` is
populated on 18 skills and is emitted as a column so the rider is visible.

### 3.2 Row population by kind and grade (4,722 OK rows)

| kind | rows | | rank grade | rows |
|---|---|---|---|---|
| direct | 2,916 | | MEASURED | 4,692 |
| dot | 718 | | RANK-CLAMPED-TO-TABLE | 20 |
| debuff | 350 | | SLOT-RANK-UNASSIGNED | 10 |
| percent_current_life | 335 | | | |
| leech | 160 | | | |
| control | 141 | | | |
| modifier | 102 | | | |

### 3.3 Per-stratum (roster actors only, 3,847 rows)

| stratum | identities | damage rows | damaging rows (direct/dot/%life/leech) |
|---|---|---|---|
| boss&quest | 33 | 1,098 | 920 |
| trash | 75 | 1,033 | 937 |
| hero | 27 | 646 | 553 |
| devotion | 16 | 455 | 398 |
| nemesis | 9 | 330 | 274 |
| bounties | 9 | 285 | 254 |

### 3.4 Delivery geometry, for F-4

| field | rows | distinct skills |
|---|---|---|
| `projectile_explosion_radius` | 1,124 | **149** |
| `projectile_velocity` | 971 | 131 |
| `skill_target_radius` | 814 | 122 |
| `expansion_time_s` | 444 | 53 |
| `wave_start_width` | 443 | 51 |
| `skill_charge_duration_s` | 210 | 17 |
| `skill_allows_warmup` | 206 | 28 |
| **any AOE carrier** | **2,238** | **304 skills across 139 of 169 identities** |

### 3.5 Sanity anchors (largest single direct magnitude at the assigned rank, roster level 102–109)

| identity | type | min at rank | skill |
|---|---|---|---|
| Tempest Spawn | Physical | 3,090 | `giantfire_moltenboulder` |
| Grava'Thul, the Voiddrinker | Chaos | 2,905 | `chthonian02_homingchaos` |
| Anasteria, Wrath of the Aether | Aether | 2,904 | `angela_annihilation` |
| The Steward | Cold | 2,428 | `tombguardian_massiveswipe` |

Against the F-1 player sheet anchor (Screenshot (495): **20,005 HP**), the top monster hit is
~15 % of the player's health bar **before** mitigation and before the `percent_current_life`
family (335 rows) is applied at all. The sim gains a fight.

---

## 4 · RANK BASIS — the one modelling choice, declared

`rank_used` is computed with `charLevel` bound to **the baton's own per-actor `level`**
(102–109, band width 0 on all 169 — every identity has exactly one level in this run).

Creature records *also* carry their own `charLevel` equation (`'charLevel*1'` ×94,
`'charLevel*1+5'` ×24, `'(charLevel*1.1)+2'` ×18, …). Re-applying it on top of the baton level
would change the assigned rank on **1,174 rows**. It is not applied, for a cited reason: the
baton's own provenance block refers to a *"charLevel ceiling 110"* and lists
`actors[].level` under `DIV-LEVEL-COVERAGE`, i.e. the baton's `level` **is** the effective
charLevel, already post-equation. Re-applying would double-count.

**Both are on the wire anyway.** Every row carries `char_level_equation`, `char_level_adjusted`
and `rank_used_alt_basis`, so if gamora rules the other way the re-fold is a column swap, not a
re-run. Grade: `rank_used` **MEASURED under a declared level basis**; `rank_used_alt_basis`
**DIAGNOSTIC**.

---

## 5 · **THE F-6 GATE — VERDICT: CLEAN**

**The chain decodes clean. The pre-registered fallback (b) does NOT fire. F-6(a) may proceed on
real substrate: the fight cell can spawn real pets from `tg2_pet_chain.csv` +
`tg2_attack_damage.csv` (`actor_kind=pet`).**

### 5.1 What resolved

| link in the chain | result |
|---|---|
| summon skill → spawn target | **149 / 149** resolved. **0 unresolved-in-arz.** Spawning classes: `Skill_TargetedSpawnPet`, `Skill_SpawnPet`, `Skill_MonsterGenerator`, `Skill_SpawnPetMonster`, `Skill_OnDeathSpawnActor`, `Skill_AttackSpellChaosSpawnPet`, `Skill_AttackProjectileSpawnPet`, `Skill_AktaiosMirage` |
| pet body → life | **149 / 149 MEASURED** via the same `characterAttributeEquations` → `bios/*.dbr` chain that A6 validated 66/66 |
| pet body → OA / DA | **149 / 149 MEASURED** |
| pet body → movement + attack speed | **149 / 149** (`characterRunSpeed`, `characterAttackSpeed`, `characterSpellCastSpeed`, `characterDodgePercent`) |
| pet body → basic swing period | **121 / 149 MEASURED**; the 28 gaps are characterised in § 5.3 and are **correct negatives** |
| pet body → attack slots + tree | **149 / 149** counted; **145 / 149 carry ≥ 1 damage-bearing skill** |
| pet body → damage magnitudes | **875 rows across 68 bodies**, same schema, same rank rule, same grades as the roster |
| spawn contract (cap / burst / period / TTL) | **148 / 149** carry at least one of `petLimit` / `petBurstSpawn` / `spawnObjectsTimeToLive`; the 1 remaining is rate-limited by a 3.0 s `skillCooldownTime` — see § 5.3 |

### 5.2 The numbers

| | |
|---|---|
| roster identities that spawn a `Class=Monster` actor | **47 / 169** (28 %) |
| …that spawn only loot/destructibles (prior lap counted these as summoners) | 45 |
| distinct pet bodies | **70** (57 at depth 1, +13 reached only at depth 2) |
| spawn-contract rows | **149** (135 at depth 1, 14 at depth 2) |
| summoner identities by stratum | nemesis 7/9 · boss&quest 21/33 · hero 12/27 · devotion 3/16 · bounties 2/9 · trash 2/75 |
| baton actors that are summoners | **72 of 344 = 20.9 %** |
| declared caps: median per summoner identity | 8 (max 76) |
| worst case if every summoner actor caps out simultaneously | **960 extra bodies** |

**Note for the fight cell, on the charter's own arithmetic.** The charter's F-6 sizing said
"cap ≤ 4; worst case ~368 extra bodies." The measured caps are larger: `petLimit` runs to 12 on
`Skill_MonsterGenerator`, and one identity's summon skills sum to 76. Under the declared caps the
worst case is **960**, not 368 — a **2.6×** sizing delta. That is a performance-budget input for
gamora, surfaced now rather than at runtime. It is not an argument against F-6(a); it is the
number F-6(a) has to be built for.

**Depth-2 is real and load-bearing.** Nine pet bodies are *spawner turrets* that deal no damage at
all — Korvaak's Eldritch Rift is the type case: it carries `turret_blankradius` +
`petskill_eldritchrift_servantgenerator` and nothing else. A depth-1-only chain would report their
summoners as harmless. The walk goes to depth 3 (bounded); depth 2 contributes 14 rows and 13
bodies, and nothing was found at depth 3.

### 5.3 Residuals inside the CLEAN verdict — named, and why none of them cliff it

**R-P1 · 28 rows / 11 bodies have no basic swing period.** Every one is stationary:
`characterRunSpeed = 0.0` or `disableMovement = True`, and 10 of the 11 declare **zero**
`unarmedAttackAnim*` fields in their animation table. These are ground effects, crystals and traps
(`beast_bloodpool`, `pet_eldritchrift`, `witchgodguardian_sentinel_crystal`, `trap_icespike_hero_a01`,
`pet_celestialeffigy`, …). **They have no swing because they do not swing** — their damage tempo is
carried by aura/radius fields (`skillTargetInterval`, `expansion_time_s`), which are on the damage
rows. This is a correct negative, not an extraction failure.

**R-P2 · 4 rows / 2 bodies carry zero damage.** Both are `pet_eldritchrift` variants — the spawner
turrets of R-P1/§ 5.2. Their progeny **is** in the table, at depth 2. Correct zero.

**R-P3 · 1 row of 149 declares no cap, burst or TTL.** *Ishtal, the Mind Reaper* →
`mindreaper_01_mirage.dbr`, class `Skill_AktaiosMirage` (a bespoke mirage-clone class). It carries
`skillCooldownTime = 3.0`, so it is rate-limited but not count-limited by declared data. **gamora
must pick a cap for this one skill and declare it**; I will not invent one (GL-12).

**R-P4 · pet level is a declared inheritance, not a measurement.** Pet `charLevel` is bound to the
*owner's* level. Each pet's own `charLevel` equation is carried in the CSV
(`pet_char_level_equation`) so the assumption is auditable and reversible.

**None of R-P1…R-P4 is an extraction cliff.** No format wall, no auth wall, no unresolvable
reference in the entire chain. **CLEAN.**

---

## 6 · ASSERT WALL

Mechanical, oracle-free, plus one byte-level anchor. Re-runnable: `pm2b_verify_2026_08_12.py`.

| assert | result |
|---|---|
| **A1** tier-1 anchor — re-decode the rank array straight from the `.arz` and byte-match the CSV value at the assigned rank | **PASS**, 60 anchors, exact, zero tolerance allowed |
| **A2** every OK row with an assigned rank carries a non-null min or max | **PASS** |
| **A3** `rank_used` ∈ [0, `n_ranks`] | **PASS** |
| **A5-slot / A5-tree** join integrity against the prior CSVs | **PASS** |
| **A6** every quantity carries a grade | **PASS** |
| **A4-reference-data** direct-damage rank tables non-decreasing | **REPORTED, 32 rows / 13 skill-type pairs** — see below |
| **A5-slot-IS5-chain** chain-slot rows have no twin to join against | **REPORTED, 78 rows** — see IS-5 |

**A4 fires on Grim Dawn's data, not on this decode.** 13 skill/type pairs carry a **single-rank
dip** authored by Crate — e.g. `aetherialworm_*` and `korvaakservant_*` drop 105 → 90 between ranks
6 and 7; `aetherialbloater_violentbarf` drops 209 → 202 between ranks 15 and 16. **Every dip sits at
rank 6 or 15, far below the rank the Crucible assigns (28), so no value this lap emits is touched.**
The monotonicity assumption is a field-class implication imported from the GD-slice adapter; the
reference violates it in 13 places. The assert stays and the data is **not smoothed** (GL-12).

---

## 7 · WHAT I DID NOT DECIDE (not mine)

- **SEM-1 — DoT storage semantics.** Both readings emitted, neither chosen. hit-math § 6. **gandalf/gamora.**
- **The rank basis ruling.** Primary basis declared and justified; the alternate is on the wire. **gamora.**
- **The OA/DA fold order** — bio base, creature flat/percent overrides and tree passives are all
  emitted separately and un-summed. **gamora.**
- **R-P3's cap** for `Skill_AktaiosMirage`. **gamora, and it must be declared on the wire.**
- **Whether 960 worst-case bodies is affordable.** Number surfaced; the budget call is **gamora's,
  and the scope call is the conductor's.**
- **Whether the `percent_current_life` family (335 rows) belongs in the sim at all.** It is real,
  it is large, and no flat-mitigation model handles it. **gandalf.**

---

## 8 · WHY THE PRIOR LAP'S "92 SUMMONERS" AND THIS LAP'S "47" ARE BOTH RIGHT

Because they measure different things, and the difference is exactly 45 loot chests. Recorded here
because the charter quotes 92/169 in F-6, and anyone reading the two documents side by side must
not conclude one of them is wrong. **The threat-bearing number is 47.** The 92 is the count of
identities with any `spawnObjects` reference of any class. Both are in the CSVs, labelled.

---

*Roster basis: `kc2-baton-v1-E-s09-cp150-20260809_052836.json`, 344 actors → 169 distinct records.
Corpus: `~/Games/vendor/grim-dawn-edition-III-20260808`, eight-archive overlay, read-only, unmodified.*
