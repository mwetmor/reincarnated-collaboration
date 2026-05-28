# Path (III) — Faction-Assembly Extension (G-B + F-C) — Cycle 14 Scope Micro-Expansion

> **STATUS:** CURRENT (load-bearing as of 2026-05-27 evening) — Matt 2026-05-27 verbatim "Let's go with option (III)" ratifies addition of G-B (Algorithmic primary-pair selection) + F-C (Phase 5 LLM-derived inter-faction relationships) to Cycle 14 scope. Composes with Matt-gate-ratified Phase 4+5 + Option α math notes; amends Dispatch 3B (PM-2 implementation) + Wave 3 (Phase 5 cohesion-judge LLM) scopes before they fire.

**Date:** 2026-05-27 evening
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-27 verbatim "Let's go with option (III)" + prior Path (1) + Path A revert + no-classes recommitment ratifications
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-kr-amendment-kicker.md` (KR routing for in-flight dispatch amendment)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` (Path 1 recognition record; Path III is micro-extension)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 0.1 amendment-pass-record (Path III entry queued)
- PM-2 math note (engine `90092d6`; D-Hybrid + D-Separate + D-Sharpened — Path III adds § X.7 primary-pair selection)
- SC-3 cohesion-judge LLM architecture research (Pattern B PRIMARY)

---

## 0. TL;DR

Path (III) adds two automatic faction-assembly mechanisms to Cycle 14 scope:

**G-B — Algorithmic primary-pair selection** (~2-3 days impl; folds into PM-2 amendment § X.7):
- Per season: compute pairwise substrate-cluster-distance across PM-1 emergent clusters (k∈{3,4})
- Select highest-distance pair as `primary_faction_pair` metadata
- Surfaces to drax loadout (player sees primary narrative tension) + star-lord telemetry (analytics tracking)
- Composes with PM-1 GMM k∈{3,4} output; algorithm operates on PM-2 cluster centroids
- Discipline #46 compliance: O(k²) at k∈{3,4} = max 12 pairwise distance computations per season; trivial

**F-C — Phase 5 LLM-derived inter-faction relationships** (~1 week impl; folds into Wave 3 dispatch):
- Per season: per unordered faction-pair (k=3 → 3 pairs; k=4 → 6 pairs), Phase 5 LLM produces inter-faction relationship narrative
- LLM output (structured): relationship_type enum + tension_narrative (1-2 sentences) + shared_history_hook (optional)
- 3-6 additional LLM calls per season; ~$0.15-$0.30 added token cost (within SC-3 envelope)
- Composes with PM-2 D-Separate (one call per cluster) + SC-3 Pattern B PRIMARY recommendation
- D7 AI-tell discipline: structured output; LLM fills constrained blanks; not raw dialogue

**Net Cycle 14 timeline impact:** +1-2 weeks under quality > timeline (Q10). Total estimated: ~11-17 weeks (was ~10-15).

---

## 1. Authority + design intent context

### 1.1 Matt-ratification chain

- Path (1) Cycle 14 scope expansion ratified 2026-05-27 ("I confirm Path (1) + Discipline #46 + the operational moves above")
- 5 in-advance design calls pre-ratified 2026-05-27 evening (A2 + B1 + C2 + D-Sharpened + E-Dev-Phase-Aware Trigger B)
- Phase 4+5 + Option α math-note Matt-gate RATIFIED 2026-05-27 evening (Package A + Package B both)
- **Path (III) faction-assembly extension ratified 2026-05-27 evening** (Matt verbatim "Let's go with option (III)")

### 1.2 Why Path (III) over Path (II) or Path (I)

Per gandalf options surface to Matt 2026-05-27 evening:
- **Path (I)** — ship Cycle 14 as-ratified (PM-1 + PM-2 + Math Note 5 only); factions are isolated identities
- **Path (II)** — add G-B only; factions have primary-pair narrative tension via algorithmic selection
- **Path (III)** — add G-B + F-C; factions have primary-pair narrative tension AND LLM-narrated inter-faction relationships

Matt chose Path (III). Composes with earlier faction-pair-season design intent (Matt thought experiment); enables player-facing faction narrative beyond identity-level.

### 1.3 Composition with no-classes architectural recommitment

Path (III) honors no-classes recommitment:
- Primary-pair selection (G-B) operates on EMERGENT clusters (PM-1 output); no pre-authored faction taxonomy
- Inter-faction relationships (F-C) emerge from LLM analyzing emergent cluster pairs; no pre-authored relationship taxonomy
- Faction labels remain post-hoc cluster identities (Discipline #41 preserved)
- Substrate-led discipline preserved at cross-faction relationship layer (same as at per-kit + per-cluster layers)

---

## 2. G-B — Algorithmic Primary-Pair Selection (math spec)

### 2.1 Problem statement

PM-1 emerges k∈{3,4} clusters per season (GMM-BIC selected). Of these, ONE pair functions as the season's central narrative tension. Without explicit selection, all faction relationships are equal-weight — player can't anchor narrative on a specific antagonism.

**This spec:** algorithmic primary-pair selection from PM-1 emergent clusters. NOT pre-authored. NOT designer-curated. Substrate-distance vote.

### 2.2 Algorithm

Given PM-1 clusters {C_1, ..., C_k} per season with cluster centroids in BC-axis space:

```
For each unordered pair (C_i, C_j) where i < j:
    pairwise_distance(C_i, C_j) = mahalanobis_distance(
        centroid_i, centroid_j,
        pooled_covariance(C_i, C_j)
    )

primary_faction_pair = argmax_{(C_i, C_j)} pairwise_distance(C_i, C_j)
```

**Why Mahalanobis distance** (not Euclidean):
- Mahalanobis accounts for cluster spread variance; faction-pair separation should reflect cluster geometry, not raw axis distance
- Already implemented in MG-3 (math note); reuse infrastructure
- Per-cell-bounding per Discipline #46 § 7 not a concern at k∈{3,4} (12 pairwise ops max)

### 2.3 Tie-breaking (when distances are close)

If max_pair pairwise_distance is within 5% of second-max pair, secondary tie-break order:

1. **Lineage diversity difference** — pair where C_i and C_j have most-different `cultural_lineage_canonical` modal votes wins
2. **Named-template anchor count difference** — pair with most-different named-template anchor profiles wins
3. **proxy_geometry_class divergence** — pair with most-orthogonal damage geometries wins (mechanical narrative distinctness)

Tie-breaks are deterministic; substrate-led; reproducible at smoke-test scale.

### 2.4 Output metadata

Engine emits per season:

```json
{
  "primary_faction_pair": {
    "faction_a_cluster_id": <integer>,
    "faction_b_cluster_id": <integer>,
    "pairwise_distance": <float>,
    "selection_rationale": "highest_substrate_distance" | "lineage_diversity_tiebreak" | "named_anchor_tiebreak" | "geometry_divergence_tiebreak"
  },
  "background_faction_pairs": [
    {"faction_a_cluster_id": ..., "faction_b_cluster_id": ..., "pairwise_distance": ...}
    // remaining (k choose 2) - 1 pairs
  ]
}
```

`primary_faction_pair` is the season's central narrative tension. `background_faction_pairs` are secondary relationships (used by F-C for full inter-faction relationship matrix).

### 2.5 Cross-seam consumption

- **drax loadout summary:** "This season's central tension: Crimson Reaver Court ⚔ Iron Hierophant" — visible in player-facing UI
- **star-lord telemetry:** tracks primary-pair selection per season; analytics dashboard surfaces pairwise distance distributions across seasons; identifies whether substrate consistently produces high-distance pairs OR all pairs are close
- **Wave 3 cohesion-judge LLM (F-C):** primary-pair metadata informs LLM prompt weighting — primary-pair relationship gets richer narrative treatment than background pairs

### 2.6 Composition with PM-2 D-Sharpened

G-B operates AT THE CLUSTER LEVEL; D-Sharpened operates AT THE PER-KIT (and per-cluster) NAMING LEVEL. They compose orthogonally:
- D-Sharpened: substrate-anchor metadata hidden engine-layer; LLM uniform player-facing names
- G-B: primary-pair metadata visible to player as "central tension"; not a naming concern

No conflict; no interaction at the naming layer. G-B adds NEW metadata field; D-Sharpened semantics unchanged.

### 2.7 PM-2 amendment scope

Add § X.7 to PM-2 (`src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md`):

> **§ X.7 — Primary-Pair Selection Algorithm (G-B; Path III addition)**
>
> Per `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` § 2. Algorithm operates AFTER PM-2 cluster naming completes; consumes cluster centroids; produces primary_faction_pair + background_faction_pairs metadata. Algorithm specified at § 2.2 of Path III spec. Discipline #46 § 7 compliance verified (k² at k∈{3,4} = max 12 ops). Tie-breaks at § 2.3. Output schema at § 2.4. Cross-seam consumption at § 2.5.

PM-2 amendment is ~50 lines; gandalf authoring or sub-agent gandalf via dispatch.

---

## 3. F-C — Phase 5 LLM-Derived Inter-Faction Relationships (LLM spec)

### 3.1 Problem statement

Per-season factions have identities (PM-2 names) and primary-pair structure (G-B) but no narrated RELATIONSHIPS between them. Player sees "Crimson Reaver Court" + "Iron Hierophant" + "Verdant Watcher" but doesn't know whether these factions are at war, allied, neutral, or have shared history.

**This spec:** LLM-derived inter-faction relationship generation. Composes with PM-2 D-Separate (per-cluster LLM call) + SC-3 Pattern B PRIMARY recommendation.

### 3.2 LLM call architecture

**Per faction-pair, one Pattern B structured-output LLM call:**

```
For each unordered pair (C_i, C_j) in season's emergent clusters:
    structured_output = llm_call_pattern_b(
        faction_a=faction_descriptor(C_i),  // name, substrate context, capstone themes
        faction_b=faction_descriptor(C_j),
        season_context=season_substrate_context,
        primary_pair_flag=(pair == primary_faction_pair),
        thematic_registry=element_thematic_registry  // per SC-3 § Recommendation 1
    )
```

### 3.3 LLM output schema (structured JSON)

```json
{
  "relationship_type": "enemies" | "rivals" | "uneasy_allies" | "allied" | "neutral" | "mixed_factions",
  "tension_narrative": "<1-2 sentences describing the inter-faction tension>",
  "shared_history_hook": "<optional 1 sentence reference to shared mythological / cultural / mechanical origin>" | null,
  "primary_pair_intensifier": "<additional 1-2 sentences if primary_pair_flag=true; null otherwise>",
  "ai_tell_compliance_score": <0.0 - 1.0; LLM self-assesses per D7 discipline>
}
```

### 3.4 LLM prompt template (sketch; refined at Wave 3 dispatch authoring)

```
SYSTEM: You are the cohesion-judge for Reincarnated's Phase 5 LLM. Produce
structured inter-faction relationship narratives. Apply D7 AI-tell discipline:
templated structure; LLM fills narrow blanks; no raw dialogue.

INPUTS:
- Faction A descriptor: {name, substrate_anchor, capstone_themes, lineage_modal}
- Faction B descriptor: {name, substrate_anchor, capstone_themes, lineage_modal}
- Season substrate context: {element_distribution, cultural_lineage_distribution}
- primary_pair_flag: <boolean — is this the season's central narrative tension?>
- Thematic registry: {element-specific 20-30 terms per SC-3 Recommendation 1}

INSTRUCTIONS:
1. Analyze substrate distance + lineage difference between Faction A and B
2. Choose relationship_type from enum (enemies / rivals / uneasy_allies / allied / neutral / mixed_factions)
3. Produce tension_narrative grounded in substrate evidence (1-2 sentences)
4. Optional shared_history_hook if substrate suggests common origin
5. If primary_pair_flag=true, intensify narrative with primary_pair_intensifier
6. Self-assess ai_tell_compliance_score (0-1; should be ≥0.7 per D7)
```

### 3.5 Volume + cost projection

- Per season at k=3: 3 unordered pairs → 3 LLM calls
- Per season at k=4: 6 unordered pairs → 6 LLM calls
- Average: ~4-5 calls per season
- Token cost per call: ~3-5K tokens (Pattern B structured input + structured output)
- Cost per season: ~$0.15-$0.30 added (within SC-3 envelope; SC-3 baseline ~$0.50-$5/season)

### 3.6 D7 AI-tell discipline compliance

- Output is structured JSON, not free-form dialogue
- Tension narratives are 1-2 sentences (constrained)
- relationship_type is from enum (no freeform invention)
- Shared history hooks are 1 sentence reference (constrained)
- LLM self-assesses ai_tell_compliance_score; calls scoring <0.7 are regenerated with prompt amendments
- Gandalf design-quality audit at Wave 3 close (Discipline #43) verifies sample outputs against D7

### 3.7 Cross-seam consumption

- **drax loadout summary:** primary-pair narrative surfaced ("Crimson Reaver Court is at war with Iron Hierophant; bound by shared exile from the Eastern Sky"); background-pair relationships available on faction-detail pages
- **star-lord telemetry:** relationship_type distribution per season; primary-pair vs background-pair narrative quality scoring; ai_tell_compliance_score tracking
- **Wave 3 dispatch:** ExportFactionRelationship schema added to engine output JSON; consumed by drax via existing star-lord Track C transform

### 3.8 Composition with primary-pair (G-B)

G-B selects primary_faction_pair via substrate distance. F-C ingests this via primary_pair_flag; produces richer narrative for primary pair than background pairs. They compose:
- G-B answers "which pair is the season's central tension?"
- F-C answers "what is the nature of that tension + the other relationships?"

Together they produce faction-pair-season narrative output that composes with player's earlier faction-pair-seasons design intent.

### 3.9 Wave 3 dispatch amendment scope

Wave 3 dispatch (Phase 5 cohesion-judge LLM architecture; KR to author) gets these additions:

1. Per-faction-pair LLM call architecture (this spec § 3.2-3.4)
2. ExportFactionRelationship JSON schema (this spec § 3.3)
3. Token cost projection update (~$0.15-$0.30 added per season)
4. D7 AI-tell compliance verification (this spec § 3.6)
5. Gandalf design-quality audit hook at Wave 3 close

Wave 3 dispatch is being authored by KR post-Matt-gate; Path (III) amendments fold in before fire.

---

## 4. Composition with already-ratified Cycle 14 work

| Already-ratified | Path (III) interaction |
|---|---|
| **PM-1 GMM k∈{3,4}** | G-B operates on PM-1 cluster output; F-C consumes PM-1 cluster definitions |
| **PM-2 D-Hybrid + D-Separate + D-Sharpened** | G-B is PM-2 § X.7 amendment; F-C composes per-pair LLM call with PM-2 per-cluster LLM calls (D-Separate extended to D-Separate-Plus-Pairs) |
| **MG-1 through MG-5** | No interaction — Phase 4 math gates operate per-kit; Path (III) operates per-cluster + per-pair |
| **Math Note 5 E2 cross-season persistence** | G-B + F-C run per season; cross-season faction relationships are Cycle 15+ scope (Court of Forms F-D Player-state derived option) |
| **D-Sharpened (substrate-anchor metadata)** | Orthogonal — D-Sharpened is per-kit naming layer; G-B + F-C are per-cluster + per-pair narrative layer |
| **E-Dev-Phase-Aware retention** | No interaction — reject pool doesn't include faction-pair relationship data |

---

## 5. Discipline composition

| Discipline | Path (III) application |
|---|---|
| **#1 (math-before-code)** | G-B + F-C math specs authored before Dispatch 3B + Wave 3 implementation |
| **#11 (empirical inspection)** | Pairwise distance distributions empirically validated post-Wave 5 |
| **#18 (math-hotspot routing)** | G-B is small math hotspot (Mahalanobis pairwise reuse from MG-3); F-C is LLM-call-volume hotspot (star-lord cost-projection consultation) |
| **#34 (concentration)** | Primary-pair selection concentrates narrative tension on ONE pair; background pairs less-elaborated; concentration discipline at narrative layer |
| **#40 (scaffold-with-pending-decision)** | F-C prompt template at sketch level (refined at Wave 3); flagged as scaffold-pending-Wave-3-refinement |
| **#41 (pre-authored taxonomy interrogation)** | relationship_type enum verified — emergent from cluster characteristics, NOT pre-authored faction taxonomy |
| **#42 (framing-audit at dispatch consumption)** | Sub-agents authoring Dispatch 3B + Wave 3 fire framing-audit; verify Path (III) scope compliant |
| **#43 (design-quality audit at wave-close)** | Wave 3 close audits faction-relationship sample outputs against D7 + substrate-led discipline |
| **#46 (DB anti-materialization)** | G-B O(k²) at k∈{3,4} = max 12 ops; F-C LLM call volume bounded; no DB queries against unbounded tables |
| **D7 (AI-tell line discipline)** | F-C output is structured JSON; templated narratives; constrained enums; ai_tell_compliance_score self-assessment |

11 disciplines compose into Path (III) execution. Substrate-led architectural commitment preserved.

---

## 6. Risks + Watch Items (additions to failure-modes register)

Add to `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-scope-creep-drift-register.md` § 1 (failure modes):

### F-8 — Primary-pair tie-break degeneracy

**Pattern:** when k=3 and all three pairwise distances are within 5%, tie-break logic may produce inconsistent primary-pair selection across smoke-test runs. Substrate close to uniform → no meaningful primary pair.

**Watch:** smoke-test G-B against substrate populations where pairwise distances cluster tightly; if tie-breaks fire >20% of seasons, algorithm needs refinement.

**Counter:** if tie-break fires too often, add a 4th tie-break (lineage-modal-name lexicographic order for determinism); OR widen tie-break tolerance to 10%; OR flag season as "balanced factions, no primary tension" and surface this honestly to drax UI.

### F-9 — LLM relationship narrative homogeneity

**Pattern:** F-C LLM produces 3-6 narratives per season; if LLM defaults to similar phrasings across pairs ("enemies bound by ancient grudge" × 6), player experiences faction relationships as samey + unconvincing.

**Watch:** Wave 3 dispatch acceptance criteria includes diversity-of-narrative smoke test — ai_tell_compliance_score + relationship_type distribution + tension_narrative semantic similarity (cosine distance via sentence embeddings; SC-3 already references local sentence-transformers).

**Counter:** if homogeneity detected, prompt template refined to require explicit substrate-context grounding per pair; LLM regenerates calls with high semantic similarity.

---

## 7. Sub-agent gandalf has finished — sequencing matters

Sub-agent gandalf transcription dispatches completed earlier this evening. KR is now authoring 4 dispatches in sequence post-Matt-gate (Wave 1.5 Stage 3 RE-AUTHORING → Dispatch 3A → Dispatch 3B → THEMATIC_REGISTRY).

**Path (III) amendments must land BEFORE Dispatch 3B + Wave 3 dispatch fire:**

1. KR receives this Path (III) spec + KR kicker
2. KR PAUSES Dispatch 3B + Wave 3 dispatch authoring (Wave 1.5 Stage 3 RE-AUTHORING + Dispatch 3A can fire if not already)
3. KR routes PM-2 § X.7 amendment authoring to gandalf (or this spec's § 2 serves as the amendment text — ~50 lines)
4. KR amends Dispatch 3B scope to include G-B + (G-B section of) F-C
5. KR amends Wave 3 dispatch scope to include F-C LLM call architecture
6. jack-ryan LIGHT re-Gate-1 verifies (math spec § 2 + LLM spec § 3 + token budget; ~half-day)
7. Dispatches fire with Path (III) scope integrated

---

## 8. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CURRENT — Path (III) faction-assembly extension ratified by Matt 2026-05-27 evening
**Authority:** Matt 2026-05-27 verbatim "Let's go with option (III)"
**Composition:** with Path (1) Cycle 14 scope expansion + no-classes recommitment + Phase 4+5 Matt-gate ratification + Option α Matt-gate ratification + Quality-Orientation Shift Five-Moves Package + Discipline #46

**For:** the ratified Cycle 14 scope micro-expansion adding G-B (Algorithmic primary-pair selection via Mahalanobis cluster-centroid distance) + F-C (Phase 5 LLM-derived inter-faction relationships via Pattern B structured calls) per `engine-as-general-serial-content-product-2026-05-22.md` § 2.2 canonical (faction-coalescence + pairing algorithm scope). Composes with PM-1 GMM k∈{3,4} clustering + PM-2 D-Hybrid + D-Separate + D-Sharpened naming; substrate-led discipline preserved at faction-pair narrative layer; D7 AI-tell discipline preserved via structured LLM output; Discipline #46 § 7 per-cell bounding preserved (k² at k∈{3,4} = trivial).

**Signed:** gandalf (story-and-design steward)
