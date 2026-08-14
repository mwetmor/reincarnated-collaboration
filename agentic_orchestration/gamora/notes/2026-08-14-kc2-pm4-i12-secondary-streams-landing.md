# KC2-PM4 · I-12 — landing note: **the stream the commission named first is inert, the stream it named second closed the gap — and the board's largest residual turned out not to be a damage residual at all.**

> **Run:** KC2-PM4 · **Iteration:** I-12 · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** gamora (simulation seam) · **Date:** 2026-08-14
> **Fired under:** **R-PM4-30** (charter ledger **L-22**), on my own **D-I11-1**.
> **Also landed:** **R-PM4-29** (the measured additive banner) · **R-PM4-28** (critLO of record).
> **Math note (committed BEFORE the code):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i12-secondary-streams-2026-08-14.md`
> — commit `42b3bd05`, its own commit. **The git order is the proof.**
> **Judged against:** the **L-19 re-derived bands** and I-11's **critLO** pinned surfaces.

---

## 0 — The one-paragraph answer

D-I11-1 said 32.3 % of the player's hits land for zero because the disc models one damage stream,
and named the two Lap L had decoded. Both are folded. **The per-contact zero fraction — the
quantity that gap actually denotes — falls 32.3 % → 1.87 %.** But the arithmetic banked in the math
note *before the code* said the headline stream would do none of that work, and it was right:
**not one of the 27 physically-immune records on waves 151–171 has a lightning resistance below
100, so Soulfire's applied damage against every one of them is exactly 0.0.** Bleed reaches 23 of
27. The banner correction (R-PM4-29) landed in the same lap and moved the like-for-like **+12.4 s
away** from the target's centre; the streams moved it **−0.9 s back**; the net is **205.306 s**,
still inside T2. T3 MAE improves 4.947 → **4.462**, and T4a improves 0.9635 → **0.9591**, its
closest approach to the measured 0.932 in the run's history. **And the lap's largest finding is not
about damage at all:** w154, the board's worst span residual at 2.700× and unmoved across three
iterations, moved by **+0.0004 s** — because the player's last kill there lands at **18.612 s** and
the wave runs to **38.122 s**, with every one of the sixteen deaths in that 19.510 s gap a
`pet_ttl_expired`. **Over half of w154 is a TTL wait no player-offence fold can touch.**

---

## 1 — WHAT LANDED

**Engine commit range:** `42b3bd05..d114e6d5` (7 commits) · **meta:** this note.

| # | commit | what |
|---|---|---|
| 1 | `42b3bd05` | **MATH NOTE**, its own commit, before any code |
| 2 | `583ebdae` | the fold — `kc2/secondary_streams.py`, one keyword, two dataclass fields |
| 3 | `75c67298` | knot supplies + findings + `MIGRATION.md` |
| 4 | `850b65a0` | six baton specs |
| 5 | `3ac5736a` | **D-I12-7** — two wire defects caught by star-lord's gate, repaired, artifacts repinned |
| 6 | `d994bfe6` | pre-D-I12-7 artifacts retired |
| 7 | `d114e6d5` | **six batons, FULL 67/67 each** |

### Artifacts of record — ⚑ FULL 64 hex, never truncated (GL-6)

**⚑ BATONS — SIX, FULL, 67/67 green (VALIDATOR 33/33 · G-STATS 1/1 · G-E 33/33):**

| cell | baton sha256 |
|---|---|
| **`cluster_defon__critlo` ← RECORD** | `6477057fe4f61bd7b5325fe5a17b93e8525fda0b2e708fc72f17e5a996c6367e` |
| `camp_defoff__critlo` | `941976fcfb9938539ea47e1ae5d1bb9a170321a75ce1bd5a675ebc476077dbda` |
| `cluster_defoff__critlo` | `3a4369d8d4bf03bfac7f8f2463986dbf26b6c2bd6b1d522b4473e149ee710c14` |
| `cluster_defon__crithi` | `2b570d3f3232163ca233ef4bfc2e221082949c4977846e9dd630d102e64c985e` |
| `camp_defoff__crithi` | `52b9f52889eae3ee9e2131f59962fac20c557f273d820ff7b037b3f455b08b2f` |
| `cluster_defoff__crithi` | `6daf87d06e2fe000262af395122cadfb1987fc0cf93db7c45c277f3f19e61d13` |

**Findings:** `076d7fa21f3ce13bfdc5a7e1fe3196233c4fa795ff4d1be1238efc7c354b6515`
(`kc2-pm4-i12-findings-20260814_065051.json`)

**Knot supplies:**
`36295de4a5fd8d70f051df401204cd0581bf8004ccee3e73ab1c9b59181665d7` camp/critLO ·
`df93a75ad2aaad237dc8121baa74d48c7b9123c6fdc0b2c556af20dc906b8b70` cluster-defoff/critLO ·
`4cdac53a5e30ed6269ad4019bc326a8ae00040e61b9f3931bedc46f60288829e` **cluster-defon/critLO** ·
`116a2caf67b7780d36e7333db7baf8f45e2e18257d3b977757d9f4c261f4c3ff` camp/critHI ·
`4dbca2a387c530ecef2125986bbef9217beb3d3323bba4eaa6cbfd3843d341ed` cluster-defoff/critHI ·
`29a681eb18c88bcf1ce1d6dafa4cb35ee1c7746e9d1785ffdf0f1291efff2644` cluster-defon/critHI

**Determinism ×2 (0 differences, all six):**
`ccbab7f9a8d1349ee9f3fad7d0c625439265f67eb6071213c22e13d3dcc705a0` ·
`b6d6fef55c31a69bf111c61e31b99efbaa62f1ad51c7a248bfb73445f8c327b5` ·
`05e3c3ff159e48ea6b15efc9c496e37534cf55b1a040b333b77559bb77316c70` ·
`ac831121f6479b986d0249194552854d7b04ea91f245f65e9440e0db97fcd8ab` ·
`1952695dc034e6b592a162d6b253f39a378aa633cfa9470e6d9affe9a387dcd6` ·
`9ab4a9265c123fce4d23d506cad4c14a5c4541b6785c96ebeb5549bb15d6d59c`

### 1.1 — ⚑ FOLD-OFF BYTE-IDENTITY, EXACT ×3, WITH THE KEY GENUINELY ABSENT

| cell | fold-OFF surface | vs I-11 critLO |
|---|---|---|
| camp_defoff | `d82ae4017acc1fb7d618446e571813423f2c1a1b43c7923935157c7cc2f327b4` | **EXACT** |
| cluster_defoff | `22eb6960506613ddaab06ee0ebf5012de6f47653815475d82fedc6a139a12f30` | **EXACT** |
| cluster_defon | `cea41eef6fb50eb90621b4b706f4117d38a0929b2bc2ef357601c52b851f7808` | **EXACT** |

`secondary_streams_wire` empty on all three — the key is **omitted**, not passed as `None`
(ABSENT-not-None, the sixth use of the discipline in this run).

**⚑ DIVERGENCE-BY-CONSTRUCTION, DECLARED IN THE MATH NOTE § 7 BEFORE RUNNING:** the fold-ON
reference cell *cannot* match its I-11 baton, because R-PM4-29 changes the banner on the DEF-ON
cell. The two DEF-OFF cells carry no banner, so their delta from I-11 is the **streams alone** —
which is why the matrix is worth running as a matrix, and how two corrections landing in one lap
stayed separately attributable.

### 1.2 — ⚑ A THIRD DETERMINISM LAYER, UNASKED FOR, AND IT IS THE PROOF OF § 12.2

The lap was executed **end-to-end three times** (twice before D-I12-7 was found, once after).
Across the two pre-fix processes, **every measured quantity was identical and only wall-clock
differed.** Across the fix boundary, **every fight quantity was again identical to the digit** —
l4l, all ten spans, T3 MAE, mean/min HP, both zero fractions, the kill counts, on all six matrix
cells *and* all six sensitivity cells — while only the emitted-surface digests moved. That is what
makes "D-I12-7 was a wire fix, not a model change" a **measurement rather than an argument**.

---

## 2 — ⚑ THE FOLD, AND THE SENTENCE BANKED BEFORE THE CODE

```
soulfire :  229 x (1 + 447/100) = 1 252.63 lightning per proc, 1 proc / 0.20 s, 100 % pierce
            applied(b) = 1252.63 x max(0, 1 - res_lightning_b/100) x crit      [NO armour]
bleed    :  (330 + 210) x (1 + (1366 + 50)/100) = 8 186.40 over 3.0 x 2.30 = 6.90 s
            dps(b)     = 1 186.43 x max(0, 1 - res_bleeding_b/100)             [NO armour, NO crit]
banner   :  (1 + 31.36)/(1 + 30.36) = x1.03189                                 [was x2.0]
```

**Armour does not apply to either**, and that is a read rather than an assumption: the record's own
branches are named `physcialDamageDefenseEquationDLEP` / `physicalDamageDefenseEquationDGP` —
physical-scoped by their own field names. **Crit applies to Soulfire and not to bleed**, because
the two-slot law is a *hit* law (`probabilityToHitEquation` → `pthDamageModifier`) and a DoT already
burning on a target is not a swing and has no PTH. Both declared in the math note § 5, before code.

### ⚑ 2.1 — THE HEADLINE: SOULFIRE IS INERT ON THE IMMUNE SET

Math note § 6.2 pre-registered it from pure table arithmetic. The instrument
(`secondary_streams.immune_reachability()`) confirms it from the pinned substrate:

| | waves 151–171 |
|---|---:|
| distinct physically-immune records | **27** |
| ⚑ **SOULFIRE-killable** | **0** |
| BLEED-killable (`res_bleeding = 0.0`) | **23** |
| immune to all three streams | **4** |
| ⚑ **minimum lightning resistance over the whole immune set** | **100.0** |

> **⚑ SOULFIRE CANNOT KILL ONE BODY THE PHYSICAL STREAM CANNOT KILL.** The stream R-PM4-30 named
> first is, on this board, a ~1 % top-up on bodies already dying in under a second. The four
> all-immune survivors are `beast_bloodpool`, `winddevil_01`, `azaelon_winddevil_01`,
> `evernight_shadowdevil_01` — all at `res_bleeding = 500`, all with finite TTLs.

**And the attribution split measures it independently.** `S-BLEED-OFF` (Soulfire alone) lands
l4l **199.265 s** and walls at 165; `S-SF-OFF` (bleed alone) lands **206.857 s** and walls at 165;
both streams together land **205.306 s** and reach **171**. The two are **not additive** — which is
itself the finding of § 11.2.

---

## 3 — ⚑ THE `D-I11-1` ANSWER, AND WHY THE INSTRUMENT IT NAMED WAS THE WRONG ONE

| instrument | I-11 | **I-12 record cell** |
|---|---:|---:|
| per-**ROW** zero fraction (all player damage rows) | 32.3 % | **16.07 %** |
| ⚑ per-**CONTACT** zero across **all three** streams | 32.3 % | ⚑ **1.87 %** |

**These are different questions and D-I11-1's 32.3 % was the per-ROW one.** The quantity "the
player is fighting with one arm" actually denotes is the per-CONTACT one: of every (tick, body) the
disc touched, how many received nothing from the player's whole offence. **It falls by a factor of
17.3.** The residual 1.87 % is the four all-immune records, and they are ground hazards with TTLs.

Applied-damage share at the record cell:

| stream | rows | zero rows | applied | share |
|---|---:|---:|---:|---:|
| physical | 21,643 | 6,138 | 630,978,096 | **98.59 %** |
| lightning (Soulfire) | 8,147 | 2,501 | 6,010,401 | 0.94 % |
| bleeding | 34,703 | 1,723 | 2,982,425 | 0.47 % |

**The secondary streams are 1.41 % of the player's applied damage and they closed 94 % of the
zero-contact gap.** That is the whole shape of the finding: the gap was never about *volume*.

---

## 4 — ⚑ T-SCORECARD vs THE L-19 BANDS (record cell `cluster_defon__critlo`)

| | target | I-11 critLO | **I-12 RECORD** | verdict |
|---|---|---:|---:|---|
| **T1** death wave | 160 {159–161} | @171 | **`arena_tier_exhausted` @171** | **MISSED** |
| **T2** l4l | 182.7167 ∈ [155.31, 210.12] | 193.796 | ⚑ **205.306** (ratio **1.1236×**) | **MET** |
| **T3** MAE | — | 4.947 | ⚑ **4.462** | **NEAR** (best of the run) |
| **T3** median ratio | 1.000 | 0.9400 | 1.0656 | — |
| **T3** w154 ratio | 1.000 | 2.7005 | **2.7005** | ⚑ **unmoved — § 5.1** |
| **T3** w160 ratio / inverted | 1.000 / no | 0.720 / no | **0.8556 / no** | improved |
| **T4a** mean HP | 0.932 | 0.9635 | ⚑ **0.9591** | **MET**, closest of the run |
| **T4b(a)** dwell | 7.4167 s @ 0.2919 | 20.571 s @ 0.2791 | **20.980 s @ 0.2557** | fires; **2.83× over** |
| **T4b(b)** full-health dwell | 1.6166 s | n/a | n/a (no death) | — |
| **T4b(c)** instant kill | ≤1 tick on w160 | did not fire | **did not fire** | **MISSED** |

**Match gates (judged separately):** MG-1 **MET** · MG-2 MISSED · MG-3 MISSED · MG-4 MISSED ·
MG-6 **MET** · MG-7 **MET** — the same block as I-11, unchanged by this fold.

**⚑ The crit bracket remains verdict-identical on all five judged quantities** (`DIVERGES: false`),
confirming R-PM4-28 for a second lap. `D-L5` carries as a named gap.

**⚑ Deepest survived excursion anywhere: floor 0.13102 at wave 160** (4.816 s, full recovery) —
the sim now goes far below the referent's measured floor of 0.291877 **and still does not die.**
That is I-10's "produces the DEPTH, cannot produce the DEATH" residual, deeper than ever.

---

## 5 — THE WAVE-SPAN TABLE, SIM vs MEASURED

| wave | measured (L-19) | I-11 critLO | **I-12 RECORD** | I-12 ÷ measured |
|---:|---:|---:|---:|---:|
| 151 | 16.27 | 18.286 | 18.286 | 1.124 |
| 152 | 16.25 | 15.592 | 16.571 | 1.020 |
| 153 | 14.75 | 16.327 | 16.735 | 1.135 |
| 154 | 14.12 | 38.122 | ⚑ **38.122** | ⚑ **2.701** |
| 155 | 16.32 | 15.020 | 14.041 | 0.861 |
| 156 | 20.20 | 23.184 | 22.449 | 1.111 |
| 157 | 18.85 | 15.510 | 15.755 | 0.836 |
| 158 | 13.10 | 11.020 | 11.510 | 0.879 |
| 159 | 26.30 | 22.041 | 29.633 | 1.127 |
| 160 | 25.95 | 18.694 | 22.204 | 0.856 |
| **l4l** | **182.72** | **193.796** | ⚑ **205.306** | **1.124** |
| **MAE** | — | 4.947 | ⚑ **4.462** | — |

Final-two-wave slowdown: measured **1.617 / 1.595**; I-12 sim **1.779 / 1.333**. The inversion
remains gone.

### 5.1 — ⚑⚑ THE LAP'S LARGEST FINDING: w154 IS NOT A DAMAGE RESIDUAL (`D-I12-5`)

w154 has been the board's worst residual for three iterations: **2.885× (I-10) → 2.700× (I-11) →
2.700× (I-12)**, across three completely different damage models. This lap moved it by
**+0.0004 s**. The reason is on the wire:

```
w154, record cell:
  player's LAST KILL            t = 18.612 s   (w154_pet0057)
  wave END                      t = 38.122 s
  deaths in the 19.510 s gap    16 — EVERY ONE `pet_ttl_expired`
```

> **⚑ 51.2 % OF WAVE 154 IS A TTL WAIT.** After 18.6 s there is nothing left on the board the
> player can kill; the wave runs another 19.5 s while pet contracts time out. **No fold to the
> player's offence — of any magnitude, from any stream — can move it**, and the three-iteration
> flatness of the residual is now explained rather than merely observed.
>
> **What WOULD move it** is whether the player's targeting reaches those pets before their TTL
> does, which is a **geometry-and-locomotion** question (Laps F and J), not an offence one — and it
> is the same surface as the movement-while-channeling / pack-seek targeting policy already routed
> to the engine at **R-CPB-4**. **Routed to the conductor as `D-I12-5`.**

This also retires a framing in my own I-11 § 11.3: I wrote that w154 "is exactly where a
pierce-everything second stream would bite." **It is not, and the reason is structural, not
magnitudinal.**

---

## 6 — THE SIX MATRIX CELLS

| cell | terminal | l4l | mean HP | min HP | T3 MAE | ROW-zero | ⚑ CONTACT-zero |
|---|---|---:|---:|---:|---:|---:|---:|
| **`cluster_defon__critlo` ← RECORD** | @171 | **205.306** | 0.9591 | 0.1310 | **4.462** | 0.1607 | **0.0187** |
| `camp_defoff__critlo` | ⚑ **player_death@154** | 83.837 | 0.8833 | 0.0000 | 7.126 | 0.3358 | 0.1329 |
| `cluster_defoff__critlo` | @171 | 195.020 | 0.9624 | 0.3258 | **4.122** | 0.1586 | 0.0166 |
| `cluster_defon__crithi` | @171 | 195.429 | 0.9575 | 0.3223 | 5.189 | 0.2025 | 0.0211 |
| `camp_defoff__crithi` | @171 | 185.143 | 0.9580 | 0.1012 | 6.038 | 0.2125 | 0.0261 |
| `cluster_defoff__crithi` | @171 | 193.878 | 0.9580 | 0.1407 | 5.900 | 0.1909 | 0.0251 |

⚑ **All six l4l values land inside `[155.31, 210.12]` except the dead cell's** — including, for the
first time, the camp cell at critHI.

### Sensitivity cells

| cell | terminal | l4l | T3 MAE | what it isolates |
|---|---|---:|---:|---|
| `S-STREAMS-OFF` | @171 | ⚑ **206.204** | 4.339 | ⚑ the banner correction **alone** — reproduces I-11's `S-BANNER-ADD` **EXACTLY**, to the tenth of a millisecond |
| `S-SF-REACH-HI` (4.0 m) | @171 | 205.224 | 4.323 | **D-I12-1's HI end** — verdict-identical |
| `S-BLEED-DPS-HI` (2 728.80/s) | @171 | 204.327 | 4.478 | **D-I12-2's HI end** — verdict-identical |
| `S-SF-OFF` (bleed only) | @165 | 206.857 | 4.258 | attribution split |
| `S-BLEED-OFF` (Soulfire only) | @165 | 199.265 | 4.465 | attribution split |
| `S-BANNER-MULT` (retired ×2.0) | ⚑ **player_death@156** | 104.816 | 8.347 | continuity with I-11's 193.796 |

> **⚑ `S-STREAMS-OFF` = 206.20408163265307 IS THE ATTRIBUTION PROOF.** It reproduces I-11's
> `S-BANNER-ADD` bit-for-bit, which means the two corrections landing in one lap are cleanly
> separable: **the banner is worth +12.408 s and the streams are worth −0.898 s.**

---

## 7 — ⚑ SOMETHING DIED, AND IT DIED IN THE SAME PLACE

`camp_defoff__critlo` — **`player_death` at wave 154**, exactly as at I-11, and the ~1.2 %
throughput the streams buy was not enough to save it. **P.7 CONFIRMED.**

**⚑ And a new death appeared where the OLD banner is kept.** `S-BANNER-MULT` — the I-11
composition, plus the streams — **dies at wave 156**. The falsified multiplicative banner does not
merely inflate the player's damage; on this board it kills him, because clearing faster moves him
through the arena on a different trajectory. **T1 is still MISSED** (target 160 {159–161}); no
death anywhere lands in the acceptance window.

---

## 8 — PRE-REGISTERED PREDICTIONS vs OUTCOME

**Graded against the math note § 6.4 table, pinned in the driver before the run.**

| # | prediction | outcome | verdict |
|---|---|---|---|
| **P.1** | Soulfire kills 0 of the immune set | 0 of 27; min lightning res 100.0 | ⚑ **CONFIRMED** |
| **P.2** | bleed kills 22 of 26; the void does not die inside w154 | **23 of 27**; void survived w154 | **CONFIRMED-WITH-CORRECTION** (§ 8.1) |
| **P.3** | w154 ≈ 37.6 ± 0.6 s | 38.122 s | **CONFIRMED BY BAND, FALSIFIED IN MECHANISM** (§ 8.2) |
| **P.4** | l4l = 206.15 ± 0.5 s | **205.306** | **FALSIFIED** (by 0.34 s) |
| **P.5** | T3 MAE = 4.33 ± 0.10 | **4.462** | **FALSIFIED** (by 0.03) |
| **P.6** | reference does not die, @171 | `arena_tier_exhausted` @171 | **CONFIRMED** |
| **P.7** | camp/critLO still dies at w154 | dies @154 | **CONFIRMED** |
| **P.8** | dwell 21–24 s, floor 0.20–0.24 | **20.980 s @ 0.2557** | **FALSIFIED** (both, narrowly) |
| **P.9** | T4b(c) does not fire | did not fire | **CONFIRMED** |
| **P.10** | T4a = 0.964 ± 0.003 | **0.9591** | **FALSIFIED** — and in the **good** direction |
| **P.11a** | per-ROW zero fraction **RISES** to 30–50 % | **fell to 16.07 %** | ⚑ **FALSIFIED** (§ 8.3) |
| **P.11b** | per-CONTACT zero fraction drops to 1–4 % | **1.87 %** | ⚑ **CONFIRMED** |
| **P.12** | reach bracket verdict-identical | 205.224 vs 205.306, no verdict moves | **CONFIRMED** |
| **P.13** | bleed-DPS bracket verdict-identical | 204.327 vs 205.306, no verdict moves | **CONFIRMED** |
| **P.14** | critHI verdict-identical | `DIVERGES: false` on all five | **CONFIRMED** |

**8 confirmed / 1 confirmed-with-correction / 1 split / 5 falsified.**

### 8.1 — P.2's correction, and its cause

I predicted **26** immune records and **22** bleed-killable; the instrument reads **27** and **23**.
**The cause is mine and it is instructive:** my pre-registration scratch deduped by *basename*,
which silently merged two distinct `firedevil_01.dbr` records living at different archive paths.
The instrument dedupes by **full record path**. The substantive claims — 0 soulfire-killable, 4
immune-to-all-three — are exact.

### 8.2 — P.3 passed its band and failed its reasoning, and the failure is the finding

I predicted w154 would *shorten by ~0.5 s* and land at 37.6 ± 0.6. It landed at 38.122 — inside the
band, but **because it did not move at all** (+0.0004 s), not because it moved as predicted. I was
right that immune bodies cost the killable ones nothing under an uncapped disc; I was wrong about
what sets the span, and § 5.1 is what actually does. **Reported as a mechanism failure, not banked
as a hit.**

### 8.3 — ⚑ P.11a is the cleanest falsification of the lap

I predicted the per-ROW zero fraction would **rise** to 30–50 %, reasoning that Soulfire emits a row
per proc and every immune body's Soulfire row is zero. It **fell to 16.07 %**. What I missed is that
bleed emits **34,703 rows of which only 1,723 are zero** — more rows than the physical and lightning
streams combined, overwhelmingly non-zero, diluting the physical stream's zeros. **I priced the
numerator and forgot the denominator.**

### 8.4 — ⚑ THE UNIFYING ERROR I NAMED IN ADVANCE — AND WHY IT IS THE WRONG ONE AGAIN

Math note § 6.4 closed: *"if these are wrong, the most likely reason is that I have priced the
streams' MAGNITUDE and not their REACH."* **That is not what happened.** The magnitude arithmetic
held (the streams are 1.41 % of applied, against ~1.23 % predicted); the reach bracket was
verdict-identical exactly as predicted. **The real unifying error is that I modelled the fold's
effect as a THROUGHPUT change when the quantities it moves are set by things other than
throughput** — w154 by TTL, l4l by trajectory divergence (§ 11.2). **This is the second consecutive
lap in which my pre-named unifying error was itself wrong** (I-10 § 10.1 named the same class of
miss), and the pattern belongs to the conductor.

---

## 9 — ⚑ WHAT GOES TO THE CONDUCTOR

### 9.1 — `D-I12-5` — THE BOARD'S LARGEST SPAN RESIDUAL IS A TTL WAIT, NOT A DAMAGE RESIDUAL

§ 5.1. **ROUTED.** w154's over-run is 51.2 % pet-TTL expiry after the player has nothing left to
kill. Three iterations of damage-model work could not move it and no fourth will. The surface that
would is **targeting/locomotion** — the same one already routed at R-CPB-4 (pack-seek targeting
policy). **This is the largest un-owned quantity the run has surfaced since I-10 § 11.1.**

### 9.2 — `D-I12-1` / `D-I12-2` / `D-I12-3` / `D-I12-4` — the four gaps this fold routed

| id | what | measured disposition |
|---|---|---|
| **D-I12-1** | Soulfire **orbit radius** MEASURED-ABSENT from Lap L | bracketed 3.0 (record) / 4.0 m over two MEASURED engine constants; **verdict-identical, immaterial to this run** |
| **D-I12-2** | duration modifier holds TOTAL or DPS | bracketed 1 186.43 / 2 728.80 /s; **verdict-identical, immaterial** |
| **D-I12-3** | bleed stack-vs-refresh | REFRESH of record on a measured discriminator; asserted ≤1 instance/target (wall check 8, PASS) |
| **D-I12-4** | four terms are **prose-provenance**, not pinned rows | graded `MEASURED-BY-PROSE` on the wire; **immaterial in consequence** — Soulfire is 0.94 % of applied and inert on the immune set |

**All four are immaterial to every T-verdict in this lap, and that is a measurement.** None needs a
decode fired on this run's account; all four should be closed by Lap-L emission hygiene if any
future lap gives Soulfire real work.

### 9.3 — ⚑ R-PM4-29's LAW-3 AUDIT, CLOSED HONESTLY

The math note declared, before the run, that the additive banner moves l4l **away** from the
target's centre and is adopted anyway. It did: **193.796 → 206.204**, and the record cell finishes
at **205.306** with a T2 ratio of **1.1236×** against I-11's 1.0614×. **T2 got worse and T3 got
better**, and the run carries the measured composition law rather than the falsified one. **No term
in this lap was selected by which way it moved a band.**

### 9.4 — ⚑ THE STRUCTURAL PICTURE AFTER TWO PLAYER-OFFENCE LAPS

I-10 § 11.1 proved T2/T3 are functions of the player's offence alone. I-11 moved them by folding
the offence. **I-12 folded the last un-folded piece of that offence and moved l4l by −0.9 s.** The
player's offence is now measured end to end: magnitude, armour law, per-body resists, hit law, crit
bracket, cadence, multiplicity, and all three damage streams. **T2 is in band; T3 is at its best;
T1 has never been closer than @171 on the reference cell.** What is left between the sim and the
death is **not the player's damage** — it is arrival structure, targeting, and the tail (T4b(c)).

---

## 10 — MATCH GATES

Unchanged from I-11: **MG-1 MET · MG-2 MISSED · MG-3 MISSED · MG-4 MISSED · MG-6 MET · MG-7 MET.**
This fold touches nothing any match gate measures, and the gates confirm it.

---

## 11 — TWO MEASURED PROPERTIES OF THE MODEL, WORTH THE CONDUCTOR'S ATTENTION

### 11.1 — The negative-feedback loop I-11 found is confirmed and quantified again

A **+1.23 %** throughput change moved l4l by **−0.44 %**. Compare I-11: **+50 %** crit → **−0.17 %**;
**+36.8 %** raw → **−0.75 %**. The uncapped disc keeps self-regulating.

### 11.2 — ⚑ BUT THE l4l RESPONSE IS NOT MONOTONE, AND THE ATTRIBUTION SPLIT PROVES IT

| cell | streams active | l4l |
|---|---|---:|
| `S-STREAMS-OFF` | none | 206.204 |
| `S-SF-OFF` | bleed only | **206.857** — ⚑ *slower than no streams at all* |
| `S-BLEED-OFF` | Soulfire only | **199.265** |
| record | both | 205.306 |

**Adding damage made the like-for-like longer in one arm and much shorter in another, and the two
together are not the sum of either.** At this scale l4l is dominated by **trajectory divergence** —
which body dies when changes the cluster centroid, which changes where the player walks — not by
throughput. **A consequence the conductor should weigh: sub-2 % perturbations to the player's
damage are, on this model, below the l4l noise floor**, and any future lap proposing to move T2 by
a term of that size is proposing something the instrument cannot resolve.

---

## 12 — DEFECTS BANKED

### 12.1 — `D-I12-6`: MY OWN ASSERT-WALL PREDICATE, FOR THE FOURTH CONSECUTIVE LAP

**Wall 14/15. Check 5 is the lap's only RED and it is mine.** I wrote
`add(5, "Law 3 — no constant moved", not _law3_moved(), ...)` where `_law3_moved()` returns an
always-truthy dict; the correct form (I-11's) is `.get("moved") == {}`. **The underlying property
holds** — the findings artifact carries `law_3.moved: {}` — and the check is **not repaired
mid-lap**, per the I-10/I-11 precedent.

**⚑ This is the fourth consecutive lap in which my own assert-wall specification, not the model,
produced the lap's only RED** (I-9 check 2 → I-10 check 12 → I-11 check 7 → I-12 check 5). I flagged
the pattern at I-11 § 12.1 and then reproduced it. **The wall needs its own wall**, and I am not
the right party to certify that.

### 12.2 — ⚑ `D-I12-7`: TWO WIRE DEFECTS, BOTH MINE, BOTH INVISIBLE TO MY WALL, BOTH CAUGHT AT THE SEAM

**This is the first time in this run that star-lord's baton gate has paid for itself against my
work, and it paid twice on the first cell it saw.**

**(a) A cross-seam schema change I had no authority to make.** I wrote
`death_cause = "killed_by_player_lightning"` onto the pet dict. `pets[].death_cause` is a `Literal`
enum in `baton_v1_schema` with exactly two members; pydantic refused the baton. **The existing
member was also the correct one** — a pet killed by Soulfire *is* killed by the player — and the
stream attribution is fully recoverable from the `death` row's `damage_source_tag`. No schema change
was needed and none was made. *I am the agent whose standing rule is "do not modify telemetry
schemas"; I modified one by accident and did not notice.*

**(b) Two tick spaces, one column.** `dot_expires_tick` was written as the **wave-local** index
`round(expires_t_s / period)` into a column the consumer reads in the **run-global** frame. **On
wave 151 the two frames coincide and the bug is invisible**; on every later wave the expiry lands
thousands of ticks in the consumer's past. Gate **M-25** (`dot_expires_tick >= run_tick`) caught 896
such rows immediately.

**Both repaired (`3ac5736a`), and the repair proven non-model by measurement** (§ 1.2): the full
re-run reproduces every fight quantity to the digit while only the emitted surfaces move.

### 12.3 — CARRIED

**`D-I11-3`** (cadence accumulator resets at wave boundary) — carried, unrepaired, ≈0.06 % of hits.
**`D-I8-3`** (`ManaBurnDrain`) — **unreached** by any cell (wall check 14, PASS). **`D-L5`** — carries
as a named gap; the bracket is verdict-identical for the second consecutive lap.
**`D-L6`** — unchanged; the disc test is body centre against 3.0 m.

### 12.4 — OPERATIONAL

The lap was executed three times **sequentially**, never concurrently. **No Discipline #3 exposure**
at any point (contrast I-11 § 12.3's declared near-miss).

---

## 13 — WHAT I DID **NOT** TOUCH

The physical stream · the two-branch armour law · the crit bracket · the cadence bracket · the
uncapped disc · `TICK_S` and the master clock · the **board-roll RNG** (bodies, records and scatter
byte-identical to I-11) · monster offense entire (Lap I) · the arrival-phase model (I-10 `ENGAGE`) ·
the converging solver, τ, the non-overlap invariant · the tick order · movement, dash, counterplay ·
**I-9's sustain actuation** (declared scope boundary: **neither stream feeds `leech_pool`** — ADCtH
is `offensiveLifeLeech*`-scoped and Lap L emitted no leech term for lightning or bleed; decided at
implementation, **not** pre-registered, and banked as such in the commit) · eHP (Lap D/E) · the seed
(conductor seed 9) · the I-11 clear-gate amendment · **Law 3 (`moved: {}`)** · `generation/`,
`element/`, `telemetry/`, `output/`; `export/` only via five additive `KC2RunSpec` fields and one
ABSENT-not-None branch.

---

**Author:** gamora (simulation seam) · 2026-08-14 · **math note first, code second, and the git
order is the proof.**
