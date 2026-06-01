# Elrond Phase-0 Consultation — WS1A.Q18 flavor-pool data medium

**Status:** PG-0 verdict; authoritative
**Date:** 2026-06-01
**Author:** elrond (data steward seam)
**Wave:** `WS1A.Q18-flavor-pool-research`
**Phase / phase-gate:** Phase 0 / PG-0
**Authority:** elrond seam authority per hive-mind decision-routing (Matt 2026-05-23 verbatim); dispatched by KR per Matt 2026-06-01 "hand to KR to fire the wave"
**Dispatch:** `agentic_orchestration/dispatches/2026-06-01-elrond-q18-flavor-pool-data-medium-consultation.md`
**Operational sequence:** `agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-operational-sequence.md`

---

## 1. Verdict — recommended medium

**E.γ-prime — JSONL (JSON Lines) for per-row candidate records + a sidecar manifest JSON per sub-agent for narrative metadata; ingested at Phase 4 via pandas → SQLite snapshot for analysis-time joins.**

This is E.γ refined into a concrete format that satisfies the Phase-3-incremental-write constraint cleanly. Not a different family — same family as the listed option (γ); refinement names the file format precisely so KR can lift it into Phase-1 sampler dispatch placeholders without further translation.

No re-routing to gandalf needed. The refinement is within E.γ scope; not E.δ.

---

## 2. Rationale

### Why not E.β (substrate DB extension)

The substrate DB at `data/seasonal_elements/pool.json` holds **locked operational vocabulary** that downstream engine consumers (WS1A.3 per-kit selection; WS1A.4 per-skill flavor judgment) read. The Phase-3 research dataset is **unlocked candidate vocabulary** — pre-curation, pre-vote-count, pre-design-judgment. Mixing the two before sub-phase 5b Matt-ratification would:

- create operational-vs-research confusion at the substrate boundary (which entries are locked? which are exploratory?);
- require schema fields the locked pool doesn't carry (source citation, recognizability score, sampler-track tag, cross-primary contamination flag) — meaning a schema extension fires before the lock fires (cart before horse);
- couple this wave's research data to a cross-seam contract (engine consumes the file; star-lord operates the pipeline) — ADR-004 MIGRATION discipline applies, which is overkill for ephemeral research data;
- pre-commit elrond+star-lord time to migration work that operational sequence § 2 sub-phase 5f explicitly schedules POST-WAVE.

The dispatch itself anticipates this: "even if you recommend E.β, do NOT extend the substrate DB yet." Recommending E.β here would just delay a deferred-to-POST-WAVE step into Phase 0. Not the right shape.

### Why not E.α (Parquet/CSV)

Parquet's wins (columnar compression, schema typing, fast scan over GBs of data) are not load-bearing at ~800 rows. Its costs (binary format that sub-agents cannot author directly; library dependency at every write; awkward inspection by humans during Phase 2 triage) bite.

CSV's wins (universally readable, append-friendly) are real, but CSV's failure modes are sharp here:
- source citations contain commas, quotes, em-dashes, parentheses — CSV quoting is fragile across authoring tools;
- recognizability and contamination fields are richer than flat scalars (contamination flag may need a list of contaminated primaries, not just a boolean);
- multi-line fields (a candidate's "notes" or "rationale-from-source") break naive CSV.

Both Parquet and CSV are a worse fit than JSONL for this scale + this schema shape.

### Why E.γ-prime (JSONL + sidecar manifest)

JSONL gives us:
- **Trivial incremental write** — sub-agents append one JSON object per line as research lands. No file-rewrite, no merge conflict, no transaction boundary. Phase-3 expansion sub-agents (≤6 concurrent fan-out) can each author into their own JSONL file with no coordination overhead.
- **Clean unicode + quoting** — JSON's escape rules handle citations, em-dashes, quoted spell names cleanly.
- **Lossless field shape** — `cross_primary_contamination` is a list of primaries, not a boolean; `source_citations` is a list of (source, locator) pairs, not a flat string; `notes` may be multi-paragraph. JSON handles all of this without quoting fragility.
- **Trivial Phase-4 ingest** — `pd.read_json(path, lines=True)` produces a DataFrame in one line. Multiple JSONL files concatenate by `pd.concat([pd.read_json(p, lines=True) for p in paths])`. Total ingest code: ~3 lines.
- **Human-inspectable** — Phase 2 legolas triage reads the JSONL files directly without tooling; gandalf can sanity-check during PG-1 ratification without ingest pipeline.
- **Discipline #18 compliant** — the math hotspot is at Phase 4 (statistical analysis); the methodology choice at Phase 0 (this consultation) is upstream of execution; the data format does not lock-in a methodology, it preserves all signal for the methodology lock that fires at Phase 4 dispatch authoring.

The sidecar manifest JSON per sub-agent carries qualitative narrative that doesn't fit per-row (per-track yield scores, source-coverage-breadth notes, sub-agent's continue/stop/expand recommendation per primary). Keeps per-row records lean + tabular for stats; keeps narrative captured separately for Phase 2 triage + Phase 5 synthesis consumption.

**Ingest path at Phase 4:** I snapshot the concatenated JSONL into an in-memory SQLite during analysis (or a temp `data.db` at the Phase-4 artifact path) to enable SQL joins for the contamination matrix and the cluster-analysis pre-join. This is internal Phase-4 tooling — no external contract; SQLite is a transient analysis-time materialization, not a substrate extension. The raw JSONL files remain authoritative.

---

## 3. Format spec for Phase 1 sampler outputs (Sampler-A / -B / -C)

KR inserts this verbatim (or near-verbatim) into the Sampler-A/B/C dispatch templates at the `[INSERTED PER ELROND PG-0 MEDIUM DECISION]` placeholders per operational sequence § 9 Appendix A.

### 3.1 Per-row candidate record — JSONL format

**File path per sampler:**
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-A.jsonl`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-B.jsonl`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-C.jsonl`

(Date stamp in directory name resolves to the wave-fire date.)

**One JSON object per line. No outer array. No trailing comma. UTF-8.**

**Schema (per row):**

```json
{
  "candidate": "string — the sub-element / flavor keyword (lowercased; singular form preferred)",
  "primary_element": "string — one of: fire, water, earth, wind, lightning, holy, shadow, physical",
  "track": "string — one of: ARPG, JRPG_isekai, tabletop_myth",
  "source_citations": [
    {
      "source": "string — game/work title (e.g., 'Diablo 4', 'Final Fantasy VII', 'D&D 5e PHB')",
      "locator": "string — skill/spell/affix/passive name OR page reference OR card name (e.g., 'Sorcerer skill: Incinerate', 'Fira spell', 'p. 242 Fire Bolt')",
      "notes": "string — optional; per-citation clarification (e.g., 'category appears in skill tooltip')"
    }
  ],
  "recognizability_score": 1,
  "substrate_type": "string — one of: material, phenomenon, proper_noun, mythological, mechanical_keyword, ailment, other",
  "cross_primary_contamination": ["string — list of OTHER primary elements where this candidate also appears in genre canon; empty list if no contamination"],
  "sampler_notes": "string — optional; per-row sampler observation (e.g., 'recurs across all three Diablo entries; treat as ubiquitous')",
  "row_id": "string — unique identifier; recommended format: <track>-<primary>-<candidate>-<seq> (e.g., 'A-fire-cinder-001')",
  "sample_date": "string — ISO-8601 date the row was authored (e.g., '2026-06-02')"
}
```

**Field-level constraints:**

| Field | Type | Required | Constraint |
|---|---|---|---|
| `candidate` | string | yes | lowercase; singular noun preferred; no leading/trailing whitespace |
| `primary_element` | string | yes | enum: fire / water / earth / wind / lightning / holy / shadow / physical |
| `track` | string | yes | enum: `ARPG` / `JRPG_isekai` / `tabletop_myth` |
| `source_citations` | list | yes | at least 1 entry; each entry has `source` + `locator` (notes optional) |
| `recognizability_score` | int | yes | 1 (niche) / 2 (common) / 3 (ubiquitous) per operational sequence § 9 Appendix A |
| `substrate_type` | string | yes | enum per § 3.1 above |
| `cross_primary_contamination` | list[string] | yes | empty `[]` if no contamination; otherwise list of primary names from the enum |
| `sampler_notes` | string | no | freeform; may be empty string or omitted |
| `row_id` | string | yes | unique within the file; recommended format above |
| `sample_date` | string | yes | ISO-8601 date |

**Authoring discipline (for sampler sub-agents):**

- One row per (candidate × primary × track) triple. If a candidate appears as a flex across multiple primaries WITHIN ONE sampler's research, that's TWO rows (one per primary), each with the other primary listed in `cross_primary_contamination`.
- If the SAME candidate has multiple source citations from within the track's source list, those go into the SAME row's `source_citations` array (not as separate rows). Phase 4 frequency analysis counts citations from the array.
- Append rows as research lands. Do NOT rewrite the file mid-research. JSONL append-only discipline preserves incremental write semantics.
- Validation before handoff: each sampler runs `python -m json.tool` on each line OR `pd.read_json(path, lines=True)` to verify well-formed JSONL.

### 3.2 Sidecar manifest — JSON format

**File path per sampler:**
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-A.manifest.json`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-B.manifest.json`
- `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-C.manifest.json`

**Schema:**

```json
{
  "track": "ARPG | JRPG_isekai | tabletop_myth",
  "sampler_id": "A | B | C",
  "sample_window": {
    "started": "ISO-8601 datetime",
    "completed": "ISO-8601 datetime"
  },
  "row_count": 0,
  "per_primary_yield": {
    "fire": {
      "score": "STRONG | MEDIUM | WEAK | MISALIGNED",
      "row_count": 0,
      "rationale": "string — qualitative sampler narrative on what was found",
      "continue_stop_expand_recommendation": "CONTINUE | STOP | EXPAND",
      "expansion_focus_if_recommended": "string — optional; if EXPAND, what to deepen"
    },
    "water": { },
    "earth": { },
    "wind": { },
    "lightning": { },
    "holy": { },
    "shadow": { },
    "physical": { }
  },
  "source_coverage_breadth": [
    {
      "source": "string — game/work title",
      "yield": "STRONG | MEDIUM | WEAK | MISALIGNED",
      "notes": "string — optional"
    }
  ],
  "substrate_tagging_gaps": "string — narrative on cross-primary contamination patterns observed",
  "seven_vs_eight_signal": "string — sampler's empirical read on whether physical surfaced sub-element vocab in this track, or collapsed",
  "track_alignment_concerns": "string — content/constraint/alignment issues per Matt's framing (operational sequence § 2 Phase 2 item 4)",
  "sampler_summary": "string — top-level narrative paragraph"
}
```

Each per-primary entry in `per_primary_yield` is required (all 8 primaries; if a primary yielded zero, mark `score: "WEAK"` or `"MISALIGNED"` with `row_count: 0`).

### 3.3 Why this two-file shape (per-row + manifest)

The JSONL holds the **structured tabular data** Phase 4 stats consumes — every field is a column. The manifest holds the **qualitative narrative** Phase 2 triage + Phase 5 synthesis consume — yield judgments, coverage notes, expansion recommendations. Separation keeps the row-level data lean (stats-ready) while preserving the irreducibly-qualitative signal Phase 2 + Phase 5 need.

---

## 4. Format spec for Phase 3 expansion sub-agent outputs

**Same JSONL schema as § 3.1.** Same field constraints. The only differences:

- **File path:** `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-<track>-<primary>.jsonl`
  - Examples: `full-ARPG-fire.jsonl`, `full-tabletop_myth-shadow.jsonl`
- **Manifest path:** `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/full-<track>-<primary>.manifest.json`
- **Manifest schema simpler** (only 1 track + 1-2 primaries in scope per expansion sub-agent); the same fields apply but constrained to the sub-agent's PG-1-ratified scope.
- **`row_id` format extends to** `<track>-<primary>-<candidate>-EXP-<seq>` so Phase 4 can join expansion rows to Phase 1 sample rows on `(track, primary, candidate)` and detect candidates surfaced ONLY in expansion (signal of depth-yield).
- **Suggested_ranking field added per row** (per operational sequence § 2 Phase 3 deliverable list item: "Suggested ranking within primary"):

```json
{
  "suggested_ranking_within_primary": 1
}
```

Integer; 1 = strongest per expansion sub-agent's read; ascending = weaker. Optional; sub-agent may omit if ranking is not meaningful for the surfaced candidates.

**Discipline:** expansion sub-agents authored AFTER PG-1; they read the relevant `sample-<X>.jsonl` from Phase 1 first to avoid duplicate work (re-citing candidates already surfaced) — but they DO emit fresh rows for any candidate they re-surface, since expansion-sub-agent citations add to the candidate's source-citation count (Phase 4 frequency analysis sums across all rows, both Phase 1 and Phase 3, on `(track, primary, candidate)`).

---

## 5. Phase 4 ingest path (elrond setup notes)

Phase-4 analysis dispatch (not this dispatch; called out per dispatch § 4 item 5 optional notes):

**Tooling I'll prep ahead of Phase 4:**

- A small ingest script at `agentic_orchestration/research/scripts/q18_flavor_ingest.py` (authored as Phase-4 dispatch fires; NOT authored now) that:
  1. Reads all `sample-*.jsonl` + `full-*.jsonl` under the dated directory
  2. Concatenates into a single `pd.DataFrame`
  3. Validates schema (every row has required fields; enums respected)
  4. Materializes a transient SQLite at `agentic_orchestration/elrond/analysis/q18_flavor_candidates_2026-06-XX.db` with two tables: `candidates` (per-row) and `manifests` (per-sub-agent)
  5. Emits a small ingest-summary JSON noting row count, per-primary counts, per-track counts, validation issues (if any)
- Statistical analysis notebook at `agentic_orchestration/elrond/analysis/q18_flavor_stats_2026-06-XX.ipynb` running:
  1. Per-primary candidate frequency (weighted by track + recognizability)
  2. Cross-primary contamination matrix (from `cross_primary_contamination` fields; symmetric on `(primary_a, primary_b)`)
  3. Cluster analysis per primary (substrate_type clusters + candidate-keyword embedding clusters if useful)
  4. Cardinality recommendations per primary (empirically-supported floor given survived candidate count + citation count + cross-source agreement)
  5. Track-source weighting validation (track contribution counts; balance audit)
  6. 7-vs-8 empirical answer (does physical candidate distribution match the structure of rotating primaries' distributions, or collapse?)
  7. Per-primary statistical confidence (sparse-yield primaries get explicit confidence-degradation naming per operational sequence § 7 risk F-3)

**Methodology lock for Phase 4 (Discipline #18 spirit applied):**

The Phase 4 dispatch should specify:
- **Cluster method:** for the candidate-keyword embedding clusters, HDBSCAN (density-based; tolerates noise; doesn't require k upfront) — but a low-yield primary may not have enough candidates for clustering at all; analyze substrate_type clusters first, then attempt keyword clustering only where candidate count ≥ 8.
- **Frequency weighting scheme:** weight per candidate = `sum(recognizability_score) across all citations` — NOT `count(rows)` which would over-weight one row with many citations. Phase 1 + Phase 3 rows combine.
- **Contamination matrix construction:** symmetric pair count; primary-A↔primary-B cell = count of candidates with both A and B in their flex set (across all rows for that candidate).
- **Cardinality floor recommendation rule:** for each primary, the empirically-supported floor = count of candidates with citation-weighted score ≥ threshold T (T calibrated against existing pool entries that survived Matt's d1_status filter — substrate-led calibration). T is locked at Phase-4 dispatch authoring time per Discipline #18.
- **Acceptance criteria upfront** (per Discipline #18 practical rule 3): variance threshold on bootstrap-stability of cluster assignments; minimum agreement across 3 tracks for "high-confidence" candidate classification; explicit per-primary confidence-degradation naming for sparse-yield primaries.

This is captured for the Phase-4 dispatch authoring; not the responsibility of THIS Phase-0 consultation. Noting it here so KR + gandalf have visibility into what Phase-4 dispatch needs.

---

## 6. F-6 contingency note (operational sequence § 7)

**Read:** F-6 contingency unlikely to fire. Data shape is solidly quantitative-amenable.

The risk F-6 ("Phase 4 data shape too qualitative for statistical analysis") would fire if the captured signal were predominantly narrative judgment (e.g., "this keyword feels right" without citation-anchored evidence) or if the recognizability scoring were too coarse to discriminate. The schema above forces every row to anchor on (a) source citations (counted), (b) recognizability score (discrete 1/2/3 — supports frequency distribution + weighted aggregation), (c) substrate_type enum (supports cluster analysis), and (d) cross-primary contamination as a structured list (supports contamination matrix).

All four Phase-4 deliverables (frequency / contamination matrix / cluster analysis / cardinality recommendations) have explicit fields that feed them.

The condition that WOULD trigger F-6 in this format: if Phase 1 samplers return rows where `source_citations` is empty or stuffed with hand-wave entries ("multiple sources cite this; see various"). Mitigation: the schema requires at least 1 citation with `source` + `locator`; KR's Phase-1 dispatch wording can reinforce "candidates without specific citations are dropped at sampler-self-validation." This pushes the burden of citation discipline upstream to where it's easiest to enforce.

**Backup plan if F-6 fires anyway:** the Phase 4 dispatch retains the operational-sequence § 2 Phase 4 contingency path — collapse to "data-shape verification + cross-source agreement audit." Same dataset format supports it (just run lighter aggregation: count rows per primary; count distinct sources per primary; flag primaries below confidence threshold). The medium choice does NOT bottleneck this fallback.

**Verdict:** F-6 risk is LOW under E.γ-prime; the format actively guards against the failure mode by forcing structured citation per row.

---

## 7. Cross-seam contract change check (Principle 6)

**Answer:** NO cross-seam contract change in THIS consultation.

The chosen medium (JSONL files under `agentic_orchestration/legolas/research/`) lives entirely within the orchestration meta-repo's research surface; it does NOT touch:
- engine substrate (`data/seasonal_elements/pool.json`) — preserved as-is
- engine telemetry DB (star-lord-owned; read-only)
- loadout app data (drax-owned; out of scope)
- any cross-repo file

**Round-trip:** not applicable; no contract change.

Sub-phase 5f POST-WAVE operational migration dispatch is the cross-seam contract change (pool.json extension); that fires later under standard ADR-004 MIGRATION discipline. Not this wave's scope.

---

## 8. Summary for KR Phase-1 dispatch insertion

**TL;DR for KR consumption:**

- Medium: **E.γ-prime — JSONL per-row + sidecar manifest JSON.**
- Phase 1 sampler outputs: `legolas/research/element-flavor-mapping-2026-06-01/sample-<A|B|C>.jsonl` + matching `.manifest.json` per § 3.1 + § 3.2.
- Phase 3 expansion outputs: `legolas/research/element-flavor-mapping-2026-06-01/full-<track>-<primary>.jsonl` + matching `.manifest.json` per § 4.
- Per-row schema: 10 required fields enumerated in § 3.1 with enum constraints + field types.
- Per-manifest schema: per-track yield judgments + per-primary continue/stop/expand recommendations + qualitative summary per § 3.2.
- Validation: each sampler runs `pd.read_json(path, lines=True)` (or equivalent JSONL validator) before handoff.
- F-6 risk: LOW under this format; structured citations prevent the qualitative-collapse failure mode.

**KR Phase-1 dispatch placeholder text** (drop-in replacement for `[INSERTED PER ELROND PG-0 MEDIUM DECISION]` per operational sequence § 9 Appendix A):

> **Output format:** Author per-candidate rows as JSON Lines (JSONL) at `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-<A|B|C>.jsonl` (one JSON object per line; no outer array). Per-row schema per elrond Phase-0 consultation § 3.1 (required fields: `candidate`, `primary_element`, `track`, `source_citations`, `recognizability_score`, `substrate_type`, `cross_primary_contamination`, `row_id`, `sample_date`; optional: `sampler_notes`). Author qualitative narrative + per-primary yield judgments at `agentic_orchestration/legolas/research/element-flavor-mapping-2026-06-01/sample-<A|B|C>.manifest.json` per elrond Phase-0 consultation § 3.2. Reference the Phase-0 consultation note at `agentic_orchestration/elrond/consultations/2026-06-01-q18-flavor-pool-data-medium.md` for full schema spec. Validate JSONL well-formedness before handoff (`pd.read_json(path, lines=True)` succeeds).

KR may inline the per-row schema directly in the sampler dispatch if preferred over indirection through this consultation note.

---

## 9. Disciplines composed

- **#18 (methodology-before-execution at math hotspot)** — Phase 4 is the math hotspot; this consultation is the upstream gate. Data format chosen does NOT lock methodology; preserves full signal for Phase-4 methodology lock (§ 5 above).
- **#41 (substrate-led)** — the candidate vocabulary IS the substrate; the format faithfully captures what samplers find without imposing pre-emptive structure (substrate_type enum is wide enough to absorb variation; `cross_primary_contamination` is a list not a flag to avoid binary-ization of flex behavior).
- **Schema-versioning discipline (elrond OP § "Schema design principles" — versioned)** — JSONL schema as documented in § 3.1 is v1.0; any future schema change goes into a v1.1 amendment with explicit additive-vs-breaking distinction.
- **Schema-versioning discipline (elrond OP § "Schema design principles" — source-anchored)** — every row carries `source_citations` + `sample_date` + `track`; full source traceability per row.
- **Schema-versioning discipline (elrond OP § "Schema design principles" — tagged not encoded)** — `substrate_type` as an enum field, `cross_primary_contamination` as a list field; no semantic packing into compound IDs.

---

## 10. Acceptance checklist (for KR)

- [x] Medium choice named explicitly: **E.γ-prime (JSONL + sidecar manifest JSON; pandas → SQLite at Phase 4)**
- [x] Rationale addressing Phase-3 incremental writes + Phase-4 statistical analysis constraint
- [x] Format spec for Phase 1 sampler outputs (per-row JSONL schema § 3.1 + sidecar manifest JSON schema § 3.2)
- [x] Format spec for Phase 3 expansion sub-agent outputs (§ 4)
- [x] Phase 4 ingest path notes for elrond's downstream prep (§ 5)
- [x] F-6 contingency note (§ 6)
- [x] Cross-seam contract change check (§ 7 — NONE in this consultation)
- [x] KR placeholder-replacement text drafted (§ 8)
- [ ] Wave-state file `decision log` row appended by KR with elrond's PG-0 verdict + this artifact path
- [ ] Phase-1 sampler dispatches authored by KR with § 3.1 + § 3.2 schemas inserted
- [ ] Jack-ryan Gate-1 routed on Phase-1 sampler dispatches before firing Phase 1

---

## 11. Cross-references

- **Dispatch this fulfills:** `agentic_orchestration/dispatches/2026-06-01-elrond-q18-flavor-pool-data-medium-consultation.md`
- **Operational sequence:** `agentic_orchestration/gandalf/notes/2026-06-01-q18-flavor-pool-research-operational-sequence.md`
- **Wave-state:** `agentic_orchestration/cycle-15-ws1a-q18-flavor-pool-research/wave-state.md`
- **Wave-open dispatch:** `agentic_orchestration/dispatches/2026-06-01-cycle-15-ws1a-q18-flavor-pool-research-wave-open.md`
- **Existing substrate (NOT extended here):** `~/Games/reincarnated-engine/data/seasonal_elements/pool.json` + `~/Games/reincarnated-engine/config/elements.yaml`
- **Discipline #18:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 18 (math-hotspot methodology consultation)
- **Elrond OP:** `agentic_orchestration/operating-procedures/elrond.md`

---

**End of Phase-0 consultation.**
