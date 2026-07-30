# Finding — 2026-07-29 — Gate-2 on WR2-ENCGEO Cell BAT (the battery of record)

**Reviewer:** jack-ryan (DEV-MODE, Gate-2, BLOCK authority)
**Severity:** **CLEAR-with-notes** — 6 WARN, 6 INFO, **no BLOCK**. Grading + AFTER-baton RELEASE,
with WARN-1 gated to discharge *before* the baton ships.
**Target:** engine `5a236697` + `21abff12` + `f1ab3b09` + `284aacaf` + `82f01917` + `d05535f9`
reviewed as ONE landing atop `796a6f6d`; meta `144cbb4d` / `22f54914`
**Developer:** gamora
**Governing:** charter §3 (S-1…S-7) · §8.15/§8.18 (WIP-triage + fragment-adoption standard) ·
§8.21 (Mechanism D + S-7, MATT-SIGNED R-WR2-19) · §8.22 (iii) (interpretation load on the nova line) ·
§8.26 (the three corrected contracts) · §8.27/§8.28 (cell + interruption) · **§8.29 (conductor
rulings on this landing)** · spec §E + §E-D (frozen wall) · §G-D (Cell BAT's obligation class)
**Principles applied:** #1 math-before-code · #2 smoke-gate/evidence · #3 cross-seam impact ·
#4 decisions-log / ruling-ledger as truth · #5 severity matters
**Disciplines cited:** #1, #3, #8, #10, #11, #12
**ADRs:** ADR-002 (tiered approval) · ADR-004 (cross-seam handoff)

---

## 0. Verdict in one paragraph

Every pre-registered gate is **independently reproduced on my own instruments, and several to the
last printed digit**. S-1: I scanned all 450 AFTER traces myself and got **292,305 pair samples,
0 violations, worst slack −0.0009889945962079372 m** — gamora's number to 17 s.f., identical on all
three legs. S-2: my own clamp-predicate scan of both arms returns boss **75.032% → 2.722%**,
final-10 s **98.046% → 4.222%**, corner **65.989% → 0.000%**, trash 51.987 → 0.000, mixed_pack
75.334 → 0.000, champion 0.065 → 0.000 — every figure exact, and three of four tiers genuinely FAIL
on the BEFORE arm, so the instrument is validated on a known-failing corpus. S-3: recomputed from
the six leg reports — 0.000 / 0.267 / 1.000-1.000, lap correctly unspent. **S-7 clause 1 with my own
grader** written against the corrected contract: **132/132 hold, 0 unassessable, worst
`ratio_to_bound` 0.14928412301085175, `identity_residual` 5.551115123125783e-17,
`law_residual_s` 0.0, 0 circle-telegraphs-without-nova-id** — every quantity matching the banked
artifact bit for bit. **S-7 clause 2 I re-ran from my own engine construction** and got firings
22 → 22, crossings 22 → 0, rate **1.000 → 0.000**, evade **88 both arms (4.0/firing)**,
`r_star` 6.699906 — the cell's per-leg row exactly. S-4 I extended past what the cell claimed: **450/450
byte-identical across two of my own scratch roots on all three legs**, and — the stronger statement —
**all 450 banked traces regenerate from the current tree with `engine_git_hash` as the ONLY differing
field on the ONLY differing line**, which proves the two post-battery commits changed zero sim
behaviour empirically rather than by diff inspection. Full regression run **alone**: **60 failed /
6197 passed / 21 errors in 1202.96 s**, name-diff **EMPTY both directions, 81/81**. Residuals
re-derived from the leg reports: **180 ticks / 1.3506294675260655 mm, all 90 trash fights at exactly
2.00, zero on the other three tiers, BEFORE 0**. **TUNED NOTHING verified in source** — all eight
§E Mechanism-C dials, `BODY_SEP_ITER_MAX = 8`, `BODY_SEP_EPS_TOUCH = 0.001`, `NOVA_ESCAPE_FRAC = 0.9`
and `ACTIONABLE_WINDOW_S = 0.7` sit at their declared defaults, and the landing's diff touches no
engine module at all. **No BLOCK.** The six WARNs split into three classes: one real ADR-004 gap
(WARN-1), two conductor-ruling corrections that my own isolation arms forced (WARN-2, WARN-4), and
the familiar Cell-C/Cell-D family — *true where measured, wrong where labelled* (WARN-5 is again a
correction to **my own** prior finding).

---

## 1. Obligation 1 — the BQ-3 door discharge — **LEGITIMATE CONTAINMENT DECLARATION. No HALT was owed. I concur with the conductor, and I verified rather than deferred.**

This is the item the cell asked to be second-guessed and the conductor routed to me as the standing
safety. My answer is unambiguous, and it rests on four checks I ran myself.

### 1.1 The falsification, both ways, on my own instruments

```
class id: gd-werewolf-kitcal-1
has _calibration_overrides: True | keys: ['max_hp','armor','crit_chance','block_chance',
                                          'block_value','lifesteal_percent',
                                          'elemental_resistances','mitigation_law']
DOOR CLOSED -> raised: CalibrationOverrideLeak
DOOR OPEN   -> ok; movement_speed = 5.75
run_spatial_fight threads piloted_competence: False
SpatialFightEngine ctor arg:                  True
```

Both limbs of gamora's proof hold. The G-5 fixture's own class dict **carries** the override block,
so every path that builds this fixture's player must opt in **or crash by design** — closing the
door does not tighten containment, it deletes the arm. And `piloted_competence` is genuinely
absent from `run_spatial_fight`'s 30-parameter signature while present on the `SpatialFightEngine`
constructor, so the R-WR2-21 M-3 arm **cannot** route through the already-allow-listed harness.
Note the sharper form of this: `run_spatial_fight` *does* accept `allow_calibration_overrides`, so
the allow-listed path exists and still cannot reach the arm. The local copy is not a convenience.

### 1.2 The scope of the declaration, enumerated rather than asserted

I ran T-8's own AST sweep and then re-ran it with the new entry removed:

```
ALL door-opening sites in the shipped tree (4, exhaustive):
   spatial_gauntlet/kitcal_g5_harness.py:882      (allow-listed 2026-07-28)
   wr1_battery_probes_2026_07_29.py:153           (allow-listed 2026-07-29)
   wr1_battery_probes_2026_07_29.py:205           (allow-listed 2026-07-29)
   wr2_cell_bat_2026_07_29.py:462                 (this entry)
offenders WITH the Cell BAT entry :  []
offenders WITHOUT the Cell BAT entry: [('…/wr2_cell_bat_2026_07_29.py', 462)]
dead allow-list entries (paths not on disk): none
```

**Exactly one file, exactly one call site.** Removing the entry produces exactly one offender and it
is the line the cell names. Every other file's containment posture is bit-identical. `T8c` (the
key-literal sweep) and the `T7*` L4 production-boundary asserts are untouched — the diff is a single
hunk at `@@ -526,6 +526,28 @@`, 21 comment lines and one frozenset member, in a **test** file.
Suite green: **39 passed in 9.21 s**.

### 1.3 Why this is a declaration and not a repair

1. **The offending line was introduced by this cell's own commit** (`f1ab3b09`). A containment
   declaration for a file the cell itself added is landing completion — the same category as writing
   one's own MIGRATION entry — not the repair of a pre-existing mechanism finding. Every *mechanism*
   finding this cell turned up (§5's escape mode, §4.1's F-WR2-2, §8's corrected AoE trigger) is
   reported and none is repaired. The report-don't-repair law protects *other people's state*; it is
   not a prohibition on finishing your own.
2. **The act is the one the test prescribes, verbatim in source**: *"If this is a genuine calibration
   harness, add it to `_DOOR_ALLOW_LIST` deliberately."* I read that string in the assert message,
   not in the cell note.
3. **Zero behaviour change, proven empirically**: all 450 banked traces regenerate from the tree
   *including* `d05535f9` with `engine_git_hash` as the sole difference (§4.4). A HALT would have
   left the tree RED on a declaration gap with the engine bit-identical.
4. **Third occurrence of a twice-accepted class**, with the richest declaration of the three, and the
   regression correctly re-run on the final tree rather than reasoned about.

**Adoption did not contaminate the evidence.** The door state is identical to the allow-listed
probe's — which is *why* `verify_m3_path_fidelity()` reads 9/9 IDENTICAL — and the same overrides
were in force on the WR1 banked battery. Nothing in the 900 fights is void.

**Two notes ride this, neither disturbing the verdict:** the justification's cited falsifier is the
wrong one (**INFO-2**), and this is now 3-for-3 on "caught by a 20-minute regression when a
9-second suite was available" (**WARN-6**).

---

## 2. Obligation 2 — the STEP-0 adoption audit — **PASS on substance, and one claimed correction does not exist in the tree**

### 2.1 What I spot-verified, and it holds

| Audited claim | My check | Verdict |
|---|---|---|
| crossing-ledger indices 3/4/6 = `r_star`/`delivered`/`realized_count` | read the append at `spatial_engine.py:4902`: the tuple is `(tick, t_star, attack_id, r_star, delivered, by_element, _n)` | ✅ **exact** |
| ledger is PLAYER-ONLY | the append sits inside the branch that reads `_hp_before = self.player.hp` and passes `target=self.player` | ✅ |
| `delivered <= 0.0` `continue`s BEFORE the append | `:4846-4851`, verbatim | ✅ — the instrument caveat is honest |
| both `_decision_trace` append sites are 3-tuples | `:4735` `(tick, ring.attacker_id, _m3_intent)` and `:5579-5581` `(_tick_counter, entity_id, _intent)` | ✅ |
| suffix order matches the harness's own builder | `kitcal_g5_harness.py:2378-2394` builds `_dec` → `_bsep` → `_mv2` → `_ntv2` | ✅ string is right |
| the `HOLD` rule §5.1 quotes | `policy/telegraph_response.py:203` (docstring) implemented at `:286-288`, strict-improvement only | ✅ verbatim |
| structural mapping (function ↔ math-note obligation) | driver §1↔note §6, §2↔§4.1, §3↔§4.2/4.3/4.4, §4↔§5, §5↔§6/§7, §6↔§6, §7↔§6; emissions ↔ §2/§3 | ✅ no orphan function, no orphan mandate |
| math-before-code | `5a236697` 01:56:41 precedes `f1ab3b09` 06:45:12 by commit order, not by claim | ✅ Discipline #1 |
| SS-1 held mechanically | I called `_assert_not_banked` on all five frozen roots (**refused**) and all four Cell-BAT roots (**allowed**); `git status -uno` clean, so no banked artifact was written | ✅ |

The empirical limb of the adoption audit I effectively re-ran at full scale: the smoke slice's
S-7a worst ratio, S-1 worst slack, G-1 PASS and the first-suspect digits all reappear in my
450-trace reproductions below.

### 2.2 The gap — **WARN-4**

The audit's one identified defect **is still in the shipped file**. See WARN-4.

---

## 3. Obligation 3 — gate reproduction on my own instruments — **ALL PASS**

### 3.1 S-1 — **PASS, 17 s.f. identical**

```
traces=450  pair_samples=292305  violations=0  worst_slack=-0.0009889945962079372
  leg pre          : samples= 96426 viol=0 worst=-0.0009889945962079372
  leg pre_endpoint : samples= 89694 viol=0 worst=-0.0009889945962079372
  leg post         : samples=106185 viol=0 worst=-0.0009889945962079372
```

Every printed figure matches, including the leg-invariance of the worst value (it occurs exactly
9 times, 3 per leg). **10× headroom against the 1 cm gate.** The *characterization* of that residual
is wrong — **WARN-5**.

### 3.2 S-2 — **PASS both clauses, four tiers, and the instrument is validated on a failing corpus**

| tier | BEFORE wall / final-10 s / corner | AFTER wall / final-10 s / corner | S2a | S2b |
|---|---|---|---|---|
| trash | 51.987% / 51.987% / 0.000% | **0.000% / 0.000% / 0.000%** | ✅ | ✅ |
| champion | 0.065% / 0.065% / 0.000% | **0.000% / 0.000% / 0.000%** | ✅ | ✅ |
| mixed_pack | 75.334% / 100.000% / 32.838% | **0.000% / 0.000% / 0.000%** | ✅ | ✅ |
| boss | **75.032% / 98.046% / 65.989%** | **2.722% / 4.222% / 0.000%** | ✅ | ✅ |

Every AFTER and BEFORE figure in the cell's gate table reproduces exactly. Bonus cross-check: the
BEFORE arm independently reproduces WR1-ENV's banked `WR1_BEFORE_WALL_SHARE` table
(trash .5199, champion .0006, mixed .7533, boss .7503), so the BEFORE arm is a sound S-6 baseline
by a second route.

### 3.3 S-3 — **PASS, recomputed from the six leg reports**

| predicate | BEFORE | AFTER | pass |
|---|---|---|---|
| S3a killable — `pre` arm-A win rate | 0.000 | **0.000** | ✅ |
| S3b reachable — `pre` arm-B win rate | 0.467 | **0.267** (> 0) | ✅ |
| S3c `post` arm-A / arm-B | 1.000 / 1.000 | **1.000 / 1.000** | ✅ |

Lap correctly **UNSPENT**. One scope note: S3a is a win-rate proxy, not a band measurement —
**INFO-3**.

### 3.4 S-4 — **PASS, and I widened it**

The cell claimed 150/150 on one leg (`pre`). I ran **all three legs twice** into my own scratch roots:

```
X-vs-Y g5_…mitR2proxy…            identical 150/150 | vs BANKED hash-only 150/150 other 0
X-vs-Y g5_…mitR2proxyresistslow…  identical 150/150 | vs BANKED hash-only 150/150 other 0
X-vs-Y g5_r3arm…mitR3…            identical 150/150 | vs BANKED hash-only 150/150 other 0
TOTAL: 450/450 byte-identical; 450/450 hash-only vs banked
```

The second column is the stronger result and it was not claimed: **every one of the 450 banked AFTER
traces regenerates from the current tree, differing in exactly one field on exactly one line** —

```
--- line 0
    engine_git_hash: mine='d05535f9'  banked='f1ab3b09'
```

— 1,202 of 1,203 lines byte-identical on the trace I diffed field-by-field, and the same
one-field-one-line signature on all 450. That is simultaneously (a) S-4 at full battery scope,
(b) provenance proof that the banked evidence came from this tree, and (c) **empirical** proof that
`82f01917` and `d05535f9` changed zero sim behaviour. Recorded as **INFO-6**.

### 3.5 S-7 clause 1 — **PASS, my own grader, every quantity identical**

Written from the §8.26 contract (onset = `tick`; player via header `is_player` → `entity_id`;
`record_type: "event"` / `event: "telegraph"`; `":nova:"` filter), run over all 450 AFTER traces:

```
firings=132  assessable=132  unassessable=0  circle-telegraph-without-nova-id=0
HOLD 132/132   fails=0
worst ratio_to_bound: 0.14928412301085175
max |law_residual_s|: 0.0
max |identity residual|: 5.551115123125783e-17
distinct d_onset: ['10.208590523869779']   distinct R: [12.0]
distinct T: ['2.318840579710145']          distinct v: [5.75]
44 distinct boss trace basenames × 3 legs = 132
```

Identical to `wr2_bat_s7_firings.json` on every field. The degeneracy the cell volunteered is
**confirmed: one distinct `d_onset` over all 132 firings.** What the gate does and does not carry is
stated at **INFO-1**.

### 3.6 S-7 clause 2 — **PASS, re-run from my own engine construction**

I built the engine myself rather than calling the cell's `_fight_engine_direct_flagged`:

```
before_m3  (B,C,D)=(0,0,0)  firings=22 crossings=22 rate=1.0  evade=88 (4.0/firing) r_star=6.699906
after_m3   (B,C,D)=(1,1,1)  firings=22 crossings= 0 rate=0.0  evade=88 (4.0/firing) r_star=[]
```

The banked per-leg row exactly: firings unchanged, rate 1.000 → 0.000, `r_star` 6.699906 vs
6.69990598342503, and — **§5's FINDING 1 independently reproduced** — the evade census is
**arm-invariant at 4 per firing**, matching neither 8 → 24 nor my own corrected 5 → 21. Over three
legs that is 66 → 66 firings and 264 evade ticks per arm, as banked.

The corrected first-suspect arithmetic also re-derived from the constants, my own loop:

```
T=0.75                telegraph_ticks=8  acting_ticks=5  reach_ceiling=2.5875000000000004
T=2.318840579710145   telegraph_ticks=24 acting_ticks=21 reach_ceiling=11.60833333333333
ratio 4.486312399355876
```

---

## 4. Obligation 4 — the F-WR2-4 mechanism characterization — **CONFIRMED in geometry; the ATTRIBUTION in §8.29 is incomplete, and I have the arms that show it**

### 4.1 The escape geometry — confirmed, by instrumenting the live ring rather than the ledger

I snapshotted the scheduler's live rings each tick and measured the player's distance to the ring
**origin** across the ring's life:

| arm (M-3 armed on all) | dist to ring origin during ring life | crossings | outcome |
|---|---|---|---|
| `before_m3` (0,0,0) | **6.6999 → 8.4248 m** | 22/22 | crossed at `r_star` 6.699906 — **hit** |
| `after_m3` (1,1,1) | **12.1944 → 12.7789 m** | **0/22** | front expires at 12.0 — **never crossed** |

gamora's 12.22 → 12.78 and my 12.1944 → 12.7789 differ only in the first sample (my grid samples one
tick earlier than her `resolve_tick` instrumentation). **The load-bearing fact is confirmed and then
some: the minimum is 12.1944 m — the player is beyond the 12.0 m expiry radius for the *entire* ring
life,** so the front dies before reaching it. I also confirmed the mechanism in source:
`gd_nova.py:917` — `if r_star > ring.params.projectile_distance_m: continue  # the ring died before
reaching them`, which returns before the crossing is ever emitted.

The PROD-AFTER limb (M-3 dark, three flags armed) I verified from the **banked** traces: the player
sits at **4.06 → 5.34 m** from the ring origin across the ring life and **44 of 44 firings per leg
cross** (delivery 1.0000, three legs, 132/132). gamora's 4.09 → 4.93 is a single-fight window inside
that envelope; her `r_star` 4.6867 vs my tick-grid estimate 4.4306 is the sub-tick solve difference.
Direction and magnitude confirmed; digits not independently reproducible — **WARN-3**.

### 4.2 The attribution — two arms the battery does not contain, and they change the reading

Both the cell's arms toggle **all three** mechanism flags together, so nothing in the battery
isolates Mechanism D. I ran the two isolation arms:

| arm | dist to ring origin during ring life | firings | crossings | **rate/firing** |
|---|---|---|---|---|
| `before_m3` (B,C,D off) | 6.70 → 8.42 m | 22 | 22 | **1.000** |
| `bc_only_m3` (B+C on, **D dark**) | 7.98 → 11.43 m | 22 | **21** | **0.955** |
| `d_only_m3` (**D only**, B+C off) | 10.21 → 12.06 m | 31 | 16 | **0.516** |
| `after_m3` (all three) | 12.19 → 12.78 m | 22 | 0 | **0.000** |

**Neither mechanism alone produces the drop.** Movement-policy-v2's orbit with the legacy 0.75 s fuse
still eats **21 of 22 rings** and never clears 11.43 m; Mechanism D's 3.09× fuse alone removes
**48%** of them and grazes 12.06 m. The 0.000 is a *joint* effect: D supplies the time, C supplies
the path. This is the substance of **WARN-2** — §8.29 names only the carrier.

### 4.3 The degeneracy corollary — confirmed

One distinct `d_onset` (10.208590523869779) over all 132 firings, one distinct `ratio_to_bound`,
one `radius_m`, one `wind_up_s`, one `v`. §8.29's corollary is accurate as written.

---

## 5. Obligation 5 — residual counters — **PASS, re-derived from the leg reports**

| tier | fights | AFTER ticks | AFTER max_m | ticks/fight | BEFORE |
|---|---|---|---|---|---|
| trash | 90 | **180** | **0.0013506294675260655** | **2.00** | 0 |
| champion | 90 | 0 | 0.0 | 0.00 | 0 |
| mixed_pack | 90 | 0 | 0.0 | 0.00 | 0 |
| boss | 180 | 0 | 0.0 | 0.00 | 0 |
| **total** | 450 | **180** | **1.3506 mm** | | **0** |

`fights_with_residual = 90`, all trash. Reproduced independently of the banked artifact (I summed
`collision_residual_ticks` / `collision_residual_max_m` across the six leg reports myself) and the
artifact agrees. P-5 holds. `engine_git_hash = f1ab3b09` on all six leg reports, every leg present,
450 fights per arm.

The two-millimetre-figures warning in §6 of the cell note is correct and worth keeping: 1.3506 mm is
the counter's deliberate pre-correction over-report; 0.98 mm is post-solver overlap in emitted frames
and is the same quantity as S-1's worst slack. Different measurements of different things — but the
*origin* attributed to both is wrong (**WARN-5**).

---

## 6. Obligation 6 — full-regression name-diff — **PASS, EMPTY both directions, 81/81**

Run **ALONE** on the final tree `d05535f9`, nothing else holding the shared editable install:

```
python3 -m pytest tests/ -q -p no:randomly --tb=no -rfE
60 failed, 6197 passed, 3 warnings, 21 errors in 1202.96s (0:20:02)
```

| | count |
|---|---|
| observed FAILED+ERROR names | **81** |
| baseline names | **81** |
| **added** | **0** |
| **removed** | **0** |

All three totals match the cell's run 2 exactly (60 / 6197 / 21). `passed` is **unchanged from Cell
D's 6197**, which is the right expectation: Cell BAT ships no new test file, only an allow-list
member — so a moved test count would itself have been a finding. The tree was clean on tracked files
before and after.

I also confirmed the run-1 → run-2 sequence was necessary rather than ceremonial: with the entry
removed the sweep yields exactly one offender, so run 1's `82` names could only have closed to `81`
by the declaration landing. Re-running on the final tree was correct (the Cell B-FIX
`inspect.getsource` lesson, applied unprompted for the second gate running).

---

## 7. Obligation 7 — doc obligations, ZERO behaviour change — **ALL FIVE DISCHARGED, and the "zero" is now empirical**

`82f01917` touches exactly three `.md` files; `d05535f9` touches exactly one test file. No `.py`
under `src/` in either. And §4.4's 450/450 hash-only regeneration proves zero behaviour change
*empirically*, not by inspection.

| # | Obligation | My verification | Verdict |
|---|---|---|---|
| **WARN-2** | "no circle skill in the boss kit" is FALSE | I read the boss entity's own header block: index 0 `slith_wightmirecave01_attack` (point, 2.0), **index 1 `primordian_frigidring_r4` (circle, range_m 10.0)**. `_gd_nova` intercept confirmed at **`spatial_engine.py:6003`** — `if skill.get(_GD_NOVA_KEY) is not None:`. `DEFAULT_AOE_RADIUS = 3.5` confirmed at `:203`. Window `(3.5, 10.5]` = **7.0 m** | ✅ corrected at all 5 sites; append-not-rewrite erratum style; each erratum names the UNAFFECTED neighbour (the 0.30 m clearance) as I asked |
| | ⚑ gamora's *additional* finding | **CONFIRMED and it is a good catch:** `feral_claws_r16` (cone 2.0) and `rip_and_tear_r16` (line 14.0) are the **PLAYER's** skills in the header, not the boss's — the cone-and-line names quoted at every propagated site were never in this boss's kit | ✅ |
| **WARN-3** | restate in ACTING ticks with the `t_eff ≤ 0` floor | re-derived from the constants in my own loop: **5 → 21** acting ticks, **2.5875000000000004 → 11.60833333333333 m**, ratio **4.486312399355876** | ✅ exact, and both entries now also carry the measured 4-per-firing census |
| **WARN-4** | the two join facts | present at MIGRATION §6 + math note; my grader was written from this contract and returned 132/132 assessable, 0 unassessable — the contract is codeable, which is what the WARN asked for | ✅ (pre-approved under ADR-002) |
| **INFO-3** | label the 0.80 m | `wr2-c-movement-policy-2026-07-29.md` — labelled **REACH-TERM SLACK** (`reach − band_outer`, `3.50 − 2.70` / `2.50 − 1.70`), numeric-coincidence trap named | ✅ |
| **INFO-4** | line-number convention per table | header on the D math note table (PRE-landing `ecea69f`) pointing at the Cell D note §2.1 (POST-landing), both saying "grep the predicate, not the number" | ✅ |

---

## 8. Obligation 8 — emissions — **PASS, both, reproduced from all six leg reports**

### 8.1 R-WR2-15(2) — the per-leg unit payload. **P-1 holds.**

| arm | `pre` | `post` | `pre_endpoint` | crossings/leg | `constant` |
|---|---|---|---|---|---|
| BEFORE | `{207.4}` | `{207.4}` | `{235.4}` | 44 | true |
| AFTER | `{207.4}` | `{207.4}` | `{235.4}` | 44 | true |

`constant: true` on all six, `modal` present, `per_tier` present, block emitted **unconditionally**
on both arms (`nova_telegraph_v2_armed` correctly false on BEFORE). The predicted failure mode —
Mechanism D moving the crossing radius across a `band_scale` step and making the unit non-constant —
did not fire, and the block still ships as a SET with a flag. Right call.

### 8.2 Per-fight `v` with its grade. **900/900.**

`values_observed_ms = [5.75]`, `constant: true`, `provenance_census = {"engine-default-ungraded": 150}`
on each of the six legs = **900/900**, zero fights flagged. I confirmed the grade's ground
independently: `"movement_speed" in class_dict` is **False**, and `entity_from_class_dict` yields
`movement_speed = 5.75`. So the census is derived, not transcribed, and the derivation is correct.
Gate-2 Cell D INFO-1 is discharged properly — the magnitude ships with its grade, and the
default-specific consumer caveat rides.

**One gap, and it is the landing's only real process defect: no MIGRATION entry — WARN-1.**

---

## 9. Obligation 9 — S-6 substrate sanity — **INTERNALLY CONSISTENT, every table reproduced**

| §4.x | claim | my reproduction |
|---|---|---|
| 4.1 win rates | pre 0.6933→0.6533, boss/B 0.467→**0.267**; post 1.0000→1.0000 all cells; pre_endpoint 0.6133→0.6000, boss/B **0.067→0.000** | ✅ **exact**, F-WR2-2 confirmed at full 30-seed grain |
| 4.2 durations | pre boss/A 37.18→32.04 (−13.8%), boss/B 57.94→48.92 (−15.6%); post boss 57.66→58.71 (+1.8%); pre_endpoint boss/A 28.57→24.02 (−15.9%), boss/B 41.39→34.50 (−16.6%) | ✅ **exact** — F-WR2-1's substrate delivered as §8.17 routed it (see **INFO-5** on the ±1% band) |
| 4.3 worst hit, two grains | event grain (`intake.worst_drop_abs`) 414.80→414.80 / 470.80→470.80; anchor grain (`worst_per_projectile_hp`) 207.40→207.40 / 235.40→235.40; non-boss ≤ 0.62 HP | ✅ **exact on both grains**; largest non-boss delta is 25.44→24.82 = 0.62, so the bound is tight not loose |
| 4.4 nova counts | firings 44/leg and crossings 44/leg **both arms**, delivery 1.0000; `distinct_wind_up_s` `{0.750}`→`{2.318840579710145}`; `distinct_onset_tick` `{8}`→`{7}`; `d_onset` 9.231090523869778 → 10.208590523869779 | ✅ **exact**, from my own trace scan; the §8.22 (iii) tick-earlier caveat is stated beside the numbers as the charter requires |
| 4.5 `total_displacement` | shipped as path-derived `player_path_length_m`; boss__B__seed74000800: 34.70 → 340.96 / 291.83 / 312.52 | ✅ **exact to 14 s.f.** (34.70475917668015 → 340.9568953080204 / 291.83364079219285 / 312.52414787886346); P-4 holds; §D-7 semantics shift named rather than left to be found |
| §7 BEFORE spot-check | onset_tick 8, onset_t_s 0.7999999999999999, wind_up 0.75, radius 12.0, fire_t_s 1.5499999999999998, `movement_speed_ms` absent | ✅ **exact**; P-6 holds — but the substrate is untracked (**INFO-4**) |

Battery structure verified rather than assumed: 150 traces/leg = 60 boss + 30 champion +
30 mixed_pack + 30 trash, ×3 legs = 450 per arm; 44 of 60 boss fights per leg carry a firing;
`--trace-decisions` armed on **both** arms (BEFORE label carries `_dec`), so the two batteries differ
in exactly the three mechanism flags.

---

## 10. Obligation 10 — conductor-ruling check (§8.29) — two corrections

| §8.29 statement | my read |
|---|---|
| S-1 450/450, 292,305 samples, 0 violations, worst −0.000989 | **CONFIRMED** to 17 s.f. |
| S-2 75.032→2.722, 98.046→4.222, 65.989→0.000, 4/4 tiers | **CONFIRMED** exactly |
| S-3 holds, lap unspent | **CONFIRMED** |
| S-4 150/150 twice | **CONFIRMED**, and widened by me to 450/450 (INFO-6) |
| S-7 clause 1 132/132, worst 0.1493 = the a-priori prediction to 15 s.f. | **CONFIRMED** on my own grader |
| S-7 clause 2 rate 1.000→0.000, firings 66→66 | **CONFIRMED** on my own construction |
| residuals AFTER 180/1.3506 mm all trash 2/fight, BEFORE 0 | **CONFIRMED** |
| `v` 900/900 ungraded default 5.75 | **CONFIRMED** |
| name-diff EMPTY 81/81 | **CONFIRMED** |
| **BQ-3 discharge ACCEPTED; report-don't-repair** | **CONCUR** — §1, falsified both ways myself |
| F-WR2-4: escape is by outrunning reach, 12.22–12.78 vs 12.0 | **CONFIRMED** (12.1944–12.7789); mechanism confirmed in source at `gd_nova.py:917` |
| F-WR2-4: *"movement-v2 orbit carries it out of the nova's world entirely"* | **INCOMPLETE → WARN-2.** B+C armed with D dark reaches only 11.43 m and 21/22 rings still land |
| F-WR2-4: *"the transition is 100% → 0% with no middle"* | **TRUE in reaction-timing space, FALSE in mechanism space → WARN-2.** My isolation arms measure 0.955 and 0.516 on this very fixture |
| clause-1 population degenerate in onset geometry, gate not weakened | **CONFIRMED**, and see INFO-1 for the precise information content |
| STEP-0 deviation RATIFIED; *"corrected two wrong comment claims"* | **MISCHARACTERIZED → WARN-4.** One wrong claim was *identified* (not corrected, and it is still in the tree); the second item was *confirmed correct*, never a wrong claim |
| amendment: wreckage audits diff untracked files by mtime | **sound**, and it should also gain the 9-second containment check (**WARN-6**) |
| F-WR2-2 CONFIRMED at full grain; F-WR2-1 substrate delivered | **CONFIRMED** exactly |

---

## 11. WARN items

### WARN-1 — the two new cross-seam emission keys ship with NO MIGRATION entry, and four code comments point at one as if it exists (ADR-004)

`21abff12` adds three additive keys consumed **outside this seam**:

* `presentation_units` (leg-report block: `nova_unit_payload_hp` + `escape_law_input_v`)
* `movement_speed_ms` / `movement_speed_provenance` (per-fight `FightRecord`)
* `nova_per_projectile_hp` (per-fight `a_dmg1`)

`MIGRATION.md` carries **no entry for any of them**. It was not touched by `21abff12` at all, and
`82f01917` added only the WARN-3/WARN-4 doc corrections. Meanwhile four comment sites in
`kitcal_g5_harness.py` read *"ADDITIVE — MIGRATION.md 2026-07-30 WR2-ENCGEO Cell BAT entry"*,
pointing at an entry that does not exist.

**Rationale.** ADR-004 makes `MIGRATION.md` the cross-seam handoff artifact, and this emission's
entire purpose is cross-seam: R-WR2-15(2) exists so **drax's decomposer stops hard-coding
207.40 / 235.40**. Review principle #3 (cross-seam impact) and the run's own §8.24 standing rule
("consequence stated rather than discovered") both want the line. The cell's own code asserts it is
owed, which settles the question of standard.

**Why WARN and not BLOCK.** The keys are purely additive, no consumer breaks, the block is
unusually well self-documented in-payload (`definition`, `ruling`, `note`, `grade_note`), the report
baseline move IS declared (`report_baseline: "796a6f6d … + this cell's two additive keys"`), and the
actual ADR-004 handoff moment — the AFTER-baton — has **not happened yet**; Cell D INFO-5 already
routed the star-lord/drax acknowledgements to baton delivery. No consumer has been misled.

**Gate.** This must be discharged **before the AFTER-baton ships**, because the baton *is* the
handoff. Content is documentation-only: I pre-approve it under ADR-002 on the same basis as the
Cell D WARN-4 join-fact lines, so it need not wait on another gate.

### WARN-2 — §8.29's F-WR2-4 attribution names the carrier but not the enabler, and "no middle" is true of only one dimension

§8.29 banks F-WR2-4 with *"movement-v2 orbit carries it out of the nova's world entirely"* and
*"the transition is 100% → 0% with no middle."* Both are natural readings of the two arms the
battery contains — and both arms toggle all three flags together, so **nothing in the battery
isolates Mechanism D.** I ran the two missing arms:

| arm | max dist reached during ring life | rate/firing |
|---|---|---|
| B+C armed, **D dark** | 11.43 m (never clears 12.0) | **0.955** — 21 of 22 rings still land |
| **D armed alone** | 12.06 m | **0.516** — 16 of 31 land |
| all three | 12.78 m | 0.000 |

**The orbit is the path; the 3.09× fuse is what makes the path long enough.** On the single-mechanism
evidence Mechanism D is the *larger* contributor (−0.484 vs −0.045). And a graded middle **exists on
this very fixture** — 0.955 and 0.516 — even though it does not exist along the reaction-timing axis
(where the deterministic policy always yields the same 4 ticks, which is the true content of
"no middle").

**Why this matters and is not pedantry.** §8.29 routes "the telegraph's graded penalty texture" to a
sequel run as *not yet empirically demonstrated*. Part of it already is. And a tuning lap reading
§8.29 as written would reach for Mechanism C's dials (`ORBIT_SPEED_FRAC`, `WALL_*`) when
`NOVA_ESCAPE_FRAC` — §E-D's one dial — is doing most of the work. Recommendation: restate the ruling
as a joint mechanism with the single-mechanism rates beside it, and note that the graded middle is
reachable by flag combination without touching a constant.

### WARN-3 — F-WR2-4's substrate is prose only; a banked conductor finding has no banked evidence

§5.2's three-row resolution table is the whole ground for F-WR2-4, and it exists **nowhere but the
cell note**. `wr2_bat_statistics.json`'s clause-2 arm banks `crossing_r_star_m: []` for `after_m3`
and no distances at all; the in-process probe's scratch was not kept. So the numbers a future reader
must trust — 9.00 → 6.70, 12.22 → 12.78, 4.09 → 4.93, `r_star` 4.6867 — are unreproducible from the
committed tree. I reproduced the *geometry* independently and it holds; my digits differ slightly
(12.1944 vs 12.22 first sample; 4.4306 vs 4.6867 on a tick grid vs the engine's sub-tick solve),
which is exactly the ambiguity a banked artifact removes.

**Rationale.** Discipline #12 (empirical inspection over assumption) and the precedent gamora already
accepted at Cell D INFO-2 — *bank the table, do not assert it in prose*. F-WR2-4 is now a **banked
conductor finding**, which raises the bar rather than lowers it. Fix: emit the per-ring
`(t_s, dist_to_origin, rho)` rows for both M-3 arms as a sibling artifact. Cheap — the arms re-run
in seconds.

### WARN-4 — the adopted driver still carries the false comment its own audit identified, and §8.29 says two such claims were "corrected"

`src/reincarnated/simulation/wr2_cell_bat_2026_07_29.py:82-84`, at HEAD:

```python
#: The three v2 flags, as CLI fragments and as the harness's label suffixes. ORDER IS THE HARNESS'S
#: and is derived, not transcribed (Cell C's convention: a second source of truth for a filename is
#: the drift the suffix convention exists to prevent).
AFTER_SUFFIX = "_dec_bsep_mv2_ntv2"
```

It is a **string literal**. It is transcribed. The comment is self-refuting: it names the exact
hazard ("a second source of truth for a filename") that the line below it instantiates.

The cell note §2.2 and the `f1ab3b09` commit message both **correctly report** the claim as wrong —
that part is good discipline. Neither claims to have fixed it. But **§8.29 states the cell
"corrected two wrong comment claims"**, and:

1. **Zero** were corrected — the one wrong claim is still in the shipped file, and I confirmed by
   grep that no correction exists anywhere in the driver.
2. There was only **one** wrong claim. The second audited item (crossing-ledger indices 3/4/6) was
   *confirmed correct*, never described as a wrong claim, by the cell or the commit.

**Rationale.** Principle #4 (the ruling ledger is the source of truth) and Discipline #9
(attribution clarity). This is the declaration-vs-transcription family I filed at Cell C WARN-1 and
Cell D WARN-1; here it is a two-line fix. Fix: restate the comment as *"TRANSCRIBED — verified
against `kitcal_g5_harness.py:2378-2394` at adoption; grep the builder if the suffix set changes"*,
and correct §8.29's clause to "identified one wrong comment claim, confirmed the other item".

### WARN-5 — "the known 0.98 mm spawn-adjacency residual" is FALSE on origin; four hands carried it and one of them is mine

The gate verdict is untouched (0 violations in 292,305 samples). The *explanation* is wrong, and I
falsified it at full battery grain:

```
negative-slack pair samples: 44,698   at tick 0: 0
min −0.0009889945962079372   median −1.33e-15
ticks where negatives occur: 28, 36, 37, 39, 47, 62, 65 … up to 262
spawn separation of the worst-slack pair (player ↔ zombie_a01_1): 17.8974 m
that pair's slack by tick: t26 +16.48 mm, t27 −0.83 mm, t43 −0.99 mm, t48 −0.69 mm
```

**Not one overlapping pair exists at tick 0 in any of the 450 fights.** The sub-zero population is
mid-engagement contact-solver residual: 34,429 of the 44,698 samples are float noise (≤ 1 nm),
~6,200 sit in the 0.5–0.99 mm band, and the worst-slack pair *spawns 17.90 m apart* and only touches
at tick 27 once melee closes. So the quantity is governed by `BODY_SEP_EPS_TOUCH` / `BODY_SEP_ITER_MAX`
(both frozen, correctly), not by spawn placement.

**Lineage, stated because the pattern is the finding:** charter §8.19 (conductor) → **my own Cell C
finding §4.5** ("exactly the spawn-adjacency signature charter §8.19 named") → charter §8.23
("independently confirmed as spawn-adjacency") → this cell note §1. Four hands, one unchecked
premise — the *same shape* as WARN-2 at Cell D, and again with my fingerprints on it. Note the cell
note is internally inconsistent on this: §6 correctly calls the 0.98 mm "post-solver overlap in
emitted frames" while §1 calls it spawn adjacency.

**Why it matters:** a reader who believes this is a spawn artifact will look for a spawn-placement
fix and will not find one, and will not think to watch the counter when the solver's tolerances are
next discussed. Fix: strike "spawn-adjacency" at all four sites; call it what it is — a
contact-solver ε residual during engagement, worst 0.99 mm, 10× inside the S-1 margin.

### WARN-6 — third occurrence of the BQ-3 class, and a 9-second check was available every time

All three occurrences were caught by a ~20-minute full regression, two of them after the offending
module had already produced evidence. `pytest tests/test_bq3_calibration_override_door.py` is
**39 tests in 9.21 s**, and its T-8 is a static AST sweep that fails the instant an undeclared module
exists under `src/` — it does not need the battery, the traces, or a single fight. §8.29 has just
amended the interruption drill for the mtime hole; the same drill should gain one line: **run the
containment suites against any newly added `src/` module before it produces evidence.** In this cell
that would have moved the catch from "three commits and one 20-minute regression later" to
"9 seconds into STEP 0", at which point the declaration is a routine part of the adoption commit
rather than an item needing a conductor ruling and a Gate-2 second-guess.

---

## 12. INFO items

- **INFO-1 — what S-7 clause 1 actually certifies, stated so the grading lap cannot over-read it.**
  Under the shipped law `ratio_to_bound ≡ 1 − d/R`, so with `law_residual_s = 0` the predicate holds
  for **every** player position inside the ring by algebra. The gate's real content is therefore
  (a) `T ≡ R/(0.90·v)` against the trace's **independent** `movement_speed_ms` — which is genuinely
  falsifiable and is why `law_residual_s` is the sharp form — plus (b) the drawn radius equalling the
  damage radius. **The cell already says this** in the driver's §2 preamble and math note §4.1, and
  volunteers the degeneracy; I am recording it only so "132/132 escapability" is not read as an
  empirical escapability result. Note (b) is inherited, not measured here: my grader reads `radius_m`
  from the telegraph for both numerator and law check, so the drawn≡damage guarantee comes from Cell
  D's source pin (`radius_m=float(p.projectile_distance_m)` asserted via `inspect.getsource`), not
  from this battery.
- **INFO-2 — the BQ-3 discharge cites the wrong falsifier.** The cell writes *"Verified with
  `T8b_the_sweep_is_not_vacuous` green, so the entry cannot have blinded the detector."* T8b never
  reads `_DOOR_ALLOW_LIST` — it re-implements the AST predicate over a synthetic source string, so it
  speaks to the *detector*, not to *blinding*. What proves non-blinding is the set-difference
  structure plus the enumeration (4 door sites in the whole tree; remove the entry → exactly 1
  offender at `:462`). I ran that and it holds, so the conclusion is right and only the citation is
  wrong. Worth one line because this run's whole discipline is naming the falsifier that actually
  falsifies.
- **INFO-3 — the death-2 band is still unmeasured anywhere in WR2.** S3a is operationalized as
  "`pre` arm-A win rate == 0.0", a win-rate proxy. That substitution is chartered (§8.21: re-verified
  from leg reports, not re-gated blind) and honestly declared in the artifact's own
  `death2_band_note`. But the band `r ∈ [0.96, 1.61] m` about the nova origin has not been measured
  in this run, and F-WR2-1/F-WR2-2 discussion should not lean on "killable at the death-2 band" as
  though it had.
- **INFO-4 — the BEFORE arm's 450 traces are on disk but UNTRACKED.** Only the six leg reports are
  committed. §7's evidence-class spot-check and every BEFORE figure in §9 above came from untracked
  files. The arm regenerates deterministically, so nothing is lost — but the S-6 baseline is not
  banked evidence in the sense SS-1 uses, and a `git clean` would take it.
- **INFO-5 — §4.2's "trash / champion / mixed_pack ±1%" understates trash.** Measured: trash −2.5%
  (pre) and −3.0% (post). The quoted magnitudes (6.05→5.90, 6.89→6.95, 25.43→25.88) are exact; only
  the summary band is loose.
- **INFO-6 — S-4 of record can be widened at no cost, and I have.** The cell's S-4 covered one leg
  (150 traces). I ran all three legs twice: **450/450 byte-identical**, and **450/450 of the banked
  traces regenerate from the current tree with `engine_git_hash` as the sole differing field**. That
  second number is worth carrying into the grading record — it is provenance proof for the battery of
  record and an empirical zero-behaviour-change proof for `82f01917` + `d05535f9`.

---

## 13. What this cell did unusually well (recorded because the run's laws are being earned, not obeyed)

- **The cell asked for its own riskiest call to be second-guessed, and supplied the falsification
  both ways rather than an argument.** Both limbs held under my independent test. That is the
  behaviour the standing-safety structure exists to produce.
- **Volunteering the clause-1 degeneracy before Gate-2 could find it** (§1.1), and stating the
  instrument's blind spot (`firings − crossings` conflation) *and then closing it by measurement*
  rather than reasoning past it (§5.2(a)).
- **P-2 predicted a priori to 15 significant figures** — 0.1492841230108518 written down before the
  battery existed, measured 0.14928412301085175. Discipline #11 at its strongest.
- **The WARN-2 discharge found a fact the erratum did not contain** (the cone/line names belong to
  the *player*), i.e. the correction was re-verified from source rather than transcribed — which is
  the exact defect being corrected.
- **The name-diff was re-run on the final tree unprompted** after the tree moved.

---

## 14. Action

- [x] **jack-ryan:** Gate-2 fired. **CLEAR-with-notes, no BLOCK, no Matt escalation.** Grading +
      AFTER-baton **RELEASE**, subject to WARN-1's pre-baton gate.
- [x] **jack-ryan (ADR-002 direct approvals):** `82f01917` (documentation-only, three `.md` files) and
      `d05535f9` (test-file allow-list declaration, zero production behaviour change proven
      empirically) **APPROVED**. WARN-1's MIGRATION content **pre-approved** as documentation-only so
      it need not wait on a further gate.
- [x] **jack-ryan (self-correction):** **WARN-5** is filed against **my own Cell C finding §4.5**,
      which originated the propagation the conductor then ratified at §8.23. Second consecutive gate
      at which a ratified *ground* claim of mine has turned out false while the *disposition* stood.
      I am adding a standing habit to my own checklist: when a prior finding supplies a causal
      *label* rather than a measurement, re-measure the label at the next gate that touches it.
- [ ] **gamora — WARN-1 (before the AFTER-baton):** add the `MIGRATION.md` entry for
      `presentation_units`, `movement_speed_ms` / `movement_speed_provenance` and
      `nova_per_projectile_hp` — additive, report-only, trace content untouched, `run_spatial_fight`
      result dict untouched — and name drax's decomposer as the consumer that stops hard-coding
      207.40 / 235.40. Content pre-approved.
- [ ] **gamora — WARN-3:** bank the F-WR2-4 substrate as a sibling artifact (per-ring
      `(t_s, dist_to_origin, rho)` for both M-3 arms), same discipline as INFO-2's residual table.
- [ ] **gamora — WARN-4:** fix `wr2_cell_bat_2026_07_29.py:82-84` — the suffix order is TRANSCRIBED;
      say so and name the verification site.
- [ ] **gamora — WARN-5:** strike "spawn-adjacency" from the cell note §1 gate table; §6's
      "post-solver overlap in emitted frames" is the correct form and is already there.
- [ ] **gamora — INFO-2:** restate the non-blinding proof as the set-difference/enumeration argument,
      not T8b. **INFO-5:** loosen the "±1%" band to the measured −3.0%.
- [ ] **gandalf (RUN-CONDUCTOR) — WARN-2:** restate §8.29's F-WR2-4 as a **joint** D+C mechanism with
      the single-mechanism rates beside it (B+C-only 0.955, D-only 0.516, both 0.000), and scope
      "no middle" to the reaction-timing axis. Consequence for the sequel/tuning lap: the graded
      middle is already reachable by flag combination, and `NOVA_ESCAPE_FRAC` — not C's dials — is
      the mechanism carrying most of the effect.
- [ ] **gandalf (RUN-CONDUCTOR) — WARN-4:** correct §8.29's *"corrected two wrong comment claims"* to
      "identified one wrong comment claim (uncorrected at landing) and confirmed the other item".
- [ ] **gandalf (RUN-CONDUCTOR) — WARN-5:** append an erratum against §8.19's and §8.23's
      "spawn-adjacency" ground. Disposition unaffected; the ground moves. Third instance of this
      failure shape in three gates — worth a line in the run's own lessons about *labels* vs
      *measurements*.
- [ ] **gandalf (RUN-CONDUCTOR) — WARN-6:** extend the §8.29 interruption/adoption drill amendment
      with "run the containment suites against any newly added `src/` module before it produces
      evidence" (9.21 s).
- [ ] **gandalf — INFO-3:** decide whether the death-2 band gets measured before the run closes or is
      ledgered as unmeasured. **INFO-4:** decide whether the BEFORE arm's 450 traces get banked as
      S-6 baseline evidence. **INFO-6:** carry the widened S-4 (450/450, plus the hash-only banked
      regeneration) into the grading record.

---

## 15. References

**Reviewed (engine, `~/Games/reincarnated-engine`):**
- `src/reincarnated/simulation/wr2_cell_bat_2026_07_29.py` (the adopted driver, 1,258 lines)
- `src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py` (emissions, +189)
- `src/reincarnated/simulation/math/wr2-bat-battery-of-record-2026-07-29.md`
- `src/reincarnated/simulation/math/wr2-c-movement-policy-2026-07-29.md`
- `src/reincarnated/simulation/math/wr2-d-nova-telegraph-2026-07-29.md`
- `src/reincarnated/simulation/MIGRATION.md`
- `tests/test_bq3_calibration_override_door.py`
- `tests/test_wr2_d_nova_telegraph.py` (the drawn≡damage radius pin, INFO-1)
- `src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` (`:4846`, `:4902`, `:6003`, `:4735`, `:5579`)
- `src/reincarnated/simulation/gd_nova.py` (`:917` ring expiry)
- `src/reincarnated/simulation/spatial_gauntlet/policy/telegraph_response.py` (`:203`, `:286-288`)
- `src/reincarnated/simulation/wr2_cell_c_move_2026_07_29.py` (S-2 predicate + thresholds)
- `src/reincarnated/simulation/output/kitcal_g5/wr2_battery_after/` — `wr2_bat_statistics.json`,
  `wr2_bat_s7_firings.json`, `wr2_bat_residual_counters_four_tier.json`, 3 leg reports, 450 traces
- `src/reincarnated/simulation/output/kitcal_g5/wr2_battery_before/` — 3 leg reports (450 traces untracked)

**Reviewed (meta, `~/Games/reincarnated-collaboration`):**
- `agentic_orchestration/gandalf/notes/2026-07-29-wr2-encgeo-run-charter.md` (§3, §8.19, §8.21, §8.22, §8.23, §8.26–§8.30)
- `agentic_orchestration/gandalf/notes/2026-07-29-wr2-mechanism-spec.md` (§E, §E-D, §G-D)
- `agentic_orchestration/gamora/notes/2026-07-29-wr2-cell-bat-battery-of-record.md`
- `agentic_orchestration/gamora/notes/2026-07-29-wr2-cell-c-movement.md` / `…-cell-d-nova-telegraph.md` (WARN-2 errata)
- `agentic_orchestration/gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt` (81-name baseline)
- `agentic_orchestration/qa/findings/2026-07-29-gate2-gamora-wr2-cell-c.md` (corrected by WARN-5)
- `agentic_orchestration/qa/findings/2026-07-29-gate2-gamora-wr2-cell-d.md` (prior gate; its WARN-2/-3/-4 + INFO-3/-4 discharged here)

**My instruments (independent; scratch, regenerable):** S-1 pairwise scanner · S-2 clamp-predicate
scanner · S-7 clause-1 grader · four-arm M-3 reproduction with live-ring distance sampling ·
S-4 three-leg double run with SHA-256 + field-level banked diff · door-site enumerator ·
acting-tick re-derivation. Full regression log at `/tmp/jr_bat_regression.txt` (60/6197/21,
1202.96 s), name list at `/tmp/jr_bat_names.txt` (81, diff empty).

---

*Gate-2 closes. — jack-ryan*
