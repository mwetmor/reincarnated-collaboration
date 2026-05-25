-- Cycle 12 SC-2 backfill — weapon_kind_classified_subtype on v1_scope=1 fantasy + military_modern
-- Authority: Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q5 sidecars SC-2)
-- KR-DIRECTIVE Option A scope: v1_scope=1 only (1,021 rows); v1_scope=0 (19,749 rows) DEFERRED to v1.1+
-- Executor: elrond
-- DB: /Users/admin/Games/reincarnated-loadout/data/telemetry.db
-- Table: weapon_knowledge_entries

PRAGMA busy_timeout=30000;
BEGIN TRANSACTION;

-- Exception 1: ammo_consumable (13 rows)
-- Fantasy bombs/grenades (D&D 5e Grenade weapon-class, thrown consumables)
-- + Warhammer standalone ammo-only profiles (Cannon Ball / Cannon Shell / Mortar Shell)
UPDATE weapon_knowledge_entries
SET weapon_kind_classified_subtype = 'ammo_consumable'
WHERE id IN (
    13731,  -- Arcano Bomb
    14269,  -- Bramble Bomb
    16197,  -- Gas Grenade
    16390,  -- Gravitic Grenade
    17182,  -- Laughing Gas Bomb
    18125,  -- Phosphorus Grenade
    19817,  -- Stun Grenade
    20076,  -- Thermobaric Bomb
    20313,  -- Venom Bomb
    178154, -- Dreadquake Bomb
    181148, -- Cannon Ball (standalone Warhammer ammo profile)
    179548, -- Cannon Shell (standalone Warhammer ammo profile)
    181151  -- Mortar Shell (standalone Warhammer ammo profile)
)
  AND weapon_kind_classified_subtype IS NULL
  AND v1_scope = 1
  AND register_canonical IN ('fantasy', 'military_modern');

-- Exception 2: siege_vehicle fantasy (25 rows)
-- Large fixed/mounted artillery in fantasy (Warhammer war machines + standalone fantasy siege)
-- Note: "Weapon: Ammo" compound names (e.g., "Great Cannon: Cannonball") are siege weapon profiles, NOT ammo
UPDATE weapon_knowledge_entries
SET weapon_kind_classified_subtype = 'siege_vehicle'
WHERE id IN (
    13848,  -- Ballista
    166414, -- Brutal Ballista
    178908, -- Dread Catapult - Necrotic Skulls
    178909, -- Dread Catapult - Cauldron of Torment
    178910, -- Dread Catapult - Cursed Stele
    180029, -- Drill Cannon
    179690, -- Fusil-cannon: Fortified Position
    179689, -- Fusil-cannon: Mobile
    179723, -- Great Cannon: Cannonball
    179725, -- Great Cannon: Grapeshot
    180016, -- Great Sky Cannon: Shell
    180017, -- Great Sky Cannon: Shrapnel
    180019, -- Great Volley Cannon
    180035, -- Grundstok Mortar
    178689, -- Harvestor Cannon
    180011, -- Heavy Sky Cannon: Shell
    180012, -- Heavy Sky Cannon: Shrapnel
    179294, -- Ironblaster Cannon: Cannon Ball
    179295, -- Ironblaster Cannon: Hail Shot
    178252, -- Plagueclaw Catapult
    178309, -- Poisoned Wind Mortar
    180027, -- Sky Cannon: Shrapnel
    180028, -- Sky Cannon: Shell
    179703, -- Steam Cannon
    178282  -- Warp Lightning Cannon
)
  AND weapon_kind_classified_subtype IS NULL
  AND v1_scope = 1
  AND register_canonical = 'fantasy';

-- Exception 3: siege_vehicle military_modern (13 rows)
-- Modern self-propelled howitzers, ATGM systems, mortars, off-route mines, ARV systems
UPDATE weapon_knowledge_entries
SET weapon_kind_classified_subtype = 'siege_vehicle'
WHERE id IN (
    183144, -- JPMRC VISMOD PCL-181 (SH-15) Chinese 155mm SPH
    183348, -- 2S19M2 (Msta-SM2) Russian 152mm SPH
    183952, -- AMX-10 PAC 90 French Amphibious Tank Destroyer / SP Artillery
    184181, -- 1V15 Russian Artillery Command and Reconnaissance Vehicle
    184445, -- KBA.48M Ukrainian 82mm Mortar
    184881, -- 2S22 Bogdana Ukrainian 155mm SPH
    186034, -- M110A1 American 203mm SPH
    186043, -- ATMOS 2000 Israeli 155mm SPH
    186073, -- 9K52 Luna-M (FROG-7) Russian Medium-Range Artillery Rocket System
    186278, -- PL-96 (Type 96) Chinese 122mm Towed Howitzer
    186697, -- FGM-148F Javelin American ATGM
    186706, -- PARM 2 German Off-Route Mine
    186745  -- 2S35-1 Koalitsiya-SV-KSh Russian 152mm SPH
)
  AND weapon_kind_classified_subtype IS NULL
  AND v1_scope = 1
  AND register_canonical = 'military_modern';

-- Exception 4: other (11 rows)
-- Per Cycle 10 precedent: knuckle dusters, banners, wondrous items, non-weapon polluters → 'other'
UPDATE weapon_knowledge_entries
SET weapon_kind_classified_subtype = 'other'
WHERE id IN (
    13513,  -- Abyssal Bane Knuckle Duster (rare)
    13514,  -- Abyssal Bane Knuckle Duster (very rare)
    13561,  -- Abyssal Bane Spiked Knuckle Duster (rare)
    14595,  -- Consecrated Weapon Knuckle Duster (uncommon)
    16832,  -- Hellscape Chatterbane Spiked Knuckle Duster
    18595,  -- Rootbound Multiweapon Knuckle Dusters
    18662,  -- Rootbound Multiweapon Spiked Knuckle Dusters (very rare)
    19441,  -- Spiked knuckle duster
    19641,  -- Starforged Weapon Knuckle Duster (legendary)
    13846,  -- Baba Yaga's Mortar and Pestle (wondrous-item / transport)
    177340  -- Crystal Healer (PF2e BACKGROUND, not a weapon — substrate pollution; flagged for v1.1+)
)
  AND weapon_kind_classified_subtype IS NULL
  AND v1_scope = 1
  AND register_canonical = 'fantasy';

-- Exception 5: accessory_handheld (11 rows)
-- Fantasy talismans per Cycle 10 doctrine (Tier-S talismans → accessory_handheld)
UPDATE weapon_knowledge_entries
SET weapon_kind_classified_subtype = 'accessory_handheld'
WHERE id IN (
    181236, -- Talisman
    181237, -- Canvas Talisman
    181238, -- Thorolund Talisman
    181239, -- Ivory Talisman
    181240, -- Sunlight Talisman
    181241, -- Darkmoon Talisman
    187581, -- Talisman (dup)
    187583, -- Sunlight Talisman (dup)
    187584, -- Canvas Talisman (dup)
    187585, -- White Hair Talisman
    187586  -- Sunless Talisman
)
  AND weapon_kind_classified_subtype IS NULL
  AND v1_scope = 1
  AND register_canonical = 'fantasy';

-- Bulk default: handheld_weapon for everything else NULL in v1_scope=1 (948 rows)
-- This covers the 917 fantasy named_template + 77 fantasy category + 15 military_modern category
-- + 1 fantasy unknown (Crystal Healer was already moved to 'other' above) minus 73 explicit exceptions
UPDATE weapon_knowledge_entries
SET weapon_kind_classified_subtype = 'handheld_weapon'
WHERE weapon_kind_classified_subtype IS NULL
  AND v1_scope = 1
  AND register_canonical IN ('fantasy', 'military_modern');

COMMIT;

-- Post-update audit
SELECT 'Post-update NULL count (target: 0)' AS check_item, COUNT(*) AS value
FROM weapon_knowledge_entries
WHERE weapon_kind_classified_subtype IS NULL
  AND v1_scope = 1
  AND register_canonical IN ('fantasy', 'military_modern');

SELECT '--- Final subtype distribution (v1_scope=1 fantasy+military_modern) ---' AS section;
SELECT weapon_kind_classified_subtype, COUNT(*)
FROM weapon_knowledge_entries
WHERE v1_scope = 1 AND register_canonical IN ('fantasy','military_modern')
GROUP BY weapon_kind_classified_subtype
ORDER BY COUNT(*) DESC;

-- Confirm v1_scope=0 NULL rows are still untouched (DEFERRED per Option A scope)
SELECT 'v1_scope=0 NULL rows (DEFERRED to v1.1+; target: 19,749)' AS check_item, COUNT(*) AS value
FROM weapon_knowledge_entries
WHERE v1_scope = 0
  AND register_canonical IN ('fantasy', 'military_modern')
  AND weapon_kind_classified_subtype IS NULL;
