-- corpus_kf2rules_rules.sql
-- KF-2 normalization_rule authoring — the source_scale -> RDR transform rules for the pilot-5 kits + monsters.
-- Author: gamora (rule_owner, sim-seam) | 2026-07-23 | Run: KIT-FIDELITY (KFL-9c)
-- Math note (Discipline #1, authored BEFORE this): reincarnated-engine/src/reincarnated/simulation/math/kf2-rdr-normalization-convention.md
-- Manifest: agentic_orchestration/elrond/notes/2026-07-23-kf23-rules-needed-manifest.md (sections A-H).
-- Idempotent (INSERT OR REPLACE keyed on rule_id PK). rule_owner = 'gamora' sign-off. rule_version = 1.
--
-- RDR-UNIT CONVENTION (seam call, full derivation in the math note): one RDR damage/HP/defense point =
-- one point of the source game's own number, carried 1:1 (IDENTITY) within that game's own scale. The
-- transform preserves internal ratios exactly so the fidelity gauge (realized/expected) reads a pure
-- pipeline-drift signal. Tempo scales convert UNIT (frames/cast -> casts/sec) without changing cadence
-- magnitude. Resolution formulas (hit/crit/mitigation) are anchored expressions the COMPOSITION applies;
-- their formula_ref points at the committed formula script (verbatim anchor in that script's header).
--
-- BLOCKED rules (NOT authored per manifest line 109 + charter KFL-9): R-K5 (gd FoI base, GAP-D1),
-- R-N5 (gd monster, GAP-D2), R-G4 (poe2 armour DR, GAP-B1). Their composition factors stay gap_excluded
-- in kit_composition; no kit_numeric/monster_numeric LEAF stays NULL on their account (see math note s3).

-- =====================================================================================================
-- SECTION A — Kit-side damage-scale rules (IDENTITY_v1: rdr = source_value; base-damage transforms)
-- =====================================================================================================
INSERT OR REPLACE INTO normalization_rule (rule_id, rule_version, source_scale, description, rule_owner, formula_ref, status) VALUES
('R-K1', 1, 'd2_fire_dps',
 'D2 fire damage-per-second -> RDR damage. IDENTITY_v1: rdr = source_value (dmg/sec is D2''s documented unit). Per-cast expectation (x duration) is a COMPOSITION factor, not a leaf rescale (math note s0.2). Fire Mastery mult applies via R-M1 in the chain. Anchor: rankedboost fire-skill tables.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-K1', 'active'),
('R-K2', 1, 'd2_fire_hit',
 'D2 single-hit fire damage -> RDR damage (Fire Ball, Meteor impact). IDENTITY_v1: rdr = source_value. Non-crit mean (PIN-A: D2 no spell crit). Fire Mastery mult applies via R-M1. Anchor: rankedboost.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-K2', 'active'),
('R-K3', 1, 'poe2_phys_hit',
 'PoE2 physical spell damage -> RDR damage (Bonestorm projectile + explosion components). IDENTITY_v1: rdr = source_value per component. N_shards(=10, PIN-N10) is a COMPOSITION multiplier (R-M3), applied per-release, not to the leaf. Anchor: poe2db.tw/us/Bonestorm.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-K3', 'active'),
('R-K4', 1, 'poe1_effectiveness_pct_v315',
 'PoE1 Cyclone 3.15-era build-point effectiveness/base-damage % -> RDR modifier %. IDENTITY_v1: rdr = source_value (the 59% at gem 20). WEAPON-DEPENDENT: per-hit damage = weapon_DPS x effectiveness x attack-speed; weapon DPS at build point = GAP (composition base_weapon_dps gap_excluded) so per-hit is PARTIAL. The 59% leaf is faithful. CONDUCTOR PIN #1 (3.15). Anchor: pathofexile.com forum 3078559. Covers poe1_base_damage_pct_v315 (same rule, both v315 leaves).',
 'gamora', 'corpus_kf2rules_derivations.sql#R-K4', 'active');
-- R-K5 (gd FoI base damage): BLOCKED (GAP-D1, gd Matt-fork KFL-8c/KFL-9b). NOT AUTHORED. 0 rows curated.

-- =====================================================================================================
-- SECTION B — Modifier / multiplier rules (rdr = the % value; the multiplicative/additive form is composition)
-- =====================================================================================================
INSERT OR REPLACE INTO normalization_rule (rule_id, rule_version, source_scale, description, rule_owner, formula_ref, status) VALUES
('R-M1', 1, 'd2_pct_bonus_fire',
 'D2 Fire Mastery bonus% -> RDR multiplicative fire-damage multiplier. IDENTITY_v1: rdr = source_value (the bonus %, e.g. 163). Composition applies x(1 + rdr/100) = x2.63; multiplicative, NOT crit. Applies to R-K1 + R-K2 in the chain. Anchor: rankedboost fire-mastery table.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-M1', 'active'),
('R-M2', 1, 'poe2_pct_more',
 'PoE2 "more" (multiplicative) modifier % -> RDR. IDENTITY_v1: rdr = source_value. Composition applies x(1 + rdr/100). "more" != "increased" is load-bearing PoE math (Impale magnitude 200% more). Anchor: poe2db + forum. NOTE: also governs poe2_pct_increased (additive-into-bucket) leaves via R-M2b below.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-M2', 'active'),
('R-M2b', 1, 'poe2_pct_increased',
 'PoE2 "increased" (additive) modifier % -> RDR. IDENTITY_v1: rdr = source_value. Composition sums into the increased-bucket then x(1 + sum/100) ONCE. Distinct rule from R-M2 (more) because the SEMANTICS differ (additive vs multiplicative) even though the leaf transform is identical. Cast-speed 100% increased. Anchor: poe2db + forum.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-M2b', 'active'),
('R-M3', 1, 'pin_shard_count',
 'Bonestorm N_shards per-release multiplier. PINNED value 10 (NOT a source anchor, NOT a derived quantity) -- rdr = 10 stamped as a FIXED MULTIPLIER for composition per-release expectation. PIN-N10 / CONDUCTOR PIN #5. This rule flags a fixed multiplier, not a magnitude derivation.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-M3', 'active'),
('R-M4', 1, 'poe1_attack_speed_pct',
 'PoE1 Cyclone attack-speed % -> RDR cadence factor. IDENTITY_v1: rdr = source_value (300 -> composition x3.0). TEMPO: shapes per-hit CADENCE not per-hit magnitude (per-hit gauge, charter s9). NOTE: also governs poe1_radius_units (geometry) via R-M4 scope -> handled under R-CTX-GEO for radius; attack-speed here. Anchor: poedb.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-M4', 'active'),
('R-M5', 1, 'poe1_pct',
 'PoE1/PoE2 kit-side modifier/mitigation percent leaves (crit-chance %, resist-cap %, move-speed-penalty %, impale-store %). IDENTITY_v1: rdr = source_value. These are the anchored % inputs the crit/mitigation FORMULAS (R-C3/R-C4) and cap/penalty context consume; the FORMULA combines, this leaf carries the %. Covers poe1_pct + poe2_pct. Anchor: poedb / poe2db / poe-vault (per-row).',
 'gamora', 'corpus_kf2rules_derivations.sql#R-M5', 'active');

-- =====================================================================================================
-- SECTION C — Attribute-scale rules (IDENTITY_v1 on coefficient/base; pool assembly is composition, LEVEL=GAP)
-- =====================================================================================================
INSERT OR REPLACE INTO normalization_rule (rule_id, rule_version, source_scale, description, rule_owner, formula_ref, status) VALUES
('R-A1', 1, 'd2_stat',
 'D2 Sorceress base attributes (str/dex/vit/energy) + life/mana pool coefficients -> RDR. IDENTITY_v1: rdr = source_value each. Pool = base + level x coeff + vit/energy x coeff is the COMPOSITION; character LEVEL at build point = GAP (pool not fully derivable). PIN-C3 CONFLICT ON RECORD: maxroll (+1/lvl,+2/vit) curated primary vs fextralife (+2/lvl,+3/vit) dual-anchored -- rule uses maxroll leaves; Gate-2-reviewable. Covers d2_stat + d2_flat_life + d2_flat_mana + d2_life_per_level + d2_life_per_vit + d2_mana_per_level + d2_mana_per_energy. Anchor: maxroll (PIN-C3).',
 'gamora', 'corpus_kf2rules_derivations.sql#R-A1', 'active'),
('R-A2', 1, 'gd_hp_per_point',
 'GD attribute coefficients (HP/DA/OA/energy/hpregen/dmg-%/invested-conversion + OA/DA formula base+level-coeff) -> RDR. IDENTITY_v1: rdr = source_value each. OA = (115 + 12xLvl + 0.4xCunning + flat)x(1+%OA/100) is the COMPOSITION; Lvl + gear = GAP. Invested-point x8 conversion carried as coeff. gd kit HELD (FoI base damage blocked) but attribute coeffs ARE anchored + authorable (manifest A2; only R-K5/R-N5 blocked). Covers gd_hp_per_point + gd_da_per_point + gd_oa_per_point + gd_energy_per_point + gd_hpregen_per_point + gd_dmg_pct_per_point + gd_attr_per_invested_point + gd_invested_points + gd_oada_base + gd_oada_level_coeff. Anchor: grimdawn.com official.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-A2', 'active'),
('R-A3', 1, 'poe2_stat_req',
 'PoE2 Int/Spirit gem requirements (gate, not damage) -> RDR. IDENTITY_v1: rdr = source_value. Character Int/Spirit total = GAP. Low join-key weight. Covers poe2_stat_req + poe2_spirit. Anchor: poe2db.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-A3', 'active'),
('R-A4', 1, 'poe1_stat_req',
 'PoE1 Str/Dex gem requirements (gate, not damage) -> RDR. IDENTITY_v1: rdr = source_value. Requirement scale. Anchor: poedb.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-A4', 'active'),
('R-A5', 1, 'poe1_flat_life',
 'PoE1 Cyclone player life pool -> RDR HP. IDENTITY_v1: rdr = source_value (6000 = one point of source HP per RDR HP point, s0). One-source/approx anchor (overgear build guide); carried faithfully as the player pool magnitude. Anchor: overgear.com Cyclone Slayer.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-A5', 'active');

-- =====================================================================================================
-- SECTION D — Cast/attack-rate rules (tempo -> cadence; R-T1 UNIT-CONVERTS, R-T2/T3 IDENTITY)
-- =====================================================================================================
INSERT OR REPLACE INTO normalization_rule (rule_id, rule_version, source_scale, description, rule_owner, formula_ref, status) VALUES
('R-T1', 1, 'd2_frames_per_cast',
 'D2 FCR frames/cast -> RDR casts/sec. UNIT CONVERSION (the one non-identity magnitude rule): rdr = 25 / source_value (D2 runs 25 frames/sec). e.g. 13 frames -> 1.923 casts/sec. TEMPO, not per-hit magnitude; never enters the per-hit damage denominator (charter s9). Anchor: maxroll FCR table.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-T1', 'active'),
('R-T2', 1, 'd2_seconds',
 'D2/PoE2/GD cast delay / cast time / tick interval / duration -> RDR cadence. IDENTITY_v1: rdr = source_value (seconds ARE the RDR cadence unit). Fire Wall 1.4s delay + 3.6s duration; Meteor 1.2s; Bonestorm 0.12s; FoI 0.3s tick. Covers d2_seconds + poe2_seconds + gd_seconds. Anchor: fextralife / poe2db / grimdawn synthesis.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-T2', 'active'),
('R-T3', 1, 'd2_mana',
 'Resource-cost scales -> RDR resource economy. IDENTITY_v1: rdr = source_value (channel mana/sec stays mana/sec; per-cast mana stays per-cast). NOT a damage transform. Covers d2_mana + poe2_mana_per_sec + poe1_mana. Anchor: rankedboost (per-cast) / poe2db (channel).',
 'gamora', 'corpus_kf2rules_derivations.sql#R-T3', 'active');

-- =====================================================================================================
-- SECTION E — Hit-chance resolution-formula rules (formula_ref -> committed formula script; no leaf transform)
--   These are the anchored chance-to-hit formulas the COMPOSITION multiplies by. formula_ref carries the
--   VERBATIM anchored expression (in corpus_kf2rules_formulas.sql header) or NAMES the GAP.
-- =====================================================================================================
INSERT OR REPLACE INTO normalization_rule (rule_id, rule_version, source_scale, description, rule_owner, formula_ref, status) VALUES
('R-H1', 1, 'd2_hit_chance_received',
 'D2 chance-to-hit for MOB attacks vs sorc (received). ANCHORED verbatim: min(max(200%x(AR/(AR+Dr))x(ALVL/(ALVL+TLVL)),5%),95%) -- maxroll hit-chance-mechanics + fextralife. Mob AR anchored (R-N1 leaves); sorc Defense (Dr) = GAP -> PARTIAL, named. Composition hit_chance factor references this.',
 'gamora', 'corpus_kf2rules_formulas.sql#R-H1', 'active'),
('R-H2', 1, 'd2_hit_chance_dealt',
 'D2 fire-skill hit-chance = 1 (spells bypass AR). PINNED, not anchored (PIN-C2 / CONDUCTOR PIN #3). Blanket verbatim unfindable (GAP-C2); named bypass-skill list exists. Composition dealt hit_chance = 1.',
 'gamora', 'corpus_kf2rules_formulas.sql#R-H2', 'active'),
('R-H3', 1, 'poe1_hit_chance',
 'PoE1 Cyclone accuracy/evasion chance-to-hit (entropy). "Evasion only works against attacks" ANCHORED (dealt: Cyclone is attack -> evasion applies; received: monster attacks vs player evasion). FORMULA EXPRESSION = GAP-A2 (image-only). formula_ref names GAP-A2; renders PARTIAL, says so (charter s9). Player accuracy + monster evasion inputs partial.',
 'gamora', 'corpus_kf2rules_formulas.sql#R-H3-GAP-A2', 'active'),
('R-H4', 1, 'poe2_hit_chance',
 'PoE2 Bonestorm evasion: projectile EVADABLE, explosion AoE-EXEMPT (LOAD-BEARING correction). Monster spells use monster Accuracy vs player Evasion; AoE explosion cannot be evaded. ANCHORED verbatim (formulas B2 / CONDUCTOR PIN #6). Composition splits hit_chance_projectile (evadable) vs hit_chance_explosion (=1, exempt).',
 'gamora', 'corpus_kf2rules_formulas.sql#R-H4', 'active'),
('R-H5', 1, 'gd_pth',
 'GD PTH (chance-to-hit + crit base). ANCHORED verbatim: PTH = ((((OA/((DA/3.5)+OA))x300)x0.3)+(((((OAx3.25)+10000)-(DAx3.25))/100)x0.7))-50; floor 55 -- grimdawn.com official. OA/DA inputs = GAP (build point + monster side) -> PARTIAL, named. Consumes gd_pth_pct leaves (R-A2-adjacent, IDENTITY).',
 'gamora', 'corpus_kf2rules_formulas.sql#R-H5', 'active');

-- =====================================================================================================
-- SECTION F — Crit-EV resolution-formula rules (formula_ref; the crit-% / crit-mult LEAVES derive IDENTITY)
-- =====================================================================================================
INSERT OR REPLACE INTO normalization_rule (rule_id, rule_version, source_scale, description, rule_owner, formula_ref, status) VALUES
('R-C1', 1, 'd2_crit_ev',
 'D2 crit-EV = 1 (no spell crit). PINNED (PIN-A / CONDUCTOR PIN #2). Non-crit mean. Composition crit_ev = 1 for all d2 skills.',
 'gamora', 'corpus_kf2rules_formulas.sql#R-C1', 'active'),
('R-C2', 1, 'gd_crit_mult',
 'GD crit-EV (FoI): crit chance = PTH-90; crit multiplier tier table 1.0->1.5x. gd_crit_mult (6 leaves) + gd_pth_pct (3 leaves) derive IDENTITY under this rule''s scope; the crit-weighted mean is the composition combining them. grimdawn.com official (Source E authoritative over Source D 2.0x). Crit-weighted mean (PIN-A). Covers gd_crit_mult + gd_pth_pct leaves.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-C2', 'active'),
('R-C3', 1, 'poe1_crit',
 'PoE1 Cyclone crit-EV: crit-weighted mean; crit chance ~96% top-gear (poe1_pct leaf IDENTITY) x crit MULTIPLIER = GAP -> crit-EV PARTIAL, named. Consumes poe1_pct crit_chance leaf.',
 'gamora', 'corpus_kf2rules_formulas.sql#R-C3-GAP', 'active'),
('R-C4', 1, 'poe2_crit',
 'PoE2 Bonestorm crit-EV: crit-weighted mean; base crit 15% (poe2_pct leaf IDENTITY) x (gear/passive total + multi) = GAP -> crit-EV PARTIAL, named. Consumes poe2_pct base-crit leaf.',
 'gamora', 'corpus_kf2rules_formulas.sql#R-C4-GAP', 'active');

-- =====================================================================================================
-- SECTION G — Mitigation resolution-formula rules (formula_ref; armour/resist LEAVES derive IDENTITY)
-- =====================================================================================================
INSERT OR REPLACE INTO normalization_rule (rule_id, rule_version, source_scale, description, rule_owner, formula_ref, status) VALUES
('R-G1', 1, 'poe1_armour_dr',
 'PoE1 Cyclone dealt -- target physical armour DR. ANCHORED verbatim: ArmourRed = Armour/(Armour + 10xPhysRawDmg), cap 90% -- pathofexile.com forum (formulas A1). THE loud KFL-7 case (Cyclone physical vs 28,790-35,988 armour). Target armour anchored (R-N2 poe1_armour_rating leaves, 8). Composition target_mitigation factor references this.',
 'gamora', 'corpus_kf2rules_formulas.sql#R-G1', 'active'),
('R-G2', 1, 'd2_fire_resist_mitigation',
 'D2 dealt -- target fire-resist mitigation on fire damage: dmg x (1 - fire_resist_pct/100). Act-1 Normal 0% (monster_numeric fire_resist_pct, gap_flag=normal_resist_inferred). Sorc has no native -enemy resist. Consumes monster fire_resist_pct leaves (R-N4).',
 'gamora', 'corpus_kf2rules_formulas.sql#R-G2', 'active'),
('R-G3', 1, 'gd_armor_absorption',
 'GD FoI dealt -- armor absorption. ANCHORED verbatim: "armor absorption is 70% ... 30% always through" (gd_pct=70 leaf IDENTITY). Armor RATING at build point = GAP -> PARTIAL, named. Consumes gd_pct absorption leaf.',
 'gamora', 'corpus_kf2rules_formulas.sql#R-G3', 'active'),
-- R-G4 (poe2 armour DR): BLOCKED (GAP-B1 / CONDUCTOR PIN #6). NOT AUTHORED. Dealt-% renders PRE-ARMOUR,
--   named (charter s9). The poe2 armour RATING leaf (R-N3) still derives IDENTITY; only the DR FORMULA is
--   gap_excluded (composition target_armour, comp_id 105). No monster leaf stays NULL on this account.
('R-G5', 1, 'player_mitigation_received',
 'ALL received -- player defensive-sheet mitigation (resists/armor/evasion at build point). GAP across all 5 kits (build-point player sheets un-anchored). formula_ref NAMES the GAP; received-% falls back PRE-MITIGATION and SAYS SO (charter s9 ladder: base-at-level -> else pre-mitigation). This is a documented render-state, NOT a leaf transform. No leaf derives under this rule (composition player_mitigation factors are gap_excluded).',
 'gamora', 'corpus_kf2rules_formulas.sql#R-G5-GAP', 'active');

-- =====================================================================================================
-- SECTION H — Monster-scale rules (KF-3; IDENTITY_v1: rdr = source_value in the source game''s own scale)
-- =====================================================================================================
INSERT OR REPLACE INTO normalization_rule (rule_id, rule_version, source_scale, description, rule_owner, formula_ref, status) VALUES
('R-N1', 1, 'd2_flat_hp',
 'D2 mob HP / Defense / damage / AR / XP -> RDR monster stats. IDENTITY_v1: rdr = source_value each (source scale). Feeds R-H1 (mob AR is the hit-chance input). Covers d2_flat_hp + d2_defense_rating + d2_phys_hit + d2_attack_rating + d2_xp. starter_set d2-act1-normal.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-N1', 'active'),
('R-N2', 1, 'poe1_flat_life',
 'PoE1 mob Life / Armour / Evasion / Damage / Attack-Time -> RDR. IDENTITY_v1: rdr = source_value (magnitudes); attack_time_sec carried in seconds (attacks/sec = 1/rdr is a composition read). Armour feeds R-G1 (the loud case). Covers poe1_flat_life + poe1_armour_rating + poe1_evasion_rating + poe1_damage + poe1_attack_time_sec. starter_set poe1-zone68.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-N2', 'active'),
('R-N3', 1, 'poe2_flat_life',
 'PoE2 level-scale baseline -> RDR. IDENTITY_v1: rdr = source_value (the levelscale[level] value IS the anchor). FORMULA-LEVEL anchor (gap_flag=formula_level_anchor); per-named mobs = GAP (next-lap). The armour RATING leaf derives here even though the poe2 armour DR FORMULA is blocked (R-G4/GAP-B1). Covers poe2_flat_life + poe2_armour_rating + poe2_evasion_rating + poe2_damage + poe2_accuracy_rating. starter_set poe2-levelscale.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-N3', 'active'),
('R-N4', 1, 'pct',
 'Monster resist% / block% / caps -> RDR. IDENTITY_v1: rdr = source_value (percent carried 1:1). D2 Normal resists inferred (gap_flag=normal_resist_inferred, value preserved); poe1 verbatim; poe2 caps 75%. Spans all three games'' monster pct rows. Feeds R-G2 (fire-resist mitigation).',
 'gamora', 'corpus_kf2rules_derivations.sql#R-N4', 'active');
-- R-N5 (gd monster side): BLOCKED (GAP-D2, gd Matt-fork). NOT AUTHORED. 0 rows.

-- =====================================================================================================
-- SECTION CTX — Context / geometry-gating rules (rdr = source_value, FENCED as NOT-the-damage-build-point)
--   Value carried faithfully for the compiler (geometry/gating); NEVER the per-hit damage denominator.
--   Generalizes the _v327_context fence (math note s1 CTX). Lets the KF-2 exit predicate (rdr non-NULL
--   for every kit_numeric row) be met without pretending context rows are damage rows.
-- =====================================================================================================
INSERT OR REPLACE INTO normalization_rule (rule_id, rule_version, source_scale, description, rule_owner, formula_ref, status) VALUES
('R-CTX-BP', 1, 'poe1_effectiveness_pct_v327_context',
 'PoE1 Cyclone post-3.27 effectiveness % -- CONTEXT ONLY, NOT the build point. IDENTITY_v1: rdr = source_value (value preserved for reversibility) BUT this rule FENCES the row: it must NEVER be consumed as the damage build point. The build point is the _v315 rows (R-K4, 3.15 era, CONDUCTOR PIN #1). 6 rows.',
 'gamora', 'corpus_kf2rules_derivations.sql#R-CTX-BP', 'active'),
('R-CTX-GEO', 1, 'context_geometry_gating',
 'Geometry / gating context scales (req-levels, skill radii in yards/metres, projectile-count caps, projectile speed, weapon-DPS build-point target). IDENTITY_v1: rdr = source_value (a metre is a metre; a req-level is a req-level; a radius is a radius). FENCED: geometry/gating input for the compiler, NEVER a damage/mitigation magnitude, NEVER the per-hit gauge denominator. Covers (via derivation scope) d2_level + d2_yards + poe1_level + poe1_weapon_dps + poe2_count + poe2_metres + poe2_metres_per_sec. NOTE poe1_weapon_dps is the GAP build-point weapon target: carried faithfully, but the per-hit assembly it feeds is gap_excluded (composition base_weapon_dps).',
 'gamora', 'corpus_kf2rules_derivations.sql#R-CTX-GEO', 'active');
