# Review — archetype-agnostic loot system (Matt mobile-draft, matt_notes_handoff_docs/reap-die-rise-agnostic-loot-system.md)

> **Trigger:** Matt request 2026-07-06 (post-HALT session, spike in flight): review the proposed loot-system spec.
> **Author:** gandalf (ELICITOR + DRIFT-CRITIC), 2026-07-06.
> **Verdict up top:** the operator model is RIGHT and the soul-as-lens fiction is the strongest gear fiction this project has produced — adopt the frame. Five collisions with ruled canon need reconciliation, three spec gaps need decisions before any build, and the build itself GATES ON batch-2 (population + caster fix) or the fairness band bakes today's 2.34× bias into every operator measurement.

---

## 1. What stands (adopt as-is)

- **§0/§1 operator model.** "Gear = operators over universal axes, not class-coupled stats" resolves the reincarnation-loot paradox correctly. §1.4's property — same item, different emergent behavior per body — is the real-loot criterion. Genre receipts: D3's build-changing legendaries and PoE's build-imposing uniques (Mjölner) prove transform-identity is the chase; D3's Legacy-of-Nightmares-era generic "+X% damage" proves value-only gear is a stat-skin. The doc's answer (operators act on STRUCTURE — slots, chains, triggers) is the correct one.
- **§3 soul-as-lens gleaning.** The item is fixed light; the soul is the lens — reincarnation makes you see MORE in the same object. This is the rare case where the mechanic IS the theme (*Reap. Die. Rise.*: the soul accretes across deaths; the world's objects don't change, your capacity to read them does). Nearest genre precedent: Last Epoch's Weaver's Will items (hidden potential awakening with use) — ours is stronger because the reveal is soul-indexed, not item-indexed. §3.3's guardrail (drops stay primary; gleaning is bonus) is the correct D3-loot-2.0 lesson.
- **§4 soul weapons.** Diegetically agnostic, not just mechanically — kills "why is my archer carrying a sword" at the fiction layer. Isekai receipt: the divine-armament-that-grows trope done with mechanical honesty.
- **§5.1 functional-compression naming.** Correct, and it composes with existing ruled discipline (see collision C5 for the hardening it needs).
- **§7 fairness-band validation via the gauntlet.** The same machinery that produced the C2 floor and today's HALT. §7.3's claim is true and is the architectural payoff of the whole decomposition bet.
- **§9's honesty.** "Gear was worn in sim but never cross-kit fairness-tested" matches the engine record (combatant carried_gear percent buffs + set bonuses exist; cross-kit banding does not).

## 2. Canon collisions (DRIFT-CRITIC — each needs explicit reconciliation)

| # | Collision | Detail | Disposition |
|---|---|---|---|
| C1 | **Axis-5 back-door (TODAY'S ruling)** | §1.2 lists "resource *type*" as a gear-operable axis. A "convert cost to HP" operator = blood magic by gear; charge-stack by gear likewise. The three structural cost-TYPE bins are **reserved, empty-by-ruling** (batch-2 spec §8 R1, Matt 2026-07-06) — different sim plumbing, three binding guards | Resource-type operators join the SAME reserved list; gear vocabulary = mana-substrate + live martial economies only, until the bins open (F5 re-derivation event). Cost/regen/pool operators stay legal |
| C2 | **The 64K number** | §1.1 "~64K-point decomposition" — retired THIS SESSION (no code derivation; BC survey note §2). Number of record: **68,040 full lattice / 12,960 live** | Fix in canonization; don't let the myth re-propagate |
| C3 | **Trait architecture (ruled 2026-05-12)** | Ruled: gear-affix trait rolls, element/mechanic-gated, rank-stacks, gear tier sets per-rank rate. "Mechanic-gated" affixes violate §1.2's universality rule; the doc doesn't mention traits at all | Fork for Matt: (a) retire traits-on-gear, operators replace; (b) traits-on-gear = value-operator subclass restricted to universal gates (element IS universal; mechanic-gates dropped); (c) dual system — **REJECT (c)** by the doc's own §0 argument (partial body/partial soul = worst of both). gandalf lean: **(b)** |
| C4 | **ω-penalty / weapon-substrate policy (2026-05-24)** | Soul weapon re-expresses to match the body → cross-attribute wielding may become impossible by construction → `OMEGA_CROSS_ATTRIBUTE_PENALTY` (0.80) loses its trigger. Also: today's finding — weapon sim fields are scaffold-0.0 "until rocket Track D wires substrate weapon binding." §4 CHANGES what Track D should wire: the weapon is an operator carrier, not a base-damage source | Soul-weapon spec and Track D must be designed together; ω-penalty disposition (retire vs re-key to soul-weapon affinity) = Matt ruling at canonization |
| C5 | **D7 AI-tell line** | §5.2 hedges "LLM (or a templating layer)" for realized descriptions. Realized descriptions are RULES TEXT — an LLM paraphrase of rules risks WRONG rules on a player-facing surface | Harden: **realized descriptions are COMPUTED (deterministic template render of operator state on current body); LLM touches the NAME only** (functional compression, D1 vocabulary-commonness lessons apply — "Hollowcost" yes, obscure-vocab no). Flavor sentence optional, clearly subordinate |

## 3. Spec gaps (ELICITOR — decisions the doc doesn't know it's missing)

**G1 — Composition algebra: the LOADOUT is the unit of play, not the operator.** §7 validates operators singly; players wear ~10 slots. Two transforms colliding ("cannot use primary" + "primary chains +1") = dead affix or degenerate combo — and the combinatorics forbid brute-forcing all ensembles. Needs: (i) composition rules by class (value ops commute/stack within band; structural ops slot-scoped; transforms slot-exclusive), (ii) **a transform-equip cap** (D3 Kanai's Cube caps at 3 legendary powers for exactly this reason; PoE governs support-gem interactions by design rule, not brute force), (iii) a loadout-level sanity sim on SAMPLED ensembles as a second validation ring. gandalf lean: cap simultaneous transforms at 2–3; value/structural free.

**G2 — Bundle-level validation.** §8 step 4 samples validated operators into items, but band-pass is per-operator and bundle power-delta ≠ sum of parts. Tractable split: marquee legendaries are FINITE authored points → gauntlet them as bundles directly; generated mass = few-op items → validate the pairwise composition table. Name this in the spec.

**G3 — THE persistence-scope question (biggest unflagged decision).** The doc establishes gear persists across BODIES within a descent (its premise). It never says whether gear persists across DESCENTS/runs. This decides everything about §3: if gear is lost per-run (death-faith frame — *death matters*), items don't live long enough to glean and soul-level thresholds are dead weight; if gear persists across runs, gear+gleaning is the meta-progression spine beside the form library (Earth meta-layer), and thresholds tune in hours not minutes. Interacts with §10's reincarnation-choice item and the gameplay-loop run model (§19/§23). **This is a Matt ruling that precedes any threshold math** → route to matt_decision_needed at canonization.

## 4. Merge §6 into §7 — one campaign, two statistics

§6 relevance ("does it change behavior meaningfully") and §7 fairness ("is the change in-band") are THE SAME SIM RUNS: relevance = |power-delta| above noise floor; coverage = fraction of kits above it; band-pass = the same delta distribution against the band. One gauntlet campaign emits both → halves the compute. And the compute is real: operators × kits × gauntlet is batch-scale — the ENTIRE staged-pilot discipline applies (representative operator sample first, pre-registered GO/HALT, then the full sweep). Also §6.2's "representative sample" already exists: it's the batch-2 population — don't invent a second sampling scheme.

**Convergence bonus (the machinery self-validates):** an "on-crit" trigger operator would FAIL today's coverage test — crit is DEX-keyed, INT kits are crit-poor by formula (today's finding §3). The agnostic search would have empirically caught the crit asymmetry. Conversely: on-crit hooks aren't universal until a spell-crit channel (F-c) or equivalent lands. The two workstreams are measuring the same substrate truth from two sides.

## 5. Sequencing (hard constraint)

**The loot BUILD gates on batch-2 close.** Reasons: (i) the fairness band needs the kit spectrum — INT cells and summoners included — which is exactly the population Leg C emits; (ii) measuring operators against the UNFIXED caster chassis bakes the 2.3384× bias into every band judgment (operators band-tested on broken casters mis-band permanently); (iii) provenance law — gear validation is downstream instrumentation; **kits vote BARE in the faction derivation; loot never contaminates the derivation population.**

**What proceeds NOW in parallel (design-only, spike-safe):** operator vocabulary freeze, composition algebra (G1), persistence ruling (G3), trait reconciliation (C3), soul-weapon/Track-D joint spec (C4), naming-constraint hardening (C5). All spec work, zero compute.

## 6. Implementation-cost honesty (for the eventual build spec)

The three operator classes map to three cost tiers, conveniently aligned with rarity: **value** = live today (ability_modifiers percent pools, set bonuses); **structural** = existing resolver geometry params (chain/fork/multi_projectile) exposed as overrides — moderate; **transform** = new rotation-constraint plumbing in ai_strategies — the expensive tier. Staging by rarity tier is natural and de-risks the build.

## 7. Disposition offer

gandalf authors the canonical spec (doc-17 gear lineage, my seam) absorbing this draft + the five reconciliations + the three gap-decisions, splitting story-side (soul weapons, gleaning fiction → `reap-die-rise-story/`) from engine-side (operator algebra, validation pipeline → `reap-die-rise-engine/`), with C3/C4/G1/G3 + fairness-band widths routed to `matt_decision_needed/`. Timing: parallel-safe now; build authorization rides batch-2 close.

---

**Signed:** gandalf, 2026-07-06 (ELICITOR). The lens is the right fiction; now rule on what the soul gets to keep.
