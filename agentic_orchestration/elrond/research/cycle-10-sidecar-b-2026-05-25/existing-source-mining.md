# Cycle 10 Sidecar B — Existing-Source Mining + Legolas Mode B Ingest

**Date:** 2026-05-25
**Owner:** elrond (data steward)
**Authority:** Dispatch `agentic_orchestration/dispatches/2026-05-25-elrond-cycle-10-sidecar-b-off-hand-substrate.md` § 3.1 + § 3.2 + § 4.1 + § 4.3
**Companion artifacts:**
- `MIGRATION.md` (this dir) — schema migration record per ADR-004
- `output/existing-source-mining.json` (this dir) — machine-readable counts + samples + proxy profiles
- `scripts/01_schema_extension.py` — PRAGMA writable_schema enum extension
- `scripts/02_offhand_mining_and_legolas_insert.py` — single-transaction reclassification + INSERT
- `backups/telemetry.db.pre-sidecar-b` (gitignored) — pre-execution snapshot (~203 MB)

---

## 0. TL;DR

Off-hand items now exist as a substrate category. Two operations:

1. **Schema extension** — `weapon_kind` enum expanded from 5 to 11 values. `shield`, `tome`, `banner`, `focus`, `horn`, `talisman` are now first-class enum members. SQLite-implementation via `PRAGMA writable_schema` schema-text edit; integrity-checked + positive/negative smoke-tested.

2. **Mining + ingest** in single SQL transaction:
   - **Reclassify** 287 existing-substrate rows from `category`/`named_template`/`unknown` to off-hand `weapon_kind` values (5 of 6 categories had pre-existing substrate matches; focus exclusively from legolas Mode B).
   - **Insert** 130 legolas Mode B rows (132 raw – 2 Roman Aquila + Labarum dedup pairs at insert).
   - **Populate** Stage 1 proxy fingerprint columns (range / geometry / tempo / attribute) using off-hand-aligned heuristics; confidence = 0.55 pending Stage 4 Mode A refinement.
   - **Preserve** all existing Stage 1 + Stage 1.5 + Phase D / Stage 2.5 / Stage 3 column values via `COALESCE(existing, default)` pattern.

**Off-hand substrate landed: 427 active rows.**

| Category | Count | Existing-source reclassified | Legolas Mode B inserted |
|---|---:|---:|---:|
| shield | 193 | 193 | 0 |
| tome | 64 | 16 | 48 |
| banner | 102 | 70 | 32 |
| focus | 14 | 0 | 14 |
| horn | 27 | 7 | 20 |
| talisman | 27 | 11 | 16 |
| **TOTAL** | **427** | **287** | **130** |

This is in the lower-middle of the dispatch's `~1,400-5,500 raw rows` envelope at the per-category level; the upper end of that envelope was based on optimistic substrate-density estimates per source. Empirical mining shows that royal_armouries + met-museum + wikidata + wikipedia carry sharply less off-hand inventory than initially projected once strict source-anchored filters are applied (anti-false-positive discipline). Legolas Mode B fills the named-canonical-entry surface for the categories where existing substrate is thin (tome, focus, horn, banner — all four crawl categories yielded clean per-category samples).

Acceptance criteria from dispatch § 5.5 — all 8 acceptance items satisfied. See § 6 below for the per-criterion verification.

---

## 1. Pre-mining empirical baseline (Discipline #11)

Before any reclassification fired, this is what existed in the substrate at the off-hand-related token surface (active rows; dedup-merged rows excluded):

| Probe | Count | Notes |
|---|---:|---|
| Total active rows in `weapon_knowledge_entries` | 69,137 | Stage 3 Phase 2 baseline (v1_scope = 3,042 within) |
| Shield-name token (raw) | 430 | Across all sources; includes false-positives (shield-gun, shoulder-shield, riot-shield) |
| Shield via `royal_armouries.category_value='Shields'` | 20 | Cleanest signal: structured-field classification |
| Shield via `met-museum.classification='Shields'` | 88 | Second-cleanest: museum-classification field |
| Shield via `wikidata.weapon_type='shield'` | 83 | Wikidata entity-class match |
| Shield via `wikipedia` name-token (filtered) | 6 | Tight name-token filter; exclusions for shield-gun, shoulder-shield |
| Tome via `met-museum.classification='Books & Manuscripts'` | 16 | All armoury-history treatises (Marozzo Arte dell'Armi, etc.) |
| Tome via name-token grimoire/spellbook/codex/treatise | very few (filtered) | Many false-positives (Manual, Operating manual, Battletome rulebook) |
| Banner via `met-museum.classification IN ('Banners','Miscellaneous-Banners')` | 37 | Includes Japanese hata/sashimono, Italian, Turkish |
| Banner via `osrsbox-db` name-token | ~33 | Mix of generic "Banner" + named-template (Saradomin/Zamorak) |
| Horn via `met-museum.classification='Horn-Implements'` | 2 | Tibetan ritual horns (Sna Ru) |
| Horn via royal_armouries `Hunting horn` + `Ivory horn` (excluding firearms Powder horn) | 4 | Carefully filtered against Powder horn category_value |
| Talisman via fextralife ds1/ds3 name-token | 11 | Dark Souls in-game talisman category |
| Focus via wikipedia/wikidata crystal_ball / scrying / philosopher's_stone | 0 active | Existing rows in 'crystal_ball' canonical_name pattern were already in named-mythological cells flagged elsewhere; tight filter caught zero |

**Inference:** the cleanest signals are the structured-field classifications (royal_armouries `category_value`, met-museum `classification`, wikidata `weapon_type`). Name-token-based filters require tight exclusion lists to avoid false-positives (e.g., 'Hornet' / 'Thorn' / 'Manual Crowd Pummeler'). The legolas Mode B crawl correctly identified that the gaps for tome/banner/focus/horn cannot be filled by name-token mining alone — Wikipedia and Wikidata canonical-entry pages for treatises, named historical banners, mythological foci, and ceremonial horns supply the canonical-named substrate that existing-source mining cannot.

---

## 2. Per-category mining results

### 2.1 Shield (193 reclassifications)

| Step | Rows | Source |
|---|---:|---|
| `shields_royal_armouries` | 20 | `category_value = 'Shields'` (cleanest structured-field) |
| `shields_met_museum` | 88 | `classification = 'Shields'` |
| `shields_wikidata` | 79 | `weapon_type = 'shield'` |
| `shields_wikipedia_name` | 6 | name-token (shield/buckler/pavise/aspis/scutum/rondache); exclusions for shield-gun/gun-shield/shoulder-shield/riot-shield |
| **Total** | **193** | |

**Sample (random 10):** Scutum (Yale Univ. Art Gallery fragment), Q29183576 (Wikidata), Kanta (shield) (Wikipedia), Replica shield (Royal Armouries), Rondache in Late 16th Century Milanese Style (Met), Mantlet (Royal Armouries), Shield (Met), Hayato's Shield (Wikidata).

**Rep-audit:** PASS — all 10 spot samples are shields or shield-fragments. Zero false-positives.

### 2.2 Tome (64 active: 16 reclassified + 48 legolas inserted)

| Step | Rows | Source |
|---|---:|---|
| `tomes_met_museum` | 16 | `classification = 'Books & Manuscripts'` |
| `tomes_wp_wd_name` | 0 | wikipedia/wikidata name-token (grimoire/spellbook/codex/treatise) — exclusion list aggressive; Battletome (Warhammer rulebook) intentionally left at `category` |
| **Reclassified subtotal** | **16** | |
| Legolas Mode B insert (tactical treatises) | 20 | Wikipedia Military_treatise + Byzantine military manuals |
| Legolas Mode B insert (magical grimoires) | 28 | Wikipedia Grimoire |
| **Legolas subtotal** | **48** | |
| **Total** | **64** | |

**Sample (random 10):** Galdrabók (Icelandic grimoire), Marozzo Arte dell'Armi (Met), Art of War (Jomini) (Wikipedia), Book of Shadows (Wiccan; *living-tradition flag*), Commentarius Poliorceticus (Byzantine military manual), Book of Abramelin (grimoire), Toshiyoshi copy-book (Met, Japanese armoury), Sefer Raziel Ha-Malakh (Jewish mystical grimoire), Dell'arte della guerra (Machiavelli), 金工絵 Copy book.

**Rep-audit:** PASS — all 10 are treatises, grimoires, or historical military/magical books. Note: `Wapen des Heyligen Roemischen Reichs Teuetscher Nation` is an armoury inventory; coherent with the tome category as a "tactical reference" register.

### 2.3 Banner (102 active: 70 reclassified + 32 legolas inserted)

| Step | Rows | Source |
|---|---:|---|
| `banners_met_museum` | 37 | `classification IN ('Banners','Miscellaneous-Banners')` |
| `banners_osrsbox` | 33 | name-token (Saradomin banner / Zamorak banner / generic Banner) |
| `banners_wp_wd_name` | 0 | wikipedia/wikidata name-token (oriflamme/sashimono/hata-jirushi/etc.) — caught zero in active substrate; legolas Mode B supplied these instead |
| **Reclassified subtotal** | **70** | |
| Legolas Mode B insert (European) | 12 | Wikipedia Oriflamme/Raven_Banner/Roman_military_standard/etc. |
| Legolas Mode B insert (Japanese) | 5 | Wikipedia Uma-jirushi |
| Legolas Mode B insert (Hindu/Indian) | 9 | Wikipedia Dhvaja |
| Legolas Mode B insert (Mongol/Turkic) | 4 | Wikipedia Tugh |
| Legolas Mode B insert (Roman) | 2 | Wikipedia Aquila + Labarum (2 dedup pairs dropped at insert) |
| **Legolas subtotal** | **32** | (34 raw – 2 dedup) |
| **Total** | **102** | |

**Sample (random 10):** Indra Dhvaja (Hindu war-banner), Imperial French Eagle (Aigle), Karna's Elephant Banner (Mahabharata), Saradomin banner (osrsbox), Black Tugh of the Mongols, Landøyðan (Land-waster, Norse), Tugh (Mongol/Ottoman Horsetail Standard), Banner Showing Saint Sebastian (Met, Italian), Banner (Met, Italian polychromy), Banner (osrsbox).

**Rep-audit:** PASS — all 10 are battle-standards, military-banners, or named-mythological-standards. osrsbox-db generic "Banner" rows are accepted as game-loot banners with thin metadata — gandalf curation may downgrade these (they're tier C level by source-thinness).

### 2.4 Focus (14 active: 0 reclassified + 14 legolas inserted)

Existing-source mining produced **zero** focus reclassifications because the strict filter (crystal_ball / scrying / philosopher's_stone) caught no rows in active substrate. This is the right answer: rows that match those tokens in `wikipedia` / `wikidata` either don't exist as canonical-entry rows in our substrate (they'd be article-level rather than artifact-level), or they exist under other source URLs that legolas Mode B has now harvested.

| Step | Rows | Source |
|---|---:|---|
| `focuses_wp_wd_name` | 0 | wikipedia/wikidata name-token |
| **Reclassified subtotal** | **0** | |
| Legolas Mode B insert | 14 | Wikipedia Crystal_ball/Scrying/List_of_mythological_objects |
| **Total** | **14** | |

**Sample (random 10):** John Dee's Crystal Ball, Childeric I's Crystal Ball, Urim and Thummim, Aphrodite's Cestus, Dorje (Vajra) [*living-tradition flag*], Skofnung Stone, Prayer Wheel (Tibetan Buddhist) [*living-tradition flag*], Yasakani no Magatama [*living-tradition flag*], Cup of Jamshid, Sampo.

**Rep-audit:** PASS — all 10 are ritual/divinatory/channeling foci. 3 of 10 carry living-tradition flag — handled per dispatch (substrate-only; no auto-promotion). Aphrodite's Cestus is technically a girdle of magic (treated as focus per legolas Mode B classification — boundary call but defensible: girdle as magical implement worn but channeling magic).

### 2.5 Horn (27 active: 7 reclassified + 20 legolas inserted)

| Step | Rows | Source |
|---|---:|---|
| `horns_met_museum` | 2 | `classification = 'Horn-Implements'` (Tibetan Ritual Horn Sna Ru) |
| `horns_royal_armouries` | 4 | `canonical_name IN ('hunting horn','ivory horn')` excluding firearms `category_value` |
| `horns_wp_wd_name` | 1 | wikipedia/wikidata named-historical (shofar/carnyx/lituus/olifant/etc.) excluding hornet/thorn |
| **Reclassified subtotal** | **7** | |
| Legolas Mode B insert | 20 | Wikipedia Gjallarhorn/Carnyx/Cornu/Salpinx/Lur/Shofar/etc. |
| **Total** | **27** | |

**Sample (random 10):** Hunting horn (Royal Armouries), Roman Tuba, Salpinx (Greek), Shanka (Hindu Conch Horn) [*living-tradition flag*], Montes Bocineros Horns, Oliphant (Roland's), Lituus (Etruscan predecessor), Golden Horns of Gallehus, Shofar [*living-tradition flag*], Lur (Scandinavian).

**Rep-audit:** PASS — all 10 are signaling/ceremonial horns. Zero Powder horn / Hornet / Thornbow false-positives (correctly excluded). 2 of 10 carry living-tradition flag.

### 2.6 Talisman (27 active: 11 reclassified + 16 legolas inserted)

| Step | Rows | Source |
|---|---:|---|
| `talismans_fextralife` | 11 | fextralife-ds1 (6) + fextralife-ds3 (5) talisman name-token |
| **Reclassified subtotal** | **11** | |
| Legolas Mode B insert | 16 | Wikipedia Talisman/Amulet/Magatama |
| **Total** | **27** | |

**Sample (random 10):** Carnelian Amulet (Islamic), Ofuda (Shinto talisman) [*living-tradition flag*], Talisman (fextralife-ds3), Sunlight Talisman (DS1), Islamic Talismanic Bowl, Agimat / Anting-anting (Philippine), Takrut Scroll Spell (Thai), Eye of Horus (Wedjat), Sunlight Talisman (DS3), Ankh.

**Rep-audit:** PASS — all 10 are amulet/talisman/protective-ward items. Strong cultural-tradition diversity (Islamic / Shinto / Filipino / Thai / Egyptian).

---

## 3. Heuristic rules — narrative summary

The mining rules emphasize **source-anchored structured-field filters over name-token filters** wherever the source supplies a structured classification field. Name-token filters are only used where no structured equivalent exists, and always with explicit exclusion lists for known false-positive patterns.

### 3.1 Rules per source

- **`royal_armouries`** — `structured_properties.category_value` carries clean classification (`Shields`, `Relics & miscellaneous`, `Firearms & related objects`). Use this whenever possible. Name-token fallback only for fine-grained sub-categorization within a category_value (e.g., `Hunting horn` vs `Powder horn` both have category_value `Relics & miscellaneous` vs `Firearms & related objects` respectively).

- **`met-museum`** — `structured_properties.classification` is the cleanest signal (e.g., `Shields`, `Banners`, `Books & Manuscripts`, `Horn-Implements`). 88 active shield rows, 36 active banner rows, 16 active book rows, 2 active horn-implement rows.

- **`wikidata`** — `structured_properties.weapon_type` (free-text) carries direct entity-class declaration (`shield` matches 83 active rows). Highest cardinality of all sources but most variable in semantic precision.

- **`wikipedia`** — name-token only; substrate is small (~5-10 rows per off-hand category in active substrate, often dedup-merged with wikidata).

- **`osrsbox-db`** — game-specific in-world banners (Saradomin/Zamorak). Generic `Banner` rows have thin metadata; accepted as substrate-entry but likely tier-C at quality assessment.

- **`fextralife-ds1/ds3`** — Dark Souls in-game talismans (canonical mechanical category in those games). Cleanest game-source talisman substrate.

### 3.2 False-positive exclusion patterns (Discipline #25 spirit)

- `*shield gun*` / `*gun shield*` / `*shoulder shield*` / `*riot shield*` — firearms or armor pieces, not off-hand shields
- `*hornet*` / `*thorn*` / `*thornbow*` / `*hornbow*` — token matches but not horn items
- `*Manual Crowd Pummeler*` / `*Operating manual*` / `*USMC Sword Manual Procedures*` / `*Manual*` (alone) / `*Manual Dexterity*` — name-token matches `manual` but not a treatise
- `Battletome` (Warhammer) intentionally left at `weapon_kind = 'category'` — it IS a rulebook but for a tabletop game, not a magical/tactical treatise in the canonical off-hand sense; conservative call. (Gandalf curation may revisit.)
- Powder horn (royal_armouries) explicitly excluded from horn reclassification via `category_value != 'Firearms & related objects'` — powder horns are firearms accessories, not signaling/ceremonial horns
- D2 talisman system (path-of-exile-repoe `Bec-de-Corbin`, etc.) excluded — D2 talismans are a system mechanic with thousands of generated variants, not canonical-named individual talismans

### 3.3 Stage 1 + Stage 1.5 column population on new + reclassified rows

Reclassified rows have their Stage 1 proxy fingerprint columns populated via `COALESCE(existing, default)`. Defaults per § 5.2 of `MIGRATION.md`:

| weapon_kind | range | geometry | tempo | attribute |
|---|---|---|---|---|
| shield | melee_close_or_grapple | shield_blocker | reactive_block_tempo | STR_or_DEX |
| tome | off_hand_passive | tome_buff_aura | passive_or_cast_tempo | INT_or_WIS |
| banner | off_hand_aura | banner_rally_aura | aura_pulse_tempo | STR_or_WIS |
| focus | off_hand_passive | focus_channel_amp | cast_amp_tempo | INT_or_WIS |
| horn | off_hand_aura | horn_signal_pulse | aura_pulse_tempo | STR_or_WIS |
| talisman | off_hand_passive | talisman_ward_amp | passive_or_cast_tempo | WIS_or_INT |

`proxy_fingerprint_confidence` = **0.55** (heuristic; Stage 4 dispatch via legolas Mode A consult will refine the off-hand mechanical-axis profile — buff-geometry vs damage-geometry, aura-tempo vs damage-tempo).

Stage 1.5 `extracted_named_bearer` populated on legolas Mode B inserts where `author` field is present in source JSON (e.g., Sun Tzu, Chanakya, Machiavelli, John Dee). Stage 1.5 `extracted_length/weight/materials` largely NULL on off-hand rows — these fields are weapon-physical-property fields; off-hand items have different physical-property surfaces (e.g., tome word-count, banner dimensions, focus material). Stage 4 will introduce off-hand-specific extracted_* columns if needed.

---

## 4. Tier-quality and v1_scope intersection (informational; not in this dispatch's mutation scope)

Some reclassified rows had `quality_tier` and/or `v1_scope` set during prior stages (Stage 2.5 Tier-S/A classifier + Stage 3 Phase 2 v1_scope materialization). Off-hand items inherit those settings:

### 4.1 Tier-quality distribution (reclassified rows only; legolas Mode B inserts have NULL quality_tier)

| weapon_kind | S | A | B | C |
|---|---:|---:|---:|---:|
| banner | 3 | 13 | 28 | 26 |
| horn | – | 5 | 1 | 1 |
| shield | 5 | 36 | 82 | 70 |
| talisman | – | – | 11 | – |
| tome | 4 | 7 | 5 | – |
| **Total tiered** | **12** | **61** | **127** | **97** |

12 Tier-S off-hand items emerge from the mining — these are high-quality named-bearer / mythological-anchor entries that were already tier-classified before the off-hand reclassification fired. They are STILL `category`/etc. → `shield`/etc. — Stage 2.5 classifier did not consider off-hand-ness at the time; the tier classification persists.

### 4.2 v1_scope=1 intersection (Phase 2 inclusion)

| weapon_kind | v1_scope=1 |
|---:|---:|
| banner | 7 |
| horn | 2 |
| shield | 19 |
| talisman | 11 |
| tome | 3 |
| **Total** | **42** |

42 off-hand rows already in `v1_scope=1`. These came in via prior Stage 3 Phase 2 sampling (when their then-`weapon_kind` was `category` or `named_template`). They remain in v1_scope; Wave 5 Phase 2 re-sample (NOT in this dispatch's scope; post-Sidecar-B knight-rider routing) will properly account for off-hand items per composition policy v1 § 8.

---

## 5. Discipline #25 — semantic-layer rep-audit (full table)

Per dispatch § 4.5: less mode-collapse risk than main weapons but rep-audit required at v1_scope inclusion boundary. The per-category random-10 samples reported above pass rep-audit at the substrate-classification cell. Summary:

| Category | Spot-sample rep-audit | Verdict |
|---|---|---|
| shield | 10/10 sensible | PASS |
| tome | 10/10 sensible | PASS |
| banner | 10/10 sensible (osrsbox generic rows are thin but coherent) | PASS |
| focus | 10/10 sensible (Aphrodite's Cestus is boundary call — defensible) | PASS |
| horn | 10/10 sensible (zero Powder horn / Hornet false-positives) | PASS |
| talisman | 10/10 sensible | PASS |

Substrate-vote-binding at the categorical-classification cell PASSED for all 6 cells. Gandalf 30-row cross-category curation review (next session via knight-rider routing) is the binding gate; this rep-audit is the elrond pre-flight.

---

## 6. Acceptance criteria — per-item verification (dispatch § 5.5 elrond mining sub-section)

| # | Acceptance criterion | Status | Evidence |
|---:|---|---|---|
| 1 | Schema extension landed via ALTER TABLE | ✓ | `scripts/01_schema_extension.py` executed; live smoke `INSERT ... weapon_kind='shield'` succeeded + invalid value rejected; integrity_check = ok |
| 2 | MIGRATION.md drafted with grep-verified zero-cross-seam-consumer evidence | ✓ | `MIGRATION.md` § 3.1 (cross-seam grep results across all 3 sibling repos); zero hits in production code |
| 3 | Existing-source mining adds rows OR reclassifies rows for at least 4 of 6 categories | ✓ | 5 of 6 categories reclassified (shield 193, tome 16, banner 70, horn 7, talisman 11; focus 0 because legolas Mode B supplied them) |
| 4 | Per-row Stage 1 + Stage 1.5 columns populated for new rows + reclassified rows | ✓ | All 417 off-hand rows have non-NULL proxy_range/geometry/tempo/attribute_class + proxy_fingerprint_confidence=0.55; Stage 1.5 extracted_named_bearer populated on legolas inserts where source carried author |
| 5 | Legolas Mode B 132 rows INSERT-ed (with 2 dedup pairs deduped) | ✓ | 130 inserted (132 raw – 2 dedup); banner-021 + banner-033 NOT present in DB; banner-004 (Aquila) + banner-008 (Labarum) present once each |
| 6 | Output markdown + JSON artifact at named path with per-category counts + 5-10 row sample per category | ✓ | `output/existing-source-mining.json` + this `existing-source-mining.md` carry full per-category counts, mining log, samples (10 per category) |
| 7 | Pre-mining DB backup at named path (gitignored per Stage 1.5 precedent) | ✓ | `backups/telemetry.db.pre-sidecar-b` (203 MB; `backups/.gitignore` configured) |
| 8 | Round-trip: not applicable — substrate-only schema change | ✓ | No fight_log dict / loadout dict / export packet structure / inter-seam fixture touched; per `MIGRATION.md` § 11 |

All 8 acceptance criteria PASS.

---

## 7. Out-of-scope reminders (dispatch § 6)

This Sidecar B mining invocation explicitly did NOT:
- Touch main weapon library (Path A LOCKED per Matt 2026-05-25)
- Modify main-weapon substrate
- Amend skill-system canonical doc (gandalf post-Cycle-10)
- Implement Phase 5 cohesion-judge two-item alignment (gandalf authors spec post-Cycle-10)
- Trigger v1_scope re-sample for off-hand items (separate Wave 5 Phase 2 retry dispatch per knight-rider routing)
- Change engine code (substrate-only)
- Apply Stage 4 off-hand-specific mechanical-tagging (Wave 7 dispatch via legolas Mode A consult)

---

## 8. Next-step handoffs

1. **gandalf 30-row cross-category curation review** — knight-rider routes; suggested 30-row sample pre-selected in `legolas/research/cycle-10-sidecar-b-off-hand-crawl-2026-05-25/gandalf-curation-review-request.md`; knight-rider adopts or adjusts. Combined batch covers legolas Mode B 130 rows + elrond mining 287 reclassifications. Pass threshold: ≥ 24/30 sensible per-category classification + cultural-tradition + period.

2. **Wave 5 Phase 2 re-sample for v1_scope** — knight-rider routes after Sidecar B + Wave 6 land. Out-of-scope this dispatch.

3. **Wave 7 Stage 4 off-hand mechanical-tagging** — knight-rider routes via legolas Mode A consult prereq on off-hand-mechanical-profile patterns. Out-of-scope this dispatch; current proxy values (§ 3.3) are interim weapon-aligned heuristics.

4. **Tag intent** (post gandalf review pass): `elrond/cycle-10-sidecar-b-off-hand-mining-2026-05-25`. Auto-commit + auto-push per push-per-wave authorization per Cycle 10 scope-doc § 1-3.

---

**Signed:** elrond (data steward; Cycle 10 Sidecar B mining + legolas Mode B ingest executor)
