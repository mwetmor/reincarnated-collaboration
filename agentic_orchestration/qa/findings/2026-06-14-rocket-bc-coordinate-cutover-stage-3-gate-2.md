# Finding — 2026-06-14 — rocket BC-coordinate cutover Stage 3 (IRREVERSIBLE deletion, the GOAL)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-AMENDMENTS (no BLOCK)
**Target:** commit `695b70f` / tag `rocket/v1.1-bc-coordinate-cutover-stage-3` (NOT pushed)
**Developer:** rocket
**Principles applied:** 2 (smoke-gate), 3 (cross-seam impact / MIGRATION.md), 4 (decisions/design-contract as truth); Disciplines #2, #11, #12

## What I found

Verified at source (not self-report — the cut is irreversible). The deletion is EXACTLY the gandalf-pinned 2-symbol set `{G1 ARCHETYPES_FORBIDDEN_CLOSE_RANGE, G9 legacy_archetype_shim}` plus the co-requisite shim-test block, with NO scope creep. Commit stat: 7 files, +113/-388. `legacy_archetype_shim.py` is gone (`git rm`, 206 lines). G1 frozenset removed from `b6_archetype_templates.py`; its dead `noqa:F401` import removed from `season_orchestrator.py`. The shim-test block (`TestLegacyArchetypeShim` + import block + `test_shim_produces_coverage_across_bc_space`) removed from `tests/test_w02_bc_target_composer.py`; composer-side imports/tests retained.

**No scope creep — HELD set verified intact at source.** `ARCHETYPE_ROLE_PRIORITY` + `_PLAYER_CONTROLLER_ARCHETYPES` present (`simulation/ai_strategies.py:52`, `:45`). Stage-3b fork machinery present: `classify_archetype`, `B6KitBuilder`/`KitConstraintError`, `archetype_composer`, `b6_archetype_templates.ARCHETYPE_TEMPLATES` all resident. **G7 cross-seam (R-2) confirmed intact** — `balance_loop.py` consumers at lines 1884/1886, 1946/1948, 2025/2030, 2177/2183 all present and untouched.

**No live consumer of either deleted symbol survives.** grep `src/` for `ARCHETYPES_FORBIDDEN_CLOSE_RANGE`, `legacy_archetype_shim`, and all 7 shim-exported names returns ONLY prose (docstrings, comments, the inverse-direction acceptance-guard at `bc_target_source.py:13-16`). Zero `import`, zero call site.

**Behavior-identical confirmed.** Post-cut artifact `…_225523.json`: ELEMENTAL_LEAK=0, PHYSICAL_LEAK=0, EXPERIMENTAL_OR_WEIRD=0, PASS=true, both label-input sites empty (`site1_ARCHETYPE_ROLE_PRIORITY: {}`, `site2_PLAYER_CONTROLLER_ARCHETYPES: {}`). The proof-relevant invariant matches the pre-cut baseline `…_214135.json` (the artifact gandalf adjudicated against, `b5af4b9`) exactly — same 0/0/0/PASS, same empty sites. (Run params differ — n_classes 12→10, fights 4→100, different per-class archetype draws — but the zero-label-firing invariant, which is what the proof asserts, is identical. That is the prove-side of prove-then-delete.)

**Test collection clean.** Re-ran at HEAD: 5810 tests collected, 0 collection errors. `tests/test_w02_bc_target_composer.py` → 45 tests (shim methods gone). The co-requisite deletion did its job — no dangling shim import hard-fails collection.

**Pre-existing failures confirmed genuinely pre-existing, NOT introduced by this cut.** 19 `tests/test_range_profile.py` failures at HEAD, matching rocket's count. Decisive check: `git diff 8ab02c0 695b70f -- tests/test_range_profile.py` is EMPTY and `git show 695b70f --stat` does not list the file — this commit did not touch it, so it cannot have introduced the failures. Failure mode is content assertion (`archetype='physical_warrior' == 'physical_grappler'`), the Stage-1 physical-pool deferral, not an ImportError/NameError from the deletion. The two `ARCHETYPES_FORBIDDEN_CLOSE_RANGE` mentions in that file (lines 1778, 1794) are comment-only; collection succeeds. No real regression hiding behind the label.

**R-4 correction confirmed.** `class_generator.py:21-22` `noqa:F401` comments corrected from the false "dead on live path" claim to "LIVE on the physical fork; HELD for Stage 3b." The guarded symbols (`KitConstraintError`, `ARCHETYPE_TEMPLATES`) were NOT deleted.

**MIGRATION.md** documents the deletion, rationale (green proof), the Stage-3b generation-seam-only reframe, the R-2 G7 cross-seam gate, downstream-consumer NONE-break analysis, and the pre-existing-failure note. Per ADR-004.

## Amendment (non-blocking, cosmetic) — dangling shim doc pointers

Four docstrings/comments still name the deleted `legacy_archetype_shim.py` as if it exists:
- `b6_archetype_templates.py:15` ("see legacy_archetype_shim.py which translates…") and `:326` ("…and legacy_archetype_shim.py is removed")
- `archetype_composer.py:15` (same "see legacy_archetype_shim.py" prose)
- `bc_target_composer.py:880` ("preserved via legacy_archetype_shim.py for backward compatibility")

**Assessment: cosmetic, NOT gating.** These are pure prose with no `import` and no behavioral effect — they cannot break collection, generation, or simulation, and the green proof + clean collection already prove they are inert. They are stale module/function docstrings pointing at a now-deleted file, which mildly misleads a future reader (the same staleness class as the R-4 noqa comments rocket just corrected, just lower-stakes because these are descriptive narrative rather than a deletion-decision signal). Recommend a follow-up doc-only cleanup pass to re-point or remove them; it does NOT need to block this gate or the program push. Note `b6_archetype_templates.py:326` is mildly ironic — it says removal happens "when … legacy_archetype_shim.py is removed," and that has now happened, so that whole deprecation-banner block is itself ripe for the same cleanup.

## Rationale

- **Principle 2 (smoke-gate / Discipline #2):** behavior-identical full-season generate→simulate proof present and matches baseline invariant. Satisfied.
- **Principle 3 / ADR-004 (cross-seam / MIGRATION.md):** MIGRATION.md present, documents the deletion + the R-2 G7 cross-seam HOLD-SIM gate. The cut itself drops no emitted/cross-seam field (the start-of-pipe machinery is distinct from the end-of-pipe `archetype_tag` output). Satisfied.
- **Principle 4 (design contract as truth):** deletion is byte-faithful to gandalf's pinned set (`b5af4b9`) and the dispatch scope; the out-of-scope HELD list is verified untouched at source. Satisfied.
- **Discipline #11 (empirical inspection over assumption):** every claim re-verified at source rather than trusted from the completion record — required for an irreversible cut.
- **Discipline #12 (semantic-shifting fixes need explicit framing):** the deprecation-banner-style prose pointers (the dangling-doc amendment) are exactly the in-place-deprecation narrative #12 governs; correcting them keeps the narrative honest. Non-gating because no behavior shifts.

## Action

- [x] Developer (rocket): cut verified clean — pinned set exactly, no scope creep, behavior-identical, collection clean, R-4 corrected. No required pre-push action.
- [ ] Developer (rocket), follow-up (doc-only, non-blocking): re-point or remove the 4 dangling `legacy_archetype_shim.py` doc pointers (`b6_archetype_templates.py:15,:326`, `archetype_composer.py:15`, `bc_target_composer.py:880`). jack-ryan pre-approves this as a documentation-only change per ADR-002 — no separate Gate-2 needed.
- [ ] knight-rider: nothing blocks the program push. Cleared.
- [ ] Matt: no decision needed (no BLOCK). FYI — the IRREVERSIBLE cut is verified clean against the green proof; the elemental-path lock is now structural.

## References

- Commit/diff: `695b70f` (`git show 695b70f`)
- `~/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (Stage-3 entry)
- `~/Games/reincarnated-engine/src/reincarnated/generation/b6_archetype_templates.py`, `class_generator.py`, `season_orchestrator.py`
- `~/Games/reincarnated-engine/tests/test_w02_bc_target_composer.py`, `tests/test_range_profile.py`
- `~/Games/reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (G7/R-2 consumers), `ai_strategies.py` (HELD tables)
- Post-cut proof: `~/Games/reincarnated-engine/output/bc-stage3-zero-label-proof-20260614_225523.json`; pre-cut baseline `…_214135.json`
- Design contract: `agentic_orchestration/gandalf/notes/2026-06-14-stage-3-consolidated-design-adjudication.md` (`b5af4b9`)
- Dispatch: `agentic_orchestration/dispatches/2026-06-14-rocket-bc-coordinate-cutover-stage-3.md`
