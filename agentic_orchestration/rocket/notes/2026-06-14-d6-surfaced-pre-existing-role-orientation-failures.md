# D6 surfacing (batch 2) — four pre-existing `test_role_orientation.py` failures unmasked by the collection fix

**Author:** rocket (generation/foundation seam)
**Date:** 2026-06-14
**Context:** autonomous Run B, Unit 1 (D6 grouping-vocab loader fix). Sibling to
`2026-06-14-d6-surfaced-pre-existing-theme-element-rotating-failure.md`. The dispatch
(`dispatches/2026-06-13-rocket-grouping-vocab-loader-fix.md`) instructs: *"Run the 9 previously-blocked
modules — confirm they pass (or **surface any real failures that were masked by the collection abort**)."*
This note surfaces a second cluster (4 failures in `tests/test_role_orientation.py`). **Per dispatch
out-of-scope ("Any generation-logic change beyond the loader path"), I did NOT fix them in the D6 unit —
I surface them for KR to route.**

## The failures (`tests/test_role_orientation.py` — 4 failed, 180 passed, 4 skipped)

| # | Test | Assertion | Result |
|---|---|---|---|
| 1 | `TestControllerStatTemplates::test_earth_controller_has_less_wis_than_earth_caster` | `ARCHETYPE_TEMPLATES["earth_controller"]["wisdom"] < ARCHETYPE_TEMPLATES["earth_caster"]["wisdom"]` | `assert 160 < 160` |
| 2 | `TestControllerStatTemplates::test_fire_controller_has_less_int_than_fire_mage` | `ARCHETYPE_TEMPLATES["fire_controller"]["intelligence"] < ARCHETYPE_TEMPLATES["fire_mage"]["intelligence"]` | `assert 160 < 160` |
| 3 | `TestClassGeneratorRolePlumbing::test_control_class_uses_controller_stat_template` | controller `wisdom` < damage-caster `wisdom` | `assert 160 < 159` |
| 4 | `TestRoleSkillTemplates::test_six_skills_added_in_some_seeds` | skill-count set == `{5, 6}` over 29 seeds | got `{5, 10, 11, 12}` |

Test #4 also logs: `WARNING reincarnated.generation.class_generator:542 B6 kit build failed for fire_mage
after retries; falling back to standard generator` (twice).

## Why these are NOT caused by the D6 loader fix (diagnosed, not assumed — Disc #11)

- The D6 fix changes **only** `foundation/grouping_vocabulary_loader.py::_resolve_vocab_doc_path` — a pure
  path-resolution change. The grouping-vocab **doc content loaded is byte-identical** to pre-move (same sole
  file, just relocated to `canonical/story/historical/`).
- The grouping-vocab doc feeds **grouping-layer naming**, NOT stat composition or skill-count.
- **Traced the actual data source** (not assumed):
  - `ARCHETYPE_TEMPLATES` (#1–3) is built by `stat_allocator._build_archetype_templates()` →
    `_get_composed_stat_profiles()` (D3 Coupling #3 composition). That function reads **only** `config/`
    (`load_substrate_identities`, `load_roles`) via `archetype_composer.get_composed_stat_profile`. **Zero
    grouping-vocab dependency.**
  - The skill-count (#4) comes from the B6 kit builder in `class_generator`. Also no grouping-vocab path.
- Therefore the path the grouping doc loads from cannot alter `wisdom=160`/`intelligence=160` template values
  or the per-seed skill count. **Independent of the D6 change.**

## Why they were latent until now

`test_role_orientation.py` imports `from reincarnated.foundation import load_foundation` (line 14), which
triggers the grouping-vocab loader at import. Before the D6 fix that loader raised `RuntimeError` at
**collection**, so the whole module aborted and **none of these 4 tests ever ran** — the drift was masked.
Unblocking collection unmasked it, exactly as the dispatch anticipated.

## Likely roots (for KR/gandalf/rocket to route — NOT acted on here)

Two distinct drifts:

**A. Composition drift (#1–3) — D3 Coupling #3.** When the hardcoded 16-profile `ARCHETYPE_TEMPLATES` dict
was replaced by composition-derived profiles (D3), the **controller-vs-caster differential on the primary
damage stat collapsed**: composition now caps both `earth_controller` and `earth_caster` wisdom at 160 (and
both `fire_controller`/`fire_mage` int at 160). The legacy tests encode a **design invariant** — "a
controller trades primary-damage stat for survivability, so controller primary-stat < pure-caster
primary-stat." That invariant is no longer honored by composition. Resolution is one of:
(a) restore the differential in the composition role-weights (`config/` roles) so controllers come in below
casters on the primary damage stat — a **generation-logic + config change (rocket seam)**;
(b) confirm with gandalf that the post-D3 design **intends** controllers and casters to share the primary-stat
cap (differentiating only on vitality), and **update/retire** the legacy invariant tests. This is a
**design-contract call (gandalf) + a generation/config change (rocket)**.

**B. Skill-count drift + B6 retry-fail (#4).** The test expects 5-or-6 skills per class (pre-B6 era). The
B6 kit builder now produces **10–12** skills (plus a `fire_mage` B6-build retry-fallback to the standard
generator). The `{5,6}` invariant is **stale** relative to the current B6 kit architecture. Resolution:
update the test's expected skill-count band to the B6 contract — but the **`fire_mage` B6-build
retry-failure warning** should be investigated separately (it may be a real B6 builder defect or an
environmental/LLM-auth artifact, given ANTHROPIC_API_KEY was removed 2026-06-12). **Generation-logic item
(rocket seam), gated on confirming the B6 skill-count contract.**

## Disposition

- **D6 deliverable stands.** These 4 are pre-existing masked generation drift, independent of the loader
  path fix, surfaced per the dispatch's explicit instruction. The D6 commit must NOT be amended for these.
- **Routing ask to KR:** route as **two separate generation-logic items** (both rocket seam), each gated on a
  gandalf design-contract confirmation:
  1. Composition controller-vs-caster primary-stat differential (#1–3) — restore vs retire-invariant.
  2. B6 skill-count contract + `fire_mage` B6-build retry-failure (#4).
- Pairs with the two D6 items already surfaced (the `test_integration` theme-element drift in the sibling
  note, and the `historical/`-filed grouping-vocab canon-placement question).

## Resolution log

- **2026-06-14 — Item #1–3 RESOLVED.** gandalf ruled (b) RETIRE the invariant
  (`agentic_orchestration/gandalf/notes/2026-06-14-controller-vs-caster-primary-stat-ruling.md`):
  the D3 shared-and-maxed primary cap (160) is ratified; primary stat is damage-only (not
  control-coupled); controller-vs-caster differentiation lives on the secondary budget (controller
  tankier VIT> + steadier DEX<). rocket rewrote the 3 assertions in
  `tests/test_role_orientation.py` accordingly (engine commit `e5a2da1`) — equal primary AND
  `controller.vit > caster.vit` AND `controller.dex < caster.dex`. **Composition/`config`/roles
  UNCHANGED — test-contract change only, no production behavior change.** Module result:
  76 passed / 4 skipped / 1 failed (the 1 = #4, intentionally untouched).
  - **→ FLAG to jack-ryan (DEV-MODE Gate-2, doc-grade):** per the ruling §4, this is a
    test-contract change encoding a ratified design contract with zero production behavior delta.
    Requested disposition is **doc-grade Gate-2 awareness, NOT a behavior gate**. Diff: 3 assertions
    in one test file (`tests/test_role_orientation.py`, commit `e5a2da1`). No `MIGRATION.md` (no
    schema/API change). No smoke-regen required (no generator behavior touched).
- **2026-06-14 — Item #4 RESOLVED (both halves: structural fix + test rewrite).** gandalf ruled
  (`agentic_orchestration/gandalf/notes/2026-06-14-two-generation-rulings-b6-kit-band-and-theme-element-flavor-pool.md`,
  RULING A): the `{5,6}` invariant was a **false-green** masking a real fire_mage B6 fallback defect.
  Two work-units:
  - **Structural fix (real behavior change, engine commit `9a46731`).** Diagnosed (Disc #11,
    `scripts/rocket_fire_mage_b6_constraint_diagnosis_2026_06_14.py`): the **sole** binding constraint
    was **`no_heal_skill` (38/38 failing attempts)** — NOT the ruling's hypothesised
    `require_dot_skill`/`require_burn_ailment` (DoT is a *required role* here; burn comes free from
    fire skills). Root cause: `_sample_free_roles` offered `sustain` to mage/caster archetypes, but
    fire_mage carries `no_heal_skill`, so every `sustain` draw tripped `_check_no_heal` → ~8% of kits
    exhausted `MAX_KIT_RETRIES` → fallback (2/29 seeds). Fix: constraint-aware free-role pool drops
    `sustain` when the template has `no_heal_skill` (gates on the constraint, not a hardcoded name, so
    water_mage's `require_heal_or_hot` sustain draw is untouched). Math pre-registered in
    `src/reincarnated/generation/math/fire-mage-b6-no-heal-pool-contradiction-2026-06-14.md`.
    **Validated: fire_mage fallback 2/29 → 0/29, length-set {10,11,12}, 29/29 first-try; water_mage
    unaffected.** → **standard Gate-2 (Disc #12)**; jack-ryan review requested.
  - **Test rewrite (doc-grade, engine commit `f48dde8`):** `test_six_skills_added_in_some_seeds` →
    `test_fire_mage_kit_size_in_b6_band` asserts `lengths ⊆ {10,11,12}` + variation; greens naturally
    from the fix (no `xfail` needed). → jack-ryan doc-grade Gate-2 awareness.
  - **The "B6 retry-fail" was NEVER env/auth.** B6 makes zero LLM calls; the ANTHROPIC_API_KEY removal
    was causally irrelevant, as the ruling §2.4 stated. The earlier surfacing note's env/auth caveat
    is hereby corrected — it was a pure constraint contradiction.
- **NEW observation surfaced (out of fire_mage scope) — `water_mage` 1/29 sub-band kit.** During the
  fire_mage fix's regression check, `water_mage` showed one seed producing a length-6 kit (1/29) of its
  own — i.e. an occasional water_mage B6 fallback, independent of and **pre-dating** my change (my gate
  does not fire for water_mage). Likely `require_heal_or_hot` or `require_chill_or_slow` occasionally
  binding against the water free-pool. **NOT fixed** (gandalf ruled fire_mage only). Routed to KR for a
  follow-on gandalf design-contract decision if water_mage reliability matters.
- **Theme-element drift (sibling note `...theme-element-rotating-failure.md`) — RESOLVED (doc-grade,
  engine commit `f48dde8`).** gandalf RULING B: `season_theme_element` is a naming-only flavor token
  post-Q18, not a rotating element. `test_theme_element_is_rotating` →
  `test_theme_element_is_valid_flavor_token` asserts membership in `data/seasonal_elements/pool.json`
  token set; `test_determinism` left untouched (still PASS). → jack-ryan doc-grade Gate-2 awareness.
