# Rogue refire — design disposition: the role-floor fix is NECESSARY-BUT-INSUFFICIENT on rogue (the falsifier fired on data)

**Type:** design-disposition note (gandalf → knight-rider). Reads the G7 HOLD-SIM rogue re-fire result against my own pre-registered falsifier.
**Date:** 2026-06-15
**Author:** gandalf (story-and-design steward)
**Authority:** continuation of the Matt-authorized 2026-06-15 (Pattern-B) rogue-degeneracy resolution workstream — *"solve through strategic design/understanding rather than allowing the archetype label to linger as an open hypothesis."* The fix was Matt-greenlit; this note reads its sim result. It records a design read; it does NOT make the Decision-2 call (HELD) — that is unchanged and confirmed.
**Parent:**
- My diagnosis: `agentic_orchestration/gandalf/notes/2026-06-15-rogue-degeneracy-role-floor-diagnosis-for-kr.md` (§1 mechanism, §3 prediction/falsifier, §5 fix, §6 b6-coupling).
- gamora refire result: `reincarnated-engine/output/g7-hold-sim-b6-prereq-B-rogue-refire-20260615.json`; criterion math-note §8: `reincarnated-engine/src/reincarnated/simulation/math/b6-deletion-prereq-B-g7-hold-sim-viable-fight-criterion-2026-06-15.md`.
- rocket fix math-note: `reincarnated-engine/src/reincarnated/generation/notes/2026-06-15-envelope-role-floor-math-note.md` (built commit `52703c9`, tag `rocket/v2.2-envelope-role-floor`; Gate-1 CLEAR-WITH-AMENDMENTS, Gate-2 PASS-WITH-INFO).
- Recognition record: `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` § 6-quater (Decision 2) / § 6-septies (prior STILL-OPEN). This note logs to a new § 6-octies.
- b6-deletion prerequisites brief: `agentic_orchestration/gandalf/notes/2026-06-15-b6-deletion-prerequisites-brief-for-kr.md` (Prereq B = G7 HOLD-SIM).

---

## 0. One line

**The floor fired exactly as designed (`defensive:1, mobility:2, area_damage:4, burst_damage:1` — the precondition-assert PASSED), and the envelope rogue arm STILL craters its upper tiers (swarm 1.0 → modifier floored to 0.0719 → magic/elite/mini_boss/boss all near-zero).** The floor closed a REAL composer gap and is worth keeping on its own merits; it did NOT dissolve the swarm-over-clear → single-global-modifier → upper-tier-crater dynamic, because that dynamic is **raw single-target throughput** (my own §1), which an *AoE-share* floor does not reduce. This is the **falsifier I pre-registered in §3, firing on data on the physical side** — the role floor is *not the whole story* for rogue. The architectural single-global-modifier hypothesis re-opens **on evidence, not silence.** Decision 2 stays HELD; b6 stays. The fix STANDS (necessary, label-free, genre-correct); the *remaining* lever is NOT another composition floor — it is either a swarm-side spatial/coverage mechanic or a per-tier-modifier balance-loop change.

---

## 1. Disposition of the diagnosis — confirmed in part, falsified in part, on EVIDENCE

My §3 registered a falsifier in the caster frame: *if a floor-intact kit ALSO craters boss while swarm is hot (branch 2 — ARCHITECTURAL), the role floor is not the whole story.* The caster precondition never arose (§ 6-septies — casters ran too cold). **But this rogue re-fire is the structurally exact same test, run on the physical side, and it reached the precondition the caster runs could not:**

- **Floor-intact** (the precondition-assert PASSED: `{defensive:1, mobility:2, area_damage:4, burst_damage:1, primary_attack:2}`, kit_size 10 — this is the FIXED kit, demonstrably, not the old 0-defensive/0-burst degeneracy).
- **Swarm hot** (envelope swarm WR `1.0` — over-ceiling, exactly the hot-swarm precondition my caster falsifier required).
- **Boss craters anyway** (envelope boss `0.0`, elite `0.0`, mini_boss `0.0`, magic `0.05`; `final_modifier` pinned at `0.0719`).

That is the **branch-2 (ARCHITECTURAL) shape**: a floor-intact kit that craters its upper tiers while swarm is hot under a floored modifier. The caster runs were silent on it; the rogue re-fire is loud on it.

**What is CONFIRMED (the floor was a real gap, now closed):**
- The composer genuinely could emit no `defensive` role and no sub-60 `burst` (§1, confirmed by rocket's audit, § 6-septies). The fix closed exactly that — the kit now carries survival + spike + mobility + AoE-share per genre doctrine. **The composer gap was real; it is closed.** That half of my diagnosis stands fully and on evidence.

**What is FALSIFIED (the floor is NOT the whole story for rogue):**
- My §1 claim *"the entire arm-to-arm delta is the role floor"* and §2 claim *"role floor is necessary AND sufficient — the canary"* are **REFUTED on data.** The floor fired and the arm STILL craters. The delta was not *entirely* the floor. The floor is **necessary** (a real gap, now closed) but **insufficient** (it does not bring the rogue arm to parity).
- The specific reason is the one I myself flagged in §1 and did not follow to its conclusion: *"swarm-hot is NOT an AoE artifact — a fast single-target striker deletes low-HP swarm one-by-one via raw ST throughput."* If swarm-over-clear is raw ST throughput, then an **AoE-SHARE floor (Rule A, 4 area skills) is aimed at the wrong variable.** Adding AoE skills to a kit does not *reduce* its single-target throughput against low-HP mobs; the ST skills still delete swarm one-by-one. The floor reserved the boss-killer burst (Rule B) correctly — but at a global modifier of `0.0719` driven down to suppress the 1.0 swarm, that burst does nothing. **I diagnosed the swarm mechanism correctly and then prescribed a fix (AoE-share) that does not act on it.** That is the precise locus of the insufficiency.

**Net disposition: the diagnosis is HALF-CONFIRMED, HALF-FALSIFIED, both on evidence.** The composer gap (real, closed) is confirmed. The "necessary-AND-sufficient / entire-delta-is-the-floor" claim is falsified. This is the honest recognition→validate→commit outcome: recognition (the floor gap) validated true and was committed; the *coupling* recognition (the floor closes Decision 2) validated FALSE and must not be committed. **The architectural single-global-modifier hypothesis (§ 6-quinquies (f) / § 6-septies) re-opens — and for the first time it has POSITIVE evidence, not a silence.** The discipline I carried in § 6-septies ("a silence is not a clearance in either direction") is now superseded for the physical side by an actual signal: the floor-intact-and-still-craters-under-hot-swarm shape DID evaluate, and it points at branch 2.

---

## 2. Does the floor fix STAND? — YES, on its own merits, independent of the b6 coupling

The fix is built, gated (Gate-1 CLEAR-WITH-AMENDMENTS, Gate-2 PASS-WITH-INFO), tagged (`rocket/v2.2-envelope-role-floor`). Necessary-but-insufficient is **not** an argument to revert it. It stands for four reasons:

1. **It closed a real composer gap that exists regardless of the b6 coupling.** Before the fix, EVERY envelope glass/fast/single-target cell composed with zero survival, zero spike — not just rogue. The fix means every such cell now carries the genre-mandatory survival tech + boss-killer + mobility + AoE-share. That is correct *whether or not* it closes Decision 2. A glass ARPG striker with no defensive layer is a composition bug by every genre standard (D3 Demon Hunter Smoke Screen/Vault mandatory; D2 Assassin Shadow Discipline; PoE glass-cannon defensive-layers doctrine). The fix encodes that truth at the coordinate layer, label-free (smuggle-test PASSED per rocket §3). **You keep a correct composition floor even if it does not, by itself, win a downstream sim gate.**

2. **It is risk-free and additive.** It does not regress the kit_size band (rocket §4 A3: 11 distinct geometries preserved with 8 reserved slots — it ENRICHES role diversity). It introduces no new field (Principle-6: reuses `Skill.role`). It is gated behind NEW OPTIONAL params and fires only when threaded. Reverting it would *re-open* a confirmed composition gap to remove a fix that costs nothing — strictly negative.

3. **It is a PREREQUISITE for any future test of the architectural question.** The reason the caster runs (§ 6-septies) were inconclusive is they could not reach the hot-swarm precondition. The reason this rogue run is DECISIVE is the floor let us hold composition constant and isolate the modifier dynamic. Without the floor, every future rogue sim re-conflates "is this the composer gap or the architecture?" The floor is what makes the architectural question cleanly askable. Reverting it would re-muddy exactly the variable we just cleaned.

4. **Necessary-but-insufficient is the CORRECT standing for a real fix that does not happen to close a coupled gate.** The error would be to read "didn't close Decision 2" as "wrong fix." It is a *right fix for the composer gap* that *revealed* the composer gap was not the only thing wrong. That is a successful diagnostic step, not a failed one.

**Verdict: the floor fix STANDS. Keep it. It is canonical envelope composition behaviour now, on its own merits.**

---

## 3. Where the ACTUAL remaining lever lives — NOT another composition floor

My §1 already named the mechanism and this run confirms it: **swarm over-clear on rogue is raw single-target throughput, not an AoE gap.** That fact eliminates the composition-floor family of levers — you cannot fix a raw-ST-throughput problem by reserving role slots in the kit, because the ST skills that over-clear swarm are exactly the skills the kit MUST have to be a single-target striker. The lever is NOT in the composer. It lives in one of two places:

**Lever candidate (A) — a swarm-side spatial/coverage mechanic (the "unbuilt lever" Matt already flagged).** This is the same lever § 6-septies upgraded the caster re-open criterion to: *"build a spatial/coverage-attacking lever."* The convergence is not coincidental — it is the SAME underlying truth surfacing from both the caster cold-swarm side and the rogue hot-swarm side. The swarm tier today is HP-bound and position-naive: a fast ST striker walks the swarm down one mob at a time and the swarm cannot punish the time that takes because there is no spatial/coverage cost to single-target-clearing a group. If swarm mobs imposed a coverage/area pressure (you take damage / lose tempo for NOT clearing them in a window; or the swarm spreads and a pure-ST kit cannot keep coverage), then a single-target kit would NOT trivially pin swarm at 1.0 — and the global modifier would not have to floor to 0.0719 to suppress it. **This is the lever that acts on the actual variable (ST throughput vs swarm coverage).** It is also the lever that would resolve BOTH the rogue hot-swarm AND the caster cold-swarm problems, which is the tell that it is the real one.

**Lever candidate (B) — per-tier modifiers instead of one global modifier (the architectural change).** This is the single-global-modifier hypothesis stated as a fix. Today `balance_loop` searches ONE `final_modifier` to bring the WHOLE kit to its target WR; when swarm is at 1.0, that one modifier floors to 0.0719 to suppress swarm, and everything above swarm dies with it. If the modifier were per-tier (or per-tier-band), swarm could be suppressed without dragging boss down. **This is the bigger, riskier change** — it touches the balance-loop architecture, not content — and it is exactly the "reshape means the balance loop needs per-tier shape" reading § 6-sexies (f) raised as the architectural branch. The rogue re-fire is the **first positive evidence** that branch 2 is real on the physical side.

**Which is the real lever?** Locating, not prescribing (per the ask): **lever (A) is the more likely real one and the better first probe**, for a genre/design reason. A per-tier modifier (B) is a balance-loop band-aid that lets a kit pass the gate while leaving the PLAYER experience untouched — the rogue still deletes swarm in a way that trivializes that tier, you have just stopped the sim from punishing it. That is the D3-pre-RoS lesson § 6-septies cited: *do not ship a symptom patch you do not understand.* Per-tier modifiers would make the sim pass while the underlying "ST striker trivializes swarm" is exactly as true as before. Lever (A) — swarm-side coverage pressure — changes what the PLAYER feels (a fast striker now has to *manage* a swarm, not auto-delete it; that is the genre-correct tension — D4 swarm-density / PoE pack-coverage design both make ST builds carry some clear tech or feel the swarm). **The remaining lever lives in the swarm-side encounter design, not in the composer and (probably) not in the global modifier.** That is a design call reserved for Matt; I locate it, I do not build it.

**One sharp caveat:** I held in §1 that rogue is "the clean canary." This run shows the canary is dirtier than I claimed — the rogue cell has TWO problems stacked: (1) the composer gap (now fixed) AND (2) the swarm-coverage / single-global-modifier problem (the four co-broken cells of § 6-sexies share #2, not #1). The fix peeled off #1 and exposed #2 cleanly. So the rogue cell is now in the SAME family as warrior/grappler/skirmisher/hunter on the residual: a swarm-over-clear → modifier-floor → upper-tier-crater problem that NEITHER arm solves. The difference is rogue's b6 arm *happens* to carry boss on the medium-range baseline — and on rogue's GENUINE close/single-target coordinates (this run), even the b6 arm now co-fails boss (b6 boss `0.0`). **That is the most important new fact in this run (see §4).**

---

## 4. Decision 2 disposition — HELD is CORRECT and UNCHANGED; one reframe worth surfacing

**Prerequisite B honest-fails again → the both-pass tally CANNOT close → b6 STAYS. Confirmed.** Nothing about the fixed floor changes this. The fix made the floor fire; the floor did not make the envelope arm clear the upper tiers; so the envelope is still not a sim-safe replacement for the b6 net on the rogue cell, and the destructive deletion does not fire. The conjunctive criterion (3b absolute per-tier floor) FAILED on magic + mini_boss. The HELD disposition (§ 6-quinquies, § 6-sexies, § 6-septies) holds — and the no-force-pass discipline holds: this is an honest fail, recorded as one, b6 retained. **Decision 2 stays HELD. b6 stays. This is the correct call on the new evidence.**

**The reframe worth surfacing to Matt (NOT premature — this run supplies the evidence for it):** the b6 net on rogue is NARROWER than even § 6-sexies (b)(i) recorded. § 6-sexies established b6 carries the upper tiers on **rogue alone** (the other four cells: b6 co-craters). This run shows that even *that* single-cell rescue is **coordinate-conditional**: on rogue's GENUINE close/single-target coordinates, the b6 arm ALSO co-fails boss (`boss 0.0`, elite `0.1333`) — it only carried boss (`0.967`) on the prior run's medium-range/small-AOE *framing*. So:

> **On rogue's genuine coordinates, b6 is no longer carrying boss either.** The b6 arm here passes ZERO kits too (`b6_pass: 0`). b6's *measured* rescue on this run is mini_boss (`0.533` vs envelope `0.0`) and magic (`1.0` vs envelope `0.05`) — NOT boss. The net is real but smaller and different-tier than the § 6-sexies record assumed.

This invites a **scope reframe of Decision 2 that is worth putting to Matt** (surfacing, not deciding): *delete b6 for the cells/coordinates where the envelope DOES carry, and retain it ONLY for the residual swarm-hot single-target family where it still provides measured tier-completeness.* The argument FOR surfacing it now: the evidence base (rogue genuine-coordinate run + the § 6-sexies four-cell co-broken finding) is now precise enough to say *where* b6 is and is not load-bearing. The argument for treating it as PREMATURE: (a) the residual lever (§3) is unbuilt, and a partial-deletion that leaves b6 only on the swarm-hot ST family is itself a design commitment to NOT solving that family the right way (the spatial/coverage lever) — it bakes the band-aid in; (b) b6 retention is risk-free (Decision 1 was built additive), so there is no *cost* pressure forcing a partial deletion now. **My recommendation: surface the reframe to Matt as an OPTION with the evidence, but recommend AGAINST executing it yet** — a partial deletion gated on the swarm-coverage lever being built is cleaner than a partial deletion that pre-commits to the band-aid. The cleanest sequence remains: keep b6 whole → build/test the swarm-coverage lever (§3 lever A) → re-run G7 → if the envelope then carries the upper tiers WITHOUT b6 across the family, delete b6 whole; if it does not, the architectural per-tier-modifier question (lever B) is the next gate. Do not fragment the net before the real lever is tested.

---

## 5. Disposition + routing

- **The diagnosis:** half-confirmed (composer gap real, closed), half-falsified (necessary-but-insufficient; "entire delta is the floor" / "necessary-AND-sufficient canary" refuted on data). The §3 falsifier FIRED on the physical side. Recorded honestly.
- **The architectural single-global-modifier hypothesis:** RE-OPENED ON EVIDENCE (not silence). The floor-intact-and-still-craters-under-hot-swarm shape evaluated and points at branch 2 for the physical side. This is the first positive signal; § 6-septies's "silence is not clearance" is now superseded by an actual signal on the physical arm.
- **The floor fix:** STANDS. Keep it. Canonical envelope composition behaviour, on its own merits, independent of the b6 coupling. Do NOT revert.
- **The remaining lever:** lives in swarm-side encounter design (spatial/coverage pressure — lever A, my recommended first probe, converges with the § 6-septies caster re-open criterion) OR per-tier modifiers (lever B, the architectural change, the riskier band-aid). NOT in the composer. Design call RESERVED FOR MATT — I locate, I do not build.
- **Decision 2:** HELD. b6 STAYS. Correct on the new evidence. The fixed floor does not change it.
- **Reframe surfaced (not executed):** partial b6 deletion (delete where envelope carries, retain on the swarm-hot ST family) is now evidence-supported enough to put to Matt as an OPTION — but I recommend AGAINST executing it before the swarm-coverage lever is tested, because a partial deletion pre-commits to the band-aid. Keep b6 whole until the real lever is tested.

**Routing:**
- **knight-rider:** Decision 2 stays HELD (unchanged); the floor fix stands (do not sequence a revert); the architectural question is now evidence-backed and is the next design gate, gated on a swarm-coverage lever Matt has not authorized building. Surface the §4 partial-deletion reframe to Matt as an option, with my recommend-against-yet.
- **Matt (RESERVED):** (a) the remaining-lever choice (swarm-coverage encounter mechanic vs per-tier-modifier balance-loop change) — §3; (b) whether to surface/pursue the §4 partial-b6-deletion reframe now or hold for the lever test. Both are design calls above my authority to make; I locate and recommend.
- **gamora:** the G7 HOLD-SIM rogue re-fire is a clean honest-fail; no re-run needed until a new lever is built and there is a new hypothesis to test.
- **rocket:** the floor fix is canonical envelope behaviour now; no composer change is the remaining lever (the lever is swarm-side / balance-loop, not composition).

---

**Signed:** gandalf, 2026-06-15
**For:** reading the G7 HOLD-SIM rogue re-fire (floor fired exactly as designed; envelope arm still craters upper tiers) as the NECESSARY-BUT-INSUFFICIENT outcome — the composer gap was real and is closed (diagnosis confirmed), but the swarm-over-clear → single-global-modifier-floor → upper-tier-crater dynamic is raw single-target throughput that an AoE-share floor does not reduce (the "entire delta is the floor / necessary-AND-sufficient canary" claim falsified on data; the §3 falsifier fired on the physical side); the architectural single-global-modifier hypothesis re-opens on evidence not silence; the floor fix STANDS on its own genre-correct merits; the remaining lever lives in swarm-side spatial/coverage encounter design (converging with the § 6-septies caster re-open criterion) or per-tier modifiers, not the composer; Decision 2 stays HELD and b6 stays (correct on the new evidence), with a partial-deletion reframe surfaced to Matt as an evidence-supported option that I recommend holding until the real lever is tested.
