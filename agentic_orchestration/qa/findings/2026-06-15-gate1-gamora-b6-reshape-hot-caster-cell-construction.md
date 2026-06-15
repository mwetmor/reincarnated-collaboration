# Finding — 2026-06-15 — gate1-gamora-b6-reshape-hot-caster-cell-construction

**Reviewer:** jack-ryan
**Severity:** CLEAR-WITH-AMENDMENTS (one WARN, two INFO — none gating; run may fire after the WARN is recorded in the harness output)
**Target:** commit `664cdae` — `src/reincarnated/simulation/math/b6-reshape-hot-caster-cell-construction-2026-06-15.md`
**Developer:** gamora
**Mode:** DESIGN-MODE Gate-1 (mandatory construction gate — no run fires until verdict)
**Principles applied:** Review #1 (math-before-code), #2 (smoke-gate), #4 (decisions-log/locked-signature as truth), #5 (severity); Disciplines #11 (empirical-not-convenient), #12 (no semantic shift), #2.1 (smoke-subset-first)

## Verdict: CLEAR-WITH-AMENDMENTS

The construction manufactures the test PRECONDITION (hot swarm) without manufacturing the test OUTCOME (upper-tier clear/crater). I verified the orthogonality claim against the engine — it holds by code structure, not by assertion. The lever is sound, the branch definitions are byte-for-byte symmetric with the locked signature, and the anti-rig floor is a genuine honesty mechanism. One WARN (record the effective-multiplier composition before the run) and two INFO. None gates the run.

## What I found (against the engine, per your five questions)

**Q1 — Is the lever provably orthogonal to the upper-tier outcome? YES, by path structure, not by assert.**
The gauntlet loop classifies each monster by `threat_tier` and forks PER MONSTER (`balance_loop.py:2879-2916`): `_is_swarm` monsters route through `_run_spatial_slot()` → `run_spatial_fight()` (the spatial path, the only path the `hp_multipliers` knob exists on); the branch ends in `continue` (`:2914`). ALL other tiers (magic/elite/mini_boss/boss) fall to the 1D path and build a fresh `combatant_b = from_monster(monster)` (`:2917`) run through `run_batch`/`run_batch_geared` (`:2963`) — a code path on which `hp_multipliers` is not a parameter and cannot be reached. The comments at `:2859-2860` and `:2875-2876` state this contract verbatim. The upper-tier Monster objects are independent (`from_monster(monster)` per opponent) at their own HP factors; a swarm-slot per-mob multiplier provably cannot touch them. gamora's §1/§2.2 path-separation claim is CORRECT as written.

**The pre-flight tier-isolation assert (§5) is sufficient AS A BACKSTOP, but it is not the primary guarantee — the path fork is.** The assert (elite/mini_boss/boss `max_hp`+`armor` identical with/without `SWARM_HP_MULT`) will catch a leak if I am wrong about the path. Given the fork is per-monster with a hard `continue`, the assert is belt-and-suspenders, which is the right posture for a load-bearing construction. Keep it.

**Q2 — Second-order coupling (the subtle rig vector)? NONE found across the three channels I checked.**
- *Seed channel:* swarm base_seed is `hash(class.id + monster.id + "spatial_swarm")` (`:2798`); upper-tier seeds are `hash(class.id + opponent_id)` (`:2873`). The lever changes mob HP, not any monster `id`, so no seed on any path shifts. No seed coupling.
- *Shared-state channel:* `_run_spatial_slot` re-derives `class_dict = player_class.model_dump()` (`:2783`) and rebuilds entity instances per fight (`:2787-2788`); the 1D branch builds `from_player_class(...)` fresh per fight (`:2952`). No cooldowns/resources/HP carry across tiers — each tier is an independent batch with fresh combatant construction. The only cross-tier coupling is the single global `modifier`, which the lever does not touch. This is exactly the surgical separation branch-4-vs-2 needs.
- *Timeout-budget channel:* each tier has its own `_tier_max_duration` (`:2924-2929`); the swarm spatial timeout is independent. Lowering swarm HP cannot consume an upper-tier budget. No coupling.
There is no second-order channel by which raising swarm WR biases convergence or upper-tier clear. The rig vector you flagged is closed by construction.

**Q3 — Branch definitions byte-for-byte symmetric with the locked signature? YES.**
I cross-checked §4 of the construction note against the signature note's locked values: `MODIFIER_FLOOR_NEAR = 0.015` (signature §3.2, `balance_loop.py:318`); `TIER_FLOORS` elite 0.45 / mini_boss 0.20 / boss 0.30 (signature line 36, `:532-538`); kills-only `:690`; `converged` `:1212`; `M_SWEEP = {0.01, 0.0316, 0.1, 0.316, 1.0, 3.16}` and `CASTER_SHAPE_EXISTS` (signature §3.2 / lines 116-120) all reused verbatim. The construction note's branch 4 = signature branch 4, branch 2 = signature branch 2 (with `CASTER_SHAPE_EXISTS==True`), branch 3 = signature branch 3 (`CASTER_SHAPE_EXISTS==False`, globally-broken, distinct). No new semantic introduced (Discipline #12). The only new object is the swarm-slot HP-multiplier construction input — an analysis-side gauntlet input, not an engine-behavior change. Confirmed.

**Q4 — Anti-rig floor + STILL-INCONCLUSIVE a genuine honesty mechanism? YES — and stricter than the note claims (see WARN).**
The ladder STOPS on first 1b-hit, the floor at `SWARM_HP_MULT=0.15` is hard (no lower), and the stop rule reports STILL-INCONCLUSIVE rather than forcing a hit by reaching for a global/kit lever. That is a real honesty mechanism — it pre-commits to admitting untestability. The ladder cannot be walked past the floor to force a convenient hit. The only nuance is the effective-multiplier accounting, below.

**Q5 — Anything that lets the run fail to discriminate branch 4 from branch 2? NO.**
Branch 2 (the falsifier) is stated sharply and gated on `CASTER_SHAPE_EXISTS==True`, so a globally-broken caster lands in branch 3, not a false-architectural branch 2. Branch 4 requires `converged==True` AND all three upper tiers ≥ floors. The two are mutually exclusive on a 1b-hot cell and both reachable on the un-rigged upper-tier path. The run discriminates.

## Amendments

### WARN-1 (record before the run; does not gate) — the lever composes MULTIPLICATIVELY with an existing 1.5× swarm-HP factor; the §3.2 floor rationale is stated against the wrong quantity.
The engine applies `effective_hp_mult = caller_hp_mult * MOB_HP_DIFFICULTY_MULTIPLIER` (`spatial_engine.py:1850`), gated on `mob_tier in MOB_HP_DIFFICULTY_TIERS = {swarm, magic, elite}` and `scenario in {open_arena, chokepoint_corridor}` (`arena.py:49,52,55`). The convergence swarm slot uses `SCENARIO_OPEN_ARENA`, swarm tier — so `MOB_HP_DIFFICULTY_MULTIPLIER = 1.5` (`arena.py:49`) DOES apply. Therefore the REALIZED swarm-mob HP is `SWARM_HP_MULT × 1.5`, not `SWARM_HP_MULT`:
- Rung 1 (0.50) → effective 0.75× base swarm HP
- Rung 2 (0.30) → effective 0.45×
- Rung 3 (0.15) → effective 0.225×

This does NOT break the construction — the composition is still a clean scalar on the swarm slot only, still tier-local, still kit-untouched. It actually makes the anti-rig floor STRICTER than the note claims: §3.2's "below ~0.15× HP the swarm degenerates into near-instant clear" is the degeneracy guard, but the floored cell is realized at effective ~0.225×, comfortably above a trivial regime — so the floor is more conservative than stated, which strengthens the honesty mechanism. The amendment is reporting hygiene (Discipline #11 — record what the cell actually does): the run output MUST label the realized swarm difficulty as `SWARM_HP_MULT × MOB_HP_DIFFICULTY_MULTIPLIER` so a reader does not mistake "0.15× HP" for the realized condition. Record the effective product in the per-rung telemetry vector. No math change to the lever or the floor; record-only.

### INFO-1 — math-note paths reference `spatial_engine.py:1747` etc.; actual file is `spatial_gauntlet/spatial_engine.py`.
The note cites `spatial_engine.py:1747, 1761, 1796-1797` (the `hp_multipliers` param). The live file is `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` and the param sits at `:1747` there (the `run_spatial_fight` signature) — line numbers match, directory prefix in the note is abbreviated. Non-gating; tighten the path in any follow-on note for traceability.

### INFO-2 — the pre-flight tier-isolation assert is a backstop, not the guarantee; frame it that way in the run record.
Per Q1, the per-monster path fork (`:2879-2916`) is the actual guarantee of orthogonality; the §5 assert is belt-and-suspenders. Keep the assert (correct posture for a load-bearing construction) but in the run record state the guarantee is structural (the fork + `continue`), with the assert as the empirical confirmation. This keeps the legitimacy argument resting on the right foundation if a future refactor ever touches the fork.

## Action
- [ ] gamora: record the effective `SWARM_HP_MULT × MOB_HP_DIFFICULTY_MULTIPLIER (=1.5)` product in the per-rung swarm-difficulty telemetry (WARN-1, record-only — no math change). Then PHASE 2 may fire foreground-blocking per §5 (smoke-subset-first, tier-isolation pre-flight asserted, ladder sequential, STOP-on-hot).
- [ ] gamora (optional): tighten the `spatial_gauntlet/` path prefix (INFO-1) and frame the assert as backstop-to-the-fork (INFO-2) in the run record.
- [ ] Matt: none required — this is within DESIGN-MODE Gate-1 clearance authority (no decisions-log conflict, no cross-seam schema change, no new ADR; the lever is a read-side analysis input with confirmed zero schema delta per §5). The run does not need Matt sign-off to fire.

## References
- `reincarnated-engine/src/reincarnated/simulation/math/b6-reshape-hot-caster-cell-construction-2026-06-15.md` (commit `664cdae`) — construction note under review
- `reincarnated-engine/src/reincarnated/simulation/math/b6-reshape-scoping-per-tier-shape-degeneracy-signature-2026-06-15.md` — locked signature (branch defs, M_SWEEP, CASTER_SHAPE_EXISTS, MODIFIER_FLOOR_NEAR, TIER_FLOORS)
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py:2742-2842` (`_run_spatial_slot` — swarm-only, fresh `model_dump`, swarm-salted seed), `:2855-2974` (per-monster tier fork: `_is_swarm` → spatial + `continue`; all others → 1D `run_batch`), `:515-518` (upper-tier HP/armor/duration multipliers, independent), `:2924-2929` (per-tier max_duration independence)
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py:1739-1799` (`run_spatial_fight` + `hp_multipliers` per-mob param + length-match assert `:1791`), `:1850` (`effective_hp_mult = caller_hp_mult * MOB_HP_DIFFICULTY_MULTIPLIER`)
- `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py:49` (`MOB_HP_DIFFICULTY_MULTIPLIER = 1.5`), `:52` (`MOB_HP_DIFFICULTY_TIERS = {swarm, magic, elite}`), `:55` (`MOB_HP_DIFFICULTY_SCENARIOS = {open_arena, chokepoint_corridor}`)
- `agentic_orchestration/gandalf/notes/2026-06-15-rogue-degeneracy-role-floor-diagnosis-for-kr.md` §3 (caster reconciliation — pre-registered branch-4 prediction this run tests)
