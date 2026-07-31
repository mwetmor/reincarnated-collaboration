# WR3-KITE-COMMIT — F-2's OWN FLAG, `prong_count`, AND THE BINDING-CLASS AUDIT

**Date:** 2026-07-30 · **Author:** gamora (simulation seam) · **Class:** verdict note (micro-commission)
**Commission:** gandalf (RUN-CONDUCTOR), run **WR3-KITE-COMMIT** — **R-WR3-25(3), (10), (7)**
**Base:** `97d51798` · **Engine commit:** `127ba505` on `main`, **NOT pushed** (the conductor pushes)
**Math note (written BEFORE the code, Discipline #1):**
`reincarnated-engine/src/reincarnated/simulation/math/wr3-f2-flag-split-2026-07-30.md`
**Scope honoured:** PLUMBING ONLY. **No battery re-fire. No calibration. No arm-default change.**
The stage-map **HALT stands at `S0_NONE`.**

---

## §0 — VERDICT, FIRST

| item | verdict |
|---|---|
| **(3) F-2 gets its own flag** | **DONE.** Tri-state `wr3_f2_inflight_v1`, `None` = INHERIT. All four corners of the 2×2 smoke-verified non-vacuous (§1.3). |
| **(10) `prong_count` emitted** | **DONE.** Additive, `replica-frame/v1` **stays v1**, MIGRATION extended. 16 on 47 nova records, `null` on all 147 others. |
| **(7) binding-class grep-audit** | **DONE, read-only. TWO further instances found**, both arithmetically INERT, one of them a live **cross-module contradiction** (boss level 16 vs 18). Nothing fixed. |
| **Flag-OFF / `inherit` byte identity vs `97d51798`** | **PROVEN by stash-and-rerun, not asserted.** Mechanical digest `6e20f7846cb07e0c` and trace digest `14b08bfa6e95fffb` **identical** on both trees over 30 fights. |
| **Effective defaults** | **UNMOVED.** Whether F-2 ships ON remains **HELD FOR MATT**. A test pins every entry point's default at `None`. |
| **Tests** | **18 new**, all passing. WR1+WR2+WR3 **4,000 pass, 0 fail**. Schema/emitter-adjacent suites **128 pass**. |
| **⚑ ONE CORRECTION TO MY OWN STAGE-2b §5** | **The banked arm B CONFOUNDED F-2 WITH ICEARMOR.** §6(2) — the `+0.500` attributed to F-2 is an **UPPER bound**. |
| **⚑ ONE DECLARED OUT-OF-SCOPE REPAIR** | `--help` on the G-5 harness has raised `TypeError` since WR2-B. One character. §1.4 — declared, not buried. |
| **⚑ ONE AMENDED PREDICATE** | The math note pre-registered stage-2b's `a0c6b5c8f6c8795f`; **I did not reproduce that value** and say so in §3 rather than quietly satisfying a different one. The instrument is now **banked**, and it covers a surface the old one did not. |

---

## §1 — F-2 GETS ITS OWN FLAG (R-WR3-25(3))

### 1.1 The attribution argument, as an equation

Stage-2b report §5, seed-matched, 30 seeds, boss tier, leech 0:

```
H1(kit only) − H1(stage 2)   = 0.433 − 0.567 = −0.134     the KIT   (boss-side, harder)
H1(kit+F-2)  − H1(kit only)  = 0.933 − 0.433 = +0.500     F-2       (player-side, easier)
                                    SUM       = +0.366     ← the ONLY thing one flag exposes
```

The sum has **the sign of neither term.** That is the defect, and it is why this is not cosmetic.

### 1.2 THE MAPPING — old flag state → new flag pair

`wr3_f2_inflight_v1: Optional[bool] = None` on `SpatialFightEngine`, `run_spatial_fight`,
`run_one_fight` and `drive`; CLI `--wr3-f2-inflight {inherit,on,off}` (default `inherit`).

```
f2_effective = wr3_stage2b_v1      if wr3_f2_inflight_v1 is None    (INHERIT — the default)
             = bool(...)           otherwise                        (OVERRIDE)
```

| `wr3_stage2b_v1` | `wr3_f2_inflight_v1` | CLI | F-2 steering | kit + icearmor | label | status |
|---|---|---|---|---|---|---|
| `False` | **`None`** | *(default)* | **OFF** | **OFF** | *(none)* | **today's OFF** — the byte-identity predicate |
| `True` | **`None`** | *(default)* | **ON** | **ON** | `_s2bv1` | **today's ON** — every banked stage-2b figure |
| `True` | `False` | `--wr3-f2-inflight off` | OFF | ON | `_s2bv1_f2off` | **NEW** — a *clean* arm B (§6(2)) |
| `False` | `True` | `--wr3-f2-inflight on` | ON | OFF | `_f2on` | **NEW** — F-2 alone on a stage-2 star |

**WHY TRI-STATE, in one sentence:** `None`-inherits makes the reproduction **structural — no call
site changes, so no call site can be missed**; a plain `bool = False` would have failed *silently*
on any caller I overlooked, by producing a different fight rather than an error. (Math note §2.)

**THE GEOMETRY GATE STILL DOMINATES.** SS-S2B-1 keyed F-2 to the star hit test
(`threat_half_width_m is not None`), not to a flag. That predicate is evaluated **inside** the
flag's branch and is unchanged — the flag can only ever **subtract** from what geometry allows.

**`inherit` ADDS NOTHING TO THE ARTIFACT LABEL** — deliberately. A suffix on the default would
orphan every directory in the stage-2b evidence chain. The two new arms are suffixed and are
**NON-POOLABLE** with an inherit run.

**⚑ ONE CONSEQUENCE ANYONE RUNNING THE NEW ARM MUST KNOW FIRST: gate `G-F2` reads `FAIL` on an
`_f2off` run, and that is the mechanism working.** `G-F2` grades *"in-flight steering events > 0"* —
R-WR3-23(7)'s mechanism-existence proof — and `_f2off` deliberately drives that counter to zero.
Read as a defect it is exactly backwards; it is the same shape as R-WR3-12(8.3)'s predicted
win-rate FALL. Nothing raises: it is an artifact-level grade, not a runtime assertion. **Verified by
running the arm end-to-end through the CLI — the smoke completes and writes its report.**

**AND THE ARM IS DECLARED IN-BAND, not only in the directory name.** On the two new arms the G-5
report's `non_poolable_with` list gains an entry naming the forced F-2 state. A label is out-of-band
for anyone reading the JSON, and that is exactly the hazard that block was built for (*"each armed
mechanism adds its own non-poolability"*). Verified: an `inherit` report's `non_poolable_with` is
**byte-unchanged**.

### 1.3 The 2×2, SMOKE-VERIFIED — a switch never flipped is a vacuous switch

6 seeds, boss tier, leech 0, `R2_proxy`. **Smoke, not a measurement** — 6 seeds cannot state a rate.

| `stage2b` | `f2` | in-flight steers | icearmor casts | win | dmg taken | new report keys |
|---|---|---|---|---|---|---|
| `True` | **`None`** | **72** | 1 | 0.667 | 489.1 | `inflight_steers` |
| `True` | `True` | **72** | 1 | 0.667 | 489.1 | + `wr3_f2_inflight_v1` |
| `True` | `False` | **0** | 1 | 0.333 | 641.2 | + `wr3_f2_inflight_v1` |
| `False` | **`None`** | **0** | — | 0.167 | 918.0 | *(none)* |
| `False` | `True` | **139** | — | 1.000 | 61.1 | + `wr3_f2_inflight_v1` |
| `False` | `False` | **0** | — | 0.167 | 918.0 | + `wr3_f2_inflight_v1` |

**The two `None` rows are bit-for-bit the rows they must inherit** (72/0.667/489.1 and 0/0.167/918.0
reproduce exactly). Every corner is non-vacuous. The residual keys appear on **exactly** the four
explicit rows and on neither inherit row — so no pre-existing artifact can be perturbed.

**⚑ The `(False, True)` row is the cleanest isolation of F-2 in the whole run:** no kit at all, so
the *only* difference from `(False, None)` is the steering — and damage taken goes **918.0 → 61.1**.
Direction and magnitude corroborate §5. Six seeds; routed as a measurement request, not a number.

### 1.4 ⚑ ONE OUT-OF-SCOPE REPAIR, DECLARED RATHER THAN BURIED

`--help` on the G-5 harness **raises `TypeError: %o format: an integer is required, not dict`** —
a bare `%` in `--body-separation-v2`'s help text (`80%-of-contact`), which argparse expands as an
octal conversion. **Verified present at `97d51798` by stashing my tree and re-running: it is
pre-existing, and it has been live since WR2-B**, i.e. through the whole of WR2 and WR3.

That nobody noticed is itself a finding: **the harness is driven exclusively by scripts with pinned
flag lists, never by its own help.**

I repaired it (`%` → `%%`, one character, zero effect on any fight) because **R-WR3-25(3)'s
deliverable IS a new switch, and an undiscoverable switch is not delivered.** A test now pins
`--help` rendering so the next unescaped `%` fails in CI rather than in an operator's terminal.
**If the conductor judges this outside the commission, it reverts in one character.**

---

## §2 — `prong_count` (R-WR3-25(10))

Fourth key on the telegraph record, beside the SS-S2B-7 trio. Additive; `null` on every
non-projectile telegraph; **`replica-frame/v1` stays v1**; MIGRATION §1a written.

**WHY THIS ONE IS EMITTED WHEN PER-PRONG POSITIONS WERE REFUSED — the distinction IS the warrant.**
R-WR3-23(6) refused positions because they are **derivable**. `N` is **not**: in
`prong_k(t) = origin + v·(t − t_launch)·(cos, sin)(spoke_offset + k·2π/N)` every term *except* `N`
was already on the record, and `launch_rotation_deg / N` (the spoke pitch) is carried by neither. A
consumer could only estimate `N` statistically across many crossings — a guess at a datum the
fixture holds exactly.

**Measured distribution on the 30-fight identity run** — 194 telegraph records:

| shape | `prong_count` | records |
|---|---|---|
| `circle` (nova) | **16** | 47 |
| `circle` (non-nova) | `null` | 20 |
| `rect` (wave) | `null` | 17 |
| `point` (blizzard drops) | `null` | 104 |
| `cone` | `null` | 6 |

**⚠ DRAX — IF YOU ALREADY BAKED THE TRIO, YOU HARD-CODED 16.** That was the only thing you could
have done and it is correct for *this* boss. It is **not** correct in general: **24 corpus records
DO rank-scale `projectileLaunchNumber`**, so the literal is a latent silent-wrong-render the moment
a rank-scaling nova ships. Read `prong_count`; drop the literal.

**NAMED so nobody guesses which count:** this is the **LAUNCHED** count, not
`n_realized(r, φ, offset)` (prong corridors overlapping a body at radius `r`). That is a per-target
**resolution** quantity; a telegraph is emitted **once, at cast, before any crossing exists**.
**And the gap is not marginal — it is 16 against 1:** on this fixture `n_realized` returns
**1.000 at every radius** (2/5/9/12 m) against a launched **16**, so a renderer reaching for the
resolution quantity would draw **one prong instead of sixteen**. Pinned by a test, so the
distinction cannot rot into a tautology.

---

## §3 — BYTE-IDENTITY, PROVEN NOT ASSERTED

Method: the stage-2b one — **stash the working tree, re-run, un-stash, re-run, compare.** Not
"read the diff and judge it inert." The script is **BANKED**, not left in `/tmp`, so the proof is
reproducible from the repo rather than from my session:
`simulation/notes/wr3_f2_flag_split_byteid_2026_07_30.py` (same precedent as
`e4_byte_identity_ab_2026_07_11.py`).

**30 fights, and the second half is the half that matters:** 24 UNARMED full-mix (4 tiers × 3 seeds
× 2 leech arms) **+ 6 STAGE-2b ARMED boss fights** — because the armed path is where F-2 actually
lives, and `inherit` must reproduce F-2 **ON**. Proving only the OFF side would be the weaker half
of the claim.

| digest | before (`97d51798`) | after | |
|---|---|---|---|
| mechanical fight outcomes (winner, elapsed, damage dealt/taken, kills, HP, ticks) | `6e20f7846cb07e0c` | `6e20f7846cb07e0c` | **IDENTICAL** |
| full trace record stream, `prong_count` popped | `14b08bfa6e95fffb` | `14b08bfa6e95fffb` | **IDENTICAL** |
| per-fight result dicts, compared field-by-field | — | — | **IDENTICAL** (all 30) |
| telegraph records carrying `prong_count` | **0** | **194** | the **only** difference in the stream |

The trace digest is computed with `prong_count` popped, which is exactly the additive claim made
falsifiable: **mechanically identical stream, one new key.**

**⚑ ONE HONEST CAVEAT — THE MATH NOTE PRE-REGISTERED A DIFFERENT NUMBER.** Its §3 named stage-2b's
`a0c6b5c8f6c8795f`. **I did not reproduce that value**, and I say so rather than quietly satisfying
a different predicate: it came from a session-local script that no longer exists recoverably, so
re-deriving it meant reconstructing an *instrument*, not proving a *property*. **The claim is the
weaker one** — *"this tree and `97d51798` agree under a digest defined here"*, not *"this tree
reproduces a banked constant."* What the substitution buys, and why it is not merely a retreat: the
new harness covers the **6 ARMED** fights the old digest did not, and the armed path is the
load-bearing one here — a digest over unarmed fights alone would pass while the split silently broke
every banked stage-2b figure. Recorded as math note §3.1, **amended, not substituted in place**.

---

## §4 — THE BINDING-CLASS GREP-AUDIT (R-WR3-25(7)) — READ-ONLY, NOTHING FIXED

**Shape sought:** any `char_level` / level-derived index bound to the **PLAYER's** charLevel 13
instead of the **owning monster's** own level. Surface: all WR3-touched simulation code —
`gd_boss_kit.py`, `gd_nova.py`, `gd_mitigation.py`, `gd_attack_speed.py`, `gd_monster_hp.py`,
`spatial_gauntlet/{spatial_engine,kitcal_g5_scenarios,kitcal_g5_harness}.py`.

### 4.1 TWO FURTHER INSTANCES (both arithmetically inert; neither touched)

**⚑ INSTANCE 4 — a LIVE CROSS-MODULE CONTRADICTION. `gd_nova.py:330-331`.**

> `# ── RANK 5, not rank 4 (M formulae, C composition; star-geometry §6.2). Boss `charLevel*1+3`
> #    at Matt's L13 -> boss level 16; `skillLevel7 = charLevel/4+1` -> rank 5.`

This applies the creature's own `charLevel*1+3` **directly to the player's 13**, skipping the
`lv6_hero` proxy level-variance stage. `gd_boss_kit.py:108-125`'s corrected chain
(`p_wightmire_slitha01` → `lv6_hero` → 15/16 → `charLevel*1+3`) gives **18-19**, anchored against a
measured `lifeAndMana` to 0.4 %.

**Two modules in the same seam now assert different boss levels — 16 and 18.** It is inert *today*
for exactly the reason §1.6 relied on (`charLevel/4+1` returns rank 5 across 16..19, and 16 is in
range), so no payload array moves. **But the invariance is load-bearing and undeclared at that
site**, and the next rank-scaled or level-keyed operand read through `gd_nova`'s chain gets 16.

**INSTANCE 5 — a REPORTING-layer instance. `kitcal_g5_scenarios.py:494`, emitted at `:902`.**

The boss `OppositionRow.char_level = 13` — the **player's** level — is carried verbatim into the
mob dict and therefore into every trace and report. Nothing derives from it arithmetically
(`max_hp` is M/measured off frame 281; `dmg_per_hit` is `HELD-SWEPT`), so the sim is unaffected.
**But a consumer reading `char_level: 13` off a boss row reads the player's level as the boss's.**

**A correction to my own stage-2b §1.6, which I should state plainly:** I wrote that this field is
*"a FIXTURE-WIDE key (HP derivation, escort levels)"* and deliberately not re-pointed. **The first
half is not accurate.** The grep finds **no arithmetic consumer** — `row.char_level` is referenced
in exactly one place, the metadata dict at line 902. `gd_monster_hp.gd_monster_hp(char_level=...)`
has **no caller in `src/`**. So the coupling I cited as the reason not to touch it does not exist in
the running code. The decision may still be right (banked artifacts change if the emitted value
moves) — but it should rest on the real reason, not the one I gave.

### 4.2 WHAT IS CLEAN (stated, because a silent audit is unfalsifiable)

| surface | binding | verdict |
|---|---|---|
| `WaveParams` / `BlizzardParams` / `IceArmorParams` rank-5 arrays | derived from the boss's **own** charLevel 18-19 (`skillLevel8 = charLevel/4+1`) | **CORRECT** |
| `STAGE_S2_FULL` — `armorbase05 (-91 + rank) @ 18 = -73` | the boss's own level | **CORRECT** — this is the *fix* for instance 3 |
| `gd_mitigation.py`, `gd_attack_speed.py` | **no level-derived operand at all** | **N/A** |
| escort / trash `char_level` 10-12 | derived from spawn levels, and nothing consumes them arithmetically | **CORRECT** |
| `OUTGOING_STAGE_EXEMPT_CHANNELS` | channel identity, not a level | **N/A** |

**Instance 3 (known, unchanged):** `NovaParams.tdm_additive_multiplier = 0.05` at `gd_nova.py:267,
373, 410`, composed from `armorbase05 = −78` @ cl 13. **Superseded as an operand** by SS-S2B-4 and
deliberately **not mutated** — it is the record of what Arm C ran.

**⇒ THE CLASS NOW HAS FIVE KNOWN INSTANCES ACROSS TWO SEAMS** (legolas's carried-ext wave +
blizzard arrays; our `tdm_additive_multiplier`; and instances 4 and 5 here). **Three of the five are
in our seam.** Every one of them is the same shape: an operand keyed to `charLevel` where the
`charLevel` reached for was the player's. That is no longer a defect — **it is a pattern**, and
§6(4) routes it as one.

---

## §5 — TESTS AND SUITE STATE

| item | value |
|---|---|
| New unit tests | **18** in `tests/test_wr3_f2_flag_split.py`, all passing |
| WR1 + WR2 + WR3 (`-k "wr1 or wr2 or wr3"`) | **4,000 pass, 0 fail** |
| Schema / emitter-adjacent (`-k "replica or telegraph or frame or spatial_telemetry"`) | **128 pass, 0 fail** |
| The three directly-affected WR3 files together | **94 pass** |
| Full `tests/` baseline | **NOT re-measured — see §5.1, and it says so rather than assuming** |

Written against the failure modes this change could actually have, not for coverage:

- `test_the_inflight_branch_reads_ITS_OWN_flag_not_the_kit_flag` — **the load-bearing guard.** If a
  later edit re-points the limb at `_wr3_stage2b_v1`, the flags are welded again and §5's
  attribution argument silently stops holding.
- `test_the_default_is_None_on_every_public_entry_point` — if any default ever becomes `True` or
  `False`, **this build silently made Matt's ruling for him.**
- `test_the_2x2_truth_table_…` — the commission's requested mapping, executable.
- `test_the_geometry_gate_still_dominates_the_flag` — `True` must stay inert against a uniform ring.
- `test_the_engine_resolves_the_tristate_in_exactly_one_place` — a second copy of the inheritance
  rule is the `_skill_range_covers` guard-the-guard lesson waiting to happen.
- `test_prong_count_is_the_LAUNCHED_count_not_the_realized_count` — asserts the two genuinely
  **differ** at the fixture's mid-band radius, so the distinction cannot rot into a tautology.
- `test_the_harness_help_actually_renders` — §1.4's repair, pinned.

### 5.1 Full-suite verdict

**The commission's requirement was the WR3 suites, and they pass (4,000, above).** The full
`tests/` sweep is my own addition and it was **still in flight at commit time** — the box is shared
and was running concurrent galadriel capture jobs, so the sweep is CPU-starved rather than wedged
(the log advances; it simply advances slowly).

**Stated as an expectation, explicitly NOT as a measurement:** the stage-2b baseline is **81 failing
names** (stage-2b report §9, after the 82nd was identified and fixed), and this change is
byte-identical off the new arms and adds no import to any production path, so the baseline *should*
be unmoved at 81. **I have not measured that, and I am not going to write it down as though I had.**
The partial sweep reached 55 % with **zero `FAILED`/`ERROR` lines beyond the known baseline block**.

---

## §6 — WHAT THE CONDUCTOR OWES A RULING ON

1. **⚑ THE F-2 DEFAULT — still Matt's, deliberately untouched.** The switch exists; the default did
   not move. Everything needed to rule is now separable and cheap to measure.

2. **⚑ THE BANKED ARM B WAS CONFOUNDED — my own §5 needs this correction.** Stage 2b's ablation
   (`/tmp/abl2.py`) built arm B by passing `wr3_stage2b_v1=False` **to the engine** while leaving
   the packets armed — which disarmed **F-2 *and* the icearmor tick together**. So §5's arm B is
   *"kit minus F-2 minus icearmor"*, and **the `+0.500` attributed to F-2 is an UPPER bound.** The
   new flag gives the *clean* arm B (kit + icearmor ON, F-2 OFF) for the first time. **I did not
   re-measure it** — that is a battery question and the stage-map HALT stands. The 6-seed smoke
   (§1.3) suggests the clean arm lands lower than 0.433, which would move it *further* into the
   Matt-signed band, but six seeds is not a rate and I will not present it as one.
   **REQUESTED: authorization for a 30-seed seed-matched re-run of arm B alone.**

3. **THE PRE-EXISTING `--help` BREAKAGE (§1.4).** Repaired as a task-1 blocker, declared here
   rather than buried. Reverts in one character if the conductor disagrees.

4. **⚑ THE RANK-BINDING CLASS IS A PATTERN, NOT THREE INCIDENTS (§4).** Five known instances across
   two seams, three of them ours, all the same shape. **This wants a standing check, not a fifth
   individual fix** — the cheap version is a rule that any `charLevel`-keyed operand must name the
   entity it belongs to at the site where it is composed. That is an engineering-discipline
   question (jack-ryan) as much as a simulation one.

5. **THE TWO NEW INSTANCES ARE UNFIXED BY INSTRUCTION (§4.1).** Instance 4 leaves two modules
   asserting different boss levels (16 vs 18) — inert only because rank 5 is invariant over 16..19,
   and that invariance is **undeclared at the `gd_nova` site**. Instance 5 emits the player's level
   as the boss's into every artifact. Both are one-line repairs whenever the conductor wants them.

6. **MY §1.6 SENTENCE WAS INACCURATE (§4.1)** — I justified leaving `OppositionRow.char_level = 13`
   by a fixture-wide coupling that the grep says does not exist. The decision may survive on the
   banked-artifact argument; the stated reason does not.

---

## §7 — REPRODUCTION

```bash
cd ~/Games/reincarnated-engine && export PYTHONPATH=src
python3 -m pytest tests/test_wr3_f2_flag_split.py -q -p no:randomly            # 18 pass
python3 -m pytest tests/ -q -p no:randomly -k "wr1 or wr2 or wr3"              # 4,000 pass
# byte identity — run, stash, run, compare (Discipline #11: method, not intention)
B=src/reincarnated/simulation/notes/wr3_f2_flag_split_byteid_2026_07_30.py   # BANKED, not /tmp
python3 $B /tmp/f2_after.json
git stash push -- src/reincarnated/simulation/spatial_gauntlet/{spatial_engine,spatial_telemetry,replica_frame_emitter,kitcal_g5_harness}.py
python3 $B /tmp/f2_before.json && git stash pop
# the new arms
… --wr3-stage2b-v1 --wr3-f2-inflight off     # clean arm B  -> label `_s2bv1_f2off`
… --wr3-f2-inflight on                       # F-2 alone    -> label `_f2on`
```

**Nothing was written to any banked artifact root.** No battery ran. No calibration ran. No arm
default moved. The stage-map HALT stands at `S0_NONE`.

---

*WR3-KITE-COMMIT F-2 flag split + `prong_count` + binding-class audit — gamora, simulation seam,
2026-07-30. Neither repo pushed.*
