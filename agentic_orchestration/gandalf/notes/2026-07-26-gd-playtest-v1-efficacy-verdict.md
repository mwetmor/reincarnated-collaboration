# VERDICT — 2026-07-26 — GD play-test v1: run efficacy

**Role:** DRIFT-CRITIC (judging a delivered run against a protocol I authored — the conflict seam is
live and declared)
**Author:** gandalf-prime
**Run:** `GP-gd-2026-07-26-s1` · `/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/`
**Spec under test:** `gandalf/notes/2026-07-26-gd-general-play-run-protocol.md` §1, §1.1, §2.0–2.2
**Evidence:** `gandalf/notes/2026-07-26-gd-playtest-v1-artifact-verification.md` §§1–9.13
**Grade of everything below:** **MEASURED** (era-substrate LAW §4) — live GD oracle readings.

---

## VERDICT

> **CONDITIONAL PASS.**
>
> The artifact is sound, the controls held, and the run answers **half** of what §1 asked. The other
> half is **not extracted but is extractable from the same footage** with one bounded pass costing
> ~19,000 frames.
>
> **Do not re-record. Do not treat the run as delivered.**

| §1's question | Status |
|---|---|
| *"SHAPE of TTK … across many level-matched engagements"* | **DELIVERED** for R2; usable for R3; **insufficient for R1** |
| *"… and damage-intake"* | **NOT EXTRACTED** — 0.85% coverage. Scoped below; one pass closes it. |
| §1.1's per-kill attack cost | **NOT RECOVERABLE at this sampling rate.** See §5 — the named field covers 4.9% of kills. |
| target **100–250 engagements** | **106** — at the floor of the band, not inside it |

---

## 1. Instrument validation — PASS, by two-method closure

Full-run T-A ledger: **13,633 samples at 0.5 s**, continuous across all four parallel segment joins,
zero gaps.

| Field | Present | Non-monotonic rejections |
|---|---|---|
| `kills` | 13,357 | **0** |
| `deaths` | 13,511 | **0** |
| `play_time` | 13,427 | 3 |
| claws / charge / weaponattack / onslaught | 10,019–12,718 | 0 |
| `life_healed` | 12,913 | **413 (3.1%)** — the noisiest series |

**Every series terminates exactly on the human-read §6b totals** — 882 kills, 74 weaponattack,
54 onslaught, 358 claws, 175 charge, 12468.06 healed — reached by OCR down a fully independent path.
Two methods, one number, no shared failure mode. **That is the strongest closure available and it
passes.** Missing samples are refusals, never interpolated.

Screenshot arm (313 native reads, re-gated): **313/313, zero rejections on every core field.**

**Clock model confirmed out-of-sample.** Divergence falls **80.0 s** (358.0 → 279.5) — the §3
piecewise slope-1 model, fitted from a handful of hand-read frames, is reproduced at 13,633 points by
independent code. 12 breaks located totalling 41.0 s; **39.0 s declared as residual** below the 1.5 s
detector floor rather than attributed to invented breaks. Correct handling: sub-second transitions
are genuinely unresolvable at 2 fps against an integer-second `play_time`.

Deaths on the game clock: **`play_time` 3156 (52:36)** and **5453 (90:53)**. Clock breaks cluster at
both — dying costs wallclock the game does not count. Free cross-validation.

**Controls held.** Potions 0/0 throughout (Matt's ruling). No devotion proc anywhere in 313 stills.
No menu return. The one anomalous full-heal resolved **benign** (a loading-screen transition, §9.12).

## 2. Two corrections that change the numbers

**C-1 — the poison-DoT regime is 16× larger than reported.** It was bounded by **level 12**
(`play_time` 6816 → 12 kills → 1.5%). The DoT is **gear-gated, not level-gated** — the correction was
made in round 1 and did not survive into the regime arithmetic. Gear equip brackets to `play_time`
**6052–6282** (level 11). **True R3 = 190 kills = 21.6%.** A `WHERE play_time < 6816` filter would
leave **178 poison-DoT kills inside the pre-DoT pool.**

**C-2 — the build-identity break is 623 s earlier than §9.10 recorded.** Not `play_time` 1757. The
series shows `defaultweaponattack` climbing **one at a time** 61 → 74 between 1019 and **1134**,
`onslaught` bursting 47 → 54 by **1145**, then **11,486 consecutive samples reading exactly 74.**
Verified as a clean climb, not an OCR jump. **A spot-sampled boundary is an upper bound, not a
location** — 1757 was merely the first sample anyone checked after the freeze.

## 3. Regime partition — TWO usable distributions, not three

| Regime | `play_time` | Kills | Engagements | Kills/engagement |
|---|---|---|---|---|
| **R1** — four-skill pre-transform build | 358 → 1134 | **43** | 13 | **3.3** |
| **R2** — two-skill werewolf | 1134 → 6052 | **647** | 77 | **8.4** |
| **R3** — werewolf + poison DoT | 6052 → 7094 | **190** | 16 | **11.9** |

- **R2 is the distribution.** 647 kills over 77 engagements. This is the fixture.
- **R3 is usable with its own error bars.** 190 kills over 16 engagements — thin in engagement count,
  rich in kills, because its packs are ~3.6× the size of R1's.
- **R1 is not a distribution.** 43 kills over 13 engagements is an anecdote about the opening
  nineteen minutes. Report it; do not fit it.

**The kills/engagement progression 3.3 → 8.4 → 11.9 is itself a finding.** The build does not merely
kill faster — it engages **larger packs**. Any pooled fit across the three describes a run that never
happened.

## 4. Engagement count — at the floor, not inside the band

Segmenting on inter-kill-event gaps:

| Threshold | Engagements | Median duration |
|---|---|---|
| gap > 5 s | **106** | **4.5 s** (mean 6.1, max 37.5) |
| gap > 8 s | 75 | — |
| gap > 10 s | 67 | — |

**§1 targets 100–250.** We reach 106 **only at the most permissive defensible threshold**, and fall
below the band at any conservative one. The verdict is PASS on this criterion, but with no margin —
**v2 should target roughly double the engagements**, which at this run's density is ~2 hours of
combat-weighted play rather than 2 hours of general play.

**Resolution caveat.** A 4.5 s median engagement sampled at 0.5 s is **9 samples**; engagement TTK
carries ~11% quantization. Usable, not tight.

## 5. §1.1's structural insight PARTLY FAILS — the finding that should shape v2

§1.1: *"`skill_use_count[defaultweaponattack]` deltas between kill increments give **attacks-per-kill
with zero read uncertainty** — the exact quantity Q47 found to be 2,2,3 — across 100–250 kills."*

Two independent failures:

1. **The named field is dead for 95% of the run.** `defaultweaponattack` covers `play_time`
   358–1134: **11.5% of elapsed time and 43 of 882 kills (4.9%).** The structural insight that shaped
   the entire capture spec names an instrument measuring one-twentieth of the run.
2. **The live substitute aliases.** 514 samples carry a kill increment; **201 (39%) are multi-kill** —
   113 doubles, 38 triples, 31 quads, 12 fives, 6 sixes, one seven. At 0.5 s, attacks cannot be
   attributed to kills inside those. Attacks-per-kill survives only on the **313 single-kill events**,
   and those are **conditioned on being single-target** — the non-AoE tail, not the distribution.

**Consequence:** the run delivers **engagement-level** TTK and kills-per-engagement — which is what §1
actually asked for — and does **not** deliver per-kill attack cost. Not recoverable by reprocessing.

**Q47 status:** the original problem (a kill cost with three quanta, 42.9% spread) is **solved at the
engagement level for R2 and R3**. It is **not** solved at the per-kill level.

## 6. The one bounded pass that closes the other half

Damage-intake has exactly one instrument — the **health-globe numerals**, proven at 60 fps with 98.2%
coverage over the 58 s death window (§9.11.4). Run-wide coverage is **0.85%**.

**It does not need a full-run pass.** Restricted to the 106 engagement windows with 3 s padding:

| | |
|---|---|
| Total engagement wallclock | **1287 s = 18.9% of the run** |
| Frames at 15 fps | **19,305** |
| Frames at 60 fps | 77,220 (vs 408,991 full-run) |

**15 fps is sufficient** — the measured DoT tick period is 1.000 s, so intake events are resolved 15×
over. Digit templates already exist (`globe-digit-templates.json`). This is roughly **5× the work
already completed** on the death window, in one bounded pass.

**This is the single highest-value remaining action on the artifact, and it converts the verdict from
CONDITIONAL PASS to PASS.**

## 7. Fitness by consumer

| Consumer | Fit |
|---|---|
| **elrond** (ingestion) | **READY** for the T-A ledger + engagement segmentation. Ingest **regime-partitioned**; a pooled table is a trap. `life_healed`'s 3.1% rejection rate must ride as a column, not be smoothed. |
| **gamora** (substrate tuning) | **READY for R2 engagement-level TTK and pack-size distribution.** NOT ready for per-kill attack cost or damage-intake. Do not tune intake against 58 seconds. |
| **Q47 / ±5% tier work** | engagement-level only; see §5. |
| **galadriel** | one pass owed (§6). |

## 8. v2 requirements, ranked

1. **One dummy segment with the debug overlay OFF** (§9.11.7) — one toggle; makes the FCT census
   tractable and recovers the outgoing-DoT measurement, the only round-2 deliverable that failed.
2. **Roughly double the engagements** — combat-weighted play, not longer play. 106 is the floor.
3. **Hold the build stable, or change it deliberately and announce it.** This run's value is
   concentrated in R2 because R2 is where the build stopped moving. Regime churn is the main tax on
   sample size.
4. **Call out deaths, gear changes and zone transitions on the audio track** (§3.5's `notes.md`
   substitute) — 11 level-ups, one gear break and 12 clock breaks were all reconstructed
   archaeologically.
5. **A loading screen is a segment boundary** (§9.12.4) — no measurement stretch may span one.
6. **Every reader emits coverage** (§9.12.1) — five D-1 instances this cycle, all of them a reader
   returning a plausible value without announcing that it had guessed.
7. ≥25 Mbps remains cheap insurance; it did **not** bind here (§4).

## 9. What this verdict does NOT claim

- It does **not** claim the run is representative of GD play generally — it is one character, one
  difficulty, no potions, no devotion, levels 1–12. Those are **controls**, and controls trade
  representativeness for cleanliness deliberately.
- It does **not** certify any trial (O-8 certification is per-trial and independent of grade).
- It does **not** claim zero devotion points were assigned — only that **no devotion proc ever fired**
  (§9.11.5), which is the control that protected the oracle. The stronger claim stays UNVERIFIED.
- It does **not** resolve restore-on-load vs Constitution regen (§9.12.3) — a 30 s v2 trial settles
  it, and the DoT number stands either way.

**Signed:** gandalf, 2026-07-26.

---

## ADDENDUM 2026-07-28 — §6 pass delivered; verdict CONVERTS

The T-B intake pass (G-1) fired and reported: **19,348 frames at 15 fps over the 106 windows,
88.8% engagement-wallclock coverage** (R1 99.95% · R2 90.11% · R3 75.89%), reader closed against
the 60 fps death-window series at 97.55% agreement / ±1 HP, windows reproducing this verdict's §4
segmentation exactly before downstream work was permitted. Evidence:
`galadriel/notes/2026-07-27-gd-playtest-v1-tb-intake-findings.md` + captures
`2026-07-26-gd-playtest-v1-tb/`.

> **VERDICT CONVERTS: CONDITIONAL PASS → PASS**, with one carried condition: **R3 intake figures
> travel with a declared hole** — 4 of 16 engagements (33 kills) at zero coverage, lost to the
> gold XP-bar bloom sharing screen rows with the globe numerals; not recoverable from this footage;
> named as a v2 requirement. R1/R2 clear outright. **R2 remains the fixture** and now carries both
> halves of §1's question: TTK shape AND intake distribution.

Two ripples into consumers (§7): gamora's "do not tune intake against 58 seconds" restriction is
**lifted for R2** (tune against zero-inflated distributions — fit the tail, not the mean; 27 rare
huge hits carry 46.8% of R2 intake, largest 72.4% EHP single-frame). The restore-on-load anomaly
(§9, `play_time` 5514.87: 66 → 759 HP with `life_healed` +14.5) is **new evidence toward
restore-on-load**, still not resolved; the 30 s v2 trial stands.

**Signed:** gandalf (DRIFT-CRITIC), 2026-07-28.
