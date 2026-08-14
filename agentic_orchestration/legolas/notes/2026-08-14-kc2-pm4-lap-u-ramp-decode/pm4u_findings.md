# KC2-PM4 · LAP U — THE RAMP DECODE · FINDINGS

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR) · **2026-08-14**
**Commission:** `R-PM4-52 part 5`, ledger `L-43`. **The run's last named residual.**
**PREREGISTRATION** `7a250772bad3bf8cbce2e43455bc3e4dae2fee677aeedc1ffad978f3dda6b144`,
hashed **2026-08-14T18:03:05Z**, before any instrument of this lap executed. Reconnaissance
preceding the hash is declared in its § 0.
**Discipline:** GL-6 (full 64-hex, `pm4u_digests.json`) · GL-12 (DECODE-NEVER-ESTIMATE) ·
NOTE-9 (no repair outside my own seam) · FIT law (self-caught, repaired in-lap, declared scope).

---

## § 0 — THE HEADLINE TABLE

| # | finding | value | grade |
|---|---|---|---|
| **1** | **⚑ `U-T-1` IS DECIDED BY THE BINARY, AND AGAINST THE COMPARATOR THE RUN FOLDED. The Crucible march is spawn → PLAYER, not spawn → patrol ring.** `ControllerAIState::ShouldFindEnemy` is `xor al,al; ret` — **FALSE by default** — and `ControllerMonsterStatePatrol` **explicitly overrides it to `mov al,1; ret`, TRUE.** A patrolling monster is *designed* to break off. `FindEnemiesInSight` queries with `controller+0x21c` = the record field **`ViewDistance`**, and every rolled tier-16 monster carries **80.0 m** — larger than the whole arena. `EnemyFound` → `DefaultEnemyFoundResponse` → `SetState("Pursue")`. | **`ViewDistance` = 80.0 on 169 / 169** rolled monsters; arena's worst spawn→player ≲ 76 m, typical ~21–22 m | **MEASURED / DECODED** |
| **2** | **⚑ THE TARGETING DISCRIMINATOR'S ANSWER FROM THE VIDEO SIDE: MOOT — AND MEASURED TO BE SO.** The player does **not** close distance toward packs. He nets **1.99–11.27 m per wave** (median 3.61) over a path of **40.2–83.0 m** (straightness median **0.060**). He **mills; he does not traverse.** Player motion can therefore move the march clock by **≤ 3.69 s worst wave, ~1.18 s typical** — so spawn→player and spawn→(a fixed point near him) are the same march to within a few metres. | net 3.61 m median; bound ≤ 3.69 s | **MEASURED** |
| **3** | **`V-a1` (the FOLLOW test) — NOT SUPPORTED, n = 0 at every cell, and my pre-registered falsifier § 8.1 fires.** In its own words: **the referent's arrivals do not demonstrably follow the player.** The cause is **starvation, not refutation**: the largest player NET displacement inside *any* surviving hold-window is **4.16 m**; the loosest pre-registered cell needed 5.0 m and the primary cell 9.0 m. | 0 of 55 / 62 windows | **NEGATIVE, honest** |
| **4** | `V-a3` arrival directions — **WEAKLY DIRECTIONAL.** Neither one door nor uniform. | pooled **R = 0.2485**; per-wave 0.087–0.490 | **MEASURED** |
| **5** | **`UNREACHED-T5` CLOSED.** `PatrolPoint::Load` (0x315a70) reads two **named record fields** and stores them to the accessors Lap T decoded. | **`radius` = 2.0 m**, **`shouldRun` = True** | **DECODED** |
| **6** | **`UNREACHED-T3` CLOSED BY EXPLANATION.** There is no state-transition table to find: transitions dispatch by **string name** through `ControllerAI::SetState`. Lap T was looking for a structure that does not exist. | literal `'Pursue'` at `.rdata` 0x52d5d4 | **DECODED** |
| **7** | **`UNREACHED-S8` PARTIALLY CLOSED.** The `.lvl` regions are **embedded** in the `.map`; their (offset, size) pairs **tile every file exactly to EOF, 20 of 20**, magic **`LVL\x0f`**. All gameplay entities live in region **A001**. **Walls are NOT decoded → `D-PDEF-2` STAYS OPEN.** | 7 regions (9 on `_f`), tiling exact 20/20 | **DECODED (container) / PARTIAL (contents)** |
| **8** | **`D-I20-1` REPAIRED AND VERIFIED — `pm4u_map_placements_v3.csv` emitted.** `H-d-A` (index-first layout) confirmed; the v2 reader started **four bytes late**. | see § 5 | **DECODED** |
| **9** | **⚑ `D-U-1` self-caught: `UNREACHED-T2` WAS MY OWN GATE.** The inherited rotation band `[0.98, 1.02]` rejected a legitimately *scaled* placement. Widened to `[0.25, 4.0]`. | complete parses **18 → 20 of 20** | **self-caught, repaired** |
| **10** | **⚑ `D-U-2` self-caught: Lap T's own `D-T-2` is a casualty of `D-I20-1`.** Spawn → nearest beacon median **10.4726 m (v2 labels) → 0.6089 m (v3 labels)**; spawn points inside the 8.0 m aura **32.7 % → 83.3 %**. **Lap S's original F-12 was substantially RIGHT and Lap T "corrected" it on displaced labels.** | 0.6089 m; 83.3 % | **self-caught, corrected** |
| **11** | **⚑ `D-U-3` self-caught: my own arrival-interval deliverable is DISQUALIFIED.** 3,324 tracked entries against a peak living count of 19–36 = **11.05× ratio**. The raw inter-entry distribution is an **UPPER BOUND only**. The living-count ramp (F-10) is unaffected and remains the like-for-like functional. | 11.05× | **self-caught, demoted** |
| **12** | Corrected geometry on the repaired labels, complete 20 arenas. | **F-3 35.5948 · F-4 16.4307 (span 0.3253–26.0779) · F-5 72.7985 · ring extent 45.7066** | **MEASURED** |
| **13** | The march arithmetic on the referent's own ramp: t→50 % = **9.98–10.49 m** of march; t→90 % = **15.18–15.94 m** ≈ the 16.43 m first march (Lap T's 1.05–1.11× reproduced from v3). Implied **spawn → player ≈ 21.0–22.1 m** median. | — | **INFERRED-WITH-EVIDENCE** |

> **⚑ THE ONE-PARAGRAPH ANSWER TO THE COMMISSION.** *Where does the gap live?* **Not in march
> speed, not in single-leg distance, and not in the player's motion — and, decisively, not in the
> comparator the run has been arguing about.** The binary says the Crucible pack sees the player
> from its spawn point (`ViewDistance` 80 m over a ≲ 76 m arena), opts into the scan by explicit
> override, and switches to `Pursue` immediately; `ControllerMonsterStatePatrol` is a state a
> Crucible attack pack **essentially never occupies for its march**. So I-20 folded a **16.80 m
> march to a ring node** when the decode-true march is **spawn → player at ~21–22 m** — i.e. the
> sim's march is if anything **too SHORT**, which makes its 2.98× **slower** ramp *more* anomalous,
> not less. **The residual is therefore CONCURRENCY, and the referent's number for it is on the
> table: 19–36 living bodies (median 25) inside the 11.6 m window, reached to 50 % in 3.267 s.**

---

## § 1 — LIMB (a): VIDEO ARRIVAL DECOMPOSITION

**Instrument** `pm4u_video_2026_08_14.py` (I-U1) + `pm4u_ramp_2026_08_14.py` (I-U2, **declared
post-hoc**). Inputs: the banked 60 fps nameplate census and camera-translation arrays. **No sim
number is consulted anywhere in this limb.**

### 1.1 `P-U-0` — the continuity pin, against the ARTIFACT (D-I20-5's lesson, adopted)

**30 fields over 10 waves reproduced EXACT** against `pm4s_video.json → arrival` — `peak_plates`,
`t_to_50pct_peak_s`, `t_to_90pct_peak_s` for waves 151–160. Zero differences; the limb would have
HALTED on one. F-10 **recomputed, not quoted**: median t→50 % **3.2670 s**, t→90 % **4.9670 s**.
The tracker also reproduces Lap S's PRIMARY cell exactly: **3,324 tracks**, birth-radius median
**306.1 gpx**, p95 **1058.0 gpx**.

### 1.2 ⚑ The player's own motion — the commission's second question, answered NO

*"Does Matt close distance toward spawn doors/packs, and how far does he displace per wave?"*

| wave | path (m) | **net (m)** | straightness | v̄ (m/s) | frames moving |
|---|---:|---:|---:|---:|---:|
| 151 | 48.66 | **11.27** | 0.232 | 3.119 | 82.5 % |
| 152 | 58.56 | **2.93** | 0.050 | 3.593 | 82.2 % |
| 153 | 54.96 | 3.84 | 0.070 | 3.688 | 64.1 % |
| 154 | 40.23 | 3.46 | 0.086 | 2.833 | 65.7 % |
| 155 | 61.05 | **1.99** | 0.033 | 3.769 | 68.4 % |
| 156 | 64.10 | 2.62 | 0.041 | 3.173 | 67.7 % |
| 157 | 70.04 | 9.73 | 0.139 | 3.629 | 66.1 % |
| 158 | 45.77 | 11.13 | 0.243 | 3.521 | 67.8 % |
| 159 | 83.02 | 2.82 | 0.034 | 3.157 | 68.1 % |
| 160 | 78.32 | 3.76 | 0.048 | 3.133 | 72.4 % |

*(metres at the 119 gpx/m edge; path length and net displacement are **magnitudes**, hence
invariant to the unresolved camera sign convention of B-5. The integrated trajectory is **not
used** — B-4.)*

**⚑ THE PLAYER MILLS.** He is moving 64–83 % of frames at ~3.1–3.8 m/s and going **nowhere**:
median straightness **0.060**. Over an entire wave his net displacement is **3.61 m median**.

**The bound this supports** (the only quantitative thing `V-a1` yields, and it is worth having): at
the decoded march bracket, the player's own motion can add or remove **1.124–1.181 s of march time
at the median and 3.511–3.688 s in the worst wave.** Against a t→50 % residual of
9.7551 − 3.267 = **6.49 s**, player motion is bounded at ~18 % typical and ~57 % worst-case, and it
is the *upper* bound on the whole "does the target move with him" question. **Targeting-as-motion
cannot carry this residual.**

### 1.3 `V-a1` — the FOLLOW test: NOT SUPPORTED, and the falsifier fires

The test: a body held within `R_hold` of the player across a window in which the player's NET
displacement was |Δp| **must itself have moved ≥ |Δp| − 2·R_hold**. Triangle inequality, not a
model; sign-free and drift-free by construction.

| `R_hold` | windows surviving guards | **passes at any `D_min`** | rejections (G-1 dash / G-2 swap / G-3 short) |
|---:|---:|---:|---|
| 2.0 m | 29 | **0** | 24 / 0 / 1539 |
| 3.0 m | 55 | **0** | 64 / 0 / 2038 |
| 4.0 m | 72 | **0** | 95 / 0 / 2327 |

**Verdict `V-a1` = NOT SUPPORTED (n = 0 at both bracket edges).** Pre-registered falsifier § 8.1
fires and I report it in the words I committed to: **the referent's arrivals do not demonstrably
follow the player.**

**And I name the reason rather than leave the negative bare.** The largest player net displacement
inside *any* surviving window is **4.16 m**. The loosest cell needed 5.0 m. **The discriminator was
never reachable on this referent** — § 1.2 explains why. `V-a1` returns **no information about
targeting**; it is a negative about the instrument's reach. It does not refute player-targeting,
and limb (b) establishes player-targeting by a different route entirely.

### 1.4 `V-a2` — the pursuit cosine (corroborating only, demoted by construction)

| convention | median cos(v_monster, bearing→player NOW) | vs frozen birth target | frac > 0 |
|---|---:|---:|---:|
| `plus` | **+0.2058** | +0.3245 | 0.5609 |
| `minus` | **+0.1883** | +0.2172 | 0.5506 |

Verdict **PURSUIT-CONSISTENT** (positive under both conventions, as required). **But note the
honest wrinkle: the cosine against the *frozen* birth-time target is HIGHER than against the
player's current position under both conventions** — so this statistic does **not** demonstrate
re-aiming, only net approach. It corroborates; per the pre-registration it may never establish.
Sign-free player-relative closure median cos = **+0.2820**.

### 1.5 `V-a3` — arrival directions

Pooled resultant **R = 0.2485 → WEAKLY DIRECTIONAL** (thresholds pre-registered at <0.20 omni,
≥0.40 directional). Per wave: 0.368, 0.254, 0.345, **0.087** (w154), 0.345, 0.237, 0.348,
**0.490** (w158), 0.214, 0.175. Twelve-sector pooled histogram
`[160, 320, 640, 618, 247, 139, 160, 162, 314, 317, 111, 136]` — a broad two-lobe preference, not a
door and not a ring. Note w154 (the only 4-spawn-point wave, Lap S F-1) is the **most
omnidirectional** and w158 the most directional; both are published, neither is ruled.

### 1.6 `V-a5` — the deliverable, and why it is DEMOTED (`D-U-3`)

| wave | entries | entries/s | burst 1 s | peak living | **entries ÷ peak living** |
|---|---:|---:|---:|---:|---:|
| 151 | 216 | 13.85 | 33 | 24 | 9.0 |
| 154 | 311 | 21.90 | 58 | 28 | 11.1 |
| 157 | 480 | 24.87 | 63 | 36 | 13.3 |
| 159 | 667 | 25.36 | 61 | 29 | 23.0 |
| **pooled** | **3,324** | 15.74 med | 46 med | 19–36 | **11.05 median** |

**⚑ `D-U-3`, self-caught.** A fight whose peak concurrent living plate count is **19–36** cannot
have **3,324** genuine arrivals in 181 s. The excess is **nameplate RE-APPEARANCE**
(`UNREACHED-S4`) — which the pre-registration named as a contamination but did **not price**, and
which I then published as an arrival rate. Priced now by an `H_GAP` sweep:

| `H_GAP` | 6 (0.10 s) | 30 (0.50 s) | 60 (1.00 s) | 120 (2.00 s) | 240 (4.00 s) |
|---|---:|---:|---:|---:|---:|
| tracks | 3,324 | 3,173 | 2,879 | 2,525 | 2,093 |
| entries ÷ peak living | 11.05 | 10.17 | 9.46 | 8.15 | 7.33 |

It does not converge to a plausible body count even at a 4-second bridging gap. **Lap S's birth
RADIUS was stable across its own H_GAP sweep and remains so — the birth COUNT is not, and I did not
distinguish them.** My own drafting error, in my own limb.

**Disposition: `pm4u_arrivals.csv` and the interval distributions in `pm4u_arrival_stats.json` are
published as a STRICT UPPER BOUND on arrival rate and MUST NOT be graded against a sim as-is.**
Every row carries the caveat in its `basis` column. **The living-count ramp (F-10) is untouched by
this defect and remains the like-for-like functional** — it counts bodies present, not births.

### 1.7 ⚑ The march arithmetic, reconciled on the referent's own ramp

| quantity | value |
|---|---|
| referent t→50 % of peak living count | **3.2670 s** → march **9.982 – 10.485 m** |
| referent t→90 % | **4.9670 s** → march **15.176 – 15.941 m** |
| decoded first march, F-4 median (v3) | **16.4307 m** (span 0.3253 – 26.0779) |
| implied spawn → PLAYER at the median | **21.04 – 22.10 m** |

**t→90 %'s march straddles the decoded first march** — Lap T's 1.05–1.11× agreement, reproduced
independently from the repaired v3 geometry. **t→50 %'s march is only ~10 m**, i.e. the ramp is
**FRONT-LOADED** relative to a *uniform* first march — which is exactly what a first-march
**distribution spanning 0.33–26.08 m** predicts and what a scalar cannot. Graded
**INFERRED-WITH-EVIDENCE**: it chains the decoded march bracket (`UNREACHED-T1` carried), the
MEASURED frustum radius, and the assumption that a body entering the window is moving at the pooled
speed. **It is not a decode and no fold should treat it as one.**

---

## § 2 — LIMB (b): THE PURSUE-TRIGGER DECODE — **the lap's headline**

**Instrument** `pm4u_pursue_2026_08_14.py` (I-U3), capstone/objdump over the shipped PE32 modules
plus the `.arz` corpus. **`V-b1` = DECODED. `V-b2` = DECODED.**

### 2.1 The transition, read verbatim

```
?EnemyFound@ControllerMonsterStatePatrol@GAME@@MAEXI@Z          0x000fecd0
  push ebp ; mov ebp,esp ; pop ebp
  jmp  0x1010a360   <?DefaultEnemyFoundResponse@?$ControllerMonsterState@
                       VControllerMonster@GAME@@VMonster@2@@GAME@@IAEXI@Z>

?DefaultEnemyFoundResponse@...                                   0x0010a360
  push 0x1052d5d4                 ; .rdata literal, length 6   ->  "Pursue"
  ...
  call 0x100e6780  <?SetState@ControllerAI@GAME@@IAEXABV?$basic_string@...@ABVControllerAIStateData@2@@Z>
```

**Patrol carries NO override of its own** — it tail-jumps straight into the base response, which
calls `SetState` with the string literal **`"Pursue"`**, read out of `.rdata` at `0x52d5d4`.

**⚑ `UNREACHED-T3` is closed by explanation, not by finding the thing Lap T looked for.** The
state machine dispatches **by string name**. There is no transition table, so none is exported, so
none could ever have been found. Lap T's UNREACHED was chasing a structure that does not exist.

### 2.2 ⚑ Patrol *opts in* to scanning — the base class does not

| symbol | RVA | body | value |
|---|---|---|---|
| `ControllerAIStateT<…>::ShouldFindEnemy` (base) | `0x00c3e0` | `xor al, al ; ret` | **FALSE** |
| `ControllerMonsterStatePatrol::ShouldFindEnemy` | `0x009350` | `mov al, 1 ; ret` | **TRUE** |

**The engine's default for an AI state is DO-NOT-SCAN. `ControllerMonsterStatePatrol` deliberately
overrides it to TRUE.** A patrolling monster is authored to break off and pursue. This is the
single cleanest piece of evidence in the lap and it is two instructions long.

### 2.3 The radius, and the number that decides the run's comparator

```
?FindEnemiesInSight@?$ControllerAIStateT@VControllerMonster@GAME@@VMonster@2@@…   0x000d2540
  mov   ecx, dword ptr [edi + 0x4]          ; the controller
  movss xmm0, dword ptr [ecx + 0x21c]       ; <-- THE QUERY RADIUS
  ...                                        ; into the query struct, then the spatial query

?Load@ControllerAI@GAME@@UAEXABVLoadTable@2@@Z                                    0x000e6710
  mov   dword ptr [esp], 0x41700000         ; default = 15.0f
  push  0x10528e08                          ; -> "ViewDistance"
  call  LoadTable::GetFloat
  fstp  dword ptr [edi + 0x21c]

?SetViewDistance@ControllerAI@GAME@@QAEXM@Z                                       0x000e6765
  ; stores to the same +0x21c — the field IS the view distance
```

**The record census, over the corpus and over this run's own roster:**

| population | n | `ViewDistance` |
|---|---:|---|
| corpus-wide, records carrying the field | 451 | **80.0 on 341**; then 24.0 (15), 18.0 (15), 15.0 (11), … |
| **`in_rolled_20w` — the tier-16 rolled roster (Lap D)** | **169** | **80.0 on 169 — 100 %** |
| `in_pool` — the full tier-16 pool | 663 | **80.0 on 661**, 15.0 on 2 |

**⚑ Against the arena's own geometry** (v3, § 5): spawn → ring centroid **max 48.07 m**, ring max
extent **max 56.81 m**. A worst-case spawn → player is bounded at roughly **48 + 28 ≈ 76 m**, and
the typical value is **~21–22 m** (§ 1.7). **80.0 m covers the arena.** Every Crucible monster can
see the player from the moment it is placed.

> **⚑ `U-T-1` IS DECIDED. THE MARCH IS SPAWN → PLAYER.** The nearest-entry + cyclic patrol
> semantics Lap T decoded are real, correct, and describe a state that a Crucible attack pack
> **essentially never occupies for its march**. `R-PM4-27 part 3` is honored: this is decided by a
> decoded relation and a record census, **not** by which comparator grades better — I have not
> looked at a scorecard, and the direction of the correction is *unfavourable* to the fold that
> already landed.

### 2.4 `UNREACHED-T5` CLOSED — the writers, and the values

```
??0PatrolPoint@GAME@@QAE@XZ                          0x315940   (the DEFAULTS)
  mov dword ptr [esi + 0x3dc], 0x0        ; radius      = 0.0f
  mov byte  ptr [esi + 0x3e0], 0x0        ; shouldRunTo = false

?Load@PatrolPoint@GAME@@UAEXABVLoadTable@2@@Z        0x315a70   (the RECORD FIELDS)
  push 0x0 ; push 0x10565f40 -> "radius"     ; LoadTable::GetFloat -> fstp [edi + 0x3dc]
  push 0x0 ; push 0x10565e84 -> "shouldRun"  ; LoadTable::GetBool  -> mov  [edi + 0x3e0]
```

| record | `radius` | `shouldRun` |
|---|---:|:-:|
| **`records/controllers/controlobjects/patrolpoint_01.dbr`** — the record every arena's patrol points instantiate | **2.0** | **True** |
| `patrolpoint_02.dbr` / `_03.dbr` | 2.0 | True |

**Two consequences.** `shouldRun = True` **decodes** what Lap T inferred from `chanceToRun = 100`:
the traversal is at **run** speed. And `radius = 2.0 m` is an **arrival tolerance** — a body reaches
a patrol point at 2.0 m, so any patrol-based march distance is effectively **F-4 − 2.0 m**. Both are
now decode-true and free of estimate.

### 2.5 What limb (b) did NOT reach — named, not estimated

* **`UNREACHED-U1`** — the update loop that drives `ShouldFindEnemy → FindEnemiesInSight →
  EnemyFound`. Both are **virtual-dispatched** (zero direct `call rel32` sites in `.text`), so the
  driver is behind vtables I did not reconstruct. `ControllerMonster::AngerUpdate` (0x0fba90) and
  `PickRandomEnemyInView` (0x0fc550) both read `+0x21c` and are the likely consumers. **Named, not
  claimed.**
* **`UNREACHED-U2`** — whether `FindEnemiesInSight` applies a **line-of-sight** test. The name
  suggests one; the spatial query is an indirect call through `[0x104e5294]` that I did not follow.
  If LOS is enforced, arena walls could suppress the 80 m acquisition — **and walls are exactly what
  limb (c) failed to decode.** This is the honest soft spot in finding 1 and I flag it as such.
* **`UNREACHED-U3`** — **`ControllerMonsterStateAlertBeforePursue` exists** (`OnBegin` 0x109410
  plays an animation, `AnimationSet_Type 0x21`, speed 1.0f) and would insert an **animation-length
  delay before the pursue march**. `DefaultEnemyFoundResponse` goes to `"Pursue"` *directly*, so
  this state is entered by some **other** path (`ShouldPlayRallyOrAlert`, 0x0f9ce0) whose condition
  I did **not** decode. **If some fraction of packs alert first, arrivals are delayed by that
  animation — a real ramp term, unmeasured.**

---

## § 3 — LIMB (c): THE `.lvl` ATTEMPT (`UNREACHED-S8`)

**Instrument** `pm4u_lvl_2026_08_14.py` (I-U5). The pre-registration declared the reconnaissance
finding that **no standalone `.lvl` file exists anywhere in the vendor tree** — `Maps.arc` holds
only `.map` members. The regions are **embedded**, so this was a container problem, not a missing
file.

**The acceptance gate, enforced by the reader and not asserted after the fact:** if the u32 pair
after each region name is `(offset, size)`, the regions must **tile the file** — each region's end
exactly the next one's start, the last exactly the file size. A wrong interpretation cannot pass
that by accident.

> **⚑ TILING EXACT ON 20 OF 20 MAPS.** Zero gap, zero overlap, last end == file size, every time.
> The instrument HALTS if it does not hold.

`survivalworld_a.map` (4,836,448 B), seven regions, every blob opening with the magic **`LVL\x0f`**:

| region | offset | size | grid | origin | dbr strings | patrol pts | tier-16 spawns |
|---|---:|---:|---|---|---:|---:|---:|
| `Region_Survival_A001.lvl` | 0x1c136b | 1,076,532 | 64 × 19 × 64 | (−224, 0, 0) | 149 | ✔ | **6** |
| `A002` | 0x2c809f | 296,367 | 64 × 19 × 64 | (−160, 0, −128) | 12 | 0 | 0 |
| `A003` | 0x31064e | 302,292 | 64 × 19 × 64 | (−32, 0, −128) | 16 | 0 | 0 |
| `A004` | 0x35a322 | 298,142 | 64 × 19 × 64 | (32, 0, 0) | 10 | 0 | 0 |
| `A005` | 0x3a2fc0 | 433,600 | 64 × 19 × 64 | (−32, 0, 128) | 23 | 0 | 0 |
| `A006` | 0x40cd80 | 294,614 | 64 × 19 × 64 | (−160, 0, 128) | 3 | 0 | 0 |
| `A007` | 0x454c56 | 294,922 | **UNVALIDATED** | — | 7 | 0 | 0 |

*(the last entry's grid/origin are read at fixed offsets inside a 72-byte tail whose validation
predicate — "the next entry's length prefix follows" — cannot hold for the last entry. Rather than
publish an unvalidated number I flag it. `(offset, size)` is validated for all seven by the tiling
gate.)*

**⚑ A completeness result that matters to every prior lap:** **all gameplay entities are in region
A001.** Regions A002–A007 carry 3–23 record strings each and **zero** spawn points and **zero**
patrol points. Lap S/T/U have been reading region A001's placement array all along, and that is
where the fight is. `survivalworld_f` carries **nine** regions rather than seven; it tiles exactly
too.

**Header:** `[magic 'LVL\x0f'][6 × f32 AABB][u32][u32][u32 count][string table…]`. For A001 the
AABB reads `(63.90, 16.70, 69.16) – (70.20, 21.51, 76.58)`.

**The large float array** at region0 + 0x1c000: 82.9 % of words decode as floats in (−10³, 10³) and
89.6 % of those lie in [0, 40] m, against arena placement Y-coordinates of ~7.9–13.8 m.
**GRADED `INFERRED-WITH-EVIDENCE` — consistent with a terrain HEIGHT field. It is NOT called a
decode and no number is taken from it anywhere.**

> **⚑ ARENA WALLS AND PATHING BLOCKERS ARE NOT IDENTIFIED. `D-PDEF-2` STAYS OPEN.** My
> pre-registered standing refusal applies and I exercise it: **I will not offer an entity-extent
> bounding box as a substitute for a decoded boundary.** Lap S's `D-S-1` is the precedent — an
> inflated hull is not a boundary. `UNREACHED-S8` is **PARTIALLY CLOSED**: container decoded,
> contents partially, walls **UNREACHED** and carried as **`UNREACHED-U4`**.

`V-c2` (patrol-point field values from the `.lvl`) was **not needed** — limb (b) closed
`UNREACHED-T5` from the binary and the record corpus. No value in this lap is taken from a `.lvl`.

---

## § 4 — LIMB (d): THE `D-I20-1` REPAIR — MY OWN ARTIFACT, MY OWN SEAM

**Instrument** `pm4u_mapv3_2026_08_14.py` (I-U4). **`H-d-A` (index-first layout) CONFIRMED;
`H-d-B` (paired controller/anchor records) REFUTED.**

The true record is
`[u32 string_index][9 × f32 rotation][3 × f32 position][u32 has_guid][16 B GUID if has_guid]`
and the array begins at **`arr_off + 4`**, not `arr_off + 8`. **Lap T's v2 reader started four
bytes late**, so every rotation, position and GUID it read was correct, but the u32 it consumed as
*this* record's string index was in fact the **next** record's. The displacement is **uniform
across all records**; gamora observed it on the patrol set because that is where anyone looked.

### 4.1 The pre-registered verdicts, graded honestly

| rule | requirement | result | verdict |
|---|---|---|---|
| **`V-d1`** | v3 completeness ≥ v2's 18/20 | **20 / 20** vs 18 / 20 | **PASS** |
| **`V-d2`** | positions/GUIDs/sizes identical on every row | **20 / 20 / 20**; shift relation `v3[i].dbr == v2[i−1].dbr` holds **20 / 20** | **PASS** |
| **`d-A1`** | the u32 at `arr_off+4` is record 0's string index | valid **20 / 20**, and **== 0 on 20 / 20** | **PASS** |
| **`V-d3`** | every `patrolpoint_01` row GUID-bearing, in the head group, count matching — **20 / 20** | **18 / 20** | **⚑ FAILED AS WRITTEN** |
| **`V-d4`** | v3 patrol set ≡ head-group GUID set | **20 / 20**, max residual **0.009070396 m** | **PASS** |
| **`V-d5`** | F-4 three ways | see below | **PASS** |

### 4.2 ⚑ `V-d3` FAILED AS WRITTEN, AND THE DRAFTING ERROR IS MINE

I graded it against what the pre-registration **said**, not against what I meant — the discipline
gamora applied to her own `S-2` and `D-I20-3` in I-20. The clause asserts *"every row labelled
`patrolpoint_01.dbr` is GUID-bearing … and the count equals `head_count`"*. **That is a claim about
the GAME's data which I had not verified and which is FALSE.** Both failures are diagnosed and
neither is a label failure:

* **`survivalworld_b` (×2 archives)** — **12** rows labelled `patrolpoint_01.dbr`: eleven
  GUID-bearing and all eleven in the `PatrolPoint_Attack` head group, plus **one genuine
  56-byte, ungrouped patrol-point placement** at (72.22, 9.20, 66.15). Real level data. My clause
  forbade it.
* **`survivalworld_d` (×2)** — under the *inherited* gate the parse halted at record 139/276, so
  only 2 patrol rows existed to test. **Unevaluable, and known to be so before the hash**
  (`UNREACHED-T2`). I failed to exclude it in drafting. *(After `D-U-1` — § 4.4 — these arenas parse
  completely and pass; the 18/20 figure is post-repair, and it was 16/20 before.)*

**The substantive claims all hold, and they are the ones that decide `H-d-A`:**

| substantive check | result |
|---|---|
| grouped patrol rows **cover the head group** | **20 of 20** |
| **foreign** labels sitting on head-group patrol GUIDs | **162 under v2 → 0 under v3**, zero-foreign on **20 of 20** |
| maps carrying a genuinely ungrouped patrol placement | 2 |

Under v2, `survivalworld_a`'s eleven patrol GUIDs were labelled `fx_eldritchrift_medium01.dbr`,
`stalagmite_large03.dbr`, `sndgen_water_stream01.dbr`, `playerspawnpoint.dbr` … while the **head
section's own strings** — read from a completely different structure — call every one of them
`patrolpoint_01.dbr`. **`H-d-B` is dead; it is not arguable.**

**⚑ AND I DEPARTED FROM A PRE-REGISTERED CONSEQUENCE, WHICH I FLAG RATHER THAN BURY.** § 6.2 said
*"≤ 18 of 20 ⇒ `H-d-A` REJECTED, no v3 is emitted."* I **emitted v3 anyway**, because the clause
that failed is the one I mis-drafted and the hypothesis is established by `V-d1`/`V-d2`/`V-d4`/
`V-d5` plus the head-section semantics. **The prediction is graded FAILED; the departure is
declared here, at full size, in the section where it happened.**

### 4.3 `V-d5` — F-4 four ways, and a NEW correction to my own Lap T headline

| basis | n | median | min | max |
|---|---:|---:|---:|---:|
| **(i) v3 patrol × v2 spawn labels** — gamora's `geometry_agreement_v2` GUID set | 110 | **16.7992** | 0.0000 | 35.3538 |
| **(iii) v2 patrol × v2 spawn labels** — her labelled-set control | 110 | **16.7308** | 0.6452 | 37.5125 |
| (ii) v3 patrol × v3 spawn, Lap T's gate | 110 | 16.8077 | 0.3253 | 26.0779 |
| **(iv) v3 patrol × v3 spawn, COMPLETE 20 arenas** | **120** | **16.4307** | 0.3253 | 26.0779 |

**(i) and (iii) reproduce gamora's two published numbers to four decimals from my reader.** That is
the transitive verification the commission asked for: her `geometry_agreement_v2` measured the
sim's 11 nodes ≡ the GUID set at **5.4e-5 m**, and `V-d4` shows v3's patrol set is **set-identical**
to that same head-group GUID set at **0.009 m max residual** — so **v3 is verified against the sim's
own geometry without my consuming a sim artifact.**

**⚑ The honest post-repair figure is (iv) `F-4 = 16.4307 m`, and it moves for TWO reasons**: the
spawn-point label set was displaced too (a consequence `H-d-A` predicted and I pre-registered as
`d-A6`), and two more arenas now parse. **Lap T's published F-4 = 16.80 m is superseded by 16.4307
m.** Note the *max* falls hard, 37.51 → 26.08 m, and the spurious **0.0000 m** minimum under the v2
labels — a "spawn point" sitting exactly on a patrol point — disappears. That zero was the
displacement showing itself.

Corrected companions, complete-20: **F-3 = 35.5948 m** (was 35.88), **F-5 = 72.7985 m**,
**attack-ring max extent = 45.7066 m median** (33.18–56.81), **patrol-point nearest-neighbour gap =
11.8987 m median**.

### 4.4 ⚑ `D-U-1`, self-caught — `UNREACHED-T2` was my own acceptance gate

Lap S chose an orthonormality band of `[0.98, 1.02]` on each row-norm of the placement rotation
matrix; Lap T inherited it. `survivalworld_d` carries a legitimately **scaled** placement with row
norms `(0.9771, 0.9585, 0.9771)`. The record is otherwise perfect — valid string index, flag 0, and
the next record begins exactly 56 bytes later. **The gate rejected it, the strict parser halted at
record 139 of 276, and Lap T banked that halt as `UNREACHED-T2`: a format mystery that was in fact
my own threshold.**

**Scope of the repair: the acceptance BAND only**, widened to `[0.25, 4.0]`. No other reader logic
changed. **Row-norms actually observed across all 20 arenas: 0.939056 – 1.000423** — only
`survivalworld_d` uses any of the new headroom. And the band is no longer load-bearing: the
validator is **end-to-end** — the file *declares* a record count, and the parse must consume
exactly that many with a valid string index and a flag in {0,1} on every one. **That passes 20 of
20 now; it passed 18 of 20 before. `UNREACHED-T2` is CLOSED.**

### 4.5 ⚑ `D-U-2`, self-caught — Lap T's `D-T-2` is itself a casualty of `D-I20-1`

| basis | spawn → nearest beacon, median | inside the 8.0 m aura |
|---|---:|---:|
| **v2 labels** (Lap T's `D-T-2`, published as the correction) | **10.4726 m** | **32.7 %** |
| **v3 labels** (repaired) | **0.6089 m** | **83.3 %** |

Lap S's original F-12 said beacons sit **0.36 m** from spawn points. Lap T "corrected" that to a
10.47 m median and filed `D-T-2` calling the 0.36 m *"the MINIMUM reported as typical."* **On the
repaired labels Lap S was substantially right and Lap T's correction was computed on displaced
data.** I am reporting a defect in my own previous lap's defect report.

**What this does and does not change.** It does **not** resurrect a march-speed term: Lap T's
HEADLINE 1 — the beacon buff carries 23 run-speed-family slots, all present, all **zero** — is a
decode of the record chain and is untouched. What it changes is **`U-T-3`**: the beacon's
`+30 % attack speed / +50 % cast speed` aura covers **83 % of tier-16 spawn points**, not 33 %.
That is a threat-density term near the spawn, not a movement term, and it is **routed, not folded.**

### 4.6 The v3 artifact

`pm4u_map_placements_v3.csv` — **9,484 rows** (v2 had 9,205; the difference is the two arenas
`D-U-1` recovered). Each row carries `dbr` (repaired), **`v2_dbr` (the superseded label)**,
`string_index`, `file_offset`, `record_size`, `label_source` and `parse_gate`, so the displacement
is **auditable per row rather than asserted**. **Lap T's `pm4t_map_placements_v2.csv` is NOT
modified, NOT moved, NOT deleted** — the ledger amends, the record stands, exactly as Lap T treated
Lap S. `pm4u_geometry_v3.csv` (120 spawn points) supersedes `pm4t_geometry_corrected.csv`.

---

## § 5 — DEFECT TABLE

| # | defect | who caught it | disposition |
|---|---|---|---|
| **`D-I20-1`** | v2 CSV `dbr` column displaced one record | gamora (I-20), routed to me | **REPAIRED.** Cause decoded (`H-d-A`, index-first, array at `arr_off+4`); v3 emitted and verified. gamora named two causes and verified neither — correctly, under NOTE-9. **Hers was right to route; the fix was mine to make.** |
| **`D-U-1`** | inherited rotation acceptance band `[0.98, 1.02]` too tight; halted 2 arenas and was banked as `UNREACHED-T2` | **me, this lap** | **REPAIRED**, declared scope = the band only. 18 → **20 / 20** complete parses. `UNREACHED-T2` **CLOSED**. |
| **`D-U-2`** | Lap T's `D-T-2` beacon "correction" was computed on displaced labels; Lap S's F-12 was substantially right | **me, this lap, against my own prior lap** | **CORRECTED on the record.** Beacon median 10.4726 → **0.6089 m**; aura coverage 32.7 → **83.3 %**. `U-T-3` revived and **routed, not folded**. |
| **`D-U-3`** | my own limb-(a) entry counts are dominated by nameplate re-appearance; I published them as an arrival rate | **me, this lap, before handing them over** | **DEMOTED.** Priced at **11.05×** peak living; `H_GAP` sweep published. The interval distribution is a **strict upper bound** and carries the caveat in every row. F-10 unaffected. |
| **`D-U-4`** | **a pre-registered CONSEQUENCE departed from**: `V-d3` failed as written, and § 6.2 said "no v3 is emitted" | **me** | **DECLARED, not buried** (§ 4.2). Prediction graded **FAILED**; drafting error named; v3 emitted on the four verdicts that passed, with the reasoning in the open. |
| `D-PDEF-2` | monster containment needs decoded arena walls | carried from P-DEF | **STAYS OPEN.** Limb (c) did not reach walls; standing refusal exercised (§ 3). |
| `D-I19-2` / `D-Q1` / `D-P1` / `D-P2` | carried | — | untouched by this lap |

---

## § 6 — UNREACHED CENSUS

| # | term | status |
|---|---|---|
| `UNREACHED-S1` | body of `Proxy::AllKilled()` | **CARRIED.** Steam-DRM `.bind`, `.text` encrypted at rest. |
| `UNREACHED-S3` | which arena Matt played | **CARRIED.** Every world-asset number here is a distribution over 20 arenas. |
| `UNREACHED-S4` | is a nameplate birth a genuine spawn or a re-appearance | **CARRIED — but now PRICED** at 11.05× (`D-U-3`). |
| `UNREACHED-S5` / `S6` / `S7` | true spawn distance from video · new-wave vs straggler · `bonusSpawnStatus` | **CARRIED**, unchanged. |
| `UNREACHED-S8` | `.lvl` region contents | **⚑ PARTIALLY CLOSED.** Container, tiling, magic and header decoded 20/20; walls not. |
| `UNREACHED-T1` | the Route-2 march conversion constant | **CARRIED.** Every march number here still rides it. |
| `UNREACHED-T2` | the two halting `.map` parses | **⚑ CLOSED** — it was `D-U-1`, my own gate. |
| `UNREACHED-T3` | the monster state-transition table | **⚑ CLOSED BY EXPLANATION** — dispatch is by string through `SetState`; no table exists. |
| `UNREACHED-T4` | permanent/transient speed-term minority | **CARRIED**, unchanged. |
| `UNREACHED-T5` | `GetRadius()` / `ShouldRunTo()` values | **⚑ CLOSED** — `radius = 2.0`, `shouldRun = True`. |
| **`UNREACHED-U1`** | the AI update loop driving `ShouldFindEnemy → FindEnemiesInSight → EnemyFound` | **NEW.** Virtual dispatch; zero direct `call rel32` sites. Likely consumers named (`AngerUpdate` 0x0fba90, `PickRandomEnemyInView` 0x0fc550), **not claimed**. |
| **`UNREACHED-U2`** | whether `FindEnemiesInSight` applies a **line-of-sight** test | **NEW, and it is finding 1's soft spot.** The spatial query is an indirect call I did not follow. If LOS is enforced, walls could suppress the 80 m acquisition — and walls are `UNREACHED-U4`. |
| **`UNREACHED-U3`** | the entry condition for `ControllerMonsterStateAlertBeforePursue` | **NEW.** The state exists and plays an animation on entry; `DefaultEnemyFoundResponse` bypasses it. **An alert delay would be a real ramp term and it is unmeasured.** |
| **`UNREACHED-U4`** | arena walls / pathing blockers inside the `LVL` blob | **NEW.** `D-PDEF-2` stays open on it. No hull substituted. |

---

## § 7 — UNDECIDED (`U-U-*`) — published, none ruled

| # | term | why undecided | what would decide it |
|---|---|---|---|
| **`U-U-1`** | **does the 80 m `ViewDistance` actually acquire through walls?** | `UNREACHED-U2` + `UNREACHED-U4`. If LOS is enforced and the arena is partitioned, some packs acquire late. | following the spatial query at `[0x104e5294]`, or decoding the blocker layer |
| **`U-U-2`** | **how much of the ramp is `AlertBeforePursue` delay?** | `UNREACHED-U3`. An animation-length pause on some fraction of packs. | decoding `ShouldPlayRallyOrAlert`'s condition and the animation's duration |
| **`U-U-3`** | **is spawn → player really ~21–22 m?** | § 1.7 chains three things (march bracket, frustum radius, pooled-speed assumption). It agrees with the geometry, but it is inference. | registering a referent frame to an arena (`UNREACHED-S3`) |
| **`U-U-4`** | **the true arrival COUNT per wave** | `D-U-3` / `UNREACHED-S4`. Bounded above at 11.05× peak living, not resolved. | a plate-identity method robust to VFX blink, or an instrumented run |
| **`U-U-5`** | **which arena** | `UNREACHED-S3`, carried unchanged. | Matt naming it, or terrain registration |
| **`U-U-6`** | **the residual's carrier is NAMED as concurrency but not MEASURED on the sim side** | not my seam. I supply the referent's number; the sim's is I-21's. | I-21 |
| `U-T-3` | does the beacon's `+30 % / +50 %` matter in-aura? | **revived by `D-U-2`** at 83 % spawn coverage rather than 33 %. | a fold experiment, not research |
| `U-S-1` / `U-S-3` / `U-S-4` / `U-S-5` / `U-T-4` | carried | unchanged | unchanged |

---

## § 8 — HAND-OFF, SHAPED FOR THE SIM FOLD (I-21)

**What is now decode-true and foldable:**

1. **⚑ THE MARCH TARGET IS THE PLAYER, NOT A RING NODE.** `ViewDistance = 80.0 m` on 169/169 rolled
   tier-16 monsters; Patrol opts into scanning by explicit override; `EnemyFound → SetState("Pursue")`.
   **The 16.80 m nearest-patrol first march that I-20 folded is the wrong comparator, and the
   correction is unfavourable to the fold that already landed.** Grade **DECODED**, with
   `U-U-1`'s LOS caveat attached and required to travel with it.
2. **Arrival tolerance `radius = 2.0 m`** and **`shouldRun = True`** — decode-true, free (§ 2.4).
   Any patrol-based distance is effectively **F-4 − 2.0 m**.
3. **`pm4u_geometry_v3.csv`** — 120 tier-16 spawn points with per-spawn `to_nearest_patrol_m`,
   `to_patrol_centroid_m`, `to_nearest_beacon_m`, `inside_beacon_aura_8m`, ring extent.
   **SAMPLE PER SPAWN POINT from this distribution** (0.3253 – 26.0779 m, median 16.4307) — never
   from the scalar median. `R-PM4-51 part 3` asked for exactly this and I-20 correctly refused it
   because the labels were displaced; **the labels are repaired and it is now foldable.**
   Supersedes `pm4t_geometry_corrected.csv`.
4. **`pm4u_map_placements_v3.csv`** — 9,484 rows with `v2_dbr` retained for audit. Verified
   transitively against gamora's `geometry_agreement_v2` (§ 4.3).

**The referent-side grading targets:**

| quantity | referent value | bound direction |
|---|---|---|
| living count inside the 11.6 m window, **peak per wave** | **19 – 36, median 25** | **LOWER bound** (B-1) |
| t→50 % of that peak | **3.2670 s** (median over 10 waves) | as F-10 |
| t→90 % | **4.9670 s** | as F-10 |
| player net displacement per wave | 1.99 – 11.27 m, **median 3.61** | sign-free magnitude |
| player path length per wave | 40.2 – 83.0 m, straightness **0.060** | sign-free |

**Two explicit DO-NOTs:**

* **DO NOT grade against `pm4u_arrivals.csv`'s inter-entry interval distribution** (`D-U-3`). It is
  an upper bound contaminated ~11× by nameplate re-appearance. **The living-count ramp is the
  like-for-like functional and always was.**
* **DO NOT fold a march distance from § 1.7's implied 21–22 m as if it were decoded.** It is
  `INFERRED-WITH-EVIDENCE` and `U-U-3` is open. The **decoded** statement is the *target* (the
  player), not the *distance*.

**The arithmetic I would put in front of the conductor.** I-20's sim folded a **16.80 m** march and
reaches 50 % of its living-window peak at **9.7551 s** — **1.8× its own folded march time** at the
folded speed. The referent reaches 50 % at **3.2670 s**, which is **9.98–10.49 m** of march, on a
board whose decode-true target sits at **~21–22 m**. **The referent's board fills faster than a
uniform march to a nearer target would allow, and the sim's fills slower than a uniform march to a
farther one.** Distance is not the free variable. **Concurrency is** — how many bodies are in
flight and inside the window at once — and the referent's number for it is 19–36, median 25.

---

## § 9 — DIGESTS

Full 64-hex on every input consumed, every instrument run and every artifact emitted:
**`pm4u_digests.json`**. PREREGISTRATION
`7a250772bad3bf8cbce2e43455bc3e4dae2fee677aeedc1ffad978f3dda6b144` (hashed 2026-08-14T18:03:05Z,
before any instrument ran; recompute it).

---

*Landed by legolas, 2026-08-14. Four limbs, four landings, four self-caught defects — one of them
against my own previous lap and one of them a departure from my own pre-registration, both reported
at full size. The run's last named residual is renamed for a fourth time, and this time the binary
does the naming.*
