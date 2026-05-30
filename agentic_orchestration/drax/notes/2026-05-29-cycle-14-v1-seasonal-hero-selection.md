# Cycle 14 v1 Seasonal Hero Selection — Drax + Galadriel Pair Notes

**Authored:** 2026-05-29
**Authority:** Matt 2026-05-29 Amendment 2 verbatim — "leave the seasonal hero call up to galadriel and drax"
**Pair:** drax (UX-fit + image-extraction feasibility) + galadriel (visual-coherence CV scoring)
**Season:** cycle-14-wave-5-season-001 (4 faction clusters; Wanderer pending gamora close)
**Decision mode:** Pair consensus (DEFAULT: per-cluster hero faction elected as season marquee)
**Deadlock escalation:** gandalf-sub-agent via KR (NOT Matt)

---

## 1. Data basis

Source: `agentic_orchestration/cycle-14-wave-5-season-001/phase5_faction_clusters.json`

**4 faction clusters:**
| Cluster | Name | Members | Modal lineage | Dominant element | BC signature |
|---|---|---|---|---|---|
| 1 | Grounded Chain Strikers | 13 | fantasy_generic | earth (38%) + lightning (31%) | ranged / chain |
| 2 | Stormbreak Vanguard | 11 | fantasy_generic | lightning (27%) + fire (27%) + wind (27%) | close / large-AOE |
| 3 | Stormveil Ironclad Surge | 9 | **european** | lightning (44%) + holy (22%) | close / large-AOE |
| 4 | Ashfield Siege Callers | **1** | fantasy_generic | fire (100%) | ranged / large-AOE |

**Note on substrate metadata richness:**
Individual kit substrate (cultural_lineage_canonical, weapon_type_family, historical_period_canonical, register_canonical) exists in the engine archive (kit_archive.db) but is NOT surfaced in phase5_faction_clusters.json. The faction-level `modal_*` fields carry aggregated substrate signals. For image-gen prompt construction (§ 12.2), the individual kit's substrate fields would need to be extracted from kit_archive.db for the elected candidate kit. This is an elrond-seam retrieval if needed.

**Wave B per-kit names:** NOT available. Wave B implementation was missing (cascade-resumption-2 finding). Kit IDs are engine-format only (e.g. `S1_endgame_bc_melee_high_flat_dex_none_s1`). No LLM-generated per-kit names exist yet. This constrains § 12.1 hero identification to the faction-level rather than individual-kit-level for this session.

---

## 2. Drax reads

### 2.1 UX-fit read per candidate faction

**Cluster 1 — Grounded Chain Strikers**
- UX-fit: GOOD. Ranged chain-propagation archetype slots cleanly into a Summary tile hero. 13 members = strong faction representation. Earth+lightning at range = defensible visual anchor.
- Limitation: `fantasy_generic` cultural lineage is the least specific substrate signal for image prompt — produces functional but genre-generic medieval ranger/mage imagery.
- UX-fit rating: 3/5

**Cluster 2 — Stormbreak Vanguard**
- UX-fit: GOOD. Close-quarters multi-element AOE archetype. 11 members = solid representation. Multi-element (3 elements at ~27% each) is tonally complex — the Summary tile would read "elemental convergence warband."
- Limitation: `fantasy_generic` lineage + 3-element spread = less visually focused hero image. The "Stormbreak" name is strong but the elemental spread makes a unified hero image harder to pin.
- UX-fit rating: 3/5

**Cluster 3 — Stormveil Ironclad Surge**
- UX-fit: EXCELLENT. `european` cultural lineage is the most specific and visually anchored substrate in the season. Lightning-dominant 44% + holy 22% = a knight/ironclad archetype with divine charge — this is a classic HD-2D hero archetype (think: armored warrior channeling storm+holy power). Close-engagement + large-AOE = dynamic combat posture for hero art. "Ironclad Surge" names are visually strong. 9 members = substantial faction.
- Image-extraction support: `european` + `medieval_or_early_modern` period + `lightning/holy` element = the most specific prompt-constructable substrate in the season. An image-gen prompt built on this substrate would yield: "European medieval ironclad warrior channeling storm lightning and holy radiance, close-engagement, wide-arc strike posture, hand-drawn pixel art HD-2D style reminiscent of Octopath Traveler / Triangle Strategy."
- This is the richest prompt substrate available from these 4 clusters.
- UX-fit rating: 5/5

**Cluster 4 — Ashfield Siege Callers**
- UX-fit: DISTINCTIVE but thin. Pure fire + ranged-AOE medieval siege caller is a visually strong archetype. However: this faction has ONLY 1 member (member_count=1). As season marquee hero, a singleton faction creates a narrative gap — the hero doesn't represent a "faction" in any meaningful sense; it's a faction of one.
- Image-extraction support: pure fire + `fantasy_generic` medieval = functional prompt but less substrate-specific than Cluster 3. Fire-mage/siege archetype is common genre imagery.
- The singleton status is a UX problem: the Summary tab would show a 1-kit "faction" as the season face, which undercuts the faction-emergence story.
- UX-fit rating: 2/5 (singleton undermines faction hero framing)

### 2.2 Image-extraction feasibility read

For § 12 (when it fires): the elected hero's substrate metadata must support a 12-image extraction package (1 hero + 11 gear slots). The faction-level modal substrate provides the direction; individual kit substrate from kit_archive.db would supply the detailed prompt fields.

**Cluster 3 substrate feasibility:** HIGHEST. `european` lineage + `lightning/holy` elements + close-engagement BC signature → the most coherent 11-gear-slot composition story:
- Helm: european ironclad visor with lightning-charge rune
- Chestplate: heavy european plate with holy-storm inscription
- Gauntlets: ironclad fists with lightning-arc charge
- Greaves: European war-plate, heavy-movement stance
- Weapon (martial-heavy modal for this cluster): two-handed or war-sword with storm-arcing blade
- Secondary (if applicable): holy focus or shield with radiance ward
- Remaining slots: accessories themed to storm/holy convergence

The european + ironclad + storm/holy combination is THE most compositionally coherent kit for 11-slot extraction in this season.

**Cluster 1 feasibility:** functional. Earth+lightning ranged medieval = bow or crossbow with earth-chain rune. Completable but less visually cohesive.

**Cluster 2 feasibility:** HARDER. 3-element spread means gear slots would fragment across fire/lightning/wind theming without a clear visual unifier. The extraction would feel compositionally scattered.

**Cluster 4 feasibility:** Fire-pure + siege = actually decent for gear composition (all fire-themed siege implements), but singleton status undermines the faction-hero selection logic.

### 2.3 Implementation pragmatism ranking

Ranked by substrate-metadata richness for ChatGPT API image-gen prompt construction:

1. **Cluster 3 — Stormveil Ironclad Surge** — european + lightning/holy + close-AOE = richest, most specific substrate. Highest prompt fidelity expected.
2. **Cluster 1 — Grounded Chain Strikers** — fantasy_generic medieval ranged earth/lightning = functional, genre-legible prompt.
3. **Cluster 4 — Ashfield Siege Callers** — fire-pure siege = clean fire-mage prompt, but singleton faction problem.
4. **Cluster 2 — Stormbreak Vanguard** — multi-element spread = hardest to produce a focused image-gen prompt from.

### 2.4 Drax election recommendation

**ELECT: Cluster 3 — Stormveil Ironclad Surge**

Reasoning:
1. `european` cultural lineage is the strongest, most visually specific substrate in the season — vs `fantasy_generic` for the other three factions. This matters for prompt quality.
2. Lightning-dominant + holy traces = armored divine-storm knight archetype — maximally legible in HD-2D pixel register. Genre-appropriate for isekai medieval ARPG aesthetic.
3. 9 members — substantial faction; not singleton; represents a real cohort of the season's kit pool.
4. Close-engagement + large-AOE posture = dynamic hero image composition (striker mid-charge, wide arc).
5. "Ironclad Surge" naming carries visual specificity that will translate into a strong hero image prompt.
6. 11-slot gear extraction would be compositionally coherent: european plate + storm-rune + holy radiance = complete thematic kit.

---

## 3. Galadriel reads

**Galadriel returned 2026-05-29.** Full reads at:
- Backing report: `agentic_orchestration/galadriel/notes/2026-05-29-cycle-14-v1-cv-pipeline-scoring-cluster-visual-coherence.md`
- Contribution file: `agentic_orchestration/galadriel/notes/2026-05-29-cycle-14-v1-seasonal-hero-selection-galadriel-contribution.md`

### 3.1 Mirror's first plain word — what the picture could and could not show

The dispatch framed CV-pipeline scoring against genre-peer marquee references (Octopath / Triangle Strategy / Eastward / CrossCode per `canonical/story/style-register.md`). **Three plain-sight gaps shape what galadriel could deliver:**

1. **No genre-peer benchmark image set exists** — the curated reference-images set at `agentic_orchestration/galadriel/reference-images/` is the 7-frame DoE mobile-ARPG cluster reference (locked for a *different* benchmark question — mobile-feel — not for HD-2D style-register adherence). Genre-peer benchmark set has not been curated, sourced, or manifest-rowed. **Surfaced to KR as infrastructure gap; acquisition plan documented; awaits KR authorization for next-session execution.**
2. **No candidate-kit imagery exists** — § 12.2-12.4 image-gen blocks on § 12.1 selection; no rendered visual to apply CV pipeline to. CV-pipeline-image-scoring is therefore architecturally downstream of THIS pair-consensus decision.
3. **Wave B per-kit names not persisted** (drax also surfaced this in § 1) — only count + cost recorded; per-kit identity-narrative-level reads await rocket/star-lord follow-on.

**Therefore: substrate-level visual-coherence reads are the only evidence-defensible scoring instrument at this moment.** Phase-2 CV-pipeline-image-scoring methodology spec is drafted ready-to-fire in the backing report once both gaps close.

### 3.2 Substrate visual-coherence rubric (galadriel v1; 6 axes, 1-5 scoring; per-axis evidence-cite; honesty floor)

| Axis | What it measures |
|---|---|
| A1. Lineage-period coherence | Modal cultural lineage + tech-level present as singular visual-tradition? |
| A2. Element-distribution coherence | Top-3 element distribution present as thematically-readable identity? |
| A3. BC-axis-geometry coherence | Modal engagement-profile + damage-geometry read as coherent fighting-style? |
| A4. Faction-narrative coherence | Wave A `faction_identity_narrative` derivable from substrate without LLM-fiat? |
| A5. HD-2D pixel-art renderability | Does substrate compose into the Octopath / Triangle Strategy HD-2D register? |
| A6. Cluster-cohesion strength | `cosine_similarity_max` against noise floor and sibling-cluster rank? |

### 3.3 Galadriel per-cluster scoring

| Cluster | A1 lineage | A2 element | A3 BC | A4 narrative | A5 HD-2D render | A6 cohesion | Substrate mean | Galadriel rank |
|---|---|---|---|---|---|---|---|---|
| 1 — Grounded Chain Strikers | 4 | 4 | 5 | 5 | 4 | 3 | **4.17** | 2nd cluster-membered |
| 2 — Stormbreak Vanguard | 4 | 3 | 5 | 4 | 3 | 4 | **3.83** | 3rd cluster-membered |
| **3 — Stormveil Ironclad Surge** | **5** | **5** | **5** | **5** | **5** | 4 | **4.83** | **1st cluster-membered** |
| 4 — Ashfield Siege Callers | 4 | 5 | 4 | 5 | 5 | N/A singleton | **4.60** (substrate-axes only) | Wanderer-alternative |

### 3.4 Galadriel-side per-cluster reads (compressed)

- **Cluster 1 — Grounded Chain Strikers:** lineage + BC + element + narrative coherent (mean 4.17); HD-2D renderable; weakest cohesion (cosine_max 0.34); reads as **a school, not an individual** — hero render would be "exemplar of the chain-striker tradition" rather than "the chain-striker."
- **Cluster 2 — Stormbreak Vanguard:** strong tactical identity (close-AOE) but **multi-element-no-primary** (3 elements at 27% each); creates render-choice burden at prompt-construction time — substrate doesn't pre-commit which element wears the colors. Mean 3.83.
- **Cluster 3 — Stormveil Ironclad Surge:** **cleanest substrate visual identity in the season.** Only cluster with substrate-anchored named lineage (`european` — not `fantasy_generic` placeholder). Lightning 44% primary anchors visual identity; holy+shadow compose as secondary palette without contesting. **HD-2D-genre-canonical** (Triangle Strategy Holy Empire / Octopath Cleric+Warrior / Live A Live medieval / FF Tactics Holy Knight). Five 5s on six axes. Mean 4.83.
- **Cluster 4 — Ashfield Siege Callers:** **Wanderer candidate per Amendment 1.** Strongest mono-element identity in the season (fire 100%); zero element-dissonance possible at render. Mean 4.60 on substrate axes; cohesion N/A for singleton. Substrate-honest "Lone Wanderer of Ashfield" framing; isekai-canon-thematic; highest LLM-image-gen consistency prior.

### 3.5 Galadriel election

**DEFAULT VOTE: Cluster 3 — Stormveil Ironclad Surge** (substrate mean 4.83; HD-2D-genre-canonical; lineage-specific; cleanest singular-hero substrate visual coherence)

**ALTERNATIVE VOTE: Cluster 4 / Ashfield Wanderer** (substrate mean 4.60; substrate-elected singleton per Amendment 1; isekai-canon-thematic Lone-Wanderer pattern)

---

## 4. Pair consensus state — CONVERGENT ON CLUSTER 3

**Drax recommendation:** Cluster 3 — Stormveil Ironclad Surge (UX-fit 5/5; image-extraction feasibility HIGHEST; pragmatism rank 1st)

**Galadriel recommendation:** Cluster 3 — Stormveil Ironclad Surge (substrate visual-coherence 4.83/5; HD-2D-genre-canonical; lineage-specific)

**Consensus status:** ✅ **CONVERGENT — PAIR ELECTS CLUSTER 3 (STORMVEIL IRONCLAD SURGE) AS THE SEASON 001 MARQUEE HERO.**

### 4.1 Triangulation summary

Pair independently converged on Cluster 3 via different evidence layers:

| Evidence layer | Drax instrument | Galadriel instrument | Cluster 3 result |
|---|---|---|---|
| Substrate specificity | UX-fit 5/5 (european lineage; lightning+holy element clarity) | Substrate visual-coherence A1=5 + A2=5 (only cluster with substrate-anchored named lineage; lightning 44% primary anchors visual identity) | CONVERGENT — substrate-richest of the four |
| Image-gen prompt construction | Image-extraction feasibility HIGHEST (compositionally coherent 11-slot gear story) | HD-2D pixel-art renderability A5=5 (Triangle Strategy Holy Empire / Octopath Cleric+Warrior direct neighbors; legolas catalogue research confirms strong asset-library prior) | CONVERGENT — strongest LLM-image-gen prior |
| Faction-cohort representation | 9 members (substantial; not singleton) | A6 cohesion = 4 (tied with cluster 2 for highest; meaningful internal cohesion at n=9) | CONVERGENT — substantial faction; not singleton |
| Genre-positioning fit | HD-2D pixel register honored at UI chrome level | HD-2D-genre-canonical via european-medieval lightning-paladin-with-shadow-undertones | CONVERGENT — genre-correct |
| Narrative coherence | "Ironclad Surge" naming carries visual specificity | A4 narrative coherence = 5 (every claim derivable from substrate; thematic tags triangulate clean) | CONVERGENT — narrative substrate-derived |

**Galadriel's veto threshold (per § 12.1 contribution file):** "if drax votes Cluster 1 or 2 over both Cluster 3 AND Ashfield Wanderer without concrete UX-fit/extraction blockers, galadriel would escalate to gandalf-sub-agent." **Drax did NOT vote Cluster 1 or 2 — drax voted Cluster 3. No deadlock; no gandalf-sub-agent escalation needed.**

**Drax's deadlock procedure note:** "If galadriel returns a different recommendation with conflicting CV evidence, pair cannot resolve internally → KR routes to gandalf-sub-agent." **Galadriel did NOT return conflicting CV evidence — galadriel returned converging substrate visual-coherence evidence. No deadlock; no gandalf-sub-agent escalation needed.**

### 4.2 Final election

**Pair-elected season_001 marquee hero: Cluster 3 — Stormveil Ironclad Surge.**

**Substrate basis for § 12.2 prompt construction (drax-authored summary cross-confirmed by galadriel):**
- Cultural lineage: **european**
- Period: **medieval** (drax noted `medieval_or_early_modern` accessible from kit_archive.db)
- Dominant element primary: **lightning (44%)**
- Element secondary palette: **holy (22%) + shadow (11%)**
- BC engagement / geometry: **close / large-AOE**
- Style register: **hand-drawn pixel-art HD-2D-shaped (per canonical/story/style-register.md lock; Octopath / Triangle Strategy / Eastward / CrossCode primary references)**
- Faction-narrative anchor: **"close-quarters European medieval warband channeling dominant lightning alongside traces of holy radiance and shadow"** (Wave A canonical)
- HD-2D-genre-canonical archetype: **lightning-paladin-with-shadow-undertones; Triangle Strategy Holy Empire / Octopath Cleric+Warrior / Live A Live medieval / FF Tactics Holy Knight neighbor**

### 4.3 Wanderer alternative — NOT ELECTED but flagged for cross-season pattern

The Ashfield Wanderer (cluster 4 singleton) was galadriel's ALTERNATIVE vote and substrate-defensible (mean 4.60; mono-element fire; substrate-elected singleton per Amendment 1; isekai-canon-thematic Lone-Wanderer pattern). It was NOT elected because Cluster 3 outranked it on substrate visual-coherence (4.83 vs 4.60) AND drax's UX-fit + image-extraction reads converged on Cluster 3.

**Forward note (post-gamora Amendment 1):** when gamora ships Wanderer architecture and the SINGLETON state schema lands, the Ashfield Siege Caller singleton will be canonically renamed as "Lone Wanderer of Ashfield" (per Amendment 2 ALTERNATIVE framing). It may carry FUTURE season-marquee weight in a different season where no faction emerges as substrate-rich as Cluster 3 here. **The Wanderer-as-hero pattern is established as a substrate-honest hero pattern; it's just not the right call for THIS season because a substrate-richer cluster-membered faction emerged.**

### 4.4 Deadlock disposition

NONE. Pair-consensus convergent on Cluster 3. **No KR routing to gandalf-sub-agent; no Matt-surface.** Per CLAUDE.md addendum + hive-mind decision-routing directive Matt 2026-05-23: pair-decided in-scope.

---

## 5. Wanderer alternative (post-gamora)

The "Lone Wanderer of [Season Identity]" alternative is NOT assessable at this time. Gamora Amendment 1 Wanderer architecture is pending. No `cluster_id="SINGLETON"` data exists in phase5_faction_clusters.json for this season.

Post-gamora-close: galadriel and drax re-assess if a Wanderer candidate has stronger standalone identity than Cluster 3. If so, pair reconsiders. If pair maintains Cluster 3, election is confirmed.

Per dispatch ALTERNATIVE criteria: elect Wanderer-as-hero only if pair judges Wanderer standalone identity STRONGER than best faction candidate. Drax's current judgment is that Cluster 3 has the strongest substrate-to-image-gen pipeline support — this would need a compelling Wanderer identity to displace it.

---

## 6. § 12.2–12.4 status

DEFERRED. § 12.2–12.4 fire AFTER § 12.1 pair selection reaches consensus.

Once galadriel returns and pair confirms Cluster 3 (or alternative), the execution sequence is:
- § 12.2: drax generates seasonal hero image via ChatGPT API (substrate-metadata-informed prompt; legolas Track B prompt coordinates)
- § 12.3: drax extracts 11 isolated gear-piece images
- § 12.4: drax sends 12 images (1 hero + 11 gear) to Matt; Matt loads into Meshy → returns animation URL; drax wires into Summary tab

---

## 7. Notes on substrate metadata gap

The individual kit-level substrate fields (cultural_lineage_canonical, weapon_type_family, historical_period_canonical, register_canonical) are present in kit_archive.db but NOT in phase5_faction_clusters.json. The faction-level `modal_*` fields provide aggregated substrate signals sufficient for the § 12.1 hero selection, but for § 12.2 image-gen prompt construction, the specific elected kit's substrate fields should be retrieved from kit_archive.db.

If this data is not directly accessible, route to KR for elrond substrate retrieval. The `modal_cultural_lineage` = "european" and element distribution for Cluster 3 are sufficient for a working image-gen prompt, but per-kit weapon_type_family (currently showing martial-heavy + caster distributions in the aggregate) would sharpen the gear composition.

This is a note for the § 12.2 execution session; does NOT block § 12.1 hero selection.
