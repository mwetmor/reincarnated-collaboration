-- corpus_kf23_kit_d2_firewall.sql
-- KF-2 kit-side population — d2-firewall-sorc (Fire Wall Sorceress).
-- Author: elrond | 2026-07-23 | Source note: agentic_orchestration/legolas/notes/2026-07-23-kf23-harvest-d2.md
-- Dual-column law: source_value IMMUTABLE + verbatim source_anchor (quote|URL|access-date); rdr_value NULL.
-- Idempotent: INSERT OR REPLACE on PK (kit_id, numeric_key). Anchor law: only verbatim-anchored values curated.
-- PINs applied: Pin A (D2 spells no crit → non-crit mean); PIN-C2 (fire-skill hit-chance=1); PIN-C3 (maxroll primary).
--
-- numeric_key convention (curation call, charter §7 reasoning-boundary):
--   firewall_manacost_lvlNN / firewall_dps_min_lvlNN / firewall_dps_max_lvlNN / firewall_radius_lvlNN  (per skill level)
--   firewall_reqlevel / firewall_castdelay_sec / firewall_duration_sec  (skill constants)
--   firemastery_bonus_pct_lvlNN  (Fire Mastery synergy table)
--   attr_str_base / attr_dex_base / attr_vit_base / attr_energy_base / life_base / mana_base / life_per_level / mana_per_level / life_per_vit / mana_per_energy
--   fcr_frames_atNNN  (FCR breakpoint: frames per cast at NNN% FCR)

-- ============ Fire Wall — skill level progression (slvl 1-20), source: rankedboost + fextralife ============
-- Anchor URL: https://rankedboost.com/diablo-2/sorceress/fire-wall/ (accessed 2026-07-23)
-- Radius unit = yards; DPS = fire damage per second (min/max); mana cost per cast.

INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('d2-firewall-sorc','firewall_manacost_lvl01',22,'d2_mana','"Level 1 | Mana Cost 22" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl01',70,'d2_fire_dps','"Level 1 | Fire Dmg/Sec 70-94" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl01',94,'d2_fire_dps','"Level 1 | Fire Dmg/Sec 70-94" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl01',4,'d2_yards','"Level 1 | Radius 4 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl02',23,'d2_mana','"Level 2 | Mana Cost 23" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl02',113,'d2_fire_dps','"Level 2 | Fire Dmg/Sec 113-137" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl02',137,'d2_fire_dps','"Level 2 | Fire Dmg/Sec 113-137" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl02',6,'d2_yards','"Level 2 | Radius 6 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl03',24,'d2_mana','"Level 3 | Mana Cost 24" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl03',156,'d2_fire_dps','"Level 3 | Fire Dmg/Sec 156-179" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl03',179,'d2_fire_dps','"Level 3 | Fire Dmg/Sec 156-179" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl03',7,'d2_yards','"Level 3 | Radius 7 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl04',25,'d2_mana','"Level 4 | Mana Cost 25" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl04',198,'d2_fire_dps','"Level 4 | Fire Dmg/Sec 198-222" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl04',222,'d2_fire_dps','"Level 4 | Fire Dmg/Sec 198-222" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl04',8,'d2_yards','"Level 4 | Radius 8 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl05',26,'d2_mana','"Level 5 | Mana Cost 26" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl05',241,'d2_fire_dps','"Level 5 | Fire Dmg/Sec 241-264" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl05',264,'d2_fire_dps','"Level 5 | Fire Dmg/Sec 241-264" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl05',10,'d2_yards','"Level 5 | Radius 10 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl06',27,'d2_mana','"Level 6 | Mana Cost 27" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl06',283,'d2_fire_dps','"Level 6 | Fire Dmg/Sec 283-307" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl06',307,'d2_fire_dps','"Level 6 | Fire Dmg/Sec 283-307" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl06',11,'d2_yards','"Level 6 | Radius 11 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl07',28,'d2_mana','"Level 7 | Mana Cost 28" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl07',323,'d2_fire_dps','"Level 7 | Fire Dmg/Sec 323-346" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl07',346,'d2_fire_dps','"Level 7 | Fire Dmg/Sec 323-346" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl07',12,'d2_yards','"Level 7 | Radius 12 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl08',29,'d2_mana','"Level 8 | Mana Cost 29" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl08',369,'d2_fire_dps','"Level 8 | Fire Dmg/Sec 369-392" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl08',392,'d2_fire_dps','"Level 8 | Fire Dmg/Sec 369-392" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl08',14,'d2_yards','"Level 8 | Radius 14 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl09',30,'d2_mana','"Level 9 | Mana Cost 30" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl09',435,'d2_fire_dps','"Level 9 | Fire Dmg/Sec 435-459" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl09',459,'d2_fire_dps','"Level 9 | Fire Dmg/Sec 435-459" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl09',15,'d2_yards','"Level 9 | Radius 15 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl10',31,'d2_mana','"Level 10 | Mana Cost 31" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl10',501,'d2_fire_dps','"Level 10 | Fire Dmg/Sec 501-525" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl10',525,'d2_fire_dps','"Level 10 | Fire Dmg/Sec 501-525" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl10',16,'d2_yards','"Level 10 | Radius 16 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl11',32,'d2_mana','"Level 11 | Mana Cost 32" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl11',568,'d2_fire_dps','"Level 11 | Fire Dmg/Sec 568-591" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl11',591,'d2_fire_dps','"Level 11 | Fire Dmg/Sec 568-591" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl11',18,'d2_yards','"Level 11 | Radius 18 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl12',33,'d2_mana','"Level 12 | Mana Cost 33" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl12',634,'d2_fire_dps','"Level 12 | Fire Dmg/Sec 634-658" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl12',658,'d2_fire_dps','"Level 12 | Fire Dmg/Sec 634-658" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl12',19,'d2_yards','"Level 12 | Radius 19 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl13',34,'d2_mana','"Level 13 | Mana Cost 34" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl13',700,'d2_fire_dps','"Level 13 | Fire Dmg/Sec 700-724" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl13',724,'d2_fire_dps','"Level 13 | Fire Dmg/Sec 700-724" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl13',20,'d2_yards','"Level 13 | Radius 20 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl14',35,'d2_mana','"Level 14 | Mana Cost 35" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl14',766,'d2_fire_dps','"Level 14 | Fire Dmg/Sec 766-790" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl14',790,'d2_fire_dps','"Level 14 | Fire Dmg/Sec 766-790" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl14',22,'d2_yards','"Level 14 | Radius 22 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl15',36,'d2_mana','"Level 15 | Mana Cost 36" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl15',833,'d2_fire_dps','"Level 15 | Fire Dmg/Sec 833-856" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl15',856,'d2_fire_dps','"Level 15 | Fire Dmg/Sec 833-856" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl15',23,'d2_yards','"Level 15 | Radius 23 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl16',37,'d2_mana','"Level 16 | Mana Cost 37" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl16',899,'d2_fire_dps','"Level 16 | Fire Dmg/Sec 899-923" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl16',923,'d2_fire_dps','"Level 16 | Fire Dmg/Sec 899-923" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl16',24,'d2_yards','"Level 16 | Radius 24 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl17',38,'d2_mana','"Level 17 | Mana Cost 38" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl17',998,'d2_fire_dps','"Level 17 | Fire Dmg/Sec 998-1,022" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl17',1022,'d2_fire_dps','"Level 17 | Fire Dmg/Sec 998-1,022" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl17',26,'d2_yards','"Level 17 | Radius 26 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl18',39,'d2_mana','"Level 18 | Mana Cost 39" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl18',1098,'d2_fire_dps','"Level 18 | Fire Dmg/Sec 1,098-1,121" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl18',1121,'d2_fire_dps','"Level 18 | Fire Dmg/Sec 1,098-1,121" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl18',27,'d2_yards','"Level 18 | Radius 27 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl19',40,'d2_mana','"Level 19 | Mana Cost 40" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl19',1197,'d2_fire_dps','"Level 19 | Fire Dmg/Sec 1,197-1,221" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_max_lvl19',1221,'d2_fire_dps','"Level 19 | Fire Dmg/Sec 1,197-1,221" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_radius_lvl19',28,'d2_yards','"Level 19 | Radius 28 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_manacost_lvl20',41,'d2_mana','"Level 20 | Mana Cost 41" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)'),
('d2-firewall-sorc','firewall_dps_min_lvl20',1296,'d2_fire_dps','"Level 20 | Fire Dmg/Sec 1,296-1,320" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23) [documented build point: slvl 20 maxed]'),
('d2-firewall-sorc','firewall_dps_max_lvl20',1320,'d2_fire_dps','"Level 20 | Fire Dmg/Sec 1,296-1,320" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23) [documented build point: slvl 20 maxed]'),
('d2-firewall-sorc','firewall_radius_lvl20',30,'d2_yards','"Level 20 | Radius 30 yards" rankedboost.com/diablo-2/sorceress/fire-wall/ (2026-07-23)');

-- ============ Fire Wall — skill constants, source: fextralife ============
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('d2-firewall-sorc','firewall_reqlevel',18,'d2_level','"Required Level: 18" diablo2.wiki.fextralife.com/Fire+Wall (2026-07-23)'),
('d2-firewall-sorc','firewall_castdelay_sec',1.4,'d2_seconds','"Cast Delay: 1.4 seconds" diablo2.wiki.fextralife.com/Fire+Wall (2026-07-23)'),
('d2-firewall-sorc','firewall_duration_sec',3.6,'d2_seconds','"Duration: 3.6 seconds" diablo2.wiki.fextralife.com/Fire+Wall (2026-07-23)');

-- ============ Fire Mastery synergy table (anchored levels), source: rankedboost ============
-- Anchor: rankedboost.com/diablo-2/sorceress/fire-mastery/ (2026-07-23). Multiplicative bonus fire damage.
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('d2-firewall-sorc','firemastery_bonus_pct_lvl01',30,'d2_pct_bonus_fire','"FM Level 1 | Bonus Fire Dmg 30%" rankedboost.com/diablo-2/sorceress/fire-mastery/ (2026-07-23)'),
('d2-firewall-sorc','firemastery_bonus_pct_lvl05',58,'d2_pct_bonus_fire','"FM Level 5 | Bonus Fire Dmg 58%" rankedboost.com/diablo-2/sorceress/fire-mastery/ (2026-07-23)'),
('d2-firewall-sorc','firemastery_bonus_pct_lvl10',93,'d2_pct_bonus_fire','"FM Level 10 | Bonus Fire Dmg 93%" rankedboost.com/diablo-2/sorceress/fire-mastery/ (2026-07-23)'),
('d2-firewall-sorc','firemastery_bonus_pct_lvl11',100,'d2_pct_bonus_fire','"FM Level 11 | Bonus Fire Dmg 100%" rankedboost.com/diablo-2/sorceress/fire-mastery/ (2026-07-23)'),
('d2-firewall-sorc','firemastery_bonus_pct_lvl15',128,'d2_pct_bonus_fire','"FM Level 15 | Bonus Fire Dmg 128%" rankedboost.com/diablo-2/sorceress/fire-mastery/ (2026-07-23)'),
('d2-firewall-sorc','firemastery_bonus_pct_lvl20',163,'d2_pct_bonus_fire','"FM Level 20 | Bonus Fire Dmg 163%" rankedboost.com/diablo-2/sorceress/fire-mastery/ (2026-07-23) [documented build point: FM maxed = +163%]');

-- ============ Character base attributes (Sorceress), source: maxroll (PIN-C3 primary) + fextralife corrob. ============
-- Anchor: maxroll.gg/d2/resources/sorceress-overview (2026-07-23). PIN-C3: maxroll primary for D2R numerics.
-- NOTE life_per_level / life_per_vit carry the maxroll value as primary; the fextralife conflict (+2/level, +3/vit)
--   is annotated in kit_composition + rules-manifest as a dual-anchored conflict per PIN-C3, not curated as a
--   separate kit_numeric row (dual-column PK is one value per key; conflict lives in the anchor annotation lane).
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('d2-firewall-sorc','attr_str_base',10,'d2_stat','"Strength: 10" maxroll.gg/d2/resources/sorceress-overview (2026-07-23)'),
('d2-firewall-sorc','attr_dex_base',25,'d2_stat','"Dexterity: 25" maxroll.gg/d2/resources/sorceress-overview (2026-07-23)'),
('d2-firewall-sorc','attr_vit_base',10,'d2_stat','"Vitality: 10" maxroll.gg/d2/resources/sorceress-overview (2026-07-23)'),
('d2-firewall-sorc','attr_energy_base',35,'d2_stat','"Energy: 35" maxroll.gg/d2/resources/sorceress-overview (2026-07-23)'),
('d2-firewall-sorc','life_base',40,'d2_flat_life','"Base Life: 40" maxroll.gg/d2/resources/sorceress-overview (2026-07-23)'),
('d2-firewall-sorc','mana_base',35,'d2_flat_mana','"Base Mana: 35" maxroll.gg/d2/resources/sorceress-overview (2026-07-23)'),
('d2-firewall-sorc','life_per_level',1,'d2_life_per_level','"Life per Level: +1" maxroll.gg/d2/resources/sorceress-overview (2026-07-23) [PIN-C3 maxroll primary; fextralife conflict +2/level dual-anchored on record]'),
('d2-firewall-sorc','mana_per_level',2,'d2_mana_per_level','"Mana per Level: +2" maxroll.gg/d2/resources/sorceress-overview (2026-07-23)'),
('d2-firewall-sorc','life_per_vit',2,'d2_life_per_vit','"Life per Vitality point: +2 per Vitality" maxroll.gg/d2/resources/sorceress-overview (2026-07-23) [PIN-C3 maxroll primary; fextralife conflict +3/vit dual-anchored on record]'),
('d2-firewall-sorc','mana_per_energy',2,'d2_mana_per_energy','"Mana per Energy point: +2 per Energy" maxroll.gg/d2/resources/sorceress-overview (2026-07-23)');

-- ============ FCR breakpoints (frames per cast), source: maxroll ============
-- Anchor: maxroll.gg/d2/resources/sorceress-overview (2026-07-23). D2 cast speed = frames/cast, not a multiplier.
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('d2-firewall-sorc','fcr_frames_at000',13,'d2_frames_per_cast','"0% FCR = 13 frames per cast" maxroll.gg/d2/resources/sorceress-overview (2026-07-23)'),
('d2-firewall-sorc','fcr_frames_at009',12,'d2_frames_per_cast','"9% FCR = 12 frames" maxroll.gg/d2/resources/sorceress-overview (2026-07-23)'),
('d2-firewall-sorc','fcr_frames_at020',11,'d2_frames_per_cast','"20% FCR = 11 frames" maxroll.gg/d2/resources/sorceress-overview (2026-07-23)'),
('d2-firewall-sorc','fcr_frames_at037',10,'d2_frames_per_cast','"37% FCR = 10 frames" maxroll.gg/d2/resources/sorceress-overview (2026-07-23)'),
('d2-firewall-sorc','fcr_frames_at063',9,'d2_frames_per_cast','"63% FCR = 9 frames" maxroll.gg/d2/resources/sorceress-overview (2026-07-23) [documented build target]'),
('d2-firewall-sorc','fcr_frames_at105',8,'d2_frames_per_cast','"105% FCR = 8 frames" maxroll.gg/d2/resources/sorceress-overview (2026-07-23) [documented build target]'),
('d2-firewall-sorc','fcr_frames_at200',7,'d2_frames_per_cast','"200% FCR = 7 frames" maxroll.gg/d2/resources/sorceress-overview (2026-07-23)');
