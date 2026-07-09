# Finding — 2026-07-09 — Gate-2 rocket E2 economy-axis

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, BLOCK authority)
**Severity (overall):** INFO — **VERDICT: PASS**
**Target:** commit `d99635a` · tag `rocket/v2.0-economy-axis-2` (NOT pushed; KR batches)
**Developer:** rocket (generation seam)
**Pattern:** A (single-commit Gate-2)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate / #2-FF), 3 (cross-seam impact), 4 (decisions-log/authority-chain as truth), 5 (severity), + cross-seam round-trip
**Disciplines cited:** #1 (math-before-code), #2 / #2-FF (smoke-gate + full-fire-rider), #11 (empirical inspection), #12 (semantic-shift), ADR-004 (cross-seam)

## What I found

rocket's E2 commit gives `bc_amplitude` mechanical meaning via a single per-skill scalar `k` layered at emission onto `(damage_multiplier, cooldown_seconds, energy_cost)`, exactly per the design note §1.2/§1.3 and dispatch §2/§4. I verified every checklist item against source rather than accepting the commit-message claims. The math note lands first and derives `k_spiky=1.6`, `k_flat=0.7` under all four §2 constraints with arithmetic shown and the conservation-law proof stated (binding constraint = felt-difference ratio ≥2.0; ceilings/floors place the pair with headroom). The sacred-table-integrity claim — the load-bearing correctness check — holds: a line-level diff scan for `TIER_COEFFICIENTS / _DAMAGE_MULTIPLIER / BASE_SPELL_DAMAGE_L50 / BASE_PHYSICAL_DAMAGE_L50 / _ENERGY_COST / _COOLDOWN / _CAST_TIME` returns ZERO added/removed table lines; `k` multiplies per-skill EMITTED values after the (unchanged) table reads, and `per_hit` correctly lands on `damage_multiplier` (the sim's per-skill scalar), leaving the sacred base carriers untouched — the smoke asserts `base_spell_damage_l50` unchanged on the emitted effect. I ran the round-trip smoke: it PASSES end-to-end (exact throughput+cost-rate invariance within ε on the cooldown-defined period; variable=mixed portfolio on both INT and STR deliveries; support/T4 byte-identical + `economy_k=1.0`; felt floor 2.2857×; sacred hash unchanged; per-chain provenance read-back; sim-consumes). Both Gate-1 amendments are honored in code, not merely acknowledged.

## Verification detail (source-confirmed, not claimed)

- **Amendment A (control-duration, FLAG-DON'T-FAKE) — CONCLUSION HOLDS; no MIGRATION correctly skipped.**
  - `damage_resolver.py:1019`: `duration = float(params.get("duration_seconds", 4.0))` — the `4.0` IS an absent-param fallback, not a re-default of a present value. Sim CONSUMES emitted `duration_seconds`. Verified.
  - `per_skill_emitter.py:828`: control-role primary effect is named literally `"control"` (`role.replace("_","_")` = identity) and carries only `{element, damage_scaling_type, economy_k}` — NO `duration_seconds`. Verified.
  - `damage_resolver.py:524/531/561/564`: dispatch has branches for `heal`/`shield`/`AILMENT_NAMES`/`silence` but NO `"control"` branch → control effect is a sim no-op. Verified.
  - `per_skill_emitter.py:838-841`: signature ailment (the live lock) is gated to `chain_id == "chain_A"` primary-attack only → it rides an ATTACK chain, not control. Verified.
  - Therefore E2 v1 scopes control `k` to cooldown+cost (per-hit unscaled), leaves the chain_A signature-ailment `duration_seconds` UNSCALED (regime separation), and flags dwell-scaling as a gamora follow-on. Every field E2 scales is already consumed → **no new emitted field → MIGRATION.md correctly omitted; no HALT.** The source-reading is accurate; the cross-seam disposition is sound.
- **Amendment B (per-chain provenance) — HONORED at correct grain.** `economy_k` written into `effect_params` on each skill's primary effect (`:805` block); smoke reads it back per skill and asserts it equals the resolved `k`. Variable kit shows 1.6 on chain_A, 0.7 on chain_B/C, 1.0 on exempt — per-chain, recoverable, sim ignores the unknown param (no contract change). Verified.
- **Conservation law:** smoke asserts EXACT (`EPS=1e-9`) throughput and cost-rate on `period ≜ cooldown_seconds` (the scaled field); the fixed `cast_time` residual is reported separately as a named E4-boundary term, not a leak. `cast_time` is untouched (E4 boundary held; `_CAST_TIME` in the zero-diff scan). Reasoning sound.
- **Vocab pin:** docstring corrected `spiky/sustained/flat` → `spiky/flat/variable`; `sustained` retained as a documented backward-compat alias → flat layer; unknown amplitude → `k=1.0` fail-safe. Verified.
- **Regression:** emitter-importing suites pass (35/35 across the two cascade-amendment test files; 139 passed in the broad emit/skill selection). The 4 pre-existing collection errors + 1 related failure are all `RuntimeError: Cannot locate grouping-layer-vocabulary.md` — a missing-canonical-doc ENV issue in naming/LLM tests (`test_cosmological_vocabulary`, `test_cp8_gear_naming`, `test_naming`, `test_no_canonical_four_in_llm_prompts`, `test_d6_step4_and_coupling9`). Zero relation to `per_skill_emitter.py`; the doc genuinely does not exist in `canonical/story/`. rocket's "unrelated, predates E2" claim holds.

## Rationale

Discipline #1 satisfied (math note lands first, four constraints with arithmetic, k derived not asserted). Discipline #2 / #2-FF satisfied (round-trip smoke exists, exercises spiky/flat/variable + STR variable, prints before/after, verdict instrument named, one-command pre-fire baseline present, support/T4 byte-identity and sim-consumes ASSERTED not claimed). ADR-004 correctly evaluated: the flag-don't-fake analysis is source-accurate, so the no-MIGRATION conclusion is correct rather than a shortcut. Dispatch §10 acceptance criteria 1-8 all met. Both Gate-1 amendments implemented and covered by smoke assertions. This is clean, well-documented, correctly-scoped work.

## Non-blocking amendments (KR folds as follow-ons — NONE are gating)

- **A1 (INFO):** the control-lock-dwell amplitude-scaling fork is correctly flagged in math note §4 as a gamora follow-on, but is not yet parked in the surface-ledger or a decisions-log stub. Recommend KR file a one-line ledger/backlog note so the fork is a tracked design choice, not a rediscovery at E-series close. (Documentation-only; within my approval authority to note.)
- **A2 (INFO):** minor float artifact in emitted values (e.g. `damage_multiplier=1.2800000000000002` from `0.8×1.6`) is cosmetically visible in the smoke banner. Harmless (assertions use ε), but if certification ever does exact-string compares on emitted economy fields, a round at emission would tidy it. Not required for E2.

## Action

- [x] Developer: no blocking action. Tag stands.
- [ ] KR: fold A1 (ledger/backlog note for control-dwell fork) as a follow-on; A2 optional.
- [ ] KR: on push batch, this tag is clear. Downstream: gamora post-E2 band re-fit (conservation-law audit) — HALT-on-lurch rule stands per dispatch §12.
- [ ] Matt: no decision needed (PASS; no cross-seam change, no locked-decision conflict).

## References

- `~/Games/reincarnated-engine` commit `d99635a`, tag `rocket/v2.0-economy-axis-2`
- `src/reincarnated/generation/math/economy-axis-e2-2026-07-09.md` (math note)
- `src/reincarnated/generation/per_skill_emitter.py` (k-layer :775-790, provenance :805, resolve_economy_k, vocab pin :703)
- `scripts/rocket_economy_axis_e2_smoke_2026_07_09.py` (round-trip smoke — run, PASS)
- `src/reincarnated/simulation/damage_resolver.py:1019` (duration consume), `:339-584` (dispatch, no control branch)
- `agentic_orchestration/gandalf/notes/2026-07-09-e2-economy-axis-design-note.md` (design note, BINDS §3)
- `agentic_orchestration/dispatches/2026-07-09-rocket-economy-axis-E2.md` (dispatch, acceptance §10 BINDS; Gate-1 amendments A+B)
