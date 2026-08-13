# KC2-PM4 · iteration I-2 · Lap E — does the roster life fold reach a monster's summon?

> **Run:** KC2-PM4 (replicate waves 150–160 faithfully) · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-13
> **Charter:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md`
> **The cliff this lap closes:** Lap D **CLIFF C-D1** — *"I have no measured evidence either way
> on whether the Crucible applies its wave scaling to a summoned body. So I do not rule it."*
> **Status:** COMPLETE. **All three questions MEASURED — none declared.** Eight conductor hooks
> PASS. **Three defects found in instruments I inherited, two of them mine, one in Lap D.**
> Zero estimated magnitudes anywhere (GL-12).

---

## 0 — The one-paragraph answer

**Both folds apply, and the evidence was already sitting inside the positive control Lap D itself
used.** `t21_wave160_board_ehp_r2.csv` carries eight rows with an *independent* `measured` eHP —
and **four of those eight are skill-spawned pets.** Recomputed here from the corpus at their
camera-measured levels, all four reproduce their measured life **EXACTLY** under the full
`580 + G + passives` fold, and **every discriminating alternative fails**: drop the Ultimate cell
and the Death Revenant reads 227,820 against a measured 468,504; drop `G` and it reads 334,053;
use Lap B's passives-only rule and it reads **93,368 — 5.02× too soft**. So the answer to C-D1 is
not an argument from naming or from where a record lives; it is four bodies whose life was read off
the real game and which are reproducible **only** with both terms applied. The dispatch reason is
equally concrete: Grim Dawn binds its difficulty pak **by the body's `Class`**
(`gameengine.dbr:monsterAttributePak` / `petAttributePak` / `playerAttributePak`), and **all 128
summon-only bodies on this board carry `Class = Monster`** — the *same* class as the roster bodies
that summon them. A monster's summon is not a "pet" to this engine. It is a monster.

**Consequence:** pet bodies are **not** the softest targets on the board — the median pet hardens
**×4.20** against what the sim carries today, Lap D's ×4.22 is **corroborated on its own basis**,
and PM-3 § 10's inverted note un-inverts. **596 of the reference cell's 779 kills ride this
correction.**

---

## 1 — The three verdicts

| # | question | verdict | the evidence, in one line |
|---|---|---|---|
| **Q1** | does the **Ultimate +580 %** difficulty cell apply to monster-summoned pets? | **MEASURED-YES** | pak dispatch is by `Class`; 128/128 summon bodies are `Class = Monster`; and 4 camera-measured pets reproduce **only** with it (without it: −51 %) |
| **Q2** | does the **Crucible wave term `G`** apply to monster-summoned pets? | **MEASURED-YES** | the same 4 camera-measured pets reproduce **only** with `G(160) = 324` folded (without it: −29 %); the survival GameAdjustment has **no class dispatch and no pet variant** to exclude them with |
| **Q3** | what **level** does a summoned pet enter at? | **MEASURED-YES (owner's level), with ONE named dissenting body** | pet's own `charLevel` equation is **NOT** applied (Death Revenant `charLevel*1+2` and Aleksander's Shard `charLevel*1+3` both enter at **109**, their owners' level, not 111/112); no spawn-skill template carries a level field at all. The 4th control dissents — **CLIFF C-E1**, filed, not smoothed |

**The fold this lap rules correct is the roster chain, unchanged, with one index moved:**

```
base_life(L)   = bio.characterLife                    evaluated at charLevel = L
passive_pct(L) = Σ_i skill_i.characterLifeModifier[ int(skillLevel_i(L)) − 1 ]
eHP(w, L)      = floor( base_life(L) × (1 + (580.0 + G[w−1] + passive_pct(L)) / 100) )
                                     ↑ L = THE OWNER'S LEVEL, not the pet's own charLevel equation
```

---

## 2 — Deliverables

| # | file | rows × cols | sha256 | what it is |
|---|---|---:|---|---|
| 1 | `pm4e_pet_ehp_by_wave.csv` | 2,560 × 15 | `35d82158…` | **the sim-consumable drop.** `(record, wave) → (ehp_lo, ehp_hi)` over waves 151–170, `is_lapb_70` marks the commission's declared subset |
| 2 | `pm4e_pet_life_decode.csv` | 128 × 29 | `5595898c…` | **the evidence row.** Per body: `Class`, template, pak binding, summoners, level set, bio, life equation, limbs, Lap-B value, hardening ratio |
| 3 | `pm4e_positive_control.csv` | 4 × 14 | `0e6579c8…` | **the four camera-measured pets, recomputed FOUR ways.** This is the file the verdict stands on |
| 4 | `pm4e_dispatch_evidence.csv` | 6 × 6 | `2f5c0190…` | the decoded pak / GameAdjustment binding surface (L1 + L3) |

**Instruments** (`agentic_orchestration/research/scripts/`, schemas in their docstrings):
`pm4e_lib_2026_08_13.py` · `pm4e_emit_2026_08_13.py` · `pm4e_verify_2026_08_13.py`.
Logs: `emit.log`, `verify.log`. Machine summaries: `pm4e_emit_summary.json`, `pm4e_verify_summary.json`.

### How gamora consumes #1

```python
pet_hp = {rec: ehp_lo for (rec, w), (ehp_lo, ehp_hi) in table.items() if w == wave}
```

`ehp_lo` is the **LO limb**, carrying **R-PM4-2** (LO by explicit column selection, never row
order). Per-`(record, wave)`, carrying **R-PM4-1** — each pet enters at **its own wave's `G`**.

> ⚑ **The cheapest correct path is not to load this file at all.** HOOK-d shows Lap D's existing
> `pm4d_band_b_ehp_by_wave.csv` **already carries all 128 of these bodies at these values**
> (2,520/2,560 rows byte-identical). Lap D folded them; it just did not *rule* them. **This lap
> rules them.** The only reason to prefer #1 is the ⚑ D-E1 correction on one record (§ 6) and the
> `lapb_life` / `hardening_ratio_lo` columns. **Emitting a second table that must not drift from a
> first is a risk; the ruling is the deliverable, the CSV is the convenience.**

---

## 3 — The decode, link by link (every citation checked first-hand, none adopted — GL-12)

### L1 — the difficulty pak is dispatched **by the body's `Class`**, and the table is in the DB

`records/game/gameengine.dbr` carries **three** class-scoped bindings:

| field | → record | `characterLifeModifier[8]` (Ultimate/solo) | template description |
|---|---|---:|---|
| `monsterAttributePak` | `balancingadjustment_mp+difficulty_enemies01.dbr` | **580.0** | "AttributePak for monster bonuses" |
| `petAttributePak` | `balancingadjustment_mp+difficulty_pets01.dbr` | **15.0** | *(none)* |
| `playerAttributePak` | `balancingadjustment_mp+difficulty_players01.dbr` | 0.0 (scalar) | "Game Balance Attribute Pak" |

Both pak arrays are **12 cells = 3 difficulties × 4 player counts**. Descriptions decoded from
`database/templates.arc → gameengine.tpl`.

### L2 — the four body classes, and which one our pets are

`templates.arc` (818/819 templates extracted; the one failure is a nameless `entry_type = 0`
placeholder) gives four body templates, each declaring its `Class` as a static `defaultValue`:

| template | `Class` | includes |
|---|---|---|
| `monster.tpl` | **`Monster`** | `Character.tpl` |
| `pet.tpl` | `Pet` | `Monster.tpl` |
| `petnonscaling.tpl` | `PetNonScaling` | `Pet.tpl` |
| `petplayerscaling.tpl` | `PetPlayerScaling` | `Pet.tpl` |

**Measured over the corpus (Edition-III `winner()`):** `Monster` 3,780 · `PetPlayerScaling` 1,244 ·
`Pet` 765 · `PetNonScaling` 0. The `Pet*` records live under `records/skills/playerclass*` /
`devotion` / `itemskills` — **the player's summons**.

**Measured over this board:**

| population | `Class` census |
|---|---|
| the 70 pet bodies of `pm2_tg2_pet_chain.csv` | **`{Monster: 70}`**, `templateName = monster.tpl` on 70/70 |
| the corrected 128 summon-only bodies (§ 5) | **`{Monster: 128}`** |
| the 53 roster owners | `{Monster: 53}` |
| all 76 spawn targets incl. non-threat | `{Monster: 70, Destructible: 5, FixedItemContainer: 1}` |

⇒ **a monster's summon takes the same pak binding as the roster body that summoned it.**

### L3 — the survival term has **no class dispatch at all**

`records/game/survivalinfo.dbr` (14 fields total) binds exactly three adjustments —
`survivalAdjustment{Normal,Elite,Ultimate}` → `balancingadjustment_survivalmode_enemies0{1,2,3}.dbr`,
template description **"GameAdjustment"**. `survivalinfo.tpl` carries **no other adjustment field**:
**no pet variant, no player variant exists to exclude a summon with.** `gameadjustment.tpl` is
`attributepak.tpl` + four spawn-**count** fields (`spawnMinAdj`, `spawnMaxAdj`,
`spawnChampionMinAdj`, `spawnChampionMaxAdj`).

The only provenance-scoped opt-out in the whole corpus is **`ignoreGameBalance`**, which exists on
**exactly one template — `proxypool.tpl`** (1,877 records carry it: 1,402 False / 475 True). A pet
is spawned by a *skill*, never by a proxypool, so that field cannot address a summoned body in
either direction. (It bears on the **roster** instead — see **CLIFF C-E2**.)

### L4 — ⚑ THE POSITIVE CONTROL, AND IT IS THE WHOLE ANSWER

`data/kc2/t21_wave160_board_ehp_r2.csv` carries **39 rows: 31 `PREDICTION-uncorroborated`, 8
`EXACT` against an independent `measured` eHP.** **Four of the eight are
`proxy = "(none - skill-spawned pet)"`.** Recomputed here from the corpus through Lap D's imported
chain, at wave 160 (`G = 324`), `ULT = 580`:

| body | record | L | **measured** | **FULL fold** | no-Ultimate | no-`G` | Lap-B (passives only) |
|---|---|---:|---:|---:|---:|---:|---:|
| Death Revenant | `nemesis_orderdeathsvigil_01_revenantsummon` | 109 | **468,504** | **468,504 ✓** | 227,820 | 334,053 | 93,368 |
| Skeletal Archer | `skeleton_a02_summon` | 109 | **41,237** | **41,237 ✓** | 19,767 | 29,244 | 7,773 |
| Aleksander's Shard | `aetherialvanguard_crystal` | 109 | **103,912** | **103,912 ✓** | 50,529 | 74,091 | 20,708 |
| Aetherial Bileeater | `aetherialbloater_b01_summon` | 112 | **484,095** | **484,095 ✓** | 236,279 | 345,660 | 97,844 |

`charLevel_grade = MEASURED-CAMERA` on all four. **4/4 EXACT under the full fold; 0/4 under any
counterfactual.** A fold that matched under all four columns would prove nothing — the point of
the table is that three of the four columns are *wrong*.

⚑ **`Aleksander's Shard` is `aetherialvanguard_crystal` — the `devastationshard` source that dealt
9,923 of the 20,903 damage that killed the sim's player on wave 160 (I-1 § 5).** The body driving
the run's terminal event is one of the four bodies this verdict is measured on.

### L5 — the level source

- `character.tpl`'s `charLevel`: *"Equation used to determine level if this character is placed in
  the world **manually**."* A summoned body is not placed manually.
- **No spawn-pet skill template carries a level field at all.** Checked on all seven spawn-skill
  classes present on this board (`Skill_SpawnPet` 18, `Skill_MonsterGenerator` 15,
  `Skill_TargetedSpawnPet` 12, `Skill_SpawnPetMonster` 10, `Skill_AttackProjectileSpawnPet` 2,
  `Skill_AttackSpellChaosSpawnPet` 2, `Skill_AktaiosMirage` 1). `skill_spawnpet.tpl` carries
  `petBurstSpawn` / `petLimit` / `spawnObjectsTimeToLive` and nothing else; `Skill_Spawning.tpl`
  carries `spawnObjects*` / `spawnObjectWeights*` / `trackSpawns`. **This closes the r2 lap's own
  note** — *"general summon-level rule NAMED-ABSENT (no petLevel field on any summon skill)"* — as
  a **positive** finding rather than a gap: the absence is total, so the level cannot come from the
  skill.
- **The pet's own `charLevel` equation is NOT applied.** Death Revenant carries `charLevel*1+2` and
  Aleksander's Shard carries `charLevel*1+3`; both were camera-measured at **109**, their owners'
  level, not at 111 / 112. (Nor is it applied to *roster* bodies: Aleksander's own equation is
  `charLevel*1+5` and Kubacabra's is `(charLevel*1.1)+2`, yet both sit at 109 = proxy band 106 + 3.)
- ⇒ **the pet enters at its owner's level**, which is what this lap emits (owner's Lap-D floor set,
  LO/HI limbs, transitive to fixpoint). **3 of the 4 controls confirm it exactly. The 4th does
  not — CLIFF C-E1.**

---

## 4 — Populations (NOTE-9: every count names what it counts over)

| id | basis | n |
|---|---|---:|
| **P-PET-70** | `pm2_tg2_pet_chain.csv`, `status = OK`, distinct `pet_record` — *the commission's declared basis* | **70** |
| **P-PET-EDGE-149** | same file, `status = OK` **rows** (owner × skill × pet) — *the basis Lap D quoted its ×4.22 over* | **149** |
| **P-SUMMON-128** | Lap D's extended closure to fixpoint over the 663 band-B pool records, restricted to bodies that are **never** a pool roster/champ record | **128** |
| **P-CONTROL-4** | `t21_wave160_board_ehp_r2.csv` rows that are both skill-spawned pets and carry an independent `measured` eHP | **4** |

`P-PET-70 ⊂ P-SUMMON-128`, and the difference is **58 bodies** — see **IS-E1** (§ 6).

**Grades over P-SUMMON-128:** `life_grade = MEASURED` **127** · `ABSENT:NO-characterAttributeEquations`
**1** (`krieg_aethertrap.dbr` — Lap D's C-D3, carried unchanged, every magnitude column empty, **not**
sibling-filled, **not** modal-filled). `level_grade = DERIVED-INHERITED-FROM-SUMMONER` **128**.

**Magnitudes, wave 160, LO limb:** per body min **150** / median **133,810** / max **2,620,587**.
Σ over P-SUMMON-128 = **32,237,672**; Σ over P-PET-70 = **16,582,699** against Lap B's Σ
**3,471,937** = **×4.78** (sum basis; the per-body median ratio is ×4.20 — different statistics,
both stated).

---

## 5 — The conductor's pre-named hooks

| hook | verdict | number |
|---|---|---|
| **(a) coverage 70/70** | **PASS** | 70/70 present **and** `life_grade = MEASURED` |
| **(a\*) coverage over the corrected population** | **PASS** | 128/128 emitted, 127 MEASURED, 1 declared-GAP named |
| **(a′) every pet body is `Class = Monster`** | **PASS** | `{Monster: 128}`; exactly **1** distinct `pak_binding` across the whole population |
| **(b) agreement with Lap B on the shared granted-passive term** | **REPORTED, and it DISAGREES** | identical **19** / **DIFFER 51** of 70 — see § 6 defect 3 |
| **(c) hardening ratio vs Lap-B** | **PASS — Lap D CORROBORATED, not adopted** | **EDGE basis (Lap D's own, n=149): min 3.38 / median 4.22 / max 10.04 — reproduces ×4.22 to the digit.** RECORD basis (n=70): median **4.20** |
| **(d) cross-lap agreement with Lap D's emission** | **PASS with ONE named divergence** | 2,520 identical / 20 differ / 20 absent, over 2,560 rows. Divergence set is exactly `{chthonianabomination_tentacles_a01}` — ⚑ **D-E1** |
| **(e) structural** | **PASS** | monotone-in-wave violations **0**, negative eHP **0**, `hi < lo` **0**, over 2,560 rows × 127 records |
| **(e′) floor-not-round re-derivation** | **PASS** | **70/70 EXACT**, re-derived from the wide table's own `base_life` + `passive_pct` columns — the long table is graded against something other than itself |
| **(f) positive control** | **PASS** | **4/4 EXACT**, re-derived in the verifier independently of the emitter |

**Hook (c) in full, because "corroborate or correct" was the instruction:** Lap D's ×4.22 was
quoted over *"the 149 pet rows this lap also covers"*. Reproduced on that exact basis this lap
reads **4.22** — **corroborated, not adopted**; I recomputed it from the corpus and from Lap B's
file rather than carrying the number forward. On the **record** basis it reads **4.20**. Both are
correct; they answer different questions, and this lap prints which.

---

## 6 — Defects found in instruments I inherited, two of them mine

| # | id | what | how found | effect |
|---|---|---|---|---|
| 1 | **IS-E1** | **My own Lap-B pet chain is not the summon population.** `pm2_tg2_pet_chain.csv` reaches **70** bodies; Lap D's extended closure run to fixpoint over the same 663 pool records reaches **128** summon-only bodies. | running both over one seed and diffing before choosing a basis | **58 summon bodies missing**, all `Class = Monster`. ⚑ **One of them is `aetherialbloater_b01_summon` — a body this lap's verdict is measured on.** Its owner edge (`aetherialcolossus_galakros.skillName12` → `galakros_summonbloater_secondary.dbr` → `spawnObjects`) exists in the corpus and Lap B's chain does not walk it. Σ eHP @w160 over the 58 = **15.7 M** the sim has never had on the board |
| 2 | **⚑ D-E1** | **Lap D's summon-level inheritance is ONE HOP, not transitive.** A depth-2 summon inherits only from its *direct* summoners' pool sets. | HOOK-d — I compared against Lap D rather than assuming agreement | exactly **1 record of 128**: `chthonianabomination_tentacles_a01` is summoned by `chthonianmonstrosity_summon`, itself a summon carrying `{106,107,108}` **in Lap D's own table** — so Lap D has the information and stops one hop short. Level set `{107,108}` → `{106,107,108}`; LO limb **60,931 → 60,227 (−1.16 %)** on all 20 waves; HI limb agrees. Same class of under-reach as Lap D's own IS-B2 |
| 3 | **IS-E2** | **My own Lap-B granted-passive term is computed differently from the roster chain's.** `pm2b_lib.declared_life_mods` takes `MAX` over each tree skill's `characterLifeModifier` array; band A / Lap D take the array cell **at the skill's rank**. | HOOK-b, which I wrote expecting agreement and which did not deliver it | **51 of 70 bodies DIFFER**, and Lap B's value is the *higher* one (`aetherialworm_b01_summon`: Lap B 169.0 vs 103.0). Lap B also folds the creature's **own** `characterLifeModifier`, which L-33(b) falsified and which this lap's own Bileeater control re-falsifies (`own = +50`, reproduces EXACT **without** it). **So Lap B's pet life is wrong in two directions at once and still lands ×4.2 too soft** — the two folds it is missing dominate the one it over-counts |

**On discipline #11:** two of the three are in work I authored (Lap B), and one of those was found
only because a body my own chain omitted turned out to be load-bearing evidence for my own verdict.

---

## 7 — CLIFFS (filed, not improvised past)

### ⚑ CLIFF C-E1 — one of the four controls dissents on the level rule, and I do not smooth it

`Aetherial Bileeater` was camera-measured at **charLevel 112**. Its owner `Galakros` was
camera-measured at **106**, and Lap D's derived floor set for Galakros is `{106,107,108}` — so
**no** owner level in the set reaches 112. The rule that fits the other three (*pet level = owner
level*) is off by **+6** here, and neither alternative fits either: the pet's own equation
`(charLevel*1.1)+2` gives 118.6 at 106, and 112 only at an input of **exactly 100**.

**Dead-ends named:** no spawn-skill template carries a level field (checked, all seven classes) ·
`monsterLevelGapFixer` at Ultimate is `+7`, not `+6` · the body is not pool-rollable
(`in_pool = False`, so it cannot have been a roster body misattributed) · Lap B's chain has **zero**
owner edges for it, so its owner is known only from the r2 lap's camera attribution.

**What it does NOT threaten:** the Q1/Q2 verdicts. The Bileeater reproduces EXACT *at its measured
level*, so the fold is confirmed regardless of where that level came from. **Only Q3's generality
is at risk**, and only on this one body. **Disposition: conductor.**

### CLIFF C-E2 — `ignoreGameBalance` is undescribed, and 31 of the 174 band-B pools set it True

`proxypool.tpl` declares `ignoreGameBalance [bool] default = 0` with **an empty `description`**. It
is therefore ambiguous between (i) *exempt from the whole GameAdjustment* and (ii) *exempt from its
spawn-**count** limb only* (`spawnMinAdj`/`spawnMaxAdj`, the other four fields of
`gameadjustment.tpl`). **31 of the 174 band-B pools set it True, and all 31 are `pool_kind = BOSS`**
— `nemesis_all`, `nemesis_aetherialvanguard`, `nemesis_beast`, `fatherkymon`, `korvaakfinal`…
**56 band-B records ride ONLY ignore=True pools.**

⚑ **Reading (i) would mean Lap D over-applied `G` to 56 roster records. It is falsified.**
`nemesis_beast_01_p1` (Kubacabra) rides `nemesis_beast` / `nemesis_all*`, all `ignoreGameBalance =
True`, and its **independently measured** eHP of **2,955,796** reproduces EXACT **with
`gladiator_pct = 324` folded**. So `ignoreGameBalance` does **not** gate the stat pak, and reading
(ii) is the one the measurement supports. **This is reported as a resolved worry, not a live
defect** — but the field's semantics remain undescribed in the template, so the resolution rests on
one measured body and is recorded as such.

### CLIFF C-E3 — `monsterLevelGapFixer = [0, 5, 7]` is folded by neither Lap D nor Lap E

`gameengine.dbr`, description **"Index by difficulty 0 to 2 — adds to monster level"**. At Ultimate
(index 2) that is **+7 monster levels**, and *nothing in the KC2 lineage folds it*. It may already
be absorbed into the `+3` offset the r2 lap measured between proxy band and camera level (106 → 109),
in which case folding it would double-count. **Named, not folded, magnitude unpriced.** It bears on
the **roster** as much as on pets. **Disposition: conductor.**

### CLIFF C-E4 — four `Class = Pet*` records exist on the monster side

`harvestman_ravenpet_a01` · `outlaw_ravenpet_a01` · `nonplayerskills/summoning/pets/thermitemine01`
(all `Pet`) and `nonplayerskillsgdx3/bossskills/pets/bloodboundbanner` (`PetPlayerScaling`). **None
is in P-SUMMON-128**, so none affects this lap's numbers — but if a future roster reaches one, it
takes `petAttributePak` (**+15 %**, not +580 %) and this lap's rule would over-harden it by ~×5.
The emitter already routes on `Class` rather than assuming, so it would emit the correct binding;
this is recorded so the exception is not later discovered as a surprise.

### CLIFF C-E5 — this lap is the LIFE limb only

`damage_grade` is out of scope on every row, exactly as Lap D's C-D4. Pet **damage** still rides
the PM-2 threat fold. Named absence with a positive sign.

---

## 8 — What this means for the run (I claim the decode; the fold is gamora's and the ruling gandalf's)

1. **C-D1 is closed MEASURED, in the direction Lap D feared.** Pets harden ×4.20 (median, record
   basis) / ×4.22 (edge basis, Lap D corroborated). PM-3 § 10's *"pets are the only bodies carrying
   real HP"* does **not** re-invert into "pets are the softest" — after this correction pets and
   roster sit on **one chain with one dispatch**.
2. **596 of 779 reference-cell kills ride this.** Every T-band number in I-1 stands on the
   uncorrected limb.
3. **The direction is toward LONGER waves, i.e. against T2's current +2.5 %.** I-1 met T2 by two
   errors cancelling (gamora's own § 13.2); this correction moves one of them. I claim only the
   sign.
4. **The cheapest fold is a ruling, not a new file** (§ 2) — Lap D's table already carries these
   values on 2,520 of 2,560 rows.
5. **IS-E1 says the pet population itself is under-counted by 58 bodies** — that is a *second*,
   independent under-read of the same board, and it is larger than it looks (Σ 15.7 M @w160).

---

## 9 — Laws observed

- **READ-ONLY** on the vendor corpus, the engine tree, every baton and every prior lap's emissions.
  Nothing outside this notes directory and `research/scripts/` was written. `templates.arc` was
  read from bytes and extracted to `/tmp`; the vendor tree was never touched.
- **GL-12 decode-never-estimate.** Every magnitude traces to a `.dbr` field or a `.tpl` declaration.
  The `+580` and `G` citations were **re-decoded from the records**; Lap D's ×4.22 was
  **recomputed**, not adopted; the r2 board's numbers were used as **measurement targets**, never as
  sources. The one unresolvable record is a NAMED GAP with empty magnitude columns. No sibling fill,
  no modal fill, no interpolation anywhere.
- **NOTE-9 basis discipline.** § 4 declares four populations by name; every ratio says which one it
  is over; records and edges are never silently interchanged (hook (c) reports both).
- **No re-implementation.** `pm4e_lib` imports Lap D's `pm4d_lib`, which imports band A's chain.
  One implementation, one place to drift.
- **Cliffs FILED** (§ 7), five of them, including one that dissents from my own Q3 verdict and one
  that I resolved *against* my initial worry and reported as such.
- **Defects self-reported** (§ 6), two of three in my own prior work.
- **Verification is adversarial:** the positive control recomputes each body **four** ways so that
  three columns must be wrong; the floor check re-derives the long table from the wide table's own
  columns; the cross-lap hook compares against Lap D rather than assuming agreement, and **found
  something**.
