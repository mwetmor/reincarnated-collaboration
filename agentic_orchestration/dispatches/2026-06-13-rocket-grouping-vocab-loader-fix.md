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
