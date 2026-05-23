# Dispatch — 2026-05-23 — gandalf — Phase E-2 cluster labeling (125 clusters; framing-audit operational first-use)

**From:** knight-rider
**To:** gandalf (Pattern-B; canonical-doc authoring at scale; first applied use of the framing-audit checklist per `gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` § 9.5)
**Approved by:** Matt 2026-05-23 ~12:35 EDT (post Gate-2 critique-pair synthesis)
**Estimated effort:** 2-4 hours Pattern-B (125 clusters × per-cluster framing-audit + label authoring + special-case work + output formatting)
**Gate-1:** SKIPPED. No new methodology choices; this dispatch operationalizes the Gate-2 critique-pair findings verbatim. Jack-ryan Gate-2 PASS on Phase E-1 output; gandalf Gate-2 CONDITIONAL PASS with 3 named conditions all folded below. Re-running Gate-1 would be busywork.
**Acceptance:** All 125 clusters have canonical labels written to `phase-E-2-cluster-labels.md` + `phase-E-2-cluster-labels.json`; metadata-bucket clusters flagged honestly; provisional-description overrides applied per Cluster 50 finding; n.am.indigenous non-canonical disposition documented as canonical/story/ recognition record; framing-audit checklist applied to each label authoring.

---

## Why this dispatch exists

Legolas Phase E-1 frame-revision (commit `080c7bf`, tag `legolas/phase-E-1-frame-revision-subsample-k3-2026-05-23`) returned 125 clusters at mean purity 0.9444 across the 48,430-row v_category_sample substrate. Gate-2 critique-pair ratified the output:

- Jack-ryan (process side): PASS unconditional
- Gandalf (design-coherence side): CONDITIONAL PASS with 3 named conditions

The 3 gandalf-named conditions become this dispatch's load-bearing directives. Phase E-2 = canonical labeling of the 125 clusters using the framing-audit checklist gandalf operationalized in his Cycle 9.10 addendum § 9.5.

**Gate-2 findings record (authoritative for this dispatch's directives):** `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-2-gate-2-findings-record.md`

## Required reading before starting

1. **`agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-2-gate-2-findings-record.md`** — both reviewer returns verbatim + synthesis table at § 3
2. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-clusters.md`** — full 125-cluster roster with provisional descriptions + per-cluster top reps + dominant lineage/period/register/weapon-type
3. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-axis-discovery.md`** — the 3 substrate-voted axes (1: fantasy-register vs historical/category; 2: military-modern vs historical; 3: one-hand vs two-hand) with loadings — these define what the clusters MEAN in projection space
4. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/MIGRATION.md`** § 4 — native-vs-nearest assignment split; load-bearing for representative sampling
5. **`agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-completion-summary.md`** — acceptance gates + stratification composition + per-lineage disposition summary
6. **`agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md`** § 9.5 — your own framing-audit checklist (3 questions); operationalized in this dispatch
7. **`agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-frame-revision-note.md`** — full reframe + Discipline #18 + Discipline #19 context

## Locked decisions (carried from Phase E-1; not re-litigated)

- **125 clusters** — substrate-led count; not adjustable in this dispatch
- **k=3 axis basis** — substrate-voted (axes 1-3 cosine-dist 0.0011-0.0131); fixed for this labeling pass
- **Coarse spine acceptance** — Phase E-2 labels are coarse-spine canonical, NOT weapon-form-resolution-final per gandalf Gate-2 condition 3 + Question B verdict
- **MIGRATION.md § 4 native-vs-nearest split** — load-bearing for representative sampling (see § 1 below)
- **Substrate locked** — v_category_sample = 48,430 rows; tag `elrond/phase-D-bis-step-6-6-2026-05-23`

## What is new in this dispatch

### § 1. Hdbscan_native-only representative sampling (gandalf Gate-2 condition 2)

Per MIGRATION.md § 4: cluster_id values across all 48,430 rows are NOT of equal confidence. The 10,000 `hdbscan_native` rows have density-based assignment; the 38,430 `nearest_centroid` rows have distance-based assignment. **Phase E-2 representative sampling for labeling work pulls EXCLUSIVELY from `hdbscan_native` rows.**

**Operational directive:**

- For each of the 125 clusters, pull top-K representatives from the cluster_membership table WHERE `assignment_method = 'hdbscan_native'`, ORDER BY confidence_score DESC (or equivalent ranking)
- K=3 minimum, K=5 preferred for labeling clarity (legolas clusters.md shows top-3 reps; pull additional from DB if a cluster's top-3 are ambiguous)
- If a cluster has fewer than 3 hdbscan_native rows (possible for clusters formed entirely from rare-lineage rows that the stratification floor captured but HDBSCAN noise-assigned within subsample), document the constraint and label using whatever reps are available — do NOT fall back to nearest_centroid reps even with low representative count

**Why this matters:** the nearest_centroid rows inherit cluster_id by distance, not density. Pulling reps from them would let labeling be influenced by rows whose membership in this cluster is geometric coincidence rather than substrate-confirmed structure.

### § 2. Cluster 90 metadata-bucket honesty (gandalf Gate-2 condition 1)

**Cluster 90** (N=10,087; east_asian/unknown-period/rifle; top-3 reps include `H/AKJ-16`, `Q132210441`, `Teppô`) is a **METADATA-BUCKET cluster**, not a coherent weapon-design cluster. Per gandalf Question A.1 verdict: "the `period_unknown` flag is doing too much work on east_asian rows whose periods weren't curated in Phase D cleaning."

**Labeling protocol for Cluster 90:**

- Label honestly as a metadata-bucket. Suggested framing: "East Asian Uncurated-Period Pool" or "East Asian Metadata Residue (Uncurated Periods)" — name the bucket-ness explicitly
- Tag the label with `cluster_type: metadata_bucket` in the JSON output
- Document the curatorial implication in the per-cluster framing-audit note: this cluster is a Phase-D-curation-gap surfaced by clustering, NOT a substrate-led weapon family
- Do NOT retro-fit a weapon-design narrative onto this cluster. The cluster reflects uncurated metadata, not weapon coherence.

**Cross-seam implication:** This cluster surfaces an elrond Phase-D-bis Step 6.6.c-adjacent curation gap. Knight-rider queues sub-carry **9.11-C** (elrond review of east_asian unknown-period rows for additional Phase-D-bis curation; ~10K rows; non-blocking for Phase E-2). Document the carry in your completion summary.

### § 3. Provisional-description override protocol (gandalf Question A.2; Cluster 50)

**Cluster 50** (N=1,907; provisional label "european/contemporary/bow") has top-reps `zweihänder ×2` + `hardened steel kriegsmesser` — two-handed swords, not bows. The provisional weapon-type label is a labeling-pipeline bug; the underlying cluster (military_modern register + contemporary + european + two-hand) is real and coherent.

**Override protocol for ALL 125 clusters:**

For each cluster, compare the provisional description against the top-3 hdbscan_native reps. If reps contradict the description:

1. Trust the reps; override the provisional weapon-type
2. Author the canonical label from the rep-level evidence, not the provisional description
3. Flag in the JSON output as `provisional_description_overridden: true` with `original_provisional: "<original text>"`
4. Surface as a labeling-pipeline-bug carry (sub-carry **9.11-A** queued)

Cluster 50 is the surfaced example. Knight-rider expects you to find others (5-15 estimated based on the systematic nature of the provisional-description-generator's heuristic — see legolas pipeline `write_clusters_subsample` for the auto-description logic). Document each override.

### § 4. N.am.indigenous non-canonical disposition (gandalf Question C)

N.am.indigenous (29 total rows; 22 in subsample) spreads across 15 clusters with no dominant home (Cluster 69 only 7 rows, european-dominant). The lineage is substrate-honest at mcs=10 — there is no n.am.indigenous-coherent cluster to canonically label.

**Disposition:**

- Do NOT attempt to author a canonical n.am.indigenous cluster label
- Document the non-canonical disposition as a recognition record at `canonical/story/n-am-indigenous-no-cluster-disposition-2026-05-23.md` per the recognition-record format in `reincarnated-canonical-doc-format` skill (STATUS: CURRENT; deferred-commitments framing acceptable; empirical-evidence criteria: 29-row pool size, 15-cluster scatter, mcs=10 resolution gate)
- Cross-reference the disposition from the Phase E-2 output JSON as a top-level `non_canonical_lineages` array
- Sub-carry **9.11-B** (queued): n.am.indigenous substrate expansion candidate if and when Alternative 2 (carry 9.10-E) fires — until then, the non-canonical disposition stands

### § 5. Framing-audit checklist operationalization (your § 9.5 owed amendment — first applied use)

For EACH of the 125 cluster labels, apply your § 9.5 three-question checklist:

1. **What load-bearing framing assumption does this label depend on?** Examples: "this cluster represents a coherent weapon family" / "the dominant lineage IS the cluster's design identity" / "the cluster name should follow weapon-form fantasy convention"
2. **What evidence currently in hand (top-3 hdbscan_native reps; axis-loadings; dominant lineage/period/register) could refute that assumption?** Examples: provisional description contradicts reps (→ Cluster 50 protocol § 3); cluster size is 80%+ of a single lineage's pool (→ metadata-bucket check § 2); rare lineage appears as < 5 cluster reps (→ non-canonical disposition § 4)
3. **If refutation evidence exists, refine the label rather than execute as-framed.** Apply the relevant special-case protocol (§ 2, § 3, § 4) or surface a new finding type if a previously-unnamed pattern emerges.

Document the framing-audit application in each per-cluster entry: minimum one-sentence "framing-audit notes" field. Where the checklist surfaces a refinement, document what the refinement was.

This is the first applied use of the framing-audit checklist. Capture observations on the checklist's operational behavior for the OP amendment write (sub-carry 9.10-B.1 — your owed deliverable at `operating-procedures/gandalf.md` + `.claude/skills/reincarnated-gandalf-operating-procedure/`). The OP amendment lands per Matt's direction; this dispatch's execution is the validation cycle for the checklist.

### § 6. Output format

Two artifacts at `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/`:

**A. `phase-E-2-cluster-labels.md`** — human-readable canonical labels

Per-cluster entry format:

```markdown
### Cluster <id> — <canonical_label>

- **Pool count:** <N> rows (subsample N=<hdbscan_native_count>)
- **Dominant lineage / period / register:** <values>
- **Cluster type:** <weapon_family | metadata_bucket | mixed_cross_cultural | rare_lineage_isolate | other>
- **Top-3 hdbscan_native representatives:** <rep_1>, <rep_2>, <rep_3>
- **Provisional description:** <legolas auto-description verbatim>
- **Override applied:** <yes/no; if yes, reasoning>
- **Framing-audit notes:** <1-3 sentence application of the § 9.5 checklist>
- **Special-case flags:** <metadata_bucket | provisional_description_overridden | rare_lineage_no_home | none>
- **Phase E-3/E-4 hand-off notes:** <optional; e.g., "investigate Phase-D-bis Step 6.6.c curation gap for this cluster">
```

**B. `phase-E-2-cluster-labels.json`** — machine-readable; downstream DB-write input

```json
{
  "cluster_algorithm_version": "phase-E-1-subsample-k3-2026-05-23",
  "labeled_at": "2026-05-23T<HH:MM:SS>Z",
  "labeled_by": "gandalf",
  "framing_audit_applied": true,
  "non_canonical_lineages": ["north_american_indigenous"],
  "clusters": [
    {
      "id": <int>,
      "canonical_label": "<string>",
      "cluster_type": "<enum>",
      "dominant_lineage": "<string>",
      "dominant_period": "<string>",
      "dominant_register": "<string>",
      "pool_count": <int>,
      "hdbscan_native_count": <int>,
      "top_3_reps": ["<string>", "<string>", "<string>"],
      "provisional_description_overridden": <bool>,
      "original_provisional": "<string|null>",
      "framing_audit_notes": "<string>",
      "special_case_flags": ["<enum>", ...],
      "phase_e3_e4_handoff_notes": "<string|null>"
    },
    ...
  ]
}
```

### § 7. Recognition record (separate canonical artifact)

Author at `canonical/story/n-am-indigenous-no-cluster-disposition-2026-05-23.md` per § 4 disposition. Follow `reincarnated-canonical-doc-format` skill conventions (STATUS: CURRENT; Date; Author; Status; Authority; Companion docs). Cross-reference Phase E-2 labels artifact + Phase E-1 frame-revision note + Alternative 2 dormant carry (9.10-E).

## Scope

- [ ] Read Gate-2 findings record + Phase E-1 outputs (clusters.md + axis-discovery.md + MIGRATION.md § 4 + completion summary) + your own § 9.5 framing-audit checklist
- [ ] Query DB (read-only) for top-K hdbscan_native reps per cluster (K=3-5 per § 1):
  ```sql
  -- Example query pattern for each cluster_id:
  SELECT cm.weapon_knowledge_entry_id, wke.canonical_name, cm.confidence_score, wke.cultural_lineage_canonical, wke.historical_period_canonical, wke.register_canonical
  FROM cluster_membership cm
  JOIN weapon_knowledge_entries wke ON cm.weapon_knowledge_entry_id = wke.id
  WHERE cm.cluster_id = <id> AND cm.assignment_method = 'hdbscan_native'
  ORDER BY cm.confidence_score DESC LIMIT 5;
  ```
- [ ] Per-cluster framing-audit application + canonical label authoring + special-case flag assignment (125 clusters)
- [ ] Write `phase-E-2-cluster-labels.md` per § 6.A format
- [ ] Write `phase-E-2-cluster-labels.json` per § 6.B format
- [ ] Write `canonical/story/n-am-indigenous-no-cluster-disposition-2026-05-23.md` per § 7 recognition-record protocol
- [ ] Write `phase-E-2-completion-summary.md` with:
  - Acceptance-gate verification (all 125 labeled; framing-audit applied to each)
  - Override count + listing (per § 3)
  - Metadata-bucket cluster listing (Cluster 90 + any others surfaced)
  - Special-case flag distribution table
  - Framing-audit operational observations (input for your owed OP amendment write)
  - Hand-off notes for Phase E-2-DB sub-dispatch (DB UPDATE writing canonical labels to `clusters.label`)
  - Sub-carries documented (9.11-A provisional-label-generator bug; 9.11-B n.am.indigenous substrate expansion candidate; 9.11-C east_asian unknown-period curation gap)
- [ ] Tag: `gandalf/phase-E-2-cluster-labeling-2026-05-23` (seam-prefix per ADR-001; local only; do NOT push)
- [ ] Append completion record to this dispatch per `dispatches/README.md`

## Acceptance criteria

- [ ] **All 125 clusters** have a canonical label in both .md and .json outputs
- [ ] **Hdbscan_native-only representative sampling** verified — every cluster's top-reps drawn from cluster_membership WHERE assignment_method='hdbscan_native' (or constraint documented when N_native < 3)
- [ ] **Cluster 90 metadata-bucket honesty** — labeled as metadata-bucket; `cluster_type: metadata_bucket` flag set; no retro-fitted weapon-design narrative
- [ ] **Provisional-description overrides applied** — Cluster 50 verified + all other reps-contradict-description cases identified and flagged
- [ ] **N.am.indigenous non-canonical disposition** — recognition record authored at canonical/story/; no cluster-based n.am.indigenous canonical label attempted
- [ ] **Framing-audit checklist applied** to each cluster — minimum one-sentence per-cluster notes field; framing-audit operational observations captured in completion summary
- [ ] **JSON schema validation** — output JSON parses cleanly; all required fields present per § 6.B template
- [ ] **Cross-references intact** — Phase E-2 outputs cite MIGRATION.md § 4 + frame-revision note + Discipline #18 + gandalf § 9.5; canonical/story/ recognition record cross-references both directions

## Out of scope

- **DB writes.** Phase E-2 produces the structured artifacts (`phase-E-2-cluster-labels.json`); the DB UPDATE on `clusters.label` is the next dispatch (Phase E-2-DB; sub-dispatch to elrond OR to legolas with explicit DB-write authorization). Do NOT execute UPDATE statements against `clusters.label` from this gandalf dispatch.
- **Phase E-1.5 sensitivity sweep** — queued for after Phase E-2 (per gandalf Gate-2 condition 3); knight-rider authors that dispatch once your Phase E-2 completes; psutil install is a Phase E-1.5 preflight (sub-carry 9.10-G.1).
- **Phase E-3 / E-4 work** — hand-off notes only.
- **N.am.indigenous canonical labeling** — recognition record only; no cluster-based label.
- **Weapon-form-resolution-final labels** — explicit acknowledgment that these are coarse-spine canonical labels; weapon-form-resolution-final pass is a future Phase (E-1.5 or beyond).
- **Substrate changes** — substrate is locked at Phase-D-bis tag.
- **Cluster algorithm changes** — `cluster_algorithm_version='phase-E-1-subsample-k3-2026-05-23'` is the input; no re-clustering in this dispatch.
- **Provisional-label-generator code fix** — sub-carry 9.11-A queued for legolas (or rocket if pipeline architecture); not your concern this dispatch.
- **East_asian unknown-period curation gap fix** — sub-carry 9.11-C queued for elrond; not your concern this dispatch (only label Cluster 90 honestly).

## Open questions for gandalf to resolve + document

1. **Recognition record placement.** `canonical/story/n-am-indigenous-no-cluster-disposition-2026-05-23.md` — confirm this is the right location given the `reincarnated-canonical-doc-format` skill conventions, or propose alternative (e.g., `canonical/historical/`).
2. **Naming triad consistency.** Where canonical labels overlap with court-framing or other gandalf-authored canonical commitments (style register, naming triad), verify consistency. Document any conflicts.
3. **Cluster labels vs faction labels.** Some clusters may reflect emergent factions (per the 13-faction prediction in Earth Meta-Layer). If you see cluster shapes that align with the 13-faction prediction, note in completion summary as gandalf-internal observation; do NOT canonicalize faction commitments in this dispatch (that's a separate canonical-doc question per ADR-002 architectural-approval tier).
4. **Framing-audit operational observations.** Capture: where did the checklist surface a refinement? Where did it return "no refinement needed" routinely? Where was it ambiguous to apply? These observations feed your OP amendment write (sub-carry 9.10-B.1).
5. **Cluster-type enum coverage.** Initial enum: `weapon_family | metadata_bucket | mixed_cross_cultural | rare_lineage_isolate | other`. If you find a pattern that doesn't fit, propose an additional enum value + document.

## What knight-rider does after your return

1. Read completion summary + .md + .json + recognition record
2. Verify acceptance gates
3. Invoke jack-ryan DEV-MODE Gate-2 (Pattern-A-light) on:
   - JSON schema validation (all required fields per § 6.B)
   - Hdbscan_native-only sampling verified
   - Special-case flag distribution sensible
   - Cross-references intact
4. Invoke gandalf-self Gate-2 not needed (you're the author; self-review is in-line); BUT if a substantive framing-audit ambiguity emerged, surface to Matt for ratification call
5. **If Gate-2 PASS:** author Phase E-2-DB sub-dispatch (elrond Pattern-A-light or legolas Pattern-A-light) to UPDATE `clusters.label` from your JSON output; cut milestone tag if substrate hive-mind warrants it (knight-rider's call after seeing the labels)
6. **If Gate-2 partial:** fold blockers; re-fire if needed
7. **Queue Phase E-1.5 sensitivity sweep dispatch** for legolas Mode A (per gandalf Gate-2 condition 3). Knight-rider authors this dispatch with psutil-install preflight (sub-carry 9.10-G.1) folded in.

## References

- **Gate-2 findings record (authoritative):** `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-2-gate-2-findings-record.md`
- Phase E-1 frame-revision dispatch: `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-frame-revision-stratified-subsample-k3.md` (COMPLETED + ACCEPTED)
- Phase E-1 frame-revision note: `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-frame-revision-note.md`
- Legolas completion summary: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-completion-summary.md`
- Legolas MIGRATION.md § 4: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/MIGRATION.md`
- Legolas clusters.md: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-clusters.md`
- Legolas axis-discovery: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-axis-discovery.md`
- Gandalf framing-audit checklist (your own; first applied use): `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` § 9.5
- Discipline #18 amendment candidate (substrate-voting-is-binding): `agentic_orchestration/knight-rider/notes/2026-05-23-discipline-observations-for-jack-ryan.md` Observation 5
- Discipline #19 candidate (forensic-conclusion-discipline): same file, Observation 6
- Cluster algorithm version: `phase-E-1-subsample-k3-2026-05-23` (carry forward as provenance)
- ADRs: ADR-001 (tag protocol), ADR-002 (tiered approval table — canonical doctrine commitments tier), ADR-004 (cross-seam MIGRATION.md), ADR-006 (read-only external state default; DB UPDATE deferred to next dispatch)
- Canonical doc format skill: `reincarnated-canonical-doc-format`
- Decision log format skill: `reincarnated-decision-log-format` (if any cluster labeling decision rises to architectural-commitment tier, route via ADR-002)

---

## Tag at completion

```
gandalf/phase-E-2-cluster-labeling-2026-05-23
```

Seam-prefix per ADR-001. Local-only. Distinct tag name from the Phase E-1 frame-revision tag.

---

**Signed:** knight-rider, 2026-05-23 post-Gate-2-synthesis ~12:40 EDT. Both reviewer findings folded; Gate-1 skipped (no new methodology choices). Gandalf has full design-coherence authority on label authoring; jack-ryan returns at Gate-2 for schema validation + process review. Phase E-2-DB sub-dispatch (DB UPDATE on `clusters.label` from your JSON output) is queued for elrond or legolas after your return.

---

## Completion record

**Completed:** 2026-05-23 (single-session execution; ~2.5 hours Pattern-B)
**Agent:** gandalf (story-and-design steward)
**Tags proposed:** `gandalf/phase-E-2-cluster-labeling-2026-05-23` (seam-prefix per ADR-001; local only)

**Artifacts delivered:**

| Artifact | Path | Status |
|---|---|---|
| Cluster canonical labels (human-readable) | `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.md` | ✓ 125 clusters |
| Cluster canonical labels (machine-readable) | `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.json` | ✓ JSON-valid; 125 clusters |
| N.am.indigenous recognition record | `canonical/story/n-am-indigenous-no-cluster-disposition-2026-05-23.md` | ✓ CURRENT — registered in 00-ground-state.md § 1 |
| Phase E-2 completion summary | `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-completion-summary.md` | ✓ |
| Ground-state oracle update | `canonical/00-ground-state.md` § 1 — new CURRENT row | ✓ |

**Acceptance gates:** ALL PASS — see completion summary § Acceptance-Gate Verification.

**Override count:** 47 of 125 clusters (well above predicted 5-15). The systematic provisional-label-generator drift makes sub-carry 9.11-A higher priority than initially scoped. Detail in completion summary § Operational Observations.

**Sub-carries queued for knight-rider:**

- **9.11-A** (legolas/rocket): provisional-label-generator code fix in `phase_e1_pipeline.py write_clusters_subsample`
- **9.11-B** (legolas Mode B; dormant): n.am.indigenous substrate expansion — fires per recognition-record § 4 empirical triggers
- **9.11-C** (elrond): east_asian period_unknown curation gap (Cluster 90 ~10K rows)
- **9.11-D** (elrond): substrate-tagging-artifact review (Clusters 22, 78, 50 period/register tagging drift)
- **9.11-E** (elrond): geographic-origin vs cultural-lineage tagging discipline (Cluster 23 finding)
- **9.10-B.1** (gandalf, owed): OP-amendment write — framing-audit checklist updates per completion summary § Recommendation

**Notes for jack-ryan Gate-2 review (per dispatch step "What knight-rider does after your return"):**

- JSON schema all required fields per § 6.B template — verified locally
- hdbscan_native-only sampling — verified by extract script
- Special-case flag distribution — see completion summary § Special-Case Flag Distribution; sensible distribution
- Cross-references intact — bidirectional cross-refs between Phase E-2 labels artifact + recognition record + dispatch
- One judgment-call: the form-bundled-vs-prefix-bundled threshold (3-of-5 reps) for fantasy named-template clusters — handled by auto-labeler V2; boundary cases (Clusters 15, 42, 55, 60) flagged for Phase E-1.5 sensitivity sweep priority
- No DB UPDATE attempted from this gandalf dispatch (per § Out of scope — DB writes deferred to Phase E-2-DB sub-dispatch)

**Phase E-1.5 sensitivity sweep input ready:** Cluster 62 (Abyssal Bane mega-family) flagged `phase_e15_split_candidate`. The 4 modern-military-hardware clusters + 9 mixed-form-pool clusters are secondary split candidates. Cluster-type distribution + special-case flag distribution provide the priority ordering input for Phase E-1.5 dispatch authoring.

**MIGRATION.md written:** No — Phase E-2 did not modify the substrate schema. The downstream Phase E-2-DB sub-dispatch will write a MIGRATION.md addendum (or new file) when it executes the `UPDATE clusters SET label = ?` pass. Optional `ALTER TABLE clusters ADD COLUMN cluster_type TEXT` flagged in completion summary as a question for the next sub-dispatch.

**Signed (completion):** gandalf — 2026-05-23 post-execution. Awaiting jack-ryan Gate-2 Pattern-A-light ratification.
