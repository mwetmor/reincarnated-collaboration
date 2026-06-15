# DoT verdict — Q4 fold-in + the power_tier attribution control (the un-confound before the fix)

**Type:** gandalf addendum to the DoT-as-boss-bridge disposition — folds in Q4 (the adjacent-lever read), names the methodology flag Q4 surfaced, and inserts a required control diagnostic BEFORE the sim bleed fix.
**Date:** 2026-06-15 (post-Q4; the disposition it amends predates Q4)
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-prompted (carried the KR DoT-diagnostic close + Q4 return to gandalf). Routing/sequencing to KR.
**Parent:** `agentic_orchestration/gandalf/notes/2026-06-15-dot-as-boss-bridge-verdict-disposition.md` (d32ead5 — the pre-Q4 verdict; Branch 2-architectural, re-scope (a) gated). Read it first.
**Evidence:** Q4 returned by rocket (envelope-rogue-vs-b6 composition diff, 3 axes) via the KR DoT-investigation session.

---

## 0. One line

Q4 **reinforces verdict (a)'s direction** (it closes off geometry / affix / power_tier as *composition-side* fixes, so the tree converges on the sim bleed lever) — but it also caught a **confound the disposition missed**: the arc's foundational "envelope worse than b6 at the SAME histogram → composition deficiency" comparison was run at **mismatched power_tier (envelope 50 vs b6 58)**, and power_tier is the *known brute-force kill lever* (Q1). The architectural conclusion holds; the positive attribution to *composition* does not — not until a matched-power_tier control re-run un-confounds it. **Insert that control BEFORE committing the sim bleed fix.**

## 1. Q4 — the three axes (rocket)

| Axis | gandalf bet | Finding | Net |
|---|---|---|---|
| **Geometry** (burst slot / boss-killer shape) | swarm-skewed, no boss-killer shape | **TRUE pre-fix, ALREADY FIXED post-fix.** Pre-floor envelope had zero burst slot (the ≥60 power_tier gate made burst structurally impossible at 50/58). The committed role-floor (52703c9, Rule B) now reserves a burst-role skill on the single_target boss-killer shape. b6 is single_target-saturated (8/13). | Lever was real; **already pulled by role-floor.** Reinforces "selection already solved." |
| **power_tier** | envelope below b6's 58 | **Not a composer deficit — a caller-supplied parameter.** The bc 8-tuple encodes no power_tier; the composer stamps whatever it's passed. gamora's harsh slice ran the envelope at **50**; b6 hard-codes **58**. At matched 58 the envelope stamps 58 across all 13 skills. | **The confound** (see §2). |
| **affix** | envelope below b6 | **Not a composer axis at all.** Affixes are a separate downstream gear seam; both kits inherit the identical path. No boss-relevant affix delta. If anything the envelope's per-skill scaling stamps are *cleaner* (DEX-scaled; b6 oddly stamps int/wis on a DEX rogue). | Closed off. Reinforces (a). |

**Net on the verdict:** the geometry/affix/power_tier landing-spots I wanted as the non-Option-2 escape hatch are **not composition fixes**: geometry is already pulled by role-floor, affix isn't a composer axis, power_tier is a free parameter. So there is **no cheaper generation-side composition change hiding in the kit** — the tree DOES converge on the sim bleed lever. Verdict (a)'s *direction* is reinforced, Option 2 stays un-earned. (This is the middle rung working: Q4 is the adjacent-lever read I added earlier this session; it earned its place.)

## 2. The confound Q4 surfaced — the disposition missed it

**The arc closed on:** "envelope rogue lands ZERO boss kills at the SAME role histogram {def:1, mob:2, area:4, burst:1} where b6 clears 0.967 → it's not the histogram (architecture), it's the kit composition." (Lever C held the global modifier M by fiat at 0.30 and 1.0.)

**The confound:** the envelope ran at **power_tier 50**, b6 at **power_tier 58**. Per Q1, **power_tier is THE brute-force kill lever** — "cranking 58 inflates the flat-magnitude legacy-path hits that kill the boss." power_tier sits **upstream of M** (it sets the base magnitudes M then scales). So the comparison changed **two** variables at once — composition AND the single most load-bearing damage variable — while attributing the entire outcome to one (composition). That is a one-variable-at-a-time violation **on the exact mechanism that does the killing.**

**What this does and does NOT overturn:**
- **HOLDS:** the *architectural* conclusion. M=1.0 zero-kills still rules out "a single global modifier can rescue the envelope." That conclusion never depended on the power match.
- **CONFOUNDED:** the *positive attribution* — "the gap is composition/bleed, NOT power." "Zero kills at M=1.0 is still damning" is only damning if pt50×M=1.0 ≥ pt58 base — and we do not know that, because pt is upstream of M. Confounded-but-suggestive still needs the clean run before a **sim balance change gets attributed to it.**

## 3. The required control (cheap; un-confounds before any fix)

**Control re-run (gamora; sim diagnostic; concurrent-safe — shifts no WR, fires now like Q1–Q4):**
> Run the **post-role-floor envelope at matched power_tier 58**, same histogram {def:1, mob:2, area:4, burst:1}, M=1.0, vs b6 at 58. Does the boss die?

- **If envelope@58 STILL ≈ zero boss kills** → the composition/bleed gap is **real and clean** → verdict (a) stands, now properly attributed → the sim bleed fix IS the lever.
- **If envelope@58 lands meaningful boss kills** → much of the "deficiency" was the **power_tier gap, not composition** → the bleed fix is **not the boss-efficacy lever** (matched power + role-floor already closes it); it demotes to a genre-correctness improvement (still real — see §4).

**Conditional follow-on (only if power turns out to be the driver):** what power_tier does the **production** envelope rogue actually receive at the boss content-tier? If production gives it < 58, the envelope is genuinely weaker at production power and b6-at-58 is an **inflated comparator** (b6 isn't a fair answer key) — which reframes the fix toward the power curve, not bleed. If production gives it ≈ 58, the pt50 slice was simply a harness artifact.

## 4. Split the bleed fix by justification-robustness (the precise move)

Q4 forces me to separate two things the disposition bundled as one verdict:

1. **DEX-scaling fix** (`tick_scale` keys on int/wis → a DEX rogue gets ZERO bleed amplification; verified first-hand in the disposition). This is a **thematic correctness bug, robust REGARDLESS of the power_tier control** — it is nearly indefensible that the physical-ailment class is the one class that cannot scale its own physical ailment. Justified now on correctness grounds; **lands gated** (still WR-shifting → after the role-floor chain, for attribution).
2. **Single-strongest-stack magnitude scaling** (the boss-efficacy lever — PoE-bleed model, at `_add_or_refresh`). Justified as **the boss fix ONLY IF the §3 control confirms a real boss-efficacy gap survives power-control.** If matched-pt closes the gap, this demotes from "the boss fix" to "not needed for efficacy." **Gated on BOTH the control AND the role-floor chain.**

The no-stack architecture (5 bleed skills → 1 instance) and the DEX-scaling bug are real facts either way. What the control decides is whether *fixing them* is the **boss-efficacy answer** or a **separate genre-correctness improvement** — two different justifications, two different priorities. We do not commit the magnitude-scaling balance change as "the boss fix" until the control disambiguates.

## 5. Revised sequencing

`role-floor G7 WR re-pass closes` → `matched-pt control re-run (§3; can fire NOW, concurrent-safe)` → **conditional on the control:** `bleed fix(es) (§4), gamora seam, gandalf-locked tuning per Discipline #16`.

- The control is a diagnostic (observation run; commits nothing; shifts no WR) → **fire it now**, concurrent with the in-flight role-floor chain, exactly as Q1–Q4 ran.
- The bleed fix(es) stay **WR-shifting → post-role-floor** for clean attribution, AND now **post-control** for clean *justification*.
- Route the control through the **existing KR DoT-investigation session** (continuation of the same diagnostic — clean attribution; do NOT spawn a parallel gamora).

## 6. What I'm recording honestly (extends disposition §4)

- The disposition (pre-Q4) **named the bleed fix without controlling power_tier.** It *knew* power_tier-58 was b6's brute-force lever (§1 table) but did not connect that to the envelope-vs-b6 comparison being run at mismatched pt. Q4 — the adjacent-lever read I insisted on adding as the middle rung — is what caught it. The framing-audit discipline (don't commit a fix on a confounded premise) worked *because* the middle rung existed.
- **Verdict direction unchanged; verdict attribution now gated on the control.** DoT/bleed is still the genre-correct bridge and the no-stack + DEX-scaling findings are robust. Whether the bleed fix is THE boss-efficacy answer is what the matched-pt control decides.

## 7. Routing answer (KR's question — "fold into gandalf canon, or hold?")

**Fold in NOW — done (this doc).** Do not hold for the sequenced fix: the flag changes the **next diagnostic step** (insert the control), and the work queue must not ossify around "just do the bleed fix" before the control runs. Carry to the KR DoT session: (1) read this addendum; (2) route the §3 matched-pt control to gamora as a concurrent-safe diagnostic; (3) hold the §4 bleed fix(es) behind both the role-floor re-pass and the control.

---

**Signed:** gandalf, 2026-06-15
**For:** folding Q4 into the DoT verdict — geometry/affix/power_tier are not composition fixes (the tree converges on the sim bleed lever, Option 2 stays un-earned), BUT Q4 caught that the arc's envelope-vs-b6 comparison was run at mismatched power_tier (50 vs 58) on the known brute-force kill lever, confounding the "composition-not-power" attribution; insert a matched-power_tier control re-run (concurrent-safe, fires now) before committing the sim bleed fix, and split the fix into the robust DEX-scaling correctness bug (justified regardless) and the boss-efficacy magnitude-scaling lever (justified only if the control confirms a gap survives power-control).
