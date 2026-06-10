# Design-Spec: atomic-substrate-registry JSON sidecar emit

> **STATUS:** DESIGN-SPEC (load-bearing as of 2026-06-10) — Path A critical-path unblock for BLOCK-WS1-A per Matt 2026-06-10 direct direction
>
> **Type:** Design-spec-as-math handoff (Discipline #18 architecture) — gandalf authors the schema + emit shape; rocket implements engine-side emit.

**Date:** 2026-06-10
**Author:** gandalf (story-and-design steward)
**Addressee:** rocket (engine content-generation seam — owns `generation/`, `foundation/`, `element/`, `anchor/`)
**Authority:** Matt 2026-06-10 direct direction ("Highest-leverage next-action: gandalf authors 2 Path A JSON sidecar design-specs (substrate-registry + experiential-axes) NOW. Direct critical-path unblock for WS1 → WS3.2-5 → vertical-slice spike chain.") composed with Sam Gate-1 BLOCK-WS1-A finding (2026-06-10) + Matt earlier ratification of Path A per DH WS3.1 routing memo § 5.

**Critical-path framing:** this design-spec → rocket implements emit → engine pushes → PC pulls → BLOCK-WS1-A resolves → WS1 fires (mantis kit-corpus ingestion to UE DataTables for `DT_PrimitiveFamily`) → WS3.2-5 + vertical-slice spike unlock.

**Companion design-spec:** `agentic_orchestration/dispatches/2026-06-10-gandalf-experiential-axes-sidecar-design-spec.md` (gamora-addressed; co-fires)

**Source-of-truth canonical:**
- `canonical/story/2026-06-06-atomic-substrate-registry.md` — Layer 0 20-family CANONICAL (this is the input-of-truth)
- Optional composing context: `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 12 (INPUT primitives correspond to families participating in elicitation cascade)

**Downstream consumer:** `agentic_orchestration/dispatches/2026-06-10-david-h-ws1-data-layer-kit-corpus-ingestion-commission.md` (mantis WS1 Phase 1 → UE `DT_PrimitiveFamily` DataTable via db-lyon `fill_datatable_from_json`)

---

## 0. TL;DR

Emit a machine-readable JSON sidecar of Layer 0 atomic substrate primitive families per `canonical/story/2026-06-06-atomic-substrate-registry.md` § 1. **Expected row count: 20** (one row per family § 1.1 through § 1.20; per Sam Gate-1 § 84 "DT_PrimitiveFamily=20 per atomic-substrate-registry Layer 0"). Emit shape: top-level dict with `schema_version` + `emission_timestamp` + `source_canonical_cite` + `families` (array of 20 family records). Output path: engine-internal canonical library emit → engine-repo staging path → push to origin → PC pull at next session-start.

---

## 1. Seam ownership recommendation

**Recommendation: rocket primary; foundation/canonical/ library is the emission home.**

**Reasoning:**
- The substrate registry catalogues GENERATIVE INPUTS the engine composes from at Phase 2 substrate-binding (per canonical 39 § 1). Generation seam owns the catalogue of what generation pulls from.
- `~/Games/reincarnated-engine/src/reincarnated/foundation/` already houses the substrate identity layer (`substrate_identity_loader.py`, `vocabularies.py`, `elements.py`, `ailment_loader.py`, `resources.py`, etc.) — the natural home for a substrate-registry catalogue file.
- `~/Games/reincarnated-engine/src/reincarnated/canonical/` (engine-internal canonical library — rocket's seam per role definitions) is where catalogue exports of canonical truth live.
- Per cross-seam protocol, if rocket needs gamora's input for substrate that touches simulation (e.g., resource models § 1.11 cross-touch BC Axis 5), rocket consults; ownership remains rocket.

**Alternate consideration (rejected):** star-lord owns export/output/. But the substrate-registry sidecar is NOT a per-cycle export artifact (like cycle-14 wave-5 kit corpus). It's a canonical-truth catalogue emit, which is rocket's seam.

---

## 2. JSON schema (the math)

Per Discipline #1 (math-before-code), the schema IS the math of the sidecar. Specify before emit code lands.

### 2.1 Top-level structure

```json
{
  "schema_version": "1.0.0",
  "emission_timestamp": "2026-06-10T00:00:00Z",
  "source_canonical_cite": "canonical/story/2026-06-06-atomic-substrate-registry.md",
  "source_canonical_status": "CANONICAL",
  "source_canonical_date": "2026-06-06",
  "expected_family_count": 20,
  "families": [
    { /* family record per § 2.2 below */ },
    /* ... 19 more ... */
  ]
}
```

**Why top-level dict (not bare array):**
- Mantis `fill_datatable_from_json` ingests an array of rows for DataTable population (per WS1 commission step 4). The `families` field IS that array. Mantis points db-lyon at `families[*]` for row extraction OR mantis Python pre-processes the dict to extract `families` array — both shapes supported by `fill_datatable_from_json` per spike PASS-WITH-WARN evidence.
- Top-level dict preserves provenance fields (schema_version + emission_timestamp + source_canonical_cite) outside the ingested DataTable row payload — provenance survives even if downstream consumers drop metadata.
- Schema-version field enables sidecar evolution without breaking ingest (semver discipline: minor bumps additive; major bumps require Mantis schema-struct update + MIGRATION.md per ADR-004).

### 2.2 Family record schema

Each of the 20 family records carries this shape:

```json
{
  "family_id": "elements",
  "family_section": "1.1",
  "family_display_name": "Element primitives",
  "family_layer": "Layer_0",
  "primitive_count": 8,
  "primitive_count_status": "locked",
  "canonical_source_path": "~/Games/reincarnated-engine/config/elements.yaml",
  "secondary_canonical_source_path": "canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md",
  "primitives": [
    {
      "primitive_id": "fire",
      "primitive_type": "canonical-7 rotating",
      "notes": "INT scaling; canonical"
    }
    /* ... per § 1.1 table contents ... */
  ],
  "composition_notes": "Per element_biases.py element-attribute coupling; composes into BC Axis 1 + Axis 4 mechanical character",
  "new_in_2026_06_06": false,
  "schema_only": false
}
```

### 2.3 Field-by-field semantics

| Field | Type | Required | Semantics |
|---|---|---|---|
| `family_id` | string | YES | Stable snake_case identifier; used as `DT_PrimitiveFamily` row key. Drawn from canonical § headings (e.g., `elements`, `sub_elements`, `attributes`, `t4_strategies`, `skill_geometry_palette`, `skill_tree_position`, `scaling_pattern_per_tier`, `chain_architecture`, `investment_scaling_patterns`, `mechanic_altering_passives`, `resource_models`, `modifier_types`, `ailment_types`, `weapon_form_tokens`, `weapon_substrate_properties`, `off_hand_items`, `races`, `racial_traits`, `race_element_affinity`, `race_attribute_affinity`) |
| `family_section` | string | YES | Canonical-doc section number (e.g., `1.1` through `1.20`); enables bidirectional reference auditing |
| `family_display_name` | string | YES | Human-readable name (e.g., `Element primitives`) |
| `family_layer` | enum string | YES | `Layer_0` for all 20 families (per canonical § 1); reserved enum extension for future Layer 0.5 / Layer 1 emits |
| `primitive_count` | int OR null | YES | Locked numeric count where canonical specifies (e.g., 8 for elements; 4 for attributes; 6 for T4 strategies; 16 for skill geometry palette; 4 for scaling-pattern-per-tier; 2 for chain architecture; 6 for investment scaling patterns; 5 for resource models; ~200 for weapon-form tokens; 89839 for weapon-substrate property rows). `null` when canonical defers (e.g., sub_elements TBD per pool; mechanic_altering_passives TBD per registry; modifier_types TBD per Cycle 13; ailment_types TBD per element; off_hand_items TBD; races + racial_traits + race_element_affinity + race_attribute_affinity SCHEMA ONLY) |
| `primitive_count_status` | enum string | YES | `locked` / `tbd` / `schema_only`. Locked = numeric and verified; tbd = canonical defers to downstream registry; schema_only = no per-instance enumeration (per § 1.17-1.20 race-family pattern) |
| `canonical_source_path` | string | YES | Primary canonical source path per canonical doc § header (e.g., `~/Games/reincarnated-engine/config/elements.yaml` for elements) |
| `secondary_canonical_source_path` | string OR null | NO | Secondary source where canonical doc cites two |
| `primitives` | array OR null | YES | When `primitive_count_status == "locked"`: array of primitive records per § 2.4. When `tbd` or `schema_only`: empty array `[]` (preserves shape stability for ingest) |
| `composition_notes` | string | NO | Free-text composition guidance per canonical doc family description (e.g., "Composes with BC Axis 1") |
| `new_in_2026_06_06` | boolean | YES | True for families flagged "NEW per Matt 2026-06-06" in canonical doc (§ 1.6 skill-tree-position; § 1.7 scaling-pattern-per-tier; § 1.17 races; § 1.18 racial-traits) |
| `schema_only` | boolean | YES | True for families § 1.17-1.20 (race-family schema-only per Matt 2026-06-06 directive); composes with `primitive_count_status == "schema_only"` |

### 2.4 Primitive record schema (for `primitives` array entries when `locked`)

```json
{
  "primitive_id": "fire",
  "primitive_type": "canonical-7 rotating",
  "notes": "INT scaling; canonical"
}
```

| Field | Type | Required | Semantics |
|---|---|---|---|
| `primitive_id` | string | YES | snake_case identifier; stable within family |
| `primitive_type` | string OR null | NO | Type-classification per family table (e.g., `canonical-7 rotating` vs `+1 retained` for elements) |
| `notes` | string OR null | NO | Free-text notes per canonical table cell content |

**Discipline #40 scaffold:** for families with rich tabular schemas (e.g., § 1.6 skill-tree-position has 4-axis tuple structure; § 1.7 scaling-pattern-per-tier has effect descriptions; § 1.15 weapon-substrate-properties has 6-property × coverage matrix), the `primitives` array carries the canonical table content as primitive records; richer structure (per-axis enumeration for § 1.6; full property × type matrix for § 1.15) lives in the canonical doc, NOT replicated in sidecar. Sidecar is a CATALOGUE of families; per-family inner-structure stays at canonical. WS1 `DT_PrimitiveFamily` ingestion is per-family-row (20 rows), not per-primitive-row.

### 2.5 Identifier convention summary

- All identifiers (`family_id`, `primitive_id`): snake_case, lowercase, no hyphens (matches `~/Games/reincarnated-engine/foundation/` convention)
- Section numbers: dotted decimal (`1.1` through `1.20`)
- Schema version: semver (`1.0.0` for first emit)
- Timestamps: ISO-8601 UTC

---

## 3. Expected row count: 20 (load-bearing)

**Per Sam Gate-1 § 84:** "DT_PrimitiveFamily=20 (per atomic-substrate-registry Layer 0)"

**Verification against canonical § 1:**

| § | Family | Count |
|---|---|---|
| 1.1 | Element primitives | 1 |
| 1.2 | Sub-element / flavor primitives | 1 |
| 1.3 | Attribute primitives | 1 |
| 1.4 | T4 strategy primitives | 1 |
| 1.5 | Skill geometry palette | 1 |
| 1.6 | Skill-tree position primitives (NEW) | 1 |
| 1.7 | Scaling pattern per tier primitives (NEW) | 1 |
| 1.8 | Chain architecture primitives | 1 |
| 1.9 | Investment scaling pattern primitives | 1 |
| 1.10 | Mechanic-altering passive pool | 1 |
| 1.11 | Resource model primitives | 1 |
| 1.12 | Modifier type primitives | 1 |
| 1.13 | Ailment type primitives | 1 |
| 1.14 | Weapon-form token primitives | 1 |
| 1.15 | Weapon-substrate property primitives | 1 |
| 1.16 | Off-hand item substrate primitives | 1 |
| 1.17 | Race primitives (NEW; SCHEMA ONLY) | 1 |
| 1.18 | Racial trait primitives (NEW; SCHEMA ONLY) | 1 |
| 1.19 | Race-element affinity primitives | 1 |
| 1.20 | Race-attribute affinity primitives | 1 |
| **TOTAL** | | **20** |

Locked. No Discipline #40 scaffold required on row count.

---

## 4. Output path target

**Recommended emission path (engine-side):**

```
~/Games/reincarnated-engine/src/reincarnated/canonical/sidecars/atomic_substrate_registry_v1.json
```

**Reasoning:**
- Engine-repo-resident (NOT meta-repo staging) — single-source-of-truth at engine canonical library
- Path A per Matt ratification: PC clones engine repo at `C:\dev\reincarnated-engine\` and pulls; sidecar reaches PC via engine push → PC pull
- Versioned filename (`_v1`) preserves prior emit on schema-major-bump
- Lives under `canonical/sidecars/` sub-directory keeping canonical library navigable as it grows (gamora's experiential-axes sidecar lives in same sub-directory)

**Mantis WS1 ingestion path resolution (PC-side):**

```
C:\dev\reincarnated-engine\src\reincarnated\canonical\sidecars\atomic_substrate_registry_v1.json
```

After Path A PC clones complete, mantis db-lyon `fill_datatable_from_json` points at this PC path. WS1 commission § 1.3 amends in-place per Sam Gate-1 WARN-on-criterion-3 (or david-h pre-fire memo) to cite this exact path.

**Alternate (rejected): meta-repo staging path.** Rejected because (a) Matt ratified Path A over Path B; (b) staging-JSON discipline would need sustaining for all future cycles; (c) engine canonical library is the true single-source-of-truth, NOT meta-repo staging mirror.

---

## 5. Emission trigger

**Recommendation: one-shot CLI command + manual re-fire on canonical doc update.**

```bash
# From engine repo root
python -m reincarnated.canonical.sidecars.emit_substrate_registry
```

**Reasoning:**
- The substrate registry CANONICAL doc evolves on Matt-ratification cycles (e.g., the 2026-06-06 multi-iteration design call produced 5 new families § 1.6/1.7/1.17/1.18/seasonal-rotation operator). Emit cadence MATCHES canonical-doc-update cadence — manual fire when doc updates is the discipline-correct trigger.
- Always-on emit hook is over-engineering for a 20-row catalogue that updates ~monthly.
- One-shot CLI composes with engine push discipline: rocket runs emit → reviews diff → commits → pushes per Matt-authorized push pattern.

**CLI behavior:**
1. Reads canonical doc (path: `canonical/story/2026-06-06-atomic-substrate-registry.md`) for content cross-check (optional; manual update is also OK for v1)
2. Reads per-family data from engine canonical library where authoritative (e.g., `config/elements.yaml` for § 1.1; `foundation/attributes.py` for § 1.3; `foundation/resources.py` for § 1.11; `foundation/ailment_loader.py` for § 1.13; foundation/ vocabularies.py for relevant text content)
3. Composes the top-level JSON dict per § 2.1
4. Writes to `canonical/sidecars/atomic_substrate_registry_v1.json`
5. Prints emit summary: row count + schema version + sidecar SHA

**Discipline #11 (empirical inspection):** the canonical doc § 1 contains the authoritative tabular content; rocket consumes the canonical-doc tables (or where engine code has authoritative source like `elements.yaml`, prefers engine-code over doc-derived text) and emits. Do NOT designer-impose; substrate-led per Discipline #41.

---

## 6. Composition with WS1 ingestion

**Mantis WS1 Phase 1 step 4:** `db-lyon fill_datatable_from_json` with source JSON path → `DT_PrimitiveFamily` UE DataTable.

**Composition:**
- WS1 commission `DT_PrimitiveFamily` row schema → mantis authors UE C++ struct matching this JSON family record schema § 2.2 (one-row-per-family; `family_id` as row key)
- `fill_datatable_from_json` consumes the `families` array within the top-level dict — either by pointing at `families[*]` via JSON path OR by mantis Python pre-processing extracting `families` and re-emitting as bare array for db-lyon ingest. Mantis WS1 implements whichever shape db-lyon's `fill_datatable_from_json` requires (per spike PASS-WITH-WARN evidence — confirm at mantis WS1 fire)
- `primitive_count_status` field flags TBD/schema-only families so DT consumers can branch per-row (e.g., "show enumeration UI for locked families; show schema-only placeholder UI for schema-only families")
- `primitives` array preserved per row even when empty (`[]`) so UE struct schema is stable across all 20 rows

**Schema-version composition:** sidecar v1.0.0 → UE struct v1; major bumps require UE struct update + MIGRATION.md per ADR-004 cross-seam contract change.

**Discipline #11 + Principle 3 cross-seam impact:** rocket emits → mantis ingests across host boundary. Round-trip verification lives at WS1 wave-close per Sam Gate-2 criterion #3 (row count match) + criterion #4 (no row-level field gaps). Sidecar-side acceptance criteria § 7 below verify EMIT correctness; mantis WS1 wave-close verifies INGEST correctness.

---

## 7. Acceptance criteria

Per Discipline #1 (math-before-code) + Discipline #11 (empirical inspection):

1. **Row count match (Sam Gate-1 § 84):** sidecar `families` array length == 20; equals canonical § 1.1-1.20 section count
2. **Family-id stability:** all 20 `family_id` values are unique snake_case identifiers; no collisions; ordered matching canonical § 1 section sequence
3. **Layer-stamp consistency:** all 20 families have `family_layer == "Layer_0"` (Layer 0.5 + Layer 1 emit reserved for future sidecars)
4. **NEW-flag accuracy:** § 1.6 + § 1.7 + § 1.17 + § 1.18 carry `new_in_2026_06_06 == true`; other 16 carry `false`
5. **Schema-only-flag accuracy:** § 1.17-1.20 carry `schema_only == true` per canonical "(NEW per Matt 2026-06-06; SCHEMA ONLY)" + race-affinity schema-only pattern; other 16 carry `false`
6. **Primitive-count-status consistency:** locked families carry non-null `primitive_count` + populated `primitives` array; tbd/schema_only families carry null `primitive_count` + empty `primitives` array (shape stability)
7. **Provenance fields populated:** `schema_version`, `emission_timestamp`, `source_canonical_cite`, `source_canonical_status`, `source_canonical_date` all non-null
8. **Canonical-doc cross-reference auditable:** for each family, `family_section` matches canonical doc § heading number; bidirectional check (any reader of sidecar can locate the canonical-doc family description)
9. **Smoke-test pass (Discipline B14.5 V1 smoke-test-vs-full-regen discipline composition):** `python -c "import json; d = json.load(open('atomic_substrate_registry_v1.json')); assert len(d['families']) == 20; assert all('family_id' in f for f in d['families']); print('PASS')"` returns PASS
10. **No designer-imposed content:** rocket emits from canonical sources only (Discipline #41 substrate-led); no fields added that lack canonical anchor

**Round-trip discipline (Principle 6 cross-seam):** sidecar-side round-trip verification is OPTIONAL at sidecar emit (the sidecar IS the source of truth for ingest); mantis WS1 owns the engine-emit → UE-ingest round-trip verification at WS1 wave-close per Sam Gate-2.

---

## 8. Engineering disciplines cited

- **Discipline #1 (math-before-code):** schema § 2 is the "math" of the sidecar; locked before emit code lands
- **Discipline #11 (empirical inspection over assumption):** rocket reads canonical sources (doc + engine-code where authoritative); does not assume content
- **Discipline #40 (scaffold-with-pending-decision):** primitive_count `null` + primitive_count_status `tbd`/`schema_only` flags families whose downstream enumeration is canonical-deferred; sidecar schema accommodates without pre-imposing
- **Discipline #41 (substrate-led):** sidecar content driven by canonical sources, not designer-imposed; no fields added that lack canonical anchor (criterion 10 above)
- **Principle 3 (cross-seam impact):** engine emits → mantis ingests across host boundary; schema-version semver discipline + ADR-004 cross-seam-contract treatment

---

## 9. Discipline #40 scaffold flags (explicit)

The following sidecar contents are SCAFFOLDED per Discipline #40 awaiting downstream canonical lock:

| Family | Scaffold | Resolves when |
|---|---|---|
| § 1.2 sub-elements | `primitives: []` + `primitive_count_status: "tbd"` | Per-primary flavor pool enumeration commits at runtime via `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` consumption |
| § 1.10 mechanic-altering passives | `primitives: []` + `primitive_count_status: "tbd"` | Mechanic registry locked in `foundation/` per Cycle 13+ |
| § 1.12 modifier types | `primitives: []` + `primitive_count_status: "tbd"` | Cycle 13 partition design milestone per canonical 42 |
| § 1.13 ailment types | `primitives: []` + `primitive_count_status: "tbd"` | `foundation/ailment_loader.py` per-element registry consumption (could populate at v1.1 if rocket judges rocket-scope) |
| § 1.16 off-hand items | `primitives: []` + `primitive_count_status: "tbd"` | off-hand-items doc per-token enumeration commits |
| § 1.17-1.20 race primitives | `primitives: []` + `primitive_count_status: "schema_only"` | Per-season race-set authoring at per-season design time |

**Discipline #40 disposition:** scaffolds are EXPLICIT not silent. Sidecar schema accommodates future fill-in via additive minor-version bump (`primitives: [...]` populated without schema change). No designer-imposed placeholder content.

---

## 10. Implementation guidance (non-binding; rocket discretion)

Rocket implements emit per rocket's seam-owner judgment. Non-binding suggestions:

- Python `dataclass` or `pydantic` model for family record + primitive record at emit time → JSON-serialize via `json.dumps(..., indent=2)` for human-readable diff in git
- Engine canonical library import: `from reincarnated.foundation import elements, attributes, resources, ailments` for authoritative per-family content where engine code holds source
- Where canonical doc holds authoritative text (e.g., § 1.4 T4 strategy descriptions live in canonical 39 § 0.5.1 + canonical 40 Algorithm § 8 + canonical 47), rocket reads canonical OR hand-encodes the 6-strategy enum per canonical doc table
- Emit CLI lives at `~/Games/reincarnated-engine/src/reincarnated/canonical/sidecars/emit_substrate_registry.py` (rocket discretion on module structure)
- First-emit smoke: rocket runs emit → JSON-loads result → asserts 20 families + all required fields populated → diffs against canonical doc § 1 table-by-table

**No rocket-side mantis interaction at emit time.** Rocket emits to engine repo; engine push to origin; PC pulls; mantis WS1 fires per WS1 commission. Sidecar emit and WS1 ingest are decoupled across cycle boundary.

---

## 11. Path A execution chain (informational; rocket's place in chain)

Per Matt 2026-06-10 ratification of Path A:

1. **gandalf** (this design-spec) → emit shape locked ✓
2. **rocket** consumes this design-spec → implements emit per § 5 + § 10 → commits to engine repo
3. **rocket** (or engine push pattern) → engine push to origin (Matt-authorized push)
4. **gamora** companion design-spec parallel-fires → gamora implements experiential-axes emit → engine push (cycle-batched OR separate)
5. **PC** pulls engine repo at next PC session-start → sidecars reach PC clone
6. **mantis** WS1 fires → consumes `DT_PrimitiveFamily` sidecar via `fill_datatable_from_json`
7. **mantis** WS1 close + **sam** Gate-2 + **david-h** wave-close → PC push (standing wave-close push pattern)
8. WS3.2-5 + vertical-slice spike unlocked

**Rocket's deliverable:** sidecar emitted + committed + pushed. Estimated bounded scope: ~2-4 hours rocket work (schema + emit CLI + smoke + diff review). Cross-seam consultation to gamora if substrate-registry families touch simulation seam authoritative source (e.g., § 1.11 resource models composing with BC Axis 5).

---

## 12. Routing handoff

**This design-spec routes to:** rocket (engine content-generation seam owner)

**KR routing pattern:** knight-rider routes this design-spec + companion experiential-axes design-spec as parallel fires (independent engine subsystems) to rocket + gamora. Both seam-owners execute in parallel; both push at engine-side cycle close.

**Pushback path:** if rocket recommends different seam allocation (e.g., joint rocket+gamora ownership; or alternate emission path; or schema simplification), surface to gandalf + knight-rider for revision. Substrate-led discipline: rocket's empirical judgment at engine-canonical-library layer can override design-spec at the implementation-detail level. Schema § 2 + acceptance criteria § 7 are load-bearing; implementation path § 5 + § 10 are non-binding.

---

## 13. Sign-off

**Author:** gandalf (story-and-design steward)
**Date:** 2026-06-10
**Authority:** Matt 2026-06-10 direct direction + Path A ratification per DH WS3.1 routing memo § 5
**Anchor docs cited:**
- `canonical/story/2026-06-06-atomic-substrate-registry.md` (CANONICAL; source-of-truth)
- `agentic_orchestration/qa/findings/2026-06-10-gate-1-ws1-ws3-paired-pre-fire.md` (Sam Gate-1 BLOCK-WS1-A surfacing)
- `agentic_orchestration/dispatches/2026-06-10-david-h-ws1-data-layer-kit-corpus-ingestion-commission.md` (downstream WS1 ingestion shape)
- `agentic_orchestration/dispatches/2026-06-10-david-h-ws3-1-routing-memo.md` § 5 (Path A ratification)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 1 (substrate-binding composition)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1 + #11 + #40 + #41 + Principle 3)

**Companion design-spec:** `agentic_orchestration/dispatches/2026-06-10-gandalf-experiential-axes-sidecar-design-spec.md`
