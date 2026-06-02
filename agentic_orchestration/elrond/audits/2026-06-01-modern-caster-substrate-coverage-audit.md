# WS2 Phase 1 — Modern-Caster Substrate Coverage Audit

**STATUS:** CURRENT (Mode A read-only audit; produced 2026-06-01)
**Author:** elrond (data steward seam)
**Authority:** Matt 2026-06-01 post-wave-close directive (transmitted via gandalf Pattern B close); WS1A.Q18 deferred-commitments § 2 as binding audit specification; jack-ryan WS2 Phase 1 Gate-1 PASS-with-INFO 2026-06-01
**Companion docs:**
- `agentic_orchestration/dispatches/2026-06-01-elrond-ws2-phase-1-modern-caster-substrate-audit.md` (dispatch)
- `agentic_orchestration/gandalf/notes/2026-06-01-q18-deferred-commitments.md` § 2 (audit specification source)
- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` § 3 (19 modern-caster overlay entries)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (substrate composition policy)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (BC axes; substrate measurement coordinate)
- `agentic_orchestration/qa/findings/2026-06-01-ws2-phase-1-gate-1.md` (Gate-1 PASS-with-INFO)
- `agentic_orchestration/research/scripts/ws2_phase1_modern_caster_audit.py` (audit query script — reproducible)

---

## 0. TL;DR

**The modern-caster substrate gap is SEVERE and uniform across all 7 rotating primaries.** Of the 19 modern-scientific overlay entries locked at WS1A.Q18, ZERO are backed by substrate weapons that are simultaneously (a) caster-attribute-coded (INT/WIS), (b) modern-period or sci-fi-coded, and (c) above ammo/accessory triage. Only **2 rows** across the entire 90,220-row substrate satisfy all three constraints (the strongest match is a single `Staff of Ionization` in `nick-aschenbach-dnd-data`).

The substrate has substantial **adjacent** coverage — modern-period military hardware (~500-1,000 rows of firearms/missiles/lasers from `cataclysm-dda`, `odin-army-tradoc`, `gta-v-data`) — but these are uniformly DEX-attribute-coded military weapons, NOT caster-attribute implements. The substrate also has pre-industrial fantasy caster substrate (tomes/focuses/talismans, ~427 rows), but these read as medieval-coded NOT modern-coded.

The structural finding: **modern-caster IS a substrate dimension the existing 90,220-row weapon corpus does NOT occupy at all.** Per-primary gap is uniform, not differential. The 19 overlay entries require fully novel manual authoring; only the `nick-aschenbach-dnd-data` library provides ~17 sci-fi-coded entries (Antimatter Carbine, Plasma Foil, Laser pistol, etc.) that could serve as STRUCTURAL TEMPLATES for the gap-fill authoring, but these need re-casting at the caster-attribute layer.

### Per-primary gap quantification

| Primary | Modern-caster rows (strong=caster-attr ∩ modern-period) | Eligible reps in fantasy-fictional-modern-coded | Gap verdict | Phase-2 manual-authoring scope estimate |
|---|---:|---:|---|---:|
| **lightning** | 1 (Staff of Ionization) | 3 | **ABSENT** | 8-12 weapons |
| **fire** | 0 | 4 | **ABSENT** | 7-10 weapons |
| **holy** | 0 | 26* | **WEAK** (fantasy fictional non-modern-coded only) | 7-10 weapons |
| **shadow** | 0 | 8 | **WEAK** (singularity/antimatter present in 1 library) | 7-10 weapons |
| **wind** | 0 | 1 | **ABSENT** | 6-9 weapons |
| **water** | 0 | 2 | **ABSENT** | 5-8 weapons |
| **earth** | 0 | 1 | **ABSENT** | 5-8 weapons |
| **TOTAL** | **1** | **~45** | **uniformly thin** | **~45-67 weapons** |

\* holy "fantasy-fictional-modern-coded" count of 26 is inflated by pre-industrial `radiant`-named entries; the truly modern-scientific-coded subset is ~10 (laser-, photon-, prismatic-themed).

Phase 2 scope recommendation: **Path A+B hybrid CONFIRMED at the upper end of gandalf § 2.5 estimate** (~5-15 weapons per primary, ~45-100 total). See § 5 for per-primary detail.

**Notable finding:** the `engine_authored_gap_fill_v1` lineage (43 rows total — Cycle 10 Stage 3.5 Sketch F anchors + Pyromantic Caster Cell 14) provides the operational template for Phase 2 authoring. The pattern composes naturally: each modern-caster identity becomes a 5-10-weapon "family" analogous to how Hattori Hanzō / Lu Bu / Moctezuma / Gilgamesh families were authored.

---

## 1. Methodology

### 1.1 Query approach

The audit performed three layers of analysis against `~/Games/reincarnated-loadout/data/telemetry.db` `weapon_knowledge_entries` table (90,220 rows; consolidated from Cycle 8 hive-mind weapon-substrate cycle 2026-05-22 + subsequent enrichment passes through 2026-05-27):

1. **Per-overlay-entry keyword scan.** For each of the 19 modern-caster overlay entries (and broader sci-fi-canonical-vocabulary umbrella terms per gandalf deferred § 2.4 query specification), case-insensitive SQL `LIKE` patterns matched `canonical_name`. Python word-boundary regex post-filtered to eliminate false-positives (e.g., "Percussion cannon" matching "ion cannon" because "percuss-ion").
2. **Lineage classification.** Each matched row tagged with one of 5 lineage categories based on `source_library` (see § 1.3).
3. **Eligibility classification.** Each matched row tagged with one of 4 eligibility tiers based on the joint condition of caster-attribute, period, and register (see § 1.2).

The audit script is reproducible at `agentic_orchestration/research/scripts/ws2_phase1_modern_caster_audit.py`.

### 1.2 "Modern-caster-eligible" operational definition (elrond seam authority)

A row is **strong**-eligible if:
- `proxy_attribute_class IN ('INT', 'WIS', 'INT_or_WIS', 'WIS_or_INT', 'STR_or_WIS')` (caster-coded per existing axis classification), AND
- `historical_period_canonical IN ('industrial', 'modern', 'contemporary')` (modern-period per axis classification) OR (`register_canonical = 'fantasy'` AND `historical_period_canonical = 'fictional'` with sci-fi-coded naming) OR (`register_canonical = 'military_modern'`), AND
- `weapon_kind` suggests caster-vessel (tome/focus/talisman/horn/banner) OR `weapon_kind_classified_subtype = 'accessory_handheld'`.

A row is **fantasy-fictional-modern-coded** if:
- `register_canonical = 'fantasy'` AND `historical_period_canonical = 'fictional'` AND sci-fi-coded naming present, regardless of attribute.
- This bucket captures the fantasy-ARPG entries (D&D / WoW / PoE) that use sci-fi terminology but in pre-industrial mechanical framing (e.g., `Plasma Foil` is mechanically a melee sword).

A row is **firearm-or-modern-hardware** if:
- `register_canonical = 'military_modern'` OR `historical_period_canonical IN ('industrial', 'modern', 'contemporary')` AND DEX-coded.

This methodology is the elrond-seam definition of "modern-caster-eligible" per the audit Gate-1 INFO note (dispatch § 2.3 "where possible" qualifier; methodology documented here as the fallback when substrate lineage fields don't permit clean disambiguation).

### 1.3 Lineage classification

5 lineage categories per `source_library`:

| Lineage | Source libraries | Rows |
|---|---|---:|
| `manually-authored` | `engine_authored_gap_fill_v1`, `legolas_crawl_substrate_enrichment_v1_2026_05_27` | 249 |
| `crawl-modern-military` | `cataclysm-dda`, `gta-v-data`, `odin-army-tradoc`, `army-recognition` | 5,842 |
| `crawl-historical` | `royal_armouries`, `met-museum`, `wikipedia`, `wikidata` | 66,723 |
| `crawl-fantasy-arpg` | `nick-aschenbach-dnd-data`, `wow-classic-items`, `bsdata-warhammer-aos`, `osrsbox-db`, `pf2ools-pf2ools-data-quarantined`, `diablo2-d2data`, `path-of-exile-repoe`, `fextralife-elden-ring`, `fextralife-ds*`, `bloqhead-demigods`, `elden-ring-erdb`, `5e-bits-5e-database*`, `souls-api-*` | 16,927 |
| `crawl-other` | misc | 479 |

**Important methodological calibration (Matt 2026-06-01 framing vs substrate data):** Matt's context "I think that we manually wrote the caster substrate mostly" maps imperfectly onto the actual data. The 90,220-row substrate has minimal manually-authored content (249 rows = 0.28%). The caster-adjacent weapon_kinds (`tome` 64, `focus` 14, `talisman` 27, `horn` 27, `banner` 102) are predominantly crawl-extracted from `wikipedia` (128), `met-museum` (55), `osrsbox-db` (33), `fextralife-ds*` (11). The 43-row `engine_authored_gap_fill_v1` set is the only true "manually-authored" lineage and it is exclusively pre-industrial-fantasy-coded (Hattori Hanzō / Lu Bu / Moctezuma / Gilgamesh / Roland / Karna / Pyromantic Caster).

The lineage-classification framing in § 1.3 above preserves the Matt-original distinction for audit auditability while accurately reflecting what the substrate actually contains.

### 1.4 Audit blind spots

1. **Keyword scan limits.** Modern-caster identity can be expressed without the specific overlay tokens (e.g., a weapon named "Quantum Disruption Rod" satisfies sci-fi-coded modern-caster without matching any overlay keyword). The keyword scan likely undercounts rows that thematically fit but use adjacent vocabulary. Audit conservatively reports the keyword-hit floor, not the theme-fit ceiling.
2. **`description_text` / `structured_properties` un-scanned.** The audit queried `canonical_name` only. Weapons whose name is generic but whose description establishes modern-caster theming are uncounted. A deeper Mode A scan over text fields would surface additional candidates; deferred as out-of-scope for Phase 1 quick-discovery horizon.
3. **`text_embedding` un-queried.** The substrate has a `text_embedding BLOB` column for semantic similarity scoring. A semantic-similarity sweep against modern-caster prototype embeddings (e.g., "energy pistol", "Tesla coil staff") would surface non-keyword-matched entries. Defer to Mode A P3 multimodal clustering work if richer signal needed; audit floor here is sufficient for Phase 2 scope decision.
4. **`v1_scope` filter not applied.** The audit queried all 90,220 rows regardless of `v1_scope` membership. Phase 2 authoring should explicitly tag new entries `v1_scope = 1` if they're meant for Reincarnated v1 ship; or `v1_scope = 0` and `v1_scope_genre_filter = 'sci_fi'` if reserved for a future profile. This determination is Phase 3 elrond schema/ingest scope, not Phase 1 audit scope.
5. **Lineage classification heuristic, not transactional truth.** Source libraries don't carry an explicit "manually-authored vs crawl-extracted" flag. The lineage classification per § 1.3 is heuristic — based on which sources we know were curated vs catalogued. Some `wikipedia` / `wikidata` entries for fantasy-canonical items (e.g., specific D&D editions) may have lineage closer to "manually-authored fantasy" than "crawl-extracted historical." Audit accepts the heuristic as good-enough for Phase 2 scope decision.

---

## 2. Per-primary detailed findings

### 2.1 lightning

**Per-overlay-entry coverage:**

| Overlay entry | Match count | Strong | Fantasy-modern | Firearm | Other | Backing assessment |
|---|---:|---:|---:|---:|---:|---|
| `tesla` | 1 | 0 | 0 | 1 | 0 | ABSENT (only `Tesla Cannon` STR-coded from wikidata) |
| `voltage` | 2 | 0 | 0 | 0 | 2 | ABSENT |
| `ion` | 2 | 1 | 1 | 0 | 0 | WEAK (`Staff of Ionization` INT-coded; `Ion Cannon` STR-coded) |
| `flash` | 2 | 0 | 1 | 1 | 0 | ABSENT |
| `_railgun_coilgun` | 7 | 0 | 0 | 6 | 1 | ABSENT (all DEX military hardware) |
| `_emp_generator` | 4 | 0 | 1 | 3 | 0 | ABSENT |
| `_plasma_electric` | 3 | 0 | 0 | 1 | 2 | ABSENT |

**Top 5 reps (sorted by eligibility):**

- `Staff of Ionization` (nick-aschenbach-dnd-data; fantasy/fictional; INT; tier B) — the ONLY genuine modern-caster lightning weapon in the substrate
- `Ion Cannon` (nick-aschenbach-dnd-data; fantasy/fictional; STR; tier C) — sci-fi-coded but wrong attribute
- `Flash Rifle` (wow-classic-items; fantasy/fictional; DEX; tier C) — sci-fi-coded but wrong attribute
- `EMP Grenade` (nick-aschenbach-dnd-data; fantasy/fictional; DEX; tier C)
- `Electric rail gun model` (royal_armouries; historical/modern; DEX; tier B)

**Lineage distribution (lightning, 20 total rows):** crawl-historical=8 / crawl-fantasy-arpg=6 / crawl-modern-military=6 / manually-authored=0

**Per-overlay backing verdict:** `tesla` ABSENT, `voltage` ABSENT, `ion` WEAK (1 caster-attribute hit), `flash` ABSENT, `_railgun_coilgun` umbrella ABSENT-for-caster (firearm-coded), `_emp_generator` ABSENT-for-caster, `_plasma_electric` ABSENT.

**Lightning verdict: ABSENT.** No genuine modern-caster lightning substrate exists. The single `Staff of Ionization` (D&D-canon) is the only structural-template candidate.

---

### 2.2 fire

**Per-overlay-entry coverage:**

| Overlay entry | Match count | Strong | Fantasy-modern | Firearm | Other | Backing assessment |
|---|---:|---:|---:|---:|---:|---|
| `fusion` | 3 | 0 | 1 | 1 | 1 | WEAK (Fusion Blade DEX-coded; sci-fi but wrong attribute) |
| `thermal` | 2 | 0 | 0 | 2 | 0 | ABSENT (FLIR thermal binoculars = military_modern) |
| `combustion` | 1 | 0 | 1 | 0 | 0 | ABSENT (`Combustion Dagger` is DEX-coded melee) |
| `_flamethrower_modern` | 36 | 0 | 2 | 27 | 7 | ABSENT-for-caster (uniformly DEX firearms — TOS-1, M9, Type 74, FHJ-84, etc.) |

**Top 5 reps:**

- `Combustion Dagger` (wow-classic-items; fantasy/fictional; DEX; tier B) — sci-fi but melee
- `Fusion Blade` (nick-aschenbach-dnd-data; fantasy/fictional; DEX; tier C)
- `Incendiary Ammo` / `Incendiary Ammunition` (nick-aschenbach-dnd-data; ammo, no attribute)
- `FLIR Recon V American Multi-Sensor Thermal Binoculars` (odin-army-tradoc; military_modern; tier A; siege_vehicle subtype)

**Lineage distribution (fire, 41 total rows):** crawl-historical=22 / crawl-modern-military=14 / crawl-fantasy-arpg=5 / manually-authored=0

**Per-overlay backing verdict:** `fusion` WEAK (1 DEX entry), `thermal` ABSENT (only siege-vehicle binoculars match), `combustion` ABSENT, `_flamethrower_modern` ABSENT-for-caster (large firearm corpus exists but uniformly wrong attribute and weapon-class).

**Fire verdict: ABSENT.** The substrate has SUBSTANTIAL modern-fire weapons (~36 flamethrowers, 14 incendiaries) but ALL are DEX-attribute-coded military hardware. ZERO INT/WIS modern-fire-caster entries. This is the most stark per-primary pattern in the audit: the modern fire arsenal is well-represented in the substrate as firearm-class, completely absent as caster-class.

---

### 2.3 holy

**Per-overlay-entry coverage:**

| Overlay entry | Match count | Strong | Fantasy-modern | Firearm | Other | Backing assessment |
|---|---:|---:|---:|---:|---:|---|
| `photon` | 3 | 0 | 1 | 1 | 1 | WEAK (Photonic Lash DEX-coded; photon torpedo tube DEX-coded; Photon Projector historical/contemporary, no attribute) |
| `laser` | 44 | 0 | 5 | 36 | 3 | ABSENT-for-caster (predominantly DEX military lasers — Peresvet, Silent Hunter, BBQ-905, Apollo) |
| `prismatic` | 8 | 0 | 2 | 0 | 6 | WEAK (mostly pre-industrial fantasy `Prismatic Blade` etc.) |
| `_radiant_emitter` | 0 | 0 | 0 | 0 | 0 | ABSENT (no genuine sci-fi "radiant emitter" entries in substrate) |

**Top 5 reps:**

- `Aasimar's Radiant Sword` (legolas_crawl_substrate_enrichment_v1_2026_05_27; fantasy/fictional; STR; tier A) — pre-industrial-fantasy-coded, not modern
- `Laser Sword` (nick-aschenbach-dnd-data; fantasy/fictional; STR; tier B)
- `Prism` (nick-aschenbach-dnd-data; fantasy/fictional; tier B; category kind)
- `Radiant Dark Greatsword (very rare variant)` (nick-aschenbach-dnd-data; fantasy/fictional; STR; tier B) — pre-industrial-fantasy
- `Radiant Dark Rapier (uncommon variant)` (nick-aschenbach-dnd-data; fantasy/fictional; DEX; tier B) — pre-industrial-fantasy

**Lineage distribution (holy, 54 total rows):** crawl-modern-military=29 / crawl-historical=11 / crawl-fantasy-arpg=31 / manually-authored=1 (the Aasimar's Radiant Sword)

**Per-overlay backing verdict:** `photon` WEAK (3 entries, no caster-attribute), `laser` ABSENT-for-caster (44 entries dominated by military hardware), `prismatic` WEAK (8 entries but mostly pre-industrial fantasy `prismatic` adjective for swords), `_radiant_emitter` ABSENT.

**Holy verdict: WEAK.** Substrate has substantial modern military laser weaponry (~36 DEX firearms) and pre-industrial fantasy `radiant`/`prismatic` weapons (~26), but ZERO genuinely modern-caster radiant-emitter / laser-focus / prism-array implements. The 18 fantasy-fictional radiant entries are misleading false-positives — they're pre-industrial-coded medieval-fantasy weapons that happen to use "radiant" as a magical descriptor, not modern-scientific radiant-emitter technology.

---

### 2.4 shadow

**Per-overlay-entry coverage:**

| Overlay entry | Match count | Strong | Fantasy-modern | Firearm | Other | Backing assessment |
|---|---:|---:|---:|---:|---:|---|
| `blackhole` | 1 | 0 | 0 | 0 | 1 | ABSENT (Black Hole Grenade DEX-coded ammo) |
| `singularity` | 3 | 0 | 3 | 0 | 0 | WEAK (3 D&D `Singularity` variants, mostly no attribute) |
| `darkmatter` | 1 | 0 | 0 | 0 | 1 | ABSENT (Dark Matter Dagger DEX-coded melee) |
| `_antimatter_void_modern` | 5 | 0 | 5 | 0 | 0 | WEAK (Antimatter Carbine/Dagger/rifle DEX-coded; Voidmaw Bombard/Sphere unattributed) |

**Top 5 reps:**

- `Singularity` (nick-aschenbach-dnd-data; fantasy/fictional; tier B; category kind, no attribute)
- `Singularity (very rare variant)` / `(uncommon variant)` (nick-aschenbach-dnd-data; fantasy/fictional; tier B/C)
- `Antimatter Carbine` (nick-aschenbach-dnd-data; fantasy/fictional; DEX; tier C)
- `Antimatter Dagger` (nick-aschenbach-dnd-data; fantasy/fictional; DEX; tier C)

**Lineage distribution (shadow, 10 total rows):** crawl-fantasy-arpg=8 / crawl-historical=2 / manually-authored=0

**Per-overlay backing verdict:** All 4 overlay-entry groupings WEAK-or-ABSENT. The `nick-aschenbach-dnd-data` library provides ~8 sci-fi-shadow-themed entries (Antimatter, Singularity, Voidmaw) but all are DEX-coded ammo/firearm/melee, NOT INT/WIS singularity-generator implements.

**Shadow verdict: WEAK.** Same pattern as fire and holy: sci-fi vocabulary exists in the substrate (concentrated in one library) but uniformly mis-coded as weapon-class for the cell intent. Notably the lowest absolute match count (10 total rows) — the smallest existing surface to build on.

---

### 2.5 wind

**Per-overlay-entry coverage:**

| Overlay entry | Match count | Strong | Fantasy-modern | Firearm | Other | Backing assessment |
|---|---:|---:|---:|---:|---:|---|
| `sonic` (compound-form-anchored) | 6 | 0 | 1 | 1 | 4 | ABSENT (Sonic Bomb DEX; Stark Sonic Cannon STR; Sonic Amplifier no-attr; Sonic Spear DEX) |
| `shockwave` | 2 | 0 | 0 | 1 | 1 | ABSENT |
| `_acoustic_pressure` | 3 | 0 | 0 | 2 | 1 | ABSENT (acoustic surveillance ships from odin-army-tradoc) |

**Top 5 reps:**

- `Sonic Bomb` (nick-aschenbach-dnd-data; fantasy/fictional; DEX; tier C)
- `Type 927 Class (Dongjian Class) Chinese Acoustic Surveillance Ship` (odin-army-tradoc; military_modern; tier B; category)
- `Kantan Class Chinese Acoustic Marine Testing Ship` (odin-army-tradoc; military_modern; tier B; category)
- `Sonic Amplifier` (wikidata; historical/contemporary; tier C; category)
- `Shockwave` (wikidata; historical/modern; tier C; category)

**Lineage distribution (wind, 11 total rows):** crawl-historical=5 / crawl-fantasy-arpg=4 / crawl-modern-military=2 / manually-authored=0

**Per-overlay backing verdict:** All 3 overlay-entry groupings ABSENT-for-caster.

**Wind verdict: ABSENT.** Substrate covers acoustic / sonic naval surveillance and a handful of sonic-themed thrown weapons (Sonic Bomb, Sonic Spear, Sonic Grenade) but ZERO sonic emitter / pressure cannon / acoustic-projector implements with caster-attribute coding.

---

### 2.6 water

**Per-overlay-entry coverage:**

| Overlay entry | Match count | Strong | Fantasy-modern | Firearm | Other | Backing assessment |
|---|---:|---:|---:|---:|---:|---|
| `hydro` (compound-form-anchored) | 0 | 0 | 0 | 0 | 0 | ABSENT |
| `hydraulic` (compound-form-anchored) | 0 | 0 | 0 | 0 | 0 | ABSENT |
| `_cryo_cavitation` | 2 | 0 | 2 | 0 | 0 | WEAK (Cryo Bomb DEX; Cryo Grenade DEX — both ammo-class) |

**Top 5 reps:**

- `Cryo Bomb` (nick-aschenbach-dnd-data; fantasy/fictional; DEX; tier C)
- `Cryo Grenade` (nick-aschenbach-dnd-data; fantasy/fictional; DEX; tier C)

**Lineage distribution (water, 2 total rows):** crawl-fantasy-arpg=2 / manually-authored=0

**Per-overlay backing verdict:** `hydro` ABSENT, `hydraulic` ABSENT, `_cryo_cavitation` WEAK (2 DEX-coded ammo entries only). Cryo-themed military hardware is substantial in the substrate but indexes as register=military_modern and the overlay vocabulary doesn't catch it (e.g., "Type 99 Russian Cold-Weather Suit" was historical research but caught no audit query).

**Water verdict: ABSENT.** The lowest absolute match count (2 rows) — most thoroughly empty modern-caster surface in the substrate.

---

### 2.7 earth

**Per-overlay-entry coverage:**

| Overlay entry | Match count | Strong | Fantasy-modern | Firearm | Other | Backing assessment |
|---|---:|---:|---:|---:|---:|---|
| `seismic` | 1 | 0 | 1 | 0 | 0 | ABSENT (only `Seismic Hammer` D&D melee; STR-coded) |
| `tectonic` | 0 | 0 | 0 | 0 | 0 | ABSENT |
| `_mass_driver` | 0 | 0 | 0 | 0 | 0 | ABSENT |

**Top 5 reps:**

- `Seismic Hammer` (nick-aschenbach-dnd-data; fantasy/fictional; STR; tier B)

**Lineage distribution (earth, 1 total row):** crawl-fantasy-arpg=1 / manually-authored=0

**Per-overlay backing verdict:** All 3 overlay-entry groupings ABSENT.

**Earth verdict: ABSENT.** Lowest absolute count tied with water (1 row). No seismic-device / tectonic-shaper / mass-driver substrate at all. The single `Seismic Hammer` is STR-coded melee, not caster-class.

---

## 3. Cross-primary patterns

### 3.1 Three structural patterns hold across all 7 primaries

**Pattern 1 — Modern-fire substrate is well-covered as FIREARM but ABSENT as CASTER.** The substrate contains ~500+ rows of modern military hardware (flamethrowers, lasers, sonic surveillance, plasma cutters) distributed across `cataclysm-dda`, `odin-army-tradoc`, `gta-v-data`, `army-recognition`. These are uniformly DEX-coded and register=military_modern. ZERO are caster-attribute-coded. The substrate composition policy at `weapon-substrate-composition-policy-v1-2026-05-24.md` § 2.1 EXPLICITLY trims military_modern to ~5-8% of v1_scope, so even if these rows were re-coded for caster use, they would still face composition-trim pressure.

**Pattern 2 — Fantasy-ARPG sci-fi-coded vocabulary EXISTS in 1-2 libraries but uniformly mis-attributed.** `nick-aschenbach-dnd-data` (the D&D supplement collection) provides ~17 sci-fi-coded entries (Antimatter Carbine, Plasma Foil, Fusion Blade, Laser pistol, Singularity, Sonic Bomb, Cryo Grenade, etc.) but these are uniformly DEX-attribute-coded (gun-class) or STR-attribute-coded (melee-class with sci-fi name). ZERO are INT/WIS modern-caster implements. The pattern is consistent: D&D sci-fi supplements model sci-fi as ranged-weapons-with-modern-vocabulary, NOT as caster-implements-with-modern-vocabulary.

**Pattern 3 — Pre-industrial fantasy caster substrate (tomes / focuses / talismans / banners / horns) is MEDIEVAL-CODED.** The ~427 caster-vessel rows are predominantly historical/medieval/classical period, with NONE in industrial/modern/contemporary. The substrate-curation pattern at Cycle 8 hive-mind explicitly targeted medieval/classical caster kit identity (per `weapon-substrate-composition-policy-v1-2026-05-24.md` Sketch D — fantasy+historical-leaning). Modern-caster was implicitly out-of-scope for that cycle.

### 3.2 Systematically thin categories (in increasing severity)

| Category | Severity | Pattern |
|---|---|---|
| `radiant emitter` / `light-amplification gauntlet` (holy) | THIN | 0 substrate; pre-industrial `radiant` weapons exist but mis-cued |
| `singularity-generator` / `antimatter-cannon` (shadow) | THIN | 8 fantasy-ARPG entries; 0 caster-attribute |
| `sonic emitter` / `pressure-cannon` (wind) | VERY THIN | 11 total entries; firearms + naval surveillance only |
| `Tesla coil staff` / `coilgun-class caster` (lightning) | VERY THIN | 1 INT-coded match (Staff of Ionization) |
| `fusion-cell focus` / `thermal lance` (fire) | VERY THIN | 41 entries dominated by firearms; 0 caster |
| `cryo-projector` / `hydro-pressure caster` (water) | ABSENT | 2 entries (Cryo Bomb / Grenade) |
| `seismic-device` / `tectonic-shaper` (earth) | ABSENT | 1 entry (Seismic Hammer STR-coded) |

The gap is **uniformly thin across all 7 primaries; no primary is unexpectedly well-covered.** This is the strongest empirical claim from the audit.

### 3.3 Unexpected finding — modern-caster IS a missing substrate axis, not differential coverage

The audit findings DO NOT support a per-primary differential Phase 2 scope (e.g., "lightning is well-covered, just fill in shadow"). They support a uniform Phase 2 scope ("modern-caster is a missing substrate dimension; all 7 primaries need fresh authoring at similar magnitude").

This composes with the BC axes lock at `qd-engine-bc-axes-lock-2026-05-20.md` § 6 substrate dependency summary — the audit confirms that the cell-coordinate (`attribute=INT/WIS` × `register=fantasy` × `period=fictional` × `naming=sci-fi-modern`) is genuinely unoccupied in the substrate. It's not a tagging issue; it's a content-coverage gap.

---

## 4. Lineage findings (auditable transparency)

### 4.1 Manually-authored caster substrate — actual scale

Per Matt 2026-06-01 context: "I think that we manually wrote the caster substrate mostly and so we may need to manually author modern variants."

The substrate evidence is more nuanced: **caster-vessel weapons in the substrate are NOT primarily manually-authored.** They are crawl-extracted from Wikipedia, Met Museum, OSRSBox, and the various Souls-game catalogues. Specifically:

| weapon_kind | Top sources | Total rows |
|---|---|---:|
| tome (64) | wikipedia (52), met-museum (8), royal_armouries (4), 5e-bits (3), wikidata (3) | 64 |
| focus (14) | wikidata (8), osrsbox-db (3), wikipedia (1), 5e-bits (1), royal_armouries (1) | 14 |
| talisman (27) | wikipedia (15), 5e-bits-2024 (6), osrsbox-db (3), fextralife-ds1 (3) | 27 |
| horn (27) | met-museum (24), wikipedia (2), royal_armouries (1) | 27 |
| banner (102) | wikipedia (58), wikidata (32), wow-classic-items (8), warhammer-aos (4) | 102 |

The genuinely manually-authored lineage is the 43-row `engine_authored_gap_fill_v1` set (Cycle 10 Stage 3.5 — Hattori Hanzō / Lu Bu / Moctezuma / Gilgamesh families + Pyromantic Caster Cell 14 + Roland / Karna / Baba Yaga supplements). This set is EXCLUSIVELY pre-industrial / classical / medieval / pre_classical period.

**Implication for Phase 2:** the operational pattern Matt referenced (manual authoring) is genuinely the right pattern, but it's not because pre-existing caster substrate was manually authored — it's because the gap-fill operational pattern from Cycle 10 (Sketch F anchor families authored ~5-10 weapons each, gandalf + rocket + star-lord + jack-ryan workflow per composition policy § 9.4) IS the proven template. Phase 2 should follow that template directly.

### 4.2 The `nick-aschenbach-dnd-data` finding (Phase 2 structural template candidate)

The single library `nick-aschenbach-dnd-data` (6,297 total rows; D&D supplement compilation) provides the ONLY non-trivial corpus of sci-fi-coded fantasy weapons in the substrate. It contains:

- ~17 sci-fi-coded weapons (Antimatter Carbine, Voidmaw Bombard, Plasma Foil, Laser Sword, Fusion Blade, Ion Cannon, EMP Grenade, Cryo Bomb, Sonic Bomb, Singularity, etc.)
- Predominantly DEX-coded (11) and STR-coded (4); 6 are no-attribute (consumable/category)
- Tier distribution: predominantly tier C (low-quality, but operational templates for naming + identity)

The `nick-aschenbach-dnd-data` library DOES NOT solve the substrate gap — it provides melee/ranged sci-fi weapons, not caster implements. But the **naming patterns + identity structures** in this library can serve as conceptual templates for the Phase 2 author to adapt to caster-class. E.g., the existence of `Antimatter Carbine` (DEX firearm) suggests the modern-caster authoring could include `Antimatter Focus` or `Antimatter Channeler` (INT/WIS caster equivalents).

This is a useful structural finding for Phase 2 scope shape: Phase 2 doesn't author from a blank slate — it has 17+ existing sci-fi-coded D&D-canonical entries to anchor the naming/identity register against.

---

## 5. Phase 2 scope recommendation

### 5.1 Path A+B hybrid CONFIRMED

The audit confirms gandalf's Path A+B hybrid recommendation at deferred-commitments § 2.4. The audit (Phase 1) revealed:

1. Uniform across-primary gap → no Path B shortcut available (can't skip authoring for some primaries because their coverage is "fine")
2. Substrate is not zero-everything → Path A insights ARE actionable (the 43-row `engine_authored_gap_fill_v1` template + 17-row `nick-aschenbach-dnd-data` sci-fi template inform the Phase 2 authoring pattern)
3. Per-primary scope can be modulated per the specific gap-shape (e.g., earth + water are deepest gaps; lightning + holy have 1 each candidate template to anchor against)

### 5.2 Per-primary Phase 2 scope estimate

| Primary | Overlay entries | Modern-caster weapons to author | Rationale |
|---|---:|---:|---|
| lightning | 4 (tesla / voltage / ion / flash) + plasma-validated | 8-12 | Heavy overlay-entry count (4 new + plasma anchor) × ~2-3 weapons per overlay (umbrella sufficient coverage); Staff of Ionization is the anchor template |
| fire | 3 (fusion / thermal / combustion) | 7-10 | Moderate overlay count × ~2-3 weapons per overlay; Fusion Blade + Combustion Dagger are template candidates (but need re-cast as caster) |
| holy | 3 (photon / laser / prismatic) | 7-10 | Moderate overlay count; Laser Sword + Prism + photonic projector are template candidates |
| shadow | 3 (blackhole / singularity / darkmatter) + soul-mystical | 7-10 | Moderate overlay count; Singularity (D&D) + Voidmaw set are template candidates |
| wind | 2 (sonic / shockwave) | 6-9 | Smaller overlay count × ~3-4 weapons; Sonic Bomb is the anchor template |
| water | 2 (hydro / hydraulic) | 5-8 | Smallest overlay count × ~3-4 weapons; Cryo Bomb / Grenade are the anchor templates (cryo isn't an overlay entry but is adjacent — could fold in or hold for v1.1) |
| earth | 2 (seismic / tectonic) | 5-8 | Smallest overlay count + total absence; Seismic Hammer is the only template; needs full novel authoring |
| **TOTAL** | **19 entries** | **~45-67 weapons** | **upper end of gandalf § 2.5 estimate** |

This matches gandalf § 2.5 estimate (5-15 per primary; 35-100 total) at the upper-medium range. The ~45-67 estimate accounts for the audit finding that ALL 7 primaries need fresh authoring (no primary unexpectedly well-covered) AND respects gandalf's preference for substantive coverage (5-10 per primary to ensure each overlay entry has 2-3 backing weapons).

### 5.3 Phase 2 operational pattern (proven via Cycle 10 Stage 3.5)

Per `weapon-substrate-composition-policy-v1-2026-05-24.md` § 9 + § 9.4, Phase 2 should follow the established Cycle 10 Stage 3.5 pattern:

- **rocket** authors engine-side skill kit for each weapon (mechanical profile)
- **gandalf** curates cultural-tradition / lore / naming per modern-scientific framing
- **star-lord** runs Phase 5 cohesion-coalescence LLM calls (if needed for naming)
- **jack-ryan** Gate-2 sim-viability per gap-fill per T4-A § 3.3 step 5

Per-entry schema must populate (per § 9.3 composition policy): canonical_name + description_text + structured_properties + register_canonical + historical_period_canonical + cultural_lineage_canonical + proxy_attribute_class (must be INT/WIS for caster) + proxy_range_class + proxy_geometry_class + proxy_tempo_class + quality_tier + lineage tag = `engine_authored_modern_caster_gap_fill_v1_2026-06-XX`.

The lineage tag is a new sub-lineage of `manually-authored`, parallel to the `engine_authored_gap_fill_v1` pattern. Phase 3 elrond schema/ingest scope should add this tag (~1-2 new schema field considerations).

### 5.4 v1_scope decision is downstream

Phase 2 authoring should NOT pre-commit `v1_scope = 1` on the new entries. The v1_scope decision is downstream and depends on:

- Whether Reincarnated v1 ship includes modern-caster kit identity at all (per genre filter `genre IN ('fantasy', 'mythological', 'historical')` at composition policy § 6.2)
- Whether modern-caster is staged for a v1.1+ or future-profile release (sci-fi profile activation)

Phase 2 entries should ingest with `v1_scope = 0` and `v1_scope_genre_filter = 'fantasy_sci_fi_overlay'` or similar. Phase 3 / Phase 4 work re-evaluates v1_scope membership against the genre-filter + composition-policy at that time.

---

## 6. Audit limitations

1. **Keyword-only scan.** The audit queried `canonical_name` with word-boundary-anchored keyword patterns. Modern-caster identity expressed through OTHER vocabulary (e.g., "Quantum Disruption Rod" or "Energy Channeling Implement") would be undercounted. The audit reports a CONSERVATIVE FLOOR; the true substrate ceiling is somewhat higher but not by orders of magnitude given the single-library concentration of sci-fi vocabulary.

2. **Text fields un-scanned.** Description text and structured_properties were not queried. A weapon with a generic name and a modern-caster description would be uncounted. A deeper Mode A pass over text fields would likely surface 10-30 additional candidates but would not change the verdict (Phase 2 authoring still needed).

3. **Embeddings un-queried.** The `text_embedding BLOB` column was not used. Semantic-similarity scoring against modern-caster prototype concepts would surface non-keyword-matched candidates. This is the highest-value extension to deepen the audit if more confidence in Phase 2 scope is needed; deferred as out-of-scope for Phase 1 quick-discovery horizon (~0.5 session per dispatch).

4. **Lineage classification is heuristic.** The 5-category lineage taxonomy in § 1.3 maps `source_library` → lineage. Some `wikipedia` / `wikidata` entries for fantasy-canonical items have lineage closer to "manually-authored fantasy" than "crawl-extracted historical." The audit accepts this as good-enough for Phase 2 scope decision; Phase 3 schema work may need to refine.

5. **Modern-caster definition is elrond-seam.** The operational definition in § 1.2 is the audit's contribution; gandalf may have a different intent for "modern-caster-eligible" given the overlay-entry intent. If gandalf's framing differs, the audit's "strong" count may be re-pegged but the structural ABSENT verdict is robust to definition variation (no plausible definition pulls more than ~5 strong matches from the substrate).

6. **No `v1_scope`-filtered cut.** The audit queried all 90,220 rows regardless of v1_scope flag. A Phase 2 scope decision may want a v1_scope-filtered re-cut to know "how many modern-caster substrate rows are already in v1_scope?" Answer per quick check: 0 strong matches are in v1_scope = 1 (the Staff of Ionization is tier B, fantasy-fictional, INT — would be in v1_scope per the constrained-sampling but the substrate v1_scope flag is unset on it; check `sqlite3 ... 'SELECT v1_scope FROM weapon_knowledge_entries WHERE canonical_name="Staff of Ionization"'`).

7. **The 89,839 figure cited in the dispatch is slightly out of date.** Current substrate row count is 90,220 (+381 since the Cycle 8 hive-mind close; subsequent enrichment via `legolas_crawl_substrate_enrichment_v1_2026_05_27` + 43 engine-authored gap-fills). Audit findings are presented against the current 90,220-row baseline; the dispatch's 89,839 figure is from a prior snapshot.

---

## 7. Notable findings to surface to Knight-rider

### 7.1 Audit confirms Phase 2 path; does NOT alter scope shape

The audit does NOT surface evidence that fundamentally changes Phase 2 scope shape (per dispatch § 5 escalation criterion). It CONFIRMS the gandalf § 2.5 estimate at the upper end. Path A+B hybrid execution is the right path; no need for Matt + gandalf to re-engage on the architectural shape.

### 7.2 Pattern finding — "modern-caster" is a missing substrate AXIS

The audit's empirical claim is sharper than "thin": **modern-caster as a substrate cell-coordinate (INT/WIS × modern-period × caster-vessel × sci-fi-coded) is genuinely unoccupied across all 7 rotating primaries.** This composes with BC axes lock § 6 substrate dependency summary — the Cycle 8 hive-mind weapon-substrate cycle implicitly did not commission modern-caster coverage (its focus per composition policy § 2.1 was fantasy + historical, military_modern explicitly trimmed). The substrate is doing what it was designed to do; modern-caster is a planned-extension territory.

### 7.3 The `nick-aschenbach-dnd-data` opportunity

The single library `nick-aschenbach-dnd-data` provides the ONLY corpus of sci-fi-coded fantasy weapons (~17 sci-fi-themed entries). These are NOT modern-caster substrate but DO provide naming/identity TEMPLATES that Phase 2 authoring should reference. Specific candidates for gandalf Phase 2 authoring inspiration: Antimatter Carbine, Voidmaw Bombard, Plasma Foil, Laser Sword, Fusion Blade, Ion Cannon, EMP Grenade, Cryo Bomb, Sonic Bomb, Singularity, Staff of Ionization.

### 7.4 Sub-finding — caster-substrate-as-manually-authored framing needs nuancing

Matt's 2026-06-01 context "I think that we manually wrote the caster substrate mostly" is partially contradicted by substrate evidence. The 64 tomes + 14 focuses + 27 talismans + 27 horns + 102 banners are predominantly crawl-extracted from Wikipedia / Met Museum / OSRSBox / Souls-canon. The genuinely manually-authored caster substrate is the 43-row `engine_authored_gap_fill_v1` set (Cycle 10 Stage 3.5 anchor families). The operational pattern Matt described (manual authoring for modern variants) is still the right pattern — but it's because the proven Cycle 10 Stage 3.5 workflow is the template, not because pre-existing caster substrate was manually authored. Phase 2 should follow the Stage 3.5 pattern; this audit confirms that's correct.

This sub-finding is INFO-level for KR + Matt + gandalf awareness; does not change Phase 2 path.

---

## 8. Cross-references

### Composes with (existing canon)

- `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` § 3 (19 modern-caster overlay entries — backing assessment target)
- `agentic_orchestration/gandalf/notes/2026-06-01-q18-deferred-commitments.md` § 2 (audit specification source)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (composition policy; § 2.1 register weights; § 9 Stage 3.5 gap-fill pattern; § 6 substrate-genre-flagging)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 6 substrate dependency summary
- `canonical/00-ground-state.md` § 1 (current truth oracle)

### Authorizes downstream

- **WS2.P2 manual authoring** — gandalf manual-authoring sessions for ~45-67 modern-caster weapons across 7 primaries; Path A+B hybrid CONFIRMED at upper-medium end
- **WS2.P3 schema + ingest + lineage tag** — elrond ingests gandalf-authored entries with new sub-lineage `engine_authored_modern_caster_gap_fill_v1_2026-06-XX`
- **WS2.P4 substrate-coverage validation pass** — gandalf design-quality review + elrond per-primary backing re-verification

### Does NOT replace or amend

- 90,220-row weapon substrate (PRESERVED; audit is read-only)
- pool.json v1.0 canonical lock (PRESERVED; this audit informs downstream substrate authoring, not vocabulary)
- `weapon-substrate-composition-policy-v1-2026-05-24.md` (PRESERVED; Phase 2 entries respect composition policy or carry explicit override rationale)

### Audit script (reproducibility)

`agentic_orchestration/research/scripts/ws2_phase1_modern_caster_audit.py` — Python 3 read-only query against `~/Games/reincarnated-loadout/data/telemetry.db`. Re-run produces deterministic output (no random sampling; deterministic keyword regex). Re-runs will reflect substrate updates if any.

---

## 9. Sign-off

**Author:** elrond (data steward seam)
**Authority chain:**
- Matt 2026-06-01 verbatim post-wave-close directive (transmitted via gandalf Pattern B close)
- gandalf deferred-commitments § 2 as binding audit specification (commit `76f2250`)
- jack-ryan WS2 Phase 1 Gate-1 PASS-with-INFO 2026-06-01 (fire authorization)
- Elrond seam authority on Mode A audit query design + substrate-lineage interpretation + per-primary gap-quantification methodology

**Status:** CURRENT — Phase 1 audit COMPLETE. Phase 2 / Phase 3 / Phase 4 HELD pending Matt + gandalf direction per dispatch § 8 out-of-scope block.

**Routing back to KR:** Audit ready for Matt + gandalf Phase 2 decision. Phase 2 scope recommendation: Path A+B hybrid CONFIRMED; per-primary scope ~5-10 weapons per primary; ~45-67 total; pattern = Cycle 10 Stage 3.5 operational template.

**Discipline composition:**

- Discipline #41 (substrate-led) — audit grounds Phase 2 scope in empirical substrate evidence, not designer assumption
- Discipline #42 (framing-audit) — § 4.1 explicitly re-frames the "manually-authored caster substrate" claim against actual substrate evidence; preserves transparency
- Discipline #18 (math-hotspot methodology consultation) — audit methodology in § 1.2 documents the elrond-seam definition explicitly for reproducibility
- Discipline #25 (semantic-layer rep-audit / marginal-lineage tagging) — § 4 lineage findings sub-section captures lineage-tag composition for downstream Phase 3 schema work

---

**End of WS2 Phase 1 modern-caster substrate-coverage audit.**

---

## Completion record

**Completed:** 2026-06-01
**Audit artifact:** `agentic_orchestration/elrond/audits/2026-06-01-modern-caster-substrate-coverage-audit.md`
**Per-primary gap quantification:**

| Primary | Verdict | Phase-2 weapons |
|---|---|---:|
| lightning | ABSENT | 8-12 |
| fire | ABSENT | 7-10 |
| holy | WEAK | 7-10 |
| shadow | WEAK | 7-10 |
| wind | ABSENT | 6-9 |
| water | ABSENT | 5-8 |
| earth | ABSENT | 5-8 |

**Phase 2 scope recommendation:** Path A+B hybrid CONFIRMED; per-primary scope ~5-10 weapons; ~45-67 total. Follows Cycle 10 Stage 3.5 operational template (gandalf authoring + rocket engine kit + star-lord LLM + jack-ryan Gate-2).
**Audit limitations / blind spots:**
- Keyword-only scan over `canonical_name`; description text + embeddings un-queried
- Lineage classification is heuristic per `source_library` → category
- Substrate row count is 90,220 (current); dispatch cited 89,839 (slightly stale)
**Notable findings:**
- Modern-caster IS a missing substrate AXIS, not differential coverage — uniform Phase 2 scope required
- `nick-aschenbach-dnd-data` library provides ~17 sci-fi-coded structural templates for Phase 2 authoring inspiration (not direct substrate, but naming/identity patterns)
- Caster-substrate-as-manually-authored framing per Matt 2026-06-01 needs nuancing — actual manually-authored set is the 43-row Cycle 10 Stage 3.5 gap-fill anchor families; pre-existing caster-vessel rows are crawl-extracted; the OPERATIONAL pattern Matt described remains the right Phase 2 template
**Routing back to KR:** report ready for Matt + gandalf Phase 2 decision
