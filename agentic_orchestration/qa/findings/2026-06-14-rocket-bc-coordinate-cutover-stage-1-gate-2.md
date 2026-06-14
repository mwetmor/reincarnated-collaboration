# Finding — 2026-06-14 — rocket-bc-coordinate-cutover-stage-1 (DEV-MODE Gate-2, implementation gate)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-AMENDMENTS (elemental cut) — INFO/WARN amendments below; the PHYSICAL fork is gandalf/Matt-ESCALATED (not jack-ryan-BLOCK; rocket escalated correctly)
**Target:** tag `rocket/v1.0-bc-coordinate-cutover-stage-1` @ `19b27f3` (amendment fold `c610ae6`; NOT pushed)
**Developer:** rocket
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam MIGRATION), 4 (decisions-log/contract truth), 6 (cross-seam round-trip)
**Disciplines cited:** #1, #2, #39
**ADRs:** ADR-002 (tiered approval), ADR-004 (cross-seam handoff)

## Verdict (one line)

The ELEMENTAL cut (16/21 coordinates) is **PASS-WITH-AMENDMENTS** and may proceed toward Stage 2 once gandalf's design half also clears. The three structural-removal assertions independently verify PASS. The physical fork is correctly STOP-AND-ESCALATED to gandalf/Matt (not my lane to rule, and not a jack-ryan BLOCK — it is the discipline working as designed). One test-delta routed to me is a real-but-bounded contract supersession (rewrite), two are clean supersessions (rewrite), one is the physical-escalation symptom (defer with the fork). One mis-attributed "pre-existing" failure needs re-labeling (WARN).

---

## What I found

I independently verified at source (not by trusting rocket's report) the three A-3 structural-removal assertions, the one-variable cleanliness of the elemental cut, the cross-seam round-trip, the A3-OPEN MIGRATION record, and the four (not three) `test_role_orientation` failures. The elemental cut is architecturally sound: the live non-experimental path composes from `bc_target` via `compose_kit` + the new adapter, the b6-template-lookup pipe and its degraded-5-skill fallback are structurally unreachable, and water_mage now composes a full kit. The R-b cost_type restamp and the Ruling-2 premise-correction (stats keyed off the kit's own resolved `scaling_attribute`, not a re-introduced element lookup) are behavior-preserving and do not smuggle a second variable. The physical fork genuinely cannot compose behavior-preservingly (pool is structurally sparse: max-reachable kit_size 2–5 vs legacy 10–13) and is loud-fail escalated, exactly per the dispatch's R1/R3 discipline.

---

## A-3 INDEPENDENT VERIFICATION (the architectural acceptance proof)

| Assertion | rocket reports | jack-ryan independently verified | Result |
|---|---|---|---|
| **A-3.1** no `b6_builder.build` on live path | PASS | Live path (`class_generator.py:430-445`, non-experimental, non-weird) routes through `_compose_class_from_coordinate` → `compose_kit` + `adapt_composed_kit_to_skills`. No `.build()` call reachable. `_generate_skills` DELETED (`:716-728` is the gravestone comment). **Nuance:** `B6KitBuilder` is still *imported* (`:21`) and *instantiated* (`self._b6_builder`, `:372`) — but never `.build()`-called on the live path; resident-but-unreachable per the Stage-3-deletion plan. The assertion is about the CALL, and the call is gone. | **PASS** |
| **A-3.2** no `archetype_tag in ARCHETYPE_TEMPLATES` gate on live path | PASS | `ARCHETYPE_TEMPLATES` imported (`:22`) but grep shows zero membership-gate on the live path; the V-7 gate + b6 branch + `KitConstraintError` fallback are structurally deleted. The symbol stays resident (Stage-3). | **PASS** |
| **A-3.3** water_mage composes kit_size ≥ 10 | 12–13 | I ran the live path: `damage/water` → kit_size **10** (mid-slow default range) and **10** across the round-trip fixture; rocket's "12–13" reflects a different range/seed family but is also ≥ floor. Every observed water kit ≥ 10. The 1/29 is DISSOLVED (the constraint concept no longer exists in `compose_kit`), not patched. | **PASS** |

All three independently confirmed. The `KitConstraintError → 5-skill fallback` is structurally removed (cannot fire). This is the architectural acceptance.

**Bonus verifications I ran:** V-8 `forbids_close_range` re-point is behavior-preserving (fire/water damage → True; physical/earth/control → False, matching the legacy `{fire_mage, water_mage}` set, label-free). Smoke suite reproduced: `pytest tests/test_class_generation.py tests/test_d3_archetype_composer.py` → **94 passed, 3 skipped** (matches rocket exactly). Determinism + round-trip below.

---

## ONE-VARIABLE DISCIPLINE (elemental cut behavior-preserving?)

**Yes for the elemental cut, with one documented tolerance.** The ONLY variable that changes is the composition mechanism (template-lookup → coordinate-composition). I specifically stress-tested the two places a second variable could hide:

1. **R-b cost_type restamp** (`composed_kit_adapter.py:565-590`): restamps `cost_type` + re-derives `power_tier` only when the orchestrator energy differs from the composer's resolved cost_type, AND guards the SET-CHANGING case with `DegradedKitError` (kit below `KIT_SIZE_FLOOR` → loud-fail re-draw, never a silent degraded kit). The "shapes are cost-type-agnostic" premise is carried in-comment and is the right premise. No second variable smuggled.
2. **Ruling-2 premise-correction** (`composed_kit_adapter.py:248-311` + `class_generator.py:452-454`): rocket surfaced that gandalf's Ruling-2 assertion ("stats are substrate-blind for elemental archetypes") is empirically incorrect — legacy stat distributions ARE element-shaped via `ELEMENT_SCALING_ATTRIBUTE`, and `damage_resolver` scales by `skill.scaling_attribute`, so stats must align to the kit's scaling_attribute or damage silently undercounts. The resolution takes the primary attribute from `skills[0].scaling_attribute` — **the kit's own resolved attribute, NOT a re-introduced element lookup.** This is the simulator-consistency the system already required; it is behavior-preserving by construction and does not re-couple element into the source map. I concur with rocket's finding and its in-seam classification (it changes stat KEYING, not the mechanic SET/SHAPE/kit_size, so it is not a Ruling-3 hard-stop). **Confirmed: no second variable.**

The documented tolerance (gandalf Ruling 3, GRANTED): tier/chain TREE topology is coordinate-derived-valid, not b6-template-identical. Mechanics are 1:1. A3 (OPEN) is the behavior-preservation backstop for this tolerance.

---

## THE 4 test_role_orientation DELTAS — jack-ryan RULES (my contract authority)

rocket routed **3**; the suite actually fails **4**. rocket's MIGRATION named 3 (kit-band, support, physical). The 4th (`test_control_class_has_no_burst_damage`) is unlisted and I surface it explicitly. My ruling per test:

### Delta 1 — `test_fire_mage_kit_size_in_b6_band` → **REWRITE to the coordinate-composition contract**
- **Symptom:** asserts `lengths <= {10,11,12}`; coordinate composition yields `{10,11,12,13,14}`.
- **Ruling:** SUPERSEDED, not a regression. The `{10,11,12}` band was the b6 per-template `_KIT_SIZES["burst_damage"]` artifact. Under the cut, kit_size is `len(compose_kit(...).selected_mechanics)` — a coordinate property, not a template constant. All observed sizes (10–14) are ≥ the behavior floor (10) and the upper drift is the composer's natural mechanic-pool spread, not a fallback.
- **Exact rewrite:** assert `lengths <= {10,11,12,13,14}` AND `min(lengths) >= 10` (the `KIT_SIZE_FLOOR` — this is the load-bearing assertion: it makes any future degraded-kit fallback visible, preserving the original test's INTENT) AND keep `len(lengths) >= 2` (spirit-preserving variation). Rename the test `test_fire_mage_kit_size_above_floor` and update the docstring to cite the coordinate-composition contract + `KIT_SIZE_FLOOR`.

### Delta 2 — `test_support_template_produces_sustain_skills` → **REWRITE to the coordinate-composition contract**
- **Symptom:** asserts `sustain_count >= 2`; coordinate composition yields 0.
- **Ruling:** SUPERSEDED, not a regression. The legacy `ROLE_SKILL_TEMPLATES["support"]` hard-injected ≥2 sustain skills; `compose_kit` derives skills from the support coordinate's mechanic pool, which does not template-inject sustain. Per the math note (§5.5) per-skill role is mechanic-derived, not template-shaped. Support is also excluded from `VALID_SOLO_ROLE_ORIENTATIONS` (the test's own docstring concedes "it just isn't called in solo seasons"), so this asserts a non-live template path.
- **Exact rewrite:** the assertion now belongs to the coordinate contract: a support coordinate composes a control/mixed-shaped kit. Replace with an assertion on what the support coordinate DOES produce (e.g. `kit_size >= KIT_SIZE_FLOOR` and `ctrl_bin`/`def_bin` reflect the support coordinate via `cls.bc_target`), OR — cleaner — mark `@pytest.mark.skip(reason="support role-template superseded by coordinate composition; support is non-solo (VALID_SOLO_ROLE_ORIENTATIONS) — re-home as a Phase-5 multi-actor contract test")`. I lean **skip-with-reason** because support is not a live solo path; do not invent a coordinate assertion for a path the orchestrator never fires. Either is acceptable; state which in the rewrite commit.

### Delta 3 — `test_physical_class_always_damage_orientation` → **DEFER WITH THE PHYSICAL FORK (do not rewrite yet)**
- **Symptom:** `class_gen.generate("fire","physical",...)` raises `PhysicalPoolInfeasibleError`.
- **Ruling:** This is NOT a test-contract delta the cut legitimately supersedes — it is the **direct symptom of the escalated physical fork.** Rewriting it now would bake in whichever resolution gandalf/Matt has not yet chosen (expand-pool vs accept-smaller-band). It is also NOT a jack-ryan BLOCK: rocket loud-failed and escalated exactly as the R1/R3 discipline requires. **Action:** leave this test failing/erroring, tracked against the physical-fork escalation; rewrite it as part of whichever physical resolution lands. Do not let it gate the elemental cut.

### Delta 4 (UNLISTED by rocket) — `test_control_class_has_no_burst_damage` → **REWRITE to control-DOMINANCE (real-but-bounded supersession)**
- **Symptom:** asserts `not any(s.role == "burst_damage")`; the earth/control coordinate (after a `DeferredEvaluation` re-draw) yields kit_size 11 with **7 control + 1 area + 3 burst**, correctly tagged `earth_controller`.
- **Ruling:** SUPERSEDED, but I looked hard at whether it is a regression because "burst on a controller" could indicate the AI mis-pilots. It does NOT: `TestControllerAIFix::test_common_ai_fires_control_for_earth_controller` PASSES in the same suite (the controller fires control skills in a traced fight), and control density is dominant (7/11). The legacy template's ABSOLUTE "zero burst on control" was a template-purity invariant; under coordinate composition the control-pure coordinate naturally samples a few high-power-tier non-CC mechanics that `_mechanic_skill_role` (`composed_kit_adapter.py:168-170`) labels burst. The control IDENTITY (dominance + AI behavior) is preserved; the purity is not. **This is a legitimate contract supersession, NOT a regression — but it is the one delta closest to the line, so it must be rewritten to assert IDENTITY not PURITY.**
- **Exact rewrite:** replace the absolute exclusion with a dominance assertion: `control_count = sum(s.role == "control" for s in cls.skills); assert control_count >= 2` (already covered by the sibling test) PLUS `assert control_count > sum(s.role == "burst_damage" for s in cls.skills)` (control strictly dominates burst) AND `assert cls.archetype_tag == "earth_controller"`. Update the docstring to cite the coordinate-composition contract + that control identity is now dominance-based, not template-purity-based. **rocket: this delta was NOT named in your MIGRATION test-delta list — add it.**

---

## A3 CALIBRATION — OPEN confirmed (A-4 amendment honored)

`MIGRATION.md` (`generation/MIGRATION.md:64-68`) records the A3 ≤20%/1-bin gate as **OPEN, NOT PASS**, registered as a **Discipline-#39-tracked** open item with the follow-up reference (KR-routed gamora Phase-3/4 sim on the 24-default-coordinate fixture). Auditable at wave-close, not silently skipped. This is exactly my A-4 amendment from the math-note gate. **Confirmed PASS on the A-4 obligation.**

## CROSS-SEAM ROUND-TRIP (Principle 6) — adequate

I ran the round-trip independently (5/5, matches rocket): `bc_target` non-null on every elemental class, `archetype_tag` legacy-format bridge + `archetype_label` coordinate-string both populated, `from_player_class` consumes without KeyError. A4 column shipped (star-lord `0d3de46`), recorder wired. MIGRATION declares the additive-nullable `bc_target` field, the OUTPUT-only `archetype_tag` re-purpose, and the decoupling buffer. **Principle 6 satisfied.**

---

## AMENDMENTS (non-blocking; address before Stage-2 close)

**WARN-1 — the "pre-existing" failure is MIS-ATTRIBUTED.** star-lord flagged `test_b11_geometry_palette.py::TestB11GeometrySmoke::test_smoke_still_emits_original_geometries` as PRE-EXISTING ("projectile geometry missing"). At source, this test now **ERRORS at fixture setup** because `smoke_geometries` generates two PHYSICAL classes (`tests/test_b11_geometry_palette.py:506,508`) which raise `PhysicalPoolInfeasibleError` under Stage-1. That is the PHYSICAL-FORK symptom, NOT an unrelated pre-existing projectile-geometry gap — the test cannot even reach its geometry assertions now. Whether projectile geometry was independently missing pre-cutover is moot and untestable in this state. **Action:** re-label this in the wave record as "blocked by the physical-fork escalation," not "pre-existing." It does not contaminate the elemental Gate-2 verdict, but the attribution must be corrected so the physical resolution knows to re-home it.

**INFO-1 — double canonical-pairing.** `pair_with_canonical` runs on every skill in BOTH the adapter (`composed_kit_adapter.py:613`) and `class_generator.generate` (`:463`). Idempotent (same ref), so not a correctness bug — redundant compute only. Remove one (prefer keeping the `class_generator` site for consistency with the experimental/weird paths). Non-blocking.

**INFO-2 — bridge-label suffix nuance.** A medium-range wind/damage coordinate synthesizes `wind_mage` where legacy was `wind_caster` (suffix derivation yields "caster" only at geo_bin=large-AOE / long range). The simulator resolves both keys (round-trip passed, no KeyError), so OUTPUT-only and non-blocking — but note for the Stage-2 simulator re-key that the bridge suffix is not 1:1 with the legacy label at non-long ranges. INFO only.

**INFO-3 — geometry_derivation WARN spew.** The adapter surfaces ~30 `derive_spatial_geometry_type: unknown geometry_type='burst'/'projectile'/'void_pool'/...` warnings per run (the mechanic pool carries geometry vocab `_RICH_TO_SPATIAL` doesn't cover). Behavior falls back to role-based derivation (non-fatal), but this is new log noise the cut introduced. Track for a follow-up `_RICH_TO_SPATIAL` extension; non-blocking for Stage 1.

---

## Discipline implication of shipping a 16/21 PARTIAL cut (analytical flag only — NOT the physical-pool design ruling, which is gandalf's lane)

Shipping the elemental 16/21 while the physical 5/21 is escalated is a **clean one-variable state, not a discipline problem** — PROVIDED the partition is along a principled axis, which it is: elemental-vs-physical is exactly the `compose_kit`-feasible-vs-pool-sparse boundary, surfaced by loud-fail, named in MIGRATION, and the physical path raises rather than silently degrading. The cut does not leave a half-migrated path that silently produces wrong kits; physical coordinates STOP. The one discipline caveat: the live orchestrator must not emit a physical coordinate into the live season path until the fork is ruled, or generation will raise mid-season. **Flag to gandalf/KR:** confirm the season orchestrator does not select physical/martial energy on the live elemental-only Stage-1 path (or that the raise is caught at season level), else Stage-1 elemental shipping needs a physical-coordinate guard at the orchestrator before any live regen. This is the one operational item the elemental "proceed" depends on. I do NOT rule the pool-expansion-vs-smaller-band question — that is gandalf's physical-pool design fork.

---

## Action

- [ ] Developer (rocket): rewrite Delta 1 (`test_fire_mage_kit_size_above_floor`, assert `min >= KIT_SIZE_FLOOR`), Delta 2 (skip-with-reason or coordinate assertion), Delta 4 (`test_control_class_has_no_burst_damage` → control-dominance assertion) per the exact specs above. ADD Delta 4 to the MIGRATION test-delta list. Leave Delta 3 deferred with the physical fork.
- [ ] Developer (rocket): remove the duplicate `pair_with_canonical` call (INFO-1).
- [ ] knight-rider / star-lord: re-label the `test_b11_geometry_palette` smoke failure as physical-fork-blocked, not pre-existing (WARN-1).
- [ ] gandalf / Matt (ESCALATED — already routed by rocket): rule the PHYSICAL pool fork (expand pool vs accept smaller band). Out of jack-ryan scope.
- [ ] gandalf / KR (operational): confirm the live orchestrator does not emit a physical coordinate on the Stage-1 elemental path before live regen, OR add a physical-coordinate guard.
- [ ] Follow-up (KR-routed gamora): run the A3 ≤20%/1-bin sim on the 24-default-coordinate fixture to close the Discipline-#39 open item.

## May the elemental cut merge / proceed toward Stage 2?

**YES — conditional on:** (a) the 3 test rewrites (Deltas 1/2/4) landing, and (b) gandalf's design half (§7) also clearing. The architectural acceptance (A-3.1/3.2/3.3) is proven, one-variable is clean, round-trip passes, A3 is auditably OPEN. The physical fork proceeds on its own escalated track and does not block elemental Stage 2. Test-rewrites and INFO/WARN amendments are within my ADR-002 direct-approval authority (test additions/refactors, docs); the physical fork is Matt/gandalf. Milestone tagging (dropping the seam prefix) remains Matt's per ADR-002.

## References

- `src/reincarnated/generation/class_generator.py` (`:430-445` live path, `:452-454` scaling_attr, `:591-668` `_compose_class_from_coordinate`, `:716-728` removal gravestone)
- `src/reincarnated/generation/composed_kit_adapter.py` (`:168-170` burst role-derive, `:248-311` allocate_stats_from_coordinate, `:565-590` R-b restamp, `:613` double-pair)
- `src/reincarnated/generation/bc_target_source.py` (`:89-102` V-8 gate; zero-label source)
- `src/reincarnated/generation/MIGRATION.md` (`:8-86` Stage-1 entry; `:64-68` A3 OPEN)
- `src/reincarnated/generation/math/bc-coordinate-cutover-stage-1-adapter-source-substrate-2026-06-14.md`
- `tests/test_role_orientation.py` (`:515-517`, `:529-533`, `:557-585` the 4 deltas)
- `tests/test_b11_geometry_palette.py` (`:505-524` smoke fixture, physical-fork symptom)
- gandalf §7 ruling + §7-review ruling `ee4f785`; tag `rocket/v1.0-bc-coordinate-cutover-stage-1` @ `19b27f3`
