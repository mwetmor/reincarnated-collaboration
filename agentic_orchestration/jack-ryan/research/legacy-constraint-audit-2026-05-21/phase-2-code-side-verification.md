# Phase 2 Code-Side Verification — QD-Engine Rebuild W0.4
# Consolidated Multi-Seam Deliverable

**Date:** 2026-05-21
**Dispatch:** `agentic_orchestration/dispatches/2026-05-21-rocket-plus-gamora-plus-star-lord-w0-4-specialist-code-audit.md`
**Status:** star-lord section COMPLETE; rocket + gamora sections PENDING (append when complete)
**Jack-ryan review:** PENDING (after all 3 seam sections appended)

---

## Star-Lord Section (Telemetry / Export / LLM Seam)

**Author:** star-lord
**Seam tag:** `star-lord/v1.15-w0-4-code-side-audit-1`
**Full deliverable:** `agentic_orchestration/star-lord/research/qd-rebuild-w0-4-star-lord-code-side-audit.md`

### LC Verdicts — Star-Lord Seam

| LC | Constraint | Verdict | Key File:Line |
|---|---|---|---|
| LC-006 | Canonical-four LLM exposure | RESOLVED (star-lord seam) | `llm/naming.py:74-95` (cipher live, test-guarded) |
| LC-007 | Humanoid gear schema in export | VERIFIED (not yet fixed) | `export/schemas.py:88-89`; `telemetry/migrations.py:_V1_6` |
| LC-003 | Modifier floor-lock telemetry gap | DRIFT-FROM-AUDIT | `floor_lock_recompose/working_modifier/floor_lock_detected` absent from schema and recorder |
| LC-008 | STR/DEX/INT in LLM prompt | NEEDS-DOWNSTREAM-FIX | `llm/naming.py:323` stats.as_dict() in name_class prompt |

### W1.13 ArchiveEntry Schema-Extension Scope

None of the W1.13 ArchiveEntry fields (`node_subset`, `per_node_coefficients`, `scalar_modifier`, `bc_coordinate`, `per_tier_WR`, `cohesion_theme`, `visual_identity`) exist in the star-lord seam. Requires new `archive_entries` table (not an extension of existing tables). Matt authorization required for DB migration. Export schema change not needed until P3.

### W0.8 `bounce_count` + `spawn_count` Scope (P1 W1.1)

Clean additive extension: 2 nullable columns on `abilities` table. 4 files, ~20 lines, no round-trip breakage. Matt authorization required for DB migration.

### v2.12 + v2.13 Schema Status

Both LIVE as of 2026-05-19 production DB apply. No drift.

### Recompose-Hive P1 Fields

`floor_lock_recompose`, `working_modifier`, `floor_lock_detected` are specced in gamora's `simulation/MIGRATION.md` but absent from star-lord telemetry schema and recorder. This is a P1-priority cross-seam gap — if gamora ships Option B before star-lord adds the columns, these fields will be silently dropped. Routed to knight-rider for P1 dispatch scoping.

### MEDIUM-Risk LCs — Quick Verdict Table (Star-Lord Touches)

| LC | Star-Lord Touch? | Status |
|---|---|---|
| LC-013 | No | rocket seam only |
| LC-015 | No | gamora seam only |
| LC-016 | No | gamora seam only |
| LC-017 | Partial (no pack-fight tag column) | W0.9 follow-on item |
| LC-018 | No | generation/gamora seam |
| LC-019 | Confirmed absent | consistent with deferred status |
| LC-020 | Schema ready (per-tier WRs recorded) | consistent with A3-primary design |
| LC-021 | Schema ready (observed_movement_speed NULL) | upstream unblocked; schema live |
| LC-022 | canonical-7-ready (D6 Coupling #9 live) | ready for substrate expansion |
| LC-023 | No fight-context discriminator column | P0/W0.9 follow-on item |
| LC-024 | No | gamora seam |
| LC-025 | No | generation/gamora seam |
| LC-026 | base_mana column queryable for bug evidence | empirical jack-ryan DB query |
| LC-027 | No | gamora/generation seam |
| LC-028 | No word-count validation at write boundary | acceptable for current scope |
| LC-030 | No cost_type column on abilities | P1 substrate enrichment scope |

---

## Rocket Section (Generation Seam)

**Status: PENDING — rocket to append**

---

## Gamora Section (Simulation Seam)

**Status: PENDING — gamora to append**

---

## Jack-Ryan Review

**Status: PENDING — after all 3 seam sections present**
