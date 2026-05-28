# Path (III) — Knight-Rider Amendment Kicker (URGENT — sequencing-sensitive)

> **STATUS:** CURRENT — orchestration signal for KR to PAUSE in-flight Dispatch 3B + Wave 3 dispatch authoring + integrate Path (III) faction-assembly extension scope BEFORE either fires.

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-27 evening
**Recipient:** knight-rider (URGENT — sequencing-sensitive)
**Authority:** Matt 2026-05-27 verbatim "Let's go with option (III)"
**Source:** `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` (full spec)

---

## 0. TL;DR

PAUSE Dispatch 3B + Wave 3 dispatch authoring. Integrate Path (III) scope additions:
- **G-B** (Algorithmic primary-pair selection; ~2-3 days impl; PM-2 § X.7 amendment) — folds into Dispatch 3B
- **F-C** (Phase 5 LLM inter-faction relationships; ~1 week impl; ExportFactionRelationship schema) — folds into Wave 3 dispatch

Wave 1.5 Stage 3 RE-AUTHORING + Dispatch 3A can fire if not already. Dispatch 3B + Wave 3 dispatch authoring resumes AFTER Path (III) integration.

---

## 1. What's still firing (no halt)

| Dispatch | KR can fire normally |
|---|---|
| Wave 1.5 Stage 3 RE-AUTHORING | ✅ Fire as planned (no Path III interaction) |
| Dispatch 3A (gamora Phase 4 impl) | ✅ Fire as planned (no Path III interaction) |
| Per-agent OP amendments (Move 2+3+5; 10 files) | ✅ Fire parallel as planned |

## 2. What pauses for amendment

| Dispatch | KR action | Path III addition |
|---|---|---|
| **Dispatch 3B** (gandalf+star-lord+rocket Phase 5 multimodal impl) | PAUSE authoring; integrate G-B scope | G-B primary-pair selection algorithm (PM-2 § X.7 amendment); Mahalanobis pairwise centroid distance over cluster set; selects primary_faction_pair metadata; ~2-3 days impl added |
| **Wave 3 dispatch** (Phase 5 cohesion-judge LLM) | PAUSE authoring; integrate F-C scope | F-C LLM call architecture (per-pair Pattern B structured calls); ExportFactionRelationship JSON schema; ~$0.15-$0.30 added per season token cost; D7 AI-tell compliance verification; ~1 week impl added |
| **THEMATIC_REGISTRY authoring dispatch** | Continue authoring | No Path III interaction; gates Wave 3 / Dispatch 3B |

## 3. PM-2 § X.7 amendment (G-B math spec)

Add to `src/reincarnated/generation/math/phase-5-pm-2-faction-label-assignment-math-2026-05-27.md` as new § X.7:

```markdown
## § X.7 — Primary-Pair Selection Algorithm (G-B; Path III addition)

> AMENDED 2026-05-27 evening per Matt Path (III) ratification (verbatim
> "Let's go with option (III)"). G-B algorithmic primary-pair selection from
> PM-1 emergent clusters. See `agentic_orchestration/gandalf/notes/
> 2026-05-27-path-iii-faction-assembly-extension.md` § 2 for full spec.

### X.7.1 Algorithm

Given PM-1 emergent clusters {C_1, ..., C_k} per season with cluster
centroids in BC-axis space:

For each unordered pair (C_i, C_j) where i < j:
    pairwise_distance(C_i, C_j) = mahalanobis_distance(
        centroid_i, centroid_j,
        pooled_covariance(C_i, C_j)
    )

primary_faction_pair = argmax_{(C_i, C_j)} pairwise_distance(C_i, C_j)

### X.7.2 Tie-breaking (within 5% of max)

1. Lineage diversity difference (most-different cultural_lineage modal vote)
2. Named-template anchor count difference
3. proxy_geometry_class divergence
4. (degenerate) lineage-modal-name lexicographic for determinism

### X.7.3 Output metadata schema

{
  "primary_faction_pair": {
    "faction_a_cluster_id": <integer>,
    "faction_b_cluster_id": <integer>,
    "pairwise_distance": <float>,
    "selection_rationale": "highest_substrate_distance" |
                           "lineage_diversity_tiebreak" |
                           "named_anchor_tiebreak" |
                           "geometry_divergence_tiebreak"
  },
  "background_faction_pairs": [...]
}

### X.7.4 Discipline #46 compliance

O(k²) at k∈{3,4} = max 12 pairwise distance ops per season. Trivial; no
per-cell bounding concern. Mahalanobis pooled-covariance reuses MG-3
infrastructure.

### X.7.5 Cross-seam consumption

- drax loadout: "primary tension: Faction A ⚔ Faction B" surfaced to player
- star-lord telemetry: pairwise distance distribution + selection_rationale
  tracking
- F-C Phase 5 LLM (Wave 3 dispatch): primary_pair_flag passed to per-pair
  LLM call for narrative intensification
```

KR can either author this amendment directly OR fire sub-agent gandalf for ~30-min targeted amendment. Either path; KR's call.

## 4. Dispatch 3B amendment scope

Add to Dispatch 3B scope (gandalf + star-lord + rocket Phase 5 multimodal implementation):

**New scope item — G-B Primary-Pair Selection (rocket primary; ~2-3 days impl):**
- Implement Mahalanobis pairwise distance over PM-1 cluster centroids
- Implement tie-break logic per PM-2 § X.7.2
- Emit primary_faction_pair + background_faction_pairs metadata per season
- Pass primary_pair_flag to F-C LLM call inputs (Wave 3 composition)
- Smoke-test: 10-season smoke; verify tie-break fires <20% of seasons; verify metadata schema integrity
- Gate-2: jack-ryan verifies G-B algorithm + Discipline #46 compliance + cross-seam JSON shape

**Acceptance criteria amendment:**
- Existing PM-2 D-Hybrid + D-Separate + D-Sharpened acceptance criteria preserved
- ADD: G-B primary_faction_pair selection produces valid metadata per acceptance schema; tie-break fires <20%; cross-seam JSON shape integration verified

## 5. Wave 3 dispatch amendment scope

Add to Wave 3 dispatch scope (Phase 5 cohesion-judge LLM architecture; gandalf primary + star-lord LLM integration):

**New scope item — F-C Inter-Faction LLM Relationship Generation (~1 week impl):**
- Per faction-pair per season (k=3 → 3 pairs; k=4 → 6 pairs), LLM Pattern B structured call
- LLM output: relationship_type enum + tension_narrative + shared_history_hook + primary_pair_intensifier + ai_tell_compliance_score
- ExportFactionRelationship JSON schema (rocket Phase 5 implementation)
- Token cost budget: ~$0.15-$0.30 added per season; within SC-3 envelope
- D7 AI-tell discipline compliance: structured output; templated; constrained enums; ai_tell_compliance_score ≥0.7 acceptance
- Diversity-of-narrative smoke-test: cosine distance between tension_narrative sentences must average <0.7 (per local sentence-transformers SC-3 reference)
- LLM prompt template authoring at Wave 3 dispatch authoring time (refined; sketch at Path III spec § 3.4)

**Acceptance criteria amendment:**
- Existing Wave 3 Phase 5 LLM acceptance criteria preserved
- ADD: F-C per-pair LLM call architecture implemented; ExportFactionRelationship schema in engine output JSON; token cost within budget; ai_tell_compliance_score average ≥0.7 across sample seasons; narrative diversity smoke-test PASS

## 6. jack-ryan LIGHT re-Gate-1 — does it fire?

YES — LIGHT re-Gate-1 verification recommended for Path (III) additions:
- PM-2 § X.7 amendment (G-B algorithm spec) — ~15-min review
- Wave 3 dispatch F-C scope addition (LLM prompt template + token budget + D7 compliance) — ~30-min review

**KR routes LIGHT re-Gate-1 as part of Dispatch 3B + Wave 3 dispatch authoring** (verification on amendment scope; not blocking authoring; jack-ryan reviews concurrently with dispatch authoring).

## 7. Updated Cycle 14 timeline

Per Path (III) ratification:

- Original Path (1) Cycle 14 total: ~10-15 weeks
- Path (III) micro-expansion adds: +1-2 weeks (G-B ~2-3 days + F-C ~1 week + LIGHT re-Gate-1 overhead)
- **Updated Cycle 14 total: ~11-17 weeks**

Quality > timeline (Q10) supports.

## 8. Failure-modes register additions

Add F-8 (Primary-pair tie-break degeneracy) + F-9 (LLM relationship narrative homogeneity) to `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-scope-creep-drift-register.md` § 1.

**Sub-agent gandalf or gandalf directly can author this addition (~5 min) OR KR can route as separate dispatch.** KR's call.

## 9. doc 39 amendment-pass-record entry

KR adds new amendment-pass-record entry to `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 0.1:

```markdown
### Amendment 2026-05-27 evening (continued) — Path (III) faction-assembly extension

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-27 verbatim "Let's go with option (III)"

**Scope:**
- G-B — Algorithmic primary-pair selection (PM-2 § X.7 amendment;
  Dispatch 3B scope addition)
- F-C — Phase 5 LLM-derived inter-faction relationships (Wave 3 dispatch
  scope addition; ExportFactionRelationship schema)

**Load-bearing implication:** automatic faction-pair-season narrative
mechanism via substrate-distance vote (G-B) + LLM-narrated inter-faction
relationships (F-C) composes with Path (1) Cycle 14 work. Substrate-led
discipline preserved at narrative layer. Cycle 14 timeline extends +1-2
weeks to ~11-17 weeks total under Q10.

**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` (Path III spec)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-kr-amendment-kicker.md` (this kicker)
```

## 10. Sign-off

**Author:** gandalf
**Status:** URGENT — pause Dispatch 3B + Wave 3 dispatch authoring; integrate Path III scope; LIGHT re-Gate-1 verification; resume dispatch authoring with Path III integrated.

**For:** KR to integrate Path (III) faction-assembly extension into in-flight Dispatch 3B + Wave 3 dispatch authoring BEFORE either fires. G-B + F-C compose with PM-1 + PM-2 ratified work; substrate-led discipline preserved at faction-pair narrative layer; D7 AI-tell + Discipline #46 + #41 all honored.

**Signed:** gandalf
