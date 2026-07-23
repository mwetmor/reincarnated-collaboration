-- corpus_kf23_monster_poe2.sql
-- KF-3 monster-side population — PoE2 baseline level-scaling table (formula-level anchor).
-- Author: elrond | 2026-07-23 | Source note: 2026-07-23-kf23-harvest-poe2.md (monster side)
-- Dual-column law: source_value IMMUTABLE + verbatim anchor; rdr_value NULL. Idempotent (INSERT OR REPLACE).
--
-- PoE2 is Early Access (0.3 era); poe2db.tw is an SPA that 404s named monster paths — per-named-mob verbatim
-- stats are NOT fetchable. The ONLY anchored monster data is the baseline level-scaling table. Per the note's
-- explicit recommendation, curated as FORMULA-LEVEL anchors (gap_flag='formula_level_anchor'): a rule composes
-- level-scale × monster-specific multiplier. monster_id encodes the level ('poe2-levelscale-lNN'); each level is
-- a synthetic "monster" row representing the baseline stat at that level. Per-named-mob verbatim = next-lap
-- admission (charter §5), NOT silently pulled. The 5 anchored levels (1-5) are what the note verbatim-captured.
-- starter_set = 'poe2-levelscale'.

-- ============ PoE2 baseline monster level-scaling (levels 1-5), source: poe2db.tw/us/Monster ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('poe2-levelscale-l1','poe2','PoE2 baseline monster (Level 1)','damage',9.16,'poe2_damage','"Monster Level 1 | Damage 9.16" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l1','poe2','PoE2 baseline monster (Level 1)','life',15,'poe2_flat_life','"Monster Level 1 | Life 15" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l1','poe2','PoE2 baseline monster (Level 1)','armour',5,'poe2_armour_rating','"Monster Level 1 | Armour 5" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l1','poe2','PoE2 baseline monster (Level 1)','evasion',24,'poe2_evasion_rating','"Monster Level 1 | Evasion 24" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l1','poe2','PoE2 baseline monster (Level 1)','accuracy',32,'poe2_accuracy_rating','"Monster Level 1 | Accuracy 32" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l2','poe2','PoE2 baseline monster (Level 2)','damage',10.26,'poe2_damage','"Monster Level 2 | Damage 10.26" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l2','poe2','PoE2 baseline monster (Level 2)','life',20,'poe2_flat_life','"Monster Level 2 | Life 20" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l2','poe2','PoE2 baseline monster (Level 2)','armour',8,'poe2_armour_rating','"Monster Level 2 | Armour 8" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l2','poe2','PoE2 baseline monster (Level 2)','evasion',30,'poe2_evasion_rating','"Monster Level 2 | Evasion 30" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l2','poe2','PoE2 baseline monster (Level 2)','accuracy',35,'poe2_accuracy_rating','"Monster Level 2 | Accuracy 35" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l3','poe2','PoE2 baseline monster (Level 3)','damage',11.39,'poe2_damage','"Monster Level 3 | Damage 11.39" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l3','poe2','PoE2 baseline monster (Level 3)','life',24,'poe2_flat_life','"Monster Level 3 | Life 24" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l3','poe2','PoE2 baseline monster (Level 3)','armour',11,'poe2_armour_rating','"Monster Level 3 | Armour 11" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l3','poe2','PoE2 baseline monster (Level 3)','evasion',36,'poe2_evasion_rating','"Monster Level 3 | Evasion 36" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l3','poe2','PoE2 baseline monster (Level 3)','accuracy',39,'poe2_accuracy_rating','"Monster Level 3 | Accuracy 39" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l4','poe2','PoE2 baseline monster (Level 4)','damage',12.57,'poe2_damage','"Monster Level 4 | Damage 12.57" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l4','poe2','PoE2 baseline monster (Level 4)','life',28,'poe2_flat_life','"Monster Level 4 | Life 28" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l4','poe2','PoE2 baseline monster (Level 4)','armour',15,'poe2_armour_rating','"Monster Level 4 | Armour 15" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l4','poe2','PoE2 baseline monster (Level 4)','evasion',43,'poe2_evasion_rating','"Monster Level 4 | Evasion 43" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l4','poe2','PoE2 baseline monster (Level 4)','accuracy',43,'poe2_accuracy_rating','"Monster Level 4 | Accuracy 43" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l5','poe2','PoE2 baseline monster (Level 5)','damage',13.78,'poe2_damage','"Monster Level 5 | Damage 13.78" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l5','poe2','PoE2 baseline monster (Level 5)','life',33,'poe2_flat_life','"Monster Level 5 | Life 33" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l5','poe2','PoE2 baseline monster (Level 5)','armour',19,'poe2_armour_rating','"Monster Level 5 | Armour 19" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l5','poe2','PoE2 baseline monster (Level 5)','evasion',49,'poe2_evasion_rating','"Monster Level 5 | Evasion 49" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-levelscale-l5','poe2','PoE2 baseline monster (Level 5)','accuracy',48,'poe2_accuracy_rating','"Monster Level 5 | Accuracy 48" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor');

-- ============ PoE2 standard monster property caps, source: poe2db.tw/us/Monster ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('poe2-monster-caps','poe2','PoE2 standard monster property caps','max_phys_dr_pct',75,'pct','"maximum physical damage reduction +% [75]" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-monster-caps','poe2','PoE2 standard monster property caps','max_all_resist_pct',75,'pct','"base maximum all resistances +% [75]" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor');

-- ============ PoE2 early-creature damage/life multipliers (anchored context), source: poe2db.tw/us/Monster ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('poe2-flathead-younglings','poe2','Flathead Younglings (early creature)','damage_life_mult_pct',70,'pct','"Flathead Younglings (70% damage/life)" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor'),
('poe2-feral-primates','poe2','Feral Primates (early creature)','damage_life_mult_pct',65,'pct','"Feral Primates (65% damage/life)" poe2db.tw/us/Monster','https://poe2db.tw/us/Monster','2026-07-23','poe2-levelscale','formula_level_anchor');

-- NOTE: Per-named PoE2 Act-1 mob stats (Zombie/Skeleton/Goatman etc.) = FULL GAP (poe2db SPA renders monster
--       pages dynamically; WebFetch 404s all named paths). The rule composes: base = levelscale[monster_level]
--       × creature_multiplier. Per-mob verbatim = next-lap admission (charter §5). Registered in rules manifest.
--       PoE2 armour damage-reduction formula = GAP-EXCLUDED (GAP-B1, sources blocked) per CONDUCTOR PIN #6.
