# Phase 1 — 3 Kit-to-Star-Sign Canonical Mappings (Hand-Curated)

**STATUS:** ACTIVE (Phase 1 output of elrond kit-to-star-sign assignment MVP commission)
**Date:** 2026-06-09
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-06-09 directive — "for kits to starsigns... for now, we only need 3 kits to map cleanly to starsigns. the rest will be random" + per-kit picks delegated "1) Duskweaver, 2) pick one other mage with magic find and no boss killer, 3) pick a physical character of your choice"
**Commission parent:** `agentic_orchestration/dispatches/2026-06-09-elrond-kit-to-star-sign-assignment-mvp.md`
**Downstream consumer:** Phase 2 elrond schema extension + assignment (consumes this doc; applies 3 hand-overrides + random-assigns the rest)
**Companion docs:**
- `agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/synthesis.md` (423-entry zodiac corpus; semantic-match search target)
- `agentic_orchestration/gandalf/notes/2026-06-02-qdx-5-top-5-character-curation.md` (top-5 Featured Characters; selection pool for kits 2 + 3)
- `canonical/story/2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` (Branch A; kit-binds-1:1 is operationalized via this hand-curation + Phase 2 elrond random-assignment)

---

## 0. TL;DR

3 hand-curated kit-to-star-sign mappings per Matt criteria:

| # | Kit ID | Kit Identity | Element | Star-Sign | Tradition | Semantic Match |
|---|---|---|---|---|---|---|
| 1 | `kit_shadow_000007` | **Duskweaver of the Eclipsed Meridian** | shadow | **Mula (मूल)** | Vedic Nakshatra (#19) | Root / Galactic Center / Nāga-serpent / death-passage / transformation — composes with shadow + eclipse + inversion + meridian themes |
| 2 | `kit_holy_000005` | **Cannonade Cleric of Scattered Light** | holy | **Krittika (कृत्तिका)** | Vedic Nakshatra (#3) | Pleiades / Kartikeya's six divine warrior-nurses who STRIKE / cluster-of-light — composes with holy + cleric + cannonade-multiplicative-strike + scattered-light themes |
| 3 | `kit_physical_000026` | **Stonefist of Broken Wall** | physical | **Hercules** | IAU constellation (post-Renaissance; Greco-Roman mythological depth) | Twelve Labors / physical-strength epitome / wall-breaking via Augean Stables + Cerberus gates — composes with stone + fist + broken-wall + siege-warden themes |

**Cross-element coverage:** shadow + holy + physical (3 different damage-scaling paths per canonical 47 three-path routing). Architectural breadth surfaced.

**Cross-tradition variety:** 2 Vedic Nakshatras + 1 IAU Greco-Roman. Both substrate-traditions carry deep mythological narrative for player-facing copy. The two Vedic picks share methodological roots (lunar mansion system; rich symbolic vocabulary; canonical zodiac alongside Western).

**Kit selection methodology:**
- Kit 1 = Duskweaver per Matt explicit direction (canonical lead identity per cycle-18; Top-1 per top-5 curation)
- Kit 2 = gandalf-discretion within top-5 mage candidates, filtered by "magic find + no boss killer" criterion (themes; explicit magic-find stats not surfaced in current corpus metadata; Cannonade Cleric's "Cannonade" semantic reads AOE-clearing-style not boss-killer-style)
- Kit 3 = gandalf-discretion physical pick; using top-5 physical pick (Stonefist of Broken Wall — Best of 16 physical candidates per QDX-5 curation; most distinctive non-template name)

---

## 1. Mapping 1 — Duskweaver of the Eclipsed Meridian ↔ Mula

### Kit identity

| Field | Value |
|---|---|
| Kit ID | `kit_shadow_000007` |
| Pre-rename name (Wave B) | Penumbra Caster of Dusk Meridian |
| Canonical name (cycle-18 LLM rename) | **Duskweaver of the Eclipsed Meridian** |
| Element | shadow |
| T4 selection | **Twilight Inversion Shell** (per cycle-18 + 2026-06-05 Duskweaver amendment) |
| Archetype | Caster (shadow primary; spell-scaling) |
| Faction | per cycle-18 faction assignments (3 factions × 37 kits; Duskweaver in faction-of-record) |
| Featured rank | TOP-1 ★ (canonical lead identity) |
| Selection authority | Matt 2026-06-09 explicit direction (kit #1 of 3) |

### Star-sign identity

| Field | Value |
|---|---|
| Star-sign primary name | **Mula** (मूल) |
| Romanization variants | Moola, Mulam |
| Tradition | Vedic Jyotish (Nakshatra system; 27-mansion lunar zodiac) |
| Position in system | #19 of 27 |
| Star coordinates | Centered on Lambda Scorpii (Shaula) + Upsilon Scorpii (Lesath) — the "stinger" of Scorpius; near Galactic Center |
| Ruling planet | Ketu (the descending lunar node — the "tail" of the celestial dragon; ECLIPSE-CAUSER in Vedic cosmology) |
| Deity | Nirṛti (goddess of destruction / dissolution / the abyss) |
| Gana | Rakshasa (demonic / shadow-aligned) |
| Symbolic role | Root / origin / foundation / dissolution / death-passage / threshold-between-worlds |
| Mythic narrative | Mula points toward the Galactic Center — the cosmic axis where all material existence has its root and ultimate dissolution. The Nakshatra of beginnings and endings. Associated with the Nāga (serpent-spirits of the underworld) + Nirṛti (goddess who dissolves what is). Ketu rulership couples Mula directly to ECLIPSE cosmology — Ketu is the eclipse-causing lunar node. Spiritual seekers, transformers, and those who walk the threshold between worlds. |

### Semantic match reasoning

Duskweaver of the Eclipsed Meridian is a shadow-caster whose load-bearing T4 selection (Twilight Inversion Shell) channels the inversion moment — the boundary where light becomes darkness, where meridian sun is eclipsed. The kit's identity sits at the cosmological boundary between manifest and dissolved, light and shadow.

**Mula composes with this identity at four layers:**

1. **Eclipse cosmology direct (ruling planet Ketu)** — Mula is one of the three Nakshatras ruled by Ketu, the descending lunar node, the eclipse-causer in Vedic astronomy. "Eclipsed Meridian" reads literally — Mula carries the eclipse-mythology Vedic tradition embeds at the cosmic-axis layer.

2. **Galactic Center alignment** — Mula points to the cosmic center, the deepest gravitational well in the galaxy, the dark heart from which all material existence has its root. The "Meridian" in Duskweaver's name composes from the local-sky meridian (where the sun reaches zenith) to the COSMIC meridian (the galactic-center axis). The kit's meridian is the cosmic one.

3. **Nāga-serpent + Nirṛti dissolution semantic** — Mula's deity Nirṛti dissolves what is; its symbolic root is the death-passage; its mythological figures are the Nāga (serpent-spirits of underworld). All shadow-archetype semantics. The "Inversion" in Duskweaver's T4 reads as Nirṛti's dissolution — what was light is inverted to its shadow-form; what was solid dissolves at its root.

4. **Threshold / boundary archetype** — Mula's role in Jyotish is the gateway Nakshatra — the place where one cycle ends and another begins. Spiritual seekers, transformers, those who walk between worlds. Duskweaver's "Caster" archetype + shadow primary positions the kit as a practitioner of threshold-crossing magic.

**Cross-tradition richness:**
- Mula is Vedic; Vedic Nakshatras are canonical alongside Western zodiac
- The Lambda + Upsilon Scorpii stars (Mula's anchor) compose with Western Scorpius mythology (the scorpion that killed Orion — death + boundary themes)
- Galactic Center adjacency composes with modern astronomical naming (Sagittarius A*) — cross-temporal richness

---

## 2. Mapping 2 — Cannonade Cleric of Scattered Light ↔ Krittika (Pleiades)

### Kit identity

| Field | Value |
|---|---|
| Kit ID | `kit_holy_000005` |
| Canonical name | **Cannonade Cleric of Scattered Light** |
| Element | holy |
| T4 selection | per kit data |
| Archetype | Caster (holy primary; spell-scaling); modern-caster + holy fusion (Q18 modern-caster overlay) |
| Featured rank | Rank 4 (top-5 Featured Characters per QDX-5 curation) |
| "Magic find + no boss killer" rationale | "Cannonade" semantic = artillery-barrage = AOE-multiplicative-strike, NOT single-target high-DPS boss-killing; "Scattered Light" semantic = dispersed-clearing-style; modern-caster + cleric fusion suggests utility/support/clearing role |
| Selection authority | gandalf curation per Matt 2026-06-09 "pick one other mage with magic find and no boss killer" |

### Star-sign identity

| Field | Value |
|---|---|
| Star-sign primary name | **Krittika** (कृत्तिका) |
| Romanization variants | Krittika, Kṛttikā |
| Tradition | Vedic Jyotish (Nakshatra system; 27-mansion lunar zodiac) |
| Position in system | #3 of 27 |
| Star coordinates | The Pleiades open star cluster (M45; ~440 light-years from Earth; 100+ stars in cluster; ~7 visible to naked eye) |
| Ruling planet | Sūrya (the Sun) |
| Deity | Agni (god of fire); the Krittika sisters (six divine warrior-nurses of Kartikeya) |
| Gana | Rakshasa (in some classifications) / Devagana (in others) — boundary placement |
| Symbolic role | Cutting / striking / piercing / forging / nurturing-fire / multiplicative-strike / divine-warrior-host |
| Mythic narrative | The Pleiades are the Krittika — six (or seven) divine sisters who became the nurses of Kartikeya, the six-headed son of Shiva and Parvati, the god of war who would defeat the demon Tarakasura. The Krittika nurses fed Kartikeya from six breasts simultaneously, giving him his six heads (or in another tradition, the seven Rishi-wives who became the Pleiades after dispersing from earthly trouble). The cluster is the multiplicative-strike formation — six warrior-nurses striking together; the cosmic forge where divine heroes are made. **CRITICAL: most-attested asterism in the Legolas corpus** — 11+ cultural traditions name the Pleiades (Western Pleiades / Chinese Mǎo / Hawaiian Makali'i / Maori Matariki / Mesopotamian "The Seven" / Inuit Sakiattiat / Anishinaabe Manidoominensag / Cherokee Ani Tsutsa / Arabic Al-Thurayya / Andean Collca — agricultural-marker; many more). |

### Semantic match reasoning

Cannonade Cleric of Scattered Light is a holy-caster whose identity is cluster-striking and area-effect, NOT single-target boss-killing. "Cannonade" + "Scattered Light" + cleric register read as multiplicative + dispersed + devotional.

**Krittika (Pleiades) composes with this identity at five layers:**

1. **Multiplicative-strike formation direct** — the Krittika nurses (six or seven) strike together; Kartikeya wields six weapons simultaneously through his six heads. The cosmic image of multiplicative coordinated strike against demon-foes. "Cannonade" reads as multiplicative artillery — the Krittika-nurse formation is its mythic analog.

2. **Scattered-Light literal** — Pleiades IS scattered light; literally a cluster of 100+ stars (~7 visible to naked eye) appearing as a luminous cluster in the sky. "Scattered Light" reads as the cluster itself. The cleric's holy-light register composes with the divine-fire (Agni rulership) of Krittika.

3. **Cleric / devotional archetype** — Krittika's deity is Agni (sacred fire; foundational ritual deity in Vedic tradition); the Krittika sisters are themselves devoted nurses to a divine child. The cleric-archetype reads as Krittika-nurse-archetype — devotional, fire-tending, holy-coordinated. Kartikeya devotion is a major Hindu tradition (especially South Indian); the cleric register is mythologically attested.

4. **NOT-boss-killer alignment** — Kartikeya does defeat Tarakasura (a major demon-killing arc), but Krittika's role is not the final boss-strike — it's the nurturing + forging + multiplicative-formation that creates and enables the hero. The cleric who clears + supports + enables, not the solo-hunter who kills the boss alone.

5. **Cross-tradition richness — MAXIMUM** — Pleiades is the most-attested asterism in the Legolas corpus (11+ cultural traditions). Cannonade Cleric's mapping to Krittika opens narrative composition with Greek Pleiades (Seven Sisters), Maori Matariki (New Year), Polynesian Makali'i (harvest), Andean Collca (El Niño proxy), Mesopotamian "The Seven" (most auspicious asterism), Hawaiian Makali'i (harvest season), Inuit Sakiattiat, multiple Native American traditions, Arabic Al-Thurayya, Chinese Mǎo (which gives "Subaru" its name). Cross-tradition reading enables seasonal-substrate-rotation operator (atomic-substrate-registry Layer 0.5) — different cultures' Pleiades-reading surfaces per season, all anchored to the same star-cluster substrate.

**Cross-tradition richness:**
- Vedic primary; Western Pleiades + Maori Matariki + many other traditions secondary
- Seasonal-rotation: S1 Krittika (Vedic); S2 Pleiades (Greek); S3 Matariki (Maori); S4 Mǎo (Chinese) — all same cluster, different cultural reading

---

## 3. Mapping 3 — Stonefist of Broken Wall ↔ Hercules

### Kit identity

| Field | Value |
|---|---|
| Kit ID | `kit_physical_000026` |
| Canonical name | **Stonefist of Broken Wall** |
| Element | physical |
| T4 selection | per kit data |
| Archetype | Physical / martial / siege-warden (per QDX-5 curation framing) |
| Featured rank | Rank 5 (top-5 Featured Characters; best of 16 physical candidates per QDX-5 curation; "Stonefist of Broken Wall" is the most distinctive non-template physical Wave B output) |
| Selection authority | gandalf curation per Matt 2026-06-09 "pick a physical character of your choice" |

### Star-sign identity

| Field | Value |
|---|---|
| Star-sign primary name | **Hercules** (Greek Hēraklēs; Latin Hercules) |
| Tradition | IAU constellation (Greco-Roman mythological origin; canonical in 88-IAU system) |
| Position in IAU | Sign IDs 030-058 batch (IAU Constellations B per Legolas corpus) |
| Star coordinates | Northern sky; bordering Lyra, Corona Borealis, Boötes, Draco, Ophiuchus; primary stars: Kornephoros (β Her), Rasalgethi (α Her — variable red giant) |
| Notable celestial features | **M13 Great Globular Cluster** (one of brightest globular clusters; target of Arecibo Message 1974); **M92** (second bright globular); **Hercules constellation cluster of nearby galaxies** |
| Mythic narrative | Hercules — the greatest hero of Greek mythology; son of Zeus and the mortal Alcmene; performed Twelve Labors as penance for killing his family in a Hera-induced madness. Labors include: Nemean Lion (strangled with bare hands — STONE-FIST archetype direct), Lernaean Hydra (multi-headed serpent — repeated multiplicative strikes), Erymanthian Boar (captured alive — physical wrestling), Cretan Bull (subdued — pure physical strength), Augean Stables (diverted two rivers through the WALLS to clean in one day — BROKEN WALL archetype direct), Cerberus (descended into Hades and dragged out the underworld guardian — broken gates of death). Apotheosized to divinity post-mortem. The mythological epitome of physical strength + labor + barrier-breaking + endurance. |
| Cross-cultural recognition | Greek + Roman + medieval European + IAU (post-Renaissance lock); strong cultural recognition in West; also adjacent figures in other traditions (Mesopotamian Gilgamesh as parallel; Norse Thor as parallel; Hindu Bhima as parallel) |

### Semantic match reasoning

Stonefist of Broken Wall is a physical-martial kit whose identity is brute-strength + barrier-destruction + siege-warden role. "Stonefist" + "Broken Wall" read as: physical force epitomized in fist + obstacle obliterated through that force.

**Hercules composes with this identity at four layers:**

1. **Stonefist archetype direct (Nemean Lion + Twelve Labors)** — Hercules strangled the Nemean Lion with bare hands; the Lion's skin became his iconic invulnerable cloak. The "stone fist" is precisely the Hercules archetype — bare-handed strength capable of slaying what conventional weapons cannot pierce. Twelve Labors are uniformly tests of physical strength + endurance; Hercules is the mythological epitome.

2. **Broken Wall archetype direct (Augean Stables + Cerberus)** — Two Labors literally involve wall-breaking: Augean Stables (diverted Alpheus and Peneus rivers THROUGH the stable walls to clean 30 years of filth in one day — a wall-breaking infrastructural feat); Cerberus (descended into Hades, broke the underworld gates, dragged out the three-headed guardian). The "Broken Wall" semantic maps cleanly to Hercules' barrier-breaking labor patterns.

3. **Siege-warden + bulwark archetype** — Hercules in his role as guardian/founder is the protective bulwark archetype: founded cities (Heraclea Lyncestis, Heracleion); guardian of gates; the strong-man at the threshold. Stonefist as siege-warden composes with Hercules as defender of foundational structures (and breaker of corrupt ones).

4. **Physical epitome in canonical Western mythology** — for a physical-primary kit, picking Hercules is the gravitational-center choice for Western/Greco-Roman mythological depth. The IAU Hercules constellation carries this mythological weight at the star-sign layer — M13 Globular Cluster provides celestial anchor + Arecibo Message 1974 provides modern-astronomical hook + Twelve Labors archetype provides narrative depth.

**Cross-tradition variety (beyond Greek):**
- Mesopotamian Gilgamesh (parallel hero-of-strength archetype; predates Hercules)
- Norse Thor (parallel hammer-wielder of physical destruction)
- Hindu Bhima (parallel mace-wielder; Mahabharata strong-man)
- These compose at seasonal-substrate-rotation (S1 Hercules; S2 Gilgamesh; S3 Thor; S4 Bhima — all physical-strength heroes; different cultural framings)

---

## 4. Cross-mapping observations

### 4.1 Element + tradition + archetype matrix

| Kit | Element | Star-sign tradition | Mythological archetype |
|---|---|---|---|
| Duskweaver | shadow | Vedic Nakshatra | Threshold / dissolution / cosmic-axis |
| Cannonade Cleric | holy | Vedic Nakshatra | Multiplicative-strike / nurturing-fire / cluster-formation |
| Stonefist | physical | IAU (Greco-Roman) | Physical strength / barrier-breaking / labor-archetype |

### 4.2 Symbolic + narrative breadth

The 3 mappings span three distinct mythological registers:
- **Duskweaver / Mula** — cosmological / metaphysical (root + galactic center + dissolution)
- **Cannonade Cleric / Krittika** — divine / coordinated / nurturing (Kartikeya's nurses + holy-fire-formation)
- **Stonefist / Hercules** — heroic / physical / labor (Twelve Labors + barrier-breaking)

This breadth gives the 3 hand-curated showcase mappings each a distinct narrative texture; no two read as the same archetype.

### 4.3 Cross-tradition vs single-tradition balance

2 Vedic + 1 IAU mix. Both Vedic picks compose natively with seasonal-substrate-rotation operator (Krittika/Pleiades opens 11+ cultural-tradition variants per season; Mula's eclipse-cosmology connects to other cultures' eclipse mythology). Hercules opens cross-cultural strength-hero variants (Gilgamesh, Thor, Bhima).

**Future seasonal-rotation note:** when seasonal-substrate-rotation operationalizes, these 3 hand-curated mappings can rotate to per-season variants without changing the underlying kit-to-star-sign architectural commitment:
- Duskweaver → Mula (Vedic) / Ketu (Vedic eclipse) / Scorpius Antares (Greek) / Andean dark-cloud
- Cannonade Cleric → Krittika (Vedic) / Pleiades (Greek) / Matariki (Maori) / Makali'i (Hawaiian) / Mǎo (Chinese)
- Stonefist → Hercules (IAU/Greek) / Gilgamesh (Mesopotamian) / Thor (Norse) / Bhima (Hindu)

### 4.4 Cultural-sensitivity audit

All 3 star-sign picks are `cultural_sensitivity: none` per Legolas corpus:
- Vedic Nakshatras: none (publicly published; Jyotish tradition is academic-available + practitioner-living)
- IAU Hercules: none (Western mythology + scientific astronomy)

No restricted content; clean substrate.

---

## 5. Open questions for Matt review (not blocking)

### 5.1 Mage selection (#2)
**Cannonade Cleric of Scattered Light is my pick for "mage with magic find and no boss killer" — selected on thematic reading.** I don't have explicit "magic find" stat data surfaced in current corpus metadata; the pick is based on:
- "Cannonade" semantic = AOE-multiplicative-strike (not single-target boss-killer)
- "Scattered Light" semantic = dispersed-clearing-style
- Modern-caster + cleric fusion (rank 4 in top-5 curation)
- Cross-element coverage from Duskweaver (shadow → holy adds light/shadow duality)

**Alternatives within top-5 mages if Matt has different read:**
- Ember Caster of Scorched Meridian (fire) — caster; "Ember" suggests low-burn/spread
- Galewright of the Scattered Pale (wind) — utility-crafter archetype

If Matt has explicit "magic find" stat data OR prefers different mage, surface for re-curation before Phase 2 elrond fires.

### 5.2 Physical selection (#3)
**Stonefist of Broken Wall** per top-5 (rank 5; best of 16 physical candidates per QDX-5 curation). gandalf-discretion per Matt; default to top-5 canonical pick.

### 5.3 Star-sign canonical lock
These 3 mappings are **Phase 1 hand-curation output** — drax Phase 4+ amended cosmograph + future kit-to-star-sign Pattern B work may iterate. Canonical lock at the star-sign-per-kit layer (vs methodology layer) DEFERRED to Pattern B with Matt when vertical-slice spike playtest informs.

---

## 6. Cross-references to commission

### Phase 2 elrond consumption
Per parent commission § 3.2 (hand-override application):
- Elrond reads this doc
- Applies 3 specific kit_id → star_sign_id assignments per § 0 TL;DR table
- Sets `star_sign_assignment_method: HAND_CURATED` for these 3
- Sets `star_sign_tradition` denormalized field per § 0 TL;DR (Vedic Nakshatra × 2; IAU × 1)

### star_sign_id specific values for elrond
Elrond should resolve from Legolas corpus.yaml using these primary names:
- Mapping 1: `star_sign_id` = entry where `cultural_tradition.primary_culture = "Vedic"` AND `sign_name.primary = "Mula"` (Nakshatra #19)
- Mapping 2: `star_sign_id` = entry where `cultural_tradition.primary_culture = "Vedic"` AND `sign_name.primary = "Krittika"` (Nakshatra #3)
- Mapping 3: `star_sign_id` = entry where `cultural_tradition.primary_culture = "Hellenistic Western"` (or IAU equivalent) AND `sign_name.primary = "Hercules"`

If exact `sign_name.primary` strings differ in corpus.yaml, elrond surfaces variance to gandalf for one-pass clarification.

---

## 7. Sign-off

**Authored:** gandalf 2026-06-09 Phase 1 of elrond kit-to-star-sign assignment MVP commission per Matt 2026-06-09 verbatim direction.

**Authority:** gandalf design-side curation authority for Branch A kit-binds-1:1 architectural commitment Phase 1 output (3 hand-curated kit-to-star-sign mappings).

**Routing:** Phase 2 elrond consumes this doc (applies 3 hand-overrides + random-assigns the rest from 423-entry zodiac corpus per cultural-sensitivity audit). KR sequences Phase 1 → Phase 2 fire. Phase 2 close report routes to gandalf for design review + Matt for awareness.

**Composition with prior canonical commitments:** all preserved (Tal Rasha 2026-06-09 + Legolas zodiac-substrate-corpus 2026-06-09 + Earth-Avatar Creation Moment Architecture 2026-06-07 + atomic-substrate-registry 2026-06-06 + cosmograph-pivot 2026-06-05 + Duskweaver canonical identity from cycle-18 + QDX-5 top-5 curation 2026-06-02).

**End of Phase 1 hand-curation.**
