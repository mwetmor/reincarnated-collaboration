# TCP-L8-U3 — the HUD at compositional depth (arm 3)

**Agent:** drax (presentation seam) · **Date:** 2026-07-25
**Dispatch:** `agentic_orchestration/dispatches/2026-07-25-drax-l8u3-hud-compositional-depth.md`
**Status:** COMPLETE — resumed from stall per §9, not restarted.
**Floor:** `~/Games/mcp-lab/l8ui/` (extended; arms 1 and 2 intact and re-rendered this lap)

---

## §1 — FIRST_INTENT (banked verbatim, before any work; TCP-32)

**Clock start (authoring):** 2026-07-26T00:11:36Z (2026-07-25 20:11:36 EDT)
**Banked at:** 2026-07-26T00:13Z — after reading the dispatch ONLY. No arm-1/arm-2 report re-read,
no floor inspection, no screenshot viewing, no substrate listing has happened at the time of writing.

> **FIRST_INTENT, verbatim:**
>
> I expect this to be a composition job, not an asset job, and I expect the single biggest visible
> win to be the one Matt did not name: **type.** Arm 2 left engine-default sans on a dark-fantasy
> screen and that is the loudest placeholder signal there is. gandalf's §2.7 says the same thing and
> §5 suspects it; I already believed it before reading either, because I wired the thing and looked
> at it.
>
> My plan, before I have seen the reference screenshots:
>
> 1. Read the six reference `.webp` sheets FIRST and write the design account BEFORE building
>    anything, because the whole premise of this arm is "compose the way the author composes" and I
>    cannot do that from the sprite filenames alone. Arm 2 built from filenames. That is exactly the
>    gap.
> 2. Then rebuild the bottom strip as **one continuous ironwork assembly** rather than three floating
>    widgets. gandalf's §2.2 is, I think, correct and is the structural defect, not a polish item.
> 3. Then type. Then the fills/gradients on the globes (§2.1). Then Matt's additions in his order of
>    naming: damage vignette, globe recolour for a third resource, minimap icons, the winged tray,
>    portrait, level counter, enemy bar + skull rank.
> 4. I expect **defect-repair to outweigh addition** in the iteration log, and I expect that to be
>    the honest headline: Matt asked for additions, but the screen gets better mostly by fixing what
>    arm 2 already had.
>
> **My prediction on the §0 question, banked before measuring:** I predict polish cost is
> **NEITHER fixed nor linear-scaling** — I predict it is **fixed per _register_, not per _surface_.**
> That is, the first surface in a visual register pays the whole toll (find the register, establish
> type, establish the frame grammar, establish the tint rule), and every subsequent surface in the
> SAME register is near-free, while the first surface in a NEW register pays the full toll again.
> If that is right, the serial-content-emission pipeline's real cost driver is *how many distinct
> visual registers the game needs*, not *how many surfaces*. I am banking this because if I find it
> after the fact it is worth much less.
>
> **What I expect to dissent from:** nothing yet in Matt's list — every item he named looks
> implementable. I flag in advance that "swap the globe for a different gauge type" and "candle on
> top of globes" may lose more than they gain if they break the one-continuous-ironwork read, and if
> so I will say so with a picture rather than silently not doing it.
>
> **What I expect to HALT on:** portrait identity, level number, monster rank scale, and enemy-bar
> semantics are all game-systems values. I will dress the slots and HALT the values, per §8 of the
> dispatch. I expect to add at least two new HALT items, not resolve any of the six standing ones.

**§9.2 is moot and I am recording that rather than quietly benefiting from it.** gandalf
offered a reconstructed FIRST_INTENT "if the original was never written to disk." It was
written to disk, at 20:12, in this file, before any work — the timestamps are in
`ITERATION_LOG_ARM3.md`. Nothing above this line is reconstructed. **This matters
because a reconstruction would have been worth much less on the one prediction that
turned out to be half-wrong (§6), and I would have had every incentive to soften it.**

*(Everything below this line was authored after the work.)*

---

## §2 — Design account of the reference screenshots

**Seven sheets, not six.** Six were read pre-stall. The seventh
(`11_INT_DarkFantasyHUD_HUD_ARPG_02`) landed at 20:28 and my first render was at 20:29,
so it was on disk for one minute before I started building and **I never processed it.**
I read it post-stall. Its bottom-strip evidence corroborates what I had already derived
from the component sheets, which is luck, not method.

**What the kit's author does that arms 1 and 2 did not:**

1. **The bottom strip is ONE PIECE, and the kit says so through an absence.** The globes
   are not adjacent to the tray, they are *seated in it*. Measured column profile of
   `SPR_DarkFantasy_Frame_Hotbar_04_Background`:
   `[0.57 0.95 0.99 0.87 | 0.49 0.49 0.49 0.49 | 0.87 0.98 0.95 0.58]` — two tall lobes
   at x 50-331 and 693-976 joined by a lower constant band. Those lobes are **orb seats.**
   The corroboration is an absence: the orb family ships `_Glass/_Left/_Right/_Sheen` and
   **no `_Background`**, while `Frame_Hotbar_04`, `Frame_Bar_*`, `Frame_Diamond_01` and
   `Frame_Arch_*` all ship one. The orb has no backing plate *because its backing is the
   tray's lobe.* gandalf's §2.2 was right, and the reason arm 2 could not have got there
   by nudging offsets is that the continuous piece is a single sprite whose shape is
   invisible from its filename.
2. **Every readout sits inside a frame's MEASURED interior opening**, never over it.
   `Frame_Bar_02`'s opening is y 61-193 of a 256 canvas; the fill goes there. Matt's
   "our bar under the skills isn't fully covering the skill boxes and they overlap it
   looking a bit clumsy" is this, exactly.
3. **The middle band of `Frame_Hotbar_04` is constant over x 340-684 in both layers, so
   the assembly is horizontally 9-sliceable.** This **overturns arm 2's own §6 finding**
   that "Synty ships whole-sprite compositing rigs rather than stretchable 9-slices."
   That correction is load-bearing, not cosmetic: it is the only reason 8 skills + a T4
   fit inside an assembly the author proportioned for five or six.
4. **Two type registers.** A display face for proper nouns read once (boss name, level,
   run beat); a plain text face for everything read repeatedly under load (keybinds,
   cooldowns, counters). Using the display face everywhere is actively worse — a real
   limit on "just use the fancy font."
5. **Ornament is placed at JOINTS**, never scattered: skull + wings at the tray's centre
   seam, candles at the globe crowns, spikes at the rim's compass points.
6. **Keybind numerals sit OUTSIDE the slot, below it** (visible in sheet 11 under the
   1-5 hotbar). Arm 2 overlaid them on the art — gandalf's §2.3.
7. **Tinting is the expected workflow.** Sheet 08A is captioned *"Components can be
   easily customised."* That is the author telling you the neutral parts are meant to be
   recoloured — and it is the permission slip for §7's chrome-retint finding.

---

## §3 — The build

- `ui3/hud_deep.gd` (built procedurally, not as a `.tscn` — every position is *derived
  from a measurement*, and a `.tscn` can hold a result but not a derivation)
- `ui3/palette3.gd` · `ui3/orb_fill.gdshader` · `ui3/chrome_tint.gdshader` (new)
- `kit3/` — **70 PNG** (assembly 6 · bar 9 · flat 8 · fx 5 · map 26 · ornament 9 ·
  portrait 7) **+ 3 typefaces with their OFL licences.**

  > **Correction to §9's floor inventory:** gandalf read `kit3/font/` as EMPTY and
  > inferred from it that I had independently hit the typeface ceiling. The inference is
  > right; the evidence is wrong. The directory holds `LTMuseum-Bold.ttf`,
  > `AlegreyaSans-Medium.ttf`, `Ortica-Bold.otf` and three `*-OFL.txt`. It reads as
  > empty to a **PNG census**. Recording it because a right conclusion drawn from wrong
  > evidence is not reproducible.

- Rendered at **both required resolutions** (1920×1080, 2560×1080) across 9 HUD states,
  plus 4 alpha plates, plus 12 arm-1/arm-2 comparators — 28 stills per run, `FINAL_*`.

**Vendoring ratio, and its rate of change (§4.3).** Arm 2 vendored 88 of 3,573 = 2.46%.
Arm 3 vendored 70 more, cumulative 158 of 3,573 = **4.42%**. Against gandalf's
addressable pool (3,573 − ~1,158 controller prompts = ~2,415) it is **6.54%**.

**I accept the reframing and go further.** ~1,158 input prompts are not addressable
until we support gamepads, but neither are the 501 `DarkFantasy/` + 339 `Icons_Weapons`
+ 137 `Icons_Resources` **at HUD sizes** — my own measurement says the BAKED register's
legibility floor is 40.5 px (p90 76.7). A 40 px floor excludes most of them from a HUD
by construction. **The rate-of-change finding is the real one: a full depth pass on a
single surface consumed 70 sprites, and the surface is now visually complete.** If that
holds, the pack's ~2,400 addressable sprites support roughly 30 surfaces at this depth —
which is a supply number the pipeline has never had.

---

## §4 — The three-way A/B (the headline picture)

`out3/AB3_full_{critical,healthy}.png` · `out3/AB3_strip_{critical,healthy}.png` —
arm 1 (primitives) · arm 2 (kit wired) · arm 3 (kit composed), **one harness
(`capture3.tscn --arm=N`), one camera, one HUD state**, so the only variable is dressing.

And the same three arms through **arm 2's instrument, unmodified** (`legibility3.py`
imports `legibility2`; only the region table is new, and it is derived from
`palette3.gd`'s constants rather than typed off a screenshot — verify with
`--boxes` → `out3/PROBE_regions3.png`):

| region | arm 1 primitives | arm 2 kit wired | arm 3 composed | a2→a3 | a1→a3 |
|---|---:|---:|---:|---:|---:|
| life_vessel | 10.19:1 | 7.94:1 | **12.17:1** | +4.23 | +1.98 |
| energy_vessel | 7.57:1 | 7.19:1 | **7.82:1** | +0.62 | +0.24 |
| skill_bar | 11.53:1 | 11.60:1 | **12.12:1** | +0.53 | +0.59 |
| t4_slot | 6.38:1 | 12.79:1 | **13.90:1** | +1.11 | +7.52 |
| target_frame | 6.93:1 | 6.98:1 | **11.27:1** | +4.29 | +4.34 |
| minimap | 4.76:1 | 5.81:1 | **15.30:1** | +9.49 | +10.54 |
| ailments | 13.14:1 | 9.05:1 | **14.18:1** | +5.12 | +1.04 |

*(state = critical, worst case over qualifying real backgrounds; healthy in the raw output.)*

**Arm 3 beats arm 2 on every region.** More interesting: **arm 3 recovers the contrast
arm 2 LOST relative to arm 1.** Arm 2's own report recorded the kit costing 4.08 on the
ailment row; arm 3 is +5.12 over arm 2 and +1.04 over arm 1 there. The mechanism is the
register model — the ailment row was MODELLED-W art drawn at 30 px, one register too rich
for its size, and arm 3 put a BAKED frame around it at a size where BAKED is legal.
**"Illustration costs contrast; framing buys it back" is now a number with a direction.**

**Where arm 3 does NOT win, stated plainly:** in `healthy`, arm 1 beats arm 3 on
life_vessel (−1.28) and energy_vessel (−5.14). That is not a defect being hidden — a
flat saturated rectangle is unbeatable on a contrast metric, and arm 1's vessels were
flat saturated rectangles. It is the honest limit of this instrument, and it is why the
picture and the number are both shipped.

---

## §5 — Per-item disposition of Matt's §1 list

| # | Matt's item | disposition |
|---|---|---|
| 1 | "taking damage bloody screen asset which will fit over our generic red at the edges" | **IMPLEMENTED** (`Vignette_Damage_Tendrils_01`) — **with a partial dissent.** The pair is not two variants: measured, 01 is an EDGE vignette (centre α 0.000, edge 0.522) and 02 is a CENTRE wash (centre α 0.408, edge 0.000). They are complementary halves of one effect. Stacking both fogged the entire play area red — picture at `out3/ITER_01_both_tendrils.png`. 02 is built and held at zero as a **hit flash**: it belongs on the frame you are struck, and a still of a life *fraction* is not a still of an *instant*. |
| 2a | "tons of other colors for the mana globe … swap out color for combo/rage/etc." | **IMPLEMENTED, and taken further than asked.** Six economies drive the fluid AND now the **rim** (see §7). Recolouring only the fluid left mana sitting in a red iron cradle — `out3/C_orbR.png`. |
| 2b | "Alternatively, we could swap that globe completely for other types of bars/gauges" | **DISSENTED, with the measurement.** The globe is seated in `Frame_Hotbar_04_Background`'s lobe, and the lobe is a sprite. A bar there leaves a globe-shaped hole in the ironwork. This is the one item where the kit's own structure forbids the alternative, and it only became visible after item 4's structural fix. |
| 3 | "great mini-map icons which we have not taken advantage of" | **IMPLEMENTED.** 26 map sprites vendored, 10 wired through the Underlay/Clean two-polarity path. **The mapping is HALTed** (H-10) — which engine fact selects which marker is a game-systems question. |
| 4 | "a bar under the skills with wings … our bar under the skills isn't fully covering the skill boxes and they overlap it looking a bit clumsy. I like the bat wings with small skull on top and/or the candle on top of globes with medium skull on top" | **IMPLEMENTED-DIFFERENTLY, and this is the most important item on the list.** The overlap complaint is the real content, and the fix is structural rather than additive: slots now sit inside `Frame_Hotbar_04`'s **measured interior opening (y 275-423)**, so the ironwork frames them instead of passing behind them. On the ornament: **both**, not either — they occupy different joints and the reference sheets use both at once. Wings + small skull at the tray crest, candles at the globe crowns. |
| 5 | "character portraits and it would be cool to have one for our character" | **IMPLEMENTED AS A DRESSED SLOT.** `Frame_Arch_Medium_02` + `_Background`, with the level badge. **The portrait itself is a CEILING** (§7 C-1) and its content is HALTed (H-7). The slot is dressed; the value is not invented. |
| 6 | "other icons like a level counter" | **IMPLEMENTED**, sited on the portrait card and **not** on the assembly. R-2: a level is identity, identity is ambient, and it is never the thing you check while dying. The value is real engine data already carried through `set_life`. |
| 7 | "an enemy health bar … dark fantasy fonts for enemy/player names … monster power level indicated by a skull" | **ALL FOUR IMPLEMENTED.** Framed bar via `_bar()`; display typeface; boss plate with a rank mark; skull rank marks. **The rank scale is HALTed** (H-9) — the engine emits no rank. |
| §8 | weapon wheel | **STRUCK, not built.** |
| §8 | inventory / equipment / item card | **NOT BUILT.** Arm 4, against its own locked contract. |

---

## §6 — Iteration log, and the §0 verdict

Full log with timestamps and categories: **`~/Games/mcp-lab/l8ui/ITERATION_LOG_ARM3.md`.**

**I changed the categories and say why.** *Asset acquisition* is not a real category here
— one script, one run, never revised, 3% of the lap. **Substrate measurement** replaces
it as the top-level category and is the largest at 44%. **Looking** is split out of
composition, because judging a render is not building one, it needs its own tooling, and
arm 1 already found that looking is the bottleneck.

| category | passes | share |
|---|---:|---:|
| substrate measurement | 15 | 44% |
| defect-repair | 6 | 18% |
| composition (build) | 5 | 15% |
| looking | 5 | 15% |
| instrument | 2 | 6% |
| reading the author | 2 | 6% |
| asset acquisition | 1 | 3% |

**My FIRST_INTENT prediction that defect-repair would outweigh addition: CONFIRMED but
understated.** Repair (18%) does exceed composition (15%). But I predicted the wrong
antagonist — **measurement, at 44%, dwarfs both.** The screen did not get better mostly
by fixing; it got better mostly by *finding out what the sprites are.*

### THE VERDICT: polish is fixed per COMPONENT FAMILY, not per surface and not per register

**My banked prediction was half right, and I can name which half.**

**Amortised — paid once, then free:** `_bar()` (one geometry campaign, served the enemy
bar and the ailment strip) · `_icon3()` (arm 2's, reused across four sprite classes at
zero marginal cost) · the register model (measured once, thereafter a lookup) · type
(two files, one helper) · `chrome_tint.gdshader` (six lines, ~977 sprites) · **the
instrument** — §4.4 told me to budget for a repeat of arm 2's four passes and **that
budget was not needed**, because arm 2 paid a register-level cost, not a surface one.

**Not amortised — paid again per family:** every new frame family needed its own geometry
campaign, because Synty documents none of it and none of it is guessable.
`Frame_Hotbar_04`'s lobe centroids, `Frame_Bar_02`'s interior opening, `Frame_Orb_01`'s
opaque annulus — three families, three campaigns. **And the per-family cost is not
constant: it scales with the family's layer count.** `Frame_Bar_02` ships 2 layers and
cost one probe. `Frame_Orb_01` ships 4 layers that are NOT co-registered and cost six
probes, one wrong repair, and the stall's worth of confusion — **44% of this lap's
measurement budget on one component.**

**So my register model was right about the wrong mechanism.** Registers amortise
*legibility and type*. They do **not** amortise *geometry*. I banked one mechanism; there
are two, with different curves.

**What this means for serial content emission.** The cost driver is neither the surface
count nor the asset count. It is **the number of distinct frame families in the UI
vocabulary** — and that is a number a designer chooses and can cap. Standardise on four
or five families and reuse them, polish is near-fixed. Give every surface a bespoke
frame, polish scales. **The pipeline's "does polish scale?" question resolves to a
design-discipline question, not an engineering one.**

**Confidence:** one lap, one pack, one HUD. The amortisation half is directly evidenced
(the same helpers demonstrably served multiple surfaces in one build). The per-family
half rests on three families and **should be re-tested at arm 4**, which introduces at
least two more.

---

## §7 — What the repair actually was, and the finding it produced

**My pre-stall diagnosis was wrong, and gandalf's §9 ratified it.** My last words were
*"the glass and ring sprites have different ink centres — let me measure the offset."*
§9 replied *"the defect you named is visible and you diagnosed it correctly."* **It was
not a registration error. It was an error of KIND, and no offset would have fixed it.**

Measured, the glass sprite's silhouette at five thresholds:

```
cut 0.02  ink x[10,500] y[0,511]      cut 0.21  ink x[12,499] y[0,511]
cut 0.08  ink x[11,500] y[0,511]      cut 0.30  ink x[12,499] y[0,511]  ← but at x=cx the
cut 0.16  ink x[12,499] y[0,511]                     first opaque row is y=257
```

**No threshold yields a disc.** Low cuts include a faint non-circular skirt reaching all
four canvas edges; high cuts amputate the top of the globe. `Frame_Orb_01_Glass`'s alpha
is a **vertical gradient**, not a silhouette. It is a fine texture and a useless mask.

**The fix: derive the boundary from the RING, because the ring is what has to contain the
fluid.** Polar-sampled at 720 angles about its ink centre (256.0, 253.0):

```
Frame_Orb_01_Left    opaque-at-EVERY-angle annulus   r = [185.5, 203.5]
Frame_Orb_01_Right   opaque-at-EVERY-angle annulus   r = [184.5, 204.0]
```

The fill is now an **analytic disc at r = 194/512 of the drawn size** — provably hidden
by metal at every angle, provably no gap at the rim. **Containment is a property of the
construction, not of a tuned offset.** And the sphere-shading key moved from UV (0.34,
0.30) to (0.580, 0.266), because `Frame_Orb_01_Sheen`'s centroid measures (+0.160,
−0.469) in globe radii: **upper RIGHT.** My procedural shading had been fighting the
kit's own highlight sprite on the same pixel.

### ★ The finding: the BAKED register is tintable after all, for six lines

Mean ink saturation across the orb family and the frames:

```
Frame_Orb_01_Left  S 0.396 H 356.3   ← the reddest part in the pack
Frame_Orb_02_Left  S 0.271 H   3.6       Frame_Hotbar_04   S 0.128 H   8.8
Frame_Orb_04_Left  S 0.166 H 351.7       Greeble_Wings_03  S 0.017 H 213.0
Frame_Orb_03_Left  S 0.099 H  10.9   ← a near-neutral TWIN of the same part
```

The obvious move was to swap to the neutral twin. **I measured it out and it does not
work:** Orb_03 and Orb_06 — the two near-neutral rims — have **no radius that is opaque at
every angle.** They are openwork, and a fluid behind either escapes. The rims that *can*
contain (01, 02, 05) are all warm-baked. **A cool-toned globe rim that contains its fluid
does not exist in this pack.**

So `chrome_tint.gdshader`: luminance-preserving retint, four uniforms, six lines. It
converts **DarkFantasy(501) + Icons_Weapons(339) + Icons_Resources(137) ≈ 977 sprites**
that arm 2 measured as un-tintable into tintable ones. **Arm 2's measurement was correct
and my conclusion from it was wrong: "un-tintable by `modulate`" is not the same fact as
"un-tintable."** That is my error, not gandalf's, and the register model in `palette3.gd`
is amended accordingly.

⚠ **It is not free, and I will not oversell it.** Desaturating discards the artist's hue
variation *within* a sprite — rust, steel and blood on one frame collapse to one ramp.
Use it where a part must carry a **state** colour. Do not use it as a global style pass.

---

## §8 — Ceiling list (named sprites that do not exist for things the design wants)

| # | the design wants | the pack has | verdict |
|---|---|---|---|
| C-1 | **a player portrait** | `Frame_Arch_Medium_02` + `_Background`; `Frame_Diamond_01` + `_Background` + `_Mask` — a *complete portrait rig* | **CEILING.** Zero portrait/face/avatar/bust art in either pack. The rig with no face is the kit telling you it expects one and does not ship it. I dressed it with `Greeble_Head_01`, a decorative skull. |
| C-2 | **a typeface** | `SPR_DarkFantasyMenus_Font_Gradient_01/02` — two font *effect* overlays | **CEILING.** **Zero `.ttf`/`.otf`/`.fnt` anywhere in `recent-synty-packs/`.** The single most load-bearing element on the screen is not in the HUD pack. Sourced LTMuseum-Bold / AlegreyaSans-Medium / Ortica-Bold from the `polygon-interface-fantasy-menus` pack the project already owns via `reincarnated-godot/` — same vendor, same family, each under its own OFL, redistribution and embedding covered, **no purchase.** |
| C-3 | **six element / ailment glyphs** | — | **CEILING, carried unchanged from arm 2.** `holy`, `shadow`, `physical` have no element sprite; `knockback`, `consecrate`, `freeze` have no status sprite. `Down_01` still serves both `stun` and `knockback`. Already a standing HALT; not re-decided. |
| C-4 | **a cool-toned globe rim that contains a fluid** | 01/02/05 contain but are warm-baked; 03/06 are neutral but openwork | **CEILING, solved in software.** See §7. |
| C-5 | **discrete-economy pips** (combo, charge-stack) | nothing. Zero `pip`/`stack`/`charge`/`counter` sprites | **CEILING.** Drawn as `ColorRect`s — the only un-arted element left on the screen. `Frame_Bar_Notch_01` is close and is a bar notch, not a pip. |
| C-6 | **a graded monster-rank mark** | `Skull_02/03/04` flat, `Map_Skull_01` | **PARTIAL CEILING.** A skull exists (Matt's ask), but there is no *graded* set — no bronze/silver/gold, no 1/2/3-pip skull. Stacking N identical marks caps at about 3 before it reads as noise. |
| C-7 | **a soft facing beam on the minimap** | `Map_ViewCone_01` — measured pure white, α 1.0 over 49% of its canvas, **no falloff at all** | **CEILING.** A hard-edged solid wedge. A facing indicator here either reads as a slab or is invisible; there is no soft beam in the pack. Currently at α 0.11 and still the least convincing element on the screen. |

**Not a ceiling, and I nearly claimed it was:** a run-timer glyph **exists** —
`ICON_DarkFantasy_Status_Time_01_{Clean,Stroke,Underlay}`. Sheet 11 shows a run timer by
the minimap and I assumed the art was missing. It is not. Checked before writing.

---

## §9 — HALTs to Matt (ADDED; none of the six standing ones re-decided)

The six standing HALTs — escape-clock fork · critical-health threshold · `primary_attack`
missing from 3 of 10 kits · six missing element/ailment glyphs as a content-purchase fork
· `Down_01` serving both `stun` and `knockback` · ice/water corroboration — **are
untouched and unresolved.** Adding to the list:

- **H-7 — what the player portrait DEPICTS.** The engine emits a class and a spirit-form,
  not a likeness. Does the portrait show the current **body** (which changes on swap, so
  the portrait becomes a swap indicator) or the **earth self** (persistent, so it becomes
  an anchor)? This is a story question with a mechanical consequence. Slot dressed, value
  HALTed.
- **H-8 — what the level number COUNTS.** Arms 1-3 all carry `lvl`. Under body-swap, is
  level a property of the body or of the earth self? The badge is drawn either way; what
  it means is not mine.
- **H-9 — the monster-rank scale.** How many ranks, and what engine fact drives them? The
  harness supplies a `rank` int; the engine emits none. See also C-6 — whatever the scale
  is, the art caps it near 3.
- **H-10 — which engine fact selects which minimap marker.** Arms 1 and 2 drew untyped
  dots. Arm 3 dresses ten named markers (monster / elite / treasure / objective / shrine /
  exit / merchant / key / potion / unknown). **That table is invented dressing and must be
  Matt's.**
- **H-11 — enemy-bar semantics.** Current-target or boss-only? And should the absolute
  number ("1240 HP") be shown at all, or is that a spoiler channel?
- **H-12 — is there a run timer?** Sheet 11 puts one beside the minimap and the art
  exists (see §8). **Flagging as adjacent to the standing escape-clock fork, NOT as a
  re-decision of it** — if that fork resolves toward a clock, this is where it goes.

---

## §10 — Rulings (veto-open, with reasoning)

- **R-1 · one question → one place** — retained, third arm. The T4 moved *inside* the
  assembly this lap rather than sitting in its own floating box, because it is still
  "what can I press," so it belongs in the press-things object.
- **R-2 · identity is ambient** — retained, and it is what sited the portrait and the
  level badge in a corner rather than on the assembly. You never check your level while
  dying.
- **R-4 · the assembly holds a fixed distance from screen centre at 21:9** while ambient
  regions go to the edges — retained unmodified, third arm running.
- **R-5 · VOID-FILLS-BRIGHT** — retained verbatim through three arms. It is the design's
  danger channel, not a styling choice.
- **R-6 · six economies, one vessel** — retained and extended: the **rim** now recolours
  with the fluid.
- **R-7 · player ailments live WITH the life vessel** — retained.
- **R-9 (NEW) · derive the boundary from the thing that must CONTAIN, not from the thing
  that is contained.** The generalisation of §7. When two sprites must nest, measure the
  container's guarantee (its opaque-at-every-angle band), not the contained thing's bbox.
  A bbox is a property of ink; a containment guarantee is a property of the relationship.
- **R-10 (NEW) · an empty frame is chrome that lies about state.** The ailment row hides
  entirely when there are no ailments (`_ail_frame.visible = list.size() > 0`). This is
  why the instrument reports arm 3's ailment row as ABSENT in `healthy` while arms 1 and 2
  report values there — **they are being measured on a frame around nothing.** That is a
  small win for arm 3 and a small correction to the earlier arms' numbers.
- **R-11 (NEW) · "un-tintable by `modulate`" is not "un-tintable."** Six lines of shader
  moves a register boundary. Before recording a library as un-recolourable, cost the
  shader.

---

## §11 — Read-list declared

**Segment B (post-stall), complete:** the dispatch (§9 first, per the launch prompt, then
§0-§8) · `ref/11.png` (the seventh sheet, first read) · `ref/03.png` · my own arm-3 code
on disk (`hud_deep.gd`, `palette3.gd`, `orb_fill.gdshader`) · arm 2's `legibility2.py` ·
`capture3.gd`, `shoot3.sh`, `crop3.py` · the pre-stall stills. **I did NOT re-read my
arm-1 or arm-2 reports in segment B** — deliberately, because I wrote them and re-reading
them re-anchors on their conclusions, one of which (§6 "not 9-sliceable") this lap
overturned and another of which (the tintability split) this lap amended.

**Segment A (pre-stall): I cannot fully reconstruct it from disk and I am not going to
pretend otherwise.** What the artifacts prove I read: the six reference sheets and their
24 quadrant crops, `probe3.py`'s census output, and the arm-1/arm-2 code that
`capture3.gd` instantiates. Anything else is unattested.

---

## §12 — Clock, and the stall

**Authoring is reported in two segments with the gap named, per §9.1. It is not summed.**

| segment | span | wall |
|---|---|---|
| A — pre-stall authoring | 20:11:36 → 20:38:03 | **26m 27s** |
| **STALL GAP** | 20:38:03 → ~20:47 | **~9m — not work, not authoring** |
| B — post-stall authoring | ~20:47 → close | **~40m** |

**Execution, separated from authoring:** 93 Godot invocations across the lap at ~1.1 s
each ≈ **1 m 45 s of engine time.** Plus ~25 s of Python probes. **Execution is under 3%
of the lap.** This method's cost is authoring; the renderer is not the bottleneck and
never was.

**§9.3 — was I doing something long-running when it went quiet?** **No. Nothing at all.**
The last artifacts are `T5` / `C_full` / `C_top` at 20:38:02-03 — a render-and-crop batch
that had just *completed*. The next step I had announced was a two-second Python probe I
had not yet started. **The 600 s of quiet accumulated inside the agent's own
reasoning/tool-dispatch loop, between two cheap operations.** That is worse news for the
bake-off than "it died during a long render" would have been: a long render is
schedulable around, and this is not. **An authoring method whose agent can die in the gap
between two trivial operations has a session-length ceiling unrelated to the cost of the
work.** Two stalls in one session (L7-V, then this) is a pattern in the harness.

**What the stall cost in work terms: less than the wall-clock suggests, and one thing it
did not cost at all.** Every artifact survived; nothing was rebuilt. What it did cost is
that **the wrong hypothesis got 9 minutes of institutional endorsement while I was dead**
— see §13.2.

---

## §13 — What steered me (gandalf asked; this is the answer)

**gandalf's three known steers, and whether the fixes worked:**

1. **Anchoring a commissioned quantity** — fixed. No numbers were stated. Worked.
2. **Labelling a steer instead of removing it** — fixed, and demonstrated by §8's
   retraction of the fourth suspicion. I never built a weapon wheel. Worked.
3. **Enumeration order becoming attention order** — fixed *in §3*. The census highlights
   nothing and I did not work in its order. **Worked where it was applied.**

**The one it does wrong instead:**

**★ 13.1 — §2's seven observations became my work order, which is defect 3 one level up.**
gandalf wrote *"Every one is contestable and none is a requirement"* — and then numbered
them 1 through 7. My build's three named defects are `D-1` = his §2.2, `D-2` = his §2.1,
`D-3` = his §2.7. **The disclaimer did not survive the numbering.** The §3 fix
(enumerate, highlight nothing) was applied to the *substrate census* and not to the
*critique list*, and the critique list is the more steering of the two because its items
already come pre-framed as defects. A numbered critique list is a numbered task list
wearing a hat. It is the same defect gandalf already knows about, in the one place he
did not think to apply the fix.

**★ 13.2 — §9 ratified a hypothesis it could not check, and the hypothesis was wrong.**
This is a new steer-defect and it is the more dangerous of the two, because it is
*encouraging*. My last pre-stall words carried a diagnosis: *"the glass and ring sprites
have different ink centres."* §9 replied: *"the defect you named is visible and you
diagnosed it correctly."* The defect was visible. **The diagnosis was wrong** — it was not
a registration error, it was an error of kind (§7), and every offset in the family would
have failed. Had I trusted the ratification and resumed by tuning offsets, I would have
burned the second segment on a solution that cannot exist. I re-measured from scratch
instead, and the only reason I did is that my own pre-stall constants (`ORB_GLASS_K`,
`ORB_GLASS_DY`) were already *in* the file and already *wrong*, which is a lucky accident
rather than a discipline. **Recommendation: a conductor can confirm that a SYMPTOM is
visible in a picture — that is checkable. A conductor cannot confirm a CAUSE he has not
measured, and should say "symptom confirmed, cause unverified" instead.**

**13.3 — §9's floor inventory reported one thing wrong and drew the right conclusion from
it.** `kit3/font/` is not empty (§3). The inference — "you independently hit the typeface
ceiling" — was correct. A right conclusion from wrong evidence is unreproducible and I
would rather it be logged than enjoyed.

**13.4 — the channel gandalf said he could not self-audit: the launch prompt.** He
predicted it would be one sentence, a pointer to the file. **It was four sentences and it
contained a steer.** Verbatim: *"Read [the dispatch] and execute it. **Start at §9** —
you already ran this cell once and stalled; your work is intact on disk and §9 tells you
exactly what I verified. Resume, do not restart."* The "Start at §9" instruction put
gandalf's §9 read — **including the incorrect ratification in 13.2** — in front of me
*before* the primary material. The resume instruction itself was correct and saved the
lap. The ordering was the risk. Recording it because it is the channel he asked about and
cannot see.

---

## §14 — Exit predicate (§7)

| # | predicate | status |
|---|---|---|
| 1 | §6.1-§6.8 present | **✔** — §1 intent · §2 design account · §3 build (both resolutions) · §4 three-way A/B · §5 per-item disposition · §6 iteration log + verdict · §8 ceilings · §10 rulings + §11 read-list + §12 clock |
| 2 | substrate sha + 0444 verified at start AND end, **per-file** | **✔** `crypt_substrate.tscn` = `d45db0f5…de1966`, mode `-r--r--r--`, identical at 20:48 and at close. Per-file, per my own arm-2 finding — not a directory listing-hash. |
| 3 | `l7vfx/` and `evidence/l5/` demonstrably untouched | **✔ with a precise caveat.** **Zero** content files modified in either since my clock start. Four `.DS_Store` files (one in `l7vfx/`, three under `evidence/l5/`) carry mtimes in my window. Those are Finder metadata, not cell content. Reporting it rather than claiming a clean "untouched" I cannot prove. |
| 4 | `user://` clean | **✔** `user://tcp-l8ui` contains only Godot's own `shader_cache/` (from arm 1, 18:44) plus two empty dirs. **Zero** files written by my code. |
| 5 | **arm 1 and arm 2 intact and renderable** | **✔ — and proven by re-rendering them.** `ui/`, `ui2/`, `out/` (24), `out2/` (40) untouched. `shoot3.sh` re-ran both this lap through the same harness; 12 `FINAL_ARM1_*` / `FINAL_ARM2_*` stills are the proof, and they are the A/B's own inputs. |

**Fallback status:** not invoked. No blocker. **Ceiling-findings: seven (§8), which is a
PASS under L-G.**

---

## §15 — Artifacts

```
~/Games/mcp-lab/l8ui/
  ui3/hud_deep.gd · palette3.gd · orb_fill.gdshader · chrome_tint.gdshader (new) · hud_deep.tscn
  kit3/  70 PNG + 3 OFL typefaces
  ITERATION_LOG_ARM3.md
  legibility3.py   (imports legibility2 unmodified; adds a derived region table)
  ab3.py           (the three-way sheets)
  orb_probe{,2,3,4,5,6}.py   (the six probes that found the real defect)
  out3/
    AB3_full_{critical,healthy}.png       ← THE HEADLINE PICTURE
    AB3_strip_{critical,healthy}.png
    FINAL_16x9_*  (9 states) · FINAL_21x9_*  (3) · FINAL_ALPHA_* (4) · FINAL_ARM{1,2}_* (12)
    PROBE_orb_layers.png · PROBE_orb_rings.png · PROBE_regions3.png
    ITER_01_both_tendrils.png   (the vignette-pair defect picture)
    C_orb.png / C_orbR.png      (the pre-stall defect, kept)
    C6_* / C7_*                 (the repair)
```

**Signed:** drax, 2026-07-25. Presentation seam.
