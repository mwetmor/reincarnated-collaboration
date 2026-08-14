# KC2-PM4 · I-11 — landing note: **the like-for-like moved. After three iterations frozen to the bit, T2 is IN BAND — and the crit bracket that was supposed to decide it turned out not to matter.**

> **Run:** KC2-PM4 · **Iteration:** I-11, THE PLAYER-OFFENSE FOLD · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** gamora (simulation seam) · **Date:** 2026-08-14
> **Fired under:** ruling **R-PM4-27** (charter ledger **L-21**), pre-authorized at **R-PM4-24** (L-20)
> on my own § 11.1 structural finding.
> **Math note (Discipline #1, written and committed BEFORE the code — commit `f39b6d0e`, its own
> commit, so the git order is the proof):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i11-player-offense-2026-08-14.md`
> **Judged against:** the **L-19 RE-DERIVED BANDS** and I-10's pinned batons.
> **Status:** COMPLETE. **No HALT.** ⚑ **No cell of record designated — by design (§ 3).**

> ### ⚑ NOTE-9 — THE BASIS FOR EVERY NUMBER IN THIS NOTE
> | class | source | sha256 (FULL, GL-6) |
> |---|---|---|
> | every **I-11** quantity | `simulation/output/kc2-pm4-i11-findings-20260814_052659.json` | **`d39ac09f06cff1dbaa43e412ebeaa0488920fc5497b0bcb0706eec81edf314de`** |
> | every **I-10** quantity | `simulation/output/kc2-pm4-i10-findings-20260814_035800.json` | `44bdeeac5d81fd3618bdbd6fe1b9186c42612bed6b197b810ad8bba1df4a6b6d` |
> | the **player's offense** | `data/kc2/pm4l_mitigation_by_body.csv` (legolas Lap L, imported unmodified) | `a8c1ffd97dc703419f8447f3d7bbba3903e0f14d2c2e6746a938ceefae9ecec6` |
> | the **chain control** | `data/kc2/pm4l_applied_damage_by_body.csv` | `5a41ad7d8a9757782c2f54e7ea018bb8ade2bc81c57b64f3774dd9e42d9cee67` |
> | the **measured death** | `data/kc2/pm4k_death_anchor.csv` (Lap K) | `999347db3e1b5caa69809abf8d56d1c7212d67321ae8c80e87abd2e71d584a6e` |
> | the **wave spans** | `data/kc2/pm4k_segments.csv` | `a1b03c319db32d81cbcbae6efe5b584f01a8069b4af3514b8a886d1ac0b80785` |
>
> All five Lap-L digests and all three Lap-K digests are **verified from bytes at run time by the
> driver**; a wrong digest HALTs the lap. **There is no unsourced number below.**

---

## 0 — The one-paragraph answer

**The term was the term.** I-10 § 11.1 proved that `PLAYER_DAMAGE_LIMB` — a constant selected at
I-1 and unexamined for ten iterations — was the sole determinant of T2 and T3, and that nothing on
the monster side could move them. Replacing it with Lap L's measured composition chain moved them
both, immediately: **the like-for-like went from `223.265306122449 s` — a number frozen to the
floating-point bit across I-8, I-9 and I-10 — to `193.796 s`, INSIDE the T2 band `[155.31, 210.12]`
for the first time in the run's history.** T3's mean absolute error fell **7.076 → 4.947 s** and its
median ratio went **1.1152 → 0.9400**; eight of ten waves moved closer to the measured span. T4a's
mean HP moved **0.9840 → 0.9635** toward the video's 0.932. T4b(a) produced, for the first time, an
excursion matching the measured shape (**20.57 s at floor 0.279, survived, full recovery** — the
referent's is 7.42 s at 0.292; the phenomenon exists and now over-shoots). A cell **died** for the
first time since I-7. ⚑ **And the crit bracket, which the math note's arithmetic predicted would
DIVERGE on T2 and force a route, produced IDENTICAL verdicts on all five judged quantities** — so
D-L5 costs this run nothing and carries as a named gap rather than a HALT. The magnitude never
moved: raw stayed `51,726.0` on both sides of the fold. What moved is that a correct number finally
passed through the board's own armour and resistance. **T1 still misses** (the reference cell walls
out at 171), the w160 span is still only **0.720×** the measured, and w154 is still **2.700×** — and
§ 11 names what is left.

---

## 1 — WHAT LANDED

| # | artifact | where | commit |
|---|---|---|---|
| 1 | **math note** (before the code; 17 predictions, 22-check wall, the immunity consequence and the crit-divergence prediction both banked pre-run) | `simulation/math/kc2-pm4-i11-player-offense-2026-08-14.md` | **`f39b6d0e`** |
| 2 | `kc2/player_offense.py` — **NEW MODULE**: the chain, the three limb enums, the Bresenham accumulator, the positive control | new module | `adacd009` |
| 3 | `kc2/run.py` — one additive nullable keyword; the per-body chain at both damage sites; the re-stated clear predicate | modified (ADDITIVE; the default IS I-10) | `adacd009` |
| 4 | `data/kc2/pm4l_*.csv` ×5 — Lap L's emissions, imported UNMODIFIED | new substrate | `adacd009` |
| 5 | **MIGRATION ×2** | `simulation/MIGRATION.md`, `export/MIGRATION.md` | `adacd009` |
| 6 | `export/kc2_run_adapter.py` — six spec fields | modified | `adacd009` |
| 7 | **driver + 22-check wall + determinism ×2 + 8 sensitivity cells** | `simulation/scripts/gamora_kc2_pm4_i11_player_offense_2026_08_14.py` | `adacd009` |
| 8 | **6 knot supplies + findings** | `simulation/output/` | `b42569f0` |
| 9 | **6 baton specs** (`_i11_spec`, built not copy-pasted) | `export/kc2_run_adapter.py` | `ce88685d` |
| 10 | ⚑ **6 BATONS**, FULL 67/67 each | `src/reincarnated/output/` | `7b021ab7` |

### Artifacts of record — ⚑ FULL 64 hex, never truncated (GL-6)

| what | sha256 |
|---|---|
| **findings** | `d39ac09f06cff1dbaa43e412ebeaa0488920fc5497b0bcb0706eec81edf314de` |
| knots camp/DEF-OFF **critLO** | `c649fdd6e091ef7754ca0dd306f250c4f8e22fa0fcaae2a6f89831cf9e3fce7d` |
| knots cluster/DEF-OFF **critLO** | `6a309a8a6673229b806f6e5c4d8dfd3c78fe0c729ff71a998075dbaf8cf4410a` |
| knots cluster/DEF-ON **critLO** ← reference | `4aaf960434a9c328145407550f89fd7f0ac0256517c019c87b492976d7eedfaf` |
| knots camp/DEF-OFF **critHI** | `80cdf7077ac32f22698da957279aca41740d42dc21cd36de3b60d114d7c934b7` |
| knots cluster/DEF-OFF **critHI** | `e6f98faf656e4c41f75b4ed35816bd7dd2c831b5a787083bff3bdf2d5add9dfb` |
| knots cluster/DEF-ON **critHI** | `2298049bcd41b03a022fb201ceb7f72fb9c8cdb94e23238bcd64ca8e1128d01a` |
| **baton** camp/DEF-OFF **critLO** | `fda674a89558eae41b979b25f29770f4a3fb001ade32988709c2716a752453bf` |
| **baton** cluster/DEF-OFF **critLO** | `6d861543a15b93482870c04fab35749c6eb27f5cbcae801785eb26d399f71d0c` |
| **baton** cluster/DEF-ON **critLO** ← reference | `8b5df91b5befadfe88ff188609fe418e5c53e42fbe943025b19fdf92b134f487` |
| **baton** camp/DEF-OFF **critHI** | `bdba55c6a915f74bc194a2bf94fa5198b483e0f5c0a6f1a8c97e7f060fb043c6` |
| **baton** cluster/DEF-OFF **critHI** | `7e0965adf1e01cc18b68f709e77dd2eba831dffd4639b5df3b546b0ef1f05478` |
| **baton** cluster/DEF-ON **critHI** | `17da204a0570503e02de668f879f1a4206c34e7ce52c94d58dfd071036a8bc4c` |
| determinism surface cluster/DEF-ON **critLO** | `cea41eef6fb50eb90621b4b706f4117d38a0929b2bc2ef357601c52b851f7808` |
| determinism surface cluster/DEF-ON **critHI** | `e18a798307b88052cdf845da7e709ed7ef02e783d33125e41904e1005bb93f9c` |

All six batons emitted **FULL, 67/67 green** (VALIDATOR 33/33 · G-STATS 1/1 · G-E 33/33) on a clean
tree. **The I-10 batons these SUPERSEDE:** `0489f5924eff1b92c63503ab976bb2e4d88ed53f5ef9bd61d1122f6b2b21ed97`
/ `759d4881ce02c2d57afa38fc2854c9cc83a75fc32994dec7ff905b8bf9682a63` /
`5a9a183d590444b306da4e67e6415a2f1ccf82ac05134f71620bfd5d6c325f46`.

### 1.1 — ⚑ THE FOLD-OFF ARM IS BYTE-EXACT, AND THE BATON LAYER IS EXACT UNDER THE ONLY MASK THAT IS HONEST

| layer | arm | declared (math note § 7) | measured |
|---|---|---|---|
| **1a** | I-10 config at I-11 HEAD with `player_offense` **ABSENT** | byte-EXACT vs I-10 ×3 | **EXACT ×3** — `7d05fc81…3351` / `faaf70e5…9516` / `8255e8d8…e91a` |
| **1b** | pre-I-6 arm (jacobi4, offense off, band-C off, φ=HASH, I-8 kit limbs) | byte-EXACT vs I-5, **six folds back** | **EXACT ×3** — `5f616040…7fa7` / `0ad5b297…2605` / `95a34b2e…c7a4` |
| **1c** | ABSENT-not-None: the legacy arm never passes `player_offense` at all | wire EMPTY on every wave | **EMPTY ×3** |
| **1d** | **baton layer** — re-emit the three I-10 specs at I-11 HEAD and diff against the committed I-10 batons | leaf-exact **except** the provenance leaves D-I10-1 proved unsatisfiable | ⚑ **4 differing leaves per baton, ALL FOUR provenance**: `_emitted_at`, `baton_run_id` (a fresh UUID), `sim_pin.engine_version_full`, `sim_pin.engine_version_sha`. **ZERO content leaves differ, on all three.** |
| **1e** | the twelve I-11 cells | divergent BY CONSTRUCTION (declared pre-run) | divergent, as declared |

> **⚑ 1d is how D-I10-1 gets dispatched properly.** At I-10 the baton-identity check was
> "unsatisfiable across commits by construction" and was closed by an **out-of-band masked
> execution**. Here it is closed by a **masked diff of the committed artifacts** — which is
> strictly better, because it names the four leaves that differ instead of asserting that some
> unspecified set of them was allowed to. The check is now reproducible from the repository alone.

---

## 2 — ⚑ THE FOLD, AND THE SENTENCE THAT MATTERS MOST

```
raw_physical_per_tick  =  (43,691 + 59,761)/2  =  51,726.0        [DETERMINISTIC, no per-hit RNG]
after_armor(b)         =  raw ≤ armor_b ? raw×0.30 : armor_b×0.30 + (raw − armor_b)
applied(b)             =  after_armor(b) × max(0, 1 − res_physical_b/100)     [immunity clamp]
expected(b)            =  applied(b) × hit(1.0) × crit(1.0 | 1.5)
```

> ### ⚑ THE RAW MAGNITUDE DID NOT MOVE BY ONE FLOAT. `51,726.0` BEFORE, `51,726.0` AFTER.
> The limb I was commissioned to replace was already carrying the correct measured number. **The
> fold is not a magnitude change; it is the discovery that a correct magnitude was being applied to
> a board it had never been made to pass through.** Under the flat limb, `damage_raw` on a player
> row took **one** value for a whole run. Measured at the reference cell it now takes **132
> distinct values**, spanning **0.0 … 103,452.0** with median **38,285.25**.

**Three of the six commissioned properties were already in the model, and the math note said so
before the code** (§ 3 of the note, the same audit I-10 § 2 ran on its own commission):

| commissioned | state pre-I-11 | disposition |
|---|---|---|
| hit = 1.0 everywhere | the disc has **no to-hit branch at all** | POSITIVE CONTROL |
| multiplicity UNCAPPED | `disc.resolve_tick` has never had a cap, arc test or truncation | POSITIVE CONTROL |
| radius 3.0 m | `EOR_RADIUS_M = 3.0` | POSITIVE CONTROL |
| cadence 0.081633 s | `TICK_S = 1/12.25 = 0.0816326530612244898` | **IDENTITY**, measured 1.0 hits/tick exactly |
| armour law + per-body resist | **ABSENT** | **THE FOLD** |
| crit multiplier | **ABSENT** (fixed 1.0 by omission) | **THE FOLD**, bracketed, no record end |

**And the commission's framing correction, banked pre-run and now measured:** density-linear
multiplicity was *always* true. What the flat limb never had is **composition-dependence** — with
one constant against a board of varying armour and resistance, *which* bodies are in the ring could
not matter. It matters now, and § 5 is what that bought.

**Chain positive control:** my `applied()` reproduces **all 79,240 rows** of Lap L's
`pm4l_applied_damage_by_body.csv`, **0 mismatches**, worst |Δ| = **0.005** — exactly half of Lap L's
own 2-dp rounding unit, on every row. The sim runs Lap L's chain, and that is a measurement rather
than a claim about my reading comprehension.

---

## 3 — ⚑ D-L5: THE BRACKET DOES NOT DIVERGE, SO THE ROLL RULE COSTS THIS RUN NOTHING

R-PM4-27 part 3 pre-registered the decision rule and the math note § 6.3 pre-registered my
prediction — **in arithmetic, before the code existed** — that the bracket would **DIVERGE on T2**
(critLO 272.97 s OUT / critHI 185.51 s IN) and force a route.

**Measured, at the reference cell, on all five judged quantities:**

| judged quantity | critLO (×1.0) | critHI (×1.5) | |
|---|---|---|---|
| T1 (death in {159–161}) | False | False | **agree** |
| T2 (l4l in band) | **True** | **True** | **agree** |
| T3 (w160 inverted vs own mid-median) | False | False | **agree** |
| T4a (alive while clearing) | True | True | **agree** |
| T4b(c) (instant kill fires) | False | False | **agree** |

> ### ⚑ VERDICT: **IDENTICAL. D-L5 IS IMMATERIAL TO THIS RUN AND CARRIES AS A NAMED GAP.**
> No route is required, no floating-combat-text decode is needed to land I-11, and **no cell of
> record was designated** — `record_cell: null` rides every one of the twelve artifacts, and
> assert-wall check 22 enforces it. The two columns differ by **0.327 s** on a 193-second
> like-for-like (`193.796` vs `193.469`), which is **0.17 %**.
>
> ⚑ **My prediction of divergence is FALSIFIED, and the reason is worth more than the prediction
> was.** I priced the crit multiplier as if it acted alone. It does not: a 50 % damage increase
> makes bodies die faster, which *empties the ring faster*, which removes exactly the parallelism
> that made them die faster. **The uncapped density-linear disc is a negative-feedback loop, and it
> ate a flat 50 % on the run's single most load-bearing term.** That is the same mechanism that ate
> my span predictions (§ 6), and it is the iteration's most transferable finding.

---

## 4 — ⚑ T-SCORECARD vs THE L-19 RE-DERIVED BANDS (reference cell, BOTH columns)

| band | L-19 target | **I-11 critLO** | **I-11 critHI** | I-10 | verdict |
|---|---|---|---|---|---|
| **T1** | death on wave **160**, acceptance {159–161} | `arena_tier_exhausted`@171 | @171 | @171 | **MISSED** — but ⚑ **a cell dies** (§ 7) |
| **T2** | l4l **182.7167 s**, band **[155.31, 210.12]** | ⚑ **193.7959** | ⚑ **193.4694** | 223.2653 | ⚑ **MET, BOTH ENDS — the run's first** |
| **T3** | the ten measured spans | median ratio **0.9400**, MAE **4.947 s**, 10/10 scored | 0.9378, MAE 5.500 s | 1.1152, MAE 7.0756 s | **NEAR — materially improved** |
| **T4a** | alive while clearing, mean → 0.932 | **0.963471** | 0.965403 | 0.984048 | **MET**, moved toward |
| **T4b (a)** | SURVIVED excursion, floor ≈0.29, ~7.4 s, full recovery | ⚑ **1 match** (20.571 s @ 0.2791, w154, recovered) | 1 match (19.102 s @ 0.2451) | **0 matches** | ⚑ **MET on shape, OVERSHOOTS on duration** |
| **T4b (b)** | full-health dwell ~1.6 s | no death at this cell → not evaluable | not evaluable | not evaluable | **UNEVALUABLE** |
| **T4b (c)** | instant kill hp≥0.95 → 0 in ≤1 tick on w160 | **DID NOT FIRE** (0 of 14 fold-ON cells) | did not fire | did not fire | **MISSED** |

**Depth:** min HP intra-tick **0.24508** at the reference cell — **below the referent's measured
floor 0.291877** — with 15 survived excursions below 0.70, 8 below 0.50, 3 below 0.33, 1 below 0.25.
I-10's reference floor was 0.3512.

---

## 5 — ⚑ THE WAVE-SPAN TABLE, SIM vs MEASURED, AND THE SHAPE IT BOUGHT

| wave | **measured (L-19)** | I-10 | **I-11 critLO** | **I-11 critHI** | I-10 ÷ meas | **I-11 ÷ meas** |
|---:|---:|---:|---:|---:|---:|---:|
| 151 | 16.27 | 18.37 | **18.286** | 19.102 | 1.129 | **1.124** |
| 152 | 16.25 | 23.10 | **15.592** | 12.653 | 1.422 | **0.959** |
| 153 | 14.75 | 16.24 | **16.327** | 17.143 | 1.101 | 1.107 |
| 154 | 14.12 | 40.73 | **38.122** | 38.122 | 2.885 | **2.700** |
| 155 | 16.32 | 13.31 | **15.020** | 11.918 | 0.816 | **0.920** |
| 156 | 20.20 | 24.08 | **23.184** | 23.102 | 1.192 | **1.148** |
| 157 | 18.85 | 33.06 | **15.510** | 15.755 | 1.754 | **0.823** |
| 158 | 13.10 | 10.94 | **11.020** | 10.367 | 0.835 | **0.841** |
| 159 | 26.30 | 27.10 | **22.041** | 27.347 | 1.030 | 0.838 |
| 160 | 25.95 | 16.33 | **18.694** | 17.959 | 0.629 | **0.720** |
| **l4l** | **182.72** | **223.27** | ⚑ **193.796** | ⚑ **193.469** | 1.222 | **1.061** |

**Eight of ten waves moved CLOSER to the measured span.** Two moved away (153 by 0.006, 159 by
0.132). The biggest single repair is **w157: 1.754 → 0.823**.

### 5.1 — ⚑ THE FINAL-TWO-WAVE SLOWDOWN EXISTS IN THE SIM FOR THE FIRST TIME

The referent's signature is that its last two waves are its **slowest**. Slowdown against each
fight's *own* mid-wave median:

| | w159 | w160 |
|---|---:|---:|
| **measured** | **1.618** | **1.596** |
| I-10 sim | 1.307 | ⚑ **0.787** — *the player cleared w160 faster than the man who died on it took to die* |
| **I-11 critLO** | **1.381** | ⚑ **1.171** |
| **I-11 critHI** | **1.663** | **1.092** |

> ⚑ **THE INVERSION IS GONE.** I-10's headline shape miss was that the sim's wave 160 was its
> *fastest recent wave*. It is now its slower-than-median wave at both bracket ends, and at critHI
> w159 reproduces the measured slowdown to within 3 %. **The mechanism is exactly the one the fold
> introduced:** w160's bodies carry median armour **1,834** against the mid-wave board's **915–991**,
> so composition-dependence prices them as the harder wave they actually are. `⚑ rank_reordering_vs_I10`
> measures **6 of 10 waves changed rank** — under a flat limb the span ordering is a pure function
> of Σ eHP and could not have.
>
> **What is NOT fixed:** in absolute terms w160 is still only **0.720×** the measured span, and
> **w154 is still 2.700×** — the single largest residual on the board, essentially unmoved from
> I-10's 2.885×. § 11 names what w154 is.

---

## 6 — THE SIX MATRIX CELLS AND THE EIGHT SENSITIVITY CELLS

| cell | terminal | l4l 151–160 | mean HP | min HP | T3 MAE | shape-match | zero-damage rows |
|---|---|---:|---:|---:|---:|---:|---|
| camp/DEF-OFF **critLO** | ⚑ **player_death@154** | 83.755 | 0.8854 | **0.0000** | 7.187 | 0 | 1,650 / 3,657 |
| cluster/DEF-OFF critLO | @171 | **208.980** | 0.9722 | 0.2643 | **3.915** | 1 | 6,642 / 22,378 |
| **cluster/DEF-ON critLO** ← ref | @171 | **193.796** | 0.9635 | 0.2451 | 4.947 | 1 | 6,128 / 18,975 |
| camp/DEF-OFF critHI | @171 | 185.306 | 0.9581 | 0.1012 | 6.022 | 1 | 3,945 / 13,174 |
| cluster/DEF-OFF critHI | @171 | 193.388 | 0.9633 | 0.1186 | 5.592 | 0 | 6,401 / 16,675 |
| **cluster/DEF-ON critHI** | @171 | 193.469 | 0.9654 | 0.2451 | 5.500 | 1 | 5,981 / 15,281 |

⚑ **Every one of the six l4l values except the dead cell's lands inside `[155.31, 210.12]`.**

| sensitivity cell | terminal | l4l | mean HP | min HP |
|---|---|---:|---:|---:|
| `S-RAW-LO` (43,691) | @171 | 195.184 | 0.965053 | 0.2313 |
| `S-RAW-HI` (59,761) | @165 | 193.714 | 0.938667 | 0.2451 |
| `S-RAW-LO-CH` | @165 | 193.878 | 0.936177 | 0.2560 |
| `S-RAW-HI-CH` | @171 | 185.061 | 0.970760 | 0.2602 |
| `S-CADENCE-LO` | ⚑ **player_death@156** | 104.898 | 0.847286 | **0.0000** |
| `S-CADENCE-LO-CH` | @165 | 198.286 | 0.946622 | 0.3350 |
| `S-IMMUNE-GATES` | ⚑ **@152 (§ 8)** | 18.286 | 0.999206 | 0.9488 |
| `S-BANNER-ADD` | @171 | **206.204** | 0.964013 | 0.2135 |

> ### ⚑ THE RANGE-END BRACKET DOES NOT SPAN EITHER, AND FOR THE SAME REASON AS THE CRIT BRACKET.
> `S-RAW-LO` = **195.184** and `S-RAW-HI` = **193.714**: a **37 % swing in the player's raw damage
> moves the like-for-like by 0.75 %.** The same negative feedback (§ 3). **Under R-PM4-27 part 2's
> own test — "if the deterministic-expectation form materially diverges from its range ends, route"
> — it does NOT diverge: all four range-end cells land inside the T2 band with the expectation
> cell. The delivery form is vindicated by measurement, not by argument.**

---

## 7 — ⚑ SOMETHING DIED, AND IT WAS KILLED BY A PET

`camp_defoff__critlo` — **`player_death` at wave 154**, run tick 1026, t = 35.3469 s into the wave,
**killer `w154_pet0042`**, 9 live bodies on the board. `S-CADENCE-LO` also dies, at **wave 156**.
**Two of the fourteen fold-ON cells die; the last death anywhere in this run was at I-7.**

**T1 is still MISSED** — the target is wave **160** {159–161}, the reference cell walls out at 171,
and neither death is in the acceptance window. But the model has stopped being unable to kill the
player, and the mechanism is the fold's: **longer correct clears buy the monsters more time.** The
camp policy, which does not walk to the density centroid, has no counterplay against a wave whose
bodies now take 30 % longer to remove.

⚑ **And it is a PET that lands the kill.** The pet arm has carried 40 % of intake since I-9's
`pet_share_of_intake = 0.4096`; this is the first lap in which it converts.

---

## 8 — ⚑ THE IMMUNITY CONSEQUENCE, MEASURED — AND THE LITERAL READING IS *DEGENERATE*, NOT MERELY SLOW

The math note § 4 banked, before the code: eleven pet records carry MEASURED physical immunity
(`defensivePhysical = 500`), three with `ttl_s = None`, reachable on waves 152 / 154 / 157. Two
measurements from the run:

**(a) A third of the player's hits land on things he cannot kill.** At the reference cell,
**6,128 of 18,975** player `damage_dealt` rows carry `damage_raw = 0.0` — **32.3 %**. The disc is
uncapped, so every immortal ground hazard inside the 3 m ring absorbs a hit slot every tick. That is
not a rounding artefact; it is a third of the weapon's output, and it exists only because the sim
models **one** damage stream (gap `D-I11-1`).

**(b) `S-IMMUNE-GATES` — the literal predicate — does NOT time out. It walks off the arena.**

```
terminal: arena_tier_exhausted @ wave 152, t = 18.286 s
detail:   simulate_wave(152) raised PlayerDriveInvariantError:
          player is 80.322 m from the arena centroid, past the declared sane bound 80.0 m.
          The CLUSTER policy ran away; the bound is not tight.
```

> ### ⚑ THIS IS A BETTER FINDING THAN THE TIMEOUT I PREDICTED.
> I pre-registered (P.10) that the literal predicate would burn `max_ticks` and end
> `wave_not_cleared:timeout` at ~348 s. **The wave is right; the mechanism is wrong, and the real
> mechanism is worse.** With immortal hazards on the board the wave cannot end, so the CLUSTER
> player keeps seeking a density centroid that is now **defined by the things he cannot kill** — and
> he is dragged off the map in 18 seconds. The literal reading does not merely make the fight long;
> it makes the player's own targeting policy incoherent. **The Discipline-#12 amendment in § 4.2 of
> the math note is not a convenience; the unamended model is degenerate on this board.**

---

## 9 — MATCH GATES: ⚑ THE BLOCK MOVES FOR THE FIRST TIME SINCE I-7, AND ONE GATE FLIPS TO MET

| gate | I-9 | I-10 | **I-11 critLO** | video target | verdict |
|---|---:|---:|---:|---:|---|
| **MG-1** ring median | 0 | 0 | ⚑ **1** | **1** | ⚑ **MET — first time** |
| **MG-2** ring p90 | 4 | 4 | **5** | 3 | MISSED (moved away) |
| **MG-3** ring max | 17 | 17 | **27** | 10 | MISSED (moved away) |
| **MG-4** moving fraction | 0.84114 | 0.84114 | **0.67669** | 0.883 | MISSED (moved away) |
| **MG-6** longest stationary | MET | MET | **MET** | ≤ 1.40 s | MET |
| **MG-7** dash rate | MET | MET | **MET** | 5.3235 s | MET |

At I-10 this entire block was **byte-identical to I-9** — "the gates measure geometry and movement;
a phase fold touches neither." **A player-damage fold touches both**, because it changes how long
bodies live and therefore how many are standing in the ring. MG-1 reaching its target is the first
match gate this run has converted. MG-2/3/4 moved **away**: bodies living ~30 % longer means a
fuller ring (max 17 → 27) and a player who spends more time in contact and less in transit
(0.841 → 0.677). **Both directions are the same mechanism, reported together.**

---

## 10 — PRE-REGISTERED PREDICTIONS vs OUTCOME

Falsified predictions keep their original wording (the run's standing practice).
**Seven confirmed · five split · four falsified.**

| # | prediction | outcome |
|---|---|---|
| **P.1** | realised spans within **[0.85, 1.05]×** the § 6.2 table on ≥ 8 of 10 waves | **⚑ FALSIFIED — 4/10 (critLO), 0/10 (critHI).** Realised l4l is **0.710×** my prediction. I priced the density feedback at 5–15 %; it is **29 %** (§ 3) |
| **P.2** | **T2 DIVERGES**: critLO ∈ [232, 287] MISSED; critHI ∈ [158, 195] MET | **SPLIT.** critHI **CONFIRMED to the number** (193.469 ∈ [158,195], MET) · critLO **FALSIFIED** (193.796, MET, far below my band) · **the divergence claim is FALSIFIED** — and that is § 3 |
| **P.3** | T1 MISSED at both ends; `arena_tier_exhausted`@171 on ≥ 5 of 6 cells; death probability ≈30 % at critLO, ≈5 % at critHI | **CONFIRMED — exactly 5 of 6 @171**, and the sixth is the death my 30 % clause anticipated |
| **P.4** | T3 shape NOT repaired; w160 ratio < 1.0 both ends; w154 > 2.0 both ends; MAE ≈5.8 critHI / ≈10.6 critLO | **SPLIT.** w160 **0.720 / 0.692** (< 1.0 ✓, and my 0.818/0.551 brackets it) · w154 **2.700 / 2.700** ✓ · **MAE FALSIFIED at critLO — 4.947, an IMPROVEMENT where I predicted 10.6** · ⚑ and the *inversion* limb is falsified: w160 is no longer inverted vs its own mid-median (§ 5.1) |
| **P.5** | T4a MET both ends, moving in OPPOSITE directions: critLO ∈ [0.972, 0.982], critHI ∈ [0.985, 0.991] | **SPLIT.** MET ✓ · **both bands FALSIFIED (0.9635 / 0.9654)** and **both moved TOWARD 0.932**, not in opposite directions |
| **P.6** | T4b(a) MISSED at both ends; dwell critLO ∈ [3.8, 5.4] s, critHI ∈ [2.6, 3.6] s; floor critLO ∈ [0.28, 0.36] | **⚑ FALSIFIED, and in the good direction.** A matching-shape excursion **FIRES** at both ends — **20.571 s @ 0.2791** (critLO) and **19.102 s @ 0.2451** (critHI), both survived with full recovery. I predicted the phenomenon would stay absent; it appears and **over-shoots the measured 7.4167 s by 2.8×** |
| **P.7** | T4b(c) does not fire on any fold-ON cell | **CONFIRMED — 0 of 14** |
| **P.8** | the match gates MOVE for the first time since I-7; MG-3 above 17; MG-4 shifts ≥ 0.002 | **CONFIRMED on every limb** — MG-3 **27**, MG-4 shifts **0.164**, and MG-1 flips to **MET** (§ 9) |
| **P.9** | fold-off byte identity EXACT ×3 vs I-10 and ×3 vs I-5; key ABSENT | **CONFIRMED** on the surface layer; the baton layer is exact under the four-leaf provenance mask D-I10-1 proved unavoidable (§ 1.1) |
| **P.10** | `S-IMMUNE-GATES` terminates `wave_not_cleared:timeout` at wave 152, t ≈ 348 s | **SPLIT — wave 152 CONFIRMED, mechanism FALSIFIED.** It does not time out; **the CLUSTER player walks 80.322 m off the arena in 18.3 s chasing immortal hazards** (§ 8) |
| **P.11** | `S-CADENCE-LO` spans = record × [1.06, 1.10]; hits exactly `⌊N × 0.9295408⌋` | **⚑ FALSIFIED on both limbs.** The cell **dies at 156** so no span ratio exists; and the accumulator fires **1,192 vs 1,194** — my own predicate defect, **D-I11-3** (§ 12.2) |
| **P.12** | `S-BANNER-ADD` l4l = critLO × [1.13, 1.22], i.e. ≥ 310 s | **⚑ FALSIFIED on magnitude, CONFIRMED on direction — 206.204, ratio 1.064.** ⚑ And it is **still inside the T2 band**, so IS-I11-1 changes no verdict either (§ 12.1) |
| **P.13** | chain positive control 79,240/79,240, worst \|Δ\| ≤ 0.005 | **CONFIRMED exactly** |
| **P.14** | ≥ 3 of 10 waves change rank vs I-10 | **CONFIRMED — 6** (153, 160, 151, 152, 156, 157) |
| **P.15** | determinism ×2 EXACT; batons FULL 67/67; Law 3 `moved: {}`; wall 22/22 | **SPLIT.** determinism **0 differences ×6** ✓ · batons **FULL 67/67 ×6** ✓ · Law 3 `moved: {}` ✓ · **wall 21/22** ✗ |
| **P.16** | D-I8-3 (`ManaBurnDrain`) unreached | **CONFIRMED** |
| **P.17** | the named unifying error (§ 10.1) | **PARTIALLY FALSIFIED — in my favour, which is the outcome I trust least and report first** |

### 10.1 — ⚑ THE ERROR I NAMED BEFORE THE RUN, AND WHY IT IS ONLY HALF RIGHT

Math note § 9.1, written before any code:

> *"I have priced the player's damage against the board's DEFENCE, and the referent's final two
> waves are not slow because his damage got worse — they are slow because he stopped attacking. …
> A composition fold makes each of those bodies take ~30 % longer to kill; it cannot make a 5-body
> wave take 25.95 s unless the player spends most of that time not in contact. … If P.4 confirms —
> if the w160 inversion survives both bracket ends — then the residual after I-11 is the player's
> TIME-ON-TARGET, and I will say so whether or not it embarrasses this iteration."*

**The antecedent did not confirm.** w160's inversion is gone: 0.787 → **1.171** (critLO) and
**1.092** (critHI) against its own mid-median. Composition-dependence bought **part** of the
final-two-wave slowdown that I said it could not buy at all — because I reasoned about *body count*
and the real driver is *body ARMOUR*, and w160's median armour (1,834) is double the mid-board's.

**But it bought only part.** Measured 1.596; sim 1.171. **The remaining 27 % of w160's slowdown, and
essentially all of w154's 2.700× over-run, are still unexplained by anything in the damage chain.**
So the residual I named is still there — it is just smaller than I claimed and no longer the whole
story. I said I would report the number whether or not it embarrassed me; here it is, and this time
it flatters me, which is the version I trust least.

### 10.2 — THE PER-ITERATION ERROR LINE, EXTENDED

I-1 priced sustain not exposure · I-2 eHP not co-residence · I-3 throughput not reach · I-4 the size
of the counterplay not its shape · I-5 the repair not its convergence · I-6 the mean not the variance
· I-7 the numerator of a saturated ratio · I-8 the solver not the board it produces · I-9 the
actuation not the arrival process · I-10 the correlation not the dwell.

**I-11: I priced every term as if it acted alone, in a system whose defining feature is that it does
not.** Both brackets — crit (a flat 50 %) and raw range-end (a 37 % swing) — moved the like-for-like
by under 1 %, because the uncapped disc converts damage into ring-emptying and ring-emptying back
into damage. **Every marginal-effect estimate in the math note was an open-loop estimate of a
closed-loop system.** That is the transferable lesson and it applies to the next iteration's
predictions too.

---

## 11 — ⚑ WHAT GOES TO THE CONDUCTOR

### 11.1 — THE STRUCTURAL FINDING FROM I-10 IS CONFIRMED BY ITS OWN REMEDY

| lap | perturbation | terminal | like-for-like |
|---|---|---|---|
| I-7 | +4,158 monster damage | unmoved | unmoved |
| I-8 | +129,150 damage; float32 re-solve | unmoved | 233.551 → 223.265 |
| I-9 | −486,590 damage-prevention | unmoved | **223.265306122449** |
| I-10 | arrival phase re-anchored; intake +19.7 % | unmoved | ⚑ **223.265306122449** |
| **I-11** | **the player's own damage chain** | ⚑ camp cell **DIES** | ⚑ **193.796 — MOVED, AND INTO BAND** |

I-10 § 11.1 claimed T2 and T3 were *"functions of the player's offence alone"* and asked the
conductor to rule on it. **The claim is now demonstrated by construction:** the one fold that touched
the player's offence moved both bands on the first attempt, after four iterations in which nothing
monster-side could move either by one bit.

### 11.2 — ⚑ `IS-I11-1` — THE BANNER COMPOSES MULTIPLICATIVELY WHERE LAP L MEASURED ADDITIVE. ROUTED.

PM-3's Vanguard Banner applies `offensiveTotalDamageModifier = +100 %` **multiplicatively** (`×2.0`),
on **1,229 of 6,321 ticks (19.44 %)** at I-10's reference cell. Lap L § 4.1 ratified the composition
law as **ADDITIVE**, exactly and to the integer on six independent damage types, with the
multiplicative candidate **falsified**. Under the measured law the banner is worth
`(1+31.36)/(1+30.36) = ×1.03189` — **+3.19 %, not +100 %**.

**I kept the ×2.0** on scope grounds (the banner is outside R-PM4-27's enumerated chain), on
minimal-delta grounds (folding two terms destroys attribution), and because it is a landed PM-3
ratification that this run's practice ROUTES rather than settles in-seam. The math note stated in
advance that this was the choice which *creates* a divergence I would have to route rather than the
one that would let me close the question — **and the measurement makes that moot: `S-BANNER-ADD`
lands at 206.204 s, still inside the T2 band, changing no T-verdict.** The contradiction is real and
belongs to the conductor; **its consequence for I-11's scorecard is nil, and that is measured.**

### 11.3 — ⚑ `D-I11-1` — THE PLAYER HAS ONE DAMAGE STREAM AND IT IS COSTING A THIRD OF HIS OUTPUT

32.3 % of the player's `damage_dealt` rows now carry `damage_raw = 0.0`. Lap L § 3.2 / § 5 emitted
the two streams that would kill those bodies — **Soulfire** (`SkillSecondary_AttackProjectileOrbiting`,
`projectilePeriod = 0.20 s`, **100 % pierce**, lightning 229 @ rank 13) and the Gutsmasher /
Sandreaver **bleed** riders (+330 and +210 per 3 s, +50 % bleed modifier, +100 % bleed duration) —
and folded neither. **This is the largest un-folded quantity left in the player's offence, it is
already decoded, and it is the obvious candidate for the next lap.** It would also plausibly move
w154 (§ 5): a wave whose over-run is 2.700× and whose roster is 13 bodies with 8 immune-pet spawns
is exactly where a pierce-everything second stream would bite.

### 11.4 — THE DISCIPLINE-#12 SEMANTIC SHIFT, FOR THE DECISIONS LOG

`outcome == "cleared"` now means **"every KILLABLE entity is dead"** rather than **"every spawned
entity is dead"**, and `n_pets_alive_at_wave_end` can be non-zero on a cleared wave. Framed in both
MIGRATION docs and in the commit message. **Proposed for the decisions log** (jack-ryan writes; I
propose): *the sim's clear predicate is scoped to the player's modelled offence, and the gap between
that and the player's actual offence is `D-I11-1`, carried explicitly.*

---

## 12 — DEFECTS BANKED

### 12.1 — `D-I11-3`: THE CADENCE ACCUMULATOR RESETS AT EVERY WAVE BOUNDARY, AND MY CHECK DID NOT KNOW

**Assert-wall check 7 is the lap's one RED.** I asserted `|n_hits − ⌊N × 0.9295408⌋| ≤ 1`; measured
**1,192 vs 1,194** (`S-CADENCE-LO`, 6 waves) and **3,068 vs 3,073** (`S-CADENCE-LO-CH`, 15 waves).

**The cause is a real modelling fact I did not declare:** `PlayerOffense` is constructed **per wave**
(it must be — the mitigation board is keyed `(record, wave)`), so the accumulator's fractional credit
is **discarded at every wave boundary**, losing up to one hit per wave. The residuals are exactly
`≈ n_waves / 3`, which is what a uniform discarded remainder predicts.

**Materiality: ≈0.06 % of hits over a 20-wave ladder.** It cannot reach a T-verdict. **Not repaired
mid-lap** — I-10's precedent stands: a predicate discovered wrong by its own run is banked and
reported, not silently fixed into green. **This is the third consecutive lap in which my own
assert-wall specification, not the model, produced the RED** (I-9 check 2 → I-10 check 12 → I-11
check 7), and that pattern is itself worth the conductor's attention.

### 12.2 — `D-I11-2`: A POSITIONAL EVENT-COLUMN READ, CAUGHT BY A CRASH RATHER THAN BY A TEST

The first draft of `offense_forensics_i11` counted `run.EVENT_COLUMNS` **by eye** and read
`damage_source_tag` where it meant `damage_raw`. It crashed on the string `'initial'` — **the good
outcome**: a positional mis-read that happened to land on a float column would have published a
wrong damage distribution silently. Fixed by resolving indices from `EVENT_COLUMNS.index(...)`,
which is now how the driver reaches every column.

### 12.3 — OPERATIONAL: A DISCIPLINE #3 NEAR-MISS, DECLARED

While launching the driver I briefly had **two concurrent processes on the same seed** — a direct
violation of Discipline #3 (no parallel runs of the same seed). **Zero artifacts had been written
when I detected and killed both**, verified by an empty `simulation/output/*i11*` glob, and the
landing run is a single process from a clean start. **No artifact in § 1 is contaminated.** Declared
because a near-miss that goes unreported is indistinguishable from one that was never noticed.

### 12.4 — CARRIED

**`D-I8-3`** (`ManaBurnDrain`, no measured resistance row) — **unreached** by any cell.
**`D-L6`** — answered from the sim's side, not invented: the disc test is body **CENTRE** against a
3.0 m radius, unchanged by this fold.

---

## 13 — WHAT I DID **NOT** TOUCH

Monster offense entire (Lap I) · the arrival-phase model (I-10 `ENGAGE`) · the converging solver, τ,
the non-overlap invariant · the tick order · movement, cadence, dash, counterplay · **the BOARD-ROLL
RNG**, so the bodies, their records and their scatter are byte-identical to I-10's · eHP (Lap D/E) ·
the seed (conductor seed 9) · **`TICK_S` and the master clock** · the player's incoming mitigation ·
Soulfire and bleed (**declared absent**, `D-I11-1`) · Law 3 (`moved: {}`) · `generation/`, `element/`,
`export/` beyond six additive spec fields, `telemetry/`.

---

**Author:** gamora (simulation seam) · 2026-08-14 · math note first, code second, and the git order
(`f39b6d0e` → `adacd009` → `b42569f0` → `ce88685d` → `7b021ab7`) is the proof.
