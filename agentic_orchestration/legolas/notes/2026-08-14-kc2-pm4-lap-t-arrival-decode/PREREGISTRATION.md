# RUN KC2-PM4 — LAP T — THE ARRIVAL DECODE — PRE-REGISTRATION

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Fired under:** R-PM4-49 part 4 (ledger row L-40) · **Written:** 2026-08-14
**Discipline:** GL-12 DECODE-NEVER-ESTIMATE · outcome-firewalled · NOTE-9 basis on every number ·
FULL 64-hex sha256 on every input and output · read-only on every external source.

**This file is written and hashed BEFORE any Lap-T instrument is run.** Its sha256 is recorded in
`pm4t_digests.json` and recomputed at landing. Every threshold, prediction and verdict rule used in
`pm4t_findings.md` appears here first.

---

## § 0 — RECONNAISSANCE THAT PRECEDED THIS HASH (declared, per the Lap S convention)

Honesty requires that I state exactly what I already saw before writing predictions. Recon was
scope-finding — *is the territory reachable, and by what instrument* — but on limb (a) it went
further than scope and **I already know the headline**. I declare it rather than pretend to
predict it.

**R-0.1 — Corpus indexed.** A new multi-archive `.arz` reader
(`agentic_orchestration/research/scripts/pm4t_arz_2026_08_14.py`) indexes all **8** archives of
`/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` — **84,829 unique record paths** under
a declared override order (base → GDX1/2/3 → SurvivalMode → SurvivalMode1/2/3).

**R-0.2 — The beacon chain is fully readable and was read.** `records/creatures/traps/spawnbeacon.dbr`
(class `Monster`, owner `SurvivalMode.arz`) → `initialSkillName`/`skillName1` =
`records/skills/misc/spawnbeacon_aura.dbr` (class `Skill_BuffRadiusToggled`) → `buffSkillName` =
`records/skills/misc/spawnbeacon_aura_buff.dbr` (class `SkillBuff_Passive`).
**I have already seen that the buff record carries `characterAttackSpeedModifier = 30.0`,
`characterSpellCastSpeedModifier = 50.0`, `skillTargetRadius = 8.0`, `skillMaxLevel = 1` — and NO
`characterRunSpeedModifier` field of any kind.** Limb (a)'s headline is therefore not a prediction;
it is a recon result that the instrument will *confirm and complete* (stacking, uptime, targeting
class, template defaults, cross-archive override). **Prediction P-A1 below is stated as
already-observed, and is not counted in the prediction score.**

**R-0.3 — The Lua is a pass-through.** `game/survival/eventcontrol.lua` (extracted from three
Scripts.arc archives) does nothing but `Entity.Create("records/creatures/traps/spawnbeacon.dbr")` at
five `ScriptEntity` coordinate carriers and re-create them on event reset. **All beacon mechanics
live in the `.dbr` chain.** The shipped comment at line 41 is the F-12 comment.

**R-0.4 — Field-name scope confirmed.** `characterRunSpeedModifier`, `characterRunSpeedMaxModifier`,
`monsterRunSpeedCapMax`, `monsterRunSpeedCapMin`, `bossRunSpeedCapMax/Min` all exist as string-table
literals. `records/game/survivalinfo.dbr` exists and is the Crucible's scaling record.

**R-0.5 — Lap R already owns much of limb (b) and I must not re-derive it.** Lap R
(`pm4r_speed_terms.csv`, 2,073 rows; `pm4r_findings.md` § 5.2) already MEASURED:
`characterRunSpeed` present on **169/169** roster records; `characterRunSpeedJitter` on 137 with
values {0,10,15,20,25,30}; `monsterRunSpeedCapMax = 500.0`,
`monsterRunSpeedCapMin = [20,25,30]`; player base `characterRunSpeed = 0.93`,
`playerRunSpeedCapMax = 135.0`. Lap R's **`UNREACHED-8` is exactly limb (b)'s open question:
*monster effective in-fight speed*.** Lap T's job on limb (b) is therefore the **UNIT CONVERSION and
the modifier search**, not a re-read of the scalars. Lap R is cited as basis (NOTE-9); anything I
re-read is a *control*, and any disagreement with Lap R is reported as a defect on one of us.

**Nothing on limbs (b), (c), (d) beyond the above was looked at before this hash.**

---

## § 1 — INPUTS TO BE HASHED BEFORE USE (GL-6)

All eight `.arz` archives; the three `eventcontrol.lua` extractions; the three `Maps.arc`
containers; `Game.dll` / `Engine.dll`; Lap S's `pm4s_arena_placements.csv` +
`pm4s_arena_geometry.json`; Lap R's `pm4r_speed_terms.csv`; Lap P's `pm4p_leech_resistance.csv`.
Full 64-hex, every one, recorded in `pm4t_digests.json`.

---

## § 2 — LIMB (a): THE BEACON MAGNITUDE (`UNREACHED-S2`)

**Instrument I-T1** — `pm4t_beacon_2026_08_14.py`. Walks the beacon record graph BFS to depth 6
across the layered corpus, following every `.dbr`-valued field; emits every reached record with its
owning archive, class, override layers, and full field set; then isolates the modifier surface.

### Predictions

| # | prediction | falsification |
|---|---|---|
| **P-A1** *(already observed, § 0.2 — NOT SCORED)* | the buff carries attack- and cast-speed modifiers and **no** run-speed modifier | a `characterRunSpeed*` field appearing anywhere in the chain |
| **P-A2** | **the beacon chain contains NO movement-speed term anywhere at any depth** — not on the beacon monster, not on the aura, not on the buff, not on the controller, not on any template default | any `characterRunSpeed`, `characterRunSpeedModifier`, `characterRunSpeedMaxModifier`, `pathMass`, `maxRotationSpeed` **modifier** reached from the chain with a non-neutral value |
| **P-A3** | the aura radius is **8.0 m** and comes from `skillTargetRadius` on the buff, with no per-rank array (`skillMaxLevel = 1`) | a rank array of length > 1, or radius sourced from a different field |
| **P-A4** | uptime is **permanent and unconditional** — `Skill_BuffRadiusToggled` + `instantCast = True` + `initialSkillName` means it is on from creation, with no cooldown/duration/energy gate | any `skillCooldownTime`, `skillActiveDuration`, `buffDuration` or energy-cost field with a non-zero value in the chain |
| **P-A5** | stacking across the 5 beacons is **not resolvable from the records alone** (same buff record from 5 sources; whether GD stacks identical passive buffs is engine behaviour) → lands **UNREACHED or INFERRED**, never MEASURED | a decoded stacking flag in the chain or template |

### Verdict rule (fixed here)

- If P-A2 holds: **limb (a) lands `UNREACHED-S2` CLOSED as MEASURED-NEGATIVE on the movement claim**
  — the shipped comment *"Spawn Beacons accelerate monster movement in their spawn areas"* is
  **a misdescription of the record**, and the correct fold is **NO march-speed boost**.
  This is the F-11 jitter precedent: authored intent, unimplemented mechanic. **DO NOT FOLD SPEED.**
- The attack/cast-speed magnitudes are reported as **what the beacon actually does**, separately
  graded, and are a *different* term from the one the run went looking for.
- **I pre-commit to reporting this even though it removes the run's leading candidate explanation
  for the 3–5× arrival gap.** The lap is outcome-firewalled; a negative that widens the residual is
  the finding.

---

## § 3 — LIMB (b): MARCH-SPEED PRICING

**Instrument I-T2** — `pm4t_march_2026_08_14.py`. Over the 790-body / 169-record tier-16 roster
(joined from `pm4p_leech_resistance.csv`): re-read `characterRunSpeed` as a **control against Lap R**;
search every roster record's full skill/aura/controller chain for run-speed modifiers; read the
engine caps; read `records/game/survivalinfo.dbr` and the Crucible difficulty/wave scaling records
for any speed term.

### The unit problem — stated in advance

`characterRunSpeed` is a **record scalar of unknown unit**. It is the load-bearing unknown: without
a unit the roster table cannot be priced in m/s and the arrival arithmetic cannot be done.
Two routes are pre-registered, in this order:

1. **DECODE (preferred).** Find the consumption site in `Game.dll`/`Engine.dll` — a literal or a
   named constant converting the scalar to world units.
2. **PLAYER CALIBRATION (fallback, explicitly INFERRED-WITH-EVIDENCE, never MEASURED).**
   The player's record scalar (0.93, Lap R) and the player's measured world speed
   (**4.029485 / 3.836070 m/s**, the px-bracket pair banked at L-38) and the player's modifier
   state (135 %, at `playerRunSpeedCapMax`, Lap R finding 5) fix a conversion constant
   `K = v_world / (characterRunSpeed × modifier)`. Applying that same K to monsters **assumes
   player and monster share one locomotion constant.** That assumption is NAMED, and the resulting
   table is graded INFERRED-WITH-EVIDENCE, carried as a **bracket** (px-LO/px-HI), never a point.

### Predictions

| # | prediction | falsification |
|---|---|---|
| **P-B1** | my re-read of `characterRunSpeed` **agrees with Lap R on 169/169 records** | any disagreement → a defect on Lap R or Lap T, self-reported either way |
| **P-B2** | **no Crucible wave-scaling record applies any run-speed modifier to monsters** — the survival scaling surface is offence/defence/life, not locomotion | a wave- or tier-indexed `characterRunSpeed*` term |
| **P-B3** | **at least one roster record's skill chain carries a movement term** (charge/leap/flee skills exist in GD monster kits), but it is **transient**, not a permanent march modifier | zero movement terms anywhere (stronger negative), or a permanent one (falsifies "transient") |
| **P-B4** | the `Game.dll`/`Engine.dll` route (route 1) **fails** — the scalar→world conversion is not recoverable as a literal from a stripped release binary | a decoded conversion constant (which would be the better outcome and would supersede route 2) |
| **P-B5** | under route-2 calibration the roster's **typical march speed is 2.5–3.5 m/s**, and therefore a **17.07 m** (NEAR) march costs **≈ 5–7 s** and a **37.03 m** (RING) march costs **≈ 11–15 s** | computed values outside those bands |

### Verdict rule

The per-body-class table lands with an explicit grade **per column**. Any body class whose speed
chain is not fully walked lands **UNREACHED for that class**, not averaged into the others.

---

## § 4 — LIMB (c): `D-I19-3` ARBITRATION — AND THE AUDIT OF MY OWN INSTRUMENT

Gamora reports two `.map` decodes of the same file agreeing on spawn points to **5.1e-4** and on
count (11), but disagreeing on **patrol-point positions by 0.45–13.28 m (median 3.44)**, centroid
**2.65 m** apart. My `pm4s_map_2026_08_14.py` is one of the two parties.

Gamora's stated (deliberately unverified) hypothesis: the sim's L-46 reader takes the **head-section
inline `Patrol Points` group**; Lap S's takes **placement-array `patrolpoint_01.dbr` rows**.

**Instrument I-T3** — `pm4t_map_arb_2026_08_14.py`. Re-parses the `.map` from both readings
independently, on the same file, and cross-tabulates.

### Predictions

| # | prediction | falsification |
|---|---|---|
| **P-C1** | gamora's hypothesis is **correct** — the two decodes are reading **two different structures**, not the same structure differently | both readers provably hitting the same byte range |
| **P-C2** | **both are "right" about their own structure**; the disagreement is a **semantic** question (which structure the engine's `PatrolPoint_Attack` group actually binds), not a parse defect | one reader shown to mis-parse its own structure → that is a defect, self-reported if mine |
| **P-C3** | the disagreement is **BRACKETABLE and small relative to U-S-2** — max 13.28 m against a 2.2× bracket spanning 17.07–37.03 m; it **cannot flip U-S-2** | a case where the two decodes straddle the NEAR/RING boundary for a majority of spawn points |

### Verdict rule (fixed here — this is the FIT-law commitment)

- **If my Lap S reader is shown wrong, I say so plainly and name the finding of Lap S that it
  contaminates (F-3/F-4/F-5), with the direction and magnitude of the error.**
- If neither is decidable from bytes, the honest landing is **BRACKET, not decision**: report the
  bound and say which quantity would decide it.
- I will **not** prefer the reading that is mine.

---

## § 5 — LIMB (d): `U-S-4`/`U-S-2` RECORDS-SIDE RESIDUE

**Instrument I-T4** — `pm4t_patrol_2026_08_14.py`. Reads every `patrolpoint*` / pathing record class
and its template; greps `Game.dll`/`Engine.dll` for `PatrolPoint`, `LinkPatrolPointGroup`,
`patrolPoint`, pathing-parameter literals.

### Predictions

| # | prediction | falsification |
|---|---|---|
| **P-D1** | patrol-point `.dbr` records are **near-empty markers** carrying no target-selection semantics | a selection-policy field |
| **P-D2** | `Game.dll`/`Engine.dll` **do** carry `PatrolPoint`-family literals (Lap S proved export-table recovery works) | zero literals |
| **P-D3** | **U-S-2 stays UNDECIDED** — no records-side or literal-side artefact discriminates NEAREST vs CENTROID; the semantics are in the DRM'd body (`UNREACHED-S1`) | a decoded discriminator, which would close U-S-2 |

---

## § 6 — INSTRUMENT GATES (a run is void unless these pass)

- **G1** — every `.arz` re-hashed at load; any digest drift = HALT.
- **G2** — the beacon walk must reach a **fixed point** (no unexplored `.dbr` reference) or explicitly
  list what it did not reach.
- **G3** — the roster re-read must be a **control against Lap R on 169/169**; disagreement = HALT-diagnose.
- **G4** — the `.map` arbitration must run **both readings on the identical byte buffer**, with the
  buffer's sha256 recorded.
- **G5** — no number enters `pm4t_findings.md` without a basis string naming its record path + field
  (or its emitting lap, for carried constants).

---

## § 7 — GRADING VOCABULARY (fixed)

**MEASURED** — read from bytes, no assumption beyond the format.
**INFERRED-WITH-EVIDENCE** — a named assumption, stated, with the evidence for it.
**INDICATIVE** — direction trustworthy, magnitude not.
**UNREACHED** — looked for, not found; what was tried is stated.
**MEASURED-NEGATIVE** — the thing was searched for exhaustively in a place where it would have to
be, and provably is not there.

---

## § 8 — THE OUTCOME FIREWALL, RESTATED

I do not read sim T-scorecards. I do not know, and will not look up, whether a faster or slower
march grades better. **If limb (a) removes the run's leading explanation for the arrival gap, that
is the finding, and it is reported at full strength.** Named in advance so it cannot be softened
after the fact.
