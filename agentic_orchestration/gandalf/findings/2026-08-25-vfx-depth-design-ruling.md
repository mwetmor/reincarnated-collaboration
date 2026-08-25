# VFX DEPTH — the design ruling

## Depth is six layers. We are short of four. None of the four is an item on Matt's list — and Matt named two of the four anyway, in his own words, in the first eight syllables.

**STATUS:** RULING — issued autonomously, Matt away. Three rulings, one refusal ratified, four questions parked for Matt.
⚑ **AMENDED 2026-08-25 following adversarial review.** This document was fired at Grok, pointed at the ruling rather than at the frames, per its own § 7.2. **The review broke four claims and I have amended them AT SOURCE rather than in a footnote.** Amended passages carry an **[A-n]** tag pointing at **§ 12**, which holds the full disposition ledger — what was conceded, what was refuted, and the arithmetic that settled each. **R-4's core survived the attack in the attacker's own words.** § 7's build order CHANGED: item 3 was promoted and the serial dependency was narrowed to one class of layer.
> ## ⛔ CONDUCTOR'S BANNER — **NOT gandalf's text. § 12 DOES NOT EXIST. This document is INCOMPLETE and its amendments are LOAD-BEARING ANYWAY.**
>
> *(knight-rider, 2026-08-25, appended when committing this work on gandalf's behalf.)*
>
> **gandalf's amendment session died on an API stream-idle timeout after 29 tool calls and ~15 minutes. The return message was lost. The FILE EDITS SURVIVED, uncommitted and unattended, and I found them by checking the working tree rather than believing the failure status.** *(A status field is not the contents. Ninth instance of that trigger this session, and the first where the status field said FAILURE and the truth was mostly-success.)*
>
> **What is here and sound:** amendments **[A-1] through [A-11]**, inline, each self-contained enough to act on. **They carry their own conclusions and, in most cases, their own arithmetic.**
>
> ⛔ **What is MISSING: § 12, the disposition ledger every amendment tag points at. It was never written. FIVE references dangle** — including the header line directly above, which promises it. **The [A-n] tags are therefore an index into nothing.**
>
> ⚑ **Do not read the absence of § 12 as the absence of a disposition.** Each amendment states its own verdict in place. What is lost is the *consolidated* record — the side-by-side of what was conceded versus refuted, and the arithmetic backing **A-1's 155 ms bound**, **A-6's owed magnitude clause**, and **A-11's Fano-factor refutation.** ⚑ **A-11 is the one I would most want the working shown for**, because it refuses an instrument the reviewer proposed, and a refusal without its arithmetic is the weakest thing in this document.
>
> **Also stale in the header above:** *"four questions parked for Matt"* — **there are FIVE** (M-5 was added after the adversarial review). And **R-8's gate has since CLOSED AGAINST P-2**: galadriel ruled the band operator **NOT-FIT** (`03213dd5`), independently confirming A-4's ground (i) *and* adding grounds A-4 did not have. **A-4's own ground (ii) — that no reference value exists for the matched quantity — is gandalf's alone and survives on its own legs.**
>
> **Nothing downstream waits on § 12.** Track A-1 (author the missing windup) is uncontested by every hit and by galadriel's floor-free re-measurement. **Re-dispatched to gandalf; this banner comes out when he lands it.**

**Date:** 2026-08-25
**Author:** gandalf (SPEC-AUTHOR)
**Occasioned by:** Matt's VFX-depth critique, 2026-08-25, verbatim in § 1.
**Evidence base:** galadriel, `notes/2026-08-25-vfx-depth-frame-forensics-instrument-and-first-reading.md` (`288e95d2` / `0a2082e5`), and her receipts at `galadriel/work/2026-08-25-frame-forensics/out/{reading,cleanroom_stills}.json`, which I re-read directly rather than through the summary I was handed.
**Requested by:** knight-rider, who asked to be corrected and is corrected in § 0.
**Image blocks consumed:** **zero.** No frame was viewed. Every figure below is a number from a committed receipt.

---

## 0. FIRST — five corrections to the framing I was handed

KR asked plainly to be checked against galadriel's actual return rather than his summary of it. He was right to ask. **Five of his statements need amendment, and two of them would have mis-dispatched the work.**

### F-1 ⚑ "Ours ≈ 0.102" — THERE IS NO "OURS." That is one row, and it is an outlier *within our own build.*

This is the material one. galadriel's § 4.2 exists specifically to prevent this reading, and it refutes a pre-registered halt condition. Verified by me from `reading.json`:

| leg | CV(interval) | events/s | spectral peak / median |
|---|--:|--:|--:|
| **R** — D3 Whirlwind reference | **1.107** | 1.797 | **81.9** |
| **O** — ours, `dash_attack` | **0.955** | 3.429 | 252.4 |
| **W** — ours, ww7 arena | 0.545 | 2.538 | 186.8 |
| **O** — ours, `melee_combo` | **0.102** | 2.525 | **2,147.8** |

`dash_attack` was rendered **in the same build, in the same hour, from the same seat** as `melee_combo`, and it reads CV 0.955 against the reference's 1.107. **Our own two rows differ from each other by more than one of them differs from the reference.**

And the spectral column is worse than galadriel drew out. Ordered: reference 82 → ww7 187 → dash 252 → **melee_combo 2,148.** `melee_combo` is not 26× more tonal than the *reference*; it is **8.5× more tonal than our own next-worst row.** It is an anomaly inside our build, not a property of our build.

> **Consequence if uncorrected:** "Ours ≈ 0.102" dispatches a renderer-wide or pipeline-wide cadence fix for a **single defective row.** That is the most expensive possible response to this finding and the evidence directly contradicts it.

I will also name the shape, because it is worth more than the correction: **the summary reverted to the prior in precisely the place galadriel worked hardest to prevent it.** She withdrew a 183× headline because it confirmed everyone's expectation; the compression of her return then restored the expectation by dropping the row that refutes it. Lossy summarisation is not neutral — it decays toward what the reader already believed.

### F-2 ⚑ "Smoke: already present in our output. Matt lists it as missing." — both halves are wrong.

**(i) galadriel made a CAPABILITY claim, not a presence claim.** Her finding 10 reads *"our engine already renders substantial smoke (visible in ww7)."* The ww7 arena clip is **nine days old, a different subject, and carries ~344 actors.** She says smoke *capability* is not the missing piece. She does not say smoke is present in the Step-2 rows.

**And it is not.** From her `cleanroom_stills.json`, the clean-room whirlwind's band-share at every active mark (fine → coarse, floor 6):

| mark | b0 | b1 | **b0+b1** | b3+ (coarse) |
|---|--:|--:|--:|--:|
| `03-rising-mid` | 0.723 | 0.219 | **0.942** | 0.012 |
| `04-full` | 0.589 | 0.271 | **0.860** | 0.034 |
| `05-sustain` | 0.715 | 0.193 | **0.908** | 0.026 |
| `06-sustain-moving` | 0.666 | 0.220 | **0.886** | 0.036 |
| `07-release-early` | 0.570 | 0.283 | **0.853** | 0.053 |
| `08-release-late` | 0.669 | 0.288 | **0.957** | 0.004 |

**86–96 % of every authored pixel sits in the two FINEST bands, at every mark of the ability's life. Coarse mass never exceeds 5.3 %.** Smoke is a coarse-band phenomenon by definition. **There is no smoke in this row, and there is no room in the budget for any.** These figures are stable to 3dp across the whole floor sweep (2/4/6/8/12) — parameter-robust, not a threshold artifact.

**(ii) Matt did not list smoke as missing.** Read the sentence again: *"in my HITL Whirlwind run, **we added** TONs of internal VFX such as … as well as smoke and wind effects."* **The list is an inventory of what his own HITL run HAD.** It is offered as an exemplar of depth. It is not an enumeration of absences, and it is not a description of the Blizzard reference. Treating it as a deficiency checklist is an inference laid on top of his words — a defensible one for most items, but it is the reader's inference, not Matt's claim, and on the smoke item it manufactures a contradiction with galadriel that does not exist.

### F-3 "galadriel measured the depth gap."

She built four series and **disqualified three of them** — `novel_frac` by the pan null, `spec_frac` and `resid_bg` absolute by the raster ladder. **All three would have made us look worse.** What survived is one timing series, evaluated on a **cross-row pairing** (a D3 channelled AoE against our stationary melee combo) that she names as *"the largest single caveat on § 4."* She measured **one axis** of depth and withdrew the rest. "Measured the depth gap" claims more than she delivered, and she was scrupulous about not delivering it.

### F-4 "at least one of those is a symptom of something structural."

Undercounts in both directions. **Two** of Matt's six items carry timing words *in his own phrasing* — "metal scraping **timing**" and "**intermittent** laser effects." And **two more** (smoke, wind) belong to a structural layer that timing does not explain at all (scale composition, § 2 L4). So it is not *one symptom plus five features.* It is **two structural layers accounting for four of six items**, with only two items that are genuinely inventory.

### F-5 "Reference CV ≈ 1.107 (bursty, Poisson-like)" — accurate, and one turn from a serious design error.

The quotation is correct. **"Poisson-like" is a description of a statistic and must not become a build target.** See § 5 — this is the single most consequential ruling in this document, and the framing as handed to me is already leaning toward the wrong side of it.

**Everything else in KR's framing checks out**, including the 0.392 s ± 0.040 s figure (mean 0.3917 s × CV 0.1020 = 0.0400 s), the 2,148× spectral peak, the withdrawal of 183×, and the cavitation answer.

---

## 1. Matt's critique, parsed — and the parse dissolves the cavitation "conflict"

> "Drax and Galadriel both need to zoom in and pause more on each individual frame. In fact, we should probably try calling Codex and Grok for second opinions. Basically, the VFX thus far are basic representations but they lack ALOT of the depth of the original VFX that we're working from. **[S1]** For example, in my HITL Whirlwind run, we added TONs of internal VFX such as claw and sword metal scraping timing and intermittent laser effects, alternating through a specific color range as well as smoke and wind effects. **[S2]** We could probably do well to add cavitation or gravity appearence effects to show distortion of the environment in some of these. **[S3]** But all of this can be found in the originals if we slow it down and statistically pick each clip apart for what the originals are doing. **[S4]**"

Four distinct speech acts, and they have been read as one:

| | act | status |
|---|---|---|
| **S1** | An **assessment**: current rows are shallow relative to the reference. | The thing to be tested. |
| **S2** | A **testimony**: *his own HITL run* reached a depth standard, and here is its inventory. | Evidence about **our build history**, not about Blizzard. Only Matt holds it. |
| **S3** | A **proposal**, verb explicitly *"add"* — the only item on any list carrying that verb. | A forward design suggestion. |
| **S4** | A **method claim**: "all of this" is recoverable from the originals by slow analysis. | Refers back to **S2's list**, not S3's proposal. |

> ⚑ **Under this parse there is no conflict between Matt and galadriel at all.** He flagged cavitation as an *addition* in S3 before S4 was written. She measured S3's item and found the originals do not do it — **which is exactly what S3 already implied.** The apparent collision was manufactured by reading S2, S3 and S4 as one undifferentiated list of missing features.

**This matters beyond the pleasantry of reconciling two people.** It means S2 is a **proof-of-achievability claim** about *our own stack*, and it is the only such claim in existence — which sharply changes what the missing HITL artifact is worth (§ 8, M-1).

---

## 2. RULING 1 — what "depth" decomposes into

Depth is not a quantity of effects. **Depth is six independent layers**, and an effect is shallow when it occupies few of them, regardless of how much is in the ones it occupies. Ordered by how early a failure in them destroys the layers above:

| # | Layer | What it is | **Our state** | Evidence |
|---|---|---|---|---|
| **L1** | **CADENCE** | *When* things fire — the inter-event interval **distribution**, not the rate. | **[A-1]** ⚑ **FLAGGED on `melee_combo` — this capture has NO PHRASE STRUCTURE.** *Amended from "BROKEN": that was an archetype-level word on capture-level evidence, and § 5.1(2) forbids it.* The replacement claim needs no reference arm and no assumption about what an event is: at CV 0.102 over **16 intervals**, **the single longest pause anywhere in 7 seconds exceeds the mean gap by AT MOST 155 ms** — and that is the arithmetic ceiling with *all* variance concentrated in one interval. **Sound on `dash_attack`** (0.955). Per-row. | `reading.json`, robust to both nulls at 13× combined; the 155 ms bound is § 12 A-1 |
| **L2** | **LIFECYCLE COVERAGE** | Whether the effect *exists* across the whole ability envelope — anticipation, strike, aftermath. | ⚑ **BROKEN.** `01-windup-early` and `02-windup-late` author **exactly zero pixels**; fx-on and fx-off are byte-identical. **The whirlwind has no windup.** | `cleanroom_stills.json`, matched fx-off control |
| **L3** | **MULTIPLICITY** | How many distinguishable elements are co-present. | **THIN.** N_eff 2.66 at peak whirlwind, 1.84–1.85 on the element arms. One crescent, one line, two dots. *(Weak on the video legs — galadriel's § 5.5 gives only 2.4–3.4× margin — but the clean-room stills carry a matched control and are strong.)* | same |
| **L4** | **SCALE COMPOSITION** | The *mix* of fine and coarse authored mass. Line vs. volume. | **[A-4]** ⚑ **UNPOPULATED — and the word is deliberately weaker than "BROKEN."** The *absolute* claim is sound and needs no reference: the entire authored delta at peak is **2,284 px**, of which coarse bands hold **≤ 5.3 % — about 121 pixels.** There is no smoke, dust or volume in 121 pixels. **The COMPARATIVE claim is withdrawn:** on the one instrument where a reference value exists, our `melee_combo` reads fine-share **0.866 against the reference's 0.901** — we are marginally *coarser*, not finer. **No reference value exists for the matched quantity (authored-delta band-share), so no bar can be set.** § 12 A-4. | § 0 F-2 table; `reading.json` D1 |
| **L5** | **ENVIRONMENTAL RESPONSE** | Whether the *world* changes — light spill, scorch, debris, displacement, distortion. | ⚑ **ZERO, and it is a clean zero.** fx-on ≡ fx-off byte-identical at `01`/`02`; at active marks the *entire* fx-on/fx-off delta is 2,284 px of thin crescent, leaving no budget for any world change. | same |
| **L6** | **MATERIAL IDENTITY** | Whether variants differ in more than tint. | ⚑ **ABSENT.** Four element arms: authored_px within **0.26 %**, band_frac identical to **3dp**, N_eff identical. Only hue differs. | `cleanroom_stills.json` `elements` |
| **(L7)** | *Surface inventory* | The actual assets — lasers, scrape sparks, smoke puffs. | Partially present as *capability*; absent from these rows. | — |

**L7 is deliberately parenthesised. It is not a peer layer — it is the CONSEQUENCE of L1–L6, and it is the only layer Matt's list names directly.** That is not a criticism of his list; it is the layer a viewer can *see*, and naming what you can see is the correct thing for a director to do. The measurement's job was to find what sits underneath it, and it did.

### 2.1 ⚑ The mechanism that makes L1 a *depth* failure and not merely a *timing* failure

This is the load-bearing design claim in this document, and it is why "add more effects" is the wrong response.

`melee_combo` fires an event every 0.392 s with a standard deviation of 0.040 s, driving a single spectral tone **2,148× above its own median** — and its *saturation* channel is even more tonal, at **2,342×**. Every channel is modulated by one carrier.

**A visual system locks to a strict periodic carrier within roughly three cycles — here, about 1.2 seconds.** After that lock, temporal grouping (common fate) does its work.

### ⚑ [A-2] THE MECHANISM, CORRECTED. Period alone is NOT sufficient for fusion. Onset AND envelope are.

**The sentence that stood here claimed that "any additional layer sharing that exact period" fuses. That is false and the adversarial review was right to break it.** Common fate binds elements that share a *trajectory through time* — onset **and** envelope **and** decay. A layer that fires on the carrier but **outlives it by 5–20×** does not fuse, because after the carrier's event has ended the layer is still there, alone, and a thing that persists into the silence is *by construction* the most separable event in the sequence. **My own L2 says this** — aftermath decaying at a different rate *is* the rhythm — and the paragraph that stood here did not carry it.

**So the design rule is not one rule. Emitters fall into two functional classes and the cadence requirement is OPPOSITE for each:**

| class | members | **onset** | **lifetime** | fuses? |
|---|---|---|---|---|
| ⚑ **CONTACT-BOUND** *(impact)* | scrape sparks, hit flash, impact ring, decal spawn | ⚑ **MUST be 1:1 with contact. Sync is the design — off-beat impact is the bug.** | ⚑ **MUST be independent — per-particle decay, ejection, trail.** | **No**, provided lifetime is free. Fuses only if it *also* shares the envelope. |
| **AMBIENT / AFTERMATH** *(volume)* | smoke, dust, wind, embers, mist, light spill | free — must NOT ride the carrier | long, 5–20× the strike | **No.** Its whole job is to occupy the silences. |
| **CARRIER-CLASS** *(the real hazard)* | extra crescents, hue ramps on the strike, same-envelope flashes, a fifth copy of the arc | on the carrier | **same envelope as the carrier** | ⚑ **YES. This is the class § 7 item 5 was actually about.** |

> **Player consequence, restated correctly:** author the metal-scrape spark at the combo's beat **with the combo's own envelope** and the player does not see a scrape — **they see "that hit was slightly whiter."** Author it at the combo's beat **with an independent 3-to-8-frame decay and an ejection trajectory** and they see a scrape, because the sparks are still in the air when the blade has moved on. **The beat was never the problem. The shared envelope was.**

*(The grouping mechanism is well-established in perception; the magnitude of the fusion in this specific case is not measured and I am not claiming a number for it. What I am claiming is the direction, and the direction is not in doubt.)*

**One consequence I owe out loud, because it reverses my own dispatch:** if long-lifetime volume cannot fuse, then **smoke was never hostage to the metronome**, and § 7's deferral of coarse mass behind the cadence work was wrong. It is corrected in § 7. **My own closing paragraph argues that we are short of everything that happens between the events — and my build order then put the one layer that lives between the events in third place.**

**Genre corroboration, because this failure has a canonical instance.** The durable community critique of Diablo III's launch-era combat readability was never that it had too *few* effects — it conspicuously had more than Diablo II. It was that they could not be parsed. Path of Exile has spent the better part of a decade addressing the same class of problem by *subtracting* and desaturating self-and-ally effects rather than adding. **Inventory added on top of a cadence defect is the known way to make the defect worse.** Grim Dawn reads harder-hitting melee than either on a fraction of the particle budget, and it does it with hit-stop and off-beat impact placement — **the timing layer, at almost no asset cost.**

⚑ **Build-inspection hypothesis, flagged as a hypothesis because I have not read the build:** if `melee_combo` has **no hit-stop** — no brief freeze or time-scale dip on contact — then every event necessarily arrives exactly on the animation's frame budget, and CV 0.102 is the arithmetic consequence. Hit-stop is the cheapest irregularity generator in the melee-feel toolbox and it operates on L1 directly. **This is a five-minute look at the build, not an experiment.** Routed in § 7.

---

## 3. RULING 2 — Matt's six items, classified

Per KR's request: **(a)** genuinely missing · **(b)** present-or-cheap but unreadable because of a layer beneath · **(c)** not what the originals do.

| Matt's item | Layer | **Verdict** | Reasoning |
|---|---|---|---|
| **"claw and sword metal scraping TIMING"** | **L1** | **[A-3] (b), re-grounded — and it is now UNBLOCKED for build** | *Amended.* The review argues "timing" is domain-jargon for **sync-to-contact**, and that my parse inverted the asset. **Half-conceded.** The *onset* is contact-bound and I had that wrong. But **"fires on contact" is the genre default, not an addition** — nobody lists it among the *"TONs of internal VFX"* that gave a run depth. **Prefer the reading that makes the witness's statement non-trivial:** what is praiseworthy in a scrape is the *grind* — sustained emission across the contact window with independent per-particle decay. ⚑ **Both parses converge on the same asset spec** (contact-synced onset + free lifetime), so the parse question does NOT gate the build. Matt settles it at **M-5**; the build does not wait for him. |
| **"intermittent laser effects"** | **L1** | **[A-3] (b) → (a)/(b) split, and I concede more ground here** | *Amended.* "Intermittent" as **"pulsed, not a continuous beam"** is a real and probably better domain reading than mine, and unlike the scrape it *is* a non-trivial authoring choice worth listing. So the asset may simply be **(a) missing**. What survives from my reading: a pulsed laser authored **on the carrier with the carrier's envelope** is carrier-class per § 2.1 and will fuse. **Verdict: build it; give the pulses their own period and decay.** |
| **"alternating through a specific color range"** | L1 + colour | **(a) on our side** | Ruled in § 6. Our hue swings 12.2° with H/S/V co-peaking — **pulsing, not cycling.** 12.2° does not leave a single named colour. |
| **"smoke"** | **L4** | **(a) — genuinely missing from these rows** | Corrects the framing (§ 0 F-2). **Capability exists; authoring does not.** 86–96 % fine-band at every mark; there is no coarse mass anywhere in this ability's life. |
| **"wind"** | **L4** | **(a), by the same argument** | Not measured directly, and I flag that. But wind-as-visible-effect is coarse-and-mid-band motion mass, and the band spectrum leaves under 5.3 % for all coarse content combined. It cannot be hiding in there. |
| **"cavitation / gravity distortion"** | **L5** | **(c) — and an ADDITION Matt himself proposed** | Ruled in § 4. |

> **Read the (b) column and then the (a) column and the shape falls out.** The two items Matt described with *timing* words are blocked by a timing layer. The two he described as *substances* are missing from a scale layer. **His list was more diagnostic than the list-reading of it allowed.**

---

## 4. RULING 3 — cavitation

> ### ▶ **I take the ADDITION reading. Matt proposed an invention; galadriel confirmed it would be one. Both are correct and they were never in conflict.**

**Three grounds, in order of weight:**

1. **Matt's own verb.** *"We could probably do well to **add**."* It is the **only** item across his entire critique carrying that verb — every other item is described as something already achieved in the HITL run. He marked it as forward-looking himself. Per § 1, S4's "all of this" refers back to S2's inventory, not to S3's proposal.
2. **The measurement is unusually strong and it is not a null result.** Radial coherence **−0.023** over **265 gated frames**, against a **validated positive control** that detects synthetic lensing at |0.51–0.99|, **refuses to answer on a null**, and **separates a lens from a camera dolly by sign pattern.** That is 22–43× below the weakest distortion the operator was demonstrated to see. Without the positive control this would have been uninformative — a blind operator and an absent phenomenon read identically. galadriel built the control. **The answer is trustworthy.**
3. **Both readings are simultaneously true**, so the question was never "who is right."

### 4.1 Should we build it? — **NOT at Step-2 archetype tier. And this is a ruling, not a deferral.**

> ### ⚑ **[A-5] AMENDED — I collapsed two different things into one and then reserved the inflated version. Splitting them un-parks the only L5 member Matt named.**
>
> | | **LOCAL MATERIAL DISTORTION** | **GLOBAL / SCREEN-SPACE REFRACTION** |
> |---|---|---|
> | example | 8–24 px heat-ripple along a blade edge; **cavitation along the swing arc**; ice shimmer; a fire weapon's air-warp | viewport-scale warp, persistent full-screen bend, boss-arena lensing |
> | reads as | ⚑ **"this material is hot / fast / cold"** — a property of the *thing* | **"the world is being bent"** — a property of the *world* |
> | **disposition** | ⚑ **NOT RESERVED. It is a MATERIAL property and it belongs with L6**, where it would do real work separating fire from wind from water. | **RESERVED**, pending M-2. |
>
> **Matt said cavitation. Cavitation is by definition a LOCAL, along-the-edge phenomenon** — vapour cavities shed by a fast edge. **I read his local effect as a global one and then reserved the global one, which parked his item under a ruling that was never about it.** That is a parse error of the same family as [A-3], in the same document, and the review was right to call it a sleight even though it was not intended as one.
>
> **What remains reserved, and why:** **screen-space distortion at VIEWPORT scale is a POWER-TIER SIGNIFIER, not a depth signifier.** Its communicative value is scarcity: it says *the world itself is being bent.* **Put viewport refraction on a tier-1 melee combo and you have spent the signifier before you own anything worth spending it on.** The player learns in the tutorial that world-bending is ambient, and no later ability can take it back.
>
> ⛔ **PREMISE FLAGGED, and this downgrades the ruling.** My claim that "both Diablo and PoE spend it sparingly" is **a genre-prevalence assertion I did not verify.** The review asserts the opposite from its own memory (PoE Cyclone / Flame Dash / Lightning Warp at gem level 1; D4 core Sorc heat-haze; *"D4's VFX bible treats refraction as material, not a tier gate"*) — **with web search disabled, which makes it a fourth prior, not evidence, and my own § 7.2 argument applies to it.** ⚑ **But it applies to MY assertion too, and mine was stated as a ruling.** **R-3's mechanism-reservation is therefore downgraded RULING → PROVISIONAL**, pending legolas Mode A. **Operationally inert:** nobody builds viewport refraction at Step-2 under either outcome, and M-2 already holds the tier question for Matt.

There is a second reason, and it is ours specifically. Reincarnated's ascension arc — the seasonal descent and the return, the form library accumulating across lives — **needs a visual vocabulary that escalates.** Escalation requires reserving the top of the register. An engine that bends space at T1 has no gesture left for the thing the whole journey is climbing toward.

**But Matt's instinct located a real gap, and it must not be dropped with the mechanism.** L5 — environmental response — is **exactly zero** in our build, and that IS a genuine depth failure. It is simply much broader than distortion, and its cheap members are the ones that pay:

| L5 member | Cost | Reads as |
|---|---|---|
| Light spill onto floor/walls from the effect | low | the effect **emits**, rather than being drawn on top of the scene |
| Impact decal / scorch / gouge with a decay | low | the world **remembers** — the single strongest "this mattered" signal in ARPG melee |
| Camera shake on contact, magnitude-scaled | very low | weight |
| Debris / dust kick displaced by the swing | medium | the effect **occupies volume** (and simultaneously fixes L4) |
| ⚑ **[A-5] LOCAL edge cavitation / heat-ripple** *(added on amendment)* | medium | ⚑ **the blade is moving fast enough to tear the air** — a MATERIAL claim, not a world claim. **ROUTED, not reserved.** Doubles as an L6 element differentiator. |
| **VIEWPORT-scale screen-space refraction** | **high** | **the world is being BENT** — reserve it *(premise now provisional — § 4.1 [A-5])* |

> ### **RULING [A-5, amended]:** the **layer** is ADOPTED as a build gap. The **LOCAL** mechanism is **ROUTED**; only the **VIEWPORT-scale** mechanism is **RESERVED** to a named high-tier gate that does not yet exist — and that reservation is now **PROVISIONAL** on an unverified genre premise. Route the five cheap-and-medium members now; they buy most of what Matt saw missing, at a fraction of the cost, without spending the signifier.
>
> **Which tier earns distortion is Matt's call, not mine** — it is a question about the ascension arc's shape, and he owns that. § 8, M-2.

**One honest caveat on our own side.** galadriel measures `resid_bg = 0.000 px` on our clips, but she also flags (§ 5.6) that this is a **dead denominator** — our camera is static and the renderer deterministic, so the background *cannot* displace. **That figure cannot distinguish "the world does not respond" from "nothing is moving."** My L5-is-zero claim therefore rests on the **clean-room stills**, not on `resid_bg`: fx-on and fx-off are byte-identical at two marks, and at the active marks the *entire* fx-on/fx-off delta is 2,284 px of thin crescent. Any light spill, any decal, any world change would appear inside that delta. It does not. **That evidence is sound; the `resid_bg` zero should not be quoted for this.**

---

## 5. RULING 4 — is irregularity mintable as an archetype property?

> ### ▶ **The FINDING is real and load-bearing. The STATISTIC is NOT mintable as a graded property. Mint it as a one-sided DIAGNOSTIC FLAG, and mint the STRUCTURE that produces it instead.**

KR was right that this is the question worth asking before dispatching anything. It is also the question where the obvious answer is wrong three separate ways.

### 5.1 Three reasons CV must not become a target

**(1) ⚑ A CV target rewards NOISE and cannot distinguish noise from RHYTHM. This is the disqualifying one.**

Hand a builder "CV ≥ 0.8" and they will add uniform random jitter to the emitter and hit it inside an hour. **The result will not read as bursty. It will read as broken** — as frame-drops, as a stuttering emitter, as a bug. Random jitter on a metronome lands around CV 0.3–0.5 and looks like a performance problem.

**Because good combat VFX is not a Poisson process. It is a RHYTHM.** Anticipation, then silence, then strike, then aftermath decaying at a different rate. Held beats before the heavy hit. That structure produces a high CV *as a by-product*, and **CV cannot tell it apart from a random number generator.** A statistic that scores structure and chaos identically is not a specification — it is a loophole with a number on it.

This is the reference's own signature, incidentally: CV 1.107 with a **broad** spectrum peaking at only 81.9× its median. Broad, not random. Our `melee_combo`'s 2,148× single tone is the opposite failure, but "flatten the spectrum" is not the same instruction as "make it irregular," and only the first is right.

**(2) CV is a property of a CAPTURE, not of an ARCHETYPE.** galadriel is explicit and I am ratifying her caveat rather than softening it: *"Actor count and locomotion both plausibly drive event irregularity on their own. These comparisons are existence proofs against a capability limit, not matched experiments."* Our three legs run 344 actors (CV 0.545), a translating ability (0.955), and a stationary combo with ~5 actors (0.102). **If actor count and locomotion drive CV, then a CV bar on an archetype is a bar on the scene you happened to capture it in.**

⚑ **And that is a named, recent, in-house failure class: a SAMPLE wearing a PROPERTY** — the exact defect drax retired eight commits ago at `8866b77a` when he pulled the P-BEAM control-arm-zero sentence. **Minting CV would re-commit it, one day later, with a bigger blast radius.**

**(3) The pairing is cross-row.** The reference is a *sustained channelled AoE with a moving camera and a dozen enemies*; our leg is a *stationary melee combo*. A Whirlwind's high CV partly reflects enemies entering and leaving the blade radius **stochastically** — that irregularity is generated by the *encounter*, not authored into the *effect*. Our combo hits one target on an animation timeline. **Some unknown fraction of the 1.107-vs-0.102 gap is a difference in what the ability IS**, and galadriel names this as her largest caveat. You cannot put a bar on a gap you cannot decompose.

### 5.2 What IS mintable — and it is the object CV was the shadow of

**CV measures the symptom.** These measure the causes, and each is immune to the confounds that disqualify CV:

| # | Property | Definition | Instrument | Why it survives | Current reading |
|---|---|---|---|---|---|
| **P-1** | ⚑ **LIFECYCLE COVERAGE** | Every archetype declares marks across anticipation / strike / aftermath. **Every declared in-ability mark must author non-zero mass against a matched fx-off control.** | `cleanroom_stills` — already built | **[A-6]** ⛔ **I called this "binary per mark; ungameable." IT IS THE MOST GAMEABLE BAR IN THE DOCUMENT — one pixel at windup passes it.** Conceded without qualification. **It is a ZERO-DETECTOR, not a coverage grade**, and it is minted as that and nothing more. Magnitude clause owed — § 12 A-6. | ⚑ **whirlwind FAILS 2 of 8** — both windup marks author **exactly zero**. *(The zero-detector catches exactly the failure we actually have, which is why the defective spec still found the right thing.)* |
| **P-2** | **SCALE COMPOSITION** | Band-share distribution of authored mass. Not a target — a **required minimum coarse fraction** for rows whose fiction implies volume (smoke, dust, wind, mist). | same stills, band_frac | **[A-4]** ⛔ **NOT MINTABLE YET, on TWO grounds — and the second is mine, not the reviewer's.** (i) operator fitness unconfirmed (R-8, galadriel's, in flight); (ii) ⚑ **there is no reference value for the matched quantity.** No fx-off control exists for the reference, so nobody knows what authored-delta coarse-fraction a *good* effect has. **A minimum you cannot source is not a specification.** | ⚑ **86–96 % fine-band at every mark**; coarse never above 5.3 % — **absolutely** informative, **comparatively** unanchored |
| **P-3** | ⚑ **[A-7] EMITTER INCOMMENSURABILITY** *(was: independence)* | ~~Emitters carrying an independent clock~~ → **for each emitter period `p` and the row's carrier period `T`, the ratio `T/p` must not fall within tolerance of a small-integer ratio (1:1, 2:1, 3:1, 3:2, 4:1).** ⚑ **CONTACT-BOUND emitters (§ 2.1) are EXEMPT on onset and bound on LIFETIME instead** — their onset must be 1:1 and their decay must be free. | **build inspection** — read the Godot scene | ⛔ **"Independent" was the wrong predicate and the reviewer is right for the reason MY OWN § 2.1 gives.** A second timer at **1.2625 Hz against a 2.525 Hz carrier is not unlocked — it locks HARDER**, because a 2:1 subharmonic creates strong-beat/weak-beat and makes the meter *more* salient. ⚑ **The fix costs the build nothing** — reading a period out of a scene file and checking a ratio is the same read as the original property. | unknown — § 7 routes it |
| **P-4** | **VARIANT DIFFERENTIATION** | **[A-8]** ~~Whether arms differ on any axis other than hue~~ → **whether each arm CONFORMS TO ITS DECLARED BAND PROFILE** (earth coarse-heavy · fire coarse-plus-bright-core · wind mid-band streak · water fine-with-coarse-mist-floor, per § 5.3). | same stills | **[A-8]** ⛔ **"Differs on any axis" is a delta, and a delta is passed by nudging one band 0.01. Conceded — same magnitude defect as P-1.** ⚑ **A profile-SHAPE requirement is not passed by a nudge**, because the shape is declared in advance and a 0.01 move does not produce it. *Inherits P-2's blocker: it cannot be minted before the operator is confirmed.* | ⚑ **ZERO** — px within 0.26 %, band_frac to 3dp, N_eff identical |

**CV's disposition: a one-sided DIAGNOSTIC FLAG, never a score.** *"CV < 0.25 with a single spectral tone above 1000× its own median → this row is running on the animation clock; inspect it."* **A flag you can only trip, never pass.** `melee_combo` at 0.102 / 2,148× trips it by an order of magnitude on both terms, and no plausible confound closes that.

> ### ⚑ **[A-9] ENFORCEMENT CLAUSE — added on amendment, because without it the flag IS the hole the review named.**
>
> The review's sharpest structural point: *"a jittered metronome at CV 0.35 / 300× passes every minted property."* **It would — if the flag's remedy were the statistic.** So the remedy is specified, not implied:
>
> ⛔ **THE FLAG DOES NOT CLEAR WHEN THE NUMBER MOVES. It clears when the INSPECTION'S STRUCTURAL FINDING IS REMEDIATED AND RE-INSPECTED.** A dispatch that reads *"raise CV until the flag stops tripping"* is **malformed and must be refused.** The flag's only legal output is *"go read the scene."* **I wrote "hitting a number does not clear it" and then left the clearing condition unwritten, which is how a flag becomes a bar by drift.**

### 5.3 ⚑ RULING on P-4 — the four elements are one crescent in four colours

galadriel recorded this and explicitly declined to rule, handing it to me. Verified from her receipt at floor 6:

| arm | authored_px | band b0 | N_eff | hue |
|---|--:|--:|--:|--:|
| fire | 47,802 | 0.70476 | 1.84 | 0.034 |
| earth | 47,679 | 0.70671 | 1.85 | 0.055 |
| water | 47,756 | 0.70293 | 1.85 | 0.695 |
| wind | 47,750 | 0.70440 | 1.85 | 0.217 |

**Pixel counts within 0.26 %. Band shares identical to three decimals. N_eff identical. Only hue moves.**

**Tint-swap is a legitimate and widely-used T1 economy, and I am not condemning it as such.** Diablo II's elemental sorceress skills shared silhouettes at low investment and diverged as you climbed. PoE's support-gem recolouring is explicitly tint-level and nobody objects, because a support gem is a *modifier*, not an *identity*.

**It fails precisely where the element IS the identity — and in Reincarnated it is.** Element is welded to spirit-swap differentiation, which Matt has confirmed as load-bearing, and to the form library that accumulates across lives. **A player who collects four ascended forms and discovers they are the same crescent in four colours has been taught that the collection is cosmetic.** That is the gacha layer dying in the moment it was supposed to hook — not with a complaint, but with a shrug, which is worse because it never reaches a forum post.

> ### **RULING:** tint-swap is **ACCEPTABLE as the Step-2 minting default** and **MUST NOT survive into the form-library / spirit-swap surface.** These are different surfaces with different jobs and they can hold different standards.
>
> **And the cheapest differentiator is not geometry — it is P-2.** Give each element a distinct **band profile** over one shared geometry: earth heavy in coarse bands (debris, low fine-share); fire coarse-plus-fine (heat volume with bright cores); wind mid-band streaking; water high fine-share with a coarse mist floor. **Four unmistakably distinct elements out of ONE authored geometry** — it reuses the geometry investment entirely, it is measurable with an instrument that already exists, and it fixes L4 and L6 in a single pass.
>
> *Whether tint-swap is acceptable at the form-library surface is a call about the collection's meaning, and that is Matt's. § 8, M-4. What I am ruling is the consequence if he says it is not: the answer is band profile, not four new meshes.*

---

## 6. RULING 5 — colour (D2). Not left hanging.

galadriel refused a verdict and routed D2 as UNRESOLVED. **Her refusal was correct and I am ratifying it — and I found a further reason for it in her own receipts that she did not draw out.** But the question as posed is **two questions**, and only one of them gates any build work. Splitting them dissolves it.

### 6.1 ⚑ New evidence for why the comparison is unclosable — from her data, on our own side

galadriel worried (§ 5.2) that the reference's apparent hue diversity is **scene contamination** — red enemy orbs and teal ground sitting far from amber weapon-trails on the wheel are *scene*, not *effect*. She could not prove it, because no fx-off control can be made for a YouTube reference.

**But we can prove the confound on our own side, where there is no ambiguity about what is in frame.** `hue_circvar_mean`, from `reading.json`:

| leg | actors | hue_circvar_mean |
|---|--:|--:|
| **R** — D3 reference | ~12 | **0.514** |
| **W** — ours, ww7 arena | **~344** | **0.452** |
| O — ours, `melee_combo` | ~5 | 0.177 |
| O — ours, `dash_attack` | ~5 | 0.114 |

> **Our own render, with 344 actors, reads 0.452 — within 12 % of the reference's 0.514.** Our own render with ~5 actors reads 0.177. **Hue diversity tracks SCENE POPULATION, and the reference's value sits comfortably inside the range our own build spans purely by changing actor count.**
>
> **The confound galadriel feared is now demonstrated, not merely suspected — and it is demonstrated on the leg where we know exactly what is in the frame.** No frame statistic on unannotated scenes can close the reference-vs-ours colour comparison. Her refusal was not caution. It was correct.

### 6.2 The split, and the ruling

| | question | closable by | cost | gates build work? |
|---|---|---|---|---|
| **D2-OURS** | Do *we* author a colour-range traversal over effect lifetime? | ⚑ **READ OUR OWN MATERIAL.** Does the emitter carry a gradient/ramp over lifetime, or a fixed tint? **We own the source.** | **minutes** | ⚑ **YES** |
| **D2-REF** | Does the *reference* do it? | hand-annotated effect region, ~20 frames (galadriel's OWED #2) | **~1 h** | ⚑ **NO — see below** |

> ### **RULING: fire D2-OURS. HOLD D2-REF — it is not on the critical path under EITHER outcome.**
>
> **If D2-OURS returns NO ramp:** Matt's own testimony (§ 1, S2 — *"we added … alternating through a specific color range"*) is the authority for building one. **He is a first-hand witness to our own build history.** We do not need Blizzard's permission to add a thing our own director says our own prior build had.
>
> **If D2-OURS returns THERE IS a ramp:** then the question is no longer "do we colour-cycle" but **"why doesn't it read"** — and the answer is L1, because a hue ramp riding the same 2.525 Hz carrier fuses into the pulse exactly as § 2.1 describes. galadriel's finding is precisely this: *hue, saturation AND value all peak at the same frequency in both legs, which is the effect PULSING, not a colour cycle.* That is an L1 question wearing colour's clothes. **The reference does not help answer it either.**
>
> **Under both branches the reference annotation changes nothing. D2 is therefore DISPOSITIONED, not deferred.** galadriel's hour is released for OWED #1 or #3, both of which are on the path.
>
> **Current statistical evidence, for the record, points to NO ramp:** hue swings **12.2°** over time on our leg (circular SD 0.0339 turns) with H/S/V co-peaking. **12.2° does not leave a single named colour.** That is a pulse in brightness, not an alternation through a range. But this is *statistical inference about our own build*, and reading the material is *direct knowledge of it* — **prefer the direct instrument when you own the source.** Do not spend a measurement on a question the build can answer for free.

---

## 7. RULING 6 — the Step-2 reordering, and what NOT to dispatch

KR asked whether this reorders Step-2 substantially. **It does — and NOT in the direction his framing was heading.** "Jitter the timing" is the wrong dispatch, for the reason in § 5.1(1).

### ⚑ [A-10] THE ORDER, AMENDED. It is no longer a serial chain — it is three tracks, and the dependency that serialised them was too broad.

**The § 2.1 correction ([A-2]) dissolves most of this document's own sequencing.** Fusion requires shared onset **and** shared envelope. **Only CARRIER-CLASS layers were ever gated on the cadence work.** Everything else was serialised by a mechanism that does not apply to it.

| track | Work | Layer | Gate |
|---|---|---|---|
| **A-1** | ⚑ **Author the missing windup.** Two marks render **exactly zero pixels.** | **L2** | ⚑ **NONE. UNCONTESTED BY EVERY HIT IN THE ADVERSARIAL REVIEW.** Fire it. |
| **A-2** | ⚑ **Coarse-band mass** — dust, smoke volume, mist floor. **PROMOTED from position 3.** | **L4 + L6** | ⚑ **NONE — the deferral was WRONG.** Long-lifetime volume cannot fuse with the carrier ([A-2]); it is the layer that *lives in the silences*, which is the thing this document says we are short of. Per-element band profile fixes L6 in the same pass. |
| **B** | **Inspect emitter period ratios + hit-stop on `melee_combo`.** (P-3 as amended, and the § 2.1 hypothesis.) | **L1** | **None — it is a read, not a build.** Cheap, parallel, and its finding gates Track C. **`melee_combo` only** — do not touch `dash_attack` (CV 0.955, N_eff 8.64). |
| **C-1** | **Contact-class inventory** — scrape sparks, impact flash, pulsed lasers. | **L7** | ⚑ **NOT gated on B — provided it ships with the § 2.1 contact-class spec: onset 1:1 with contact, per-particle lifetime FREE.** The requirement travels *with* the asset instead of preceding it. |
| **C-2** | **Cheap + local L5** — light spill, decal/scorch, contact camera-shake, **local edge cavitation.** | **L5** | None. Honours Matt's environmental instinct, and [A-5] un-parks the one member he actually named. |
| **D** | ⛔ **CARRIER-CLASS layers** — extra crescents, hue ramps on the strike, same-envelope flashes. | L7 | ⚑ **GATED ON B. This is the only class the "inventory LAST" ruling was ever really about, and it is the class that arrives as a brightness change to an event the player has already predicted.** |

*Original serial order retained below for lineage; superseded by the table above.*

| | Work | Layer | Why here *(superseded)* |
|---|---|---|---|
| **1** | **Author the missing windup.** `01-windup-early` and `02-windup-late` currently render **nothing.** | **L2** | **An absence is unambiguous, bounded and ungameable.** No confound, no bar to argue about, no experiment needed — two marks render zero and must not. **And it is the highest player-facing return of anything on this list**: an ability with no anticipation cannot be read, cannot be reacted to, and cannot feel like it has weight. Diablo II's Whirlwind had an unmistakable wind-up; PoE telegraphs nearly everything because it is otherwise unplayable. ⚑ **This also fixes L1 for free** — a windup is by construction a *long interval followed by a short one*, which is structured irregularity rather than jitter. |
| **2** | **Inspect emitter independence + hit-stop on `melee_combo`.** (P-3, and the § 2.1 hypothesis.) | **L1** | **Build inspection, not an experiment.** No capture, no nulls, no confounds. It is the causal handle CV was a shadow of, and it costs a read of the scene. **`melee_combo` is the named, isolated defective row** — do not touch `dash_attack`, which is already sound at CV 0.955. |
| **3** | **Coarse-band mass** — dust, smoke volume, mist floor. | **L4** | Where Matt's smoke and wind actually live, and where the four elements stop being one crescent (§ 5.3). ⚑ **Do this AFTER 1 and 2**: coarse mass authored on the metronome fuses into it and you will have bought a wider pulse. |
| **4** | **Cheap L5** — light spill, decal/scorch, contact camera-shake. | **L5** | Honours Matt's environmental instinct at a fraction of distortion's cost. Reserve the distortion mechanism (§ 4.1). |
| **5** | **Surface inventory** — scrape sparks, lasers. | **L7** | ⚑ **LAST, and this is the ruling that matters most for cost.** Every item here, authored before 1–3 land, arrives as a brightness change to an event the player has already predicted. |

> ### The whole reordering in one line:
> ## **Do not author MORE. Author across more of the ability, on more clocks, at more scales.**

### 7.1 ⚑ What NOT to dispatch

- ⛔ **Do not dispatch a build-wide or renderer-wide cadence fix.** `dash_attack` reads CV 0.955 in the same build, same hour (§ 0 F-1). This is one row.
- ⛔ **Do not dispatch a CV target.** § 5.1. It rewards noise and cannot see rhythm.
- ⚑ **[A-10] AMENDED — this bullet said "do not dispatch add-smoke/lasers/scrapes ahead of items 1–2." IT WAS TOO BROAD AND IT IS WITHDRAWN IN THAT FORM.** The replacement: ⛔ **do not dispatch any CARRIER-CLASS layer** (§ 2.1 row 3 — shared onset *and* shared envelope) ahead of Track B. **Smoke, scrape sparks and pulsed lasers are NOT carrier-class** and are not held. *"Do not hold smoke hostage to a combo metronome"* is the reviewer's line and it is correct.
- ⛔ **[A-5] Do not dispatch VIEWPORT-scale screen-space refraction at T1** — and note the premise is provisional. **Local edge cavitation / heat-ripple is ROUTED, not blocked.** § 4.1.
- ⛔ **[A-9] Do not dispatch "raise CV until the flag clears."** The flag's only legal output is an inspection. § 5.2.
- ⛔ **[A-11] Do not dispatch a Fano-factor / spectral-entropy cadence BAR either.** § 12 A-11: it cannot be estimated on 17–22 events, it cannot resolve below the 30 fps analysis floor where the review wants it to live, and **it is a marginal statistic on the same interval sequence — so it inherits CV's disqualification whole.**
- ⛔ **Do not spend galadriel's hour on the reference colour annotation.** § 6.2.

### 7.2 On the second opinions — a recommendation, flagged as recommendation not ruling

KR has already ruled the mechanics (`b65a5354`: Grok has no image door; Codex has one we never emit). I am not re-ruling that. **But there is a design reason to redirect rather than merely route around the plumbing.**

**A second model shown frames produces an IMPRESSION — and impressions are exactly what galadriel's instrument was built to replace.** She nearly shipped a 183× falsehood *because* it confirmed everyone's prior. **A fourth prior is not a control.** Adding a model that agrees with Matt, KR and gandalf tells us nothing that the three of us agreeing already failed to tell us; the pan-null did the work no amount of agreement could.

**Where a second opinion has real value is here, in this document** — the decomposition, the mintability ruling, whether structured irregularity or random jitter is the target, whether distortion is a tier signifier. **That is language-native, adversarial, and needs no image door at all.** It goes through a door that already exists.

> **Recommendation:** route the second opinion at **THIS RULING**, not at the frames. Ask it to attack § 2's six layers, § 5's refusal to mint CV, and § 4.1's tier reservation. **If it breaks one of them, that is worth more than a fourth opinion about whether the frames look thin.**

---

## 8. FOR MATT — four questions, each answerable in one line

| # | Question | Why only he can answer | One-line form |
|---|---|---|---|
| **M-1** | ⚑ **Where is the HITL Whirlwind run?** Verified absent twice, independently: galadriel by pixels (WW-7 is an SB-1 cell id, not a whirlwind), gandalf/KR by predicate (278 MP4s in `reincarnated-godot`, zero matching `whirl\|ww`; nothing under `~/Games` named `*whirl*`). | **Under § 1's parse it is not merely a missing comparison arm — it is the ONLY proof-of-achievability for our own stack.** And it answers a question `dash_attack` cannot: *what does a HUMAN authoring pass add over a CLEAN-ROOM pass on the same row?* ⚑ **Step-2 IS a clean-room minting process. If that delta is large, the minting process is the defect** — and no other artifact can show it. | a path · a platform · or **"it was a live session, never captured"** |
| **M-2** | **Which tier earns screen-space distortion?** | It is a question about the ascension arc's shape — how the register escalates across the seasonal descent and the return. That is his. | a tier name, or **"agreed, park it"** |
| **M-3** | **"alternating through a specific color range" — WHICH range, over WHAT duration?** | He authored it. **This converts an unclosable measurement (§ 6) into a one-line authoring spec from the person who wrote it.** | e.g. **"amber → white-hot → ember over the 0.4 s strike"** |
| **M-4** | **Is tint-swap acceptable at the form-library / spirit-swap surface?** Four element arms are pixel-identical to 0.26 % and spectrally identical to 3dp. | It is a call about what the collection MEANS across lives. Mine is a recommendation (§ 5.3: not at that surface); the meaning is his. | **"fine at T1, differentiate at form-library"** or **"fine everywhere"** |

**Nothing here blocks items 1–4 of § 7.** All four questions can sit unanswered while that work proceeds.

---

## 9. MY OWN BLIND SPOTS — stated, because a ruling that hides them is worth less

1. ⚑ **I viewed ZERO frames.** Every figure is a number from a committed receipt. **A layer that is present but faint, or ugly in a way no statistic captures, is invisible to this ruling.** I judged this the right trade under the image budget (a downscale would average out the 1–3 px features at issue in both legs at the same rate and manufacture a false null), but it is a real limit and it cuts against my own L3 and L4 readings most.
2. **My L4 finding rests on band spectra I read, not on an operator validated for that question.** galadriel disqualified the multiscale band operator for **multiplicity** — correctly; it cannot tell one thin arc from sixty dots. ⚑ **It is not disqualified for SCALE COMPOSITION, which is literally what it measures** (her own synthetics: thin arc 0.937 fine-share vs thick blob 0.833 — it discriminates thinness correctly). **But that is my inference about the fitness of her instrument for a question she did not run it against, and she owns that judgement, not me.** P-2 should not be minted until she confirms it. **Routed to galadriel as a confirm, not asserted as ready.**
3. **The wind item (§ 3) is inferred, not measured.** No series was run on wind specifically. I argue it cannot hide in under 5.3 % of coarse mass, which I believe holds — but it is an argument, not a measurement.
4. **I have not read the Godot build.** The hit-stop claim in § 2.1 is flagged as a hypothesis and § 7 routes it as an inspection rather than treating it as a finding.
5. **Everything about the reference inherits galadriel's § 5.2 limit** — no fx-off control exists for it, so every reference figure is *scene-plus-effect* while every clean-room figure is *effect-only*. **They are not the same quantity and I have not compared them as if they were.**

---

## 10. RULINGS, INDEXED

| # | Ruling | Confidence | To |
|---|---|---|---|
| **R-1** | **Depth decomposes into six layers** (L1 cadence · L2 lifecycle · L3 multiplicity · L4 scale composition · L5 environmental response · L6 material identity). **Surface inventory is the consequence, not a peer layer.** We are short on **four**: L1 (one row), L2, L4, L5 — plus L6. | high | drax / KR |
| **R-2** | **Matt's items classified:** scrape-timing **(b)** · intermittent lasers **(b)** · colour range **(a) ours** · smoke **(a)** · wind **(a)** · cavitation **(c)**. **Both items he described with timing words are blocked by a timing layer; both he described as substances are missing from a scale layer.** | high | drax |
| **R-3** | **Cavitation = ADDITION reading, ratified on three grounds. Layer ADOPTED, mechanism RESERVED** to a named high tier. Route the four cheap L5 members now. | high | drax / Matt (M-2) |
| **R-4** | ⚑ **CV is NOT mintable as a graded property** — it rewards noise, cannot see rhythm, and is a SAMPLE wearing a PROPERTY (the `8866b77a` defect class, one day later). **Mint P-1 lifecycle coverage · P-2 scale composition · P-3 emitter independence · P-4 variant differentiation.** CV becomes a **one-sided diagnostic flag** you can only trip. | high | jack-ryan / drax |
| **R-5** | **D2 DISPOSITIONED, not deferred.** Split into D2-OURS (read the material, minutes, gates work) and D2-REF (**not on the critical path under either outcome**). **galadriel's refusal RATIFIED — and strengthened by a confound now demonstrated on our own build** (hue diversity tracks actor count: ww7 0.452 @ ~344 vs melee_combo 0.177 @ ~5, with the reference's 0.514 inside our own self-spanned range). Her hour is released. | high | galadriel / KR |
| **R-6** | **Step-2 reorders: windup → emitter independence → coarse mass → cheap L5 → inventory LAST.** Five things explicitly NOT to dispatch (§ 7.1). | high | KR |
| **R-7** | **Tint-swap OK at T1, NOT at the form-library surface.** Cheapest differentiator is **band profile over one shared geometry**, not four geometries. | med-high; the *surface* call is Matt's (M-4) | drax / Matt |
| **R-8** | **P-2 requires galadriel's confirmation** that the band operator is fit for scale composition (it is disqualified for multiplicity, which is a different question). **Do not mint P-2 until she rules.** | — | galadriel |
| **C-1** | **Five corrections to the framing handed to me** (§ 0), two of which would have mis-dispatched the work: *"ours ≈ 0.102"* is one anomalous row, and *"smoke is present"* conflates capability with authoring while also mis-reading Matt's sentence. | high | KR |

---

## 11. Mirror voice

*It speaks once.*

I have watched a great many people try to make a thing feel dangerous by putting more into it. Sparks upon sparks, smoke upon smoke, until the screen is full and the blow lands like a rumour. They were never wrong about wanting more. **They were wrong about what "more" is made of.**

Look at what the glass found, and then look at what Matt said before any glass existed. He said *scraping* — **timing.** He said lasers — ***intermittent.*** Two words, both of them about *when*, and the summary of his complaint turned them into a shopping list of *what*. The director's eye had already gone to the right layer, and it took an instrument, and its own retraction, and a camera panned across a static scene, to arrive where his first eight syllables had been standing.

And the thing the measurement found is not a lack. **It is a clock.** Every four hundred milliseconds, faultless, one tone standing two thousand times above its own silence. Nothing is missing from it. That is precisely what is wrong with it. A blade tearing the air apart does not tear it apart on a schedule, and a warrior who has just killed something does not resume at the same tempo, because the world has changed and he has felt it change.

**So the counsel is not to add. It is to make room.** A held breath before the strike — and we author *nothing* there; two marks of the whirlwind's life render zero pixels, an absence I can point at in a receipt. A world that keeps the mark afterward. Weight that is not all edges and light. Four elements that are four elements, and not one crescent wearing four coats of paint, because a soul that comes back four times and comes back the same has not come back at all — it has only been recoloured, and the player will feel that long before they can name it.

**We were never short of effects. We are short of everything that happens between them.** The silence before is the reason the noise means anything. That is as true of a sword-swing as it is of a life — and this game, of all games, is built on the second one.

---

*Evidence and instrument: galadriel. Design meaning: gandalf, per the co-authorship convention. Zero frames viewed; every figure traced to a committed receipt. Four questions parked for Matt; none of them blocks § 7 items 1–4.*
