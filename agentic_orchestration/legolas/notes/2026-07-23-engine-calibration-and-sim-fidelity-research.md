# Research — Cross-Engine Calibration Methodology & Sim Fidelity Testing — 2026-07-23

**Mode:** A (analytical)
**Commissioner:** gandalf (ELICITOR) + Matt — ultra-think session, TRUE-SOURCES forks
**Feeds:** TSF-6 shape (Matt's blind-hero hypothesis); also informs TSF-2/TSF-3 (adapter architecture)
**Sources consulted:** listed in full at end

---

## Summary

Five precedent communities handle multi-source calibration. Their shared pattern: one authoritative reference (hardware, retail server, original binary) against which a single target engine is pinned — not N-to-N cross-comparison. The closest analog to our problem is the MMO private-server community, which calibrates mob AI (aggro, leash, speed) against retail *behavior observations* when no ground-truth data file is accessible. The robotics sim-to-sim community supplies the cleanest formal vocabulary: parameter-fidelity (does the ingested number survive into the sim intact?) vs. behavior-fidelity (do emergent dynamics match a reference capture?). Matt's blind-hero design maps cleanly to parameter-fidelity testing, which is machine-decidable without ground-truth video capture. GD's spatial behavior fields (aggro range, movement speed, leash, pack composition) ARE stored in DBR records but are confirmed absent from grimtools web payloads; the .arz extraction is the only lane that surfaces them.

---

## Q1 — Cross-Engine Calibration Methodology: Named Precedents

### Precedent 1: Emulation-accuracy communities — byuu/bsnes/higan

**Shape:** One reference (real SNES hardware) → one target engine (bsnes). The question is never "reconcile two emulators together" — it is always "does this emulator reproduce the reference hardware's behavior?"

**Calibration method:** Test ROMs purpose-built to isolate a specific hardware behavior (e.g., SA-1 bus conflict timings). Vitor Vilela's SNES speed test suite revealed bsnes timing was "all way off" against hardware measurement; byuu then tuned until achieving "~99% accurate" timings (his reported metric). Ground truth is hardware captures — logic analyzer traces, oscilloscope waveforms, observed pixel timing on real silicon. (Source: bsnes.org/articles/state-of-emulation-5/)

**Acceptance criterion:** byuu frames it qualitatively — "a respectable state" where the delta between hardware units and the emulator is smaller than the variance between hardware units themselves. Not a formal pass/fail band.

**What transfers to our case:** The test-ROM pattern maps directly to "fixed probe input → measure output" — our blind hero is the test ROM equivalent. The principle that accuracy is measured against the *reference system's behavior*, not against another emulator, is load-bearing.

**What does NOT transfer:** byuu targets a SINGLE source system. We normalize N ARPGs into one original engine. No single one of our sources is "the hardware." We cannot use one game's parameters as the acceptance band for another game's behavior.

### Precedent 2: Decompilation/reimplementation — Devilution (Diablo 1)

**Shape:** galaxyhaxz's Devilution project (2018–2020) reconstructed Diablo 1's exact source code from the compiled binary, aided by a symbol map accidentally left on the Japanese PS1 port and debug strings embedded in the PC release. Goal verbatim: "recreate the original source code as accurately as possible, in order to ensure that everything is preserved, *including bugs and badly written code in the original game*." (Source: github.com/galaxyhaxz/devilution README)

**Calibration method:** The source code IS the fidelity target. Once the decompiled code compiles and produces bit-identical output to the original binary, fidelity is proven. Ground truth is the original binary's observable outputs.

**D2R extension:** Blizzard's Diablo 2 Resurrected retained the original game logic as the authoritative computation core ("all the core logic is still based on the old calculations") with a new renderer laid over it. The legacy binary is not emulated — it is the system.

**What transfers:** The "original binary as oracle" pattern. When we ingest D2 Skills.txt numbers and push them through our kit_compiler, the D2 binary's known outputs (the kit_numeric anchors VDM-1 verified, e.g., Fire Ball 6–15 post-formula) serve as our oracle — exactly as Devilution used the original executable as its oracle.

**What does NOT transfer:** We are not reimplementing any single game. Our engine is original. The "preserve bugs too" ethos is inverted — we normalize across games, which means intentionally diverging from any single game's behavior when it doesn't generalize.

### Precedent 3: MMO private-server emulation — vMaNGOS / TrinityCore

**Shape:** vMaNGOS (Vanilla MaNGOS core) and TrinityCore are the closest structural cousin to our problem. They reverse-calibrate World of Warcraft's mob AI — aggro radius, leash behavior, pathing, threat tables — against retail server behavior without access to Blizzard's server source code. (Sources: github.com/TrinityCore/TrinityCore issues #830, #1031, #25833; github.com/vmangos/core; wowpedia aggro_radius article)

**Calibration method:** Two lanes used in practice:
1. **Packet sniffing:** Client-server traffic is captured with network sniffers during retail gameplay, revealing mob state transitions (enter combat, reset, evade) at known player positions. This yields behavioral ground truth at specific distance/angle values.
2. **Community parameter tables:** Player-observed aggro distances (documented as "~20 yards for same-level mob, ~1 yard per level difference, capped at 45 yards for 25+ level advantage") aggregated from consistent in-game testing. These are behavior-fidelity observations, not file extractions.

**Fidelity gap documented in TrinityCore:** Mob leash behavior explicitly deviates from retail in the public core — "mobs only follow you for a certain distance" vs. retail "mobs follow continuously if you keep attacking." This gap is open in the bug tracker (TC issue #25833, AC issue #5455) and represents a known behavior-fidelity failure where the parameter (leash distance) is hardcoded rather than sourced from observed retail behavior.

**What transfers:** This is the direct analog. We have the same problem structure — no server source access, must infer spatial parameters from external observation or community-sourced tables. The packet-sniff method = our "grimtools web payload + community guides" lane. The behavior-fidelity gap in TrinityCore is the exact failure mode we risk if we use synthetic mob parameters in our engine.

**What does NOT transfer:** vMaNGOS/TC calibrate a single reference (WoW retail) into a single target (their server core). We aggregate N games. Their behavior-fidelity oracle (retail WoW) is a live, queryable system; our reference ARPGs are single-player games we can run but not query in a structured way at scale.

### Precedent 4: Robotics / RL — Sim-to-Sim Validation (MuJoCo vs Isaac Gym)

**Shape:** Robotics practitioners train policies in one simulator (Isaac Gym / Isaac Sim) then validate in another (MuJoCo) before real-world deployment, or vice versa. The validation question: does a policy trained in sim A transfer to sim B without retraining? (Sources: arxiv.org/html/2404.05695v1 Humanoid-Gym; arxiv.org/pdf/2603.06218 Few-Shot Neural Differentiable Simulator; roboticscenter.ai MuJoCo vs Isaac Sim 2026)

**Calibration method:** System identification — running the same control inputs through both simulators and comparing trajectory outputs. Key parameters: joint friction, rotor inertia, actuator delay, contact stiffness. MuJoCo's identified-parameter workflow is documented across dozens of papers; "contact parameter identification reduced average trajectory error from 1.14 to 0.73 RMSE." Residual analysis: the per-step difference between reference and target simulator trajectories, minimized by parameter tuning.

**Vocabulary directly applicable to our problem:**
- **Parameter-fidelity:** Does the ingested parameter value survive intact through the target system? (machine-decidable)
- **Behavior-fidelity:** Do emergent dynamics match a reference trajectory? (requires ground-truth acquisition)
- **System identification:** Tuning free parameters in the target system to minimize residual error against reference outputs.
- **RMSE / trajectory delta:** Quantitative acceptance metric used across sim-to-sim work.

**What transfers:** This vocabulary is the cleanest framework for Matt's blind-hero hypothesis. The two-track fidelity split (parameter vs. behavior) maps directly. Behavior-fidelity for us would require GD gameplay capture; parameter-fidelity is machine-decidable from the .arz extraction alone.

**What does NOT transfer:** Robotics has a physical ground truth (the real robot). We have no single authoritative "real" ARPG combat system — each source game IS its own reality. Sim-to-sim for robotics also assumes the same physical laws govern both simulators; our engine uses different combat math than any source game by design.

### Precedent 5: Digital Twin Validation

**Shape:** Industrial digital twins (manufacturing, infrastructure) are validated against physical system telemetry by comparing twin outputs to real-world sensor streams. (Sources: ASIMOV D2.5 Digital Twin Validation; arxiv.org/pdf/2603.14607 IBM Quantum calibration; mdpi.com/2075-1702/13/9/750)

**Calibration method:** IoU, PSNR, RMSE, structural similarity (SSIM) against a reference dataset. Acceptance thresholds cited in literature: 95% = near-identical, 90% = close match, 85% = usefully similar. Validation uses statistical tests (chi-squared, Kolmogorov-Smirnov) for distribution comparison, not just point-to-point RMSE.

**What transfers:** The acceptance-band framework (RMSE < X, distribution divergence < Y) is portable. For our engine, a behavior-fidelity test would need to define what "85% similar" means for an ARPG encounter — time-to-kill distribution? Pack engagement range distribution? This is the design question Matt's hypothesis would force to a concrete answer.

**What does NOT transfer:** Digital twins target exact physical reproduction. Our engine explicitly normalizes across games — "fidelity to which source" is not resolved the way it is for a factory floor twin.

### What Transfers to N-Source ARPG → Single RDR Engine

The aggregated lesson from all five communities:

1. **Per-adapter, not cross-adapter:** No community attempts to reconcile two reference systems against each other. The emulation-accuracy pattern is always "one reference → one target." For N source ARPGs, the correct architecture is N independent adapters, each calibrated against its own game's oracle — not a baseline-game-to-baseline-game chain. This is structural evidence for TSF-2 lean (a).

2. **Parameter-fidelity is testable before behavior-fidelity.** Robotics sim-to-sim communities always validate parameter delivery first (does the number arrive intact?) before validating behavior (do trajectories match?). Parameter-fidelity is cheaper and machine-decidable. Behavior-fidelity requires ground-truth capture.

3. **Community-observation tables as a legitimate calibration tier.** vMaNGOS demonstrates that player-measured aggro distances (community tables) are a valid, widely-used calibration input when no file extraction is available. This legitimizes our current corpus prose/lattice data as a tier, not a failure — it is what private-server teams use at scale.

4. **The oracle inversion:** For us, as in Devilution, the corpus `kit_numeric` anchors (VDM-1 verified) become the oracle that checks the adapter, not the other way around. The datamine adapter emits a number; the corpus anchor verifies it. The pipeline is: raw file → adapter formula → compare to VDM-1-verified corpus anchor → pass/fail.

---

## Q2 — Testing the Battle Sim's Fidelity: Matt's Blind-Hero Design

### The experimental shape and its precedents

Matt's design: import GD's (or another source game's) enemy monster roster — true aggro range, physics, movement speed, pack details — run against a BLIND BASIC HERO in our engine, compare against GD's own enemy/pack behavior.

**"Blind" in our vocabulary (confirmed from gamora ablation files):** `policy_config: [["distance", 1.0]]` — a fighter that acts purely on proximity, no skill intelligence, no targeting awareness. This is already implemented machinery in `spatial_gauntlet/spatial_engine.py`. The arm is operational.

**Closest precedent: Fighting game frame-data verification rigs.**

Fighting game communities (Street Fighter, Tekken, Guilty Gear) maintain deterministic test harnesses where a character is placed in a fixed state (standing, neutral) and a specific move is executed, then frame-counted against a reference capture. The "opponent" is either a stationary training dummy (the purest fixed-agent case) or a character frozen in a specific pose. This decouples the question "does the move have the correct startup/active/recovery frames" from all interaction effects. The key principle: *fix the response surface; measure the stimulus side*. Our blind hero IS the fixed-response surface; GD's enemy parameters are the stimulus side.

**Game AI regression testing:** RL-based regression testing for game AI compares behavioral outputs between engine versions by running the same input sequence through both versions and measuring output divergence (cited: arxiv.org/pdf/1906.00317). The fixed-agent pattern appears here too — a scripted agent with deterministic actions used as a probe to isolate the engine's response.

**MMO-emulator analog:** vMaNGOS uses player characters with scripted movement (walk to a fixed position, stop) as de facto fixed agents when calibrating aggro radius. The player is the control; the mob's response (engage/not-engage) at each tested distance is the measurement.

### The ground-truth question: parameter-fidelity vs. behavior-fidelity

**Parameter-fidelity test (machine-decidable, recommended first):**

The question is: does our engine correctly instantiate GD's aggro radius of X meters such that an enemy with that parameter engages a target at distance X but not X+ε? This is answerable by:
1. Extracting the parameter from .arz (e.g., aggro range = N GD units)
2. Converting to our sim's unit system (requires establishing the conversion constant — see Risks)
3. Instantiating an enemy with that converted parameter in our engine
4. Positioning the blind hero at distances X−ε, X, X+ε and checking engagement
5. Pass if engagement boundary matches within conversion tolerance

This test is 100% machine-decidable. It does NOT require GD gameplay capture.

**Behavior-fidelity test (requires ground-truth acquisition):**

The question is: does an encounter with GD's enemy roster "feel" like GD combat — timing, tempo, threat geography? This requires:
1. Video capture of GD gameplay with the same enemy types (the reference trajectory)
2. Replay analysis: player position, mob positions, engagement events, time-to-contact, damage cadence
3. Comparison of these distributions against our sim's outputs for the same roster

This is what the digital-twin and sim-to-sim communities call "behavior-fidelity validation." It is expensive to acquire and not machine-decidable without defining explicit metrics (e.g., "time-to-first-contact distribution within ±15% of GD reference"). Matt's observation — "that may be all we need to prove this hypothesis" — suggests he is reaching for parameter-fidelity first, not behavior-fidelity, which is the lower-cost correct ordering.

**What precedent communities use:**

| Community | Primary oracle type | Metric |
|---|---|---|
| bsnes/higan | Hardware captures (logic analyzer) | Timing within ~99% of hardware |
| TrinityCore | Packet sniff + community observation | Qualitative issue-tracker comparison |
| Robotics sim-to-sim | Reference trajectory from other sim | RMSE on trajectory delta |
| Digital twin | Physical sensor telemetry | RMSE, SSIM, IoU; 85–95% threshold |
| Fighting game frame data | Video frame-count from official source | Exact frame count match |

For our case: **corpus VDM-1 anchors = our "hardware capture"** for player-side parameters. For the enemy side, there is no equivalent existing corpus oracle — the .arz extraction would be the first true ground truth.

### GD spatial-field availability: what .arz carries vs. what grimtools surfaces

**Confirmed: grimtools web payloads do NOT carry spatial/behavioral fields.**

Three direct observations from this research pass:
1. grimtools.com/monsterdb monster page (fetched: /monsterdb/2253): displays Health, Energy, Attributes, Offensive/Defensive Ability, DPS, Armor, Resistances. No movement speed, aggro range, sight range, leash range, or pack composition fields.
2. The grimtools monster database thread (forums.crateentertainment.com/t/grimtools-monster-database/42861) explicitly lists what the DB contains: character stats, skills, loot. No spatial/behavioral mention.
3. The gamersizayuke.com guide confirms the same field set: attributes, combat stats, resistances, skills, loot — no behavioral fields.

**The prior join-surface probe (2026-07-23-join-surface-probe.md §2c) already confirmed:** "GD monster HP and DPS are NOT stored in the monsterdb.js payload; they are computed at browser render time from base-stat tables and difficulty modifiers." Spatial fields follow the same pattern — they live in DBR records, not the grimtools JS payload.

**DBR record types to check once .arz lands (sourced from modding community):**

Confirmed DBR field name (from forums.crateentertainment.com/t/help-movement-attack-and-castspeed/41855):
- `characterRunSpeed` — character run speed, confirmed in `/records/creatures/pc/` player records

From the same modding community discussions, the following field name pattern is established for character records:
- `characterAttackSpeedAverage` — attack speed type field

By GD's DBR naming convention (field names are camelCase descriptors), the spatial/AI fields expected in monster DBRs are:
- **Speed:** `characterRunSpeed` (confirmed in PC records; monster records use the same template hierarchy)
- **Aggro/sight range:** Field names in GD use the "sphere" or "radius" suffix pattern; expect `aggroSphere` or `sightRadius` or `notificationRadius` (these are GD engine-internal naming conventions based on the template system — NOT confirmed, inferred from convention)
- **Leash:** Leash behavior in GD appears to be engine-level rather than per-monster (the gameengine.dbr `run speed cap` and camera range discussion suggests engine-globals); individual monster leash may be in the monster AI controller record
- **Pack composition:** Grimtools confirms spawn location data (area, count per area) is tracked; the spawn count/pack size data likely lives in proxy/spawn records, not the monster base record

**Record path structure to check once .arz extracted:**

Based on GD modding guide structure references and player character DBR paths:
```
records/
  creatures/
    pc/             — player character records (confirmed: malepc01.dbr, femalepc01.dbr)
    monsters/       — expect monster base records here
      [zone]/       — zone-specific subdirectory
    bosses/
    champions/
  game/
    gameengine.dbr  — engine-global parameters (run speed cap, camera ranges confirmed)
  proxies/          — spawn proxy records (likely source for pack/spawn composition)
```

The exact field names in monster records are UNCONFIRMED from web sources. The DBR Editor tool (part of GD modding tools, shipped with the game) exposes all fields from the template hierarchy when a .dbr is opened — this is the intended inspection method. After .arz extraction, opening any monster record in the DBR Editor (or examining the extracted .dbr text directly) will surface the exact field names. The grimarz tool (gitlab.com/atom0s/grimarz) is documented as capable of extracting any .arz database file.

**A critical negative finding:** there is no community wiki, forum thread, or guide that documents the specific field names for GD enemy aggro range, sight range, or leash range. This is knowledge that lives in the extracted files themselves, not in any indexed community resource. The .arz extraction (Matt's T4 steam download) is the only path to these field names.

### Risks

**1. Unit-system conversion (highest priority risk).**

GD map units are not documented in any accessible community resource. The grimtools monsterdb shows HP and DPS in GD native units; movement speed and range are in GD's engine coordinate system. Our sim uses its own spatial model. Establishing the conversion constant (GD units → our sim units) requires either: (a) a known reference measurement in both systems (e.g., GD melee attack range = X GD units = Y meters in our sim, calibrated against visual gameplay), or (b) a community-sourced conversion table (none found in this research pass). This conversion constant is the single highest-risk unknown — without it, parameter-fidelity testing is blocked.

**2. Animation-time vs. logic-time coupling.**

GD's attack cadence involves animation timing that is NOT stored in the skill DBR payload (confirmed: `cast_time` is absent from all_skills.js per the join-surface probe §4). Attack speed in GD is stored as `characterAttackSpeedAverage` (a type field) with actual timing derived from animation frames. Our sim uses logic-time tick intervals. If we import GD's "attack speed" as a raw parameter, we may be importing an animation-time value that our sim interprets as a logic-time interval. This can make enemies appear to attack significantly faster or slower than in the reference game.

**3. Difficulty-tier modifiers masking base parameters.**

GD applies difficulty modifiers (Normal/Veteran/Elite/Ultimate) to mob stats — HP, damage, speed are all multiplied. The base DBR values are the unmodified parameters; the in-game behavior players experience is the modified values. If we import DBR base values and compare against video capture of Elite-difficulty GD gameplay, we are comparing different parameter tiers. Resolution: pin the comparison to Normal difficulty, which is closest to base DBR values, or extract difficulty modifier tables and apply them.

**4. Pathfinding-implementation differences.**

GD's pathfinding (A* or navmesh, not documented in public sources) will produce different mob movement trajectories than our sim's spatial engine even with identical aggro radius and speed values. Two mobs with identical parameters will reach a target at different times if pathfinding geometry differs. This is a structural limitation: parameter-fidelity testing can be isolated to a flat open-space scenario to minimize pathfinding variance, but complex encounter geometry will always show divergence that is not a parameter failure — it is a pathfinding-implementation difference. **The blind-hero test design should use simple flat topology to quarantine this risk.**

**5. GD `sk<N>` ID fragility for skill parameter import.**

Confirmed from join-surface probe §3: GD skill IDs are generated numeric keys (`sk296`, etc.) with no embedded English name. For mob spatial parameters (aggro, speed), the risk is lower because those are likely in the character/monster record, not the skill record. But any mob skills that affect movement (teleport, charge, leap) will have the same ID fragility as player skills — the skill name bridge from `sk<N>` to English is not yet built.

---

## Short Synthesis for TSF-6 Shape (evidence-only; gandalf draws recommendation)

The five-precedent survey establishes that Matt's blind-hero design is a recognized experimental shape — it appears in emulation-accuracy (test ROM + fixed probe), fighting-game testing (dummy + fixed move), and MMO-emulator calibration (scripted player + mob response measurement). The design is structurally sound.

The two-track fidelity split is the critical architectural choice for the TSF-6 charter:

**Track A (parameter-fidelity):** Import GD DBR aggro range, movement speed from .arz extraction → convert to sim units → pin blind hero at bracketed distances → verify engagement boundary. Machine-decidable. Blocked only by: (a) .arz extraction completing (Matt's T4), (b) unit conversion constant established. Does not require GD gameplay video capture.

**Track B (behavior-fidelity):** GD gameplay video capture → extract engagement timing, approach trajectory, pack behavior distributions → compare against sim outputs for same roster. Requires ground-truth acquisition infrastructure not currently in place; this is a Phase 2 question.

The evidence indicates that Track A alone answers Matt's hypothesis as stated: "a test of the battle sim's capability to represent true spatial ARPG combat physics and feel, *enemy-side only*." The unit-conversion problem is the single gate between the .arz landing and a first parameter-fidelity run. The grimtools web payload is confirmed insufficient for this purpose — .arz is the necessary substrate.

---

## Knowledge Gaps Not Resolved

1. **GD unit → sim unit conversion constant.** No community source documents GD's map unit system. Will need to be reverse-derived from a known reference (e.g., GD melee attack range is documented in community guides as "close range"; the DBR value for that range can be compared to player expectation to establish a conversion factor).

2. **Exact DBR field names for monster aggro/sight/leash/speed in .arz.** Not documented in any indexed community resource. Dependent on .arz extraction (Matt T4). Field names will be visible directly in extracted .dbr files via DBR Editor or grimarz.

3. **GD difficulty modifier tables for base DBR → in-game-observed values.** Not retrieved in this pass. Needed to establish which difficulty tier to pin the behavior-fidelity comparison to.

4. **Pack composition record structure (proxy records).** Spawn proxy records likely hold pack size and composition parameters. Their schema is not documented in any retrieved source — also dependent on .arz extraction.

5. **Whether `characterRunSpeed` in monster DBRs matches the format confirmed for PC DBRs.** Confirmed for PC records; monster records likely use the same character template hierarchy but this is inferred, not confirmed from the modding community docs available.

---

## Source List

| Source | URL / Path | Access date |
|---|---|---|
| Join-surface probe | `agentic_orchestration/legolas/notes/2026-07-23-join-surface-probe.md` | 2026-07-23 |
| True-sources grill brief | `agentic_orchestration/gandalf/notes/2026-07-23-true-sources-grill-brief.md` | 2026-07-23 |
| KIT-FIDELITY wind-down | `agentic_orchestration/gandalf/notes/2026-07-23-kit-fidelity-run-wind-down.md` | 2026-07-23 |
| gamora blind ablation | `agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-ablation-blind-full.json` | 2026-07-23 |
| bsnes accuracy article (byuu) | https://bsnes.org/articles/state-of-emulation-5/ | 2026-07-23 |
| Emulation accuracy — GameTechWiki | https://emulation.gametechwiki.com/index.php/Emulation_Accuracy | 2026-07-23 |
| Higan on Libretro docs | https://docs.libretro.com/library/bsnes_accuracy/ | 2026-07-23 |
| Devilution README | https://github.com/galaxyhaxz/devilution/blob/master/README.md | 2026-07-23 |
| Devilution — GDNet article | https://www.gamedeveloper.com/programming/reverse-engineered-i-diablo-i-source-code-released-on-github | 2026-07-23 |
| TrinityCore issue #830 (NPC leash) | https://github.com/TrinityCore/TrinityCore/issues/830 | 2026-07-23 |
| TrinityCore issue #25833 (mob leash) | https://github.com/TrinityCore/TrinityCore/issues/25833 | 2026-07-23 |
| AzerothCore issue #5455 (aggro/leash rework) | https://github.com/azerothcore/azerothcore-wotlk/issues/5455 | 2026-07-23 |
| vMaNGOS core — GitHub | https://github.com/vmangos/core | 2026-07-23 |
| Wowpedia aggro_radius | https://wowpedia.fandom.com/wiki/Aggro_radius | 2026-07-23 |
| WoWWiki aggro_radius | https://wowwiki-archive.fandom.com/wiki/Aggro_radius | 2026-07-23 |
| Humanoid-Gym (sim-to-sim) | https://arxiv.org/html/2404.05695v1 | 2026-07-23 |
| MuJoCo vs Isaac Sim 2026 | https://www.roboticscenter.ai/rl-environments/mujoco-vs-isaac-sim | 2026-07-23 |
| Few-Shot Neural Differentiable Simulator | https://arxiv.org/pdf/2603.06218 | 2026-07-23 |
| ASIMOV D2.5 Digital Twin Validation | https://itea4.org/project/workpackage/document/download/8906/ASIMOV_D2_5_M32_version_1-0%20Digital%20Twin%20Validation%20-%20Methods%20and%20Techniques.pdf | 2026-07-23 |
| Digital twin fidelity metrics | https://www.emergentmind.com/topics/digital-twin-fidelity | 2026-07-23 |
| Fighting game RL agent paper | https://arxiv.org/pdf/1904.03821 | 2026-07-23 |
| GD modding — movement/castspeed forum | https://forums.crateentertainment.com/t/help-movement-attack-and-castspeed/41855 | 2026-07-23 |
| GD modding — making an enemy forum | https://forums.crateentertainment.com/t/question-dbr-editor-setup-making-an-enemy/32315 | 2026-07-23 |
| GD grimtools monster DB forum | https://forums.crateentertainment.com/t/grimtools-monster-database/42861 | 2026-07-23 |
| grimtools monsterdb entry /2253 | https://www.grimtools.com/monsterdb/2253 | 2026-07-23 |
| GD monster guide | https://www.grimdawn.com/guide/gameplay/monsters/ | 2026-07-23 |
| grimarz .arz extractor | https://gitlab.com/atom0s/grimarz | 2026-07-23 |
| GDModdingTool config_ALL.txt | https://github.com/azakhi/GDModdingTool/blob/master/Example%20Configurations/config_ALL.txt | 2026-07-23 |
