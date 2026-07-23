-- corpus_kf23_kit_poe2_bonestorm.sql
-- KF-2 kit-side population — poe2-bonestorm (Bonestorm Witch Hunter/Blood Mage, 0.3 era).
-- Author: elrond | 2026-07-23 | Source note: agentic_orchestration/legolas/notes/2026-07-23-kf23-harvest-poe2.md
-- Dual-column law: source_value IMMUTABLE + verbatim anchor; rdr_value NULL. Idempotent (INSERT OR REPLACE).
--
-- Bonestorm = channel skill consuming Power Charges; PHYSICAL SPELL damage (not weapon-dependent — simpler
-- than Cyclone). Two components per shard: projectile hit + explosion. Full gem 1-20 table for BOTH from poe2db.
-- PIN-N10 (CONDUCTOR PIN #5): N_shards = 10 (documented-build midpoint) for expected-per-release — curated as a
-- pinned scalar (charter-ruling, not a source anchor) with source_scale 'pin_shard_count'.
-- poe2 composition split (CONDUCTOR PIN #6): projectile = evadable; explosion = AoE-exempt. poe2 armour = GAP-EXCLUDED.
--
-- numeric_key convention: bonestorm_proj_{min,max}_gemNN / bonestorm_expl_{min,max}_gemNN / bonestorm_int_req_gemNN
--   / bonestorm_manapersec_gemNN + skill constants + character partials.

-- ============ Bonestorm — projectile physical damage (gem 1-20), source: poe2db + fextralife ============
-- Anchor: poe2db.tw/us/Bonestorm (2026-07-23). "Deals (4-116) to (7-175) Physical Damage" [projectile].
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('poe2-bonestorm','bonestorm_proj_min_gem01',4,'poe2_phys_hit','"Gem 1 | Projectile Dmg 4-7" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem01',7,'poe2_phys_hit','"Gem 1 | Projectile Dmg 4-7" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem02',6,'poe2_phys_hit','"Gem 2 | Projectile Dmg 6-9" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem02',9,'poe2_phys_hit','"Gem 2 | Projectile Dmg 6-9" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem03',8,'poe2_phys_hit','"Gem 3 | Projectile Dmg 8-12" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem03',12,'poe2_phys_hit','"Gem 3 | Projectile Dmg 8-12" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem04',10,'poe2_phys_hit','"Gem 4 | Projectile Dmg 10-16" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem04',16,'poe2_phys_hit','"Gem 4 | Projectile Dmg 10-16" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem05',13,'poe2_phys_hit','"Gem 5 | Projectile Dmg 13-20" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem05',20,'poe2_phys_hit','"Gem 5 | Projectile Dmg 13-20" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem06',16,'poe2_phys_hit','"Gem 6 | Projectile Dmg 16-24" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem06',24,'poe2_phys_hit','"Gem 6 | Projectile Dmg 16-24" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem07',19,'poe2_phys_hit','"Gem 7 | Projectile Dmg 19-29" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem07',29,'poe2_phys_hit','"Gem 7 | Projectile Dmg 19-29" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem08',23,'poe2_phys_hit','"Gem 8 | Projectile Dmg 23-34" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem08',34,'poe2_phys_hit','"Gem 8 | Projectile Dmg 23-34" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem09',27,'poe2_phys_hit','"Gem 9 | Projectile Dmg 27-40" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem09',40,'poe2_phys_hit','"Gem 9 | Projectile Dmg 27-40" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem10',31,'poe2_phys_hit','"Gem 10 | Projectile Dmg 31-47" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem10',47,'poe2_phys_hit','"Gem 10 | Projectile Dmg 31-47" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem11',36,'poe2_phys_hit','"Gem 11 | Projectile Dmg 36-55" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem11',55,'poe2_phys_hit','"Gem 11 | Projectile Dmg 36-55" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem12',42,'poe2_phys_hit','"Gem 12 | Projectile Dmg 42-63" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem12',63,'poe2_phys_hit','"Gem 12 | Projectile Dmg 42-63" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem13',48,'poe2_phys_hit','"Gem 13 | Projectile Dmg 48-72" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem13',72,'poe2_phys_hit','"Gem 13 | Projectile Dmg 48-72" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem14',55,'poe2_phys_hit','"Gem 14 | Projectile Dmg 55-83" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem14',83,'poe2_phys_hit','"Gem 14 | Projectile Dmg 55-83" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem15',63,'poe2_phys_hit','"Gem 15 | Projectile Dmg 63-94" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem15',94,'poe2_phys_hit','"Gem 15 | Projectile Dmg 63-94" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem16',71,'poe2_phys_hit','"Gem 16 | Projectile Dmg 71-107" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem16',107,'poe2_phys_hit','"Gem 16 | Projectile Dmg 71-107" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem17',81,'poe2_phys_hit','"Gem 17 | Projectile Dmg 81-121" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem17',121,'poe2_phys_hit','"Gem 17 | Projectile Dmg 81-121" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem18',91,'poe2_phys_hit','"Gem 18 | Projectile Dmg 91-137" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem18',137,'poe2_phys_hit','"Gem 18 | Projectile Dmg 91-137" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem19',103,'poe2_phys_hit','"Gem 19 | Projectile Dmg 103-155" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_max_gem19',155,'poe2_phys_hit','"Gem 19 | Projectile Dmg 103-155" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_proj_min_gem20',116,'poe2_phys_hit','"Gem 20 | Projectile Dmg 116-175" poe2db.tw/us/Bonestorm (2026-07-23) [documented build point: gem 20]'),
('poe2-bonestorm','bonestorm_proj_max_gem20',175,'poe2_phys_hit','"Gem 20 | Projectile Dmg 116-175" poe2db.tw/us/Bonestorm (2026-07-23) [documented build point: gem 20]');

-- ============ Bonestorm — explosion physical damage (gem 1-20), source: poe2db ============
-- Anchor: poe2db.tw/us/Bonestorm (2026-07-23). "Deals (3-89) to (5-134) Physical Damage" [explosion]. AoE-exempt (PIN #6).
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('poe2-bonestorm','bonestorm_expl_min_gem01',3,'poe2_phys_hit','"Gem 1 | Explosion Dmg 3-5" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem01',5,'poe2_phys_hit','"Gem 1 | Explosion Dmg 3-5" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem02',5,'poe2_phys_hit','"Gem 2 | Explosion Dmg 5-7" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem02',7,'poe2_phys_hit','"Gem 2 | Explosion Dmg 5-7" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem03',6,'poe2_phys_hit','"Gem 3 | Explosion Dmg 6-9" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem03',9,'poe2_phys_hit','"Gem 3 | Explosion Dmg 6-9" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem04',8,'poe2_phys_hit','"Gem 4 | Explosion Dmg 8-12" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem04',12,'poe2_phys_hit','"Gem 4 | Explosion Dmg 8-12" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem05',10,'poe2_phys_hit','"Gem 5 | Explosion Dmg 10-15" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem05',15,'poe2_phys_hit','"Gem 5 | Explosion Dmg 10-15" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem06',12,'poe2_phys_hit','"Gem 6 | Explosion Dmg 12-18" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem06',18,'poe2_phys_hit','"Gem 6 | Explosion Dmg 12-18" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem07',15,'poe2_phys_hit','"Gem 7 | Explosion Dmg 15-22" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem07',22,'poe2_phys_hit','"Gem 7 | Explosion Dmg 15-22" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem08',18,'poe2_phys_hit','"Gem 8 | Explosion Dmg 18-26" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem08',26,'poe2_phys_hit','"Gem 8 | Explosion Dmg 18-26" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem09',21,'poe2_phys_hit','"Gem 9 | Explosion Dmg 21-31" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem09',31,'poe2_phys_hit','"Gem 9 | Explosion Dmg 21-31" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem10',24,'poe2_phys_hit','"Gem 10 | Explosion Dmg 24-36" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem10',36,'poe2_phys_hit','"Gem 10 | Explosion Dmg 24-36" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem11',28,'poe2_phys_hit','"Gem 11 | Explosion Dmg 28-42" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem11',42,'poe2_phys_hit','"Gem 11 | Explosion Dmg 28-42" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem12',32,'poe2_phys_hit','"Gem 12 | Explosion Dmg 32-48" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem12',48,'poe2_phys_hit','"Gem 12 | Explosion Dmg 32-48" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem13',37,'poe2_phys_hit','"Gem 13 | Explosion Dmg 37-56" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem13',56,'poe2_phys_hit','"Gem 13 | Explosion Dmg 37-56" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem14',42,'poe2_phys_hit','"Gem 14 | Explosion Dmg 42-63" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem14',63,'poe2_phys_hit','"Gem 14 | Explosion Dmg 42-63" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem15',48,'poe2_phys_hit','"Gem 15 | Explosion Dmg 48-72" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem15',72,'poe2_phys_hit','"Gem 15 | Explosion Dmg 48-72" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem16',55,'poe2_phys_hit','"Gem 16 | Explosion Dmg 55-82" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem16',82,'poe2_phys_hit','"Gem 16 | Explosion Dmg 55-82" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem17',62,'poe2_phys_hit','"Gem 17 | Explosion Dmg 62-93" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem17',93,'poe2_phys_hit','"Gem 17 | Explosion Dmg 62-93" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem18',70,'poe2_phys_hit','"Gem 18 | Explosion Dmg 70-105" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem18',105,'poe2_phys_hit','"Gem 18 | Explosion Dmg 70-105" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem19',79,'poe2_phys_hit','"Gem 19 | Explosion Dmg 79-119" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_max_gem19',119,'poe2_phys_hit','"Gem 19 | Explosion Dmg 79-119" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_expl_min_gem20',89,'poe2_phys_hit','"Gem 20 | Explosion Dmg 89-134" poe2db.tw/us/Bonestorm (2026-07-23) [documented build point: gem 20]'),
('poe2-bonestorm','bonestorm_expl_max_gem20',134,'poe2_phys_hit','"Gem 20 | Explosion Dmg 89-134" poe2db.tw/us/Bonestorm (2026-07-23) [documented build point: gem 20]');

-- ============ Bonestorm — Int req + mana/sec (gem 1-20), source: poe2db ============
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('poe2-bonestorm','bonestorm_int_req_gem01',4,'poe2_stat_req','"Gem 1 | Int 4" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_manapersec_gem01',6,'poe2_mana_per_sec','"Gem 1 | Mana/sec 6" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_int_req_gem05',28,'poe2_stat_req','"Gem 5 | Int 28" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_manapersec_gem05',11,'poe2_mana_per_sec','"Gem 5 | Mana/sec 11" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_int_req_gem10',65,'poe2_stat_req','"Gem 10 | Int 65" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_manapersec_gem10',21,'poe2_mana_per_sec','"Gem 10 | Mana/sec 21" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_int_req_gem15',113,'poe2_stat_req','"Gem 15 | Int 113" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_manapersec_gem15',36,'poe2_mana_per_sec','"Gem 15 | Mana/sec 36" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','bonestorm_int_req_gem20',157,'poe2_stat_req','"Gem 20 | Int 157" poe2db.tw/us/Bonestorm (2026-07-23) [documented build point]'),
('poe2-bonestorm','bonestorm_manapersec_gem20',61,'poe2_mana_per_sec','"Gem 20 | Mana/sec 61" poe2db.tw/us/Bonestorm (2026-07-23) [documented build point]');

-- ============ Bonestorm — skill constants, source: poe2db ============
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('poe2-bonestorm','crit_chance_pct_base',15,'poe2_pct','"Critical Hit Chance: 15.00%" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','cast_time_sec',0.12,'poe2_seconds','"Cast Time: 0.12 sec" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','projectile_speed_mps',27,'poe2_metres_per_sec','"Projectile Speed: 27 metres per Second" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','explosion_radius_m',0.5,'poe2_metres','"Explosion radius is 0.5 metres" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','explosion_radius_bonus_powercharge_m',0.7,'poe2_metres','"+0.7 metres to explosion radius if a Power Charge was Consumed" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','aoe_more_pct_per_powercharge',40,'poe2_pct_more','"40% more Area of Effect per Power Charge Consumed" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','max_projectiles',20,'poe2_count','"Can fire up to 20 Projectiles" poe2db.tw/us/Bonestorm (2026-07-23)'),
('poe2-bonestorm','impale_magnitude_more_pct',200,'poe2_pct_more','"200% more Impale Magnitude" poe2db.tw/us/Bonestorm (2026-07-23) [both projectile and explosion]');

-- ============ N_shards PIN (PIN-N10 / CONDUCTOR PIN #5) — pinned, NOT a source anchor ============
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('poe2-bonestorm','n_shards_expected_pin',10,'pin_shard_count','[PIN-N10 / CONDUCTOR PIN #5] N_shards = 10, documented-build midpoint for expected-per-release (max 20 per "Can fire up to 20 Projectiles"). PINNED charter ruling, not a source anchor — supersede only with an anchored count.');

-- ============ Character / defense build-point (Bonestorm Witch Hunter) — partials only ============
-- Anchored verbatim from forum/game8 build context; most stat-sheet values are GAP (rules-manifest + composition).
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('poe2-bonestorm','cast_speed_increased_pct_target',100,'poe2_pct_increased','"about 100% increased Cast Speed on your gear" PoE2 forum build thread view-thread/3706145 (2026-07-23) [target, not stat-sheet]'),
('poe2-bonestorm','spirit_req_target',65,'poe2_spirit','"about 60-70 Spirit" PoE2 forum build thread view-thread/3706145 (2026-07-23) [midpoint of stated 60-70 range; requirement, not stat-sheet]'),
('poe2-bonestorm','mana_per_sec_gem25_context',619,'poe2_mana_per_sec','"Bonestorm [at gem level 25] costs 619 per second" game8.co (2026-07-23) [gem 25 — beyond gem-20 table; context]'),
('poe2-bonestorm','impale_store_pct_bonestorm',90,'poe2_pct','"Bonestorm increases the effect of Impale by 3x! So instead of 30%, we are storing 90% of the damage" PoE2 forum view-thread/3852711 (2026-07-23)'),
('poe2-bonestorm','impale_store_pct_base',30,'poe2_pct','"Impale stores 30% of the Hit damage you deal" PoE2 forum view-thread/3852711 (2026-07-23) [base, pre-Bonestorm 3x]');
