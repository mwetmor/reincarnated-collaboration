# Variant-Cluster Policy Assignments — Phase A → Phase D Bridge

**Date:** 2026-05-23
**Author:** gandalf (in-flight Matt+gandalf review per cleaning-policy-design § 6.3)
**Inputs:**
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/variant-clusters.md` (legolas; 26 cluster IDs surfaced across 8 cluster groups, covering ~38 discrete variant decisions when sub-clusters are enumerated)
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/per-source-quality.md`
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/phase-A-audit/cleanliness-baseline.md`
- `canonical/story/cleaning-policy-design-2026-05-22.md` § 6 (policy framework + criteria) — Matt-locked
**Dispatch chain:** `agentic_orchestration/dispatches/2026-05-22-legolas-phase-A-substrate-audit.md` → this document → elrond Phase D execution
**Decision criteria applied:** § 6.3 (1) mechanical-signature variance, (2) cultural-narrative distinctness, (3) substrate-density consequence, (4) anchor-test
**Output consumed by:** elrond (Phase D dedup/collapse pipeline)

---

## 0. Frame

Legolas surfaced 26 cluster IDs (RA-1..5, MET-1..3, WIKI-1..4, DND-1..3, SOULS-1..3, ODIN-1..3, AOS-1..2, CS-1..3). Several IDs contain multiple discrete variant decisions (RA-4 spans Pike/Spontoon/Halberd/Partizan; WIKI-4 spans AK-47/AKM/AK-74/AK-12/AK-15/AK-103/AK-203; MET-1 spans Katana/Tachi/Wakizashi/Tantō; MET-3 spans Tsuba/Kozuka/Fuchi/Menuki). Counting at the decision-level the surface holds **38 variant-decisions across 26 cluster IDs**. I assign policy at the cluster-ID level with sub-cluster operational hints where Policy C applies.

**Empirical baselines shifting prior framework:**
- `ammo_or_consumable` boundary error is 17.5%, not 5-8%. Any cluster touching armor/cartridge/sword-furniture/scabbard space gets **Policy B + aggressive ammo_or_consumable tagging** (drains the active substrate of ammo pollution).
- Royal Armouries within-source raw duplication is 87.9% — F1 TIERED rule already locked; my § 6.4 default of Policy B for museums holds with high confidence.
- Cross-source name overlap (Katana in 10+ sources, Dagger nearly universal) is denser than projected — CS-cluster Policy C assignments need explicit per-game-vs-historical sub-policy in elrond's executor.

**One framework override:** § 6.4 says "TRPG/MMO/ARPG sources → Policy A by default." I am keeping that for `named_template` rows but **routing `category` rows in those sources to F4 cross-source merge consideration** (Policy D-or-A per F4 ≥0.85 threshold test). This is consistent with the locked F4 rule, not a framework change.

---

## 1. Per-cluster policy assignments

### Cluster Group 1 — Royal Armouries within-source dedup

| Cluster ID | Variants | Policy | Dominant § 6.3 criterion | Rationale |
|---|---|---|---|---|
| **RA-1** | Centrefire six-shot revolver × 379 | **B** | (1) mechanical-identity + (3) density-concentration | All 379 share signature (ranged/point/fast/semi-auto). Collapse to one canonical "Centrefire six-shot revolver" with specimen_count=379 and Webley/Warnant/Bayet listed in structured_properties.variants. Single highest-yield F1 move. |
| **RA-2** | "Sword" × 3,155 (mixed culture/period/type) | **C** | (1) mechanical variance + (2) cultural distinctness | Distinct mechanical signatures (English longsword ≠ tulwar ≠ katana). Elrond must group by (culture × century × broad_type) then apply per-group B (collapse near-duplicates within a group) or A (keep cross-cultural canonicals separate). See § 2 operational hints. |
| **RA-3** | Flintlock military musket × 486 | **D** | (1) mechanical-identity + (2) partial cultural-name | All flintlock smoothbore .75 — mechanically identical. But Brown Bess / Charleville / Potsdam ARE culturally named at the national-pattern level. Policy D: one canonical "Flintlock military musket" + variant-retrievable sub-entries (Brown Bess, Charleville, Potsdam) for culture-anchored seasons. |
| **RA-4** | Pike (588) / Spontoon (562) / Halberd (284) / Partizan (253) | **A at top + B within** | (1) mechanical distinctness | Pike ≠ Spontoon ≠ Halberd ≠ Partizan are four distinct geometry signatures. Each TYPE stays as its own canonical (A). Within each type, the hundreds of specimens collapse via F1 TIERED (B). Treat as 4 Policy-A canonicals each with internal Policy-B sub-merge. |
| **RA-5** | Ammunition cartridge varieties × 2,171+ | **B + ammo_or_consumable tag** | (1) no wield signature + density consequence | Pure ammo_or_consumable; should not enter category sampling. Collapse to canonical class entries ("Centrefire rifle cartridge", "Centrefire pistol cartridge", "Centrefire shotgun cartridge"). Tag drains 2K+ rows from active substrate. |

### Cluster Group 2 — Met Museum Japanese sword variants

| Cluster ID | Variants | Policy | Dominant § 6.3 criterion | Rationale |
|---|---|---|---|---|
| **MET-1** | Katana / Tachi / Wakizashi / Tantō (~80+ rows total) | **A at top + B within** | (1) mechanical distinctness + (2) cultural distinctness | Four canonically distinct objects in Japanese tradition; mechanical signatures differ (katana=arc/measured/two-hand; wakizashi=arc/measured/one-hand; tantō=point/fast/one-hand; tachi=arc/measured/two-hand-slung). KEEP-ALL at type level. Within each type, Met specimens collapse via Policy B (museum-default). |
| **MET-2** | "Blade for X" vs "Blade and Mounting for X" | **B** | (1) mechanical-identity | Same sword, mounting completeness differs. structured_properties.mounted = true/false. No semantic split warranted. |
| **MET-3** | Tsuba (650) / Kozuka (618) / Fuchi-Kashira (278) / Menuki (86) | **B + ammo_or_consumable tag** | (1) no wield signature | Sword furniture — not wieldable weapons. All ammo_or_consumable. Four sub-types stay as distinct canonical entries WITHIN the ammo_or_consumable bucket (they're meaningfully different parts) but are excluded from category sampling. Drains 1,632 rows from active substrate. |

### Cluster Group 3 — Wikidata / Wikipedia cross-source

| Cluster ID | Variants | Policy | Dominant § 6.3 criterion | Rationale |
|---|---|---|---|---|
| **WIKI-1** | Aegis (wikidata Q190662 + wikipedia article) | **D** | F4 confirmed met + (2) mythological-unique | Single mythological object described by two sources. Cosine >0.90 + corroboration; F4 threshold met. One canonical "Aegis" (weapon_kind=unique) with wikidata Q190662 as primary key and wikipedia text merged. Disambiguation: Kimber Aegis and Aegis cruiser stay as separate `category` rows (different referents). |
| **WIKI-2** | Excalibur (wikidata + wikipedia + osrsbox) | **D for wikidata+wikipedia / A for osrsbox** | F4 met for myth pair + (2) game-instance distinct | wikidata + wikipedia merge into one "Excalibur" unique. OSRS Excalibur stays as `named_template` with related_entries → mythological unique. M982 Excalibur stays as its own `category` entry. |
| **WIKI-3** | Gladius (wikipedia + D2 + PoE + WoW + RA replica/rubber) | **C** | (1) mechanical-identity across game sources + (2) historical-vs-fantasy register split | Historical Roman gladius (wikipedia + RA replica) stays as one canonical (Policy B merge of wikipedia + RA replica into "Gladius (Roman short sword)"). The three game-source entries (D2 + PoE + WoW) F4-merge into one "Gladius (fantasy ARPG one-hand sword)" canonical. Rubber Gladius stays as its own `unique` (film prop, 2000). Net: 6 rows → 3 canonicals. |
| **WIKI-4** | AK family (AK-47/AKM/AK-74/AK-74M/AK-12/AK-15/AK-103/AK-203/AK-63) | **C** | (1) caliber-driven mechanical variance + (2) generational cultural-distinctness | Caliber-bucket grouping: **AK-47+AKM → Policy B collapse** (same 7.62×39mm, AKM is production-simplification of AK-47). **AK-74+AK-74M → Policy B collapse** (5.45×39mm; M is folding-stock). **AK-12, AK-15, AK-103, AK-203 → Policy A keep-all** (each a distinct modern generation/caliber), with related_entries pointing to AK-47 progenitor. AK-63 AMM = Hungarian AKM variant → collapse into AK-47/AKM canonical. **Net: 9 ODIN rows → 6 canonicals (AK-47/AKM, AK-74/AK-74M, AK-12, AK-15, AK-103, AK-203).** |

### Cluster Group 4 — D&D / TRPG / WoW named templates

| Cluster ID | Variants | Policy | Dominant § 6.3 criterion | Rationale |
|---|---|---|---|---|
| **DND-1** | Katana / Katana of the Ronin / Magehunter Katana / etc. | **A** | (2) named-narrative distinctness | Each magical katana is a distinct narrative artifact (`named_template`). The base "Katana" is `category`. Phase D distinguishes rarity-gated named_templates from the plain category entry; no merge. |
| **DND-2** | Abyss Warden's Axeblade + Abyss Warden's Battleaxe | **B** | (1) mechanical-identity (same trick weapon, two forms) | Two source rows describe the SAME trick weapon (longsword↔battleaxe transformation). Collapse to one canonical "Abyss Warden's Trick Weapon" with structured_properties.forms = ["longsword", "battleaxe"]. |
| **DND-3** | Worn Mace / Worn Shortsword / Worn Axe (WoW starter set) | **A** | (1) mechanical distinctness | Mace/sword/axe are mechanically distinct (blunt/point-slash/slash). Each starter weapon stays as its own canonical category-representative for its weapon-type. |

### Cluster Group 5 — Soulslike

| Cluster ID | Variants | Policy | Dominant § 6.3 criterion | Rationale |
|---|---|---|---|---|
| **SOULS-1** | Dagger across ds1/ds2/ds3/ER fextralife sources | **C** | F4 borderline + (3) game-specific lore preservation | Type-shape is same across all games but per-game lore + stats are distinct. One cross-game canonical "Dagger (soulslike category)" with game-specific variants in structured_properties. F4 should NOT auto-merge here — manual review flag because the 0.85 cosine threshold may misfire and flatten per-game flavor. |
| **SOULS-2** | Great Katana (bloqhead-demigods + fextralife-ER) | **B** | F4 confirmed met | Same weapon (ER SotE Great Katana), two sources. bloqhead has structured tier/skill data; fextralife has prose. Merged entry richer than either alone. Cosine >0.90 + corroboration → confident F4 collapse. |
| **SOULS-3** | Fextralife "Greataxes" category-index pages (DS3 + ER) | **A as weapon_kind=category** | (4) anchor-test: class-index pages aren't sampling targets | Each is a class-level meta-page, valid as a class anchor. Keep separate but mark weapon_kind=category and EXCLUDE from category sampling (these are catalogue index pages, not exemplars). Useful for Pattern-6 axis discovery as class-level reference points. |

### Cluster Group 6 — ODIN modern military edge cases

| Cluster ID | Variants | Policy | Dominant § 6.3 criterion | Rationale |
|---|---|---|---|---|
| **ODIN-1** | (overlap with WIKI-4) AK-family cross-source merge | **C** | See WIKI-4 | ODIN entries + wikipedia AK-47 + cataclysm AK-47 rifle. Policy: wikidata/wikipedia/ODIN AK-47 merge via D (one canonical with source-variants). Cataclysm "AK-47 rifle" stays separate as `named_template` (civilian-legal post-apoc clone with game-specific stats). |
| **ODIN-2** | M224 LWCMS mortar (dual-mode wieldability) | **A** | (1) wieldability bifurcation | Single canonical entry with both modes captured in structured_properties.operational_modes = [{mode: "crew-served", wieldable_humanoid: "no"}, {mode: "handheld", wieldable_humanoid: "shoulder_supported"}]. Not a collapse case; it's a single multi-mode entry. |
| **ODIN-3** | Yak-130 / Yak-130M aircraft pair | **B** | (1) mechanical-identity + (3) inactive-substrate | Same aircraft platform, M=modernized stock variant. Aircraft are wieldable_humanoid=no anyway (excluded from category sampling). Collapse reduces axis-discovery noise. |

### Cluster Group 7 — Warhammer AoS

| Cluster ID | Variants | Policy | Dominant § 6.3 criterion | Rationale |
|---|---|---|---|---|
| **AOS-1** | Vicious Claws / Tearing Fangs / Zangrom-Thaz | **A** | (1) wieldable-humanoid bifurcation | Creature attack profiles (wieldable_humanoid=no) stay distinct from named humanoid weapons. No merge case. Each is its own canonical. |
| **AOS-2** | "Skull Bludgeon and Varanspire Gladius" compound profile | **B + split-on-import** | (1) mechanical distinctness | Schema edge case: one row = two weapons. **Operational hint to elrond:** split the compound row into two canonical entries (Skull Bludgeon, Varanspire Gladius) AND keep the compound as a `weapon_kind=named_template` with structured_properties.compound_of = [child_canonical_ids]. The compound is a narrative-pairing artifact distinct from the constituent weapons. |

### Cluster Group 8 — Cross-source canonicals

| Cluster ID | Variants | Policy | Dominant § 6.3 criterion | Rationale |
|---|---|---|---|---|
| **CS-1** | Katana across 10+ sources | **C** | (2) historical-vs-fantasy register split + (3) extreme density concentration | Dedicated Phase D decision pass. **Historical tier (wikipedia + wikidata-class + met-museum + RA katana specimens): merge to one canonical "Katana (historical Japanese sword)".** **Fantasy-game tier:** each game-named katana stays separate (Moonlit Katana = WoW; hardened steel katana = Cataclysm; Great Katana = ER per SOULS-2). **D&D tier:** named_template variants stay separate per DND-1. Three policy lanes converge on Katana — elrond must implement per-lane routing. |
| **CS-2** | Dagger across nearly all sources | **C** | Identical pattern to CS-1 | Same three-lane treatment. One historical "Dagger" canonical (Policy B merging wikipedia + wikidata + RA + Met-Museum dagger specimens); soulslike per SOULS-1; per-game daggers (WoW/D2/PoE) F4-merge into one "Dagger (fantasy ARPG)" canonical if F4 ≥0.85; D&D magical daggers stay as named_templates. |
| **CS-3** | Spear / Pike / Polearm family (RA + ODIN + wikipedia + D&D) | **A at type / B within** | (1) mechanical distinctness across types | Spear ≠ Pike ≠ Halberd ≠ Spontoon ≠ Partizan: four-to-five distinct canonical types (Policy A at the type level). Within each type, specimens collapse per F1 (Policy B). Cross-source merges per F4 within type bucket. |

---

## 2. Operational hints for elrond (Phase D executor)

### 2.1 Policy C executor patterns

**Pattern RA-2 — "Sword" grouping algorithm:**
1. Group 3,155 rows by `(culture_lineage_canonical × century_bucket × broad_type_inferred)`.
2. For groups with ≥3 specimens and same `(culture, century, broad_type)`: collapse via Policy B (near-duplicate merge).
3. For groups with <3 specimens or cross-cultural mismatch: keep as separate canonicals (Policy A).
4. Expected outcome: 3,155 rows → ~150-300 canonicals.

**Pattern WIKI-4 — Caliber-bucket grouping for AK family:**
- Bucket 1 (7.62×39mm): AK-47, AKM, AK-63 AMM → one canonical "AK-47/AKM (7.62mm Soviet assault rifle)"
- Bucket 2 (5.45×39mm legacy): AK-74, AK-74M → one canonical "AK-74 (5.45mm Soviet assault rifle)"
- Bucket 3 (modern variants): AK-12, AK-15, AK-103, AK-203 each as own canonical with related_entries → AK-47

**Pattern CS-1/CS-2 — Three-lane routing for ultra-high cross-source canonicals:**
- Lane 1 (historical): museum + encyclopedia → one canonical via Policy B/D merge
- Lane 2 (per-game category items): F4 cross-source merge candidate (≥0.85 cosine + corroboration)
- Lane 3 (named_template magical/specific): stay separate per Policy A

### 2.2 Ammo_or_consumable drain (Phase D priority 1)

The following cluster decisions collectively drain the largest pollution from active substrate:
- **RA-5** (ammunition cartridges): ~2,171 rows → ammo_or_consumable bucket
- **MET-3** (sword furniture): 1,632 rows → ammo_or_consumable bucket
- Plus Royal Armouries armour/equestrian/etc. surfaced in per-source-quality.md but outside this cluster surface: ~7,266 additional rows

These four cluster-IDs alone resolve approximately 10,000+ of the ~15,727 estimated ammo_or_consumable-boundary errors. **Execute these FIRST in Phase D** before any F4 cross-source merge work — they decontaminate the substrate that F4 then operates on.

### 2.3 F4 merge candidates surfaced

Cluster-IDs that map to confirmed F4 cross-source merges (cosine ≥0.85 + corroboration confirmed by legolas):
- WIKI-1 Aegis (cosine >0.90; 2-source corroboration)
- WIKI-2 Excalibur wikidata+wikipedia pair (>0.90; 2-source)
- SOULS-2 Great Katana ER pair (>0.90; 2-source)
- WIKI-3 game-source Gladius trio (D2+PoE+WoW — F4 test should confirm ≥0.85 cosine)

F4 merge candidates flagged for cautious review (may miss 0.85 threshold but human judgment says merge):
- SOULS-1 Dagger across soulslikes — DO NOT auto-merge; manual confirmation required

### 2.4 schema delta confirmation

Per § 6.6, every Policy-A canonical needs `related_entries` populated. Every Policy-B/C/D canonical needs `merged_entry_ids` + `structured_properties.variants`. Every cluster-derived canonical needs `variant_relationship` enum populated (`independent` / `sub_variant_of:<id>` / `model_line_sibling_of:<ids>`). My assignment table above gives elrond enough information to populate all three fields per cluster.

---

## 3. Cross-cluster meta-patterns

These patterns hold across the assignment surface and inform elrond's executor design:

1. **All museum-holding clusters with mechanical-identity sub-variants got Policy B.** RA-1, RA-3 (fuzzy variant of B), RA-5, MET-2, MET-3. The § 6.4 museum-default holds with high confidence.
2. **All cross-game named_template clusters got Policy A** (DND-1, DND-3, AOS-1). Per-game narrative artifacts are first-class canonicals.
3. **All clusters with mechanical-distinctness across the cluster surface got Policy A at type-level** (RA-4, MET-1, DND-3, CS-3, AOS-1). KEEP-ALL is the right default when geometry/range/tempo differ.
4. **F4 cross-source merges concentrate in the mythological-unique and ER-specific spaces.** WIKI-1, WIKI-2, SOULS-2 are the cleanest auto-merge candidates; SOULS-1 and WIKI-3 game-tier require borderline judgment.
5. **Three-tier "historical / game-category / named_template" splitting is the right default for ultra-high-cross-source canonicals** (CS-1 Katana, CS-2 Dagger). This may extend to Sword, Spear, Bow, Shield — elrond should design the three-lane router to be reusable.
6. **AK-family caliber-bucket pattern generalizes to other modern weapon families.** M-16/AR-15/M-4 family, FN FAL family, G3 family, etc. will likely require the same caliber-bucketing logic if/when they surface. The caliber-as-mechanical-signature axis is load-bearing for modern firearms.

---

## 4. Flagged for Matt review

These clusters are genuinely ambiguous and warrant Matt's call before Phase D commits:

| Cluster ID | Ambiguity | My lean (non-binding) |
|---|---|---|
| **WIKI-3 (Gladius game-tier)** | F4 should merge D2+PoE+WoW Gladius into one fantasy-ARPG canonical, but each game's stats/lore are non-trivial. Risk: flattening fantasy-game flavor diversity. | Lean: F4-merge with structured_properties.per_game preserving each game's stats. Matt's call: is per-game stat richness load-bearing for the engine, or is the merged ARPG-gladius shape sufficient? |
| **SOULS-1 (Dagger across soulslikes)** | F4 cosine likely 0.80-0.85, borderline. Auto-merging flattens DS1/DS2/DS3/ER lore distinction. Not merging leaves 4 near-duplicate canonicals. | Lean: do NOT auto-merge; keep 4 game-specific canonicals with related_entries cross-linking. Soulslike fans distinguish the games' daggers; flattening loses that. |
| **AOS-2 (Skull Bludgeon and Varanspire Gladius compound)** | Schema design: do we (a) keep one row as a `named_template` with compound_of pointing to children, plus split into two child canonicals, OR (b) keep as a single compound entry without splitting? | Lean: option (a) — split into two children, retain compound as `named_template` pairing-artifact. Compound is a narrative pairing; the two weapons are individually meaningful. |
| **RA-2 grouping threshold** | I specified group-by `(culture × century × broad_type)` with ≥3 specimens triggering collapse. Threshold is a judgment call. | Lean: ≥3 specimens with all three keys matching = collapse. If <3, keep separate. Matt may want a different threshold; flagging for confirmation before elrond executes. |
| **WIKI-2 OSRS Excalibur disposition** | OSRS Excalibur is `named_template` (player-obtainable item named for the legend). My assignment keeps it separate with related_entries → mythological unique. Alternative: treat OSRS Excalibur as a sub-variant of the unique. | Lean: keep separate. The OSRS item is mechanically a game-template; the mythological Excalibur is a story-unique. Different referents. |

---

## 5. Phase D operational guidance summary

1. **Execute ammo_or_consumable drain FIRST** (RA-5, MET-3, plus per-source-quality.md armor/etc.) before any merge work. ~10K rows leave active substrate before F4 runs.
2. **Run F1 RA TIERED collapse** per cluster assignments (RA-1, RA-3, RA-4 internal, RA-5). Expected: 38,127 RA rows → ~3,500 canonicals.
3. **Execute F4 confirmed merges** (WIKI-1, WIKI-2, SOULS-2, WIKI-3 game-tier). Small count of merges; high confidence.
4. **Execute Policy-C complex routings** (RA-2, WIKI-4, SOULS-1, CS-1, CS-2, CS-3). These need the three-lane router and caliber-bucket logic. Most engineering effort lives here.
5. **Populate schema deltas** (`variant_relationship`, `related_entries`, `merged_entry_ids`, `structured_properties.variants`) per § 6.6 + § 2.4 above.
6. **Flag the 5 Matt-review items** before any irreversible collapse.

---

**Output:** `canonical/story/variant-cluster-policy-assignments-2026-05-23.md` (this document)
**Tag:** `gandalf/variant-cluster-policy-2026-05-23` (annotated)
**Signed:** gandalf
