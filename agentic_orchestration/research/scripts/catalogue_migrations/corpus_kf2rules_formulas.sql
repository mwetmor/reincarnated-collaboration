-- corpus_kf2rules_formulas.sql
-- KF-2 resolution-formula anchor register (manifest E/F/G) — the VERBATIM anchored hit/crit/mitigation
-- formulas the normalization rules reference via formula_ref. KFL-7 first-class formula anchors.
-- Author: gamora (rule_owner, sim-seam) | 2026-07-23 | Run: KIT-FIDELITY (KFL-9c)
-- Math note: reincarnated-engine/src/reincarnated/simulation/math/kf2-rdr-normalization-convention.md (s1 E/F/G, s4).
--
-- WHY THIS FILE: the normalization_rule.formula_ref column is "a pointer, not inline math." For the
-- RESOLUTION-FORMULA rules (E hit / F crit / G mitigation), formula_ref points HERE, at the ONE committed
-- home of the verbatim anchored expression (anchor law: formulas are first-class harvest targets under the
-- same anchor discipline as values, charter KFL-7). These formulas are NOT leaf transforms — they are the
-- factors the kit_composition chain multiplies by. This file carries NO SQL derivation of a leaf; it is the
-- anchored-formula record. It runs clean (no-op) so the .sql set is byte-rebuildable and self-documenting.
-- The composition ledger (kit_composition) already carries these factors verbatim in its `ref` column
-- (comp_ids referenced below); this file is the rule-lane's anchor cross-index for formula_ref resolution.
--
-- No table is written. Assertions below prove the anchored LEAF inputs these formulas consume exist and
-- derive, so a formula rule's status='active' is honest (its inputs are present even where a build-point
-- input is GAP). Each assertion is a SELECT that must return the expected count; a mismatch is a STOP.
-- =====================================================================================================

-- ============ E — HIT-CHANCE FORMULAS (verbatim anchors) ============
--
-- R-H1  D2 chance-to-hit (received: mob attacks vs sorc). ANCHORED verbatim:
--   ChanceToHit = min( max( 200% * (AR / (AR + Dr)) * (ALVL / (ALVL + TLVL)), 5% ), 95% )
--   Anchor: maxroll.gg/d2/resources/hit-chance-mechanics + diablo2.wiki.fextralife.com (formulas C1).
--   INPUTS: AR = mob attack rating (monster_numeric d2_attack_rating, R-N1, ANCHORED: Fallen 8, Zombie 8).
--           Dr = sorc Defense at build point = GAP (composition sorc_defense gap_excluded, comp_id 84/71).
--           ALVL/TLVL = attacker/target level = build-point GAP.
--   -> PARTIAL: hit_chance computes from anchored mob AR; the sorc-side Dr/level GAP is NAMED (charter s9).
--
-- R-H2  D2 fire-skill hit-chance (dealt). PINNED: hit_chance = 1 (fire spells bypass AR).
--   PIN-C2 / CONDUCTOR PIN #3. Blanket verbatim unfindable (GAP-C2); named bypass-skill list exists.
--   -> composition dealt hit_chance = 1.0 (pinned, comp_id 79/66).
--
-- R-H3  PoE1 Cyclone accuracy/evasion (entropy). ANCHORED (prose): "Evasion only works against attacks"
--   -> Cyclone IS an attack, so evasion applies (dealt); monster attacks vs player evasion (received).
--   FORMULA EXPRESSION = GAP-A2 (the numeric entropy expression is image-only on the anchor page).
--   -> PARTIAL: the applies/does-not-apply rule is anchored; the % expression is GAP-A2, NAMED (charter s9).
--
-- R-H4  PoE2 Bonestorm evasion. ANCHORED verbatim (LOAD-BEARING correction, CONDUCTOR PIN #6 / formulas B2):
--   "able to evade any incoming projectile or strike ... whether ... an arrow ... or a fireball" -- AoE
--   explosion EXEMPT ("cannot be evaded"). -> projectile component EVADABLE (monster Accuracy vs player
--   Evasion); explosion component AoE-EXEMPT (hit_chance_explosion = 1). Monster-side spells: monster
--   Accuracy vs player Evasion. Composition splits comp_id 102 (projectile) / 103 (explosion=exempt).
--
-- R-H5  GD PTH (chance-to-hit + crit base). ANCHORED verbatim (grimdawn.com/guide/gameplay/combat):
--   PTH = ((((OA / ((DA/3.5) + OA)) * 300) * 0.3) + (((((OA*3.25) + 10000) - (DA*3.25)) / 100) * 0.7)) - 50
--   floor 55.  INPUTS: OA/DA = offensive/defensive ability at build point (+ monster side) = GAP.
--   Leaves present: gd_pth_pct (pth_floor 55, crit_offset 90, pth_equal_oa_da 90) derive IDENTITY (R-A2/R-C2).
--   -> PARTIAL: formula anchored verbatim; OA/DA totals GAP, NAMED (charter s9).

-- ============ F — CRIT-EV FORMULAS (verbatim anchors) ============
--
-- R-C1  D2 crit-EV = 1 (no spell crit). PINNED (PIN-A / CONDUCTOR PIN #2). Non-crit mean. comp_id 80/67/85/72.
--
-- R-C2  GD crit-EV (FoI). ANCHORED verbatim (grimdawn.com, Source E authoritative over Source D 2.0x):
--   crit_chance = PTH - 90 ;  crit multiplier TIER table by PTH:
--     PTH  70 -> 1.0x | 90 -> 1.1x | 105 -> 1.2x | 120 -> 1.3x | 130 -> 1.4x | 135 -> 1.5x
--   crit-weighted mean (PIN-A). Leaves: gd_crit_mult (6) + gd_pth_pct (3) derive IDENTITY (R-C2 scope).
--
-- R-C3  PoE1 Cyclone crit-EV. ANCHORED (leaf): crit_chance ~96% top-gear (poe1_pct, IDENTITY).
--   crit MULTIPLIER = GAP -> crit-EV PARTIAL (crit-weighted mean cannot complete without multi), NAMED.
--
-- R-C4  PoE2 Bonestorm crit-EV. ANCHORED (leaf): base crit 15% (poe2_pct, IDENTITY).
--   total crit chance (gear/passive) + crit multi = GAP -> crit-EV PARTIAL, NAMED.

-- ============ G — MITIGATION FORMULAS (verbatim anchors) ============
--
-- R-G1  PoE1 physical armour DR (dealt vs target armour). ANCHORED verbatim (pathofexile.com forum, A1):
--   ArmourReduction = Armour / (Armour + 10 * PhysicalRawDamage) ;  cap 90%.
--   THE loud KFL-7 case (Cyclone physical vs 28,790-35,988 armour). Target armour anchored (R-N2, 8 rows).
--   -> composition target_mitigation = (1 - ArmourReduction), comp_id 93.
--
-- R-G2  D2 target fire-resist mitigation (dealt). Standard resist form:
--   damage_after = damage * (1 - fire_resist_pct / 100). Act-1 Normal fire_resist_pct = 0%
--   (monster_numeric, gap_flag=normal_resist_inferred, value preserved). Sorc has no native -enemy resist.
--   -> composition target_fire_resist, comp_id 81/68.
--
-- R-G3  GD armor absorption (dealt). ANCHORED verbatim (grimdawn.com/guide/gameplay/combat):
--   "armor absorption is 70% ... 30% always through" -> absorbed = min(armor, dmg)*0.70; 30% always through.
--   gd_pct=70 leaf IDENTITY. Armor RATING at build point = GAP -> PARTIAL, NAMED. comp_id 122 (received side
--   armor_absorption anchored; dealt side target armor RATING GAP-D2).
--
-- R-G4  PoE2 armour DR (dealt vs target armour). BLOCKED / GAP-EXCLUDED (GAP-B1 / CONDUCTOR PIN #6).
--   PoE2 armour DR formula un-anchored. NOT AUTHORED. Dealt-% renders PRE-ARMOUR, NAMED (charter s9).
--   The poe2 armour RATING leaf (R-N3) still derives IDENTITY; only this FORMULA is excluded (comp_id 105).
--
-- R-G5  Player defensive-sheet mitigation (received, ALL kits). GAP across all 5 kits (build-point player
--   sheets un-anchored). No verbatim formula authorable. Received-% falls back PRE-MITIGATION and SAYS SO
--   (charter s9 ladder: source-game base-at-level -> else pre-mitigation). A documented render-state, not a
--   leaf transform. Composition player_mitigation factors gap_excluded (comp_ids 86/73/98/111).

-- =====================================================================================================
-- INPUT-PRESENCE ASSERTIONS (prove the anchored LEAF inputs exist so active-status is honest).
-- Each SELECT prints a label + a count; the expected count is in the label. A mismatch is a STOP-and-report.
-- (Read-only; writes nothing.)
-- =====================================================================================================
SELECT 'ASSERT R-H1 mob AR leaves (expect 4)=' || COUNT(*) FROM monster_numeric WHERE source_scale='d2_attack_rating';
SELECT 'ASSERT R-G1 poe1 armour leaves (expect 8)=' || COUNT(*) FROM monster_numeric WHERE source_scale='poe1_armour_rating';
SELECT 'ASSERT R-G2 d2 fire_resist leaves (expect >=2)=' || COUNT(*) FROM monster_numeric WHERE numeric_key='fire_resist_pct' AND game='d2';
SELECT 'ASSERT R-H5/R-C2 gd_pth_pct leaves (expect 3)=' || COUNT(*) FROM kit_numeric WHERE source_scale='gd_pth_pct';
SELECT 'ASSERT R-C2 gd_crit_mult leaves (expect 6)=' || COUNT(*) FROM kit_numeric WHERE source_scale='gd_crit_mult';
SELECT 'ASSERT R-G3 gd_pct absorption leaf (expect 1)=' || COUNT(*) FROM kit_numeric WHERE source_scale='gd_pct';
SELECT 'ASSERT R-C3 poe1 crit leaf (expect >=1)=' || COUNT(*) FROM kit_numeric WHERE source_scale='poe1_pct' AND numeric_key LIKE '%crit%';
SELECT 'ASSERT R-C4 poe2 crit leaf (expect >=1)=' || COUNT(*) FROM kit_numeric WHERE source_scale='poe2_pct' AND numeric_key LIKE '%crit%';
