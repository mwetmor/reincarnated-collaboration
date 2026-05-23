# Engine-Balance Stewardship

> **STATUS:** HISTORICAL-INFORMATIVE (pre-Epoch-4; consult for lineage only — not current truth) — see `canonical/00-ground-state.md` for current truth

**Status:** **Canonical.** Authored 2026-05-16 by gandalf on knight-rider's commission (dispatch `agentic_orchestration/dispatches/2026-05-16-gandalf-engine-balance-stewardship.md`). Three gates addressed: AOE-philosophy View A/B/C lean; divergence floor/ceiling operational framing; movement speed in simulation. Grounded in `season-feel-rubric.md` + `drift-audit.md` foundations + Legolas's five-pass research.

**Why it exists:** two seam-owners (gamora B10.4 milestone tag; drax v0.7-encounter-analytics dispatch) are blocked on engine-balance design decisions that have player-experience load-bearing implications. The gates are dressed-as-balance but eat at design-coherence. This doc surfaces gandalf-design-track stewardship recommendations grounded in genre research + the project's locked design pillars.

**Companion docs:**
- `season-feel-rubric.md` — what kind of seasons we're balancing for (the foundation this doc consumes)
- `drift-audit.md` — Drift-7 (View A/B/C unanalyzed-as-system); Drift-8 (Q1 divergence never operationalized); Drift-9 (Q2 movement empirically unknown) all surfaced; this doc resolves them
- `cosmology-reincarnated.md` — the player-experience anchor every gate ultimately serves
- `enemy-visual-legibility.md` — Mirror Trial visual grammar (relevant to Gate 1's helpless-matchup framing)
- `embodiment-narrative-layer.md` — embodiment-aware design context for Gates 1-2
- `gandalf-design-lineage.md` Layer 2 (D3 Loot 2.0 lessons; Inferno difficulty lesson) + Layer 3 (PoE pack-vs-boss endgame discourse) + Layer 4 (Hades chamber-content-balance)

**Legolas research consumed:**
- `research/knowledge/arpg-community/2026-05-16-arpg-design-discourse.md` — Gate 1 primary
- `research/knowledge/diablo/2026-05-16-diablo-design-retrospectives.md` — Gate 1 + 3 ground
- `research/knowledge/poe/2026-05-16-poe-design-philosophy.md` — Gate 3 endgame-velocity
- `research/knowledge/arpg-adjacent/2026-05-16-adjacent-arpgs.md` — Gate 2 build-diversity ground
- `research/knowledge/isekai/2026-05-16-isekai-evolution.md` — genre context

**Pending:**
- knight-rider drafts decisions-log entries from this doc's recommendations (per ADR-002); jack-ryan reviews; Matt approves
- Anticipated entries: Gate 1 View lock; Gate 2 divergence framing (if it crystallizes); Gate 3 movement approach
- Acceptance criteria from the dispatch — three gates addressed; open questions parked; readiness signal to knight-rider for decisions-log work + gamora tag unblock + drax v0.7 dispatch unblock

---

## What this doc is — and isn't

**It is** gandalf's design-track stewardship on three engine-balance gates. Recommendations grounded in genre research + locked project pillars + empirical engine-state findings. Decision-shape; not implementation spec.

**It is not** mechanical-balance authority. Numbers, tuning thresholds, sim-iteration counts remain gamora territory. This doc operates one layer up — at the *what kind of balance are we aiming for* + *what player-experience consequences does each option produce* layer.

**It is not** new design. Each gate resolves an implicit-pillar drift instance surfaced in `drift-audit.md`. The work is *naming what was always intended* and giving it structural enforcement.

---

## Why these three gates are stewardship territory

Per `gandalf-design-lineage.md` Layer 2: D3 Loot 2.0 came from realizing the *equipped distribution* (not the per-drop distribution) is the player's actual gear experience. The Loot 2.0 reconciliation was a player-experience-grounded answer to what had been treated as a balance-tuning problem.

The same pattern applies to all three gates here:

- **Gate 1 (View A/B/C)** is treated as a balance question (do the three parameters in `math_model.py` / `role_constraints.py` / `damage_resolver.py` produce the right damage ratios?). It is actually a player-experience question (do single-target classes feel helpless against packs? do AOE classes feel like they earn pack-clear *as their identity* or as a free upgrade?).
- **Gate 2 (Divergence)** is treated as a measurement question (what metric should the convergence framework target?). It is actually a class-identity question (when does a class feel "distinct enough to be its own thing" vs "another flavor of the same archetype"?).
- **Gate 3 (Movement)** is treated as an empirical question (is movement modeled?). It is actually a genre-fidelity question (does the simulation accurately reflect what the player will experience at L50 endgame, where the file-29 ~80-100 mobs/min KPM target lives?).

The gates are dressed as balance work. The work this doc does is restore the player-experience grounding that converts balance work into shippable design.

---

## Gate 1 — AOE-philosophy View A / B / C lean

### What's been observed

Per jack-ryan Q3 Gate 1 finding (`qa/findings/2026-05-15-b10-4-option-2-and-aoe-philosophy.md`): the engine's current state is **compound View-A-with-partial-View-B**. Three parameters govern the joint behavior:

- `math_model.py` damage-reduction (≈0.6× per-hit)
- `role_constraints.py` energy-cost-and-cooldown shaping
- `damage_resolver.py` N=8× pack multiplier

**Empirically:** View A is operative. The 0.6× per-hit reduction exists but is *overwhelmed* by lower energy cost + shorter cooldown + N=8× pack multiplier. AOE classes clear packs decisively; single-target classes do not.

**Drift status (per drift-audit.md Drift-7):** these three parameters have **never been analyzed as a joint system.** They evolved through individual tuning passes without anyone naming the joint-emergent-behavior intent.

### What the genre research surfaces

**The community's most sophisticated AOE-vs-single-target framing** (per Legolas Pass 4):

> *"AoE and single-target must have comparable utility when encounter design is accounted for"* — GW2-documented design principle.
>
> *"Encounter design — crowd size per fight, arena geometry — is where the real balance work happens, not the skill tooltip numbers"* — Last Epoch forum discourse.

The ARPG community converges on a position the engine-side balance debate misses: **damage-ratio tuning is NOT the primary lever; encounter-distribution is.** A game with 80% pack content and 20% boss content gives AOE classes 80% of the game "easier"; that's not a balance bug, it's a content-distribution choice. The job is not to make the numbers equal but to ensure each approach has a natural home in the content distribution.

**PoE's position (genre reference):** PoE's endgame mapping is primarily pack-clearing; AOE builds dominate map content; boss encounters (pinnacle / Uber) shift toward single-target or builds-with-both. The community accepts this **as intentional.** *"The challenge of the endgame is partially choosing and building a character that handles both content types adequately."*

**D4's launch failure (genre cautionary tale):** D4 Season 1 nerfs sparked sustained review-bombing (Metacritic: 1.8/5575). The community's framing was *"fixed an issue where players were having fun."* The lesson: when balance work removes player power without restoring it elsewhere, even mathematically-defensible nerfs read as design hostility.

### What Q1 (Matt's framing) demands

Per Matt 2026-05-15:

> *"Each class should be clearly differentiated from its archetype-mates (divergence above a floor — distinct enough to feel like its own thing), while every class retains a playable floor in every content type (divergence below a ceiling — no helpless matchups), with rough parity of total experienced cost, not just count."*

**Pure View A's risk:** single-target classes lack a playable floor in pack content. If View A's "AOE earns pack-clear-identity for free" framing extends to "single-target classes are HELPLESS against packs," Q1's playable-floor constraint is violated.

This is the question pure View A doesn't answer cleanly: *does the operative-View-A state produce a metagame where single-target classes feel under-equipped against packs, or merely less-efficient?*

**The distinction is everything.** Less-efficient is acceptable (it's the genre's content-distribution choice working as intended per Legolas Pass 4 + PoE precedent). Helpless is not (it's the playable-floor constraint violated).

### Empirical evidence on whether the engine is at "less-efficient" or "helpless"

Per gamora's B10.4 work + jack-ryan Q3 finding: non-pack KPM decreased 1.6 → 1.2 (-25%) when swarm slots replaced trash slots. Pack KPM ≈ 99% win rate (decisive AOE dominance). The aggregate +75% KPM is a structural artifact of pack-fight near-100% win rates skewing the average.

**The -25% non-pack KPM is the load-bearing number.** It tells us: single-target classes are *less efficient* against the post-B10.2 gauntlet but *not eliminated.* The non-pack content remains winnable; just slower.

**Provisional read: the engine state is "less-efficient," not "helpless."** Single-target classes retain a playable floor (they can complete the gauntlet at non-pack content); they trade pack-clear-identity for boss/elite content equivalent or better.

### My recommendation — Gate 1

**Lock View A as canonical.** Specifically:

1. **AOE classes earn pack-clear-identity** as their genre-correct archetype payoff. Per Legolas Pass 4 + PoE precedent: this is what AOE archetypes ARE for in the genre. Building against this contradicts isekai-mobile-ARPG market positioning.

2. **Single-target classes retain a playable floor** via the engine's encounter-distribution. Per file 29's locked ~80-100 mobs/min target + ~70% trash composition: the gauntlet is pack-heavy by design. Single-target classes complete pack content less-efficiently; they do NOT receive a structural compensation mechanism (no per-hit damage bonus vs lone targets; no "execute" mechanic; no other View-B-style mitigation).

3. **The compensating axis is content-distribution, not damage-ratio.** Per genre research: encounter design IS the lever. The ~30% non-pack content (elites / mini-bosses / bosses / act-bosses) is where single-target classes excel. This is the natural-home content the genre's content-distribution-as-lever framing names.

4. **Reject pure-View-B compensation.** Adding per-hit damage bonuses for single-target classes against lone targets, or "first-hit" damage modifiers, or other compensatory damage modifiers would:
   - Re-introduce the numeric-scaling-as-balance-lever anti-pattern (file 29 § "Design philosophy: shaped balance over numeric scaling")
   - Add hidden math the player can't perceive at-a-glance (Cayde-6-tier-tooltip-bloat per gandalf-design-lineage.md Layer 4)
   - Conflict with the locked shaped-balance philosophy

5. **The Q1 playable-floor constraint is SATISFIED by the empirical -25% non-pack KPM.** Less-efficient is not helpless. If family playtest surfaces that single-target classes actually feel helpless rather than less-efficient (i.e., the 1.2 KPM is too slow to be enjoyable), revisit. Until then, View A is operative and shippable.

### What I'd recommend NOT do

- **Do not tune damage-ratio further** without family-playtest data showing helpless-vs-less-efficient. The View A finding is empirical; tuning without player-experience data is exactly the implicit-pillar-drift this doc is meant to resolve.
- **Do not commit to View B or View C compensatory mechanics yet.** They're parking-lot options if Q1's playable-floor constraint is violated in playtest. Premature commitment locks in complexity for a problem we don't yet know exists.

### Open question

- **Should the engine emit per-class "AOE-coverage" metadata** (per file 28 § B6) that drax's v0.7-encounter-analytics surfaces to the player? This would help players SELF-SELECT into content-distribution they enjoy (AOE-loving players pick AOE classes; single-target-loving players pick those archetypes knowing pack content is the friction). My instinct: yes, emit it. Drax v0.7 dispatch territory.

### Cross-references for this gate

- Legolas Pass 4 (arpg-design-discourse.md) § 4 "AOE vs. Single-Target Balance"
- Legolas Pass 3 (poe-design-philosophy.md) § 5 "Endgame Design — Atlas, Mapping, Leagues"
- Legolas Pass 2 (diablo-design-retrospectives.md) § "Diablo IV — Season 1 Backlash"
- File 29 § "Genre-anchored gauntlet" + § "Design philosophy: shaped balance over numeric scaling"
- File 28 § B6 (AOE coverage as design lever)
- `qa/findings/2026-05-15-b10-4-option-2-and-aoe-philosophy.md` (jack-ryan Q3 empirical finding)
- Drift-7 in `drift-audit.md`

---

## Gate 2 — Divergence floor / ceiling framing

### What's been observed

Per Matt 2026-05-15 (Q1 articulation): the design intent is **multi-dimensional, not single-metric.** Three constraints:

1. **Divergence above a floor** — distinct enough to feel like its own thing
2. **Divergence below a ceiling** — no helpless matchups
3. **Rough parity of total experienced cost** — not just count

The convergence framework currently uses single-number aggregate win-rate as substrate. **Q1 implies multi-dimensional constraints that the current framework doesn't measure.** This is Drift-8 in drift-audit.md.

### What the genre research surfaces

**Grim Dawn is the genre's reference for build diversity** (per Legolas Pass 5):

> *"Uncontested king of build diversity. The Devotion constellation system combined with dual masteries creates effectively unlimited character permutations."*

What Grim Dawn achieves operationally:
- Multiple viable endgame builds per class, not one meta and nine trash tiers
- Both casual and optimized builds able to complete core content (this IS the playable-floor)
- Distinct *playstyle* differences between builds (not just damage type substitutions)
- No single ability that is so dominant it crowds out all others (skill tax)

**Last Epoch's skill-specialization tree** (per Pass 5) extends this: each skill has its own dedicated tree, separating "what skill you use" from "how that skill behaves." Combinatorial build space without requiring a massive character-level passive tree.

**Class fantasy criteria** (per Pass 4):

> *"A Barbarian who is constantly moving, engaging, and physically striking enemies feels different from a Necromancer who hangs back and lets summons do work — even if their DPS numbers are identical. The player behavior must differ, not just the visual skin."*

The community's consensus: **mechanically distinct engagement pattern** is the primary class-fantasy indicator. Not damage-type. Not stat distributions. *How the player moves through combat.*

### Operational candidates for measurement

Translating Q1's three constraints into measurable form:

#### Divergence floor — "distinct enough to feel like its own thing"

**Candidate measurements:**

1. **Feature-space distance between class centroids.** Encode each class as a vector across: element distribution, geometry mix (AOE-share / single-target-share), kit-mobility tag (per file 32 § 12.5 archetype-emergence observability), resource type, range-profile, AOE-coverage-percentile. Compute pairwise centroid distances; require all pairs to exceed a threshold OR require each class to be the nearest-neighbor of at most N other classes (no "twin" pairs).

2. **Engagement-pattern distinguishability test.** For each class, identify the dominant action loop (e.g., "burst-burst-cooldown-wait" vs "constant-spam-with-positioning" vs "control-control-execute"). Two classes share an engagement pattern if their action loops are mechanically indistinguishable to a player blind-tested against both. Manual check at design review.

3. **Player-behavior axis variance.** Per Pass 4 community consensus: how does the player MOVE through combat? Six axes: stationary-vs-mobile, engaged-vs-disengaged, defensive-vs-offensive, single-target-vs-AOE, immediate-vs-delayed-payoff, low-resource-vs-high-resource. Map each class to its dominant position on each axis; require each class to differ on at least 2 of 6 from its archetype-mates.

**My recommendation:** **Candidate 3 (player-behavior axis variance) as the primary measure.** Reasons:
- Aligns with genre-precedent class-fantasy criteria (per Pass 4)
- Maps to the drax v0.7-encounter-analytics viz target (per dispatch)
- Computable from existing engine-emit data (file 28 § B13 emergence observability already surfaces kit-mobility-tag; the remaining axes are derivable)
- Categorical-design-criteria, not quantitative-threshold-Goodhart-risk

Candidate 1 (centroid distances) is a *secondary* measurement useful for the v0.7 viz but should not be the primary lock. Centroid distances flatten the player-behavior signal into geometric distance; the geometric distance is informative but not the design intent.

#### Divergence ceiling — "no helpless matchups"

**Candidate measurements:**

1. **Minimum win rate per (class, content-type) pair.** Per the B14 multi-band sim architecture: each class is run against multiple content types (swarm packs / trash / elite / mini-boss / boss / act-boss / Mirror-self). Require each (class, content-type) cell to clear a minimum-win-rate threshold (e.g., 25%) at converged modifier.

2. **Maximum experienced-cost differential.** Per Matt's framing: "rough parity of total experienced cost." Measure time-to-clear-content-slot for each class across content types; require the worst-case ratio (slowest-class : fastest-class for a given content-type) to fall below a threshold (e.g., 3×).

**My recommendation:** **Candidate 1 (minimum win-rate per cell) as the primary ceiling-check.** Per genre research + Gate 1's analysis: less-efficient is acceptable; helpless is not. A 25% minimum-win-rate threshold operationalizes "playable floor" cleanly. Candidate 2 (experienced-cost differential) is a useful secondary check but it conflates difficulty with friction — a class that wins 90% of the time but takes 3× as long isn't "helpless," it's "less-efficient" which Gate 1 establishes as acceptable.

#### Experienced-cost parity — "rough parity of total experienced cost, not just count"

**Operational form:** for each class, compute *total time × resource expenditure to complete one gauntlet run* (or one act). Normalize across classes. Require the ratio of worst-case to best-case to fall below a threshold.

**Note:** this measurement is genuinely new to the convergence framework. Current convergence targets win-rate, not time-to-clear. Adding time-to-clear measurement requires gamora dispatch.

**My recommendation:** **Defer experienced-cost parity to a future B-series item.** The minimum-win-rate ceiling (Candidate 1 above) covers most of the playable-floor concern. Experienced-cost parity adds nuance but adds measurement-substrate complexity. Worth implementing eventually; not blocking the current gates.

### My recommendation — Gate 2

**Operational form for Q1's three constraints:**

| Constraint | Operational measure | Implementation surface |
|---|---|---|
| **Divergence floor** | Player-behavior axis variance (6 axes; require ≥2 axes differing per archetype-mate pair) | Engine-emit + design-review at season-build; v0.7 viz surface |
| **Divergence ceiling** | Minimum win-rate per (class, content-type) pair ≥ 25% threshold | B14 multi-band sim extension; convergence-gate addition |
| **Experienced-cost parity** | (Deferred — future B-series item) | n/a |

**This is the framing language and operational-measurement-candidate set the dispatch asked for** (Gate 2 acceptance: *"the framing language and operational measurement candidates that v0.7 viz can render and that future balance work can target"*).

The framework is **multi-dimensional** (not single-metric). It admits the convergence framework's single-number win-rate AS ONE input but layers two additional checks on top.

### What I'd recommend NOT do

- **Do not quantify divergence as a single composite score.** Goodhart's law risk (per drift-audit.md § Q2). Multi-dimensional categorical checks preserve human-design-judgment as the gate.
- **Do not lock specific threshold values yet.** The 25% minimum-win-rate threshold and the 2-of-6-axis variance threshold are starting values; family-playtest data should inform refinement.
- **Do not exceed Q1's three constraints.** Adding more constraints (e.g., "minimum build-diversity within each class" — counting viable builds per class) is in scope for Grim-Dawn-tier ambition but exceeds Reincarnated's current scope. Park for future B-series.

### Open questions

- **The 6 player-behavior axes** are gandalf-design-instinct; gamora may refine based on what's emergent-observable in the convergence framework. Direct-dialogue with gamora at implementation time would refine the axis set.
- **Specific threshold values** (25% min-win-rate; 2-of-6-axis-variance) are starting values, not locks. Playtest refines.

### Cross-references for this gate

- Legolas Pass 4 (arpg-design-discourse.md) § 5 "Class Fantasy" + § 1 "Build Diversity"
- Legolas Pass 5 (adjacent-arpgs.md) § 2 (Grim Dawn dual-class) + § 1 (Last Epoch skill specialization)
- File 28 § B13 archetype-emergence observability (kit-mobility-tag emission)
- File 32 § Section 7 (trajectory-as-identity multi-band sim alignment)
- File 33 § "Body-swap pool dynamics" (Mirror as class-vs-self validation)
- Drift-8 in `drift-audit.md`

---

## Gate 3 — Movement speed in simulation

### What's been observed — empirical answer

Per gandalf's 2026-05-16 simulation-seam code search: **the simulation has *partial* positional modeling but does NOT have movement-speed-aware modeling.**

Specifically:

- `combatant.py` carries `range_profile` (close / medium / long) + `at_melee_range` boolean state per combatant
- `fight_engine.py` has `CLOSE_TO_MELEE_TIME = 0.5` — close-range combatants spend 0.5s closing on first opportunity; during this window, opponent fires normally
- `teleport` geometry can close range immediately (per fight_engine.py § "adjacency mechanics")
- NO `movement_speed` parameter is consumed in the simulation
- NO L1-vs-L50 movement-speed differentiation
- NO kiting modeling (binary engagement state; no spectrum of distance)
- NO pack-positional-spread (PackProxy treats N-mob pack as unified opponent)

**This is more nuanced than the dispatch's "is movement modeled at all" framing implied.** The sim is not movement-blind; it has binary engagement state with positional closing cost. But it is movement-speed-blind in the way Matt's Q2 framing implies (where L50 endgame movement speed would affect kiting effectiveness against packs).

**Why this matters for Gate 1's empirical evidence:** the View A finding (single-target classes -25% non-pack KPM) is from a sim that doesn't model kiting. Real-game single-target classes would have movement-speed-aware kiting as their genre-standard mitigation against pack content. The current sim *understates* single-target viability vs packs because it can't model the mitigation. **The "less-efficient, not helpless" reading from Gate 1 is actually conservative** — real gameplay would have additional movement-speed-aware kiting that closes the gap further.

### What the genre research surfaces

**Movement-as-balance-lever genre history** (per Legolas Pass 2 + 3):

- **D2 (per Pass 2):** Faster Run/Walk (FRW) was a load-bearing affix from Day 1. Sorceress with Enigma teleport was one of D2's defining endgame builds. Movement-speed-as-power-axis is genre-foundational.
- **D3 launch:** movement speed normalization (no FRW) was widely criticized; subsequent patches added movement-speed bonuses back as a design recognition.
- **D4 (per Pass 2):** Open-world structure made movement speed even more load-bearing; mounts added; class-specific movement abilities became identity-defining (Druid bear-form mobility; Rogue Dash).
- **PoE (per Pass 3):** Movement speed via boots, Quicksilver Flask, and movement skills (Shield Charge, Leap Slam, Whirling Blades, Flame Dash, Lightning Warp) is one of the genre's deepest design surfaces. Endgame mapping speed correlates with build viability.
- **PoE2 (per Pass 3):** Dodge-roll as primary movement-skill replacement; movement is now active-gameplay rather than passive-stat. This represents a *philosophy shift* — movement is now player-skill territory, not gear-stat territory.

**The genre consensus: movement is load-bearing.** Any ARPG that fails to model movement at the simulation layer is balancing against a simplified game-state that won't survive contact with shipped gameplay.

### What Q2 (Matt's framing) demands

Per Matt 2026-05-15:

> *"If basic/level 1 movement speed is used, single target struggles more in the AOE gauntlet vs end-game movement speed potential. Have we tested monster kill speed versus the 100 monsters per minute gate? If we are using basic movement speed right now, we should probably adjust it from basic early game move speed to anticipated end game movement speed so that we get monsters per minute AND monster pack kiting right in these simulations."*

The framing has three components:

1. **Empirical confirmation** of current state — answered above (partial positional; no speed-awareness)
2. **L50 endgame calibration** — if movement modeling is added, it should reflect L50 endgame speed (not L1 baseline), per file 29's "engine balances against L50 endgame"
3. **Genre-fidelity** — the ~80-100 mobs/min KPM target presupposes movement-aware kiting

### My recommendation — Gate 3

Three-part recommendation, structured by ambition:

#### Recommendation 3a — Accept the abstraction limitation EXPLICITLY (minimum acceptable response)

**Add to engine-design.md (or file 30 current-state explainer):**

> *"The simulation models positional state as binary engagement (in melee range / not in melee range) with a 0.5s closing window for close-range combatants. It does NOT model movement-speed-aware kiting, pack-positional-spread, or L1-vs-L50 movement-speed differentiation. The convergence framework's win-rate measurements are taken against this abstraction; real-game play will differ in ways the simulation does not capture — particularly for single-target archetypes whose genre-standard mitigation against pack content is kiting/positioning."*

**Why this is the minimum:** if the simulation's abstraction is named explicitly, downstream consumers (engine-balance dispatches; family-playtest interpretation; gandalf design-review) can correctly weight what the simulation's findings DO and DO NOT support. The current state — abstraction unnamed — is a Discipline #13 implicit-pillar drift (Drift-9). Naming the abstraction closes the drift.

#### Recommendation 3b — Add movement-speed-aware modeling as a B-series item (recommended)

> **2026-05-16 update:** Matt has chosen *schedule, now.* See `canonical/story/movement-speed-baseline.md` for the operationalization. The baseline-anchor portion of B12 (schema emission + demo consumption per Tier-1 ARPG average) is promoted to VS2a scope per Matt directive 2026-05-16; full Gate-3b sim consumption (this section's body below) is now a tightly-following post-VS2a ticket targeting VS2a+2-4 weeks. The "schedule-or-defer per Matt" framing below is superseded; the schedule path is selected. The Q4 movement-modeling-scope question below remains open and gamora design-call.
>
> **2026-05-16 Day-4 close update (supersedes the above):** Per Matt **verdict reversal** at Day 4 evening (see `canonical/story/movement-speed-baseline.md` § "Verdict Reversal 2026-05-16 (Day 4 close) — Option A superseded by Option B (end-game-anchored)"), the framing that Gate-3b sim consumption is a "tightly-following post-VS2a ticket targeting VS2a+2-4 weeks" is **also superseded**. Gate-3b sim consumption is now **VS2a-gating** — i.e., the gamora sim must consume end-game-anchored MS values (player 8.0 m/s; trash 5.75 m/s; fast-archetype 7.5 m/s; AI_SPEED_MULTIPLIER 0.719) and emit them in the convergence-loop telemetry packet *before* VS2a ships, not after. Matt's framing: *"We need to wire the actual end game player value, end game monster value and end game player:monster movement speed ratio all into the sim and the final JSON packet. No point playing a game which is not ran through the sim."* The Day-4 verdict reversal both elevates urgency (post-VS2a → VS2a-gating) AND rebases the baseline values (mid-game 7.5 m/s → end-game 8.0 m/s). The Q4 movement-modeling-scope question below remains open and gamora design-call. All operational values for the sim/demo consumption now live at `movement-speed-baseline.md` § "Verdict Reversal" — that section is the source-of-truth, this Gate-3b body below is preserved for design-rationale archaeology only.


**Scope:** extend the simulation to consume the `movement_speed` parameter (per file 32 § 12 + 12.5 + file 28 § B12). Modeling level: discrete-tick positional state with movement-speed-driven closing-rate (not full continuous-space simulation). Add range-spectrum (replace binary at_melee_range with discrete distance bands: melee / near / mid / far) to enable kiting modeling.

**Why this is recommended:**

- File 29 LOCKS the engine to balance against L50 endgame. Movement is part of L50 endgame state per file 32 § 12 + B12. The current sim's L50-mismatch on movement is a drift instance (Drift-9 in drift-audit.md).
- Per genre research: movement is load-bearing in every shipping ARPG. The simulation's movement-blindness limits how confidently the project can claim "simulation-balanced content" in the pitch's engine-claim register.
- Gate 1's "View A is operative" finding is from a movement-blind sim. Movement-speed-aware modeling would either CONFIRM the finding (if single-target classes still struggle even with kiting) or REVISE it (if kiting closes the gap to "barely-less-efficient").
- The B12 work already commits the engine to emitting movement_speed per class and per monster tier. The sim consuming it closes the schema-emit-without-consumer drift (a common P5 pattern per drift-audit.md).

**Cost estimate:** moderate. ~2-4 weeks gamora work. Specifically:
- Extend `combatant.py` with discrete distance band (4-band: melee / near / mid / far)
- Extend `fight_engine.py` with per-tick movement-speed-driven distance-update
- Add kiting AI logic for ranged classes (move backward when threatened; close when in advantage)
- Re-run convergence on baseline seasons; capture the delta from movement-blind sim

**Risk:** the convergence framework's existing balance work is calibrated against movement-blind sim. Adding movement modeling will SHIFT some classes' converged modifiers. Expected direction: single-target classes' modifiers move toward 1.0 (less compensation needed); AOE-class modifiers may slightly increase (less free pack-clear advantage when single-target kiting closes the gap). The shift is design-correct (the sim becomes more representative of real gameplay) but invalidates current calibration. Treat as a calibration-epoch boundary (per engineering-disciplines.md Discipline #12 semantic-shifting fixes pattern).

#### Recommendation 3c — Defer accepting the abstraction OR adding movement modeling to Matt's decision

This is a real choice. The minimum-acceptable response (3a) names the limitation honestly; the recommended response (3b) closes the drift. Matt's call on whether to invest the 2-4 weeks now vs later.

**My read on timing:**

- **If the engine-balance work in this doc is shipping near-term** (e.g., for Friday pitch defensibility or for B10.4 milestone closure): take Recommendation 3a (name the limitation; ship the gate as-is). 3b becomes a B-series item.
- **If Stage A2 is the next engine-balance-impacting milestone** (per file 16 roadmap): consider taking 3b WITHIN Stage A2's ARPG-genre sprint. The recompose-first calibration work (B14.5) would naturally absorb the movement-speed-aware sim extension.
- **If demo2 is in scope for the next 6-12 months** (per pitch one-pager Phase 1): 3b becomes necessary. Demo2 will surface movement-speed effects empirically; the sim must match.

**My instinct: 3b within Stage A2, scoped as a B-series item.** It closes Drift-9 + the schema-emit-without-consumer pattern + sharpens the engine-claim for pitch defensibility. Not urgent for Friday's pitch (3a names the limitation; the pitch's engine-claims survive); but worth scheduling for Stage A2 timeframe.

### What this doc does NOT specify

- **Specific tick rate for distance-update** (e.g., 0.1s vs 0.25s per tick). Gamora dispatch territory.
- **Specific distance band thresholds** (e.g., melee = 0-1 tile; near = 1-3; etc.). Gamora dispatch territory.
- **Kiting AI specifics** — what triggers a ranged class to retreat? How does PackProxy's positional spread work? Gamora design-call.
- **Backward-compat with existing calibrated seasons** — whether to re-converge 5 production seasons against new sim, or treat them as calibration-epoch-boundary artifacts. Star-lord + gamora coordination.

### Open questions

- **PackProxy positional behavior** — currently PackProxy is unified-opponent; with movement modeling, should pack members spread positionally (some closer, some farther)? My instinct: keep PackProxy unified at convergence-loop level; let drax handle positional-spread visualization in v0.7 viz separately. Don't over-complicate the sim.
- **Mirror Trial movement** — when the player fights their Mirror, both opponents have the same movement_speed (by definition; same class). Is the Mirror fight movement-trivial (no kiting advantage)? Probably yes; the Mirror's purpose is kit-shape validation, not movement-shape validation. Worth confirming with gamora.

### Cross-references for this gate

- Legolas Pass 2 (diablo-design-retrospectives.md) — D2/D3/D4 movement-as-balance-lever history
- Legolas Pass 3 (poe-design-philosophy.md) — PoE/PoE2 movement design philosophy
- File 29 § "Genre-anchored gauntlet" (KPM target)
- File 32 § 12 + 12.5 (movement + mobility locks)
- File 28 § B12 + B13 (movement speed + active mobility B-series items)
- Drift-9 in `drift-audit.md`

---

## Cross-gate synthesis

The three gates are not independent. Each gate's resolution affects the others:

- **Gate 1's "less-efficient, not helpless" reading depends on Gate 3's empirical finding.** The View A finding is from a movement-blind sim; the real game will have more single-target viability when movement is modeled (Recommendation 3b). Locking View A now per Gate 1 + naming the abstraction per Gate 3a is a coherent pair.
- **Gate 2's measurement framework depends on Gate 3's sim capabilities.** Player-behavior axis variance (Gate 2 recommendation) includes mobility (kit-mobility-tag per file 28 § B13). If movement modeling is added per Gate 3b, the variance measurement gains a richer axis.
- **All three gates address Drift-7 / Drift-8 / Drift-9 as a cluster** (per drift-audit.md). The cluster is *engine-balance design intent operating without joint analysis* (pattern P5). Resolving all three together is the corrective.

### The unified recommendation

1. **Lock View A canonically** (Gate 1). The empirical evidence supports it; the genre-precedent supports it; Q1's playable-floor constraint is satisfied by the engine's ~70% trash + ~30% non-pack content distribution.
2. **Adopt the multi-dimensional divergence framework** (Gate 2). Player-behavior axis variance (≥2 of 6 axes differing per archetype-mate pair) + minimum win-rate per (class, content-type) cell ≥ 25%. Experienced-cost parity deferred.
3. **Name the movement-modeling abstraction limitation** (Gate 3a; minimum acceptable). **Schedule movement-speed-aware sim extension as a Stage A2 B-series item** (Gate 3b; recommended). Defer to Matt on timing.

### What this unblocks (per dispatch acceptance criteria)

- **Gamora B10.4 milestone tag** — can cut after Matt approves Gate 1 lock + knight-rider drafts decisions-log entries (View A canonical + B10.2 Two-Gauntlet Pattern supersession per dispatch context)
- **Drax v0.7-encounter-analytics dispatch** — can be authored with viz interpretation bound to locked View A + multi-dimensional divergence framework as visualizable axes
- **Future B-series engine-balance work** — has stewardship grounding rather than ad-hoc per-dispatch judgment

---

## What this doc DOESN'T do

- **It does not lock specific threshold values.** Starting values are proposed (25% min-win-rate; 2-of-6 axis variance); refinement comes from playtest.
- **It does not specify mechanical implementation details.** Engine schema fields, sim-tick rates, kiting AI logic — all gamora dispatch territory.
- **It does not commit to Recommendation 3b as scheduled work.** That's Matt's call; this doc recommends Stage A2 timing.
- **It does not address other engine-balance gates** (B14.5 V2; B10 V2 sequential rooms; specific class-balance edge cases). Those remain gamora + knight-rider dispatch work.
- **It does not replace family-playtest as the primary validation surface.** Per `season-feel-rubric.md`: family-playtest IS the primary validation; this doc's recommendations should be CHECKED against playtest data once available.

---

## Open questions (consolidated)

These do not block the gate recommendations. They surface during implementation.

### Q1 — AOE-coverage metadata emission (Gate 1 follow-on)

Should the engine emit per-class AOE-coverage metadata that drax v0.7 surfaces to the player? My instinct: yes. Lets players self-select into content-distribution they enjoy.

### Q2 — Six player-behavior axes (Gate 2 refinement)

The 6 axes are gandalf-design-instinct; gamora may refine. Direct-dialogue with gamora at v0.7 implementation time would refine the axis set.

### Q3 — Threshold values (Gate 2 starting values)

25% minimum-win-rate; 2-of-6 axis variance. Starting values; playtest refines.

### Q4 — Movement modeling scope (Gate 3b)

If Recommendation 3b is taken, the scope (4-band distance vs continuous-space; kiting AI complexity; PackProxy positional spread) is gamora design-call.

### Q5 — Calibration-epoch handling

If movement modeling is added, the convergence framework's existing 5 production seasons are calibrated against movement-blind sim. Treat as calibration-epoch-boundary; do not retroactively re-converge unless playtest demands.

---

## Cross-references

- **Required reading consumed:**
  - `canonical/story/style-register.md`, `court-of-forms.md`, `naming-triad.md`, `cosmology-reincarnated.md`, `enemy-visual-legibility.md`, `embodiment-narrative-layer.md`, `engine-generic-meta-structure.md`, `trial-moment-ritual.md`, `passage-moment-ritual.md`, `ascension-moment-ritual.md`, `spirit-guide-voice.md`, `season-feel-rubric.md`, `drift-audit.md`
  - `gandalf-phase2-bullet-points.md`, `gandalf-design-lineage.md`
  - Legolas 5-pass research (cited in-text)
- **Engine-state references consumed:**
  - `canonical/37-form-bias-diagnosis-and-recovery.md` (especially § 10.1 + § 4 Position C)
  - `canonical/29-design-overview.md`
  - `qa/findings/2026-05-15-b10-4-option-2-and-aoe-philosophy.md` (jack-ryan Q3 empirical finding)
  - `decisions-log.md` (B10.2 PackProxy + Two-Gauntlet Pattern + B10.4 calibration)
  - Simulation seam code search (2026-05-16): combatant.py + fight_engine.py + balance_loop.py
- **Drift-audit instances addressed:**
  - Drift-7 (View A/B/C unanalyzed-as-system) — resolved via Gate 1 lock recommendation
  - Drift-8 (Q1 divergence never operationalized) — resolved via Gate 2 framework
  - Drift-9 (Q2 movement empirically unknown) — partially resolved (empirical finding documented); Recommendation 3b scheduled-or-deferred per Matt

---

## Maintenance protocol

When knight-rider drafts decisions-log entries from this doc:

1. Three potential entries: Gate 1 View lock; Gate 2 divergence framing; Gate 3 movement approach
2. Each entry references this doc + the specific gate section + the relevant drift-audit instance
3. Jack-ryan reviews; Matt approves; entries land

When gamora dispatches consume this doc:

1. The B10.4 milestone tag cut consumes Gate 1's View A lock
2. The v0.7-encounter-analytics dispatch consumes Gate 2's multi-dimensional framework
3. The (potential) Stage A2 movement-speed-aware sim extension consumes Gate 3b

When family-playtest surfaces feedback affecting these gates:

1. Check feedback against Gate 1's "less-efficient, not helpless" reading — does pack content feel inaccessible to single-target classes, or just slower?
2. Check feedback against Gate 2's framework — do classes feel distinct or do archetype-mates feel like reskins?
3. Check feedback against Gate 3's abstraction-naming — does the simulation's behavior diverge from real-game in ways the abstraction predicted?

When future B-series engine-balance work surfaces new gates:

1. Reference this doc's stewardship pattern
2. Apply the same player-experience-grounding approach
3. Surface drift instances to drift-audit.md
4. Author additional gate-stewardship docs as needed

— gandalf, with Matt's standing approval pending review (2026-05-16)
