# Finding — 2026-06-19 — star-lord cycle14-unified-bundle-emitters (Gate-2, engineering half)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2 engineering-correctness half of the joint gate)
**Severity:** PASS-WITH-INFO (no block)
**Target:** commit `2c252d5` / tag `star-lord/v-cycle14-unified-bundle-emitters-1`
**Developer:** star-lord
**Principles applied:** #2 (smoke-gate), #6 (cross-seam round-trip / verify-on-disk), #8 (schema validation at boundaries), #11 (empirical inspection)
**Disciplines applied:** #2, #8, #11, D7 (no-fabrication narrow-blank)
**Composition:** this is the engineering half only. Design-intent-fidelity (gandalf endorse-criteria) gated separately by knight-rider. Clean engineering gate here + design-intent pass = Tier-1 close.

## What I found

All six engineering gate criteria verified on disk, not on star-lord's report (Principle #6). (1) The diff at `2c252d5` does exactly what it claims: four emitter blocks (P2 `emit_faction_block`, P3 `emit_monster_block`, P5 `emit_weapon_descriptor`, P1 `build_unified_season_content_blocks`) in one new module; P1 is driver-agnostic and does NOT bake route-vs-replace — the architecture choice is parked Tier-3 via the `P1_ARCHITECTURE_PARK` constant and the module-bottom park notice. (2) The 60 new tests PASS on disk (`60 passed in 0.11s`). (3) Cross-seam contract honored: `MIGRATION.md §v1.80` documents the additive bundle-shape change, the drax notification, and a consumer table (gamora ZERO impact, drax sequenced cutover); the round-trip smoke is REAL — `TestRoundTripSmoke`'s 6 tests RAN (not skipped) against live `phase5_faction_clusters.json` + `phase5_faction_relationships.json` for season-001 AND season-002 (both files exist on disk), exercising the provisional gate, the repr-string parser (all 6 season-001 relationships parse clean, 0 errors), and the telemetry-absence partition on real data. (4) No regression to the export seam: `test_export`, both cycle13 export suites, the cycle12 off-hand export round-trip, and `wb_typewall_export` all PASS (220 passed across the export seam). (5) Telemetry-tier fields do not leak — `_check_no_combat_fields_in_faction_block` plus the unit + live telemetry-absence tests confirm the §3 partition holds mechanically; the §5 provisional gate fires on the all-provisional season-001 clusters. (6) No fabricated weapon identity — `emit_weapon_descriptor` returns `None` at four guard points before any descriptor is built (missing gear_rep / main_weapon / substrate_binding / weapon_type_family); `test_returns_none_when_substrate_binding_absent` PASSES; structurally cannot invent fields (D7).

## The full-suite failure (INFO — pre-existing, out-of-seam, NOT this commit)

The full export-adjacent run surfaced 33 failures, ALL in `tests/test_cycle12_layer4_convergence.py`. These are pre-existing and out-of-seam, independently confirmed (not taken on trust):
- Root cause: every one of the 33 raises `NotImplementedError: SkillTreeGenerator.generate() is retired (b6-stack deletion 2026-06-16, G10)` at `src/reincarnated/generation/skill_tree.py:422` — rocket's GENERATION seam, retired 2026-06-16.
- The commit touches ZERO generation files (`git show --stat 2c252d5` = only the 4 export-seam files).
- The layer4 test file is byte-identical between the gated commit `2c252d5` and its parent `f32e48a` (diff = empty).
- The decisions-log (lines 4335/4352, 2026-06-18 three-flip ratification) already records this same retirement at the same `skill_tree.py:422` as pre-existing + out-of-seam, worktree-confirmed at an earlier parent.

**Disambiguation vs the dispatch's flag:** the dispatch named the specific test `test_cycle12_layer4_convergence::test_dataclass_fields_exist`. I confirm the ROOT CAUSE matches (same G10 retirement, same file:line), but the failure surface is the WHOLE `test_cycle12_layer4_convergence.py` file collapsing on that single retired generator (33 fails / 10 pass), not one isolated test. This is one out-of-seam regression in rocket's seam manifesting across a whole convergence-test file, not a new fail attributable to star-lord. star-lord's "487/487 combined PASS" claim is internally consistent IF the combined scope excludes `test_cycle12_layer4_convergence.py` (the broken-upstream file); it is not a fresh regression from this commit either way.

## Rationale

- **Principle #6 (verify-on-disk + cross-seam round-trip):** every claim checked against disk; round-trip smoke confirmed to actually execute against live artifacts, not skip. MIGRATION.md present per ADR-004.
- **Principle #2 / Discipline #2 (smoke-gate):** 60/60 new + live-data smoke all green.
- **Discipline #8:** all three blocks have boundary validators that raise on shape violation.
- **Discipline #11:** the field partition was drawn against the live cycle-14 sidecar + schema annotations; the live smoke proves the partition on real data.
- **D7:** P5 cannot fabricate — None-return at every missing-input guard.
- **The 33-fail INFO is dispositioned per the decisions-log 2026-06-18 entry** (rocket seam, G10 retirement, pre-existing). It does not gate this export commit.

## Action

- [x] Developer (star-lord): no engineering action required. PASS.
- [ ] knight-rider: compose this engineering PASS with the gandalf design-intent pass for the Tier-1 close.
- [ ] knight-rider/Matt (separate, NOT a block on this commit): the 33-fail `test_cycle12_layer4_convergence.py` collapse is a standing rocket-seam cleanup (the test file references a retired `SkillTreeGenerator.generate()`). The dispatch tracked only one test name; the real surface is the whole file. Route to rocket to either retire/rewrite the convergence tests against the live `per_skill_emitter` path or xfail them, so the full suite reads clean. Tracking-only; out of scope for this gate.
- [ ] P1 top-level assembly (route-vs-replace) remains Tier-3 PARKED for Matt — correctly NOT wired here.

## References

- `src/reincarnated/export/cycle14_unified_bundle_emitters.py` (724 lines; P2/P3/P5/P1)
- `tests/test_cycle14_unified_bundle_emitters.py` (60 tests; `TestRoundTripSmoke` = 6 live-data smokes, all ran)
- `src/reincarnated/export/MIGRATION.md` §v1.80 (additive shape change + drax notification + consumer table + smoke table)
- `src/reincarnated/export/AGENT_STATE.md`
- `agentic_orchestration/gandalf/notes/2026-06-18-faction-content-shape-emission-spec.md` (the P2 contract; §3 partition / §4 shape / §5 provisional gate / §8 writer contract — all honored)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` lines 4335/4352 (pre-existing out-of-seam G10 fail disposition)
- Pre-existing fail root: `src/reincarnated/generation/skill_tree.py:422` (rocket seam, G10 retirement 2026-06-16)
