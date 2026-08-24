# KC2 MODEL-COMPLETION RUN · D-4 — the DoT-STACKING video-measurement lap

> **Run:** KC2 Model-Completion (charter `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md`) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · ledger **L-2 / L-3 / L-20**
> **Author:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-24
> **Facet:** (i) DoT stacking — declared UNDECODABLE-FROM-SUBSTRATE, routed to empirical video measurement by Matt's ruling (RULING-NOTE § 2).
> **Laws:** READ-ONLY on every source · **Law 3 — a guessed formula never ships** · GL-12 decode-never-estimate · NOTE-9 every quantity asserts its basis · GL-6 full digests (§ 8).
> **Contention:** charter § 7 honoured — nothing written under `galadriel/captures/`.

---

## VERDICT — **MEASUREMENT-INSUFFICIENT** (charter § 4 → HALT to Matt)

**The stacking function is NOT measurable from this footage.** Four independent instruments were
designed and built against it; all four returned structural negatives, each for a *named* reason,
not for want of effort. The commissioned deliverable — "which candidate the measurements support" —
**cannot be honourably issued.** Per facet (i) there is no fallback and guessing is prohibited, so
this halts.

**But the lap is not empty.** It returns three first-of-kind MEASURED quantities the model layer
needs regardless of the stacking verdict, and — more valuable — it converts the blocker from
"we need better footage" into **a named, bounded, decidable substrate task** (§ 5). The ceiling
test is blocked by an *unresolved substrate ambiguity*, not by the video. Close that ambiguity and
the existing footage may already answer the question.

### What IS measured (ships, provenance `video-measured`)

| # | Quantity | Value | Basis |
|---|---|---|---|
| **M-1** | **DoT tick period** | **100 ms (10 Hz)** — modal gap exactly 6 frames @60 fps; mean 100.85 ms over 275 intervals (primary); **replicated independently on the sibling session at 55.2 % modal concentration over 1,443 gaps** | § 2.2, EVIDENCE 2 + 4 |
| **M-2** | DoT damage **arrival shape** | discrete ticks on the M-1 clock; the *total* is **piecewise-constant** between application/expiry events (plateau structure), not a smooth drain | § 2.3, EVIDENCE 1 |
| **M-3** | Observed instantaneous post-mitigation DoT rate on the player | **120 – 690 HP/s** across 12 primary plateaus (sibling reaches ~1,490 HP/s, no roster basis — see § 4.3) | `d4_plateaus.csv` |

**M-1 is the load-bearing by-product.** The Godot runtime must tick DoTs on *some* clock; without
this it would have been a guess. It is now a measurement, replicated across two independent
recording sessions.

### The stacking candidates, and where each stands

| candidate | status | why |
|---|---|---|
| (a) full stacking (sum) | **NOT CONFIRMED** | no instrument could count instances |
| (b) no stacking / refresh-only | **DISFAVOURED, NOT FALSIFIED** | § 3.4 asymmetry is directional evidence against it; the ceiling test that would have falsified it dies inside a substrate bracket (§ 3.3) |
| (c) per-source stacking | **INDISTINGUISHABLE from (a)** | separating them needs per-application *source* attribution; the optical channel is saturated (Lap M Q2, established) |
| (d) partial / capped | **UNTESTED** | requires a measured N-vs-rate curve, which no instrument produced |

**Nothing here is strong enough to ship as a rule.** The honest statement for the baton is that
facet (i)'s stacking function remains **UNDECODABLE-FROM-SUBSTRATE and UNMEASURED-FROM-VIDEO**.

---

## 0 — What this lap did, and the instrument it inherited

### 0.1 The starting asset

Lap K (`pm4k_full_trace.csv`) had already OCR'd the **game's own printed integer HP** at 60 fps
across the whole referent fight — 12,600 frames, 675.0 → 884.9833 s, 97.1 % certified. That is an
*exact* instrument (integers, not a bar sprite), and it is the only channel in this footage with the
resolution to see a DoT tick at all. This lap is built on it.

### 0.2 Sources (exhaustive), all READ-ONLY

| source | sha256 | used for |
|---|---|---|
| `…/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` | `4c60960d…4de8` — **re-verified in full this session**, byte-identical to Lap M | primary measurement |
| `…/eor-test-1/video/eor-warlord-2026-08-04 21-09-31.mp4` (2,498.37 s) | `cc428e94…1155` — **verified in full this session** | independent corroboration |
| Lap K `pm4k_full_trace.csv` | `bbe31eed…86ee` | the exact HP trace + OCR ground-truth labels |
| Lap I `pm4i_dot_riders.csv` (264 rows, 198 DoT) | `2dc3e380…6ce1` | rider magnitudes, durations, families |
| `reincarnated-engine/data/kc2/pe6_crucible_wave_pools_v2.csv` | `bbdc18f1…5587` | per-wave POOL population for the ceiling test |

`/Volumes/reincarnated` **re-verified mounted at lap start** (T19 requirement). Note the commission's
path pointed at `/Volumes/reincarnated/GD-matt-test/eor-test-2`, which is a **save-game directory**;
the video lives at `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/`. Corrected
without incident — recording it so the next lap's brief carries the right path.

### 0.3 The instrument this lap built (and validated)

Lap K's OCR scripts were never committed — only its outputs survive. The reader was therefore
**re-built and bootstrapped**: glyph templates were learned from 10,949 eor-test-2 frames *using Lap
K's certified values as labels*, so the label source is a prior MEASURED instrument, never an
assumption about the font.

**Validation against Lap K on the primary: 11,906 both-read frames, 99.88 % agreement, 95.3 %
coverage.** All 14 residual disagreements are one characterised defect.

> **⚑ DEFECT D-D4-1, caught and banked.** Lap K's absolute per-glyph NCC floor (0.78) *rejects a
> real digit*: the last glyph of the `hp_max` field anti-aliases against the globe rim and scores
> ~0.73, while its top-2 margin stays enormous (0.729 vs 0.456). My first reader inherited the
> absolute floor and silently returned `2000` for `20005` on 994 frames. **An absolute NCC floor is
> the wrong gate here; a top-2 MARGIN gate is the discriminative one.** Reader rewritten to gate on
> margin (≥0.15) and to prefer the *longest* valid parse — never discard a glyph that parses.
> `hp_cur` was correct in every disagreement both before and after, so no § 2–3 result depends on
> this; it is banked because the next lap to read this HUD will hit it.

Reader then transferred to the sibling video (ROI, font and `20005` HP max confirmed identical —
`evidence/roi-transfer-check.png`) and run over all 149,902 frames: **110,724 read (73.86 %)**.

---

## 1 — CALIBRATION (the step that stopped a wrong answer)

The first look at the delta histogram was seductive: on frames where regen is unclipped, `+0`
occurs 1,107 times (19.3 %) — which reads as "regen being cancelled by a DoT."

**It is not.** `+1` occurs **13 times** against 1,107 zeros, 1,457 `+2`s and 1,102 `+3`s. A smooth
continuous drain partially cancelling regen *must* produce `+1` abundantly. And zeros are
**isolated**: 1,068 of 1,077 zero-runs have length 1. The zeros are capture-side frame duplication
(the game's HP value not updating between two video frames), not damage.

Had this not been checked, every drain figure in this lap would have been inflated by a
sampling artefact. **Recorded because it is a trap for any future lap reading this HUD.**

Robust regen baseline (invariant to the duplication): mean delta over quiet unclipped frames
≈ **101.8 HP/s**; the `+2/+3` sub-population alone gives 145.8 HP/s. Both bracket the independently
decoded 129.38 HP/s (Lap M). Regen is *not* re-asserted by this lap — it is used only as a bound.

---

## 2 — WHAT THE FOOTAGE DOES CONTAIN

### 2.1 Damage events are frame-resolvable

At 60 fps with exact integer HP, every HP change is visible. Negative deltas across the primary
fight: **1,392 total** — 713 at DoT scale (1–40 HP), 468 mid, 211 at direct-hit scale (>200 HP).

### 2.2 M-1 — the 100 ms DoT tick clock

Inter-event gaps between **DoT-scale** events show a sharp mode at **exactly 6 frames = 100.0 ms**
(26.1 % of 653 gaps in the primary). Gaps of 5 and 7 frames are the ±1-frame sampling jitter of a
10 Hz clock against a 60 fps capture. Tick-weighted mean period from 12 plateau spans:
**101.78 ms**; from 275 chain intervals: **100.85 ms**; modal value exactly **100.00 ms**.

**Independently replicated on the sibling session** (different day, different recording):
modal 6 frames = 100.0 ms at **55.2 % of 1,443 gaps** — a much sharper concentration than the
primary, because the sibling's combat is less contaminated by direct hits.

Two independent sessions, one clock. **This is the lap's most secure result.**

### 2.3 M-2 — plateau structure

A *plateau* = ≥6 consecutive 100 ms-cadence events whose magnitudes sit within ±12 % of their
median. A chain of coincidental direct hits cannot hold a plateau (variable damage, variable
cadence); a DoT stack can. **12 plateaus** in the primary, **122 cadence chains** in the sibling
(longest 49 ticks).

The canonical example (EVIDENCE 1): `t = 744.8167`, **27 ticks over 2.667 s**, magnitude flat at
13–15 HP/tick, gaps `[6,7,6,6,6,6,7,6,6,5,6,7,6,6,7,5,7,6,6,6,7,6,6,7,5,6]`. A textbook sawtooth —
DoT tick down, regen up, on a rigid clock.

---

## 3 — THE FOUR INSTRUMENTS, AND WHY EACH FAILED

This is the substance of the MEASUREMENT-INSUFFICIENT finding. Each row is an *earned* negative.

### 3.1 Instrument A — decay staircase on the HP slope · **IMPOSSIBLE**

The idea: after applications stop, each instance expires on its own timer, so the recovery slope
rises in **N discrete steps** — the expiries count themselves, so N need not be known in advance.
(a) predicts N steps, (b) predicts exactly one, (c) predicts one per caster.

Requirement: a hit-free, leech-free, regen-unclipped window at least as long as one DoT duration.
Corpus DoT durations: **1, 2, 3, 4, 5, 6, 8, 10, 12 s**.

**Census over the whole 210 s referent fight:**

| criterion | longest window in the entire fight | ≥1 s | ≥2 s | ≥3 s | ≥5 s | ≥8 s |
|---|---:|---:|---:|---:|---:|---:|
| hit-free, unclipped | 1.267 s | 1 | 0 | 0 | 0 | 0 |
| hit-free, unclipped, **leech-free** | **0.983 s** | **0** | 0 | 0 | 0 | 0 |
| sibling: hit-free, unclipped, leech-free | **1.367 s** | 4 | 0 | 0 | 0 | 0 |

**The longest usable window in 3,532 s of footage is 1.367 s — shorter than all but the shortest
DoT in the corpus.** The player is never out of contact long enough for a DoT to expire under
observation. The instrument has no substrate. (Windows of up to 13.3 s exist with the player pinned
at *full* HP, but there regen is clipped at the cap and drain is invisible by construction — they
bound drain ≤ regen and cannot count anything.)

### 3.2 Instrument B — decay staircase read off TICK MAGNITUDE · **ABSENT**

A better instrument, found mid-lap: since the tick magnitude *is* the DoT rate, the staircase can
be read directly without needing a quiet window at all. Segment each chain into level plateaus and
read the level sequence; an equal-step descent counts expiring instances.

**Result: 0 multi-step descents in 23 primary chains.** Only 4 chains have ≥2 levels at all, and
every one is a single step. On the sibling, 4 of 122 chains show a nominal multi-step descent, but
every step is **1–2 HP/tick** — at the integer-quantization and regen-jitter floor, not a credible
instance expiry.

**Cause, and it is structural:** every direct hit terminates a cadence chain, and at Crucible
150–160 direct hits are near-continuous. Chains cap at 2.7 s (primary) / 5.0 s (sibling); DoTs run
1–12 s. **No DoT is ever observed running to completion.**

### 3.3 Instrument C — the CEILING test · **INCONCLUSIVE (blocked by substrate, not by video)**

Under refresh-only, at most one instance per DoT family sits on the target, so total DoT rate is
capped at Σ over families of (max single-rider dps) × (1 − player resist). Player sheet is Lap A
MEASURED (physical 16 %, bleed 85 %, all eight others 80 %); Lap M § 6.1 measured **no resistance
reduction anywhere on the board**, so the wall stands unreduced.

Max observed plateau: **690.0 HP/s** (and it is a *lower* bound — the observed tick is net of that
frame's regen, so true DoT is larger).

| population | ceiling, TOTAL limb | ceiling, PER-SECOND limb | verdict vs 690 |
|---|---:|---:|---|
| per-wave POOL (wave 157) | 219.0 | 468.4 | exceeds both → *would falsify (b)* |
| per-wave POOL (wave 160) | 229.1 | 605.1 | exceeds both → *would falsify (b)* |
| **cumulative POOL (waves 149…W)** | **619.1** | **1,568.7** | **exceeds TOTAL limb only → INCONCLUSIVE** |

> **⚑ I found a falsification and then killed it myself.** The per-wave ceiling gave a clean,
> bracket-invariant exceedance at two plateaus — strict refresh-only falsified. It does not survive
> scrutiny: **Crucible waves overlap.** A body spawned on an earlier wave can still be alive later,
> so the honest population at time *t* is the **union** of pools for waves 149…W, not wave W alone.
> Under that conservative population the exceedance collapses into the bracket. The per-wave result
> is an artefact of a population assumption I cannot justify, and it is reported here as a
> **rejected candidate finding**, not as evidence.
>
> A second, smaller catch en route: three DoT-bearing bodies were initially orphaned by the pool
> join because their `summoner` field is pipe-separated (multiple summoners) and I matched it
> exactly. Two are `nemesis_wendigo_01`'s wraiths, which carry the **top LifeLeach riders on the
> wave-160 board** — excluding them understated that board's ceiling. Fixed before the cumulative
> test was run; only 3 orphans remained of 85 distinct bodies, so the join is otherwise sound.

**The finding under the finding.** The bracket that swallows the result is *not* a video limitation.
It is **Lap I § 5.1, DECLARED GAP — the DoT magnitude convention**: is `offensiveSlowPoisonMin = 890`
with `duration = 5.0` the *total* over 5 s (178 dps) or the *per-second* rate (890 dps)? Lap I could
not settle it from substrate and bracketed it honestly; the bracket is a factor of up to 12, and it
is exactly what makes 690 HP/s undecidable against a 619–1,569 HP/s ceiling. See § 5.

### 3.4 Instrument D — the RE-APPLICATION test · **CIRCULAR, then UNDERPOWERED**

Most monster DoT riders in this corpus ride on attacks, so **every direct hit is also a DoT
application event** — the applications count themselves. During a flat plateau, (a) predicts the
level rises with each application; (b) predicts it stays flat.

**First form — applications *inside* a plateau: 0 observed, across all 12 plateaus.** This is not a
result, it is a **construction artefact**: the plateau detector requires magnitudes within ±12 %,
and a direct hit violates that by definition. The two detectors are mutually exclusive; the
experiment cannot run in this form. *(Recorded because it looks like a finding and is not.)*

**Second form — DoT rate immediately before vs after an intervening hit.** 16 usable pairs:

- **9 up, 7 down** — not decisive by count.
- **But the asymmetry is marked:** rises are large (115→160, 160→320, 245→400, 360→690, 280→670,
  220→740 — up to **3.4× off a single hit**), while falls are small and gradual (120→115, 400→390,
  390→360) and read as expiry, not as re-application.

**Reading, stated at its true weight:** this is **directional evidence disfavouring strict
refresh-only** — under (b), once all families are present no further application can raise the
rate, yet large rises keep occurring. It is **not** a measurement of the rule, because the *type*
carried by each hit is unattributable: a rise is equally consistent with (a) same-type addition,
(c) a new source, or (b) a family not yet present. n = 16. It does not ship.

### 3.5 The channel that does not exist

Grim Dawn's HUD prints **no per-damage-type breakdown** and no DoT stack counters
(`evidence/hud-strip-t776.png`, `evidence/buff-icon-row-4times.png` — the icon rows adjacent to the
globes are skill-bar slots with keybind numerals, not a stack display). Lap M already established
that the optical/VFX channel at Crucible 150–160 is **saturated past the point of resolving
individual arrivals**. There is therefore no attribution channel in this footage at all.

---

## 4 — COVERAGE DECLARATION (per DoT type, as commissioned)

`d4_coverage_by_dot_type.csv`.

| DoT family | rider rows | player resist | individually resolved? | stacking rule measured? |
|---|---:|---:|---|---|
| Poison | 66 | 80 % | **NO** | NOT MEASURED |
| Bleeding | 49 | 85 % | **NO** | NOT MEASURED |
| Fire | 30 | 80 % | **NO** | NOT MEASURED |
| Life (vitality decay) | 18 | 80 % | **NO** | NOT MEASURED |
| Cold | 14 | 80 % | **NO** | NOT MEASURED |
| Physical (internal trauma) | 10 | 16 % | **NO** | NOT MEASURED |
| Lightning | 6 | 80 % | **NO** | NOT MEASURED |
| LifeLeach | 5 | 80 % | **NO** | NOT MEASURED |

**0 of 8 families individually resolved.** The commission anticipated that types might differ and
asked for what the footage offers per type. The honest answer is that the footage offers **nothing
per type**: the player HP globe is a *scalar* that sums every simultaneous effect, and no channel
in the game's rendered output decomposes it. M-1 and M-2 are properties of the **aggregate** and
are asserted only for the union.

### 4.3 Why the sibling cannot rescue the magnitude tests

`eor-test-1` corroborates *mechanism* beautifully (§ 2.2) and contains richer, calmer combat
(122 chains vs 23; rates to ~1,490 HP/s). But **the entire KC2 roster/pool decode is keyed to the
eor-test-2 fight, waves 150–160.** The sibling's board is unidentified — no wave table, no roster,
no pool basis. It can therefore support timing and shape claims and **cannot support any ceiling or
magnitude claim.** Stated so nobody later mistakes its 1,490 HP/s for a ceiling exceedance.

---

## 5 — THE RECOMMENDATION (what actually unblocks facet (i))

**Do not commission more footage.** The binding constraint is not the video.

1. **The decisive, bounded task is closing Lap I § 5.1** — the DoT magnitude convention
   (total-over-duration vs per-second). It is a *substrate* question with a named route Lap I
   already scoped and declined as out-of-lane: **write an ARC/format-string evaluator** against
   `Text_EN.arc` tooltip templates and the `.dbr` fields. If the convention resolves to **TOTAL**,
   the ceiling test in § 3.3 becomes decisive on *existing* footage (690 HP/s observed against a
   619.1 HP/s cumulative ceiling) and **strict refresh-only falsifies immediately**. If it resolves
   to PER-SECOND, the ceiling stays out of reach and facet (i) is genuinely unmeasurable here.
   *One bounded decode lap decides whether this lap's data already contains the answer.*
2. **If (1) resolves to PER-SECOND**, the only remaining honourable routes are outside this
   footage: a **controlled capture** (Matt records a low-difficulty fight where a single known
   monster applies one known DoT repeatedly, with long disengagements — the decay staircase of
   § 3.1/3.2 then works immediately and cheaply), or facet (i) ships **declared-absent**.
3. **M-1 (100 ms tick) ships now** regardless, provenance `video-measured`, two independent
   sessions. It is needed by the Godot runtime whatever the stacking rule turns out to be.

**Matt's decision (the HALT):** accept a controlled-capture request, or accept facet (i) shipping
as a declared absence in the baton with the stacking function unmodelled. Recommend firing (1)
first — it is cheap, it is substrate work, and it may make the question moot.

---

## 6 — SELF-CRITIQUE

- **The § 3.3 per-wave result is the thing to watch.** It would have been the lap's headline. I
  report it as rejected. If a reviewer thinks Crucible waves *don't* meaningfully overlap by waves
  157–160 (the player is an EoR Warlord who clears fast), the per-wave ceiling becomes defensible
  and **(b) falsifies**. I could not establish leftover-population emptiness from the footage —
  the nameplate census is a lower bound (Lap M I-3) and cannot prove absence. **This is the single
  assumption on which the verdict turns, and it is named here rather than buried.**
- **Plateau detection has a free parameter** (±12 %, ≥6 ticks). It was fixed before the ceiling test
  was run and not tuned afterward, but it was not pre-registered. Treat plateau *counts* as
  instrument-dependent; M-1 (the tick period) does not depend on it — it is measured from raw
  inter-event gaps.
- **Regen is used only as a bound**, never as a fitted constant. Every drain figure is a lower
  bound on true DoT.
- **What I did not do:** no attempt was made to track individual monster nameplate HP for
  player-applied DoTs. Judged not worth the cost — the player channels EoR (constant AoE) plus two
  summons, so no monster is ever out of contact either, and Lap M established that per-body optical
  tracking fails at this saturation. Recorded as a declined branch, not an oversight.

---

## 7 — ARTIFACTS

| file | contents |
|---|---|
| `d4_plateaus.csv` | 12 primary plateaus: t, ticks, median/min/max magnitude, span, implied HP/s |
| `d4_tick_chains.csv` | 45 primary chains, 320 ticks, per-tick gap + magnitude + basis |
| `d4_tick_period.csv` | inter-tick gap histogram (primary) |
| `d4_sibling_hp_trace.csv` | **new**: full 60 fps HP trace of eor-test-1, 149,902 frames, 110,724 read |
| `d4_sibling_tick_chains.csv` | 122 sibling chains, 1,454 ticks |
| `d4_coverage_by_dot_type.csv` | the § 4 coverage declaration |
| `evidence/d4-tick-structure.png` | EVIDENCE 1–3 (tick train · 100 ms mode · before/after scatter) |
| `evidence/d4-sibling-corroboration.png` | EVIDENCE 4–5 (sibling 100 ms mode · high-amplitude chain) |
| `evidence/roi-transfer-check.png` | ROI/font/HP-max identity across the two videos |
| `evidence/hud-strip-t776.png`, `evidence/buff-icon-row-4times.png` | the negative: no per-type or stack display in the HUD |
| `d4_ocr.py` `d4_reader.py` `d4_build_templates.py` `d4_validate.py` | the bootstrapped, validated HP reader (reusable; D-D4-1 fixed) |
| `d4_step*.py`, `d4_lib.py`, `d4_emit.py`, `d4_plot.py` | every measurement in this note, re-runnable |

---

## 8 — DIGESTS

```
eor-test-2 mp4   4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8  (full, this session)
eor-test-1 mp4   cc428e944aa385e3cd147140b6271401947a2a98390157b6b3e7df427fe01155  (full, this session)
pm4k_full_trace  bbe31eed7ed13e2f8223cdf13bb5f747b15b7fbee3da5708068276d058b786ee
pm4i_dot_riders  2dc3e380a3800b3afd14f1923d1e2a32efe9263f4ee2eaec7c69c753ed7f6ce1
pe6_wave_pools   bbdc18f12aab8e3788eac229ed1871a88ed7790dc3d1786c509cd26c076e5587
```

*Lap D-4 closed 2026-08-24 by legolas. Outcome MEASUREMENT-INSUFFICIENT → charter § 4 HALT to Matt.
Three measured by-products ship; the unblocking task is named and bounded (§ 5).*
