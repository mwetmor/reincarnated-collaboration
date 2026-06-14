# Stage-3 BC-cutover — consolidated design adjudication (the pinned deletion set + 2 corrections reconciled)

**Type:** consolidated design adjudication (gandalf seam). Reconciles the two empirical corrections to my §2 carve priors; pins the exact irreversible-deletion set; reframes Stage 3b. The final list KR hands Matt.
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-ruled NARROW Stage 3 (Pattern-B 2026-06-14); my scope ruling `agentic_orchestration/gandalf/notes/2026-06-14-stage-3-bc-cutover-scoping-ruling.md` (§2 carve / §3 prereqs); this note resolves the two corrections that ruling's priors required.
**Prereq sources (all COMPLETE, all read this session):**
- rocket generation-side audit `~/Games/reincarnated-engine/src/reincarnated/generation/notes/2026-06-14-stage-3-generation-reference-audit.md` (engine commit 5a4005c).
- gamora sim-side audit + zero-label proof `agentic_orchestration/gamora/notes/2026-06-14-bc-stage3-simulation-reference-audit.md` (engine commit 8ab02c0).
- drax demo-VFX sweep `agentic_orchestration/drax/notes/2026-06-14-demo-vfx-archetype-tag-coupling-sweep.md` (GATE CLEARS).
- Proof artifact `~/Games/reincarnated-engine/output/bc-stage3-zero-label-proof-20260614_214135.json` (ELEMENTAL_LEAK=0, PHYSICAL_LEAK=0, PASS=true).

---

## 0. TL;DR — the three rulings

1. **R-1 shim verdict: DELETE in narrow Stage 3.** My HELD prior was a pre-Stage-1 code-state artifact. I traced it myself: the shim has zero live `src/` importers (the two grep "hits" are an acceptance-guard docstring and a backward-compat comment), touches NEITHER live path, and its only out-of-`src/` consumer is the W0.2.5 smoke test OF the shim itself — which dies with it. It is dead on both paths and joins the cut.
2. **The reframe: `ARCHETYPE_ROLE_PRIORITY` + `_PLAYER_CONTROLLER_ARCHETYPES` are PERMANENT-HELD, not "→ Stage 3b".** gamora's correction is decisive: these tables are reached only by the bc_target-ABSENT population (monsters + experimental), which is permanent and unaffected by physical-pool expansion. They never reach Stage-3b-deletability. **Stage 3b is consequently re-scoped to a generation-seam-only event, and it frees almost nothing at the sim seam.**
3. **The pinned narrow-Stage-3 deletion set = exactly two symbols:** `{ G1 ARCHETYPES_FORBIDDEN_CLOSE_RANGE, G9 legacy_archetype_shim }` (plus the dead `tests/test_w02_bc_target_composer.py` shim-import block that dies with G9). Validated against the green proof: zero elemental leak, zero physical leak. **The go/no-go to Matt is UNCHANGED — still GO, now with a 2-symbol pinned set instead of 1.**

---

## 1. R-1 — the shim verdict (DELETE, with my own trace)

rocket overrode my prior on evidence and flagged it rather than reclassifying unilaterally. Correct discipline. I traced it myself before ruling (the request invited verification; the cut is irreversible).

**What my §2 prior said:** "`legacy_archetype_shim` — physical kits use the shim bridge → HELD."

**What the source actually shows (my trace, this session):**

- **Zero live importers in `src/`.** `grep -rn "legacy_archetype_shim" src/ --include="*.py"` returns 5 hits; ALL are prose, not imports:
  - `bc_target_source.py:14-15` — an **acceptance-guard docstring** that asserts the module imports NOTHING from the shim ("grep of classify_archetype, ARCHETYPE_TAG_TO_BC_TARGET, bc_target_for_archetype ... in this module returns EMPTY"). This is the *inverse* of a consumer — it is a guard certifying non-consumption.
  - `b6_archetype_templates.py:15` + `:326`, `archetype_composer.py:15`, `bc_target_composer.py:880` — backward-compat comments / a comment naming the W0.2.5 smoke test. No `import`.
- **Symbol-level grep** for the four exported names (`bc_target_for_archetype`, `compose_for_archetype_tag`, `ARCHETYPE_TAG_TO_BC_TARGET`, `ARCHETYPE_TAG_TO_ROLE`) across `src/` returns only the same `bc_target_source.py:15` docstring line. No call site.
- **The physical fork does not touch it.** Confirmed against rocket's G4→G7→G8 trace: physical routes `classify_archetype → ARCHETYPE_TEMPLATES → B6KitBuilder.build`. The shim's direction is `archetype-tag → BC` — the W0.2.4 (2026-05-21) label→BC bridge, the **INVERSE** of the cutover. Nothing on either live path runs it.
- **Out-of-`src/` consumer = the W0.2.5 smoke test, which is a test OF the shim, not a downstream dependant.** `tests/test_w02_bc_target_composer.py` (header: "W0.2 Phase 2 smoke tests — BC-target composer + legacy archetype shim ... Verify shim path produces kits for all 24 archetype tags," author rocket, 2026-05-21) imports all four shim symbols and exercises them across ~15 methods. This is a test of the bridge being deleted — it does not keep the bridge alive; it dies with it. (The `.claude/worktrees/...` copy is a git-worktree mirror, not a second consumer.)

**Why my prior was wrong:** it predates Stage 1. At W0.2.4 the shim WAS the bridge; my §2 carve was written before tracing the post-Stage-1 fork, and I carried the W0.2.4-era mental model forward. rocket's source trace caught the staleness. This is exactly the failure the prove-then-delete gate exists to catch — a HELD prior that no longer matches code-state.

**Verdict: DELETE `legacy_archetype_shim` (the whole module: `ARCHETYPE_TAG_TO_BC_TARGET`, `ARCHETYPE_TAG_TO_ROLE`, `bc_target_for_archetype`, `role_for_archetype`, `compose_for_archetype_tag`, `archetype_tag_from_label`, `ArchetypeTagNotFound`) in narrow Stage 3 — NOT deferred to 3b.** It touches neither live path; it is the inverse-direction bridge the cutover obsoletes. Holding it would be holding a corpse — precisely the "stagnant vestigial logic that becomes ingrained" Matt named on 2026-05-27 as worse than scope-creep.

**Deletion co-requisite:** the shim-import block + the shim-exercising test methods in `tests/test_w02_bc_target_composer.py` (lines 37-45 import block; the `bc_target_for_archetype` / `compose_for_archetype_tag` test methods, ~lines 409-527) must be removed in the SAME commit — they will hard-fail collection otherwise. The composer-side imports (lines 24-36, `bc_target_composer`) STAY; only the shim block goes. This is test-deletion-with-the-tested-corpse, not coverage loss: the behavior the methods assert (label→BC bridging) is the behavior being deleted. rocket executes; jack-ryan Gate-2 confirms the test file still collects + passes post-edit.

## 2. The reframe — ARCHETYPE_ROLE_PRIORITY + _PLAYER_CONTROLLER_ARCHETYPES are PERMANENT-HELD

My scope ruling §2 framed both as "HELD → Stage 3b," with Stage 3b's re-open criterion = "physical-pool expansion landing." gamora's empirical correction dissolves that framing.

**The correction (gamora §3, Disc #12):** physical kits carry a `bc_target` (computed unconditionally at `class_generator.py:433`, stamped `:553`) even though their CONTENT routes to the legacy b6 builder. At the SIMULATION instrument they therefore pilot via BINS (the tri-state PRIMARY path) and **never reach the label fallback.** The proof confirms it: 1 live physical kit (`rogue`, bc_target present) → PHYSICAL_LEAK = 0.

**Consequence — who actually reaches these tables:** the bc_target-ABSENT population only:
- **Monsters** (`from_monster`, `ai_strategy="scripted"`, no bc_target) — a **permanent** population.
- **The experimental observation slot** (`bc_target is None`) — also permanent (experimental IS production per `season_orchestrator.py:1550`).

Neither is touched by physical-pool expansion. Physical-pool expansion moves physical *player kits* onto the coordinate — but physical player kits already carry bc_target and already bypass these tables. **So physical-pool expansion frees NOTHING at the simulation seam.** The premise of my §2 "→ Stage 3b" framing for these two symbols was simply false.

**RULING: `ARCHETYPE_ROLE_PRIORITY` + `_PLAYER_CONTROLLER_ARCHETYPES` are PERMANENT-HELD.** They are the Stage-2 demoted fallback for the bc_target-absent population (monsters + experimental). That population is permanent. These tables are load-bearing infrastructure, not vestige. They have no deletion horizon under the current architecture and should be recorded as PERMANENT-HELD with justification "demoted fallback for the bc_target-absent population (monsters + experimental), NOT the physical kit path." The earliest they could EVER become deletable is a hypothetical future where monsters + experimental kits also carry bc_targets — which is not on any roadmap and is not Stage 3b.

## 3. Stage 3b — redefined

My scope ruling defined Stage 3b as "delete the physical fallback (at minimum `ARCHETYPE_ROLE_PRIORITY` + `legacy_archetype_shim` + physical templates), re-open criterion = physical-pool expansion landing." Both named symbols have now moved OUT of that set (shim → Stage 3 DELETE; ROLE_PRIORITY → PERMANENT-HELD). Stage 3b must be redefined or it is a hollow placeholder.

**Redefined Stage 3b (generation-seam-only; sim seam frees nothing):**

- **Scope:** the GENERATION-side physical fork in rocket's seam — `class_generator.py:636-714` (the `if is_physical:` block) and the legacy machinery it alone keeps alive: G4 `classify_archetype` (physical-fork caller at `:637`), G5 `archetype_composer` (transitive via G4), G7 `b6_archetype_templates.ARCHETYPE_TEMPLATES` (the kit-template dict, physical-fork lookups), G8 `B6KitBuilder`.
- **Re-open criterion (unchanged in spirit, sharpened): physical-pool expansion that moves physical PLAYER kit CONTENT onto the coordinate** — i.e., physical kits compose via `compose_kit` + `adapt_composed_kit_to_skills` instead of routing to `b6_builder.build`. When that lands, the `if is_physical:` fork becomes inert for player kits and the G4/G5/G7/G8 generation-side chain can be cut.
- **Honest scope note: Stage 3b frees ONLY generation-side physical-fork machinery. It frees NOTHING at the simulation seam** (the sim label tables are PERMANENT-HELD per §2). Anyone expecting Stage 3b to clean up the sim-seam label tables is mistaken — there is no such cleanup, because monsters + experimental keep those tables permanently live. Stage 3b is a smaller, generation-only event than my original framing implied.

**CRITICAL cross-seam gate on G7 (rocket R-2):** `b6_archetype_templates.ARCHETYPE_TEMPLATES` is HOLD-PHYS **AND** HOLD-SIM — consumed by `simulation/balance_loop.py:1886/1948/2030/2183` for element-redistribution/role-swap during balancing (applies to elemental + physical kits, graceful None-skip). **G7 must NOT be deleted on a generation-only Stage 3b clearance.** Even after physical-pool expansion frees the generation-side physical consumers, the balance-loop consumers are an independent HOLD. Stage 3b's G7 deletion is gated on BOTH the generation physical fork going inert AND the balance-loop consumers being re-pointed off the table. Recorded here so the eventual Stage-3b executor sequences correctly and does not trust a generation-only green light.

## 4. The pinned narrow-Stage-3 deletion set (the list KR hands Matt)

Against the green proof (ELEMENTAL_LEAK=0, PHYSICAL_LEAK=0, PASS=true) and both reference-audits:

| # | Symbol | File | Verdict | Why safe to cut now |
|---|---|---|---|---|
| **G1** | `ARCHETYPES_FORBIDDEN_CLOSE_RANGE` | `b6_archetype_templates.py` | **DELETE** | V-8 re-pointed in Stage 1 to `forbids_close_range(element, role)` at `season_orchestrator.py:149`; the import at `:40` is dead (`noqa: F401`). `forbids_close_range` fires elemental-branch-only (physical returns at `:138-143` before reaching it). No live consumer besides the dead import + docstrings. |
| **G9** | `legacy_archetype_shim` (whole module) | `legacy_archetype_shim.py` | **DELETE** (R-1 ruling) | Zero live `src/` importers; touches neither live path; inverse-direction W0.2.4 bridge the cutover obsoletes. Out-of-`src/` consumer is the test OF the shim, which dies with it. |
| — | shim-import block + shim test methods | `tests/test_w02_bc_target_composer.py` | **DELETE (co-requisite of G9)** | Tests the deleted bridge; must go in the same commit or collection hard-fails. Composer-side imports (lines 24-36) STAY. |

**Sim seam contributes ZERO deletable symbols** (gamora: elemental-only-deletion-set EMPTY; every sim label symbol is HELD — PERMANENT-HELD per §2). The entire narrow Stage-3 target lives in rocket's generation seam, and it is two symbols.

**Everything else is HELD** — split into two NON-equivalent buckets that the record must keep distinct:
- **PERMANENT-HELD (no deletion horizon):** sim `ARCHETYPE_ROLE_PRIORITY`, sim `_PLAYER_CONTROLLER_ARCHETYPES`, `CombatantState.archetype` field, `_PREFERRED_BEHAVIOR_ROLES`, `_REGISTRY_DEFAULT_PRIORITY`/`_ROLE_REGISTRY`, and the HOLD-UNCOORD generation symbols (G3 `_geo_map`, G6 `allocate_stats`/stat `ARCHETYPE_TEMPLATES`, G11 action_register/role_function) — all reached by the permanent monster/experimental/uncoordinated population.
- **HOLD → Stage 3b (generation-only, physical-pool-expansion-gated):** G4 `classify_archetype`, G5 `archetype_composer`, G7 `ARCHETYPE_TEMPLATES` kit-dict (ALSO gated on balance-loop re-point per R-2), G8 `B6KitBuilder`. (G10 `skill_tree._ARCHETYPE_TEMPLATES` HELD with R-3 elemental-reachability trace open — low risk, shape dict not behavior-input; not in either Stage-3 OR a clean Stage-3b until R-3 closes.)

## 5. Captured-for-record (rocket R-2, R-4)

- **R-2 (G7 cross-seam):** `b6_archetype_templates.ARCHETYPE_TEMPLATES` is HOLD-PHYS **and** HOLD-SIM (balance_loop.py 4 sites). Do NOT delete on generation-only clearance. Folded into §3 Stage-3b gate above.
- **R-4 (hygiene, NOT a deletion item):** stale `noqa: F401` comments at `class_generator.py:21` ("KitConstraintError now dead on live path" — FALSE; caught in physical fork at `:664`/`:701`) and `:22` (`ARCHETYPE_TEMPLATES` "no live consumer post-cutover" — FALSE; physical fork at `:642`/`:657`/`:688`). These anticipate the FULL cut, not the narrow one, and now mislead. They are comment-only, do not change any classification (both symbols HELD-PHYS), and are out of the no-modify constraint this audit honored. **Recommend rocket correct these comments in the Stage-3 deletion commit** (they are in the same file the deletion touches) so a future deleter does not trust the comment over the fork. Cosmetic; not gating.
- **drax cosmetic re-points (from the demo sweep, NOT gating):** two UI text labels (`classSelector.ts:131`, `characterSheet.ts:170`) read `archetype_tag` and will render `undefined` after the engine eventually drops the field. The Stage-3 cut here does NOT drop the emitted `archetype_tag` field (that is the END-of-pipe composed field, distinct from the start-of-pipe machinery being deleted) — so these are not even triggered by this cut. Recorded for the eventual field-drop, not for Stage 3.

## 6. Go/no-go to Matt — UNCHANGED: GO

The prove-then-delete gate is empirically GREEN and nothing in the two corrections changes the verdict:

- **Elemental path proven inert** (16/16 Stage-2 PASS; proof ELEMENTAL_LEAK=0). The irreversibility payoff is earned on the elemental path → make it structural.
- **drax gate CLEARS** — no Pixi VFX coupling breaks; the §7-flagged Layer-2 overlays key on `PlayerClass.name` + `dominant_element` (safe); the one null-guarded label read already misses on live data.
- **The two corrections SHRINK risk, not raise it.** R-1 adds one provably-dead symbol to the cut (removing vestige, the goal). The reframe REMOVES two symbols from any deletion horizon (recognizing them as permanent infrastructure) — which means Stage 3 is touching LESS load-bearing machinery than my original framing feared, not more.
- **The pinned set is 2 symbols** (G1 + G9), both traced to zero live consumers, both validated against a zero-leak full-season proof.

**KR hands Matt: GO on the narrow Stage-3 irreversible cut. Pinned deletion set = { G1 ARCHETYPES_FORBIDDEN_CLOSE_RANGE, G9 legacy_archetype_shim } + the co-requisite shim test block.** rocket executes the deletion; jack-ryan Gate-2 confirms (a) the engine generates a full season behavior-identical to the green proof, (b) `tests/test_w02_bc_target_composer.py` still collects + passes post-edit, (c) the R-4 comment corrections landed. Stage 3b is parked as a generation-seam-only, physical-pool-expansion-gated event that frees nothing at the sim seam.

---

**Signed:** gandalf, 2026-06-14
**For:** the Stage-3 consolidated adjudication — R-1 shim ruled DELETE-in-narrow-Stage-3 (pre-Stage-1 prior staleness, self-traced to zero live consumers); ARCHETYPE_ROLE_PRIORITY + _PLAYER_CONTROLLER_ARCHETYPES reframed PERMANENT-HELD (monster+experimental fallback, not physical, not Stage-3b-deletable); Stage 3b redefined as generation-seam-only / physical-pool-expansion-gated / frees-nothing-at-sim; pinned narrow deletion set = {G1, G9} + co-requisite shim test block; go/no-go to Matt UNCHANGED = GO against the green zero-leak proof.
