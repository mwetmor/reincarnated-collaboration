# KC2-PLAY — ARCHITECT pass: from the EoR-warlord mechanistic twin to a playable Astra 2D scene

> **STATUS:** CURRENT — open-questions gate **DRAINED 2026-09-20** (Q81 F1–F7 ruled as recommended); P0 audits fired; charter follows their return. **Author:** gandalf (`ARCHITECT`; SCENEWRIGHT + SPEC-AUTHOR lenses), 2026-09-20. **Trigger:** Matt — *"make that a fully playable sim that we can build out in an Astra 2D scene … I want to play the game and compare how accurately we can get it to my video."*
> **Authority:** recommendation + gate only. No code, no dispatch fired. Forks are Matt's (Q81).
> **Companion docs:** runtime spec SKIRT `2026-08-25-kc2-mc-w4-godot-runtime-spec.md` · twin-test F-5 `2026-08-25-kc2-mc-w4-twin-test-spec.md` · LIFT charter/ledger `2026-08-25-kc2-lift-run-charter.md` · post-close handoff `2026-09-07-kc2-lift-postclose-session-handoff.md` · burst lane `astra_test_01/burst/HOWTO.md` · C-7 account `2026-09-17-c7-account.md`.

---

## 1 · What IS (survey — verified on disk this session)

**The run.** The most recent autonomous run on the EoR-warlord data is the **KC2 LIFT RUN** (Crucible waves 150–160, seed family `E-s09-cp150`), **CLOSED at L-19, 2026-08-26**, Gate-2 PASS-with-WARN. Lineage: KC2-SIM → PM1–PM4 → KC2-MC (behavioural twin, baton-v2) → KC2-LIFT (mechanistic twin, **baton-v3.1**). Engine HEAD then `9fd60cee`; nothing KC2 has moved since (engine log since = two decisions-log entries + a gitignore).

**The artifact.** `reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p1-20260826_031143/` — 12 members, ~22 MB: `player_kit` (EoR channel, bindings, `interrupts_channel` rows, 7 devotion procs, sustain breakers) · `math_rules` (72 KB; **test vectors normative**) · `monsters` (31,601 stat rows) · `controllers` (8,162 params) · `waves` (11 waves × 8 spawn points, 576 pool weights) · `summons` · `target_selection` · `arena` (video-measured ring + hazard zones; containment AUTHORED-WALLS) · `ai_states` · `rng_contract` · `provenance` (absence registry).

**The pack's own playability verdict:** *NOT playability-complete — eight rows over five holes*:

| Hole | State in pack | Bites a human-played build? |
|---|---|---|
| `ABS-TARGET-SELECTION` | pilot policy undecodable; paired rows | **No — dissolves.** A human at the controls *is* the target-selection policy. Survives only in the scripted pilot used for the port-fidelity test. |
| `ABS-AI-STATE-KEYSPACE` / `-TRANSITIONS` | 5 of 43 controller states in pack, **zero transition edges** | **Yes — the largest hole.** Monsters need a behaviour loop. The Python sim has a working *behavioural* one (pursuit → engage → volley → re-engage; `kc2/pursuit.py`, `engagement.py`, `discrete_volley.py`, `reengagement.py`, `threat.py`) that is not the 43-state decode. |
| `ABS-B3-STAT-DIMENSIONS` | OA/DA, defence, skills, specials for the tier-16 pool absent | Yes — but the sim resolves intake at an effective layer (`intake.py`, PM4 I-23). Whether that law is *in the pack* is unverified (§ 3 P0-a). |
| `ABS-DEVOTION-PROC-ICD` | no ICDs for the seven procs | Yes — runtime choice. |
| `ABS-CRIT-ROLL-RULE` | PTH threshold → multiplier unruled | Yes — runtime choice (`CM-BOARD-PTH.value`; never the `REFUTED_*` rows; no flat ×1.5). |

**The sim is not steppable.** `kc2/run.py::simulate_wave` is one ~4,400-line batch function (lines 353–4794). There is no seam to attach live input to. "Make the sim playable" therefore means **a GDScript re-implementation against the pack** — which is exactly what SKIRT specifies (R-1…R-9) — with the Python sim kept as the *oracle* the port is graded against.

**No runtime exists.** `reincarnated-godot/scripts/kc2_baton.gd` is the **v1 recording consumer** (3D; *"computes no damage, resolves no hit"*). SKIRT was written for a 3D drax build that never fired; **3D scenes were retired 2026-09-15** (engine decisions-log `20e778a8`). SKIRT §§ 1–6, 8–9 are render-agnostic and stand; **§ 7's SKIRT dress-plane / fog / `camera_ground_gate` and twin-test § 6.1 (F-5 camera ratification) are 3D-shaped and need a 2D re-target.**

**Open rulings inherited.** **Q66** (tick binding-class) — still unruled; it gated "only drax's runtime cadence," which is now the thing being built. **G-1** pool DoT: D-LIFT-1 (⅙ max pool per tick, defences ignored) + D-LIFT-2 (~1 s ticks, death ≈ 6 s) are MATT-RULED — at the runtime layer this is directly buildable, no fork. **R-L68-2** metre-scale pin (arena ring is `DERIVED-WEAK`, u = 0.198 m/px, band 1.7×): landing status unverified this session.

**The Astra 2D side** (`astra_test_01/burst/runs/C-7/cliffside_v45`, Godot 4.6, live on web13): `keeper.gd` (402 lines) — 8-direction authored cells, idle/walk/run/jump/cast, WASD + mouse/E cast, Godot floor collision; 19 VFX kits over four grammars (G1 projectile · G2 field/flipbook · G3 · G4), capsule colliders, seven static training dummies + hounds with hit responses, event-trace probes, MP4 capture chain, drax web deploy. Characters: **Keeper 40/40 cells** (camera flaw, Q80) · **Necromancer 25/40** (S/SW/E + mirrors; no north-facing). **What it does not have:** moving enemies, enemy actors of any kind, HP/energy, damage resolution, a HUD, a channel/held-skill state, hit-react or death cells, an arena plate, mouse-to-move.

**⚑ The referent video is no longer on this machine.** `~/gd-scratch/eor-test-2/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` (457 MB, sha256 `4c60960d…`) was flagged **KEEP-PROTECTED sole reachable copy** on 2026-09-10 (disk-reclaim ledger). `gd-scratch` was deleted under the Matt-agreed delete list on 2026-09-17 (C-5 ledger ruling, ~line 18336). Spotlight and a home-dir search find nothing; no external volume is mounted. The *measurements* taken from it are committed (galadriel KC2 laps), so instrument comparison survives; **side-by-side viewing and any re-measurement do not, until the file is re-supplied** (→ `matt_to_do` T30).

---

## 2 · The design of the thing (what "playable + comparable" requires)

### 2.1 The hinge: sim-space is metres on a plane; the screen is a projection
The cliffside resolves movement with Godot physics in pixels. **The Crucible scene must not.** Every position, radius, range and hit-test lives in model metres on the arena plane; the painted-2D view is an affine projection (x → x·ppm; y → y·ppm·sin 53°, y-sorted). `keeper.gd` contributes its **cell system and sockets**, not its controller. A build that lets a pixel capsule decide whether EoR's 3.0 m radius touched a body has replaced the model with the art. This is the same split v1 held (`apply_tick(tick_f)` — a pure function of the tick) and it is what makes two parallel build seats possible.

### 2.2 The view contract (author first — it is what unblocks parallelism)
Runtime → view, per sim tick: world snapshot (actor id, kind, xy, facing, hp frac, state) + event stream (`spawn · cast_start · channel_on/off(cause) · hit(src,dst,amount,type,crit) · dot_tick · control_applied/expired · proc(id) · summon · death · wave_flip · pool_tick · player_death`). View → runtime, per render frame: input intents (move target, channel held, skill pressed + aim point). The **same event stream is the telemetry recorder** (§ 2.6) — one emitter, two consumers, so the comparison instrument can never drift from what was on screen.

### 2.3 Placeholders must be geometry-true
Matt has licensed placeholder monster animation and placeholder VFX. The discipline that keeps placeholders from corrupting the comparison: **art may be fake; space and time may not.** EoR's ring draws at the model's radius (projected ellipse) for exactly the channel's active ticks; a projectile travels at the pack's speed for the pack's flight time (the referent's 1.6166 s dwell *was* projectile flight); a ground effect draws its true radius for its true duration; a pool is its measured circle (radius = upper bound, labelled). Monster "animation" = a tinted silhouette token sized by size-class, with three procedural states (move bob · attack lunge + flash on the volley tick · death fade) — tweens, zero image generation. Hero/nemesis bodies larger with a nameplate. Each of the seven devotion procs gets a distinct coloured burst **with a floating label** — in a comparison build, seeing *which* proc fired is worth more than beauty. Reuse the four VFX grammars with stub art; no new kit minting is on the critical path.

### 2.4 The player body
A spinning melee channel has no cell set. Placeholder answer: **walk/run cells play under the EoR ring VFX while the channel is held** (the channel survives movement — MD-B4app-2 — so walk-while-spinning is model-true); cast one-shot for Blitz / Vire's Might / War Cry; hit-react = a flash; death = fade. No Grok spend.

### 2.5 Input is part of the referent
The D-CP2-2 mechanism rule's *referent explanation* is a keybind fact: **RMB held = EoR, LMB = Blitz, 2 = Vire's Might, 3 = War Cry, 7 = Rune of Rush**, move-toward-cursor. If Matt plays the twin on WASD he is a different pilot, and T-B (below) measures the control scheme instead of the model. GD-faithful mouse scheme → desktop build; this scene is not a phone playtest.

### 2.6 The comparison — three tiers, in this order
- **T-A · port fidelity (machine).** GDScript runtime + a scripted pilot (port of PM1 movement + the sealed channel policy) vs the Python sim's pre-registered bands: terminal wave (sim 153.2, σ 2.32), per-wave clear time, intake, channel uptime, DPS. This is twin-test F-5, already specified. **Without it every later difference is unattributable** — port bug, model gap, or play variance all look the same.
- **T-B · referent fidelity (instrumented).** Matt plays N runs; the recorder computes *the same statistics galadriel measured from the footage*: channel uptime **0.838**, release duty **≈10.5 %**, cast rate **0.290 /s**, Type-A onset lag **1.60 s** / duration **1.03 s**, Type-B duration **0.60 s**, per-skill interrupt attribution, movement as **ratios** (instrument hygiene § 8), per-wave durations off the wave flips, HP and energy traces, terminal wave (referent **160**). Reported with the footage instruments' own uncertainty; ratios where instruments disagree.
- **T-C · felt fidelity (Matt's eye).** Side-by-side, synced at wave flips, verdict per named axis: density on screen · threat pressure · time-to-kill · move speed · EoR reach · sustain. Needs the video back.

**The metric I would put first, journey-shaper voice:** the EoR warlord's feel is not DPS — it is *living on leech inside the pack*: the HP globe saw-toothing at a characteristic rate while you hold RMB and wade. D2's Whirlwind barb had the same signature (leech-per-hit against incoming, and you feel the moment it inverts). If the twin's HP trace does not saw-tooth with the video's period and depth, the aggregate bands can all pass and it will still feel like a different game. **HP-trace shape (period, depth, time-below-50 %) is a first-class T-B metric, not a footnote.**

**And the honest prior:** the sealed sim ends at **153**, the referent at **160**, with the gap's candidates named and unadjudicated (Type-B phase · target selection · defensive weave). Two of those three are *pilot* deficits. A human pilot is therefore the first real experiment on that residual: if Matt reaches 160 in the twin, the gap was the pilot; if he dies near 153, it is the world. Either outcome is a finding. A runtime that lands short with a scripted pilot is **correct, not defective** (SKIRT § 4.2).

### 2.7 Known comparison confounds (name now, not after)
(i) **Dodgeability** — a human strafes what the pilot could not; whether the sim's deferred-arrival law hit-tests at arrival or resolves at fire time is unverified (P0-a). (ii) **Zoom** — house register is a 14–17 % figure; GD's measured register is ~8 % (D3, 8.02 %): at house zoom Matt sees roughly half the ground he saw in GD, which changes threat reading. (iii) **CDR/gear not recovered** — cooldowns are base; measured deltas are small (Blitz +0.10 s, Ascension +0.4 s) but it is declared. (iv) **Metre scale** 1.7× band until R-L68-2 is confirmed landed. (v) **Tick quantisation** — see F1.

---

## 3 · Work breakdown (seams execute; conductor writes no code)

**P0 — audits, parallel, read-only, cheap. Nothing else is safe to size before these return.**
| # | Piece | Seat |
|---|---|---|
| P0-a | **Pack→runtime traceability census.** For every behaviour the runtime must perform (monster loop, intake, sustain/leech/potions, projectile arrival, wave advance, Crucible buffs, summon AI, proc triggers): *pack row* / *Python module:line only* / *absent_ref*. Anything that lives only in `kc2/*.py` is either lifted into a **v3.2 pack delta** (star-lord cut, gamora rows) or registered as a runtime choice **:= the sim's choice**. Answers confound (i). | gamora |
| P0-b | SKIRT + F-5 **2D re-target delta** (§ 7 presentation layer, § 6.1 camera gate → Camera2D/zoom gate; add § 2.1 projection law, § 2.2 view contract, § 2.3 geometry-true clause). | gandalf sub-agent (SPEC-AUTHOR) |
| P0-c | Astra scene capability census: what `keeper.gd`, the cell importer, the kit exporter and PACK already give; what the exporter must learn (actor tokens, HUD, arena plate, mouse input). | drax |
| P0-d | R-L68-2 scale-pin status; arena geometry JSON reachable + sha. | conductor (recon) |

**P1 — the runtime core, headless, no pixels.** Loader + two-level digest gates (R-1) · rule census + absence/runtime-choice ledger (R-2, R-8) · fixed tick + own RNG at declared draw sites · `math_rules` with **all test vectors reproduced** (R-5) · player kit, channel model, `interrupts_channel` flags, both DO-NOTs mechanically enforced (R-3, R-4) · monsters from stat rows + the behaviour loop · waves/pools/spawn points · DoT timelines (same-source MAX, distinct-source ADD) · **control concurrency law** (overlapping controls burn each other's wall-clock — queue/refresh semantics would be wrong) · summons on the monster actor template (R-6) · devotion procs · crit · authored walls + pool DoT per D-LIFT-1/2 (R-7) · view-contract emitter · scripted pilot → **T-A**. jack-ryan Gate-2 on T-A. *This is the bulk of the labour and none of it needs the scene.*

**P2 — the scene, parallel with P1 behind the view contract (driven by a canned event stream until P1 lands).** Arena plate placeholder (ring walls + 4 obstructions from the video-measured geometry; the three phantom pillars asserted absent; the two never-walked north arcs flagged not smoothed; 6 pools) · projection + y-sort + Camera2D with a zoom gate · player view on existing cells · monster/summon tokens · geometry-true placeholder VFX set on the four grammars · HUD (HP, energy, wave badge, skill bar with cooldown sweep, buff row, damage numbers toggle) · GD-faithful input · telemetry recorder + MP4 capture harness (already exists in the lane) · restart key.

**P3 — integration, HITL.** Feel round with Matt (pre-T-A play is fine for *feel*; nothing is quoted as a fidelity figure until T-A is green) → T-B sessions → T-C once the video is back → findings harvest: every T-B miss classified *port* / *model* / *placeholder* / *pilot*.

**Run shape.** Fits the desirable-run pattern (bounded substrate: pack + SKIRT R-1…R-9 + the P2 list; decidable: vectors, bands, headless proofs; forks drainable below; authority resident). Proposed: **Run KC2-PLAY**, gandalf `RUN-CONDUCTOR`, chartered after Q81 is ruled and P0 returns; jack-ryan Gate-1 on the charter. Concurrency: C-6/C-7 hold the Astra heavy lock and the freeze — KC2-PLAY's scene work queues behind it or takes its own project directory outside the cliffside freeze.

---

## 4 · Open-questions gate

**RESOLVED (no ask):** walls + pools both layers (D-CP2-1) · pool DoT magnitude + cadence (D-LIFT-1/2) · per-skill interrupt flag (D-CP2-2) · bands-not-tape (R-L91-4) · no energy-gated release, no release-on-every-cast · hazard radii as labelled upper bounds · base cooldowns + declared absence (R-L91-7) · pets parked.

**Conductor law, veto-open:** *wherever the sealed sim made a choice the pack does not carry, the runtime's registered choice is the sim's choice* — so T-A compares like with like. Divergences from it (e.g. real dodgeability) are deliberate, listed, and excluded from T-A by running the pilot with them off.

**GATED + TRACKED:** dodgeability semantics ← P0-a · v3.2 pack delta scope ← P0-a · exporter work ← P0-c · any metre figure on screen ← R-L68-2 confirmed · T-C ← video re-supplied (T30) · any quoted fidelity number ← T-A green.

**~~OPEN → Matt (Q81)~~ ✓ ALL SEVEN RULED AS RECOMMENDED, 2026-09-20 (Matt verbatim: *"Agreed - accept all"*). The table below is now the ruling of record; F1 closes Q66 and runtime-spec OQ-3.**

| # | Fork | Recommendation |
|---|---|---|
| **F1** | **Q66 tick binding-class** — now blocking. | **(A) MODEL-BINDING**, 12.25 Hz fixed sim tick, render interpolated — **with one rider:** the *player's own* kinematics integrate at render rate and are sampled by the sim each tick. Combat cadence stays where the bands were born; the 82 ms quantisation lands on ability resolution (D2 shipped at 40 ms and nobody called it mushy) but not on the feel of your own feet. |
| **F2** | Who writes the GDScript runtime. | **drax builds the runtime** (SKIRT's named recipient; pure logic with normative test vectors; lives in git with a headless suite); **the Astra lane builds the scene and PACKs it**, vendoring the runtime by sha. A combat runtime cut into ≤ 40-minute codex bursts is the wrong grain, and the lane's usage ceiling has already halted two runs. |
| **F3** | Input scheme. | **GD-faithful mouse** (RMB-hold EoR, LMB Blitz, 2 / 3 / 7, move-to-cursor), **desktop native build only**. WASD makes you a different pilot. |
| **F4** | Camera zoom for this scene. | **GD-matched (~8 % figure) as default**, house 17 % on a toggle. The scene's purpose is comparison; the house register is a product call that this scene does not need to re-litigate. |
| **F5** | Player body. | **The Keeper** — the only complete 8-direction set; an open arena with no north-facing cells (Necromancer) reads broken within seconds. Her camera flaw (Q80) is cosmetic in a placeholder scene and the body is a one-resource swap later. |
| **F6** | Scope of the first playable. | **Waves 150–160, one life, restart key.** No loot, no levelling, no Crucible shop, no between-run meta. Exactly the referent's window. |
| **F7** | Pre-T-A play. | **Yes, for feel only** — Matt plays as soon as P1 + P2 meet; no fidelity figure is quoted from those sessions. |

---

*Tracker-delta: game tracker SESSION-DELTA 2026-09-20; Q81 filed (Q66 cross-noted as folded into F1, row not struck — unruled); matt_to_do T30 filed. — gandalf, 2026-09-20.*

---

## 5 · P0-d — conductor recon, returned 2026-09-20 (evidence only)

1. **Arena geometry is reachable:** `agentic_orchestration/galadriel/notes/crucible-arena-geometry-v1.json` exists on disk (sha256 derived at use, never retyped here).
2. **⚑ R-L68-2 (the metre-scale pin) never landed.** It is cited at KC2-MC L-68 (born) and L-91 (spec delivery) and **in no later row of either the KC2-MC or the LIFT ledger.** The ring's scale is therefore still `DERIVED-WEAK` — u = 0.198 m/minimap-px, band [0.094, 0.366], a **1.7× spread** — and SKIRT § 7.1 / R-L91-5 made first-arena-frame-for-Matt's-eye gate on it. **For a playable this is not cosmetic:** arena size sets time-to-reach-spawn, kiting room and how often walls matter. The pin (register the Class-1 footprint against the final pursuit model's occupancy hull, 86.9 × 85.3 m) becomes a **KC2-PLAY P0 item for galadriel + gamora**, before the arena plate is authored.
3. **⚑ The pack's `arena.json · containment.runtime_containment` still reads `policy: "SKIRT"`, `claim_class: "PRESENTATION-CHOICE-NOT-MODEL-TRUTH"`** — the pre-D-CP2-1 text. The runtime spec body was integrated to AUTHORED-WALLS (both layers); the v3.1 pack row was not. Spec and pack disagree; the ruling (D-CP2-1, Matt verbatim) governs. Routed into the **v3.2 pack-delta scope** (star-lord cut) alongside whatever P0-a returns; the builder is told to follow the ruling, not the row.

---

## 6 · Corrigenda-forward (2026-09-20) — after P0-b (`2026-09-20-kc2-play-2d-retarget-spec.md`, `6cc64e5d`) and P0-c (`drax/notes/2026-09-20-kc2-play-p0c-scene-capability-census.md`, `05b0f4ab`). Nothing above is rewritten; where this section conflicts with the body, this section governs.

1. **§ 2.6 "living on leech" — WRONG SHAPE, mine.** Measured: the referent sits at **full health 42.84 %** of the fight, **below half 3.46 %**, Menhir's Will **MEASURED-ABSENT**. He is *topped up* by leech, not living on it. HP-trace shape stays a first-class T-B metric; its **expected value is a mostly-full globe with a shallow fast saw-tooth and rare deep excursions.** A builder must not "fix" a correct twin for sitting full. The D2 Whirlwind comparison holds at the inversion moment only, not the steady state. I asserted a feel from genre memory where the footage had already measured it — the instrument-inversion family, an eleventh face.
2. **§ 2.2 `hp frac` → absolute `hp` + `hp_max` on the wire** (Lap Q D-Q1: referent `health_max` fell 18.18 % for 8.283 s; a fraction hides it).
3. **§ 2.7(iv) / § 1 / § 5 "1.7× band" — STALE.** R-L3-2 excludes the point estimate 0.1981 and narrows to **[0.22277, 0.3663] (1.64×)**. And P0-b + P0-c independently show R-L68-2's pin method is **unsatisfiable**: the wall-less hull (86.915 m) cannot fit the 201-px ring inside the window. **Conductor ruling (veto-open): the arena is a swappable data object.** T-A runs on the W1 sim-sibling's own wall (like with like); play runs on the video-measured ring at a registered `u`; the hull is retired as a pin target; the rider routes to galadriel. The walled play arena being markedly tighter than the sealed wall-less spread is a **declared expectation**, not a port defect.
4. **§ 2.1 `sin 53°` → the wire's constant** (52.9535…°, GL-10); `ppm` = ~~71.885 / 152.374~~ **75.668 (F4 default) / 160.394 (house)** *(corrected 2026-09-20: the first pair was computed at h_fig 2.0 against a text fixing 1.9 — Gate-1 BLOCK-A; see the 2D spec's Corrigendum-Forward 1)*, derived not chosen; F4's toggle is a Camera2D zoom ratio.
5. **From P0-c, now charter law:** the Crucible scene gets its **own project directory** (not `cliffside_v*`; clear of the C-7 freeze) · `cliffside_v*` is a generated artifact, so the runtime enters by a new exporter `--vendor` capability (sha-verified, refuse-on-mismatch) — **first build item** · the VFX grammars' pixel-physics hit resolver is excluded **by assertion** (no `CollisionObject2D` under any token) · **no combat-relevant duration is handed to a 60-Hz grammar** — the sim starts and cancels · runtime home `reincarnated-godot/kc2_runtime/`, headless `--script` runners, no GUT · macOS export preset built early; editor-on-Matt's-Mac is the feel-only fallback, never a Web build.
6. **SKIRT § 7(3) figure hygiene:** floor area — spec says 27,875 px², the geometry file says 29,455; the four obstructions are "unmapped islands" in the file. **The file governs; the spec figure is not re-quoted forward.**
7. **P0-b open questions, conductor dispositions (veto-open):** OQ-2 `h_fig` = 1.9 m · OQ-3 route to galadriel, do not block · OQ-4 fire the HP saw-tooth re-query before T-B · OQ-5 in-process plain GDScript · OQ-6 token = model radius exactly. **OQ-1 (held-RMB across a release — auto-resume?) goes to Matt:** it is a fact about Grim Dawn his hands know and no document records.
