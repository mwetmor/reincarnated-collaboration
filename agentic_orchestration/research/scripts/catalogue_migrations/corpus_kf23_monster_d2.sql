-- corpus_kf23_monster_d2.sql
-- KF-3 monster-side population — D2 Act-1 Normal starter set (5 mobs).
-- Author: elrond | 2026-07-23
-- Source notes: 2026-07-23-kf23-harvest-d2.md (HP/def/damage/resist/XP) + 2026-07-23-kf23-harvest-formulas.md (C4 mob AR).
-- Dual-column law: source_value IMMUTABLE + verbatim anchor; rdr_value NULL. Idempotent (INSERT OR REPLACE on (monster_id, numeric_key)).
-- starter_set = 'd2-act1-normal'. All source_url + source_date + source_anchor populated (schema NOT NULL).
--
-- gap_flag='normal_resist_inferred' on Normal-difficulty resist rows: the note anchors Hell resists verbatim
-- but marks Normal resists as "0% inferred from Hell column + Normal baseline, not explicitly stated per-row."
-- Curated at 0% with the gap_flag so a consumer never mistakes the inference for a hard anchor. Hell resist
-- values are NOT curated (out of the Normal starter set). HP is per-variant; the starter set uses the base
-- variant of each family (Fallen, Zombie, Skeleton, Dark Hunter, Quill Rat).

-- ============ MOB 1: Fallen (Normal Act 1) ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('d2-fallen','d2','Fallen (Normal Act 1)','hp_min',1,'d2_flat_hp','"HP (Fallen variant) 1-4" fextralife/Fallen','https://diablo2.wiki.fextralife.com/Fallen','2026-07-23','d2-act1-normal',NULL),
('d2-fallen','d2','Fallen (Normal Act 1)','hp_max',4,'d2_flat_hp','"HP (Fallen variant) 1-4" fextralife/Fallen','https://diablo2.wiki.fextralife.com/Fallen','2026-07-23','d2-act1-normal',NULL),
('d2-fallen','d2','Fallen (Normal Act 1)','defense',5,'d2_defense_rating','"Defense (Fallen) 5" fextralife/Fallen','https://diablo2.wiki.fextralife.com/Fallen','2026-07-23','d2-act1-normal',NULL),
('d2-fallen','d2','Fallen (Normal Act 1)','melee_dmg_min',1,'d2_phys_hit','"Melee Dmg Attack 1 (Fallen/Normal) 1-2" fextralife/Fallen','https://diablo2.wiki.fextralife.com/Fallen','2026-07-23','d2-act1-normal',NULL),
('d2-fallen','d2','Fallen (Normal Act 1)','melee_dmg_max',2,'d2_phys_hit','"Melee Dmg Attack 1 (Fallen/Normal) 1-2" fextralife/Fallen','https://diablo2.wiki.fextralife.com/Fallen','2026-07-23','d2-act1-normal',NULL),
('d2-fallen','d2','Fallen (Normal Act 1)','ar_attack1',8,'d2_attack_rating','"Attack Rating 1 (Normal): 8" fextralife/Fallen (formulas note C4)','https://diablo2.wiki.fextralife.com/Fallen','2026-07-23','d2-act1-normal',NULL),
('d2-fallen','d2','Fallen (Normal Act 1)','ar_attack2',8,'d2_attack_rating','"Attack Rating 2 (Normal): 8" fextralife/Fallen (formulas note C4)','https://diablo2.wiki.fextralife.com/Fallen','2026-07-23','d2-act1-normal',NULL),
('d2-fallen','d2','Fallen (Normal Act 1)','physical_resist_pct',15,'pct','"Physical Resist (Normal) 15%" fextralife/Fallen','https://diablo2.wiki.fextralife.com/Fallen','2026-07-23','d2-act1-normal',NULL),
('d2-fallen','d2','Fallen (Normal Act 1)','fire_resist_pct',0,'pct','Normal Fallen 0% fire resist (fextralife Hell column = 0-125%; Normal 0% inferred, not explicit per-row) fextralife/Fallen','https://diablo2.wiki.fextralife.com/Fallen','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-fallen','d2','Fallen (Normal Act 1)','cold_resist_pct',0,'pct','Normal Fallen 0% cold resist (inferred from Hell column + Normal baseline) fextralife/Fallen','https://diablo2.wiki.fextralife.com/Fallen','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-fallen','d2','Fallen (Normal Act 1)','lightning_resist_pct',0,'pct','Normal Fallen 0% lightning resist (inferred) fextralife/Fallen','https://diablo2.wiki.fextralife.com/Fallen','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-fallen','d2','Fallen (Normal Act 1)','poison_resist_pct',0,'pct','Normal Fallen 0% poison resist (inferred) fextralife/Fallen','https://diablo2.wiki.fextralife.com/Fallen','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-fallen','d2','Fallen (Normal Act 1)','experience',18,'d2_xp','"Experience (Fallen/Normal): 18" fextralife/Fallen','https://diablo2.wiki.fextralife.com/Fallen','2026-07-23','d2-act1-normal',NULL);

-- ============ MOB 2: Zombie (Normal Act 1) ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('d2-zombie','d2','Zombie (Normal Act 1)','hp_min',7,'d2_flat_hp','"HP (Zombie) 7-12" fextralife/Zombie','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal',NULL),
('d2-zombie','d2','Zombie (Normal Act 1)','hp_max',12,'d2_flat_hp','"HP (Zombie) 7-12" fextralife/Zombie','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal',NULL),
('d2-zombie','d2','Zombie (Normal Act 1)','defense',5,'d2_defense_rating','"Defense (Zombie/Normal) 5" fextralife/Zombie','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal',NULL),
('d2-zombie','d2','Zombie (Normal Act 1)','block_pct',3,'pct','"Block % (Zombie) 3%" fextralife/Zombie','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal',NULL),
('d2-zombie','d2','Zombie (Normal Act 1)','melee_dmg1_min',1,'d2_phys_hit','"Melee Attack 1 Damage (Normal): Zombie 1-3" fextralife/Zombie','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal',NULL),
('d2-zombie','d2','Zombie (Normal Act 1)','melee_dmg1_max',3,'d2_phys_hit','"Melee Attack 1 Damage (Normal): Zombie 1-3" fextralife/Zombie','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal',NULL),
('d2-zombie','d2','Zombie (Normal Act 1)','melee_dmg2_min',2,'d2_phys_hit','"Melee Attack 2 Damage (Normal): Zombie 2-3" fextralife/Zombie','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal',NULL),
('d2-zombie','d2','Zombie (Normal Act 1)','melee_dmg2_max',3,'d2_phys_hit','"Melee Attack 2 Damage (Normal): Zombie 2-3" fextralife/Zombie','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal',NULL),
('d2-zombie','d2','Zombie (Normal Act 1)','ar_attack1',8,'d2_attack_rating','"Attack Rating 1 (Normal): Zombie 8" fextralife/Zombie (formulas note C4)','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal',NULL),
('d2-zombie','d2','Zombie (Normal Act 1)','ar_attack2',8,'d2_attack_rating','"Attack Rating 2 (Normal): Zombie 8" fextralife/Zombie (formulas note C4)','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal',NULL),
('d2-zombie','d2','Zombie (Normal Act 1)','fire_resist_pct',0,'pct','Normal Zombie 0% fire resist (inferred; not explicit per-row, Normal baseline) fextralife/Zombie','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-zombie','d2','Zombie (Normal Act 1)','cold_resist_pct',0,'pct','Normal Zombie 0% cold resist (inferred; Hell shows Cold 120 immune, Normal 0%) fextralife/Zombie','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-zombie','d2','Zombie (Normal Act 1)','lightning_resist_pct',0,'pct','Normal Zombie 0% lightning resist (inferred) fextralife/Zombie','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-zombie','d2','Zombie (Normal Act 1)','poison_resist_pct',0,'pct','Normal Zombie 0% poison resist (inferred) fextralife/Zombie','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-zombie','d2','Zombie (Normal Act 1)','experience',33,'d2_xp','"Experience (Zombie/Normal): 33" fextralife/Zombie','https://diablo2.wiki.fextralife.com/Zombie','2026-07-23','d2-act1-normal',NULL);

-- ============ MOB 3: Skeleton (Normal Act 1) ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('d2-skeleton','d2','Skeleton (Normal Act 1)','hp_min',7,'d2_flat_hp','"HP (Skeleton) 7-11" / "Hit Points: Skeleton | Normal | 7/11" fextralife/Skeleton','https://diablo2.wiki.fextralife.com/Skeleton','2026-07-23','d2-act1-normal',NULL),
('d2-skeleton','d2','Skeleton (Normal Act 1)','hp_max',11,'d2_flat_hp','"HP (Skeleton) 7-11" fextralife/Skeleton','https://diablo2.wiki.fextralife.com/Skeleton','2026-07-23','d2-act1-normal',NULL),
('d2-skeleton','d2','Skeleton (Normal Act 1)','defense',10,'d2_defense_rating','"Defense (Skeleton/Normal) 10" fextralife/Skeleton','https://diablo2.wiki.fextralife.com/Skeleton','2026-07-23','d2-act1-normal',NULL),
('d2-skeleton','d2','Skeleton (Normal Act 1)','melee_dmg1_min',1,'d2_phys_hit','"Melee Dmg Attack 1 (Skeleton/Normal) 1-3" fextralife/Skeleton','https://diablo2.wiki.fextralife.com/Skeleton','2026-07-23','d2-act1-normal',NULL),
('d2-skeleton','d2','Skeleton (Normal Act 1)','melee_dmg1_max',3,'d2_phys_hit','"Melee Dmg Attack 1 (Skeleton/Normal) 1-3" fextralife/Skeleton','https://diablo2.wiki.fextralife.com/Skeleton','2026-07-23','d2-act1-normal',NULL),
('d2-skeleton','d2','Skeleton (Normal Act 1)','fire_resist_pct',0,'pct','Normal Skeleton 0% fire resist (inferred; Normal baseline) fextralife/Skeleton','https://diablo2.wiki.fextralife.com/Skeleton','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-skeleton','d2','Skeleton (Normal Act 1)','cold_resist_pct',0,'pct','Normal Skeleton 0% cold resist (inferred) fextralife/Skeleton','https://diablo2.wiki.fextralife.com/Skeleton','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-skeleton','d2','Skeleton (Normal Act 1)','lightning_resist_pct',0,'pct','Normal Skeleton 0% lightning resist (inferred; Hell = 100% immune, Normal 0%) fextralife/Skeleton','https://diablo2.wiki.fextralife.com/Skeleton','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-skeleton','d2','Skeleton (Normal Act 1)','poison_resist_pct',0,'pct','Normal Skeleton 0% poison resist (inferred; Hell = 75%, Normal 0%) fextralife/Skeleton','https://diablo2.wiki.fextralife.com/Skeleton','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-skeleton','d2','Skeleton (Normal Act 1)','experience',34,'d2_xp','"Experience (Skeleton/Normal): 34" fextralife/Skeleton','https://diablo2.wiki.fextralife.com/Skeleton','2026-07-23','d2-act1-normal',NULL);

-- ============ MOB 4: Corrupt Rogue - Dark Hunter (Normal Act 1) ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('d2-dark-hunter','d2','Dark Hunter / Corrupt Rogue (Normal Act 1)','hp_min',5,'d2_flat_hp','"Dark Hunter: 5-9 (Normal)" fextralife/Corrupt+Rogue','https://diablo2.wiki.fextralife.com/Corrupt+Rogue','2026-07-23','d2-act1-normal',NULL),
('d2-dark-hunter','d2','Dark Hunter / Corrupt Rogue (Normal Act 1)','hp_max',9,'d2_flat_hp','"Dark Hunter: 5-9 (Normal)" fextralife/Corrupt+Rogue','https://diablo2.wiki.fextralife.com/Corrupt+Rogue','2026-07-23','d2-act1-normal',NULL),
('d2-dark-hunter','d2','Dark Hunter / Corrupt Rogue (Normal Act 1)','defense',10,'d2_defense_rating','"Dark Hunter: 10 (Normal defense)" fextralife/Corrupt+Rogue','https://diablo2.wiki.fextralife.com/Corrupt+Rogue','2026-07-23','d2-act1-normal',NULL),
('d2-dark-hunter','d2','Dark Hunter / Corrupt Rogue (Normal Act 1)','melee_dmg_min',1,'d2_phys_hit','"Dark Hunter: 1-3 (Normal melee)" fextralife/Corrupt+Rogue','https://diablo2.wiki.fextralife.com/Corrupt+Rogue','2026-07-23','d2-act1-normal',NULL),
('d2-dark-hunter','d2','Dark Hunter / Corrupt Rogue (Normal Act 1)','melee_dmg_max',3,'d2_phys_hit','"Dark Hunter: 1-3 (Normal melee)" fextralife/Corrupt+Rogue','https://diablo2.wiki.fextralife.com/Corrupt+Rogue','2026-07-23','d2-act1-normal',NULL),
('d2-dark-hunter','d2','Dark Hunter / Corrupt Rogue (Normal Act 1)','fire_resist_pct',0,'pct','Normal Dark Hunter 0% fire resist (inferred; Hell Fire 33, Normal 0%) fextralife/Corrupt+Rogue','https://diablo2.wiki.fextralife.com/Corrupt+Rogue','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-dark-hunter','d2','Dark Hunter / Corrupt Rogue (Normal Act 1)','cold_resist_pct',0,'pct','Normal Dark Hunter 0% cold resist (inferred; Hell Cold 100 immune, Normal 0%) fextralife/Corrupt+Rogue','https://diablo2.wiki.fextralife.com/Corrupt+Rogue','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-dark-hunter','d2','Dark Hunter / Corrupt Rogue (Normal Act 1)','lightning_resist_pct',0,'pct','Normal Dark Hunter 0% lightning resist (inferred; Hell Lightning 33, Normal 0%) fextralife/Corrupt+Rogue','https://diablo2.wiki.fextralife.com/Corrupt+Rogue','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-dark-hunter','d2','Dark Hunter / Corrupt Rogue (Normal Act 1)','experience',31,'d2_xp','"Experience (Dark Hunter/Normal): 31" fextralife/Corrupt+Rogue','https://diablo2.wiki.fextralife.com/Corrupt+Rogue','2026-07-23','d2-act1-normal',NULL);

-- ============ MOB 5: Spike Fiend - Quill Rat (Normal Act 1) ============
INSERT OR REPLACE INTO monster_numeric (monster_id, game, monster_name, numeric_key, source_value, source_scale, source_anchor, source_url, source_date, starter_set, gap_flag) VALUES
('d2-quill-rat','d2','Quill Rat / Spike Fiend (Normal Act 1)','hp_min',1,'d2_flat_hp','"Quill Rat | Normal | 1/5" (HP solo/full party) fextralife/Spike+Fiend','https://diablo2.wiki.fextralife.com/Spike+Fiend','2026-07-23','d2-act1-normal',NULL),
('d2-quill-rat','d2','Quill Rat / Spike Fiend (Normal Act 1)','hp_max',5,'d2_flat_hp','"Quill Rat | Normal | 1/5" fextralife/Spike+Fiend','https://diablo2.wiki.fextralife.com/Spike+Fiend','2026-07-23','d2-act1-normal',NULL),
('d2-quill-rat','d2','Quill Rat / Spike Fiend (Normal Act 1)','melee_dmg_min',1,'d2_phys_hit','"Melee: 1-2 (Normal)" fextralife/Spike+Fiend','https://diablo2.wiki.fextralife.com/Spike+Fiend','2026-07-23','d2-act1-normal',NULL),
('d2-quill-rat','d2','Quill Rat / Spike Fiend (Normal Act 1)','melee_dmg_max',2,'d2_phys_hit','"Melee: 1-2 (Normal)" fextralife/Spike+Fiend','https://diablo2.wiki.fextralife.com/Spike+Fiend','2026-07-23','d2-act1-normal',NULL),
('d2-quill-rat','d2','Quill Rat / Spike Fiend (Normal Act 1)','ranged_dmg_min',0,'d2_phys_hit','"Ranged: 0-1 (Normal)" fextralife/Spike+Fiend','https://diablo2.wiki.fextralife.com/Spike+Fiend','2026-07-23','d2-act1-normal',NULL),
('d2-quill-rat','d2','Quill Rat / Spike Fiend (Normal Act 1)','ranged_dmg_max',1,'d2_phys_hit','"Ranged: 0-1 (Normal)" fextralife/Spike+Fiend','https://diablo2.wiki.fextralife.com/Spike+Fiend','2026-07-23','d2-act1-normal',NULL),
('d2-quill-rat','d2','Quill Rat / Spike Fiend (Normal Act 1)','defense',5,'d2_defense_rating','"Defense Range: 5-45 (Normal)" fextralife/Spike+Fiend [low end of Normal range]','https://diablo2.wiki.fextralife.com/Spike+Fiend','2026-07-23','d2-act1-normal','range_estimate'),
('d2-quill-rat','d2','Quill Rat / Spike Fiend (Normal Act 1)','fire_resist_pct',0,'pct','Normal Quill Rat 0% fire resist (inferred; Normal baseline) fextralife/Spike+Fiend','https://diablo2.wiki.fextralife.com/Spike+Fiend','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-quill-rat','d2','Quill Rat / Spike Fiend (Normal Act 1)','cold_resist_pct',0,'pct','Normal Quill Rat 0% cold resist (inferred; Hell 50%, Normal 0%) fextralife/Spike+Fiend','https://diablo2.wiki.fextralife.com/Spike+Fiend','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-quill-rat','d2','Quill Rat / Spike Fiend (Normal Act 1)','physical_resist_pct',0,'pct','Normal Quill Rat 0% physical resist (inferred; Hell 50%, Normal 0%) fextralife/Spike+Fiend','https://diablo2.wiki.fextralife.com/Spike+Fiend','2026-07-23','d2-act1-normal','normal_resist_inferred'),
('d2-quill-rat','d2','Quill Rat / Spike Fiend (Normal Act 1)','experience',21,'d2_xp','"Experience (Quill Rat/Normal): 21" fextralife/Spike+Fiend','https://diablo2.wiki.fextralife.com/Spike+Fiend','2026-07-23','d2-act1-normal',NULL);

-- NOTE: monster attack rate / attack speed (frames per attack) = GAP for all d2 mobs (not in fetched tables).
--       Skeleton + Dark Hunter + Quill Rat AR (attack rating) = GAP-C4b (AR column exists on fextralife but not
--       re-fetched for these 3; only Fallen + Zombie AR captured per formulas note C4). Registered in rules manifest.
