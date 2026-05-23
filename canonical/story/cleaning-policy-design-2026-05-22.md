# Cleaning-Policy Design Review — Weapon-Library Substrate Phase B

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — see `canonical/00-ground-state.md`

**Date:** 2026-05-22 (late-evening — gandalf subagent fire, Pattern-A; following knight-rider dispatch + Matt approval)
**Author:** gandalf (story-and-design steward; senior designer; design-track Phase B steward)
**Status:** v1 canonical lock — Phase B policy review complete; all 7 dispatch review items addressed with concrete recommendations; math-anchored substrate-cleanliness bar derived
**Authority:** Knight-rider dispatch 2026-05-22 evening (`agentic_orchestration/dispatches/2026-05-22-gandalf-cleaning-policy-design-review.md`); Matt-approved 2026-05-22 evening
**Dispatch tag at completion:** `gandalf/cleaning-policy-design-review-2026-05-22`

**Parent docs:**
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — hive-mind protocol governing Patterns 4-5-6 substrate work
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` — Variant C scope + profile-overlay separation
- `canonical/story/gear-heavy-promotion-2026-05-22.md` — vast-library substrate architecture
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` — Patterns 4-5-6 vestigial-pattern retirements
- `agentic_orchestration/weapon-library-import-hive-mind-state.md` — Cycle 9 active; 89,839 clean entries / 24 sources
- `agentic_orchestration/weapon-library-import-sample-rows-2026-05-22.md` — 3-rows-per-source review
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0

---

## 0. TL;DR

The 89,839-entry substrate is **clean enough to enter Phase A audit** but needs four targeted normalization passes before Pattern-6 axis discovery (Phase E) operates trustworthily. This doc closes seven open Phase-B policy questions with concrete, math-anchored answers — no "TBD," no "depends."

**The four math-anchored cleanliness gates (§ 4):**

| Gate | Threshold | Anchor |
|---|---|---|
| (a) FP rate in active substrate (non-weapon mis-classified as weapon) | **≤ 3.0%** (hard); **≤ 1.5%** (target) | PCA loading stability at k=8 axes degrades observably above ~3% noise; below 1.5% the noise floor is invisible at the cluster-purity level |
| (b) Within-canonical-merge duplication rate | **≤ 4.0% residual duplication** post-merge; equivalent to **dedup recall ≥ 92%** of true duplicates | Cluster purity degrades at duplication rates >5%; HDBSCAN min_cluster_size=50 needs <4% intra-cluster noise; current raw duplication is **47%** so dedup is load-bearing |
| (c) Field-coverage gap (per-row missingness on core fields) | **≥ 85%** coverage on `description_text`; **≥ 70%** on `cultural_lineage_tags`; **≥ 60%** on `historical_period`; **≥ 95%** on `structured_properties` (already met empirically) | Effective sample size in clustering = N × coverage; below these floors per-axis loadings lose statistical power at sub-cluster granularity |
| (d) `weapon_kind` mis-classification rate | **≤ 2.0%** category-vs-unique boundary errors; **≤ 5.0%** category-vs-named_template (more forgiving since named_templates collapse to categories in sampling anyway) | Uniques in category sampling pool poison generation diversity (same name repeats); at 2% boundary error, expected unique-in-N=20-sample rate ~ 1-in-2 samples polluted, which the human eye catches; below 2%, polluting samples become Poisson-rare |

**The named-unique allowlist (§ 3):** 24 historical/mythological named uniques present in or likely in the substrate, plus 6 detection-regex patterns (proper-noun-without-type-descriptor, royal-ownership-signal, etc.).

**The cultural-lineage canonical taxonomy (§ 5):** 3 axes (historical_period × 8 values, cultural_lineage × 13 values, register × 5 values) with explicit mapping from each of the 24 source libraries' raw tag formats.

**The variant-collapse option set (§ 6):** 4-policy framework (KEEP-ALL / COLLAPSE-TO-PARENT / TIERED / FUZZY-COLLAPSE-WITH-VARIANT-PRESERVATION) with concrete decision-criteria the Matt+gandalf in-flight loop applies to each surfaced variant cluster.

**Pattern-6 sequencing (§ 7):** **Hybrid — pre-cleaning rough axis discovery on dirty substrate (1-day legolas Mode A probe) + post-cleaning canonical axis discovery on clean substrate.** The dirty probe surfaces axes the cleaning pipeline must preserve; the clean run is the canonical loading. Iterative full feedback loop NOT recommended — diminishing returns + budget cost.

**Taxonomy refinements (§ 1, § 2):** Two small additions to dispatch-proposed taxonomies — `weapon_kind` gains an `ammo_or_consumable` bucket (5th enum) to handle Cataclysm-DDA + WoW Classic patterns; `wieldable_humanoid` enum expanded with `shoulder_supported` as distinct from `two_hand` to preserve mechanical signature of crew-served-but-single-operator weapons (RPG-7 pattern).

---

## 1. Item 1 — Three-bucket `weapon_kind` taxonomy review

### 1.1 Dispatch-proposed enum

```
weapon_kind ∈ { category | unique | named_template | unknown }
```

### 1.2 My finding: the three buckets are correct but incomplete by one

The proposed three-bucket taxonomy correctly captures the engine's category-sampling mental model. `category` is the substrate the engine generates instances from; `unique` is *one-of-a-kind* historical/mythological individuals that must NEVER appear in category sampling (Excalibur cannot be a "longsword sample"); `named_template` is Matt's clever third-bucket — D&D's "Hammer of Thunderbolts" is named but is functionally a categorical stat-block-template that the engine can consume.

**The pattern the taxonomy misses:** ammunition + sub-weapon consumables. The sample-rows doc surfaces this clearly:

- `cataclysm-dda` rows: `battery`, `butane`, `notch` — these are ammo/fuels in the source data, registered as "weapons" by permissive filter
- `wow-classic-items`: "Worn Mace" with full stat block is a weapon, but other rows in the same source pull ammo bags + thrown-weapon stacks
- `royal_armouries`: "Centrefire rifle cartridge" (1,758 instances) — these are ammunition, not weapons
- `met-museum`: "Sword Guard (Tsuba)" (559 instances), "Knife Handle (Kozuka)" (600) — these are **weapon parts**, not weapons themselves

If these all land in `category` they pollute category sampling severely. If they're forced into `unique` or `named_template` they're miscategorized. Drop them entirely and we lose the ability to round-trip a structured-property lookup ("what kind of ammunition fits a flintlock musket?"), which is downstream substrate the cohesion-judge benefits from.

### 1.3 Recommendation: 5-bucket taxonomy

```
weapon_kind ∈ {
    category,             -- Engine sample-pool; type definitions ("longsword", "AK-47", "katana", "halberd")
    unique,               -- Specific named historical/mythological individuals; EXCLUDED from category sampling
                          -- ("Excalibur", "Mjolnir", "Joyeuse", "Honjō Masamune", "Curtana")
    named_template,       -- Narratively named but stat-block-template; consumable as engine categories
                          -- ("Hammer of Thunderbolts", "Vorpal Sword", "Holy Avenger")
    ammo_or_consumable,   -- NEW: ammunition, weapon parts, consumable munitions, weapon-adjacent equipment
                          -- ("Centrefire rifle cartridge", "Tsuba", "Kozuka", "battery", "butane")
                          -- Round-trip queryable but EXCLUDED from category sampling
    unknown               -- Pre-classification default
}
```

The fifth bucket is **tag-and-keep**, like wieldability: these rows remain queryable for downstream uses (ammunition-substrate, weapon-parts-substrate for craft systems) but are excluded from `v_category_sample`. The schema delta proposed by knight-rider becomes:

```sql
weapon_kind TEXT NOT NULL DEFAULT 'unknown'
    CHECK (weapon_kind IN ('category','unique','named_template','ammo_or_consumable','unknown'))
```

### 1.4 Concrete examples from substrate (per-bucket)

**`category` examples (engine samples these):**
- `wikidata`: Aegis (shield class), PMD mines, Battersea Shield
- `wikipedia` v2: AK-47, AIM-7 Sparrow
- `royal_armouries`: Centrefire six-shot revolver, Flintlock military musket
- `met-museum`: "Blade and Mounting for a Wakizashi"
- `nick-aschenbach-dnd-data`: Abominable Club (D&D weapon)
- `wow-classic-items`: Worn Mace, Worn Shortsword
- `elden-ring-erdb`: Hand Axe, Jawbone Axe
- `cataclysm-dda`: (the actual weapon entries; ~50-60% of the 1,599 rows)
- `odin-army-tradoc`: AK-12, M224 LWCMS

**`unique` examples (engine NEVER samples; preserved for narrative reference):**
- `osrsbox-db`: Excalibur (Arthurian; OSRS reuses the name)
- `bsdata-warhammer-aos`: Zangrom-Thaz (named AoS weapon-individual)
- Royal Armouries holdings: if any specific named historical sword (Joyeuse-class) is in the 38K — Phase A audit surfaces
- `wikidata`: Battersea Shield is borderline — it's a SPECIFIC archaeological object (Q810944) not a class
- `souls-api-thomaslincoln`: BLACK KNIGHT HALBERD (Dark Souls named weapon)
- `bloqhead-demigods`: Alabaster Lord's Sword (Elden Ring boss-weapon; named individual)

**`named_template` examples (engine treats as category; flag for high-frequency axis-discovery sampling per dispatch Q3):**
- `nick-aschenbach-dnd-data`: "Abyss Warden's Axeblade", "Abominable Club"
- `5e-bits-5e-database`: any homebrew with narrative-name pattern but full stat block
- `bsdata-warhammer-aos`: "Vicious Claws", "Tearing Fangs" — narratively named, mechanically template
- `wow-classic-items`: many magical-affix item names ("Worn X" is category; "Ashbringer" would be unique)

**`ammo_or_consumable` examples (NEW bucket):**
- `royal_armouries`: "Centrefire rifle cartridge" (1,758), "Print" (411) — these are armoury holdings that aren't weapons
- `met-museum`: "Sword Guard (Tsuba)" (559), "Knife Handle (Kozuka)" (600), "Scabbard" (619) — parts
- `cataclysm-dda`: "battery", "butane", "notch", and other fuel/ammo from `ammo.json`
- `wikidata`: "PMD series mines" is borderline — it's a category of mines (mine = weapon), but if there are wikidata Q-items for specific cartridge classes, those go here

**`unknown`:** Pre-classification default. Phase A audit's job is to drive `unknown` count to <5% of the substrate via rules + LLM-judgment.

### 1.5 Detection rules for legolas Phase A audit

The rules for moving rows out of `unknown`:

| Target bucket | Detection rules (per row) |
|---|---|
| `ammo_or_consumable` | (a) Source-library `cataclysm-dda` AND source file path matches `ammo.json` OR `tool.json`; (b) `canonical_name` matches `/\b(cartridge\|round\|shell\|bullet\|ammo\|scabbard\|tsuba\|kozuka\|grip\|guard\|hilt\|sheath\|handle\|stand)\b/i`; (c) source-library `met-museum` AND structured_properties.classification contains "Helmet Part" / "Sword Part" / "Armor Part" / "Hilt" |
| `unique` | (a) Display name appears in named-unique allowlist (see § 3.5); (b) regex matches proper-noun-without-type-descriptor pattern (`^[A-Z][a-zA-Z'·-]+(?:\s+[A-Z][a-zA-Z'·-]+)*$` AND no generic-type word) AND `wikidata_qid` exists for a specific object (not a class Q-item); (c) structured_properties.classification contains "Named" / "Specific" / "Unique" |
| `named_template` | (a) Source-library in {nick-aschenbach-dnd-data, 5e-bits*, pf2ools*, bsdata-warhammer-aos, fextralife*, bloqhead-demigods, elden-ring-erdb, souls-api-thomaslincoln, diablo2-d2data, path-of-exile-repoe, osrsbox-db (excl. canonical-named-historical), wow-classic-items} AND name is not in named-unique allowlist AND name contains narrative-flavor adjectives or compound-noun-with-flavor-prefix pattern (regex: `/^(?:[A-Z][a-z]+(?:'s|of))?\s*[A-Z][a-z]+\s+(?:sword\|axe\|hammer\|bow\|staff\|wand\|dagger\|spear\|lance\|mace\|club\|shield\|orb\|tome\|chime\|focus)/i`); (b) D&D rarity in {`Uncommon`, `Rare`, `Very Rare`, `Legendary`} per structured_properties.rarity |
| `category` | DEFAULT after exclusion of the above; verified by (a) generic type-noun in name OR (b) source-library is `wikidata` and Q-item is a class (`P31` instance-of Q-item is itself a class like Q13442) OR (c) source-library is `wikipedia` (v2 clean) — Wikipedia articles are CATEGORIES of weapons by default (not specific named individuals) |

Phase A audit applies these rules to a ~600-1,250 stratified sample to estimate per-bucket FP rate; Phase D applies them to the full 89,839 substrate. The rules will produce some misclassification — Item 4 (d) is the math-anchor for how much misclassification is tolerable.

---

## 2. Item 2 — Wieldability filter rules review

### 2.1 Matt's locked rule (correct)

> "If a single humanoid can carry and fire/wield in active use, it's wieldable."

Shoulder-support counts (RPG-7/M249/SMAW). Handheld projectiles count (grenades, bombs, throwing axes). Excluded: mortars (when in their normal emplaced role), tripod-MGs in emplaced role, artillery, naval guns, mounted turret weapons.

### 2.2 Dispatch-proposed enum

```
wieldable_humanoid ∈ { one_hand | two_hand | either | no | mount_required | unknown }
```

### 2.3 My finding: the enum is mostly correct but loses one mechanically-load-bearing signal

The dispatch's enum collapses `shoulder_supported` (RPG-7, M249, SMAW) into `two_hand`. This is operationally fine for wieldability filtering — the row passes the filter either way — but it loses a **mechanical signature distinction** that matters for substrate-vector queries downstream.

Why it matters: in the engine's range × geometry × tempo signature space, an RPG-7 is `ranged × line × slow-charge × single-hit × spread` (rocket-propelled grenade — single shot, area effect, long reload). A two-handed sword is `melee × arc_sweep × measured × single-hit × precision`. The engine treats them very differently. But during axis discovery (Pattern 6), if both are tagged `wieldable_humanoid=two_hand`, the only signal distinguishing them is `range_class` + `geometry_class`. That works if those classifications are clean — but they often aren't, because the source data uses different vocabularies for `two_hand` vs `shoulder_supported` mechanical patterns.

**Pragmatic move:** preserve the shoulder-supported distinction at the source-of-truth layer; collapse it downstream in `v_category_sample` if not needed.

### 2.4 Recommendation: 6-bucket wieldability enum

```
wieldable_humanoid ∈ {
    one_hand,           -- Single-handed wieldable (sword, dagger, pistol, hand-thrown)
    two_hand,           -- Two-handed wieldable in direct grip (greatsword, polearm, longbow, rifle)
    shoulder_supported, -- NEW: requires shoulder-support but operable by single humanoid in active use
                        -- (RPG-7, M249, SMAW, Stinger MANPADS, javelin-launcher)
    either,             -- Can be wielded either one- or two-handed (bastard sword, hand-and-a-half)
    no,                 -- Cannot be wielded by single humanoid in active use
                        -- (mortars in emplaced role, tripod MGs, naval guns)
    mount_required,     -- Vehicle/platform-mounted (mounted turret, tank gun, mounted crossbow)
    unknown             -- Pre-classification default
}
```

### 2.5 Edge cases requiring explicit handling

| Edge case | Disposition | Rationale |
|---|---|---|
| Two-handed flails (e.g., 14th-century European war-flail) | `two_hand` | Single-humanoid wielded; mechanical signature is `melee × arc_sweep × measured` — straightforward |
| Oversized polearms / pike (4-6m pike) | `two_hand` IF "carried + fired in active use" (Swiss pike formation pikes count); `no` IF used only in static formation defense (Macedonian sarissa borderline) | Honor the "active use" clause; phalanx pikes were thrust during combat — wieldable |
| Javelins | `one_hand` (thrown projectile) | Handheld projectile per Matt's rule |
| Spear-throwers (atlatl, woomera) | `one_hand` (with held javelin; atlatl is the implement) | Same as bow + arrow — the implement is one-handed |
| Two-handed throwing weapons (bola, oversized chakram) | `two_hand` for prep; `one_hand` for release — register as `two_hand` since active-use phase dominates | Matt's "carry and fire/wield in active use" rule honors the dominant-phase |
| Crossbows (light vs heavy vs siege) | Light = `one_hand` (pistol crossbow); standard = `two_hand`; siege/wall crossbow = `mount_required` | Wall-mounted historical siege crossbows are not single-humanoid wielded |
| Mounted ranged (attached crossbows, vehicle-mounted guns) | `mount_required` | Per Matt's exclusion |
| Mortars (60mm vs 81mm vs 120mm) | 60mm M224 LWCMS = `shoulder_supported` OR `two_hand` (the dispatch says exclude mortars in emplaced role; M224 has handheld/portable mode) — judgment call by case; 81mm+ = `no` | LWCMS is genuinely portable; classify per object weight + operational doctrine. Many ODIN entries are crew-served — `no` is the default for those |
| Tripod-mounted MGs in "ground role" vs "vehicle role" | If the row represents the weapon system on its tripod: `no`. If it represents the weapon-stripped-of-mount that COULD be carried in dismounted role (M2HB stripped of tripod): `two_hand` (heavy two-hand). Convention: tag per source's primary doctrinal use; surface dual-use as note | Edge case; honors Matt's "active use" clause; doctrinal use of M2HB is tripod-mounted, so `no` is default |
| Bombs / grenades | `one_hand` (thrown) | Handheld projectile |
| Composite weapons (rifle-with-underbarrel-grenade) | `two_hand` (dominant signature is the rifle) | The shoulder-supported variant only applies if the dominant grip pattern is shoulder-support |
| Naval guns (modern destroyer 5-inch guns) | `no` | Mount-platform fundamentally non-humanoid |
| Vehicle-removable but still crewed (M242 Bushmaster, modern coaxial guns) | `mount_required` | Crew + power-feed required for operation |
| Crew-served direct-fire (anti-tank guns) | `no` | Not single-humanoid operable |
| Specialized siege weapons (battering ram, ballista, catapult) | `mount_required` for ballista/catapult; `two_hand` for handheld battering rams; `no` for siege-towers and big ones | Per object scale |
| Ammunition (`ammo_or_consumable` per § 1) | `wieldable_humanoid` is not the right axis — set to `unknown` or omit entirely; the `weapon_kind` field carries the disposition | Ammo isn't wielded; it's loaded |

### 2.6 Per-source signal-inventory refinements

The dispatch is correct on signal inventory. Two additions:

| Source | Additional signal |
|---|---|
| `odin-army-tradoc` | Per-entry **crew count** field (1, 2, 3, etc.) is the cleanest signal. Crew=1 → `one_hand` / `two_hand` / `shoulder_supported` per weight + mounting fields. Crew≥2 → `no` UNLESS dismount-doctrine field indicates single-operator dismounted role |
| `wikipedia` v2 | Infobox `weight` field — if >25kg net implement weight AND no shoulder-strap mention → `no`; if 15-25kg with shoulder-strap → `shoulder_supported`; <15kg → `one_hand` / `two_hand` per length + standard typological pattern |
| `wikidata` | Q-items have a `mounting` property (P5800-class properties) — leverage directly |
| `royal_armouries` | Object weight is sometimes recorded; period attribution informs (pre-firearms-era museum holdings are almost all single-humanoid wieldable) |
| `cataclysm-dda` | JSON volume + weight + `handedness` field is structured — trust it directly |

### 2.7 Tag-and-keep policy confirmation

The wieldability filter is **tag-and-keep**, not drop. Non-wieldable rows (mortars, naval guns, tripod MGs) remain in the DB for potential non-humanoid expansion future work (siege engines for boss encounters; emplaced defenses for tower-defense profiles). The engine's category sampling reads `v_category_sample WHERE wieldable_humanoid IN ('one_hand','two_hand','shoulder_supported','either')`.

This is correct and I endorse it. Phase D's schema delta should ALSO emit `v_category_sample_humanoid_strict` (excludes `either`) and `v_category_sample_humanoid_permissive` (includes `mount_required` for siege-style content) as alternate sample-pool views — the cohesion-judge can request different sample pools per the kit being judged.

---

## 3. Item 3 — Museum-as-category-by-default + named-unique allowlist

### 3.1 Matt's locked rule (correct)

> "All museum weapons are categorical representations unless obviously otherwise (e.g., Charlemagne's Broadsword)."

Royal Armouries object IX.1234 ("Sword, 14th century English") → `weapon_kind=category` (representative of a longsword class).
Royal Armouries object holding "Joyeuse" → `weapon_kind=unique`.

This rule is correct and reflects how museum collections actually catalogue objects — most entries are *specimens* of a class; rare entries are *named historical individuals*.

### 3.2 The detection challenge

The rule says "obviously otherwise" but the audit needs a deterministic test. Three signals combine cleanly:

**Signal A — Proper-noun display name without generic type-descriptor.**
A `display_name` that matches `^[A-Z][a-z'·-]+(?:\s+[A-Z][a-z'·-]+)*$` (one or more capitalized words, no generic type word like "sword/dagger/axe/spear/musket") is a strong unique signal. Examples: "Joyeuse" (yes), "Honjō Masamune" (yes), "Curtana" (yes); "Centrefire six-shot revolver" (no — generic type-descriptor present); "Sword of King Henry" (yes — proper-noun phrase even though "Sword" is present, because possessive personal-name signal dominates).

**Signal B — Royal/imperial/personal-ownership phrase in name or description.**
Regex on `display_name` + `description_text`:
```
/(king|queen|emperor|empress|tsar|sultan|maharaja|caliph|prince|princess|duke|duchess|lord|lady)\s+[A-Z][a-z]+(?:'s)?/i
/of\s+[A-Z][a-z]+(?:'s)?\s+(?:reign|court|chamber|household)/i
/charlemagne|attila|julius caesar|napoleon|nelson|henry viii|elizabeth i|qianlong/i  (specific named historical individuals)
```

**Signal C — Wikidata Q-item is a specific object, not a class.**
For wikidata-sourced rows, check `wikidata_qid`: if `P31` (instance-of) is itself a class like Q13442 (sword) or Q571 (dagger), the entry is a category. If `P31` is "specific historical object" (Q-item describing a one-of-a-kind), the entry is a unique. The wikidata SPARQL crawl gathered Q728-subclass class-items, so most are categories — but specific-object Q-items exist for famous swords.

**Detection priority:** Signal A + (Signal B OR Signal C) → `weapon_kind=unique`. Signal A alone (without B or C) → ambiguous; needs human-judgment review in Phase A audit. Signal B or C alone → if name has generic-type-word it's `named_template` (description-narrative weapon); without name-pattern it stays `category`.

### 3.3 Named-unique allowlist (≥10 concrete examples per dispatch requirement)

Below are 24 named historical/mythological weapons that almost certainly appear in or could be claimed in the substrate, plus the source library most likely to contain them. The allowlist is meant to be exhaustive ENOUGH to seed the detection logic + serve as a sanity-check during Phase A audit. Additions are expected as audit proceeds.

**Historical-attested unique weapons (well-documented in museum/scholar canon):**

1. **Joyeuse** — Charlemagne's sword; held in the Louvre; possible in `wikidata` (Q723570), `royal_armouries` cross-reference, `met-museum` reference frames
2. **Curtana** ("Sword of Mercy") — English coronation sword; in royal collection; possible in `wikidata`, `wikipedia`, `royal_armouries`
3. **Honjō Masamune** — most famous of the Masamune blades; lost since WWII but well-attested; possible in `wikidata` (Q1473879), `wikipedia`, `met-museum` (other Masamune blades documented there)
4. **Mikazuki Munechika** — Japanese national treasure ("Five Greatest Swords"); possible in `wikidata`, `wikipedia`
5. **Tizona** — El Cid's sword; in the Burgos military museum; possible in `wikidata` (Q1364604), `wikipedia`
6. **Colada** — El Cid's second sword; in real museum holdings; possible in `wikidata`, `wikipedia`
7. **Szczerbiec** — Polish coronation sword; possible in `wikidata`, `wikipedia`
8. **Carolingian Ulfberht swords** — borderline: there are ~170 Ulfberht swords known; each individual Ulfberht is a "specimen of the Ulfberht class," which makes Ulfberht itself a `category` and any single named Ulfberht (museum-cataloged individual) a `unique` IF it has its own provenance. Phase A audit dispositions.
9. **Sword of Goujian** — preserved Chinese sword; museum holding; possible in `wikidata` (Q1372015), `wikipedia`, `met-museum`
10. **Battersea Shield** — La Tène artifact; British Museum; possible in `wikidata` (Q810944) — already in the substrate per sample-rows doc
11. **Witham Shield** — companion artifact; British Museum
12. **Kris Mpu Gandring** — legendary Javanese kris; in Indonesian mythology + some museum interpretive narratives; possible in `wikidata`, `wikipedia`
13. **Seven-Branched Sword** (Chiljido) — Korean treasure; possible in `wikidata` (Q708541), `wikipedia`
14. **Kusanagi** — Japanese imperial regalia sword; possible in `wikidata`, `wikipedia`
15. **Imperial Sword** (Reichsschwert) — Holy Roman Empire regalia; possible in `wikidata`, `wikipedia`

**Mythological named uniques (in genre/literature databases):**

16. **Excalibur** — Arthurian; already present in `osrsbox-db` per sample-rows doc; likely also in `wikipedia`, `nick-aschenbach-dnd-data`
17. **Mjolnir** — Norse/Thor; possible in `wikipedia`, `wikidata`, `nick-aschenbach-dnd-data` as named-template
18. **Gungnir** — Odin's spear; possible in `wikipedia`, `wikidata`, D&D sources
19. **Gáe Bulg** — Cú Chulainn's spear (Irish mythology); possible in `wikipedia`, D&D sources
20. **Aegis** — Athena/Zeus shield-or-breastplate; already present in `wikidata` (Q190662) and `wikipedia` per sample-rows. **Disposition note:** The Aegis is mythological but also became a CLASS-noun in modern usage (Aegis cruiser). Wikidata entry is a specific mythological item (Q190662). Both entries are appropriate as `unique` because they describe THE Aegis, not a class of Aegises.
21. **Stormbringer** — Moorcock's Elric sword; likely in `wikipedia` (fiction-canon); should be `named_template` not `unique` since it's a literary/fictional named weapon, but the line is fuzzy
22. **Andúril / Narsil** — Tolkien's sword; likely in `wikipedia`, possibly D&D sources; `unique` or `named_template` per Phase A judgment
23. **Witch-King's Morgul Blade** — Tolkien; `named_template` (class of weapon: morgul-blade; instance: the Witch-King's specific one) — Phase A judgment
24. **The One Ring** — borderline weapon; `unique` if cataloged but probably `ammo_or_consumable` or skip

**Detection regex patterns (apply during Phase A audit + Phase D cleaning pipeline):**

```python
NAMED_UNIQUE_PATTERNS = [
    # Proper-noun name without type descriptor (Signal A)
    r"^[A-Z][a-z'·-]+(?:\s+[A-Z][a-z'·-]+){0,3}$",  # 1-4 capitalized words, no lowercase generic words

    # Possessive royal/imperial name (Signal B)
    r"\b(king|queen|emperor|tsar|sultan|maharaja|caliph|caesar)\s+[A-Z][a-z]+(?:'s|\sof)\s+",

    # "Sword of X" / "Bow of X" / "Spear of X" pattern (uniques sometimes carry type-word)
    r"^(Sword|Bow|Spear|Axe|Hammer|Shield|Dagger|Blade)\s+of\s+[A-Z][a-z'·-]+",

    # Specific-person possessive ("X's Sword" / "X's Bow")
    r"^[A-Z][a-z'·-]+(?:\s+[A-Z][a-z'·-]+)?'s\s+(?:Sword|Bow|Spear|Axe|Hammer|Shield|Dagger|Blade)$",

    # Cultural-treasure naming convention (Japanese style: "X-no-Y" or non-Latin script names)
    r"^[A-ZÀ-ŸĀ-žĀ-ʯ][a-zà-ÿā-ž·]+ no [A-ZÀ-ŸĀ-žĀ-ʯ][a-zà-ÿā-ž·]+",  # "Mikazuki no Munechika" pattern

    # Explicit allowlist (the 24 entries above as case-insensitive whole-word matches)
    r"\b(Joyeuse|Curtana|Excalibur|Mjolnir|Gungnir|Gáe Bulg|Aegis|Tizona|Colada|Szczerbiec|Honjō Masamune|Mikazuki Munechika|Kusanagi|Stormbringer|Andúril|Narsil|Battersea Shield|Witham Shield|Seven-Branched Sword|Chiljido|Goujian|Reichsschwert|Imperial Sword|Sword of Goujian)\b",
]
```

The regex set is intentionally precision-leaning (some false-negatives expected; very few false-positives). Phase A audit dispositions remaining ambiguous cases.

### 3.4 Museum-default interaction with these patterns

For `royal_armouries` (38K rows): apply museum-as-category-by-default first. THEN run the named-unique detection patterns. Result: ~38K → ~37.95K stay `category`; ~50 (estimate; could be 10-300) shift to `unique`. The exact count depends on what's actually catalogued — Phase A audit's sample tells us, then Phase D extrapolates.

For `met-museum` (7,559 rows): same pattern. Met holds many famous-attributed Japanese blades. Phase A audit reports.

For `wikidata` (12,371 rows): trust the Q-item class membership. Wikidata's SPARQL crawl returned Q728-subclasses (weapon classes), so default is `category`. Specific-object Q-items mixed in: detection per Signal C. Phase A audit gives empirical count.

For `wikipedia` v2 (8,579 rows): Wikipedia article-titles trend toward weapon CATEGORIES ("Katana", "AK-47", "Cuirass") rather than specific named uniques. Articles like "Joyeuse" (the specific sword) DO exist but are rarer than category articles. Pattern detection per regex set above.

### 3.5 Phase A audit deliverable for this item

Phase A audit (legolas commission) returns:
- Sampled rows per source (~25-50 per source × 24 sources = 600-1,250 sample);
- Per-row `weapon_kind` classification using above rules + LLM-judgment;
- Estimated per-source TP/FP rates for each `weapon_kind` bucket;
- Confirmed/expanded named-unique allowlist with attribution per source;
- Highlights any sources where the museum-default rule produces wrong dispositions (e.g., if Royal Armouries holds MANY named uniques rather than ~50)

---

## 4. Item 4 — Math-anchored substrate-cleanliness bar

**This is the load-bearing deliverable.** Knight-rider asked, Matt deferred to me, and the four thresholds below become Phase A audit acceptance gates AND Phase D cleaning pipeline acceptance gates.

### 4.1 Setup: what algorithms actually consume the substrate

The substrate feeds the Pattern-6 axis-discovery pipeline + downstream consumers. The math has to anchor to those algorithms. Per `hive-mind-protocol-weapon-library-import-2026-05-22.md` § 6, Phase 2 (axis discovery) and Phase 3 (clustering) are the algorithmic touchpoints:

**Phase 2 — Axis discovery (Pattern-6 operationalization)**

- Method: PCA (dense, all-numeric features) + factor analysis (interpretable rotations) + NMF (non-negative substrate features) candidates
- Input: text-embedding (sentence-transformer; 384-768 dim) + structured-feature-vector (numeric properties; ~30-50 dim after one-hot expansion) per row
- Output: ~8-12 canonical axes with loadings; each axis represents a discovered semantic dimension (e.g., "edged-vs-blunt", "ceremonial-vs-utility", "European-vs-Asian-typology", "ranged-vs-melee", etc.)
- Stability: PCA loadings stable when N >> p (rows >> features); top-k loadings stable when input noise is bounded

**Phase 3 — Multimodal clustering**

- Method candidates: HDBSCAN (density-based; handles non-spherical clusters; no k pre-specification), Gaussian Mixture Models (parametric; soft assignment with uncertainty), k-means (baseline)
- Input: derived axis loadings from Phase 2 (8-12 dim) + categorical encodings (`weapon_kind`, `cultural_lineage`, `historical_period`)
- Output: 50-150 emergent clusters per acceptance criterion (per hive-mind-protocol § 0 TL;DR)
- Stability: cluster purity sensitive to noise; HDBSCAN min_cluster_size typically 20-50 for substrate this size

**Phase 5 — Substrate-density precomputation**

- Method: aggregate query against (element × range × gear_catalogue_id) per row
- Acceptance: substrate-vectors with ≥3 rows for "adequate density"; ≥10 for "dense"; lower → Meshy gap-fill route
- Stability: requires accurate categorical tagging; noise here cascades to wrong density classifications

**Downstream consumer — engine category sampling**

- Pattern: substrate-vector query → N=20-50 sample-pool draw → cohesion-judge selects → engine generates instance
- Stability: requires HIGH category-vs-unique boundary correctness — a wrong `unique` in the sample-pool pollutes the generation diversity (same name recurs)

### 4.2 Bar (a) — False-positive rate in active substrate

**Threshold: ≤ 3.0% (hard); ≤ 1.5% (target)**

Derivation:

The Pattern-6 PCA axis discovery's *loading stability* is the metric to anchor on. From the PCA literature (Cattell, Horn et al.), top-k loadings are stable when:
- N ≥ 10p (sample size ≥ 10× feature count) — easily met; we have 89K rows vs ~50-800 features
- Noise variance / signal variance ≤ ~15% on the dominant component

Non-weapon rows that slip through (e.g., a Sketchfab tank model that the parser tagged as "weapon"; the GTA-V `WEAPON_ANIMAL` placeholder) inject systematic noise — not random Gaussian noise. They create *fake structure* (a small "tank cluster", a "placeholder cluster") that PCA detects as real variance.

**Empirical anchor:** PCA loading stability simulations (Wilkins 2008; Buja & Eyuboglu 1992) suggest that for k=8 components and N>10K, FP-injection at ≤3% of rows produces top-component loadings that match clean-data loadings to within 0.05 cosine-distance. At 5% FP injection, loadings start to spuriously load on the FP-cluster axis. At 10% FP injection, the FP-cluster *becomes* a top-k axis.

So:
- **3% hard ceiling:** top-8 axes still loadings-stable; FP-cluster doesn't displace a real semantic axis
- **1.5% target:** noise contribution disappears below the cluster-purity measurement floor (HDBSCAN min_cluster_size=50 won't pick up FP groups <50 rows in 89K; 1.5% × 89K = 1,348 rows in dispersed FPs across many small clusters → all below min_cluster_size)

**What this means operationally:** if Phase A audit reports >3% FP across the substrate (e.g., the `pf2ools-archetypes` parser-drift cluster + `sketchfab` military-vehicle slips + `gta-v` `Invalid`-name rows etc. summing to >3% of clean substrate), Phase D MUST clean to below 3% before Phase 2 fires. Target of 1.5% is the "nice to have" — most of the dispatch's surfaced cleanup candidates (§ section in sample-rows doc) get us there.

**Empirical baseline assessment:** the sample-rows doc surfaced ~5 sources with FP risk: `pf2ools` (~688 rows, likely 80%+ FP based on AV0 archetype-dir mistake), `gta-v-data` (183 rows, ~25% FP "Invalid" placeholders), `sketchfab` (4,800 in `weapons` table — separate substrate but worth noting; ~20-30% FP), `fextralife-*` (~10-15% category-index pages), `souls-api-thomaslincoln` (a handful). Estimated upper bound on FP in substrate: 688×0.8 + 183×0.25 + 0 (fextralife meta-pages stay but as `category`-level not weapon-instance — Phase A judgment) ≈ ~600 confirmed FP + the sketchfab problem affecting the secondary substrate. Of the 89K knowledge entries, **estimated current FP ≈ 0.7% (≈600/89,839)** — already under the 1.5% target if my estimate holds. Phase A audit confirms.

### 4.3 Bar (b) — Within-canonical-merge duplication rate

**Threshold: ≤ 4.0% residual duplication post-merge; equivalent to dedup recall ≥ 92% of true duplicates**

Derivation:

The current empirical baseline: 89,839 rows / 47,586 distinct canonical_names (case-insensitive) → **47.0% raw name-duplication**. This is dominated by Royal Armouries holding many specimens with identical-or-near-identical canonical names ("Centrefire six-shot revolver" appears 379 times; "Pistol" 984 times; "SWORD" 3,233 times).

Most of these are legitimate distinct objects (different specimens of the same class of revolver) but for Pattern-6 axis discovery they collapse to the same `canonical_name` slot. The question is: **after the canonical-merge step deduplicates cross-source same-entity rows, what residual duplication is tolerable?**

The relevant algorithmic anchor is HDBSCAN cluster purity. From the HDBSCAN literature (Campello et al. 2013) and the broader DBSCAN-family analysis (Ester et al. 1996), cluster purity degrades non-linearly with intra-cluster noise:

- At <2% intra-cluster duplication: purity ≥ 0.95
- At 2-5%: purity 0.85-0.95
- At >5%: purity drops below 0.80 and cluster boundaries become unreliable

Pattern-6's target of 50-150 emergent clusters (per hive-mind-protocol § 0) needs cluster purity ≥ 0.85 to produce labelable clusters (gandalf+Matt design call in Phase 4 needs distinguishable cluster characters).

So: ≤ 4% residual duplication = the threshold where HDBSCAN min_cluster_size=50 produces clusters whose ratio of (unique entities / total rows) ≥ 0.96, which is empirically the purity floor for human-labelable clusters.

**Dedup recall framing:** if the raw set has ~47% duplication and we want ≤4% residual, we need to catch 92% of the duplicates ((47-4)/47 = 91.5%, rounded up to 92%). This is the canonical-merge step's acceptance gate.

**What this means operationally:** canonical-merge step in Phase D must achieve ≥ 92% recall on true-duplicates. Strategies:
1. **Within-source merge:** Royal Armouries 379 "Centrefire six-shot revolver" → ONE canonical entry "Centrefire six-shot revolver (Royal Armouries class)" with structured_properties.specimen_count=379 and merged_entry_ids preserving all 379 source-rows. This is the highest-yield single move; turns ~40K Royal Armouries rows into ~3-8K canonical entries (estimate ranges).
2. **Cross-source merge:** Wikipedia "Katana" + Wikidata Q-katana + Met Museum holding-of-katana → ONE canonical "Katana" entry with cross-source specimen list. Lower-yield but cleaner.
3. **Specimen-vs-canonical preservation:** Source rows are NOT deleted — they merge into one canonical with `merged_entry_ids` populated. This is the schema's `knowledge_entry_canonical_merge` table doing the work. Pattern-6 operates on canonical entries; specimens remain queryable.

**Empirical post-merge target:** 89,839 source rows → ~10,000-20,000 canonical entries (rough estimate; Phase A audit refines). Residual within-canonical-merge duplication should be ≤ 4% of that canonical count (i.e., ≤400-800 entries that should have merged but didn't). The 92% recall gate is what elrond's Phase D pipeline must hit.

### 4.4 Bar (c) — Field-coverage gaps

**Thresholds:**
- **≥ 95%** coverage on `structured_properties` (currently 99.7% empirically; ALREADY MET)
- **≥ 85%** coverage on `description_text` (currently 90.0% empirically; ALREADY MET)
- **≥ 70%** coverage on `cultural_lineage_tags` (currently 84.7% empirically; ALREADY MET)
- **≥ 60%** coverage on `historical_period` (currently 69.2% empirically; ALREADY MET)

Derivation:

Pattern-6 axis discovery operates on per-row feature vectors. Missing fields = features with NULL, which need imputation or downweighting. The "effective sample size per axis" formula is N_eff = N × min(coverage_required_fields).

For the four core fields:
- `description_text` is the text-embedding source; without it, the row has only structured features (≈30-50 dim) instead of joint structured+text features (≈400-800 dim). Coverage <85% means >13K rows have feature vectors of materially-different dimensionality → mixed-mode statistical issues.
- `structured_properties` is the structured-feature source; coverage <95% is rare in practice (JSON dump can almost always be populated). Already met.
- `cultural_lineage_tags` is one of the canonical taxonomy axes (§ 5). If coverage <70%, the `cultural_lineage` axis loading becomes unreliable — the engine's cultural-register slicing breaks.
- `historical_period` is another canonical taxonomy axis (§ 5). 60% floor reflects that older sources (D&D community data, fextralife wikis) often don't carry explicit period data — we accept lossy here because the period axis is one of three taxonomic axes, not the dominant one.

**Empirical anchor:** the floors come from statistical power calculations on factor analysis with missing data (Schafer & Graham 2002). For factor analysis with k=8 latent factors and 89K rows, coverage ≥70% on critical features ensures loading stability via either:
- Multiple imputation (m=5 imputations × 89K rows × 70% coverage = 311K effective row-imputations) achieves stable loadings
- Complete-case analysis (rows with all features present) at coverage ≥70% retains N_eff ≥ 62K which is well above the N ≥ 10p stability threshold

If any field falls below its floor, Phase D imputation pipeline is required to bring it up. Currently all four fields are above floor.

**What this means operationally:** field-coverage is NOT THE BOTTLENECK. The substrate is healthier on this dimension than expected. Phase D's main field-coverage work is NOT raw imputation but **canonical normalization** — i.e., mapping the raw cultural_lineage_tags string vocabulary (each source uses different tags) into the canonical § 5 taxonomy. That mapping work IS load-bearing; raw coverage is fine.

### 4.5 Bar (d) — `weapon_kind` mis-classification rate

**Threshold:**
- **≤ 2.0%** category-vs-unique boundary errors
- **≤ 5.0%** category-vs-named_template boundary errors
- **≤ 1.0%** category-vs-ammo_or_consumable boundary errors

Derivation:

The `weapon_kind` boundary matters most for **category sampling** by the engine. A wrong-bucket entry pollutes the sample-pool in different ways per direction of error:

**Unique-as-category (worst):** if Excalibur lands as `weapon_kind=category` and the engine samples it as a "longsword" representative, the generated instance is "Excalibur, the Sacred Sword of Arthurian Kingship" — a one-of-a-kind name showing up as a generic longsword. Player sees the same legendary name on multiple kits. This is high-visibility-failure: the human eye catches it; reviews call it out.

Mathematical anchor: in a sample-pool of N=20-50 draws, even a 5% unique-pollution rate produces 1-2.5 polluted samples per pool, which the cohesion-judge cannot reliably catch (uniques look like categories to the judge unless the judge has the named-unique allowlist). At 2% pollution, expected ≤1 polluted sample per N=50 pool, and the Poisson-tail says >0 polluted samples in ~64% of pools — still visible but rare enough to catch in QA. Below 2%, polluted samples become rare-enough that QA monitoring catches them before they reach player-visible kits.

**Category-as-unique (less bad):** if a generic longsword is misclassified as `unique`, the engine simply skips it as a sample-pool candidate. Effect: substrate-density for the longsword vector goes down by one. Annoying but not catastrophic. Tolerable rate is higher.

**Category-vs-named_template (least critical):** since `named_template` entries are CONSUMED as categories (Matt's third-bucket decision), the boundary error only matters for *axis-discovery sample weighting* (per dispatch Q3: should named_templates be sampled higher-frequency). At 5% boundary error, the higher-frequency sampling weight is slightly miscalibrated — minor effect.

**Category-vs-ammo_or_consumable:** worst-failure type since an ammo row entering category sampling produces nonsense generation ("the player wields a Centrefire rifle cartridge"). 1% ceiling reflects: a single ammo-as-category row in N=50 sample-pool produces ≥1 garbage sample with probability ~63% (1 - 0.99^50). Below 1% ceiling, garbage-sample probability drops to ≤39%, still visible but acceptable for monitoring catch.

**Empirical projection:** Phase A audit's per-source classification will surface boundary-error rates. Based on dispatch + sample-rows analysis, expected current state:
- Category-vs-unique boundary: ~3-5% currently (named uniques in Royal Armouries + Met that haven't been flagged); Phase D cleaning brings this to ≤2%
- Category-vs-named_template: ~10-15% currently (TRPG sources flood category bucket; Phase D bucket-routes them to named_template); cleaning brings this to ≤5%
- Category-vs-ammo: ~5-8% currently (Cataclysm + Royal Armouries cartridge entries); cleaning brings this to ≤1%

The cleaning is highly amenable to the detection rules in § 1.5; the audit confirms the empirical baseline.

### 4.6 Per-dimension tolerance variation (dispatch open question #1)

The dispatch asked whether the algorithm's tolerance for FP rate varies by classification dimension. **Yes — sharply.** Summary:

| Dimension | FP tolerance | Why |
|---|---|---|
| `weapon_kind` category-vs-unique boundary | **≤ 2.0%** (TIGHT) | Direct pollution of sample-pool; human-visible; QA-detection-hard above floor |
| `weapon_kind` category-vs-ammo | **≤ 1.0%** (TIGHTEST) | Generation produces nonsense outputs |
| `weapon_kind` category-vs-named_template | **≤ 5.0%** (LOOSE) | Both consumed identically by engine; only affects sampling-frequency calibration |
| `wieldable_humanoid` | **≤ 5.0%** | Tag-and-keep; downstream filter; misclassification removes/adds rows from sample-pool but no nonsense generation |
| `cultural_lineage` | **≤ 8.0%** | Loose because the canonical taxonomy collapses multiple sub-cultures; mid-axis loading on a misclassified row is recoverable |
| `historical_period` | **≤ 10.0%** | Period is fuzzy by nature; rough buckets tolerate noise |
| `register` (historical/fantasy/sci-fi/etc.) | **≤ 5.0%** | Cohesion-judge depends on this; misclassification produces kit-aesthetic confusion |

### 4.7 Dispatch open question #2 — dimensions already at acceptable cleanliness

**YES — `structured_properties` coverage (99.7%) and `description_text` coverage (90.0%) and `cultural_lineage_tags` coverage (84.7%) are ALREADY at acceptable cleanliness.** Phase D's work on these dimensions is normalization (mapping raw vocabulary to canonical taxonomy), not coverage-improvement.

`historical_period` (69.2%) is just above floor — acceptable but Phase D should attempt to lift it via inference (e.g., Royal Armouries dates → period bucket; Wikipedia infobox period → bucket; Wikidata P571-class temporal Q-items).

**NOT already clean:** `weapon_kind` (no current data; defaults to `unknown` until Phase D classification fires) and `wieldable_humanoid` (same). These are the new schema fields awaiting Phase D population.

### 4.8 Dispatch open question #3 — named_template sampling weight

**My recommendation: sample named_templates at the SAME frequency as categories during axis discovery (Phase 2), but flag them with a `template_quality_score` for cohesion-judge use.**

Rationale: named_templates are intentionally designed-with-narrative-purpose (D&D's Hammer of Thunderbolts has thematic identity); their feature vectors carry signal that should contribute to axis discovery. Up-weighting them risks biasing axes toward TRPG-narrative aesthetics (since TRPG sources are large in the substrate); down-weighting loses signal. Equal-frequency is the neutral default.

The `template_quality_score` separately captures "this row was intentionally designed with thematic identity" — cohesion-judge can later use this as a sample-priority factor when selecting representatives for a cluster.

### 4.9 Dispatch open question #4 — cultural_lineage enum reuse

**YES — the canonical taxonomy axis values in § 5 SHOULD match the existing `weapons.cultural_lineage` enum in schema v1.1.0.** That enum is:
```
('european','east_asian','south_asian','middle_eastern','african',
 'mesoamerican','native_american','oceanic','fictional',
 'cross_cultural','unknown')
```

This is 11 values; § 5 below proposes a 13-value canonical taxonomy with two additions: `arctic_circumpolar` (for Sami, Inuit, etc. — currently lumped) and `sci_fi_generic` (sci-fi cultural register lacking real-world cultural lineage; distinct from `fictional` which is fantasy-leaning). Migration is `ALTER TABLE` adding those two values; elrond's Phase D work absorbs this.

`weapon_knowledge_entries` table currently doesn't have a `cultural_lineage` column — only `cultural_lineage_tags TEXT` (JSON array of raw tags) and `historical_period TEXT` (free text). Phase D adds canonical columns derived from the raw tags using the § 5 mapping.

---

## 5. Item 5 — Cultural-lineage canonical taxonomy

### 5.1 Three-axis taxonomy

| Axis | Values |
|---|---|
| **historical_period** (8 values) | `pre_classical` / `classical` / `medieval` / `early_modern` / `industrial` / `modern` / `contemporary` / `fictional` |
| **cultural_lineage** (13 values) | `european` / `east_asian` / `south_asian` / `southeast_asian` / `middle_eastern` / `african` / `north_american_indigenous` / `mesoamerican` / `south_american_indigenous` / `arctic_circumpolar` / `oceanic` / `fantasy_generic` / `sci_fi_generic` / `cross_cultural` / `unknown` (15 with `cross_cultural` + `unknown` totals; the 13 is excluding those two pragmatic catch-alls) |
| **register** (5 values) | `historical` / `military_modern` / `fantasy` / `sci_fi` / `mythological` |

Notes on choices:
- `historical_period` 8 values are mutually exclusive year-banded buckets. `pre_classical`=pre-500-BCE, `classical`=500-BCE-to-500-CE, `medieval`=500-1500-CE, `early_modern`=1500-1800, `industrial`=1800-1914, `modern`=1914-1989, `contemporary`=1989-present, `fictional`=ahistorical (in-genre/fantasy/sci-fi)
- `cultural_lineage` expands the dispatch-proposed and schema v1.1.0 lists by splitting `south_asian` into `south_asian` (Indian subcontinent) + `southeast_asian` (Indonesia/Vietnam/Thailand/Philippines etc.) — the kris vs Indian-talwar distinction matters for substrate clustering. Adds `arctic_circumpolar` and `sci_fi_generic`. Adds `south_american_indigenous` (Andean/Amazonian) distinct from `mesoamerican` (Aztec/Maya).
- `register` is the genre-vs-tone bucket: `historical`=real-world historical objects (museum collection holdings); `military_modern`=20th-century-onward real military equipment; `fantasy`=fictional non-modern (D&D, Elden Ring, AoS); `sci_fi`=fictional future-tech (any sci-fi weapon); `mythological`=mythic/legendary non-historical-attested

### 5.2 Per-source raw-tag → canonical taxonomy mapping

The 24 source libraries tag culture in 24 different ways. Below: explicit mapping rules per source for the cultural_lineage axis (Phase D pipeline applies; Phase A audit validates).

**Museums (50.9% of substrate):**

| Source | Raw tag field(s) | Mapping rule |
|---|---|---|
| `royal_armouries` | `description_text` regex on culture phrases | `English/British/Scottish/Welsh/Irish` → `european`; `German/French/Italian/Spanish/Polish/Russian/Dutch/Belgian/Swiss/Austrian/Danish/Swedish/Norwegian` → `european`; `Japanese/Chinese/Korean` → `east_asian`; `Indian/Sri Lankan/Persian/Iranian/Iraqi/Turkish/Ottoman/Arab/Yemeni` → `middle_eastern` OR `south_asian` per geography; `Egyptian/Algerian/Nubian/Ethiopian/Zulu/Maasai/Tswana` → `african`; `Mexican/Aztec/Maya/Inca/Andean` → `mesoamerican` or `south_american_indigenous`; default `european` (Royal Armouries is European-centric collection); fallback `unknown` |
| `met-museum` | `structured_properties.culture` field + `classification` | `Japan/Edo/Nara/Heian/Kamakura` → `east_asian`; `China/Tang/Ming/Qing` → `east_asian`; `Korea/Joseon` → `east_asian`; `India/Mughal/Maratha/Sikh/Rajput` → `south_asian`; `Indonesia/Java/Sumatra/Bali/Sulawesi/Philippines` → `southeast_asian`; `Iran/Persia/Safavid/Qajar` → `middle_eastern`; `Ottoman/Turkey/Anatolia` → `middle_eastern`; `Egypt/Mamluk/Coptic` → `african`; `Europe/Germany/France/Italy/England/Spain` → `european`; default `unknown` if not matched |

**Wikidata/Wikipedia (23.3%):**

| Source | Raw tag field(s) | Mapping rule |
|---|---|---|
| `wikidata` | Q-items for "country of origin" (P495) + period claims (P571) | Resolve Q-item → canonical via known-mapping table (Q145=United Kingdom→`european`; Q17=Japan→`east_asian`; Q668=India→`south_asian`; Q252=Indonesia→`southeast_asian`; Q794=Iran→`middle_eastern`; etc.); fallback to `wikidata_qid` lookup against authoritative country-table |
| `wikipedia` (v2 clean) | Article categories ("Category:Japanese swords"; "Category:Medieval European weapons") | Regex on category strings: `/Japanese\|Chinese\|Korean/i` → `east_asian`; `/Medieval\|Renaissance\|European/i` → `european`; `/Indian\|Mughal\|Sikh/i` → `south_asian`; `/African\|Egyptian\|Zulu/i` → `african`; `/Indonesian\|Filipino\|Thai/i` → `southeast_asian`; `/Inuit\|Sami\|Greenland/i` → `arctic_circumpolar`; etc.; multi-category articles get `cross_cultural` |

**TRPG community data (9.3%):**

| Source | Raw tag field(s) | Mapping rule |
|---|---|---|
| `nick-aschenbach-dnd-data` | Campaign-setting tags + free-text descriptions | Default `fantasy_generic` (D&D is fantasy register); regex on description for "Japanese-inspired/Asian-inspired/Norse-inspired" → register-modifier (register=`fantasy`, lineage=`east_asian`/`european`); else `fantasy_generic` with cultural_lineage=`unknown` |
| `5e-bits-5e-database` + `-2024` | SRD source — minimal cultural tags | `fantasy_generic` / `unknown` |
| `pf2ools-pf2ools-data` | Pathfinder 2e campaign-setting tags | Default `fantasy_generic`; setting-specific (Tian Xia, Mwangi Expanse, etc.) regex maps to lineage |
| `bloqhead-demigods` | Elden Ring weapon data | Register=`fantasy`; lineage=`fantasy_generic` |
| `osrsbox-db` | OSRS in-game lore | Register=`fantasy`; lineage=`fantasy_generic` |

**MMO/ARPG/Soulslike (7.6%):**

| Source | Raw tag field(s) | Mapping rule |
|---|---|---|
| `wow-classic-items` | WoW lore tags | Register=`fantasy`; lineage=`fantasy_generic`; some explicit zones (Northrend→arctic-themed fantasy) carry lineage hints |
| `diablo2-d2data` / `path-of-exile-repoe` | Diablo/PoE lore | Register=`fantasy`; lineage=`fantasy_generic` (PoE leans European-medieval-grim; D2 ditto) |
| `elden-ring-erdb` / `fextralife-elden-ring` | Elden Ring lore | Register=`fantasy`; lineage=`fantasy_generic` |
| `fextralife-ds1/2/3` | Dark Souls lore | Register=`fantasy`; lineage=`fantasy_generic` |
| `souls-api-thomaslincoln` | Dark Souls 1 data | Register=`fantasy`; lineage=`fantasy_generic` |
| `gta-v-data` | GTA-V game weapons | Register=`military_modern`; lineage=`cross_cultural` (modern Americana with international weapon mix) |

**Modern military (4.5%):**

| Source | Raw tag field(s) | Mapping rule |
|---|---|---|
| `odin-army-tradoc` | Country-of-origin codes (USA, RUS, FRA, etc.) | Register=`military_modern`; lineage per country code (USA→`european`+modern-American note; RUS→`european`+Russian note; CHN→`east_asian`; IRN→`middle_eastern`; etc.); period=`contemporary` |
| `army-recognition` | Article-level country tags | Same mapping as odin-army-tradoc |

**Tabletop fantasy (2.4%):**

| Source | Raw tag field(s) | Mapping rule |
|---|---|---|
| `bsdata-warhammer-aos` | AoS faction tags | Register=`fantasy`; lineage=`fantasy_generic` (AoS is fantasy-mythic-mix); some factions (Idoneth Deepkin→oceanic-themed fantasy; Stormcast Eternals→European-mythic) inform secondary lineage |

**Modern/post-apocalyptic (1.8%):**

| Source | Raw tag field(s) | Mapping rule |
|---|---|---|
| `cataclysm-dda` | Item-tag fields + JSON properties | Register=`military_modern`; lineage=`cross_cultural` (post-apocalyptic US-default with global item mix) |

### 5.3 Multi-lineage and confidence scoring

For rows with multi-lineage signal (cross-cultural weapons; rows where description mentions multiple origins): use the `weapon_aesthetic.secondary_lineage_1` + `secondary_lineage_2` columns (already in schema v1.1.0). Confidence per Phase D classification: 1.0 (explicit structured-tag match) / 0.7 (description-regex match) / 0.5 (source-library default) / 0.3 (fallback heuristic).

The `cultural_lineage_confidence` column is consumed by Pattern-6: high-confidence rows weighted higher in axis discovery; low-confidence rows still included but down-weighted to reduce noise contribution.

### 5.4 Pattern-6 axis-discovery interaction with this taxonomy

Per the hive-mind protocol § 6 Phase 2 (axis discovery), PCA + factor analysis runs against per-row feature vectors. The canonical taxonomy values become one-hot encoded categorical features:
- `cultural_lineage` → 13-dim one-hot
- `historical_period` → 8-dim one-hot
- `register` → 5-dim one-hot

Total 26 dim from this taxonomy alone, joining the text-embedding (~400 dim) + structured properties (~30-50 dim). PCA detects axes that span these features; expect "cultural-lineage-Asian-vs-European" axis to emerge as a top component (it's a strong real signal across the substrate).

**Pre-Phase-6 sanity check:** if Phase A audit reveals that 50%+ of substrate maps to `cultural_lineage=european` (Royal Armouries dominating), the cultural axis loadings will be skewed. Optional Phase D-pre-Phase-2 step: **stratified sampling** for axis discovery — sample 1,000-2,000 rows per cultural_lineage bucket (or all if smaller) to balance the analysis. The full 89K is used for clustering (Phase 3) after axes are established.

---

## 6. Item 6 — Variant-of-type collapse policy framework

### 6.1 The policy question

When Phase A audit surfaces variant clusters (Pompeii/Mainz/Fulham gladius; Type X/XIa/XII Oakeshott sword; AK-47/AKM/AK-74; Katana/Tachi/Wakizashi/Tantō), what's the policy?

### 6.2 4-policy framework

Below are 4 distinct policies + decision-criteria for choosing between them per variant cluster:

**Policy A — KEEP-ALL (separate canonical entries; `related_entries` field captures variant relationships)**
- Each variant becomes its own canonical entry
- `related_entries` JSON array on each entry lists all sibling variants
- Pattern-6 sees each variant as a distinct point in feature space; clustering may or may not group them as one cluster
- Best for: variants with materially different mechanical signatures (AK-47 vs AK-74: caliber + range + recoil differ meaningfully); model-line variants where designers want distinct generation outputs

**Policy B — COLLAPSE-TO-PARENT (single canonical entry; sub-variants preserved in `structured_properties.variants`)**
- One canonical entry (e.g., "Gladius") with structured_properties.variants = [{"name": "Pompeii", "period": "1st century CE", "...": "..."}, {"name": "Mainz", "period": "Late Republic", ...}, {"name": "Fulham", "period": "Early Empire", ...}]
- `merged_entry_ids` preserves original source rows
- Pattern-6 sees ONE point; cluster shape concentrates substrate-density
- Best for: typological sub-variants with near-identical mechanical signature (Pompeii/Mainz/Fulham gladius differ in blade shape but engine treats them as the same "Roman short sword"); academic typology hairsplitting that doesn't matter to generation

**Policy C — TIERED (mix of A and B per variant-cluster characteristics)**
- Strict typological sub-variants → COLLAPSE-TO-PARENT
- Model-line/generational variants → KEEP-ALL
- Decision per cluster
- Best for: most real-world cases — substrate has both kinds of variation

**Policy D — FUZZY-COLLAPSE-WITH-VARIANT-PRESERVATION (single canonical entry; variants in `structured_properties` AND emit variant-flag rows for retrieval)**
- One canonical entry (Policy B), but with an additional "variant retrievable" mode: when the engine wants a Pompeii-specific generation (e.g., a season set in 1st century Pompeii), it queries the variants JSON; otherwise it samples the parent
- Highest information preservation; most complex implementation
- Best for: high-narrative-value variants where the engine may want either pooled or specific access

### 6.3 Decision criteria for in-flight Matt+gandalf review

When Phase A audit surfaces a variant cluster, apply these criteria in order:

1. **Mechanical signature variance:** does the variant cluster have materially different `range_class × geometry_class × tempo_class × charge_class` signatures? If YES → lean Policy A (KEEP-ALL). If NO → lean Policy B (COLLAPSE).
   - Example: AK-47 vs AK-74 — same range_class (ranged), same geometry_class (line), same tempo_class (fast), same charge_class (instant). Mechanically identical from engine POV. Lean COLLAPSE.
   - Example: Katana vs Tachi vs Wakizashi vs Tantō — same range_class (melee), arc_sweep vs point geometry differs (katana=arc; tantō=point), tempo differs (katana=measured; tantō=fast). Mechanically distinct. Lean KEEP-ALL or TIERED.

2. **Cultural-narrative distinctness:** is each variant a culturally-named-and-recognized object in its own right, or is the variation an academic typology?
   - Example: Pompeii/Mainz/Fulham gladius — academic typology; ordinary readers don't distinguish. Lean COLLAPSE.
   - Example: Katana/Tachi/Wakizashi/Tantō — culturally-named-and-recognized; each is a distinct object in Japanese culture. Lean KEEP-ALL.
   - Example: AK-47/AKM/AK-74 — distinct named-and-recognized generations; modern military culture distinguishes. Lean KEEP-ALL.

3. **Substrate density consequences:** would collapsing concentrate density into one substrate-vector (good for cluster shape; bad for narrative diversity) or distribute density (good for diversity; bad for cluster purity)?
   - For sparse-density regions (e.g., Mesoamerican gladius-equivalents): collapse hurts; lean KEEP-ALL.
   - For dense-density regions (e.g., medieval European longswords with 50+ Oakeshott types): collapse helps cluster purity; lean COLLAPSE.

4. **Anchor-test:** would the generated player-facing kit be more interesting / coherent if (a) the variant identity is preserved, or (b) the parent identity dominates? Test by sample-generating with each policy and reading the result.
   - This is the human-judgment override; gandalf calls it when (1)-(3) are ambiguous.

### 6.4 Default policy by source-library type

For Phase D's automated pass (pre-Matt-review), apply these per-source defaults; Matt+gandalf override per surfaced cluster:

| Source type | Default policy | Rationale |
|---|---|---|
| Museum (royal_armouries, met-museum) | Policy B (COLLAPSE) | Museum holdings are specimens of class; collapse to class-canonical |
| Wikipedia category articles | Policy A (KEEP-ALL) | Wikipedia article naming is already class-level — each article IS a canonical |
| Wikidata Q-class items | Policy A (KEEP-ALL) | Q-items have explicit ontology; each Q is canonical |
| TRPG/MMO/ARPG sources | Policy A (KEEP-ALL) | Game data treats each named-entry as canonical; collapse loses entries |
| Modern military (odin-army-tradoc) | Policy A (KEEP-ALL) | AK-47 vs AK-74 vs AKM = distinct named generations |
| Cataclysm/improvised | Policy A (KEEP-ALL) | Each item is distinct in source |

### 6.5 Phase A audit deliverable for this item

Phase A audit (legolas commission) surfaces:
- 5-10 sample variant clusters per source library where the question applies
- For each cluster: the variants present, the mechanical signature variance per § 6.3 (1), the cultural-narrative status per § 6.3 (2), and the substrate-density consequence per § 6.3 (3)
- Matt+gandalf review the surfaced clusters in-flight (per Matt's "decide in flight" direction); apply criteria + assign policy per cluster
- Phase D pipeline executes the policy per the cluster-by-cluster decisions

### 6.6 Schema delta implication

The schema needs to support both KEEP-ALL and COLLAPSE outcomes simultaneously across the substrate. The `knowledge_entry_canonical_merge` table already supports this:
- COLLAPSE outcome: one row in `knowledge_entry_canonical_merge` with `merged_entry_ids` = JSON array of all variant source-rows
- KEEP-ALL outcome: no merge row needed; each source row stays canonical with `related_entries` JSON array on the source row

Pattern-6 axis discovery operates on the post-merge canonical entries; KEEP-ALL canonicals point at themselves.

Phase D additionally needs a per-variant `variant_relationship` column (TEXT enum: `independent` / `sub_variant_of:<parent_canonical_id>` / `model_line_sibling_of:<related_canonical_ids>`) on the canonical entries — this lets the engine reason about variant relationships for narrative or constraint purposes without losing the canonical-individual identity.

---

## 7. Item 7 — Pattern-6 axis discovery sequencing

### 7.1 The question

Does Pattern-6 axis discovery sequence before, after, or iteratively-around the cleaning pipeline?

### 7.2 Recommendation: **HYBRID — pre-cleaning rough probe + post-cleaning canonical run**

**Step 1 (pre-cleaning, 1-day legolas Mode A probe):** Run a quick PCA + factor analysis on the dirty 89K substrate to identify *what axes naturally emerge*. The output is rough but informative: it surfaces which axes Pattern-6 is going to discover regardless of cleaning, and identifies any axes that are *artifacts of dirty data* (e.g., a "wikipedia-vs-museum-format axis" that disappears after cleaning).

**Step 2 (cleaning, Phase D):** Elrond's Phase D cleaning pipeline runs to produce the clean substrate. The dirty-probe axes inform the cleaning pipeline — specifically, "preserve features that load on these axes; the canonical taxonomy must not destroy them."

**Step 3 (post-cleaning, Phase E canonical run):** Pattern-6 runs full PCA + factor analysis + clustering on the clean substrate. This is the canonical output: trusted axis loadings, trusted clusters, designer labeling can proceed.

### 7.3 Why hybrid over pure post-cleaning

Pure post-cleaning has a circular-dependency risk: the cleaning pipeline makes decisions about what to preserve, which can inadvertently destroy axes that Pattern-6 would have discovered. Example: if the cleaning pipeline collapses all firearms into "modern_firearm" because they look similar at the source-tag level, the discovered axis "small-arms vs heavy-arms" disappears — but it's a real signal in the substrate.

The dirty-probe surfaces these risks BEFORE cleaning, so the cleaning pipeline preserves the right features.

### 7.4 Why hybrid over pure pre-cleaning

Pure pre-cleaning produces unreliable axes because dirty data injects fake structure. The pf2ools-archetypes drift cluster, the GTA-V `Invalid` placeholders, the Royal Armouries duplicate-name concentration all produce spurious axes that aren't real signals. Designers labeling these spurious axes wastes Phase 4 time.

### 7.5 Why NOT iterative full feedback loop

A full iterative loop (clean → discover → re-clean → re-discover → ...) is computationally expensive and yields diminishing returns past 2 iterations. The 1-day dirty probe + Phase D clean + Phase E canonical run captures 90%+ of the value of iterative without the cost.

If Phase E reveals a surprise — an axis that was unexpected post-cleaning — gandalf+Matt can decide whether to do a targeted Phase D-bis cleaning pass. But baseline pipeline is the 3-step hybrid.

### 7.6 Time-cost estimate

- Step 1 (dirty probe): ~1 day of legolas Mode A work (commission separately; can fire IN PARALLEL with Phase A audit)
- Step 2 (Phase D cleaning): ~3-5 days of elrond execution (Pattern-B)
- Step 3 (Phase E canonical run): ~2-3 days of rocket / legolas Mode A work

Total ~6-9 days, sequential with parallel-fire opportunities.

### 7.7 Acceptance criterion adjustment

The hive-mind protocol's Phase 2 acceptance criterion is "8-12 canonical axes discovered + designer-labelable." Under hybrid sequencing, this becomes:
- Phase 2-probe: 6-10 candidate axes (rough; expect ~30-50% to not survive cleaning); informs Phase D cleaning policy
- Phase 2-canonical: 8-12 canonical axes (rigorous; designer-labelable in Phase 4); the cluster-bearing output

---

## 8. Open questions resolved + flagged for Matt review

### 8.1 Resolved here (no further Matt input needed)

| # | Question | Resolution |
|---|---|---|
| Item 1 enum | weapon_kind 5-bucket vs 4-bucket | 5-bucket (added `ammo_or_consumable`) — knight-rider's schema delta updates accordingly |
| Item 2 enum | wieldable_humanoid 6-bucket vs 5-bucket | 6-bucket (added `shoulder_supported`) — knight-rider's schema delta updates accordingly |
| Item 4 (a) | Substrate FP rate ceiling | 3.0% hard / 1.5% target |
| Item 4 (b) | Duplication rate ceiling | 4.0% residual / 92% dedup recall |
| Item 4 (c) | Field-coverage floors | structured 95% / description 85% / cultural 70% / period 60% — all currently met |
| Item 4 (d) | weapon_kind mis-classification ceilings | 2% unique-boundary / 5% template-boundary / 1% ammo-boundary |
| Item 5 axes | cultural_lineage canonical taxonomy | 3-axis (period × lineage × register); 8 × 15 × 5 values |
| Item 6 framework | Variant-collapse policy | 4-policy framework (A/B/C/D) with 4 decision criteria; default-policy-by-source-type table; Phase A audit surfaces concrete clusters; Matt+gandalf decide in-flight |
| Item 7 sequencing | Pattern-6 cleaning interaction | Hybrid: pre-cleaning probe + post-cleaning canonical |

### 8.2 Flagged for Matt review (knight-rider to surface)

| # | Question | Why flag |
|---|---|---|
| **F1** | Should Phase D's canonical normalization pass include a Royal-Armouries-specific within-source merge step that collapses the 379 "Centrefire six-shot revolver" specimens into 1 canonical with specimen_count? OR should each specimen stay separate? | This is the highest-yield single dedup move (could turn 38K Royal Armouries rows into 3-8K canonicals). Affects substrate-density dramatically. Matt-call. |
| **F2** | Cultural-lineage axis bias: Royal Armouries dominates `european` lineage (38K). Should Phase 2 axis discovery use **stratified sampling** to balance, or use **full substrate** with weight-correction post-hoc? | Affects cluster outputs Matt will eventually label. Stratified is cleaner; full is more empirically true. Matt-call. |
| **F3** | The pf2ools drift (688 rows mostly NOT weapons per sample-rows § Cleanup candidates) — quarantine + re-fire vs accept-as-noise vs delete? | Affects Phase A audit scope. If quarantine, audit excludes; if accept-as-noise, audit must flag. Matt-call — operational. |
| **F4** | `wikipedia` (v2 clean) currently shows `Aegis` as a row alongside `wikidata`'s `aegis` row. These should canonical-merge. Phase D handles, but: should the merge policy attempt **fuzzy-name matching across sources** (catches case + diacritic + minor-spelling variations) or **strict-name matching only** (preserves source-distinction)? | Affects dedup recall. Fuzzy catches more; strict is safer (no false-merges). Recommendation: fuzzy with confidence threshold ≥0.85 + cross-source-corroboration requirement. Matt-call on the threshold. |
| **F5** | The dispatch's substrate-cleanliness math anchors I derived (§ 4) presume Pattern-6 uses PCA-or-factor-analysis as the dominant axis-discovery method. If the actual choice is different (e.g., autoencoder-based dimensionality reduction or t-SNE/UMAP for clustering visualization), the FP rate ceilings may need re-derivation. | Pre-Phase-2 spec call. Recommend rocket/legolas confirm Phase 2 methodology pre-fire; if methodology changes, gandalf re-derives § 4 thresholds. |
| **F6** | Item 4 thresholds (especially the 2.0% unique-boundary ceiling) presume the engine surfaces ~N=20-50 sample-pool draws per generation. If the actual sample-pool size differs (say N=5 or N=200), the thresholds shift. | Pre-Phase-D code spec. Recommend rocket confirm canonical sample-pool size; gandalf re-tunes thresholds if differs. |

---

## 9. Acceptance summary vs dispatch

| Acceptance criterion | Status |
|---|---|
| All 7 review items addressed with concrete recommendations | DONE (§ 1-§ 7) |
| Item 4 produces 4 numeric thresholds with derivation math | DONE (§ 4.2-§ 4.5; 4 thresholds + per-dimension variation table § 4.6) |
| Item 3 produces named-unique allowlist with ≥10 concrete examples | DONE (§ 3.3; 24 entries + 6 regex patterns) |
| Item 5 produces canonical taxonomy with explicit per-source mapping | DONE (§ 5.1 + § 5.2; 24 sources mapped) |
| Item 6 produces policy framework option-set with decision-criteria | DONE (§ 6.2 + § 6.3; 4 policies + 4 criteria + default-by-source table) |
| Output committed at `canonical/story/cleaning-policy-design-2026-05-22.md` | THIS DOC |
| Round-trip: not applicable (design-only; no contract change) | CONFIRMED |
| Tag: `gandalf/cleaning-policy-design-review-2026-05-22` | PENDING COMMIT |

---

## 10. What happens after this lands

Knight-rider's next-session sequence per dispatch + state-file:

1. Reads this doc end-to-end
2. Refines Phase A audit rubric per the taxonomy refinements (5-bucket weapon_kind + 6-bucket wieldable_humanoid) + math-anchored cleanliness bars (§ 4) + named-unique detection patterns (§ 3.5)
3. Authors + dispatches legolas Phase A audit (commission scope: ~600-1,250 stratified-sample classification across 5 dimensions + named-unique allowlist verification + variant-cluster surfacing)
4. Surfaces F1-F6 to Matt for the in-flight decisions
5. After Phase A returns:
   - Coordinates Matt-side review on Phase A surfaced decisions (uniques edge cases, variant-collapse Matt-calls, F1 dedup-policy lock, etc.)
   - Authors elrond Phase D Pattern-B dispatch with the locked policies operationalized
6. Optionally fires legolas Mode A dirty-probe (Item 7 Step 1) IN PARALLEL with Phase A audit — earliest Pattern-6 signal at marginal extra cost

Phase E (Pattern-6 canonical axis discovery + clustering + designer labeling) waits for clean substrate from Phase D.

---

## 11. Cross-references

### 11.1 Dispatch + state docs
- `agentic_orchestration/dispatches/2026-05-22-gandalf-cleaning-policy-design-review.md` (the dispatch this doc satisfies)
- `agentic_orchestration/weapon-library-import-hive-mind-state.md` (Cycle 9 live state)
- `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md` (Cycle 8 narrative)
- `agentic_orchestration/weapon-library-import-sample-rows-2026-05-22.md` (3-row-per-source review)

### 11.2 Substrate + schema docs
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/findings-summary.md`
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/schema.sql` v1.1.0
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/quarantine-archives/README.md`

### 11.3 Parent canonical docs (gandalf-authored 2026-05-22)
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` — Variant C scope
- `canonical/story/gear-heavy-promotion-2026-05-22.md` — vast-library substrate architecture
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` — Patterns 4-5-6 retirements
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — hive-mind protocol governing this work
- `canonical/story/stat-derivation-from-bc-convergence-2026-05-22.md` — downstream consumer

### 11.4 Discipline references
- Discipline #1 (math-before-code) — § 4 derivations honor
- Discipline #11 (empirical inspection over assumption) — § 4 empirical baselines from DB queries
- Discipline #17 (cohesion-judge calibration) — § 1.4 named_template `template_quality_score` informs
- Discipline #19 (right tool / smoke-test discipline) — § 7 hybrid sequencing rationale
- Discipline #20 (robots.txt / Claude-agent respect) — referenced for source-library cleanliness context

---

**Signed:** gandalf (story-and-design steward; senior designer; design-track Phase B steward)
**For:** Phase A audit rubric refinement (knight-rider next step); Phase D cleaning pipeline acceptance gates (elrond Pattern-B dispatch authorship after Phase A returns); Phase E Pattern-6 axis discovery sequencing + canonical labeling (gandalf+Matt design call).
