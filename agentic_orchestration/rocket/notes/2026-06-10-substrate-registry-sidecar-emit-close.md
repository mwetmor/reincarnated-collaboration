# Close memo — Atomic Substrate Registry sidecar emit

**Date:** 2026-06-10
**Author:** rocket (engine content-generation seam owner)
**Dispatch:** `agentic_orchestration/dispatches/2026-06-10-gandalf-substrate-registry-sidecar-design-spec.md`
**Engine-repo commit SHA:** `e7de6d1`

---

## Emit code path

`~/Games/reincarnated-engine/src/reincarnated/canonical/sidecars/emit_substrate_registry.py`

CLI trigger (from engine repo root):
```
python3 -m reincarnated.canonical.sidecars.emit_substrate_registry
```

Also added: `src/reincarnated/canonical/sidecars/__init__.py` (module init for the new `sidecars` package)

---

## Sidecar artifact path

`~/Games/reincarnated-engine/src/reincarnated/canonical/sidecars/atomic_substrate_registry_v1.json`

**Row count verification:** `len(d['families']) == 20` — PASS (Sam Gate-1 § 84 criterion satisfied)

**Provenance fields:**
- `schema_version`: "1.0.0"
- `emission_timestamp`: "2026-06-10T21:03:33Z"
- `source_canonical_cite`: "canonical/story/2026-06-06-atomic-substrate-registry.md"
- `source_canonical_status`: "CANONICAL"
- `source_canonical_date`: "2026-06-06"

---

## Smoke-test output summary (Discipline #2)

**Full emit run:** `python3 -m reincarnated.canonical.sidecars.emit_substrate_registry`

```
EMIT PASS
  sidecar: .../src/reincarnated/canonical/sidecars/atomic_substrate_registry_v1.json
  schema_version: 1.0.0
  emission_timestamp: 2026-06-10T21:03:33Z
  family_count: 20
  sha256_prefix: fb24e49eb92e
  scaffold_families (Discipline #40): [9 families listed below]
  acceptance_criteria: ALL PASS
```

**Design-spec § 7 criterion 9 exact command:**
```
python3 -c "import json; d = json.load(open('atomic_substrate_registry_v1.json')); assert len(d['families']) == 20; assert all('family_id' in f for f in d['families']); print('PASS')"
```
Output: `PASS`

---

## Discipline #40 scaffolds preserved

9 scaffold families carried as `tbd` or `schema_only` per design-spec § 9 and Discipline #40. No designer-imposed placeholder content.

| § | family_id | status | Resolves when |
|---|---|---|---|
| 1.2 | sub_elements | tbd | Per-primary flavor pool enumeration commits via flavor-pool doc |
| 1.10 | mechanic_altering_passives | tbd | Mechanic registry locked in foundation/ per Cycle 13+ |
| 1.12 | modifier_types | tbd | Cycle 13 partition design milestone per canonical 42 |
| 1.13 | ailment_types | tbd | ailment_loader.py per-element registry consumption (v1.1 candidate) |
| 1.16 | off_hand_items | tbd | off-hand-items doc per-token enumeration commits |
| 1.17 | races | schema_only | Per-season race-set authoring at season-design time |
| 1.18 | racial_traits | schema_only | Per-season race-set authoring at season-design time |
| 1.19 | race_element_affinity | schema_only | Per-season race-set authoring at season-design time |
| 1.20 | race_attribute_affinity | schema_only | Per-season race-set authoring at season-design time |

Note: design-spec § 9 listed 6 explicit scaffolds; § 1.19-1.20 (race affinity families) also carry `schema_only` per canonical source — 9 total scaffold families in sidecar, all correct per canonical.

---

## Locked families (primitive_count_status = "locked")

| § | family_id | primitive_count | primitives populated |
|---|---|---|---|
| 1.1 | elements | 8 | 8 (from config/elements.yaml) |
| 1.3 | attributes | 4 | 4 (from config/attributes.yaml; VIT excluded per canonical § 1.3) |
| 1.4 | t4_strategies | 6 | 6 (per canonical 39 + 40 tables) |
| 1.5 | skill_geometry_palette | 16 | 16 (CORE 14 + CORE-MARGINAL 2) |
| 1.6 | skill_tree_position | 4 | 4 (4 position axes; combinatorial space not enumerated per design-spec § 2.4) |
| 1.7 | scaling_pattern_per_tier | 4 | 4 (per canonical 47) |
| 1.8 | chain_architecture | 2 | 2 (per canonical 40 D83) |
| 1.9 | investment_scaling_patterns | 6 | 6 (per canonical 51) |
| 1.11 | resource_models | 5 | 5 (per cycle13_characters.db CHECK constraint) |
| 1.14 | weapon_form_tokens | 200 | 0 (rich inner structure stays at canonical per design-spec § 2.4) |
| 1.15 | weapon_substrate_properties | 89839 | 0 (rich matrix stays at canonical per design-spec § 2.4) |

---

## Acceptance-criteria verdict

| AC | Criterion | Verdict |
|---|---|---|
| AC1 | Row count == 20 | GREEN |
| AC2 | family_id uniqueness + snake_case | GREEN |
| AC3 | All families family_layer == "Layer_0" | GREEN |
| AC4 | NEW-flag accuracy (§ 1.6/1.7/1.17/1.18 = true; others false) | GREEN |
| AC5 | schema-only-flag accuracy (§ 1.17-1.20 = true; others false) | GREEN |
| AC6 | primitive_count_status consistency | GREEN |
| AC7 | Provenance fields populated | GREEN |
| AC8 | family_section bidirectional reference auditable | GREEN |
| AC9 | Design-spec § 7 smoke-test command -> PASS | GREEN |
| AC10 | No designer-imposed content (Discipline #41) | GREEN |

**Overall verdict: GREEN — all 10 acceptance criteria pass.**

---

## Engine-repo commit SHA

`e7de6d1`

Commit message: `rocket: atomic-substrate-registry JSON sidecar emit (BLOCK-WS1-A unblock)`

**Do NOT push engine-repo from this fire.** KR sequences engine-repo push after both rocket + gamora engine emits land per Path A execution chain.

---

## Cross-seam notes

- Gamora fires in parallel (experiential-axes sidecar); both land at engine-repo before KR push.
- Mantis WS1 Phase 1 ingestion path (PC-side): `C:\dev\reincarnated-engine\src\reincarnated\canonical\sidecars\atomic_substrate_registry_v1.json`
- Schema-version composition: v1.0.0 -> UE struct v1; major bumps require UE struct update + MIGRATION.md per ADR-004.
- MIGRATION.md not required for this emit per design-spec Principle 3 note: "emit-only at engine seam; consumer-side ingestion lives at PC mantis seam; design-spec § round-trip handles cross-seam contract."

---

**Signed:** rocket, 2026-06-10
