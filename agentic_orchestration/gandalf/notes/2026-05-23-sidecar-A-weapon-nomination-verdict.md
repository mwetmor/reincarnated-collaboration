# Sidecar A — Weapon Nomination Verdict (5 weapons for image-pass-through-vs-LLM-description Meshy comparison)

**From:** gandalf (story-and-design steward, sub-agent verdict)
**To:** knight-rider (Cycle 10 hive-mind orchestrator); star-lord (Sidecar A executor); jack-ryan (Gate-2)
**Date:** 2026-05-23
**Authority:** knight-rider dispatch — `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Sidecar A
**Anchor docs:**
- `canonical/00-ground-state.md` § 1 (current truth)
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` § 3.6 (hypothesis tested)
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` § 4.3 criterion 3.3 + § 7 (D7 AI-tell)
- `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Sidecar A

---

## 1. Top-line nomination

| # | entry_id | canonical_name | source_library | cluster_id | weapon_form | register |
|---|---|---|---|---|---|---|
| 1 | **196274** | Claymore (Scottish hilt / German blade, 16-17th C) | met-museum | (unclustered / museum-curated) | melee — two-handed greatsword | historical |
| 2 | **167849** | Halberd of Archduke Ferdinand II of Austria (1578-1637) | met-museum | (unclustered) | polearm — halberd | historical (named-bearer) |
| 3 | **193565** | Crossbow (Halbe Rüstung) with Cranequin Winder (German, prob. Dresden) | met-museum | 97 | ranged — crossbow w/ mechanical winder | historical |
| 4 | **184683** | Barrett M82 (M107) American Semi-Automatic Anti-Material Rifle | odin-army-tradoc | 70 | firearm — modern rifle | military_modern |
| 5 | **181416** | Yellow Quartz Longsword (Dark Souls II) | fextralife-ds2 | 19 | melee — fantasy longsword | fantasy |

---

## 2. Per-weapon rationale

### #196274 — Claymore (Met Museum, two-handed greatsword)
**Why:** Iconic two-handed sword form; cross-cultural object (Scottish hilt + German Solingen blade) tests lineage attribution. Met Museum reference image is studio photograph against neutral background — Path 1 ideal-case input. Structured_properties carries dimensions (L. 53½ in.), weight (4 lb 9 oz), medium (steel, wood), accessionNumber. Description supports Path 2 prompt with cultural composition detail.
**Image state:** 5 reference images (5 angles), 1 canonical (`sfsb54.46.10(0325.08)s1d1.jpg`). Quality: museum studio.
**Variety dimension covered:** historical melee + Met Museum source + cross-cultural lineage stress case.

### #167849 — Halberd of Archduke Ferdinand II (Met Museum, polearm)
**Why:** Polearm form is structurally distinct from sword (long shaft + complex head with axe + spike + hook). Stress-tests rigging for shaft-attached weapons (separate handle/blade pivot relationships in Meshy output). Named-bearer attribution (Archduke Ferdinand II) is a Tier-S signal that Stage 1.5 will mine. Met Museum image quality + structured properties (dimensions 99½ in., 6 lb 1 oz, dated 1598) are ideal Path 1 + 2 inputs.
**Image state:** 2 reference images (duplicate canonical entries — `96.5.19_001june2014.jpg`). Quality: museum studio.
**Variety dimension covered:** polearm form + early-modern period + named-bearer Tier-S stress case.

### #193565 — Crossbow with Cranequin Winder (Met Museum, ranged)
**Why:** Ranged weapon with mechanical winder assembly (two-piece composite object: bow + cranequin tool). Worst-case Meshy stress test — does Path 1 correctly produce a single articulated mesh, or fragment into multiple objects? Path 2 ChatGPT-gen will likely produce a cleaner single-object image; comparison directly probes asset-pipeline § 3.6 hypothesis for compound objects. 9 reference images give Path 1 abundant angle coverage. Structured_properties enumerate medium (steel/wood/staghorn/copper alloy/hemp/leather/silk/gold/iron alloy/wool) — multi-material complexity will tax Meshy texture generation.
**Image state:** 9 reference images (DP295989 canonical + 8 additional angles). Quality: museum studio multi-angle.
**Variety dimension covered:** ranged form + compound-object stress case + multi-image abundance test.

### #184683 — Barrett M82 (Odin Army Tradoc, firearm)
**Why:** Firearm form (covers the optional ≥1 firearm criterion). Modern military-industrial reference photographs — different photographic quality regime than museum studio (operational/manufacturer photos with variable lighting + backgrounds). Tests whether Path 1 robustness degrades on non-studio reference images. 4000-character description with deep technical structured properties (Variants, System.Alternate, etc.) — Path 2 prompt has rich input. Cluster 70 (European Contemporary Assault-Rifle Pool) is one of the highest image-coverage clusters (64/77 = 83%) — strong canonical-cluster representative.
**Image state:** 3 reference images (one canonical `82_(C)a288.jpg`). Quality: operational/manufacturer photography (NOT studio).
**Variety dimension covered:** firearm form + military_modern register + non-studio reference-photo stress case + Odin source.

### #181416 — Yellow Quartz Longsword (Dark Souls II, fantasy)
**Why:** Soulslike game-data source provides a rendered-3D-asset reference image (NOT a photograph). Critical stress case — does Path 1 work when input is already a stylized game render rather than physical-object photograph? Tests whether Meshy can preserve fantasy-stylization (crystalline blade glow, exotic geometry) vs. degrading to generic-sword reconstruction. Path 2 (ChatGPT-gen from structured description) bypasses the stylized-render input and may produce a more generic result — direct hypothesis test on whether substrate-resident fantasy images are usable for Meshy direct-pass-through. Cluster 19 (Fantasy-Generic Fictional Longsword Named-Item Family) representative.
**Image state:** 1 reference image (`Yellow%20Quartz%20Longsword.png` — fextralife-wiki-render canonical). Quality: stylized game-asset render.
**Variety dimension covered:** fantasy register + Soulslike source + stylized-render-vs-photograph stress case.

---

## 3. Variety coverage matrix

| Dimension | Coverage | Notes |
|---|---|---|
| **Source library** | Met Museum (3) + Odin Army Tradoc (1) + fextralife-ds2 (1) | 3 sources; Met Museum dominance justified by being the richest provenance source (~870 char structured_properties avg on candidates). Royal Armouries considered + rejected: thinner structured_properties (~350 char) than Met Museum's ~870; would dilute Path 2 prompt quality. D&D source rejected: no high-resolution per-entry reference image typical in TRPG data dumps. |
| **Weapon form** | melee × 2 (greatsword + fantasy longsword) + polearm × 1 + ranged × 1 + firearm × 1 | 4 distinct forms; melee duplicated by register split (historical Claymore vs. fantasy Yellow Quartz Longsword — intentional, tests rendering regime delta on same form). |
| **Register** | historical × 3 + military_modern × 1 + fantasy × 1 | Spans the 3 dominant populated registers per substrate-conclusion-declaration. Mythological register intentionally absent (no Tier-S mythological-corpus matching at this dispatch stage; deferred to Stage 2.5+). Sci-fi absent per Recognition 4 v1.1+ deferral. |
| **Period** | early_modern × 2 + industrial-ish + contemporary × 1 + fictional × 1 | Spans pre-modern → modern → fictional. |
| **Image regime** | museum studio × 3 + operational/manufacturer × 1 + game-render × 1 | 3 regimes — most diverse possible within 5-weapon budget. Critical for PASS/FAIL/MIXED verdict resolution per § 3.6 — if MIXED, per-regime guidance can be authored. |
| **Object complexity** | single-object × 3 (sword, halberd, rifle, fantasy sword) + compound-object × 1 (crossbow + cranequin) | Compound-object stress case present. |

**Variety gaps explicitly accepted:** No South Asian / East Asian / African / Middle Eastern lineage representation. No mythological register. Justification: this is a 5-weapon Sidecar pipeline test, not a substrate-coverage exercise. Sidecar A produces a per-regime PASS/FAIL/MIXED verdict that locks production default for ~91.5% of substrate (per dispatch implication); lineage diversity is downstream substrate-curation territory (Stages 1-4), not Sidecar A's question.

---

## 4. D7 AI-tell discipline note — ChatGPT image-gen prompt template (Path 2, INTERNAL test artifact)

Per dispatch § Sidecar A method notes: prompt is INTERNAL test artifact, not player-facing. D7 prohibition on raw-LLM player-facing surfaces does NOT directly apply; however cohesion-grade construction is required so Path 2 produces a comparable input for Meshy.

**Template (gandalf-authored, for star-lord to instantiate per weapon):**

```
Generate a single high-resolution photograph of {canonical_name}.

WEAPON SPEC:
- Cultural lineage: {culture from structured_properties.culture if present, else cultural_lineage_canonical}
- Period: {objectDate or historical_period_canonical}
- Materials: {medium from structured_properties}
- Dimensions: {dimensions from structured_properties}
- Form: {weapon_form descriptor}

VISUAL CONSTRAINTS (locked for comparability with Path 1 museum/reference image input):
- Single weapon, full-view, side-profile orientation preferred (or 3/4 if mechanically complex)
- Neutral background (light grey to white), studio lighting
- Photograph realism — NOT illustration, NOT stylized rendering, NOT game art
- No human holding the weapon; weapon stands alone or rests on a surface
- Visible material textures (metal, wood, leather) at native quality
- No text overlays, no watermarks, no UI elements

EXCLUDE:
- Fantasy elaboration unless the weapon's register is fantasy
- Modern military elaboration unless register is military_modern
- Multiple weapons in frame
- Anachronistic context (e.g., medieval halberd in modern setting)

DESCRIPTION CONTEXT (for shape and detail accuracy, NOT for stylistic embellishment):
{first 500 chars of description_text}
```

**Per-weapon adjustments:**
- #181416 (Yellow Quartz Longsword, fantasy): visual constraint "photograph realism" relaxed to "high-quality detailed render in the style of dark fantasy concept art"; preserves stylization parity for the rendering-regime stress test
- #184683 (Barrett M82, military_modern): "photograph realism" preserved; "neutral background" relaxed if Odin operational-photo regime is being matched as the comparison reference

**Cohesion-judge gate before Meshy submission:** star-lord runs each Path 2 output through cohesion-judge cohesion-grade check (per existing P5 cohesion-judge infrastructure) before Meshy submission. Failed cohesion-grade → regen prompt with adjustments. Three regen failures → flag weapon as Path-2-incompatible, log to comparison artifact.

---

## 5. Risk flags

1. **#193565 Crossbow (compound object) is the highest-risk candidate.** Compound-object Meshy output may fragment into separate meshes (bow + winder). If Path 1 succeeds and Path 2 fails (or vice versa), this single weapon could MIX the verdict on its own. Recommend star-lord author per-weapon-PASS/FAIL detail in addition to overall verdict so this case is isolable.

2. **#181416 Yellow Quartz Longsword (stylized-render input) could produce a Path 1 failure NOT because direct-pass-through is bad but because the input image is a low-resolution wiki render (likely ~200-400px) vs. museum 2000+px studio shots.** If Path 1 fails here, attribute carefully — input quality, not pipeline. Star-lord should log image-resolution-per-input as a comparison metric, not just mesh-quality-output.

3. **#184683 Barrett M82 has 3 reference images of variable regime (operational photo + manufacturer side-shot + alt-angle).** Meshy may behave differently per-input — star-lord should test the canonical (`82_(C)a288.jpg`) primarily but optionally test a non-canonical to surface input-sensitivity.

4. **Met Museum dominance (3/5 candidates).** If Met Museum's photo regime produces ideal Path 1 results, the PASS verdict could over-generalize. Conversely, if it produces poor results, the FAIL verdict could under-attribute to non-museum sources. Star-lord should weight the verdict reasoning by source-regime, not just count successes.

5. **Discipline #25 semantic-layer rep-audit applied:** No candidate is from a high-purity cluster whose semantic label fights its content. Cluster 70 (European Contemporary Assault-Rifle Pool) label honestly describes Barrett M82. Cluster 97 (where crossbow + halberd sit) is "European-Tagged Early-Modern Halberd Pool (Mixed)" — crossbow#193565 IS a mixed-content member but its individual content matches museum-quality-standard. No marginal-lineage rep-audit failure mode triggered. SAFE.

6. **Framing-audit (Discipline #23) on nomination set:**
   - **Q1 — load-bearing assumptions:** assumes (a) reference image quality dominates Path 1 outcome more than weapon-form complexity; (b) structured_properties richness dominates Path 2 prompt quality; (c) variety on 3 regimes (museum / operational / game-render) is more informative than variety on 6 lineages.
   - **Q2 — what could refute:** if all 5 weapons produce identical Path-1/Path-2 deltas regardless of regime, assumption (c) is wrong and additional samples needed to surface regime-sensitivity. Star-lord should log per-regime delta explicitly so this is testable.
   - **Q3 — refine or execute as-framed:** EXECUTE AS-FRAMED. The 5-weapon budget is the dispatch constraint; refinement would over-engineer; if Sidecar A produces MIXED verdict, follow-up Sidecar A.2 can expand sample. Knight-rider routes follow-up if needed.

---

## 6. Sign-off

**Author:** gandalf (story-and-design steward, sub-agent verdict per hive-mind Cycle 10)
**Date:** 2026-05-23
**Authority:** knight-rider dispatch § Sidecar A — gandalf weapon nomination authority
**Anchor docs cited:**
- `canonical/00-ground-state.md` § 1
- `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` § 3.6
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` § 4.3 criterion 3.3 + § 7 (D7 AI-tell)
- `agentic_orchestration/gandalf/requests/2026-05-23-knight-rider-substrate-curation-multi-stage-dispatch.md` § Sidecar A
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` Disciplines #7, #23, #25

**Empirical basis:** Direct SQL inspection of `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` `weapon_knowledge_entries` (69,137 active rows) + `knowledge_entry_reference_images` JOIN; cluster centrality via Phase E-2 cluster_id; structured_properties richness measured by character-length proxy.

**Status:** READY FOR star-lord execution. jack-ryan Gate-2 review applies at comparison-artifact completion, not nomination stage.

**Signed:** gandalf
