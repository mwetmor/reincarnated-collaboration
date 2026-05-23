# Phase E-2 Output Gate-2 Findings Record — 2026-05-23

**Author:** knight-rider
**For:** durable record of jack-ryan DEV-MODE Gate-2 review on gandalf Phase E-2 output (commit `5b8754e`, tag `gandalf/phase-E-2-cluster-labeling-2026-05-23`)
**Reviewer:** jack-ryan (Pattern-A-light, ~30 min)
**Verdict:** **Gate-2 ratification PASS** — Phase E-2-DB sub-dispatch unblocked

---

## 1. Findings (verbatim from jack-ryan return)

### Finding 1 — JSON schema compliance [INFO PASS]

All 15 dispatch § 6.B required fields present on all 125 cluster entries. Zero missing fields. Top-level fields all correct types. `framing_audit_applied: true` (bool). `non_canonical_lineages: ["north_american_indigenous"]` (array). JSON parses cleanly.

### Finding 2 — hdbscan_native-only sampling [INFO PASS]

`db_cluster_id` present on all 125; equals `id + 1` exactly (no mismatches). All `top_3_reps` arrays length ≥ 3. Completion summary's smallest native count = 12 (Cluster 0) consistent with JSON. `indexing_note` field correctly documents id/db_cluster_id distinction.

### Finding 3 — Cross-references intact [INFO PASS]

Recognition record ↔ Phase E-2 outputs bidirectional. Phase E-2 .md header cites MIGRATION.md § 4, framing-audit § 9.5, Disciplines #18/#19. Recognition record cross-references Alternative 2 dormant carry (9.10-E).

### Finding 4 — Schema gap: clusters.cluster_type column [INFO]

`cluster_type` lives in JSON only; no `clusters` table column. NOT a Gate-2 BLOCK — JSON artifact is durable; Phase E-3/E-4 can read directly. Phase E-2-DB sub-dispatch should carry as open design question: ALTER TABLE now (idempotent ADD COLUMN; while connection is open) or defer to Phase E-3.

### Finding 5 — Recognition record format [INFO PASS]

STATUS stamp, Date, Author, Authority, Status verbose, Companion docs block all present. Matches precedent (`fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md`).

### Finding 6 — Ground-state oracle § 1 registration [INFO PASS]

Recognition record registered as CURRENT row in ground-state § 1 with full description. Phase E-2 labels artifact correctly NOT registered (lives under `agentic_orchestration/legolas/research/`, not canonical/).

### Finding 7 — Special_case_flag distribution documentation [WARN]

Dispatch § 6.B initial enum listed 5 values; actual output contains **15 distinct flag values**. The 10 additional values are NOT documented in any canonical reference. Completion summary's distribution table has one-line descriptions, minimally sufficient for sub-dispatch authoring. **However:** the OP-amendment write (sub-carry 9.10-B.1) MUST canonicalize these as the authoritative `special_case_flags` enum BEFORE Phase E-3/E-4 work begins, otherwise downstream agents will re-derive or conflict with this flag vocabulary. Cite: Discipline #10 (attribution clarity) + Principle #2 (no free-floating design decisions).

**Recommendation:** knight-rider folds a note into the Phase E-2-DB sub-dispatch + Phase E-1.5 dispatch that **9.10-B.1 must land before the Phase E-3 dispatch is authored.**

### Finding 8 — Phase E-2-DB sub-dispatch readiness [INFO PASS]

JSON ready for elrond UPDATE pass. SQL pattern in completion summary § Hand-off Notes is correct (parameterized `(db_cluster_id, canonical_label)` pairs; `WHERE id = ?`; verification query). `db_cluster_id` present on all entries; indexing semantics documented at JSON top level.

### Micro INFO — Override-count discrepancy

`provisional_description_overridden` boolean count = 47; flag-array count for same = 46. One cluster has the boolean true but missing the corresponding flag-array entry. Authoritative signal for sub-dispatch is the boolean field. Surface for gandalf low-priority cleanup; not blocking.

---

## 2. Synthesis for next dispatches

| Finding | Required directive in next dispatch authoring |
|---|---|
| F4 | Phase E-2-DB sub-dispatch carries ALTER TABLE design question (decide-at-fire) |
| F7 | Phase E-2-DB + Phase E-1.5 dispatches BOTH carry sequencing constraint: **9.10-B.1 (gandalf OP amendment + flag enum canonicalization) must land before Phase E-3 is authored** |
| Micro | Gandalf low-priority cleanup carry (9.11-A-adjacent); flag-array consistency on the 1 cluster |

---

## 3. Sub-carry status after this Gate-2

| Sub-carry | Status change |
|---|---|
| 9.10-G — Phase E-1.5 sensitivity sweep | UNBLOCKED; ready for legolas Mode A Pattern-A-light fire |
| 9.10-G.1 — psutil install preflight | Carried forward into Phase E-1.5 dispatch |
| 9.10-B.1 — gandalf framing-audit OP amendment + flag enum canonicalization | **NEW sequencing constraint:** must land before Phase E-3 dispatch is authored |
| 9.11-A — provisional-label-generator bug fix | Priority ESCALATED (47 overrides vs 5-15 predicted) |
| 9.11-B — n.am.indigenous substrate expansion | DORMANT; conditional on 4 empirical triggers per recognition record |
| 9.11-C — east_asian period_unknown curation gap (elrond) | Queued |
| 9.11-D — substrate-tagging-artifact review (elrond) | Queued (NEW from gandalf operational observations) |
| 9.11-E — geographic-origin vs cultural-lineage tagging discipline (elrond) | Queued (NEW from gandalf operational observations) |

---

**Signed:** knight-rider, post-Gate-2-PASS synthesis 2026-05-23 ~13:10 EDT. Phase E-2-DB sub-dispatch authoring + Phase E-1.5 sensitivity sweep authoring follow.

---

## 4. Gandalf design-side spot-check relay (post-jack-ryan-Gate-2; ~13:15 EDT)

Gandalf returned a design-side spot-check of `phase-E-2-cluster-labels.md` and surfaced four sub-carry adjustments + one condition withdrawal. Folding into orchestration sequencing.

### 4.1 Cultural-tradition-descriptor condition: WITHDRAWN

Earlier framing-conversation-tier discussion contemplated permitting cultural-tradition descriptors (Arthurian-aesthetic / Greek / Norse) in broadly-fictionalized tiers. Gandalf's spot-check confirms sub-agent gandalf held strictly to **substrate-descriptive labels** throughout — and that is the correct operational lock.

**Operational lock confirmed:** substrate-descriptive-only for cluster labels. Aesthetic-cultural-tradition handles belong downstream (Phase E-3 configuration), NOT in the label layer.

### 4.2 Sub-carry 9.11-A (labeler bug fix): ELEVATE PRIORITY — sequencing constraint

**Fires BEFORE Phase E-1.5 sensitivity sweep, NOT in parallel.**

Gandalf's spot-check finds the labeler bug is NOT 5-15 edge cases — it is **systemic random token-pair generation**. Spot-check examples:

- Cluster 0: provisional `staff/axe` — reps are revolver / kukri / wakizashi
- Cluster 9: provisional `dagger/wand` — reps are all javelins
- Cluster 23: provisional `lance/rifle` — reps are SPH + MANPADS systems
- Cluster 53: provisional `bow/hammer` — reps are bow + glaive + halberd

The generator appears to produce token-pairs ungrounded in actual rep content. If Phase E-1.5 re-fires with the broken labeler, all new clusters need ~37.6%+ human-override pass — wastes the labeling work.

**Investigation location:** `phase_e1_pipeline.py write_clusters_subsample` (legolas-authored). Owner: legolas (or rocket). Likely quick fix once located.

**Sequencing impact:** Phase E-1.5 sensitivity sweep dispatch is **DEFERRED** until 9.11-A lands.

### 4.3 Sub-carries 9.11-D + 9.11-E: EXPAND SCOPE

Original scope named Clusters 22, 78, 50. Spot-check finds **~15-25 of 125 clusters** have variants of the substrate-tagging issue (`lineage_tag_geographic_not_cultural`, `period_tag_likely_metadata_artifact`, `lineage_uncurated`, `mixed_form_within_cluster`).

Sampled affected clusters: 22, 23, 50, 78, 114, 115, 117, 124, plus the ~10K-row Cluster 90 metadata-bucket.

**Discipline-level issue:** substrate cleaning policy collapses "cultural-tradition-of-origin" with "geographic-region-of-origin-or-deployment." These are different things. Russian Cold War MANPADS are not culturally arctic_circumpolar; they are geographically northern.

Elrond work; non-blocking for Phase E-2 acceptance; load-bearing for substrate quality going forward.

### 4.4 NEW sub-carry 9.11-G: marginal-lineage recognition record pass

Parallel structure to n.am.indigenous-no-cluster-disposition. Lineages where substrate-coverage failure + substrate-tagging-failure compound:

- **south_american_indigenous** (N=197; Cluster 114 only; purity 0.4947; reps are modern Argentine military hardware)
- **arctic_circumpolar** (N=56; Cluster 23 only; reps are Russian/Swedish/French missile systems)
- **oceanic** (N=39; needs cluster-distribution check)
- **mesoamerican** (N=83; needs cluster-distribution check)

**Owner:** gandalf (recognition record territory)
**Trigger:** Phase E-2 labels landed; honest disposition prevents premature commitments at Phase E-3 / Spirit Form / faction-architecture
**Why it matters:** these are the lineages where appropriation concerns are sharpest AND substrate is least able to support cluster-coherent representation. Recognition records establish the empirical boundary condition before downstream design surfaces inherit assumptions.

### 4.5 What's NOT in the relay

- Form-bundling vs prefix-bundling distinction is already captured in the labels themselves (cluster-type distribution; Cluster 62 explicitly named as Abyssal Bane Mega-Family with `phase_e15_split_candidate` flag). No additional artifact needed.
- Framing-audit checklist amendment candidates (under 9.10-B.1) are gandalf-owed for the OP amendment write; not knight-rider's queue.

---

## 5. Revised orchestration sequencing (post-spot-check relay)

**Authoring now (this session):**

1. **Phase E-2-DB sub-dispatch** → elrond Pattern-A-light. UPDATE `clusters.label` from JSON; optional ALTER TABLE for `cluster_type`; round-trip smoke; MIGRATION.md amendment; tag.
2. **Sub-carry 9.11-A dispatch** → legolas Pattern-A-light. Investigate + fix provisional-label-generator in `phase_e1_pipeline.py write_clusters_subsample`; verify by re-firing subsample mode + comparing new provisional descriptions to gandalf's overrides.
3. **Sub-carry 9.11-G dispatch** → gandalf Pattern-A-light. 4 marginal-lineage recognition records (south_american_indigenous, arctic_circumpolar, oceanic, mesoamerican) following the n.am.indigenous precedent.

**Deferred until 9.11-A lands:**

- **Phase E-1.5 sensitivity sweep** (9.10-G + 9.10-G.1). Knight-rider authors this AFTER 9.11-A acceptance.

**Owed:**

- **9.10-B.1** (gandalf OP amendment + flag enum canonicalization). Must land before Phase E-3 dispatch is authored. Non-blocking for the three dispatches above.

**Sub-carry status (updated):**

| Sub-carry | Status |
|---|---|
| 9.11-A | **ESCALATED + SEQUENCED;** authoring now; fires BEFORE Phase E-1.5 |
| 9.11-D | **EXPANDED;** ~15-25 affected clusters; elrond queue |
| 9.11-E | **EXPANDED;** discipline-level (cultural vs geographic tagging); elrond queue |
| 9.11-G | **NEW;** 4 recognition records; gandalf queue; authoring now |
| 9.10-G | DEFERRED until 9.11-A lands |
| 9.10-B.1 | Owed by gandalf; must land before Phase E-3 |
