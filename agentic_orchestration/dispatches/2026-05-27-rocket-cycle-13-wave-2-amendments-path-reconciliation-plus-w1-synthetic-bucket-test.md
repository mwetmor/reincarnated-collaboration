# Dispatch — 2026-05-27 — rocket — Cycle 13 Wave 2 Amendments (Path Reconciliation + W1 Synthetic-Bucket Test)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-05-27 + jack-ryan Wave 2 Gate-2 PASS verdict (commit `0783860`) flagging 2 small follow-on items: (1) elrond integration path reconciliation [INFO placeholder-by-design; KR mediates routing]; (2) W1 substrate-finding synthetic-bucket test gap [WARN; rocket follow-on]
**Estimated effort:** 30-60 min trivial amendments (2 small items in single rocket invocation)
**Acceptance:** path reconciliation landed (rocket stub points at elrond's actual priors path); W1 synthetic-bucket test added covering `_validate_separate_buckets()` False path; tests still PASS (68 + 1 new = 69); tagged commit

## Context

Jack-ryan Wave 2 Gate-2 verdict PASS (commit `0783860`) closed Wave 2 with two small follow-on items:

**Item 1 — Path reconciliation (INFO placeholder-by-design; KR mediates):**
- Elrond priors landed at `reincarnated-engine/data/synergy_priors/v1_co_occurrence_priors.json` per elrond seam canonical structure
- Rocket Pattern B stub `_load_elrond_priors()` reads from `reincarnated-engine/config/t4_synergy_priors/elrond_priors.json` per rocket MIGRATION.md + module docstring
- Jack-ryan resolution: this is placeholder-by-design (NOT coordination gap); MIGRATION.md documents two-location integration as known-open

**KR routing decision:** simplest reconciliation = rocket changes stub path to elrond's actual location (single-line change). Avoids file duplication + symlink complexity. Rocket also updates MIGRATION.md + module docstring to reflect single-path integration. Elrond's seam-canonical path preserved.

**Item 2 — W1 substrate-finding synthetic-bucket test (WARN; rocket follow-on):**
- Per jack-ryan Gate-2 W1: `_validate_separate_buckets()` returning `False` (additive-bucket penalty path) has zero test coverage
- Elrond methodology note § 6 D4 substrate finding: zero substrate-native additive-within-bucket pair instances; cannot self-validate from real data
- Jack-ryan recommendation: one synthetic test injecting TRADE_OFF+GEOMETRY_COLLAPSE with `bc_attribute="INT"` and asserting the 20.0-point additive-bucket penalty appears in `pass_2_breakdown`

## Required reading before starting

1. `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-2-rocket-implementation.md` (Gate-2 verdict; Item 1 + Item 2 specifics)
2. `reincarnated-engine/src/reincarnated/generation/t4_synergy_scan.py` (your code; `_load_elrond_priors()` location + `_validate_separate_buckets()` code path)
3. `reincarnated-engine/MIGRATION.md` (current two-location integration documentation; UPDATE)
4. `reincarnated-engine/tests/test_cycle13_wave2_t4_algorithm.py` (add new test for additive-bucket penalty path)
5. `reincarnated-engine/data/synergy_priors/v1_co_occurrence_priors.json` (elrond's actual priors location; verify path)
6. `agentic_orchestration/elrond/notes/2026-05-27-wave-2-synergy-priors-methodology.md` § 6 (D4 substrate finding source)
7. `agentic_orchestration/operating-procedures/rocket.md` (operating procedure)

## Math-before-code (trivial amendments; no new math)

NOT applicable — existing Wave 2 math note (`generation/math/cycle-13-wave-2-t4-algorithm-math-2026-05-27.md`) covers; no new math required.

## Cross-seam contract change? (Principle 6 gate)

**Round-trip: not applicable — no new cross-seam contract change.** Path reconciliation changes rocket's INTERNAL stub path to point at elrond's existing path; MIGRATION.md reflects single-path integration (cleanup of placeholder docs). Synthetic test addition is internal test coverage. Neither introduces new cross-seam fixture mutations.

## Scope

### Item 1 — Path reconciliation (~10-15 min)

- [ ] In `t4_synergy_scan.py`: change `_load_elrond_priors()` to read from `reincarnated-engine/data/synergy_priors/v1_co_occurrence_priors.json` (elrond's actual path)
- [ ] In `MIGRATION.md`: update Wave 2 cross-seam contract documentation to reflect single-path integration (remove placeholder path documentation; cite elrond's canonical path)
- [ ] In module docstring: update integration documentation
- [ ] Verify: existing 68 tests still PASS after path change (load test should now succeed via real elrond priors file)
- [ ] Note: if existing tests had Pattern B stub-mode behavior baked in, may need to adjust test to handle Pattern A real-priors-load mode

### Item 2 — W1 synthetic-bucket test (~15-30 min)

- [ ] In `tests/test_cycle13_wave2_t4_algorithm.py`: add ONE synthetic test per jack-ryan W1 recommendation:
  - Inject TRADE_OFF + GEOMETRY_COLLAPSE pair with `bc_attribute="INT"` (forced same-bucket)
  - Run through compositional synergy scan
  - Assert 20.0-point additive-bucket penalty appears in `pass_2_breakdown`
- [ ] Update test count: 68 + 1 = 69 tests; verify all PASS
- [ ] Update module-load `assert len(X) == N` if test fixtures count changes

### Discipline compose-check

- [ ] **#11 empirical inspection** — post-script empirical count assertions: 1 new test added; total = 69; verify empirically. **WARN-pattern is REMEDIATED per jack-ryan Wave 2 Gate-2 verdict (commit 0783860); maintain that closure.**
- [ ] **#1.2 code-citation** — cite affected file + line numbers in completion record
- [ ] **Principle 6 round-trip** — tests still PASS after path reconciliation

## Acceptance criteria

- [ ] `_load_elrond_priors()` path reconciled to elrond's actual location
- [ ] MIGRATION.md + module docstring updated to reflect single-path integration
- [ ] W1 synthetic-bucket test added (1 new test; total 69)
- [ ] 69/69 tests PASS empirically (run pytest; verify count)
- [ ] Post-script empirical count assertion: "69 tests PASS verified by pytest re-run returning '69 passed'"
- [ ] Tagged commit per rocket convention: `rocket: Cycle 13 Wave 2 amendments — path reconciliation + W1 synthetic-bucket test (per jack-ryan Wave 2 Gate-2 verdict 0783860)`
- [ ] Round-trip: not applicable — no new cross-seam contract change

## Out of scope (explicit non-goals)

- Re-implementing W2.0-W2.9 sub-waves (already complete per commit `2445bad`)
- Architectural changes to compositional synergy scan algorithm
- New T4 algorithm features
- Wave 3 dispatch authoring (KR separate work; gandalf design intent doc 44 forthcoming)
- Elrond seam changes (her priors path is canonical; rocket adapts)
- Modifying canonical docs (cross-seam gandalf authority)
- decisions-log entries
- Production code modifications beyond the 2 small items

## Open questions for the agent to resolve

- Path-mismatch resolution form: rocket-side path change (recommended; smaller diff) vs symlink at elrond's path (more invasive); recommend single-line stub path change in `_load_elrond_priors()`
- Test mode: existing tests may have been authored against stub-priors mode; verify Pattern A real-priors-load doesn't break test fixtures; adjust if needed
- Module-load assertion update: if test count changes from 68 → 69, update any module-load `assert len(X) == N` if necessary

## References

- `agentic_orchestration/qa/findings/2026-05-27-cycle-13-wave-2-gate-2-rocket-implementation.md` (Gate-2 verdict)
- `agentic_orchestration/elrond/notes/2026-05-27-wave-2-synergy-priors-methodology.md` § 6 (D4 substrate finding source)
- `reincarnated-engine/src/reincarnated/generation/t4_synergy_scan.py` (target file)
- `reincarnated-engine/MIGRATION.md`
- `reincarnated-engine/tests/test_cycle13_wave2_t4_algorithm.py`
- `reincarnated-engine/data/synergy_priors/v1_co_occurrence_priors.json` (elrond's actual priors)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1.2 + #11 + Principle 6)

---

**Cycle:** 13
**Wave:** 2 follow-on amendments (small)
**Gates:** clean canonical state + closed Wave 2 follow-on items
**Priority:** P2 — small amendments; non-blocking on Wave 3 dispatch authoring (gandalf doc 44 firing in parallel)
