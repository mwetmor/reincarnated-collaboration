# Gamora Close Memo — Experiential-Axes Sidecar Emit

**Date:** 2026-06-10
**Author:** gamora (engine simulation + spirit-guide seam owner)
**Dispatch:** `agentic_orchestration/dispatches/2026-06-10-gandalf-experiential-axes-sidecar-design-spec.md`
**Authority:** Matt 2026-06-10 direct direction + Path A ratification (DH WS3.1 routing memo § 5)

---

## Emit code path

`~/Games/reincarnated-engine/src/reincarnated/canonical/sidecars/emit_experiential_axes.py`

CLI trigger:
```bash
python3 -m reincarnated.canonical.sidecars.emit_experiential_axes
```

Module also creates `__init__.py` in the new `canonical/sidecars/` subdirectory
(gamora-authored; rocket's companion `emit_substrate_registry.py` co-locates here on parallel fire).

---

## Sidecar artifact path

`~/Games/reincarnated-engine/src/reincarnated/canonical/sidecars/experiential_axes_v1.json`

PC ingestion path (mantis WS1):
`C:\dev\reincarnated-engine\src\reincarnated\canonical\sidecars\experiential_axes_v1.json`

Row count: **7** (matches `expected_axis_count` field; Sam Gate-2 can verify with
`python3 -c "import json; d=json.load(open('experiential_axes_v1.json')); assert d['expected_axis_count']==len(d['axes']); print('PASS')"`)

---

## Smoke-test output summary

```
experiential_axes emit COMPLETE
  output_path : .../canonical/sidecars/experiential_axes_v1.json
  schema_version : 1.0.0
  axis_count : 7 (expected_axis_count=7)
  row_count_variant : bundled_7rows
  emission_timestamp : 2026-06-10T21:03:34Z
  sidecar_sha256 : 7769b3fd8b51b77477adc07b49f3933e1da01e2aea45732ecf6b7eb50edb4f5a
  per-axis status:
  [progression_stage]         status=hypothesis_pending
  [target_pattern]            status=locked
  [depth_vs_breadth]          status=locked
  [activity_format]           status=proposed_playtest_pending
  [loot_focus]                status=locked
  [maxroll_5axis]             status=locked
  [survivability_playability] status=locked
smoke_test PASS — all acceptance criteria verified
```

Discipline #2 smoke-gate satisfied. Emit + smoke-test ran in a single CLI invocation.

---

## Row-count decision: 7 (bundle variant) — rationale

Design-spec § 3.1 presents two variants:
- **7 rows** (Maxroll 5-axis as single bundle row; gandalf default)
- **11 rows** (Maxroll 5-axis decomposed into 5 atomic rows)

**Gamora seam-owner elects 7-row BUNDLE variant.**

Reasoning: hypothesis-flow § 3.5 carries `maxroll_5axis_prediction` as a **single dict field**
in the cell schema.  Design-spec § 3.1 makes this explicit: "cells carry `maxroll_5axis_prediction`
as a single dict field."  Emitting 5 separate Maxroll rows would split a schema unit that is
intentionally bundled at the cell layer.  The bundle framing is the canonical cell-schema treatment;
decomposing the sidecar row would introduce a schema-sidecar / cell-schema mismatch.

**Deferred upgrade path:** if canonical § 3.5 later splits `maxroll_5axis_prediction` into 5
discrete cell fields, re-emit with v1.1.0 minor bump and 5 atomic rows at that time.

Sam Gate-2 verifier: `len(axes) == expected_axis_count == 7` is the committed numeral.
This resolves Sam Gate-1 § 84 TBD + § 159 explicit-numeral requirement.

---

## Discipline #40 scaffolds preserved

Three axes carry non-locked status per design-spec § 10:

| Axis | scaffold flag | Resolves when |
|---|---|---|
| `progression_stage` | `hypothesis_pending` | Playtest validates or refutes § 1.8.5 leveling-as-viability hypothesis |
| `activity_format` | `proposed_playtest_pending` | Player-input procedural map architecture commits canonically + playtest validation |
| `maxroll_5axis` | `locked` (bundled_7rows variant explicit in `bundled_vs_decomposed_variant` field) | Sidecar version bumps if canonical cell-schema splits the maxroll field |

All three scaffolds surfaced explicitly in sidecar fields (`axis_status`, `proposed_playtest_pending`,
`scaffold_note`, `bundled_vs_decomposed_variant`) per Discipline #40 (scaffold-with-pending-decision).

---

## Composition note: experiential axes vs BC axes

**Compose-vs-extend disposition: COMPOSE WITH (not extend).**

Per design-spec § 6 + canonical § 3.4 vs § 3.5:

- **BC axes (8)** are mechanical-substrate vectors (engagement profile / damage geometry / proxy
  density / control density / damage tempo / damage amplitude variance / defensive profile /
  resource economy).  Substrate-vote at generation layer; designer-writes-substrate.
- **Experiential axes (7)** are player-experience prediction coordinates (Target-Pattern /
  Depth-vs-Breadth / Progression-Stage / Activity-Format / Loot-Focus / Maxroll 5-axis /
  Survivability+Playability).  Cells PREDICT these scores; simulation + playtest VALIDATE.

The two layers are orthogonal coordinates in cell space (separate cell-schema sections § 3.4 vs
§ 3.5).  Experiential axes do NOT extend BC axes; they occupy a separate layer.

Each axis record carries a `composition_with_bc_axes` field enumerating the specific BC axes
that compose with it (e.g., Target-Pattern Bossing composes with BC Axis 1 Engagement Profile
+ Axis 3A Damage Tempo + Axis 3B Damage Amplitude Variance + Axis 2 Damage Geometry).

**Gamora simulation seam ownership:** per design-spec § 1, gamora owns the experiential-axes
catalogue as the VALIDATION half of the prediction loop (cells predict → simulation evaluates
→ playtest finalizes).  Rocket consults at substrate-registry composition surface.

---

## Acceptance criteria verdict

| Criterion | Verdict | Notes |
|---|---|---|
| 1. Emit code at canonical/sidecars/ | GREEN | Path confirmed; module at emit_experiential_axes.py |
| 2. CLI trigger exists per design-spec § 5 | GREEN | `python3 -m reincarnated.canonical.sidecars.emit_experiential_axes` |
| 3. Valid JSON; row count matches committed N=7 | GREEN | Smoke PASS; expected_axis_count==len(axes)==7 |
| 4. schema_version + emission_timestamp + source_canonical_cite + 3 scaffolds | GREEN | All top-level provenance fields non-null; 3 scaffold rows flagged |
| 5. Smoke-test PASS (Discipline #2) | GREEN | PASS logged above; SHA confirmed |
| 6. Engine-repo auto-commit | GREEN | Committed per CLAUDE.md addendum (see SHA below) |

**Overall: GREEN**

---

## Engine-repo commit SHA

`7ddeffe` — gamora: experiential-axes JSON sidecar emit (BLOCK-WS1-A unblock)

Auto-committed per CLAUDE.md addendum (authorized BLOCK-WS1-A critical-path cycle work).
Engine-repo push timing: KR sequences push after BOTH gamora + rocket engine emits land.
Do NOT push engine-repo from this fire per dispatch instruction.
