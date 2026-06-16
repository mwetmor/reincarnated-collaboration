# Dispatch — 2026-06-13 — rocket — fix grouping-vocab loader path (D6, 9-module collection break)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-06-13 (D6 disposition — "assign a cleanup owner; you route it"). KR routed to rocket (foundation seam).
**Status:** READY — fire when convenient (cleanup; unblocks the engine test suite's full collection).
**Estimated effort:** ~minutes (one path fix + collection re-verify).

## The break (diagnosed by KR)

`python3 -m pytest --collect-only` aborts with **9 collection errors**, all the same root cause:

```
src/reincarnated/foundation/grouping_vocabulary_loader.py:174: RuntimeError:
  Cannot locate grouping-layer-vocabulary.md. Tried:
    .../reincarnated-collaboration/canonical/story/grouping-layer-vocabulary.md
  Set GROUPING_VOCAB_DOC_PATH env-var to override.
```

**Root cause:** the doc was **moved** to `canonical/story/historical/grouping-layer-vocabulary.md` in collab commit `93b8427` ("docs(canonical): structural restructure — HISTORICAL to historical/..."). The loader's path candidates (lines ~160–180 of `grouping_vocabulary_loader.py`) still point at the **pre-move** `canonical/story/grouping-layer-vocabulary.md`, so the lookup fails and 9 modules abort at collection.

**Affected modules (all collection-blocked):** `test_b6_generator_wired`, `test_cosmological_vocabulary`, `test_cp8_gear_naming`, `test_gear_integration`, `test_integration`, `test_naming`, `test_no_canonical_four_in_llm_prompts`, `test_role_orientation`, `test_spirit_guide_orchestrator_wiring`.

## The decision you must make (foreground it in your fix)

The doc is now in `historical/` — which implies someone judged it historical/superseded. **Before pointing the loader at `historical/`, confirm that `historical/grouping-layer-vocabulary.md` IS still the authoritative grouping-layer vocabulary the loader should consume** (i.e. it wasn't superseded by a newer live doc elsewhere). 
- If it IS the live authority despite the `historical/` location → either update the loader candidates to include `canonical/story/historical/grouping-layer-vocabulary.md`, OR (cleaner, if it's genuinely current) flag to KR that the doc may have been mis-filed into `historical/` by the restructure (a docs-side question — KR routes to gandalf if so; do NOT move canonical docs yourself).
- If a NEWER live grouping-vocab doc exists → point the loader at that.

Document which you found and why in the fix.

## Scope

- [ ] Confirm the authoritative grouping-layer-vocabulary doc location (per the decision above)
- [ ] Update `foundation/grouping_vocabulary_loader.py` path candidates so the lookup resolves (additive — keep the env-var override + existing fallbacks)
- [ ] `pytest --collect-only` re-verifies: **0 collection errors** (the 9 modules collect)
- [ ] Run the 9 previously-blocked modules — confirm they pass (or surface any real failures that were masked by the collection abort)
- [ ] AGENT_STATE.md updated; Tag: `rocket/v-grouping-vocab-loader-fix-1`
- [ ] If the doc looks mis-filed into `historical/` (a canon-placement question), surface to KR — do NOT relocate canonical docs (gandalf's seam)

## Out of scope

- Relocating / re-authoring canonical grouping-vocab docs (gandalf's canon seam — surface, don't act)
- Any generation-logic change beyond the loader path
- Pushing to remote (Matt's gate)

## References

- D6 in `agentic_orchestration/cert-wave-2d-W-D-close-2026-06-13.md`
- Move commit: collab `93b8427`

---

**Author:** knight-rider, 2026-06-13. A docs-restructure (`93b8427`) orphaned the foundation loader's path; rocket repairs the path (foundation seam), surfacing any canon-placement question rather than relocating canonical docs.

---

## Completion record

**Completed by:** rocket, 2026-06-14 — commit `d583f64`, tag `rocket/v-grouping-vocab-loader-fix-1`.
**Closure verified by:** knight-rider, 2026-06-16 (autonomous run, Wave 1).

### Deliverable — COMPLETE

`_resolve_vocab_doc_path` now tries `canonical/story/historical/grouping-layer-vocabulary.md` FIRST (the sole on-disk copy + the boot-time YAML the engine actually reads), with the pre-move path retained as a self-healing fallback across both base resolutions. Env-var override + fail-loud preserved (additive — Pattern P7 not weakened).

- **Collection restored:** `pytest --collect-only` → **5796 collected, 0 errors** (was 9 collection errors). The 9 modules that aborted at collection now collect and run.
- **Decision foregrounded (per the dispatch's required judgment):** the `historical/`-filed doc IS the de-facto live authority — no live successor carrying the `grouping_vocabulary:` YAML exists; `naming.py`, `cosmological_vocabulary.py`, `season_writer.py` all boot against it. Its `STATUS:HISTORICAL-INFORMATIVE` flag is therefore a **canon-placement question** (a doc may be mis-filed in `historical/` while remaining live authority). **SURFACED to KR — not relocated** (gandalf's canon seam). See PARK (c) below.

### Characterization of the unmasked failures — PARKED (Tier-3 test-health surface)

KR ran the full previously-blocked set to ground-truth what the collection abort had been masking: **13 failed, 297 passed, 6 skipped** (2859s / 47:39 — genuine heavy generation/integration compute, not a hang). These failures are **pre-existing**, UNMASKED by the collection fix, NOT caused by the path-only change, and OUT OF D6 SCOPE. They split into two families:

- **Family A — b6-generator structural/constraint/balance (5), `test_b6_generator_wired.py`:** `TestBucket1Structural::test_t1_skills_have_no_parents`, `::test_t2plus_parent_is_tier_n_minus_one`; `TestBucket2Constraint::test_chain_count_within_template_bounds`, `::test_skill_count_within_template_bounds`; `TestBucket4BalanceGate::test_taxonomy_doppelganger_in_band`.
- **Family B — element-naming / no-canonical-four (8):** `test_naming.py` (`test_name_skill_with_energy_type`, `test_name_class_includes_energy_type_in_prompt`); `test_no_canonical_four_in_llm_prompts.py` (`test_skill_with_elements_and_vocab`, `test_all_four_canonical_elements`, `test_class_with_elements_and_vocab`, `test_class_without_elements`, `test_class_skills_summary_no_canonical_four`, `test_all_elements_monsters`). (rocket's commit body also flagged `test_theme_element_is_rotating` — 'brand' flavor vs rotating-canonical-7 — in the same pre-existing-drift class.)

**Why Tier-3 (parks, does not auto-resolve):** each requires a product-bug-vs-stale-test judgment (is the generator wrong, or has the test fallen behind a deliberate spec change?). That is a design/spec call, not a loader-fix deliverable — exactly the kind of question the autonomous envelope parks for Matt rather than promoting into a decision while he is away. See return-package PARKING LOT.

**D6 STATUS: CLOSED on its deliverable** (collection unblocked; 297 tests now run that could not before). The 13 unmasked failures are a separate, newly-VISIBLE test-health surface — handed to the parking lot, not folded into this dispatch's scope.
