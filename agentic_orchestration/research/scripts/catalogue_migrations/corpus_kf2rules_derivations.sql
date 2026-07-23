-- corpus_kf2rules_derivations.sql
-- KF-2 rdr_value derivation — stamps rdr_value + rule_id + rule_version_applied on every non-blocked
-- non-formula-only kit_numeric (pilot) + monster_numeric row, per the rules in corpus_kf2rules_rules.sql.
-- Author: gamora (rule_owner, sim-seam) | 2026-07-23 | Run: KIT-FIDELITY (KFL-9c)
-- Math note (Discipline #1): reincarnated-engine/src/reincarnated/simulation/math/kf2-rdr-normalization-convention.md
--
-- DUAL-COLUMN LAW ENFORCED BY CONSTRUCTION: every statement is an UPDATE that touches ONLY
-- {rdr_value, rule_id, rule_version_applied}. source_value is NEVER in a SET clause. Idempotent
-- (UPDATE not append; same inputs -> same outputs; re-run is a no-op-equivalent).
--
-- SEED PROTECTION: kit_numeric UPDATEs are scoped to the pilot-5 kit_ids explicitly. The 2 pre-existing
-- seed rows (poe1-glacial-hammer, poe2-walking-calamity) are NEVER in scope. Guard-assert at the tail.
--
-- RDR-UNIT CONVENTION (math note s0): rdr = source_value (IDENTITY) for every damage/HP/defense/modifier/
-- attribute/percent/geometry magnitude within the source game's own scale. The ONLY non-identity magnitude
-- transform is R-T1 (frames/cast -> casts/sec = 25/sv). R-M3 stamps the pinned constant 10.
--
-- PILOT KIT SET (for scoping):
--   'd2-firewall-sorc','d2-fire-sorc','gd-flames-of-ignaffar-purifier','poe2-bonestorm','poe1-cyclone'

-- =====================================================================================================
-- A. KIT DAMAGE-SCALE (R-K1/K2/K3/K4) — IDENTITY
-- =====================================================================================================
-- R-K1 d2_fire_dps (80)
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-K1', rule_version_applied = 1
 WHERE source_scale = 'd2_fire_dps' AND kit_id IN ('d2-firewall-sorc','d2-fire-sorc');
-- R-K2 d2_fire_hit (80)
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-K2', rule_version_applied = 1
 WHERE source_scale = 'd2_fire_hit' AND kit_id IN ('d2-firewall-sorc','d2-fire-sorc');
-- R-K3 poe2_phys_hit (80)
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-K3', rule_version_applied = 1
 WHERE source_scale = 'poe2_phys_hit' AND kit_id = 'poe2-bonestorm';
-- R-K4 poe1_effectiveness_pct_v315 + poe1_base_damage_pct_v315 (2) — 3.15 build point
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-K4', rule_version_applied = 1
 WHERE source_scale IN ('poe1_effectiveness_pct_v315','poe1_base_damage_pct_v315') AND kit_id = 'poe1-cyclone';

-- =====================================================================================================
-- B. MODIFIER / MULTIPLIER (R-M1/M2/M2b/M3/M4/M5) — IDENTITY (R-M3 pinned constant)
-- =====================================================================================================
-- R-M1 d2_pct_bonus_fire (12)
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-M1', rule_version_applied = 1
 WHERE source_scale = 'd2_pct_bonus_fire' AND kit_id IN ('d2-firewall-sorc','d2-fire-sorc');
-- R-M2 poe2_pct_more (2)
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-M2', rule_version_applied = 1
 WHERE source_scale = 'poe2_pct_more' AND kit_id = 'poe2-bonestorm';
-- R-M2b poe2_pct_increased (1)
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-M2b', rule_version_applied = 1
 WHERE source_scale = 'poe2_pct_increased' AND kit_id = 'poe2-bonestorm';
-- R-M3 pin_shard_count (1) — PINNED fixed multiplier value 10 (rdr = source_value = 10, flagged as fixed mult)
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-M3', rule_version_applied = 1
 WHERE source_scale = 'pin_shard_count' AND kit_id = 'poe2-bonestorm';
-- R-M4 poe1_attack_speed_pct (1)
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-M4', rule_version_applied = 1
 WHERE source_scale = 'poe1_attack_speed_pct' AND kit_id = 'poe1-cyclone';
-- R-M5 poe1_pct (3) + poe2_pct (3) — kit-side modifier/mitigation % leaves
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-M5', rule_version_applied = 1
 WHERE source_scale IN ('poe1_pct','poe2_pct') AND kit_id IN ('poe1-cyclone','poe2-bonestorm');

-- =====================================================================================================
-- C. ATTRIBUTE-SCALE (R-A1/A2/A3/A4/A5) — IDENTITY on coefficient/base
-- =====================================================================================================
-- R-A1 d2 attributes + life/mana coeffs (20): d2_stat, d2_flat_life, d2_flat_mana, d2_life_per_level,
--      d2_life_per_vit, d2_mana_per_level, d2_mana_per_energy
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-A1', rule_version_applied = 1
 WHERE source_scale IN ('d2_stat','d2_flat_life','d2_flat_mana','d2_life_per_level','d2_life_per_vit','d2_mana_per_level','d2_mana_per_energy')
   AND kit_id IN ('d2-firewall-sorc','d2-fire-sorc');
-- R-A2 gd attribute coefficients (15): gd_hp_per_point, gd_da_per_point, gd_oa_per_point, gd_energy_per_point,
--      gd_hpregen_per_point, gd_dmg_pct_per_point, gd_attr_per_invested_point, gd_invested_points,
--      gd_oada_base, gd_oada_level_coeff
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-A2', rule_version_applied = 1
 WHERE source_scale IN ('gd_hp_per_point','gd_da_per_point','gd_oa_per_point','gd_energy_per_point','gd_hpregen_per_point','gd_dmg_pct_per_point','gd_attr_per_invested_point','gd_invested_points','gd_oada_base','gd_oada_level_coeff')
   AND kit_id = 'gd-flames-of-ignaffar-purifier';
-- R-A3 poe2_stat_req (5) + poe2_spirit (1)
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-A3', rule_version_applied = 1
 WHERE source_scale IN ('poe2_stat_req','poe2_spirit') AND kit_id = 'poe2-bonestorm';
-- R-A4 poe1_stat_req (2)
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-A4', rule_version_applied = 1
 WHERE source_scale = 'poe1_stat_req' AND kit_id = 'poe1-cyclone';
-- R-A5 poe1_flat_life (1) — player life pool
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-A5', rule_version_applied = 1
 WHERE source_scale = 'poe1_flat_life' AND kit_id = 'poe1-cyclone';

-- =====================================================================================================
-- D. CAST/ATTACK-RATE (R-T1 UNIT-CONVERT, R-T2/T3 IDENTITY)
-- =====================================================================================================
-- R-T1 d2_frames_per_cast (14) — rdr = 25 / source_value (casts/sec). D2 = 25 fps.
UPDATE kit_numeric SET rdr_value = 25.0 / source_value, rule_id = 'R-T1', rule_version_applied = 1
 WHERE source_scale = 'd2_frames_per_cast' AND kit_id IN ('d2-firewall-sorc','d2-fire-sorc');
-- R-T2 d2_seconds (3) + poe2_seconds (1) + gd_seconds (1) — IDENTITY (seconds = RDR cadence unit)
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-T2', rule_version_applied = 1
 WHERE source_scale IN ('d2_seconds','poe2_seconds','gd_seconds')
   AND kit_id IN ('d2-firewall-sorc','d2-fire-sorc','poe2-bonestorm','gd-flames-of-ignaffar-purifier');
-- R-T3 d2_mana (60) + poe2_mana_per_sec (6) + poe1_mana (1) — IDENTITY resource economy
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-T3', rule_version_applied = 1
 WHERE source_scale IN ('d2_mana','poe2_mana_per_sec','poe1_mana')
   AND kit_id IN ('d2-firewall-sorc','d2-fire-sorc','poe2-bonestorm','poe1-cyclone');

-- =====================================================================================================
-- F. CRIT-EV LEAVES that derive IDENTITY under R-C2 (gd crit table). (R-C1/C3/C4 are formula-only, no leaf.)
-- =====================================================================================================
-- R-C2 gd_crit_mult (6) + gd_pth_pct (3) — the crit-mult tier + pth leaves the crit-weighted mean composes
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-C2', rule_version_applied = 1
 WHERE source_scale IN ('gd_crit_mult','gd_pth_pct') AND kit_id = 'gd-flames-of-ignaffar-purifier';

-- =====================================================================================================
-- G. MITIGATION LEAVES that derive IDENTITY (armour/absorption %). (Formulas R-G1/G2/G3/G5 are formula-only.)
--    gd_pct absorption leaf (70) is the anchored input R-G3 consumes; derive it IDENTITY here.
-- =====================================================================================================
-- gd_pct armor absorption (1) — anchored mitigation % leaf (consumed by R-G3 formula)
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-G3', rule_version_applied = 1
 WHERE source_scale = 'gd_pct' AND kit_id = 'gd-flames-of-ignaffar-purifier';

-- =====================================================================================================
-- CTX. Context / geometry-gating (R-CTX-BP fenced build-point context; R-CTX-GEO geometry/gating)
-- =====================================================================================================
-- R-CTX-BP poe1_effectiveness_pct_v327_context (6) — post-3.27 CONTEXT, fenced NOT-the-build-point
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-CTX-BP', rule_version_applied = 1
 WHERE source_scale = 'poe1_effectiveness_pct_v327_context' AND kit_id = 'poe1-cyclone';
-- R-CTX-GEO geometry/gating (32): d2_level (3), d2_yards (22), poe1_level (2), poe1_weapon_dps (1),
--      poe2_count (1), poe2_metres (2), poe2_metres_per_sec (1)
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-CTX-GEO', rule_version_applied = 1
 WHERE source_scale IN ('d2_level','d2_yards','poe1_level','poe1_weapon_dps','poe2_count','poe2_metres','poe2_metres_per_sec')
   AND kit_id IN ('d2-firewall-sorc','d2-fire-sorc','poe1-cyclone','poe2-bonestorm');
-- poe1_radius_units (1) — geometry, also fenced under R-CTX-GEO
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-CTX-GEO', rule_version_applied = 1
 WHERE source_scale = 'poe1_radius_units' AND kit_id = 'poe1-cyclone';

-- =====================================================================================================
-- H. MONSTER-SCALE (R-N1/N2/N3/N4) — IDENTITY
-- =====================================================================================================
-- R-N1 d2 monster (38): d2_flat_hp, d2_defense_rating, d2_phys_hit, d2_attack_rating, d2_xp
UPDATE monster_numeric SET rdr_value = source_value, rule_id = 'R-N1', rule_version_applied = 1
 WHERE source_scale IN ('d2_flat_hp','d2_defense_rating','d2_phys_hit','d2_attack_rating','d2_xp') AND game = 'd2';
-- R-N2 poe1 monster (38): poe1_flat_life, poe1_armour_rating, poe1_evasion_rating, poe1_damage, poe1_attack_time_sec
UPDATE monster_numeric SET rdr_value = source_value, rule_id = 'R-N2', rule_version_applied = 1
 WHERE source_scale IN ('poe1_flat_life','poe1_armour_rating','poe1_evasion_rating','poe1_damage','poe1_attack_time_sec') AND game = 'poe1';
-- R-N3 poe2 monster (25): poe2_flat_life, poe2_armour_rating, poe2_evasion_rating, poe2_damage, poe2_accuracy_rating
UPDATE monster_numeric SET rdr_value = source_value, rule_id = 'R-N3', rule_version_applied = 1
 WHERE source_scale IN ('poe2_flat_life','poe2_armour_rating','poe2_evasion_rating','poe2_damage','poe2_accuracy_rating') AND game = 'poe2';
-- R-N4 pct (44): monster resist/block/caps across all three games
UPDATE monster_numeric SET rdr_value = source_value, rule_id = 'R-N4', rule_version_applied = 1
 WHERE source_scale = 'pct';

-- =====================================================================================================
-- GUARD ASSERTIONS (read-only; a mismatch is a STOP-and-report)
-- =====================================================================================================
-- Seeds untouched: both pre-existing seed rows must still have rdr_value NULL + rule_id NULL.
SELECT 'GUARD seeds-untouched (expect 2 NULL)=' || COUNT(*) FROM kit_numeric
 WHERE kit_id IN ('poe1-glacial-hammer','poe2-walking-calamity') AND rdr_value IS NULL AND rule_id IS NULL;
-- Every pilot kit row derived (expect 0 NULL among the 444 pilot rows).
SELECT 'GUARD pilot-kit NULL-remaining (expect 0)=' || COUNT(*) FROM kit_numeric
 WHERE kit_id IN ('d2-firewall-sorc','d2-fire-sorc','gd-flames-of-ignaffar-purifier','poe2-bonestorm','poe1-cyclone')
   AND rdr_value IS NULL;
-- Every monster row derived (expect 0 NULL among 145).
SELECT 'GUARD monster NULL-remaining (expect 0)=' || COUNT(*) FROM monster_numeric WHERE rdr_value IS NULL;
-- source_value immutability spot: d2-fire-sorc fireball_dmg_max_lvl20 must still be its anchored source.
SELECT 'GUARD source_value-immutable spot (fireball lvl20 source)=' || source_value FROM kit_numeric
 WHERE kit_id='d2-fire-sorc' AND numeric_key='fireball_dmg_max_lvl20';
