-- corpus_kf23_kit_poe1_cyclone.sql
-- KF-2 kit-side population — poe1-cyclone (Cyclone Slayer).
-- Author: elrond | 2026-07-23 | Source note: agentic_orchestration/legolas/notes/2026-07-23-kf23-harvest-poe1.md
-- Dual-column law: source_value IMMUTABLE + verbatim anchor; rdr_value NULL. Idempotent (INSERT OR REPLACE).
--
-- VERSION PIN (KFL-3/KFL-5 conductor, ref CONDUCTOR PIN #1): poe1-cyclone build point = 3.15 era.
--   59% effectiveness of added damage at gem 20 IS the corpus-cited documented build point the join key
--   measures against (pathofexile.com/forum/view-thread/3078559). The current poedb.tw table (150% at gem 20,
--   post-3.27 buff) is CONTEXT ONLY — curated below with source_scale '..._v327_context' + anchor marked
--   [CONTEXT ONLY — NOT build point] so the harvested verbatim data is preserved (reversibility) WITHOUT
--   the pin being violated. Era re-pin would require a kit_citations amendment first (out of this run).
--
-- Cyclone is WEAPON-DEPENDENT (channel-move; deals weapon damage per hit × effectiveness). There is no
-- fixed skill damage roll — the source_value that matters is effectiveness% + attack-speed multiplier + the
-- weapon DPS (weapon DPS at build point is a PARTIAL gap: "650+ dps" target only, curated as gap-annotated).

-- ============ 3.15 build-point effectiveness (THE documented build point) ============
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('poe1-cyclone','effectiveness_pct_gem20_bp',59,'poe1_effectiveness_pct_v315','"deals 59% of Base Damage, and has 59% Effectiveness of Added Damage at gem level 20" pathofexile.com/forum/view-thread/3078559 (2026-07-23) [3.15 era — THE documented build point per CONDUCTOR PIN #1]'),
('poe1-cyclone','base_damage_pct_gem20_bp',59,'poe1_base_damage_pct_v315','"deals 59% of Base Damage ... at gem level 20" pathofexile.com/forum/view-thread/3078559 (2026-07-23) [3.15 era build point]');

-- ============ Attack-speed multiplier + AoE (version-stable skill mechanics, poedb) ============
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('poe1-cyclone','attack_speed_pct_of_base',300,'poe1_attack_speed_pct','"Attack Speed: 300% of base" poedb.tw/us/Cyclone (2026-07-23)'),
('poe1-cyclone','radius',16,'poe1_radius_units','"Radius: 16" poedb.tw/us/Cyclone (2026-07-23)');

-- ============ poedb CURRENT (post-3.27) level progression — CONTEXT ONLY, not the build point ============
-- Base Dmg % column: v3.27 effectiveness scaling. Curated to preserve harvested verbatim data; source_scale
-- marks it _v327_context; every anchor carries [CONTEXT ONLY]. The pin governs: gem20=150% here is NOT the
-- build point (the build point is 59%, above). Str/Dex/mana-req columns are version-agnostic char requirements.
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('poe1-cyclone','basedmg_pct_gem01_v327ctx',81.6,'poe1_effectiveness_pct_v327_context','"Gem 1 | Base Dmg 81.6%" poedb.tw/us/Cyclone (2026-07-23) [CONTEXT ONLY — post-3.27, NOT build point]'),
('poe1-cyclone','basedmg_pct_gem05_v327ctx',96,'poe1_effectiveness_pct_v327_context','"Gem 5 | Base Dmg 96%" poedb.tw/us/Cyclone (2026-07-23) [CONTEXT ONLY — post-3.27, NOT build point]'),
('poe1-cyclone','basedmg_pct_gem10_v327ctx',114,'poe1_effectiveness_pct_v327_context','"Gem 10 | Base Dmg 114%" poedb.tw/us/Cyclone (2026-07-23) [CONTEXT ONLY — post-3.27, NOT build point]'),
('poe1-cyclone','basedmg_pct_gem15_v327ctx',132,'poe1_effectiveness_pct_v327_context','"Gem 15 | Base Dmg 132%" poedb.tw/us/Cyclone (2026-07-23) [CONTEXT ONLY — post-3.27, NOT build point]'),
('poe1-cyclone','basedmg_pct_gem19_v327ctx',146.4,'poe1_effectiveness_pct_v327_context','"Gem 19 | Base Dmg 146.4%" poedb.tw/us/Cyclone (2026-07-23) [CONTEXT ONLY — post-3.27, NOT build point]'),
('poe1-cyclone','basedmg_pct_gem20_v327ctx',150,'poe1_effectiveness_pct_v327_context','"Gem 20 | Base Dmg 150%" poedb.tw/us/Cyclone (2026-07-23) [CONTEXT ONLY — post-3.27 buff, NOT the 3.15 build point]'),
-- gem-20 character requirements (version-stable), poedb
('poe1-cyclone','req_level_gem20',70,'poe1_level','"Gem 20 | Req Level 70" poedb.tw/us/Cyclone (2026-07-23)'),
('poe1-cyclone','req_str_gem20',68,'poe1_stat_req','"Gem 20 | Str 68" poedb.tw/us/Cyclone (2026-07-23)'),
('poe1-cyclone','req_dex_gem20',98,'poe1_stat_req','"Gem 20 | Dex 98" poedb.tw/us/Cyclone (2026-07-23)'),
('poe1-cyclone','mana_cost_gem20',3,'poe1_mana','"Gem 20 | Mana Cost 3" poedb.tw/us/Cyclone (2026-07-23)'),
('poe1-cyclone','move_speed_penalty_pct_gem20',20,'poe1_pct','"Gem 20 | Move Speed Penalty 20%" poedb.tw/us/Cyclone (2026-07-23)');

-- ============ Character / defense build-point (Cyclone Slayer) — mostly PARTIAL/GAP ============
-- What IS verbatim-anchored (values marked one_source / range where the note flags them). Exact Str/Dex/Int,
-- armor, evasion, resist %, crit multi, attack speed at build point are GAP (rules-manifest + composition ledger).
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('poe1-cyclone','crit_chance_pct_topgear',96,'poe1_pct','"~96% Crit Chance in top-end gear" poe-vault.com [3.20] Cyclone Slayer guide (2026-07-23) [range/top-gear anchor, not stat-sheet]'),
('poe1-cyclone','life_pool',6000,'poe1_flat_life','"6k life pool" overgear.com Cyclone Slayer build guide (2026-07-23) [approx, one-source; not stat-sheet verbatim]'),
('poe1-cyclone','resist_cap_pct',75,'poe1_pct','"75% cap for Fire/Cold/Lightning resistances" maxroll.gg Cyclone Slayer guide (2026-07-23) [cap target, not per-resist exact value]'),
('poe1-cyclone','weapon_dps_target',650,'poe1_weapon_dps','"Exquisite Blade with 650+ dps" overgear.com (2026-07-23) [target floor, not stat-sheet; weapon-dependent — join key composes weapon DPS x effectiveness]'),
('poe1-cyclone','gem_available_level',28,'poe1_level','"Cyclone available at level 28" maxroll.gg Cyclone Slayer guide (2026-07-23)');
