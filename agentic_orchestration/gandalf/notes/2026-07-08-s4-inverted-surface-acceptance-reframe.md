# §4 Inverted-Surface Design Read — Acceptance-Layer Reframe (Verdict on My Own Criterion)

> **✓ RULED — Matt, 2026-07-08 (same-day, rulings session): OPTION A** ("I agree with option A").
> KPM = the measurement · WR = validity screen · WR-gradient → difficulty ladder (post-demo).
> **Two riders attach to the ruling:** (1) **declared-baseline condition** — the KPM bands are
> calibrated at a NAMED gear state; Matt same-turn surfaced that the gauntlet fights STRIPPED kits
> (spec-gap vs `design-decisions-session.md §7` "validated as geared units") and ruled a geared arm
> onto pilot Leg i (`certification_gear` v0; spec + succession clause:
> `2026-07-08-leg-i-geared-arm-certification-gear-spec.md`) — bands re-fit when the baseline moves;
> (2) **jack-ryan independent review leg still OWED** (self-amended criterion; §7's routing stands).
> Tracker delta: `canonical/current-to-end-state/current-to-end-state-engine.md` 2026-07-08 rulings block.

**Author:** gandalf (DRIFT-CRITIC on own SPEC-AUTHOR work — the conflict seam is the point)
**Date:** 2026-07-08
**Consumes:** R3a step-4 re-run verdict (769 clean-surface cells: 765 ceiling / 4 mid / 0 floor,
ceil-fraction 0.995); gamora tier-1 gate diagnosis (`2026-07-08-r3a-tier1-gate-band-vs-viability-diagnosis.md`);
my §4 criterion (`2026-07-08-spatial-difficulty-levers-design-read.md §4`).
**Routing:** Matt (one ruling ask, §7) + KR (sequencing) + gamora (execution) + jack-ryan (review — I am
amending my own criterion; independent review is mandatory, not optional).
**Disciplines:** #11, #12 (semantic-shift honesty — this note retracts parts of my own prior reads),
Goodhart-guard (§4 self-test, stated in full at §4 below), #23 framing-audit.

---

## TL;DR

- **§4 as written: uncontested FAIL. The criterion, not the engine, was mis-pointed.** I asked the
  WR surface on a SINGLE difficulty rung to show a gradient. The genre says that gradient does not
  live there. On-tier farm content in this genre is cleared by every viable build — discrimination
  is CLEAR SPEED, and the run's own tier-1 KPM data shows that gradient alive and wide (~2.4×
  spread). The instrument did not lose its gradient; **I looked for it on the wrong axis.**
- **Reframe:** tier-1 KPM = the MEASUREMENT. Tier-2 WR = the VALIDITY SCREEN. The WR gradient's
  true home is a difficulty LADDER (per-build wall depth) — which is the descent depth-scaling
  run-model, post-demo machinery.
- **Two real findings survive untouched:** boss_with_adds genuine non-viability (117/189 kits kill
  ZERO mobs — content, not instrument) and the lethality-floor question (mobs that never kill =
  no stakes — a Godot game-feel workstream, not a certification gate).
- **Moving-goalposts self-test passed and shown** (§4): the reframe stands on falsifiable genre +
  in-run data claims independent of the gate outcome, preserves §4's spirit (spread-not-rails, in
  KPM space where it is empirically live), and deletes no finding.

---

## §1 — Verdict on §4-as-authored

My criterion: *"WR surface regains a gradient: mass in (0.05, 0.95); differentials persist as
spread, not rails. NOT 'N/18 pass.'"* The re-run returned 765/769 at ceiling, 4 mid, 0 floor.
By the letter: **FAIL, uncontested.** No re-litigation of the number.

But the criterion was authored against the PRE-un-stack state, where rails at 0.000/1.000 were
**lockout mechanics** — ~65× stacked HP on a fixed clock, total-field convergence at tick 0. In
that regime, rails meant the instrument was broken, and demanding mid-mass was the correct
anti-Goodhart gate. **The un-stack + serial-engagement pass removed the lockout.** What remains at
WR≈1.000 is not lockout — it is a competent endgame population clearing on-tier content. The
criterion did not survive the regime change it was designed to force.

## §2 — Why WR-gradient-on-one-rung was the wrong observable

**Genre evidence (named, per discipline):**

- **Diablo 3, Greater Rift farming:** at farm tier (GR90 when your wall is GR110), every viable
  build clears at ~100% survival. Discrimination between builds is **rifts per hour** — clear
  speed. Death-rate discrimination only appears at the WALL — the highest rung a build can push.
  Blizzard's own leaderboard architecture encodes this: the ladder metric is highest-tier-cleared
  + time, never survival-at-fixed-tier.
- **Path of Exile, mapping:** white/yellow maps are cleared by every build that reaches them;
  the economy metric is maps/hour. GGG balances around clear-speed-vs-tankiness TRADEOFFS, and
  the community measures builds in clear speed. Survival gradient appears only in pinnacle/uber
  content — the ladder's top rungs.
- **The structural reason:** WR on a single fixed rung is near-binary for any competent
  population — you clear it or you cannot meaningfully engage it. Continuous discrimination
  requires either (a) a continuous observable on the rung (time/speed) or (b) a discrete ladder
  of rungs (wall depth). A single-rung WR gradient is the one shape the genre never produces.

**In-run evidence:** tier-1 KPM spread on the SAME surface that failed §4 — open_arena p10/med/p90
= 22.3/31.9/53.8; chokepoint 23.3/35.2/57.1 (gamora's diagnosis note). A ~2.4× clear-speed spread
across the endgame-BC population. **The differential §4 wanted — "spread, not rails" — exists,
one layer down, in the observable the genre actually uses.**

## §3 — The reframe (the amendment I propose)

| Layer | Old role (§4 as authored) | New role (amended) |
|---|---|---|
| Tier-1 KPM | Gate/filter (bands reject before sim) | **THE MEASUREMENT** — per-scenario clear-speed envelope; the discrimination surface |
| Tier-2 WR | The measurement (gradient demanded) | **VALIDITY SCREEN** — clears on-tier ⇒ viable; cannot engage ⇒ flagged non-viable; the WR number beyond that bit is not the discriminant |
| WR gradient | Demanded on one rung | **Lives on the difficulty LADDER** — per-build wall depth; = descent depth-scaling run-model (`gameplay-loop-design`); post-demo instrument |

Note the irony, which is also the reassurance: **the certification architecture already runs on
KPM bands** (`season_emit`, `family_certification_pass` consume band verdicts). The architecture
was right; my §4 overlay demanding a WR-gradient was the mis-point. The amendment is therefore
SMALL: rule that tier-2 WR feeds a validity bit + non-viability flags, not a gradient requirement.
Lever-4 (certification-criterion work) now fires properly scoped: **clear-time bands (discrimination)
+ tier-2 validity (screen) + non-viability flags (content findings).**

## §4 — Moving-goalposts self-test (Goodhart guard, stated in full)

I authored §4; I am amending it after a FAIL. The test I must pass:

1. **Does the amendment stand on claims falsifiable independent of the gate outcome?** Yes:
   (a) the genre claims (§2) are documented design facts about D3/PoE, checkable against my
   Phase-2 research lineage; (b) the KPM spread is measured IN THE SAME RUN that failed §4 —
   the data furnishing the reframe was produced by the gate it reframes.
2. **Does it preserve §4's spirit?** §4's spirit: *differentials persist as spread, not rails.*
   The amendment relocates that requirement to KPM space, where it is empirically satisfied AND
   remains demandable (if KPM spread ever collapses to a point mass, the instrument is dead and
   the amended criterion FAILS).
3. **Does it delete any finding?** No. boss_with_adds non-viability stays flagged. The
   lethality-floor concern stays routed. The 4-mid-cell count stays on record.
4. **What would refute the reframe?** (a) KPM spread collapsing to noise (no discrimination
   anywhere — instrument dead); (b) genre evidence that fixed-rung WR gradients are a real
   ARPG design surface (none exists to my knowledge); (c) playtest evidence that clear-speed
   differentiation reads as meaningless to players (contradicted by the entire seasonal-ladder
   economy of the genre).

## §5 — What survives, what I retract (Discipline #12 — semantic-shift honesty)

- **RETRACT (partial), my G2 concurrence:** "bimodality = positional identity, the design signal
  the engine exists to emit." The DIRECTION was real (corridors favor melee geometry; open ground
  favors kiting range). The AMPLITUDE — 0.000/1.000 rails — was instrument artifact (stacked HP +
  tick-0 total-field convergence), now proven by the un-stacked surface where the floor mass
  vanished entirely. Pattern = signal, amplitude = artifact — my own §2 formula, which I should
  have applied to the bimodality reading too.
- **SURVIVES, my §1 diagnosis:** "the instrument lost its gradient" was TRUE for the pre-un-stack
  state and its levers (un-stack, serial engagement) were the correct fix — the re-run proves they
  removed the lockout. §1's error was only in where the recovered gradient would live.
- **SURVIVES, boss_with_adds:** 182/189 tier-1 reject; **117 kits kill ZERO mobs.** That is not a
  band mis-fit — zero engagement is content non-viability. Real finding, routed to content design
  (§6, parallel lane). Open sub-question for that lane: boss rooms may be mis-instrumented under
  KPM at all — a boss fight's genre observable is TTK + deaths, not kills-per-minute. Fork:
  (a) content state (room over-tuned for non-burst kits) vs (b) instrument scope (KPM wrong
  observable for boss rooms). Likely both. gamora data pull decides.
- **SURVIVES, magic_pack scrutiny:** 153/189 tier-1 rejects (117 below-floor + 36 above-ceiling).
  The band (18.61, 100.00) predates the F2 re-population and never got step-5's density-anchored
  re-derivation. Audit it with the same method before trusting its rejections.
- **NEW ITEM, lethality floor:** on the un-stacked surface mobs rarely kill. A world with no
  death has no stakes — *Reap. Die. Rise.* cannot ship combat where "Die" is vestigial. But this
  is a GAME-FEEL question (dodge layer, player skill, real-time pressure in Godot) — a playtest
  workstream, NOT a sim-certification gate. Routing it into certification would repeat §4's
  mistake in mirror image.

## §6 — The plan to the Godot demo

**Demo-critical chain (serial):**

1. **§4 amendment ratification** — Matt rules on §7's ask; jack-ryan reviews this note (I amended
   my own criterion — independent review required).
2. **Certification re-point (Lever-4, now properly scoped)** — gamora executes: tier-2 WR → validity
   bit + non-viability flags; KPM bands stay the discrimination surface; magic_pack band gets the
   step-5 density-anchored audit. Gate-2 per ADR-004. Small diff — the architecture already
   points this way.
3. **Step-4-bis verdict under amended criterion** — expected PASS on existing run data (no re-run
   needed: KPM spread is live, validity screen is 765/769 viable, flags emitted). Chain unblocks.
4. **R4 / Leg-C fires** (summoner campaign) — with boss_with_adds carried as a FLAGGED scenario
   (its non-viability finding must not silently gate Leg-C; KR sequences whether the content fix
   lands pre- or post-R4 based on gamora's data pull).
5. **R5 VALUES** — Matt touchpoint (band-sheet values, already parked).
6. **§7 loot campaign** → engine emissions → **drax's Godot One-Realm build consumes.**

**Parallel design lane (feeds Godot directly, not chain-blocking):**

- **boss_with_adds content read** — my design read + gamora data pull (which 117 kits; what do
  they share — prediction: the wis/int caster cohort from G2; what's the add composition doing).
- **Lethality/game-feel workstream** — parked to Godot floor-design + playtest with the descent
  ladder; explicitly NOT a certification gate.
- **Difficulty-ladder instrument** (WR-gradient's true home) — design doc when descent
  depth-scaling work fires; post-demo.

**Post-chain cleanup (unchanged):** Option-C consolidation — the four same-family inherited
constants (HP multiplier, leash, density/geometry, band tuples) into one governed per-scenario
difficulty home.

## §7 — Ruling ask (ELICITOR — one fork)

**RULE:** accept the acceptance-layer reframe? — **(A)** YES: tier-1 KPM = measurement, tier-2
WR = validity screen, WR-ladder = post-demo descent instrument; step-4-bis re-verdicts on existing
data; chain proceeds per §6. **(B)** NO — contest: name the observable you believe single-rung WR
should discriminate, and I will design against it.

**My lean: A, firm.** The genre, the in-run data, and the existing certification architecture all
point the same direction; B has no genre precedent I can name.

---

**Sign-off:** gandalf, 2026-07-08. Anchors: R3a step-4 re-run verdict (run-state tail),
gamora tier-1 diagnosis note, `gauntlet_sim.py:405-446` band architecture,
`gameplay-loop-design.md` descent run-model, D3 GR-ladder / PoE mapping design lineage.
