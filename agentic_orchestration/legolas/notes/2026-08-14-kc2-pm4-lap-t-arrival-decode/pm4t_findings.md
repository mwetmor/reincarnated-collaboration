# RUN KC2-PM4 — LAP T — THE ARRIVAL DECODE

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR)
**Fired under:** R-PM4-49 part 4 (ledger row L-40) · **Date:** 2026-08-14
**Discipline:** GL-12 DECODE-NEVER-ESTIMATE · outcome-firewalled · NOTE-9 basis on every number ·
FULL 64-hex sha256 on every input and output · read-only on every external source.

**Pre-registration:** `PREREGISTRATION.md`, sha256
`05ff859b7520920ea36f0c1e354207e98b9994196509ef4f2a1ea0a1847b045a`, written and hashed
**2026-08-14T16:40:27Z — before any instrument ran**, recomputed EXACT at landing. Every
threshold and verdict rule below appears there first. Reconnaissance that preceded the hash is
declared in its § 0, including the fact that limb (a)'s headline was already observed.

---

## 0. HEADLINE — the residual was never a speed term, and my own Lap S instrument was broken

| # | finding | number |
|---|---|---|
| **1** | **⚑ THE BEACON DOES NOT TOUCH MOVEMENT. `UNREACHED-S2` CLOSED AS MEASURED-NEGATIVE.** The beacon's mechanical chain is **4 records, fixed point, nothing missing**. Its entire effect surface is `characterAttackSpeedModifier = 30.0`, `characterSpellCastSpeedModifier = 50.0`, `skillTargetRadius = 8.0`. The buff record carries **23 run-speed-family slots — ALL PRESENT, ALL ZERO.** The shipped Lua comment *"Spawn Beacons accelerate monster movement in their spawn areas"* **is a misdescription of the record it documents.** | **0** movement terms of 23 slots |
| **2** | **⚑ NOTHING ELSE ACCELERATES THE MARCH EITHER.** `characterRunSpeedModifier` is **0.0 on all 790 roster records**. All three Crucible wave-scaling records (`balancingadjustment_survivalmode_enemies01/02/03`) carry the full 23-slot run-speed surface **at zero**, while scaling life, OA, DA, attack speed, cast speed and damage by wave index. **The Crucible scales everything except movement.** | **0** of 3 scaling records |
| **3** | **⚑ `D-I19-3` ARBITRATED — AND I LOST. THE TWO DECODES NEVER DISAGREED.** With the `.map` placement array parsed correctly, the head-section `PatrolPoint_Attack` group's GUIDs match placement records **exactly**, and their positions agree to **0.000 m** (max 0.009 m) across **18 of 20 arenas / 205 patrol points**. The 0.45–13.28 m "disagreement" gamora reported was **entirely an artefact of my Lap S reader**. **Gamora's/the sim's head-section reader was right.** | residual **0.000 m** |
| **4** | **⚑ `D-T-3` — MY LAP S `.map` READER WAS UNSOUND, AND ITS QUALITY GATE MEASURED NOTHING.** The placement record is **variable-length** (`[rot 36][pos 12][u32 flag][if flag: GUID 16][u32 index]` = 56 or 72 bytes). Lap S assumed a fixed 56. On one map it therefore **skipped 509,756 times over 2,039,024 bytes** to collect `declared` many gate-passing windows. Lap S's published *"parsed/declared, 11 of 20 maps at 100 %, worst 97.67 %"* is **~100 % by construction** and is not evidence of a clean parse. | **509,756** resyncs |
| **5** | **⚑ `U-S-2` IS DECIDED BY DECODE: **NEAR**, NOT CENTROID — AND IT IS NEITHER ARM EXACTLY.** `ControllerMonsterStatePatrol::OnBegin` (Game.dll `0x105230`) calls `GetClosest(vector<UniqueId>&)` — a textbook nearest-by-squared-3-D-distance scan (init `+inf`, `comiss`/`jbe`) — and stores the returned **index** as the current patrol point. Traversal is then `(current + 1) mod n` (`MoveToNextPatrolPoint`, `0x1057b0`). **Entry is NEAREST; the walk is a cyclic sequence.** | **nearest-entry, cyclic** |
| **6** | **⚑ THE ARRIVAL ARITHMETIC CLOSES ON THE NEAR ARM WITH NO SPEED BOOST INVENTED.** Corrected march distances: **NEAR 16.80 m**, **RING 35.88 m**. Calibrated monster march **3.06–3.21 m/s**. **t_NEAR = 5.23–5.50 s = 1.05–1.11× the referent's measured t→90 % of 4.97 s.** t_RING = 11.18–11.74 s = **2.25–2.36×**. | **NEAR 1.05–1.11×** |
| **7** | **⚑ AND F-10 IS NOT A LIKE-FOR-LIKE VALIDATION CURVE.** Lap S's referent ramp is a **living-plate** count — it *"ramps over ~4–6 s and then drains"*, its per-wave `min` returns to **0**, and Lap S finding 6 proved plates are frustum-limited to **≤ 11.6 m**. It is the peak of a *population* (arrivals minus kills, truncated at 11.6 m). A sim curve over *fraction-of-wave-arrived* is a **monotone cumulative** curve over the whole arena. **These are different functionals and their t→50 % values are not comparable.** | peak plates **19–36** |

**The shape, in one sentence.** The run went looking for a missing *speed* term, and the game's own
bytes say there is none anywhere — not on the beacon, not on the rosters, not in the Crucible's
wave scaling; **what was missing was the march DISTANCE (`U-S-2`), which the binary now decides,
and part of the remaining gap is a comparison between two different measurements.**

---

## 1. Inputs — every one hashed before use (GL-6)

Full 64-hex digests for all 15 corpus containers, 3 shipped binaries, 4 carried lap artifacts,
9 instruments and 17 outputs are in **`pm4t_digests.json`**. Heads:

| input | sha256 (FULL 64-hex) |
|---|---|
| `mods/survivalmode/database/SurvivalMode.arz` | `e9f6e2213eada8f5ffcc4fc430395b43c95384b745b629def096dbb2e7da29b6` |
| `survivalmode3/resources/Maps.arc` | `94e20abadfce0f92d5187ab20bb8a9510fca9163e2b5b67b038cb55953f34911` |
| `vendor/grim-dawn/Game.dll` | `4876d6bdb69cca71cfa987652cbd7a42cf6d5578564d02d09aaf9b55c078ab02` |
| `…/lap-s-arena-advance/pm4s_arena_placements.csv` | `d553960f58f8cf38f73b490c4b47ca1999fc31821f10eb810de97621d1c5ee90` |
| `…/lap-p-sustain-engine/pm4p_leech_resistance.csv` | `cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e` |
| `PREREGISTRATION.md` | `05ff859b…847b045a` — **recomputed EXACT** |

**Corpus scope.** A new layered reader (`pm4t_arz_2026_08_14.py`) indexes all **8** `.arz`
archives — **84,829 unique record paths** — under a declared override order. The order is an
**assumption** about mod stacking; every finding below states which archive owns its record, and
all the load-bearing beacon records resolve in a **single layer** (`SurvivalMode.arz`), so the
assumption is not load-bearing for limb (a).

**Carried constants, each with its emitting lap named (NOTE-9):** player `characterRunSpeed = 0.93`
and `playerRunSpeedCapMax = 135.0` (Lap R) · player world speed **4.029485 / 3.836070 m/s**
(banked at L-38, px-LO / px-HI) · referent ramp **t→50 % 3.27 s / t→90 % 4.97 s** (Lap S F-10) ·
`placementExtents = 8.0` (Lap S F-2).

---

## 2. LIMB (a) — `UNREACHED-S2`, THE BEACON MAGNITUDE. **CLOSED.**

### 2.1 The chain, walked to a fixed point

Instrument **I-T1** expands only through an explicit allow-list of fields that mean *"this record's
own behaviour runs through that record"* (`initialSkillName`, `buffSkillName`, `controller`,
`skillName1..17`, …). Reached **4 records, 0 missing, fixed point TRUE**:

| depth | record | class | archive | fields | reached via |
|---|---|---|---|---:|---|
| 0 | `records/creatures/traps/spawnbeacon.dbr` | `Monster` | `SurvivalMode.arz` | 924 | — |
| 1 | `records/skills/misc/spawnbeacon_aura.dbr` | `Skill_BuffRadiusToggled` | `SurvivalMode.arz` | 4 | `initialSkillName`, `skillName1` |
| 1 | `records/controllers/pets/controller_trapmortar.dbr` | `ControllerStationaryMonster` | `database.arz` | 63 | `controller` |
| 2 | `records/skills/misc/spawnbeacon_aura_buff.dbr` | `SkillBuff_Passive` | `SurvivalMode.arz` | **594** | `buffSkillName` |

Two references are captured as **declared leaves, deliberately not expanded**:
`factions → faction_aetherial.dbr` (a peer-listing of faction members, not a mechanic this record
runs) and `charAnimationTableName → anm_groble.dbr` (an art asset). Both are recorded in
`pm4t_beacon_summary.json`.

**The Lua is a pass-through.** `game/survival/eventcontrol.lua` (extracted from three `Scripts.arc`
archives; the three digests are in `pm4t_digests.json`) does nothing but
`Entity.Create("records/creatures/traps/spawnbeacon.dbr")` at five `ScriptEntity` coordinate
carriers, and re-creates them on event reset. **All beacon mechanics live in the `.dbr` chain.**
The F-12 comment is line 41 of that file.

### 2.2 ⚑ The complete effect surface — three numbers

`spawnbeacon_aura_buff.dbr` has **594 fields**. Every one of them is zero/empty except:

| field | value | grade |
|---|---|---|
| `characterAttackSpeedModifier` | **30.0** | MEASURED |
| `characterSpellCastSpeedModifier` | **50.0** | MEASURED |
| `skillTargetRadius` | **8.0** | MEASURED |
| `skillMaxLevel` | 1 (**no rank array**) | MEASURED |
| `hideFromUI` / `cameraShakeAmplitude` | True / 0.12 | cosmetic |

**Uptime:** the search for `cooldown` / `duration` / `energyCost` / `lifetime` / `chargeLevel`
across the whole chain returns **NOTHING non-zero**. Combined with `Skill_BuffRadiusToggled` +
`instantCast = True` + delivery through `initialSkillName`, the aura is **on from creation,
unconditional, permanent**. (**P-A4 HELD.**)

### 2.3 ⚑ The load-bearing negative, stated at full strength

The buff record carries the run-speed slots **and leaves them empty**:

```
characterRunSpeed                     = 0.0     characterRunSpeedModifier            = 0.0
offensiveSlowRunSpeedChance           = 0.0     offensiveSlowRunSpeedMin/Max         = 0.0
offensiveSlowRunSpeedDurationMin/Max  = 0.0     offensiveSlowRunSpeedModifier        = 0.0
offensiveSlowRunSpeedGlobal/XOR       = False   offensiveSlowRunSpeedModifierChance  = 0.0
offensiveSlowRunSpeedDurationModifier = 0.0     retaliationSlowRunSpeed* (11 slots)  = 0.0/False
```

**23 slots, all present, all zero.** The over-broad pattern search (21 substrings incl.
`runspeed`, `movespeed`, `walkspeed`, `pathmass`, `charge`, `haste`, `velocity`, `locomot`) finds
**no non-neutral movement term anywhere in the chain**. The templates
(`skill_buffradiustoggled.tpl`, `skillbuff_passive.tpl`, resolved from `templates.arc`) declare
**no movement variable** either.

The only non-neutral movement-pattern hits in the whole chain belong to the **beacon's own body** —
`characterRunSpeed = 0.8`, `pathMass = 2.0`, `pathingSize = Small`, `min/maxRotationSpeed = 2/3` —
which is a `ControllerStationaryMonster` trap that never moves, and `TeleportToLeaderDistance =
99999.0` on that controller.

> **VERDICT (pre-registered in § 2 of the prereg, fired without discretion): `UNREACHED-S2` CLOSES
> as MEASURED-NEGATIVE on the movement claim. The beacon accelerates ATTACK and CAST, not
> movement. `D-I19-4`'s signed march-speed bias DOES NOT EXIST. DO NOT FOLD A SPEED BOOST.**
> This is the F-11 jitter precedent exactly: authored intent, unimplemented mechanic — except here
> the intent lives in a *comment* rather than an unconsumed field.

**I pre-committed to reporting this at full strength even though it removes the run's leading
candidate explanation for the arrival gap (prereg § 8). It does. That is the finding.**

### 2.4 What the beacon actually is worth — and P-A5, settled by geometry

Recomputed from the **corrected** placement reader (§ 4), over 110 tier-16 spawn points / 18
complete arenas:

| quantity | value | grade |
|---|---|---|
| beacons per arena | **5** on every complete arena | MEASURED |
| spawn point → nearest beacon | min **0.24**, median **10.47**, mean **12.41**, max **36.04** m | MEASURED |
| **tier-16 spawn points inside an 8 m beacon aura** | **36 of 110 = 32.7 %** | MEASURED |

**⚑ `D-T-2` — this corrects my own Lap S F-12.** Lap S reported the beacons as *"0.36 m from spawn
points"*. That is the **minimum-distance case reported as if typical**: 24 of 98 beacons do sit
within 0.5 m of *some* spawn-point-like entity, but against the **tier-16** spawn set the median
separation is **10.47 m**, and **two thirds of tier-16 spawn points are not in a beacon aura at
all**. F-12's placement claim is regraded.

**P-A5 (stacking) is MOOT, not UNREACHED.** The engine's rule for stacking two identical passive
buffs is not decodable from records — but it does not need to be: even where auras do overlap, the
buff carries no movement term, so the stacking rule cannot move the march. The attack/cast buff it
*does* carry reaches a third of spawn points and is left behind within the first 8 m of a 16.8–35.9 m
march.

---

## 3. LIMB (b) — MARCH-SPEED PRICING

### 3.1 The records side — three independent negatives

| test | result | grade |
|---|---|---|
| **P-B1** control vs Lap R | `characterRunSpeedJitter` distinct values **{0, 10, 15, 20, 25, 30}** — **identical to Lap R § 5.2**; engine caps re-read identical (`monsterRunSpeedCapMax = 500.0`, `monsterRunSpeedCapMin = [20, 25, 30]`, `playerRunSpeedCapMax = 135.0`) | **HELD** |
| **P-B2** Crucible wave scaling | `survivalinfo.dbr` → `balancingadjustment_survivalmode_enemies01/02/03`. All three carry **627 fields, 37 non-neutral**, scaling `characterLifeModifier`, `characterOffensive/DefensiveAbility`, `characterAttackSpeedModifier`, `characterSpellCastSpeedModifier`, `offensiveTotalDamageModifier`, `spawnMin/MaxAdj`, … **by wave index** — and the entire 23-slot run-speed surface is **zero on all three** | **HELD** |
| roster base modifier | `characterRunSpeedModifier` **= 0.0 on 790/790 roster records** | MEASURED |

### 3.2 The roster table — MEASURED scalars

`characterRunSpeed` on all **790** roster records (`pm4t_march_speed.csv`), 0 missing from corpus:

| classification | n | median | min–max | distinct | jitter values | `runSpeedModifier ≠ 0` |
|---|---:|---:|---|---:|---|---:|
| Boss | 19 | **1.10** | 1.00 – 1.52 | 7 | {0} | 0 |
| Champion | 188 | **1.00** | 0.00 – 1.55 | 20 | {0,10,15,20,25,30} | 0 |
| Common | 110 | **1.00** | 0.00 – 2.00 | 21 | {0,10,15,20,25,30} | 0 |
| Hero | 388 | **1.00** | 0.60 – 2.00 | 18 | {0,10,15,20,25,30} | 0 |
| Quest | 85 | **1.00** | 0.66 – 1.45 | 12 | {0,10,15,25} | 0 |
| **pooled** | **790** | **1.00** | 0.00 – 2.00 | 36 | — | **0** |

Two bodies carry `characterRunSpeed = 0.0` (immobile by record); they are **counted, never averaged
in**. Jitter is **not** folded — Lap S proved it MEASURED-NEGATIVE at consumption (`F-11`).

### 3.3 ⚑ P-B3 — movement skills exist, and I was partly wrong about them

Walking every roster record's own skill/controller chain (depth 3) found **592** movement-term hits.
Splitting them by the *class that carries them* — which my first classifier did **not** do
correctly (**`D-T-4`**, self-caught: it filed on-life/on-hit triggers as "permanent"):

| bucket | classes | roster bodies | values |
|---|---|---:|---|
| **ALWAYS-ON** | `Skill_Passive`, `SkillBuff_Passive` | **65 / 790 (8.2 %)** | +10, +15, +20, +25, **+60** % |
| **CONDITIONAL TRIGGER** | `Skill_PassiveOnLifeBuffSelf`, `…OnHitBuffSelf` | 32 / 790 (4.1 %) | +15 … +100 % (enrage below a life threshold) |
| **TRANSIENT SKILL** | `Skill_AttackWeaponCharge`, `…PathCharge`, `…WeaponBlink`, `Skill_Shapeshift`, `Skill_BuffSelfDuration`, … | 224 / 790 (28.4 %) | −35 … **+500** % |

**P-B3 is HELD in direction and CORRECTED in detail:** the dominant class is transient (charges at
+100/+120/+150 %), **but 8.2 % of the roster does march permanently faster** — the hero archetypes
`swift` (+10) and `unstoppable` (+15), rally/frenzy/sand auras (+15/+25), and a cave-spider passive
(+60). My prereg implied there were none; there are.

**Bound on the effect:** 8.2 % of bodies at a median ~+20 % raises the pooled march rate by
**≈ 1.6 %** — two orders below the NEAR/RING question (2.1×). It is named, bounded, and does not
move any verdict.

### 3.4 The unit — route 1 FAILED as pre-registered (**P-B4 HELD**)

- `Character::GetRunSpeed(bool)` (Game.dll `0x54750`) — its only float literals are
  **0.01, 1.0, 100.0**. It is percent arithmetic and returns a **multiplier**, not a world rate.
- `Character::GetSpeed()` (`0x5caa0`) — literally `sqrt(vx² + vy² + vz²)`. A **query** of the
  physics velocity, not its producer.
- The `bool` argument is the **walk/run selector**, and every one of the **54** tier-16 proxies
  carries **`chanceToRun = 100.0`** — so **every dispensed pack RUNS**. (MEASURED.)
- `delayedRun = True` on all 54 is **not** a march delay: `Proxy::DelayedRun` (`0x351d10`) is a
  one-shot state gate that calls `Proxy::RunProxy` — it is the *spawn* trigger the Lua fires.
  **MEASURED-NEGATIVE as an arrival-timing term.**

**The scalar→world-rate conversion is not recoverable as a literal from the stripped release
binary. Route 1 lands UNREACHED (`UNREACHED-T1`).**

### 3.5 Route 2 — player calibration. **INFERRED-WITH-EVIDENCE, carried as a bracket**

All three player quantities are independently measured by earlier laps:

```
K = v_world / (characterRunSpeed × modifier) = v / (0.93 × 1.35) = v / 1.2555
    px-LO:  4.029485 / 1.2555  =  3.209466 m/s per unit
    px-HI:  3.836070 / 1.2555  =  3.055412 m/s per unit
```

> **THE NAMED ASSUMPTION: player and monster share one locomotion constant `K`.** It is not
> decoded. It passes one sanity check worth stating — monster median `characterRunSpeed` (1.00)
> **exceeds** the player's base (0.93), so the player only outruns the board via the +35 %
> modifier, which is how the genre works and how the referent video reads. The table is graded
> **INFERRED-WITH-EVIDENCE** and carried on **both px edges, never as a point**.

| classification | median runSpeed | m/s px-LO | m/s px-HI | t_NEAR (16.80 m) | t_RING (35.88 m) |
|---|---:|---:|---:|---:|---:|
| Boss | 1.10 | 3.530 | 3.361 | **4.76 – 5.00 s** | 10.16 – 10.68 s |
| Champion / Common / Hero / Quest | 1.00 | 3.209 | 3.055 | **5.23 – 5.50 s** | 11.18 – 11.74 s |
| **pooled** | **1.00** | **3.209** | **3.055** | **5.23 – 5.50 s** | **11.18 – 11.74 s** |

---

## 4. LIMB (c) — `D-I19-3` ARBITRATED, AND MY OWN INSTRUMENT AUDITED

### 4.1 The two structures, decoded

**READING A — head-section group.** Immediately after the `.map` header the file carries, in
plain form: `u32 len | "PatrolPoint_Attack"` (the **group name**), `u32 len | "Patrol Points"`
(the field name), `u32 count`, then `count ×` `{ 16-byte GUID | u32 len + dbr path | 16-byte GUID
| 3 × f32 position }`. **Self-describing, zero heuristics.** The group name is
`PatrolPoint_Attack` on **all 20 maps**.

**READING B — placement array.** Lap S's reader, filtered to `patrolpoint_01.dbr` rows.

### 4.2 ⚑ `D-T-3` — the defect, in my own Lap S limb (a)

The placement record is **variable-length**:

```
[ 9 × f32 rotation | 3 × f32 position | u32 has_guid | if has_guid: 16-byte GUID | u32 string_index ]
       has_guid == 0  ->  56 bytes        has_guid == 1  ->  72 bytes
```

**GUID-bearing records are exactly those an authored group can reference by id — which includes
every member of `PatrolPoint_Attack`.** Lap S assumed a fixed 56 bytes, so on a 72-byte record it
read the GUID's first four bytes as the string index, found it out of range, rejected the record,
and advanced 4 bytes to resync.

On `survivalmode3:survivalworld_c` that happened **509,756 times, consuming 2,039,024 bytes**,
while collecting exactly `declared` (536) accepted windows spread across **~2 MB**. The first
rejection was at record **#0** — the array does not even begin where the reader assumed
(it begins at `arr_off + 8`, not `arr_off + 4`).

> **⚑ AND THE QUALITY GATE LAP S PUBLISHED MEASURED NOTHING.** *"11 of 20 maps parse 100 %, worst
> 97.67 %"* was offered as evidence of a clean parse. The loop terminates when it has collected
> `declared` many gate-passing windows **from anywhere downstream**, so the ratio is ~100 % by
> construction whenever enough such windows exist. **It was not evidence of anything, and I
> reported it as though it were.**

### 4.3 The corrected reader, and the verdict

`pm4t_map_v2_2026_08_14.py` parses strictly and sequentially with **no resync heuristic** — a
malformed record **HALTS** the parse and the shortfall is reported instead of back-filled.

- **18 of 20 maps parse COMPLETELY** (parsed == declared), **9,205 placements**.
- 2 maps HALT honestly (`survivalworld_d`, both copies, record 138/139, rotation not orthonormal) →
  **`UNREACHED-T2`**, reported, not patched.
- **Cross-check:** on every complete map, **head-group GUIDs matched placement records
  100 %** — 9–12 of 9–12 — with **position residual 0.000 m** (max 0.00907 m on two maps).

> **VERDICT (P-C1/P-C2 falsified, P-C3 superseded): THE TWO DECODES NEVER DISAGREED. They read the
> SAME points, which agree to the millimetre. The 0.45–13.28 m spread gamora measured was
> generated entirely by my Lap S reader dropping every grouped placement and back-filling the count
> with unrelated rows. `D-I19-3` is CLOSED: the sim's L-46 head-section reader is CORRECT; the
> defect is MINE.**
>
> I pre-committed in prereg § 4 to saying so plainly if my reader lost, and to naming what it
> contaminates. It lost.

### 4.4 What Lap S's numbers actually cost — the honest diff

| quantity | Lap S published | **corrected** | delta |
|---|---:|---:|---:|
| **F-3** spawn → patrol **centroid**, median | 37.03 m | **35.88 m** | **−3.1 %** |
| F-3 mean / min / max | 34.36 / 3.56 / 51.42 | **33.08 / 1.70 / 52.68** | — |
| **F-4** spawn → **nearest** patrol, median | 17.07 m | **16.80 m** | **−1.6 %** |
| F-4 mean / min / max | 16.09 / 0.65 / 37.51 | **15.85 / 0.00 / 35.35** | — |
| **F-5** spawn pairwise max, range | 59.2 – 85.4 m | **59.21 – 85.37 m** | **unchanged** |
| tier-16 spawn points per arena | **4 – 6** | **6 on every complete arena** | Lap S **under-counted 6 arenas** |
| n (spawn points) | 114 over 20 arenas | 110 over **18 complete** arenas | — |

**⚑ The defect was severe in mechanism and small in consequence.** Lap S's aggregate distances
survive within **1.6–3.1 %**, because the dropped rows were a modest fraction and the surviving
rows were representative. **Lap S's headline — that the spawn *scale* agrees with the sim and the
residual is *structure* — is NOT overturned; it is confirmed on a sound parse.** What genuinely
changes is the spawn-point census (every arena has 6, not 4–6) and the beacon placement claim
(§ 2.4).

---

## 5. LIMB (d) — `U-S-4` RESIDUE, AND `U-S-2` DISCRIMINATED

### 5.1 The patrol surface is in the readable module, not behind the DRM

`Game.dll` exports **48** patrol symbols (Engine.dll: 0). The load-bearing ones:

| symbol | RVA | what it says |
|---|---|---|
| `Monster::GetPatrolPoints() const → const mem::vector<UniqueId>&` | `0x2d2fd0` | the group is an **ORDERED VECTOR** |
| `Monster::SetPatrolPoints(const mem::vector<UniqueId>&)` | `0x2d2fc0` | assigned externally (by the proxy / map link) |
| `ControllerMonster::GetCurrentPatrolPoint() const → unsigned` | `0x0faf60` | current point is an **INDEX** |
| `ControllerMonster::SetCurrentPatrolPoint(unsigned)` | `0x0faf70` | — |
| `ControllerMonsterStatePatrol::OnBegin()` | `0x105230` | **entry selection** |
| `ControllerMonsterStatePatrol::MoveToCurrentPatrolPoint()` | `0x1054e0` | — |
| `ControllerMonsterStatePatrol::MoveToNextPatrolPoint()` | `0x1057b0` | **traversal** |
| `ControllerMonsterStatePatrol::EndOfPathReached()` / `PathFailed()` | `0x105460` | advance trigger |
| `PatrolPoint::GetRadius() const → float` | `0x0b68d0` | per-point **arrival tolerance** (`this+0x3dc`) |
| `PatrolPoint::ShouldRunTo() const → bool` | `0x0b68e0` | per-point **run-vs-walk** flag (`this+0x3e0`) |

### 5.2 ⚑ The decoded semantics

**Entry — `OnBegin` (`0x105230`):**

```
lea  eax, [ecx + 0x4dc]          ; the patrol-point vector
call ?GetClosest@...@(const mem::vector<UniqueId>&)
cmp  ecx, -1
jne  set_current                 ; -1 -> SetState("Return")
set_current:
mov  dword ptr [eax + 0x4e8], ecx   ; current patrol point = returned INDEX
```

**`GetClosest` (`0x0d2710`)** is textbook nearest-selection, fully read:

```
best_d2 = +inf            ; the literal at 0x10589320 IS +inf
best_i  = -1
for i in 0 .. n-1:                       ; stride 0x10 = 16 bytes per UniqueId
    e = Resolve(vector[i]);  if (!e) continue
    if (!e->predicate())     continue
    d2 = dx*dx + dy*dy + dz*dz           ; SQUARED 3-D distance
    if (best_d2 > d2) { best_d2 = d2; best_i = i }   ; comiss / jbe
return best_i
```

**Traversal — `MoveToNextPatrolPoint` (`0x1057b0`):**

```
n       = (end - begin) >> 4
current = (current + 1) mod n            ; div; remainder -> current.  WRAPS.
MoveToCurrentPatrolPoint()
```

> **⚑ `U-S-2` IS DISCRIMINATED BY DECODE, AND THE ANSWER IS NEITHER ARM AS FRAMED.** A pack does
> **not** march to the group **CENTROID** (the RING arm is wrong as a *first-march* comparator),
> and it does not merely march to the nearest point and stop. It **enters at the NEAREST patrol
> point by squared 3-D distance, then walks the group cyclically.** The correct first-march
> distance is the **NEAR** family — **16.80 m corrected** — and the RING family (35.88 m) describes
> where the pack ends up *circulating*, not how far it travels to first contact.
>
> **R-PM4-27 part 3 is honored:** this is decided by a decoded relation, not by which arm graded
> better. I did not look at a scorecard.

### 5.3 The honest caveat, stated in advance of any fold

This decodes the **`ControllerMonsterStatePatrol`** state. Whether a Crucible attack-pack occupies
that state for its whole march, or transitions to `MonsterStatePursue` / `MonsterStateMove` on
sighting the player, is **NOT decoded** — the state-machine transition table is not exported.
Evidence that Patrol is the march state: `MoveToCurrentPatrolPoint` is one of the 25 call sites of
`Character::GetRunSpeed`; the group is literally named **`PatrolPoint_Attack`**; and the proxies set
`chanceToRun = 100`. That is strong but it is not a decode. **Graded
INFERRED-WITH-EVIDENCE and carried as `U-T-1`.**

`ControllerMonsterStatePursue::OnBegin` (`0xff1d0`) is also a `GetRunSpeed` caller, so the pursue
path is speed-driven the same way; the *distance* it covers is what remains open.

---

## 6. THE ARRIVAL STORY, ASSEMBLED

| term | value | grade |
|---|---|---|
| monster march speed, pooled median | **3.055 – 3.209 m/s** | INFERRED-WITH-EVIDENCE (§ 3.5) |
| **first-march distance (NEAR, decoded arm)** | **16.80 m** | MEASURED |
| circulation distance (RING/centroid) | 35.88 m | MEASURED |
| **t_march NEAR** | **5.23 – 5.50 s** | INFERRED-WITH-EVIDENCE |
| t_march RING | 11.18 – 11.74 s | INFERRED-WITH-EVIDENCE |
| referent t→90 % peak | **4.97 s** | MEASURED (Lap S F-10) |
| **NEAR ÷ referent t→90 %** | **1.05 – 1.11 ×** | — |
| RING ÷ referent t→90 % | 2.25 – 2.36 × | — |

**⚑ With `U-S-2` resolved to NEAR, the decoded march reproduces the referent's measured 90 %-arrival
time to within 5–11 %, with NO speed term invented anywhere.** The board does not build 3–5× too
slowly because the monsters are too slow; it built too slowly because the sim was pricing a march
**2.1× too long**, and because part of the measured gap is a comparison artefact (§ 7).

---

## 7. ⚑ F-10 IS NOT A LIKE-FOR-LIKE VALIDATION CURVE — a caution, not a correction

R-PM4-46 part 3(e) made Lap S's F-10 the **pre-registered validation curve**, graded like-for-like.
Three MEASURED facts, all from Lap S's own artifacts, say the two sides are different quantities:

1. **F-10 counts LIVING plates.** Lap S § 3.4's own words: *"it ramps over ~4–6 s and then
   drains"*, and the per-wave `min` column returns to **0**. Peak plates is where **arrival rate =
   kill rate**, not where the board is built.
2. **Plates are frustum-limited.** Lap S finding 6: the farthest a nameplate ever appears is
   **11.08 – 11.64 m**; the tightest geometric limit is **6.39 – 6.71 m**. F-10 therefore measures
   arrivals **within ~11.6 m of the camera**, not arrivals in the arena.
3. **Peak plates is 19–36** — a visibility- and kill-saturated ceiling, not a wave census.

A sim curve over *fraction-of-wave-arrived* is a **monotone cumulative** function over the whole
arena; F-10 is the **peak of a population under simultaneous drain, truncated at ~11.6 m**. Their
t→50 % values are not comparable, and the direction is signed: **the cumulative curve must reach
its half-point later, mechanically, at any march speed.**

**This is a caution about the instrument, not a claim that the sim is right.** The cheap, decisive
test — recompute the sim's ramp on a **living count inside an 11.6 m window around the player**,
which is what the referent measured — costs nothing and makes the comparison like-for-like.
Graded **INFERRED-WITH-EVIDENCE**; published as **`U-T-2`**.

---

## 8. Departures from the pre-registration — all self-caught, all declared

| id | departure | direction of conservatism |
|---|---|---|
| **DEP-T1** | Prereg § 3 planned the march table from the roster's `characterRunSpeed` only. I additionally walked every roster record's **skill chain** (depth 3) and split terms by carrying class. | **Against my own lean** — it is what found the 8.2 % always-on modifiers that P-B3 implied did not exist. |
| **DEP-T2** | Prereg § 4 scoped limb (c) to *arbitrating* two readers. I went further and **rewrote the placement reader**, because the arbitration could not be settled without deciding whether either parse was sound. | Expands the defect surface **against Lap S**, i.e. against my own prior work. |
| **DEP-T3** | Prereg § 2 predicted P-A5 (stacking) would land UNREACHED. It lands **MOOT** — dissolved by the § 2.3 negative rather than answered. | Neutral; stated rather than quietly upgraded. |
| **DEP-T4** | § 7's F-10 caution was **not pre-registered under any limb**. It arose from limb (b)'s arithmetic. | Declared as an unregistered finding and graded INFERRED-WITH-EVIDENCE, **not** MEASURED. |

## 9. Instrument defects — all self-caught (FIT law)

| id | defect | disposition |
|---|---|---|
| **`D-T-1`** | I-T1 v1 walked **every** `.dbr`-valued field and followed `faction_aetherial.dbr` — a peer-listing — reaching **6,044** records and contaminating the load-bearing movement-term negative with unrelated nemesis creatures. | **REPAIRED** in v2 (explicit field allow-list, declared leaves). The negative in § 2.3 is from v2, scope **4 records**. |
| **`D-T-2`** | Lap S **F-12**'s *"0.36 m from spawn points"* is the minimum reported as typical; median spawn→beacon is **10.47 m** and 67 % of tier-16 spawn points are outside every aura. | **F-12 placement claim REGRADED** (§ 2.4). Does not affect the § 2.3 verdict. |
| **`D-T-3`** | Lap S `.map` reader assumed a fixed 56-byte placement record; the record is 56 **or 72** bytes. 509,756 resyncs over 2 MB; every grouped placement dropped; the published parsed/declared gate was **vacuous**. | **REPAIRED** by `pm4t_map_v2` (18/20 strict-complete). Lap S F-3/F-4 recomputed (§ 4.4); Lap S artifacts **not modified**. |
| **`D-T-4`** | My first permanent/transient classifier filed `Skill_PassiveOnLifeBuffSelf` / `…OnHitBuffSelf` as "permanent", over-counting always-on speed terms 115 → true **65**. | **REPAIRED** (§ 3.3 three-bucket split). |

**Gate status:** G1 all digests re-hashed at load, no drift · **G2** fixed point TRUE, 0 missing ·
**G3** Lap R control HELD on jitter + caps · **G4** both readings on the identical buffer, sha256
emitted per map · G5 every number in this file carries a record path + field or an emitting lap.

## 10. Prediction score

**HELD:** P-A2, P-A3, P-A4 (limb a) · P-B1, P-B2, P-B4 (limb b) · P-D1, P-D2.
**FALSIFIED:** **P-C1** and **P-C2** (the two readers do **not** read different structures and are
**not** both right — they read the same points and one parse was broken) · **P-D3** (U-S-2 was
predicted to stay UNDECIDED; it is **decided**) · **P-B5** in detail (predicted NEAR 5–7 s ✓ at
5.23–5.50 s, RING 11–15 s ✓ at 11.18–11.74 s — **both bands HELD**; the *speed* band 2.5–3.5 m/s
HELD at 3.06–3.21).
**CORRECTED:** P-B3 (transient dominance held; "no permanent terms" was wrong — 8.2 % carry them).
**MOOT:** P-A5. **NOT SCORED:** P-A1 (declared as already-observed recon).

**Score: 8 held · 3 falsified · 1 corrected · 1 moot.** The three falsifications are the lap's
most valuable output: two of them are defects in my own prior work.

## 11. UNREACHED census — honest per limb

| id | what | why |
|---|---|---|
| **`UNREACHED-T1`** | the `characterRunSpeed` → m/s **conversion constant** | Not recoverable as a literal from the stripped release binary; `GetRunSpeed` is percent arithmetic, `GetSpeed` is a velocity query. Route 2 calibration substitutes, graded INFERRED-WITH-EVIDENCE with its assumption named. |
| **`UNREACHED-T2`** | 2 of 20 arenas (`survivalworld_d`, both copies) | Strict parse HALTS at record 138/139 (rotation not orthonormal). Reported, **not** patched or back-filled. All § 4.4 statistics are over the **18 complete** arenas and say so. |
| **`UNREACHED-T3`** | the monster **state-transition table** | Not exported. Whether an attack-pack stays in `MonsterStatePatrol` for the whole march or hands off to `Pursue`/`Move` is inferred (§ 5.3), not decoded. |
| **`UNREACHED-T4`** | engine **stacking rule** for identical passive buffs | Not in records. **Moot** for the beacon (no movement term) but still open in general. |
| **`UNREACHED-T5`** | `PatrolPoint::GetRadius()` / `ShouldRunTo()` **values** | The accessors are decoded (`this+0x3dc`, `this+0x3e0`) but the fields are not in the `patrolpoint_01.dbr` record; they are set from the `.map` or defaulted in the unexported loader. |
| carried | `UNREACHED-S1` (`Proxy::AllKilled()` body, Steam-DRM `.bind`) · `UNREACHED-S3` (which arena Matt played) | unchanged by this lap |

## 12. UNDECIDED published — none ruled

| id | question | why it matters | what would decide it |
|---|---|---|---|
| **`U-T-1`** | does a Crucible attack-pack remain in `MonsterStatePatrol` for the whole march? | If it hands to `Pursue` on sighting, the march distance becomes spawn→**player**, a third comparator. | the state-transition table (unexported) or an in-game instrumented measurement |
| **`U-T-2`** | is the sim's arrival ramp measured on the same functional as F-10? | § 7 — the 3–5× gap is partly a comparison artefact of unknown size. | recompute the sim ramp as a **living** count inside an **11.6 m** window; costs nothing |
| **`U-T-3`** | does the beacon's **+30 % attack / +50 % cast** matter at all? | It reaches 33 % of spawn points and is left behind in the first 8 m of the march — but ambush packs (`ProxyAmbush`, 7 of 54) may fight *inside* it. | pack-by-pack dwell time inside the aura |
| **`U-T-4`** | the **8.2 %** always-on speed-modifier minority | bounded at ≈ +1.6 % pooled; foldable per-body if wanted. | already decoded — a fold decision, not a research one |

---

## 13. What I hand the conductor for I-20

| # | term | value | grade |
|---|---|---|---|
| **T-1** | **beacon movement effect** | **NONE — do not fold.** `D-I19-4`'s signed bias does not exist | **MEASURED-NEGATIVE** |
| **T-2** | beacon actual effect | `characterAttackSpeedModifier = 30.0`, `characterSpellCastSpeedModifier = 50.0`, `skillTargetRadius = 8.0`, permanent, no rank array; reaches **36 / 110** tier-16 spawn points | MEASURED |
| **T-3** | Crucible wave-scaling movement term | **NONE** on all three difficulty records | MEASURED |
| **T-4** | roster `characterRunSpeedModifier` | **0.0 on 790 / 790** | MEASURED |
| **T-5** | roster `characterRunSpeed` | pooled median **1.00**; Boss **1.10**; per-class table in `pm4t_march_speed.csv` | MEASURED |
| **T-6** | pack run flag | **`chanceToRun = 100.0` on all 54** tier-16 proxies — packs RUN | MEASURED |
| **T-7** | `delayedRun` | spawn trigger, **not** a march delay | MEASURED-NEGATIVE |
| **T-8** | **patrol semantics** | **enter at NEAREST by squared 3-D distance (`GetClosest`), then cyclic `(i+1) mod n`** | **MEASURED** (from Game.dll) |
| **T-9** | **`U-S-2`** | **NEAR arm is the first-march comparator. 16.80 m.** RING (35.88 m) is the circulation radius, not the march | **MEASURED** geometry + **MEASURED** selection rule |
| **T-10** | corrected F-3 / F-4 / F-5 | 35.88 / 16.80 m medians; pairwise max 59.21–85.37 m; **6 spawn points on every arena** | MEASURED (18 arenas) |
| **T-11** | monster march rate | **3.055 – 3.209 m/s** (both px edges) | **INFERRED-WITH-EVIDENCE** — assumption named |
| **T-12** | **arrival check** | **t_NEAR 5.23–5.50 s vs referent t→90 % 4.97 s = 1.05–1.11 ×** | INFERRED-WITH-EVIDENCE |
| **T-13** | always-on speed minority | 65 / 790 bodies, +10…+60 %; pooled effect **≈ +1.6 %** | MEASURED, bounded |
| **T-14** | **F-10 as validation curve** | **not like-for-like** — see § 7; re-measure the sim side as a living 11.6 m count | INFERRED-WITH-EVIDENCE |
| **T-15** | `D-I19-3` | **CLOSED — the sim's reader was right, mine was broken** | MEASURED |

**Law 3 note.** Every term above is decode-sourced or explicitly calibrated-with-a-named-assumption.
No constant here was chosen because it grades better; I did not read a scorecard, and the lap's
largest single finding removes the run's own leading hypothesis.
