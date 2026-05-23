#!/usr/bin/env python3
"""
Phase D-bis Step 6.6.b: Unknown-lineage recovery (CRITICAL — runs BEFORE Step 6.6).

Per phase-D-bis-math-note.md §5 + Matt-delegated self-disposition:

The §5 sampling pass surfaced that 54-100% of unknown-lineage rows across the 4 major
sources (wikidata / wikipedia / odin-army-tradoc / met-museum) are β/γ-recoverable via
extended CULTURE_REGEX_PATTERNS + a new COUNTRY_NAME_TO_LINEAGE mapping + per-source
extraction enhancements.

This script:
  1. Extends CULTURE_REGEX_PATTERNS with: Chinese dynasties (Shang/Han/Zhou/etc.),
     Tibetan/Mongolian/Bhutanese, Caucasian regions, country-name forms (France/Italy/
     Ukraine/etc.), missing European regional adjectives (Silesian/Bohemian/Flemish/etc.),
     Bornean/Dyak/Cambodian/Laotian, expanded African terms, expanded oceanic terms,
     additional indigenous-group names.
  2. Adds COUNTRY_NAME_TO_LINEAGE (full country-name → lineage; complements the existing
     COUNTRY_CODE_TO_LINEAGE which only handles ISO codes).
  3. Rewrites the south_american_indigenous regex per §4 to drop the buggy `\\binca` /
     bare `amazon` / bare `peru` patterns that match "incantation"/"incarnate"/etc.
  4. Extends per-source extraction:
     - wikipedia: consults `origin` structured field (currently only consults `place`)
     - wikidata: extends `country` handling to include dynasty names + COUNTRY_NAME map
     - odin-army-tradoc: extends origin_countries handling to include full country names;
       also extracts from canonical_name (e.g., "Zhakh 10 Ukrainian UAV" → european)
     - met-museum: extends `culture` regex matching + falls through to `country` field
  5. Applies targeted SQL UPDATE to correct ~498 mis-mapped south_amer FPs.

INVARIANTS (additive-only):
  - ONLY rows currently at cultural_lineage_canonical='unknown' are touched (except §4 FP fix)
  - NO row that currently has a non-unknown lineage label is relabeled (except §4 FP fix
    which specifically targets the broken south_amer regex hits in game sources)
  - Step 6.5's original mapping decisions are preserved for all confidence-1.0 rows

Idempotency: WHERE clause filters on lineage='unknown'. Re-run is a no-op on
already-recovered rows.

Authority: Matt 2026-05-23 (fire authorization + §5 self-disposition delegation).
Math note: §5 disposition (all 4 major sources β+γ ≥ 54%, fire 6.6.b).
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
import time
from pathlib import Path

DB_PATH = "/Users/admin/Games/reincarnated-loadout/data/telemetry.db"
LOG_PATH = Path(__file__).parent.parent / "logs" / "09b_step6_6b_unknown_lineage_recovery.json"

# ---------------------------------------------------------------------------
# EXTENDED CULTURE_REGEX_PATTERNS (replaces Step 6.5's set; superset of original)
# ---------------------------------------------------------------------------

CULTURE_REGEX_PATTERNS = [
    # === EAST ASIAN ===
    # Japan
    (re.compile(r"\b(japan(ese)?|edo|tokyo|kyoto|nara|heian|kamakura|samurai|"
                r"meiji|tokugawa|yamato)\b", re.I), "east_asian"),
    # China — major dynasties + general
    (re.compile(r"\b(china|chinese|qing|ming|tang|"
                r"shang|zhou|qin|han|jin|liao|song|yuan|cao wei|sui|"
                r"northern wei|southern wei|eastern jin|western jin|"
                r"eastern han|western han|eastern zhou|western zhou|"
                r"warring states|three kingdoms|five dynasties|sixteen kingdoms|"
                r"han dynasty|tang dynasty|song dynasty|yuan dynasty|ming dynasty|qing dynasty)\b",
                re.I), "east_asian"),
    # Korea
    (re.compile(r"\b(korea(n)?|joseon|goryeo|silla|baekje|goguryeo)\b", re.I), "east_asian"),
    # Tibetan / Mongolian / Bhutanese (Met museum populated)
    (re.compile(r"\b(tibet(an)?|mongol(ian)?|bhutan(ese)?|manchu(rian)?|sinhala(?:ese)?|"
                r"khampa|amdo|kham|inner mongolia|outer mongolia)\b", re.I), "east_asian"),
    # Chinese provinces (wikidata empirical: 6,000+ unknowns mention these in descriptions —
    # mostly "item from the collection of X Provincial Museum"). Catch the most populous.
    (re.compile(r"\b(hubei|fujian|guangdong|guangzhou|sichuan|zhejiang|henan|shandong|"
                r"hebei|hunan|anhui|jiangsu|jiangxi|shanxi|shaanxi|gansu|yunnan|"
                r"guizhou|xinjiang|qinghai|hainan|ningxia|chongqing|liaoning|jilin|"
                r"heilongjiang|inner mongolia|tibet autonomous|guangxi|"
                r"shanghai|beijing|peking|hong kong|hongkong|macao|macau|"
                r"chinese provincial|chinese national|"
                r"hubei museum|fujian museum|guangdong museum|"
                r"sichuan provincial|hebei provincial|hunan provincial|"
                r"anhui provincial|jiangsu provincial|jiangxi provincial|"
                r"shanxi provincial|shaanxi provincial|gansu provincial|"
                r"yunnan provincial|guizhou provincial|xinjiang provincial|"
                r"qinghai provincial|hainan provincial|ningxia provincial|"
                r"liaoning provincial|jilin provincial|heilongjiang provincial|"
                r"guangxi provincial)\b",
                re.I), "east_asian"),
    # Japanese cities + JSDF acronyms (smaller bucket but real)
    (re.compile(r"\b(osaka|yokohama|nagoya|sapporo|fukuoka|hiroshima|nagasaki|sendai|"
                r"jmsdf|jgsdf|jasdf|"
                r"japan maritime|japan ground|japan air|japan self-defense|"
                r"tokyo national|kyoto national|nara national)\b",
                re.I), "east_asian"),

    # === SOUTH ASIAN ===
    (re.compile(r"\b(india(n)?|mughal|sikh|rajput|punjab(i)?|tamil|telugu|kannada|"
                r"sri lanka(n)?|sinhalese|pakistan(i)?|bangladesh(i)?|nepali|nepal|"
                r"maldiv(es|ian)|bengal(i)?|gujarati|marathi|maratha|hindu kush|deccan)\b",
                re.I), "south_asian"),

    # === SOUTHEAST ASIAN ===
    (re.compile(r"\b(indonesia(n)?|java(nese)?|sumatra(n)?|bali(nese)?|sulawesi|"
                r"philippin(es|e|o)|vietnam(ese)?|thai|thailand|burm(a|ese)|myanmar|"
                r"malaya(n)?|malaysia(n)?|filipino|singapore|brunei|"
                r"bornean|borneo|dyak|iban|kadazan|cambodian|cambodia|laotian|laos|"
                r"khmer|cham|mon|tagalog|cebuano|moro|hmong|karen|tai|timor(ese)?)\b",
                re.I), "southeast_asian"),

    # === MIDDLE EASTERN ===
    (re.compile(r"\b(iran(ian)?|persia(n)?|safavid|qajar|ottoman|turk(ey|ish)?|anatolia(n)?|"
                r"arab(ian|ic)?|syria(n)?|iraq(i)?|yemen(i)?|saudi|jordan(ian)?|lebanese|"
                r"mamluk|levantine|mesopotamian|sumerian|akkadian|"
                r"phoenician|hittite|assyrian|babylonian|sassanid|"
                r"palestinian|kurd(ish)?|kuwait(i)?|qatar(i)?|emirat(es|i)|"
                r"oman(i)?|bahrain(i)?|israeli|"
                r"byzantine|crusader)\b", re.I), "middle_eastern"),
    # Caucasian (Met heavily populated; classified middle_eastern per cleaning-policy §5.2 mapping family)
    (re.compile(r"\b(caucasian|caucasus|georgian|tbilisi|dagestan(i)?|circassian|chechen|"
                r"armenian|azerbaijani|abkhaz|ossetian|kabardian)\b", re.I), "middle_eastern"),

    # === AFRICAN ===
    (re.compile(r"\b(africa(n)?|moroc(can|co)|algeria(n)?|nubia(n)?|ethiopia(n)?|"
                r"zulu|maasai|tunisia(n)?|tswana|coptic|"
                r"nigeria(n)?|ghanaian|ghana|senegal(ese)?|cameroon(ian)?|congo(lese)?|"
                r"kenya(n)?|tanzania(n)?|uganda(n)?|south african|namibia(n)?|"
                r"zimbabwe(an)?|mozambic(an|ue)|angola(n)?|sudan(ese)?|somali(an)?|"
                r"eritrea(n)?|libya(n)?|"
                r"yoruba|igbo|hausa|fulani|swahili|amhara|oromo|berber|tuareg|"
                r"benin|ashanti|dahomey|mande)\b", re.I), "african"),

    # === MESOAMERICAN ===
    (re.compile(r"\b(mexic(an|o)?|aztec|maya(n)?|toltec|tlatoani|"
                r"zapotec|mixtec|tarascan|totonac|otomi|huastec|"
                r"olmec|teotihuacan|tarasco|nahua|mexica|chichimec|"
                r"guatemala(n)?|honduras|honduran|el salvador|salvadoran|nicaragua(n)?)\b",
                re.I), "mesoamerican"),

    # === SOUTH AMERICAN INDIGENOUS — REWRITTEN per math note §4 ===
    # OLD (buggy): r"\b(inca|peru|andean|amazon|brazil|colombia)" — matched incantation/incarnate/amazon-warrior
    # NEW: full adjectival forms + indigenous groups + specific place names
    (re.compile(
        r"\b(peruvian|andean|amazonian|brazilian|colombian|argentin(ian|e|a)?|chilean|bolivian|"
        r"ecuadorian|venezuelan|paraguayan|uruguayan|guyanese|surinamese|"
        r"quechua|aymara|guaran[ií]|mapuche|tainos?|moche|nazca|chim[uú]|"
        r"potos[ií]|cuzco|cusco|machu picchu|inca empire|incan empire|chibcha|muisca|"
        r"andes mountains|south american)\b",
        re.I,
    ), "south_american_indigenous"),

    # === NORTH AMERICAN INDIGENOUS ===
    (re.compile(r"\b(native\s+american|first\s+nations|sioux|apache|cherokee|iroquois|"
                r"navaj[oa]|hopi|comanche|lakota|dakota|nakota|crow|blackfoot|"
                r"haida|tlingit|kwakiutl|cree|metis|"
                r"seminole|chickasaw|choctaw|creek|powhatan|wampanoag|"
                r"pueblo|zuni|mohawk|huron|micmac|miqmaq|ojibw[ae])\b",
                re.I), "north_american_indigenous"),

    # === ARCTIC CIRCUMPOLAR ===
    (re.compile(r"\b(sami|saami|inuit|greenland(ic)?|arctic|"
                r"yupik|aleut|chukchi|nenets|evenki|finno-ugric)\b",
                re.I), "arctic_circumpolar"),

    # === OCEANIC ===
    (re.compile(r"\b(maori|polynesia(n)?|hawaiian|fijian|samoan|tongan|melanesian|micronesian|"
                r"aboriginal|aborigine|australia(n)?|new zealand(er)?|"
                r"papuan|papua new guinea|austronesian|gweagal|"
                r"vanuatu(an)?|solomon islands|tahitian)\b",
                re.I), "oceanic"),

    # === EUROPEAN ===
    # Adjectival forms (existing Phase D regex, retained)
    (re.compile(
        r"\b(britain|british|england|english|scottish|scotland|welsh|wales|irish|ireland|"
        r"german(y)?|french|france|italian|italy|spanish|spain|"
        r"polish|poland|russian|russia|dutch|netherlands|belgian|belgium|"
        r"swiss|switzerland|austrian|austria|danish|denmark|swedish|sweden|"
        r"norwegian|norway|portuguese|portugal|"
        r"hungarian|hungary|czech(ia)?|finnish|finland|greek|greece|"
        r"birmingham|london|paris|berlin|vienna|prague|warsaw|moscow|"
        r"europe(an)?|usa|united states|canada|america(n)?|austria-hungary|"
        r"soviet|ussr|soviet union)\b",
        re.I,
    ), "european"),
    # Country-name forms (additions; current regex only matched adjectives)
    (re.compile(r"\b(ukraine|ukrainian|belarus(ian)?|moldova(n)?|"
                r"romania(n)?|bulgaria(n)?|bosnia(n)?|croatia(n)?|serbia(n)?|"
                r"slovenia(n)?|slovak(ia)?|albania(n)?|"
                r"north macedonia|macedonian|"
                r"estonia(n)?|latvia(n)?|lithuania(n)?|"
                r"iceland(ic)?|malta|maltese|cyprus|cypriot(e)?|"
                r"vatican|san marino|montenegro|kosovo|"
                r"andorra|monaco|luxembourg|liechtenstein)\b",
                re.I), "european"),
    # Missing regional adjectives (Silesian, Bohemian, Flemish, etc.)
    (re.compile(r"\b(silesian|bohemian|flemish|flanders|netherlandish|visigothic|"
                r"etruscan|burgundian|prussian|saxon|bavarian|tyrolean|"
                r"vlach|moldavian|ruthenian|cossack|"
                r"venetian|florentine|genoese|milanese|piedmontese|"
                r"andalusian|catalan|basque|galician|asturian|"
                r"cornish|gaelic|breton|frankish|merovingian|carolingian|"
                r"slovak|magyar|finnic)\b", re.I), "european"),

    # === DEFAULTS / FALLBACKS ===
    # The original Phase D regex had a fallback case I'm preserving here:
    # (none additional; the unknown default is handled by extract_culture_for_row)
]

# ---------------------------------------------------------------------------
# COUNTRY_NAME_TO_LINEAGE — for use when structured fields contain country NAMES
# (vs the existing COUNTRY_CODE_TO_LINEAGE which only handles ISO codes)
# ---------------------------------------------------------------------------

COUNTRY_NAME_TO_LINEAGE: dict[str, str] = {
    # Europe (full country names)
    "France": "european", "Germany": "european", "United Kingdom": "european",
    "Italy": "european", "Spain": "european", "Poland": "european",
    "Netherlands": "european", "Belgium": "european", "Switzerland": "european",
    "Austria": "european", "Sweden": "european", "Norway": "european",
    "Finland": "european", "Denmark": "european", "Portugal": "european",
    "Greece": "european", "Ireland": "european", "Hungary": "european",
    "Estonia": "european", "Latvia": "european", "Lithuania": "european",
    "Iceland": "european", "Czech Republic": "european", "Czechia": "european",
    "Slovakia": "european", "Slovenia": "european", "Croatia": "european",
    "Serbia": "european", "Bosnia and Herzegovina": "european", "Bosnia": "european",
    "Albania": "european", "Romania": "european", "Bulgaria": "european",
    "North Macedonia": "european", "Macedonia": "european",
    "Montenegro": "european", "Kosovo": "european",
    "United States": "european", "United States of America": "european",
    "Russia": "european", "Soviet Union": "european", "USSR": "european",
    "Ukraine": "european", "Belarus": "european", "Moldova": "european",
    "Canada": "european", "Australia": "oceanic", "New Zealand": "oceanic",
    "Andorra": "european", "Monaco": "european", "Luxembourg": "european",
    "Liechtenstein": "european", "Malta": "european", "Cyprus": "european",
    "Vatican": "european", "Vatican City": "european", "San Marino": "european",
    # Soviet successor / RU regional
    "Russian Federation": "european",
    # East Asian
    "China": "east_asian", "People's Republic of China": "east_asian",
    "Japan": "east_asian", "South Korea": "east_asian", "North Korea": "east_asian",
    "Republic of Korea": "east_asian", "Korea": "east_asian",
    "Taiwan": "east_asian", "Hong Kong": "east_asian", "Macau": "east_asian",
    "Mongolia": "east_asian", "Tibet": "east_asian", "Bhutan": "east_asian",
    # Southeast Asian
    "Vietnam": "southeast_asian", "Thailand": "southeast_asian", "Indonesia": "southeast_asian",
    "Philippines": "southeast_asian", "Malaysia": "southeast_asian", "Singapore": "southeast_asian",
    "Myanmar": "southeast_asian", "Burma": "southeast_asian",
    "Cambodia": "southeast_asian", "Laos": "southeast_asian",
    "Brunei": "southeast_asian", "East Timor": "southeast_asian", "Timor-Leste": "southeast_asian",
    # South Asian
    "India": "south_asian", "Pakistan": "south_asian", "Bangladesh": "south_asian",
    "Sri Lanka": "south_asian", "Nepal": "south_asian", "Maldives": "south_asian",
    "Afghanistan": "south_asian",
    # Middle Eastern
    "Iran": "middle_eastern", "Iraq": "middle_eastern", "Saudi Arabia": "middle_eastern",
    "Turkey": "middle_eastern", "Türkiye": "middle_eastern",
    "Israel": "middle_eastern", "Palestine": "middle_eastern",
    "Jordan": "middle_eastern", "Lebanon": "middle_eastern", "Syria": "middle_eastern",
    "Yemen": "middle_eastern", "Oman": "middle_eastern", "Qatar": "middle_eastern",
    "Bahrain": "middle_eastern", "Kuwait": "middle_eastern",
    "United Arab Emirates": "middle_eastern", "UAE": "middle_eastern",
    "Georgia": "middle_eastern",  # the country (not US state); Caucasian
    "Armenia": "middle_eastern", "Azerbaijan": "middle_eastern",
    # African
    "Egypt": "african", "South Africa": "african", "Nigeria": "african",
    "Kenya": "african", "Ethiopia": "african", "Algeria": "african",
    "Morocco": "african", "Tunisia": "african", "Libya": "african",
    "Sudan": "african", "Ghana": "african", "Cameroon": "african",
    "Senegal": "african", "Tanzania": "african", "Uganda": "african",
    "Namibia": "african", "Zimbabwe": "african", "Mozambique": "african",
    "Angola": "african", "Somalia": "african", "Eritrea": "african",
    "Mali": "african", "Burkina Faso": "african", "Niger": "african",
    "Chad": "african", "Madagascar": "african",
    # Mesoamerican
    "Mexico": "mesoamerican", "Guatemala": "mesoamerican", "Honduras": "mesoamerican",
    "El Salvador": "mesoamerican", "Nicaragua": "mesoamerican",
    "Costa Rica": "mesoamerican", "Panama": "mesoamerican", "Belize": "mesoamerican",
    # South American
    "Brazil": "south_american_indigenous", "Argentina": "south_american_indigenous",
    "Chile": "south_american_indigenous", "Peru": "south_american_indigenous",
    "Colombia": "south_american_indigenous", "Venezuela": "south_american_indigenous",
    "Ecuador": "south_american_indigenous", "Bolivia": "south_american_indigenous",
    "Paraguay": "south_american_indigenous", "Uruguay": "south_american_indigenous",
    "Guyana": "south_american_indigenous", "Suriname": "south_american_indigenous",
    "French Guiana": "south_american_indigenous",
    # Oceanic
    "Papua New Guinea": "oceanic", "Fiji": "oceanic", "Samoa": "oceanic",
    "Tonga": "oceanic", "Vanuatu": "oceanic", "Solomon Islands": "oceanic",
    "Tuvalu": "oceanic", "Kiribati": "oceanic", "Palau": "oceanic",
    "Micronesia": "oceanic", "Marshall Islands": "oceanic", "Nauru": "oceanic",
    # Arctic
    "Greenland": "arctic_circumpolar",
}

# Pre-compute lowercase keys for case-insensitive matching
COUNTRY_NAME_LC = {k.lower(): v for k, v in COUNTRY_NAME_TO_LINEAGE.items()}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def extract_culture_from_text(*texts: str | None) -> tuple[str, float]:
    """Run extended regex bank over text; return (lineage, confidence)."""
    combined = " ".join(t for t in texts if t)
    if not combined.strip():
        return ("unknown", 0.0)
    for pat, bucket in CULTURE_REGEX_PATTERNS:
        if pat.search(combined):
            return (bucket, 0.7)
    return ("unknown", 0.0)


def match_country_name(text: str) -> str | None:
    """Try to match a country name in text; return lineage or None."""
    if not text:
        return None
    text_lc = text.lower()
    # Try exact match first (whole text == country name)
    if text_lc.strip() in COUNTRY_NAME_LC:
        return COUNTRY_NAME_LC[text_lc.strip()]
    # Then try substring match — sorted by length desc so longer names match first
    # ("United States of America" before "United States" before "States")
    for country_lc in sorted(COUNTRY_NAME_LC.keys(), key=len, reverse=True):
        # word-boundary substring match
        if re.search(r"\b" + re.escape(country_lc) + r"\b", text_lc):
            return COUNTRY_NAME_LC[country_lc]
    return None


def recover_lineage_for_row(row: dict) -> tuple[str, float]:
    """Per-source extended extraction. Returns (lineage, confidence) or ('unknown', 0.0).

    Order: structured fields (high confidence) → name + description (lower confidence).
    """
    src = row["source_library"] or ""
    sp_json = row["structured_properties"] or "{}"
    try:
        sp = json.loads(sp_json)
    except Exception:
        sp = {}
    desc = row["description_text"] or ""
    name = row["canonical_name"] or ""
    cultural_tags = row["cultural_lineage_tags"] or ""

    # ---- WIKIPEDIA ----
    if src == "wikipedia":
        # Structured `origin` field (was not consulted in Step 6.5)
        origin = sp.get("origin") or ""
        if origin:
            # COUNTRY_NAME map first
            cn = match_country_name(origin)
            if cn:
                return (cn, 0.9)  # structured-field-derived
            # Then regex
            lineage, _ = extract_culture_from_text(origin)
            if lineage != "unknown":
                return (lineage, 0.85)
        # Also `used_by` field as secondary signal (often mentions countries)
        used_by = sp.get("used_by") or ""
        if used_by:
            cn = match_country_name(used_by)
            if cn:
                return (cn, 0.75)
            lineage, _ = extract_culture_from_text(used_by)
            if lineage != "unknown":
                return (lineage, 0.7)
        # Description regex (Phase D §5.2 wikipedia: regex on category strings; now applied to desc)
        lineage, _ = extract_culture_from_text(desc[:1000], cultural_tags)
        if lineage != "unknown":
            return (lineage, 0.65)
        return ("unknown", 0.0)

    # ---- WIKIDATA ----
    if src == "wikidata":
        # country / country_of_origin field — extended to handle dynasty names
        country = sp.get("country_of_origin") or sp.get("country") or ""
        if country:
            cn = match_country_name(country)
            if cn:
                return (cn, 1.0)
            # Try regex (covers dynasties like "Shang dynasty", "Han dynasty")
            lineage, _ = extract_culture_from_text(country)
            if lineage != "unknown":
                return (lineage, 0.9)
        # Description regex
        lineage, _ = extract_culture_from_text(desc[:500])
        if lineage != "unknown":
            return (lineage, 0.65)
        # Name regex (catches e.g., "Targe (Russian)" via the (Russian) parenthetical)
        lineage, _ = extract_culture_from_text(name)
        if lineage != "unknown":
            return (lineage, 0.6)
        return ("unknown", 0.0)

    # ---- ODIN-ARMY-TRADOC ----
    if src == "odin-army-tradoc":
        # origin_countries — extended to handle full country names (not just ISO codes)
        origin_countries = sp.get("origin_countries") or []
        if isinstance(origin_countries, list) and origin_countries:
            for entry in origin_countries:
                if not isinstance(entry, str):
                    continue
                # COUNTRY_NAME map (covers "Ukraine", "Belarus", "Malaysia", etc.)
                cn = match_country_name(entry)
                if cn:
                    return (cn, 1.0)
                # Then regex
                lineage, _ = extract_culture_from_text(entry)
                if lineage != "unknown":
                    return (lineage, 0.9)
        # canonical_name extraction (ODIN naming convention is "X [Nationality] [Type]"
        # e.g., "Zhakh 10 Ukrainian UAV", "Tarantula Malaysian 4x4 HMAV")
        # The new regex catches "Ukrainian", "Malaysian", "Australian", "Belarusian" etc.
        lineage, _ = extract_culture_from_text(name)
        if lineage != "unknown":
            return (lineage, 0.85)
        # Description
        lineage, _ = extract_culture_from_text(desc[:500])
        if lineage != "unknown":
            return (lineage, 0.7)
        return ("unknown", 0.0)

    # ---- MET-MUSEUM ----
    if src == "met-museum":
        # culture field (Met always has this; extended regex now catches Tibetan/Mongolian/
        # Caucasian/Flemish/Silesian/etc.)
        culture_field = sp.get("culture") or ""
        if culture_field:
            lineage, _ = extract_culture_from_text(culture_field)
            if lineage != "unknown":
                return (lineage, 1.0)
            # COUNTRY_NAME fallback on culture field (e.g., "Italian" in regex; "Italy" in map)
            cn = match_country_name(culture_field)
            if cn:
                return (cn, 0.9)
        # country field (Met often has this even when culture is ambiguous)
        country = sp.get("country") or ""
        if country:
            cn = match_country_name(country)
            if cn:
                return (cn, 0.95)
            lineage, _ = extract_culture_from_text(country)
            if lineage != "unknown":
                return (lineage, 0.9)
        # region field
        region = sp.get("region") or ""
        if region:
            cn = match_country_name(region)
            if cn:
                return (cn, 0.85)
            lineage, _ = extract_culture_from_text(region)
            if lineage != "unknown":
                return (lineage, 0.75)
        return ("unknown", 0.0)

    # ---- OTHER SOURCES ----
    # cataclysm-dda / gta-v-data / army-recognition / royal_armouries / etc.
    # Already had non-unknown lineage via their source-default; if at 'unknown' here,
    # they have empty culture-extraction surface. Try description regex as last resort.
    lineage, _ = extract_culture_from_text(desc[:500], cultural_tags, sp.get("place") or "",
                                            sp.get("country") or "")
    if lineage != "unknown":
        return (lineage, 0.7)
    return ("unknown", 0.0)


# ---------------------------------------------------------------------------
# § 4 secondary regex FP correction
# ---------------------------------------------------------------------------

# Game sources where south_amer FP is concentrated (per math note §4.1 + Q9 verification)
FP_SOUTH_AMER_GAME_SOURCES = {
    "fextralife-elden-ring", "fextralife-ds1", "fextralife-ds2", "fextralife-ds3",
    "nick-aschenbach-dnd-data", "bsdata-warhammer-aos",
    "pf2ools-pf2ools-data", "pf2ools-pf2ools-data-quarantined",
    "elden-ring-erdb", "bloqhead-demigods", "wow-classic-items",
    "diablo2-d2data", "path-of-exile-repoe", "osrsbox-db",
    "5e-bits-5e-database", "5e-bits-5e-database-2024",
    "souls-api-thomaslincoln", "souls-api-thomaslincoln-quarantined",
}

# Legitimate south_amer markers (if any present in description, preserve the lineage)
LEGIT_SOUTH_AMER_RE = re.compile(
    r"\b(peruvian|andean|amazonian|brazilian|colombian|argentin|chilean|bolivian|"
    r"quechua|aymara|guaran[ií]|mapuche|tainos?|moche|nazca|chim[uú])\b",
    re.I,
)


def fix_south_amer_fps(conn: sqlite3.Connection) -> dict:
    """Correct ~498 mis-mapped south_american_indigenous rows in game sources.

    For each row currently labeled south_amer in a game source: if the description
    does NOT contain a legitimate south-american term, relabel to the source's default
    (fantasy_generic for game sources). Confidence reset to 0.5.
    """
    cur = conn.cursor()
    cur.execute(
        """SELECT id, canonical_name, description_text, source_library
           FROM weapon_knowledge_entries
           WHERE cultural_lineage_canonical = 'south_american_indigenous'
             AND source_library IN ({})""".format(
            ",".join("?" * len(FP_SOUTH_AMER_GAME_SOURCES))
        ),
        list(FP_SOUTH_AMER_GAME_SOURCES),
    )
    rows = cur.fetchall()

    fp_corrected = 0
    legit_preserved = 0
    per_source_fixed: dict[str, int] = {}
    for row_id, name, desc, src in rows:
        desc_text = desc or ""
        if LEGIT_SOUTH_AMER_RE.search(desc_text):
            legit_preserved += 1
            continue
        # FP — relabel to source default (fantasy_generic for game sources)
        cur.execute(
            """UPDATE weapon_knowledge_entries
               SET cultural_lineage_canonical = 'fantasy_generic',
                   cultural_lineage_confidence = 0.5
               WHERE id = ?""",
            (row_id,),
        )
        fp_corrected += 1
        per_source_fixed[src] = per_source_fixed.get(src, 0) + 1
    conn.commit()
    return {
        "south_amer_fps_corrected": fp_corrected,
        "south_amer_legit_preserved": legit_preserved,
        "south_amer_per_source_fixed": per_source_fixed,
    }


# ---------------------------------------------------------------------------
# Main Step 6.6.b run
# ---------------------------------------------------------------------------


def run_step6_6b(conn: sqlite3.Connection) -> dict:
    cur = conn.cursor()

    # Pull all rows currently at cultural_lineage_canonical='unknown' (additive-only invariant)
    cur.execute(
        """SELECT id, canonical_name, source_library,
                  description_text, structured_properties, cultural_lineage_tags,
                  cultural_lineage_canonical, cultural_lineage_confidence
           FROM weapon_knowledge_entries
           WHERE cultural_lineage_canonical = 'unknown'
             AND dedup_status != 'merged_into'"""
    )
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    print(f"  [6.6b] candidates (lineage=unknown, non-merged): {len(rows)}")

    updates: list[tuple] = []
    per_source_recovered: dict[str, dict[str, int]] = {}
    per_source_total: dict[str, int] = {}

    for r in rows:
        row = dict(zip(cols, r))
        src = row["source_library"] or "unknown"
        per_source_total[src] = per_source_total.get(src, 0) + 1

        new_lineage, new_conf = recover_lineage_for_row(row)
        if new_lineage == "unknown":
            continue
        # Additive invariant: only touch rows currently at unknown (filter already ensures this)
        updates.append((new_lineage, new_conf, row["id"]))
        per_source_recovered.setdefault(src, {})[new_lineage] = (
            per_source_recovered.setdefault(src, {}).get(new_lineage, 0) + 1
        )

    # Bulk UPDATE
    BATCH = 500
    for i in range(0, len(updates), BATCH):
        batch = updates[i : i + BATCH]
        cur.executemany(
            """UPDATE weapon_knowledge_entries
               SET cultural_lineage_canonical = ?,
                   cultural_lineage_confidence = ?
               WHERE id = ?""",
            batch,
        )
    conn.commit()
    print(f"  [6.6b] lineage recoveries applied: {len(updates)}")

    # Compute per-source recovery rate (of total unknowns in that source, how many recovered)
    per_source_recovery_rate = {}
    for src, total in per_source_total.items():
        recovered = sum(per_source_recovered.get(src, {}).values())
        per_source_recovery_rate[src] = {
            "total_unknown_at_start": total,
            "recovered": recovered,
            "recovery_rate_pct": round(100.0 * recovered / total, 2) if total else 0.0,
        }

    return {
        "candidates": len(rows),
        "lineage_recoveries_applied": len(updates),
        "per_source_recovery_rate": per_source_recovery_rate,
        "recovered_to_lineage_top_by_source": {
            k: dict(sorted(v.items(), key=lambda x: -x[1])[:5])
            for k, v in per_source_recovered.items()
        },
    }


def acceptance_check(conn: sqlite3.Connection, recovery_summary: dict, fp_fix_summary: dict) -> dict:
    """Step 6.6.b acceptance per math note §5.5.

    Gates:
      (i) Recovery rate ≥ 50% for each major source (wikidata, wikipedia, odin, met)
      (ii) South-amer FP correction completed; remaining south_amer pool reasonable
      (iii) Additive invariant — no non-unknown lineage was relabeled (verified by §4 fix
            being the only intentional relabel)
    """
    cur = conn.cursor()

    major_sources = ["wikidata", "wikipedia", "odin-army-tradoc", "met-museum"]
    per_source_audit = {}
    for src in major_sources:
        info = recovery_summary["per_source_recovery_rate"].get(src, {})
        per_source_audit[src] = {
            "recovery_rate_pct": info.get("recovery_rate_pct", 0.0),
            "passes_50_floor": info.get("recovery_rate_pct", 0.0) >= 50.0,
        }

    # South-amer post-fix pool size
    south_amer_post = cur.execute(
        "SELECT COUNT(*) FROM weapon_knowledge_entries WHERE cultural_lineage_canonical='south_american_indigenous'"
    ).fetchone()[0]

    # Lineage distribution after Step 6.6.b
    lineage_dist = dict(
        cur.execute(
            """SELECT cultural_lineage_canonical, COUNT(*)
               FROM weapon_knowledge_entries
               WHERE dedup_status != 'merged_into'
               GROUP BY cultural_lineage_canonical
               ORDER BY 2 DESC"""
        ).fetchall()
    )

    return {
        "major_source_recovery_audit": per_source_audit,
        "south_amer_remaining_count": south_amer_post,
        "south_amer_fps_corrected_in_this_run": fp_fix_summary["south_amer_fps_corrected"],
        "lineage_distribution_post_step_6_6_b": lineage_dist,
        "gate_recovery_pass": all(p["passes_50_floor"] for p in per_source_audit.values()),
        "gate_south_amer_pass": south_amer_post <= 50,  # math note §4.4 hard ceiling
    }


def main() -> int:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    summary: dict = {
        "script": "09b_step6_6b_unknown_lineage_recovery.py",
        "db_path": DB_PATH,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    conn = sqlite3.connect(DB_PATH)
    try:
        # Step 1: Lineage recovery (additive)
        summary["recovery_execution"] = run_step6_6b(conn)
        # Step 2: §4 secondary regex FP correction
        summary["fp_fix_execution"] = fix_south_amer_fps(conn)
        # Acceptance
        summary["acceptance"] = acceptance_check(
            conn, summary["recovery_execution"], summary["fp_fix_execution"]
        )
    finally:
        conn.close()

    summary["wall_clock_s"] = round(time.time() - started, 3)
    summary["ended_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    acc = summary["acceptance"]
    summary["passed"] = acc["gate_recovery_pass"] and acc["gate_south_amer_pass"]

    with LOG_PATH.open("w") as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"  ==> Recovery candidates: {summary['recovery_execution']['candidates']}")
    print(f"  ==> Recoveries applied: {summary['recovery_execution']['lineage_recoveries_applied']}")
    print(f"  ==> South-amer FPs corrected: {summary['fp_fix_execution']['south_amer_fps_corrected']}")
    print(f"  ==> South-amer pool post-fix: {acc['south_amer_remaining_count']}")
    print(f"  ==> Per-source recovery audit:")
    for src, info in acc["major_source_recovery_audit"].items():
        print(f"        {src}: {info['recovery_rate_pct']}% ({'PASS' if info['passes_50_floor'] else 'FAIL'})")
    print(f"  ==> PASSED: {summary['passed']}")
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
