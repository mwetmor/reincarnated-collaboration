# 36 — B14.5 Recompose-First Claude CLI Agent Prompt

**Captured:** 2026-05-12
**Purpose:** Copy-paste-ready prompt for the Claude CLI agent at the start of B14.5 (recompose-first iterative tuning loop) work. Primes the agent with the architectural context, nested-loop design lock, and engineering disciplines learned during KI-B6-1 resolution.

## How to use

1. Confirm `v1.3-b6-generator-validated` tag is landed on both engine + demo repos
2. Confirm B14 (multi-band convergence simulator) is fully validated and the 9-runs-per-class harness is reliable
3. Open Claude CLI in the `reincarnated-engine` repo on `stage-a2` branch
4. Paste the prompt block below as your opening message
5. Let the agent orient itself BEFORE engineering begins

---

## Copy-paste prompt block

```
You are beginning B14.5 — recompose-first iterative tuning loop. This is the
natural follow-on to v1.3-b6-generator-validated. The work transforms the
balance loop from "damage_modifier as primary scalar" to a nested-loop
architecture where composition-level levers cycle BEFORE numeric scaling
fallback.

This is a load-bearing piece of work that realizes Section 1's "shaped balance
over numeric balance" lock. Estimated ~1-2 weeks engineering. Do NOT write any
code yet. Your first job is ORIENTATION.

## Required reading (in order)

Read these docs cover-to-cover before proposing any implementation:

1. `canonical/28-engine-arpg-rebalance-design.md` § B14.5
   FULL ARCHITECTURE LOCK. Nested-loop structure, deliverable scope,
   architectural hooks (gear, traits), implementation discipline. This is the
   spec.

2. `canonical/32-progression-design.md` § Section 1
   Anti-pattern locks including "shaped balance over numeric balance." B14.5
   realizes this principle.

3. `canonical/28-engine-arpg-rebalance-design.md` § B14
   Multi-band convergence sim. B14.5 nests INSIDE B14's per-band convergence
   loop. Understand the 9-runs-per-class harness before refactoring it.

4. `engine-repo/design/decisions/decisions-log.md`
   2026-05-12 entries especially:
   - "B6 generator-validated — KI-B6-1 resolution sequence" (variance fix
     discipline; math-before-code lesson)
   - "Trait architecture — dual-source design locked" (trait-fill cycling hook
     context)
   - "Thematic ailment damage signatures — DEFERRED" (alternative path that
     B14.5 may dissolve)
   - "B14.5 scope expansion — nested-loop architecture locked" (the design
     decision you're implementing)

5. `engine-repo/design/known-issues.md`
   KI-B6-1 detail. Understand the empirical state of the engine post-Prop 4
   per-fight variance, the water_mage tightest-baseline diagnostic, and the
   wind_controller attrition-variance pattern.

6. `engine-repo/design/b6-schema-proposal.md`
   B6 schema fields B14.5 operates on (skill role, tier, chain_id, energy_cost,
   cooldown_seconds, geometry, etc.). Understand the primitive surface before
   cycling on it.

7. `engine-repo/src/reincarnated/simulation/balance_loop.py`
   Current balance loop implementation. Identify where damage_modifier
   convergence happens; that's the structural insertion point for the new
   nested-loop architecture.

8. `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_trait_architecture.md`
   Trait fill cycling hook context — what shape the eventual trait-affix lever
   will take. You're scaffolding the extension point.

9. `~/.claude/projects/-Users-admin-Games-reincarnated-collaboration/memory/project_ailment_damage_thematic.md`
   The deferred alternative path. If B14.5 dissolves wind_controller mirror
   match weakness via kit recomposition, this proposal stays deferred. If B14.5
   doesn't fix it, this becomes the next item.

## Critical constraints (DO NOT VIOLATE)

DAMAGE_MODIFIER AS LAST RESORT. The primary insight: the current balance loop
uses damage_modifier as its primary tuning lever, producing 6× spread across
archetypes that all converge to similar win rates. This is the anti-pattern
B14.5 fixes. damage_modifier must be the FALLBACK after composition cycles
exhaust their lever space — not the primary tool.

NESTED LOOPS, NOT FLAT CYCLES. The architecture is hierarchical: cheap inner
cycles (skill swaps, geometry mix, energy/cooldown values) first, expensive
outer cycles (element-distribution variations) second, hooks for the most
expensive (gear loadouts, trait fills) at the outermost layer. Do not collapse
into a flat lever list — the hierarchy matters for compute budget and
attribution clarity.

ARCHITECTURAL HOOKS FOR DEFERRED LEVERS. Scaffold gear loadout cycling and
trait fill cycling as extension points (empty function stubs with clear
extension contracts). Do NOT implement the levers themselves — those wait for
Priority 02/B15 (gear) and B9a (intrinsic traits + gear-affix integration).
The hooks must be plug-in-ready so adding them later is not redesign.

ATTRIBUTION CLARITY. Each composition lever change should be measurable in
isolation. Recording which lever was cycled and what win-rate delta resulted
is part of the deliverable — future analysis (and possibly auto-tuning) will
depend on this telemetry. Extend `convergence_report` accordingly.

REGRESSION BASELINE EXISTS. v1.3-b6-generator-validated is the regression
baseline for B14.5 work. After B14.5 lands, all 25 classes must still pass
[0.20, 0.80] doppelganger gate AND all 1259 tests must still pass AND mean
damage_modifier across classes should drop substantially. If mean
damage_modifier stays similar to pre-B14.5, the recompose loop isn't actually
doing work — it's just calling damage_modifier under a new name.

PARTIAL-TAG PROTOCOL. Tag intermediate states:
  v1.3-b14-5-design        (proposal accepted; before code)
  v1.3-b14-5-primary-loop  (skill-level lever cycling lands)
  v1.3-b14-5-secondary-loop (element-distribution cycling lands)
  v1.3-b14-5-hooks         (gear + trait extension points scaffolded)
  v1.3-b14-5-validated     (full revalidation passes; ready for next item)

## Engineering disciplines (from KI-B6-1 phase learnings)

MATH BEFORE CODE ON NON-TRIVIAL CHANGES. The biggest cost overrun during
KI-B6-1 was attempting Prop 1 (chill on cooldown) and Prop 3 (per-hit damage
variance) without mathematical analysis first. Both failed. The eventual 1/√N
analysis was retrospective — it would have prevented both dead ends if done
upfront. For any new variance, constraint, or fight-engine mechanic: produce
mathematical analysis predicting the change's effect BEFORE implementing.

For B14.5 specifically: each lever-cycling implementation should have an
analytical prediction of how it affects convergence rate, win-rate variance,
and damage_modifier spread. If the prediction doesn't match measured behavior
after implementation, that's the diagnostic signal — don't proceed to magnitude
escalation; re-diagnose mechanism.

CIRCUMSTANTIAL → STRUCTURAL DIAGNOSIS. Don't jump from "this looks like X" to
"X is the root cause." Trace actual code paths. KI-B6-1's "wind_controller has
0 knockouts in 60 fights" was the smoking gun that pointed to structural kit
underdamage — but the agent initially diagnosed it as a variance magnitude
issue. Verify hypotheses against actual fight data before committing to fixes.

EMPIRICAL INSPECTION OVER ASSUMPTION. Before implementing a lever cycle, query
real season data to confirm the lever's domain. E.g., before implementing
"swap skills within archetype role pool," verify what role pools exist in
practice and what skill diversity they actually produce. Use the telemetry DB.

ATTRIBUTION CONTAMINATION RISK. KI-B6-1 surfaced a subtle bug: Prop 1's chill
extension propagated through balance_modifier convergence values, contaminating
the test season. When a B14.5 lever change affects convergence, regenerate the
test fixture(s) so balance_modifiers re-converge against the new lever space.
Otherwise B14.5's measurements will reflect old-loop balance against new-loop
mechanism.

STALE BUILD FIRST. When something looks wrong, FIRST verify build state and
test fixture freshness. Don't deep-dive diagnostics on stale state.

NO PARALLEL REGENS OF THE SAME SEED. During B14.5 dev (2026-05-12), the agent
launched two `generate-season --seed 1005 --no-llm` invocations in parallel —
one filtered with grep, one without. Both UPDATE the same `seasons` row, write
to the same `exports/season_001005/` directory (race condition on file writes),
INSERT duplicate `generation_runs` entries, and double the compute cost.
Correct patterns:
  (a) Run once, capture full output, grep post-hoc on the captured output
  (b) If a second run is genuinely needed (e.g., re-run after a fix), wait for
      the first to complete before starting the second
  (c) Use the smoke-test mode for fast in-development iteration; reserve full
      regens for validation milestones
Never start a regen while another regen on the same seed is in flight.

## Open implementation questions (require design before code)

The B14.5 architecture is locked, but several implementation details need
deliberate decisions before code:

1. SECONDARY LOOP — element-distribution magnitude:
   How much variation in element distribution per cycle? (e.g., 70/30 →
   65/35? → 60/40?) Larger steps explore more, fewer cycles fit in compute
   budget. Smaller steps converge slower. Recommend a logarithmic schedule
   (5% → 10% → 20% deltas) to broaden search if narrow cycles fail.

2. PRIMARY LOOP — exit conditions:
   Each lever cycle has a budget. When to stop trying a lever and move to the
   next? Recommend: 3-5 attempts per lever before progressing.

3. damage_modifier FALLBACK CALIBRATION:
   When composition exhausts, how aggressively to scale? The current loop runs
   damage_modifier tuning until convergence; should B14.5 limit it (e.g.,
   max ±20% from 1.0) to surface "this class genuinely can't be balanced"
   as a regenerate signal?

4. CONVERGENCE REPORT EXTENSIONS:
   What metadata does the telemetry packet record about which lever fired and
   what the win-rate delta was? Recommend per-lever attempt log inside
   convergence_report with `{lever_type, before_winrate, after_winrate,
   delta}` records.

5. EXPERIMENTAL CLASS HANDLING:
   The experimental slot (per `b6_kit_builder.py`) already does primitive
   recompose via the 5-retry/fallback policy. Does B14.5 supersede this with
   the nested loop, or do experimental classes keep their separate path?
   Recommend: nested loop applies to taxonomy-first classes; experimental
   keeps its current 5-retry path (because experimental's variance is
   specifically observation-of-novel-archetypes, not balance-of-known-archetypes).

Surface these and request user decisions BEFORE writing implementation code.

## Your first response

DO NOT write code in your first response. Instead:

1. Confirm you have read the required docs (list which you actually read)
2. Confirm `v1.3-b6-generator-validated` tag exists and reproduces 25/25
   doppelganger pass + 1259/1259 tests
3. Identify your proposed implementation order. Recommend starting with the
   PRIMARY LOOP (skill-level levers) as the minimum viable recompose-first;
   secondary and hooks follow.
4. Surface the 5 open implementation questions above and request decisions
5. Outline your design proposal plan: which markdown file you'll draft
   (modeled on b6-schema-proposal.md), what sections it'll have, what tag
   you'll create on proposal acceptance (v1.3-b14-5-design)

DO NOT begin engineering until the user explicitly confirms:
  - Your chosen first sub-step (primary loop most likely)
  - Resolutions of the 5 open implementation questions
  - The design proposal plan

## Cross-references

If you need to look up specifics:

- B14.5 full architecture: `canonical/28-engine-arpg-rebalance-design.md` § B14.5
- Shaped-balance principle: `canonical/32-progression-design.md` § Section 1
- Trait fill cycling context: `memory/project_trait_architecture.md`
- Deferred ailment damage path: `memory/project_ailment_damage_thematic.md`
- KI-B6-1 resolution detail: `engine-repo/design/known-issues.md` § KI-B6-1
- Variance fix lessons: decisions-log 2026-05-12 entries
- Existing balance loop code: `src/reincarnated/simulation/balance_loop.py`

Acknowledge orientation. Ask questions. THEN we plan implementation.
```

---

## Notes on tuning this prompt

This is a focused-scope prompt (single B-item, ~1-2 weeks) compared to file 35's stage-spanning sprint prompt. Two design choices reflect the focus:

1. **Required reading is heavier on memory files and recent decisions-log entries.** B14.5 is the most context-rich item in Stage A2's remaining queue — it touches the balance loop refactor (KI-B6-1 lessons), the trait architecture (gear/trait extension hooks), and the alternative path (ailment thematic damage). The agent needs to internalize all three before code.

2. **Math-before-code is the explicit first discipline.** KI-B6-1 work surfaced this lesson empirically (Prop 1 and Prop 3 per-hit dead ends would have been caught by upfront math). B14.5 lever cycling has analogous risk — each lever should have an analytical prediction of effect on convergence behavior. Without this discipline, B14.5 risks recreating KI-B6-1's "tune magnitude until pass" anti-pattern at a different layer.

After the user-confirmed primary loop lands:
- Tag `v1.3-b14-5-primary-loop`
- Diff against regression baseline (v1.3-b6-generator-validated): mean damage_modifier should drop substantially; 25/25 doppelganger should still pass; tests should still be green
- Document the lever cycling behavior observed (which levers fired most often; which classes triggered which paths)
- Then ask the agent: "ready for secondary loop — propose plan"

## Revisit signals after B14.5 lands

When `v1.3-b14-5-validated` lands, check whether B14.5 dissolves these deferred items:

- **`project_ailment_damage_thematic.md`** (DEFERRED): Did wind_controllers and other pure-control archetypes land at 30-50% mirror-match win rate via kit recomposition? If yes, thematic damage stays deferred. If no, it becomes the immediate next item.
- **Per-fight variance magnitude** (currently ±25%): Did damage_modifier compress meaningfully (e.g., 0.10-0.20 spread instead of 0.054-0.317)? If yes, consider dialing per-fight variance back to ±15%. If no, ±25% stays.
- **Extension candidates for mage range constraint** (earth_caster, wind_caster, all controllers): Did B14.5 compose around the range mismatch, or do these archetypes still need explicit close-range forbidding? Empirical post-B14.5 data answers this.
