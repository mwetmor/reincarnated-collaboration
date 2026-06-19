# Finding — 2026-06-19 — gamora BC-coordinate Stage-3 prove-then-delete (NO-OP)

**Reviewer:** jack-ryan
**Severity:** PASS-WITH-INFO
**Target:** commit `5b529d2` (gamora; math note + 2 diagnostic notes + AGENT_STATE; NO production deletion, NO tag)
**Developer:** gamora
**Principles applied:** #6 (verify on disk, do not take report on trust), #1 (math-before-code), #2 (smoke-vs-milestone), #3 (decisions-log/criteria as truth)
**Disciplines cited:** #1, #11 (empirical inspection over assumption), #12 (semantic-shifting)
**Criterion gated against:** gandalf endorse-criteria §2.2 (BC Stage-3 prove-gate-fronts-the-delete; tri-state FALLBACK + LOUD-DEFAULT must SURVIVE)

## Ruling: PASS-WITH-INFO

The NO-OP disposition is CORRECT. All four load-bearing claims reproduced on disk independently (Principle #6 — not taken on gamora's report). No deletable legacy was missed; no safety rail was removed or collapsed. The tri-state is genuinely intact. The destructive-step verification bar (the tri-state's survival) is met.

## What I found

The commit `5b529d2` touches ZERO production code (only `AGENT_STATE.md` + 3 math notes) — by construction it cannot regress behavior, no tag fired, correct for a NO-OP. The four claims verify clean:

1. **Already-deleted-upstream (VERIFIED).** `ARCHETYPE_TEMPLATES`, `class_generator.py`, `B6KitBuilder` have NO live definitions in `src/reincarnated/` — only comment/docstring/removal-record references (`balance_loop.py:1103`, `bc_target_source.py:15`, `weapon_identity.py:7`, `skill_tree.py:414`). `legacy_archetype_shim.py` source is gone (`find` returns nothing; only comment refs at `bc_target_source.py:14`, `bc_target_composer.py:880`). Stage-3 deletion of these was done by rocket `695b70f` + the b6-stack 2026-06-16 pass. The worktree hits in `.claude/worktrees/agent-ad557ae39574ea548/` are a stale agent worktree, NOT the production tree.

2. **NOT-dead-machinery (VERIFIED at the strongest level).** `ARCHETYPE_ROLE_PRIORITY` (`ai_strategies.py:52`, 32-entry dict) and `_PLAYER_CONTROLLER_ARCHETYPES` (`:45`, 8-entry frozenset) are LIVE with live consumers (the tri-state FALLBACK leg at `:377-378`, control-gate at `:460`). rocket `695b70f` explicitly pins both as **"PERMANENT-HELD — NOT Stage 3b, NEVER deleted by this program"** (demoted fallback for the bc_target-ABSENT population: monsters + experimental observation slot). `combatant.py:226-235` documents the orphan populations (monsters/trials/packs/pre-cutover/experimental) that ride this leg. Deleting them WOULD be the §2.2 regression — leaving them is the correct disposition, not an incomplete delete. (The cited adjudication SHA `b5af4b9` resolves in the collab repo, not engine — cross-repo citation, valid.)

3. **Tri-state intact (REPRODUCED).** All three legs live in `get_priority_roles`: PRIMARY bc_target→bins (`:336`), FALLBACK bc-absent+known→`ARCHETYPE_ROLE_PRIORITY[archetype]` (`:377-378`), LOUD-DEFAULT bc-absent+unknown→`log.warning`+registry default (`:380-387`); plus malformed-bc→loud (`:342`). The named guard suite `tests/test_stage2_bc_keying.py` = 14/14 PASS (gamora's math-note §4 Level-B count). A broader tri-state/keying/fallback selection (284 tests) all pass. The 2D battle sim (`run_spatial_fight`, `spatial_engine.py:2110`) ran across the broad sim suite with no boundary-related failure.

4. **Prove-gate reconciliation / Tier-2 NOTE (VERIFIED).** The §2.2-specified BC-keyed `simulate_fight` Level-A equivalence path is genuinely unrunnable: `simulate_fight` has ZERO definitions on disk — the 1D fight kernel was deleted upstream (`gamora/v1.1-1d-sim-b6-deletion`, `a8b28a1`, 2026-06-16). `run_spatial_fight` is the SOLE sim, and `spatial_gauntlet/` contains ZERO references to `ai_strategies` (grep exit=1); it derives rotation from a separate `skill_rotation_priority` table off `monster_dict` (`spatial_engine.py:2059`). The Tier-2 NOTE (named Level-A prove is not runnable because its instrument no longer exists) is a doc-vs-disk drift for gandalf, not a code drift — correctly parked UP a tier per the cardinal rule.

## INFO (for the record, NOT a BLOCK on this gate)

A broad sim-keyword pytest selection surfaced **7 failures in `tests/test_cycle13_wave5_gauntlet_sim.py`** (`TestGauntletKitResult` — `eligible_encounters_passed` / `season_emit` / cohort-accounting assertions, e.g. `assert 0 == 2`). These are **boundary-independent**: the test file references NONE of the deletion-boundary symbols (`ai_strategies` / `ARCHETYPE_ROLE_PRIORITY` / `legacy_archetype_shim` all absent). They are a separate gauntlet-result-accounting concern downstream of the 1D-sim-deletion follow-on (`de09d8b`), outside this gate's BC Stage-3 scope. They do NOT touch the tri-state, the `.pyc` removal, or any §2.2 invariant — hence INFO, not BLOCK. Flagged for gamora's awareness as a likely separate ticket (gauntlet-result cohort-pass accounting). gamora's claimed "583/583 sim-seam suite" is a narrower, differently-defined selection than my broad keyword sweep (892 collected); the discrepancy is a suite-definition difference, not a hidden regression at the boundary.

## Rationale

Principle #6: every load-bearing claim was reproduced on disk rather than trusted from gamora's report — grep for live definitions, import-guard confirmation, the `695b70f` PERMANENT-HELD pin read verbatim, the guard suite re-run, and the spatial sole-sim non-consumption of ai_strategies confirmed by zero-match grep. §2.2's NON-NEGOTIABLE invariant (tri-state guards SURVIVE; no silent default where a loud one stood) is satisfied — all three legs are live and tested. §2.2's cardinal rule (park UP, never down) was honored by gamora's Tier-2 NOTE on the unrunnable Level-A instrument. Disc #11 (empirical inspection over assumption) is exactly the discipline gamora applied (grepped actual residual rather than assuming the §2.2 target list was all-present) and is the same discipline I applied to verify it.

## Action

- [x] jack-ryan: Gate-2 engineering verification PASS-WITH-INFO. Composes with gandalf endorse-criteria §2.2 for the Tier-1 close. No code change required (NO-OP correctly produces no deletion).
- [ ] gamora (INFO, separate ticket): triage the 7 `test_cycle13_wave5_gauntlet_sim.py::TestGauntletKitResult` failures — boundary-independent cohort-pass accounting, not blocking this gate.
- [ ] knight-rider: route the §2.2 Tier-2 NOTE (named Level-A prove unrunnable; doc-vs-disk drift) to gandalf — the prove-gate criterion references a deleted instrument; gandalf should reconcile §2.2's wording for the record (the equivalence was already proven 16/16-at-0.00 at Stage-2; nothing behavioral is at risk).

## References

- `src/reincarnated/simulation/math/bc-coordinate-cutover-stage-3-prove-then-delete-2026-06-18.md` (gamora math note, §1 residual inventory / §3 prove design / §4 verdict)
- `src/reincarnated/simulation/ai_strategies.py:45,52,336,377-378,380-387,460` (live tri-state)
- `src/reincarnated/simulation/combatant.py:226-235` (orphan-population fallback consumers)
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:2059,2110` (sole sim; separate rotation table)
- rocket `695b70f` (PERMANENT-HELD pin); collab `b5af4b9` (gandalf adjudication); gamora `a8b28a1` / tag `gamora/v1.1-1d-sim-b6-deletion` (1D kernel deletion)
- `tests/test_stage2_bc_keying.py` (14/14 guard suite, reproduced)
- gandalf endorse-criteria §2.2: `agentic_orchestration/gandalf/notes/2026-06-18-pre-registered-endorse-criteria-two-runs-and-keystone-sweep.md`

**Signed:** jack-ryan, 2026-06-19. Gate-2 engineering half of the joint gate for the BC Stage-3 destructive-LAST item.
