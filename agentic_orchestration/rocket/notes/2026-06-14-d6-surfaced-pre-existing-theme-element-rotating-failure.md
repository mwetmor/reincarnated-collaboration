# D6 surfacing — pre-existing `test_theme_element_is_rotating` failure unmasked by the collection fix

**Author:** rocket (generation/foundation seam)
**Date:** 2026-06-14
**Context:** autonomous Run B, Unit 1 (D6 grouping-vocab loader fix). The dispatch
(`dispatches/2026-06-13-rocket-grouping-vocab-loader-fix.md`) instructs: *"Run the 9 previously-blocked
modules — confirm they pass (or **surface any real failures that were masked by the collection abort**)."*
This note is that surfacing. **Per dispatch out-of-scope ("Any generation-logic change beyond the loader
path"), I did NOT fix it in the D6 unit — I surface it for KR to route.**

## The failure

```
tests/test_integration.py::TestSeasonOrchestrator::test_theme_element_is_rotating
  rotating = {e.name for e in foundation.get_rotating_elements()}
  assert season_output.season_theme_element in rotating
E AssertionError: assert 'brand' in {'earth','fire','holy','lightning','shadow','water', ...}
```
(heavy-pair run 2026-06-14: `tests/test_integration.py` + `tests/test_gear_integration.py` → **1 failed, 67 passed**, 404s.)

## Why it is NOT caused by the D6 loader fix (diagnosed, not assumed — Disc #11)

- The D6 fix changes **only** `foundation/grouping_vocabulary_loader.py::_resolve_vocab_doc_path` — a pure
  path-resolution change so the loader finds `grouping-layer-vocabulary.md` at its post-restructure
  `canonical/story/historical/` location. The **doc content loaded is byte-identical** to pre-move (same
  sole file, just relocated).
- The failure is about **theme-element selection vs the rotating-element set**, neither of which is the
  grouping-vocab doc:
  - `'brand'` is a **seasonal flavor element** in `data/seasonal_elements/pool.json` (confirmed present).
  - `get_rotating_elements()` returns the **canonical rotating substrates** from `foundation/foundation.py`
    (`{earth, fire, holy, lightning, shadow, water, wind}` — canonical-7, the `e.rotating` set).
- The season orchestrator picked a **seasonal/flavor element name** (`'brand'`) as `season_theme_element`,
  but the test asserts the theme element must be a **canonical rotating substrate**. That mismatch is a
  generation-logic / pool-vs-foundation drift, independent of the loader path.

## Why it was latent until now

The module aborted at **collection** (the loader `RuntimeError` the D6 fix repairs), so this test **never
ran** — the divergence has been masked. Unblocking collection unmasked it, exactly as the dispatch
anticipated.

## Likely root (for KR/gandalf to confirm — NOT acted on here)

Smells like **Q18 / Epoch-4 drift**: `pool.json` has a `pool.json.pre-q18-2026-06-01-backup` sibling, and
ground-state records the **season concept ARCHIVED (Matt 2026-06-02)** — "per-skill LLM flavor element …
applied only … within the naming of the skill." A legacy `TestSeasonOrchestrator` that asserts
`season_theme_element ∈ rotating-canonical-7` may be testing **pre-Q18 season-theme behaviour** against a
**post-Q18 flavor-bearing pool** that now surfaces names like `'brand'` as theme candidates. If so the fix
is one of: (a) constrain theme-element selection to the canonical rotating set; (b) update/retire the
legacy assertion to the post-Q18 flavor-vocabulary contract; (c) the test is archived-behaviour and should
be xfail/removed. **This is a design-contract call (gandalf) + a generation-logic change (rocket), NOT a
D6-loader-fix change** — hence surfaced, not patched.

## Disposition

- **D6 deliverable stands:** `pytest --collect-only` → **5796 collected, 0 errors** (was 9 collection
  errors). 8 of the 9 previously-blocked modules collect-and-pass; the 9th (`test_integration`) collects and
  is **67 passed / 1 failed**, the single failure being this pre-existing unmasked drift.
- **Routing ask to KR:** route the `test_theme_element_is_rotating` fix as a **separate generation-logic
  item** (rocket seam) gated on a gandalf theme-element-vs-flavor-pool design-contract confirmation. Pairs
  with the D6 canon-placement question already surfaced (the `historical/`-filed grouping-vocab doc).
