#!/usr/bin/env python3
"""
Build the VS2a icon + interactable-prop curation subset manifests.

Consumes (legolas raw catalogue, 2026-05-17 crawl):
    agentic_orchestration/research/catalogue/icons-and-props-2026-05-17/floor-loot.jsonl
    agentic_orchestration/research/catalogue/icons-and-props-2026-05-17/ambient-props.jsonl
    agentic_orchestration/research/catalogue/icons-and-props-2026-05-17/ui-icons.jsonl

Produces (curated subsets — drax-consumable):
    agentic_orchestration/research/curated/floor-loot-subset-vs2a-2026-05-17.jsonl
    agentic_orchestration/research/curated/ambient-props-subset-vs2a-2026-05-17.jsonl
    agentic_orchestration/research/curated/ui-icons-subset-vs2a-2026-05-17.jsonl

Subset selection methodology (parallel to elrond's Pimen VS2a curation pattern):

  Step 1 — Per legolas raw row, decide one of:
      RECOMMEND-PRIMARY  : in active subset; first-call pack for its coverage cells
      RECOMMEND-BACKUP   : in active subset; fallback if primary quality issues surface
      DEFER              : not in active subset (rationale recorded)

  Step 2 — Per (subcategory × variant) cell, the curation determines GREEN/YELLOW/RED:
      GREEN   : ≥1 commercial-license (or CC-0) pack in the recommended subset
      YELLOW  : covered only by CC-BY packs (attribution surface; CC-BY-SA flagged-and-deferred)
      RED     : no coverage in the recommended subset (acquisition shortlist target)

  Step 3 — Acquisition shortlist is derived from RECOMMENDED packs with non-zero cost.

Schema per row (matches dispatch § Item 2 schema-match elrond Pimen pattern):

    {
      "asset_id": "<legolas-asset-id>",       # carries through from legolas crawl
      "vendor": "...",
      "category": "floor-loot" | "ambient-prop" | "ui-icon",
      "subcategory": "potion" | "gold" | "gear-weapon" | "gear-armor" | "chest" | "coffin" | ...,
      "specific_type": "<as crawled>",
      "rarity_tier": null | "white,magic,rare,unique" | "star-bronze,...",
      "pixel_size": "<as crawled>",
      "attribution_class": "commercial-license" | "cc-by" | "cc-0" | "cc-by-nd" | "cc-by-sa",
      "pack_origin": "<as crawled>",
      "cost_usd": <float|null>,
      "encounter_compatibility": [...],       # always present (mostly broad for icons/props)
      "render_notes": "...",                  # downscale / upscale / frame-system hints
      "curation_status": "RECOMMEND-PRIMARY" | "RECOMMEND-BACKUP" | "DEFER",
      "curation_rationale": "...",
      "coverage_cells": [...],                # (subcategory, variant) cells this pack populates
      "size_register_fit": "EXACT" | "CLOSE" | "UPSCALE-REQUIRED" | "DOWNSCALE-REQUIRED",
      "spec_ref": "canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md § 3.3",
      "legolas_crawl_ref": "agentic_orchestration/research/catalogue/icons-and-props-2026-05-17/<file>.jsonl::<asset_id>",
      "vs2a_status": "active" | "deferred"
    }

Drax-consumption pattern (post-VS2a M5 panel redesigns + ambient prop dispatches):
    Filter rows where vs2a_status == "active" AND curation_status startswith "RECOMMEND".
    Group by `pack_origin` to determine acquisition list.
    Per row, use `coverage_cells` to wire pack contents into UI/world slot positions.
    Use `size_register_fit` + `render_notes` to drive scale-resolution decisions.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]
CRAWL_DIR = (
    REPO_ROOT
    / "agentic_orchestration"
    / "research"
    / "catalogue"
    / "icons-and-props-2026-05-17"
)
CURATED_DIR = REPO_ROOT / "agentic_orchestration" / "research" / "curated"

INPUTS = {
    "floor-loot": CRAWL_DIR / "floor-loot.jsonl",
    "ambient-props": CRAWL_DIR / "ambient-props.jsonl",
    "ui-icons": CRAWL_DIR / "ui-icons.jsonl",
}

OUTPUTS = {
    "floor-loot": CURATED_DIR / "floor-loot-subset-vs2a-2026-05-17.jsonl",
    "ambient-props": CURATED_DIR / "ambient-props-subset-vs2a-2026-05-17.jsonl",
    "ui-icons": CURATED_DIR / "ui-icons-subset-vs2a-2026-05-17.jsonl",
}


# -----------------------------------------------------------------------------
# Curation decisions (per legolas asset_id)
#
# Decision keys document, per asset_id:
#   - curation_status        : RECOMMEND-PRIMARY | RECOMMEND-BACKUP | DEFER
#   - curation_rationale     : short prose
#   - coverage_cells         : list of (subcategory, variant/state) tuples
#   - size_register_fit      : EXACT | CLOSE | UPSCALE-REQUIRED | DOWNSCALE-REQUIRED
#   - vs2a_status            : active | deferred
#
# Decisions encode the dispatch § Acceptance criteria:
#   - GREEN/YELLOW/RED matrix is derivable post-build from `coverage_cells` ×
#     `attribution_class` × `curation_status`.
#   - Acquisition shortlist is derivable from cost_usd > 0 AND curation_status
#     == RECOMMEND-PRIMARY rows.
# -----------------------------------------------------------------------------
# Post-acquisition update — 2026-05-17 (Matt L3 acquisition pass):
#   Matt acquired 7 packs ~00:30 EDT 2026-05-17 (dispatch
#   `2026-05-17-elrond-icon-and-prop-acquisition-registration.md`).
#   ACQUISITIONS dict below maps each acquired asset_id → relative path under
#   `reincarnated-demo/public/assets/` plus actual cost. curate_row stamps
#   `acquired_path`, `acquired_date`, and `acquired_cost_usd` fields on
#   matching rows so drax can consume the manifest directly without resolving
#   pack-origin → local-path manually.
# -----------------------------------------------------------------------------


ACQUISITIONS: dict[str, dict] = {
    # ─────────────────────────────────────────────────────────────────────
    # DireDungeon Items + Loot ($10 CC BY 4.0; DerNachbar)
    # Single bundle acquisition covers floor-loot AND ui-icons subsets.
    # PNG tileset + per-item folders + 10-color animated outline rarity
    # proxy + size-tier potion variants (healing/mana big/medium/small)
    # confirmed at acquisition. 214 base items × 10 outline colors × 2 modes
    # = 137,602 animated frames in animatedOutlines folder.
    # ─────────────────────────────────────────────────────────────────────
    "itch-direndachbar.floor-loot.gold.dire-dungeon-items-coins": {
        "acquired_path": "DireDungeon_Items_Loot/",
        "acquired_path_primary_asset": (
            "DireDungeon_Items_Loot/DireDungeonItemsTileset_by_DerNachbar (v1.0).png"
        ),
        "acquired_path_per_item_folder": (
            "DireDungeon_Items_Loot/DireDungeonItems_by_DerNachbar/"
        ),
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 10.00,
        "acquisition_notes": (
            "Shared acquisition with dire-dungeon weapon/armor/potions/UI rows. "
            "45 coin variants in 32x32 confirmed."
        ),
    },
    "itch-direndachbar.floor-loot.gear-weapon.dire-dungeon-weapons": {
        "acquired_path": (
            "DireDungeon_Items_Loot/DireDungeonItems_by_DerNachbar/melee_weapons/"
        ),
        "acquired_path_ranged": (
            "DireDungeon_Items_Loot/DireDungeonItems_by_DerNachbar/ranged_weapons/"
        ),
        "acquired_animated_outlines": (
            "DireDungeon_Items_Loot/DireDungeonItems_animatedOutlines_by_DerNachbar/melee_weapons/"
        ),
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,  # shared with dire-dungeon coins; bundle paid once
        "acquisition_notes": (
            "6 melee categories (axes/daggers/maces/polearms/staves/swords); "
            "9 sword variants × 10 outline colors × 32 frames in animated outlines."
        ),
    },
    "itch-direndachbar.floor-loot.gear-armor.dire-dungeon-armor": {
        "acquired_path_body": (
            "DireDungeon_Items_Loot/DireDungeonItems_by_DerNachbar/body/"
        ),
        "acquired_path_helmet": (
            "DireDungeon_Items_Loot/DireDungeonItems_by_DerNachbar/helmet/"
        ),
        "acquired_path_gloves": (
            "DireDungeon_Items_Loot/DireDungeonItems_by_DerNachbar/gloves/"
        ),
        "acquired_path_shoes": (
            "DireDungeon_Items_Loot/DireDungeonItems_by_DerNachbar/shoes/"
        ),
        "acquired_path_jewelry": (
            "DireDungeon_Items_Loot/DireDungeonItems_by_DerNachbar/jewelry/"
        ),
        "acquired_path_shields": (
            "DireDungeon_Items_Loot/DireDungeonItems_by_DerNachbar/shields/"
        ),
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,  # shared
        "acquisition_notes": (
            "body/helmet/gloves/shoes/jewelry/shields all present; belt slot still "
            "uncovered (per prior G-BELT non-load-bearing flag)."
        ),
    },
    "itch-direndachbar.ui-icon.gear-icon.dire-dungeon-items-all": {
        "acquired_path": "DireDungeon_Items_Loot/",
        "acquired_path_tileset": (
            "DireDungeon_Items_Loot/DireDungeonItemsTileset_by_DerNachbar (v1.0).png"
        ),
        "acquired_path_no_outlines": (
            "DireDungeon_Items_Loot/DireDungeonItemsTileset_noOutlines_by_DerNachbar (v1.0).png"
        ),
        "acquired_path_items_outlines": (
            "DireDungeon_Items_Loot/items_outlines/"
        ),
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,  # shared
        "acquisition_notes": (
            "Both outlined and outline-free spritesheets present + per-category "
            "subfolders for direct UI-icon ingest. items_outlines folder gives "
            "black-outline single-state variants suitable for UI rendering."
        ),
    },
    "itch-direndachbar.ui-icon.potion-icon.dire-dungeon-potions": {
        "acquired_path": (
            "DireDungeon_Items_Loot/DireDungeonItems_by_DerNachbar/potions/"
        ),
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,  # shared
        "acquisition_notes": (
            "16 potion variants confirmed including healing_big/medium/small + "
            "mana_big/medium/small — these are explicit fill-level/size-tier "
            "states. MATERIAL UPGRADE to G-FILL gap status (see selection doc)."
        ),
    },
    "itch-direndachbar.ui-icon.gold-icon.dire-dungeon-coins-gems": {
        "acquired_path_jewelry": (
            "DireDungeon_Items_Loot/DireDungeonItems_by_DerNachbar/jewelry/"
        ),
        "acquired_path_gems": (
            "DireDungeon_Items_Loot/DireDungeonItems_by_DerNachbar/gems/"
        ),
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,  # shared
        "acquisition_notes": "10 gem variants + jewelry confirmed.",
    },
    # ─────────────────────────────────────────────────────────────────────
    # Magic_Potions_Pack_V1 (FREE; substitute for SODA — vendor TBD)
    # 25 individual potion icons (5 colors × 5 shapes); no fill-level
    # variants, no buff/debuff/elemental labels. Functional substitute for
    # AquaSenshi + partial SODA coverage. Vendor metadata pending — flagged
    # for legolas to confirm provenance + license at future crawl.
    # ─────────────────────────────────────────────────────────────────────
    "itch-aquasenshi.floor-loot.potion.medieval-rpg-potions": {
        "acquired_path": "Magic_Potions_Pack_V1/",
        "acquired_path_individual_icons": "Magic_Potions_Pack_V1/Individual_Icons/",
        "acquired_path_spritesheet": "Magic_Potions_Pack_V1/Spritesheet.png",
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,
        "acquisition_notes": (
            "SUBSTITUTE acquisition: Matt acquired Magic_Potions_Pack_V1 (vendor "
            "TBD, free) in lieu of AquaSenshi-specific pack. 25 icons (5 colors × "
            "5 shapes: classic/heart/round/skull/square). No explicit "
            "health/mana/poison/energy/speed labels — vendor neutral; color-coded "
            "use mapping required at drax integration. Vendor + license metadata "
            "pending legolas verification."
        ),
    },
    "itch-aquasenshi.ui-icon.potion-icon.medieval-rpg-25": {
        "acquired_path": "Magic_Potions_Pack_V1/Individual_Icons/",
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,
        "acquisition_notes": (
            "SUBSTITUTE acquisition (same Magic_Potions_Pack_V1 as floor-loot). "
            "Vendor TBD, license pending legolas verification."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────
    # CraftPix Guild Hall (FREE; closes G-ARMOR-MANNEQUIN with damage states)
    # Pack 189780. Contains 3 attacked-mannequin spritesheets (4×4 frames
    # each — destruction animation) + Interior_objects.png with weapon
    # racks, banner stands, bookshelves, shield displays + Exterior.png +
    # citizen NPCs. The attacked-mannequin sheets provide MULTI-STATE armor
    # stand coverage — materially better than single-state expectation.
    # ─────────────────────────────────────────────────────────────────────
    "craftpix.ambient-prop.weapon-stand.guild-hall-free": {
        "acquired_path": "craftpix-net-189780-free-top-down-pixel-art-guild-hall-asset-pack/",
        "acquired_path_interior_objects": (
            "craftpix-net-189780-free-top-down-pixel-art-guild-hall-asset-pack/PNG/Interior_objects.png"
        ),
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,
        "acquisition_notes": (
            "Interior_objects.png contains weapon racks, banner stands, "
            "bookshelves with skill-tome filler, banner displays. Top-down register "
            "confirmed."
        ),
    },
    "craftpix.ambient-prop.armor-stand.guild-hall-mannequin": {
        "acquired_path_mannequin1": (
            "craftpix-net-189780-free-top-down-pixel-art-guild-hall-asset-pack/PNG/Attacked_Manequin1_with_shadow.png"
        ),
        "acquired_path_mannequin2": (
            "craftpix-net-189780-free-top-down-pixel-art-guild-hall-asset-pack/PNG/Attacked_Manequin2_with_shadow.png"
        ),
        "acquired_path_mannequin3": (
            "craftpix-net-189780-free-top-down-pixel-art-guild-hall-asset-pack/PNG/Attacked_Manequin3_with_shadow.png"
        ),
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,
        "acquisition_notes": (
            "MATERIAL UPGRADE on G-ARMOR-MANNEQUIN: 3 mannequin designs × 4-frame "
            "destruction animation each (with + without shadow variants). "
            "Multi-state armor stand coverage materially exceeds the single-state "
            "expectation in prior selection doc. Helmet/helmless variants are "
            "implicit in the destruction frame sequence (broken stand reveals "
            "what's underneath)."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────
    # CraftPix Basic Pixel Art UI for RPG (FREE; LOAD-BEARING)
    # Pack 255216. Provides inventory/equipment frames with rarity-coloured
    # gem inserts (blue/orange/red visible in Inventory.png + Equipment.png).
    # Equipment.png explicitly shows paper-doll character with helm + sword
    # + shield — armor-stand-equivalent affordance baked in.
    # ─────────────────────────────────────────────────────────────────────
    "craftpix.ui-icon.gear-icon.basic-pixel-art-ui-rpg": {
        "acquired_path": "craftpix-net-255216-free-basic-pixel-art-ui-for-rpg/",
        "acquired_path_inventory": (
            "craftpix-net-255216-free-basic-pixel-art-ui-for-rpg/PNG/Inventory.png"
        ),
        "acquired_path_equipment": (
            "craftpix-net-255216-free-basic-pixel-art-ui-for-rpg/PNG/Equipment.png"
        ),
        "acquired_path_icons": (
            "craftpix-net-255216-free-basic-pixel-art-ui-for-rpg/PNG/Icons.png"
        ),
        "acquired_path_shop": (
            "craftpix-net-255216-free-basic-pixel-art-ui-for-rpg/PNG/Shop.png"
        ),
        "acquired_path_craft": (
            "craftpix-net-255216-free-basic-pixel-art-ui-for-rpg/PNG/Craft.png"
        ),
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,
        "acquisition_notes": (
            "MATERIAL UPGRADE on G-RARITY: Inventory + Equipment screens contain "
            "rarity-coloured slot indicators (blue/orange/red gem inserts) visible "
            "in Inventory.png + Equipment.png — supports procedural rarity-border "
            "path with native pre-built slot frames. Equipment.png shows paper-doll "
            "with helm + sword + shield (armor-stand-equivalent UI panel)."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────
    # Seliel Treasure Chests 1 (19.07c, FREE) — closes Seliel-side chest row
    # 160×192px spritesheet visible: ~5 chest types × 6+ rows = open/closed
    # states × multiple color swaps.
    # ─────────────────────────────────────────────────────────────────────
    "seliel.ambient-prop.chest.mana-seed-treasure-chests": {
        "acquired_path": "19.07c - Treasure Chests 1/",
        "acquired_path_spritesheet": "19.07c - Treasure Chests 1/treasure chests.png",
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,
        "acquisition_notes": (
            "160×192px composite spritesheet (10 cols × 12 rows at 16px grid). "
            "5 chest types × open/closed × 3 color swaps visible. No coffin-style "
            "variant present — G-COFFIN remains OPEN."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────
    # Seliel Breakable Pots 1 (20.05b, FREE)
    # 128×128px composite + 4 color variant sheets (gray/red/white/yellow).
    # 4 pot designs × 3-frame breaking animation + 6 shard particles per
    # design.
    # ─────────────────────────────────────────────────────────────────────
    "seliel.ambient-prop.urn-vase-box.breakable-pots": {
        "acquired_path": "20.05b - Breakable Pots 1/",
        "acquired_path_composite": "20.05b - Breakable Pots 1/breakable pots.png",
        "acquired_path_gray": "20.05b - Breakable Pots 1/breakable pots (gray).png",
        "acquired_path_red": "20.05b - Breakable Pots 1/breakable pots (red).png",
        "acquired_path_white": "20.05b - Breakable Pots 1/breakable pots (white).png",
        "acquired_path_yellow": "20.05b - Breakable Pots 1/breakable pots (yellow).png",
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,
        "acquisition_notes": (
            "4 color variants (not 3 as legolas crawled — minor uplift). 3-frame "
            "breaking animation + shard particles per pot confirmed."
        ),
    },
    # ─────────────────────────────────────────────────────────────────────
    # Elthen Destructible Objects (FREE PWYW) — confirmed acquired
    # Sprite sheet placed at assets root (not in vendor folder).
    # ─────────────────────────────────────────────────────────────────────
    "itch-elthen.ambient-prop.urn-vase-box.destructible-objects": {
        "acquired_path_spritesheet": "Destructible Objects Sprite Sheet.png",
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,
        "acquisition_notes": (
            "Composite sprite sheet acquired at assets root. Contains barrels, "
            "crates, rocks/stones, signs, sign-posts with 3-state intact + "
            "destruction frames + shard particles per object."
        ),
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Non-shortlisted bonus acquisition: CraftPix Animated Magic Book
# (pack 809047, FREE). Not in the original 3-manifest selection but acquired
# alongside the others. Stored here as a registration footnote so the
# audit trail records what was acquired.
# ─────────────────────────────────────────────────────────────────────────────
BONUS_ACQUISITIONS: list[dict] = [
    {
        "pack_origin": "craftpix-net-809047-free-animated-magic-book",
        "acquired_path": "craftpix-net-809047-free-animated-magic-book-pixel-art-asset-pack/",
        "acquired_date": "2026-05-17",
        "acquired_cost_usd": 0.00,
        "acquisition_class": "bonus",
        "rationale": (
            "Not in prior PRIMARY/BACKUP shortlist; acquired bonus pack. "
            "Provides 12-frame animated magic-book open/close + per-element "
            "skill-icon set (fire/nature/water/lightning) with 8 frames per "
            "icon. Useful as UI lore/decoration asset or skill-icon backup. "
            "Logged for downstream drax visibility but does not modify the "
            "VS2a curation rollup."
        ),
        "coverage_cells_potential": [
            ("ui-decoration", "magic-book-animated"),
            ("ui-icon", "skill-element-fire"),
            ("ui-icon", "skill-element-nature"),
            ("ui-icon", "skill-element-water"),
            ("ui-icon", "skill-element-lightning"),
        ],
    }
]


# -----------------------------------------------------------------------------
# (CURATION dict below — pre-acquisition. Acquisitions are stamped onto rows
# at curate_row() time by joining ACQUISITIONS[asset_id] into the output.)
# -----------------------------------------------------------------------------


CURATION: dict[str, dict] = {
    # ─────────────────────────────────────────────────────────────────────
    # FLOOR LOOT — POTIONS
    # ─────────────────────────────────────────────────────────────────────
    "itch-aquasenshi.floor-loot.potion.medieval-rpg-potions": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "Free + health/mana explicitly typed + 32x32 native fits gandalf "
            "floor-loot ~35px target. Compact but type-clean (5 explicit types). "
            "Pairs with SODA below for breadth."
        ),
        "coverage_cells": [
            ("potion", "health"),
            ("potion", "mana"),
            ("potion", "poison"),
            ("potion", "energy"),
            ("potion", "speed"),
        ],
        "size_register_fit": "EXACT",
        "vs2a_status": "active",
    },
    "itch-soda.floor-loot.potion.150-stylized-potions": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "$3.25 for 150+ stylized potions. Health+mana explicitly confirmed + "
            "small/medium/large size variants serve as fill-level proxy + elemental "
            "subtypes for buff/debuff thematic variants. 32x32 EXACT to floor-loot "
            "target. Complements AquaSenshi free coverage with breadth."
        ),
        "coverage_cells": [
            ("potion", "health"),
            ("potion", "mana"),
            ("potion", "buff"),
            ("potion", "debuff"),
            ("potion", "elemental"),
            ("potion", "fill-level-proxy-size-tier"),
        ],
        "size_register_fit": "EXACT",
        "vs2a_status": "active",
    },
    "itch-bis.floor-loot.potion.potions-icons-pack-270": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "270 variants + EMPTY variants is the closest proxy for fill-level "
            "states surfaced in the crawl. CC BY-ND 4.0 prevents modification — "
            "license is acceptable but restricts derived-art work. Hold as backup "
            "in case SODA + AquaSenshi prove insufficient for fill-level needs."
        ),
        "coverage_cells": [
            ("potion", "empty-state-fill-proxy"),
        ],
        "size_register_fit": "EXACT",
        "vs2a_status": "active",
    },
    "craftpix.floor-loot.potion.craftpix-free-magic-potions": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "Free 96 icons; not type-labeled (shape/color differentiation only). "
            "Hold as visual-breadth backup. Same source also published as oga-48 "
            "under OGA-BY 3.0 — prefer the craftpix free distribution to avoid "
            "double-attribution surface."
        ),
        "coverage_cells": [
            ("potion", "visual-breadth-generic"),
        ],
        "size_register_fit": "EXACT",
        "vs2a_status": "active",
    },
    "craftpix.floor-loot.potion.craftpix-potion-icons-pack": {
        "curation_status": "DEFER",
        "curation_rationale": "Subsumed by SODA breadth. Reconsider only if SODA quality issues surface.",
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    "craftpix.floor-loot.potion.craftpix-potion-icons-pixel-art": {
        "curation_status": "DEFER",
        "curation_rationale": "Subsumed by SODA breadth.",
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    "craftpix.floor-loot.potion.craftpix-100-potion-icons": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed by SODA + Dire Dungeon. No marginal value.",
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    "craftpix.floor-loot.potion.craftpix-rpg-potions-pack": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; 64x64 oversize for floor target. Subsumed.",
        "coverage_cells": [],
        "size_register_fit": "DOWNSCALE-REQUIRED",
        "vs2a_status": "deferred",
    },
    "seliel.floor-loot.potion.alchemy-gear": {
        "curation_status": "DEFER",
        "curation_rationale": (
            "$12.99 — highest-cost potion pack; 16x16 native requires 2x upscale "
            "for floor-loot target. SODA + AquaSenshi + Bis cover the need at "
            "lower cost and EXACT register. Reconsider only for style-register "
            "coherence with Seliel chests if seliel chest is selected — but Mucho "
            "Pixels selected over Seliel for chest coverage, so this is moot."
        ),
        "coverage_cells": [],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "deferred",
    },
    "oga.floor-loot.potion.48-free-magic-potions": {
        "curation_status": "DEFER",
        "curation_rationale": (
            "OGA-BY 3.0 attribution surface; same source as craftpix free 48. "
            "Prefer craftpix distribution (no OGA-BY attribution). Defer to "
            "avoid double-attribution."
        ),
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    # ─────────────────────────────────────────────────────────────────────
    # FLOOR LOOT — GOLD
    # ─────────────────────────────────────────────────────────────────────
    "itch-direndachbar.floor-loot.gold.dire-dungeon-items-coins": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "Part of $10 Dire Dungeon Items bundle (single acquisition unlocks "
            "weapons + armor + potions + coins + gems). CC BY 4.0 attribution "
            "surface is acceptable per Pimen Gap-G4 Path B precedent. 45 coin "
            "variants in copper/silver/gold cover the floor-drop currency spread. "
            "32x32 EXACT to floor-loot target."
        ),
        "coverage_cells": [
            ("gold", "single-coin"),
            ("gold", "small-pile"),
            ("gold", "medium-pile"),
            ("gold", "large-pile"),
            ("gold", "copper-tier"),
            ("gold", "silver-tier"),
            ("gold", "gold-tier"),
        ],
        "size_register_fit": "EXACT",
        "vs2a_status": "active",
    },
    "oga.floor-loot.gold.gold-treasure-icons-16x16": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "CC0 (public domain) — zero attribution surface. 10 icons cover "
            "single/stacks 2/4/8/16 progression. 16x16 native requires 2-3x "
            "upscale to reach floor-loot target. Hold as CC-0 fallback if "
            "Dire Dungeon attribution becomes load-bearing for spec compliance."
        ),
        "coverage_cells": [
            ("gold", "stack-progression-1-2-4-8-16"),
        ],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "active",
    },
    "oga.floor-loot.gold.gold-treasure-icons-32x32": {
        "curation_status": "DEFER",
        "curation_rationale": (
            "CC-BY-SA 3.0 share-alike clause flagged in legolas summary § 4. "
            "Share-alike conflicts with proprietary commercial release. Strict "
            "defer per legolas recommendation."
        ),
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    "itch-pixel1992.floor-loot.gold.coin-piles-treasure-chests-64-32": {
        "curation_status": "DEFER",
        "curation_rationale": (
            "AI-ASSISTED flag triggers team AI-asset policy review. Dire Dungeon "
            "(no AI) + OGA 16x16 (no AI, CC0) cover the gold need without AI "
            "provenance concerns. Defer pending AI-policy clarification."
        ),
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    "itch-pixel1992.floor-loot.gold.rpg-loot-pack-gold-1200": {
        "curation_status": "DEFER",
        "curation_rationale": "AI-ASSISTED flag; sizing-mismatch (128x128 / 64x64 oversize); subsumed.",
        "coverage_cells": [],
        "size_register_fit": "DOWNSCALE-REQUIRED",
        "vs2a_status": "deferred",
    },
    "craftpix.floor-loot.gold.things-rpg-32x32": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed by Dire Dungeon + OGA CC-0 coverage.",
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    "craftpix.floor-loot.gold.treasure-currency-gems-loot": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed.",
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    "craftpix.floor-loot.gold.free-game-coins-spritesheets": {
        "curation_status": "DEFER",
        "curation_rationale": (
            "512x512 source — far oversize for ~35px floor-loot target. ~14x "
            "downscale would destroy detail. Animated spin not load-bearing for "
            "VS2a (static pickup acceptable). Defer."
        ),
        "coverage_cells": [],
        "size_register_fit": "DOWNSCALE-REQUIRED",
        "vs2a_status": "deferred",
    },
    # ─────────────────────────────────────────────────────────────────────
    # FLOOR LOOT — GEAR-WEAPON
    # ─────────────────────────────────────────────────────────────────────
    "itch-direndachbar.floor-loot.gear-weapon.dire-dungeon-weapons": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "Dire Dungeon Items ($10 CC BY 4.0 — single bundle). 54 melee + 19 "
            "ranged covers daggers/swords/axes/maces/polearms/staves/bows/"
            "crossbows/throwing. 10 colored outline variants serve as rarity "
            "differentiation proxy. No AI. 32x32 CLOSE to gandalf ~50px floor-gear "
            "target (1.5x upscale to register cleanly)."
        ),
        "coverage_cells": [
            ("gear-weapon", "dagger"),
            ("gear-weapon", "sword"),
            ("gear-weapon", "axe"),
            ("gear-weapon", "mace"),
            ("gear-weapon", "polearm"),
            ("gear-weapon", "staff"),
            ("gear-weapon", "bow"),
            ("gear-weapon", "crossbow"),
            ("gear-weapon", "throwing"),
            ("gear-weapon", "rarity-tier-outline-color-proxy"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "itch-vennril.floor-loot.gear-weapon.250-item-pack": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "$4.99 — provides 48x48 size variant (EXACT to ~50px gear-drop target) "
            "and adds wands (not in Dire Dungeon naming). Hold as scale-register "
            "alternative if Dire Dungeon 32x32 upscale shows quality issues at "
            "render-time."
        ),
        "coverage_cells": [
            ("gear-weapon", "wand"),
            ("gear-weapon", "size-register-48px-alternative"),
        ],
        "size_register_fit": "EXACT",
        "vs2a_status": "active",
    },
    "itch-akari21.floor-loot.gear-weapon.rpg-icon-pack-200": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "$3.00 — star-rarity system (bronze/silver/gold/purple stars) is the "
            "ONLY pack in crawl with explicit per-tier rarity differentiation. "
            "NOT the ARPG white/magic/rare/unique border system, but the closest "
            "available without custom authoring. Hold for VS2b rarity-pass if "
            "custom borders prove costly."
        ),
        "coverage_cells": [
            ("gear-weapon", "rarity-tier-star-system"),
            ("gear-weapon", "weapon-breadth-200"),
        ],
        "size_register_fit": "EXACT",
        "vs2a_status": "active",
    },
    "itch-shikashipx.floor-loot.gear-weapon.shikashi-fantasy-icons": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "Free 284 icons CC BY 4.0. Includes status-effect + buff icons not "
            "in Dire Dungeon. Attribution layer overlaps with Dire Dungeon (both "
            "CC BY) so no additional attribution surface. Useful breadth backup."
        ),
        "coverage_cells": [
            ("gear-weapon", "free-cc-by-breadth"),
        ],
        "size_register_fit": "EXACT",
        "vs2a_status": "active",
    },
    "itch-bigwander.floor-loot.gear-weapon.weapons-rack-128": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "Free (PWYW) 128 weapons. Originally rack-display assets but usable "
            "as floor drops. Mixed sizing 16x16-32x48 — variable register may "
            "cause integration noise but provides breadth at zero cost."
        ),
        "coverage_cells": [
            ("gear-weapon", "free-pwyw-breadth-128"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "itch-franuka.floor-loot.gear-weapon.rpg-icon-pack-500": {
        "curation_status": "DEFER",
        "curation_rationale": (
            "$4.99 + custom attribution required + 48x48 size matches UI-icon "
            "register (not floor-loot 50px). Subsumed by Dire Dungeon + Vennril. "
            "Reconsider for UI-icon subset (separate subcategory)."
        ),
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    "craftpix.floor-loot.gear-weapon.100-pixel-art-weapon-icons": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed by Dire Dungeon weapon coverage.",
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    "craftpix.floor-loot.gear-weapon.1000-rpg-icons-pack": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed.",
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    # ─────────────────────────────────────────────────────────────────────
    # FLOOR LOOT — GEAR-ARMOR
    # ─────────────────────────────────────────────────────────────────────
    "itch-direndachbar.floor-loot.gear-armor.dire-dungeon-armor": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "Dire Dungeon Items bundle covers armor too: 36 pieces "
            "(headpieces/body/gloves/boots) + 12 amulets + 12 rings + 9 shields. "
            "Belt slot NOT covered. 32x32 CLOSE to floor-armor ~55px target. "
            "Outline-color variants provide rarity-tier proxy."
        ),
        "coverage_cells": [
            ("gear-armor", "helm"),
            ("gear-armor", "chest"),
            ("gear-armor", "gloves"),
            ("gear-armor", "boots"),
            ("gear-armor", "amulet"),
            ("gear-armor", "ring"),
            ("gear-armor", "shield"),
            ("gear-armor", "rarity-tier-outline-color-proxy"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "itch-vennril.floor-loot.gear-armor.250-item-armor-subset": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "Armor subset of Vennril pack adds robe + cape + circlet (mage-"
            "register armor types not in Dire Dungeon plate/leather framing). "
            "Bundled with Vennril weapon backup acquisition — no extra cost."
        ),
        "coverage_cells": [
            ("gear-armor", "robe-mage-register"),
            ("gear-armor", "cape"),
            ("gear-armor", "circlet"),
        ],
        "size_register_fit": "EXACT",
        "vs2a_status": "active",
    },
    "craftpix.floor-loot.gear-armor.100-rpg-armor-icons": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed by Dire Dungeon armor coverage.",
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    # ─────────────────────────────────────────────────────────────────────
    # AMBIENT PROP — CHEST
    # ─────────────────────────────────────────────────────────────────────
    "itch-muchos.ambient-prop.chest.dungeon-tileset-pack-chests": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "$4.95 GameDev Market Pro Licence (royalty-free). Chest with "
            "locked/unlocked/opened states in BOTH gold AND silver variants — "
            "state-coverage is the dominant criterion for chest prop. Pack ALSO "
            "covers coffin + weapon-stand + pots in same purchase (best multi-"
            "prop pack found). 16x16 tile-grid base requires multi-tile composition "
            "to reach 110-130px chest target."
        ),
        "coverage_cells": [
            ("chest", "small-locked"),
            ("chest", "small-unlocked"),
            ("chest", "small-opened"),
            ("chest", "medium-locked"),
            ("chest", "medium-unlocked"),
            ("chest", "medium-opened"),
            ("chest", "rarity-tier-gold-silver-color-proxy"),
        ],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "active",
    },
    "seliel.ambient-prop.chest.mana-seed-treasure-chests": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "FREE. 5 chest designs x 3 color swaps = 15 variants. Open + closed "
            "states confirmed. 16-bit top-down style. 100% human-made no AI. "
            "Pairs with Mucho Pixels for visual-breadth — different style register "
            "(SNES-leaning) provides design alternative if Mucho's grid-tile feel "
            "is too modular for the final visual treatment."
        ),
        "coverage_cells": [
            ("chest", "free-style-register-snes"),
            ("chest", "color-swap-3-variants"),
        ],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "active",
    },
    "itch-pixelserial.ambient-prop.chest.free-rpg-chests-9-types": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "Free (PWYW). 9 unique designs + 4-frame open/close animation. "
            "Top-down confirmed. SIZING: 18x16 closed is small; 6-7x upscale "
            "for chest target. Hold as visual-breadth backup with animated-state "
            "for chest-opening events if Mucho + Seliel lack animation."
        ),
        "coverage_cells": [
            ("chest", "free-9-types-animated"),
        ],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "active",
    },
    "craftpix.ambient-prop.chest.free-2d-topdown-dungeon": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": "Free CraftPix asset pack; chests + animated water + traps. Useful supplementary breadth at zero cost.",
        "coverage_cells": [
            ("chest", "free-craftpix-supplementary"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "craftpix.ambient-prop.chest.free-dungeon-props": {
        "curation_status": "DEFER",
        "curation_rationale": "Free CraftPix; chests + gold piles. Subsumed by topdown-dungeon free pack + Mucho.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    "craftpix.ambient-prop.chest.topdown-dungeon-tileset": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed by Mucho Pixels paid pack + Seliel free.",
        "coverage_cells": [],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "deferred",
    },
    "itch-pixelexplosive.ambient-prop.chest.12-chest-opening-animations": {
        "curation_status": "DEFER",
        "curation_rationale": (
            "$2.00 for 12 opening-only animations (no closed/closing frames). "
            "Single-state coverage; Mucho + Pixel Serial cover full state cycle. Defer."
        ),
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    "itch-pixel1992.ambient-prop.chest.coin-piles-chests-60-variants": {
        "curation_status": "DEFER",
        "curation_rationale": "AI-ASSISTED flag. Static-only (no open animation). Subsumed.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    # ─────────────────────────────────────────────────────────────────────
    # AMBIENT PROP — COFFIN
    # ─────────────────────────────────────────────────────────────────────
    "itch-muchos.ambient-prop.coffin.dungeon-tileset-pack-coffin": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "Bundled into Mucho Pixels $4.95 pack (no marginal cost beyond chest "
            "selection). Stone coffin with explicit open state listed. The ONLY "
            "vendor with confirmed coffin open-state at the crawl scope. SPARSE "
            "GAP partially closed by this single coverer — legolas-flagged gap "
            "remains noted for Matt review."
        ),
        "coverage_cells": [
            ("coffin", "stone-closed"),
            ("coffin", "stone-open"),
        ],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "active",
    },
    "craftpix.ambient-prop.coffin.topdown-dungeon-tileset": {
        "curation_status": "DEFER",
        "curation_rationale": (
            "Premium membership; coffin present but open state NOT confirmed. "
            "Mucho coverage is cleaner. Defer."
        ),
        "coverage_cells": [],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "deferred",
    },
    # ─────────────────────────────────────────────────────────────────────
    # AMBIENT PROP — WEAPON-STAND
    # ─────────────────────────────────────────────────────────────────────
    "itch-muchos.ambient-prop.weapon-stand.dungeon-tileset-weapon-stand": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "Bundled in Mucho Pixels pack. Resizable stand + broken/damaged "
            "variant + 7 different weapons on stand — best detail level found. "
            "State coverage (intact + broken) primary requirement met."
        ),
        "coverage_cells": [
            ("weapon-stand", "intact-7-weapons"),
            ("weapon-stand", "broken-variant"),
        ],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "active",
    },
    "craftpix.ambient-prop.weapon-stand.guild-hall-free": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "FREE CraftPix top-down guild hall pack. Weapon rack + training "
            "mannequin in same pack — closes armor-stand mannequin gap "
            "simultaneously. Top-down register matches play surface."
        ),
        "coverage_cells": [
            ("weapon-stand", "free-topdown-rack"),
            ("armor-stand", "free-mannequin"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "craftpix.ambient-prop.weapon-stand.free-dungeon-objects": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": "FREE CraftPix dungeon objects — weapon racks (swords/shields/spears) confirmed.",
        "coverage_cells": [
            ("weapon-stand", "free-rack-supplementary"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "itch-bigwander.ambient-prop.weapon-stand.weapons-rack-display": {
        "curation_status": "DEFER",
        "curation_rationale": "Free but no state animations for rack itself. Subsumed by Mucho + CraftPix guild hall.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    "craftpix.ambient-prop.weapon-stand.training-arena-tileset": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    # ─────────────────────────────────────────────────────────────────────
    # AMBIENT PROP — ARMOR-STAND
    # ─────────────────────────────────────────────────────────────────────
    # (CraftPix guild hall handles armor-stand mannequin in shared row above)
    "craftpix.ambient-prop.armor-stand.guild-hall-mannequin": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "FREE. Training mannequin / armor stand confirmed. SPARSE GAP per "
            "legolas — helmless vs full variants not confirmed in any pack. "
            "Single-state mannequin from CraftPix is the best available; "
            "helmet/helmless variants flagged as POSSIBLE custom-authoring "
            "target or future commission."
        ),
        "coverage_cells": [
            ("armor-stand", "free-mannequin-single-state"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "craftpix.ambient-prop.armor-stand.free-dungeon-objects": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": "FREE. Iron armor pieces interpretable as armor-stand display items. Supplementary.",
        "coverage_cells": [
            ("armor-stand", "free-iron-pieces-display"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "itch-indie-vova.ambient-prop.armor-stand.dungeons-pixels-pack": {
        "curation_status": "DEFER",
        "curation_rationale": (
            "$5.99 — armor-stand-as-mannequin NOT explicitly listed (shields/banners/closets "
            "only). Subsumed by CraftPix guild hall mannequin coverage."
        ),
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    # ─────────────────────────────────────────────────────────────────────
    # AMBIENT PROP — URN/VASE/BOX
    # ─────────────────────────────────────────────────────────────────────
    "itch-muchos.ambient-prop.urn-vase-box.dungeon-tileset-pots-barrels": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "Mucho Pixels pack covers 4 pot types (blue+red) with broken states "
            "+ 2 barrel types with broken states. Intact + destroyed state pair "
            "is the primary requirement for destructible prop; Mucho meets it "
            "for both pots AND barrels."
        ),
        "coverage_cells": [
            ("urn-vase-box", "pot-intact"),
            ("urn-vase-box", "pot-broken"),
            ("urn-vase-box", "barrel-intact"),
            ("urn-vase-box", "barrel-broken"),
        ],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "active",
    },
    "itch-elthen.ambient-prop.urn-vase-box.destructible-objects": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "FREE (PWYW). 6 destructible objects: crate, barrel, two signs, pot, "
            "chest. EXPLICIT damage + destroy animation per object. License: "
            "Creative Commons NC with commercial use explicitly OK per author "
            "(team should verify this against current page text at acquisition "
            "time). Animated destruction is uniquely valuable here."
        ),
        "coverage_cells": [
            ("urn-vase-box", "crate-intact-animated"),
            ("urn-vase-box", "crate-destroyed-animated"),
            ("urn-vase-box", "barrel-animated-destruction"),
            ("urn-vase-box", "pot-animated-destruction"),
            ("urn-vase-box", "sign-prop"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "seliel.ambient-prop.urn-vase-box.breakable-pots": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "FREE Mana Seed pack. 3 pot designs x 4 colors. 3-frame breaking "
            "animation + 6 small shard particles for destruction effect. "
            "100% human-made no AI. Shard-particle inclusion is a meaningful "
            "addition over Mucho's static broken-state — adds VFX-tier polish "
            "to the break event."
        ),
        "coverage_cells": [
            ("urn-vase-box", "pot-3-designs-4-colors"),
            ("urn-vase-box", "pot-3-frame-breaking-animation"),
            ("urn-vase-box", "pot-shard-particles"),
        ],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "active",
    },
    "craftpix.ambient-prop.urn-vase-box.free-dungeon-props": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": "FREE CraftPix. Barrels + crates + workbenches breadth supplement.",
        "coverage_cells": [
            ("urn-vase-box", "free-craftpix-barrel-crate"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "craftpix.ambient-prop.urn-vase-box.free-dungeon-objects": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": "FREE CraftPix. Barrels + jugs/vase (vase explicitly listed here).",
        "coverage_cells": [
            ("urn-vase-box", "free-craftpix-vase-jug"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "itch-indie-vova.ambient-prop.urn-vase-box.dungeons-pixels-barrels-crates": {
        "curation_status": "DEFER",
        "curation_rationale": "$5.99 — no broken-state animation. Subsumed by Mucho + Elthen + Seliel state coverage.",
        "coverage_cells": [],
        "size_register_fit": "EXACT",
        "vs2a_status": "deferred",
    },
    "itch-anokolisa.ambient-prop.urn-vase-box.dungeon-crawler-pack": {
        "curation_status": "DEFER",
        "curation_rationale": "FREE but specific urn/vase/barrel inventory not confirmed; broader pack unfocused. Subsumed.",
        "coverage_cells": [],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "deferred",
    },
    # ─────────────────────────────────────────────────────────────────────
    # UI ICON — GEAR-ICON
    # ─────────────────────────────────────────────────────────────────────
    "itch-direndachbar.ui-icon.gear-icon.dire-dungeon-items-all": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "Same Dire Dungeon $10 CC BY 4.0 acquisition used for floor-loot. "
            "259 items single-source UI coverage: weapons 54 + ranged 19 + "
            "shields 9 + armor 36 + amulets 12 + rings 12 + potions 16 + coins "
            "45 + gems 10 + scrolls 10 + spell books 10. Outline-color variants "
            "act as visual rarity differentiation. 32x32 native + frame/slot "
            "system at 3-4x = 96-128px CLOSE to gandalf 110-125px UI target."
        ),
        "coverage_cells": [
            ("gear-icon", "weapon-comprehensive"),
            ("gear-icon", "armor-comprehensive"),
            ("gear-icon", "amulet"),
            ("gear-icon", "ring"),
            ("gear-icon", "shield"),
            ("gear-icon", "scroll"),
            ("gear-icon", "spellbook"),
            ("gear-icon", "gem"),
            ("gear-icon", "rarity-outline-color-proxy"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "craftpix.ui-icon.gear-icon.basic-pixel-art-ui-rpg": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "FREE CraftPix Basic UI for RPG pack — provides the FRAME/SLOT "
            "INFRASTRUCTURE that bridges 32x32 native icons to 110-125px UI "
            "target. Includes inventory windows, equipment slots, HP/mana bars, "
            "XP meter, quick-slot bar, settings/shop/crafting screens. "
            "LOAD-BEARING for the size-register bridge per legolas summary § 3."
        ),
        "coverage_cells": [
            ("ui-frame", "inventory-slot-frame"),
            ("ui-frame", "equipment-slot-frame"),
            ("ui-frame", "hp-mana-bars"),
            ("ui-frame", "quick-slot-bar"),
            ("ui-frame", "shop-crafting-screens"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "itch-shikashipx.ui-icon.gear-icon.shikashi-fantasy-icons-ui": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "FREE 284 icons CC BY 4.0. Status-effect + buff icons not present in "
            "Dire Dungeon — useful for buff-bar UI authoring. RPG Maker MV/MZ "
            "spritesheet format is a structural mismatch with our pipeline; will "
            "require unpacking. Attribution layer overlaps with Dire Dungeon."
        ),
        "coverage_cells": [
            ("gear-icon", "status-effect-buff-icons"),
            ("gear-icon", "general-items-64"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "itch-akari21.ui-icon.gear-icon.rpg-icon-pack-200-ui": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "$3.00 — star-rarity UI variant of the floor-loot Akari21 pack. "
            "Hold for VS2b rarity-pass alongside floor-loot Akari21 selection."
        ),
        "coverage_cells": [
            ("gear-icon", "rarity-tier-star-system-ui"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "itch-franuka.ui-icon.gear-icon.rpg-icon-pack-500-ui": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "$4.99 — 48x48 size variant is closest native to gandalf 110-125px "
            "UI target (at 2x upscale). Custom attribution required. Hold as "
            "scale-register alternative if 32x32 + frame-system feel too compact."
        ),
        "coverage_cells": [
            ("gear-icon", "48px-native-scale-alternative"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "craftpix.ui-icon.gear-icon.1000-rpg-icons-pack": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed by Dire Dungeon 259-item coverage.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    "craftpix.ui-icon.gear-icon.100-weapon-icons": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    "craftpix.ui-icon.gear-icon.100-armor-icons": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    "craftpix.ui-icon.gear-icon.armor-weapons-pixel-rpg-icons": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    "craftpix.ui-icon.gear-icon.fantasy-32x32-collection": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership bundle; subsumed.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    # ─────────────────────────────────────────────────────────────────────
    # UI ICON — POTION-ICON
    # ─────────────────────────────────────────────────────────────────────
    "itch-aquasenshi.ui-icon.potion-icon.medieval-rpg-25": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "FREE. 25 icons; health+mana explicitly confirmed. Compact set for "
            "direct UI hotbar health/mana display + standard buff/debuff "
            "indicators. Pairs with SODA breadth for additional types."
        ),
        "coverage_cells": [
            ("potion-icon", "health-typed"),
            ("potion-icon", "mana-typed"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "itch-soda.ui-icon.potion-icon.150-stylized-potions-ui": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "$3.25 — same SODA pack used for floor-loot (single acquisition "
            "serves both subsets). 150 stylized UI icons + size variants serve "
            "as fill-level proxy in UI inventory display."
        ),
        "coverage_cells": [
            ("potion-icon", "stylized-150-breadth"),
            ("potion-icon", "buff-debuff-ui"),
            ("potion-icon", "elemental-ui"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "itch-direndachbar.ui-icon.potion-icon.dire-dungeon-potions": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "16 potion icons inside the Dire Dungeon $10 bundle (no marginal "
            "cost beyond gear-icon acquisition). Outline-color rarity variants "
            "provide UI-tier consistency with gear icons (single style register)."
        ),
        "coverage_cells": [
            ("potion-icon", "dire-dungeon-style-register-16"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "itch-bis.ui-icon.potion-icon.potions-icons-270-ui": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "$7.00 — 270 icons + empty variants serve as definitive fill-level "
            "UI states if needed. CC BY-ND 4.0 (no derivatives) limits "
            "modification. Hold for fill-level UI design pass."
        ),
        "coverage_cells": [
            ("potion-icon", "empty-state-ui-fill-proxy"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "craftpix.ui-icon.potion-icon.free-magic-potions-ui": {
        "curation_status": "DEFER",
        "curation_rationale": "Free; subsumed by AquaSenshi + SODA UI coverage.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    "craftpix.ui-icon.potion-icon.potion-icons-pack-48": {
        "curation_status": "DEFER",
        "curation_rationale": "$5.50 — subsumed by SODA + AquaSenshi.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    "craftpix.ui-icon.potion-icon.100-potion-icons": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    "craftpix.ui-icon.potion-icon.rpg-potions-160": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    "itch-seliel.ui-icon.potion-icon.alchemy-gear-416": {
        "curation_status": "DEFER",
        "curation_rationale": "$12.99 high-cost; 16x16 native requires heavy upscale. Subsumed.",
        "coverage_cells": [],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "deferred",
    },
    # ─────────────────────────────────────────────────────────────────────
    # UI ICON — GOLD-ICON
    # ─────────────────────────────────────────────────────────────────────
    "itch-direndachbar.ui-icon.gold-icon.dire-dungeon-coins-gems": {
        "curation_status": "RECOMMEND-PRIMARY",
        "curation_rationale": (
            "Same Dire Dungeon bundle. 45 coin/pile variants + 10 gemstones "
            "with style-register coherence to gear-icon + potion-icon. Single "
            "acquisition unifies UI visual register across all three subsets."
        ),
        "coverage_cells": [
            ("gold-icon", "coin-pile-45-variants"),
            ("gold-icon", "gem-10-variants"),
            ("gold-icon", "outline-color-rarity-proxy"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "craftpix.ui-icon.gold-icon.free-40-loot-icons": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": "FREE 40-icon loot pack — simple pile-of-coins + misc loot. Supplementary.",
        "coverage_cells": [
            ("gold-icon", "free-pile-of-coins-simple"),
        ],
        "size_register_fit": "CLOSE",
        "vs2a_status": "active",
    },
    "oga.ui-icon.gold-icon.gold-treasure-16x16": {
        "curation_status": "RECOMMEND-BACKUP",
        "curation_rationale": (
            "CC0 — same Bonsaiheldin 16x16 pack used for floor-loot. Stack "
            "progression 1/2/4/8/16/32/64/128/256/512 useful for loot-amount UI "
            "tier visualization. Zero attribution surface."
        ),
        "coverage_cells": [
            ("gold-icon", "stack-progression-tier-visualization"),
        ],
        "size_register_fit": "UPSCALE-REQUIRED",
        "vs2a_status": "active",
    },
    "craftpix.ui-icon.gold-icon.treasure-currency-gems-loot": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    "craftpix.ui-icon.gold-icon.treasure-32x32-objects-icons": {
        "curation_status": "DEFER",
        "curation_rationale": "Premium membership; subsumed.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
    "oga.ui-icon.gold-icon.gold-treasure-32x32": {
        "curation_status": "DEFER",
        "curation_rationale": "CC-BY-SA 3.0 share-alike flagged — strict defer per legolas summary recommendation.",
        "coverage_cells": [],
        "size_register_fit": "CLOSE",
        "vs2a_status": "deferred",
    },
}


# -----------------------------------------------------------------------------
# Build helpers
# -----------------------------------------------------------------------------


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def curate_row(raw: dict) -> dict | None:
    asset_id = raw["asset_id"]
    if asset_id not in CURATION:
        raise KeyError(f"Missing curation decision for {asset_id}")
    decision = CURATION[asset_id]

    # Build encounter_compatibility — icons/props are broadly applicable
    # across all combat encounter types unless flagged otherwise.
    encounter_compatibility = [
        "trash",
        "magic",
        "pack",
        "elite",
        "mini-boss",
        "boss",
    ]

    # render_notes carries through from legolas crawl + adds size-register
    # bridging hint.
    raw_notes = raw.get("notes", "")
    size_register = decision["size_register_fit"]

    render_notes_pieces = [f"size_register_fit={size_register}"]
    if "SIZING" in raw_notes or "Sizing" in raw_notes:
        # Carry through sizing flag from raw
        for piece in raw_notes.split("."):
            piece = piece.strip()
            if piece.startswith(("SIZING", "Sizing")):
                render_notes_pieces.append(piece)
    if "FRAME" in raw_notes or "frame" in raw_notes.lower():
        render_notes_pieces.append("frame-slot-system-eligible")
    render_notes = " | ".join(render_notes_pieces)

    row = {
        "asset_id": asset_id,
        "vendor": raw["vendor"],
        "category": raw["category"],
        "subcategory": raw["subcategory"],
        "specific_type": raw["specific_type"],
        "rarity_tier": raw.get("rarity_tier"),
        "pixel_size": raw["pixel_size"],
        "attribution_class": raw["attribution_class"],
        "pack_origin": raw["pack_origin"],
        "cost_usd": raw.get("cost_usd"),
        "encounter_compatibility": encounter_compatibility,
        "render_notes": render_notes,
        "curation_status": decision["curation_status"],
        "curation_rationale": decision["curation_rationale"],
        "coverage_cells": decision["coverage_cells"],
        "size_register_fit": decision["size_register_fit"],
        "spec_ref": "canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md § 3.3",
        "legolas_crawl_ref": (
            f"agentic_orchestration/research/catalogue/icons-and-props-2026-05-17/"
            f"{raw['category']}.jsonl::{asset_id}"
        ),
        "vs2a_status": decision["vs2a_status"],
    }

    # Stamp acquisition fields if this asset_id was acquired by Matt
    # (registration pass 2026-05-17).
    if asset_id in ACQUISITIONS:
        acq = ACQUISITIONS[asset_id]
        # acquisition_status surfaces this row as drax-consumable directly.
        row["acquisition_status"] = "ACQUIRED"
        # Promote all acquired_path_* keys to the row top-level so drax can
        # iterate them without nested lookup.
        for k, v in acq.items():
            row[k] = v
    else:
        row["acquisition_status"] = "NOT-ACQUIRED"

    return row


def build_subset(name: str, src: Path, dst: Path) -> dict:
    raw_rows = load_jsonl(src)
    curated = [curate_row(r) for r in raw_rows]

    # Header row — manifest metadata
    attribution_classes = sorted({r["attribution_class"] for r in curated})
    subcategories = sorted({r["subcategory"] for r in curated})
    statuses = {
        "RECOMMEND-PRIMARY": 0,
        "RECOMMEND-BACKUP": 0,
        "DEFER": 0,
    }
    for r in curated:
        statuses[r["curation_status"]] += 1

    active_packs = sorted(
        {
            r["pack_origin"]
            for r in curated
            if r["vs2a_status"] == "active"
            and r["curation_status"] == "RECOMMEND-PRIMARY"
        }
    )
    backup_packs = sorted(
        {
            r["pack_origin"]
            for r in curated
            if r["vs2a_status"] == "active"
            and r["curation_status"] == "RECOMMEND-BACKUP"
        }
    )

    acquisition_cost_estimate = 0.0
    seen_packs = set()
    for r in curated:
        if (
            r["curation_status"] == "RECOMMEND-PRIMARY"
            and r["pack_origin"] not in seen_packs
            and r.get("cost_usd")
        ):
            acquisition_cost_estimate += float(r["cost_usd"])
            seen_packs.add(r["pack_origin"])

    # Actual acquisition cost rollup (de-duplicated by pack_origin).
    # ACQUIRED rows record acquired_cost_usd per occurrence; sum once per
    # pack_origin where the first occurrence carries the canonical cost.
    actual_cost = 0.0
    acquired_packs_seen_cost: dict[str, float] = {}
    for r in curated:
        if r.get("acquisition_status") != "ACQUIRED":
            continue
        po = r["pack_origin"]
        ac = float(r.get("acquired_cost_usd", 0.0) or 0.0)
        if po not in acquired_packs_seen_cost:
            acquired_packs_seen_cost[po] = ac
            actual_cost += ac

    acquired_pack_origins = sorted(acquired_packs_seen_cost.keys())
    primary_packs_not_acquired = sorted(
        set(active_packs) - set(acquired_pack_origins)
    )

    header = {
        "_manifest_kind": f"{name}-subset-vs2a",
        "_manifest_version": "1.1",  # bumped: adds acquisition_status fields
        "_generated_at": datetime.now(timezone.utc).isoformat(),
        "_generated_by": "elrond+build_icons_and_props_subset_vs2a_2026_05_17.py",
        "_dispatch_ref": (
            "agentic_orchestration/dispatches/"
            "2026-05-17-elrond-icon-and-prop-acquisition-registration.md"
        ),
        "_predecessor_dispatch_ref": (
            "agentic_orchestration/dispatches/"
            "2026-05-17-elrond-icon-and-prop-curation-queued.md"
        ),
        "_legolas_crawl_ref": str(src.relative_to(REPO_ROOT)),
        "_spec_ref": "canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md",
        "_row_count": len(curated),
        "_distinct_pack_count": len({r["pack_origin"] for r in curated}),
        "_curation_status_counts": statuses,
        "_active_primary_pack_origins": active_packs,
        "_active_backup_pack_origins": backup_packs,
        "_acquisition_cost_usd_primary_only_estimate": round(acquisition_cost_estimate, 2),
        "_acquisition_cost_usd_actual_this_subset": round(actual_cost, 2),
        "_acquired_pack_origins": acquired_pack_origins,
        "_primary_packs_not_acquired": primary_packs_not_acquired,
        "_attribution_classes": attribution_classes,
        "_subcategories": subcategories,
    }

    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8") as fh:
        fh.write(json.dumps(header, sort_keys=False) + "\n")
        for r in curated:
            fh.write(json.dumps(r, sort_keys=False) + "\n")

    return header


def main() -> None:
    summary = {}
    for name in ("floor-loot", "ambient-props", "ui-icons"):
        header = build_subset(name, INPUTS[name], OUTPUTS[name])
        summary[name] = header
        print(f"[{name}] wrote {OUTPUTS[name]}")
        print(f"   rows: {header['_row_count']}")
        print(f"   primary packs: {len(header['_active_primary_pack_origins'])}")
        print(f"   backup packs: {len(header['_active_backup_pack_origins'])}")
        print(
            "   acquisition cost ESTIMATE (PRIMARY only): "
            f"${header['_acquisition_cost_usd_primary_only_estimate']:.2f}"
        )
        print(
            "   acquisition cost ACTUAL (this subset): "
            f"${header['_acquisition_cost_usd_actual_this_subset']:.2f}"
        )
        print(
            f"   acquired packs in this subset: "
            f"{len(header['_acquired_pack_origins'])}"
        )
        if header["_primary_packs_not_acquired"]:
            print(
                f"   primary packs not acquired: "
                f"{header['_primary_packs_not_acquired']}"
            )

    # Cross-subset de-duplicated rollups
    grand_primary_packs: set[str] = set()
    grand_acquired_packs: set[str] = set()
    grand_actual_cost_by_pack: dict[str, float] = {}
    grand_not_acquired: set[str] = set()
    for header in summary.values():
        for pack in header["_active_primary_pack_origins"]:
            grand_primary_packs.add(pack)
        for pack in header["_acquired_pack_origins"]:
            grand_acquired_packs.add(pack)
        for pack in header["_primary_packs_not_acquired"]:
            grand_not_acquired.add(pack)

    # Sum actual cost once per acquired pack across all rows in all subsets
    for name in ("floor-loot", "ambient-props", "ui-icons"):
        with OUTPUTS[name].open("r", encoding="utf-8") as fh:
            for i, line in enumerate(fh):
                if i == 0:
                    continue
                r = json.loads(line)
                if r.get("acquisition_status") != "ACQUIRED":
                    continue
                po = r["pack_origin"]
                ac = float(r.get("acquired_cost_usd", 0.0) or 0.0)
                if po not in grand_actual_cost_by_pack:
                    grand_actual_cost_by_pack[po] = ac

    grand_actual_cost = sum(grand_actual_cost_by_pack.values())

    # Estimate cost rollup (de-duplicated)
    grand_est_cost_by_pack: dict[str, float] = {}
    for name in ("floor-loot", "ambient-props", "ui-icons"):
        with OUTPUTS[name].open("r", encoding="utf-8") as fh:
            for i, line in enumerate(fh):
                if i == 0:
                    continue
                r = json.loads(line)
                if r["curation_status"] != "RECOMMEND-PRIMARY":
                    continue
                po = r["pack_origin"]
                cost = r.get("cost_usd")
                if cost and po not in grand_est_cost_by_pack:
                    grand_est_cost_by_pack[po] = float(cost)

    grand_est_cost = sum(grand_est_cost_by_pack.values())

    print(
        f"\n── Cross-subset rollup ──────────────────────────────────────"
    )
    print(f"Distinct PRIMARY packs across all subsets: {len(grand_primary_packs)}")
    print(f"Distinct ACQUIRED packs across all subsets: {len(grand_acquired_packs)}")
    print(f"De-duplicated ESTIMATE cost (PRIMARY): ${grand_est_cost:.2f}")
    print(f"De-duplicated ACTUAL outlay (ACQUIRED): ${grand_actual_cost:.2f}")
    print(f"Cost savings vs estimate: ${grand_est_cost - grand_actual_cost:.2f}")
    print(f"PRIMARY packs not acquired: {sorted(grand_not_acquired)}")
    print(
        f"\nBONUS acquisitions (outside shortlist): "
        f"{[b['pack_origin'] for b in BONUS_ACQUISITIONS]}"
    )


if __name__ == "__main__":
    main()
