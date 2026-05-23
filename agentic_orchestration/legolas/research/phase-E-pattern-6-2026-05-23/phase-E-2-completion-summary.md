# Phase E-2 Completion Summary — Cluster Canonical Labeling (Coarse Spine)

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-23
**Dispatch:** `agentic_orchestration/dispatches/2026-05-23-gandalf-phase-E-2-cluster-labeling.md`
**Tag (proposed):** `gandalf/phase-E-2-cluster-labeling-2026-05-23` (seam-prefix per ADR-001; local only)
**Cluster algorithm version (input, carry-forward provenance):** `phase-E-1-subsample-k3-2026-05-23`

---

## Acceptance-Gate Verification

| Acceptance criterion | Status | Evidence |
|---|---|---|
| All 125 clusters have canonical labels in both `.md` and `.json` outputs | ✓ PASS | `phase-E-2-cluster-labels.md` lists 125 per-cluster entries; `phase-E-2-cluster-labels.json` `clusters[]` length = 125 |
| hdbscan_native-only representative sampling verified | ✓ PASS | Extract script (`/tmp/phase-E-2-author/`) issues `WHERE cm.assignment_method = 'hdbscan_native'`; all 125 clusters have ≥ 12 native reps (smallest = Cluster 0 with 12 native rows; well above the 3-rep minimum). Constraint clause for N_native < 3 was unreachable. |
| Cluster 90 metadata-bucket honesty | ✓ PASS | Cluster 90 canonical label = "East Asian Uncurated-Period Metadata Pool"; `cluster_type: metadata_bucket`; no retro-fitted weapon-design narrative. Sub-carry 9.11-C documented. |
| Provisional-description overrides applied | ✓ PASS | 47 overrides applied (well above predicted 5-15). Cluster 50 (zweihänder + drone-detector) handled per § 3 protocol; all other reps-contradict-description cases identified and flagged with `provisional_description_overridden`. |
| N.am.indigenous non-canonical disposition | ✓ PASS | Recognition record authored at `canonical/story/n-am-indigenous-no-cluster-disposition-2026-05-23.md`; no cluster-based n.am.indigenous canonical label attempted; `non_canonical_lineages: ["north_american_indigenous"]` in JSON output. |
| Framing-audit checklist applied to each cluster | ✓ PASS | Every cluster has a non-empty `framing_audit_notes` field. Operational observations captured below. |
| JSON schema validation | ✓ PASS | Output JSON parses cleanly (`json.load()` succeeds); all required fields per dispatch § 6.B template present. |
| Cross-references intact | ✓ PASS | Phase E-2 outputs cite MIGRATION.md § 4, frame-revision note, Discipline #18 + #19, gandalf § 9.5; recognition record cross-references Phase E-2 labels artifact + frame-revision note + Alternative 2 dormant carry (9.10-E). |

**Bis-disposition: ACCEPTANCE.** Phase E-2 cluster labeling artifacts ready for Gate-2 process review (jack-ryan DEV-MODE Pattern-A-light) and Phase E-2-DB sub-dispatch authoring (elrond or legolas DB UPDATE).

---

## Override Count + Listing

**Total overrides applied:** 47 (predicted 5-15; actual 47 is **~3-9× the prediction**).

This is a load-bearing finding. The systematic nature of the provisional-label-generator drift makes sub-carry **9.11-A (provisional-label-generator code fix)** higher priority than the dispatch authoring contemplated. Detail in § Operational Observations.

**Categories of overrides** (each cluster may contribute to multiple categories):

| Category | Count | Example clusters |
|---|---|---|
| Provisional `weapon-form` token did not appear in any top-3 hdbscan_native rep | ~30 | Clusters 0, 4, 8, 22, 23, 24, 27, 50, 52, 62, 67, 68, 71, 78, 87, 90, 92, 101, 108, 119 (representative) |
| Provisional named pre-modern weapon-form but reps were contemporary military hardware (UAV/missile/SPH/APC) | 4 | Clusters 23, 31, 44, 71 |
| Provisional named weapon-form but reps showed substrate metadata residue (Wikidata Q-numbers, alphanumeric catalog IDs) | 4 | Clusters 90, 92, 101, 108 |
| Form-bundled fantasy named-template cluster mis-tokenized (provisional took first-token of weapon-type field; rep evidence showed unified weapon-form across named-template prefixes) | ~25 | Clusters 2 (Battleaxe), 6 (Wand), 7 (Shield), 12 (Dagger), 16 (Shortsword), 17 (Greatsword), 18 (Longsword), 26/28 (Staff), 29 (Crossbow), 34 (Bow), 35 (Halberd), 36 (Glaive), 38 (Hammer), 40 (Scimitar), 41 (Crossbow), 43 (Lance), 45 (Flail), 46 (Rapier), 48/49 (Rifle), 51 (Mace), 56 (Axe), 57 (Mace), 59 (Hammer), 61 (Spear), 64 (Musket), etc. |

**Note on the form-bundled category:** the auto-labeler's framing-audit detected form-bundling in 25+ clusters where provisional descriptions tokenized weapon-type fields incorrectly (likely the legolas pipeline `write_clusters_subsample` heuristic). The provisional fields look like "PROVISIONAL: fantasy_generic fictional axe/greataxe weapons (fantasy register; named_template; N=214)" but rep evidence reveals the cluster is actually a **Battleaxe** form-bundled named-item family. Some of these were technically borderline (the provisional description listed *a* weapon-type that was *related to* the form, e.g., "axe/greataxe" vs. true form "Battleaxe"), but they share the same root cause: the provisional-label-generator picked top-K tokens from a sparse/partial weapon_type column rather than honoring the form-signal in rep canonical_names.

---

## Metadata-Bucket Cluster Listing

| Cluster ID | Canonical label | Pool N | Lineage | Period | Sub-carry |
|---|---|---|---|---|---|
| Cluster 90 | East Asian Uncurated-Period Metadata Pool | 10,087 | east_asian | unknown | **9.11-C** — elrond Phase-D-bis Step 6.6.c-adjacent review of east_asian period_unknown rows (~10K) for additional curation |

Only Cluster 90 was flagged `metadata_bucket` per the dispatch § 2 criterion (large lineage-pure cluster collapsed by uncurated-period metadata). The framing-audit checked all other clusters; no other clusters met the metadata-bucket signature (≥5,000 rows + dominant period=unknown + lineage-purity=1.0 + reps that are alphanumeric catalog IDs). Several smaller clusters surfaced **catalog-residue patterns** (raw Wikidata Q-numbers in reps), captured under `lineage_uncurated` flag rather than `metadata_bucket` — see Cluster 92, 101, 108, 119.

---

## Special-Case Flag Distribution

| `special_case_flag` | Count | Description |
|---|---|---|
| `provisional_description_overridden` | 46 | Provisional auto-generated label was refined from rep evidence |
| `low_lineage_purity` | 20 | Cluster lineage purity < 0.60 — substantial secondary lineage content |
| `mixed_form_within_cluster` | 13 | Cluster substrate-coherent at axis level but weapon-form-heterogeneous |
| `modern_military_hardware` | 7 | Cluster dominated by contemporary military hardware (UAV/missile/SPH/APC/grenade-launcher/SMG) |
| `lineage_uncurated` | 7 | Cluster contains substantial raw Wikidata Q-number or untyped-lineage rows |
| `period_tag_likely_metadata_artifact` | 2 | Cluster period tagging appears to be substrate-curation artifact (e.g., bronze-age palstave tagged early_modern) |
| `absorbs_rare_lineage_rows` | 2 | Cluster absorbs rare-lineage rows that have no coherent home of their own |
| `lineage_tag_geographic_not_cultural` | 1 | Cluster lineage tagging reflects geographic origin rather than cultural lineage (Cluster 23) |
| `labeling_pipeline_bug_surfaced` | 1 | Cluster surfaced by Gate-2 Question A.2 as the canonical labeling-pipeline-bug example (Cluster 50) |
| `fantasy_named_template_cross_form` | 1 | Fantasy-generic named-template family bundles across weapon-forms (Cluster 62 Abyssal Bane mega-family) |
| `phase_e15_split_candidate` | 1 | Cluster identified as Phase E-1.5 sensitivity sweep priority for splitting (Cluster 62) |
| `n_am_indigenous_passenger` | 1 | Cluster 69; 7 n.am.indigenous rows ride along non-canonically; see disposition record |
| `rare_lineage_substrate_isolate` | 1 | Substrate-led genuine rare-lineage cluster (Cluster 86 S. American Indigenous Contemporary Shotgun) |
| `metadata_bucket` | 1 | Uncurated-period metadata residue (Cluster 90 only) |
| `phase_d_bis_curation_gap` | 1 | Cluster surfaces a Phase-D-bis curation gap (Cluster 90 only) |
| `rare_lineage_no_home` | 1 | Cluster reflects rare-lineage scatter with no coherent home (Cluster 114) |

---

## Framing-Audit Operational Observations

This was the **first applied use** of the framing-audit checklist from `gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` § 9.5. Capturing observations on the checklist's operational behavior for the owed OP-amendment write (sub-carry 9.10-B.1 — landing at `agentic_orchestration/operating-procedures/gandalf.md` + `.claude/skills/reincarnated-gandalf-operating-procedure/`).

### Where the checklist surfaced refinement

The checklist's three questions:

1. What load-bearing framing assumption does this label depend on?
2. What evidence in hand could refute that assumption?
3. If refutation exists, refine the label rather than execute as-framed.

**Surfaced refinements in this pass:**

1. **Form-bundling vs prefix-bundling distinction within fantasy named_template space.** Initial draft assumed top-rep name-prefix was the cluster signature. The framing-audit asked "what evidence could refute that?" and looking at all 5 top reps revealed that most named_template clusters are **form-bundled** (one weapon-form across many name-prefixes), with only Cluster 62 + a couple others being prefix-bundled mega-families. This is a substrate-honest emergent structural distinction that the auto-labeler V1 missed and V2 captures.

2. **Modern military hardware "weapon-form" inadequacy.** Initial framing assumed rare-lineage contemporary clusters would be small traditional-weapon pools. The framing-audit on Clusters 23, 31, 44, 71 revealed they're contemporary UAV/missile/SPH/APC pools whose lineage tagging is **geographic-origin** rather than cultural-lineage. The refinement: `modern_military_hardware_pool` cluster_type + `lineage_tag_geographic_not_cultural` flag.

3. **Metadata-bucket signature is not just "large + unknown-period."** Initial assumption was that the metadata-bucket pattern would surface multiple clusters. The framing-audit's "could anything else here be metadata residue?" sweep revealed that the metadata-bucket signature is specifically (a) one dominant lineage, (b) period=unknown, (c) rep canonical_names that are alphanumeric catalog IDs or raw Q-numbers, (d) ≥5,000 rows. Only Cluster 90 met all four. Smaller catalog-residue patterns (Cluster 92, 101, 108, 119) surfaced as `lineage_uncurated` rather than `metadata_bucket`.

4. **Substrate-tagging artifact recognition.** The framing-audit on Cluster 50 (zweihänder tagged contemporary military_modern), Cluster 78 (palstave tagged early_modern), and Cluster 22 (naginata/ji/dao tagged east_asian contemporary) surfaced a class of finding: **the substrate tagging itself contains period/register artifacts that the clustering faithfully captures**. The refinement: `period_tag_likely_metadata_artifact` flag + hand-off notes to elrond for period-canonicalization review.

### Where the checklist returned "no refinement needed"

Routine substrate-honest weapon-family clusters with high lineage purity and rep-consistent form-tokens. Examples: Cluster 5 (Fantasy-Generic Fictional Dagger Family), Cluster 11 (Fantasy-Generic Fictional Sword Family), Cluster 26 (Fantasy-Generic Fictional Staff Named-Item Family), Cluster 73 (European Early-Modern Pistol Family). For these the framing-audit was a quick "lineage-purity + form-coherence sanity-check" pass and produced one-sentence audit notes.

### Where the checklist was ambiguous

1. **Form-bundled vs prefix-bundled threshold (3-of-5).** The auto-labeler used "3-of-5 reps share form-token → form-bundled" / "3-of-5 share prefix → prefix-bundled" / "neither → mixed." This threshold worked for most clusters but a handful sit at the boundary (Cluster 15 starknife; Cluster 42 axe; Cluster 55 longbow; Cluster 60 longbow) where the dominant signal was at 2-of-5 in either dimension. These were handled by fallback labeling but the threshold itself is a judgment call. The OP-amendment write should name this threshold explicitly and surface the boundary cases as Phase E-1.5 sensitivity-sweep priorities.

2. **"Period-tag artifact" vs. "intentional period-tagging".** Cluster 22 (East Asian polearm/blade tagged contemporary) — is this a substrate-curation artifact or a legitimate contemporary catalogue entry of traditional weapon forms? The framing-audit could not adjudicate; I flagged the artifact possibility + hand-off to elrond. The cluster_type defaulted to `weapon_family` rather than `mixed_form_pool` because the form coherence was strong (naginata + ji + dao are all polearms/blades).

3. **Rare-lineage isolate threshold.** Clusters 86 (S. American Indigenous Contemporary Shotgun, N=36, purity 0.9444) and 23 (Arctic Heavy Weapon Systems, N=34) sit at very different ends of "rare-lineage substrate-led cluster": Cluster 86 has form-coherence + lineage-coherence; Cluster 23 has lineage-coherence-via-geographic-tagging but is a heavy-weapon-systems pool. Initially both were classified `rare_lineage_isolate`; the framing-audit reclassified Cluster 23 as `modern_military_hardware_pool` because the dominant identity was the weapon-systems form, not the rare-lineage cultural identity. The OP-amendment write should name this distinction.

### Operational rhythm

For each cluster: ~30-60 seconds. Routine substrate-honest clusters at the fast end (lineage + period + form-coherence sanity-check). Special-case clusters at the slow end (5+ minutes when reps revealed substrate-curation artifacts or cross-form bundling). The checklist's three-question structure was tractable at this pace because most clusters did not surface refinement — the audit was an active *check* rather than an active *redesign*, which is the correct ratio per § 9.5 spirit.

### Recommendation for OP amendment (sub-carry 9.10-B.1)

The framing-audit checklist as drafted in § 9.5 is **operationally sound** but needs four amendments:

1. **Per-cluster output expectation:** explicit "framing_audit_notes" field of 1-3 sentences (this dispatch defined; the OP should standardize).
2. **Form-bundling-vs-prefix-bundling guidance** for named-template substrate work (this dispatch surfaced; the OP should generalize the form-detection heuristic to other named-template contexts).
3. **Substrate-tagging-artifact recognition pattern** as a named refinement category (this dispatch surfaced; the OP should codify "is this substrate honesty or substrate-curation drift?" as the fourth audit question).
4. **Boundary-threshold judgment-call** flag — when the audit is ambiguous, name the boundary explicitly + flag for Phase E-1.5 sensitivity sweep priority (this dispatch surfaced).

The OP-amendment write lands at `agentic_orchestration/operating-procedures/gandalf.md` + `.claude/skills/reincarnated-gandalf-operating-procedure/SKILL.md` per Stream 2 / Skill Creator packaging convention. Non-blocking for further Phase E work; lands before the next Pattern A-deep ratification.

---

## Hand-off Notes for Phase E-2-DB Sub-Dispatch

The downstream Phase E-2-DB sub-dispatch (elrond Pattern-A-light or legolas Pattern-A-light per dispatch § "What knight-rider does after your return") will UPDATE `clusters.label` from the Phase E-2 JSON output. Key inputs:

1. **JSON path:** `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-2-cluster-labels.json`
2. **UPDATE key:** `db_cluster_id` field on each cluster entry maps directly to `clusters.id` (1-125 in SQLite). The `id` field (0-124) is the legolas cluster_id for cross-doc reference and should NOT be used as the UPDATE WHERE clause.
3. **UPDATE column:** `clusters.label` (TEXT). Source: `canonical_label` field from JSON.
4. **Optional UPDATE column:** `clusters.dominant_axes_description` — could be populated with `framing_audit_notes` content for free-text review trail. Not load-bearing; optional.
5. **Schema gap:** the `clusters` table has no `cluster_type` column. If Phase E-2-DB sub-dispatch wants to capture cluster_type, an `ALTER TABLE clusters ADD COLUMN cluster_type TEXT` would be needed (idempotent ADD pattern per MIGRATION.md § Schema changes). If not added, the cluster_type lives in the JSON artifact only — acceptable for Phase E-2 since the JSON is durable and Phase E-3/E-4 can read it directly.
6. **No DB writes from Phase E-2 gandalf dispatch.** Per dispatch "Out of scope": "Do NOT execute UPDATE statements against `clusters.label` from this gandalf dispatch." This summary respects that bound.

### Suggested SQL pattern (for the next sub-dispatch to use)

```sql
BEGIN;
-- Optional schema add for cluster_type (idempotent)
-- ALTER TABLE clusters ADD COLUMN cluster_type TEXT;  -- catch error if exists

UPDATE clusters SET label = ?
WHERE id = ?;
-- one UPDATE per cluster, parameterized from JSON clusters[*]
-- (db_cluster_id, canonical_label) pairs

-- Verification:
SELECT COUNT(*) FROM clusters WHERE label LIKE 'PROVISIONAL:%';
-- expected: 0 (all 125 should be canonical-labeled)

COMMIT;
```

---

## Sub-Carries Documented

| Sub-carry | Owner | Status | Description |
|---|---|---|---|
| **9.11-A** | legolas (or rocket if pipeline architecture) | Queued | Provisional-label-generator code fix in `phase_e1_pipeline.py write_clusters_subsample` — the auto-generated provisional descriptions tokenized weapon_type fields in ways that drift from rep evidence in 47/125 clusters (~38%). Code path needs to honor rep canonical_name form-signal more heavily, or alternatively the provisional descriptions should be marked as "structural-only" (lineage + period + register; no weapon-form guess) so downstream labelers don't inherit drift |
| **9.11-B** | legolas Mode B (dormant) | Queued; dormant | N.am.indigenous substrate expansion — fires if Alternative 2 path (carry 9.10-E) authorized. See `canonical/story/n-am-indigenous-no-cluster-disposition-2026-05-23.md` § 4 for the four empirical triggers |
| **9.11-C** | elrond | Queued | East_asian period_unknown curation gap — Cluster 90's 10,087 rows reveal a Phase-D-bis Step 6.6.c-adjacent curation gap on east_asian rows with `period_unknown`. Non-blocking for Phase E-2 (the cluster is honestly labeled as metadata-bucket). Phase-D-bis follow-on review warranted |
| **9.11-D (new)** | elrond | Queued | Substrate-tagging-artifact review — Clusters 22 (east_asian polearms tagged contemporary), 78 (palstave bronze-age tagged early_modern), 50 (zweihänder/kriegsmesser tagged contemporary military_modern). These are period/register tagging artifacts the clustering faithfully captured. Phase-D-bis Step 6.6.d-style review for cross-period/cross-register tagging drift |
| **9.11-E (new)** | elrond | Queued | Geographic-origin vs cultural-lineage tagging discipline — Cluster 23 (arctic_circumpolar tagging on Russian/Swedish/French missile systems whose lineage IS geographic-origin not arctic-circumpolar culture). The `cultural_lineage_canonical` column needs a tagging-discipline doc or schema clarification (geographic-origin vs cultural-lineage). Non-blocking |
| **9.10-B.1** | gandalf (owed) | Queued | OP amendment write — framing-audit checklist updates per § Framing-Audit Operational Observations § Recommendation. Lands at `agentic_orchestration/operating-procedures/gandalf.md` + `.claude/skills/reincarnated-gandalf-operating-procedure/SKILL.md` |
| **9.10-G** | knight-rider authoring + legolas execution | Queued | Phase E-1.5 sensitivity sweep (per gandalf Gate-2 condition 3). Psutil install preflight (9.10-G.1) folded in. Phase E-2-DB sub-dispatch likely lands first; Phase E-1.5 can fire in parallel |

---

## Gandalf-Internal Observations (Not Canonicalized in This Dispatch)

Per dispatch § "Open questions for gandalf to resolve + document" question 3 — clusters that *might* align with the 13-faction prediction from Earth Meta-Layer / Fate-genre faction architecture (`fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` § 4).

**Faction-architecture-adjacent observation (not a commitment):**

The substrate-honest cluster shapes that emerged map plausibly to several of the 13-faction prediction's likely factions:

- **European medieval/early-modern weapon families** (Cluster 78, 84, 95, 96, 99, 106, 115, 118) → could anchor a "European Knightly" faction
- **East Asian classical/early-modern weapon families** (Cluster 19, 22, 93, 97, 110) → could anchor an "East Asian Traditional" faction
- **Middle Eastern classical/medieval clusters** (Cluster 71, 89, 109, 113, 123, 124) → could anchor a "Middle Eastern" faction
- **S. American Indigenous Contemporary Shotgun isolate** (Cluster 86) → potential micro-faction or sub-faction
- **Fantasy-Generic named-template clusters** (41 clusters) → orthogonal to historical factions; could be "creative/synthetic" register
- **Modern military hardware clusters** (Clusters 23, 31, 44, 71) → orthogonal to traditional factions; modern-warfare register

**These are observations, not commitments.** Per the recognition-validate-commit discipline + dispatch § Open Question 3 directive ("do NOT canonicalize faction commitments in this dispatch (that's a separate canonical-doc question per ADR-002 architectural-approval tier)"), this dispatch does not promote any of these observations to canonical faction declarations. They are flagged here so that future faction-architecture work has the cluster substrate available as design input.

---

## Cross-References

- **Phase E-2 cluster labels (this dispatch's main artifact):** `phase-E-2-cluster-labels.md` + `phase-E-2-cluster-labels.json` (this directory)
- **N.am.indigenous recognition record:** `canonical/story/n-am-indigenous-no-cluster-disposition-2026-05-23.md`
- **Dispatch:** `agentic_orchestration/dispatches/2026-05-23-gandalf-phase-E-2-cluster-labeling.md`
- **Gate-2 findings record:** `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-2-gate-2-findings-record.md`
- **Phase E-1 clusters:** `phase-E-1-clusters.md` (this directory)
- **Phase E-1 axis discovery:** `phase-E-1-axis-discovery.md` (this directory)
- **MIGRATION.md § 4 (native-vs-nearest split):** `MIGRATION.md` (this directory)
- **Frame-revision note:** `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-frame-revision-note.md`
- **Framing-audit checklist (gandalf § 9.5):** `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-kernel-panic-diagnosis.md` § 9.5
- **Discipline #18 (substrate-voting-is-binding):** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- **Discipline #19 (forensic-conclusion-discipline):** Same
- **Recognition-record format precedent:** `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md`
- **Substrate-led discipline:** `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md`
- **Ground-state oracle:** `canonical/00-ground-state.md`

---

**Signed:** gandalf (story-and-design steward), 2026-05-23 post-execution
**Status:** Phase E-2 cluster canonical labeling COMPLETE. Acceptance gates PASSED. Phase E-2-DB sub-dispatch input ready. Phase E-1.5 sensitivity sweep can proceed in parallel.
**Empirical-evidence next-gate:** Gate-2 ratification by jack-ryan DEV-MODE Pattern-A-light on JSON schema + cross-references + hdbscan_native sampling + flag distribution sensibility. If PASS, Phase E-2-DB sub-dispatch fires.
