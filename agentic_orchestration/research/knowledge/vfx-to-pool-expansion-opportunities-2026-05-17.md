# Research — VFX Catalogue to Pool: Expansion Opportunity Audit — 2026-05-17

**Mode:** A (analytical; file inspection)
**Commissioner:** knight-rider (per Matt directive 2026-05-17; Track A reverse direction)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-17-legolas-track-a-reverse-vfx-to-pool-expansion-opportunity-audit.md`
**Parallel context:** Gandalf Track B in-flight (pool-cull decisions from Track A original data); this audit produces net-new expansion data for a post-Track-B cascade item.
**Sources consulted:** All vendor JSONL files in `research/catalogue/`; canonical pool at `~/Games/reincarnated-engine/data/seasonal_elements/pool.json`; cipher-migration paths audit at `research/cipher-migration-paths-audit-2026-05-16.md`

---

## Section 1 — Catalogue Corpus Inventory

### 1.1 Vendors enumerated

All 10 vendor JSONL files at `research/catalogue/<vendor>/full-2026-05-16.jsonl` were read. No additional vendors found beyond those listed.

| Vendor | Pack count | Crawl date | Source |
|---|---|---|---|
| Pimen | 46 packs | 2026-05-16 | `research/catalogue/pimen/full-2026-05-16.jsonl` |
| CraftPix | 7 packs | 2026-05-16 | `research/catalogue/craftpix/full-2026-05-16.jsonl` |
| CreativeKind | 8 packs | 2026-05-16 | `research/catalogue/creativekind/full-2026-05-16.jsonl` |
| Fellor | 7 packs | 2026-05-16 | `research/catalogue/fellor/full-2026-05-16.jsonl` |
| Frostwindz | 15 packs | 2026-05-16 | `research/catalogue/frostwindz/full-2026-05-16.jsonl` |
| Pixogen | 2 packs | 2026-05-16 | `research/catalogue/pixogen/full-2026-05-16.jsonl` |
| Ansimuz | 6 packs | 2026-05-16 | `research/catalogue/ansimuz/full-2026-05-16.jsonl` |
| Brackeys | 1 pack | 2026-05-16 | `research/catalogue/brackeys/full-2026-05-16.jsonl` |
| CodeManu | 3 packs | 2026-05-16 | `research/catalogue/codemanu/full-2026-05-16.jsonl` |
| Pipoya | 5 packs | 2026-05-16 | `research/catalogue/pipoya/full-2026-05-16.jsonl` |
| **Total** | **100 packs** | | |

**Vendors named in dispatch but NOT found in catalogue:** Elthen, chierit, GandalfHardcore. These vendors appear in dispatch scope but no JSONL files exist for them. Noted as knowledge gap — no coverage data available for these vendors.

### 1.2 Concept-name extraction methodology

Concept-names extracted from three fields per asset record:
- `style_tags` array (primary source)
- `vendor_mechanic_tags` array (secondary source)
- `substrate_classification` field (tertiary; cross-check)

Pack-name boilerplate ("Spell Effect", "VFX Pack", "Pixel Art", version numbers) was stripped. Only single-word or close-compound concept tokens with plausible seasonal-element-name register were retained (i.e., evocative, visualizable nouns or adjectives-used-as-nouns). Pure mechanic-type labels (`impact`, `slash`, `projectile`, `hit-spark`, `buff`, `debuff`) were excluded from the candidate pool — these are animation-mechanic labels, not element-vocabulary candidates.

### 1.3 Canonical concept-name corpus (unique, de-duplicated)

Total unique concept-tokens extracted across all vendors: 436 raw tags/tokens. After filtering to element-vocabulary register (evocative nouns, elemental substrates, thematic register words): **28 candidate concept-names** for cross-reference.

**Vendor attribution per concept:**

| Concept | Pimen | CraftPix | CreativeKind | Fellor | Frostwindz | Pixogen | Ansimuz | Brackeys | CodeManu | Pipoya | Vendor count |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| acid | X | X | | | | | | | | | 2 |
| chromatic | | | X | | | | | | | | 1 |
| cosmic | | | X | | X | | | | | | 2 |
| dark | X | | X | | X | | | | | | 3 |
| death | | | | | X | | | | | | 1 |
| divine | X | | X | | X | | | | | | 3 |
| electric | X | | | X | | X | X | | | | 4 |
| explosion | X | X | | | | X | X | X | | | 5 |
| fireworks | | | | | | X | | | | | 1 |
| freeze | | X | | | | | | | | | 1 |
| healing | | X | X | | X | | | | | | 3 |
| holy | X | | X | | X | X | | | | | 4 |
| icicle | | X | | | | | | | | | 1 |
| implosion | | X | | | | | | | | | 1 |
| lightning | X | X | | X | | | X | | | | 4 |
| necrotic | | | | | X | | | | | | 1 |
| poison | | | X | X | | | | | | | 2 |
| portal | | | | | | X | | | | X | 2 |
| shadow | X | | X | | X | | | | | | 3 |
| space | | | X | | | | | | | | 1 |
| stellar | | | X | | X | | | | | | 2 |
| technology | | | | | | X | | | | | 1 |
| thunder | X | | | | | | | | | | 1 |
| time | | | | | | | | | | X | 1 |
| tornado | | X | | | | | | | | | 1 |
| toxic | | | X | X | | | | | | | 2 |
| void | | | | | X | X | | | | | 2 |
| warp | | | | | | | | | | X | 1 |

**Note on canonical-four label surface:** `fire`, `water`, `earth`, `wind` appear as style_tags and substrate labels across many vendors but are the canonical-four structural slot labels, NOT pool entries. They are correctly absent from the element pool (which contains seasonal names, not slot labels). These were excluded from the candidate corpus as structurally ineligible.

**Also in-pool already (confirmed VFX coverage, track here for completeness):**
`crystal` (allow-list/earth; Fellor+Pimen), `dust` (allow-list/wind; Pimen), `frost` (allow-list/wind; Pimen+Fellor+Frostwindz), `gem` (allow-list/earth; Fellor), `hail` (allow-list/wind; Pimen), `ice` (allow-list/water; Pimen+Fellor+Frostwindz+Pixogen), `smoke` (eligible/fire; Pimen+Fellor+Ansimuz), `spark` (allow-list/fire; Pimen+Ansimuz), `stone` (allow-list/earth; Pimen+CreativeKind+Fellor), `typhoon` (allow-list/wind; CraftPix), `blood` (allow-list/water; CodeManu+Frostwindz), `wood` (eligible/earth; Pimen).

---

## Section 2 — Pool Cross-Reference (Inverse of Track A Original)

### 2.1 Cross-reference result

Pool source: `/Users/admin/Games/reincarnated-engine/data/seasonal_elements/pool.json` — 156 entries (81 allow-list / 40 eligible / 35 quarantine), all with `primary_slot` classified across fire/wind/water/earth.

**Result: 28 NOT-IN-POOL concept-names** surface from the catalogue corpus with plausible pool-expansion relevance. 12 pool entries confirmed in-catalogue (not expansion candidates; already in scope).

### 2.2 NOT-IN-POOL concept names

| Concept | Vendor count | Substrate hypothesis | In-pool? | In-pool-but-quarantine? |
|---|:---:|---|:---:|:---:|
| acid | 2 | water/dark-flex | NO | NO |
| chromatic | 1 | neutral/light-flex | NO | NO |
| cosmic | 2 | dark/neutral-flex | NO | NO |
| dark | 3 | dark (substrate label) | NO | NO |
| death | 1 | dark | NO | NO |
| divine | 3 | light/holy-flex | NO | NO |
| electric | 4 | wind/water-flex | NO | NO |
| explosion | 5 | fire/kinetic | NO | NO |
| fireworks | 1 | fire | NO | NO |
| freeze | 1 | water/wind-flex | NO | NO |
| healing | 3 | light/holy | NO | NO |
| holy | 4 | light/holy | NO | NO |
| icicle | 1 | water/wind-flex | NO | NO |
| implosion | 1 | dark/void-flex | NO | NO |
| lightning | 4 | wind/water-flex | NO | NO |
| necrotic | 1 | dark | NO | NO |
| poison | 2 | earth/dark-flex | NO | NO |
| portal | 2 | dark/void-flex | NO | NO |
| shadow | 3 | dark | NO | NO |
| space | 1 | dark/void-flex | NO | NO |
| stellar | 2 | light/dark-flex | NO | NO |
| technology | 1 | neutral/other | NO | NO |
| thunder | 1 | wind | NO | NO |
| time | 1 | neutral/dark-flex | NO | NO |
| tornado | 1 | wind | NO | NO |
| toxic | 2 | earth/dark-flex | NO | NO |
| void | 2 | dark/neutral | NO | NO |
| warp | 1 | dark/void-flex | NO | NO |

**Important structural observation:** `dark`, `light`, `holy`, `shadow`, `cosmic`, `void` are substrates BEYOND the canonical-four (fire/water/earth/wind). The current pool of 156 entries covers only canonical-four slots. The catalogue surfaces a meaningful "beyond canonical-four" expansion zone — these concepts have genuine VFX coverage but no pool slot at all. This is a structural gap, not just a missing-entry gap. Surfacing for gandalf disposition: does the D1 rubric and pool structure need to expand to include non-canonical-four slots?

---

## Section 3 — Per-Candidate Pre-Screening

### 3.1 Screening criteria

Per each NOT-IN-POOL candidate:
- **Substrate hypothesis:** which slot (fire/water/earth/wind or beyond-canonical-four) would this most plausibly occupy?
- **Genre-precedent signal:** ARPG/fantasy/Isekai vocabulary recognition
- **Vendor-coverage strength:** multi-vendor (strong) vs single-vendor (weaker)
- **Canonical-pair-leak risk:** would adding this name structurally re-introduce canonical-four bias?
- **Existing-pool-overlap risk:** semantic duplication with an existing pool entry
- **D1-amenable estimate:** rough hand-estimate of d1_total under existing rubric (genre-precedent + visualizable + fantasy-heroic + vocab-commonness; max 12)

### 3.2 Per-candidate screening table

**REJECT candidates (HIGH leak-risk OR strong overlap OR niche-single-vendor):**

| Name | Reject reason | Vendor coverage |
|---|---|---|
| **dark** | HIGH leak-risk: "dark" is the canonical substrate label for the dark slot; adding it as a pool entry would name the slot directly, re-introducing the structural-bias Drift-14 surfaced (canonical-pair-leak in the element name vocabulary itself) | pimen, creativekind, frostwindz |
| **tornado** | HIGH overlap risk: tornado is semantically identical to existing wind-storm cluster entries (typhoon/cyclone/squall/tempest/hurricane); Track A original flagged 8 wind-storm cluster entries as cull candidates for concentration risk; adding tornado worsens the exact problem Track A found | craftpix only |
| **thunder** | HIGH overlap risk: wind-slot already has 14 allow-list entries including 8 storm-cluster entries flagged by Track A as concentration risk; thunder adds to wind concentration without adding wind diversity; overlaps with typhoon/cyclone/tempest family semantically | pimen only |
| **explosion** | Mechanic-type noun: explosion is an animation mechanic label, not an element-vocabulary seasonal name; genre-precedent as mechanic but not as elemental identity; d1_estimate=6 | 5 vendors (but as mechanic label, not element name) |
| **freeze** | Mechanic-verb-state: freeze is an animation state/status-effect descriptor; ice already in pool (allow-list/water); icicle is ice-derivative; weak as seasonal element name | craftpix only |
| **healing** | Mechanic-type noun: healing is an action-mechanic label; not element-vocabulary register; no canonical-four slot it would fit | craftpix, creativekind, frostwindz |
| **icicle** | Overlap with ice (allow-list/water): icicle is a sub-variant of ice with single-vendor coverage; ice is the canonical form already in pool | craftpix only |
| **technology** | Niche sci-fi register: technology is not ARPG/fantasy/Isekai vocabulary; single-vendor (Pixogen); d1_estimate=4; fails genre-precedent dimension badly | pixogen only |
| **space** | Weak ARPG register: space is too sci-fi for the game's fantasy register; single-vendor; d1_estimate=5 | creativekind only |
| **necrotic** | Adjective form: necrotic is a D&D/tabletop adjective; not common as noun seasonal-element name; semantic overlap with death; single-vendor | frostwindz only |
| **implosion** | Mechanic-type noun: implosion is a physics-mechanic label; single-vendor; d1_estimate=6 | craftpix only |
| **chromatic** | Adjective form; weak noun register: chromatic is a color-theory adjective; weak as fantasy element identity; single-vendor | creativekind only |

**TOTAL REJECT: 12**

**Viable candidates (NOT rejected — proceed to Section 4 tiering):**

acid, cosmic, death, divine, electric, fireworks, holy, lightning, poison, portal, shadow, stellar, time, toxic, void, warp

**TOTAL VIABLE: 16**

### 3.3 Viable candidate detailed screening

**acid**
- Substrate hypothesis: water/dark-flex (chemical-corrosive; distinct from poison-biological)
- Genre-precedent: strong — acid damage type ubiquitous in ARPG (Path of Exile, Diablo); corrosive/chemical register is established genre vocabulary
- Vendor-coverage: 2 vendors (Pimen + CraftPix); Pimen ships a dedicated Acid Spell Effect pack
- Canonical-pair-leak risk: LOW — acid has no structural binding to any canonical-four slot name; it implies a distinct chemical sub-element not captured by fire/water/earth/wind framing
- Existing-pool-overlap risk: NONE — no pool entry covers acid/corrosive register
- D1-amenable estimate: 9/12 (genre-precedent=3, visualizable=3, fantasy-heroic=2, vocab-commonness=1; acid is somewhat harsh as fantasy vocabulary)
- Note: the geometry-element-coverage matrix (elrond's work) identified acid as a distinct substrate (`acid` column) with elrond's Level-2 adjudication; this aligns with expansion candidacy

**cosmic**
- Substrate hypothesis: dark/neutral-flex (cosmic-stellar register distinct from shadow-arcane dark)
- Genre-precedent: moderate — cosmic appears in ARPG (PoE has cosmic micro-transactions, Isekai often has cosmological themes); not as common as fire/lightning
- Vendor-coverage: 2 vendors (CreativeKind Space Spell Effects + Frostwindz Starcaller)
- Canonical-pair-leak risk: LOW — cosmic has no canonical-four binding
- Existing-pool-overlap risk: NONE directly; but stellar (another candidate) is semantically close
- D1-amenable estimate: 8/12 (genre-precedent=2, visualizable=2, fantasy-heroic=2, vocab-commonness=2)

**death**
- Substrate hypothesis: dark (necrotic/death-magic sub-register, distinct from shadow-arcane)
- Genre-precedent: strong — death is core ARPG/fantasy/Isekai vocabulary (death knights, death magic, death damage type)
- Vendor-coverage: 1 vendor (Frostwindz Deathbringer + Necromancer); but both are Frostwindz packs, same vendor family
- Canonical-pair-leak risk: LOW — death is a thematic noun, not a canonical-four label
- Existing-pool-overlap risk: NONE — no pool entry covers death/necrotic register
- D1-amenable estimate: 8/12 (genre-precedent=3, visualizable=2, fantasy-heroic=2, vocab-commonness=1; "death" is blunt/direct, may score lower on fantasy-heroic elegance)

**divine**
- Substrate hypothesis: light/holy-flex (divine is the adjective form of holy; strong genre-synonym)
- Genre-precedent: strong — divine appears throughout ARPG/fantasy (Divine Orb in PoE, divine damage type, divine smite in D&D-derived games, Isekai isekai reincarnation as divine intervention)
- Vendor-coverage: 3 vendors (CreativeKind Holy Spell Effects, Pimen Holy Spell Effect, Frostwindz Paladin/Priest)
- Canonical-pair-leak risk: LOW — divine has no canonical-four binding; it is a distinct substrate adjective
- Existing-pool-overlap risk: NONE — no pool entry covers divine/holy register; but note it overlaps semantically with the holy candidate below
- D1-amenable estimate: 9/12 (genre-precedent=3, visualizable=2, fantasy-heroic=3, vocab-commonness=1)

**electric**
- Substrate hypothesis: wind/water-flex (electricity bridges wind-storm and water substrates in genre; thunder/lightning are adjacent)
- Genre-precedent: strong — electric is standard ARPG damage type vocabulary (electric/lightning often synonymous in genre)
- Vendor-coverage: 4 vendors (Pimen Thunder packs have electric tag, Fellor Lightning VFX, Pixogen electric-bolt, Ansimuz electric-explosion); strongest multi-vendor signal
- Canonical-pair-leak risk: LOW — electric has no canonical-four binding; though it is adjacent to wind-slot thunder/lightning, "electric" is the broader phenomenon, not a slot-aligned word
- Existing-pool-overlap risk: LOW — no pool entry covers electric directly; thunder (wind) and lightning (not in pool) are the nearest pool-adjacent terms; but electric is distinct enough as the base phenomenon
- D1-amenable estimate: 9/12 (genre-precedent=3, visualizable=3, fantasy-heroic=2, vocab-commonness=1)
- Note: existing overlap with thunder/lightning warrants flagging — if wind-storm cluster gets culled per Track A, electric could serve as a cleaner wind/lightning-type anchor with less concentration risk than storm vocabulary

**fireworks**
- Substrate hypothesis: fire (spectacle/celebratory fire register)
- Genre-precedent: weak-to-moderate — fireworks appears in games but is not core ARPG element vocabulary; more spectacle/ambient than combat-element identity
- Vendor-coverage: 1 vendor (Pixogen only)
- Canonical-pair-leak risk: MEDIUM — fireworks implies fire-ish register; though not a direct canonical-four name, it could bias selector toward fire-conforming names if added to fire slot
- Existing-pool-overlap risk: LOW — no pool entry directly, but smoke/blaze/flare are adjacent
- D1-amenable estimate: 7/12

**holy**
- Substrate hypothesis: light/holy (primary holy/divine/radiant register; distinct from fire/water/earth/wind)
- Genre-precedent: very strong — holy is one of the most genre-recognized magical registers in ARPG/fantasy/Isekai (Diablo Holy magic, PoE Radiance/Faith adjacents, D&D-derived holy damage)
- Vendor-coverage: 4 vendors (Pimen Holy Spell Effect, CreativeKind Holy Spell Effects, Pixogen holy category, Frostwindz Paladin + Priest); strongest multi-vendor convergence in the not-in-pool candidate set
- Canonical-pair-leak risk: LOW — holy has no canonical-four binding; it is a distinct substrate beyond canonical-four
- Existing-pool-overlap risk: NONE — no pool entry covers holy register; divine is semantically close but holy is the more direct noun form
- D1-amenable estimate: 10/12 (genre-precedent=3, visualizable=3, fantasy-heroic=3, vocab-commonness=1)
- Structural gap note: holy is currently a "beyond canonical-four" substrate — if the pool expands beyond fire/wind/water/earth slots, holy is the strongest candidate to anchor a light/divine slot

**lightning**
- Substrate hypothesis: wind/water-flex (lightning is ambiguous — wind-storm in most ARPG, water-storm in others; this ambiguity is the main concern)
- Genre-precedent: very strong — lightning is one of the most universally recognized ARPG damage types and element names (Final Fantasy Thunder/Lightning, PoE Lightning, Diablo Lightning)
- Vendor-coverage: 4 vendors (Pimen Thunder Spell Effects have lightning tags, Fellor Lightning VFX Pack, CraftPix Top-Down Wind and Lightning, Ansimuz Gothicvania lightning); strong multi-vendor signal
- Canonical-pair-leak risk: MEDIUM — lightning is not a canonical-four label but has strong wind-slot alignment; if wind-storm cluster is culled per Track A and lightning is added, it could effectively become the dominant wind-anchor name with implicit canonical binding
- Existing-pool-overlap risk: MEDIUM — pool already has thunder as a wind-cluster overlap (see thunder REJECT above), typhoon/cyclone/squall/gust/gale/howl in wind allow-list; lightning has a different character (electromagnetic vs atmospheric) but does add to wind concentration; however lightning distinctively differs from storm vocabulary in that it describes a phenomenon that can flex to water
- D1-amenable estimate: 9/12 (genre-precedent=3, visualizable=3, fantasy-heroic=2, vocab-commonness=1)

**poison**
- Substrate hypothesis: earth/dark-flex (biological-venom register distinct from acid/chemical; earth sub-register via nature/biological pathway)
- Genre-precedent: very strong — poison is one of the core ARPG status-effect damage types (PoE Poison, Diablo Poison, Final Fantasy Poison status)
- Vendor-coverage: 2 vendors (CreativeKind Poison Spell Effects + Fellor Poison VFX Pack); both ship dedicated poison packs
- Canonical-pair-leak risk: LOW — poison has no canonical-four binding; it is a distinct biological-venom sub-element
- Existing-pool-overlap risk: NONE — no pool entry covers poison register; acid is adjacent but acid is chemical-corrosive while poison is biological-venom (elrond's Level-2 distinction confirmed in geometry matrix)
- D1-amenable estimate: 9/12 (genre-precedent=3, visualizable=3, fantasy-heroic=2, vocab-commonness=1)

**portal**
- Substrate hypothesis: dark/void-flex (spatial-transit; distinct from void-absence which is more black-hole register)
- Genre-precedent: moderate — portal is common in fantasy gaming (teleport portals, dimensional gates) but less common as an element-vocabulary name specifically
- Vendor-coverage: 2 vendors (Pixogen void-portal category + Pipoya FREE VFX Warp Portal); note Pixogen license is verified-with-attribution
- Canonical-pair-leak risk: LOW — portal has no canonical-four binding
- Existing-pool-overlap risk: LOW — warp is semantically adjacent (see warp below); adding both portal and warp would create semantic-pair
- D1-amenable estimate: 8/12 (genre-precedent=2, visualizable=3, fantasy-heroic=2, vocab-commonness=1)

**shadow**
- Substrate hypothesis: dark (shadow-arcane sub-register of dark; strongly dark-slot-aligned)
- Genre-precedent: very strong — shadow is one of the most recognized ARPG/fantasy/Isekai element names (PoE Shadow class, Final Fantasy Shadow damage, Isekai shadow magic, stealth/darkness archetype)
- Vendor-coverage: 3 vendors (Pimen Dark Spell Effect has shadow tag, CreativeKind Dark Spell Effects has shadow tag, Frostwindz Dark Mage + Rogue with shadow-stealth)
- Canonical-pair-leak risk: MEDIUM — shadow is strongly dark-slot-aligned; if a dark slot is ever added to the canonical-four structure, shadow would effectively name it directly (similar to how hurricane names the wind-storm cluster). Flagged but lower severity than dark itself since shadow is a distinct vocabulary word, not the slot label
- Existing-pool-overlap risk: LOW to MEDIUM — dark (rejected above as HIGH-RISK) would be the pool overlap; since dark is rejected, shadow has no direct overlap. However shadow + dark together would recreate the canonical-pair-leak problem. Since dark is REJECTED, shadow alone has no overlap with existing pool entries
- D1-amenable estimate: 9/12 (genre-precedent=3, visualizable=3, fantasy-heroic=2, vocab-commonness=1)

**stellar**
- Substrate hypothesis: light/dark-flex (stellar spans cosmic-light and dark-void registers; ambiguous slot fit)
- Genre-precedent: moderate — stellar appears in ARPG/Isekai (star magic, celestial themes, astromancer classes) but less universally than holy or shadow
- Vendor-coverage: 2 vendors (Frostwindz Starcaller + CreativeKind Space Spell Effects / stellar-magic tags)
- Canonical-pair-leak risk: LOW — stellar has no canonical-four binding; ambiguous slot flex is a design question, not a leak risk
- Existing-pool-overlap risk: MEDIUM — cosmic (another candidate) is semantically adjacent; adding both stellar and cosmic would create a semantic cluster that could bias selector toward cosmological vocabulary
- D1-amenable estimate: 8/12 (genre-precedent=2, visualizable=2, fantasy-heroic=3, vocab-commonness=1)

**time**
- Substrate hypothesis: neutral/dark-flex (temporal magic; no natural canonical-four slot; dark-flex because time-manipulation is often dark/arcane-adjacent in ARPG)
- Genre-precedent: strong — time magic is a well-established ARPG/JRPG register (Final Fantasy Time Mage, Chrono Trigger time magic, PoE temporal chains, Isekai time-stop abilities); the vocabulary reads clearly in genre context
- Vendor-coverage: 1 vendor (Pipoya only; but the TIME MAGIC pack is highly specific with 6 distinct temporal mechanic animation categories: Quickly/Double/Triple/Slowly/Reverse/Stop)
- Canonical-pair-leak risk: LOW — time has no canonical-four binding whatsoever; it is genuinely orthogonal to fire/water/earth/wind
- Existing-pool-overlap risk: NONE — no pool entry is remotely adjacent to time/temporal
- D1-amenable estimate: 7/12 (genre-precedent=3, visualizable=2, fantasy-heroic=1, vocab-commonness=1; "time" is extremely common but may score low on fantasy-heroic distinctiveness)
- Note: single-vendor reduces signal strength; but Pipoya TIME MAGIC is the most substrate-specific single pack in the catalogue for this register

**toxic**
- Substrate hypothesis: earth/dark-flex (toxic = biological-venom register; near-synonym to poison)
- Genre-precedent: moderate — toxic appears in gaming but more as an adjective-status (toxic cloud, toxic damage) than as a standalone element noun; poison is the more canonical noun form
- Vendor-coverage: 2 vendors (CreativeKind Poison Spell Effects has toxic tag, Fellor Poison VFX Pack has toxic tag)
- Canonical-pair-leak risk: LOW — toxic has no canonical-four binding
- Existing-pool-overlap risk: HIGH — toxic is a near-synonym to poison (the other candidate); adding both toxic and poison to the pool would create a semantic-overlap pair with minimal D1 diversity value. One of the two (likely poison as the stronger noun form) is the appropriate candidate; not both
- D1-amenable estimate: 7/12

**void**
- Substrate hypothesis: dark/neutral (void = spatial-absence register; distinct from shadow-arcane dark)
- Genre-precedent: strong — void is well-established in ARPG/Isekai vocabulary (PoE Void-touched, void magic in Final Fantasy/Isekai, the void as cosmological absence register)
- Vendor-coverage: 2 vendors (Pixogen void category with 8 dedicated void animations + Frostwindz Warlock void-adjacent-arcane register); note Pixogen license is verified-with-attribution
- Canonical-pair-leak risk: LOW — void has no canonical-four binding; it is a novel substrate entirely orthogonal to fire/water/earth/wind
- Existing-pool-overlap risk: NONE — no pool entry covers void/spatial-absence
- D1-amenable estimate: 9/12 (genre-precedent=3, visualizable=3, fantasy-heroic=2, vocab-commonness=1)

**warp**
- Substrate hypothesis: dark/void-flex (teleportation/spatial-transit; distinct from void-absence)
- Genre-precedent: moderate — warp appears in Isekai/sci-fi gaming but less in pure ARPG fantasy; borderline register fit
- Vendor-coverage: 1 vendor (Pipoya FREE VFX Warp Portal; 5 color variants)
- Canonical-pair-leak risk: LOW — warp has no canonical-four binding
- Existing-pool-overlap risk: MEDIUM — portal (another candidate) is semantically adjacent; adding both warp and portal creates near-synonymous pair
- D1-amenable estimate: 7/12 (genre-precedent=2, visualizable=3, fantasy-heroic=1, vocab-commonness=1)

---

## Section 4 — Priority-Ranked Shortlist

### Tier definitions

- **TIER 1 — STRONG CANDIDATES:** multi-vendor coverage + clean substrate + LOW leak-risk + LOW overlap-with-existing + estimated d1_total ≥ 8; ready for gandalf disposition, likely allow-list candidates
- **TIER 2 — VIABLE CANDIDATES:** good coverage but one weak dimension (single-vendor OR substrate-ambiguous OR moderate overlap risk); ready for gandalf disposition, likely eligible-tier candidates
- **TIER 3 — INVESTIGATE:** interesting but ambiguous; needs gandalf judgment; low-priority
- **REJECT:** HIGH leak-risk OR strong-overlap-with-existing OR niche-single-vendor-only; do not surface to gandalf disposition

### 4.1 TIER 1 — STRONG CANDIDATES (5 candidates)

| Name | Substrate hypothesis | Vendors with coverage | Vendor count | Leak-risk | Overlap-risk | D1-est | Rationale |
|---|---|---|:---:|---|---|:---:|---|
| **holy** | light/holy (beyond canonical-four) | Pimen, CreativeKind, Pixogen, Frostwindz | 4 | LOW | NONE | 10 | Strongest multi-vendor convergence; universal ARPG genre recognition; clean substrate; no pool overlap; high D1 estimate; anchors potential light/divine slot if pool expands beyond canonical-four |
| **electric** | wind/water-flex | Pimen, Fellor, Pixogen, Ansimuz | 4 | LOW | LOW | 9 | Strong multi-vendor signal; core ARPG damage type; clean VFX coverage; no pool overlap; distinct from storm vocabulary (avoids wind-storm cluster concentration risk); could serve as cleaner lightning/thunder anchor post-Track-A wind-storm cull |
| **poison** | earth/dark-flex | CreativeKind, Fellor | 2 | LOW | NONE | 9 | Strong genre-precedent; dedicated vendor packs (not just tag mentions); distinct from acid (chemical vs biological); clean earth-adjacency; universal ARPG recognition |
| **void** | dark/neutral (beyond canonical-four) | Pixogen, Frostwindz | 2 | LOW | NONE | 9 | Strong genre-precedent; distinct spatial-absence substrate not covered in pool; clean VFX evidence; anchors potential void/dark slot if pool expands beyond canonical-four |
| **shadow** | dark (beyond canonical-four) | Pimen, CreativeKind, Frostwindz | 3 | MEDIUM | LOW | 9 | Very strong genre-precedent; excellent VFX coverage; medium leak-risk flagged (dark-slot-aligned); risk is manageable because dark slot is not currently in canonical-four structure; needs gandalf disposition on whether MEDIUM leak-risk disqualifies or is acceptable for a beyond-canonical-four expansion |

### 4.2 TIER 2 — VIABLE CANDIDATES (8 candidates)

| Name | Substrate hypothesis | Vendors with coverage | Vendor count | Weak dimension | D1-est | Rationale |
|---|---|---|:---:|---|:---:|---|
| **acid** | water/dark-flex | Pimen, CraftPix | 2 | Substrate-ambiguous (chemical register fits neither water nor dark cleanly) | 9 | Strong genre-precedent; elrond identified acid as Level-2 distinct substrate; but slot assignment is ambiguous for current canonical-four structure |
| **divine** | light/holy-flex | CreativeKind, Pimen, Frostwindz | 3 | Semantic-overlap with holy (both light/divine register) | 9 | Strong coverage; high D1 estimate; but semantic-overlap with holy means only one of {holy, divine} is likely needed; holy is the cleaner noun form |
| **lightning** | wind/water-flex | Pimen, Fellor, CraftPix, Ansimuz | 4 | MEDIUM overlap-risk (wind-storm cluster + existing pool concentration) | 9 | Excellent coverage and D1 estimate; relegated to Tier 2 due to MEDIUM overlap-risk with existing wind-storm cluster; post-Track-A-cull this may upgrade to Tier 1 if 4+ wind-storm entries are removed |
| **cosmic** | dark/neutral-flex | CreativeKind, Frostwindz | 2 | Moderate genre-precedent (not as universal as core ARPG elements) | 8 | Distinct substrate; no pool overlap; multi-vendor; but genre-precedent weaker than Tier 1 entries |
| **death** | dark (beyond canonical-four) | Frostwindz | 1 | Single-vendor; blunt register (may score lower on fantasy-heroic elegance) | 8 | Core ARPG/Isekai vocabulary; distinct necrotic register; but single-vendor surface reduces signal strength |
| **portal** | dark/void-flex | Pixogen, Pipoya | 2 | Mechanic-adjacent (portal is an object/mechanic more than an element-identity) | 8 | Distinct spatial-transit register; multi-vendor; but registers more as a mechanic noun than an element name |
| **stellar** | light/dark-flex | Frostwindz, CreativeKind | 2 | Ambiguous slot (bridges light and dark); cosmic overlap-risk | 8 | Distinct cosmological register; but slot ambiguity and cosmic semantic-overlap reduce priority |
| **time** | neutral/dark-flex | Pipoya | 1 | Single-vendor; "time" may score low on fantasy-heroic distinctiveness despite strong genre-precedent | 7 | Genuinely novel substrate orthogonal to canonical-four; Pipoya TIME MAGIC pack is highly specialized; single-vendor reduces signal; interesting expansion that opens temporal-magic vocabulary |

### 4.3 TIER 3 — INVESTIGATE (3 candidates)

| Name | Why | Vendor count |
|---|---|:---:|
| **fireworks** | Interesting fire-register concept with Pixogen coverage, but spectacle-adjacent rather than element-identity; single-vendor; MEDIUM canonical leak in fire-slot direction; requires gandalf judgment on whether fire-slot already has sufficient coverage | 1 |
| **warp** | Distinct spatial-transit register distinct from portal (teleport = warp vs gateway = portal); single-vendor Pipoya; but semantic-overlap with portal reduces independent value; low priority unless portal is also advanced | 1 |
| **toxic** | Two-vendor coverage but near-synonym to poison; if poison advances to Tier 1, toxic has no independent value; if poison is rejected, toxic inherits poison's candidacy at lower strength | 2 |

### 4.4 REJECT (12 candidates)

| Name | Reject rationale |
|---|---|
| dark | HIGH leak-risk: names the dark substrate slot directly; canonical-bias re-introduction |
| tornado | HIGH overlap-risk: wind-storm cluster (typhoon/cyclone/squall/hurricane) + Track A cull targets; worsens concentration |
| thunder | HIGH overlap-risk: wind-storm cluster concentration + single-vendor |
| explosion | Mechanic-type noun; not element-vocabulary register |
| freeze | Verb-state noun; mechanic-type; ice (allow-list/water) already in pool |
| healing | Mechanic-type noun; not element-vocabulary register |
| icicle | Ice-derivative; ice already in pool; single-vendor |
| technology | Sci-fi register; not ARPG/fantasy vocabulary; single-vendor |
| space | Sci-fi register; weak ARPG fit; single-vendor |
| necrotic | Adjective form; single-vendor; semantic-overlap with death candidate |
| implosion | Mechanic-type noun; single-vendor |
| chromatic | Adjective form; single-vendor; weak as fantasy element noun |

---

## Section 5 — Aggregate Statistics and Hand-off

### 5.1 Aggregate statistics

| Metric | Count |
|---|---|
| Catalogue vendors enumerated | 10 (Elthen/chierit/GandalfHardcore not found in catalogue files — knowledge gap) |
| Total packs across corpus | 100 |
| Unique concept-tokens extracted (raw) | 436 |
| Unique concept-names in element-vocabulary register | 28 |
| Pool entries confirmed in-catalogue (already covered) | 12 |
| NOT-IN-POOL candidates surfaced (raw) | 28 |
| REJECT | 12 |
| TIER 3 — Investigate | 3 |
| TIER 2 — Viable | 8 |
| TIER 1 — Strong | 5 |

### 5.2 Per-substrate breakdown (expansion opportunity by slot)

| Substrate | TIER 1 candidates | TIER 2 candidates | TIER 3 | Notes |
|---|:---:|:---:|:---:|---|
| fire | 0 | 0 | 1 (fireworks) | Fire pool already well-populated (20 allow-list, 11 eligible); fire-slot expansion has lowest priority |
| wind | 0 | 1 (lightning — MEDIUM overlap) | 0 | Wind-storm cluster concentration problem dominates; Track A cull should resolve before expansion; post-cull lightning may upgrade to Tier 1 |
| water | 0 | 0 | 0 | Water pool reasonably populated (14 allow-list); no strong beyond-water expansion candidates in catalogue |
| earth | 1 (poison — earth-flex) | 1 (acid — ambiguous earth-flex) | 0 | Earth-adjacent expansion: poison and acid represent biological/chemical sub-elements adjacent to earth; both useful |
| dark/light/beyond-C4 | 4 (holy, void, shadow + acid/poison as flex) | 5 (divine, cosmic, death, portal, stellar) | 2 (warp, toxic) | DOMINANT expansion zone: catalogue is richest in dark/light/beyond-canonical-four substrates; this reflects that the current pool covers only canonical-four slots, missing the non-canonical element vocabulary that VFX vendors consistently ship |
| neutral/temporal | 1 | 1 (time) | 0 | Time as genuinely novel temporal register; no current pool coverage |

**Key structural finding:** The catalogue's expansion signal concentrates overwhelmingly in BEYOND-CANONICAL-FOUR substrates (dark/light/holy/void/cosmic). The current 156-entry pool covers only fire/wind/water/earth slots. If gandalf disposition confirms the game's D1 vocabulary should remain strictly canonical-four-anchored, the Tier 1 expansion candidates (holy, void, shadow, electric) would need to be force-fit into existing slots — electric → wind-flex, shadow → dark slot (if created), holy → light slot (if created), void → neutral or dark slot (if created). If the pool is meant to stay canonical-four-only, the expansion opportunity is limited to electric (wind-flex) and poison/acid (earth-flex).

### 5.3 Cross-reference to Track A original — rebalancing opportunities

Track A original (as summarized in gandalf Track B dispatch) found:
- Wind-slot worst-affected with 28.9% RED entries
- 8 wind-storm cluster entries flagged as cull candidates: hurricane/gale/cyclone/tempest/gust/howl/typhoon/squall

This audit's findings on wind:
- **No TIER 1 wind candidates surfaced** — the catalogue does not offer clean wind-expansion vocabulary beyond the storm-cluster problem
- **Lightning (TIER 2)** is the only plausible wind-adjacent expansion, but it carries MEDIUM overlap-risk with the existing cluster; if Track A culls 4+ storm-cluster entries, lightning would become viable post-cull as a distinct electromagnetic-wind anchor
- **electric (TIER 1)** is wind/water-flex and represents a cleaner expansion than any storm vocabulary — it would serve as a distinct wind-adjacent anchor without storm-concentration risk
- **Rebalancing assessment:** If Track A culls 5+ wind-storm entries, this audit surfaces 1-2 wind-adjacent replacements (electric + lightning post-cull) — partial rebalancing but not full numerical replacement. Wind-slot would end up smaller but less concentrated. This is the coherent rebalancing call: cull 5+ storm-cluster entries, add electric (and possibly lightning post-cull) as distinct wind/electrical anchors.

### 5.4 Structural gap observation for gandalf disposition

The single most significant finding from this audit is the **beyond-canonical-four structural gap:**

The catalogue consistently ships VFX in dark, light/holy, void, cosmic, and poison/acid registers that have no pool-slot equivalents. The current pool's 156 entries are exclusively fire/wind/water/earth-slotted. The 4 strongest Tier 1 candidates (holy, electric, void, shadow) either: (a) map to a non-existent slot (holy=light, void=void, shadow=dark) or (b) flex to an existing slot in an ambiguous way (electric=wind-flex).

Gandalf disposition question (NOT a legolas recommendation): Does the D1 rubric and pool structure scope to canonical-four exclusively, or does the team intend to expand to a 6-8 element model (fire/wind/water/earth + dark + light + void/other)? The answer determines whether Tier 1 candidates holy/void/shadow are viable at all.

### 5.5 Hand-off for gandalf disposition (post-Track-B cascade)

**TIER 1 candidates for disposition (5 entries):**

| Name | Substrate | Vendor coverage | Leak-risk | Overlap-risk | D1-est |
|---|---|---|---|---|:---:|
| holy | light/holy (beyond C4) | Pimen + CreativeKind + Pixogen + Frostwindz | LOW | NONE | 10 |
| electric | wind/water-flex | Pimen + Fellor + Pixogen + Ansimuz | LOW | LOW | 9 |
| poison | earth/dark-flex | CreativeKind + Fellor | LOW | NONE | 9 |
| void | dark/neutral (beyond C4) | Pixogen + Frostwindz | LOW | NONE | 9 |
| shadow | dark (beyond C4) | Pimen + CreativeKind + Frostwindz | MEDIUM | LOW | 9 |

**TIER 2 candidates for disposition (8 entries):**

| Name | Substrate | Vendor count | Primary concern |
|---|---|:---:|---|
| acid | water/dark-flex | 2 | Substrate ambiguity; no slot in current C4 structure |
| divine | light/holy-flex | 3 | Semantic-overlap with holy; one or the other, not both |
| lightning | wind/water-flex | 4 | MEDIUM overlap-risk with wind-storm cluster; post-Track-A-cull upgrade path |
| cosmic | dark/neutral-flex | 2 | Moderate genre-precedent |
| death | dark (beyond C4) | 1 | Single-vendor |
| portal | dark/void-flex | 2 | Mechanic-adjacent noun register |
| stellar | light/dark-flex | 2 | Slot ambiguity; cosmic overlap |
| time | neutral/dark-flex | 1 | Single-vendor; novel but orthogonal register |

**Per-candidate empirical data:** see Section 3.3 detailed screening above.

**Disposition perimeter (do NOT decide here):** which candidates land, at what d1_status, and at what slot. Gandalf's call. Legolas's output is the empirical tier classification and per-candidate data package.

---

## Knowledge Gaps

1. **Three vendors in dispatch scope not found:** Elthen, chierit, GandalfHardcore. No JSONL files exist for these vendors. If these vendors were crawled and their data exists elsewhere, this audit may have missed concepts they contribute. Coverage estimate: Elthen is a character/monster vendor (Step B Tier-1 context); chierit and GandalfHardcore are likely character-specialist vendors per dispatch context. VFX-specific gap is assessed as LOW-risk (these vendors are less likely to be VFX specialists), but flagged for completeness.

2. **Pixogen license status:** Pixogen Full Pack (EUR 19.99) license was verified by Matt 2026-05-16 (proprietary-with-attribution; see `research/catalogue/pixogen/findings-summary-2026-05-16.md`). Pixogen is included in this audit's coverage data. Attribution requirement for void/electric concepts derived from Pixogen: credit "Antoine Fauville / AFGameAssets."

3. **D1-amenable estimates are hand-estimates only:** not load-bearing; rocket performs actual D1 rubric scoring. These estimates are calibration signals only.

4. **Beyond-canonical-four slot structure:** this audit assumes the pool remains canonical-four-slotted unless gandalf disposition confirms expansion. If the pool structure expands, Tier 1 candidates (holy/void/shadow) become immediately viable at high priority. If it does not expand, electric (wind-flex) and poison/acid (earth-flex) are the only structurally clean additions.

---

## Source list

| Source | Type | Location |
|---|---|---|
| Canonical element pool | Primary | `/Users/admin/Games/reincarnated-engine/data/seasonal_elements/pool.json` (156 entries) |
| Pimen catalogue | Primary | `research/catalogue/pimen/full-2026-05-16.jsonl` (46 packs) |
| CraftPix catalogue | Primary | `research/catalogue/craftpix/full-2026-05-16.jsonl` (7 packs) |
| CreativeKind catalogue | Primary | `research/catalogue/creativekind/full-2026-05-16.jsonl` (8 packs) |
| Fellor catalogue | Primary | `research/catalogue/fellor/full-2026-05-16.jsonl` (7 packs) |
| Frostwindz catalogue | Primary | `research/catalogue/frostwindz/full-2026-05-16.jsonl` (15 packs) |
| Pixogen catalogue | Primary | `research/catalogue/pixogen/full-2026-05-16.jsonl` (2 packs) |
| Ansimuz catalogue | Primary | `research/catalogue/ansimuz/full-2026-05-16.jsonl` (6 packs) |
| Brackeys catalogue | Primary | `research/catalogue/brackeys/full-2026-05-16.jsonl` (1 pack) |
| CodeManu catalogue | Primary | `research/catalogue/codemanu/full-2026-05-16.jsonl` (3 packs) |
| Pipoya catalogue | Primary | `research/catalogue/pipoya/full-2026-05-16.jsonl` (5 packs) |
| Pixogen findings summary | Primary | `research/catalogue/pixogen/findings-summary-2026-05-16.md` |
| Cipher migration paths audit | Cross-reference | `research/cipher-migration-paths-audit-2026-05-16.md` |
| Geometry-element coverage matrix | Cross-reference | `research/curated/geometry-element-coverage-matrix-2026-05-16.md` |
| Track A original (inline) | Cross-reference | Summarized in gandalf Track B dispatch `2026-05-16-gandalf-drift-14-track-b-pool-cull-and-selector-hardfloor-synthesis.md` |

---

*Authored by legolas, 2026-05-17. Dispatch: `2026-05-17-legolas-track-a-reverse-vfx-to-pool-expansion-opportunity-audit.md`.*
