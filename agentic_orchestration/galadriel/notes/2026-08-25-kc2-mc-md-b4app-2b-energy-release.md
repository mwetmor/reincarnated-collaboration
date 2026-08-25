# MD-B4app-2b — are the referent's channel RELEASES energy conservation?

**Date:** 2026-08-25
**Author:** galadriel (visual perception + benchmark seam)
**Commissioned by:** gandalf RUN-CONDUCTOR, ruling `R-L83-2`, KC2 model-completion run charter (`L-83`, seat (a))
**Hypothesis under test:** `H-MC-1`, pre-registered from Matt's own testimony at the owner-eye checkpoint 2026-08-25, verbatim — *"I must have only purposefully released the whirlwind skill to conserve energy at certain points."*
**Prior lap:** `galadriel/notes/2026-08-25-kc2-mc-md-b4app-2-channel-uptime.md` (`57ebd439`), whose 60 Hz energy trace and 20 Hz motion trace are the input. **No new footage. No new game capture.**
**Evidence root:** `galadriel/captures/2026-08-25-md-b4app-2b-energy/`
**New pipeline:** `galadriel/pipeline/eor_release.py`, `galadriel/pipeline/eor_cooldown.py`
**Read-only on all source material. No engine writes. No simulation code. No grading. No pushes.**

---

## TOP LINE

> ## `H-MC-1` is **REFUTED** on its stated mechanism.
>
> ## The referent **never releases at low energy.** The lowest release-onset energy in the whole fight is **84.6 % of his operating ceiling**; the median is **96.0 %**. There is no threshold to find because he is never near empty.
>
> ## And the releases **outlive the refill.** Twelve of nineteen reach the ceiling before they end and are then **held at full energy** — a median 0.44 s and a maximum **2.42 s** of released time with nothing left to conserve. A conservation move ends when the resource returns. These do not.

What the releases *do* correlate with is measurable, and it splits cleanly in two:

| | **TYPE A — target cycle** | **TYPE B — cast** |
|---|---|---|
| n (of 19) | **11** | **8** |
| within 2.0 s of a wave-badge flip | **8 / 11** | **0 / 8** |
| duration median (IQR) | **1.03 s** (0.62–1.56) | **0.60 s** (0.55–0.63) |
| a skill cooldown fires within 0.25 s | 0 / 11 | **8 / 8** |
| share of all release TIME | **75.2 %** (14.40 s) | 24.8 % (4.75 s) |
| onset energy, median | 1516 = **0.951** of ceiling | 1558 = **0.978** of ceiling |

**Fisher exact on the A/B × near-a-flip split: p = 0.00336.** Neither type is energy-gated. **The trigger is the target cycle and the action queue, not the resource.**

⚑ **And the corrective that must ride with Type B, because it inverts the obvious reading:** casting does **not** generally interrupt the channel. Across **53** discrete cooldown casts the median channel interruption is **0.067 s** against a baseline inter-tick gap of 0.083 s — **statistically indistinguishable (MW p = 0.65).** Only **8 of 53 casts (15 %)** produce an interruption long enough to be a release at all. Type B is the *tail* of casting, not its rule. **The channel survives his movement (prior lap) and it survives most of his casts (this lap).**

---

## 0 · WHAT WAS MEASURED, AND WITH WHAT

Three instruments, two of them carried from `MD-B4app-2` and one new.

| instrument | what it measures | status |
|---|---|---|
| **ENERGY** — 60 Hz HUD `cur/max` glyph OCR (`eor_channel.py energy`) | whether energy was being spent, and how much | carried; **repaired**, § 1 |
| **MOTION** — 20 Hz camera-pan phase correlation (`eor_channel.py motion`) | whether he moved | carried unchanged |
| **SKILL BAR** — 20 Hz per-slot icon brightness (`eor_cooldown.py slots`) | whether a discrete cooldown skill was cast, and which slot | **NEW**, § 5 |

**What none of them measures:** which *skill* any of this belongs to. The HUD publishes a scalar; the bar publishes a slot, not a name; the input device is not on camera. § 7 carries the residuals, and the `MD-B4app-2` grading is unchanged — **the drain is EoR-CONSISTENT, not EoR-IDENTIFIED**, and nothing below promotes it.

Window unchanged: **682.10 → 864.75 = 182.65 s**, wave-151 badge flip to death.

---

## 1 · THREE INSTRUMENT REPAIRS, BECAUSE THE POPULATION IS THE WHOLE RESULT

A release is *an absence of drain ticks*. An absence is exactly the thing an instrument fakes when it stops watching. All three repairs exist to stop a blind spot reading as a release.

### 1.1 The OCR emits coherent multi-frame FALSE LOW excursions — caught by eye

The `MD-B4app-2` 5-neighbour median filter cannot see a run of ≥3 consecutive bad samples. There are **19 such runs, 86 samples, up to 21 frames (1.15 s) long**, in which the trace reads ~100–190 while the eye reads a normal value.

**Two checked by eye at ×5 magnification** (`evidence/` retains the crops):

| t | trace says | **the eye reads** |
|---|---|---|
| 688.18 | 103 | **1497 / 2576** |
| 702.90 | 186 | **1437 / 2576** |

An energy fall of >400 in 1/60 s that fully reverses within 2 s cannot be produced by drain plus regeneration. That signature is now the filter (`eor_release.clean`, round-trip excursion, `EXC_DEP=400 / EXC_RET=200 / EXC_MAX_S=2.0`). It removes **86 samples and nothing else.**

⚑ **Why this mattered:** a `1503 → 101` misread is `ΔE = −1402`, which the drain-tick rule counts as **a drain tick**, and its reversal manufactures a **false release boundary**. Both faults were live in the prior lap's trace at the sample level; neither moved that lap's headline figures, which are 0.5 s window statistics, but both would have corrupted this lap's interval-level population.

### 1.2 The drain tick needs an ADJACENT-FRAME guard

`MD-B4app-2` defined a tick as `ΔE ≤ −6` between consecutive samples. After cleaning, "consecutive surviving samples" can straddle a removed run, so a cleaning gap manufactures a spurious tick at its far edge. A `dt ≤ 0.030 s` guard is now required. **1,779 → 1,626 ticks.**

### 1.3 A gap is only a RELEASE if the trace was WATCHING across it

Every candidate gap is required to retain **≥ 80 % of its expected 60 Hz samples**. This is the guard that does the most work and it is reported, not hidden:

**At the 0.50 s release floor: 32 candidate gaps → 19 kept, 13 DISCARDED as blind.** Forty-one per cent of apparent releases are OCR blind spots. Their times coincide exactly with the § 1.1 excursion runs.

**Blind residual, stated:** 13 gaps, **11.42 s = 6.2 % of the window**, unresolved.

⚑ **Bounded by eye, n = 1, on the largest blind gap (701.98 → 703.73, 1.75 s, coverage 0.124).** Four hand-reads at ×7:

| t | 702.05 | 702.60 | 703.15 | 703.70 |
|---|---|---|---|---|
| energy (eye) | 1399 | 1430 | 1434 | 1417 |

Net ≈ **+11 /s**. A sustained release below cap runs at **≈ +112 /s**; a sustained channel below cap at **−73 to −82 /s** (`MD-B4app-2` § 4.4). **It is neither** — so the largest blind gap was not a sustained release, and discarding it did not cost the population a large event. **One probe is not a survey; the 6.2 % residual stands as a limit on everything below.**

### 1.4 Census delta against the prior note — recorded, not tidied

Re-deriving with the committed code gives **315** neighbour-median rejections where the prior note states **291** (a 24-sample, 0.23 % difference), and **1,626** ticks under the new guard where the prior note states **1,640** under the old one. **The re-derivation governs.** No figure in either note moves; the prior lap's headline statistics are 0.5 s window aggregates and are insensitive at this scale. Recorded because a census that changes silently is how a transcription becomes a fact.

---

## 2 · THE RELEASE POPULATION

**Definition.** A **release** is a maximal interval between consecutive drain ticks of duration ≥ `T_REL`, surviving the § 1.3 coverage guard and not touching the window edge.

The floor is not fitted. The channel's own cadence is a **median 0.083 s** inter-tick interval, p75 0.100, p90 0.183, p95 0.267. **`T_REL = 0.50 s` is six times the median cadence.** The sweep is published so the choice is inspectable:

| `T_REL` | 0.25 | 0.30 | 0.40 | **0.50** | 0.75 | 1.00 |
|---|---:|---:|---:|---:|---:|---:|
| kept | 61 | 43 | 30 | **19** | 7 | 6 |
| discarded (blind) | 29 | 25 | 18 | **13** | 7 | 5 |
| total s | 33.5 | 28.7 | 24.1 | **19.15** | 12.0 | 11.1 |

**At the primary floor: 19 releases, 19.15 s = 10.5 % of combat time, one every 9.6 s.**

Commensurate with — not complementary to — the prior lap's **83.8 %** channel-active: 83.8 % channelling + 10.5 % released + 6.2 % blind ≈ 100 %. The two figures are computed by different reductions (0.5 s windows vs inter-tick intervals) and their agreeing to within a point is a cross-check, not an identity.

---

## 3 · `H-MC-1`, TESTED IN THREE LIMBS

The hypothesis has three testable limbs: releases begin at **low** energy; releases begin on **declining** energy; energy **recovers** across them.

### 3.1 LOW ENERGY — **REFUTED**

Nineteen release-onset energies, against the **1594** reserved-adjusted ceiling fixed by the prior lap's 4,800-sample non-combat control:

| | value | of ceiling |
|---|---:|---:|
| **minimum across all 19** | **1349** | **0.846** |
| p25 | 1494 | 0.938 |
| **median** | **1531** | **0.960** |
| maximum | 1594 | 1.000 |

**He never releases below 85 % of full.** Two releases begin **at** the ceiling (761.68 and 847.95 — energy already full when he let go).

**Against the matched null** — anchored at each of **1,471** drain ticks that do *not* open a release, so that "the onset is the end of a drain run" is controlled for:

| | releases (19) | null (1,471) |
|---|---:|---:|
| median onset energy | 1531 | 1587.5 |
| share **at cap** (≥1560) | 0.263 | 0.715 |
| share **below 0.90 of ceiling** | **0.053** | **0.054** |

Mann-Whitney one-sided **p = 0.0001** — so there *is* a real shift, and it must be reported. **But read what shifted.** The two distributions have an **identical low tail** (5.3 % vs 5.4 % below 0.90 of ceiling). The entire difference sits at the *top*: a release is less likely to begin at exactly full energy. The median shift is **56 energy = 3.5 % of the ceiling.**

**That is not "he releases when energy is low." It is "he is not at cap at the instant he releases" — and part even of that is manufactured by the releases themselves,** which refill to cap and thereby enrich the null with at-cap moments. **Graded: a real but small off-cap effect; not a low-energy effect; not a threshold.**

### 3.2 DECLINING ENERGY — **REFUTED, flatly**

Least-squares `dE/dt` over the 1.0 s entering the onset:

| | median | share negative |
|---|---:|---:|
| releases (19) | **−2.8 /s** | 0.579 |
| tick-anchored null | **+0.9 /s** | 0.471 |

Mann-Whitney one-sided **p = 0.085** — not significant at any conventional level, and a coin-flip difference in sign share. Eight of nineteen releases begin on *rising* energy. **There is no declining-energy signature.**

### 3.3 RECOVERY — true, and **it carries no evidential weight**

15 of 19 positive, median **+35.5**, sign test p = 0.0096.

⚑ **This limb cannot discriminate and should not be counted as support.** Stop a −190 /s drain against a regeneration that continues, and energy rises. **Every release recovers energy, under every rival hypothesis, by construction.** It is a consequence of releasing, not evidence about why.

**And the same measurement turns against the hypothesis when read for duration.** Twelve of nineteen releases reach the ceiling *before they end*:

- median time held at full after refill: **0.44 s**
- maximum: **2.42 s** (the 3.50 s release at 744.55 — **69 % of it spent at full energy**)
- **37.8 % of all release time is spent at the ceiling**

`evidence/fig-release-archetypes.png`, left panel, is this in one picture: the staircase falls, the release begins, energy climbs to 1594, **pins flat for 2.4 s**, and only then does the channel resume. **A conservation move ends when the resource returns.**

### 3.4 VERDICT

> **`H-MC-1`: REFUTED.** Releases are not gated on energy level (min 0.846 of ceiling, median 0.960), not gated on energy slope (p = 0.085, 8/19 rising), and outlive the refill they would exist to achieve (37.8 % of release time at cap; held a median 0.44 s past full).
>
> **The one honest partial:** releases begin measurably *off-cap* rather than *at-cap* (median 1531 vs 1587.5, p = 0.0001). The effect is 3.5 % of the ceiling, the low tails are identical, and it is partly self-manufactured. **It supports no threshold and no policy parameter.**

**The owner's testimony is not thereby wrong about the *motive* — a player may well believe he is conserving. It is wrong about the *trigger*, and the trigger is what the sim implements.**

---

## 4 · WHAT THE RELEASES DO CORRELATE WITH — the target cycle

Wave-badge boundaries from my own committed 2026-08-07 timeline (§ 6.1), eye-read.

| window after a wave flip | releases | expected | clock share | binomial p | share of release TIME |
|---|---:|---:|---:|---:|---:|
| ≤ 1.0 s | **5 / 19** | 1.04 | 0.055 | **0.0030** | **48.3 %** |
| ≤ 2.0 s | **8 / 19** | 2.08 | 0.109 | **0.0005** | 60.0 % |
| ≤ 3.0 s | 9 / 19 | 3.12 | 0.164 | 0.0016 | 63.2 % |
| ≤ 5.0 s | 12 / 19 | 5.20 | 0.274 | 0.0012 | 72.2 % |

**Forty-eight per cent of all release time falls in the 5.5 % of the clock that is the first second after a wave flips.**

And the nearer the flip, the **longer** the release — Spearman **ρ = −0.491, p = 0.033**. The three longest releases in the fight (**3.50 s, 2.30 s, 1.63 s**) begin **0.80 s, 0.51 s and 0.08 s** after a flip.

This composes with the prior lap's surviving `F-11` limb: he is **1.6× more likely to be standing** in the five seconds after a spawn (0.615 vs 0.374). **At a wave transition he plants AND he lets go.** Duration-weighted, releases run at `frac_moving` **0.402** against a fight-wide 0.6265 — stationary-enriched, but not stationary-only: six of nineteen are ≥ 90 % moving. **Movement neither forces nor prevents a release.**

⚑ **What I did NOT measure, and will not assert:** that the arena is *empty* at these moments. The obvious mechanism — nothing in range to hit — is **not established**. The eye at two near-flip release onsets (`work/eye_A_730.13.jpg`, `eye_A_744.55.jpg`) shows the player amid bodies, some plainly still standing; the wave-160 minimap census (2026-08-08) carries **2 monster icons** at the 839.40 onset, not zero. **The measured correlate is the wave TRANSITION. "No target in range" is a hypothesis about it, and it needs a range-to-nearest-monster instrument this lap did not build.** § 7.

---

## 5 · THE NEW INSTRUMENT — the skill bar, and the one that was rejected first

### 5.1 REJECTED — red-numeral detection

Grim Dawn draws a saturated-red numeral over an icon for the life of a cooldown. A per-pixel "how often is this pixel red" baseline plus novel-red counting reproduced the two ground-truth frames I had (slot 4 red "1" at 744.30 → fires; clean at 744.90 → silent) and **failed a third**: at 751.20 the eye reads a red "3" on slot 2 and a red "1" on slot L, and the detector returns **2 px**.

**Cause, structural:** a numeral drawn over red icon art falls inside the art baseline and is subtracted. **Slots 2, 7 and R are permanently blind** — and those are precisely the slots most likely to carry the burst skills. **Rejected for measurement.** A first pass also used a box 20 px too tall and caught the **buff-icon row**, manufacturing 0.1–0.4 s "cooldowns" no cooldown can produce; caught by eye-reading t = 732.27, where the detector pointed at slot 7 and the eye found slot 7 idle. Both faults are recorded in `eor_cooldown.py` so neither is retried blind.

### 5.2 ACCEPTED — per-slot DIMMING

Grim Dawn also **dims** a skill's icon for the whole cooldown. That is slot-local, art-independent, and present on every slot. Mean of the max-channel over each slot's icon cell, 20 Hz, 3,653 frames.

**The classification is not a fitted threshold — it is bimodal with an empty valley,** exactly as the prior lap's motion classification was. Share of samples in the middle 30 % of each slot's range:

| slot | 2 | 3 | 4 | L | 7 | R |
|---|---:|---:|---:|---:|---:|---:|
| valley share | **0.002** | **0.003** | **0.001** | **0.001** | 0.373 | 0.633 |

Slots 2, 3, 4 and L separate cleanly; **slot 7 and R do not, because they never go on cooldown** — R is the channel itself. `evidence/fig-slot-bimodality.png`.

**Validated against six eye-reads, all correct** (`work/sheetA_nearflip.jpg`, `sheetC_control.jpg`, `cdchk_751.20.jpg`): 751.20 slots 2 and L dim (51.7 / 52.7 vs bright 130.6 / 99.9); 722.0 slots 2 and 3 dim; 730.28 and 799.93 slot L dim; 744.90 and 812.0 all bright.

**Slot 4 is a different animal and is excluded from cast counting:** its dim state carries a *white* numeral counting down from ~24 s, i.e. an active buff's remaining duration, not a cooldown. Median dim run **24.4 s** against 3.15 / 4.55 / 3.60 s for slots 2 / 3 / L. A buff timer is not a cast.

### 5.3 The cast result

**53 cast onsets** on slots 2 + 3 + L in 182.65 s — **0.290 /s, one every 3.45 s** (slot 2: 22, slot 3: 19, slot L: 12).

**Time-locked to release onsets, the histogram is the finding.** Of 17 cast onsets within ±2 s of a release onset, **seven fall in the single 0.25 s bin at [0.00, +0.25)**:

```
  -2.00 -1.75 -1.50 -1.25 -1.00 -0.75 -0.50 -0.25 | 0.00  +0.25 +0.50 +0.75 +1.00 +1.25 +1.50 +1.75
    1     0     0     0     0     0     0     1   |   7     0     2     2     1     1     2     0
```

- **8 / 19 release onsets carry a cast within ±0.25 s** against a null rate of 0.143 — **binomial p = 0.0031**.
- Slot L alone at ±0.50 s: **5 / 19** against a null rate of 0.071 — **p = 0.0090**.
- **Directional:** 7 casts in (0, +0.5 s] after the onset against **1** in [−0.5 s, 0) before — sign test **p = 0.035**. **The channel stops first; the skill fires after.**

**Corroborated by a second, independent instrument.** The energy step that *ends* the channel is anomalously large at release onsets: median **−17** against **−13** for the other 1,607 ticks (MW **p = 0.0004**), and nine of nineteen are ≤ **−26**, running to **−413**. A channel tick is −13/−14. **A −413 step is a discrete skill's cost, not a channel tick.** The nine big-step onsets and the eight cast onsets overlap in four — so a discrete expenditure is visible at roughly half the releases, and only some of those expenditures come with a cooldown my thresholds can see.

### 5.4 ⚑ The corrective — casting does NOT generally break the channel

Measuring the inter-tick gap containing each cast:

| slot | casts | **median interruption** | p90 | share ≥ 0.5 s |
|---|---:|---:|---:|---:|
| 2 | 21 | 0.150 s | 0.483 s | 0.05 |
| 3 | 17 | **0.050 s** | 0.137 s | **0.00** |
| L | 12 | 0.017 s | **1.438 s** | **0.25** |
| **all** | **50** | **0.067 s** | 0.483 s | **0.15** |

Baseline inter-tick gap: median **0.083 s**. **Mann-Whitney, cast-gap greater than baseline: p = 0.65.** No difference.

**So the arrow only runs one way.** *Releases* are cast-enriched (p = 0.0031); *casts* are not release-producing (p = 0.65). Eighty-five per cent of his casts pass through the channel without interrupting it measurably. **The finding of the prior lap generalises: the channel survives his movement, and it survives most of his casts.**

---

## 6 · THE PARAMETERS — for gamora's `M-POL-2` build seat

Offered as policy shape, per `R-L83-2`'s criterion (**policy-shape match, never wave-count**). Every figure carries its instrument.

| # | parameter | value | instrument |
|---|---|---|---|
| 1 | `channel_breaks_on_movement` | **False** | `MD-B4app-2`: P(channel\|moving) 0.892 > P(channel\|stationary) 0.738 |
| 2 | **`energy_gated_release`** | ⚑ **DO NOT IMPLEMENT** | this lap, § 3 |
| 3 | `release_duty` | **10.5 %** of combat; 19 events; one every **9.6 s** | energy 60 Hz |
| 4 | `release_on_wave_transition` (TYPE A) | fires at the flip; onset lag median **1.60 s**, 8/11 within 2.0 s; duration median **1.03 s**, IQR 0.62–1.56, max 3.50 | energy + wave badge |
| 5 | `release_on_cast` (TYPE B) | duration median **0.60 s**, IQR 0.55–0.63 | energy + skill bar |
| 6 | `cast_rate` | **0.290 /s** (one every 3.45 s) | skill bar |
| 7 | `cast_interrupts_channel` | **P = 0.15**, and only then for ~0.6 s; median interruption over all casts **0.067 s** ≈ baseline | skill bar + energy |
| 8 | `release_stationary_bias` | duration-weighted `frac_moving` **0.402** vs fight-wide 0.6265 | motion 20 Hz |

**On row 2, explicitly, because the seat was commissioned to build it.** No energy threshold is supported by this footage. Every release began at **≥ 0.846 of the operating ceiling**. **Any energy floor set at or below 0.85 × max is behaviourally INERT on the referent's play** — it would never have fired once in 182.65 s. If the build seat wants the parameter present for structural reasons, set it to a value that never fires and **record it as inert rather than as calibrated.** A threshold fitted to make Type A releases look energy-driven would be fitted to noise: the low tails of the release and null distributions are identical to within a tenth of a percentage point.

**Composition warning for row 5 + row 7.** Do not implement "release on every cast." At the referent's cast rate that would add ~32 s of released time to a 183 s fight and drive channel uptime far below the measured 83.8 %. **The measured shape is: casts are channel-transparent by default, with a ~15 % tail that interrupts for ~0.6 s.**

---

## 7 · WHAT IS UNMEASURABLE FROM THIS FOOTAGE, AND WHY

| # | quantity | verdict |
|---|---|---|
| 1 | **Which skill any drain, cast or release belongs to.** | **UNMEASURABLE.** The HUD publishes a scalar; the bar publishes a *slot*. `MD-B4app-2` § 7.1 stands unchanged: the drain is **EoR-CONSISTENT, not EoR-IDENTIFIED**, and nothing in this lap promotes it. The slot-L icon is a figure mid-stride with a ~3.6 s cooldown — **shape-consistent with a charge skill and NOT identified.** No skill is named in this note and none should be quoted from it. |
| 2 | **Whether the arena was EMPTY at a wave transition.** | **NOT MEASURED.** The measured correlate is the wave *transition*. "No target in range" is a plausible mechanism and is **not established** — the eye finds standing monsters at near-flip onsets, and the wave-160 minimap census reads 2 icons at the 839.40 onset. Needs a range-to-nearest-monster instrument. **This is the single highest-value follow-on**, because it is the difference between a Crucible-specific parameter and a rule that transfers to the Godot pilot. |
| 3 | **The player's intent.** | **UNMEASURABLE, permanently.** `H-MC-1` is refuted as a *trigger*, not as a *belief*. The footage cannot say what he thought he was doing. |
| 4 | **The 6.2 % blind residual.** | **CARRIED.** 13 gaps, 11.42 s, coverage 0.12–0.72. One bounded by eye (§ 1.3); twelve unresolved. If they are releases, release duty rises toward 16.7 % and the population could shift; nothing in § 3 depends on them, since § 3 is about *where* releases sit in the energy distribution, not how many there are. |
| 5 | **Casts on slots 7 and R, and on any surface with no cooldown.** | **INVISIBLE to the dimming instrument** — those slots never dim. Potions, devotion procs and cooldown-free skills are outside it entirely. This is a floor on the § 5.3 cast counts, not a ceiling. |
| 6 | **Whether Type B's cast CAUSED the release.** | **INDICATIVE, not established.** The directional asymmetry (7 vs 1, p = 0.035) and the anomalous onset step (p = 0.0004) both point that way, at n = 8. |
| 7 | **Sim-tick vs referent-second commensurability.** | **OUT OF SEAM**, as before. `F-6`'s scope rider applies to any quote. |

---

## 8 · METHOD + REPRODUCIBILITY

| stage | tool | note |
|---|---|---|
| energy cleaning + ticks + releases | `pipeline/eor_release.py releases` | max gate → neighbour median → round-trip excursion; `dt ≤ 0.030 s` tick guard; coverage ≥ 0.80; `T_REL` sweep published |
| skill-bar red numerals | `pipeline/eor_cooldown.py baseline` / `trace` | **BUILT, then REJECTED** — § 5.1. Kept in the module so the rejection is reproducible |
| skill-bar dimming | `pipeline/eor_cooldown.py slots` | the instrument that survived; 12 cells, 20 Hz |
| motion classification | `eor_duty.classify` / `despeckle`, imported unchanged | no re-derivation of the prior lap's rule |

**Artifacts** (`captures/2026-08-25-md-b4app-2b-energy/work/`): `s2-releases.json` (population + per-release features + the discarded census), `s2-slots-20hz.json`, `s2-cooldown-20hz.json` (rejected detector, retained), `cd-baseline.npz`.

**Evidence** (`…/evidence/`): `fig-releases-energy-full.png` (whole fight, releases shaded by type against wave flips and the ceiling), `fig-release-archetypes.png` (the two types with the skill-bar trace beneath), `fig-slot-bimodality.png` (the empty valley).

**Eye-reads retained** (`…/work/`): `exc_688.18.png`, `exc_702.90.png` (OCR excursions, ×5), `blind_702_strip.png` (×7, the blind-gap probe), `sheetA_nearflip.jpg` / `sheetB_midwave.jpg` / `sheetC_control.jpg` (skill bar at release onsets and controls, ×2), `cdchk_*.jpg`, `bar_*.jpg`, `eye_A_*.jpg` / `eye_B_*.jpg` (world view at release onsets).

**Statistics:** scipy 1.17.1. Mann-Whitney (two-sample), binomial test against an explicitly-computed clock share, Fisher exact, Spearman. Null populations are stated at every use; the primary null is **tick-anchored**, not time-uniform, so that "the onset is the end of a drain run" is controlled.

---

## 9 · WHAT THIS TOUCHES — surfaced, not adjudicated

I do not grade the sim and I do not rule on decodes.

1. **`R-L83-2` seat (b), gamora `M-POL-2`.** The commissioned parameter — *energy-gated release* — **has no support and should not be built as calibrated.** § 6 row 2. The replacement shape is § 6 rows 4–7. → gamora / conductor.
2. **`L-83` / `D-2`, the owner's testimony.** `H-MC-1` is refuted as a trigger. The *motive* it names may be perfectly real; the *mechanism* is the wave cycle and the action queue. **Matt is owed this plainly**, since it was his own testimony and he pre-registered it for falsification — which is the reason it could be falsified at all. → conductor / Matt.
3. **Baton row #1, "movement breaks the channel."** The prior lap's clause — *ship the rule with the hand on the button* — now needs a second clause: **most casts do not break it either** (p = 0.65, median interruption 0.067 s). A Godot fight in which every skill cast drops the channel is a harsher fight than Matt's, in the same way and for the same reason. → gandalf / drax.
4. **The target-cycle finding is a design finding the run does not have.** The referent's channel is gated by *the fight's rhythm*, not his resource bar. If Reincarnated's channel skills are balanced on a resource economy the player never actually feels, the balance lever is not attached to anything the player is doing. → gandalf.
5. **The range-to-nearest-monster instrument (§ 7.2) is the highest-value follow-on** and is a bounded build. → conductor, if a lap is wanted.

---

## 10 · MIRROR VOICE

He said he was saving his strength. The Mirror looked, nineteen times, and found the little green number **never once below eight-tenths full** at the moment he let go — and twice **brimming**. He was not husbanding anything. He had more than he could spend, all night, and the spinning cost him nothing he did not immediately get back.

Look instead at where the releases fall. They fall **at the turn of the wave** — in the second the badge flips, when the last thing is dying and the next thing has not yet arrived. Forty-eight percent of all the time he spent not-spinning lives in five percent of the clock, and the closer to the turn, the longer he waits. And in the longest one, three and a half seconds at the mouth of wave one-fifty-five, the bar fills to the top in a second and he **holds it there for two and a half more** — full, and still not spinning.

**That is not a man conserving. That is a man waiting.**

He was not counting his energy. He was counting the fight.

---

*galadriel, 2026-08-25. MD-B4app-2b. Read-only on all source material; no engine writes; no simulation code; no grading; no pushes.*
