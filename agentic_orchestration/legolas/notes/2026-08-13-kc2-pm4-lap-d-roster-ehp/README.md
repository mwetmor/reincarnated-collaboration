# KC2-PM4 · iteration I-1 · Lap D — every monster in band B gets its body back

> **Run:** KC2-PM4 (replicate waves 150–160 faithfully) · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-13
> **Charter:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md`
> **The finding this lap closes:** gamora's PM-3 landing note § 5 — *182 of 188 band-B bodies enter
> `hp_max = 0.0`, die to the first disc tick, and yield zero ADCtH.*
> **Status:** COMPLETE. **Coverage 100 % on every declared population.** Three conductor hooks all
> PASS. **Two defects found in the sim's existing band-B consumption, and three in the instruments
> I inherited — including two of my own.** Zero estimated magnitudes anywhere (GL-12).

---

## 0 — The one-paragraph answer

**Band B's life surface was never missing from the corpus; it was missing from the table.** The
same four-link chain that closes band A closes band B unchanged — only the wave index moves — and
it reproduces **all six** already-covered bodies **exactly, to the integer**, including
`F1 = 3,722,896`, `F2 = 2,955,796` and `F3 = 2,295,755`, the three fingerprints the § 6.2b chain
was ruled on. Coverage over PM-3 § 5's own population goes **6/188 actors (3.2 %) → 188/188
(100 %)**; over the full 20-wave roll **344/344**; over the band-B pool **663/663**; over the
summon-closed population **790/791**, the one hole a NAMED GAP with zero magnitude. Waves 151–160
carry **Σ eHP 117,203,808** where the sim had **18,923,016** — **×6.2** — and at the sim's *own*
run-of-record kill term that board costs **185.0 s of pure disc contact against the reference's
measured 186 s**. The board the sim was fighting was 96.8 % empty; it is not empty now.

---

## 1 — Deliverables

All four emissions are **source-of-record here**; gamora vendors byte-identical copies into
`reincarnated-engine/data/kc2/` and SHA-pins them (the established lane — `opposition.py`'s own
comment: *"Vendored byte-identical from the meta-repo emissions"*).

| # | file | rows × cols | sha256 | what it is |
|---|---|---:|---|---|
| 1 | `pm4d_band_b_monster_life.csv` | 791 × 33 | `8fa5279a…` | **the life table.** Band-A schema, extended. Record grain, lo/hi level limbs, anchors at w151 / w160 / w170 |
| 2 | `pm4d_band_b_ehp_by_wave.csv` | 15,801 × 8 | `3e82e72b…` | **the sim-consumable drop.** `(record, wave) → (ehp_lo, ehp_hi)`. Loads straight into `hp_lookup` |
| 3 | `pm4d_band_b_life_by_level.csv` | 1,812 × 8 | `adfec980…` | `(record, charLevel) → base_life, passive %, eHP`. For a consumer that knows an actor's own level |
| 4 | `pm4d_band_b_wave_life_modifier.csv` | 20 × 4 | `9d276ddb…` | `G` per wave 151–170, decoded, + `M` without passives |

**Recommended vendor names** (gamora's call): `pm4_band_b_monster_life.csv`,
`pm4_band_b_ehp_by_wave.csv`, `pm4_band_b_life_by_level.csv`, `pm4_band_b_wave_life_modifier.csv`.

**Instruments** (in `agentic_orchestration/research/scripts/`, declared schemas in their
docstrings): `pm4d_lib_2026_08_13.py` · `pm4d_emit_2026_08_13.py` · `pm4d_verify_2026_08_13.py`.
Run logs: `emit.log`, `verify.log`. Machine summaries: `pm4d_emit_summary.json`,
`pm4d_verify_summary.json`.

### How gamora consumes #2

```python
hp_lookup = {rec: ehp_lo for (rec, w), (ehp_lo, ehp_hi) in table.items() if w == wave}
```

`ehp_lo` is the **LO limb**, which is the limb the baton already declares
(`DECLARED-LEVEL-LO-LIMB`, F5-A → LO: *`L` is a floor SET, never a midpoint, and the life
equations are convex in `L`*). `ehp_hi` is emitted beside it so the bracket is a **choice**, not
an artifact — see § 5.2, where it is currently an artifact.

---

## 2 — The chain (band A's, verbatim; one index moves)

```
base_life(L)   = bio.characterLife                     evaluated at charLevel = L
passive_pct(L) = Σ_i  skill_i.characterLifeModifier[ int(skillLevel_i(L)) − 1 ]
Σ(w, L)        = 580.0  +  G[w−1]  +  passive_pct(L)
eHP(w, L)      = floor( base_life(L) × (1 + Σ(w,L)/100) )        ← floor, NOT round
```

- `580.0` = `balancingadjustment_mp+difficulty_enemies01.characterLifeModifier[8]` (Ultimate/solo)
- `G` = `balancingadjustment_survivalmode_enemies03.characterLifeModifier`, at index `w−1` under
  the § 10.7 / L-33 **array-lookup law** (fighting wave `w` reads the cell **labelled** `w`)

**The instrument does not re-implement this.** It *imports* `resolve` / `Chain` / `ev` from
`gamora_kc2_c1_closure_ed3_2026_08_08.py` and `lv_formula_table` / `floor_set` /
`pool_slot_proxies` / `APL_B_PRIME` from `gamora_kc2_stat_fold_ed3_2026_08_08.py`. A second
implementation of the same chain is a second thing that can drift — gamora's rule at the band-A
lap, and it binds here. Consequence: the reader is `Ed.winner()` (**whole-record replacement**,
the L-33/C-9 overlay law), not a field merge.

**The creature's own `characterLifeModifier` is emitted but NOT folded** — band A does not fold
it either, and L-33(b) falsified it on camera (`own_applied = NO` on every r2 row). It rides as a
column so the exclusion stays inspectable.

### The constants, decoded first-hand (GL-12 — the citation was checked, not trusted)

| | |
|---|---|
| `survivalmode_enemies03.characterLifeModifier` | **200 cells**, archive `sm_mod` |
| G(150) … G(170) | **304 → 344** — the playtest-directions v3 citation **CORROBORATED from the record**, not adopted from it |
| G over band B | 151:306 152:308 153:310 154:312 155:314 156:316 157:318 158:320 159:322 **160:324** 161:326 … 170:344 |
| Ultimate cell `[8]` | **580.0**, archive `base` |
| ⚑ **G(171) = 420.0** | a **+76 pt discontinuity** at the tier-17/18 boundary. Band B stops at 170. Extrapolating one wave past it is a different board, and the table refuses to. |
| `halt9_survival_wave_scaling_full.csv` (gladiator) vs this decode | **200/200 cells identical** — the CSV is checked *against* the decode, which is the opposite direction of trust |

---

## 3 — Populations (NOTE-9: every count in this lap names what it counts over)

| id | basis | records | actors |
|---|---|---:|---:|
| **P-ROLLED-10** | frozen baton `…-20260809_052836.json`, `actors[]`, wave ∈ [151,160] | 91 | **188** |
| **P-ROLLED-20** | same baton, wave ∈ [151,170] | 169 | 344 |
| **P-POOL** | `pe6_crucible_wave_pools_v2.csv`, `roster_records ∪ champ_records`, `global_wave ∈ [151,170]` | **663** | — (174 pools) |
| **P-CLOSED** | P-POOL + summon closure to **fixpoint** | **791** | — (+128 summon bodies, layers [123, 5]) |
| **P-PM3** | union of the five PM-3 fight batons | 55 | — |

- **P-ROLLED-10's 188 actors reproduce PM-3 § 5's published 188 exactly**, and its 6 covered
  actors reproduce PM-3's published 6. The population is confirmed, not assumed.
- **P-ROLLED-20 \ P-POOL = 0** — every rolled record is in the pool population, so a re-roll under
  a different seed stays covered.
- **P-PM3 ⊆ P-ROLLED-20 = True.**
- `_actors_ ≠ _records_` throughout: 188 actors are 91 distinct records; PM-3's "6 (3.2 %)" is
  **6 actors of 188**, which is **5 distinct records**. Both numbers are correct; they answer
  different questions, and this lap prints which.

---

## 4 — Coverage and grades

| population | MEASURED records | MEASURED actors |
|---|---|---|
| **P-ROLLED-10** (PM-3 § 5's own) | **91 / 91 = 100.00 %** | **188 / 188 = 100.00 %** |
| **P-ROLLED-20** | **169 / 169 = 100.00 %** | **344 / 344 = 100.00 %** |
| **P-POOL** | **663 / 663 = 100.00 %** | — |
| **P-CLOSED** | **790 / 791 = 99.87 %** | — |

**⚑ PM-3 § 5's headline, before → after: 6/188 (3.2 %) → 188/188 (100 %). 182 bodies that entered
with `hp_max = 0.0` now do not.**

### Grade distribution (P-CLOSED, n = 791)

| grade | n |
|---|---:|
| `life_grade = MEASURED` | **790** |
| `life_grade = ABSENT:NO-characterAttributeEquations` | **1** |
| `level_grade = MEASURED-SET` (band-B pool slot, index-paired slot law) | 663 |
| `level_grade = DERIVED-INHERITED` (summon body inherits its summoner's set) | 128 |

**THE ONE NAMED GAP, in full:**
`records/skills/nonplayerskillsgdx1/bossskills/pets/krieg_aethertrap.dbr` — `Class = Monster`,
reached through the summon closure, but the record carries **no `characterAttributeEquations`**,
so there is no bio, no `characterLife` equation, and therefore **no life**. It is emitted as a row
with every magnitude column **empty**. GL-12: it is not estimated, not sibling-filled, not
modal-filled. It is one body in 791 and it is not in any rolled population.

### Sanity of the numbers

- 259 distinct bios · 143 distinct `characterLife` equations over 790 rows.
- eHP at wave 160, LO limb: min **150** · median **450,012** · max **3,879,847** (P-CLOSED).
- Over P-ROLLED-10's 91 records: min **33,207** · median **450,012** · max **3,722,896**.
- charLevel range across band B: **102 … 109**, floor-set widths {1:19, 2:503, 3:136, 4:5}.

---

## 5 — The conductor's three hooks

### (a) Coverage vs the 188 rolled — **PASS**

Rolled-set basis declared in § 3. `188` and `6` both reproduce PM-3's published figures from the
frozen baton's own `actors[]`. New coverage **188/188**.

### (b) Agreement on the 6 already-covered bodies — **PASS, 6/6, and it surfaced two defects**

| wave | record | sim `hp_max` | lap-D at that wave (lo / hi) | verdict |
|---:|---|---:|---:|---|
| 154 | `nemesis_beast_01_p1` | 2,955,796 | 2,924,379 / 2,924,379 | reproduces **at wave 160's G**, not at 154's |
| 160 | `nemesis_kymon_01` | 3,722,896 | **3,722,896** / 3,722,896 | **EXACT, LO limb** |
| 160 | `nemesis_wendigo_01` | 3,722,896 | **3,722,896** / 3,722,896 | **EXACT, LO limb** |
| 160 | `nemesis_aetherialvanguard_01` | 3,722,896 | **3,722,896** / 3,722,896 | **EXACT, LO limb** |
| 160 | `statue_korvaaktombguardian` | 2,399,266 | 2,295,755 / **2,399,266** | EXACT on the **HI** limb |
| 160 | `statue_korvaaktombguardian` | 2,399,266 | 2,295,755 / **2,399,266** | EXACT on the **HI** limb |

Nothing was silently overwritten. Both non-trivial matches are **findings**:

**⚑ D-1 — the wave-160 board is applied at every wave 151–160.**
`gamora_kc2_pm3_fight_v2_2026_08_12.py` builds **one** `board160` dict (line ~169) and hands it to
every band-B wave (line ~184). `nemesis_beast_01_p1` rolled on **wave 154** (G = 312) but entered
with the **wave-160** value (G = 324). The sim **overstated that body by +1.07 %**. Small on one
body; **structural on 188**, and it is exactly the F-2-class regression `monster_stats._g_band`
raises to prevent — a wave-indexed value consumed as if it were a constant. Emission #2 is
per-wave precisely so this closes.

**⚑ D-2 — the band-B limb is CSV-order-determined, not ruled.**
`{e.record: float(e.ehp) for e in op.load_wave160_board()}` is a dict over a CSV that carries
**7 records on more than one row** (15 rows collapsing to 7): `statue_korvaaktombguardian` ×3,
`nemesis_wendigo_01` ×2, `wendigocannibal_h01…h05` ×2 each. The surviving row is **whichever is
last in the file**. For the Steward that is the **L = 108 HI limb** (2,399,266) while the baton
declares `DECLARED-LEVEL-LO-LIMB (F5-A → LO)` — the LO row is 2,295,755, **−4.31 %**. The three
r2 rows are `charLevel` 106/107/108 of one body, and **this lap reproduces all three exactly**
(2,295,755 / 2,345,066 / 2,399,266), which is what makes the collapse legible. Emissions #1–#3
carry both limbs explicitly so the pick becomes a ruling.

### (c) Wave-160 Σ eHP vs 15,967,220 across 5 bodies — **PASS**

| | bodies | Σ eHP |
|---|---:|---:|
| PM-3 § 5 published | 5 | **15,967,220** |
| the sim's own wave-160 actors | 5 | **15,967,220** ← **AGREES** |
| lap-D, HI limb | 5 | **15,967,220** ← **reproduces exactly** |
| lap-D, LO limb | 5 | 15,760,198 (−1.30 %, and the −1.30 % *is* D-2) |

Wave 160 was already fully covered, so board growth there is **×1.00**. The change is everywhere
else.

---

## 6 — What the covered board is worth (P-ROLLED-20 actors)

| wave | G | actors | sim bodies | Σ sim | Σ lap-D lo | Σ lap-D hi | ×lo |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 151 | 306 | 28 | 0 | 0 | 7,346,927 | 7,542,838 | ∞ |
| 152 | 308 | 18 | 0 | 0 | 10,682,643 | 11,042,012 | ∞ |
| 153 | 310 | 24 | 0 | 0 | 9,514,571 | 9,827,431 | ∞ |
| 154 | 312 | 13 | 1 | 2,955,796 | 12,743,291 | 13,169,327 | 4.3 |
| 155 | 314 | 18 | 0 | 0 | 12,778,568 | 13,207,742 | ∞ |
| 156 | 316 | 19 | 0 | 0 | 14,224,630 | 14,796,916 | ∞ |
| 157 | 318 | 21 | 0 | 0 | 11,045,967 | 11,404,179 | ∞ |
| 158 | 320 | 33 | 0 | 0 | 7,527,326 | 7,722,749 | ∞ |
| 159 | 322 | 9 | 0 | 0 | 15,579,687 | 16,282,784 | ∞ |
| **160** | 324 | 5 | 5 | 15,967,220 | 15,760,198 | 15,967,220 | 1.0 |
| 161–170 | 326–344 | 156 | 6 | 22,337,376 | 146,682,356 | 151,228,159 | 6.6 |
| **TOTAL** | | **344** | **12** | **41,260,392** | **263,886,164** | **272,191,157** | **6.4** |

**⚑ Waves 151–160 — PM-3's band: Σ 18,923,016 → 117,203,808 = ×6.2.**

### The arithmetic consequence (§ V-g) — **division, not a prediction**

At the sim's own **run-of-record** player limb (`PLAYER_DAMAGE_LIMB = SHEET_MEASURED`,
`gamora_kc2_phase_e_seeded_batch` line 77 — **not** the module default `DB_COMPONENT`):

| limb | dmg/tick | dps | contact s (sim board) | contact s (lap-D board) |
|---|---:|---:|---:|---:|
| **SHEET_MEASURED** ← the run of record | 51,726 | 633,644 | 29.9 | **185.0** |
| DB_COMPONENT (module default) | 334 | 4,092 | 4,625.0 | 28,645.7 |

**Reference truth, MEASURED (Lap C): ten waves 151–160 in 186 s. Lap-D pure contact: 185.0 s.
Ratio 0.99.**

**Read this carefully and do not over-read it.** 185.0 s is *pure disc contact* — it ignores
travel, arrival, overkill on the killing tick, pets, leech and death. The reference's 186 s is
*wall clock* and includes all of them. So the honest statement is directional, not confirmatory:

> the kill-throughput term moves from **6.2× SHORT** of what the measured curve demands to
> **flush against it, with every remaining term pushing the sim OVER**.

That inverts the sign of the queue's I-2. PM-3 § 3 concluded *"kill throughput was never the
survival constraint"* from a board that was **96.8 % empty**; on a full board the same
conclusion has to be re-argued, and the risk direction is now over-shoot, not under-shoot. **That
is gamora's fold to run and gandalf's to rule. I claim only the division.**

---

## 7 — Defects I found in the instruments I inherited, including two of my own

| # | id | what | how found | effect |
|---|---|---|---|---|
| 1 | **IS-B1** | **My own Lap-B reader is wrong for this chain.** `s2_lib.E3.merged()` does a last-wins **field merge**; L-33/C-9 ruled the overlay to be **whole-record replacement**. A merge *resurrects deliberately deleted fields* — exactly how Kubacabra's stripped death-spawn chain would have haunted the model. | diffing the two readers over P-ROLLED-20 before choosing one | **169/169 band-B records read differently** (e.g. `aetherialbloater_b01`: winner 975 fields, merge 985 — `lootMisc1Item1…4` and siblings resurrected). This lap uses `winner()`. The Lap-B roster *basis* is unaffected; only the *reader* changed. |
| 2 | **IS-B2** | **Band A's summon closure under-reaches.** `summon_targets` walks `buffSkillName`/`petSkillName` exactly **one hop**, never follows `autoCastSkill`, and never traverses a skill-record pet carrier. | running band A's closure and Lap B's pet chain over the same seed and diffing | band A's closure reaches **748** bodies on this seed and **misses 27 of Lap B's 70 measured pet bodies**. Extended closure reaches **791**. |
| 3 | **IS-B3** | **Admission by path, not by `Class`.** Restoring the two edges still missed 18 pet bodies, *all* under `records/skills/…/pets/` while carrying `Class = Monster`. **This is Lap B's own IS-3 finding, verbatim, unfixed in the band-A instrument.** | re-running the closure and reading the residual by path | admission is now the target record's own `Class`. `Class` census of the 43 added bodies: **{Monster: 43}** — no loot chest, no destructible, which is the other half of IS-3's warning. Pet coverage **70/70, residual 0.** |
| 4 | **D-1** | wave-160 board applied at every band-B wave (§ 5.b) | the agreement hook | one covered body overstated +1.07 %; structural across the band |
| 5 | **D-2** | band-B limb selected by CSV row order (§ 5.b) | the agreement hook | Steward enters on the HI limb, +4.51 % over LO, against a declared LO-limb ruling |
| 6 | **level fallback** | the baton's `actors[].level` is a **fallback** on 176/344 actors — `_BAND_B_MODAL_LEVEL = 109`, emitted with `False` and declared as `DIV-LEVEL-COVERAGE`. | checking derived level sets against the baton's | over P-ROLLED-20's 169 records, **93 carry a baton level OUTSIDE the derived set** (all of them 109 against sets like {107,108} or {103,104}). **This lap supplies the missing source: 663/663 MEASURED-SET + 128 DERIVED-INHERITED.** |

Also re-checked rather than carried: **R-L65-1's floor-equivalence** — that `(a) apl = 100, floor,
+3` and `(b′) apl = 103.4, no offset` agree — was **re-run on band B's own 9 lv proxies**:
**identical 9, differ 0**. Band A proved it on 13 band-A proxies; that is not the same population,
and a carry-forward whose scope does not reach is exactly finding #69.

**Structural checks on the emission** (790 MEASURED records × 20 waves): monotone-in-wave
violations **0** · negative eHP **0** · `hi < lo` limb-order violations **0** · floor-not-round
re-derivation spot-check **200/200 EXACT** (re-derived from the wide table's own columns, so the
long table is graded against something other than itself).

---

## 8 — CLIFFS (filed, not improvised past)

### ⚑ CLIFF C-D1 — two folds on one board, and I do not rule it

Lap B's `pet_life_at_owner_level` = `floor(base × (1 + tree_pct/100))`. **It folds the granted-
passive term ONLY.** It does **not** fold the Ultimate cell (+580 %) and it does **not** fold the
Crucible wave term `G`. The roster chain folds both. Over the 149 pet rows this lap also covers,
at wave 160:

```
lap-D eHP / Lap-B pet life :   min 3.38    median 4.22    max 10.04
    aetherialcorruption_b03_summon    Lap-B  74,248    lap-D  282,675   ×3.81
    aetherialworm_b01_summon          Lap-B  74,221    lap-D  294,325   ×3.97
```

**Consequence if unresolved:** once I-1 lands, pet bodies become the **softest targets on the
board by ~4×**, and PM-3 § 10's note that *"CLUSTER's live set includes pets — they are the only
bodies on this board carrying real HP"* **inverts into its opposite**: the cluster policy would
start preferring pets for precisely the wrong reason.

**I have no measured evidence either way** on whether the Crucible applies its wave scaling to a
summoned body. So I do not rule it. This lap emits a **same-chain value for all 70 pet bodies**
(they are in P-CLOSED), so the conductor can rule in either direction from measured numbers rather
than from a preference. **Disposition: conductor.**

### CLIFF C-D2 — `G(171) = 420` (a +76 pt jump from `G(170) = 344`)

The tier-17/18 boundary. Band B as this lap defines it stops at wave 170 because the frozen baton
stops there (`arena_tier_exhausted`). The table **refuses** to extrapolate one wave past it, and
`G_at` raises rather than clamps. A future band must be decoded, not extended.

### CLIFF C-D3 — one record has `Class = Monster` and no bio

`krieg_aethertrap.dbr` (§ 4). Named, zero magnitude, in no rolled population. Closes only if the
record does.

### CLIFF C-D4 — this lap is the LIFE limb only

`damage_grade = NOT-IN-SCOPE` on all 791 rows. Band A's table carries a measured swing column;
band B's does not, because I-1 is *"give the monsters their bodies back"* and monster **damage** on
band B is a separate decode. It is a **named absence with a positive sign** (supplying it can only
raise monster output), and it belongs to the queue's I-2/I-5.

---

## 9 — Laws observed

- **READ-ONLY** on the vendor corpus, the engine tree, and every baton. Nothing outside this notes
  directory and `research/scripts/` was written. The four batons and both pool CSVs were read from
  bytes and never touched.
- **GL-12 decode-never-estimate.** Every magnitude in every emission traces to a `.dbr` field. The
  one unresolvable record is a NAMED GAP with empty magnitude columns. No sibling fill, no modal
  fill, no interpolation. The playtest-directions' `+304 → 344 %` citation was **re-decoded from
  the record**, not adopted; `halt9`'s CSV was **checked against** the decode, not trusted.
- **NOTE-9 basis discipline.** § 3 declares five populations by name; every ratio in this note
  names which one it is over, and actors are never silently reported as records.
- **Instrument schemas declared** in the module docstrings (`pm4d_lib` § IS-B1/IS-B2/IS-B3).
- **Cliffs FILED**, not improvised past (§ 8). C-D1 in particular is left to the conductor with
  the numbers on the table rather than resolved by preference.
- **Discipline #11** — three of the six defects in § 7 are in instruments I wrote or relied on,
  and one of them (IS-B1) is my own Lap-B reader.
