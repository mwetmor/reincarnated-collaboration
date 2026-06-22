# Path B × the defensive-axis recal — the homogenization-guard reconciliation

**Author:** gandalf (design seam). **Mode:** Pattern-B, verification-first. **Status:** cross-thread design recognition — NOT a ruling. It reconciles two just-landed decisions that, uncaught, collide. It is an INPUT to (a) jack-ryan's Gate-1 on the Path B spec and (b) the entry conditions for Path B Step 1c. **(Correction below: the "defensive-axis recal wave" this originally paired with 1c is the typed-resistance spine, already CLOSED at G-C — not a pending wave.)**

**Reconciles:**
- `2026-06-22-path-b-resist-design-spec.md` (Path B: resist a mandatory-but-costly baseline, ~0.75 on all 7).
- `2026-06-21-monster-to-player-calibration-design-half.md` §11.3 — **the homogenization guard** (Matt ruled death is a core pillar; the prime calibration constraint).
- gamora's defensive-axis diagnose (`simulation/math/defensive-axis-calibration-diagnose-2026-06-21.md`, jack-ryan Gate-2 PASS-WITH-INFO): `MOB_DAMAGE_SCALE` 0.40→4.0 is the primary death lever; the guard is *satisfiable* (offense partially substitutes for defense; no mandatory armor floor).

---

> **⟢ CORRECTION (verification-first re-read of the G-C close, post-authoring).** §3/§4 below frame "the defensive-axis recal" as a SECOND, still-pending Matt-gated wave (flat `MOB_DAMAGE_SCALE` 0.40→4.0) going live *alongside* Path B. **That is stale.** A direct re-read of the decisions-log G-C close establishes:
>
> - **There is no separate pending defensive-axis recal wave.** The decisions-log names the TYPED-RESISTANCE spine itself "the defensive-axis recalibration wave" and marks it **CLOSED at G-C** (2026-06-21, line 4566). The defensive axis is a **single, already-closed COMPOUND** — armor + per-element resist + the dm=5.0 death channel — **jointly calibrated and ratified at the Path A budget** (G-A: max total resist N·r = 1.50 < 2.0; line 4576).
> - **The flat `MOB_DAMAGE_SCALE` 0.40→4.0 knob-set is MOOT,** not pending — explicitly invalid under the resolver (G-D, line 4579: "fit to the flat equation and are MOOT under the resolver"). The "pending wave / knob-set / not-yet-authorized" text that seeded §3 is the **struck-through, CLOSED revisit item** at line 4619, read as live.
> - **The compound guard WAS validated on the joint compound** (the G-C close is a *two-axis joint* close), not "on the physical axis alone" — at the **Path A budget.**
>
> **What survives unchanged:** §2 (Path B is guard-compliant by construction — the clause-by-clause §11.3 mapping) and the §3 boxed criterion (*evaluate the guard on the COMPOUND, not per-axis*). Both are **reinforced** by the correction, not weakened — the compound is already joint, and Path B re-opens it jointly.
>
> **What the correction SHARPENS — Path B 1c re-opens the CLOSED G-C compound at a ~3× budget, and the re-open has TWO failure modes, not one:**
> 1. **Compound tax (the §3 original concern):** budget too demanding relative to slots → must buy both defensive floors before any offense → the build screen becomes a checklist (D4-launch one-shot-meta / PoE mandatory-defensive-layers creep).
> 2. **Death-channel collapse (NEW — the stale framing hid this):** dm=5.0 was tuned so the thinnest cohort *barely* survives **at the Path A budget** (players eat near-full elemental on unmatched elements; thinnest unmatched mean_dur 12.4s vs cadence 4.5s — line 4579). Path B's ~3× budget means a capped player eats **~0.25× elemental** → the death channel softens → the already-soft **0.926 unmatched-survive median slides toward ~1.0** — the silence the typed spine was built to kill, returning. dm=5.0's *number* is unchanged; its *equilibrium with the resist budget* must be re-proven at 1c.
>
> **1c must thread BOTH:** capping achievable-but-costly (avoids the tax) **AND** death still real at the capped budget (avoids the collapse). That is the real needle; the per-axis-tax framing saw only half of it.
>
> **Net effect on routing — conclusions HOLD** (joint calibration; lean A co-calibrate). The coupling record's "3 strands" collapse to **2**: (1) the re-opened closed compound [was strands 1+2], (2) the army-soak [strand 3, survives intact — the third-axis non-gear-bypass recognition is sound]. The dm=5.0 "strand" is a re-validation obligation *inside* strand 1, not a separate wave. **Non-blocking for rocket-fire on Step 1a** (1a is schema widening, upstream; the correction binds at 1c).

## 1. The collision, stated plainly

The defensive-axis design-half §11.3 names its prime constraint using a **literal example**:

> *"PoE's capped-resist lesson: if calibration makes ONE defensive threshold mandatory ('**hit 75% resist or die to everything**'), defense becomes a TAX everyone pays identically, build diversity COLLAPSES to a single floor, and we achieve the OPPOSITE of the intent."*

The Path B spec §1 says:

> *"every endgame player is **expected** to reach ~0.75 on all 7 rotating elements."*

**On the surface, Path B is the exact thing the guard forbids.** "Hit 75% resist or die" *is* Path B's headline read. If a Gate-1 reviewer holds the defensive-axis note in canon — jack-ryan does — this is the obvious objection, and it is a fair one. It must be answered explicitly, not left implicit in the spec's internals.

---

## 2. The resolution — Path B is "capped-resist done right," the careful version the guard's own example warns against doing *wrong*

The §11.3 guard is not "never have a resist cap." It is "don't make a single defensive threshold a **uniform, un-substitutable, build-collapsing** tax." It then states the two conditions that make a defensive mechanic guard-compliant:

> *"(a) MULTIPLE defensive strategies work (mitigation OR avoidance OR sustain OR kill-speed), and (b) OFFENSE can PARTIALLY substitute for defense."*

Path B satisfies both **by construction** — this is what the slot-competition design is *for*. Mapped clause-by-clause:

| §11.3 requirement | Path B mechanism that delivers it |
|---|---|
| **(a) multiple strategies viable** | the three archetypes (spec §6.1): full-cap (mitigation), concentrated-cap-4 (selective mitigation + kill the rest), glass (pure kill-speed). All three viable is **CONCERN-2's measurable collapse-criterion** (spec §13.4). |
| **(b) offense substitutes for defense** | slot-competition: the 9 resist slots compete with offense; the glass kit spends 0 on resist and pays in survival, exactly the §11.3(b) "kill-speed" strategy. Spec §7. |
| **not a one-shot mandatory floor** | PoE-layered reduction, **NOT** D2 Conviction cap→0 (spec §11). Capping is necessary-AND-achievable, never necessary-but-unachievable. The amplification floor (spec §10) caps the worst case at full damage, never amplified. |

So the surface contradiction dissolves: **the difference between "the §11.3 tax" and "Path B" is precisely whether capping is a free-or-forced flat floor (tax) or a costly, substitutable, non-dominant choice (Path B).** The spec's whole architecture — achievable-but-total budget (§9.2), the three-piece set (§9), the non-dominance criterion (§13.4) — is the machinery that keeps it on the right side of the §11.3 line.

**This belongs in the Gate-1 record as the §11.3 reconciliation.** I recommend it be folded into the Path B spec (a one-paragraph cross-reference in §13, pointing here) by whichever gandalf instance is processing the Gate-1 concerns — I am not editing the spec concurrently to avoid a collision.

---

## 3. The genuinely-new output — the COMPOUND-FLOOR co-calibration constraint

§2 resolves the *elemental* axis against the guard. But the guard now has to hold against something §11.3 was written before: **a SECOND defensive axis is going live at almost the same time.**

- **Path B** makes the **elemental** defensive read live (resist, ~9 gear slots).
- **The defensive-axis recal** (Matt ruled B) makes the **physical/general** defensive read live (`MOB_DAMAGE_SCALE` 0.40→4.0 + armor/HP — gamora's validated knob-set).

These are **separate axes** (spec §14: armor ≠ elemental; `armor/(armor+3000)` vs the resist dict) — and separateness is GOOD for build space. But they **share one gear budget** and they go live in the same window. The §11.3 guard was validated by gamora **on the physical axis alone** (the homogenization sweep was armor/HP-vs-offense). It has **not** been validated on the *compound* of physical + elemental demand.

**The risk: a compound defensive tax neither axis exhibits alone.** Each axis can individually satisfy §11.3 (offense substitutes; no single floor) and yet, *summed*, force the player to pay both — cap resist AND hit the armor/HP threshold to survive mob-scale-4.0 — leaving no budget for offense. At that point §11.3(b) fails on the **compound**: offense no longer substitutes, because you must buy both defenses before you may buy any offense.

**Player consequence (the anchor):** the build screen stops being a choice and becomes a **checklist** — cap resists, hit the armor number, *then* (if anything is left) play your fantasy. That is the **D4-launch one-shot-meta feel** the defensive-axis note spent its §11.3 explicitly warning against — and it is the well-documented **PoE "mandatory defensive layers" creep** (resists AND a life pool AND phys mitigation AND ailment avoidance, all before damage), the genre's canonical version of this exact failure. The compound is where it bites, not either layer alone.

### The constraint (design criterion — gandalf-owned)

> **The §11.3 homogenization guard must be evaluated on the COMPOUND defensive demand (elemental resist + physical mitigation), not per-axis.** Specifically: there must exist no single (resist-floor, armor/HP-floor) pair that is *strictly mandatory* across the encounter set; offense-substitution (§11.3b) must hold against the **sum** of both defensive demands; and the viable-build set must include kits that under-invest in ONE axis and compensate with offense or the OTHER axis. The glass kit (low both, kill-fast) must remain viable; the tank (high both, slow-safe) is the opposite extreme; the spread between them across **two** defensive axes plus offense is now a **3-way** build space, not 2-way — richer, but only if no corner is forced.

---

## 4. The sequencing implication (recommend to KR; calibration is gamora's)

Path B Step 1c (budget recalibration) and the defensive-axis recal are **both gamora calibration jobs, both touching the same post-1a sim Loadout and the same gear budget.** Calibrating them independently is how the compound tax slips in. Two clean options:

- **(A) Co-calibrate** — run Step 1c and the defensive-axis recal as ONE two-axis calibration against the compound guard. Cleanest; one validation over the real (elemental+physical) surface. My lean.
- **(B) Sequence with the compound guard as an explicit entry condition on the second** — whichever calibrates second must hold §3's compound criterion against the first's locked values, not just its own axis.

Either way, **the defensive-axis recal wave (currently Matt-gated) and Path B Step 1c are now coupled** — they cannot be validated in isolation. This is a KR sequencing input and a gamora calibration constraint, both under jack-ryan's Gate-2.

**Note on independence elsewhere:** this coupling is *only* at the calibration step (1c ↔ recal). Path B Step 1a (sim Loadout widening) and Step 1b (breadth affix mint) are unaffected — they build the machinery; the compound guard binds only when the numbers are set.

---

## 5. Proof obligation (extends Path B §13 + defensive-axis §11.3)

Add to the §13 proof set, evaluated at the co-calibration (or the second calibration if sequenced):

5. **The compound defensive read is not a tax.** Run the reference shapes across both axes: a kit may under-invest in resist OR in armor/HP and remain viable by compensating (offense, or the other axis). No (resist-floor + armor-floor) pair is strictly mandatory. Offense-substitution holds against the **summed** defensive demand. If the only viable kits are those that pay both defensive axes near-fully, the compound tax has formed — calibration fails this obligation regardless of how each axis scores alone.

The numeric thresholds are gamora's to set and jack-ryan's to ratify (per spec §17). My contract is only the *shape* of the test: the guard is a **compound** guard now.

---

## 6. What's mine / what routes

- **gandalf owns:** the §2 reconciliation (Path B is guard-compliant by construction), the §3 compound-floor criterion, the §5 compound proof obligation. These are design criteria.
- **Routes to gamora under jack-ryan's gate:** the co-calibration (or sequenced calibration) of Step 1c + the defensive-axis recal against the compound guard; all numbers, including the dominance margin and the floor thresholds.
- **Routes to KR:** the §4 sequencing decision (co-calibrate vs sequence-with-entry-condition) and the recognition that the defensive-axis recal wave is now coupled to Path B Step 1c — neither validates alone.
- **Feeds:** jack-ryan's Gate-1 on the Path B spec (§2 is the answer to the §11.3 objection); the entry conditions for the Matt-gated defensive-axis recal wave.
- **No code touched.** Design recognition only.
