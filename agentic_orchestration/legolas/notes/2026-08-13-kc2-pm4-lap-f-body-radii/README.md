# KC2-PM4 · iteration I-3 · Lap F — give the bodies their space back: per-record collision radii

> **Run:** KC2-PM4 (replicate waves 150–160 faithfully) · **Conductor:** gandalf (`RUN-CONDUCTOR`)
> **Author:** legolas (UNKNOWN-RESEARCHER) · **Date:** 2026-08-13
> **Charter:** `agentic_orchestration/gandalf/notes/2026-08-13-kc2-pm4-replication-run-charter.md` (ledger **L-4**)
> **The divergence this lap serves:** gamora I-2 § 5.3 — the sim's player-weapon hit-test is a
> POINT (`entity_radius_m = None` on all 188 baton actors), the 3.0 m disc held up to **54**
> co-resident bodies, and 8.3 % of the reference cell's kill work happened above a packing ceiling.
> **Status:** COMPLETE. **11/11 conductor + adversarial hooks PASS.** Coverage **297/297 + player**.
> Two of the four questions **MEASURED**, one **MEASURED-ABSENT**, one **DECLARED-GAP with four
> failed discriminators published in full**. Zero estimated magnitudes anywhere (GL-12).

---

## 0 — The one-paragraph answer, and it does not point where the commission expected

**The radius substrate exists, it is complete, and it is one field: `actorRadius`, declared on
`database/templates/actor.tpl` alongside `actorHeight`, `collisionShape` and `scale`, present on
297/297 board records and on the player.** The unit needed no conversion and it is not asserted:
`resources/Text_EN.arc → tags_ui.txt` carries `SkillDistanceFormat={%.1f0 {^E}Meter %s1}` — the game
prints a raw DB length scalar, to one decimal, immediately followed by the word **"Meter"**, with no
factor anywhere in the format string. **⚑ But the number that re-frames Iteration 3 is the split
between the two populations: the 169 roster bodies have a median radius of 0.600 m, and the 128
summoned bodies — which are 76.5 % of the reference cell's kills and 53.6 % of its life — measure
0.360 m.** A 0.36 m body admits **79 centres** inside the 3.0 m disc. **The wave-160 board is
entirely 0.35–0.40 m wraiths and shards, whose ceiling is 83.** So the measured geometry does *not*
make the observed 54 impossible on the ticks that actually carry the kill work — and separately,
**gamora's "32" was computed on a *containment* basis while the sim's hit test
(`‖e.pos − c‖ ≤ 3.0`) is a *centre-in-disc* basis, whose ceiling at the same 0.5 m radius is 44.**
Both corrections point the same way: **the co-residence term is real but it is materially smaller
than the I-2 headline, and a single uniform cap would be wrong in both directions.** The bound must
be evaluated per tick on the actual co-resident mix, from this table.

---

## 1 — The four verdicts

| # | question | verdict | the evidence, in one line |
|---|---|---|---|
| **Q1** | per-record collision/body radius | **MEASURED — `actorRadius`** | `actor.tpl` declares `actorRadius`/`actorHeight`/`collisionShape`/`scale` in ONE template; the include closure `monster.tpl → character.tpl → actor.tpl` (14 templates, re-walked in the verifier) puts it on every body; **297/297 + player carry it**; and a SECOND, independently-authored field agrees (§ 5 hook k) |
| **Q2** | do wave / difficulty / champion modifiers scale body size? | **MEASURED-ABSENT** | `attributepak.tpl` 4 declared variables, ZERO geometric · `gameadjustment.tpl` = attributepak + four spawn-**COUNT** fields, ZERO geometric · across all **819** templates the only runtime body-scale pair is `actorScale`/`actorScaleTime` on `skill_buffselfcolossus.tpl`, carried by **4** corpus records and by **0 of the 297** · champions/heroes are separate `.dbr` records already in this table |
| **Q3** | monster-to-monster collision semantics | **SPLIT: flags MEASURED, base rule DECLARED-GAP** | `monster.tpl` declares `forceCollision` "force collision (**ignores hostility**)" and `forceNoCollision` "force no collision (**ignores hostility**)". ⚑ Those two descriptions say the base rule is a function of the **hostility relation**, and **no hostility→collision table, collision category, or collision layer exists anywhere in the corpus.** Overrides emitted (68 + 14); base rule engine-internal. **Dead end named, not estimated past.** |
| **Q4** | the player's own body radius | **MEASURED** | `records/creatures/pc/{male,female}pc01.dbr`, `Class = Player`, `templateName = player.tpl`: **`actorRadius = 0.3199999928474426`**, `actorHeight = 3.0`, `scale = 1.0499999523162842`, `pathingSize = Small`, `pathMass = 3.0`. **Both sexes identical on every geometry field** (asserted), so the choice of record is immaterial and is recorded rather than hidden |

### ⚑ And the one limb this lap REFUSES to rule: does `scale` multiply the collision radius?

`actor.tpl:scale` has an **empty description**. Two readings survive: `radius = actorRadius` (LO) or
`radius = actorRadius × scale` (HI). **I built four discriminators and ran them all. None
discriminates, and § 4 publishes all four — including the two that failed outright and the one that
produced a signal whose counter-evidence I then went looking for and found.** So the lap emits
**both limbs by explicit column** (`radius_m` / `radius_m_hi`, never row order — R-PM4-2's law,
carried) and **the conductor rules which one Iteration 3 binds.** It is a ×1.20 difference at the
board median and a ×3.00 difference on the wave-160 Korvaak statue.

---

## 2 — Deliverables

| # | file | rows × cols | sha256 | what it is |
|---|---|---:|---|---|
| 1 | **`pm4f_body_radii.csv`** | **299 × 28** | `80517e398f05432fccfb267ccd3b26bada418abf989099ccc4cc23934ecc39d5` | **THE SIM-CONSUMABLE.** 169 roster + 128 summon + 2 player. `(record, radius_m, radius_source_field, collision_flag, grade)` as commissioned, plus the HI limb, the raw fields, the footprint class and the mesh AABB |
| 2 | `pm4f_field_evidence.csv` | 10 × 9 | `e5a6cfde16d6ec0f9a11a27e57352d4ba757a1c50fb6aefef3e2f52b0f832f9c` | the template declaration surface: every geometry/collision field, its declaring template(s), class, type, **description verbatim**, default |
| 3 | `pm4f_scale_modifier_scan.csv` | 8 × 6 | `994b6d575d4d7a3112910a5255daa01094f1d7397b2cd2c3dc26d8e87001c441` | **Q2's census** — every surface in the corpus that could scale a body, and what it actually carries |
| 4 | `pm4f_discriminators.csv` | 4 × 6 | `e6cd69c40e6c18eecb45d2cead4d7168f774063ea53ca21acbe7fe934c1430e9` | **the four `scale` tests, all four published, none of them decisive** |
| 5 | `pm4f_mesh_aabb.csv` | 280 × 8 *(278 board + 2 player)* | `34ba23694731047d4cc3d6bd900ee8c013db8fffd8d1914c75de5e33922a04e1` | the first-of-kind `.msh` chunk-10 AABB decode (§ 4 D2) — a **failed** discriminator, published because a deleted one is a silent estimate |

**Instruments** (`agentic_orchestration/research/scripts/`, schemas + the full decode in their
docstrings): `pm4f_lib_2026_08_13.py` · `pm4f_emit_2026_08_13.py` · `pm4f_verify_2026_08_13.py`.
Logs: `emit.log`, `verify.log`. Machine summaries: `pm4f_emit_summary.json`,
`pm4f_verify_summary.json`.

### How gamora consumes #1

```python
# LO limb (the field verbatim) — R-PM4-2's explicit-column law, carried
radius = {row["record"]: float(row["radius_m"]) for row in table}       # grade MEASURED
# HI limb (x the record's own `scale`) — DERIVED; select by COLUMN, never by row order
radius = {row["record"]: float(row["radius_m_hi"]) for row in table}    # grade DERIVED
player_radius = 0.3199999928474426                                      # malepc01.dbr
```

**Values are emitted at FULL float32 precision, unrounded** (`0.3499999940395355`, not `0.35`).
Rounding a measured quantity to a pretty number is a modification, and hook (i) is written to catch
exactly that — it caught it on the first emission, which is why this one is unrounded.

---

## 3 — The decode, link by link (every citation checked first-hand — GL-12)

### F1 — the field, and why it is *this* field and not a differently-named one

`database/templates.arc` (**818/819** templates decoded; the one failure is the same nameless
`entry_type = 0` placeholder Lap E hit) declares, in **`actor.tpl`**, four variables **in one
template**:

| variable | class | type | description | defaultValue |
|---|---|---|---|---|
| `actorRadius` | variable | real | *(empty)* | `0` |
| `actorHeight` | variable | real | *(empty)* | `0` |
| **`collisionShape`** | picklist | string | *(empty)* | `Box;Sphere;Cylinder;Capsule` |
| `scale` | variable | real | *(empty)* | `1` |

**⚑ `collisionShape`'s co-location is the decisive structural evidence.** `actorRadius` and
`actorHeight` are the parameters of a **collision primitive** — a sphere/cylinder/capsule needs
exactly a radius and a height. The corpus keeps every *other* radius suffixed and elsewhere:
`MonsterMusicRadius`, `characterLightRadius`, `npcAlertRadius`, `npcSocialRadius`,
`npcWanderRadius`, `skillTargetRadius`, `explosionRadius`. **`actorRadius` is the un-suffixed
geometric radius of the actor itself.** *(The descriptions are empty — this is a structural
argument, and it is graded as one. The independent corroboration is hook (k), § 5.)*

**The include closure, walked from bytes in both the emitter and the verifier (never assumed):**

```
monster.tpl → Character.tpl → Actor.tpl        14-template closure
pet.tpl     → Monster.tpl   → …                15-template closure
player.tpl  → …             → Actor.tpl        13-template closure
```

⇒ every roster body, every summon and the player inherit the four fields. **MEASURED: 297/297 + 2.**

### F2 — the second size surface, which is a class and therefore corroborates rather than competes

`character.tpl` declares `pathingSize` (picklist `Small;Medium;Large`) and `pathMass` (real, 1.0) —
the navmesh footprint **class**. It is not a length, so it cannot be the radius. It **corroborates**:

| basis | Small | Medium | Large |
|---|---:|---:|---:|
| median `actorRadius`, board 297 | **0.400** (n=189) | **0.750** (n=99) | **1.000** (n=9) |
| median `actorRadius`, 3,070 corpus `Class=Monster` | **0.400** | **0.700** | **1.000** |

Strictly monotone on both bases (hook c).

### F3 — ⚑ THE UNIT, PROVED FROM THE GAME'S OWN UI STRINGS

`resources/Text_EN.arc → tags_ui.txt`:

```
SkillDistanceFormat={%.1f0 {^E}Meter %s1}
SkillDistanceFormatMod=+{%.1f0 {^E}Meter %s1}
TargetRadius=Target Area
```

**The game prints a raw DB length scalar, to one decimal, immediately followed by the literal word
"Meter", with no conversion factor anywhere in the format string.** Composed with `TargetRadius`
this is the "2.5 Meter Target Area" string the sim's own `EOR_RADIUS_M` citation refers to — and
this lap **re-decoded it rather than adopting the citation.**

The sim already rides the identity twice, unconverted:

| DB | value read here | sim constant |
|---|---:|---|
| `gameengine.dbr:meleeTargetDistance` | **2.4000000953674316** | `locomotion.MELEE_TARGET_DISTANCE_M = Cited(2.4, …, "DB-CITED")` → `D_ENGAGE_M = 2.4` |
| EoR `skillTargetRadius` | 3.0 | `fixture.EOR_RADIUS_M = Cited(3.0, …, "DB-CITED")` → the disc |

⇒ **`actorRadius` is commensurable with the 3.0 m disc without rescaling.** *(Stated precisely: the
sim's metre axis **is** the GD DB length axis, and the game's own UI calls that unit a metre.
Nothing in this lap is converted.)*

### F5 — collision semantics, and the exact point at which the data stops

`monster.tpl` declares exactly two collision variables, and their **descriptions are the finding**:

```
forceCollision    bool  "force collision (ignores hostility)"     default 0
forceNoCollision  bool  "force no collision (ignores hostility)"  default 0
```

⚑ **Both say "ignores hostility".** That is the template corpus stating that the base
character-vs-character collision rule is a function of the **hostility relation** between two
bodies, and that these two fields are the **overrides**. The overrides are decodable and are
emitted. **The base rule is not:** there is no hostility→collision table, no collision-category
field, no collision-layer record, and no collision-mask anywhere in the 819 templates or the
`.arz` corpus. **DECLARED-GAP, dead end named.**

Second dead end: **`collisionShape` is set on 0 of the 297** board records (1,004 corpus records DO
set it — Box 583 / Sphere 392 / Capsule 11 / Cylinder 9), so all 297 take an engine default whose
value is likewise not in the data — a picklist `defaultValue` enumerates the **options**, it does
not name a default. **DECLARED.**

**Per-record flags, MEASURED:**

| flag | ROSTER-169 | SUMMON-128 | total |
|---|---:|---:|---:|
| `FORCE-COLLISION` | 46 | 22 | **68** |
| `FORCE-NO-COLLISION` | 0 | 14 | **14** |
| `DEFAULT-HOSTILITY-DEPENDENT-UNDECODABLE` | 123 | 92 | **215** |

**⇒ Per the conductor's instruction: the engine-behavioural half of Q3 is NOT decodable from the
data, and I declare it rather than estimate it. The geometric bound is therefore the sim's own
abstraction to rule on.**

### F6 — Q2 in full: nothing scales a body by wave, difficulty or champion status

| surface | declared variables | geometric | verdict |
|---|---:|---|---|
| `attributepak.tpl` (the difficulty pak's own template) | 4 | **none** | NO-GEOMETRIC-FIELD |
| `gameadjustment.tpl` (the Crucible survival term's template) | 8 = attributepak + `spawnMinAdj`, `spawnMaxAdj`, `spawnChampionMinAdj`, `spawnChampionMaxAdj` | **none** (all four are spawn **counts**) | NO-GEOMETRIC-FIELD |
| all **819** templates | — | `actorScale`, `actorScaleTime` on **`skill_buffselfcolossus.tpl`** only | SOLE-RUNTIME-BODY-SCALE-SURFACE |
| corpus `Class = Skill_BuffSelfColossus` | **4** records: `salazar_possession1` 1.20 · `cultist_possession1` 1.20 · `theforsaken_overflowingrage` 1.50 · base template 1.80 | — | RUNTIME-BODY-SCALE-EXISTS |
| the 297 board bodies × all `skillName*` slots | — | — | **ZERO carry one** |

Champion and hero bodies are **separate `.dbr` records** carrying their own `actorRadius` and
`scale`, and they are already rows in this table. ⇒ **body size on the E-s09-cp150 board is a pure
per-record constant.**

---

## 4 — ⚑ THE `scale` LIMB: four discriminators, four failures, published in full

`actor.tpl:scale` is undescribed. I could not decide it, and here is everything I tried.

| # | test | basis | result | discriminates? |
|---|---|---|---|---|
| **D1** | **authoring invariance** — within mesh-groups whose `scale` varies, is `actorRadius` constant or is `actorRadius/scale` constant? | 189 corpus mesh-groups (≥3 records, varying `scale`) | **105 hold `actorRadius` CONSTANT · ZERO hold `actorRadius/scale` constant · 84 neither** | **NO.** It *excludes* "`actorRadius` is a hand-authored world-space radius" — authors never re-author it per scale — but it does not choose between the two readings |
| **D2** | **mesh bounding box** — is `actorRadius` a mesh-space or a world-space quantity? | 278/297 board meshes, chunk-10 AABB (first-of-kind decode, § 4.1) | `actorRadius / mesh_half_Z`: median **0.499**, IQR 0.275–1.169. ×`scale`: median **0.666**, IQR 0.309–1.443. Neither lands on 1.0 | **NO.** The bind-pose AABB includes arms, wings and weapons, so it is not a body-width proxy. **A failed discriminator, published rather than deleted** |
| **D3** | **`pathingSize` concordance** (Goodman-Kruskal gamma against the ordinal class) | 3,070 corpus `Class = Monster` creature records, full pair set, no sampling | gamma raw **0.541268** · gamma scaled **0.551610** | **NO.** A 0.010 move |
| **D4** | **`pathingSize` at constant (mesh, actorRadius)** — does the author's own footprint class track `scale` when the geometry is otherwise identical? | corpus groups sharing `(mesh, actorRadius)` | **SIGNAL:** only **2** such groups vary in class, and on both the larger `scale` carries the larger class — **5/5 cross-class pairs agree, 0 disagree** (`raptorwinged01.msh` r=0.55: scale 0.40→Small, 0.65/0.90/1.00→Medium · `possessedstatue_m_01a.msh` r=0.75: scale 2.5→Medium, 3.0→Large). **⚑ COUNTER-EVIDENCE I went looking for and found:** **545** groups hold the class CONSTANT, and **37 of them span ≥ 1.5× in `scale`** (widest **3.87×**, `prawnb01.msh`) | **NO.** 5 agreeing pairs against 37 disagreeing groups is not a decode |

**⇒ VERDICT: DECLARED-GAP.** Both limbs emitted, neither ruled. **Conductor's call.**

### 4.1 — the `.msh` container, solved here (first-of-kind in this lineage)

`resources/Creatures.arc → *.msh` is a flat chunk container: magic `MSH\x03`, then
`[chunkID u32][payloadLen u32][payload]` repeated. **Chunk 10 is 24 bytes = six little-endian floats
= the mesh AABB `(minX, minY, minZ, maxX, maxY, maxZ)`, Y up, in mesh space.** Verified by **exact
byte coverage** — the walk consumes every byte of every file with zero residue (hook g: 278/278).
1,303 meshes indexed across five `Creatures.arc` containers. **19 board records do not resolve, and
they resolve to nothing for a clean reason: their `mesh` points into `fx/meshfx/` or
`level art/` rather than `creatures/`** — they are FX and set-dressing bodies (obsidian sentries,
ice spikes, totems, portals, and `aetherialvanguard_crystal`). Named, not filled.

**This decode did not answer the question it was built for, and it is reported anyway.**

---

## 5 — The conductor's pre-named hooks (and six adversarial ones I added) — **11/11 PASS**

| hook | verdict | number |
|---|---|---|
| **(a) coverage 297/297 + player** | **PASS** | 297 board rows ≡ P-ROLLED-20 ∪ P-SUMMON-128 exactly (0 missing / 0 extra), **grade census `{MEASURED: 297}`**, 2 player rows |
| **(b) unit sanity — the DB↔metre conversion** | **PASS** | `SkillDistanceFormat={%.1f0 {^E}Meter %s1}` decoded from `tags_ui.txt`, **no conversion factor**; `meleeTargetDistance` re-read at **2.4000000953674316** = the sim's `D_ENGAGE_M`; `EOR_RADIUS_M = 3.0` from the same DB length space |
| **(c) distribution sanity** | **PASS** | min-including-zero **0.000** (`aetheranomaly_01_summon`) · min-physical **0.200** (`beetle_maggot01_maggotsummon`) · p25 **0.350** · **median 0.500** · p75 **0.750** · max **2.000** (`aetherialcommander_01`). **⚑ The conductor's own predicate: wendigo 0.700 > wraith orb 0.350 — PASS.** `pathingSize` medians strictly monotone 0.400 / 0.750 / 1.000 |
| **(d) wave-160 spot check** | **PASS** | all five bodies re-read from the corpus inside the verifier and matched to the CSV bit-for-bit — table below |
| **(e) reader independence** (`winner()` vs `merged()`) | **PASS** | 297 records × 4 geometry fields, **0 disagreements**. IS-B1's failure mode does not touch this limb |
| **(f) closure independence** | **PASS** | `actor.tpl` re-proved present in monster/pet/player closures from `templates.arc` bytes inside the verifier; `actorRadius` decl `type=real default=0`; `collisionShape` decl `picklist Box;Sphere;Cylinder;Capsule` |
| **(g) mesh walk integrity** | **PASS** | **278/278 exact byte coverage, 0 residue**; 19 board meshes unresolved and named |
| **(h) packing bound, BOTH predicates** | **PASS (reported, not ruled)** | § 6 |
| **(i) no-estimate audit** | **PASS** | 299 rows re-derived from `E3.winner` inside the verifier; **0 violations**. *(This hook FAILED on the first emission and caught my own 6-dp rounding — § 7 IS-F1.)* |
| **(j) zero-radius census** | **PASS** | **17** records carry a MEASURED `actorRadius = 0.0`, all 17 in SUMMON-128, all named. **Not missing data; not back-filled** |
| **(k) ⚑ cross-field corroboration** | **PASS** | § 5.1 |

### 5.1 — ⚑ HOOK (k): a second, independently-authored field agrees on which records have no body

`actorRadius` lives on `actor.tpl`; `forceNoCollision` lives on `monster.tpl`. Different templates,
different authoring surfaces, both hand-set per record. If `actorRadius` really is the collision
radius, the two should agree about which bodies are not bodies. **They do:**

| basis | n | `r=0` ∧ noCollision | P(noCollision \| r=0) | base rate | **lift** |
|---|---:|---:|---:|---:|---:|
| **board 297** | 297 | **13** of 17 | **0.7647** | 0.0471 | **×16.2** |
| corpus (creatures + skills) | 6,292 | 485 of 1,003 | 0.4835 | 0.1305 | **×3.7** |

**13 of the board's 14 force-no-collision bodies are exactly its zero-radius bodies.** They are
ground effects, voids, pools and anomalies — `sandstorm`, `eldritchground`, `beast_bloodpool`,
`chthonian02_void`, `giantfire_moltenpool`, `siff_icefloe`, `krieg_aethertrap`. **This is
CORROBORATION, graded as such: it does not decode engine code.** Four zeros are *not* flagged
(`loghorrean_void`, `aetheranomaly_01`, two `korvaak_lieutenant_02_trapsummon*`) and are reported,
not smoothed.

### 5.2 — HOOK (d) in full: the wave-160 board, explicitly

`w160_a000…a004` are **five actors on four distinct records** — `statue_korvaaktombguardian` rolls
twice (a003 + a004).

| actor | record | **radius_m (LO)** | radius_m_hi | `scale` | `pathingSize` | grade |
|---|---|---:|---:|---:|---|---|
| `w160_a000` | `nemesis_kymon_01` | **0.500** | 0.675 | 1.350 | Small | MEASURED |
| `w160_a001` | `nemesis_wendigo_01` | **0.700** | 0.980 | 1.400 | Medium | MEASURED |
| `w160_a002` | `nemesis_aetherialvanguard_01` | **0.400** | 0.540 | 1.350 | Small | MEASURED |
| `w160_a003` | `statue_korvaaktombguardian` | **0.750** | **2.250** ⚑ | **3.000** | Large | MEASURED |
| `w160_a004` | `statue_korvaaktombguardian` | **0.750** | **2.250** ⚑ | **3.000** | Large | MEASURED |

⚑ **The Korvaak Tomb Guardian is the whole `scale` question in one row: ×3.00 between the limbs, and
it rolls twice on the death wave.** It is also the board's only `scale = 3.0`.

**And the 30 pets the terminal wave actually spawned:**

| record | count | radius_m (LO) | radius_m_hi | note |
|---|---:|---:|---:|---|
| `wraith_b01_summon` | 12 | **0.350** | 0.403 | |
| `wraith_c01_summon` | 12 | **0.350** | 0.438 | |
| `aetherialvanguard_crystal` | 6 | **0.400** | 0.460 | ⚑ Aleksander's Shard — the `devastationshard` source that dealt 9,923 of the 20,860 that killed the I-2 player |

---

## 6 — ⚑ HOOK (h): what the disc actually holds, and the TWO basis corrections the conductor needs

Hexagonal packing density `η = π/(2√3) = 0.906900` — not a fitted number, a constant.

**⚑ BASIS CORRECTION 1 — the two predicates are not the same question.**
gamora's "32" is the **CONTAINED** basis: bodies wholly inside the 28.27 m² disc,
`N ≤ η·(R/r)²`. **The sim's hit test is `‖e.position(t) − c‖ ≤ 3.0` — a CENTRE-IN-DISC
predicate.** Bodies whose centres lie in disc(R) all lie in disc(R+r), giving
`N ≤ η·((R+r)/r)²`. At r = 0.5 that is **44, not 32.**

| r (m) | CONTAINED (gamora's basis) | **CENTRE-IN-DISC (the sim's own predicate)** |
|---:|---:|---:|
| 0.20 | 204 | **232** |
| 0.32 *(player)* | 79 | **97** |
| **0.35** *(w160 wraiths)* | 66 | **83** |
| 0.40 | 51 | **65** |
| **0.50** *(board median, LO)* | **32** | **44** |
| **0.60** *(board median HI; roster median LO)* | 22 | **32** |
| 0.70 | 16 | 25 |
| 0.75 | 14 | 22 |
| 1.00 | 8 | 14 |
| 2.00 | 2 | 5 |

**⚑ BASIS CORRECTION 2 — the roster and the summons are not the same size, and it is the summons
that crowd the disc.**

| population | n | LO min | LO p25 | **LO median** | LO p75 | LO max | HI median | centre-in-disc ceiling at the median (LO / HI) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **ROSTER-169** | 169 | 0.350 | 0.400 | **0.600** | 0.800 | 2.000 | 0.810 | **32 / 20** |
| **SUMMON-128** | 128 | **0.000** | 0.350 | **0.360** | 0.520 | 1.100 | 0.404 | **79 / 64** |
| board 297 | 297 | 0.000 | 0.350 | **0.500** | 0.750 | 2.000 | 0.600 | **44 / 32** |
| player | 1 | — | — | **0.320** | — | — | 0.336 | 97 / 89 |

**⚑ 76.5 % of the reference cell's kills and 53.6 % of its life are summoned bodies, and they
measure 0.360 m — a ceiling of 79 centres, above gamora's observed max of 54.** The wave-160 board
is entirely 0.35–0.40 m bodies (ceiling **83**). **So on the ticks that carry the kill work, the
measured geometry does not by itself make the observed occupancy impossible.**

**What I claim and what I do not.** I claim the *radii* and the *arithmetic*. I do **not** claim
what Iteration 3 should cap, and I have not evaluated the per-tick mix — that requires the
tick-level co-residence roster, which is gamora's surface, not mine. **The correct bound is
composition-dependent and must be evaluated per tick.** A rigorous necessary condition for a mixed
set whose centres lie in disc(R):

```
Σ_i π·r_i²  ≤  η · π · (R + max_i r_i)²
```

**A single uniform cap is wrong in both directions on this board: too tight for a wraith swarm, far
too loose for two Korvaak statues.**

---

## 7 — Defects found, one of them mine and caught by my own hook

| # | id | what | how found | effect |
|---|---|---|---|---|
| 1 | **IS-F1** | **⚑ MY OWN FIRST EMISSION ROUNDED A MEASURED QUANTITY.** `radius_m` was written as `round(actorRadius, 6)`, turning the corpus's float32 `0.3499999940395355` into `0.35`. | **hook (i), the no-estimate audit I wrote to be adversarial to myself — it FAILED, along with hook (d), on the first run** | 2 of 11 hooks red. Rounding is small, but the rule is that a measured magnitude is emitted as measured; a "prettier" number is the reader's job, not the file's. **Fixed: full precision, unrounded. Both hooks now PASS and the audit is exact-equality, not tolerance-based.** The first digest (`2ff2f32a…`) is superseded by `80517e39…` |
| 2 | **⚑ D-I2-1** | **gamora's packing ceiling answers a different predicate than the sim's hit test.** I-2 § 5.3's "hexagonal packing fits 32" is a **containment** bound; `disc.resolve_tick`'s predicate is `‖e.pos − c‖ ≤ 3.0`, i.e. **centre-in-disc**, whose ceiling at the same radius is **44** | recomputing the bound from measured radii and noticing the two formulas disagree | The "8.3 % of kill work is physically impossible" claim is **directionally intact but numerically overstated**: 54 exceeds 44 by 23 %, not 32 by 69 %. **⚑ And 0.5 m — the radius gamora assumed — turns out to be the board's MEASURED median exactly, so the assumption was good and only the predicate was mismatched.** Not gamora's error to have made the assumption; reported so the fold is built on the right formula |
| 3 | **D-I2-2** | **the I-2 headline is computed over the wrong population's radius.** The bodies co-residing at high occupancy are overwhelmingly pets (620 spawned vs 183 roster kills), and pets measure **0.360 m**, not 0.500 m | splitting the distribution by population before quoting a median | at 0.360 m the centre-in-disc ceiling is **79** — above the observed max of 54. **The occupancy term is real but materially smaller than I-2 § 5.3 priced it.** Named as a measurement, not as a criticism: the number could not have been known before this lap |
| 4 | **IS-F2** | **19 of 297 board `mesh` fields point outside `creatures/`** (into `fx/meshfx/` and `level art/`), so the D2 corroboration covers 278, not 297 | building the mesh index and counting misses instead of reporting the hits | no effect on any radius (D2 is corroboration only, and it failed to discriminate anyway). Named so the 278 is never read as 297 |

---

## 8 — CLIFFS (filed, not improvised past)

**⚑ CLIFF C-F1 — `scale` is undecided, and it is a ×1.20 board-median / ×3.00 worst-case fork.**
§ 4. Four discriminators, none decisive. Both limbs emitted by explicit column. **Conductor rules.**
The single most consequential row is `statue_korvaaktombguardian` (0.750 vs 2.250), which rolls
twice on the death wave.

**⚑ CLIFF C-F2 — the base collision rule is engine-internal.** § F5. The templates say collision is
hostility-dependent; no hostility→collision table, collision category, collision layer or collision
mask exists in the corpus. **Per the conductor's own instruction, this limb is DECLARED with the
dead end named, and the geometric bound is therefore the sim's own abstraction to rule on.** The
per-record overrides (68 force-collision, 14 force-no-collision) are MEASURED and emitted.

**CLIFF C-F3 — `collisionShape` is unset on 297/297.** All take an engine default that a picklist
`defaultValue` cannot name (it enumerates the options). 1,004 corpus records DO set it — Box 583 /
Sphere 392 / Capsule 11 / Cylinder 9 — so if a future roster reaches one of those, the shape is
decodable for that body. **A cylinder and a box of the same `actorRadius` do not pack identically**;
this lap's bound assumes discs, which is the disc-abstraction the sim already runs.

**CLIFF C-F4 — 17 MEASURED zero-radius bodies.** All in SUMMON-128, 13 of them independently
flagged `forceNoCollision`. Under an occupancy bound they legitimately remain **POINTS** — a
0-radius body is not a hole in the data (hook j). **They must NOT be back-filled to a modal radius**;
doing so would invent bodies for `sandstorm` and `eldritchground`.

**CLIFF C-F5 — this lap is the GEOMETRY limb only.** No life, no damage, no locomotion, no
placement. `actorHeight` is emitted (census: 2.0 on 260 / 1.0 on 19 / 1.5 on 16 / 1.25 on 2) but
**nothing in this lap uses it**, because the sim's disc is 2-D. If a future fold wants a 3-D body,
the field is there and it is measured.

**CLIFF C-F6 — `pathMass` / `physicsMass` are emitted and unpriced.** `pathMass` is 1.0 on 271 and
2.0 on 26 board bodies; the **player is 3.0**. If GD resolves body-vs-body push by pathing mass, a
crowd-separation model would want it — but the field is undescribed and this lap does not model
separation. **Named absence, not a gap.**

---

## 9 — Populations (NOTE-9: every count names what it counts over)

| id | basis | n |
|---|---|---:|
| **P-ROLLED-20** | Lap D's frozen baton `…-20260809_052836.json`, `actors[]`, wave ∈ [151,170], distinct records | **169** |
| **P-SUMMON-128** | Lap E's summon-only closure over the 663 band-B pool records (R-PM4-5) | **128** |
| **union** | the board this lap covers; **overlap = 0** (the two populations are disjoint by construction) | **297** |
| **P-PLAYER-2** | `Class = Player` records; identical on every geometry field | **2** |

**Grades over the union:** `radius_m` **MEASURED 297/297** · `radius_m_hi` **DERIVED 297/297** ·
`collision_flag` MEASURED-override **82**, DECLARED-GAP-base-rule **215** · **DECLARED-GAP rows: 0**
(every record resolved; the krieg record that is a life GAP in Laps D/E carries a MEASURED radius of
0.0 here — a body can be lifeless in one limb and measured in another, and both are stated).

---

## 10 — What this means for the run (I claim the decode; the fold is gamora's and the ruling gandalf's)

1. **The substrate the conductor said did not exist, exists and is complete.** `entity_radius_m` can
   be populated on 297/297 board records and the player from one MEASURED field. The point hit-test
   (M-5) is retirable.
2. **⚑ But the term is smaller than I-2 priced it, for two independent measured reasons** (§ 6):
   the predicate basis (44, not 32) and the population basis (pets at 0.360 m, not 0.500 m). **I
   claim only the direction and the arithmetic — I have not evaluated the per-tick mix.**
3. **⚑ The occupancy fold may not re-discriminate CLUSTER vs CAMP the way L-4 registered as its
   expectation.** If the bound rarely binds on pet-dominated ticks, the matrix stays converged and
   the conductor's "matrix redesign at Iteration 4" trigger fires. **This is a prediction I am
   making before the fold runs, so it can be falsified.**
4. **`scale` is the fork that matters and I could not close it** (C-F1). On the LO limb the board
   median is 0.500 and the ceiling 44; on the HI limb 0.600 and 32. **The HI limb reproduces
   gamora's 32 exactly — a coincidence, and it must not be mistaken for agreement**, because it is
   the *centre-in-disc* ceiling at the HI median, while gamora's 32 is the *contained* ceiling at
   the LO median. Two different formulas landing on one integer.
5. **Nothing here can touch T4b.** Wave 160's player deals zero damage rows; giving bodies radii
   does not put a weapon in the approach window. **I-2 (kit/dash) and I-3 (potions) remain the only
   queued items that can reach it**, exactly as gamora's I-2 § 15 said.

---

## 11 — Laws observed

- **READ-ONLY** on the vendor corpus, the engine tree, every baton and every prior lap's emissions.
  Nothing outside this notes directory and `research/scripts/` was written. `templates.arc`,
  `Creatures.arc` and `Text_EN.arc` were read **from bytes in memory**; the vendor tree was never
  touched and nothing was extracted into it.
- **GL-12 decode-never-estimate.** Every magnitude traces to a `.dbr` field or a `.tpl` declaration,
  at **full float32 precision, unrounded**. The unit was **re-decoded** from `tags_ui.txt` rather
  than adopted from the sim's citation; `meleeTargetDistance` was **re-read** rather than quoted.
  **Two questions are DECLARED rather than answered** (C-F1 `scale`, C-F2 the base collision rule),
  and both name their dead ends. No sibling fill, no modal fill, no interpolation, no default
  substituted for an absence — **audited, 0 violations over 299 rows** (hook i).
- **NOTE-9 basis discipline.** § 9 declares four populations by name; every median in § 6 says which
  population it is over; **the two packing predicates are never interchanged**, and the one place
  they coincide on an integer is called out as a coincidence.
- **No re-implementation.** `pm4f_lib` imports Lap D's `pm4d_lib` and Lap E's `pm4e_lib` for the
  reader and both populations. One implementation, one place to drift.
- **Verification is adversarial:** the verifier re-walks the template closure from bytes, re-reads
  every radius from the corpus rather than from the emitter's objects, re-runs the mesh walk with a
  byte-coverage assertion, cross-checks `winner()` against `merged()`, and runs a no-estimate audit
  **that failed on the first emission and caught my own rounding** (§ 7 IS-F1).
- **Failed instruments published.** D2 and D3 discriminate nothing and are emitted anyway
  (`pm4f_discriminators.csv`); D4's counter-evidence was actively sought and is reported alongside
  its signal. **A discriminator you delete because it did not help is an estimate wearing a
  measurement's clothes.**
