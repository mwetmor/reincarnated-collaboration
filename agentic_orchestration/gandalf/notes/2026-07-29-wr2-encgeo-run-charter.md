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
- **R-WR2-7..-14 — the Cell-SPEC fork drain** (spec: `2026-07-29-wr2-mechanism-spec.md` §F; all
  conductor, veto-open). Context the spec forced (§0, adopted as the run's mechanism record): the sim
  ALREADY resolves collision at a mis-set 80%-of-contact setpoint (`SOFT_COLLISION_FRACTION` 0.8 ×
  2.0 = the measured 1.600 flat), and the player has NO contact-range movement policy at all — the
  "kite-drift" is the boss bulldozing a motionless puck. B replaces a wrong law; C fills a no-op.
  - **R-WR2-7 (OQ-1):** split law is **area-weighted (r²)** — the boss wins the shove (player takes
    0.90 vs boss). Genre-unanimous (D2 Baal, PoE size-asymmetric body-block, GD Nemesis); degenerates
    to 50/50 at equal radii.
  - **R-WR2-8 (OQ-2) — ⚑ THE ONE MATT SHOULD EYE (moves damage-side outcomes):** attack range goes
    **surface-to-surface**: `effective_range = range_m + target.entity_radius`, gated to
    `body_separation_v2` (B creates the units problem; the fix travels with B's flag). Without it, a
    2.0 m melee skill vs the 1.5 m-radius boss is permanently out of range once separation holds —
    player boss-DPS → 0 and S-3 fails on a units bug no tuning can reach. Fidelity ground: Matt's
    fixture melee reached the werewolf's BODY, not its centre; D2/GD/PoE convention. Veto reverts to
    spec option (a) or (c) with the lap budgeted for the FAIL.
  - **R-WR2-9 (OQ-3):** REPOSITION does **not** suppress the attack (C-6). A sidestep is not a trade;
    EVADE remains the only uptime-costing motion.
  - **R-WR2-10 (OQ-4):** flip trigger is **state-driven, zero RNG draws** (wall / dwell / target-change,
    debounced). A wall-answering flip reads as intention on the render; zero draws is zero S-4/S-6 risk.
  - **R-WR2-11 (OQ-5):** **S-2 is a post-C gate only.** Cell B's Gate-2 grades S-1 + S-4 + flag-OFF
    byte-identical full regression + the D-2 shuffled-order test + the D-3 identity-membership grep
    sweep. B alone provably worsens the corner pin (90/10 bulldozer) — a correct B must not be read
    as a regression.
  - **R-WR2-12 (OQ-6):** **one split law everywhere** (mob↔mob included). Boss shoves its own adds
    aside; a second law would be a third physics.
  - **R-WR2-13 (OQ-7):** boss wall-awareness **out of scope** (R-WR2-4: player only). Ledgered as the
    FIRST SUSPECT if S-2 fails post-C; the lap's first two dials are `WALL_PUSH_FRAC` / `WALL_BAND_M`.
  - **R-WR2-14 (OQ-8):** **two flags** (`body_separation_v2`, `movement_policy_v2`), both default OFF.
    B provable in isolation; the S-3 lap moves C without touching B.
  - Spec §E's tunable/frozen wall and §G's per-cell Gate-2 obligations are ADOPTED as charter law;
    §D-7 (`total_displacement` semantics shift) added to the S-6 diff table as a named line item.

## §8 — Landing log (per-landing law: push → bank → report)

- **§8.1 — Cell SPEC banked** (`26f812b1`, rulings `ad6bd378`). Spec §0 adopted as mechanism record:
  the sim ALREADY collides at a mis-set 80%-of-contact setpoint (1.600 = 0.8×2.0, the measured flat);
  the player has NO contact-range policy (motionless from first contact; the "drift" is the boss
  bulldozing). Eight forks ruled R-WR2-7..-14; R-WR2-8 (surface-to-surface range) flagged to Matt,
  veto window open until Cell B's Gate-2.
- **§8.2 — Cell A COMPLETE, all five items PASS** (engine `c8ef0ba`/`6b13b25`/`9bfbdda`, meta
  `96a26365`, pushed). Zero kernel change CONFIRMED — the instrument existed since BW-1; the G-5
  harness had simply never threaded it. Aim battery at `output/kitcal_g5/wr1_battery_2_aim/` (145 MB,
  committed per wr1_battery_2 precedent); **R-WR2-2 non-perturbation PASS 450/450** (declared digest;
  raw digest 0/450 proves the comparison live; sole exclusion `header.engine_git_hash`, inspected
  field-list == declared set); **S-5 holds all three legs** (450/450 attack fights ≥1 decision;
  decision count == tick count exactly); determinism 150/150 twice (first attempt caught a `-dirty`
  straddle — cell re-fired clean rather than explained away). SS-1 asserted mechanically; banked
  battery untouched. **Cell-C datum banked:** `advance` = 1,680 per leg, IDENTICAL across all three
  regimes (6/7/11/16 ticks per fight), then HOLD forever — independent corroboration of spec §0.2.
- **§8.3 — Gate-2 on Cell A fired** (jack-ryan; harness threading + driver are code landings; §4
  per-landing law). Cell B holds until CLEAR.

- **§8.4 — drax playback machinery COMPLETE; owner-eye #1 READY** (godot `4f69e93`+`7e0507a`, pushed;
  cell note banked by conductor — found untracked, arm-3c precedent). Trace loader / leg registry /
  decomposer / playback scene land additive (`replica_playback.gd` untouched; the shared parser gains
  a `g5_header` arm it lacked). Smoke MP4: `reincarnated-godot/tmp/wr2/wr2_smoke_pre_boss_A_74000802.mp4`
  — 658 frames/21.93 s vs footer 22.0 s; a 2×207.40 crossing (the decomposition-exercising case), the
  drift, the (0.5, 0.5) pin, a death. Coverage 5/5 record types; `leech` STUB (fires at healed 0.0 —
  drawing it is a lie); `decision` SCHEMA-READY, dark until AFTER. Decomposer reproduces the banked
  crossing histogram `{1×:30, 2×:14}` on all legs. **§6.2 vindicated: three render lies caught on
  cheap traces** (settle window ate the nova every seed; two floaters collapsed near the view axis;
  parallel fade tween rendered N−1 of N).
- **§8.5 — R-WR2-15 (conductor, veto-open): dispositions on drax's five baton ambiguities.**
  (1) `leech` consumer note ADDED to the AFTER-baton obligations (stub stands; healed-0.0 events do
  not draw). (2) **Per-leg unit payload moves to its right owner:** Cell BAT emits it in the leg
  report/header of the AFTER battery — emission metadata, not fight content; the presentation seam
  stops hard-coding 207.40/235.40. (3) AFTER-baton documents telegraph `damage_amount` ≠ decomposed
  payload, by field name. (4) Emission behavior stands (dead entities DROP from frames — frozen
  instrument); AFTER-baton documents it, renderer carries corpses at last-known position (carcass
  render is presentation's call; matches R-WR2-3's carcasses-don't-block). (5) AFTER-baton documents
  tick 0 as post-resolution.

- **§8.6 — Gate-2 on Cell A: CLEAR-with-notes** (jack-ryan, `cf64c696`, pushed). Regression name-diff
  EMPTY both directions (81/81, T8 absent, full 24 m suite); kernel-untouched confirmed on the strong
  form (whole `spatial_gauntlet/` diffs to the harness alone); R-WR2-2 refalsified with NO a-priori
  exclusions (72 stratified pairs, recursive field-diff → `engine_git_hash` ×72, nothing else); S-5
  refalsified on a decision-free denominator; default-OFF proven at artifact level with an
  independent paired battery. Cell-C datum STRENGTHENED: `advance` is seed- AND arm-invariant —
  exactly 6/7/11/16 ticks in all 450 fights. **Conductor dispositions:** **WARN-1** (second, ungated
  `frame_sink.decision` at spatial_engine.py:4258 on the evade branch — unreachable today, but Cell C
  touches that branch) → ADDED to Cell C's build obligations: gate or unify it under
  `_trace_decisions` so the flag names a trace-content invariant, not a battery arm. **INFO-1** →
  ADOPTED: Cell B's flag-OFF byte-identity baseline pins at **`9bfbdda`+**, not pre-landing (the
  report key emits unconditionally now). Remaining 7 INFO ledgered in the finding; none blocks.
- **§8.7 — Cell B (collision) FIRED** (gamora; spec §B + §D + R-WR2-7/-8/-11/-12/-14; Gate-2
  obligations per spec §G as adopted in §8.1, baseline per INFO-1).

*Charter closes when the exit predicate holds or Matt halts. — gandalf, RUN-CONDUCTOR*
