# Engine-vs-Demo Fight-Integrity Gap — Diagnosis (2026-05-18)

**Status:** Canonical diagnostic document. Captures a five-axis architectural gap between the engine's balance simulation, the Pixi.js demo's runtime, and the player's expectation of an ARPG combat experience. Load-bearing for Pattern-B commercial-direction dialogue (2026-05-19 morning), for any roadmap amendment that follows, and for any future "is the engine balanced?" claim.

**Authority:** Matt (playtest findings + data analysis from /encounters tab); gandalf (synthesis, code-trace verification via Explore sub-agents, genre comparator framing).

**Authored:** 2026-05-18 late afternoon, immediately after Matt's two-finding briefing + the three-question diagnostic exchange.

**Companion artifacts:**
- `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-dialogue.md` — Pattern-B agenda (amended to absorb this doc as load-bearing context)
- `agentic_orchestration/gandalf/research/arpg-fight-mechanics-database-2026-05-18.md` — comparator data across Wolcen / Dragon's Dogma 2 / Grim Dawn / Diablo 2-3-4 / PoE / Last Epoch (in flight at time of authoring)
- `agentic_orchestration/gandalf/research/arpg-gap-analysis-2026-05-18.md` — per-axis gap + commercial-path cost analysis (in flight)

---

## § 0 — TL;DR

**Three surfaces. Three games. None of them is the same game as the other two.**

| Surface | Spatial substrate | What it measures |
|---|---|---|
| Engine balance simulation | 1D scalar distance + 1v1 PackProxy | Aggregate win-rate across 12 sequential 1v1 fights, mean-weighted |
| Pixi.js demo runtime | 2D pixel-space, **no** entity-to-entity collision, **no** leash | What the player sees on screen |
| Player expectation (ARPG genre) | 2D top-down or 2.5D isometric, **hard** entity collision, leash + aggro-radius, **per-skill range** | What the genre has trained the player to expect |

The engine produces a "balanced" claim that is **mathematically true at its own level** and **operationally misleading** at every other level. Five concrete axes drive the divergence. Two playtest findings + one /encounters-tab data finding triggered the diagnosis. Five recommended workstreams (R1–R5) follow.

**The single sentence:** *the engine is balancing the wrong game.*

---

## § 1 — Why this doc exists

### § 1.1 — Two playtest findings (Matt, 2026-05-18)

**Finding A — Bosses and minibosses are unbeatable.**

> "Highest WR I think is 45% for any class on miniboss and sub-20% on boss; mean WR lower than that. Playtest confirms this in the current seasons. I only beat the miniboss with one class (I think lightning caster) and I could not beat the boss with any classes."

The /encounters tab data corroborates: across the shipped 5 seasons, miniboss WR caps at ~45% for the strongest class-matchups; boss WR for most classes is sub-20%; mean across all classes is lower than the cap. **No class reliably beats the act boss.** Playtest is even harsher than data: Matt has personally beaten the miniboss with exactly one class across all play (lightning caster); zero classes for the act boss.

**Finding B — Pack/swarm handling is broken on both surfaces.**

> "Gauntlet sim uses a modified single entity which is set to match the statistics of a pack (in place of an actual pack)... (1) the AI of these combatants is set to constantly run away, (2) the geospatial setting of the demo have the enemy combatants clump up sometimes 8-10 combatants overlapping on a single pixel."

This is two distinct failures braided into one observation: the engine never sees a real pack (it sees a single PackProxy with N×HP), and the demo sees a pack that has no spatial substrate to spread on (no collision, no separation).

### § 1.2 — Three diagnostic questions (Matt, 2026-05-18 — answered inline)

> Q: Why are mobs "constantly running away" — is the demo AI reading from engine JSON or is it hardcoded?

**A: Hardcoded in TypeScript constants; not reading from JSON.** The demo's `world/movement.ts:74-81` defines `PREFERRED_RANGE: { close: 90, medium: 420, long: 660 }` and `KITE_TRIGGER: 300` as **demo-side constants**. Long-range enemies retreat the instant the player gets within 300px — which describes the majority of generated content. The reverse-running observation is the kite mechanic firing too aggressively, not a sign error. The engine has no opinion on this; the demo is alone.

> Q: Do ARPGs treat pack stacking as acceptable, or do they enforce separation?

**A: Hard entity collision is genre-canonical. Demo violates it.** Diablo 2/3/4, Path of Exile, Grim Dawn, Wolcen, Last Epoch — all enforce entity↔entity collision (hard or soft-via-separation-forces). Eight mobs do not pile on one pixel in any shipped ARPG. The demo has zero collision/separation logic — `world/movement.ts:197-199` explicitly defers it ("Repulsion forces can be added here if overlap looks bad at future playtests — not added speculatively"). The "future playtest" has happened; the speculative deferral is now a confirmed defect.

> Q: What is the standard ARPG AI pattern?

**A: Behavior-tree or finite-state-machine with idle / approach / attack / reposition states. Pack behavior is EMERGENT from collision + targeting, not scripted. Constant-flee is NOT a canonical AI pattern.** Genre standard: melee mobs approach to attack-range and swing on cooldown; ranged mobs hold at preferred range and shoot, kite only when threatened; bosses run scripted skill rotations with telegraphed wind-ups. Reincarnated's "long" range_profile is over-applied to too many enemy archetypes, producing an unintended permanent-kite default that no genre comparator exhibits.

### § 1.3 — Three independent AI implementations (architectural finding)

While verifying the questions above, the audit confirmed a deeper structural issue: **there are three decoupled AI implementations governing the same fight.**

1. **Engine simulation AI** (`reincarnated-engine/src/reincarnated/simulation/ai_strategies.py` + `fight_engine.py`) — Python, priority-rotation, 3-band scalar distance.
2. **Demo runtime AI** (`reincarnated-demo/src/world/aggro.ts` + `world/movement.ts`) — TypeScript, FSM-ish, 2D pixel positions, hardcoded range constants.
3. **Implicit balance-loop AI assumption** (`reincarnated-engine/src/reincarnated/simulation/balance_loop.py`) — what the gauntlet THINKS the player and monster will do, which drives convergence targets.

These three implementations share no source of truth. The engine and demo do not negotiate. Per-mob behavior cannot be tuned in one place. **This is the architectural enabler of the gap.** Without unification, fixes to any one of the five axes below will drift back out of sync with the others.

---

## § 2 — The five axes of the gap

### § 2.1 — Axis 1: PackProxy collapses N-entity attrition dynamics

**Current state.** The engine's gauntlet (`balance_loop.py:269-275`) is a 12-fight sequence composed `{swarm: 6, magic: 2, elite: 2, mini-boss: 1, boss: 1}`. Each "swarm" slot is **not** an 8-mob pack — it is a **PackProxy**: a single proxy entity with `HP = 8 × per-individual_HP`, where AOE geometries deal `damage × 8` against it (`damage_resolver.py:204, 235`).

**What this models well.** The aggregate damage exchange between an AOE-capable kit and a high-HP target. Pretty good for "does fire wizard have enough sustained AOE to clear waves of trash."

**What this misses.**
- **Death-attrition momentum.** Killing 4 of 8 mobs in a real pack reduces incoming damage by 50%. The PackProxy HP pool just shrinks; incoming damage stays constant until it's dead. No "I'm winning" feedback inflection.
- **Focus-fire dynamics.** Single-target burst on real packs lets a player triage threats (kill the healer, kill the ranged, kill the elite first). The proxy makes every swarm fight a generic HP race.
- **Crowd-control geometry.** A real root or chill on one mob in a pack of 8 lets the other 7 keep advancing. CC on a proxy = all-or-nothing.
- **Overkill waste.** AOE in real ARPGs frequently overkills the front-line and underdamages the back-line. The proxy doesn't model this; AOE is monotonically more efficient than it would be in reality.
- **Positioning** — see § 2.3.

**Severity.** Medium for trash, **severe** for the boss-with-adds pattern that every modern ARPG uses for elite/miniboss encounters. The engine literally cannot model a fight where the boss is at one position and three adds are at another.

### § 2.2 — Axis 2: Aggregate WR convergence hides per-tier failure

**Current state.** `balance_loop.py:1907-1936` converges on a single aggregate target: the **mean win-rate** across the 12-opponent gauntlet. No per-tier WR thresholds exist. There is no signal that fires when any *single tier* falls below an acceptable floor.

**Worked example that explains Matt's playtest finding.** A class can pass the gauntlet with mean WR ≈ 50% while having:

| Tier | Slots | Per-tier WR | Weighted contribution |
|---|---|---|---|
| Swarm (PackProxy) | 6 | 0.80 | 4.80 |
| Magic | 2 | 0.65 | 1.30 |
| Elite | 2 | 0.55 | 1.10 |
| Mini-boss | 1 | 0.30 | 0.30 |
| **Boss** | **1** | **0.15** | **0.15** |
| **Mean** | **12** | — | **0.622 (PASS at 0.50 target)** |

The AOE-strong class clears swarms easily, struggles on boss, and the gauntlet rates it **balanced**. The player rates it **boss-unwinnable**. Both are correct measurements of different questions.

**What this misses.** The genre's actual balance contract is **per-tier**, not aggregate. Diablo 2 tuned Baal separately from cows. PoE tunes Maven separately from Hillock. Grim Dawn tunes Ravager separately from Cronley's Gang. Every modern ARPG treats per-tier balance as the primary contract. We do not.

**Severity.** **Severe.** This is the most operationally consequential gap. Right now we ship "balanced" classes that fail every act-boss encounter, and the balance system reports green.

### § 2.3 — Axis 3: Dimensional mismatch (1D engine / 2D no-collision demo / 2D-with-collision player expectation)

**Current state.**

| Surface | Position type | Collision | Separation |
|---|---|---|---|
| Engine sim | Scalar `distance_m` between two combatants (`fight_engine.py:155`); 3-band state machine (CLOSE ≤1.5m, MID 1.5–12m, FAR ≥12m) | N/A (no concept of space) | N/A |
| Demo runtime | Vector `(x, y)` per entity | **None** (`world/movement.ts:197-199` deferred) | **None** |
| Genre expectation (Diablo/PoE/Grim Dawn/etc.) | Vector `(x, y)` per entity | Hard entity↔entity collision | Boid-style separation or hard-stop |

**What this means in practice.**
- The engine can't conceive of "two mobs occupying space near each other," because the engine doesn't have space.
- The demo can conceive of position but lets every entity occupy the same point as every other entity.
- The player expects mobs to spread, surround, flank — none of which any surface delivers.

**Why neither side maps to "collision" as a concept.** Matt asked: is the gauntlet using hard / soft / no collision? **The answer is: none of the above. There is no spatial substrate at all.** Distance is a single scalar between exactly two combatants. The 8 mobs in a swarm fight are mathematically pooled into one proxy; they're not "in space" either spread or stacked. Collision is not abstracted as pass-through — the question doesn't apply because there's only ever one opponent in the engagement state.

**What this misses.**
- **Pack flanking.** Real ARPG packs surround the player. The geometry of being surrounded changes everything (escape vector, AOE coverage, kite viability).
- **Chokepoint exploitation.** Pulling mobs into doorways is a core ARPG skill. Engine can't model it; demo doesn't reward it (mobs just stack inside the doorway).
- **Boss-with-adds spatial reading.** Aggro the adds first or fight the boss while adds chip you? Real ARPG decision; neither surface presents the choice.
- **AOE shape mattering.** A cone, a circle, a line, and a chain hitting a spread pack do dramatically different things. Engine collapses them to a damage-multiplier. Demo stacks the pack so all four shapes hit identically.

**Severity.** **Severe** for the gauntlet (it cannot test the dimension at all). **Severe** for the demo (visible defect in playtest). Genre baseline absent on both surfaces.

### § 2.4 — Axis 4: Range is not a design lever

**Current state.** The engine has exactly one range gate: the binary `at_melee_range` flag, true when `distance_m ≤ CLOSE_THRESHOLD (1.5m)`, gating MELEE_GEOMETRIES (`fight_engine.py:161`, `damage_resolver.py`'s MELEE_GEOMETRIES check). One soft band cutoff at MID_THRESHOLD (12m) ends actions. That's it.

**What this means concretely.**
- A "ranged_physical" skill works at 2m, 5m, 11m identically. There is no per-skill range data; the catalogue doesn't carry it.
- A skill cannot "miss because the target is too far" except by being in the FAR band, which is universal across all skills.
- A player cannot **out-range** an enemy. There is no "I have 12m, you have 8m, I can shoot you outside your attack range."
- A player cannot **disengage**. The fight runs to 0 HP. The FAR band auto-converges back to MID (`fight_engine.py:313-318`); the monster always advances.
- The demo also has no per-skill range, no leash, no aggro-radius reset.

**What every comparator does.** Per-skill range in published tooltips is **genre baseline** since Diablo II (2000). Build-stat range modifiers (PoE "Increased AoE", Grim Dawn "+Radius", D4 "Ranged Damage > 11 yards") are standard. Leash + aggro-radius + outrun + LOS-break are all canonical disengagement tools. The implicit contract in 2026 is: **"I can choose my engagement range. I can run away. I can be out-ranged."** We meet none of it.

**Severity.** **Severe.** This is the dimension Matt's intuition surfaced unprompted: "I am fairly sure it is a global skill damage feature as I recall being able to avoid monsters by running away from them." Correct intuition; we are missing the dimension on both surfaces.

### § 2.5 — Axis 5: Three decoupled AI implementations (the unifying frame)

**Current state.** Restated from § 1.3: three AI codebases (engine sim Python, demo runtime TypeScript, balance-loop implicit) share no source of truth. The engine sim assumes "scripted priority rotation"; the demo runtime applies hardcoded TS range constants; the balance loop computes win-rate convergence based on engine-sim behavior that the demo doesn't replicate.

**Why this is its own axis, not just a derived problem.** Even if we fix Axes 1–4 in either surface, the divergence persists until the AI is unified. A boss balanced in the engine with per-tier WR targets, spatial substrate, and per-skill range — still won't feel that way in the demo if the demo runs different AI. The unification is the architectural prerequisite for any of the fixes landing in the player's lap.

**Severity.** **Architecturally load-bearing.** Without resolving this axis, fixes to other axes drift back out of sync over time. The hive will quietly grow the gap back to its current size.

---

## § 3 — Proposed correction shape

Matt's framing during the diagnostic exchange:

> "If we did use a 2D space gauntlet, we would need at least one large room to ensure this is a feature of a skill (player can run away from some monsters)."

This is the right scoping move. **Not** "rewrite the gauntlet as a full 2D combat sim across all 12 fights." That's expensive and most of the gauntlet's 1v1 stat-baseline work doesn't need it. The correct shape is **two layers**:

### § 3.1 — Layer 1: keep the 1D scalar gauntlet for stat-baseline iteration

The existing PackProxy + 3-band-distance gauntlet stays. It's fast, it's well-validated for the question it answers ("are the damage numbers in the right ballpark?"), it converges quickly during balance loop iterations. Most kit-tuning questions live here. Don't throw it away.

### § 3.2 — Layer 2: spatial sub-gauntlet — open-arena 2D test surface

Add a smaller 2D sub-gauntlet that runs 3–5 spatial scenarios per class and specifically exercises:

| Dimension | Requirement |
|---|---|
| Arena size | Large enough for run-away to matter — recommended floor 30m × 30m, with a 50m × 50m "open arena" preset |
| Aggro radius | Per-mob configurable; engine-emitted; default scaled by threat_tier |
| Leash distance + reset-on-leash | Per-mob configurable; if exceeded, mob returns to spawn and recovers |
| Per-skill range | Real check: target outside range = skill cannot fire; this requires per-skill range data on every skill in the catalogue |
| Spatial AOE coverage | Skill footprint geometry actually queried against mob positions; count how many of N mobs are inside the radius/cone/line |
| Disengage-as-strategy | Player AI can choose "retreat to leash" as a valid action, not just fight-to-death |
| Entity↔entity collision | Real (hard or soft-via-separation); 8 mobs do not pile on one point |
| Boss-with-adds composition | At least one scenario per class tests the boss-tier with 2–4 adds at non-boss positions |
| Spatial CC | Root/chill/stun affect single mob's mobility, not all-or-nothing on the pack |

This is the test surface that **forces the boss/miniboss WR failure into the metric**, because aggregate-mean-of-12 can't mask it anymore — the spatial fights expose the geometry truth.

### § 3.3 — Layer 2 demo parity — what the player surface needs

The demo needs the same dimensions to actually deliver the spatial fight to the player:

- Entity↔entity separation (soft via push-apart force at ≤ small radius; or hard via collision body)
- Aggro radius + leash + reset-on-leash
- Per-skill range as a real check (skill cannot fire if target out of range; or fires but misses)
- Range_profile distribution review — the over-applied "long" profile causing the constant-flee artifact gets re-distributed across approach / engage / kite profiles
- AI behavior tree or proper FSM with `idle → approach → attack → reposition` states (not the current always-kite-if-long pattern)

### § 3.4 — Architectural prerequisite — unify the AI source of truth

Before either layer can ship reliably, the three AI implementations must share a contract. Options:

- **Option A.** Engine emits monster-AI behavior fields in monster JSON (preferred behavior, telegraph windows, aggro radius, leash distance, skill rotation, range profile). Demo reads them. Engine sim uses the same fields. **Single source of truth: the catalogue.**
- **Option B.** A shared AI specification document drives separate-but-mirror implementations on both sides, with a parity test that fails when they diverge.
- **Option C.** Defer parity; declare the demo is "Phase 0 visualization," not authoritative; document the divergence. **Cheapest, weakest.**

Recommended: **Option A**. Cost is real (schema migration across all shipped seasons, AI consumption code on both sides) but it's the only option that doesn't accumulate drift over time.

---

## § 4 — Roadmap impact

This is **not a quick patch**. It's roadmap-shape work. Rough sizing (gandalf-level — gamora + star-lord will firm up numbers when scoped):

### § 4.1 — Five recommended workstreams (R1–R5)

These are recommendations to knight-rider for formal roadmap amendment per ADR-002. They are gated by the Pattern-B direction commit (§ 5).

| Ref | Workstream | Primary owner | Rough size |
|---|---|---|---|
| **R1** | Per-tier WR balance targets in the gauntlet (per-tier convergence targets replacing/augmenting aggregate mean) | gamora | 1–2 weeks |
| **R2** | Spatial sub-gauntlet (open-arena 2D test surface, per-mob aggro/leash, real spatial AOE coverage) | gamora + star-lord (telemetry emission) | 3–5 weeks |
| **R3** | AI specification fields in monster JSON (preferred behavior, telegraph window, aggro radius, leash, skill rotation, range profile) + per-skill range data on every skill in the catalogue + schema migration across 5 shipped seasons | rocket (schema + catalogue), star-lord (telemetry/export), elrond (migration tooling) | 2–4 weeks |
| **R4** | Demo collision/separation system + leash/aggro-radius + per-skill range check + range_profile redistribution | drax | 2–3 weeks |
| **R5** | Demo AI parity audit + range_profile redistribution + fix over-applied "long" profile causing constant-flee artifact | drax | 1 week |

**Total nominal:** 9–15 dev-weeks of work, depending on parallelism. **Not insertable into Track B.5.** This is its own track (provisional name: **Track F — Fight Integrity**).

### § 4.2 — Ordering

`R1 → R3 → (R2 + R4 + R5 in parallel)` is the natural critical path. R1 is cheap and reveals the failure in metric (validates the diagnosis empirically). R3 is the schema prerequisite for R2, R4, R5. Once R3 lands, R2/R4/R5 can parallelize across gamora/drax/star-lord.

### § 4.3 — Risk

The largest non-obvious risk: **R1 alone will likely produce a balance regression cascade.** Once per-tier targets exist, the current "balanced" class pool will fail boss thresholds across the board, and the balance loop will demand re-tuning every class against the new contract. This is *correct* — that's what the metric exists to do — but Matt should expect a multi-week class-retuning sprint *immediately following* R1 ship, before R2 even starts. Sequencing R1 separately from R2/R3 lets that sprint happen in cleaner isolation.

---

## § 5 — Commercial-path implications (Pattern-B input)

The fight-integrity gap **re-prices each of the three commercial paths** identified in `canonical/story/apex-director-debrief-2026-05-18.md`. Pattern-B tomorrow morning must absorb this re-pricing in its Q1 (direction commit) and Q4 (engineering scope) deliberations.

### § 5.1 — Path A: Standalone Reincarnated-the-game

**Path A is the highest-cost path under this gap.** A standalone ARPG that violates per-skill range, lacks entity collision, has aggregate-only balance targets, and ships unbeatable bosses **will be rejected by the genre audience**. There is no version of "standalone Reincarnated" that ships in a viable state without closing the gap on at least Axes 1, 2, 4. Axis 3 (spatial substrate in the demo) is also non-negotiable for player feel. Axis 5 (AI unification) is required to keep the fixes durable.

**Implication:** Path A requires the full Track F (~9–15 dev-weeks) AND a multi-week class-retuning sprint AND the existing Phase-1 P1 commitments. Realistic ship horizon under Path A is **shifted right by 2–4 months minimum**.

### § 5.2 — Path B: Mod-first into Wolcen / Dragon's Dogma 2 / Grim Dawn

**Path B partially solves Axes 1, 2, 3 for free, because the host game already has spatial combat, real collision, real range.** What Path B requires from Reincarnated is:

- Per-skill range data emitted from the engine (R3 partial — schema work) so host-game can place skills in its range system
- Per-skill geometry footprint (cone/circle/line/chain) emitted explicitly so host-game can render correctly
- AI behavior fields in the format the host game expects (translation layer per target)
- Per-tier balance targets in the engine (R1) so the content we hand to the host isn't pre-broken by aggregate-WR masking

**Implication:** Path B's engine-side work is approximately **R1 + a subset of R3**, **without R2, R4, R5**. That is dramatically cheaper — maybe 3–5 dev-weeks vs. 9–15 — because the host game absorbs the spatial substrate work. **This is the path most made cheaper by the gap diagnosis.**

Of the three Director-named targets:
- **Grim Dawn** — strongest precedent (Asset Manager, Database Editor, Steam Workshop, total-conversion mods like Grimarillion exist); host engine is well-documented; modding community is alive
- **Wolcen** — viable; less mature modding scene than GD; range/collision native to engine
- **Dragon's Dogma 2** — different sub-genre (action-RPG vs looter-ARPG); RE Engine modding is mostly cosmetic; **fit is weakest**

(Comparator deep-dives in flight; see `arpg-fight-mechanics-database-2026-05-18.md`.)

### § 5.3 — Path C: Engine-as-tool / B2B SaaS

**Path C cost depends on the buyer's substrate.** If the buyer's game is a spatial ARPG, Path C inherits Path A's requirements (full Track F). If the buyer's game is auto-battler / idle / strategic-layer, Path C may need only Axes 1, 2 (and skip Axes 3, 4) because the buyer doesn't model space anyway.

**Implication:** Path C cost is bimodal — either ~3–5 weeks (auto-battler buyer) or ~9–15 weeks (ARPG buyer). The Director's "cement-deep-season → live-ops-tool" framing tilts toward auto-battler-or-similar buyers, which is the cheaper end. But this needs validation per actual buyer profile.

### § 5.4 — Cross-path summary

| Path | Track-F cost | Why |
|---|---|---|
| A (standalone) | **Full** (~9–15 wk) | Must close all five axes to ship a genre-credible standalone |
| B (mod-first) | **Partial** (~3–5 wk) | Host game absorbs spatial substrate; we ship R1 + schema work |
| C (engine-as-tool) | **Bimodal** (~3–5 wk OR ~9–15 wk) | Depends on buyer's substrate |

**Pattern-B implication:** The gap doesn't change which path is best, but it **dramatically widens the cost spread between paths**. Path B becomes more attractive specifically because the host games solve our hardest architectural problem for us.

---

## § 6 — What this doc does NOT claim

- **Not** that the engine is broken or worthless. The engine is **correctly solving the wrong problem.** The 1D scalar gauntlet is a perfectly good answer to "what damage numbers are in the right ballpark"; it is a poor answer to "what will the player feel."
- **Not** that the demo is unfixable. The collision/leash/range_profile fixes are real but scoped.
- **Not** that the gap is anyone's fault. PackProxy was a deliberate B10.2 simplification with good reasons; the 1D scalar distance was a deliberate Gate-3b simplification with good reasons. Both were correct at the time. The gap is what happens when good simplifications accumulate without an architecture check.
- **Not** that the recommended workstreams (R1–R5) are pre-approved. They are recommendations to knight-rider for formal roadmap amendment. Matt's Pattern-B direction commit gates whether they ship in this form, a reduced form, or not at all.
- **Not** that the gap requires immediate fix. It is **strategically load-bearing** — Pattern-B tomorrow needs to weigh it. But "defer Track F until after [milestone X]" is a valid Pattern-B output as long as it's done with eyes open.

---

## § 7 — Open questions surfaced (queued for Pattern-B and beyond)

These are questions the gap surfaces that need answers but are not pre-answered here:

1. **Per-tier WR target floors** — what are the right WR floors per tier? Boss 35%? 40%? 45%? Diablo II's stated design philosophy was "elite content should pass on ~30% of attempts for a build that beats it." Reincarnated's answer needs to be set by Matt, not derived mechanically.
2. **Aggro radius / leash distance defaults** — what scales these per threat_tier? Per substrate? Per season?
3. **Per-skill range data — backfill strategy** — do we re-derive range from skill geometry on the existing catalogue, or do we re-roll skills with range as a generation-time field? Either path is non-trivial.
4. **Demo collision soft-vs-hard choice** — hard collision is more genre-faithful but harder to retrofit into Pixi.js entity model; soft separation is easier and visually adequate. Which?
5. **AI unification — Option A vs. B vs. C** — preferred Option A (catalogue as source of truth) but the schema migration cost is real.
6. **Pattern-B direction commit** — Path A, B, C, or combination? § 5 makes the case that Path B is uniquely advantaged by the gap; this should be in tomorrow's deliberation.

---

## § 8 — What comes next

**Tonight (this session):**
- This canonical doc filed (✓ on completion).
- Pattern-B open-thread amended to absorb this doc as load-bearing context.
- ARPG fight-mechanics research database authored (in flight via 4 parallel Legolas Mode-A agents).
- Per-axis gap analysis vs. comparator landscape authored (after research returns).
- Next-session handoff doc filed.

**Tomorrow morning (Pattern-B session):**
- Matt opens gandalf session; Pattern-B fires.
- This doc + the database + the gap analysis are the load-bearing context for Q1 (direction commit) and Q4 (engineering scope).
- Direction commit gates whether R1–R5 ship as Track F.

**Following the Pattern-B direction commit:**
- knight-rider routes the roadmap amendment recommendation per ADR-002.
- gamora / drax / rocket / star-lord receive sprint dispatches in path-appropriate sequence.
- The class-retuning sprint sequencing decision happens before R1 ships, not after.

---

*Filed 2026-05-18 late afternoon by gandalf. The gap is named; the gap is mapped; the gap is priced. Five axes, five workstreams, three commercial paths re-weighed. Tomorrow the road forks — and now we know what each road costs. Mithrandir signs.*
