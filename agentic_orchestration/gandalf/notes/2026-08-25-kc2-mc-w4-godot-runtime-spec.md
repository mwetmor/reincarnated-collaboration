# W4 · THE GODOT RUNTIME SPEC — what the runtime must implement

> ▶ **ROLE: SPEC-AUTHOR** — Wave-4 piece, charter tag **SKIRT**.
>
> **STATUS:** SPEC — consumable by a later drax session. **Spec, not code.** No production code in this seat; the build is a separate session (charter § 7 seat-map: drax is **recipient-only** this run, and this file lives in the run's notes, never in `reincarnated-godot/`).
> **Run:** KC2 MODEL-COMPLETION RUN · **Wave:** 4 (export + handoff) · **Date:** 2026-08-25
> **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`) · **Conductor:** gandalf `RUN-CONDUCTOR`
> **Companion:** `2026-08-25-kc2-mc-w4-twin-test-spec.md` (charter tag F-5) — *how this is proven.* Read this file first; that one grades it. **F-5 camera re-ratification is a hard requirement on this build and lives there** (twin-test § 6.1) because it is an owner-eye gate.
> **Authority rows:** charter § 1.4 + § 3 Wave 4 · **RULING-NOTE** `2026-08-24-kc2-model-pack-reframe-and-gap-rulings.md` §§ 1–2 (the two-layer reframe + facet rulings (a)–(i)) · ledger **L-19 / L-27** (arena boundary UNDERIVABLE-FROM-SUBSTRATE, path named) · **L-68** (the video-measured Class-1 boundary + R-L68-2 scale pin) · **L-83 / L-85** (channel policy + the two DO-NOTs) · **L-88** (built + sealed; A-1…A-6 approximations; D-MPOL2-1/2) · **L-89** (per-skill binary flag, not a die roll) · **L-90** (the mechanism rule; NOT RECOVERED list) · schema `2026-08-24-s1-baton-v2-schema-draft.md`.
> **Standing law:** **Law 3** (no fitted constants, no invented rules) · **D5** · **GL-6** (verify digest before load) · **GL-7** (linear interpolation between knots IS the position function) · **GL-10** (use the wire's constant; never re-derive one it carries) · **GL-12** (absence is DECLARED, not filled) · **GL-13** (the pinned rectangle is a fact about the recording, not an extent claim).

---

## 0 · Headline — the constitutional inversion

**v1 was a recording.** `kc2_baton.gd` states its own law at line 22: *"this file computes no damage, resolves no hit, decides no death, and moves nothing the baton did not move."* **v2 is a model-pack, and the runtime does all four.**

What does **not** invert is the honesty half of that law. The v1 consumer's gates (`GL-6` digest-before-load, `GL-9` read the shape word, `GL-10` the wire's constant, `GL-12` absence declared, `FG-13` the need-list census) are **carried forward and widened**, not retired. The one change is *who may fill an absence*: **the runtime may fill, but only by registering a runtime choice against an `absent_ref`, surfaced in a ledger.** Silent filling is the failure mode this whole architecture exists to make impossible.

**Consumer role:** `MODEL-RUNTIME` — reads `model/` **only**. It never loads `reference/`; only the twin-test harness does (S-1 § 4).

---

## 1 · LOAD + GATE SEQUENCE

1. **Digest.** Verify the **pack digest**, then each **member digest** (S-1 § 1). A member whose digest fails is a **load abort**, not a warning. GL-6 at two levels.
2. **Version.** `_schema_version: 2` / `pack_format: "kc2-model-pack/v2"`. v1 consumers fail closed on a v2 pack — correct behaviour, nothing to fix.
3. **Wire constants verbatim (GL-10).** `tick_period_s`, axis convention, arena figures, placement extents, scatter shape word. **Never re-derive a constant the wire carries.** Absent constant ⇒ load error naming the field, never a default.
4. **Parameter resolution (DR-3).** Every rule value is a `(value, scope, precedence, provenance)` object. Resolve by precedence; **two overlapping scopes at equal precedence is a hard error**, never resolved by array order. The founding case is live: **ViewDistance is 15.0 m population-wide (WR3-W2) and 80.0 m on 169/169 rolled tier-16 Crucible monsters (Lap U)** — both measured, both true in scope, and waves 150–160 are governed by the Crucible override.
5. **Rule census (FG-13 generalised).** Emit the three-valued disposition table over rules · states · skills · stats · entities. This is the twin-test's **G-0** input and it is produced by the runtime, not by the harness.
6. **Absence ledger (GL-12).** Every `absent_ref` the runtime touches gets a runtime-choice entry: what was chosen, by whom, and that it is the consumer's choice — **never laundered back as model truth.**

---

## 2 · TICK, DETERMINISM, MOTION

- **Tick.** `tick_period_s = 0.0816326530612245` (= 1/12.25); `run_tick` is the one global clock (GL-11). `binding_class` on the wire declares whether the runtime **must** step at this rate (`MODEL-BINDING`) or may pick its own (`SIM-ARTIFACT`) — see **OQ-3**.
- **Recommended posture either way:** fixed-tick simulation with **render interpolation between ticks** — the same discipline GL-7 already imposes on positions. drax's `apply_tick(tick_f)` in the SB-1 build is already a pure function of the tick with no accumulator, no easing, no velocity integrator; that shape carries.
- **Positions.** GL-7: linear interpolation between knots **is** the position function. Do not fit one speed per body — that puts bodies where the model does not.
- **RNG.** The runtime uses **its own** RNG, at the **declared draw sites**, in the **declared consumption order** (`model/rng_contract.json`). This is what makes divergent play well-defined rather than improvised. Exact reproduction for the twin-test comes from the Layer-2 **tape**, not from reimplementing MT19937.

---

## 3 · ⚑ THE MECHANISM RULE — input architecture (this run's design payload)

**This is the single most transferable thing the run produced, and it carries no Grim Dawn skill with it.**

**LAYER 1 — the rule the runtime implements:**

> **BINDING EXCLUSIVITY.** The channel is bound to **one mouse button**. Activating the skill bound to **the other mouse button** releases the channel. Skills bound to **keyboard** keys are **fully transparent** to the channel — they cast without releasing it.

The basis (L-90): slot **R** is the channel itself (Eye of Reckoning, right mouse — *the only bar skill in the save with no `skillCooldownTime` field at all: the format's own signature of a channel*); slot **L** is the left-mouse skill (Blitz). **Left-click activation and held right-click channel are mutually exclusive character actions.** The keyboard-bound War Cry is transparent at **0.000** across 19 casts, and the ticks *tighten* around its casts (p = 4.9 × 10⁻⁷ *less* interruption than the duration-weighted null). Vire's Might — also keyboard-bound, also a charge skill — sits at **0.136**.

**Why the rule is BINDING and not SKILL-CLASS:** three `…Charge`-class skills were bound on that bar (Blitz L 3.5 s; Vire's Might key-2 3.6 s; Rune of Rush key-7 2.5 s). Slot 2 carries 22 of the 53 casts and is *not* the family outlier. **"Charge skills interrupt" is not the rule the evidence points at; "the opposite-mouse-bound skill interrupts" is.**

**Named residual, shipped with the rule (L-90):** slot 7 (Rune of Rush) is **footage-blind** — its casts are outside the 53-cast population — so *left-click-interrupts* and *charge-interrupts* **cannot be fully separated** on this evidence. The rule ships with the residual attached, not with the residual quietly dropped.

**LAYER 2 — measured per-skill reference values** (reference only; the runtime derives from the Layer-1 rule, it does not read these as parameters):

| binding | skill | casts | P(interrupt \| cast) | note |
|---|---|---:|---:|---|
| **left mouse** | Blitz | 13 | **0.385** | p = 0.00034 vs the null |
| key 2 | Vire's Might | 22 | **0.136** | p = 0.104 — *not* distinguishable from L at this n |
| key 3 | War Cry | 19 | **0.000** | fully transparent; ticks tighten |
| right mouse | Eye of Reckoning | — | — | **is** the channel |
| key 7 | Rune of Rush | ? | **BLIND** | never dims; outside the population |

**Interrupt duration when it fires:** median **0.60 s**, range **0.53–0.67 s**, n = 8 — the tightest distribution in the measurement.

**⚑ NAMED APPROXIMATION, carried on the wire, not hidden (R-L89-2 / R-L90-2):** the sealed sim implements a **uniform 0.15 per-cast roll**. It is *arithmetically true and mechanically false* — a **cancellation** of an always-interrupting family against a never-interrupting one, not a probability. **The runtime implements the flag shape; the 0.15 ships labelled as an approximation** in the baton's cast-interrupt row. What the uniform roll costs, in the player's terms: *under a die roll the player has no move that is safe to weave; under a flag, one skill is safe, and choosing it becomes a decision the referent was demonstrably making — 19 times without a single break.*

**Implementation note for the Reincarnated product seam, not just this fight:** implement this as an **input-architecture rule over bindings**, not as a per-skill data field. A per-skill `interrupts_channel: bool` reproduces this fight and teaches the engine nothing; a binding-exclusivity rule is a mechanic the project's own kits inherit for free.

---

## 4 · THE CHANNEL MODEL

| # | parameter | value | provenance |
|---|---|---|---|
| 1 | `channel_breaks_on_movement` | **False** — the channel survives movement | MD-B4app-2: P(chan\|moving) 0.892 > P(chan\|stationary) 0.738 |
| 2 | `energy_gated_release` | ⚑ **DO NOT IMPLEMENT** — see below | 2b § 3 |
| 3 | `release_duty` | **≈ 10.5 %** of combat; one release every ≈ 9.6 s | energy 60 Hz |
| 4 | **TYPE A — `release_on_wave_transition`** | fires at the wave flip; onset lag **median 1.60 s** (8/11 within 2.0 s); duration **median 1.03 s**, IQR 0.62–1.56, max 3.50 | energy + wave badge; Fisher p = 0.00336 |
| 5 | **TYPE B — `release_on_cast`** | duration **median 0.60 s**, IQR 0.55–0.63 — and per § 3 it fires on the **binding**, not on a roll | energy + skill bar |
| 6 | `cast_rate` | **0.290 /s** (one every 3.45 s) | skill bar |
| 7 | `release_stationary_bias` | duration-weighted `frac_moving` **0.402** vs fight-wide 0.6265 — **ship as a RATIO** (§ 8) | motion 20 Hz |
| 8 | drain / tail / rotation | `drain_rate_per_s` 176.4 `PER_TICK` · `channel_tail_s` 0.25 · `rotation_speed_multiplier` 0.35 · `radius_m` 3.0 | L-22 pins |

### 4.1 · The two DO-NOTs — enforced, not advisory (L-85, and they were AST-scanned in the sim build)

1. **`energy_gated_release` — NEVER.** **H-MC-1 is REFUTED on its trigger.** Every release began at **≥ 0.846 of the operating ceiling** (median 0.960; two began *at* the ceiling); 8/19 began on *rising* energy; **12/19 reached the ceiling before they ended and were HELD there** (37.8 % of release time at cap, max hold 2.42 s) — *a conservation move ends when the resource returns; these do not.* Any energy floor at or below 0.85 × max is **behaviourally inert** on this footage: it would never have fired once in 182.65 s. If the parameter must exist structurally, set it to a value that never fires and **record it as INERT, never as calibrated.** A threshold fitted to make Type-A releases look energy-driven would be **fitted to noise** — Law 3.
   > The finding under the finding, and it is the design one: **he was not counting his energy; he was counting the fight.** The wave-transition release IS the design-true behaviour.
   > Per the L-84 discipline: this **refutes an execution, never the testimony.** Matt's stated intent was a hypothesis *source*; it did its job by being testable.
2. **No release-on-every-cast.** At the referent's cast rate that adds ≈32 s of released time to a 183 s fight and drives uptime far below the measured 83.8 %. **The measured shape is: casts are channel-transparent by default, with an interrupting minority (§ 3).**

### 4.2 · What the corrected policy did NOT do — carried so the next session does not rediscover it as a bug

L-88, plainly: with the fix built and sealed, **terminal wave moved 153.0 → 153.2** (σ 1.67 → 2.32) against a referent of 160. **Deleting ~10 % of damage-dealing ticks cost nothing**, and the forecast that survival would fall is refuted with **no mechanism supplied** — the seat correctly declined to explain over five numbers. **Playing like Matt's release pattern was never the survival driver.** Residual candidates, **named and not adjudicated**: Type-B **phase** (unmeasured), **target selection**, **defensive weave usage**. A runtime that reproduces this model and lands short of 160 is **correct**, not defective.

---

## 5 · COMBAT RESOLUTION

The runtime derives damage, resolves hits and decides deaths from `model/math_rules.json`. **`test_vectors` are normative; `expr` is documentary** — implement the rule in GDScript and reproduce every vector to declared precision (S-1 § 2.4). No expression evaluator is required.

Rule families the runtime must implement: damage composition + type resolution · **mitigation in both directions** (monster-side mitigation did not exist in v1 at all) · crit (v1 `NOT_MODELLED`; PM4 introduced limbs — carry the model with its limb selection as a parameter) · leech ladder · **DoT application and stacking** — decoded from binary at D-4b/D-4c: **per-(type, attacker) 100 ms timelines; same-source MAX, distinct-source ADD with per-ordinal weight; no cap** · energy drain/regen · movement + the 3 dash layers · **eHP affine reconstruction — the `G_BAND_A` array ships verbatim, never a fitted shape** (linearising `G` costs 17.49 pp max error ≈ 2.5 % on eHP).

---

## 6 · ACTORS

- **Monsters** — one stat block per `record_path` (S-1 § 2.2): life/eHP anchors + reconstruction rule, offense, **defense (armour · resists · OA · DA)**, AI profile with per-record overrides, skills, **specials with reuse gates**, DoT riders, and monster-summoned pets as their own first-class blocks. A special slot that does not fire ships `fires: false` **with an `absent_ref`** — the schema is deliberately incapable of hiding a borrowed distribution.
- **Player summons** — **Guardian of Empyrion** + **Deathstalker** use the **same actor-template schema as monsters**, `faction: "player_summon"`. Facet (f) is structural, not a special case. (`R-L53-2` — summons carry no recorded *path* — is a **Layer-2** absence and must not be mistaken for a Layer-1 one.)
- **AI states** — the key space is the **43 controller states** enumerated from `Game.dll` strings; every one is a row, with status `DECODED` / `VIDEO_MEASURED` / `DECLARED_ABSENT` / `UNREACHABLE`. There is deliberately **no `ESTIMATED`** at this layer. The runtime executes `DECODED` rows and registers a runtime choice for every `DECLARED_ABSENT` row it touches.
- **Pets — Matt-ruled, no design coupling** (L-83 D-3): *"I did not have a pet."* The decoded Guardians are non-pet furniture; Reincarnated's loot-carrier pet is unimplemented and **PARKED**. Wave-4 pet/summons rows ship as **Layer-1 decoded truth only** — the runtime must not use them as a design premise for the product's pet system.

---

## 7 · ⚑ SKIRT — ARENA, CONTAINMENT, AND THE HAZARD ZONES

**Three claims the word "bounds" fuses, kept apart on the wire (S-1 § 2.6):**

1. **What substrate says.** `arena_bounds.shape = "UNBOUNDED"`, `collision_model = "OPEN-PLANE"`. The Crucible boundary is **UNDERIVABLE-FROM-SUBSTRATE with the path named** (D-5 / D-5b): terrain does not close the arena (flood-fill exits all four sides at every threshold); no bounds field, no blocker entity, no Lua leash, no stored nav map; what closes the arena is entity collision behind `NavManager::CreateNavigationData`, undecoded — **and reimplementing it is inventing a rule.** The first-pass polygon was **deleted, not shipped**, because the engine-faithful cell put three shipped anchors including `tier16spawnpoint01` *inside* blocking geometry — falsified by the game's own data.
   **Salvage that DOES ship, and is baton-critical however containment rules:** `NavManager::SetDefaultConfig` — **cell 0.25, agent height 2.0, agent radius 0.8, max climb 0.5.** Use these for the Godot navigation bake; do not pick your own.
2. **The measured occupancy hull.** `86.915 × 85.303 m` is a **FACT-ABOUT-THE-RECORDING** — 5,085 recorded positions plus one 3.0 m sweep radius — **not an extent claim.** GL-13 pins the rectangle in the world; **placing a wall on it is a fitted constant.** (C-1's binary was declared **UNEARNABLE in both directions**: the rectangle is the paths' own AABB by construction, so a crossing check against it is near-tautological.)
3. **The video-measured boundary — this is new since S-1 and it is the buildable object** (L-68, from Matt's own 21-shot perimeter circuit): a **177-vertex outer ring + 4 interior obstruction rings** (2 symmetric inner-wall arcs, 2 south-lobe blocks), extent 201 × 269 minimap px, floor 27,875 px²; **per-vertex uncertainty ±2.5 px, both terms measured**; **coverage TOTAL** — 0/1755 boundary px abut unobserved canvas, every vertex ≥3 observations (median 13). Geometry of record: `agentic_orchestration/galadriel/notes/…/crucible-arena-geometry-v1.json`. **Evidence class is `video-measured` — weaker than `decoded-substrate`, and it is labelled as such wherever it is consumed.**

### 7.1 · Three traps that will otherwise ship wrong geometry into Godot

- ⚑ **Do not re-add the phantom pillars.** Of seven candidate "interior obstructions", **three were teal pedestal HUD icons.** Four survive. A build that reads an earlier draft grows three pillars that do not exist.
- ⚑ **Two arcs due north are MAPPED-BUT-NEVER-WALKED and are FLAGGED, not interpolated.** Do not smooth them closed.
- ⚑ **The metre scale is `DERIVED-WEAK`: u = 0.198 m/minimap-px, band [0.094, 0.366] — a 1.7× spread.** The native-px geometry **does not inherit it.** **R-L68-2 fires the pin at Wave-4 assembly** (register the Class-1 footprint against the final pursuit model's occupancy hull). **Until the pin lands, every metre figure derived from this geometry is provisional** — and per twin-test OQ-4 that bears directly on when the camera gate can fire.

### 7.2 · Containment policy — a CONSUMER CHOICE, declared as one

```jsonc
"runtime_containment": { "policy": "SKIRT",
                         "claim_class": "PRESENTATION-CHOICE-NOT-MODEL-TRUTH" }
```

**R-CPA-3, Matt-ruled:** *"skirt for SB-1, walls at the authored level."* The SKIRT as built (drax, SB-1 A2 item 1) is the reference implementation and its discipline is what makes it honest rather than decorative:

- an **800 × 800 m dress plane, 1 cm under the measured floor**, whose half-extent is a **presentation choice with NO WIRE BASIS and says so in its own report row**;
- it is **not** the clip surface — `clip_rect()` reads the footprint and **cannot** read the skirt, asserted by **identity** against the floor *and* by **difference** against the skirt, so a clip rect that had quietly grown to 800 m **fails**;
- it is **not geometry** — 1,430 nodes walked, zero `CollisionObject3D`/`CollisionShape3D`/`CollisionPolygon3D`;
- the camera **never reaches its edge** — `camera_ground_gate(eye, look, fov, aspect, far)`, nine frustum rays intersected with the ground plane, each landing inside the skirt **or** beyond fog saturation, per-frame, HALT on red. Fog discipline rides with it: `fog_density` is the density reached **at** `fog_depth_end` in DEPTH mode (not a per-metre rate — 0.006 carried across ran the fog at 0.6 % strength and produced a lit grey plain with a hard horizon), fog colour **identically** the background colour, skirt albedo 0.038.

**The fork this build must resolve, because a live player can walk where a recording did not (OQ-1):** SB-1 was a *presentation*; this is a *playable character*. Options: **(a)** SKIRT + a soft clamp registered in the runtime-choice ledger · **(b)** **authored walls built from the § 7 (3) video-measured ring** — R-CPA-3's own "walls at the authored level", now that an authored object exists · **(c)** unbounded + fog + camera gate only. **Lean: (b)**, with the wall declared `video-measured` and `PRESENTATION-CHOICE` in the same breath — the *sim* stays unbounded (B-7 dissolved: there is no decoded wall object to build), so the wall is a **level-authoring fact, never a model fact**, and the two must never be allowed to read alike.

### 7.3 · The hazard zones — a named absence that reaches the player's hands

**Class 2 (green zones): 6 zones DEMONSTRATED** (15/15 pairs separated on evidence), each a measured interior point plus a radius **UPPER bound** (23.3–52.0 px). **The count ships `≥ 6`** — a zone entered between exposures leaves no evidence. **Outlines are `polygons: null`** with the reason in-file and the cheapest refuting test named (one dense pass at a single zone). Damage corroboration: 5 in-zone shots show HP down (15,460–17,030 of 20,005) against 15 zone-free stations at full; one anomaly (622: in-zone, full health, lowest green fraction) is **reported, not explained**. **The DoT ships `ATTESTED-UNMEASURED` — no magnitude was invented.**

**Consequence the runtime must carry honestly:** a live player can walk into a hazard whose **shape and magnitude the model does not have.** This is a `blocks_playability` absence in the S-1 sense and it belongs in the runtime-choice ledger with whatever the build does about it — a placeholder radius is a consumer choice and must be labelled as one, never a model value.

---

## 8 · INSTRUMENT HYGIENE — binding on every figure this runtime quotes forward

1. **Ship RATIOS for movement.** Three instruments give the referent's `frac_moving` as **0.883 / 0.705 / 0.6265** — **1.41×**. "Movement excess" is, on this evidence, an **instrument disagreement about the referent**, routed not adjudicated (`D-MPOL2-2`). The sim ships ratios so the instrument cancels; the runtime does the same.
2. **G5's uptime is 0.0960, not 1.9 %** — a **5.2×** correction (`R-L88-5`). Any forward quote uses 0.0960; **the derived "~40×" moves with it and must be RE-DERIVED, never re-quoted.**
3. **A published aggregate can be arithmetically true and mechanically false** (`R-L89-4`). Where an aggregate is quoted, say whether it is a *rate* or a *cancellation*. The 0.15 is the founding instance.
4. **The 6.2 % blind residual** on the release population is **CARRIED**, not closed. If those gaps are releases, duty rises toward 16.7 %.

---

## 9 · NAMED APPROXIMATIONS + OPEN PARAMETERS

**Approximations — the model says this, and it is not exactly what happened:**

| id | approximation | direction / cost |
|---|---|---|
| **A-1** | **one Type-A release per wave transition** vs measured **1.1** | correcting it would likely land duty ≈ 0.110. **PARKED, explicitly not fired** (R-L88-3): correcting an approximation *because a band failed* is band-rescue even when the parameter is measured. It may ride into Wave-4 as a noted refinement **with this reasoning attached.** |
| **A-2** | **Type-B PHASE unmeasured** (rate and duration are measured; phase is not) | a **named residual candidate** for the 153→160 gap (L-88) |
| — | **uniform 0.15 cast-interrupt roll** in the sealed sim | a **cancellation, not a rate** (§ 3). The runtime implements the flag; the 0.15 ships labelled. |
| — | **A-3…A-6** as enumerated in the M-POL-2 math note | carried by reference; the runtime does not re-derive them |

**NOT RECOVERED — open parameters the build must treat as absences, not as zeros (L-90):**

| # | what | state |
|---|---|---|
| 1 | **Cooldown reduction (CDR)** | **NOT RECOVERED — inventory v11 undecoded, and the character carries heavy devotion investment.** Unquantified. Every cooldown in the model is a **base** cooldown; the fight's *effective* cooldowns were shorter by an unknown factor. A runtime that treats base as effective is systematically slow, and **it must say so rather than fit a multiplier.** |
| 2 | **Equipped gear** | **NOT RECOVERED.** Player stats come from the fixture, not from a decoded loadout. |
| 3 | **The poison-DoT item** | **NOT RECOVERED / open question** — an unattributed poison DoT source. |
| 4 | **"No target in range"** — the Type-A mechanism | **UNMEASURABLE from this footage.** The measured correlate is the wave **transition**; the *mechanism* needs a range-to-nearest-monster instrument. Named by galadriel as **the single highest-value follow-on: it is the difference between a Crucible-specific parameter and a rule that transfers to the Godot pilot.** |
| 5 | The channel drain's skill attribution | **EoR-CONSISTENT, never IDENTIFIED** — the HUD publishes a scalar. |

Every row above is an **absence with a reason**, and the runtime's obligation is the same for all of them: **choose, register the choice against the `absent_ref`, and never write the choice back as model truth.**

---

## 10 · ACCEPTANCE CRITERIA — when THIS SPEC is satisfied

- [ ] **R-1** — pack loads under the § 1 gate sequence: two-level digest, version check, wire constants verbatim, precedence resolution with equal-precedence overlap as a hard error.
- [ ] **R-2** — **rule census emitted** (§ 1.5) with three-valued dispositions over all five facets, plus the **runtime-choice ledger**. This is the twin-test's G-0 input.
- [ ] **R-3** — **binding exclusivity implemented as an input-architecture rule over bindings** (§ 3), *not* as a per-skill data field and *not* as a per-cast die roll; the slot-7 residual carried in its documentation.
- [ ] **R-4** — channel model per § 4 with **both DO-NOTs structurally enforced** (the sim build enforced them by identifier-only AST scan; an equivalent mechanical check is expected here — a comment is not enforcement).
- [ ] **R-5** — `math_rules` implemented in GDScript, **all `test_vectors` reproduced** to declared precision.
- [ ] **R-6** — summons instantiated from the **same actor template as monsters**; no special case.
- [ ] **R-7** — containment declared as **`PRESENTATION-CHOICE-NOT-MODEL-TRUTH`** with the § 7.2 fork resolved and recorded; the three § 7.1 traps checked *by assertion*, not by care; nav bake uses the decoded `SetDefaultConfig` values.
- [ ] **R-8** — every § 9 open parameter present in the ledger as an absence with a registered runtime choice; **no fitted constant anywhere** (Law 3).
- [ ] **R-9** — **F-5 satisfied** per twin-test § 6.1: no prior camera ratification treated as transferring; the build's camera row reads **PROVISIONAL** until Matt's eye rules on an identified frame *of this build*.

---

## 11 · OPEN QUESTIONS BACK TO THE CONDUCTOR

**OQ-1 — containment for a playable character.** (a) SKIRT + soft clamp · **(b) authored walls from the video-measured ring (leaned)** · (c) unbounded + camera gate. Note the layer asymmetry this creates and that it is *correct*: the **sim** stays unbounded (B-7 dissolved) while the **level** has walls. Conductor's call whether that asymmetry needs Matt's eye — it is visible-consequence territory, and facet (h) was a commitment boundary once already.

**OQ-2 — the hazard zones (§ 7.3).** Six zones with radii-as-upper-bounds, `polygons: null`, DoT `ATTESTED-UNMEASURED`, count `≥6`. For a *playable* build this is a `blocks_playability` absence. (a) ship the absence and let the runtime choose visibly · (b) commission the cheapest refuting test already named (one dense pass at a single zone) before the build · (c) omit hazards entirely and declare the omission. **Lean: (a) now, (b) queued** — omission is the one option that makes the arena *feel* wrong without saying so.

**OQ-3 — is `tick_period_s` model truth or a sim artifact?** (S-1 OQ-7, still open.) `MODEL-BINDING` makes the twin-test tractable but promotes a sim convenience to game truth **for the product seam**; `SIM-ARTIFACT` is honest and makes exact twin-testing much harder. **Lean: `MODEL-BINDING` with the limitation recorded** — the product-seam question is properly Matt's, and this baton is the prototype of the engine→Godot contract the product ships.

**OQ-4 — CDR (§ 9 row 1) is the largest unquantified lever in the model.** Every cooldown ships as base; the fight's were shorter by an unknown factor. (a) ship base + the absence, accept a systematically slow pilot · (b) commission an inventory-v11 decode lap · (c) bound CDR from the footage — measured icon dim durations vs DBR base cooldowns *(and note that two such deltas already exist and are small: Blitz +0.10 s, Ascension +0.4 s — which is itself evidence worth a look before commissioning anything)*. **Lean: (a) ships now, (c) is cheap and may make (b) unnecessary.**

**OQ-5 — does the runtime spec bind the product seam or only this fight?** § 3's closing note argues binding-exclusivity should be built as a **project** input rule rather than a KC2 data field. That is a design-direction claim beyond this run's charter and it belongs to Matt, not to a spec. Flagged, not asserted.

---

*Filed 2026-08-25 by gandalf (`SPEC-AUTHOR`), Wave-4, KC2 MODEL-COMPLETION RUN. No production code. Files to run notes per charter § 7; committed, not pushed — the conductor releases.*
