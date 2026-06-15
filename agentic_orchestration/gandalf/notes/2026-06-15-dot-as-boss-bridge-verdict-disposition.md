# DoT-as-boss-bridge — diagnostic CLOSED, branch named, re-scope verdict

**Type:** gandalf design-judgment + recognition record (closes the read-only diagnostic from `2026-06-15-dot-as-boss-bridge-investigation-brief.md`).
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-prompted diagnostic ("Could it be that we have not yet included physical ailments?"); evidence returned by gamora (Q1 sim read) + rocket (Q2/Q3 composition+magnitude read); design-judgment + branch-naming is gandalf's per brief §6. Routing/sequencing to KR.
**Status:** Diagnostic CLOSED on evidence. Re-scope recommended + GATED (see §3).
**Verified independently:** `damage_resolver.py:991-998` (_add_or_refresh no-stack) + `:983-985` (tick_scale keys on int/wis, DEX rogue gets 1.0) read first-hand 2026-06-15. Both load-bearing claims confirmed.
**AMENDED post-Q4 (2026-06-15):** see `2026-06-15-dot-verdict-Q4-foldin-and-power-tier-control.md`. Q4 reinforces verdict (a)'s direction (geometry/affix/power_tier are not composition fixes; the tree converges on the sim bleed lever) BUT caught a confound this disposition missed — the arc's envelope-vs-b6 comparison ran at mismatched power_tier (50 vs 58) on the known brute-force kill lever. A matched-power_tier **control re-run** is now inserted BEFORE the bleed fix, and the fix is split (robust DEX-scaling correctness bug vs control-gated boss-efficacy magnitude lever). The §3 sequencing below is superseded by the addendum's §5.

---

## 0. One line

DoT IS selected and IS flavor-realized — but for a STRUCTURAL no-stack reason in the sim, not a missing-selection or small-constant reason. The tree didn't anticipate this exact shape: it's a **Branch 2 variant where the lever relocated from generation to sim ailment-resolution architecture.** Re-scope warranted = **(a) sim-side single-strong-stack scaling at `_add_or_refresh`**, the genre-correct (PoE-bleed) model — GATED behind the role-floor chain.

## 1. The branch we landed in — and why the tree didn't cleanly hold it

My §3 tree had three branches. Map the evidence:

| Brief §3 assumption | Evidence returned | Match? |
|---|---|---|
| b6 brute-forces the boss (Q1) | CONFIRMED — direct-hit 94.58%, burn 5.42%, ~19× ratio; power_tier-58 flat-magnitude inflation | ✅ my bet held |
| rogue does NOT select DoT (Q2) | REFUTED — envelope rogue selects bleed on 5/10 damage skills | ❌ my bet wrong |
| bleed is flavor-magnitude (Q3) | YES-ISH — flavor-to-moderate realized (one-instance-worth, 3-4% boss HP per application) | ✅ but for the wrong reason |

So we are **NOT in Branch 1** (the hoped-for "doesn't-select + flavor" → re-bias-selection-and-scale). The rogue already selects DoT richly — my role-floor fix *incidentally* raised it (ceil(0.25×13)=4 area_damage skills carry the highest 0.50 ailment_chance). The selection problem is already solved, by accident, by adjacent work. That is a genuinely good finding: **the generation layer is producing the genre-correct bleed-rogue identity.** It just doesn't *land* as primary damage.

We are **closest to Branch 2** ("selects-DoT-but-flavor → magnitude fix") — BUT the brief's Branch 2 assumed the fix was a "pure magnitude scale (lighter touch than re-biasing selection)." That assumption is **wrong in mechanism.** The realized magnitude is low NOT because the per-tick constant is small — rocket showed the tick is large (750/sec at tier 50, 1009/sec at tier 58; a single 5s application is already 3-4% of the 123k boss). It's low because:

1. **No-stack (the architectural cap).** `_add_or_refresh` (damage_resolver.py:991-998) matches on ailment NAME — all 5 bleed-skills collapse to ONE refreshed instance. Five bleed-applying skills do the boss-damage of one. Verified first-hand.
2. **DEX rogue gets no tick_scale.** `tick_scale = 1.0 + eff_attr*0.003` keys on `intelligence`/`wisdom` (line 983). A DEX rogue's bleed never amplifies. Verified first-hand. *This is itself a thematic bug — the physical-ailment class is the one class whose ailment scaling stat it doesn't possess.*
3. **35% per-hit application gate** caps realized uptime well under the 100%-uptime bound.

So Q3-as-I-framed-it ("is 0.12 flavor or primary") was a **category error** — 0.12 is `_EFFECT_POWER_WEIGHT["bleed"]`, a gear power-budget normalization weight, never a tick value. I cited the wrong number. The honest read: the question I should have asked was *"does the sim let bleed accumulate to primary-tier?"* — and the answer is **no, by architecture.**

**Is the falsifier (Branch 3) triggered?** NO. Branch 3 = "DoT already selected AND already primary-magnitude AND still zero boss kills → DoT is not the lever." We are not there: DoT is selected (yes) but is NOT primary-magnitude — it is architecturally CAPPED below primary. The DoT hypothesis is **NOT falsified.** It is *confirmed with a relocated lever*: DoT genuinely can bridge the swarm/boss gap, but only after a sim-side change lets it. The b6-route-around (Option 2) is NOT earned — the cheap composition lever (selection) came up *already-solved*, and the next lever (sim stacking) is identified and actionable.

**Naming it precisely:** this is **Branch 2-architectural** — a refinement the tree didn't anticipate. Selects-DoT (refuting my Q2 bet), flavor-realized (confirming my Q3 bet), but the cause is structural no-stack, so the fix relocates from generation/constant (rocket's seam, what Branch 2 assumed) to sim ailment-resolution (gamora's seam, what Branch 2 did NOT assume).

## 2. Design-judgment — re-scope verdict: (a), the genre-correct sim change

**Re-scope IS warranted.** The verdict is **(a): a sim-side single-strong-stack scaling change at `_add_or_refresh`** — NOT (b) pure magnitude tune, NOT (c) accept-and-route-via-b6.

Reasoning, on the three sub-options:

- **(b) pure magnitude/uptime tune is REJECTED.** You cannot tune your way to primary-tier through the no-stack wall without making a *single* bleed application grotesque. To hit ~40-50% boss HP from bleed via one instance, the per-tick has to roughly double-to-triple — which then makes the SAME bleed delete swarms in one tick and trivializes elites. The no-stack cap is precisely what makes the "scale the constant" path produce a monster. The lever is not magnitude; it is accumulation. (b) is the wrong knob.

- **(c) accept-and-route-via-b6 is REJECTED — NOT earned.** Per my own falsifier discipline in §4 of the brief: Option 2 is earned only when DoT *and* the adjacent levers all come up empty. They did not. Selection came up already-solved; the sim-stacking lever is identified and cheap relative to a new ailment. Routing around via b6 here would pay real architectural debt (b6 as permanent hand-authored answer key) to avoid a change we can see and name. We do not pay that debt.

- **(a) sim-side single-strong-stack scaling is the verdict.** This is the genre-correct model, and the precedent matters:
  - **PoE bleed = single-strongest-stack.** Only the largest bleed applies; new applications overwrite if stronger. This is *almost exactly* what `_add_or_refresh` does today — EXCEPT PoE bleed magnitude scales hard with the attacker's damage + ailment-effect, so the single stack is *enormous* and carries boss fights. Our single stack is capped at flat-tier value with no DEX scaling, so it's a garnish.
  - **PoE poison = stacks unboundedly.** Many small instances summing — the assassin's boss-bridge.
  - The genre offers BOTH as valid DoT-rogue identities. Our engine already implements the *shape* of PoE-bleed (single-instance overwrite) — so the minimal, genre-faithful, lowest-architectural-blast-radius change is: **keep single-instance, but make that instance scale to primary-tier for the physical-ailment class.** Two concrete sub-levers for gamora to weigh:
    1. **Extend tick_scale to DEX** (or to the class's primary offensive stat) so the physical-ailment class actually amplifies its own physical ailment. This is the bug-shaped half — it's nearly indefensible that bleed is the one ailment whose scaling stat its native class can't possess. Fixing this alone may move bleed from 3-4% to a moderate-but-real boss contributor.
    2. **Single-strongest-stack-with-magnitude** (true PoE-bleed): on refresh, take `max` of the *tick magnitude* (not just duration), and let that magnitude carry attacker damage-scaling. Keeps the one-instance simplicity, makes the instance matter.
  - I do NOT recommend converting bleed to unbounded-stacking-poison. That's a bigger sim change, a different genre identity (poison-assassin, not bleed-rogue), and poison doesn't even exist yet (P2). Single-strong-stack is the smaller, truer change and it's the model the code already gestures at.

**What "primary-tier DoT" should mean (my genre-target judgment, the thing brief §6 says I own):** primary-tier means a DoT-rogue's bleed should be able to carry **~40-60% of a boss fight's damage** with the *hits* carrying the rest — so the kit is swarm-strong-via-hits AND boss-strong-via-bleed, ONE kit, no per-tier modifiers, exactly the bridge I argued in §1 of the brief. It does NOT mean bleed should one-shot swarms (duration-gated DoT inherently barely ticks on a 2s swarm death — the mechanism self-balances against trash). The target is: on a 30-60s boss fight, a DEX rogue who selected 5 bleed skills should SEE bleed climb toward half the damage bar. Today it sees 5.42% (b6) / capped-flavor (envelope). That gap is the re-scope.

**Player consequence (the anchor):** today, a rogue that "looks like" a bleed-assassin in its kit composition plays like a hit-stacker with a cosmetic bleed number that never matters — the player reads the skill tooltips promising bleed, builds for it, and watches direct hits do 19× the work. That's the *performance of an identity* without the identity — exactly the hollow-journey failure I'm here to catch. A Last Epoch DoT-rogue or PoE bleed-bow player FEELS the boss melt over the fight from the stack they built. Our player feels nothing from the bleed they selected. Fixing (a) makes the selected identity real.

## 3. Sequencing — CONFIRMED, holding the change for post-role-floor

**Confirmed: I am holding the change for post-role-floor.** Per brief §5 and my own one-variable-at-a-time discipline:

- The diagnostic was read-only + concurrent-safe — fine, it ran clean against the in-flight role-floor validation (a read shifts no WR).
- The FIX (a sim-side bleed-scaling change at `_add_or_refresh` / tick_scale) is **WR-shifting and must NOT land mid-role-floor-chain.** It sequences AFTER the in-flight role-floor chain + its G7 WR re-pass closes. Clean attribution: we cannot distinguish a role-floor WR delta from a bleed-scaling WR delta if both land in the same pass.
- This also composes correctly with the *content* of the finding: the role-floor fix is what INCIDENTALLY raised bleed-selection in the first place. So the bleed-efficacy change wants the role-floor histogram STABLE underneath it — another reason to let role-floor close first, then land the sim change against a settled selection distribution.
- The change is gamora's seam (sim ailment-resolution), NOT rocket's (generation). When it fires, it's a gamora balance-loop increment + a gandalf-locked tuning sign-off per Discipline #16 (the tick-scale/stack-magnitude change is a locked constant/mechanism change, not free tuning).

## 4. What I got wrong, recorded honestly

- **Q2 bet wrong:** I bet the rogue likely doesn't select DoT. It selects bleed on half its damage skills. My own role-floor fix raised it. Good — the generation layer is healthier than I feared.
- **Q3 framed on a category error:** I cited 0.12 as the bleed magnitude. It's a gear power-budget weight, never a tick value. The real tick is large; the cap is structural. I asked the wrong question (magnitude) when the right one was architecture (accumulation).
- **What held:** Q1 (brute-force, my bet) and the core hypothesis — DoT IS the genre-correct bridge for this shape, and it's NOT falsified. The lever just sits one layer deeper than the brief's tree drew it.

## 5. Recommendation to KR (one line to carry to Matt)

Diagnostic CLOSED. **Branch 2-architectural** (selects-DoT, flavor-realized, lever relocated generation→sim). DoT hypothesis **confirmed, not falsified.** Re-scope = **(a) sim-side single-strong-stack bleed scaling at `_add_or_refresh` + extend tick_scale to the physical-ailment class's offensive stat** — genre-correct (PoE-bleed model), gamora's seam, gandalf-locked tuning. **GATED behind the role-floor chain + G7 WR re-pass** for clean attribution. Option 2 (route-around-via-b6) explicitly NOT earned.

---

**Signed:** gandalf, 2026-06-15
