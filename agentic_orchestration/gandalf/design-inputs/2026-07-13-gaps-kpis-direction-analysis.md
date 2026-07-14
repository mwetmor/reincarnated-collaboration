# Gaps, KPIs, and Direction — the four-charge ultrathink analysis

**Author:** gandalf (Pattern B sustained design analysis) · **Date:** 2026-07-13
**Charter:** `gandalf/design-inputs/2026-07-13-gaps-kpis-direction-ultrathink-prompt.md`
**Settled input:** `gandalf/design-inputs/2026-07-13-family-definition-analysis.md` (family = fiber of behavior map B)
**Evidence base:** `research/curated/corpus.db` (read-only; 524 corpus rows, 470 keyed combat-kits, 38 negatives — all counts re-verified at assertion time per Discipline #11) · `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` · `gamora/analyses/2026-07-13-cell-key-dedup-v1/` · engine code (`simulation/fight_result.py`, `simulation/gauntlet_sim.py`, `simulation/bounded_viability_validation.py`, `telemetry/{db,recorder,migrations}.py`) · `canonical/reap-die-rise-game/one-realm-mvp-scope.md`
**Role-tags worn:** `SPEC-AUTHOR` (Charges A–C) → `DRIFT-CRITIC` + `ELICITOR` (Charge D)

---

## 0. Orientation — what this file rules on

Four charges, one decision. A: what the genre's 38 labeled corpses teach. B: what the sim can actually measure, and therefore what "behavior map B" can honestly mean. C: which empty cells of the lattice are discoveries and which are warnings. D: whether the whole bet — 13-coordinate lattice + curated corpus + generation + sim-as-oracle + gaps-as-product — survives its own steelmen. The Charge-D closing paragraph is the object Matt acts on.

▶ ROLE: SPEC-AUTHOR — Charges A–C are evidence work; the critic comes later.

---

# Charge A — The graveyard speaks: mining the 38 negatives

## A.1 The split, refined (the prompt's 33/5 is wrong)

The charter claimed a verified split of 33 genre-negatives vs 5 pipeline-negatives ("no rule matched"). Re-verification breaks this: **all five no-rule-matched kits (d2-impale-zon, gd-reap-spirit, d2-grim-ward-barb, d2-leap-attack-barb, hot-blood-catcher) carry real genre postmortems in `mech_note`.** "No rule matched" is a *keying-pipeline TODO flag*, orthogonal to provenance. The correct split:

| class | count | members |
|---|---|---|
| **Kit-level genre-negatives** (real postmortem, real skill) | **36** | everything below except the two next rows |
| **System-level evidence records** (not kits — degeneracy documentation) | **1** | vs-golden-egg-scaling |
| **Unfilled records** (mech_note NULL) | **1** | d2-sacrifice — which has also **leaked into the keyed 470** with a blank-heavy key (`walk\|blank\|spiky\|melee_strike\|blank\|unknown\|…`) |
| *(orthogonal flag)* pipeline keying-TODO | 5 | the no-rule-matched five — genre-negatives that ALSO need pipeline attention |

Coverage: 38 negatives across **11 sources** (d2×8, d3×4, d4×4, poe1×6, poe2×4, gd×3, le×3, tq×2, vs×2, tl×1, hot×1). Only **1/38 is keyed** — the full negative-vs-positive collision analysis is blocked on re-keying (curation item A.5-3).

Data-quality finding: `mech_note` is truncated at ~140 chars in the DB (mid-word cutoffs on every long note) — ingest artifact, elrond flag.

## A.2 Twelve failure patterns

Kits may carry multiple tags (a corpse can die of two things); the tag-sum exceeds 38 by design. Each pattern carries: members, verdict (**intrinsic RED law** / **extrinsic AMBER** / structural), coordinate region, KPI signature (how Charge-B's vector would see it), curation follow-up.

### 1. TUNING-STARVATION — extrinsic → AMBER
**Members (6, 4 games):** d2-inferno-sorc, d2-blade-sin, tl-arc-beam, d3-shield-bash, poe2-wall-of-shields, poe2-chronomancer-01.
The shape was fine; the numbers were starved — Inferno under-delivered its *listed* damage for decades; Blade skills were "chronically undertuned pre-D2R"; Arc Beam "drank the mana pool faster than it killed"; Wall of Shields was on 0.5's dead-on-arrival list. **Our balance loop is the specific antidote:** bounded viability exists precisely to make scalar starvation impossible. Coordinate region: mostly rooted/channel and shield-verb cells. KPI signature: shape-normal, scalar-low at reference tuning — the exact class the loop repairs. Curation: tag `death=extrinsic-tuning`.

### 2. ITEMIZATION-/SUPPORT-ORPHAN — extrinsic → structurally DISSOLVED
**Members (7, 3 games):** d3-firebomb ("no set, legendary, or meta ever wanted"), d3-wave-of-force ("never earned a set"), d3-spectral-blade, d4-wind-shear ("never found its Heartseeker moment"), d4-kick, d4-blade-shift ("never earned an aspect home"), le-shield-bash-le ("never found a tree path worth building").
These died of a lottery *outside the kit*: per-skill legendary/set/aspect/tree support that never arrived. **This death cannot occur in our system** — gear law §3A.1 (amplify your own · path texture to anyone · import no one's core · invent nothing) plus universal gear generation means no kit waits on a named-item sponsor. KPI signature: none — the kill mechanism lives outside the sim, which is itself the diagnostic (a kit that sims fine but "needs" external sponsorship is this pattern). Curation: `death=extrinsic-itemization`.

### 3. DISPLACED-DAMAGE MOVEMENT FUSION — intrinsic → **RED LAW (co-location)**
**Members (2, 2 games, ~20 years apart):** d2-blaze-sorc (fire trail *behind* the running caster), poe1-charged-dash (mirage projected *along the path*, damage where you were).
Same death twice across two decades: damage painted where the avatar WAS while mobs chase where the avatar IS. **Red law: damage must be co-located with the avatar's present position or an anchored proxy (totem/trap/minion).** Coordinate region: movement-fused delivery + path/trail geometry. KPI signature: **mostly unobservable** — the abstract positional model can't see trail-vs-chase geometry. This law must be carried by curation and generation filters, not by B. That is not a flaw to fix; it is the division of labor (§B.2).

### 4. MOVEMENT-VERB-AS-PRETENSE — intrinsic RED unless instant+spammable
**Members (3):** d2-leap-attack-barb ("the movement verb was the payload and the payload never paid"), d4-blade-shift (dual-tagged), poe1-charged-dash (dual).
A movement verb asked to be a main damage loop, priced with wind-up/travel/recovery. The register **already separates** the living from the dead: the 19 keyed dash/teleport survivors (poe1-flicker et al.) sit at tempo=high + commit=instant; the corpses sit at wind-up + low tempo. The carve-out is real: **instant + spammable movement-damage lives; committal movement-damage dies.** KPI: K3 duty-cycle + K2 escape-context. Curation: none — this is a register success story; cite it in Stage-2.

### 5. SPLIT-SCALING FUSION — AMBER if scaling is unified
**Members (4):** d2-golemancer ("golem-as-primary never worked across two decades"), gd-reap-spirit (nuke + summon per cast, halves of different builds), le-soul-feast (nuke that lived as curse-texture, never core), poe1-reaper (dual).
Two damage sources scaling off disjoint stat axes → neither reaches viability. Our generation emits **unified scaling grammars** (one dependency spine per kit), so the fusion is legal where the genre's stat-split made it fatal. KPI: K5 proxy-share bimodality (a kit whose proxy share oscillates between "why bother" and "why cast" is this pattern). Curation: `death=extrinsic-split-scaling` on the ambers; poe1-reaper stays red via pattern 6.

### 6. ANTI-SYNERGY LOOP — intrinsic → **RED LAW**
**Members (2, 2 games):** poe1-reaper (flagship minion that EATS your other minions), vs-gatti-amari (cats that eat your pickups).
The kit's sustain mechanism consumes the build's own scaling substrate. **Red law: sustain must not cannibalize the build's own resources, army, or economy.** KPI signature: observable — K5 proxy-death anomaly (deaths attributed to own side) and K6 economy drain without output gain. This is the one intrinsic law B *can* eventually see.

### 7. STOCHASTIC-WITHOUT-LEVER — AMBER if operators supply the lever
**Members (3):** poe1-wild-strike (random element + random secondary per hit), le-tempest-strike (random storm procs), gd-stun-jacks (scatter, partial tag).
Randomness the player cannot itemize toward: three elements → zero elements you can build around. The genre's own fix proves the amber: PoE's Trinity support turned tri-element from trap to archetype — a *loading lever*. Our operator grammar can emit weighted/loadable randomness natively. KPI: K3 amplitude CV high without corresponding spike payoff. Curation: `death=extrinsic-no-lever`.

### 8. TIMING-TAX OVERPRICED — structural PRICING LAW (variable-execution pillar input)
**Members (3, 3 games):** poe2-perfect-strike-01 ("rhythm-game flourish"), tq-calculated-strike (every-fourth-hit payoff losing to Onslaught's always-on), d2-impale-zon (huge hit, durability cost, glacial recovery).
Execution taxes (timing windows, Nth-hit rhythms, recovery locks) priced above their payoff. Not a red law — a **pricing law: a timing tax must buy strictly more than its cost, benchmarked against the always-on sibling.** This is direct input to the H-series / variable-execution emission bars: the genre keeps shipping this trap because the tax *feels* like depth at design time. KPI: K3 spike-amplitude vs duty-cycle ratio against the flat sibling.

### 9. SINGLE-TARGET-NO-BOSS-NICHE — context-structural, conditional AMBER
**Members (3):** gd-blade-trap, d2-impale-zon, poe1-glacial-hammer ("entire cultural footprint is jokes").
ST kits die when the content mix offers no protected niche. Our F3 boss run-beat family is the structural antidote — **conditional on boss beats being real, frequent content** (they are: §23 run-beat families). KPI: K1 spike on boss-cell + K2 F3; the kit is HEALTHY iff its F3 spike exists and the run guarantees F3 beats. Curation: `death=extrinsic-content-mix`.

### 10. SIBLING-SHADOWED — not cell failures; isotope-model validation
**Members (5):** poe1-cleave ("the skill you replace by act 2"), poe1-sweep, poe1-glacial-hammer (dual), tq-flame-surge ("never out-earned its own mastery siblings"), d3-spectral-blade (dual).
Died of comparison, not of self — a strictly-better sibling occupied the same cell. These are **isotopes of living cells**, which is precisely why dedup retains losers instead of deleting them. No law. Validates the isotope model: the cell is fine; the loser documents the intra-cell quality bar.

### 11. SYSTEM-LEVEL DEGENERACY — evidence records for ceilings
**Members (2):** hot-blood-catcher (interaction produced hundred-billion damage totals), vs-golden-egg-scaling (infinite permanent stats "eventually DISSOLVE build identity").
Not kit deaths — system-interaction blowups. Input to gauntlet ceiling design (the KPM=600 ceiling bypass must stay a *bypass*, never a norm) and progression caps (golden-egg is the canonical argument against uncapped permanent stacking: **identity dissolution is the end-state of infinite generic scaling**). Curation: keep as system-evidence rows; exclude from kit-level statistics.

### 12. PORT-CONTEXT DEATH — franchise-level proof that viability is extrinsic
**Members (3, 1 franchise):** poe2-concoction (**PoE1's league-start QUEEN, ported, dead**), poe2-chronomancer-01, poe2-wall-of-shields.
The same or near-same kit, moved to a new game context, died. Concoction is the cleanest single exhibit in the corpus: nothing about the kit changed; the world around it did. **This is the strongest evidence that a large fraction of graveyard cells are AMBER: the cell didn't fail — the game around it did.**

## A.3 Negative–positive collisions (what the register sees and doesn't)

Only d2-sacrifice is keyed, so full collision analysis is blocked (→ A.5-3). Raw-column proxy probes:

- **The rooted-channel region is CONTESTED, not blind.** 12 keyed survivors sit in `rooted|…|channel|…` cells — gd-aar (Albrecht's Aether Ray) among them, which survived *essentially the same configuration* that killed tl-arc-beam, d2-inferno-sorc, and d4-incinerate. The register does not separate them — and it *shouldn't*, because the deaths were tuning/pricing (pattern 1), not structure. Knife-edge tuning sensitivity is a fact about the cell, not a blindness of the key. **This forces a fourth cell category: CONTESTED — cells holding both corpses and survivors, where the difference is tuning, not coordinates** (→ Charge C taxonomy, Charge D refinement b).
- **Where a real difference exists, the register sees it.** poe1-incinerate (alive; build→spend ramp) vs d4-incinerate (dead): separated by #13 dependency plus context — same verb name, different machines.
- **One genuine blindness candidate:** "skill-IS-movement" appears as a raw marker on 5 negatives but is not a coordinate value. Partially expressible today via geometry=dash_attack/teleport + #10 tempo + #11 commit (which already split flicker from leap-attack). Verdict: **a Stage-2 consideration, not a new coordinate** — the existing coords carry the discrimination that matters.

## A.4 The amber ledger (headline)

Tallying deaths by curability: **intrinsic RED** (patterns 3, 6, and the non-carve-out half of 4) accounts for ~6 kit-deaths. **Extrinsic AMBER** (patterns 1, 2, 5, 7, 12) accounts for ~20. Structural/pricing (8, 9) ~6, validation/system (10, 11) ~7 (multi-tags overlap). **Roughly two-thirds of the genre's labeled corpses died of causes our architecture specifically removes** — tuning starvation (balance loop), itemization orphanhood (agnostic loot), port context (one coherent game). The graveyard is not a list of forbidden cells; it is a list of cells the genre *mispriced*, plus a short list of true laws:

> **Red laws (hard generation/curation filters):**
> 1. **Co-location:** damage co-located with the avatar's present position or an anchored proxy.
> 2. **No anti-synergy:** sustain must not cannibalize the build's own scaling substrate.
> 3. **Movement-damage carve-out:** movement verbs as damage loops only at instant-commit + high tempo.
>
> **Pricing laws (emission bars, not filters):** timing taxes must out-buy the always-on sibling (8); control payloads must be priced in AoE/duration/cooldown against their damage-pure sibling (from gd-blade-trap/gd-stun-jacks); ST kits require the F3 niche to exist (9).

## A.5 Curation follow-ups (elrond batch)

1. `mech_note` 140-char ingest truncation — re-ingest full postmortems.
2. d2-sacrifice: unfilled record leaked into keyed 470 with blank-heavy key — fill or quarantine.
3. **Re-key the remaining 37 negatives** (highest value: unblocks corpus-wide collision analysis; the CONTESTED map needs it).
4. Resolve the 5 no-rule-matched pipeline TODOs (they are genre-negatives awaiting keys, not a provenance class).
5. Add `death=` provenance tags per A.2 (extrinsic-tuning / extrinsic-itemization / extrinsic-split-scaling / extrinsic-no-lever / extrinsic-content-mix / intrinsic-red / system-evidence) — this single column turns the graveyard into a queryable prior for Charge-C classification.

---

# Charge B — Opening behavior map B

## B.1 What the sim measures today (code-grounded)

From `simulation/fight_result.py` (read in full): **FightResult** carries winner/loser, duration, termination_reason (a_dead / b_dead / timeout / stalemate), remaining HPs, damage dealt both sides, action counts, heals/potions, proxy telemetry (damage contribution, by-type, deaths, per-side), and the **BC raw accumulators**: hit count/sum/sumsq (→ amplitude CV), evasion-misses + incoming-attempts (→ avoidance rate), shield_absorbed, hot_recovered, premitigation damage (→ mitigation decomposition), plus E3 per-element attribution. **RoomResult** chains sequential encounters with HP carry-through; **BatchResult** aggregates win-rate and duration → matchup matrices are computable today. `gauntlet_sim.py` runs 18 SC-6 encounters × 4 cohorts with per-archetype KPM bands; `bounded_viability_validation.py` implements doc 50 §4.4 (specialization = 1–2 cells at 1.5–2.0× ratio).

**Stale-gap correction (Discipline #11):** two telemetry gaps flagged in prior analyses — engine_version unknown, termination_reason missing — are **both CLOSED schema-side** (engine_version NOT NULL on seasons and threaded through the recorder; termination_reason landed in migration 1.9). Analyses citing them are stale.

## B.2 The core derivation: B is differential shape at frozen tuning — never the balanced scalar

Doc 50's bounded viability makes the balance loop's *job* the equalization of scalar win-rate into bands. Therefore **post-balance scalar win-rate carries approximately zero identity information by design** — using it as B would be measuring the thing we engineered to be constant. Identity lives in what the loop *preserves*: the specialization spike (1–2 encounter cells at 1.5–2.0×) and the shape of response across contexts.

Charge A supplies the confirming split: the genre's corpses divide into **scalar-deaths** (tuning starvation — which our loop cures) and **shape-deaths** (displaced damage, anti-synergy — which no tuning cures). So the division of labor is:

> **The loop owns the scalar. B owns the shape. Curation owns the shapes the sim cannot see.**

Formally: **B(kit) = the differential-response vector of the kit at frozen reference tuning against a fixed encounter/opponent panel.** Two kits are same-family iff their differential shapes match (invariance), across the fiber's free coordinates. Freezing tuning is what makes B well-defined — the same kit measured pre- and post-balance would otherwise wander the codomain.

## B.3 The KPI vector (proposed)

| KPI | definition | measured from | status |
|---|---|---|---|
| **K1 matchup-differential shape** | per-opponent-panel normalized win-margin/TTK vector at frozen tuning; identity = *which cells spike* (doc 50's 1.5–2.0× formalized) | BatchResult matrices | computable today |
| **K2 density-response curve** | performance across F1 dense / F2 open / F3 boss / F4 escape run-beat contexts, normalized to cohort band | gauntlet contexts | **blocked on gauntlet re-base** (jack-ryan metrology) |
| **K3 temporal shape** | damage-event CV (hit sumsq), ramp time-to-steady-output, burst duty cycle | BC accumulators | computable today |
| **K4 survival-route decomposition** | premitigation→actual decomposition via evasion misses / shield absorbed / HoT recovered / potions | BC accumulators | computable today |
| **K5 proxy displacement** | proxy damage share + by-type + proxy deaths (incl. self-inflicted → anti-synergy detector) | proxy telemetry | computable today |
| **K6 economy stress** | starvation events, downtime share, resource-floor time | **not accumulated** | needs small gamora accumulators |
| *(excluded)* | balanced scalar win-rate | — | **excluded by design** (§B.2) |

## B.4 Coordinate → KPI influence map + validation sketch

| register coord | primary KPI echo |
|---|---|
| #1 movement, #9 range | K2 (escape/kite contexts), K1 (vs ranged/melee panel cells) |
| #2 delivery, #4 geometry | K2 density-response (the AoE-vs-ST signature) |
| #3 amp, #10 tempo | K3 (CV, event rate) |
| #5 control (both slots) | control-uptime share (existing BC 2B) + K1 vs swarm cells |
| #6 defense | K4 route decomposition |
| #7 economy, #13 dependency | K6 + K3 ramp profile (build→spend = time-shifted K3) |
| #8 proxy | K5 |
| #11 commit, #12 activation | K3 duty cycle + K2 interrupt-rich contexts |

Validation against knowns (predictions, falsifiable once instrumented): **whirlwind fiber** → K2 spikes F1-dense, K3 flat-CV sustained, K4 mitigate/tank routes. **Trap/mine** → K3 setup-ramp (time-shifted damage), K2 F3 spike (pre-lay burst), commit=setup echo. **Aura** → near-zero K3 rhythm, K5 zero, K2 flat (density-insensitive). **Totem-sentry** → K5 high, K3 deploy-ramp. Negatives: **d2-inferno** → shape-normal + scalar-low (amber signature: the loop would have saved it). **poe1-reaper** → K5 self-inflicted proxy-death anomaly (red signature: no tuning saves it). **d2-blaze** → *no clean KPI signature* — the honest case; see B.5.

## B.5 Feasibility verdict (honest)

**Measurable today:** K1 (matrices), K3/K4/K5 (accumulators exist in FightResult). **Blocked:** K2 on the gauntlet re-base (the 8-mob saturation wall was ruled a broken instrument 2026-07-07; jack-ryan metrology pending). **Missing:** K6 needs small new accumulators (gamora seam, low cost). **Structurally under-observable:** displaced-damage / positional-painting patterns (pattern 3) — the abstract positional model cannot see trail-vs-chase geometry, and building positional fidelity for one red law is not worth it: **the co-location law is carried by curation/generation filters instead.** That is division of labor, not failure.

**Verdict: B-as-oracle is a build milestone, not a current fact.** Named acceptance test: *the K-vector separates the six confirmed fibers from the 126-kit null mush (pairwise fiber separation ≥ the fiber-internal spread) AND reproduces at least one known-bad signature (poe1-reaper's K5 anomaly is the best candidate) on a synthetic re-key.* Until that test passes, fibers remain **proxy-confirmed** — designer judgment + cross-game recurrence (the current standard, which the six fibers already meet with lifts 224–2119). Nothing in the family definition has to wait for the oracle; the oracle upgrades confidence, it doesn't gate the lattice.

---

# Charge C — Gaps: discoveries, warnings, and the honesty exhibit

## C.1 Method + taxonomy

Hamming-1/2 enumeration around the six confirmed fibers (populations re-verified: whirlwind 11 · trap-mine 10 · aura 6 · minion-taunt 7 · chan-beam 7 · totem-sentry 21); 44 isolate kits at minHam ≥ 4 (families-of-one candidates); 33 zero-co-occurrence coordinate pairs (forbidden-prior candidates). Classification taxonomy, **now five-way** (Charge A forced the fifth):

- **UNCLAIMED** — no genre attempt found (corpus + out-of-corpus check) → Mendeleev prediction.
- **GRAVEYARD-RED** — attempted, died of an intrinsic law → do not generate.
- **AMBER** — attempted, died extrinsically (tuning/itemization/port) → *promoted generation target*: our systems are the specific antidote.
- **CONTESTED** — corpses AND survivors in the same region; difference is tuning, not coordinates → generate with pricing laws attached.
- **FORBIDDEN-PRIOR** — zero co-occurrence for definitional or deep-tension reasons → prior, not law; generation may test the tension ones.

## C.2 The honesty exhibit (rule before the list)

The control-trap cell (trap-mine fiber + treatment=control) looked like a clean UNCLAIMED gap from fiber adjacency alone. It is not: **the corpus itself holds two nearby corpses** — gd-blade-trap (single-target immobilize, long cooldown; "GD's running punchline") and gd-stun-jacks (scatter-stun) — and the genre holds a *success* outside our sample: PoE1's Bear Trap thrived for a decade as a utility/boss tool. The cell is **AMBER-CONTESTED with a pricing law** (control payload priced against the damage-pure sibling), not virgin territory. **Lesson, binding on all gap work: corpus sparsity ≠ genre absence. Every UNCLAIMED ruling requires an out-of-corpus genre-check before it may be called a discovery.** The lattice proposes; the genre record cross-examines.

## C.3 Ranked gap list

| # | cell (fiber + delta) | class | one-line |
|---|---|---|---|
| 1 | chan-beam + movement=full-move (**mobile beam**) | UNCLAIMED | the beam that comes with you — genre-wide absence is balance-fear, not physics |
| 2 | whirlwind + treatment=control (**herding spin**) | UNCLAIMED | drag the pack with you; genre precedent only as PoE support-gem texture, never kit-core |
| 3 | retaliation family (chr-thorns-templar, minHam 5) | AMBER-THIN | genre-proven family (D2 Iron Maiden, D3 Invoker thorns meta, LE riposte); corpus n=1 is a sampling artifact → densify |
| 4 | trap-mine + treatment=control (**control trap**) | AMBER-CONTESTED | two GD corpses (pricing deaths) + PoE Bear Trap success → generate with pricing law |
| 5 | banked-channel mobile emitter (poe1-winter-orb, minHam 5) | UNCLAIMED-adjacent | channel-to-bank, auto-emit while moving — family-of-one begging densification |
| 6 | deferred-detonation family (4 hades isolates: merciful-end, ares-doom, medea-skull-cast, glorious-disaster) | **candidate fiber seed** | curse-then-burst recurs 4× in one source — likely a *fiber we haven't confirmed*, not 4 gaps |
| 7 | stack-release marksman (poe2-snipe-mirage, minHam 5) | thin | banked-stacks burst archer; densify |
| 8 | whirlwind + range=ranged (tornado emitter) | CLAIMED-THIN | D3 Wastes dust-devils already lives here as isotope texture; emission target, weak discovery |
| 9 | rooted-channel region writ large | CONTESTED | 12 survivors incl. gd-aar + 3 corpses (arc-beam, inferno, d4-incinerate); knife-edge tuning cell — the balance loop's showcase |
| 10 | forbidden priors held | FORBIDDEN-PRIOR | melee⊗projectile (definitional); channel⊗cooldown/finite, proxy-heavy⊗channel, build→spend⊗reserve (deep tensions — priors generation may deliberately test, one probe each) |

## C.4 Top-gap archetype briefs

**Brief 1 — Mobile Beam** (chan-beam fiber + movement=full-move). *Genre-check:* D3 Disintegrate and D4 Incinerate are rooted (and Incinerate is a corpse); Lost Ark's Machinist laser proves the fantasy lands out-of-corpus; nothing in our 470 occupies the cell. The genre avoids it because channel pricing assumes a rooted-tax; remove the tax and the price breaks. *Our answer:* pay with economy instead — heavy drain/reserve (K6) + tempo cost. *Player consequence:* the walk-and-burn kiter — sustained-damage fantasy without the rooted claustrophobia that killed three corpses in the adjacent CONTESTED cell. *KPI prediction:* K2 escape-lane spike + strong F1; K3 flat CV; K6 heavy drain. *Red-law check:* co-location clean (beam anchored to live aim). The single best Mendeleev candidate in the lattice.

**Brief 2 — Herding Spin** (whirlwind fiber + treatment=control, function=slow/pull). *Genre-check:* every WW in the corpus is damage-pure; PoE Cyclone takes Hinder/maim only as support-gem texture. Kit-core control-spin is unoccupied. *Player consequence:* the pack comes WITH you — the spin that repositions the fight instead of just surviving it; melee crowd-authorship. *KPI prediction:* K2 F1-dense spike, control-uptime high, K1 spike vs swarm cells. *Red-law check:* clean. *Pricing law from A.2-8/gd corpses applies:* the control payload must be priced against damage-pure WW or it becomes the shadowed sibling.

**Brief 3 — Retaliation densification** (thorns; chr-thorns-templar is a minHam-5 isolate). *Genre-check:* this is a *proven family we under-sampled* — D2 Iron Maiden, D3 Invoker (a full set meta), LE Sentinel riposte. *Player consequence:* the tank whose defense IS the offense; the only archetype where getting hit is the rotation. *KPI prediction:* K4-dominant route + damage keyed to incoming events — and the premitigation/absorb accumulators needed to see it **already exist**, making this the cheapest fiber to sim-confirm. *Action:* crawl densification (elrond/legolas) + generation isotopes.

**Brief 6 (called out) — Deferred-detonation as fiber seed.** Four hades isolates share one machine: apply mark/curse → payoff detonation. That is not four gaps; that is **a fiber our corpus sampled only through one source** (Hades' boon system). D2 Corpse Explosion and PoE Bane/Impending Doom are adjacent precedents. Recommend: treat as a seventh candidate fiber (designer+recurrence proxy-confirmation), not as isolates.

## C.5 What gaps are NOT

The 33 zero-co-occurrence pairs stay **priors, not laws** — melee⊗projectile is definitional (the range coord is partly derived from delivery), but channel⊗cooldown and proxy-heavy⊗channel are design *tensions* the genre never resolved, which is exactly what a generation engine is for. Budget: one deliberate probe each, red-law and pricing-law filters attached, sim-gated. If the probe dies in the gauntlet, the prior hardens toward law at zero player cost — that is the lattice doing its job.

---

# Charge D — Direction re-assessed

⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC (+ ELICITOR for the ruling surface)

## D.1 The current bet, stated precisely

> A 13-coordinate mechanical lattice (14-slot key), populated by a curated 470-kit cross-genre corpus and extended by LLM generation, with the fight sim as the eventual family oracle (B) and lattice gaps as a discovery product, feeds a zero-hand-authored content pipeline. The demo pitch is one feel-complete 25–27-minute run (One Realm, THE DENOMINATOR); the product pitch is breadth (§20d parametric-verb condition as the breadth test). Balance is bounded viability with engineered specialization spikes; loot is kit-agnostic per gear law §3A.1.

## D.2 Six steelmen, six verdicts

**1. "Depth-over-breadth — 470 kits is a vanity number; ship 25 great ones."**
*Steelman:* every wishlist the genre ever built came from a slice that felt complete; breadth never sold a demo. *Verdict:* **PARTIALLY ABSORBED — the MVP already rules this.** The demo pitch IS the loop (25 BC-cell kits + H-series); breadth is the *product* pitch behind it. The steelman lands only as a budget discipline: breadth work is subordinate to the §20d parametric-verb condition and never competes with run-feel work for the same window. Refinement (e) below.

**2. "The coordinate model is overfit — 13 hand-chosen coords, hand-chosen bins; the lattice is a mirror of our assumptions."**
*Steelman:* FCA on your own encoding finds your own encoding. *Verdict:* **LARGELY REFUTED by this session's evidence.** The dedup near-orthogonality (470→457; flat-topped near-twin distribution, no runaway texture coord; delivery and treatment at zero near-twins) says the coords genuinely partition. The collision probes show the register separating real pairs (incinerate-vs-incinerate via #13; flicker-vs-leap-attack via #10/#11) and *correctly refusing* to separate tuning-differences (rooted-channel CONTESTED). Residuals are known and queued: #7 economy value-split (not wholesale demote), #4 geometry demotion — Stage-2 review. The register is behaving like an instrument, not a mirror.

**3. "The sim can't be the oracle — you're defining families against a measurement that doesn't exist."**
*Steelman:* the gauntlet is a ruled-broken instrument; K2 is blocked; K6 unmeasured; positional patterns invisible. *Verdict:* **PARTIALLY TRUE TODAY — and priced in.** B.5's verdict: fibers are proxy-confirmed (designer + cross-game recurrence, lifts 224–2119) until the named acceptance test passes. The family definition never depended on the oracle existing *now*; it depends on B being *definable*, which B.2 settles (differential shape at frozen tuning). The steelman becomes a milestone, not an objection.

**4. "The periodic table is vanity — players never see it."**
*Steelman:* internal taxonomy as self-indulgence. *Verdict:* **DEFUSED BY USE.** The table already earned its keep this cycle as an internal instrument: dedup (isotope collapse), curation QA (it caught the d2-sacrifice leak), trap-labeling (red laws now queryable). Its status is instrument, not player-facing promise — nothing in the MVP scope sells "68,040 cells" to a player, and nothing should. The player-visible face of the lattice is variety-that-keeps-arriving, full stop.

**5. "Gaps are a trap — empty cells are empty because they're bad; you'll ship a museum of the genre's rejects."**
*Steelman:* Mendeleev predicted elements, not viable products; the genre already ran the experiment. *Verdict:* **DEFUSED, WITH TEETH KEPT.** Charge A's amber ledger is the answer: ~two-thirds of labeled corpses died of causes our architecture removes (tuning → balance loop; itemization → agnostic loot; port-context → one coherent game). The genre's experiment was run under conditions we don't reproduce. BUT the teeth: intrinsic red laws are hard filters; CONTESTED cells carry pricing laws; and the C.2 honesty rule (out-of-corpus genre-check before any UNCLAIMED ruling) prevents museum-curation of known rejects. Gaps are ranked and cross-examined, not worshipped.

**6. "Generation is the wrong core — curate the 470, ship the best, skip the machine."**
*Steelman:* the corpus is already good; LLM generation adds variance and slop risk. *Verdict:* **DEFUSED BY COMPOSITION.** The zero-hand-authored ruling makes curation and generation one pipeline, not rivals: the corpus is the prior, generation is the sampler, the sim+laws are the filter. Shipping "the best of 470" is a licensing minefield (these are *other games' kits* — the corpus is evidence, not inventory) and abandons the only pitch that differentiates us (content that keeps arriving). The 470 were never product; they are the measurement that makes the product possible.

## D.3 The ruling

**REFINE — stay on the bet, with five bindings.** The lattice + corpus + generation + sim architecture survives its steelmen and this session's evidence strengthens it (near-orthogonal coords; a graveyard that is two-thirds amber; six fibers with real lifts; a definable B). Bind these five refinements: **(a)** B is *defined* as differential-shape at frozen reference tuning — the balanced scalar is excluded as identity signal forever, because bounded viability is engineered to destroy it; B-as-oracle is a milestone with the B.5 acceptance test, and fibers remain proxy-confirmed until it passes. **(b)** The cell taxonomy gains **CONTESTED** (corpses + survivors, tuning-separated) alongside unclaimed/graveyard/amber/forbidden; rooted-channel is its first member. **(c)** The **amber-promotion law**: graveyard cells with extrinsic deaths are *promoted generation targets* because our loop and loot are their specific antidotes; the three intrinsic red laws (co-location, no anti-synergy, movement-damage carve-out) are hard filters carried by curation/generation, not by the sim. **(d)** The elrond curation batch (A.5: truncation, d2-sacrifice, re-key 37 negatives, 5 pipeline TODOs, death-provenance tags) fires before Stage-2 coarsening concludes, so the coarsening ruling sees the corpses. **(e)** Breadth stays the product-layer pitch, permanently subordinate to the one-run feel-complete demo gate; §20d is the breadth test, cell-count is not. Nothing here pivots the architecture; everything here makes it harder to fool.

---

## Follow-ups (owners, not enactments)

| item | owner | note |
|---|---|---|
| Curation batch A.5 (5 items) | elrond | recommend before Stage-2 close |
| K6 accumulators + K1 reference-panel freeze spec | gamora (design-spec-as-math handoff from gandalf) | small seam work; unblocks B acceptance test |
| K2 / gauntlet re-base | jack-ryan metrology (already queued) | unchanged by this analysis |
| Stage-2 dedup review | gandalf + gamora + Matt (already queued) | this analysis feeds it: #4/#3 demote support, #7 value-split, movement-fusion marker consideration, CONTESTED annotations |
| Deferred-detonation fiber seed (C.4 brief 6) | gandalf | proxy-confirmation pass next design window |
| Stay/refine/pivot ruling | **Matt** | D.3 is the decision surface |

**Signed:** gandalf — SPEC-AUTHOR (A–C), DRIFT-CRITIC + ELICITOR (D) · 2026-07-13
