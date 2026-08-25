# galadriel's R-8 return — **P-2 is dead, and it was killed by a clip we shot nine days ago**

**Filed:** 2026-08-25 (knight-rider). **Class:** return record + routing. **Source:** `galadriel/notes/2026-08-25-p2-scale-composition-instrument-ruling.md` (`03213dd5`, pushed).
**Commissioned by:** gandalf's R-8 — *"P-2 should not be minted until she rules."* He deferred the fitness call on his own proposed property to the person who built the instrument. **She ruled against it.**

---

## The verdict in one row

> ### **NOT-FIT. Do not mint P-2. No bounded version offered — she looked for bounds and there are none.**

**gandalf's argument was good**, and she says so: scale composition is *literally what the band operator measures*. **That is an argument from the operator's NAME**, and it is `#64` at the level of an instrument rather than an artifact — the same shape that has now fired eight times against me this session. She did not answer it from the armchair; she ran six analysis-only experiments against a question the operator had never been pointed at.

---

## 1. ⚑ The falsifier was already in our corpus, and nobody had looked

One table, identical mask operator, identical raster, identical code path:

| leg | what is in the frame | **fine b0+b1** |
|---|---|--:|
| **D3 Whirlwind, Blizzard 2012** | the thing we are trying to be more like | **0.9099** |
| **ours, ww7 arena** | ⚑ **a large grey smoke volume** + thin orange arc | **0.9137** |
| **ours, `melee_combo`** | one thin arc | **0.9054** |
| **ours, `dash_attack`** | one thin arc | **0.9651** |

> **The reference is at 91 % fine-band too.** The spread *within our own build* (0.060) is **five times** the gap to the reference (0.0045). **And the one clip that actually contains the volumetric phenomenon reads FINER than the reference and finer than the bare arc.**

**gandalf's L4 — "86–96 % of every authored pixel sits in the two finest bands" — is arithmetically exact** (she re-derived it independently: 0.0261 against his 0.026). **It read as damning because it had no anchor beside it. The anchor is 91 %.**

⚑ **She looked at the frame.** `zoom_ww7_full.png`, 1920×1080, native, no downscale — *"a grey volumetric cloud occupies roughly a quarter of the frame's central area — soft-edged, internally varying, unmistakably a volume and not a card."* **One image block consumed, and it is the one the ruling stands on.** *(Contrast gandalf's own first-listed blind spot: "I viewed ZERO frames.")*

## 2. ⚑ The gameability hole — and it is not where I said it would be

I asked whether P-2 has CV's defect: *hand a builder a number and they hit it without producing the thing.* **It has a worse one, and my guess about its shape was measured and refuted.**

| what the builder does | authoring cost | **coarse b3+** | × baseline |
|---|---|--:|--:|
| nothing | — | 0.0261 | 1.0 |
| one large dull fog quad | one card | 0.0474 | 1.8 |
| render at 50 % scale | **one project setting** | 0.0962 | **3.7** |
| **author genuine volumetric dust** | **the expensive correct thing** | **0.1343** | **5.1** |
| strip fine detail | one shader line | 0.1684 | 6.5 |
| ⚑ **Gaussian-blur the existing crescent** | ⚑ **NOTHING** | ⚑ **0.2027** | ⚑ **7.8** |

**My framing said a dull quad would fake it as easily as dust. Measured: no — dust beats the fog card 2.8×, and the operator is honestly not fooled by a plain quad.** That is a point in its favour and it belongs on the record.

> ⚑ **The hole is upstream of authoring entirely. Every cheap exploit is a SUBTRACTION.** Blur, detail-removal, render-scale — **none of them author anything, all of them make the row uglier, and the best of them beats real dust by 1.5×.**
>
> **A property whose top-scoring strategy is "defocus the render" is not a specification. It is an instruction to degrade the game.**

**The mechanism, so this is not a table of coincidences:** band energy is variance, variance is amplitude **squared**, so a smoke pixel at Δ8 and a weapon core at Δ200 enter at **1 : 625**. Measured consequence — a volume that is **99.12 % of the authored pixels** moves coarse share by **0.0004**. ⚑ **P-2's own definition names "band-share distribution of authored MASS." The operator does not compute mass.** And its sensitivity is governed by an **amplitude ratio** (blind beyond ~6× core-to-volume), which makes it a contrast measure wearing a scale measure's name.

## 3. ⚑ Routed to me — the control does not subtract the CAMERA

She built the fx-off control and she ruled on what it does. gandalf claimed it immunises camera, actor count, locomotion and raster. **Three of four correct; raster is wrong; and the fifth is unnamed by anyone:**

> **The pyramid indexes bands in PIXELS, not in WORLD UNITS. Double the camera stand-off and the identical authored effect halves in apparent size and slides one full octave finer.** The control is matched, so it subtracts the *scene* — **it does not subtract the PROJECTION.**

**And there is a camera-framing dispatch in flight right now** (`2026-08-25-drax-camera-framing-and-wwab-render.md`, still PENDING). **P-2 is dead, so the hazard has lost its target** — but the rule generalises past it, and I am recording the general form because the *next* ruler will be built in the same units:

> ⚑ **A pixel-indexed statistic is a function of the camera that produced the pixels. Clips rendered on either side of a framing change are not band-comparable, and nothing in the file names will say so.** Every figure in § 1 above was computed on **pre-framing-change** captures.

## 4. What she killed, what she ratified, and what she did to her own replacement

| | after this ruling |
|---|---|
| **L4 as a design LAYER** | ✅ **untouched — she agrees with it.** *"I am killing the RULER, not the LAYER."* Line-vs-volume is real; Matt's smoke and wind items really do live there |
| **P-1 lifecycle coverage** | ✅ ⚑ **STRENGTHENED — she tried to break it and failed.** See below |
| **P-3 emitter independence** | ✅ untouched — build inspection, no operator, none of these failure modes reach it |
| **P-4 variant differentiation** | ⚠️ **stands, on cleaner ground.** Its `band_frac`-identical clause is weak evidence (the operator is near-blind to all but the core). **Drop the clause; `authored_px` and `N_eff` carry it** |
| **R-4 CV not mintable** | ✅ **ratified doubly — the suite gandalf asked for killed his own property harder than it killed CV** |
| **§ 5.3 band-profile-per-element** | ❌ **falls with the ruler.** Cheapest route to four band profiles is **four blur radii** |
| **R-6 ordering** | ⚠️ item 3 loses its **gate**, keeps its **place** — and it was behind items 1–2 anyway |

⚑ **The ratification is the part I would not have predicted.** gandalf's L5-is-zero claim rested on a *floored* mask, and light spill is the textbook low-amplitude/high-area phenomenon a floor discards. **She went below the floor deliberately to break it** — every pixel differing by even one code value:

> **Windup marks `01` and `02`: BYTE-IDENTICAL to the control. Max Δ exactly 0.** Peak mark authors **2,814 px**, not the 200,000 a hidden spill would need. **There is no faint spill under the threshold. She built the test that would have overturned him and it did not overturn.**

**And she ran her own candidate replacement (P-2′, a mass-not-energy statistic) against the same suite. It failed too** — blur still moves it 8×; `N_eff` reads 1.00 for a fog card *and* for real dust. ⚑ **She reported it instead of proposing it.** *"The suite is not rigged — it killed my proposal as readily as gandalf's."*

## 5. Her self-correction, which lands in a Matt-facing doc

⚑ **The "~344 actors" figure in gandalf's § 6.1 is hers and it is wrong** — the arena's total bodies built across 20 waves, read off a receipt line, not the on-screen count. **She opened the frame and counted six or seven.** Her own note contained both figures and gave him no way to choose.

**Monotonicity survives (0.177 · 0.452 · 0.514 still climbs); magnitude does not.** And she found a **second unexcluded confound** in our code: `hue_circvar` weights by novelty magnitude, **not saturation** — and a near-grey pixel's hue is ill-conditioned, so ww7's large desaturated smoke volume enters at full weight as hue noise. **Two suspects is not a conviction; "demonstrated" becomes "still suspected."**

> ✅ **The conclusion is untouched and she ratifies it twice over: a second unexcluded confound makes the colour comparison LESS closable by measurement, not more.** D2-REF stays dispositioned. **M-3 is still Matt's to answer and now by two routes instead of one.**

**Both corrections are already applied at source** to `canonical/matt_decision_needed/2026-08-25-vfx-depth-four-questions-….md` (M-3 and M-4), because that document is the one Matt reads and it was carrying a retracted number.

---

## Routing

| # | Item | To | Status |
|---|---|---|---|
| 1 | **P-2 NOT-FIT ruling** — kills a property gandalf proposed | **gandalf** | ⏸ queued behind his in-flight Grok return; **not injected mid-run** |
| 2 | Drop the `band_frac` clause from P-4's evidence | gandalf | queued with (1) |
| 3 | Replace L4's *"everything we author is a thin bright line"* with his own F-2(i) phrasing (*capability exists, authoring does not in these rows*) — n=1 ability, the F-1 shape recurring one section later | gandalf | queued with (1) |
| 4 | ⚑ **Blur outscores dust — never bar a builder on a defocus-rewarding number** | drax / jack-ryan | recorded here; no dispatch carries such a bar |
| 5 | **Pixel-indexed statistics are camera-dependent; the framing change creates a comparability boundary** | knight-rider / drax | ⚑ **annotating the PENDING framing dispatch** |
| 6 | Mass-and-extent ruler in world units via the known projection | galadriel | **OWED — not started, not blocking** |

**One property killed. One ratified against a deliberate attempt to break it. Two agents corrected, one of them herself. Nothing escalated to Matt.**

---

## What I am NOT doing, and why

**I am not injecting this into gandalf's live sub-agent run.** He is mid-task on Grok's four hits against the same document. Adding a second adversarial return mid-flight mutates the scope of the higher-stakes item (Matt's five questions) to save one invocation. **The cost of waiting is one extra call; the cost of injecting is a muddled return on the thing Matt actually reads.** It queues.
