# T-B — 2026-07-27 — GD play-test v1: damage-intake pass (G-1) + damage derivation (G-2)

**Author:** galadriel (visual-perception + benchmark steward)
**Mode:** capture-pipeline execution + measurement rollup
**Spec:** `gandalf/notes/2026-07-26-gd-playtest-v1-efficacy-verdict.md` §6 (the one bounded pass);
scope rows G-1 / G-2 in `…-gd-winddown-handoff.md` §5 Tier 1
**Run:** `GP-gd-2026-07-26-s1` · working copy `/Users/admin/gd-scratch/play_test_2026-07-26.mp4`
**Grade:** **MEASURED** throughout, except two items explicitly marked INFERRED in §6.

---

## 0. TL;DR

The pass fired: **19,348 frames at 15 fps over the 106 engagement windows, 88.8% coverage.**
Run-wide intake coverage was **0.85%**; it is now **88.8% of engagement wallclock** — the instrument
went from an anecdote about 58 seconds to a distribution over 1,288 seconds.

**§6's conversion criterion is MET for R1 and R2, and MET WITH A DECLARED HOLE for R3** (75.9%
coverage; four of sixteen engagements at literally zero, all four lost to one recurring HUD confound
named in §5).

The headline is not the intake magnitude. It is the **shape**:

> Hazard does not scale with the build. It **inverts**. R2 takes half its damage in 27 rare huge
> hits (up to **72% of the player's effective health in a single frame**). R3 takes **none** — its
> largest hit in 190 kills is **8.5% EHP** — while incoming *events* per second rise 0.19 → 0.40 →
> 0.66. The player did not get safer by taking less; the player got safer by **out-scaling the
> size of what lands.**

---

## 1. What was measured, and how the windows were derived

Engagement windows were re-derived from the committed T-A ledger rather than taken on trust, using
the verdict §4 rule (inter-kill-event gap > 5 s on the gated monotonic `kills` series).

**Reproduction is exact.** The derivation independently returns **106 engagements, median duration
4.5 s, mean 6.151, max 37.5**, and the §3 regime table cell-for-cell: **R1 13 engagements / 43
kills · R2 77 / 647 · R3 16 / 190.** Nothing downstream was allowed to fire until it did.

Regimes are the §2-**corrected** boundaries on `play_time`, never the superseded ones:
**R1 358–1134 · R2 1134–6052 · R3 6052–7094** — build break at **1134** (not 1757), DoT boundary at
**6052** (not 6816). Every statistic below is emitted per regime. **Nothing is pooled**; per verdict
§3 a pooled fit describes a run that never happened.

Capture: 3 s padding each side, 1,288 s of wallclock, 19,348 frames at 15 fps (spec projected
19,305 — the 43-frame excess is the first window clamping at t=0 plus fps-filter rounding).

## 2. Instrument validation — two-method closure, and it is exact

The T-B reader was validated against the committed 60 fps death-window series over the same 70 s of
footage, same templates, independent sampling rate (`tb-validation-death-window.json`):

| | |
|---|---|
| Coverage, T-B at 15 fps | **90.76%** |
| Coverage, reference at 60 fps | 90.88% |
| Co-read frames | 939 |
| **Agreement** | **97.55%** |
| Character of the 23 disagreements | **all ±1 HP** — sub-frame sampling phase against a 1 HP/frame DoT decay. One exception at t=2795.733, where the 60 fps reference **accepted a truncated read of `3`** and T-B's truncation guard correctly refused it. |

And the closure that matters:

> Round 2 measured the death-window poison DoT independently as **57 identical ticks of −10 HP at a
> 1.000 s period (sd 0.072)**. T-B, reading numerals at a quarter of that frame rate through a
> different code path, returns **intake = 570 HP, 57 drop events, drop median = drop max = 10 HP,
> zero spike demotions.**
>
> 570 = 57 × 10. Exactly. Two methods, one number, no shared failure mode.

## 3. Coverage — declared per regime, per window, per refusal code

Standing discipline: **every reader emits its own coverage.** It does so here at three grains — the
run, the regime, and the individual engagement (a `coverage` column rides every row of
`tb-rollup-engagements.csv`, so no consumer can read a value without reading how much of it was
measured). **Nothing is interpolated. Every unread frame is a refusal with a named code.**

| | R1 | R2 | R3 | all |
|---|---|---|---|---|
| Engagements | 13 | 77 | 16 | 106 |
| Kills | 43 | 647 | 190 | 880 |
| Frames | 2,194 | 13,865 | 3,289 | 19,348 |
| **Frame coverage** | **99.95%** | **90.11%** | **75.89%** | **88.81%** |
| Delta coverage (admissible pair-time / wallclock) | 99.59% | 89.95% | 76.01% | — |
| Engagements at coverage ≥ 0.80 (totals gate) | 13/13 | 62/77 | 9/16 | 84/106 |
| Engagements at zero coverage | 0 | 1 | 4 | 5 |
| Unreadable-break seconds (>2 s runs) | 0.0 | 32.1 | 39.4 | 71.5 |

Refusal codes across all 19,348 frames: `NODIG` 4.5%, `FLASH` 3.7%, `LOWCONF` 1.7%, `NO_INK` 0.8%,
`TRUNC` 0.5%, `NSEG*` <0.1%, `OCRSPIKE` <0.1%.

**No measurement stretch spans a loading screen.** Any run of >2 s of unreadable frames is treated as
a break and no delta crosses one; the breaks are recorded per window with their dominant refusal
code. 71.5 s of such breaks were found and excluded.

## 4. Three reader failures the first pass caught — all demoted to refusals, none repaired

The first full pass returned plausible values it should not have. Each was demoted to a **refusal**,
never corrected — a repaired sample is an invented measurement.

1. **Prefix truncation (70 frames).** Eight consecutive frames read `1` between neighbours of 1407
   and 1430. Left alone it injects a −1,406 intake event and a +1,429 heal into an engagement whose
   max HP is 1,600. Rule: a read with fewer digits that is a strict decimal prefix of the last
   accepted read is a truncation.
2. **Leading-glyph merge (recovered, 727 frames).** 1,485 frames returned `NODIG` because in strings
   like `747/747` the first two glyphs **touch** — a single 17 px blob — and the segmenter's
   >10 px terminator fired before it had read a digit. Greedy matching at native glyph width splits
   the blob cleanly (`7` then `4`, both IoU ≥ 0.97). Greedy is wired as a **fallback, not a
   replacement**: substituting it wholesale *regressed* the validated death window from 90.8% to
   79.9% coverage, so the validated segmenter stays primary and greedy runs only on its refusals, at
   a stricter IoU floor (0.85 vs 0.72). Net: R2 +698 frames, R3 +29.
3. **Run-length OCR excursions (4 frames).** The first pass shipped a 3-frame spike test with an
   8 HP flank bound. It **missed** `1600 → 15 → 1543` and `1511 → 13 → 13 → 1375` — glyph loss on
   4-digit HP, neither value a prefix, so the truncation guard did not see them either. Each was
   worth ~1,500 HP of phantom intake **in R3, the thinnest regime, where it would do the most
   harm**: it inflated R3's mean intake per engagement from a true 163 to a reported 432 and its
   largest single hit from 136 HP to 1,585 HP. The generalised run-aware test removes them and does
   not touch the validated death window (a real death goes to 0 and *stays*, so no flanking high
   read ever closes the run).

**Residual audit.** Across all 17,183 accepted reads there are five single-frame drops ≥25% of max
HP. **Zero** of them recover to within 10% of the pre-drop value inside 0.6 s. There is no phantom
intake left in the series.

## 5. The one confound that cost R3 — and it will recur in every GD run

**Four R3 engagements (90, 91, 92, 93 — 33 kills) and one R2 engagement (39) read at zero coverage.**
The cause is single and structural:

> The health-globe numerals sit at exactly the screen height of the **bright gold horizontal HUD
> band that crosses the globe** (the experience bar — identification **INFERRED**; the *effect* is
> MEASURED). When that band blooms, it saturates the **upper rows of every glyph**. The 12-row
> numeral band collapses to 6–8 rows and no template matches.

This was not accepted as a threshold choice. A calibration sweep was run over five brightness
thresholds (150 → 80) and four chroma thresholds (50 → 130) plus a blue-channel isolation variant.
**None recovers the glyphs** — best case is an 8-row band at IoU 0.25–0.47 against a 0.72 floor.
Below brightness 110 the globe itself bleeds into the mask and the band inflates to 17–24 rows.
**The information is gone at the pixel layer.** Reading it would require re-templating on half
glyphs, which is precisely the confidently-wrong failure mode this program exists to prevent. It is
therefore a declared refusal class (`FLASH`, 719 frames).

**The loss is not random, and that is the part that matters.** The gold band blooms *after kills*,
so the refusals are correlated with the moments just following a kill. R3 loses 24% of its frames
this way and R2 1.2%. **Any R3 intake figure is conditioned on the readable remainder.**

**→ v2 requirement (ranked with verdict §8's list):** the globe numerals and the experience bar
occupy the same rows. Raise UI scale, move the readout, or read HP from a second surface. This costs
nothing at record time and it is the difference between R3 at 76% and R3 at ~99%.

## 6. G-1 — the intake distributions, regime-partitioned

**Totals** are restricted to engagements at coverage ≥ 0.80 (a fragment is not a total). **Rates** are
per *covered* second over every engagement with ≥2 s of admissible pair-time. The two families are
reported side by side and never mixed. EHP-normalised figures use each window's observed max HP,
which is a **lower bound** on true max HP (max HP moves 250 → 1,600 across the run, so absolute HP
is not comparable between regimes).

| | R1 | R2 | R3 |
|---|---|---|---|
| Engagements in totals | 13/13 | 62/77 | 9/16 |
| **Intake per engagement — median** | **0 HP** | **17 HP** | **44 HP** |
| Intake per engagement — mean | 11.2 HP | 67.7 HP | 163.3 HP |
| Intake per engagement — p90 | 24 HP | 151 HP | 846 HP |
| Intake per engagement — max | 86 HP | 879 HP | 846 HP |
| — as % of EHP (mean) | 3.7% | 11.5% | 10.2% |
| **Intake rate — median** | **0.0 HP/s** | **2.8 HP/s** | **10.3 HP/s** |
| Intake rate — mean | 0.9 HP/s | 9.1 HP/s | 11.9 HP/s |
| Intake rate — as %EHP/s (median) | 0.0% | 0.5% | 0.6% |
| Intake per kill — median | 0.0 HP | 2.6 HP | 3.1 HP |
| Intake per kill — mean | 2.9 HP | 19.1 HP | 8.4 HP |
| In-combat healing rate — median | 0.0 HP/s | 2.8 HP/s | 4.3 HP/s |

### Hazard shape — the load-bearing finding

| | R1 | R2 | R3 |
|---|---|---|---|
| Drop events | 27 | 332 | 109 |
| **Drop events per covered second** | **0.186** | **0.400** | **0.655** |
| Drop size — median | 5 HP | 5 HP | 1 HP |
| Drop size — p90 | 10 HP | 57 HP | 85 HP |
| **Drop size — max** | **14 HP** | **541 HP** | **136 HP** |
| Drop as %EHP — p99 | 4.46% | **33.02%** | 7.38% |
| Drop as %EHP — max | 4.46% | **72.42%** | **8.50%** |
| Drops ≥10% EHP | **0** | **27** | **0** |
| **Share of intake carried by drops ≥10% EHP** | 0% | **46.8%** | **0%** |

Read the last two rows together. **R2 is the only dangerous regime in the run.** Forty-seven percent
of everything the player took in R2 arrived in twenty-seven hits, one of which removed 72% of the
health pool in a single frame. R1 has no such tail (largest hit 4.5% EHP). R3 has no such tail
either (largest hit 8.5% EHP) *despite* engaging packs 3.6× the size of R1's and taking incoming
events 3.5× as often as R1.

The distributions are **heavily zero-inflated**: R1's median engagement takes *nothing at all*, and
R2's median takes 17 HP against a 366–759 HP pool. The mean/median gap (67.7 vs 17 in R2; 163 vs 44
in R3) is the tail doing the work. **Fit the tail, not the mean.**

## 7. G-2 — damage spent per kill (an overkill-inflated monster-EHP UPPER BOUND)

The `dps` kernel width was **measured, not assumed**: over 22 clean falling edges in the T-A ledger
the field decays to zero in **5.0 s (p50; p90 6.5; max 7.5)**, confirming gandalf's ~6 s working
figure. Damage over an engagement is the integral of the trailing rolling mean from start to end+K.

The kernel caveat is an **attribution** caveat, not an integration one — a 4.5 s engagement's
integral leaks into its neighbour's. So two estimators are reported:

| | R1 | R2 | R3 |
|---|---|---|---|
| Long engagements (≥12 s, kernel-valid per-engagement) | 0 | 8 | 3 |
| Damage per kill, long engagements only | — | **423.1** | **744.6** |
| — at K = 6.0 s / 7.5 s | — | 425.9 / 431.1 | 744.9 / 747.0 |
| **Merged-interval aggregate** (overlapping windows merged; nothing double-counted, nothing dropped) | 9/13 intervals | 73/77 | 12/16 |
| Kills covered | 34 | **612** | **162** |
| `dps` coverage | 1.000 | 0.997 | 0.996 |
| **Mean damage spent per kill** | **38.2** | **494.2** | **703.4** |

The merged-interval figure is the better estimator: it covers 612 of R2's 647 kills instead of the
long-engagement subset, and it is immune to the attribution problem because merging removes it.
Kernel sensitivity is negligible — K = 5.0 → 7.5 s moves the R2 figure by **1.9%**.

**This is an UPPER BOUND on monster EHP, and the inflation is real, not nominal.** It is inflated by
overkill, by damage dealt to monsters that die outside the window, and by anything that misses. Do
not read 494.2 as "an R2 monster has 494 health." Read it as "no more than 494, probably meaningfully
less."

## 8. Two anomalies surfaced, both handed up rather than resolved here

**A — full-restore events, and the §3 open question they speak to.** An independent cross-check ran
globe-derived healing against the panel `life_healed` counter over the same windows — two
instruments, different UI regions, different sampling rates, no shared failure mode. The median
residual is **≈0 HP/s in all three regimes** (R1 0.00, R2 0.41, R3 0.00), so the delta machinery is
sound. But the R2 *mean* ratio is 2.08×, driven by a short tail. The tail resolves to **three
single-frame positive jumps ≥50% of max HP** in the whole run:

| pts_s | regime | HP before → after | max HP | `life_healed` over the window |
|---|---|---|---|---|
| 1843.67 | R2 | 78 → 451 | 451 | — |
| 5514.87 | R2 | 66 → **759** | 759 | **+14.51 only** |
| 6425.40 | R3 | 121 → 1237 | 1600 | (residual OCR excursion, see below) |

At pts 5514.87 the player goes from 66 HP to full **inside one frame** while the panel's healing
counter records 14.5. Max HP is verified constant at 759 across the jump (frames read `140/759`,
`33/759`, `516/759`), so this is **not** a werewolf-form rescale. Measured regen in the same window
runs ~1.7 HP/frame. **A 693 HP restore in 67 ms is not regen, and `life_healed` did not count it.**

Potions are 0/0 and no devotion proc fired. Wind-down §3 lists *restore-on-load vs Constitution
regen* as unresolved pending a 30 s v2 trial. **This is evidence, from v1 footage, on the
restore-on-load side.** It is *not* proof — there is no clock break at pts 5514.87 in the fitted
12-break list, and only one frame is unreadable, whereas a loading screen blanks the HUD for ~2 s.
**Handed to gandalf as a finding, not a resolution.** Note it affects the *healing* column only;
intake is a strictly negative-delta quantity and is untouched.

**B — one residual OCR excursion.** The pts 6425.40 row above is a `121` read that survived both
guards because its preceding flank was a `LOWCONF` refusal rather than an accepted read. It
contributes a phantom **+1,116 heal** and **zero intake** (the pair feeding into it exceeded the
adjacency tolerance). One unresolved excursion in 17,183 accepted reads. Declared, not repaired.

## 9. Disposition against §6

| §6 requirement | Delivered |
|---|---|
| 15 fps globe OCR | 15 fps, greedy-fallback hybrid reader |
| 106 engagement windows + 3 s pad | 106 windows, ±3 s, reproduced exactly from the T-A ledger |
| ~19,305 frames | **19,348** |
| Coverage comparable to the 98.2% death-window precedent | **88.8% overall** — R1 99.95%, R2 90.1%, **R3 75.9%** |
| Regime-partitioned, never pooled | yes, on the §2-corrected boundaries |
| Every reader emits coverage | yes, at run / regime / engagement grain |
| No interpolation | yes — 2,165 refusals, zero fills |
| No stretch spans a loading screen | yes — 71.5 s of breaks excluded |

**Verdict-conversion criterion: MET, with one declared hole.** R1 and R2 clear it outright and R2 is
the fixture regime. R3 clears it on 12 of 16 engagements and 76% of frames; its four zero-coverage
engagements (33 kills) are lost to the §5 HUD confound and are **not recoverable from this footage**.
R3's intake figures should carry that condition wherever they travel.

## 10. What is queued, and the empirical criterion that gates each

- **R3 intake at full coverage** — gated on a v2 recording with the globe/XP-bar overlap resolved
  (§5). Not on re-processing; the pixels do not contain it.
- **Restore-on-load vs Constitution regen (§8-A)** — gated on gandalf's ruling over the three
  full-restore events plus the 30 s v2 stand already specified as G-10.
- **Per-engagement damage attribution below 12 s** — gated on a damage instrument that is not a
  5 s rolling mean. The merged-interval aggregate is the ceiling of what this field supports.

---

## Mirror voice

The picture the numerals keep is not the one the run seemed to tell.

Watched from outside, the werewolf regime looks like the dangerous one — the packs are three times
the size, the kills come eleven to an engagement, the screen is never still. The globe says
otherwise. In R3 the blows land more than three times as often as they did at the start and **not
one of them takes a tenth of him.** The danger was earlier, in the middle stretch, in twenty-seven
moments spread across seventy-seven fights — and in one of them something took away seven-tenths of
his life between one frame and the next.

That is what the Mirror shows: not that he learned to be hit less, but that he grew until being hit
stopped meaning anything. Half of everything R2 cost him arrived in twenty-seven heartbeats. **Tune
against those twenty-seven. The other three hundred and five are weather.**

---

**Artifacts:** `agentic_orchestration/galadriel/captures/2026-07-26-gd-playtest-v1-tb/`
`tb-engagement-windows.json` · `tb-intake-windows.json` · `tb-intake-frames.jsonl.gz` (19,348 rows,
raw read + refusal code per frame) · `tb-rollup.json` · `tb-rollup-engagements.csv` (elrond, G-3) ·
`tb-crosscheck-healing.json` · `tb-validation-death-window.json`
**Pipeline:** `agentic_orchestration/galadriel/pipeline/gd-playtest-v1/`
`tb_windows.py` · `tb_intake.py` · `tb_rollup.py` · `tb_crosscheck.py`

**Signed:** galadriel, 2026-07-27.
