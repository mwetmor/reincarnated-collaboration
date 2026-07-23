# KF-2/3 Rules-Needed Manifest — normalization_rule dispatch substrate for gamora/star-lord

**Author:** elrond (data steward) | **Date:** 2026-07-23 | **Run:** KIT-FIDELITY (KFL-8d)
**For:** the `rule_owner` sim-seam (gamora / star-lord) — the KF-2 normalization-rule lane.
**Companion:** MIGRATION `agentic_orchestration/research/curated/MIGRATION-kf23-monster-composition-2026-07-23.md` ·
composition ledger `kit_composition` table · population scripts under `research/scripts/catalogue_migrations/corpus_kf23_*.sql`.

---

## What this manifest is

elrond curated the pilot-5 kit-side (`kit_numeric`, 444 rows) + monster-side (`monster_numeric`, 145 rows)
under the dual-column law: **`source_value` immutable + verbatim anchor; `rdr_value` NULL.** The
normalization-rule lane now authors the `normalization_rule` rows (`rule_id`, `source_scale`, `formula_ref`
pointer, `rule_owner` sign-off, `status`) that derive `rdr_value` for every curated row. **elrond does NOT
author rules or derive rdr_values** — this manifest is the hand-off: one entry per distinct `source_scale` →
RDR transform encountered, the anchored resolution formula each rule must implement, and the row-count depending
on each. Every KF-2/KF-3 exit predicate requires `rdr_value` non-NULL under an `status='active'` rule with owner
sign-off; this manifest enumerates exactly which rules that demands.

**Anchored resolution formulas are first-class (KFL-7):** every hit/crit/mitigation formula a rule applies is
listed with its verbatim anchor (or its GAP id if un-anchorable). The composition ledger (`kit_composition`)
carries the per-kit per-direction factor chains those formulas compose into.

---

## A. Kit-side damage-scale rules (the base-damage transforms)

| # | source_scale | rows | RDR transform the rule must author | anchored formula / note |
|---|---|---|---|---|
| R-K1 | `d2_fire_dps` | 80 | D2 fire damage-per-second → RDR damage. DoT: expected-per-cast = dps × duration (Fire Wall 3.6s; Meteor burn duration=GAP). Fire Mastery mult applies (see R-M1). | dmg/sec is the game's documented unit; tick rate GAP-C5 (per-tick excluded, per-cast gauge). |
| R-K2 | `d2_fire_hit` | 80 | D2 single-hit fire damage → RDR damage (Fire Ball, Meteor impact). Non-crit mean (Pin A). Fire Mastery mult applies. | single-hit impact; no DoT. |
| R-K3 | `poe2_phys_hit` | 80 | PoE2 physical spell damage → RDR damage (Bonestorm proj + explosion). Per-release = N_shards(=10, PIN-N10) × (proj+expl). | two-component; 200% Impale Magnitude rider (see R-X). |
| R-K4 | `poe1_effectiveness_pct_v315` (+`poe1_base_damage_pct_v315`) | 2 | PoE1 Cyclone: RDR damage = weapon_DPS × effectiveness(59% at gem20, 3.15) × attack-speed(×3.0). WEAPON-DEPENDENT — weapon DPS at build point = GAP. | CONDUCTOR PIN #1 (3.15 build point). `_v327_context` rows (6) are CONTEXT-ONLY — the rule must NOT consume them as the build point. |
| R-K5 | gd FoI base damage | 0 rows curated | GD Flames of Ignaffar per-rank fire/burn damage → RDR. **NO kit_numeric rows exist** (FoI rank table FULL GAP, kit HELD PIN #8). Rule is BLOCKED until the gd Matt-fork resolves (KFL-8c). | GAP-D1. Do not author until FoI rank table lands. |

## B. Modifier / multiplier rules

| # | source_scale | rows | RDR transform | anchored formula / note |
|---|---|---|---|---|
| R-M1 | `d2_pct_bonus_fire` | 12 | Fire Mastery bonus% → multiplicative fire-damage multiplier (e.g. +163% → ×2.63). Applies to R-K1 + R-K2. | rankedboost fire-mastery table; multiplicative, NOT crit. |
| R-M2 | `poe2_pct_more` (2) · `poe2_pct_increased` (1) | 3 | PoE2 "more" (multiplicative) vs "increased" (additive) modifier semantics → RDR. Impale magnitude (200% more) + cast-speed (100% increased). | poe2db + forum; "more"≠"increased" is load-bearing PoE math. |
| R-M3 | `pin_shard_count` | 1 | N_shards multiplier for Bonestorm per-release expectation. **PINNED value 10, not a source anchor.** | PIN-N10 / CONDUCTOR PIN #5. |
| R-M4 | `poe1_attack_speed_pct` (1) · `poe1_radius_units` (1) | 2 | Cyclone attack-speed ×3.0 (tempo, shapes per-hit cadence not per-hit magnitude — per-hit gauge, charter §9). | poedb; tempo factor. |

## C. Attribute-scale rules (character stat → derived-stat transforms)

| # | source_scale | rows | RDR transform | anchored formula / note |
|---|---|---|---|---|
| R-A1 | `d2_stat` (8) · `d2_flat_life` (2) · `d2_flat_mana` (2) · `d2_life_per_level` (2) · `d2_life_per_vit` (2) · `d2_mana_per_level` (2) · `d2_mana_per_energy` (2) | 20 | D2 Sorceress life/mana pool from base + level + vit/energy. Life = 40 + level×1 + vit×2 (PIN-C3 maxroll primary). | **CONFLICT ON RECORD (PIN-C3):** maxroll +1/level,+2/vit (curated primary) vs fextralife +2/level,+3/vit (dual-anchored annotation). Rule uses maxroll; conflict is Gate-2-reviewable. Character LEVEL at build point = GAP (pool not fully derivable). |
| R-A2 | gd `gd_hp_per_point` (3) · `gd_da_per_point` (1) · `gd_oa_per_point` (1) · `gd_energy_per_point` (1) · `gd_hpregen_per_point` (1) · `gd_dmg_pct_per_point` (2) · `gd_attr_per_invested_point` (1) · `gd_invested_points` (3) · `gd_oada_base` (1) · `gd_oada_level_coeff` (1) | 15 | GD OA/DA/HP from attributes. **OA = (115 + 12×Level + 0.4×Cunning + FlatBonuses)×(1+%OA/100); DA symmetric on Spirit.** Invested-point ×8 conversion. | grimdawn.com official (formulas anchored verbatim in kit_composition refs). Build-point Level + gear bonuses = GAP → OA/DA totals not fully derivable (kit HELD anyway). |
| R-A3 | `poe2_stat_req` (5) · `poe2_spirit` (1) | 6 | PoE2 Int/Spirit requirements (gate, not damage). Int scales 4→157 per gem; character Int total = GAP. | poe2db; requirement scale, low join-key weight. |
| R-A4 | `poe1_stat_req` (2) | 2 | PoE1 Str/Dex gem requirements (gate, not damage). | poedb; requirement scale. |

## D. Cast/attack-rate rules (tempo → cadence)

| # | source_scale | rows | RDR transform | anchored formula / note |
|---|---|---|---|---|
| R-T1 | `d2_frames_per_cast` | 14 | D2 FCR frames/cast → casts/sec (25/frames). Tempo, not per-hit magnitude. | maxroll FCR table; D2 uses frames not multipliers. |
| R-T2 | `d2_seconds` (3) · `poe2_seconds` (1) · `gd_seconds` (1) | 5 | Cast delay / cast time / tick interval → cadence. Fire Wall 1.4s delay + 3.6s duration; Meteor 1.2s; Bonestorm 0.12s; FoI 0.3s tick. | fextralife / poe2db / grimdawn synthesis. |
| R-T3 | `poe2_mana_per_sec` (6) · `d2_mana` (60) · `poe1_mana` (1) | 67 | Resource-cost scales → RDR resource economy (channel mana/sec vs per-cast mana). Not a damage transform. | poe2db (channel) / rankedboost (per-cast). |

## E. Hit-chance resolution-formula rules (KFL-7 first-class formula anchors)

| # | scope | RDR transform the rule must implement | anchored formula |
|---|---|---|---|
| R-H1 | D2 (both sorcs, received) | D2 chance-to-hit for MOB attacks vs sorc. | **`min(max(200%×(AR/(AR+Dr))×(ALVL/(ALVL+TLVL)),5%),95%)`** — maxroll hit-chance-mechanics + fextralife (formulas C1). Mob AR anchored (`d2_attack_rating`, 4 rows: Fallen/Zombie=8); sorc Defense (Dr) = GAP. |
| R-H2 | D2 (both sorcs, dealt) | D2 fire-skill hit-chance = 1 (spells bypass AR). **PINNED, not anchored.** | PIN-C2 / CONDUCTOR PIN #3. Blanket verbatim unfindable (GAP-C2); named bypass-skill list exists. |
| R-H3 | PoE1 (Cyclone dealt + received) | PoE1 accuracy/evasion chance-to-hit (entropy system). Evasion applies to ATTACKS only. | Entropy mechanic + "Evasion only works against attacks" ANCHORED (formulas A2); **formula EXPRESSION = GAP-A2 (image-only)**. Player accuracy + monster evasion inputs partial. |
| R-H4 | PoE2 (Bonestorm dealt + received) | PoE2 evasion: **projectile EVADABLE, explosion AoE-EXEMPT** (LOAD-BEARING correction). Monster spells use monster Accuracy vs player Evasion. | "evade any incoming projectile or strike… whether… an arrow… or a fireball"; AoE exception ANCHORED verbatim (formulas B2 / CONDUCTOR PIN #6). |
| R-H5 | GD (FoI dealt + received) | GD PTH (chance-to-hit + crit). | **`PTH = ((((OA/((DA/3.5)+OA))×300)×0.3)+(((((OA×3.25)+10000)−(DA×3.25))/100)×0.7))−50`; floor 55** — grimdawn.com official ANCHORED verbatim. OA/DA inputs = GAP (build point + monster side). |

## F. Crit-EV resolution-formula rules

| # | scope | RDR transform | anchored formula |
|---|---|---|---|
| R-C1 | D2 (all d2 skills) | Crit-EV = 1 (no spell crit). | Pin A / CONDUCTOR PIN #2. Non-crit mean. |
| R-C2 | GD (FoI) | Crit chance = PTH−90; crit multiplier tier table 1.0→1.5x. | grimdawn.com official (Source E authoritative over Source D 2.0x). `gd_crit_mult` (6 rows) + `gd_pth_pct` (3 rows). Crit-weighted mean (Pin A). |
| R-C3 | PoE1 (Cyclone) | Crit-weighted mean: crit chance ~96% top-gear × crit multiplier. | `poe1_pct` crit_chance anchored; **crit MULTIPLIER = GAP** → crit-EV partial. |
| R-C4 | PoE2 (Bonestorm) | Crit-weighted mean: base crit 15% × (gear/passive + multiplier). | `poe2_pct` base 15% anchored; total crit chance + multi = GAP → crit-EV partial. |

## G. Mitigation resolution-formula rules (KFL-7 first-class formula anchors)

| # | scope | RDR transform | anchored formula |
|---|---|---|---|
| R-G1 | PoE1 (Cyclone dealt — target armour) | PoE1 physical armour DR. **THE loud KFL-7 case** (Cyclone physical vs 28,790–35,988 verbatim armour — unformalized, dealt-% drifts ×2–5). | **`ArmourRed = Armour/(Armour + 10×PhysRawDmg)`, cap 90%** — pathofexile.com forum ANCHORED verbatim (formulas A1). Target armour anchored (`poe1_armour_rating`, 8 rows). |
| R-G2 | D2 (both sorcs dealt — target fire resist) | Target fire-resist mitigation on fire damage. | `pct` fire_resist_pct (Act-1 Normal 0%, gap_flag=normal_resist_inferred). Sorc has no native -enemy resist. |
| R-G3 | GD (FoI dealt) | Armor absorption. | "armor absorption is 70% … 30% always through" ANCHORED (`gd_pct`). Armor RATING at build point = GAP → partial. |
| R-G4 | PoE2 (Bonestorm dealt — target armour) | **GAP-EXCLUDED.** PoE2 armour DR formula un-anchored. | GAP-B1 / CONDUCTOR PIN #6. Dealt-% renders PRE-ARMOUR, named (charter §9). Do not author until B1 anchor lands. |
| R-G5 | ALL (received — player mitigation) | Player defensive-sheet mitigation (resists/armor/evasion at build point). | **GAP across all 5 kits** (build-point player sheets un-anchored). Received-% falls back PRE-MITIGATION, says so (charter §9 ladder). |

## H. Monster-scale rules (KF-3 — monster stat → RDR)

| # | source_scale | rows | RDR transform | note |
|---|---|---|---|---|
| R-N1 | `d2_flat_hp` (10) · `d2_defense_rating` (5) · `d2_phys_hit` (14) · `d2_attack_rating` (4) · `d2_xp` (5) | 38 | D2 mob HP / Defense / damage / AR / XP → RDR monster stats. | starter_set d2-act1-normal. Feeds R-H1 (mob AR is the hit-chance input). |
| R-N2 | `poe1_flat_life` (8) · `poe1_armour_rating` (8) · `poe1_evasion_rating` (4) · `poe1_damage` (10) · `poe1_attack_time_sec` (8) | 38 | PoE1 mob Life / Armour / Evasion / Damage / Attack-Time → RDR. Attack-time inverts to attacks/sec. | starter_set poe1-zone68. Armour feeds R-G1 (the loud case). |
| R-N3 | `poe2_flat_life` (5) · `poe2_armour_rating` (5) · `poe2_evasion_rating` (5) · `poe2_damage` (5) · `poe2_accuracy_rating` (5) | 25 | PoE2 level-scale baseline → RDR. **FORMULA-LEVEL anchor** (gap_flag=formula_level_anchor): RDR = level-scale[monster_level] × creature_multiplier. Per-named mobs = GAP (next-lap). | starter_set poe2-levelscale. |
| R-N4 | `pct` (monster resist/block/caps, 44 rows) | 44 | Monster resist% / block% / caps → RDR. D2 Normal resists inferred (gap_flag); poe1 verbatim; poe2 caps 75%. | spans all three games. |
| R-N5 | GD monster side | 0 rows | GD Act-1 monster stats → RDR. **NO rows (FULL GAP).** Rule BLOCKED until gd Matt-fork (KFL-8c). | GAP-D2. |

---

## Row-count roll-up (what each lane owes rdr_value for)

- **kit_numeric pilot rows needing rdr_value:** 444 (d2-firewall 106 · d2-fire 188 · poe1-cyclone 20 · poe2-bonestorm 104 · gd 26). Of these, the 6 `_v327_context` poe1 rows + the `pin_shard_count` row are special (context / pinned) — the rule lane should mark context rows NOT-for-derivation and the pin row as a fixed multiplier.
- **monster_numeric rows needing rdr_value:** 145 (d2 58 · poe1 58 · poe2 29).
- **Formulas needing a `formula_ref` transform script:** R-H1..H5 (5 hit) · R-C1..C4 (4 crit) · R-G1..G5 (5 mitigation). 14 resolution-formula transforms; 3 are GAP-blocked (R-H3 expression GAP-A2, R-G4 GAP-B1, R-G5 player-sheet GAP) and render partial/pre-mitigation per charter §9.
- **BLOCKED rules (do not author until an anchor/fork lands):** R-K5 + R-N5 (gd, Matt-fork KFL-8c) · R-G4 (poe2 armour, GAP-B1).

## Dual-column discipline reminder for the rule lane

`source_value` NEVER mutates. Author `normalization_rule` rows → derive `rdr_value` → set `rule_id` +
`rule_version_applied` on each dependent kit_numeric/monster_numeric row. A `rule_version` bump re-derives all
dependents. The composition ledger (`kit_composition`) is the authoritative map of which formula composes into
which factor of which kit's expected value — read it alongside this manifest.
