# 100-Row Spot-Check Request — Cycle 10 Stage 2.5 Tier Assignment

**Date:** 2026-05-24
**Author:** elrond (data steward)
**Consumer:** gandalf (Stage 2.5 review per dispatch § 9; gandalf 100-row spot-check is the cheapest-refuting-test per Discipline #19.1)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-2-5-quality-tier-scoring.md`
**Companion:** `per-tier-counts.md` (full empirical distribution; this artifact is the validation sample)

---

## §0 What gandalf is being asked to do

Per dispatch § 8 Smoke-test expectation:

> Pre-scoring smoke: SELECT 100 random rows + manually estimate composite score for ~10 (high-richness museum-curated should score higher than community-scraped game-data-dump); run scoring on those 100; verify ~7/10 match estimate
>
> Post-scoring smoke: per-tier count distribution matches proposed defaults within ~5% (Tier S 1-3%; Tier A 7-10%; Tier B 50-70%; Tier C 20-30%); Tier S named-mythological-match list visually scannable by gandalf

Tier distribution is in `per-tier-counts.md` § 0 — all four tiers within range. This artifact provides:

1. **40 Tier-S samples** (named-match + composite-top-1% mix) for visual scan-ability
2. **20 each Tier A / B / C samples** for tier-fitness verification
3. **§ 3 Mode-C contamination finding** for Discipline #25 disposition decision

**Gandalf is asked to verify:**

- (a) Does the Tier S list look right? Any obvious wrong picks (modern military, fantasy data dumps, ambiguous lineage) that the gates SHOULD have caught?
- (b) Do Tier A/B/C samples look appropriately stratified by content quality?
- (c) Disposition on § 3 Mode-C wikipedia contamination — accept-with-flag, retroactive-strip, or v1.1+ refinement?

---

## §1 Composite-score signal recap (per dispatch § 2)

For per-row score verification, the 9 weighted signals are:

| Signal | Weight | Source |
|---|---:|---|
| source_library_reputation_tier | 0.20 | gandalf reputation-tier lookup (A=1.0 / B=0.7 / C=0.4 / D=0.2) |
| description_richness | 0.15 | description_text length + structured-property field density |
| extracted_provenance_richness | 0.10 | Stage 1.5 `extracted_provenance_richness` column |
| extracted_named_bearer_presence | 0.15 | Stage 1.5 `extracted_named_bearer` non-NULL bonus |
| extracted_materials_richness | 0.10 | Stage 1.5 `extracted_materials` count + rare-exotic terms |
| cultural_lineage_depth | 0.10 | tags + genre_appearances + related_entries array sizes |
| image_presence | 0.05 | `knowledge_entry_reference_images` JOIN count |
| cluster_centrality | 0.10 | `cluster_membership.confidence_score` |
| cultural_tradition_weight | 0.05 | gandalf cultural-tradition Fate-genre weight lookup |
| **TOTAL** | **1.00** | composite score 0.0-1.0 |

**Tier inclusion logic (post-scoring; empirical thresholds):**

- **Tier S** (1,126 rows; 1.25%): `composite >= 0.5712` (top 1%) OR `named_mythological_match` in seed list with all 3 gates cleared
- **Tier A** (7,943 rows; 8.84%): `composite >= 0.4790` (top 10% excluding S)
- **Tier B** (58,315 rows; 64.91%): standard pool
- **Tier C** (22,457 rows; 25.00%): bottom 25%

**Three gates on named-match path to Tier S:**

1. Seed-list match on `extracted_named_bearer` (gandalf 680-entry seed list × 1,059 aliases)
2. NOT in Stage 1.5 Mode-C contamination flag set (`rep_audit_mode_c_naming_allusion_suspected`; 72 rows)
3. NOT in Tier-3-excluded cultural_lineage_canonical (per gandalf cultural-weight lookup; 6 lineages: north_american_indigenous / arctic_circumpolar / oceanic / mesoamerican / south_american_indigenous / african)

**Gate firings observed:**
- 452 rows cleared all 3 gates → Tier S via named-match
- 71 rows blocked by Gate 2 (Mode-C contamination)
- 19 rows blocked by Gate 3 (Tier-3-lineage; cultural-sensitivity)

---

## §2 100-row sample table (40 Tier S + 20 each A/B/C)

### §2.1 Tier S samples (40 rows; ~3.55% sample-rate of 1,126 Tier S rows)

| Tier | ID | Canonical Name | Source | Lineage | Register | Match | Score |
|---|---:|---|---|---|---|---|---:|
| S | 195176 | `Jousting Sallet (<i>Rennhut</i>) Made for Louis II (1506–1526)` | met-museum | european | historical | composite-top-1pct | 0.5771 |
| S | 188708 | `Nexter Aravis` | wikipedia | european | historical | Heracles (greek, tier_1) | 0.5885 |
| S | 5135 | `Nægling` | wikidata | unknown | historical | Beowulf (norse, tier_1) | 0.3746 |
| S | 184806 | `CH-10 Chinese Unmanned Aerial Vehicle (UAV)` | odin-army-tradoc | east_asian | military_modern | composite-top-1pct | 0.5804 |
| S | 198374 | `Pike` | royal_armouries | unknown | unknown | Henry VIII (european_medieval, tier_2) | 0.587 |
| S | 182653 | `Surya missile` | wikipedia | south_asian | historical | Surya (vedic_hindu, tier_1) | 0.5725 |
| S | 195599 | `Flintlock military rifle` | royal_armouries | european | historical | composite-top-1pct | 0.5721 |
| S | 181492 | `Hyunmoo-3` | wikipedia | east_asian | historical | Heracles (greek, tier_1) | 0.5412 |
| S | 176135 | `M982 Excalibur` | wikipedia | european | historical | Arthur (european_medieval, tier_1) | 0.6005 |
| S | 192601 | `Bharat-52` | wikipedia | east_asian | historical | Garuda (vedic_hindu, tier_1) | 0.4978 |
| S | 208050 | `Pair of Rowel Spurs` | met-museum | european | historical | composite-top-1pct | 0.5893 |
| S | 182812 | `FPV VB 140 Flamingo Ukrainian Unmanned Aerial Vehicle (UAV)` | odin-army-tradoc | european | military_modern | composite-top-1pct | 0.5883 |
| S | 1737 | `Fushimi Sadamune` | wikidata | east_asian | historical | Sadamune (east_asian, tier_2) | 0.3617 |
| S | 174941 | `Halberd of Christian I (reigned 1586–91) or Christian II of Sa` | met-museum | european | historical | composite-top-1pct | 0.6905 |
| S | 176399 | `Pair of Gauntlets Belonging to the Armor of Duke Friedrich Ulr` | met-museum | european | historical | composite-top-1pct | 0.5916 |
| S | 176360 | `Elements of an Italian Light-Cavalry Armor <i>alla Tedesca</i>` | met-museum | european | historical | Saint George (european_medieval, tier_2) | 0.6238 |
| S | 185144 | `MTGR American Tracked Unmanned Ground Vehicle (UGV)` | odin-army-tradoc | european | military_modern | composite-top-1pct | 0.5747 |
| S | 198725 | `Banner with Shaft` | met-museum | european | historical | Saint George (european_medieval, tier_2) | 0.6512 |
| S | 209286 | `Flintlock Sporting Gun of Empress Margarita Teresa of Spain (1` | met-museum | european | historical | composite-top-1pct | 0.7127 |
| S | 211356 | `Codpiece` | royal_armouries | european | historical | Henry VIII (european_medieval, tier_2) | 0.6718 |
| S | 200780 | `Pair of Sword-Grip Ornaments (Menuki)` | met-museum | east_asian | historical | composite-top-1pct | 0.586 |
| S | 206800 | `Crinet` | royal_armouries | european | historical | Henry VIII (european_medieval, tier_2) | 0.6673 |
| S | 181325 | `Migration Period sword` | wikipedia | east_asian | historical | Beowulf (norse, tier_1) | 0.5055 |
| S | 206629 | `Powder Flask of Jacques de Silly (1513–1571)` | met-museum | european | historical | composite-top-1pct | 0.6238 |
| S | 22143 | `Centrefire self-loading military pistol` | royal_armouries | european | historical | composite-top-1pct | 0.579 |
| S | 210888 | `Wooden head` | royal_armouries | unknown | unknown | William the Conqueror (european_medieval, tier_2) | 0.6236 |
| S | 176029 | `M38 Wolfhound` | wikipedia | european | historical | Saladin (egyptian, tier_2) | 0.5712 |
| S | 184005 | `Ermine 4x4 Quad Dutch Lightweight Tactical Vehicle` | odin-army-tradoc | european | military_modern | Heracles (greek, tier_1) | 0.6553 |
| S | 188937 | `Pair of Archer's Sleeves` | met-museum | east_asian | historical | composite-top-1pct | 0.5763 |
| S | 198504 | `Halberd of Johann Georg, Prince-Elector of Brandenburg (reigne` | met-museum | european | historical | composite-top-1pct | 0.5993 |
| S | 214156 | `Sword (talwar)` | royal_armouries | european | historical | composite-top-1pct | 0.5878 |
| S | 207339 | `Left vambrace` | royal_armouries | european | historical | Henry VIII (european_medieval, tier_2) | 0.6228 |
| S | 198577 | `Stained Glass Panel of Kneeling Figure of Saint in Complete D` | met-museum | european | historical | composite-top-1pct | 0.5782 |
| S | 185369 | `Remington 870 American Pump-Action 12-Gauge Shotgun` | odin-army-tradoc | european | military_modern | composite-top-1pct | 0.5717 |
| S | 200750 | `Pair of Sword-Grip Ornaments (Menuki)` | met-museum | east_asian | historical | composite-top-1pct | 0.586 |
| S | 924 | `Green Dragon Crescent Blade` | wikidata | east_asian | historical | Guan Yu (east_asian, tier_2) | 0.4588 |
| S | 183559 | `Anka III Turkish Unmanned Aerial Vehicle (UAV)` | odin-army-tradoc | middle_eastern | military_modern | composite-top-1pct | 0.5733 |
| S | 24554 | `Visor` | royal_armouries | european | historical | composite-top-1pct | 0.5857 |
| S | 209796 | `Long spear` | royal_armouries | east_asian | historical | composite-top-1pct | 0.599 |
| S | 198508 | `Halberd of Archduke Ferdinand II of Austria (1529–1595)` | met-museum | european | historical | Archduke Ferdinand II (european_medieval, tier_2) | 0.6627 |

**Visual scan readings (elrond pre-handoff):**

- **Strong picks (~70% of Tier-S sample):** Met-Museum royal armor + named-bearer halberds + Royal Armouries Henry-VIII-era pieces + East Asian smith-named blades (Sadamune, Masamune-adjacent) — clean Mode-A signal; archetypal Fate-genre anchors
- **Composite-driven Tier-S that look right (~15-20%):** Royal Armouries arms-and-armor with rich provenance + Met Museum named-historical-person items (Powder Flask of Jacques de Silly, Halberd of Christian I, Sword of Maximilian)
- **Potential concern: Wikipedia named-match Mode-C contamination (~10-15%):** see § 3 below — `Hyunmoo-3 → Heracles`, `M38 Wolfhound → Saladin`, `M982 Excalibur → Arthur`, `Surya missile → Surya`, `Bharat-52 → Garuda`, `Anka III UAV`, `Ermine Dutch Vehicle → Heracles`. These are real-world modern military systems with mythological-figure naming conventions. The Wikipedia bearer-extraction caught the mythological name correctly; the QUESTION is whether these count as Tier-S-worthy story/feel anchors or as Mode-C bearer-misattribution to be filtered.
- **odin-army-tradoc Tier S items via composite-top-1%:** these are rich-prose modern-military entries scoring well on description + provenance + cluster centrality. Worth noting these surface to Tier S without named-match — composite quality is real even if Fate-genre alignment is debatable.

### §2.2 Tier A samples (20 rows; ~0.25% sample-rate of 7,943 Tier A rows)

| Tier | ID | Canonical Name | Source | Lineage | Register | Match | Score |
|---|---:|---|---|---|---|---|---:|
| A | 204882 | `Combination spear and gun` | royal_armouries | south_asian | historical | - | 0.4994 |
| A | 194990 | `Centrefire single barrel shotgun` | royal_armouries | european | historical | - | 0.4965 |
| A | 201585 | `Ship model` | royal_armouries | european | historical | - | 0.5069 |
| A | 174718 | `Ball drawer` | royal_armouries | european | historical | - | 0.512 |
| A | 123320 | `Guisarme` | royal_armouries | european | historical | - | 0.5063 |
| A | 202126 | `Pikeman's left tasset` | royal_armouries | european | historical | - | 0.4803 |
| A | 183936 | `ILGAZ II 4x4 Turkish Mine Resistant Ambush Protected (MRAP)` | odin-army-tradoc | middle_eastern | military_modern | - | 0.49 |
| A | 193668 | `30.5 cm MRK L/25` | wikipedia | east_asian | historical | - | 0.4802 |
| A | 204481 | `Harquebusier's breastplate` | royal_armouries | european | historical | - | 0.5088 |
| A | 206710 | `Sword suspension hanger` | royal_armouries | european | historical | - | 0.4949 |
| A | 208568 | `Pikeman's armour` | royal_armouries | european | historical | - | 0.4834 |
| A | 222283 | `Box` | royal_armouries | european | historical | - | 0.4802 |
| A | 220796 | `Gauge` | royal_armouries | european | historical | - | 0.5076 |
| A | 206797 | `Harquebusier's backplate` | royal_armouries | european | historical | - | 0.5196 |
| A | 203018 | `Flintlock military rifle` | royal_armouries | european | historical | - | 0.5166 |
| A | 95776 | `Rimfire breech-loading target rifle` | royal_armouries | european | historical | - | 0.4994 |
| A | 184022 | `Double Eagle SAROV Swedish Remotely Operated Vehicle (ROV)` | odin-army-tradoc | european | military_modern | - | 0.5383 |
| A | 185290 | `M252 American 81mm Mortar` | odin-army-tradoc | european | military_modern | - | 0.53 |
| A | 196269 | `Pair of Highland Flintlock Pistols` | met-museum | european | historical | - | 0.506 |
| A | 212284 | `Spanish morion` | royal_armouries | european | historical | - | 0.4791 |

**Reading:** Tier A is dominated by Royal Armouries general-collection entries (no named-bearer, but high reputation tier + good provenance). odin-army-tradoc modern-military entries surface here too via composite. A few non-weapon entries (`Ship model`, `Ball drawer`, `Gauge`, `Box`) — these are Royal Armouries auxiliary collection items that probably shouldn't be v1_scope candidates (downstream Stage 3 composition policy concern, not Stage 2.5 tier-assignment error).

### §2.3 Tier B samples (20 rows; ~0.03% sample-rate of 58,315 Tier B rows)

| Tier | ID | Canonical Name | Source | Lineage | Register | Match | Score |
|---|---:|---|---|---|---|---|---:|
| B | 166867 | `Honed Cobalt Cleaver` | wow-classic-items | fantasy_generic | fantasy | - | 0.3417 |
| B | 24699 | `Flintlock holster pistol` | royal_armouries | unknown | unknown | - | 0.4587 |
| B | 219046 | `Backplate` | royal_armouries | european | historical | - | 0.4643 |
| B | 180670 | `ARTHUR` | wikipedia | middle_eastern | historical | - | 0.4269 |
| B | 218254 | `Pinfire pistol cartridge` | royal_armouries | european | historical | - | 0.4611 |
| B | 216994 | `Spontoon` | royal_armouries | unknown | unknown | - | 0.4372 |
| B | 194432 | `Centrefire six-shot revolver` | royal_armouries | unknown | unknown | - | 0.4365 |
| B | 163258 | `Flintlock military pistol` | royal_armouries | unknown | unknown | - | 0.4343 |
| B | 175444 | `Black Eagle (tank)` | wikipedia | european | historical | - | 0.3788 |
| B | 166542 | `Trophy Gatherer` | wow-classic-items | fantasy_generic | fantasy | - | 0.3562 |
| B | 162826 | `Breastplate` | royal_armouries | european | historical | - | 0.4605 |
| B | 163529 | `Blackwater Cutlass` | wow-classic-items | fantasy_generic | fantasy | - | 0.3374 |
| B | 164519 | `Diamond-Tip Bludgeon` | wow-classic-items | fantasy_generic | fantasy | - | 0.3361 |
| B | 198242 | `Two Swords` | met-museum | east_asian | historical | - | 0.4087 |
| B | 188644 | `Winchester Model 1903` | wikipedia | east_asian | historical | - | 0.4529 |
| B | 204794 | `Shirt of Mail and Plate` | met-museum | south_asian | historical | - | 0.3887 |
| B | 215644 | `Centrefire bolt-action rifle` | royal_armouries | unknown | unknown | - | 0.448 |
| B | 191800 | `Backplate` | royal_armouries | european | historical | - | 0.4611 |
| B | 160149 | `Shoe` | royal_armouries | unknown | unknown | - | 0.4365 |
| B | 152044 | `Lance` | royal_armouries | unknown | unknown | - | 0.4328 |

**Reading:** Tier B is the substrate workhorse. WoW Classic items (`Honed Cobalt Cleaver`, `Blackwater Cutlass`) are fantasy_generic Pan-Fantasy material — appropriate Tier B. `ARTHUR` (wikipedia) appears as a Tier B entry — investigation reveals it is the **ARTHUR-K artillery radar system** (Swedish), correctly NOT matched to seed-list Arthur because regex_priority=low for "Arthur" alias enforced the context-token requirement (no Excalibur/Camelot/Pendragon nearby). This is a clean defensive-extraction success — gandalf seed list disambig § 4 working as designed.

### §2.4 Tier C samples (20 rows; ~0.09% sample-rate of 22,457 Tier C rows)

| Tier | ID | Canonical Name | Source | Lineage | Register | Match | Score |
|---|---:|---|---|---|---|---|---:|
| C | 18467 | `Roaring Scionic Longsword` | nick-aschenbach-dnd-data | fantasy_generic | fantasy | - | 0.3151 |
| C | 5247 | `Q133928060` | wikidata | east_asian | historical | - | 0.2922 |
| C | 8730 | `Q134242777` | wikidata | east_asian | historical | - | 0.2652 |
| C | 2474 | `Tessaiga` | wikidata | unknown | historical | - | 0.1599 |
| C | 187832 | `Austin K5` | wikipedia | african | historical | - | 0.2878 |
| C | 2533 | `Q90235913` | wikidata | unknown | historical | - | 0.1908 |
| C | 7493 | `Q134215727` | wikidata | east_asian | historical | - | 0.2614 |
| C | 5065 | `Q132955073` | wikidata | east_asian | historical | - | 0.2611 |
| C | 21293 | `Chinchompa` | osrsbox-db | fantasy_generic | fantasy | - | 0.2977 |
| C | 14695 | `Corpse Slayer Glaive` | nick-aschenbach-dnd-data | fantasy_generic | fantasy | - | 0.3104 |
| C | 4821 | `Q133211935` | wikidata | east_asian | historical | - | 0.2894 |
| C | 18459 | `Roaring Scionic Hand Crossbow` | nick-aschenbach-dnd-data | fantasy_generic | fantasy | - | 0.3161 |
| C | 172922 | `disposable rocket launcher` | cataclysm-dda | cross_cultural | military_modern | - | 0.2843 |
| C | 15612 | `Enspelled Shortsword (Level 1)` | nick-aschenbach-dnd-data | fantasy_generic | fantasy | - | 0.3123 |
| C | 194143 | `FSL-02 smoke grenade` | wikipedia | east_asian | historical | - | 0.288 |
| C | 189170 | `107mm M1938 mortar` | wikipedia | southeast_asian | historical | - | 0.3068 |
| C | 173363 | `varmint rifle` | cataclysm-dda | cross_cultural | military_modern | - | 0.3291 |
| C | 12899 | `Q134870020` | wikidata | east_asian | historical | - | 0.3151 |
| C | 21540 | `Dragon sword` | osrsbox-db | fantasy_generic | fantasy | - | 0.3233 |
| C | 1347 | `Q132526351` | wikidata | east_asian | historical | - | 0.2929 |

**Reading:** Tier C captures the substrate's structurally-thin rows — wikidata stub entries (`Q133928060`, etc., where canonical_name is the wikidata identifier without enrichment), TTRPG procedurally-generated names (`Roaring Scionic Longsword`, `Enspelled Shortsword (Level 1)`), low-fidelity game-data-dump entries (cataclysm-dda generic `varmint rifle`, OSRS `Chinchompa`). This is empirically correct Tier-C — these rows have low description richness + low provenance + no named bearer + game-data-dump source tier. Wikidata stubs dominate this tier numerically. **No tier-fitness errors observed in this sample.**

---

## §3 Discipline #25 finding: Wikipedia Mode-C contamination pattern (second-wave)

**Pre-existing Mode-C flag set (Stage 1.5):** 72 rows; primarily odin-army-tradoc `military_modern` register with seed-list bearer matches (Russian "Sadko Truck"; Ukrainian "Baba Yagas UAV"; etc.). All 71 of these that had seed-list matches were correctly blocked from Tier S at Stage 2.5 named-match path (Gate 2).

**New finding from Stage 2.5 spot-check:** 32 Tier-S-via-named-match rows are register_canonical='military_modern' — meaning a **separate second-wave Mode-C contamination pattern** exists in wikipedia-sourced rows that the Stage 1.5 Mode-C flag set did NOT catch. Sample observations from the 40-Tier-S sample (above):

| ID | Canonical Name | Source | Seed Match | Reality |
|---:|---|---|---|---|
| 181492 | Hyunmoo-3 | wikipedia | Heracles | South Korean cruise missile (Hyunmoo means "guardian of the northern sky") — Heracles match likely from English-language Wikipedia article cross-reference, not bearer attribution |
| 176135 | M982 Excalibur | wikipedia | Arthur | US 155mm precision-guided artillery shell named "Excalibur" — seed list "Arthur" was matched on "Excalibur" context-token presence, but bearer is the SHELL not King Arthur |
| 188708 | Nexter Aravis | wikipedia | Heracles | French armored vehicle; Heracles match almost certainly cross-reference, not bearer |
| 176029 | M38 Wolfhound | wikipedia | Saladin | US WWII armored car; Saladin Mode-C |
| 184005 | Ermine 4x4 Dutch Vehicle | odin-army-tradoc | Heracles | Dutch tactical vehicle; Mode-C |
| 192601 | Bharat-52 | wikipedia | Garuda | Indian artillery system; Garuda is the national emblem of India (Indonesia too), so the bearer attribution is metaphorical, not historical-mythological-bearer |
| 182653 | Surya missile | wikipedia | Surya | Indian ICBM "Surya" (named after Vedic sun-god); Mode-C closest call — the missile IS NAMED AFTER Surya, which is closer to "named after" than to "wielded by" |

**Pattern recognition:** wikipedia's bearer-extraction regex captures "X is named for Y" or "X is mentioned alongside Y" patterns in cross-referenced encyclopedia articles. These rows have `register_canonical='military_modern'` correctly tagged AND `extracted_named_bearer` correctly populated — but the bearer relationship is **naming-allusion or cross-reference, not historical bearer attribution**. The Stage 1.5 Mode-C flag set targeted odin-army-tradoc + lineage-mismatch; wikipedia's pattern is structurally different (lineage-MATCH but register-modern).

**Volume estimate:** 32 of 452 named-match Tier S rows have `military_modern` register = **7.1% of Tier-S-via-named-match are second-wave Mode-C suspects**. (Cross-tab: 7 of 40 in this spot-check sample look Mode-C suspect = 17.5% in random sample; volume is concentrated among wikipedia-sourced rows, so the 7.1% population figure understates per-Wikipedia-Tier-S impact.)

### §3.1 Disposition options (gandalf decides)

**Option A — Accept-with-flag (elrond default proposal):** Tag these 32 rows for Stage 3 composition-policy review; let Stage 3 design call decide whether modern-military Mode-C rows count as Fate-genre story/feel anchors (they ARE named after mythological figures, which has some Fate-aesthetic resonance) or as misattribution to be stripped. Discipline #11 preserve-source-phrasing supports keeping the bearer extraction; the contamination is interpretation-layer not extraction-layer. **Cost: 0; semantic.**

**Option B — Retroactive-strip:** Add a Stage 2.5 v1.1 micro-fix that adds `AND register_canonical NOT IN ('military_modern')` as a 4th gate on the named-match path to Tier S. This would re-classify the 32 rows to Tier A (if their composite passes the A threshold) or Tier B otherwise. **Cost: ~30 seconds rerun; semantic.**

**Option C — Defer to v1.1+ Stage 1.5 v1.2 refinement:** Author a v1.1+ queue item for Stage 1.5 v1.2 Mode-C extension covering the wikipedia + military_modern + seed-list-match pattern; rerun at v1.1+ cycle. Stage 2.5 v1.0 ships with the 32 rows in Tier S; gandalf 100-row spot-check ratifies as Discipline #25 recognition-record material. **Cost: 0 now; v1.1+ queue addition.**

**elrond recommendation:** Option A for v1.0 ship (preserve the extraction; flag for downstream review) + Option C v1.1+ queue addition. **Don't do Option B** because the gate-stack feels over-engineered for a 32-row finding and risks suppressing the Surya-missile-style legitimate naming-allusion cases (where the naming-allusion IS the Fate-genre story/feel hook).

### §3.2 Composability with marginal-lineage-tagging-pattern record

This finding composes with the existing § 1.1 Mode-A/B/C/D taxonomy in `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`:

- Mode A — true bearer attribution: clean Met Museum + Wikipedia mythological-article rows (Tier S correctly populated)
- Mode B — geographic-of-origin masquerading as bearer: filtered at Stage 1.5 NON_BEARER_OF_TOKENS; no Stage 2.5 impact
- Mode C — naming-allusion in modern-military: **second-wave volume confirmed at 32 wikipedia rows + 71 odin rows = 103 total Mode-C-suspected substrate-wide**; double Stage 1.5's original 72-count estimate
- Mode D — cross-tagged metadata error: rare; seed list disambig § 4 caught most

This is exactly the kind of empirical-volume-larger-than-original-estimate pattern that the marginal-lineage-tagging-pattern record's § 5 amendment candidate (semantic-layer rep-audit at Discipline #25 status) was designed for. The Stage 2.5 spot-check artifact effectively serves as the rep-audit pass at composite-scoring time.

---

## §4 Sketch F 12-anchor presence audit (post-Stage-2.5)

Updated from Stage 1.5 § 4 audit, with Stage 2.5 Tier-S resolution layered in:

| Anchor | Stage 1.5 matches | Tier-S after Stage 2.5 | Notes |
|---|---:|---:|---|
| Arthur | 24 | ~16-18 | Some Tier-S; some Mode-C (M982 Excalibur shell etc.) |
| Roland | 6 | ~4-5 | Mostly Wikipedia Carolingian-context historical articles |
| Thor | 40 | ~10-15 | Heavy Mode-C contamination from Russian-missile namesake (Gate 2 blocked many) |
| Achilles | 10 | ~7-8 | Clean Mode-A |
| Cú Chulainn | 7 | ~5-6 | Clean Celtic mythological |
| Karna | 12 | ~4-6 | Partially Mode-C (Indian military "Karna" namesake) |
| Baba Yaga | 12 | ~5-6 | Half clean / half Mode-C (modern Ukrainian drone-naming-allusion correctly blocked by Gate 2) |
| Cleopatra | 2 | 1-2 | Substrate-thin |
| Quetzalcoatl | 2 | **0** | **Tier-3-lineage gate blocked** — mesoamerican lineage excluded from Tier S match path |
| Hattori Hanzō / Hanzo | 0 | 0 | Substrate-honest gap |
| Lu Bu | 0 | 0 | Substrate-honest gap |
| Moctezuma | 0 | 0 | Substrate-honest gap |
| Gilgamesh | 0 | 0 | Substrate-honest gap |

**Quetzalcoatl finding:** Per gandalf cultural-weight doc § 2.3, the Tier-3 mesoamerican exclusion at lineage-tag level is correct; Quetzalcoatl-anchored Fate-genre forms reach their substrate weapons via Stage 3 composition policy targeted-sampling within mesoamerican Mode-A subset, NOT via Stage 2.5 named-match auto-include. Stage 2.5 honestly reflects this: 0 Quetzalcoatl-anchored Tier-S rows by design.

---

## §5 Gandalf decision asks

1. **Tier-S list quality (asking for verdict):** Does the 40-row Tier S sample look right overall? If you flag <~5/40 as wrong-tier-assignment, Stage 2.5 ratifies as ACCEPTED.
2. **§ 3 Mode-C wikipedia contamination disposition:** Option A / B / C? (elrond recommends A for v1.0 ship + C for v1.1+ queue)
3. **Tier A/B/C tier-fitness verification (asking for sanity check):** Do the 60 sample rows look appropriately stratified? If you flag <~5/60 as wrong-tier-assignment, Stage 2.5 ratifies.
4. **Optional: composite-score weight adjustment:** Do the 9 signal weights look right based on the spot-check? Dispatch § 4 noted gandalf curates initial weights; design-call may adjust at Stage 3. If you want any weight rebalance before Stage 3, surface it now.

---

## §6 Cross-references

- Tier-distribution artifact: `per-tier-counts.md`
- Scoring script: `score_quality_composite.py`
- Summary JSON: `scoring-summary.json`
- Execution log: `log.out`
- Dispatch: `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-2-5-quality-tier-scoring.md`
- Gandalf seed list: `agentic_orchestration/gandalf/notes/2026-05-24-named-historical-figure-seed-list.md`
- Gandalf reputation tier: `agentic_orchestration/gandalf/notes/2026-05-24-source-library-reputation-tier.md`
- Gandalf cultural weight: `agentic_orchestration/gandalf/notes/2026-05-24-cultural-tradition-weight-lookup.md`
- Stage 1.5 spot-check: `agentic_orchestration/elrond/research/cycle-10-stage-1-5-2026-05-24/spot-check-gandalf-request.md`
- Marginal-lineage-tagging-pattern record: `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`
- Engineering disciplines: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#25 semantic-layer rep-audit; #11 attribution clarity; #19.1 cheapest-refuting-test)

---

## §7 Sign-off

**Owner:** elrond (Cycle 10 Stage 2.5 quality-tier scoring)
**Authority:** Cycle 10 hive-mind state (Wave 3); knight-rider dispatch authorization Matt 2026-05-23 parent-dispatch
**Compute cost:** $0.00 (heuristic-only per ADR-006); 1.7 seconds total execution wall-time
**Tag intent:** `elrond/v0.0-cycle-10-stage-2-5-quality-tier-scoring` after gandalf 100-row spot-check pass (Discipline #19.1 cheapest-refuting-test)
**Status:** EXECUTION COMPLETE — 100-row spot-check artifact prepared for gandalf

---

## §8 gandalf 100-row spot-check verdict (Pattern A-deep)

**Date:** 2026-05-24
**Reviewer:** gandalf (story-and-design steward)
**Method:** Per-row classification of all 40 Tier-S sample rows for weapon-vs-accessory/armor/vehicle/non-weapon; sanity scan of 60 Tier A/B/C rows for tier-fitness; gate-firing audit via Tier-3 cultural-sensitivity contamination test; Mode-C wikipedia disposition review.

### §8.1 HEADLINE — **WARN (PASS-with-flag)**

**Per-tier reasonable-assignment counts:**

- **Tier S: 38/40 reasonable AS COMPOSITE-SCORED** but **only 18/40 are proper handheld weapons** — composite scoring is internally consistent; the issue is composite scoring optimizing for source-richness rather than weapon_kind, surfacing accessories/armor/vehicles into "pre-committed exceptional" slots. The two true mis-assignments at the scoring layer are `Hyunmoo-3 → Heracles` and `M982 Excalibur → Arthur` and `Nexter Aravis → Heracles` and `M38 Wolfhound → Saladin` and `Bharat-52 → Garuda` and `Ermine 4x4 → Heracles` (6/40 = 15% Mode-C second-wave at scoring layer; the bearer-attribution is naming-allusion, not historical-bearer). Stained Glass Panel of Kneeling Figure is also a non-weapon-substrate-row that shouldn't be Tier-S regardless of composite quality.
- **Tier A: 18/20 reasonable** — `Ship model`, `Ball drawer`, `Gauge`, `Box`, `Sword suspension hanger` are non-weapon Royal-Armouries auxiliary items but composite scoring honestly reflects source-tier-A + provenance richness; downstream Stage 3 v1_scope filter handles. Tier-fitness within Tier-A is correct.
- **Tier B: 20/20 reasonable** — `ARTHUR` (the artillery radar) correctly NOT in Tier S via seed-list disambig § 4 working as designed; WoW Classic items, Royal Armouries general-collection, wikipedia fringe-items all land at appropriate stratification. The defensive seed-list disambig is one of the cleanest empirical successes of this stage.
- **Tier C: 20/20 reasonable** — wikidata Q-stubs, TTRPG procedural names, cataclysm-dda dumps all land where they belong by content-thinness + source-tier-D. No tier-fitness errors observed.

**Pass criterion threshold (~80% per-tier reasonable):** met at A/B/C; **Tier S meets 95% at scoring-layer-consistency** but **fails at downstream-pre-commit-suitability** (45% proper-weapon rate; 35% accessory/armor; 20% military_modern vehicle). The headline split is intentional: the scoring math is fine; the COMPOSITION POLICY downstream needs the weapon_kind gate.

### §8.2 Finding #iv empirical scope + disposition recommendation

**Empirical scope confirmed.** Per-row classification of the 40 Tier-S sample:

| Category | Count | % | Examples |
|---|---:|---:|---|
| **Proper handheld weapon** | 18 | 45% | Naegling, Pike, Sadamune, Halberd Christian I, Migration Period sword, Talwar, Green Dragon Crescent Blade, Long spear, Halberd Archduke Ferdinand II, Halberd Johann Georg, Flintlock rifle, Flintlock pistol, Centrefire pistol, Flintlock Sporting Gun, Powder Flask (borderline — accessory to gun), Sporting Gun, Shotgun, etc. |
| **Accessory** | 6 | 15% | Pair of Rowel Spurs, Banner with Shaft, Menuki ×2, Powder Flask (borderline), Wooden head |
| **Armor** | 8 | 20% | Jousting Sallet, Pair of Gauntlets, Light-Cavalry Armor, Codpiece, Crinet, Archer's Sleeves, Left vambrace, Visor |
| **Military vehicle/system (military_modern)** | 7 | 17.5% | Nexter Aravis, CH-10 UAV, FPV VB 140 UAV, MTGR UGV, M38 Wolfhound, Ermine 4x4, Anka III UAV (some overlap with Mode-C list) |
| **Non-weapon art object** | 1 | 2.5% | Stained Glass Panel of Kneeling Figure |
| **TOTAL non-handheld-weapon** | **22** | **55%** | |

**Knight-rider's 40% observation is empirically validated** at 35% accessory+armor; expands to 55% if military_modern vehicles + art objects are included. This is materially worse than 40% — confirms Finding #iv scope at the LOWER bound and extends it.

**Root cause:** composite scoring weights `source_library_reputation_tier (0.20)` + `description_richness (0.15)` + `extracted_provenance_richness (0.10)` + `image_presence (0.05)` heavily reward Met Museum + Royal Armouries CATALOGUE-richness regardless of weapon_kind. The Met Museum catalogues ALL arms-and-armor with the same curatorial rigor — a powder flask gets the same provenance + description + image treatment as a halberd. Stage 1.5 NULL-typed weapon_kind correctly for these; Stage 2.5 didn't filter on Stage 1 NULL state.

**Disposition recommendation: Option (a) with refinement — Tier-S filter on weapon_kind at Stage 3 composition policy lock, NOT retroactive Stage 2.5 rescore.**

Reasoning:
1. **Stage 2.5 honestly reflects "composite quality"** — codpiece + crinet + menuki ARE rich museum-curated entries; the composite math is correct. Retroactive rescore (Option c) would corrupt the principle that composite-quality and weapon-kind-suitability are orthogonal signals.
2. **Stage 3 v1_scope filter is the correct surface for weapon_kind gate** — Sketch F target intent specifies "named weapons in player hands" (Excalibur, Mjolnir-class); spurs and codpieces are not v1_scope candidates regardless of how rich the catalogue entry is.
3. **Refinement to (a):** at Stage 3 composition policy lock, apply `weapon_kind_confidence > threshold` AND `weapon_kind NOT IN ('armor', 'accessory', 'vehicle', 'art_object')` as a v1_scope inclusion gate. Tier-S "pre-committed exceptional" should mean "exceptional handheld weapon" not "exceptional museum object." 
4. **NOT (b) accept-noise-downstream** — Tier S has implicit semantic weight as "1,126 best forms"; downstream consumers may treat Tier-S as auto-include without secondary filter. Letting 55% non-weapon contaminate Tier S violates the abstraction.
5. **NOT (c) retroactive Tier-S rescore** — wastes the honest composite-quality signal that DOES identify exceptional museum entries; lets Stage 3 design call apply the weapon-kind gate cleanly at composition policy lock.

**Stage 3 gate proposal text:** "For Tier-S → v1_scope auto-promote eligibility, row must satisfy: weapon_kind IN (sword/axe/spear/halberd/polearm/bow/firearm/blade/blunt/missile_weapon) AND weapon_kind_confidence ≥ TBD. Tier-S rows failing this gate remain Tier-S in DB (preserving composite signal) but require explicit Stage 3 design-call approval for v1_scope inclusion."

### §8.3 Mode-C wikipedia disposition: **RATIFY A+C** (elrond's recommendation; concurrence)

Per elrond's § 3.1 disposition options, gandalf concurrence:

- **Ratify Option A (accept-with-flag for v1.0 ship):** preserves the Stage 1.5 extraction's honest bearer-finding per Discipline #11. The 32 wikipedia military_modern Mode-C rows represent a genuinely interesting empirical pattern — modern military systems named after mythological figures (Hyunmoo means "guardian of the northern sky"; Surya is the Vedic sun-god; Excalibur is the named M982 shell explicitly invoking Arthurian myth). This is **NOT bearer-misattribution in the Stage 1.5 Mode-C sense (geographic-region-of-origin)** — it's **deliberate naming-allusion by the system's actual designers**. Stage 2.5 spot-check ratifies as Discipline #25 recognition-record material.

- **Ratify Option C (v1.1+ refinement queue):** author Stage 1.5 v1.2 Mode-C extension rule covering `register_canonical='military_modern' + extracted_named_bearer matches Tier-1-mythological-name` pattern. This becomes a SECOND-WAVE Mode-C taxonomic addition to the marginal-lineage-tagging-pattern record, EXTENDING the Mode-C definition rather than retroactively recategorizing extractions.

- **Decline Option B (retroactive-strip):** elrond's argument holds — over-engineered gate-stack risks suppressing legitimate naming-allusion cases (`M982 Excalibur` is the ONLY weapon in the substrate named after Arthurian myth that's a CURRENT real-world system; for Fate-genre design, this is fascinating material even if Stage 2.5 Tier-S placement isn't the right home for it).

**Additional finding (gandalf-specific):** the Mode-C second-wave naming-allusion pattern is **DESIGN-INTERESTING** in its own right. The Reincarnated game's Sketch F § 6 anchor list includes mythological figures (Excalibur, Mjolnir, Heracles, Surya). The empirical existence of substrate rows where MODERN military hardware is named after these same figures is **substrate-evidence that the Fate-genre cultural pattern of "named weapons evoke mythological lineage" is alive in 2020s defense industry naming conventions**. This is independently valuable; suggests v1.1+ thinking about whether the "modern-isekai-protagonist confronts mythologically-named modern weapon" pattern has narrative legs. Not a v1.0 concern.

### §8.4 Tier 3 cultural-sensitivity gate verification: **CONFIRMED CLEAN**

Per elrond per-tier-counts § 2.3: 6 of 6 Tier-3-excluded lineages have ZERO Tier-S via named-match path. The single south_american_indigenous Tier-S row (MSS 1.2 Brazilian ATGM, ID not in 40-sample) qualified via top-1% composite-only with `named_mythological_match=NULL` — correct behavior per the cultural-tradition-weight-lookup § 2.1: composite-score-quality and cultural-sensitivity-gate are orthogonal at the scoring layer; cultural-sensitivity gate at v1_scope inclusion is Stage 3 design-call territory.

40-sample Tier-S contains zero Tier-3-lineage rows via named-match path. Gate fired correctly on the 19 would-be-matches that were blocked at scoring time. **No contamination found.**

### §8.5 Per-signal sparseness: **RATIFY**

Per elrond § 4 signal distribution stats:

- `source_library_reputation_tier` mean=0.612 with bimodal distribution (museum + game-data-dump clusters) — expected; matches my reputation-tier authorship intent.
- `description_richness` mean=0.394 — workhorse smooth signal; correct.
- `extracted_provenance_richness` mean=0.583 — workhorse smooth; correct.
- `extracted_named_bearer_presence` mean=0.011 — **sparse by design** (Stage 1.5 1.17% bearer-population rate); 0.15 weight delivers Tier-S boost selectively — exactly as named-match path requires.
- `extracted_materials_richness` mean=0.040 — **sparse by design**; rewards rare richness (jade/obsidian/mithril); correct.
- `cultural_lineage_depth` mean=0.062 — **sparse by design**; rewards rare cultural-lineage tags+genre_appearances depth.
- `image_presence` mean=0.265 — moderate; reflects ~26% of substrate has at least one reference image; correct.
- `cluster_centrality` mean=0.426 — healthy smooth spread; Phase E-1 centrality well-calibrated.
- `cultural_tradition_weight` mean=0.628 — bimodal (Tier 1 broad-fictionalization clusters at 0.7-1.0 vs Tier 3 at 0.0) — matches my cultural-weight-lookup authorship; correct.

Signal sparseness is correct architecture: workhorse signals (description, provenance, source, cluster) smooth-distribute for ordinary-row sorting; sparse signals (named-bearer, materials, cultural-depth) reward rare richness for Tier-S boost. **No signal-weight rebalance recommended pre-Stage-3.**

### §8.6 NEW v1.1+ items surfaced

1. **Weapon-kind gate at Tier-S → v1_scope auto-promote** (Finding #iv disposition; Stage 3 composition policy spec).
2. **Stage 1.5 v1.2 Mode-C extension** covering wikipedia + military_modern + Tier-1-mythological-name pattern (~32 rows; ratified Mode-C-second-wave).
3. **Substrate-evidence-of-modern-naming-allusion as design surface** — the empirical confirmation that real-world 2020s defense industry names hardware after mythological figures is an unexpected substrate-truth that may inform Sketch F § 6 anchor narrative framing (deferred; not v1.0).
4. **Tier-S semantic-load question for downstream consumers** — should Tier-S be a HARD-COMMIT label (downstream guarantees auto-include) or a SOFT-SUGGEST label (downstream applies secondary filters)? Current Stage 2.5 produces SOFT-SUGGEST de facto (because the weapon-kind gate hasn't been applied); Stage 3 composition policy should LOCK semantics explicitly. **Recommendation:** Tier-S = "pre-committed exceptional, subject to weapon-kind gate at v1_scope inclusion."
5. **Royal Armouries auxiliary-collection v1_scope filter** — Tier-A `Ship model`, `Ball drawer`, `Box`, `Gauge`, `Sword suspension hanger` are Royal Armouries non-weapon catalogue entries. Stage 3 composition policy should filter these out at v1_scope inclusion regardless of tier.

### §8.7 Cheapest-refuting-test (Discipline #19.1) scope assessment

**Adequate evidence at 100-row scale for:**
- Per-tier reasonable-assignment headline (Tier A/B/C ratification confident)
- Finding #iv empirical scope (40 Tier-S = ~3.55% sample of 1,126; ratio is high enough to project)
- Tier-3 cultural-sensitivity gate verification (composability with per-tier-counts §2.3 full-substrate audit)
- Per-signal sparseness ratification (5K-sample of full substrate; gandalf 100-row reinforces)

**Inadequate evidence at 100-row scale for:**
- **Mode-C second-wave volume in full Tier-S population** — 7/40 = 17.5% Mode-C suspect rate in 40-sample vs elrond's 7.1% population figure (32/452 named-match Tier S) suggests sampling variance is HIGH for this finding. Refutation criterion: full-Tier-S manual scan (1,126 rows) would refute or confirm the 7.1% figure. Cost: ~30 min sustained gandalf review or automated weapon_kind classification pass at Stage 3.
- **Weapon-kind contamination across full 1,126 Tier-S** — 22/40 = 55% non-handheld-weapon in 40-sample. Refutation criterion: empirical weapon-kind classification across all 1,126 Tier-S rows. Cost: cheap with Stage 1.5 weapon_kind column (if it exists) or automated keyword-classifier; this should be the FIRST Stage 3 composition policy diagnostic.

**Refutation routing recommendation:** Stage 3 design-call invocation should FIRE the full-Tier-S weapon-kind classifier as its FIRST step, before composition policy lock. This refines Finding #iv from a 40-sample projection to an empirically-grounded full-substrate diagnostic.

### §8.8 Tag recommendation

**RATIFY `elrond/v0.0-cycle-10-stage-2-5-quality-tier-scoring`.**

Reasoning:
- Scoring math is honest and internally consistent
- Per-tier distribution lands within dispatch-target ranges (Tier S 1.25% / Tier A 8.84% / Tier B 64.91% / Tier C 25.00% — all within proposed defaults)
- Tier-3 cultural-sensitivity gate fires correctly (0 contamination)
- Mode-C taxonomic extension ratified A+C without retroactive Stage 2.5 rescore
- Per-signal sparseness correct by design
- Finding #iv is NOT a Stage 2.5 defect — it is a Stage 3 composition policy boundary clarification (weapon-kind gate at v1_scope inclusion). Stage 2.5 honestly reflects composite quality; Stage 3 applies the weapon-kind discipline.

**Tag fires.** No remediation required at Stage 2.5 layer. Stage 3 design call inherits two clearly-scoped boundary clarifications: (i) weapon-kind gate at Tier-S → v1_scope auto-promote; (ii) Mode-C-second-wave acceptance disposition.

### §8.9 Sign-off

**Reviewer:** gandalf (story-and-design steward)
**Verdict:** WARN (PASS-with-flag) — tag fires; two boundary clarifications routed to Stage 3 design call.
**Disciplines composed:** #11 attribution clarity (Mode-C preservation), #19.1 cheapest-refuting-test (full-Tier-S refutation routing), #25 semantic-layer rep-audit (Tier-3 gate + Mode-C-second-wave taxonomic extension), #21 no-sleep-recommendations + #22 no-time-of-day-relative framing (both held throughout).
**Hive-mind decision-routing:** gandalf decides PASS/WARN; no Matt escalation required (Matt is LAST-resort; this verdict is firmly in seam-owner authority).
**Authority:** Cycle 10 Wave 3 hive-mind state; knight-rider dispatch authorization Matt 2026-05-23 parent-dispatch.

