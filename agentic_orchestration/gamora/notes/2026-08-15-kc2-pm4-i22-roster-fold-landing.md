# KC2-PM4 · I-22 — THE ROSTER FOLD — LANDING NOTE

**Agent:** gamora · **Conductor:** gandalf (RUN-CONDUCTOR) · **2026-08-15/16**
**Commission:** `R-PM4-60 part 4`; amendment mechanics `L-47`; ledger `L-47`…`L-50`.
**Authority:** Matt, verbatim 2026-08-15 — ***"fix the bonus spawn system and count-model holes
now."***
**Evidence:** legolas **Lap V**, **Lap V-2**, **Lap W** — all three re-hashed **EXACT** from my own
seat before a line of the math note was written (GL-6, § 11).

**Commits (engine, mine, THREE, math-note-only FIRST):**
`4dcfc100` math note (**zero code**) → `9bb524e0` math-note **ADDENDUM**, my own defect committed
**before** its repair (**zero code**) → `6c9cb5be` fold + module + driver + findings + MIGRATION +
AGENT_STATE. **NOT PUSHED.**

**Findings:** `src/reincarnated/simulation/output/kc2-pm4-i22-findings-20260816_040355.json`
sha256 **`5cdc6b434ac071d37729b769cd7d52bb9f9d75ecc53f57207cf3865a1c9c104c`**. Wall **17.1 s**.

---

## 0 — THE HEADLINE, IN ONE PARAGRAPH

**Wave 151 is body-identity-identical between the incumbent and the fold — same seed, same 28
bodies, same names, same records — and the incumbent clears it and reaches 155 while the fold dies
on it.** The only difference is the decoded `ProxyAmbush` burst: the p05 contingent lands at
`t + 4.000 s` **together** instead of at 4 / 7 / 10 / 13 s. **Four bodies arriving three, six and
nine seconds earlier end the ladder.** Every T-grade collapses — death **155 → 151**, l4l
**161.0612 → 8.4082**, T2 **0.8815 → 0.0460**, T4a **0.8848 → 0.8608** — and **I pre-registered that
they would, against my own interest, before the fold ran.** And the same term does the thing the
run has been chasing for four iterations: **the arrival ramp lands closer to the referent than in
any prior iteration — `t→50 %` 3.6735 s against 3.2670, `t→90 %` 7.1020 against 4.9670 — verified
against I-19/I-20/I-21's emitted artifacts, not their prose.** The roster amendment itself lands
exactly as decoded (188 → 177, 10/10 inside envelope, the three degenerate waves EXACT at 17/11/4)
and is **not** where the residual lives. **The residual's new address is the player's survival
model, and that is outside the decoded recipe — reported as such, never folded as such.**

---

## 1 — ⚑ THE RECORD-CELL SCORECARD — TWO ARMS

Bands: **T1** wave 160 {159–161} · **T2** l4l 182.7167 ∈ [155.31, 210.12] · **T4a** 0.932 ± 0.02 ·
**T4b(b)** 1.6166 s · **T4b(c)** wave-160 kill from full health only.

| record cell (`cluster_defon__critlo__COUPLED__…`) | T1 | T2 | T3 | T4a | T4b(b) | T4b(c) | death | class | l4l s | **T2 ratio** | T4a | T3 MAE |
|---|:-:|:-:|:-:|:-:|:-:|:-:|---:|---|---:|---:|---:|---:|
| **`PX-LO`** | ✗ | ✗ | — | ✗ | ✗ | **not armed** | **151** | DEATH | **8.4082** | **0.0460** | 0.8608 | 7.859 (9 unev.) |
| `PX-HI` | ✗ | ✗ | — | ✗ | ✗ | **not armed** | 152 | DEATH | 36.4082 | 0.1993 | 0.8994 | 7.828 (8 unev.) |

**Graded distance:** `PX-LO` **T1 −9 waves · T2 0.0460 · T4a −0.0712**; `PX-HI` **T1 −8 · T2 0.1993
· T4a −0.0326**.

**T4b(c) is NOT ARMED and that is the scorecard law, not a convenience** (`R-PM4-40 part 5`): it
scores **only** a wave-160 kill from full health, the ladder reaches 151/152, and the instrument
confirms **no ≥pool tick fired anywhere** (`⚑ instrument_saw_a_pool_tick_somewhere: false` on both
arms). The deepest single hits were 9,901 / 15,538 against a 20,005 pool — **neither is a one-shot
and neither is at wave 160.**

### 1.1 ⚑ AGAINST THE HONEST INCUMBENT — I-21's OWN RECORD CELLS, PINNED FROM ITS ARTIFACT

`D-I20-5`'s lesson held: pinned from I-21's **findings JSON** (`d68801c8…341d`), never its prose.

| arm | l4l I-21 → I-22 | Δ | death I-21 → I-22 | T2 ratio I-21 → I-22 | T4a I-21 → I-22 |
|---|---|---:|---|---|---|
| `PX-LO` | 161.0612 → **8.4082** | **−152.653** | 155 → **151** | 0.8815 → **0.0460** | 0.8848 → 0.8608 |
| `PX-HI` | 90.0408 → **36.4082** | **−53.633** | 154 (INSTRUMENT) → **152 (DEATH)** | 0.4928 → 0.1993 | 0.9057 → 0.8994 |

> **⚑ AND THE DIRECTION IS NOT A REASON TO WITHHOLD IT.** I wrote `S-2` into the math note, in its
> own commit, before any code existed: *"THE FOLD MAKES THE GRADES WORSE, AND I SAY SO BEFORE IT
> RUNS … registered against my own interest for exactly the `R-PM4-29` reason: the direction of a
> decode-true correction is not its justification, and neither is its cost."* I-21 was adopted
> while grading BETTER on that same basis. This one lands on the identical basis.

### 1.2 ⚑ THE SUPERLATIVE GUARD, EXERCISED (`D-CON-1`)

The one superlative in this note is the ramp, and it is checked against **emitted artifacts**:

| iteration | best record-cell `median_t50_s` | distance from referent **3.2670** |
|---|---:|---:|
| I-19 (`F10_arrival_ramp`) | 5.7959 | 2.529 |
| I-20 | 6.7755 | 3.509 |
| I-21 | 1.8776 (`PX-HI`) | 1.389 |
| **I-22** | **3.6735** (`PX-LO`) | **0.407** |

`t→90 %` likewise: I-20 9.6327, I-21 10.2857 (best), **I-22 7.1020** against the referent's 4.9670.
**No T2 claim is made anywhere in this note** — I-18 held 0.8502 and I-21 0.8815, both hits, and
I-22 holds neither.

---

## 2 — ⚑ THE PER-WAVE OLD-vs-NEW ROSTER TABLE (`L-47`'s required deliverable)

Same seed **E-s09**, corrected recipe, **re-rolled**. p06 **OFF** (referent-true, Lap W).

| wave | **OLD** (incumbent) | **NEW** (corrected) | Δ | decoded envelope | inside | degenerate |
|---|---:|---:|---:|---|:-:|:-:|
| 151 | 28 | **28** | 0 | 24–29 | ✅ | |
| 152 | 18 | **17** | −1 | **17–17** | ✅ | ⚑ **EXACT** |
| 153 | 24 | **24** | 0 | 23–24 | ✅ | |
| 154 | 13 | **11** | −2 | **11–11** | ✅ | ⚑ **EXACT** |
| 155 | 18 | **17** | −1 | 16–18 | ✅ | |
| 156 | 19 | **17** | −2 | 14–17 | ✅ | |
| 157 | 21 | **21** | 0 | 15–21 | ✅ | |
| 158 | 33 | **33** | 0 | 27–42 | ✅ | |
| 159 | 9 | **5** | −4 | 5–7 | ✅ | |
| **160** | **5** | **4** | −1 | **4–4** | ✅ | ⚑ **EXACT** |
| **band** | **188** | **177** | **−11** | | **10/10** | **3/3** |

Median **18.5 → 17.0**. Six of ten waves sit below the referent's **minimum** concurrent living
count of 19. **The OLD column reproduces I-21's roster exactly** (`⚑ i21_roster_reproduced: true`),
pinned from its artifact.

**Expected-value side, re-derived from the sidecar at run time rather than typed from the report:**
decoded p06-OFF **172.083** / p06-ON 197.083 / incumbent-OFF 183.583 / incumbent-ON 208.583 — **all
four of Lap V's published totals reproduced**, with `F-8`'s band delta exactly **−11.500**.

---

## 3 — ⚑ THE ISOLATION, AT BODY-IDENTITY GRAIN — AND WHAT IT CONVICTS

Equal counts do not prove equal boards, so the isolation is done on the full
`(spawn_point, name, record, is_champion)` tuple list.

| limb | roster per wave | identity vs incumbent | death | l4l s |
|---|---|:-:|---:|---:|
| incumbent (`roster_fold=None`) | 28,18,24,13,18,19,21,33,9,5 | — | **155** | **161.0612** |
| **`S-CAP-OFF`** (every new term but `F-8`) | **identical, all 10 waves** | ⚑ **IDENTICAL** | **151** | **8.4082** |
| `S-CHAMPFIRST-OFF` (`D-V-3` off, cap on) | 28,17,24,11,17,17,21,33,5,4 | = FULL | 151 | 8.4082 |
| `S-ADJ-OFF` (`D-V-2` off, cap on) | = FULL | = FULL | — | — |
| `S-AMBUSH-OFF` (burst off, cap on) | = FULL | = FULL | **152** | **44.4082** |
| **FULL corrected** | 28,17,24,11,17,17,21,33,5,4 | w151/153/158 identical | **151** | **8.4082** |

> **⚑ `S-CAP-OFF` IS EXACTLY "THE AMBUSH BURST ALONE."** Its roll is identity-identical to the
> incumbent on all ten waves — so `D-V-2` and `D-V-3` are not merely count-inert, they are
> **identity-inert** — and it still dies at 151. **Every fight-level difference it shows is the
> `+4.000 s` burst and nothing else.**

**Wave 151 under the FULL fold is also identity-identical to the incumbent** (28 bodies, 4 of them
p05). Burst offsets `[4.0, 4.0, 4.0, 4.0]`; drip offsets `[4.0, 7.0, 10.0, 13.0]`. That is the
entire delta at the wave where the ladder now ends.

**And it refines my own math note § 7.** I cautioned that a body missing from a later wave "may
have been displaced" by the cap's stream shift rather than capped. **Measured: on every wave where
the count is unchanged the roll is identity-unchanged too** (151, 153, 158) — the cap's
perturbation does not reach waves it does not cap. My caution was right in principle and
conservative in fact, and I am reporting the measurement rather than quietly keeping the caution.

---

## 4 — ⚑ THE CONCURRENCY FUNCTIONAL, GRADED (living bodies inside 11.64 m)

| | referent | `PX-LO` | `PX-HI` | I-21 `PX-LO` |
|---|---:|---:|---:|---:|
| median `t→50 %` | **3.2670 s** | **3.6735** | 6.5306 | 13.7959 |
| median `t→90 %` | **4.9670 s** | **7.1020** | 9.8776 | 15.7551 |
| peak living (w151) | **19–36, median 25** (LOWER bound) | **10** | 10 | 8 |

**The ramp is nearly closed and the crowd is not.** The board now *assembles* at very close to the
referent's rate; it assembles to **10** bodies where the referent shows **19–36**. `S-5` predicted
median peak living stays below 19 — **PASSED** — and wave 160's roster of **4** is short of the
referent's floor by **15**, which no arrival model can repair.

> **⚑ THE TWO FACTS TOGETHER ARE THE ITERATION'S RESULT.** Fold the decoded arrival clock and the
> ramp statistic goes from 13.80 s to 3.67 s against a 3.27 s referent — **and the player dies on
> the first wave.** The board was never too slow. It is too small, and the player cannot survive
> even the small one arriving on schedule. **That points past the roster recipe entirely**, at the
> player's defence/sustain model, and I am naming it rather than folding it.

---

## 5 — THE PRE-REGISTERED PREDICTIONS, GRADED HONESTLY

| id | claim | grade |
|---|---|---|
| **`S-1`** | 10/10 inside envelope; 152/154/160 EXACT at 17/11/4; band ∈ [156, 190] | ⚑ **PASSED, all clauses** (10/10; 17/11/4 exact; 177) |
| **`S-2`** | the fold makes the grades WORSE — T1 does not improve, T4a does not improve | ⚑ **PASSED** (T1 151 ≤ 155; T4a 0.8608 < 0.8848). **Registered against my own interest** |
| **`S-3`** | `F-8` is the only count-mover | ⚑ **PASSED — AS A REPAIRED PASS.** The FIRST BUILD **FAILED** it, and that failure caught `D-I22-1`. Wording NOT rewritten |
| **`S-4`** | the ambush adds nothing and only moves a clock | ⚑ **PASSED** (roster identical; every offset exactly 4.000; 154/155/160 declare no p05) |
| **`S-5`** | the residual survives; median peak living < 19 | ⚑ **PASSED** (10 and 10 against a floor of 19) |

**Mechanical pins:** `P.1` `law_3.moved == {}` on **24** witnesses ✅ · `P.2` fold-off EXACT **6/6**,
scope ∅ ✅ · `P.3` determinism ×2 all three legs, both cells, pass 2 a **real second execution** ✅ ·
`P.4` frozen **20/20** under the hard `SystemExit` gate ✅ · `P.5` no new wave-row key ✅ · `P.6`
smoke **296 pass / 1 pre-existing failure**, unchanged ✅ · `P.7` T4b(c) correctly **not armed** ✅ ·
`P.8` I-18 record artifact KEPT + verified ✅ · `P.9` wall **13/13** with `keys_asserted` on every
row ✅ · `P.10` all four band totals reproduced ✅ · `P.11` count_bounds **139/139** ✅ · `P.12` `F-6`
re-censused from the sim's own pools: **0/139** ✅.

---

## 6 — ⚑ `D-I22-1`: MY OWN DEFECT, CAUGHT BY MY OWN PRE-REGISTERED FALSIFIER

`S-3` predicted that a limb with the `F-8` cap **OFF** would reproduce the incumbent exactly. The
first build returned **190 against 188**, differing at waves 151 and 158 — *with the cap switched
off.* `S-ADJ-OFF` was clean, so the carrier was `champion_first`.

**Mechanism:** running the champion limb first does not change the *multiset* of `rng` calls, it
changes their **ORDER** — so `randint` returns a different `n` from a different stream position.
**The conversion RULE is inert in band exactly as `F-6` says (0/139); the LIMB ORDER is not.**

**And it was the same error I had already diagnosed and written up, applied inconsistently.**
`roster.RAND_ORDER_DISPOSITION` and math note § 2.2 both argue that stream POSITION is not
decode-transferable (MT19937 vs CRT `rand()`, `UNREACHED-V4`). I applied that reasoning to the
body-free rows and violated it everywhere else. **The 178 of the first build was a number produced
by a stream permutation, not by a decoded rule.**

**Repair:** draw the regular count at the incumbent's stream position, then the champion limb, then
emit. Keeps the decoded **rule** (`n − emitted_ch`) and the decoded **emission order** (champions
appended first — list order carries no PRNG dependence, so *that* half IS decode-transferable).
Addendum `9bb524e0` committed **before** the repair. `S-3`'s wording is **not** rewritten.

> **`S-3` was written to falsify Lap V's `F-6` census. It falsified my implementation instead. A
> pre-registration that can only ever convict someone else is decoration.**

---

## 7 — DEFECT TABLE

| id | defect | seam | disposition |
|---|---|---|---|
| **`D-I22-1`** | `champion_first` permuted the RNG stream, moving counts by a PRNG artifact rather than a decoded rule | gamora (mine) | **SELF-CAUGHT** by my own `S-3`. Addendum BEFORE repair; repaired; band roll 178 → 177 |
| **`D-I22-2`** | `S-3`'s wording survives the repair and is **not** restated to match the outcome | gamora (mine) | Recorded as a REPAIRED pass, not a clean one |
| **`D-I22-3`** | the hygiene instrument hashed a file that an earlier crashed execution had already removed — a check that can only ever report `None` | gamora (mine) | **REPAIRED IN-ITERATION**: verifies **from git** when the worktree copy is gone. Both digests match |
| **⚑ commission count error** | `R-PM4-60 part 4 (f)` says "two stale I-18 look-alike files"; measurement says **ONE** — `…105832` is the RECORD artifact `L-46`'s BLOCK re-read | conductor | **REPORTED, NOT EXECUTED.** Removing both would delete the record. One removed, one kept; glob now returns exactly one file |

---

## 8 — SEMANTIC SHIFTS, NAMED (Discipline #12)

1. **`N-1` — `simulate_wave`'s `limb` default `ZONE_FIRST → GATE_FIRST`.** Behaviour-bearing for
   99 call sites. **Blast radius measured before the flip** (296/1 → 295/2); the single new red was
   `test_non_ambush_bodies_do_bend…`, which **asserts the decode-false semantics**. Repaired by
   making that module's fixture **declare** its limb, not by weakening the assertion. `ZONE_FIRST`
   stays reachable as a runnable control. `calibration.py`'s provenance report follows.
2. **`EMPTY_ROSTER_DISPOSITION` DECLARED → DECODED**, both rivals **DECODED-ABSENT**. String
   unmoved. `test_F_9…` renamed and re-asserted against the **new** grade rather than relaxed to
   accept either. **`C-13`'s +11 is STRUCK — the branch that graded better, removed anyway**, and
   kept reachable so the refutation stays runnable.
3. **`P05_DRIP_CADENCE_S` keeps its value (3.0) and loses its reach** — `min(30, |queue|) =
   |queue|` on every declaring wave, so the cadence gates nothing in this band. Re-valuing would
   have been tuning; measuring that it never binds is not.

---

## 9 — UNREACHED CENSUS

| id | what | status |
|---|---|---|
| **`UNREACHED-I22-1`** | per-entry `limitN` values (only their SUM is in the sidecar), so which roster NAME is exhausted first | **OPEN.** Count-inert, identity-live. Named, not modelled |
| **`UNREACHED-I22-2`** | capacity outside 151–160 | **OPEN, and MEASURED VACUOUS this lap** — `n_distinct_uncovered_rows = 0` |
| **`UNREACHED-V3`** | the loader default for an absent `limit` field | INFERRED-WITH-EVIDENCE, not read |
| **`UNREACHED-V4`** | whether the CRT `rand()` count stream is seeded deterministically | **OPEN — and it is the reason the rand-call ORDER is not folded** |
| **`UNREACHED-V2-2`** | the `+4.000 s` offset is `4.000 s + O(1 tick)` | carried as **slop**, never as precision |
| **`UNREACHED-S7`** | the p06 referent-side election | **CLOSED to STRONG by Lap W**, not DECISIVE (§ 10) |
| **`F-4M-1`** | the geometry-identity audit (which spawn entities the map-parse keyed) | conductor's named carry; **does not affect this fold's comparative grades** — geometry is unchanged between recipes |

---

## 10 — ⚑ CAVEATS THAT TRAVEL WITH THE NUMBERS

* **p06 OFF is STRONG, NOT DECISIVE.** The chain is two frame-attested clicks → the "…can do
  better" options never taken → `bonusChest` decoded as a disjoint quest event → **therefore not
  elected (INFERRED)**. The last arrow is an inference. **Falsifier: one artefact —
  `conversations/npc_event_01.cnv` (`matt_to_do` **T17**).** If it lands and contradicts, +25.000
  bodies re-open. The p06-ON arm is **published and never designated** (Lap W § 7.2 forbids
  adopting a fixture limb because it grades better).
* **`UNREACHED-I22-1`** means body IDENTITIES inside a capped pool are not decode-pinned.
* **The `+4.000 s`** carries `O(1 tick)` slop — and since that offset is now the term carrying the
  whole result, the slop matters more this iteration than last.
* **`D-I21-1`** (the sim's player over-travels vs Lap U's referent) is **unrepaired and unmoved** —
  the repair is not decoded.
* **`D-PDEF-2`** (arena walls, `UNREACHED-U4`) stays open; `PLAYER_SANE_BOUND_M` was **not raised**.

---

## 11 — DIGESTS (full 64 hex throughout, `R-PM4-55 part 2`)

### 11.1 Outputs of this iteration

| artefact | sha256 |
|---|---|
| `output/kc2-pm4-i22-findings-20260816_040355.json` | `5cdc6b434ac071d37729b769cd7d52bb9f9d75ecc53f57207cf3865a1c9c104c` |
| `math/kc2-pm4-i22-roster-fold-2026-08-15.md` | `db6fa60d9e95fbd0d3a40e59d2897c590e67e8cc40e09666934decb6c73ed5f8` |
| `math/kc2-pm4-i22-roster-fold-ADDENDUM-2026-08-15.md` | `467913f53543323ce3c866f2cdc68c68079e3eb45c27ec76e2f7cb531ec2836d` |
| `kc2/roster.py` | `75afebb2e725dd8345f48af99db8a637567b2c146036b41e4964791b48cc140c` |
| `scripts/gamora_kc2_pm4_i22_roster_fold_2026_08_15.py` | `aceed206db78d89bc26a1e4b3e22a8c8f09805cbce089f8fe618a2bb89f48cb1` |

### 11.2 Inputs, re-hashed EXACT before use (HALT on mismatch; none fired)

| input | sha256 |
|---|---|
| `lap-v/pm4v_findings.md` | `5450e1567fe58337827c20719ec477ee56a40351cbd7c49ab823d0896ca1b895` |
| `lap-v/pm4v_roster_arithmetic.csv` | `991f75cfdb43ddff06fb01fbd16c81693af020a56f7dfe315e87e11e4db4a93c` |
| `lap-v2/pm4v2_findings.md` | `3aeccfe9ec8b38ba486212ae78e84b1a0aeb3493d838d3d90c5a80ac9601b7c1` |
| `lap-v2/pm4v2_contribution.json` | `9c3b3db20ac8ce2b0f3a3b31adb6161b68990518fcc20ec25f8c306c95a8ac05` |
| `lap-w/pm4w_findings.md` | `96333f0dcae4a5694134ba0c455af84d73b820d036b66920c5ec81cc4709a42c` |
| I-21 findings (the incumbent, pinned to the ARTIFACT) | `d68801c8d03e3c4ceacba7f3936d83625e0eed2c7e18ded0efc92214a990341d` |

### 11.3 I-18 hygiene (L-36 procedure — digests banked in `4dcfc100` BEFORE removal)

| file | sha256 | fate |
|---|---|---|
| `kc2-pm4-i18-findings-20260814_105605.json` | `51a06f32a81c7de02648bfbd53d2a425098b9a08c98b11992c1ec8758ef5449a` | **REMOVED** (re-verified **from git**) |
| `kc2-pm4-i18-findings-20260814_105832.json` | `8cb394607bb2d492a99ba9987a08918902001ff946a0e326d5e3342b874175bd` | **KEPT — the record** |

---

## 12 — ⚑ THE WALL, RE-ARMED (`R-PM4-55 part 3`'s obligation discharged)

**13/13 GREEN, `keys_asserted` on every row.** Re-armed, **not** re-ruled — the run re-opened at
`L-47` and I-22 is the first fold iteration since.

1 fold-off byte identity ×6, scope ∅ · 2 lap substrate EXACT at full 64 hex · 3 frozen 20/20 (hard
`SystemExit`) · 4 Law 3 `moved == {}`, 24 witnesses · 5 `count_bounds` 139/139 · 6 four band totals
+ `F-8` delta −11.500 · 7 envelope 10/10 · 8 degenerate waves EXACT 17/11/4 · 9 `F-6` 0/139 from
the sim's own pools · 10 ambush temporal-only · 11 determinism ×2 three legs · 12 I-18 hygiene ·
13 identity-grain isolation.

**Law 3:** `moved == {}` on **24** witnesses, including `SPAWN_MIN_MODIFIER_GLADIATOR`,
`BASE_ADDITIVE`, `P05_DRIP_CADENCE_S` (**3.0, unchanged**), `P05_GROUP_SIZE` (**30, not modelled as
thirty bodies**), `EMPTY_ROSTER_DISPOSITION`, `P06_OPERATIVE_LIMB`, `D_ENGAGE_M`,
`PLAYER_SANE_BOUND_M` (**not raised**).

---

## 13 — WHAT I RECOMMEND THE CONDUCTOR CONSIDER (mine to state, not to decide)

1. **The roster hole is CLOSED and it was not the residual.** `L-47`'s two named holes are decoded
   and folded; the amendment behaves exactly as Lap V predicted, to the body. The board is now
   decode-true and **still half the referent's size**, and no term inside the decoded recipe closes
   that.
2. **The residual has moved to a seam this fold does not touch:** the player survives 28 bodies
   arriving over 13 s and dies to the same 28 arriving over 4 s. That is a **defence/sustain**
   statement, not a roster or movement statement.
3. **`T17` is now the highest-leverage open item on the roster axis** — it is the only thing that
   can re-open +25 bodies, and it is a host action, not an agent action.
4. **`R-PM4-27 part 3` bites again:** `S-AMBUSH-OFF` grades better than the record cell (44.41 vs
   8.41) **because a decoded limb is switched off**. Published at full size, **not designated** —
   the fourth consecutive iteration where the best number sits on an arm the run may not carry.
