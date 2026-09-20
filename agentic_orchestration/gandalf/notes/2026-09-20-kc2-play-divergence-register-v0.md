# KC2-PLAY · THE DIVERGENCE REGISTER — v0

> **STATUS:** CURRENT — **v0, 2026-09-20.** The register of record for Run KC2-PLAY. One row per switch by which the **`PLAY`** configuration differs from the **`ORACLE`** configuration, plus the non-divergences carried with a named confound.
> **Authority:** charter `2026-09-20-kc2-play-run-charter.md` § 2 (*the central design: ONE runtime, TWO configurations, a DIVERGENCE REGISTER*) + rulings **R-KP-0a…0f**, **KP-1**, **KP-2 (L4, L5)**, **KP-3** · Matt rulings **Q81 F1–F7**, **D-CP2-1/-2**, **D-LIFT-1/2**, **R-L3-2** · jack-ryan Gate-1 **WARN-2** (the fifth attribution class) and re-check **WARN-2 PARTIAL** (unfuse `placeholder` from `instrument`) — `qa/findings/2026-09-20-run-KC2-PLAY-charter-gate1.md`.
> **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`), Wave 1.
> **Companions:** `2026-09-20-kc2-play-ta-prereg.md` (T-A decision rules — **none of the `DIV` rows below is graded by T-A, by construction**) · `2026-09-20-kc2-play-2d-retarget-spec.md` §§ 3–6 (view, input, telemetry) · `2026-08-25-kc2-mc-w4-twin-test-spec.md` (the tier definitions) · `gamora/notes/2026-09-20-kc2-play-p0a-traceability-census.md` (the behaviour census this register indexes against).
> **Standing law:** Law 3 · K-7 · GL-12 (absence is DECLARED, never filled) · R-L89-4 (an aggregate says whether it is a *rate* or a *cancellation*) · digests and hashes **derived at use, never retyped**.

---

## § 0 · What this document is for, in one paragraph

The P0 returns showed that the oracle and the thing Matt asked to play **are deliberately not the same fight**. The run holds them apart by construction: one runtime, two configurations, and *every* switch between them enumerated here. **The config id and this register's hash are stamped into every telemetry file.** A T-B miss is then attributable to exactly one of **five** classes (§ 5) — and **a difference that is in none of the five is a defect in this register**, not a mystery.

⚑ **The register's value is not that it lists what we changed. It is that it makes "we changed something and forgot" a checkable claim.** Every `DIV` row names how it is tested *given that T-A cannot grade it*, and every row names the direction it is expected to push a T-B statistic — **before** any T-B statistic exists.

---

## § 1 · INDEX

| id | switch | class | status |
|---|---|---|---|
| **DIV-01** | arena wall — circle `R = 43.758…` m vs the video-measured ring at registered `u` | DIVERGENCE | ACTIVE |
| **DIV-02** | spawn-pool DoT magnitude — `0.0` vs D-LIFT-1/2 | DIVERGENCE | ACTIVE |
| **DIV-03** | cast-interrupt rule — uniform 0.15 cancellation vs the per-skill `interrupts_channel` flag | DIVERGENCE | ACTIVE |
| **DIV-04** | Type-B auto-resume under held RMB | DIVERGENCE | ACTIVE (KP-1, Matt-accepted at KP-2 L5) |
| **DIV-05** | pilot — `DRIVE_TO_PACK` scripted vs Matt's hands | DIVERGENCE | ACTIVE |
| **DIV-06** | bound skills — Blitz / Vire's Might / Rune of Rush additions OFF vs ON; riders `PLACEHOLDER-INERT` | DIVERGENCE | ACTIVE (R-KP-0e) |
| **DIV-07** | Vanguard Banner **placement** (the ×2.0 modifier itself is NOT a divergence) | DIVERGENCE | ACTIVE (R-KP-0f) |
| **DIV-08** | summons **presentation** — drawn beside the player; no health bar, no view-side `hp` | DIVERGENCE | ACTIVE (R-KP-0b) |
| **DIV-09** | `u` — the metre scale the oracle does not have | DIVERGENCE | ACTIVE (R-KP-0c, R-L3-2) |
| **DIV-10** | zoom / view register — `ZOOM-GD` default, `ZOOM-HOUSE` toggle | DIVERGENCE | ACTIVE (F4) |
| **DIV-11** | player kinematics integrate at render rate and are sampled per tick | DIVERGENCE | ACTIVE (F1 rider) |
| **DIV-12** | one life + restart key + scope window | DIVERGENCE | ACTIVE (F6) |
| **DIV-13** | ⚑ **entry state — does PLAY *play* wave 150, or resume the `cp150` state?** | DIVERGENCE | **UNRESOLVED — not in the charter. § 8 OQ-1** |
| **DIV-14** | ⚑ **potion agency — auto-fire at θ vs a human's finger; and F3 binds no potion key** | DIVERGENCE | **UNRESOLVED — not in the charter. § 8 OQ-2** |
| **ND-01** | fire-time damage resolution — strafing does not dodge | NON-DIVERGENCE + confound | CARRIED (R-KP-0a) |
| **ND-02** | no player crit | NON-DIVERGENCE + confound | CARRIED |
| **ND-03** | base cooldowns; CDR not recovered | NON-DIVERGENCE + confound | CARRIED (R-L91-7(a)) |
| **ND-04** | ⚑ **three** known-bad live limbs (charter L4 says two) | NON-DIVERGENCE + confound | CARRIED — **count correction, § 7** |
| **ND-05** | `health_max` constancy (`D-Q1` / B-18) | NON-DIVERGENCE + known model gap | CARRIED |
| **ND-06** | spawn scatter law — polar disc in both; **the pack says box and warns off the disc** | NON-DIVERGENCE + pack trap | CARRIED |
| **ND-07** | `hit_test_model` — pack says `"point"`, both configs run the uniform 3.0 m disc | NON-DIVERGENCE + pack trap | CARRIED |
| **ND-08** | monster-side mitigation, census (c-2) | **PENDING-W1** — gamora's refuting test; V6 is written to its answer (R-KP-0d) | **WILL MOVE THE HASH** |

---

## § 2 · DIVERGENCE ROWS

### DIV-01 · ARENA WALL

| | |
|---|---|
| **ORACLE** | `arena_fold` armed **only in the W1 arm**: shape **CIRCLE**, `R_wall = 43.758085029822276 m` (`= max\|emitter\| 35.758085 + PLACEMENT_EXTENTS_M 8.0`), response **STOP, never slide**, class `MODEL-FACT-DERIVED-FROM-DECODED-SPAWN-GEOMETRY`. In the M-POL-2 / M0 arms, `arena_fold = None` — **the sealed reference cell is WALL-LESS** (census W4). The ring's rotation into the sim frame is **UNDERIVABLE**, which is why the sim's wall is a circle. |
| **PLAY** | the **video-measured ring** — 177 outer vertices + 4 interior obstruction rings, geometry of record `galadriel/notes/crucible-arena-geometry-v1.json` sha `68d895d7…` — drawn in native minimap px and scaled by the registered `u` (DIV-09). Containment resolves **in the runtime, in metres, against the ring polygon**; the plate's wall art is a *depiction* of a rule that lives elsewhere. |
| **Authority** | **R-KP-0c** (charter § 2: the arena is a swappable data object; the wall-less hull is retired as a scale-pin target) · **D-CP2-1** (Matt: *"live walls for both"*) · R-L3-2. |
| **How it is tested** | **Geometry-true assertion (R2D-6):** 177 outer vertices asserted against the JSON at the pinned sha, vertex set **identical** (no resampling, spline, decimation or hull), `interpolated_segments == []`, **exactly 4** obstructions or the build **fails load**, the two `unwalked_arcs` `[0→8]` and `[174→176]` carried **flagged, not smoothed**, the north-gate landmark at the **TOP** of the plate. **Physics-negative (R2D-3):** zero `CollisionObject2D`/`CollisionShape2D`/`CollisionPolygon2D`/`Area2D` on the plate, on any token, on any VFX node. **Unit probe:** a body driven at the ring boundary STOPs and does not slide. ⚑ And the ORACLE side is graded by T-A **E-7a/E-7b** — so the circle is proven before the ring replaces it. |
| **Expected direction on T-B** | charter R-KP-0c declares it: **a tighter walled arena than the sealed spread.** Shorter time-to-contact; higher body density near the player; **shorter per-wave durations and higher per-wave intake**, both pushed the same way. Magnitude is unbounded because it compounds with DIV-09. |
| **Handoff sentence** | *"The wall is the one measured from your video, not the circle the simulation used. It is tighter and it is not round — and how big it is in metres is still uncertain (see below)."* |

### DIV-02 · SPAWN-POOL DoT MAGNITUDE

| | |
|---|---|
| **ORACLE** | `POOL_DOT_MAGNITUDE_ABSENT = 0.0` — the arm of record. **Pools are inert.** Geometry: the **six emitter discs at radius 8.0 m** (`PLACEMENT_EXTENTS_M`, a declared semantic shift), **player-faction only** (`pool_dot_faction: "player"`), source id `w1_spawn_pool_hazard` so it **ADDs** rather than MAXes against a monster timeline (census W5). |
| **PLAY** | **D-LIFT-1**: ⅙ of max pool per tick, **defences ignored**. **D-LIFT-2**: ~1 s ticks, death ≈ 6 s, **crossable-not-campable**. Against 20,005 HP that is **≈ 3,334 hp/tick and death in ≈ 6 s**. Radii ship as **UPPER BOUNDS**, labelled; count ships **`≥ 6`**; `polygons: null` with the reason in-file. **Pools are NON-BLOCKING** (`green_zones.class_note`: *"ENTERABLE DAMAGE FIELDS, NOT WALLS"*) — a pool built as an obstacle inverts *crossable-not-campable*. |
| **Authority** | **D-LIFT-1 / D-LIFT-2 — Matt-ruled model-design values.** 2D spec § 3.2 (*the magnitude is no longer a runtime choice; a build that registers one has ignored a ruling*). The `absent_ref` row survives as the record of what the **footage** did not measure (`dot_mechanic.provenance: "ATTESTED-UNMEASURED"`, `magnitude: null`, `element: "suspected-poison"`) — the ruling is a design decision *about the game*, not a claim about the referent, **and the two must not be collapsed.** |
| **How it is tested** | **Geometry-true probe (R2D-5):** radius, tick cadence ~1 s, magnitude ⅙-of-max asserted. **Unit probe:** a full-health player standing in a disc is dead in **6 ticks**, exactly, defences ignored. **Non-blocking assertion (R2D-6).** **ORACLE OFF-state is a T-A EXACT row (E-8):** total pool damage `== 0.0` in every arm and salt — so the *off* state is proven, not assumed. |
| **Expected direction on T-B** | **Bimodal and mediated by occupancy.** Zero effect if the player never enters a disc; catastrophic if he does. ⚑ **`n_pool_occupancy_ticks` must be reported beside every T-B intake row**, or a pool death reads as a damage-model error. Note the geometry: *the sim's pools are the six spawn discs — which is where every monster arrives.* A lethal pool there is a very different game from an inert one. |
| **Handoff sentence** | *"The green pools kill. Six seconds from full health if you stand in one, and your defences do not apply. You can walk through them; you cannot fight in them. In the simulation they did nothing at all."* |

### DIV-03 · CAST-INTERRUPT RULE

| | |
|---|---|
| **ORACLE** | the **uniform 0.15 per-cast cancellation, folded in**: `DS-TYPEB-RELEASE` bernoulli `p_per_tick = 0.0035510204081632656` = `0.290 × 0.15 / 12.25`. ⚑ **That number IS the cancellation, not a measured rate** (R-L89-4; V19 labels it). `interrupts_fold = None` is *"the only state the M-POL-2 cell can reach"* (census K7/K8). The per-skill fold exists in the codebase with **`armed: bool = False`** and an under-determined cast-mix (`ABS-W2-CAST-MIX`: one equation, three unknowns; `LO → 0.0`, `HI → 1.0`, **neither of record**). |
| **PLAY** | the **per-skill `interrupts_channel` flag** (D-CP2-2): *casting a flagged skill while the channel is **ACTIVE** releases it.* **A skill property — not a rule over mouse buttons and not a per-cast die roll.** Assignment: **Blitz `true`** (0.385 over 13 casts, 5/8 releases attributed) · **Vire's Might `true`** (0.136 over 22, 3/8 — *the datum that killed the pure-binding rule*) · **War Cry `false`** (0.000 over 19; the channel **tightens** around its casts, p = 4.9 × 10⁻⁷) · **Rune of Rush `UNDETERMINED`** — footage-blind, a **registered default, never a measured `false`**. |
| **Authority** | **D-CP2-2** (Matt saw the fork and ruled it) · twin-test § 5 · 2D spec § 5. |
| **How it is tested** | ⚑ **The T-0 FOOTAGE-VECTOR TABLE for the flag rule** (twin-test § 5 final paragraph; acceptance row **A-2**) — graded against the **measured footage**, not against the sim, *which is why it survives every reference re-pairing*: **does an unflagged cast ever release the channel?** (expect **never** — War Cry 19/19 clean). **Does a flagged cast release it?** (expect at rate, **0.60 s median, 0.53–0.67 s range, n = 8**). Plus the negative: `channel_off.cause` is emitted for **every** release (R2D-4). |
| **Expected direction on T-B** | **Aggregate release count and duty ≈ AGREE by construction** (both mechanisms produce ≈ 0.15 in aggregate). **Per-cast attribution DIVERGES by design**, direction pre-named. ⚠ **A builder who inserts a per-cast probability to close the rate residual (Blitz 0.385 vs fight-wide uptime 0.838) has re-created the 0.15 cancellation this whole run took apart.** That is the specific failure to refuse. |
| **Handoff sentence** | *"Blitz and Vire's Might break the spin. War Cry does not — you can shout mid-channel and keep spinning. In the simulation every cast had the same 15 % chance to break it, whichever key you pressed, which is why the two will not line up cast for cast."* |

### DIV-04 · TYPE-B AUTO-RESUME UNDER HELD RMB

| | |
|---|---|
| **ORACLE** | **no such mechanism exists.** The sim has no held-input notion at the fight layer — `ChannelMachine` **is not used by `run.py`** at all; only `compose_damage_basis, tick_period_s, ticks_per_s` are imported (census K2). Releases are drawn, and the channel resumes on the policy's own schedule. |
| **PLAY** | **Type-B releases AUTO-RESUME while RMB remains held** (a mechanical lockout the game serves and ends by itself); **Type-A resumes on input only** (the hand let go). `channel_held` is sampled as a **LEVEL, never as an edge** (2D spec § 2.3) — which is what makes the question answerable at all. |
| **Authority** | **KP-1** — conductor ruling **from measurement**, veto-open; **Matt-accepted at KP-2 (launch-sheet L5)**. Load-bearing evidence is the **within-subject contrast**: the same hand, in the same fight, produced Type-A releases with **IQR 0.62–1.56 s, max 3.50 s** (n = 11); Type-B is **median 0.60 s, IQR 0.55–0.63, range 0.53–0.67** (n = 8). *When that hand chooses, it is loose; Type-B is not loose.* ⚠ Per re-check **WARN-17**, the conclusion is **the better-supported reading, not a proof** — a 0.14 s range over n = 8 implies σ ≈ 49 ms, which is ordinary reaction-time variance. |
| **How it is tested** | **Unit probe on the channel state machine, two cases:** (a) intent level held `true` across a Type-B release → assert resume on the tick the release ends; (b) intent held `true` across a Type-A release → assert **no** resume until an input edge. Plus an assertion that the runtime reads `channel_held` as a level and has **no edge detector** on it. |
| **Expected direction on T-B** | **Raises channel uptime (B-1)** relative to a re-press build, by roughly the Type-B release population's share of the fight. ⚑ **B-1 names this row as its own first suspect** if it misses — pre-registered here, so the attribution is not invented after the fact. |
| **Handoff sentence** | *"If a cast breaks the spin and you are still holding the right button, it starts again by itself. If you let go at a wave flip, it waits for you."* |

### DIV-05 · PILOT

| | |
|---|---|
| **ORACLE** | **scripted.** `PlayerPolicy.DRIVE_TO_PACK` — `S(i) = Σ_{j: \|xⱼ−xᵢ\| ≤ 8.0} (1 + 3.0·boss(j))`, argmax, ties → lowest `actor_id`; retarget every **12 ticks**; hysteresis **0.25** / cooldown **24 ticks**; pass-through lock 3.0 m; **step never clamped** — drive-through, not stop-at-target; empty board → HOLD, **no spawn-schedule read** (census K23). Speed **5.4 m/s** = `v_ref 4.0` × 1.35, and ⚑ **`v_ref` is a DECLARED-FREE-PARAMETER** — player base m/s is NAMED-ABSENT from the corpus; the I-18 locomotion fold measures **25–29 % slower** (census K24, c-5). **No facing model at all** — `heading_rad` is 0.0 on 100 % of samples and no damage predicate reads a heading (census K25). |
| **PLAY** | **Matt's hands.** GD-faithful mouse: RMB-held EoR, LMB Blitz, keys 2 / 3 / 7, **move-toward-cursor**. Desktop native build only — *WASD makes him a different pilot and T-B would then be measuring the control scheme.* |
| **Authority** | **F3** (Q81, Matt-ruled) · charter § 0. |
| **How it is tested** | ⚑ **Not testable by T-A, by construction — this is the class the two-config design exists to isolate.** The instrument instead: **the recorder emits the same five-state census and the same movement ratios for both configurations**, so the pilot's contribution appears as *a difference in the same statistic computed the same way*, never as an inference. The ORACLE side of that statistic is T-A's B-3/B-4/B-5. |
| **Expected direction on T-B** | **Unbounded, and it is the single largest uncontrolled term.** The scripted pilot drives *into* packs and never stops; Matt will kite, retreat, and stand in the banner. ⚠ `v_ref` compounds: **metres per second against an arena whose metres are uncertain by 1.64×** (DIV-09). Nothing the player touches more continuously than his own speed rests on a freer number. |
| **Handoff sentence** | *"The simulation's player drove into the biggest pack it could find and never stopped moving, and it had no idea which way it was facing. You will not play that way. Where your numbers differ from its numbers, that is usually why."* |

### DIV-06 · BOUND-SKILL ADDITIONS

| | |
|---|---|
| **ORACLE** | **Blitz is not simulated at all** — omitted because `Skill_AttackWeaponCharge` declares no range field and a layer whose `range_grade` is not MEASURED is **refused, never defaulted** (census K14). **Vire's Might** = a generic dash layer, `range_m 12.0`, cd 3.5999999 — **twelve riders unmodelled**. **Rune of Rush** = a generic dash layer, `range_m 16.0`, riders unmodelled. **War Cry** is the only bound skill with a real modelled effect (K-5, **−29 % enemy damage**, applied before absorb pools). |
| **PLAY** | built **from the pack's own geometry, where the pack carries the value**: **Blitz** `skillTargetNumber 3` / `skillTargetAngle 180°` / `characterRunSpeedModifier 300 %` / cd 3.5 · **Vire's Might** `path_radius 2.2` × `endRadiusMultiplier 1.5` / cd 3.6 · **War Cry** `skillTargetRadius 16.0` / cd 7.5 · **Rune of Rush** cd 2.5. ⚑ **Any rider the pack does not carry is `PLACEHOLDER-INERT` — named on the HUD tooltip and in the handoff, never invented (Law 3).** **All additions are OFF under `ORACLE`.** |
| **Authority** | **R-KP-0e** (charter § 2) · census (c-6) · WARN-1 discharge. *(All three geometry values verified exact against census (c-6) by jack-ryan at the Gate-1 re-check: "no invented rider — Law 3 held".)* |
| **How it is tested** | **Geometry-true probe (R2D-5)** asserts each value against the pack. **Inertness probe:** every `PLACEHOLDER-INERT` rider produces **zero damage, zero status, zero RNG draw** — asserted, not commented. **Config probe:** `config == ORACLE` ⇒ all three additions OFF, asserted at load. **HUD probe:** every inert rider has a tooltip naming it inert. |
| **Expected direction on T-B** | **Raises player throughput in PLAY relative to ORACLE by an unbounded amount** — Blitz goes from *not existing* to a 3-target 180° charge. Against the **footage**, the direction is the opposite: the riders the pack does not carry are riders the referent had, so PLAY still under-reads the video. ⚑ **The row therefore pushes the two comparisons in opposite directions and must never be quoted as a single "direction".** |
| **Handoff sentence** | *"Three of your four keys do less than they did in the video. Blitz, Vire's Might and Rune of Rush move you and hit what the data file says they hit; every extra effect they had in Grim Dawn is switched off, labelled on the tooltip, because nobody measured it and we are not going to guess."* |

### DIV-07 · VANGUARD BANNER — PLACEMENT (the modifier is **not** a divergence)

| | |
|---|---|
| **ORACLE** | `offensiveTotalDamageModifier = +100 %` — a positional **×2.0 on the player's OUTGOING damage**, evaluated from his own position **every tick, no hysteresis, no grace period**, inside an **8 m aura** (census W6, `defenses.py:334-357`). **Placement is `D-1`: DECLARED, not decoded** — no coordinate is minted; the four defences sit on the sim's own `PatrolPoint_Attack` anchors, greedy ascending radius, separation floor = the banner's own 8 m aura. ⚑ **The runner-up anchor sits 2.27 m outside the aura, which would flip a camping player from 100 % tether occupancy to 0 %.** The three beacons **do not fire** (reuse cadence UNREAD; *a defence with no measured reuse gate does not fire*), a bias **away** from reaching 160. |
| **PLAY** | **the modifier and the 8 m radius are MODEL-BOUND and identical in both configs.** What diverges is only that PLAY **draws** the aura on the plate at true radius and shows a **HUD buff icon that drops the instant you leave** — and that the **placement** is carried as the declared choice it is, with occupancy emitted against **all eleven anchor nodes**, as the sim does. |
| **Authority** | **R-KP-0f** (charter § 2: MODEL-BOUND regardless of V14's tier status; placement is `DECLARED-not-decoded` and is a register row) · census (c-10) / W6c · WARN-11. |
| **How it is tested** | **Geometry-true probe (R2D-5):** the aura at **8.0 m** asserted against the census figure (`defenses.py:10-14`) **until V14 lifts it into the pack** — ⚑ the provenance is named because § 4.4's rule says *"against pack values"* and **the Banner is in no pack member** (INFO-10). **Unit probe:** stepping from 7.9 m to 8.1 m halves outgoing damage **on the next tick**, with no hysteresis. **Occupancy emitted against all eleven anchors**, so the placement's sensitivity is measured rather than assumed. |
| **Expected direction on T-B** | ⚑ **Knife-edge, and it is the only Crucible term the player can act on.** The whole ×2.0's T-B contribution is a function of a placement nobody decoded. A 2.27 m error in one direction is the difference between a camping player at 100 % uptime and 0 %. **Any T-B damage row must carry banner-occupancy beside it or it is uninterpretable.** |
| **Handoff sentence** | *"Standing inside the banner's ring doubles your damage, instantly, with no grace period. We know the ring is 8 metres. We do not know exactly where the banner stood — and two metres either way is the difference between always-on and never-on."* |

### DIV-08 · SUMMONS — PRESENTATION

| | |
|---|---|
| **ORACLE** | they **do** deal damage (`OffenseLimb.MEASURED_BASIC`; Guardian 0.7037 s swing, phys 33 + fire 25, `skillTargetNumber 5`; Deathstalker 0.8116 s, phys 130 + poison 130) — **but they are leader-coincident, positionless and immortal**: candidate distance is measured from **the player's own `(px, py)`**, reach `MELEE_REACH_M ≡ D_ENGAGE_M = 2.4 m`, they do not move, do not pursue, and **have no HP field** (`C-B3-1` refuses to invent one; both bodies are MEASURED `invincible = True`). Basics only, **Min** rolls, DoT riders REFUSED. Summon damage does **not** feed leech. **Mana is not spent.** ⚑ **Aggro is DECODED-FALSE**: `causesAnger = False` / `angerMultiplier = 0.0` — *"the Guardians never enter the threat table, are never selected, and draw no attacks."* Seat of record `PRESENT_INERT`, which draws **zero RNG**. |
| **PLAY** | **the oracle's law is kept exactly.** The **view** draws them beside the player as a **registered presentation choice** — and **no health bar renders on any summon token; the view carries no `hp` field for them.** |
| **Authority** | **R-KP-0b** (charter § 2) · census (c-7) / W9 · **WARN-13** (the no-health-bar clause is the part that keeps the drawn summons from lying about a mechanic that is `DECODED-FALSE`). |
| **How it is tested** | **Scene probe:** *"no health bar renders on any summon token"* as a mechanical assertion (WARN-13's still-open § 4.4 item) + *"no summon token carries an independent position field; its draw position is derived from the player's"*. **Model probe:** summon damage does not enter the leech basis; summon casts draw zero RNG. |
| **Expected direction on T-B** | **None on any statistic** — the view is strictly downstream of the model. The risk is **perceptual**: a player watching two guardians soak a pack is watching a fiction, will believe they tank, and will position as though they do. That mis-belief then enters T-B through the **pilot** class, not through the model. |
| **Handoff sentence** | *"Your two guardians stand next to you because that is exactly where the simulation keeps them. They have no position of their own, they cannot die, and they do not pull a single attack off you. They are not tanking; they are hitting whatever you are hitting."* |

### DIV-09 · `u` — THE METRE SCALE

| | |
|---|---|
| **ORACLE** | **there is no metre scale to diverge from.** The sim's arena is defined in metres directly (`R_wall` derived from decoded spawn geometry); there is no minimap-pixel chain anywhere in it. |
| **PLAY** | the ring is **native minimap px** scaled by a **registered runtime choice** `u ∈ [0.22277, 0.3663]` (**R-L3-2**, a **1.64×** window). ⚑ The geometry file's own `scale` block still prints the **SUPERSEDED** `u = 0.1981` and `[0.094, 0.3663]`; **R-L3-2 governs and excludes the point estimate.** Native-px geometry is what is frozen; its metre scale is not. |
| **Authority** | **R-KP-0c** · **R-L3-2** · charter **S-7** (WARN-8) · 2D spec § 1.4. Rider routed to **galadriel** (W1). |
| **How it is tested** | **`u` is read from exactly ONE symbol** — asserted (2D spec § 3.3). **R2D-7 as re-based by Corrigendum-Forward 1 item 2:** any metre readout drawn from the ring **displays the registered `u` and its window `[0.22277, 0.3663]` beside it**, until galadriel's rider returns. **Negative assertion:** no build reads `scale.value_m_per_minimap_px` from the geometry file. |
| **Expected direction on T-B** | ⚑ **The largest unquantified term in `PLAY`.** A 1.64× window on arena size multiplies straight into **every traversal statistic** — time-to-reach-spawn, kiting room, how often the wall matters, how often a pool is crossed — and it **compounds with `v_ref`'s freedom** (DIV-05): *metres per second against an arena whose metres are uncertain by 1.64×.* **Three independent instruments now push `u` upward** (the published 0.1981 point estimate, `D-W1-1`'s 0.22277 floor, and the containment re-derivation at 2D spec OQ-3), which is a direction worth a measurement seat's attention and is not adjudicated here. |
| **Handoff sentence** | *"How big the arena is in metres is still uncertain by a factor of 1.64, and everything about how long it takes to walk anywhere inherits that. If distances feel wrong, that is the most likely reason, and it is a measurement we have not finished."* |

### DIV-10 · ZOOM / VIEW REGISTER

| | |
|---|---|
| **ORACLE** | none — headless, no pixels. |
| **PLAY** | **`ZOOM-GD` default** at `ppm = **75.668** px/m`; **`ZOOM-HOUSE` toggle** at `**160.394** px/m`. Both derived from `ppm = (fraction · 1080)/(h_fig · cos α)` at **`h_fig = 1.9 m`**, `α = 52.9535411256029°`, `cos α = 0.6024624070853052`. Zoom ratios against the 100.62 px/m plate: **0.752 / 1.594**. |
| **Authority** | **F4** (Q81, Matt-ruled: GD-matched default, house on a toggle) · **KP-0e** (`h_fig = 1.9` re-affirmed) · 2D spec **Corrigendum-Forward 1 item 1** (the superseded pair `71.885 / 152.374` was computed at `h_fig = 2.0` — Gate-1 BLOCK-A) and **Corrigendum-Forward 2** (the § 1.3 figures re-derived: EoR ring **227.0 × 181.2 px radii**, 454.0 px across, = **2.62 × figure height**; ViewDistance **6,053.5 px**; house extents **1.79× / 3.37×**). |
| **How it is tested** | **R2D-2:** `ppm` **derived, not typed** — both presets reproduce **from the formula** at build; none is copied from prose. **R2D-7:** zoom **bounded to the two presets** (a free zoom control is out of scope and would silently re-scale every T-C judgment); the camera gate `visible_rect ⊆ dressed_extent` asserted **per frame on the POST-OFFSET rect** (Camera2D applies `offset` **after** `limits` — R-C3-53, learned the expensive way). |
| **Expected direction on T-B** | ⚑ **None on any runtime statistic** — zoom is strictly downstream of the model and **no code path lets it touch a number**. But it changes **what Matt can see and therefore what he does**, so it enters T-B through the **pilot** class: at house zoom he sees roughly **half the ground**. **A session played at `ZOOM-HOUSE` is not comparable to the footage** and the recorder header's zoom field is what makes that checkable. |
| **Handoff sentence** | *"The default view matches the zoom in your video. The house zoom shows about half as much ground — it is there because you will want it, but a session played at house zoom cannot be compared to your footage, and the recorder knows which one you used."* |

### DIV-11 · PLAYER KINEMATICS AT RENDER RATE (the F1 rider)

| | |
|---|---|
| **ORACLE** | the player moves **once per sim tick** at 12.25 Hz (`tick_period_s = 0.0816326530612245`, `binding_class MODEL-BINDING`). |
| **PLAY** | **the player's own kinematics integrate at render rate and are sampled by the sim each tick.** Combat cadence stays at 12.25 Hz — the 82 ms quantisation lands on **ability resolution**, not on the feel of his own feet. |
| **Authority** | **F1** (Q81, Matt-ruled; closes Q66 and runtime-spec OQ-3). |
| **How it is tested** | **R2D-9 determinism:** re-feeding a recorded intent log at the same seed reproduces the event stream **exactly**. ⚑ **`position_correction` events are COUNTED and reported — a high count is a finding, not a pass** (2D spec § 2.5, *the F1 rider's two-authority problem*). **Bound:** the sub-tick divergence is at most one tick of travel, `5.4 ÷ 12.25 = **0.441 m**`. |
| **Expected direction on T-B** | **None on any damage statistic** — every damage predicate reads the sim's tick position. The divergence is presentational **unless** `position_correction` count is high, which means the two position authorities are fighting; that is a port finding, not a feel one. |
| **Handoff sentence** | *"Your own feet move smoothly. Everything that resolves a hit still happens 12.25 times a second, exactly as it did in the simulation."* |

### DIV-12 · ONE LIFE, RESTART KEY, SCOPE WINDOW

| | |
|---|---|
| **ORACLE** | the sim runs to `player_death` and stops. ⚑ **Every terminal in every arm is `terminal_reason: "player_death"`.** No restart, no meta. |
| **PLAY** | **waves 150–160, one life, restart key.** No loot, no levelling, no Crucible shop, no between-run meta. |
| **Authority** | **F6** (Q81, Matt-ruled: *exactly the referent's window*). |
| **How it is tested** | **Assertion on the recorder:** the restart key **re-seeds and opens a NEW telemetry file with a new `run_id`** — it never appends to an existing one. ⚑ **A restart that continues a file would silently pool two fights into one T-B statistic**, and every occupancy fraction (B-11…B-14) would be computed over a denominator spanning two deaths. **Grader assertion:** the T-B grader **refuses** to compute a statistic across more than one `run_id`. |
| **Expected direction on T-B** | **None within a session.** The hazard is **pooling across sessions**, and it is closed in the grader rather than in the player's discipline. |
| **Handoff sentence** | *"One life, waves 150 to 160, restart key. No loot, no levels, no shop — exactly the window in your video. Every restart is its own recording."* |

### DIV-13 · ⚑ ENTRY STATE — **UNRESOLVED, and not in the charter**

| | |
|---|---|
| **ORACLE** | the sealed cells are `**cp150**` checkpoints; the census's per-wave activity table runs **151–160** (census M4b) while `waves.json` carries **11 wave rows**. The oracle **resumes from a pinned fixture state** — HP 20,005, energy 2,576, reserved 982, usable ceiling 1,594 — and plays 151 onward. |
| **PLAY** | **F6 says "waves 150–160".** Whether that means *play wave 150* or *start from the 150 checkpoint* is **not stated anywhere**, and the two are different runs. If PLAY plays 150, the entry state into 151 — energy, cooldown phases, potion charge, circuit-breaker cooldowns, summon state, HP — is **pilot-determined**, and the whole 151–160 comparison inherits an uncontrolled initial condition. |
| **Authority** | **NONE YET.** Routed to the conductor, § 8 **OQ-1**. |
| **How it would be tested** | recorder header carries `entry_state_source ∈ {"cp150_fixture", "played_150"}` and the T-B grader **refuses to pool the two**. |
| **Expected direction on T-B** | ⚑ **This is precisely the cold-start confound that sibling S6 exists to measure — and S6 is pre-declared out of scope.** Direction is unbounded because energy is the binding resource (`run.py` terminates the wave loop on `energy < per_tick_cost`, outcome `"dry_out"`). |
| **Handoff sentence** | *(pending the ruling)* |

### DIV-14 · ⚑ POTION AGENCY — **UNRESOLVED, and not in the charter**

| | |
|---|---|
| **ORACLE** | the sim **does** model a potion: `defaulthealthpotion.dbr` + HoT — **800 flat + 25 % instant + 25 % HoT, cd 12.0 s, 1 charge**, fired by the policy at threshold **θ = `I4_EXCURSION_MAX` = 0.49** — ⚑ **the MEASURED-FALSIFIED limb, failing 5 of its own 9 predicted actuations**, kept only for byte-identity of the fold-off arm (census K11, c-4). The potion is `RequestUseItem`, **decoded PERMITTED in every control state** (census K26). |
| **PLAY** | ⚑ **undefined.** The F3 input table binds RMB, LMB, keys 2 / 3 / 7 and movement — **there is no potion key.** So either the potion auto-fires at the oracle's θ (and Matt cannot drink when he wants to), or it is silently absent (a removal of 800 + 25 % + 25 % HoT with a 12 s cooldown). **Neither is written down.** |
| **Authority** | **NONE YET.** Routed to the conductor, § 8 **OQ-2**. |
| **How it would be tested** | unit probe on the potion's magnitude/cooldown/charge against the census values; recorder emits `potion_use` with `trigger ∈ {"auto_theta","player_input"}`. |
| **Expected direction on T-B** | **Lands squarely on the HP trace — the richest T-B family there is (B-11…B-18).** A human drinking at his own threshold moves *time at full health* (referent **42.84 %**), *time below 50 %* (**3.46 %**) and *HP min* (**5,360 of 20,005**) all at once, and these are the rows that would otherwise catch a sustain model that is wrong. |
| **Handoff sentence** | *(pending the ruling)* |

---

## § 3 · NON-DIVERGENCES CARRIED WITH A NAMED CONFOUND

*These are identical in both configurations. They are in the register because **a difference the register does not explain is a defect in the register** — and each of these will produce a visible T-B difference against the footage that is not a port error, not a declared divergence, and not the pilot.*

**ND-01 · Fire-time damage resolution.** Both configs resolve at the **cast tick**; **there is no arrival hit-test** (`deferred_arrival.py:13-17`; the arrival block subtracts HP **unconditionally**). Magnitude, to-hit, crit tier, resist, armour and separation are all fixed at the cast tick against where the player stood **then**. **Confound:** a human who strafes takes the hit anyway, and *the most basic ARPG instinct silently fails*. ⚑ The sim **measured what the fix would cost and declined to spend it** — arrival separation differs from cast separation by a **median −0.26 m on an 8.8 m median** — but **that instrument measured a POLICY, not a CAPABILITY**, and quoting it as *"dodging barely matters"* reads a pilot's habits as a law of the world. Authority **R-KP-0a**, L4 Matt-accepted. Closure: sibling **S1**, out of scope. Mitigating fact for the feel: the referent sat at **full health 42.84 %** of the fight; he was not dodging for a living.
> *Handoff:* **"Projectiles you side-step will still hit you.** The simulation decided every hit the moment the monster swung, against where you were standing then — and we kept that, because changing it would make every number in the comparison unattributable."

**ND-02 · No player crit.** `CritLimb` default `LO` = ×1.0; **every player damage row hardcodes `is_crit=False`**; the volley crit override is structurally disabled whenever a measured board is present. `ABS-CRIT-ROLL-RULE` is `blocks_playability` and the pack's own instruction is **"DO NOT build a flat ×1.5"**. **Confound:** the referent's warlord crit; PLAY therefore **under-reads player DPS against the footage by an unmeasured amount**, and every time-to-kill row inherits it. Graded as T-A **E-9**.
> *Handoff:* **"You never crit.** The Grim Dawn warlord did. Nobody has decoded the rule and inventing one would make every damage comparison meaningless, so this build hits for the average every time."

**ND-03 · Base cooldowns; CDR not recovered.** Cooldown sweeps run from **base** values with the CDR absence **declared** (R-L91-7(a)). Measured deltas are small — Blitz **+0.10 s**, Ascension **+0.4 s** — but the direction is systematic. **T-C's *time-to-kill* axis pre-declares this direction** (*"base cooldowns → systematically slow pilot"*), which is what makes that verdict informative rather than a shrug.

**ND-04 · ⚑ THREE known-bad live limbs — not two.** `WarCryLimb.I8_LEGACY`: War Cry's duration is the **retired invented literal 5.0**, which **priced 19.43 % of all incoming damage**. `PotionLimb.I4_EXCURSION_MAX`: θ = 0.49, **measured-falsified on 5 of its own 9 predicted actuations**. `LifeMonitorLimb.POLL_AT_SLOT`: the circuit breakers poll a **post-lift** HP value and measurably miss floor ticks — **Turtle 51 vs 41 seen, Menhir 13 vs 10**, and *in waves 151/153 the censored tick was the only sub-threshold tick, so the breaker was off entirely there*. They are the defaults **for byte-identity of the fold-off arms** — correct for T-A, **wrong for anything a human is asked to judge**. Closure: sibling **S6**, out of scope.
> ⚑ **Charter L4 reads *"two oracle limbs are known-bad"*. The census names three** (c-4). Recorded as a finding (§ 7); the charter is not this document's to edit.
> *Handoff:* **"Three of the simulation's settings are known to be wrong and were kept anyway,** because changing them would break the like-for-like comparison: War Cry's duration is a made-up number that was later retired, the health-potion trigger is measurably wrong, and the two emergency heals fire slightly late. **Do not quote a feel session as a fidelity result.**"

**ND-05 · `health_max` constancy (`D-Q1`, B-18).** Both configs hold **20,005** throughout. The referent's `health_max` **dropped 18.18 % for 8.283 s**, and the sim models it as constant. **Pre-registered as a KNOWN MODEL GAP, not a build defect** (2D spec § 6.3 B-18). This is why the view wire carries `hp` **and** `hp_max`, not `hp_frac` — a fraction-only wire cannot express it and a T-B HP comparison would silently compare two different quantities.

**ND-06 · Spawn scatter law — the pack steers the builder wrong.** Both configs run the oracle's **`POLAR_UNIFORM_RHO`**: `θ = 2π·u₁`, `ρ = 8.0·u₂`, **uniform in radius, not in area** (`Engine.dll 0x100edf30`; driver of record). ⚑ **The pack's `DS-SPAWN-SCATTER` row says `uniform-box-per-axis` and warns emphatically against the disc** — *"NOT A DISC. The box corner sits 1.414 × h from the anchor; a loader drawing an h-radius circle rejects bodies the sim placed correctly."* **The oracle draws the disc.** A builder who follows the pack implements the **superseded incumbent** and monsters appear in the corners of a square the model does not have. **Falsified by T-A E-7a/E-7b**: `R_wall = 35.758085 + 8.0 = 43.758085` is exactly the disc law's supremum, while the box reaches `35.758085 + 8.0·√2 = 47.072` m — **above the wall with certainty**. V11b fixes the row.
> ⚑ Compounding: **`PLACEMENT_EXTENTS_M = 8.0` now carries three meanings** — square half-width (incumbent), max disc radius (I-26's semantic shift), and hazard-field radius (W1's second shift). One constant, three readings, **and both wrong picks surface as level-design mistakes rather than model mistakes.**

**ND-07 · `hit_test_model` — the second pack trap.** `player_kit.channel.hit_test_model = **"point"**`. Both configs run the sim's law: a **true uniform disc of radius 3.0 m re-centred on the player every tick**, counting every body inside it — **no angular gate, no corridor, no to-hit roll, no target cap** (MEASURED-ABSENT 4/4). *"A builder implementing a point test against a 3.0 m radius builds a different weapon"* (census D8, flagged-not-adjudicated). ⚑ **There is no T-A row for this** (prereg § 6, C-7); it is caught only by the R2D-5 geometry-true probe and by the coverage table. V17 fixes the row.

**ND-08 · Monster-side mitigation — ⚑ PENDING-W1, the one row that will move the hash.** `monsters.mitigation_note` (provenance `PRV-BATON-V1`) says `NONE-MODELLED … BY CONSTRUCTION` and warns that adding a term **double-counts against eHP that already carries the armour/resist chain**. The PM4-lineage sim **does** apply it per body (`after_armor(raw, armor, absorption) × (1 − res_physical) × crit_mult`). **Not adjudicated by the conductor (R-KP-0d)**: gamora runs her named one-record refuting test as the **first act of W1** — one tier-16 record at one wave, `player_damage_per_tick` against `monsters.blocks` eHP with and without `applied_damage`, compared to the sealed cell's own per-body kill times. **One record, no sim run.** **V6 is written to its answer.** Until then this row carries **both candidate values named**, and **the register hash changes when it resolves** (§ 6).

---

## § 4 · WHAT IS **NOT** A REGISTER ROW

A thing **neither** configuration has is out of scope, not a divergence. Named here so the boundary is checkable:

- **The 43-state AI controller graph** — *the oracle never ran it*; lifting it would make the port **less** comparable, not more. The sim has a view-distance gate, a halt radius and a swing clock.
- **Loot / levelling / meta / Crucible shop** — F6, Matt-ruled out.
- **Web / phone delivery** — F3/Q81-F3, Matt-ruled out.
- **Pets** — Matt-ruled `L-83 D-3` (*"I did not have a pet"*), PARKED.
- **Celestial blessings** — a **measured zero, both sittings**; the four Lap-C blessing rows are a counterfactual the module **refuses** to read (*"would model a run Matt did not play"*). Not a switch; an absence with a measurement behind it.
- **The three Crucible beacons' output** — they **do not fire** in either config (cadence UNREAD; *a defence with no measured reuse gate does not fire*). Signed bias named: it under-reads ally help, biasing **away** from reaching 160. One read of `skillCooldownTime` on three `turret*.dbr` records would close it.

---

## § 5 · THE FIVE ATTRIBUTION CLASSES FOR A T-B MISS, AND THE DECISION PROCEDURE

### 5.1 The five classes

⚑ **This unfuses the charter § 2 pair `placeholder/instrument`, discharging jack-ryan's WARN-2 PARTIAL** — *"they have different remedies (re-author an asset vs re-compute a denominator)"*. The resolution is **not** to add a sixth class: **`placeholder` is a SUBCLASS of `declared divergence`**, because in this build every placeholder has a register row by construction (R-KP-0e: *"named on the HUD tooltip and in the handoff, never invented"*). `instrument` takes the free slot.

| # | class | what it means | remedy |
|---|---|---|---|
| **1** | **PORT** | the GDScript derives a different fight from the same rules | fix the runtime. **Bounded — not eliminated — by T-A**, to the resolution the prereg's § 6 ceilings state |
| **2** | **DECLARED DIVERGENCE** | a `DIV-nn` row. **Includes PLACEHOLDER-INERT riders** (a placeholder is a declared divergence whose PLAY value is *inert*, DIV-06) | either accept it and quote the row, or build the missing rider — a **design** decision, never a bug |
| **3** | **MODEL GAP** | the sim and Grim Dawn differ. The `ND` confounds; `health_max` (ND-05); no player crit (ND-02); base cooldowns (ND-03); the three known-bad limbs (ND-04) | a research finding for a later lap; **never** closed by tuning the twin |
| **4** | **PILOT** | Matt's hands vs `DRIVE_TO_PACK` — **including everything downstream of what he can see (DIV-10) and what he chooses (DIV-14)** | not a defect. Re-run under the scripted pilot to measure it |
| **5** | **INSTRUMENT** | the recorder and the footage instrument computed the **same-named statistic on a different denominator or window** | **re-compute one side on the other's construction.** The census names this the **likeliest non-reason failure** |

### 5.2 The decision procedure — ordered, mechanical, cheapest-falsifier-first

> **Run the steps in order and stop at the first hit. Each step is a test that can be run, not a judgment that can be made.**

**Step 0 — INSTRUMENT first, because it is the cheapest and the likeliest.**
Does the T-B row's denominator and window match the footage instrument's, **as the row's own definition states** (2D spec § 6.3: *every T-B row carries the denominator and window as the footage instrument defines them*)? If not → **INSTRUMENT**.
*Test:* recompute the twin side on the footage instrument's construction. **If the miss closes, INSTRUMENT is confirmed.** *(B-8 is the founding case: `frac_moving` reads 0.883 / 0.705 / 0.6265 across three instruments — a **1.41×** spread — so an absolute movement figure in a green report is a defect in the report.)*

**Step 1 — DECLARED DIVERGENCE.**
Is there a `DIV-nn` row whose **pre-registered expected direction matches the sign of the miss**? If yes → **DECLARED DIVERGENCE**, provisionally.
*Test:* **re-run the same fight under `ORACLE`** — the divergence's OFF state — and check the miss closes. ⚑ **This test is buildable because there is ONE runtime with two configurations. That is what the two-config design bought, and it is the only reason step 2 works.**

**Step 2 — PORT vs MODEL GAP. This is the decisive fork, and it is exactly what T-A is for.**
Does the miss **survive under `ORACLE` with the scripted pilot**? If yes, neither the pilot nor a divergence can explain it. Then:
- **T-A has a graded row covering this statistic and that row is RED → `PORT`.**
- **T-A has a graded row covering this statistic and that row is GREEN → `MODEL GAP`** — the port faithfully reproduces the sim, and the sim differs from the footage.
- **T-A has no row covering this statistic → UNATTRIBUTABLE-PENDING**, and the disposition is to name the missing row as a finding for the next lap. *It is not assigned to PORT by default.*
> ⚑ **The single most useful sentence in this register: a green T-A row plus a miss that survives under `ORACLE` is a MODEL GAP, not a port bug.** That inference is the whole return on building T-A, and it is available on the day T-A goes green.

**Step 3 — PILOT.**
Does the miss appear **only** with Matt at the controls and vanish under the scripted pilot **in the same configuration**? → **PILOT**.

**Step 4 — none of the above.**
→ **a defect in this register** (charter § 2, verbatim). Disposition: **file a new `DIV` or `ND` row, re-hash (§ 6), and record why it was missed.** A T-B miss in no class is never reported as a mystery and never reported as fidelity.

**Tie-break rule.** Where two classes are both consistent with the evidence: **assign the one whose OFF-state test is cheapest to run, run it, and record the result.** Never assign by narrative plausibility — that is how a port bug becomes a "model gap" and stops being fixed.

---

## § 6 · THE REGISTER HASH

**Purpose.** Every telemetry file's header carries `divergence_register_sha256`. A recording whose header hash does not match the register in force at grading time **is not comparable, and the grader says so** — the same shape as 2D spec § 6.1's *"a run without a header is not comparable and the harness rejects it."*

**What is hashed: the MACHINE FORM, not this markdown.** This document carries prose that will be improved without any switch changing; hashing the prose would make every clarification a new incomparable epoch. So:

1. **The runtime EMITS the machine form from its own configuration tables** — mechanical, per #72. **This document is the labelled expectation, checked against the emitted form, never substituted for it** (twin-test § 2.3 clause 1). **A mismatch between the emitted form and this document is a COVERAGE FAIL**, surfaced at the prereg's precondition **P-1**.
2. **The machine form is a JSON array of row objects**, one per `DIV`/`ND` row:
   `{"id","class","switch","oracle","play","authority","test","direction","status"}`
   — `class ∈ {"DIVERGENCE","NON-DIVERGENCE"}`, `status ∈ {"ACTIVE","UNRESOLVED","CARRIED","PENDING-W1","RESOLVED"}`.
3. **Canonical serialisation:**
   - rows sorted by `id`, ascending ASCII;
   - object keys sorted ascending within each row;
   - UTF-8, **NFC-normalised**; each value's internal whitespace collapsed to single spaces, leading/trailing stripped;
   - JSON with **no insignificant whitespace** (separators `","` and `":"`);
   - **no trailing newline.**
4. `register_sha256 = sha256(canonical_bytes)`, **full 64 hex in the header; 12-char prefix in prose.**
5. ⚑ **DERIVED AT USE, NEVER RETYPED.** *(WARN-10 is this project's founding breach of exactly this rule, committed in the act of stating it.)*
6. **Any row's `status` change re-hashes the register.** **ND-08 is the known pending mover** (gamora's (c-2) refuting test, first act of W1). A run recorded under the pre-resolution hash and graded after it is **not silently pooled**: the grader reports the two epochs separately, or refuses.

---

## § 7 · WHAT THE CHARTER MISSED — found by writing this register

*The point of the exercise, per the brief. Three items; none is a design objection.*

1. **DIV-13 — the entry state is undefined.** F6 scopes PLAY to *"waves 150–160"*; the oracle's arms are `cp150` checkpoints resuming at 151. **Whether PLAY plays wave 150 or resumes the checkpoint's fixture state is written down nowhere**, and the two produce different entry conditions into wave 151 (energy, cooldown phase, potion charge, breaker cooldowns). ⚑ That is **precisely the cold-start confound sibling S6 exists to measure — and S6 is pre-declared out of scope**, so the run would be carrying the confound with no instrument for it.
2. **DIV-14 — the potion has a model and no key.** The sim models a potion (800 flat + 25 % instant + 25 % HoT, cd 12.0 s, 1 charge) fired at a **measured-falsified** threshold. **F3's input table binds no potion key.** So PLAY either auto-fires at a falsified θ or silently drops a sustain term — **and neither is declared**. It lands on the HP trace, which is the richest T-B family (B-11…B-18) and the one with the most published reference values.
3. **ND-04 — charter L4 undercounts the known-bad limbs: it says two, the census names three** (War Cry `I8_LEGACY` · Potion `I4_EXCURSION_MAX` · LifeMonitor `POLL_AT_SLOT`). **Two of the three are ones a human will feel.** Disclosing two of three is the shape of disclosure that gets discovered at the controls.

*(A fourth, filed in the prereg rather than here because it is a grading defect: the oracle's per-salt uptime and release-duty ranges are **not complements** while the pooled pair sums to exactly 1 — see prereg § 3.3, B-7, with the one-read refuting test.)*

---

## § 8 · OPEN QUESTIONS TO THE CONDUCTOR — one recommendation each, stated first

**OQ-1 · DIV-13, the entry state.**
**Recommendation: PLAY resumes the `cp150` fixture state and opens at wave 151 — wave 150 is NOT played.** Otherwise the first graded wave's entry conditions are pilot-determined and the entire 151–160 comparison inherits an uncontrolled initial condition that **S6 was the instrument for, and S6 is out of scope**. If Matt wants to play 150 as a warm-up, it ships as a **labelled pre-roll excluded from every statistic**, with the recorder emitting `entry_state_source` so the two can never pool.

**OQ-2 · DIV-14, the potion.**
**Recommendation: PLAY binds the potion to key `1` and auto-fire is OFF; `ORACLE` keeps auto-fire at the oracle's θ = 0.49.** It becomes a clean `DIV` row with an obvious test, it matches *"I want to play the game"*, and it removes a **measured-falsified** threshold from the one configuration a human is asked to judge. The cost — a hand-driven potion adds a pilot term to the HP trace — is **declared, bounded by a 12 s cooldown and a single charge, and attributable via step 3 of § 5.2**. The alternative (auto-fire in both) keeps T-B cleaner and gives Matt a build that drinks for him at a threshold we know is wrong; that is the worse trade for a build whose purpose is for him to play it.

**OQ-3 · Charter § 2's attribution list still reads `placeholder/instrument` fused.**
**Recommendation: adopt this register's five classes verbatim at the next charter touch** — `placeholder` folded **into** declared divergence (it has a `DIV` row by construction), `instrument` given its own slot. This discharges WARN-2's PARTIAL without adding a sixth class, and it preserves jack-ryan's point that the two have different remedies.

**OQ-4 · WARN-13's last open item is a scene assertion, not a handoff page.**
**Recommendation: add *"no health bar renders on any summon token"* to the § 4.4 probe list now, while the scene is unbuilt.** L4 already carries the disclosure and the re-check marked it PARTIAL for exactly this reason — *declared but not probed*. It costs one assertion and it closes DIV-08's only failure mode.

**OQ-5 · ND-08 will move the register hash mid-run.**
**Recommendation: pre-declare the two-epoch rule now — recordings made under the pre-resolution hash are reported separately and never pooled**, and the W1 seal records the hash before and after. The alternative (delaying every recording until (c-2) resolves) stalls the feel sessions F7 explicitly licenses.

---

*Filed 2026-09-20 by gandalf (named sub-agent, `SPEC-AUTHOR`), **Wave 1 of Run KC2-PLAY**. **Law 3 held:** every value above is quoted with its source or derived in the open; nothing is invented, and every rider the pack does not carry is marked `PLACEHOLDER-INERT` rather than filled. **GL-12 held:** absences are declared, including the two the charter had not declared (DIV-13, DIV-14). **K-7 held:** no sealed cell was opened or re-run. No production code, no dispatch, no push.*
