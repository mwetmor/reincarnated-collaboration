# DoT-as-boss-bridge — bounded composition investigation (the sharp, falsifiable form of Option 1)

**Type:** gandalf design-investigation brief → KR to route (rocket + gamora); recommended next WS1 step.
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-prompted 2026-06-15 (*"Could it be that we have not yet included physical ailments?"* + *"is this a good next step?"*). Routing/sequencing pending KR; trigger pending Matt go.
**Parent:**
- KR rogue/b6 arc closeout — Lever C **composition verdict**: envelope rogue lands ZERO boss/elite/mini_boss kills even at M=1.0 (above the 0.65-killable calibration); b6 clears boss **0.967** at the SAME role histogram `{def:1, mob:2, area:4, burst:1}` → composition deficiency, not architecture, not genre-correct fragility.
- Engine ailment evidence (gandalf grep 2026-06-15): bleed EXISTS as the physical DoT (`element_biases.py:70` physical→bleed; `config/ailments.yaml`; `geometry_derivation.py:174` bleed+burst/area+physical→melee_arc; gear affix magnitude **0.12**; ticks every second for duration at 35% base application). Poison does NOT exist (`resistance_matrix.py:21,57` P2 candidate, not added).

---

## 0. One line

Run a **read-only diagnostic** (not a balance change) to test whether **DoT-selection / DoT-magnitude** is the composition lever that closes the rogue swarm-strong/boss-weak gap — more elegantly than b6's raw-power_tier brute-force, and as the genre-correct rogue identity. Three questions, one pass, falsifiable.

## 1. Why DoT is the genre-correct resolver of THIS shape

The rogue is swarm-strong, boss-weak. DoT DPS scales with **single-target fight DURATION**:
- Swarm dies in ~2s → bleed barely ticks → swarm damage comes from hits.
- Boss fight runs 30s+ → bleed stacks accumulate → boss damage comes from the DoT.

So ONE kit can be **swarm-strong-via-hits AND boss-strong-via-DoT with no per-tier modifiers.** This is exactly how PoE poison/bleed assassins and Last Epoch DoT-rogues bridge the trash→pinnacle-boss gap that pure-hit builds fall into. b6 "solves" the boss by cranking `power_tier` to 58 — a power-stat brute-force that is *less* genre-authentic than a DoT-bridged rogue would be.

This complements the role-floor work, it does not compete with it: **role floor guarantees the burst SLOT exists (count/presence); DoT is the EFFICACY mechanism that makes that slot actually kill bosses.** Count vs efficacy, composing.

## 2. The three-question diagnostic (READ-ONLY — no sim/balance change in this phase)

| Q | Question | Owner | gandalf bet |
|---|---|---|---|
| **Q1** | Does b6 kill the boss via **DoT ticks** or via **brute-force direct hits** at power_tier 58? | gamora (sim read) | brute-force |
| **Q2** | Does the **envelope rogue even SELECT** bleed/DoT skills+affixes in its kit? | rocket (composition read) | likely not / weakly |
| **Q3** | Is bleed magnitude (**0.12**) **flavor-tier** (small bonus on top of hits) or **primary-tier** (can carry a boss fight as the main damage source)? | rocket read + gandalf design-judgment on the target | flavor-tier |

## 3. Decision tree (what each outcome implies)

- **b6 brute-forces (Q1) ∧ rogue doesn't select DoT (Q2) ∧ bleed is flavor (Q3)** → the elegant fix: make rogue kits **select DoT** + scale bleed to **primary-tier** → one kit becomes swarm-strong-via-hits + boss-strong-via-DoT; b6's power_tier brute-force becomes unnecessary; genre-correct rogue identity restored. **This is the hoped-for result.**
- **Rogue selects DoT but it's flavor-magnitude (Q2 yes, Q3 flavor)** → fix is pure **magnitude** (scale bleed; lighter touch than re-biasing selection).
- **Rogue selects DoT AND it's already primary-magnitude AND still zero boss kills** → **HYPOTHESIS FALSIFIED.** The gap is NOT DoT; it's elsewhere (power/composition writ large). Option 2 (b6-as-net) gets stronger. Surface it; don't force the DoT narrative.

**Falsifier (keeps this honest):** the third branch. If DoT is already selected + primary + still failing, we do NOT have a DoT lever — report that plainly and the investigation closes Option 1 in favor of Option 2.

## 4. Constraints

- **Diagnostic phase is READ-ONLY.** It changes nothing in the sim or generation. It can therefore run **concurrently** with the in-flight role-floor validation without confounding the G7 WR signal (a read shifts no win-rate).
- **Poison stays a P2.** We do NOT need a new ailment to test this — bleed already exists to instrument. No new-ailment work in scope.
- **gandalf owns the design-intent** of what "primary-tier DoT magnitude" should mean (the genre target); **rocket/gamora own the engine read** (what the code actually does). Don't pre-impose the fix; read first.
- **Constants discipline (#16):** any eventual bleed-magnitude re-scope is a gandalf-locked tuning change requiring sign-off — out of scope for the diagnostic; in scope only if the read warrants it AND it sequences per §5.

## 5. Sequencing (clean attribution — the answer to "prompt the current session?")

- **Diagnostic (Q1–Q3 read): concurrent-safe.** Read-only; no WR shift; fire it in parallel with / independent of the in-flight role-floor chain. Does NOT confound the G7 HOLD-SIM re-pass.
- **Any resulting BALANCE CHANGE (DoT selection re-bias and/or bleed magnitude scale): sequences AFTER the in-flight b6/rogue role-floor chain + its G7 WR re-pass closes.** Same one-variable-at-a-time discipline as the queued perception-asymmetry wiring — we do not land a WR-shifting bleed change mid-role-floor-validation or we can't attribute the result.
- **Recommendation on session mechanics (KR's call):** do NOT inject the change into the live role-floor-validation session. Fire the diagnostic as its own scoped read (rocket + gamora); act on findings as a clean, separately-attributed increment once the role-floor chain closes.

## 6. Roles / acceptance

- **gamora:** Q1 — trace b6's boss-kill damage source (DoT ticks vs direct hits at power_tier 58).
- **rocket:** Q2 + Q3 — does the envelope rogue's composition SELECT bleed/DoT; is the 0.12 affix flavor or primary relative to a boss HP pool.
- **gandalf:** design-judgment on the "primary-tier" target + which decision-tree branch we're in + whether a re-scope is warranted.
- **KR:** route + sequence per §5; hold any change for post-role-floor clean attribution.
- **Acceptance (diagnostic):** the three questions answered with code/sim evidence + the decision-tree branch named. NOT a balance change — that's a separate, sequenced follow-on gated on the read.

---

**Signed:** gandalf, 2026-06-15
**For:** the bounded, falsifiable form of Option 1 — a read-only three-question diagnostic (does b6 brute-force the boss; does the envelope rogue select DoT; is bleed flavor-tier or primary-tier) testing whether DoT-selection/magnitude is the genre-correct composition lever that bridges the rogue swarm-strong/boss-weak gap, with a real falsifier (DoT already selected+primary+still failing → not the lever → Option 2 strengthens), the diagnostic safe to run concurrently with the in-flight role-floor validation because a read shifts no win-rate, and any resulting balance change sequenced AFTER the role-floor G7 re-pass for clean attribution.
