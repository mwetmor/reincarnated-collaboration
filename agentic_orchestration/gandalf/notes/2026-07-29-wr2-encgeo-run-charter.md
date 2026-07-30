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

- **§8.8 — Cell B lands at a ⚑ HALT: S-1 FAILS 321/450, and the defect is the SPEC's** (engine
  `6dca36a`, meta `d8ae0637`, pushed). Build complete and honest — nothing tuned, failure pinned by
  test. Mechanism: every violation involves a wall-clamped body (free-space pairs exact to 1e-12;
  champion tier zero-residual in 90/90); the clamped player's 0.90 share is annulled per pass, gap
  decays `0.90^m`, `0.9^8 = 0.43` survives per tick (worst slack −0.252 m; the recurrence's fixed
  point returns the measured boss speed). **Spec §B-2's prose promised shortfall redistribution its
  own frozen pseudocode never implemented.** Passing gates: S-4 450/450 twice all legs; regression
  name-diff EMPTY (60/6082/21); shuffled-order PASS; D-3 AST sweep 2 hits converted, re-sweep 0.
  Process catch ledgered: first regression came back `added=4` (TestByteIdentity digests caught the
  §B-6 keys emitted unconditionally — dict SHAPE, combat untouched, adjacent suites green the whole
  time); fixed emit-when-armed, battery re-proven byte-identical. Battery `wr2_cell_b_s1/` 141 MB
  on-disk uncommitted, statistics committed (per cell brief).
- **§8.9 — conductor rulings on the HALT** (⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC — the judged
  artifact is this seam's own spec):
  - **R-WR2-16:** resolution **R1 — clamp-aware shortfall transfer** (realized post-clamp
    displacement measured per pass; annulled magnitude transfers to the pair partner, same index
    order). The prose IS the mechanism; the pseudocode was its defective transcription — spec §B-2
    carries the erratum banner. **R2 REFUSED** by spec §E's own line (raising ITER_MAX to pass S-1
    is drift; and Δ→34/56 sweeps is the smell, not the fix). **R3 REFUSED** — S-1 is a pre-registered
    geometric invariant; deferring it post-C is goalpost motion, the exact thing pre-registration
    exists to catch. S-1 predicate, ε_touch, ITER_MAX all UNCHANGED.
  - **R-WR2-17:** SS-B-1 surface-to-surface range applies to **ALL attackers** (mobs and boss too),
    ratifying gamora's build. Mirror-image units bug otherwise: post-B boss↔player separation holds
    at 2.0, a 2.0 m boss melee goes permanently out of range, boss DPS → 0, and S-3's "player still
    killable" dies the same death as the player's side. One law everywhere (R-WR2-12's spirit).
  - **Spec §D-3(3) erratum banked** (gamora's correction ACCEPTED): `list.__contains__` short-circuits
    on identity — the NaN self-miss cannot occur; live hazard is D-3(1) value-equality between
    distinct equal entities. Sweep + index-only law unchanged.
  - **Cell C's flag-OFF baseline pins at `6dca36a`** (same class as INFO-1, adopted).
- **§8.10 — Cell B-FIX fired** (gamora): implement R-WR2-16, re-run S-1 + S-4 + flag-OFF regression +
  unit tests. Gate-2 on the combined B landing follows the fix.

- **§8.11 — Cell B-FIX lands; the HALT clears** (engine `4f09e35`, meta `5bc0fdf6`, pushed).
  **S-1 PASS 450/450** (from 129/450); worst slack −0.000998 m, inside ε_touch and 10× inside the
  gate; zero violating pair-samples. Residual counters 95,852→**7** ticks / 0.28018→**0.0012 m** —
  all 7 are mixed_pack mob↔mob pack chains (seeds 74000801/-16/-24) hitting §B-6's deliberate
  pre-correction over-report; emitted-frame verification shows worst POST-solver overlap ≤ 0.95 mm.
  Reported, not repaired; gamora's own 0-prediction recorded as missed (her call — right one).
  Zero wall-pinned residuals anywhere. S-4 PASS twice all legs; flag-OFF regression name-diff EMPTY
  (60/6084/21 = baseline + 2 new tests); flag-OFF traces byte-identical to `6dca36a` modulo git-hash
  header. HALT battery `wr2_cell_b_s1/` PRESERVED as evidence beside the passing `_r2`. Two process
  catches self-ledgered: mid-run source edit tripping `inspect.getsource` tests, and a `__pycache__`
  race from PARALLEL suites sharing the editable install (Discipline #3 generalization; corroborates
  WR1 INFO-8) → wave-tail item: no parallel pytest against a shared editable install.
- **§8.12 — Gate-2 on the combined Cell B landing FIRED** (jack-ryan; `6dca36a`+`4f09e35` as one
  landing). **Cell C holds for CLEAR.** R-WR2-8/-17 veto window to Matt effectively closes at this
  gate's verdict.

- **§8.13 — Gate-2 on combined Cell B: CLEAR-with-notes; Cell C releases** (jack-ryan, `188ca160`,
  pushed). Name-diff EMPTY (baseline + the 2 judged new tests); frozen-row conformance on every row;
  R-WR2-16 transfer matches the erratum banner clause-by-clause; flag-OFF legacy-verbatim; SS-1
  intact. Falsification pass validated its OWN instrument on the preserved HALT battery first
  (129/450 reproduced to 17 s.f.) then confirmed B-FIX every digit; provenance closed by re-firing
  the armed battery from the clean tree (third determinism replicate — only `engine_git_hash`
  differs). One prose falsification: the worst-slack pair is player↔mob on the SOUTH-WALL clamp
  (residual chain terminates on a corner-pinned player) — conclusions survive, sentences don't.
  **Conductor dispositions:** **WARN-1** (two "no wall involved" claims) → jack-ryan's finding is
  the correction of record; no re-run owed. **WARN-2** (ITER_MAX=8 has ZERO measured headroom — the
  7 residual ticks spent the full budget, and Cell C changes contact geometry) → ITER_MAX stays
  frozen; the §B-6 counters ARE the instrument. Distinction ledgered for the future boundary:
  raising ITER_MAX to pass a GATE is drift (refused at R-WR2-16); raising it to answer a MEASURED
  over-constraint reported by the counters post-C would be a mechanism amendment ruled on evidence.
  Cell C/BAT watch the counters. **WARN-3** (SS-B-2's in-code rationale cites the errata'd NaN
  mechanism on two unflagged default-path changes) → comment correction added to Cell C's build
  obligations (same file). **INFO-AoE ADOPTED into Cell C's brief:** SS-B-1 opens a
  select-but-whiff window for circle AoEs vs the boss (`aoe_radius` 3.0 < selection 3.5) and C's
  preferred-range band walks toward it — named S-3 diagnosis candidate.
- **§8.14 — Cell C (movement policy v2) FIRED** (gamora; spec §C + §D; R-WR2-9/-10/-13/-14; Cell-A
  WARN-1 evade-branch gating + Cell-B WARN-3 comment fix ride along; flag-OFF baseline pins at
  `4f09e35`). Gate owes S-2, S-3, S-4, flag-OFF regression, and the `boss__B__seed74000802`
  trajectory reconstruction — the drift trace must turn.

- **§8.15 — Cell C interrupted by infrastructure, RELAUNCHED.** First Cell C agent died on a
  server-side 529 after ~45 min: zero commits, no cell note, uncommitted WIP across seven engine
  files + one stray. Relaunch carries a STEP-0 WIP triage (default DISCARD-via-stash — the fragment
  stays recoverable as evidence; adopt only if fully auditable) and an incremental-commit
  instruction so a repeat death loses minutes, not the cell. Brief otherwise unchanged. Committed
  base remains `4f09e35`.

- **§8.16 — R-WR2-18 (MATT-SIGNED):** "agreed on 1" — R-WR2-8 + R-WR2-17 (surface-to-surface
  effective range, all attackers) RATIFIED by Matt explicitly; the veto window closes signed, not by
  silence. Standing design statement beyond this run: reach is measured to the body, not the centre.
- **§8.17 — Owner-eye #1 verdict + a NEW owner observation (F-WR2-1, banked, NOT scope-grown).**
  Matt on the smoke render: machinery "makes sense for what it is," AND — "it seems like the player
  does too little damage versus monster health." Disposition: F-WR2-1 is a PACING/TTK observation,
  outside WR2's bounded scope (geometry + observability; R-WR2-6 keeps WR1 grades closed; damage
  tuning builds nothing here). Context that may partially dissolve it: the smoke fight is the
  no-evasion proxy player on the PRE leg (weakest configuration) in a fight selected FOR a death and
  a double nova. Route: (a) S-6's before/after diff (durations, win rates, worst-hit) becomes the
  measured substrate; (b) the AFTER render is the honest re-test — movement v2 changes uptime and
  positioning, so TTK feel legitimately moves; (c) if the too-little-damage feel SURVIVES the AFTER
  watch, TTK/damage-pacing charters as a SEQUEL run candidate on the S-6 evidence. Cheap offer open:
  drax renders a post-leg WIN fight from the banked set for pacing contrast on one word.

- **§8.18 — Cell C lands: S-2 / S-3 / S-4 ALL PASS, first lap, no dials moved** (engine
  `61a6be4`+`ecea69f`, meta `54b437e7`, pushed). **The fight turns:** on the WR1 drift trace the
  player's cumulative heading change goes 3.84 → **150.80 rad (24 circles)**, a full 2π orbit of the
  boss, straightness 0.48 → 0.07; B-only measures 4.07, so C is the mechanism. **S-2:** boss
  wall-share 75.03% → **1.004%** (trash 51.99→0.000, mixed 75.33→0.000); the (0.5,0.5) corner state
  NEVER occurs on any tier. **S-3:** killable / pre-winnable / post-won all hold; the §E table
  untouched; the AoE whiff window never reached for (`band_outer` 0.80 m clear, test-pinned). C-1's
  degeneracy dissolved under R-WR2-17's effective reach, verified. S-4 150/150; regression name-diff
  EMPTY; flag-OFF byte-identity across two trees. Both riding obligations discharged. **WIP-triage
  deviation ACCEPTED as correct:** the relaunched cell ADOPTED the dead agent's fragment against the
  brief's discard-default — but earned it: every changed line audited against spec §C/§D/§E, and
  every MEASURED claim re-derived rather than trusted (the real hazard — MIGRATION carried numbers
  with no battery on disk; one wording did not survive re-derivation and was corrected).
- **§8.19 — conductor dispositions on Cell C's two ⚑ reports:**
  - **F-WR2-2 (`pre_endpoint`/B win rate 0.067 → 0.033 → 0.000).** Not an S-3 predicate (endpoint
    excluded by charter design) but a leg's win rate reached ZERO under the new geometry. REPORTED →
    named line item in S-6; Cell BAT re-measures on the battery of record; grading lap judges it.
    CONNECTED to Matt's F-WR2-1 (damage-feels-low) — same suspect: endpoint boss tuning vs the
    no-evasion proxy. If both survive grading, they charter the sequel run TOGETHER.
  - **F-WR2-3 (the nova goes DARK under `body_separation_v2` — B's effect, not C's; ring 1→0→0 at
    the base commit).** The BEFORE fight fired 132 novas; the boss's signature telegraph vanishing
    changes what Matt watches — it collides with the intent sentence ("worth watching") even though
    S-6 carries it reported-not-gated. Plausible mechanism: R-WR2-8 effective reach makes boss melee
    eligible where it never was, starving nova selection — i.e. the BEFORE novas may have been an
    ARTIFACT of broken geometry (unreachable melee). **DIAGNOSTIC fired (read-only, no build): pin
    the mechanism before Cell BAT.** Bug in the S2S wiring → in-scope fix (B's correctness). Honest
    consequence of fixed geometry → ledger; the AFTER watch judges whether a nova-less boss is
    watchable; if flat, boss-kit-behavior-under-fixed-geometry charters as a sequel (bounded-substrate
    law holds — no boss redesign smuggles into WR2).
  - Residual counters 7 → **180** ticks (all trash, exactly 2 ticks/fight × 90, 17-s.f.-identical,
    worst 0.98 mm, neither body clamped — spawn-adjacency signature) → routed to Gate-2 attention +
    Cell BAT re-report. WARN-2's evidence-boundary not yet reached (overlap inside the 1 mm target).
- **§8.20 — Gate-2 on Cell C + F-WR2-3 nova diagnostic FIRED in parallel** (jack-ryan on the
  committed landing; gamora read-only diagnostic — no tree writes, single-writer law preserved).
  Cell BAT holds for BOTH.

- **§8.21 — R-WR2-19 (MATT-SIGNED) — CHARTER AMENDMENT: Mechanism D, telegraph escapability.**
  Matt, verbatim: *"The telegraph is too fast, it needs to be tuned to be just slower than player
  movement speed. In the current state, there is no reason for the telegraph as the skill damage
  cannot be avoided."* Scope §1 grows a fourth mechanism under founding-authority signature:
  - **Mechanism D (small, parameter-law class):** the nova telegraph-to-detonation window obeys the
    **escape-speed law** — required escape speed from ANY point inside the damage area is just below
    player movement speed: `damage_radius / telegraph_duration = NOVA_ESCAPE_FRAC × player_move_speed`,
    `NOVA_ESCAPE_FRAC` default **0.90**, TUNABLE (the one dial; the law itself frozen). Conductor
    operationalization of "just slower," veto-open: 0.90 means a prompt reaction always escapes, a
    late one pays — the D3-postmortem rule. Duration derives at cast from the CASTER's target-kit
    move speed so it stays deterministic and per-fight-constant.
  - D must RECONCILE the WR1 flag: telegraph draws at 12.0 but `range_m` is 10.0 — the escape law
    binds on the DAMAGE radius; the drawn ring must equal the damage ring (a telegraph that lies
    outward is noise; one that lies inward is a trap).
  - **New pre-registered gate S-7 (escapability):** for every nova firing in the battery of record,
    `(distance from player position at telegraph onset to the damage edge) / telegraph_duration
    ≤ NOVA_ESCAPE_FRAC × player_move_speed`, all firings, analytic from traces. PLUS the M-3
    evade-armed player's realized nova-crossing rate must DROP vs BEFORE (the telegraph now has a
    reason; WR1's M-3 moved 0.000).
  - **Sequencing:** D builds AFTER the F-WR2-3 diagnostic verdict + Cell C's Gate-2 (a dark nova has
    nothing to telegraph — if the diagnostic returns a wiring bug, its fix and D land as ONE gamora
    cell; if honest-selection, D still lands and the diagnostic's numbers say how often it shows).
    Cell BAT then re-verifies S-3's predicates alongside S-1/S-2/S-4 (D moves when damage lands;
    outcome symmetry gets re-checked cheaply from leg reports, not re-gated blind).
  - F-WR2-1 note: a longer fuse shifts endpoint-boss damage later — F-WR2-2's zero-win leg gets
    re-measured AFTER D, not before.

- **§8.22 — F-WR2-3 diagnostic verdict: (b) BUG in the S2S wiring; §8.19's hypothesis (a)
  FALSIFIED** (gamora read-only cell, `e9ff58ac`, pushed; engine tree clean before/after). SS-B-1
  moved the SHARED SELECTOR to surface-to-surface but not the nova's OWN fire gate — the two
  predicates disagree by exactly `target.entity_radius`: selector admits at d=10.2086 ≤ 10.5, cast
  gate refuses > 10.0, and the refusal bills the boss's full 6.0 s action budget; by t=6.8 the
  player has closed to 2.0 and index-0 melee wins every remaining selection. Seed-invariant to every
  printed digit (OFF 6/6 novas, ON 0/6). The conductor's romance ("BEFORE novas were an artifact of
  broken geometry") is dead: **BEFORE novas were the mechanic working**; hypothesis (c) also ruled
  out (`gd_nova.py` reads no radius). Fix described-not-built: flag-condition the cast gate's
  effective range identically to the selector; scratch falsifier 6/6. **DISPOSITIONS:** (i) fix
  lands inside **Cell D** per §8.21's pre-declared sequencing (one gamora cell: nova-gate fix +
  telegraph escape law). (ii) **Gate-escape ledgered for the wave tail:** Cell B's Gate-2 verified
  R-WR2-17 on the selector but no one diffed selector-vs-per-skill-gates — the run caught it via
  owner-render + Cell C's reporting, i.e. §6.2 caught what the gate missed. Gate-2 checklists gain
  "a range-semantics change must be verified at EVERY predicate that consumes range, enumerated by
  grep, not at the shared entry point." (iii) The diagnostic's honest caveat carried forward: the
  fix does NOT reproduce BEFORE nova numbers exactly (fires a tick earlier) and does NOT close
  F-WR2-2 — S-6 diffs against BEFORE stay interpretation-loaded on the nova line.

- **§8.23 — Gate-2 on Cell C: CLEAR-with-notes; conductor dispositions; R-WR2-20; Cell D releases**
  (jack-ryan, `7827fb13`, pushed). Regression name-diff EMPTY vs the 81-name baseline; flag-OFF
  byte-identity re-proven; the trajectory turn verified under BOTH stall conventions (3.84 or
  7.43 → 150.80 — INFO-1); flip triggers grep-complete (three disjuncts, no fourth); the 180
  residual ticks independently confirmed as spawn-adjacency (worst 0.98 mm, WARN-2's evidence
  boundary NOT reached). Five WARNs, six INFO, none blocking. **Conductor dispositions:**
  - **WARN-4 + WARN-5 RATIFIED TOGETHER (⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC — the judged fork is
    in this seam's own spec): SS-C-3 stands; spec §C-1 is the operative text.** Post-R-WR2-17,
    §C-0's prose and §C-1's radial rule name DIFFERENT sets; the builder implemented §C-1, and
    §C-0's literal reading would have left the band measure-zero post-B — a no-op inside a
    mechanism chartered to end a no-op. Erratum banner added to spec §C-0 (this landing's commit).
    **WARN-5 disposed name-and-pin, NOT repair** (jack-ryan's recommendation, adopted): the
    residual HOLD annulus `d ∈ (1.70, 2.00]` vs standard-radius targets (129 ticks, 0.096% of
    armed ticks) is named in the erratum with its TUNABLE coupling (`BAND_WIDTH` moves it; any
    band-touching tuning lap re-measures it). Closing it by widening REPOSITION's claim is a
    mechanism change no gate is asking for.
  - **WARN-1/-2/-3 + INFO-1/-4 ride Cell D as doc/pin obligations, zero behavior change:** flip
    clock named as REPOSITION-tick-clock in the math note + pinned with one test (WARN-1 — the one
    dial-facing item; `FLIP_DWELL_S` tuning reads that clock); AoE whiff-window clearance corrected
    0.80 → **0.30 m** at the note/test seam (WARN-2); MIGRATION §5 restated by field name
    (`total_abs_turn_rad`, path-derived — WARN-3); stall-convention + `azimuth_reversals` deadband
    docstrings (INFO-1/-4). WARN-5's one-fact line in the math note rides too.
  - **INFO-5 ADOPTED: Cell BAT's flag-OFF byte-identity baseline pins at `ecea69f`**, not `4f09e35`
    (the statistics report carries one more key; same class as Cell B's INFO-1).
  - **R-WR2-20 (conductor, veto-open) — Cell D flag topology:** the nova cast-gate fix rides
    **`body_separation_v2`** — it is the COMPLETION of R-WR2-8/SS-B-1 (one range law at every
    predicate that consumes range), not a new mechanism; a third flag there would let the two
    predicates disagree by flag state, which is the bug's shape. The telegraph escape-speed law
    (Mechanism D) gets its **own new flag `nova_telegraph_v2`, default OFF** — it is a new
    parameter law, not a repair, and S-7 must be attributable to it in isolation. Cell BAT arms
    all three.

- **§8.24 — Cell D lands: ALL PASS; F-WR2-3 CLOSED; conductor rulings on its four ⚑ items** (engine
  `28386b26`/`b35695c0`/`796a6f6d`, meta `3f1e71a4`, pushed). The nova fires again under the one
  range law: cast gate 6/6 at d=10.2086 ≤ 10.5, `n_nova_crossings` 0 → 1 on the five seeds Cell C
  measured dark. Range-predicate sweep: **19 sites, exactly ONE out of law** — the nova's private
  reach gate was the only per-skill REACH predicate downstream of the shared selector; the class is
  closed, not just the instance. Mechanism D: T = 12.0/(0.90×5.75) = **2.319 s** vs the measured
  0.750 (3.09×), zero RNG, per-fight-constant. S-7 spot-check 5/5, worst ratio-to-bound 0.149,
  matching the math note's a-priori table to 15 s.f. Flag-OFF byte-identity vs `ecea69f` exact
  (SHA-256, all 6 traces); regression name-diff EMPTY 81/81; 69/69 new tests, 223/223 across
  B+C+D+nova; all six riding obligations discharged, zero behavior change; residual counters
  UNCHANGED by D. Process catch self-ledgered: comment-only mid-regression edit → killed and
  re-ran against the final tree (the Cell B-FIX lesson, applied unprompted). **Rulings:**
  - **R-WR2-21 (conductor, veto-open) — S-7 clause 2 stays; Cell BAT gains the instrument to
    measure it.** M-3 is dark on the battery of record (`piloted_competence_m3: null`), so the
    evade-armed crossing-rate clause is unmeasurable without an arm — dropping the clause is
    goalpost motion (refused, same law as R-WR2-16 R3). Cell BAT adds a **paired M-3 evade-armed
    arm** (BEFORE flags-off / AFTER flags-on, same seeds). Pre-named FIRST SUSPECT if the rate
    does not drop (R-WR2-13 pattern): `ACTIONABLE_WINDOW_S = 0.70` caps the evade budget
    identically in both arms — D reaches the clause through telegraph tick count (8 → 24), not
    budget. That constant is **M-graded, outside spec §E: any change HALTs to Matt.** A measured
    non-drop with the mechanism pinned is a processable finding judged at grading, veto-open —
    not a silent gate edit.
  - **Ring reconciliation disposition RATIFIED as name-and-pin:** drawn ring already equals damage
    ring (one constant, four readers); the WR1 flag was a naming collision across two record
    blocks, not a lying telegraph. Nothing moved; the pin is the test.
  - **FOOTPRINT classification RATIFIED:** the circle-AoE select-but-whiff window stays open on a
    classification argument (blast extent ≠ reach to a body), not convenience. INFO-AoE watch item
    stands; harmless on this fixture (no circle skill in the boss kit).
  - **ADOPTED: Cell BAT's flag-OFF REPORT baseline pins at `796a6f6d`** (`wave_regime` gains two
    unconditional keys); trace byte-identity remains vs `ecea69f`, verified. Third occurrence of
    the class — standing rule named: *report-baseline pins at the latest landing; trace-identity
    pins at the mechanism baseline.*
  - **ADOPTED: the S-7 onset tick is `tick`, NOT `tick − 1`** (gamora's own falsifier: at
    `tick − 1` the distance 10.7836 exceeds the cast gate's 10.5 ceiling — the telegraph could not
    exist there; the wrong convention loosens the gate 32%). Cell BAT's grading script MUST use
    `tick`; no downstream transcript of the earlier draft survives unaudited.
- **§8.25 — Gate-2 on Cell D FIRED** (jack-ryan; landing = the three engine commits as one; the
  §8.22(ii) range-semantics checklist law gets its first enforcement — independent re-enumeration
  of the 19-site sweep). **Cell BAT holds for CLEAR.**

- **§8.26 — Gate-2 on Cell D: CLEAR-with-notes; an erratum against §8.24's own ground; Cell BAT
  releases** (jack-ryan, `6a720545`; pushed with this landing). Every obligation independently
  reproduced, several by stronger routes: only **three** sites in all of `simulation/` consume a
  target radius in a range predicate and all three are surface-aware — no fourth site COULD be out
  of law; T re-derived to exact IEEE-754 round-trip; his own S-7 grader agrees 5/5 to gamora's last
  printed digit; flag isolation proven by source partition; regression 60/6197/21 name-diff EMPTY.
  Five WARNs (one family: true where measured, incomplete where generalized), five INFO, no BLOCK,
  no Matt escalation. **Conductor dispositions:**
  - **⚠ ERRATUM against §8.24 (append-only; the ledger does not rewrite):** the FOOTPRINT
    ratification's parenthetical ground — "no circle skill in the boss kit" — is **FALSE** (WARN-2;
    origin jack-ryan's own Cell-C finding, propagated by gamora, ratified by me: three hands, one
    unchecked premise — the same failure shape as the §8.22 (ii) gate-escape). The boss's index-1
    skill IS circle geometry (`primordian_frigidring_r4`, range 10.0); the window is shut by the
    `_gd_nova` intercept at spatial_engine.py:6003, not by kit absence. **The disposition STANDS**
    (FOOTPRINT ≠ REACH, reported-not-repaired — jack-ryan re-affirms) but the ledger item's true
    trigger is *a circle-geometry skill WITHOUT a `_gd_nova` block* and its magnitude is
    `(3.5, 10.5]` = **7.0 m**, not 0.5 m. Watch item re-armed with corrected trigger + magnitude;
    gamora corrects the four propagated sites (rides Cell BAT).
  - **R-WR2-21's FIRST-SUSPECT arithmetic corrected (WARN-3):** `t_remaining` decays per tick, so
    the 0.70 s cap binds only at the first tick — ACTING ticks are **5 → 21** (not 8 → 24),
    executed-reach ceiling 2.59 → 11.61 m. D reaches clause 2 MORE strongly than reported;
    designation unchanged, ground corrected so Cell BAT's grader cannot mis-diagnose a non-drop.
    Nothing tuned; `ACTIONABLE_WINDOW_S` stays M-graded.
  - **S-7 field contract corrected for the gate of record (WARN-4):** onset tick = `tick`; the
    player joins via header `is_player == true` → `entity_id` (tick-record entity blocks carry no
    `is_player`); the telegraph record is `record_type: "event"` / `event: "telegraph"`. Cell BAT's
    grading script writes against THIS contract; jack-ryan's grader is the existence proof. gamora's
    two MIGRATION/math-note join-fact lines approved directly by jack-ryan under ADR-002.
  - **Spec is re-made the one home (WARN-5, SPEC-AUTHOR):** §E-D tunable/frozen rows + §G-D
    obligation class folded into the mechanism spec (this landing's commit) — a tuning lap reading
    §E now finds D's wall where §8.23 ruled walls live.
  - **INFO-1 ADOPTED as a named grading gap:** the escape law's one free input `v = 5.75` is an
    UNGRADED engine default filling an absent kit field. No repair in-run; Cell BAT emits per-fight
    `v` in the leg header; the S-6/grading lap carries "3.09× / 1.57 s are default-specific" as a
    consumer caveat (drax's tell-animation warning stands). INFO-2 (bank the four-tier counter
    table + regression name list) and INFO-3/-4 (label/convention one-liners) ride Cell BAT;
    INFO-5's ADR-004 acknowledgements route to star-lord + drax at AFTER-baton delivery.
- **§8.27 — Cell BAT (battery of record) FIRED** (gamora): BEFORE (flags OFF) / AFTER (all three
  armed) + the R-WR2-21 paired M-3 evade arms, `_trace_decisions` armed; S-1/S-2/S-4 recomputed,
  S-3 re-verified from leg reports, **S-7 both clauses** on the corrected contract; report baseline
  `796a6f6d`; leg headers carry the R-WR2-15(2) unit payload + per-fight `v`; residual counters
  re-reported and banked; S-6 raw diff substrate emitted (durations, per-leg win rates incl.
  F-WR2-2's `pre_endpoint`, worst-hit, nova counts — interpretation-loaded per §8.22 (iii),
  `total_displacement` per §D-7). Grading + AFTER-baton hold for its Gate-2.

- **§8.28 — Cell BAT interrupted by infrastructure (529), RELAUNCHED — and the §8.15 discipline
  paid.** The agent died server-side ~24 min in, but the incremental-commit law (imposed after Cell
  C's zero-commit death) turned the wreckage into two AUDITABLE landed units: `5a236697` (BAT math
  note — the two emissions defined, S-7's instruments separated, jack-ryan's 5→21 re-derived) and
  `21abff12` (emissions build — R-WR2-15(2) per-leg unit + INFO-1 per-fight `v` with its grade).
  No battery started, no tracked WIP, no orphan processes, no cell note. Relaunch ADOPTS the two
  commits after verification-read (committed work is the auditable case; the §8.18 fragment-adoption
  standard applies with the audit already half-done by git) and resumes at the battery arms.
  Loss: minutes, exactly as designed.

- **§8.29 — Cell BAT lands: THE BATTERY OF RECORD, every pre-registered gate PASS, tuning lap
  expires UNSPENT** (engine `f1ab3b09`/`284aacaf`/`82f01917`/`d05535f9` atop the adopted
  `5a236697`/`21abff12`, meta `144cbb4d`/`22f54914`, pushed; three spawn-529s + one status-page
  incident — "all models recovered except [ours]" — cost ~4 h wall-clock and zero work). Numbers of
  record: **S-1** 450/450, 292,305 pair samples, 0 violations, worst slack −0.000989 m. **S-2** boss
  wall-share 75.032% → **2.722%**, final-10 s 98.046% → **4.222%**, corner 65.989% → **0.000%**,
  4/4 tiers. **S-3** holds, lap unspent. **S-4** 150/150 twice. **S-7 clause 1** 132/132, worst
  ratio 0.1493 = the a-priori prediction to 15 s.f. **S-7 clause 2** crossing rate 1.000 → **0.000**
  (firings 66 → 66 — the nova fires as often and lands NEVER on the piloted player). Residuals:
  AFTER 180 ticks/1.3506 mm (all trash, 2/fight), BEFORE 0. `v` audit: 900/900 at the ungraded
  default 5.75. Name-diff EMPTY 81/81. **Conductor rulings:**
  - **F-WR2-4 (new finding, banked): clause 2 passed by a mechanism §8.21 did not describe.** The
    M-3 player escapes by OUTRUNNING THE RING'S REACH (12.22–12.78 m vs the front expiring at
    12.0 m — movement-v2 orbit carries it out of the nova's world entirely), not by in-window
    radial escape; the transition is 100% → 0% with no middle — not "prompt reaction escapes, late
    one pays." The GATE stands as pre-registered (rate must drop; it dropped, honestly measured;
    the policy earned it). What is NOT yet empirically demonstrated is the telegraph's graded
    penalty texture — clause 1 certifies it analytically for a player inside the ring; no arm
    SAMPLES that regime. Routed to the grading lap; sequel-run candidate ALONGSIDE F-WR2-1/F-WR2-2
    (the three share the endpoint-boss/pacing suspect space). `NOVA_ESCAPE_FRAC` untouched; no
    re-gate; no scope growth. Corollary ledgered: **S-7 clause 1's population is degenerate in
    onset geometry** (132 firings, ONE distinct `d_onset` = 10.2086) — the law-residual and
    identity checks are configuration-independent so the gate is not weakened, but analytic
    coverage is a point, not a distribution; distributional coverage needs varied fixtures =
    sequel space, named.
  - **F-WR2-2 CONFIRMED at full grain** (`pre_endpoint` boss/B 0.067 → **0.000**) and the §8.17
    F-WR2-1 substrate delivered (player-LOSS boss fights end ~15% sooner; player-WIN ~2% longer)
    — both to the grading lap as chartered.
  - **STEP-0 deviation RATIFIED — and the conductor's own audit hole owned:** §8.28's "no tracked
    WIP" was literally true and materially incomplete — a 1,258-line UNTRACKED driver
    (`wr2_cell_bat_2026_07_29.py`, mtime post-death) existed and MY wreckage audit filtered it
    with the pre-existing untracked junk. The cell caught it, audited three ways
    (structural/API/empirical), corrected two wrong comment claims, adopted under the §8.18
    standard. Amendment to the interruption drill: **wreckage audits diff untracked files by mtime
    against the death window; wholesale `??`-filtering is the hole.**
  - **BQ-3 door discharge ACCEPTED; routed to Gate-2 as its FIRST checklist item.** The name-diff
    law caught the adopted driver opening the calibration-override door undeclared (+1); the cell
    proved the door MANDATORY by falsification both ways (closing it raises
    `CalibrationOverrideLeak` AND deletes the M-3 arm), then discharged via `_DOOR_ALLOW_LIST`
    declaration — third occurrence of a twice-accepted class, regression re-run on the final tree.
    I judge a containment declaration for the cell's OWN new file to sit inside
    report-don't-repair. The cell asked for this call to be second-guessed; jack-ryan's
    independent read IS the standing safety for exactly this concentration — if he reads it as a
    repair that owed a HALT, the revert is one line and the finding says so.
- **§8.30 — Gate-2 on Cell BAT FIRED** (jack-ryan; the six BAT commits as one landing).
  **Grading + AFTER-baton hold for CLEAR.**

- **§8.31 — Gate-2 on Cell BAT: CLEAR-with-notes; BQ-3 concurrence; two errata against this
  ledger's own grounds; grading + AFTER-baton RELEASE with WARN-1 gated ahead of the baton**
  (jack-ryan, `dfb83982`; pushed with this landing). Every gate reproduced on his own instruments
  to the last printed digit; his S-2 scanner validated on BEFORE's known-failing tiers before a
  PASS was trusted; S-4 widened past the claim — **all 450 banked traces regenerate from the
  current tree with `engine_git_hash` the only differing field** (provenance + empirical
  zero-behavior-change in one stroke). **BQ-3: concurrence, no HALT owed** — he falsified both
  limbs himself, enumerated exactly four door sites tree-wide via T-8's own AST sweep, and named
  the decisive category: the offending line was THIS cell's own commit, so the declaration is
  landing-completion (one's own MIGRATION entry), not repair of another's state. 6 WARN, 6 INFO,
  no Matt escalation. **Conductor dispositions:**
  - **⚠ ERRATUM to F-WR2-4 (WARN-2, the gate's check on the conductor — accepted):** §8.29 named
    the carrier and not the enabler. His isolation arms (which the battery lacks): B+C with D dark
    → rate **0.955**, never past 11.43 m; **D alone → 0.516**, reaches 12.06 m; both → **0.000**
    at 12.19–12.78 m. The orbit is the PATH; **D's 3.09× fuse is what makes it long enough** — and
    a graded middle EXISTS along the mechanism-isolation axis; "no middle" is true only along
    reaction-timing. Consequence pinned: a tuning lap reading the old wording would reach for C's
    dials when `NOVA_ESCAPE_FRAC` is doing most of the work. F-WR2-4's sequel routing unchanged;
    its causal text is hereby the WARN-2 version.
  - **⚠ ERRATUM to the residual LABEL (WARN-5 — jack-ryan filing against his own Cell C finding):**
    "spawn-adjacency" is FALSE ON ORIGIN — zero overlapping pairs at tick 0 anywhere; the
    sub-zero samples occur at ticks 28–262 during melee and the worst-slack pair spawns 17.90 m
    apart. It is a **contact-solver ε residual**. Lineage of the unchecked premise: §8.19 → his
    Cell C finding → §8.23 → the BAT note — four hands, second consecutive gate where a ratified
    GROUND was false while the disposition stood. His new standing habit (re-measure causal labels
    at the next gate that touches them) ADOPTED into this run's Gate-2 obligations; pattern-class
    noted for the wave tail (grounds-vs-dispositions audit discipline).
  - **⚠ ERRATUM to §8.29's own sentence:** "corrected two wrong comment claims" — ZERO were
    corrected (WARN-4: the driver's self-refuting "derived, not transcribed" comment survives at
    :82-84; the second item was confirmed-correct, never wrong).
  - **WARN-1 GATED discharge (the baton does not ship before it):** the three new cross-seam
    emission keys have four comments citing a MIGRATION entry that does not exist (ADR-004 — and
    the emission exists precisely so drax stops hard-coding). Content pre-approved under ADR-002.
    Fired as a gamora micro-cell TOGETHER WITH: the WARN-4 one-line comment fix, WARN-3's banking
    of the clause-2 distances (a conductor finding's substrate must be reproducible from the
    tree, as INFO-2's residual table is), and the INFO-2 falsifier-cite fix.
  - **WARN-6 wave-tail item:** 3-for-3 on a 20-minute regression catching what a 9.21-second
    containment suite catches — cheap-suite-first sequencing enters the cell-brief template.
- **§8.32 — WARN-discharge micro-cell FIRED** (gamora, doc/bank-only). Grading synthesis +
  AFTER-baton authoring follow; the baton ships only after §8.32 lands CLEAN.

- **§8.33 — WARN-discharge micro-cell LANDED CLEAN on its gate set; baton gate OPEN; one
  conductor ruling on the M-3 half** (gamora; engine `36ea2a5c`/`33c134b2`/`74a5a5c5`/`54536c30`,
  meta `fee39348`; conductor pushes with this landing). WARN-1: the ADR-004 MIGRATION entry
  shipped — keys by exact name/type/unit, provenance semantics (`kit` vs `engine-default-ungraded`
  5.75, neither M nor D), drax's decomposer named as the 207.40/235.40 consumer, and the
  `movement_speed_ms` collision between Cell D's conditional trace field and the unconditional
  report field disambiguated so nobody joins the wrong two things. WARN-4: the self-refuting
  "derived, not transcribed" comment replaced with a recorded correction (order is TRANSCRIBED;
  grep-the-builder drift-proof per INFO-4's convention). INFO-2: set-difference proof into the
  allow-list comment; erratum appended to the BAT cell note §9.1. Verification: containment 39/39
  (9.07 s final tree, cheap-suite-first), WR2 B/C/D + kitcal slice 185/1.00 s, py_compile +
  import OK, `AFTER_SUFFIX` and all six `leg_dir()` paths unchanged, door allow-list 3 entries /
  4 sites / 0 offenders. **Conductor dispositions:**
  - **R-WR2-22 (veto-open): the M-3 half of WARN-3 is declared OUT-OF-RUN.** The cell proved the
    12.1944–12.7789 m figures are NOT extractable from any banked file — they are the M-3
    (`piloted_competence`) arms, built in-process, writing no trace directory; M-3 is dark on the
    battery of record BY CHARTER DESIGN. What IS banked
    (`wr2_bat_f_wr2_4_ring_life_distances.json`) reproduces jack-ryan's PROD-AFTER limb at every
    printed digit (4.0619–5.3358 m, 132/132, r\* 4.4306 at full precision) on an independently
    written instrument, plus the BEFORE_prod arm. Closing the M-3 half requires an instrumented
    `s7_clause2` re-run = driver change + simulation execution = scope growth on a doc/bank-only
    cell gating a baton. Ruling: the M-3 substrate's durable home is jack-ryan's pushed finding
    (`dfb83982` §4.1 — his own instrument, both rows adjacent in his table); the instrumented
    re-run routes to the F-WR2-4 SEQUEL space, where distributional clause-1 coverage (§8.29
    corollary) already lives. **Substrate clarification pinned to F-WR2-4: its 12.19–12.78 m
    escape figures are M-3 isolation-arm values; the production battery's banked ring-life
    distances are 4.06–5.34 m** — the grading lap reads both rows from the finding, not from
    memory.
  - **⚑ WARN-1 count erratum ledgered (the gate's own ground, third instance of the class):**
    "four comments cite the missing entry" — the file carries ONE (`kitcal_g5_harness.py:700`);
    the other four cite entries that exist. Gap real, multiplicity not; §8.31 transcribed the
    figure and this brief repeated it — corrected on measurement in the MIGRATION entry's own §7
    rather than transcribed a third time. Same family as WARN-5: true where measured, wrong where
    labelled. The wave-tail grounds-vs-dispositions item gains its third exhibit.
  - **Tail (outside the §8.31 gate set, NOT baton-gating):** WARN-5's cell-note-site edit and
    INFO-5's one-liner (jack-ryan §14 gamora list) remain open — the WARN-5 substance is
    discharged charter-side (§8.31 erratum). Fired as a doc-only tail micro-task alongside the
    grading lap; lands before run close, not before the baton.
- **§8.34 — Grading synthesis + AFTER-baton authoring FIRED** (named gandalf sub-agent per
  conductor-economics §2.1; the run's largest synthesis piece). Deliverable: S-6 BEFORE/AFTER
  verdict + the F-WR2-1/-2/-4 evidence book + drax consumer notes + the baton document. The baton
  ships on its landing; then drax renders; then Matt's watch closes the run.

- **§8.35 — Grading synthesis LANDED; S-6 verdict of record banked; four conductor rulings; two
  errata; the §8.33 tail discharged** (synthesis: gandalf sub-agent `726efe3b`, 803 lines at
  `gandalf/notes/2026-07-30-wr2-grading-synthesis-after-baton.md`; tail: gamora `81c328a8` —
  WARN-5 cell-note strike + INFO-5 −3.0% loosening landed WHILE the synthesis was being written,
  so its §4.2 lists them open; they are not). **S-6 VERDICT OF RECORD: PASS on all four decidable
  §0 intent clauses at full battery grain** — corner-pin 65.989% → 0.000%, hard combined-radii
  floor (292,305 samples / 0 violations), aim-lines live with drift turning 3.84 → 150.80 rad,
  telegraph escapable on both S-7 clauses — with "worth watching" deferred BY DESIGN to Matt's
  watch and the price named: held-loss boss fights −13.8…−18.0%, EIGHT fights flipped WIN→LOSS,
  every surviving win slightly longer. Instrument validated against six independently banked
  facts before any conclusion. **Conductor dispositions (all four §4.3 recommendations RULED,
  veto-open):**
  - **R-WR2-23: the missing S-6 column is ADOPTED as S-6's fourth column, computed at the grading
    lap.** Nova-crossing quantum histogram `{1×:30, 2×:14}` → `{1×:12, 2×:32}`, all three legs;
    mean intake per nova-carrying fight **+84.85 HP** (`pre`/`post`) / **+96.30 HP**
    (`pre_endpoint`) = 11.2–12.7% of the player's pool in one event. **⚠ ERRATUM-class process
    miss, §8.22(ii) family one level up:** a PRE-REGISTERED diff column went uncomputed through
    four cells and two gates — verified where computed, never computed where registered. No CLEAR
    re-opens (no gated predicate moves; worst-hit genuinely still); a **courtesy-read
    verification routes to jack-ryan IN PARALLEL with the baton, not gating it** — the number
    informs Matt's sequel decision, and this run's standard is that no number of record reaches
    Matt on one instrument. Wave-tail rule candidate: every pre-registered column names its
    computing cell at registration.
  - **⚠ ERRATUM to the §8.19/§8.29 sequel routing (fourth true-where-measured/wrong-where-labelled
    exhibit — first in a ROUTING rather than a mechanism ground):** the three findings do NOT
    share one suspect space. F-WR2-1's five catastrophic flips are nova-quantum-driven on `pre`
    (1×→2×, boss at 43–56% HP when the player dies); F-WR2-2's two flips are **nova-free**
    knife-edge losses on `pre_endpoint` (boss at 9.0/10.0% HP). The sequel question Matt rules on
    is therefore TWO mechanisms, not one cluster — presented as such in the evidence book.
  - **INFO-3 death-2 band: ledgered UNMEASURED, run closes without measuring it** (S3a was a
    win-rate proxy by charter design; the artifact self-declares the substitution; carried into
    baton §3.4-3 so no consumer leans on it).
  - **INFO-4 BEFORE traces: NOT banked for the baton, said out loud** — deterministic
    regeneration + SS-1's freeze covers AFTER/WR1 evidence only; `git clean` exposure flagged to
    drax in §3.1. Standing offer: if Matt asks for a BEFORE/AFTER split-screen watch, banking
    becomes cheap insurance and the conductor rules then.
- **§8.36 — BATON DELIVERED (exit-predicate step 2 of 4).** Charter pushed with this landing;
  drax cell FIRED against baton Part 3: swap the 450 AFTER traces, retire the 207.40/235.40
  hard-codes via the MIGRATION keys, honor the 2.32 s tell caveat, render the §3.7 pick
  (`pre/boss__B__seed74000802`, duration-invariant — geometry isolated from pacing) with its
  cautions, file the ADR-004 acknowledgement. jack-ryan courtesy read fired in parallel
  (R-WR2-23). star-lord's ADR-004 acknowledgement (ack-only, nothing to ship) fired as a
  micro-task. Then: **Matt watches. The charter closes when that holds or Matt halts.**

*Charter closes when the exit predicate holds or Matt halts. — gandalf, RUN-CONDUCTOR*
