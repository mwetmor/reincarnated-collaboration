# SB-1 · ENEMY MECHANICAL-IDENTITY SUBSTRATE RECON (elrond)

**Ledger row:** A1b-8 (Matt premise change: mechanical substrate → Synty body fit → name)
**Date:** 2026-08-12 · **Author:** elrond (data steward)
**Mode:** read-only reconnaissance. Engine tree, vendor tree, and godot tree untouched.
Only write is this file.
**Companions:** `agentic_orchestration/drax/notes/2026-08-12-sb1-synty-enemy-body-census.md`
(137-body target side) · `agentic_orchestration/gandalf/notes/2026-08-10-sb1-scene-run-ledger.md`
(row A1b-8, the premise).

---

## 0 · HEADLINE — THE COMMISSION'S PREMISE IS WRONG IN ONE LOAD-BEARING WAY

The commission states: *"The run is engine-emitted season content; trace the roster names back to
their source records."*

**It is not engine-emitted content.** `E-s09-cp150` is a **Grim Dawn Crucible metrology
reconstruction**. Every one of the 344 actors carries a `record_path` of the form
`records/creatures/enemies/**.dbr` — those are **Grim Dawn database records**, decoded out of
`/Users/admin/Games/vendor/grim-dawn/**/*.arz` by legolas. The 163 names are Grim Dawn's names
("Haunted Noble", "Ugdenbog Spikeshell", "Reaper of the Lost"). The engine did not mint them.

This matters for three reasons and I will not bury them:

1. **GL-17 exposure.** Deriving families from this roster and fitting bodies to them is
   *reproducing the reference's roster*, not being governed by it. If the SB-1 scene run is a
   metrology fixture, that is fine — the fixture is allowed to wear the reference's coat. If any
   of this flows toward shipped content, the roster must be re-minted from engine substrate first.
   **Route to gandalf.** I do not rule on it.
2. **There are two enemy substrates, not one**, and they do not share a key, a vocabulary, or a
   schema. § 1 names both.
3. **The fit function's eventual production input is the engine substrate**, not this one — and
   the engine substrate has a *different and worse* problem (§ 4).

Second headline, and the one that actually helps the fit function:

**The reference already answers the fit question, and its answer is "body is heavily reused and
does not follow the family label."** 66 covered roster records ride **23 distinct rigs**. In
**34 of 66 cases the rig prefix contradicts the lexical family name** — `ghost_b01` "Haunted
Noble" rides `heroine01_sword1h`; `cultist_cultleader_01`, `ghost_stepsoftorment_01`,
`humanascendant_terrnox` and `odv_bounty07` all ride the *same* `hero01_sword1h` humanoid.
See § 3 and § 4.3. **Any (family-name → body) shortcut is falsified by the reference itself.**

---

## 1 · WHERE THE MECHANICAL TRUTH LIVES

There is **no database**. Not one row of enemy mechanical identity lives in a DB table anywhere in
the project. `data/telemetry.db` (35.5 GB) is player-fight telemetry; `data/research.db` and
`data/knowledge_base.db` are **0 bytes**; `data/emission_registry.db` (45 KB) is emission
bookkeeping. The entire enemy-identity surface is **flat CSV and JSON**.

### 1.1 SUBSTRATE A — the Grim Dawn reference (this roster)

Join key throughout is `record` == the baton's `record_path`. The baton's `archetype_tag`
(`ghost_b01`) is the record basename — so the baton **does** carry a clean join key; the
commission's read that it "groups nothing" is right as a *grouping* claim and wrong as a
*joinability* claim.

| # | Store | Path | Rows × cols | Roster coverage |
|---|---|---|---|---|
| A0 | **Raw corpus** (ground truth) | `/Users/admin/Games/vendor/grim-dawn/{database,gdx1,gdx2,gdx3,survivalmode1..3}/**/*.arz` + `resources/Creatures.arc` | 8-archive overlay stack | **100%** (undecoded) |
| A1 | **Wave pools** | `~/Games/reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv` | 1,998 × 26 | **169/169 records · 163/163 names** |
| A2 | **Skills / attack slots** | `agentic_orchestration/legolas/notes/2026-08-08-kc2-threat-grammar-arz-boundary/tg_attack_slots.csv` | 3,064 × 51 | 62/169 |
| A3 | **Per-monster behaviour + rig** | `…/2026-08-08-kc2-threat-grammar-arz-boundary/tg_monster_timing.csv` | 968 × 53 | 66/169 |
| A4 | **Rig index** (`.anm` header decode) | `…/2026-08-08-kc2-threat-grammar-arz-boundary/anm_index.json` | 3,452 rigs | keyed by asset folder |
| A5 | **Animation event track** | `…/2026-08-08-kc2-threat-grammar-arz-boundary/anm_events.json` | 1.4 MB | per-rig |
| A6 | **Stat fold** (eHP + damage types) | `~/Games/reincarnated-engine/data/kc2/t22_band_a_monster_stats.csv` | 968 × 24 | 66/169 |
| A7 | **Record inputs** (controller, movement) | `~/Games/reincarnated-engine/data/kc2/kc2_s1_banda_record_inputs.csv` (dup at `legolas/notes/2026-08-08-kc2-citation-microprobe/`) | 895 × 86 | 66/169 |
| A8 | **Pool balance flags** | `~/Games/reincarnated-engine/data/kc2/pe6_pool_ignoregamebalance.csv` | 635 × 14 | pool-keyed |
| A9 | Decode adapters (mine, meta-repo) | `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py`, `gd_arc_reader_2026_07_26.py` | — | working |
| A10 | Extraction harness | `…/2026-08-08-kc2-threat-grammar-arz-boundary/{x1_extract.py,x2_events.py,tg_lib.py}` | — | working, re-runnable |

**The coverage cliff is the whole story.** A2/A3/A6/A7 were all cut against **band A** (the t22
968-record roster, `0d6992e8`). The E-s09-cp150 roster is the **s2 band, waves 151–160**. Only
**66 of 169 records (39%)** overlap. Coverage by stratum:

| stratum | distinct records | tg-covered |
|---|---|---|
| bounties | 9 | **9/9** |
| trash | 75 | 36/75 |
| boss&quest | 33 | 12/33 |
| devotion | 16 | 6/16 |
| hero | 27 | **3/27** |
| **nemesis** | 9 | **0/9** |

**Nemesis is 0%. Hero is 11%.** The two strata carrying the most identity weight are the two
least decoded. This is not an absence in the world — those records are in the `.arz`, the adapter
reads them, the harness is checked in and re-runnable. **It is an un-run extraction lap.**

### 1.2 SUBSTRATE B — the engine's own enemies (production path)

| Store | Path | Count |
|---|---|---|
| Season monster records | `~/Games/reincarnated-engine/seasons/season_*/monsters/monster_*.json` | **1,108** across 25 seasons (44/season) |
| Bundled emission | `~/Games/reincarnated-engine/src/reincarnated/output/one_realm_demo_bundle{,_w3_flavor}.json`, `w3_batch1_bundle.json` | — |
| Loadout mirror | `~/Games/reincarnated-loadout/` season artifacts | — |

Zero join to Substrate A. Different names, different keys, different vocabulary.

---

## 2 · FIELD CENSUS

### 2.1 Baton wire (what survives to the scene run) — 22 fields × 344
`actor_id · archetype_tag · display_name · record_path · threat_tier · level · wave ·
hp_max · hp_max_basis · life_modifier_pct · is_champion · spawn_{x,y,t_s,tick,heading_rad} ·
spawn_point_id · engage_{t_s,tick,null_reason} · path[] · entity_radius_m`

`entity_radius_m` is **null ×344**. No species, no size, no family, no skills, no element.
The wire carries *position and durability*, nothing about **what the thing is**.
`config.kit.body_radius_role = "NON-CAUSAL"` — the sim declares body irrelevant to its model, which
is why the emitter drops it. **Not a bug. A scope statement.** (§ 5, gap G1.)

### 2.2 Substrate A identity fields — what a fit function could actually use

| axis | field(s) | store | shape |
|---|---|---|---|
| **skills** | `skill` (DBR path), `skill_class`, `chance_pct`, `delay_s`, `range_band`, `skill_cooldown_s`, `distance_profile`, `projectile{,_velocity,_distance,_launch_angle}` | A2 | **983 distinct skills**; 60+ `skill_class` values — `Skill_AttackWeapon` 319, `Skill_BuffRadiusToggled` 301, `Skill_AttackProjectileAreaEffect` 272, `Skill_AttackWave` 268, `Skill_AttackRadius` 256, `Skill_SpawnPet` 118 … |
| **element** | `damage_types` | A6 | pipe-list: `Physical\|Pierce\|Cold`, `Physical\|Aether\|Life`, `Physical\|Poison` |
| **role / AI** | `controller` (`controller_ghost_rangedbasic`, `controller_swampcrab_melee`, `controller_skeletoncaster01`), `ctrl_*` (28 fields: pursuit, view, flee, dodge, roam, distress) | A3, A7 | rich; controller stem is a *declared* role |
| **range** | `range_band` per slot (ShortRange 755 / MediumRange 493 / AnyRange 492 / LongRange 455) | A2 | per-skill, not per-monster |
| **threat class** | `monster_classification` (Hero 446 / Champion 275 / Common 181 / Quest 64 / Boss 1), `in_band_as` | A3, A7 | |
| **tempo** | `character_attack_speed{,_tag}`, `basic_swing_period_s`, `windup_s`, `recovery_s`, `root_lock_s`, `n_hits`, `hit_frames` | A2, A3 | frame-exact |
| **locomotion** | `character_run_speed`, `walk_speed`, `run_speed_jitter`, `min/max_rotation_speed`, `disableMovement` | A3, A7 | |
| **stats** | `life_equation`, `ehp_w{1,47,93}_{lo,hi}`, `flat_total_mid`, `mod_total_pct`, `armorbase_*`, `ultimate_pct`, `gladiator_*` | A6, A7 | MEASURED-graded |
| **BODY (!)** | `basic_attack_anims` (rig filenames), `anim_table`, A4 folder key `enemies/<body name>/anm/…` | A3, A4 | **the reference's own body statement** |
| **grouping (reference's own)** | `pool_record` basename — `ghost_t1/t2/t3`, `wendigo_t1..t3`, `nemesis_all`, `devotion_heroes04`, `basilisk_hero` | A1 | 140 pools touch the roster, **100% coverage** |

**Does a family/species axis exist in source?** — **Yes, three of them, and they disagree:**

- **(i) Lexical stem** of `record_path` → 87 groups over 169 records (`aetherialcorruption` 33,
  `ghost` 20, `eldritcharmor` 16, `chthoniandevourer` 15, `basilisk` 13, `wendigocannibal` 13…).
  100% coverage, free, and it is **the reference's taxonomy verbatim** — GL-17 forbids it as a label.
- **(ii) Spawn pool** (A1) → 140 pools, 100% coverage. Family × tier. Also the reference's own.
- **(iii) Rig** (A3/A4) → 23 rigs over the 66 covered. **Contradicts (i) in 34/66 cases.**

None of these is a *derived* family. All three are the reference's authored labels. The commission's
Discipline-#41 requirement — substrate votes, no pre-imposed taxonomy — means (i) and (ii) are
**validation targets only**. (iii) is different: it is not a taxonomy, it is an *outcome*, and it is
the closest thing in the corpus to a ground-truth answer key for a fit function.

### 2.3 Substrate B identity fields (engine) — richer schema, poorer signal
`id · name · flavor_text · threat_tier · archetype_tag · energy_type · role_orientation ·
range_profile · dominant_element · max_hp · armor · elemental_resistances{fire,water,earth,wind} ·
skills[{id, name, composition_mode, role, canonical_element, effect_category,
canonical_pair_ref, energy_cost, cooldown_seconds, damage_multiplier, effects[{name,params}],
color_value, flavor_text, tier, chain_id, chain_position, parent_skill_ids,
scaling_coefficient}] · balance_metadata`

Structurally this is **the better schema** — skills are first-class, typed, elementally tagged.
Its problem is distributional, not structural (§ 4.2).

---

## 3 · SAMPLE — 10 IDENTITIES ACROSS ALL SIX STRATA

| # | name | stratum / tier | lvl | element (`damage_types`) | role (`controller`) | skills (`skill_class` @ `range_band`) | rig (body) | pools |
|---|---|---|---|---|---|---|---|---|
| 1 | **Haunted Noble** `ghost_b01` | trash / Champion | 103 | Physical\|Pierce\|Cold | `ghost_rangedbasic` | 1: AttackProjectileBurst@Medium | **`heroine01_sword1h`** | ghost_t1/t2/t3 |
| 2 | **Fleshwarped Aberration** `aetherialcorruption_c01` | trash / Champion | 103 | Physical\|Aether\|Life | `aetherialcorruption` | 3: WeaponPool_ChargedFinale · AttackProjectileRing@Medium · BuffAttackRadiusToggled | `aetherialcorruption` | aetherialbloater_t2/t3, aetherialcorruption_poison_t2/t3, aetherialcorruption_t2 |
| 3 | **Chthonian Hungerer** `chthoniandevourer_a01` | trash / Common | 102 | Physical | `chthoniandevourer` | 1: AttackWeapon@Medium | `devourer` | chthonian_t1/t2/t3, chthoniandevourer_t1, chthonian_bolvar |
| 4 | **Ugdenbog Spikeshell** `swampcrab_b01` | trash / Common | 103 | Physical\|Pierce | `swampcrab_melee` | 3: AttackWeapon@Short · AttackWave@Short · AttackWeapon@Short | `crabmonstrosity` | swampcrab_t1/t3 |
| 5 | **Moltenclaw** `sandlizard_volcanic_a01` | trash | 109 | **NOT EXTRACTED** | **NOT EXTRACTED** | **NOT EXTRACTED** | **NOT EXTRACTED** | sandlizard_volcanic_t2/t3 |
| 6 | **Stormslither** `hero/basilisk_h01` | hero / Hero | 107 | Physical\|Poison | `basilisk_melee` | 6: AttackRadius@Short · AttackWave@Medium · AttackRadiusLightning@Long · BuffAttackRadiusDuration@Any · AttackProjectileBurst@Long · … | `basilisk` | basilisk_hero |
| 7 | **Rimelord ~ Frozen** `devotion/skeleton_h06` | devotion / Hero | 107 | Physical | `skeletoncaster01` | 5: AttackWave@Medium · AttackWeapon@Short · AttackProjectile@Long · AttackProjectileRing@Medium · BuffRadiusToggled | `skeleton_01a` | devotion_heroes04 |
| 8 | **Vanoxxis Bile** `bounties/cu_bounty04` | bounty / Hero | 107 | Physical | `aetherialbloater` | 6: WeaponPool_ChargedFinale · AttackProjectileBurst@Medium · AttackWave@Short · AttackProjectileAreaEffect@Any · AttackBuff@Any · … | **`aetherialbloater`** | bounty_heroes01 |
| 9 | **The Sentinel** `boss&quest/witchgod_finalboss` | boss | 109 | **NOT EXTRACTED** | **NOT EXTRACTED** | **NOT EXTRACTED** | **NOT EXTRACTED** | witchgod_sentinel |
| 10 | **Reaper of the Lost** `nemesis/nemesis_wendigo_01` | **nemesis** | 109 | **NOT EXTRACTED** | **NOT EXTRACTED** | **NOT EXTRACTED** | **NOT EXTRACTED** | nemesis_all, nemesis_wendigo, nemesis_all_no{aetherialvanguard,beast,voidborn} |

Read rows 5 / 9 / 10 as the finding they are: **the boss and the nemesis — the two identities the
scene run most needs to get right — have no mechanical record extracted at all.** Row 1 and row 8
are the rig-divergence proof: a "ghost" on a swordswoman rig, an "outlaw bounty" (`cu_` = Coven of
Ugdenbog) on a bloater rig.

Every row's **name, threat tier, level, and pool membership are 100% available today.**

---

## 4 · CLUSTERING FEASIBILITY — VERDICT

### 4.1 Substrate A (Grim Dawn) — **CONDITIONAL**

The *shape* of the substrate is genuinely rich enough. 983 distinct skills, 60+ typed skill
classes, four range bands, ~30 controllers, pipe-list damage types, frame-exact tempo, 28
behavioural controller fields. A skills×element×role feature space over this will separate — it is
not homogeneous, and it is not thin.

**But it is 39% populated on this roster, and 0% on nemesis.** Clustering 66 of 169 and
extrapolating to the other 103 is not an emergent derivation, it is a guess wearing a table. Two
sub-findings sharpen the condition:

- `range_band` is **per attack-slot, not per monster** — a monster with 8 slots spans Short→Long.
  Any per-monster range feature must be an aggregation (modal? weighted by `chance_pct`?) and that
  aggregation choice is a **design decision, not a data one**. Route to gandalf.
- `damage_types` is a *pipe-list with `Physical` in nearly every row*. `Physical` is
  near-universal and carries no separating information. The signal is in the **non-physical
  remainder** (Aether/Life, Pierce/Cold, Poison). Any element axis must drop `Physical` as a
  stopword or it will dominate the metric. **Documented so nobody re-derives it.**

**Verdict: CONDITIONAL — unblocked by one re-run of an already-checked-in harness.**
`x1_extract.py` + `tg_lib.py` + the adapters read the `.arz` that is on this disk. Re-pointing the
roster basis from t22's 968-record band-A list to the 169-record s2 list closes the cliff. This is
hours, not a research lap. **Owner: legolas** (extraction) with the s2 roster supplied by me.

### 4.2 Substrate B (engine) — **FAIL, and this is the more important finding**

The engine's 1,108 monster records look richer and cluster worse. The distributions:

| axis | distribution | read |
|---|---|---|
| `archetype_tag` | caster 196 · brute 196 · controller 189 · swarmer 189 · sniper 169 · tank 169 | **six values, near-equal counts** |
| `dominant_element` | fire 269 · water 269 · earth 267 · wind 267 · shadow 12 · holy 12 · lightning 12 | **four values, near-equal counts** |
| `role_orientation` | damage 721 · control 147 · **null 240** | two values + 22% null |
| `range_profile` | close 434 · medium 301 · long 133 · null 240 | |

Those are **generator quotas, not a population.** 196/196/189/189/169/169 is not what emergence
looks like; it is what a round-robin looks like. Clustering this substrate will recover the
generator's own six-by-four grid and report it as a discovery. **That is a false positive waiting
to happen, and it is exactly the form-bias failure mode doc 37 diagnoses.**

`role_orientation` is additionally **22% null** and collapsed to two of the four taxonomy values
(no `support`, no `hybrid` — see memory `project_role_orientation_taxonomy`).

**Verdict: FAIL for emergent family derivation.** The engine substrate is too homogeneous *by
construction*. It is not that the data is thin — it is that the data is **uniform**, and uniform
data has no families in it. If production enemies must eventually be body-fit, the engine's
enemy generator needs a variance lap before any fit function can key off it. **Route to gandalf +
rocket.** I flag it; I do not rule on it.

### 4.3 The Grim Dawn 7-family reference grammar — GL-17 handling

Used **only** as an external-validity check per the commission, never as labels. Two checks are
available and I recommend both:

1. **Pool-partition agreement** (A1, 100% coverage) — does a substrate-derived clustering
   recover `ghost_t*` / `wendigo_t*` / `chthonian_t*` as coherent blocks? Agreement = the
   substrate is saying what the reference's designers said. Disagreement is *informative*, not
   failure.
2. **Rig-partition agreement** (A3/A4, 39% coverage) — the stronger check, because rig is the
   reference's *answer to our exact question*: given this mechanical identity, what body did a
   professional studio put it on?

**Negative result, banked so nobody re-derives it:** rig and lexical family are **not** the same
partition. 34/66 disagree. 23 rigs cover 66 identities (**~2.9 identities per body**), and
`hero01_sword1h` alone carries at least four unrelated lexical families. Two consequences:

- **A fit function keyed on family *name* is falsified before it is written.** The reference does
  not work that way.
- **Body reuse of ~3:1 is normal and professionally sanctioned.** Cross-check against drax's
  census: 163 names ÷ 137 enemy bodies = 1.19:1 — the Synty tree is **~2.4× more generous** than
  the reference's own ratio. drax's "the gap does not exist" holds with margin to spare.

---

## 5 · GAP TABLE BY OWNING SEAM

| # | Gap | Detail | Owner | Blocks | Cost |
|---|---|---|---|---|---|
| **G1** | **Baton carries no identity** | 22 fields, all positional/durability. `entity_radius_m` null ×344; no skills/element/role/family. `body_radius_role="NON-CAUSAL"` — declared out of model | **star-lord** (producer carrier) | any downstream consumer that isn't handed the CSVs separately | small — add a `record_path`-keyed identity block or a sidecar; join key already present as `archetype_tag` |
| **G2** | **s2-band extraction cliff** | 66/169 (39%); **nemesis 0/9**, hero 3/27, boss&quest 12/33. Harness + adapters + corpus all present and working | **legolas** (re-run) · roster basis from **elrond** | § 4.1 CONDITIONAL → PASS; rows 5/9/10 of the sample | hours — re-point `x1_extract.py` roster basis, no new research |
| **G3** | **No identity store exists** | Zero DB rows anywhere. 8 unversioned CSV/JSON files across 2 repos, 2 duplicated (`kc2_s1_banda_record_inputs.csv` in both `data/kc2/` and `legolas/notes/…`). No `source`/`source_date`/schema version on any of them | **elrond** | reproducible joins; any second consumer | medium — a source-anchored catalogue DB keyed on `record`, curated-from-raw, versioned per ADR-004 |
| **G4** | **Two substrates, no bridge** | Substrate A (GD, 169) and Substrate B (engine, 1,108) share no key, no vocabulary, no schema. `damage_types` (Physical\|Aether\|Life) vs `dominant_element` (fire/water/earth/wind) do not map | **elrond** (crosswalk schema) · **gandalf** (semantic ruling on the element mapping) | any fit function that must serve both fixture and production | medium — needs a design ruling before a schema |
| **G5** | **Engine substrate is quota-uniform** | 196/196/189/189/169/169 archetype; 269/269/267/267 element; `role_orientation` 22% null, 2 of 4 values used | **gandalf** (is this intended?) · **rocket** (generator variance) | § 4.2 FAIL; production-path fit | large — generator work, not data work |
| **G6** | **No mesh/model field decoded** | Rig is inferred from `basic_attack_anims` filename prefix, not read from a declared mesh field. The creature `.dbr` mesh reference is undecoded | **legolas** (decode) | rig-partition validity check at full strength | small — one more field in the existing `.arz` lap; fold into G2 |
| **G7** | **Per-monster range is underdetermined** | `range_band` is per attack-slot; 8-slot heroes span Short→Long. Aggregation rule (modal? `chance_pct`-weighted?) is unspecified | **gandalf** (design ruling) → **elrond** (implement) | the range feature in any clustering | small, but a ruling not a computation |
| **G8** | **`Physical` is a stopword** | Present in nearly every `damage_types` row; carries no separating information. Undropped, it dominates any element metric | **elrond** (curation rule, document it) | element axis validity | trivial — banked here |
| **G9** | **GL-17 premise exposure** | The 163 names are Grim Dawn's. Fitting bodies to them reproduces the reference's roster | **gandalf** (ruling) | nothing today if SB-1 is a fixture; everything if it flows to shipped content | ruling only |

---

## 6 · WHAT I RECOMMEND, IN ORDER

1. **G2 first.** It is the cheapest gap with the largest effect and it converts § 4.1 from
   CONDITIONAL to PASS. Nothing else should start before the nemesis and boss rows exist.
2. **G7 + G8 in parallel** — a one-line design ruling and a one-line curation rule, both needed
   before the first clustering run, both nearly free.
3. **G3 after G2** — build the catalogue once the field set is stable, not before. Building it
   now would version a schema against 39% of its own rows. (Per my standing discipline: defer
   schema where possible; where forced, document the assumption. I am not forced here.)
4. **G1 to star-lord as an ADR-004 request** whenever a consumer other than this recon needs
   identity on the wire. Not urgent today — the CSVs are joinable by hand.
5. **G5 and G9 to gandalf as findings, not asks.** Both are design questions wearing data
   clothes. I have stated what the data says. I do not interpret what it means.

---

*Read-only throughout. Engine tree, vendor tree, godot tree untouched — no files, no caches, no
`__pycache__` (all Python run from `/tmp` under `PYTHONDONTWRITEBYTECODE=1`). No DB writes; the
only DBs touched were listed, not opened for write. This file is the sole write.*
