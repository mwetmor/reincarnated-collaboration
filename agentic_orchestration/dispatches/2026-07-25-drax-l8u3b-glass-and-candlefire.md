# DISPATCH — TCP-L8-U3b: the globe becomes glass as it empties, and the candles are lit

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Authorization:** Matt, 2026-07-25, at the owner's eye, on arm 3's frames.
**Lap:** L8 UI (T4-UI), **arm 3b — a continuation of arm 3, not a new arm.** Same floor, same two
components. Arm 4 (inventory) is unaffected and still queued behind its own rulings.

## §0 — The brief, in Matt's words, and it is the whole brief

> *"Yes, I like the opacity of the third version but as the health level lowers, the globe should
> become translucent like glass. Also, can we please either add VFX to each of the 6 candles on the
> globes?"*

Two owner rulings. **Neither is mine and neither is open to redesign.**

**On the first:** this settles the arm-1 inversion at the owner's eye. Your empty-space-grows-and-glows
move is kept — Matt names the opacity as the thing he likes — and the *empty* region's material is
ruled: **not an opaque amber disc, but glass.** I had drafted a different fix (hold a red liquid line
so fill-height survives as a channel). **Matt's is better and mine is withdrawn**, because glass
carries the vessel reading *and* keeps your growing-void signal, where mine would have re-imposed the
genre default on top of your invention.

**On the second, an honest gap: the sentence says "either" and never says "or."** I do not know the
alternative he had in mind and **I am not going to invent it.** I have asked him. Build the stated
branch — the candles are lit — because that branch is unambiguous and because the picture is what he
needs in order to rule the fork. **If a second branch lands mid-cell it comes to you as an amendment
to this file, not as a redesign.**

**Count verified before writing:** `SPR_DarkFantasy_Greeble_Candles_01` is a **three-candle cluster**
(tall centre, two shorter flanking), placed once per globe. **2 × 3 = 6. Matt's count is exact.** All
three wicks read as **unlit stubs** in the source art. Wick positions are **yours to measure** — I am
not handing you coordinates I got by looking.

## §1 — The measurement, and it is a pre-registered test of a law we wrote one cell ago

TCP-52 ① — authored from *your* arm-3 log — states: **polish is fixed per COMPONENT FAMILY. Registers
amortise legibility and type; they do NOT amortise geometry. Each new frame family pays its own full
integration, scaling with layer count.**

**This cell adds no new component family.** It deepens one existing family (the orb) and lights an
ornament already placed. **The law therefore predicts this cell is cheap. That prediction is
registered here, before you start, and it is falsifiable.**

**If it comes back expensive, the law is wrong or incomplete, and that is worth more than the HUD.**
Report the category split as arm 3 did, so the two are comparable, and **say plainly whether the law
predicted your lap or not.** A refutation is a PASS.

**Sealed: no numbers, no counts, no forecasts of magnitude.** One qualitative suspicion, stated
because arm 2 proved a directional hypothesis aims the search without fixing its answer: **I suspect
the flames are too cheap to measure and that the translucency is the whole cost.** I may be wrong in
either direction.

**A second question, live and secondary:** L7-V ④ found that **particle COUNT is nearly free and
particle AREA is the entire cost** — measured in a 3D scene, at 4K, with SDFGI. This is **2D, on a
CanvasLayer, at UI scale.** Does the area-not-count law survive the change of medium? If the honest
answer is *"the whole thing sits below my measurement floor,"* **say exactly that** — establishing
that UI VFX budgets at zero is a real result for the serial-content pipeline.

## §2 — One measured fact from your own arm 3, offered as a question with both branches live

Your §7 measured `Frame_Orb_01_Glass` as a **vertical gradient reaching all four canvas edges** and
discarded it: *"a fine texture and a useless mask."* That verdict was about its use **as a mask**, and
it stands.

**Matt has now asked for glass.** Whether a sprite you correctly rejected as a mask is or is not the
right thing to reach for as a **material** is **an open question and it is yours.** I am not answering
it, and I am not implying an answer by raising it — I am raising it because withholding a measurement
your own cell produced would be worse than either branch. **`Frame_Orb_02_Glass` also exists.**

**This is the only observation of mine in this dispatch, and it is deliberately not a list.** Arm 3
proved that seven observations captioned *"none is a requirement"* are consumed in order as a work
order — your D-1/D-2/D-3 were my §2.2/§2.1/§2.7. **The defect is ordered lists from an authority, not
inventories**, so this dispatch contains one paragraph and no enumeration of my opinions.

## §3 — The complete FX inventory of both owned packs, counted, alphabetical, uncommented

Given in full because I have now twice failed by omitting content Matt supplied (TCP-41 ④ animation
packs, TCP-49 the whole HUD kit), and because your own standing form is *state the complete list with
counts and no commentary.* **Nothing below is highlighted, recommended, or ranked. Arm 3 vendored 5 of
the 23 in the first folder and 0 of the 10 in the second; that ratio is a fact, not a criticism.**

`matt_notes_handoff_docs/recent-synty-packs/Source_Sprites/Sprites/FX` — **23 PNG**

```
Beams_01 · BloodSplats_01 · Bubble_01 · Damage_Directional_02 · Damage_Directional_02_Bottom
Damage_Directional_02_Middle · Damage_Directional_02_Top · Damage_Hit_01 · Damage_Sparks_01
FireSheet_01 · Glow_01 · Glow_02 · Glow_03 · Glow_04 · Glow_05 · Glow_06 · Glow_07
GlowDot_01 · GlowPatches_01 · HalfCircle_01 · Vignette_Damage_Tendrils_01
Vignette_Damage_Tendrils_02 · Vignette_Heal_Glow_01
```

`INTERFACE_Dark_Fantasy_Menus_SourceFiles_v1/Sprites/FX` — **10 PNG**

```
FireSheet_01 · Gem_Sheen_01 · Glow_01 · Glow_02 · Glow_03 · Glow_04 · Glow_05 · Glow_06
Glow_Dot_01 · Glow_Small_01
```

Adjacent families, complete and uncommented: **Greeble** carries `Candles_01/02`, `Lantern_01_Glass`,
`Banner_04`, `Horns_01`, `Skull_03/05`, `Skull_Cluster_01`, `Wings_01/03`. **Glass** carries
`Frame_Orb_01_Glass`, `Frame_Orb_02_Glass`, `Flask_01_Left_Glass`, `Flask_01_Right_Glass`,
`Flask_02…07_Glass`, `Greeble_Lantern_01_Glass`. The Menus pack ships its own
`SPR_DarkFantasyMenus_Greeble_Candles_01/02`.

## §4 — Constraints (five)

1. **Floor: `~/Games/mcp-lab/l8ui/`, extending `ui3/`.** This is a continuation — **arm 3's `ui3/`
   scenes must remain intact and addressable** so arm 3 and arm 3b can be composited side by side,
   exactly as `ui/` and `ui2/` were. Method is yours.
2. **Vendor what you need and census it**, as arm 3 did; the vendored-to-available ratio is a serial-
   pipeline number.
3. **The legibility instrument carries forward unmodified.** Arm 2 built it, arm 3 used it unchanged;
   changing it now would make three arms incomparable. **If translucency breaks the instrument, say
   so and repair it explicitly as its own logged pass** — do not repair it silently.
4. **Two resolutions minimum, the same two**, so the whole L8 series stays comparable.
5. ★ **A MOVING artifact is required, and this is L-A generalised.** A flame is motion and a drain is
   motion; **stills cannot judge either, and a still of a glass transition is a still of one frame of
   it.** Ship at minimum a short capture of (a) the flames idling and (b) a continuous health sweep
   from full to critical. Format and length are yours. Stills still ship — they do not substitute.

**Forbidden floors:** `~/Games/mcp-lab/project/` (substrate — read-only; sha
`d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`, mode 0444, verify at start and
end) · `~/Games/mcp-lab/evidence/l5/` (live comparison). **L-J binds: W-PRO stays parked.**

## §5 — What you ship

1. **FIRST_INTENT banked verbatim + clock started before any work** (TCP-32).
2. **The two rulings realised**, at the states arm 3 already renders, so the A/B is exact.
3. **An A/B against arm 3** — same states, arm 3 vs arm 3b, side by side.
4. **The moving artifact** per §4.5.
5. **The iteration log with arm 3's categories**, and **the verdict on §1's registered prediction —
   did the component-family law predict this lap?** A refutation is a PASS.
6. **Whatever the flames cost, or an explicit statement that they sit below your measurement floor.**
7. **Rulings, veto-open, with reasoning. Read-list declared. Clock closed, authoring separate from
   execution.**

## §6 — Exit predicate

1. §5.1–§5.7 present. 2. Substrate sha + 0444 verified at start AND end. 3. `mcp-lab/project/` and
`evidence/l5/` demonstrably untouched, by per-file sha — **not by a directory listing-hash**, which
your own arm-2 finding established is the wrong instrument. 4. `user://` clean. 5. **Arm 3's `ui3/`
artifacts still intact and renderable** — proven by re-rendering them as the A/B's inputs, as arm 3
proved arms 1 and 2.

**Honorable fallback (L-F):** an attributed blocker plus the best partial is a **PASS.**
**Ceiling-finding is a PASS (L-G).** *"The pack cannot express a lit candle and here is the sprite
that fails"* is a first-class result, and so is *"translucency cannot be done on this rim and here is
the polar measurement that proves it."*

**Report to:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l8u3b-glass-and-candlefire-report.md`

**HALT to Matt:** the six standing HALTs and arm 3's H-7…H-12 are **open and NOT yours to re-decide**
— including H-7 (what the portrait depicts) and H-8 (what the level counts), which are story questions
I have taken back. Add to the list; do not resolve from it.

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`).

**Name anything in this dispatch that steered you.** Arm 3 convicted me of two things and this file
answers both: the ordered-critique-as-work-order (§2 is one paragraph, unenumerated) and **ratifying a
cause I had not measured — now standing law L-Q, and I committed the same defect a second time twenty
minutes later by reading an empty `kit3/font/` and declaring your fonts item a purchase when you had
already solved it at zero cost from a pack we own.** Both are struck in place in the record rather
than edited away. **Tell me what this one does wrong instead.** My Agent launch prompt will be one
sentence pointing here, so that everything that can steer you is greppable in the committed record.

---

## §7 — AMENDMENT, landed AFTER launch (2026-07-25, mid-flight, owner's eye on the live frames)

**I have no channel to a running agent. This is in the committed record at the moment it was ruled,
which is the only thing available to me. It is yours at close-out or it becomes arm 3c.**

### §7.1 — The §0 fork is CLOSED, and the candles win on their own merits

Matt, verbatim: *"the or is: we can just use the bat wings … Regardless … now that I've seen the
candle VFX, I really like it!!"*

**The alternative was to drop the candles and use bat wings instead. He has withdrawn it after seeing
your flames.** The candles and their VFX are **kept and ratified.** Nothing in §0–§6 changes.

### §7.2 — A NEW ruling, and it REVERSES arm 3's item-4 structural fix

Matt, verbatim: *"the bar surrounding the skills in our HUD is now way too big … remove that box
around the skills and instead either use exactly what's around the skill boxes in the bat wings
version or what's around the skill boxes in the candles version."*

**Reference:** `matt_notes_handoff_docs/recent-synty-packs/synty-dark-fantasy-hud-recommended-uses/`
→ `01_INT_DarkFantasyHUD_Components_ActionBars_*.webp`, the vendor's own composition of their own
parts. **Two rows are named, and either is acceptable — Matt's word is "either." The choice is yours.**
Identifying them unambiguously by content, since row indices are ambiguous on a two-column sheet:

- **the BAT WINGS row** — LEFT column, third from the top. Globes with large bat wings spreading
  outward and chain greebles beneath; **six** slots; `H`-shaped dividers between slots; small skull at
  the crest, small demon greeble at bottom centre; the rail tapers to points where it meets the globes.
- **the CANDLES row** — RIGHT column, third from the top. Globes topped with **lit candles**, dark
  spiked collars; **five** slots with chevron dividers; a **spiked top edge** of small triangular
  teeth; a skull at the crest; the bracket flares to points at both ends.

**What I see in both, stated as observation and not as a specification — the measurement is yours:**
the bar's vertical extent is close to the slot height plus a thin margin. **The slots dominate and the
ironwork is an edge, not a panel.** In both rows the number pips hang **below and outside** the bar.

★ **THE PART THAT MUST NOT BE LOST, and it is the reason this is an amendment rather than a tweak:
this reverses your arm-3 item-4 fix.** That fix answered Matt's overlap complaint by seating the slots
*inside* `Frame_Hotbar_04`'s measured interior opening (y 275–423) so the ironwork framed them. **It
worked, and it is the cause of the new complaint** — the container that stopped the overlap is the box
that is now too big. **So the overlap problem returns the moment the box goes, and it must be solved a
second time by different means.** Both reference rows have already solved it: their slots sit in a
slim rail without overlapping anything. **The answer exists in the art, and the parts are the vendor's
own — they are findable by name rather than by reconstruction.** Do not re-derive what the pack ships.

**Owner-ruled, not yours to re-open:** the box goes. **Yours entirely:** which of the two rows, which
sprites realise it, and how the overlap is solved without a panel. **If neither row's construction can
be assembled from named sprites in the packs we own, that is a CEILING and a PASS (L-G)** — say which
sprite fails and show the frame.

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`), amending in place rather than deleting, as with
arm 3's struck weapon-wheel steer. **This amendment names two reference rows and nothing else about
them; I have deliberately not ranked them, not counted their slots as a target, and not named a
sprite.** Arm 3 proved that what I enumerate becomes what gets built.
