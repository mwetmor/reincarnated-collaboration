# Encounter-measurement doctrine — design-session spine

**Type:** design-note spine (gandalf → design session with Matt; knight-rider for sequencing). A DRAFT for the session to react to, not a locked ruling. The session rules; the output becomes canonical.
**Date:** 2026-06-19
**Author:** gandalf (story-and-design steward)
**Authority:** Matt-authorized Pattern-B dialogue (2026-06-18→19) that began on the caster-Lever-C park and opened into a re-architecture of the battle-sim's combat-efficacy MEASUREMENT layer. Matt approved authoring this spine ("ok") to seed the session. Locates + frames + drafts; the doctrine DECISION and the Model-A-vs-B call remain RESERVED FOR MATT.

**Supersedes / reconciles:**
- `agentic_orchestration/gandalf/notes/2026-06-18-caster-upper-tier-crater-disposition.md` — its caster-composition-crater finding does NOT reproduce in production (§5 below). The caster-pointed Lever-C probe it recommended is DISSOLVED. Its boss-bridge family roster is REVISED.

**Evidence (read/reproduced first-hand 2026-06-19, not taken on report):**
- Production season-001 run: `agentic_orchestration/cycle-14-wave-5-season-001/phase3_gauntlet_results.json` (66 kit_results, 3762 encounter_results). Used for the regime-mixed read the GATE-1 addendum overturns; SUPERSEDED for boss numbers by the clean run below.
- **Clean boss run (2026-06-19) — the boss-throughput basis for §5:** `agentic_orchestration/cycle-14-wave-5-season-001/clean-boss-numbers-harness-2026-06-19.json` (21,120 fights, faithful power, single regime; gamora `clean_boss_numbers_harness_2026_06_19.py`). Verified jack-ryan Gate-2 PASS-WITH-INFO (`agentic_orchestration/qa/findings/2026-06-19-gamora-clean-boss-numbers-harness-gate2.md`).
- Scenario shells: `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/arena.py` (win_condition per shell; MOB_HP 1.5× anchor on open_arena + chokepoint).
- Ship-record DB: `agentic_orchestration/cycle-14-wave-5-season-001/kit_archive.db` (no modifier column anywhere; band-select is the ship gate).
- Legolas Mode-A research (returned 2026-06-19): "ARPG Combat Efficacy Measurement" — folded in §8. Sources: Maxroll/Icy-Veins (D3 GRift, D4 Pit), PoE wiki/Switchblade (PoE2), Last Epoch, Grim Dawn, Lost Ark LOA-logs.
- Predecessor's contradicting code citation: `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py:16-17,125-138` (boss-only gating) vs production metadata `eligible_encounter_types` = all six — flagged §7.

---

## ⚠️ GATE-1 VERIFICATION ADDENDUM (2026-06-19, post-draft, FIRST-HAND code trace)

Before this spine reaches a design session I verified its flagged-but-unread load-bearing claims directly against the gate code (`gauntlet_sim.py`, `t4_sim_cycling.py`). **Three of the spine's own claims were OVERTURNED. The doctrine direction (§1–§4, §8–§10) SURVIVES and SHARPENS; the diagnosis of "what is wired today" was wrong.**

1. **"Single global KPM band across all six shells" (§0, §1, §6) — FALSE.** Per-encounter-type bands already exist and already SHIP. The ship gate is `season_emit → gauntlet_pass → eligible_encounters_passed`, which counts `tier_2_kpm` inside `ENCOUNTER_COHORT_KPM_BAND[enc_type][cohort]` (gauntlet_sim.py:582-592, 636) — a 6-shell × 4-cohort table, Stage-2d-recalibrated to mobs/min (2026-06-16). Per-room banding is not the unbuilt fix; it is live.

2. **"The survive/kill signal already lives in `tier_1_outcome`" (§6) — FALSE.** `tier_1_outcome` is a KPM quick-estimate routing flag (REJECT / PROVISIONAL_PASS / BORDERLINE). Survival is a SEPARATE subgate, sg2, and it is **telemetry-only** — explicitly excluded from `in_band` and from the pass criterion (gauntlet_sim.py:1069 comment "survival sub-gate (sg2)... preserved unchanged. Only sg1 (KPM in-band) is enriched"; sg2 increments a counter at :1080-1081 and feeds nothing that ships). Survival never gates anything, for any shell. `sg2_fail_count = 0` in the artifact means the survival floor never fired — not that everything survived.

3. **"STR is the real boss-crater — 0.0 kpm, dies 100%" (§5) — FALSE framing.** `tier_2_survival_rate = 0.0` on STR boss rows is a DEFAULT, not a measured death: tier_2 only runs when `tier_1_outcome != REJECT` (gauntlet_sim.py:1019), and STR boss rows are REJECT at tier_1, so tier_2 never ran. The `t2_kpm = 0.0` is the same default. STR is **tier_1-KPM-rejected** on bosses; whether STR could survive-and-kill the boss was **never tested**. The artifact cannot distinguish death from under-damage.

**The sharpened diagnosis (better than the draft):** bosses ARE still KPM-gated — by their OWN narrow band (`boss_with_adds` (2.49, 3.78), `mini_boss` (0.57, 3.30) mobs/min) WITH a hard p90 ceiling. The doctrine says bosses should be survive-and-kill-gated, DPS measured, NO over-performance ceiling. The code comment already names that intent — `gauntlet_sim.py:357` "boss/mini: SURV-judged, KPM a wide sanity rail" — but the code does the opposite (narrow ceiling, survival inert). **The doctrine's central move is UNBUILT, not already-built.** And the broken KPM-on-boss gate does worse than mis-measure: by REJECTing low-KPM boss attempts at tier_1, it PREVENTS the survive+kill measurement (tier_2) from ever running — it manufactures a fake "STR boss-crater" by refusing to test the one thing that would clear or condemn it.

**Two co-existing in-band definitions (measurement-hygiene hazard).** The serialized row `in_band` field = `get_archetype_cohort_kpm_band` → `_ARCHETYPE_COHORT_KPM_BAND` is `None` by default (gauntlet_sim.py:1500) → falls back to `COHORT_KPM_BAND[cohort]` (t4_sim_cycling.py:117, a single per-cohort band in the OLD 52–97 KPM scale). The SHIP gate uses a different band (`ENCOUNTER_COHORT_KPM_BAND`, per-shell, mobs/min). They disagree 8× on the same rows (row `in_band` 427 vs metadata `eligible_encounters_in_band` 3285). **Both the predecessor's analysis and this spine's §5/§6 read the NON-shipping field.** The serialized `in_band` is not what ships kits.

**Substrate caveat (load-bearing for the session):** the phase3 artifact is REGIME-MIXED — its metadata block and its per-row block were written under different KPM scales/runs (per-shell `within_current_band = 0.00` for all six shells; row vs metadata in-band disagree 8×). §5's numbers therefore cannot carry empirical weight. **A clean current-regime gauntlet run (current mobs/min bands, all six shells, faithful power) is the precondition for ANY boss-crater number** (caster-vs-STR, death-vs-under-damage). The doctrine can be ADOPTED on direction now; the per-archetype boss claims must wait for clean data. **[UPDATE 2026-06-19 — RESOLVED: the clean boss run landed and passed jack-ryan Gate-2 (PASS-WITH-INFO). §5 now carries the clean per-archetype boss data; the regime-mixed table is superseded. This caveat is closed.]**

The sections below are corrected inline where they stated an overturned claim; the doctrine table (§1), asymmetry (§2), DPS-measure-not-gate (§3), proxy rule (§4), Legolas fold-in (§8), open decisions (§9), and player consequence (§10) stand.

---

## 0. One line

**Measurement follows win condition. Clear rooms (`all_mobs_killed`) are throughput problems → a cohort-relative KPM band with a floor AND a ceiling gates them. Boss rooms (`*_killed`) are payoff moments → a binary survive-and-kill-within-the-enrage-timer gates them, and DPS/TTK is MEASURED but never gates. The bug is NOT one global band (Gate 1 refuted that — per-shell bands already exist and ship via `eligible_encounters_passed`); the bug is that boss rooms are KPM-gated AT ALL — by a narrow per-boss band with a hard p90 ceiling (`boss_with_adds` 2.49–3.78 mobs/min) — when the doctrine says they should be survive-and-kill-gated with DPS measured and NO over-performance ceiling. The code already names this intent (`gauntlet_sim.py:357` "boss/mini: SURV-judged, KPM a wide sanity rail") but the code does the opposite, and survival is wired as telemetry that gates nothing. The doctrine's central move is therefore UNBUILT, not already-built. The genre confirms every load-bearing piece (§8).**

---

## ⚖️ RULINGS (Matt, 2026-06-19) — the doctrine is ADOPTED

The design session ruled. On these points the spine is no longer a draft:

1. **Doctrine table (§1) — ADOPTED.** The win-condition split is canonical: clear rooms → KPM band (floor + ceiling); boss rooms → survive-and-kill-within-the-enrage-timer (binary gate), DPS/TTK MEASURED but never gating, NO over-performance ceiling. → knight-rider drafts the decisions-log entry; jack-ryan reviews.
2. **STR cheap pre-step (rocket kit-check) — SKIPPED.** Matt fast-tracked straight to the DPS build to inspect STR's cause directly.
3. **DPS measurement build (Matt #8) — BUILD ASAP.** Brief: `gandalf/requests/2026-06-19-dps-measurement-build-brief.md`. Surfaces player + all-proxy damage from `SpatialFightResult`; classifies STR (slow-but-real vs degenerate); becomes the doctrine's permanent boss MEASURE. gamora building; jack-ryan Gate-2 (semantic-shift declaration for the new field).
4. **Boss-gate implementation (§6) — AGREED.** Re-route bosses off KPM at both tiers onto survive+kill; wire sg2 as the GATE (not telemetry); record DPS/TTK. Real engine build; knight-rider sequences (composes with / follows the DPS build).

**Still OPEN (NOT ruled):** §9.2 Model-A-vs-B for clear-room measurement; STR's *final* disposition (blocked on the DPS build output); the rogue crater re-read at faithful power.

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

**Empirically confirmed (clean run, §5):** `a_dead = 0.000` across all 21,120 boss fights at faithful power — survival is never the binding boss constraint, so the gate reduces in practice to kill-before-enrage. The kill-time FLOOR binds (STR fails it: timeout=1.000); the ABSENT ceiling is correct (caster KPM medians 3.70/3.43 already sit at/above the 3.78 boss band hi — a ceiling would clip the payoff). The asymmetry is now measured, not just argued.

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

## 5. Reconciliation — the clean boss run (2026-06-19): caster crater DISSOLVED, STR crater RECLASSIFIED

**This section now rests on clean data.** The regime-mixed phase3 table that stood here (and that the predecessor read) is SUPERSEDED — see the GATE-1 addendum for why it could not carry weight. A clean current-regime run was authorized ("let's run real boss numbers", Matt 2026-06-19), executed by gamora (`clean_boss_numbers_harness_2026_06_19.py`), and independently verified by jack-ryan Gate-2 (**PASS-WITH-INFO**, `qa/findings/2026-06-19-gamora-clean-boss-numbers-harness-gate2.md`). It drives `w4g2_tier_2_full_sim` directly on the two boss shells, BYPASSING the tier_1 KPM-REJECT that previously prevented survive+kill from ever being simulated. 21,120 fights, faithful power (max-profile investment), single regime. All four verify-gates confirmed first-hand (V1 winner = survive-AND-kill, V2 240s enrage cap, V3 faithful power, V4 proxy-inclusive kills); V1 reproduced as a data invariant across all 1,056 cells (0 violations).

**Clean boss-shell table** (survive+kill = `winner=="player"` = boss dead AND player alive; pooled across both boss shells; attribute parsed from `legendary_id`):

| attr | survive+kill | a_dead (died) | timeout | TTK_med (wins) | KPM_med |
|---|---|---|---|---|---|
| int | 0.992 | **0.000** | 0.008 | 33.2s | 3.70 |
| wis | 0.984 | **0.000** | 0.016 | 35.2s | 3.43 |
| dex | 0.786 | **0.000** | 0.213 | 34.6s | 3.15 |
| str | **0.000** | **0.000** | **1.000** | n/a | 0.25 |

By cohort: all four cohorts ≈0.77 survive+kill, `a_dead = 0.000` uniformly. STR = 0.000 on BOTH boss shells (timeout 1.000); dex|mini_boss drops to 0.646.

**What this says (clean data):**

1. **The caster crater is DISSOLVED — on clean data, not inference.** int/wis survive+kill ≈ 0.99 at faithful power. The predecessor's caster WR=0.0 was suppression in the synthetic reshape regime (`g7-reshape-hot-caster-b6-20260615.json`, modifiers 0.018–0.366), NOT composition — production at faithful power kills bosses fine. The caster-pointed Lever-C probe stays DISSOLVED.

2. **The STR crater is RECLASSIFIED, not dismissed.** The DEFENSIVE crater is DISPROVEN: `a_dead = 0.000` across all 21,120 fights — STR never dies to the boss. But STR fails the doctrine's OWN gate: `timeout = 1.000` — it never kills the boss inside the 240s enrage timer, on either shell, in any cohort. **Removing the wrongful KPM ceiling does NOT make STR ship.** The dev framing ("STR crater is not real, just a KPM-reject artifact") and the Gate-2 framing ("the legitimate slow boss-kill") both lean too far toward "STR is fine": with timeout=1.000 there is no kill at all, slow or otherwise. The KPM-reject WAS happening AND a real boss failure sits underneath it; both are true.

3. **The cause is undeterminable from THIS run — and that is itself a finding.** STR's failure is one of: **(a)** chips the boss but too slowly (real throughput-vs-enrage shortfall → kit-efficacy or encounter-tuning), or **(b)** barely damages the boss (kit-construction degeneracy → fix the population). The disambiguating signal is boss-HP-removed-in-240s = the dropped `player_damage_dealt` field. **STR's disposition is therefore BLOCKED on the Tier-B DPS-measure build (Matt #8)** — #8 is not a "nice second KPI," it is the instrument required to even classify this failure. The 0.25 KPM is NOT independent evidence: on a single-boss shell, no-kill ⇒ ≈no mob-deaths ⇒ ≈0 KPM, so it is circular with timeout=1.000, not a second data point.

4. **`a_dead = 0.000` EVERYWHERE is the doctrine-shaping surprise.** Not one archetype, not one cohort, dies to a boss at faithful power. The "survive" half of survive-and-kill is FREE. The boss gate collapses, in practice, to "kill it before the 240s enrage" — a pure TTK-vs-timer question. This is the Diablo III Greater-Rift-timer pattern exactly: tanky builds survive forever but cannot beat the clock. It VINDICATES the §2 asymmetry empirically (a kill-time FLOOR binds; a kill-time CEILING would wrongly clip) and SHARPENS it (the boss gate IS a kill-before-enrage gate; survival is inert at faithful power).

5. **The throughput gradient is clean and monotone:** int 0.992 → wis 0.984 → dex 0.786 → str 0.000. STR is the FLOOR of a throughput spectrum, not a unique break; dex is the intermediate case (timeout 0.213, mini_boss 0.646 — a thin margin, not a crater). The whole spectrum is defense-free (a_dead=0 throughout), which strengthens the read that the binding boss constraint is throughput, not survivability.

6. **The over-performance ceiling EMPIRICALLY bites casters.** int KPM_med 3.70 and wis 3.43 sit at/above the `boss_with_adds` band hi of 3.78 mobs/min — the upper half of caster boss kills is clipped by the existing KPM ceiling RIGHT NOW. Removing the boss KPM ceiling is not a theoretical fix; it recovers caster power-fantasy payoff the gate is already throwing away (PoE's stance: boss melt/juice is the reward you do NOT cap, distinct from clear-speed which you do). The §2 asymmetry is biting, not hypothetical.

**Consequences:**
- **Caster REMOVED from the boss-bridge family** (production + clean run both clear it).
- **STR reclassified:** not a defensive crater, not "fine." A real boss-gate FAILURE whose cause (slow-but-real vs degenerate kit) is BLOCKED on the DPS instrument. Disposition is a session call (§9.3) with that new dependency.
- **rogue crater** — still un-re-read at faithful power; this run was attribute-parsed cohorts on boss shells only, not the rogue-composer question. Stays open (§9.3).
- **Open follow-on:** under W-α6 the ship gate needs 9 eligible-encounter passes; the two boss shells are 2 of 6 shell types. **Does STR clear the 9-pass floor on the non-boss shells alone?** If yes, STR's honest disposition may be "route via the floor — melee is not a boss-soloist" rather than "fix the kit" — a legitimate class-fantasy call (Diablo II never asked a pure-Vitality Barbarian to solo every Uber) PROVIDED it is decided on purpose. Verify the denominator + the boss-pass requirement before the session rules.

---

## 6. Where the fix actually lives (CORRECTED post-Gate-1)

The draft put the bug at "one global band wrongly applied to bosses" and claimed the survive/kill signal already lived in `tier_1_outcome`. Gate 1 refuted both. The corrected location:

**Bosses are KPM-gated at TWO points, both KPM, neither survival:**
1. **tier_1 routing** — a quick KPM estimate routes each encounter REJECT / PROVISIONAL_PASS / BORDERLINE. A REJECT short-circuits tier_2 entirely (gauntlet_sim.py:1019). STR boss rows REJECT here on low KPM, so their survive+kill is never simulated.
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

1. **~~Adopt the doctrine table (§1)?~~ — RULED: ADOPTED (Matt, 2026-06-19; see RULINGS).** Win-condition split; clear rooms = KPM band (floor+ceiling); boss rooms = survive+kill gate + DPS measure-only. knight-rider to draft the decisions-log entry; jack-ryan to review.
2. **Model A vs Model B for clear-room measurement:**
   - **Model A — per-room (per-shell) cohort-relative KPM bands.** Genre support as density TIERING (Q3). Density-aware: open_arena/chokepoint (8-swarm) naturally band higher than packs. Lower sim-structure change.
   - **Model B — session-wide clear-speed including travel/walk time between encounters.** The genre-CANONICAL frame (Q5). Higher fidelity to how the genre actually measures. BUT a sim-structure change (the sim must model inter-encounter travel; movement speed becomes a first-class measured lever). Flagged as the larger build.
   - Not mutually exclusive — Model A could be the near-term per-room banding while Model B is the longer-arc session-wide frame. The session should rule the sequencing.
3. **Boss-bridge family — membership now partly settled (clean run §5).** Caster is OUT (production + clean run). STR is a CONFIRMED boss-gate failure, but its cause (slow-but-real vs degenerate kit) is BLOCKED on the Tier-B DPS-measure build — its disposition (throughput fix / enrage tuning / accept-via-the-9-pass-floor) is a session call with that dependency. rogue is still un-re-read at faithful power (out of this run's scope). One doctrine, N instances — N is now: caster = 0, STR = 1 (pending DPS to classify), rogue = open. **[Matt 2026-06-19: the rocket kit-check cheap-step was SKIPPED; the DPS build is fast-tracked to classify STR directly — brief at `gandalf/requests/2026-06-19-dps-measurement-build-brief.md`.]**
4. **~~clean current-regime boss run~~ — DONE + VERIFIED (2026-06-19).** Both preconditions are now satisfied: (i) Gate-1 resolved the `tier_1_outcome` / gating-tier reads (§6, §7); (ii) the clean boss run + jack-ryan Gate-2 PASS-WITH-INFO now carry the per-archetype boss claims (§5). Caster crater dissolved; STR crater reclassified (defensive → throughput-or-degenerate, blocked on the DPS build). Residual scope: the run covered attribute-parsed cohorts on boss shells only — the rogue-composer crater and the clear-room bands were out of scope (§9.3); DPS instrumentation (Matt #8) is the next build (§3).

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
