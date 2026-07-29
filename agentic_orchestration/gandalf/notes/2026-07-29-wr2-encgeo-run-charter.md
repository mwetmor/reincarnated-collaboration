# WR2-ENCGEO-2026-07-29 — the encounter-geometry run: the 3 updates

**Conductor:** gandalf (`RUN-CONDUCTOR`) · **Chartered:** 2026-07-29 · **Authority:** Matt, verbatim
**"Go ahead and run with the 3 updates"** (= founding ruling **R-WR2-1**, MATT-SIGNED), issued against
the conductor's three-tier sizing at the WR1 baton hold. Predecessor: WR1-2026-07-28 (TERMINAL at
§8.30; hold resolved by supersession). Pattern: `operating-procedures/desirable-run-pattern.md` —
all four fit-test answers YES (bounded substrate = WR1's banked battery + the 2026-07-26 werewolf
fixture; decidable targets = §3 predicates; forks pre-drained §2; design authority resident).

## §0 — Intent sentence (rubric-law anchor; diff every predicate against this)

**Make the sim's fight worth watching AND more faithful to the fixture in the same stroke: the
player AI stops resolving boss fights in a corner, combatant bodies stop overlapping, and the
traces carry aim-lines — then re-bank, re-grade, and hand drax an AFTER baton whose depicted fight
is the one Matt watches.** The owner's question is fidelity-to-his-own-play, not cosmetics: the
fixture (Matt's werewolf run) kited, circled, and dodged — it never wall-pinned and never stood
inside the boss.

## §1 — The three mechanisms (bounded scope; nothing else builds in this run)

| # | Mechanism | Class | Seam |
|---|---|---|---|
| **A** | Aim-line emission — arm `_trace_decisions` in a SUPPLEMENTARY emission from the banked WR1 battery (same seeds/tree class); zero kernel change | small | gamora |
| **B** | Combatant collision — pairwise separation resolution at tick close: centre-distance ≥ rᵢ+rⱼ, all combatant pairs, deterministic order-stable relaxation, arena clamp still outermost | kernel | gamora |
| **C** | Movement policy v2 (player) — fixture-anchored melee repositioning: lateral strafe/orbit replaces linear back-off (tangential component with sign persistence + occasional flip); wall-repulsion steering term rising inside a boundary band; preferred-range band per kit class | kernel + design | gamora, to conductor spec |

Conductor authors the mechanism spec for B + C (named gandalf sub-agent, from the design rulings in
§2) BEFORE either build cell fires. Cell A needs no spec — it is a flag and a falsifier.

## §2 — Pre-drained forks (conductor rulings, veto-open; the ELICITOR pass)

- **R-WR2-2:** Cell A's supplementary set must prove **non-perturbation**: fight content byte-matches
  the banked battery modulo the added `decision` events (digest on non-decision content). If the flag
  perturbs outcomes, that is a FINDING and Cell A halts — observation must not change the fight.
- **R-WR2-3:** Collision resolves **all combatant pairs** (player↔mob AND mob↔mob) — GD resolves
  both; half-collision would invent a third physics no game has. Dead bodies exempt (carcasses don't
  block; matches GD).
- **R-WR2-4:** Movement v2 designs to the FIXTURE, not to prettiness: the acceptance shape is
  orbit-and-reposition melee (Matt's measured play), not ranged kiting. The 5.62 m figure stays
  retired; the preferred-range band derives from post-collision contact (≥ 2.0 m combined radii).
- **R-WR2-5:** Same seeds (74000800×30), same legs (pre / pre_endpoint / post), same arms, same
  36×36 arena. The arena is NOT scope (walls-the-sim-respects beyond the clamp stays sequel-of-the-
  sequel); only the policy's wall-AWARENESS is in scope.
- **R-WR2-6:** WR1's grades are NOT re-opened. G-A closed at its MISS (P-1, Matt-ratified) — the
  mitigation finding is untouched by geometry. Only the G-B-shaped outcome symmetry re-grades here
  (§3 S-3), because movement legitimately moves outcomes.

## §3 — Decidable target-state (pre-registered gates; goalposts pinned before results)

| Gate | Predicate (checkable in-run) |
|---|---|
| **S-1** separation | min pairwise combatant separation ≥ combined radii − 1 cm, every tick, all 450 fights |
| **S-2** de-cornering | player wall-contact share ≤ **5%** of player-alive ticks per tier (WR1 BEFORE: 75% boss) AND no terminal corner-pin state (final-10-s wall share ≤ 20%) |
| **S-3** outcome symmetry (the honorable-fallback gate) | no-evasion player still KILLABLE at the death-2 band; win still REACHABLE on the pre leg; post leg still won. A FAIL here is a processable finding → one declared tuning lap (policy parameters only, mechanisms frozen), then re-gate |
| **S-4** determinism | battery byte-reproducible at fixed seed, twice |
| **S-5** aim-lines | supplementary set carries ≥1 `decision` event per player-attack fight; R-WR2-2 digest holds |
| **S-6** before/after diff | full diff table vs WR1 banked battery (durations, win rates, worst-hit, nova-crossing histogram) — REPORTED, not gated; movement is EXPECTED to move these |

**Exit predicate:** S-1..S-5 GREEN + Gate-2 per landing + AFTER baton emitted (WR1 baton's consumer
notes updated where geometry changed them: separation triple, interpenetration note DELETED as
repaired, corner-pin note replaced by measured wall-share) + **Matt watches the AFTER boss fight
render** (owner-eye, §5).

## §4 — Cells + sequencing (per-landing law; Gate-2 between every build and the next)

1. **Cell A** (gamora) — aim-line supplementary emission + R-WR2-2 falsifier. FIRES NOW (parallel with spec).
2. **Cell SPEC** (named gandalf sub-agent) — mechanism spec for B + C from §2 rulings. FIRES NOW.
3. **Cell B** (gamora) — collision build + tests → Gate-2.
4. **Cell C** (gamora) — movement v2 build + tests → Gate-2. (B before C: policy tunes against real contact geometry.)
5. **Cell BAT** (gamora) — full battery, S-1..S-4 computed (cell computes, conductor grades) → Gate-2.
6. **Grading + AFTER-baton** (named gandalf sub-agent) → **Matt watch**.

**Parallel, non-blocking (Godot seam, drax):** playback-machinery build against the WR1 banked
baton — trace loader, ArenaDatum spawn frame, transform playback, telegraph/floater rendering via
the per-leg decomposer constants, R-WR1-21 wall-face dressing. Schema-identical to AFTER traces;
swap-in when they land. **Mid-run owner-eye (pattern §6.2): Matt gets a machinery smoke render
BEFORE the AFTER traces exist** — render lies caught early, on cheap traces.

## §5 — Matt interface (declared pre-launch)

Red-flag pings only, mid-run. Two scheduled eyes: (1) machinery smoke render (any banked trace,
drax cell); (2) the AFTER boss-fight render — the run's exit. Commitment-boundaries reserved to
Matt: S-3 FAIL's second tuning lap (first lap is pre-authorized), any charter amendment, the watch
verdict. Everything else rules in-run, veto-open, ledgered below.

## §6 — Standing safeties

Preregistration (§3 pinned) · independent Gate-2 per landing (jack-ryan; full-regression
name-diff law — "adjacent suites green" is not the criterion, WR1 §8.19 lesson) · SS-1: WR1's
banked battery/baton/grading record are FROZEN (BEFORE-evidence); AFTER artifacts land beside,
never over · veto-open ruling ledger (R-WR2-n, appended §7) · single-writer: engine tree = gamora
cells only, sequential · conductor writes no production code — seams execute.

## §7 — Ruling ledger (append-only)

- **R-WR2-1 (MATT-SIGNED):** "Go ahead and run with the 3 updates." Founding authority.
- R-WR2-2..-6: §2 above, conductor, veto-open.

*Charter closes when the exit predicate holds or Matt halts. — gandalf, RUN-CONDUCTOR*
