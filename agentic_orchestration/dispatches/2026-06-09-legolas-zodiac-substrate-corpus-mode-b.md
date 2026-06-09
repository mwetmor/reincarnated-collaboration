# Legolas Mode B Commission — Zodiac Substrate Corpus (Cross-Cultural Sky-Tradition Catalogue)

**STATUS:** ACTIVE (in-flight commission)
**Date authored:** 2026-06-09
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-09 directive — "author the legolas commission, and be sure that we capture either a drawing, rendering, mapping, coordinate space (or something similar) across every single star sign which can be used to ensure we get the mapping right"
**Mode:** Mode B (systematic catalogue crawl); background process per Discipline #19
**Audience:** legolas (executor), elrond (downstream curation consumer), gandalf (Q2 mapping consumer), Matt (architectural-pivot decision consumer)
**Companion docs (read first):**
- `agentic_orchestration/gandalf/notes/2026-06-09-next-session-plan-zodiac-cosmograph-design.md` (Matt's pre-pivot zodiac framework state; this commission supersedes Q1 single-culture lean)
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` (the player-facing scene this substrate populates)
- `canonical/story/2026-06-06-atomic-substrate-registry.md` (20 primitive families + Layer 0.5 seasonal-substrate-rotation operator)
- `canonical/story/2026-06-05-cosmograph-pivot.md` § 9 amendment 2026-06-06 (primitive-as-star + kit-as-constellation — pending refinement to primitive-as-glyph + kit-as-constellation post-this-commission)
- `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` (4-mode tagging-vocabulary discipline; this commission MUST apply same rep-audit discipline at substrate-tagging layer)
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` § 3.6 Pattern 6 (axis-as-pre-imposition; this commission IS substrate-led discipline at zodiac layer)

---

## 0. TL;DR

**Mission:** systematic catalogue crawl across all human sky-traditions to produce a substrate-led empirical corpus of named celestial figures (zodiacs, constellations, lunar mansions, decans, asterisms, sky-figures by cultural-tradition). Output feeds gandalf Q2 primitive-mapping work + architectural decision-point on whether kits bind 1:1 to star-signs (if N ≥ ~400) or cluster against fewer anchors (if N < ~400) + cosmograph constellation-anchor layer.

**Critical operational requirement (Matt 2026-06-09 verbatim):** **every single star sign in the corpus MUST carry visual-representation data** — image URL OR star-coordinate-set OR descriptive asterism schematic OR cultural-iconography reference (preferably ≥2 of these per sign). The visual-representation field is **non-negotiable** because (a) Q2 mapping requires visual verification, (b) eventual cosmograph rendering requires visual data, (c) Discipline #25 semantic-layer rep-audit requires visual evidence to validate cultural-tradition claims against substrate-tagging-artifact risk.

**Cultural-sensitivity protocol:** gather what's published in mainstream ethnoastronomy / museum / academic / cultural-heritage-institution literature. FLAG content that source material marks "restricted," "sacred," or "ceremonial-only" with explicit `cultural_sensitivity_flag` field. Default conservative on inclusion — substrate carries metadata; downstream design decides surfacing.

**Estimated wall-clock:** 2-5 days as background workstream (Discipline #19). Per-tradition phased reporting (not all-or-nothing at completion).

---

## 1. Why this commission exists (substrate-led architectural pivot)

Matt 2026-06-09 directive pivoted the zodiac framework from "lock to Western 12-sign + figure out which 5 secondary-axis slots fill the count" to **substrate-led: gather all existing zodiac signs across cultures; let the data vote on count + count-mismatch dissolves naturally**.

This is Pattern 6 (axis-as-pre-imposition retirement, per `legacy-categorical-cleanup-audit-2026-05-22.md` § 3.6) applied to the zodiac framework itself. Western zodiac's 12-sign structure was pre-imposition disguised as natural taxonomy. Substrate-led discipline says **gather all and let the data vote on emergent structure**.

**Architectural decision Matt is pre-thinking** (depends on commission output count):

| Outcome | Architecture |
|---|---|
| **N ≥ ~400 star-signs** | Each KIT binds 1:1 to a star-sign (constellation anchor); primitive-only clusters use a SEPARATE visual register — archaic glyph/symbology/numbering system (Matt-named precedent: **Tal Rasha's tomb sigils from Diablo 2** — abstract Horadric glyphs that are visually distinct from figurative constellations; players "sign" the glyph as input gesture) |
| **N < ~400 star-signs** | Star-signs become CLUSTER anchors; multiple kits per star-sign; primitive-mapping per cluster (Q2 mapping work as originally framed) |

**Either outcome composes natively with:**
- Two-layer + buffer-space architecture (constellation layer + glyph/primitive layer)
- Seasonal-substrate-rotation operator (per-season cultural-tradition rotation — e.g., S1 Western + Celtic; S2 Chinese + Vedic Nakshatra; S3 Mayan + Aztec + Polynesian; etc.)
- Earth-Avatar Creation Moment Architecture § 2.6 (cosmograph IS the literal night sky; cultural-reading per season)
- Marginal-lineage recognition records (sky substrate surfaces coherent cultural-tradition presence where weapon substrate did not — Aboriginal Emu-in-the-Sky, Inuit Caribou Ursa, Andean Yacana, Polynesian navigator stars, Mesoamerican Tzolkin)

**The commission output gates the architectural decision.** Do not pre-commit either architecture; surface the count and let Matt direct.

---

## 2. Scope — what to crawl

### 2.1 Mandatory cultural traditions (must produce at least baseline corpus)

| Tradition | Expected counts (informational only — surface empirical reality) | Source-quality expectation |
|---|---|---|
| **Western (Babylonian / Hellenistic / IAU-recognized)** | 12 zodiac signs + 88 IAU constellations | Wikipedia + IAU + Britannica + academic |
| **Chinese** | 12-animal zodiac cycle + 28 Xiu lunar mansions (4 quadrants: Azure Dragon, White Tiger, Vermilion Bird, Black Tortoise) + 5-element 60-year cycle interactions | Wikipedia + Chinese Academy of Sciences ethnoastronomy + Stellarium cultural-tradition data |
| **Vedic / Jyotish (Hindu)** | 12 Rashi + 27 (sometimes 28) Nakshatras lunar mansions | Wikipedia + Sanskrit primary sources via academic translation + cultural-heritage institutions |
| **Egyptian** | 36 decans + Dendera zodiac figures + named deities mapped to dates (Ra, Bastet, Anubis, Sekhmet, etc. — period-distinguished Ptolemaic vs older) | Wikipedia + British Museum + Met Museum + Egyptological academic |
| **Mayan** | 20 Tzolkin day-signs (Imix, Ik, Akbal, Kan, Chicchan, Cimi, Manik, Lamat, Muluc, Oc, Chuen, Eb, Ben, Ix, Men, Cib, Caban, Etznab, Cauac, Ahau) × 13 numbers = 260-day cycle | Wikipedia + Smithsonian + academic Mesoamericanist |
| **Aztec** | 20 Tonalpohualli day-signs + named deity associations | Wikipedia + INAH (Instituto Nacional de Antropología e Historia) + academic |
| **Celtic tree zodiac (Coelbren / Ogham-adjacent)** | 13 trees (Birch, Rowan, Ash, Alder, Willow, Hawthorn, Oak, Holly, Hazel, Vine, Ivy, Reed, Elder) — note this is partly modern-neopagan reconstruction; flag accordingly | Wikipedia + Robert Graves White Goddess (with caveat) + academic Celticist |
| **Tibetan** | 12-animal cycle (Garuda substitutions where varies from Chinese) + Tibetan-Buddhist constellation tradition | Wikipedia + Tibetan-Buddhist academic + Stellarium |
| **Japanese (Jūnishi)** | 12-animal Chinese-derived (preserve variant lineage tags) + Japanese constellation tradition | Wikipedia + Japanese cultural-heritage |
| **Vietnamese** | 12-animal Chinese-derived (Cat-for-Rabbit; Buffalo-for-Ox variant) | Wikipedia + Vietnamese cultural |
| **Korean** | 12-animal Chinese-derived (Ddi) + Korean constellation tradition | Wikipedia + Korean cultural-heritage |
| **Persian / Zoroastrian** | 12 month-signs + named angels (Frawardin, Ardwahisht, Khordad, Tishtrya, Amurdad, Shahrewar, Mihr, Aban, Adur, Day, Wahman, Spendarmad) | Wikipedia + Encyclopaedia Iranica + academic Iranologist |
| **Arabic** | 28 lunar mansions (Manazil al-Qamar) | Wikipedia + Islamic-astronomy academic |
| **Polynesian (broad)** | Navigator-star traditions; Pleiades (Makali'i Hawaiian, Matariki Maori); voyaging-star sets per island culture | Bishop Museum (Hawaiian) + Te Papa (Maori) + Polynesian Voyaging Society + academic |
| **Aboriginal Australian** | Emu in the Sky + per-culture sky-figures (Yolngu, Wardaman, Boorong, Adnyamathanha — multiple cultural traditions) | **CULTURAL SENSITIVITY FLAG SUBSTANTIAL** — Australian Institute of Aboriginal and Torres Strait Islander Studies (AIATSIS) + academic ethnoastronomy with explicit indigenous-permission framing |
| **Inuit / Arctic Circumpolar** | Caribou-hunting Ursa Major + per-culture sky-figures (Inuit, Sámi, Yupik, Aleut, Chukchi) | Smithsonian Arctic Studies + academic ethnoastronomy |
| **Andean (Quechua / Aymara)** | Yacana llama dark-cloud constellation + Pleiades (Qoto) + Andean cross + per-culture sky-figures | Wikipedia + academic Andeanist + UNESCO World Heritage records |
| **Mesoamerican (beyond Tzolkin)** | Maya + Aztec + Olmec + Toltec sky-figures; Tzolkin sky-mapping; named star groupings | Smithsonian + INAH + academic Mesoamericanist |
| **West African (Dogon + broader)** | Dogon Sirius tradition (Sigui ceremony 60-year cycle) + Yoruba + Akan + other tribal sky-traditions | **CULTURAL SENSITIVITY FLAG SUBSTANTIAL for Dogon Sirius lore** — academic ethnoastronomy with caveat about Marcel Griaule sources |
| **Native American (multi-tribal — broad scope)** | Per-tribal sky-traditions (Lakota, Navajo, Pawnee, Cherokee, Inuit, Anishinaabe, etc.) — DO NOT collapse into single "Native American zodiac"; surface per-tribe | **CULTURAL SENSITIVITY FLAG SUBSTANTIAL** — Smithsonian National Museum of the American Indian + tribal cultural-heritage offices + academic with explicit tribal-permission framing |
| **Mesopotamian (Babylonian / Sumerian / Akkadian)** | Predecessor constellation traditions (MUL.APIN tablet content; predecessors to Greek zodiac) | Wikipedia + British Museum + Mesopotamian-studies academic |
| **Tahitian / Maori navigator (Polynesian-deeper)** | Beyond Pleiades — full navigator constellation sets | Polynesian Voyaging Society + academic Polynesianist |
| **Norse / Germanic / runic** | Runic-zodiac (12 houses with runes — note partial modern reconstruction; flag) + Norse constellation tradition (Aurvandil's Toe, Odin's Wagon = Ursa Major) | Wikipedia + Old Norse academic |

### 2.2 Discretionary / opportunistic (surface if found; no mandate)

Tibetan-Buddhist Kalachakra constellation system; Tamil 27 Nakshatra (variant of Vedic); Korean Cheonsang Yeolcha Bunyajido star-chart; Khmer cosmology; Persian-Babylonian Astronomical Diaries; medieval European astrological constellation variants; Etruscan; Phoenician; Carthaginian; pre-Islamic Arabic; Tongan navigator stars; Pacific Northwest Coast (Tlingit, Haida); Andean Inca-specific subset; Mapuche; Patagonian; Tehuelche; African beyond Dogon (Maasai, San, Zulu); Madagascar; Khoisan.

### 2.3 Out of scope (do NOT crawl)

- **Modern fictional zodiacs** (e.g., Pokémon-themed zodiacs, anime-zodiacs, Final Fantasy zodiac jobs, custom RPG zodiacs). The substrate-led discipline targets EMPIRICAL human cultural traditions. Fictional zodiacs may inform design downstream but are not substrate.
- **Personality-quiz / horoscope content** (per Q5 from gandalf 2026-06-09 plan — tonal-register navigation toward mythic/cosmological reading, away from horoscope baggage). Do not include horoscope-content sites as sources.
- **Astrology-app-derived content** (Co-Star, The Pattern, modern astrology apps). Source from primary ethnoastronomy / museum / academic.

---

## 3. Output schema (mandatory per-entry fields)

Every entry in the corpus MUST carry the following fields. The visual-representation requirement is **non-negotiable** per Matt directive.

```yaml
sign_name:
  primary: "Leo"                              # Most-recognized name in the tradition
  variants: ["Aslad (Arabic)", "Simha (Vedic)", "獅子 (Chinese)"]   # Cross-cultural name variants if same sign appears across traditions; optional
  romanization: "Leo"                          # If primary not Roman alphabet
  native_script: ""                            # If applicable (Sanskrit, Hieroglyph transliteration, Mayan glyph code, etc.)

cultural_tradition:
  primary_culture: "Hellenistic Western"      # Authoritative cultural-tradition of origin
  derivative_cultures: ["Roman", "Islamic Golden Age", "Modern Western"]  # Cultures that inherited or adapted
  geographic_origin: "Greece"                  # Distinct from cultural — geographic origin
  period_range: "Babylonian origin ~1000 BCE; Greek codification ~150 BCE Ptolemy"
  status_in_modern_tradition: "active_living | living_ceremonial | scholarly_reconstruction | extinct"

system_metadata:
  system_name: "Western zodiac"                # The named system this sign belongs to
  total_signs_in_system: 12                    # Count of signs in this system
  position_in_system: 5                        # Ordinal position (Leo is 5th)
  sign_classification:                         # Per-system organizing principle
    element: "Fire"                            # If system has element axis
    modality: "Fixed"                          # If system has modality/quadrant
    quadrant: ""                               # If system has quadrant (Chinese Xiu Azure Dragon etc.)
    deity_association: ""                      # If system has deity
    season: "Summer (Northern Hemisphere)"     # If system has seasonal
    other: {}                                  # Tradition-specific axes

# ════════════════════════════════════════════════════════════
# VISUAL REPRESENTATION (LOAD-BEARING — Matt 2026-06-09 directive)
# At LEAST ONE of the following four MUST be populated.
# Preferably ≥2 for cross-verification.
# ════════════════════════════════════════════════════════════
visual_representation:
  image_url:                                   # Primary visual reference
    url: "https://upload.wikimedia.org/..."
    description: "Constellation diagram showing star positions and conventional figurative outline"
    source: "Wikipedia commons"
    license: "CC-BY-SA-3.0"
    verified_loads: true                        # Boolean confirmation the URL resolves
  image_url_secondary: []                       # Additional images (cultural-iconography, museum-artifact photos, etc.)
  star_coordinates:                             # Astronomical star-set for IAU-recognized or research-recoverable
    coordinate_system: "IAU equatorial J2000"
    primary_stars:                              # Major stars composing the asterism
      - name: "Regulus (α Leonis)"
        ra: "10h 08m 22.3s"
        dec: "+11° 58′ 02″"
        magnitude: 1.40
      - name: "Denebola (β Leonis)"
        ra: "11h 49m 03.6s"
        dec: "+14° 34′ 19″"
        magnitude: 2.14
      # ... continue for all major asterism stars
    notes: "Lion-shape asterism per IAU constellation boundary"
  asterism_schematic:                           # Text-described shape if image unavailable
    description: "Reverse question-mark forming the lion's mane (Regulus, Eta, Gamma, Zeta, Mu); triangle forming hindquarters (Denebola, Theta, Beta)"
    line_topology: "Mane: Regulus→Eta→Gamma→Zeta→Mu. Body: Mu→Theta→Denebola→Beta→back-to-Theta"
  cultural_iconography:                         # How the tradition depicts the figure (artwork, sculpture, ritual)
    description: "Depicted as a lion in profile; often crowned or rampant in heraldic-derived medieval European depictions; Persian astronomical manuscripts show seated lion"
    reference_sources: ["Al-Sufi Book of Fixed Stars 964 CE", "Dürer's Imagines coeli 1515", "Met Museum medieval European astronomical manuscripts"]
    reference_urls: ["https://www.metmuseum.org/..."]

# ════════════════════════════════════════════════════════════

primitive_association_hints:                  # Substrate hints for gandalf Q2 mapping (NOT final mapping; informational)
  suggested_element: "Fire"                    # If tradition associates element
  suggested_attribute: "STR"                   # If tradition associates personality / strength / etc. (with caveat about horoscope baggage)
  suggested_animal_form: "Lion"                # If figurative
  suggested_object_form: ""                    # If symbolic-object-based
  symbolic_role: "Sovereign, royalty, courage, sustained-presence"
  mythic_narrative_summary: "Greek: Nemean Lion slain by Heracles, placed in sky by Zeus. Vedic: Simha governs courage and royal nature. Egyptian: associated with Sekhmet lioness goddess of Ra's wrath."

semantic_vocabulary:                          # Rich text for embedding-similarity if elrond Phase C uses semantic methodology
  symbolic_keywords: ["lion", "fire", "summer", "sovereign", "courage", "pride", "fixed", "sustained"]
  mythic_narrative: "Free text capturing the tradition's full narrative around this sign — Heracles + Nemean Lion + Zeus + sky-placement; Sekhmet wrath of Ra; Simha governs royal qualities; etc."
  visual_motifs: ["crowned lion", "rampant lion", "seated lion", "lion of Judah variant lineage"]

cultural_sensitivity:
  flag_level: "none | low | medium | high | restricted"
  explanation: "none"                          # If non-none, explain — e.g., "Aboriginal Australian sky-lore may contain sacred-restricted content per AIATSIS guidelines; this entry sourced only from publicly-published academic material"
  source_authorization: "Public-domain Wikipedia + Met Museum (non-restricted)"

provenance:
  primary_source_url: "https://en.wikipedia.org/wiki/Leo_(constellation)"
  secondary_sources:
    - "Wikipedia: Leo (astrology)"
    - "Britannica: Leo constellation"
    - "Stellarium cultural-tradition data: Western zodiac module"
  academic_anchor: "Ridpath, Ian. Star Tales. 2018 edition. (Background on Greek mythological origin)"
  crawl_date: "2026-06-09"
  legolas_confidence: "high | medium | low"   # How confident is legolas this entry is well-sourced
```

### 3.1 Visual-representation completeness gate

**An entry is INCOMPLETE if `visual_representation` has zero populated sub-fields.** Legolas does NOT ship the corpus with any incomplete entry. If a sign cannot be visually represented by any of the four sub-fields, file a per-sign disposition note in the synthesis explaining why (e.g., "Aboriginal sky-figure X — visual representation restricted per AIATSIS protocol; sourced as text-only with explicit cultural-sensitivity flag").

### 3.2 Output file structure

```
agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/
├── synthesis.md                                    # Overall report + per-tradition counts + dispositions
├── corpus.yaml                                     # Single-file machine-readable corpus (all entries)
├── per-tradition/
│   ├── western-zodiac.md                           # Markdown summary per tradition
│   ├── western-iau-constellations.md
│   ├── chinese-zodiac.md
│   ├── chinese-xiu-lunar-mansions.md
│   ├── vedic-rashi.md
│   ├── vedic-nakshatras.md
│   ├── egyptian-decans.md
│   ├── mayan-tzolkin.md
│   ├── ...
│   └── (one file per tradition listed in § 2.1)
├── visual-assets/                                  # Image URL references list per tradition; do NOT download images (substrate-tagging discipline)
│   ├── western-zodiac-image-refs.md
│   ├── chinese-zodiac-image-refs.md
│   └── ...
└── cultural-sensitivity-dispositions.md             # Per-tradition cultural-sensitivity protocol decisions + restricted-content carve-outs
```

---

## 4. Methodology + discipline citations

### 4.1 Mode B systematic catalogue crawl protocol (per Legolas OP § Mode B)

- **Background process** per Discipline #19 — fire as background workstream; do not block on completion; report per-phase progress
- **Robots.txt + rate-limit respect** per Discipline #20 — Wikipedia / Wikidata / museum APIs are well-behaved; respect their TOS
- **Read-only** per ADR-006 — never modify source data; download is for substrate-extraction, not republication
- **Source-quality hierarchy** (descending preference):
  1. IAU + Stellarium cultural-tradition data (highest authority for star-coordinate-set)
  2. Major museum collections (Met / British Museum / Smithsonian / National Museum of Iran / INAH / Bishop Museum / Te Papa / AIATSIS)
  3. Academic ethnoastronomy literature
  4. Cultural-heritage institutional records
  5. Wikipedia (start here for breadth; cross-validate with above)
  6. Britannica
  7. Cultural-specific institutional websites (Polynesian Voyaging Society, AIATSIS, etc.)
  - **AVOID:** astrology-app sites, horoscope-content sites, personality-quiz sites, modern fictional-zodiac sites

### 4.2 Cultural-sensitivity protocol (LOAD-BEARING)

**This is non-optional.** Several traditions carry sacred or restricted-knowledge components. The protocol:

| Sensitivity level | Examples | Protocol |
|---|---|---|
| **none** | Western zodiac (publicly published since antiquity); Chinese zodiac (publicly published since antiquity); IAU constellations (scientific) | Standard crawl; no restrictions |
| **low** | Vedic Nakshatras (some esoteric Jyotish content); medieval European astrological variants | Source from academic / museum; flag specific entries if cited as esoteric |
| **medium** | Mayan / Aztec ceremonial content; Andean dark-cloud astronomical content; West African non-Dogon | Source from academic + cultural-heritage institutions; cite institutional permission framing where available |
| **high** | Dogon Sirius lore; Polynesian navigator full-traditions; Tibetan-Buddhist Kalachakra full system; non-public Native American tribal star-traditions | Source ONLY from academic + cultural-heritage with explicit acknowledgment of sensitivity; flag every entry; default-conservative on inclusion |
| **restricted** | Sacred Aboriginal Australian sky-figures (per AIATSIS sacred-restricted lists); ceremonial Native American star-traditions (per tribal cultural-heritage offices); restricted Polynesian navigator-knowledge | DO NOT include entry in corpus; file a per-tradition disposition note explaining the exclusion |

**When in doubt, flag higher and exclude.** Substrate cleanliness > completeness. The cosmograph will surface what's appropriate; what isn't appropriate doesn't enter the substrate.

### 4.3 Substrate-tagging discipline (Discipline #25 semantic-layer rep-audit applied in advance)

The marginal-lineage tagging-pattern meta-record (`canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`) named the 4-mode collapse where lineage tags drift between:
- Mode A — intended (cultural-tradition of origin)
- Mode B — geographic-origin artifact
- Mode C — naming-allusion artifact
- Mode D — cross-tagged metadata error

**Apply this discipline AT CRAWL TIME, not post-hoc.** Specifically:
- Aboriginal "Emu in the Sky" → cultural_tradition.primary_culture must specify which Aboriginal cultural-tradition (Yolngu / Wardaman / Boorong / etc.) — NOT "Australian geographic"
- Inuit "Caribou Ursa" → cultural_tradition.primary_culture must specify which Arctic cultural-tradition (Inuit / Sámi / Yupik / Aleut / Chukchi — these are DISTINCT cultures, do not collapse to "Arctic")
- Andean "Yacana llama" → cultural_tradition.primary_culture must specify Quechua / Aymara / Inca / Mapuche / other (these are DISTINCT traditions, do not collapse to "Andean")
- Mesoamerican Tzolkin day-signs → cultural_tradition.primary_culture must specify Maya / Aztec / Olmec / Toltec / other (these are DISTINCT traditions, do not collapse to "Mesoamerican")
- Chinese-derived 12-animal cycle (Vietnamese / Japanese / Korean / Tibetan variants) → preserve each as DISTINCT entry with cultural_tradition.primary_culture per variant + cultural_tradition.derivative_cultures linking to Chinese origin; DO NOT collapse to "East Asian"

**Substrate-led rep-audit means:** when you have a sign, ask "what does this specifically depict?" not just "what does the metadata say?" If a "Polynesian navigator star" entry's source material specifically credits Hawaiian navigator tradition, tag it Hawaiian-specific. If sources are ambiguous, tag at the most specific level the source supports + flag the ambiguity in `legolas_confidence: medium | low`.

### 4.4 Background process discipline (#19)

- Spawn as background workstream
- Report per-phase progress at completion of each cultural tradition (synthesis.md gets appended incrementally; do not wait for full completion to surface)
- Estimated wall-clock 2-5 days; report sooner if a tradition completes faster
- If crawl encounters a tradition that takes substantially longer than expected (e.g., Vedic Nakshatras at full depth), surface a per-tradition status note + continue
- DO NOT block on perfection per tradition; surface "good enough for substrate purposes" + flag gaps for follow-on Phase 2 supplementary crawl

---

## 5. Deliverables

### 5.1 Primary deliverables

1. **`synthesis.md`** — overall report with:
   - Total entry count + per-tradition count breakdown
   - Per-tradition cultural-sensitivity disposition summary
   - Visual-representation completeness audit (% entries with each visual sub-field populated)
   - Substrate-tagging rep-audit summary (per-tradition tag-precision confidence)
   - Per-tradition gap notes (signs known to exist but not surfaced; reasons)
   - Cross-tradition deduplication structure observations (e.g., 12-animal Chinese cycle reappearing across 5+ cultures; Pleiades named in 20+ cultures)
   - Recommended Phase 2 supplementary crawl scope (if applicable)

2. **`corpus.yaml`** — single-file machine-readable corpus containing all entries per § 3 schema

3. **`per-tradition/<tradition>.md`** — one markdown summary per cultural tradition listed in § 2.1

4. **`visual-assets/<tradition>-image-refs.md`** — per-tradition image URL reference list (do NOT download; reference only)

5. **`cultural-sensitivity-dispositions.md`** — per-tradition cultural-sensitivity protocol decisions + restricted-content carve-outs + AIATSIS / tribal / cultural-heritage-institution-permission framing notes

### 5.2 Operational reporting cadence

Append to `synthesis.md` per-tradition completion. Surface intermediate counts:
- "Western zodiac complete: 12 entries"
- "Chinese zodiac + Xiu complete: 12 + 28 = 40 entries"
- "Vedic Rashi + Nakshatra complete: 12 + 27 = 39 entries"
- "..."
- "Running total: N entries across M traditions"

Matt makes architectural-decision call (kit-binds-1:1 vs cluster-anchor) post-completion based on final N.

---

## 6. Completion criteria

The commission is COMPLETE when:

1. ✅ All mandatory cultural traditions listed in § 2.1 have been crawled OR a clear "no further mainstream-source coverage exists" disposition is filed
2. ✅ Every entry in `corpus.yaml` has ≥1 populated `visual_representation` sub-field (or per-entry exclusion disposition in `cultural-sensitivity-dispositions.md`)
3. ✅ Substrate-tagging rep-audit per § 4.3 applied at crawl time; cultural_tradition.primary_culture tags at appropriate specificity per source material
4. ✅ Cultural-sensitivity protocol per § 4.2 applied; high/restricted entries flagged or excluded per protocol
5. ✅ `synthesis.md` surfaces total N + per-tradition breakdown + visual-completeness audit + gap notes
6. ✅ Discretionary § 2.2 traditions opportunistically included if encountered; not blocking on coverage

**Matt-routed decision point (post-completion):** gandalf consumes corpus + Matt makes the kit-binds-1:1 vs cluster-anchor architectural call per § 1 table.

---

## 7. Composition with prior work

- **Composes with** `canonical/story/2026-06-06-atomic-substrate-registry.md` Layer 0.5 seasonal-substrate-rotation operator — different cultural sky-traditions become natural seasonal rotations
- **Composes with** `canonical/story/2026-06-05-cosmograph-pivot.md` § 9 — primitive-as-star + kit-as-constellation may refine to primitive-as-glyph + kit-as-constellation depending on architectural-decision outcome
- **Composes with** `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 2.6 — cosmograph IS the literal night sky; cultural-reading layer per season
- **Composes with** marginal-lineage recognition records (2026-05-23 × 5) — sky substrate surfaces coherent cultural-tradition presence (Aboriginal / Inuit / Andean / Polynesian / Mesoamerican) where weapon substrate did not
- **Composes with** Discipline #41 (pre-authored taxonomy interrogation) — substrate-led discipline at zodiac framework layer (Pattern 6 applied to zodiac axis)
- **Composes with** Discipline #25 (semantic-layer rep-audit) — applied AT CRAWL TIME via § 4.3 protocol

---

## 8. Anti-patterns to avoid (gandalf flags)

- ❌ Pre-imposing a target count ("we need 400 entries; pad if short") — substrate-led: surface empirical reality, whatever the count
- ❌ Collapsing distinct cultural traditions to broader-geographic labels for convenience (e.g., "Native American zodiac" — there is NO single Native American zodiac; surface per-tribe)
- ❌ Shipping entries without visual representation (Matt directive non-negotiable)
- ❌ Crawling fictional / horoscope-app content because it's easier (out of scope per § 2.3)
- ❌ Including restricted sacred content because "it's in the source" — when in doubt, flag higher and exclude
- ❌ Blocking on perfection per tradition — surface good-enough-for-substrate-purposes + flag gaps; Phase 2 supplementary crawl handles deep gaps
- ❌ Re-collapsing Chinese-derived variants (Vietnamese / Japanese / Korean / Tibetan) — preserve as distinct entries with derivative_cultures lineage tags
- ❌ Adding "personality" or "horoscope" fields to entries — symbolic-role + mythic-narrative are the appropriate symbolic vocabulary (cosmological reading per Q5 tonal-navigation)

---

## 9. Sign-off

**Authored:** gandalf 2026-06-09 per Matt directive "author the legolas commission, and be sure that we capture either a drawing, rendering, mapping, coordinate space (or something similar) across every single star sign which can be used to ensure we get the mapping right."

**Authority:** gandalf design-steward authority for cross-cutting substrate enrichment commission + Matt 2026-06-09 directive ratifying substrate-led pivot at zodiac framework layer.

**Routing:** legolas executes (background process per Discipline #19); per-tradition reporting to `synthesis.md` as crawl progresses; gandalf consumes at completion + routes to Matt for architectural-decision call (kit-binds-1:1 vs cluster-anchor).

**Empirical-evidence triggers (post-completion):**
- gandalf reads corpus + visual-representation audit + cultural-sensitivity dispositions
- gandalf surfaces N + key observations to Matt
- Matt makes kit-binds-1:1 vs cluster-anchor architectural call
- If kit-binds-1:1: primitive-clusters get glyphic-symbology architecture (Tal Rasha tomb sigil precedent per Matt 2026-06-09 directive) — follow-on gandalf design call + Legolas Mode A research on archaic glyph/symbology systems (Cuneiform, Hieroglyph, Mayan glyphs, Runes, Theban, Enochian, sigil-magic traditions, Horadric-inspired fictional precedent)
- If cluster-anchor: Q2 primitive-mapping work proceeds per gandalf 2026-06-09 plan original framing (sign-to-primitive vote scoring; elrond methodology consultation per Discipline #18)
- Either architecture: composes with seasonal-substrate-rotation operator + two-layer + buffer-space + Earth-Avatar Creation Moment Architecture

**Composition with prior canonical commitments:** all preserved (Earth-Avatar Creation Moment Architecture 2026-06-07 + atomic-substrate-registry 2026-06-06 + cosmograph-pivot 2026-06-05 + hypothesis-flow 2026-06-06 CANONICAL + federated PC team architecture 2026-06-07 + marginal-lineage recognition records 2026-05-23).

**End of commission.**
