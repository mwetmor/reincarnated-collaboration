# The resist-design fork: cap-everything (Matt's target) vs spiky-anti-tax (currently locked)

**Author:** gandalf (design seam). **Mode:** Pattern-B development, verification-first. **Status:** design fork surfaced for Matt — NOT a ruling. I own the recognition; the call is Matt's because it pivots a just-locked foundation decision.

**Synthesizes:** the verified resist mechanism (`2026-06-22-player-resist-vs-encounter-element-explainer.md`), the all-7-elements correction (Matt 2026-06-22), Legolas's D2/PoE endgame-resist research (`legolas/findings/2026-06-22-d2-poe-endgame-resist-and-monster-modifiers.md`), and the typed-resistance anchor ruling (`2026-06-21-typed-resistance-boss-anchor-ruling.md`).

---

## TL;DR — Matt has described Path B twice; the engine is locked to Path A

Matt's stated target — **"every player should have 65–75%+ resistance to EACH of the 7 elements"** plus **"a cycle of rare/unique monster groups with varying resists/damage/damage-types"** — is the **D2/PoE cap-everything endgame model, exactly.** Legolas confirms both games run precisely this.

But the typed-resistance wave just **LOCKED the opposite design:** the anti-tax guard caps the resist roller at ~1.5–1.6 total resist-units, deliberately making cap-everything **unreachable** (capping all 7 at 0.70 needs **4.9 units**; at 0.75 needs **5.25**). The locked design is **spiky** — you cap 1–2 elements and eat the rest. That is a coherent design, but it is **not** the one Matt described.

**This is a genuine fork, not a tuning tweak.** It cannot be split: resist is either a scarce spiky budget (Path A) or a mandatory-but-costly baseline (Path B). Pick one.

---

## The collision, in numbers

| | Path A — spiky (LOCKED today) | Path B — cap-everything (Matt's target / D2 / PoE) |
|---|---|---|
| Resist budget | ~1.5 units total (anti-tax guard: max 1.60 < 2.0) | ~4.9–5.25 units (cap all 7 at 0.70–0.75) |
| What a built player looks like | high on 1–2 elements, ~0 elsewhere | ~capped on all 7, little headroom for anything else defensive |
| "Bring the right form" means | match your *spike* to the boss's signature element | bring *overcap + the right counter* to THIS rare pack |
| The threat | the one element you didn't build | the rare/unique monster that strips your cap |
| Genre cousin | lite-MOBA elemental matchup | **D2 Hell / PoE maps** |
| Anti-tax guard | budget ≪ cost-to-cap (capping impossible) | budget ≈ cost-to-cap (capping achievable-but-total) |

The two designs sit at **opposite ends of the same guard.** Path B doesn't *delete* the anti-tax guard — it **re-aims** it from "capping is impossible" to "capping is achievable but consumes ~the whole defensive budget."

## Why Path B is NOT the dm=6.0 tax the wave rejected

The wave rejected dm=6.0 because it **raised per-hit damage** until the unmatched cohort cliffed 0.50→0.00 — floor-crushing. Path B does **not** touch per-hit damage. It makes capping *necessary AND achievable*. The safety condition that separates Path B from the PoE under-cap tax is exactly:

> **capping must be ACHIEVABLE within budget.** Necessary-but-achievable = the genre standard (works). Necessary-but-UNachievable = the PoE one-shot tax (the failure). The current guard sits at "unachievable" — which is safe *only because capping isn't required.* The moment you make capping matter without making it reachable, you've built the tax.

So Path B's load-bearing requirement is the **all-resist affix + adequate budget** (below). Without them, Path B *becomes* the tax. With them, it's D2 Hell.

---

## What D2/PoE actually do — the three structural pieces (Legolas-grounded)

Both games make capping **mandatory-but-costly** via three pieces we'd need to build:

### 1. A cost structure (so capping competes with offense)
- **D2:** Hell applies **−100 to all resists**; you stack **+175/element** just to reach the 75% cap. Resist isn't bonus power — it's *climbing out of a hole*, and every slot spent climbing is a slot not spent on offense.
- **PoE:** **−60% campaign penalty** (−10%/act ×6); you stack **+135/element**. Same opportunity cost via gear-suffix competition.
- **Us, today:** resist starts at **0** and there's no hole. **If we simply raise the budget to 4.9 units with no cost structure, capping becomes a free flat baseline everyone gets — the worst outcome (mandatory tax, zero decision).** Two ways to create the cost:
  - **B1 (deficit, D2/PoE-literal):** add an endgame baseline penalty resist climbs out of. *Faithful but gratuitous — it imports a difficulty-tier artifact (Normal→NM→Hell) we don't have.*
  - **B2 (slot-competition, native):** keep resist starting at 0, set the budget so capping all 7 consumes ~the entire **defensive** affix budget, and let **offense compete for the same gear slots.** You choose: cap (survive) XOR load offense (kill fast). **My lean: B2** — it produces the identical opportunity cost without bolting a "Hell penalty" concept onto a game that has no difficulty tiers.

### 2. The all-resist affix (the efficient capping path)
- Both games have **"+X to ALL resistances"** as the gear-efficient source, *alongside* higher-rolling per-element affixes. Capping 7 elements off per-element rolls alone is brutal; the all-resist affix is what makes uniform capping a *puzzle* instead of a slog.
- **Us, today:** we mint **per-element `element_resist` only** (`gear_generation.py:969-980`). **Concrete ask to rocket if Path B:** add an `all_element_resist` mint branch (distributes a smaller value across all 7). This is the single most important generation piece for Path B viability.

### 3. The resist-reduction monster cycle (Matt's rare/unique ask — what keeps capped resists LIVE)
This is the part Matt explicitly wants and it's the **payoff** of Path B — without it, a capped player has *solved* defense and the system goes inert. Legolas gives the taxonomy:
- **D2 model — spiky/brutal:** Conviction aura on a rare pack applies **−75%** at common Hell levels → a **75%-capped player drops to 0% against that pack.** Max-resist does NOT protect (it caps how *high* you go, not how far you're *reduced*). Location-based, terrifying, build-defining ("the single most threatening affix for elemental builds").
- **PoE model — layered/granular:** Elemental Weakness (−15–30%) + Exposure (−10–15%) + penetration (34%) + −max-resist map mods (−9–12%), with **overcapping (to 90%+) as the buffer.**
- **Legolas's divergence note (important):** our system (always-hit, 0.95 formula clamp, no immunity wall, linear scaling) is **structurally closer to PoE.** The PoE layered-reduction-plus-overcap model fits us; D2's binary immunity wall does not.

---

## The beautiful structural fit: our overcap headroom is ALREADY the PoE buffer

The formula clamps at **0.95**; gear caps each element at **0.80**. That **0.80→0.95 headroom** — which I flagged in the explainer as "reachable only from non-gear sources" — **IS PoE's overcap buffer, already built into our math.**

- A reduction pack applies −0.20 to your fire resist. At 0.80 gear-cap you drop to 0.60 against that pack. With an overcap source pushing you to 0.95, you drop to 0.75 — still capped.
- This gives **non-gear overcap sources** (set bonuses, spirit-guide, a keystone) a *reason to exist* and a clear role: **buffer against the reduction cycle.** Exactly PoE's design.
- **Path A leaves this headroom inert. Path B gives it purpose.** The formula needs **no change** to support Path B — this is a generation-budget + affix + monster-content change, not a math-model change. That materially lowers the cost of choosing B.

### One sub-decision the reduction cycle forces: the amplification floor
Our formula clamps resist at **`max(0.0, …)`** (`math_model.py:116-128`) — so reduction can at most strip a player to **0% (full damage), never negative (amplified >100%).** D2/PoE both go negative (Conviction/penetration → take 130%+). **Design knob:**
- **Keep the 0.0 floor for the player** → reduction is gentler (full damage is the worst case). *My lean — fits the always-hit-no-dodge floor; amplification on top of unavoidable hits is over-punishing.*
- **For monsters as defenders, allow negative** → penetration as the offense reward (already partially there via the floored monster path). Asymmetric floor is defensible and probably correct.

---

## My recommendation

**Path B (cap-everything-but-costly), implemented as B2 (slot-competition), is what Matt has described — twice — and it is the genre-canonical, internally-coherent model.** I recommend adopting it AS A DELIBERATE PIVOT, with eyes open that it retires the spiky-anti-tax design the typed-resistance wave just locked.

**But three conditions gate it, and they must land together or Path B becomes the PoE tax:**
1. The **all-resist affix** (rocket) — non-negotiable; it's what makes capping achievable.
2. The **budget raised to ≈ cap-everything cost** (gamora/rocket calibration) — *and not past it* (past it = free flat tax).
3. The **reduction-monster cycle** (the rare/unique groups Matt wants) — or capped defense goes inert.

**Do NOT** raise the budget without (1) and (3). A high resist budget with no all-resist affix = an unachievable mandate = the tax. A high budget with no reduction cycle = a solved, boring baseline. The three are a set.

**What stays mine vs. routes elsewhere:** I own the design recognition and the player-experience spec (what must be *proven*: capped players sweat-not-die against reduction packs; resist genuinely competes with offense; no one-shot under max reduction). The **budget/affix/cycle numbers are a gamora+rocket calibration job under jack-ryan's gate** — not my call to set.

---

## Matt's sim-methodology question (test cycles vs averages)

**You do not need to sim the element×resist grid — it's deterministic.** `damage_taken = incoming × (1 − resist)` is a multiply; the full player-resist × encounter-element grid is **analytically free** (the §5 table in the explainer was computed by hand, no sim). Sim is only needed for the **dynamic fight outcome** (survive + kill, which depends on HP/timing/rotation).

So the answer to "test cycles in sim, or averages?" is **neither extreme — a bounded representative enum:**
- **Don't** sim every monster-element permutation (combinatorial explosion).
- **Do** define a **small fixed set of rare/unique modifier archetypes** — exactly as D2 ships **~5 champion types + ~13 boss affixes** (a bounded enum, not a combinatorial space). Candidate archetypes: *resist-stripper (Conviction-pack)*, *high-elemental-burst*, *all-resist-tank*, *penetration-boss*, *dual-element*. Sim each against a representative spread of player builds.
- That's tractable on compute AND it's the genre-proven structure. The cycling Matt wants **is** an enum of modifier archetypes, not a continuous space.

---

## What this gates / what stays Matt-gated

- **Surfaces (for Matt's decision):** Path A vs Path B. This is a foundation pivot off a just-locked decision — Matt's call, not mine.
- **If Path B:** three sequenced build pieces (all-resist affix → budget recalibration → reduction-monster cycle), each a gamora/rocket/jack-ryan workstream. The reduction cycle is itself a multi-wave build (≈ the proxy's weight) — Matt-gated.
- **If Path A:** the explainer + anchor ruling stand as-is; "bring the right form" = spike-matching; the 65–75%-on-everything target is consciously abandoned and should be recorded as such so it doesn't drift back in (Discipline #13).
- **Unchanged Matt-gates:** content emission; all push; the proxy build.
- **No code touched by this note.** It is a design recognition + recommendation only.
