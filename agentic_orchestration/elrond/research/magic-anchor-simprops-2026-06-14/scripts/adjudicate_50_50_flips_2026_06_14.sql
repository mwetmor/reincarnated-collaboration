-- adjudicate_50_50_flips_2026_06_14.sql
-- ----------------------------------------------------------------------------
-- Per-row correction pass on the magic-anchor caster sim_props (elrond commit
-- a9b48dc). Applies gandalf's adjudication (Matt-approved 2026-06-14) of the
-- two "closest-to-50/50" flag sets raised in MIGRATION.md § 5.3 and § 5.4.
--
-- ADJUDICATION PRINCIPLE (locked weapon-as-identity model):
--   The weapon FORM establishes CASTER at L1 (locked). Within "caster", the
--   row's POWER ELEMENT decides arcane-vs-faith via the engine's own locked
--   element->attribute coupling (element_biases.py:28):
--     fire/water/lightning/shadow -> INT / caster-arcane
--     earth/wind/holy             -> WIS / caster-faith
--
-- TARGET TEMPLATE BANDS (from MIGRATION.md § 4, live pool exemplars):
--   A  arcane single-target : rng 5.0-18.0  spd 1.5  chg 0.0  aoe 0.0  amp 0.84-2.4  smod 82
--   B  arcane area          : rng 5.0-18.0  spd 0.7  chg 1.2  aoe 3.5  amp 0.48-3.0  smod 68
--
-- element_affinity_modifiers_json is a per-instance flavor/affinity tag, NOT a
-- family-encoder (Discipline #14: tagged-not-encoded). Live pool already carries
-- 12 caster-arcane rows with {"holy":15}; holy-on-arcane is an established,
-- non-contradictory pattern. The element JSON is therefore LEFT UNCHANGED on all
-- flipped rows (the power element is what DROVE the flip; it is not re-authored).
--
-- v1_scope STAYS 1 on all 102 rows (Matt ACCEPTED the +102 pool growth). This
-- script does NOT touch weapon_knowledge_entries at all.
-- ----------------------------------------------------------------------------

BEGIN TRANSACTION;

-- ===========================================================================
-- § 5.3 FLIPS (3 of 6 ritual-form / occult-power rows flip; 3 stay)
-- ===========================================================================

-- 226135 Grimoire Athame of Solomon (shadow) -> caster-arcane / INT / template A
--   athame = single implement -> arcane single-target band.
UPDATE weapon_sim_props SET
    weapon_type_family       = 'caster-arcane',
    primary_stat             = 'INT',
    secondary_stat           = 'none',
    range_min_units          = 5.0,
    range_max_units          = 18.0,
    base_attack_speed        = 1.5,
    charge_time_s            = 0.0,
    aoe_radius_units         = 0.0,
    damage_amplitude_min     = 0.84,
    damage_amplitude_max     = 2.4,
    spell_damage_modifier_pct = 82.0,
    sim_viability_notes      = 'template=A; family=caster-arcane; gandalf_magic_anchor_simprops_v1_2026_06_14; gandalf-adjudicated 2026-06-14: faith->arcane by element-coupling (shadow->INT)'
WHERE weapon_id = 226135;

-- 226138 Seidstafr of the Volva (shadow) -> caster-arcane / INT / template A
--   seidstafr = single staff implement -> arcane single-target band.
UPDATE weapon_sim_props SET
    weapon_type_family       = 'caster-arcane',
    primary_stat             = 'INT',
    secondary_stat           = 'none',
    range_min_units          = 5.0,
    range_max_units          = 18.0,
    base_attack_speed        = 1.5,
    charge_time_s            = 0.0,
    aoe_radius_units         = 0.0,
    damage_amplitude_min     = 0.84,
    damage_amplitude_max     = 2.4,
    spell_damage_modifier_pct = 82.0,
    sim_viability_notes      = 'template=A; family=caster-arcane; gandalf_magic_anchor_simprops_v1_2026_06_14; gandalf-adjudicated 2026-06-14: faith->arcane by element-coupling (shadow->INT)'
WHERE weapon_id = 226138;

-- 226113 Witch's Brimstone Censer (fire) -> caster-arcane / INT / template B
--   censer = area form -> preserve area aoe/charge profile, move range into the
--   arcane band (5.0-18.0). amp/aoe/charge already match template B values.
UPDATE weapon_sim_props SET
    weapon_type_family       = 'caster-arcane',
    primary_stat             = 'INT',
    secondary_stat           = 'none',
    range_min_units          = 5.0,
    range_max_units          = 18.0,
    base_attack_speed        = 0.7,
    charge_time_s            = 1.2,
    aoe_radius_units         = 3.5,
    damage_amplitude_min     = 0.48,
    damage_amplitude_max     = 3.0,
    spell_damage_modifier_pct = 68.0,
    sim_viability_notes      = 'template=B; family=caster-arcane; gandalf_magic_anchor_simprops_v1_2026_06_14; gandalf-adjudicated 2026-06-14: faith->arcane by element-coupling (fire->INT)'
WHERE weapon_id = 226113;

-- 226140 Inquisitor's Iron Maiden Reliquary (holy-dark)  -> STAY caster-faith/WIS/D
-- 226122 Geomancer's Sigil-Pestle (earth)                -> STAY caster-faith/WIS/D
-- 226124 Witch-Storm Broom-Stave (wind)                  -> STAY caster-faith/WIS/D
--   (no UPDATE: element keeps them faith under the coupling; holy/earth/wind->WIS)

-- ===========================================================================
-- § 5.4 FLIPS (all 3 sci-fi WIS sceptres flip; tech-arcane power, INT wins)
--   Each row's CURRENT profile is area (chg 1.2 / aoe 3.5 present) -> map D->B.
--   Clear the resolved wis_caster_register_tension_scifi tag.
-- ===========================================================================

-- 226174 EMP Channeler Sceptre (lightning) -> caster-arcane / INT / template B
UPDATE weapon_sim_props SET
    weapon_type_family       = 'caster-arcane',
    primary_stat             = 'INT',
    secondary_stat           = 'none',
    range_min_units          = 5.0,
    range_max_units          = 18.0,
    base_attack_speed        = 0.7,
    charge_time_s            = 1.2,
    aoe_radius_units         = 3.5,
    damage_amplitude_min     = 0.48,
    damage_amplitude_max     = 3.0,
    spell_damage_modifier_pct = 68.0,
    sim_viability_notes      = 'template=B; family=caster-arcane; gandalf_magic_anchor_simprops_v1_2026_06_14; gandalf-adjudicated 2026-06-14: faith->arcane by element-coupling (lightning->INT); wis_caster_register_tension_scifi RESOLVED'
WHERE weapon_id = 226174;

-- 226178 Prism Array Sceptre (radiant/light; "array" = area) -> caster-arcane / INT / template B
--   element_affinity_modifiers_json {"holy":15} LEFT UNCHANGED (flavor tag; 12
--   caster-arcane rows already carry holy in the live pool).
UPDATE weapon_sim_props SET
    weapon_type_family       = 'caster-arcane',
    primary_stat             = 'INT',
    secondary_stat           = 'none',
    range_min_units          = 5.0,
    range_max_units          = 18.0,
    base_attack_speed        = 0.7,
    charge_time_s            = 1.2,
    aoe_radius_units         = 3.5,
    damage_amplitude_min     = 0.48,
    damage_amplitude_max     = 3.0,
    spell_damage_modifier_pct = 68.0,
    sim_viability_notes      = 'template=B; family=caster-arcane; gandalf_magic_anchor_simprops_v1_2026_06_14; gandalf-adjudicated 2026-06-14: faith->arcane by element-coupling (radiant/light tech-arcane, INT wins); wis_caster_register_tension_scifi RESOLVED'
WHERE weapon_id = 226178;

-- 226188 Blackhole Containment Sceptre (gravity/shadow; "blackhole" = area) -> caster-arcane / INT / template B
UPDATE weapon_sim_props SET
    weapon_type_family       = 'caster-arcane',
    primary_stat             = 'INT',
    secondary_stat           = 'none',
    range_min_units          = 5.0,
    range_max_units          = 18.0,
    base_attack_speed        = 0.7,
    charge_time_s            = 1.2,
    aoe_radius_units         = 3.5,
    damage_amplitude_min     = 0.48,
    damage_amplitude_max     = 3.0,
    spell_damage_modifier_pct = 68.0,
    sim_viability_notes      = 'template=B; family=caster-arcane; gandalf_magic_anchor_simprops_v1_2026_06_14; gandalf-adjudicated 2026-06-14: faith->arcane by element-coupling (gravity/shadow->INT); wis_caster_register_tension_scifi RESOLVED'
WHERE weapon_id = 226188;

COMMIT;
