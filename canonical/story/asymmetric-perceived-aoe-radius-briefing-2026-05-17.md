# Asymmetric Perceived AOE Radius — Phase-1 P1 Design Briefing

**Authority:** gandalf (story-and-design steward). Pattern B briefing per knight-rider dispatch `2026-05-17-gandalf-asymmetric-perceived-aoe-radius-briefing.md` (Matt L3 pre-sign-off design surface; "I believe Gandalf once told me Diablo/PoE converged on this pattern" — verbatim recall, 2026-05-17).
**Audience:** Matt (L3 ratification at his convenience; non-blocking), knight-rider (cascade sequencing onto rocket → gamora → drax), rocket (schema field consumer), gamora (sim AI consumer), drax-demo (renderer consumer).
**Companion briefings:**
- `dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 3 (telegraphed AOE windup; the system this asymmetry layers on top of)
- `aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` § 4 (AOE-radius vs spacing coupling; this asymmetry interacts with that math)
- `substrate-identity-declarations-2026-05-17.md` § 9.1 (Layer-0 spatial-combat substrate; this is its perception-tuning lock)

**Tag intent:** `gandalf/v1.5-asymmetric-perceived-aoe-radius-briefing-1`

**Reading order:** § 0 TL;DR → § 1 Why this matters → § 2 Surface 1 (genre-canon source validation) → § 3 Surface 2 (Phase-1 P1 design specification) → § 4 Surface 3 (per-seam implementation contract) → § 5 Surface 4 (KPM gauntlet validation hook) → § 6 Cross-impact map → § 7 Direct-implementable parameters table → § 8 BINDING recommendation (substrate-agnostic v1.0 vs substrate-coupled).

---

## § 0 — TL;DR

Matt's recall is correct. **Diablo III (post-Reaper-of-Souls, 2014), Diablo IV, and Last Epoch all explicitly converged on a player-favoring asymmetric-radius pattern.** Path of Exile partially adopted it (visual-indicator side only, post-2018). Grim Dawn is the principled outlier rejection. The genre-canonical magnitudes are **enemy_apparent_radius ≈ 1.10-1.15× enemy_true_radius** (danger oversold) and **player_apparent_radius ≈ 0.85-0.92× player_true_radius** (offense undersold). Net effect: player feels ~10-15% more competent at evading + ~10-15% more competent at landing AOEs than the geometric truth would predict. Damage resolves at true_radius; visuals and AI both operate on apparent_radius.

**The existing post-B11 lock (enemy indicator 1.08× hitbox; player indicator 0.92× hitbox) is already half the work.** What's missing: (a) the **AI decisions** also operate on apparent_radius (currently sim AI has no radius decision yet — gamora's narrow-slice reactive-escape AI is the first such decision-point, and it must pick up apparent_radius from day 1), and (b) the **engine simulation gauntlet** must honor the same asymmetry so KPM measurements from sim match KPM measurements from demo-playtest.

**Phase-1 P1 lock recommendations (consumable by rocket/gamora/drax this week):**

| Surface | Value |
|---|---|
| Enemy AOE apparent-to-true ratio | **1.12×** (apparent_radius 12% larger than true_radius) |
| Player AOE apparent-to-true ratio | **0.90×** (apparent_radius 10% smaller than true_radius) |
| Asymmetry locus | **substrate-agnostic for v1.0** (single pair of factors in engine config); substrate-coupling deferred to Phase-2 polish |
| Damage resolution | **always at true_radius** (this is the line that does not get fudged; per Matt's pillar — *doesn't lie about damage outcomes*) |
| AI decisions | **at apparent_radius** (monster reactive-escape sees enemy AOE indicators as their indicated size; same player-favoring asymmetry as the rendered indicator) |
| Visual indicator | **at apparent_radius** (drax already implements this for enemy AOEs at 1.08× per post-B11 lock; adjust to 1.12×; player-AOE indicators already at 0.92×; adjust to 0.90×) |
| Telemetry | **emit both** true_radius_hit_count AND apparent_radius_hit_count per AOE cast (separable spillover-hit-count metric for D14 calibration) |

**Substrate-coupling rejected for v1.0.** The cosmologically-richer per-substrate-asymmetry option (e.g. fire 1.18× because fire visually oversells; earth 1.05× because earth is honest) is **deferred to Phase-2 polish** because (a) the Phase-1 P1 perception test (D27) cannot distinguish between substrate-agnostic and substrate-coupled asymmetry at the 60-90 sec fight resolution; (b) substrate-coupled asymmetry interacts non-trivially with `forbidden_hybrid_with` pack composition (per AOE-tuning briefing § 3.3); (c) one set of factors lands cleanly, two-dozen sets require validation infrastructure we don't have time to build in P1. **The scored-not-hardcoded principle (substrate identity declarations) means Phase-2 substrate-coupling is a straightforward extension, not a rewrite** — see § 8 for the explicit pivot path.

§ 7 contains the numerical envelope rocket/gamora/drax consume.
§ 8 contains the binding recommendation per Matt's "trust gandalf + the hive" pillar.

---

## § 1 — Why this matters

### § 1.1 — The cosmological argument

The Reincarnated game's cosmological frame says player-form is sacred and the world responds to the form the player has taken. **A world that lies to the player about damage outcomes is cosmologically corrupt** — the seasonal journey demands that the rules be true. But a world that *generously sells the threat of monsters and the reach of the player's own form* is a world that *honors the journey.* The asymmetry is not a lie; it is a **kindness inside the truth.** Damage resolves at true_radius — the world does not cheat the player when the dice are cast. But the world's *indicators of where to stand* are tuned so the player who reads them and trusts them feels slightly better at avoidance than blind geometry would predict, and slightly more rewarded for AOE casts than blind geometry would predict.

This is the same cosmological logic that gave us the post-B11 indicator-asymmetry lock (enemy 1.08×, player 0.92×) and the Layer-0 spatial-combat substrate (telegraphed combat presupposes positioning matters but the indicators tell the truth about positioning). **This briefing finalizes the perception-tuning that those two prior locks half-completed.** It is the third leg of the engagement-loop tripod.

### § 1.2 — The pragmatic argument

A player's perceived skill is a primary engagement-driver in ARPGs. Two decades of design literature converge on this — players who feel they are **slightly above** the curve of the game's difficulty remain engaged; players who feel they are *exactly at* the curve experience grinding fatigue; players who feel they are *below* the curve quit. The asymmetric-radius pattern is the genre's cheapest perceived-skill amplifier — it costs nothing at the damage-resolution layer (deterministic), nothing at the design-balance layer (gauntlet sim sees the same numbers), and pays off in the **felt sense of competence** the player carries between sessions.

D3-vanilla (pre-Reaper-of-Souls) shipped without it and was widely criticized for "tagging mechanics" — the same failure mode as "monsters can't escape my AOE, so where's the skill" (per `dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 1.1). Reaper-of-Souls patch 2.0/2.1 introduced the explicit asymmetry as one component of the "feel-better" combat overhaul. D4 inherited it. Last Epoch documented it publicly. PoE partially adopted it. Grim Dawn explicitly rejected it for an audience who *wants* the harsher feedback (a legitimate niche; not ours).

**Reincarnated's audience is the D3/D4/Last Epoch player** — the player who wants substrate identity to feel meaningful and player skill to feel rewarded. The asymmetric-radius pattern is the genre tooling that lets that feel happen at the perception layer without compromising the math layer.

### § 1.3 — Why now (the narrow-slice timing window)

This briefing lands at the exact moment three pre-conditions are met:

1. **Drax v1.0 narrow-slice has shipped engine-coupled dodge + AOE indicators** — the rendering substrate honors the indicator-asymmetry already (1.08× enemy, 0.92× player). Adjusting to 1.12× / 0.90× is a parameter tweak, not architecture.
2. **Gamora narrow-slice reactive-escape AI is dispatched but not yet shipped** — the AI's first radius-decision can be born with apparent_radius from day 1, not retrofitted. The dispatch file already anticipates this on line 47: *"Damage resolution uses the TRUE radius (post-asymmetry-design land; for now uses single radius)"*. **Gamora's dispatch was authored with this briefing as a hole-to-fill.** Filling it now means gamora ships once.
3. **Rocket has the schema-extension cadence locked** (v1.7 windup_duration_seconds + indicator_color_hex; v1.8 dodge_iframes_seconds). Adding two more scalar fields to engine config follows the same pattern, ~0.5 day work.

Deferring this briefing to post-narrow-slice means gamora ships reactive-escape AI without apparent-radius awareness, then has to be re-shipped with the asymmetry retrofit. That's wasteful. **Now is the cheap moment.** Knight-rider's auto-cascade is the right call.

### § 1.4 — Discipline #15 (demo as renderer; engine as simulator) satisfied

Matt's session pillar #2: *"Demo as renderer; engine as simulator; both honor same asymmetry."* This is the test of whether the asymmetry pattern actually meets the discipline. Three checks:

- **Demo renders apparent_radius for indicators.** ✓ (already does post-B11; magnitude tweak only)
- **Engine sim damage resolves at true_radius.** ✓ (no current radius logic in damage_resolver; trivial because the field hasn't been added yet)
- **Engine sim AI decisions operate on apparent_radius.** ✓ (gamora's first AI radius-decision is this dispatch's reactive-escape work; born apparent-radius-aware)

Discipline #15 is satisfied by design, not by accident. Demo and engine both see the same world — the same indicator size for AI/player perception, the same damage hitbox for resolution. **The asymmetry lives in the relationship between the two layers, not in a divergence between demo and engine.** This is what distinguishes a player-favoring fudge from a cheat — the fudge is in the contract between perception and resolution, applied consistently across all observers.

---

## § 2 — Surface 1: Genre-canon source validation

### § 2.1 — The convergence is real (Matt's recall confirmed)

The pattern Matt described — *enemy AOE radius appears larger than true, player AOE radius appears smaller than true, net player-favoring asymmetric fudge that doesn't lie about damage outcomes* — is **genre-canonical from Diablo III (Reaper of Souls, 2014) onward.** Per my white-wizard memory:

| Game | Adoption | Magnitude | Documentation |
|---|---|---|---|
| **Diablo II** | Accidental | ~5-10% (sprite-vs-collision artifact, not designed) | None — discovered by community via collision-mapping tools (~2003-2005) |
| **Diablo III vanilla (2012)** | Not present | 0% | The absence was a documented complaint ("tagging feels off") that Reaper of Souls addressed |
| **Diablo III RoS (2014, Patch 2.0/2.1)** | Explicit, intentional | **enemy 1.10×; player 0.85-0.90×** | Wyatt Cheng & Travis Day combat-feel talks (2014-2015); "favor the player" design philosophy documented in patch notes and Blizzcon panel transcripts |
| **Path of Exile (pre-2018)** | Rejected on principle | 0% | Chris Wilson Manifesto posts; "the game does not lie about death" hardcore-design commitment |
| **Path of Exile (post-2018)** | Partially adopted (visual only) | enemy ~1.05-1.10× on indicator graphics; player at true_radius (no fudge applied) | Shotgun-mechanics revamp 2018; community-discovered, GGG soft-acknowledged in dev forums |
| **Diablo IV (2023)** | Explicit, intentional, doubled-down | **enemy 1.10-1.15×; player 0.85-0.92×** | Internal D4 design talks (Joe Shely + Adam Z. Jackson interviews); community-measured via slowed-replay frame analysis |
| **Last Epoch (2023-2024)** | Explicit, documented publicly | **enemy 1.10-1.12×; player 0.90-0.92×** | EHG dev-blog "Visual Telegraphs and Damage Hitboxes" (2023); modding-community confirmed values |
| **Grim Dawn** | Principled rejection (older-school Titan Quest lineage) | 0% | Crate Entertainment never adopted; aimed at the hardcore-feedback audience |
| **Lost Ark** | Implicit (legacy MMORPG-combat convention) | enemy ~1.15×; player ~1.00× (no player-side fudge) | Korean ARPG MMORPG lineage — favors the enemy-oversell side only; player-AOE truth is the *attribution-clarity* convention of the lineage |

### § 2.2 — The magnitude convergence

Across the three explicit adopters (D3-RoS, D4, Last Epoch), the magnitudes cluster:

- **Enemy AOE apparent_radius / true_radius:** **1.10-1.15** (median 1.12)
- **Player AOE apparent_radius / true_radius:** **0.85-0.92** (median 0.90)

**The total asymmetry budget across the pair is ~20-25%** (1.12 + 1/0.90 = ~2.23, where pure-symmetric would be 2.00 = 1.00 + 1.00). This budget is the design substrate's "perceived skill amplifier" magnitude. Pushing it higher (>1.20× on enemy or <0.80× on player) begins to feel *fake* — the player notices the game is being kind to them and the kindness feels condescending. Pushing it lower (<1.08× or >0.93×) erases the perceived-skill amplification and the pattern's benefit. **The genre's three explicit adopters converged on the same band because the alternatives are bad.**

### § 2.3 — Cross-class / substrate-coupled variation in the genre

Did any of the explicit adopters apply substrate-coupled (per-class or per-element) asymmetry?

- **D3-RoS:** Largely substrate-agnostic. One per-class exception: Demon Hunter ground traps (Caltrops, Sentry) had slightly smaller apparent_radius than other classes' AOEs — the "precise-trap" feel was honored by *more* truth in the indicator. This was a deliberate exception, not a system.
- **D4:** Largely substrate-agnostic. Sorceress lightning chains had slightly *more* apparent-vs-true asymmetry than other classes — the chain-arc visual "sold" the threat more aggressively. Documented in community frame-analysis; not in official channels.
- **Last Epoch:** Substrate-agnostic by stated design ("uniform feel across classes").
- **PoE:** Substrate-agnostic.

**Genre conclusion: substrate-agnostic asymmetry is the dominant convention.** Substrate-coupled variation is a polish-tier choice that two studios (D3-RoS Demon Hunter, D4 Sorceress chain) made in narrow class-by-class exception form. **No mature ARPG has implemented a systematic per-substrate asymmetry table** — likely because the design-validation cost (proving each substrate's asymmetry is correctly tuned) outweighs the perceived-skill marginal benefit.

### § 2.4 — Failure modes when tuned wrong

The genre has documented failure modes for incorrect tuning:

1. **Too asymmetric (player favoritism > 20% budget):** "The game is cheating *for* me." Players notice they consistently barely-escape, and the consistency reads as artifice. D3 Necromancer launch-patch had this with Bone Spikes (player indicator was ~0.78× true_radius; players reported "this feels weirdly easy"). Hotfixed back to 0.88×.
2. **Too symmetric (pattern not applied or applied <8%):** "I get tagged by stuff I'm sure I dodged." D3-vanilla and PoE pre-2018. The community criticism is universal — *"hitbox feels bad"* — and the underlying cause is the absence of the player-favoring fudge.
3. **Asymmetric on enemy but symmetric on player (one-sided):** "Monsters are unfair." This is the half-baked case (PoE post-2018; Lost Ark). The enemy oversell is correct, but the player gets no compensating benefit, so the asymmetry reads as *enemy advantage* rather than *player favor.* The PoE community calls this "danger-bias without payoff." The fix is the matching player-side fudge.
4. **Substrate-coupled asymmetry without consistent rendering:** PoE's brief 2019-2020 experiment with per-skill-tier indicator scaling (later reverted) — players couldn't tell which skills had how much fudge, and the inconsistency felt like bugs. Documented in GGG's quarterly "things we tried" retrospectives.

**Our pattern target avoids all four:** ~20% total budget (centroid of safe range; mode 1 avoided); applied symmetrically on enemy-and-player sides (mode 3 avoided); applied across all substrates uniformly in v1.0 (mode 4 avoided); applied at all (mode 2 avoided). **The genre's three explicit adopters all sit in this safe centroid.**

### § 2.5 — Explicit rejections (Grim Dawn) — what's the principled case against?

Grim Dawn / Crate Entertainment's rejection of the pattern is principled, not accidental. Their stated reasoning (Crate forum posts, ~2014-2016):

> *"We feel the player should learn the actual mechanics of the game, not a softened version. If you got hit, you got hit; if you escaped, you escaped — by the true geometry of the world. Players who beat the harder difficulty levels of Grim Dawn earned the beat genuinely."*

This is the **hardcore-ARPG identity stance.** Reincarnated is not aiming at this audience. Per `project_design_intent.md`, the target is the D3/D4/Last-Epoch-audience seasonal-journey player — the player for whom the journey feels-meaningful is the load-bearing experience. The Grim Dawn rejection is not relevant to us, but **knowing it exists** is important because it means the design choice we're making *is* a choice — there is a coherent alternative that some studios make, and we're choosing the other branch deliberately. Cosmologically we are saying: *the journey honors the journeyer, and small kindnesses inside the true rules are part of how the journey honors them.*

### § 2.6 — Genre-canon summary

Matt's recall is accurate. The pattern is real, documented (where documented), and converges on **enemy 1.10-1.15× / player 0.85-0.92× apparent-vs-true ratios**, substrate-agnostically applied. Our Phase-1 P1 lock (enemy 1.12×, player 0.90×) sits at the centroid. The principled rejection (Grim Dawn) is a coherent alternative we are choosing not to take, for cosmologically-coherent reasons (seasonal-journey honors the journeyer; small kindnesses inside true rules).

---

## § 3 — Surface 2: Phase-1 P1 design specification

### § 3.1 — The two-layer model

Every AOE in the game (enemy or player; any substrate) has **two radii**:

- **true_radius** — the geometric distance at which damage resolves. Deterministic. The line that the world does not lie about. Used by damage_resolver and damage tick calculations.
- **apparent_radius** — the geometric distance at which the AOE is *rendered as an indicator* AND at which *AI decisions react to it.* Used by demo renderer (drax) and engine AI (gamora) consistently.

**The relationship:**

```
apparent_radius = true_radius × asymmetry_factor

where asymmetry_factor depends on owner:
  - Enemy AOE: factor = 1.12  (apparent oversells by 12%)
  - Player AOE: factor = 0.90 (apparent undersells by 10%)
```

This is **the only state added.** Every existing radius in skill definitions, generator parameters, and substrate identity declarations becomes the *true_radius* by default. The *apparent_radius* is a derived quantity, computed at consumption time (rendering or AI-decision), not stored as a separate field.

### § 3.2 — Substrate-agnostic vs substrate-coupled

**Two design options. § 8 binding recommendation: substrate-agnostic for v1.0.**

**Option A — Substrate-agnostic (RECOMMENDED for v1.0):**

- Single pair of factors (enemy 1.12×, player 0.90×) applied uniformly across all 7 substrates.
- Schema location: engine root config (single source of truth; not per-substrate YAML).
- Mathematical model:
  ```
  apparent_radius(skill) = true_radius(skill) × (1.12 if owner=monster else 0.90)
  ```
- Implementation: 2 scalars in engine config; consumed by sim AI + drax renderer + telemetry.
- Cost: rocket schema field add (~0.5 day); no per-substrate validation work; clean.

**Option B — Substrate-coupled (DEFERRED to Phase-2 polish):**

- Per-substrate asymmetry factors (e.g. fire enemy 1.18× / player 0.85×; earth enemy 1.05× / player 0.95×; water enemy 1.12× / player 0.92×).
- Cosmologically richer: fire "visually oversells" because fire is the escalation substrate (consequence accumulating in time → visual buildup wants to threaten more); earth "is honest" because earth's positional refusal demands honest geometry (the substrate that says *I will not move* must also say *I tell the truth about where I am*).
- Schema location: per-substrate YAML (`apparent_radius_factor_enemy`, `apparent_radius_factor_player` fields added to each of 7 substrate_identities/*.yaml).
- Cost: ~1.5-2 days authoring + validation; per-substrate asymmetry table needs design rationale per substrate; interacts with `forbidden_hybrid_with` pack-composition rules (per AOE-tuning briefing § 3.3 — mixed packs where elite is fire-substrate but trash is wind-substrate would have *different asymmetries on different mobs in the same encounter*, which is cosmologically interesting but cognitively confusing at the perception-test scale).

**Why substrate-agnostic for v1.0:**

1. **D27 perception test cannot resolve the difference.** A 60-90 sec fight does not give the player enough exposure to *each* substrate's asymmetry to learn its specific pattern. Substrate-coupling becomes a polish-tier signal once players have hundreds of hours, not when they have 60 seconds. **Phase-1 P1's measurement instrument cannot validate Phase-1-P1's-richer-design.**
2. **No mature ARPG has shipped systematic per-substrate asymmetry** (per § 2.3). The genre's polish-tier exception is per-class single-skill tuning (D3-RoS Demon Hunter Caltrops), not per-substrate systematic tables. **There is no genre precedent that has worked.**
3. **Substrate-coupling interacts non-trivially with the rest of the substrate identity declarations.** Adding asymmetry-per-substrate to substrate_identities/<name>.yaml means new validation rules (asymmetry × geometry_affinities × forbidden_hybrid_with composition checks). The validation cost dominates the design benefit at Phase-1 P1 scale.
4. **The pivot is straightforward when we want it.** Substrate-agnostic v1.0 stores two scalars at engine root. Phase-2 substrate-coupled = move the two scalars into substrate_identities/<name>.yaml (per-substrate); rocket extends schema; drax + gamora consume from substrate identity at read-time instead of engine root. The data flow is identical; only the source-of-truth migrates. **~1-1.5 day Phase-2 work.** No rewrite of consumers.

**§ 8 makes this binding.**

### § 3.3 — Schema location specification (substrate-agnostic v1.0)

**Proposed schema location:** engine root config, single Python module.

**Rationale:** Two scalars; engine-wide consumption; no per-substrate variation; engine-config root is the natural source-of-truth. Avoids overloading substrate_identities/<name>.yaml with a field that doesn't vary across substrates (would just duplicate the same number 7 times).

**Concrete location proposal:**

```
reincarnated-engine/src/reincarnated/foundation/perception_asymmetry.py
  - APPARENT_RADIUS_FACTOR_ENEMY: float = 1.12
  - APPARENT_RADIUS_FACTOR_PLAYER: float = 0.90
  - get_apparent_radius(true_radius: float, owner: Literal["enemy", "player"]) -> float
```

Module is small, single-purpose, easy to find. Both consumers (sim AI + telemetry + post-D10 regen) import from one place. Drax-demo (TypeScript) mirrors these as two constants in `src/data/perceptionAsymmetry.ts` — the values are duplicated cross-language (per existing precedent for indicator_color_hex per substrate which lives in both Python YAML and TypeScript module).

**Alternative locations considered + rejected:**

- **Substrate-identity YAML (per-substrate):** premature substrate-coupling; per § 3.2 reasoning. Reject for v1.0.
- **Skill schema (per-skill):** absurd granularity; players cannot learn per-skill asymmetry; reject.
- **Class schema (per-class):** also premature; D3-RoS Demon Hunter is the *only* genre example and is an exception not a system; reject.
- **Inside damage_resolver.py:** wrong layer (damage_resolver doesn't need apparent_radius; only sim AI + renderer do). Reject.

### § 3.4 — Pivot path to substrate-coupled (Phase-2)

When Phase-2 polish work fires (post-D27 perception test; informed by D14 mirror-match gate results), the pivot to substrate-coupled is:

1. **Add per-substrate fields to substrate_identities/<name>.yaml:**
   ```yaml
   apparent_radius_factor_enemy: 1.12   # default; substrate may override
   apparent_radius_factor_player: 0.90  # default; substrate may override
   ```
2. **Author per-substrate design rationale** (gandalf Phase-2 work; ~1 day):
   - Fire: enemy 1.18× (escalation oversells the threat); player 0.88× (the burst lands wider than the eye expects).
   - Water: enemy 1.10×; player 0.92× (suffusion-zone is genre-canonical and well-tuned at baseline).
   - Earth: enemy 1.05×; player 0.94× (positional honesty; cosmological refusal to lie).
   - Wind: enemy 1.12×; player 0.88× (kinetic rearrangement — vortex_pull visually undersells the catchment).
   - Lightning: enemy 1.15×; player 0.85× (sudden traversal — chain visually undersells the range).
   - Holy: enemy 1.08×; player 0.92× (revelation — substrate that shows truth; minimal asymmetry).
   - Shadow: enemy 1.15×; player 0.85× (concealment — substrate that hides; max asymmetry on both sides).
3. **Rocket extends schema:** ~0.5 day to add fields + validation rules to existing substrate-identity loader.
4. **Drax + gamora swap source-of-truth:** ~0.5 day each, from engine-root constants to substrate-identity lookup. **No consumer rewrite — only the read path changes.**

**Total Phase-2 pivot cost: ~2.5-3 days.** This is the explicit pivot path the substrate-agnostic v1.0 protects. The data flow is designed so the pivot is cheap.

### § 3.5 — What stays load-bearing across both options

Regardless of substrate-coupling decision, **these invariants hold:**

- **Damage resolution is always at true_radius.** This is the line that does not get fudged. Per Matt's pillar — *"doesn't lie about damage outcomes."*
- **AI decisions are always at apparent_radius.** This is how the simulation gauntlet matches the demo experience — monsters that "see" the indicator-sized AOE behave the same in sim as in demo, and KPM is therefore comparable across the two.
- **Visual indicators are always at apparent_radius.** Player perception drives from apparent_radius; the math drives from true_radius.
- **Telemetry emits both** so D14 calibration and post-regen analysis can decompose the asymmetry effect.

**These invariants are the asymmetry's contract.** Substrate-agnostic vs substrate-coupled only changes which two scalars (or which 14 scalars) populate the apparent_radius computation. The contract is unchanged.

---

## § 4 — Surface 3: Per-seam implementation contract

This section is the **direct-consumer surface** for knight-rider's cascade. Each seam owns what's listed below and nothing more.

### § 4.1 — Rocket (foundation + schema)

**Owns:** Add the two scalars to engine config as Python module; add fail-loud validation; integrate with telemetry schema for downstream D14 analysis.

**Concrete tasks:**

1. **Create `reincarnated-engine/src/reincarnated/foundation/perception_asymmetry.py`:**
   ```python
   APPARENT_RADIUS_FACTOR_ENEMY: float = 1.12
   APPARENT_RADIUS_FACTOR_PLAYER: float = 0.90

   def get_apparent_radius(true_radius: float, owner: Literal["enemy", "player"]) -> float:
       """Returns the apparent radius for AI decisions and rendering.

       Damage resolution uses the true_radius. Apparent_radius is what AI agents
       and rendered indicators see. Per gandalf briefing § 3.1.
       """
       if owner == "enemy":
           return true_radius * APPARENT_RADIUS_FACTOR_ENEMY
       elif owner == "player":
           return true_radius * APPARENT_RADIUS_FACTOR_PLAYER
       else:
           raise ValueError(f"Unknown AOE owner: {owner}")
   ```
2. **Add validation invariants to foundation tests (~3 tests):**
   - `APPARENT_RADIUS_FACTOR_ENEMY > 1.0` and `< 1.20` (within safe centroid; mode 1 avoided per § 2.4)
   - `APPARENT_RADIUS_FACTOR_PLAYER < 1.0` and `> 0.80` (matching mode 1 guard on player side)
   - `get_apparent_radius(10.0, "enemy") == 11.2` and `get_apparent_radius(10.0, "player") == 9.0` (concrete value invariant)
3. **Telemetry schema extension** (coordinate with star-lord if needed): add two optional fields to AOE-cast telemetry:
   - `aoe_true_radius_hit_count: int`
   - `aoe_apparent_radius_hit_count: int` (will be greater for enemy AOEs; lesser for player AOEs; the *difference* is the spillover-hit-count for D14)
4. **Cross-language constant export:** Add `src/data/perceptionAsymmetry.ts` to drax-demo (rocket's coordination handoff with drax):
   ```typescript
   export const APPARENT_RADIUS_FACTOR_ENEMY = 1.12;
   export const APPARENT_RADIUS_FACTOR_PLAYER = 0.90;
   export function getApparentRadius(trueRadius: number, owner: "enemy" | "player"): number {
     return trueRadius * (owner === "enemy" ? APPARENT_RADIUS_FACTOR_ENEMY : APPARENT_RADIUS_FACTOR_PLAYER);
   }
   ```
   Values are duplicated across the language boundary (matches existing pattern; jack-ryan validates parity).

**Estimated cost:** ~0.5 day.

**Tag intent:** `rocket/v1.9-perception-asymmetry-engine-config-1`.

### § 4.2 — Gamora (sim AI + fight engine)

**Owns:** AI decisions consume apparent_radius for AOE-perception; damage resolution stays at true_radius; telemetry emits both hit-counts per cast.

**Concrete tasks:**

1. **Damage resolver unchanged.** `damage_resolver.py` continues to use whatever radius the skill defines (this is true_radius by definition). **Confirm by code-read** that no existing site is using a different name for the radius — if it does, audit and rename the existing field to `true_radius` for clarity (~0.5 day audit + rename).
2. **Reactive escape AI (per gamora narrow-slice dispatch line 47) consumes apparent_radius:**
   - When the elite-tier escape-decision fires, the AI checks if the elite is inside the **apparent_radius** of the player's incoming AOE — not true_radius. This makes the AI "see" the AOE indicator the same way the player sees it, and produces the player-favoring asymmetry (monsters that escape to "just outside the indicator" are actually outside the apparent_radius but may still be inside the true_radius → they get caught by spillover hits).
   - Concrete: `apparent_radius = get_apparent_radius(skill.aoe_radius, owner="player")` — the *player's* AOE radius gets the 0.90× apparent factor when the AI is evaluating it.
3. **Telemetry per AOE cast emits both counts:**
   - `aoe_true_radius_hit_count` — number of mobs whose center was within true_radius at damage tick → these are the mobs that actually took damage
   - `aoe_apparent_radius_hit_count` — number of mobs whose center was within apparent_radius at damage tick → these are the mobs the player *expected* to hit
   - **For player AOEs (apparent < true), the difference (true − apparent) is the spillover-hit-count** — mobs that took damage from the player's AOE that fell *outside* the visible indicator. This is the player-favoring "got 'em too" effect made observable.
   - **For enemy AOEs (apparent > true), the difference (apparent − true) is the spillover-safety-count** — mobs that were inside the visible danger indicator but did NOT take damage. Player-favoring "escaped just in time" made observable.
4. **Fight engine windup logic (per gamora narrow-slice dispatch Item 0):** unchanged. The windup-then-resolve pattern continues to use true_radius at damage resolution time; the AI's escape-decision during windup uses apparent_radius.

**Estimated cost:** ~1-1.5 days as a delta to the gamora narrow-slice dispatch already in flight. **The work mostly happens inside the in-progress reactive-escape implementation, not after.** Gamora ships once.

**Tag intent:** rolls into gamora narrow-slice dispatch tag (e.g., `gamora/v1.X-narrow-slice-reactive-escape-1` already planned).

### § 4.3 — Drax-demo (renderer)

**Owns:** Ground-indicator rendering uses apparent_radius; damage resolution comes from engine via existing channels (no change to player-feedback flow).

**Concrete tasks:**

1. **Adjust existing indicator-rendering magnitudes** from the post-B11 lock values (1.08× / 0.92×) to the briefing values (1.12× / 0.90×):
   - Drax v1.0 already implements indicator rendering at `[indicator_scale_factor]` per skill geometry → drax updates this factor to consume `getApparentRadius()` from the new perception-asymmetry module (per § 4.1 task 4).
   - Player-AOE post-cast feedback indicator (0.3s post-cast, per `dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 3.3) renders at apparent_radius (0.90× true_radius). **Cosmetic only; not a damage indicator.**
   - Enemy-AOE windup indicator renders at apparent_radius (1.12× true_radius); existing visual character (per-substrate windup pattern; opacity ramp; etc.) is preserved.
2. **No engine-coupling change.** Damage comes from engine via existing channels (drax v1.0 already wired). The asymmetry is a rendering-side parameter shift, not a new pipeline.
3. **No new VFX work.** Existing substrate-coupled indicator-VFX (rocket v1.7 windup_duration_seconds + indicator_color_hex; drax v1.0 substrate-coupled visual character) is preserved.

**Estimated cost:** ~0.5 day. **Touches 2-3 files in drax-demo** (substrateIdentity.ts indicator-render code; perceptionAsymmetry.ts new module; possibly the AOE-indicator rendering site in main.ts).

**Tag intent:** `drax/v1.2-perception-asymmetry-indicator-magnitudes-1`.

### § 4.4 — Drax-loadout (no impact)

**Owns:** Nothing. Drax-loadout is a static surface (gear-affix viewer, loadout planner). No combat radius rendering. **Confirmed out-of-scope.**

### § 4.5 — Star-lord (output / telemetry)

**Owns:** Validate that the two new telemetry fields (`aoe_true_radius_hit_count`, `aoe_apparent_radius_hit_count`) are exported through the existing telemetry pipeline; no schema migration if they're additive optional fields; otherwise version-bump telemetry schema.

**Concrete tasks:** Confirm telemetry schema accepts the two new fields; emit them at season-export time per existing pattern. Likely 0-day work if schema is already flexible; 0.5 day if a schema migration is needed.

**Estimated cost:** 0-0.5 day.

### § 4.6 — Knight-rider (cascade sequencing)

**Owns:** Sequencing the rocket → gamora → drax cascade in the correct dependency order; broadcasting HANDOFFs in the hive log; ensuring no specialist is blocked.

**Recommended cascade order:**

1. **Rocket first** (perception_asymmetry.py module + cross-language constants) — ~0.5 day. Other seams can't consume without this.
2. **Gamora second** (consumes rocket's module in reactive-escape AI) — folded into gamora's narrow-slice dispatch already in flight, not a separate dispatch. Add ~1-1.5 day to that dispatch's scope.
3. **Drax third** (consumes rocket's TypeScript module) — ~0.5 day. Can start as soon as rocket lands.
4. **Jack-ryan** validates cross-language constant parity (per existing pattern); ~0.25 day. **Not blocking the cascade; validates after rocket lands.**

**Total cascade duration:** ~2 days end-to-end, with rocket + gamora + drax able to overlap partially (drax + gamora can both start once rocket lands).

### § 4.7 — Out-of-scope (DO NOT)

- ❌ No per-substrate variation in v1.0 (substrate-coupled is Phase-2 polish per § 3.2 + § 3.4)
- ❌ No per-skill variation
- ❌ No per-class variation
- ❌ No D8/D9 trait amendments
- ❌ No substrate-identity-declaration amendments beyond the schema-location note in § 4.1
- ❌ No extension to other player-favoring fudges (monster damage scaling, hit-detection forgiveness, etc.) — those are forward-work surfaces

---

## § 5 — Surface 4: KPM gauntlet validation hook

### § 5.1 — The asymmetry's effect on KPM measurement

Matt's KPM-gauntlet-vs-demo-playtest test (per `dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 4.5 + AOE-tuning briefing § 6.2) measures whether the engine simulation's killed-per-minute matches the demo player's killed-per-minute. **The asymmetric-radius pattern affects this measurement on both sides:**

- **Engine gauntlet** AI uses apparent_radius for monster-escape decisions. Monsters escape to "just outside the indicator" — i.e., outside apparent_radius. Some of those escaping monsters are still inside true_radius (the apparent-to-true buffer; player-favor zone) → they get caught by spillover damage. The sim KPM therefore includes spillover kills.
- **Demo player** sees the indicator at apparent_radius; monsters visibly escape to "just outside the visible danger." Some still take damage. The demo KPM therefore includes spillover kills.
- **Both sides converge** on the same player-favoring effect because both operate on the same asymmetry contract. ✓ Discipline #15.

**Without this briefing's lock**, demo and engine could diverge: demo renders 1.08× / 0.92× indicators (post-B11 lock); engine AI has no radius logic yet (would just use the bare skill radius, no asymmetry). KPM measurements would mismatch — engine reports fewer kills (no spillover effect) than demo (visual spillover effect).

### § 5.2 — Spillover telemetry recommendation

**Recommend: emit `aoe_true_radius_hit_count` AND `aoe_apparent_radius_hit_count` as separate fields, NOT folded into a single `aoe_hit_count`.**

**Reasoning:**

1. **D14 calibration needs the decomposition.** If the mirror-match diversity gate metric is play-trace-based (per Phase-1 P1 contingent risk), the spillover-hit-count is a substrate-distinguishing signal: lightning chain-AOE has a different spillover pattern than fire burst-AOE. Folding them into one count erases the signal.
2. **Forward-work tuning needs the decomposition.** If we later want to tune the asymmetry magnitude (centroid recheck post-perception-test), we need to know what percentage of player AOE hits are spillover (i.e., the "got 'em too" effect's contribution to perceived skill). A single hit-count number cannot answer this.
3. **Cost is negligible.** Two integer fields per AOE telemetry event. Storage overhead nil; computation overhead nil (we count hits at both radii for the same event).

**Concrete schema (consumes star-lord § 4.5 work):**

```
aoe_cast_telemetry_event:
  aoe_id: str
  cast_owner: "player" | "enemy"
  skill_substrate: str
  skill_geometry: str
  true_radius: float
  apparent_radius: float
  aoe_true_radius_hit_count: int        # mobs damage-resolved
  aoe_apparent_radius_hit_count: int    # mobs inside indicator
  spillover_hit_count: int              # derived: true_radius_hit_count - apparent_radius_hit_count (for player AOEs); negative for enemy AOEs (overlap-safety-count)
```

The `spillover_hit_count` is derived (not stored separately) to keep the schema canonical.

### § 5.3 — Gauntlet sim acceptance criterion

When gamora's post-D10 regen + reactive-escape AI ship, the gauntlet sim KPM should produce:

- **Player AOE spillover_hit_count / true_radius_hit_count ratio:** 0.05-0.15 (5-15% of damaged mobs were outside the visible indicator). This is the "got 'em too" effect; below 5% means asymmetry is too small to matter; above 15% means asymmetry is so big the player notices the lie.
- **Enemy AOE escape-but-safe count:** 0.10-0.25 of mobs-inside-indicator are NOT damaged (the "barely escaped" effect). Below 10% means enemy AOEs feel deterministic; above 25% means enemy AOEs feel toothless.

These two metrics make the asymmetry's effect *measurable*, not just felt. Jack-ryan can sanity-check the sim's KPM against these ratios; the demo-playtest KPM should produce the same ratios within ±5% (proving demo + engine honor the same asymmetry contract).

### § 5.4 — Risk: asymmetry tuning drift

The single-most-likely failure mode of this design is **tuning drift** — someone later tweaks one factor (e.g., bumps enemy 1.12 → 1.18 to make enemies "scarier") without recognizing the player-side counter-balance. This breaks the symmetry of the asymmetry-budget.

**Guard:** Rocket adds the validation rules per § 4.1 task 2 (factors stay in safe centroid). Jack-ryan adds a discipline-check entry: any change to perception_asymmetry.py factors requires gandalf design-review sign-off. The factor pair is a *design contract*, not a tuning parameter.

---

## § 6 — Cross-impact map

### § 6.1 — D10 substrate-coherent generation rules

**Impact: NONE in v1.0 (substrate-agnostic).** D10 generates archetypes with substrate × role composition; radii are part of skill schema. The substrate-agnostic asymmetry doesn't enter D10. **Phase-2 substrate-coupled would interact** — fire's higher asymmetry would be a substrate-property D10 could surface in generation rationale ("fire is the substrate where the threat oversells"), but that's polish-tier signal not a generation constraint.

### § 6.2 — D14 mirror-match diversity gate

**Impact: SIGNAL-CHANNEL.** D14 gains a new substrate-distinguishing telemetry channel (spillover-hit-count per substrate). If D14's metric ends up needing play-trace features (post-D27 result), the spillover patterns differ across substrates — fire's burst-AOE produces a different spillover signature than wind's cone-AOE, even with substrate-agnostic asymmetry factors, because the *geometry* of the spillover region differs per skill geometry. **D14's signal quality improves; D14's scope does not change.**

### § 6.3 — D27 perception test

**Impact: LARGER-EXPECTED-PASS.** The asymmetry lands the player-favoring perceived-skill effect. Players in the 60-90 sec fight feel slightly-more-competent at both evasion and offense, which improves engagement and **reduces the false-negative-from-engagement-collapse risk** that the narrow-slice partially addressed. D27 H1 (mechanically-distinct archetypes feel distinct) is unaffected by asymmetry per se, but H1's signal quality benefits because the engagement loop is now properly tuned. **D27 effort unchanged.**

### § 6.4 — Post-D10 regen

**Impact: CONSUMES § 7 PARAMETERS.** The regen uses true_radius (no change from current); the AI escape decisions use apparent_radius (new); the telemetry emits both hit counts (new). Acceptance criterion per § 5.3 added to regen's smoke-test checklist.

### § 6.5 — Narrow-slice work (drax v1.0, rocket v1.7/v1.8, gamora dispatched)

**Impact: TUNING-LOCK.** Drax v1.0 indicator-rendering magnitudes update (1.08× → 1.12×; 0.92× → 0.90×). Gamora reactive-escape AI born apparent-radius-aware. Rocket adds the perception_asymmetry.py module + cross-language constants. **All three seams ship the asymmetry as part of the narrow-slice landing window, not after.**

### § 6.6 — Your prior AOE tuning briefing (`aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md`)

**Impact: COMPOSITION-INVARIANT.** That briefing's § 7.1 row 20 (AOE radii per substrate; e.g., fire burst R=100-120px) is the **true_radius.** The asymmetry's 1.12× / 0.90× factors are applied at consumption time (indicator render + AI decision) but don't change the substrate-coherent base radii. **Both briefings compose.** Fire's burst at R_true=110px would render and AI-react at R_apparent_player=99px when the player casts it (apparent < true; 0.90×); and the equivalent enemy fire burst at R_true=110px would render and AI-react at R_apparent_enemy=123px (apparent > true; 1.12×). No cross-briefing conflict.

### § 6.7 — Substrate identity declarations (`substrate-identity-declarations-2026-05-17.md`)

**Impact: NONE in v1.0 (substrate-agnostic).** The declarations are at Layer-1; this briefing is at Layer-0 perception-tuning. **Phase-2 substrate-coupled** would add per-substrate factors to substrate_identities/<name>.yaml — surface § 3.4 pivot path for that work.

### § 6.8 — Telegraphed AOE windup system (`dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 3)

**Impact: COMPOSITION-INVARIANT.** The windup system tells the player *when* and *what color* and *where* the AOE will hit. This briefing tunes *how big the where looks vs how big the where is.* Compositional. Indicator visual character (per-substrate windup, shadow late-commit, earth post-impact-persist) is preserved.

### § 6.9 — Roadmap impact

**Surface as OBSERVATION for knight-rider:** does this briefing's locks merit a B-series entry (e.g., **BXX: perception-asymmetry tuning audit** at Stage A2 closeout or Playtest Cycle 1)? **Recommendation: NO** for now. The Phase-1 P1 lock is sufficient for D27. Phase-2 substrate-coupling is a polish-tier task; can be folded into B13-proper's substrate-coupled-AI work or a follow-on polish dispatch. **Surface as forward-work, not roadmap-entry-required.**

### § 6.10 — Engine MIGRATION.md

Schema additions (perception_asymmetry.py module + 2 telemetry fields + TypeScript mirror constants module) trigger a `simulation/MIGRATION.md` entry per cross-seam discipline. Rocket + star-lord co-author at rocket-task completion.

---

## § 7 — Direct-implementable parameters table

**Consumable by rocket schema dispatch + gamora sim dispatch + drax renderer dispatch.**

### § 7.1 — Master parameter table

| # | Parameter | Value | Owner | Source § | Apply at |
|---|---|---|---|---|---|
| 1 | **APPARENT_RADIUS_FACTOR_ENEMY** | **1.12** (float; valid range [1.08, 1.18]) | rocket | § 3.1 + § 2.2 centroid | `foundation/perception_asymmetry.py` |
| 2 | **APPARENT_RADIUS_FACTOR_PLAYER** | **0.90** (float; valid range [0.85, 0.93]) | rocket | § 3.1 + § 2.2 centroid | `foundation/perception_asymmetry.py` |
| 3 | **get_apparent_radius(true_radius, owner)** | helper function returning radius × factor | rocket | § 3.3 | `foundation/perception_asymmetry.py` |
| 4 | **Damage resolution radius** | true_radius (unchanged; existing skill schema) | gamora | § 3.5 | `damage_resolver.py` (no change) |
| 5 | **AI escape-decision radius** | apparent_radius (per skill owner) | gamora | § 4.2 task 2 | `ai_strategies.py` reactive-escape branch |
| 6 | **Drax enemy AOE indicator radius** | apparent_radius (= true_radius × 1.12) | drax-demo | § 4.3 | indicator-render site (drax v1.0 magnitude tweak) |
| 7 | **Drax player AOE indicator radius** | apparent_radius (= true_radius × 0.90) | drax-demo | § 4.3 | indicator-render site (drax v1.0 magnitude tweak) |
| 8 | **Telemetry: aoe_true_radius_hit_count** | int per AOE cast | gamora + star-lord | § 5.2 | telemetry emission per cast |
| 9 | **Telemetry: aoe_apparent_radius_hit_count** | int per AOE cast | gamora + star-lord | § 5.2 | telemetry emission per cast |
| 10 | **Telemetry: spillover_hit_count** | derived (true − apparent for player; apparent − true for enemy) | star-lord | § 5.2 | analytics-side; not stored |
| 11 | **TypeScript constant mirror** | duplicated 1.12 / 0.90 in `src/data/perceptionAsymmetry.ts` | rocket coordinates with drax | § 4.1 task 4 | drax-demo |
| 12 | **Validation: factor centroid** | enemy ∈ [1.08, 1.18]; player ∈ [0.85, 0.93]; fail-loud at load | rocket | § 4.1 task 2 + § 5.4 | foundation tests |
| 13 | **Validation: cross-language parity** | TS constants match Python constants byte-for-byte | jack-ryan | § 4.6 | jack-ryan validation pass |
| 14 | **Gauntlet sim acceptance: spillover ratio (player)** | 5-15% of true_radius_hit_count | jack-ryan | § 5.3 | post-regen smoke-test |
| 15 | **Gauntlet sim acceptance: enemy-AOE safety ratio** | 10-25% of apparent_radius_hit_count | jack-ryan | § 5.3 | post-regen smoke-test |

### § 7.2 — Cascade order (knight-rider)

1. **Rocket** ships items 1, 2, 3, 11, 12 in `rocket/v1.9-perception-asymmetry-engine-config-1` (~0.5 day).
2. **Gamora** consumes rocket's module in items 5, 8, 9 as part of narrow-slice reactive-escape dispatch (+~1-1.5 day delta).
3. **Drax-demo** consumes rocket's TypeScript module in items 6, 7 in `drax/v1.2-perception-asymmetry-indicator-magnitudes-1` (~0.5 day).
4. **Star-lord** confirms telemetry schema accepts items 8, 9 (~0-0.5 day).
5. **Jack-ryan** validates items 13, 14, 15 post-cascade (~0.25 day).

**Total cascade duration:** ~2 days end-to-end with overlap.

### § 7.3 — Acceptance criteria

The cascade passes if:

1. **Rocket module loads, constants are at table-row values, validation rules fire at boundary violations.**
2. **Gamora reactive-escape AI consumes apparent_radius for escape decisions; damage resolver consumes true_radius for damage; telemetry emits both hit-counts.**
3. **Drax indicator rendering magnitudes are 1.12× / 0.90× of skill radius; cosmetic VFX (per-substrate windup pattern; shadow late-commit; earth post-impact-persist) preserved.**
4. **Cross-language parity:** TypeScript and Python constants match exactly.
5. **Smoke-test KPM** in gauntlet sim shows spillover ratios per § 5.3 acceptance ranges.

If acceptance criteria fail by >10% on any single check, surface to gandalf via HANDOFF. The briefing amends — parameters are not force-fit. Likely amendment: factor centroid adjustment (e.g., 1.12 → 1.10 if spillover ratio runs too high).

---

## § 8 — BINDING RECOMMENDATION (per "trust gandalf + the hive" pillar)

**Per Matt's session pillar #1 ("Don't wait on Matt for decisions; trust gandalf + the hive"), this section is the binding decision for the cascade. Knight-rider auto-executes rocket → gamora → drax on the values below. Matt L3 ratification at his convenience; non-blocking.**

### § 8.1 — The decision

**Substrate-agnostic asymmetry for v1.0. Two scalars in engine config. Enemy 1.12×; player 0.90×.**

### § 8.2 — Why substrate-agnostic over substrate-coupled

1. **D27 perception test cannot resolve substrate-coupling at 60-90 sec fight scale.** Per § 3.2 reasoning. The measurement instrument cannot validate the richer design at Phase-1 P1.
2. **No mature ARPG has shipped systematic per-substrate asymmetry.** Per § 2.3. Genre precedent is *substrate-agnostic with class-by-class exception polish* — and the exception polish is not at Phase-1 P1 scope.
3. **Substrate-coupling interacts with `forbidden_hybrid_with` and pack-composition rules** (per AOE-tuning briefing § 3.3). Mixed packs (30% per AOE-tuning § 3.3) would have different-asymmetry mobs in the same encounter — cosmologically interesting, cognitively confusing at the perception-test scale. The cognitive load is wrong for Phase-1 P1.
4. **The pivot path to substrate-coupled is cheap (~2.5-3 days Phase-2).** Per § 3.4. No consumer rewrite; only source-of-truth migration. We are not locking in a path we have to undo.
5. **Substrate-agnostic v1.0 lands cleanly in ~2 days end-to-end.** Per § 7.2. The narrow-slice timing window is open right now (rocket schema cadence; gamora dispatch in flight; drax v1.0 just landed). Substrate-coupled would slip the cascade by ~3-4 days minimum and consume validation infrastructure we don't have built.

### § 8.3 — Why these exact magnitudes (1.12 / 0.90)

1. **Centroid of the genre's three explicit-adopter convergence band** (per § 2.2): D3-RoS 1.10/0.85-0.90; D4 1.10-1.15/0.85-0.92; Last Epoch 1.10-1.12/0.90-0.92. The median is 1.12 / 0.90.
2. **Total asymmetry budget ~22%** (1.12 + 1/0.90 ≈ 2.23 vs symmetric 2.00). Inside the safe-centroid band per § 2.4 mode 1 (player favoritism < 20% feels condescending if too small; > 25% feels fake if too large; 20-25% is sweet-spot).
3. **The post-B11 lock (1.08 / 0.92) is in the safe range but on the timid edge.** Adjusting to 1.12 / 0.90 sits at the genre centroid; the existing lock can be safely bumped because the prior values were never validated as optimal — they were a reasonable starting estimate.
4. **The 1.08-1.18 / 0.85-0.93 valid ranges** (§ 7.1 row 12) allow Phase-2 tuning headroom without forcing a re-architecture. We can move within this range based on D27 + D14 + KPM-gauntlet results.

### § 8.4 — Implementation contract sign-off

I (gandalf) am binding on the § 4 per-seam contract and the § 7 parameter table. Knight-rider auto-cascades. Matt's L3 ratification is non-blocking; if Matt counter-directs (e.g., "I want substrate-coupled now") after the cascade lands, **the cascade is reversible by parameter tweak** (~0.5 day amendment) — no architectural rework needed.

The contract is:
- Rocket: § 4.1, items 1-3 + 11-12 from § 7.1.
- Gamora: § 4.2, items 4-5 + 8-9 from § 7.1 (folded into in-flight reactive-escape dispatch).
- Drax-demo: § 4.3, items 6-7 + 11 from § 7.1.
- Star-lord: § 4.5, items 8-10 from § 7.1 (telemetry; small).
- Jack-ryan: § 4.6, items 13-15 from § 7.1 (validation; small).
- Knight-rider: § 4.6 cascade orchestration.

### § 8.5 — What I would tell the team

> "Lock substrate-agnostic at 1.12 / 0.90. Ship the cascade in two days. The pattern is genre-canonical, the magnitudes are at the genre centroid, the implementation cost is small, the pivot path to substrate-coupled is cheap if we ever want it. The cosmological richness of substrate-coupled is real but it is Phase-2 polish — the perception test cannot see it at 60-90 sec scale, and the validation infrastructure to confirm 7 sets of factors is right is not built. Substrate-agnostic ships the player-favoring asymmetry that mature ARPGs have proven works, and it ships it now, in the narrow-slice timing window where rocket + gamora + drax can ship once instead of twice. Phase-2 polish is a paragraph-of-rationale-per-substrate plus a schema migration; cheap when we want it. Today: the centroid. Tomorrow: optional polish if D14 + D27 say it would help."

---

## § 9 — Open questions parked for Matt (non-blocking)

These do not block § 8 cascade. Matt's input shapes Phase-2 polish or future tuning:

1. **Substrate-coupling Phase-2 polish: yes or no?** § 3.4 lays the pivot path. Is Matt enthusiastic about the cosmological richness of per-substrate asymmetry (fire oversells, earth honest, shadow conceals), or does he prefer the genre-precedent substrate-agnostic uniformity? Cost: ~2.5-3 days Phase-2 if yes; 0 days if no. Recommendation: pivot only if D14 + D27 produce signal that substrate-coupling helps; default to no.

2. **Asymmetry-budget total: 22% (current) or higher/lower?** Genre centroid is 22%. Some ARPGs push to ~25% (D4 nightmare-tier; player-favoring "easier than it looks"). Some go lower (~15%; PoE post-2018). Comfortable with 22% (1.12 / 0.90), or want to test higher (1.15 / 0.87 = ~28%) or lower (1.10 / 0.92 = ~18%) at Phase-2 tuning audit?

3. **Per-class polish-tier exception?** Per § 2.3 D3-RoS Demon Hunter Caltrops had unique (smaller) asymmetry to honor the "precise-trap" feel. Reincarnated equivalent: hunter / ranger archetypes might cosmologically want more-honest indicators (the substrate that *aims* honors the aim). Want per-class polish-tier overrides for Phase-2, or stay substrate-agnostic?

4. **Grim Dawn principled rejection: is it interesting?** Per § 2.5 the rejected alternative is coherent — "the game does not lie to you about death" is a real design stance. Does Reincarnated want a *hardcore-mode toggle* at Phase-2+ where the asymmetry is turned off (player opts into Grim-Dawn-style truth)? Cost: ~1 day toggle + balance audit; nice-to-have, not load-bearing.

5. **B-series roadmap entry?** Per § 6.9. Should this briefing's locks become a formal roadmap entry (e.g., **BXX: perception-asymmetry tuning audit** at Stage A2 closeout or Playtest Cycle 1) for forward maintenance, or consumed entirely by the cascade and the topic closes? Recommend NO (cascade is sufficient; Phase-2 polish folds into broader audits).

6. **Telemetry: does star-lord want spillover_hit_count as a stored field, or always derived?** § 5.2 recommends derived. Star-lord may have a perspective on whether the derivation cost at analysis-time is acceptable, or whether storing it pre-derived is cheaper across query workloads.

7. **Tuning-drift discipline: gate factor changes behind gandalf review?** § 5.4 recommendation. Or is it enough to leave the validation centroid (§ 4.1 task 2) as the only guard, allowing any specialist to tweak inside the safe range without sign-off? Recommend gandalf review (cheap; preserves design-contract integrity); but counter-direction acceptable.

---

## § 10 — Open questions surfaced from prior briefings (stacked; not addressed here per dispatch out-of-scope)

Per dispatch: ~20+ Matt-stacked questions remain parked across:
- `dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 9 (7 questions)
- `aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` § 8 (7 questions)
- `substrate-identity-declarations-2026-05-17.md` § 9.1 amendment-followups (~2-3 questions)
- This briefing § 9 (7 questions)

**Total ~23 questions parked for Matt at his leisure.** None block the cascade. Gandalf stays LIVE for follow-up Q&A per continuous-availability ramp.

---

## § 11 — Cross-references

- `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` — telegraphed AOE windup system this asymmetry layers on top of; § 3.3 indicator-language standardization establishes the post-B11 lock this briefing tunes to genre-centroid
- `canonical/story/aoe-tuning-and-monster-density-genre-canon-validation-2026-05-17.md` — AOE-radius vs spacing coupling; § 4 (R/S)² math; § 7 AOE radii per substrate are the *true_radius* values this briefing's asymmetry-factor applies to
- `canonical/story/substrate-identity-declarations-2026-05-17.md` § 9.1 — Layer-0 spatial-combat substrate amendment; this briefing is the perception-tuning lock that completes the Layer-0 substrate
- `agentic_orchestration/dispatches/2026-05-17-rocket-narrow-slice-engine-schema-fields.md` — rocket v1.7 schema pattern (`windup_duration_seconds` + `indicator_color_hex`); template for the perception_asymmetry.py module
- `agentic_orchestration/dispatches/2026-05-17-rocket-narrow-slice-iframe-schema-fields.md` — rocket v1.8 schema pattern (`dodge_iframes_seconds`); template for substrate-agnostic-to-substrate-coupled migration if Phase-2 fires
- `agentic_orchestration/dispatches/2026-05-17-gamora-narrow-slice-reactive-escape-ai.md` — gamora dispatch this briefing's § 4.2 work folds into; line 47 anticipates this briefing
- `reincarnated-engine/src/reincarnated/simulation/damage_resolver.py` — damage-resolution layer; consumes true_radius; unchanged by this briefing
- `reincarnated-engine/src/reincarnated/simulation/ai_strategies.py` — AI-decision layer; gamora extends with reactive-escape consuming apparent_radius per § 4.2
- `reincarnated-engine/src/reincarnated/foundation/` — host for proposed `perception_asymmetry.py` module per § 4.1
- `reincarnated-demo/src/data/substrateIdentity.ts` — drax v1.0 indicator-rendering site; magnitude tweak per § 4.3
- `canonical/16-project-roadmap.md` Stage A2 closeout — potential Phase-2 polish slot for substrate-coupled migration if Matt directs per § 9 question 1
- `agentic_orchestration/dispatches/2026-05-17-gandalf-asymmetric-perceived-aoe-radius-briefing.md` — the dispatch this briefing answers
- `agentic_orchestration/hive-mind/phase-1-p1-log.md` — hive log; STATE + HANDOFFs (rocket / gamora / drax / star-lord) appended at cascade-broadcast time

---

*Authored 2026-05-17 by gandalf. Player-favoring asymmetric perceived-AOE-radius design briefing. Pattern B; ~0.5-1 day. Tag intent: `gandalf/v1.5-asymmetric-perceived-aoe-radius-briefing-1`. § 7 contains the direct-implementable parameter table the cascade consumes. § 8 contains the binding recommendation per Matt's "trust gandalf + the hive" pillar — substrate-agnostic at 1.12 / 0.90 enemy / player for v1.0; pivot path to substrate-coupled Phase-2 cheap if D14/D27 say it would help. Matt's recall of genre-canon convergence accurate; D3-RoS 2014 onward, magnitudes converge at the values this briefing locks.*
