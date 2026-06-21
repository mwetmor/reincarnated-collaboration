# The monster→player axis — "the player never dies" is a SILENCE, not a defect (design-half framing + conditional ruling)

**Type:** gandalf design-half note, paralleling gamora's DIAGNOSE-ONLY engine-evidence half (commissioned via the KR run). The two halves converge — this one rules the design PRINCIPLE; gamora's measures the substrate that gates the one conditional inside it.
**Date:** 2026-06-21
**Author:** gandalf (story-and-design steward)
**Resolves the framing of:** the "player never dies in boss fights" finding (`a_dead=0.000` universal across all 21,120 clean-boss fights) — surfaced as a candidate FIFTH instrument-validity defect on the never-examined monster→player side.
**Amends (honestly):** my own `2026-06-19-encounter-measurement-doctrine-spine.md` §2 (last ¶) and §5-finding-4 — the half that called `a_dead=0` "the D3 Greater-Rift pattern exactly" and "VINDICATES the asymmetry." That read was an over-claim; corrected in §9 below.
**Authority:** instrument-validity workstream, gandalf-owned; the encounter-MODEL and gate-semantics calls are reserved to gandalf/Matt per the workstream brief. This rules the design principle and the disposition; the A-vs-B encounter-model decision is teed for Matt at proxy Wave-3 (it is the same question as the proxy packet §4). DOES NOT touch the banked instrument.

---

## 0. The one-line ruling

**"The player never dies on bosses" is not a fifth defect in the sense the other four were — it is a SILENCE, not a LIE.** The four banked defects were the instrument **lying about throughput it claimed to measure** (DoT counted-but-inert, armor asymmetry, rotation collapse, resource economy). The defensive-blindness is the instrument being **silent about an axis it never measured** — boss death-risk. A lie is a defect; a silence is a scope boundary. **It becomes a defect ONLY if we have decided defensive viability is in the instrument's scope.** That decision is not yet made — so the honest move is not "fix the fifth defect" but: (1) name the silence explicitly so the solo instrument does not ship it as blessed texture; (2) recognize this is the **exact structural mirror** of the T1.1 clear-shell ruling — a metric out of its domain, with the honest grading living on a *different axis* (there: completion; here: time-to-kill); and (3) route the one real design decision — *should defense be in scope at all?* — to proxy Wave-3, where it is **literally the same question** the proxy packet §4 already raised. It is gated on one empirical test gamora is running: **does a glass cannon die?**

---

## ⚖️ MATT RULING (2026-06-21, same session) — A-vs-B RESOLVED TO B: death is a CORE PILLAR

> Matt: *"There is no point in playing a game where you cannot die, and all game data is pushed into the battle sim. So whatever outputs in the JSON will be the core gameplay loop (player survival included)."*

This collapses the §4 A-vs-B. The defensive axis is **IN SCOPE, NOW** — not a deferred Phase-1 / proxy-Wave-3 question. The silence must be broken **instrument-wide.** The §1–§5 diagnosis below STANDS (why/how the silence exists; the lie-vs-silence classification; the T1.1 domain-mirror; the instrument-wide §10 finding). The §6 DISPOSITION ("does not block the close; defer the axis decision to Wave-3") is **SUPERSEDED by §11.** I held A-vs-B neutral when for an ARPG it was never a real choice — death is the genre's other half, and "the JSON is the gameplay" means a vacuous survive-clause is a missing pillar, not a scope option. Owned; operationalized in §11. The glass-cannon test (§5) converts from a go/no-go DECIDER into the CALIBRATION ANCHOR (§11.2).

---

## 1. What the substrate says (provenance) — CORRECTED by gamora's measurement (see §12)

> **§1 MECHANISM CORRECTION (2026-06-21, post-gamora).** My original §1 named `PLAYER_ARMOR_FACTOR_VS_BOSS` the *dominant* knob. **That was wrong.** gamora measured — jack-ryan Gate-2-verified, and I re-derived it arithmetically — that **`MOB_DAMAGE_SCALE` is the PRIMARY death-axis lever; boss-armor is only the FINE dial.** The corrected mechanism is below; the over-claim is owned in §12(a). The *destination* — both knobs are stale and the survive-clause is vacuous, NOT intended texture — is unchanged and strengthened.

The death channel **is wired** (`spatial_engine.py:1948-1976`: `raw_dmg = dm × 300 × MOB_DAMAGE_SCALE`; `player.hp -= dmg × (1 - armor)`; `hp ≤ 0 → is_alive=False`; loss-on-player-dead at `:2107`). So this is a **calibration** property, not a missing mechanism. The corrected mechanism:

- **`MOB_DAMAGE_SCALE = 0.40`** (`:228`) — the **PRIMARY** lever, and the real reason no kit dies. At this scale the channel is so weak that **a competent kit kills the boss before the channel can grind it down.** gamora: glass-cannon TTK ≈ 39.7s; time-to-death at scale 0.40 is ≈ 62s *even at the most extreme boss-armor (0.10, player taking 90%)*. The binding comparison is **TTD-vs-TTK** (the fight ends when the boss dies), **NOT TTD-vs-enrage** (240s) — my original error was reasoning from TTD-vs-enrage. So at production mob-scale, **boss-armor at ANY value cannot kill a competent kit** — the channel never bites inside the kill window. The scalar is stale on four counts besides: tuned (R2 second-pass, 2026-05-19) against (a) a **120s** cap (boss now 240s); (b) an **HP>50%-at-timeout** win model (boss now binary survive-and-kill); (c) **open_arena clear-shell** WR variance as the calibration TARGET (`:154`), never boss death-risk; (d) pre-dates the four-defect fixes AND was EXCLUDED from the T1.1/Fork-2 re-validation (`v5-boss-hp-removed-attribution-clamp-2026-06-21.md:24`).
- **`PLAYER_ARMOR_FACTOR_VS_BOSS = 0.95`** (`:159`) — the **FINE dial, not the dominant knob.** It only grades once `MOB_DAMAGE_SCALE` is high enough (gamora: ≈4.0) to bring the death channel inside the TTK window; there, a glass kit flips from safe→dead across boss-armor 0.80→0.74. Comment's stated intent: "boss tier fights require durability"; actual effect at the stale mob-scale: **durability requires nothing** — but the cause is the mob-scale starving the channel, with boss-armor riding on top. The knob's *direction* is right (lower armor-factor = more death); its *authority* is secondary to mob-scale.

**Conclusion of the read (unchanged in destination):** the "survive" half of the boss gate is vacuous because the death channel is **starved by a stale clear-shell mob-scale**, with boss-armor a secondary multiplier on top — **not** because of an intended design choice that survival should be free. The provenance points AWAY from "intended texture." (And §1a below shows the production endgame path nulls the channel a SECOND way I missed entirely.)

### 1a. The deeper nullifier I missed — production endgame mobs are SKILL-LESS (zero damage by construction)

gamora found, and I verified first-hand, a *second* independent reason `a_dead=0` on the production endgame boss path (`w4g2_tier_2_full_sim`): the synthetic mobs it builds via `_synthetic_mob_dict_for_spatial` carry **`"skills": []`** (`t4_sim_cycling.py:1082`). A skill-less mob never enters the cast branch, so it deals **zero skill damage** — independent of any armor or mob-scale knob. Combined with coverage-pressure being OFF on the boss path, the production endgame encounter has **NO active mob→player damage channel at all.** `a_dead=0` there is **doubly guaranteed**: no skill to cast AND no proximity channel firing.

**This changes the recal's CHARACTER, not just its knobs.** You cannot restore boss death on the endgame path by turning the armor knob — there is nothing to mitigate. Restoring it requires **giving the boss/adds a damaging mechanism** — a real spatial skill on the mob, OR enabling the coverage-pressure channel. That is **monster-offense DESIGN work**, not a two-knob calibration. The recalibration wave is correctly scoped as partly a content/design wave (what damage do endgame monsters deal, and how), not purely a scalar re-fit. I missed this layer entirely in my original read; owned in §12(b).

---

## 2. The reframe — lie vs silence (why "fifth defect" mis-classifies it)

| | The four banked defects | The monster→player silence |
|---|---|---|
| **Failure kind** | instrument **lied**: counted DoT it didn't apply; rewarded throughput it mis-resolved | instrument is **silent**: never speaks to defensive viability at all |
| **Did it pass a bad kit?** | YES — over/under-credited kits on a metric it *claimed* | Vacuously no kit has died, so no kit is *wrongly* passed-on-survival — there is just no signal |
| **Correct classification** | DEFECT (fix recompose-first) | SCOPE BOUNDARY (decide if in scope; only then a defect) |

The boss gate's "survive" clause is a **vestigial limb**: the doctrine table lists "survive + kill," `sg2` computes a survival floor as telemetry, but `a_dead=0` makes the survive clause non-discriminating. It is dressed as a gate and functions as a silence. **Naming that honestly is the §5/§5a anti-pattern discipline** — do not bless a limitation as texture without naming it.

---

## 3. The structural mirror — this is the T1.1 ruling again, on the boss side

I just ruled (T1.1) that **KPM is out of its domain** on sub-`T_min` clears: the metric measures the tick-floor, not throughput; the honest grading lives on a **different axis** (completion); resolution = domain-guard, gate on the axis that applies.

The boss side is the **same structure**: **win-RATE is out of its domain** when `a_dead=0`. WR snaps 0→1 as mean-TTK crosses the timeout — it measures the clock-crossing, not survivability. The honest grading lives on a **different axis: time-to-kill** (exactly what the proxy spike independently re-discovered — "the genuine grading lives on the TIME axis, not the binary-WR axis"). The resolution is identical in KIND: recognize WR is out-of-domain under `a_dead=0`, and grade on the axis that carries signal (TTK / kill-before-enrage).

So this is not a new weird thing — it is the **same domain-of-validity finding** appearing on the boss side. Both the clear-shell metric (KPM, sub-`T_min`) and the boss metric (WR, `a_dead=0`) are metrics measuring their own floor instead of the fight, with the real signal on an adjacent axis. The instrument has *one* recurring pathology, surfacing twice.

---

## 4. The decision actually on the table (A vs B) — and what each costs

The reframe makes the real question precise. It is NOT "texture or defect." It is: **does the Phase-0 instrument measure defensive viability at all?** Two internally-coherent end-states:

**(A) Offensive-throughput instrument, defense out-of-scope for Phase 0 — by deliberate, LOGGED choice.**
- Accept the silence. **Rename the operative gate "kill-within-enrage"** (drop the vacuous "survive" pretense); grade the boss on the TIME axis (TTK / kill-before-enrage) exactly as §3 prescribes. Defense is a **prerequisite everyone meets** (the 95% armor budget is the floor), not a graded differentiator.
- COST: the instrument is **blind to glass-cannon non-viability**. A kit that is offensively in-band and kills-in-time, but is defensively paper, ships with the sim's blessing. Acceptable ONLY if the shipped game's death channel is not harsher than the sim models AND defensive build-differentiation is not a Phase-0 goal. Both currently hold (workstream has been entirely offensive; "solo gameplay only"; spirit-swap is the differentiator, not defense).
- This is the **recompose-first, domain-guard** resolution — consistent with T1.1, no new calibration on a closing instrument.

**(B) Restore the defensive axis — re-tune so bosses carry real death-risk.**
- Bring `PLAYER_ARMOR_FACTOR_VS_BOSS` (and/or `MOB_DAMAGE_SCALE`) back to where a defensively-weak kit *can* die in-window. Restores a **WR-graded** boss outcome; gives the instrument sight of the genre's second primary failure axis (the glass cannon that gets one-shot — half the genre's build-crafting depth).
- COST: this is **NEW calibration work** on never-validated knobs, against a 240s/binary model the scalars were never tuned for — a real defect-hunt. It changes the boss gate from binary-kill-in-time back to graded-WR, re-opening a banked surface. It is genre-TRUER but it is a scope EXPANSION of the instrument, not a bug-fix.

The provenance (§1) tilts toward **B being eventually correct** (the knob fails its own "require durability" intent) but toward **A being correct for NOW** (don't re-open a closing instrument to chase a stale knob before the need is empirically proven).

---

## 5. The empirical criterion that decides A vs B (gamora's half)

The decision must NOT be made on vibes. It is decided by one test gamora is running DIAGNOSE-ONLY: **does a deliberately glass-cannon kit die at the current `PLAYER_ARMOR_FACTOR_VS_BOSS=0.95`?**

- **If even a glass cannon survives** → durability is not even a *prerequisite*; it is fully free; the 95% knob has erased the axis against its own stated intent → the silence is **provably total**, and choosing (A) means EXPLICITLY accepting defensive-blindness as a Phase-0 scope cut (eyes open), while (B) becomes the genre-true eventual fix.
- **If a glass cannon DIES but a normal-durability kit survives** → durability is a **working prerequisite** (everyone-meets-it bar); the instrument is fine AS-IS under reading (A) with no re-tune; `a_dead=0` at faithful power was a power-profile artifact, not an axis-collapse. (A) is then not a scope cut but an accurate model.

**Refinement to the engine commission — CORRECTED (post-gamora):** my original refinement said sweep `PLAYER_ARMOR_FACTOR_VS_BOSS` "as the PRIMARY lever." **That was the inverted-mechanism error (§1, §12a).** The correct primary lever is **`MOB_DAMAGE_SCALE`** (boss-armor is the fine dial). gamora swept exactly this and found the (mob-scale ≈ 4.0, boss-armor ≈ 0.76) pair at which a glass cannon's boss death-rate crosses into the viable-but-risky band — see §12(c).

---

## 6. Disposition

1. **DOES NOT block the solo-instrument close.** The four banked defects are all offensive-side; the close is about those; defense was never in the workstream's scope. Recompose-first forbids bolting a fifth fix onto a closing instrument before the need is proven. **Matt's band-batch approval proceeds.**
2. **BUT the close carries an explicit one-line rider** (so the silence is not shipped as blessed texture — §5/§5a): *"Boss gate is offensive-only (kill-within-enrage); the 'survive' clause is vacuous at the current boss-armor calibration (`a_dead=0.000`); defensive viability is a deliberate Phase-0 scope cut pending the glass-cannon re-validation."* This belongs in the decisions-log batch as a noted limitation, not a defect.
3. **The A-vs-B decision routes to proxy Wave-3 — because it IS the proxy packet §4 question.** The packet's §4 ("grade the proxy boss on clear-time band OR add a player-death channel") and this note's A-vs-B are the **same call**: (A) = grade on time-axis, no death channel; (B) = add a real death channel. **Rule them ONCE, together, at proxy Wave-3, gated on gamora's glass-cannon test.** Do not make it twice.
4. **No new Matt-halt is opened.** The architecture call (build/re-scope/park proxy) is unaffected — this is a Wave-3 calibration question, downstream of the build decision, exactly where the packet already placed it.

---

## 7. Player consequence (the anchor)

Under (A) shipped silently: a player invests in a defensively-fragile kit, the sim blesses it (offensively in-band, kills the boss in time), and then — *if the live game ever carries a death channel the sim didn't model* — the player gets one-shot and feels the build was a lie. That is the inverse of the D4-launch "wet noodle" complaint: not "my damage feels weak," but "the game told me this works and then killed me for a choice it never warned me about." The rider in §6.2 is the guard against that: we ship (A) **knowing** the instrument is offense-only, so we never *claim* defensive validation we didn't perform.

Under (B): the player who builds tanky-survivable — the genre's legitimate "outlast the boss" fantasy — finally has that choice MEAN something to the instrument, and the glass cannon is correctly told "too fragile for this boss." That is the genre's second axis restored. It is the truer game — but it is a deliberate scope expansion, made when Phase 0's offensive instrument is closed and we choose to open the defensive one, not bolted on mid-close.

The honest path: **close the offensive instrument; name the silence; decide the axis once, with evidence, at the proxy Wave-3 door where the same question already waits.**

---

## 8. Convergence with gamora's engine-evidence half — HER HALF RETURNED (see §12)

This note ruled the PRINCIPLE (silence-not-defect; domain-mirror; A-vs-B framing; pre-ruling disposition). gamora's DIAGNOSE-ONLY half has now RETURNED, jack-ryan Gate-2-verified. **It did more than resolve the §5 conditional — it landed AFTER Matt's (B) ruling, so the question is no longer "which A-flavored truth to log" but "does the (B) recalibration exist and hold its guard."** Answer: YES to both. The glass-cannon test converted from a go/no-go decider into the CALIBRATION ANCHOR (§11.2), and the validated knob-set lands glass viable-but-risky / bruiser safe with the homogenization guard intact. The pre-ruling "disposition unchanged either way, route A-vs-B to Wave-3" in the original §6/§8 is **SUPERSEDED** — twice over: by Matt's (B) ruling (death is in scope NOW, instrument-wide) and by gamora's evidence (the recal is reachable, the guard holds). Full return record, corrections owned, and the proxy §4 resolution are in **§12.** Neither half ever touched the banked instrument; both ran safe in parallel.

---

## 9. Honest amendment to my own doctrine spine (for the record)

- **§2, last ¶ ("a_dead=0 ... VINDICATES the §2 asymmetry empirically"):** AMENDED. `a_dead=0` at faithful power is DATA; my reading of it as *vindication* assumed the free-survival was intended texture. The provenance (§1) shows it is a stale clear-shell scalar + a boss-armor knob 3× past its own "require durability" intent. The asymmetry (no boss DPS ceiling) still stands on its own genre merits; it is just not *vindicated* by `a_dead=0`, because `a_dead=0` is an artifact, not a designed property.
- **§5-finding-4 ("`a_dead=0` ... is the D3 Greater-Rift pattern exactly"):** AMENDED — this was the over-claim. **D3 Greater-Rift has death LIVE at the push margin** — the entire skill of GR pushing is the survivability-vs-damage tradeoff; a glass wizard *does* get one-shot by a Rift Guardian three tiers up. `a_dead=0.000` UNIVERSAL, every archetype, every cohort, is the OPPOSITE of GRift — it is the defensive axis calibrated *out*. The correct genre frame is not "GRift texture" but "a single farmable difficulty tier where everyone clears the durability bar" — which is real, but is a SCOPE statement (defense is a met prerequisite at this tier), not a vindication that survival *should* be free. The operative doctrine content (kill-before-enrage gates; DPS measured; no ceiling) is **unchanged**; only the STATUS of the "survive" clause moves: from "confirmed-free texture (GRift)" to "vacuous-pending-revalidation (stale knob)."

This is the discipline working in the same shape as the T1.1 amendment: I made an empirical-character claim ("free survival is intended texture"), the substrate read it back ("free survival is a stale knob past its own intent"), and the ruling updates. The destination of the doctrine is preserved; one mischaracterized status is corrected.

---

## 10. ADDENDUM (Matt Q, same session) — the silence is INSTRUMENT-WIDE, not boss-specific

Matt asked whether non-boss encounters damage the player. Checked phase3 first-hand, separating the rows where tier_2 ACTUALLY RAN (`tier_1 != REJECT`) from the tier_1-REJECT `0.0` defaults (the exact masquerade that manufactured the false STR boss-crater — caught here, not fallen for):

| clear shell | tier_2-RAN rows | survival where measured | tier_1-REJECT (0.0 defaults, NOT deaths) |
|---|---|---|---|
| open_arena | 659 | **1.000** (min 1.0, zero <1.0) | 133 |
| chokepoint_corridor | 497 | **1.000** | 97 |
| magic_pack | 570 | **1.000** | 24 |
| elite_pack | 0 | (never measured) | 990 (all-REJECT) |

**Finding:** `a_dead=0` is **not a boss property — it is instrument-WIDE.** On every shell where survival was actually simulated, the player survived 100%. This is produced by TWO armor knobs — `PLAYER_ARMOR_FACTOR_VS_STANDARD=0.85` (clear shells, 15% taken) and `PLAYER_ARMOR_FACTOR_VS_BOSS=0.95` (boss, 5% taken) — plus the coverage-pressure channel calibrated to "ST kit survives the walk-down." All three are set so that nothing kills.

**This STRENGTHENS the §0 ruling.** The silence is UNIFORM, not a weird boss-specific inversion. Mechanically the clear shells deal **3× the boss's damage** (15% vs 5%), so the most-dangerous encounter to the player is *trash*, and the *least* dangerous is the boss — but neither kills, so the asymmetry never surfaces as outcome. There is no "boss safer than trash" inversion in the GAMEPLAY today because the defensive axis is collapsed everywhere. The instrument is offense-only on ALL six shells by one coherent mechanism.

**Consequence for A-vs-B (§4):** the framing "add BOSS damage" is wrong. The decision is "**does the instrument have a defensive axis AT ALL**," and if yes (path B), it must be rationalized **instrument-wide** — both armor knobs + coverage-pressure together, holistically re-derived — NOT a boss-only patch that would CREATE the trash-safer-than-boss inversion. **Caveat:** phase3 is regime-mixed + tier_2-gated, and elite_pack is unmeasured (all-REJECT). The clean confirmation extends gamora's commission to **all six shells, tier_1-bypassed** (Q6), not boss-only.

## 11. OPERATIONALIZATION — death is core; the HOW (post-Matt-ruling)

The decision is made; this seat's job is now the HOW, where the genre's failure modes are sharp. Six positions:

1. **This ACTIVATES the adopted doctrine's dormant half — it does NOT overturn it, and it VINDICATES the gate.** The doctrine table already lists "survive + kill" as the boss gate; we were shipping the survive clause vacuous. Making death real activates the limb the doctrine always claimed — nothing in the encounter-measurement doctrine reverses. And it vindicates the survive+kill GATE over a DPS gate: with real death the boss becomes a genuine **2D race** (out-DPS the 240s enrage AND out-survive the boss), and the survive+kill binary NATURALLY admits BOTH the glass-burst "kill it in 4s before it kills me" AND the tank-grind "outlast it 90s" — the genre's two boss-kill fantasies — with no DPS floor and no defense floor. Just "did you win." The gate was designed for exactly this 2D world; it was running in a degenerate 1D mode.

2. **The calibration TARGET (the dial): glass cannon at ~0.6–0.8 survive+kill — viable but high-variance — NOT 1.0 (blind, current) and NOT 0.0 (over-punished); bruiser at ~0.95+.** The SPREAD between them IS the defensive axis the instrument can finally see. gamora's glass-cannon test converts from a go/no-go decider into the CALIBRATION ANCHOR: sweep the death knobs, find where the glass cannon lands viable-but-risky and the bruiser safe. Genre target: the D3 speed-GR glass wizard and the PoE one-shot-or-be-one-shot assassin are VIABLE but DIE MORE; the bruiser is SAFE but slower. Both ship.

3. **THE PRIME CONSTRAINT — the homogenization guard.** This is where the genre most often gets "death matters" wrong, and it is the single most load-bearing HOW-constraint. PoE's capped-resist lesson: if calibration makes ONE defensive threshold mandatory ("hit 75% resist or die to everything"), defense becomes a TAX everyone pays identically, build diversity COLLAPSES to a single floor, and we achieve the OPPOSITE of the intent. D4-launch's parallel failure: global mob-damage cranked so the endgame became a one-shot/telegraph-or-die meta they spent a year walking back. The guard: calibrate so (a) MULTIPLE defensive strategies work (mitigation OR avoidance OR sustain OR kill-speed), and (b) OFFENSE can PARTIALLY substitute for defense. That keeps the axis genuinely 2D. **A death channel that forces every build to the same armor number is a defect dressed as the fix.**

4. **Clear-shell death is RARE-but-REAL (the swarm punish), distinct from boss death (the DPS-race) — but coverage-pressure ALONE won't deliver it (gamora-corrected).** You don't die to white trash on a normal clear; but a dense swarm that overwhelms an under-defended kit SHOULD kill it — the D3 "I got swarmed and melted" moment. I originally named coverage-pressure as "the exact mechanism — just re-tune it to kill a paper kit." **gamora's sweep corrects that:** coverage-pressure is a **WEAK lever for fast-AOE kits** — a circle-AOE glass kit covers and clears the swarm before the bleed accrues, so it survives 1.000 across the full coverage sweep (cov_per_mob 8→150). Coverage punishes **point/melee/slow** kits, not fast-AOE. That is *arguably the correct 2D outcome* (clearing fast IS a defensive strategy — offense substituting for defense, the §11.3 guard working as designed), but it means **clear-shell death needs its OWN mechanism review** (per-hit variance? burst spikes? not-fully-coverable threats?), not just a coverage-pressure re-tune. The headroom (clear shells carry 3× the boss's damage) is real; the *delivery mechanism* for fast-AOE punish is not coverage alone. jack-ryan carries this as a recal-wave CONSTRAINT; detail in §12(e).

5. **SEQUENCING — this re-rates the close.** The four offensive fixes (mechanism) stand; they're independent of death. But the BANDS are fit over survive+kill outcomes, and making death real CHANGES every kit's survive+kill rate — a kit that killed-in-time may now die first and fail. The boss/clear dispositions (str 1.000, dex 0.678, …) WILL move. **The bands cannot finalize until the defensive axis is calibrated.** This is NOT a regression — it FOLDS INTO the workstream's own "single tail-refit" discipline: the tail now includes the defensive axis, and bands fit ONCE over BOTH. **RECOMMENDATION:** hold the band-batch approval for the joint two-axis close, OR approve offensive bands as explicitly PROVISIONAL-pending-defense. Matt's sequencing call; knight-rider sequences the recalibration.

6. **The directive is also an anti-drift PRINCIPLE worth keeping: "if a gameplay pillar is not a real, varying signal in the sim's JSON, it is not in the game."** Death was the case in point — the docs claimed survive+kill; the substrate showed survive-vacuous. That is Discipline #13 implicit-pillar drift in its purest form: the gap between what the design CLAIMS and what the JSON SHOWS. Death is the first vacuous pillar caught; the standing audit lane is "what ELSE does the JSON claim but not actually vary" (build diversity? spirit-swap differentiation? defensive choice?).

---

## 12. GAMORA EVIDENCE RETURNED — convergence, corrections owned, recalibration validated

gamora's DIAGNOSE-ONLY half returned (`~/Games/reincarnated-engine/src/reincarnated/simulation/math/defensive-axis-calibration-diagnose-2026-06-21.md`); jack-ryan Gate-2 = **PASS-WITH-INFO**, every load-bearing claim re-derived first-hand (`agentic_orchestration/qa/findings/2026-06-21-defensive-axis-calibration-diagnose-gate2.md`). I re-derived the mechanism correction arithmetically and confirmed the skill-less-mob finding first-hand (`t4_sim_cycling.py:1082`) before recording. What the evidence did to this note:

**(a) My §1 "boss-armor dominant" claim was WRONG — corrected, owned.** I reasoned from TTD-vs-ENRAGE (TTD ≈ 630s ≫ 240s → "the boss-armor knob is dominant"). The binding comparison is **TTD-vs-TTK**: the fight ends when the boss dies (~39.7s for a glass kit), and at production mob-scale (0.40) the death channel needs ~62s to kill *even at the most extreme boss-armor (0.10)* — so the kit always wins first, at ANY armor. **`MOB_DAMAGE_SCALE` is the primary lever; boss-armor is the fine dial.** Same discipline shape as the Fork-2/3a and D3-GRift amendments: I made an empirical-character claim, the substrate read it back inverted, the ruling updates; the destination (survive-clause vacuous, not texture) is unchanged and strengthened.

**(b) The deeper nullifier I missed entirely — skill-less synthetic mobs (§1a).** Production endgame boss path builds mobs with `"skills": []` → zero skill damage by construction, independent of every knob; combined with coverage-pressure off, the endgame encounter has NO active mob→player damage. `a_dead=0` there is doubly guaranteed. **This makes the recal partly a MONSTER-OFFENSE-DESIGN wave** (give endgame monsters a damaging mechanism), not a two-knob re-fit. A genuine gap in my read; owned.

**(c) The (B) recalibration EXISTS and my §11 direction is empirically CONFIRMED.** Validated knob-set: `MOB_DAMAGE_SCALE` 0.40→**4.0**, `PLAYER_ARMOR_FACTOR_VS_BOSS` 0.95→**~0.76**, `PLAYER_ARMOR_FACTOR_VS_STANDARD` 0.85 held, coverage off (boss path). Lands glass cannon at **0.75–0.92** survive+kill, bruiser **1.000** — exactly the §11.2 target (glass viable-but-risky, bruiser safe). ~0.60 armor of grading headroom, tracking the 3.3× HP ratio. The spread between glass and bruiser IS the defensive axis the instrument can finally see.

**(d) THE PRIME CONSTRAINT (§11.3 homogenization guard) HOLDS — verified.** At fixed HP+armor, survival is a pure TTK-vs-TTD race driven by OFFENSE: a fast kit survives-by-killing where a slow kit of *identical* HP/armor dies (gamora guard sweep: dm≤0.8 → all dead; dm≥1.6 → all survive). Offense **partially substitutes for defense**; combined with the bruiser surviving-by-enduring at the same knob-set, the axis is genuinely **2D with no mandatory armor floor.** This is the single result that says the recal avoids the PoE capped-resist tax and the D4-launch one-shot meta. It is the load-bearing confirmation that the §11.3 guard is satisfiable, not just aspirational.

**(e) §11.4 softened — coverage-pressure is a WEAK clear-shell death lever vs fast-AOE.** A circle-AOE glass kit clears the swarm before bleed accrues → survives 1.000 across the full coverage sweep. Coverage punishes point/melee/slow kits, not fast-AOE. Arguably the correct 2D outcome (clear-fast = a defensive strategy), but clear-shell death needs its OWN mechanism review; coverage alone won't punish a fast-AOE glass. (jack-ryan Gate-2 carries this as a recal-wave CONSTRAINT.)

**(f) Proxy packet §4 — RESOLVED for solo.** The packet's §4 asked, for the summoner boss, "grade on clear-time band OR add a player-death channel." Matt's (B) ruling answers it for solo: **death is real.** Proxy Wave-3 therefore **inherits a real death channel** — it is no longer a deferred A-vs-B choice. The summoner question narrows to "how does the army's defensive profile (proxy survivability + caster exposure) read against the SAME real death channel solo now carries" — a calibration inside an answered model, not a fresh encounter-model fork. One fewer open design fork downstream.

**(g) Sequencing (§11.5) — my lean sharpens toward (b)-with-emission-hold.** Findings (b)+(c) show the recal is bigger than a two-knob tail-fold — it carries monster-offense DESIGN (skill-less mobs) and a separate clear-shell mechanism review (e). Folding that into the offensive close as one tail-refit would bloat the close and couple two independently-validatable surfaces. **Recommendation:** bank the offensive instrument now (the four fixes + bands as PROVISIONAL-on-offense), run the defensive recal as its OWN Matt-scoped wave — BUT gate **content emission** on the joint two-axis close, so no offensively-blessed-but-defensively-fragile kit ships before death is real. This preserves the "single tail-refit" discipline's intent (bands finalize once over both axes) without holding the offensive close hostage to a design-weight wave. jack-ryan's two recal-wave constraints (instrument-wide joint re-derivation of standard-armor + mob-scale; clear-shell death needs its own mechanism) are the wave's named entry conditions.

**Net:** my §11 *direction* (death core; calibration target; homogenization guard as prime constraint; instrument-wide, not boss-only) is empirically confirmed. Two of my factual reads were wrong (boss-armor dominance; coverage-pressure sufficiency) and one whole layer was missed (skill-less mobs) — all owned, all corrected. The recal is real, reachable, and bigger than first scoped: a monster-offense-design wave, not a two-knob patch. Nothing here touches the banked offensive instrument; the recal is a future Matt-authorized production wave.

---

**Signed:** gandalf, 2026-06-21. The player not dying is the instrument staying silent on an axis it never measured, not lying about one it did — a scope boundary, not a fifth defect, until we decide defense is in scope. It is the T1.1 domain-of-validity finding again, on the boss side: win-rate out of its domain, the real grading on the time axis. The solo close proceeds with the silence named in a rider; the one real decision — restore the defensive axis or not — is the proxy packet §4 question, ruled once at Wave-3, gated on whether a glass cannon dies. gamora measures that; I have ruled everything else.
