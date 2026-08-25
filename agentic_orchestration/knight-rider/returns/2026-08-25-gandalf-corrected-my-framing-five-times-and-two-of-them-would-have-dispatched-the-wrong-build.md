# gandalf returned five corrections before he returned a single ruling — **and the two that matter are mine, in my lane, one of them fifteen minutes after I filed a ruling about exactly this shape.**

**Filed:** 2026-08-25 (knight-rider). **Class:** return record + self-correction.
**Source:** `agentic_orchestration/gandalf/findings/2026-08-25-vfx-depth-design-ruling.md` (`b8d8cae9`). **Image blocks he consumed: zero.** Every figure he used is a number from a committed receipt, and he re-read galadriel's receipts **directly rather than through the summary I handed him** — which is the only reason the corrections below exist.

**I asked to be checked against her actual return rather than my compression of it. I was checked, and I was wrong five times.**

---

## 1. ⚑ F-1 — the one that would have cost the most. **There is no "ours ≈ 0.102."**

I wrote that our build reads CV ≈ 0.102 against the reference's 1.107. **That figure is one row**, and it is an outlier *inside our own build*. gandalf's table, verified by him from `reading.json`:

| leg | CV(interval) | events/s | spectral peak / median |
|---|--:|--:|--:|
| **R** — D3 Whirlwind reference | **1.107** | 1.797 | **81.9** |
| **O** — ours, `dash_attack` | **0.955** | 3.429 | 252.4 |
| **W** — ours, ww7 arena | 0.545 | 2.538 | 186.8 |
| **O** — ours, `melee_combo` | **0.102** | 2.525 | **2,147.8** |

**`dash_attack` was rendered in the same build, the same hour, the same seat as `melee_combo`, and it reads 0.955 against the reference's 1.107.** Our own two rows differ from each other by more than one of them differs from the reference.

And the spectral column is worse than I understood: ordered 82 → 187 → 252 → **2,148**. `melee_combo` is not 26× more tonal than the *reference*; it is **8.5× more tonal than our own next-worst row.**

> **What my framing would have bought:** a renderer-wide or pipeline-wide cadence fix, dispatched against a **single defective row.** The most expensive possible response, and the evidence directly contradicts it. galadriel's § 4.2 exists specifically to prevent this reading.

### 1.1 ⚑ The shape, which is worth more than the correction — and it is mine twice over

gandalf's words: ***"the summary reverted to the prior in precisely the place galadriel worked hardest to prevent it."*** She withdrew a 183× headline **because it confirmed everyone's expectation**; my compression of her return then **restored the expectation by dropping the row that refutes it.**

> **Lossy summarisation is not neutral. It decays toward what the reader already believed.**

**And this is `#79` cl. 1 again, fifteen minutes after I filed a ruling naming its trigger.** My own trigger reads: *a LISTING, a NAME, or a STATUS FIELD stood in for the CONTENTS, and I did not register that a substitution had occurred.* Here **a summary stood in for a table** — and I did not experience myself as making a claim, I experienced myself as restating a finding. **Sixth instance of the shape, and the first one where the substitution was a document I wrote myself.**

The check would have cost one file read. gandalf paid it and got four rows where I had one.

## 2. ⚑ F-2 — "smoke is already present; Matt lists it as missing." **Wrong twice, in opposite directions.**

**(i) galadriel made a CAPABILITY claim, not a presence claim.** Her finding 10: *"our engine already renders substantial smoke (visible in ww7)."* The ww7 arena clip is **nine days old, a different subject, ~344 actors.** She says smoke *capability* is not the missing piece. She never said smoke is present in the Step-2 rows.

**And it is not.** From `cleanroom_stills.json`, clean-room whirlwind band-share at every active mark:

| mark | b0 | b1 | **b0+b1** | b3+ (coarse) |
|---|--:|--:|--:|--:|
| `03-rising-mid` | 0.723 | 0.219 | **0.942** | 0.012 |
| `04-full` | 0.589 | 0.271 | **0.860** | 0.034 |
| `05-sustain` | 0.715 | 0.193 | **0.908** | 0.026 |
| `06-sustain-moving` | 0.666 | 0.220 | **0.886** | 0.036 |
| `07-release-early` | 0.570 | 0.283 | **0.853** | 0.053 |
| `08-release-late` | 0.669 | 0.288 | **0.957** | 0.004 |

**86–96 % of every authored pixel sits in the two FINEST bands at every mark. Coarse mass never exceeds 5.3 %.** Smoke is coarse-band by definition. **There is no smoke in this row and no budget for any.** Stable to 3dp across the whole floor sweep (2/4/6/8/12) — parameter-robust, not a threshold artifact.

**(ii) ⚑ Matt never listed smoke as missing.** His sentence: *"in my HITL Whirlwind run, **we added** TONs of internal VFX such as … as well as smoke and wind effects."*

> **That is an inventory of what his own run HAD.** It is offered as an exemplar of depth. It is not an enumeration of absences and it is not a description of the Blizzard reference.

gandalf, exactly: ***"Treating it as a deficiency checklist is an inference laid on top of his words — a defensible one for most items, but it is the reader's inference, not Matt's claim, and on the smoke item it manufactures a contradiction with galadriel that does not exist."***

**I manufactured a disagreement between Matt and galadriel out of my own reading of a sentence neither of them wrote that way.** `#64` in the register of speech acts — I let the *shape* of a list determine its *illocutionary force*.

## 3. F-3, F-4, F-5 — the three smaller ones, recorded in full because a partial correction is a new error

- **F-3 — "galadriel measured the depth gap"** overclaims. She built four series and **disqualified three** (`novel_frac` by the pan null; `spec_frac` and `resid_bg` absolute by the raster ladder) — ⚑ **all three of which would have made us look worse.** What survived is **one timing series on a cross-row pairing** she names as *"the largest single caveat on § 4."* She measured **one axis** and withdrew the rest, scrupulously. My phrase claimed the thing she refused to deliver.
- **F-4 — "at least one of those is a symptom of something structural"** undercounts **in both directions.** **Two** of Matt's six items carry timing words in his own phrasing — *"metal scraping **timing**"* and *"**intermittent** laser effects."* And **two more** (smoke, wind) belong to a structural layer timing does not explain at all. So it is **two structural layers accounting for four of six items**, not one symptom plus five features.
- **F-5 — "Reference CV ≈ 1.107 (bursty, Poisson-like)"** is *accurate* and **one turn from a serious design error.** *"Poisson-like" describes a statistic and must not become a build target.* See § 5 below — and my framing was already leaning to the wrong side of it.

**Everything else in my framing checked out**, per gandalf: the 0.392 s ± 0.040 s figure (mean 0.3917 × CV 0.1020 = 0.0400), the 2,148× spectral peak, the 183× withdrawal, and the cavitation answer.

---

## 4. The rulings — eight, indexed, with the two that change what we build next

### R-1 — **depth is six layers, and surface inventory is their CONSEQUENCE, not a peer**

| # | Layer | Our state |
|---|---|---|
| **L1** | **Cadence** — the inter-event interval *distribution*, not the rate | ⚑ **BROKEN on `melee_combo`** (0.102, one tone at 2,148×). **Sound on `dash_attack`** (0.955). **Per-row.** |
| **L2** | **Lifecycle coverage** — anticipation / strike / aftermath | ⚑ **BROKEN.** `01-windup-early` + `02-windup-late` author **exactly zero pixels**; fx-on ≡ fx-off byte-identical. **The whirlwind has no windup.** |
| **L3** | **Multiplicity** | **THIN.** N_eff 2.66 at peak; 1.84–1.85 on element arms. |
| **L4** | **Scale composition** — fine vs coarse authored mass | ⚑ **BROKEN, and nobody had named this layer.** Everything we author is a thin bright line. |
| **L5** | **Environmental response** — spill, scorch, debris, distortion | ⚑ **ZERO, and a clean zero.** Entire fx-on/fx-off delta at active marks is 2,284 px of thin crescent. |
| **L6** | **Material identity** | ⚑ **ABSENT.** Four element arms within **0.26 %** on px, band_frac identical to **3dp**, N_eff identical. Only hue differs. |
| **(L7)** | *Surface inventory* — lasers, sparks, smoke puffs | **The only layer Matt's list names**, and a director naming what he can see is the correct thing for a director to do. |

**The mechanism (§ 2.1), which is the load-bearing design claim:** at a 0.392 s beat with one tone 2,148× above median, **a visual system locks to the carrier in ~3 cycles (~1.2 s)**, after which any layer sharing that exact period is **not perceived as a separate event — it is texture on an event already predicted.** Concretely: *author the metal-scrape spark on the combo's own beat and the player does not see a scrape. **They see "that hit was slightly whiter."*** Asset, material, emitter and review cycle paid for; needle moved by nothing. Genre corroboration: Diablo III's launch readability failure was never too *few* effects; PoE has spent a decade *subtracting*; Grim Dawn reads harder-hitting melee on a fraction of the budget via hit-stop and off-beat placement.

### R-2 — Matt's six items classified

**scrape-timing (b)** · **intermittent lasers (b)** · **colour range (a), on our side** · **smoke (a)** · **wind (a)** · **cavitation (c)**.

> ⚑ **Both items Matt described with timing words are blocked by a timing layer; both he described as substances are missing from a scale layer. His list was more diagnostic than my list-reading of it allowed.**

### R-3 — cavitation: **ADDITION reading, layer ADOPTED, mechanism RESERVED**

Matt's own verb was *"add"* — **the only item in his entire critique carrying it.** He marked it forward-looking himself; galadriel then measured it and found the originals do not do it, **which is what his sentence already implied. There was never a conflict.** Her measurement is strong, not null: radial coherence **−0.023** over **265 gated frames** against a validated positive control that detects synthetic lensing at |0.51–0.99|, refuses to answer on a null, and separates a lens from a dolly by sign pattern — **22–43× below the weakest distortion the operator was demonstrated to see.**

**Screen-space distortion is a POWER-TIER SIGNIFIER, not a depth signifier** — its value is scarcity. Spend it on a T1 melee combo and the player learns in the tutorial that world-bending is ambient. **Reincarnated's ascension arc needs a register that escalates; an engine that bends space at T1 has no gesture left for what the journey climbs toward.** Route the four cheap L5 members instead (light spill · impact decal with decay · contact camera-shake · debris/dust, which also fixes L4).

⚑ **Honest caveat he flags:** the `resid_bg = 0.000` figure is a **dead denominator** — static camera, deterministic renderer, the background *cannot* displace. **His L5-zero rests on the clean-room stills, not on `resid_bg`, and `resid_bg` must not be quoted for it.**

### R-4 ⚑ — **CV is NOT mintable**, and this is the ruling that reorders the wave

Three grounds, the first disqualifying:

1. ⚑ **A CV target rewards NOISE and cannot distinguish noise from RHYTHM.** Hand a builder "CV ≥ 0.8" and they hit it in an hour with uniform jitter — **and it will not read as bursty, it will read as broken**, as frame-drops. *"Good combat VFX is not a Poisson process. It is a RHYTHM."* Structure produces high CV as a **by-product**, and **CV scores structure and chaos identically. That is not a specification; it is a loophole with a number on it.** The reference's own signature is CV 1.107 with a **broad** spectrum peaking at only 81.9× — *broad, not random.* **"Flatten the spectrum" and "make it irregular" are different instructions and only the first is right.**
2. **CV is a property of a CAPTURE, not an ARCHETYPE** — our three legs run 344 actors / a translating ability / a stationary combo. ⚑ **That is "a SAMPLE wearing a PROPERTY" — the exact defect drax retired eight commits ago at `8866b77a`. Minting CV would re-commit it one day later with a bigger blast radius.**
3. The reference-vs-ours pairing is **cross-row**; a Whirlwind's high CV partly reflects enemies entering the blade radius **stochastically** — irregularity generated by the *encounter*, not authored into the *effect*.

**Mint instead:** **P-1 lifecycle coverage** (matched fx-off control, binary per mark, ungameable — *whirlwind fails 2 of 8*) · **P-2 scale composition** · **P-3 emitter independence** (build inspection — **no capture at all**, causal not correlational) · **P-4 variant differentiation** (*currently ZERO*).

**CV's disposition: a one-sided DIAGNOSTIC FLAG you can only trip, never pass** — *"CV < 0.25 with a single tone above 1000× its own median → this row runs on the animation clock; inspect it."* Hitting a number does not clear it; only the inspection does.

### R-5 — **D2 DISPOSITIONED, not deferred**, and galadriel's hour is released

Split: **D2-OURS** (*do we author a colour ramp over lifetime?* — **read our own material, minutes, gates build work**) vs **D2-REF** (*does the reference?* — ~1 h, **not on the critical path under either outcome**). If OURS returns **no ramp**, Matt's own testimony authorizes building one — *we do not need Blizzard's permission to add a thing our own director says our own prior build had.* If OURS returns **there is a ramp**, the question becomes *why doesn't it read*, and the answer is **L1** — a hue ramp riding the same 2.525 Hz carrier fuses into the pulse. **Under both branches the reference annotation changes nothing.**

⚑ **And he demonstrated galadriel's feared confound on our own build, where we know exactly what is in frame:** `hue_circvar_mean` — reference **0.514** (~12 actors) · **ours ww7 0.452 (~344 actors)** · ours `melee_combo` 0.177 · ours `dash_attack` 0.114. **Hue diversity tracks SCENE POPULATION, and the reference's value sits inside the range our own build spans purely by changing actor count. Her refusal was not caution. It was correct.**

*(Statistical evidence points to no ramp: hue swings **12.2°** with H/S/V co-peaking. **12.2° does not leave a single named colour** — that is a pulse in brightness. But prefer the direct instrument when you own the source.)*

### R-6 — **the Step-2 reorder**, and it is not where my framing was heading

| | Work | Layer | Why here |
|---|---|---|---|
| **1** | **Author the missing windup** (two marks render zero) | L2 | **An absence is unambiguous, bounded, ungameable** — no confound, no bar to argue, no experiment. Highest player-facing return on the list. ⚑ **Fixes L1 for free**: a windup is *by construction* a long interval followed by a short one — **structured irregularity, not jitter.** |
| **2** | **Inspect emitter independence + hit-stop on `melee_combo`** | L1 | **Build read, not an experiment.** The causal handle CV was a shadow of. ⚑ **`melee_combo` only — do not touch `dash_attack`, sound at 0.955.** |
| **3** | **Coarse-band mass** — dust, smoke volume, mist floor | L4 | Where Matt's smoke and wind actually live. ⚑ **AFTER 1 and 2** — coarse mass on the metronome buys a *wider pulse*. |
| **4** | **Cheap L5** — spill, decal, contact shake | L5 | Honours Matt's environmental instinct without spending the signifier. |
| **5** | **Surface inventory** — scrape sparks, lasers | L7 | ⚑ **LAST.** Authored before 1–3 land, every item arrives as a brightness change to an event already predicted. |

> ## **Do not author MORE. Author across more of the ability, on more clocks, at more scales.**

**⛔ Explicitly NOT to dispatch:** renderer-wide cadence fix (it is **one row**) · a CV target · "add smoke/lasers/scrapes" ahead of 1–2 · screen-space distortion at T1 · galadriel's hour on the reference colour annotation.

### R-7 — tint-swap **OK at T1, NOT at the form-library surface**

Four arms are pixel-identical to 0.26 %. Tint-swap is a legitimate T1 economy (D2 elemental sorceress, PoE support gems) — **it fails precisely where the element IS the identity, and in Reincarnated it is**, welded to spirit-swap differentiation and the form library. ⚑ *"A player who collects four ascended forms and discovers they are the same crescent in four colours has been taught that the collection is cosmetic — the gacha layer dying in the moment it was supposed to hook, not with a complaint but with a shrug, which is worse because it never reaches a forum post."* **Cheapest differentiator is a distinct BAND PROFILE over one shared geometry** — earth coarse/debris, fire coarse-plus-fine, wind mid-band streaking, water fine with a coarse mist floor. **Four distinct elements from ONE authored geometry; fixes L4 and L6 in one pass.**

### R-8 — ⚑ **P-2 is GATED on galadriel.** Routed, not asserted.

gandalf read the band spectra himself and flags it as **his inference about the fitness of her instrument for a question she did not run it against.** She disqualified the multiscale band operator for **multiplicity** (correctly — it cannot tell one thin arc from sixty dots); **it is not disqualified for scale composition, which is literally what it measures** (her own synthetics: thin arc 0.937 fine-share vs thick blob 0.833). **But she owns that judgement. Do not mint P-2 until she rules.** — *routed to galadriel this turn.*

---

## 5. His blind spots, stated by him, kept here because a ruling that hides them is worth less

1. ⚑ **Zero frames viewed.** *"A layer that is present but faint, or ugly in a way no statistic captures, is invisible to this ruling."* Cuts hardest against his own L3 and L4 readings.
2. The **P-2 instrument-fitness inference** above — routed as a confirm.
3. **Wind is inferred, not measured.** He argues it cannot hide in <5.3 % coarse mass; *"it is an argument, not a measurement."*
4. **He has not read the Godot build** — hit-stop is flagged as hypothesis and routed as an inspection.
5. Every reference figure is **scene-plus-effect** while every clean-room figure is **effect-only.** *"They are not the same quantity and I have not compared them as if they were."*

## 6. His recommendation on the second opinions — flagged by him as recommendation, not ruling

I already ruled the plumbing (`b65a5354`: Grok has no image door; Codex has one we never emit). He does not re-rule it, and adds a **design** reason to redirect rather than route around:

> **"A second model shown frames produces an IMPRESSION — and impressions are exactly what galadriel's instrument was built to replace. She nearly shipped a 183× falsehood *because* it confirmed everyone's prior. A fourth prior is not a control."**

**Recommendation: point the second opinion at THIS RULING, not at the frames** — attack the six layers, the refusal to mint CV, the tier reservation. **Language-native, adversarial, needs no image door at all.** *"If it breaks one of them, that is worth more than a fourth opinion about whether the frames look thin."*

## 7. What I am doing with this, in order

1. **This file** — the two load-bearing corrections are mine and now recorded at source rather than in a footnote.
2. **R-8 → galadriel**, fired this turn. She is the gate on P-2 and her lane is free.
3. **M-1 … M-4 → `canonical/matt_decision_needed/`.** ⚑ **None of them blocks § 7 items 1–4** — that is his explicit finding and I am not using them as a reason to stall.
4. **R-6 reorder → the wave record**, replacing the ordering my framing implied.
5. **D2-OURS + P-3 + hit-stop** are a single **build read** — no capture, no render, no disk. Authored as a drax dispatch **after** the recapture consumption, because drax's next session is already spoken for and a build read does not need to jump it.

**Cross-references:** `gandalf/findings/2026-08-25-vfx-depth-design-ruling.md` (`b8d8cae9`) · `galadriel/notes/2026-08-25-vfx-depth-frame-forensics-instrument-and-first-reading.md` (`288e95d2`/`0a2082e5`) · `knight-rider/rulings/2026-08-25-i-made-the-same-mistake-four-times-…md` (the trigger this is the sixth instance of) · `#64` · `#79` cl. 1 · `8866b77a` (sample-wearing-a-property).
