# WR3-KITE-COMMIT — THE CLEAN ABLATION, THE 283.14 RECONCILIATION, AND THE INSTANCE-4 REPAIR

**Date:** 2026-07-30 · **Author:** gamora (simulation seam) · **Class:** verdict note (micro-commission)
**Commission:** gandalf (RUN-CONDUCTOR), run **WR3-KITE-COMMIT** — **R-WR3-27(3)**, **R-WR3-26(5)**,
**R-WR3-27(5) instance 4**, **R-WR3-27(7)**
**Base:** engine `127ba505` on `main` · **not pushed** (the conductor pushes)
**Math note (written BEFORE the code and BEFORE the measurement, Discipline #1):**
`reincarnated-engine/src/reincarnated/simulation/math/wr3-clean-ablation-2026-07-30.md`
**Scope honoured:** the stage-map **HALT stands at `S0_NONE`**. **No calibration. No arm-default
change. No battery. No banked evidence root written** — the ablation owns a fresh root,
`output/kitcal_g5/wr3_clean_ablation/`.

---

## §0 — VERDICT, FIRST

| item | verdict |
|---|---|
| **(1) THE CLEAN ABLATION** | **DONE.** 5 arms × 3 leech legs × 30 seed-matched fights. **PREDICATE R PASS** — the three banked arms reproduce `wr3_s2b_f2_ablation.json` **to the last digit**. |
| **⚑ THE HEADLINE SURVIVES, AND ON BETTER GROUND** | **"The band is reachable; F-2 is what leaves it" HOLDS.** The clean arm B is **0.467 — IN the Matt-signed [0.40, 0.60] band**, nearer its centre than the banked 0.433, and it is a **shippable** configuration where the banked one was not. F-2 alone then takes it to **0.933**. |
| **⚑ THE CORRECTED F-2 ATTRIBUTION** | **+0.467** (was reported as +0.500). The banked figure **was** an upper bound, exactly as R-WR3-27(3) labelled it. Intake **−50.5 %** (608.5 → 301.0), not −54 %. |
| **⚑ THE CONFOUND IS NOT WHAT WE THOUGHT — IT IS WORSE, AND IT INVERTS** | **Disarming the engine flag did NOT remove icearmor. It made it PERMANENT.** The flag gates `_gd_icearmor_tick`, not `_gd_icearmor_cast`; `remaining_s` decrements only in `tick()`. Measured: buff UP on **95.0 %** of state reads with `tick_calls == 0`. The banked arm B ran **+35 % boss attack speed, +28 % cold, 25 % absorb, for the entire fight**. §2. |
| **(2) THE R-WR3-26(5) RECONCILIATION** | **LEGOLAS IS RIGHT. SAID FLATLY.** `283.14` was **three simultaneous far-band prong crossings** — reproduced exactly — and **three prongs are unreachable** at that band (`n_bounds(9.5) = (0,1)`). It is not a per-event maximum and is not comparable to `greatestDamageReceived`. **Charter should carry 95.36**; his 94.4 is the same number rider-free. §5. |
| **(3) INSTANCE-4 REPAIR** | **LANDED, and byte-inert — PROVEN, not asserted.** Stash-and-rerun over 30 fights **including 6 stage-2b-ARMED**: the whole artifact is **IDENTICAL**, `mech 6e20f7846cb07e0c` / `trace 14b08bfa6e95fffb`, reproducing R-WR3-27's banked digests. §6. |
| **(R-WR3-27(7)) FULL `tests/` SWEEP** | **62F / 9,861P / 21E in 22:51 = 83 names vs the 81 baseline. ⚑ +2, AND ONE OF THEM IS A DEFECT MY OWN `127ba505` SHIPPED** — an undeclared BQ-3 override-door site, in the very commit whose report said the sweep *"should be unmoved at 81"* as an explicitly-labelled expectation. **The expectation was wrong; only the sweep caught it.** Both deltas diagnosed and fixed; **post-fix baseline 81**. §7.2. |
| **Tests** | **19 new**, all passing. WR1+WR2+WR3 **4,019 pass, 0 fail** (was 4,000). Schema/emitter-adjacent **128 pass** (unchanged). |
| **⚑ A REPORTING DEFECT I WALKED INTO, IN MY OWN SEAM** | Eight of the nine stage-2b kit counters are **ABSENT, not zero**, on an engine-flag-OFF arm. My first draft printed `wave_casts = 0` for a wave that fired **63 times**. My own flag-split §2.1 named this exact hazard and fixed it for one counter only. §4. MIGRATION errata written; the engine widening is **routed, not landed**. |

---

## §1 — THE DECOMPOSITION TABLE (the deliverable, up top)

30 seeds, seed-matched to stage-2b §5 (`base_seed = 74000800 + i`), boss tier, `R2_proxy`,
`S0_NONE`. **Player win rate**; band = Matt-signed [0.40, 0.60] (R-WR3-17).

| arm | icearmor as the fight runs it | F-2 | **leech 0** | leech 0.05 | leech 0.08 | intake @ leech 0 |
|---|---|---|---|---|---|---|
| **A** stage 2 — no kit | absent | OFF | **0.567 IN BAND** | 1.000 | 1.000 | 785.6 (103.5 %) |
| **B\*** kit *(the BANKED "kit ONLY" arm)* | **PERMANENT** | OFF | **0.433 IN BAND** | 0.667 | 0.767 | 656.2 (86.5 %) |
| **D** kit *(NEW — closes the 2×2)* | **PERMANENT** | **ON** | 0.800 | 0.900 | 0.933 | 361.2 (47.6 %) |
| **B** kit *(NEW — the **CLEAN** arm B)* | **cycling, 33.2 %** | OFF | **0.467 IN BAND** | 0.733 | 0.900 | 608.5 (80.2 %) |
| **C** kit *(the banked full arm)* | cycling, 26.5 % | ON | 0.933 | 0.967 | 1.000 | 301.0 (39.7 %) |

### 1.1 The attribution, decomposed — **the terms the confound hid**

At leech 0, the decision-grade leg (R-WR3-25(4)):

```
Δkit                     =  B*  − A   =  0.433 − 0.567  =  −0.133     boss-side, harder   (unchanged)
Δicearmor  PERM→CYCLING  =  B   − B*  =  0.467 − 0.433  =  +0.033     ← the hidden term
ΔF2  | icearmor cycling  =  C   − B   =  0.933 − 0.467  =  +0.467     ← THE CORRECTED F-2 NUMBER
                                                            ─────────
                                        Δ sum = C − A   =  +0.366     telescopes exactly ✔

  the BANKED composite   =  C   − B*  =  0.933 − 0.433  =  +0.500     ← what was published as ΔF2
  ΔF2 | icearmor PERM    =  D   − B*  =  0.800 − 0.433  =  +0.367
  INTERACTION            =  0.467 − 0.367                =  +0.100
```

**Damage taken**, same leg: `Δkit −129.4` · `Δicearmor −47.7` · **`ΔF2 −307.5` (608.5 → 301.0 =
−50.5 %)**. The banked composite was −355.2 (−54.1 %).

**Paired per-seed discordance** (the honest small-sample statement; 30 seeds, SE ≈ 0.091, so a
±0.10 gap is one standard error and is not a finding):

| contrast | seeds flipping **player-ward** | flipping **boss-ward** |
|---|---|---|
| **F-2** (C vs clean B) | **15** | 1 |
| **icearmor perm→cycling** (clean B vs B\*), leech 0 / 0.05 / 0.08 | 1 / 2 / 4 = **7** | **0 / 0 / 0** |

F-2 is decisive at 15:1. The icearmor term is **small but not noise**: it never once flips a seed
boss-ward across three legs, so the *sign* is real even though +0.033 alone is not.

### 1.2 What this does to stage-2b §5's three decision-grade findings

| § | finding as published | status now |
|---|---|---|
| **5(1)** | *"F-2 cuts intake 54 % and moves win 0.433 → 0.933"* | **AMENDED, direction intact.** Clean: **0.467 → 0.933 (+0.467)**, intake **−50.5 %**. The `+0.500` was an upper bound and is now bounded. F-2 remains the largest single intervention in the run by a factor of ~3.5 over the kit. |
| **5(2)** | *"THE KIT WORKS — arm B at 0.433 is inside the band"* | **SURVIVES, ON A DIFFERENT ARM, AND STRONGER.** The 0.433 arm ran a **permanently-up boss buff** and is not a shippable configuration. The shippable neighbour — kit with icearmor cycling correctly — is **0.467**, also in band and nearer its centre. **⚑ The `Δkit = −0.133` in that finding is likewise not "the kit": it is *the kit plus permanent icearmor*.** The kit's own contribution is not separable with the current flag set (§3). |
| **5(3)** | *"H1 on the battery is a lifesteal reading"* | **UNTOUCHED and re-confirmed.** All three leech legs reproduce to the digit; at leech 0.05 the stage-2 arm still goes 0.567 → 1.000. |

### 1.3 And to R-WR3-25's headline

> *"The band is reachable; F-2 is what leaves it."*

**BOTH CLAUSES HOLD, and the first is now better supported than when it was written.** Reachable at
a **shippable** arm (clean B, 0.467) rather than at a configuration no build could ship. F-2 alone
carries it out of band (+0.467, 15 seeds to 1). **No charter amendment is owed to the headline** —
only to the two attributions underneath it, §1.2.

---

## §2 — ⚑ THE FINDING: THE BANKED ARM B RAN **PERMANENT** ICEARMOR

R-WR3-27(3), my own stage-2b §6(2), and the math note I wrote three hours ago all say the engine
flag *"disarmed F-2 and the icearmor tick together"*, and all three then treat that as *"icearmor
OFF"*. **The first half is correct. The inference is backwards.**

```
spatial_engine.py:7377   if self._wr3_stage2b_v1:   self._gd_icearmor_tick(dt)   ← FLAG-GATED
spatial_engine.py:7709   elif skill.get(_GD_ICEARMOR_KEY) is not None:            ← PACKET-DRIVEN,
                              self._gd_icearmor_cast(mob, skill, elapsed)            behind NO flag
gd_boss_kit.IceArmorState:  `remaining_s` is decremented ONLY by `tick()`
```

With the packets armed and the tick off, the boss casts icearmor once and **the buff never
expires**.

**MEASURED, not read off the source** (`simulation/notes/wr3_icearmor_uptick_probe_2026_07_30.py`,
banked; shims tally `is_up` reads and mutate nothing; 30 seed-matched fights per arm):

| arm | `fires` | `tick_calls` | `is_up` TRUE / reads | duty |
|---|---|---|---|---|
| **B\*** — the banked arm B | 30 | **0** | 574 / 604 | **95.0 %** |
| **B** — clean | 30 | 7,203 | 168 / 506 | **33.2 %** |
| **C** — full | 34 | 10,623 | 240 / 904 | 26.5 % |

The clean arm's 33.2 % independently reproduces the battery's measured **G-I1 uptime 0.342 /
0.347 / 0.344** — which is the check that the shim is not distorting the fight it measures. The
residual 5 % on B\* are the reads before the first cast lands.

**⇒ The banked arm B is not "kit minus icearmor". It is "kit with +35 % boss attack speed, +28 %
boss cold and 25 % boss absorb, permanently."** Every artifact and every sentence carrying the
label *"icearmor OFF"* on a packets-armed run is mislabelled, including
`wr3_s2b_f2_ablation.json`'s key `"B kit ONLY (F-2+icearmor OFF)"`. **The JSON is not rewritten** —
it is the record of what ran; the corrected labels live in the new artifact's `arm_titles` and
`icearmor_semantics_correction` blocks, and a test pins the mechanism.

**THIS IS THE THIRD OCCURRENCE THIS RUN OF ONE SHAPE:** a mechanism whose *state object* is created
by one path and *advanced* by another, where disabling the second leaves the first in a degenerate
regime. R-WR3-15's `is_boss`-on-the-wrong-object; the icearmor cooldown-init at 32.0 s (stage-2b
§6); and now this. The first two produced a mechanism measuring **nothing**; this one produced a
mechanism measuring **everything, forever**. Same shape, opposite degeneracy, and the second is
more dangerous because every counter looks plausible.

---

## §3 — WHAT THIS RUN **CANNOT** SAY, STATED BEFORE ANYONE ASKS IT TO

**ICEARMOR-ALONE (present vs absent) IS NOT MEASURABLE WITH THE CURRENT FLAG SET.** No flag removes
the icearmor *cast* — it is packet-driven, and the packet is the kit. The three reachable regimes
are `absent-because-no-kit` (arm A), `permanent` and `cycling`. What §1.1's second term measures is
therefore **`Δ(permanent → cycling)`**, and the artifact names it
`delta_icearmor_PERMANENT_to_CYCLING` rather than `delta_icearmor`.

**CONSEQUENCE FOR R-WR3-25(5).** Icearmor's promotion to **rank 2** in the loss-mechanism ranking
rests on a *"twice-the-ability, up 37.5 % of the fight"* warrant that this run neither confirms nor
refutes: the only icearmor contrast available moves the win rate **+0.033** and intake **−47.7 HP**,
and that is the contrast between *too much* icearmor and *the right amount*, not between icearmor
and none. **The rank is not challenged here. It is UNMEASURED, and it was previously believed
measured.** Closing it needs a packet-level `icearmor` kill-switch — a mechanism change, out of
scope for a measurement commission. **ROUTED (§8).**

**`ΔF2` is unaffected by all of this.** The F-2 flag is clean: `B_clean` and `C` differ in F-2 and
in nothing else, and both run icearmor cycling. That contrast is exactly what R-WR3-27(3)
authorized and it is the one the Matt-held fork needs.

---

## §4 — ⚑ THE REPORTING DEFECT, DECLARED RATHER THAN QUIETLY FIXED

`wave_casts` · `wave_hits` · `blizzard_casts` · `blizzard_hits` · `blizzard_slows` ·
`icearmor_casts` · `icearmor_up_ticks` · `icearmor_total_ticks` are added to the result dict
**inside `if wr3_stage2b_v1:`** (`spatial_engine.py:9823`). On an engine-flag-OFF arm they are
**absent**. My cell's first draft read them as `r.get(k) or 0` and printed:

```
B_conf   wave 0/0  bliz 0  ice 0      ← what the draft reported
B_conf   wave 63   bliz 46  ice 30    ← what actually happened (counted by wrapping the cast methods)
```

**MIGRATION.md §3's sentence *"All default 0"* is wrong**, and §3a's table column *"kit + icearmor"*
is misleading for icearmor in both `False` rows. Both are corrected in a new **MIGRATION §3b
errata**. star-lord: **NO ACTION** — no telemetry table, no export schema, no emitted field moves;
this is a reading correction on an existing result-dict surface.

**The meta-finding is the part worth keeping.** The F-2 flag-split note's §2.1 named this exact
hazard — *"a reader cannot tell 'never steered' from 'never armed'"* — and fixed it for
`inflight_steers` **alone**, leaving the other eight counters in the same block with the same
defect. The very next consumer of those counters was me, one commission later, and I read an
absence as a measurement. **A convention applied to one field is not a convention.** The engine-side
widening is a residual-key schema change and this is a measurement commission: **routed, not
landed** (§8).

---

## §5 — R-WR3-26(5) RECONCILIATION. **LEGOLAS IS RIGHT.**

### 5.1 What `283.14` actually was — reproduced exactly

The stage-2b column headed *"A-NOVA-2 ceiling"* is `nova_delivered(r = 9.5 m, count = 3)` —
**THREE SIMULTANEOUS FAR-BAND PRONG CROSSINGS**, delivered **post-mitigation**, `pre` / `R2_proxy`:

| stage | column said | recomputed `count=3` | match |
|---|---|---|---|
| `S0_NONE` | 1274.11 | **1274.112** | exact |
| `S1_PAK` | 895.67 | **895.671** | exact |
| `S2_FULL` | 283.14 | **286.081** | 1.0 % off — see 5.2 |

- **pre or post mitigation?** **Post.**
- **summed simultaneous events?** **Yes — three of them.**
- **which band?** **The 140 % far band** (≥ 9.0 m).
- **comparable to a per-event maximum like `greatestDamageReceived`?** **NO.** That field is the
  worst *single* receipt; this is a three-crossing sum. **Category error, and it was mine.**

**AND THE QUANTITY IS NOT REACHABLE AT ALL.** `n_bounds(9.5, STAR) = (0, 1)` — at the far band the
star lands **at most one** prong; its maximum reachable count *anywhere* is **2**, only at the 2.0 m
body-collision floor. **Three simultaneous far-band prongs cannot happen in this fixture.**

My prose sentence — *"the entire Primordian kit's single-event ceiling is 283.14"* — is wrong three
ways: not single-event, not the entire kit (wave 91.37 and blizzard 45.93 are separate rows), and
mis-ordered. **The banked instrument was right the whole time**: `a_nova_2_ceiling()` respects
`n_bounds` and returns **359.55** at `S0_NONE` / **95.36** at `S2_FULL`, and that is what
`wr3_cell_s2b_statistics.json` → `outgoing_stage_sidecar` carries. **The prose and the artifact
disagreed and nobody checked** — including me, in the note that printed both.

### 5.2 The 1.0 % residual is an order-of-operations defect

`283.14405 = 359.548 × 0.2625 × 3` — the outgoing stage applied **after** mitigation. Correct order
gives **286.081**. GD's armour operator is **piecewise, not linear**: a larger incoming event clears
the absorb threshold, so per-prong delivery rises 359.5 → 384.8 → 424.7 across counts 1 → 2 → 3. At
the *single*-prong far band the leg is armour-saturated and both orders agree to the digit
(94.3813), which is why this never surfaced in a number that mattered.

### 5.3 The `~107 worst prong` — his diagnosis of *that* figure is wrong; his conclusion is right

Legolas §4: *"the commission's '~107 worst nova prong' is the **100 %-band** figure (mine: 103.7
pre-mitigation); the far band is the governing case."*

**It was never a 100 %-band figure.** `107.0895 = 407.96 × 0.2625` — the **far-band SINGLE prong**
on the `pre_endpoint` / `R2_proxy_resists_low` leg (the low-resist gear endpoint), **post**-mitigation
and rider-free; **108.07** with the ×1.06 physical rider `STAGE_S2_FULL` carries in its own
definition. The 100 %-band single prongs at `S2_FULL` are **68.11** (`R2_proxy`) and **77.19**
(`resists_low`) — neither is his 103.7 nor my 107. His reconstruction found a different quantity
that happened to land nearby.

**His substantive point stands and the correction does not touch it**: the far band governs, and
the comparator he reached for is the right one. What my 107 *was* is the far band **on the wrong
leg for a headline** — the endpoint gear vector rather than the `pre` leg the fork is argued on,
which is why the charter figure is **95.36** and not 108.07.

**⚑ AND HIS CONDITIONAL ON 283 WAS EXACTLY RIGHT, WORD FOR WORD.** He wrote: *"If 283 came from
summing simultaneous events it is not comparable to `greatestDamageReceived`, which is a per-event
maximum."* **It did, and it is not.** He was careful enough to state the discriminating condition
without being able to check it; §5.1 checks it and the condition holds.

### 5.4 Which figure the charter should carry

**`95.36`** — the `S2_FULL` **far-band SINGLE prong**, post-mitigation, `pre` / `R2_proxy`,
rider-inclusive. Legolas's **94.4** is the identical quantity rider-free (**94.3813**): **he
reproduced it to 1.0 %, and the residual is fully accounted for.** Whole-kit worst *reachable*
single event at `S2_FULL` = `max(nova 95.36, wave 91.37, blizzard 45.93)` = **95.36** (**108.07** on
the endpoint leg).

**`283.14` should be STRUCK, not corrected** — its repaired value (286.08) still names an
unreachable event.

**⚑ AND THE CORRECTION CUTS AGAINST THE ARM I ARGUED FOR.** Nothing in R-WR3-26's ruling moves —
the decision substrate is legolas's roster ceiling sweep (S2 252.9 / 240.3 vs 260.498), which is
independent of this figure. But the correction **strengthens R-WR3-26(7)'s lean toward `S1_PAK`**:
under `S2_FULL` the Primordian kit's worst *reachable* single event is not 283 but **95**, i.e.
**2.7× below** the referent's 260.498 rather than 8 % above it. My stage-2b §1.3 listed 283.14 as
evidence **against** `S2_FULL`; corrected, it is much *stronger* evidence against `S2_FULL`. **I was
arguing my own case with a number that argues it better once fixed, and in the direction away from
the arm I said I believed was mechanically correct.**

---

## §6 — INSTANCE-4 REPAIR (R-WR3-27(5)). TRIVIAL, AND THE NOTE SAYS SO.

**The mathematics is one line** and the math note §6 says so rather than manufacturing ceremony:

```
skillLevel(charLevel) = floor(charLevel / 4) + 1
    cl 16 → 5    cl 17 → 5    cl 18 → 5    cl 19 → 5        ⇒ INVARIANT over [16, 19]
```

**What landed:**

- `gd_boss_kit`: `gd_skill_rank_at()` (**one reader** for a formula previously written out in prose
  in two modules at two different charLevels), `PRIMORDIAN_RANK_INVARIANT_LEVELS = (16,17,18,19)`
  — **deliberately WIDER than the 18–19 bracket, so it spans the whole disagreement and not only
  the side that won** — `PRIMORDIAN_KIT_RANK = 5`, and `assert_primordian_rank_invariance()`.
- `gd_nova`: the in-place *"boss level 16"* derivation is **gone**; the site now names
  `gd_boss_kit.PRIMORDIAN_CHAR_LEVEL` as the one source and **declares the invariance**, with
  `assert_star_rank_provenance()` making it executable.
- **NOT called at import**, deliberately, for two reasons stated at the site: it keeps `gd_boss_kit`
  a deferred import (the nova's pre-stage-2b import graph), and an import-time assertion would make
  an inert repair capable of changing behaviour **in a commission whose predicate is byte-identity**.
  A test calls it; the fight never does.

**⚑ THE SHARPEST FACT THE REPAIR SURFACED, now a test:** at the **player's** charLevel 13 the
formula returns **rank 4** — which is exactly the rank the superseded `PRIMORDIAN_FRIGIDRING`
carries. The star's arrays being right was an accident of the intermediate 16, not of the reasoning
that produced it. **The binding-class error was one step from biting.**

**BYTE-IDENTITY — PROVEN, NOT ASSERTED.** Stash-and-rerun through the banked harness
`notes/wr3_f2_flag_split_byteid_2026_07_30.py`, 30 fights = 24 UNARMED full-mix + **6 STAGE-2b
ARMED** boss fights:

| | before (stashed = `127ba505`) | after | |
|---|---|---|---|
| mechanical digest | `6e20f7846cb07e0c` | `6e20f7846cb07e0c` | **IDENTICAL** |
| trace digest (`prong_count` popped) | `14b08bfa6e95fffb` | `14b08bfa6e95fffb` | **IDENTICAL** |
| `prong_count` records | 194 | 194 | identical |
| whole artifact, compared field-by-field | — | — | **IDENTICAL** |

Both digests also reproduce R-WR3-27(1)'s banked pair, so the proof chains to the previous landing
rather than standing alone.

**INSTANCE 5 NOT TOUCHED** (HELD to stage-2c). One thing did change in its vicinity and I name it:
the `gd_boss_kit` comment that justified holding it by calling `OppositionRow.char_level` *"a
FIXTURE-WIDE key (HP derivation, escort levels)"* is **factually wrong** — the grep finds one
reference, a metadata dict — and now says so in source. **The hold stands on the real reason** (the
field is emitted into every banked artifact) rather than on a coupling that does not exist. Comment
only; zero arithmetic.

---

## §7 — TESTS, SUITE STATE, AND REPRODUCTION

### 7.1 Tests

| item | value |
|---|---|
| New unit tests | **19** in `tests/test_wr3_clean_ablation.py`, all passing |
| WR1 + WR2 + WR3 (`-k "wr1 or wr2 or wr3"`) | **4,019 pass, 0 fail** (was 4,000 at `127ba505`; +19) |
| Schema / emitter-adjacent (`-k "replica or telegraph or frame or spatial_telemetry"`) | **128 pass, 0 fail** — unchanged |

Written against the failure modes this work can actually have:

- `test_icearmor_is_PERMANENT_when_the_tick_is_disabled` + `test_the_engine_flag_gates_the_TICK_and_not_the_CAST`
  — **the pair that pins §2.** One asserts the mechanism on the state object, the other asserts the
  gate's location structurally, so a refactor that moves the gate is caught even if nobody re-runs
  the ablation.
- `test_the_two_modules_agree_on_the_boss_level` — **the instance-4 guard**; re-introducing a second
  in-place derivation is precisely what the repair removed.
- `test_the_PLAYERS_own_level_would_have_given_rank_4_not_5` — pins the near-miss so the
  binding-class pattern stays visible at the site.
- `test_the_kit_counters_are_ABSENT_not_zero_on_an_engine_flag_OFF_arm` — §4's defect pinned as a
  **known property**, so the next consumer meets a test instead of a trap.
- `test_the_provenance_assertion_is_NOT_called_at_import` — AST-asserted; an import-time raise would
  break the byte-identity predicate the repair is landed under.
- `test_PREDICATE_R_the_banked_arms_reproduce_at_leech_0` — if the banked arms stop reproducing, no
  row of this report's table is comparable to stage-2b §5.
- `test_the_seed_constants_are_the_BANKED_ones` — seed matching is the whole instrument.
- `test_no_banked_root_is_written`.

### 7.2 The full `tests/` sweep owed under R-WR3-27(7)

**Method note first, because it changes what the number means.** A sweep was in flight from the
start of this session; I **killed and restarted it** after the source edits landed. pytest imports
production modules at collection, so the first sweep was measuring `127ba505`'s modules from
`sys.modules` and did not include the new test file — it would have been a baseline measurement
wearing a post-change label. The banked number below is from the **restarted** sweep on the final
tree.

> **RESULT: 62 failed, 9,861 passed, 21 errors in 1,371 s (22:51) = 83 failing names against the
> 81-name baseline. ⚑ +2, AND THE SWEEP EARNED ITS 23 MINUTES — one of the two is a real defect
> that MY OWN PREVIOUS LANDING SHIPPED.**

Name-diff against the banked baseline (`gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt`):
**2 new, 0 gone.** Both diagnosed, neither left standing:

| new failing name | cause | disposition |
|---|---|---|
| `test_bq3_calibration_override_door.py::TestStaticContainment::test_T8_no_production_callsite_enables_overrides` | **A REAL CONTAINMENT DECLARATION GAP — three files, and one of them predates this commission.** | **FIXED** — three deliberate `_DOOR_ALLOW_LIST` entries |
| `test_kitcal_g5_harness.py::test_G5_W1_untracked_loaded_source_is_invisible_until_it_is_imported` | **A WORKING-TREE STATE ARTIFACT, not a code defect.** The test forces `git status` clean and then asserts the `-dirty` stamp comes *only* from untracked-**loaded** source. My new modules were untracked **and** imported by the new test file at sweep time, so `git ls-files --others` named them and the clean-stamp assertion at step (0) failed. **This is the WARN-1 detector working exactly as designed** — it is supposed to notice that the code that ran is in no commit. | **RESOLVES ON COMMIT** (verified, §7.2.1) |

**⚑ THE T8 FINDING, AND IT IS ABOUT MY LAST REPORT, NOT THIS ONE.** The three offending files are
`wr3_cell_cleanabl_2026_07_30.py` and `notes/wr3_icearmor_uptick_probe_2026_07_30.py` (both this
commission) **and `notes/wr3_f2_flag_split_byteid_2026_07_30.py` — which shipped at `127ba505`,
undeclared.** That report's §5.1 said the sweep *"should be unmoved at 81"* and was careful to
label it *"an expectation, explicitly NOT a measurement"*. **The expectation was wrong: `127ba505`
shipped an 82nd name.** R-WR3-27(7) owed the measurement so that an expectation could not stand in
for one — and it did not stand. **The honest sentence is that my own carefulness about labelling
the guess did not stop the guess being wrong; only the sweep did.**

All three are the same class as the three existing allow-list entries — measurement drivers, no
season, no convergence loop, no production telemetry — and **the door is not optional, proven not
argued**: with `allow_calibration_overrides=False` the construction raises `CalibrationOverrideLeak`
(*"class_dict 'gd-werewolf-kitcal-1' carries '_calibration_overrides'"*). **And closing it would
falsify the measurement**: the banked ablation ran with the door open on all 270 of its fights, so
PREDICATE R is only meaningful if the door state matches.

**Non-blinding, decidable by enumeration** (re-run, not remembered): **7** door-opening sites in the
tree, **6** allow-list entries, offenders **with** the three = `[]`, offenders **without** = exactly
**three**, one per named module; **dead entries = none**. `test_bq3_calibration_override_door.py`:
**39 pass**.

**⇒ POST-FIX BASELINE: 81, unmoved.** §7.2.1 records the verification.

#### 7.2.1 Post-fix verification

Both names re-run green after the allow-list entries and the commit that makes the new modules
tracked; `_untracked_loaded_source()` returns `[]` with the cell and the probe imported, and the
harness stamp reads a clean `5731ce07`. **A confirming full sweep was then fired on the committed
tree** — that is the number to trust, and it was fired knowing that a disagreement with 81 would
itself be the finding.

> **CONFIRMING SWEEP AT `5731ce07`: 60 failed, 9,863 passed, 21 errors in 1,322.72 s (22:02) =
> 81 failing names.**
>
> **Name-diff against the banked 81-name baseline: 0 new, 0 gone — EXACT MATCH.**

**⇒ R-WR3-27(7) IS DISCHARGED WITH A MEASUREMENT, AND THE BASELINE IS 81, UNMOVED.** Not an
expectation this time, and the distinction is not pedantic: the *first* sweep is the reason there
was anything to fix, and it fixed something that predates this commission.

The banked failure-name list
(`gamora/notes/2026-07-29-wr1-battery-3-regression-failure-names.txt`) is therefore **still
current and is not rewritten**.

### 7.3 Reproduction

```bash
cd ~/Games/reincarnated-engine && export PYTHONPATH=src
python3 -m pytest tests/test_wr3_clean_ablation.py -q -p no:randomly          # 19 pass
python3 -m pytest tests/ -q -p no:randomly -k "wr1 or wr2 or wr3"             # 4,019 pass

# the clean ablation (fresh root; SEQUENTIAL legs, Discipline #3)
python3 -c "from reincarnated.simulation import wr3_cell_cleanabl_2026_07_30 as C; C.main()"

# the icearmor permanence probe (BANKED, not /tmp)
python3 src/reincarnated/simulation/notes/wr3_icearmor_uptick_probe_2026_07_30.py

# byte identity for the instance-4 repair — run, stash, run, compare
B=src/reincarnated/simulation/notes/wr3_f2_flag_split_byteid_2026_07_30.py
python3 $B /tmp/inst4_after.json
git stash push -- src/reincarnated/simulation/gd_nova.py src/reincarnated/simulation/gd_boss_kit.py
python3 $B /tmp/inst4_before.json && git stash pop
```

Artifacts: `output/kitcal_g5/wr3_clean_ablation/wr3_clean_ablation.json` (+ per-seed win vectors,
banked so the next pairing question is answerable without a re-run) and
`.../wr3_icearmor_uptick_probe.json`. **Nothing was written to `wr2_battery_after/`,
`wr3_battery_s2/`, `wr3_battery_s2b/` or `wr3_stagesweep_s2b/`.**

---

## §8 — WHAT THE CONDUCTOR OWES A RULING ON

1. **⚑ THE ARM-B RE-LABEL IS A CHARTER CORRECTION, NOT A FOOTNOTE (§2).** R-WR3-27(3) records the
   confound as *"disarmed F-2 and the icearmor tick together"*. Measured, it disarmed F-2 and made
   icearmor **permanent**. Every sentence in R-WR3-25 and R-WR3-27 reading arm B as *"kit only"* or
   *"icearmor OFF"* needs the correction. **The headline itself survives (§1.3).**
2. **⚑ ICEARMOR'S RANK-2 PROMOTION IS UNMEASURED, AND WAS BELIEVED MEASURED (§3).** R-WR3-25(5)
   promoted it on a *"twice the ability, up 37.5 %"* warrant. No arm in the tree removes it. The
   only available contrast is permanent-vs-cycling. **Not challenged — UNMEASURED.** Closing it
   wants a packet-level icearmor kill-switch (a mechanism change; not in a measurement commission).
   **REQUESTING AUTHORIZATION**, or an explicit ruling that the rank stands unmeasured.
3. **⚑ THE `Δkit = −0.133` IN STAGE-2b §5 IS ALSO NOT "THE KIT" (§1.2).** It is *kit + permanent
   icearmor* vs *no kit*. Same flag set, same limitation. Rides (2) if authorized.
4. **THE RESIDUAL-KEY WIDENING (§4).** Eight counters are absent-not-zero on a flag-OFF arm. The
   fix is one `if`; it is a result-dict schema change and I did not land it. **Routed.** The
   companion is a discipline question for jack-ryan, alongside R-WR3-27(5)'s standing check: **a
   convention (P-2's measured-zero/unmeasured-zero rule) applied to one field is not a convention** —
   it wants a rule that any conditionally-emitted counter block declares its own absence.
5. **283.14 SHOULD BE STRUCK FROM THE CHARTER (§5).** Replace with **95.36** (rider-inclusive
   far-band single prong, `pre`/`R2_proxy`); legolas's 94.4 is the rider-free same number. The
   correction **strengthens R-WR3-26(7)'s S1_PAK lean** — against the arm I argued for.
6. **INSTANCE 5 STILL HELD**, and its stated justification in `gd_boss_kit` is now corrected in
   source (§6). The hold rests on the banked-artifact argument alone.
7. **THE STATE-OBJECT DEGENERACY SHAPE HAS THREE OCCURRENCES THIS RUN (§2)** — R-WR3-15's
   `is_boss`-on-the-wrong-object, the icearmor cooldown-init, and now the tick/cast split. Two
   produced a mechanism measuring nothing; one produced a mechanism measuring everything, forever.
   **That is a second named class**, and the "measuring everything" variant is the dangerous one
   because every counter it emits looks plausible.
8. **⚑ THE BQ-3 DOOR DECLARATION IS NOW A FOUR-OCCURRENCE CLASS, AND THE FOURTH CAUGHT ME (§7.2).**
   Every occurrence has been a *measurement driver* that its author did not think of as "a shipped
   module" — and three of the four were found by the full-regression name-diff rather than by the
   author. **The full sweep is the only instrument that has ever caught this**, which is a direct
   argument for R-WR3-27(7)'s standing requirement: an expectation, however carefully labelled as
   one, is not a substitute. Mine was labelled correctly and was still wrong.

---

*WR3-KITE-COMMIT clean ablation + R-WR3-26(5) reconciliation + instance-4 repair — gamora,
simulation seam, 2026-07-30. Neither repo pushed.*
