#!/usr/bin/env python3
"""
Cycle 12 SC-1 substrate-tagging cleanup — Tier-S named-mythological items
canonical-lineage + canonical-period backfill.

Authority: Matt 2026-05-25 Cycle 12 framing brief bulk-ratification
Dispatch: 2026-05-25-elrond-cycle-12-sc-1-substrate-tagging-cleanup.md

Per Discipline #11 (empirical inspection BEFORE updating): I direct-inspected
the 150-row Tier-S unknown set and found it splits into:

  Subset A — Mythological items proper (canonical_name IS the named mythological
             weapon itself; Sketch F anchor-naming target). 30 items.

  Subset B — Real historical-figure weapons (canonical_name IS the named
             historical weapon attributed to a figure). 21 items.

  Subset C — DEFERRED + FLAGGED for gandalf Pattern A-light:
             - Modern military hardware named-after-mythology (Agni-II/IV/V/VI/P,
               M982 Excalibur, M142 HIMARS, Operation Aphrodite, etc.)
             - Royal Armouries generic-typology curatorial items (Pike, Print,
               Painting, Wooden head, etc.) attributed by depiction/temporal-
               association
             - Modern-fictional items namedropping mythology (Hammer of Thor
               [TMNT 1987], Dark Elf Particle Rifle [Marvel Thor], etc.)
             - Museum items where named-bearer match is spurious (Musée
               Saint-Raymond items tagged via museum-name)
             - Items where the bearer-match is depictive-not-substantive
               (Shield Depicting Saint George Slaying the Dragon)
             ~99 items.

Backfill mapping:
  named_mythological tradition → (cultural_lineage_canonical, historical_period_canonical)
  greek            → european      / classical
  norse            → european      / medieval        (historiographic skaldic era)
  vedic_hindu      → south_asian   / pre_classical   (Vedic itihasa)
  east_asian       → east_asian    / (per-item; varies)
  european_medieval→ european      / medieval
  egyptian         → middle_eastern / pre_classical  (Pharaonic)
  mesopotamian     → middle_eastern / pre_classical  (Sumer/Akkad/Assyria)

For Subset B (real historical-figure weapons), period is derived from the
historical figure's era:
  Charlemagne/El Cid/medieval-figures        → medieval
  Masamune/Sadamune/Yoshimitsu/Kotetsu/Norimitsu (Japanese smiths) → early_modern
  Tukulti-Ninurta I (Mace-AO 2152), Shulgi   → pre_classical
  Tutankhamun                                 → pre_classical

Idempotency: only updates fields where current value is 'unknown'. Existing
non-unknown values are preserved (e.g., id=379 Mjölnir keeps cultural=european
and only historical_period_canonical is set).

ADR-004: this is a data-backfill on existing columns; no schema change. Cross-
seam consumers (cohesion-judge / spirit-guide explainer / loadout app) read same
columns; new values surface. MIGRATION.md authored.

Confidence: cultural_lineage_confidence is set to 0.9 for these backfills
(strong-signal: named-mythological-bearer match + canonical_name = mythological
weapon proper). Higher than the 0.7 description-regex confidence used by Phase D
Step 6.5. Lower than 1.0 to preserve the meta-signal that this is an elrond-
applied backfill, not a vendor-source-structured-tag.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("/Users/admin/Games/reincarnated-loadout/data/telemetry.db")
WORK_DIR = Path(__file__).resolve().parent
LOG_PATH = WORK_DIR / "sc1_backfill_log.json"

# ----------------------------------------------------------------------------
# Subset A — Mythological items proper (canonical_name IS the mythological weapon)
# ----------------------------------------------------------------------------
# Format: (id, canonical_name, cultural_lineage_canonical, historical_period_canonical, comment)

SUBSET_A_BACKFILLS: list[tuple[int, str, str, str, str]] = [
    # GREEK / classical
    (11,   "shield of Achilles",        "european",       "classical",     "Iliad-described; Greek classical"),
    (660,  "trident of Poseidon",       "european",       "classical",     "Olympian-attributed; Greek classical"),

    # VEDIC-HINDU / pre_classical (itihasa era)
    (131,  "Indraastra",                "south_asian",    "pre_classical", "Vedic celestial weapon of Indra"),
    (134,  "Anjalikastra",              "south_asian",    "pre_classical", "Vedic celestial weapon"),
    (366,  "Vijaya",                    "south_asian",    "pre_classical", "Vedic celestial bow (Indra-attributed)"),
    (385,  "vajra",                     "south_asian",    "pre_classical", "Vedic ritual weapon; already south_asian, period unknown"),
    (482,  "Gandiva",                   "south_asian",    "pre_classical", "Mahabharata celestial bow of Arjuna"),
    (174145, "Vajra",                   "south_asian",    "pre_classical", "Vajra Wikipedia article (variant; already south_asian)"),
    (176853, "Vel",                     "south_asian",    "pre_classical", "Divine spear of Murugan"),

    # NORSE / medieval (skaldic-era; using medieval per project canonical period taxonomy)
    (379,  "Mjölnir",                   "european",       "medieval",      "Thor's hammer; Norse mythological (already european)"),
    (387,  "Gungnir",                   "european",       "medieval",      "Odin's spear; Norse mythological (already european)"),
    (4996, "Sword of Freyr",            "european",       "medieval",      "Freyr's sword; Norse mythological (already european)"),
    (191620, "Sword of Freyr",          "european",       "medieval",      "Freyr's sword wikipedia article variant (already european)"),
    (5131, "Hrunting",                  "european",       "medieval",      "Beowulf's sword (already european)"),
    (5135, "Nægling",                   "european",       "medieval",      "Beowulf's sword (wikidata variant)"),
    (5144, "Hǫfuð",                     "european",       "medieval",      "Sword of Heimdall in Norse myth"),
    (180679, "Mistilteinn",             "european",       "medieval",      "Mistletoe-arrow that slew Baldr; Norse (already european)"),
    (176855, "Nægling",                 "european",       "medieval",      "Beowulf's sword (wikipedia variant; already european)"),

    # CELTIC / EUROPEAN-MEDIEVAL Arthurian + Carolingian / medieval
    (497,  "Carnwennan",                "european",       "medieval",      "Arthurian dagger (already european)"),
    (5108, "Excalibur",                 "european",       "medieval",      "Arthur's legendary sword (already european)"),
    (5097, "Galatine",                  "european",       "medieval",      "Gawain's Arthurian sword"),
    (5165, "Aroundight",                "european",       "medieval",      "Lancelot's romance sword"),
    (5105, "Ascalon",                   "european",       "medieval",      "Saint George's legendary sword"),
    (5137, "Hauteclere",                "european",       "medieval",      "Oliver's sword in Charlemagne legend"),
    (209,  "Failnaught",                "european",       "medieval",      "Tristan's bow (Arthurian romance)"),
    (4391, "Saber of Charlemagne",      "european",       "medieval",      "Carolingian-era saber (already european)"),
    (175580, "Joyeuse",                 "european",       "medieval",      "Charlemagne's legendary sword (already european)"),
    (190415, "Sabre of Charlemagne",    "european",       "medieval",      "Carolingian saber wikipedia article (already european)"),
    (175173, "Curtana",                 "european",       "medieval",      "Sword of Mercy; English coronation regalia (already european)"),

    # EAST-ASIAN mythological / pre_classical to medieval
    (388,  "Ruyi Jingu Bang",           "east_asian",     "pre_classical", "Sun Wukong's magical staff; Journey-to-the-West Tang-era folklore (already east_asian)"),
    (924,  "Green Dragon Crescent Blade","east_asian",    "classical",     "Guan Yu's polearm; Three Kingdoms era (already east_asian)"),
    (194198, "Tai'e",                   "east_asian",     "classical",     "Legendary ancient Chinese sword"),
    (174017, "Naginata",                "east_asian",     "medieval",      "Japanese polearm (Tomoe Gozen-attributed; already east_asian)"),
]

# ----------------------------------------------------------------------------
# Subset B — Real historical-figure weapons (named-bearer = historical figure;
# canonical_name IS a real named weapon; period derives from figure's era)
# ----------------------------------------------------------------------------

SUBSET_B_BACKFILLS: list[tuple[int, str, str, str, str]] = [
    # EL CID / Spanish medieval reconquista
    (2463, "Tizona",                    "european",       "medieval",      "El Cid's sword (already european)"),
    (2477, "Colada",                    "european",       "medieval",      "El Cid's second sword (already european)"),
    (181836, "Colada",                  "european",       "medieval",      "El Cid's sword wikipedia article (already european)"),

    # JAPANESE smith-attributed blades / early_modern (Edo-era curation; Kamakura-Muromachi creation)
    (1647, "Hyūga Masamune",            "east_asian",     "early_modern",  "Masamune blade (already east_asian)"),
    (1728, "Hōchō Masamune",            "east_asian",     "early_modern",  "Masamune blade (already east_asian)"),
    (1734, "Hōchō Masamune",            "east_asian",     "early_modern",  "Masamune blade (already east_asian)"),
    (1736, "Hōchō Masamune",            "east_asian",     "early_modern",  "Masamune blade (already east_asian)"),
    (1738, "Kuki Masamune",             "east_asian",     "early_modern",  "Masamune blade (already east_asian)"),
    (3149, "Ishida Masamune",           "east_asian",     "early_modern",  "Masamune blade"),
    (4254, "Tsugaru Masamune",          "east_asian",     "early_modern",  "Masamune blade (already east_asian)"),
    (4255, "Nakatsukasa Masamune",      "east_asian",     "early_modern",  "Masamune blade (already east_asian)"),
    (4256, "Kanze Masamune",            "east_asian",     "early_modern",  "Masamune blade (already east_asian)"),
    (4257, "Tarosaku Masamune",         "east_asian",     "early_modern",  "Masamune blade (already east_asian)"),
    (1729, "Terasawa Sadamune",         "east_asian",     "early_modern",  "Sadamune blade (already east_asian)"),
    (1730, "Tokuzen-in Sadamune",       "east_asian",     "early_modern",  "Sadamune blade (already east_asian)"),
    (1737, "Fushimi Sadamune",          "east_asian",     "early_modern",  "Sadamune blade (already east_asian)"),
    (3224, "Hakusan Yoshimitsu",        "east_asian",     "early_modern",  "Yoshimitsu blade (already east_asian)"),
    (4288, "Nagasone Kotetsu",          "east_asian",     "early_modern",  "Kotetsu blade"),
    (3164, "Wakisashi by Norimitsu",    "east_asian",     "early_modern",  "Norimitsu wakizashi; period already early_modern"),

    # EGYPTIAN ANCIENT (Pharaonic) / pre_classical
    (1676, "Tutankhamun's meteoric iron dagger blade", "middle_eastern", "pre_classical",
                                                                        "18th Dynasty (~1336-1327 BCE) tomb artifact; overrides 'medieval' regex misfire"),
    (13367, "Narmer Macehead",          "middle_eastern", "pre_classical", "Early Dynastic Egyptian (~3100 BCE) decorative mace head"),

    # MESOPOTAMIAN ANCIENT / pre_classical
    (107,  "Mace-AO 2152",              "middle_eastern", "pre_classical", "Mace of Tukulti-Ninurta I (1243-1207 BCE); overrides 'contemporary' regex misfire"),
    (634,  "mace",                      "middle_eastern", "pre_classical", "Shulgi (~2094-2046 BCE) dedicatory mace; overrides 'contemporary' regex misfire"),
]

# ----------------------------------------------------------------------------
# Subset C — DEFERRED (flagged separately for gandalf Pattern A-light routing).
# NOT updated in this dispatch. Listed here for traceability.
# ----------------------------------------------------------------------------

SUBSET_C_DEFERRED: list[tuple[int, str, str, str]] = [
    # Modern military named-after-mythology — named-mythological-bearer is naming-only attribution
    (176575, "Agni-II",         "wikipedia",       "Modern Indian ballistic missile; named-after Vedic Agni; NOT Sketch F target"),
    (181810, "Agni-IV",         "wikipedia",       "Modern Indian missile"),
    (187688, "Agni-V",          "wikipedia",       "Modern Indian missile"),
    (189522, "Agni-VI",         "wikipedia",       "Modern Indian missile"),
    (192956, "Agni-P",          "wikipedia",       "Modern Indian missile"),
    (174029, "Kukri",           "wikipedia",       "Nepalese knife; named-bearer match to Alexander the Great is spurious"),
    (175087, "Operation Aphrodite", "wikipedia",   "WWII USAAF operation codename; named-bearer attribution"),
    (176135, "M982 Excalibur",  "wikipedia",       "Modern guided artillery shell named-after Arthurian Excalibur"),
    (181325, "Migration Period sword", "wikipedia","Generic typology; Beowulf-tagged via mention"),
    (189708, "ShAK-12",         "wikipedia",       "Russian carbine; Beowulf-tagged spuriously"),
    (173959, "War hammer",      "wikipedia",       "Generic typology; Charles Martel-tagged via etymology mention"),
    (191289, "21 cm SK L/40",   "wikipedia",       "WWI German naval gun; Freyja-tagged spuriously"),
    (192601, "Bharat-52",       "wikipedia",       "Modern Indian howitzer; Garuda-tagged"),
    (192830, "Pindad Maung",    "wikipedia",       "Modern Indonesian vehicle; Garuda-tagged"),
    (192784, "Zastava M19",     "wikipedia",       "Modern Serbian rifle; 6.5 Grendel cartridge-tagged"),
    (181848, "Imperial Sword",  "wikipedia",       "HRE Imperial regalia; Henry-the-Fowler-tagged"),
    (174014, "M142 HIMARS",     "wikipedia",       "Modern rocket launcher; Hercules-aircraft-mention"),
    (174207, "Nike Hercules",   "wikipedia",       "Cold-War missile"),
    (174383, "Bloodhound (missile)", "wikipedia",  "1950s British missile"),
    (175339, "NASAMS",          "wikipedia",       "Modern SAM system"),
    (175441, "FNSS ACV-19",     "wikipedia",       "Modern Turkish IFV"),
    (176150, "MGM-134 Midgetman", "wikipedia",     "Cold-War ICBM"),
    (176276, "Coventry armoured car", "wikipedia", "WWII British armoured car"),
    (176975, "M88 recovery vehicle", "wikipedia",  "Modern ARV"),
    (181492, "Hyunmoo-3",       "wikipedia",       "Modern South Korean cruise missile"),
    (187818, "High Velocity Aircraft Rocket", "wikipedia", "WWII rocket"),
    (188637, "Chenowth Advanced Light Strike Vehicle", "wikipedia", "Modern vehicle"),
    (190235, "Nike Zeus",       "wikipedia",       "Cold-War ABM"),
    (190334, "General Dynamics Flyer", "wikipedia","Modern vehicle"),
    (182497, "21 cm Mörser 10", "wikipedia",       "WWI German howitzer; Isis-tagged spuriously"),
    (189505, "Type 73 light machine gun", "wikipedia", "Modern NK LMG; Isis-tagged spuriously"),
    (193457, "Tumbok lada",     "wikipedia",       "Malay dagger; Lada-tagged via name homonymy"),
    (176295, "ELVO Kentaurus",  "wikipedia",       "Modern Greek IFV; Leonidas-tagged spuriously"),
    (174611, "Grand Slam (bomb)","wikipedia",      "WWII RAF earthquake bomb; Merlin-engine-mention"),
    (189638, "MGD PM-9",        "wikipedia",       "1950s SMG; Merlin-tagged spuriously"),
    (175736, "46 cm/45 Type 94 naval gun", "wikipedia", "WWII Japanese naval gun; Musashi-tagged"),
    (174194, "M3 Lee",          "wikipedia",       "WWII US tank; Odysseus-tagged spuriously"),
    (174108, "Cutlass",         "wikipedia",       "Generic typology; Oisín-tagged spuriously"),
    (173952, "Trident (missile)","wikipedia",      "Modern SLBM; Poseidon-tagged"),
    (176461, "W68",             "wikipedia",       "Cold-War warhead; Poseidon-tagged"),
    (188301, "Harpoon (missile)","wikipedia",      "Modern anti-ship missile; Poseidon-tagged"),
    (174631, "Combat Vehicle Reconnaissance (Tracked)", "wikipedia", "Modern AFV; Saladin-tagged"),
    (174104, "Katar",           "wikipedia",       "Indian dagger typology; Shivaji-tagged"),
    (182089, "Bichuwa",         "wikipedia",       "Indian dagger typology; Shivaji-tagged"),
    (182653, "Surya missile",   "wikipedia",       "Speculated Indian ICBM; Surya-tagged"),
    (173945, "Katyusha rocket launcher", "wikipedia", "WWII Soviet rocket artillery; Suvorov-tagged"),
    (192182, "THeMIS",          "wikipedia",       "Modern UGV; Themis-tagged"),
    (192856, "Integrated Unmanned Ground System", "wikipedia", "Modern UGS; Themis-tagged"),
    (176834, "Otomat",          "wikipedia",       "Modern anti-ship missile; Theseus-tagged"),
    (175456, "Mjolnir (comics)","wikipedia",       "Marvel Comics fictional weapon"),
    (175890, "Mark 7 nuclear bomb", "wikipedia",   "Cold-War nuclear bomb (Thor-codename)"),
    (174117, "Sten",            "wikipedia",       "WWII British SMG; Turpin-tagged"),
    (191035, "Varunastra (torpedo)", "wikipedia",  "Modern Indian torpedo; Varuna-tagged"),

    # Modern-fictional namedropping mythology
    (532,  "Hammer of Thor",    "wikidata",        "Fictional 1987 TMNT weapon"),
    (603,  "Dark Elf Particle Rifle", "wikidata",  "Marvel Thor: Dark World fictional"),
    (606,  "Asgardian Cannon",  "wikidata",        "Marvel Thor: Dark World fictional"),

    # Spurious museum-name attribution
    (77,   "Q88199410",         "wikidata",        "Musée Saint-Raymond item; Raymond-of-Toulouse via museum name"),
    (1006, "Musée Saint-Raymond, D 78 6 6", "wikidata", "Museum cataloguing item"),
    (1530, "Musée Saint-Raymond, Niel 2463 n°6", "wikidata", "Museum cataloguing item"),

    # Depictive-not-substantive
    (46,   "Shield Depicting Saint George Slaying the Dragon", "wikidata", "19th-century depictive shield; named-bearer is depiction-content"),

    # Royal Armouries generic-typology curatorial items
    # (canonical_name is generic 'Pike'/'Print'/'Painting'/'Sword'/'Wooden head'/'Helm'/'Pollaxe'/'Gun'/'Partizan'/
    #  'Equestrian mannequin'; named-bearer attribution via depiction or temporal-association;
    #  NOT named-mythological-bearer-resonance Sketch F target)
    (204133, "Painting",        "royal_armouries", "Augustus-depicting painting"),
    (219614, "Partizan",        "royal_armouries", "Augustus-era partizan"),
    (196880, "Helm",            "royal_armouries", "Black-Prince-attributed helm"),
    (208781, "Wooden head",     "royal_armouries", "Edward III curatorial object"),
    (209612, "Print",           "royal_armouries", "Edward III print"),
    (206662, "Sword",           "royal_armouries", "Elizabeth I sword"),
    (211611, "Print",           "royal_armouries", "Elizabeth I print"),
    (204323, "Print",           "royal_armouries", "Francis Drake print"),
    (207299, "Print",           "royal_armouries", "Gaston de Foix print"),
    (209511, "Print",           "royal_armouries", "Gaston de Foix print"),
    (204318, "Print",           "royal_armouries", "Henry Bolingbroke print"),
    (159244, "Pike",            "royal_armouries", "Henry VIII pike"),
    (159288, "Pike",            "royal_armouries", "Henry VIII pike"),
    (159291, "Pike",            "royal_armouries", "Henry VIII pike"),
    (197738, "Pollaxe",         "royal_armouries", "Henry VIII pollaxe"),
    (198374, "Pike",            "royal_armouries", "Henry VIII pike"),
    (199788, "Print",           "royal_armouries", "Henry VIII print"),
    (203288, "Gun",             "royal_armouries", "Henry VIII gun"),
    (204135, "Painting",        "royal_armouries", "Henry VIII painting"),
    (204298, "Print",           "royal_armouries", "Henry VIII print"),
    (204696, "Equestrian mannequin", "royal_armouries", "Henry VIII equestrian"),
    (208015, "Print",           "royal_armouries", "Henry VIII print"),
    (208289, "Partizan",        "royal_armouries", "Henry VIII partizan"),
    (209783, "Wooden head",     "royal_armouries", "Henry VIII curatorial"),
    (218476, "Pike",            "royal_armouries", "Henry VIII pike"),
    (218478, "Pike",            "royal_armouries", "Henry VIII pike"),
    (218481, "Pike",            "royal_armouries", "Henry VIII pike"),
    (207287, "Print",           "royal_armouries", "John Hawkwood print"),
    (204328, "Wooden head",     "royal_armouries", "John of Gaunt curatorial"),
    (209510, "Print",           "royal_armouries", "Maximilian I print"),
    (201336, "Sword",           "royal_armouries", "Paris of Troy depictive sword"),
    (210962, "Sword",           "royal_armouries", "Saladin depictive sword"),
    (204314, "Print",           "royal_armouries", "Walter Raleigh print"),
    (210888, "Wooden head",     "royal_armouries", "William the Conqueror curatorial"),
]


def conn_open() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH.as_posix())
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA busy_timeout = 30000")  # Per dispatch concurrency note + Cycle 11 P2.5 pattern
    c.execute("PRAGMA foreign_keys = ON")
    return c


def fetch_pre_state(c: sqlite3.Connection, ids: list[int]) -> dict[int, dict]:
    rows: dict[int, dict] = {}
    if not ids:
        return rows
    placeholder = ",".join("?" for _ in ids)
    cur = c.execute(
        f"""SELECT id, canonical_name, source_library, quality_tier,
                   cultural_lineage_canonical, historical_period_canonical,
                   cultural_lineage_confidence, named_mythological_match
            FROM weapon_knowledge_entries
            WHERE id IN ({placeholder})""",
        ids,
    )
    for r in cur.fetchall():
        rows[r["id"]] = dict(r)
    return rows


def apply_backfill(c: sqlite3.Connection,
                   backfills: list[tuple[int, str, str, str, str]],
                   subset_label: str) -> tuple[int, int, list[dict]]:
    """Idempotent backfill: only update unknown fields. Returns (rows_touched, fields_updated_count, per_row_log)."""
    rows_touched = 0
    fields_updated = 0
    per_row_log: list[dict] = []
    ids = [b[0] for b in backfills]
    pre = fetch_pre_state(c, ids)

    for (id_, name_hint, lineage, period, comment) in backfills:
        pre_row = pre.get(id_)
        if pre_row is None:
            per_row_log.append({
                "id": id_, "subset": subset_label, "status": "skip-missing",
                "comment": f"id not found; hint={name_hint}",
            })
            continue
        if pre_row["quality_tier"] != "S":
            per_row_log.append({
                "id": id_, "subset": subset_label, "status": "skip-not-tier-S",
                "current_tier": pre_row["quality_tier"], "comment": comment,
            })
            continue

        set_clauses: list[str] = []
        params: list = []
        updates_this_row: dict = {"id": id_, "subset": subset_label,
                                  "canonical_name": pre_row["canonical_name"],
                                  "named_mythological_match": pre_row["named_mythological_match"],
                                  "comment": comment, "changes": {}}

        # Only overwrite 'unknown' for cultural_lineage_canonical
        if (pre_row["cultural_lineage_canonical"] or "unknown") == "unknown":
            set_clauses.append("cultural_lineage_canonical = ?")
            params.append(lineage)
            updates_this_row["changes"]["cultural_lineage_canonical"] = {
                "before": pre_row["cultural_lineage_canonical"], "after": lineage,
            }
            fields_updated += 1
        else:
            updates_this_row["changes"]["cultural_lineage_canonical"] = {
                "before": pre_row["cultural_lineage_canonical"], "after": pre_row["cultural_lineage_canonical"],
                "preserved": True,
            }

        # Only overwrite 'unknown' for historical_period_canonical
        if (pre_row["historical_period_canonical"] or "unknown") == "unknown":
            set_clauses.append("historical_period_canonical = ?")
            params.append(period)
            updates_this_row["changes"]["historical_period_canonical"] = {
                "before": pre_row["historical_period_canonical"], "after": period,
            }
            fields_updated += 1
        else:
            # Special override case: id=1676 (Tutankhamun) currently 'medieval' (regex misfire on YEAR_RE)
            # and id=107/634 currently 'contemporary' (regex misfire). The dispatch authorizes elrond
            # judgment on these; comment explicitly flags the override.
            if "override" in comment.lower():
                set_clauses.append("historical_period_canonical = ?")
                params.append(period)
                updates_this_row["changes"]["historical_period_canonical"] = {
                    "before": pre_row["historical_period_canonical"], "after": period,
                    "override_reason": "regex_misfire_corrected",
                }
                fields_updated += 1
            else:
                updates_this_row["changes"]["historical_period_canonical"] = {
                    "before": pre_row["historical_period_canonical"], "after": pre_row["historical_period_canonical"],
                    "preserved": True,
                }

        # Bump confidence to 0.9 for SC-1 backfilled items (elrond-asserted from named-bearer)
        current_conf = pre_row["cultural_lineage_confidence"] or 0.0
        if set_clauses and current_conf < 0.9:
            set_clauses.append("cultural_lineage_confidence = ?")
            params.append(0.9)
            updates_this_row["changes"]["cultural_lineage_confidence"] = {
                "before": current_conf, "after": 0.9,
            }

        if not set_clauses:
            updates_this_row["status"] = "no-op-already-clean"
            per_row_log.append(updates_this_row)
            continue

        params.append(id_)
        c.execute(
            f"UPDATE weapon_knowledge_entries SET {', '.join(set_clauses)} WHERE id = ?",
            params,
        )
        updates_this_row["status"] = "updated"
        per_row_log.append(updates_this_row)
        rows_touched += 1

    return rows_touched, fields_updated, per_row_log


def post_audit(c: sqlite3.Connection) -> dict:
    """Post-update audit: verify Subset A/B no longer have unknown lineage AND unknown period."""
    audit: dict = {}
    audited_ids = [b[0] for b in SUBSET_A_BACKFILLS] + [b[0] for b in SUBSET_B_BACKFILLS]
    placeholder = ",".join("?" for _ in audited_ids)
    cur = c.execute(
        f"""SELECT id, canonical_name, cultural_lineage_canonical, historical_period_canonical
            FROM weapon_knowledge_entries
            WHERE id IN ({placeholder})""",
        audited_ids,
    )
    still_unknown_lineage: list[dict] = []
    still_unknown_period: list[dict] = []
    for r in cur.fetchall():
        row = dict(r)
        if row["cultural_lineage_canonical"] == "unknown":
            still_unknown_lineage.append(row)
        if row["historical_period_canonical"] == "unknown":
            still_unknown_period.append(row)

    audit["audited_ids_count"] = len(audited_ids)
    audit["still_unknown_cultural_lineage"] = still_unknown_lineage
    audit["still_unknown_historical_period"] = still_unknown_period
    audit["clean_count"] = len(audited_ids) - max(
        len(still_unknown_lineage), len(still_unknown_period),
    )

    # Sanity: post-counts overall
    counts: dict = {}
    counts["tier_S_named_myth_unknown_remaining"] = c.execute(
        """SELECT COUNT(*) FROM weapon_knowledge_entries
           WHERE quality_tier='S' AND named_mythological_match IS NOT NULL
             AND (cultural_lineage_canonical='unknown' OR historical_period_canonical='unknown')"""
    ).fetchone()[0]
    audit["counts"] = counts

    return audit


def main() -> None:
    t0 = datetime.utcnow().isoformat()
    print(f"[sc1_backfill] start: {t0}")
    print(f"[sc1_backfill] DB: {DB_PATH}")
    print(f"[sc1_backfill] Subset A target rows: {len(SUBSET_A_BACKFILLS)}")
    print(f"[sc1_backfill] Subset B target rows: {len(SUBSET_B_BACKFILLS)}")
    print(f"[sc1_backfill] Subset C deferred (NOT updated): {len(SUBSET_C_DEFERRED)}")

    c = conn_open()
    try:
        # Pre-state for clean before/after sample
        all_ids = [b[0] for b in SUBSET_A_BACKFILLS] + [b[0] for b in SUBSET_B_BACKFILLS]
        pre = fetch_pre_state(c, all_ids)

        a_touched, a_fields, a_log = apply_backfill(c, SUBSET_A_BACKFILLS, "A")
        b_touched, b_fields, b_log = apply_backfill(c, SUBSET_B_BACKFILLS, "B")

        c.commit()
        print(f"[sc1_backfill] Subset A: {a_touched} rows touched, {a_fields} field updates")
        print(f"[sc1_backfill] Subset B: {b_touched} rows touched, {b_fields} field updates")

        audit = post_audit(c)
        print(f"[sc1_backfill] post-audit: {audit['clean_count']}/{audit['audited_ids_count']} backfilled rows clean")
        print(f"[sc1_backfill] Tier-S named-myth unknown remaining (Subset C): "
              f"{audit['counts']['tier_S_named_myth_unknown_remaining']}")

        # Build sample (5 from A, 5 from B) for completion record
        sample = []
        for entry in (a_log[:5] + b_log[:5]):
            sample.append(entry)

        log_payload = {
            "started_at": t0,
            "finished_at": datetime.utcnow().isoformat(),
            "db_path": DB_PATH.as_posix(),
            "subset_a_target_count": len(SUBSET_A_BACKFILLS),
            "subset_b_target_count": len(SUBSET_B_BACKFILLS),
            "subset_c_deferred_count": len(SUBSET_C_DEFERRED),
            "subset_a_rows_touched": a_touched,
            "subset_a_field_updates": a_fields,
            "subset_b_rows_touched": b_touched,
            "subset_b_field_updates": b_fields,
            "audit": audit,
            "before_after_sample_10": sample,
            "subset_a_full_log": a_log,
            "subset_b_full_log": b_log,
            "subset_c_deferred_list": [
                {"id": x[0], "canonical_name": x[1], "source_library": x[2], "comment": x[3]}
                for x in SUBSET_C_DEFERRED
            ],
        }
        LOG_PATH.write_text(json.dumps(log_payload, indent=2, default=str))
        print(f"[sc1_backfill] log written: {LOG_PATH}")
    finally:
        c.close()


if __name__ == "__main__":
    main()
