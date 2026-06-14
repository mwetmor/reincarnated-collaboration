# Dispatch — 2026-06-14 — rocket — BC-coordinate cutover, Stage 3 (irreversibility deletion — THE GOAL)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-06-14 (final GO authorized on the irreversible cut, set pinned by gandalf b5af4b9)
**Estimated effort:** bounded — two symbols + co-requisite test block + comment corrections
**Acceptance:** the pinned narrow-Stage-3 deletion set `{G1 ARCHETYPES_FORBIDDEN_CLOSE_RANGE, G9 legacy_archetype_shim}` + the co-requisite shim-test block are physically deleted; a full season generates + simulates behavior-identically; the test suite still collects; the elemental-path lock is structural (nothing to revert to).

## Context

This is **Stage 3 of the three-stage BC-coordinate-identity cutover — THE GOAL.** Stage 1 (generation compose-from-bc_target, elemental partial) and Stage 2 (simulation AI bin-keying) are LANDED and gate-cleared. Matt ruled Stage 3 **NARROW** (gandalf scope ruling `a4bf91f`): delete only the elemental-abandoned start-of-pipe archetype-tag machinery; HOLD the physical fallback to a deferred Stage 3b.

All three read-only prove-then-delete prereqs CLEARED:
- **gamora zero-label proof** (`8ab02c0`): full 12-class season, ELEMENTAL_LEAK=0, PHYSICAL_LEAK=0, PASS=true — no elemental kit fires any label-input path.
- **drax demo-VFX sweep** (`aaab426`): no Pixi VFX coupling breaks on `archetype_tag` deletion.
- **rocket + gamora reference-audits** (`5a4005c`, `8ab02c0`): pinned the exact elemental-only set.

gandalf's consolidated adjudication (`b5af4b9`) ratified the final set against the green proof. This dispatch executes it. **The cut is irreversible by design — that is the point: the elemental-path lock becomes structural, there is nothing to re-wire to.**

## Required reading before starting

- `agentic_orchestration/gandalf/notes/2026-06-14-stage-3-consolidated-design-adjudication.md` (`b5af4b9`) — **the pinned set + the three rulings; this is your contract**
- `agentic_orchestration/gandalf/notes/2026-06-14-stage-3-bc-cutover-scoping-ruling.md` (`a4bf91f`) — narrow scope + Stage 3b reframe
- Your own generation-side audit: `~/Games/reincarnated-engine/src/reincarnated/generation/notes/2026-06-14-stage-3-generation-reference-audit.md` (`5a4005c`) — the G-symbol map + R-1/R-2/R-4
- gamora sim audit + proof: `agentic_orchestration/gamora/notes/2026-06-14-bc-stage3-simulation-reference-audit.md` (the proof that justifies the cut)

## Math-before-code

Deletion, not algorithm — no math note required. The justification is the green zero-label proof (already run). Document the deletion rationale + the co-requisite in the MIGRATION.md.

## Scope — the pinned set (EXACTLY this; do not expand)

- [ ] **G1 — delete `ARCHETYPES_FORBIDDEN_CLOSE_RANGE`** (generation). V-8 was already re-pointed to `forbids_close_range` in Stage 1; the gate fires on the elemental branch only; the import is now dead (`noqa: F401`). Remove the symbol + its now-dead import.
- [ ] **G9 — delete `legacy_archetype_shim`** (generation). Zero live `src/` importers; dead on both paths; it was the W0.2.4 label→BC bridge (inverse of the cutover).
- [ ] **Co-requisite — delete the shim-test block** in `tests/test_w02_bc_target_composer.py` (the shim-import block + the shim test methods, e.g. "Verify shim path produces kits for all 24 archetype tags"). **Delete in the SAME commit** or test collection hard-fails on the missing import. Composer-side imports/tests STAY.
- [ ] **R-4 hygiene — correct the stale `noqa` comments** at `class_generator.py:21-22` (they falsely claim the symbols are dead post-cutover; they are live on the physical fork). Correct, don't delete the symbols they guard.
- [ ] Smoke-test: a full season generates + simulates behavior-identically (this is the acceptance proof — re-run a representative season end-to-end)
- [ ] Test suite still COLLECTS (the co-requisite deletion verification)
- [ ] MIGRATION.md authored (the deletion + rationale + the Stage-3b reframe note)
- [ ] AGENT_STATE.md updated
- [ ] Tag: `rocket/v?.?-bc-coordinate-cutover-stage-3`

## Out of scope (explicit non-goals — DO NOT TOUCH)

- **`ARCHETYPE_ROLE_PRIORITY` + `_PLAYER_CONTROLLER_ARCHETYPES`** — PERMANENT-HELD (monsters + experimental, the bc_target-absent population). NOT Stage 3b, NOT ever-deleted by this program. Do not touch.
- **Stage 3b machinery** — G4 `classify_archetype` / G5 `archetype_composer` / G7 b6 `ARCHETYPE_TEMPLATES` kit-dict / G8 `B6KitBuilder`+`KitConstraintError` (the `if is_physical:` fork). HELD; gated on physical-pool expansion landing. Do NOT delete.
- **G7 specifically** — also HOLD-SIM (consumed by `simulation/balance_loop.py`); carries an independent cross-seam gate (R-2). Out of scope regardless.
- **Any symbol not in the pinned `{G1, G9}` set.** No scope creep on an irreversible cut.

## Acceptance criteria

- [ ] `ARCHETYPES_FORBIDDEN_CLOSE_RANGE` and `legacy_archetype_shim` are physically gone from `src/`
- [ ] The shim-test block is deleted in the same commit; `tests/` collects clean
- [ ] A full season generates + simulates behavior-identically (no regression vs the Stage-2 baseline)
- [ ] `class_generator.py:21-22` comments corrected
- [ ] MIGRATION.md documents the deletion + the Stage-3b reframe
- [ ] Gate: jack-ryan Gate-2 confirms behavior-identical season + test collection + R-4 correction

## References

- gandalf consolidated adjudication `b5af4b9` (pinned set); scope ruling `a4bf91f`
- gamora zero-label proof `8ab02c0` (the prove-then-delete evidence)
- Per-stage gate: jack-ryan Gate-2 (on the deletion)
