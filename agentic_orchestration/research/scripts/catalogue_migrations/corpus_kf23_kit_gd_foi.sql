-- corpus_kf23_kit_gd_foi.sql
-- KF-2 kit-side population — gd-flames-of-ignaffar-purifier (Flames of Ignaffar, Purifier).
-- Author: elrond | 2026-07-23 | Source note: agentic_orchestration/legolas/notes/2026-07-23-kf23-harvest-gd.md
-- Dual-column law: source_value IMMUTABLE + verbatim anchor; rdr_value NULL. Idempotent (INSERT OR REPLACE).
--
-- KIT HELD (CONDUCTOR PIN #8 / KFL-8(c)): curate ONLY the ANCHORED character formulas' SCALAR constants
-- (attributes, per-point contributions, PTH floor, crit-tier multipliers, armor absorption). The FoI per-rank
-- table (fire dmg min/max, burn, energy/sec per rank) is FULL GAP — grimtools JS-rendered, fandom 402 — so
-- ZERO FoI-rank rows are inserted (anchor law: gaps are absences, never estimates). A Matt fork on the gd
-- disposition is queued (KFL-8(c)); this curation must not pre-empt it.
--
-- SCHEMA NOTE (reported anomaly): kit_numeric.source_value is REAL. GD's PTH, OA, and DA are FORMULA
-- EXPRESSIONS, not scalars — they cannot live in a REAL column. Handling (no improvisation): the SCALAR
-- constants inside those formulas (per-point coefficients, the 55 floor, tier multipliers, 70% absorption)
-- are curated here as kit_numeric rows; the FORMULA EXPRESSIONS themselves are carried verbatim in the
-- composition ledger (ANCHORED factor refs) + the rules-needed manifest (the transforms the rules implement).
-- Crit-tier divergence: Source E (official grimdawn.com) is authoritative over Source D (community, 2.0x max);
-- the 1.5x-max official tier table is curated. Source D's 2.0x tier is NOT curated (superseded per note).

-- ============ Character attribute allocation (build-point invested points), source: lonewardengaming ============
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('gd-flames-of-ignaffar-purifier','attr_physique_invested',96,'gd_invested_points','"Physique: 96" lonewardengaming.com/grimdawn-home/purifierdwr/ (2026-07-23) [invested points; DW-Ranged Purifier variant]'),
('gd-flames-of-ignaffar-purifier','attr_cunning_invested',11,'gd_invested_points','"Cunning: 11" lonewardengaming.com/grimdawn-home/purifierdwr/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','attr_spirit_invested',0,'gd_invested_points','"Spirit: 0" lonewardengaming.com/grimdawn-home/purifierdwr/ (2026-07-23)');

-- ============ Per-point attribute contributions (SCALAR coefficients), source: grimdawn.com official ============
-- Anchor: grimdawn.com/guide/character/character-basics/ (2026-07-23). These scalars feed the HP/OA/DA formulas.
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('gd-flames-of-ignaffar-purifier','physique_hp_per_point',2.5,'gd_hp_per_point','"Every point of Physique increases your health by 2.5" grimdawn.com/guide/character/character-basics/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','physique_hpregen_per_point',0.05,'gd_hpregen_per_point','"...health regeneration by 0.05" grimdawn.com/guide/character/character-basics/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','physique_da_per_point',0.4,'gd_da_per_point','"...Defensive Ability by 0.4" (per Physique point) grimdawn.com/guide/character/character-basics/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','cunning_hp_per_point',1.0,'gd_hp_per_point','"Every point of Cunning increases health by 1.0" grimdawn.com/guide/character/character-basics/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','cunning_physpierce_dmg_pct_per_point',0.41,'gd_dmg_pct_per_point','"...your physical and pierce damage by 0.41%" (per Cunning point) grimdawn.com/guide/character/character-basics/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','cunning_oa_per_point',0.4,'gd_oa_per_point','"...Offensive Ability by 0.4" (per Cunning point) grimdawn.com/guide/character/character-basics/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','spirit_hp_per_point',1.5,'gd_hp_per_point','"Every point of Spirit increases your health by 1.5" grimdawn.com/guide/character/character-basics/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','spirit_magicdmg_pct_per_point',0.47,'gd_dmg_pct_per_point','"...magical damage by 0.47%" (per Spirit point) grimdawn.com/guide/character/character-basics/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','spirit_energy_per_point',2,'gd_energy_per_point','"...energy by 2" (per Spirit point) grimdawn.com/guide/character/character-basics/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','invested_point_to_attr_mult',8,'gd_attr_per_invested_point','"Each point will increase that attribute by 8" (1 invested point = +8 attribute stat) grimdawn.com/guide/character/character-basics/ (2026-07-23)');

-- ============ OA/DA formula base constants (SCALARS from the composite formulas), source: Steam Mechanics Guide ============
-- Anchor: steamcommunity.com/sharedfiles/filedetails/?id=596728673 (2026-07-23).
-- Full formulas: OA = (115 + 12*Level + 0.4*Cunning + FlatBonuses)*(1 + %OA/100); DA symmetric on Spirit.
-- The formula EXPRESSIONS are carried in the composition ledger + rules manifest; the SCALAR constants here.
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('gd-flames-of-ignaffar-purifier','oada_formula_base_const',115,'gd_oada_base','"OA = (115 + 12*Level + 0.4*Cunning + Other Flat Bonuses)*(1 + (%Offensive Ability bonus)/100)" steamcommunity.com/sharedfiles/filedetails/?id=596728673 (2026-07-23) [base constant 115; also DA base]'),
('gd-flames-of-ignaffar-purifier','oada_formula_level_coeff',12,'gd_oada_level_coeff','"OA = (115 + 12*Level + ...)" steamcommunity.com/sharedfiles/filedetails/?id=596728673 (2026-07-23) [per-level coefficient 12; symmetric for DA]');

-- ============ PTH (chance-to-hit / crit) constants, source: grimdawn.com official combat guide ============
-- Anchor: grimdawn.com/guide/gameplay/combat/ (2026-07-23). The full PTH formula expression lives in the
-- composition ledger + rules manifest (formula, not scalar). Here: the floor + crit-chance offset scalars.
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('gd-flames-of-ignaffar-purifier','pth_floor',55,'gd_pth_pct','"PTH cannot go below 55 for you or your enemies" grimdawn.com/guide/gameplay/combat/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','crit_chance_offset_from_pth',90,'gd_pth_pct','"The chance to critically strike is PTH - 90" (e.g. 95% PTH = 5% crit) grimdawn.com/guide/gameplay/combat/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','pth_equal_oa_da',90,'gd_pth_pct','"Equality of attackers OA and receivers DA results in a 90% chance to hit and 0% chance to crit" grimdawn.com/guide/gameplay/combat/ (2026-07-23)');

-- ============ Crit-damage tier table (official, Source E) — PTH threshold -> multiplier ============
-- Anchor: grimdawn.com/guide/gameplay/combat/ (2026-07-23). Official 1.5x-max table (Source D 2.0x superseded).
-- numeric_key: crit_mult_pthNNN = crit multiplier at PTH threshold NNN.
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('gd-flames-of-ignaffar-purifier','crit_mult_pth070',1.0,'gd_crit_mult','"70 | 1.0x (no crit)" grimdawn.com/guide/gameplay/combat/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','crit_mult_pth090',1.1,'gd_crit_mult','"90+ | 1.1x" grimdawn.com/guide/gameplay/combat/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','crit_mult_pth105',1.2,'gd_crit_mult','"105+ | 1.2x" grimdawn.com/guide/gameplay/combat/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','crit_mult_pth120',1.3,'gd_crit_mult','"120+ | 1.3x" grimdawn.com/guide/gameplay/combat/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','crit_mult_pth130',1.4,'gd_crit_mult','"130+ | 1.4x" grimdawn.com/guide/gameplay/combat/ (2026-07-23)'),
('gd-flames-of-ignaffar-purifier','crit_mult_pth135',1.5,'gd_crit_mult','"135+ | 1.5x (maximum)" grimdawn.com/guide/gameplay/combat/ (2026-07-23) [official max; Source E authoritative over Source D 2.0x]');

-- ============ Armor absorption (mitigation), source: grimdawn.com official ============
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('gd-flames-of-ignaffar-purifier','armor_absorption_default_pct',70,'gd_pct','"By default, your armor absorption is 70% across all your equipment" grimdawn.com/guide/gameplay/combat/ (2026-07-23)');

-- ============ FoI channel tick cadence (structural, anchored), source: Steam discussion synthesis ============
INSERT OR REPLACE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('gd-flames-of-ignaffar-purifier','foi_tick_interval_sec',0.3,'gd_seconds','"channeled skill ... dealing damage and draining energy every 0.3 seconds at 100% Cast Speed" grimtools/Crate forum synthesis, steamcommunity.com/app/219990/discussions/0/1620599015872291805/ (2026-07-23)');

-- NOTE: FoI per-rank damage table (fire min/max, burn, energy/sec) = FULL GAP. No rows inserted (anchor law).
--       Intensify / Endless Flame / energy-cost modifier numeric tables = FULL GAP. No rows inserted.
--       Build-point HP/OA/DA/armor-value/resists = GAP (formula-anchored but totals not verbatim). No rows inserted.
--       All gd GAPs registered in the rules-needed manifest + composition ledger (gap_excluded) — never estimated.
