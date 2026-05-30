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

*Pending galadriel parallel session. Galadriel provides:*
- *Visual-coherence read per candidate faction (CV-pipeline similarity scores against genre-peer marquee references)*
- *Per-faction image quality projection*
- *Hero recommendation with CV scoring*

**Status: AWAITING galadriel input.** Galadriel is firing in parallel under independent dispatch `2026-05-29-galadriel-cycle-14-cascade-r4-track-b-cv-scoring-plus-12-1-hero-pair-galadriel-half.md`.

---

## 4. Pair consensus state

**Drax recommendation:** Cluster 3 — Stormveil Ironclad Surge

**Galadriel recommendation:** PENDING

**Consensus status:** DRAX-SIDE COMPLETE — AWAITING GALADRIEL

**Deadlock procedure:** If galadriel returns a different recommendation with conflicting CV evidence, pair cannot resolve internally → KR routes to gandalf-sub-agent for design-fit adjudication per dispatch KR routing triggers.

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
