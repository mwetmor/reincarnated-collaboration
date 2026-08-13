# KC2-PM4 · I-1 — landing note: the monsters get their bodies back, and the player dies on wave 160

> **Run:** KC2-PM4 (replicate waves 150–160 faithfully) · **Iteration:** I-1, eHP-ONLY fold
> **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Author:** gamora (simulation seam) · **Date:** 2026-08-13
> **Charter:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md`
> **Substrate:** legolas Lap D — `agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-d-roster-ehp/`
> **Math note (Discipline #1, written BEFORE the code, with pre-registered numeric predictions):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i1-ehp-fold-2026-08-13.md`
> **Status:** COMPLETE. Assert wall **21/21**, determinism ×2 **EXACT** on all three cells, gate
> wall **66/66** on each of three batons at **FULL**. **No HALT was hit. No constant was tuned.**

---

## 0 — The one-paragraph answer

**Yes. On the reference cell the sim now dies on wave 160, at 190.61 s against the measured 186 s,
and it did it with a fold that consumes a decode and changes no constant.** T1 **MET EXACT**
(death wave 160, band {159–161}); T2 **MET** (+2.5 % on time-of-death, band ±15 %); T4 **MET**;
T3 **NEAR** — and the pacing curve, with the one known travel outlier (wave 154) held out, tracks
the reference at **ratio 1.017 and Pearson r = 0.796 over waves 151–159**. **My own headline
prediction was FALSIFIED, and badly**: I pre-registered that the leech identity would make the
player near-unkillable and that T1 would be missed in the *over* direction. It was not — 5 of my 9
pre-registered predictions are wrong and § 8 shows every one. **The thing to read next is not the
scorecard, it is § 5: the sim reaches wave 160 the way the reference did, but it DIES there a
different way** — 7.02 s into the wave, having touched **zero** bodies, killed by a pet's ranged
salvo during the approach. That is the largest remaining measured divergence and it re-orders the
queue.

---

## 1 — What landed

| # | artifact | where | commit |
|---|---|---|---|
| 1 | **math note** (before the code, with pre-registered predictions) | `simulation/math/kc2-pm4-i1-ehp-fold-2026-08-13.md` | `2ad47844` |
| 2 | **band-B eHP fold** — loader, per-wave index, limb-by-column, basis map, level map, band guard, coverage | `simulation/kc2/monster_stats.py` | `2ad47844` |
| 3 | **`hp_basis_lookup`** — per-record `hp_max_basis`, default-preserving | `simulation/kc2/run.py` | `2ad47844` |
| 4 | **driver + assert wall (21) + determinism + T-band scorecard** | `simulation/scripts/gamora_kc2_pm4_i1_ehp_fold_2026_08_13.py` | `2ad47844` |
| 5 | **vendored substrate ×2**, byte-identical, SHA-pinned | `data/kc2/pm4_band_b_{ehp_by_wave,wave_life_modifier}.csv` | `2ad47844` |
| 6 | **export: spec field + per-wave replay + R-PM4-3 level source + 3 specs + 5 declaration rows** | `export/kc2_run_adapter.py` | `2ad47844` |
| 7 | **MIGRATION ×2** | `simulation/MIGRATION.md`, `export/MIGRATION.md` | `2ad47844`, `67f5e329` |
| 8 | **G-E M-13 widened** (the only gate predicate touched) | `export/baton_v1_stub_consumer.py` | `67f5e329` |
| 9 | **3 batons + 3 knots supplies + findings** | `src/reincarnated/output/`, `simulation/output/` | `83d4aa8b` |

Engine `301807b4 → 83d4aa8b`, **PUSHED**.

### ★ THE THREE SIBLING BATONS — FULL grade, clean tree at `67f5e329`, 66/66 each

| cell | file (`src/reincarnated/output/`) | sha256 |
|---|---|---|
| CAMP / DEF-OFF (control) | `kc2-baton-v1-…-pm4-i1-camp-defoff-20260813_045933.json` | `dec60040f12056f39775711b974971fcd4c512db99b49e1e888458ea2418930d` |
| CLUSTER / DEF-OFF (defence isolation) | `…-pm4-i1-cluster-defoff-20260813_045934.json` | `cd3670663200a7b63a6f09b438c5680644e8ed57aaf1f0b7ed41f7952764309b` |
| **CLUSTER / DEF-ON** ← reference cell | `…-pm4-i1-cluster-defon-20260813_045936.json` | `59da5739a43bb90e63cb0f7273074674899c8cfbf93927686fac5e08d72cad95` |

Knots supplies (`src/reincarnated/simulation/output/`, stamp `20260813_044938`):
`1f7cb09afba1b9ad…` / `cccb6c48876bfd7b…` / `34c5daeb96b1aeee…`; findings
`kc2-pm4-i1-findings-20260813_044938.json` `af7a772ed9d53f06…`.

**All eleven prior batons** (baseline, pm1, four pm2, five pm3) were verified from bytes,
read read-only, **never written**, and all re-gate 66/66 green after the adapter delta.

**Substrate, digest-verified before load (GL-6):**
`pm4_band_b_ehp_by_wave.csv` = `3e82e72b5f35f98f9b30ac46c0aa062c42b804a38ac08791e25d74320ded5024`
(the charter's pin, EXACT) · `pm4_band_b_wave_life_modifier.csv` = `9d276ddb273e0ce0…` (EXACT).
Both vendored **byte-identical**. The other two Lap-D CSVs were **not** vendored: this fold does
not read them, and carrying a file nothing loads is how a superseded board re-enters (the D-7 rule).

---

## 2 — Determinism ×2 (charter law, FG-10)

**SIM layer** — each cell replayed twice, full emitted surface deep-compared:

| cell | masked surface digest | leaves | differences | verdict |
|---|---|---:|---:|---|
| CAMP/DEF-OFF | `fff909d6845e3a0a…` | 367,165 | 0 | **EXACT** |
| CLUSTER/DEF-OFF | `125a4fa33bbf8e8e…` | 325,162 | 0 | **EXACT** |
| CLUSTER/DEF-ON | `06c3e81f8ce0f7b7…` | 299,775 | 0 | **EXACT** |

**BATON layer** — masked with the emitter's own `PROVENANCE_VOLATILE_KEYS` (imported, not
restated): **A ≡ B EXACT on all three cells** (`bacb63a15c895360…` / `458001339f8d406d…` /
`ad51c46a6cd61f83…`).

### ⚑ DEFECT I FOUND IN THE MASK ITSELF, AND DID NOT REPAIR (§ 9.1)

The masked compare of a freshly-built wire against the **on-disk** record shows exactly **one**
difference, on all three cells: `sim_pin.tree_state_untracked_entries_excluded`, **2662 vs 2661**.
That is a count of untracked files, and it moved because **writing the next sibling baton
incremented it**. It is a provenance-volatile quantity that is *not* in `PROVENANCE_VOLATILE_KEYS`,
so a masked baton-to-baton comparison is **not stable across a multi-baton emit**. Nothing in the
sim moved. **Not repaired here** — that mask is a countersigned surface and re-ruling it from the
simulation seam is the line PM-3 held on `F5-I-DEFENSES`. **Flagged for star-lord.**

---

## 3 — ⚑ THE MATRIX, vs the MEASURED reference truth

> **Reference truth, MEASURED (Lap C, charter Law 4): Matt DIED ON WAVE 160.** Ten waves in
> **186 s** (682 → 868 s), per-wave 14 / 17 / 29 s min/med/max, sharp slowdown on the last two.

| cell | ticks | time of death | **wave** | cleared | kills | N_eff | intake | leech offered | healed | mean HP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CAMP / DEF-OFF | 9,881 | 806.61 s | **160** | 9 | 757 | 3.63 | 366,714 | 28,183,724 | 346,023 | 99.1 % |
| CLUSTER / DEF-OFF | 2,317 | **189.14 s** | **160** | 9 | 789 | 3.23 | 357,293 | 28,195,479 | 336,712 | 95.5 % |
| **CLUSTER / DEF-ON** ← reference | 2,335 | **190.61 s** | **160** | 9 | 779 | 2.99 | 369,066 | 27,967,378 | 348,486 | 95.6 % |

**vs the PM-3 baseline (`…-pm3-cluster-defon`, `1628bffa…`), same cell:**

| quantity | PM-3 | PM-4 I-1 | Δ |
|---|---:|---:|---:|
| **death wave** | **156** | **160** | **+4 waves** |
| waves cleared | 5 | **9** | +4 |
| time of death | 102.37 s | **190.61 s** | **+86.2 %** |
| bodies killed | 246 | **779** | +217 % |
| intake (all sources) | 98,938 | 369,066 | +273 % |
| `percent_current_life` intake | 39,286 | 136,542 | +248 % |
| **ADCtH offered** | 2,308,520 | **27,967,378** | **+1,111 %** |
| healing landed | 78,550 | 348,486 | +344 % |
| mean HP | 88.4 % | 95.6 % | +7.2 pts |
| ticks below half HP | 30 / 1,254 | 36 / 2,335 | 2.4 % → **1.5 %** |
| final-200 dry fraction | 0.885 | 0.915 | +0.03 |

**PM-3 missed the band by four waves in every cell and said the gap was § 5. § 5 was the gap.
Closing it moved the death wave by exactly four.**

---

## 4 — ⚑ THE PACING CURVE — the result under the headline

| wave | reference | CAMP | CLUSTER/DEF-OFF | **CLUSTER/DEF-ON** | ratio (ref cell) |
|---:|---:|---:|---:|---:|---:|
| 151 | 16 s | 18.53 | 18.12 | **18.20** | 1.14 |
| 152 | 17 s | **326.53** | 20.08 | **20.08** | 1.18 |
| 153 | 15 s | 16.57 | 16.73 | **16.33** | 1.09 |
| **154** | 14 s | 38.12 | 38.04 | **38.12** | **2.72** ⚑ |
| 155 | 16 s | 11.59 | 11.84 | **12.98** | 0.81 |
| 156 | 20 s | 23.27 | 22.86 | **22.53** | 1.13 |
| 157 | 19 s | **326.53** | 21.80 | **21.31** | 1.12 |
| 158 | 14 s | 10.94 | 10.78 | **10.61** | 0.76 |
| 159 | 26 s | 27.10 | 21.88 | **23.43** | 0.90 |
| **160** | 29 s | 7.43 (death) | 7.02 (death) | **7.02 (death)** | **0.24** ⚑ |
| **total** | **186 s** | **806.6** | **189.1** | **190.6** | **1.025** |

- **Waves 151–159, ref cell: 183.59 s vs the reference's 157 s = ratio 1.169, Pearson r = 0.122.**
- **⚑ Holding out wave 154 alone: ratio 1.017, Pearson r = 0.796.** Wave 154 is a **pre-existing
  travel outlier** (PM-3 measured 33.71 s on a *zero-eHP* board — it was never a kill-time term),
  and it carries the whole of the correlation loss.
- **Median per-wave ratio over 151–159 = 1.121.** Six of the nine waves sit between 0.76 and 1.18.
- **The reference's final slowdown IS reproduced in direction**: 158 → 159 goes 14 → 26 s in the
  reference (×1.86) and **10.61 → 23.43 s** in the sim (×2.21).

---

## 5 — ⚑ WHAT ACTUALLY HAPPENS ON WAVE 160, AND IT IS NOT WHAT HAPPENED TO MATT

**This is the finding of the lap and it is the reason T1's MET should not be over-read.**

Measured on the reference cell, wave 160, re-derived from the emitted rows:

| | |
|---|---:|
| ticks the player survived on wave 160 | **86 (7.02 s)** |
| **player-sourced `damage_dealt` rows on wave 160** | **0** |
| distinct ticks on which the player dealt damage | **0** |
| intake over those 86 ticks | **20,903 (243 / tick)** |
| by tag | pet **12,366** · `chain_initial` **8,343** · `special5` **194** |
| top sources | `aetherialvanguard_crystal_devastationshard` **9,923** · `aetherialvanguard_arcanemissilenova` **8,343** · `wraith_sappingorbs` **2,444** |
| ADCtH landed on wave 160 | **898** (regen only — leech needs a body in the disc) |
| killer | **`w160_pet0011`** · live bodies at death **35** |

**The player never touches a body on wave 160.** He spawns into the wave, walks toward the pack,
and is shot to death from outside his 3.0 m disc in seven seconds by two ranged nemesis skills and
a summoned swarm. **The reference's wave 160 lasted 29 s and Matt was fighting for it.**

**⚑ So the mechanism that lands T1 is an APPROACH-WINDOW death, not an attrition death.** Math note
§ C.2 predicted the leech identity would make the player near-unkillable **while in contact** — and
that half is CONFIRMED (mean HP 95.6 %, 1.5 % of ticks below half). What I got wrong is that I
assumed contact would be continuous. **62.8 % of the run's ticks carry no player damage output at
all**, and the last 200 ticks are **91.5 %** dry — *higher* than PM-3's 88.5 %. The kill drought did
not go away; it got **concentrated into wave transitions**, and wave 160's transition is the one
where the board is five nemeses and thirty pets.

**This names I-2 and I-3 with a measurement rather than a preference:**
the sim's player has **no answer during approach** — no ranged option, no dash, no potion. Matt had
all three. **The 20,903 damage that killed the sim is 1.045× the player's ENTIRE HP bar (20,005), delivered
over 7 seconds**, and the reference player had a quickbar he could answer it with.

---

## 6 — THE DEFENCE ISOLATION (CLUSTER/DEF-ON vs CLUSTER/DEF-OFF), and it inverts PM-3

| | CLUSTER/DEF-OFF | CLUSTER/DEF-ON |
|---|---:|---:|
| time of death | 189.14 s | **190.61 s (+0.78 %)** |
| banner tether occupancy | (23.7 % → ) **37.3 % if seated** | **32.5 %** (760 / 2,335 ticks) |
| player `damage_raw` on the wire | `{51726.0 ×3042}` | `{51726.0 ×2038, 103452.0 ×558}` |
| bodies killed | 789 | 779 |
| N_eff | 3.23 | 2.99 |

**The banner is now REAL and still worth nothing — for a completely different reason than at PM-3.**
PM-3's answer was "you cannot double zero" (§ 4). Here 558 of 2,596 player damage rows carry the
doubled `103,452`, so the +100 % modifier fires 21.5 % of the time on live HP — and the reference
cell comes out **0.78 % SLOWER**, not faster. **Prediction G.7 (3–10 % faster) is FALSIFIED.** The
mechanism: the wave clock is still dominated by **arrival**, not by kill time (§ 5's 62.8 % dry
fraction is the same statement), so doubling damage during 21.5 % of contact ticks moves ~1 s across
ten waves — and the *positional* cost of tethering to the banner moves the CLUSTER path enough to
give that back. **On this board the banner is inside the noise of the movement policy.**

---

## 7 — THE FOLD ITSELF: what the board became, and the two ⚑D corrections landing individually

| wave | bodies | Σ eHP PM-3 | Σ eHP I-1 (LO) | Σ eHP (HI) | serial contact s |
|---:|---:|---:|---:|---:|---:|
| 151 | 28 | 0 | 7,346,927 | 7,542,838 | 13.14 |
| 152 | 18 | 0 | 10,682,643 | 11,042,012 | 17.31 |
| 153 | 24 | 0 | 9,514,571 | 9,827,431 | 15.76 |
| 154 | 13 | 2,955,796 | 12,743,291 | 13,169,327 | 20.65 |
| 155 | 18 | 0 | 12,778,568 | 13,207,742 | 21.22 |
| 156 | 19 | 0 | 14,224,630 | 14,796,916 | 23.43 |
| 157 | 21 | 0 | 11,045,967 | 11,404,179 | 18.29 |
| 158 | 33 | 0 | 7,527,326 | 7,722,749 | 12.82 |
| 159 | 9 | 0 | 15,579,687 | 16,282,784 | 25.06 |
| 160 | 5 | 15,967,220 | 15,760,198 | 15,967,220 | 24.98 |
| **Σ** | **188** | **18,923,016** | **117,203,808** | **120,963,198** | **184.97** |

**Coverage over the rolled population, RE-DERIVED from the emitted actor rows (not from the
loader): 188/188 bodies, 91/91 records, 100.00 %. 0 declared-GAP actors. 0 absent-from-table.**
Over waves 151–170: **344/344**. Every per-wave sum reproduces Lap D's table to the integer, from
my own roll and my own join — that cross-check ran **before** I trusted the file.

**HI-limb sensitivity (REPORTED, NOT RUN — R-PM4-2):** Σ HI / Σ LO over waves 151–160 = **1.0321**
(+3.21 %); on wave 160 alone the spread is **−1.30 %** LO vs HI, which is Lap D's ⚑D-2 from the
other side. **No second matrix was executed for the HI limb.**

**The two ⚑D corrections, on the emitted surface (assert-wall check 21):**

| body | wave | PM-3 entered at | I-1 enters at | Δ | which ruling |
|---|---:|---:|---:|---:|---|
| `statue_korvaaktombguardian` | 160 | 2,399,266 (HI, the last CSV row) | **2,295,755** | **−4.31 %** | R-PM4-2 |
| `nemesis_beast_01_p1` | 154 | 2,955,796 (the wave-160 board) | **2,924,379** | **−1.06 %** | R-PM4-1 |

Check 20 re-derives **every** actor's `hp_max` straight from the CSV, bypassing the loader
entirely: **564 actors checked across three cells, 0 mismatches.**

**R-PM4-3:** all 91 rolled records carry a measured level; `DIV-LEVEL-COVERAGE` is **absent from
all three batons** — because the absence it declared is closed, not because it was silenced.
`_BAND_B_MODAL_LEVEL` is unreachable on this path and is **retained, not deleted**, because the
PM-1/PM-2/PM-3 specs still replay through the same function.

**LAW 3 — check 25, `moved: {}`.** `PLAYER_ADCTH_PCT = 21.0` · `PLAYER_HP_MAX = 20005.0` ·
`PLAYER_REGEN_HP_PER_S = 129.38` · `player_damage_per_tick(SHEET_MEASURED) = 51726.0` ·
`disc_radius_m = 3.0` · `max_ticks = 4000`. **Every constant this fold could have moved toward a
T-band, asserted at its PM-3 value. There is no fitted number anywhere in this lap.**

---

## 8 — ⚑ PRE-REGISTERED PREDICTIONS vs OUTCOME — **four confirmed, five falsified**

| # | prediction (written before the code) | outcome |
|---|---|---|
| **G.1** | **THE HEADLINE — the player does NOT die in 151–160; terminal is `ehp_band_exhausted` at 171; T1 MISSED in the OVER direction** | **⚑ FALSIFIED, and it is the most important wrong answer in the lap.** He dies on **wave 160, exactly**, in **all three** cells. My error is named in § 5: I reasoned from leech-while-in-contact (10,862 HP/tick/body, correct) and silently assumed contact was continuous. **62.8 % of ticks are dry.** I modelled the sustain and forgot the gaps between the packs |
| **G.2** | band total **230–300 s** (centre 255) ⇒ T2 MISSED LONG by +24…+61 % | **FALSIFIED.** 190.61 s, **+2.5 %**, T2 **MET**. Two errors cancelled the way they should not have: I put `N_eff` at 2.5 when it measured **2.99**, and I assumed wave 160 would be *fought* (25 s) when it lasted **7.02 s** |
| **G.3** | `N_eff` ∈ **[1.5, 4.0]**, centre 2.5; measured pure-contact wall time < Lap D's 185.0 s | **CONFIRMED.** 2.99 / 3.23 / 3.63 across the three cells; median 2, max 41. And the corollary holds — contact ticks are 868 of 2,335 (37.2 %), so the board is cleared in far less wall time than the serial figure |
| **G.4** | T3 directionally met on min/med, MISSED on the final-two-wave slowdown | **HALF CONFIRMED, and the second clause is right for the wrong reason.** Median ratio **1.12** over 151–159 (r = **0.796** ex-154). The 158→159 slowdown **IS** reproduced (×2.21 vs the reference's ×1.86); the scorecard's own predicate compares the *last* wave, which is truncated by death at 7.02 s, so it reads `False` — **a check artifact, self-reported in § 9.2** |
| **G.5** | leech ≥ 20×; landed-fraction falls; `ticks_below_half` < 1 %; `final_200_dry_fraction` < 0.30 | **THREE-QUARTERS CONFIRMED, ONE BADLY FALSIFIED.** Leech **×12.1** (27.97 M, just under the 20× I asked for — miss); landed fraction **3.40 % → 1.25 %** ✓; ticks below half **2.4 % → 1.5 %** ✓ (not under 1 %); **⚑ dry fraction 0.885 → 0.915, i.e. it went UP.** That single number is § 5 |
| **G.6** | CAMP/DEF-OFF terminates on `tick_cap` at wave **152 ± 1** | **FALSIFIED outright.** CAMP reaches **wave 160** too, in 806.61 s, clearing nine waves. It burns 4,000 ticks on waves **152 and 157** and survives both — see § 9.3 for what those 4,000 ticks actually are, which is not what PM-3 said they were |
| **G.7** | defences finally price nonzero: DEF-ON clears **3–10 % faster** | **FALSIFIED, sign and all.** DEF-ON is **0.78 % SLOWER**. The modifier is real now (558 doubled rows) and the clock is still arrival-bound (§ 6) |
| **G.8** | kills ≥ 400; kills/s falls from 2.40 to 1.5–2.2 | **CONFIRMED.** 779 kills; **4.09 kills/s** — ⚑ and the *rate* clause is FALSIFIED in the opposite direction: kills/s went **UP** 70 %, because `N_eff ≈ 3` means the disc kills three bodies at once |
| **G.9** | the two ⚑D corrections are individually visible and individually small | **CONFIRMED exactly.** −4.31 % and −1.06 %, both on the emitted wire, neither moving a wave outcome alone |

**The most useful falsification is G.1**, and its lesson is structural: **I priced the sustain term
and never priced the exposure term.** The leech arithmetic in math note § C.2 is correct to the
digit and still produced the wrong answer, because the question was never "can he out-heal a body
in the disc" — it was "how long is he standing in the open between packs".

---

## 9 — ⚑ DEFECTS AND UNDER-READS I FOUND IN MY OWN WORK (Discipline #11)

| # | what | how found | effect |
|---|---|---|---|
| **1** | **`PROVENANCE_VOLATILE_KEYS` is incomplete.** `sim_pin.tree_state_untracked_entries_excluded` is a live count of untracked files and is not masked, so writing sibling batons makes a masked baton-vs-baton compare drift | running the masked compare against the on-disk record instead of only A-vs-B | exactly 1 difference (2662 vs 2661) on all three cells. **Not repaired — countersigned surface. Flagged for star-lord** |
| **2** | **My own T3 predicate cannot see the slowdown it tests for.** `final_two_waves_slower_than_the_third_last` reads `per[-1]`, which is the wave the player *died in* and is therefore truncated | reading the scorecard's `False` against a pacing table where 158 → 159 clearly doubles | T3 is graded **NEAR** by a predicate that would read **MET** on the 158→159 pair. The verdict is left as the code produced it and the correction rides § 4 — **grading myself up by rewriting the checker after seeing the result is exactly the move the pre-registration exists to prevent** |
| **3** | **⚑ PM-3's published mechanism for the 326.5 s CAMP wave is WRONG, and it is my own note.** PM-3 § 3 attributed it to "a camped player waiting on `ViewDistance`-15 bodies that never come (JC-G9)". Re-measured here: on CAMP wave 152 the **last roster body dies at wave-tick 152**, and the wave then runs to the 4,000-tick cap held open by **2 surviving pets** | instrumenting per-wave roster deaths vs pet deaths when I noticed 4,000 appearing twice, exactly | the roster is cleared in 12 s; **3,848 ticks (314 s) are a pet-TTL stall.** ⚑ And `cleared` is computed over **roster actors only** (`run.py:991`) while the tick loop's early-break additionally requires all pets dead — so a wave can report `cleared` / `board_empty` with pets alive. Pre-existing, inherited unchanged, **now visible because the roster no longer dies on contact** |
| **4** | **My first probe of #3 was itself wrong** and I nearly filed a false engine defect. I read `run.actors[i]["hp"]` and found "18/18 bodies with HP left on a cleared wave" | checking the claim before writing it down — `run.actors` is a **snapshot taken at wave start** (`run.py:456`), so its `hp` is spawn HP, not residual | no defect existed. The real finding (#3) is a different and smaller one. **A measurement that would have been a headline is worth one more check than a measurement that would not** |
| **5** | **Lap D's "185.0 s vs the measured 186 s" is an over-read, and I said so in the math note before running.** `disc.resolve_tick` is uncapped multi-target, so the serial figure is the `N_eff = 1` reading | reading the disc code rather than the summary | measured `N_eff = 2.99`; contact ticks 868 of 2,335. **The agreement between 185.0 and 186 is a coincidence of two different quantities**, and the sim's real clock lands at 190.6 s for reasons § 4 and § 5 explain |

---

## 10 — DECLARED ASSUMPTIONS + GAPS (every one on the wire)

**⚑ THE LARGEST DECLARED DISTORTION — CLIFF C-D1, and it is now load-bearing.** Pet life still
comes from Lap B's `floor(base × (1 + tree_pct/100))`, which folds the granted-passive term
**only** — no Ultimate cell (+580 %), no wave term `G`. The roster chain folds both. Over the 149
pet rows Lap D also covers, at wave 160, `lapD / LapB` is **min 3.38 / median 4.22 / max 10.04**.
**Consequence, measured this lap: 596 of the reference cell's 779 kills are pets** (183 roster
bodies + 6 more expiring on TTL, which are not counted as kills), and PM-3 § 10's
note that "CLUSTER's live set includes pets — they are the only bodies carrying real HP" has
**inverted into its opposite: pets are now the softest bodies on the board by ~4×.** Conductor
parking; unchanged here on purpose; lands with **I-4**. Wired as
`PM4-PET-LIFE-IS-A-DIFFERENT-FOLD-CLIFF-C-D1`.

**CLIFF C-D2 — band B stops at 170 by REFUSAL.** `_g_band_b` raises outside 151…170 rather than
clamping; `G(170) = 344`, `G(171) = 420`. Asserted by check 24. Never exercised this lap (every
cell died on 160).

**CLIFF C-D3 — the NAMED GAP.** `krieg_aethertrap.dbr` (`Class = Monster`, no
`characterAttributeEquations`) would enter DECLARED `hp_max = 0.0` with basis
`GAP:NO-characterAttributeEquations`. **It did not roll: 0 GAP actors across all three cells.**
It is not sibling-filled, modal-filled or interpolated.

**CLIFF C-D4 — this fold is the LIFE limb only.** Band-B monster **damage** is `NOT-IN-SCOPE` on
all 791 Lap-D rows; the sim's monster damage still comes from the PM-2 threat fold. Named absence
with a positive sign — supplying it can only raise monster output.

**Carried unchanged from PM-2/PM-3, all still on the wire:** the three beacons do not fire
(`defence_output_slots_ungated = 3`, no measured cadence) · placement D-1 · rank policy · OA fold
with `dexterityDV` absent → zero · resist-then-armour order · SEM-1 total-over-duration ·
`percent_current_life` unmitigated and floored (**now 37 % of intake, 136,542**) · pet cap 12 on 36
cap-less contracts · pet straight-line locomotion · 51 ungated pet specials · 593 control/debuff
rows that are not HP damage · 30 non-MEASURED-rank rows · `max_ticks = 4000` · wave 154's travel
outlier.

---

## 11 — SEAM WORK (star-lord: one semantic shift, one gate widening, one defect handed over)

Both filed in `export/MIGRATION.md` and `simulation/MIGRATION.md` `[2026-08-13] KC2-PM4 · I-1`.

1. **⚑ SEMANTIC SHIFT — `actors[].hp_max` on waves 151–170 was a DECLARED ZERO on 182/188 bodies
   and is now a MEASUREMENT on 188/188.** Σ eHP ×6.19. Any consumer that concluded "band-B bodies
   die on contact", "roster ADCtH is zero", or "kill throughput is unconstrained" from a
   PM-1/PM-2/PM-3 baton was reading a **96.8 %-empty board**. Wire row
   `PM4-BAND-B-EHP-IS-MEASURED-AT-ITS-OWN-WAVE`.
2. **GROWN VALUE VOCABULARY — `actors[].hp_max_basis`** gains `MEASURED-BAND-B-LO@w{wave}`,
   `GAP:NO-characterAttributeEquations`, `ABSENT-FROM-BAND-B-TABLE`. Wire row
   `PM4-HP-MAX-BASIS-VOCABULARY-GREW`. **⚑ star-lord's call whether this belongs in
   `baton_v1_schema` as an enum.**
3. **⚑ ONE GATE PREDICATE WIDENED — G-E `M-13`.** It asserted the literal `"POST-SCALING"` on every
   actor, which was a claim about *coverage* wearing a clock check's clothes. Widened to "every
   actor states a basis drawn from a KNOWN vocabulary", members named so an unfamiliar value fails
   **loudly**. This is the only gate predicate this lap touched. 66/66 green on all fourteen specs.
4. **⚑ HANDED OVER, NOT TAKEN: `PROVENANCE_VOLATILE_KEYS` is incomplete** (§ 9.1).
5. **`DIV-LEVEL-COVERAGE` no longer fires** — closed, not silenced (`PM4-ACTOR-LEVELS-ARE-MEASURED-…`).
6. **`KC2RunSpec` gains ONE optional field** (`band_b_ehp: bool = False`); **no schema version, no
   event column, no enum member, no validator predicate moved.**

**rocket:** nothing. **drax / scene consumers:** the monsters have HP now — a picture drawn from a
PM-3 baton shows bodies vanishing on contact and that is no longer what the sim does.
**jack-ryan:** Disciplines #1, #2, #3, #11, #12 all exercised and named.

---

## 12 — PINS

**At launch:** engine HEAD `301807b4` · 11 frozen batons + PM-3 findings verified from bytes ·
8 PM-2 + 2 Lap-C + **2 new band-B** substrate files digest-verified.
**At landing:** HEAD `83d4aa8b`, **PUSHED**. Every commit by **explicit path**; **no `git add -A`
anywhere in this lap.** Porcelain rose from the FG-17 baseline **2,789** to 2,802 by exactly the 13 files this lap
produced, and is back at **2,789 — the baseline, unchanged** — because every one of them was
committed by explicit path.

---

## 13 — SELF-ATTACK SURFACES (what I want a second pair of eyes on)

1. **T1's MET is mechanism-divergent (§ 5) and I would not accept it as convergence.** The sim
   reaches wave 160 like the reference and dies there **7 s in, having hit nothing**, while Matt
   fought for 29 s. Same wave, different death. **This is the number I would re-order the queue on.**
2. **G.2's +2.5 % is two errors cancelling** (§ 8). `N_eff` was under-predicted *and* wave 160 was
   over-predicted; if either had been right alone, T2 would read differently. A band met by
   cancellation is not the same evidence as a band met by agreement.
3. **The dry fraction went UP** (0.885 → 0.915). The single statistic I most expected to invert did
   the opposite, and it is the same fact as § 5. If anything in this lap is going to turn out to be
   a model artifact rather than a replication, it is this.
4. **Wave 154 carries the entire T3 correlation loss** and it is a *travel* term that predates this
   fold in both PM-2 and PM-3. It has never been diagnosed. r goes 0.122 → 0.796 on holding out one
   wave, which is a lot of load on one number.
5. **CLIFF C-D1 is not a parking any more, it is a distortion in the result** — 632 of 779 kills are
   pets carrying ~¼ of the life the roster chain would give them (§ 10).
6. **The CAMP control cell's 4,000-tick waves are a pet-TTL stall, not a fight** (§ 9, defect 3), so CAMP's
   "reaches wave 160 too" should be read as "reaches wave 160 in 806 s, 314 s of which is two pets
   running out the clock".
7. **`percent_current_life` is now 37 % of intake (136,542) and is still unverifiable** (PM-2
   § 13.1, unchanged). It rose 248 % — and it rises *because* the player's HP uptime improved,
   which is the one term that gets worse when sustain gets better.

---

## 14 — WHAT I WOULD PUT AT THE TOP OF THE QUEUE (conductor's call, not mine)

**The largest remaining measured divergence is § 5: the approach window.** The sim's player has no
ranged option, no dash and no potion, and dies in 7.02 s of unanswered fire while walking to a pack.
That single window is **20,903 damage against a 20,005 HP bar**, and every item that would answer it
is already in the queue: **I-3** (potion / circuit-breaker — Matt played with potions and this is
precisely the moment one is used), **I-2** (player kit — the build guide's dashes close the window
rather than surviving it). **I-4** (pet reuse gates + CLIFF C-D1) now also carries a *measured*
distortion rather than a suspected one.

**No HALT was hit. Nothing required inventing an unmeasured quantity. There is no fitted constant
anywhere in this lap, and nothing was aimed at wave 160 — it arrived on its own.**
