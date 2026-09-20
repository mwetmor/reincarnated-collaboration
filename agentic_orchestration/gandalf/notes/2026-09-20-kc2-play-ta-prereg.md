# KC2-PLAY · T-A PREREGISTRATION — decision rules, row decisiveness, FAIL taxonomy, denominator law

> ⚑ **STATUS: IMMUTABLE ON COMMIT — v1.0, 2026-09-20.**
> **This file does not get edited.** Any change is a **new dated prereg version** (`…-ta-prereg-v2.md`) carrying, on its face, *what changed and why*. **A change made after a graded run exists against this version is a HALT to Matt** — not an amendment (charter § 4 row 4, WARN-16; D4; A-3's *no band widened post-hoc, by anyone*).
> **Authority:** charter `2026-09-20-kc2-play-run-charter.md` § 4 rows 2–4 + § 5 W1 + § 8 KP-4 · jack-ryan Gate-1 **BLOCK-C** (per-row decisiveness · FAIL taxonomy · T-B quoting cap as a harness refusal) and Gate-1 re-check **WARN-16** (immutability + independent pre-read) — `qa/findings/2026-09-20-run-KC2-PLAY-charter-gate1.md`.
> **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1. **Decision rules only.** Band WIDTHS are not mine and are not in this file.
> **Companion, cross-pinned by sha at the W1 seal (KP-4):** `agentic_orchestration/gamora/notes/2026-09-20-kc2-play-ta-band-widths.md` — gamora owns the variance (WARN-4). Every `WIDTH := gamora` slot below resolves there and **nowhere else**.
> **Independent pre-read:** jack-ryan reads this file **at the W1 seal, before any graded run exists** (WARN-16). The goalposts are reviewed before the result, or the review is of a conclusion.
> **Standing law binding on every line:** Law 3 (no fitted constants, no invented rules) · K-7 (no sealed cell re-run) · D4 (prereg alone, before results) · GL-6 / GL-12 · #72 (mechanical enumeration) · R-L91-4 (bands-not-tape) · D-MPOL2-2 (ratios/ordering where instruments disagree) · R-L89-4 (an aggregate says whether it is a *rate* or a *cancellation*) · digests **derived at use, never retyped** (S-1's own rule; WARN-10 is its founding breach).

---

## § 0 · What this document decides, and what it deliberately does not

It fixes, **before any graded run exists**: which configuration is under test, which arms run, which statistics are graded, on which denominator, from which sealed source, in which decisiveness class, under which failure taxonomy, and what a pass licenses.

It does **not** contain a single band width, and it must not. Widths are a variance question over gamora's own per-salt spreads (WARN-4); an author who does not own the variance drawing a width produces a band that is either unfalsifiable or unreproducible. **What this file owns is *how* a width is applied once she supplies it** (§ 3.0), which is a decision-rule question and is mine.

> ⚑ **The rubric declaration, carried verbatim from the twin-test spec § 0 and reprinted on the face of every T-A report (A-7):**
> *This test grades **runtime ≡ sim**. It does **not** grade **sim ≡ Matt**. A green T-A therefore certifies implementation fidelity, and a session that reads it as "the Godot build plays like Matt" has swapped the owner's question for a narrower proxy. That is the KIT-FIDELITY failure, and it is named here so it cannot be discovered later.*

---

## § 1 · THE CONFIGURATION UNDER TEST — `ORACLE`, and no other

### 1.1 Definition by reference, not by transcription

**`ORACLE` is defined as baton-v3.2 `V0` — the FOLD/LIMB SET OF RECORD** (census § 2 Tier 1, V0). V0 is the artifact; this section is a **labelled expectation checked against it**, never substituted for it (twin-test § 2.3 clause 1). The census's own headline on V0 governs the whole instrument:

> *"Without it a port cannot be configured to the oracle, so T-A grades a configuration difference and calls it a port bug."* — census § 2, V0

**The expected content of V0, as the census transcribes the lift build's own call:** `spawn_fold: POLAR_UNIFORM_RHO` · `sustain: COUPLED` · `intake: ARMOUR_THEN_RESIST + global_flat` · `dot: DECODED_D4C/PER_ROW` · `control: RECORD/ARM_B` · `summons: PRESENT_INERT + offense MEASURED_BASIC` · `alert: ARM_HOLD` · `px_arm: LO` · `defences: true` · `arena_fold: None` · `interrupts_fold: None` · `WarCryLimb: I8_LEGACY` · `PotionLimb: I4_EXCURSION_MAX` · `CritLimb: LO` · `p06: OFF`.

**Two cross-checks owed at the V0 cut, named here so they are not discovered at grading:**
- **(i)** `alert: ARM_HOLD` in the V0 list vs census M8's body text (`alert_fold=None`, default limb `OBSERVE_ONLY`, *"OFF on every incumbent path"*). These may be the driver's arm name and the module's limb name for the same off-state, or they may not be. **gamora resolves at the V0 transcription; the runtime prints its resolved limb set in the verdict header for a line-by-line diff against V0.** If V0 and a committed census row genuinely contradict, that is a **committed-truth conflict → HALT** (charter § 6), not a lift-row judgment call.
- **(ii)** Several module defaults **differ from the cell of record** (`OffenseLimb.REFUSED` vs `MEASURED_BASIC`; `P06_CODE_DEFAULT True` vs the driver's `False`; `PlayerSustainFold.limb` has **no default and raises**). *"Read the defaults" is not a fallback; it is a different sim* (census § 2, V0). The port **refuses to boot** on any unset limb rather than defaulting one.

### 1.2 The pilot

**Scripted, never human.** Charter § 2 names it *"PM1 + the M-POL-2 channel policy"*. Mechanically, per the census:
- **Movement:** `PlayerPolicy.DRIVE_TO_PACK` is of record — `S(i) = Σ_{j: |xⱼ−xᵢ| ≤ 8.0} (1 + 3.0·boss(j))`, argmax, ties → lowest `actor_id`; retarget every **12 ticks**; hysteresis margin **0.25**, cooldown **24 ticks**; pass-through lock 3.0 m; **step never clamped** — drive-through, not stop-at-target; empty board → HOLD (census K23). Speed **5.4 m/s** = `v_ref 4.0` (a **DECLARED-FREE-PARAMETER**) × `playerRunSpeedCapMax 1.35` (census K24).
- **Channel:** the **M-POL-2** policy of record — Type-A releases at wave transition (`DS-RELEASE-MOTION-SUPPRESS` p = 0.3583399840383079, lag median 1.60 s, duration mean 1.309 s); Type-B on the **uniform 0.15 cancellation folded in** (`DS-TYPEB-RELEASE p_per_tick = 0.0035510204081632656` = `0.290 × 0.15 / 12.25`) (census K6, K7).
- ⚑ *"PM1" is the charter's label for the movement-policy lineage; the mechanical content above is the census's, and **V0 is the binding statement of both**.* Where label and mechanism disagree, V0 governs.

### 1.3 Salts and arms

**5 salts per arm**, as the oracle ran them (census § 3c). **FIVE arms**, not four:

| arm | what moves relative to V0 | why it must run |
|---|---|---|
| **`M0`** | nothing (the control of record) | ⚑ **The referent of the first inertness relation.** The oracle asserts `M-POL-2-NULL` byte-inert **vs `M0`** — *not* vs `M-POL-2`. Without `M0` in the port's own matrix, **E-2 cannot be evaluated at all.** The charter's *"base, NULL, W1 walls, W1-NULL at minimum"* yields one checkable inertness pair; adding `M0` yields **two independent pairs and one distinctness falsifier**, for four extra headless runs. |
| **`M-POL-2`** | the channel policy armed (the build; the policy of record) | The arm every BAND row is graded against. Seal `ad61ad2a…`. |
| **`M-POL-2-NULL`** | the channel-policy fold **disarmed** | The disarmed control. Oracle: **byte-inert vs `M0`**. |
| **`W1`** | `arena_fold` **ARMED** (`R_wall = 43.758085029822276 m`, `CIRCLE`, `STOP`-never-slide) | The walls arm. Seal `7a992c81…`. Carries the containment invariants and the wall/pool counters. |
| **`W1-NULL`** | `arena_fold` present but **disarmed** | Oracle: **byte-inert vs the M-POL-2 seal** — terminals `[156, 152, 151, 151, 156]`, identical to `M-POL-2`. |

**5 arms × 5 salts = 25 headless runs.** Each arm is V0 with **exactly one fold moved**, and that single-fold delta is the entire reason the inertness relations are readable.

### 1.4 What `ORACLE` is NOT

`ORACLE` runs **pools inert** (`POOL_DOT_MAGNITUDE_ABSENT = 0.0`), **the uniform 0.15 coin** (`interrupts_fold = None`), **no player crit** (`CritLimb LO`), **fire-time damage resolution** (no arrival hit-test), **bound-skill additions OFF** (R-KP-0e), and **the scripted pilot**. Every one of those is a row in the divergence register (`2026-09-20-kc2-play-divergence-register-v0.md`) and **none of them is graded here**. T-A grades the port, not the game.

---

## § 2 · PRECONDITIONS — two gates, both green, before the first graded run

### P-1 · COVERAGE (charter § 4 row 3; Gate-1 BLOCK-B)

All **72** P0-a census rows mapped **mechanically** — a table emitted by the runtime's own rule census, never prose — to exactly one of `IMPLEMENTED` · `DIVERGENCE(DIV-nn)` · `RUNTIME-CHOICE(absent_ref)` · `OUT-OF-SCOPE(§ 1 citation)`. **Counts sum to 72. Zero unmapped.**

- **T-A does not run until P-1 is green.** A red P-1 is not a T-A result; it is an absent T-A.
- **Every reported band prints `value @ coverage k/72`.** No band is ever quotable without the denominator it was measured on. *An accurate port of a fraction of the fight is not a fidelity result.*
- P-1 is itself graded as an **EXACT** row (E-1) so that it appears in the verdict file with a status rather than only in a gate log.

### P-2 · ⚑ STREAM DISJOINTNESS (new — this prereg's own framing-audit finding; see § 8)

**The inertness relations (E-2, E-3) and the distinctness falsifier (E-4) are meaningless unless the port implements the sim's disjoint-stream discipline (`D-I22-1`).** The oracle's relations hold *because* each fold draws from its own stream, so disarming a fold removes draws without shifting any other site's stream position. A port that shares one RNG across sites will fail E-2/E-3 **even when every rule is implemented correctly**, and will fail them for a non-reason.

**The probe, run once before any graded run, cost ≈ one headless run:**

> Run `M-POL-2`, salt 0, twice: (a) as configured; (b) with a **no-op fold inserted that draws zero values**. **Assert identical run digests.** If a fold that draws nothing changes the stream, the port does not have disjoint streams.

- P-2 green → E-2/E-3/E-4 are graded as **EXACT**.
- P-2 red → E-2/E-3/E-4 are **UNGRADEABLE**, the verdict is **INDETERMINATE** (§ 4), the T-B quoting cap trips, and the finding is *"the port's RNG architecture, not the port's rules."*
- ⚑ **Dependency, declared:** the disjoint-stream discipline is carried into the pack by **V9** (draw-site registry 3 → ~13 + the `D-I22-1` law row, Tier 1). The census is explicit that *"that discipline transfers; the registry does not yet describe it"* (census W11). **If V9 HONEST-FAILs at the v3.2 cut, P-2 is still runnable** — it is a property of the port, not of the pack — but the port's per-site stream assignment is then a **RUNTIME-CHOICE** ledger row rather than a lifted rule, and the T-A report says so.

---

## § 3 · THE GRADED ROWS

### 3.0 · Decisiveness classes, and how a width is applied

**Two classes. No third.**

| class | meaning | tolerance |
|---|---|---|
| **EXACT** | An identity, an invariant, a count, or a declared-precision reproduction. A red here says **the port is wrong**. | **No statistical tolerance, ever.** An EXACT row may carry a **NUMERICAL** tolerance for floating-point representation (stated per row); it may never carry a **STATISTICAL** one. That distinction is fixed here so it cannot be argued mid-run. |
| **BAND** | A distributional comparison between two implementations at n = 5. **Individually NON-DECISIVE** — no BAND row, alone or in combination, can produce a STRUCTURAL verdict. | `WIDTH := gamora`, resolved in the companion file and nowhere else. |

**A BAND row is graded in exactly one of three FORMS. The form is fixed here; the width is gamora's.**

| form | when it is used | how the width applies |
|---|---|---|
| **INTERVAL** | the statistic is directly comparable and gamora's spread supports an interval | port value ∈ `[lo, hi]`, where `[lo, hi]` is derived **from the per-salt spread**, not from the pooled point. Applied **per-salt-envelope** (the port's 5 values must lie inside the oracle's per-salt envelope widened by gamora's rule) **and** on the pooled statistic — **both reported, the pooled one non-decisive on its own** (a pooled agreement over a disagreeing envelope is the 2.5×-spread trap). |
| **RATIO** | instruments disagree about the absolute, per **D-MPOL2-2** | a dimensionless ratio of two of the port's own statistics compared against the same ratio on the oracle side, inside gamora's width. The instrument cancels. *(Twin-test § 7 rule 1: an absolute movement figure in a green report is a defect in the report.)* |
| **ORDERING** | a width would be meaningless but a direction is decidable | a **strict inequality between two of the port's own statistics**, matching the oracle's direction. No width consumed. **Still BAND class** — a satisfied ordering is weak evidence, not structure. |

⚑ **Cross-implementation rows are NOT salt-paired.** Bands-not-tape (R-L91-4) makes the two streams different by construction; the port's salt *k* is not the oracle's salt *k*. Every BAND row is a **distributional** comparison over the unordered 5-multiset. **The inertness rows are the opposite and this is the whole point:** E-2/E-3/E-4 are **run-internal and salt-paired *within the port*** — same seed, same stream, one fold disarmed — which is why they can be exact when nothing else can.

⚑ **No width is ever defaulted.** A BAND row whose `WIDTH := gamora` slot is unfilled when the first graded run fires is **UNGRADEABLE**, declared as such. It is not graded loosely, not graded on the pooled point estimate, and not skipped silently.

### 3.1 · The oracle sources

| tag | cell | sha256 (16) | bytes |
|---|---|---|---|
| `[M-POL2]` | `simulation/output/kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` | `ad61ad2a8c799d6e` | 123,564 |
| `[MECH]` | `…/kc2-checkpoint-E-s09-cp150-mech-20260816_124031.json` | `20b05cb4ef3bd888` | 2,125,271 |
| `[W1W]` | `…/kc2-checkpoint-E-s09-cp150-w1walls-20260825_220058.json` | `7a992c81ca6e56e5` | 403,084 |

**K-7: hash-verify only. No sealed cell is re-run, for any reason, including to produce a statistic this prereg asks for.** A statistic that is not at these digests is **UNGRADEABLE**, never manufactured.
⚑ **Key paths below are named as the census names them in prose. The exact JSON key path is derived at read time by gamora and never retyped** — the same law that governs digests (WARN-10's founding case).

### 3.2 · EXACT rows

| id | statistic | definition (incl. denominator where one exists) | oracle source | numerical tolerance |
|---|---|---|---|---|
| **E-0** | **port self-determinism** | Any arm, any salt, run twice → **identical run digest**. *Precondition-within-the-set: without it, every other digest row is noise.* | none — run-internal | exact byte equality |
| **E-1** | **coverage** | 72 rows mapped, `Σ classes = 72`, `unmapped = 0` (P-1) | none — the census is the denominator | integer, exact |
| **E-2** | **inertness A** | `port(M-POL-2-NULL, salt s) ≡ port(M0, salt s)` for **all 5 salts**, by the port's own digest over its declared canonical event serialisation | `[M-POL2] · ⚑ arms` — the oracle asserts `M-POL-2-NULL` **byte-inert vs `M0`** | exact byte equality of the port's own digest |
| **E-3** | **inertness B** | `port(W1-NULL, salt s) ≡ port(M-POL-2, salt s)` for **all 5 salts** | `[W1W]` / `[M-POL2]` — oracle: `W1-NULL` byte-inert vs the seal; terminals `[156,152,151,151,156]` identical to `M-POL-2` | *ibid.* |
| **E-4** | **distinctness** (one-sided falsifier) | `port(M-POL-2, salt s) ≢ port(M0, salt s)` for **at least one** salt | `[M-POL2] · ⚑ T1_reported_never_gated` — the oracle's two arms differ (`[155,152,155,151,152]` vs `[156,152,151,151,156]`) | exact |
| **E-5** | **deferred-arrival conservation identity** | Per wave, per salt, per arm: `offered = applied + dropped + voided + pool_truncated + pcl_reclaim + counterplay_absorbed`; residual → 0 | ⚑ **run-internal — needs no oracle side.** That is why it is always gradeable and why it carries weight | `abs(residual) ≤ 1e-9 · max(1, offered)` — a representation tolerance on an exact identity, **not** a band |
| **E-6** | **test vectors** | All **9** `math_rules.test_vectors` reproduced to **each vector's own declared precision**. A vector declaring no precision is compared by exact equality on its numeric type; a vector with neither is **UNGRADEABLE and declared** | the pack (`ACC-T0-VECTORS`, `report_only: false`) | per-vector |
| **E-7a** | **containment supremum** (W1 only) | `max_body_radius_m ≤ 43.758085029822276` and `max_player_radius_m ≤ 43.758085029822276`, every salt | `[W1W] · ⚑ wall` (oracle observed 43.405 m body / 24.877 m player; margin 0.353 m = 0.81 %) | exact, ≤ |
| **E-7b** | **wall-clamp count** (W1) | `n_wall_clamps_body` and `n_wall_clamps_player` match the oracle's values at `[W1W] · ⚑ wall` | `[W1W] · ⚑ wall` | integer, exact — ⚑ **conditional**: if gamora reads the oracle's values as **non-zero**, E-7b **reclassifies to BAND** before the first graded run (a reclassification made *after* a graded run is a HALT) |
| **E-8** | **pool inertness under ORACLE** | Total pool damage applied to the player `== 0.0` across every arm and salt (`POOL_DOT_MAGNITUDE_ABSENT = 0.0`, census W5). `n_pool_occupancy_ticks` may be non-zero; **damage may not** | `[W1W] · ⚑ pools` | exact |
| **E-9** | **no player crit** | Count of player damage rows with `is_crit == true` is **0** (census D12: `CritLimb LO` = ×1.0; every player damage row hardcodes `is_crit=False`) | census D12 / V0 `CritLimb: LO` | integer, exact |
| **E-10** | **the two DO-NOTs** | `channel_off.cause == "energy"` occurs **ZERO** times (`RULE-NO-ENERGY-GATED-RELEASE`); no release fires on every cast (`RULE-NO-RELEASE-ON-EVERY-CAST`). Mechanically enforced, not commented (R2D-4) | the pack, prohibitions | integer, exact |
| **E-11** | **release-schedule negative** | `p01–p04` release **every** body at `t = 0.0`; `p05` is a **single burst at `t = 4.000 s`**; **no intra-point stagger anywhere** (census M4; `verify_release_negative` HALTs on one in the sim) | census M4 / v3.2 **V11** | exact |
| **E-12** | **p06 OFF** | Spawn point `p06` contributes **zero** bodies in every arm and salt (V0 `p06: OFF`; ⚠ the code default disagrees — `P06_CODE_DEFAULT = True`, census M4b) | V0 / census M4b | integer, exact |

⚑ **E-7a is a tautology under the correct spawn law and a pure falsifier under the wrong one — and that is deliberate.** `R_wall = max|emitter| + PLACEMENT_EXTENTS_M = 35.758085 + 8.0 = 43.758085` *is* the supremum of the polar-disc scatter, so a correct port can never exceed it. Under the pack's **superseded** `DS-SPAWN-SCATTER` box reading (half-width 8.0 → corner at `8.0 · √2 = 11.3137` m) the reachable radius is `35.758085 + 11.3137 = 47.072` m — **above the wall, with certainty**. **Pre-registered prediction, in D4 form: a port that implements the pack's emphatic "NOT A DISC" note reds E-7a and E-7b in the named upward direction.** (Census (c-9): *the pack tells the builder to draw a square and warns him off the disc; the oracle draws the disc.*)

### 3.3 · BAND rows

| id | statistic | definition + **denominator** | form | oracle source + value | width |
|---|---|---|---|---|---|
| **B-1** | **terminal-wave 5-vector** | the unordered multiset of 5 terminal waves per arm, with `terminal_reason`, `run_tick`, `t_s`, `killer_id`, `n_live_bodies` per cell | INTERVAL | `[M-POL2] · ⚑ T1_reported_never_gated` — `M-POL-2 [156,152,151,151,156]`, mean **153.2**, **σ 2.32**; `M0 [155,152,155,151,152]` mean 153.0; `M-POL (G5) [151×5]`; `W1 [156,152,151,151,151]` | `WIDTH := gamora` |
| **B-2** | **per-wave durations** | `duration_s` per wave 151→terminal, per salt; clear/death terminal | INTERVAL | ⚑ **CONDITIONAL — see the note below** | `WIDTH := gamora` |
| **B-3** | **channel uptime** | `(CHANNELLING + CHANNELLING_AND_MOVING) / D` where **`D = CHANNELLING + CHANNELLING_AND_MOVING + MOVING + IDLE`**, excluding `PRE_FIGHT` and `DEAD` | INTERVAL (per-salt envelope **and** pooled) | `[M-POL2] · ⚑ acceptance` — pooled **0.897593**, per-salt **0.783 – 0.914** (D = 2,700 ticks for M0) | `WIDTH := gamora` |
| **B-4** | **`frac_moving`** | `(CHANNELLING_AND_MOVING + MOVING) / D`, same `D` | RATIO | `[M-POL2] · ⚑ acceptance` — pooled **0.854114**, per-salt available | `WIDTH := gamora` |
| **B-5a** | **P(channel \| moving)** | `CHANNELLING_AND_MOVING / (CHANNELLING_AND_MOVING + MOVING)` | INTERVAL | *ibid.* — **0.930164** | `WIDTH := gamora` |
| **B-5b** | **P(channel \| stationary)** | `CHANNELLING / (CHANNELLING + IDLE)` | INTERVAL | *ibid.* — **0.706897** | `WIDTH := gamora` |
| **B-6** | **conditional ordering** | `P(channel \| moving) > P(channel \| stationary)` in the port | ORDERING | *ibid.* — oracle direction 0.930 > 0.707 | none consumed |
| **B-7** | **release duty** | `1 − uptime` on the **same `D`** — ⚑ **DERIVED, NOT INDEPENDENT. See the note below.** | INTERVAL, **reported not counted** | `[M-POL2] · ⚑ acceptance` — pooled **0.102407**, per-salt **0.086 – 0.215** | `WIDTH := gamora`, **reported only** |
| **B-8** | **plant ratio** | window-stationary / fight-stationary, **window = 5.0 s** | INTERVAL | `[M-POL2] · ⚑ acceptance` — **1.390601** | `WIDTH := gamora` |
| **B-9** | **release count + duration by type** | count and duration distribution of Type-A and Type-B releases per salt | INTERVAL | `[M-POL2] · ⚑ acceptance` | `WIDTH := gamora` |
| **B-10** | **arrival latency** | latency histogram in ticks and seconds (min / median / max); co-arrival census; `n_deferred / n_arrived / n_dropped_at_wave_end` | INTERVAL | ⚑ **CONDITIONAL — `[MECH]` emits `DeferredArrivalFold.as_dict` per wave, but `[MECH]` is a DIFFERENT ARM. See the note below** | `WIDTH := gamora` |
| **B-11** | **wall + pool counters** (W1) | `n_wall_clamps_{player,body}` (if reclassified from E-7b), `n_avoidance_vetoes`, `n_pool_occupancy_ticks`, `max_{body,player}_radius_m` | INTERVAL | `[W1W] · ⚑ wall`, `⚑ pools` | `WIDTH := gamora` |
| **B-12** | **intake by wave and damage family** | player damage taken per wave, split by family; leech healed per tick | INTERVAL | ⚑ **CONDITIONAL** (same shape as B-2) | `WIDTH := gamora` |

#### ⚑ B-7 — release duty is the complement of uptime, and the two per-salt ranges do not agree

`0.897593 + 0.102407 = 1.000000` **exactly**. On the constructed denominator, release duty **is** `1 − uptime`. Grading both as independent bands counts one measurement twice and inflates the apparent evidence by a factor of two on the row the charter leans on hardest. **Disposition: B-3 is the graded band; B-7 is reported beside it and contributes nothing to the verdict counts**, plus one EXACT-class internal check — `uptime + release_duty = 1` within `1e-6` **inside the port** — which catches a port that builds two different denominators.

⚠ **And the oracle's own per-salt figures are not complements.** Uptime per-salt `[0.783, 0.914]` implies duty `[0.086, 0.217]`; the census reports duty `[0.086, 0.215]`. Complementation is monotone, so the min-uptime salt **must** be the max-duty salt: if `u = 0.783` to 3 d.p. then `u ∈ [0.7825, 0.7835)` and `1 − u ∈ (0.2165, 0.2175]`, which rounds to **0.217 or 0.216 — never 0.215**. The pooled pair sums to exactly 1; the per-salt extremes do not. **Either the two statistics are on different denominators in the oracle, or a third state category sits outside both, or the census transcribed one figure.** This is the census's own named hazard turned on the census — *"using a different denominator is the single easiest way to fail T-A for a non-reason"* (census § 3d item 3).

> **Cheapest refuting test, named and owed before the first graded run:** gamora reads the five per-salt `(uptime, release_duty)` pairs from `[M-POL2]` and reports whether `uptime_s + duty_s = 1` for **every** salt *s*. **One read, no sim run, K-7 untouched.** If they are not complements, B-3's denominator is not the denominator this prereg states, and **B-3, B-4, B-5a, B-5b, B-6 and B-7 are all UNGRADEABLE until the construction is restated** — they share the denominator.

#### ⚑ B-2 / B-10 / B-12 — the conditional rows, and what happens if the oracle has no value

Census **§ 3c** enumerates what exists at the sealed digests: terminal-wave vectors, the channel/motion shape, per-arm per-salt digests, wall+pool geometry, and arrival telemetry **in the mech cell**. It does **not** list per-wave durations or per-wave intake for the **arm of record**. Census **§ 3d** lists them as things *the port must emit* — which is not the same claim.

**Rule, pre-registered:** for each of B-2, B-10 and B-12, **gamora names a key path in `[M-POL2]` (or `[W1W]` for the W1 arm) carrying the statistic for the arm of record.** If no such path exists at those digests:
- the row is **UNGRADEABLE**, declared with the reason *"no oracle-side value at the sealed digest for the arm of record"*;
- it is **not** graded against `[MECH]`, which is a different arm — grading across arms measures a configuration difference and calls it a port bug, which is the exact failure V0 exists to prevent;
- and it is **not** manufactured by re-running a sealed cell (**K-7**).

*(B-10's internal half survives regardless: E-5's conservation identity is run-internal and needs no oracle side.)*

### 3.4 · Emitted but NOT graded

- **Per-registered-site draw counters.** Emitted per § 3d item 7, reported as an **internal consistency instrument only**. ⚑ **No sealed cell emits a per-site draw count (sibling S5 is out of scope), so these localise nothing.** A stream divergence is visible and **not locatable**; localisation is next-lap work behind S5 (WARN-14, charter § 4 row 4 declared ceiling).
- **The HP trace at tick resolution** (§ 3d item 5). Emitted because it is what makes the T-B saw-tooth checkable; **no oracle-side reference exists for its waveform**, so it is a T-B instrument banked at T-A, never a T-A row.

---

## § 4 · FAIL TAXONOMY — mechanical antecedents, and the rule for mixed outcomes

### 4.1 The four verdicts

| verdict | **mechanical antecedent** | consequence |
|---|---|---|
| **`STRUCTURAL`** | **≥ 1 EXACT row RED** | The port is wrong. **The run does NOT proceed to W4 until repaired.** T-B quoting cap **TRIPS**. HALT to Matt after **two graded runs against this prereg version** both returning STRUCTURAL. |
| **`INDETERMINATE`** | **0 EXACT rows red, but ≥ 1 EXACT row UNGRADEABLE** (includes P-1 red and P-2 red) | Nothing was refuted; an instrument was missing. T-B quoting cap **TRIPS** (an exact row we could not decide is not a pass). ⚑ **Does NOT increment the two-attempts HALT counter** — that counter exists for refutations, not for absent instruments. |
| **`STATISTICAL`** | **all EXACT rows green; ≥ 1 BAND row RED** | A **finding**. The handoff proceeds. Cap does **not** trip. The verdict names which band rows red, out of how many graded. |
| **`PASS`** | **all EXACT rows green; no BAND row red** | Reported as **`PASS @ coverage k/72, n/m band rows graded`**. Never as an unqualified pass. |

**UNGRADEABLE is orthogonal to the verdict, not a verdict.** A BAND row that is UNGRADEABLE lowers `m` in `n/m`; it never reds and never greens. Every UNGRADEABLE row appears in the verdict file with its reason.

### 4.2 Mixed outcomes — the ordering rule, stated once

> **Evaluate in this order and stop at the first hit:** `STRUCTURAL` → `INDETERMINATE` → `STATISTICAL` → `PASS`.
> **A BAND row can never outrank an EXACT row in either direction.** A green EXACT set does not rescue a red band from being reported; a red band set does not upgrade to STRUCTURAL however many rows red. That is what *"BAND rows are individually NON-decisive"* means made mechanical: **they are non-decisive collectively too.**

### 4.3 "Two attempts" — the referent, fixed here (WARN-16)

- A **GRADED RUN** is one execution of the full **5 arms × 5 salts** matrix that produces a **verdict file** conforming to § 5.1. A run that aborts before writing a verdict file is **not** a graded run.
- **Both attempts are graded against THIS prereg version.** A port repair between attempts does **not** reset the counter; a new prereg version does not reset it either — it *is* the HALT (§ 0).
- **Two STRUCTURAL verdicts against prereg v1.0 → HALT to Matt.** INDETERMINATE verdicts do not count toward it (§ 4.1).
- This clause is a **stricter superset** of charter § 6's *"two consecutive failed attempts at the same gate by the same seat"* (which is seat-keyed); where they differ, the stricter binds.

### 4.4 No post-hoc widening, by anyone

**A-3, and the L-88 precedent that paid for it: a failed band was carried FAILED-AS-REGISTERED rather than widened, by seat *and* by conductor.** A red BAND row is reported red with its named first suspect. Widening a width after a result — including "clarifying" a width, "correcting" a denominator toward agreement, or re-pooling salts to a friendlier statistic — is a **prereg change after a graded run exists**, which is § 0's HALT.

---

## § 5 · THE T-B QUOTING CAP — a harness refusal, specified so it can be built

**Pattern of record: R2D-10.** *(A structural guarantee, not a procedural promise — the harness refuses; it does not ask the report's author to remember.)* This cap composes with R2D-10 rather than replacing it: **R2D-10 refuses a T-B table from a FEEL-ONLY recording; this cap refuses a *fidelity figure* from a legitimate T-B table.**

### 5.1 The verdict file the T-B grader reads

Written by the T-A grader at the W3 seal; read by the T-B grader at every invocation. Schema `kc2play.ta_verdict.v1`:

```
{
  "schema":            "kc2play.ta_verdict.v1",
  "prereg_path":       "agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg.md",
  "prereg_version":    "v1.0",
  "prereg_sha256":     "<derived at write time from the file on disk, never retyped>",
  "band_widths_path":  "agentic_orchestration/gamora/notes/2026-09-20-kc2-play-ta-band-widths.md",
  "band_widths_sha256":"<derived>",
  "register_sha256":   "<the divergence register hash, § 6 of the register>",
  "config":            "ORACLE",
  "v0_limb_set":       { ... as the runtime resolved it, for line-by-line diff against V0 ... },
  "run_id": "...", "run_utc": "...", "attempt_index": 1,
  "preconditions": { "P1_coverage": {"mapped":72,"total":72,"unmapped":0,"by_class":{...},"green":true},
                     "P2_stream_disjointness": {"green":true,"probe_digests":["...","..."]} },
  "rows": [ {"id":"E-2","class":"EXACT","form":"IDENTITY","status":"GREEN|RED|UNGRADEABLE",
             "value":..., "oracle":..., "width":null, "reason":"", "first_suspect":""} , ... ],
  "counts": {"exact_green":n,"exact_red":n,"exact_ungradeable":n,
             "band_green":n,"band_red":n,"band_ungradeable":n},
  "verdict": "PASS|STATISTICAL|STRUCTURAL|INDETERMINATE",
  "quoting_cap": {"t_b_fidelity_quotable": true|false, "refusal_condition": null|"C1"|"C2"|"C3"}
}
```

### 5.2 The three refusal conditions

The T-B grader **refuses to print a fidelity figure** iff any of:

- **C1 — T-A ABSENT.** The verdict file is missing, unparseable, fails schema validation, or its `prereg_sha256` does not match the sha256 of the committed prereg on disk at grading time.
- **C2 — STRUCTURAL-RED or INDETERMINATE.** `verdict ∈ {"STRUCTURAL", "INDETERMINATE"}`.
- **C3 — COVERAGE NOT 72/72-MAPPED.** `preconditions.P1_coverage.green != true`, or `mapped != 72`, or `unmapped != 0`.

*(C2 folds INDETERMINATE in deliberately: the charter's clause reads "STRUCTURAL-red"; an EXACT row that could not be decided is not a pass, and a cap that lets an un-decidable instrument through is a cap with a hole in it. Named here as a widening of the charter's condition, not a silent reading of it.)*

### 5.3 What "a fidelity figure" is, defined mechanically so the refusal is buildable

Any output row or field that:
1. **pairs a twin-side statistic with a referent-side (footage) statistic in the same row**; **or**
2. emits a **ratio, percentage, delta, residual or score** between a twin value and a referent value; **or**
3. carries any of `fidelity` / `faithful` / `accuracy` / `match` / `agreement` / `% of referent` in a row label, column header or summary line.

### 5.4 Degraded behaviour under refusal

- **Raw statistics only**: twin-side values, each with its own denominator and window stated, **no referent column, no referent row, no derived comparison**.
- **A banner at the head of every page and at the head of every emitted file**, naming the condition:
  > ⚑ **T-B FIDELITY FIGURES WITHHELD — `<C1|C2|C3>`: `<the condition's own sentence>`.** *These are raw twin-side statistics. Nothing below is a comparison against Matt's footage, and no number here may be quoted as fidelity.*
- **Exit code non-zero** on the grader, so a script cannot consume a capped run as a green one.
- The banner is emitted **before** the statistics, not appended — a footnote is not a refusal.

---

## § 6 · DECLARED CEILINGS — what this instrument cannot do, stated before it runs

**C-1 · Draw-site localisation.** The port emits a per-registered-site draw counter; **no oracle-side per-site count exists** (S5 out of scope, K-7). A stream divergence is **visible and not locatable**. The T-A report says so on its face (WARN-14).

**C-2 · n = 5 cannot resolve a small port error on the terminal wave — and the arithmetic is printed so nobody over-reads the row.** With σ = 2.32 and n = 5: `SE = 2.32/√5 = 1.0375`; the half-width of a 95 % interval on the oracle's own mean is `t(.975,4) × SE = 2.7764 × 1.0375 = ` **± 2.88 waves**. For a two-sample comparison (port 5 salts vs oracle 5 salts, equal σ): `SE_diff = 2.32 × √(2/5) = 1.4673`, and the minimum difference detectable at 95 %/80 % is `(2.3060 + 0.8889) × 1.4673 = ` **≈ 4.7 waves**.
> ⚑ **The oracle's own `M0 → M-POL-2` effect is 153.0 → 153.2 = 0.2 waves.** **B-1 cannot see the effect the arm of record was built to show, by a factor of more than twenty.** *(Assumes normality, equal variance and independent salts — approximations at n = 5; the figure is an order-of-magnitude statement, not a power calculation of record.)* **This is why the EXACT rows carry the decision and the bands carry only findings.**

**C-3 · Multiplicity, and the discipline that follows from it.** With ~10 band rows each graded at a ~95 % width, **roughly one red by chance is the expectation under a perfectly correct port**. The response is **not** to widen (§ 4.4) and **not** to correct for multiplicity by re-drawing widths after the fact. The response is: a `STATISTICAL` verdict **states how many band rows red out of how many graded, beside the expected false-red count under gamora's own widths**. A single red band row is a finding to be named, not a fidelity failure.

**C-4 · The test vectors prove emitter agreement, not oracle agreement.** `ABS-TEST-VECTORS-SIM-SOURCED`: the 9 vectors are **emitter-restated, not sim-produced**. E-6 green proves the port agrees with the **emitter**. Oracle agreement is what the rest of this file is for (WARN-3).

**C-5 · The ORACLE config carries three known-bad live limbs, and T-A is honest with them only for `runtime ≡ sim`.** `WarCryLimb.I8_LEGACY` (the **retired invented literal 5.0**, which priced **19.43 %** of all incoming damage) · `PotionLimb.I4_EXCURSION_MAX` (θ = 0.49, **measured-falsified on 5 of its own 9 predicted actuations**) · `LifeMonitorLimb.POLL_AT_SLOT` (breakers poll a post-lift HP value; **Turtle 51 floor-ticks vs 41 seen, Menhir 13 vs 10**; in waves 151/153 the breaker was **off entirely**) — census (c-4). They are the defaults **for byte-identity of the fold-off arms**, which is correct for T-A and wrong for anything a human is asked to judge. **No design conclusion may be drawn from a T-A green.** Closure is sibling **S6**, out of scope.
> ⚑ **Charter L4 says "two oracle limbs are known-bad". The census names three.** Recorded here as a finding, not corrected here — the charter is not mine to edit (§ 9, OQ-3).

**C-6 · Cross-implementation rows are not salt-paired** (§ 3.0). A BAND row's agreement is distributional. There is no per-salt trajectory claim in this instrument and none may be made from it.

**C-7 · The two known wrong-steer traps in the pack are graded only indirectly.** `DS-SPAWN-SCATTER` (box vs the oracle's polar disc — census (c-9)) is caught by **E-7a/E-7b**, which is a *consequence* test, not a direct one. `player_kit.channel.hit_test_model = "point"` against the sim's uniform 3.0 m disc (census D8, *flagged not adjudicated*) has **no T-A row at all** and is caught only by the R2D-5 geometry-true probe and by the coverage table. **Named so that a green T-A is not read as clearing them.**

---

## § 7 · WHAT A T-A PASS LICENSES MATT TO BELIEVE — and what it does not

**It licenses exactly one sentence:**

> **Under the `ORACLE` configuration, the GDScript runtime derives the same fight from the same rules as the sealed Python sim, to the resolution stated in § 6 — and therefore the `PORT` term in a T-B miss is bounded, not eliminated, to that resolution.**

**It does not license:**

- **Anything about `PLAY`.** Every declared divergence (`DIV-01 … DIV-15`) is **ungraded by T-A by construction** — that is what the two-config design is *for*. A T-A pass says nothing about the walled ring, the lethal pools, the per-skill interrupt flag, the auto-resume, the bound-skill additions, the banner placement, the potion in a human hand, or `u`.
- **Anything about model-vs-Grim-Dawn.** T-A grades `runtime ≡ sim`. `sim ≡ Matt` is T-B, and `sim ≡ Matt's eye` is T-C. **L-88 already reported that question open** (the corrected channel policy moved terminal wave 153.0 → 153.2 against a referent 160).
- **Any design conclusion**, because of C-5's three known-bad limbs.
- **Any localisation of a divergence** (C-1), **any small-effect claim on the terminal wave** (C-2), or **any claim that the port agrees with the oracle on the 9 vectors** (C-4 — it agrees with the *emitter*).
- **"The build plays like Matt."** The § 0 rubric declaration is on the report's face for exactly this reason.

---

## § 8 · FRAMING AUDIT — pointed at this prereg

*The SPEC-AUTHOR reflex, Q1–Q3, applied to my own instrument. Three assumptions ordered by what their falsity costs. The first is the answer.*

### ⚑ THE assumption: *an inertness RELATION transfers across implementations.*

Everything decisive in this prereg rests on E-2/E-3/E-4. The oracle asserts `M-POL-2-NULL ≡ M0` **in Python**; the port asserts `port(NULL) ≡ port(M0)` **in GDScript**. A GDScript run cannot reproduce a Python digest, so what transfers is **the relation, run-internal** — and the relation is a property of the **rules** only if disarming a fold removes draws *without shifting any other site's stream position*. The sim has that property because **each stream is deliberately disjoint (`D-I22-1`), which is precisely why each fold's off-state is provable by digest**. A port that shares one RNG across draw sites will **fail E-2 and E-3 with every rule implemented correctly** — and the failure will look exactly like a port defect.

**If this is false, T-A is meaningless**: the EXACT rows carry the decision (C-2 shows the bands cannot), and this assumption sits under three of them.

**Cheapest refuting test — pre-registered as precondition P-2, ≈ one headless run:** run one arm at one salt twice, once with a **no-op fold inserted that draws zero values**, and assert identical digests. A fold that draws nothing must not move the stream. *(And note the recursion, which is the honest part: `D-I22-1` names the discipline, and census W11 says the **registry does not yet describe it** — the port's per-site stream assignment is a RUNTIME-CHOICE ledger row unless V9 lands.)*

### Runner-up 1: *the oracle's statistics were computed on the denominator the census describes.*

If false, every BAND row is graded against a number that does not mean what this prereg says it means, and a red is a non-reason — *"the single easiest way to fail T-A for a non-reason"* (census § 3d item 3). **There is already positive evidence against it**: the per-salt uptime and release-duty ranges are not complements while the pooled pair sums to exactly 1 (§ 3.3, B-7). **Cheapest refuting test:** gamora reads the five per-salt `(uptime, duty)` pairs from `[M-POL2]` and checks `u_s + d_s = 1` for every salt. **One read, no sim run.**

### Runner-up 2: *the port can be CONFIGURED to the oracle.*

If V0 is incomplete or mis-transcribed, T-A grades a **configuration** difference and calls it a **port** bug — the census says so in those words. Several module defaults already differ from the cell of record, and `PlayerSustainFold.limb` **has no default and raises**. **Cheapest refuting test:** the runtime prints its **resolved** limb set into the verdict header (`v0_limb_set`) and it is diffed line-by-line against V0 **before** any row is read. A one-line diff, run automatically, on every graded run.

---

## § 9 · OPEN QUESTIONS TO THE CONDUCTOR — one recommendation each, stated first

**OQ-1 · The fifth arm.** **Recommendation: RUN `M0`.** Four arms give one checkable inertness pair; five give two independent pairs plus the E-4 distinctness falsifier, for four extra headless runs at zero risk. `M-POL-2-NULL`'s oracle-side relation is **to `M0`**, not to `M-POL-2`, so without `M0` in the port's matrix E-2 is not evaluable at all — the charter's "at minimum" set is one arm short of its own EXACT rows.

**OQ-2 · The conditional rows (B-2, B-10, B-12).** **Recommendation: declare them UNGRADEABLE at prereg time unless gamora names a key path in `[M-POL2]`/`[W1W]` for the arm of record — never grade them against `[MECH]`.** Cross-arm grading measures a configuration difference; that is the one failure V0 exists to prevent, and it would land inside the rows the charter names most prominently.

**OQ-3 · Charter L4 says two known-bad limbs; the census names three** (War Cry `I8_LEGACY`, Potion `I4_EXCURSION_MAX`, LifeMonitor `POLL_AT_SLOT`). **Recommendation: correct L4 to three at the next charter touch and name all three on the handoff's "what this build does not do" page.** Two of the three are ones a human will *feel* (census c-4); disclosing two of three is the shape of disclosure that gets discovered at the controls.

**OQ-4 · E-7b's class is conditional on a value nobody has read yet.** **Recommendation: gamora reads `n_wall_clamps_{body,player}` from `[W1W]` BEFORE the W1 seal and the class is fixed then** — EXACT if zero, BAND if not. A reclassification *after* a graded run is a HALT (§ 0), so this must be settled while it is still free.

**OQ-5 · WARN-2's PARTIAL is discharged in the register, not here.** The charter § 2 line fuses `placeholder/instrument` into one attribution slot; the register unfuses it by folding **placeholder into declared divergence** (every placeholder in this build has a `DIV` row by construction, per R-KP-0e) and giving **instrument** its own class. **Recommendation: adopt the register's five classes and update charter § 2's wording at the next touch.** The two have different remedies — re-author an asset vs re-compute a denominator — which is jack-ryan's objection, and it is right.

---

## § 10 · CHANGE PROTOCOL (restated at the foot, because this is where a future reader will look)

1. **This file is immutable on commit.** Typographic repair that changes no predicate, no denominator, no class and no threshold is permitted and must be recorded in the commit message as `prereg typo, no predicate change`.
2. **Any change to a predicate, denominator, class, threshold, arm set, precondition or taxonomy is a NEW dated prereg version**, carrying what changed and why.
3. **A change of any kind made after a graded run exists against this version is a HALT to Matt.**
4. **The band-widths companion is immutable on the same terms**, from the moment the two files are cross-pinned by sha at the W1 seal.

---

*Filed 2026-09-20 by gandalf (named sub-agent, `SPEC-AUTHOR`), **Wave 1 of Run KC2-PLAY**. Decision rules only — **no band width is authored here and none is defaulted anywhere**. **K-7 held:** every sealed cell named above was reached by digest, and this document asks for no re-run of one. **Law 3 held:** every number is quoted with its source or derived in the open from one. **D4 held:** committed before any graded run exists. No production code, no dispatch, no push.*
