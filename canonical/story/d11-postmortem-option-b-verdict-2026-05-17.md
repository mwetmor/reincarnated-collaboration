# D11 Post-mortem + Option B verdict — STOP

> *[RETIRED OUTCOME — hybrid_mage RETIRED 2026-05-18 per canonical-6 transition; this reference is historical record. See `canonical/story/canonical-6-transition-retire-hybrid-mage-2026-05-18.md` for retire verdict and rationale. See `reincarnated-engine/design/decisions/decisions-log.md` for the RETIRE entry.]*

**Authority:** Matt L3 2026-05-17 late evening — explicit early-stop grant per dispatch `2026-05-17-gandalf-d11-postmortem-option-b-veto-authority.md`.
**Author:** gandalf (story-and-design steward).
**Predecessors:** own D11 advisory (`canonical/story/d11-hybrid-mage-tuning-advisory-2026-05-17.md`); gamora D11 math note (`reincarnated-engine/output/standard-demo-regen-2026-05-17/D11-hybrid-mage-tuning-math-note-2026-05-17.md`); rocket v1.13 completion record + `d11_salvage_summary.json`.
**Type:** Pattern B post-mortem + verdict; gates the D11.1 sprint auto-fire.

---

## § 0 — Verdict TL;DR

**STOP. Do not fire D11.1 with Option B (α=0.08-0.09 + skill-count 12→10).**

Two reasons stacked:

1. **The empirical failure of D11.0 was not a magnitude failure; it was a measurement-site failure.** My advisory pegged α=0.07 against a v1.5 sample where the kit's pre-modifier WR was 1.000 *with full 4-element coverage and all D10-pruned-but-still-redundant skills present*. The post-D11 17 instances are pinning at WR 0.56–0.84 at the modifier floor *after* the tax. That floor pin is not "tax was 7% when it needed to be 35%" — it is "the kit's structural DPS density was not reduced by removing one of four elements and shaving 7% off the remainder; the kit *still over-generates damage* at the worst possible modifier the balance loop can apply." Option B adds another 1-2% of damage tax (insufficient at the same site) plus a 16.7% skill-count cut (which is doing the *right kind of thing* but bundled with a tax that the empirical evidence says is operating on the wrong slot).

2. **A live inspection of season_002012/class_0012 (Cartographer of Erased Borders — my original anchor class) shows that the tax was *measured in salvage but not persisted to skill damage_multiplier values*.** The class JSON has `post_process_d10: true`, the manifest has `post_process_d11: true` and `schema_version: v1.8`, but every skill in the class still has `damage_multiplier = 1.000`. There is no per-class `d11_post_process` field or `element_coverage_tax_multiplier` field on the class object. Rocket's completion record asserts these fields are present "on each hybrid_mage"; the file I read does not have them. This is either (a) the salvage ran the tax transiently to compute a balance-loop result then wrote back the pre-tax kit, (b) the persistence path skipped the tax write, or (c) the class object schema places these fields somewhere I didn't search. Whichever is true, the math note's Site A claim ("damage_multiplier values reflect the tax-applied values; player-visible truth") is empirically not in the on-disk data. **Before D11.1 fires anything, this discrepancy must be diagnosed.** It is possible that D11.0's 6% convergence is *partially* a persistence bug, not solely a magnitude failure — and Option B compounds magnitude without diagnosing the underlying issue.

**Recommended alternative: Option C (skill-count ceiling only, 12 → 9 or 12 → 10) plus a Discipline-#1+#11 diagnostic gate before D11.1 fires.** Skill-count is the structural lever — it reduces DPS density at the source by capping the kit's outbound-damage surface area. The tax was the wrong primary lever for the magnitude problem the engine has. The tax can remain as identity-flavor at α=0.05 or even at zero, gated by what the diagnostic gate reveals. § 5 details the alternative shape.

The rest of this doc: § 1 self-critique on the math-before-code projection failure; § 2 Option B compatibility analysis with chromatic_mage design intent; § 3 the rename timing recommendation; § 4 the persistence-bug finding from live data; § 5 the Option C alternative; § 6 open questions for Matt; § 7 handoffs; § 8 engineering-discipline cross-refs.

---

## § 1 — Sub-Q 1: self-critique on the math-before-code projection failure

The dispatch is right to demand this section regardless of verdict. The lesson is durable.

### § 1.1 — What went wrong in the projection

My D11 advisory claimed α=0.07 would land the v1.5 Class C analog "post-modifier convergence WR ≈ 0.73 × 0.93 ≈ 0.72 → balance loop should find convergence modifier ~0.06-0.12." That projection had three structural defects.

**Defect 1 — Wrong genre anchor.** I anchored against the D2 Sorceress specialist-vs-split DPS differential (~40-50%; advisory § 2.2 + § 12.1). The mapping went: D2 split-Sorceress is the worst-case "player chose breadth in a system that punishes it"; Reincarnated's hybrid_mage is the intended-playable archetype; therefore Reincarnated's tax should be *lighter* than D2's split-Sorceress empirical penalty. I picked 28% at 4 elements (vs D2's ~50%) and 7% at 3 elements (a 4× quadratic backoff). The logic of "Reincarnated's hybrid is intended-playable" was correct. **The error was assuming that the magnitude required to land the balance loop's convergence target was in the *gentle* range D2's *intended-playable* range would be.** Reincarnated's balance loop is not D2's player-choice-driven leaderboard; it is a *sharp* binary search against a 0.50 target with a 0.05 modifier floor. The genre anchor that should have been load-bearing is *not* "what does breadth cost in a system where the player chose it" — it is "what damage reduction does the balance loop's binary-search empirically need to find a non-floor modifier on a kit currently pinning at 0.77 WR at floor." Those are different questions. The first is a *design-feel* question (mid-tier in leaderboards); the second is an *engineering* question (modifier-floor unstuck condition). I conflated them.

The right anchor would have been: *given a kit currently pinning at modifier=0.05 with conv_wr=0.77, what damage scalar reduction does the balance loop's convergence math require to find an interior modifier?* That is a math question, not a genre question. A 30-second back-of-envelope would have answered it: if the kit deals damage D and the modifier sets effective_damage = modifier × D, the floor-pinned state means even at modifier=0.05, effective_damage × 100 fights still produces WR>0.50. To bring WR=0.77 to 0.55 at the same modifier, you need to reduce effective damage by *roughly* the ratio that converts a 0.77-WR kit into a 0.55-WR kit. WR is not linear in damage — it scales with monster HP / kit DPS roughly inversely, and fight duration compounds (longer fights = more hits taken by player = lower WR). Empirically (per rocket's salvage results), the kit at α=0.07 lost ~10% effective damage but lost only ~3-7% WR. The non-linearity is severe; my projection treated it as roughly linear. **A linear projection on a non-linear function with sharp asymptote behavior at the floor is the math-before-code failure mode here.**

**Defect 2 — Ignored the floor-modifier asymptote.** The balance loop's modifier floor (0.05, with epsilon 0.005) is a hard wall. Kits whose untaxed WR at floor is well above target (the v1.5 Class C had 0.77, well above 0.50) can absorb a substantial damage reduction *without the balance loop moving off the floor* — because the modifier search interprets "still well above target at floor" as "kit needs more damage reduction, not less modifier reduction," and there is no more modifier to give. The kit stays at floor and the WR drops along with the tax. The *only way* to get off the floor is to reduce the kit's structural DPS density enough that the floor-modifier WR lands below target — at which point the loop can find an interior modifier. The empirical conv_wr range of 0.56-0.84 at floor post-tax confirms exactly this: most kits' floor-modifier WR dropped from 0.6-0.8 to 0.56-0.78 (a small drop from a 7% damage cut compounded against fight-duration non-linearity), but only one kit dropped below 0.50, and that one converged. My projection should have included a *floor-pin diagnostic*: "to converge a floor-pinned kit at conv_wr=X, the tax must drive conv_wr below target (0.50) at floor — i.e., the required damage reduction is *the reduction that takes WR from X to 0.50 at the same monster-set*." That is a different math problem than "tax produces roughly proportional WR reduction." I did not run it.

**Defect 3 — No empirical-calibration POC before full salvage.** The dispatch's Sub-Q-3 asks this directly: "Would a small empirical-calibration POC (e.g., rocket smoke-test α=0.07/0.10/0.15 BEFORE full salvage) have caught this earlier?" The answer is **yes, unambiguously yes.** The salvage took 269 seconds for 17 instances. A 3-alpha-point smoke (5 hybrid_mage instances at α=0.07, α=0.15, α=0.25) would have taken ~120 seconds and revealed the floor-pin asymptote behavior immediately. Three data points define the curve: at α=0.07 the kit barely moves; at α=0.15 it might dent the floor pin; at α=0.25 it should converge cleanly. The shape of that 3-point curve tells you both *what α actually works* and *whether α is even the right knob*. If at α=0.25 (substantially harsh) the WR at floor is *still* 0.6+, that's the signal that the tax is not the right primary lever — you're in a structural-DPS-density problem, and the lever needs to be skill-count or kit-shape, not damage scalar.

This is the missing discipline: **before any full-regen / full-salvage with a new lever, run a 3-point parametric sweep on a small sample (3-5 representative classes) to map the lever's actual response curve.** I will propose this as a new engineering discipline (§ 8.1).

### § 1.2 — What I would do differently

Concretely, with the benefit of hindsight, my D11 advisory should have:

1. **Provided two anchor questions, not one.** The genre-feel anchor (what does breadth cost in PoE/LE/D2 — the answer informs *player perception of the tax*) AND the engineering-math anchor (what damage reduction is required to unstuck a floor-pinned kit at conv_wr=0.77 — the answer informs *the magnitude of the tax*). My advisory had only the first.

2. **Computed the floor-pin escape velocity for the v1.5 Class C sample.** Specifically: "Class C floors at conv_wr=0.77; to bring conv_wr to 0.50 at the floor modifier requires reducing effective damage by approximately X (with non-linearity caveat); α=0.07 produces 7% reduction; if X > 15%, α=0.07 is insufficient and a magnitude-only tax cannot land the convergence target." Once X is computed (even roughly), the recommendation either holds or doesn't, and the magnitude is properly anchored.

3. **Recommended a 3-point alpha smoke gate before rocket's full salvage.** Even just naming this as a gate in the gamora math note's § 9 acceptance criteria would have caught the magnitude failure in ~2 minutes of additional sim time.

4. **Acknowledged a meta-uncertainty in the advisory.** I was confident about the *direction* (the tax is the right kind of lever for the right kind of failure mode) but the *magnitude* was anchored against a different system's empirical baseline. The advisory should have said: "α=0.07 is the *design-recommended starting point*; the empirical α may need to be substantially higher (in the 0.15-0.30 range) if the floor-pin asymptote is severe. Run the 3-point smoke first."

### § 1.3 — Where v1.5 Class C convergence sample analysis should have warned me

Re-reading the v1.5 convergence-sample analysis (per dispatch required reading) with the post-D11 lens: Class C (Cartographer of Erased Borders, season_002012, hybrid_mage, 4 elements) had `convergence_winrate=0.773` at `final_modifier=0.0509`. The modifier floor is 0.05. That is *full floor-pin with a 27 percentage-point WR overshoot.* The pre-D11 lens read this as "the kit over-generates; we need a damage tax to absorb the overshoot." The lens I should have applied: **"the balance loop ran 10 iterations of binary search and could not find a modifier interior to [0.05, 1.0] — the kit is so over-generating that no modifier in the searchable range puts it at 0.50 WR. The kit's *structural DPS density* is the problem; the modifier search is the symptom, not the diagnostic."**

The 0.77 conv_wr at floor is *the signal*. It is saying "even at the smallest damage scalar the system has, this kit wins 77% of fights." A 7% damage tax brings that to 0.72 (roughly). A 28% tax brings it to maybe 0.55-0.62 (accounting for fight-duration non-linearity that makes longer fights *worse* for the player, not just proportionally weaker damage). To bring it to *below* 0.50 — at which point the balance loop can find an interior modifier — requires probably 35-50% damage reduction, which is the territory where the archetype is no longer "comfortable mid-tier" but is "structurally crippled."

**The signal I missed:** when a kit pins at floor with WR ≥ 0.70, you are not in tax-tuning territory. You are in *kit-shape* territory. The kit must be made structurally smaller (fewer skills, less coverage, slower CDs) such that its *uncapped* DPS density at modifier=1.0 is no longer in the over-generating band. Then the tax becomes a *flavor lever* on top, not the load-bearing balance lever.

Rocket's empirical result confirms this. The hybrid_mage at 12 skills with 3 elements and α=0.07 still floors. The skill-count ceiling reduction in Option B (and more aggressively in Option C) is the structural lever. The tax is the wrong primary tool for the structural problem.

### § 1.4 — Self-rating on the math-before-code discipline

I missed the discipline. The advisory was rich in genre evidence (§ 2 surveyed 13 ARPGs in detail) and thematic framing (§ 5 substrate-identity alignment), and that work is durable — it remains the right intellectual frame for chromatic_mage. But the lever's magnitude was assigned by analogy, not by computation against the empirical data the engine already had. That is the math-before-code Discipline #1 failure mode.

The genre evidence and thematic framing were not wasted; they constrain *which kinds of levers* are appropriate (damage tax, skill-count cap, breadth ceiling, ailment-overlap, resistance hole, etc.). But choosing *which* lever and at *what* magnitude required a back-of-envelope on the engine's empirical response curve, and I did not do that math. The advisory should have been at least 30% shorter on genre survey and 30% longer on engine-math anchor.

This is the lesson. The dispatch is right that it is durable regardless of verdict.

---

## § 2 — Sub-Q 2: Option B compatibility with chromatic_mage design intent

This section evaluates Matt's selected Option B (α=0.08-0.09 + skill-count 12→10) against the chromatic_mage design intent established in the D11 advisory.

### § 2.1 — What chromatic_mage was supposed to be

Per advisory § 3.4 and § 5.5, the chromatic_mage post-reshape feels like: *a deliberate integrator; access to many elements; each one a choice; pays for the choice in raw output; wins through coverage, positioning, and right-tool-at-right-time, not raw output.* This is the PoE Elementalist / LE Runemaster / D4 Sorcerer mid-band feel — *mid-tier in raw output, high-tier in versatility, mechanically distinct, thematically beloved, not the leaderboard-top archetype.*

The kit shape that produces this feel (per advisory § 4.2 and § 6.5):
- 2-3 elements (3 is the ceiling for general play; 2 is the comfortable hybrid)
- 12-skill kit (per D10's already-tightened ceiling) — broader than non-hybrid (typically 10-11 skills under D10 constraints)
- One primary attack, multiple area/burst skills covering each element, a defensive or two, a mobility, a utility
- A small damage tax (~7%) that reads as "you pay for breadth at the moment of use"

The thematic claim was that *the breadth was the identity*: the player has many tools, slightly weaker each, but the *aggregate kit's coverage* gives them what a specialist cannot have.

### § 2.2 — What Option B does to that intent

**Element-breadth: 3 (unchanged from D11).** This part is fine; the 3-element ceiling preserves the breadth-as-identity claim. The 2-element comfortable hybrid is still possible (and shows as tax-free in the salvage data — 2 of 17 instances).

**Damage tax: α=0.08-0.09 instead of 0.07.** This is a marginal change at the *feel* level (8-9% instead of 7%). Not meaningfully different in player perception; the tax is invisible to the player anyway (they see the modifier-resolved damage values, not the tax math). Compatibility verdict on this lever alone: **fine, neutral.**

**Skill-count ceiling: 12 → 10.** This is the load-bearing change for chromatic_mage identity. Let me work through it carefully.

A 12-skill chromatic_mage kit at 3 elements averages 4 skills per element. That comfortably covers: primary attack (in one element), 2 burst damage (in two elements), 2 area damage (covering the third element + a second slot for the dominant), 1 DoT, 1 defensive, 1 mobility, 1 utility, 1 secondary defensive, 2 floating slots that vary by template = 12. Each element has 3-4 mechanically present skills. The player experience is "I have a fire option, a water option, and a wind option for most situations."

A 10-skill chromatic_mage kit at 3 elements averages 3.3 skills per element. Removing 2 slots typically means: one element drops from 4 skills to 3 (still functional), another element drops from 4 to 3, and one of the non-damage slots (utility or secondary defensive) is cut. The kit now has: primary attack, 1 burst, 2 area, 1 DoT, 1 defensive, 1 mobility, 1 utility, 1 floating = 10 minimum-satisfying. Each element has 3 mechanically present skills, *just barely* clearing the "this element is recognizably present" threshold.

**The compatibility problem:** at 10 skills with 3 elements, the chromatic_mage's *coverage advantage* — the thing the breadth-tax is paying for — shrinks materially. The "I have a fire option for fire-resistant monsters" claim is held by 3 fire skills (one of which is the primary attack, which is fixed-element); the chromatic flexibility narrows. The kit reads less like *deliberate-integrator with many tools, each weaker* and more like *specialist-adjacent with one bonus element*.

This is **not a small compatibility hit.** The whole design intent of chromatic_mage's tax is the trade: *raw power reduced; coverage breadth retained.* If skill-count is cut to the point that coverage breadth also reduces, the trade is no longer favorable on either axis. The player is paying tax for breadth they don't fully have.

### § 2.3 — Does PoE Elementalist / LE Runemaster / D4 Sorcerer combine damage tax AND skill-count restriction?

This is the genre-anchor check the dispatch asks for. Walking through:

**PoE Elementalist:** does *not* restrict skill-count. The skill bar holds the same 5-8 active gems any class can equip. The taxes are at the passive-tree, gear-socket, resistance-cap, and ailment-overlap layers — all *power-investment* taxes, not *capacity* taxes. The Elementalist is structurally permitted as many skills as any other build; the cost is in what each skill can do.

**LE Runemaster:** does *not* restrict skill-count. The 5-skill bar is the standard LE limit; Runemaster gets the same. The Runic Invocation mechanic is a *separate* combat-tool (not subtracted from the skill bar). The taxes are cooldown-management on Invocations + mastery-point opportunity cost + per-skill-tree depth. Again, *power-investment* taxes, not *capacity* taxes.

**D4 Sorcerer:** does *not* restrict skill-count. The 6-skill bar applies to all classes; Sorcerer gets the same. The taxes are tree-point opportunity cost + enchantment-slot opportunity cost + legendary-aspect synergy. *Power-investment* again.

**D2 Sorceress:** does *not* restrict skill-count. Three trees, full access to all skills (110 total tree skills across all classes). The tax is the synergy-point opportunity cost (you can't max-out skills across multiple trees because skill points are limited).

**Grim Dawn dual-mastery hybrids:** do *not* restrict skill-count. Both masteries' skill trees are fully accessible; shared skill-point pool is the only tax.

**Diablo Immortal Sorcerer:** *does* restrict skill-count (4 active + 1 ultimate). Immortal is the *exception* in genre. And critically, Immortal does *not* combine its skill-count cap with a damage tax for breadth — the 4-skill cap *is* the breadth-tax (because spreading across 4 elements gives 1 skill per element with no synergy).

**Conclusion:** No canonical multi-element ARPG combines damage-output tax AND skill-count restriction as a composite breadth-tax. The genre pattern is to use *one* lever: either capacity (Immortal's 4-skill cap) or power-investment (everyone else). Combining both is a genre novelty, and the novelty is in the direction of *more punitive than canonical*.

**Implication for chromatic_mage:** Option B's dual lever (damage tax + skill-count cut) puts Reincarnated's chromatic_mage in a more-taxed configuration than *any* multi-element archetype in the surveyed genre. This crosses from "comfortable mid-tier" into "structurally constrained — the player should not expect to play this archetype for the joy of breadth, because breadth has been substantially clipped."

This is not what I designed chromatic_mage to be.

### § 2.4 — The dual-ceiling compounding problem

Beyond the genre-novelty concern, there's a mechanical compounding issue with Option B. The original D11 advisory had two ceilings:

1. **Element-breadth ceiling 4 → 3** (caps how many elements)
2. **Damage tax at α=0.07 on n_elements > 2** (taxes the breadth that remains)

Together those produced a "comfortable hybrid" at 2-3 elements with a 0-7% tax. Net player-perceived constraint: mild.

Option B stacks a third ceiling on top:

3. **Skill-count ceiling 12 → 10** (caps how many skills)

The compounding effect at 3 elements:
- 3.3 skills per element (vs 4 under D11.0)
- Each skill 8-9% weaker than baseline (vs 7% under D11.0)
- Net coverage flexibility: ~17% reduced kit capacity × ~9% reduced per-skill damage = ~24% combined effective output reduction at the kit-aggregate level

This is *in the territory of the D2 specialist-vs-split differential* (~40-50%) that my advisory explicitly cited as the *upper bound of "too punitive for an intended-playable archetype."* Option B is not yet at that upper bound, but it is materially closer to it than the 7-28% range the advisory targeted.

More important than the magnitude: the player experience of "I am paying tax for breadth I don't have" is qualitatively wrong. The whole design pitch was *pay for breadth; receive breadth*. Option B charges the tax while shrinking the breadth being paid for.

### § 2.5 — Compatibility verdict on Option B

**INCOMPATIBLE with the chromatic_mage design intent as authored in the D11 advisory.**

Specifically:
- The skill-count cut (12→10) shrinks the breadth that the damage tax is paying for, breaking the design trade
- The dual-ceiling stacking pushes Reincarnated's chromatic_mage to a more-taxed configuration than any canonical genre exemplar
- The damage-tax escalation (0.07→0.08-0.09) is too marginal to fix the actual problem (floor-pin asymptote — see § 1.2 Defect 2) but is enough to compound the kit-shrink

Option B will likely *still miss the convergence target* — because the underlying problem is structural DPS density at the kit level, not damage per skill, and a 2-skill cut + 2% tax escalation is unlikely to drive the floor-pinned conv_wr below 0.50. Per § 1.2 Defect 2's analysis, the floor-pinned kits need conv_wr to drop *below 0.50* before the balance loop can find an interior modifier. The current state is 0.56-0.84 at floor. A 16.7% skill-count cut might drop the kit's WR at floor by ~10-15% in the best case (skills don't reduce WR linearly either — removing the weakest 2 skills costs ~10%; removing 2 from the middle costs ~15%; removing 2 from the top costs ~20%). Combined with the 1-2% additional tax: estimated final WR at floor ~0.45-0.75. That spread is *too wide* — some kits will converge, some won't, and the convergence rate will probably land at 40-60% rather than the ≥70% target.

In other words: Option B might bring convergence from 6% to 50%, but it will not reliably land it at ≥70%, and it will do so by partially gutting the archetype's identity. That is a bad trade.

### § 2.6 — Why I am exercising the veto

The dispatch grants me veto authority precisely for this situation: a proposed sprint that risks compounding the original projection error while damaging design coherence. Option B compounds in two directions:

1. It does not fix the math-before-code failure (Option B's α=0.08-0.09 is still anchored against my flawed projection; nobody has run the 3-point alpha smoke that would calibrate empirically)
2. It damages the design coherence of the archetype I was asked to shape

A STOP here protects against another "implement → miss → recalibrate" cycle. The alternative (§ 5) addresses both: empirical-calibration discipline first, then a structural lever that operates on the actual failure mode.

---

## § 3 — Sub-Q 3: chromatic_mage rename timing

My D11 advisory parked the rename question for Matt (advisory § 7.1). The dispatch asks whether to do (a) rename FIRST, then tune; (b) tune NOW, rename LATER; (c) don't rename.

**Recommendation: (b) tune NOW, rename LATER.**

Reasoning:

1. **The rename is a *cleanup* deliverable, not a *prerequisite* one.** The mechanical work in D11.x (Option C or whatever lands) is independent of nomenclature. Renaming first would force the gamora math note + rocket implementation + jack-ryan gate-1 + telemetry schema to all carry the new name through a cycle that may still need iteration. If D11.x lands cleanly under the chromatic_mage name and then needs adjustment, we have two paragraphs of "the chromatic_mage previously known as hybrid_mage…" littered across the records. Cleaner to land mechanical convergence first, then rename when the dust settles.

2. **The current sprint is in a STOP state pending diagnostic + alternative.** Adding rename scope to a sprint that needs to be re-shaped is the wrong time. Once D11.1 (or whatever replaces it) ships and the archetype lands at >50% convergence with the design intent intact, *then* the rename pass is a clean 2-3 hour rocket+star-lord+drax task with no design risk.

3. **Strategically, the rename signals "we believe this archetype works now."** Doing it while we're in the middle of a sprint that's failing to land sends the opposite signal. Land first; rename when we've earned the new name.

4. **A small concession:** the *gandalf-side language* can shift now. I will use "chromatic_mage" in design docs going forward (this post-mortem already does in §§ 1-2). The engine-side identifier stays `hybrid_mage` until the rename pass is scheduled. This is a low-cost split — design docs read with the cleaner vocabulary; implementation code is unchanged.

If Matt prefers option (a) (rename first), I can support it — but I'd want it sequenced as a separate small pass *after* the D11.1 successor lands, not bundled. If Matt prefers option (c) (don't rename ever), I'd want to revisit when chromatic_mage stabilizes; the name "hybrid_mage" is generic enough that it doesn't actively obstruct, but it doesn't capture what the archetype is doing thematically either.

---

## § 4 — Live-data finding: persistence discrepancy

While inspecting season_002012/class_0012 (Cartographer of Erased Borders — my original Class C anchor; same instance referenced in the v1.5 convergence analysis), I found that the D11 salvage's output state on disk does not match rocket's completion-record assertions. This is a non-trivial finding that bears on the verdict.

**What rocket's completion record asserts:**
- "schema_version=v1.8 on manifest.json (WARN-2 compliant: manifest only, not per-class)" — confirmed; manifest has it
- "d11_post_process=True + element_coverage_tax_multiplier fields on all hybrid_mage class objects" — **not present in the class JSON I read**

**What I found in `season_002012/classes/class_0012.json`:**
- Top-level keys: `archetype_tag`, `balance_metadata`, `class_role_function`, `color_palette`, `convergence_report`, `dominant_element`, ... , `post_process_d10`, ... , `skills`, ...
- `post_process_d10: true` is present (D10 post-process flag)
- **No `d11_post_process` field, no `post_process_d11` field, no `element_coverage_tax_multiplier` field**
- Skills (11 total — note: not 12; D10 ceiling already pruned to 11): all show `damage_multiplier = 1.000`
- Elements: `['fire', 'water', 'wind']` — confirms the 4→3 ceiling enforcement (originally fire/water/wind/physical; physical was dropped by D11's ceiling pruning)
- `balance_metadata.convergence_winrate: 0.7666...` at `final_modifier: 0.0509...` — confirms the floor-pin

The manifest does have `post_process_d11: True`, so the salvage *ran*. But the per-class persistence appears to have either:
- (a) Persisted only the balance_metadata (with the post-tax convergence outcome) but not the taxed skill values
- (b) Persisted the taxed skill values to a different output path I didn't search
- (c) Used a separate object in memory for the balance loop without writing back to the class JSON

This matters because:

1. **Math note § 3.2 explicitly chose Site A (kit finalization) over Site B (balance-loop modifier) on the grounds that "the export path writes `damage_multiplier` per skill to the season JSON. Post-D11, the exported `damage_multiplier` values reflect the tax-applied values (Site A)."** That claim is empirically not in the data I read. If the tax is applied transiently in the balance loop but the persisted skill values are pre-tax, then *the player surface (demo, loadout) will render pre-tax damage values*, contradicting the math note's Site A rationale.

2. **The 6% convergence result might be conflated with a persistence bug.** If the salvage ran the balance loop on a taxed in-memory kit but wrote back the pre-tax kit, then the next iteration of the balance loop (if there is one) would run on the pre-tax kit again. Likewise, any downstream re-validation would see pre-tax kits. The 6% convergence number might be measuring something slightly different than "tax applied to persisted skills converges 6% of the time."

3. **Discipline #11 (empirical inspection over assumption) directly applies.** I should not endorse, amend, or stop D11.1 based on a convergence number whose underlying persistence behavior is unclear. Before any D11.x sprint fires, the persistence discrepancy needs to be diagnosed and reconciled.

**Possible reconciliations:**
- (i) The class object schema places D11 fields somewhere other than top-level — perhaps inside `balance_metadata.modifier_flag` or a nested `provenance` dict. I checked `balance_metadata` and saw no D11-specific fields there. Could be elsewhere; rocket would know.
- (ii) Rocket's salvage script writes the D11 fields to a separate output (e.g., the `d11_salvage_summary.json` I read), and the per-class JSONs were never expected to be updated. If so, math note § 3.2's Site A claim is structurally wrong as implemented, and either (a) the math note's Site A justification needs revisiting, or (b) the implementation needs a follow-on pass to actually write the D11 state to per-class JSONs.
- (iii) Schema v1.8's per-class fields are documented somewhere I haven't read. Worth checking before any D11.x.

**This is not a blame finding.** Rocket implemented to the math note; the math note specified Site A; the persistence path's actual write-back may have a layered routing decision that didn't fully execute the math note's intent. The right response is *diagnose, not blame.* Knight-rider can route this to rocket as a Discipline-#11 diagnostic before D11.1 fires.

---

## § 5 — Alternative recommendation: Option C with empirical-calibration gate

If Matt accepts the STOP, the alternative path is structured to:
1. Fix the math-before-code projection failure (Defect 3 — empirical-calibration POC)
2. Apply the right kind of lever for the actual failure mode (structural DPS density, not damage scalar)
3. Preserve chromatic_mage design intent (breadth-with-cost; coverage-not-output)
4. Diagnose the persistence discrepancy (§ 4) before iterating

**Recommended shape: Option C-prime — skill-count ceiling reduction with empirical-calibration gate.**

### § 5.1 — The lever

**Primary lever: hybrid_mage skill-count ceiling 12 → 10 (likely; possibly 9 if the 10 smoke shows insufficient).** This is the structural DPS-density lever. It operates at the *kit-aggregate* level, which is where the empirical failure mode lives. Per § 1.2 Defect 2, kits floor-pinning at conv_wr=0.6-0.8 need their *uncapped* DPS density reduced; cutting 2-3 skills from a 12-skill kit removes ~17-25% of the kit's outbound-damage surface area, which is the magnitude order required to bring floor-WR below target.

**Secondary lever: damage tax remains at α=0.07 (or possibly reduced to α=0.05) as identity-flavor.** The tax is no longer the load-bearing balance lever; it is the *thematic differentiator* — the substrate-commitment-cost framing from advisory § 5.5 still applies. The 5-7% tax at 3 elements is read by the player as "breadth has a small cost"; the structural balance is held by the skill-count.

**Element-breadth ceiling: stays at 3 (unchanged from D11.0).** This is the breadth-shape lever; it's working correctly.

### § 5.2 — The empirical-calibration gate

Before rocket runs a full D11.1 salvage, the gate is:

1. **Run a 3-point skill-count smoke on 5 representative hybrid_mage classes from the 002011-015 pool.** Test ceilings of 10, 9, and 8. Measure: convergence rate, conv_wr at converged modifier (interior, not floor), kit-coverage assessment (how many elements have ≥2 mechanically present skills).
2. **Identify the ceiling that converges ≥4 of 5 smoke classes at interior modifiers with conv_wr near 0.50.** Likely 10 or 9; 8 may over-correct.
3. **Run a 3-point alpha smoke at the selected ceiling on the same 5 classes.** Test α=0.00, α=0.05, α=0.07. The structural balance should be carried by skill-count; α is the differentiator.
4. **Surface results to me + Matt** before full salvage fires.

Total smoke time: ~10-15 minutes. Diagnostic value: substantial. Math-before-code Discipline #1 + smoke-test Discipline #2 + empirical-inspection Discipline #11 all satisfied.

### § 5.3 — Why this is compatible with chromatic_mage design intent

The skill-count reduction is the *one* of the canonical genre levers that fits Reincarnated structurally. Genre evidence (per § 2.3 above):

- **Immortal Sorcerer at 4-skill cap:** the canonical "capacity is the breadth-tax" archetype. Multi-element is permitted but spreading across 4 elements yields 1 skill per element with no synergy lock-in. The Immortal Sorcerer is *the* genre exemplar of "skill-count alone gates breadth."
- The other multi-element exemplars (PoE Elementalist, LE Runemaster, D4 Sorcerer, D2 Sorceress) all use power-investment taxes, which Reincarnated doesn't have a clean analog for (no passive trees, no gear sockets at the right granularity, no per-skill investment).

The PoE/LE/D4 lineage I anchored chromatic_mage to in the advisory uses *power-investment* taxes. Reincarnated cannot replicate those cleanly. The damage tax was my attempt to express the same net effect at the effective-damage layer. **The empirical evidence is that the damage tax does not produce the same net effect** — because the engine's balance loop has a sharp asymptote at the modifier floor that the genre exemplars don't have.

Skill-count is the *one* canonical lever Reincarnated can directly apply. It maps cleanly to Immortal (a respected genre exemplar). The chromatic_mage at 10 skills, 3 elements, 7% tax reads as: *Immortal-style capacity-constrained hybrid, with a small flavor tax to express substrate-commitment cost.* That is a coherent identity in genre terms.

At 10 skills with 3 elements (3-4 skills per element), the coverage breadth is preserved enough to be the archetype's identity. The compounding problem of Option B (10 skills + 8-9% tax = identity-shrinking compound) is not present at 10 skills + 7% (or 0%) tax, because the dual ceiling stacking happens at the *tax* level only when the tax is materially affecting the kit's effective output. At α=0.07 the tax is design-flavor, not balance-load-bearing; at α=0.05 it's even more clearly flavor.

### § 5.4 — Why not Option D (full redesign), E (different magnitude composite), F (further identity reshape), or G (ship at 6%)

Brief justifications:

- **Option D (D11.2 full redesign):** the 1-2 day timeline is wasteful when the structural lever is already named and just needs empirical calibration. The redesign would mostly re-derive what § 5.1-5.3 already says.
- **Option E (different composite magnitude, e.g., α=0.15 + skill-count 12→11):** less aggressive on skill-count, more aggressive on tax. Same compounding problem as Option B in milder form; same wrong primary-lever choice.
- **Option F (further identity reshape — chromatic_mage becomes a smaller kit by design, e.g., 8 skills + 2 elements):** this is *retiring chromatic_mage* by another name. 8 skills + 2 elements is structurally indistinguishable from a generic 2-element specialist. Loses the form-library narrative apex (advisory § 5.2) and the canonical-7 thematic framing (advisory § 5.1). Strongly reject.
- **Option G (accept 6% + ship):** the dispatch's framing is interesting ("if chromatic_mage feels right in playtest, the WR-band miss may be acceptable"). The problem: floor-pinned classes do not just "feel a bit weaker" — they enter combat where every encounter is decided by the level-scaling stat baseline rather than the kit's specific design. The kit's identity is *invisible* in floor-pinned play because the balance loop has forced its damage to a minimum. The player would not feel "I'm playing chromatic_mage with a 7% breadth tax"; they would feel "this class deals weirdly low damage and combats are slow." Reject for player-experience reasons.

Option C-prime (§ 5.1) is the cleanest path. The smoke gate (§ 5.2) protects against repeating the projection failure.

### § 5.5 — If Matt wants to keep some tax (preserve substrate-commitment framing)

The substrate-commitment framing in advisory § 5.1 + § 5.5 is the thematic argument for *some* damage tax existing. The argument: each substrate's full power is its commitment fully expressed; a hybrid form holds multiple commitments without fully expressing any one; the tax is the substrate community's honest response.

This thematic argument is *real* and worth preserving — but the load-bearing balance work does not need to do it. The tax can remain at α=0.05 (3 elements = ~5% damage reduction) as a *thematic differentiator* while skill-count carries the balance. At 5% the player perceives almost nothing mechanically; the loadout-panel tooltip can carry the substrate-commitment language ("integrating multiple substrates: each commitment beyond the first costs ~5% raw power") without the tax mattering for convergence.

This is the cleanest reconciliation: structural balance via skill-count; thematic identity via small tax; coverage breadth preserved at 3 elements.

---

## § 6 — Open questions for Matt

These are decisions I cannot make unilaterally. Each is small but real.

### § 6.1 — Q1: Accept the STOP and the Option C-prime alternative?

Specifically: do you accept (a) the veto on Option B; (b) skill-count ceiling reduction as primary lever; (c) damage tax demoted to thematic-flavor at α=0.05 or kept at α=0.07; (d) empirical-calibration smoke gate before D11.1 fires?

If yes: knight-rider re-fires gamora with a new math note brief based on § 5; rocket implements; jack-ryan gates; we run the smoke; if the smoke lands, we full-salvage; if not, we iterate at the smoke layer (no full-salvage cycle wasted).

If no (you want Option B anyway): I am on record opposing; recommend at minimum the empirical-calibration smoke gate before the full salvage. Even Option B benefits from a 3-point smoke before committing to a 5-minute full salvage.

### § 6.2 — Q2: Persistence discrepancy diagnostic — who and when?

Per § 4: the on-disk class JSONs don't appear to have the D11 fields rocket's completion record asserts. Either I'm reading the wrong file or there's a persistence routing issue. Before D11.1 fires (whatever it is), this should be diagnosed.

Recommendation: knight-rider routes a small diagnostic dispatch to rocket — "inspect post-salvage class_0012 from 002012; confirm D11 fields are persisted to per-class JSON or to a different output path; reconcile with math note § 3.2 Site A claim." ~30 minutes of rocket time.

If the persistence is fine and I read the wrong field, no harm done — clarifies for future inspection.
If the persistence is broken, rocket fixes before any D11.1 work.

### § 6.3 — Q3: Rename timing locked as (b) tune NOW, rename LATER?

Per § 3, I recommend (b). Confirm? If yes, design docs (this post-mortem, future advisories) will use "chromatic_mage"; engine-side stays `hybrid_mage` until a post-D11.x clean rename pass.

If you prefer (a) rename FIRST or (c) don't rename, surface and I align.

### § 6.4 — Q4: New engineering discipline — empirical-calibration-before-full-salvage?

Per § 1.2 Defect 3 + § 8 below, I want to propose a new discipline: "Before any full-regen or full-salvage with a new lever, run a 3-point parametric sweep on a small sample to map the lever's actual response curve." This would have caught D11.0's projection failure in ~2 minutes of additional sim time.

Confirm? If yes, jack-ryan adds to `engineering-disciplines.md` as Discipline #14 (or appropriate number); future math notes and dispatches reference it.

If no, I'll continue to surface case-by-case in advisories.

---

## § 7 — Handoffs

### § 7.1 — HANDOFF → knight-rider (auto-fire control)

**HALT gamora D11.1 math note. STOP D11.1 sprint.** Do not auto-fire on this post-mortem's completion record.

**Re-surface to Matt with this post-mortem's verdict.** Specifically: (a) STOP verdict + Option C-prime alternative; (b) persistence diagnostic recommended; (c) rename timing recommendation; (d) discipline #14 proposal.

**Once Matt confirms:** if STOP + Option C-prime: fire new gamora dispatch with brief based on § 5; sequence persistence diagnostic in parallel; jack-ryan gate-1 on the new math note. If Matt overrides and selects Option B anyway: fire gamora D11.1 with my dissent on record and at minimum require the empirical-calibration smoke gate from § 5.2.

### § 7.2 — HANDOFF → gamora (conditional)

If Matt confirms STOP + Option C-prime: you will receive a new dispatch with a brief derived from § 5 of this post-mortem. The math note will cover:
- Skill-count ceiling 12 → 9-10 as primary lever (calibrate via smoke)
- Damage tax demoted to α=0.05 or α=0.00 (preserving thematic framing per § 5.5)
- Element-breadth ceiling unchanged at 3
- Empirical-calibration smoke gate (§ 5.2) before any full salvage
- Persistence discrepancy diagnostic incorporated (with rocket's diagnostic results as input)

No work for you to start until Matt confirms and knight-rider fires.

### § 7.3 — HANDOFF → jack-ryan (gate readiness; standby)

Standby. If Matt confirms STOP, you'll have a new gamora math note to gate-1 review (same pattern as D11.0). If Matt overrides, you'll have an Option B math note to gate-1 review with my dissent attached for your synthesis.

Also: please consider whether to formalize Discipline #14 (empirical-calibration-before-full-salvage) per § 6.4 — your decision on the engineering-disciplines.md addition.

### § 7.4 — HANDOFF → rocket (conditional; persistence diagnostic)

If Matt accepts the persistence diagnostic recommendation (§ 6.2): you'll receive a small dispatch from knight-rider — inspect post-salvage class_0012 from 002012; reconcile on-disk fields vs your completion-record assertions vs math note § 3.2 Site A claim. ~30 minutes; non-blocking on other work.

No other rocket action until D11.1 is determined.

### § 7.5 — HANDOFF → drax (no action)

Drax-demo + drax-loadout: no D11 action. Your current state (002011-015 D10-curated with D11 floor-pinned hybrid_mages running through them) is the same regardless of D11.1 verdict. Hold the data refresh until D11.1 actually lands at >50% convergence. Continue with v1.12.0.1 audio hotfix and other in-flight work (parallel-safe per dispatch coordination).

### § 7.6 — HANDOFF → star-lord (no action)

MIGRATION.md v1.10 entry is unchanged regardless of D11.1 shape. The three new `ClassBalanceResult` fields are still the right contract; you can implement the telemetry columns whenever convenient. Non-blocking.

---

## § 8 — Engineering-discipline cross-references

### § 8.1 — Discipline #1 (math-before-code)

**Direct violation acknowledged** per § 1. The D11 advisory recommended α=0.07 by analogy to D2 Sorceress synergy mathematics, without computing the empirical floor-pin escape velocity for the v1.5 Class C sample. The right discipline practice would have been: compute (even roughly) the damage reduction required to drop conv_wr from 0.77 to below 0.50 at the modifier floor, BEFORE recommending an α magnitude. The advisory's genre survey (§ 2) was rich and durable; the magnitude assignment was undisciplined.

Lesson for future advisories: when a lever's magnitude needs to land a quantifiable balance-loop outcome, the magnitude must be anchored against the empirical data the loop will face, not against genre-comparative analogies. Genre evidence constrains lever *type*; engine empirics constrain lever *magnitude*.

### § 8.2 — Discipline #2 (smoke-test vs full-regen)

**Adjacent violation in the implementation chain.** Rocket's D11 smoke (per math note § 9.2) tested the implementation correctness — that the tax function ran, that 2-element kits got tax=1.0, that 3-element kits got tax=0.93, that the assertion failures didn't trip. The smoke did *not* test whether α=0.07 actually moved the convergence outcome. The math note's smoke acceptance criteria § 9.2 includes "hybrid_mage convergence: target is `converged=True` with `final_modifier` > `MODIFIER_FLOOR + FLOOR_EPSILON (0.055)`. If still floor-pinned, flag α for recalibration." Rocket flagged correctly — the smoke surfaced the floor-pin and rocket escalated. But the *math-magnitude* validation (the 3-point alpha smoke I propose as Discipline #14) was not part of the math note's gate.

The smoke-test discipline as practiced is functioning at the implementation-correctness layer but not at the math-magnitude layer. Discipline #14 (§ 8.4 below) extends the smoke discipline to the math-magnitude layer.

### § 8.3 — Discipline #11 (empirical inspection over assumption)

**Active during this post-mortem.** Per § 4: I inspected on-disk class_0012.json directly and found a discrepancy with rocket's completion-record assertions. This is exactly the discipline working as designed — *inspect the actual data; don't assume the upstream report fully captures the state*. The persistence diagnostic recommended in § 6.2 is a Discipline #11 follow-on for rocket.

This discipline saved this post-mortem from endorsing or rejecting Option B based on a possibly-conflated convergence metric. Worth flagging as a positive case study for the discipline.

### § 8.4 — Proposed new Discipline #14: empirical-calibration-before-full-salvage

**Proposed text (for jack-ryan's consideration in engineering-disciplines.md):**

> **Discipline #14 — Empirical-calibration before full-regen / full-salvage with a new lever.**
>
> When a math note specifies a new tuning lever with an empirically-derivable magnitude (e.g., a coefficient α, a ceiling, a threshold), the implementation gate before any full-regen or full-salvage operation must include a *parametric sweep smoke* — minimum 3 magnitude points on minimum 3-5 representative classes from the affected pool — measuring the lever's *actual response curve* (not just implementation correctness).
>
> The sweep's purpose: confirm the lever produces the projected magnitude of effect on the target metric. If the response curve shows the lever is in the wrong magnitude range (too gentle, too harsh, or flat), surface to the design steward and math-note author BEFORE the full operation runs. Do not full-regen / full-salvage in the hope that the lever's magnitude lands.
>
> Wall-time cost: typically 1-3 minutes per parametric sweep (vs 5-30+ minutes for a full operation). The discipline pays for itself in one prevented mismatched-magnitude full-regen.
>
> Pairs with Discipline #1 (math-before-code) and Discipline #2 (smoke-test) — the parametric sweep is the *magnitude-validation* extension of the smoke-test discipline.

The D11.0 cycle is the case study that motivates this discipline. A 2-3 minute alpha sweep before the 5-minute full salvage would have caught the magnitude mismatch in real-time, surfaced to me + Matt, and either led to (a) re-tuning α before the full salvage ran or (b) a direct STOP-and-re-evaluate decision with full empirical evidence rather than after-the-fact reasoning.

### § 8.5 — Discipline #13 (implicit-pillar drift)

**Adjacent finding from § 4.** The math note's Site A claim ("damage_multiplier values reflect the tax-applied values; player-visible truth") may be empirically untrue if the persistence routing didn't write the tax-applied values to per-class JSONs. If so, there is an implicit-pillar drift between the math note's design claim ("player surface sees taxed values") and the engine's actual state ("player surface sees pre-tax values; tax exists only in transient balance-loop computation"). Discipline #13 (catching implicit-pillar drift before it ossifies) directly applies — the persistence diagnostic (§ 6.2) is also a Discipline #13 enforcement.

### § 8.6 — Discipline #12 (semantic shift)

The chromatic_mage rename is a semantic shift if/when it happens. § 3's recommendation (tune NOW, rename LATER) defers the semantic-shift discipline to a post-D11.x rename pass. When that pass fires, MIGRATION.md will need entries; telemetry tables will need column renames; design docs will need a search-and-replace. Standard Discipline #12 practice applies.

---

## § 9 — Closing

The D11 cycle taught the engine three things at once: (1) the lever I chose was the wrong primary tool for the actual failure mode; (2) the magnitude I assigned was anchored against a different system's empirical baseline; (3) the persistence path may have a discrepancy worth diagnosing. Option B as proposed compounds problem (1) with a partial fix and does not address (2) or (3). The STOP is to give us a clean reset where the alternative lever (skill-count ceiling, structural-DPS-density operative) is calibrated empirically before any full salvage runs.

The chromatic_mage design intent is unchanged: a deliberate integrator, mid-tier in output, high-tier in coverage flexibility, *recognizably* multi-element. The way we encode it mechanically needs to change — from damage tax (which the empirical evidence says doesn't work as the primary balance lever) to skill-count ceiling (which the genre evidence and the engine's empirical response curve both support).

The Court of Forms remembers the form. The reshape gives the form back to itself — through the right mechanism, this time.

---

*Authored 2026-05-17 by gandalf per Matt L3 explicit early-stop authority grant. STOP verdict on Option B; Option C-prime alternative with empirical-calibration gate proposed. Persistence discrepancy flagged for diagnostic. Discipline #14 proposed for jack-ryan's consideration. Knight-rider holds D11.1 auto-fire pending Matt confirmation.*
