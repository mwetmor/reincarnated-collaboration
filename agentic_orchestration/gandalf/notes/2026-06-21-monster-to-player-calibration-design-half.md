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

## 1. What the substrate says (provenance, read first-hand)

The death channel **is wired** (`spatial_engine.py:1948-1976`: `raw_dmg = dm × 300 × MOB_DAMAGE_SCALE`; `player.hp -= dmg × (1 - armor)`; `hp ≤ 0 → is_alive=False`; loss-on-player-dead at `:2107`). So this is a **calibration** property, not a missing mechanism. Two knobs set the calibration, and BOTH are stale against the current boss model:

- **`PLAYER_ARMOR_FACTOR_VS_BOSS = 0.95`** (`:159`) — the **dominant** knob. Player takes 5% of mob damage on bosses (vs 15% standard). At 5%, player TTD ≈ 3× the 210s computed at standard armor → **~630s, far beyond the 240s enrage timer**. The player *cannot* die in-window. Comment's stated intent: "boss tier fights require durability." Actual effect: **durability requires nothing** (`a_dead=0.000`). The knob overshot its own stated purpose into the opposite.
- **`MOB_DAMAGE_SCALE = 0.40`** (`:228`) — stale on **four** counts: tuned (R2 second-pass, 2026-05-19) against (a) a **120s** cap (boss now 240s); (b) an **HP>50%-at-timeout** win model (boss now binary survive-and-kill); (c) **open_arena clear-shell** WR variance as the calibration TARGET (`:154`), never boss death-risk; (d) pre-dates the four-defect fixes AND was explicitly EXCLUDED from the T1.1/Fork-2 magnitude re-validation (`v5-boss-hp-removed-attribution-clamp-2026-06-21.md:24`).

**Conclusion of the read:** the "survive" half of the boss gate is vacuous because of a stale *clear-shell* scalar plus a boss-armor knob calibrated 3× past its own intent — **not** because of an intended design choice that survival should be free. The provenance points AWAY from "intended texture."

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

**Refinement to the engine commission (relay to gamora if not already in flight):** the threshold sweep must include **`PLAYER_ARMOR_FACTOR_VS_BOSS` as the PRIMARY lever**, not `MOB_DAMAGE_SCALE` alone — §1 shows the boss-armor knob is the dominant cause of `a_dead=0`. Sweep both; report the (armor, mob-scale) pair at which a glass cannon's boss death-rate crosses ~0 → ~0.5.

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

## 8. Convergence with gamora's engine-evidence half

This note rules the PRINCIPLE (silence-not-defect; domain-mirror; A-vs-B framing; disposition). gamora's DIAGNOSE-ONLY half supplies the ONE empirical input that resolves the conditional in §5 (glass-cannon death-rate across the armor/mob-scale sweep). When her half returns: if glass cannon survives → the §5 "provably total silence" branch fires and (A) becomes an eyes-open scope cut; if it dies → the "working prerequisite" branch fires and (A) is simply accurate. **Either way the disposition in §6 is unchanged** — the close proceeds, the rider attaches, the A-vs-B routes to proxy Wave-3. gamora's evidence sets WHICH (A)-flavored truth we log, and whether (B) is genre-eventual or unnecessary. Neither half touches the banked instrument; both run safe in parallel.

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

4. **Clear-shell death is RARE-but-REAL (the swarm punish), distinct from boss death (the DPS-race).** You don't die to white trash on a normal clear; but a dense swarm that overwhelms an under-defended kit SHOULD kill it — the D3 "I got swarmed and melted" moment. The coverage-pressure channel is the exact mechanism (built for swarm-punish, currently calibrated to never kill). Re-tune so it CAN kill a paper kit in a dense pack while a competent kit survives. Clear shells already carry 3× the boss's damage (0.85 vs 0.95 armor) — the headroom is there.

5. **SEQUENCING — this re-rates the close.** The four offensive fixes (mechanism) stand; they're independent of death. But the BANDS are fit over survive+kill outcomes, and making death real CHANGES every kit's survive+kill rate — a kit that killed-in-time may now die first and fail. The boss/clear dispositions (str 1.000, dex 0.678, …) WILL move. **The bands cannot finalize until the defensive axis is calibrated.** This is NOT a regression — it FOLDS INTO the workstream's own "single tail-refit" discipline: the tail now includes the defensive axis, and bands fit ONCE over BOTH. **RECOMMENDATION:** hold the band-batch approval for the joint two-axis close, OR approve offensive bands as explicitly PROVISIONAL-pending-defense. Matt's sequencing call; knight-rider sequences the recalibration.

6. **The directive is also an anti-drift PRINCIPLE worth keeping: "if a gameplay pillar is not a real, varying signal in the sim's JSON, it is not in the game."** Death was the case in point — the docs claimed survive+kill; the substrate showed survive-vacuous. That is Discipline #13 implicit-pillar drift in its purest form: the gap between what the design CLAIMS and what the JSON SHOWS. Death is the first vacuous pillar caught; the standing audit lane is "what ELSE does the JSON claim but not actually vary" (build diversity? spirit-swap differentiation? defensive choice?).

---

**Signed:** gandalf, 2026-06-21. The player not dying is the instrument staying silent on an axis it never measured, not lying about one it did — a scope boundary, not a fifth defect, until we decide defense is in scope. It is the T1.1 domain-of-validity finding again, on the boss side: win-rate out of its domain, the real grading on the time axis. The solo close proceeds with the silence named in a rider; the one real decision — restore the defensive axis or not — is the proxy packet §4 question, ruled once at Wave-3, gated on whether a glass cannon dies. gamora measures that; I have ruled everything else.
