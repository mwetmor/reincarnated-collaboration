# KC2-PM4 · I-2 — landing note: the board hardens ×1.67 and the fight gets FASTER

> **Run:** KC2-PM4 (replicate waves 150–160 faithfully) · **Iteration:** I-2, pet-life fold + pet
> wire observability · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Author:** gamora (simulation
> seam) · **Date:** 2026-08-13
> **Charter:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md` (ledger **L-3**)
> **Substrate:** legolas Lap E — `agentic_orchestration/legolas/notes/2026-08-13-kc2-pm4-lap-e-pet-life/`
> **Math note (Discipline #1, written BEFORE the code, with twelve pre-registered numeric predictions):**
> `reincarnated-engine/src/reincarnated/simulation/math/kc2-pm4-i2-pet-life-fold-2026-08-13.md`
> **Status:** COMPLETE. Assert wall **27/27**, determinism ×2 **EXACT** on all three cells at BOTH
> layers, gate wall **66/66** on each of three batons at **FULL**, all **17** batons re-gate green.
> **No HALT was hit. No constant was tuned.**

---

## 0 — The one-paragraph answer

**I predicted this fold would push the fight past T2's ceiling. It did the opposite: the reference
cell went 190.61 s → 186.12 s against the measured 186 s — a +0.06 % miss on a band that allows
±15 % — while the board it fights hardened ×1.67.** Nine of my twelve pre-registered predictions
are wrong, and every one of them is wrong the same way. **The mechanism, measured not inferred:
contact ticks moved 868 → 864 (−0.5 %) while rows-per-contact-tick moved 2.99 → 4.76 (+59 %).**
`disc.resolve_tick` is uncapped multi-target and the hit test is a **point** (`entity_radius_m =
None`, M-5), so a harder crowd is a *denser* crowd and the player's throughput scales with it.
**At I-1 my error was pricing sustain and never pricing exposure. Here it is the same error one
level up: I priced the eHP term and never priced the co-residence term.** § 5 is the reading that
matters — **8.3 % of this cell's kill work now happens on ticks carrying ≥ 36 bodies inside a 3.0 m
disc, which is above the hexagonal-packing ceiling for half-metre bodies. At I-1 that figure was
1.4 %.** That is the largest remaining measured divergence and it is not the limb I was sent to fold.

---

## 1 — What landed

| # | artifact | where | commit |
|---|---|---|---|
| 1 | **math note** (before the code, twelve pre-registered predictions) | `simulation/math/kc2-pm4-i2-pet-life-fold-2026-08-13.md` | `0aba5839` |
| 2 | **pet eHP fold** — loader, per-wave index, limb-by-column, basis map, coverage, retired-instrument label | `simulation/kc2/monster_stats.py` | `0aba5839` |
| 3 | **consumption + lifecycle recording + the pets surface** | `simulation/kc2/run.py` | `0aba5839` |
| 4 | **`PetActor` model + `Wave.pets` (additive, defaulted)** | `export/baton_v1_schema.py` | `0aba5839` |
| 5 | **pet second-times DERIVED from run-wide ticks** | `export/baton_v1_emitter.py` | `0aba5839` |
| 6 | **`pet_ehp` spec field · 3 specs · `waves[].pets[]` emission · 6 declaration rows · 1 superseded row** | `export/kc2_run_adapter.py` | `0aba5839` |
| 7 | **driver + assert wall (27) + determinism + pet forensics + split T4 scorecard** | `simulation/scripts/gamora_kc2_pm4_i2_pet_life_fold_2026_08_13.py` | `0aba5839` |
| 8 | **vendored substrate**, byte-identical, SHA-pinned | `data/kc2/pm4_pet_ehp_by_wave.csv` | `0aba5839` |
| 9 | **MIGRATION ×2** | `simulation/MIGRATION.md`, `export/MIGRATION.md` | `0aba5839` |
| 10 | **3 batons + 3 knots supplies + findings** | `src/reincarnated/output/`, `simulation/output/` | `1128a055` |

Engine `e6f3b2c6 → 1128a055`, **PUSHED**.

### ★ THE THREE SIBLING BATONS — FULL grade, 66/66 each, clean code surface at `0aba5839`

| cell | file (`src/reincarnated/output/`) | sha256 |
|---|---|---|
| CAMP / DEF-OFF (control) | `kc2-baton-v1-…-pm4-i2-camp-defoff-20260813_061907.json` | `6cbd4150c74046d9a4f254871c0f135e54c52ab7eb2abe541468a1e2ccaf2418` |
| CLUSTER / DEF-OFF (isolation) | `…-pm4-i2-cluster-defoff-20260813_061909.json` | `9767f920762c4f210bb5aab328b45e4904d1b2f9d0a39d16b95872ec7522661b` |
| **CLUSTER / DEF-ON** ← reference | `…-pm4-i2-cluster-defon-20260813_061912.json` | `355ddfd7bd44afdaedfac297205a296cf8fdb1fff9ea5efaf58deecc24936531` |

Knots supplies (`simulation/output/`, stamp `20260813_055638`): `49d64796…` / `30fa1713…` /
`f993b072…`; findings `kc2-pm4-i2-findings-20260813_055638.json` `9236e17de25c30af…`.

**All fourteen prior batons** verified from bytes, read read-only, **never written**, and all
**re-gate green** (33/33 stub + 32/32 validator) carrying `pets: []`. **17 of 17 green.**

**Substrate, digest-verified before load (GL-6), FULL hash not a prefix:**
`pm4_pet_ehp_by_wave.csv` = `35d82158c809a6b61af4e04b153da054589813901eb113b49389146be73ee6f4`
(the charter's pin, EXACT) · plus I-1's two, both EXACT. Vendored **byte-identical** (`cmp` clean).
The other three Lap-E CSVs were **not** vendored: this fold does not read them, and carrying a file
nothing loads is how a superseded board re-enters (the D-7 rule).

---

## 2 — Determinism ×2 (charter law, FG-10), at BOTH layers

**SIM layer** — each cell replayed twice, full emitted surface deep-compared:

| cell | masked surface digest | leaves | differences | verdict |
|---|---|---:|---:|---|
| CAMP/DEF-OFF | `b6f279dc8ba73b42…` | 418,835 | 0 | **EXACT** |
| CLUSTER/DEF-OFF | `4d54e75d0ecd7882…` | 374,953 | 0 | **EXACT** |
| CLUSTER/DEF-ON | `b846f73b0f7d1126…` | 342,920 | 0 | **EXACT** |

**BATON layer** — masked with the emitter's own `PROVENANCE_VOLATILE_KEYS` (imported, not
restated): **A ≡ B EXACT on all three cells** (`09e9bcb9538ed20c…` / `9a14edb0151b2ca9…` /
`d565e24bbe9db4c6…`).

### The known-defect gap, and it is confined to exactly the flagged key

The masked compare of a freshly-built wire against the **on-disk** record shows **exactly one**
difference per cell, and it is `sim_pin.tree_state_untracked_entries_excluded` (2705 vs
2701/2702/2703) — the untracked-file count that moves because writing the next sibling baton
increments it. **Nothing else differs on any cell.** The charter's instruction was to treat a diff
confined to that key as the known defect and anything else as a failure: **it is confined.**
**Still not repaired here** — re-ruling a countersigned mask from the simulation seam is the line
PM-3 held on `F5-I-DEFENSES`. **Star-lord's.**

---

## 3 — ⚑ THE MATRIX, vs the MEASURED reference truth

> **Reference truth, MEASURED (Lap C, charter Law 4): Matt DIED ON WAVE 160.** Ten waves in
> **186 s** (682 → 868 s), per-wave 14 / 17 / 29 s min/med/max, sharp slowdown on the last two.

| cell | ticks | time of death | **wave** | cleared | kills | pets | N_eff | intake | leech offered | healed | mean HP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CAMP / DEF-OFF | 9,881 | 806.61 s | **160** | 9 | 751 | 626 | 5.57 | 387,469 | 48,851,967 | 366,778 | 99.1 % |
| CLUSTER / DEF-OFF | 2,312 | **188.73 s** | **160** | 9 | 771 | 623 | 4.94 | 378,644 | 48,416,984 | 358,064 | 96.2 % |
| **CLUSTER / DEF-ON** ← reference | 2,280 | **186.12 s** | **160** | 9 | 767 | 620 | 4.76 | 376,483 | 47,963,839 | 356,212 | 96.1 % |

**vs the I-1 baseline (`…-pm4-i1-cluster-defon`, `59da5739…`), same cell:**

| quantity | I-1 | I-2 | Δ |
|---|---:|---:|---:|
| **death wave** | **160** | **160** | 0 |
| waves cleared | 9 | 9 | 0 |
| **time of death** | 190.61 s | **186.12 s** | **−2.36 %** |
| bodies killed | 779 | 767 | −1.5 % |
| pets spawned | 632 | 620 | −1.9 % |
| **pet attacks** | 121 | **196** | **+62.0 %** |
| intake (all sources) | 369,066 | 376,483 | +2.0 % |
| DoT intake | 18,181 | 16,740 | −7.9 % |
| `percent_current_life` intake | 136,542 | 147,027 | +7.7 % |
| **ADCtH offered** | 27,967,378 | **47,963,839** | **+71.5 %** |
| healing landed | 348,486 | 356,212 | +2.2 % |
| mean HP | 95.6 % | 96.1 % | +0.5 pts |
| ticks below half | 36 | 33 | −8.3 % |
| dry fraction (run) | 0.628 | 0.621 | −1.2 % |
| final-200 dry fraction | 0.915 | 0.840 | −8.2 % |
| **`N_eff`** | **2.99** | **4.76** | **+59.3 %** |
| **contact ticks** | **868** | **864** | **−0.5 %** |

**The last two rows are the whole lap.**

---

## 4 — ⚑ THE T-BAND SCORECARD, and T4 is graded SPLIT as the conductor ruled

| band | verdict | number |
|---|---|---|
| **T1** survival depth | **MET (exact)** — but see § 5 | death on **wave 160**, all three cells |
| **T2** fight duration, ±15 % of 186 s (158.1–213.9) | **MET** | **186.12 s = +0.06 %** |
| **T3** pacing shape | **NEAR** | median ratio over 151–159 **1.104**; ex-154 **ratio 0.988, Pearson r 0.697**; 158→159 **×2.00** vs reference **×1.86** |
| **T4a** sustain-through-throughput | **MET** | ADCtH **127.4×** intake; mean HP **96.1 %**; **33 / 2,280** ticks below half; landed fraction **0.74 %** |
| **T4b** terminal mechanism (DoT-involved AND fought) | **MISSED** | terminal wave **6.69 s**, **ZERO** player damage rows, DoT **0.0 %** of its 20,860 intake |

**T3 in full.** The raw I-1 predicate (`per[-1]` vs `per[-3]`) reads `False` and the corrected
predicate over the last **completed** pair also reads `False` — **both are emitted, and the verdict
is graded on the raw one, unchanged.** I self-reported this predicate defect at I-1 § 9.2 and
declared the double-emission in math note § F.2 **before this lap ran**, precisely so that
"correcting a checker" could not be mistaken for grading myself up. The pacing table below shows
the slowdown the predicate cannot see.

### The pacing curve

| wave | reference | I-1 | **I-2** | ratio (I-2) | pets (I-2) | Σ pet eHP |
|---:|---:|---:|---:|---:|---:|---:|
| 151 | 16 s | 18.20 | **18.20** | 1.14 | 12 | 3.41 M |
| 152 | 17 s | 20.08 | **19.59** | 1.15 | 81 | 10.19 M |
| 153 | 15 s | 16.33 | **16.24** | 1.08 | 16 | 0.82 M |
| **154** | 14 s | 38.12 | **38.12** | **2.72** ⚑ | 55 | 23.64 M |
| 155 | 16 s | 12.98 | **11.92** | 0.75 | 8 | 5.53 M |
| 156 | 20 s | 22.53 | **22.53** | 1.13 | 30 | 6.96 M |
| 157 | 19 s | 21.31 | **20.98** | 1.10 | 70 | 18.92 M |
| 158 | 14 s | 10.61 | **10.61** | 0.76 | 55 | 3.10 M |
| **159** | 26 s | 23.43 | **21.22** | 0.82 | **263** | **54.62 M** |
| **160** | 29 s | 7.02 | **6.69 (death)** | **0.23** ⚑ | 30 | 8.18 M |
| **total** | **186 s** | **190.61** | **186.12** | **1.0007** | **620** | **135.4 M** |

**⚑ Wave 159 carries 40 % of the pet eHP on the board and it got 9.4 % FASTER.** Wave 154 remains
the pre-existing travel outlier (unchanged at 38.12 s in both laps; it predates both folds and has
never been diagnosed).

---

## 5 — ⚑ WHY THE BOARD HARDENED ×1.67 AND THE CLOCK DID NOT MOVE

**This is the finding of the lap, and it is not about pets.**

### 5.1 The identity, verified against the emitted rows in both laps

The math note § D used `rows ≈ Σ eHP / 51,726`. **That was an approximation and it happened to
close at I-1 only because overkill and banner-doubling cancelled.** Re-derived properly here:

| | I-1 | I-2 |
|---|---:|---:|
| body-hit rows (player-sourced damage rows) | 2,596 | **4,116** |
| contact ticks | 868 | **864** |
| rows per contact tick (`N_eff`) | 2.991 | **4.764** |
| Σ `damage_applied` | **133.2 M** | **228.4 M** |
| Σ `hp_max` of bodies actually killed | **133.2 M** | **228.3 M** |
| agreement | EXACT | **0.04 %** |

**The true identity is `Σ applied = Σ eHP destroyed`, and the throughput unit is the body-hit ROW.**
The player destroyed **95.2 M more eHP** and paid **four fewer contact ticks** for it.

### 5.2 The mechanism, and it is a declared model property that has become load-bearing

`disc.resolve_tick` is **uncapped multi-target** — every body inside 3.0 m takes the full tick
damage — and the hit test is a **point** (`entity_radius_m = None`, gate item **M-5**), so bodies
have no packing constraint. Harder pets survive longer, longer-lived pets accumulate, and
accumulation *is* throughput. **The fold made the crowd denser, not the fight longer.**

### 5.3 ⚑ AND THE DENSITY IS NOW PHYSICALLY IMPOSSIBLE, MEASURED

A 3.0 m disc is **28.27 m²**. At a half-metre body radius, hexagonal packing fits **32** bodies;
simple area division gives **36**.

| tick class | I-1 ticks | I-1 share of kill work | **I-2 ticks** | **I-2 share of kill work** |
|---|---:|---:|---:|---:|
| `N_eff ≥ 10` | 33 | 21.5 % | **87** | **39.1 %** |
| `N_eff ≥ 20` | 8 | 8.2 % | **32** | **22.8 %** |
| `N_eff ≥ 26` | 4 | 4.9 % | **19** | **15.8 %** |
| `N_eff ≥ 36` (above the packing ceiling) | 1 | **1.4 %** | **8** | **8.3 %** |
| max `N_eff` observed | **37** | | **54** | |

**8.3 % of the reference cell's kill work now happens at a body density no arrangement of bodies
could achieve, up from 1.4 %.** The point hit-test was a declared simplification when the board was
96.8 % empty (PM-3), a rounding when the roster got its bodies back (I-1), and is now a term. **It
is not tuned, not touched, and not mine to rule on alone — it is the queue item this matrix names.**

---

## 6 — ⚑ WAVE 160 IS UNCHANGED IN KIND, EXACTLY AS PREDICTED

| | I-1 | **I-2** |
|---|---:|---:|
| ticks the player survived | 86 (7.02 s) | **82 (6.69 s)** |
| **player-sourced damage rows** | **0** | **0** |
| intake over the wave | 20,903 | **20,860** |
| `aetherialvanguard_crystal_devastationshard` | 9,923 | **9,923** |
| `aetherialvanguard_arcanemissilenova` | 8,343 | **7,584** |
| `wraith_sappingorbs` | 2,444 | **3,353** |
| pet-source share of the terminal intake | — | **63.6 %** |
| pets spawned / killed on w160 | 30 / 0 | **30 / 0** |
| player HP entering the wave | full | **20,005 (full)** |
| killer | `w160_pet0011` | **`w160_pet0017`** |
| live bodies at death | 35 | **35** |

**Prediction P.5 was CONFIRMED on all five clauses, and the reason it was predictable is
structural: the player deals zero damage on wave 160, so a body that is never hit does not care how
much life it has.** The pet-life fold is incapable of reaching this mechanism. **T4b fails again,
and it will keep failing until the player gets an answer during the approach window — which is
I-2 (kit/dash) and I-3 (potion) in the queue, not this limb.**

⚑ **And the fold DID reach one thing here:** `aetherialvanguard_crystal` — Aleksander's Shard, one
of Lap E's four camera-measured control bodies, and the source of 9,923 of the 20,903 that killed
the I-1 player — now enters at its **measured 103,912** instead of Lap B's 24,759. It is emitted on
the wire at that value (assert-wall check 28). It still killed the player, because the player never
touched it.

---

### 6.1 — ⚑ THE OBSERVABILITY LIMB, DEMONSTRATED: the L-2 CL-10 ambiguity is now a JOIN, not a dispute

At L-2 the conductor had to resolve by hand whether the killer was `w160_pet0011` (my driver) or
`w160_a001` (the wire), and ruled it a **NOTE-9 basis split on one row** — `source_id` was the
owner wendigo, `damage_source_tag` was its summoned wraith, both true. **That resolution cost a
conductor a manual read of two surfaces because the wire could not express the relation.** It now
can. Straight off the I-2 baton bytes, no driver involved:

```json
{"actor_id": "w160_pet0017", "record_path": "records/creatures/enemies/wraith_c01_summon.dbr",
 "owner_id": "w160_a001", "spawn_wave": 160, "spawn_tick": 2221, "spawn_t_s": 181.3061,
 "spawn_skill_id": ".../nemesis/wendigo_summonwraiths.dbr",
 "hp_max": 395757.0, "hp_max_basis": "MEASURED-PET-BAND-B-LO@w160",
 "death_tick": null, "death_cause": null, "alive_at_wave_end": true}
```

**`owner_id` is the join.** The pet and its summoner are one row apart, the basis names the limb and
the wave, and `death_tick: null` says out loud that this body outlived the player. Every L-2 pet
claim — **620 bodies, 584 killed, 6 TTL, 30 alive at death, Σ `hp_max` 135,375,626** — re-derives
from the baton alone. `run_summary.actors_killed` still counts **183 roster bodies only**, which is
correct and now *checkable* rather than confusing.

---

## 7 — THE DEFENCE ISOLATION, and the banner flips sign

| | I-1 DEF-OFF | I-1 DEF-ON | **I-2 DEF-OFF** | **I-2 DEF-ON** |
|---|---:|---:|---:|---:|
| time of death | 189.14 s | 190.61 s (**+0.78 %**) | 188.73 s | **186.12 s (−1.38 %)** |
| banner tether occupancy | — | 32.5 % (760/2,335) | — | **32.8 % (748/2,280)** |
| kills | 789 | 779 | 771 | 767 |
| `N_eff` | 3.23 | 2.99 | 4.94 | **4.76** |

At I-1 the banner made the reference cell **0.78 % slower** and I called it "inside the noise of the
movement policy." **It has flipped to 1.38 % faster.** Same modifier, same tether, same placement —
the difference is that on a denser board the doubled damage does more work per tethered tick. **The
banner's sign is a property of board density, not of the banner.** Neither reading is large; both
are reported because a sign flip on an unchanged mechanism is worth naming.

---

## 8 — ⚑ PRE-REGISTERED PREDICTIONS vs OUTCOME — **three confirmed, nine falsified**

| # | prediction (written before the code) | outcome |
|---|---|---|
| **P.1** | pet bodies spawned **FALL** from 632 to 300–500 as the cap binds | **⚑ FALSIFIED.** **620** — a 1.9 % fall. Median pet lifespan barely moved (2.94 s → 3.02 s) *despite each pet being 4.08× harder*, so the cap never bound. § 5 is why |
| **P.2** | Σ pet eHP destroyed rises by **less** than ×4.08 (band ×2.4–3.2) | **FALSIFIED.** **×4.083** — the naive figure, essentially exactly. The population did not fall, so nothing discounted it |
| **P.3** | **THE HEADLINE — ToD 225–275 s (centre 248), T2 MISSED LONG** | **⚑ FALSIFIED, and it is the most important wrong answer in the lap.** **186.12 s**, +0.06 %, **T2 MET**. The fight got **FASTER** with a ×1.67 harder board. I argued the direction explicitly and the direction was wrong |
| **P.4** | T1 holds — death on wave 160, approach-window mechanism | **CONFIRMED.** Wave 160 in all three cells |
| **P.5** | wave 160 unchanged in kind: 7.0 ± 1.5 s, ZERO player damage rows, intake 20,903 ± 2,000, killer a pet, **T4b still fails** | **CONFIRMED on all five clauses.** 6.69 s · 0 rows · 20,860 · `w160_pet0017` · T4b **MISSED**. The one prediction that reasoned from a *structure* rather than from a magnitude |
| **P.6** | `N_eff` rises from 2.99 into 3.4–4.5 | **FALSIFIED on the high side, direction right.** **4.76**, over my ceiling. I saw the mechanism and under-priced it — which is worse than not seeing it |
| **P.7** | pet share of intake 25–40 %; total intake 500–700 k | **FALSIFIED, both clauses.** Share **23.1 %** (from 15.9 %, just under my floor); intake **376,483**, nowhere near 500 k. Pets swing 62 % more often and it barely moves the total, because pet damage is a small term |
| **P.8** | dry fraction < 0.60; final-200 dry > 0.85 | **FALSIFIED, both narrowly, both in the predicted direction.** 0.628 → **0.621** (not under 0.60); final-200 0.915 → **0.840** (not over 0.85) |
| **P.9** | wave 159 becomes 45–70 s; T3 median ratio 1.4–1.9 | **⚑ FALSIFIED, and the SIGN is wrong on the headline clause.** Wave 159 went **23.43 → 21.22 s** — the wave carrying 40 % of the new eHP got **FASTER**. T3 median ratio **1.104** (from 1.121), i.e. T3 barely moved |
| **P.10** | ADCtH offered 40–55 M; landed fraction falls below 1.25 % | **CONFIRMED.** **47.96 M**; landed fraction **1.25 % → 0.74 %** |
| **P.11** | total kills fall to 460–650 | **FALSIFIED.** **767**, down 1.5 %. Roster 183 (fixed by the roll) + pets 584 |
| **P.12** | CAMP's TTL stalls worsen: ≥ 3 capped waves, total > 806.61 s | **FALSIFIED.** **Two** capped waves (152, 157) and **806.61 s exactly**, to the tick, identical to I-1 — see § 9 defect 2, which explains why and is the cleanest mechanism measurement in the lap |

**The unifying error, and it is the same shape as I-1's G.1.** At I-1 I priced the sustain term and
never priced the exposure term. Here I priced the **eHP** term and never priced the **co-residence**
term. Both times the arithmetic was right to the digit and produced the wrong answer, because the
question was never "how much life does this body have" — it was **"how many bodies is the disc
touching while it has it."** § 5's identity is the correction, and it is now on the wire.

---

## 9 — ⚑ DEFECTS AND UNDER-READS I FOUND IN MY OWN AND OTHERS' WORK (Discipline #11)

| # | what | how found | effect |
|---|---|---|---|
| **1** | **⚑ THE CONDUCTOR'S L-2 PREMISE IS FALSE, AND THE FINDING IS STILL TRUE.** L-2 says `waves[].pets` was *"present in PM-2/PM-3"* and dropped at I-1. **No baton in the lineage — baseline, pm1, four pm2, five pm3, three pm4-i1 — carries a key matching `pet*` anywhere in its payload.** | I checked the bytes before implementing, because "restore" and "add" are different jobs | `waves[].pets` has always been a **sim-surface** structure (`run.py`), which the adapter's own pet-row-withholding note refers to. **Nothing regressed at I-1**; the wire has been blind to pets since PM-2 and I-1 is simply the first lap where the blindness was load-bearing. **This lap is an ADDITION, not a restoration**, and it is filed as one |
| **2** | **⚑ MY OWN P.12 WAS WRONG FOR A REASON WORTH MORE THAN THE PREDICTION.** CAMP's per-wave times are identical to I-1 **to the centisecond on all ten waves**, while its kills (757 → 751) and TTL expiries (6 → 24) both moved | the coincidence was too exact to write down without one more check (I-1 defect #4's rule) | Instrumented last-roster-death vs last-pet-death per wave: on **6 of 10** waves the clock is set by the **last ROSTER death** and every pet is already dead; on **154 and 159** it is set by a **pet TTL**, a wall clock independent of HP; on **152 and 157** by the 4,000-tick cap; on **160** by the player's death with no deaths at all. **CAMP's wave clock is never set by pet HP**, so a pet-life fold cannot move it. Not a defect in the fold — a measurement of what the CAMP control actually controls for |
| **3** | **My own math note § D used the wrong throughput identity.** It wrote `rows ≈ Σ eHP / 51,726`, which ignores overkill capping *and* the banner's doubled rows | the I-2 numbers did not close (applied 228.4 M vs `rows × 51,726` = 212.9 M) and I chased it | The approximation closed at I-1 to 0.6 % **only because the two errors cancelled at that board density.** The correct identity is `Σ applied = Σ eHP destroyed` (§ 5.1, closes to 0.04 %). **My pre-registered bands were computed on the wrong identity** — it does not rescue any of them, but the record should say which arithmetic produced them |
| **4** | **⚑ THE LO LIMB OF RECORD UNDERSTATES 2 OF LAP E'S 4 CAMERA CONTROLS, AND I DID NOT MOVE IT.** | assert-wall check 28, written to fingerprint the fold against the bodies Lap E's verdict stands on | Death Revenant **468,504 = EXACT** · Aleksander's Shard **103,912 = EXACT** · `skeleton_a02_summon` **39,771 vs 41,237 = −3.6 %** (its HI limb is exact; camera level 109 = the set's ceiling) · Aetherial Bileeater **422,162 vs 484,095 = −12.8 %** (CLIFF C-E1: camera level 112 lies **outside** its derived set {104…108}, so **no** limb reaches it). **The limb of record is CONSERVATIVE on every body where truth is independently known.** Moving it to make the controls fit would be fitting a limb to an outcome — declared on the wire as `PM4-PET-LO-LIMB-UNDERSTATES-THE-CAMERA-CONTROLS` |
| **5** | **`PROVENANCE_VOLATILE_KEYS` is still incomplete** — carried from I-1 unrepaired | the masked baton-vs-on-disk compare | Exactly one difference per cell, confined to `sim_pin.tree_state_untracked_entries_excluded`. **Handed over, not taken. Star-lord's.** |
| **6** | **One pre-existing test failure in star-lord's seam**, unrelated to this lap | the smoke wall | `test_cycle13_normal_season_export.py::TestRoundTrip::test_manifest_has_elements_block` asserts `water` in the manifest while the substrate emits `ice` — star-lord's own `water→ice` rename, commit `1038e285`. **No import path from anything I touched. Reported, not fixed** (not my seam) |

### ⚑ 9.1 — THE REGRESSION CLAIM IS PROVED, NOT ASSERTED

The full wall reads **63 failed / 10,466 passed / 21 errors** and I will not hand that over with
"they look unrelated." Re-run over the **exact 13 files that fail**, in an isolated `git worktree`
at the **pre-I-2 commit `e6f3b2c6`**:

| | failed | passed | errors |
|---|---:|---:|---:|
| pre-I-2 (`e6f3b2c6`, worktree) | **72** | 574 | 21 |
| post-I-2 (`01a42e3b`) | **63** | 583 | 21 |

**Set difference of failing test IDs: ZERO new failures introduced by I-2.** Nine are present
before and absent after — the worktree lacks untracked `data/` artifacts, which is the expected
direction. Every one of the 63 lives outside the simulation seam: `test_cycle12_layer4_convergence`
(33), `test_cycle13_wave5_season_generation` (21 errors), `test_cycle12_layer6_t4_wireup` (12),
`test_kit_space_emitter` (4), `test_foundation` (4), and eight singletons.

---

## 10 — DECLARED ASSUMPTIONS + GAPS (every one on the wire)

**⚑ CLIFF C-I2-1 — THIS FOLD CORRECTS PET *LIFE*, NOT PET *POPULATION*.** Lap E's **IS-E1**
measured that the Lap-B contract chain (`pm2_tg2_pet_chain.csv`, which this iteration does **not**
re-emit) reaches **70 of the 128** summon bodies. The **58** it misses carry **Σ 15.7 M eHP @ w160**
and are **still never spawned** — one of them, `aetherialbloater_b01_summon`, is a body Lap E's own
verdict is measured on. **Named absence with a positive sign: closing it can only harden the board
further.** Wired as `PM4-PET-POPULATION-IS-STILL-LAP-B-CLIFF-C-I2-1`.

**CLIFF C-E3 — `monsterLevelGapFixer = [0, 5, 7]`** (+7 at Ultimate) is folded by neither lap and
bears on roster and pets alike. **QUEUED by conductor ruling, NOT folded**, magnitude unpriced. It
may already be absorbed into the +3 proxy-band→camera offset, in which case folding it would
double-count. Wired as `PM4-C-E3-MONSTERLEVELGAPFIXER-IS-QUEUED-NOT-FOLDED`.

**CLIFF C-E1** — one of the four camera controls dissents on the owner-level rule by +6; carried,
not smoothed (§ 9 defect 4).

**CLIFF C-D3 / R-PM4-6 — the NAMED GAP.** `krieg_aethertrap.dbr` would enter DECLARED `hp_max = 0.0`
with basis `GAP:NO-characterAttributeEquations`. **It did not roll: 0 GAP pets across all three
cells.** It is absent from the value dict (so it cannot masquerade as a measured zero) and named in
the basis dict at every wave (so the absence is loud). **Not sibling-filled, modal-filled or
interpolated** (assert-wall check 30).

**Carried unchanged from I-1:** pet **damage** still rides the PM-2 threat fold (C-E5 / C-D4) ·
band B stops at 170 by refusal (C-D2) · the three beacons do not fire · placement D-1 · rank policy
· OA fold with `dexterityDV` absent · resist-then-armour order · SEM-1 total-over-duration ·
`percent_current_life` unmitigated, floored and **still unverifiable** (now 39.1 % of intake at
147,027) · pet cap 12 on 36 cap-less contracts · pet straight-line locomotion · 51 ungated pet
specials · 593 control/debuff rows that are not HP damage · 30 non-MEASURED-rank rows ·
`max_ticks = 4000` · wave 154's travel outlier · **the point hit-test (M-5), which § 5.3 has just
promoted from a rounding to a term.**

**LAW 3 — check 25, `moved: {}`.** `PLAYER_ADCTH_PCT = 21.0` · `PLAYER_HP_MAX = 20005.0` ·
`PLAYER_REGEN_HP_PER_S = 129.38` · `player_damage_per_tick(SHEET_MEASURED) = 51726.0` ·
`disc_radius_m = 3.0` · `max_ticks = 4000` · **`GLOBAL_PET_LIMIT = 12`, added to the witness set
this lap** because a ×4 lifespan makes the pet cap tempting for the first time. **There is no
fitted number anywhere in this lap, and 186.12 s was not aimed at — I predicted 248 s.**

---

## 11 — COVERAGE, counted from the emission (#70)

| | |
|---|---:|
| Lap-E table records | **128** (127 MEASURED, 1 named gap) |
| the sim's contract pet population | **70** distinct records |
| of those, in the table and MEASURED | **70 / 70 = 100.00 %** |
| records that actually spawned this run | **36** |
| emitted pets absent from the table | **0** |
| emitted pets carrying the GAP basis | **0** |
| `hp_max_basis` census (reference cell) | **10 distinct**, one per wave, `MEASURED-PET-BAND-B-LO@w151…w160` |
| pets on the wire | **626 / 623 / 620** across the three cells |
| pet lifecycle completeness | **0** missing fields, **0** dead-without-a-death-tick, **0** alive-carrying-a-death-tick, wire count **≡** model counter (1,869 ≡ 1,869) |
| pet `hp_max` min / median / max (reference) | **149 / 213,639 / 767,272** |

---

## 12 — SEAM WORK (star-lord: one schema addition, two semantic shifts, one defect handed back)

Both filed in `export/MIGRATION.md` and `simulation/MIGRATION.md` `[2026-08-13] KC2-PM4 · I-2`.

1. **⚑ ONE ADDITIVE FIELD ON A COUNTERSIGNED MODEL — `Wave.pets: list[PetActor] = []`.**
   Defaulted, so all fourteen frozen batons round-trip and re-gate byte-for-byte (**measured: 17/17
   green**). `PetActor` carries 17 fields; `spawn_t_s`/`death_t_s` are **DERIVED from the run-wide
   tick** in the emitter, exactly as `Actor.spawn_t_s` is, so `waves[].pets[]` joins to `events` and
   `tracks` on the same axis every other surface uses. **This is not the move I-1 refused** —
   retyping `Actor.threat_tier`'s closed `Literal` would have changed an existing field's meaning;
   **pets still do NOT enter `actors[]`.** **Star-lord's three calls, none taken here:** (a) does
   `PetActor` belong in `baton_v1_schema` or in a sim-side sidecar; (b) should `hp_max_basis` /
   `death_cause` be `Literal` enums; (c) should `_integrity` gain a `pet_count` (it does **not**
   today — no countersigned invariant moved).
2. **⚑ SEMANTIC SHIFT — `waves[].pets[].hp_max` was a Lap-B declaration and is now a measurement.**
   ×4.083 over the realised spawns; pet share of the board's life 22.4 % → 53.6 %. Wire row
   `PM4-PET-EHP-IS-MEASURED-AT-ITS-OWN-SPAWN-WAVE`.
3. **⚑ SEMANTIC SHIFT — `waves[].pets[].hp_max_basis` was the literal `"PET-MEASURED"`**, a claim
   about a value now measured wrong in two directions. Wire row `PM4-PET-HP-MAX-BASIS-VOCABULARY`.
4. **ONE I-1 DECLARATION SUPERSEDED, NOT DELETED** — `PM4-PET-LIFE-IS-A-DIFFERENT-FOLD-CLIFF-C-D1`
   is replaced by `PM4-PET-LIFE-CLIFF-C-D1-IS-CLOSED-MEASURED` on I-2 batons only, so a consumer
   that read the old row can see which row replaced it.
5. **`KC2RunSpec` gains ONE optional field** (`pet_ehp: bool = False`); **no schema version, no
   event column, no enum member, no validator predicate moved.** The `M-13` known-vocabulary
   predicate widened at I-1 already admits the new basis strings and needed no change.
6. **⚑ HANDED BACK AGAIN, STILL NOT TAKEN: `PROVENANCE_VOLATILE_KEYS` is incomplete** (§ 2).

**rocket:** nothing. **drax / scene consumers:** ⚑ **a picture drawn from a PM-4 I-1 baton shows
pets popping on contact and roughly a third of the board's life on summoned bodies; it is now over
half, and they survive ~4× longer.** Also: **the sim routinely puts 20–54 bodies inside a 3.0 m
circle** (§ 5.3) — a scene that renders that literally will not look like a game.
**jack-ryan:** Disciplines #1, #2, #3, #11, #12 exercised and named.

---

## 13 — PINS

**At launch:** engine HEAD `e6f3b2c6` · 14 frozen batons + I-1 findings verified from bytes ·
3 substrate CSVs digest-verified at FULL hash.
**At landing:** HEAD `1128a055`, **PUSHED**. Every commit by **explicit path**; **no `git add -A`
anywhere in this lap.**

---

## 14 — ⚑ SELF-ATTACK SURFACES, AND THE FIRST ONE IS THE WHOLE NOTE

1. **⚑ T2's +0.06 % IS THE WEAKEST KIND OF EVIDENCE THERE IS AND I WILL NOT LET IT READ AS
   CONVERGENCE.** I-1 met T2 at +2.5 % by two errors cancelling and said so (§ 13.2). I-2 meets it
   at +0.06 % **after a fold I predicted would blow it out by +33 %** — which means the agreement is
   produced by a mechanism I did not model until after I measured it (§ 5). **A band met by a
   mechanism you could not predict is not a replicated fight; it is a coincidence you now understand.**
2. **§ 5.3 says 8.3 % of the kill work is physically impossible.** That is the number I would
   re-order the queue on, and it is a property of the *player's weapon model*, not of the monsters.
3. **T1's MET is still mechanism-divergent** (§ 6) and has been since I-1. Same wave, different
   death, two laps running. **T4b has now failed twice, for the same reason, and neither eHP fold
   could ever have touched it.**
4. **The three cells have converged on each other**: CLUSTER/DEF-OFF 188.73 s, CLUSTER/DEF-ON
   186.12 s — a 1.4 % spread where I-1 had 0.78 % the other way. When a matrix stops discriminating,
   the matrix has stopped being an instrument.
5. **`percent_current_life` is now 39.1 % of intake (147,027) and is still unverifiable** (PM-2
   § 13.1, unchanged across three laps). It is the single largest un-audited term in the damage model.
6. **Wave 154's 38.12 s travel outlier is now the ONLY wave over 26 s** and has survived PM-2, PM-3,
   I-1 and I-2 without ever being diagnosed. It carries the whole of T3's correlation loss
   (r 0.049 → **0.697** on holding it out).

---

## 15 — WHAT I WOULD PUT AT THE TOP OF THE QUEUE (conductor's call, not mine)

**The largest remaining measured divergence has moved off the monsters and onto the player's
weapon.** Two laps of substrate completion have now given the roster and the summons their real
bodies, and the fight clock did not move, because `disc.resolve_tick` converts extra life into
extra density and density into throughput. **The next measurable limb is the disc itself: the point
hit-test (`entity_radius_m = None`, M-5) and the absence of any multi-target cap.** § 5.3 prices it:
**39.1 % of kill work at `N_eff ≥ 10`, 8.3 % above the packing ceiling, max 54 bodies in 28.27 m².**

**C-E3 (`monsterLevelGapFixer`) prices out small against that** — it is a +7-level term on a life
model that the disc has just demonstrated it can absorb. **I would not fire Lap F for it yet.**

**I-2 (kit/dash) and I-3 (potion) remain the only queued items that can touch T4b**, which has now
failed twice for a mechanism neither eHP fold can reach (§ 6).

**No HALT was hit. Nothing required inventing an unmeasured quantity. There is no fitted constant
anywhere in this lap, and 186.12 s was not aimed at — I predicted 248 s and argued the direction
out loud before running.**
