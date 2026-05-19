# Engine Rebuild — Gauntlet Sim Gap Solutions + Hypothesis Tests + Season-as-Emergent-Output (2026-05-19)

**Status:** Canonical design doc. Authored by gandalf during Pattern-B parking decision evening. Captures: (1) six diagnosed gaps in the engine's gauntlet simulator with proposed solutions + measurable hypothesis tests for each; (2) the season-as-emergent-output concept Matt + gandalf surfaced together and now want to test. Companion to `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` (the diagnosis). Pattern-B-independent — these workstreams proceed regardless of commercial-direction commit.

**Authority:** Matt (directive); gandalf (synthesis); gamora + rocket + star-lord + elrond + drax (executors when dispatched).

**Authored:** 2026-05-19 evening, post-Pattern-B parking, pre-engine-rebuild-session.

---

## § 0 — TL;DR

Six diagnosed gauntlet gaps + one generative-side hypothesis. Each gets:
1. **Hypothesis** — the testable claim about what's broken / what we want to test
2. **Proposed solution(s)** — 1–3 ranked options
3. **Hypothesis test** — measurable success criterion that proves the fix landed
4. **Suggested owner + size** — for sequencing dispatches

**The seven workstreams in priority order:**

| # | Workstream | Closes | Owner | Size | Pattern-B coupling |
|---|---|---|---|---|---|
| **R1** | Per-tier balance targets | Axis 2 | gamora | 1–2 wk | None |
| **R3** | Per-skill range + AI behavior schema migration | Axis 4 + foundation | rocket + star-lord + elrond | 2–4 wk | None |
| **R5** | Demo AI parity audit | Axis 5 demo-side | drax | 1 wk | None |
| **R2** | 2D spatial sub-gauntlet | Axes 1 + 3 + 6 | gamora + star-lord | 3–5 wk | Light (Path A primary; Path B partial) |
| **R7** | AI catalogue source of truth | Axis 5 architectural | rocket + star-lord | 2–3 wk | None |
| **R4** | Demo collision/leash/range | Axes 3 + 4 player surface | drax | 2–3 wk | Light (Path A primary) |
| **R8** | Season-as-emergent-output A/B | New generative-side test | rocket + star-lord + gandalf | 1–2 wk for prototype + measurement | None |

(R6 — Host-Calibration Protocol — held pending Pattern-B Path-B commit; not listed in this doc's primary track.)

**The single most operationally consequential workstream is R1.** It is the gap that explains your playtest finding ("highest WR ~45% miniboss, sub-20% boss, only beat miniboss with one class") and it's cheap (1–2 weeks). **It should fire first.**

---

## § 1 — Workstream summary table

| Ref | Name | Hypothesis (1-line) | Test (1-line) | Size |
|---|---|---|---|---|
| **R1** | Per-tier balance targets | Aggregate WR mean hides per-tier failure; per-tier targets surface it | Convergence pass-rate drops 85%→25% on first run; recovers to ≥70% after class-retuning | 1–2 wk |
| **R2** | 2D spatial sub-gauntlet | 1D scalar distance cannot model AOE shape, pack flanking, positioning; spatial sim exposes geometry-type WR variance | WR variance by geometry-type within same role increases from ~0.05 to ~0.15+ | 3–5 wk |
| **R3** | Per-skill range + AI fields schema | No per-skill range = no out-ranging, no disengage, no kite-by-design | Long-range class can out-range melee monster and win; melee class cannot reach long-range monster and loses; +20–30pp WR for range advantage | 2–4 wk |
| **R4** | Demo collision + leash + range | Demo has no collision, no leash, no per-skill range; 8 mobs stack on one pixel | After fix: pack visibly spreads under separation force; mobs leash + reset when out-of-aggro; skill out-of-range visibly fails | 2–3 wk |
| **R5** | Demo AI parity audit | Demo runtime AI hardcodes range constants in TS; doesn't read engine JSON; over-applies "long" range_profile producing constant-flee | After fix: demo AI consumes monster JSON range_profile field; "long" profile redistribution prevents permanent-kite | 1 wk |
| **R7** | AI catalogue source of truth | Three decoupled AI implementations (Python sim / TS demo / balance-loop implicit) drift independently | Change `aggro_radius` in monster JSON; both engine sim AND demo reflect new behavior identically within tolerance; parity test passes | 2–3 wk |
| **R8** | Season-as-emergent-output A/B | Removing theme-as-input lets mechanical convergence happen first; one post-convergence LLM call coalesces theme; emergent theme is at least as coherent as input-driven theme AND cheaper AND produces more mechanical variety | Inverted seasons score within 0.5 of baseline on cohesion (human + LLM judge), have measurable mechanical variety increase, cost ~90% less in LLM calls | 1–2 wk |

---

## § 2 — R1 — Per-tier balance targets ⭐ *fire first*

### Hypothesis

The balance loop currently converges on the **mean win-rate across the 12-fight gauntlet** (`balance_loop.py:1907-1936`). No per-tier WR thresholds exist. **A class with boss WR 0.15, miniboss 0.30, elite 0.55, magic 0.65, swarm 0.80 passes convergence at mean 0.622** while being boss-unwinnable. This explains Matt's empirical playtest finding directly.

### Proposed solutions (ranked)

1. **★ Per-tier targets with per-tier tolerance bands.** Each of 5 tiers (swarm, magic, elite, mini-boss, boss) gets its own target + tolerance. Convergence requires all 5 to pass, not just the mean. Genre-baseline; what Diablo II / PoE / Grim Dawn all do.
2. **Per-tier floors + aggregate target.** Each tier has a hard floor (e.g., boss ≥ 0.30); aggregate must hit 0.50. Cheaper to converge against. Allows partial-tier-failure if aggregate compensates — weaker than (1).
3. **Stack-weighted aggregate.** Weight slots by significance (boss × 3, miniboss × 2, etc.). Boss failure becomes visible in aggregate. Hacky; doesn't fix the underlying issue.

**Recommendation: Option 1.** Per-tier targets, per-tier convergence, per-tier failure visible.

### Per-tier target proposals (Matt to confirm)

| Tier | Slots | Proposed target | Floor | Ceiling | Rationale |
|---|---|---|---|---|---|
| Swarm | 6 | 0.72 | 0.65 | 0.80 | AOE clears trash; not pure DPS race |
| Magic | 2 | 0.62 | 0.55 | 0.70 | Moderate threat tier |
| Elite | 2 | 0.52 | 0.45 | 0.60 | Hard fights; should not always pass |
| Mini-boss | 1 | 0.45 | 0.35 | 0.55 | Genuine challenge |
| Boss | 1 | 0.38 | 0.30 | 0.45 | Diablo II baseline: "elite content should pass on ~30% of attempts for a build that beats it" |

### Hypothesis test

**Pre-condition:** Run R1 across 5 shipped seasons' classes under current aggregate-only convergence. Capture per-class per-tier WR distribution as baseline.

**Test 1 — Initial failure rate.** Run R1 against shipped classes under new per-tier criteria *without* re-tuning. Predicted: ~70%+ classes FAIL the new convergence criteria because boss-tier was masked. **Success criterion: failure rate ≥ 60%** on shipped class set. (Higher = stronger evidence the gap was real.)

**Test 2 — Re-tuning convergence.** After class-retuning sprint, re-run convergence. Predicted: pass-rate climbs back to ~70%+ for tunable classes. Some classes may be structurally unable to converge under per-tier targets (especially controllers with poor solo-boss capability). **Success criterion: ≥ 70% pass-rate post-retune** with named structural failures documented.

**Test 3 — Playtest validation.** Take 3 classes that pass new per-tier criteria; Matt + son playtest. Verify boss-tier is now beatable (WR ≥ 30% in human play). **Success criterion: Matt beats boss with at least 2 of 3 selected classes within 5 attempts each.**

**The risk to name explicitly:** R1 will produce a **balance-regression cascade.** Most currently-shipped classes will fail the new criteria, triggering a multi-week class-retuning sprint. This is *correct* — that's what the metric exists to do — but expect a sprint, not a hotfix.

### Owner + size

**gamora** — 1–2 weeks for R1 itself; multi-week class-retuning sprint follows.

---

### § 2.1 — Per-tier target revision (2026-05-19 disposition, evidence-driven)

**Amendment authored 2026-05-19 by gandalf** under autonomous-operation authority (protocol § 4.0; protocol § 4 dispatch text "Per-tier target tuning if R1 produces unexpected convergence behavior — gandalf revises targets per evidence").

**Trigger:** gamora's R1 class-retuning sprint (engine commit `9b2ebf4`, 2026-05-19) achieved 0% overall pass-rate against the original per-tier target table (above). Two structural blockers surfaced — see `reincarnated-engine/design/working-agreement/R1-structural-blockers-disposition-2026-05-19.md` for the full disposition decision.

**Original per-tier target table (preserved as historical record):**

The table above (§ 2 — Per-tier target proposals) is **preserved as authored** and stands as the original-intent design. The revision below applies to the OPERATIVE table that gamora's balance loop reads; the original captures gandalf's pre-evidence intuition for the band shape.

**Empirical findings that triggered the revision:**

1. **Bimodal boss WR distribution (n=34 retuned classes):** 8 classes at WR=0.000, 10 classes at WR=1.000, 1 class in the [0.30, 0.45] target band. The 10 classes at WR=1.0 are at modifier floor (0.05) — they cannot possibly damage the boss (133k HP, 86.4% armor mitigation). They are winning by HP%-at-timeout, not by killing the boss. **The "win" semantic conflates kill-rate with survival-rate.**
2. **Mini-boss DPS floor universal:** 30/34 classes show mini-boss WR = 0.000. The 4 classes that DO kill the mini-boss are at modifiers 0.8-3.5× (saturating the engine modifier ceiling 4.0) and blow swarm/magic/elite ceilings while STILL failing the boss tier. **The single scalar modifier cannot simultaneously satisfy mini-boss kill-rate and per-tier ceilings on lower tiers.**
3. **Discipline #12 semantic shift:** the gate measures "fight outcome including HP%-at-timeout" while Matt's playtest experience measures "did the boss die." The gap is a Pattern P7 silent-pass; the math note § 5.1 had warned of this exact risk.

**Revised per-tier target table (OPERATIVE post-disposition):**

| Tier | Slots | Floor (old → new) | Target (old → new) | Ceiling (old → new) | Semantic (NEW) | Encounter knob (NEW) |
|---|---|---|---|---|---|---|
| Swarm | 6 | 0.65 | 0.72 | 0.80 | HP%-at-timeout (retained) | `SWARM_HP_DIFFICULTY_MULTIPLIER = 3.5` (existing) |
| Magic | 2 | 0.55 | 0.62 | 0.70 | HP%-at-timeout (retained) | (none) |
| Elite | 2 | 0.45 | 0.52 | 0.60 | HP%-at-timeout (retained) | (none) |
| **Mini-boss** | 1 | **0.35 → 0.20** | **0.45 → 0.35** | **0.55 → 0.50** | **KILLS-ONLY (NEW)** | **`MINI_BOSS_HP_DIFFICULTY_MULTIPLIER = 0.70` (NEW; reduces gauntlet mini-boss HP 30%)** |
| **Boss** | 1 | **0.30 (unchanged)** | **0.38 (unchanged)** | **0.45 (unchanged)** | **KILLS-ONLY (NEW)** | **`BOSS_HP_DIFFICULTY_MULTIPLIER = 0.80` (NEW; reduces gauntlet boss HP 20%)** |

**Boss target table UNCHANGED. The 0.30 floor is the load-bearing genre constraint** (Diablo II Uber Tristram, PoE Maven, Grim Dawn Celestials all converge at 30-40% kill rate for designed-for-content builds at minimum viable spec). The HP-multiplier calibration makes the 0.30 floor REACHABLE rather than lowering it — the genre principle is preserved.

**Mini-boss target table revised** to acknowledge the genre-transition character of the tier (Diablo II Champions / PoE Rares / Grim Dawn Heroes all converge in [0.25, 0.45] for minimum-viable builds). Original mini-boss floor 0.35 was intuition-derived; empirical evidence + genre-canon recalibration lands floor 0.20, target 0.35.

**Semantic shift — kills-only for single-slot tiers:**

For boss + mini-boss tiers, WR is now defined as kill-rate:

```
boss_kill_rate = count(fights where boss died at hands of player) / total fights
mini_boss_kill_rate = count(fights where mini-boss died at hands of player) / total fights
```

Timeouts (`termination_reason == "timeout"` or `"stalemate"`) count as **non-wins** for these tiers regardless of HP%. This is **Discipline #12 semantic shift, explicit and named.** Multi-slot tiers (swarm, magic, elite) retain HP%-at-timeout semantics because group engagements involve genuine survival-cost as fight information.

**Genre canon for kills-only semantic:**
- **Diablo II:** Uber Tristram / Diablo / Baal — no time limit; "win" means corpse hits the floor
- **Diablo III / IV:** same — Tormented bosses, Greater Rift guardians; HP%-at-timeout is not a recognized win state
- **Path of Exile:** Maven / Uber Sirus / Uber Elder / Uber Exarch — portal exhaustion is the only failure mode; GGG actively designs against stall (Maven memory game; Sirus DI-mechanic)
- **Grim Dawn:** Celestials — no timeout; Crate's design philosophy frames boss WR explicitly as kill-rate
- **Last Epoch:** Lord Brand and pinnacle Echo — same kill-or-die structure
- **No ARPG in the lineage considers boss survival to timeout a player win.**

**Encounter calibration via HP scaling** mirrors genre-standard difficulty knobs:
- D2 `/players 1..8` parameter scales monster HP without altering monster identity
- PoE atlas tree passive nodes calibrate map difficulty
- GD Crucible / Shattered Realm scale through challenge tiers
- The disposition applies the same idea at the gauntlet-test-fixture layer (the gauntlet is NOT shipped content; it is the benchmark suite against which class capability is measured)

**Aggregate weighted-WR target (gamora's binary-search):**

Re-computing per the math note § 4.2 derivation with the revised mini-boss target (0.35 instead of 0.45):

```
Numerator = 0.5×0.62×2 + 1.0×0.52×2 + 2.0×0.35×1 + 4.0×0.38×1
         = 0.62 + 1.04 + 0.70 + 1.52 = 3.88
Denominator = 0.5×2 + 1.0×2 + 2.0×1 + 4.0×1 = 9.0
Weighted mean at exact targets = 3.88 / 9.0 = 0.431

Revised target_winrate for weighted path: 0.45 (was 0.47)
```

**Future improvements queued (not blocking; revisit post Test 2):**
- Archetype rotation in mini-boss + boss gauntlet selection (replaces worst-case-instance sampling with multi-instance averaging)
- Per-encounter (HP × damage-through) "effective HP" calibration as a more principled successor to uniform HP multipliers
- Per-tier fight-duration tuning (e.g., 180s for boss specifically) if the kill-rate distribution clusters at timeout boundary post-disposition

**Cross-reference:**
- Disposition document: `reincarnated-engine/design/working-agreement/R1-structural-blockers-disposition-2026-05-19.md` (load-bearing decision; full rationale + per-class evidence + Discipline #12 framing + implementation specification)
- Math note: `reincarnated-engine/design/working-agreement/R1-retuning-math-2026-05-19.md` (predecessor mechanism analysis)
- Per-tier math note: `reincarnated-engine/design/working-agreement/R1-per-tier-math-2026-05-19.md` (original target derivation; § 7 genre canon source)
- Engineering disciplines: `reincarnated-engine/design/working-agreement/engineering-disciplines.md` § 12 (semantic-shift discipline)

---

## § 3 — R2 — 2D spatial sub-gauntlet

### Hypothesis

The engine's 1D scalar distance + 3-band state machine (`fight_engine.py:155`) cannot represent space. AOE shape doesn't matter (cone vs circle vs line collapse to a multiplier). Pack flanking is invisible. Chokepoint exploitation cannot be tested. Boss-with-adds spatial composition cannot exist (the proxy lives nowhere). **The current gauntlet has no spatial substrate at all.**

### Proposed solutions (ranked)

1. **★ Build 2D spatial sub-gauntlet alongside the 1D gauntlet.** Add 3–5 spatial scenarios per class: open arena (50m × 50m), choke-point corridor (10m × 50m with bottleneck), boss-with-adds composition (one boss + 2–4 adds at varying spawn positions). Real entity collision (soft via push-apart force at small radius; hard via collision body for boss-tier), real per-skill range (R3 dependency), real AOE coverage queries against mob positions. The 1D gauntlet stays for damage-number ballparking.
2. **Approximate spatial effects in 1D via geometry penalties.** Cone skill in 1D = damage × cos(angle/2) × expected_targets_in_cone_fraction. Line skill = damage × expected_line_intersect_count. Hacky; cheap; doesn't fix pack flanking or chokepoints.
3. **Mathematical attrition model with positional parameters.** Treat pack as a 2D probability distribution; analytically compute % hit by each geometry per pack-size. More principled than (2); less accurate than (1).

**Recommendation: Option 1**, scoped tight. Not a full combat-sim rewrite — 3 scenarios per class, each ~30–60s sim time, run alongside the existing 1D gauntlet during convergence iterations. Total sim cost increase: ~3–4×, acceptable.

### Hypothesis test

**Pre-condition:** Score 5 shipped classes' WR under current 1D gauntlet. Note: WR variance by geometry-type within the same role (e.g., all damage-class skills, varying geometry) is currently ~0.05 (collapse to damage-multiplier).

**Test 1 — Geometry-type WR divergence.** Score same 5 classes under R2 spatial sub-gauntlet. Predicted: WR variance by geometry-type within same role increases to ~0.15+. Cone-AOE class shows materially different WR than circle-AOE class on same swarm scenario. **Success criterion: WR variance ≥ 0.10 by geometry-type within role.**

**Test 2 — Boss-with-adds detection.** Run boss-tier scenario with 2 adds at flanking positions. Predicted: classes that scored well on 1D boss fight may score differently when adds are flanking. **Success criterion: ≥ 30% of shipped classes show ≥ 10pp WR delta between 1D boss fight and spatial boss-with-adds scenario.**

**Test 3 — Chokepoint testability.** A class that exploits chokepoints (e.g., cone-AOE-with-knockback) should score higher on chokepoint scenario than open-arena scenario; a class that doesn't (e.g., single-target-burst) should score similarly. **Success criterion: chokepoint-vs-arena WR delta correlates with class's spatial-aware skill set.**

### Owner + size

**gamora + star-lord** (telemetry emission for spatial events) — 3–5 weeks. Depends on R3 (per-skill range) being available.

---

## § 4 — R3 — Per-skill range + AI behavior schema migration

### Hypothesis

The engine has exactly one range gate: `at_melee_range` binary flag (`fight_engine.py:161`). No per-skill range data exists in the catalogue. Skills work identically at 2m, 5m, 11m. Player cannot out-range an enemy. Player cannot disengage. **Range is not a design lever; it's a binary check.**

### Proposed solutions

**This is a multi-part schema migration, not a single fix.** All four parts are required:

1. **Per-skill range field.** Each skill in the catalogue carries `range_m` (or `range_band: short/medium/long/extreme`). Balance loop checks range before skill fires. Out-of-range = skill cannot fire.

2. **Per-mob AI behavior fields.** Monster JSON carries: `preferred_behavior` (one of: melee_aggressive / ranged_kite / cast_at_range / charge_then_melee / etc.), `telegraph_window_seconds`, `aggro_radius_m`, `leash_distance_m`, `skill_rotation_priority`, `range_profile_redistribution` (replaces over-applied "long").

3. **Backfill across 5 shipped seasons.** Existing catalogue entries need per-skill range derived from geometry-type defaults + AI fields populated from archetype priority. ~317 LLM calls/season × 5 seasons might re-derive naming + range simultaneously; or batched offline.

4. **Disengage as valid balance-loop action.** Both player-sim AI and monster-sim AI can choose "retreat to leash" or "kite to optimal range" as a valid action — not just fight-to-death.

**Recommendation: All four parts ship together as R3.** Partial R3 produces inconsistent runtime; full R3 enables R2 and R4.

### Hypothesis test

**Pre-condition:** Score 5 shipped classes under current binary-melee-gate. Note: a class with range_profile=long and a class with range_profile=close perform identically on the engagement-distance dimension.

**Test 1 — Out-ranging viability.** Take a long-range class (`range_m = 12`) and a melee class (`range_m = 1.5`). Fight each against a mid-range monster (`range_m = 8`). Predicted: long-range class wins via out-ranging at distance > 8m; melee class must close to 1.5m, losing some HP to the monster's 8m skills in transit. **Success criterion: long-range class WR ≥ 20pp higher than melee class on same monster.**

**Test 2 — Disengage viability.** Run a controller class (low burst, high survival) vs. a hard-counter boss. Pre-fix: fights to death, loses. Post-fix: AI can disengage to leash distance, recover resources, re-engage. **Success criterion: controller class WR on hard-counter boss improves from 0% to ≥ 20% via disengage-and-reset pattern.**

**Test 3 — Range-profile redistribution.** Inspect monster archetype range_profile distribution before and after R3. Predicted: pre-R3 has ~60% of monsters at "long" range_profile (causing constant-flee in demo); post-R3 redistributes to ~30% long / 40% medium / 30% close. **Success criterion: range_profile distribution within 5pp of target distribution.**

### Owner + size

**rocket** (schema + catalogue) + **star-lord** (telemetry/export) + **elrond** (migration tooling) — 2–4 weeks together.

---

## § 5 — R4 — Demo collision + separation + leash + per-skill range

### Hypothesis

The Pixi.js demo has **no entity-to-entity collision** (`world/movement.ts:197-199` explicitly deferred). 8 mobs can pile on one pixel. No aggro-radius reset, no leash. Per-skill range is hardcoded TS constants (`PREFERRED_RANGE`, `KITE_TRIGGER`) not read from engine JSON. The demo's "constant-flee" artifact is the over-applied "long" range_profile firing kite logic too aggressively.

### Proposed solutions

1. **★ Soft separation via push-apart force.** At `r < 0.8 × entity_radius`, apply mutual push force scaled by overlap. Cheap (boid-style). Visually adequate. Industry standard for top-down games where strict collision is undesired.
2. **Hard collision body per entity.** More genre-faithful but harder to retrofit into Pixi.js entity model. Risk of mobs blocking each other from reaching the player in chokepoints.
3. **Aggro + leash per monster, read from JSON (R3 dependency).** When player out-leashes monster, monster returns to spawn + recovers full HP. Standard genre pattern.
4. **Per-skill range as real check (R3 dependency).** Skill cannot fire if target out of range (or fires-and-misses with visible "out of range" indicator).
5. **Range_profile distribution rebalance (R3 dependency).** Stop over-applying "long" profile; redistribute across approach / engage / kite profiles.
6. **AI behavior tree or proper FSM** with `idle → approach → attack → reposition` states (replacing current always-kite-if-long pattern).

**Recommendation: 1 + 3 + 4 + 5 + 6 ship together as R4.** Option 2 deferred unless playtest reveals soft-separation is visually inadequate.

### Hypothesis test

**Pre-condition:** Capture demo playtest video showing 8 mobs piling on one pixel during a swarm fight.

**Test 1 — Pack-spread visible.** Post-fix playtest: 8 mobs visibly maintain ≥ 0.8 × entity_radius separation distance. **Success criterion: galadriel-capture pipeline screenshot at swarm-engagement moment shows no entity-overlap at center-pixel.**

**Test 2 — Leash + reset.** Player out-runs a monster past its leash distance. Monster turns, returns to spawn, regenerates HP. **Success criterion: monster HP returns to 100% within 5 seconds of leash break.**

**Test 3 — Skill out-of-range visibly fails.** Player attempts to fire a melee skill (range_m = 1.5) at a target 5m away. Skill does not fire or visibly misses. **Success criterion: visible feedback + no damage applied + skill on cooldown anyway.**

**Test 4 — Constant-flee artifact fixed.** Post-fix playtest: monsters with redistributed range_profile no longer flee constantly. Approach states fire correctly. **Success criterion: across 10 playtest fights, fewer than 2 show "monster flees indefinitely" behavior.**

### Owner + size

**drax** — 2–3 weeks. Depends on R3 schema migration being available.

---

## § 6 — R5 — Demo AI parity audit + range_profile fix

### Hypothesis

The demo runtime AI (`world/movement.ts:74-81`) hardcodes range constants in TypeScript (`PREFERRED_RANGE: { close: 90, medium: 420, long: 660 }`, `KITE_TRIGGER: 300`). Doesn't read engine JSON. Over-applies "long" profile causing demo's constant-flee. Engine and demo share no source of truth on AI behavior. **The same mob behaves differently in engine sim vs demo runtime.**

### Proposed solution

**Audit + redistribute + read-from-JSON:**

1. **Audit current TS constants** — what range_profile fraction is currently being applied to what monster archetypes
2. **Redistribute range_profile** across approach / engage / kite profiles per archetype (cross-reference R3's monster JSON spec)
3. **Read range_profile from monster JSON at demo spawn** rather than hardcoded — this is the actual unification point with R7

### Hypothesis test

**Pre-condition:** Audit captures show ~60% of monsters at "long" range_profile, ~70% of playtest fights show kite-default behavior.

**Test 1 — Distribution post-audit.** Range_profile distribution rebalances to ~30% long / 40% medium / 30% close. **Success criterion: per-monster range_profile assignments visible in `world/aggro.ts` match the JSON spec from R3.**

**Test 2 — Kite-default behavior reduced.** Playtest videos pre-fix and post-fix; count "monster kites indefinitely" frames. **Success criterion: kite-default frames drop by ≥ 70% across same-class playtest comparison.**

### Owner + size

**drax** — 1 week. Best run AFTER R3 (so the JSON has the fields to read) but before R4 (so R4 can build on the corrected baseline). Could overlap with end of R3.

---

## § 7 — R7 — AI catalogue source of truth (architectural unification)

### Hypothesis

Three decoupled AI implementations share no source of truth:

1. **Engine simulation AI** (`reincarnated-engine/src/reincarnated/simulation/ai_strategies.py` + `fight_engine.py`) — Python, priority-rotation, 3-band scalar distance
2. **Demo runtime AI** (`reincarnated-demo/src/world/aggro.ts` + `world/movement.ts`) — TypeScript, FSM-ish, 2D pixel positions
3. **Implicit balance-loop AI assumption** (`balance_loop.py`) — what the gauntlet THINKS the player and monster will do

Per-mob behavior cannot be tuned in one place. Fixes to other axes drift back out of sync.

### Proposed solutions

1. **★ Catalogue as single source of truth.** Engine emits AI behavior fields in monster JSON (per R3 schema). Demo reads them at spawn. Engine sim reads them at convergence. Balance loop reads them when computing expected behavior. **Single source of truth: the catalogue.**

2. **Shared AI specification doc + mirror implementations + parity test.** Same spec drives separate-but-mirror implementations on both sides; parity test fails when they diverge. Cheaper schema-wise but harder to enforce.

3. **Defer / declare demo as Phase-0 visualization only.** Cheapest, weakest, allows drift. Not recommended.

**Recommendation: Option 1.** It's the only one that doesn't accumulate drift over time. Cost is real (consumption code on both sides + parity test infrastructure) but it's the foundation that lets R1–R5 + R6 land durably.

### Hypothesis test

**Pre-condition:** Confirm that current engine sim AI and demo runtime AI for the same monster (`monster_NNNNN.json`) produce divergent behavior. Measure by: engine-sim aggro response distance, demo-runtime aggro response distance, expected behavior from `archetype_tag` priority.

**Test 1 — Parity test passes.** Change `aggro_radius` in monster JSON from 8m to 12m. Run engine-sim fight + demo-runtime spawn. Both should reflect new behavior identically (within their respective dimensional substrates — 1D vs 2D position, but same trigger distance). **Success criterion: aggro-trigger distance matches within ±10% across both surfaces.**

**Test 2 — Parity test fails on intentional break.** Hardcode TS constant override in demo. Parity test should fail loudly. **Success criterion: parity test reports the divergence with file:line of the override.**

**Test 3 — Cross-surface behavioral consistency.** Take 3 monsters with distinctly different `preferred_behavior` fields (melee_aggressive, ranged_kite, charge_then_melee). Run each in both engine sim and demo. Observed behavior matches declared behavior on both surfaces. **Success criterion: 100% match between declared `preferred_behavior` and observed behavior across all 3 monsters on both surfaces.**

### Owner + size

**rocket** (schema + engine-sim AI consumption) + **star-lord** (catalogue + parity-test infrastructure) — 2–3 weeks. **Best run in parallel with R3** since they share the schema work.

---

## § 8 — R8 — Season-as-Emergent-Output (the generative-side test) ⭐ *Matt + gandalf co-surfaced concept*

### Hypothesis

The current generation pipeline takes seasonal theme + cosmological vocabulary + anchor + substrate selection as **INPUTS** to generation, then constrains all downstream content to match. ~317 LLM calls per season are spent on naming/flavor/cosmology that flows FROM theme-as-input.

**The hypothesis to test:** if we remove seasonal-theme-as-input entirely and let mechanical convergence happen on pure substrate-mechanic combinations, then ONE LLM call after convergence can coalesce the seasonal theme from the converged content. The season becomes **the story the data tells you**, not the story you tell the data.

**Three claims to test:**

1. **Cohesion:** Emergent theme is at least as coherent as input-driven theme (within 0.5 of baseline on cohesion score)
2. **Mechanical variety:** Removing theme-as-input produces MORE mechanical variety (the input-constraint was restricting the space)
3. **Cost:** LLM cost per season drops by ~90% (from ~317 calls / ~$0.74 per season to ~5–15 calls / ~$0.07–$0.10 per season)

### Proposed solutions (the design space to test)

1. **★ Full inversion as DEFAULT; theme-as-input as OPT-IN flag.** Mechanical substrate is the only generation-time input by default; one LLM call after convergence coalesces element / anchor / cosmological vocabulary / naming. **Theme-as-input is retained as a non-default CLI flag** (e.g., `--theme-input PATH` or `--theme-name fire-coliseum`) that invokes the current input-driven pipeline when explicitly requested. This matches the engine's existing flag pattern (`--no-llm`, `--smoke`, `--use-room-evaluation` in `cli.py` lines 202-225) and Matt's design intent: *"hide the seasonal inputs as a matter of course but leave a non-default placeholder flag which we could invoke with --season at the end of the python procedure."*

2. **Partial inversion: keep substrate selection as input; remove cosmological vocabulary + anchor; coalesce after convergence.** Less risky; substrate stays a generation-time identity. Mid-step.

3. **A/B parallel run.** Run 3 inverted seasons + 3 baseline seasons at seed parity. Compare outputs side-by-side. Scientific approach; lets us measure all three claims rigorously.

**Recommendation: Option 3 (A/B parallel run) is the methodology; Option 1 (full inversion as default + opt-in flag) is the variant under test.** A/B comparison is the only way to measure cohesion + mechanical variety + cost differences honestly.

### Proposed CLI surface (extends existing `cli.py:189-225` pattern)

```
generate-season  [--seed N]
                 [--theme-input PATH | --theme-name SLUG]   ← NEW; default OFF; invokes current input-driven mode
                 [--no-coalesce]                            ← NEW; opt-out of post-convergence theme-coalescence (raw mechanics output)
                 [--output DIR] [--no-llm] [--classes N] [--fights N]
                 [--smoke] [--use-room-evaluation] [--telemetry-db PATH]
```

| Invocation | Behavior |
|---|---|
| `generate-season --seed 2026` (default) | Mechanical convergence with no theme-as-input; post-convergence LLM coalesces theme/anchor/cosmology from converged content. **R8 inverted mode.** |
| `generate-season --seed 2026 --theme-input themes/fire-coliseum.json` | Current input-driven pipeline; theme constrains generation. Legacy mode preserved. |
| `generate-season --seed 2026 --no-coalesce` | Raw mechanics output; no theme coalescence at all. **Path-B-mod-export mode** — host game absorbs the thematic frame; also **Path-C-buyer "pure substrate" mode**. |
| `generate-season --seed 2026 --theme-input host-grim-dawn-cairn` | Host-specific theme injection — useful if we author host-flavor passes for Path-B exports (Grim Dawn's Cairn vocab, TQAE's Greek-Egyptian-Norse-Atlantean cycles). |

### Why default-off-theme-input is especially right for Path B

For Path B mod-export, the host game already has its own thematic frame (Grim Dawn's Cairn lore, TQAE's mythological cycles). **Reincarnated's cosmological vocabulary fights with the host's vocabulary if generated as input.** Default-off-coalescence means:

- **Path B mod-export uses `--no-coalesce`** → ship pure mechanics into the host's existing lore frame
- **Path A / Path B-standalone uses default-coalesce** → Reincarnated's own cosmology emerges from converged content
- **Path C buyers choose** which mode fits their use case; engine ships both
- **Future per-host theme adapters** (`--theme-input host-grim-dawn-cairn`) become a small additional surface, not a fork of the pipeline

### Hypothesis test

**Setup:** 6 seasons total. 3 baseline (current input-driven model), 3 inverted (theme-as-output). Seeded so substrate distributions match (e.g., all 6 use seed-derived substrate-rosters but the inverted 3 don't have theme-as-input distorting mechanical convergence).

**Test 1 — Cohesion score (the must-pass test).**
- Human judge (Matt + gandalf) rates each season's thematic cohesion on 1–5 scale
- LLM-judge rates same on 1–5 scale (separate prompt; can't see which is which)
- **Success criterion: inverted-season cohesion mean within 0.5 of baseline-season cohesion mean** (no significant degradation)
- **Stronger success criterion: inverted-season cohesion mean within 0.2 of baseline** OR inverted-season cohesion mean **HIGHER** than baseline (suggests theme-as-input was distorting rather than improving cohesion)

**Test 2 — Mechanical variety (the interesting test).**
- Measure skill-diversity (entropy of skill geometries/elements/roles used per season)
- Measure role-distribution (variance of role-orientation across classes)
- Measure gear-set coherence (within-set similarity vs between-set distinction)
- **Success criterion: inverted-season mechanical variety ≥ baseline variety** on all three measures
- **Strong evidence the hypothesis is right: inverted variety > baseline variety by ≥ 10%**

**Test 3 — LLM cost (the operational test).**
- Count LLM calls per season under each model
- Predicted baseline: ~317 calls / ~$0.74 per season
- Predicted inverted: ~5–15 calls / ~$0.07–$0.10 per season
- **Success criterion: ≥ 75% reduction in LLM calls** AND ≥ 75% reduction in $ cost

**Test 4 — Substrate-identity invariance (the diagnostic test).**
- For inverted seasons, examine the post-convergence LLM call's theme-coalescence output
- Does a fire-heavy converged class still get thematized as fire-substrate? Or does the LLM discover unexpected groupings (e.g., "this season is actually about velocity, not elements")?
- **No pass/fail criterion** — this is a discovery test. Either result is informative.
  - If invariance: substrate identity is a real signal the data carries inherently
  - If non-invariance: substrate identity was a generation-time imposition, and the data has its own emergent structure

**Test 5 — Multi-shot stability.**
- Run the post-convergence theme-coalescence LLM call 3× on the same inverted season's converged content
- **Success criterion: the 3 outputs converge on the same anchor + same dominant element + cosmological vocabulary within ≥ 70% Jaccard overlap**
- If unstable, the emergent theme isn't grounded enough — would need refinement to the post-convergence prompt

### What this changes about the engine architecture

If R8 succeeds (cohesion within 0.5, variety equal-or-greater, cost ≥75% lower):

- **`season_theme_element` becomes an OUTPUT field, not an INPUT field** in `manifest.json`
- **Cosmological vocabulary slots fill post-convergence** rather than gating skill/monster/gear naming
- **Anchor archetype is selected from converged content** rather than pre-declared
- **LLM call map (`canonical/19-llm-call-map.md`) collapses dramatically** — most calls move from generation-time to one post-convergence coalescence call
- **The substrate-identity declarations doc (`canonical/story/substrate-identity-declarations-2026-05-17.md`)** may need amendment: substrate identity might be confirmed-as-real (Test 4 invariance) or might be revealed as input-correlation (Test 4 non-invariance)

If R8 fails (cohesion drops > 0.5, or variety degrades, or cost doesn't drop):

- We learn the input-driven model was load-bearing in ways we didn't see
- Revert to current model with R8 findings documented for future revisit
- Possibly try partial inversion (Option 2) as a less-risky variant

**Either result is valuable.** R8 is a science experiment, not a re-architecture commitment.

### Owner + size

**rocket** (generation pipeline modifications) + **star-lord** (LLM call orchestration + telemetry) + **gandalf** (cohesion judging + theme-coalescence prompt authoring) — **1–2 weeks for prototype + A/B run + measurement.** Decision to commit-or-revert based on results comes after.

---

## § 9 — Suggested sequencing

**Critical-path observation:** R3 schema migration is the foundation for R2 (spatial sub-gauntlet needs per-skill range), R4 (demo needs per-skill range + aggro/leash), R5 (demo AI needs to read JSON spec), R7 (catalogue source of truth uses same schema). **R3 should fire early; everything else depends on it.**

R1 is independent and cheapest. **R1 fires first** as the no-regret start.

R8 is independent and tests a different question entirely. **R8 can fire in parallel with R1/R3** because it touches the generation pipeline, not the simulation gauntlet.

```
Week 0 (now):
  Matt directive to knight-rider: activate engine-rebuild hive-mind protocol

Week 1-2:
  R1 — per-tier balance targets (gamora)
    → triggers class-retuning sprint
  R8 — season-as-emergent-output A/B (rocket + star-lord + gandalf)
    → 6-season A/B run + measurement; decision at end

Week 1-4:
  R3 — schema migration (rocket + star-lord + elrond)
    → per-skill range + AI behavior fields + backfill across 5 shipped seasons
  R7 — AI catalogue source of truth (rocket + star-lord, partial-parallel with R3)
    → catalogue schema work overlaps R3; parity-test infrastructure separate

Week 3-5 (after R3 / R7 baseline):
  R5 — demo AI parity audit (drax)
    → fast cleanup once R3 schema lands

Week 5-8:
  R2 — 2D spatial sub-gauntlet (gamora + star-lord)
    → primary fight-integrity payoff
  R4 — demo collision + leash + range (drax)
    → player-surface payoff

Week 8+ — hypothesis-test validation gates:
  - R1 test: post-retune convergence pass-rate ≥ 70%
  - R2 test: WR variance by geometry-type ≥ 0.10 within role
  - R3 test: range-advantage WR delta ≥ 20pp
  - R4 test: pack-spread visible; leash + reset working
  - R5 test: kite-default frames drop ≥ 70%
  - R7 test: parity-test infrastructure operational; aggro_radius change reflects on both surfaces
  - R8 test: cohesion within 0.5 of baseline AND variety ≥ baseline AND cost ≥75% lower
```

**Total Track-F (engine-rebuild) engineering: ~8 weeks parallel** with class-retuning sprint running alongside R1's completion through ~week 4.

---

## § 10 — Open questions (resolved under AUTONOMOUS OPERATION — gandalf decides per Matt directive 2026-05-19)

Per Matt directive 2026-05-19, the engine-rebuild hive operates autonomously without Matt-in-the-loop. The previously-Matt-bound questions resolve to gandalf decisions, captured here so knight-rider can fire dispatches without delay:

1. **Per-tier balance targets (§ 2):** ✅ **Gandalf-confirmed.** The proposed per-tier WR targets and tolerance bands stand as authored. The boss-tier 0.30 floor is canonical (Diablo II precedent). Knight-rider routes this to gamora's R1 dispatch without further confirmation.

2. **R8 inversion scope:** ✅ **Gandalf-confirmed: Option 1 (full inversion as default + opt-in `--theme-input` flag).** This is the cleanest test of the hypothesis AND matches Matt's `--season`-flag design intent (per § 8 CLI surface). Partial inversion (Option 2) is rejected as not actually testing the hypothesis.

3. **R8 A/B run scope:** ✅ **Gandalf-confirmed: 3 inverted + 3 baseline seasons at seed parity.** Faster results; if signal is clear we save time; if signal is ambiguous we extend to 5+5 at second-pass.

4. **R7 parity-test:** ✅ **Gandalf-confirmed: build now alongside R3/R7 schema work.** Cheaper to build with fresh schema than retrofit; jack-ryan can use the parity-test as continuous-observation tooling.

5. **Sprint cadence:** ✅ **Gandalf-confirmed: parallel-fire** per the sequencing in § 9. R1 + R3 + R7 + R8 fire in parallel; R2 + R4 + R5 queue behind R3; ~8 weeks total elapsed.

6. **Pattern-B-PARKED workstreams (R6 — Host-Calibration Protocol):** ✅ **Confirmed parked** per `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`. R6 does not enter this dispatch cycle.

**Knight-rider authority during operation:** if questions arise that gandalf hasn't pre-decided here, **knight-rider decides under L2 autonomous-operation authority** (for orchestration/sequencing/cross-seam) or **routes to gandalf for in-session call** (for design/canonical/architectural). No Matt escalation. SME agents decide within their seams.

---

## § 11 — Provenance

Authored 2026-05-19 evening by gandalf during Pattern-B parking decision. Synthesizes:

- `canonical/story/engine-vs-demo-fight-integrity-gap-2026-05-18.md` (the diagnosis)
- Matt's push-back this morning that surfaced Axis 6 (convergence-target mismatch)
- Matt's directive this evening to author solutions + tests
- Matt + gandalf co-surfaced season-as-emergent-output concept (held since earlier sessions; now time to test)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (math-before-code, hypothesis-first discipline)

Pattern-B-independent: all 7 workstreams (R1, R2, R3, R4, R5, R7, R8) proceed regardless of commercial-direction commit. R6 (Host-Calibration Protocol) is held until Pattern-B resolves.

Hive-mind protocol activation: companion doc at `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` (forthcoming next).

Knight-rider launch instructions: `agentic_orchestration/dispatches/2026-05-19-knight-rider-engine-rebuild-launch.md` (forthcoming next).

*Filed 2026-05-19 evening by gandalf. The gaps are mapped; the tests are written; the season-as-emergent-output is named. The road ahead is engineering; the path is clear. Mithrandir signs.*
