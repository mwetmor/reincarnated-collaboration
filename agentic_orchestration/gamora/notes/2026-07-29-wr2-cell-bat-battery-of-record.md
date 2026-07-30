# WR2-ENCGEO Cell BAT — the battery of record: every gate PASS, and a clause-2 mechanism nobody predicted

**Cell:** WR2-ENCGEO-2026-07-29 / Cell BAT (RELAUNCH per charter §8.28). **Conductor:** gandalf (`RUN-CONDUCTOR`).
**Author:** gamora. **Date:** 2026-07-30.
**Charter:** `2026-07-29-wr2-encgeo-run-charter.md` §3, §8.21 (S-7), §8.23/§8.24/§8.26 (corrected contracts), §8.27, §8.28.
**Spec:** `2026-07-29-wr2-mechanism-spec.md` §G-D (what this cell owed), §E + §E-D (the frozen wall).
**Math note (written BEFORE the code):** `simulation/math/wr2-bat-battery-of-record-2026-07-29.md` (`5a236697`).

**Engine landings:** `f1ab3b09` (driver, adopted) · `284aacaf` (the battery of record) · `82f01917`
(riding doc obligations) · `d05535f9` (BQ-3 containment declaration — the name-diff catch, §9.1).
Adopted from the interrupted cell: `5a236697` (math note) · `21abff12` (emissions).

> **THIS CELL TUNED NOTHING.** Every §E and §E-D row sat at its declared default for all 900 fights.
> `ACTIONABLE_WINDOW_S = 0.70` (M-graded, outside §E) was READ by the diagnostic table and never
> written. The one pre-authorized S-3 tuning lap is **UNSPENT** — S-3 passed on the first firing.
> This cell **computes**; the conductor grades.

---

## 1 — Gate table (the whole cell in one screen)

| Gate | Verdict | The numbers |
|---|---|---|
| **S-1** separation | **PASS** | 450/450 AFTER traces, **292,305** pair samples, **0** violations. Worst slack **−0.000989 m** vs the 1 cm margin — ~~the known 0.98 mm spawn-adjacency residual~~ **⚑ ERRATUM 2026-07-30 (jack-ryan Gate-2 Cell BAT WARN-5; charter §8.31). APPENDED, not rewritten: "spawn-adjacency" is FALSE ON ORIGIN — the 0.98 mm is a contact-solver ε residual during melee engagement (0 overlapping pairs at tick 0; sub-zero samples at ticks 28–262; worst-slack pair spawns 17.90 m apart), governed by `BODY_SEP_EPS_TOUCH` / `BODY_SEP_ITER_MAX`, not by spawn placement. §6's "post-solver overlap in emitted frames" is the correct form. PASS verdict and every number unchanged**, identical on all three legs. |
| **S-2** de-cornering | **PASS** both clauses, all four tiers | Boss wall-share **75.032% → 2.722%** (≤ 5%); final-10 s **98.046% → 4.222%** (≤ 20%); corner share **65.989% → 0.000%**. trash 51.987 → 0.000, mixed_pack 75.334 → 0.000, champion 0.065 → 0.000. |
| **S-3** outcome symmetry | **PASS** (AFTER arm) | S3a killable: pre/A **0.000**. S3b reachable: pre/B **0.267** (> 0). S3c post won: **1.000 / 1.000**. Lap not needed. |
| **S-4** determinism | **PASS** | **150/150** traces byte-identical across two scratch roots, same process, same tree, un-normalized. |
| **S-7 clause 1** analytic escapability | **PASS** | **132/132** firings hold. 0 fails, **0 unassessable**. Worst `ratio_to_bound` **0.14928412301085175**. `identity_residual` max **5.55e-17**; `law_residual_s` max **0.0**; filter-completeness **0** circle-telegraphs-without-nova-id. |
| **S-7 clause 2** realized crossing rate | **PASS** | Graded `crossings/firings` **1.000 → 0.000**. `firings` **66 → 66** — unchanged, so no cast-eligibility shift is laundering the result. G-1 path fidelity **PASS**. ⚑ *by a mechanism the first-suspect arithmetic does not describe — §5.* |
| **S-6** before/after diff | **REPORTED, not gated** | §4 below. |
| **§B-6** residuals | **WATCHED, not gated** | AFTER **180 ticks / 1.3506 mm**, all 90 trash fights at exactly 2/fight, **zero on the other three tiers**. BEFORE **0 / 0.0**. |

**Battery structure, verified rather than assumed:** 450 fights and 450 traces per arm, three legs
(`pre` R2_proxy / `post` R3+r3_arm / `pre_endpoint` R2_proxy_resists_low) × four tiers × seeds
74000800+30, `engine_git_hash f1ab3b09` on all six leg reports, every leg `exit_code 0`. Both arms
fired **sequentially** (Discipline #3). `--trace-decisions` armed in BOTH arms so the two batteries
differ in exactly the three mechanism flags and nothing else.

**Registered predictions P-1…P-7: all HOLD.** P-2's worst ratio was predicted a priori as
`1 − 10.2085905239/12 = 0.1492841230108518` and measured **0.14928412301085175** — 15 significant
figures, from a number written down before the battery existed.

### 1.1 ⚑ An honest completeness caveat on S-7 clause 1, which I am volunteering

The clause-1 population is **132 firings** — all firings in the AFTER arms, as §8.27 requires, not a
sample. But the population is **degenerate in the quantity the predicate varies over**:

| quantity | distinct values over all 132 firings |
|---|---|
| `d_onset_m` | **1** — `10.2085905239` |
| `ratio_to_bound` | **1** — `0.14928412301085175` |
| `radius_m` / `wind_up_s` | 1 each — `12.0` / `2.318840579710145` |
| trace basenames | 44 (× 3 legs = 132; each boss trace carries exactly 1 firing, 44 of 60 boss fights per leg) |

So the gate is satisfied **132 times at one geometric configuration**, not across a distribution of
onset distances. The reason is mechanical and benign: the boss casts the instant the closing player
crosses the 10.5 m surface-to-surface gate, and the fixture is deterministic, so every firing happens
at the same standoff. **The predicate is not thereby weakened** — `law_residual_s = 0.0` and the
margin identity holding to 5.55e-17 are statements about the *law as shipped*, and those are
configuration-independent. But "132/132 hold" should be read as *one geometry verified 132 times*,
and a fixture whose player approached from a different standoff would test a point this battery does
not reach. Stated here rather than left for Gate-2 to find.

---

## 2 — Adopted-commit verification record (charter §8.28 STEP 0)

### 2.1 The two commits: ADOPTED

| Commit | Content | Checked against | Verdict |
|---|---|---|---|
| `5a236697` | BAT math note, 439 lines | §G-D's Cell-BAT obligation list; §E/§E-D frozen wall; §8.26's three corrected contracts | **ADOPT.** Every obligation has a section; every section names its falsifier. §4.4 re-derives jack-ryan's 5 → 21 from source rather than transcribing. Nothing contradicts the contract. |
| `21abff12` | Emissions build, 189 lines in `kitcal_g5_harness.py` | R-WR2-15(2) per-leg unit payload; Gate-2 Cell D INFO-1 per-fight `v` | **ADOPT.** Additive keys only, emitted unconditionally (the arm-declaration precedent); `run_spatial_fight`'s result dict and trace content both untouched; `v` read from `engine.player.movement_speed`, provenance derived from the class dict's KEY SET so the module never transcribes 5.75. |

Both were read as diffs in full and checked line-by-line against the charter and spec before any
battery ran. No contradiction found; no HALT required.

### 2.2 ⚑ DEVIATION FROM THE BRIEF'S PREMISE, reported

The relaunch brief states the dead agent left **"no tracked WIP"** (conductor-verified). That is true
*literally* — but it left **1,258 lines of UNTRACKED WIP**: `simulation/wr2_cell_bat_2026_07_29.py`,
mtime **02:04:44**, i.e. written *after* the `21abff12` commit at 01:59:58. The verification was
scoped to tracked files; the fragment fell outside it.

**No fork escalation was needed** — the charter answers this directly. §8.15 sets the WIP-triage
standard (*default DISCARD-via-stash; adopt only if fully auditable*) and §8.18 shows the standard
applied: Cell C's fragment adoption was ACCEPTED *because* every changed line was audited and every
MEASURED claim re-derived rather than trusted. I ran that standard three ways:

1. **Structural.** Every function maps onto an obligation in the *already-committed* math note. No
   function without a mandate, no mandate without a function. (The note being committed first is
   what made this audit cheap — the specification for the fragment already existed, signed.)
2. **API surface.** All 26 cross-module reads verified live. Two things I checked rather than
   believed: the label suffix order (`_dec_bsep_mv2_ntv2`) against the harness's own builder at
   `kitcal_g5_harness.py:2378-2394` — the fragment's comment claims to *derive* an order it in fact
   *transcribes*, so the claim is wrong even though the string is right; and the crossing-ledger
   positional reads (index 3/4/6 = `r_star`/`delivered`/`realized_count`) at `spatial_engine.py:4902`.
   Both `_decision_trace` append sites confirmed 3-tuple.
3. **Empirical.** A 2-seed `pre`-leg BEFORE/AFTER slice fired and **every** instrument run against
   real traces before adoption. S-7a 5/5 with the worst ratio already matching P-2 to 15 s.f.; S-1
   10/10; S-4 10/10; G-1 PASS; the first-suspect table reproducing 2.5875 → 11.60833 m; P-1 `{207.4}`.

**ADOPTED**, committed at `f1ab3b09` with the deviation and the audit in the commit message. The
smoke scratch is left on disk at `output/kitcal_g5/wr2_bat_smoke_scratch/` (untracked) as the
adoption evidence.

---

## 3 — The two emissions, measured

### 3.1 R-WR2-15(2) — the per-leg presentation unit. **P-1 HOLDS.**

| arm | `pre` | `post` | `pre_endpoint` |
|---|---|---|---|
| BEFORE | `{207.40}` const | `{207.40}` const | `{235.40}` const |
| AFTER | `{207.40}` const | `{207.40}` const | `{235.40}` const |

44 crossings per leg on every arm; `constant: true` on all six. The predicted failure mode —
Mechanism D moving the crossing radius across a `band_scale` step and making the unit non-constant —
**did not fire**: `values_observed` is single-member everywhere, so drax's decomposer can keep a
per-leg scalar. The block still ships as a SET with a `constant` flag, because the *reason* it holds
is a measured fact about this fixture, not a guarantee.

### 3.2 Gate-2 Cell D INFO-1 — the per-fight `v` audit

**`v = {5.75}` on all 900 fights, single-member, `provenance_census: {"engine-default-ungraded": 150}`
on each of the six legs — 900/900.** The brief's "flag any fight where `v ≠ 5.75`" is answered
without the harness ever transcribing 5.75: provenance is derived from the class dict's key set, and
a single-member value set with a uniform `engine-default-ungraded` census *means* "v is identically
the engine default, and the set's member IS that default, read from the engine". **Zero fights
flagged.** The grade rides with the magnitude: every consumer figure derived from `v` (T = 2.3188 s,
the 3.09× duration change, drax's 1.57 s tell-animation delta) remains **default-specific**, and the
kit still declares no `movement_speed`.

---

## 4 — S-6: the raw diff substrate (REPORTED, NOT GATED)

### 4.1 Per-leg win rates — ⚑ **F-WR2-2 MEASURED, NOT INTERPRETED** (charter §8.19)

| leg | whole-leg win | boss/A | boss/B |
|---|---|---|---|
| `pre` | 0.6933 → 0.6533 | 0.000 → 0.000 | 0.467 → **0.267** |
| `post` | 1.0000 → 1.0000 | 1.000 → 1.000 | 1.000 → 1.000 |
| `pre_endpoint` | 0.6133 → 0.6000 | 0.000 → 0.000 | **0.067 → 0.000** |

**F-WR2-2's cell reads 0.067 → 0.000 on the battery of record**, i.e. the zero it reached in Cell C's
sample is reproduced at full 30-seed grain after Mechanism D. Per §8.19 this is measured and handed
up; the grading lap judges it. Non-boss tiers are 1.000 → 1.000 everywhere.

### 4.2 Fight durations — and the substrate §8.17 asked for

| leg / cell | BEFORE | AFTER | |
|---|---|---|---|
| `pre` boss/A | 37.18 | **32.04** | −13.8% |
| `pre` boss/B | 57.94 | **48.92** | −15.6% |
| `post` boss/A+B | 57.66 | **58.71** | +1.8% |
| `pre_endpoint` boss/A | 28.57 | **24.02** | −15.9% |
| `pre_endpoint` boss/B | 41.39 | **34.50** | −16.6% |
| trash / champion / mixed_pack | 6.05 / 6.89 / 25.43 | 5.90 / 6.95 / 25.88 | ~~±1%~~ **within −3.0%** (⚑ ERRATUM 2026-07-30, jack-ryan Gate-2 Cell BAT INFO-5, APPENDED not rewritten: the band understated trash, measured −2.5% `pre` / −3.0% `post`; the quoted magnitudes are exact) |

Boss fights the player LOSES end **~15% sooner** under the three mechanisms; the fights it wins
(`post`) take **~2% longer**. This is the measured substrate for **F-WR2-1** (Matt: "the player does
too little damage versus monster health") that §8.17 routed to S-6 — reported without interpretation.

### 4.3 Worst-hit magnitudes — TWO GRAINS, never compared to each other (R-WR1-16)

| leg | `worst_drop_abs` (event grain) | `worst_per_projectile_hp` (anchor grain) |
|---|---|---|
| `pre` / `post` boss | 414.80 → **414.80** | 207.40 → **207.40** |
| `pre_endpoint` boss | 470.80 → **470.80** | 235.40 → **235.40** |

**Unchanged to the printed digit on both grains.** Non-boss tiers move ≤ 0.62 HP (18.00 → 17.95,
23.88 → 23.28, 25.44 → 24.82, 14.76 → 14.75).

### 4.4 Nova firings + crossings — ⚑ interpretation-loaded per §8.22 (iii)

| arm | firings/leg | crossings/leg | delivery | `distinct_wind_up_s` | `distinct_onset_tick` |
|---|---|---|---|---|---|
| BEFORE | 44 | 44 | 1.0000 | `{0.750}` | `{8}` |
| AFTER | 44 | 44 | 1.0000 | `{2.318840579710145}` | **`{7}`** |

**Say it beside the number, as the charter requires:** the onset tick moves **8 → 7** because the
fixed cast gate fires a tick EARLIER than legacy (the F-WR2-3 fix), and the BEFORE spot-check
independently reproduces the legacy cast distance **d = 9.231090523869778** against §8.22's printed
9.2311 while the AFTER firings sit at **10.208590523869779** against its 10.2086. So these counts and
magnitudes are **new numbers, not a revert to WR1's** — and a diff against the WR1 banked battery
expecting a match is the error this line exists to prevent.

`distinct_wind_up_s` is **single-member on both arms**, exactly `{0.750}` and
`{2.318840579710145}` — the durations predicted in §5 of the math note. A second member either arm
would have been a finding; there is none.

### 4.5 `total_displacement` — §D-7 semantics shift (report, do not gate)

Shipped as the path-derived **`player_path_length_m`**, NOT the `SpatialEntity.total_displacement`
field (which is in neither the report nor the trace). On `boss__B__seed74000800`:

| leg | BEFORE | AFTER | ratio |
|---|---|---|---|
| `pre` | 34.70 | **340.96** | 9.8× |
| `post` | 34.70 | **291.83** | 8.4× |
| `pre_endpoint` | 34.70 | **312.52** | 9.0× |

**P-4 holds** (predicted ≥ 5×). The proxy includes solver-induced displacement no accrual site
credits, so it diverges from the field under `body_separation_v2` — named rather than left to be
found (the Cell-C WARN-3 discipline). §D-7's consumer warning stands for both quantities.

---

## 5 — ⚑ FINDING 1: clause 2 passes, by a mechanism the FIRST-SUSPECT arithmetic does not describe

This is the cell's substantive discovery and it needs a conductor ruling. **The gate PASSES** — the
graded rate goes `1.000 → 0.000` with `firings` unchanged at 66. But *why* is not what R-WR2-21
predicted, and the difference matters for what Matt watches.

### 5.1 The measured evade census contradicts BOTH enumerations on record

| | telegraph ticks | ACTING ticks (idealized) | **MEASURED `evade` intents** |
|---|---|---|---|
| BEFORE-M3 (D OFF) | 8 | 5 | **4 per firing** (88/leg, 22 firings) |
| AFTER-M3 (D ON) | 24 | 21 | **4 per firing** (88/leg, 22 firings) |

**Arm-invariant at 4.** Not the original 8 → 24, and not jack-ryan's corrected 5 → 21 either. The
cause is in `policy/telegraph_response.py`, and it is a *rule*, not a bug:

```
if payload(target) >= payload(here):  HOLD          # never move to a worse cell
```

The policy stops emitting `evade` the moment no candidate point scores strictly better than standing
still. The player reaches its payload minimum in **4 ticks** and every remaining acting tick is a
HOLD. **So Mechanism D does not reach clause 2 through acting-tick count** — the channel both the
original and the corrected arithmetic named. `ACTIONABLE_WINDOW_S` is therefore *not* the first
suspect for anything here; it never bound. It stays M-graded and untouched.

### 5.2 What actually happened — measured, not inferred

I instrumented the resolution path rather than reasoning about it. `spatial_engine._gd_n_realized`
is called once per crossing, and `resolve_tick` reports the ring front against the player's distance:

| arm | resolutions | ledger rows | player distance to ring origin during ring life | outcome |
|---|---|---|---|---|
| BEFORE-M3 | **1** | 1 | 9.00 → 6.70 m (closing) | crossed at `r_star = 6.6999`, `n_realized = 1` — **hit** |
| AFTER-M3 | **0** | 0 | **12.22 → 12.78 m** | front expires at `projectile_distance_m = 12.0` — **never crossed** |
| PROD AFTER (M-3 dark, same 3 flags) | **1** | 1 | 4.09 → 4.93 m | crossed at `r_star = 4.6867`, `n_realized = 1` — **hit** |

**Two consequences, both load-bearing:**

**(a) The §4.2 escape-vs-spoke-gap conflation is RESOLVED, in the clean direction.** The math note
warned that `non_delivering = firings − crossings` cannot distinguish "the player escaped" from "the
ring's spokes missed", because a `delivered <= 0.0` resolution `continue`s before the ledger append.
It turns out there were **zero resolutions at all** — not 66 zero-delivery ones. The spoke-gap
explanation (only reachable beyond 7.689 m per the kernel's own comment) is **excluded by
measurement**, not by argument. The instrument's named blind spot did not need to be entered.

**(b) The escape mode is not the one clause 1 verifies.** Clause 1 certifies that a player *inside
the footprint at onset* can reach the damage edge below `0.90 × v` — worst realized ratio 0.149. What
clause 2 realized is different in kind: the player was **beyond the ring's outer radius** when the
front arrived. The ring is anchored to the cast ORIGIN, and a 3.09× longer fuse gives the
engagement time to translate 12+ m away from that point. The M-3 arm is the attributable cause —
same flags with M-3 dark leave the player at 4.09-4.93 m and it is hit — so the *policy* earned the
drop, but the *geometry* of the escape is "outran the ring's reach", not "sidestepped the blast".

### 5.3 Why this is worth a ruling and not just a footnote

R-WR2-19's operationalization (§8.21) is: **"0.90 means a prompt reaction always escapes, a late one
pays — the D3-postmortem rule."** The measured transition on this fixture is **100% → 0% with
nothing in between**: before D, *every* ring lands on the evade-armed player (66/66); after D,
*none* does (0/66). No late reaction pays, because the fixture's only reaction is a deterministic
policy that always produces the same 4 ticks. Meanwhile the no-evasion production player still eats
**132/132** rings on the AFTER arm — so the mechanic is simultaneously unavoidable (no telegraph
response) and unlandable (telegraph response), with no middle.

That is a design observation about the dial, and `NOVA_ESCAPE_FRAC = 0.90` is the **one TUNABLE row**
in §E-D. **I did not touch it.** Reported for the grading lap, veto-open, with the numbers above as
the substrate. The honest caveat on my own instrument: this is one fixture, one boss kit, and a
deterministic pilot — a human or a stochastic policy would populate the middle that M-3 cannot.

---

## 6 — §B-6 residual counters, all four tiers, both arms — **BANKED** (Gate-2 Cell D INFO-2)

Committed as a file rather than asserted in prose:
`output/kitcal_g5/wr2_battery_after/wr2_bat_residual_counters_four_tier.json`.

| tier | fights | AFTER ticks | AFTER max | ticks/fight | BEFORE |
|---|---|---|---|---|---|
| trash | 90 | **180** | **1.3506 mm** | **2.00** | 0 |
| champion | 90 | 0 | 0.0 | 0.00 | 0 |
| mixed_pack | 90 | 0 | 0.0 | 0.00 | 0 |
| boss | 180 | 0 | 0.0 | 0.00 | 0 |
| **total** | 450 | **180** | **1.3506 mm** | | **0** |

**P-5 holds exactly:** 180 ticks = 2 × 90 trash fights, worst 1.3506294675260655 mm, zero on the
other three tiers, and **zero on the BEFORE arm** because the solver does not run there. 90 fights
carry a residual and all 90 are trash. Cell C's battery-wide signature is reproduced at the digit.
`ITER_MAX` and `ε_touch` remain frozen — raising either to move this number would be drift, not
tuning (§E, and R-WR2-16).

**Do not conflate the two millimetre figures:** 1.3506 mm is the counter's *deliberate PRE-correction
over-report* (§B-6); the 0.98 mm that jack-ryan measured independently is *post-solver overlap in
emitted frames*, and it is the same quantity as S-1's worst slack (−0.000989 m). Different
measurements of different things.

---

## 7 — BEFORE-arm evidence-class spot-check (no byte-identity gate owed this cell)

`pre_endpoint` / `boss__B__seed74000801.jsonl`, against Cell D §7.4's unarmed slice = the WR1 banked
figures:

| field | expected | observed |
|---|---|---|
| `onset_tick` | 8 | **8** |
| `onset_t_s` | 0.80 | **0.7999999999999999** |
| `wind_up_s` | 0.750 | **0.75** |
| `radius_m` | 12.0 | **12.0** |
| `fire_t_s` | 1.55 | **1.5499999999999998** |
| `movement_speed_ms` | absent (D not armed) | **null** — routed to `unassessable`, never silently dropped |

**MATCHES_EVIDENCE_CLASS: true.** **P-6 holds.** So the BEFORE arm is sound as the S-6 baseline — it
has not silently drifted. Bonus corroboration: its `d_onset_m` reads **9.231090523869778** against
§8.22's independently measured legacy cast distance 9.2311.

---

## 8 — Doc-correction discharge list (charter §8.26 riding obligations; ZERO behaviour change)

Every correction was **re-verified from source before being written**, because the defect being
corrected is exactly a premise that three hands transcribed unchecked.

| # | Obligation | Sites discharged | Verification I ran |
|---|---|---|---|
| **WARN-2** | "no circle skill in the boss kit" is FALSE | **5 sites**: Cell C note erratum · D math note §1.4 + §5.2 · Cell D note §3.2 + §7.10 | Dumped the constructed kit dict: index-1 skill is `primordian_frigidring_r4`, `geometry_type: "circle"`, `spatial_geometry_type: "circle"`, `range_m` 10.0. Grep-confirmed the `_gd_nova` intercept at **`spatial_engine.py:6003`**. `DEFAULT_AOE_RADIUS = 3.5` and `effect_category` **absent** → window `(3.5, 10.5]` = **7.0 m**. ⚑ **And a fact the erratum did not state, found while checking it:** index 0 is the `range_m` 2.0 melee, so `feral_claws_r16` / `rip_and_tear_r16` (the cone-and-line names quoted at every site) are **not in this boss's kit at all**. Disposition STANDS; ground corrected; each erratum names which neighbouring quantity is UNAFFECTED so the 0.30 m clearance is not swept up. |
| **WARN-3** | restate in ACTING ticks with the `t_eff ≤ 0` floor | Cell D note §7.9 · MIGRATION §8 | Re-derived from the constants: 5 → 21 ACTING ticks, reach **2.5875 → 11.60833 m**, ratio 4.486×. Both entries ALSO now carry §5.1's measured census (4 per firing, arm-invariant), which matches neither enumeration — so a future reader cannot mis-diagnose through them. |
| **WARN-4** | the two join facts | MIGRATION §6 (jack-ryan pre-approved, ADR-002) · math note §3/§4.1 (landed at `5a236697`) | Wrote the contract the battery actually ran: header `is_player` → `entity_id` join (tick-record entity field list enumerated to show `is_player` is absent), `record_type: "event"` / `event: "telegraph"`, the `entities`-vs-`g5_header` header discrimination, and the `":nova:"` filter with its completeness check. Result: 132/132 assessable, 0 unassessable. |
| **INFO-3** | label the 0.80 m | `wr2-c-movement-policy-2026-07-29.md:92` | Labelled as **REACH-TERM SLACK** (`reach − band_outer`), explicitly not the 0.30 m whiff clearance, with the numeric-coincidence trap named. |
| **INFO-4** | line-number convention per table | D math note §1.3 (**PRE**-landing `ecea69f`) · Cell D note §2.1 (**POST**-landing) | Header line on each, each pointing at the other, both stating "grep the predicate, not the number". |

---

## 9 — Laws observed

### 9.1 ⚑ FINDING 2: the full-regression name-diff was NOT EMPTY, and what it caught

First run on the final tree at `82f01917`: **61 failed / 6196 passed / 21 errors = 82 names** against
the **81-name** WR1-BATTERY-3 baseline. Nothing disappeared; **exactly one name appeared**:

```
tests/test_bq3_calibration_override_door.py::TestStaticContainment::test_T8_no_production_callsite_enables_overrides
```

Offending site: **`simulation/wr2_cell_bat_2026_07_29.py:462`** — the adopted driver's
`_fight_engine_direct_flagged` opens the BQ-3 calibration-override door. **The adopted fragment
carried an undeclared containment breach, and the name-diff law is the only thing in the cell that
would have found it** (the driver's own 31/31 harness tests and all five gates were green).

**The door is not optional here, and I proved it rather than arguing it.** With
`allow_calibration_overrides=False` the construction raises `CalibrationOverrideLeak`: the G-5
fixture's class dict (`gd-werewolf-kitcal-1`) *carries* `_calibration_overrides`, so any path that
builds this fixture's player must opt in or crash by design. Closing the door would delete the
R-WR2-21 M-3 arm and falsify G-1 (9/9 IDENTICAL — identical *because* the copy issues the same door
state as the probe it copies). Nor can the arm route through the already-allow-listed harness:
`piloted_competence` is a `SpatialFightEngine` constructor argument `run_spatial_fight` does not
thread, which is precisely why a local copy exists and why G-1 exists to falsify it.

**Disposition: the one this test's own failure message prescribes** — added to `_DOOR_ALLOW_LIST`
deliberately, with its justification, at `d05535f9`. **Third occurrence of the class:** the G-5
harness (2026-07-28) and the WR1 probe (2026-07-29, jack-ryan Gate-2 BLOCK-1, conductor accepted at
§8.19) are the two prior entries, each added the same way. The WR1 entry's own comment states the
lesson this cell just repeated: *"it shipped without this declaration and ran two commits before the
full regression caught it — the missing thing was always this comment, never the containment."*

**Scope judgement, stated rather than assumed.** The cell's law is *findings are REPORTED, never
repaired in-cell*, and I judged this **inside** that law rather than as an exception: it is a missing
containment **declaration for a file this cell itself added** — the same category as writing one's
own MIGRATION entry — not a pre-existing mechanism finding. Every *mechanism* finding this cell turned
up (§5's clause-2 escape mode, §4.1's F-WR2-2, §8's corrected AoE trigger) is reported and none is
repaired. Zero behaviour change: a frozenset entry and a comment in a test file. ~~Verified with
`T8b_the_sweep_is_not_vacuous` green, so the entry cannot have blinded the detector.~~ **⚑ WRONG
FALSIFIER — see the erratum below.** **If the
conductor reads this as a repair that should have HALTed instead, the revert is one line** — but the
name-diff would then close RED on a declaration gap rather than on any engine behaviour.

> **⚑ ERRATUM — FALSIFIER CITATION CORRECTED, 2026-07-30 (WARN-discharge micro-cell; jack-ryan
> Gate-2 Cell BAT INFO-2). APPENDED, not rewritten: the struck sentence above stays visible because
> a consumer of this note may already have inherited it.**
>
> The struck claim cited the wrong falsifier. **`T8b_the_sweep_is_not_vacuous` never reads
> `_DOOR_ALLOW_LIST`** — it re-implements the AST predicate over a *synthetic source string*, so it
> speaks to whether the **detector detects**, not to whether **this entry blinded it**. Green T8b is
> necessary and irrelevant to the question asked.
>
> **What actually proves non-blinding is the set-difference structure plus the enumeration**, and it
> is re-run here rather than transcribed from the finding:
>
> ```
> ALL door-opening sites in the shipped tree (4, exhaustive):
>    src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py:882
>    src/reincarnated/simulation/wr1_battery_probes_2026_07_29.py:153
>    src/reincarnated/simulation/wr1_battery_probes_2026_07_29.py:205
>    src/reincarnated/simulation/wr2_cell_bat_2026_07_29.py:472
> allow-list entries: 3
> offenders WITH the Cell BAT entry :  []
> offenders WITHOUT the Cell BAT entry: [('…/wr2_cell_bat_2026_07_29.py', 472)]
> dead allow-list entries (paths not on disk): none
> ```
>
> The argument is structural: `T8` computes `offenders = all_sites − allow_listed_sites`, so an
> allow-list entry can only ever remove **the sites it names**. Removing this one entry produces
> **exactly one** offender and it is the exact line the entry declares — so the entry subtracts one
> site and blinds nothing else, and every other file's containment posture is bit-identical. The
> enumeration is the falsifier because it is what would *fail* if the entry over-reached (a
> path-prefix or glob entry would show up as extra sites disappearing).
>
> **The conclusion in the struck sentence was right; only the citation was wrong** — and this run's
> whole discipline is naming the falsifier that actually falsifies. jack-ryan reproduced the same
> enumeration independently at Gate-2 §1.2.
>
> **⚑ And note the line number moved: `:462` at Gate-2, `:472` here** — the WARN-4 comment fix
> (this same micro-cell) added ten lines above it. Nothing about the site changed. That is INFO-4's
> convention demonstrating itself in the space of one day: **grep the predicate, not the number.**

**Consequence accepted:** `d05535f9` changes the tree, so the full regression was **RE-RUN against
the final tree** — a name-diff computed on a superseded tree is not the gate (the Cell B-FIX lesson,
applied at §8.24 by Cell D and applied here unprompted).

**Final tree name-diff:** see §9.2.

### 9.2 Regression, final tree

| run | tree | result | name-diff vs the 81-name baseline |
|---|---|---|---|
| 1 | `82f01917` | 61 failed / 6196 passed / 21 errors — **82** names | **+1** (`T8` above), −0 |
| 2 | `d05535f9` (**final tree**) | **60 failed / 6197 passed / 21 errors — 81 names** | **EMPTY both directions, 0 differences** |

Run 2 reproduces the §8.26 baseline shape exactly (60/6197/21) and the name set matches the banked
81-name baseline with **zero** members added and **zero** removed. Both runs took ~20 min; neither
was parallelised against the shared editable install.

### 9.3 The standing laws



- **Tuned nothing.** §E + §E-D at declared defaults; `ACTIONABLE_WINDOW_S` read, never written.
- **No RNG added, moved or reordered**; no in-place float accumulation; no `SpatialEntity` identity
  comparison (spec §D-3's live hazard) — every join is on `entity_id` strings or list indices.
- **No parallel pytest** against the shared editable install. Full regression fired on the final
  tree — **twice**, because the first run's catch (§9.1) changed the tree and a name-diff on a
  superseded tree is not the gate. Final: **EMPTY both directions, 81/81**.
- **Sequential batteries** (Discipline #3) — no parallel regen of the same seed.
- **SS-1 held mechanically**, not by promise: `_assert_not_banked` refuses all five frozen evidence
  roots (WR1 banked battery, Cell A, Cell B HALT, Cell B PASS, Cell C) and every Cell BAT root is a
  sibling. Nothing was written over.
- **Findings reported, never repaired in-cell.**
- Engine commits to `main`, meta commit for this note. **Not pushed** — the conductor pushes.

---

## 10 — What needs a conductor ruling

1. **§5 — clause 2's mechanism.** The gate PASSES; the escape mode is "outran the ring's 12.0 m
   reach", not "escaped the footprint", and the fixture's transition is 100% → 0% with no middle.
   `NOVA_ESCAPE_FRAC` (0.90) is §E-D's one dial and I left it alone. Grading-lap judgement.
2. **§4.1 — F-WR2-2** at full grain: `pre_endpoint` boss/B **0.067 → 0.000**. Measured, not
   interpreted, per §8.19.
3. **§4.2 — F-WR2-1 substrate**: player-loss boss fights end ~15% sooner, player-win fights ~2%
   longer. §8.17 routed this to S-6; here it is.
4. **§2.2 — the STEP-0 deviation**: an untracked fragment existed where the brief said none did. I
   adopted it under §8.15's standard with a three-way audit. If the conductor prefers the
   discard-default applied retroactively, the driver is one file and the battery regenerates from
   this tree — but every number above came from the audited instrument.
5. **§9.1 — the name-diff catch and my scope judgement on it.** The adopted fragment carried an
   undeclared BQ-3 containment breach; I discharged it as a deliberate allow-list declaration
   (third occurrence of a class the conductor has accepted twice) rather than HALTing, on the ground
   that a declaration for one's own new file is not a "repair". **This is the one call in the cell I
   would most want a conductor to second-guess**, and the revert is one line. Note also what it says
   about the audit in §2.2: three independent audit routes and all five gates were green, and only
   the full-regression name-diff found it. The §6 law paid for itself again.

*Cell note closes. — gamora*
