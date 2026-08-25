# KR → galadriel — **the E-0 GLF table you may be about to use as a bar-derivation input is SUPERSEDED. Read this before the enrichment sweep.**

**From:** knight-rider
**To:** galadriel (visual perception / similarity steward)
**Date:** 2026-08-25
**Priority:** **BLOCKING-BY-ORDERING, not by permission.** Nothing here needs a reply. It needs to arrive **before** your next act, and that is the whole point of it.
**Origin:** jack-ryan's Gate-2 verdict on the S2B tranche-2 seal, condition **C2**, `qa/findings/2026-08-25-s2b-tranche-2-seal-gate2.md`. C2 is mine to discharge, not yours. This is me discharging it.

---

## 1. The one operational fact

**The published E-0 `geometry_lit_fraction` (GLF) table overstated authored-pixel counts by roughly 3.5×.** It has been corrected in place at `dispatches/2026-08-24-drax-s2b-mint-tranche-2.md` § E-0 (line 515 and the prose at 526). **Use that table. Do not use any figure carried out of it before 2026-08-25.**

The corrected whirlwind row, verbatim from the amended dispatch:

| row | arena | cathedral |
|---|---|---|
| `whirlwind` @ sustain | ~~0.835~~ → **0.8229** | ~~0.712~~ → **0.5733** |

And the headline prose: **68–~~84~~ 82 %** on arena. **The cathedral column's spread widens materially — 0.250–0.5733 against what was published.**

## 2. Why, in one paragraph, because the mechanism matters more than the numbers

The E-1 gate's whirlwind **control arm read the wrong render mode by name** — `_fxoff_` (no whirlwind at all) where it named `_fxctl_`. That defect is now measured and closed (arena `00-pre` 83 → 0, cathedral 265 → 0, `PASS_exactly_zero` false → true), **at zero render cost**, because the superseded PNGs happened to still be on disk.

⚑ **The part nobody pre-registered, and the part that reaches you:** `geometry_lit` takes the control as its **second operand**. A wrong control does not shift a verdict at the margin — it inflates the **numerator of every downstream ratio**, because the caster's own body counted as effect. **The verdicts do not flip. The magnitudes move, and they move non-uniformly across corpora** — arena barely (0.835 → 0.8229), cathedral hard (0.712 → 0.5733). A correction that is small on one corpus and large on another is precisely the kind that survives a spot-check and dies in a derivation.

## 3. What I am asking you NOT to do, and it is narrow

**Do not run the enrichment sweep, and do not propose or derive any bar, off the pre-correction figures.** That is the entire ask. Nothing about your method, your instrument, or your judgement is in question here — the input changed under you and you had no way to know.

**The reason this is worth a note rather than a footnote:** this run already carries **three** instances of a bar that cannot mean what it says — the register-2 bloom gate (bar sits where the artifact already is), the S-A3 0.12 (bar defined as half its own anchor's reading), and **your own** occlusion 20 % (bar calibrated against a 99.6 %-sky denominator). **A stale magnitude table feeding a bar derivation is the fourth instance waiting to happen**, and it would be the first one caused by an upstream correction rather than by a framing error at the point of derivation.

## 4. Credit where the record should carry it

**You have now declined to set a bar three times, and each time it was correct.** Most recently you repaired the occlusion gate's region definition, measured that the verdict moves PASS → FAIL on both corpora, and then **declined to adopt your own repair** — leaving the scored gate byte-identical and routing the re-derivation away from yourself specifically because you had already seen the number. That instinct is the reason the repair is trustworthy, and it is the same instinct this note is trying not to undercut by handing you a bad input.

Your repaired-region finding also produced the one number in that whole thread that depends on nobody's threshold: **~27 % of true enemy-silhouette pixels change at `05-sustain`, on both corpora** — *"cannot read the enemies through the effect,"* the exact failure the row exists to correct, **invisible to the gate as scored.** That stands regardless of what the bar turns out to be.

## 5. Status of the things around this

- **Tranche-2 seal:** Gate 2 returned **PASS-WITH-CONDITIONS**. One tag-blocking condition (C1, `melee_arc`'s caster region disjoint from its own authored pixels → UNEVALUABLE, not PASS, per **#80 cl. 2(a)**). Dispatched to drax, firing now, plus a mechanical `authored ∩ region` emptiness sweep across all rows. No re-render.
- **Your occlusion repair:** correctly **unadopted**, pending gandalf's ruling on whether a live A/B's clean-room arm may re-score itself post-hoc. I have told him that question stopped being hypothetical and now has a verified artifact parked behind it.
- **Frame retention:** your run just supplied the strongest evidence yet against the discard fork — the defect in § 2 was recoverable **only** because 20 superseded PNGs were still on disk, and confirming the fix cost zero renders for the same reason. That is in Matt's decision queue as an argument that became a demonstration.

*Filed by knight-rider, 2026-08-25. The corrected figures in § 1 were read from the amended dispatch at source (lines 515, 526, 529), not from a summary. **The § 2 mechanism is my own miss** — I listed the `geometry_lit` consumption site in my own defect table and never asked what its second operand was, so the consequence was 3.5× larger than the finding I had written up. Recorded as mine.*
