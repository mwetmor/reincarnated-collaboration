# Findings — GD enemy AI: THE OWN-FILES INVENTORY (Step 1 of the enemy-AI commission)

**Seat:** legolas (`UNKNOWN-RESEARCHER`) · **Date:** 2026-09-29
**Commissioner:** gandalf (`RUN-CONDUCTOR`, Run KC2-PLAY), on Matt's T-C finding — ledger **KP-110**
**Matt, verbatim (the finding):** *"most importantly, I feel like the AI state of the enemies was smarter by a long shot in the video."*
**Matt, verbatim (the method):** *"commission the research, BUT start with our own files. We did extensive research in the past recording ALL grim dawn AI enemy states and statuses."*

**Scope of THIS piece:** inventory only. What we already hold · what is actually implemented · what is therefore still owed externally.
**Law 3 honoured.** Every row below is a path, a line, a count or a commit. Where our files disagree I print both readings and say so. No fitted behaviour, no plausible reconstruction. Read-only throughout.

---

## 0 · THE HEADLINE, IN FOUR LINES

1. **Matt is right, and our files already say why.** We hold a deep, mostly-MEASURED record of GD's enemy AI — the full 40-state controller table, 53 of 68 controller fields per-record, the six-limb alert gate, the anger economy, the distress-call system, per-monster wind-up and root-lock timings. **Almost none of it is implemented.**
2. **The oracle runs 7 behavioural states; the Godot port runs none.** `kc2/engagement.py:118-131` maps 24 decoded GD states onto 7 sim states and marks **17 of them `None` = UNREACHED**. The port has no state machine at all — monster behaviour is ~90 lines: a view gate, a straight-line walk, a halt radius, a modular swing clock.
3. ⚑ **`ABS-AI-STATE-KEYSPACE` IS ALREADY CLOSED BY OUR OWN FILES AND NOBODY NOTICED — and the pack's "43" is wrong.** See § 3. The key space is **40**, enumerated with byte offsets since 2026-07-25, and cross-checked by an independent MEASURED 36-name scan. The pack ships `n_states_enumerated: 43` with no enumeration behind it.
4. **The gap is not uniform — it is concentrated in exactly the four field groups that produce perceived intelligence.** Senses, AngerManagement, Pursuit and DistressCalls are the 15 fields the decode laps and the model pack both skip (§ 4.2). Detection, threat ranking, leash, and pack alert propagation. That is the shortlist for "smarter".

---

## 1 · SUBSTRATE CONSTRAINT THAT GOVERNS EVERYTHING BELOW

⚑ **The vendor trees are GONE.** `ls /Users/admin/Games/vendor/grim-dawn*` → no matches (verified this session). Both the Edition-III and Edition-II roots were lost in the 2026-09-10 / 09-17 disk sweep — the second sole-copy loss after the EoR recording. `/Users/admin/depots/` is the only readable game substrate and it is **Edition II** while every existing engine row is Edition III. Host action is filed as `matt_to_do` **T31** (restore an Ed-III tree; not blocking).

**Consequence for this commission, stated plainly:** every DATAMINED row in this map is currently **non-reproducible**. The scratch scripts that produced the parameter tables (`legolas/scratch/2026-07-31-wr3-w2/w1_fieldcensus.py` … `w10_allfields.py`; `research/scripts/mcd1_alert_decode_2026_08_24.py`) all require a vendor tree. We can still **read** what we banked; we cannot currently **re-derive or extend** it. By this project's own discipline a claim that cannot be re-derived is a memory of evidence, not evidence — so any new decode work is blocked on T31 or on an Ed-II-with-declared-edition path.

---

## 2 · (a) THE MAP — WHAT WE ALREADY HOLD

### 2.1 The state vocabulary

| Artifact | Path | Commit | Records | Grade | Coverage |
|---|---|---|---|---|---|
| **The 40-state ControllerMonster table** | `agentic_orchestration/research/knowledge/gd/2026-07-25-gd-ai-state-tables-complete.md` | `0155118e6` | all 40 state names with **decimal byte offsets** into `Game.dll` 5418372–5418812, boundary evidence both ends, plus the RTTI class set (42 classes) and the 19-entry `Action State:` table | **DATAMINED** (strings + xxd, binary sha-pinned) | **40/40 states enumerated.** The single most complete AI-state artifact we own |
| **The 36-name registered-state scan** | `agentic_orchestration/legolas/notes/2026-08-24-kc2-mc-lap-d9-summon-bodies-and-pet-routing/d9_pet_control_routing.csv:47` | `6cb823ff4` | 36 state names, string-literal exact, from a push-literal scan over `RegisterStates@ControllerMonster` `0x000f87c0` | **MEASURED** (bounded disassembly) | 36 persistent states; independent of the string-table read |
| **Matt's live overlay observation** | `agentic_orchestration/gandalf/notes/2026-07-25-gd-observed-ai-states.md` | — | first-hand: TWO green labels (top-left = controller decision, bottom-right = `Action State:` action layer); the invisible-player peaceful set collapses to `Idle`/`Walk`/`Roam` | **MEASURED** (primary observation, live oracle) | the only behavioural attestation of the state machine running |
| **The anger overlay** | `agentic_orchestration/gandalf/fixtures/2026-07-25-gd-anger-overlay/` (README + 4 PNGs) | — | `character.ShowAngerLevels true` draws a **directed graph edge**, not a scalar — mob→anger-target, appearing at commitment, correctly pointing at *other mobs* during infighting. Apparent dashes are terrain occlusion of a depth-tested 3D line | **MEASURED** | 4 screenshots; establishes anger as a live retargetable relation |
| **Attestation / scope census** | `agentic_orchestration/elrond/notes/2026-07-25-gd-attestation-scope-census.md` | `95b4bc4a1` | 40 states two-sided-classified → **IN 11 (both) · IN 22 (M only) · OUT 5 · NEEDS-JOIN 2 = 33-state proposed roster**; 84 behavioural controller params → 62 IN / 22 OUT | **DATAMINED** | 4,066 monster records; controller join **3,207/3,207** |
| **Sim coverage audit against all 40** | `agentic_orchestration/gamora/notes/2026-07-25-gd-40-state-coverage-audit.md` | `4c751ac0b` | every one of the 40 states classified against the spatial engine with file:line or absence evidence; 9 families + 2 loose | **attested** (code audit + executed probes) | **MODELLED 4 · PARTIAL 9 · ABSENT 21 · PROPOSED-OUT 6** |

### 2.2 The parameter surface

| Artifact | Path | Commit | What it records | Grade | Coverage |
|---|---|---|---|---|---|
| **D-3 — the 12 controller field groups** | `agentic_orchestration/legolas/notes/2026-08-24-kc2-mc-lap-d3-controller-groups/` (README 50 KB + `d3_roster_controller_params.csv`) | `ac2e58855` | per-(controller × field) with Crucible value, base-game value, owner archive and the `this+disp` memory slot; full `ControllerMonster::Load` disassembly (1,122 instructions) | **DATAMINED [bin]+[rec]** | **4,081 rows · 77 controllers × 53 fields · 169 rostered monster records** |
| ↳ pinned engine copy | `reincarnated-engine/data/kc2/d3_roster_controller_params.csv` | — | identical 4,081 rows | same | same |
| **D-12 — the anger economy** | `agentic_orchestration/legolas/notes/2026-08-25-kc2-mc-lap-d12-diversion-decode/` (`findings.md` + `d12_roster_anger_parameters.csv`) | `96e90a378` | `AngerTolerance` · `AttackedAnger` (15.0 on 77/77) · `AllyAttackedAnger` · `petAngerTransference` (modal 0.17, a **split** of one grant, not a transfer) · `ignorePets*` · `RandomAnger*` — each with its memory slot | **DATAMINED** | **77 controllers**; + `d12_summon_threat_eligibility.csv` 2,009 rows |
| **WR3-W2 — aggro / social / leash referent** | `agentic_orchestration/legolas/research/2026-07-31-wr3-w2-aggro-leash-referent.md` (444 ln) | `0a6d6d91f` | ⚑ **the first-of-kind extraction.** Senses + AngerManagement + Pursuit + DistressCalls, template-default vs shipped-value, binned by `monsterClassification` | **DATAMINED [extracted]**, grades carried per row | 3,735 Monster · 447 controller · 356 `ControllerMonster` records |
| **Threat grammar — the animation seam** | `agentic_orchestration/legolas/notes/2026-08-08-kc2-threat-grammar-arz-boundary/` (`tg_monster_timing.csv`, `tg_attack_slots.csv`) | `0fa0eb94b` | ⚑ **wind-up / recovery / root-lock / active-window per monster**, event-derived from the `.anm` clips; plus `num_attack_slots`, `waiting_anim_delay_ms`, projectile velocity | **MEASURED** (animation events) | **968 monsters × 53 cols · 3,064 attack slots × 51 cols** |
| **D-1 — the alert gate** | `agentic_orchestration/legolas/notes/2026-08-24-kc2-mc-lap-d1-alert-decode/` (README + 25 evidence files) | `eb78cd0e6` | the **six-limb conjunction** in `DefaultEnemyFoundResponse` `0x10a360`, limb by limb with offsets; duration = `(frames−1)/(frameRate × speed)` off the shipped `.anm` header | **DATAMINED [bin]** | both halves DECODED; per-record alert incidence over 91 records / 188 actors |
| **D-2 — special-slot reuse gates** | `agentic_orchestration/legolas/notes/2026-08-24-kc2-mc-lap-d2-specials-reuse-gates/` | `55619755f` | `specialAttack{N}Chance/Delay/Timeout/Range` per slot — the gates that decide when a monster casts | **DATAMINED** | **65/65 slots, zero residue** |
| **RESID-D1-2 — the action-permission matrix** | `agentic_orchestration/legolas/notes/2026-08-25-kc2-mc-lap-resid-d1-2/` (66 evidence files, 17 scripts) | `2c4b70f76` | the shipped **26×26 `CharacterActionPermission` matrix**, byte-exactly reconstructed (676/676 cells); movement gated on `ActionState ∈ {5,6,19,20,21}` | **DATAMINED [bin]** | the mechanism by which an alerted body actually stands still |
| ↳ pinned engine copy | `reincarnated-engine/data/kc2/resid_d1_2_action_permission_matrix.json` + `..._action_type_enum.json` | — | the matrix + 23 action types | same | — |
| **The encounter-AI module of record** | `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/wr3_encounter_ai.py` | — | proximity aggro + distress call + pursuit envelope, every constant from shipped records, never from `controllerai.tpl` (TQ heritage, wrong ~10× on the anger economy) | referent-bound code | 3 declared non-builds: no leash, no heal-on-return, no anger gate |
| **Tier-3 encounter grammar** | `agentic_orchestration/gandalf/notes/2026-07-22-tier3-w1-encounter-grammar-spec.md` + `legolas/harvests/2026-07-22-tier3-era-family-mob-harvest/` | — | MACRO/MESO/MICRO grammar; pack formation in space; per-family pressure verb | **attested / authored** | 80 GENRE-ATTESTED + 5 RDR-NATIVE-DERIVED templates |

### 2.3 The live-oracle lane (L0–L5)

The ladder is defined verbatim at `agentic_orchestration/skill_handoff_2026-07-25.md` § 2.3. Its governing property: **the constraint set IS the gap register** — each mechanism implemented retires one constraint and unlocks one rung.

| Rung | Fixture | Measures | Blocked on |
|---|---|---|---|
| **L0** | one melee monster, pre-aggroed, no pack, no flee | the conversion key, nearly isolated | **nothing — runnable now** |
| L1 | + a ranged monster | projectile speed, range bands, kiting geometry | ranged-attack modelling |
| **L2** | + engagement from idle | ⚑ **aggro onset radius, telegraph duration** | KPI 1 · KPI 2 |
| **L3** | + a pack of three | ⚑ **distress propagation, pack leadership, attack-token spacing** | KPI 5 · `WaitToAttack` |
| **L4** | + a flee-capable monster | disengage, leash, return | KPI 3 · fear states |
| L5 | full room, played normally | everything, and play feel | all of the above |

Raw evidence banked: `research/knowledge/gd/live-probe-{1,2,3}/` (console notes, PlayStats panels, 3 paired-frame fight trials). Console surface: `…/2026-07-25-gd-console-command-table.md`, `…-custom-game-console-unlock.md`, `…-console-spawn-syntax.md`. Bank: `research/curated/fixtures.db` — 113 trials, 5 sessions, 3 certified measured fixtures, 175,985 panel readings.

⚑ **The AI-state channel of that bank is EMPTY.** `fixtures.db.trial_participant` = **0 rows**. The per-monster AI-state column the L0 schema designed for was never populated. **No live-oracle AI-state transition has ever been banked as data** — the state machine has been *seen* (§ 2.1) but never *recorded*.

### 2.4 The canon frame

`canonical/reap-die-rise-engine/era-substrate-architecture-2026-07-25.md` **§ 3, Layer 3**, verbatim:

> | **3 — Monster AI / combat feel** | State machines, aggro, telegraphs, attack budgets, leash | **NO — built ONCE** on the GD-validated substrate; eras are parameter profiles (§5) | The GD three-goal program: census-scoped build (G1), live L0–L5 fixtures (G3) |

§ 5 names the dials by name: *"Profiles turn dials (`ViewDistance`, `numAttackSlots`, `EmoteBeforePursuingChance`, leash radii, telegraph beats, pack size/composition…); they **never fork the state machine**."* § 4's fidelity LAW reserves **MEASURED** for the GD lane alone, because it is the only lane with a live oracle.

⚑ **Two of the four dials that sentence names have since been falsified or re-ruled** — `EmoteBeforePursuingChance` is a dead record field (§ 5.1), `numAttackSlots` is surround capacity not a skill count (§ 5.3). Canon has not been updated.

### 2.5 The DB lane — a named negative

`research/curated/corpus.db`: `gd_monster_record` **4,066 rows**, `gd_monster_field` **202,120 rows**, 349 distinct controllers.

⚑ **No controller AI parameter is in any database.** `gd_monster_record.controller_record` is a **pointer only**; `gd_monster_field` carries zero `ViewDistance` / `AngerTolerance` / `MaxPursuitDistance` / `DistressResponse*` / `numAttackSlots` rows. The ~84-parameter surface exists **only as markdown tables and loose CSVs**. Combined with § 1 (vendor trees gone), this is the most fragile thing in the inventory.

---

## 3 · ⚑ THE KEYSPACE IS CLOSED, AND THE PACK'S "43" IS WRONG

The model pack ships `ai_states.json` with `key_space.n_states_enumerated: 43`, `coverage_view: {n_total: 43, n_decoded_in_pack: 5, n_declared_absent: 38}`, `transitions: []`, and absences `ABS-AI-STATE-KEYSPACE` / `ABS-AI-STATE-TRANSITIONS`. The charter, the architect pass, elrond's curation note and the gamora census all repeat "43", and elrond recorded (`A-B2-1`) that *"no enumeration of all 43 exists in `data/kc2`"*.

**Three checks, run this session:**

1. **The five published ids are Table-3 1-based indices, exactly.** idx 8 → `Flee` · 12 → `Return` · 13 → `FollowLeader` · 16 → `DefendLeader` · 30 → `Patrol`. **5/5 match.** The pack's id space *is* the 40-entry string table.
2. **36 + 4 = 40, with no residue.** The MEASURED 36-name registered-state list (§ 2.1) is a strict subset of the 40; the four in the table and not registered are **`UseSkillOnPoint`, `UseSkillOnAlly`, `Emote`, `AlertBeforePursue`** — which is precisely the set D-1 proved are pushed via `AddTemporaryState`, not `RegisterStates`. Two independent instruments, one number.
3. **No artifact anywhere enumerates 43.** The RTTI count is 42 (40 + `ReturnFast` + `Hidden`, with `Sleep`/`Sleeping` a naming variance). 43 appears only as an asserted cardinality with provenance `PRV-BATON-V1`.

> **Finding.** `ABS-AI-STATE-KEYSPACE` is **closeable today from files we have held since 2026-07-25**, at n = **40**, with byte offsets and an independent MEASURED cross-check. The "43" is an unbacked cardinality that has propagated into the pack, the charter's out-of-scope clause, three divergence-register versions and canon. It should be corrected forward, not silently.
>
> ⚑ And note what the correction does *not* buy: `ABS-AI-STATE-TRANSITIONS` stays open. We hold **transitions for exactly one state** — `AlertBeforePursue` (D-1's six-limb entry gate, RESID-D1-2's exit). The other 39 states' edges are undecoded. **The key space was the cheap half.**

---

## 4 · (b) WHAT THE ORACLE AND THE PORT ACTUALLY RUN

### 4.1 The state machines, side by side

**The Python oracle** does not run a state machine and says so. `kc2/engagement.py:115-131` declares its own vocabulary and its own mapping:

- `SIM_STATES` = **7**: `PRESPAWN · PATROL_TO_NODE · PURSUE · HALT_AT_ENGAGE · PARK_AT_NODE · BLOCKED · DEAD`
- `STATE_MAP` maps **7 GD states in** (`Attack`/`WaitToAttack` → `HALT_AT_ENGAGE`, `Pursue` → `PURSUE`, `Patrol`/`Move` → `PATROL_TO_NODE`, `Return`/`Idle` → `PARK_AT_NODE`) and marks **17 GD states `None` = UNREACHED**: `Roam · Wander · DodgeAttack · JumpAttack · RepositionForAttack · FollowLeader · DefendLeader · Trapped · Confused · GettingUp · Immobile · KnockedDown · Panic · Paralyze · Sleep · Stunned · TakeHit`.
- `reengagement.MECH_STATE_CODES` adds 13 locomotion codes; `ALERT_STATE_CODES` adds code 19, `HALTED_ALERT_BEFORE_PURSUE`, **unreachable unless an AlertFold arms a hold (`alert_fold=None` ⇒ never set)**.
- `actor_state.py` states the position outright: *"This sim has five state machines and no state."*

**The Godot port** (`kc2_runtime/sim/kc2rt_fight.gd`, vendored byte-identically into `kc2_play/vendor/`) has **no monster state enum at all**. Monsters are flat dicts (`alive`, `can_swing`, `phi`, `pos`, `enter_tick`, `slot_cooldowns`). The entire behaviour is `_pursue()` (41 lines, `:1387-1427`) + `_resolve_threat()` (51 lines, `:1535-1585`). Its own census declares this: `loader/kc2rt_census_map.gd:191` row M21 `OUT-OF-SCOPE` — *"ai_states.json publishes 5 of 43 states and ZERO transitions; the sim has no state machine at all."*

### 4.2 ⚑ THE SHAPE OF THE GAP — the four missing field groups

`controllerai.tpl` (12) + `controllermonster.tpl` (56) = **68 fields**. D-3 decoded **53** (50 of the 68 + 3 hidden `Leader` fields). The model pack's `controllers.json` carries **exactly those same 53** — verified this session by set-diff: `IN D3 NOT IN PACK: []`, `IN PACK NOT IN D3: []`.

The 15 fields in neither are **Senses · AngerManagement · Pursuit · DistressCalls** — and elrond flagged this at `A-B2-2` ("*a consumer reading this file as 'the controller surface' is short 22 %*"). Pack v3.2 later restored three of them into `monster_kinematics.json` as the V3 rowset (`ViewDistance` 80.0, `MaxPursuitDistance` 125.0, `PursuitTime` 10,000 ms). **Twelve remain absent from the pack entirely**, including every anger field, every distress field, and `InnerViewDistance`.

> **This is not a random 22 %.** Fleeing, Dodging, Roaming, Emote, Loot, Dying, PetBehaviour — the groups that ARE in the pack — are the ones D-3 proved provably inert for this fight. The groups that are MISSING are detection, threat ranking, leash and pack recruitment: **the four mechanisms that make an enemy look like it is thinking.**

### 4.3 The behaviour ledger

| Behaviour | Recorded in our files | Oracle | Godot port | Evidence |
|---|---|---|---|---|
| Sight acquisition | ✅ `ViewDistance` 80.0 (Crucible) / 15.0 (base), `InnerViewDistance` 4.0, `MaxYViewDistance` 10.0 | ✅ 80 m gate | ✅ `kc2rt_fight.gd:110,1405` | unlatched, centre-to-centre, no memory, no inner band |
| Pursuit | ✅ | ✅ | ✅ `:1387-1427` | straight line, re-pathed every tick, zero latency, no steering |
| Engage / halt radius | ✅ `meleeTargetDistance` 2.4 m | ✅ | ✅ `:144,1415-1420` | one scalar board-wide, no hysteresis |
| Swing clock | ✅ per-record `basic_swing_period_s` | ✅ | ✅ `:1559-1570` | deterministic modular arithmetic |
| **Swing-pause jitter** | ✅ `min/maxSwingPause`, re-rolled every swing in `StateAttack::OnUpdate`, **308 pack rows** | ❌ declared out-of-model | ❌ | `locomotion.py:515-524`; gamora M12 — *"a builder who implements SwingPause has implemented a cadence the oracle does not run"* |
| **Wind-up / telegraph / root-lock** | ✅ **MEASURED per monster**, 963/968 records: wind-up min/med/max **0.267 / 0.500 / 1.133 s**; root-lock **0.367 / 1.200 / 2.333 s** | ❌ `ENGAGE_WINDUP` is a declared sensitivity only | ❌ asserted absence; `is_telegraph` read by nothing | `tg_monster_timing.csv`; `threat.py:1207-1210`; census M16 |
| **AlertBeforePursue** | ✅ **fully decoded both halves** — six-limb gate + duration + the standstill mechanism | ⚠️ implemented but **off** (`alert_fold=None`) | ❌ ⚑ census M8 says IMPLEMENTED; **the code contains one comment and no mechanism** | `alert.py` 1,127 ln; `census_map.gd:112-115` vs `grep alert kc2_runtime/` |
| **Leash / Return home** | ✅ `MaxPursuitDistance` 125 m (Crucible) / 75 m / 210 m boss, `PursuitTime` 10 s, `StateReturn` | ✅ carried (`locomotion.py:106,459,1437`) | ❌ **zero carriers** | only spatial bound in the port is the arena wall |
| **Patrol / roam / wander / idle** | ✅ full parameter set + 173 decoded patrol points | ⚠️ `PATROL_TO_NODE` exists, decoded away (every body sees the player at spawn) | ❌ ⚑ a comment says bodies *"revert to patrol"*; **there is no patrol** | `patrol.py` 358 ln; `kc2rt_fight.gd:1376` |
| **Attack-slot concurrency** | ✅ `num_attack_slots` **in the pinned CSV**: 4×91, 8×76, 12×2 over 169 records (968-row lap: 8×508, 4×459) — **re-ruled 2026-09-21 as melee SURROUND CAPACITY** | ❌ | ❌ ⚑ `SLOT_ORDER` is one monster's *skill* slots, not a board budget | `pm2_tg2_monster_timing.csv`; KP-53/KP-55 |
| **Anger / threat ranking / target switching** | ✅ the whole economy + `GetCurrentTargetNotMostHated` | ❌ one target, the player | ❌ structurally impossible | gamora M20; `target_selection.json` PROHIBITION |
| **Distress calls / alert propagation** | ✅ range 18 m, delay 500–2000 ms, cap 1–2, responder 20–75 %, `RespondToSameGroup` 85 % | ❌ out-of-model (`locomotion.py:530`) | ❌ zero hits for `distress` | WR3-W2 § 2 |
| **Reposition / dodge / kite / retreat / flank** | ✅ `RepositionChance`, `DodgeChance`, `DodgeDelay` decoded | ❌ all `None` | ❌ motion is monotone-approach only | `engagement.py:128-129` |
| **Ranged behaviour** | ✅ range bands, projectile velocity, `distance_profile` | ⚠️ fires at range | ⚠️ **fires at range, but a 40 m nova-caster still walks to 2.4 m** | `kc2rt_fight.gd:1590-1634` |
| **Monster support (heal / buff / debuff-on-sight)** | ✅ `DebuffEnemyBehavior = WhenEnemyIsSeen` on **169/169**; ally-heal thresholds **70–80 %** | ❌ | ❌ `_apply_slot` handles damage rows only | D-3 § 3.4 |
| **Hard CC consumption** | ✅ decoded | ⚠️ delivered, **explicitly not actuated** | ❌ | `control_states.py`; gamora F8 `BLOCKED-CONSUMER` |
| **Facing** | ✅ rotation speeds decoded | ❌ heading 0.0 on 100 % of samples | ❌ facing-free tokens | census K25 |
| Pack hierarchy (`FollowLeader`/`DefendLeader`) | ✅ **decoded-unreachable with reason** — hidden `Leader` group `__ABSENT__` on 359/359 records | n/a | n/a | D-3 `F-D3-2` — the one honest "absent" in the set |

### 4.4 ⚑ THE SHORTLIST FOR "SMARTER BY A LONG SHOT"

Ranked by how legible the behaviour is to a player, with the file that already holds the parameters:

1. **Wind-up / telegraph / root-lock.** A GD monster visibly *commits* — a 0.27–1.13 s wind-up, then a 0.37–2.33 s root-lock during which it cannot move. The port's bodies hit on the tick with a 0-frame anticipation. This is the single biggest legibility difference and it is **already MEASURED for 963 monsters**. ⚑ It was measured in the 2026-08-08 lap and **dropped at the tg→tg2 cut** — `pm2_tg2_monster_timing.csv` has zero wind-up columns.
2. **Attack-slot surround capacity (4 / 8 / 12).** GD caps how many bodies may engage at once; surplus bodies sit in `WaitToAttack` and rotate in. That reads as *tactics*. The port lets every body in reach swing every clock. The value is in the pinned CSV and read by nobody. *(Our own L13 envelope note put it exactly: pressure in GD is pack-shaped, not hit-shaped.)*
3. **AlertBeforePursue.** A body notices you, plays a 1.33–2.43 s alert animation while **standing still**, then charges. ~8 % of arrivals (14.9 of 188 expected) — a sparse garnish, but it is the beat that makes an enemy look like it *saw* you. Fully decoded; off in the oracle; absent in the port; **the port's census wrongly claims it implemented**.
4. **Distress calls / staggered pack recruitment.** Four independent stagger parameters — call delay, call cap, responder probability, pre-pursuit telegraph. Our own file warns: *"If the lap models stagger as an emergent by-product of radii, it will under-produce it."* The port has no stagger at all; every body from a spawn point shares one `enter_tick`, and the census says the stagger is *"unrepresentable"* by construction.
5. **Anger as retargetable threat ranking.** `GetCurrentTargetNotMostHated` — GD's AI deliberately sometimes picks *not* the most-hated. Matt has literally watched the red edges swing between targets during infighting. The port has one target and cannot switch.
6. **Reposition / dodge / range-keeping.** `RepositionForAttack` and `DodgeAttack` (projectile-reactive, live on 42/169) are both decoded and both absent. A ranged body that walks into melee looks stupid in a way nothing else on this list does.
7. **Leash / return.** Lowest player-visible value in a closed arena, but it is the reason the port has "stragglers" to hunt down — which Matt reported in the same breath.

⚑ **Every one of these seven is a RECORDED-BUT-UNIMPLEMENTED gap, not an unknown.** None requires new external research to specify. That is the answer to Matt's instruction: the files are there.

### 4.5 One defect found in passing, worth routing

`kc2_runtime/loader/kc2rt_census_map.gd:112-115` grades row **M8 (AlertBeforePursue)** as `D_IMPL` — IMPLEMENTED — citing `V0-19 alert_fold.limb = AlertLimb.ARM_HOLD`, and the row itself notes a "TENSION" with the v3.1 census reading `alert_fold=None`. Verified this session: the only occurrence of "alert" in the runtime's executable code is a **comment** at `kc2rt_fight.gd:1406`. There is no hold clock, no `alert_hold_until_t_s`, no rotate-towards. **The census claims a behaviour the code does not contain.** The port's coverage artifact is the thing a Godot builder and a Gate-2 reviewer both read first, so this is a live mis-statement, not a paperwork nit. Routed to the conductor; not adjudicated here.

---

## 5 · CONTRADICTIONS INSIDE OUR OWN FILES (print both, average neither)

**5.1 `EmoteBeforePursuingChance` — an entry gate that does not exist.** elrond's 2026-07-25 census records it as the **HEADLINE FIND**: *"93.0% attestation, mode 20, is the entry gate for AlertBeforePursue — the binding the binary-inspection research doc listed as 'cannot determine'."* WR3-W2 carries it as a stagger source. D-3 `F-D3-3` (2026-08-24) then proved it is a **DEAD RECORD FIELD**: the literal string does not exist in `Game.dll`, `Engine.dll`, `Grim Dawn.exe`, `Editor.exe` or `DBREditor.exe` — **0 hits, all five**. Crate authors it; the engine never reads it. D-1 then decoded the real gate (a six-limb conjunction on `alertAnimChance`). ✅ **Corrected forward by the decode laps — but the 2026-07-25 census still reads as current, and canon § 5 still lists it as an era dial.**

**5.2 The state count: 40 vs 43.** See § 3. Unreconciled anywhere until this note.

**5.3 `numAttackSlots` semantics.** Re-ruled 2026-09-21 (KP-53/KP-55) from "skill count" to **melee surround capacity**, with a disproof needing no depot: **13 of 169 records decode more slots than the field declares.** Canon's era-dial list predates the re-ruling. ⚑ Note the re-ruling *strengthens* item 2 of § 4.4 — surround capacity is exactly the concurrency cap.

**5.4 Alert incidence: "universal" vs "~8 %".** Lap AA read the distance limb as satisfied for essentially every body and concluded bodies are *"pushed into an animation state before it marches"*. D-1 added limbs 2 and 3 and removed ~92 % of the roster. ✅ Corrected in place by D-1 § 2.5.

**5.5 Base game vs Crucible.** WR3-W2's table is base-game Edition II (`ViewDistance` 15 m, `MaxPursuitDistance` 75/210 m). D-3 `F-D3-1` established that **77/77 Crucible controllers are SurvivalMode-owned and every one of the 68 fields moves on at least one controller** (`ViewDistance` 15→80 on 77/77; boss `MaxPursuitDistance` 210→**125**, i.e. the Crucible *shortened* the boss leash). Both are true in their own scope. ⚑ **Any AI work must state which scope it is in** — this is the DR-3 precedence case, and the pack's own note records that it is not reproducible from this fight because the value is unanimous at tier 16.

---

## 6 · (c) WHAT IS *NOT* IN OUR FILES — THE EXTERNAL RESEARCH STILL OWED

Everything in § 2 is ours already. The genuinely-absent set is small and sharply shaped.

### 6.1 Owed from the BINARY (not external — but blocked on § 1)

| # | Surface | Why it is not in our files | Cheapest instrument |
|---|---|---|---|
| **X-1** | ⚑ **Transition edges for 39 of 40 states.** We hold entry+exit for `AlertBeforePursue` alone. `ABS-AI-STATE-TRANSITIONS` is genuinely open. | Never commissioned — the laps were scoped on *field groups*, not on the graph | Disassemble `OnBegin`/`OnUpdate`/`HandleEvent`/`EnemyFound` for each `ControllerMonsterState*` class (all offsets already in the 2026-07-25 doc). **Bounded: 40 classes × 4 methods.** Needs a `Game.dll` — **blocked on T31** |
| **X-2** | The `WaitToAttack` / attack-slot arbitration rule. We hold the *capacity* per record; we do not hold *who gets a slot, in what order, and what a waiting body does* | Capacity was extracted; the arbiter was never decoded | `Game.dll` — the `ControllerMonsterStateWaitToAttack` class + whatever holds the slot table |
| **X-3** | `RepositionForAttack` entry/exit conditions and target-point choice | RTTI confirmed, 20-method surface listed, never disassembled | same |
| **X-4** | `ReturnFast` vs `Return`, and `Hidden` — the two RTTI classes with no string-table entry | Flagged as unresolved in the 2026-07-25 doc § "Cannot determine" | same |

### 6.2 Owed from the LIVE ORACLE (Matt's hands — cannot be agent-fetched)

| # | Rung | What it would settle | Status |
|---|---|---|---|
| **X-5** | **L2** | aggro onset radius **as behaviour**, and telegraph duration as *seen* | **runnable now** — the rig, console surface and overlay instrument all exist and are banked |
| **X-6** | **L3** | distress propagation, pack leadership, attack-token spacing — items 2 and 4 of the § 4.4 shortlist, which are the two the binary can specify but only play can *validate* | rig exists; needs a sitting |
| **X-7** | — | ⚑ **AI-state transitions banked as DATA.** `fixtures.db.trial_participant` is empty. The overlay is a **self-validating instrument** (red anger edge and the `Pursue` label should coincide frame-for-frame) and that check has never been run | schema exists, table empty |

⚑ **X-7 is the highest-value cheap item on this page.** We have an instrument that reads the state machine off the screen, a schema with a slot for it, and zero rows in it. One sitting with LogData on converts the whole of § 2.1 from "we know the names" to "we have watched the graph run."

### 6.3 Genuinely EXTERNAL (web / genre) — and it is a short list

| # | Question | Why it cannot come from our files |
|---|---|---|
| **X-8** | How do peer ARPGs shape the *legibility* of enemy intent — telegraph lead times, wind-up conventions, surround caps, stagger? | We hold GD's values; we do not hold the genre's **norms**, and "smarter" is partly a perception question. Our one prior pass (`legolas/notes/2026-07-22-game-combat-ai-landscape-modeA.md`, 384 ln) covered *architectures* (utility AI, BT, the System-1/System-2 split) and found **no ARPG has shipped learned or LLM-runtime mob AI** — but it did not measure telegraph or concurrency conventions. ⚑ **Its D4 Season-11 row is the nearest hit and it is squarely on point:** ranged enemies maintaining distance, large units prioritising disruption, swarmers actively surrounding, wider pack spread, **improved telegraph clarity on high-disruption attacks** — shipped explicitly as a *"smarter monsters"* update. That is items 1, 2, 4 and 6 of our shortlist, confirmed as the industry's own answer to the same complaint |
| **X-9** | Is there public documentation of GD's AI beyond the binary — Crate dev posts, modding-community controller docs? | Never surveyed. WR3-W2 used web as **tertiary corroboration only** and did not sweep it. Likely low yield, but cheap, and it is the only lane unaffected by the vendor-tree loss |

**Not owed:** the state vocabulary (§ 3), the controller parameter surface (§ 2.2), the alert mechanism, the anger economy, the distress system, the wind-up timings. **We have all of it.** The deficit is implementation and, for the graph edges, one more binary lap — not discovery.

---

## 7 · WHAT I DID NOT DO

- **No adjudication.** § 5's contradictions are printed, not resolved; § 4.5's census defect is routed, not fixed.
- **No design recommendation.** § 4.4 ranks by *player legibility grounded in cited parameters*; whether any of it should be built is gandalf's and Matt's.
- **No new decode.** Vendor trees are gone (§ 1); nothing here required them.
- **No re-derivation of DATAMINED rows.** Every count is quoted from its artifact with a path, or computed this session from a file on disk (the set-diffs in § 3 and § 4.2 and the distributions in § 4.3 are mine, this session, and reproducible from the named CSVs without a vendor tree).

---

## 8 · EMPIRICAL CRITERIA GATING THE NEXT STEP

Not time-passage — evidence:

- **External research (Step 2) is gated on** a conductor ruling over § 6.3. On this inventory the external surface is **two questions (X-8, X-9)**, and X-8 is largely answered by an existing own-file note. ⚑ **The honest report is that Matt's instinct was right and the commission's external half is nearly empty.**
- **X-1 (transition edges) is gated on** `matt_to_do` **T31** — an Ed-III `Game.dll` on disk.
- **X-5/X-6/X-7 (live oracle) are gated on** a Matt sitting. The rig is banked and runnable; nothing agent-side blocks them.
- **§ 3's keyspace correction is gated on** a conductor decision to amend forward (pack `ai_states.json`, the charter's out-of-scope clause, the divergence register, canon § 5's dial list).

---

**Signed:** legolas (`UNKNOWN-RESEARCHER`). Step 1 of the KP-110 enemy-AI commission: the own-files inventory. The map is § 2, the gap is § 4, the residue is § 6. The one-line answer to Matt: **we recorded GD's enemy AI in depth, and then built a fight engine that deliberately runs arithmetic instead of behaviour — the "smarter" he saw is sitting in our own files, unimplemented.**
