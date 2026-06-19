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

## ⚠️ GATE-1 VERIFICATION ADDENDUM (2026-06-19, post-draft, FIRST-HAND code trace)

Before this spine reaches a design session I verified its flagged-but-unread load-bearing claims directly against the gate code (`gauntlet_sim.py`, `t4_sim_cycling.py`). **Three of the spine's own claims were OVERTURNED. The doctrine direction (§1–§4, §8–§10) SURVIVES and SHARPENS; the diagnosis of "what is wired today" was wrong.**

1. **"Single global KPM band across all six shells" (§0, §1, §6) — FALSE.** Per-encounter-type bands already exist and already SHIP. The ship gate is `season_emit → gauntlet_pass → eligible_encounters_passed`, which counts `tier_2_kpm` inside `ENCOUNTER_COHORT_KPM_BAND[enc_type][cohort]` (gauntlet_sim.py:582-592, 636) — a 6-shell × 4-cohort table, Stage-2d-recalibrated to mobs/min (2026-06-16). Per-room banding is not the unbuilt fix; it is live.

2. **"The survive/kill signal already lives in `tier_1_outcome`" (§6) — FALSE.** `tier_1_outcome` is a KPM quick-estimate routing flag (REJECT / PROVISIONAL_PASS / BORDERLINE). Survival is a SEPARATE subgate, sg2, and it is **telemetry-only** — explicitly excluded from `in_band` and from the pass criterion (gauntlet_sim.py:1069 comment "survival sub-gate (sg2)... preserved unchanged. Only sg1 (KPM in-band) is enriched"; sg2 increments a counter at :1080-1081 and feeds nothing that ships). Survival never gates anything, for any shell. `sg2_fail_count = 0` in the artifact means the survival floor never fired — not that everything survived.

3. **"STR is the real boss-crater — 0.0 kpm, dies 100%" (§5) — FALSE framing.** `tier_2_survival_rate = 0.0` on STR boss rows is a DEFAULT, not a measured death: tier_2 only runs when `tier_1_outcome != REJECT` (t4_sim_cycling.py:1452), and STR boss rows are REJECT at tier_1, so tier_2 never ran. The `t2_kpm = 0.0` is the same default. STR is **tier_1-KPM-rejected** on bosses; whether STR could survive-and-kill the boss was **never tested**. The artifact cannot distinguish death from under-damage.

**The sharpened diagnosis (better than the draft):** bosses ARE still KPM-gated — by their OWN narrow band (`boss_with_adds` (2.49, 3.78), `mini_boss` (0.57, 3.30) mobs/min) WITH a hard p90 ceiling. The doctrine says bosses should be survive-and-kill-gated, DPS measured, NO over-performance ceiling. The code comment already names that intent — `gauntlet_sim.py:357` "boss/mini: SURV-judged, KPM a wide sanity rail" — but the code does the opposite (narrow ceiling, survival inert). **The doctrine's central move is UNBUILT, not already-built.** And the broken KPM-on-boss gate does worse than mis-measure: by REJECTing low-KPM boss attempts at tier_1, it PREVENTS the survive+kill measurement (tier_2) from ever running — it manufactures a fake "STR boss-crater" by refusing to test the one thing that would clear or condemn it.

**Two co-existing in-band definitions (measurement-hygiene hazard).** The serialized row `in_band` field = `get_archetype_cohort_kpm_band` → `_ARCHETYPE_COHORT_KPM_BAND` is `None` by default (gauntlet_sim.py:1500) → falls back to `COHORT_KPM_BAND[cohort]` (t4_sim_cycling.py:117, a single per-cohort band in the OLD 52–97 KPM scale). The SHIP gate uses a different band (`ENCOUNTER_COHORT_KPM_BAND`, per-shell, mobs/min). They disagree 8× on the same rows (row `in_band` 427 vs metadata `eligible_encounters_in_band` 3285). **Both the predecessor's analysis and this spine's §5/§6 read the NON-shipping field.** The serialized `in_band` is not what ships kits.

**Substrate caveat (load-bearing for the session):** the phase3 artifact is REGIME-MIXED — its metadata block and its per-row block were written under different KPM scales/runs (per-shell `within_current_band = 0.00` for all six shells; row vs metadata in-band disagree 8×). §5's numbers therefore cannot carry empirical weight. **A clean current-regime gauntlet run (current mobs/min bands, all six shells, faithful power) is the precondition for ANY boss-crater number** (caster-vs-STR, death-vs-under-damage). The doctrine can be ADOPTED on direction now; the per-archetype boss claims must wait for clean data.

The sections below are corrected inline where they stated an overturned claim; the doctrine table (§1), asymmetry (§2), DPS-measure-not-gate (§3), proxy rule (§4), Legolas fold-in (§8), open decisions (§9), and player consequence (§10) stand.

---

## 0. One line

**Measurement follows win condition. Clear rooms (`all_mobs_killed`) are throughput problems → a cohort-relative KPM band with a floor AND a ceiling gates them. Boss rooms (`*_killed`) are payoff moments → a binary survive-and-kill-within-the-enrage-timer gates them, and DPS/TTK is MEASURED but never gates. The bug is NOT one global band (Gate 1 refuted that — per-shell bands already exist and ship via `eligible_encounters_passed`); the bug is that boss rooms are KPM-gated AT ALL — by a narrow per-boss band with a hard p90 ceiling (`boss_with_adds` 2.49–3.78 mobs/min) — when the doctrine says they should be survive-and-kill-gated with DPS measured and NO over-performance ceiling. The code already names this intent (`gauntlet_sim.py:357` "boss/mini: SURV-judged, KPM a wide sanity rail") but the code does the opposite, and survival is wired as telemetry that gates nothing. The doctrine's central move is therefore UNBUILT, not already-built. The genre confirms every load-bearing piece (§8).**

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

> **⚠️ GATE-1 SUBSTRATE CAVEAT (read before trusting this table):** the artifact this table is drawn from is REGIME-MIXED (metadata + rows written under different KPM scales — see addendum). The `t2 kpm` and `t2 survival` columns are unreliable for REJECTed rows, where both are tier_2-never-ran DEFAULTS (0.0), not measurements. The only solid signals here are the tier_1 REJECT rates and the directional caster-vs-martial split. Absolute KPM magnitudes are old-scale. Treat this as a hypothesis to re-measure on a clean run, NOT as settled per-archetype boss data.

Verified boss-scenario throughput (n=792; attribute parsed from `legendary_id`; reproduced 2026-06-19):

| attr | n | t1 kpm | t2 kpm | t2 survival | REJECT | in_band | sg BLOCK |
|---|---|---|---|---|---|---|---|
| int | 144 | 38.0 | 37.3 | **1.00** | 0% | 0% | 100% |
| wis | 360 | 36.3 | 36.1 | **1.00** | 0% | 0% | 100% |
| dex | 144 | 32.3 | 32.5 | 0.83 | 17% | 0% | 100% |
| str | 144 | 0.6 | **0.0** | **0.00** | **100%** | 0% | 100% |
| **CASTER** (int+wis) | 504 | 36.8 | **36.5** | **1.00** | 0% | 0% | 100% |
| **MARTIAL** (str+dex) | 288 | 16.4 | **16.3** | 0.42 | 58% | 0% | 100% |

**What this says (CORRECTED post-Gate-1):**
1. **Casters pass tier_1 (0% REJECT) and survive the tier_2 they actually run (survival 1.00 is REAL — tier_2 ran).** Casters are NOT the boss-cratered archetype. This holds.
2. **STR is tier_1-KPM-REJECTED 100% on bosses — NOT "dies 100%".** The 0.0 t2-kpm and 0.00 survival are tier_2-never-ran defaults (REJECT short-circuits tier_2; t4_sim_cycling.py:1452), not measured death. Whether STR could survive-and-kill the boss was never tested — the KPM gate rejected it before the survive+kill measurement could run. The "martial survival 0.42" average is itself a blend of DEX (tier_2 ran, ~real) and STR (default 0.00), so it overstates a crater that may be a measurement artifact. **Under the doctrine, STR's low boss-KPM is exactly the legitimate slow-survivable boss kill the KPM ceiling wrongly condemns — we cannot know which until bosses are survive+kill-gated and tier_2 runs.**
3. **The predecessor's WR=0.0 came from the SYNTHETIC reshape run** (`g7-reshape-hot-caster-b6-20260615.json`) at suppressed modifiers (0.018–0.366), which deliberately manufactured a magic_pack over-clear to drag the modifier down. Its own §3 left "composition vs suppression" explicitly OPEN. **Production answers it:** at faithful power (the 2026-06-18 `apply_max_profile_investment` default-ON flip #3 — "kit power" now means FAITHFUL/geared), casters kill bosses fine. The caster crater was **suppression in a synthetic regime, not composition.**

**Consequences:**
- **The caster-pointed Lever-C probe is DISSOLVED — doubly.** (a) It pins M=1.0/M=0.30 through the DEAD converged-modifier scalar path (production ships via band-select, no modifier persisted). (b) Production at faithful power already delivers the answer the M=1.0 pin was built to find: casters kill bosses. There is nothing left for the probe to discover.
- **The boss-bridge family roster is REVISED.** Caster is REMOVED (not cratered in production). The production boss-crater is STR martial — but before naming STR a "composition gap," it must get the production re-read the caster just got (the rogue's original crater was also synthetic-regime; verify the rogue + STR craters reproduce at faithful power before treating them as composition). Keystone-ceiling stays EXCLUDED (measurement-saturation, the predecessor's correct call). **Net: the boss-bridge family is not closed, but its membership is now an open production-verification question, not a settled roster.**

---

## 6. Where the fix actually lives (CORRECTED post-Gate-1)

The draft put the bug at "one global band wrongly applied to bosses" and claimed the survive/kill signal already lived in `tier_1_outcome`. Gate 1 refuted both. The corrected location:

**Bosses are KPM-gated at TWO points, both KPM, neither survival:**
1. **tier_1 routing** — a quick KPM estimate routes each encounter REJECT / PROVISIONAL_PASS / BORDERLINE. A REJECT short-circuits tier_2 entirely (t4_sim_cycling.py:1452). STR boss rows REJECT here on low KPM, so their survive+kill is never simulated.
2. **tier_2 in-band / ship gate** — `eligible_encounters_passed` counts `tier_2_kpm` inside `ENCOUNTER_COHORT_KPM_BAND[boss_with_adds]` = (2.49, 3.78) mobs/min (gauntlet_sim.py:582-592). A boss-melt above 3.78 mobs/min fails the SHIP gate even with the p90-hi tail — the over-performance ceiling the doctrine forbids on bosses.

**Survival (sg2) gates NOTHING.** It is computed (`SURVIVAL_FLOOR_BY_COHORT`, t4_sim_cycling.py:811-815) and counted (`sg2_fail_count`, gauntlet_sim.py:1080-1081), but it is explicitly excluded from `in_band` and from `gauntlet_pass` (line 1069 comment: "Only sg1 (KPM in-band) is enriched"). The survive/kill signal the doctrine wants as the boss GATE is not "already computed and discarded" — it exists as telemetry and was never wired to gate.

**So the fix is real work, not a one-line overlay-drop:** on boss shells, (a) tier_1 must stop KPM-REJECTing — route boss rooms to tier_2 unconditionally (or on a wide sanity rail) so survive+kill can actually be measured; (b) the tier_2 ship gate must read sg2 (survive within the 240s enrage timer + target killed), not the narrow KPM band; (c) DPS/TTK becomes recorded telemetry. The oracle comment (gauntlet_sim.py:357) already specifies (b) as intent — it is unimplemented. **The concrete production payoff still stands and sharpens: the current gate manufactures a fake STR boss-crater by KPM-rejecting STR before survive+kill is ever tested. Adopting the doctrine would let STR's boss attempts run and reveal whether they are legitimate slow-survivable kills or genuine failures — a question the current instrument structurally cannot answer.**

✅ **Gate-1 verified (supersedes the draft's gamora verify-item):** `tier_1_outcome` is a KPM quick-estimate routing flag, not a survive/kill signal; survival is sg2 telemetry-only; per-shell bands (`ENCOUNTER_COHORT_KPM_BAND`) are the live ship gate; a second, non-shipping per-cohort band (`COHORT_KPM_BAND` via the uninstalled `get_archetype_cohort_kpm_band` fallback) populates the misleading serialized `in_band` field. No outstanding gamora code-read remains for §6.

---

## 7. Eligible-tier discrepancy — RESOLVED (Gate-1)

The conflict is resolved in favor of **all-six gating**. The predecessor cited a SUPERSEDED constant:
- `GAUNTLET_ELIGIBLE_ENCOUNTER_TYPES_C14V1 = {boss_with_adds, mini_boss}` (gauntlet_sim.py:131-134) and `GAUNTLET_ELIGIBLE_PASS_FLOOR_C14V1 = 2` (:144) are HISTORICAL — the Cycle-14-v1 boss-only stratified floor.
- They were retracted by **W-α6** (Matt 2026-05-28 Gate-7 D1 ratification): the live criterion is `gauntlet_pass = eligible_encounters_passed(cohort) >= GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6 (=9)` over ALL SIX shells, in-band via `ENCOUNTER_COHORT_KPM_BAND` (gauntlet_sim.py:562-636; docstring §7.3 semantic-shift declaration).

So the production metadata (`eligible_encounter_types` = all six) is canonical; the boss-only constant is dead code the predecessor read as live. No gamora routing needed. The design session rules against all-six per-shell KPM gating — which is precisely the gating the doctrine reshapes (clear shells keep their band; boss shells move off KPM onto survive+kill).

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
4. **~~`tier_1_outcome` mechanics + gating tier-set (gamora verify)~~ — RESOLVED by Gate-1** (§6, §7). Replaced by ONE new precondition: **authorize a clean current-regime gauntlet run** (current mobs/min `ENCOUNTER_COHORT_KPM_BAND`, all six shells, faithful power) before the per-archetype boss claims (§5) are treated as data. The phase3 artifact is regime-mixed; the doctrine can be adopted on direction without it, but the boss-bridge membership question (§9.3) cannot be settled until clean boss-room data exists.

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
