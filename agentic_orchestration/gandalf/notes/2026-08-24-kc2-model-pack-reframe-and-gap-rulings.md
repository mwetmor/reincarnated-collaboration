# KC2 — THE MODEL-PACK REFRAME + THE GAP-AUDIT RULINGS (Matt, 2026-08-23/24)

**Author:** gandalf (`ELICITOR` → ruling capture; sim arc).
**Session shape:** Pattern-B dialogue. Matt requested a full ultra-think gap audit — the Python battle sim vs the real GD fight he played — to decide what must exist before the (JSON) baton hands to the Godot team. Two named sub-agent inventories (gamora: sim modeled-vs-unmodeled; legolas: referent substrate enumeration) fed a foreground synthesis; Matt ruled the full set.
**Supersedes:** Q59 as written (`matt_decision_needed/README.md`, struck this session) — the replay-baton premise the fork rested on is retired.
**Standing law untouched:** D5 (`E-s09-cp150` immutable; siblings only) · Law 3 (no fitted constants, no invented rules) · sibling checkpoint `E-s09-cp150-mech` sha `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b`.

---

## 1. THE REFRAME (Matt verbatim, the load-bearing sentence)

> *"the goal is to provide the baton which will allow the godot team to immediately create a version of it that is playable as the character. This is why I want all aspects present"*

**Replay baton → PLAYABLE MODEL-PACK.** A replay carries one fight's recorded truth (enough to watch). Playable-as-the-character means the player goes where the recording didn't — monsters must react live — so the baton must carry **the rules of the fight**, not (only) its record. The Godot side stops being a playback head and becomes a **runtime** executing the same model the Python sim executes.

**The two-layer baton (ruled):**

- **Layer 1 — MODEL (playable):** monster AI state machine (graph + transition conditions + parameters) · 188 monster stat blocks with skills/specials/reuse gates/DoT riders · player kit complete (9 bar skills, 8 devotion procs, Menhir's Will, potions, summons) · damage/mitigation/leech math · per-wave spawn structure · arena geometry with bounds · tick + RNG contract. All decoded provenance, digest-pinned; **no invented rules.**
- **Layer 2 — REFERENCE (acceptance test):** the recorded fight (sibling-checkpoint tracks). The Godot runtime, driven along the recorded player path, must reproduce the recorded fight within tolerance — the twin-test that converts "we implemented your model" from assertion to checkable fact.

**Founding-precedent note:** this baton is the prototype of the engine→Godot contract the actual product ships (engine-emitted model-packs executed by a Godot runtime). The seam is being built early, on a fight that can be verified.

## 2. THE RULINGS (Matt, confirmed 2026-08-24)

**Prior two rulings this dialogue:** the baton is **not cut** until the model is complete enough to play (Q59 premise retired). **Wave-160 is a GRADED ROW, never a hard pass/fail gate** (settles the shape of the F-4/D4 prereg question; PM5 grades terminal wave first-class but does not gate on it).

Per-facet, from the gap audit (**IN-SIM + BATON = "BOTH"** throughout — the governing principle Matt's (d,e) challenge produced: *anything the sim models with a visible consequence must reach the baton, or Godot renders lies*; the only coherent sim-only content is invisible math):

| # | Facet | Ruling |
|---|---|---|
| (a) | Per-monster state track | **BOTH** |
| (b) | Alert-before-pursue (entry condition + duration decode) | **BOTH** |
| (c) | Monster specials firing (45/58 slots silent → reuse-gate decode) | **BOTH** |
| (d) | Menhir's Will + devotion procs (Turtle Shell, Fighting Spirit, Ascension…) | **BOTH** |
| (e) | Incapacitation states (monster) + player control effects (286 rows) — stun/knockdown first | **BOTH** |
| (f) | Player's two summons (Guardian of Empyrion, Deathstalker) as first-class actors | **BOTH** |
| (g) | Player cast events (dashes, War Cry, potions, procs) in the event vocabulary | **BOTH** (sim half largely exists; work is emission) |
| (h) | Arena walls/bounds | **BOTH — sim half gated on the path-vs-boundary check** (if any recorded path crosses the decoded 86.915 × 85.303 m boundary → walls IN-SIM non-negotiable; if none approaches → provably inert in-sim, baton geometry + runtime clamp satisfies) |
| (i) | Fleeing · dodging · distress calls · swing-pause · emotes · DoT stacking | **Model-layer as rules/parameters** (re-ruled under the playability reframe — "inert in the recording" ceased to be the criterion; a live runtime is entitled to the rules). **DoT stacking via video-measurement lap** — the stacking function is absent from substrate (declared UNDECODABLE-FROM-SUBSTRATE); the lap derives it empirically from the reference footage; a guessed formula never ships |

## 3. AUDIT ESSENTIALS (the facts the rulings rest on — sub-agent inventories, 2026-08-23/24)

**Sources:** gamora sim inventory + legolas substrate enumeration, both in-conversation; load-bearing facts banked here.

- **Baton vintage:** the baton the Godot scene pins (`kc2_baton.gd:57`, `kc2-baton-v1-E-s09-cp150-20260809_052836.json`, sha `d7ecd866…`) is **pre-I-1**: monster `hp_max: 0.0`, `crit_model: NOT_MODELLED`, no monster mitigation, `monster_attack_model: abstract-schedule`, player never dies (end `arena_tier_exhausted`). Godot has been presenting the pre-PM4 sim. Re-cut non-optional under any ruling.
- **Monster AI:** real controller = **43 states** (enumerated from `Game.dll` strings). Sim expresses ~9 (7-state engagement enum + 11-code mech enum; 12/17/18 declared unreachable with reasons). Baton carries **3** (PRESPAWN/LIVE/DEAD). `AGENT_STATE.md:347` names "17 unexpressed AI states" standing. AlertBeforePursue: state + `OnBegin @0x109410` (anim `0x21`) decoded; **entry condition (`ShouldPlayRallyOrAlert`) + duration UNDECODED** (`UNREACHED-U3`/`U-U-2`). Sim binds 3 of 27 ControllerMonster fields. Undecoded-but-present groups: `SkillUsage` `Attacking` `Dodging` `PetBehaviour` `Patrolling`-idle `Emote` `Sleep` `Loot` `Dying` + 7/9 `Fleeing`. Decoded ready: Senses, AngerManagement, DistressCalls, Pursuit, Patrol-disassembly.
- **⚑ ViewDistance contradiction (surfaced to Matt in-audit):** WR3-W2 measured 15.0 m population-wide; Lap U measured **80.0 m on 169/169 rolled tier-16 Crucible monsters** — the Crucible override governs waves 150–160; worst spawn→player ≲ 76 m ⇒ everything sees the player at spawn (this is what made distress calls inert *in the recording*).
- **Player:** modeled-measured core (HP 20,005, full energy model, EoR channel to the tick, Soulfire, Tip the Scales, leech ladder, potions + War Cry counterplay limb, movement + 3 dash layers, armour/resists; fixture envelope −0.5/+3.9%). **13-row OUT_OF_MODEL manifest** (`fixture.py:234-248`) incl. Ascension, **Menhir's Will (the build's actual circuit-breaker — not Ghoulish Hunger)**, Fighting Spirit, Resilience, devotion procs, retaliation. Lap G decoded the full kit: 9 bar-bound skills, 8 devotion procs with host bindings, 21 defensive actives, 76 consumable rows.
- **Monster stats/skills:** eHP 188/188 closed (Lap D) · damage measured-slots · OA/DA sheets · roster decode 100% (nemesis 9/9, hero 27/27; 1,733 granted-tree skills; 584 nested damage rows to depth 6) · 264 DoT riders with terminal-wave killers named. Gaps: **45/58 special slots DO NOT FIRE** (no measured reuse gate, `threat.py:607`) · DoT *stacking* undecodable-from-substrate · player-side control application not carried (I-5).
- **Environment:** `arena_bounds.shape = "UNBOUNDED"`, open-plane, **no walls/collision in sim at all** · arena-identity disagreement `NAMED-I26-1` (sm1 vs survivalmode3) measured-unswitched · reference run is **BLESSINGS-OFF, DEFENCES-ON** (4 purchases decoded: 3 beacons + Vanguard Banner; 6 effect rows land on player) · T17 `.cnv` falsifier standing (non-blocking; lands on PM5 basis if it overturns p06=OFF).
- **Sustain-asymmetry reading (why 151–156 vs 160 is unmysterious):** every missing player-side layer (Menhir's Will, Turtle Shell, Fighting Spirit, Ascension) extends survival; partly offset by monster-side gaps pointing the other way (45 silent specials = missing incoming damage; control-immune sim player). Grading faithfulness before these layers enter would grade the wrong question — the empirical ground for the wave-160-not-a-gate ruling.

## 4. WORK SEQUENCING (proposed to Matt; the next ruling)

- **Wave 1 — decode + cheap checks (parallel):** D-1 legolas AlertBeforePursue entry+duration · D-2 legolas specials reuse gates · D-3 legolas remaining ControllerMonster field groups (SkillUsage/Attacking/Dodging/Fleeing/PetBehaviour/Roaming-Crucible/idle/emote) · D-4 DoT-stacking video-measurement lap (legolas+galadriel; media = eor-test-2 MP4, `/Volumes/reincarnated` re-verified at launch — mounted 2026-08-23 per T19) · C-1 gamora path-vs-boundary check (gates (h) sim-half; co-feeds F-5/SKIRT) · S-1 gandalf `SPEC-AUTHOR` two-layer baton-v2 schema draft.
- **Wave 2 — sim builds (gamora; Gate 2 + DRIFT-CRITIC):** B-1 player sustain layer (d) · B-2 control states (e) · B-3 summons (f) · B-4 specials firing (consumes D-2) · B-5 alert-before-pursue (consumes D-1) · B-6 state-machine expansion + per-actor state emission (feeds (a)) · B-7 walls iff C-1 fires · cast-event emission (g).
- **Wave 3 — KC2-PM5 re-grade:** grades the COMPLETED model (occupancy + terminal wave GRADED-not-gated + duration/pacing), prereg per D4; F-2 alert decode closes before it; T17 falsifier carried on its basis.
- **Wave 4 — export + handoff:** baton-v2 cut (star-lord/gamora; WARN-A `export/MIGRATION.md` entry rides) · Godot runtime spec → drax, carrying F-5 (camera re-ratification under translation) + SKIRT load-bearing.
- **Conduct fork for Matt:** (A) one chartered **model-completion run** under the desirable pattern (fit test passes: gap list bounded/enumerable; per-gap decidable closure; forks just pre-drained by this ruling set; authority-resident) — *conductor's lean* · (B) KR-sequenced ordinary engine waves per the D3=(a) precedent (builds outside runs; runs only grade).
- **Carried, unblocked:** decisions-log entry for the mech wave (owed; jack-ryan writes) · F-3 camp-limb sentence (gamora) · VFX archetype-binding run continues in parallel — seam-disjoint (its seats: elrond/Codex/galadriel/drax-probe; this arc's: legolas/gamora/star-lord; single soft contention = legolas if the VFX P2 lane-fault fallback ever fires).

---

*Captured 2026-08-24 by gandalf. Queue + tracker synced this commit (Q59 struck with ruling; engine-tracker SESSION-DELTA prepended).*
