-- corpus_poe1_cyclone_weapon_leaves.sql
-- KFL-13(d) elrond micro-lane — poe1-cyclone documented-3.15 build-point WEAPON leaves.
-- Author: elrond | 2026-07-23 | Source note (conductor-verified ANCHORED, commit 8abfeed5):
--   agentic_orchestration/legolas/notes/2026-07-23-cyclone-weapon-dps-anchor.md
--
-- WHY: KF-4 left one RED acceptance assert (poe1-cyclone has_damage_base) because the kit carried
--   ZERO weapon leaf rows — Cyclone is weapon-dependent (deals weapon damage per hit x effectiveness),
--   so with no weapon the damage base cannot compose. legolas anchored the documented 3.15 Cyclone
--   Slayer build (thread 3033867) whose embedded PoB export (pastebin Sf8AYHkK) carries a verbatim
--   Weapon-1 item block. These rows store the VERBATIM LEAVES ONLY. The gamora weapon-composition
--   normalization rule (queued behind KF-5) derives rdr_value + flips the assert RED->GREEN.
--
-- DUAL-COLUMN LAW: source_value = the verbatim number; source_anchor = the verbatim quote it came from
--   (PoB XML line or poedb stat). rdr_value STAYS NULL and rule_id STAYS NULL — composition/derivation
--   is gamora's normalization-rule step, NOT this leaf lane. No number here is computed, averaged, or
--   derived. (Conductor KFL-13b flagged two arithmetic defects in the note's DERIVED ~570 pDPS sketch:
--   a wrong two-hander quality rule and a per-hit/cadence conflation. NEITHER touches these rows —
--   they are pure verbatim leaves; the composition that would have consumed that arithmetic is gamora's,
--   pinned to a citable source (PoB CalcOffence), jack-ryan-checked. Recorded so it cannot leak in.)
--
-- IDEMPOTENCY + IMMUTABILITY: INSERT OR IGNORE (ON CONFLICT DO NOTHING) — strictly existing-row-preserving.
--   DEVIATION FROM HOUSE STYLE (logged, not silent): the sibling file corpus_kf23_kit_poe1_cyclone.sql
--   uses INSERT OR REPLACE. This file uses INSERT OR IGNORE instead, because the micro-lane mandate is to
--   NEVER overwrite any existing row (incl. the immutable weapon_dps_target=650 context row under R-CTX-GEO,
--   the overgear aspirational floor the compiler correctly never consumes). OR IGNORE makes existing-row
--   immutability STRUCTURAL: a re-run against a populated DB is a no-op on every prior row. All new keys
--   below are collision-free (weapon_* namespace, verified absent 2026-07-23), so nothing is silently skipped
--   on first apply; on re-apply, all 12 rows conflict-skip -> byte-stable proof.
--
-- BUILD-POINT SELECTOR: these ARE the documented 3.15 endgame PoB weapon (Blood Razor, iLvl 83). They carry
--   the compiler's _bp suffix (the KF-4 build-point selector treats _bp rows as build-point anchors and skips
--   any key carrying _v327_context/_ctx). Damage-shaping weapon scales carry the _v315 build-point marker
--   (matching effectiveness_pct_gem20_bp's poe1_effectiveness_pct_v315), so the future weapon-composition rule
--   selects them as the 3.15 build point and never confuses them with the _v327_context fence. Pure-percentage
--   modifiers reuse the version-stable poe1_pct scale already established for this kit.

-- ============ Weapon IDENTITY / gear-stage (context leaf — full identity in the anchor text) ============
-- Recorded per the micro-lane brief ("record the weapon identity/gear-stage somewhere appropriate").
-- source_value = iLvl 83 (a real verbatim number worth carrying). rule_id STAYS NULL like every leaf here
-- (gamora's rule step decides any fencing at derivation; the durable identity lives in source_anchor).
INSERT OR IGNORE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('poe1-cyclone','weapon_identity_ilvl',83,'poe1_level','"Blood Razor" rare Exquisite Blade, Item Level 83, Quality 44, active Weapon 1 (PoB slot line 1840). The documented 3.15 endgame Cyclone Slayer PoB variant. pastebin.com/Sf8AYHkK PoB XML lines 1618-1634 (2026-07-23) [WEAPON IDENTITY / gear-stage — build point]');

-- ============ poedb base-item stats (Exquisite Blade — version-stable base) ============
INSERT OR IGNORE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('poe1-cyclone','weapon_base_phys_min_bp',67,'poe1_weapon_base_phys_v315','"Physical Damage 67-112" (min) poedb.tw/us/Exquisite_Blade (2026-07-23) [base item stat — Blood Razor base]'),
('poe1-cyclone','weapon_base_phys_max_bp',112,'poe1_weapon_base_phys_v315','"Physical Damage 67-112" (max) poedb.tw/us/Exquisite_Blade (2026-07-23) [base item stat — Blood Razor base]'),
('poe1-cyclone','weapon_base_aps_bp',1.35,'poe1_weapon_aps_v315','"Attacks per Second 1.35" poedb.tw/us/Exquisite_Blade (2026-07-23) [base item stat]'),
('poe1-cyclone','weapon_base_crit_chance_pct_bp',5.7,'poe1_pct','"Critical Strike Chance 5.7%" poedb.tw/us/Exquisite_Blade (2026-07-23) [base item stat]');

-- ============ PoB item-block mods (verbatim from PoB XML Sf8AYHkK lines 1618-1634) ============
INSERT OR IGNORE INTO kit_numeric (kit_id, numeric_key, source_value, source_scale, source_anchor) VALUES
('poe1-cyclone','weapon_mod_inc_phys_pct_bp',156,'poe1_pct','"156% increased Physical Damage" pastebin.com/Sf8AYHkK PoB XML line 1629 (2026-07-23) [Blood Razor mod, 3.15 build point]'),
('poe1-cyclone','weapon_mod_flat_phys_min_bp',23,'poe1_weapon_flat_phys_v315','"Adds 23 to 49 Physical Damage" (min) pastebin.com/Sf8AYHkK PoB XML line 1630 (2026-07-23) [Blood Razor mod]'),
('poe1-cyclone','weapon_mod_flat_phys_max_bp',49,'poe1_weapon_flat_phys_v315','"Adds 23 to 49 Physical Damage" (max) pastebin.com/Sf8AYHkK PoB XML line 1630 (2026-07-23) [Blood Razor mod]'),
('poe1-cyclone','weapon_mod_inc_attack_speed_pct_bp',21,'poe1_pct','"21% increased Attack Speed" pastebin.com/Sf8AYHkK PoB XML line 1631 (2026-07-23) [Blood Razor mod]'),
('poe1-cyclone','weapon_quality_pct_bp',44,'poe1_pct','"Quality: 44" (incl. {crafted}+14% to Quality) pastebin.com/Sf8AYHkK PoB XML lines 1624 + 1633 (2026-07-23) [Blood Razor total quality]'),
('poe1-cyclone','weapon_implicit_global_crit_multi_pct_bp',50,'poe1_pct','"+50% to Global Critical Strike Multiplier" (implicit) pastebin.com/Sf8AYHkK PoB XML line 1628 (2026-07-23) [Blood Razor implicit]'),
('poe1-cyclone','weapon_crafted_inc_crit_chance_pct_bp',25,'poe1_pct','"{crafted}25% increased Critical Strike Chance" pastebin.com/Sf8AYHkK PoB XML line 1632 (2026-07-23) [Blood Razor crafted mod]');
