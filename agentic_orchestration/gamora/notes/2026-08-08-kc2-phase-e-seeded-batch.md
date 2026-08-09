# KC2 Phase E — the seeded batch: 20/20 runs executed, 0 candidates, and the reason is structural

**Author:** gamora (simulation seam) · **Date:** 2026-08-08
**Commission:** R-L73-1 (ledger row L-73) · **Conductor:** gandalf, `RUN-CONDUCTOR`
**Math note (Discipline #1, written before the driver):** `reincarnated-engine/src/reincarnated/simulation/math/kc2-phase-e-seeded-batch-2026-08-08.md`
**Driver:** `reincarnated-engine/src/reincarnated/simulation/scripts/gamora_kc2_phase_e_seeded_batch_2026_08_08.py`
**Artifact of record:** `reincarnated-engine/src/reincarnated/simulation/output/kc2-phase-e-seeded-batch-full-20260808_205104.json`

> **HEADLINE — the batch ran clean and returns an EMPTY slate.** All 20 pre-registered runs executed,
> **zero anomaly flags across all five classes on all 20**, and § 4.5 applied verbatim yields
> **filter 1: 10/20 · filter 2: 0/20 · survivors: 0 · top-3: EMPTY.** No filter was relaxed. Filter 2
> returns zero not because the runs were dirty but because **its admissible terminal set has an empty
> intersection with the states this model can reach** — death has no mechanism, ladder-exhaustion has
> no geometry, cash-out has no model. **HALTing the selection back to the conductor** per the brief's
> own instruction; the measurement layer under the choice is below, complete.

---

## 1 · Seed mapping declaration + harness provenance

### 1.1 Seed mapping — DECLARED BEFORE ANY OUTCOME (R-L73-1 clause 2)

The mapping was printed by the driver's § A block ahead of the first `simulate_wave` call, and is
committed at engine `40a269dd` in both the math note (§ B) and the driver (`engine_seed`).

```
engine_seed(conductor_seed c, wave w)  =  600_000  +  w × 1000  +  (c − 1)        c ∈ {1…10}
```

| conductor-seed | w1 | w93 | w151 | w170 |
|---:|---:|---:|---:|---:|
| 1 | 601000 | 693000 | 751000 | 770000 |
| 2 | 601001 | 693001 | 751001 | 770001 |
| 3 | 601002 | 693002 | 751002 | 770002 |
| 4 | 601003 | 693003 | 751003 | 770003 |
| 5 | 601004 | 693004 | 751004 | 770004 |
| 6 | 601005 | 693005 | 751005 | 770005 |
| 7 | 601006 | 693006 | 751006 | 770006 |
| 8 | 601007 | 693007 | 751007 | 770007 |
| 9 | 601008 | 693008 | 751008 | 770008 |
| 10 | 601009 | 693009 | 751009 | 770009 |

**Band disjointness (Discipline #3) by arithmetic, not assertion:** s1 occupies 311,000…403,031 · s2
occupies 481,000…489,031 · **Phase E opens at 601,000** and closes at 770,009. The band opens above
the maximum of every prior KC2 band, so disjointness holds for every `(wave, k)` pair — not merely
for the ones both bands happen to use. Non-KC2 bands in this seam sit at 71M+ and 74M; no contact.

**No seed shopping, no re-rolls.** The 20 runs are the population.

### 1.2 Harness provenance

| Item | Value |
|---|---|
| engine sha at execution | `40a269dd` (math note + driver commit; parent `c60db115`) |
| **tree-state at execution** | **`clean`**, policy **`code-surface-v2`** — `untracked_outside_src=134`, `untracked_excluded=2573` |
| invocation | `gamora_kc2_phase_e_seeded_batch_2026_08_08.py` (no args = full) |
| wall-clock, full batch | **4.98 s** (20 runs, 1,130 wave-simulations) |
| wall-clock, smoke | 1.14 s (2 seeds × 2 configs) |
| python / platform | 3.12 / macOS (darwin 24.6.0) |

⚑ **Harness hygiene (R-L73-1 clause 6) verified BEFORE and AFTER.** Before: the only untracked entries
under `src/` outside an `output/` directory were this lap's own math note and driver — both committed
at `40a269dd` **prior to the full run**, which is why the tree grades `clean` and the FULL capability
built at L-71/L-72 is exercised rather than merely available. After: **0** untracked entries under
`src/` outside `output/`. Batch artifacts land in `src/reincarnated/simulation/output/` (excluded by
v2) and this note lands outside the engine repo entirely.

### 1.3 Pinned parameters, unvaried across the population

`SHEET_MEASURED` player-damage limb = **51,726.0 /tick = 633,643.5 DPS** (R-L68-2, extending
`fixture.py:126`) · p06 **OFF** (F-10 operative limb) · `MotionLimb.ZONE_FIRST` ·
`NodeAssignment.NEAREST_NODE` · `PlayerPolicy.CAMP_THEN_COLLECT` · `WaveScaling()` default ·
tree-state policy `code-surface-v2` (R-KC2-11) · band `[151,160]` · wall threshold 1.5 ·
trailing window 5 · uptime floor 60 %.

Arena pairing is the run's DECLARED per-sitting selection: wave-1 → `ARENA_S1` (`sm_mod/survivalworld_f`),
checkpoint-150 → `ARENA_S2` (`sm1/survivalworld_a`). Neither run substitutes the other's;
`Arena.merge` raises rather than pools (L-21).

---

## 2 · Full population table — all 20 runs

Per-wave clear time is the **§ 10.9 four-term cycle**, `quantise_to_wave_tick(0.5 + t_end_s + 0.5)` —
the quantity this run's own calibration lane compares against the fixture (math note § C.2). Channel
uptime is against **alive-time including the 1.0 s inter-wave interval** (math note § C.3); against
engagement-time alone it is 100.0 % on all 20 and would not be a tie-break at all.

| run-id | seed | first wave | arena | waves fought (first–last) | deepest | terminal state | class | uptime % | aura 100 % | anomaly flags | emit-stub | tree grade |
|---|---:|---:|---|---|---:|---|---|---:|---|---:|---|---|
| `E-s01-w1` | 1 | 1 | s1 | 1–93 (93) | 93 | `ehp_band_exhausted` | **INSTRUMENT** | 92.72 | ✔ | **0** | PASS | clean |
| `E-s01-cp150` | 1 | 151 | s2 | 151–170 (20) | 170 | `arena_tier_exhausted` | **INSTRUMENT** | 90.68 | ✔ | **0** | PASS | clean |
| `E-s02-w1` | 2 | 1 | s1 | 1–93 (93) | 93 | `ehp_band_exhausted` | **INSTRUMENT** | 92.95 | ✔ | **0** | PASS | clean |
| `E-s02-cp150` | 2 | 151 | s2 | 151–170 (20) | 170 | `arena_tier_exhausted` | **INSTRUMENT** | 90.84 | ✔ | **0** | PASS | clean |
| `E-s03-w1` | 3 | 1 | s1 | 1–93 (93) | 93 | `ehp_band_exhausted` | **INSTRUMENT** | 92.63 | ✔ | **0** | PASS | clean |
| `E-s03-cp150` | 3 | 151 | s2 | 151–170 (20) | 170 | `arena_tier_exhausted` | **INSTRUMENT** | 91.21 | ✔ | **0** | PASS | clean |
| `E-s04-w1` | 4 | 1 | s1 | 1–93 (93) | 93 | `ehp_band_exhausted` | **INSTRUMENT** | 92.72 | ✔ | **0** | PASS | clean |
| `E-s04-cp150` | 4 | 151 | s2 | 151–170 (20) | 170 | `arena_tier_exhausted` | **INSTRUMENT** | 90.95 | ✔ | **0** | PASS | clean |
| `E-s05-w1` | 5 | 1 | s1 | 1–93 (93) | 93 | `ehp_band_exhausted` | **INSTRUMENT** | 92.80 | ✔ | **0** | PASS | clean |
| `E-s05-cp150` | 5 | 151 | s2 | 151–170 (20) | 170 | `arena_tier_exhausted` | **INSTRUMENT** | 90.20 | ✔ | **0** | PASS | clean |
| `E-s06-w1` | 6 | 1 | s1 | 1–93 (93) | 93 | `ehp_band_exhausted` | **INSTRUMENT** | 92.38 | ✔ | **0** | PASS | clean |
| `E-s06-cp150` | 6 | 151 | s2 | 151–170 (20) | 170 | `arena_tier_exhausted` | **INSTRUMENT** | 91.25 | ✔ | **0** | PASS | clean |
| `E-s07-w1` | 7 | 1 | s1 | 1–93 (93) | 93 | `ehp_band_exhausted` | **INSTRUMENT** | 92.70 | ✔ | **0** | PASS | clean |
| `E-s07-cp150` | 7 | 151 | s2 | 151–170 (20) | 170 | `arena_tier_exhausted` | **INSTRUMENT** | 90.80 | ✔ | **0** | PASS | clean |
| `E-s08-w1` | 8 | 1 | s1 | 1–93 (93) | 93 | `ehp_band_exhausted` | **INSTRUMENT** | 92.52 | ✔ | **0** | PASS | clean |
| `E-s08-cp150` | 8 | 151 | s2 | 151–170 (20) | 170 | `arena_tier_exhausted` | **INSTRUMENT** | 90.62 | ✔ | **0** | PASS | clean |
| `E-s09-w1` | 9 | 1 | s1 | 1–93 (93) | 93 | `ehp_band_exhausted` | **INSTRUMENT** | 92.59 | ✔ | **0** | PASS | clean |
| `E-s09-cp150` | 9 | 151 | s2 | 151–170 (20) | 170 | `arena_tier_exhausted` | **INSTRUMENT** | 91.49 | ✔ | **0** | PASS | clean |
| `E-s10-w1` | 10 | 1 | s1 | 1–93 (93) | 93 | `ehp_band_exhausted` | **INSTRUMENT** | 92.61 | ✔ | **0** | PASS | clean |
| `E-s10-cp150` | 10 | 151 | s2 | 151–170 (20) | 170 | `arena_tier_exhausted` | **INSTRUMENT** | 91.38 | ✔ | **0** | PASS | clean |

### 2.1 Anomaly flags — each class, explicitly ZERO on all 20 runs

| # | Class | Predicate applied (math note § F) | Result |
|---|---|---|---|
| 1 | illegal channel-machine transition | exactly one `channel_start`, one terminal, ordered; `energy_dryout` ⇒ not cleared | **ZERO** (0/1,130 wave-instances) |
| 2 | energy < 0 | `min(tracks.energy) < 0` | **ZERO** |
| 3 | roster/count-model mismatch | realized bodies inside the hard per-point envelope `Σ min_alt(n_min) … Σ max_alt(n_max+c_max)`; champions ≤ `Σ max_alt(c_max)`; `actors[]` count == spawn-row count | **ZERO** |
| 4 | locomotion-law violation | any mover with `death_t_s` and no `contact_t_s`; or `death_t_s < contact_t_s` | **ZERO** |
| 5 | schema-validation warning at emit-stub | unknown `event_type`; row width ≠ `EVENT_COLUMNS`; `KC2Run.validate()` raise | **ZERO** |

**1,130 wave-simulations, zero flags of any class.** The harness is clean; nothing below is a defect
report against it.

### 2.2 Per-wave clear times inside [151, 160] — the 10 runs that reach the band (`cycle_s`)

| run | 151 | 152 | 153 | 154 | 155 | 156 | 157 | 158 | 159 | 160 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `E-s01-cp150` | 20 | 12 | 18 | 12 | 12 | **25** | 13 | 12 | 11 | 15 |
| `E-s02-cp150` | 18 | 14 | 19 | 15 | 12 | **26** | 14 | 14 | 11 | 15 |
| `E-s03-cp150` | 18 | 12 | 18 | 12 | 11 | **24** | 14 | 14 | 11 | 16 |
| `E-s04-cp150` | 19 | 13 | 17 | 14 | 12 | **25** | 14 | 13 | 11 | 17 |
| `E-s05-cp150` | 20 | 15 | 18 | 12 | 12 | **25** | 13 | 14 | 13 | 17 |
| `E-s06-cp150` | 19 | 13 | 16 | 15 | 13 | **26** | 12 | 12 | 12 | 18 |
| `E-s07-cp150` | 20 | 14 | 18 | 11 | 11 | **25** | 12 | 14 | 11 | 16 |
| `E-s08-cp150` | 20 | 12 | 16 | 13 | 12 | **25** | 14 | 14 | 12 | 16 |
| `E-s09-cp150` | 20 | 13 | 17 | 15 | 11 | **24** | 12 | 12 | 10 | 17 |
| `E-s10-cp150` | 16 | 14 | 17 | 16 | 12 | **24** | 12 | 14 | 10 | 18 |
| **mean** | 19.0 | 13.2 | 17.4 | 13.5 | 11.8 | **24.9** | 13.0 | 13.3 | 11.2 | 16.5 |
| **CV across seeds** | 6.7 % | 7.4 % | 5.3 % | 12.1 % | 5.1 % | 2.8 % | 6.9 % | 6.8 % | 7.8 % | 6.2 % |

The 10 wave-1 runs contribute **no** rows here — they never reach the band (§ 3.1).

---

## 3 · § 4.5 applied verbatim — the arithmetic

### 3.1 Filter 1 — band relevance (HARD): **10/20 pass**

| Config | n | waves in [151,160] | verdict |
|---|---:|---|---|
| checkpoint-150 (`*-cp150`) | 10 | 151…160, all ten | **PASS ×10** — satisfied by construction (spec § 10.2, `first_wave_fought = 151`) |
| wave-1 (`*-w1`) | 10 | none — every run stops at wave 93 | **FAIL ×10** |

⚑ **The reason the wave-1 limb fails is NOT the one R-L73-1 anticipated, and the difference is
load-bearing.** The brief's illustration reads *"a wave-1 run that dies at wave 30 is DATA (it fails
filter 1 and drops out) — that is the design working."* No wave-1 run died, because **death has no
mechanism** (§ 5, F-2). All ten stopped at wave 93 on `ehp_band_exhausted`, and even had eHP extended,
**`ARENA_S1` carries p01 placements for tiers 1…15 only — highest simulable wave 150, one short of the
band** (§ 5, F-4). The wave-1 limb cannot reach filter 1's band for a *geometric* reason. That is the
instrument binding, not the design working.

### 3.2 Filter 2 — technical cleanliness (HARD): **0/20 pass**

The five anomaly classes are **zero on all 20** (§ 2.1). Filter 2 nonetheless returns 0/20 on its
second clause:

```
admissible terminals   =  { death,  voluntary cash-out,  ladder-exhaustion }
reachable terminals    =  { ehp_band_exhausted,  arena_tier_exhausted }        both INSTRUMENT

death              unreachable   — 0 emitters of `player_death`; 0 rows with target_id="player";
                                   0 writes to `hp_player` after init; monster attack model
                                   `abstract-schedule` emits no monster-side damage at all
ladder-exhaustion  unreachable   — ARENA_S2 p01 tiers 1…17 (highest wave 170); ARENA_S1 tiers 1…15
                                   (highest wave 150); tiers 18/19/20 raise KeyError on BOTH.
                                   MAX_WAVE = 200 is not expressible on either cited arena.
voluntary cash-out unmodelled    — no offer surface, no policy; § 10.3 does not model it

| admissible ∩ reachable |  =  0        ⇒        filter 2 passes 0/20 BY CONSTRUCTION
```

Every run must terminate by instrument bound, and filter 2 **explicitly excludes instrument
terminations**. This is not a strict threshold; it is a predicate with an empty satisfiable set.

### 3.3 Composition result

```
filters 1 ∧ 2  →  survivors = ∅
rank 3         →  not reached (no input)
tie-break 4    →  not reached
TOP-3          →  EMPTY
```

**Fewer than 3 candidates survive; 0 survive. Stated plainly, and NO filter was relaxed to fill the
slate** (R-L73-1's own instruction). `filters_relaxed: false` is asserted in the artifact.

### 3.4 The counterfactual rank — run anyway, clearly labelled, so the HALT is actionable

Rule 3 + rule 4 were computed for all 20 runs *as if* filter 2 had passed, purely so the conductor can
see what the criterion would have selected. **This is NOT a slate and must not be read as one.**

Wall detection per math note § C.4: `trailing5_median(i) = median(c[i−5..i−1])`, `ratio(i) = c[i] / trailing5_median(i)`,
`W* = argmax ratio`, wall ⟺ `max ratio ≥ 1.5`.

| rank | run | W* | clear @ W* | trailing-5 median | ratio | wall ≥ 1.5 | W* in band | uptime % |
|---:|---|---:|---:|---:|---:|---|---|---:|
| 1 | `E-s01-cp150` | **156** | 25.0 | 12.0 | **2.0833** | ✔ | ✔ | 90.68 |
| 2 | `E-s03-cp150` | **156** | 24.0 | 12.0 | **2.0000** | ✔ | ✔ | 91.21 |
| 3 | `E-s08-cp150` | **156** | 25.0 | 13.0 | **1.9231** | ✔ | ✔ | 90.62 |
| 4 | `E-s07-cp150` | 156 | 25.0 | 14.0 | 1.7857 | ✔ | ✔ | 90.80 |
| 5 | `E-s02-cp150` | 156 | 26.0 | 15.0 | 1.7333 | ✔ | ✔ | 90.84 |
| 6 | `E-s05-cp150` | 156 | 25.0 | 15.0 | 1.6667 | ✔ | ✔ | 90.20 |
| 7 | `E-s04-cp150` | 167 | 28.0 | 14.9 | 1.8750 | ✔ | ✘ (>160) | 90.95 |
| 8 | `E-s06-cp150` | 167 | 29.0 | 16.0 | 1.8125 | ✔ | ✘ | 91.25 |
| 9 | `E-s09-cp150` | 161 | 21.0 | 12.0 | 1.7500 | ✔ | ✘ | 91.49 |
| 10 | `E-s10-cp150` | 167 | 29.0 | 17.0 | 1.7059 | ✔ | ✘ | 91.38 |
| 11–20 | all `*-w1` | **13** | 34–41 | 12–13 | 2.6429–3.2308 | ✔ | ✘ (fails filter 1) | 92.4–93.0 |

Rule 4 floor (uptime ≥ 60 %) passes 20/20 — range 90.20–92.95 %; aura reservation 982.0 absolute,
constant on every sample of every run, **100 % of alive-time on 20/20**. RF stacks are STRUCK from the
class per § 4.5 (RF DISSOLVED at Phase B); the fixture carries none, and none was evaluated.

⚑ **And the counterfactual is where the substantive problem shows.** See § 5, F-6 and F-7: the
detected wall is nearly seed-invariant, and it sits on the **wrong wave** relative to the only field
measurement of that band that exists.

---

## 4 · Beat-5 binding-term census (R-L68-2 / R-L73-1 clause 4)

Composition law: `clear_time ≈ MAX(last_arrival, cumulative_kill) + tail` (§ 10.9a E), measured per
wave, never assumed. **1,130 wave-instances censused.**

| Config | wave-instances | binds `last_arrival` | binds `cumulative_kill` | mean eHP coverage |
|---|---:|---|---|---:|
| wave-1 (waves 1–93), MEASURED band-A eHP | 930 | **892 (95.9 %)** | 38 (4.1 %) | **100.0 %** |
| checkpoint-150 (waves 151–170), r2 board | 200 | **170 (85.0 %)** | 30 (15.0 %) | **11.2 %** |

**Waves that EVER bind `cumulative_kill`:**

- wave-1 config: **{25, 55, 65, 70, 84, 89, 90}**
- cp150 config: **{160, 165, 170}**

**Waves with MIXED binding across the 10 seeds** (the term flips seed-to-seed): **{25, 55, 70, 84}** —
all in band A. **Waves binding `cumulative_kill` on every one of the 10 seeds:**
**{65, 89, 90, 160, 165, 170}**.

⚑ **Reading, MEASURED.** The kill term binds where and only where the body count collapses: w89 (6
bodies), w90 (2), w160 (5), w165 (5.9), w170 (4). Everywhere else — 92.2 % of all wave-instances —
**clear time IS arrival time.** On the cp150 band this is largely the § 5 F-1 absence wearing a
census costume: mean eHP coverage there is **11.2 %**, and the three `cumulative_kill` waves
{160, 165, 170} are exactly where the wave-160 r2 board's roster overlaps the rolled board.

L-68's band-A finding is **corroborated and extended**: under the MEASURED stat fold + SHEET limb the
two terms do separate on band A, and the flip at w90 reproduces (10/10 seeds). This is the first
end-to-end 93-wave band-A ladder run under both, and it is the substantive product of this lap.

---

## 5 · Findings

### F-1 · MEASURED opposition eHP does not exist on the target band — MEASURED

`ehp_lookup(w)` returns 968 records at `w = 93` and **raises `ValueError` for every `w ≥ 94`** (F-7's
raise, working exactly as built). The only band-B eHP is the 36-entry wave-160 r2 board, whose
coverage over [151,160], measured on this batch's own 10 seeds:

```
w151  0/211  0.0%     w156  0/141  0.0%
w152  0/143  0.0%     w157  0/164  0.0%
w153  0/189  0.0%     w158  0/266  0.0%
w154  3/ 95  3.2%     w159  0/ 74  0.0%
w155  0/149  0.0%     w160 40/ 40 100.0%      BAND: 54/1850 = 2.92%
```

40 of 43 covered instances (at 8 seeds) are wave 160 itself — the board *is* the wave-160 roster. **On
eight of the ten band waves the kill term is a declared zero and the clear time is pure arrival.**

### F-2 · Player death is structurally unreachable — MEASURED by enumeration

0 emitters of `player_death` (the string occurs once, in the `EVENT_TYPES` frozenset) · 0 rows with
`target_id="player"` · 0 writes to `hp_player` after initialisation · monster attack model
`abstract-schedule`, emitting no monster-side damage at all. The player-HP track is flat **by design**
(`run.py:107` — *"a player HP track that moved would be inventing intake"*). Filter 3's second limb
(*death within 3 waves of the slowest cleared wave*) is evaluated and reported `False` **with its
reason**, never silently dropped.

### F-3 · Ladder-exhaustion is unreachable — the arena runs out of geometry first — MEASURED

`ARENA_S2` (`sm1/survivalworld_a`) carries p01 placements for tiers 1…17 → highest simulable wave
**170**. `ARENA_S1` (`sm_mod/survivalworld_f`) carries tiers 1…15 → highest wave **150**. Tiers
18/19/20 raise `KeyError` on both. `MAX_WAVE = 200` is the ladder's measured length (R-KC2-4); it is
not a length this geometry can express.

### F-4 · A wave-1 start cannot reach the band on its own arena — MEASURED

Tier 16 is absent from `ARENA_S1`, so an s1 run stops at wave 150 — one wave short of the band.
Substituting `ARENA_S2` mid-run is the pooling L-21 forbids: `Arena.merge` raises
`"pooling arenas 's1' and 's2' is a spec violation (L-21)"`. **Half the pre-registered population
cannot satisfy filter 1 for a reason that is geometric, not stochastic.**

### F-5 · The emit-stub is NOT reachable at `build_baton` grain — MEASURED, and it is a seam boundary

Discharged at the reachable grain: `KC2Run.validate()` (the § 11.3.1 source-side obligations),
`EVENT_COLUMNS` / `EVENT_TYPES` conformance, and the tree-state grade under `code-surface-v2`
(**`clean`**). All PASS on 20/20.

A full `build_baton` + `baton_v1_validator` pass was **not** reached: no `KC2Run → run_record` adapter
exists, and by set-difference against the schema the `Actor` model carries **four required fields with
no supplier on the sim surface** — `archetype_tag`, `level`, `spawn_heading_rad`, `threat_tier` — plus
two derivable-but-unwired (`spawn_tick`, `life_modifier_pct`) and one on `Wave` (`nemesis_wave`).
Supplying `threat_tier` / `archetype_tag` / `level` would mean **inventing** classifications the roster
does not carry (`level` is a floor SET per the C-1 prescription — a caller wanting one number must
*pick an end*, and the pick goes on the record). Not done. § 11 is star-lord's seam and `run.py`'s own
docstring says this module *"builds the SURFACES, not the emitter."* **Routed, not patched.**

### F-6 · ⚑ The rule-3 wall is ~seed-invariant — the rank discriminates WAVES, not RUNS — MEASURED

`W* = 13` on **10/10** wave-1 runs. `W* = 156` on **7/10** cp150 runs (the other three: 161, 167, 167).
Measured dispersion:

```
between-SEED per-wave CV      median 6.4 % (cp150) / 6.9 % (wave-1),  max 14.2 %
between-WAVE spread in band   11.2 s (w159)  …  24.9 s (w156)   =  2.2×
```

The clear-time profile is **wave-determined**. The § 4.5 rank orders the 10 band-reaching runs on a
quantity whose seed-driven variation (~3–7 %) is an order of magnitude below its wave-driven variation
(~120 %). Ranking 20 runs on it selects **noise around a fixed calendar**, not distinct narratives.
The counterfactual top-3 (§ 3.4) are separated by ratios 2.0833 / 2.0000 / 1.9231 — a 7.7 % spread,
comfortably inside the 12.1 % per-wave CV measured at w154.

### F-7 · ⚑ The sim's wall sits on the WRONG WAVE relative to the only field measurement of the band — MEASURED

Against `MEASURED_S2_CLEAR_S` (galadriel § 2.2, sitting 2 — the field's own clear times):

| wave | fixture s | sim mean s | delta |
|---:|---:|---:|---:|
| 151 | 16.28 | 19.00 | +2.72 |
| 152 | 16.45 | 13.20 | −3.25 |
| 153 | 14.78 | 17.40 | +2.62 |
| 154 | 14.13 | 13.50 | −0.63 |
| 155 | 16.33 | 11.80 | −4.53 |
| 156 | 20.22 | **24.90** | +4.68 |
| 157 | 19.13 | 13.00 | −6.13 |
| 158 | 13.18 | 13.30 | +0.12 |
| 159 | **26.25** | 11.20 | **−15.05** |

```
fixture's wall in [151,160]  =  w159  @ 26.25 s
sim's     wall in [151,160]  =  w156  @ 24.90 s        ← what § 4.5 rule 3 would rank on
sim at the fixture's wall    =  w159  @ 11.20 s        ← the band's LARGEST miss, −15.05 s
w160 (fixture: death-in-progress, 104.73 s, NOT a clear)  =  sim 16.50 s
```

The `sim ≤ fixture` tripwire fires on **5 of 9** band waves {152, 154, 155, 157, 159}. Its attribution
is already on record in `s2_second_geometry_diagnostic`: the sim's kill term is a declared zero here
(11.2 % coverage), so the sim's clear time is pure arrival while the fixture's contains kill — **the
tripwire cannot discriminate on this band.**

**Consequence for the commission:** had filter 2 been satisfiable, § 4.5 would have handed Matt a
top-3 whose narrative peak sits at w156 while the field's peak sits at w159, and whose reading of the
wave that *actually killed the player* (w160, 104.73 s) is 16.5 s. That is precisely the hazard L-73(k)
named — *"a batch ranked on stale physics would hand Matt a top-3 the emit then invalidates."* The
physics is not stale; it is **absent on this band**, which is the same failure by a different route.

### F-8 · Declared simplifications introduced by the run-composition law (math note § C)

Energy and channel state do **not** cross a wave boundary — `simulate_wave` re-initialises energy to
the 1,594.0 usable ceiling and opens a fresh channel per wave. The energy error is **one-signed and
favourable to the player**, so the `energy < 0` flag is *harder* to trip under it than under a carried
pool. `run_tick` does chain (monotonic run-wide, § 11.3.1(2)). Declared, signed, left alone — carrying
energy across the boundary is a mechanism change, and R-L73-1 pins the parameters.

### F-9 · Nothing was repaired mid-batch

Zero anomalies arose, so the rule was not exercised — recorded so its non-exercise is a stated fact
rather than an inference from silence.

---

## 6 · HALT back to the conductor

**HALT-CLASS.** The § 4.5 composition cannot produce a top-3 from this model, and the brief forbids
relaxing a filter to fill the slate. The blocking condition is **filter 2's terminal-state clause**
(§ 3.2): its admissible set has an empty intersection with the reachable states. F-6 and F-7 are the
reason the conductor should want a ruling rather than a workaround — even with filter 2 set aside, the
rank would select on a quantity that is ~95 % wave-determined and whose peak disagrees with the field.

The decision is the conductor's / Matt's, not mine. Three forks are visible from the seam; **none is
taken here**, and each is stated so it can be challenged rather than adopted:

- **F-KC2-E-1 — re-scope filter 2's terminal clause** to the terminals this model *can* reach
  (`ehp_band_exhausted`, `arena_tier_exhausted` as ADMISSIBLE-BY-DECLARATION). Cheapest; costs the
  clause its meaning, because an instrument bound is then a legitimate ending.
- **F-KC2-E-2 — close the band-B eHP absence** (the C-1 / F-L7 lineage: a band-B `G` array and a
  151–170 roster board). Makes F-1, F-6 and F-7 all move at once, because all three are the same
  absence seen from three angles. Largest, and the only one that makes the rank mean what its name says.
- **F-KC2-E-3 — re-pin the band** to [1, 93], where MEASURED eHP exists at 100 % coverage, the kill
  term genuinely binds on {25, 55, 65, 70, 84, 89, 90}, and the wave-1 config already produces 10 clean
  93-wave runs. Costs the run its s2 field-anchoring; gains a band the physics can actually answer.

**No mechanism was changed and no pin was moved this lap.** The math note, driver, artifact and this
note are the record.

---

## 7 · Grade vocabulary (R-KC2-7)

Every quantity in §§ 1–5 is **MEASURED** — an instrument read against engine `40a269dd`, reproduced by
the driver's own § B probes at execution so this note and the run cannot drift. § 3.4 is a
**COUNTERFACTUAL** and is labelled as one at its head. § 6's three forks are **NAMED, NOT TAKEN**.
Nothing here is "verified" or "confirmed"; those words carry a rubric this lap does not run.

---

**Commit:** engine `40a269dd` (math note + driver, pre-execution) + the artifact commit carrying
`output/kc2-phase-e-seeded-batch-full-20260808_205104.json`; meta repo carries this note.
**COMMIT-ONLY, NO PUSH** (R-KC2-10 — the conductor's pushes carry these as passengers).
