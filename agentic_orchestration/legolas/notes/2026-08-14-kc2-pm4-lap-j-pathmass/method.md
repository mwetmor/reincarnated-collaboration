# LAP J (RUN KC2-PM4) — decode `pathMass` (cliff C-F6)

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **Date:** 2026-08-14
**Charter row:** L-16, ruling **R-PM4-19** · **Cliff closed:** **C-F6** (raised in Lap F § 8)
**Discipline:** GL-12 decode-never-estimate · NOTE-9 basis on every value · outcome-firewalled
(no sim output was read at any point in this lap)

---

## 0 — The one-line answer

`pathMass` is a **`GAME::Character` movement-manager field that weights how much a body resists
being displaced — doubled whenever the body is NOT locomoting.** The semantic is decoded from the
shipped binary, not guessed. **But the shipped `Game.dll` contains no call site that reads it**, so
the field is authored, loaded, transformed-on-demand — and, in this build, **consumed by nothing**.

**Semantic grade: split, and deliberately so.**

| claim | grade |
|---|---|
| field name, class, declaring templates, member offset, load path, per-record values | **MEASURED** |
| the runtime transform `GetPathMass() = field × (locomoting ? 1.0 : 2.0)` and the state gate | **MEASURED** (disassembled) |
| "it means resistance to displacement in body-vs-body separation" | **INFERRED-WITH-EVIDENCE** (six independent hooks, § 4) |
| "the shipped game's separation solver consumes it" | **MEASURED NEGATIVE** — it does not (§ 5) |

---

## 1 — Deliverable

| file | rows × cols | sha256 |
|---|---:|---|
| **`pm4j_pathmass.csv`** | **299 × 17** | `49bf92862c8f1876f098f922b8afbb403d76dc9bbf6b78005a965c4c71c0ba16` |

Companion: `emit.log` (the emitter's own census, verbatim).
Instrument: `agentic_orchestration/research/scripts/pm4j_emit_2026_08_14.py`.
It **re-implements nothing** — populations, the `.arz` reader (`E3.winner`, whole-record
replacement) and the roster roll are imported from Laps D and F, so no second population
definition exists to drift.

### Populations (NOTE-9 — every count names what it counts over)

| id | basis | n |
|---|---|---:|
| **P-ROLLED-20** | Lap D's frozen baton, `actors[]`, wave ∈ [151,170], **distinct records** | **169** |
| — | the same population counted as **actor instances** | **344** |
| **P-SUMMON-128** | Lap E's summon-only closure over the 663 band-B pool records (R-PM4-5) | **128** |
| **P-PLAYER-2** | `Class = Player`; identical on every field in this lap (asserted) | **2** |
| | **total rows emitted** | **299** |

⚑ **The commission's "344 records" is 344 *actor instances* over 169 *distinct records*.** Both
numbers are carried: `n_actors` is a column, so either basis is reconstructible without re-rolling.

---

## 2 — Q1: the field

| property | value | basis |
|---|---|---|
| **exact name** | **`pathMass`** | `templates.arc`, decoded from bytes |
| class / type | `variable` / `real` | template declaration |
| defaultValue | `1.0` | template declaration |
| description | ***empty*** — the corpus documents nothing | template declaration |
| declaring templates | **`character.tpl`**, **`characterenemy.tpl`** | corpus-wide scan of all 818 templates (817 decoded; the one failure is the same nameless `entry_type = 0` placeholder Lap E and Lap F both hit) |
| declaring **group** | **`"Movement Parameters"`** | template group structure |
| record class | reaches every body via `monster.tpl → Character.tpl` and `player.tpl → …` | Lap F's walked include-closure |
| **population / coverage** | **299/299 present — zero gaps** | `pm4j_pathmass.csv`, `path_mass_grade = MEASURED` on all 299 |
| C++ owner | **`GAME::Character`**, member at **offset `+0x1DDC`** | `Game.dll` disassembly |

**It is NOT the same field as `physicsMass`**, and the corpus keeps them rigorously apart:

| | `pathMass` | `physicsMass` |
|---|---|---|
| declaring template | `character.tpl` / `characterenemy.tpl` | `actor.tpl` |
| declaring group | **`Movement Parameters`** | **`Physics`** (with `physicsFriction`, `physicsRestitution`) |
| shipped module | **`Game.dll`** | **`Engine.dll`** |
| C++ symbol | `?GetPathMass@Character@GAME@@QBEMXZ` (non-virtual, `Character`) | `?GetPhysicsMass@Entity/Actor@GAME@@UBEMXZ` (**virtual**, `Entity`/`Actor`) |
| board census | 1.0 ×271 · 2.0 ×26 · 3.0 ×2 | 5.0 ×229 · 1.0 ×70 |

The two vary **independently** across the board — `physicsMass = 5.0` with `physicsFriction = 10.0`
on 229 bodies is a rigid-body/ragdoll material pair, and it is not the gameplay quantity.

---

## 3 — Q2: the values

`pm4j_pathmass.csv`; census reproduced verbatim from `emit.log`:

| population | 1.0 | 2.0 | 3.0 |
|---|---:|---:|---:|
| **P-ROLLED-20** (169 records) | **168** | **1** | 0 |
| P-ROLLED-20 **actor-weighted** (344 instances) | **339** | **5** | 0 |
| P-SUMMON-128 | 103 | 25 | 0 |
| P-PLAYER-2 | 0 | 0 | **2** |
| **board + player (299)** | **271** | **26** | **2** |

**Range across the roster + player: `1.0 … 3.0`. Three distinct values exist in the whole board.**
Emitted at full float32 precision, unrounded.

### ⚑ The finding that matters most to the fold

**The roster is effectively constant.** 168 of 169 roster records — **339 of 344 actor
instances — sit at the default 1.0.** The single roster exception is
`records/creatures/enemies/livingplant_a01.dbr` (a rooted plant) at 2.0.

**Consequence, stated factually:** a mass-weighted pairwise split keyed on `pathMass` is
**arithmetically identical to 50/50 for essentially every monster–monster pair on this board.**
The only pairs where it differs are (a) the five `livingplant_a01` instances, and (b) **every
player–monster pair**, where 3.0 vs 1.0 gives a **75/25** split — the monster yields three times
as far as the player. What this implies for the sim is the conductor's call, not mine.

### Which bodies are heavy

All 26 board bodies at 2.0 carry `avoidForce = 0.5` (the default) and `physicsMass = 1.0`. By
record identity they are overwhelmingly **rooted, stationary or hazard-class entities**:
`sandstorm`, `eldritchground`, `giantfire_moltenpool`, `siff_icefloe`, `beast_bloodpool`,
`chthonian02_void`, `loghorrean_void`, `krieg_aethertrap`, `trap_brambletrap_a01`,
`korvaak_lieutenant_02_trapsummon_{01,02}`, `necro2_nulltotem`, `outlaw2_aethershard`,
`nemesis_undead_02b_icecrystalsummon`, `firedevil_01`, `winddevil_01`, `bladeswarm_a01`,
`livingplant_a01(_summon)`. **17 of them carry `actorRadius = 0.0`** — Lap F's C-F4 point-bodies.

**The player is the unique maximum on two axes at once:** `pathMass = 3.0` (global max on the
board) **and** `avoidForce = 0.6` — the only non-`0.5` avoid force among all 299 bodies (the
other non-default is `0.0`, on 13 bodies). The player is the hardest thing to shove and the thing
others steer hardest around.

**Corroboration from the binary:** `GAME::Player::Player()` at rva `0x319707` initialises the
member **in C++** with `mov dword [ebx+0x1DDC], 0x40400000` = **3.0f**, and
`GAME::Character::Character()` at rva `0x3F252` with `0x3F800000` = **1.0f**. The DBR values and
the hard-coded constructor defaults **agree exactly**. Two independent authoring surfaces, same
numbers.

---

## 4 — Q3: what it MEANS — the evidence trail

### The decisive hook — `Character::GetPathMass()`, disassembled

`Game.dll`, export `?GetPathMass@Character@GAME@@QBEMXZ`, rva `0x59850`, decoded with
`objdump -d` (Apple LLVM 17, `coff-i386`) directly against the shipped PE:

```
mov   dword [ebp-4], 0x3F800000        ; mult := 1.0f
call  [vtbl+0x228]  ;  == Character::GetActionState()   (vtable slot resolved, § 4a)
cmp   eax, 5    / je  keep             ; Move
cmp   eax, 6    / je  keep             ; Walk
cmp   eax, 0x13 / je  keep             ; Jump
cmp   eax, 0x15 / je  keep             ; Evade
cmp   eax, 0x14 / je  keep             ; (Illegal — a hole in the enum)
mov   dword [ebp-4], 0x40000000        ; mult := 2.0f      <-- every OTHER state
keep:
flds  dword [esi+0x1DDC]               ; the DBR pathMass field
fmuls dword [ebp-4]
ret
```

⇒ **`GetPathMass() = pathMass_field × (ActionState ∈ {Move, Walk, Jump, Evade} ? 1.0 : 2.0)`**

**a. The gate is named, not guessed.** Vtable slot `+0x228` on `??_7Character@GAME@@6BObject@1@@`
resolves to `?GetActionState@Character@GAME@@UBE?BW4Character_ActionState@2@XZ`. The enum's 22
value-names were decoded from the jump table at rva `0x471A8` inside
`?GetActionStateAsText@…`: `0 Unknown · 1 Forced Stop · 2 Play Animation · 3 Idle · 4 Fidget ·
5 Move · 6 Walk · 7 Attack · 8 Stun · 9 Knockdown · 10 TakeHit · 11 Illegal · 12 Immobilize ·
13 Trap · 14 Pickup · 15 Chatting · 16 Illegal · 17 Fallen · 18 Dying · 19 Jump · 20 Illegal ·
21 Evade`.

**This is the single strongest semantic fact in the lap.** The exempt set is *exactly the four
locomotion states*. A body that is **standing, attacking, stunned, knocked down, taking a hit,
immobilised, trapped, fallen or dying weighs twice as much** as the same body while it is moving.
A quantity that doubles the moment a body stops moving is a **resistance-to-displacement** term.
It is not a pathfinding traversal cost — a traversal cost has no reason to depend on whether the
agent is mid-stride, and Grim Dawn's actual navmesh-footprint surface is a *different* field
(`pathingSize`, picklist `Small;Medium;Large`, and Lap F already showed it is monotone in
`actorRadius`).

### Corroborating hooks

**b. Template group.** `pathMass` is declared inside the group **`"Movement Parameters"`**, whose
other members are `avoidForce`, `tweakSpineOnTurn`, `pathGenerationStyle`, `minRotationSpeed`,
`maxRotationSpeed`, `disallowRotation`, `rotateWhenChatting`, `dbIgnoreWhenPathing`,
`allowedOffNavmesh`, `walkDistance`, `walkSpeed`, `walkUsesRun`, `disableMovement`. That last one
carries the only description in the group that names a subsystem: *"Character is never part of
**movement manager**."*

**c. `avoidForce` adjacency, in two independent orderings.** In `character.tpl` the variable
immediately **preceding** `pathMass` is `avoidForce` (real, default 0.5) — a neighbour-avoidance
steering force. Independently, in `Game.dll`'s own DBR field-name string pool the two literals are
**back-to-back**, 12 bytes apart (`avoidForce` @ file `0x4F2918`, `pathMass` @ `0x4F2924`), inside
a run reading `turnRate · avoidForce · pathMass · disallowRotation · rotateWhenChatting ·
deathAnimBlendTime · dbIgnoreWhenPathing`. An **avoid force** and a **mass** registered adjacently
is the classic steering pair (`acceleration = force / mass`).

**d. The load order is read from code, not inferred from the template.**
`?Load@Character@GAME@@UAEXABVLoadTable@2@@Z` (rva `0x414D0`) issues, in sequence:
`GetFloat("turnRate", …) → +0x9E8`, `GetFloat("avoidForce", 0.0f) → +0x9EC`,
`GetFloat("pathMass", <ctor default>) → +0x1DDC`, `GetBool("disallowRotation") → +0x1CB8`,
`GetBool("rotateWhenChatting") → +0x1CB5`. The pushed string pointer at `0x104F3D24` was
dereferenced and reads **`pathMass`** verbatim — the field/offset binding is measured, not assumed.

**e. `pathingSize` is registered elsewhere.** In the same string pool `pathingSize` sits ~1.1 KB
away (`0x4F3D08` region) among `characterRacialProfile · spawnEffect · numAttackSlots`, and the
pathfinding cluster proper (`tweakSpineOnTurn · pathGenerationStyle · allowedOffNavmesh`) is
separate again. **`pathMass` is not filed with the navmesh surface.**

**f. The value distribution agrees with the reading.** The heavy bodies are rooted hazards,
totems, traps and a plant — things that should not be shoved. The player, the one body the game
must never let the crowd push around, is the global maximum at 3.0 *and* the only body with a
raised `avoidForce`.

**g. The crowd subsystem exists and is named.** `Engine.dll` carries a `CROWD` namespace with
source-file strings `crowd.cpp · crowdmanager.cpp · crowdpath.cpp · crowdthread.cpp ·
proximitymap.cpp · agenthandle.cpp`, assertions (`"CrowdManager - Agent already in simulation!"`,
`"Must call ProximityMap::Prepare(numAgents) before adding agents!"`), and an `ICrowdAgent`
interface that `GAME::Character`/`Monster`/`Npc`/`Player` implement —
`CrowdAgentCreated/Update/Moved/Stopped/ReachedGoal/Error/Destroyed(CrowdAgentParams&)` and,
directly on point, **`?CrowdAgentDepenetrate@Character@GAME@@UAE_NW4CrowdAgentState@CROWD@@H0H@Z`**.
**The real game does run a depenetration step, and it is a `Character`-level virtual.**

---

## 5 — ⚑ The measured negative: nothing reads it

Having decoded the transform, I looked for the consumer. There is none.

| test | result |
|---|---|
| direct `call rel32` sites targeting `GetPathMass` (rva `0x59850`) across the whole of `Game.dll` `.text` | **0** |
| direct `call rel32` sites targeting `SetPathMass` (rva `0x59BE0`) | **0** |
| the VA `0x10059850` appearing as a **data** pointer in ANY section (`.text .rdata .data .gfids .tls .rsrc .reloc`) — i.e. a vtable slot, script binding or property table | **0** |
| modules anywhere in the install whose strings contain `?GetPathMass@Character@GAME@@QBEMXZ` (name-imports require the literal) | **1 — `Game.dll` itself** |
| **every** instruction in `Game.dll` `.text` bearing displacement `0x1DDC` | **7 sites, in 6 functions: `Character::Load` (×2), `Character::Character()`, `Npc::Npc()`, `Player::Player()`, `GetPathMass`, `SetPathMass` — and nothing else** |
| the same displacement in `Engine.dll` `.text` | 2 sites, both unrelated (`DayNightCycle::SetDefault`, `Options::Options`) — different classes |
| the same displacement in `Grim Dawn.exe` | 0 |

`GetPathMass` is non-virtual (`QBE`), so it cannot be reached through a vtable; it has no call
sites and no address-taken reference; and the member itself is touched **only** by the three
constructors, the DBR loader and the two accessors. If the function had been inlined into a
consumer, the inlined copy would still have to load `[reg+0x1DDC]` — and no such load exists.

I also read `Character::CrowdAgentCreated` (rva `0x526E0`) directly: it fills `CrowdAgentParams`
with constants (`[+0x0C]=0`, `[+0x10]=4`, `[+0x14]=6`, `[+0x18]=0.1f`, `[+0x2C]=0`, `[+0x30]=0`,
`[+0x34]=0x481`) and one computed float at `[+0x04]`. **`pathMass` is not among them.**

**Therefore:** in Grim Dawn Edition III as shipped, `pathMass` is **authored, defaulted in C++,
loaded from the DBR into a live member, and given a state-gated accessor — which nothing calls.**
It is a **dormant field**: the design intent is legible and measured; the runtime consumption is
absent.

**What this does and does not license.** It does license: "Crate modelled body mass as a
displacement-resistance weight that doubles when a body stops moving, set the player to 3× a
common monster, and made rooted hazards heavy." It does **not** license: "the real game's observed
crowd behaviour is produced by mass-weighted separation" — because the shipped build does not read
the field. Any sim fold that adopts a mass-weighted split is anchored to Crate's **authored
intent**, not to Crate's **runtime behaviour**, and the distinction must travel with the number.

---

## 6 — What was NOT determinable, named as absences

- **The arithmetic of the split.** No formula relating two bodies' path masses to a displacement
  ratio exists anywhere in the substrate — because no consumer exists. A 75/25 player–monster
  split is *my* arithmetic on the ratio 3:1, not the game's. **UNDECODABLE-FROM-SUBSTRATE.**
- **`CrowdAgentDepenetrate`'s policy.** The hook exists on `Character`/`Monster`/`Npc` (not on
  `Player`, not on `Entity`) with signature `(CrowdAgentState, int, CrowdAgentState, int) → bool`.
  It returns a **predicate** — whether a pair may be depenetrated — not a displacement split. Its
  body was not decoded in this lap; that is a separate question and I did not stretch this one to
  cover it. **NAMED ABSENCE.**
- **The `Grim Dawn Modding Guide.pdf`** shipped in the install was extracted (`pdftotext`, 73 KB of
  text) and searched for `pathMass · avoidForce · physicsMass · pathingSize · Movement · mass ·
  collision · navmesh`: **zero hits on all eight.** The guide does not document this surface.
  **DECLARED-GAP, dead end named** rather than left silent.
- **`avoidForce`'s consumer** was not isolated: its member offset `+0x9EC` collides with unrelated
  members of the `ItemEquipment`/`Weapon*`/`Armor*` classes, so the raw-displacement scan that is
  clean for `+0x1DDC` is confounded for `+0x9EC`. **No claim is made either way about
  `avoidForce`'s consumption** — the negative in § 5 is asserted for `pathMass` ONLY, where the
  scan is clean.

---

## 7 — Provenance

- **Data substrate:** `/Users/admin/Games/vendor/grim-dawn-edition-III-20260808/` — `database/templates.arc`, the `.arz` record corpus, read through Lap D's `E3` whole-record-replacement reader. **Read-only; nothing was extracted into the vendor tree.**
- **Binary substrate:** `/Users/admin/Games/vendor/grim-dawn/` — `Game.dll`, `Engine.dll`, `Grim Dawn.exe` and the shipped tool binaries. **Read-only.** PE export tables parsed with a purpose-written dependency-free parser (`/tmp/pm4j/pe.py`, scratch); disassembly by `objdump` (Apple LLVM 17) reading the PE as `coff-i386` with symbol resolution.
- **Outcome firewall:** no sim output, baton scoreboard or iteration result was opened at any point. The only imported artefacts are Lap D's frozen roster baton and Lap E's summon closure, both used solely to define *which bodies to look up*.
