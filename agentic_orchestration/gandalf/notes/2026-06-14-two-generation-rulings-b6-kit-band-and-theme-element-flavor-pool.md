# The other two generation rulings — B6 kit-size band + theme-element-vs-flavor-pool drift

**Type:** design-contract rulings (gandalf seam) — resolve the remaining D6-surfaced generation-drift failures (#4 + the theme-element drift) named open in the controller-vs-caster ruling §6.
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-14 ("take the other two generation rulings").
**Empirical grounding:** direct code + decisions-log reads, 2026-06-14 (cited inline by file:line; Explore-agent composition audit + my own verification of the two failing tests and the two sourcing paths).
**Companion docs:**
- `agentic_orchestration/gandalf/notes/2026-06-14-controller-vs-caster-primary-stat-ruling.md` — the first of the three generation-drift rulings; this completes the set.
- `canonical/story/2026-06-02-season-archive-realm-expansion-pivot.md` — the Q18 pivot that supersedes the theme-element invariant (Ruling B).
- `canonical/37-form-bias-diagnosis-and-recovery.md` — the spine these three rulings all rhyme with (separate entangled dimensions; differentiate on real axes).
- decisions-log `2026-05-12: earth_caster B6 constraint ... deferred to B11` (`design/decisions/decisions-log.md:860-872`) — the exact precedent template for the fire_mage structural item (Ruling A §2.4).

---

## 0. TL;DR — two RULINGS

- **RULING A (B6 kit-size band):** **Retire the `{5,6}` skill-count invariant** in `test_six_skills_added_in_some_seeds`. It encodes the *pre-B6* probabilistic-6th-slot contract; B6 superseded it with a deterministic per-archetype kit-size band (fire_mage → `burst_damage` → `(10,11,12)`). Rewrite the test to assert the B6 band. **Load-bearing discovery: the stale `{5,6}` invariant was a FALSE-GREEN that masked a real fire_mage defect** — the fallback-5 kit made the test pass, hiding that B6 has been failing to build fire_mage kits since 2026-05-12. The rewrite *exposes* it. **The fire_mage B6-build failure is a SEPARATE rocket structural engineering item** (constraint-satisfaction, explicitly NOT env/auth), routed with the earth_caster deferred-restoration entry as its precedent template.
- **RULING B (theme-element drift):** **Retire/rewrite the `season_theme_element ∈ rotating-elements` invariant** in `test_theme_element_is_rotating`. The code already embodies the Q18 / season-archive pivot — it splits the *mechanical* theme (rotating, by construction) from the *output* `season_theme_element`, which is explicitly "the OUTPUT vocabulary token … used for naming prompts only, not mechanical generation" (`season_orchestrator.py:442-444`). The test conflates the two and asserts the *output flavor token* must be a *canonical rotating element* — a pre-Q18 contract the 2026-06-02 pivot archived. Rewrite to assert the output token is a valid flavor-naming token, not a rotating element.

Both are **test-contract changes, not generation-logic changes** — except the fire_mage *structural* item (Ruling A §2.4), which is real rocket engineering. Both rulings **ratify the post-refactor design** the code already implements.

---

## 1. The shared root cause — three failures, one cause (the meta-finding)

All three D6-surfaced generation-drift failures (controller-vs-caster + these two) have the **same shape**: a test encodes a **pre-refactor entanglement** that a dimensional/compositional refactor cleanly **separated**, and the test was never updated. The project's spine is *separating entangled dimensions into clean discriminating axes*; these stale tests are the last residue of the pre-separation world.

| Failure | Pre-refactor entanglement the test asserts | The refactor that separated it | Post-refactor truth |
|---|---|---|---|
| Controller-vs-caster (ruling 1) | primary stat carries control-vs-damage identity (`controller.primary < caster.primary`) | D3 composition (primary-first; role shapes the 110-pt secondary budget) | primary = damage-only; identity lives in skill kit + crit/defense lean |
| **B6 skill-count (Ruling A)** | skill-count is a loose probabilistic property (`{5,6}`) | B6 kit builder (deterministic per-archetype band) | skill-count is a tight per-archetype contract (`{10,11,12}` for burst_damage) |
| **Theme-element (Ruling B)** | season theme is one mechanical rotating identity (`theme ∈ rotating`) | Q18 / season-archive pivot (mechanical theme ≠ output naming token) | output `season_theme_element` = flavor-naming token; mechanical theme rotates separately, by construction |

This is the **same lesson as form-bias (doc 37) and the cert wave**: the engine keeps getting *more rigorous* about separating structure from flavor, mechanics from naming, real axes from flat scalars — and each separation orphans a test that asserted the old entanglement. Retiring these invariants is **consistent with the project's spine; restoring them would fight it.**

## 2. RULING A — B6 kit-size band (and the fire_mage false-green it unmasks)

### 2.1 The test and the stale invariant

`tests/test_role_orientation.py:565-571`:
```python
def test_six_skills_added_in_some_seeds(self, class_gen):
    """Some seeds produce 6 skills (optional slot hit); others 5."""
    lengths = set()
    for seed in range(1, 30):
        cls = class_gen.generate("fire", "fire", 50, seed=seed, role_orientation="damage")
        lengths.add(len(cls.skills))
    assert 5 in lengths and 6 in lengths, f"Expected both 5 and 6 skill lengths, got {lengths}"
```

`generate("fire", "fire", 50, role_orientation="damage")` → fire-scaling + damage role → **fire_mage** (`burst_damage`; `archetype_composer.py:76`). The docstring says it plainly: the `{5,6}` contract is the **pre-B6** `_generate_standard_skills` world — 5 base skills + a probabilistic 6th slot. That generator is now the **fallback safety net** (`class_generator.py:552`), not the path. The path is B6: `_KIT_SIZES["burst_damage"] = (10, 11, 12)` (`archetype_composer.py:109-110`), sampled by a triangular distribution (`b6_kit_builder.py:129-135`). The B6 band for fire_mage is **10/11/12 skills**, never 5 or 6.

### 2.2 The false-green discovery (the load-bearing part)

The observed length-set is `{5, 10, 11, 12}`. The `10/11/12` are B6 successes; the `5` is the **pre-B6 fallback firing** when B6 can't satisfy fire_mage's constraints. Here is the trap: **because the stale invariant accepted `5`, the fallback firing made the test GREEN** — so the test has been *certifying* a state where B6 silently fails for fire_mage. The `{5,6}` invariant wasn't merely stale; it was a **false-green masking a real archetype-fantasy break**. decisions-log:864 confirms this is not new — "Discovered when B6 corpus showed **fire_mage and earth_caster consistently producing pre-B6 kits**" (2026-05-12). earth_caster got a deferred-restoration entry (decisions-log:860-872); **fire_mage never did.** It has been falling back, masked, for a month.

Rewriting the invariant to the B6 band **`lengths ⊆ {10,11,12}`** makes the fallback **visible** — the test goes red on any fallback-5. That is the test doing its job for the first time.

### 2.3 The test rewrite (rocket; test-contract only)

Rewrite `test_six_skills_added_in_some_seeds` (rename → `test_fire_mage_kit_size_in_b6_band`) to assert the documented B6 contract:
- **Primary assertion:** `lengths ⊆ {10, 11, 12}` — every seed produces an in-band fire_mage kit (no fallback).
- **Spirit-preserving secondary (optional):** `len(lengths) >= 2` — the triangular distribution still varies the count across seeds (the original test's real intent: count varies seed-to-seed; now *within the band*, not 5-vs-6).
- **Source of truth:** the band is `design/b6-kit-composition-templates.md` (fire_mage 10/11/12) + `_KIT_SIZES["burst_damage"]`. Cite it in the docstring so the next reader doesn't re-derive it.

**Sequencing note (recognition→validate→commit):** the primary assertion will be **RED while the fire_mage structural defect (§2.4) persists** — which is *correct* (it exposes the defect). If rocket closes the defect in the same batch, the test greens naturally. If the fix is deferred (mirroring earth_caster→B11), mark the test `xfail(reason="fire_mage B6 constraint-satisfaction fallback — tracked as <rocket item / decisions-log entry>", strict=False)` so the contract is committed now, the suite stays non-blocking, and the test **auto-greens** when rocket lands the fix. Do **not** weaken the assertion to `{5,10,11,12}` to make it pass — that re-creates the false-green.

### 2.4 The fire_mage structural item (SEPARATE — real rocket engineering, NOT env/auth)

**This is NOT a test problem and NOT an auth problem.** B6 makes **zero LLM calls** (deterministic constraint-satisfaction); the ANTHROPIC_API_KEY removal (2026-06-12) is **causally irrelevant** to it. The fallback fires because B6 cannot, within `MAX_KIT_RETRIES = 5` (`b6_kit_builder.py:34,86-101`), assemble a 10-12-skill fire_mage kit satisfying its full constraint set:
- `require_primary_attack_skill` (burst_damage role; `archetype_composer.py:392`)
- `require_burn_ailment` + `require_dot_skill` (fire substrate; `:405`)
- `no_heal_skill` (fire+burst_damage; `:435`)

On exhaustion → `KitConstraintError` → `class_generator.py:540` fallback → 5-skill generic kit. **This is the exact failure class as earth_caster's `tier1_ground_slam_and_melee_arc` (decisions-log:860-872)** — a structurally-(near-)unsatisfiable constraint against the current skill pool.

**Design requirement (firm — mine):** a fire_mage **must** receive a burn-bearing, DoT-bearing, no-self-heal, 10-12-skill kit. **The fallback breaks the archetype fantasy.** A fire mage's identity in the genre *is* the deep burning/damage-over-time spell kit — Diablo III Wizard's deep fire pool, PoE's Ignite/Righteous-Fire DoT builds where the burn *is* the build. A fire_mage that silently degrades to a 5-skill generic kit with no guaranteed burn or DoT is **not a fire mage — it is a generic damage class wearing fire's name.** That is precisely the "performs meaning vs. means something" gap. The fallback is acceptable as a *crash-guard*; it is **not** acceptable as the *steady state* for a core archetype.

**Disposition (rocket's engineering call on the path; my call on the requirement):** rocket **diagnoses which constraint is binding** (likely `require_dot_skill` or `require_burn_ailment` against the available fire burst-tier pool), then either:
- **(i) Fix now** — close the skill-pool gap so the constraints are satisfiable (the pattern used for the warrior `require_gap_closer` gap-closer fix, decisions-log:715); or
- **(ii) Defer with documentation** — if the fix needs pool/geometry scope that's out of this batch, write a decisions-log entry **mirroring earth_caster's** (explicit deferred-restoration + TODO + the design intent preserved, decisions-log:868 discipline #12), and `xfail` the test per §2.3.

Either path keeps the design intent explicit and the defect *visible*. Silent fallback is the one outcome the ruling forbids.

## 3. RULING B — theme-element-vs-flavor-pool drift

### 3.1 The test and the conflation

`tests/test_integration.py:95-97`:
```python
def test_theme_element_is_rotating(self, season_output, foundation):
    rotating = {e.name for e in foundation.get_rotating_elements()}
    assert season_output.season_theme_element in rotating
```

It asserts the **output** field `season_output.season_theme_element` is a member of the **canonical rotating elements**. But the code already separates two different things (`season_orchestrator.py:440-473`):

1. **`theme_element` (mechanical generation input)** — `rotating[int(rng.integers(0, len(rotating)))].name` (`:446-447`). Rotating **by construction**, deterministic by seed. This is the real "the season's mechanical theme rotates" invariant — and it's enforced structurally, so it needs no test to protect it.
2. **`season_output.season_theme_element` (output vocabulary token)** — in legacy baseline mode, `elements.fire_slot.element_name` (`:471`), i.e. the **fire-slot flavor token drawn from the expanded flavor pool** (pool.json). The code comment is explicit: *"the OUTPUT vocabulary token (e.g. 'flicker') — used for **naming prompts only, not mechanical generation**"* (`:442-444`).

The test asserts (2) must satisfy the contract of (1). It conflates the **output flavor/naming token** with the **mechanical rotating theme**. Post-Q18, those are deliberately different objects.

### 3.2 Why this is a superseded contract, not a bug

`'brand'` is a legitimate fire-family flavor token (a valid `season_theme_element` example long predating this — `season_orchestrator.py:1154`). The Q18 pool expansion (109 entries) simply shifted the seed=42 fire-slot sample onto it, and `'brand'` is (correctly) **not** a canonical rotating element — so the test fails. **The failure is the test catching the code being correct.** The 2026-06-02 season-archive pivot archived the per-season *mechanical* theme concept and locked in *"flavor element = applied only within the naming of the skill."* `season_theme_element`-as-output is now a **flavor-naming token**, full stop.

**Genre framing:** in live-service ARPGs a "season theme" is a *mechanical* identity — a PoE league mechanic (Harvest/Delirium/Sentinel), a Diablo III season buff, a Diablo IV seasonal power. The pre-Q18 invariant treated `season_theme_element` as that kind of rotating *mechanical* league-identity. The pivot **decided not to build PoE-league-style per-season mechanical rotation into Phase 0.** Retiring this invariant **ratifies that decision**; keeping it asserts an abandoned league-mechanic design.

### 3.3 The test rewrite (rocket; test-contract only)

Rewrite `test_theme_element_is_rotating` (rename → `test_theme_element_is_valid_flavor_token` or similar) to assert what the output field **is** now:
- **Primary:** `season_output.season_theme_element` is a valid member of the **seasonal flavor pool** (the loaded `data/seasonal_elements/pool.json` token set) — the actual source via `elements.fire_slot`. This keeps a *real* invariant (the naming token is a legit flavor token, not garbage/empty) while dropping the false one (it's a canonical rotating element).
- **Minimal fallback** (if pool-membership is awkward in the fixture): assert it's a non-empty string. Weaker but still retires the false invariant.
- **Leave `test_determinism` (`:99-104`) untouched** — its `o1.season_theme_element == o2.season_theme_element` assertion is determinism-only and remains true.
- If you want to *preserve* the mechanical-rotation invariant explicitly, that belongs on the internal `theme_element` (the recorder `theme_selection` step metadata, `:448-453`), **not** the output field — but it's enforced by construction at `:446-447`, so a test is optional housekeeping, not load-bearing.

## 4. What rocket does (summary)

| Item | Type | Action |
|---|---|---|
| `test_six_skills_added_in_some_seeds` rewrite | test-contract | assert `lengths ⊆ {10,11,12}` (B6 band); rename; cite band doc; `xfail` if fire_mage fix deferred (§2.3) |
| **fire_mage B6 fallback** | **structural engineering** | diagnose binding constraint → fix-now (pool gap) **or** defer-with-decisions-log-entry (earth_caster pattern); design requirement = fire_mage gets a burn+DoT 10-12 kit (§2.4) |
| `test_theme_element_is_rotating` rewrite | test-contract | assert output token ∈ flavor pool (or non-empty); rename; leave `test_determinism` alone (§3.3) |

Two are low-gate test-contract changes (no production behavior change; tests encode a ratified contract — jack-ryan aware as Gate-2 doc-grade, not a behavior gate, same disposition as the controller-vs-caster rewrite). The **fire_mage structural item is a real behavior fix** → standard Gate-2 (Disc #12) if fixed in-batch, or a decisions-log deferred-restoration entry if deferred.

## 5. Genre/design anchor + AI-tell validation

Both rulings **validate the AI-tell line (D7)** — they ratify the engine's structure/flavor separation, the exact discipline D7 protects:
- **Ruling A:** B6 structural kit composition is **deterministic** (zero LLM calls). The LLM's role is flavor/naming only. The stale `{5,6}` test belonged to a looser-structure world; B6 tightened structure into a deterministic per-archetype contract. Confirming the band ratifies *structure = deterministic engine, not LLM.*
- **Ruling B:** the output `season_theme_element` is, in the code's own words, "used for naming prompts only." This **is** the Q18 pivot embodied: *flavor element = naming only.* Retiring the rotating-mechanical invariant ratifies *flavor drives naming, not mechanics.*

Same spine as the controller-vs-caster ruling and doc 37: **the engine differentiates on real, separated axes; the orphaned tests asserted the old entanglements.**

## 6. Disposition

- **Ruling A: RETIRE the `{5,6}` invariant; rewrite to the B6 band** (rocket, test-contract). **fire_mage B6 fallback = SEPARATE rocket structural item** (diagnose → fix-or-defer per earth_caster precedent); design requirement firm (burn+DoT 10-12 kit); fallback-as-steady-state forbidden. The rewrite intentionally exposes the defect (removes the false-green).
- **Ruling B: RETIRE/REWRITE the rotating-theme invariant** (rocket, test-contract). The code already implements the Q18 split; the test asserts the superseded pre-pivot contract. Rewrite to assert the output token is a valid flavor token.
- **Both → warm rocket session** (test rewrites; the same generation-triage batch as the controller-vs-caster rewrite + the Q4 code-flip, per controller-ruling §6). The fire_mage structural item rides the same session but is its own work-unit with its own gate.
- **KR generation-triage batch unit** (confirming controller-ruling §6): controller-vs-caster rewrite [DONE, e5a2da1] + **these two test rewrites** + **fire_mage structural diagnosis** + the Q4 code-flip — all rocket-seam, gandalf-contract-gated.
- **Still queued (named, not ruled here):** fire_controller status-resist cross-element asymmetry (controller-ruling §5); Q4-flip code-flip routing (rocket + jack-ryan gate).

---

**Signed:** gandalf, 2026-06-14
**For:** the other two generation-drift rulings — (A) retire the pre-B6 `{5,6}` skill-count invariant for the documented B6 per-archetype kit-size band, exposing the false-green that has masked a fire_mage B6-fallback defect since 2026-05-12 (routed as a separate rocket structural item with the earth_caster deferred-restoration entry as its precedent), and (B) retire the rotating-theme invariant the Q18 / 2026-06-02 season-archive pivot superseded, because the output `season_theme_element` is by the code's own declaration a naming-only flavor token, not a canonical rotating mechanical element. Three failures, one root cause: tests encoding pre-refactor entanglements that the project's dimensional/compositional refactors cleanly separated.
