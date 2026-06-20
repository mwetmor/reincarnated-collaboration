# gandalf RULING — instrument-validity G1 escalation (rocket reference-economy prerequisite)

**Type:** Pattern A-deep design ruling. KR-escalated G1 condition (a). gandalf rules the design; **Matt holds the scope authorization** (the rocket generation change is new scope on the workstream).
**Author:** gandalf, 2026-06-20.
**Parents:** `gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md` (§1, §3-G1, §3-G3, §6/§7); gamora math-note `reincarnated-engine/src/reincarnated/simulation/math/resource-economy-wiring-phase1-2026-06-20.md` §3/§4; gamora `AGENT_STATE.md` G1 surface; tag `gamora/v-resource-economy-phase1-1`.
**Verified first-hand (trust-but-verify):** `season_generation_pipeline.py:213-218` `_BC_TEMPO_TO_RESOURCE = {low:cooldown, mid:energy, high:mana, sustained:stamina}`; `:541-543` `_infer_resource_model`; `bc_target_source.py:105-189` (the energy_type→bc_target binning + the R-b restamp comment); `gear_generation.py:108-159` (gear-roll energy_type weights DO carry the full doc-48 vocabulary, but that path does not author the harness population's authoritative `energy_type`). gamora's three-vocabulary finding holds.

---

## TOP-LINE

**The rocket generation change is REQUIRED. There is no faithful read of the STR-lever question without it.** gamora's read is correct and I ratify it without softening: **the rage lever IS the rage economy.** Phase 6 measures STR's focus-fire answer by watching a Barbarian *build rage on the swarm and spend it on the anchor*. If no entity in the population carries `energy_type="rage"`, that behavior cannot occur, and Phase 6 measures the mana-default greedy-capstone shape wearing a Barbarian's name — which answers nothing about STR. Running Phase 6 on a mana-default-only population would not be a weaker read of the (A)-vs-(B) question; it would be a **null instrument reporting a confident number**, which is the exact contamination this entire workstream exists to kill (§0). I will not let the workstream's own terminal measurement reproduce the defect it was chartered to remove.

**But this does NOT stop Phases 1-4.** The diagnosis is precise: the kernel is correct, the sim wiring is correct, the gap is one un-checked seam (generation's authoritative `energy_type` assignment). The fix slots as a **new prerequisite phase before Phase 5**, runs in parallel with the offense chain, and the offense chain does real instrument-clearing work on the mana-default population in the meantime. Below, by your four questions.

---

## (1) Is the rocket generation change REQUIRED? — YES.

The brief's own §3 Phase-2 names it: *"rage → build on the swarm, spend on the anchor — this is STR's focus-fire LEVER, native to the economy."* The Diablo 3 parallel I drew there is exact and worth re-stating because it makes the dependency unavoidable: **Rend is a Fury-spender.** A Barbarian with no Fury bar does not "do less Rend" — Rend is *uncastable*. There is no Rend-without-Fury, the way there is no rage-spend-without-rage-pool. The lever and the economy are the same object. A faithful STR read therefore *requires* a rage entity in the population; the question "can we read STR without it" answers itself — without it there is no STR kit, only a mana kit mislabeled.

**The deeper finding (why this was invisible until now):** there are not two vocabularies in tension, there are **three**, and two of them were never connected:

| layer | vocabulary | role |
|---|---|---|
| kernel `_ENERGY_CONFIGS` | rage / combo / focus / stamina-as-resource / charge-stack (+mana-default) | **consuming** (the economy *machinery*) |
| doc-48 §3.1 | charge-stack(rage) / steady / combo / stealth / HP-economy / overflow / mana | **design intent** (which class gets which economy) |
| harness population `_BC_TEMPO_TO_RESOURCE` | cooldown / energy / mana / stamina | **substrate-measurement inference** (tempo→a resource *label*) |

The third vocabulary is a **measurement artifact masquerading as a design assignment.** `_BC_TEMPO_TO_RESOURCE` infers a resource *label from observed tempo* — it is a descriptive read of the BC substrate, not a prescriptive class-economy assignment. It was never meant to carry doc-48's design intent, and it doesn't. The doc-48 *intent* and the kernel *machinery* are both correct and both present; the **generation seam that should hand doc-48's intent to the kernel's machinery instead hands it a tempo-inferred label that collapses to mana-default.** That is the un-checked link. (This is a clean instance of the §4.4 semantic-layer discipline: the substrate's tempo-vote is binding at the *measurement* layer but must NOT be read as binding at the *design-economy* layer. Tempo→resource-label is geometry; class→economy is semantics. The seam read geometry where it needed semantics.)

---

## (2) Where does the rocket change slot? + what it does to Phase 2/5 sequencing.

**New phase. Call it Phase 4b (or "Phase R" — rocket reference-economy hardening). It slots PARALLEL to the offense chain (1-2-3) and to mitigation (Phase 4), and it is a HARD PREREQUISITE for Phase 5.** Revised spine:

```
  1 (resource wiring, DONE) → 2 (rotation) → 3 (DoT)        [offense, mana-default pop]
  4 (mitigation)                                            [‖, selector-independent]
  R (rocket: doc-48 economy → population)                  [‖, generation-seam]
        └──────────────┬──────────────┬─────────────┘
                       5 (ONE composed re-baseline)  ← waits on 1,2,3,4,AND R
                       6 (STR-lever read)            ← honest pop, honest bands
```

**Why before Phase 5, and why this is the load-bearing sequencing call:** Phase 5 is the **ONE refit** — the entire discipline of the workstream (§0, §5) is that the bands are re-fit exactly once, against the *composed* instrument. The doc-48 economies **materially move KPM**: a rage build-spend kit has a burst→lull rhythm (empty pool → build on swarm → dump on anchor) that is a *different KPM shape* from mana-default greedy-capstone (start-full → throttle-on-spam). If Phase 5 refits the bands on a mana-default-only population and THEN Phase R injects rage/combo/charge-stack, the bands are fit to the wrong instrument and a **second refit is forced** — which violates the ONE-refit discipline and silently re-contaminates the instrument. So Phase R is not "nice before Phase 6"; it is **mandatory before Phase 5**, because the composed instrument Phase 5 fits against is not complete until the population carries its real economies.

**Why NOT before Phase 2:** it doesn't need to be, and forcing it earlier serializes work that can run in parallel. See (3).

**What Phase 2 does to G3 on a mana-default population — important caveat:** with the population mana-default-only, Phase 2's selector has only ONE economy to branch on. So:
- **G3's economy-distinguishability falsifier is DEGENERATE pre-Phase-R** — you cannot show "rage/steady/combo/charge-stack fire visibly differently" when only mana exists in the population. KR must NOT auto-resolve G3 as PASS on a mana-default population; that would be a false PASS (the branch *looks* fine because only one path is exercised). **G3 RE-ARMS after Phase R** — when the population carries multiple economies, G3 fires for real.
- **The rage-lever falsifier within G3** (escalate-if "rage fails to produce build-on-swarm/spend-on-anchor") **also cannot fire pre-Phase-R** — no rage entity exists to falsify. It too re-arms after Phase R.

So I am **amending the gate schedule** (a clarification of my own brief, Discipline #12 honest-correction): **G3 is evaluated against the post-Phase-R population, not the Phase-2 mana-default delta.** Phase 2's mana-default delta is still measured and gated, but on a *narrower* G3 criterion: "does the selector now fire tiers above T1 on the mana-default economy" (the T1-collapse break, which is what Phase 2 must do to unblock Phase 3's DoT). The economy-distinguishability + rage-lever halves of G3 defer to a post-Phase-R evaluation. KR: treat G3 as **G3a (T1-collapse break, Phase 2, mana-default)** + **G3b (economy distinguishability + rage lever, post-Phase-R)**.

---

## (3) Should Phases 2/3/4 proceed NOW or wait on Phase R? — PROCEED NOW.

**Yes, all three proceed immediately; none waits on Phase R.** Here is the reasoning per phase, anchored on what each *measures* and whether mana-default-only confounds it:

- **Phase 2 (rotation) — PROCEED.** Its primary instrument-clearing job is breaking the T1-collapse (§1 defect #2: "only T1 ever fires; ¾ of every kit is decorative"). That defect exists *on the mana-default population* — fixing it so tiers above T1 fire is real, necessary work that is a hard prerequisite for Phase 3 (DoT only matters once the selector fires the non-zero-tick skills). Phase 2 also *builds the energy_type branch cleanly* so that when Phase R lands, the multi-economy selector falls out of it with **zero further sim work** (gamora already committed to this in the math-note §6). Proceeding now is strictly better: it clears defect #2 AND pre-builds the rails Phase R rides. Gate on G3a only (see above).
- **Phase 3 (DoT) — PROCEED (after Phase 2, per the existing dep chain).** Defect #3 (DoT inert + physical-DoT mis-scaled) is economy-independent — DoT ticks and attribute-routing are the same broken machinery regardless of which resource pays for the cast. Activating DoT on the mana-default population is faithful work; G4's physical≈caster symmetry read holds because both sides fire on the mana-default pop equally (no economy asymmetry confound). The ONE caution: STR *bleed contribution* in G4 will be measured on a mana-default Barbarian, not a rage Barbarian — so G4's STR-bleed number is **provisional** until Phase R. That is fine: G4's job is "is DoT non-zero and is physical≈caster symmetric," not "is STR's final bleed output correct" (that is Phase 6). Flag the G4 STR-bleed figure as pre-Phase-R provisional; do not read STR sufficiency from it (the §5 caution "no STR read before Phase 6" already covers this).
- **Phase 4 (mitigation) — PROCEED (already ‖ per the brief).** Wholly economy-independent (armor/resist is on the defense side of the equation; resource economy is on the offense-gating side). G5 holds unchanged. No interaction with Phase R.

**The net:** proceeding loses nothing and gains the parallel-track time. Phase R runs alongside; Phase 5 is the join point that waits for all of {1,2,3,4,R}. The only adjustment is the G3 re-arming above — and that is a *gate-schedule* change, not a *work-sequencing* change.

---

## (4) Recompose-first disposition for the rocket fix — PORT/ACTIVATE, not BUILD. (with one guard)

**This is recompose-first, and it clears the framing-audit (§4.1).** Apply the three questions:

- **Q1 (load-bearing framing assumptions):** that doc-48 §3.1 already specifies the per-class economy assignment, and that the kernel `_ENERGY_CONFIGS` already implements the consuming machinery for the 5 distinctive economies. **Both verified true** (doc-48 §3.1 carries all 10 Cycle-14 class assignments; kernel `combatant.py:374-385` holds the 5 configs). So the fix is: **map an existing spec onto an existing seam.** Neither the spec nor the machinery is invented.
- **Q2 (refutation evidence in scope):** could the fix secretly require inventing a mechanic? The one risk: if doc-48 assigns an economy the kernel does NOT implement, that economy would need building. gamora already checked condition (b) and confirmed the kernel does NOT implement damage-taken-converts (Skirmisher) or HP-economy (Crusader Channel-Aura) — **and those two stay DEFERRED** (G1 pre-ratified this; 2/10 classes, neither STR, neither blocks the STR read). For the 8/10 covered classes — including **both STR classes (Barbarian-rage, Hoplite-steady)** — every doc-48 economy maps to an existing kernel config. So no new mechanic is needed for the covered roster.
- **Q3 (refine framing rather than execute?):** No refinement needed; the framing holds. The fix is a mapping table, not a design problem.

**So the rocket fix is:** replace (or override) `_BC_TEMPO_TO_RESOURCE`'s tempo-inference with a **doc-48 per-archetype economy assignment** for the generated population, so that a Barbarian-archetype entity is authored with `energy_type="rage"` (which the now-wired kernel + sim already consume correctly). This is the *same recompose-first disposition* as the DoT-activation ruling and as Phase 1 itself: **the substrate designed this; it just doesn't function in the shipping regime; port/activate the existing intent.** No new economy mechanic enters the workstream. (This is precisely the brief's §3-G1 "revisit in a follow-on if cohesion-judge/playtest surfaces pressure" — the pressure surfaced *at the population level, before Phase 6*, which is the cheapest possible place to catch it.)

**The one guard I attach (rocket's math-note-first, Discipline #1):** rocket must confirm the doc-48→kernel-config mapping does not collide with the BC-substrate's own use of the tempo→resource inference *elsewhere in generation*. `_infer_resource_model` may feed bc_target binning (`bc_target_source.py` reads energy_type to set econ_bin/tempo_bin and the physical-override eng_bin). If the rocket change swaps the population's `energy_type` from tempo-inferred to doc-48-assigned, rocket must verify the **bc_target round-trip still holds** (the R-b restamp comment at `bc_target_source.py:123` is the anchor — the composer re-resolves cost_type from econ_bin; the adapter reconciles the chosen energy_type). This is the recompose-first integrity check: changing the economy assignment must not silently re-shape the bc_target geometry the rest of generation depends on. Rocket's math-note estimates this before wiring. **If the round-trip does NOT hold cleanly** (i.e., doc-48 economy assignment can't be threaded without re-shaping bc_target geometry) — THAT is a genuine scope-surprise that re-escalates to gandalf+Matt. My expectation is it holds (energy_type already flows through bc_target; we are changing the *source* of the value, not adding a new field), but rocket confirms empirically. This guard is why Phase R is rocket-owned with a math-note gate, not a trivial one-liner.

---

## (5) G1 mapping-integrity ruling: my pre-ratification HOLDS; the finding revises the SEAM-LOCATION assumption, not the mapping.

**My pre-ratified G1 table (doc-48 economy → kernel config) is correct and stands.** Every row maps as ratified; the 8/10 coverage including both STR classes is intact; the two DEFERRALS are correct. The mapping was never wrong.

**What the finding revises is an *implicit assumption beneath* the table, not the table itself:** the G1 table tacitly assumed the doc-48 economies were *already live on the generated population* — i.e., that "map doc-48 → kernel config" was a wiring job inside the sim seam. The finding shows the doc-48 economies **never reach the population at all**, because the generation seam authors `energy_type` from a *third* vocabulary (tempo-inference) that the G1 table didn't know existed. So:

- **The kernel is correct** (configs present and right).
- **The sim is correct** (Phase 1 wiring now consumes them faithfully — verified, tag `gamora/v-resource-economy-phase1-1`).
- **The generation seam is the gap** (it tags entities with tempo-inferred labels, not doc-48 economies).

This is an **honest-correction (Discipline #12)** to my brief, not a reversal: the G1 mapping ratification is sound; I add that the mapping has a **third seam in its delivery path (generation) that the table did not account for**, and that seam is the actual gap. The brief's §1 Phase-0 read confirmed "the kernel HAS the configs" and "the doc-48 assignments are the spec" — both true; what neither I nor the Phase-0 read checked was whether the *generated population carries the doc-48 assignment*, and it does not. gamora caught the un-checked link exactly where the framing-audit (§4.1 Q2) is designed to catch it: at dispatch consumption, before downstream (Phase 6) fired against the bad assumption. **This is a clean, in-scope catch — the discipline working as intended.** No blame; the seam was simply not in the table's sightline.

---

## What MATT must decide vs. what I have RULED

**I have RULED (gandalf design authority; KR auto-resolves these):**
- The rocket economy change is **design-required** — Phase 6 is null without it. (No faithful STR read exists on a mana-default population.)
- It slots as **Phase R, parallel to 1-4, hard-prerequisite to Phase 5** (the ONE-refit discipline forces it before the refit).
- **Phases 2/3/4 proceed NOW** — none waits on Phase R.
- **G3 splits into G3a (T1-collapse break, Phase 2, mana-default) + G3b (economy distinguishability + rage lever, post-Phase-R).** G4's STR-bleed figure is pre-Phase-R provisional.
- The rocket fix is **recompose-first (port doc-48 spec → generation seam; no new mechanic)**, with rocket's math-note bc_target-round-trip guard; the two DEFERRED economies stay deferred.
- My **G1 mapping ratification holds**; the finding revises the seam-location assumption, not the mapping.

**MATT must AUTHORIZE (scope authority — this is genuinely new scope on the workstream):**
- **The rocket generation-seam change itself** — a new phase (Phase R) was not in the original spine; adding rocket as a seam on this workstream is a scope expansion that needs Matt's go. (The *design necessity* is mine to rule; the *resourcing of a new seam-phase* is Matt's to authorize. This is the §3-G1 escalate-(a) split exactly: I rule the design; Matt holds the decision.)
- **Whether the two DEFERRED economies stay deferred for this workstream** — I recommend YES (they don't block the STR read, 2/10 roster, neither STR; revisit in a cohesion-judge/playtest follow-on). But if Matt wants the full 10/10 roster economy-faithful before Phase 5, that is a scope call only he makes — and it would mean the kernel must first BUILD damage-taken-converts + HP-economy (a real new-mechanic cost, NOT recompose-first), which is why I recommend against it for THIS workstream.

**One thing Matt does NOT need to re-decide:** the Phase-5 ONE-refit discipline. Phase R going before Phase 5 *preserves* that discipline (it ensures the single refit fits the complete instrument). If Matt declines Phase R, the honest consequence is **Phase 6 cannot run as an STR read** — it would measure a mana-default population and report a number about nothing. I would then rule Phase 6 HELD (not run) rather than let the workstream's terminal measurement reproduce the contamination it was built to remove. So the real fork for Matt is: **authorize Phase R, or accept that the STR-lever read is deferred until a separate economy-hardening effort lands.** There is no third path where Phase 6 runs honestly without the economies in the population.

---

**Signed:** gandalf, 2026-06-20. The kernel holds the economy; the sim now consumes it; the spec assigns it per class — but the generation seam hands the population a tempo-inferred label instead of the design economy, so the Barbarian reaches the arena with no rage bar. A Fury-spender with no Fury is not a weak Barbarian; it is not a Barbarian. Author the economy onto the population (recompose-first; port the doc-48 spec), slot it before the one refit, let the offense chain clear the instrument in parallel — then, and only then, ask whether STR's rage-spent bleed turns the anchor-gap from a wall into a choice.
