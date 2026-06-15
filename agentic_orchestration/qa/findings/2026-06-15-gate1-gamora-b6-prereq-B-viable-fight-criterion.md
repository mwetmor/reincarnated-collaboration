# Finding — 2026-06-15 — Gate-1 — gamora b6-deletion Prerequisite B "viable fight" sim-validation CRITERION

**Reviewer:** jack-ryan
**Mode:** DESIGN-MODE (Gate-1, pre-run — the MANDATORY criterion gate)
**Severity:** N/A (Gate-1 verdict: CLEAR-WITH-AMENDMENTS)
**Target:** math-note `src/reincarnated/simulation/math/b6-deletion-prereq-B-g7-hold-sim-viable-fight-criterion-2026-06-15.md`, commit `11e1608`, tag `gamora/v1.x-b6-deletion-prereq-B-g7-hold-sim-criterion` (engine repo)
**Developer:** gamora
**Principles applied:** 1 (math-before-code), 3 (cross-seam impact), 4 (decisions-log as truth), 5 (severity / honest-fail integrity)
**Disciplines cited:** #1, #11, #12

## Verdict

**CLEAR-WITH-AMENDMENTS.** The conjunctive 5-prong criterion is decisive and force-pass-proof at source — every code anchor verified, P4's anti-timeout guard is real, the cross-seam boundary claim is correct at source. ONE methodology amendment is required before the run: an absolute per-tier floor must sit UNDERNEATH the b6-baseline-parity comparator. The parity bar alone is defensible against an absolute-100% bar (gamora's force-FAIL argument is correct) but leaves one real force-PASS surface — parity to a co-weak baseline. The floor closes it. Two minor citation-drift fixes folded in below (non-blocking).

## What I found

I verified all five prong anchors against `balance_loop.py` at source, not from the note. **P2** converged: `abs(target_winrate - convergence_wr) <= TOLERANCE * 2` (:1212), `TOLERANCE=0.03` (:60) — accurate. **P3** convergence gate: `_evaluate_convergence_gate` (:3249) iterates ALL 5 tiers in `TIER_EVALUATION_ORDER` with no early-exit, `passed = floor_wr <= observed <= ceiling_wr`, bands at :532-545 (swarm .65/.80, magic .55/.70, elite .45/.60, mini_boss .20/.50, boss .30/.45) — accurate. **P4** kills-only: confirmed at `_compute_kills_only_tier_rates` (:3180-3247) — an all-timeout boss tier produces `termination_reason != "b_dead"` for every fight → `boss_kills=0` → `boss_kill_rate=0.0`, and `0.0 < floor 0.30` → P3 `below_floor` → gate FAIL. The "viable-looking-but-degenerate all-timeout" failure mode IS caught. P4 is therefore strictly redundant with P3 as gamora candidly states (§2 note), but the explicit per-tier WR vector pinning is sound audit hygiene, NOT a force-pass surface — keep it. **P5** doppelganger: `_evaluate_doppelganger` (:2674) runs L17/L33/L50, `balanced = lo <= win_rate <= hi`, range (0.20, 0.80) at :77 — accurate.

The cross-seam boundary claim is correct at source. The composer (`weapon_envelope_composer.py`) uses the EXACT b6 mechanism `grammar.generate(forced_geometry=...)` + `composer.compose()` and stamps `damage_scaling_type="physical"` / `scaling_attribute` / `canonical_element` onto the shared `Skill`. Every sim-consumed field gamora enumerates exists on the `Skill` Pydantic model (`skill_schema.py`): `range_m` (:27), `spatial_geometry_type` (:37), `role` (:39), `canonical_element` (:40), `scaling_attribute` (:44), `tier` (:51), `damage_scaling_type` (:75). No new field; no MIGRATION warranted. All four `ARCHETYPE_TEMPLATES` consumers degrade gracefully and stay untouched: :1886 `return []` on `template is None`; :2030 and :2183 `return False, current_wr, {"rationale": "no_template"}`; :1948 reads the template only for element-distribution counting (read-defensive). The run-precondition boundary assert (§4) is a real live check — required-field presence asserted before fights execute, missing/None → HONEST-FAIL routed to rocket+KR, not silently defaulted. Sound.

The §5 run plan is right-sized per Principle-6 / Discipline #2.1: smoke subset (~5-6 kits + matched b6 counterparts) before fuller population, sequential same-seed (Discipline #3), ~30 min bound, no full-regen. Correct — this is a sim-validation gate, not a milestone-validation gate.

**The one gap — crux 2.** gamora's argument that an absolute 100%-pass bar would be STRICTER than the b6 net it removes is CORRECT and well-reasoned: b6 shields degraded kits today, so demanding the replacement clear an absolute bar the current system does not is the inverse force-FAIL error. The same-run measurement (both arms, same gauntlet, same seeds) is apples-to-apples and sound. The pre-registered one-kit one-sided `-1` tolerance is genuinely locked HERE (§5.3) and cannot be loosened post-hoc — that is good discipline. BUT the parity comparator alone has a force-PASS surface that this exact gate exists to prevent: **parity is RELATIVE to the b6 baseline, so on any gauntlet cell where b6 kits are ALSO weak (e.g. both arms fail the boss tier on the same monster), `envelope_pass_count >= b6_pass_count - 1` passes envelope kits that are broadly degenerate on that cell** — because the baseline is co-weak there. Parity-to-a-co-weak-baseline licenses deleting the net precisely where the net is least active, but is silent on cells where envelope kits are degenerate AND b6 was the thing carrying them. That is a quiet defang of a destructive-deletion gate.

## Rationale

Principle 5 (severity / honest-fail integrity) + the founding logic of this gate: B licenses a DESTRUCTIVE deletion, so the criterion must be force-pass-proof in BOTH directions. gamora has correctly armored the absolute-bar / force-FAIL direction; the force-PASS direction needs the floor. Discipline #12 (no semantic-shift) is satisfied — the floor I require is NOT a new band, it is the SAME locked `TIER_FLOORS`/`TIER_CEILINGS` (:532-545) and kills-only `> 0.0` semantic already in P3/P4, simply asserted as an ABSOLUTE precondition that the parity test cannot waive. Principle 1 (math-before-code) is satisfied: this is the pre-run criterion gate, the note precedes the run.

## Action

- [ ] **gamora (AMENDMENT 1 — required before run):** Bolt an absolute per-tier floor UNDER the parity comparator. The §3 PASS condition becomes conjunctive: PASS iff `(envelope_pass_count >= b6_baseline_pass_count - 1)` AND `(no envelope kit exhibits a STRUCTURAL degenerate-tier pattern in absolute terms — i.e. a tier whose envelope-arm observed WR is below its locked `TIER_FLOOR`, or boss/mini_boss kills-only `== 0.0`, on a cell where the b6 arm is NOT also failing that same tier on that same cell)`. Plainly: parity may license parity-with-a-weak-net, but it may NOT license an envelope-only degeneracy that b6 was masking. Pre-register this floor in §3 + §5.3 alongside the existing `-1` tolerance so it is equally locked. This is the only blocking amendment.
- [ ] **gamora (AMENDMENT 2 — non-blocking, fold at convenience):** Correct two citation drifts so the note is audit-clean. (a) §4 cites `ARCHETYPE_TEMPLATES` consumers at `:1884/1946/2025/2176`; the fourth is the import-block start at `:2177` with the template lookup at `:2183` (note says 2176/return-sites are approximate) — pin the lookup lines `:1886/1948/2030/2183` and the degrade returns `:1888/:2031` to actuals. (b) §0/§4 composer field-stamp line cites `345/346/354/356`; actuals are STEP-4 stamp ~:351 and STEP-5 element overlay ~:360-363. Structurally accurate, just off by a few lines.
- [ ] **Matt:** No decision needed. CLEAR-WITH-AMENDMENTS is within my Gate-1 authority (criterion is a method construct, not an architectural change; ADR-002). Relayed for clearance only.

## References

- `src/reincarnated/simulation/math/b6-deletion-prereq-B-g7-hold-sim-viable-fight-criterion-2026-06-15.md` (note under review)
- `src/reincarnated/simulation/balance_loop.py` — :60, :77, :503, :532-545, :686, :934, :1212, :1884/:1886, :1946/:1948, :2025/:2030, :2177/:2183, :2674, :3180-3247, :3249-3320 (verified at source)
- `src/reincarnated/generation/weapon_envelope_composer.py` — :290-363 (compose path + field stamps, verified)
- `src/reincarnated/generation/skill_schema.py` — :6-164 (shared Skill model; all sim-consumed fields verified present)
- `output/weapon-as-identity-phase2-gate-20260615.json` — 64 floor-proven envelope kits (the population to sim-validate)
- `agentic_orchestration/dispatches/2026-06-15-gamora-b6-deletion-prereq-B-g7-hold-sim.md` (parent dispatch)
- `agentic_orchestration/qa/findings/2026-06-15-gate1-gamora-b6-prereq-B-g7-hold-sim.md` (prior Gate-1 on the dispatch)
