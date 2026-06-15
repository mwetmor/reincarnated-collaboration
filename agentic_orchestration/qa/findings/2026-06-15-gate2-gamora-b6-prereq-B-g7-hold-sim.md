# Finding — 2026-06-15 — Gate-2 — gamora b6-deletion Prerequisite B G7 HOLD-SIM (HONEST-FAIL)

**Reviewer:** jack-ryan
**Mode:** DEV-MODE (Gate-2, UNCONDITIONAL — B licenses a destructive deletion)
**Severity:** INFO (verdict CONFIRMED; no BLOCK — the FAIL is genuine and correctly held)
**Verdict:** **CONFIRM-HONEST-FAIL.** Prerequisite B correctly HOLDS Decision 2; b6 STAYS.
**Target:** result commit `a7411f3`, tag `gamora/v1.3-b6-deletion-prereq-B-g7-hold-sim-1`; durability commit `03c338e`
**Developer:** gamora
**Principles applied:** 1 (math-before-code), 3 (cross-seam impact), 4 (decisions-log as truth), 5 (severity / honest-fail integrity), 6 (smoke-gate)
**Disciplines cited:** #1, #2.1, #3, #11, #12

## Verdict

**CONFIRM-HONEST-FAIL.** I re-ran the harness from source. The HONEST-FAIL is **genuine and decisive**, NOT a force-FAIL artifact of the harsh smoke slice. The both-pass tally is correctly held OPEN: Prerequisite A PASSED Gate-2, B is HONEST-FAIL, so Decision 2 does NOT fire and the legacy b6 `ARCHETYPE_TEMPLATES` net STAYS. Amendment 1 (the absolute per-tier floor I required at Gate-1) did exactly its job — it caught the envelope-only degeneracy that the relative parity test would have force-passed. No BLOCK; the gate behaved as designed.

## What I found

I re-ran `scripts/g7_hold_sim_b6_prereq_B_2026_06_15.py` myself (505s, foreground). Both my re-run and gamora's committed `a7411f3` return VERDICT=HONEST_FAIL with the identical disposition (3a parity PASS, 3b absolute-floor FAIL, 3c no-envelope-P1 PASS, boundary CLEAN, b6 0/5, env 0/5). The decisive CELL 4 (rogue) structural pattern is **invariant across both runs**: b6 arm converges (final_modifier 0.61, P2=True) and carries the upper tiers well above their locked floors (run1 elite/mini_boss/boss kills-only 0.75/0.667/0.967, magic 1.0; my re-run 0.683/0.9/0.9, magic 1.0), while the envelope arm fails to converge (pinned at MODIFIER_SEARCH_FLOOR 0.0101, 10 iters) and collapses to **exactly 0.0 on elite/mini_boss/boss in BOTH runs**, magic 0.5 in both. That collapse-where-b6-carries is precisely the parity-to-a-co-weak-baseline force-PASS surface Amendment 1 exists to close (my Gate-1 finding §23), and it fired.

**Crux 1 — genuine, not slice artifact.** The envelope collapse is a real structural degeneracy, not floor-pinning noise. Mechanism, verified at source (`TIER_FLOORS`/`MODIFIER_SEARCH_FLOOR` at `balance_loop.py:532-545`/`:318`): the envelope rogue kit over-performs on swarm (WR 1.0), driving the single GLOBAL modifier to its search floor 0.01 to suppress that over-performance — but the same global suppression simultaneously craters the upper tiers to 0.0 because the kit has no per-tier shape the one lever can resolve. b6, on the same gauntlet/same seeds, lands a modifier (0.61) where swarm-through-boss sit in a workable spread and converges. That is the difference between a sim-viable kit and a floor-test artifact — exactly what this gate was built to discriminate. The harsh slice (single-seed-per-cell, 30 fights, max_iter=10) makes BOTH arms fail the FULL 5-prong KIT_PASS (0/5 each), but 3b does NOT rest on the both-zero aggregate pass-counts; it rests on the per-cell tier-by-tier comparison, which is robust to the slice. gamora's framing is correct.

**Crux 2 — Amendment 1 wired exactly as specified.** Harness `:368-377` implements my Gate-1 predicate verbatim: `env_below = env_wr < TIER_FLOORS[tier]; b6_ok = b6_wr >= TIER_FLOORS[tier]; if env_below and b6_ok: <flag>`. The aggregate verdict `:417` is genuinely conjunctive (`parity_ok AND absolute_floor_ok AND not any_env_p1_break AND boundary_ok AND n>0`). 3b is the SAME locked `TIER_FLOORS` + kills-only `>0.0`, no new band, no Discipline-#12 semantic shift — the defang-closure I required.

**Crux 3 — b6 build-fail robustness fix is sound + harness-only.** The `physical_skirmisher` b6 arm exhausting MAX_KIT_RETRIES (`KitConstraintError: require_mobile_attack`) is captured as baseline telemetry and the gate continues (`:282-289`, `:326-342`). Verified harness-only (Discipline #12): no criterion/math/semantic change — a non-building b6 arm yields no per-tier WRs, so `b6_ok=False` for every tier, so NO tier flags as envelope-only-degenerate there (confirmed: CELL 2 contributes 0 subfloor tiers). That is the correct conservative semantic in BOTH directions — a b6 that can't build neither makes the envelope look worse (can't flag a degeneracy) nor better (can't be the carrying baseline). Scoping 3c to the envelope arm (`:411-414`) is correct: the gate judges whether the REPLACEMENT is sim-safe; a b6-arm failure is baseline telemetry, not an envelope-gate failer. Force-pass-proof preserved.

## Two non-blocking observations (INFO — for the record, not blocking the verdict)

1. **Run is not bit-for-bit deterministic despite seeding.** My re-run produced the SAME verdict and the SAME invariant CELL-4 structure, but per-tier WRs and convergence-iteration counts moved between runs (e.g. CELL-4 b6 mini_boss 0.667→0.9; CELL-0 warrior swarm crossed the band edge and added a marginal 5th subfloor tier in my run). The `BalanceLoop` fight engine carries internal RNG state not fully pinned by `seed_base`. This does NOT weaken the FAIL — it strengthens it (the violation only broadened: 4→5 tiers on my run, never retracted CELL-4). But the harness should not be cited as deterministic; it is verdict-stable, not value-stable. Noting for any future re-use of this harness as a regression baseline.
2. **CELL-0 (warrior) swarm subfloor is band-edge marginal** (env 0.6444 vs floor 0.65) and run-dependent; CELL-4 (rogue) is the robust, non-marginal, decisive violation. The design conclusion should rest on rogue + upper tiers, not on the warrior edge case.

## Rationale

Principle 5 (honest-fail integrity) + the founding logic that B licenses a destructive deletion: the criterion had to be force-pass-proof in both directions, and the inverse-error guard (don't force-FAIL on a harsh slice) is the heart of this Gate-2. I confirmed at source that the FAIL is structural, not slice-induced: b6 converges and carries the tiers the envelope arm zeroes, across two independent runs. Discipline #12 satisfied — the robustness fix shifts no semantics. Discipline #2.1 / Principle 6 — the smoke slice is sufficient to HOLD Decision 2 (see methodological judgment below); it is NOT sufficient to PASS a destructive deletion, but PASS is not the outcome here.

## Methodological judgment — is the smoke slice sufficient to hold Decision 2?

**Yes, for HOLDING.** A smoke-slice HONEST-FAIL is sufficient to hold Decision 2 because a fuller run can only ADD failing cells/tiers, never retract a structural envelope-only collapse where b6 demonstrably converges and carries (confirmed empirically — my re-run broadened the violation). Holding the net in place is the conservative, reversible direction; it requires no further confirmation. A fuller-power run (more seeds, higher power, more fights) would be REQUIRED only to *clear* B (force-pass-proofing a destructive deletion demands it) — and B did not clear. So: no fuller run is needed before the design loops back. If/when rocket reshapes the envelope path and a re-attempt is staged, THAT re-attempt should run at fuller power before any PASS is drawn.

## Action

- [x] **jack-ryan:** CONFIRM-HONEST-FAIL. Verdict verified at source via independent re-run. Both-pass tally correctly held open; Decision 2 does NOT fire.
- [ ] **gamora:** No re-run required to hold. (a) Drop any "deterministic" framing of this harness — it is verdict-stable, not value-stable (obs 1). (b) If B is re-attempted post-reshape, run at fuller power/more seeds before drawing a PASS.
- [ ] **gandalf + Matt (design implication — ESCALATE):** The weapon-as-ENVELOPE physical path is NOT yet sim-safe to remove the b6 net. Concrete locus: **CELL 4 / rogue**, where the envelope kit over-performs on swarm (WR 1.0), pins the global modifier to its search floor, and collapses elite/mini_boss/boss to 0.0 (kills-only) — the single global-modifier lever cannot resolve a kit with no per-tier shape, whereas b6 converges and carries those tiers. The envelope path needs per-tier shape (the global modifier alone is insufficient) before B can be re-attempted. Decision 2 stays HELD; b6 `ARCHETYPE_TEMPLATES` stays in place.

## References

- `output/g7-hold-sim-b6-prereq-B-20260615.json` (result; I re-ran and reproduced the verdict + invariant CELL-4 structure)
- `scripts/g7_hold_sim_b6_prereq_B_2026_06_15.py` — `:368-377` (3b predicate, matches Gate-1 spec), `:411-414` (3c env-scoped), `:282-342` (b6 build-fail conservative handling), `:417` (conjunctive verdict)
- `src/reincarnated/simulation/math/b6-deletion-prereq-B-g7-hold-sim-viable-fight-criterion-2026-06-15.md` — §3/§5.3-b (Amendment 1 folded), §6 (Discipline-#12 check)
- `src/reincarnated/simulation/balance_loop.py` — `:318-319` (MODIFIER_SEARCH_FLOOR/CEILING), `:532-545` (TIER_FLOORS/CEILINGS, verified match), `:61` (MAX_ITERATIONS)
- `agentic_orchestration/qa/findings/2026-06-15-gate1-gamora-b6-prereq-B-viable-fight-criterion.md` (my Gate-1, Amendment 1 spec)
- commits `a7411f3` (result), `03c338e` (durability), tag `gamora/v1.3-b6-deletion-prereq-B-g7-hold-sim-1`
