# WR3-KITE-COMMIT — STAGE-2c REPORT (gamora, simulation seam)

> **Provenance:** authored by the gamora stage-2c relaunch agent 2026-07-30; the agent's harness
> blocked `.md` writes, so the conductor (gandalf) banked this text VERBATIM from the agent's
> return. Verified against the engine tree before banking: commits present, artifact JSON
> reproduces §8/§9 headline figures (S0 0.733 / S1 0.900 / S2 0.967, duration 34.75 s,
> leech-scope legs identical), code sites spot-checked (`family` in spatial_telemetry,
> `lifesteal_scope` door, `_wr3_icearmor` mirror sites). Ruling: R-WR3-35.

**Commits (engine, `~/Games/reincarnated-engine`, NOT pushed at authoring time):** `f1039b3a` · `b20f1b9a` · `c3887bd3`
**Math note:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/wr3-stage2c-2026-07-30.md` (471 lines §1–§9 by the stopped predecessor + §10 for R-WR3-34 by me; written BEFORE code in both cases)
**Cell:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/wr3_cell_s2c_2026_07_30.py`
**Artifact:** `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5/wr3_stage2c/wr3_stage2c.json`
**Tests:** `/Users/admin/Games/reincarnated-engine/tests/test_wr3_stage2c.py` (33)

## §0 Predecessor-work disposition — **ABSORBED**

The stopped instance left uncommitted: a 331-line addition to `gd_boss_kit.py` (item (i) only) and an **untracked** 471-line math note covering all of items (i)–(viii). Nothing was committed, consistent with R-WR3-34(5).

**Absorbed on evidence, not on label.** Before accepting I executed it: the operator reproduces all four Matt-signed pins to 0.01 (nova mid 81.27 / far 113.78 / wave 85.12 / blizzard 44.28) and the T11 flip runs in both branches. Landed as `f1039b3a` with a 12-test smoke; full sweep on it returned **81 names, name-diff 0/0**.

## §1 Arm wiring + the flip-not-rebuild demonstration

Operator, flag-parameterised, per R-WR3-33(1):

```
outgoing = base × (1 + Σpool(charLevel)/100) × (1 + pak[difficulty,players]/100) × (1 + veteran/100)
```

| cell | Σpool | pak | veteran | total_factor | phys rider |
|---|---|---|---|---|---|
| **CELL_OF_RECORD** cl13/r4 | −70 | −25 | own +40 | **0.3150** | **1.166** |
| **CELL_SHIPPED** cl18/r5 | −65 | −25 | — | **0.2625** | **1.060** |
| cl13/r4 POOLED | −30 | −25 | pooled | 0.5250 | 1.160 |

**SS-S2C-1:** `STAGE_S2_FULL`'s 0.2625 is no longer a literal — it is what the operator returns, and `assert_stage_literals_agree_with_operator()` is that claim executable.

**The flip (R-WR3-33(3)), one enum value:**
```
VETERAN_COMPOSITION_OF_RECORD = own_stage → ratio 0.9554 → |1−r| ≤ 0.05 → STAGE_S2_FULL, 0.2625
                              = pooled    → ratio 1.5911 → |1−r| > 0.05 → rebased,       0.4177
```
1.5911 reproduces R-WR3-32(4)'s ×1.58–2.19 band at its cl-13/r4 end. No mechanism, resolver, packet or scheduler moves. A test performs the flip and asserts both branches.

### ⚑ CORRECTION OWED TO R-WR3-33(2)'s CAVEAT

| channel | rank-4 array | **cell of record** | rank-5 array | **shipped** | ratio |
|---|---|---|---|---|---|
| nova prong, mid | 118/200 | **81.27** | 148/247 | 83.73 | 0.9706 |
| nova prong, far ×1.40 | | **113.78** | | 117.22 | 0.9706 |
| wave impact | 122/210 | **85.12** | 153/272 | 91.37 | **0.9316** |
| blizzard per drop | 58/111 | **44.28** | 76/137 | 45.93 | 0.9641 |

mean 0.9554 · dispersion **4.19 %** · worst channel **6.84 % low**.

**"Within 5 %" is a statement about DISPERSION and about the MEAN. It is FALSE per-channel:** the wave is 6.84 % low here and legolas's full grid bottoms at 9.1 %. The substitution is a uniform ≈0.955× rescaling with ±2 % wobble — a better object than the caveat as written, but **a reader taking "within 5 %" as a per-channel bound mis-prices the wave by two points.** A test pins the correction.

## §2 Leech scope-mapping — **P-2 HOLDS, against R-WR3-31(4)**

**Mapping implemented:** `lifesteal_scope` as a closed-set door field (`all_damage` default / `attack_only`), with attack eligibility carried as a **positive per-skill marker** (`leech_eligible`) rather than inferred from which HP-decrement site a mechanism was written at. Unknown value **raises** at the door (`_coerce_lifesteal_scope`, on `_coerce_mitigation_law`'s argument).

The DoT's exclusion is **structural, not marked**: GD's ADCtH excludes damage-over-time, and the bleed reaches HP at a site carrying no leech term at all.

**Measured effect (30 seeds, arm of record, leech 0.05):**

| leg | H1 | intake | healed |
|---|---|---|---|
| `all_damage` | 0.967 | 426.6 | 10807.3 |
| `attack_only` | **0.967** | **426.6** | **10807.3** |
| leech 0.00 control | 0.900 | 399.8 | 0 |

Identical H1, intake, healing, and **per-seed win vector**. `scope_is_measured_noop: True`.

**R-WR3-31(4) expected this to be load-bearing. It is not.** The sim's leech channel was already attack-only for this fixture. The 0.733 was never a scope artifact — it is the `S0_NONE` arm's own value, which §A reproduces exactly. Built anyway because an *asserted* no-op and a *measured* no-op are different objects, and because the aura pulse and Wave-C mark burst are both in-tree and leech-free **by accident, not by declaration**.

**G-LEECH:** healed/capacity = 0.5766 — the ring's capacity is ≈1.9× what the pool can absorb.

## §3 F-2 cap — **P-3 FALSIFIED BY SIGN**

**Cap chosen:** structural clamp `F2_INFLIGHT_MAX_CORRECTIONS_PER_RING = 1` (derived — it is the count a corrective read has). **Both floats ship at ZERO** (`EXTRA_LATENCY_S`, `MISS_RATE`): there is no measured referent in-flight escape rate anywhere in the ledger, and R-WR3-23(5) ratified that a number that will not reproduce is not a calibration. The miss-rate has its own RNG sub-stream that **draws nothing at 0.0**, so an armed cap consumes the stream identically to an unarmed one.

**Priced in the CLEAN regime (S0_NONE, leech 0.00, 30 seeds) so the denominator is ΔF2 = +0.467:**

| leg | H1 | intake | duration | steers | rings | reads/ring |
|---|---|---|---|---|---|---|
| F-2 OFF | 0.467 | 608.5 | 24.1 s | 0 | 50 | 0.00 |
| F-2 ON uncapped | 0.933 | 301.0 | 35.5 s | 331 | 68 | **4.87** |
| F-2 ON **CAPPED** | **0.167** | 724.1 | 17.7 s | 39 | 39 | **1.00** |

ΔF2 uncapped measured **+0.4667** — reproduces the banked +0.467. **Δ capped = −0.300, i.e. −0.64× of ΔF2.**

**P-3 predicted [0.5, 0.9]. Measured −0.64. Falsified by sign, not magnitude.** The clamp works exactly as designed (4.87 → 1.00 reads/ring) and the result is a **third, worse regime**: one corrective read is worse than zero. The player commits to a bearing on the first read and can no longer revise it; duration collapses 35.5 → 17.7 s and intake rises 301 → 724. **The in-flight verb's value is in the RE-solving, so a clamp does not attenuate it — it inverts it.** The cap is built, measured and **NOT shipped** (`wr3_f2_cap_v1` defaults False). Routed as a fork in §10.

`G_F2_capped_predicate` (steers ≤ rings) **PASS at equality**, 39 ≤ 39.

## §4 Melee graduation — ONE declared unit system, and it exposes a **channel** error

`BOSS_DMG_SWEEP (33.0, 50.0, 67.0) → (43.1, 52.0, 60.8)`, `dmg_grade` HELD-SWEPT → **M-BAND**, boss row only; escorts stay D-HELD.

**Declared unit system: POST-MITIGATION, R2_proxy, MEASURED off the fight** — not computed from `gd_taken_physical`, because **the melee channel does not call it.**

⚑ The math note §4.2 declared "physical only (the boss melee is physical)". **Measured FALSE:** `OppositionRow(element="cold", cold_rider=0.0)` — our boss melee is **100 % COLD**.

| pre-mit (the tuple) | our post-mit (MEASURED) | referent post-mit (cl18/r5 no-Vet) | ratio |
|---|---|---|---|
| 43.1 | **32.397** | 17.13 | **1.89× over** |
| 52.0 | **39.087** | 22.52 | **1.74× over** |
| 60.8 | **45.701** | 27.90 | **1.64× over** |

(uniform ×0.7517; second target band cl13/r4 own = 16.59–27.07)

**Decomposition of the gap — the magnitudes were right and hiding a channel error:**
- referent 43.1 pre-mit = **35.60 physical (83 %)** + 7.50 cold (17 %)
- referent 60.8 pre-mit = **43.55 physical (72 %)** + 17.25 cold (28 %)
- legolas's own model on a 100 %-cold 43.1 gives 37.07 vs her 17.13 → **the SPLIT carries 2.16×**
- our engine on the same 43.1 gives 32.40 → our mitigation carries 0.87×, the *other* way

**The dominant term is the channel split, not the magnitude and not the mitigation model.** R-WR3-32(7b) asked for a unit fix; performing it revealed that graduating the magnitude alone moves the fixture *further* from the referent in the units every pin is quoted in. **Fork in §10** — re-splitting the boss melee is a fixture change no ruling covers.

**`BOSS_DMG_DEFAULT` deliberately NOT moved** (50.0). R-WR3-33(4)(iv) rules the SWEEP and is silent on the DEFAULT; 50.0 lies inside the graduated band, and moving it to the midpoint 52.0 would re-base every banked figure on a ruling nobody made. **Ruling owed.**

## §5 Icearmor — kill-switch, the two measurements, and the emission mirror

**(v) Kill-switch at the PACKET** (`wr3_icearmor_enabled`, default True = byte-identical). The engine flag gated only the tick; the cast is packet-driven, so disarming the flag made the buff **permanent**. `absent-with-kit` is reachable for the first time. `_wr3_special_indices` re-index asserted (`[1,2,3,4]` → `[1,2,3]`, melee keeps index 0).

**THE DECOMPOSITION (clean regime, 30 seeds) — and R-WR3-25(4)'s Δkit INVERTS:**

| arm | H1 | derived |
|---|---|---|
| A no kit at all | 0.567 | — |
| B kit, icearmor **ABSENT** (NEW) | **0.667** | **TRUE Δkit = +0.100** |
| B kit, icearmor CYCLING | 0.467 | **icearmor-alone = −0.200** |
| B\* kit, icearmor PERMANENT (banked) | 0.433 | cycling→permanent = −0.034 |

telescope: 0.567 + 0.100 − 0.200 = **0.467**, exactly the clean arm B.

```
R-WR3-25(4) banked "Δkit" (confounded with PERMANENT icearmor)  −0.134
TRUE Δkit (icearmor genuinely absent)                           +0.100   ← SIGN FLIP
```

**The kit minus icearmor is PLAYER-ward. Every boss-ward point attributed to "the kit" was icearmor's**, and it took a packet-level switch to see it. **P-5 falsified by magnitude**: sign (boss-ward) correct, |Δ| = 0.200 against a predicted ≤ 0.10. R-WR3-25(5)'s rank-2 promotion is **supported and then some** — icearmor is the single largest boss-ward term measured.

**G-IA0:** `icearmor_casts == 0` on the kill-switch arm as a **measured zero**, not an absence. PASS.

**(ix) Emission mirror (SS-S2C-9).** Confirmed the defect empirically first: boss `combatant_state.active_effects` was **empty (len 0)** while the buff was live. Now routed:

```
active_effects → ActiveEffect(name="wr3_icearmor", duration_remaining=11.9, params={
  damage_taken_multiplier 0.75, cold_damage_multiplier 1.28, attack_speed_multiplier 1.35,
  absorb_pct 25.0, cold_damage_pct 28.0, attack_speed_pct 35.0,
  authority: "mirror_of_IceArmorState; read-only; IceArmorState owns the timer" })
```

**A MIRROR, not a migration, and the direction of authority is declared.** `active_effects` is a live mechanism surface — the resolver iterates it and decrements `duration_remaining`. Migrating would put a second clock beside `IceArmorState.remaining_s`, and **two writers of one quantity is exactly how the permanent-icearmor confound happened.** One writer; `duration_remaining` written from `remaining_s`, never read back. Name namespaced away from the dispatcher's 26 names (which carry no `else` — the silent no-op that cost the charge bleed three batteries). Mirrored at tick **and** at cast, so the permanent regime emits too.

## §6 Residual keys + instance-5

**(vi) SS-S2C-7.** Nine counters + the flag's own value emitted whenever the caller is a WR3 arm: `None` = UNMEASURED, `0` = MEASURED ZERO, **absent = forbidden**. Plus `f2_rings_launched` (G-F2's denominator) and `wr3_f2_cap_v1`.

**Self-caught defect:** my first cut counted `f2_rings_launched` inside the F-2 branch and it read 0 on F-2-OFF arms while rings were plainly launching — reproducing, in the very commit that generalises the residual-key rule, the confusion that rule exists to kill. Caught by the smoke, fixed, pinned by a test.

**(vii) Instance-5 — BYTE-INERTNESS PROVEN, NOT ASSERTED.** `OppositionRow.char_level = 13` (the **player's**) → `PRIMORDIAN_CHAR_LEVEL` (18, the monster's own, and the level the rank-5 arrays are transcribed at). Every other row already bound its own (escorts 10/11, trash 12, champions 11, hero 10).

Digest over **30 armed fights**, char_level 13 vs 18:
```
MECHANICAL digest  c00230bfae3b3137…  ==  c00230bfae3b3137…   → byte-inert TRUE
ARTIFACT   digest  82d703b4be0a5784…  !=  4d02accd191c8fd2…   → metadata moved (expected)
```
Exactly what SS-S2C-8 declared: a re-labelling, not a numeric correction — the fight never read the field. `_kc1_meta` now carries `char_level_owner: "monster"` + the cell-of-record declaration.

**Whole-build byte-inertness:** clean-ablation **PREDICATE R PASS** — all nine banked arm × leech cells reproduce **to the last digit** from the post-2c tree.

## §7 Telegraph `family` (x), the audit, `attack_id` (xi), MIGRATION

**`family: "nova"|"blizzard"|"wave"|"melee"`** on `TelegraphSpec`, additive, `None` default, validated (non-None outside the set raises). Wired on all three emitters — including the wave, whose `rect` is currently unambiguous, because **a discriminator only some members carry is not a discriminator**.

### ⚑ VERDICT-INTEGRITY AUDIT — the answer is NOT the feared one

| site | keys on | conflates? | banked figures suspect? |
|---|---|---|---|
| `wr2_cell_bat:249` escape-rate **firing selector** | `NOVA_ATTACK_ID_FRAGMENT in attack_id` | **NO** | **NO** |
| `wr2_cell_bat:253` `circle_non_nova` completeness counter | unqualified `shape == "circle"` | counts, does not score | NO — but **cried wolf** |
| `wr3_cell_kc:669` `g4_damage_substrate` | unqualified `geometry == "circle"` on **damage** events | **YES** | NO — **latent** |

**The escape-rate statistic the run is graded on is NOT scored by shape.** It is keyed on the nova's own minted `attack_id`, which a blizzard drop cannot carry. **NO stage-2b escape figure is suspect.** The conflation R-WR3-34(2) feared is **playback-only** (drax's consumer); the engine scorer never had it. The `family` key still lands for the baton.

**One REAL engine-side defect found, in a different instrument than the ruling named.** `g4_damage_substrate` recovers the nova's payload-grain set from boss damage events with `geometry == "circle"` — and the blizzard emits *exactly that label* (`spatial_engine:6441` vs the nova's `:6150`). Under an armed packet its 24 drops would score into the nova's grain set, corrupting `distinct_delivered_hp`, `worst_drop_abs` and `anchor_grain_207_40_present`.

**Latent, not realised** — G4 ran at stage 1 (`a6c6bcf9`) before the blizzard landed (`97d51798`). It would corrupt the *next* run, not the last one. That is a narrower claim than "the numbers are fine" and it is the one the evidence supports. Repaired before the battery, qualified on `attack_id` (stronger than `family` here — `family` lives on the telegraph, this reads damage events), and the repair now **reports its own selectivity** via `conflation_guard`.

**(xi) `attack_id`** on damage/dot events, forwarded from `ring.attack_id` / `ev.attack_id` / `drop.drop_id` — never minted at the emitter. Not new information: it was minted upstream and **dropped at the emission boundary**. Same defect shape as (ix) and (x): *the discriminator existed and was lost at the seam.* Three instances in one commission — named as a pattern.

**Its value demonstrated immediately:** the G-N3″ measurement below could only separate blizzard from nova *because of* the new join key.

### MIGRATION note (ADR-004) — star-lord emission seam + drax consumer

All additive; `replica-frame/v1` stays `v1`; no schema bump.

1. **`TelegraphSpec.family`** — `str|None` ∈ {nova, blizzard, wave, melee}. `None` on every pre-2c and every non-declaring telegraph. **Consumers MUST carry a default arm** (drax D-F4): fifth value-set growth in five runs on this schema. **Any consumer testing `shape == "circle"` to identify the nova is wrong and must switch to `family` or `attack_id`.**
2. **`damage` / `dot` events gain `attack_id`** — `str|None`. Null on every hit with no minted id (the whole generic per-skill path) — honest "belongs to no scheduled attack", not a fabricated id. Enables exact telegraph↔hit joins.
3. **Boss `active_effects` becomes non-empty** on armed WR3 fights, carrying `wr3_icearmor` with six multiplier params. Any instrument reading `len(active_effects)` as "number of ailments" now sees one more object. It is a **read-only mirror**; `IceArmorState` owns the timer.
4. **Result-dict counter block is now tri-state-gated.** `wr3_stage2b_v1=None` (production default) → block absent, dict shape unchanged. `True`/`False` → ten keys present, `None`=unmeasured / `0`=measured-zero. **Consumers must not use `dict.get(k, 0)` or `or 0` on these** — that is the defect this fixes.
5. **`_calibration_overrides` gains `lifesteal_scope`** (closed set, raises on unknown).

## §8 Gate re-registration (stage-2c params, 30 seeds, arm of record)

| gate | band / predicate | measured | verdict |
|---|---|---|---|
| **H1** boss win rate | [0.40, 0.60] (Matt-signed) | **0.967** | **FAIL — above.** P-0 pre-registered |
| **G-T′** mean boss duration | [59, 118] s | **34.75 s** | **FAIL — below.** Pre-existing: S0_NONE is 30.4 s, so not a 2c regression |
| **G-W1** wave hit rate | [0.05, 0.45] | 13/74 = **0.176** | PASS |
| **G-B1** blizzard drops/cast | [0.0, 0.9] | 26/59 = **0.441** | PASS |
| **G-B2** blizzard slows | > 0 | **26** | PASS |
| **G-I1** icearmor uptime | [0.30, 0.42] | 3630/10395 = **0.349** | PASS |
| **G-F2** steers | > 0 on an F-2-**armed** arm | 0 on the battery arm (F-2 OFF, **fails BY DESIGN** per R-WR3-26(6)); 331/68 armed | PASS on armed |
| **G-F2′** capped | steers ≤ rings launched | **39 ≤ 39** | PASS (equality = the clamp) |
| **G-N3″** worst received event | ≤ arm ceiling; ≤ A-DMG-1 260.50 | **91.369** | PASS |
| **G-LEECH** *(NEW)* | scope is a measured no-op | **TRUE**, byte-identical | PASS |
| **G-IA0** *(NEW)* | `icearmor_casts == 0` measured zero | **TRUE** | PASS |
| **G-BYTE** | flag-OFF digests reproduce | PREDICATE R **PASS**, 9/9 cells to last digit | PASS |

**G-N3″ by family** (only separable because of the new `attack_id`):

| family | realized worst | computed | agreement |
|---|---|---|---|
| wave | **91.369** | shipped 91.37 | **exact** |
| blizzard | **45.932** | shipped 45.93 | **exact** |
| nova | 68.115 | mid 83.73 (far band not reached) | under |
| melee | 50.995 | — | — |

**The operator's computed pins reproduce the fight's realized damage to three decimals.** That is the strongest available cross-validation of §1.

## §9 Battery of record — R-WR3-15's debt DISCHARGED

**Arm:** S2_FULL × Veteran own-stage (×1.40) · cell of record cl13/r4, fixture cl18/r5 as the ruled approximation (mean ratio 0.955, **wave residual 6.8 %**) · leech 0.05 `attack_only` · F-2 OFF · icearmor cycling · `boss_dmg_per_hit` 50.0 · R2_proxy · 30 seeds, `BASE_SEED 74000800+i`.

```
H1 = 0.967   vs Matt-signed [0.40, 0.60]   → FAIL, ABOVE BAND
intake 426.6 = 56.2 % of the 759 pool · duration 34.75 s
per-seed wins: 29 of 30 (single loss on seed +2)
```

**P-0, pre-registered before the build, HOLDS.** The arm of record puts the win rate above band and no authorized stage-2c lever brings it back:

| lever | swept | effect on H1 | verdict |
|---|---|---|---|
| arm | S0 0.733 → S1 0.900 → **S2 0.967** | the arm *raises* it | — |
| leech scope | all_damage ↔ attack_only | **0.000** | inert (P-2) |
| leech depth | 0.05 → 0.00 | −0.067 | insufficient |
| F-2 cap | OFF → capped | **wrong direction** — F-2 is already OFF on this arm | cannot help |
| melee | 43.1 → 60.8 | intake +16 % on a 41 % increase; self-limiting vs a kiting policy | inert |

**R-WR3-15's debt is a debt to a MEASUREMENT, not to a pass.** It is discharged.

**Full-regression name-diff sweep, confirming, on `c3887bd3`: 60F / 9896P / 21E = 81 names. Name-diff 0/0 — EXACT MATCH to the 81-name baseline.**

Sweep history this commission — three sweeps, and the middle one earned its runtime:
- `f1039b3a` → 81 names, 0/0
- `b20f1b9a` → **139 names, +58**. Diagnosed below.
- `c3887bd3` → **81 names, 0/0**

### What the middle sweep caught (all in `c3887bd3`)

**One real regression I shipped.** The widening emitted unconditionally and **moved the production combat digest** — `_combat_digest` hashes the aggregate dict, so *dict shape alone* breaks byte-identity. `spatial_engine`'s own WR2-D comment records that exact lesson four inches above the code I wrote. Repaired by making `run_spatial_fight(wr3_stage2b_v1)` a **tri-state** on R-WR3-25(3)'s precedent: `None` = caller never heard of WR3 → production dict untouched; `True`/`False` = a WR3 arm, entitled to three-valued counters. All four production digests restored.

**Two real defects the widening surfaced,** both silently scoring unmeasured as zero:
1. `kitcal_g5_harness` read `int(result.get("wave_casts", 0))` for all nine counters — the `get(k) or 0` hazard **inside the harness that writes the battery report**. Every non-stage-2b G-5 fight has been recording measured zeros for quantities it never measured. The widening converted it into a loud `int(None)` TypeError. Repaired with `_wr3_opt_int` (which contains no `or 0` anywhere).
2. `wr3_cell_cleanabl` guarded on `if k in r:` — correct under the old convention, wrong under the new — so the convention change reproduced the hazard *inside the cell written to avoid it*. Guard moved to the value.

**Two false positives I caused with comments — I moved the comments, not the tests.** Two source-scanning tests locate code by literal text; my comments quoted the literals, one of them shifting an `index()` window onto the comment. A containment test is not worth loosening for a comment.

**Four declared allow-list entries,** each argued at its own site: `lifesteal_scope` into BQ-3's closed `ALL_OVERRIDE_FIELDS` (third time that set has earned an entry); the 2c cell into `_DOOR_ALLOW_LIST`; `BOSS_DMG_SWEEP`'s graduation; and the three absent-not-zero tests inverted to present-and-None with the old convention kept in their docstrings.

**Re-verified after repair, not assumed:** PREDICATE R PASS, and the 2c cell re-run returned **every figure identical, digit for digit**.

## §10 Rulings owed / forks HALTed

1. **THE BAND FORK (§9) — Matt's.** Referent-parity on the boss's outgoing damage and R-WR3-17's [0.40, 0.60] are in **measured conflict**, and no authorized stage-2c lever bridges them. The levers that could all sit outside this commission: player pool (759 vs 1600), player DPS, boss HP/duration (G-T′ also fails, *below*, at 34.75 s vs [59,118]), and the ring itself (Matt-ruled at 0.05). **Calibration thread HALTED; the build and the battery completed, as pre-registered.**
2. **THE F-2 CAP INVERTS (§3).** The structural clamp does not produce a capped-imperfect F-2 between OFF and ON — it produces a **third, worse regime** (−0.64× of ΔF2). Selecting it would be an unruled balance intervention. **Built, measured, NOT shipped.** Matt's Fork-3 (c) presumed attenuation; the mechanism does not attenuate. Needs a re-ruling on what "imperfect F-2" should mean.
3. **THE BOSS MELEE'S CHANNEL COMPOSITION (§4).** The unit fix exposed that our melee is 100 % cold against a referent that is 72–83 % physical, putting us **1.64–1.89× over** the referent's post-mitigation band at the *same* pre-mitigation magnitudes. Re-splitting the row is a fixture change no ruling covers. **HALTED, not improvised.**
4. **`BOSS_DMG_DEFAULT` (§4).** The sweep is ruled; the default is not. Left inert at 50.0 (inside the band). Ruling owed before any battery treats 52.0 as canonical.
5. **THE ≤5 % CAVEAT UNDER-STATES THE WAVE (§1).** Dispersion 4.19 %, per-channel deviation 6.84 % here and 9.1 % in legolas's full grid.
6. **R-WR3-25(4)'s Δkit HEADLINE IS WRONG IN SIGN (§5).** −0.134 → **+0.100**. Charter correction owed. R-WR3-25(5)'s icearmor rank-2 promotion is over-supported: icearmor-alone is −0.200, double P-5's bound.
7. **P-5 falsified by magnitude; P-3 falsified by sign.** Both pre-registered before the build.
8. **The "discriminator lost at the seam" pattern (§7)** — three instances in one commission (icearmor state, telegraph family, attack_id). Routes to jack-ryan as a discipline candidate.
9. **Veteran terms not priced (OA/DA/speed/str, U-V4)** all bias our boss *weaker* than the referent's. Bias, not conservatism.

### Key file paths

- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/gd_boss_kit.py` — operator, cells, degeneracy, `stage_of_record()`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` — leech scope, F-2 cap, icearmor mirror, residual keys, telegraph families
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_scenarios.py` — melee graduation, instance-5, icearmor packet switch, leech markers
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_telemetry.py` — `family`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/replica_frame_emitter.py` — `attack_id`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/calibration_overrides.py` — `lifesteal_scope` door
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/wr3_cell_s2c_2026_07_30.py` — the measurement cell
