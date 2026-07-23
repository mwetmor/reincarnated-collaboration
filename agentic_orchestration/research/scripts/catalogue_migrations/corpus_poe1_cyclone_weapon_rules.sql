-- corpus_poe1_cyclone_weapon_rules.sql
-- KFL-13(e) gamora weapon-composition rule step — poe1-cyclone build-point WEAPON normalization.
-- Author: gamora (rule_owner, sim-seam) | 2026-07-23 | Run: KIT-FIDELITY (conductor: gandalf RUN-CONDUCTOR)
-- Math note (Discipline #1, authored BEFORE this migration): §9 of
--   reincarnated-engine/src/reincarnated/simulation/math/kf5-expected-pct-2026-07-23.md
-- Leaf source (verbatim, immutable): corpus_poe1_cyclone_weapon_leaves.sql (elrond, KFL-13d).
-- Legolas anchor (conductor-verified ANCHORED, commit 8abfeed5):
--   agentic_orchestration/legolas/notes/2026-07-23-cyclone-weapon-dps-anchor.md
--
-- WHY: KF-4 left one RED acceptance assert (poe1-cyclone has_damage_base) because the kit carried ZERO
--   weapon leaf rows — Cyclone is weapon-dependent (deals weapon damage per hit × effectiveness of added
--   damage). elrond landed 12 verbatim weapon leaves (all rdr_value/rule_id NULL). THIS migration derives
--   their rdr_value + rule_id so the compiler can compose the per-hit weapon damage base and flip RED→GREEN.
--
-- DUAL-COLUMN LAW ENFORCED BY CONSTRUCTION: every leaf statement is an UPDATE touching ONLY
--   {rdr_value, rule_id, rule_version_applied}. source_value is NEVER in a SET clause. Every UPDATE is
--   guarded on `rdr_value IS NULL` so a re-run is a strict no-op AND no already-derived row (e.g. the
--   existing R-M5 poe1_pct leaves crit_chance_pct_topgear / move_speed_penalty / resist_cap, or the
--   R-CTX-GEO weapon_dps_target=650 context fence) is ever in scope. IDEMPOTENT + IMMUTABLE by construction.
--
-- RDR-UNIT CONVENTION (math note §9.4): rdr = source_value (IDENTITY) for every weapon leaf in the source
--   game's own scale — a base-phys number is a base-phys number, a % is a %, an APS is an APS, an iLvl is
--   an iLvl. The COMPOSITION that assembles the per-hit weapon band ((base+flat)×(1+local_inc/100)×eff)
--   is the COMPILER's job (kit_compiler.py amendment), EXACTLY as bonestorm's proj/explosion leaves are
--   IDENTITY and the compiler sums+scales them. No number here is composed, averaged, or derived — the
--   arithmetic lives in the compiler + the math note, anchored to PoB CalcOffence's local-mod path.
--
-- QUARANTINED DEFECTS NOT REUSED (KFL-13b): legolas's ~570 pDPS sketch is arithmetically wrong twice —
--   (i) an invented "+0.5% inc phys per 1% quality for two-handers" (the real PoE local rule is 1:1, so
--   quality 44 → +44% increased, additive with the 156% mod → 200% total → avg phys 376.5 → ~615 pDPS);
--   (ii) a per-hit sketch (570×0.59/3.0) that conflates Cyclone's attack CADENCE with per-hit MAGNITUDE.
--   NEITHER enters this migration: every leaf is pure IDENTITY (rdr = source_value); the corrected
--   composition (verified 615.01 pDPS against PoB CalcOffence) lives in the compiler + math note §9.2/§9.3.
--
-- BUILD-POINT / CONTEXT FENCE: these ARE the documented 3.15 endgame PoB weapon (Blood Razor, iLvl 83).
--   They carry the compiler's _bp selector suffix + the _v315 build-point marker. The aspirational
--   weapon_dps_target=650 (overgear floor, R-CTX-GEO) is NEVER the build point and is NEVER touched here.

-- =====================================================================================================
-- SECTION 1 — NEW normalization_rule rows (R-K6 weapon damage-base, R-K7 weapon APS/tempo)
--   Idempotent: INSERT OR REPLACE keyed on rule_id PK. rule_owner='gamora'. rule_version=1.
--   The existing R-M5 (poe1_pct) + R-CTX-GEO (poe1_level) rules ALREADY cover the other weapon scales —
--   NOT re-authored here; the leaf stamps below reference them.
-- =====================================================================================================
INSERT OR REPLACE INTO normalization_rule (rule_id, rule_version, source_scale, description, rule_owner, formula_ref, status) VALUES
('R-K6', 1, 'poe1_weapon_base_phys_v315',
 'PoE1 Cyclone 3.15 build-point WEAPON physical damage base (Blood Razor Exquisite Blade). IDENTITY_v1: rdr = source_value per leaf (base phys 67-112 + local added phys 23-49, in PoE''s own damage scale). WEAPON-COMPOSITION (compiler, NOT a leaf rescale): weapon per-hit phys band = (base+flat) x (1 + local_increased/100), local_increased = inc_phys(156, R-M5) + quality(44, R-M5, 1:1 PoE local-weapon rule) = 200% -> avg 376.5. Cyclone per-hit dealt = weapon-hit x effectiveness (59%, R-K4). Verified 615.01 pDPS vs PoB CalcOffence local-mod path (Path of Building Community src/Modules/CalcOffence.lua). Fills the base_weapon_dps gap as a per-hit band. Covers poe1_weapon_flat_phys_v315 (same rule; both v315 weapon-damage-base leaves). Anchor: pastebin.com/Sf8AYHkK PoB XML 1618-1634 + poedb.tw/us/Exquisite_Blade.',
 'gamora', 'catalogue_migrations/corpus_poe1_cyclone_weapon_rules.sql#R-K6 (math note kf5-expected-pct-2026-07-23.md §9.2/§9.4)', 'active'),
('R-K7', 1, 'poe1_weapon_aps_v315',
 'PoE1 Cyclone 3.15 build-point WEAPON base attacks/sec (Exquisite Blade 1.35 APS). IDENTITY_v1: rdr = source_value (1.35). TEMPO: final APS = base_aps x (1 + inc_attack_speed/100) = 1.35 x 1.21 = 1.6335 shapes per-hit CADENCE, NOT per-hit magnitude (fenced exactly like R-M4''s attack-speed; charter per-hit gauge separation). NEVER the per-hit damage denominator. Anchor: poedb.tw/us/Exquisite_Blade.',
 'gamora', 'catalogue_migrations/corpus_poe1_cyclone_weapon_rules.sql#R-K7 (math note kf5-expected-pct-2026-07-23.md §9.3/§9.4)', 'active');

-- =====================================================================================================
-- SECTION 2 — Leaf rdr_value derivation (UPDATE-only; dual-column law; each guarded on rdr_value IS NULL)
--   All 12 leaves derive IDENTITY (rdr = source_value). Guard = strict idempotency + existing-row safety.
-- =====================================================================================================

-- R-K6 — weapon damage-base leaves (base phys 67/112 + local added phys 23/49): 4 rows.
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-K6', rule_version_applied = 1
 WHERE kit_id = 'poe1-cyclone'
   AND source_scale IN ('poe1_weapon_base_phys_v315', 'poe1_weapon_flat_phys_v315')
   AND rdr_value IS NULL;

-- R-K7 — weapon base APS (1.35): 1 row.
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-K7', rule_version_applied = 1
 WHERE kit_id = 'poe1-cyclone'
   AND source_scale = 'poe1_weapon_aps_v315'
   AND rdr_value IS NULL;

-- R-M5 (EXISTING rule) — the 6 NEW weapon poe1_pct leaves (inc_phys 156, quality 44, inc_aps 21,
--   base_crit 5.7, crafted_crit 25, implicit_crit_multi 50). Scoped to the weapon_* namespace + NULL
--   guard so the pre-existing R-M5 poe1_pct rows (crit_chance_pct_topgear, move_speed_penalty_pct_gem20,
--   resist_cap_pct) are NEVER in scope. IDENTITY: rdr = source_value.
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-M5', rule_version_applied = 1
 WHERE kit_id = 'poe1-cyclone'
   AND source_scale = 'poe1_pct'
   AND numeric_key LIKE 'weapon_%'
   AND rdr_value IS NULL;

-- R-CTX-GEO (EXISTING rule) — weapon identity / gear-stage iLvl (83). poe1_level scale is already in
--   R-CTX-GEO's derivation scope. FENCED: context/gating, NEVER a damage magnitude. Scoped to the
--   weapon_identity_ilvl key so weapon_dps_target=650 (also R-CTX-GEO) is untouched (already has rdr).
UPDATE kit_numeric SET rdr_value = source_value, rule_id = 'R-CTX-GEO', rule_version_applied = 1
 WHERE kit_id = 'poe1-cyclone'
   AND numeric_key = 'weapon_identity_ilvl'
   AND rdr_value IS NULL;

-- =====================================================================================================
-- SECTION 3 — Guard asserts (fail LOUD if the migration touched anything it must not, or missed a leaf).
--   These SELECTs are diagnostics for the applying operator; sqlite3 prints them. Byte-rebuildable proof
--   is in the report (apply to a fresh copy → state matches live).
-- =====================================================================================================
-- (a) all 12 weapon leaves now carry rdr_value + rule_id (0 NULL remaining in the weapon_*-except-target set):
SELECT 'GUARD leaves_still_null (expect 0):' AS check_name,
       COUNT(*) AS n
  FROM kit_numeric
 WHERE kit_id = 'poe1-cyclone'
   AND numeric_key LIKE 'weapon_%'
   AND numeric_key != 'weapon_dps_target'
   AND (rdr_value IS NULL OR rule_id IS NULL);
-- (b) the context fence is intact (weapon_dps_target still R-CTX-GEO / 650, untouched):
SELECT 'GUARD dps_target_fence (expect 650/R-CTX-GEO):' AS check_name,
       rdr_value, rule_id
  FROM kit_numeric
 WHERE kit_id = 'poe1-cyclone' AND numeric_key = 'weapon_dps_target';
-- (c) dual-column immutability: every derived weapon leaf has rdr_value == source_value (IDENTITY):
SELECT 'GUARD identity_violations (expect 0):' AS check_name,
       COUNT(*) AS n
  FROM kit_numeric
 WHERE kit_id = 'poe1-cyclone'
   AND numeric_key LIKE 'weapon_%'
   AND numeric_key != 'weapon_dps_target'
   AND rdr_value IS NOT NULL
   AND rdr_value != source_value;
