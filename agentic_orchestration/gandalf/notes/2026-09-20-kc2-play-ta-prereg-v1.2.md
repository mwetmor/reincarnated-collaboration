# KC2-PLAY · T-A PREREGISTRATION **v1.2** — decision rules, row decisiveness, FAIL taxonomy, denominator law

> ⚑ **STATUS: IMMUTABLE ON COMMIT — v1.2, 2026-09-20. SUPERSEDES v1.1 FORWARD.**
> **v1.1 (`30111ac8`) and v1.0 (`5f2c27cf`) are NOT edited and not deleted.** Superseded readings named in place at **§ A**. **No graded run exists against any version** — the only reason a new version is legal (WARN-16). **Any change after a graded run exists is a HALT to Matt.**
> **Occasioned by:** charter ledger **KP-13** — gamora's three pre-seal reads (band-widths **Addendum 2**, `5cd34a75`).
> **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1. **Decision rules only. NO WIDTH IS TRANSCRIBED HERE.**
> ⚑ **Companion, CROSS-PINNED BY SHA — RE-PINNED AT v1.2:** `agentic_orchestration/gamora/notes/2026-09-20-kc2-play-ta-band-widths.md` — **sha256 `6709cfe6f7427068226f6af8a9cc98668b3018194403cfe82eeb3310c26aade9`** (body `a2150122` + Addendum 1 `b1210565` + **Addendum 2 `5cd34a75`**). *v1.1 pinned `a7984b79…`, which is the pre-Addendum-2 file; that pin is superseded, not wrong.* Every width is **looked up there, by statistic name, in the table § D names as governing.** **Derived at read time, never retyped.**
> **Also consumed:** galadriel W1 T-B + `u` rider — sha256 `0411e6b805e2baa9df19497683340a59385eb27973cfad125cb656548c0c711f`.
> **Counts:** 2 preconditions · **23 EXACT** (22 carried + 1 added at v1.2, § A row 6) · **14 BAND ids — 6 COUNTED · 4 REPORTED-NOT-COUNTED · 0 CONDITIONAL · 4 UNGRADEABLE-declared** · 2 emitted-not-graded.
> **Next gate:** jack-ryan pre-reads **this file + both width files = the W1 seal.**
> **Standing law:** Law 3 · K-7 · D4 · GL-6 / GL-12 · #72 · R-L91-4 · D-MPOL2-2 · R-L89-4 · digests **derived at use, never retyped**.

---

## § A · CHANGE TABLE — v1.1 → v1.2

| # | row / clause | v1.1 | **v1.2** | reason | ledger |
|---|---|---|---|---|---|
| 1 | **`TA-X-23` board roll** | proposed at v1.1 **OQ-1** as a conditional EXACT row, pending one read | ⚑ **STRUCK. Never minted. The board roll is OUTSIDE T-A'S REACH, DECLARED** (§ E trap 6). **The id `TA-X-23` is retired and never re-used.** | Both seals swept for `roster` / `n_bodies` / `n_regular` / `hero` / `nemesis` / `champion` / `composition` / `n_spawn`: `[M-POL2]` returns **zero matching keys**; `[W1W]` carries only `n_spawn_placements` / `n_spawn_outside_wall` / `n_spawn_within_half_m_of_wall` — **a placement TOTAL, not a class breakdown.** ⚑ **There is no oracle side to grade against**, and `L-49` (*the recorded composition VALIDATES, IT DOES NOT SPAWN*) means a red would indict the port for the oracle's own behaviour. **Closure is a sibling, not a row.** | **KP-13 (1)**; Add. 2 § B1 |
| 2 | **`TA-B-09`** channel split | **CONDITIONAL** — `WIDTH := gamora (OWED)` | ⚑ **COUNTED. The width exists** (Add. 2 § B2 — both components are published per salt, so the split exists) | — | **KP-13 (2)** |
| 3 | **the power table** | *"the weight sits on the EXACT rows and on `TA-B-03 frac_moving` alone"* | ⚑ **`TA-B-09` DISPLACES `TA-B-03` at the top.** Report-face sentence becomes: **"the verdict's weight sits on the EXACT rows and on `TA-B-09` / `TA-B-03`."** | its sample sd is **less than half** of `TA-B-03`'s — the most discriminating BAND row T-A has. And it survives the short-salt critique that bites `TA-B-02`: **the split is a ratio *within* the channelling population**, so the 10.4× `D` span barely touches it. It is also the **one degree of freedom the four alive-state shares had left**, which is why v1.1 nominated it | **KP-13 (2)**; Add. 2 § B2 |
| 4 | **`TA-B-13`** `max_body_radius_m` | **CONDITIONAL** — `WIDTH := gamora (OWED)` | ⚑ **UNGRADEABLE-DECLARED. Dropped as a BAND.** | ⚑ **Its t-band would REJECT THE ORACLE'S OWN MAXIMUM.** A band that rejects the oracle cannot grade a port. Two independent reasons: **(i)** it is an **EXTREME over hundreds of bodies, not a mean** — maxima have asymmetric sampling distributions and `t · s · √(2/5)` assumes one, so § C.3's whole construction is the wrong instrument; **(ii)** the per-salt sample is **DEGENERATE** — 4 of 5 salts return an identical *structural* value (one body's placement plus its own radius), so `s` measures *"did salt 0 happen to roll the big body"*, not model variance. ⚑ **Nothing is lost: its falsifying power is carried one-sidedly and exactly by `TA-X-11`/`TA-X-10`** (`max ≤ R_wall 43.758085`, which the oracle satisfies at 43.404802 with a 0.353 m / 0.81 % margin and which the **superseded box scatter cannot satisfy at 47.072 m**). **A wrong instrument is removed, not a test** | **KP-13 (2)**; Add. 2 § B2 |
| 5 | **`TA-X-21`** cadence rounding | one site (the cadence law), asserting *"round = half-to-even"*; **v1.1 OQ-3 asked which `round`** | ⚑ **ANSWERED and WIDENED. The rule is `ROUND-HALF-TO-EVEN` (banker's), asserted EXPLICITLY — the word "round" never appears on the threat path.** **Four LIVE sites**, each with its own vector, plus a **negative assertion** and a per-site rule table (§ F.2a) covering the CEIL and TRUNCATE sites of record | **It is the Python BUILT-IN** — no `numpy`, no `decimal`, no `math.floor(x+0.5)` on the threat / cadence / arrival modules — and ⚑ **the seal corroborates in its own words**: the M-POL-2 fold's `⚑ quantisation_error` block reads *"round-half-to-**EVEN** to the nearest whole tick (Python's `round`)"*. **GDScript's `round()` rounds half AWAY FROM ZERO** — `round(2.5)` is **2** in Python, **3** in GDScript. ⚑ And the consequence is not one tick: the period sets `is_opportunity`, which sets **how many `choose_slot` calls draw** — so a bare GDScript `round()` **desynchronises the threat RNG stream** (V4-LAW-1) | **KP-13 (3)**; Add. 2 § B3 |
| 6 | ⚑ **`TA-X-24`** attack-phase model | *(absent)* | ⚑ **ADDED** — the port's phase model is **`ENGAGE`** (first tick inside the body's own max reach), never `PhaseModel.HASH` | **`HASH` is the MODULE DEFAULT and `ENGAGE` is the DRIVER OF RECORD** (V0) — ⚑ *the exact MODULE-DEFAULT-vs-DRIVER-OF-RECORD defect that has now bitten this run three times* (War Cry, Potion, and the census's own two first-pass errors). Both are deterministic, so **no band and no digest catches the difference** — but a different phase schedule changes *which tick each body swings*, hence the order of to-hit draws, hence the whole threat stream. And `HASH` is **explicitly labelled an invented de-correlator**, so implementing it is a Law-3 violation in the port as well. **Cheap, deterministic, free now** — and **raised as § H OQ-1 so the conductor can strike it** | this file; census M13; Add. 2 § B3 (`threat.py:1424` *"not of record"*) |
| 7 | **width companion pin** | `a7984b79…` | ⚑ **`6709cfe6…`** (Addendum 2 folded) | a pin to a superseded file state would make `TA-B-09`'s width unlocatable and `TA-B-13`'s reclass invisible | **KP-13** |
| 8 | **BAND sub-class counts** | 5 COUNTED · 4 REPORTED-NOT-COUNTED · 2 CONDITIONAL · 3 UNGRADEABLE | ⚑ **6 · 4 · 0 · 4** | rows 2 and 4 | **KP-13 (2)** |

**v1.1's open questions, dispositioned:** OQ-1 → **struck** (row 1) · OQ-2 → **both widths resolved** (rows 2, 4) · OQ-3 → **answered** (row 5) · OQ-4 (`M-POL` G5 left out) → **stands, carried to § H** · OQ-5 (`TA-X-20` half-closes V17; R2D-5 owns the drawn radius) → **stands, carried to § H**.

---

## § B · CONFIGURATION AND PRECONDITIONS

### B.1 · `ORACLE` — v3.2 `V0`, five arms, five salts

`V0` carries five `V0-ARM-*` rows — `M0`, `M-POL-2`, `M-POL-2-NULL`, `W1`, `W1-NULL` — each a **DELTA against the base row set, never a second full copy**. **5 arms × 5 salts = 25 headless runs**, each arm the base set with **exactly one fold moved**: that single-fold delta is the entire reason the inertness relations are readable.

Limbs of record include `spawn_fold: POLAR_UNIFORM_RHO` · `sustain: COUPLED` · `intake: ARMOUR_THEN_RESIST + global_flat` · `summons: PRESENT_INERT + offense MEASURED_BASIC` · `arena_fold: None` (armed only in `W1`) · `interrupts_fold: None` · **`WarCryLimb.COOLDOWN` (7.5 s)** · **`PotionLimb.TRACE_CONSISTENT` (θ 0.22972972972972974)** · `CritLimb: LO` · `p06: OFF` · ⚑ **`PhaseModel: ENGAGE`** (see `TA-X-24`).

**The runtime prints its RESOLVED limb set into the verdict header (`v0_limb_set`), diffed line-by-line against `V0` before any row is read; it refuses to boot on an unset limb rather than defaulting one.** ⚑ *"Is X wired?" is a driver fact a module default cannot answer* — which is why `V0` leads the lift, and why three of this run's corrections were caught by it within one wave.

**Pilot:** scripted — `DRIVE_TO_PACK` + the M-POL-2 channel policy; `v_ref = 4.0` is a DECLARED-FREE-PARAMETER → 5.4 m/s; **no facing model**.

### B.2 · P-1 · COVERAGE — **89/89**

All **89 enumerated census row ids** mapped **mechanically** (`kc2_runtime/loader/kc2rt_coverage.gd` carries the id list) to exactly one of `IMPLEMENTED` · `DIVERGENCE(DIV-nn)` · `RUNTIME-CHOICE(absent_ref)` · `OUT-OF-SCOPE`. **Counts sum to 89. Zero unmapped.** T-A does not run until green; **every band prints `value @ coverage k/89`**; graded as `TA-X-02`.

### B.3 · P-2 · STREAM DISJOINTNESS — and what it does not cover

**Probe:** run `M-POL-2` salt 0 twice, once with a **no-op fold inserted that draws zero values**; assert identical digests. **COVERS** stream isolation at *fold* granularity — exactly what `TA-X-03…06` need.

⚑ **DOES NOT COVER:** (1) that the port's draw sites are the **same sites in the same order** — P-2 is a null-fold probe, not a site census, and V9's registry is **29 live sites across 11 streams** (+2 NOT-LIVE); (2) ⚑ **the BOARD ROLL** (§ E trap 6); (3) that the per-site assignment is *lifted* rather than *chosen* — if `V9` is not consumed it is a RUNTIME-CHOICE ledger row and the report says so.

**P-2 red → `TA-X-03…06` UNGRADEABLE → `INDETERMINATE` → the cap trips.**

---

## § C · THE DENOMINATOR LAW, STATED ONCE

```
D_constructed = CHANNELLING + CHANNELLING_AND_MOVING + MOVING + IDLE      (PRE_FIGHT and DEAD excluded)
```
Verified on the seal: pooled `287 + 2211 + 166 + 119 = 2783 = D`; the per-salt sum equals the pooled sum, so the partition is exact at both grains. ⚑ **No sealed artifact carries `D`. It is CONSTRUCTED.**

**Two identities, 5/5 on the seal, graded as `TA-X-08`:** `n_player_ticks_observed = D + PRE_FIGHT` · `n_channelling + n_released = D` ⇒ `uptime + n_released/D = 1.000000` exactly.
⚑ **The seal publishes `release_duty` on `D + PRE_FIGHT`** (key `⚑ release_duty_on_observed_ticks`) — which is why the published per-salt duty max reads `0.214953` while the complement of the published uptime min is `0.216981`. **Every rate row here divides by `D` and by nothing else.**

**C.2 · Pooled vs mean-of-salts.** Every band is on the **MEAN-OF-SALTS**; a port's pooled figure is **never** compared against these bands. `D` per salt is **[1084, 305, 106, 185, 1103]** — a **10.4× span**. On the plant ratio the pooled/mean gap consumes **38 % of the whole tolerance** by choosing the wrong one of two numbers that share a name.
**C.3 · The graded object** is the **mean of a NEW 5-salt run**; the interval is a **prediction interval** carrying both runs' sampling error; `ddof = 1`. All arithmetic lives in gamora's file.
**C.4 · T-B denominators are NOT these.** HP occupancy on **`LIVE-MAX`** reproduces **42.84 %**; NOMINAL gives **39.76 %** — **3.08 pp with no fight in it**. HP window **181.0 s**; energy/motion **182.65 s**.

---

## § D · ROW-ID CONCORDANCE — the single namespace

⚑ **Every citation uses the `TA-` id; a width is looked up by STATISTIC NAME in the table named "governs", never by a bare `B-n`.**

| **canonical** | statistic | gandalf v1.0 | gamora § 2.4 | gamora Add. 1 | **width governs** |
|---|---|---|---|---|---|
| `TA-B-01` | terminal wave | B-1 | B-1 | — | § 2.4 · **REPORT-ONLY** |
| `TA-B-02` | **uptime** on `D` | B-3 | **B-2** | **B-4** | ⚑ Add. 1 restatement |
| `TA-B-03` | `frac_moving` on `D` | B-4 | B-3 | B-3 | Add. 1 restatement |
| `TA-B-04` | `P(chan \| moving)` | B-5a | B-4 | B-5a | Add. 1 restatement |
| `TA-B-05` | `P(chan \| stationary)` | B-5b | B-5 | B-5b | Add. 1 restatement |
| `TA-B-06` | plant ratio (window 5.0 s) | B-8 | B-6 | B-6 | Add. 1 restatement |
| `TA-B-07` | release duty on `D` | B-7 | B-7 | B-7 (restated) | Add. 1 · **reported-not-counted** |
| ⚑ `TA-B-09` | **channel split** `CHANNELLING / (CHANNELLING + CH_AND_MOVING)` | *(nominated v1.1)* | — | — | ⚑ **Addendum 2 § B2** |
| `TA-X-03…06` | inertness / distinctness | E-2, E-3, E-4 | **E-1 (a–d)** | A4 | — |
| `TA-X-07` | conservation, 7 terms | E-5 | **E-2** | — | — |
| `TA-X-02` | coverage | E-1 | **E-3** | — | — |
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
| **4** | **V4-LAW-1** — the cadence law is **not RNG-neutral** | `TA-X-21`, now **four sites + banker's + a negative assertion** (§ F.2a) | **CLOSED** |
| **5** | **V18 + V19** — flag **AND** coin = the 0.15 applied twice | `TA-X-22` | **CLOSED** |
| **6** | ⚑ **THE BOARD ROLL** | ⚑ **NONE, and `TA-X-23` is STRUCK rather than minted.** Both seals carry **no roster counts by class**; `[W1W]`'s `n_spawn_placements` is a **placement TOTAL** that would catch a gross count error and **nothing about composition**. `L-49`: the recorded composition **validates, it does not spawn** — asserting against `waves.json` would indict the port for the oracle's behaviour | **OPEN — DECLARED** |
| **7** | ⚑ **the attack-PHASE model** — `HASH` is the module default, `ENGAGE` the driver of record; both deterministic, so **no band and no digest sees the difference**, yet the swing schedule and therefore the to-hit draw order change | ⚑ **`TA-X-24`, added at v1.2** | **CLOSED (new row)** |

⚑ **Trap 6, stated for the report's face:** **12 of the 29 live draw sites are the board roll.** It is the mechanism most likely to be rewritten from scratch in GDScript; **its divergence shows as a different SET of monsters, not a different number; and T-A cannot see it at all.** Closing it properly is **a sibling that emits per-wave class counts**, not a T-A row.

**Also outside reach, unchanged:** per-site draw localisation (S5 out of scope — and at **29** sites the ceiling is *lower* than the charter assumed) · the tick-resolution HP trace · every `DIV-nn` row, by construction.

⚑ **And the limit on `TA-X-11` that must not be over-read:** the oracle's clamp counters are **structural zeros** — the wall never binds (margin **0.353 m / 0.81 %**). `TA-X-11` says *"the port never needed to clamp"*, **not** *"the port's wall works"*; **a port with no wall at all also scores zero.** The wall's existence is an R2D geometry probe.

---

## § F · THE GRADED ROWS

### F.1 · Decisiveness classes

**EXACT** — identity, invariant, count, or declared-precision reproduction; a red says **the port is wrong**; may carry a **NUMERICAL** tolerance, **never a STATISTICAL one**.
**BAND** — distributional at n = 5; **individually and collectively non-decisive**. Forms: `INTERVAL` · `RATIO` · `ORDERING`.
⚑ **No width is defaulted.** ⚑ **Cross-implementation rows are NOT salt-paired**; **inertness rows are salt-paired within the port**, which is why they can be exact when nothing else can.

### F.2 · EXACT rows — **23**

| id | statistic | basis | tolerance |
|---|---|---|---|
| `TA-X-01` | port self-determinism — any arm/salt run twice → identical digest | run-internal | byte-exact |
| `TA-X-02` | **coverage 89/89**, zero unmapped | the census id list | integer |
| `TA-X-03` | inertness A — `port(M-POL-2-NULL, s) ≡ port(M0, s)`, all 5 | `[M-POL2] ⚑ arms` | byte-exact |
| `TA-X-04` | inertness B — `port(W1-NULL, s) ≡ port(M-POL-2, s)`, all 5 ⚑ **not M0** | `[W1W]` | byte-exact |
| `TA-X-05` | distinctness C — `port(M-POL-2, s) ≢ port(M0, s)`, ≥ 1 salt | `[M-POL2]` | exact, one-sided |
| `TA-X-06` | distinctness D — `port(W1, s) ≢ port(M-POL-2, s)`, ≥ 1 salt | `[W1W]` | ⚑ **RELATION ONLY, never magnitude** — `Q.10`: one salt, five waves, two suppressed ticks, fold **exonerated** |
| `TA-X-07` | **conservation — SEVEN terms** | run-internal | **`1e-6`** ⚑ a live driver assert-wall in this repo checks **six** |
| `TA-X-08` | denominator identity, both sub-identities | `[M-POL2]`, 5/5 | exact |
| `TA-X-09` | all **9** `math_rules.test_vectors` | the pack | per-vector |
| `TA-X-10` | containment supremum `max_body_radius_m ≤ 43.758085029822276` (W1) | `[W1W] ⚑ wall` | exact, ≤ |
| `TA-X-11` | wall-clamp zeros — `n_wall_clamps_{player,body} == 0`, every W1 arm | `[W1W] ⚑ pools/per_arm` | integer |
| `TA-X-12` | pool inertness under ORACLE — total pool damage `== 0.0` | `[W1W] ⚑ pools` | exact |
| `TA-X-13` | no player crit | `V0 · CritLimb LO` | integer |
| `TA-X-14` | the two DO-NOTs (`cause == "energy"` → 0; no release-on-every-cast) | pack prohibitions, R2D-4 | integer |
| `TA-X-15` | release-schedule negative — p01–p04 at `t = 0.0`, p05 one burst at `t = 4.000 s`, no intra-point stagger | census M4 / `V11` | exact |
| `TA-X-16` | p06 OFF | `V0` ⚠ code default disagrees | integer |
| `TA-X-17` | spawn offset — `‖spawn_xy − anchor_xy‖ ≤ 8.0` m, every body, arm, salt | `ρ = 8.0·u₂`; box reaches **11.3137 m**, **~21.5 %** of box draws exceed 8.0 | exact, ≤ |
| `TA-X-18` | **scatter-law three-law discriminator** — feed `u₁ = u₂ = 0.5`, assert **`(−4.0, 0.0)`** | polar → `(−4.0, 0)` · uniform-in-area → `(−5.6569, 0)` · box → `(0.0, 0.0)` | exact |
| `TA-X-19` | arrival unconditionality — every queued arrival with a live caster in a live wave **is applied**; arrivals suppressed for **any position-dependent reason = 0**; **no damage predicate reads an arrival's `px, py`** | `deferred_arrival.py:13-17` | integer |
| `TA-X-20` | player hit-test predicate — 2.99 m hit / 3.01 m miss; **no angular gate** (3.0 m *behind* is hit); **no target cap** (12 inside → 12 hits) | census D7 (`disc.py:123-154`, MEASURED-ABSENT 4/4) | exact |
| ⚑ `TA-X-21` | **quantisation rule per site** — see **§ F.2a** | `threat.py`, `deferred_arrival.py`, `dot_timeline.py`, `control_application.py` | exact |
| `TA-X-22` | flag-off release cause under ORACLE — `cause == "interrupts_channel_flag"` occurs **0** times | `V0 · interrupts_fold: None`; V18+V19 | integer |
| ~~`TA-X-23`~~ | ~~board-roll composition~~ | ⚑ **STRUCK at v1.2 — outside T-A's reach (§ E trap 6). Id retired, never re-used** | — |
| ⚑ `TA-X-24` | **attack-phase model is `ENGAGE`** — a body entering its own max reach at tick *T* takes its opportunity at tick *T*; **`sha256(actor_id) mod n` is never evaluated** (assert the identifier is absent from the built path) | census M13; `V0 · PhaseModel: ENGAGE`; `threat.py:1438-1472` of record, `:1424` **not** | exact |

#### F.2a · ⚑ `TA-X-21` — THE QUANTISATION RULE, PER SITE

> **The word `round` must not appear anywhere on the threat path. The port implements `ROUND-HALF-TO-EVEN` explicitly — GDScript's built-in `round()` rounds half AWAY FROM ZERO** (`round(2.5)` → **2** in Python, **3** in GDScript).
> ⚑ **The consequence is not one tick.** The swing period sets `is_opportunity`, which sets **how many `choose_slot` calls draw** — a bare GDScript `round()` **desynchronises the threat RNG stream** (V4-LAW-1).
> **Corroborated by the seal itself:** the M-POL-2 fold's `⚑ quantisation_error` block states the rule in its own words — *"round-half-to-EVEN to the nearest whole tick (Python's `round`)"*.

| site | expression | **rule the port implements** | graded |
|---|---|---|---|
| `threat.py:1402` | swing period → ticks (**the cadence law**) | ⚑ **HALF-TO-EVEN** | **vector** |
| `threat.py:1522` | `max(1, int(round(delay_s × ticks_per_s)))` — first-cast gate | ⚑ **HALF-TO-EVEN** | **vector** |
| `threat.py:1555` | `max(1, int(round(cd × ticks_per_s)))` — slot cooldown | ⚑ **HALF-TO-EVEN** | **vector** |
| `threat.py:1867` | `tick + max(1, int(round(dot_duration_s × ticks_per_s)))` — DoT expiry | ⚑ **HALF-TO-EVEN** | **vector** |
| `deferred_arrival.py:330` | arrival tick | **`CEIL`** — the limb of record, half-insensitive (`:329`'s `round` is reachable only under `QuantLimb.ROUND`, **not of record**) | assert `CEIL` |
| `dot_timeline.py:380` | DoT bucket count | **`TRUNCATE`** — `R-DOT-2` truncates, never rounds | assert `TRUNCATE` |
| `control_application.py:591` | control bucket count | **`TRUNCATE`** | assert `TRUNCATE` |
| `counterplay.py:212` | `int(round(x × BAR_PX))` | presentation quantisation only — **not on a damage path** | not graded |

**Vectors (each of the four LIVE sites):** `n_raw = 8.5 → 8` · `n_raw = 10.5 → 10` · `n_raw = 2.5 → 2` *(GDScript's `round` returns 9, 11, 3 — every one discriminates)*.
**Negative assertion:** a source scan of the built runtime finds **zero** bare `round(` calls on the threat / cadence / arrival path; every quantisation site names its rule.

### F.3 · BAND rows — **14 ids**

| id | statistic | sub-class | width |
|---|---|---|---|
| ⚑ `TA-B-09` | **channel split** | ⚑ **COUNTED · INTERVAL — the strongest BAND row T-A has** | **Add. 2 § B2** |
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
| ⚑ `TA-B-13` | `max_body_radius_m` (W1) | ⚑ **UNGRADEABLE-DECLARED at v1.2** — an **extreme, not a mean**; the sample is **degenerate** (4 of 5 salts identical, a structural value); **its t-band rejects the oracle's own maximum.** Falsifying power carried one-sidedly by `TA-X-10`/`TA-X-11` | — |

**Sub-class counts: 6 COUNTED · 4 REPORTED-NOT-COUNTED · 0 CONDITIONAL · 4 UNGRADEABLE-DECLARED = 14.**

> ⚑ **THE REPORT-FACE SENTENCE, v1.2:** **"The verdict's weight sits on the 23 EXACT rows and on `TA-B-09` / `TA-B-03`. Every other BAND row is corroboration."** That is an honest statement of what a 5-salt fidelity grade is worth, and it belongs on the report's face, not in a footnote.

### F.4 · Emitted, not graded

Per-registered-site draw counters (**29 sites**; they localise nothing without S5) · the tick-resolution HP trace (a T-B instrument banked at T-A).

---

## § G · FAIL TAXONOMY AND THE T-B QUOTING CAP

| verdict | antecedent | consequence |
|---|---|---|
| **`STRUCTURAL`** | **≥ 1 EXACT row RED** | port is wrong; **no W4 until repaired**; cap **TRIPS**; **two graded runs against v1.2 both STRUCTURAL → HALT to Matt** |
| **`INDETERMINATE`** | 0 EXACT red, **≥ 1 EXACT UNGRADEABLE** (incl. P-1 or P-2 red) | cap **TRIPS**; does **not** increment the two-attempts counter |
| **`STATISTICAL`** | all EXACT green; **≥ 1 COUNTED BAND row RED** | a **finding**; handoff proceeds; cap does not trip |
| **`PASS`** | all EXACT green; no counted BAND red | **`PASS @ coverage k/89, n/6 counted band rows graded`** — never unqualified |

**Order:** `STRUCTURAL → INDETERMINATE → STATISTICAL → PASS`, stop at the first hit. **A BAND row can never outrank an EXACT row in either direction.** UNGRADEABLE is orthogonal — it lowers the denominator, never reds, never greens. **A GRADED RUN** = one execution of the 5 × 5 matrix producing a conforming verdict file; a port repair between attempts does not reset the counter. **No post-hoc widening, by anyone** (A-3; L-88).

**Verdict file** `kc2play.ta_verdict.v1` — `prereg_version: "v1.2"`, `prereg_sha256` of this file, `band_widths_sha256` **`6709cfe6…`**, `preconditions.P1_coverage {"mapped":89,"total":89,"unmapped":0}`, `v0_limb_set` diffed against `V0`.
**Cap — three refusal conditions:** **C1** verdict file absent / unparseable / sha mismatched · **C2** `verdict ∈ {STRUCTURAL, INDETERMINATE}` · **C3** coverage not **89/89**-mapped.
**"A fidelity figure"** (mechanical): a row pairing a twin statistic with a referent statistic; or a ratio/percentage/delta/residual/score between them; or `fidelity`/`faithful`/`accuracy`/`match`/`agreement`/`% of referent` in a label.
**Degraded behaviour:** raw twin-side statistics only, each with its own denominator and window; a **banner before** the statistics naming the condition; **non-zero exit**. Composes with R2D-10.

---

## § H · OPEN QUESTIONS — one lean each

**OQ-1 · `TA-X-24` is an addition I made, not one you asked for.** → **Keep it.** It costs one deterministic assertion, it closes the **only remaining trap that no band and no digest can see**, and it guards the exact defect that has already produced three corrections in this run — a **module default standing in for a driver of record**. Strike it with one word if you judge the phase model settled enough by `V0` alone; the cost of keeping it is a line of GDScript.

**OQ-2 · The board roll is declared open, and "declared" is not "closed."** → **Name the sibling in the handoff's findings harvest, with its one deliverable: per-wave class counts.** It is the largest surface T-A cannot see, it is **12 of 29 draw sites**, and the failure it hides — *a different set of monsters* — is the one a player would notice before any statistic did. Registering it as next-lap work is cheap; discovering it at T-B is not.

**OQ-3 · `M-POL` (G5) is in the seal and not in the arm set** *(carried from v1.1, still open)*. → **Leave it out.** The third inertness relation is not runnable at five arms, and a sixth arm buys one distinctness row against an arm the run is not porting.

**OQ-4 · `TA-X-20` half-closes V17** *(carried from v1.1, still open)*. → **Adopt both halves and say so on the report: `TA-X-20` clears the resolved predicate, `R2D-5` clears the drawn radius, and a green T-A clears only the first.** Narrowing a named gap is worth more than leaving it whole; overstating the narrowing is worth less than nothing.

**OQ-5 · `TA-B-13`'s removal leaves the wall covered one-sidedly only.** → **Accept the one-sidedness and print it.** `TA-X-10`/`TA-X-11` catch a port that *exceeds* the wall and cannot catch a port that *has no wall* — and gamora is right that a band rejecting the oracle's own maximum is worse than no band. The two-sided check belongs to the R2D geometry probes, and the T-A report should say which half it owns.

---

*Filed 2026-09-20 by gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1, Run KC2-PLAY. **v1.1 and v1.0 not edited; superseded readings named in place at § A.** **No width transcribed** — gamora's file is cross-pinned at `6709cfe6…` and governs every one. **K-7 held.** **Law 3 held:** every new assertion cites a substrate value or arithmetic derived in the open; none is fitted. No production code, no dispatch, no push.*
