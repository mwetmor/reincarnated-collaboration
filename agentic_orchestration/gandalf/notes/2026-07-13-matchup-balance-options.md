# Kit-vs-Kit Matchup Balance — the options space

> **STATUS:** OPTIONS ANALYSIS (Pattern B deep-think, Matt commission 2026-07-13: *"ultra think about what options we have to balance the kit versus kit matchups… a derived set of KPIs that could build out something like a pokemon-style matchup system where we balance the faces of the matchup."*)
>
> **Discipline:** recognition + options NOW; architectural commitments DEFERRED until the empirical gate (§8 pilot matrix on the founding roster) resolves. Nothing here amends canon yet.
> **Author:** gandalf, 2026-07-13. Companion: wind-down doc §3/§5 (pointers added same session).

---

## §0 The problem, stated precisely

Two balance contexts, one shared substrate:

1. **The mothership ARPG.** The goldilocks dungeon plan (as discussed: per-dungeon PvE normalization) balances **kit-vs-content**. But under *Keep What You Kill*, **every boss encounter is already a kit-vs-kit matchup** — bosses are entries from this same roster (PART F B13: enemy-side consumer of the same roster). A player piloting kit A into boss-kit B experiences `matchup(A,B)` whether we've designed it or not. Goldilocks can normalize scalars per encounter; it cannot erase matchup *texture* — nor should it (§7).
2. **The satellite mini-games.** Hero-line-wars / horde / TD / auto-chess put **player-selected populations** of kits against each other, directly or via armies. Here matchup structure is the whole game. PvE-parity does not transfer: two kits perfectly goldilocks-balanced can be 90/10 head-to-head (the oldest lesson in the genre — D2 PvP was never D2 PvE).

**The core distinction:** kit power decomposes into a **scalar** (how much total stuff the kit does — what goldilocks/B14.5 already normalizes vs canonical content) and a **shape vector** (how the stuff is distributed across range/movement/tempo/geometry/defense — which is what wins or loses specific matchups). Scalar parity is necessary, not sufficient. Matchup balance is a claim about the *structure of the pairwise outcome graph*, and about the *population* placed on it.

## §1 What we now know that changes the problem

- **Every kit has a plane address** (movement × delivery × tempo) + engine-key descriptors (geometry/control/defense/economy). Matchup-relevant physics *derive from these coordinates* — the plane is not just a browse surface; it is the coordinate system matchup structure lives in.
- **Measured-vs-projected law:** corpus ghosts cannot fight — only emitted, sim-runnable kits can enter a measured matchup matrix. The matchup instrument is therefore **post-emission for corpus kits, available NOW for the 45-kit founding roster** (pilot seam, §8).
- **The candidate pool is large (500+).** Population-level balance (choose a healthy subset) is only viable when the pool is big enough that healthy subsets exist. It now is — this is what the corpus bought us.
- **Mini-games are thin rule-set wrappers** over certified kit JSONs — meaning *the wrapper itself is a balance layer* (pricing, tiers, draft) that costs nothing at the kit grain.
- **The sim + telemetry stack is ready to extend:** spatial gauntlet (kit-vs-environment) + v2.21 per-element output columns; a duel/arena mode is an extension, not a new subsystem.

## §2 What the genre already learned (named precedents)

| Precedent | The lesson we take |
|---|---|
| **Pokemon type chart + Fairy** | Ecosystem balance ≠ flat matchups. When Dragon dominated, Game Freak didn't nerf stats — they **added a type** (Fairy, Gen VI): intervention by *population/structure design*, not stat surgery. Faces + representation is the right target. |
| **Smogon usage tiers (OU/UU/NU)** | Population balance **by measurement**: tiers derive from usage data; each league is internally balanced without touching a single stat. Stratification is a balance operation. |
| **Fighting-game matchup charts** | Community N×N win-rate matrices; health = every row-average ≈ 5, no 9-1s, archetype spread. The informal archetype set converges at **~5-6** (rushdown / zoner / grappler / turtle / puppet / all-rounder) — Matt's "6 sides" matches the genre's own convergence point for legible matchup reasoning. |
| **Auto-chess costing** | Cost tiers convert "imbalanced units" into "correctly priced units." Price-accuracy is measurable; equality is not required. |
| **MOBA draft/ban** | Counter-pick structure is the *strategic layer*, not a bug. Self-balancing under selection pressure is a design goal. |
| **MTG metagame health** | Archetype RPS (aggro>control>midrange>aggro); health = no archetype above share-cap, every archetype has predators AND prey. |
| **D3 vanilla flattening (warning)** | Over-normalization kills identity. If all matchups trend 50/50, kit choice stops mattering and the power fantasy dies. **Perfect flatness is a failure state, not the goal.** |

## §3 The options space

**OPTION 1 — Declared element type-chart (Pokemon-literal).** Hand-author element-vs-element multipliers.
*Verdict: REJECT as core.* Element is RULED a free axis (flavor-forward, pipeline-assigned, disregardable) — making it balance-bearing reverses a standing ruling. Worse, a hand-authored chart is pre-imposed taxonomy: if the sim contradicts the declared counter, we've taught players lies. (A wrapper MAY later add a legible element-multiplier as a mini-game gimmick — wrapper option, never core.)

**OPTION 2 — Derived faces from plane + engine key.** Interaction classes derived from coordinates (SUMMON armies lose to NOVA sweep; ROOTED artillery loses to FREE-MOVE divers…), pre-registered as hypotheses, sim-validated.
*Verdict: ADOPT as the hypothesis layer.* Substrate-led; the chart is honest physics, not fiat.

**OPTION 3 — Empirical matchup matrix (measure, don't declare).** Duel-harness N×N win-rate matrices per context; faces EMERGE by clustering matchup-profiles (rows). Same methodology as V8 (fingerprints → factor analysis → named composites → Edition freeze) applied to pairwise outcomes.
*Verdict: ADOPT as the measurement layer.* Options 2+3 compose: 2 pre-registers, 3 validates; the surviving faces are the legible compression of the measured matrix.

**OPTION 4 — Population/ecosystem curation.** Balance the SELECTION, not the kits: given the matrix, choose demo/mini-game populations whose matchup graph is healthy (KPIs §5). This is Matt's own framing ("all have decent representation across the final group I select") and the Fairy-type lesson operationalized.
*Verdict: ADOPT as the primary balance operation.* No kit surgery; per-mini-game populations; composes with S7 curation — the selection surface gains a live ecosystem-health read.

**OPTION 5 — Wrapper-layer knobs.** Pricing (HLW send-economy, auto-chess cost), tiers/leagues (Smogon-style, usage- or strength-derived), draft/ban, mirror-symmetric formats.
*Verdict: ADOPT as the secondary operation.* Converts residual imbalance into strategy; preserves the power chase.

**OPTION 6 — Kit-internal tuning.** Stat surgery on outliers.
*Verdict: LAST RESORT.* Only for pathological rows (a kit with no prey, or an unwinnable matchup that population design can't route around) — it re-fires certification and risks the D3-flattening failure.

## §4 Recommended architecture (layered; extends the factory, invents nothing new)

- **L0 (exists):** goldilocks/B14.5 scalar normalization vs canonical content. Keep — it's the precondition that makes shape the only remaining variable.
- **L1 (new measurement — gamora seam):** duel harness extending the spatial gauntlet. **A 3-context battery**, because AoE/summon value flips wildly between contexts: **(i) open arena 1v1** · **(ii) lane army-vs-army** (HLW physics) · **(iii) wave-throughput** (TD/horde physics). Output → matchup matrices per context → telemetry (star-lord).
- **L2 (faces — gandalf spec, math hotspot):** cluster matchup rows per context; test pre-registered interaction hypotheses (§6); derive ~5-8 faces (legibility prior; the count is the data's call, 6 if the data says 6). Validity test: intra-face matchup-profile coherence (a face label must PREDICT a matchup row). Freeze face taxonomy Edition-I style once retrodiction holds.
- **L3 (operations, preference order):** population curation → wrapper pricing/tiers/draft → kit surgery last.
- **L4 (the dashboard — Matt's S7 surface):** ecosystem-health KPI panel live over any candidate selection: pick kits on the periodic table, watch the health vector update.
- **Bridge hypothesis (registered, not assumed):** V8 behavior-space position predicts matchup profile. If validated on measured kits, corpus ghosts get **projected matchup estimates** via nearest measured anchors (watermarked PROJECTED per measured-vs-projected law) — matchup foresight even before a kit is emitted.

## §5 The derived KPI catalog (Matt's ask)

**Per kit (per context):** matchup row (win% vs each opponent) · row-mean (target band ~45-55%) · row-spread σ · worst/best matchup · counter-count & prey-count (each ≥k in the selected population) · price-accuracy residual (priced modes) · context-divergence (how much the profile flips arena↔lane↔wave — high divergence = "context specialist," a feature to surface, not a bug).

**Per population (the selection-health vector):**
1. **Face representation** — every face ≥m members (Matt's "all sides have decent representation," directly).
2. **Row-mean band compliance** — % of kits inside the fairness band.
3. **Cyclicity index** — 3-cycle density of the win digraph vs transitive-tournament baseline (RPS structure present; the graph must be far from a strict hierarchy).
4. **Equilibrium diversity** — replicator-dynamics / Nash-averaging equilibrium over the matrix; KPI = entropy / effective-population-size at equilibrium (no kit >share-cap, no kit ~0). This is the formal version of "self-balancing under player selection pressure."
5. **Dominated-kit count** — kits with no prey (target: zero).
6. **Reachability (mothership)** — from every starting kit, an ascending beatable-boss path exists to endgame (§7). A *routing* criterion, not a flatness criterion.

**Per face:** intra-face coherence (silhouette on matchup-space) · face-vs-face aggregate matrix cyclicity + row-balance.

## §6 Candidate faces + pre-registered interaction hypotheses (UNVALIDATED — sim will vote)

Illustrative 6-face draft derived from plane coordinates — pre-registered so the pilot can confirm/refute, **not** adopted:

| Face (draft) | Plane signature | Hypothesized beats | Hypothesized loses to |
|---|---|---|---|
| ARTILLERY | ROOTED/WALK × PROJECTILE/BEAM, long range | ZONER (outranges placement), SWARM (kills at spawn) | DIVER (gap-close under commitment) |
| DIVER | FREE-MOVE × MELEE/PROJ, SPIKY | ARTILLERY (closes), ZONER (jumps the zone) | NOVA-BRAWLER (point-blank retaliation), TURTLE (burst absorbed) |
| NOVA-BRAWLER | FREE-MOVE/WALK × NOVA/ORBITAL | SWARM (sweep), DIVER (welcome party) | ARTILLERY (outranged) |
| SWARM-MASTER | SUMMON | DUELIST/TURTLE (target saturation) | NOVA-BRAWLER, ZONER (armies path through zones) |
| ZONER | ZONE, placed-persistent | lanes/chokes generally; TURTLE (forced off ground) | DIVER (open-arena pickoffs), ARTILLERY |
| TURTLE/DUELIST | single-target FLAT, tank/absorb | DIVER (wins extended trades), NOVA (out-sustains) | SWARM (saturated), ZONER (attrition on ground) |

Cross-cutting tempo/defense hypotheses worth testing in the same pilot: absorb-shields counter SPIKY (burst eaten) while FLAT chews shields; hard control counters WIND-UP/CHANNEL (the commitment axis returns as matchup-relevant even though it isn't a plane row — the archive axis earns its keep).

## §7 The KWYK recognition — matchup graph as progression topology (mothership)

Under *Keep What You Kill*, defeating boss-kit B grants B. Therefore **the matchup digraph IS the progression graph: you climb the food chain by eating your predators.** This flips the mothership requirement from "flatten matchups" to **"route them"**:

- Run curriculum as matchup story: early bosses = prey (power fantasy) → mid = mirrors (skill check) → late = counters (mastery test). Dramatic structure and balance become the same instrument.
- Beating your counter *hands you the counter* — the reincarnation loop is narratively self-balancing.
- The balance criterion becomes **reachability** (KPI §5.6): every kit has an ascending path; no kit is a dead end; goldilocks handles scalars per-encounter while the matchup layer supplies legible texture ("this boss is hard *for you* because you're both melee" is a feature when the player can read it).

This is a design-direction recognition, registered here; it needs no ruling to proceed with the mini-game work, but it should shape how the dungeon's boss-ladder generator eventually consumes the matrix.

## §8 Staged plan + the empirical gate

1. **PILOT (fires when Matt says go — no dependency on Q19/S6):** gamora extends the gauntlet with arena-1v1 duel mode; run the founding-roster matrix (~45×45, sampled, 100x speed — small). Output: first real matchup matrices + noise profile.
2. **Methodology consultation (Discipline #18, extension-hotspot timing):** AFTER pilot empirics land, legolas Mode A on the formal toolkit — Nash averaging / α-Rank (DeepMind agent-population evaluation), replicator dynamics for game balance, tournament-graph statistics — chosen against the observed signal-to-noise, not in the dark.
3. **Face derivation + hypothesis adjudication (§6 table confirmed/refuted) → face taxonomy freeze** (Edition-I discipline).
4. **Lane + wave contexts** added to the battery (mini-game physics).
5. **L4 dashboard** joins the S7 selection surface; per-mini-game population curation + wrapper pricing derive from it.
6. **Corpus kits enter the matrix as they emit** (S6) — matchups measured on arrival; projected-estimate bridge (§4) validated or discarded.

**Forks for Matt (decision-shaped, one-word-vetoable):**
- **F-1 Face source:** derived-and-validated (Options 2+3, my lean) vs declared element chart (Option 1, rejected-with-reasons) — confirm the lean or challenge.
- **F-2 Operation order:** curation → wrapper → surgery-last (my lean) — confirm or reorder.
- **F-3 Context battery:** 3 contexts (my lean) vs arena-only-first.
- **F-4 Pilot timing:** roster-now (my lean — it's also the Disc-18 baseline gate) vs post-emission.
- **F-5 Face count:** let clustering vote within 5-8 (my lean) vs fix 6 ex-ante.

---

**Signed:** gandalf, 2026-07-13. The goldilocks loop makes every kit *worthy*; the matchup layer decides what its worth *means against a living opponent*. We measure the war of all against all, name its faces, and then — as with the corpus — let the substrate vote.
