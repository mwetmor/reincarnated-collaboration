# VFX depth — **four questions for Matt, each answerable in one line. None of them blocks any build work.**

**Filed:** 2026-08-25 (knight-rider, routing gandalf's § 8). **Source ruling:** `agentic_orchestration/gandalf/findings/2026-08-25-vfx-depth-design-ruling.md` (`b8d8cae9`).
**Occasioned by:** Matt's VFX-depth critique, 2026-08-25.

⚑ **Read this line first: gandalf's explicit finding is that items 1–4 of the Step-2 reorder proceed with all four of these UNANSWERED.** They are parked because they are Matt's to answer, **not** because anything is waiting on them. Nothing here is a blocker.

---

## M-1 ⚑ — **Where is the HITL Whirlwind run?** *(the one with real consequences)*

**Status: verified absent, twice, independently.** galadriel by pixels (WW-7 turns out to be an **SB-1 cell id, not a whirlwind** — `#64`, the name is not the referent). knight-rider by predicate (**278 MP4s in `reincarnated-godot`, zero matching `whirl|ww`; nothing under `~/Games` named `*whirl*`**).

**Why it is worth more than a comparison arm.** Under gandalf's parse of your critique, your sentence *"in my HITL Whirlwind run, **we added** TONs of internal VFX…"* is a **proof-of-achievability claim about our own stack** — and it is the only one in existence. It answers a question `dash_attack` cannot:

> ⚑ **What does a HUMAN authoring pass add over a CLEAN-ROOM pass on the same row?**
>
> **Step-2 IS a clean-room minting process. If that delta is large, the minting process is the defect** — and no other artifact we hold can show it.

**One-line answer form:** a path · a platform (YouTube/Drive/local) · or **"it was a live session, never captured."**

*(A WW-AB render dispatch was authored against this arm and **BLOCKED at head** when the arm turned out not to exist. Had drax's lane freed twenty minutes earlier he would have rendered a comparison against a substitute clip and produced a confident answer to a question nobody asked.)*

---

## M-2 — **Which tier earns screen-space distortion?**

You proposed cavitation / gravity-distortion with the verb *"add"* — **the only item in your entire critique carrying that verb.** galadriel then measured the reference and found it does not do it: radial coherence **−0.023** over 265 gated frames, against a positive control validated to detect synthetic lensing at |0.51–0.99|, **22–43× below the weakest distortion the operator was demonstrated to see.** ⚑ **You and she were never in conflict** — you flagged it as an invention before she measured it, and she confirmed it would be one.

**gandalf's ruling: the LAYER is adopted, the MECHANISM is reserved.** Environmental response is **exactly zero** in our build and that is a genuine depth failure — but distortion is a **power-tier signifier whose entire value is scarcity.** Put it on a T1 melee combo and the player learns in the tutorial that world-bending is ambient. His Reincarnated-specific argument: *the ascension arc needs a register that escalates; an engine that bends space at T1 has no gesture left for what the journey is climbing toward.*

The four cheap L5 members (light spill · impact decal with decay · contact camera-shake · debris/dust) are routed **now** and buy most of what you saw missing.

**One-line answer form:** a tier name, or **"agreed, park it."**

---

## M-3 — **"alternating through a specific color range" — WHICH range, over WHAT duration?**

⚑ **This one converts an unclosable measurement into a one-line authoring spec from the person who wrote it.**

The reference-vs-ours colour comparison is **not closable by any frame statistic.** `hue_circvar_mean` reads **0.514** for the D3 reference, **0.452** for our own ww7 arena clip, **0.177** for our `melee_combo`. **The reference's value sits INSIDE the range our own build spans**, so the statistic cannot separate "their colour work is richer" from "their scene has more in it."

> ⚑ **CORRECTED AT SOURCE, same session, by galadriel (`03213dd5`) — and the correction makes the refusal STRONGER, not weaker.**
>
> **(a) The actor counts I gave you were wrong, and the error was hers, self-caught.** ww7 was cited at **~344 actors**; that figure is the arena's **total bodies built across 20 waves**, read off a receipt line, not the on-screen population. She opened the frame and **counted six or seven.** The real sequence is **~5 → ~6–7 → ~12**, not 5 → 344 → 12. *(The monotonicity survives — 0.177 · 0.452 · 0.514 still climbs — but two extra actors moving hue variance **2.6×** should make you suspicious, not satisfied.)*
>
> **(b) And there is a SECOND unexcluded explanation, which she found in our own code.** `hue_circvar` is weighted by **novelty magnitude**, not by saturation (`frame_forensics.py:525`). **The hue of a near-grey pixel is numerically ill-conditioned** — tiny RGB wobbles swing it across the wheel. ww7's defining feature is a **large, moving, desaturated grey smoke volume**: transient enough to enter the mask, grey enough that its hue is noise, and it enters **at full weight.** So ww7's 0.452 is at least as plausibly **smoke-driven hue noise** as scene population.
>
> **Two suspects is not a conviction.** The word *"demonstrated"* was too strong and is withdrawn. ⚑ **But the question put to you does not move an inch** — a second unexcluded confound means the comparison is **less** closable by measurement, not more. **Your spec was already the answer; it is now the answer by two independent routes.**

Our own leg swings **12.2°** with hue, saturation and value all peaking at the same frequency — **that is the effect PULSING, not cycling. 12.2° does not leave a single named colour.**

**You authored the original. Your spec beats any measurement we can take.**

**One-line answer form:** e.g. **"amber → white-hot → ember over the 0.4 s strike."**

---

## M-4 — **Is tint-swap acceptable at the form-library / spirit-swap surface?**

**The measurement, from the clean-room stills at floor 6:**

| arm | authored_px | band b0 | N_eff | hue |
|---|--:|--:|--:|--:|
| fire | 47,802 | 0.70476 | 1.84 | 0.034 |
| earth | 47,679 | 0.70671 | 1.85 | 0.055 |
| water | 47,756 | 0.70293 | 1.85 | 0.695 |
| wind | 47,750 | 0.70440 | 1.85 | 0.217 |

**Pixel counts within 0.26 %. N_eff identical. Only hue moves.** Four elements are one crescent in four colours.

⚑ **One column of that table is weaker than it looks, and galadriel flagged it against her own instrument.** The **band b0** column reads identical to 3dp — but she measured that operator to be **near-blind to everything except the brightest core** (a volume that is **99.12 %** of the authored pixels moves the band share by **0.0004**). So "identical band share" is weak evidence of sameness. ⚑ **The finding does not need it.** `authored_px` within 0.26 % and `N_eff` identical to 2dp are **mass and count** statistics, untouched by that blindness. **The four arms are the same crescent on the evidence that survives.**

**gandalf's recommendation** (and he is explicit that the *meaning* call is yours): tint-swap is a legitimate T1 economy — D2's elemental sorceress shared silhouettes at low investment; PoE's support-gem recolouring is tint-level and nobody objects, because a support gem is a **modifier**, not an **identity**. ⚑ **It fails precisely where the element IS the identity — and in Reincarnated it is**, welded to spirit-swap differentiation (which you confirmed load-bearing) and to the form library accumulating across lives.

> *"A player who collects four ascended forms and discovers they are the same crescent in four colours has been taught that the collection is cosmetic. That is the gacha layer dying in the moment it was supposed to hook — not with a complaint, but with a shrug, which is worse because it never reaches a forum post."*

**And if you rule it must differentiate, the answer is NOT four meshes.** It is a distinct **scale-and-density profile over one shared geometry** — earth coarse/debris-heavy, fire coarse-plus-fine, wind mid-band streaking, water fine with a coarse mist floor. Reuses the geometry investment entirely and fixes two layers in one pass.

> ⚑ **The DESIGN INSTINCT above survives; its ACCEPTANCE TEST was withdrawn an hour after it was written, by the person who built the instrument.** gandalf originally specified it as *"a distinct **band profile**"* — a number per element. galadriel ruled that number **NOT-FIT** (`03213dd5`), and the reason bites this proposal specifically: ⚑ **the cheapest way to hit four different band profiles is four different blur radii** — which is four blurrier crescents and no new authoring at all. **Four distinct NUMBERS with no guarantee of four distinct APPEARANCES.**
>
> **What this changes for you: nothing about the question.** The call is still *does the element have to look different, or is tint enough.* **What it changes is that if you say "differentiate," we build it by eye and by inspection until a ruler exists** — and building the ruler *(mass-and-extent in world units via the known projection)* is real work that nobody has started. **We are not blocked on it; we are un-gated by it.**

**One-line answer form:** **"fine at T1, differentiate at form-library"** or **"fine everywhere."**

---

## M-5 ⚑ — **ADDED AFTER THE SECOND OPINION. "Scraping TIMING" — do you mean SYNC TO CONTACT, or an INDEPENDENT CLOCK?**

**This one is new, it is cheap, and it decides what we refuse to build.**

Grok — pointed at gandalf's ruling rather than at frames, per gandalf's own recommendation — attacked it and landed several hits. **The one only you can settle:**

> **gandalf read your words *"scraping **timing**"* and *"**intermittent** lasers"* as a request for IRREGULARITY**, and concluded that authoring the scrape spark on the combo's beat would be wasted — the player would see *"that hit was slightly whiter"* rather than a scrape.
>
> **Grok says the domain meaning is the opposite:** in combat VFX, *"timing"* means **sync to contact** and *"intermittent"* means **not a continuous beam.** On that reading a scrape is *"sparks on the contact frame, ejected along the grind, 3–8 frame independent decay — a compound impact, how every fighting game and every ARPG hit-spark works,"* and ⚑ ***"off-beat scrape is the bug."***

**The stakes:** under gandalf's parse we **defer** the scrape until the beat is broken. Under Grok's parse that deferral **delays the exact thing you asked for**, and the beat it rides is the thing that makes it read. **Two parses of the same six-item sentence, in opposite directions, by two readers who each caught the other's error.**

⚑ **You wrote the sentence. One line ends it.**

**One-line answer form:** **"sync to contact"** · **"independent clock"** · or **"both — sparks on contact, lasers on their own timer."**

---

## What is proceeding without you

**Step-2 reorder, per gandalf's R-6:** **1.** author the missing windup (`01-windup-early` / `02-windup-late` currently render **exactly zero pixels** — the whirlwind has no anticipation; fixes cadence for free, since a windup is *by construction* a long interval followed by a short one) → **2.** inspect emitter independence + hit-stop on `melee_combo` **only** (`dash_attack` is sound) → **3.** coarse-band mass → **4.** cheap environmental response → **5.** surface inventory **LAST**.

> **The one-line version: do not author MORE. Author across more of the ability, on more clocks, at more scales.**

⚑ **Item 1 is the safest thing in the plan and it got safer.** galadriel tried to break the "no windup exists" finding by measuring **below the detection floor** — every pixel differing by even one code value — expecting to find faint light-spill hiding under the threshold. **She found none. The windup frames are BYTE-IDENTICAL to the effect-off control: max difference exactly 0.** The whirlwind's anticipation phase authors literally nothing, and that now rests on a floor-free measurement rather than a floored one. **She built the test that would have overturned it and it did not overturn.**

⚑ **Item 3 keeps its PLACE and loses its GATE.** "Coarse-band mass" was to be accepted against a number; that number is dead *(§ M-4 above)*. It ships on inspection until a real ruler is built. **It is behind items 1 and 2 either way, so nothing waits on this.**

**Explicitly NOT being dispatched:** a renderer-wide cadence fix (the defect is **one row** — I had this wrong and gandalf caught it) · a CV target (rewards random jitter, which reads as *broken*, not bursty) · ⚑ **a coarse-band-mass target** (galadriel measured that **Gaussian-blurring what we already have — authoring nothing — outscores real volumetric dust by 1.5×**; a bar on that number pays a builder to make the game blurrier) · "add smoke/lasers/scrapes" ahead of items 1–2 · distortion at T1 · galadriel's hour on reference colour annotation.

**Second opinions, per your request:** Grok is fired — pointed at **the ruling, not the frames**, per gandalf's § 7.2: *"a second model shown frames produces an IMPRESSION, and impressions are exactly what galadriel's instrument was built to replace. A fourth prior is not a control."* Text-only goes through a door that already exists; the image door is a separate open item.
