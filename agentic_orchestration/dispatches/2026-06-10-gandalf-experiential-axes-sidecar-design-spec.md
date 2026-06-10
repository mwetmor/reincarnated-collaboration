# Design-Spec: experiential-axes JSON sidecar emit

> **STATUS:** DESIGN-SPEC (load-bearing as of 2026-06-10) — Path A critical-path unblock for BLOCK-WS1-A per Matt 2026-06-10 direct direction
>
> **Type:** Design-spec-as-math handoff (Discipline #18 architecture) — gandalf authors the schema + emit shape; gamora (primary) + rocket (consulting) implement engine-side emit.

**Date:** 2026-06-10
**Author:** gandalf (story-and-design steward)
**Addressee:** gamora (engine simulation + spirit-guide seam — owns `simulation/`, `spirit_guide/`); rocket consulting (foundation registry composition)
**Authority:** Matt 2026-06-10 direct direction ("Highest-leverage next-action: gandalf authors 2 Path A JSON sidecar design-specs (substrate-registry + experiential-axes) NOW. Direct critical-path unblock for WS1 → WS3.2-5 → vertical-slice spike chain.") composed with Sam Gate-1 BLOCK-WS1-A finding (2026-06-10) + Matt earlier ratification of Path A per DH WS3.1 routing memo § 5.

**Critical-path framing:** this design-spec → gamora implements emit → engine pushes → PC pulls → BLOCK-WS1-A resolves → WS1 fires (mantis kit-corpus ingestion to UE DataTables for `DT_ExperientialAxis`) → WS3.2-5 + vertical-slice spike unlock.

**Companion design-spec:** `agentic_orchestration/dispatches/2026-06-10-gandalf-substrate-registry-sidecar-design-spec.md` (rocket-addressed; co-fires)

**Source-of-truth canonical:**
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 1.8 multi-axis experiential architecture (iter 4 → iter 6 refined; iter 8 PROPOSED-PLAYTEST-PENDING for Activity-Format)
- Companion reference: `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (8 BC axes; substrate-vector cheatsheet; compose-or-extend relationship per § 6 below)

**Downstream consumer:** `agentic_orchestration/dispatches/2026-06-10-david-h-ws1-data-layer-kit-corpus-ingestion-commission.md` (mantis WS1 Phase 1 → UE `DT_ExperientialAxis` DataTable via db-lyon `fill_datatable_from_json`)

---

## 0. TL;DR

Emit a machine-readable JSON sidecar of experiential-axis architecture per `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 1.8 (multi-axis decomposition) + § 3.5 (per-cell experiential-axis coordinates as cell schema fields). **Expected row count: 7 axes** at canonical-lock (sam Gate-1 WARN-on-count requesting numeral; gandalf surfaces here). Discipline #40 scaffold flag: 1 of 7 (Activity-Format) is PROPOSED-PLAYTEST-PENDING per hypothesis-flow iter 8; sidecar emits axis as `proposed_playtest_pending` status. Emit shape: top-level dict with `schema_version` + `emission_timestamp` + `source_canonical_cite` + `axes` (array of 7 axis records). Output path: engine-internal canonical library emit → engine-repo staging path → push to origin → PC pull at next session-start.

---

## 1. Seam ownership recommendation

**Recommendation: gamora primary; rocket consulting; canonical sidecar lives in engine canonical library alongside substrate-registry sidecar.**

**Reasoning:**
- The experiential axes are the **player-names-experience layer** of pattern-library cells (per hypothesis-flow § 1.1 designer-writes-substrate / player-names-experience principle). They scaffold the SIMULATION-validation surface: per-cell experiential predictions (Bossing score / Speedfarming score / Push score / etc.) get validated against simulated combat outcomes + (downstream) playtest.
- Per hypothesis-flow § 1.8 + § 3.5, experiential-axis coordinates are predictions cells make ABOUT simulated behavior. Gamora's simulation seam owns the validation half of this loop (cells predict → simulation evaluates → playtest finalizes). So gamora owns the axis-catalogue emit as well — the catalogue is the math that simulation will score against.
- Rocket-consulting because the axes COMPOSE with substrate-registry families (e.g., target-pattern-bossing-score correlates with substrate § 1.5 skill geometry palette + § 1.6 skill-tree position + scaling-pattern-per-tier). Cross-seam consultation per Discipline #18 mathematical-layer routing.
- Star-lord NOT primary — telemetry seam consumes axis scores at output but does not OWN the axis catalogue.

**Alternate consideration (rejected):** rocket sole ownership. Rejected because cells predict experiential scores ABOUT generated kits; the prediction-validation loop runs through gamora simulation primarily (B14.5 V1 primary loop pattern composes with axis-prediction validation). Rocket emits substrate-registry (what gets generated); gamora emits experiential-axes (what we predict the generated thing produces in player experience).

---

## 2. JSON schema (the math)

Per Discipline #1 (math-before-code), the schema IS the math of the sidecar. Specify before emit code lands.

### 2.1 Top-level structure

```json
{
  "schema_version": "1.0.0",
  "emission_timestamp": "2026-06-10T00:00:00Z",
  "source_canonical_cite": "canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md",
  "source_canonical_status": "CURRENT (iter 6 lock; iter 8 PROPOSED-PLAYTEST-PENDING for Activity-Format)",
  "source_canonical_date": "2026-05-31",
  "source_canonical_section": "1.8 + 3.5",
  "expected_axis_count": 7,
  "axes": [
    { /* axis record per § 2.2 below */ },
    /* ... 6 more ... */
  ]
}
```

**Why top-level dict (not bare array):** identical reasoning to substrate-registry sidecar — `fill_datatable_from_json` ingest compatibility + provenance preservation + semver discipline. Mantis ingest pattern is consistent across both sidecars for sam Gate-2 verification simplicity.

### 2.2 Axis record schema

Each of the 7 axis records carries this shape:

```json
{
  "axis_id": "target_pattern",
  "axis_section": "1.8.1",
  "axis_display_name": "Target-Pattern axis",
  "axis_type": "identity",
  "axis_status": "locked",
  "value_count": 2,
  "values": [
    {
      "value_id": "bossing",
      "value_display_name": "Bossing",
      "operational_definition": "Single-strong-high-quality targets; combat optimization for boss-fight encounters",
      "cell_score_field": "target_pattern_bossing_score",
      "score_range": "0-10 continuous"
    },
    {
      "value_id": "speedfarming",
      "value_display_name": "Speedfarming",
      "operational_definition": "Many-weak-low-quality targets; combat optimization for clear-speed encounters",
      "cell_score_field": "target_pattern_speedfarming_score",
      "score_range": "0-10 continuous"
    }
  ],
  "sub_axes": [],
  "axis_treatment": "Specialize-and-differentiate; per-cell prefer dominance pattern; cells declare axis dominance",
  "viability_threshold": null,
  "removed_in_iter_6": false,
  "proposed_playtest_pending": false,
  "composition_with_bc_axes": "Composes with BC Axis 1 (engagement profile) + Axis 3 (damage tempo); single-target tempo + boss-engagement profile correlates with Bossing identity"
}
```

### 2.3 Field-by-field semantics

| Field | Type | Required | Semantics |
|---|---|---|---|
| `axis_id` | string | YES | Stable snake_case identifier; used as `DT_ExperientialAxis` row key. Drawn from canonical § 1.8 (e.g., `progression_stage`, `target_pattern`, `depth_breadth`, `activity_format`, `loot_focus`, `maxroll_5axis`, `survivability_playability`) |
| `axis_section` | string | YES | Canonical-doc section number (`1.8.1` for the three primary axes; `1.8.4` for cell-shape; etc.); enables bidirectional reference auditing |
| `axis_display_name` | string | YES | Human-readable name (e.g., `Target-Pattern axis`) |
| `axis_type` | enum string | YES | `identity` / `viability` / `sub` / `progression_stage_hypothesis_pending`. Per § 1.8.2 axis-type taxonomy. Mode (`mode`) REMOVED per iter 6 — not emitted. |
| `axis_status` | enum string | YES | `locked` / `proposed_playtest_pending` / `hypothesis_pending`. Per canonical doc iter-state — locked for Target-Pattern + Depth-vs-Breadth + Survivability + Playability + Loot-Focus + Maxroll; proposed_playtest_pending for Activity-Format (per § 1.8.7 iter 8); hypothesis_pending for Progression-Stage (per § 1.8.5 leveling-as-viability hypothesis) |
| `value_count` | int OR null | YES | Count of axis values where canonical specifies (e.g., 2 for Target-Pattern: Bossing/Speedfarming; 2 for Depth-vs-Breadth: Push/Generalist; 3 for Progression-Stage: Leveling/League_Starter/End_Game). `null` when canonical defers (e.g., Activity-Format pending player-input map architecture lock) |
| `values` | array | YES | Array of value records per § 2.4. When `value_count` is null, array may be empty `[]` (shape stability) OR contain working enumeration per § 1.8.7 (`boss_rich` / `mob_dense` / `currency_rich` / `magic_find_rich` / `anti_faction_rich` / `mixed` / `tier_scaling_high` / `tier_scaling_broad` for Activity-Format scaffold). Working enumeration carries `value_status: "proposed_playtest_pending"` per Discipline #40. |
| `sub_axes` | array | NO | Empty array `[]` for non-sub-axis-carrying axes; populated with sub-axis records for axes that carry sub-axes (e.g., Loot-Focus is itself a sub-axis WITHIN Target-Pattern Speedfarming; relationship preserved here) |
| `axis_treatment` | string | YES | Per-axis treatment description per § 1.8.2 (e.g., "Specialize-and-differentiate; per-cell prefer dominance pattern" for identity; "Universal-adequate-score; gates per minimum threshold" for viability; "Within-axis sub-classification" for sub) |
| `viability_threshold` | float OR null | YES | For viability axes, the threshold score below which cells fail viability (e.g., 5.0 default; canonical defers exact threshold to playtest calibration); null for non-viability axes |
| `removed_in_iter_6` | boolean | YES | True ONLY for Mode axis (per § 1.8 iter 6 amendment). Mode axis is NOT emitted — this flag preserves the removal record. Implementation note: 7 emitted axes exclude Mode; Mode is documented as historical record outside the sidecar |
| `proposed_playtest_pending` | boolean | YES | True for Activity-Format axis (per § 1.8.7 iter 8 PROPOSED architecture status); false for the other 6 |
| `composition_with_bc_axes` | string | NO | Description of how this axis composes with the 8 BC axes per `qd-engine-bc-axes-lock-2026-05-20.md`; surfaces compose-vs-extend relationship per § 6 below |

### 2.4 Value record schema (for `values` array entries)

```json
{
  "value_id": "bossing",
  "value_display_name": "Bossing",
  "operational_definition": "Single-strong-high-quality targets; combat optimization for boss-fight encounters",
  "cell_score_field": "target_pattern_bossing_score",
  "score_range": "0-10 continuous",
  "value_status": "locked"
}
```

| Field | Type | Required | Semantics |
|---|---|---|---|
| `value_id` | string | YES | snake_case identifier; stable within axis |
| `value_display_name` | string | YES | Player-facing label (e.g., `Bossing` / `Speedfarming` / `Push` / `Generalist`) |
| `operational_definition` | string | YES | Operational definition per canonical § 1.8.1 table (e.g., "Single-strong-high-quality targets") |
| `cell_score_field` | string | YES | The per-cell-schema field name where this value's score lives (e.g., `target_pattern_bossing_score` per hypothesis-flow § 3.5); enables bidirectional schema-field ↔ axis-value linking |
| `score_range` | string | YES | Score-range description (e.g., `0-10 continuous`; `enum: Leveling / League_Starter / End_Game`) |
| `value_status` | enum string | YES | `locked` / `proposed_playtest_pending` / `hypothesis_pending`. Per-value status (may differ from axis-level status; e.g., Activity-Format axis is `proposed_playtest_pending` and ALL its 8 working values are `proposed_playtest_pending`) |

### 2.5 Identifier convention summary

- Identifiers: snake_case, lowercase (matches substrate-registry sidecar convention)
- Section numbers: dotted decimal (`1.8.1`, `1.8.2`, etc.)
- Schema version: semver (`1.0.0` for first emit)
- Timestamps: ISO-8601 UTC
- Cross-sidecar consistency: `axis_id` + `value_id` namespace MUST NOT collide with substrate-registry `family_id` + `primitive_id` namespace (separate `DT_PrimitiveFamily` vs `DT_ExperientialAxis` tables enforce this; row keys are independently scoped)

---

## 3. Expected axis count: 7 (load-bearing; Sam Gate-1 WARN response)

**Per Sam Gate-1 § 84 + § 159:** "DT_ExperientialAxis=TBD (per hypothesis-flow § 1.8 axis count) ... ~4-7 axes per the multi-axis architecture" — gandalf surfaces the canonical count.

**Enumeration per canonical § 1.8 + § 3.5:**

| # | Axis | § | Type | Status |
|---|---|---|---|---|
| 1 | Progression-Stage axis | 1.8.1 | identity_or_viability_per_1_8_5_hypothesis | `hypothesis_pending` (per § 1.8.5) |
| 2 | Target-Pattern axis | 1.8.1 | identity | `locked` |
| 3 | Depth-vs-Breadth axis | 1.8.1 | identity | `locked` |
| 4 | Activity-Format axis | 1.8.1 + 1.8.7 | identity | `proposed_playtest_pending` (per iter 8) |
| 5 | Loot-Focus sub-axis | 1.8.1 + 3.5 | sub (within Speedfarming under Target-Pattern) | `locked` |
| 6 | Maxroll 5-axis structured rating | 1.8.1 + 3.5 | identity (Bossing/Speed/Push) + viability (Survivability/Playability) cross-cutting | `locked` (as continuous-prediction per § 3.5; treated as bundle) |
| 7 | Survivability + Playability (Maxroll-derived) | 1.8.2 + 3.5 | viability | `locked` |

**Count: 7.** This is the canonical-derived numeral that resolves Sam Gate-1 § 84 TBD.

**Mode axis NOT emitted** (per § 1.8 iter 6 amendment — REMOVED; mode is player-session-level choice, not kit-axis property).

### 3.1 Discipline #40 scaffold disposition

**3 of 7 axes carry non-locked status:**

| Axis | Scaffold flag | Resolves when |
|---|---|---|
| Progression-Stage | `hypothesis_pending` per § 1.8.5 leveling-as-viability hypothesis | Playtest evidence validates or refutes Leveling-as-viability treatment |
| Activity-Format | `proposed_playtest_pending` per § 1.8.7 iter 8 player-input procedural map architecture | Player-input map architecture commits canonically + playtest validation |
| Maxroll 5-axis | `locked` per § 3.5 as continuous-prediction; emit as single bundle row OR decompose into 5 separate rows per gamora discretion | If decomposed: 11 emitted rows; if bundled: 7 emitted rows. **Gandalf recommendation: emit as 1 bundle row per § 3.5 cell-schema treatment** (cells carry `maxroll_5axis_prediction` as a single dict field). |

**Sidecar carries `axis_status` per row** flagging scaffold state explicitly. Discipline #40 honored: scaffolds are EXPLICIT not silent.

**Possible row count variants per gamora seam-owner judgment:**

- **7 rows** (gandalf default; Maxroll 5-axis as single bundle row per § 3.5 cell-schema treatment)
- **11 rows** (Maxroll 5-axis decomposed into 5 atomic axis rows: Bossing-Speed-Push-Survivability-Playability)
- **6 rows** (Mode-only-counted-as-removed; explicit row count after Mode-axis removal historical record)

**Gamora's call.** Document in emit which variant chose + reasoning. Sam Gate-2 verifies the EMITTED count against the COMMITTED count per criterion #3 sharpening (Sam Gate-1 WARN response: explicit numerals before mantis runs).

---

## 4. Output path target

**Recommended emission path (engine-side):**

```
~/Games/reincarnated-engine/src/reincarnated/canonical/sidecars/experiential_axes_v1.json
```

**Reasoning:** identical to substrate-registry sidecar — engine-repo-resident, single-source-of-truth, sub-directory navigability, semver discipline, Path A PC clone pull. The two sidecars co-locate in `canonical/sidecars/`.

**Mantis WS1 ingestion path resolution (PC-side):**

```
C:\dev\reincarnated-engine\src\reincarnated\canonical\sidecars\experiential_axes_v1.json
```

---

## 5. Emission trigger

**Recommendation: one-shot CLI command + manual re-fire on canonical doc update.**

```bash
# From engine repo root
python -m reincarnated.canonical.sidecars.emit_experiential_axes
```

**Reasoning:** identical to substrate-registry sidecar — canonical-doc-update-cadence emit triggers manual re-fire; one-shot CLI; engine push to origin per Matt-authorized push pattern. Consistent emission discipline across both sidecars.

**CLI behavior:**
1. Reads canonical doc (path: `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md`) § 1.8 + § 3.5 for axis content
2. Constructs the 7 axis records per § 2.2 + § 3 above
3. Composes the top-level JSON dict per § 2.1
4. Writes to `canonical/sidecars/experiential_axes_v1.json`
5. Prints emit summary: axis count + per-axis status flag + sidecar SHA

**Discipline #11 (empirical inspection):** gamora reads canonical doc § 1.8 + § 3.5 as authoritative; does not designer-impose. Per-value `operational_definition` text drawn from canonical tables directly. If canonical doc updates (e.g., Activity-Format values stabilize when player-input architecture commits), gamora re-emits with sidecar version bump (v1.0.0 → v1.1.0 minor for additive value enumeration; v2.0.0 major if axis-type changes).

---

## 6. Composition with substrate-vector cheatsheet (8 BC axes)

**Per Sam Gate-1 surfacing + gandalf design discipline:** experiential axes compose with the 8 BC axes from `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`. The relationship:

**BC axes (8) are mechanical-substrate substrate-vectors:** engagement profile / damage geometry / proxy density / control density / damage tempo / damage amplitude variance / defensive profile / resource economy. Substrate-vote at generation layer; designer-writes-substrate per Disc #41.

**Experiential axes (7) are player-experience predictions:** Target-Pattern / Depth-vs-Breadth / Progression-Stage / Activity-Format / Loot-Focus / Maxroll 5-axis / Survivability+Playability. Cells PREDICT these scores; simulation + playtest VALIDATE; player NAMES the experience at output.

**Compose-vs-extend disposition:**

- Experiential axes do NOT extend BC axes. They occupy a separate layer of the cell schema (per hypothesis-flow § 3.4 substrate-axis coordinates VS § 3.5 experiential-axis coordinates — distinct schema sections).
- Experiential axes COMPOSE WITH BC axes. Each cell carries BOTH a `bc_axis_signature` 8-vector (§ 3.4) AND experiential-axis prediction fields (§ 3.5). The substrate-vector determines mechanical character; the experiential-axes predict the player-experience consequence.
- The `composition_with_bc_axes` field in each axis record (§ 2.3) surfaces SPECIFIC compositional relationships (e.g., Target-Pattern Bossing composes with BC Axis 1 + Axis 3; Depth-vs-Breadth composes with BC Axis 4 + Axis 6; etc.).

**Why this matters operationally:** mantis at WS1 ingests both `DT_PrimitiveFamily` (substrate-registry families including geometry palette per § 1.5) AND `DT_ExperientialAxis` (experiential axes per this sidecar) AND downstream `DT_Kit` (per-kit substrate-vector + experiential-axis prediction). UE downstream consumers see both layers; player-facing surfaces (cosmograph side-panel per atomic-substrate-registry § 6) display experiential predictions alongside substrate-vector for player legibility.

**Discipline #41 substrate-led:** the compose-vs-extend disposition is NOT designer-imposed taxonomy. It reflects the canonical architecture (substrate-axis layer is generation-targetable per § 1.1; experiential-axis layer is generation-targetable as PREDICTIONS per § 1.1; the layers are orthogonal coordinates in cell space).

---

## 7. Composition with WS1 ingestion

**Mantis WS1 Phase 1 step 4:** `db-lyon fill_datatable_from_json` with source JSON path → `DT_ExperientialAxis` UE DataTable.

**Composition:**
- WS1 commission `DT_ExperientialAxis` row schema → mantis authors UE C++ struct matching this JSON axis record schema § 2.2 (one row per axis; `axis_id` as row key)
- `fill_datatable_from_json` consumes the `axes` array within the top-level dict — same pattern as substrate-registry sidecar
- `axis_status` field flags `locked` / `hypothesis_pending` / `proposed_playtest_pending` so DT consumers branch per-row UI / behavior
- `values` array preserved per row (potentially empty `[]` for pure-status-flagging rows; populated for value-carrying rows) so UE struct schema is stable

**Schema-version composition:** sidecar v1.0.0 → UE struct v1; downstream evolution per ADR-004 cross-seam-contract treatment. Activity-Format value enumeration finalization → minor bump v1.0.0 → v1.1.0 (additive values; backward compatible).

**Discipline #11 + Principle 3 cross-seam impact:** gamora emits → mantis ingests across host boundary. Same round-trip pattern as substrate-registry sidecar.

---

## 8. Acceptance criteria

Per Discipline #1 (math-before-code) + Discipline #11 (empirical inspection):

1. **Axis count match (Sam Gate-1 § 84 + § 159 sharpening):** sidecar `axes` array length matches gamora-committed count (7 per gandalf default; 11 if Maxroll decomposed; document in emit; resolves Sam Gate-1 TBD)
2. **Axis-id stability:** all axis `axis_id` values are unique snake_case identifiers; no collisions; ordered matching canonical § 1.8 + § 3.5 enumeration
3. **Axis-type accuracy:** each axis carries correct `axis_type` per § 1.8.2 taxonomy; Mode-axis NOT emitted (removed_in_iter_6 historical record only)
4. **Axis-status accuracy:** Target-Pattern + Depth-vs-Breadth + Loot-Focus + Maxroll bundle + Survivability+Playability carry `locked`; Activity-Format carries `proposed_playtest_pending`; Progression-Stage carries `hypothesis_pending`
5. **Cell-schema-field linkage:** each value record's `cell_score_field` matches an existing field name in hypothesis-flow § 3.5 cell schema (e.g., `target_pattern_bossing_score`, `target_pattern_speedfarming_score`, `depth_breadth_push_score`, `depth_breadth_generalist_score`, `survivability_score`, `playability_score`, `leveling_viability_score`, `progression_stage_target`, `progression_stage_classification`, `activity_format_target`, `loot_focus_sub_axis`, `maxroll_5axis_prediction`)
6. **Compose-with-BC-axes annotation:** each axis carries `composition_with_bc_axes` field describing relationship to relevant BC axes per § 6 above
7. **Discipline #40 scaffold flagging explicit:** 3 of 7 axes (Progression-Stage / Activity-Format / Maxroll-as-bundle-decision) carry non-locked status flags surfaced in `axis_status` field
8. **Provenance fields populated:** `schema_version`, `emission_timestamp`, `source_canonical_cite`, `source_canonical_status`, `source_canonical_date`, `source_canonical_section` all non-null
9. **Canonical-doc cross-reference auditable:** for each axis, `axis_section` matches canonical doc § heading
10. **Smoke-test pass:** `python -c "import json; d = json.load(open('experiential_axes_v1.json')); assert d['expected_axis_count'] == len(d['axes']); print('PASS')"` returns PASS
11. **No designer-imposed content (Discipline #41 substrate-led):** all axis content drawn from canonical sources; no fields added that lack canonical anchor
12. **Cross-sidecar id-namespace independence:** no `axis_id` collides with substrate-registry `family_id`; separate DataTable scopes enforce but explicit naming discipline prevents downstream consumer confusion

**Round-trip discipline (Principle 6 cross-seam):** identical to substrate-registry — mantis WS1 wave-close owns engine-emit → UE-ingest round-trip verification.

---

## 9. Engineering disciplines cited

- **Discipline #1 (math-before-code):** schema § 2 + axis count § 3 are the "math" of the sidecar; locked before emit code lands
- **Discipline #11 (empirical inspection over assumption):** gamora reads canonical doc § 1.8 + § 3.5 + § 1.1 (designer-writes-substrate / player-names-experience principle); does not assume content
- **Discipline #18 (mathematical-layer routing):** experiential-axes catalogue is gamora seam's mathematical-layer authority (simulation validates predicted scores); rocket consults at composition with substrate-registry
- **Discipline #40 (scaffold-with-pending-decision):** axis-level `axis_status` flags `hypothesis_pending` for Progression-Stage + `proposed_playtest_pending` for Activity-Format; value-level `value_status` flags accordingly; scaffolds explicit not silent
- **Discipline #41 (substrate-led):** sidecar content driven by canonical sources (hypothesis-flow § 1.8 + § 3.5); compose-vs-extend disposition reflects canonical architecture (separate cell-schema layers), not designer-imposed taxonomy
- **Principle 3 (cross-seam impact):** engine emits → mantis ingests across host boundary; schema-version semver discipline + ADR-004 cross-seam-contract treatment
- **Principle 6 (round-trip discipline):** owned downstream at mantis WS1 wave-close

---

## 10. Discipline #40 scaffold flags (explicit summary)

| Scaffold | Axis | Resolves when |
|---|---|---|
| Hypothesis-pending leveling-as-viability | Progression-Stage | Playtest validates or refutes § 1.8.5 hypothesis (post-Phase-1 retroactive identity finalization → playtest cycles) |
| Proposed playtest-pending player-input map architecture | Activity-Format | Player-input procedural map architecture (per § 1.8.7 iter 8) commits canonically + playtest validation. Note: § 1.8.7 is "ARCHITECTURAL COMMITMENT STATUS: PROPOSED PLAYTEST-PENDING" per canonical doc; sidecar honors that status. |
| Bundled-vs-decomposed Maxroll 5-axis | Maxroll 5-axis | gamora seam-owner emits with chosen variant; documents reasoning; first-cycle emit is the lock OR an explicit gamora pushback memo to gandalf surfaces alternative |
| Activity-Format working enumeration | Activity-Format values (8 working values per § 1.8.7) | Player-input architecture commits canonically; values stabilize OR mutate per architecture commit |

---

## 11. Implementation guidance (non-binding; gamora discretion)

Gamora implements emit per gamora's seam-owner judgment. Non-binding suggestions:

- Python module: `~/Games/reincarnated-engine/src/reincarnated/canonical/sidecars/emit_experiential_axes.py`
- Hard-encoded axis enumeration per canonical doc § 1.8 + § 3.5 (the 7-axis enumeration is stable canonical content; not derived from runtime data)
- Per-axis `operational_definition` + `axis_treatment` text: drawn from canonical doc tables verbatim where possible; minor rewording OK where canonical text is multi-paragraph
- `composition_with_bc_axes` field: gamora authors per axis using `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 6 BC-axes operational definitions. Substrate-vector-cheatsheet skill (per gamora OP) supplies the 8 BC axes content for cross-reference
- First-emit smoke: gamora runs emit → JSON-loads result → asserts 7 axes (or chosen variant) + all required fields populated → diffs against canonical doc § 1.8 + § 3.5
- **Cross-consultation with rocket** at first emit if axis-value `cell_score_field` references conflict with substrate-registry primitive_id (sanity check; expected no conflict, but explicit at first emit)

**No gamora-side mantis interaction at emit time.** Same pattern as substrate-registry sidecar.

---

## 12. Path A execution chain (informational; gamora's place in chain)

Per Matt 2026-06-10 ratification of Path A:

1. **gandalf** (this design-spec) → emit shape locked ✓
2. **gamora** consumes this design-spec → implements emit per § 5 + § 11 → commits to engine repo (parallel to rocket substrate-registry emit; independent module; no cross-dep)
3. **gamora + rocket** consult on `composition_with_bc_axes` field content if cross-seam check warranted
4. Engine push to origin (Matt-authorized push; cycle-batched with rocket substrate-registry emit OR separate)
5. **PC** pulls engine repo at next PC session-start → sidecars reach PC clone
6. **mantis** WS1 fires → consumes `DT_ExperientialAxis` sidecar via `fill_datatable_from_json`
7. **mantis** WS1 close + **sam** Gate-2 + **david-h** wave-close → PC push
8. WS3.2-5 + vertical-slice spike unlocked

**Gamora's deliverable:** sidecar emitted + committed + pushed. Estimated bounded scope: ~3-5 hours gamora work (schema + emit CLI + per-axis content authoring + BC-axes composition annotations + smoke + diff review). Slightly larger than substrate-registry scope because experiential-axes carry more semantic content per row.

---

## 13. Routing handoff

**This design-spec routes to:** gamora (engine simulation seam owner; primary); rocket (consulting on substrate-registry composition)

**KR routing pattern:** knight-rider routes this design-spec + companion substrate-registry design-spec as parallel fires to gamora + rocket. Both seam-owners execute in parallel; both push at engine-side cycle close.

**Pushback path:** if gamora recommends different axis enumeration count (e.g., 11 rows decomposed; or simplification to 6 rows; or alternate schema), surface to gandalf + knight-rider for revision. Substrate-led discipline: gamora's empirical judgment at simulation-validation-loop layer can refine design-spec count if canonical-doc reading produces different enumeration. Schema § 2 + acceptance criteria § 8 are load-bearing; row-count § 3 disposition and implementation path § 5 + § 11 carry gamora-discretion latitude.

---

## 14. Cross-spec coherence with substrate-registry sidecar

Both design-specs (substrate-registry + experiential-axes) share these patterns for sam Gate-2 verification simplicity + mantis ingestion consistency:

| Pattern | Both sidecars |
|---|---|
| Top-level JSON shape | dict with provenance fields + array field carrying the rows |
| Provenance fields | `schema_version` + `emission_timestamp` + `source_canonical_cite` + `source_canonical_status` + `source_canonical_date` |
| Identifier convention | snake_case lowercase |
| Schema versioning | semver |
| Timestamp format | ISO-8601 UTC |
| Output path | `~/Games/reincarnated-engine/src/reincarnated/canonical/sidecars/<sidecar_name>_v1.json` |
| Emit trigger | one-shot CLI; manual re-fire on canonical doc update |
| Round-trip ownership | downstream at mantis WS1 wave-close per sam Gate-2 |
| Acceptance-criteria smoke | json-load + length-assert + key-presence-assert |
| Discipline #41 substrate-led discipline | content from canonical sources only |
| Cross-seam consultation | yes (substrate-registry: rocket consults gamora on simulation-touching families; experiential-axes: gamora consults rocket on substrate-registry composition) |

---

## 15. Sign-off

**Author:** gandalf (story-and-design steward)
**Date:** 2026-06-10
**Authority:** Matt 2026-06-10 direct direction + Path A ratification per DH WS3.1 routing memo § 5
**Anchor docs cited:**
- `canonical/story/2026-05-31-hypothesis-flow-pattern-library-architecture.md` § 1.8 + § 3.5 (CURRENT; source-of-truth for axis architecture + cell-schema fields)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` (CURRENT; 8 BC axes for compose-with annotations)
- `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` (CURRENT; third-coordinate-axis recognition)
- `agentic_orchestration/qa/findings/2026-06-10-gate-1-ws1-ws3-paired-pre-fire.md` § 84 + § 159 (Sam Gate-1 BLOCK-WS1-A + axis-count surfacing WARN)
- `agentic_orchestration/dispatches/2026-06-10-david-h-ws1-data-layer-kit-corpus-ingestion-commission.md` (downstream WS1 ingestion shape)
- `agentic_orchestration/dispatches/2026-06-10-david-h-ws3-1-routing-memo.md` § 5 (Path A ratification)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #11 + #18 + #40 + #41 + Principle 3 + Principle 6)

**Companion design-spec:** `agentic_orchestration/dispatches/2026-06-10-gandalf-substrate-registry-sidecar-design-spec.md`
