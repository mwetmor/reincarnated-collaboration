-- corpus_kf23_monster_poe1.sql
-- KF-3 monster-side population — PoE1 zone-level-68 starter set.
-- Author: elrond | 2026-07-23 | Source note: 2026-07-23-kf23-harvest-poe1.md
-- Dual-column law: source_value IMMUTABLE + verbatim anchor; rdr_value NULL. Idempotent (INSERT OR REPLACE).
-- starter_set = 'poe1-zone68'. poedb 'Damage' is a single value (avg/calculated); min/max range only where noted.
-- Attack Time is seconds/attack (invert for attacks/sec — a rule concern). Resists + Crit verbatim.
-- The zone-68 Cannibal variant used is CannibalFemaleThrowFire (Level 68), per the note's map-tier table.

-- ============ MOB 1: Cannibal Female ThrowFire (Level 68) ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('poe1-cannibal-l68','poe1','Cannibal Female ThrowFire (Level 68)','life',6433,'poe1_flat_life','"CannibalFemaleThrowFire Level 68 (Map) | Life 6,433" poedb.tw/us/Cannibal','https://poedb.tw/us/Cannibal','2026-07-23','poe1-zone68',NULL),
('poe1-cannibal-l68','poe1','Cannibal Female ThrowFire (Level 68)','armour',28790,'poe1_armour_rating','"CannibalFemaleThrowFire Level 68 | Armour 28,790" poedb.tw/us/Cannibal','https://poedb.tw/us/Cannibal','2026-07-23','poe1-zone68',NULL),
('poe1-cannibal-l68','poe1','Cannibal Female ThrowFire (Level 68)','evasion_rating',5450,'poe1_evasion_rating','"CannibalFemaleThrowFire Level 68 | Evasion Rating 5,450" poedb.tw/us/Cannibal','https://poedb.tw/us/Cannibal','2026-07-23','poe1-zone68',NULL),
('poe1-cannibal-l68','poe1','Cannibal Female ThrowFire (Level 68)','damage',374,'poe1_damage','"CannibalFemaleThrowFire Level 68 | Damage 374" poedb.tw/us/Cannibal','https://poedb.tw/us/Cannibal','2026-07-23','poe1-zone68',NULL),
('poe1-cannibal-l68','poe1','Cannibal Female ThrowFire (Level 68)','attack_time_sec',1.995,'poe1_attack_time_sec','"Attack Time 1.995" poedb.tw/us/Cannibal','https://poedb.tw/us/Cannibal','2026-07-23','poe1-zone68',NULL),
('poe1-cannibal-l68','poe1','Cannibal Female ThrowFire (Level 68)','fire_resist_pct',0,'pct','"Fire Resist 0%" poedb.tw/us/Cannibal','https://poedb.tw/us/Cannibal','2026-07-23','poe1-zone68',NULL),
('poe1-cannibal-l68','poe1','Cannibal Female ThrowFire (Level 68)','cold_resist_pct',0,'pct','"Cold Resist 0%" poedb.tw/us/Cannibal','https://poedb.tw/us/Cannibal','2026-07-23','poe1-zone68',NULL),
('poe1-cannibal-l68','poe1','Cannibal Female ThrowFire (Level 68)','lightning_resist_pct',0,'pct','"Lightning Resist 0%" poedb.tw/us/Cannibal','https://poedb.tw/us/Cannibal','2026-07-23','poe1-zone68',NULL),
('poe1-cannibal-l68','poe1','Cannibal Female ThrowFire (Level 68)','chaos_resist_pct',0,'pct','"Chaos Resist 0%" poedb.tw/us/Cannibal','https://poedb.tw/us/Cannibal','2026-07-23','poe1-zone68',NULL),
('poe1-cannibal-l68','poe1','Cannibal Female ThrowFire (Level 68)','crit_chance_pct',5,'pct','"Critical Strike Chance +5%" poedb.tw/us/Cannibal','https://poedb.tw/us/Cannibal','2026-07-23','poe1-zone68',NULL);

-- ============ MOB 2: Goatman LeapSlam (Level 68) ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('poe1-goatman-l68','poe1','Goatman LeapSlam Abberath Gauntlet (Level 68)','life',7077,'poe1_flat_life','"GoatmanLeapSlamAbberathGauntlet (Level 68): Life 7,077" poedb.tw/us/Goatman','https://poedb.tw/us/Goatman','2026-07-23','poe1-zone68',NULL),
('poe1-goatman-l68','poe1','Goatman LeapSlam Abberath Gauntlet (Level 68)','armour',28790,'poe1_armour_rating','"...Armor 28,790" poedb.tw/us/Goatman','https://poedb.tw/us/Goatman','2026-07-23','poe1-zone68',NULL),
('poe1-goatman-l68','poe1','Goatman LeapSlam Abberath Gauntlet (Level 68)','evasion_rating',4976,'poe1_evasion_rating','"...Evasion Rating 4,976" poedb.tw/us/Goatman','https://poedb.tw/us/Goatman','2026-07-23','poe1-zone68',NULL),
('poe1-goatman-l68','poe1','Goatman LeapSlam Abberath Gauntlet (Level 68)','damage',616,'poe1_damage','"...Damage 616" poedb.tw/us/Goatman','https://poedb.tw/us/Goatman','2026-07-23','poe1-zone68',NULL),
('poe1-goatman-l68','poe1','Goatman LeapSlam Abberath Gauntlet (Level 68)','damage_range_min',493,'poe1_damage','"Base Damage Range 493-740" poedb.tw/us/Goatman','https://poedb.tw/us/Goatman','2026-07-23','poe1-zone68',NULL),
('poe1-goatman-l68','poe1','Goatman LeapSlam Abberath Gauntlet (Level 68)','damage_range_max',740,'poe1_damage','"Base Damage Range 493-740" poedb.tw/us/Goatman','https://poedb.tw/us/Goatman','2026-07-23','poe1-zone68',NULL),
('poe1-goatman-l68','poe1','Goatman LeapSlam Abberath Gauntlet (Level 68)','attack_time_sec',1.2,'poe1_attack_time_sec','"Attack Time 1.2" poedb.tw/us/Goatman','https://poedb.tw/us/Goatman','2026-07-23','poe1-zone68',NULL),
('poe1-goatman-l68','poe1','Goatman LeapSlam Abberath Gauntlet (Level 68)','fire_resist_pct',40,'pct','"Fire Resistance 40%" poedb.tw/us/Goatman','https://poedb.tw/us/Goatman','2026-07-23','poe1-zone68',NULL),
('poe1-goatman-l68','poe1','Goatman LeapSlam Abberath Gauntlet (Level 68)','cold_resist_pct',0,'pct','"Cold/Lightning/Chaos Resistance 0%" poedb.tw/us/Goatman','https://poedb.tw/us/Goatman','2026-07-23','poe1-zone68',NULL),
('poe1-goatman-l68','poe1','Goatman LeapSlam Abberath Gauntlet (Level 68)','lightning_resist_pct',0,'pct','"Cold/Lightning/Chaos Resistance 0%" poedb.tw/us/Goatman','https://poedb.tw/us/Goatman','2026-07-23','poe1-zone68',NULL),
('poe1-goatman-l68','poe1','Goatman LeapSlam Abberath Gauntlet (Level 68)','chaos_resist_pct',0,'pct','"Cold/Lightning/Chaos Resistance 0%" poedb.tw/us/Goatman','https://poedb.tw/us/Goatman','2026-07-23','poe1-zone68',NULL),
('poe1-goatman-l68','poe1','Goatman LeapSlam Abberath Gauntlet (Level 68)','crit_chance_pct',5,'pct','"Critical Strike Chance 5%" poedb.tw/us/Goatman','https://poedb.tw/us/Goatman','2026-07-23','poe1-zone68',NULL);

-- ============ MOB 3: Corrupted Rhoa (RhoaSkeletonBlackMap Level 68) ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('poe1-corrupted-rhoa-l68','poe1','Corrupted Rhoa (RhoaSkeletonBlackMap Level 68)','life',7205,'poe1_flat_life','"RhoaSkeletonBlackMap (Level 68): Life 7,205" poedb.tw/us/Corrupted_Rhoa','https://poedb.tw/us/Corrupted_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-corrupted-rhoa-l68','poe1','Corrupted Rhoa (RhoaSkeletonBlackMap Level 68)','armour',35988,'poe1_armour_rating','"...Armour 35,988" poedb.tw/us/Corrupted_Rhoa','https://poedb.tw/us/Corrupted_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-corrupted-rhoa-l68','poe1','Corrupted Rhoa (RhoaSkeletonBlackMap Level 68)','evasion_rating',4739,'poe1_evasion_rating','"...Evasion Rating 4,739" poedb.tw/us/Corrupted_Rhoa','https://poedb.tw/us/Corrupted_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-corrupted-rhoa-l68','poe1','Corrupted Rhoa (RhoaSkeletonBlackMap Level 68)','damage',601,'poe1_damage','"...Damage 601" poedb.tw/us/Corrupted_Rhoa','https://poedb.tw/us/Corrupted_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-corrupted-rhoa-l68','poe1','Corrupted Rhoa (RhoaSkeletonBlackMap Level 68)','attack_time_sec',1.395,'poe1_attack_time_sec','"Attack Time 1.395" poedb.tw/us/Corrupted_Rhoa','https://poedb.tw/us/Corrupted_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-corrupted-rhoa-l68','poe1','Corrupted Rhoa (RhoaSkeletonBlackMap Level 68)','fire_resist_pct',0,'pct','"Fire 0%" poedb.tw/us/Corrupted_Rhoa','https://poedb.tw/us/Corrupted_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-corrupted-rhoa-l68','poe1','Corrupted Rhoa (RhoaSkeletonBlackMap Level 68)','cold_resist_pct',40,'pct','"Cold 40%" poedb.tw/us/Corrupted_Rhoa','https://poedb.tw/us/Corrupted_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-corrupted-rhoa-l68','poe1','Corrupted Rhoa (RhoaSkeletonBlackMap Level 68)','lightning_resist_pct',0,'pct','"Lightning 0%" poedb.tw/us/Corrupted_Rhoa','https://poedb.tw/us/Corrupted_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-corrupted-rhoa-l68','poe1','Corrupted Rhoa (RhoaSkeletonBlackMap Level 68)','chaos_resist_pct',0,'pct','"Chaos 0%" poedb.tw/us/Corrupted_Rhoa','https://poedb.tw/us/Corrupted_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-corrupted-rhoa-l68','poe1','Corrupted Rhoa (RhoaSkeletonBlackMap Level 68)','crit_chance_pct',5,'pct','"Crit 5%" poedb.tw/us/Corrupted_Rhoa','https://poedb.tw/us/Corrupted_Rhoa','2026-07-23','poe1-zone68',NULL);

-- ============ MOB 4: Infested Rhoa (Level 68) ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('poe1-infested-rhoa-l68','poe1','Infested Rhoa (Level 68)','life',4503,'poe1_flat_life','"Life 4,503" poedb.tw/us/Infested_Rhoa','https://poedb.tw/us/Infested_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-infested-rhoa-l68','poe1','Infested Rhoa (Level 68)','armour',35988,'poe1_armour_rating','"Armor 35,988" poedb.tw/us/Infested_Rhoa','https://poedb.tw/us/Infested_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-infested-rhoa-l68','poe1','Infested Rhoa (Level 68)','evasion_rating',4739,'poe1_evasion_rating','"Evasion Rating 4,739" poedb.tw/us/Infested_Rhoa','https://poedb.tw/us/Infested_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-infested-rhoa-l68','poe1','Infested Rhoa (Level 68)','damage',374,'poe1_damage','"Damage 374" poedb.tw/us/Infested_Rhoa','https://poedb.tw/us/Infested_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-infested-rhoa-l68','poe1','Infested Rhoa (Level 68)','attack_time_sec',1.395,'poe1_attack_time_sec','"Attack Time 1.395" poedb.tw/us/Infested_Rhoa','https://poedb.tw/us/Infested_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-infested-rhoa-l68','poe1','Infested Rhoa (Level 68)','fire_resist_pct',0,'pct','"Fire 0%" poedb.tw/us/Infested_Rhoa','https://poedb.tw/us/Infested_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-infested-rhoa-l68','poe1','Infested Rhoa (Level 68)','cold_resist_pct',40,'pct','"Cold 40%" poedb.tw/us/Infested_Rhoa','https://poedb.tw/us/Infested_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-infested-rhoa-l68','poe1','Infested Rhoa (Level 68)','lightning_resist_pct',0,'pct','"Lightning 0%" poedb.tw/us/Infested_Rhoa','https://poedb.tw/us/Infested_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-infested-rhoa-l68','poe1','Infested Rhoa (Level 68)','chaos_resist_pct',0,'pct','"Chaos 0%" poedb.tw/us/Infested_Rhoa','https://poedb.tw/us/Infested_Rhoa','2026-07-23','poe1-zone68',NULL),
('poe1-infested-rhoa-l68','poe1','Infested Rhoa (Level 68)','crit_chance_pct',5,'pct','"Crit 5%" poedb.tw/us/Infested_Rhoa','https://poedb.tw/us/Infested_Rhoa','2026-07-23','poe1-zone68',NULL);

-- ============ MOB 5: Albino Rhoa (Level 68 — non-attacking variant) ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('poe1-albino-rhoa-l68','poe1','Albino Rhoa (Level 68)','life',7720,'poe1_flat_life','"Albino Rhoa (Level 68): Life 7,720" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-albino-rhoa-l68','poe1','Albino Rhoa (Level 68)','armour',34548,'poe1_armour_rating','"Armour 34,548" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-albino-rhoa-l68','poe1','Albino Rhoa (Level 68)','damage',0,'poe1_damage','"Damage 0" (non-attacking variant) poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-albino-rhoa-l68','poe1','Albino Rhoa (Level 68)','attack_time_sec',1.395,'poe1_attack_time_sec','"Attack Time 1.395" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source');

-- ============ Additional zone-68 Rhoa variants (search-synthesis) ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('poe1-primal-rhoa-l68','poe1','Primal Rhoa (Level 68)','life',24318,'poe1_flat_life','"Primal Rhoa | 68 | Life 24,318" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-primal-rhoa-l68','poe1','Primal Rhoa (Level 68)','armour',34548,'poe1_armour_rating','"Armour 34,548" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-primal-rhoa-l68','poe1','Primal Rhoa (Level 68)','damage',523,'poe1_damage','"Damage 523" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-primal-rhoa-l68','poe1','Primal Rhoa (Level 68)','attack_time_sec',0.93,'poe1_attack_time_sec','"Attack Time 0.93" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-saqawine-rhoa-l68','poe1','Saqawine Rhoa (Level 68)','life',28950,'poe1_flat_life','"Saqawine Rhoa | 68 | Life 28,950" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-saqawine-rhoa-l68','poe1','Saqawine Rhoa (Level 68)','armour',35988,'poe1_armour_rating','"Armour 35,988" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-saqawine-rhoa-l68','poe1','Saqawine Rhoa (Level 68)','damage',560,'poe1_damage','"Damage 560" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-saqawine-rhoa-l68','poe1','Saqawine Rhoa (Level 68)','attack_time_sec',1.395,'poe1_attack_time_sec','"Attack Time 1.395" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-tercel-rhoa-l68','poe1','Tercel Rhoa (Level 68)','life',8235,'poe1_flat_life','"Tercel Rhoa | 68 | Life 8,235" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-tercel-rhoa-l68','poe1','Tercel Rhoa (Level 68)','armour',35988,'poe1_armour_rating','"Armour 35,988" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-tercel-rhoa-l68','poe1','Tercel Rhoa (Level 68)','damage',598,'poe1_damage','"Damage 598" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source'),
('poe1-tercel-rhoa-l68','poe1','Tercel Rhoa (Level 68)','attack_time_sec',1.395,'poe1_attack_time_sec','"Attack Time 1.395" poedb.tw search synthesis','https://poedb.tw/us/','2026-07-23','poe1-zone68','one_source');

-- NOTE: poedb 'Damage' is a single value (avg/calculated); min/max range only anchored for Goatman (493-740).
--       Monster attack speed = derived (invert attack_time_sec — a rule concern). Normal/magic/rare rarity HP
--       multipliers = GAP (poedb entries are single-rarity variants). Registered in rules manifest.
