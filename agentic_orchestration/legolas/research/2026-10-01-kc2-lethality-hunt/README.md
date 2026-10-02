# Research — KC2 THE LETHALITY HUNT (the ×3) — 2026-10-01

**Mode:** A (analytical; primary-source binary decode + footage-trace audit)
**Commissioner:** gandalf (RUN-CONDUCTOR), Run KC2-PLAY, KP-202 (Matt Q97: *"Full GD rule + hunt the x3"*)
**Agent:** legolas (UNKNOWN-RESEARCHER) · **Access:** read-only everywhere (pack, oracle, port, vendor tree, save). Nothing tuned. Footage share **not needed** (the committed Lap-Q trace was sufficient).
**Labels:** DATAMINED (binary/records) · FOOTAGE (the referent trace) · SIM (oracle counterfactual) · INFERRED.

**Sources consulted**
- `x64/Game.dll`, Grim Dawn Edition IV (`~/Games/vendor/grim-dawn-edition-IV-20260929/`), 25,100 exports. Disassembly in `evidence/gamedll_composition_decode.txt`.
- Edition-II records (`records/game/gameengine.dbr`, the referent's skill/devotion/item records) via the S-1 `arz.py` reader.
- The referent HP trace `legolas/notes/2026-08-14-kc2-pm4-lap-q-heal-discriminator/pm4q_hp_trace.csv` (sha256 in `referent_audit.json`).
- Oracle `reincarnated-engine/src/reincarnated/simulation/kc2/` at engine `d2d9ee1f`: `threat.py` (`resolve_attack`), `offense.py`, `global_magnitude.py`, `c11a_corrections.py`. Harness: gamora `gamora_kc2_play_c11a_fold_pricing_2026_09_30.run_arm("PW-FOLDED")` + C-11 `_capture`.
- Lap M `pm4m_body_chain.csv` / `pm4m_candidate_table.csv`, Lap I `pm4i_wave_damage_modifier.csv`, Lap O `pm4o_trash_terms.csv`.
- Prior findings: C-8, C-10, C-11, C-11a, C-11b, C-11c, C-11d; gamora C-11 FINDINGS; gamora KP-201 range counterfactual.

---

## Summary

1. **Leg 1. The denominator is sound. It is not off by a large factor.** The referent's 1,605.6 hp/s reproduces exactly from the trace. One real error was found: a −3,637 HP **max-health step** was counted as intake (−1.45 %, so ×3.243 → ×3.291). Same-frame heal masking is **hard-capped at ×1.235** by the measured 60 Hz update grid and the decoded EoR tick cadence. Taking every candidate at its most generous, the floor is **×2.67**. FOOTAGE + DATAMINED.
2. **Leg 2. Found: the oracle composes damage in the wrong FORM** (DATAMINED, grade A).
   - In GD, `offensiveTotalDamageModifier` is **expanded into a per-type percent modifier on every damage type**, instant and DoT alike. Per-type percents are **added to the attribute-scaled base**: `row = base·(a + P/100)`.
   - The oracle multiplies them instead: `base · a · (1 + P/100)`.
   - On the attribute-folded bodies, the instant rows run **×1.5 (trash) to ×2.5 (nemesis)** too high.
   - The same rule makes the oracle's DoT rows **~×40–80 too LOW**, and it gives physical damage back to the bodies the oracle clamps to zero.
3. **The counterfactual applies GD's full composition rule, both directions** (SIM, NOT-A-GRADED-RUN, PW-FOLDED, salts 0–19):
   - The ratio falls from **×3.243 to ×2.24–2.26** (paired Δ −1.00 [−1.09, −0.92]).
   - The first death moves from **mean wave 154.3 to 159.0–159.2**. **15–16 of 20 salts now first die IN WAVE 160**, the referent's death wave; the other 4–5 still die at 156.
   - **The largest single correction any investigation has priced: it removes about a third of the gap in rate, and most of it in survival.**
4. **What remains (~×2.2 in rate):**
   - It sits on the same hero/champion/trash boards (w152 ×3.4, w158 ×8.5, w156 ×4.6).
   - At w160 the oracle player still dies 4–11 s in, against the referent's 29 s. That is the known zero-occupancy, zero-heal board (C-11 § 4, KP-100).
   - No player-side DR is missing from the referent's own records (§ 2.5).

---

## LEG 1 — Audit of the referent measurement (the denominator)

### 1.1 The method, located and reproduced (FOOTAGE)

- **Instrument.** Lap Q (legolas, 2026-08-14) OCR'd the player's HP readout (`x 520–780, y 996–1026`, the "HP/max" text on the health orb) at **60 fps**, `t 683.0–864.0`, on the referent MP4 (sha256 `4c60960d…`). That gave 10,861 frames, 100 % accepted against the decoded denominator 20,005.
- **Wave windows.** Lap H-2's boundaries (±0.25 s) tile the trace contiguously.
- **Rate.** gamora's C-11 harness (`referent()`) takes intake = Σ of **negative frame-to-frame HP deltas** in each wave window, divided by the window length. Pooled over 151–159 that is **250,475 HP / 156.0 s = 1,605.6 hp/s**. `tools/referent_audit.py` reproduces it exactly.

### 1.2 Candidate errors, each tested on the trace

| # | candidate | finding | effect on the referent rate | label |
|---|---|---|---|---|
| E1 | **max-health change counted as damage** | ⚑ **REAL.** Frame 1823 (`t 713.383`, w152): HP 20,005/20,005 → 16,368/16,368, Δ −3,637, both frames at full. This is Lap Q's `D-Q1` max-HP debuff, not damage. Its restore (+3,735 at `t 721.667`) was counted as heal. | **−1.45 %** (1,605.6 → 1,582.3); gap ×3.243 → **×3.291** (the gap WIDENS) | FOOTAGE |
| E2 | **heal not added back** (intake = loss + heal) | Does not apply. The estimator already sums gross decrements and never nets a wave. The only hidden intake is a hit and a heal in the **same frame** (E3). | 0 | FOOTAGE |
| E3 | **same-frame heal masking** (KP-135's "independence assumption") | **Update grid:** the HP text changes on consecutive frames (regen-drip gap of 1 frame: 1,584 times; no parity structure), so the coincidence window is one 1/60 s frame. **The heal source:** EoR ticks at ≤ 11.408/s (measured; inside Lap L's decoded bracket), so p(tick in a given frame) ≤ 0.190. The visible tick rate below full HP is 0.051/frame. **Cap:** even if every coincident hit were fully hidden, true ≤ measured/(1−0.19) = **×1.235**. C-11's independence estimate is ×1.151. | **at most +23.5 %** (realistic +5–15 %) | FOOTAGE + DATAMINED |
| E4 | **wave windows include idle time** | GD advances the wave ≤ 1 s after the last proxy kill (Lap S, `updatePeriod 1000`), and the oracle uses the same gate. Time at full HP at the end of waves sums to 12.9 s; excluding it gives 1,750 hp/s (×1.09). That is not a legitimate correction: the oracle's waves carry their own walk-in and tail. ⚑ **A matched window makes the gap WORSE.** Over the first 10 s of each wave the referent takes **1,338.6 hp/s** and the oracle 5,327 (**×3.98**). Bodies reach Matt late (first decrement at w152 is 10.5 s in; at w151, 5.3 s). | none owed | FOOTAGE |
| E5 | **absorption/barrier not counted** | The definitions match: the trace is HP after every absorber, and the oracle's "landed" is after counterplay absorption and overkill truncation (C-11 § 0). | 0 | FOOTAGE / SIM-code |
| E6 | **deaths/potions mis-attributed** | No death in 151–159; HP minimum 26.8 %. A potion appears as a positive step and only matters through E3. There are 4 one-frame dip-and-return events ≥ 200 HP (2,687 HP in 151–159), each consistent with a hit plus a tick that refills to the cap; they are not adjudicated as OCR errors (≤ 1.1 %). | ≤ −1.1 % if all were misreads | FOOTAGE |
| E7 | **health-bar read scale** | It is a text readout, not bar pixels. Denominator 20,005 = the decoded `health_max`, 100 % accepted. No scale term exists. | 0 | FOOTAGE |

### 1.3 Leg-1 verdict

- **Most generous true referent: 1,582.3 × 1.235 = 1,953.8 hp/s.** Against A0's 5,207.1 that leaves a **floor of ×2.67**. The denominator cannot carry the ×3.
- ⚑ **Side finding: the referent's "heal:intake = 1.01" is a telescoping identity, not a measurement.** Over any window that starts and ends at full HP, Σ increments − Σ decrements = net HP change ≈ 0 (`referent_audit.json` E4: heal − intake equals the net change on every wave). The referent's heal is also **overheal-censored**: a tick at full HP is invisible. So comparing it with the sims' *gross* heal:intake (port 24.1, oracle 72.5 in KP-96/98) compares two different instruments.

---

## LEG 2 — The total-damage composition layer (the numerator)

### 2.1 GD's composition, byte-decoded (DATAMINED, Edition IV `Game.dll`, grade A)

1. **`offensiveTotalDamageModifier` is not a total-layer multiplier.** The record field loads as `DamageAttributeAbsMod_TotalDamageModifier` (type `0x3c`; tag string read at `0x1801899c0`). Its `AddModifierToAccumulator` (`0x1801899d0`) pushes two kinds of object:
   - one `CombatAttributeTotalDamageMod`, whose `Execute` is the empty stub C-11a found. It is a bookkeeping object, so C-11a's "never touches a row" is true **of that object only**;
   - **eighteen value-identical per-type modifiers:** `CombatAttributeAbsDamageMod` for types {2 Physical, 4 Pierce, 5 Cold, 6 Fire, 7 Poison, 8 Lightning, 9 Life, 10 Chaos, 11 Aether}, and `CombatAttributeDurDamageMod` for DoT types {2, 5, 6, 7, 8, 9, 15 Bleeding, 10, 11}. The type ids come from every `DamageAttribute*::GetType` (the table is in the evidence file).
2. **These are the same objects a per-type modifier creates.** `DamageAttributeAbsMod::AddModifierToAccumulator` (`0x180177360`; e.g. `offensiveFireModifier`, `offensivePhysicalModifier`) pushes exactly one `CombatAttributeAbsDamageMod` of its own type. `CombatAttributeAccumulator::ModifyDamage` (`0x1801061c0`) Executes every modifier except type `0x3d` on every row, and each Execute adds its value into the row's percent field:
   - `+0x2c` for abs rows (`0x1801007e0`);
   - `+0x48` physical, `+0x4c` pierce ratio and `+0x50` pierce on `BasePhysical` (`0x1801042c0`);
   - `+0x34` on DoT rows (`0x180101240`).
3. **`Process` adds the percent term to the attribute-scaled base.** The percent term is computed on the **UNSCALED** base; then the attribute equation is applied; then the two are **ADDED**:
   - `AbsDamageElemental::Process` `0x180100a50`, magical equation `Character+0x748`;
   - `DurDamageElemental::Process` `0x1801015e0`, magical-duration `+0x750`;
   - `BasePhysical` (C-11a § 2.3);
   - then a clamp at 0.

   **Row = base·a + |base|·P/100**, where P is every percent that reaches the row's type: the Ultimate pak +40, the survival wave +42/43, the body's own TDM passives, grants, and per-type modifiers. **C-11a's § 2.3 form, which it graded B and scoped to "own", now holds for the whole pool. That closes C-11a's one open end (L-C11-3, A− → A) and removes the premise of the C3 HALT (KP-131): the TDM objects do reach the rows, and additively.**
4. Already folded or immaterial:
   - **The attacker's "reduced damage" debuffs** (`TotalDamageReductionPercent` `0x1c`, physical `0x1e`, elemental `0x1f`) compose by **MAX, not sum**: `v·(1 − max(%)/100) − abs`, in the same Process. War Cry −29 % therefore swallows EoR's own −20 % (`eyeofreckoning2`); the oracle's War Cry at 100 % uptime is already the ceiling.
   - **Crit:** `TakeAttack` adds `ParametersCombat+0xa0` (the sum of type `0x3b` `offensiveCritDamageModifier`) to the PTH multiplier **only on a crit**. The form is additive (Lap M's "×1.37" limb). Grade B: the unit of `+0xa0` was not traced. Immaterial, since crits are 1.2 % of hits (C-11).
   - **`offensiveDamageMultModifier`** (type `0x3d`) is the only true multiplier. `TakeAttack` applies `(100 + defender + attack)/100` only when the total exceeds 100.
   - Ruled out: `gameengine.dbr`'s `abs*MinScale 0.75 / MaxScale 1.15` are **hit-FX scalars**, loaded beside `absFireFx` / `absFireFxSound` in `Character::Load`. There is no `waveDamageModifier` in `tier16waves.lua` or `survivalevent.lua`, and no Champion/Hero damage multiplier in `gameengine.dbr` or either pak.

### 2.2 The oracle's composition, and the discrepancy (SIM-code)

`threat.py resolve_attack`, instant rows: `r.magnitude() * a_mult * om * t_mult * mult`. Here `om = M_inst + own + grant` (`offense.mult_for` + `gmag.own_add`) and `a_mult = (int/215)+1` or `(dex/245)+1`. Lap M had flagged this choice as **UNDECODABLE** (§ 6.5, limb C-M5); I-13 and I-14 adopted the multiplicative limb.

| body (examples, `pm4m_body_chain`) | int | P | oracle a·(1+P) | GD a+P | oracle ÷ GD |
|---|---:|---:|---:|---:|---:|
| `nemesis_outlaw_01` (w160) | 1,170 | 2.37 | 21.71 | 8.81 | **×2.46** |
| `nemesis_aetherial_01` (w160) | 1,170 | 1.52 | 16.23 | 7.96 | **×2.04** |
| `witchgod_finalboss` (w159) | 914 | 1.57 | 13.50 | 6.82 | ×1.98 |
| `wendigocannibal_h01` (hero) | 927 | 1.24 | 11.90 | 6.55 | ×1.82 |
| `ghost_b01` (w151 trash, Lap O) | 697 | 0.82 | 7.72 | 5.06 | ×1.53 |

**39 Lap-M bodies: ×1.78–2.46, median ×1.93.** Inert bodies (no attribute term) are unchanged.

Two further departures follow from the same decode, and both point **UP**:
- **DoT.** The oracle takes `r.lo · M_dot` with M_dot = 1 − 0.91 = 0.09 at w159/160 (`offense.py` § 3.1 chose this "LOWER reading"). GD gives DoT rows the attribute too (C-11a) and the TDM pool: `base·(a_dur + (−0.91 + 0.83 + own))`. That is ~×10 on inert bodies and ~×75 at int 1,170.
- **Physical.** The oracle zeroes Physical rows on `physical_clamped` bodies, because Lap M's type factor 1 + (−135 − 21 + 33)/100 = −0.23 is negative. In GD the −123 sits **in the same pool** as +83 + own, against base·a with a ≈ 5–6, so the leg survives.

### 2.3 Player-side defence chain (DATAMINED, referent records)

`tools/referent_player_dr_probe.py` scanned all 147 records the referent carries (allocated skills and devotions with their buff chains; equipped items with affixes and components). The output is `evidence/referent_player_dr_fields.txt`. Every damage-reduction-class field it found is already in the oracle:
- War Cry −25 % (−29 % with +skills), EoR2 −20 % (swallowed by the MAX rule);
- Ascension `damageAbsorption`;
- the Turtle (`tier1_29e_skill` 500 base) and barrier procs;
- `defensiveAbsorptionModifier` +5/+8/+12 (inside Lap X's +48 absorption stack in `intake.py`);
- armour.

There is **no `racialBonusPercentDefense`** (the only racial field is +6 % *offensive*). **No missing player-side DR exists.** This confirms C-11c.

### 2.4 Composition counterfactual (SIM, ⚑ NOT-A-GRADED-RUN)

**Harness.** `tools/composition_counterfactual.py` patches the source of `resolve_attack` at exactly five sites (`assert (4,1)`); everything else is the incumbent code.
- The A0 control reproduces exactly: ×3.1703 (salts 0–4), ×3.2431 (0–19), terminals `[156,152,155,152,152]`.
- The engine's kc2 code and data hash is identical before and after the run (`engine_unchanged_during_run: true`).
- Results: `composition_counterfactual_PW-FOLDED_salts0-19.json`.
- The Δ is a paired per-salt mean with a t95 interval (n = 20).

| arm | ratio ×ref | Δ vs A0 [95 %] | mean first-death wave | die in 151 | first death IN w160 | Leg-B deaths/salt | DoT share |
|---|---:|---|---:|---:|---:|---:|---:|
| **A0** control | **3.243** | — | 154.3 | 1/20 | 0/20 | 3.25 | 0.1 % |
| G-INST (instant, non-physical) | 2.502 | −0.74 [−0.84, −0.64] | 155.85 | 0 | 0 | 1.65 | 0.2 % |
| G-PHYS-LO (+ physical in the pool) | 2.045 | −1.20 [−1.29, −1.11] | 159.2 | 0 | 16 | 1.20 | 0.2 % |
| G-PHYS-HI | 2.060 | −1.18 [−1.27, −1.10] | 159.0 | 0 | 15 | 1.25 | 0.2 % |
| G-DOT (DoT only) | 3.462 | **+0.22** [+0.18, +0.25] | 154.2 | 2 | 0 | 3.40 | 4.8 % |
| **G-FULL-LO** (GD's rule, all limbs) | **2.239** | **−1.00 [−1.09, −0.92]** | **159.2** | 0 | **16** | 1.20 | 7.3 % |
| **G-FULL-HI** | **2.256** | −0.99 [−1.07, −0.90] | 159.0 | 0 | **15** | 1.25 | 7.3 % |

**Reading the table.**
- **The DoT half points UP, and it is carried, not dropped.** Selecting only the instant half would be fitting (Law 3); the FULL arms are the GD rule.
- **Non-160 deaths in the FULL arms** are on 4–5 salts at **w156** (chthonian herald chaos blasts).
- **Deaths at w160** come 4.0–11.0 s in, against the referent's 29.0 s.
- **Per wave, FULL-LO vs the referent:** 151 ×1.81 · 152 ×3.43 · 153 ×2.26 · 154 ×1.46 · 155 ×2.59 · 156 ×4.58 · 157 ×1.09 · 158 ×8.46 · 159 ×1.85 · 160 ×1.61. A0 was ×4.0 / 7.1 / 5.3 / 1.5 / 5.0 / 3.3 / 1.6 / 21.7 / 1.7 / 1.7.
- **LO/HI is the bracket for the 4.5k physical rows** whose body has no Lap-M type factor (unmapped f = −0.44 / −0.23). The bracket moves the ratio by 0.016.

**Declared, not encoded:**
- crit-damage composition (UP, ≤ +0.3 %);
- `DamageScaleInfo`;
- grant percents on DoT rows;
- SlowChaos/SlowAether `a_dur` (set to 1.0; its divisor is undecoded);
- Lap M's physical factors re-based from w160 by the survival physical term only;
- PCL untouched.

**Instrument failure, reported:** the "physical-tagged landed" column reads 0 in every arm, A0 included, while the pre-mitigation physical row total is 68 M HP. The `mitigation_source` tag it greps never carries "armor" under the intake fold. The column is blind and is not used.

---

## Most likely explanation of the ×3

1. **About a third of the rate gap and most of the survival gap (DATAMINED + SIM, high confidence):** the oracle multiplies the attribute limb by the total-damage pool where GD adds them. This is the "global-magnitude attribute limb" that C-11 found holding the whole surplus (ρ 0.177), which no scope correction could close.
   - The term was right; the **form** was wrong.
   - Corrected **in full** (DoT and physical included), the oracle player first dies **in wave 160 on 15–16 of 20 salts**, against the referent's 160.
2. **The residual ×2.2 (INFERRED; open):** it concentrates on w152/w156/w158, the hero/champion/trash boards.
   - At w160 the oracle still dies at 4–11 s against 29 s: the zero-occupancy, zero-heal board (C-11 § 4).
   - The denominator can take at most ×1.24 of it (Leg 1).
   - Leads, not findings:
     - per-wave **engagement onset**: the referent's first hit lands 3–10 s into a wave, and matched first-10-s windows give ×3.98;
     - the C-11b A+B attribute folds (sourced, +10 %, UP) are still unfolded;
     - the four unmodelled monster mutators (UP).

**Confidence.** The decode itself is grade A: instruction-level and cross-checked across four classes. The counterfactual is exact to the decoded form, but **Edition IV is the mechanism and Edition II/CRUCIBLE supplies the values** (the same caveat as C-11a). "The ×3 is mostly composition" holds at **moderate-high** confidence for survival, and **moderate** for rate, where ×2.2 remains.

## Knowledge gaps not resolved

- The unit of `ParametersCombat+0xa0` (crit damage).
- The `DamageScaleInfo[0]` caller argument (weapon-damage % of monster skills).
- The `a_dur` divisor for SlowChaos/SlowAether.
- Physical type factors for the ~4.5k rows whose body Lap M never composed.
- The referent's heal events at full HP (invisible by construction).

## Files

- `referent_audit.json` · `tools/referent_audit.py` — Leg 1.
- `composition_counterfactual_PW-FOLDED_salts0-19.json` · `tools/composition_counterfactual.py` — Leg 2 SIM.
- `evidence/gamedll_composition_decode.txt` · `tools/dump_composition_evidence.py` · `tools/gd_dis.py` — the decode.
- `evidence/referent_player_dr_fields.txt` · `tools/referent_player_dr_probe.py` — the player-DR census.
