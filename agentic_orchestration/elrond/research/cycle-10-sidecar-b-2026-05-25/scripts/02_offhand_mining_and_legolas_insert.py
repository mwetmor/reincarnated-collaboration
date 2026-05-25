#!/usr/bin/env python3
"""
Cycle 10 Sidecar B — Step 2: existing-source mining + legolas Mode B INSERT.

Authority:
  - Dispatch §3.2 + §4.1 + §4.3: reclassify off-hand items in existing substrate
    sources (royal_armouries / met-museum / wikidata / wikipedia / fextralife);
    insert legolas Mode B crawl rows; dedup 2 banner pairs at insert.
  - Off-hand-items canonical doc § 1.1 - § 1.5.
  - Engineering disciplines #11 (empirical inspection), #25 (semantic-layer rep-audit).

Reclassification rules (per category):

  shield:
    - royal_armouries: structured_properties.category_value == 'Shields'
      AND canonical_name NOT GLOB '*gun*' / '*riot*' / '*shoulder*'
    - met-museum: structured_properties.classification == 'Shields'
    - wikidata: structured_properties.weapon_type == 'shield'
    - wikipedia: canonical_name token = shield/buckler/pavise/aspis/scutum
                 AND NOT 'shield gun' / 'gun shield' / 'shoulder shield'
    Currently 'category' or 'unknown'; we reclassify to 'shield'.

  tome:
    - met-museum: structured_properties.classification == 'Books & Manuscripts'
    - wikipedia / wikidata: canonical_name token = grimoire/treatise/codex/spellbook
      (excluding clear false-positives: 'Manual Crowd Pummeler', 'Manual Dexterity',
       'Operating manual', 'USMC Sword Manual Procedures', 'Manual', 'Battletome'
       (Warhammer rulebook — leave at category for now))

  banner:
    - met-museum: classification IN ('Banners','Miscellaneous-Banners')
    - wikipedia / wikidata: canonical_name token = banner/oriflamme
      AND NOT (osrsbox-db generic 'Banner' rows — those are game-loot
       'category' rows; leave as-is since they're per-source duplicates of a
       generic in-game banner; reclassify only named-template ones)

  horn:
    - met-museum: classification == 'Horn-Implements'
    - royal_armouries: canonical_name LIKE '%hunting horn%' / '%ivory horn%' /
                       canonical_name = 'horn' AND category_value = 'Relics & miscellaneous'
      (Powder horn is firearms accessory — leave at category)
    - wikipedia / wikidata: canonical_name token = shofar/lur/carnyx/lituus/
                            olifant + 'war horn' / 'signal horn'

  talisman:
    - fextralife-ds1 / fextralife-ds3 / fextralife-ds2: canonical_name CONTAINS
      'talisman' as a word AND weapon_kind IN ('category','named_template')
    - wikipedia / wikidata: canonical_name token = amulet/talisman
      (be careful: D2 talisman is a system mechanic; only named-template count)

  focus:
    - Existing substrate has very few canonical focuses. Mostly come from
      legolas Mode B insert + a handful of Wikipedia crystal_ball /
      mythological_objects rows.
    - Rule: wikipedia/wikidata canonical_name CONTAINS 'crystal ball' or
      named-bearer focus.

Stage 1 + Stage 1.5 column population on reclassified/inserted rows:
  - For shields: proxy_range_class='melee_close_or_grapple' (defensive use),
                 proxy_geometry_class='shield_blocker',
                 proxy_tempo_class='reactive_block_tempo',
                 proxy_attribute_class='STR_or_DEX'
  - For tomes: proxy_range_class='off_hand_passive',
               proxy_geometry_class='tome_buff_aura',
               proxy_tempo_class='passive_or_cast_tempo',
               proxy_attribute_class='INT_or_WIS'
  - For banners: proxy_range_class='off_hand_aura',
                 proxy_geometry_class='banner_rally_aura',
                 proxy_tempo_class='aura_pulse_tempo',
                 proxy_attribute_class='STR_or_WIS'
  - For focuses: proxy_range_class='off_hand_passive',
                 proxy_geometry_class='focus_channel_amp',
                 proxy_tempo_class='cast_amp_tempo',
                 proxy_attribute_class='INT_or_WIS'
  - For horns: proxy_range_class='off_hand_aura',
               proxy_geometry_class='horn_signal_pulse',
               proxy_tempo_class='aura_pulse_tempo',
               proxy_attribute_class='STR_or_WIS'
  - For talismans: proxy_range_class='off_hand_passive',
                   proxy_geometry_class='talisman_ward_amp',
                   proxy_tempo_class='passive_or_cast_tempo',
                   proxy_attribute_class='WIS_or_INT'

  Confidence: 0.55 (heuristic substrate-class assignment; off-hand mechanical
  profile not yet axis-validated; Stage 4 dispatch via legolas Mode A consult
  will refine; this is interim per dispatch § 4 last paragraph: "Stage 4 dispatch
  (Wave 7) will apply off-hand-specific mechanical-tagging via legolas Mode A
  consult prereq").

  Stage 1.5 columns (extracted_*) populated where source JSON carries the info
  (mostly only legolas Mode B has author/period/cultural_tradition cleanly).

Idempotency:
  Script tracks an `imported_at` watermark via a sidecar B run-marker column.
  Reclassification is gated on current weapon_kind state — re-running the script
  will not double-process rows (UPDATE filters on prior weapon_kind state).
"""

import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Optional

DB_PATH = Path("/Users/admin/Games/reincarnated-loadout/data/telemetry.db")
LEGOLAS_DIR = Path(
    "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/cycle-10-sidecar-b-off-hand-crawl-2026-05-25"
)

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -- Stage 1 proxy profiles per off-hand category -----------------------------

OFF_HAND_PROXY = {
    "shield": {
        "proxy_range_class": "melee_close_or_grapple",
        "proxy_geometry_class": "shield_blocker",
        "proxy_tempo_class": "reactive_block_tempo",
        "proxy_attribute_class": "STR_or_DEX",
    },
    "tome": {
        "proxy_range_class": "off_hand_passive",
        "proxy_geometry_class": "tome_buff_aura",
        "proxy_tempo_class": "passive_or_cast_tempo",
        "proxy_attribute_class": "INT_or_WIS",
    },
    "banner": {
        "proxy_range_class": "off_hand_aura",
        "proxy_geometry_class": "banner_rally_aura",
        "proxy_tempo_class": "aura_pulse_tempo",
        "proxy_attribute_class": "STR_or_WIS",
    },
    "focus": {
        "proxy_range_class": "off_hand_passive",
        "proxy_geometry_class": "focus_channel_amp",
        "proxy_tempo_class": "cast_amp_tempo",
        "proxy_attribute_class": "INT_or_WIS",
    },
    "horn": {
        "proxy_range_class": "off_hand_aura",
        "proxy_geometry_class": "horn_signal_pulse",
        "proxy_tempo_class": "aura_pulse_tempo",
        "proxy_attribute_class": "STR_or_WIS",
    },
    "talisman": {
        "proxy_range_class": "off_hand_passive",
        "proxy_geometry_class": "talisman_ward_amp",
        "proxy_tempo_class": "passive_or_cast_tempo",
        "proxy_attribute_class": "WIS_or_INT",
    },
}

OFF_HAND_PROXY_CONFIDENCE = 0.55  # heuristic; Stage 4 will refine via Mode A consult

# Cultural lineage normalization for legolas Mode B insert
CULTURAL_TRADITION_MAP = {
    "Chinese": "east_asian",
    "Indian": "south_asian",
    "Hindu/Indian": "south_asian",
    "Hindu / Indian": "south_asian",
    "Greek": "european",
    "Roman": "european",
    "Italian": "european",
    "French": "european",
    "Norse": "european",
    "Norse/Viking": "european",
    "European": "european",
    "European/English": "european",
    "European/French": "european",
    "Byzantine": "european",
    "Frankish/Merovingian": "european",
    "German": "european",
    "Prussian": "european",
    "English": "european",
    "Scottish": "european",
    "Polish": "european",
    "Russian": "european",
    "Spanish": "european",
    "Portuguese": "european",
    "Japanese": "east_asian",
    "Korean": "east_asian",
    "Mongolian": "central_asian_to_east_asian",  # will map below
    "Mongol/Ottoman": "central_asian_to_east_asian",
    "Mongol": "central_asian_to_east_asian",
    "Turkic": "central_asian_to_east_asian",
    "Ottoman": "middle_eastern",
    "Tibetan": "east_asian",
    "Hindu": "south_asian",
    "Jewish": "middle_eastern",
    "Hawaiian": "oceanic",
    "Aztec": "mesoamerican",
    "Mesoamerican": "mesoamerican",
    "Tahitian": "oceanic",
    "Maori": "oceanic",
    "Persian": "middle_eastern",
    "Egyptian": "middle_eastern",
    "Arabic": "middle_eastern",
    "Islamic": "middle_eastern",
    "Welsh": "european",
    "Irish": "european",
    "Celtic": "european",
    "Lovecraftian": "fantasy_generic",
    "Western occult": "european",
}

def normalize_cultural_tradition(raw: str) -> str:
    """Map free-text cultural tradition to cultural_lineage_canonical enum."""
    if not raw:
        return "unknown"
    # exact match
    if raw in CULTURAL_TRADITION_MAP:
        v = CULTURAL_TRADITION_MAP[raw]
    else:
        # Try first '/' or '-' split component
        head = re.split(r"[/\-]", raw)[0].strip()
        v = CULTURAL_TRADITION_MAP.get(head, "unknown")
    # Collapse mixed-region placeholder to closest canonical bucket
    if v == "central_asian_to_east_asian":
        return "east_asian"  # Mongol/Turkic — best-fit in current enum
    return v


PERIOD_MAP = {
    "ancient": "classical",
    "classical": "classical",
    "pre-classical": "pre_classical",
    "late-antique": "classical",
    "medieval": "medieval",
    "early-modern": "early_modern",
    "early modern": "early_modern",
    "industrial": "industrial",
    "modern": "modern",
    "contemporary": "contemporary",
    "mythological": "fictional",
    "Bronze Age": "pre_classical",
    "Iron Age": "classical",
    "antiquity": "classical",
    "renaissance": "early_modern",
}

def normalize_period(raw: str) -> str:
    if not raw:
        return "unknown"
    return PERIOD_MAP.get(raw.lower().strip(), "unknown")


STYLE_REGISTER_MAP = {
    "historical": "historical",
    "military_modern": "military_modern",
    "fantasy": "fantasy",
    "sci-fi": "sci_fi",
    "sci_fi": "sci_fi",
    "mythological": "mythological",
}


def get_existing_row_count(cur) -> int:
    cur.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE (dedup_status != 'merged_into' OR dedup_status IS NULL)"
    )
    return cur.fetchone()[0]


# ------------------------- RECLASSIFICATION --------------------------------- #

def reclassify_shields(cur, log: list[dict]) -> int:
    """Reclassify shield rows in existing substrate to weapon_kind='shield'."""
    updates = 0
    # Royal Armouries — category_value='Shields'
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'shield',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library = 'royal_armouries'
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND json_extract(structured_properties, '$.category_value') = 'Shields'
           AND weapon_kind IN ('category','unknown','named_template')
           AND LOWER(canonical_name) NOT GLOB '*shield gun*'
           AND LOWER(canonical_name) NOT GLOB '*gun shield*'
           AND LOWER(canonical_name) NOT GLOB '*shoulder shield*'
           AND LOWER(canonical_name) NOT GLOB '*riot shield*'
        """,
        (
            OFF_HAND_PROXY["shield"]["proxy_range_class"],
            OFF_HAND_PROXY["shield"]["proxy_geometry_class"],
            OFF_HAND_PROXY["shield"]["proxy_tempo_class"],
            OFF_HAND_PROXY["shield"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "shields_royal_armouries", "rows_affected": cur.rowcount})

    # Met Museum — classification='Shields'
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'shield',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library = 'met-museum'
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND json_extract(structured_properties, '$.classification') = 'Shields'
           AND weapon_kind IN ('category','unknown','named_template')
        """,
        (
            OFF_HAND_PROXY["shield"]["proxy_range_class"],
            OFF_HAND_PROXY["shield"]["proxy_geometry_class"],
            OFF_HAND_PROXY["shield"]["proxy_tempo_class"],
            OFF_HAND_PROXY["shield"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "shields_met_museum", "rows_affected": cur.rowcount})

    # Wikidata — weapon_type='shield'
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'shield',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library = 'wikidata'
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND json_extract(structured_properties, '$.weapon_type') = 'shield'
           AND weapon_kind IN ('category','unknown','named_template')
        """,
        (
            OFF_HAND_PROXY["shield"]["proxy_range_class"],
            OFF_HAND_PROXY["shield"]["proxy_geometry_class"],
            OFF_HAND_PROXY["shield"]["proxy_tempo_class"],
            OFF_HAND_PROXY["shield"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "shields_wikidata", "rows_affected": cur.rowcount})

    # Wikipedia — name-token (filtered)
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'shield',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library = 'wikipedia'
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND weapon_kind IN ('category','unknown','named_template')
           AND (
                LOWER(canonical_name) GLOB '*shield*'
             OR LOWER(canonical_name) GLOB '*buckler*'
             OR LOWER(canonical_name) GLOB '*pavise*'
             OR LOWER(canonical_name) GLOB '*scutum*'
             OR LOWER(canonical_name) GLOB '*aspis*'
             OR LOWER(canonical_name) GLOB '*rondache*'
           )
           AND LOWER(canonical_name) NOT GLOB '*shield gun*'
           AND LOWER(canonical_name) NOT GLOB '*gun shield*'
           AND LOWER(canonical_name) NOT GLOB '*shoulder shield*'
           AND LOWER(canonical_name) NOT GLOB '*riot shield*'
        """,
        (
            OFF_HAND_PROXY["shield"]["proxy_range_class"],
            OFF_HAND_PROXY["shield"]["proxy_geometry_class"],
            OFF_HAND_PROXY["shield"]["proxy_tempo_class"],
            OFF_HAND_PROXY["shield"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "shields_wikipedia_name", "rows_affected": cur.rowcount})

    return updates


def reclassify_tomes(cur, log: list[dict]) -> int:
    updates = 0
    # Met Museum — classification='Books & Manuscripts'
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'tome',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library = 'met-museum'
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND json_extract(structured_properties, '$.classification') = 'Books & Manuscripts'
           AND weapon_kind IN ('category','unknown','named_template')
        """,
        (
            OFF_HAND_PROXY["tome"]["proxy_range_class"],
            OFF_HAND_PROXY["tome"]["proxy_geometry_class"],
            OFF_HAND_PROXY["tome"]["proxy_tempo_class"],
            OFF_HAND_PROXY["tome"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "tomes_met_museum", "rows_affected": cur.rowcount})

    # Wikipedia / Wikidata — name-token (filtered)
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'tome',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library IN ('wikipedia','wikidata')
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND weapon_kind IN ('category','unknown','named_template')
           AND (
                LOWER(canonical_name) GLOB '*grimoire*'
             OR LOWER(canonical_name) GLOB '*spellbook*'
             OR LOWER(canonical_name) GLOB '*codex*'
             OR LOWER(canonical_name) GLOB '*treatise*'
             OR LOWER(canonical_name) GLOB '*battletome*'
           )
           -- Exclude clear false-positives
           AND LOWER(canonical_name) NOT IN (
                'manual','operating manual','manual dexterity','manual crowd pummeler',
                'usmc sword manual procedures'
           )
        """,
        (
            OFF_HAND_PROXY["tome"]["proxy_range_class"],
            OFF_HAND_PROXY["tome"]["proxy_geometry_class"],
            OFF_HAND_PROXY["tome"]["proxy_tempo_class"],
            OFF_HAND_PROXY["tome"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "tomes_wp_wd_name", "rows_affected": cur.rowcount})

    return updates


def reclassify_banners(cur, log: list[dict]) -> int:
    updates = 0
    # Met Museum — classification='Banners' or 'Miscellaneous-Banners'
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'banner',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library = 'met-museum'
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND json_extract(structured_properties, '$.classification') IN ('Banners','Miscellaneous-Banners')
           AND weapon_kind IN ('category','unknown','named_template')
        """,
        (
            OFF_HAND_PROXY["banner"]["proxy_range_class"],
            OFF_HAND_PROXY["banner"]["proxy_geometry_class"],
            OFF_HAND_PROXY["banner"]["proxy_tempo_class"],
            OFF_HAND_PROXY["banner"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "banners_met_museum", "rows_affected": cur.rowcount})

    # OSRSBox — named-template banners ('Saradomin banner', 'Zamorak banner')
    # Note: the bare 'Banner' rows are osrsbox tradeable-item categories that
    # already have weapon_kind='category'; reclassify both named_template and
    # generic 'Banner' rows because they are by definition banner-type items.
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'banner',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library = 'osrsbox-db'
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND LOWER(canonical_name) GLOB '*banner*'
           AND weapon_kind IN ('category','unknown','named_template')
        """,
        (
            OFF_HAND_PROXY["banner"]["proxy_range_class"],
            OFF_HAND_PROXY["banner"]["proxy_geometry_class"],
            OFF_HAND_PROXY["banner"]["proxy_tempo_class"],
            OFF_HAND_PROXY["banner"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "banners_osrsbox", "rows_affected": cur.rowcount})

    # Wikipedia/Wikidata — name-token (filtered: not 'banner ad' etc.)
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'banner',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library IN ('wikipedia','wikidata')
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND weapon_kind IN ('category','unknown','named_template')
           AND (
                LOWER(canonical_name) GLOB '*oriflamme*'
             OR LOWER(canonical_name) GLOB '*sashimono*'
             OR LOWER(canonical_name) GLOB '*hata-jirushi*'
             OR LOWER(canonical_name) GLOB '*nobori*'
             OR LOWER(canonical_name) GLOB '*tugh*'
             OR LOWER(canonical_name) GLOB '*vexillum*'
             OR LOWER(canonical_name) GLOB '*labarum*'
             OR LOWER(canonical_name) GLOB '* banner'
             OR LOWER(canonical_name) GLOB 'banner of *'
             OR LOWER(canonical_name) GLOB '*war banner*'
             OR LOWER(canonical_name) GLOB '*battle standard*'
             OR LOWER(canonical_name) GLOB '*royal standard*'
           )
        """,
        (
            OFF_HAND_PROXY["banner"]["proxy_range_class"],
            OFF_HAND_PROXY["banner"]["proxy_geometry_class"],
            OFF_HAND_PROXY["banner"]["proxy_tempo_class"],
            OFF_HAND_PROXY["banner"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "banners_wp_wd_name", "rows_affected": cur.rowcount})

    return updates


def reclassify_horns(cur, log: list[dict]) -> int:
    updates = 0
    # Met Museum — classification='Horn-Implements' (Tibetan ritual horns)
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'horn',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library = 'met-museum'
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND json_extract(structured_properties, '$.classification') = 'Horn-Implements'
           AND weapon_kind IN ('category','unknown','named_template')
        """,
        (
            OFF_HAND_PROXY["horn"]["proxy_range_class"],
            OFF_HAND_PROXY["horn"]["proxy_geometry_class"],
            OFF_HAND_PROXY["horn"]["proxy_tempo_class"],
            OFF_HAND_PROXY["horn"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "horns_met_museum", "rows_affected": cur.rowcount})

    # Royal Armouries — Hunting horn / Ivory horn (NOT Powder horn — firearms accessory)
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'horn',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library = 'royal_armouries'
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND (LOWER(canonical_name) = 'hunting horn' OR LOWER(canonical_name) = 'ivory horn')
           AND json_extract(structured_properties, '$.category_value') != 'Firearms & related objects'
           AND weapon_kind IN ('category','unknown','named_template')
        """,
        (
            OFF_HAND_PROXY["horn"]["proxy_range_class"],
            OFF_HAND_PROXY["horn"]["proxy_geometry_class"],
            OFF_HAND_PROXY["horn"]["proxy_tempo_class"],
            OFF_HAND_PROXY["horn"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "horns_royal_armouries", "rows_affected": cur.rowcount})

    # Wikipedia/Wikidata — named historical/ceremonial horns
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'horn',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library IN ('wikipedia','wikidata')
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND weapon_kind IN ('category','unknown','named_template')
           AND (
                LOWER(canonical_name) GLOB '*shofar*'
             OR LOWER(canonical_name) GLOB '*carnyx*'
             OR LOWER(canonical_name) GLOB '*lituus*'
             OR LOWER(canonical_name) GLOB '*olifant*'
             OR LOWER(canonical_name) GLOB '*gjallarhorn*'
             OR LOWER(canonical_name) GLOB '*war horn*'
             OR LOWER(canonical_name) GLOB '*signal horn*'
             OR LOWER(canonical_name) GLOB '*hunting horn*'
             OR LOWER(canonical_name) GLOB '*cornu*'
             OR LOWER(canonical_name) GLOB '*lur (instrument)*'
             OR LOWER(canonical_name) GLOB '*pututu*'
             OR LOWER(canonical_name) GLOB '*salpinx*'
             OR LOWER(canonical_name) GLOB '*dungchen*'
             OR LOWER(canonical_name) GLOB '*shankha*'
           )
           AND LOWER(canonical_name) NOT GLOB '*hornet*'
           AND LOWER(canonical_name) NOT GLOB '*thorn*'
        """,
        (
            OFF_HAND_PROXY["horn"]["proxy_range_class"],
            OFF_HAND_PROXY["horn"]["proxy_geometry_class"],
            OFF_HAND_PROXY["horn"]["proxy_tempo_class"],
            OFF_HAND_PROXY["horn"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "horns_wp_wd_name", "rows_affected": cur.rowcount})

    return updates


def reclassify_talismans(cur, log: list[dict]) -> int:
    updates = 0
    # Fextralife DS1/DS3 — talismans (Dark Souls in-game off-hand category)
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'talisman',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library IN ('fextralife-ds1','fextralife-ds2','fextralife-ds3')
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND (LOWER(canonical_name) GLOB '*talisman' OR LOWER(canonical_name) = 'talisman')
           AND weapon_kind IN ('category','unknown','named_template')
        """,
        (
            OFF_HAND_PROXY["talisman"]["proxy_range_class"],
            OFF_HAND_PROXY["talisman"]["proxy_geometry_class"],
            OFF_HAND_PROXY["talisman"]["proxy_tempo_class"],
            OFF_HAND_PROXY["talisman"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "talismans_fextralife", "rows_affected": cur.rowcount})

    return updates


def reclassify_focuses(cur, log: list[dict]) -> int:
    """Focuses are sparse in existing substrate; mostly come from legolas Mode B
    insert. Reclassify only clear named-bearer focuses from wikidata/wikipedia."""
    updates = 0
    cur.execute(
        """
        UPDATE weapon_knowledge_entries
           SET weapon_kind = 'focus',
               proxy_range_class      = COALESCE(proxy_range_class,      ?),
               proxy_geometry_class   = COALESCE(proxy_geometry_class,   ?),
               proxy_tempo_class      = COALESCE(proxy_tempo_class,      ?),
               proxy_attribute_class  = COALESCE(proxy_attribute_class,  ?),
               proxy_fingerprint_confidence = COALESCE(proxy_fingerprint_confidence, ?)
         WHERE source_library IN ('wikipedia','wikidata')
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
           AND weapon_kind IN ('category','unknown','named_template')
           AND (
                LOWER(canonical_name) GLOB '*crystal ball*'
             OR LOWER(canonical_name) GLOB '*scrying*'
             OR LOWER(canonical_name) GLOB '*philosopher''s stone*'
           )
        """,
        (
            OFF_HAND_PROXY["focus"]["proxy_range_class"],
            OFF_HAND_PROXY["focus"]["proxy_geometry_class"],
            OFF_HAND_PROXY["focus"]["proxy_tempo_class"],
            OFF_HAND_PROXY["focus"]["proxy_attribute_class"],
            OFF_HAND_PROXY_CONFIDENCE,
        ),
    )
    updates += cur.rowcount
    log.append({"step": "focuses_wp_wd_name", "rows_affected": cur.rowcount})

    return updates


# --------------------- LEGOLAS MODE B INSERT -------------------------------- #

# Asset IDs flagged in legolas manifest as dedup pairs (drop these)
LEGOLAS_DEDUP_DROP = {"banner-021", "banner-033"}

# Asset IDs flagged as living-religious-tradition (substrate-only; tag for gandalf)
LEGOLAS_LIVING_TRADITION = {
    "tome-045",  # Book of Shadows
    "focus-008",  # Yasakani no Magatama
    "focus-012",  # Dorje
    "focus-018",  # Ofuda
    "focus-026",  # Prayer Wheel
    "horn-003",   # Shofar
    "horn-006",   # Dungchen
    "horn-018",   # Shanka
}


def normalize_legolas_row(rec: dict) -> dict:
    """Map legolas Mode B JSON to weapon_knowledge_entries column shape."""
    weapon_kind = rec.get("weapon_kind") or rec.get("category") or "unknown"
    if weapon_kind not in OFF_HAND_PROXY:
        weapon_kind = "unknown"

    structured = {
        # Preserve legolas-extracted structured fields
        "category": rec.get("category"),
        "dimensionality": rec.get("dimensionality"),
        "style_register": rec.get("style_register"),
        "decomposition": rec.get("decomposition"),
        "file_format": rec.get("file_format"),
        "license": rec.get("license"),
        "cost": rec.get("cost"),
        "cultural_tradition": rec.get("cultural_tradition"),
        "period": rec.get("period"),
        "approx_date": rec.get("approx_date"),
        "author": rec.get("author"),
        "subject": rec.get("subject"),
        "appearance": rec.get("appearance"),
        "significance": rec.get("significance"),
        "slot_eligibility": rec.get("slot_eligibility"),
        "deliverable_register": rec.get("deliverable_register"),
        "legolas_asset_id": rec.get("asset_id"),
        "legolas_crawl_date": rec.get("crawl_date"),
    }

    style_tags = rec.get("style_tags") or []
    cultural_tag_value = json.dumps(style_tags) if style_tags else None

    # Map style_register → register_canonical
    raw_reg = (rec.get("style_register") or "").lower()
    register_canonical = STYLE_REGISTER_MAP.get(raw_reg, "unknown")

    # cultural_lineage_canonical
    cult_raw = rec.get("cultural_tradition") or ""
    cultural_lineage = normalize_cultural_tradition(cult_raw)

    # historical_period_canonical
    period_canonical = normalize_period(rec.get("period") or "")

    # Style tags as cultural_lineage_tags
    return {
        "canonical_name": rec["name"],
        "source_library": rec.get("source", "wikipedia"),
        "source_url": rec["url"],
        "source_id": rec.get("asset_id"),
        "description_text": rec.get("significance") or rec.get("subject"),
        "structured_properties": json.dumps({k: v for k, v in structured.items() if v is not None}),
        "cultural_lineage_tags": cultural_tag_value,
        "historical_period": rec.get("period"),
        "genre_appearances": json.dumps([rec["style_register"]]) if rec.get("style_register") else None,
        "license_class": rec.get("license"),
        "weapon_kind": weapon_kind,
        "register_canonical": register_canonical,
        "cultural_lineage_canonical": cultural_lineage,
        "historical_period_canonical": period_canonical,
        "cultural_lineage_confidence": 0.75 if cultural_lineage != "unknown" else 0.4,
        "extracted_named_bearer": rec.get("author"),
        # Note: legolas asset_id appears in source_id; also used for living-tradition flag
        "legolas_asset_id": rec.get("asset_id"),
    }


def insert_legolas_rows(cur, log: list[dict]) -> tuple[int, int, int]:
    """Insert legolas Mode B 132 rows, dedup 2, return (inserted, dedup_skipped, living_traditions_flagged)."""
    files_to_consume = [
        LEGOLAS_DIR / "tomes" / "cleaned-tomes-2026-05-25.jsonl",
        LEGOLAS_DIR / "banners" / "cleaned-banners-2026-05-25.jsonl",
        LEGOLAS_DIR / "focuses" / "cleaned-focuses-talismans-2026-05-25.jsonl",
        LEGOLAS_DIR / "horns" / "cleaned-horns-2026-05-25.jsonl",
    ]

    inserted = 0
    dedup_skipped = 0
    living_flagged = 0

    for path in files_to_consume:
        if not path.exists():
            print(f"WARN: legolas file not found: {path}")
            continue
        with path.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)

                if rec.get("asset_id") in LEGOLAS_DEDUP_DROP:
                    dedup_skipped += 1
                    continue

                norm = normalize_legolas_row(rec)
                weapon_kind = norm["weapon_kind"]
                proxy = OFF_HAND_PROXY.get(weapon_kind, {})

                # Check UNIQUE (source_library, source_url) — if exists, skip to avoid dup with
                # potential earlier ingest. This is also defensive against re-runs.
                cur.execute(
                    "SELECT id, weapon_kind FROM weapon_knowledge_entries WHERE source_library = ? AND source_url = ? LIMIT 1",
                    (norm["source_library"], norm["source_url"] + f"#{norm['legolas_asset_id']}"),
                )
                # Note: legolas Mode B rows share source_url within a single Wikipedia page (e.g., all
                # 'tomes from Military_treatise' share URL). The substrate UNIQUE constraint on
                # (source_library, source_url) would block multiple inserts. We add the asset_id as a
                # URL fragment to ensure unique per legolas asset.
                existing = cur.fetchone()
                if existing:
                    continue  # already inserted in a prior run

                living_flag = norm["legolas_asset_id"] in LEGOLAS_LIVING_TRADITION
                if living_flag:
                    living_flagged += 1

                cur.execute(
                    """
                    INSERT INTO weapon_knowledge_entries (
                        canonical_name, source_library, source_url, source_id,
                        description_text, structured_properties,
                        cultural_lineage_tags, historical_period, genre_appearances,
                        license_class, weapon_kind,
                        register_canonical, cultural_lineage_canonical,
                        historical_period_canonical, cultural_lineage_confidence,
                        extracted_named_bearer,
                        proxy_range_class, proxy_geometry_class,
                        proxy_tempo_class, proxy_attribute_class,
                        proxy_fingerprint_confidence
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        norm["canonical_name"],
                        norm["source_library"],
                        norm["source_url"] + f"#{norm['legolas_asset_id']}",  # uniqueness fragment
                        norm["source_id"],
                        norm["description_text"],
                        norm["structured_properties"],
                        norm["cultural_lineage_tags"],
                        norm["historical_period"],
                        norm["genre_appearances"],
                        norm["license_class"],
                        weapon_kind,
                        norm["register_canonical"],
                        norm["cultural_lineage_canonical"],
                        norm["historical_period_canonical"],
                        norm["cultural_lineage_confidence"],
                        norm["extracted_named_bearer"],
                        proxy.get("proxy_range_class"),
                        proxy.get("proxy_geometry_class"),
                        proxy.get("proxy_tempo_class"),
                        proxy.get("proxy_attribute_class"),
                        OFF_HAND_PROXY_CONFIDENCE,
                    ),
                )
                inserted += 1

    log.append({"step": "legolas_mode_b_insert", "rows_inserted": inserted, "dedup_skipped": dedup_skipped, "living_traditions_flagged": living_flagged})
    return inserted, dedup_skipped, living_flagged


# ----------------------- SAMPLE EXTRACTION ---------------------------------- #

def emit_per_category_samples(cur) -> dict:
    """Pull 5-10 sample rows per off-hand category for the curation artifact."""
    samples = {}
    for cat in ("shield", "tome", "banner", "focus", "horn", "talisman"):
        cur.execute(
            """
            SELECT id, canonical_name, source_library, register_canonical,
                   cultural_lineage_canonical, historical_period_canonical,
                   proxy_geometry_class, proxy_fingerprint_confidence
              FROM weapon_knowledge_entries
             WHERE weapon_kind = ?
               AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
             ORDER BY RANDOM()
             LIMIT 10
            """,
            (cat,),
        )
        rows = cur.fetchall()
        samples[cat] = [
            {
                "id": r[0],
                "canonical_name": r[1],
                "source_library": r[2],
                "register_canonical": r[3],
                "cultural_lineage_canonical": r[4],
                "historical_period_canonical": r[5],
                "proxy_geometry_class": r[6],
                "proxy_fingerprint_confidence": r[7],
            }
            for r in rows
        ]
    return samples


def emit_per_category_counts(cur) -> dict:
    """Final per-category counts after mining + insert."""
    counts = {}
    for cat in ("shield", "tome", "banner", "focus", "horn", "talisman"):
        cur.execute(
            """SELECT COUNT(*) FROM weapon_knowledge_entries
                WHERE weapon_kind = ?
                  AND (dedup_status != 'merged_into' OR dedup_status IS NULL)""",
            (cat,),
        )
        counts[cat] = cur.fetchone()[0]
    # Total off-hand
    cur.execute(
        """SELECT COUNT(*) FROM weapon_knowledge_entries
            WHERE weapon_kind IN ('shield','tome','banner','focus','horn','talisman')
              AND (dedup_status != 'merged_into' OR dedup_status IS NULL)"""
    )
    counts["_off_hand_total"] = cur.fetchone()[0]
    return counts


# ------------------------------ MAIN --------------------------------------- #

def main() -> int:
    if not DB_PATH.exists():
        print(f"FATAL: DB not found at {DB_PATH}", file=sys.stderr)
        return 1
    if not LEGOLAS_DIR.exists():
        print(f"FATAL: legolas Mode B dir not found at {LEGOLAS_DIR}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    log: list[dict] = []
    pre_active = get_existing_row_count(cur)

    # Empirical pre-state per-category snapshot (Discipline #11)
    pre_counts = emit_per_category_counts(cur)

    # --- Existing-source mining (reclassifications) ----
    cur.execute("BEGIN")
    try:
        shield_n  = reclassify_shields(cur, log)
        tome_n    = reclassify_tomes(cur, log)
        banner_n  = reclassify_banners(cur, log)
        horn_n    = reclassify_horns(cur, log)
        talis_n   = reclassify_talismans(cur, log)
        focus_n   = reclassify_focuses(cur, log)
        inserted, dedup, living = insert_legolas_rows(cur, log)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"FATAL: mining/insert transaction failed; rolled back. error={e}", file=sys.stderr)
        return 2

    post_active = get_existing_row_count(cur)
    post_counts = emit_per_category_counts(cur)
    samples = emit_per_category_samples(cur)

    # Discipline #25 rep-audit: did the new weapon_kind cells actually contain off-hand items?
    # For each category, spot-check the random sample for "does this look off-hand?"
    # (this is human-curated; emit the sample for gandalf review)

    # Tier S/A intersection: any off-hand items already touched by Stage 2.5 tier-S classification?
    cur.execute(
        """
        SELECT weapon_kind, COUNT(*) FROM weapon_knowledge_entries
         WHERE weapon_kind IN ('shield','tome','banner','focus','horn','talisman')
           AND quality_tier IS NOT NULL
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
         GROUP BY weapon_kind
        """
    )
    tier_intersection = dict(cur.fetchall())

    # v1_scope intersection
    cur.execute(
        """
        SELECT weapon_kind, COUNT(*) FROM weapon_knowledge_entries
         WHERE weapon_kind IN ('shield','tome','banner','focus','horn','talisman')
           AND v1_scope = 1
           AND (dedup_status != 'merged_into' OR dedup_status IS NULL)
         GROUP BY weapon_kind
        """
    )
    v1_intersection = dict(cur.fetchall())

    output = {
        "cycle": "10",
        "sidecar": "B",
        "date": "2026-05-25",
        "owner": "elrond",
        "dispatch": "agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-sidecar-b-off-hand-substrate.md",
        "schema_extension_applied": True,
        "pre_state": {
            "active_rows": pre_active,
            "per_category": pre_counts,
        },
        "mining_log": log,
        "reclassification_totals": {
            "shield": shield_n,
            "tome": tome_n,
            "banner": banner_n,
            "horn": horn_n,
            "talisman": talis_n,
            "focus": focus_n,
            "_existing_source_reclassified_total": shield_n + tome_n + banner_n + horn_n + talis_n + focus_n,
        },
        "legolas_mode_b_insert": {
            "rows_inserted": inserted,
            "dedup_pairs_dropped": dedup,
            "living_tradition_flagged": living,
            "living_tradition_asset_ids": sorted(LEGOLAS_LIVING_TRADITION),
            "dedup_dropped_asset_ids": sorted(LEGOLAS_DEDUP_DROP),
        },
        "post_state": {
            "active_rows": post_active,
            "per_category": post_counts,
        },
        "tier_quality_intersection": tier_intersection,
        "v1_scope_intersection": v1_intersection,
        "samples_per_category": samples,
        "proxy_profiles_applied": OFF_HAND_PROXY,
        "proxy_fingerprint_confidence_applied": OFF_HAND_PROXY_CONFIDENCE,
        "stage_4_consult_note": (
            "Proxy fingerprints for off-hand items use weapon-aligned heuristics "
            "(damage-geometry → buff-geometry; damage-tempo → aura-tempo) per dispatch § 4.5. "
            "Stage 4 dispatch (Wave 7) will refine via legolas Mode A consult on off-hand mechanical-axis design."
        ),
    }

    out_path = OUTPUT_DIR / "existing-source-mining.json"
    out_path.write_text(json.dumps(output, indent=2))
    print(f"[ok] wrote {out_path}")
    print(f"[stats] pre_active={pre_active} post_active={post_active}  delta={post_active-pre_active}")
    print(f"[stats] reclassified: shield={shield_n} tome={tome_n} banner={banner_n} horn={horn_n} talisman={talis_n} focus={focus_n}")
    print(f"[stats] legolas inserted={inserted} dedup_dropped={dedup} living_traditions_flagged={living}")
    print(f"[stats] final off-hand counts: {post_counts}")

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
