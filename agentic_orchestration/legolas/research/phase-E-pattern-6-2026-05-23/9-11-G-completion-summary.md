# 9.11-G Completion Summary — Marginal-Lineage Recognition Records (4 + Meta)

**Date:** 2026-05-23
**Author:** gandalf (story-and-design steward)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-gandalf-9-11-G-marginal-lineage-recognition-records.md`
**Tag:** `gandalf/9-11-G-marginal-lineage-recognition-records-2026-05-23` (local-only per ADR-001)

---

## Acceptance gates (per dispatch § Acceptance criteria)

| Gate | Status | Evidence |
|---|---|---|
| **4 recognition records authored at canonical/story/** | ✓ | 4 files listed below |
| **All 4 registered in ground-state oracle § 1** | ✓ | `canonical/00-ground-state.md` § 1 updated; 4 new rows + 1 meta-row added below n.am.indigenous entry |
| **Cross-references bidirectional (recognition records ↔ Phase E-2 artifacts; records ↔ each other)** | ✓ | Each record's Companion docs block names sister records + Phase E-2 cluster-labels artifact; companion docs network is peer-to-peer (Open Question 2 resolved as full peer-network, not parent-only) |
| **Empirical evidence honest — no commitments beyond what substrate observation supports** | ✓ | All 4 records use deferred-commitments framing per recognition-record format precedent; § 4 empirical-evidence-criteria table per record |
| **Geographic-vs-cultural tagging issue named where it applies** | ✓ | Named in all 4 records (universal across the 4 cases); cross-referenced to meta-record |
| **Sub-carry cross-references to 9.11-D / 9.11-E where relevant** | ✓ | All 4 records cite 9.11-D (substrate-tagging-artifact review) + 9.11-E (cultural-vs-geographic discipline) as corrective path |
| **Empirical triggers for future re-engagement documented per record** | ✓ | All 4 records have § 4 trigger table; 5-trigger consistency per Open Question 1 resolution; lineage-specific notes added in trigger descriptions where applicable |

---

## Records authored

| File | Lineage | Disposition framing |
|---|---|---|
| `canonical/story/south-american-indigenous-marginal-lineage-disposition-2026-05-23.md` | south_american_indigenous (N=197) | Substrate-coherent-but-geographic-tagged (Cluster 87 @ 94.4% purity, Cluster 115 @ 49.5%, Cluster 105 passenger; ~2 cultural items in 290 lineage-tagged rows) |
| `canonical/story/arctic-circumpolar-marginal-lineage-disposition-2026-05-23.md` | arctic_circumpolar (N=56) | Substrate-coherent-but-geographic-tagged (Cluster 24 @ 88.2% purity; ~0 cultural items at audited resolution; cleanest positive-control case) |
| `canonical/story/oceanic-marginal-lineage-disposition-2026-05-23.md` | oceanic (N=39) | Mostly-absorbed-and-scattered (Cluster 69 passenger 21/502 = 4.2% within-cluster + scatter across 10 clusters; ~6-8 cultural items across 5 clusters; compounding failure across coverage + tagging + lineage-vocab over-collapse) |
| `canonical/story/mesoamerican-marginal-lineage-disposition-2026-05-23.md` | mesoamerican (N=83) | Scattered-no-coherent-home (16-cluster scatter; top cluster 19/115 = 16.5% passenger; ~12-15 cultural items across 5 clusters; highest reclamation potential via 9.11-E re-tag) |
| `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md` | Cross-cutting meta | Names the 4-mode tagging-vocabulary collapse (Mode A cultural-tradition / B geographic-origin / C naming-allusion / D cross-tagged-error); universal across 4 of 5 with n.am as clean-control; corrective-path table; Fate-genre faction-architecture rep-audit prerequisite |

5 files total. Dispatch required 4; meta-record authored per Open Question 3 resolution (cross-cutting pattern is universal across all 4 marginal cases AND has an asymmetric clean-control from the 5th lineage — both halves justify the meta-record).

---

## Cluster-distribution check outcomes (per dispatch § Scope items 4-5)

### Oceanic (N=39) — RESOLVED

DB query against `cluster_membership` 2026-05-23. The 39 oceanic rows distribute across 10 clusters:

| db_cluster_id | oceanic rows | Cluster pool_count | Within-cluster % |
|---|---|---|---|
| 69 | 21 | 502 | 4.2% — passenger in cross_cultural mixed-munitions |
| 112 | 5 | 115 | 4.3% |
| 120 | 4 | 1201 | 0.3% |
| 64 | 2 | 187 | 1.1% |
| 88 | 2 | 188 | 1.1% |
| 33, 67, 109, 114, 115 | 1 each | various | < 1% |

**Outcome:** No coherent isolate. Cluster 69 absorbs 53.8% of pool as passengers (4.2% within-cluster). Rep audit of the 21 Cluster 69 oceanic rows confirms all 21 are modern Australian / NZ defence-force military hardware (frigates, LHDs, UAVs, AUVs, patrol boats, etc.); zero culturally-Pacific content. The 6-8 genuine cultural items (Boomerang ×2, Spear Thrower, Club, Kaumaile, Gweagal shield, Solomon Islands shield, Parade shield) scatter across 5 non-overlapping clusters. Framing: mostly-absorbed-and-scattered with three compounding failure modes (coverage + tagging artifact + lineage-vocab over-collapse).

### Mesoamerican (N=83) — RESOLVED per Open Question 4

DB query against `cluster_membership` 2026-05-23. The 83 mesoamerican rows distribute across 16 clusters:

| db_cluster_id | mesoamerican rows | Cluster pool_count | Within-cluster % |
|---|---|---|---|
| 112 | 19 | 115 | 16.5% (top — passenger) |
| 102 | 13 | 61 | 21.3% |
| 109 | 11 | 111 | 9.9% |
| 120 | 10 | 1201 | 0.8% |
| 69 | 8 | 502 | 1.6% (incl. 7 macuahuitl variants) |
| 88 | 5 | 188 | 2.7% |
| 78 | 4 | mixed | passenger |
| 103 | 3 | mixed | passenger |
| 108 | 3 | mixed | passenger |
| 21, 64, 67, 73, 93, 95, 114 | 1 each | various | < 1% |

**Outcome (Open Question 4 resolution):** **No coherent cluster home.** Top within-cluster percentage is 16.5% (Cluster 112) — far below the substrate-led coherent-isolate threshold seen in south_am Cluster 87 (94.4%) or arctic Cluster 24 (88.2%). Framing remains "no coherent cluster home" rather than "substrate-coherent but marginal pool size." Critically, rep audit reveals mesoamerican has the HIGHEST absolute cultural-content count of the 5 marginal-lineage cases (~12-15 items: macuahuitl ×7 in Cluster 69, Obsidian Blades with Gold Handle in Cluster 112, Hummingbird Bloodletter ×2 in Cluster 109, Macehead in Cluster 114, Macuahuitl + Tlaximaltepoztli in Cluster 120, Cashuat). The cultural items are scattered across 5+ clusters by axis-pull from modern Mexican arms-industry content within the same lineage tag — making mesoamerican the highest-reclamation-potential case via sub-carry 9.11-E re-tag-then-re-cluster smoke.

### Validation against relay claims

The dispatch's relay text (Gate-2 findings record § 4.4) gave these initial characterizations:

| Lineage | Relay framing | Empirical-investigation result | Agreement |
|---|---|---|---|
| south_am | "Cluster 114 only; purity 0.4947; modern Argentine military hardware" | Cluster 87 @ 94.4% pure (N=36) + Cluster 115 @ 49.5% (N=95) + Cluster 105 passenger pool 39 in 491-row cluster | Partial — relay had off-by-one (HDBSCAN id 114 = db_cluster_id 115) and missed the 94.4%-pure Cluster 87 home; substrate-tagging-artifact framing CONFIRMED |
| arctic | "Cluster 23 only; Russian/Swedish/French missile systems" | db_cluster_id 24 (= HDBSCAN id 23) @ 88.2% pure (N=34); confirmed | Confirmed — indexing reconciled |
| oceanic | "Pool below stratified-subsample floor in some Phase E-1 contexts; investigate where 39 rows ended up" | Cluster 69 passenger 21 + scatter across 9 other clusters; ~6-8 cultural items across 5 non-overlapping clusters | Investigated and resolved |
| mesoamerican | "Slightly above the gate; investigate cluster home (single coherent home? scattered?)" | Scattered across 16 clusters; top 16.5% within-cluster passenger; NOT substrate-coherent | Investigated and resolved per Open Question 4 |

The south_am case was the most off in the relay framing — the relay anchored on Cluster 115 (49.5% purity mixed pool) rather than Cluster 87 (94.4% purity isolate). The recognition record corrects this and frames south_am as the MOST substrate-coherent of the 4 marginal cases on raw clustering signal, with the geographic-vs-cultural tagging artifact being the load-bearing observation rather than no-coherent-home.

No methodology concerns surfaced during the cluster-distribution checks. No Gate-2 invocation needed per dispatch § "What knight-rider does after your return" item 3.

---

## Cross-cutting pattern observations (per dispatch § Open Question 3)

The geographic-vs-cultural tagging artifact is **universal across all 4 marginal cases** (south_am, arctic, oceanic, mesoamerican) and **asymmetric on the 5th case** (n.am.indigenous as clean-control). This justified authoring the meta-record `canonical/story/marginal-lineage-tagging-pattern-2026-05-23.md`.

Key cross-cutting observations:

1. **The `cultural_lineage_canonical` tag is currently multi-mode** (Mode A cultural-tradition / Mode B geographic-origin / Mode C naming-allusion / Mode D cross-tagged-error). HDBSCAN clusters substrate-led on the lineage-centroid which is mostly Mode-B-content in 4 of 5 cases, producing high-purity isolates that are NOT cultural-tradition substrate.

2. **N.am.indigenous is asymmetric because no active US/Canadian arms-industry tags items as `north_american_indigenous`.** The 4 affected cases all had active modern arms-industries during substrate-acquisition (Argentine/Brazilian/Chilean; Russian/Swedish/French; Australian/NZ; Mexican) which pulled Mode B/C/D content into their lineage tags. N.am.indigenous's clean-control state makes it the load-bearing comparison case for confirming the hypothesis.

3. **Execution-order recommendation for substrate-tagging cleanup: 9.11-D (diagnostic) → 9.11-E (re-tag) → re-clustering smoke (mesoamerican specifically; highest-leverage) → conditional 9.10-E (Mode-A-targeted expansion).** This puts substrate-vocabulary cleanup BEFORE substrate expansion so that expansion targets the actual cultural-content gap rather than amplifying both modes proportionally.

4. **Fate-genre faction-architecture rep-audit-discipline prerequisite (load-bearing for downstream).** A substrate-led cluster passing as "cultural-tradition X faction substrate" REQUIRES rep-audit AT EACH FIRING. A cluster whose top-N reps are Mode B/C/D content is NOT cultural-tradition faction substrate, regardless of lineage-purity score. This is the meta-record's most-important load-bearing observation for downstream design surfaces (D10 Path C, Phase E-3, Spirit Form).

5. **Discipline #18 amendment candidate surfaced for tracking** (semantic-layer rep-audit; the substrate's vote is binding at the geometry layer but NOT necessarily at the semantic layer). Not commitment-tier yet; surfaced in meta-record § 2.4 for future decision-log routing.

---

## Cross-cutting empirical triggers (per dispatch § Open Question 1)

Open Question 1 resolved: **the same 5 trigger categories from n.am.indigenous apply to all 4 marginal records uniformly**, with lineage-specific notes added in trigger descriptions:

1. **D10 Path C substrate-evidence gate** — Universal
2. **Phase E-1.5 sensitivity sweep** — Universal (with note that mesoamerican is the lineage most likely to surface a stable sub-cluster at different mcs due to existing cultural-content tail)
3. **Sub-carry 9.11-E resolution** — Universal (oceanic specifically calls for lineage-vocabulary sub-categorization; mesoamerican specifically gains re-clustering-smoke validation step)
4. **Substrate-expansion targeted crawl (9.10-E)** — Universal (with Mode-A-targeting constraint per meta-record § 2.3; oceanic requires sub-categorized vocabulary FIRST; mesoamerican needs smallest absolute expansion)
5. **Faction-architecture design-fit** — Universal (mesoamerican has strongest faction-fit base-state given existing Aztec mythological richness; arctic has clean-slate state requiring full substrate-expansion before faction call; oceanic likely produces separate Maori / Aboriginal / Pan-Polynesian factions rather than single oceanic faction)

---

## Companion-docs cross-linking (per dispatch § Open Question 2)

Open Question 2 resolved: **full peer-to-peer companion-docs network**, not parent-only. Each of the 4 marginal records cross-references:

- The n.am.indigenous record (parent precedent)
- The 3 other marginal records (peer sisters)
- The meta-record (cross-cutting parent)
- Phase E-2 cluster-labels artifact (.md + .json)
- Ground-state oracle § 1
- Fate-genre recognition record

This creates a fully-connected 6-node recognition-record subgraph (n.am + south_am + arctic + oceanic + mesoamerican + meta), which is the right structure for downstream readers entering the substrate-tagging-discipline territory at any node — they can navigate sideways to peer records or upward to the meta-record without traversing through n.am as required hub.

---

## Sub-carry status

| Sub-carry | Status after this dispatch |
|---|---|
| 9.11-G | **CLOSED** — 4 marginal-lineage recognition records + 1 meta-record authored; all registered in ground-state § 1 |
| 9.11-D | Queued (elrond substrate-tagging-artifact review); now has 5 lineage-specific records citing it as corrective path |
| 9.11-E | Queued (elrond cultural-vs-geographic tagging discipline); now has 5 lineage-specific records citing it as corrective path + meta-record naming it as highest-leverage substrate-tagging cleanup; mesoamerican specifically identified as highest-reclamation-potential candidate for re-tag-then-re-cluster smoke |
| 9.10-E | Dormant (legolas Mode B substrate-expansion); now has 5 lineage-specific records citing § 4 empirical triggers + meta-record naming the Mode-A-targeting constraint for dispatch authoring |
| 9.10-B.1 | Owed by gandalf (OP amendment + flag enum canonicalization); separate from this dispatch; still must land before Phase E-3 dispatch is authored |
| Discipline #18 semantic-layer amendment | Tracking candidate per meta-record § 2.4 |

---

## Tag

`gandalf/9-11-G-marginal-lineage-recognition-records-2026-05-23` — seam-prefix per ADR-001; LOCAL ONLY (not pushed).

---

## Out-of-scope items confirmed not done

- No architectural commitments (faction declarations, Spirit Form parameters, Phase E-3 design surface inheritance) — per ADR-002 + dispatch § Out of scope
- No substrate cleaning or re-tagging — that's elrond's queue (9.11-D / 9.11-E)
- No cluster re-labeling — Phase E-2 labels stand
- No 9.10-B.1 OP amendment write — separate carry, owed but not this dispatch
- No DB writes — read-only SELECT queries only per dispatch § Out of scope

---

**Signed:** gandalf (story-and-design steward), 2026-05-23
**Authority:** dispatch § Scope + Acceptance + Open Questions 1-4 resolution
