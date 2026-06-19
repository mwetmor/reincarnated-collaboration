# Encounter-measurement doctrine — design-session spine

**Type:** design-note spine (gandalf → design session with Matt; knight-rider for sequencing). A DRAFT for the session to react to, not a locked ruling. The session rules; the output becomes canonical.
**Date:** 2026-06-19
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-authorized Pattern-B dialogue (2026-06-18→19) that began on the caster-Lever-C park and opened into a re-architecture of the battle-sim's combat-efficacy MEASUREMENT layer. Matt approved authoring this spine ("ok") to seed the session. Locates + frames + drafts; the doctrine DECISION and the Model-A-vs-B call remain RESERVED FOR MATT.

**Supersedes / reconciles:**
- `agentic_orchestration/gandalf/notes/2026-06-18-caster-upper-tier-crater-disposition.md` — its caster-composition-crater finding does NOT reproduce in production (§5 below). The caster-pointed Lever-C probe it recommended is DISSOLVED. Its boss-bridge family roster is REVISED.

**Evidence (read/reproduced first-hand 2026-06-19, not taken on report):**
- Production season-001 run: `agentic_orchestration/cycle-14-wave-5-season-001/phase3_gauntlet_results.json` (66 kit_results, 3762 encounter_results). Boss-throughput-by-attribute reproduced here (§5 table); n=792 boss-scenario rows.
- Scenario shells: `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` (win_condition per shell; MOB_HP 1.5× anchor on open_arena + chokepoint).
- Ship-record DB: `agentic_orchestration/cycle-14-wave-5-season-001/kit_archive.db` (no modifier column anywhere; band-select is the ship gate).
- Legolas Mode-A research (returned 2026-06-19): "ARPG Combat Efficacy Measurement" — folded in §8. Sources: Maxroll/Icy-Veins (D3 GRift, D4 Pit), PoE wiki/Switchblade (PoE2), Last Epoch, Grim Dawn, Lost Ark LOA-logs.
- Predecessor's contradicting code citation: `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py:16-17,125-138` (boss-only gating) vs production metadata `eligible_encounter_types` = all six — flagged §7.

---

## 0. One line

**Measurement follows win condition. Clear rooms (`all_mobs_killed`) are throughput problems → a cohort-relative KPM band with a floor AND a ceiling gates them. Boss rooms (`*_killed`) are payoff moments → a binary survive-and-kill-within-the-enrage-timer gates them, and DPS/TTK is MEASURED but never gates. The single global KPM band applied uniformly across all six shells is the bug: it blocks every boss encounter (competent and incompetent identically), because a clear-room band calibrated near ~264 kpm cannot be met by a boss room whose natural kill-rate is ~30 kpm. The genre confirms every load-bearing piece of this (§8); production data confirms the diagnosis and refutes the prior caster-crater framing (§5).**

---

## 1. The doctrine table (the core deliverable)

| Room class | shells | `win_condition` | what over-performance MEANS | GATE (ships/rejects) | MEASURE (recorded, never rejects) |
|---|---|---|---|---|---|
| **Clear rooms** | `elite_pack`, `magic_pack`, `open_arena`, `chokepoint_corridor` | `all_mobs_killed` | pacing / economy DEFECT — too-fast clear breaks loot + XP + difficulty pacing | **KPM band: floor + CEILING** (cohort-relative, density-aware) | per-room KPM (for tuning) |
| **Boss rooms** | `boss_with_adds`, `mini_boss` | `boss_killed` / `mini_boss_killed` (kill ONE target; adds optional) | power-fantasy PAYOFF — a fast boss kill IS the reward | **survive + kill the target within the enrage timer** (the 240s hard cap IS the enrage timer) | **DPS / TTK** (observed; informs encounter tuning; NEVER rejects a build) |

**Ship gate, restated under the doctrine:** a kit ships if it (a) lands KPM-in-band on clear rooms AND (b) survives-and-kills boss rooms within the timer. DPS is telemetry throughout. The KPM band is NEVER applied to boss rooms; the survive+kill gate is NEVER applied to clear rooms.

**Why a CEILING on clear rooms but not on boss rooms** is the whole asymmetry — §2.

---

## 2. The over-performance asymmetry principle

The two room classes are not the same kind of object, so over-performance means opposite things:

- **Clear-room over-performance is a defect.** If a kit clears `open_arena` at 3× the cohort KPM, the run paces wrong: packs evaporate before they threaten, loot/XP fire-hose, the moment-to-moment journey goes slack. This is the D3-Area-Damage trash-melt problem and the PoE map-blaster pace. It needs a CEILING — a kit that clears too fast is as out-of-band as one that clears too slow. Both ends gate.
- **Boss-room over-performance is the payoff.** If a kit kills the boss in 4 seconds, that is the player cashing the power-fantasy cheque the whole build was written to cash. Capping it would punish the exact moment the genre exists to deliver. There is NO ceiling on boss DPS. The only boss gate is binary: did you survive, and did you kill it before the enrage timer. Speed above that is reward, recorded but never penalized.

This is why DPS is **measure-only** on bosses: the genre does not have an upper bound on "too much boss damage" the way it has an upper bound on "too-fast trash clear." (Genre confirmation: §8, finding C — survival/offense on bosses is treated as a constraint-and-reward, never a scored ceiling.)

---

## 3. DPS = measurement, not gate — and the "tune the encounter, observe the player" loop

**Matt's call (load-bearing):** add DPS as a second boss KPI alongside survive/kill. It is the most canonical KPI across all of ARPG and RPG. But it is a MEASUREMENT, not a gate. It never rejects a build.

**Why measure-not-gate protects the game:**

1. **Anti-homogenization.** A DPS *gate* (minimum DPS to ship) collapses build diversity toward whatever maximizes the number — the PoE2 "5-second boss kill" monoculture Legolas flagged (finding B / the EZG source). A DPS *measurement* lets a slow-but-survivable control build and a glass burst build BOTH ship, because the gate is "can you kill it in time," not "can you kill it fast."
2. **It tunes the encounter, not the player.** This is the inverse of the dead global-modifier era. For clear rooms we select the KIT to fit the sim (band-select). For boss rooms we observe the DPS distribution and tune the ENCOUNTER (boss HP, enrage-timer length, add count) to the population — never reject a player's build for being on the slow side of viable. DPS is the telemetry that informs encounter design; it is not a verdict on the kit.
3. **It is the right instrument for ramp builds.** A continuous DPS signal sees a DoT/summoner build's *equilibrium* output. A kill-time *gate* on a short fight punishes ramp (Legolas finding B: ramp = 20–50% of a sub-15s fight; our boss KPM of 28–30 sits squarely in that danger zone). Measure-not-gate is the genre-correct protection for the proxy/DoT archetypes (§4).

**Genre precedent (Legolas §8):** Lost Ark's per-phase enrage/DPS-check is exactly "kill enough within the window or the boss enrages" — a survive-and-kill-in-time gate, not a kill-*fast* gate. Our 240s cap is that enrage timer. D3's Rift-Guardian-Killer role and PoE's Boss-Killer archetype are both measured by kill-*time* as a comparative observation, not a published threshold. We are squarely on the genre's line.

---

## 4. Proxy-attribution rule (Matt's #5) — and the measurement-vs-mechanics distinction

**The rule:** KPM and DPS count kills/damage by the player AND ALL of the player's proxies — minions, summons, totems, DoT, ailments. A kill is the player's kill regardless of which source landed the final blow. We would not discount a boss kill because a summoned skeleton struck last.

**This resolves the B4 summoner park.** B4 parked because proxy damage was invisible to KPM under a COUNT≠CONTRIBUTION cut — the summoner's army did the work but the instrument credited none of it. Under #5, proxy kills are the player's kills; the summoner's throughput becomes measurable; the park's measurement-limit dissolves. (The remaining B4 instrument question — whether summoners seat on a contribution metric vs the KPM band — is downstream of THIS doctrine, because once boss rooms measure DPS-with-proxies, the summoner's boss output is finally visible.)

**Legolas correction to my prior (Q6) — capture so it doesn't bite us later:** PoE does NOT use universal attribution. It SPLITS: proxy kills credit the player *economically* (loot, XP, flask charges) but do NOT fire most player *on-kill mechanical triggers* (life-on-kill, phasing-on-kill). Our #5 is a **measurement-attribution** rule (the kill counts toward the player's efficacy score) — and for measurement, universal attribution is the correct, clean choice. The PoE split is a **mechanics-attribution** concern (which on-kill effects fire for whom) that only becomes live when we wire actual on-kill mechanics. **Doctrine boundary:** #5 governs measurement; it does not pre-decide on-kill mechanical attribution. Two separate questions; do not let the measurement rule silently dictate the mechanics rule.

---

## 5. Reconciliation: the caster-crater finding does NOT reproduce in production

The predecessor (2026-06-18) concluded casters have a REAL, ROBUST boss-composition crater (mini_boss + boss WR = 0.0 invariant across 4 cells × 4 rungs) and recommended a caster-pointed Lever-C probe. **Production season-001 data refutes the production-level framing.**

Verified boss-scenario throughput (n=792; attribute parsed from `legendary_id`; reproduced 2026-06-19):

| attr | n | t1 kpm | t2 kpm | t2 survival | REJECT | in_band | sg BLOCK |
|---|---|---|---|---|---|---|---|
| int | 144 | 38.0 | 37.3 | **1.00** | 0% | 0% | 100% |
| wis | 360 | 36.3 | 36.1 | **1.00** | 0% | 0% | 100% |
| dex | 144 | 32.3 | 32.5 | 0.83 | 17% | 0% | 100% |
| str | 144 | 0.6 | **0.0** | **0.00** | **100%** | 0% | 100% |
| **CASTER** (int+wis) | 504 | 36.8 | **36.5** | **1.00** | 0% | 0% | 100% |
| **MARTIAL** (str+dex) | 288 | 16.4 | **16.3** | 0.42 | 58% | 0% | 100% |

**What this says:**
1. **Casters out-throughput martials 2.2× on bosses (36.5 vs 16.3) and survive perfectly (1.00 vs 0.42).** Casters are NOT the boss-cratered archetype in production.
2. **STR martials are the real boss-crater:** 0.0 kpm, die 100%, REJECT 100%. DEX is middling (0.83 survival, 17% REJECT).
3. **The predecessor's WR=0.0 came from the SYNTHETIC reshape run** (`g7-reshape-hot-caster-b6-20260615.json`) at suppressed modifiers (0.018–0.366), which deliberately manufactured a magic_pack over-clear to drag the modifier down. Its own §3 left "composition vs suppression" explicitly OPEN. **Production answers it:** at faithful power (the 2026-06-18 `apply_max_profile_investment` default-ON flip #3 — "kit power" now means FAITHFUL/geared), casters kill bosses fine. The caster crater was **suppression in a synthetic regime, not composition.**

**Consequences:**
- **The caster-pointed Lever-C probe is DISSOLVED — doubly.** (a) It pins M=1.0/M=0.30 through the DEAD converged-modifier scalar path (production ships via band-select, no modifier persisted). (b) Production at faithful power already delivers the answer the M=1.0 pin was built to find: casters kill bosses. There is nothing left for the probe to discover.
- **The boss-bridge family roster is REVISED.** Caster is REMOVED (not cratered in production). The production boss-crater is STR martial — but before naming STR a "composition gap," it must get the production re-read the caster just got (the rogue's original crater was also synthetic-regime; verify the rogue + STR craters reproduce at faithful power before treating them as composition). Keystone-ceiling stays EXCLUDED (measurement-saturation, the predecessor's correct call). **Net: the boss-bridge family is not closed, but its membership is now an open production-verification question, not a settled roster.**

---

## 6. The band-mismatch, confirmed — and where the fix actually lives

`in_band = 0%` AND `sg BLOCK = 100%` for **every attribute** on boss rooms. The competent caster (36 kpm, survives) and the dead STR (0 kpm, dies) are blocked **identically**. A clear-room KPM band (calibrated near ~264 kpm on the 8-swarm `open_arena`/`chokepoint` shells) cannot be met by a boss room whose natural kill-rate is ~30 kpm (1 target + optional adds). So the band rejects all 792 boss encounters regardless of competence. This IS the bug the doctrine fixes.

**But the survive/kill signal already EXISTS in production — it is just discarded.** `tier_1_outcome` discriminates correctly: caster PROVISIONAL_PASS (0% REJECT), STR REJECT (100%). The apparatus already measures the right thing at tier 1. The `sg_overall` band overlay (requiring clear-room `in_band`) then erases that discrimination, blocking everyone. **So the doctrine fix may be smaller than "rebuild boss measurement": on boss rooms, gate on the survive/kill signal that is already computed and DROP the `in_band` overlay; add DPS as telemetry.** Adopting the doctrine would RESTORE discrimination on bosses (casters ship, STR does not) — the concrete production payoff.

⚠️ **Verify item (gamora):** I observed the `tier_1_outcome` ↔ survive/kill correlation; I have NOT read the code that produces `tier_1_outcome`. Confirm the mechanics before treating "the signal already exists" as load-bearing.

---

## 7. Eligible-tier discrepancy — flag, do not assert

- Predecessor cites `gauntlet_sim.py:16-17,125-138`: gating = `boss_with_adds` + `mini_boss`; `swarm`/`magic_pack`/`elite_pack` BYPASSED.
- Production metadata: `eligible_encounter_types` = ALL SIX shells; per-row data shows packs carry `in_band` 13–36% and contribute to pass (i.e. packs are NOT bypassed in production).

These conflict. The production run evidence says **all-six gating**; the code citation says **boss-only**. Most likely a code-era-vs-run-era difference (a stale constant, or `gauntlet_sim.py` being a different/legacy harness than the phase3 production runner — consistent with jack-ryan's BC-Stage-3 finding that the 1D `simulate_fight` kernel was deleted and `run_spatial_fight` is the sole sim). **Route to gamora: which gating is canonical going forward?** The doctrine's diagnosis (one band wrongly applied to boss rooms) holds for production either way, but the design session should rule against the TRUE current gating, not a stale constant.

---

## 8. Legolas research fold-in — the genre's answers (with my prior corrections)

| Q | genre answer | doctrine consequence |
|---|---|---|
| **Q1** kill-RATE where it matters / where not | CONFIRMED: rate for trash/pack/clear; bosses judged on kill-TIME/DPS. D3 names a Rift-Guardian-Killer role (kill-*time*); D4 Pit boss phase = boss-kill-time; PoE Mapper vs Boss-Killer; Lost Ark per-phase DPS-checks. | The win-condition split is genre-canonical, not invented. |
| **Q2** absolute KPM target? | CONFIRMED none. Always comparative (build-vs-build, league-vs-league, layout-vs-layout). PoE2 community DPS *floors* (200K/500K/1M) exist but are DPS-not-KPM and community-derived, not dev-published. | Our cohort-RELATIVE band is right in kind. Do NOT chase an absolute KPM number. |
| **Q3** KPM bucketed by room type? | No headline numeric KPM-per-room-type anywhere. BUT de-facto per-layout/density TIERING is real (PoE/PoE2 map tier lists; D3 23-monster-set density ranking). PoE2 makes "boss skippability" a first-class axis. D3 GRift EXCLUDES the boss room from density optimization (all trash despawns at 100%). | **Model A (per-room bands)** has genre support as TIERING, not as a published per-room KPM number. Build it as cohort-relative per-shell bands, not absolute targets. |
| **Q4** density comparison normalized or raw? | CONFIRMED raw clear-time per FIXED UNIT (rift/tier/map/echo), not per-enemy normalized. | If we band per-room, band on raw room-clear, NOT per-enemy. |
| **Q5** include travel/downtime? | CONFIRMED whole-run elapsed, travel INCLUDED. Movement speed is a first-class lever ("almost required" boots). | **Model B (session-wide clear-speed incl. walk time) is THE genre-canonical frame.** Major input to the Model-A-vs-B call (§9). |
| **Q6** proxy kill attribution | PARTIALLY WRONG (my prior). PoE SPLITS: economic credit (loot/XP/flask) universal to player; most on-kill triggers (life-on-kill, phasing) do NOT fire for player on proxy kills. D3/D4/GD/LE ~player-attributed for most purposes. | #5 holds for MEASUREMENT; the split is a MECHANICS question (§4 boundary). |

**Bonus findings (not asked, load-bearing):**
- **(A) Lost Ark enrage/phase DPS-check** = the genre precedent for our survive-and-kill-in-timer gate. The 240s cap = the enrage timer. Validates the gate model over raw kill-time.
- **(B) DoT/summoner ramp penalty on short bosses** is a GENRE-RECOGNIZED weakness (PoE2 higher boss ailment thresholds; D3's first-6-seconds damage reduction vs pre-stacking). Ramp = 20–50% of a sub-15s fight. **Our boss KPM 28–30 is in the danger zone** — strongest third-party case for DPS-as-continuous-measure over kill-time-gate, and a flag that the proxy/DoT archetypes need the measure-not-gate protection most.
- **(C) Survival is a CONSTRAINT, not a scored dimension** anywhere in the genre. Validates survive+kill as a binary gate with no defensive *score*.
- **(D) D3 group GRift formalized 4 roles** (Speed/DPS/Rift-Guardian-Killer/Support) — the most explicit encounter-type-bucketed measurement in the genre. Solo collapses to one character, but the trash-throughput-vs-boss-kill-time dichotomy is structurally exactly what this doctrine encodes.

---

## 9. Open decisions for the design session (RESERVED for Matt)

1. **Adopt the doctrine table (§1)?** Win-condition split; clear rooms = KPM band (floor+ceiling); boss rooms = survive+kill gate + DPS measure-only. (My recommend: yes — production-confirmed bug, genre-confirmed fix.)
2. **Model A vs Model B for clear-room measurement:**
   - **Model A — per-room (per-shell) cohort-relative KPM bands.** Genre support as density TIERING (Q3). Density-aware: open_arena/chokepoint (8-swarm) naturally band higher than packs. Lower sim-structure change.
   - **Model B — session-wide clear-speed including travel/walk time between encounters.** The genre-CANONICAL frame (Q5). Higher fidelity to how the genre actually measures. BUT a sim-structure change (the sim must model inter-encounter travel; movement speed becomes a first-class measured lever). Flagged as the larger build.
   - Not mutually exclusive — Model A could be the near-term per-room banding while Model B is the longer-arc session-wide frame. The session should rule the sequencing.
3. **Boss-bridge family — re-verify membership at faithful power** before any fix. Caster is out (production). Re-read the rogue + STR craters at faithful power (the rogue crater was also synthetic-regime). One doctrine, N instances — but N is now an open production question, not a settled 3.
4. **`tier_1_outcome` mechanics (gamora verify, §6)** and **canonical gating tier-set (gamora verify, §7)** — both gate the precision of the doctrine's implementation, not its direction.

**Park dispositions carried/updated:**
- caster-Lever-C probe → DISSOLVED (§5).
- B4 summoner → measurement-limit RESOLVED by #5 (§4); residual instrument-seating question downstream of this doctrine.
- keystone-ceiling → stays EXCLUDED (measurement-saturation); re-engages when open_arena de-saturates off the 1.000 WR ceiling.

---

## 10. Player consequence (the anchor)

Under the broken band, a player who builds a competent caster kills the boss in 36-kpm style and *still sees the build rejected* — blocked by the same gate that rejects the STR build that died without landing a hit. The instrument cannot tell mastery from failure at the one moment the player most wants to be told. And a player who builds a slow, survivable control or summoner kit — the genre's legitimate "outlast the boss" fantasy — would, under a DPS *gate*, be told their build is illegitimate for not killing fast enough.

The doctrine fixes both. Survive-and-kill-in-time honors every build that can actually win — the burst caster AND the patient summoner. DPS-as-measurement lets the burst build SEE its 4-second kill as the payoff it is, without forcing the summoner to match it. Clear-room ceilings keep the journey-pacing intact so the trash never goes slack. **The promise is "your build, played with intent, can win the fight its own way" — and the measurement, finally, says yes to exactly the builds that deliver on that promise.** That is the substance of power, not its performance — the journey this seat exists to keep honest.

---

**Signed:** gandalf, 2026-06-19. A spine for the encounter-measurement design session — the doctrine table, the over-performance asymmetry, DPS-measure-not-gate with the tune-the-encounter/observe-the-player loop, the proxy-attribution rule with its measurement-vs-mechanics boundary, the production-data reconciliation that dissolves the caster-crater framing and the caster-Lever-C probe, the band-mismatch confirmation with the smaller-than-expected fix location, two gamora verify-items, and the Model-A-vs-B call left open for Matt.
