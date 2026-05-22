# Gear-HEAVY Promotion — Real Mechanical Substrate in v1 + Vast-Library Pivot

**Date:** 2026-05-22 (evening session; canonical lock)
**Author:** gandalf (story-and-design steward; senior designer)
**Status:** v1 canonical lock — LITE framing retired; gear is real mechanical substrate in v1 at the derived-tag-plus-tier-hierarchy level; vast-library substrate pivot supersedes 15-entry hand-authored catalogue; WR-bracket-under-gear sequencing locked v1 vs v1.1+
**Authority:** Matt 2026-05-22 evening — three canonical calls (LITE→HEAVY rename + vast-library substrate pivot + 15-catalogue retirement as Patterns 4, 5, 6 of six vestigial retirements)
**Companion docs:**
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` § 3.4, § 3.5, § 3.6 (Patterns 4-5-6 detail)
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` (Variant C strategic lock; § 6 baked-by-default + decoupling-flag architecture)
- `canonical/story/stat-derivation-from-bc-convergence-2026-05-22.md` (stat-derivation companion; § 4.3 gear-affix integration)
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` (operationalizes the substrate import work)
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` (Profile A asset pipeline; companion finalization pending)
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/` (research foundation)

---

## 0. TL;DR

Three locked architectural commitments:

1. **LITE→HEAVY rename.** Gear-substrate is **real mechanical substrate in v1** at the derived-tag-plus-tier-hierarchy level. The "LITE" framing — which signaled "we're not committing to gear as substrate yet" — is retired. Full *generative* substrate promotion (gear-as-emergent-from-convergence at the BC-axis layer) remains v1.1+ (G-PROMOTE-v1.1).

2. **Vast-library substrate pivot.** The 15-entry hand-authored gear catalogue is retired as a pre-imposed enumeration. The substrate is instead **a queryable vast weapon library** — knowledge-first PRIMARY substrate (~15,000-30,000 weapon knowledge entries: Wikipedia + Wikidata + game wikis + SRD + museums + anime/manga wikis) with 3D models attached as SECONDARY visual references. Emergent clusters from statistical axis-discovery + clustering supersede the 15-entry enumeration.

3. **WR-bracket-under-gear sequencing.** In v1, gear effects are **small-magnitude baked armor** (≤5% per slot) and convergence runs **without gear-in-loop** (option (c) from prior conversation). In v1.1+, gear-in convergence loop OR two-pass calibration lands (option (a) preferred).

**Tier hierarchy commitment:** v1 ships with **one tier** per gear/armor. D2-style multi-tier (Normal / Exceptional / Elite or finer) is deferred to v1.1+. Reasoning: ship with the minimum viable tier surface; let progression depth deepen post-v1 once telemetry surfaces what depth is right.

**Baked-by-default with explicit decoupling-flag support** (per engine-as-general-product § 6): the Reincarnated profile ships baked-armor; the engine flag `gear_armor_decoupling = baked | decoupled` is exposed for profiles needing runtime equip-swap.

**Phase D Meshy generation gap-fill canonical pipeline:**

```
Weapon knowledge entry (rich text + properties + reference images)
   ↓
ChatGPT image-gen (prompted from knowledge data; T-pose-isolated; plain background)
   ↓
Meshy image-to-3D (mesh + PBR textures)
   ↓
Meshy rigging (most weapons static-attach; humanoid-rig if needed)
   ↓
Unity assembly (parented to RightHand bone; VFX attached per canonical galadriel § 8 rules)
```

This is the canonical visual pipeline when knowledge entries lack 3D model coverage. Same pipeline already validated for characters (Canary work 2026-05-22); adapted for weapons.

**The 15-entry catalogue is demoted from "canonical taxonomy" to "clustering hypothesis":** designer-authored predictions about what emergent clusters may surface in the imported library. Some will likely validate (greatsword cluster, wand cluster); some will likely merge (censer + holy symbol may collapse into broader "ritual implement" cluster); some unexpected clusters will likely surface (cultural-lineage clusters that the 15-entry catalogue elided).

**v1 vs v1.1+ scope draw** (§ 8) explicit.

---

## 1. LITE→HEAVY rename rationale

### 1.1 What LITE meant

The gear-substrate workstream entered the protocol (v1.3 § 6.2.2) as G1-LITE / G2-LITE / G5-LITE / G7-LITE. The LITE qualifier signaled:

- We're not committing to gear-as-substrate at the BC-axis layer yet
- Gear is treated as a **derived tag** post-convergence (signature_gear_archetype is computed from substrate-vector, not generated as substrate-input)
- Generation runs without gear-in-loop; gear is applied as overlay
- Full generative gear-substrate (where gear forms emerge from convergence pressure alongside element + skill) is deferred to G-PROMOTE-v1.1

The LITE framing was a hedge: ship with a gear surface that doesn't carry mechanical load; reserve full substrate promotion for post-v1 when empirical data informs the design.

### 1.2 What changed today (Matt 2026-05-22 evening)

Matt's canonical call: **gear-as-substrate is real in v1**. Not at the full generative-promotion layer (that stays v1.1+), but at the **derived-tag-plus-tier-hierarchy layer**. Gear has real mechanical effects (small-magnitude baked armor; signature gear-form per kit; per-element ω-affinity). It is not just a cosmetic tag.

The LITE framing under-sold this. By calling it LITE, the protocol communicated "we haven't committed to gear yet" — which is no longer accurate. Gear is committed; what *changes* between v1 and v1.1+ is whether gear-emergence happens at substrate-input or substrate-output layer.

**HEAVY** signals the commitment: gear is real mechanical substrate in v1; the v1.1+ promotion is a *further* deepening (full generative emergence), not the first commitment.

### 1.3 Naming sweep

| Old | New | Context |
|---|---|---|
| G1-LITE (rule-table workstream) | G1 (rule-table → cluster queries) | Protocol § 6.2.2 |
| G2-LITE (gear-archetype derivation) | G2 (gear-substrate derivation) | Protocol § 6.2.2 |
| G3-LITE (gear-instance generation constrained by archetype) | G3-LITE deferred to v1.1+ | Protocol; v1 uses density-routed library queries |
| G5-LITE (Unity integration with derived gear) | G5 (Unity integration with substrate-queried gear) | Protocol § 6.2.2 |
| G7-LITE (4-substrate empirical validation gate) | G7 deferred to v1.1+ | Protocol; v1 ships 3-substrate empirical test |
| LITE-path naming throughout | HEAVY-path naming for v1; LITE drops from vocabulary | Forward |
| "gear-substrate as derived tag" | "gear-substrate as substrate" | Forward |
| "gear is cosmetic v1; mechanical v1.1+" | "gear is real mechanical substrate v1; generative-emergence v1.1+" | Forward |

The LITE qualifier survives only in *historical references* (existing dispatches, commit messages, decisions-log entries dated pre-2026-05-22). New work uses HEAVY (or no qualifier — gear-substrate as bare term).

### 1.4 Why this matters operationally

The rename has downstream effects on:

- **Engineering disciplines compliance.** Discipline #1 (math-before-code) applies more rigorously when gear carries mechanical load. The gear-affix stat-variation math (per stat-derivation § 4.3) needs canonical specification before W1.15 implementation.
- **Cohesion-judge prompts.** When gear is real substrate (not cosmetic tag), the cohesion-judge prompts incorporate gear identity as a load-bearing input, not just a flavor footnote.
- **Telemetry attribution.** Per-kit gear effects become attributable telemetry. The pre-LITE-rename schema treated `signature_gear_archetype` as derived classification; post-HEAVY-rename, gear effects on stats + sim outcomes need first-class telemetry surfaces.
- **v1.1+ promotion path clarity.** G-PROMOTE-v1.1 (full generative emergence) is now clearly *the next promotion*, not "the first commitment." The path is HEAVY → G-PROMOTE-v1.1, not LITE → HEAVY → G-PROMOTE-v1.1.

---

## 2. Vast-library substrate architecture (knowledge-first PRIMARY + 3D models SECONDARY visual references)

### 2.1 The pivot

The original gear-substrate architecture (pre-2026-05-22 evening) had a 15-entry hand-authored catalogue as the substrate. Generation queried "what substrate-vector → which of 15 gear entries?" via the G1 rule-table.

The pivot Matt called late evening 2026-05-22: **the substrate is the vast library, not the 15 entries.**

The 15-entry catalogue was wrong-target in two ways:
1. **Wrong scale.** 15 entries cannot cover the genre space the engine wants to span. Reincarnated's spirit-form library accumulates across seasons; multiple seasons + multiple aesthetic registers + multiple cultural lineages need vocabulary far beyond 15 gear forms.
2. **Wrong substrate type.** 15 hand-authored entries are *enumeration*, not *substrate*. Substrate is something the engine can *query against* with rich semantic + mechanical + cultural-lineage dimensions. An enumeration of 15 is a closed list; a vast library is open substrate.

The corrected substrate is **knowledge-first**: ~15,000-30,000 weapon knowledge entries with rich textual + structured property + cultural/historical/genre context + reference images. 3D models attach as secondary visual references.

### 2.2 Why knowledge-first (not 3D-model-first)

Initial planning targeted 3D model libraries (Sketchfab + Kenney + OGA + Meshy) as primary substrate. Matt corrected: that's wrong-target.

**Knowledge entries carry the substrate the engine reasons about.** Mechanical properties (length, weight, two-handed-ness, range), cultural lineage (origin period, region, ceremonial vs utility), genre context (historical vs fantasy vs sci-fi vs anime), descriptive vocabulary (curved-blade, single-edged, polearm). These are what Pattern 6 axis-discovery operates on. PCA / factor analysis on knowledge-feature vectors produces meaningful substrate axes (edged-vs-blunt, cultural lineage, ceremonial-vs-utility).

**3D models carry the visual realization.** They are *attachments* to knowledge entries, not the substrate themselves. A knowledge entry for "katana" may have N model attachments (low-poly Kenney version; high-fidelity Sketchfab version; museum-grade Smithsonian scan; Meshy-generated variant). One model may render N knowledge entries (a generic "longsword" model serves as visual reference for multiple knowledge entries representing variant longswords).

The many-to-many relationship is captured in the schema (`knowledge_model_attachments` join table per orchestration plan).

### 2.3 Knowledge source landscape

Per the orchestration plan's RE-PLAN section + legolas Track A:

| Source | Format | Crawl viability | Estimated entries |
|---|---|---|---|
| Wikipedia weapons categories | REST API; structured infoboxes | Documented; crawler-friendly | ~5,000-15,000 entries |
| Wikidata weapon Q-items | SPARQL endpoint; CC0 | Documented; ideal | ~2,000-5,000 entries with rich property graphs |
| Game wikis (Fandom-hosted) | MediaWiki API per wiki | Crawler-friendly (verify per-wiki robots.txt) | ~2,000-10,000 across PoE/D3/D4/Last Epoch/Dark Souls/Monster Hunter/WoW/Bleach/SAO |
| D&D / Pathfinder SRD | Open Game License; static | Free; documented | ~100-200 weapons with rich mechanical taxonomy |
| Royal Armouries / Met Museum / Smithsonian | Various open APIs | Open data; museum-grade | ~5,000-10,000 historical weapons |
| TVTropes weapon tropes | Crawler-friendly; CC-BY-SA | Verify robots.txt | Fictional-genre taxonomy enrichment |
| IMFDB (Internet Movie Firearms Database) | Crawler-friendly | Verify robots.txt | Movies/TV weapon canon |
| Anime/manga weapon wikis | Mostly Fandom-hosted | Crawler-friendly | Isekai-relevant substrate enrichment |

**Total realistic target: ~15,000-30,000 weapon knowledge entries.** ~50-200MB of substrate data.

### 2.4 Reference images as first-class data

Per the orchestration plan's MEMO FOR LEGOLAS, knowledge entries carry **reference images as first-class data** (not after-thought attachments):

- Wikipedia almost always has Commons-licensed infobox + gallery images
- Wikidata Property P18 links to Commons images
- Wikimedia Commons direct image repository with structured license metadata
- Museums (Smithsonian / Royal Armouries / Met) provide museum-grade photos
- Game wikis carry in-game renders + item icons + 3D viewer captures
- D&D Beyond / Pathfinder SRD carry illustration art
- Anime/manga wikis carry character-with-weapon canonical art

**Why reference images matter:** they are the visual ground truth for the Phase D Meshy generation gap-fill validation loop. Without reference images, Meshy generation has no objective quality signal — we can't tell whether a generated katana looks "right" if we don't have authoritative reference photos to compare against.

The validation loop:
```
Reference images for knowledge entry → visual ground truth
  ↓
ChatGPT image-gen synthetic weapon image → compare to references
  ↓ PASS / FAIL
ChatGPT iterate or feed to Meshy → 3D mesh
  ↓ compare preview-image to references → PASS / FAIL
Unity assembly
```

Acceptance criterion per legolas Track A: ≥70% of knowledge entries with at least one reference image; ≥30% with canonical (primary) image marked.

### 2.5 The schema

Per the orchestration plan's RE-PLAN section:

```sql
-- Knowledge repository (PRIMARY substrate)
CREATE TABLE weapon_knowledge_entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  canonical_name TEXT NOT NULL,
  source_library TEXT NOT NULL,
  source_url TEXT NOT NULL,
  source_id TEXT,
  description_text TEXT,
  structured_properties JSON,
  cultural_lineage_tags JSON,
  historical_period TEXT,
  genre_appearances JSON,
  related_entries JSON,
  license_class TEXT,
  imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  -- Pattern 6 features (post-import pass)
  text_embedding BLOB,
  structured_feature_vector BLOB,
  derived_axis_loadings BLOB,
  cluster_id INTEGER REFERENCES clusters(id)
);

-- 3D model attachments (SECONDARY visual references)
CREATE TABLE knowledge_model_attachments (
  knowledge_entry_id INTEGER REFERENCES weapon_knowledge_entries(id),
  weapon_id INTEGER REFERENCES weapons(id),
  attachment_confidence REAL,
  attachment_source TEXT,
  PRIMARY KEY (knowledge_entry_id, weapon_id)
);

-- Canonical entry merging across sources
CREATE TABLE knowledge_entry_canonical_merge (
  canonical_id INTEGER PRIMARY KEY AUTOINCREMENT,
  canonical_name TEXT NOT NULL UNIQUE,
  merged_entry_ids JSON,
  merge_strategy TEXT,
  merge_confidence REAL
);

-- Reference images per knowledge entry
CREATE TABLE knowledge_entry_reference_images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  knowledge_entry_id INTEGER REFERENCES weapon_knowledge_entries(id),
  image_url TEXT NOT NULL,
  image_source TEXT,
  license_class TEXT,
  is_canonical BOOL,
  image_caption TEXT,
  image_local_path TEXT,
  width_px INTEGER,
  height_px INTEGER,
  imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reference_image_entry ON knowledge_entry_reference_images(knowledge_entry_id);
CREATE INDEX idx_reference_image_canonical ON knowledge_entry_reference_images(knowledge_entry_id, is_canonical);
```

Plus the existing 9-table schema (per legolas's `schema.sql`) for the 3D model side. The full schema lives at `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (greenfield as of 2026-05-22 evening).

---

## 3. Tier hierarchy commitment — one tier v1

### 3.1 The commitment

**v1 ships with one tier per gear / armor.** No D2-style Normal / Exceptional / Elite hierarchy. No PoE-style item-level scaling. No Last Epoch base-type vs unique vs set distinctions at the tier-hierarchy level.

Tier hierarchy depth > 1 is **deferred to v1.1+**.

### 3.2 Why one tier v1

**Reasoning:**

1. **Ship with minimum viable surface.** Multi-tier hierarchies are mechanically rich but require careful balancing to land cleanly. Diablo II's tier hierarchy (Normal / Exceptional / Elite × non-magic / magic / rare / set / unique) is genre-canonical but took years of iteration to balance. Reincarnated v1 ships with the minimum surface that supports the player loop; tier depth deepens post-v1 with empirical data on what depth feels right.

2. **The progression surface is the spirit-form library, not gear tiers.** Reincarnated's horizontal-collection-progression (per the Earth Self meta-layer) is the dominant progression surface. Each spirit-form in the library is a *unique entity* — its identity is its substrate signature, not its tier. Adding tier-hierarchy on top of horizontal-collection would compete with the library-as-progression pattern and dilute the gacha-style accumulation feel.

3. **Engine flag exposes the surface for other profiles.** The engine flag `tier_hierarchy_depth = 1` (default v1; 3 for D2-style v1.1+) lets profiles needing tier-hierarchy turn it on. Profile B (B2B SaaS) likely wants `tier_hierarchy_depth = 3` to match mainstream ARPG expectation. Reincarnated profile holds at 1.

4. **Avoid premature optimization.** Tier-hierarchy depth is a *gameplay-loop tuning parameter*, not an architectural commitment. Get the substrate-as-cohesion + library-accumulation + spirit-swap loops right v1; tune tier depth v1.1+ when playtesting surfaces calibration needs.

### 3.3 What "one tier" means operationally

- Each weapon in the library has a single canonical form (no Normal / Exceptional / Elite variants per weapon)
- Each spirit-form in the library has a single signature gear configuration (no upgrade path within a spirit)
- Per-element ω-affinity calculations operate on the single tier
- Stat-derivation projection operates on the single tier
- No tier-related affix prefixes / suffixes
- No tier-gated content (all content accessible at base tier)

### 3.4 What v1.1+ tier hierarchy looks like (sketch)

When v1.1+ opens, tier hierarchy candidates:

- **Diablo II style:** Normal / Exceptional / Elite per weapon (3× width); within-tier rarity (white / magic / rare / set / unique). Total tier × rarity ~15 variants per base weapon.
- **PoE style:** item-level scaling (1-100); affix-roll-driven rarity. No explicit tier hierarchy; tier is implicit in item-level + affix quality.
- **Hybrid:** narrow tier hierarchy (3 tiers) + within-tier affix variety (per the per-tier ω-affinity calibration).

Which tier model lands depends on v1 playtesting + Reincarnated's specific loop needs. The engine flag architecture supports any of these per-profile.

---

## 4. Baked-by-default with explicit decoupling-flag support

### 4.1 The architecture

Per `engine-as-general-serial-content-product-2026-05-22.md` § 6 (baked-by-default architecture):

- **Default behavior:** armor is *baked into the character mesh* (one mesh per spirit-form; armor visual is part of the character art). No runtime equip-swap.
- **Engine flag override:** `gear_armor_decoupling = baked | decoupled` exposed at engine level. Profiles needing runtime equip-swap set `decoupled`.
- **Reincarnated profile (v1):** `gear_armor_decoupling = baked`. Spirit-forms are atomic — each spirit is a unique character mesh; the player swaps among spirits via spirit-swap mechanic; no equipping armor *to* a spirit.
- **v1.1+ loot system:** when the loot system lands, the decoupling flag may flip to `decoupled` for Reincarnated profile if the loot system requires runtime equip. Decision deferred.

### 4.2 Why baked-by-default

**Reasoning:**

1. **Character mesh authoring cost.** Per legolas Unity catalogue findings: baked-armor path is clean ($0 additional asset cost); equippable armor needs Asset Store rigged packs ($80-130) plus per-spirit assembly engineering. Baked is cheaper to ship v1.

2. **Spirit-form atomicity.** Reincarnated's spirit-form library accumulates **whole characters** (the Canary of the Drowned Seam is a *complete* spirit — body + outfit + canary + flame). Decoupling armor from spirit breaks the atomicity; the player would be assembling spirits rather than collecting them.

3. **Visual cohesion.** Baked armor preserves designer-intent visual cohesion per spirit. Decoupled armor risks visual incoherence (mismatched aesthetic tuples; tech-level clashes when fire-mage equips primitive-tribal armor).

4. **Player expressive surface is the spirit-swap mechanic + library accumulation, not equip-loadout.** The Reincarnated player expresses through *which spirit they swap to*, not through *what armor they equipped*. Baked supports this; decoupled fights it.

### 4.3 What "baked" means operationally

- Each spirit-form has a single character mesh (body + outfit + rigid accessories all baked into one rig per asset-pipeline § 8 canonical rule)
- Armor stat effects (defense, resistances) apply at the spirit level — choosing this spirit means accepting this armor config
- No inventory of armor pieces; no equip slots; no swap-armor UI
- Per-element resistances + defense values are properties of the spirit-form, not separable equipment

### 4.4 What decoupled would look like (Profile B reference)

If Profile B (B2B SaaS) ships `gear_armor_decoupling = decoupled`:
- Per-tier-per-slot armor assets generated (head / chest / arms / legs / boots × tiers)
- Runtime equip system in Unity assembles armor onto base character rig
- Stat effects apply per equipped piece (sum across slots)
- Inventory + swap UI surfaces

The engine emits both baked + decoupled artifacts when the flag is set; profiles consume what they need. Reincarnated v1 consumes only baked.

---

## 5. WR-bracket-under-gear sequencing — v1 vs v1.1+

### 5.1 The convergence-loop question

Where does gear sit in the engine's mechanical convergence loop?

**Three options surfaced in prior conversation:**

- **(a) Gear-in-convergence-loop.** Gear effects participate in the gauntlet sim convergence loop. The kit converges *with* gear; gear pressure shapes the converged mechanical signature; WR-brackets calculated *with* gear effects in the mix.
- **(b) Two-pass calibration.** Convergence runs without gear; then gear effects layer on; then a second-pass calibration adjusts to maintain WR-bracket invariants.
- **(c) Small-effect baked armor; convergence runs without gear-in-loop.** Gear effects are *small enough* (≤5% per slot) that the convergence loop ignores them; gear effects layer on as marginal variation; WR-bracket targets are met substrate-only.

### 5.2 v1 commitment: option (c) — small-effect baked armor

**v1 ships option (c):**

- Per-slot armor effects ≤5% per slot
- Convergence runs without gear-in-loop
- Gear effects apply as marginal post-convergence overlay
- WR-bracket targets computed substrate-only

**Reasoning:**

1. **Convergence-loop stability.** Gear-in-convergence-loop adds dimensionality to the convergence search. The convergence loop is already operating at near-the-limit of stability (per B14.5 sidecar analyses: convergence iterations highest for controllers/mages); adding gear dimensionality risks destabilizing convergence.

2. **Calibration tractability.** Small-effect baked armor (≤5% per slot) is bounded enough that its sum across slots cannot blow up balance. Larger gear effects (D2-style 30-50% per piece) would require option (a) or (b) to maintain WR-brackets; small effects let option (c) work.

3. **v1 scope minimization.** Option (c) is the minimum surface that ships gear-as-substrate. Options (a) and (b) require more engineering investment + more empirical calibration. Ship (c) v1; promote to (a) or (b) v1.1+.

### 5.3 v1.1+ commitment: option (a) preferred

**v1.1+ promotes to option (a) — gear-in-convergence-loop — OR option (b) — two-pass calibration.**

**Preference for (a):**

1. **Substrate-as-cohesion-coherent.** Option (a) treats gear as full substrate alongside element + skill; the substrate-as-cohesion architectural commitment wants gear to participate in convergence pressure.

2. **Larger gear effects supportable.** Option (a) handles D2-style larger gear effects (15-30% per piece) cleanly because gear is part of the convergence math.

3. **Loot system compatibility.** When v1.1+ loot system lands, larger gear effects + meaningful gear variation become the player loop. Option (a) supports this; option (c) caps gear's contribution to a marginal layer.

**Option (b) as fallback** if option (a) destabilizes convergence at v1.1+ scale. Two-pass calibration is engineering-heavier but lower-risk than option (a).

### 5.4 Decision criterion for v1.1+ promotion

**Promote from (c) to (a) when:**

1. Convergence loop has demonstrated stability across v1 telemetry (Phase 5 + early B-series; ≥3 months production data)
2. Loot system design requires larger gear effects than ≤5% per slot
3. Engineering bandwidth available for convergence-loop-with-gear implementation
4. Cohesion-judge prompts can handle gear-as-substrate inputs cleanly (Phase 5 multi-aesthetic gate passes)

**Promote from (c) to (b) when:**

- (a) attempted and convergence destabilizes
- (b) is engineering-feasible alternative

---

## 6. The 15-entry catalogue retirement

### 6.1 What it was

The 15-entry gear catalogue (`gear-as-substrate-2026-05-21.md` § 3):

1. Greatsword
2. Twin daggers
3. Battle spear / longstaff
4. Mace / warhammer
5. Longbow
6. Crossbow
7. Blunderbuss / scattergun
8. Throwing knives / chakram
9. Wand / focus rod
10. Orb / sphere
11. Caster staff
12. Tome / grimoire
13. Censer / thurible
14. Holy symbol / icon
15. War-trumpet / horn

Designer-authored synthesis of ARPG canon (D2/D3/PoE weapon families) + thematic-class signaling. Each entry was a generation-input enumeration: when the rule-table mapped substrate-vector → gear, the output was one of these 15 values.

### 6.2 Why retired

Per Pattern 5 of the audit doc (§ 3.5):

1. **The list was closed.** 15 entries cannot cover the gear-form diversity Reincarnated wants to span (multiple aesthetic registers; multiple cultural lineages; multiple genres).
2. **The list inherited genre biases.** Asset Store coverage is "asymmetric (medieval-European saturated; non-European thin or absent)" per legolas Unity catalogue findings — exactly mirroring the catalogue's coverage shape. The catalogue inherited the genre's Eurocentric medieval-spanning bias.
3. **The list was pre-imposed.** Designer authored the 15; engine queried against them. Substrate-as-cohesion requires the substrate to be queryable open data, not closed enumeration.
4. **The list survives as predictive hypothesis.** What the 15 entries represent is *plausible emergent clusters*. The vast library + statistical clustering will surface emergent clusters; some of the 15 will likely validate (greatsword cluster, wand cluster); some will likely merge (censer + holy symbol → "ritual implement"); some unexpected clusters will surface (cultural-lineage clusters).

### 6.3 The clustering-hypothesis framing

The 15-entry catalogue is **not deleted**. It is **demoted** from "canonical taxonomy" to "clustering hypothesis":

- The list captures designer intuition about what clusters should emerge from the imported library
- Post-clustering Phase 3 + Phase 4 (per orchestration plan), the empirical clusters get compared against the 15 predictions
- Validated predictions: cluster matches a 15-entry prediction; designer label of the cluster aligns
- Refuted predictions: cluster either merges multiple 15-entry predictions OR splits one 15-entry prediction into multiple empirical clusters OR fails to surface at all
- Unexpected clusters: empirical clusters that the 15-entry catalogue elided (likely cultural-lineage-specific clusters: katana-family, kpinga-family, macuahuitl-family, etc.)

### 6.4 Per-prediction expectation

| 15-entry catalogue entry | Empirical clustering prediction |
|---|---|
| 1 Greatsword | Strong cluster expected; possibly merges with battle-spear into "two-handed melee" |
| 2 Twin daggers | Strong cluster; possibly splits into curved-vs-straight cultural-lineage variants |
| 3 Battle spear / longstaff | Strong cluster; possibly merges with greatsword |
| 4 Mace / warhammer | Strong cluster; possibly splits ceremonial-vs-utility |
| 5 Longbow | Strong cluster; possibly splits cultural-lineage variants (English / Japanese / composite) |
| 6 Crossbow | Likely cluster; possibly subordinate to longbow cluster |
| 7 Blunderbuss / scattergun | Borderline; small representation in library may not surface as separate cluster |
| 8 Throwing knives / chakram | Likely cluster; cultural-lineage splits (shuriken, chakram, kpinga) likely |
| 9 Wand / focus rod | Likely cluster; ceremonial-vs-utility split possible |
| 10 Orb / sphere | Borderline; may merge into wider "focus implement" cluster |
| 11 Caster staff | Strong cluster; cultural-lineage variants likely (Western wizard staff vs Asian sage staff) |
| 12 Tome / grimoire | Borderline; may merge into "focus implement" or stand alone |
| 13 Censer / thurible | Likely merges with holy symbol into "ritual implement" cluster |
| 14 Holy symbol / icon | Likely merges with censer |
| 15 War-trumpet / horn | Borderline; small library representation; may merge into "ceremonial sound-instrument" |

**Empirical clustering surfaces what the catalogue couldn't predict:**
- Cultural-lineage clusters (katana-family, dao-family, kpinga-family, macuahuitl-family) likely surface as first-class clusters
- Cross-genre clusters (anime-styled curved-blade weapons, sci-fi-styled energy weapons) likely surface
- Ritual / ceremonial clusters likely surface across cultural lineages

Phase 4 (Cluster Semantic Labeling) per orchestration plan resolves the empirical clusters into canonical labels.

---

## 7. Phase D Meshy generation gap-fill canonical pipeline

### 7.1 The pipeline (canonical)

When knowledge entries lack 3D model coverage (gap-fill region in the density map), Meshy generation produces visual assets:

```
Weapon knowledge entry (rich text + properties + reference images)
   ↓
ChatGPT image-gen
  - Prompted from knowledge data
  - T-pose-isolated (weapon presented in canonical reference pose)
  - Plain white background
  - Per canonical character-image specs adapted for weapon-props
   ↓
Meshy image-to-3D
  - Mesh + PBR textures
  - Output format per Unity import spec
   ↓
Meshy rigging
  - Most weapons static-attach (no rigging needed)
  - Humanoid-rig only for unusual weapon types (e.g., weapons with moving parts)
   ↓
Unity assembly
  - Parented to RightHand bone
  - VFX attached per canonical galadriel § 8 rules (rigid-static vs independent-life)
  - Static accessories baked into mesh
  - Dynamic / independent-life effects (flames, glow, particles) added as Unity-layer
```

This is the same pipeline already validated for characters (Canary work 2026-05-22 documented in `galadriel/notes/2026-05-22-canary-meshy-regen.md`); adapted for weapons.

### 7.2 Validation loop

Per orchestration plan § MEMO FOR LEGOLAS:

```
Reference images for weapon knowledge entry → visual ground truth
   ↓
ChatGPT image-gen → synthetic weapon image
   ↓ galadriel visual-similarity scoring → PASS / FAIL
PASS → feed to Meshy image-to-3D
FAIL → re-prompt ChatGPT with adjusted parameters; iterate
   ↓
Meshy 3D mesh
   ↓ galadriel preview-image-similarity to reference → PASS / FAIL
PASS → ready for Unity assembly
FAIL → re-iterate or route to alternative source
```

**The reference images are the validation ground truth.** Without them, Meshy generation has no objective quality signal. Acceptance criterion per Track A: ≥70% knowledge entries with reference images; ≥30% with canonical primary image marked.

### 7.3 Density-routing pattern

Per legolas's findings (`selection-patterns.md`) and the orchestration plan D11 substrate-density precomputation:

```
Substrate-vector query → density check
  ↓
Dense region (≥N library matches) → library-routed
  - Query weapons table
  - Return top-K matches by ω-score + cohesion-fit
  - No Meshy generation needed
  ↓
Sparse region (<N library matches) → Meshy gap-fill routed
  - Identify representative knowledge entry from the sparse cluster
  - ChatGPT → Meshy pipeline runs
  - Generated asset attached to knowledge entry post-generation
  - Density map updates
```

The density map evolves as the catalogue grows. Initial Phase D runs target the most identified sparse regions; subsequent runs gap-fill as needed.

### 7.4 Canonical rule on what goes in source vs Unity layer

Per `galadriel/notes/2026-05-22-canary-meshy-regen.md` § 8 canonical lesson:

| Accessory category | Pattern | Examples |
|---|---|---|
| **Rigidly-attached static** — moves WITH the body part by design | OK in source; baked into mesh | Medallion / emblem; sash; fixed pouch; armor pieces; carried tool without independent life; attached holster |
| **Independent-life dynamic** — needs its own movement/behavior | Must be Unity-layer; never in source | Companion creatures (canary, familiar, spirit-pet); element-derived VFX (flames, lightning, holy glow); flowing cloth (cape, banner); detachable items; spirit-guide manifestations |

**Decision criterion:** "when the character animates, does this thing have its own intended movement OR should it stay rigidly attached?" First category → source-bakeable. Second category → Unity-layer with separate-root parented via Animation Rigging.

**Three-level pipeline success distinction:**
1. Geometric preservation — does the desired feature appear in the output mesh?
2. Rig correctness — is the feature attached to the right bone with right weights?
3. Animation usability — does the feature behave correctly when the character animates?

The v2 canary test (2026-05-22) hit (1) cleanly but failed (3) catastrophically. Future Meshy predictions must structure prediction around all three levels.

---

## 8. v1 vs v1.1+ scope draw (explicit lines)

| Surface | v1 ships | v1.1+ deferred |
|---|---|---|
| Gear-substrate commitment | HEAVY (real mechanical substrate at derived-tag-plus-tier-hierarchy level) | G-PROMOTE-v1.1 (full generative emergence at BC-axis layer) |
| Catalogue | Vast library (knowledge-first) + emergent clusters | (unchanged; deepens with import progress) |
| Tier hierarchy | One tier | D2-style multi-tier (Normal / Exceptional / Elite) or PoE-style item-level scaling |
| Gear-armor decoupling | Baked (Reincarnated profile) | Decoupled when loot system lands |
| Convergence-loop sequencing | Option (c) — small-effect baked armor; convergence runs without gear-in-loop | Option (a) preferred — gear-in-convergence-loop; option (b) two-pass calibration as fallback |
| Per-slot armor effects | ≤5% per slot | Larger effects (D2-style 15-30% per piece) supportable under option (a) |
| Gear affixes | Mark gear affixes can roll stat affixes (marginal variation per stat-derivation § 4.3) | Full affix-pool generation + rarity tiers |
| Phase D Meshy gap-fill | Operational; pipeline canonical | (unchanged; evolves with density-map maturation) |
| Reference-image validation loop | Operational; ≥70% knowledge entries with reference images | (unchanged) |
| 15-entry catalogue | Demoted to clustering hypothesis | (catalogue is gone; clusters are canonical) |
| Cultural-lineage register | Multi-aesthetic medieval-spanning (per Variant C lock) | Sci-fi + post-singularity expansion |
| Asset Store integration | Tier 1 ($140-180 medieval-European core) + Meshy gap-fill | Expanded coverage as needed |
| LITE qualifier | Retired; HEAVY used forward | (no qualifier needed) |

**v1 vs v1.1+ decision criterion summary:**

- v1 = "ship the smallest surface that supports substrate-as-cohesion + spirit-form library + spirit-swap mechanic with mechanical gear effects"
- v1.1+ = "deepen substrate-as-cohesion to full generative gear emergence + multi-tier hierarchy + decoupled armor + loot system + sci-fi register expansion"

---

## 9. Cross-references

### 9.1 This session's canonical foundations
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` § 3.4 + § 3.5 + § 3.6 — Patterns 4-5-6 detail (parent audit)
- `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` — Variant C strategic lock; § 6 baked-by-default + decoupling-flag architecture
- `canonical/story/stat-derivation-from-bc-convergence-2026-05-22.md` — stat-derivation companion; § 4.3 gear-affix integration
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — operationalizes the substrate import workstream

### 9.2 Asset pipeline + visual pipeline
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` — Profile A asset pipeline (companion finalization pending)
- `agentic_orchestration/galadriel/notes/2026-05-22-canary-meshy-regen.md` § 8 — canonical pipeline rule (rigid-static vs independent-life; three-level pipeline success distinction)
- `agentic_orchestration/legolas/research/meshy-pipeline-2026-05-22/findings.md` — Meshy pipeline capability research

### 9.3 Library + schema foundations
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/findings-summary.md` — five headline findings
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/library-enumeration.md` — 14-library inventory
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/metadata-normalization.md` — canonical tag schema
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/sql-ddl-proposal.md` + `schema.sql` — 9-table base schema
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/selection-patterns.md` — 7 parameterized query templates + density-routing
- `agentic_orchestration/legolas/research/weapon-library-import-2026-05-22/import-strategy.md` — four-phase plan (A-D)
- `agentic_orchestration/legolas/research/unity-catalogue-armor-meshy-2026-05-22/` — Unity catalogue + Meshy armor capability research

### 9.4 Historical / superseded references
- `canonical/story/gear-as-substrate-2026-05-21.md` — 15-entry catalogue origin; § 3 demoted to clustering hypothesis
- `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` — surface-cleaned; full restructure pending (rule-table → cluster queries)
- `canonical/story/bdi-omega-tau-tables-v1-2026-05-22.md` — BDI ω/τ formalism (recalibration pending under role_orientation drop + cluster substrate)

### 9.5 BC axes + element foundations
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` — 8 BC axes canonical definitions
- `canonical/story/substrate-design-supplement-2026-05-21.md` — per-element identity-stance definitions
- `~/Games/reincarnated-engine/src/reincarnated/generation/element_biases.py:28` — ELEMENT_SCALING_ATTRIBUTE

### 9.6 Operational / orchestration
- `agentic_orchestration/weapon-library-import-orchestration-plan-2026-05-22.md` — operational plan for knight-rider
- `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` — greenfield SQLite DB (empty as of 2026-05-22 evening)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #1 (math-before-code applies to gear-affix stat math); Discipline #19 (background imports; no babysit)

---

## 10. Closing — what HEAVY commits to

The LITE→HEAVY rename is more than naming. It commits the engine to:

1. **Gear is real mechanical substrate v1.** Not a derived classification post-hoc; not a cosmetic tag; not a deferred concern. Mechanical effects on stats, sim outcomes, and cohesion-judging.

2. **The substrate is the vast library, not the 15 entries.** Substrate-as-cohesion requires substrate that the engine queries against; the library is that substrate. The 15 entries become predictions about emergent clusters, not the substrate itself.

3. **The catalogue is open, not closed.** Knowledge entries grow as crawls deepen + Meshy gap-fill fires. The engine's gear vocabulary grows with the catalogue, not against a fixed enumeration.

4. **v1.1+ promotion path is clear.** G-PROMOTE-v1.1 (full generative emergence at BC-axis layer) is the next promotion. It is not "the first commitment to gear as substrate" — that commitment is v1 HEAVY. v1.1+ deepens the substrate-as-cohesion architecture to the gear layer's full generative emergence.

5. **The cultural-lineage scope is honest.** v1 ships medieval-spanning per Variant C lock; sci-fi and post-singularity are explicit v1.1+ deferrals. The catalogue's Eurocentric bias is real and acknowledged; the vast-library substrate gives the engine the data shape to expand non-European cultural lineages as those entries grow.

The substrate-as-cohesion architecture is realer with HEAVY than with LITE. The patterns audited tonight (Patterns 4-5-6) are operationalized through this doc + the orchestration plan + Phase 1-Phase 5 import + clustering + axis-discovery work. The road continues.

---

**Signed:** gandalf (story-and-design steward; senior designer)
**Authority:** Matt 2026-05-22 evening — LITE→HEAVY rename + vast-library substrate pivot + 15-catalogue retirement + tier hierarchy one-v1 + baked-by-default + WR-bracket-under-gear sequencing all canonical
**For:** canonical lock of gear-substrate as real mechanical substrate v1; vast-library substrate architecture; tier hierarchy depth 1 v1; baked armor v1 with decoupling-flag exposure; Option (c) convergence sequencing v1, Option (a) preferred v1.1+; 15-entry catalogue demoted to clustering hypothesis; Phase D Meshy gap-fill canonical pipeline; explicit v1 vs v1.1+ scope draw.
