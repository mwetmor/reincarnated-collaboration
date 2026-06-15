# Finding — 2026-06-15 — gate2-gamora-lever-c-result

**Reviewer:** jack-ryan
**Severity:** INFO (verdict: PASS — C-2 is sound and legitimately reached)
**Target:** tag `gamora/v1.x-lever-c-disambiguation` (commits 072e743 amended-note, 79cb145 harness, 01da930 result+state)
**Developer:** gamora
**Principles applied:** Review-Process #1 (math-before-code), #2 (smoke-gate), #5 (severity matters); Disciplines #1, #4, #8, #11; Gate-1 amendments A1/A2/A3 (finding 8d3bb0e)

## What I found
The Lever C disambiguation result reaches **C-2 (KIT-COMPOSITION)** soundly and legitimately. All six Gate-2 verification points pass. The amended math-note (072e743) folds Gate-1 A1/A2/A3 correctly: §1 + §3 re-pivot the architecture discriminator from M=1.0 to M=0.30 and demote M=1.0 to a reported sanity datapoint; the A3 inversion guard is in both §3 and the harness `_verdict`. The harness (79cb145) runs BOTH M=0.30 and M=1.0 via a DIRECT `loop._evaluate_class(env_pc, upper_gauntlet, 60, modifier=M)` call (balance_loop.py:2865) with NO `balance_class()` / binary-search wrapper, so M is genuinely held fixed by fiat — confirmed by reading the call site. Swarm is genuinely excluded: the gauntlet is filtered to upper-four tiers (`GAUNTLET_TIER_TO_R1_KEY != "swarm"`), so the `_is_swarm` spatial branch (:2899) never fires; the result JSON `upper_tiers_only` is `[boss, elite, magic, mini_boss]` with `swarm_set_aside: true`. The kit under test carries `{defensive:1, mobility:2, area_damage:4, burst_damage:1, primary_attack:2}` on genuine glass/close-fast/single-target coords lifted verbatim from the refire harness, with the role-floor PRECONDITION asserted as `floor_fired: true` — apples-to-apples vs d003f8f.

I independently re-ran the boss + mini_boss batches at M=0.30 to rule out a "fight-never-ran" artifact. **The zero is genuinely real and fully diagnosed.** The boss batch (monster_00012, b_max_hp 123,356) terminated `a_dead` on all 60 fights, with the rogue dealing mean 192.5 damage (max 363.7) over 17.8–29.4s — the boss ends every fight at 100.0% HP. The mini_boss batch (70,255 HP) is the same story: 60/60 `a_dead`, best fight leaves the boss at 92.1% HP. Meanwhile the magic tier clears at 0.9167 (M=0.30) / 1.0 (M=1.0), which proves the engine, kit, damage-resolver, and modifier-application path are all live — the kit kills magic, it simply cannot scratch the upper three tiers. This is a genuine kit-composition wall, not a dead harness.

## Rationale
- **A1 folded + M held fixed (Disc #1).** Discriminator reads M=0.30 in both note §3 and `_verdict` (boss_clears_030 gate); M=1.0 is reported only. `_evaluate_class` called directly — no convergence search. PASS.
- **A2 reconstruction correct (Disc #8, schema-at-boundary).** `termination_reason` is in-memory on `FightResult` (fight_result.py:41) and `BatchResult.results` is `list[FightResult]` (fight_result.py:116) — both verified. `b_dead` is the correct kill string: `_build_result` (search_estimator.py:1101) sets `b_dead` when `state_b` (the opponent/boss) is not alive, and combatant_a is the player (`from_player_class`, balance_loop.py:2990). `_kills_only_rate` computes `kills / n` with n=`batch.n_fights`=60 — correct denominator. No MIGRATION-HALT correctly NOT triggered. PASS.
- **The zero is real, not an artifact (Disc #11, empirical inspection).** Independent re-run confirms n=60 per tier, fights executed (non-zero a_damage_dealt, real durations), and the kit simply loses every fight by a wide HP margin. The magic-tier clear is the live-engine control. PASS.
- **Kit is the floored envelope rogue (Disc #4, right comparison).** role_histogram + floor_fired + verbatim refire construction confirm apples-to-apples. PASS.
- **Scope clean (ADR-002, Disc #1).** Diffs touch only the new probe script, the output JSON, and AGENT_STATE.md (+4/-1). No balance-loop architecture change, no per-tier-modifier build, no composer change, no b6 deletion, no schema growth. Telemetry.db read SELECT-only (`mode=ro`). PASS.

The C-2 prong fired correctly per the pre-registered rule: boss craters `<0.05` at BOTH M=1.0 AND M=0.30. The A3 inversion guard is moot (boss does not clear, so no boss-clears-but-elite-craters inversion) and gamora surfaced that honestly. The broad upper-tier collapse (elite + mini_boss also 0.0) is reported transparently rather than buried.

## Action
- [x] Developer: none required — result stands as authored.
- [ ] Matt: C-2 GATES your next decision. The probe shows NO balance-architecture change is warranted; the floored glass-ST rogue genuinely lacks boss tools (genre-correct fragility). Decision: accept-as-known-limitation vs. revisit the kit-composition envelope. This is a design call, not a process gate — Gate-2 clears the run as sound.

## References
- `/Users/admin/Games/reincarnated-engine/scripts/lever_c_upper_tier_disambiguation_2026_06_15.py`
- `/Users/admin/Games/reincarnated-engine/output/lever-c-upper-tier-disambiguation-20260615.json`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/lever-c-upper-tier-throughput-disambiguation-2026-06-15.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/fight_result.py` (:41 termination_reason, :116 BatchResult.results)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/search_estimator.py` (:1101 b_dead semantics)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/balance_loop.py` (:2865 _evaluate_class, :2899 swarm branch, :2990 modifier application)
- Gate-1 finding: `agentic_orchestration/qa/findings/2026-06-15-gate1-gamora-lever-c-disambiguation.md` (8d3bb0e)
