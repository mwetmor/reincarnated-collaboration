# MIGRATION — GD devotion payload bank (the rank axis resolved, then 7,114 rows landed)

**Author:** elrond (data steward) | **Date:** 2026-07-25 | **DB:** `agentic_orchestration/research/curated/corpus.db`
**Class:** ADDITIVE + one **re-identification** of `exact_skill`/`exact_skill_field` (prior tables PRESERVED, not dropped).
**Schema-meta version:** `gd-devotion-payloads-2026-07-25` (+ `gd-deviation-reverify-2026-07-25`, §9)
**Backup:** `corpus.db.pre-devotion-20260726T032913Z-backup` (md5 `84dd4ca4269eb750fd15f81630b9650a`), pre-DDL, Discipline #8/#11.
**Fidelity grade (era-substrate LAW §4):** **MEASURED**, basis `primary-source-datamine`. See **§7** — the LAW has a naming gap and I am flagging it rather than force-fitting.

**Scripts (reproducible, committed):**
| Script | Role |
|---|---|
| `research/scripts/gd_devotion_rank_axis_probe_2026_07_25.py` | GATE 0 round 1 — E1–E9 |
| `research/scripts/gd_devotion_rank_axis_probe2_2026_07_25.py` | GATE 0 round 2 — E10–E16, the decisive tests |
| `research/scripts/gd_devotion_field_policy_2026_07_25.py` | GATE 1 — the field policy, as code + census |
| `research/scripts/gd_devotion_bank_2026_07_25.py` | the banker (idempotent; `--verify-only` / `--dry-run`) |
| `research/scripts/gd_deviation_reverify_2026_07_25.py` | §9 docket re-verification |

**Ruling lineage.** gandalf GD-program commission 2026-07-25, off elrond's own probe
`agentic_orchestration/elrond/notes/2026-07-25-devotion-payload-probe.md`. Consuming forks ruled by
Matt the same day: **F1** (proc-binding absorbs into gear operators) and **F5** (`proc_chance` + ICD
as a pair). This bank is the spec substrate for build items **B1** and **B2** in
`agentic_orchestration/gandalf/notes/2026-07-25-gd-surface-fit-mapping.md`. Inherits **TSR-1**
(canonical value + raw provenance), **TSR-2** (one normalized exact-fields schema; per-game
extension by tag, not by table), **TSR-4** (three-tier verification), and the GD-SLICE float32
canonicalization law.

---

## 1. Bottom line

| | |
|---|---|
| Rank axis | **RESOLVED — `skill_xp_level`.** Evidence in §3. Banking proceeded. |
| Rows banked | 674 devotion headers · **7,114** payload field rows · 65 `devotion_power` · 110 `devotion_constellation` · 29 `devotion_trigger_vocab` |
| Trigger enum | **6 events × 3 target frames × 8 chance values**, confirmed from DECODED controller fields (not filename parsing); 27 of 144 combinations realized |
| Grade | MEASURED / `primary-source-datamine` @ `gd-edition-II-20260724`, 4/4 archives sha256-verified pre-parse |
| Docket 153 | **CLOSED** — surface verified BUILT on both engine seams |
| Corrections to my own probe | **three**, §8. The probe's "65 celestial powers" is 65 *records* (live count 63); its §2.2 "verbatim" Twin Fangs decode was truncated; its "max depth 48" was a boilerplate string array. |

---

## 2. What was banked, and the field policy that decided it

### 2.1 L1 — record scope

The devotion lane is 823 records. Not all of them are a skill.

| Scope | Records | Disposition |
|---|---:|---|
| `records/skills/devotion/**` skill records | **674** | **IN SCOPE** |
| `records/skills/devotion/pets/` (`Pet`, `PetPlayerScaling`) | 147 | **EXCLUDED — named, not dropped silently.** These are monster-ACTOR records (`actorHeight`, `controller`, animation tables, `characterRacialProfile`). They carry most of the lane's 2,907 distinct field names and have a different schema shape entirely. The corpus already has a monster-side store (`monster_numeric`). Routing them through a *skill* lane would be a category error. **Flagged as a future lane.** |
| `_devotiontree.dbr`, `_blank_passive.dbr` | 2 | EXCLUDED — registry/scaffolding, no behaviour. (`_devotiontree` is consumed as a *join oracle*, §4.) |

### 2.2 L2/L3 — field policy, with the residual accounted to zero

The probe warned that a naive dump gives 117,363 rows dominated by scaffolding, and that the gap is
a **curation** decision. The policy is therefore written as code (`gd_devotion_field_policy_*.py`),
not buried in a comprehension, and it prints its own census.

| Layer | Rows | |
|---|---:|---|
| naive (every non-default field on in-scope records, arrays expanded) | 16,469 | |
| **L2 deny** — scaffolding/presentation, by name/prefix/substring, each with a reason string | −8,325 | icons, sounds, FX, ragdoll, camera shake, animation, template chains, localization tags, and the rank-axis XP table (→ header) |
| **L3 string-valued payload** | −1,030 | **NOT dropped.** `canon_value` is `REAL NOT NULL`, so record-pointers and enum tags cannot live there. They are routed to `exact_skill.ext_json.string_valued_payload` and to `devotion_power`, where they are first-class. |
| unclassified residual | **0** | |
| **BANKED** | **7,114** | is_core 5,463 / extension 1,651 |

**The residual was driven to zero deliberately, and it mattered.** The first census pass left 483
rows in 71 unnamed fields. Inspecting them (rather than accepting the number) recovered genuine
behaviour that a family-regex would have discarded: `damageAbsorption*` (110 rows), the **only
authored contagion parameters in the lane** (`contagionInterval/Limit/MaxSpread/Radius` — directly
relevant to gandalf's mapping row #60, contagion/proximity spread, currently PARTIAL/GAP), wave and
drop geometry, spark chaining, GD's weapon-type proc gating (100 rows), and the damage qualifiers.
The banker **HALTs** on any unclassified payload field: the policy must be extended explicitly, never
extended by accident.

### 2.3 canon_key provenance — 2,231 curated / 4,883 mechanical

TSR-1 wants a player-facing canonical key. There are 261 distinct payload field names here, ~2× the
FoI slice's breadth, and I have not actually mapped most of them across D2/PoE. So: 32 field names
get a **curated** `canon_key` (`offensiveFireMin` → `damage_fire_min`); everything else gets a
**mechanical** snake_case key (`gd_defensive_total_speed_resistance`) and is tagged
`canon_key_provenance='mechanical'`. **The tag exists so nobody mistakes a mechanical transliteration
for a cross-game semantic claim.** Upgrading a key from mechanical to curated is a later, cheap,
additive act; silently pretending 261 GD field names are already canonical vocabulary is not
recoverable.

---

## 3. GATE 0 — the rank axis, resolved before a single row landed

Probe §4.3 flagged the hazard: Twin Fangs carries `skillMaxLevel = 1` yet 20-element damage arrays,
and max array depth across the lane was reported as 48. An unlabelled `rank` column silently poisons
every payload number, so this was gated: **resolve, or bank nothing.**

**RESOLUTION: the array axis is the power's own SKILL-EXPERIENCE LEVEL** — an auto-levelling tier
driven by accumulated skill XP, authored per-power as `skillExperienceLevels`. It is **not** a
player-bought rank, **not** devotion points spent, **not** constellation stars.

| # | Test | Result | What it rules out |
|---|---|---|---|
| E10 | per power, `len(payload array) == len(skillExperienceLevels)`? | **60 of 65 exactly; 5 have one short/long field each** (§8.3) | the axis is the XP table's cardinality |
| E11 | how many distinct XP tables? | **4**, of length **25 / 20 / 15 / 10**, used by 14 / 27 / 21 / 3 powers — matching the payload-length clusters exactly. The 10-table is the first 10 entries of the 15-table. Tier-1 constellations get 25 levels, tier-2 get 20, tier-3 get 15 or 10 (fewer, steeper levels the deeper the tree) | a single global scale |
| E12 | **CONTROL** — do player-class skills carry `skillExperienceLevels`? | **0 of 694.** FoI: `skillMaxLevel=16` + `skillUltimateLevel=26` → 26-element arrays, **no XP table** | that the two lanes share an axis. They are cleanly separated by the presence of this one field. |
| E13 | **CONTROL** — item-granted proc skills? | **0 of 2,728** | that this is a generic proc-skill mechanism |
| E6 | constellation star counts | max **8** (histogram 1–8) | "points invested in the constellation" as the axis (would need 20–25) |
| E15 | `_devotiontree.dbr` | declares 559 (`skillName`,`skillType`,`skillLevel`) triplets; **every `skillLevel` is `'0'`** | a tree-authored level |
| E9 | devotion `Skill_Passive` star nodes | **500 of 502 carry no arrays at all** | that the axis is lane-wide. It exists only on the powers. |
| E2 | where does "48" come from? | **`skillTemplates`** — a 44–48 element array of *base-template path strings*, on the boilerplate deny-list | the "second axis" worry. It dissolves. |
| E16 | monotonicity | 5,021 up / 435 down / 1,794 flat-or-single. The 435 "down" are semantically-negative fields — resist-reduction debuffs authored as negatives, cooldown-*reduction* buffs. They grow in **power** while shrinking in **value**. | a direction-blind monotonic check. §5 |

**Axis assignment as banked** (`exact_skill.rank_axis`, NOT NULL, CHECK-constrained):

| Value | Rows | Source recorded in `rank_axis_source` |
|---|---:|---|
| `skill_xp_level` | 69 | `skillExperienceLevels` in-record (65), or **inherited** from the XP-bearing parent that references the record via `buffSkillName`/`petBonusName` (4 pet-bonus riders — their array lengths match the parent's axis) |
| `none` | 605 | no rank arrays — flat scalar star-node passives and pet-bonus records |
| `bought_rank` | 1 | the migrated FoI slice — `skillMaxLevel` + `skillUltimateLevel`, no XP table |

The banker **HALTs** if any record carries arrays on an unresolved axis. It did not.

---

## 4. Schema

### 4.1 Re-identification of `exact_skill` / `exact_skill_field` — why, and what was preserved

`exact_skill.kit_id` was `PRIMARY KEY … REFERENCES canon_corpus(kit_id)`. A devotion power is **not
a corpus kit** — it is a game skill. There were three ways to land 674 of them:

- (a) mint 674 fake `canon_corpus` rows — **rejected.** It would corrupt every kit-count in the corpus.
- (b) build a separate devotion payload table — **rejected.** It abandons the TSR-2 property (ONE normalized exact-fields schema) that the FoI slice existed to prove.
- (c) **generalize the identity.** Taken.

`entity_id` (PK) + `entity_kind ∈ {corpus_kit, game_skill}`, with `kit_id` retained as a **nullable
real FK**, populated only when `entity_kind='corpus_kit'` and CHECK-enforced. The FK stays honest
where it means something instead of being weakened to fit.

**The prior tables were RENAMED, not dropped:** `exact_skill_pre_devotion_20260725` (1 row) and
`exact_skill_field_pre_devotion_20260725` (136 rows) remain readable. Compatibility views
`v_exact_skill_by_kit` / `v_exact_skill_field_by_kit` reproduce the old kit-shaped surface exactly.

New columns on `exact_skill`: `rank_axis` (NOT NULL), `rank_axis_source`, `fidelity_grade`,
`fidelity_basis`, `lane`. New on `exact_skill_field`: `field_family`, `canon_key_provenance`,
`monotonic_dir`.

### 4.2 `devotion_power` — 65 rows, the trigger surface B1 keys on

`power_record` PK · `entity_id` → payload · `power_role` · `devotion_node_record` ·
`constellation_record` · `trigger_event` · `target_frame` · `proc_chance_pct` · `trigger_param` ·
`auto_target_radius` · `icd_sec` · `icd_is_rank_array` · `rank_axis` · `rank_axis_max` ·
`is_pet_power` · **`autocast_record`** · provenance.

`autocast_record` stores the controller `.dbr` path **verbatim** alongside the decoded fields — the
table is *derived* (one `read_record` hop), so per the reversibility principle its input is kept.

### 4.3 `devotion_constellation` — 110 rows, the point economy

`affinity_given_{1,2,3}` + names, `affinity_required_{1,2,3}` + names and their totals, `tier`,
`star_count`, `celestial_power_count`, plus **`buttons_json`** and **`links_json`** preserving the
raw `devotionButton*` / `devotionLinks*` fields. The tree topology is therefore *retained* without
minting the `devotion_node` table the probe deferred — raw now, normalized later if a consumer needs it.

Totals as banked: **360 affinity given, 1,000 affinity required** across 110 constellations;
559 stars; tier 1 = 50 constellations / 195 stars / 14 powers · tier 2 = 38 / 228 / 27 ·
tier 3 = 21 / 136 / 22.

### 4.4 `devotion_trigger_vocab` — 29 rows, the documented enum surface

**This is the table gandalf's B1 spec keys on.** One row per distinct autocast controller, with
`power_count` (all 65 records) and `live_power_count` (the real powers) kept apart.

Derived from **decoded controller fields**, never from filename parsing — `cast_@selfat45%health_100%`
decodes to `triggerType='LowHealth'` + `triggerParam=45.0`, and the filename would not have told us
`triggerParam` exists at all.

| Axis | Cardinality | Values (with live-power counts) |
|---|---:|---|
| `trigger_event` | **6** | `AttackEnemy` 35 · `HitByEnemy` 13 · `AttackEnemyCrit` 9 · `Block` 3 · `LowHealth` 2 · `HitByMelee` 1 |
| `target_frame` | **3** | `Enemy` 33 · `Self` 29 · `EnemyLocation` 1 |
| `proc_chance_pct` | **8** | 15 · 20 · 25 · 30 · 33 · 35 · 50 · 100 |
| `trigger_param` | optional | present ONLY on `LowHealth`: 40 / 45 / 50 (% health threshold) |
| `auto_target_radius` | 3 | 22.0 (enemy-framed) · 5.0 (self-framed) · 15.0 (one case); **absent on `LowHealth`** |

**27 of 144 theoretical combinations are realized.** The probe's design read — 6 × 3 × 8 — is
confirmed, and holds identically on the live-power subset. The one addition the probe did not name:
**`trigger_param` is a fourth, optional dimension.** A B1 spec that models only (event × frame ×
chance × ICD) cannot express `LowHealth@45%`.

ICD (`skillCooldownTime`) is present on **57 of 63** live powers, ranging **0.1 s – 60 s**. On some
powers it is itself level-scaled (`icd_is_rank_array`), e.g. a 50 s cooldown falling to 45 s.
**F5 ruled `proc_chance` + ICD as a pair; the source agrees — but the source also makes the ICD a
scaling quantity, not a constant.**

---

## 5. Verification

- **G3 EDITION PIN (new gate, run BEFORE parsing).** SHA-256 of all four `.arz` verified against the Edition-I freeze fingerprint §3 and the Edition-II cut record §3. **4/4 match.** Every banked row's `source_version` carries the composite pin `gd-edition-II-20260724; depot=…; manifest=…; arz_sha256=…`. Probe §4.4 flagged that it had skipped this; the gate closes it. A silent edition drift would poison the bank invisibly, so this fires first and HALTs.
- **G4 in-pipe asserts, every row:** non-null; orphan-header; `canon_key` PK-collision (HALT, never dedupe); ranked rows forbidden on `rank_axis='none'`; trigger-surface completeness; constellation-join completeness. **GREEN.**
- **G5 read-back byte-match from SQLite, float32-canonical:** **20/20 PASS** (13 field anchors + 7 `devotion_power` anchors). `integrity_check ok`, `foreign_key_check` clean.
- **Direction-aware monotonicity.** `monotonic_dir ∈ {up,down,flat,none}` was added because the FoI-era `monotonic_class` (1 = non-decreasing) would have flagged 435 correctly-authored rows as defects. A resist-reduction debuff that goes −4 → −13 across levels is *growing*, and the schema now says so instead of the assert lying about it.

---

## 6. Reversibility

1. **Re-run (intended).** `python3 research/scripts/gd_devotion_bank_2026_07_25.py` is **idempotent**: it detects a prior run, reverses that run's table swap, and re-lands. Verified by an actual second apply.
2. **Restore.** `corpus.db.pre-devotion-20260726T032913Z-backup` (md5 `84dd4ca4269eb750fd15f81630b9650a`); §9's backup is `corpus.db.pre-devreverify-20260726T033140Z-backup` (md5 `da1547fb4fa996a372ff943d77f3116c`).
3. **Drop.** The three devotion tables are additive and isolated. Undoing the re-identification is a rename back from `*_pre_devotion_20260725`, which is exactly what the idempotency path does.
4. **Raw preserved throughout.** `raw_field` / `raw_value` per row; `autocast_record`, `buttons_json`, `links_json` verbatim; string-valued payload in `ext_json` rather than discarded. No transform is destructive.

---

## 7. Fidelity grade — and a naming gap in the LAW, flagged not fudged

Era-substrate LAW §4 gives three grades: **MEASURED** ("verified against a live game oracle
(fixtures, L0–L5 ladder)"), **MODEL-VERIFIED** ("verified against a maintained external
model/calculator"), **AUTHORED**.

**Banked as `fidelity_grade='MEASURED'`, `fidelity_basis='primary-source-datamine'`.**

Reasoning, stated so it can be overruled:
- **MODEL-VERIFIED is plainly wrong here.** That grade covers community models (Path of Building, D2 formula docs). These rows come from the game's own database — the artifact those models are *derived from*. The GD-SLICE run already demonstrated primary source **beating** the community model (grimtools reports 60 ranks for FoI; the `.arz` says 26).
- **MEASURED under a literal reading is an overclaim**, because no L0–L5 fixture has been run against a devotion payload.
- So **the LAW has no term for a pinned primary-source datamine**, which is why `fidelity_basis` exists as a second column rather than a new grade invented in a migration doc. Minting canon grades is gandalf's call, not mine.

**The distinction is real and worth naming**, because the two fail differently: a live-oracle
measurement cannot be wrong about what the game does; a datamine **can** be wrong about *which
record the game actually uses*. This run met that failure mode head-on — two records in this very
lane are authored, complete, decodable, and **never referenced by anything** (§8.1). A fixture would
have caught them instantly; only an all-records reference scan caught them here.

**REQUEST TO GANDALF:** name the sub-grade in LAW §4 (e.g. `MEASURED (primary-source)` vs
`MEASURED (live-oracle)`). Until then `fidelity_basis` carries it per row.

---

## 8. Three corrections to my own probe note

Recorded plainly. Each is a case where the probe's number was right about the file and wrong about
the world, and each would have propagated into a spec.

### 8.1 "65 celestial powers" is 65 RECORDS. The live count is **63**.

`power_role` on `devotion_power`:

| Role | n | What it is |
|---|---:|---|
| `tree_node` | 52 | the devotion tree node carries the autocast directly |
| `buff_half` | 11 | the tree node carries **no** autocast; it delegates via `buffSkillName` to a buff record that does. **The pair is one power.** `devotion_node_record` records the node. |
| `unreferenced` | **2** | `tier3_01f_skill_old` ("Aeon's Hourglass - Time Stop") and `tier3_01f_skill_cooldownreduction` ("Time Dilation"). **A scan of all 82,131 union records found ZERO inbound references to either.** Retired design iterations left in the database. The live power is `tier3_01f_skill.dbr` (`Skill_RefreshCooldown`). |

The honest query is `COUNT(DISTINCT devotion_node_record) WHERE power_role <> 'unreferenced'` = **63**.
`COUNT(*)` reads 65 and silently includes two dead records. Likewise the probe's "62 with ICDs" is
**57 of 63** live.

### 8.2 The probe's §2.2 "VERBATIM PROOF" was truncated — the G5 gate caught it

The first apply FAILED 3/17 anchors. Per the GD-SLICE law the failure was HALT-diagnosed and the
layer named: **the ORACLE, not the parse.** The probe note transcribed Twin Fangs' **25**-element
arrays as 20 elements and labelled `skillExperienceLevels` "20 entries" when it holds 25.

The probe's headline spec sentence is therefore wrong. Corrected from the archive:

> Twin Fangs fires on a 20% chance when you attack an enemy (`AttackEnemy`, `chanceToRun=20`), on a
> 0.6 s ICD, launching 2 fully-piercing projectiles 10° apart at 22 wu auto-target radius, dealing
> **128–221 vitality + 165 pierce + 22% weapon damage at level 25 of 25** — not "108–186 vitality +
> 140 pierce + 20% weapon damage at rank 20 of 20". Life leech does max at 40%, and is the one
> short array: 20 levels authored against a 25-level axis.

The banked rows were correct from the first run; only my hand-transcribed oracle was wrong. **The
anchors in the banker are now read from the archive, not from the note.**

### 8.3 "Max rank-array depth 48" was a boilerplate string array

The 44–48 element arrays are `skillTemplates` — engine base-template path chains. Not an axis. The
probe's "at least one lane has a different axis again" concern dissolves entirely.

**The five length mismatches that DO exist** are single fields authored short (or, twice, long)
against their power's axis — `offensiveLifeLeechMin` 20 in a 25-level power, `offensiveStunChance`
15 in a 20-level power, etc. Two rows carry `rank > rank_count`; they are banked **verbatim** per
reversibility and reported by the banker rather than clamped.

---

## 9. Docket re-verification — 153 CLOSED, and a second stale row found

Script: `research/scripts/gd_deviation_reverify_2026_07_25.py`. Schema-meta `gd-deviation-reverify-2026-07-25`.

**Design of the correction.** `kit_deviation.deviation_class` records what was true **when the row
was authored** (2026-07-22, VDM-2 W4). Overwriting it would destroy the authored claim and leave the
corpus unable to answer *"what did we believe then, and what changed?"* — precisely the question a
stale-docket incident should leave answerable. So the migration is **additive**: three nullable
columns (`resolution_status`, `resolution_evidence`, `resolution_date`) carry current truth
**alongside** the authored claim. NULL = not re-verified. `deviation_class` values are **unchanged**.

**Authority boundary held.** Establishing whether an engine surface *exists* is evidentiary (mine).
Deciding whether an existing-but-partial surface still counts as a deviation is a **design call**
(gandalf's). Unambiguous rows are resolved; partial ones are marked and routed, never silently flipped.

| dev | kit | docket | resolution | evidence |
|---:|---|---:|---|---|
| **818** | `gd-retaliation-warlord` | **153 → CLOSED** | **`surface-built-gap-closed`** | Verified read-only in engine source: `generation/resource_economy.py:185` sub-shape `stack-fill`, comment reads *"D2 rage-on-damage / **GD retaliation** stack builder"*; `:87-88` `reflect_damage_fraction` (≤1.00 LOCKED) + `reflect_scaling_stat`; `simulation/damage_resolver.py:502` *"Apply Wave-C TH damage-taken-converts reflect"*; `generation/bc_target_composer.py:364` *"damage-taken-converts → LIFTED (Wave-C)"*. Design verdict: gandalf mapping §1.2 row 68 = **FIT**. |
| **797** | `gd-berserker-wereforms` | 149 open | **`cause-void-recrawl-required`** | **A second stale row, found by re-verifying rather than by anyone reporting it.** The row's stated cause was *"the source content does not yet exist — Fangs of Asterkarn is unshipped."* That is now false. `GDX3.arz` is banked and byte-verified this run: 24,178 records including **333 wereform/berserker records** and a `playerclass10` skill lane (40 records) — the new mastery. **The deviation is NOT thereby resolved:** no dossier exists against the now-held source. **Routes to legolas: Mode B re-crawl against gdx3, then re-derive.** |
| 799, 815, 817, 821 | blight-fiend-ritualist, pet-conjurer, reap-spirit, skeleton-ritualist | 150–152, 154 open | `partial-surface-class-under-review` | BUILT: `delivery=SUMMON` (`generation/summon_economy.py:215,261`); one-summon-one-decl bridge (`proxy_vocabulary_bridge.py:243`); **proxy bins LIFTED** — `bc_target_composer.py:113` `_DEFERRED_PROXY_BINS = frozenset()`. NOT BUILT: proxy **P2 nav/command** (autonomous behaviour grammar), a named OPEN Matt thread. So `engine_inexpressible` (= no native expression *at all*) is now too strong — hosting and emission exist, autonomy does not. **Whether the residual is `engine_inexpressible` or `param_gap` is gandalf's call; deliberately not made here.** |

---

## 10. Discharged: the probe's §4.2 soft-count obligation

The probe warned that *"any kit-count over devotion procs is soft"* because kit prose conflates
constellations with celestial powers. That is now reproducible from banked structure
(`census_refinement()` in the banker). Of the **41 GD kits**:

| | kits |
|---|---:|
| name a **celestial power** (an actual proc) | **12** |
| name a **constellation** | 21 |
| name **either** (touch the devotion system) | **26** (63%) |
| name **only** a constellation | 14 |

**The census's "18 kits / 44% devotion procs" sat between two different true numbers.** The
devotion *system* footprint is larger (26, 63%); the *named-proc* subset is smaller (12, 29%). The
mechanism's #2 ranking is untouched — it strengthens — but **B2 must not be specced off a kit count
that mixes the two.**

**Two curation defects in my own first-pass query, both found and fixed before publishing:**
1. **Unscoped scan.** Many GD constellation names are generic ARPG nouns (Assassin, Berserker, Hammer, Tempest, Spider, Viper, Widow, Huntress, Anvil). An unscoped substring scan credited **48 PoE/TL/TQ kits** with devotion mentions. Scan is now scoped to GD kits; the ambiguous single-word names are printed so the hazard is visible.
2. **Substring, not word-boundary.** `gd-ravenous-earth-oppressor` was credited with the constellation **"Raven"** — because "Raven" is inside "**Raven**ous". Matching is now word-boundary with an apostrophe guard. With the fix, that kit correctly matches **"Twin Fangs"** — the probe's own worked example — from `canon_corpus.fidelity_notes`, a table the first pass did not even scan.

*(A third bug, fixed in the same pass: the scan iterated a cursor while re-executing `PRAGMA` on the
same cursor, silently truncating the outer loop and under-reporting counts. Table list is now
materialized first.)*

---

## 11. What remains open

1. **Devotion→skill BINDING is not in the `.arz`, and no crawl will find it** (probe §4.1, unchanged). The *trigger condition* is fully attested; *which skill the player binds a power to* is a save-game/runtime choice. **A design question for B2, not a data gap.**
2. **The pet-actor lane (147 records)** is excluded and unbanked. If pet-scaling numbers are needed, that is a monster-side lane against `monster_numeric`, not this schema.
3. **`devotion_node` (normalized tree topology)** still deferred. Raw topology is preserved in `devotion_constellation.links_json`/`buttons_json`, so building it later needs no re-parse.
4. **4,883 mechanical `canon_key`s** await curation as D2/PoE adapters reveal which concepts are genuinely cross-game.
5. **LAW §4 sub-grade naming** — §7, routed to gandalf.
6. **Docket 149** — legolas gdx3 re-crawl; **dockets 150–152, 154** — class call to gandalf.

## Boundary note

Change to elrond's own data layer (`corpus.db`) only. No engine telemetry schema, no engine source —
engine files were read **read-only** for §9 evidence. The `.arz` archives are read-only vendor data.
No ADR-004 cross-seam request. DB file is gitignored; the committed artifacts are this note, the five
scripts, and the `corpus_schema_meta` records inside the regenerable DB.
