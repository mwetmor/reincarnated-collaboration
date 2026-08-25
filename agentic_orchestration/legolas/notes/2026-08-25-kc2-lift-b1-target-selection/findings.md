# KC2 LIFT RUN · Wave-1 · **B1 — `ABS-TARGET-SELECTION`** — decode lap

> **CONDUCTOR CAPTURE NOTE (gandalf RUN-CONDUCTOR, 2026-08-25):** the harness blocks seat-authored `findings.md` writes (same constraint as lap `md-b4app-2d`); the seat returned the complete findings text in its lap result and the conductor captured it here VERBATIM. Authorship is the legolas seat's; the capture is mechanical. Seat commit: `5448e701` (7 predecessor artifacts, verified `git show --stat HEAD`, not pushed — conductor releases). Fold: LIFT ledger L-6.

**Seat:** legolas (UNKNOWN-RESEARCHER) · **Commissioner:** gandalf `RUN-CONDUCTOR`
**Charter:** `agentic_orchestration/gandalf/notes/2026-08-25-kc2-lift-run-charter.md` § 2.2 · ledger L-1
**Date:** 2026-08-25 · **Lap dir:** `agentic_orchestration/legolas/notes/2026-08-25-kc2-lift-b1-target-selection/`
**Substrate posture:** READ-ONLY throughout. K-7 honoured — sealed cell re-hashed PRE and POST, `ad61ad2a…dc5c` unchanged.

## § 0 — VERDICT IN ONE PLACE

| Half of the split | Verdict | Basis |
|---|---|---|
| **(a) MECHANISM** — targeting/acquisition rules the game files determine | **DECODED**, first-of-kind. Engine-level selection-bias family (8 values) + developer-authored semantics + per-skill acquisition for all four bound skills + the `targetingMode` enum. | § 2 |
| **(a′) MECHANISM residue** — the *function* combining the eight bias terms | **UNDECODABLE-FROM-SUBSTRATE.** Parameters are data; the composition is compiled engine code. | § 2.6 |
| **(b) POLICY** — which body the pilot chose | **UNDECODABLE-FROM-SUBSTRATE**, and the substrate says *why* rather than merely staying silent: the game expresses target-selection policy declaratively **for every AI-driven actor and for no player**. | § 3 |
| **160-residual candidacy** | **SURVIVES, materially reshaped.** Evidence in § 5; conductor adjudicates. | § 5 |

**The lap's most consequential finding is not in the game files at all — it is in the sim.** The graded cell's live player-movement law (`kinematics.MillWalk`, K-MILL) is **board-blind by construction**: it accepts the live-body list and executes `del live`. The sim that produced the 153.2 terminal mean **has no target selection of any kind**, and its own justification chain-cites a prior-lap test which that lap explicitly declares uninformative about targeting (§ 4.2).

## § 1 — PREDECESSOR DISPOSITION (kept vs re-derived)

Every load-bearing claim was re-derived; none inherited on trust.

| Artifact | Disposition |
|---|---|
| `pins.json` · `pins.txt` (17 pins) | **RE-DERIVED — 17/17 sha256 match exactly.** Kept. |
| `b1_arz.py` | **KEPT and RE-RUN.** Reuses the banked `ArzArchive` TQIT reader (lane est. 2026-07-23); read-only. |
| `ge3.txt` | **RE-DERIVED.** Independent re-run reproduced every `selectionBias*`, range and rotation constant identically. |
| `skill_targeting_table.txt` | **RE-DERIVED for 3 of 4** (Blitz, EoR, War Cry) — exact match incl. War Cry's rank-array idx 11 → 16.0. ⚑ **Correction: Vire's Might is `records/skills/playerclass09/viremight1.dbr`, not `viresmight1.dbr`.** Values right; the path as written resolves to nothing. |
| `fieldcensus3.txt` | **KEPT as lead index** (165 field names) — it is what pointed at `gameengine.dbr`; findings re-derived at source. |
| `barskills3.txt` | **KEPT.** Corroborating bulk; contains no `selectionBias` rows (grep count 0). |

Predecessor's work was sound. The one path defect is the kind a re-derivation catches and a copy-forward does not.

## § 2 — (a) MECHANISM — DECODED

### 2.1 Engine target-acquisition constants
`records/game/gameengine.dbr` [base], 367 fields. Edition I ↔ III drift: **ZERO on every constant below.**

| Field | Value | Tpl default | Tpl description |
|---|---:|---|---|
| `meleeRange` | 1.25 | 0.4 | — |
| `meleeTargetDistance` | **2.4** | 2.5 | `"TQ was 2.5"` |
| `meleeAutoTargetDistance` | **4.0** | 3.0 | `"TQ was 3.0"` |
| `shortRange`/`moderateRange`/`longRange`/`maximumRange`/`bossRange` | 4.75 / 9 / 15 / 18 / 32 | 2/4/8/12/20 | — |
| `minPlayerRotationSpeed` / `maxPlayerRotationSpeed` | **19.0 / 30.0** | 5/10 | — |
| `playerPathSlowdownLength` | 0.0 | 0.3 | — |
| `alertDistance` | 6.0 | 2.0 | `"min distance for alert+rally"` (monster-side) |
| `combatIdleTime` | 1.2 | 3.0 | — |

`meleeTargetDistance = 2.4` **is already the sim's `D_ENGAGE_M`** (`locomotion.py:82` reads it directly) — that linkage is sound and undisturbed. ⚑ `meleeAutoTargetDistance = 4.0` is a **separate, larger ring** the sim carries nowhere; value MEASURED, semantics **INFERRED FROM NAME ONLY** (no template description). Not promoted.

### 2.2 ⚑ The `selectionBias` family — first-of-kind
Eight live values, grouped in `gameengine.tpl` under a Group literally named **`"Targeting"`**. Four carry developer descriptions. **All four say the same word: stickiness.**

| Field | Value | Developer description (verbatim) |
|---|---:|---|
| `selectionBiasLockOnMultiplier` | **1.8** | *(empty)* |
| `selectionBiasLockOnOffset` | **1.9** | *(empty)* |
| `selectionBiasComparisonMultiplier` | 0.2 | `"Increases target stickiness vs. other targets while moving (multiplied by speed)"` |
| `selectionBiasComparisonOffset` | 0.15 | `"Increases target stickiness vs. other targers (additive)"` *(sic)* |
| `selectionBiasBaseMultiplier` | 0.5 | `"Increases target stickiness vs. ground while moving (multiplied by speed)"` |
| `selectionBiasBaseOffset` | 0.5 | `"Increases target stickiness vs. ground (additive)"` |
| `selectionBiasVelocityMultiplier` | 0.5 | *(empty)* |
| `selectionBiasMouseDownOffset` | **1.6** | *(empty)* |

Establishes, at the strength the source supports: (1) GD target selection is a **scored cursor-pick with hysteresis**, competing two-sidedly — target-vs-other-targets and target-vs-bare-ground; (2) every documented multiplier is `"multiplied by speed"` — bias **scales with player movement speed**; (3) `LockOn*` are the largest terms by ~3.6–12.7× over `Comparison*`; (4) `MouseDownOffset` makes bias **conditional on button-held state**, coupling selection directly to the referent's bindings (L = left-mouse Blitz, R = right-mouse EoR channel). Holding right-mouse to channel is a *targeting* state, not only an activation state.

### 2.3 Per-skill acquisition — the four bound skills

| Slot | Skill | Record | Class | `targetingMode` | Acquisition rule |
|---|---|---|---|---|---|
| **L** | Blitz | `playerclass01/blitz1.dbr` [base] | `Skill_AttackWeaponCharge` | ABSENT | **REQUIRES A TARGET OBJECT.** Charge-to-target; on arrival `skillTargetNumber=3` (*"Max number of targets"*), `skillTargetAngle=180.0` (*"Angle for targeting"*). `characterRunSpeedModifier=300`, cd 3.5. |
| **R** | Eye of Reckoning | `playerclass09/eyeofreckoning1.dbr` [gdx2] | `Skill_AttackRadiusSpin` | **`Point`** | **NO TARGET.** Self-centred spin, `skillTargetRadius=3.0` m. No target-count field exists (10 names probed, all MEASURED-ABSENT). No `skillCooldownTime` — the channel signature. |
| **2** | Vire's Might | `playerclass09/viremight1.dbr` [gdx2] | `Skill_AttackPathCharge` | **`Point`** | **NO TARGET** — charges to a *ground point*. Path radius 2.2 m; `endRadiusMultiplier=1.5` (*"Multiplier for final radius attack at destination point"*) → 3.3 m terminal blast. |
| **3** | War Cry | `playerclass01/warcry1.dbr` [base] | `Skill_AttackRadius` | ABSENT | **NO TARGET.** Self-centred, rank-array n=22, **rank 12 → idx 11 → 16.0 m**. cd 7.5. |

⚑ **THREE OF FOUR BOUND SKILLS ACQUIRE NO TARGET OBJECT.** The referent's *primary damage skill* — the EoR channel the whole KC2 model is built around — is `Point`-mode and self-centred. **For it, "target selection" is not a pick problem; it is a positioning problem.** Object-pick binds on exactly one skill: Blitz, left-mouse. This is the most important mechanism result for a Godot implementer.

### 2.4 `targetingMode` enum + corpus census
Declared once, in `templatebase/skill_base.tpl` — the universal base of every skill:
```
name = "targetingMode"  class = "picklist"  type = "string"
defaultValue = "Default;Point;Object;Target"
```
Census over **12,256 `Skill*` records, all 7 Edition-III archives**: ABSENT 10,260 · picklist-string-verbatim (authored-never-set) 905 · `Point` 872 · `Target` 218 · `Default` 1 · ⚑ **`Object` = 0 — the enum member is never used anywhere in the shipped corpus.** Per class: `Skill_AttackWeaponCharge` ABSENT on **all 85** records (charge-to-target skills never declare a mode; it is implied by the class); `Skill_AttackRadiusSpin` `Point` on all 4.

`distanceProfile` likewise a picklist (`Melee;Short;Moderate;Long;Maximum;Boss;`) mapping onto the § 2.1 ladder: Melee 922 · Short 1,027 · Moderate 736 · Long 1,483 · Maximum 761 · Boss 174 · absent 7,127.

### 2.5 Aim/rotation coupling — targeting has a measured time cost
EoR carries `rotationSpeedMultiplier = 0.35` (*"Multiplier applied to player rotation speed while skill is active"*). Against § 2.1's 19/30, channelling re-aims at **[6.65, 10.5]** units/s. `canUseWhileMoving = True` vs template default 0; `characterRunSpeedModifier` MEASURED-ABSENT — **no translation penalty**. ⚑ **Turning is the measured cost of channelling; translation is free.** For a `Point`-mode 360° spin facing does not gate the AoE, so this cost lands on *switching to a directional action* (Blitz's 180° arc, Vire's heading) while the channel is up — the natural companion to `selectionBiasMouseDownOffset`. **Honest limit:** whether the engine *uses* facing to gate Blitz's arc is expressed by no field; `delayMovement` has an **empty** description (`D-P-G3` carried).

### 2.6 ⚑ MECHANISM RESIDUE — UNDECODABLE-FROM-SUBSTRATE
The eight values are data; the function consuming them is not. Unrecoverable from any `.arz`/`.arc`/`.tpl`/save: **the score expression** (additive? multiplicative? screen-distance penalty? what the multipliers multiply beyond speed? units of the offsets); **what `LockOn` state IS** (entry/persistence/break — both descriptions empty, largest terms); **what `VelocityMultiplier` acts on**; **the candidate set** scoring runs over (screen-space vs world-space vs `meleeAutoTargetDistance` cull). These live in the compiled binary. **No binary lane exists and none was opened.** Named, not estimated.

## § 3 — (b) POLICY — UNDECODABLE-FROM-SUBSTRATE (declared)

The declaration is stronger than "we looked and found nothing." GD **does** express target-selection policy as documented data — **for every AI-driven actor**:

| Template | Field | Description (verbatim) |
|---|---|---|
| `controllermonster.tpl` | `petTargetLeastAttacked` | `"try to target the least-recently attacked enemy"` |
| `controllermonster.tpl` | `petTargetGreatestHealth` | `"try to target monsters with greatest health"` |
| `controllermonster.tpl` | `petTargetLevelRange` | `"only target enemies within n levels of player"` |
| `controllermonster.tpl` | `BuffAllyTargeting` | picklist `BuffClosest;BuffStrongest;BuffWeakest` |
| `controllermonster.tpl` | `FleeTarget` | picklist `AwayFromEnemy;TowardsAllies;TowardsHome` |
| `skillautocastcontroller.tpl` | `targetType` / `autoTargetRadius` | `Enemy;Self;Ally;EnemyLocation;` / `"Set to pick ally or enemy"` (def 10.0) |
| `controllerai.tpl` | `ViewDistance`/`InnerViewDistance`/`enemyTooClose`/`AngerTolerance`/`AttackedAnger`/`AllyAttackedAnger`/`ForgiveRate`/`SightAngerRate`/`InnerSightAngerRate`/`ProjectileAnger` | the full threat/aggro acquisition model (B2 territory) |

**And for the player it expresses nothing.** `controllerplayer.tpl`'s entire `"Player Control"` group is **one field — `controllerDeathDelay`, in seconds.** The sole `ControllerPlayer` record in the corpus:
```
records/controllers/player/playercontroller.dbr   [base]   6 fields
    Class = ControllerPlayer          controllerDeathDelay          = 3.0
    controllerFollowAngle = 20.0      ← inherited, ControllerBaseCharacter
    controllerFollowDistance = 1.0    ← inherited
    controllerObstructionDistance = 3.0  ← inherited
    templateName = database/templates/controllerplayer.tpl
```
Six fields, none a targeting policy, three inherited formation constants — against `ControllerMonster`'s 64 fields including explicit target-selection policy.

⚑ **The asymmetry IS the finding.** The player's policy is absent **by design**, because in GD that policy is the human at the mouse. There is no record to decode, and no amount of further `.arz` work will produce one. **Correctly declared UNDECODABLE-FROM-SUBSTRATE — not "not yet found."**

### 3.1 Searched surfaces (complete)
**Game files:** (1) `records/game/gameengine.dbr` full 367-field dump, **both editions**, zero drift; (2) `templates.arc :: gameengine.tpl` `"Targeting"` group, all 8 vars + descriptions; (3) **full-text scan of all 819 `templates.arc` entries** for `targetingMode`/`skillTargetNumber`/`skillTargetAngle`/`skillTargetRadius`/`autoTargetRadius`/`skillTargetInterval` — ⚑ **1 of 819 failed LZ4 decompression and was not read** (named, not silently skipped; not a controller or skill-base template); (4) `templatebase/skill_base.tpl`; (5) `skill_attackweapon.tpl` · `templatebase/skill_radius.tpl` · `skillautocastcontroller.tpl`; (6) **include-chain resolution** for all four bound skill classes, 8–15 templates deep each; (7) **census of 12,256 `Skill*` records** across all 7 archives; (8) the four bound DBRs + Ascension + `defaultweaponattack`, 13 targeting fields each; (9) **all `ControllerPlayer` records (n=1)** + `controllerplayer.tpl`; (10) `controllermonster` · `controllerbasecharacter` · `controllercharacter` · `controllerai` · `controllermegalesios` · `controllerspirit` · `skillautocastcontroller` templates; (11) **overlay-wide field-name census** for `target`/`select`/`slot` (165 names — this surfaced `selectionBias*`).
**Save:** (12) prior lap `md-b4app-2d` — `ui_settings` v7 solved; it is the **hotslot/action-bar block** (47 hotslots), carrying bar bindings and **no targeting configuration**.
**Sim:** (13) `player_locomotion.py` · `kinematics.py` · `run.py` · `engagement.py` · `locomotion.py`.
**Sealed telemetry (READ-ONLY):** (14) the mpol2 checkpoint.
**Prior laps (digests re-derived):** (15) Lap U · Lap R · Lap R episodes CSV.
**NOT searched — named:** `.map`/`.lvl` world assets (Lap R § 5.4 UNREACHED, carried) · the compiled engine binary (no lane; § 2.6's residue lives there) · ⚑ **footage — deliberately not fired; the conductor routes galadriel.**

## § 4 — SIM-SIDE CURRENT HANDLING

### 4.1 ⚑ The graded cell has no target selection at all
Two policies exist; `run.py:1570` makes the second **supersede** the first (*"SUPERSEDED, NOT LAYERED"*):
- `player_locomotion.NearestKillableSeek` (`player_locomotion.py:400`) — greedy nearest-killable, `D-I18-2` tie-break lowest `actor_id`, **zero cross-tick state**; trigger `SEEK_TRIGGER_RADIUS_M = D_ENGAGE_M = 2.4`.
- `kinematics.MillWalk` (`kinematics.py:315`) — tethered random-heading mill, stop/go phases, specular reflection.

The sealed M-POL-2 driver passes `kinematics_factory=(lambda: kn.KinematicsFold(shape=kn.Shape.K_MILL, tether=kn.TetherLimb.PER_WAVE, px_arm_label="PX-LO", seed_salt=salt))`. **So the policy behind 153.2 is `MillWalk`, and `MillWalk.step` opens:**
```python
del live                                   # ⚑ board-blind by decode — see the docstring
```
Its docstring: *"`live` is accepted and **ignored**: the policy is board-blind by decode… the parameter is kept so this object is drop-in for `NearestKillableSeek` and so the* absence *of a target read is visible at the seam rather than hidden behind a different signature."*

⚑ **This is the exact, quantified statement of B1's absence.** `NearestKillableSeek` is **built, tested, and not running in the graded cell** — a residual argument aimed at its greediness would be aimed at code the seal never executed. (I formed that wrong hypothesis mid-lap; it did not survive the trace.)

### 4.2 ⚑ A provenance defect in the board-blind decode
`kinematics.py` § 0 justifies board-blindness on three cited evidences, re-read at source:

| Cited evidence | Holds? |
|---|---|
| Lap U § 1.2 — *"does he close distance toward packs"* = **NO** | ✅ **HOLDS.** Net 1.99–11.27 m/wave (median **3.61**) over 40.2–83.0 m paths; straightness median **0.060**. *"THE PLAYER MILLS."* |
| Lap R § 4.4 — movement-while-channeling **CONTINUES** | ✅ **HOLDS.** Ratio 0.971, Wilson CIs overlap; `canUseWhileMoving=1` vs default 0. |
| Lap U § 1.3 — `V-a1` FOLLOW test **NOT SUPPORTED** (0 of 29/55/72 windows) | ❌ **DOES NOT SUPPORT THE INFERENCE.** |

Lap U § 1.3, in its own words: *"The largest player net displacement inside any surviving window is **4.16 m**. The loosest cell needed 5.0 m. **The discriminator was never reachable on this referent.** `V-a1` returns **no information about targeting**; it is a negative about the instrument's reach. **It does not refute player-targeting**…"* `V-a1` additionally conditions on *monster* displacement (a body held within `R_hold` must itself have moved ≥ |Δp| − 2·R_hold) — it is cited as evidence that the **player** does not read the board.

**Evidence base is two supports, not three.** Board-blindness is not thereby refuted — § 1.2 and § 4.4 stand alone — but they establish something narrower than the code claims. **This is a finding against my own seam's prior work, recorded as such; the conductor adjudicates.**

### 4.3 What § 1.2 does and does not establish
It measures **net displacement and straightness** → establishes *no long-range pack-seeking traversal*. It does **not** establish *heading is independent of the board*: a pilot orbiting/kiting the nearest pack at short range yields the same signature — low net displacement, low straightness, high moving-fraction. **The measurement cannot separate "board-blind mill" from "short-radius target-conditioned mill."** → U-7.

### 4.4 A false-attribution trap, named
`engagement.py` carries an exit cause literally named **`"retargeted"`** with a `RETARGET_BINDING_CLAUSE`. **This is MONSTER-side** — it fires when a monster's pursuit gate (`view`/`leash`/`memory`) closes. It is **not** player target selection and must not be read into B1.

## § 5 — 160-RESIDUAL CANDIDACY — EVIDENCE ONLY

Derived from the seal (read-only, re-hashed unchanged):

| Arm | Terminals | Mean |
|---|---|---:|
| M0 | [155,152,155,151,152] | 153.0000 |
| **M-POL-2** | **[156,152,151,151,156]** | **153.2000** |
| M-POL-2-NULL | [155,152,155,151,152] | 153.0000 |
| M-POL | [151,151,151,151,151] | 151.0000 |

All 20 runs terminate `player_death`. Referent reached **wave 160** (OBS-H2-6: `160@839.0`; OBS-H2-5 terminal collapse from t=856.1). Residual **6.8 waves**.

**FOR candidacy:** (1) the absence is **total, not partial** — not "a different policy" but *no* policy; the gap between board-blind random mill and a human with 1.8/1.9 lock-on stickiness is the largest a targeting difference can be; (2) **the player moves on 85.3% of ticks** (`n_ticks_moved=930`/`n_player_ticks_observed=1090`, sealed M-POL-2 run 0) — position is actively determined every tick by a rule that ignores monsters; (3) **position directly drives damage dealt** — EoR is a 3.0 m self-centred disc, so output is a function of how many bodies sit inside it, which a board-blind walk optimises only by accident; (4) **position directly drives damage taken** — all 20 runs die, and a random-heading mill has no notion of retreating from density; (5) the bias family is **speed-coupled**, and the referent runs **at the engine's hard speed cap** (sheet 135%, `playerRunSpeedCapMax=135.0`) moving 79.5% of the fight — precisely the regime where stickiness is maximal. **The sim reproduces the speed and the duty cycle and none of the bias.**

**AGAINST candidacy — substantial:** (1) ⚑ **three of four bound skills need no target**; the classical pick surface binds on Blitz alone — one 3.5 s-cooldown skill on a build whose damage is a continuous channel. **Most of B1-as-imagined does not exist for this referent.** (2) The referent's own motion is **measured as non-traversing** (median net 3.61 m against 40–83 m path) — a board-blind mill is wrong in *mechanism* but not obviously wrong in *gross positional statistics*, which is exactly why K-MILL was fitted from Lap R's 86 measured episodes. (3) Lap U § 1.2 already published *"Targeting-as-motion cannot carry this residual"* — ⚑ **that ruling is about the march-time residual (t→50%, 6.49 s), NOT the 153.2-vs-160 wave residual. It does not transfer and I decline to transfer it**, but it is prior evidence from this seam that targeting-as-motion is a small term on an adjacent question. (4) K-MILL's parameters are **measurement-derived, not fitted** (`GL-6` HALT armed on every digest).

**Shape, stated honestly:** the charter names B1 *"how the pilot chooses which body to fight next."* **The substrate says that is not the operative question for this build.** The operative question is **"where does the pilot stand, and does that placement read the board"** — and the sim's answer is a measured, unambiguous **no**. The candidate to weigh is **not** "the sim picks the wrong body"; it is **"the sim's pilot positions itself without reference to the board, on a build whose entire damage output is a 3 m disc centred on that position."** Live, plausible, correctly-directed.

**What would settle it:** an A/B against the same sealed prereg with a board-reading positioning limb — a **gamora** build, **NOT proposed here** (naming is not chartering). **What would inform it:** a galadriel lap measuring **short-radius heading conditioning** (does heading correlate with local body density inside ~5 m) — the exact discriminator § 4.3 names as unreachable by the existing instrument; **routing is the conductor's**. **What would NOT settle it:** more `.arz` work — mechanism is decoded to the binary boundary.

## § 6 — UNMEASURABLE / UNDECODABLE REGISTER

| # | Item | Class |
|---|---|---|
| U-1 | The `selectionBias` **scoring function** | UNDECODABLE-FROM-SUBSTRATE (compiled) |
| U-2 | What **`LockOn` state** is — entry/persistence/break | UNDECODABLE (empty descriptions; largest terms) |
| U-3 | What `selectionBiasVelocityMultiplier` acts on | UNDECODABLE (empty description) |
| U-4 | The **candidate set** scoring runs over | UNDECODABLE (no field expresses it) |
| U-5 | **Semantics** of `meleeAutoTargetDistance = 4.0` | INFERRED-FROM-NAME ONLY; not promoted |
| U-6 | **The pilot's policy** | UNDECODABLE — no player-side policy record exists, by design |
| U-7 | Referent's **heading conditioning at short radius** | **UNMEASURABLE by the existing instrument** (§ 4.3); footage-side |
| U-8 | Whether facing **gates** Blitz's 180° arc | UNDECODABLE (`delayMovement` description empty; `D-P-G3`) |
| U-9 | **Ground-px → metres** on the referent | DECLARED GAP, carried (OBS-H2-9) — blocks metric comparison of footage radii against § 2.1 |
| U-10 | Arena dimensions + spawn placement | UNREACHED, carried (`.map`/`.lvl`, Lap R § 5.4) |
| U-11 | 1 of 819 `templates.arc` entries | NOT READ (LZ4 failure); not a controller/skill-base template |

## § 7 — PINS (all sha256 DERIVED this session, DR-1)

**Edition III of record** (`~/Games/vendor/grim-dawn-edition-III-20260808/`): `database/database.arz` `2ad6d379285cfb745462316949e8d59e9450cb58a13f9ffa2fdeb70193183bfd` (58,543,495) · `gdx1/database/GDX1.arz` `431e64e1d372e4ebee5d1048d3aca458923e1df8c97844274636f5373a01e292` (42,427,625) · `gdx2/database/GDX2.arz` `13fa0b93be15835958968ad672b9efa5159d7221a279aca791590390dd81a072` (33,117,410) · `gdx3/database/GDX3.arz` `e990e1265f14ff2ee241658433d4d666d399a5b0be27543ae9481fc97d6a2ae4` (47,552,036) · `database/templates.arc` `679db83f019020ef7d4d27be8e61203006ee94e5c582dd8a59642f3fddd54602` (793,541).
Record counts derived: base 34,171 · gdx1 18,453 · gdx2 16,454 · gdx3 24,307 · sm1 1,005 · sm2 811 · sm3 1,433. Templates 819 entries.

**Edition I (drift control):** `database/database.arz` `8cdeff128422c765278087b7e4f95a41b59be8ee51184370d139c451afb5ae3f` · `gdx2/database/GDX2.arz` `f6d5bd67602ce5af2de394507c36f198a9388be26350517434e7ff5e4ee1e985`.

**Sim** (`~/Games/reincarnated-engine/src/reincarnated/simulation/kc2/`): `kinematics.py` ⚑ `8268735dcd37f10743d5c12957126e6ac543280119eb888cc7a6e52267a32e13` (34,084) · `player_locomotion.py` `cebfac464d75254ca153d0190279f565276dd603e2728012c36520b06f7353bb` · `run.py` `3ed86119c964b1067216541ee5e66596f8fd9df47cce8506ce9a5127323cd4b0` · `engagement.py` `d57d3bc9bdebfc2def10d1a4c913a45d1f858b9f8497f51b9012e76ea71e6f9e` · `locomotion.py` `3f2abf7d810cbcd03b49a45ded29694e287dbb3a5800bf9c4e3530c62b62ef5a` · `player_offense.py` `5be276e7805d3f2cf13e5e91ecfd43facb418bdb7d3573093f9827ab27acc010` · `player_drive.py` `082a214d878411f49b55fb74d46582f4565f37e7efa559dee3f3c0b76fdcff27` · `disc.py` `d5631db8eeaaddf7bea15fd042f463b42885f2c74790e8a12eb30066ce3c7ebe`.

**Sealed (K-7, READ-ONLY):** driver `gamora_kc2_mpol2_channel_policy_2026_08_25.py` `ecb9017c56a30f4554b6920b5b0771122e22739cae6d4cedbde85fc0bc6fb7db` · cell `kc2-checkpoint-E-s09-cp150-mpol2-20260825_114420.json` `ad61ad2a8c799d6ef11a68436756c253f0a34fbb1052e575cdf9f9cd3a44dc5c`. ⚑ **Derived PRE and POST: identical. No sealed cell re-run.**

**Data + prior findings:** `pm4l_target_multiplicity.csv` `9fc53083723ba47f88de063fa0977e38a0b4dfb419d56d0cd3d738bee78a102e` · `pm4h2_observables.csv` `61c25fab2f22c91fc8ee9260517a1e1e4fbdc8b09b1427f5f7551d9c4209c042` · `pm4h2_ring_density.csv` `a675367c9f46cedcb3413b3c43dfa0ac2aa0591c8ae120dcef05ce9a2f903eb5` · `pm4m_body_chain.csv` `fb8624cb0ef4b6c292ad5f1d6b89bdb55ac0ba01eded25e52434c9f4e00a4797` · pack `provenance.json` `dabdc53e1380dc5791e3b8036d43555015a1ec0cade60d475ec00be12ea5d28e` · Lap U `pm4u_findings.md` `f1a34cb11c6015d83169bd2ebbb7fd3ee7ba15bbc20622756f37fbb75fbec6ce` · Lap R `pm4r_findings.md` `c223dfb04653a7e8682d5c1dd42356fc2a8398b06951372445d235a6eff224ea` · `pm4r_movement_episodes.csv` `dc3173ae53c2a371d9336e95db79c25c4deb04834cebdd4c9318f554d9f576cc` · `md-b4app-2d/findings.md` `22d63b6952bb3a7a940231565861e8a804d764d1f0e5ef3c41a97d3cacfdec88`.

**Tooling (banked lanes, reused verbatim):** `gd_arz_adapter_2026_07_24.py` `040bd078a73f81ed7b839820fcfc15af1e74beba81a930fc147f1080bb317266` · `gd_arc_reader_2026_07_26.py` `a5def5a669270f6362f96dfcb932d0ba8a77b689919086675b97b95fa16f7597` · `gd_gdc_ui_settings_v7_2026_08_23.py` `26aa5cb02fcaec4520b4b456ee4040f5f73f356c69fab508762c86afed4c5c4e`.

## § 8 — WHAT THIS LAP HANDS THE CONDUCTOR

1. **B1 mechanism: CLOSED to the binary boundary.** § 2 is liftable as rows-not-fields with (value, scope, provenance) triples: 13 engine constants + 8 `selectionBias` values + 4 developer descriptions + the `targetingMode` enum + per-skill acquisition for 4 bound skills. ⚑ **U-1…U-5 must ride with them** — the parameters must not ship implying a known function.
2. **B1 policy: UNDECODABLE-FROM-SUBSTRATE, DECLARED**, with 15 searched surfaces and the structural reason. Per charter § 2.2 a galadriel lap fires before the declaration stands; **not fired by this seat.** The precise discriminator worth commissioning is **U-7**, not a general "watch the targeting" pass — and **U-9 constrains what such a lap can return.**
3. **Residual candidacy: SURVIVES, reshaped** (§ 5.3). The operative absence is **board-blind positioning**, not body-picking.
4. **Two uncommissioned findings, routed not actioned:** § 4.2 (the incumbent's board-blind decode cites a test its own source declares uninformative — against my own seam) and § 4.4 (`"retargeted"` is monster-side and will be misread).
5. **No HALT condition.** Completed against non-footage substrate as chartered; nothing requires Matt.

---

**Deviations to note:** findings file could not be written (harness); returned above for conductor capture. Commit contains the seven predecessor artifacts only — verified via `git show --stat HEAD`, no concurrent-session files swept in. Not pushed.
