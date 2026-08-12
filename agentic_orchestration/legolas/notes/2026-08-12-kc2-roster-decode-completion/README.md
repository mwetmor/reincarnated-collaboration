# KC2 · E-s09-cp150 ROSTER DECODE-COMPLETION LAP (legolas)

**Gap closed:** G2 (s2-band extraction cliff) from `elrond/notes/2026-08-12-enemy-identity-substrate-recon.md`
**Also closed:** G6 (no mesh/model field decoded) · **partially answered:** G7, G8
**Date:** 2026-08-12 · **Author:** legolas (UNKNOWN-RESEARCHER)
**Mode:** read-only. Engine tree, vendor corpus and godot tree untouched. All Python run
from `/tmp` under `PYTHONDONTWRITEBYTECODE=1` (SB-1 FG-17 containment). Only writes are the
files in this directory.
**Schema lineage:** `legolas/notes/2026-08-08-kc2-threat-grammar-arz-boundary/` — that
directory is unmodified.

---

## 0 · HEADLINE

**Coverage 39% → 100% on all six strata. Nemesis 0/9 → 9/9. Hero 3/27 → 27/27.**

And the lap found a real cliff, which was **not** where it was expected. Every one of the
169 records resolved on the first try — the nemesis records are ordinary, well-formed,
~1,000-field creature records. There was no format wall, no auth wall, no indirection the
adapter could not follow. The cliff was **in the harness's own schema**:

> **The 2026-08-08 harness decoded only ONE of the two skill surfaces a Grim Dawn creature
> carries.** It read the 8 attack *slots*. Every creature also carries a granted-skill
> *tree* (`skillName1..N` / `skillLevel1..N`) holding passives, boss skills, auras and
> summons. Across this roster that tree is **1,733 skills against 667 slots — 2.6× the
> surface the old schema saw**, and the ratio is uniform across all six strata (2.3–2.9×).

That gap is the source of a 46-of-66-row disagreement between this lap's `damage_types` and
A6's (`t22_band_a_monster_stats.csv`). Once both surfaces are unioned, the disagreement goes
to **zero** (§ 4). The old 66 "covered" records were never 39% covered on skills — they were
39% of records at ~28% of the skill surface.

---

## 1 · COVERAGE BY STRATUM — BEFORE / AFTER

| stratum | records | identity BEFORE | identity AFTER | stats BEFORE → AFTER | slots | tree skills |
|---|---|---|---|---|---|---|
| **nemesis** | 9 | **0/9 (0%)** | **9/9 (100%)** | 0/9 → **9/9** | 50 | 131 |
| **hero** | 27 | **3/27 (11%)** | **27/27 (100%)** | 3/27 → **27/27** | 129 | 342 |
| boss&quest | 33 | 12/33 (36%) | **33/33 (100%)** | 12/33 → **33/33** | 164 | 397 |
| devotion | 16 | 6/16 (38%) | **16/16 (100%)** | 6/16 → **16/16** | 88 | 212 |
| bounties | 9 | 9/9 (100%) | 9/9 (100%) | 9/9 → 9/9 | 54 | 123 |
| trash | 75 | 36/75 (48%) | **75/75 (100%)** | 36/75 → **75/75** | 182 | 528 |
| **TOTAL** | **169** | **66/169 (39%)** | **169/169 (100%)** | 66/169 → **169/169** | **667** | **1,733** |

Roster basis is the baton itself — `reincarnated-engine/src/reincarnated/output/kc2-baton-v1-E-s09-cp150-20260809_052836.json`,
344 actors → 169 distinct records / 163 distinct names. Stratum counts reproduce elrond's
recon exactly (75 / 33 / 27 / 16 / 9 / 9).

**Records left undecoded: none.** Per-identity residuals are itemised in § 5; all are
sub-record and all are labelled in-band.

---

## 2 · FILES

| file | rows × cols | what it is |
|---|---|---|
| `tg2_monster_timing.csv` | 169 × 104 | one row per identity. Lineage of `tg_monster_timing.csv` (53 cols) + baton facts + declared body + rolled-up damage/control/skill axes + widened `ctrl_*` |
| `tg2_attack_slots.csv` | 667 × 40 | one row per attack slot. Lineage of `tg_attack_slots.csv` (51 cols → 40 kept/renamed) + per-slot damage types, control effects, radius/targets/angle |
| `tg2_skill_tree.csv` | 1,733 × 28 | **new surface.** One row per granted tree skill, with role bucket (passive 852 / attack 525 / buff 187 / other 112 / summon 54 / modifier 2) |
| `tg2_monster_stats.csv` | 169 × 25 | A6-lineage stat fold at 100% coverage: bio record, life equation, life at roster level, declared modifiers, DA/OA |
| `s2_lib.py` | — | roster basis re-pointed t22-968 → baton-169; overlay stack unchanged |
| `s2_extract.py` / `s2_skilltree.py` / `s2_stats.py` | — | the three laps, re-runnable |

Join key throughout is `record` (lowercased `record_path`), identical to A1–A7.

---

## 3 · FIELD COMPLETENESS AGAINST THE FIT-SPEC NEEDS

The commission named six axes. All six are at 169/169.

| fit-spec need | field(s) | coverage | grade |
|---|---|---|---|
| **skills** | `skill_classes`, `tree_skill_classes`, `n_skills_total`, + 2,400 per-skill rows across two CSVs | **169/169** | MEASURED |
| **range** | `range_band_modal`, `range_band_chanceweighted`, `range_band_profile`, per-slot `range_band` | **169/169** | MEASURED (aggregation unruled — § 6) |
| **damage types** | `damage_types_union`, `..._nonphysical`, `damage_types_dot_union` | **169/169** | MEASURED, validated against A6 (§ 4) |
| **behaviour** | 29 `ctrl_*` fields (was 9) + `control_effects_union` + `n_summons` | **169/169** | MEASURED |
| **RIG / body** | `mesh`, `mesh_key`, `mesh_body`, `mesh_scale`, `base_texture` + `basic_attack_anims` | **169/169** | **DECLARED** (was inferred — G6 closed) |
| **stats** | `life_equation`, `life_at_level_min/max`, `defensive/offensive_ability` | **169/169** | MEASURED (base life; wave-scaled eHP out of scope — § 5.4) |

### 3.1 G6 closed — the body is now *declared*, not inferred

The creature record carries a first-class `mesh` field (`creatures/enemies/wendigo/wendigo02a_golden.msh`)
plus `scale` and `baseTexture`. The 08-08 lap inferred the rig from the `.anm` filename
prefix; that inference **disagrees with the declared mesh on 54/169 rows (32%)**. The
declared field supersedes the inference. Both are emitted; use `mesh_key`.

### 3.2 Body-reuse ratio is granularity-dependent — a correction worth banking

elrond reported ~2.9 identities per body at 39% coverage and concluded the Synty tree has
2.4× margin. At full coverage the number **depends entirely on which granularity you mean**,
and the two answers point different directions:

| granularity | distinct | ratio |
|---|---|---|
| exact `mesh` / `mesh_key` (the thing you actually instantiate) | **126** | **1.34 : 1** |
| `mesh_body` (skeleton-family directory) | 43 | 3.93 : 1 |
| anim-inferred rig (the 08-08 method elrond measured) | 41 | 4.12 : 1 |

**Read:** the reference reuses ~43 *skeletons* heavily, but gives most identities their own
*mesh* — a texture/scale variant on a shared skeleton. Within `crabmonstrosity` (n=8) scale
runs 1.00–2.80; within `aetherialcorruption` (n=9), 1.25–2.05. **Size and skin are doing
much of the differentiation work that a naïve "one body per family" read would miss.**

Consequence for drax's census: against the honest instantiation-level ratio (1.34:1),
Synty's 137 bodies for 169 identities is **1.23:1 — comparable to the reference, not 2.4×
more generous.** drax's conclusion ("the gap does not exist") still holds, but the margin is
thin, and it holds *only if* scale and material variation are used as the reference uses
them. I state the numbers; the ruling is gandalf's and drax's.

### 3.3 The reference's rig-divergence finding is confirmed and strengthened

`mesh_body` contradicts the lexical family stem on **72/169 (43%)** — elrond saw 34/66 (52%)
at partial coverage. The direction holds at full scale: **a fit function keyed on family
*name* is falsified by the reference.** Two of nine nemeses (Curate Ignus, Fabius Gonzar)
ride plain human NPC meshes (`humanmale04b.msh`) — the *same* mesh, for two different
nemeses.

---

## 4 · THE DAMAGE-TYPE CONTRADICTION, AND ITS RESOLUTION

Derived slot-only, `damage_types` disagreed with A6 on **46 of 66** overlap rows — and not
as a superset: 24 superset, 14 subset, 8 crossing. A subset relation means the new lap was
*losing* information A6 had (`Physical` on 13 rows), which is a genuine contradiction, not a
scope difference.

Cause: A6 counted tree passives such as `damagebonus_physical03`; a slot-only read cannot
see them. Re-derived as the **union of both surfaces**:

| derivation | equal | superset | **subset** | **crossing** | A6 types missed |
|---|---|---|---|---|---|
| slot-only (08-08 schema) | 20 | 24 | 14 | 8 | Physical ×13, Life ×4, Poison ×3, Aether ×3, … |
| **union slot + tree** | 34 | 32 | **0** | **0** | **NONE** |

The union **contains A6's answer on every row where A6 has one**, and extends it on 32.
That is the validation that the schema gap is closed. Use `damage_types_union`.

Two further validations:
- **Regression against the 08-08 lap: zero drift.** On the 66 shared records, all 7 shared
  fields (`basic_swing_period_s`, `basic_attack_anims`, `character_attack_speed`,
  `controller`, `anim_table`, `monster_classification`, `character_run_speed`) are
  byte-identical. The re-point changed the roster, not the decode.
- **`life_equation` against A6: 66/66 identical.** The bio chain
  (`characterAttributeEquations` → `bios/*.dbr` → `characterLife`) is the right one.

---

## 5 · CLIFF + RESIDUAL CHARACTERISATION (honest boundaries)

**5.1 The schema cliff (found, closed).** Two skill surfaces, one modelled. Described in § 0.
Anyone re-running the 08-08 harness on any other roster inherits this gap — it is not
specific to the s2 band.

**5.2 One dangling reference (1 / 1,733 = 0.06%).** `records/skills/nonplayerskillsgdx3/attackmelee/dranghoul_butcher.dbr`,
granted by *Fariim ~ Bramble*, is present in no archive of the eight-archive overlay stack.
Row is emitted with `status=UNRESOLVED-IN-ARZ`. Either a dangling reference in the
reference's own data or an archive outside Edition-III. Not modellable from this disk.

**5.3 Multi-phase boss, phase 1 only.** `nemesis_beast_01_p1.dbr` (*Kubacabra, the Endless
Menace*) is phase-suffixed; the roster carries only p1. Its phase-2 record is not in the
scene run and is not decoded here. **The fit spec sees Kubacabra's p1 body and p1 skill set
only.** Modelling the transition would need the `dyingSkillName` → spawn chain followed one
hop; that is a design question (does the scene run even have phase transitions?) before it
is a decode question.

**5.4 Wave-scaled eHP not reproduced.** `tg2_monster_stats.csv` emits base life at roster
level plus every declared multiplier it can cite. A6's `ehp_w{1,47,93}` additionally fold the
Crucible wave ladder, armour and resist mitigation — the ratio `A6 ehp_w1_lo / our
life_at_level_min` has median **3.26** across the 66 overlap rows, i.e. A6's number is
consistently ~3.3× ours and the difference *is* the mitigation stack. Reproducing it is a
separate lap. Labelled in-band as `ehp_wave_scaled = NOT-DERIVED (A6 scope …)`.

**5.5 68 slots graded `REF-UNSATISFIED-BY-TABLE`** (of 667; 306 `DIRECT-REF`, 293 `NO-REF`).
A slot skill names a special-animation ref its creature's anim table does not satisfy.
Carried forward from the 08-08 grading vocabulary unchanged — a labelled measurement state,
not a decode failure.

**5.6 Five records declare zero attack slots** (*Apparition* ×2, *Groble ~ Frost Clan
Scavenger*, *Ugdenbog Wretch*, *Corpsefiend*) — but all five carry 3–5 tree skills. Under
the old schema they would have read as doing nothing at all. This is the second surface
earning its keep on the trash stratum, not only on bosses.

**5.7 `mesh_body` is too coarse for the human stratum.** 14 identities collapse to
`mesh_body = "npcs"`; `mesh_key` separates them (`humanmale12a`, `humanfemale04a`, …).
**Fit functions must key on `mesh_key`, not `mesh_body`.**

---

## 6 · GAPS I DID NOT CLOSE (not mine to close)

- **G7 — per-monster range aggregation.** Still a design ruling, not a computation. I emit
  **both** candidate aggregations (`range_band_modal`, `range_band_chanceweighted`) plus the
  full `range_band_profile` so the ruling can be made on evidence and applied without a
  re-run. **gandalf.**
- **G8 — `Physical` as a stopword.** Confirmed at full coverage. I emit
  `damage_types_union_nonphysical` as a ready-made stopworded column alongside the raw one.
  Curation rule remains **elrond's** to document.
- **G1 / G3 / G4 / G5 / G9** — untouched; owners unchanged per elrond's § 5.

---

## 7 · NEMESIS + HERO: DOES THE FIT SPEC HAVE ENOUGH?

**Yes.** Every nemesis and every hero now carries body, size, range, damage, control,
summons and skill counts. Sample of the nemesis stratum, all nine:

| name | mesh_body | range | non-physical damage | slots+tree | summons |
|---|---|---|---|---|---|
| Valdaran, the Storm Scourge | reanimator | LongRange | Lightning\|Aether\|Elemental | 7+16 | 1 |
| Archmage Aleksander | possessed | AnyRange | Fire\|Aether\|Elemental | 6+12 | 2 |
| Kubacabra, the Endless Menace | yeti | ShortRange | Pierce\|Life | 6+14 | 1 |
| Grava'Thul, the Voiddrinker | chthonianrylok | MediumRange | Fire\|Chaos | 5+15 | 2 |
| Nyarlathon, Herald of Annihilation | chthonianherald | AnyRange | Chaos | 5+12 | 1 |
| Curate Ignus | npcs / humanmale04b | ShortRange | Fire\|Chaos | 4+15 | 0 |
| Zantarin, the Immortal | skeleton | AnyRange | Poison\|Life | 6+15 | 3 |
| Fabius "the Unseen" Gonzar | npcs / humanmale04b | ShortRange | Pierce\|Cold | 5+16 | 2 |
| Reaper of the Lost | wendigo | ShortRange | Pierce\|Life | 6+16 | 2 |

Row 10 of elrond's § 3 sample — *Reaper of the Lost*, "NOT EXTRACTED" across every column —
is now fully populated. So are rows 5 (*Moltenclaw*) and 9 (*The Sentinel*).

One caveat the fit law should absorb: **92 of 169 identities summon** (up to 4 distinct pets).
A body fitted to a summoner has to accommodate a summoning gesture and, arguably, its pets'
bodies too. That axis did not exist in the substrate before this lap and nobody has ruled on it.

---

## 8 · ELROND'S § 4.1 VERDICT

**CONDITIONAL → PASS.** The condition was "39% populated, 0% on nemesis." Both are gone.
The clustering feature space is now 169/169 on skills × element × role × range × body ×
size × control × summons.

---

*GL-17 note, restating elrond's § 0 without adopting a position: the 163 names, the 43
skeleton families and the 126 meshes are Grim Dawn's. This lap deepens the reference
extraction; it does not mint anything. If SB-1 is a metrology fixture that is fine. If it
flows toward shipped content the roster must be re-minted first. **gandalf's ruling, not mine.***
