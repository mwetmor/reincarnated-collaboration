# KC2-PLAY · T-A PREREGISTRATION **v1.3** — decision rules, row decisiveness, FAIL taxonomy, denominator law

> ⚑ **STATUS: IMMUTABLE ON COMMIT — v1.3, 2026-09-20. SUPERSEDES v1.2 FORWARD.**
> **v1.2 (`72204f7a`), v1.1 (`30111ac8`) and v1.0 (`5f2c27cf`) are NOT edited.** Superseded readings named in place at **§ A**. **No graded run exists against any version** — the only reason a new version is legal (WARN-16). **Any change after a graded run exists is a HALT to Matt.**
> **Occasioned by:** jack-ryan's **W1 PRE-READ — NO-SEAL on pinning** (`agentic_orchestration/qa/findings/2026-09-20-run-KC2-PLAY-w1-preread.md`, `9e02f5b2`): **BLOCK-1** (the denominator **72** still live in the normative gate text, the executable constant, and the prereg's own pinned governing companion) · **WARN-1** (v1.2 carried a stale galadriel pin **inside the change table that re-pinned the other companion**) · **WARN-5** (§ F.2a's headline, read literally, is **false of the oracle**).
> **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1. **Decision rules only. NO WIDTH IS TRANSCRIBED HERE.**

### ⚑ PINS — all four derived this session by `shasum -a 256`, never retyped from a prior document

| # | artifact | **sha256** | what moved |
|---|---|---|---|
| **P-a** | `agentic_orchestration/gamora/notes/2026-09-20-kc2-play-ta-band-widths.md` — **the governing width file** | **`1c971da9d5f1e1cb3385965e44c38a6a32d1d3f24fdd260757bea748b0d0a121`** | ⚑ **Addendum 3** (`16d1b6a7`) — § E-3's coverage rule restated **72 / 72 → 89 / 89**. v1.2 pinned `6709cfe6…` (pre-Addendum-3) |
| **P-b** | `agentic_orchestration/galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values-and-u-rider.md` | **`8186202cc0c78ae9ef428c57164fac35bd1adb0e14ec5310c395783361653158`** | ⚑ v1.0–v1.2 all pinned `0411e6b8…`, the **pre-`b3f175ff`** state (WARN-1) |
| **P-c** | `agentic_orchestration/galadriel/notes/2026-09-20-kc2-play-w1-tb-expected-values.json` | **`a8b85331764ba3fe90f45cf7cd6f1a25f6dc0dae4a7e7fa555c487f0b153ea0b`** | ⚑ **NEW — consumed and pinned nowhere until now** |
| **P-d** | `agentic_orchestration/galadriel/notes/2026-09-20-kc2-play-w1-tb-release-labels.json` | **`15dace604c8d5bb4888223a8b25a07a038bae44431ebd194d682545c0f29c58a`** | ⚑ **NEW — consumed and pinned nowhere until now** |

**Sealed cells (hash-verify only, never opened — K-7):** `[M-POL2]` `ad61ad2a8c799d6e` / 123,564 B · `[MECH]` `20b05cb4ef3bd888` / 2,125,271 B · `[W1W]` `7a992c81ca6e56e5` / 403,084 B. **Lifted rows:** `e0117429…`.
**Companion register:** `2026-09-20-kc2-play-divergence-register-v0.2.md`.
**Next gate:** jack-ryan re-check — *"a sha diff on four files. Minutes."*
**Counts:** 2 preconditions · **23 EXACT** · **14 BAND ids — 6 COUNTED · 4 REPORTED-NOT-COUNTED · 0 CONDITIONAL · 4 UNGRADEABLE-DECLARED** · 2 emitted-not-graded.
**Standing law:** Law 3 · K-7 · D4 · GL-6 / GL-12 · Discipline #72 · R-L91-4 · D-MPOL2-2 · R-L89-4 · digests **derived at use, never retyped**.

---

## § A · CHANGE TABLE — v1.2 → v1.3

| # | clause | v1.2 | **v1.3** | reason | finding |
|---|---|---|---|---|---|
| 1 | **width-file pin** | `6709cfe6…` | ⚑ **`1c971da9…`** (P-a) | **Addendum 3 restates § E-3 at 89 / 89.** The prereg pins this file *by sha* and declares it **governing** — so at `6709cfe6…` the governing text said **72**, and P-1 could not go green against the artifacts as they stood | **BLOCK-1** |
| 2 | **galadriel note pin** | `0411e6b8…` (carried unchanged from v1.0) | ⚑ **`8186202c…`** (P-b) | the pinned digest is the **`10a85641`** state; the note was amended at **`b3f175ff`**. ⚑ **v1.2's own § A row 7 re-pinned the *width* file for exactly this class of reason and left this one stale** — with KP-10 (the amendment) two ledger rows above the commission. **Content-innocent for the prereg** (everything § C.4 uses — `LIVE-MAX`, 42.84 %, 39.76 %, the 181.0 / 182.65 s windows — is present at the old sha); what was compromised is **the pin discipline the whole immutability argument rests on** | **WARN-1** |
| 3 | **the two consumed JSONs** | ⚑ **pinned nowhere** | ⚑ **PINNED** — P-c, P-d | a consumed artifact with no pin is outside the immutability guarantee entirely | BLOCK-2 (register), applied here for symmetry |
| 4 | **§ F.2a headline** | *"The word `round` must not appear anywhere on the threat path."* | ⚑ **"No bare `round(` may appear on THE PORT'S threat path."** Plus an explicit sentence: **the oracle's Python threat path uses `int(round(…))` at all four LIVE sites, and that built-in's rule — half-to-even — is precisely what the port must reproduce EXPLICITLY** | ⚑ **read literally, the v1.2 headline is FALSE OF THE ORACLE.** The table directly beneath it shows `int(round(…))` at all four sites; the disambiguating clause (*"a source scan of the built runtime"*) sat sixteen lines later. **A builder or grader scanning `threat.py` against the headline reds a correct oracle** | **WARN-5** |
| 5 | **P-1 denominator** | 89/89 throughout | **89/89 throughout — VERIFIED, and the verification recorded** (§ B.2) | BLOCK-1 asks that no live-tense **72** survive. Swept: this file's only occurrences of the digit-string `72` are **Discipline `#72`** (a rule id) and the substring inside **`47.072`** (the box-scatter reach). ⚑ **No live-tense coverage `72` exists in v1.2 or in this file** — the prereg was never the defect; its *pinned companion* and the *charter* were | **BLOCK-1** |
| 6 | **the cap's trip condition vs the charter's** | § G **C3** = *"coverage not **89/89**-mapped"*; charter § 4.4 still reads *"coverage < **72/72**-mapped"* | ⚑ **Stated explicitly: for the T-B cap, THIS PREREG GOVERNS at 89/89.** The charter clause is **superseded-pending-annotation**, and the annotation is KP-9 propagation, not a new ruling | **two trip conditions for one cap** is the defect; a cap with two thresholds has none. The grader reads the prereg (§ G names the verdict file as its input), so naming the governing text closes it *for the harness* while the charter edit travels | **BLOCK-1** |

**Not mine, recorded so the seal can see the whole of BLOCK-1:** charter § 4.3 / § 4.4 / § 3 F1 / § 9 forward-annotation to **89** (conductor) · `kc2rt_coverage.gd:48` `CHARTER_DENOMINATOR := 72` → **89**, and re-emit the transcript (drax) · charter **L4** *"two known-bad limbs"* → **ONE** (WARN-2; the register's rewritten handoff sentence already governs).

---

## § B · CONFIGURATION AND PRECONDITIONS

### B.1 · `ORACLE` — v3.2 `V0`, five arms, five salts

`V0` carries five `V0-ARM-*` rows — `M0`, `M-POL-2`, `M-POL-2-NULL`, `W1`, `W1-NULL` — each a **DELTA against the base row set, never a second full copy**. **5 arms × 5 salts = 25 headless runs**, each arm the base set with **exactly one fold moved**: that single-fold delta is the entire reason the inertness relations are readable, and it is why `W1-NULL` returns to **`M-POL-2`** rather than to `M0` (`TA-X-04`).

Limbs of record include `spawn_fold: POLAR_UNIFORM_RHO` · `sustain: COUPLED` · `intake: ARMOUR_THEN_RESIST + global_flat` · `summons: PRESENT_INERT + offense MEASURED_BASIC` · `arena_fold: None` (armed only in `W1`) · `interrupts_fold: None` · **`WarCryLimb.COOLDOWN` (7.5 s)** · **`PotionLimb.TRACE_CONSISTENT` (θ 0.22972972972972974)** · `CritLimb: LO` · `p06: OFF` · **`PhaseModel: ENGAGE`** (`TA-X-24`).

**The runtime prints its RESOLVED limb set into the verdict header (`v0_limb_set`), diffed line-by-line against `V0` before any row is read; it refuses to boot on an unset limb rather than defaulting one.** ⚑ *"Is X wired?" is a driver fact a module default cannot answer* — the reason four of this run's corrections were caught by `V0` within one wave.

**Pilot:** scripted — `DRIVE_TO_PACK` + the M-POL-2 channel policy; `v_ref = 4.0` is a DECLARED-FREE-PARAMETER → 5.4 m/s; **no facing model**.

### B.2 · P-1 · COVERAGE — **89 / 89**, and the verification

All **89 enumerated census row ids** mapped **mechanically** (`kc2_runtime/loader/kc2rt_coverage.gd` carries the id list) to exactly one of `IMPLEMENTED` · `DIVERGENCE(DIV-nn)` · `RUNTIME-CHOICE(absent_ref)` · `OUT-OF-SCOPE`. **Counts sum to 89. Zero unmapped.** T-A does not run until green; **every band prints `value @ coverage k/89`**; graded as `TA-X-02`.

⚑ **Why 89 and not 72, stated once so the gate never has to re-litigate it:** the census's `17 / 41 / 14 = 72` is a **class-share headline taken after collapsing ~a dozen genuinely split rows to their primary class** — and *the note never records which id collapses into which*. **No rule reproduces 72 from the tables.** A mechanical gate keyed to 72 asks the runtime to map to a denominator that **cannot be reconstructed from the document that defines it**. The **89 enumerated ids govern** (M 23 · D 19 · P 7 · K 26 · W 14); the 72 survives as a headline and **is not a gate**.

⚑ **Sweep recorded (BLOCK-1):** the only occurrences of `72` in this file are **Discipline `#72`** and the substring in **`47.072`**. No live-tense coverage `72` survives here, and none survived in v1.2 either — **the prereg was never BLOCK-1's defect; its pinned companion and the charter were.**

### B.3 · P-2 · STREAM DISJOINTNESS — and what it does not cover

**Probe:** run `M-POL-2` salt 0 twice, once with a **no-op fold inserted that draws zero values**; assert identical digests. **COVERS** stream isolation at *fold* granularity — exactly what `TA-X-03…06` need; a port sharing one RNG across sites would red all four **with every rule implemented correctly**.

⚑ **DOES NOT COVER:** (1) that the port's draw sites are the **same sites in the same order** — a null-fold probe is not a site census, and V9's registry is **29 live sites across 11 streams** (+2 NOT-LIVE); (2) ⚑ **the BOARD ROLL** (§ E trap 6); (3) whether the per-site assignment is *lifted* or *chosen* — if `V9` is not consumed it is a RUNTIME-CHOICE ledger row and the report says so.

**P-2 red → `TA-X-03…06` UNGRADEABLE → `INDETERMINATE` → the cap trips.**

---

## § C · THE DENOMINATOR LAW, STATED ONCE

```
D_constructed = CHANNELLING + CHANNELLING_AND_MOVING + MOVING + IDLE      (PRE_FIGHT and DEAD excluded)
```
Verified on the seal: pooled `287 + 2211 + 166 + 119 = 2783 = D`; the per-salt sum equals the pooled sum, so the partition is exact at both grains. ⚑ **No sealed artifact carries `D`. It is CONSTRUCTED.**

**Two identities, 5/5 on the seal, graded as `TA-X-08`:** `n_player_ticks_observed = D + PRE_FIGHT` · `n_channelling + n_released = D` ⇒ `uptime + n_released/D = 1.000000` exactly.
⚑ **The seal publishes `release_duty` on `D + PRE_FIGHT`** (key `⚑ release_duty_on_observed_ticks`): `23/106 = 0.2169811 = 1 − 0.7830189` on `D`, against `23/107 = 0.2149533` on `D + PRE_FIGHT`. **The 0.215-vs-0.217 tell resolves entirely to a denominator difference. Every rate row here divides by `D` and by nothing else.**

**C.2 · Pooled vs mean-of-salts.** Every band is on the **MEAN-OF-SALTS**; a port's pooled figure is **never** compared against these bands. `D` per salt is **[1084, 305, 106, 185, 1103]** — a **10.4× span**. On the plant ratio the pooled/mean gap consumes **38 % of the whole tolerance** by choosing the wrong one of two numbers that share a name.
**C.3 · The graded object** is the **mean of a NEW 5-salt run**; the interval is a **prediction interval** carrying both runs' sampling error; `ddof = 1`; `half-width = t(0.975, df=4) · s · √(2/5) = 1.755978 · s`. All widths live in **P-a**.
**C.4 · T-B denominators are NOT these** (from **P-b**). HP occupancy on **`LIVE-MAX`** reproduces **42.84 %**; NOMINAL gives **39.76 %** — **3.08 pp with no fight in it**. HP window **181.0 s**; energy / motion / release / cast **182.65 s**.

---

## § D · ROW-ID CONCORDANCE — the single namespace

⚑ **Every citation uses the `TA-` id; a width is looked up by STATISTIC NAME in the table named "governs", never by a bare `B-n`.**

| **canonical** | statistic | gandalf v1.0 | gamora § 2.4 | gamora Add. 1 | **width governs (in P-a)** |
|---|---|---|---|---|---|
| `TA-B-01` | terminal wave | B-1 | B-1 | — | § 2.4 · **REPORT-ONLY** |
| `TA-B-02` | **uptime** on `D` | B-3 | **B-2** | **B-4** | ⚑ Add. 1 restatement |
| `TA-B-03` | `frac_moving` on `D` | B-4 | B-3 | B-3 | Add. 1 restatement |
| `TA-B-04` | `P(chan \| moving)` | B-5a | B-4 | B-5a | Add. 1 restatement |
| `TA-B-05` | `P(chan \| stationary)` | B-5b | B-5 | B-5b | Add. 1 restatement |
| `TA-B-06` | plant ratio (window 5.0 s) | B-8 | B-6 | B-6 | Add. 1 restatement |
| `TA-B-07` | release duty on `D` | B-7 | B-7 | B-7 (restated) | Add. 1 · **reported-not-counted** |
| `TA-B-09` | **channel split** | *(nominated v1.1)* | — | — | ⚑ **Addendum 2 § B2** |
| `TA-X-03…06` | inertness / distinctness | E-2, E-3, E-4 | **E-1 (a–d)** | A4 | — |
| `TA-X-07` | conservation, 7 terms | E-5 | **E-2** | — | — |
| `TA-X-02` | coverage | E-1 | **E-3** ⚑ *at 89/89 per **Addendum 3*** | — | — |
| `TA-X-08` | denominator identity | *(implicit)* | **E-4** | A1 | — |
| `TA-X-11` | wall-clamp zeros | E-7b | — | **A2** | — |

*The uptime row remains the reason this table exists: **B-3 · B-2 · B-4 — three ids, one statistic, two files.***

---

## § E · ⚑ OUTSIDE T-A'S REACH — the catching-row audit

| # | trap | **caught by** | verdict |
|---|---|---|---|
| **1** | **V5-GUARD-2** — arrival `px, py` are **TELEMETRY ONLY**; hit-testing with them silently builds sibling **S1** inside the T-A config | `TA-X-19` (a port folding misses into `voided` would balance the seven-term books and hide it from `TA-X-07`) | **CLOSED** |
| **2** | **V9-DEAD-2** — the retired square-box scatter draws at the **same stream position** as the live polar draw; **invisible to a digest** | `TA-X-17` + `TA-X-18` (direct, every arm); `TA-X-10`/`TA-X-11` indirectly in the W1 arms | **CLOSED** |
| **3** | **V17** — `hit_test_model = "point"` in the pack vs the sim's **uniform 3.0 m disc** | `TA-X-20` for the **resolved predicate**. ⚑ **`R2D-5` still owns the DRAWN radius; a green T-A does not clear that half** | **HALF-CLOSED — declared** |
| **4** | **V4-LAW-1** — the cadence law is **not RNG-neutral** | `TA-X-21` — four sites, banker's, per-site rule table, negative assertion (§ F.2a) | **CLOSED** |
| **5** | **V18 + V19** — flag **AND** coin = the 0.15 applied twice | `TA-X-22` | **CLOSED** |
| **6** | ⚑ **THE BOARD ROLL** | ⚑ **NONE.** `TA-X-23` is **STRUCK, never minted, id retired.** Both seals carry **no roster counts by class**; `[W1W]`'s `n_spawn_placements` is a **placement TOTAL** that catches a gross count error and **nothing about composition**. `L-49`: the recorded composition **validates, it does not spawn** | **OPEN — DECLARED** |
| **7** | the attack-**PHASE** model — `HASH` is the module default, `ENGAGE` the driver of record; both deterministic, so **no band and no digest sees the difference** | `TA-X-24` | **CLOSED** |

⚑ **Trap 6, for the report's face:** **12 of the 29 live draw sites are the board roll.** It is the mechanism most likely to be rewritten from scratch in GDScript; **its divergence shows as a different SET of monsters, not a different number; and T-A cannot see it at all.** Closure is **a sibling that emits per-wave class counts**, not a T-A row.

**Also outside reach:** per-site draw localisation (S5 out of scope — at **29** sites the ceiling is *lower* than the charter assumed) · the tick-resolution HP trace · every `DIV-nn` row, by construction.
⚑ **And the limit on `TA-X-11` that must not be over-read:** the oracle's clamp counters are **structural zeros** — the wall never binds (margin `43.758085 − 43.404802 = 0.353283` m = **0.807 %**). `TA-X-11` says *"the port never needed to clamp"*, **not** *"the port's wall works"*; **a port with no wall at all also scores zero.**

---

## § F · THE GRADED ROWS

### F.1 · Decisiveness classes

**EXACT** — identity, invariant, count, or declared-precision reproduction; a red says **the port is wrong**; may carry a **NUMERICAL** tolerance, **never a STATISTICAL one**.
**BAND** — distributional at n = 5; **individually and collectively non-decisive**. Forms: `INTERVAL` · `RATIO` · `ORDERING`.
⚑ **No width is defaulted.** ⚑ **Cross-implementation rows are NOT salt-paired**; **inertness rows are salt-paired within the port.**

### F.2 · EXACT rows — **23**

| id | statistic | basis | tolerance |
|---|---|---|---|
| `TA-X-01` | port self-determinism — any arm/salt run twice → identical digest | run-internal | byte-exact |
| `TA-X-02` | **coverage 89/89**, zero unmapped | the census id list | integer |
| `TA-X-03` | inertness A — `port(M-POL-2-NULL, s) ≡ port(M0, s)`, all 5 | `[M-POL2] ⚑ arms` | byte-exact |
| `TA-X-04` | inertness B — `port(W1-NULL, s) ≡ port(M-POL-2, s)`, all 5 ⚑ **not M0** | `[W1W]` | byte-exact |
| `TA-X-05` | distinctness C — `port(M-POL-2, s) ≢ port(M0, s)`, ≥ 1 salt | `[M-POL2]` | exact, one-sided |
| `TA-X-06` | distinctness D — `port(W1, s) ≢ port(M-POL-2, s)`, ≥ 1 salt | `[W1W]` | ⚑ **RELATION ONLY, never magnitude** — `Q.10`: one salt, five waves, two suppressed ticks, fold **exonerated** |
| `TA-X-07` | **conservation — SEVEN terms** `offered = applied + dropped + voided + pool_truncated + pcl_reclaim + counterplay_absorbed` | run-internal | **`1e-6`** ⚑ a live driver assert-wall in this repo checks **six**, omitting `counterplay_absorbed` |
| `TA-X-08` | denominator identity, both sub-identities | `[M-POL2]`, 5/5 | exact |
| `TA-X-09` | all **9** `math_rules.test_vectors` | the pack | per-vector |
| `TA-X-10` | containment supremum `max_body_radius_m ≤ 43.758085029822276` (W1) | `[W1W] ⚑ wall` | exact, ≤ |
| `TA-X-11` | wall-clamp zeros — `n_wall_clamps_{player,body} == 0`, every W1 arm | `[W1W] ⚑ pools/per_arm` | integer |
| `TA-X-12` | pool inertness under ORACLE — total pool damage `== 0.0` | `[W1W] ⚑ pools` | exact |
| `TA-X-13` | no player crit | `V0 · CritLimb LO` | integer |
| `TA-X-14` | the two DO-NOTs (`cause == "energy"` → 0; no release-on-every-cast) | pack prohibitions, R2D-4 | integer |
| `TA-X-15` | release-schedule negative — p01–p04 at `t = 0.0`, p05 one burst at `t = 4.000 s`, no intra-point stagger | census M4 / `V11` | exact |
| `TA-X-16` | p06 OFF | `V0` ⚠ code default disagrees | integer |
| `TA-X-17` | spawn offset — `‖spawn_xy − anchor_xy‖ ≤ 8.0` m, every body, arm, salt | `ρ = 8.0·u₂`; box reaches **11.313708 m**; **21.46 %** of box draws exceed 8.0 (`1 − π/4`) | exact, ≤ |
| `TA-X-18` | **scatter-law three-law discriminator** — feed `u₁ = u₂ = 0.5`, assert **`(−4.0, 0.0)`** | polar → `(−4.0, 0)` · uniform-in-area → `(−5.656854, 0)` · box → `(0.0, 0.0)` | exact |
| `TA-X-19` | arrival unconditionality — every queued arrival with a live caster in a live wave **is applied**; arrivals suppressed for **any position-dependent reason = 0**; **no damage predicate reads an arrival's `px, py`** | `deferred_arrival.py:13-17` | integer |
| `TA-X-20` | player hit-test predicate — 2.99 m hit / 3.01 m miss; **no angular gate** (3.0 m *behind* is hit); **no target cap** (12 inside → 12 hits) | census D7 (`disc.py:123-154`, MEASURED-ABSENT 4/4) | exact |
| `TA-X-21` | **quantisation rule per site** — § F.2a | `threat.py`, `deferred_arrival.py`, `dot_timeline.py`, `control_application.py` | exact |
| `TA-X-22` | flag-off release cause under ORACLE — `cause == "interrupts_channel_flag"` occurs **0** times | `V0 · interrupts_fold: None`; V18+V19 | integer |
| ~~`TA-X-23`~~ | ~~board-roll composition~~ | ⚑ **STRUCK at v1.2 — outside T-A's reach. Id retired, never re-used** | — |
| `TA-X-24` | **attack-phase model is `ENGAGE`** — a body entering its own max reach at tick *T* takes its opportunity at tick *T*; **`sha256(actor_id) mod n` is never evaluated** | `V0` carries `PhaseModel.ENGAGE`; `run.py:696` and `threat.py:1246` carry `PhaseModel.HASH` as the **DEFAULT**; `threat.py:1419-1420` in the module's own words: *"the run brackets them (`HASH` vs `SPAWN`) and takes the zero-parameter reading (`ENGAGE`) as the limb of record"* | exact |

#### F.2a · ⚑ `TA-X-21` — THE QUANTISATION RULE, PER SITE

> ⚑ **No bare `round(` may appear on THE PORT'S threat path.**
> **The oracle's Python threat path DOES use `int(round(…))` at all four LIVE sites — and that is the point, not a contradiction.** Python's built-in `round` on a float is **ROUND-HALF-TO-EVEN**, and **that rule is what the port must reproduce EXPLICITLY**, because **GDScript's `round()` rounds half AWAY FROM ZERO** (`round(2.5)` → **2** in Python, **3** in GDScript). A port that writes `round(` inherits the wrong rule silently; the oracle that writes `round(` inherits the right one. *The assertion is about the port's source, never the oracle's.*
> ⚑ **And the cost is not one tick.** The swing period sets `is_opportunity`, which sets **how many `choose_slot` calls draw** — so a bare GDScript `round()` **desynchronises the threat RNG stream** (V4-LAW-1).
> **Corroborated by the seal:** the M-POL-2 fold's `⚑ quantisation_error` block states it in its own words — *"round-half-to-EVEN to the nearest whole tick (Python's `round`)"*. `threat.py` imports `csv, hashlib, math, random, dataclasses, enum, functools, pathlib, typing` — **no `numpy`, no `decimal`**, so the built-in is the one in play.

| site | expression (oracle) | **rule the port implements** | graded |
|---|---|---|---|
| `threat.py:1402` | `max(1, int(round(per / mult * ticks_per_s)))` — **the cadence law** | ⚑ **HALF-TO-EVEN, explicit** | **vector** |
| `threat.py:1522` | `max(1, int(round(s.delay_s * ticks_per_s)))` — first-cast gate | ⚑ **HALF-TO-EVEN, explicit** | **vector** |
| `threat.py:1555` | `tick + max(1, int(round(cd * ticks_per_s)))` — slot cooldown | ⚑ **HALF-TO-EVEN, explicit** | **vector** |
| `threat.py:1867` | `tick + max(1, int(round(r.dot_duration_s * ticks_per_s)))` — DoT expiry | ⚑ **HALF-TO-EVEN, explicit** | **vector** |
| `deferred_arrival.py:330` | `int(math.ceil(raw))` — arrival tick | **`CEIL`**, half-insensitive (`:329`'s `round` is gated behind `QuantLimb.ROUND`, **not of record**) | assert `CEIL` |
| `dot_timeline.py:380` | `int(exact) if TRUNCATE_NTICKS else …` | **`TRUNCATE`** — `R-DOT-2` truncates, never rounds | assert `TRUNCATE` |
| `control_application.py:591` | `max(0, int(exact) if TRUNCATE_BUCKETS else …)` | **`TRUNCATE`** | assert `TRUNCATE` |
| `counterplay.py:212` | `int(round(x * BAR_PX))` | presentation quantisation — **not on a damage path** | not graded |

**Vectors at each of the four LIVE sites:** `n_raw = 8.5 → 8` · `10.5 → 10` · `2.5 → 2`. *(GDScript's `round` returns 9, 11, 3 — every one discriminates.)*
**Negative assertion:** a source scan **of the built port** finds **zero** bare `round(` calls on the threat / cadence / arrival path; every quantisation site names its rule.

### F.3 · BAND rows — **14 ids**

| id | statistic | sub-class | width (in **P-a**) |
|---|---|---|---|
| `TA-B-09` | **channel split** `CHANNELLING / (CHANNELLING + CH_AND_MOVING)` | ⚑ **COUNTED · INTERVAL — the strongest BAND row T-A has** (its `s` is **less than half** `TA-B-03`'s; and the split is a ratio *within* the channelling population, so the 10.4× `D` span barely touches it) | **Addendum 2 § B2** |
| `TA-B-03` | `frac_moving` on `D` | COUNTED · INTERVAL — second | Add. 1 restatement |
| `TA-B-02` | uptime on `D` | COUNTED · INTERVAL — weak, **clips at 1.0; a one-sided band is half a test** | Add. 1 |
| `TA-B-04` | `P(chan \| moving)` | COUNTED · INTERVAL — weak, clips at 1.0 | Add. 1 |
| `TA-B-05` | `P(chan \| stationary)` | COUNTED · INTERVAL — weak; small stationary population | Add. 1 |
| `TA-B-06` | plant ratio (window 5.0 s) | COUNTED · INTERVAL — weak, **§ C.2-fragile** | Add. 1 |
| `TA-B-01` | terminal wave | **REPORT-ONLY** — its band **admits every arm in the seal, including the G5 control** | § 2.4 |
| `TA-B-07` | release duty on `D` | **REPORTED-NOT-COUNTED** — `s` byte-identical to uptime's; `released/D ≡ 1 − uptime`. **One row with a sign flip; never counted twice** | Add. 1 |
| `TA-B-08` | ordering `P(chan\|moving) > P(chan\|stationary)` | **REPORTED-NOT-COUNTED** — implied by `TA-B-04 ∧ TA-B-05`; retained because it **survives a denominator dispute that would void both** | none |
| `TA-B-14` | `n_avoidance_vetoes`, `n_pool_occupancy_ticks` | **REPORTED-NOT-COUNTED** — oracle values 0–2; bands-not-tape means a port with its own stream will not reproduce a small integer | none |
| `TA-B-10` | per-wave durations | ⚑ **UNGRADEABLE-DECLARED** · T-B-only | — |
| `TA-B-11` | arrival latency / co-arrival / `n_deferred` | ⚑ **UNGRADEABLE-DECLARED** — absent from both seals; `[MECH]` is a different arm. ⚑ **The internal half survives: `TA-X-07` gates the arrival machinery on conservation, not latency** | — |
| `TA-B-12` | intake by wave and damage family; leech per tick | ⚑ **UNGRADEABLE-DECLARED** | — |
| `TA-B-13` | `max_body_radius_m` (W1) | ⚑ **UNGRADEABLE-DECLARED** — an **extreme, not a mean**; the sample is **degenerate** (4 of 5 salts identical); **its t-band rejects the oracle's own maximum.** Power carried one-sidedly by `TA-X-10`/`TA-X-11` | — |

**Sub-class counts: 6 COUNTED · 4 REPORTED-NOT-COUNTED · 0 CONDITIONAL · 4 UNGRADEABLE-DECLARED = 14.**

> ⚑ **THE REPORT-FACE SENTENCE:** **"The verdict's weight sits on the 23 EXACT rows and on `TA-B-09` / `TA-B-03`. Every other BAND row is corroboration."**

### F.4 · Emitted, not graded

Per-registered-site draw counters (**29 sites**; they localise nothing without S5) · the tick-resolution HP trace.

---

## § G · FAIL TAXONOMY AND THE T-B QUOTING CAP

| verdict | antecedent | consequence |
|---|---|---|
| **`STRUCTURAL`** | **≥ 1 EXACT row RED** | port is wrong; **no W4 until repaired**; cap **TRIPS**; **two graded runs against v1.3 both STRUCTURAL → HALT to Matt** |
| **`INDETERMINATE`** | 0 EXACT red, **≥ 1 EXACT UNGRADEABLE** (incl. P-1 or P-2 red) | cap **TRIPS**; does **not** increment the two-attempts counter |
| **`STATISTICAL`** | all EXACT green; **≥ 1 COUNTED BAND row RED** | a **finding**; handoff proceeds; cap does not trip |
| **`PASS`** | all EXACT green; no counted BAND red | **`PASS @ coverage k/89, n/6 counted band rows graded`** — never unqualified |

**Order:** `STRUCTURAL → INDETERMINATE → STATISTICAL → PASS`, stop at the first hit. **A BAND row can never outrank an EXACT row in either direction.** UNGRADEABLE is orthogonal. **A GRADED RUN** = one execution of the 5 × 5 matrix producing a conforming verdict file; a port repair between attempts does not reset the counter. **No post-hoc widening, by anyone** (A-3; L-88).

**Verdict file** `kc2play.ta_verdict.v1` — `prereg_version: "v1.3"`, `prereg_sha256` of this file, `band_widths_sha256` **`1c971da9…`**, `galadriel_note_sha256` **`8186202c…`**, `galadriel_expected_values_sha256` **`a8b85331…`**, `galadriel_release_labels_sha256` **`15dace60…`**, `register_sha256` (v0.2's machine form), `preconditions.P1_coverage {"mapped":89,"total":89,"unmapped":0}`, `v0_limb_set` diffed against `V0`.

**Cap — three refusal conditions:** **C1** verdict file absent / unparseable / any pinned sha mismatched · **C2** `verdict ∈ {STRUCTURAL, INDETERMINATE}` · **C3** ⚑ **coverage not 89/89-mapped — and THIS PREREG GOVERNS the threshold** (charter § 4.4's `72/72` is superseded-pending-annotation; **a cap with two thresholds has none**).
**"A fidelity figure"** (mechanical): a row pairing a twin statistic with a referent statistic; or a ratio/percentage/delta/residual/score between them; or `fidelity`/`faithful`/`accuracy`/`match`/`agreement`/`% of referent` in a label.
**Degraded behaviour:** raw twin-side statistics only, each with its own denominator and window; a **banner before** the statistics naming the condition; **non-zero exit**. Composes with R2D-10.

---

## § H · OPEN QUESTIONS — one lean each

**OQ-1 · The cap now has one governing threshold (89/89) and the charter still prints another.** → **Annotate charter § 4.3 / § 4.4 / § 3 F1 / § 9 forward to 89 in the same strike-through form S-2 already carries, and do it before the seal re-check.** It is **KP-9 propagation, not a new ruling — no Matt.** § A row 6 closes it *for the harness*; leaving the charter unannotated leaves the run's own top-level document contradicting its preregistration, which is Discipline #73 with a second lap.

**OQ-2 · `kc2rt_coverage.gd:48` still holds `CHARTER_DENOMINATOR := 72` and the transcript prints `COVERAGE RED | mapped 0/89 (charter pins 72)`.** → **Rename it `CENSUS_DENOMINATOR := 89` and retire the disagreement branch entirely.** The constant's *name* is half the defect: it asserts the charter as the authority for a number the **census** enumerates, which is what let the two drift. drax's escalation was right and the answer did not reach his file.

**OQ-3 · The skeleton emits 9 divergence rows against the register's 23.** → **Leave the § F mismatch → `COVERAGE FAIL` at P-1 armed, and expect it to fire at T-0.** It is the right catch working; naming it now means it is met as a scheduled event rather than a surprise. The emitter fills at W3.

**OQ-4 · `M-POL` (G5) is in the seal and not in the arm set** *(carried, still open)*. → **Leave it out.** The third inertness relation is not runnable at five arms, and a sixth arm buys one distinctness row against an arm the run is not porting.

**OQ-5 · `TA-X-20` half-closes V17** *(carried, still open)*. → **Adopt both halves and print the split:** `TA-X-20` clears the resolved predicate, `R2D-5` clears the drawn radius, and a green T-A clears only the first.

---

*Filed 2026-09-20 by gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1, Run KC2-PLAY. **v1.2 / v1.1 / v1.0 not edited; superseded readings named in place at § A.** **All four pins derived this session by `shasum -a 256`, never retyped.** **No width transcribed.** **K-7 held** — the three sealed cells were reached by digest and byte count only. **Law 3 held.** No production code, no dispatch, no push.*
