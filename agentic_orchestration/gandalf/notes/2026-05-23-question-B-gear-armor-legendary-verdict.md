# Question B — Gear / Armor / Legendary-Class Verdict (Pattern A-deep)

> **STATUS:** CURRENT — gandalf verdict on Matt's Question B (raised 2026-05-23 11:05:57 EDT; killed by kernel panic before response; recovered + answered 2026-05-23 12:00 EDT post-Phase-E-1-incident). Pattern A-deep multi-question verdict authored at Matt direct invocation.

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — direct Pattern A-deep invocation ("engage both, pattern A-deep, B first")
**Status:** **Mixed: recognition + load-bearing**. The architectural commitments in §§ 2-4 are LOAD-BEARING for v1 design intent under existing canon (gear HEAVY, T4-A, fate-genre recognition). Specific catalogue/numerical commitments are **deferred** per substrate-led discipline + recognition-validate-commit (§ 8). Companion to the A verdict (forthcoming).
**Companion docs:**
- `canonical/00-ground-state.md` § 1 (current-truth oracle; this verdict lands as `agentic_orchestration/gandalf/notes/` entry, not canon — canonical promotion fires post-empirical-validation per § 8)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` (D1-D10 framing; D10 substrate-evidence gate)
- `canonical/story/gear-heavy-promotion-2026-05-22.md` (gear HEAVY lock; v1 vs v1.1+ scope draw § 8; one tier v1; baked; ≤5% per slot; option (c) convergence sequencing)
- `canonical/story/tier-4-architecture-defaults-2026-05-22.md` (T4-A architecture; 1 signature + 1-3 secondary; rank-3 completer; gear-anchored when signature_gear_archetype present; hand-authored catalogue ~30-50)
- `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` (named-mythological-weapons substrate § 3; faction emergence § 4.2; Track M1 substrate-enrichment proposal § 3.4; recognition-record discipline § 9)
- `canonical/story/w1-13-rescope-disposition-2026-05-22.md` (sim methodology framing; dual-witness + Surface A footnote; BDI/T4 alignment preservation; Surface A as design parameter § 3.3)
- `canonical/historical/17-gear-and-spirit-guide-design.md` (origin doc; Priority 02 gear design + Spirit Guide engine-API)
- MEMORY entries: `project_earth_meta_layer.md` (Rift canon; Form Library; Earth Self; gacha accumulation across seasons), `project_gear_and_spirit_guide.md`, `project_trait_architecture.md`
- Engine: `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (Discipline #11 empirical inspection over assumption; Discipline #18 methodology-before-execution)

---

## 0. TL;DR — top-line verdict

Matt's Question B contains four interlocking sub-questions. Here is the headline verdict for each, followed by per-sub-question reasoning in §§ 2-5.

| Sub-question | Verdict |
|---|---|
| **B-1: Armor design — once weapons solidify, what's the armor architecture?** | **Build a parallel armor-substrate library** (~5K-15K knowledge entries; same vast-library pattern as the 89K weapon substrate). Armor remains BAKED into spirit-forms per gear HEAVY § 4 (no equippable armor v1); the substrate provides the design vocabulary the engine reasons about + the visual ground truth for Phase D Meshy gap-fill. Armor substrate-vector dimensions parallel weapon's but with armor-specific axes (defensive-profile, coverage, ceremonial-vs-utility, etc.). |
| **B-2: Legendary class — how chosen with fate / mythical framing?** | **The "legendary class" IS the named-mythological substrate layer** already proposed as Track M1 in the fate-genre recognition doc § 3.4. Selection mechanic is gacha-style summoning (per Earth Meta-Layer / Form Library canon 2026-05-11), routed by faction-tradition affinity (per fate-genre § 4.2 13 predicted factions). Named-mythological binding is fixed-per-spirit-form (Fate canon: Saber→Excalibur is a binding, not a choice). Track M1 extends to armor too — named-mythological armor corpus exists (Aegis, Andvaranaut, Achilles' shield, Yamato Takeru's armor pieces) but is ~50-150 entries vs ~200-500 for weapons. |
| **B-3: What tier of skills for legendary items?** | **Tier 4 signature capstone (build-defining; rank-3 completer).** Named-mythological signatures REPLACE (or REPLACE-WITH-ENHANCEMENT) the substrate-only Tier 4 signature for spirits that carry named-mythological binding. Rationale anchored on Fate canon (Noble Phantasm IS the Servant's signature ability, not a passive modifier) + T4-A architecture (signature capstone is rank-3 completer; gear-anchored when signature_gear_archetype present — extends naturally to "named-mythological-anchored when named-mythological binding present"). Secondary capstones (1-3 rank-2 modulators) remain substrate-driven; may be themed by named-mythological tradition's secondary mechanics. **Tier 3 or below: REJECTED** — too marginal for the identity-weight of a named-mythological binding; would make legendary items feel like flavor footnotes. |
| **B-4: Combinatorial-strength testing methodology?** | **A/B paired sim methodology owned by gamora; critique-pair Gate-1 reviewed by jack-ryan + gandalf; methodology consultation via legolas Mode A at math hotspot.** Paired sims: same substrate-vector, one with named-mythological signature, one without. Measure WR-band delta. Acceptance: |delta| < 5% (named-mythological is identity-flavor, NOT power-amplification). Plus per-keystone sim-viability flag (parallels T4-B § 3.3 step 5). Plus BDI H1-H5 hypothesis-test extension to incorporate named-mythological as authorship parameter (parallels Surface A coupling per W1.13 § 3.3). |

**Critical caveat (load-bearing for the whole verdict):** the fate-genre recognition itself is a **Recognition Record** per its § 9 — architectural commitments deferred until P4 cluster labeling validates the 13 predicted factions. This verdict's §§ 2-4 commitments are therefore **conditional architectural intent**, not unconditional lock. The locks fire on P4 cluster-labeling acceptance. The recognition-validate-commit discipline runs through this verdict.

---

## 1. Question B verbatim + sub-question decomposition

### 1.1 Matt's question verbatim (recovered from interrupted-session transcript)

> B) gear. once we solidify weapons, we will still have these outstanding in the category: armor, legendary weapon/armor class (how to choose with fate and mythical framing's origin; what tier of skills to add to these? should they be build defining tier 4 or should they be chain defining/normal tier 4? Or should they be 3 or below? How should they be tested for combat combinatorial strenght against the skills from the skill trees?)

### 1.2 Sub-question decomposition

- **B-1:** Armor design — parallel substrate library? Or implicit in spirit-form baked configuration?
- **B-2:** Legendary class selection mechanic — how does "fate and mythical framing's origin" operationalize?
- **B-3:** Skill tier assignment for legendary items — build-defining Tier 4, secondary Tier 4, or Tier 3-below?
- **B-4:** Combat-combinatorial-strength testing methodology — how do we validate legendary skills don't break the WR-bracket discipline?

The four sub-questions are interlocking but the chain runs B-2 → B-1 → B-3 → B-4. The Fate-genre framing (B-2) reshapes the substrate architecture for both weapons and armor (B-1); the legendary class's skill-tier assignment (B-3) requires the Tier 4 architecture already locked at T4-A; the testing methodology (B-4) requires the existing convergence/sim engine + BDI hypothesis-test framework already designed at W1.13 + BDI § 6.

---

## 2. Sub-question B-1 — armor substrate library + spirit-form integration

### 2.1 The current canon position

Per `canonical/story/gear-heavy-promotion-2026-05-22.md` § 4:

- **Spirits are atomic.** Each spirit-form has a single character mesh (body + outfit + accessories baked) per asset-pipeline § 8 canonical rule.
- **Armor stat effects apply at the spirit level** — choosing this spirit means accepting this armor config. No inventory; no equip slots.
- **`gear_armor_decoupling = baked`** for Reincarnated profile v1. Decoupled is engine-flag-exposed for other profiles (e.g., Profile B B2B SaaS).
- **Per-slot armor effects ≤5% per slot**, convergence runs without gear-in-loop (option (c)).

### 2.2 What "armor" needs to be operationally in v1

The atomicity does NOT mean armor lacks engine-side substrate. It means armor is **rendered + presented + statted atomically with the spirit**. Engine-side, the spirit-form's armor configuration is still computed from:
- A substrate-vector (defense, resistances, cultural-lineage signal, period, ceremonial-vs-utility, etc.)
- A visual realization (the baked mesh's outfit + accessories)
- A stat-derivation (per-slot ≤5% effects summed into the spirit's defense / resistance numbers)

That substrate-vector has to come from somewhere. **Either it's derived from the spirit-form's overall substrate (no separate armor library) or it has its own armor-substrate library that supplies armor-specific dimensions.**

### 2.3 Recommended path — parallel armor-substrate library

**Gandalf-lean: build a parallel armor-substrate library, smaller in scale than the 89K weapon library.**

| Aspect | Spec (parallel-to-weapon-library pattern) |
|---|---|
| **Estimated volume** | ~5,000-15,000 armor knowledge entries (smaller than weapons because armor categories are more bounded; broader categories like "gambeson" or "lamellar" cover larger semantic regions per entry) |
| **Sources** | Wikipedia armor categories; Wikidata armor Q-items; Royal Armouries / Met Museum / Smithsonian armor collections (already partial coverage from weapon-library crawls); game wikis (D2/D3/D4/Last Epoch/Dark Souls/Monster Hunter armor); anime/manga character-armor wikis; D&D / Pathfinder armor SRD |
| **Schema** | Parallel to `weapon_knowledge_entries` per gear-heavy § 2.5; new table `armor_knowledge_entries` with armor-specific structured_properties (defensive_class, coverage, materials, ceremonial_vs_utility, era, cultural_tradition) |
| **License posture** | Same as weapons — Wikipedia/Wikidata CC0/CC-BY-SA; museums open; game wikis CC-BY-SA; verify per-source |
| **Workstream estimate** | 2-3 hive-mind cycles parallel to or following weapon-library cleanup completion |
| **Substrate-vector axes (predicted)** | Defensive profile (heavy/medium/light/none); coverage (full plate / torso-only / accessories); cultural-lineage (parallels weapon's 13 faction taxonomy); period; ceremonial-vs-utility; gendered vs gender-neutral aesthetic register |

### 2.4 Why parallel library, not derived-from-weapon-library

Two reasons:

1. **Different substrate dimensions matter.** A katana and a Japanese o-yoroi armor share cultural-lineage but the armor's defensive-class / coverage / ceremonial-vs-utility dimensions don't exist in the weapon library. Deriving armor from weapon-substrate would either lose those dimensions or force them into ill-fitting weapon-substrate cells.
2. **Substrate-led discipline.** Per `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` Pattern 4-5-6 retirements: don't pre-impose taxonomy where substrate should vote. Empirical armor clustering (P3-style multimodal clustering on armor knowledge entries) will surface emergent armor archetypes the way weapon clustering will surface emergent weapon archetypes. Hand-authoring an armor enumeration is a Pattern-5 violation (same shape as the retired 15-entry gear catalogue).

### 2.5 Integration with spirit-form atomicity

Per gear HEAVY § 4: spirits are baked. The armor substrate library doesn't change atomicity — it changes where the spirit's armor configuration COMES FROM at generation time.

Generation flow at spirit-form creation (v1):
```
Substrate-vector for spirit-form (element + skill + faction + tradition + cultural-lineage)
  ↓
Spirit-form configuration assembly:
  ├─ Weapon query → weapon_knowledge_entries (89K, growing) → signature weapon archetype
  ├─ Armor query → armor_knowledge_entries (~5K-15K, growing) → signature armor archetype  
  ├─ Visual realization → ChatGPT image-gen + Meshy → baked character mesh
  ├─ Stat derivation → per-slot armor effects summed → spirit's defense + resistances
  └─ Cohesion-judge naming → spirit-form name + lore
```

Player still experiences spirit-forms as atomic ("Inferno-Knight" is one thing, not weapon+armor); engine-side, both substrate libraries inform the generation.

### 2.6 v1 vs v1.1+ deferrals for armor

| Surface | v1 | v1.1+ deferred |
|---|---|---|
| Armor substrate commitment | HEAVY (real mechanical substrate at derived-tag-plus-tier-hierarchy level) parallel to weapon | G-PROMOTE-v1.1 (full generative emergence at BC-axis layer) |
| Armor catalogue | Vast library (~5K-15K knowledge entries) + emergent clusters | (unchanged; deepens with import progress) |
| Tier hierarchy | One tier (per gear HEAVY § 3 commitment) | Multi-tier (Normal/Exceptional/Elite or item-level scaling) when v1.1+ tier hierarchy lands |
| Gear-armor decoupling | Baked (Reincarnated profile) | Decoupled when loot system lands |
| Per-slot armor effects | ≤5% per slot (option (c)) | Larger effects supportable under option (a) |
| Armor affixes | Mark armor affixes can roll stat affixes (parallels weapon affix marginal variation) | Full affix-pool generation + rarity tiers |
| Phase D Meshy gap-fill for armor | Operational; same canonical pipeline as weapons | (unchanged) |

---

## 3. Sub-question B-2 — legendary class as the named-mythological substrate layer

### 3.1 The mapping is structural, not surface-level

Per `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` § 2.1 (the Reincarnated ↔ Fate one-to-one mapping):

| Fate / FGO | Reincarnated |
|---|---|
| Master | Earth Self |
| Servant | Spirit Form |
| Servant roster | Form Library (gacha-accumulated) |
| **Noble Phantasm** | **Substrate-grounded weapon + named-mythological echo** |
| Throne of Heroes + Holy Grail War | **The Rift** (canon 2026-05-11) |

Matt's "legendary weapon/armor class" = Reincarnated's **named-mythological substrate layer** (Fate's Noble Phantasm equivalent). This is the Track M1 substrate-enrichment proposal from fate-genre § 3.4.

### 3.2 Named-mythological corpus — extends to armor

Per fate-genre § 3.3, the named-mythological corpus is cross-cultural (200-500 distinct named WEAPONS, 800-1500 with cross-references). The fate-genre doc focused on weapons but the corpus extends to armor:

| Named-mythological armor corpus (representative; verify via Legolas Mode B catalogue crawl) | Tradition |
|---|---|
| Aegis (the goatskin / shield of Zeus and Athena) | Greek |
| Achilles' shield (forged by Hephaestus) | Greek |
| Brynhildr's armor + ring | Norse |
| Sif's golden hair (treated as worn relic) | Norse |
| Andvaranaut (Norse ring, weaponized accessory) | Norse |
| Sampo (Finnish mythical artifact, partially armor-like) | Finnish |
| Yamato Takeru's armor pieces | Japanese |
| Susanoo's named armor in some lineages | Japanese |
| Karna's birth-gift kavacha (golden armor) | Indian |
| Krishna's named ornaments (Kaustubha, Vaijayanti) | Indian |
| Pendragon-era named shields (Pridwen + variants) | Arthurian |
| Tlaloc's headdress / cape (priestly war-regalia) | Mesoamerican |
| Bog of Allen relic-armor named in Irish corpus | Celtic |
| Hauberk-of-Saint-Olaf / similar canonized relic-armor | European Christian |

**Estimated volume:** ~50-150 distinct named armor entries (smaller than weapons — mythology emphasizes signature weapons over signature armor). Track M1 extends to cover both.

### 3.3 Selection mechanic — Fate-style binding (not player choice)

Per fate-genre § 2.1: Fate canon binds each Servant to one signature Noble Phantasm. **The mapping is canon-driven, not player-choice-driven.** A Saber-class Servant has Excalibur (or whichever named weapon their historical/mythological identity carries). A Lancer has Gáe Bolg. The player doesn't pick the Noble Phantasm; they summon the Servant whose Noble Phantasm is canonically theirs.

**Reincarnated parallel:**
- Each spirit-form's named-mythological binding (if any) is determined at spirit-form generation by substrate-vector + faction-tradition affinity
- A Pendragon-Court spirit (substrate-vector ∋ {Arthurian tradition, knightly weapon class, holy element, leadership archetype}) gets bound to Excalibur or a related Arthurian named weapon at generation
- The binding is fixed: once the spirit-form is in the Form Library, its named-mythological binding doesn't change
- **Player "choice" mechanic = which spirit-form to summon/swap-to**, NOT which Noble Phantasm to equip
- Gacha summoning per Earth Meta-Layer canon 2026-05-11 — new spirit-forms enter the library via summoning; their named-mythological bindings are revealed at summon

### 3.4 Not every spirit has named-mythological binding

Critical: **named-mythological binding is OPT-IN at substrate-vector evaluation, not universal.** A spirit-form with substrate-vector that doesn't match any named-mythological corpus entry gets a substrate-only signature (per existing T4-A gear-anchored signature mechanic). This means:

- **Common-tier spirit-forms** — substrate-only; standard signature_gear_archetype-anchored Tier 4 signature
- **Legendary-tier spirit-forms** — substrate-vector triggers named-mythological binding; signature is named-mythological-anchored Tier 4 signature
- The legendary tier is RARE-by-design (substrate-vector matching restricts to specific cultural-lineage / tradition / archetype combinations)
- Gacha rarity tiers naturally align: common-tier vs legendary-tier maps to standard-vs-rare summon rates (genre canon: 3-star/4-star/5-star/SSR rarity hierarchies)

### 3.5 Empirical-evidence gate for this section's commitments

Per fate-genre § 9 (recognition-validate-commit discipline), the architectural commitments in §§ 3.1-3.4 above fire on:

1. **Track M1 substrate-enrichment dispatch** authored + executed (legolas Mode B catalogue crawl) → produces named-mythological substrate library
2. **P3 multimodal clustering** of weapon library produces clusters that coherently express cultural-mythological-tradition structure (the 13 predicted factions per fate-genre § 4.2)
3. **P4 cluster semantic labeling** confirms ≥80% cluster-naming with cultural-mythological-tradition identity; at least 8-10 of the 13 predicted factions clearly expressed
4. **Faction-coherent kit-pool methodology** validated post-P4

If P4 cluster labeling fails to surface faction structure coherently, this verdict's named-mythological-binding mechanic becomes premature — the underlying assumption (substrate clusters faction-coherently) failed empirical test. In that case, the named-mythological substrate exists but isn't bound via faction-tradition; binding becomes a different design problem.

---

## 4. Sub-question B-3 — skill tier assignment for legendary items

### 4.1 The three options Matt named

(a) **Build-defining Tier 4** (signature capstone; rank-3 completer; per T4-A § 2)
(b) **Chain-defining / normal Tier 4** (secondary capstone; rank-2 modulator; per T4-A § 2)
(c) **Tier 3 or below** (per-rank scaling tier; not regime-changing)

### 4.2 Verdict — option (a) Tier 4 signature capstone

**Named-mythological signatures REPLACE (or REPLACE-WITH-ENHANCEMENT) the substrate-only Tier 4 signature capstone for spirits that carry named-mythological binding.**

### 4.3 Per-option reasoning

| Option | Design-intent fidelity | Strengths | Weaknesses | Gandalf-lean |
|---|---|---|---|---|
| **(a) Tier 4 signature capstone** | ✅ Aligned with Fate canon: Noble Phantasm IS the Servant's signature ability (not a passive modifier). ✅ Aligned with T4-A: signature capstone is rank-3 completer; gear-anchored extends naturally to "named-mythological-anchored." ✅ Aligned with substrate-as-cohesion: named-mythological substrate is most identity-bearing entry; deserves most identity-bearing tier. | Player-experience: "I summoned Excalibur" becomes a defining moment, properly weighted. Architectural cleanliness: extends existing T4-A gear-anchoring mechanic without architectural amendment. Genre canon: FGO, Genshin, Honkai Star Rail all bind named-character ultimate to character identity. | Authorship cost: every named-mythological signature needs hand-authored regime-change mechanic per T4-A § 3.3 (and sim-viability flag per step 5). For 200-500 named weapons + 50-150 named armor, that's ~250-650 keystones. Larger than T4-A's ~30-50 catalogue. **Mitigated:** authorship is per-named-mythological-entry, not per-spirit-form (many spirits share named-mythological bindings via faction). Also: per-season per-faction rotation means full corpus doesn't all author at once. | **STRONG LEAN — primary path** |
| **(b) Tier 4 secondary capstone** | ⚠️ Partially aligned — secondary capstones are rank-2 modulators per T4-A § 2. Demoting a named-mythological binding to secondary undersells its identity weight. | Authorship cost lower (secondaries are smaller-magnitude per T4-A § 2.2). | **Major design weakness:** under-weights the named-mythological. A spirit's named-mythological IS its identity-defining feature per Fate canon; pushing it to secondary makes the substrate-only signature carry more identity weight than the named-mythological binding. That inverts the design intent. | REJECT as primary path; viable as supplementary tier (some named-mythological bindings carry BOTH a signature replacement AND a secondary capstone reflecting auxiliary mythology, e.g., Excalibur's signature + Avalon's secondary protection effect) |
| **(c) Tier 3 or below** | ❌ Not aligned. Tier 3 is per-rank scaling tier; named-mythological as Tier 3 reduces it to "this spirit has slightly better numbers for [reason]." Player-experience collapses; identity-weight collapses. | None aligned with named-mythological design intent. | Fatal: would make legendary items feel like flavor footnotes. The Fate-genre player who summons Excalibur expects defining-moment weight, not marginal modifier. | **REJECT** — not viable |

### 4.4 Hybrid path consideration — option (a) primary + (b) supplementary

Some named-mythological bindings naturally carry BOTH a primary signature AND a secondary auxiliary mythology. Examples:

- **Excalibur (primary) + Avalon (secondary):** Excalibur's signature regime-change (sun-blade burst damage; per Arthurian legend); Avalon's secondary protection effect (passive heal-over-time per Arthurian regenerative scabbard lore)
- **Mjolnir (primary) + Megingjörð (secondary):** Mjolnir's signature regime-change (thunder-strike with returning mechanic); Megingjörð's secondary (the belt that doubles Thor's strength; passive STR amplifier)
- **Gáe Bolg (primary) + Cú Chulainn's geis (secondary):** Gáe Bolg's signature (the heart-strike); the geis's secondary (taboo-breaking power-boost when conditions met)

**Recommendation:** option (a) primary + (b) supplementary is **the right answer for named-mythological bindings WITH richer mythological supporting context**. For named-mythological bindings WITHOUT richer context (simpler entries), option (a) signature-only is correct.

This is a per-named-mythological-entry authorship choice at T4-B catalogue authorship time.

### 4.5 What this changes vs T4-A

**Minimal architectural amendment.** T4-A § 5 already specifies signature capstone is gear-anchored when `signature_gear_archetype` is present. The named-mythological binding is structurally a special case of gear-anchoring: instead of being anchored to a gear-ARCHETYPE (e.g., "blunderbuss class"), the signature is anchored to a named-mythological INSTANCE (e.g., "Powder Hex-Cannon of the Holy Pirate Sniper canon"). The gear-anchoring mechanic extends naturally:

| Spirit-form binding tier | Signature anchoring | Catalogue source |
|---|---|---|
| Substrate-only | Substrate-vector → archetype (signature_gear_archetype = blunderbuss) | T4-A v1 catalogue (~30-50 generic per-archetype keystones) |
| Named-mythological | Substrate-vector → named-mythological binding (Excalibur, Mjolnir, etc.) | Track M1 named-mythological catalogue (~250-650 entries) |

The convergence engine treats both the same way (discrete categorical choice per chain per math note § 5). The cohesion-judge prompt extension (T4-C) gets a parameter for "named-mythological binding present (yes/no) + which one"; signature naming aligns accordingly.

### 4.6 v1 vs v1.1+ phasing for legendary skill tier

- **v1:** named-mythological binding ships with primary Tier 4 signature only (option (a)). Hybrid (a)+(b) supplementary deferred to v1.1+ (additional authorship investment).
- **v1.1+:** hybrid signature + auxiliary mythology secondary capstone for richer named-mythological entries.

---

## 5. Sub-question B-4 — combinatorial-strength testing methodology

### 5.1 The discipline frame

Per `canonical/story/w1-13-rescope-disposition-2026-05-22.md` § 3 (BDI + T4 architectural alignment preserved) and Discipline #18 (methodology-before-execution at math hotspots):

- Sim work is **gamora's seam** (engine simulation + balance per AGENTS.md)
- Methodology validation is **critique-pair Gate-1** (gandalf + jack-ryan)
- Methodology consultation at math hotspots is **legolas Mode A** (per Discipline #18; especially for sim methodologies that touch P5 cohesion-judge calibration)

### 5.2 Proposed testing methodology — A/B paired sim + WR-band delta

**Methodology Tier 1 (recommended):**

```
For each named-mythological binding in Track M1 catalogue:
  1. Identify substrate-vectors that would trigger this binding
     (filter: spirit-forms whose substrate matches the named-mythological's cultural-lineage + archetype)
  2. Generate ≥100 paired sim kits per binding:
       Pair A: substrate-vector + named-mythological signature
       Pair B: substrate-vector + substrate-only signature (control)
  3. Run gauntlet sims; measure WR-band convergence per kit
  4. Compute WR-band delta per pair: delta_i = WR(A_i) - WR(B_i)
  5. Aggregate: mean_delta, std_delta, |max_delta|
  6. Acceptance gates:
       - mean(|delta|) < 5% (named-mythological is identity-flavor, NOT power-amplification)
       - max(|delta|) < 10% (no single named-mythological outlier breaks WR discipline)
       - Pearson correlation between delta and substrate-vector dimensions < 0.3
         (named-mythological doesn't systematically amplify or deflate by substrate-cluster)
```

### 5.3 Why this methodology

1. **A/B paired methodology** isolates the named-mythological's contribution — identical substrate-vector except for the named-mythological binding. Variance from substrate-vector diversity cancels out across pairs.
2. **WR-band delta** is the existing balance discipline. Per gear HEAVY § 5 + W1.13 § 5, WR-brackets are the canonical balance target. The named-mythological needs to preserve WR-bracket discipline, not break it.
3. **|delta| < 5% acceptance gate** treats named-mythological as identity-flavor (small WR contribution; identity-bearing) NOT power-amplification (large WR contribution; would force named-mythological-mandatory builds = anti-pattern that destroys substrate-only spirits' viability).
4. **Pearson correlation gate** catches systematic biases — a named-mythological that secretly amplifies all controllers, for instance, would correlate with controller substrate-vector dimensions and fail this gate.

### 5.4 Sim-viability flag extension (per T4-A § 3.3 step 5)

Every named-mythological binding in the Track M1 catalogue carries a **sim-viability flag** before lock. Same discipline as T4-A § 3.3 step 5; same workflow (rocket runs sim-viability check; jack-ryan Gate-2 reviews; gandalf design ratification).

### 5.5 BDI hypothesis-test extension

Per W1.13 § 3 (BDI + T4 alignment), the BDI H1-H5 hypothesis tests already validate rank-3 substrate-richness expression at sim scale. The named-mythological layer extends BDI:

- **BDI H1-H5** (existing) — validates substrate-only Tier 4 signature's rank-3 expression
- **BDI H6 (NEW, proposed)** — validates named-mythological Tier 4 signature's rank-3 expression AT the named-mythological-substrate-vector intersection (does Excalibur-bound kit's γ-coefficient over the Arthurian+holy+leadership substrate-triple dominate the kit's β pairs? per BDI § 6)
- **BDI H7 (NEW, proposed)** — validates that named-mythological binding doesn't break substrate-only kit's γ-dominance for the same substrate-triple. (Named-mythological should ADD identity, not REPLACE substrate-led identity.)

H6 + H7 are math-hotspot work; require Discipline #18 methodology consultation via legolas Mode A before fire.

### 5.6 Sim methodology — Pattern-A vs Pattern-C scope

Per critique-pair gate protocol + math-hotspot routing:

- Initial methodology authoring is **gamora + legolas Mode A consultation** (math hotspot per Discipline #18)
- Critique-pair Gate-1 review: jack-ryan (process) + gandalf (design); BLOCK authority if methodology unsound
- Execution: gamora (Pattern-A or Pattern-C depending on scope)
- Critique-pair Gate-2 review: jack-ryan + gandalf with BLOCK authority on completion record

### 5.7 Empirical-evidence gate for this section's methodology

The methodology itself is **conditional on Track M1 substrate-enrichment landing first.** Until Track M1 produces the named-mythological substrate library, there's nothing to sim against. Sequencing:

```
Phase D weapon-library cleanup (in flight) → completes
  ↓
P2 axis discovery + P3 multimodal clustering → completes
  ↓
P4 cluster semantic labeling → validates faction structure (or refutes)
  ↓ IF faction-validated:
Track M1 named-mythological substrate-enrichment dispatch authored + fired
  ↓
Track M1 catalogue lands ~200-650 named-mythological entries
  ↓
T4-B named-mythological catalogue authorship (gandalf + Matt design pass)
  ↓
B-4 methodology fires (gamora + critique-pair + legolas Mode A consultation)
  ↓
Acceptance: |delta| < 5% per § 5.2 gates
```

---

## 6. Ranked recommendation tier table

Per Pattern A-deep spec, explicit ranking of all proposed paths:

| Tier | Path | Rationale | Sequence |
|---|---|---|---|
| **Tier 1 (must-fire; load-bearing for v1 design intent)** | (a) Armor substrate library parallel to weapon library (~5K-15K entries) per § 2 | Substrate-led discipline + spirit-form atomicity preserved + Phase D Meshy gap-fill applies | Post-weapon-library Phase D completion |
| **Tier 1 (must-fire; load-bearing for v1 design intent)** | (b) Named-mythological substrate layer = Track M1 (per fate-genre § 3.4) per § 3 | Fate-genre architectural mapping + structural device for legendary class identity | Post-P4 cluster-labeling validation (gates on faction structure surfacing) |
| **Tier 1 (must-fire; load-bearing for v1 design intent)** | (c) Tier 4 signature capstone for named-mythological bindings (option (a) for B-3) per § 4 | Fate canon (Noble Phantasm IS signature) + T4-A architectural alignment (gear-anchoring extends naturally) | Post-Track M1 catalogue + T4-B catalogue authorship pass |
| **Tier 2 (primary path; design-side ratified)** | (d) A/B paired sim methodology + WR-band delta gates + BDI H6/H7 extension per § 5 | Existing convergence + BDI framework extends cleanly; critique-pair Gate-1 ratifies methodology before fire | Post-Track M1 catalogue + critique-pair Gate-1 methodology review |
| **Tier 3 (supplementary; v1.1+)** | (e) Hybrid (a)+(b) supplementary capstone for named-mythological bindings with richer mythology per § 4.4 | Adds depth without v1 authorship-cost explosion | v1.1+ deferred |
| **Reserve (consider if Tier 1 paths face complications)** | (f) Substrate-only legendary signatures (legendary class WITHOUT named-mythological binding; just rare substrate-vector combinations producing rare keystones) | Fallback if Track M1 substrate-enrichment fails OR P4 cluster labeling doesn't surface faction structure | Reserve; only fires if Tier 1 (b) blocks |
| **Reject** | (g) Tier 3-or-below skill tier for legendary items (B-3 option (c)) | Under-weights named-mythological identity; collapses player-experience; Fate canon misaligned | Do not pursue |
| **Reject** | (h) Pre-imposed legendary enumeration (e.g., "we author 25 legendary items as canonical taxonomy") | Pattern-5 violation per legacy-cleanup audit; same shape as retired 15-entry gear catalogue | Do not pursue |

---

## 7. Cross-references to existing canon this verdict integrates

### 7.1 Canon this verdict preserves unchanged

- **Gear HEAVY commitment** (gear-heavy-promotion-2026-05-22.md): one-tier v1, baked, ≤5% per slot, convergence option (c), spirit atomicity. Armor verdict (§ 2) extends gear HEAVY to armor without amending it.
- **T4-A architecture** (tier-4-architecture-defaults-2026-05-22.md): 1 signature + 1-3 secondary, hand-authored catalogue, gear-anchored signature, T4-A→T4-E phasing. B-3 verdict (§ 4) extends T4-A via the named-mythological-anchoring case without amending T4-A's hierarchy commitment.
- **Substrate-led discipline** (legacy-categorical-cleanup-audit-2026-05-22.md): no pre-imposed taxonomies. Armor library (§ 2) and named-mythological library (§ 3) both follow substrate-led — IMPORT + CLUSTER rather than ENUMERATE.
- **Earth Meta-Layer canon** (project_earth_meta_layer.md, 2026-05-11): Form Library, gacha accumulation, Rift. Named-mythological binding mechanic (§ 3.3-3.4) operates inside this canon.
- **Recognition-validate-commit discipline** (fate-genre § 9): architectural commitments wait for empirical validation. § 8 below names the empirical-evidence criteria.

### 7.2 Canon this verdict augments (proposes addition)

- **T4-B catalogue authorship workflow** (T4-A § 3.3): step 1 ("Identify rank-3 candidate identities") extends to include named-mythological candidates from Track M1 catalogue, in addition to BDI ω/τ table substrate-pairs.
- **Track M1 substrate-enrichment** (fate-genre § 3.4): proposed dispatch extends to cover armor too (~50-150 named-mythological armor entries) in addition to ~200-500 named weapons.
- **BDI hypothesis tests** (existing H1-H5): proposed extension H6 (named-mythological rank-3 γ-dominance) + H7 (named-mythological doesn't break substrate-only rank-3 γ-dominance) at named-mythological substrate-vector intersection.

### 7.3 Decisions-log entries to propose (post-empirical-validation)

When the empirical gates in § 8 fire clean, the following decisions-log entries are warranted (jack-ryan owns writing):

- "Adopt named-mythological substrate layer (Track M1 weapons + armor) as legendary-class architecture; binding via faction-tradition affinity"
- "Adopt Tier 4 signature capstone tier for named-mythological skill assignment; substrate-only signatures continue for non-bound spirit-forms"
- "Adopt A/B paired sim methodology + WR-band |delta| < 5% acceptance gate for named-mythological combinatorial-strength testing; extend BDI hypothesis tests with H6 + H7"

---

## 8. Empirical-evidence criteria for re-engagement + architectural commitment

Per OP § 3.4 recognition-validate-commit + fate-genre § 9 substrate-led discipline:

| Verdict element | Empirical-evidence criterion to fire architectural lock |
|---|---|
| § 2 armor substrate library | Phase D weapon-library cleanup completes; weapon-library architecture validated as model; armor source-list authored by legolas Mode A research; volume estimate validates 5K-15K target |
| § 3 named-mythological substrate = legendary class | (1) P3 multimodal clustering on weapon library produces clusters with cultural-mythological-tradition structure (2) P4 cluster semantic labeling confirms ≥80% cluster-naming with cultural-mythological-tradition identity (3) ≥8 of 13 predicted factions surface in clusters. **IF P4 refutes faction structure → Tier 1 (b) blocks; Reserve (f) substrate-only legendary fires instead** |
| § 4 Tier 4 signature capstone for named-mythological | Track M1 catalogue lands; T4-B catalogue authorship includes named-mythological entries; sim-viability flags pass for ≥80% of named-mythological signatures |
| § 5 A/B paired sim methodology | Methodology consultation via legolas Mode A completes; critique-pair Gate-1 ratifies; first A/B run produces |delta| < 5% per § 5.2 gates |
| § 4.4 hybrid (a)+(b) supplementary capstone (v1.1+) | v1 catalogue ships; player telemetry surfaces named-mythological identity engagement; v1.1+ authorship budget approved |

**Architectural lock criterion (binding for the whole verdict):** when § 8 gates above fire clean, this verdict's §§ 2-4 architectural commitments upgrade from "recognition + design intent" to "load-bearing canon." Status updates to "RECOGNITION VALIDATED — see [downstream canon doc] for architectural lock," same pattern as fate-genre § 9.5.

---

## 9. What this verdict explicitly does NOT touch

Surface-level discipline — preventing scope creep:

- **Existing gear HEAVY v1 vs v1.1+ scope draw** (gear-heavy § 8). Not amended.
- **T4-A's ~30-50 hand-authored catalogue** (T4-A § 4). The Track M1 named-mythological catalogue is ADDITIVE (~250-650 entries layered on top), not REPLACEMENT.
- **Convergence-loop option (c) commitment** (gear-heavy § 5). v1 still runs convergence without gear-in-loop; option (a) preferred v1.1+.
- **Baked-by-default architecture** (gear-heavy § 4). Named-mythological binding doesn't change baking — spirit-forms remain atomic; named-mythological is part of the spirit's atomic configuration when binding present.
- **Question A** (W1.13 hypothesis tests + Tier 4 build-defining synergy authoring). That's the companion verdict, authoring next per Matt's "engage both, pattern A-deep, B first" instruction.

---

## 10. Sign-off

**Author:** gandalf (story-and-design steward)
**Pattern:** Pattern A-deep verdict per OP § 2 (multi-question; multi-page reasoning; per-option assessment; explicit ranked recommendation; anchor-doc citations by section)
**Authority for the verdict:** Matt 2026-05-23 direct invocation ("engage both, pattern A-deep, B first")
**Authority for architectural lock:** **Deferred** per § 8 empirical-evidence criteria. This verdict captures design-intent + recognition; the architectural commitments fire on substrate-led validation (P4 cluster labeling + Track M1 catalogue + sim-methodology Gate-1 ratification).
**Co-attestation:** none required at this layer (verdict, not decisions-log entry). When § 8 gates fire clean, jack-ryan writes decisions-log entries per § 7.3.
**Next:** Question A verdict (W1.13 + Tier 4 build-defining synergy hypothesis test authoring). Same Pattern A-deep shape; will land at `agentic_orchestration/gandalf/notes/2026-05-23-question-A-w1-13-tier-4-hypothesis-verdict.md`.

---

**Signed:** gandalf
**For:** the design-side verdict on Matt's Question B (gear / armor / legendary-class skill tier + combinatorial-strength testing methodology), recovered from the kernel-panic-interrupted session of 2026-05-23 11:05:57 EDT and authored fresh per Pattern A-deep discipline.
