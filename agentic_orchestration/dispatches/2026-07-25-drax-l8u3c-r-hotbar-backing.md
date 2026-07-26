# DISPATCH — TCP-L8-U3c (RE-DISPATCH): the box is too big; the backing stays

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Authorization:** Matt, 2026-07-25, two rulings at the owner's eye, the second landing mid-flight.
**Lap:** L8 UI (T4-UI), **arm 3c, re-dispatched.** Supersedes
`2026-07-25-drax-l8u3c-hotbar-unbox.md` **in full** — read this one, not that one.
Predecessors: arms 1, 2, 3, 3b, all yours, none blind to you.

---

## §0 — I stopped your cell at ~6 minutes, deliberately, and here is exactly why

A second owner ruling landed while you were running:

> *"The only thing missing now from the UI is the darker metallic grey design behind the boxes.
> **We really do need one of them.**"*

**That names the precise failure mode the first dispatch was steering you toward, and it named it
before it happened.** My v1 §2 said *"the removal is the easy half"* and framed the entire cell as a
subtraction — while §1 carried Matt's actual words, which say **use** what's around the skill boxes,
not remove it. My own ledger says which of those wins: arms 2 and 3 both recorded that **my emphasis
beats my disclaimers**, three laps running. So the honest expectation was that you would optimise
toward deletion because I built the cell to reward it.

**L-R was born ninety minutes ago** — *a dispatch is delivered once; an amendment authored after
launch does not exist; a changed ruling is a new cell.* I could not reach you. The cheapest moment to
apply that law is at minute 6, not at minute 46, so I applied it. **This is L-R's first deliberate
use rather than its third post-mortem.**

**Your ~6 minutes of work is on the floor and it is not wasted** — see §3.1.

---

## §1 — The brief: both of Matt's statements, verbatim, in order

**First:**

> *"the or is: we can just use the bat wings. left-hand side, third from the top here: [reference
> sheet]. Regardless, please look at that image as the bar surrounding the skills in our HUD is now
> way too big. But now that I've seen the candle VFX, I really like it!! We just need to remove that
> box around the skills and instead either use exactly what's around the skill boxes in the bat wings
> version or whats around the skill boxes in the candles version from that image above."*

**Then:**

> *"The only thing missing now from the UI is the darker metallic grey design behind the boxes. We
> really do need one of them."*

**Three things are settled by this and are not yours to re-open:**

1. **The candles stay.** His "or" branch — *use the bat wings instead* — was your H-13, the unstated
   second branch you correctly refused to invent. **He has now stated it and then declined it**
   (*"now that I've seen the candle VFX, I really like it!!"*). H-13 is discharged. **Do not regress
   the candle VFX, the glass drain, the R-5 brightness-channel danger ramp, or R-9.**
2. ★ **"Remove that box" is NOT "remove the backing." A backing is required.** Zero-backing —
   slots floating on the stone — is **out of scope**, however well it measures.
3. **"One of them" means one of the two he named.** Picking neither is not admissible. Which of the
   two, and how you adapt it, is entirely yours.

**The exemplars, identity already resolved for you** (the sheet's layout is irregular and "third from
the top on the left-hand side" took hunting):

```
~/Games/mcp-lab/l8ui/ref3c/  SHEET_01_ActionBars.png     the whole sheet, 1568×882
                             PANEL_batwings.png  / _3x   ← Matt's "bat wings version"
                             PANEL_candles.png   / _3x   ← Matt's "candles version"
```

**I have looked at both and I am describing neither.** Resolving *which* panel he meant is a fact I
owe you; saying *what is good about it* is a steer, and arm 2 proved that labelling a steer does not
defuse it. **Look at the pictures.**

★ **One textual observation I owe you, which I am explicitly NOT resolving.** His two statements use
different prepositions: *"what's **around** the skill boxes"* and *"the darker metallic grey design
**behind** the boxes."* **A frame around a slot and a plate behind a slot are different objects**,
and a panel may carry both. Whether he is naming one thing twice or two things once is a question to
answer **by looking at the reference and at our current HUD** — or to **HALT on** if the pictures do
not settle it. It is not a question I should answer from a chair.

The only design position I hold, unchanged since arm 1: **a HUD must answer "am I about to die, and
what can I do about it" in peripheral vision, during combat, without being looked at directly.**

---

## §2 — What is honest about this cell

**It is not a deletion. It is a REPLACEMENT of a heavy component family with a lighter one**, and the
first dispatch had that wrong in a way that mattered.

**The consequence I got right and which still stands:** this reverses your own arm-3 item-4 fix.
Matt's item 4 asked for a tray that *covered* the skill boxes because the greeble was overlapping
them, and you solved it with the container. **The container that stopped the overlap is the box that
is now too big.** So the overlap returns the moment it shrinks, and it must be solved a second time
by different means. **That second solve is the work of this cell; the resize is the easy half.**

★ **The program question, corrected.** TCP-52 ① concluded that polish cost is **fixed per component
family** and scales with layer count — and **every datum behind it is an ADDITION.** v1 asked what a
*deletion* costs. There is no deletion here, so the real question is:

> **What does it cost to SWAP one component family for a lighter one?**

If a swap costs like an addition, the law is about **touching** families at all, and early
frame-family choices are near-irreversible — which makes the serial-content pipeline's first pass
enormously load-bearing. If a swap costs materially less, the law is about **adding**, and the
discipline is just "cap the count up front." **I am registering no number and no prediction.** One
qualitative suspicion, freely refutable: *I suspect the swap itself is minutes and the overlap
re-solve is the whole cell* — which, if true, means the cost never lived in the family but in **the
constraint the family was discharging.** Arm 3b refuted my last suspicion and was better for it.

---

## §3 — Constraints (six)

1. ★ **RESUME `~/Games/mcp-lab/l8ui/ui3c/`; do not restart it.** The stopped cell left
   `hud_unbox.gd` (56 KB), `palette3c.gd`, `hud_unbox.tscn` and four inherited shaders on the floor.
   **Inspect it, keep what serves, and declare what you discard and why.** Its last emitted line was
   *"The probe was wrong — it measured adjacent-column difference, which a slowly-sloping thorn
   passes. Fixing the instrument."* — **that instrument defect is yours, real, and unfinished.**
   Per the TCP-52 ⑦ continuation protocol: **declare the clock in two segments with the ~6-minute
   prior segment named and treated as unattributable**, and a reconstructed FIRST_INTENT is
   admissible **if labelled as reconstructed.**
   `ui/`, `ui2/`, `ui3/`, `ui3b/` stay intact and renderable — the A/B needs 3b re-rendered.
2. ★ **A backing is required (§1.2). Measure its extent** — whatever ratio you judge actually
   expresses "too big," before and after, under the **arm-3b true-HUD-alpha two-flat instrument**
   you already built. I attempted a plate-vs-slot ratio myself on `FINAL_16x9_stone_healthy.png`, got
   column runs contaminated by mid-grey stone, and **stopped rather than publish it** — L-Q, I do not
   ship numbers I cannot defend. **The measurement is yours. Matt's ruling is the authority; the
   number is the receipt, not the justification.**
3. **Do not regress the ratified work** (§1.1). If the swap forces a change to any of it, that is a
   **finding** — name it; do not silently absorb it.
4. **Two resolutions minimum**, the same two as every prior arm, so the strip stays comparable.
5. **Forbidden floors:** `~/Games/mcp-lab/project/` (substrate — read-only copies out only; sha
   `d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`, mode 0444, **verify start and
   end**) · `~/Games/mcp-lab/l7vfx/` · `~/Games/mcp-lab/evidence/l5/`. Per-file sha, never a
   directory-listing hash — your own arm-1 finding. **L-J binds: W-PRO stays parked.**
6. **Method is yours.** No wire question is being asked here; arm 2 retired it and arm 3b did not
   revive it.

---

## §4 — What you ship

1. **FIRST_INTENT banked (labelled reconstructed if it is) + the two-segment clock declared.**
2. **The fork resolved** — bat wings or candles — **as a veto-open ruling with reasoning.**
3. ★ **The backing ruling:** what the darker metallic grey element is in your build, where it sits
   relative to the slots, and **your reading of around-vs-behind** (§1) — or the HALT if the pictures
   do not settle it.
4. ★ **The overlap re-solve**, as its own ruling: what now discharges the occlusion job the
   container was doing, and why that is better or worse than a container.
5. **A/B at both resolutions:** arm 3b hotbar vs arm 3c hotbar, identical HUD state, identical
   frames, one instrument.
6. **Before/after backing-extent numbers** per §3.2, with the instrument stated.
7. ★ **The iteration log split three ways: the swap · the overlap re-solve · everything else.**
   That split is the payload and the reason this runs as its own arm.
8. **Rulings veto-open with reasoning. Read-list declared. Clock closed, authoring separate from
   execution.**

---

## §5 — Exit predicate

1. §4.1–§4.8 present. 2. Substrate sha + `-r--r--r--` verified **start AND end**.
3. `mcp-lab/project/`, `l7vfx/`, `evidence/l5/` demonstrably untouched, per-file. 4. `user://` clean.
5. **Arms 1, 2, 3 and 3b artifacts still intact and renderable.**

**Honorable fallback (L-F):** an attributed blocker plus the best partial is a **PASS.**
**Ceiling-finding is a PASS (L-G)** — *"neither treatment can carry 9 slots plus the utility slot at
1080p and here is the sprite that fails"* is a first-class result.

**HALT to Matt:** any game-systems decision not yet made. The standing list is open and **not yours
to resolve from** — arm 1's three (escape clock, critical threshold, `primary_attack` present in only
7 of 10 kits), arm 2's three (the 6 missing glyphs as a purchase fork, `Down_01` serving both `stun`
and `knockback`, Ice-and-no-Water), arm 3's H-7…H-12, arm 3b's H-14 (the R-5 / glass monotonicity
conflict) and H-15/H-16. **H-13 is now discharged by §1.1. Add to the list; do not resolve from it.**

---

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`).

**Name anything in this dispatch that steered you.** The running tally of my defects on this lap, so
you can check whether I have repeated any: arm 1 — named an exemplar and foreclosed a branch. Arm 2 —
enumerated 6 of 14 folders, and enumeration order became attention order. Arm 3 — **ratified a cause
I had not measured** (L-Q), then called a font ceiling a purchase when the fonts were already owned
one pack over. Arm 3b — put a thumb on the scale by naming which verdict was "worth more," and
claimed a "cost" with no unit. Arm 3c v1 — **built a cell that rewarded deletion when the owner
wanted a replacement**, and only the owner's own second ruling caught it. **Tell me what it is this
time.**
