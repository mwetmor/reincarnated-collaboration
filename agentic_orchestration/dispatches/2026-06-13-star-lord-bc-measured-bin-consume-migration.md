# Dispatch — 2026-06-13 — star-lord — BC measured-bin consume-side MIGRATION (fast-follow)

**From:** knight-rider
**To:** star-lord
**Approved by:** Matt 2026-06-13 — in-scope to the authorized BC-measurement keystone; telemetry/export is internal-to-engine (not an external-system write), so this is auto-commit-eligible star-lord seam work. No Matt sign-off needed; push-to-remote is his only gate, at keystone-close.
**Status:** SEQUENCED — DO NOT START until gamora's emit-side schema lands. This is a fast-follow on the gamora BC-measurement pipeline build (`2026-06-13-gamora-bc-measurement-pipeline-build.md`). Picks up the moment gamora writes the emit-side MIGRATION section defining the per-kit MEASURED-bin record shape.
**Estimated effort:** ~2–4 hours once the emit schema exists (consume-side wiring + any required telemetry-signal emission)
**Acceptance:** export/telemetry consumes gamora's per-kit MEASURED Axis 4 / Axis 3B bin records cleanly; round-trip verified; consume-side MIGRATION.md section authored per ADR-004.

## Context

This is the export-seam half of the BC-measurement keystone's cross-seam boundary. gamora is building the BC-measurement pipeline (keystone middle link — confirmed by KR 2026-06-13 to not previously exist). gamora EMITS the per-kit MEASURED-bin record; you CONSUME it on the export side. Two possible work items, gated on what gamora's math-note signal audit finds:

1. **Always:** consume-side MIGRATION for the new MEASURED-bin record (export packet / season JSON shape). Author the MIGRATION.md section so the schema round-trips.
2. **Conditional:** if gamora's telemetry-signal availability audit (their math note, anchored to `qd-engine-bc-axes-lock-2026-05-20.md` lines 511–545) finds the current sim does NOT emit a needed raw signal — candidates: per-hit damage-application logs (not just totals), HoT-recovery-distinct-from-mitigation, avoidance tags (`grants_evasion`/`grants_stealth`/`grants_iframes`/`grants_reflection`) — gamora flags the exact field list to KR, and that raw-signal emission is YOUR telemetry MIGRATION. Bins that stay un-measurable route to the lock doc's deferred-evaluation pool (substrate evidence, not a failure).

## Required reading before starting (after gamora schema lands)

- `agentic_orchestration/dispatches/2026-06-13-gamora-bc-measurement-pipeline-build.md` (the emit-side dispatch + gamora's completion record / emit MIGRATION section)
- gamora's BC-measurement math note in `simulation/math/` (the signal-availability audit — tells you whether item 2 above fires)
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` §§ 3.6 / 3.7 + lines 511–545 (deferral matrix / telemetry-signal gaps)
- `src/reincarnated/export/MIGRATION.md` + `src/reincarnated/simulation/MIGRATION.md` (existing schema chain)

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring)

**YES** — you are the consume side of gamora's emit boundary, and possibly the emit side of a new raw-telemetry signal. Production-DB migration (if any new telemetry column) requires Matt authorization per ADR-006 — flag the migration to KR; dry-run/smoke is yours, production apply is Matt's gate. The deferred carry-forward v2.16 production migration in your AGENT_STATE is unrelated and stays Matt-gated.

## Out of scope

- gamora's emit-side pipeline / math note (simulation seam)
- The locked BC axis edges / vocabulary
- The weapon/substrate BC clustering line (Cycle 14/15 — different work)

## Tag intent

`star-lord/v-bc-measure-consume-<n>`. Auto-commit per standing pattern (telemetry-internal). Push at keystone-close, Matt's gate.

---

**Author:** knight-rider, 2026-06-13. Sequenced as fast-follow on the gamora BC-measurement build; fires on gamora emit-schema landing.
