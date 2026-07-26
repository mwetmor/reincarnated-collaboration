# DISPATCH — TCP-L8-U3c: take the box off the skills

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Authorization:** Matt, 2026-07-25, at the owner's eye.
**Lap:** L8 UI (T4-UI), **arm 3c.** Predecessors — arm 1 `…-tcp-l8u-hud-arrival-report.md`, arm 2
`…-tcp-l8u2-dark-fantasy-kit-report.md`, arm 3 `…-tcp-l8u3-compositional-depth-report.md`, arm 3b
`…-tcp-l8u3b-glass-and-candlefire-report.md`. **All yours, none blind to you.**

---

## §0 — Two things happened, and the second one is a conductor defect

**First: Matt ratified the candle VFX.** Verbatim — *"now that I've seen the candle VFX, I really
like it!!"* The glass drain landed too. **Neither is in play in this cell. Do not regress them.**

**Second: I amended arm 3b's dispatch mid-flight and the amendment reached nobody.** §7 of
`2026-07-25-drax-l8u3b-glass-and-candlefire.md` carries a ruling you never saw, because you were
already running and **there is no channel to a running cell.** I have now confirmed this twice this
lap (the weapon-wheel steer, and this). It is written into the charter as **L-R — a dispatch is
delivered once; an amendment authored after launch does not exist. A changed ruling means a new
cell, not an edited file.** That is the whole reason this dispatch exists as its own arm.

---

## §1 — The brief, in Matt's words, unedited

> *"the or is: we can just use the bat wings. left-hand side, third from the top here: [reference
> sheet]. Regardless, please look at that image as the bar surrounding the skills in our HUD is now
> way too big. But now that I've seen the candle VFX, I really like it!! We just need to remove that
> box around the skills and instead either use exactly what's around the skill boxes in the bat
> wings version or whats around the skill boxes in the candles version from that image above."*

**Two admissible answers, both named by the owner. Choosing between them is yours.**

The sheet is `matt_notes_handoff_docs/recent-synty-packs/synty-dark-fantasy-hud-recommended-uses/01_INT_DarkFantasyHUD_Components_ActionBars_*.png.webp`.
Its layout is irregular and I had to hunt for "third from the top on the left-hand side" myself, so
**I have resolved the identity of both exemplars for you and cut them**, at:

```
~/Games/mcp-lab/l8ui/ref3c/  SHEET_01_ActionBars.png     (the whole sheet, 1568×882)
                             PANEL_batwings.png  / _3x   ← Matt's "bat wings version"
                             PANEL_candles.png   / _3x   ← Matt's "candles version"
```

**I have looked at both panels and I am deliberately not describing either one.** Arm 2 established
that when I enumerate, enumeration order becomes attention order, and that labelling it "inventory,
not recommendation" does not defuse it. Resolving *which* panel Matt meant is a fact and I owe you
it. Saying *what is good about it* is a steer and I do not. **Look at the pictures.**

The only design position I hold is unchanged from arm 1 and arm 2: **a HUD must answer "am I about
to die, and what can I do about it" in peripheral vision, during combat, without being looked at
directly.**

---

## §2 — What is honest about this cell, up front

**This is not a trim. It reverses your own arm-3 item-4 fix.**

Matt's arm-3 item 4 asked for a hotbar tray that *covered the skill boxes* — the greeble was
overlapping them. You solved it with the container. **The container that stopped the overlap is the
box that is now too big.** So the overlap returns the moment the box goes, and **it has to be solved
a second time, by different means.** That second solve is the actual work of this cell; the removal
is the easy half.

**★ And that makes arm 3c the program's first SUBTRACTIVE measurement.** TCP-52 ① concluded that
polish cost is **fixed per component family** and scales with layer count. Every datum behind that
was an *addition*. **Nobody has measured a deletion.** So:

> **Does removing a component family cost like adding one, less, or more?**

If removal is cheap, the law is about *adding* families and the discipline is "cap the count up
front." If removal costs like addition, the law is about *touching* families at all, and the
discipline is much harsher — it means early frame-family decisions are near-irreversible and the
serial-content pipeline must get them right on the first pass. **Either answer is a real finding.
I am registering no prediction and no number**, and I hold one suspicion only, qualitatively:
*I suspect the removal is minutes and the overlap re-solve is the whole cell* — which, if true,
means the cost never lived in the family at all but in the **constraint the family was discharging.**
Refute that freely; arm 3b refuted my last one and was better for it.

---

## §3 — Constraints (five)

1. **Floor `~/Games/mcp-lab/l8ui/`. New work in `ui3c/`. `ui3/` and `ui3b/` stay intact and
   renderable** — the A/B needs arm 3b re-rendered this cell, as you did for arm 2.
2. ★ **Measure the box, before and after, with the instrument you already built.** Arm 3b's
   true-HUD-alpha two-flat solve isolates HUD ink from background; it is the right instrument and it
   exists. I attempted a plate-vs-slot ratio myself on `FINAL_16x9_stone_healthy.png`, got column
   runs contaminated by mid-grey stone, and **stopped rather than publish it** — per L-Q, I do not
   ship numbers I cannot defend. **The measurement is yours.** At minimum: hotbar ink footprint as a
   fraction of frame, and whatever ratio you judge actually expresses "too big."
   **Matt's ruling is the authority. The number is the receipt, not the justification** — if the
   numbers come back saying the old box was fine, the box still goes.
3. **Do not regress the ratified work.** Six lit candles, the glass drain, the R-5 brightness-channel
   danger ramp, R-9. If the unbox forces a change to any of them, that is a **finding** — name it,
   do not silently absorb it.
4. **Two resolutions minimum**, the same two as every prior arm, so the four-arm strip stays
   comparable.
5. **Forbidden floors:** `~/Games/mcp-lab/project/` (substrate — read-only copies out only; sha
   `d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`, mode 0444, **verify at start
   and end**) · `~/Games/mcp-lab/l7vfx/` · `~/Games/mcp-lab/evidence/l5/`. Per-file sha, not
   directory-listing hash — your own arm-1 finding. **L-J binds: W-PRO stays parked.**

---

## §4 — What you ship

1. **FIRST_INTENT banked verbatim + authoring clock started before any work** (TCP-32).
2. **The fork resolved** — bat wings or candles — **as a veto-open ruling with reasoning.**
3. ★ **The overlap re-solve**, as its own ruling: what now discharges the occlusion job the
   container was doing, and why that is better or worse than a container.
4. **A/B at both resolutions:** arm 3b hotbar vs arm 3c hotbar, identical HUD state, identical
   frames, one instrument.
5. **Before/after footprint numbers**, per §3.2, with the instrument stated.
6. ★ **The iteration log split three ways: removal · overlap re-solve · everything else.** That
   split is this cell's payload and the reason it is worth running as its own arm.
7. **Rulings veto-open with reasoning. Read-list declared.**
8. **Clock closed, authoring separate from execution.**

---

## §5 — Exit predicate

1. §4.1–§4.8 present. 2. Substrate sha + `-r--r--r--` verified **start AND end**.
3. `mcp-lab/project/`, `l7vfx/`, `evidence/l5/` demonstrably untouched, per-file. 4. `user://` clean.
5. **Arms 1, 2, 3 and 3b artifacts still intact and renderable.**

**Honorable fallback (L-F):** an attributed blocker plus the best partial is a **PASS.**
**Ceiling-finding is a PASS (L-G)** — *"neither exemplar's treatment can carry 9 slots plus the
utility slot at 1080p and here is the sprite that fails"* is a first-class result.

**HALT to Matt:** any game-systems decision not yet made. The standing list is open and **not yours
to re-decide** — arm 1's three (escape clock, critical threshold, `primary_attack` in 7 of 10 kits),
arm 2's three (the 6 missing glyphs as a purchase fork, `Down_01` serving both `stun` and
`knockback`, the Ice-and-no-Water corroboration), arm 3's H-7…H-12, and arm 3b's H-14 (the R-5 /
glass monotonicity conflict). **Add to it; do not resolve from it.**

---

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`).

**Name anything in this dispatch that steered you.** The running tally of what I have done wrong on
this lap, so you can check whether I repeated any of it: arm 1 — named an exemplar and foreclosed a
branch. Arm 2 — enumerated 6 of 14 folders and made enumeration order into attention order. Arm 3 —
**ratified a cause I had not measured** (L-Q), and then called a font ceiling a purchase when the
fonts were already owned one pack over. Arm 3b — put a thumb on the scale by naming which verdict
was "worth more," and registered a claim about "cost" with no unit. **Tell me what it is this time.**

---

## SUPERSEDED — do not execute

**Stopped at ~6 minutes and replaced in full by `2026-07-25-drax-l8u3c-r-hotbar-backing.md`.**

Reason: a second owner ruling landed mid-flight — *"The only thing missing now from the UI is the
darker metallic grey design behind the boxes. We really do need one of them."* — which names the
exact failure mode this dispatch was steering toward. §2 here framed the cell as a **deletion** and
said *"the removal is the easy half"*, while §1 carried Matt's actual words, which say **use** what is
around the skill boxes. **A backing is required; the correct framing is a family SWAP, not a
deletion.**

**First deliberate application of L-R** (a changed ruling is a new cell, never an edited file) —
applied at minute 6 rather than as a third post-mortem. The partial floor at `~/Games/mcp-lab/l8ui/ui3c/`
is inherited by the re-dispatch, not discarded.
